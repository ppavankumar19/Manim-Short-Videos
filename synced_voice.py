"""Pause-anchored word timing for the Gemini Zephyr voiceover.

manim_voiceover maps every `<bookmark>` (and the exported SRT) through the
speech service's `word_boundaries`. The Gemini service derives those purely
from character counts spread over the clip, which drifts badly from the real
speech (measured on this project: mean sentence-pause error 5.1 s, max 18.8 s).

This module re-derives the boundaries from the REAL audio instead:

  1. read the cached narration wav and find its actual speech blocks
     (silence >= ~0.22 s splits blocks), using a plain numpy envelope,
  2. split the narration's words across those blocks with a dynamic program
     that matches each group's spoken weight to its block's duration,
  3. place each word proportionally inside its block.

`install_synced_voiceover(scene)` wraps the scene's voiceover so every
tracker gets these real timings (same audio file, same voice -- only the
timeline is corrected).
"""
from __future__ import annotations

import re
import wave
from pathlib import Path

import numpy as np
from manim import logger
from manim_voiceover.helper import remove_bookmarks

RES = 10_000_000  # manim_voiceover AUDIO_OFFSET_RESOLUTION


# ------------------------------------------------------------------ audio ---
def _read_wav_mono(path: Path):
    with wave.open(str(path), "rb") as w:
        sr, nch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(w.getnframes())
    if sw == 2:
        data = np.frombuffer(raw, dtype="<i2").astype(np.float32)
    elif sw == 1:
        data = (np.frombuffer(raw, dtype=np.uint8).astype(np.float32) - 128.0) * 256.0
    elif sw == 4:
        data = np.frombuffer(raw, dtype="<i4").astype(np.float32) / 65536.0
    else:
        raise ValueError(f"unsupported sample width: {sw}")
    if nch > 1:
        data = data.reshape(-1, nch).mean(axis=1)
    return sr, data


def speech_blocks(path: Path, frame_ms: float = 20.0, min_pause: float = 0.22,
                  rel_thr: float = 0.10, abs_thr: float = 45.0,
                  min_speech: float = 0.10) -> tuple[list[tuple[float, float]], float]:
    """Real speech blocks in `path` -- gaps shorter than `min_pause` are
    treated as word gaps and joined, longer ones are genuine pauses."""
    sr, data = _read_wav_mono(path)
    dur = len(data) / sr
    frame = max(int(sr * frame_ms / 1000.0), 1)
    usable = len(data) // frame * frame
    if usable == 0:
        return [], dur
    rms = np.abs(data[:usable]).reshape(-1, frame).mean(axis=1)
    thr = max(float(rms.max()) * rel_thr, abs_thr)
    speech = rms > thr
    segs: list[list[float]] = []
    start = None
    for i, s in enumerate(speech):
        t = i * frame / sr
        if s and start is None:
            start = t
        elif not s and start is not None:
            if t - start >= min_speech:
                segs.append([start, t])
            start = None
    if start is not None and dur - start >= min_speech:
        segs.append([start, dur])
    merged: list[list[float]] = []
    for seg in segs:
        if merged and seg[0] - merged[-1][1] < min_pause:
            merged[-1][1] = seg[1]
        else:
            merged.append(seg)
    return [(s, e) for s, e in merged], dur


# ------------------------------------------------------------- alignment ---
def _word_weight(word: str) -> float:
    """Rough spoken length: syllable count from vowel groups (min 1)."""
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 1.0
    syl = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and syl > 1:
        syl -= 1
    return float(max(syl, 1))


def align_words(input_text: str, blocks: list[tuple[float, float]],
                duration: float) -> list[dict] | None:
    """Return word boundaries (service format) aligned to the real blocks."""
    cleaned = remove_bookmarks(input_text)
    tokens = [(m.group(), m.start(), m.end()) for m in re.finditer(r"\S+", cleaned)]
    if not tokens or len(blocks) < 2 or len(blocks) > len(tokens):
        return None

    n, k = len(tokens), len(blocks)
    weights = np.array([_word_weight(t[0]) for t in tokens], dtype=np.float64)
    cum = np.concatenate([[0.0], np.cumsum(weights)])
    total_w = float(cum[-1])
    durs = np.array([e - s for s, e in blocks], dtype=np.float64)
    total_d = float(durs.sum())
    if total_w <= 0 or total_d <= 0:
        return None

    inf = float("inf")
    dp = [[inf] * (n + 1) for _ in range(k + 1)]
    back = [[0] * (n + 1) for _ in range(k + 1)]
    dp[0][0] = 0.0
    for j in range(1, k + 1):
        for i in range(j, n - (k - j) + 1):
            best, arg = inf, j - 1
            for p in range(j - 1, i):
                prev = dp[j - 1][p]
                if prev == inf:
                    continue
                cost = prev + abs((cum[i] - cum[p]) / total_w - durs[j - 1] / total_d)
                if cost < best:
                    best, arg = cost, p
            dp[j][i] = best
            back[j][i] = arg
    if dp[k][n] == inf:
        return None

    splits = []
    i = n
    for j in range(k, 0, -1):
        p = back[j][i]
        splits.append((p, i))
        i = p
    splits.reverse()

    bounds: list[dict] = []
    for (a, b), (bs, be) in zip(splits, blocks):
        wsum = float(cum[b] - cum[a])
        span = be - bs
        for idx in range(a, b):
            frac0 = (cum[idx] - cum[a]) / wsum if wsum > 0 else 0.0
            frac1 = (cum[idx + 1] - cum[a]) / wsum if wsum > 0 else 1.0
            word, cs, _ = tokens[idx]
            bounds.append({
                "audio_offset": int(round((bs + span * frac0) * RES)),
                "text_offset": cs,
                "word_length": len(word),
                "text": word,
                "boundary_type": "Word",
            })
    bounds.append({
        "audio_offset": int(round(duration * RES)),
        "text_offset": len(cleaned),
        "word_length": 1,
        "text": "",
        "boundary_type": "Word",
    })
    return bounds


# ------------------------------------------------------------- scene hook ---
class _SyncedCM:
    def __init__(self, scene, cm, text: str | None = None):
        self.scene = scene
        self.cm = cm
        self.text = text

    def __enter__(self):
        tracker = self.cm.__enter__()
        # The speech cache is keyed on the words alone (bookmarks are stripped
        # before hashing), so a cached clip carries the input_text of the FIRST
        # synthesis.  Any later edit to the bookmark layout -- splitting a
        # window, adding a mark -- would then ask the tracker for a mark its
        # stored text does not contain, and manim-voiceover raises.  Hand the
        # tracker the text this scene is actually speaking.
        if self.text:
            tracker.data["input_text"] = self.text
        try:
            _retime(self.scene, tracker)
        except Exception as exc:  # never let timing refinement break a render
            logger.warning(f"[synced_voice] keeping service timings: {exc}")
        return tracker

    def __exit__(self, *exc):
        return self.cm.__exit__(*exc)


def _retime(scene, tracker) -> None:
    data = tracker.data
    cache_dir = Path(getattr(scene.speech_service, "cache_dir", "media/voiceovers"))
    wav_name = data.get("final_audio") or data.get("original_audio")
    if not wav_name:
        return
    wav = cache_dir / wav_name
    if not wav.exists():
        return
    blocks, dur = speech_blocks(wav)
    aligned = align_words(data["input_text"], blocks, dur)
    if not aligned:
        logger.warning("[synced_voice] not enough speech blocks; keeping service timings")
        return
    data["word_boundaries"] = aligned
    tracker._process_bookmarks()  # recompute bookmark times from real audio


def install_synced_voiceover(scene) -> None:
    """Wrap `scene.voiceover` so every narration clip is timed against the
    real audio it will play."""
    original = scene.voiceover

    def voiceover(text=None, **kwargs):
        return _SyncedCM(scene, original(text=text, **kwargs), text)

    scene.voiceover = voiceover

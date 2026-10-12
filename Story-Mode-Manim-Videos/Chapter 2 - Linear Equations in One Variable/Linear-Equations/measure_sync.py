"""Measure the real voice-vs-timeline drift for equation_anatomy_story.

For every cached narration WAV:
  - detects real speech segments and real PAUSES (silence >= 0.25 s) from
    the audio envelope (pure numpy, no subprocesses), and
  - compares them with the word timings the Gemini TTS service hands to
    manim_voiceover (which is what the bookmarks, animations and the SRT
    are all built from).

Reports per beat: audio duration, word-midpoint-in-pause rate, and the
ordered sentence-pause alignment error (heuristic pause position vs the
real pause position).
"""
from __future__ import annotations

import re
import sys
import wave
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
_ROOT = next(p for p in _HERE.parents
        if (p / "speech_service.py").exists())
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from manim import config  # noqa: E402
config.renderer = "cairo"

from gemini_speech_service import GeminiZephyrSpeechService  # noqa: E402
from equation_anatomy_story import NARRATION  # noqa: E402

VO_DIR = _HERE / "media" / "voiceovers"
NO_BM = re.compile(r"<bookmark mark='[^']+'/>")


def slug(text: str, n: int = 40) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", NO_BM.sub("", text).lower()).strip("-")
    return s[:n]


def find_wav(text: str) -> Path | None:
    stem = slug(text)
    best = None
    for p in VO_DIR.glob("*.wav"):
        if p.stem.startswith(stem[:34]):
            best = p
            break
    return best


def read_wav(path: Path):
    with wave.open(str(path), "rb") as w:
        sr = w.getframerate()
        raw = w.readframes(w.getnframes())
    return sr, np.frombuffer(raw, dtype=np.int16).astype(np.float32)


def speech_and_pauses(path: Path, frame_ms: float = 20.0,
                      min_pause: float = 0.25):
    sr, data = read_wav(path)
    dur = len(data) / sr
    frame = max(int(sr * frame_ms / 1000.0), 1)
    usable = len(data) // frame * frame
    rms = np.abs(data[:usable]).reshape(-1, frame).mean(axis=1)
    thr = max(rms.max() * 0.10, 50.0)
    speech = rms > thr
    segs: list[list[float]] = []
    start = None
    for i, s in enumerate(speech):
        t = i * frame / sr
        if s and start is None:
            start = t
        elif not s and start is not None:
            segs.append([start, t])
            start = None
    if start is not None:
        segs.append([start, dur])
    # merge segments separated by less than min_pause (those are word gaps)
    merged: list[list[float]] = []
    for seg in segs:
        if merged and seg[0] - merged[-1][1] < min_pause:
            merged[-1][1] = seg[1]
        else:
            merged.append(seg)
    pauses = [(merged[i][1], merged[i + 1][0]) for i in range(len(merged) - 1)]
    return merged, pauses, dur


def heuristic_words(text: str, dur: float):
    svc = GeminiZephyrSpeechService.__new__(GeminiZephyrSpeechService)
    cleaned = NO_BM.sub("", text)
    wbs = GeminiZephyrSpeechService._calculate_word_boundaries(
        svc, cleaned, int(dur * 10_000_000))
    return [(w["text"], w["audio_offset"] / 10_000_000) for w in wbs
            if w.get("text", "").strip()]


def main() -> None:
    from synced_voice import align_words, speech_blocks
    print(f"{'beat':14s} {'dur':>6s} | {'OLD word-silence':>16s} | "
          f"{'NEW word-silence':>16s}")
    old_fracs: list[float] = []
    new_fracs: list[float] = []
    for piece, text in NARRATION.items():
        wav = find_wav(text)
        if wav is None:
            print(f"{piece:14s} (no cached wav found)")
            continue
        sr, data = read_wav(wav)
        dur = len(data) / sr
        frame = max(int(sr * 0.02), 1)
        usable = len(data) // frame * frame
        rms = np.abs(data[:usable]).reshape(-1, frame).mean(axis=1)
        thr = max(float(rms.max()) * 0.10, 50.0)
        silent = rms <= thr

        def word_silence(seq):
            """Mean fraction of each word's interval that is real silence."""
            fr = []
            for wtext, t in seq:
                wlen = max(len(wtext) / 13.0, 0.08)
                a = int(t / 0.02)
                b = max(a + 1, int((t + wlen) / 0.02))
                seg = silent[a:min(b, len(silent))]
                if seg.size:
                    fr.append(float(seg.mean()))
            return fr

        old = word_silence(heuristic_words(text, dur))
        blocks, bdur = speech_blocks(wav)
        aligned = align_words(text, blocks, bdur)
        aw = ([(b["text"], b["audio_offset"] / 10_000_000) for b in aligned
               if b.get("text", "").strip()] if aligned else [])
        new = word_silence(aw) if aw else []
        old_fracs.extend(old)
        new_fracs.extend(new)
        ot = f"{100 * np.mean(old):.0f}%" if old else "n/a"
        nt = f"{100 * np.mean(new):.0f}%" if new else "n/a"
        print(f"{piece:14s} {dur:6.2f} | {ot:>16s} | {nt:>16s}")

    print(f"\nOLD heuristic: words spend {100 * np.mean(old_fracs):.0f}% of their "
          f"time in real silence (n={len(old_fracs)})")
    print(f"NEW aligned:   words spend {100 * np.mean(new_fracs):.0f}% of their "
          f"time in real silence (n={len(new_fracs)})")


if __name__ == "__main__":
    main()

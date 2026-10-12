"""Narration audio for Chapter 2, Episode 1.

VOICE  : Google Gemini ``Zephyr`` -- the same voice the newest videos in this
         repo use (see the voiceover caches under the Chapter 2 maths topics).
TIMING : genuine per-word offsets measured from the *audio itself*.

Why this module exists
----------------------
The Gemini TTS API returns audio only -- no timestamps.  So
``gemini_speech_service._calculate_word_boundaries()`` invents them by
spreading each clip's duration across its words in proportion to character
count.  Measured against real audio, that estimate is off by 0.03-0.79 s per
clip, and it is worst on exactly the material this episode is made of:
numerals, token IDs (``27746``, ``8582``) and symbols (``CAPITALIZATION``,
``##``).

edge-tts, by contrast, emits real ``WordBoundary`` events straight from the
synthesiser.  So we take the Zephyr *voice* and the edge *recording*, and
align them:

  1. synthesise the line with Zephyr (cached, shared with the repo's own
     ``GeminiZephyrSpeechService`` cache),
  2. measure that clip's real duration and its leading / trailing silence
     with ffmpeg's silencedetect,
  3. synthesise the same line with edge-tts -- whose per-word onsets are
     known exactly from its WordBoundary events,
  4. dynamic-time-warp the two *recordings* against each other on their
     log-mel spectra, which maps every edge word onset onto the actual
     moment Zephyr speaks it.

The result: Zephyr's sound, with word timings that come from the rendered
audio itself rather than from an estimate.  Everything is cached on disk, so
re-renders never re-synthesise, re-decode or re-align.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

from manim import logger
from manim_voiceover._typing import VoiceoverData
from manim_voiceover.helper import remove_bookmarks
from manim_voiceover.services.base import (
    PathLike, SpeechService, initialize_speech_service, path_to_string,
)

HERE = Path(__file__).resolve().parent

# `gemini_speech_service.py` lives at the repo root and the .env holding
# GOOGLE_API_KEY sits beside it, so make both reachable no matter which
# directory manim is invoked from.
_REPO_ROOT = HERE.parent.parent
for _p in (str(_REPO_ROOT), str(HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

try:
    from dotenv import find_dotenv, load_dotenv
    load_dotenv(find_dotenv(usecwd=True) or (_REPO_ROOT / ".env"))
    load_dotenv(_REPO_ROOT / ".env")
except Exception:  # pragma: no cover - dotenv is optional
    pass

from gemini_speech_service import DEFAULT_MODEL, GeminiZephyrSpeechService

try:
    import edge_tts
except ImportError:  # pragma: no cover
    edge_tts = None

TIMING_DIR = HERE / "media" / "narration_timing"
VOICEOVER_DIR = HERE / "media" / "voiceovers"

# The timing donor.  only used for *offsets*; its audio is thrown away.
EDGE_TIMING_VOICE = "en-GB-RyanNeural"

_AUDIO_OFFSET_RESOLUTION = 10_000_000  # 100 ns ticks, matching manim-voiceover


# --------------------------------------------------------------- caching ---
def _key(*parts: object) -> str:
    raw = "||".join(str(p) for p in parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def _read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=1), encoding="utf-8")


# ------------------------------------------------------- real edge timing ---
async def _edge_stream(text: str, audio_path=None) -> list[dict]:
    """Stream edge-tts, keeping the WordBoundary events and, when
    ``audio_path`` is given, the audio itself.

    The audio is what makes true alignment possible: the boundary list alone
    can only be *resampled* onto the Zephyr clip, while the recording can be
    warped against it.
    """
    communicate = edge_tts.Communicate(
        text, EDGE_TIMING_VOICE, rate="+0%", pitch="+0Hz",
        boundary="WordBoundary",
    )
    out: list[dict] = []
    search = 0
    fh = open(audio_path, "wb") if audio_path else None
    try:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                if fh is not None:
                    fh.write(chunk["data"])
                continue
            if chunk["type"] != "WordBoundary":
                continue
            word = chunk["text"]
            idx = text.find(word, search)
            if idx == -1:
                idx = search
            else:
                search = idx + len(word)
            start = chunk["offset"] / _AUDIO_OFFSET_RESOLUTION
            end = (chunk["offset"] + chunk.get("duration", 0)) / _AUDIO_OFFSET_RESOLUTION
            out.append({"text_offset": idx, "start": start, "end": end})
    finally:
        if fh is not None:
            fh.close()
    return out


def edge_curve(text: str) -> list[dict] | None:
    """Real per-word edge-tts offsets for `text`, cached on disk.

    Returns ``None`` only if edge-tts is genuinely unavailable, in which case
    the caller falls back to a proportional estimate so a render never dies.
    It retries first: this curve is not just the timing source, it is also
    what tells :func:`take_is_plausible` how long the line *should* take, and
    a transient failure here would silently disable that check.
    """
    if edge_tts is None:
        return None
    path = TIMING_DIR / f"edge_{_key(EDGE_TIMING_VOICE, text)}.json"
    cached = _read_json(path)
    if cached is not None:
        return cached
    for attempt in range(1, 4):
        try:
            curve = asyncio.run(_edge_stream(text))
            if len(curve) >= 2:
                _write_json(path, curve)
                return curve
            logger.warning(f"[timing] edge donor returned {len(curve)} "
                           f"boundaries for {text[:40]!r}")
        except Exception as exc:  # noqa: BLE001 - offline / voice changed
            logger.warning(f"[timing] edge-tts timing donor failed "
                           f"(attempt {attempt}/3): {exc}")
        time.sleep(1.0 * attempt)
    logger.warning("[timing] falling back to a proportional estimate")
    return None


# --------------------------------------------------- audio envelope probe ---
def audio_envelope(path: Path) -> dict:
    """Measure a clip: duration, leading/trailing silence, and every pause.

    Measured, not assumed.  Zephyr clips commonly open with 0.2-0.3 s of
    silence, and if that is not accounted for every word in the clip is
    placed too early.  The internal pause list is what lets us snap a word
    that was placed *inside* a silence back onto the moment speech resumes.
    """
    empty = {"duration": 0.0, "lead": 0.0, "trail": 0.0, "gaps": []}
    try:
        stat = path.stat()
        stamp = f"{stat.st_size}:{int(stat.st_mtime)}"
    except OSError:
        return empty

    cache_path = TIMING_DIR / f"env_{_key(path.name, stamp)}.json"
    cached = _read_json(cache_path)
    if cached is not None:
        return cached

    duration = 0.0
    try:
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(path)],
            capture_output=True, text=True, check=True,
        )
        duration = float(probe.stdout.strip())
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"[timing] ffprobe failed on {path.name}: {exc}")
        return empty

    lead = trail = 0.0
    gaps: list[list[float]] = []
    try:
        sil = subprocess.run(
            ["ffmpeg", "-v", "info", "-i", str(path), "-af",
             "silencedetect=noise=-40dB:d=0.08", "-f", "null", "-"],
            capture_output=True, text=True,
        ).stderr
        starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", sil)]
        ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", sil)]
        for i, start in enumerate(starts):
            end = ends[i] if i < len(ends) else duration
            if start <= 0.05:
                lead = max(0.0, min(end, duration))
            elif end >= duration - 0.05:
                trail = max(0.0, duration - start)
            else:
                gaps.append([start, end])
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"[timing] silencedetect failed on {path.name}: {exc}")

    result = {"duration": duration, "lead": lead, "trail": trail, "gaps": gaps}
    _write_json(cache_path, result)
    return result


# ----------------------------------------- audio-aligned word timing --------
# Resampling the edge timing curve assumes the two voices pace a sentence the
# same way; they do not, and the residual shows.  The fix aligns the two
# *recordings* of the same sentence: DTW over log-mel spectra maps the edge
# clip (whose word onsets are known exactly) onto the Zephyr take, so every
# word timing is measured from the rendered voice itself.

_SR = 16000
_HOP = 0.010          # seconds between feature frames
_N_FFT = 400          # 25 ms windows
_N_MELS = 26
_BAND = 150           # DTW band width in frames (~1.5 s)


def edge_audio_path(text: str) -> Path:
    return TIMING_DIR / f"edge_audio_{_key(EDGE_TIMING_VOICE, text)}.mp3"


def ensure_edge_audio(text: str) -> Path | None:
    """The edge donor *recording* for `text`, cached on disk."""
    path = edge_audio_path(text)
    if path.exists() and path.stat().st_size > 500:
        return path
    try:
        asyncio.run(_edge_stream(text, str(path)))
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"[timing] edge donor audio failed: {exc}")
        return None
    if path.exists() and path.stat().st_size > 500:
        return path
    return None


def _decode_mono(path: Path, target_sr: int = _SR) -> np.ndarray:
    """Decode any audio container to a mono float32 signal at ``target_sr``."""
    import av
    container = av.open(str(path))
    resampler = av.AudioResampler(format="s16", layout="mono", rate=target_sr)
    chunks: list[np.ndarray] = []
    try:
        for frame in container.decode(audio=0):
            for out in resampler.resample(frame):
                # to_ndarray returns (channels, samples); flatten to 1-D
                chunks.append(out.to_ndarray().reshape(-1))
        for out in resampler.resample(None):  # flush
            chunks.append(out.to_ndarray().reshape(-1))
    except Exception:  # noqa: BLE001 - flush() raising on some builds
        pass
    if not chunks:
        raise RuntimeError(f"no audio decoded from {path.name}")
    return np.concatenate(chunks).astype(np.float32) / 32768.0


def _mel_filterbank(n_mels: int, n_fft: int, sr: int) -> np.ndarray:
    def hz2mel(f):
        return 2595.0 * np.log10(1.0 + f / 700.0)

    def mel2hz(m):
        return 700.0 * (10.0 ** (m / 2595.0) - 1.0)

    pts = mel2hz(np.linspace(hz2mel(0.0), hz2mel(sr / 2), n_mels + 2))
    bins = np.floor((n_fft + 1) * pts / sr).astype(int)
    fb = np.zeros((n_mels, n_fft // 2 + 1))
    for i in range(n_mels):
        for k in range(bins[i], bins[i + 1]):
            fb[i, k] = (k - bins[i]) / max(bins[i + 1] - bins[i], 1)
        for k in range(bins[i + 1], min(bins[i + 2] + 1, fb.shape[1])):
            fb[i, k] = max((bins[i + 2] - k) / max(bins[i + 2] - bins[i + 1], 1), 0.0)
    return fb.astype(np.float32)


def _logmel(audio: np.ndarray, sr: int = _SR):
    hop = int(sr * _HOP)
    if len(audio) < _N_FFT:
        return None
    n_frames = 1 + (len(audio) - _N_FFT) // hop
    if n_frames < 3:
        return None
    frames = np.lib.stride_tricks.sliding_window_view(audio, _N_FFT)[::hop]
    frames = frames[:n_frames]
    win = np.hanning(_N_FFT).astype(np.float32)
    spec = np.abs(np.fft.rfft(frames * win, _N_FFT))
    mel = _mel_filterbank(_N_MELS, _N_FFT, sr)
    feats = np.log(np.maximum(spec @ mel.T, 1e-6))
    feats -= feats.mean(axis=0, keepdims=True)
    feats /= feats.std(axis=0, keepdims=True) + 1e-6
    return feats.astype(np.float32)


def _dtw_path(a: np.ndarray, b: np.ndarray, band: int = _BAND) -> list[tuple[int, int]]:
    """Monotone alignment path between feature sequences a (n) and b (m)."""
    n, m = len(a), len(b)
    band = max(band, abs(n - m) + 4)
    d = np.full((n + 1, m + 1), np.inf, dtype=np.float32)
    d[0, 0] = 0.0
    for i in range(1, n + 1):
        j0, j1 = max(1, i - band), min(m, i + band)
        if j0 > j1:
            continue
        cost = np.linalg.norm(a[i - 1] - b[j0 - 1:j1], axis=1)
        w = j1 - j0 + 1
        # The three moves, vectorised.  diag/up first...
        t = cost + np.minimum(d[i - 1, j0:j1 + 1], d[i - 1, j0 - 1:j1])
        # ...then the left move, via the prefix-min identity:
        #   d[i,j] = cost[j] + min(d[i-1,j-1], d[i-1,j], d[i,j-1])
        #          = C[j+1] + min_k<=j ( t[k] - C[k+1] )
        # where C is the prefix sum of cost.  A naive vectorised row update
        # cannot see d[i,j-1] from the same row, so it silently dropped the
        # horizontal move and the reachable region collapsed to one column
        # per row -- d[n,m] went to infinity and every alignment failed.
        c = np.concatenate(([0.0], np.cumsum(cost)))
        acc = np.minimum.accumulate(t - c[1:w + 1])
        d[i, j0:j1 + 1] = c[1:w + 1] + acc

    # Backtrack.  The step below must never leave the computed grid: when
    # every candidate is infinite (uncomputed band edge), ``inf == inf``
    # would tie on the diagonal branch and could even push an index
    # negative -- which, thanks to Python's negative indexing, then reads a
    # *valid-looking* but unrelated row and poisons the whole path.  A
    # finite pick can always be made unless the cell itself was infinite,
    # so treat non-finite picks as "walk toward the origin".
    i, j = n, m
    path = [(i, j)]
    while i > 0 or j > 0:
        up = d[i - 1, j] if i > 0 else np.inf
        left = d[i, j - 1] if j > 0 else np.inf
        diag = d[i - 1, j - 1] if i > 0 and j > 0 else np.inf
        pick = min(diag, up, left)
        if not np.isfinite(pick):
            if i > 0 and j > 0:
                i, j = i - 1, j - 1
            elif i > 0:
                i -= 1
            else:
                j -= 1
        elif diag == pick:
            i, j = i - 1, j - 1
        elif up == pick:
            i -= 1
        else:
            j -= 1
        path.append((i, j))
    path.reverse()
    return path


def _energy_envelope(audio: np.ndarray, sr: int = _SR) -> tuple[float, float]:
    """Leading/trailing silence of a decoded signal, by an energy gate.

    Needed for the edge recording, whose envelope is not otherwise measured.
    """
    win = int(0.02 * sr)
    hop = int(0.01 * sr)
    if len(audio) < win + hop:
        return 0.0, 0.0
    rms = np.sqrt(np.convolve(audio.astype(np.float64) ** 2,
                              np.ones(win) / win, "valid")[::hop])
    thr = max(float(rms.max()) * 0.04, 1e-4)
    speech = np.flatnonzero(rms > thr)
    if not len(speech):
        return 0.0, 0.0
    return speech[0] * 0.01, (len(audio) / sr) - (speech[-1] + 1) * 0.01


def _aligned_times(text: str, zephyr_wav: Path, curve: list[dict], env: dict):
    """Per-word Zephyr onset times, from warping the edge recording onto it.

    Returns a numpy array (one time per ``\\S+`` token of `text`), or ``None``
    if alignment is impossible, in which case the caller falls back to the
    resampled curve.

    Only the *speech spans* are aligned: the silence at each clip's head and
    tail is trimmed first.  Aligning silence to silence lets DTW absorb a
    long opening stretch of one clip into a few silence frames of the other
    (it is free to do so), after which every following word is mis-timed.
    """
    try:
        stat = zephyr_wav.stat()
        stamp = f"{stat.st_size}:{int(stat.st_mtime)}"
    except OSError:
        return None
    cache_path = TIMING_DIR / f"aln_{_key(text, stamp)}.json"
    cached = _read_json(cache_path)
    if cached is not None:
        return np.array(cached, dtype=float)

    try:
        edge_mp3 = ensure_edge_audio(text)
        if edge_mp3 is None:
            return None
        z = _decode_mono(zephyr_wav)
        e = _decode_mono(edge_mp3)
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"[timing] alignment decode failed: {exc}")
        return None

    lead_z = float(env.get("lead", 0.0))
    trail_z = float(env.get("trail", 0.0))
    lead_e, trail_e = _energy_envelope(e)

    hop_n = int(round(_SR * _HOP))
    z0 = int(lead_z * _SR)
    z1 = max(z0 + hop_n, int((len(z) / _SR - trail_z) * _SR))
    e0 = int(lead_e * _SR)
    e1 = max(e0 + hop_n, int((len(e) / _SR - trail_e) * _SR))
    z_trim, e_trim = z[z0:z1], e[e0:e1]

    z_feat = _logmel(z_trim)
    e_feat = _logmel(e_trim)
    if z_feat is None or e_feat is None:
        return None
    try:
        path = _dtw_path(z_feat, e_feat)
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"[timing] DTW failed: {exc}")
        return None

    js = np.array([j for _, j in path], dtype=np.float64)
    is_ = np.array([i for i, _ in path], dtype=np.float64)

    def edge_time_to_zephyr(t: float) -> float:
        j_q = int(round((t - lead_e) / _HOP))
        i_q = float(np.interp(j_q, js, is_))
        return lead_z + i_q * _HOP

    length = max(len(text), 1)
    xs = [0.0]
    ys = [lead_z]
    for c in curve:
        xs.append(c["text_offset"] / length)
        ys.append(edge_time_to_zephyr(float(c["start"])))
    xs.append(1.0)
    ys.append(max(env.get("duration", 0.0) - trail_z, ys[-1] + 0.05))
    xs = np.array(xs, dtype=float)
    ys = np.array(ys, dtype=float)
    keep = np.concatenate(([True], np.diff(xs) > 0))
    xs, ys = xs[keep], ys[keep]
    if len(xs) < 2:
        return None

    words = list(_WORD.finditer(text))
    times = np.array([float(np.interp(m.start() / length, xs, ys))
                      for m in words], dtype=float)
    times = np.maximum.accumulate(times)
    times = _snap_out_of_pauses(times, env.get("gaps", []))
    _write_json(cache_path, times.tolist())
    return times


# --------------------------------------------------------- boundary build ---
_WORD = re.compile(r"\S+")


def _proportional_curve(text: str) -> list[dict]:
    """The old character-count estimate, kept only as an offline fallback."""
    words = list(_WORD.finditer(text))
    weights = []
    for m in words:
        w = m.group()
        weight = float(len(w))
        if w[-1] in ".!?":
            weight += 4.0
        elif w[-1] in ",;:":
            weight += 2.0
        weights.append(weight)
    total = sum(weights) or 1.0
    curve, acc = [], 0.0
    for m, weight in zip(words, weights):
        curve.append({"text_offset": m.start(), "start": acc / total, "end": 1.0})
        acc += weight
    return [{"text_offset": c["text_offset"], "start": c["start"]} for c in curve]


def _snap_out_of_pauses(times: np.ndarray, gaps: list) -> np.ndarray:
    """Push any word that was placed inside a measured pause to the resume.

    A word cannot have started during silence.  If the resampled curve puts
    its onset inside a detected gap, the honest reading is that the word
    begins when speech comes back -- and because gaps are disjoint and
    ascending, pushing forward preserves monotonicity.  A running maximum
    then keeps the sequence ordered.
    """
    if not len(gaps):
        return times
    starts = np.array([g[0] for g in gaps], dtype=float)
    ends = np.array([g[1] for g in gaps], dtype=float)
    out = times.copy()
    for i, t in enumerate(out):
        # last gap that begins before this word
        j = int(np.searchsorted(starts, t, side="right")) - 1
        if j >= 0 and t < ends[j] and t >= starts[j]:
            out[i] = ends[j]
    return np.maximum.accumulate(out)


def build_word_boundaries(text: str, audio_path: Path) -> list[dict]:
    """Word boundaries in manim-voiceover's format, timed from real audio.

    ``text_offset`` is measured against the bookmark-stripped text, which is
    what ``VoiceoverTracker`` interpolates against to resolve
    ``<bookmark mark='...'/>`` positions.

    Primary path: DTW-align the edge donor recording onto this Zephyr take
    (``_aligned_times``), which measures each word onset in the actual audio.
    Fallback: the resampled edge curve, so a render never dies offline.
    """
    text = " ".join(text.split())
    length = max(len(text), 1)
    env = audio_envelope(audio_path)
    duration, lead, trail = env["duration"], env["lead"], env["trail"]
    curve = edge_curve(text) or _proportional_curve(text)
    words = list(_WORD.finditer(text))

    times = None
    if edge_tts is not None and len(curve) >= 2:
        times = _aligned_times(text, audio_path, curve, env)

    if times is None:
        # Normalise the timing donor onto the pure-speech span (0..1), so it
        # is independent of how long that donor clip happened to be.
        t0 = min(c["start"] for c in curve)
        t1 = max(c.get("end", c["start"]) for c in curve)
        span = max(t1 - t0, 1e-6)
        xs = np.array([c["text_offset"] / length for c in curve], dtype=float)
        ys = np.array([(c["start"] - t0) / span for c in curve], dtype=float)
        ys = np.clip(ys, 0.0, 1.0)
        # np.interp needs strictly increasing x.
        keep = np.concatenate(([True], np.diff(xs) > 0))
        xs, ys = xs[keep], ys[keep]
        if len(xs) < 2 or xs[0] > 0.0:
            xs = np.concatenate(([0.0], xs))
            ys = np.concatenate(([0.0], ys))
        if xs[-1] < 1.0:
            xs = np.concatenate((xs, [1.0]))
            ys = np.concatenate((ys, [1.0]))

        # Resample onto the Zephyr clip's own measured speech span.
        if duration <= 0.0:
            speech_start, speech_span = 0.0, 1.0
        else:
            speech_start = lead
            speech_span = max(duration - lead - trail, 0.1)

        raw = np.array([speech_start + float(np.interp(m.start() / length,
                                                       xs, ys))
                        * speech_span for m in words], dtype=float)
        # Then correct against the pauses this clip actually contains.
        times = _snap_out_of_pauses(raw, env.get("gaps", []))

    out: list[dict] = []
    for m, t in zip(words, times):
        out.append({
            "audio_offset": int(t * _AUDIO_OFFSET_RESOLUTION),
            "text_offset": m.start(),
            "word_length": len(m.group()),
            "text": m.group(),
            "boundary_type": "Word",
        })

    # Anchor the close of the text so a bookmark near the end interpolates
    # rather than clamping to the last spoken word.
    out.append({
        "audio_offset": int((duration - trail if duration > 0 else 1.0)
                            * _AUDIO_OFFSET_RESOLUTION),
        "text_offset": len(text),
        "word_length": 1,
        "text": "",
        "boundary_type": "Word",
    })
    return out


# ------------------------------------------------------------ take quality ---
def _edge_total_seconds(text: str) -> float | None:
    """How long this text takes to say, per the edge timing donor."""
    curve = edge_curve(text)
    if not curve:
        return None
    return max(c.get("end", c["start"]) for c in curve)


def take_is_plausible(text: str, audio_path: Path) -> tuple[bool, str]:
    """Is this take a complete reading of the whole line?

    Gemini TTS occasionally returns a *truncated* clip -- measured on this
    very script: 32 words crammed into 4.4 s, i.e. 7.3 words/second against
    the voice's normal 2.1-3.1.  Nothing about the response says "truncated",
    so the only way to catch it is to measure the audio against how long the
    same text takes to say.  Without this the beat renders with narration
    that simply stops mid-sentence.
    """
    env = audio_envelope(audio_path)
    duration = env["duration"]
    if duration <= 0.0:
        return False, "zero-length audio"

    ref = _edge_total_seconds(text)
    if ref and ref > 1.0:
        ratio = duration / ref
        if ratio < 0.62:
            return False, (f"truncated: {duration:.2f}s vs {ref:.2f}s expected "
                           f"({ratio:.0%})")
        if ratio > 2.0:
            return False, (f"implausibly slow: {duration:.2f}s vs {ref:.2f}s "
                           f"expected ({ratio:.0%})")

    # Independent band, so a transient edge-tts failure cannot disable the
    # check above.  Measured across this episode's takes: 2.07-3.10 w/s.
    words = len(text.split())
    if words >= 8 and duration > 0:
        wps = words / duration
        if wps > 4.2:
            return False, f"truncated: {wps:.1f} words/second"
        if wps < 1.7:
            return False, f"implausibly slow: {wps:.1f} words/second"
    return True, ""


def evict_take(cache_dir: Path, text: str) -> None:
    """Remove a bad take (audio + cache entry) so it is re-synthesised.

    ``GeminiZephyrSpeechService`` keys its cache on the input data, so a bad
    take would otherwise be handed back on every retry -- and on every future
    render.
    """
    cache_json = Path(cache_dir) / "cache.json"
    if not cache_json.exists():
        return
    try:
        entries = json.loads(cache_json.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return
    if not isinstance(entries, list):
        return

    def squashed(s: str) -> str:
        return re.sub(r"\s+", "", s)

    want = squashed(remove_bookmarks(text))
    kept, dropped = [], []
    for e in entries:
        idata = e.get("input_data") or {}
        if (idata.get("service") == "gemini-zephyr"
                and squashed(str(idata.get("input_text", ""))) == want):
            dropped.append(e)
        else:
            kept.append(e)
    if not dropped:
        return
    for e in dropped:
        for key in ("original_audio", "final_audio"):
            name = e.get(key)
            if not name:
                continue
            f = Path(cache_dir) / str(name)
            try:
                f.unlink()
            except OSError:
                pass
    cache_json.write_text(json.dumps(kept, indent=1), encoding="utf-8")
    logger.warning(f"[voice] evicted {len(dropped)} bad take(s) for "
                   f"{remove_bookmarks(text)[:50]!r}")


# --------------------------------------------------------------- service ----
class HybridZephyrSpeechService(SpeechService):
    """Zephyr voice, real word timings.

    Reuses ``GeminiZephyrSpeechService`` for synthesis (and therefore the
    repo's existing voice cache), then replaces the invented word boundaries
    with measured ones.
    """

    def __init__(self, voice: str = "Zephyr", model: str | None = None,
                 **kwargs: object) -> None:
        initialize_speech_service(self, kwargs)
        self.voice = voice
        self.model = model or DEFAULT_MODEL
        self._zephyr = GeminiZephyrSpeechService(voice=voice, model=self.model)

    def generate_from_text(self, text: str, cache_dir: PathLike | None = None,
                           path: PathLike | None = None, **kwargs: object) -> VoiceoverData:
        if cache_dir is None:
            cache_dir = self.cache_dir
        # 1) the voice (shared cache with the repo's own Gemini service)
        data = dict(self._synth_with_retry(text, cache_dir, path, **kwargs))
        # 2) the clock
        spoken = " ".join(remove_bookmarks(text).split())
        audio_path = Path(cache_dir) / str(data["original_audio"])
        if not audio_path.exists():
            raise RuntimeError(
                f"narration audio missing for {spoken[:60]!r}: {audio_path}")
        data["word_boundaries"] = build_word_boundaries(spoken, audio_path)
        data["timing"] = "edge-derived, silence-anchored"
        return data

    def _synth_with_retry(self, text: str, cache_dir: PathLike,
                          path: PathLike | None, **kwargs: object) -> VoiceoverData:
        """Synthesise, retrying the API's two intermittent failure modes.

        1. HTTP 200 with ``finishReason: OTHER`` and no audio at all --
           measured at roughly one call in three on the same input.  The
           upstream service only retries non-200 responses, so without this
           the render dies with a bare ``KeyError: 'content'``.
        2. A *truncated* clip that looks like a normal success.  Caught by
           measuring the audio against how long the text takes to say.

        Both are fixed by throwing the take away and asking again.
        """
        attempts = 10
        last: Exception | None = None
        for attempt in range(1, attempts + 1):
            try:
                data = self._zephyr.generate_from_text(
                    text, cache_dir=cache_dir, path=path, **kwargs)
                audio_path = Path(cache_dir) / str(data["original_audio"])
                ok, why = take_is_plausible(text, audio_path)
                if ok:
                    return data
                last = RuntimeError(why)
                logger.warning(f"[voice] bad take (attempt {attempt}/{attempts}"
                               f"): {why}; discarding and retrying")
                evict_take(Path(cache_dir), text)
            except Exception as exc:  # noqa: BLE001 - empty body / transport
                last = exc
                logger.warning(f"[voice] synthesis attempt {attempt}/"
                               f"{attempts} failed ({type(exc).__name__}: {exc})")
            if attempt < attempts:
                # The endpoint starts refusing under sustained load, so back
                # off hard rather than hammering it.
                time.sleep(min(1.5 * attempt, 8.0))
        raise RuntimeError(
            f"Gemini TTS failed {attempts} times for {text[:70]!r}: {last}")


# ------------------------------------------------------------ pre-warming ---
def warm_narration(texts: list[str], *, cache_dir: Path | None = None) -> None:
    """Synthesise, measure and cache every line before a render.

    Running this first keeps the render itself deterministic and quiet (no
    network calls mid-render) and surfaces a bad key or an offline machine in
    seconds rather than 20 minutes in.  It also *locks the voice in*: Gemini
    TTS is stochastic, so the take that gets timed here is the take that gets
    rendered.

    Goes through ``_wrap_generate_from_text`` on purpose -- that is the call
    which writes the cache entry ``VoiceoverScene.voiceover()`` later reads,
    so calling ``generate_from_text`` directly would re-synthesise every take.
    """
    service = HybridZephyrSpeechService(cache_dir=cache_dir or VOICEOVER_DIR)
    fresh = 0
    for i, text in enumerate(texts, 1):
        spoken = " ".join(remove_bookmarks(text).split())
        before = len(list(Path(service.cache_dir).glob("*.wav")))
        data = service._wrap_generate_from_text(text)  # noqa: SLF001 - intended
        after = len(list(Path(service.cache_dir).glob("*.wav")))
        fresh += after - before
        wb = data["word_boundaries"]
        dur = wb[-1]["audio_offset"] / _AUDIO_OFFSET_RESOLUTION
        print(f"[{i:>3}/{len(texts)}] {dur:6.2f}s  {len(wb):>3} words  "
              f"{spoken[:56]!r}", flush=True)
        # Deliberately unhurried: the TTS endpoint degrades under sustained load.
        time.sleep(0.8)
    print(f"\nwarmed {len(texts)} lines into {service.cache_dir} "
          f"({fresh} newly synthesised, {len(texts) - fresh} from cache)")


__all__ = [
    "HybridZephyrSpeechService", "build_word_boundaries", "audio_envelope",
    "edge_curve", "warm_narration", "VOICEOVER_DIR", "TIMING_DIR",
]

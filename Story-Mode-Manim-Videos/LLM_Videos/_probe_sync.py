"""Objective sync audit: the estimated timings vs the audio-aligned timings.

For every unique narration line in the voice cache:

  * old = the word boundaries the previous method stored (resampled edge
    curve, which is what the current renders were synced to),
  * new = DTW alignment of the edge recording onto the actual Zephyr take,

and reports per-word deltas plus two checks that the *new* timings really do
land on speech: no word onset inside a measured pause, and each word window
carries more energy than the clip's noise floor.

Usage:  python _probe_sync.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from audio import (  # noqa: E402
    VOICEOVER_DIR, _SR, _aligned_times, _decode_mono, _snap_out_of_pauses,
    audio_envelope, edge_curve,
)


def rms(a: np.ndarray) -> float:
    return float(np.sqrt(np.mean(a.astype(np.float64) ** 2))) if len(a) else 0.0


def main() -> int:
    entries = json.loads((VOICEOVER_DIR / "cache.json").read_text(encoding="utf-8"))
    seen: dict[str, dict] = {}
    for e in entries:
        seen.setdefault(e["input_data"]["input_text"], e)

    print(f"{len(seen)} unique narration lines\n")
    worst: list[tuple[float, str]] = []
    total_delta, n_delta = 0.0, 0
    onset_in_pause = 0
    low_energy_onsets = 0
    total_words = 0

    for text, entry in sorted(seen.items()):
        wav = VOICEOVER_DIR / entry["original_audio"]
        if not wav.exists():
            continue
        env = audio_envelope(wav)
        curve = edge_curve(text)
        if not curve:
            continue
        new = _aligned_times(text, wav, curve, env)
        if new is None:
            print(f"  ALIGN-FAIL  {text[:52]!r}")
            continue

        old_wb = [w for w in entry["word_boundaries"] if w.get("text", "").strip()]
        old = np.array([w["audio_offset"] / 1e7 for w in old_wb], dtype=float)
        n = min(len(old), len(new))
        delta = np.abs(new[:n] - old[:n])
        total_delta += float(delta.sum())
        n_delta += n
        worst.append((float(delta.max()), text))

        # validate the new timings against the audio itself
        audio = _decode_mono(wav)
        floor = max(rms(audio[:int(0.15 * _SR)]), 1e-4)
        for i in range(len(new)):
            total_words += 1
            s = int(round(new[i] * _SR))
            s = max(0, min(s, len(audio) - 1))
            e = int(round((new[i + 1] * _SR) if i + 1 < len(new)
                          else min(new[i] + 0.3, len(audio) / _SR)))
            e = max(s + 1, min(e, len(audio)))
            win = audio[s:e]
            if rms(win) < floor * 2.0:
                low_energy_onsets += 1
        onset_in_pause += int(np.sum([
            any(g[0] <= t < g[1] for g in env["gaps"]) for t in new]))

    worst.sort(reverse=True)
    print(f"mean |old-new| delta : {total_delta / max(n_delta, 1) * 1000:6.1f} ms")
    if worst:
        print(f"max  |old-new| delta : {worst[0][0] * 1000:6.1f} ms "
              f"({worst[0][1][:44]!r})")
    print(f"\nchecks on the NEW timings:")
    print(f"  word onsets inside a measured pause : {onset_in_pause} / {total_words}")
    print(f"  word windows with near-silent energy: {low_energy_onsets} / {total_words}")
    print("\n10 largest deltas (old vs new):")
    for d, t in worst[:10]:
        print(f"  {d * 1000:6.1f} ms  {t[:60]!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

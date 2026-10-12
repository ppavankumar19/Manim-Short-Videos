"""Spot-check one line: old vs DTW-aligned word times against the real audio.

Prints the measured silence map of the Zephyr take, then the two timing
tables, so the correct one can be judged against where speech actually is.

Usage:  python _probe_one.py "Here are four of them"
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from audio import (  # noqa: E402
    VOICEOVER_DIR, _aligned_times, audio_envelope, edge_curve,
)

_PREFIX = sys.argv[1] if len(sys.argv) > 1 else "Here are four of them"

entries = json.loads((VOICEOVER_DIR / "cache.json").read_text(encoding="utf-8"))
target = None
for e in entries:
    t = e["input_data"]["input_text"]
    if t.startswith(_PREFIX):
        target = e
        break
if target is None:
    print("no line starts with", _PREFIX)
    sys.exit(1)

text = target["input_data"]["input_text"]
wav = VOICEOVER_DIR / target["original_audio"]
env = audio_envelope(wav)
curve = edge_curve(text)
print(f"text  : {text!r}")
print(f"audio : {wav.name}  dur {env['duration']:.2f}s  lead {env['lead']:.2f}s "
      f"trail {env['trail']:.2f}s")
print("pauses:", [(round(a, 2), round(b, 2)) for a, b in env["gaps"]])
print()

old_wb = [w for w in target["word_boundaries"] if w.get("text", "").strip()]
new = _aligned_times(text, wav, curve, env)

print(f"{'word':>18} {'old':>8} {'new':>8} {'delta':>8}")
for i, w in enumerate(old_wb):
    o = w["audio_offset"] / 1e7
    n = new[i] if i < len(new) else float("nan")
    print(f"{w['text']!r:>18} {o:8.2f} {n:8.2f} {abs(n - o):8.2f}")

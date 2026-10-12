"""Inspect the warmed takes: duration, envelope, and the edge reference ratio."""
from __future__ import annotations

import json
import sys
import wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from audio import VOICEOVER_DIR, audio_envelope, edge_curve  # noqa: E402

entries = json.loads((VOICEOVER_DIR / "cache.json").read_text(encoding="utf-8"))
seen: dict[str, dict] = {}
for e in entries:
    t = e["input_data"]["input_text"]
    seen.setdefault(t, e)

print(f"{'wav':>7} {'lead':>5} {'trail':>5} {'edge':>6} {'ratio':>5} {'w/s':>5} "
      f"{'pauses':>6}  text")
for t, e in seen.items():
    fp = VOICEOVER_DIR / e["original_audio"]
    if not fp.exists():
        print(f"MISSING {fp.name}")
        continue
    env = audio_envelope(fp)
    with wave.open(str(fp)) as w:
        d = w.getnframes() / w.getframerate()
    cur = edge_curve(t)
    ref = max(c.get("end", c["start"]) for c in cur) if cur else 0.0
    ratio = d / ref if ref else 0.0
    wps = len(t.split()) / d if d else 0.0
    flag = "  <-- CHECK" if (ratio and (ratio < 0.62 or ratio > 2.0)) else ""
    print(f"{d:7.2f} {env['lead']:5.2f} {env['trail']:5.2f} {ref:6.2f} "
          f"{ratio:5.2f} {wps:5.2f} {len(env['gaps']):6d}  {t[:48]!r}{flag}")

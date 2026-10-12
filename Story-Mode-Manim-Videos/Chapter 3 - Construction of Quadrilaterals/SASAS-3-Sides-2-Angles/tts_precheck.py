"""Pre-check the TTS for a narration line before rendering.

The speech service occasionally returns an empty/clipped response for certain
phrasings, which only shows up as a silent or missing line in the finished video.
This asks the service for the piece and reports how much audio came back, so the
wording can be fixed before a render is spent on it.

Usage (from the topic folder):
    python tts_precheck.py <story_module>                 # every piece
    python tts_precheck.py <story_module> scene10         # one piece
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "speech_service.py").exists())
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))

from speech_service import get_speech_service  # noqa: E402

if len(sys.argv) < 2:
    print(__doc__)
    raise SystemExit(2)
MODULE, wanted = sys.argv[1], sys.argv[2:]

narration = importlib.import_module(MODULE).NARRATION

service = get_speech_service()
ok = True
for key, text in narration.items():
    if wanted and key not in wanted:
        continue
    try:
        resp = service.generate_from_text(text)
        # the service answers with a dict: the wav it wrote plus the word
        # boundaries it returned -- an empty response has neither
        if isinstance(resp, dict):
            wav = resp.get("final_audio") or resp.get("original_audio")
            words = len(resp.get("word_boundaries") or [])
            good = bool(wav) and words > 0
            detail = f"{words:3d} boundaries, {wav or 'no audio'}"
        else:  # older service shape: an object carrying the audio bytes
            size = len(getattr(resp, "audio", b"") or b"")
            good, detail = size > 0, f"{size / 1024:8.1f} kB"
        print(f"{'ok ' if good else '!! '}{key:>14}  {detail:>34}  "
              f"{text[:48]!r}")
        ok = ok and good
    except Exception as exc:  # noqa: BLE001
        ok = False
        print(f"!! {key:>14}  FAILED: {type(exc).__name__}: {exc}")
print("ALL OK" if ok else "PROBLEMS FOUND")



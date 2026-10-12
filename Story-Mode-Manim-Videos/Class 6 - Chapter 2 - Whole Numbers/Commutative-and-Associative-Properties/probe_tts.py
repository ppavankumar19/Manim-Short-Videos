"""Find which narration piece the TTS refuses to synthesise."""
from __future__ import annotations

import re
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "speech_service.py").exists())
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))

from speech_service import get_speech_service  # noqa: E402
from commutative_associative_story import NARRATION  # noqa: E402

NO_BM = re.compile(r"<bookmark mark='[^']+'/>")


def main() -> None:
    svc = get_speech_service()
    for key, raw in NARRATION.items():
        text = NO_BM.sub(" ", raw)
        text = re.sub(r"\s+", " ", text).strip()
        try:
            svc.generate_from_text(text)
            print(f"ok   {key:14s} ({len(text)} chars)")
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL {key:14s} ({len(text)} chars) -> {type(exc).__name__}: {exc}")
            print(f"     text: {text[:120]}...")
            traceback.print_exc(limit=2)


if __name__ == "__main__":
    main()

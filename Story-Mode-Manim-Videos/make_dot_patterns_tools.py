"""Create the audit/sync tools for the Geometric Dot Patterns topic AND
pre-check every narration line against the TTS before rendering."""
from __future__ import annotations

import py_compile
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "Class 6 - Chapter 2 - Whole Numbers" / "Whole-Numbers"
DST = HERE / "Class 6 - Chapter 2 - Whole Numbers" / "Geometric-Dot-Patterns"

ANCHORS = '''PIECE_ANCHORS = {
    "title": "today we look at patterns made from dots",
    "scene1": "here are six dots",
    "scene2": "begin with the simplest pattern",
    "scene3": "now take six dots and arrange",
    "scene4": "what if the rows and the columns",
    "scene5": "build triangles",
    "scene6": "patterns can make calculations easier",
    "scene7": "the same idea works for multiplication",
    "scene8": "here is a practical example",
    "scene9_setup": "your turn two questions",
    "scene9_reveal": "the next triangle needs",
    "scene10": "dots can make a line",
}'''


def make_tools() -> None:
    for name in ("audit_sync_overlap.py", "sync_map.py"):
        shutil.copy(SRC / name, DST / name)
        p = DST / name
        text = p.read_text(encoding="utf-8")
        text = text.replace("from whole_numbers_story import",
                            "from dot_patterns_story import")
        text = text.replace("WholeNumbersStory", "DotPatternsStory")
        text = text.replace('"whole_numbers_story"', '"dot_patterns_story"')
        text = text.replace("whole_numbers_story.py", "dot_patterns_story.py")
        if name.startswith("audit"):
            start = text.index("PIECE_ANCHORS = {")
            end = text.index("}", start) + 1
            text = text[:start] + ANCHORS + text[end:]
        p.write_text(text, encoding="utf-8")
        py_compile.compile(str(p), doraise=True)
        print(f"created {name}")


def check_tts() -> None:
    ROOT = next(p for p in HERE.parents if (p / "speech_service.py").exists())
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(DST))
    from speech_service import get_speech_service  # noqa: E402
    from dot_patterns_story import NARRATION  # noqa: E402

    svc = get_speech_service()
    no_bm = re.compile(r"<bookmark mark='[^']+'/>")
    bad = []
    for key, raw in NARRATION.items():
        text = re.sub(r"\s+", " ", no_bm.sub(" ", raw)).strip()
        try:
            svc.generate_from_text(text)
            print(f"ok   {key}")
        except Exception as exc:  # noqa: BLE001
            bad.append(key)
            print(f"FAIL {key} -> {type(exc).__name__}: {exc}")
            print(f"     {text[:130]}")
    print("TTS pre-check:", "ALL OK" if not bad else f"FAILED: {bad}")


if __name__ == "__main__":
    make_tools()
    check_tts()

"""Create the audit / sync tools for the Whole Numbers topic by cloning the
fractions ones and re-pointing them at the new module, class and SRT."""
from __future__ import annotations

import py_compile
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = (HERE / "Chapter 2 - Linear Equations in One Variable"
       / "Solving-Equations-with-Fractions")
DST = HERE / "Class 6 - Chapter 2 - Whole Numbers" / "Whole-Numbers"

ANCHORS = '''PIECE_ANCHORS = {
    "title": "today we meet the whole numbers",
    "scene1": "look at this pencil box",
    "scene2": "how do we count things",
    "scene3": "now let us place the two collections",
    "scene4": "now let us put the whole numbers on a line",
    "scene5": "let us look closely at one number",
    "scene6": "now a very important question",
    "scene7": "let us practise with bigger numbers",
    "scene8": "numbers describe real things",
    "scene9_setup": "your turn look at the number line",
    "scene9_reveal": "let us check eleven plus one",
    "scene10": "let us recap",
}'''

OLD_ANCHORS_START = "PIECE_ANCHORS = {"
OLD_ANCHORS_END = "}"


def patch_audit(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace("from fractions_clearing_story import",
                        "from whole_numbers_story import")
    text = text.replace("FractionsClearingStory", "WholeNumbersStory")
    text = text.replace('"fractions_clearing_story"', '"whole_numbers_story"')
    # replace the anchor table
    start = text.index(OLD_ANCHORS_START)
    end = text.index(OLD_ANCHORS_END, start) + 1
    text = text[:start] + ANCHORS + text[end:]
    text = text.replace("two_digit_puzzles_story.py", "whole_numbers_story.py")
    text = text.replace("Replays the scene headlessly:",
                        "Replays the Whole Numbers scene headlessly:")
    path.write_text(text, encoding="utf-8")


def patch_sync(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "from fractions_clearing_story import NARRATION, FractionsClearingStory",
        "from whole_numbers_story import NARRATION, WholeNumbersStory")
    text = text.replace("scene = FractionsClearingStory()",
                        "scene = WholeNumbersStory()")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    for name in ("audit_sync_overlap.py", "sync_map.py"):
        shutil.copy(SRC / name, DST / name)
        target = DST / name
        if name.startswith("audit"):
            patch_audit(target)
        else:
            patch_sync(target)
        py_compile.compile(str(target), doraise=True)
        print(f"created {name}")


if __name__ == "__main__":
    main()

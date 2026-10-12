"""Create the audit / sync tools for Operations on Whole Numbers by cloning
the Whole Numbers ones and re-pointing them at the new module, class and SRT."""
from __future__ import annotations

import py_compile
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "Class 6 - Chapter 2 - Whole Numbers" / "Whole-Numbers"
DST = HERE / "Class 6 - Chapter 2 - Whole Numbers" / "Operations-on-Whole-Numbers"

ANCHORS = '''PIECE_ANCHORS = {
    "title": "today we use the number line",
    "scene1": "imagine a floor marked with numbers",
    "scene2": "let us remember our number line",
    "scene3": "now let us add on the number line",
    "scene4": "subtraction is the opposite",
    "scene5": "multiplication is repeated addition",
    "scene6": "let us compare the three operations",
    "scene7": "now a game from the textbook",
    "scene8": "here is a simple routine",
    "scene9_setup": "your turn here is the question",
    "scene9_reveal": "let us check five jumps",
    "scene10": "let us recall",
}'''


def main() -> None:
    for name in ("audit_sync_overlap.py", "sync_map.py"):
        shutil.copy(SRC / name, DST / name)
        p = DST / name
        text = p.read_text(encoding="utf-8")
        text = text.replace("from whole_numbers_story import",
                            "from operations_on_whole_numbers import")
        text = text.replace("WholeNumbersStory", "OperationsOnWholeNumbersStory")
        text = text.replace('"whole_numbers_story"', '"operations_on_whole_numbers"')
        text = text.replace("whole_numbers_story.py", "operations_on_whole_numbers.py")
        text = text.replace('"whole_numbers_story import NARRATION, '
                            'WholeNumbersStory"',
                            '"operations_on_whole_numbers import NARRATION, '
                            'OperationsOnWholeNumbersStory"')
        if name.startswith("audit"):
            start = text.index("PIECE_ANCHORS = {")
            end = text.index("}", start) + 1
            text = text[:start] + ANCHORS + text[end:]
        p.write_text(text, encoding="utf-8")
        py_compile.compile(str(p), doraise=True)
        print(f"created {name}")


if __name__ == "__main__":
    main()

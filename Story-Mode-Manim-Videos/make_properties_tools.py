"""Create the audit / sync tools for the Commutative & Associative topic."""
from __future__ import annotations

import py_compile
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "Class 6 - Chapter 2 - Whole Numbers" / "Whole-Numbers"
DST = (HERE / "Class 6 - Chapter 2 - Whole Numbers"
       / "Commutative-and-Associative-Properties")

ANCHORS = '''PIECE_ANCHORS = {
    "title": "today we meet two properties",
    "scene1": "here is a quick challenge",
    "scene2": "begin with two small groups",
    "scene3": "the same idea works for multiplication",
    "scene4": "we can write this rule with letters",
    "scene5": "now something different",
    "scene6": "multiplication obeys the same rule",
    "scene7": "keep these two ideas apart",
    "scene8": "now back to our challenge",
    "scene9_setup": "your turn find the sum",
    "scene9_reveal": "two hundred thirty eight and one",
    "scene10": "commutative means changing the order",
}'''


def main() -> None:
    for name in ("audit_sync_overlap.py", "sync_map.py"):
        shutil.copy(SRC / name, DST / name)
        p = DST / name
        text = p.read_text(encoding="utf-8")
        text = text.replace("from whole_numbers_story import",
                            "from commutative_associative_story import")
        text = text.replace("WholeNumbersStory", "CommutativeAssociativeStory")
        text = text.replace('"whole_numbers_story"', '"whole_numbers_properties"')
        text = text.replace("whole_numbers_story.py",
                            "commutative_associative_story.py")
        if name.startswith("audit"):
            start = text.index("PIECE_ANCHORS = {")
            end = text.index("}", start) + 1
            text = text[:start] + ANCHORS + text[end:]
        p.write_text(text, encoding="utf-8")
        py_compile.compile(str(p), doraise=True)
        print(f"created {name}")


if __name__ == "__main__":
    main()

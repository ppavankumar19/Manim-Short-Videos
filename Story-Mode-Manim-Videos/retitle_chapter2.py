"""Retitle the eight Chapter-2 videos (on-screen title card + storyboard).

Run from the Story-Mode-Manim-Videos folder:
    python ../.venv/Scripts/python.exe retitle_chapter2.py
"""
from __future__ import annotations

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAPTER = "Chapter 2 - Linear Equations in One Variable"

# folder, script, old on-screen title literal (incl. size), new title, new size
EDITS = [
    ("Linear-Equations", "equation_anatomy_story.py",
     'board_text("Anatomy of an Equation", 36, CHALK_WHITE, "BOLD")',
     'board_text("Linear Equations", 42, CHALK_WHITE, "BOLD")'),
    ("Solving-Simple-Equations", "equation_solving_story.py",
     'board_text("Solving Simple Linear Equations", 34,',
     'board_text("Solving Simple Equations", 40,'),
    ("Linear-Equation-Word-Problems", "from_words_to_equations_story.py",
     'board_text("From Words to Equations", 34, CHALK_WHITE,',
     'board_text("Linear Equation Word Problems", 36, CHALK_WHITE,'),
    ("Linear-Equations-with-Variables-on-Both-Sides", "variables_both_sides_story.py",
     'board_text("Variables on Both Sides", 36, CHALK_WHITE,',
     'board_text("Linear Equations with Variables on Both Sides", 28, CHALK_WHITE,'),
    ("Two-Digit-Number-Riddles", "two_digit_puzzles_story.py",
     'board_text("Two-Digit Number Puzzles", 33, CHALK_WHITE,',
     'board_text("Two-Digit Number Riddles", 38, CHALK_WHITE,'),
    ("Boats-and-Streams-Problems", "upstream_downstream_story.py",
     'board_text("Upstream & Downstream", 33, CHALK_WHITE,',
     'board_text("Boats and Streams Problems", 38, CHALK_WHITE,'),
    ("Applications-of-Angles-and-Parallel-Lines", "geometry_angles_story.py",
     'board_text("Geometry into Algebra", 33, CHALK_WHITE,',
     'board_text("Applications of Angles and Parallel Lines", 30, CHALK_WHITE,'),
    ("Solving-Equations-with-Fractions", "fractions_clearing_story.py",
     'board_text("Fractions in Linear Equations", 31,',
     'board_text("Solving Equations with Fractions", 36,'),
]

STORYBOARD_TITLES = {
    "Linear-Equations": "Linear Equations",
    "Solving-Simple-Equations": "Solving Simple Equations",
    "Linear-Equation-Word-Problems": "Linear Equation Word Problems",
    "Linear-Equations-with-Variables-on-Both-Sides": "Linear Equations with Variables on Both Sides",
    "Two-Digit-Number-Riddles": "Two-Digit Number Riddles",
    "Boats-and-Streams-Problems": "Boats and Streams Problems",
    "Applications-of-Angles-and-Parallel-Lines": "Applications of Angles and Parallel Lines",
    "Solving-Equations-with-Fractions": "Solving Equations with Fractions",
}

# the anatomy video also opens by naming the old topic out loud
NARRATION_EDITS = [
    ("Linear-Equations", "equation_anatomy_story.py",
     '"Today, the anatomy of an equation!<bookmark mark=\'b0\'/> "',
     '"Today, linear equations!<bookmark mark=\'b0\'/> "'),
]


def main() -> None:
    for folder, script, old, new in EDITS:
        path = HERE / CHAPTER / folder / script
        text = path.read_text(encoding="utf-8")
        n = text.count(old)
        if n != 1:
            print(f"!! {folder}: found {n} matches for {old!r}")
            continue
        path.write_text(text.replace(old, new), encoding="utf-8")
        print(f"ok  {folder:46s} title -> {new.split(chr(34))[1]}")

    for folder, script, old, new in NARRATION_EDITS:
        path = HERE / CHAPTER / folder / script
        text = path.read_text(encoding="utf-8")
        if text.count(old) != 1:
            print(f"!! narration edit failed for {folder}")
            continue
        path.write_text(text.replace(old, new), encoding="utf-8")
        print(f"ok  {folder:46s} narration title line updated")

    for folder, title in STORYBOARD_TITLES.items():
        path = HERE / CHAPTER / folder / "storyboard.md"
        if not path.exists():
            print(f"!! no storyboard in {folder}")
            continue
        text = path.read_text(encoding="utf-8")
        new_text, n = re.subn(r"^\*\*VIDEO TITLE:\*\*.*$",
                              f"**VIDEO TITLE:** {title}", text, count=1, flags=re.M)
        if n != 1:
            print(f"!! storyboard title not found in {folder}")
            continue
        path.write_text(new_text, encoding="utf-8")
        print(f"ok  {folder:46s} storyboard -> {title}")


if __name__ == "__main__":
    main()

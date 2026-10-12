"""Update the header docstring title of each retitled Chapter-2 script."""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAPTER = "Chapter 2 - Linear Equations in One Variable"

EDITS = [
    ("Linear-Equations", "equation_anatomy_story.py",
     "Anatomy of an Equation — LHS, RHS & Transposition",
     "Linear Equations — LHS, RHS & Transposition"),
    ("Solving-Simple-Equations", "equation_solving_story.py",
     "Solving Simple Linear Equations — Undo to Find the Unknown",
     "Solving Simple Equations — Undo to Find the Unknown"),
    ("Linear-Equation-Word-Problems", "from_words_to_equations_story.py",
     "From Words to Equations — Turn the Story into Algebra",
     "Linear Equation Word Problems — Turn the Story into Algebra"),
    ("Linear-Equations-with-Variables-on-Both-Sides", "variables_both_sides_story.py",
     "Variables on Both Sides — Bring Like Terms Together",
     "Linear Equations with Variables on Both Sides — Bring Like Terms Together"),
    ("Two-Digit-Number-Riddles", "two_digit_puzzles_story.py",
     "Two-Digit Number Puzzles — Cracking Digit Reversal",
     "Two-Digit Number Riddles — Cracking Digit Reversal"),
    ("Boats-and-Streams-Problems", "upstream_downstream_story.py",
     "Upstream & Downstream — When the River Changes Your Speed",
     "Boats and Streams Problems — When the River Changes Your Speed"),
    ("Applications-of-Angles-and-Parallel-Lines", "geometry_angles_story.py",
     "Geometry into Algebra — Finding Unknown Angles with Linear Equations",
     "Applications of Angles and Parallel Lines — Finding Unknown Angles"),
    ("Solving-Equations-with-Fractions", "fractions_clearing_story.py",
     "Fractions in Linear Equations — Clear the Denominators",
     "Solving Equations with Fractions — Clear the Denominators"),
]


def main() -> None:
    for folder, script, old, new in EDITS:
        path = HERE / CHAPTER / folder / script
        text = path.read_text(encoding="utf-8")
        if text.count(old) != 1:
            print(f"!! {folder}: {text.count(old)} matches")
            continue
        path.write_text(text.replace(old, new, 1), encoding="utf-8")
        print(f"ok  {folder:46s} docstring -> {new}")


if __name__ == "__main__":
    main()

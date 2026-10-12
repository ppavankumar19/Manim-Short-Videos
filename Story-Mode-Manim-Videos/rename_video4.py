"""Video 4 (Linear Equations with Variables on Both Sides): replace the two
character names with common Indian names.

    Rafi    -> Arjun
    Fathima -> Meera

Applies to the narration, the on-screen labels and the storyboard.
"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAPTER = "Chapter 2 - Linear Equations in One Variable"
FOLDER = HERE / CHAPTER / "Linear-Equations-with-Variables-on-Both-Sides"
SCRIPT = FOLDER / "variables_both_sides_story.py"
STORYBOARD = FOLDER / "storyboard.md"

RENAMES = [("Arjun", "Karthik"), ("Meera", "Ananya")]


def apply(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for old, new in RENAMES:
        n = text.count(old)
        text = text.replace(old, new)
        print(f"  {path.name:32s} {old:8s} -> {new:8s} ({n} occurrences)")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    for p in (SCRIPT, STORYBOARD):
        if p.exists():
            apply(p)
        else:
            print(f"!! missing {p}")


if __name__ == "__main__":
    main()

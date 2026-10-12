"""Move the eight Class-8 Chapter-2 topics into their own chapter folder.

     Story-Mode-Manim-Videos/<Topic>/...                       (before)
     Story-Mode-Manim-Videos/Chapter 2 - Linear Equations in One Variable/
                                            <Topic>/...        (after)

Every scene / audit / sync tool located the shared helpers with
`_ROOT = _HERE.parent.parent`, which would break one level deeper.  So each
file is first rewritten to FIND the folder that holds `speech_service.py`
instead of counting parents -- the scripts then work at any depth.

Run from the Story-Mode-Manim-Videos folder:
    python ../.venv/Scripts/python.exe move_to_chapter2.py
"""
from __future__ import annotations

import py_compile
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAPTER = "Chapter 2 - Linear Equations in One Variable"

TOPICS = [
    "Anatomy-of-an-Equation-LHS-RHS-Transposition",
    "Solving-Simple-Linear-Equations",
    "From-Words-to-Equations",
    "Variables-on-Both-Sides",
    "Two-Digit-Number-Puzzles",
    "Upstream-and-Downstream",
    "Geometry-into-Algebra",
    "Fractions-in-Linear-Equations",
]

OLD_ROOT = "_ROOT = _HERE.parent.parent"
NEW_ROOT = ('_ROOT = next(p for p in _HERE.parents\n'
            '        if (p / "speech_service.py").exists())')

OLD_PATH = "sys.path.insert(0, str(HERE.parent.parent))"
NEW_PATH = ('sys.path.insert(0, str(next(p for p in HERE.parents\n'
            '            if (p / "speech_service.py").exists())))')


def patch(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    new = text.replace(OLD_ROOT, NEW_ROOT).replace(OLD_PATH, NEW_PATH)
    if new == text:
        return False
    path.write_text(new, encoding="utf-8")
    py_compile.compile(str(path), doraise=True)
    return True


def main() -> None:
    chapter_dir = HERE / CHAPTER
    chapter_dir.mkdir(exist_ok=True)
    print(f"chapter folder: {chapter_dir}\n")

    for topic in TOPICS:
        src = HERE / topic
        if not src.is_dir():
            print(f"!! missing topic {topic}")
            continue
        changed = []
        for py in sorted(src.rglob("*.py")):
            if "__pycache__" in py.parts:
                continue
            if patch(py):
                changed.append(py.name)
        dst = chapter_dir / topic
        if dst.exists():
            print(f"!! {dst.name} already exists - folder not moved")
            continue
        shutil.move(str(src), str(dst))
        print(f"moved {topic:46s} patched: {', '.join(changed) or '(none)'}")


if __name__ == "__main__":
    main()

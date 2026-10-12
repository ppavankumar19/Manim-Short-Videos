"""Rename the eight Chapter-2 folders to match the new video titles.

     Chapter 2 - Linear Equations in One Variable/
         Anatomy-of-an-Equation-LHS-RHS-Transposition/  ->  Linear-Equations/
         ...

Also repoints the repo-level tools (confirm / verify / burn / retitle /
rename_video4) at the new folder names.  The scene scripts themselves never
mention their folder, so they need no change.

Run from the Story-Mode-Manim-Videos folder.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAPTER = "Chapter 2 - Linear Equations in One Variable"

RENAME = {
    "Anatomy-of-an-Equation-LHS-RHS-Transposition": "Linear-Equations",
    "Solving-Simple-Linear-Equations": "Solving-Simple-Equations",
    "From-Words-to-Equations": "Linear-Equation-Word-Problems",
    "Variables-on-Both-Sides": "Linear-Equations-with-Variables-on-Both-Sides",
    "Two-Digit-Number-Puzzles": "Two-Digit-Number-Riddles",
    "Upstream-and-Downstream": "Boats-and-Streams-Problems",
    "Geometry-into-Algebra": "Applications-of-Angles-and-Parallel-Lines",
    "Fractions-in-Linear-Equations": "Solving-Equations-with-Fractions",
}

TOOLS = ["confirm_chapter2.py", "verify_360_all.py", "burn_1080_all.py",
         "retitle_chapter2.py", "retitle_headers.py", "rename_video4.py"]

RX = re.compile("|".join(sorted((re.escape(k) for k in RENAME),
                                key=len, reverse=True)))


def main() -> None:
    chapter = HERE / CHAPTER
    for old, new in RENAME.items():
        src, dst = chapter / old, chapter / new
        if not src.is_dir():
            print(f"!! {old} not found")
            continue
        if dst.exists():
            print(f"!! {dst.name} already exists")
            continue
        shutil.move(str(src), str(dst))
        print(f"renamed {old:48s} -> {new}")

    print()
    for tool in TOOLS:
        p = HERE / tool
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        new_text, n = RX.subn(lambda m: RENAME[m.group(0)], text)
        if n:
            p.write_text(new_text, encoding="utf-8")
        print(f"{tool:24s} {n} folder reference(s) updated")


if __name__ == "__main__":
    main()

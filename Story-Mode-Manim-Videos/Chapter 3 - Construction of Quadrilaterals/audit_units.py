"""Report every raw string literal in a module that mentions a measurement
without a unit, so nothing on the board is left as a bare number.

    python audit_units.py <module.py>

A literal is reported when it contains "=" between a letter name and a
number, and mentions neither an angle (\\circ / \\angle / degree sign) nor a
unit (cm / mm / m).  Angle-only literals and prose are ignored.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

LIT = re.compile(r'r"((?:[^"\\]|\\.)*)"|\'((?:[^\'\\]|\\.)*)\'')
MEAS = re.compile(r"[A-Z]{1,3}\s?=\s?\d")


def main() -> None:
    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        if "NARRATION" in line or line.strip().startswith("#"):
            continue
        for m in LIT.finditer(line):
            lit = m.group(1) or m.group(2) or ""
            if not MEAS.search(lit):
                continue
            if "cm" in lit or "circ" in lit or "angle" in lit or "°" in lit:
                continue
            if "\\text{ or}" in lit or "A+B" in lit or "A=B" in lit:
                continue
            hits.append((i, lit))
    print(f"{path.name}: {len(hits)} measurement literals without a unit")
    for i, lit in hits:
        print(f"  line {i:5d}: {lit}")
        print(f"          {text.splitlines()[i - 1].strip()[:110]}")


if __name__ == "__main__":
    main()

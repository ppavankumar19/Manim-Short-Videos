"""Print each narration piece's absolute start time in a delivered cut.

The audit harness already resolves the piece boundaries from the rendered
(ground-truth) SRT by matching the topic's narration anchors, so this simply
loads each topic's audit_sync_overlap.py and reports bounds[piece]["start"].

    python _piece_starts.py
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

CHAPTER = (Path(r"D:\Manim-Short-Videos\Story-Mode-Manim-Videos")
           / "Class 8 - Chapter 4 - Exponents and Powers")
TOPICS = [
    "Introduction-to-Exponents-and-Powers",
    "Negative-Exponents-and-Multiplicative-Inverses",
    "Product-and-Quotient-Laws-of-Exponents",
    "Advanced-Laws-of-Exponents",
    "Standard-Form-with-Powers-of-10",
]


def fmt(t: float) -> str:
    return f"{int(t // 60)}:{t % 60:04.1f}"


def main() -> int:
    for topic in TOPICS:
        folder = CHAPTER / topic
        spec = importlib.util.spec_from_file_location(
            f"aud_{abs(hash(topic))}", folder / "audit_sync_overlap.py")
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod
        sys.path.insert(0, str(folder))
        spec.loader.exec_module(mod)
        sys.path.pop(0)
        stream = mod.parse_srt()
        bounds = mod.piece_bounds(stream)
        print(f"=== {topic}")
        for piece in mod.PIECE_ORDER:
            b = bounds[piece]
            print(f"   {piece:>6}  start {fmt(b['start']):>7}  "
                  f"dur {b['dur']:6.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

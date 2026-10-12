"""Does Segoe Print (the series font) carry every symbol this episode uses?

The episode prints token markers and code, not just prose.  Switching the
whole episode to the series font is only safe if the font actually has the
glyphs -- a missing glyph renders as *nothing*, silently, which is how the
musical note was lost earlier.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from manim import DOWN, RIGHT, Text, VGroup  # noqa: E402

CHARS = [
    ("space marker", "\u2423"),
    ("hash pair", "##"),
    ("square brackets", "[UNK]"),
    ("angle brackets", "<unk>"),
    ("pipe token", "<|endoftext|>"),
    ("arrow right", "\u2192"),
    ("em dash", "\u2014"),
    ("middle dot", "\u00b7"),
    ("bullet", "\u2022"),
    ("open box", "\u2610"),
    ("check", "\u2713"),
    ("cross", "\u2715"),
    ("tab", "\u21b9"),
    ("quote", "\u201c\u201d"),
    ("ellipsis", "\u2026"),
    ("degree", "\u00b0"),
    ("plus-minus", "\u00b1"),
    ("hash single", "#"),
    ("underscore", "_"),
    ("caret", "^"),
    ("brace", "{}"),
    ("at", "@"),
    ("tilde", "~"),
]


def main() -> int:
    fonts = ["Segoe Print", "Calibri", "Consolas"]
    header = VGroup(*[Text(f, font="Calibri", font_size=18, color="#22D3EE")
                      for f in fonts]).arrange(RIGHT, buff=1.0)
    header.move_to([0, 3.2, 0])
    rows = VGroup()
    for label, chars in CHARS:
        cells = [Text(label, font="Calibri", font_size=15, color="#8FB3D9")]
        for f in fonts:
            t = Text(chars, font=f, font_size=26, color="#EAF4FF")
            # A missing glyph yields a near-zero-width mobject; measure it.
            t.width = max(t.width, 1e-6)
            cells.append(t)
        row = VGroup(*cells)
        cells[0].move_to([-4.6, 0, 0])
        for i, c in enumerate(cells[1:], start=1):
            c.move_to([-2.4 + (i - 1) * 2.2, 0, 0])
        rows.add(row)
    rows.arrange(DOWN, buff=0.24)
    rows.move_to([0, 0, 0])

    # report widths, which is the objective test for "glyph exists"
    print(f"{'symbol':<16} " + "".join(f"{f:>14}" for f in fonts))
    for label, chars in CHARS:
        widths = []
        for f in fonts:
            t = Text(chars, font=f, font_size=26)
            widths.append(t.width)
        flag = ""
        for f, w in zip(fonts, widths):
            if w < 0.02:
                flag = "  <-- MISSING in " + f
        print(f"{label:<16} " + "".join(f"{w:14.2f}" for w in widths) + flag)

    # emit a still so the shapes can be eyeballed too
    class _Lab:
        pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

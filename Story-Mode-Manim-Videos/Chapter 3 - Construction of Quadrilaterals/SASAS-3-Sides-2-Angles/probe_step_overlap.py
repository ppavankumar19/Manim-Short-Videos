"""Measure the two overlap complaints in video 06, in board units.

  1. beat8_complete draws the example quadrilateral A B C D at full scale and
     the four "1. SKETCH ... 4. FINAL SIDE" method cards in the right column.
     This prints both bounding boxes and their intersection, so the fix (shift
     the figure left, the cards right, or both) can be sized exactly.
  2. beat10_recap prints the recap rows against the figure's `C` label.

    python probe_step_overlap.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from manim import config  # noqa: E402

config.renderer = "cairo"

import construct_quadrilateral_3sides_2angles as M  # noqa: E402


def box(mob, tag):
    l, r = mob.get_left()[0], mob.get_right()[0]
    b, t = mob.get_bottom()[1], mob.get_top()[1]
    print(f"  {tag:26s} x [{l:+.2f} .. {r:+.2f}]   y [{b:+.2f} .. {t:+.2f}]"
          f"   w={r - l:.2f} h={t - b:.2f}")
    return l, r, b, t


def overlap(a, b, na, nb):
    ix = min(a[1], b[1]) - max(a[0], b[0])
    iy = min(a[3], b[3]) - max(a[2], b[2])
    print(f"  overlap {na} vs {nb}: x {ix:+.2f}  y {iy:+.2f}  "
          f"-> {'OVERLAP' if (ix > 0 and iy > 0) else 'clear'}")
    return ix, iy


def main() -> None:
    # ---- 1. the method cards (beat8_complete) ---------------------------
    d = M.example_construction()
    A, B, C, D = d["quad"]
    quad = M.Polygon(A, B, C, D)
    steps = M.VGroup(
        M.combo_card("1. SKETCH", "the 3 sides + 2 angles", M.CHALK_CYAN),
        M.combo_card("2. SAS TRIANGLE", "A B, angle B, B C", M.CHALK_GREEN),
        M.combo_card("3. SECOND ANGLE", "the ray from C", M.CHALK_PINK),
        M.combo_card("4. FINAL SIDE", "6 cm on that ray, then A D",
                     M.CHALK_YELLOW),
    ).arrange(M.DOWN, buff=0.14, aligned_edge=M.LEFT).move_to(
        np.array([2.85, 0.55, 0]))

    print("\n== beat8_complete: figure vs method cards, as rendered ==")
    fq = box(quad, "figure A B C D")
    cs = box(steps, "method cards")
    overlap(fq, cs, "figure", "cards")
    box(steps[0], "  card 1")
    print(f"  vertex C at ({C[0]:+.2f}, {C[1]:+.2f})")
    for shift in (0.30, 0.40, 0.50, 0.60):
        moved = steps.copy().shift(M.RIGHT * shift)
        b = (moved.get_left()[0], moved.get_right()[0],
             moved.get_bottom()[1], moved.get_top()[1])
        print(f"  cards +{shift:.2f} right -> x [{b[0]:+.2f} .. {b[1]:+.2f}]"
              f"   (board right edge {M.BOARD_RIGHT:+.2f})")

    # ---- 2. the recap rows (beat10_recap) -------------------------------
    d2 = M.example_construction(centre=np.array([M.BOARD_CX - 2.8, 0.35, 0]),
                                scale=0.60)
    A2, B2, C2, D2 = d2["quad"]
    c_name = M.board_text("C", 15, M.CHALK_WHITE, "BOLD").move_to(
        C2 + np.array([0.26, 0.02, 0]))
    rows = M.VGroup(
        M.summary_row(1, "First three measurements:", r"\triangle ABC",
                      M.CHALK_YELLOW),
        M.summary_row(2, "Next angle: a", r"direction", M.CHALK_PINK),
        M.summary_row(3, "Final side: the", r"distance", M.CHALK_CYAN),
    ).arrange(M.DOWN, buff=0.16, aligned_edge=M.LEFT).move_to(
        np.array([M.BOARD_CX + 1.5, 1.15, 0]))

    print("\n== beat10_recap: figure's C label vs the rows, as rendered ==")
    cc = box(c_name, "label C")
    rr = box(rows, "recap rows")
    overlap(cc, rr, "C", "rows")
    for shift in (0.20, 0.30, 0.40, 0.50):
        moved = rows.copy().shift(M.RIGHT * shift)
        b = (moved.get_left()[0], moved.get_right()[0])
        print(f"  rows +{shift:.2f} right -> x [{b[0]:+.2f} .. {b[1]:+.2f}]"
              f"   gap to C = {b[0] - cc[1]:+.2f}"
              f"   (board right edge {M.BOARD_RIGHT:+.2f})")


if __name__ == "__main__":
    main()

"""Size/layout check for the scene-1 measurement block and the nudged figures.

Prints the real bounding boxes of the scene-1 elements so the row spacing can
be set from measurements, and re-checks the left figure + right column
composition for scenes 8, 9 and 10 after the nudge.

    .venv/Scripts/python.exe probe_sizes.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "speech_service.py").exists())
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))

from manim import config  # noqa: E402

config.renderer = "cairo"

import construct_quadrilateral_3sides_2diagonals as M  # noqa: E402

print("--- element sizes ---")
for name, mob in [
    ("measure_card 18", M.measure_card(r"AB=4.5", M.CHALK_CYAN)),
    ("measure_card 16", M.measure_card(r"BD=5.4", M.CHALK_AMBER, 16)),
    ("measure_card 15", M.measure_card(r"OL=7.5", M.CHALK_CYAN, 15)),
    ("board_text 17", M.board_text("3 sides", 17, M.CHALK_CYAN, "BOLD")),
    ("board_text 19", M.board_text("Which three should we use first?", 19,
                                   M.CHALK_WHITE, "BOLD")),
    ("board_text 22", M.board_text("Three Sides and Two Diagonals", 22,
                                   M.CHALK_AMBER, "BOLD")),
    ("board_text 18", M.board_text("B", 18, M.CHALK_WHITE, "BOLD")),
    ("combo_card", M.combo_card("1. SKETCH", "mark 3 sides + 2 diagonals",
                                M.CHALK_CYAN)),
    ("summary_row", M.summary_row(1, "Two sides + one diagonal:",
                                  r"\triangle ABC", M.CHALK_YELLOW)),
]:
    print(f"  {name:16s} w={mob.width:5.2f} h={mob.height:5.2f}")


def bounds(mob, name, pad=0.0):
    l, r = mob.get_left()[0], mob.get_right()[0]
    b, t = mob.get_bottom()[1], mob.get_top()[1]
    bad = []
    if l < M.BOARD_LEFT + pad:
        bad.append("OUT-LEFT")
    if r > M.BOARD_RIGHT - pad:
        bad.append("OUT-RIGHT")
    if t > M.BOARD_TOP - pad:
        bad.append("OUT-TOP")
    if b < M.BOARD_BOTTOM + pad:
        bad.append("OUT-BOTTOM")
    print(f"  {name:22s} x[{l:+.2f},{r:+.2f}] y[{b:+.2f},{t:+.2f}] "
          f"{' '.join(bad) if bad else 'ok'}")
    return l, r, b, t


# ---------------------------------------------------------- scene 1 rows ----
print("\n--- scene 1 stack (proposed) ---")
heading_y, lab1_y, row1_y, lab2_y, row2_y = 2.72, 2.16, 1.60, 1.05, 0.485
heading = M.board_text("Three Sides and Two Diagonals", 22, M.CHALK_AMBER,
                       "BOLD").move_to(np.array([M.BOARD_CX, heading_y, 0]))
lab1 = M.board_text("3 sides", 17, M.CHALK_CYAN, "BOLD").move_to(
    np.array([M.BOARD_CX, lab1_y, 0]))
sides = M.VGroup(
    M.measure_card(r"AB=4.5", M.CHALK_CYAN),
    M.measure_card(r"BC=5.2", M.CHALK_CYAN),
    M.measure_card(r"CD=4.8", M.CHALK_CYAN),
).arrange(M.RIGHT, buff=0.30).move_to(np.array([M.BOARD_CX, row1_y, 0]))
lab2 = M.board_text("2 diagonals", 17, M.CHALK_AMBER, "BOLD").move_to(
    np.array([M.BOARD_CX, lab2_y, 0]))
diags = M.VGroup(
    M.measure_card(r"AC=5", M.CHALK_YELLOW),
    M.measure_card(r"BD=5.4", M.CHALK_AMBER),
).arrange(M.RIGHT, buff=0.30).move_to(np.array([M.BOARD_CX, row2_y, 0]))
strip = M.board_text("3 Sides + 2 Diagonals", 21, M.CHALK_GREEN, "BOLD"
                     ).move_to(np.array([M.BOARD_CX, -1.75, 0]))

bh = bounds(heading, "heading")
b1 = bounds(lab1, "3 sides")
bs = bounds(sides, "sides row")
b2 = bounds(lab2, "2 diagonals")
bd = bounds(diags, "diagonals row")
bstr = bounds(strip, "strip")
print(f"  gap heading->label1   {b1[3] - bh[2]:+.2f}")
print(f"  gap label1->row1      {bs[3] - b1[2]:+.2f}")
print(f"  gap row1->label2      {b2[3] - bs[2]:+.2f}")
print(f"  gap label2->row2      {bd[3] - b2[2]:+.2f}")
print(f"  gap row2->strip       {bstr[3] - bd[2]:+.2f}")

# ------------------------------------------------- scene 8 / 9 / 10 figures --
print("\n--- scene 8 mini figure (origin BOARD_CX+1.7) ---")
A, B, C, D = M.example_frame(origin=np.array([M.BOARD_CX + 1.7, 0.55, 0]),
                             scale=0.28)
mini = M.VGroup(
    M.Polygon(A, B, C, D, color=M.CHALK_WHITE, stroke_width=2.0),
    M.Line(A, C, color=M.CHALK_YELLOW, stroke_width=3.0),
    M.Line(B, D, color=M.CHALK_AMBER, stroke_width=2.4),
    M.Polygon(A, B, C, color=M.CHALK_CYAN, stroke_width=1.6,
              fill_color=M.CHALK_CYAN, fill_opacity=0.18),
    M.locating_arc(B, D, 5.4 * 0.28, 20, M.CHALK_AMBER),
    M.locating_arc(C, D, 4.8 * 0.28, 20, M.CHALK_PINK),
    M.Dot(radius=0.07, color=M.CHALK_YELLOW).move_to(D),
    M.diamond_names(A, B, C, D, "ABCD", 13, pull=0.05),
)
l, r, b, t = bounds(mini, "mini figure")
print(f"  gap to steps column (right edge -0.35): {l - (-0.35):+.2f}")

print("\n--- scene 9 GOLD (origin BOARD_CX-2.3) ---")
G, O, L, Dp = M.practice_frame(origin=np.array([M.BOARD_CX - 2.3, -0.25, 0]),
                               scale=0.34)
lab_gl = M.board_text("GL = 6", 15, M.CHALK_GREEN, "BOLD").move_to(
    L + np.array([0.66, -0.50, 0]))
names = M.VGroup(
    M.board_text("G", 15, M.CHALK_WHITE, "BOLD").move_to(G + np.array([-0.30, 0.02, 0])),
    M.board_text("O", 15, M.CHALK_WHITE, "BOLD").move_to(O + np.array([-0.30, -0.28, 0])),
    M.board_text("L", 15, M.CHALK_WHITE, "BOLD").move_to(L + np.array([0.26, -0.02, 0])),
    M.board_text("D", 15, M.CHALK_WHITE, "BOLD").move_to(Dp + np.array([-0.02, 0.30, 0])),
)
quad = M.Polygon(G, O, L, Dp, color=M.CHALK_WHITE, stroke_width=2.4)
arc_l = M.locating_arc(L, O, 7.5 * 0.34, 14 + 4, M.CHALK_CYAN)
arc_d = M.locating_arc(Dp, O, 10.0 * 0.34, 14 + 4, M.CHALK_PINK)
bounds(quad, "rough quad")
bounds(names, "vertex names")
bounds(lab_gl, "GL label")
bounds(M.VGroup(arc_l, arc_d), "both arcs (sector+4deg)")
cards = M.VGroup(*[M.measure_card(s, M.CHALK_CYAN, 15) for s in
                   (r"OL=7.5", r"GL=6", r"LD=5", r"DG=5.5", r"OD=10")]
                 ).arrange(M.DOWN, buff=0.20).move_to(
    np.array([M.BOARD_CX + 2.4, 0.55, 0]))
bounds(cards, "cards column")
for name, mob in (("G", names[0]), ("O", names[1]), ("L", names[2]),
                  ("D", names[3]), ("GL label", lab_gl)):
    l2 = mob.get_left()[0]
    r2 = mob.get_right()[0]
    print(f"    {name:9s} x[{l2:+.2f},{r2:+.2f}]")
print(f"  figure/column gap: {cards.get_left()[0] - max(r2 for r2 in [lab_gl.get_right()[0], names[2].get_right()[0]]):+.2f}")
print(f"  ask text x-extent: ", end="")
ask = M.board_text("Which triangle comes first?", 18, M.CHALK_WHITE, "BOLD"
                   ).move_to(np.array([M.BOARD_CX, -2.45, 0]))
bounds(ask, "ask")
print(f"  gap O label -> ask: {ask.get_left()[0] - names[1].get_right()[0]:+.2f}")

print("\n--- scene 10 recap (origin BOARD_CX-3.1) ---")
A, B, C, D = M.example_frame(origin=np.array([M.BOARD_CX - 3.1, 0.55, 0]),
                             scale=0.30)
quad = M.Polygon(A, B, C, D, color=M.CHALK_CYAN, stroke_width=2.2)
bounds(quad, "recap quad")
names = M.diamond_names(A, B, C, D, "ABCD", 15, pull=0.05)
bounds(names, "recap names")
rows = M.VGroup(
    M.summary_row(1, "Two sides + one diagonal:", r"\triangle ABC", M.CHALK_YELLOW),
    M.summary_row(2, "One side + one diagonal:", r"D", M.CHALK_AMBER),
    M.summary_row(3, "The fifth side is fixed by the drawing:", r"AD", M.CHALK_GREEN),
).arrange(M.DOWN, buff=0.18, aligned_edge=M.LEFT).move_to(
    np.array([M.BOARD_CX + 1.8, 1.35, 0]))
bounds(rows, "rows")
print(f"  gap figure -> rows: {rows.get_left()[0] - names.get_right()[0]:+.2f}")
final = M.board_text("3 build, 2 locate.", 18, M.CHALK_GREEN, "BOLD").move_to(
    np.array([M.BOARD_CX, -1.90, 0]))
take = M.board_text("Sketch, find the triangle, intersect, join.", 16,
                    M.CHALK_WHITE, "BOLD").move_to(np.array([M.BOARD_CX, -2.45, 0]))
bounds(final, "final line")
bounds(take, "take line")
print(f"  gap quad bottom -> final: {final.get_top()[1] - quad.get_bottom()[1]:+.2f}")

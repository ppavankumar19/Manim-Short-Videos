"""Geometry and layout sanity probe for storyboard 04.

Prints the constructed points, the realised side/diagonal lengths and the board
bounds of every label used in the beats, so positions can be judged before a
render is spent.

    .venv/Scripts/python.exe probe_layout.py
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


def dist(p, q) -> float:
    return float(np.linalg.norm(np.array(p, dtype=float) - np.array(q, dtype=float)))


def report(name, pts, scale, want):
    print(f"--- {name} (scale {scale}) ---")
    for i, p in enumerate(pts):
        print(f"  {i}: ({p[0]:+.3f}, {p[1]:+.3f})")
    for label, (a, b, cm) in want.items():
        got = dist(pts[a], pts[b]) / scale
        flag = "OK " if abs(got - cm) < 0.02 else "BAD"
        print(f"  {flag} {label}: {got:.3f} cm (want {cm})")


A, B, C, D = M.example_frame()
report("example_frame", (A, B, C, D), M.SCALE,
       {"AB": (0, 1, 4.5), "BC": (1, 2, 5.2), "CD": (2, 3, 4.8),
        "AC": (0, 2, 5.0), "BD": (1, 3, 5.4), "AD?": (0, 3, 0.0)})

G, O, L, D2 = M.practice_frame()
report("practice_frame", (G, O, L, D2), 0.40,
       {"GL": (0, 2, 6.0), "LD": (2, 3, 5.0), "DG": (3, 0, 5.5),
        "OL": (1, 2, 7.5), "OD": (1, 3, 10.0)})

# does D sit on the far side of A C?
def side(p, a, b) -> float:
    a, b, p = (np.array(v, dtype=float) for v in (a, b, p))
    return float(np.cross(b - a, p - a)[2])


print(f"  side(AC, B)={side(B, A, C):+.3f}  side(AC, D)={side(D, A, C):+.3f}")
print(f"  side(GL, D)={side(D2, G, L):+.3f}  side(GL, O)={side(O, G, L):+.3f}")

# --- board bounds of the real labels ---------------------------------------
board = dict(left=M.BOARD_LEFT, right=M.BOARD_RIGHT, top=M.BOARD_TOP,
             bottom=M.BOARD_BOTTOM)


def bounds(mob, name):
    l, r = mob.get_left()[0], mob.get_right()[0]
    b, t = mob.get_bottom()[1], mob.get_top()[1]
    bad = []
    if l < board["left"]:
        bad.append("OUT-LEFT")
    if r > board["right"]:
        bad.append("OUT-RIGHT")
    if t > board["top"]:
        bad.append("OUT-TOP")
    if b < board["bottom"]:
        bad.append("OUT-BOTTOM")
    print(f"  {name:22s} x[{l:+.2f},{r:+.2f}] y[{b:+.2f},{t:+.2f}] "
          f"{' '.join(bad) if bad else 'ok'}")


# default frame labels
names = M.diamond_names(A, B, C, D, "ABCD", 17)
print("--- labels on the default example frame ---")
for letter, mob in zip("ABCD", names):
    bounds(mob, f"name {letter}")
cen = np.array([A, B, C, D], dtype=float).mean(axis=0)
for letter, (p, q) in zip(("AB", "BC", "CD", "DA"), ((A, B), (B, C), (C, D), (D, A))):
    lab = M.side_label(p, q, cen, f"{letter} = 9.9", M.CHALK_CYAN, 16, 0.18)
    bounds(lab, f"side {letter}")
lab_ac = M.board_text("AC = 5 cm", 17, M.CHALK_CYAN, "BOLD").move_to((A + C) / 2 + M.DOWN * 0.62)
bounds(lab_ac, "AC=5 under")
lab_bc = M.side_label(C, B, B + C - cen, "BC = 5.2 cm", M.CHALK_YELLOW, 16, 0.18)
bounds(lab_bc, "BC outward")
rad = M.radius_line(B, D, M.CHALK_AMBER, "diagonal BD = 5.4 cm", 15)
bounds(rad, "radius BD")

# practice / challenge frame labels
names2 = M.diamond_names(G, D2, L, O, "GOLD", 15, pull=0.05)
print("--- labels on the practice frame ---")
for letter, mob in zip("GOLD", names2):
    bounds(mob, f"name {letter}")

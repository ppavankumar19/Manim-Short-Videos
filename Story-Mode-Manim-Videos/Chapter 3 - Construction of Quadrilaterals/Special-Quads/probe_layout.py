"""Geometry and layout check for storyboard 07 (special quadrilaterals).

Re-measures all three figures off the constructed vertices -- the two sides and
the angle of the parallelogram, the perpendicular-bisecting diagonals of the
rhombus, the equal diagonals of the square -- and checks the board bounds.

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

import construct_special_quadrilaterals_rhombus_parallelogram as M  # noqa: E402

LEFT, RIGHT, TOP, BOTTOM = (M.BOARD_LEFT, M.BOARD_RIGHT, M.BOARD_TOP,
                            M.BOARD_BOTTOM)


def dist(p, q) -> float:
    return float(np.linalg.norm(np.array(p, dtype=float)
                                - np.array(q, dtype=float)))


def angle_at(v, p, q) -> float:
    d1 = np.array(p, dtype=float) - np.array(v, dtype=float)
    d2 = np.array(q, dtype=float) - np.array(v, dtype=float)
    c = float(np.dot(d1[:2], d2[:2])
              / (np.linalg.norm(d1[:2]) * np.linalg.norm(d2[:2])))
    return float(np.degrees(np.arccos(max(-1.0, min(1.0, c)))))


def bounds(mob, name, pad=0.0):
    l, r = mob.get_left()[0], mob.get_right()[0]
    b, t = mob.get_bottom()[1], mob.get_top()[1]
    bad = []
    if l < LEFT + pad:
        bad.append("OUT-LEFT")
    if r > RIGHT - pad:
        bad.append("OUT-RIGHT")
    if t > TOP - pad:
        bad.append("OUT-TOP")
    if b < BOTTOM + pad:
        bad.append("OUT-BOTTOM")
    print(f"  {name:26s} x[{l:+.2f},{r:+.2f}] y[{b:+.2f},{t:+.2f}] "
          f"{' '.join(bad) if bad else 'ok'}")


# ------------------------------------------------------------ parallelogram --
print("--- parallelogram B E L T (BE=4.2, EL=5, angle T=45) ---")
d = M.parallelogram_frame()
B, E, L, T = d["quad"]
s = M.PARA_SCALE
print(f"  B({B[0]:+.3f},{B[1]:+.3f}) E({E[0]:+.3f},{E[1]:+.3f}) "
      f"L({L[0]:+.3f},{L[1]:+.3f}) T({T[0]:+.3f},{T[1]:+.3f})")
for label, (a, b, cm) in {"BE": (0, 1, 4.2), "EL": (1, 2, 5.0),
                          "LT": (2, 3, 4.2), "TB": (3, 0, 5.0)}.items():
    got = dist((B, E, L, T)[a], (B, E, L, T)[b]) / s
    print(f"  {'OK ' if abs(got - cm) < 0.02 else 'BAD'} {label}: {got:.3f} "
          f"cm (want {cm})")
for label, (v, a, b, deg) in {"angle E": (1, 0, 2, 45.0),
                              "angle T": (3, 2, 0, 45.0),
                              "angle L": (2, 1, 3, 135.0),
                              "angle B": (0, 1, 3, 135.0)}.items():
    got = angle_at((B, E, L, T)[v], (B, E, L, T)[a], (B, E, L, T)[b])
    print(f"  {'OK ' if abs(got - deg) < 0.5 else 'BAD'} {label}: {got:.2f} "
          f"deg (want {deg})")
quad = M.Polygon(B, E, L, T, color=M.CHALK_WHITE)
bounds(quad, "quad BELT")
print(f"  parallel: BE vs TL -> "
      f"{abs(np.cross((E - B), (L - T))[2]):.4f} (0 is parallel)")
print(f"  parallel: EL vs BT -> "
      f"{abs(np.cross((L - E), (T - B))[2]):.4f} (0 is parallel)")

# ------------------------------------------------------------------ rhombus --
print("\n--- rhombus A B C D (diagonals 4.5 and 6) ---")
r = M.rhombus_frame()
A, Bb, C, D = r["quad"]
s = M.RHOMB_SCALE
O = M.mid(A, C)
print(f"  A({A[0]:+.3f},{A[1]:+.3f}) B({Bb[0]:+.3f},{Bb[1]:+.3f}) "
      f"C({C[0]:+.3f},{C[1]:+.3f}) D({D[0]:+.3f},{D[1]:+.3f}) "
      f"O({O[0]:+.3f},{O[1]:+.3f})")
print(f"  {'OK ' if abs(dist(A, C) / s - 4.5) < 0.02 else 'BAD'} AC: "
      f"{dist(A, C) / s:.3f} cm")
print(f"  {'OK ' if abs(dist(Bb, D) / s - 6.0) < 0.02 else 'BAD'} BD: "
      f"{dist(Bb, D) / s:.3f} cm")
print(f"  halves: OA {dist(O, A) / s:.3f}  OC {dist(O, C) / s:.3f}  "
      f"OB {dist(O, Bb) / s:.3f}  OD {dist(O, D) / s:.3f}")
sides = [dist(A, Bb), dist(Bb, C), dist(C, D), dist(D, A)]
print(f"  sides (should be equal): "
      f"{[round(x / s, 3) for x in sides]}")
print(f"  AC . BD = {abs(np.dot((C - A), (D - Bb))):.4f} (0 is a right "
      f"angle)")
bounds(M.Polygon(A, Bb, C, D, color=M.CHALK_WHITE), "rhombus ABCD")

# ------------------------------------------------------------------- square --
print("\n--- square J U M P (diagonal 4.2) ---")
q = M.square_frame()
J, Mm, U, Pp = q["quad"]
s = M.SQUARE_SCALE
O = M.mid(J, U)
print(f"  J({J[0]:+.3f},{J[1]:+.3f}) M({Mm[0]:+.3f},{Mm[1]:+.3f}) "
      f"U({U[0]:+.3f},{U[1]:+.3f}) P({Pp[0]:+.3f},{Pp[1]:+.3f})")
print(f"  JU {dist(J, U) / s:.3f} cm, MP {dist(Mm, Pp) / s:.3f} cm")
print(f"  halves: OJ {dist(O, J) / s:.3f}  OM {dist(O, Mm) / s:.3f}")
sides = [dist(J, Mm), dist(Mm, U), dist(U, Pp), dist(Pp, J)]
print(f"  sides: {[round(x / s, 3) for x in sides]}")
print(f"  JU . MP = {abs(np.dot((U - J), (Pp - Mm))):.4f}")
bounds(M.Polygon(J, Mm, U, Pp, color=M.CHALK_WHITE), "square JUMP")

# ------------------------------------------------------- letters and column --
print("\n--- letters and the right-hand column ---")
names = M.VGroup(*[
    M.board_text(letter, 17, M.CHALK_WHITE, "BOLD").move_to(
        np.array(p, dtype=float) + np.array([off[0], off[1], 0.0]))
    for letter, p, off in zip("BELT", (B, E, L, T),
                              ((-0.10, -0.28), (0.12, -0.30), (0.30, 0.10),
                               (-0.30, 0.10)))])
bounds(names, "BELT letters")
names_r = M.VGroup(*[
    M.board_text(letter, 17, M.CHALK_WHITE, "BOLD").move_to(
        np.array(p, dtype=float) + np.array([off[0], off[1], 0.0]))
    for letter, p, off in zip("ABCD", (A, Bb, C, D),
                              ((-0.30, 0.02), (0.06, 0.26), (0.26, 0.02),
                               (0.06, -0.34)))])
bounds(names_r, "ABCD letters")
for y in (1.75, 1.15, 0.55, -0.35, -1.10):
    bounds(M.measure_card(r"AC=4.5", M.CHALK_YELLOW).move_to(
        np.array([3.05, y, 0])), f"card at y={y:+.2f}")
notes = M.board_text("Diagonals bisect each\nother at right angles", 15,
                     M.CHALK_WHITE, "BOLD").move_to(
    np.array([3.05, -1.60, 0]))
bounds(notes, "two-line note")



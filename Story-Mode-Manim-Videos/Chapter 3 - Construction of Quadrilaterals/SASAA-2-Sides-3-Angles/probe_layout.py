"""Geometry check for storyboard 05 (S.A.S.A.A).

Re-measures both figures off the constructed vertices -- the two sides, the
three angles, the crossing point and the board bounds -- before a render is
spent on them.

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

import construct_quadrilateral_2sides_3angles as M  # noqa: E402

LEFT, RIGHT, TOP, BOTTOM = (M.BOARD_LEFT, M.BOARD_RIGHT, M.BOARD_TOP,
                            M.BOARD_BOTTOM)


def dist(p, q) -> float:
    return float(np.linalg.norm(np.array(p, dtype=float) - np.array(q,
                                                                 dtype=float)))


def angle_at(v, p, q) -> float:
    """The interior angle at v between the directions to p and to q."""
    d1 = np.array(p, dtype=float) - np.array(v, dtype=float)
    d2 = np.array(q, dtype=float) - np.array(v, dtype=float)
    c = float(np.dot(d1[:2], d2[:2]) / (np.linalg.norm(d1[:2]) * np.linalg.norm(d2[:2])))
    return float(np.degrees(np.arccos(max(-1.0, min(1.0, c)))))


def report(name, pts, scale, sides, angles):
    print(f"--- {name} (scale {scale}) ---")
    for letter, p in zip("PQRS", pts):
        print(f"  {letter} ({p[0]:+.3f}, {p[1]:+.3f})")
    for label, (a, b, cm) in sides.items():
        got = dist(pts[a], pts[b]) / scale
        print(f"  {'OK ' if abs(got - cm) < 0.02 else 'BAD'} {label}: "
              f"{got:.3f} cm (want {cm})")
    for label, (v, a, b, deg) in angles.items():
        got = angle_at(pts[v], pts[a], pts[b])
        print(f"  {'OK ' if abs(got - deg) < 0.5 else 'BAD'} {label}: "
              f"{got:.2f} deg (want {deg})")


P, Q, R, S = M.example_frame()
report("example_frame (P Q R S)", (P, Q, R, S), M.SCALE,
       {"PQ": (0, 1, 4.0), "QR": (1, 2, 4.8),
        "PS (not given)": (0, 3, 0), "RS (not given)": (2, 3, 0)},
       {"angle P": (0, 1, 3, 75.0), "angle Q": (1, 0, 2, 100.0),
        "angle R": (2, 1, 3, 120.0), "angle S": (3, 2, 0, 65.0)})

A, B, C, D = M.practice_frame()
report("practice_frame (A B C D)", (A, B, C, D), M.PRACTICE_SCALE,
       {"AB": (0, 1, 5.0), "BC": (1, 2, 4.0)},
       {"angle A": (0, 1, 3, 70.0), "angle B": (1, 0, 2, 110.0),
        "angle C": (2, 1, 3, 120.0), "angle D": (3, 2, 0, 60.0)})

print("\n--- board bounds: example figure + its labels ---")
board = dict(left=LEFT, right=RIGHT, top=TOP, bottom=BOTTOM)


def bounds(mob, name):
    l, r = mob.get_left()[0], mob.get_right()[0]
    b, t = mob.get_bottom()[1], mob.get_top()[1]
    bad = []
    if l < board["left"] + 0.12:
        bad.append("OUT-LEFT")
    if r > board["right"] - 0.12:
        bad.append("OUT-RIGHT")
    if t > board["top"] - 0.05:
        bad.append("OUT-TOP")
    if b < board["bottom"]:
        bad.append("OUT-BOTTOM")
    print(f"  {name:22s} x[{l:+.2f},{r:+.2f}] y[{b:+.2f},{t:+.2f}] "
          f"{' '.join(bad) if bad else 'ok'}")


quad = M.Polygon(P, Q, R, S, color=M.CHALK_WHITE)
bounds(quad, "quad PQRS")
names = M.diamond_names(P, R, Q, S, "PRQS", 17)
for letter, mob in zip("PRQS", names):
    bounds(mob, f"name {letter}")

# the two rays, extended a little past S
ray_p = M.Line(P, M.ray_point(P, M.dir_deg(P, S), dist(P, S) * 1.16))
ray_r = M.Line(R, M.ray_point(R, M.dir_deg(R, S), dist(R, S) * 1.20))
bounds(M.VGroup(ray_p, ray_r), "the two rays (+16/20%)")
for name, mob in (("pin", M.Polygon(P, Q, R, color=M.CHALK_YELLOW)),
                  ("triangle PQR", M.Polygon(P, Q, R, color=M.CHALK_CYAN))):
    bounds(mob, name)

print("\n--- right-hand column space ---")
print(f"  figure right edge {max(P[0], Q[0], R[0], S[0]):+.2f} "
      f"-> space up to {RIGHT:+.2f}")

print("\n--- compass setout of 120 deg at R (chord points) ---")
r_len = 1.05
arm = M.dir_deg(R, Q)
ray = M.dir_deg(R, S)
step = 60.0 if ((ray - arm) % 360.0) > 180.0 else -60.0
A1 = M.ray_point(R, arm, r_len)
A2 = M.ray_point(R, arm + step, r_len)
A3 = M.ray_point(R, arm + 2 * step, r_len)
print(f"  arm {arm:7.2f}  ray {ray:7.2f}  step {step:+.0f}")
print(f"  A1 ({A1[0]:+.2f},{A1[1]:+.2f})  A2 ({A2[0]:+.2f},{A2[1]:+.2f})  "
      f"A3 ({A3[0]:+.2f},{A3[1]:+.2f})")
print(f"  |A1-A2| {dist(A1, A2):.3f}  |A2-A3| {dist(A2, A3):.3f}  "
      f"(both should be {r_len:.2f} = the compass opening)")
print(f"  A3 on the R S ray: {abs(((M.dir_deg(R, A3) - ray + 180) % 360) - 180):.3f} deg off")
bounds(M.VGroup(*[M.Dot(radius=0.05, color=M.CHALK_PINK).move_to(p)
                  for p in (A1, A2, A3)]), "chord points")

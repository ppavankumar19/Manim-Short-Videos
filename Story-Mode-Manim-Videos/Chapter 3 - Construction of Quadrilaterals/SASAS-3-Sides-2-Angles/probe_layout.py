"""Geometry and layout check for storyboard 06 (S.A.S.A.S).

Re-measures both figures off the constructed vertices -- the three sides, the
two included angles, the angles that follow, and the board bounds -- and checks
that the five-card chain row of scene 1 fits the board.

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

import construct_quadrilateral_3sides_2angles as M  # noqa: E402

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


def report(name, pts, scale, sides, angles):
    print(f"--- {name} (scale {scale}) ---")
    for letter, p in zip("ABCD", pts):
        print(f"  {letter} ({p[0]:+.3f}, {p[1]:+.3f})")
    for label, (a, b, cm) in sides.items():
        got = dist(pts[a], pts[b]) / scale
        ok = "OK " if cm is not None and abs(got - cm) < 0.02 else (
            "    " if cm is None else "BAD")
        print(f"  {ok} {label}: {got:.3f} cm" + (f" (want {cm})" if cm else ""))
    for label, (v, a, b, deg) in angles.items():
        got = angle_at(pts[v], pts[a], pts[b])
        ok = "OK " if deg is not None and abs(got - deg) < 0.5 else (
            "    " if deg is None else "BAD")
        print(f"  {ok} {label}: {got:.2f} deg" + (f" (want {deg})" if deg else ""))


A, B, C, D = M.example_frame()
report("example_frame (Example 8)", (A, B, C, D), M.SCALE,
       {"AB": (0, 1, 5.0), "BC": (1, 2, 4.5), "CD": (2, 3, 6.0),
        "AD (not given)": (0, 3, None)},
       {"angle B": (1, 0, 2, 100.0), "angle C": (2, 1, 3, 75.0),
        "angle A": (0, 1, 3, None), "angle D": (3, 2, 0, None)})
print(f"  convex: {M._convex(A, B, C, D)}")

P, Q, R, S = M.practice_frame()
report("practice_frame (Ex 3.5a)", (P, Q, R, S), M.PRACTICE_SCALE,
       {"PQ": (0, 1, 3.6), "QR": (1, 2, 4.5), "RS": (2, 3, 5.6),
        "PS (not given)": (0, 3, None)},
       {"angle Q": (1, 0, 2, 135.0), "angle R": (2, 1, 3, 60.0),
        "angle P": (0, 1, 3, None), "angle S": (3, 2, 0, None)})
print(f"  convex: {M._convex(P, Q, R, S)}")


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
    print(f"  {name:24s} x[{l:+.2f},{r:+.2f}] y[{b:+.2f},{t:+.2f}] "
          f"{' '.join(bad) if bad else 'ok'}")


print("\n--- example figure, letters and rays ---")
bounds(M.Polygon(A, B, C, D, color=M.CHALK_WHITE), "quad ABCD")
d = M.example_construction()
letters = M.VGroup(*[
    M.board_text(letter, 17, M.CHALK_WHITE, "BOLD").move_to(
        np.array(p, dtype=float) + np.array([off[0], off[1], 0.0]))
    for letter, p, off in zip("ABCD", (A, B, C, D),
                              ((-0.28, -0.10), (0.14, -0.30), (0.30, 0.02),
                               (-0.10, 0.30)))])
bounds(letters, "vertex letters")
ray_b = M.Line(B, M.ray_point(B, d["bc_deg"], dist(B, C) * 1.12),
               color=M.CHALK_AMBER)
ray_c = M.Line(C, M.ray_point(C, d["cd_deg"], 6.0 * M.SCALE * 1.02),
               color=M.CHALK_PINK)
bounds(M.VGroup(ray_b, ray_c), "both rays")
bounds(M.arc_center if False else M.Dot(radius=0.05).move_to(C), "C dot")
ang_b = M.angle_mark(B, A, C, radius=0.85, color=M.CHALK_AMBER, label="100°")
ang_c = M.angle_mark(C, B, D, radius=0.85, color=M.CHALK_PINK, label="75°")
bounds(M.VGroup(ang_b, ang_c), "both angle marks")

print("\n--- scene 1 chain row ---")
row = M.VGroup(
    M.measure_card(r"AB=5", M.CHALK_CYAN),
    M.degree_card(r"\angle B = 100^\circ", M.CHALK_AMBER),
    M.measure_card(r"BC=4.5", M.CHALK_CYAN),
    M.degree_card(r"\angle C = 75^\circ", M.CHALK_PINK),
    M.measure_card(r"CD=6", M.CHALK_CYAN),
).arrange(M.RIGHT, buff=0.42).move_to(np.array([M.BOARD_CX, 0.55, 0]))
bounds(row, "five cards")
print(f"  card widths: {[round(m.width, 2) for m in row]}")
letters_sas = M.VGroup(*[
    M.board_text(s, 15, M.CHALK_GREEN, "BOLD").move_to(
        np.array([m.get_center()[0], 0.05, 0])) for m, s in zip(row, "SASAS")])
bounds(letters_sas, "S A S A S row")
strip = M.board_text("S.A.S.A.S", 21, M.CHALK_GREEN, "BOLD").move_to(
    np.array([M.BOARD_CX, -1.30, 0]))
box = M.SurroundingRectangle(strip, color=M.CHALK_GREEN, buff=0.16,
                             corner_radius=0.1, stroke_width=2.6)
bounds(M.VGroup(strip, box), "boxed S.A.S.A.S")
spell = M.board_text("Side – Angle – Side – Angle – Side", 16, M.CHALK_WHITE,
                     "BOLD").move_to(np.array([M.BOARD_CX, -1.85, 0]))
bounds(spell, "spelled-out line")
print("\n--- right column ---")
for y in (1.55, 0.95, 0.35, -0.55, -1.30):
    bounds(M.measure_card(r"AB=5", M.CHALK_YELLOW).move_to(
        np.array([3.05, y, 0])), f"card at y={y:+.2f}")

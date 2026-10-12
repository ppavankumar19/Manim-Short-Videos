"""Numeric check of every compass arc / label position used in storyboard 04.

    .venv/Scripts/python.exe probe_arcs.py
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

LEFT, RIGHT, TOP, BOTTOM = M.BOARD_LEFT, M.BOARD_RIGHT, M.BOARD_TOP, M.BOARD_BOTTOM


def arc_pts(centre, target, radius, spread, bias=0.0, n=25):
    C = np.array(centre, dtype=float)
    ang = float(np.degrees(np.arctan2(target[1] - C[1], target[0] - C[0])))
    start = ang - spread + bias
    out = []
    for i in range(n + 1):
        a = (start + 2 * spread * i / n) * M.DEGREES
        out.append(C + radius * np.array([np.cos(a), np.sin(a), 0.0]))
    return np.array(out)


def show(name, pts, target=None):
    x0, x1 = pts[:, 0].min(), pts[:, 0].max()
    y0, y1 = pts[:, 1].min(), pts[:, 1].max()
    bad = []
    if x0 < LEFT:
        bad.append("OUT-LEFT")
    if x1 > RIGHT:
        bad.append("OUT-RIGHT")
    if y1 > TOP:
        bad.append("OUT-TOP")
    if y0 < BOTTOM:
        bad.append("OUT-BOTTOM")
    tw = ""
    if target is not None:
        d = np.linalg.norm(pts - np.array(target, dtype=float), axis=1).min()
        tw = f" nearest-to-target {d:.3f}"
    print(f"  {name:28s} x[{x0:+.2f},{x1:+.2f}] y[{y0:+.2f},{y1:+.2f}] "
          f"{' '.join(bad) if bad else 'ok'}{tw}")


def quads(name, A, B, C, D, scale):
    print(f"--- {name} ---")
    for letter, p in zip("ABCD", (A, B, C, D)):
        print(f"  {letter} ({p[0]:+.3f},{p[1]:+.3f})")
    for lab, (p, q, cm) in {"AB": (A, B, 4.5), "BC": (B, C, 5.2),
                            "CD": (C, D, 4.8), "AC": (A, C, 5.0),
                            "BD": (B, D, 5.4)}.items():
        got = np.linalg.norm(np.array(p) - np.array(q)) / scale
        print(f"  {'OK ' if abs(got - cm) < 0.02 else 'BAD'} {lab} {got:.2f} ({cm})")


# ---------------------------------------------------------------- example ----
A, B, C, D = M.example_frame()
quads("example_frame (default)", A, B, C, D, M.SCALE)
print("  arcs:")
show("A r=AB 16 deg", arc_pts(A, B, 4.5 * M.SCALE, 16), B)
show("A r=AB 16 b+4", arc_pts(A, B, 4.5 * M.SCALE, 16, 4), B)
show("C r=CB 15 deg", arc_pts(C, B, 5.2 * M.SCALE, 15), B)
show("B r=BD 16 deg", arc_pts(B, D, 5.4 * M.SCALE, 16), D)
show("C r=CD 16 deg", arc_pts(C, D, 4.8 * M.SCALE, 16), D)
show("C r=CD 14 b+8", arc_pts(C, D, 4.8 * M.SCALE, 14, 8), D)
show("B r=BD 14 b-6", arc_pts(B, D, 5.4 * M.SCALE, 14, -6), D)

# --------------------------------------------------------------- practice ----
for scale, base_y in ((0.40, -0.40), (0.34, -0.25), (0.30, -0.10), (0.32, -0.20)):
    G, O, L, Dp = M.practice_frame(
        origin=np.array([M.BOARD_CX - 2.9, base_y, 0.0]), scale=scale)
    print(f"--- practice_frame scale={scale} base_y={base_y} ---")
    for letter, p in zip("GOLD", (G, O, L, Dp)):
        print(f"  {letter} ({p[0]:+.3f},{p[1]:+.3f})")
    for lab, (p, q, cm) in {"GL": (G, L, 6.0), "LD": (L, Dp, 5.0),
                            "DG": (Dp, G, 5.5), "OL": (O, L, 7.5),
                            "OD": (O, Dp, 10.0)}.items():
        got = np.linalg.norm(np.array(p) - np.array(q)) / scale
        print(f"  {'OK ' if abs(got - cm) < 0.02 else 'BAD'} {lab} {got:.2f} ({cm})")
    for spread, bias in ((14, 0), (14, 4), (12, 8), (16, 0)):
        show(f"L r=OL {spread} b{bias:+d}",
             arc_pts(L, O, 7.5 * scale, spread, bias), O)
    for spread, bias in ((14, 0), (14, 4), (12, 8), (10, 10)):
        show(f"D r=OD {spread} b{bias:+d}",
             arc_pts(Dp, O, 10.0 * scale, spread, bias), O)

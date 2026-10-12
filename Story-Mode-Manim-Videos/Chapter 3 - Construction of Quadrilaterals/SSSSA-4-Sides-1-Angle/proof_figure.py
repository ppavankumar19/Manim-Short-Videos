"""Proof figure: both constructed quadrilaterals with their measurements
re-read from the computed vertex coordinates.

Run from the topic folder:
    python -m manim render -s -r 1920,1080 --media_dir D:\\m3 proof_figure.py ProofFigure

The numbers on the board are measured from the points the scene actually
draws, so a wrong `example_frame()` / `exercise_frame()` would show up here as a
value that does not match the given data (Example 1: 4.5, 5.2, 5.5, 4, 120??;
Exercise 3.1(a): 5.5, 3.5, 4, 5, 45??).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "speech_service.py").exists())
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))

from manim import DOWN, RIGHT, MathTex, Polygon, Scene, VGroup  # noqa: E402

import construct_quadrilateral_4sides_1angle as M  # noqa: E402


def side(a, b) -> float:
    return float(np.linalg.norm(np.array(b) - np.array(a)))


def angle_at(v, a, b) -> float:
    u1 = np.array(a, dtype=float) - np.array(v, dtype=float)
    u2 = np.array(b, dtype=float) - np.array(v, dtype=float)
    c = float(np.dot(u1, u2) / (np.linalg.norm(u1) * np.linalg.norm(u2)))
    return float(np.degrees(np.arccos(np.clip(c, -1.0, 1.0))))


def panel(points, letters, title, givens, origin):
    """One figure, anchored at `origin`, with its measured values beside it."""
    pts = [np.array(origin, float) + (np.array(p, float) - np.array(points[0], float))
           for p in points]
    quad = Polygon(*pts, color=M.CHALK_CYAN, stroke_width=3.0,
                   fill_color=M.CHALK_CYAN, fill_opacity=0.12)
    names = M.quad_names(tuple(pts), letters, 22)
    head = M.board_text(title, 26, M.CHALK_AMBER, "BOLD").next_to(
        quad, np.array([0.0, 1.0, 0.0]), buff=0.75)

    rows = []
    for tex, value in givens:
        rows.append(MathTex(tex.format(value), font_size=32,
                            color=M.CHALK_GREEN))
    info = VGroup(*rows).arrange(DOWN, aligned_edge=RIGHT, buff=0.22)
    info.next_to(quad, RIGHT, buff=0.85)
    return VGroup(quad, names, head, info)


class ProofFigure(Scene):
    def construct(self) -> None:
        self.camera.background_color = "#123B2A"
        sc = M.SCALE * 0.62

        P, Q, R, S = M.example_frame(origin=np.array([-4.0, -1.7, 0]), scale=sc)
        A, B, C, D = M.exercise_frame(origin=np.array([-4.0, 2.3, 0]), scale=sc)

        left = panel((P, Q, R, S), "PQRS", "Example 1", (
            (r"PQ = {:.2f}\ \text{{cm}}", side(P, Q)),
            (r"QR = {:.2f}\ \text{{cm}}", side(Q, R)),
            (r"RS = {:.2f}\ \text{{cm}}", side(R, S)),
            (r"PS = {:.2f}\ \text{{cm}}", side(P, S)),
            (r"\angle RQP = {:.0f}^\circ", angle_at(Q, R, P)),
        ), np.array([-4.0, -1.7, 0]))

        right = panel((A, B, C, D), "ABCD", "Exercise 3.1(a)", (
            (r"AB = {:.2f}\ \text{{cm}}", side(A, B)),
            (r"BC = {:.2f}\ \text{{cm}}", side(B, C)),
            (r"CD = {:.2f}\ \text{{cm}}", side(C, D)),
            (r"AD = {:.2f}\ \text{{cm}}", side(A, D)),
            (r"\angle A = {:.0f}^\circ", angle_at(A, B, D)),
        ), np.array([-4.0, 2.3, 0]))

        check = M.board_text(
            "measured off the constructed vertices -- geometry is exact",
            20, M.CHALK_PINK, "BOLD").move_to(np.array([0.3, -3.1, 0]))
        self.add(left, right, check)
        self.wait(0.1)

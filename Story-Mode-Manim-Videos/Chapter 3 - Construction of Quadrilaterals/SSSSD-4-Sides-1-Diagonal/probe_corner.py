import numpy as np
from manim import *
import construct_quadrilateral_4sides_1diagonal as M

def bb(m):
    return (float(m.get_corner(DL)[0]), float(m.get_corner(UR)[0]),
            float(m.get_corner(DL)[1]), float(m.get_corner(UR)[1]))

def clear(label, curves):
    x0, x1, y0, y1 = bb(label); best = 9.9
    for c in curves:
        for part in [m for m in c.get_family() if len(getattr(m, "points", ()))]:
            for t in np.linspace(0, 1, 200):
                p = part.point_from_proportion(t)
                dx = max(x0 - p[0], 0.0, p[0] - x1); dy = max(y0 - p[1], 0.0, p[1] - y1)
                best = min(best, float(np.hypot(dx, dy)))
    return round(best, 3)

def report(tag, P, Q, R, S, sc, spread):
    arcs = [M.locating_arc(P, S, 4.5 * sc if sc > 0.5 else 4.8 * sc, spread, M.CHALK_CYAN),
            M.locating_arc(R, S, 5.0 * sc if sc > 0.5 else 4.2 * sc, spread, M.CHALK_PINK)]
    edges = [Line(P, S), Line(S, R), Line(P, R), Line(P, Q), Line(Q, R)]
    print(f"-- {tag}: S/D at {np.round(S, 2)}")
    for side in ("DL", "DR"):
        for nx, ny in ((0, 0), (0.12, -0.12), (0.22, -0.22), (0.30, -0.30)):
            vec = np.array([(0.12 if side == "DR" else -0.12) + nx * (1 if side == "DR" else -1),
                            -0.12 - ny, 0.0])
            lab = M.vertex_label("X", S, side, M.CHALK_WHITE, 16).shift(vec)
            a = clear(lab, arcs); e = clear(lab, edges)
            print(f"   {side} shift={np.round(vec[:2],2)}: arcs {a:.3f} edges {e:.3f}"
                  f"  {'OK' if min(a, e) > 0.06 else '!!'}")

A, B, C, D = M.example_frame()
report("example (D)", A, B, C, D, M.SCALE, 22)
A, B, C, D = M.example_frame(origin=np.array([M.BOARD_CX + 2.2, 0.55, 0]), scale=0.30)
report("mini scene8 (D)", A, B, C, D, 0.30, 26)
A, B, C, D = M.example_frame(origin=np.array([M.BOARD_CX - 4.2, -1.15, 0]), scale=0.34)
report("mini scene10 (D)", A, B, C, D, 0.34, 24)
P, Q, R, S = M.practice_frame()
report("practice (S)", P, Q, R, S, 0.40, 24)

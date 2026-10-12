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
            for t in np.linspace(0, 1, 240):
                p = part.point_from_proportion(t)
                dx = max(x0 - p[0], 0.0, p[0] - x1); dy = max(y0 - p[1], 0.0, p[1] - y1)
                best = min(best, float(np.hypot(dx, dy)))
    return round(best, 3)

sc = 0.40
P, Q, R, S = M.practice_frame()
arcs = [M.locating_arc(P, S, 4.5 * sc, 24, M.CHALK_CYAN),
        M.locating_arc(R, S, 5.0 * sc, 24, M.CHALK_PINK)]
edges = [Line(P, S), Line(S, R), Line(P, R), Line(P, Q), Line(Q, R)]
print("practice S at", np.round(S, 2))
best = None
for side in ("DL", "DR"):
    for d in (0.00, 0.10, 0.18, 0.26, 0.34):
        for dy in (0.0, -0.08):
            vec = np.array([(0.10 + d) * (1 if side == "DR" else -1),
                            -(0.10 + d) + dy, 0.0])
            lab = M.vertex_label("S", S, side, M.CHALK_WHITE, 16).shift(vec)
            a, e = clear(lab, arcs), clear(lab, edges)
            ok = min(a, e) > 0.07
            print(f"   {side} d={d:.2f} dy={dy:+.2f}: arcs {a:.3f} edges {e:.3f}"
                  f"  {'OK' if ok else '!!'}   centre={np.round(lab.get_center()[:2], 2)}")
            if ok and (best is None or min(a, e) > best[0]):
                best = (min(a, e), side, d, dy, np.round(lab.get_center()[:2], 2))
print("BEST:", best)

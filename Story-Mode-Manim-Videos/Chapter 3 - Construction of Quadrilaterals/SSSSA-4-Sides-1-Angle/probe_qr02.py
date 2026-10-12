import numpy as np
from manim import *
import construct_quadrilateral_4sides_1angle as M

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

P, Q, R, S = M.example_frame()
mid = (Q + R) / 2
arc = M.locompass if False else M.locating_arc(Q, R, 5.2 * M.SCALE, 26, M.CHALK_GREEN)
edges = [Line(P, Q), Line(Q, R), Line(P, R)]
print("mid", np.round(mid, 2), " arc bbox", np.round(bb(arc), 2))
for dx in (0.94, 0.80, 1.05):
    for dy in (-0.17, -0.05, -0.30):
        lab = M.board_text("QR = 5.2 cm", 16, M.CHALK_GREEN, "BOLD").move_to(mid + np.array([dx, dy, 0]))
        a = clear(lab, [arc]); e = clear(lab, edges)
        print(f"   offset ({dx:+.2f},{dy:+.2f}): arc {a:.3f} edges {e:.3f}"
              f"  {'OK' if min(a, e) > 0.12 else '!!'}  centre {np.round(lab.get_center()[:2], 2)}")

"""True collision test for the S vertex letter: sample the construction lines
and arcs and measure the real distance to the label's bounding box."""
import numpy as np
from manim import *

import construct_quadrilateral_4sides_1angle as M


def bbox(m):
    return np.array([float(m.get_corner(DL)[0]), float(m.get_corner(UR)[0]),
                     float(m.get_corner(DL)[1]), float(m.get_corner(UR)[1])])


def dist_to_box(p, box):
    """0 when the point is inside the box, otherwise the clearance."""
    x0, x1, y0, y1 = box
    dx = max(x0 - p[0], 0.0, p[0] - x1)
    dy = max(y0 - p[1], 0.0, p[1] - y1)
    return float(np.hypot(dx, dy))


def clearance(label, curves):
    """Smallest clearance between the label box and any sampled curve point."""
    box = bbox(label)
    best = 9.9
    for c in curves:
        pts = [np.array(c.point_from_proportion(t))[:2]
               for t in np.linspace(0, 1, 400)]
        best = min(best, min(dist_to_box(p, box) for p in pts))
    return best


def scene_curves(P, Q, R, S, sc, spread_p, spread_r):
    return {
        "arc_p": M.locating_arc(P, S, 4.0 * sc, spread_p, M.CHALK_PINK),
        "arc_r": M.locating_arc(R, S, 5.5 * sc, spread_r, M.CHALK_GREEN),
        "PS": Line(P, S), "RS": Line(R, S), "PQ": Line(P, Q),
        "QR": Line(Q, R), "SR_edge": Line(S, R),
    }


print("=== scene 6 (default frame) ===")
P, Q, R, S = M.example_frame()
curves = scene_curves(P, Q, R, S, 0.52, 30, 40)
for buff in (0.10, 0.16, 0.22, 0.28):
    for side in ("UL", "UR", "DL"):
        lab = M.board_text("S", 18, M.CHALK_WHITE, "BOLD").next_to(
            S, {"UL": UL, "UR": UR, "DL": DL}[side], buff=buff)
        cl = {nm: round(clearance(lab, [c]), 3) for nm, c in curves.items()}
        worst = min(cl.values())
        print(f"  buff={buff:.2f} {side}: clearances {cl}  worst={worst:.3f}"
              f"  {'CLEAR' if worst > 0.03 else 'TOUCHES'}")

print("=== scene 10 (origin -3.6,-1.3 scale 0.34) ===")
P, Q, R, S = M.example_frame(origin=np.array([0.5 - 4.1, -1.3, 0]), scale=0.34)
curves = scene_curves(P, Q, R, S, 0.34, 30, 25)
for buff in (0.10, 0.16, 0.22, 0.28):
    for side in ("UL", "UR", "DL"):
        lab = M.board_text("S", 16, M.CHALK_WHITE, "BOLD").next_to(
            S, {"UL": UL, "UR": UR, "DL": DL}[side], buff=buff)
        cl = {nm: round(clearance(lab, [c]), 3) for nm, c in curves.items()}
        worst = min(cl.values())
        print(f"  buff={buff:.2f} {side}: clearances {cl}  worst={worst:.3f}"
              f"  {'CLEAR' if worst > 0.03 else 'TOUCHES'}")

print("=== scene 7 / 3 / 2 (no arcs) -- UL is safe? ===")
P, Q, R, S = M.example_frame()
for sc, tag in ((0.52, "scene3/7")):
    lab = M.board_text("S", 18, M.CHALK_WHITE, "BOLD").next_to(S, UL, buff=0.10)
    cl = {"PS": round(clearance(lab, [Line(P, S)]), 3),
          "RS": round(clearance(lab, [Line(R, S)]), 3),
          "SR_edge": round(clearance(lab, [Line(S, R)]), 3)}
    print(f"  {tag} UL: {cl}")

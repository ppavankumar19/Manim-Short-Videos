import numpy as np
from manim import *
import construct_quadrilateral_4sides_1angle as M

def bbox(m):
    return (float(m.get_corner(DL)[0]), float(m.get_corner(UR)[0]),
            float(m.get_corner(DL)[1]), float(m.get_corner(UR)[1]))

def clearance(label, tool):
    x0, x1, y0, y1 = bbox(label)
    best = 9.9
    for part in [m for m in tool.get_family() if len(getattr(m, "points", ()))]:
        for t in np.linspace(0, 1, 120):
            p = part.point_from_proportion(t)
            dx = max(x0 - p[0], 0.0, p[0] - x1)
            dy = max(y0 - p[1], 0.0, p[1] - y1)
            best = min(best, float(np.hypot(dx, dy)))
    return round(best, 3)

def tool_at(centre, target, radius, spread, away, hinge_dir, leg_ratio, sweep_frac):
    C = np.array(centre, float)
    ang = float(np.degrees(np.arctan2(target[1] - C[1], target[0] - C[0])))
    a = ang - spread + 2 * spread * sweep_frac
    tip = C + radius * np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0.0])
    return M.compass_tool(C, tip, away=away, hinge_dir=hinge_dir, leg_ratio=leg_ratio)

P, Q, R, S = M.example_frame()
cen = np.array([P, Q, R, S], dtype=float).mean(axis=0)
print("=== SCENE 5: compass about Q vs the Q vertex label ===")
q_lab = M.vertex_label("Q", Q, "DR")
for lr in (0.55, 0.62, 0.70, 0.78):
    worst = 9.9
    for f in np.linspace(0, 1, 9):
        tool = tool_at(Q, R, 5.2 * M.SCALE, 26, None, (1.0, -0.6, 0.0), lr, f)
        worst = min(worst, clearance(q_lab, tool))
    print(f"  leg_ratio={lr}: worst clearance to Q label = {worst:.3f}")

print("=== SCENE 6: compass about P vs the PS label ===")
rad_p = M.radius_line(P, S, M.CHALK_PINK, "PS = 4 cm")
ps_lab = rad_p[1]
print("  PS label bbox", np.round(bbox(ps_lab), 2))
for lr in (0.55, 0.62, 0.70, 0.78):
    for hd in ((1.0, -0.5, 0.0), (-0.4, -1.0, 0.0), (1.0, -1.0, 0.0)):
        worst = 9.9
        for f in np.linspace(0, 1, 9):
            tool = tool_at(P, S, 4.0 * M.SCALE, 26, None, hd, lr, f)
            worst = min(worst, clearance(ps_lab, tool))
        print(f"  leg_ratio={lr} hinge={hd}: worst clearance = {worst:.3f}")

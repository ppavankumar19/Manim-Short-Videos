import numpy as np
from manim import *
import construct_quadrilateral_4sides_1diagonal as M
A, B, C, D = M.example_frame()
lab = M.board_text("AC = 5 cm", 17, M.CHALK_CYAN, "BOLD").move_to(C + np.array([-0.72, -0.36, 0]))
x0 = float(lab.get_corner(DL)[0]); x1 = float(lab.get_corner(UR)[0])
y0 = float(lab.get_corner(DL)[1]); y1 = float(lab.get_corner(UR)[1])
print("label box", round(x0,2), round(x1,2), round(y0,2), round(y1,2))
for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
    arc, tool, sweep = M.compass_arc_drawer(A, B, 4.0 * M.SCALE, 24, M.CHALK_CYAN, hinge_dir=(1.0, -1.0, 0.0))
    sweep.set_value(48 * frac)
    worst = (9.9, None)
    for part in [m for m in tool.get_family() if len(getattr(m, "points", ()))]:
        for t in np.linspace(0, 1, 240):
            p = part.point_from_proportion(t)
            dx = max(x0 - p[0], 0.0, p[0] - x1); dy = max(y0 - p[1], 0.0, p[1] - y1)
            d = float(np.hypot(dx, dy))
            if d < worst[0]:
                worst = (d, type(part).__name__, np.round(p[:2], 2))
    print(f" sweep {48*frac:4.0f} deg: min gap {worst[0]:.3f}  part {worst[1]} at {worst[2]}")

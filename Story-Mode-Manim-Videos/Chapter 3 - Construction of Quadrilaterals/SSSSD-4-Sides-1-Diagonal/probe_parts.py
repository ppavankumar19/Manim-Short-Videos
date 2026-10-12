import numpy as np
from manim import *
import construct_quadrilateral_4sides_1diagonal as M
A, B, C, D = M.example_frame()
arc, tool, sweep = M.compass_arc_drawer(A, B, 4.0 * M.SCALE, 24, M.CHALK_CYAN, hinge_dir=(1.0, -1.0, 0.0))
for part in tool.get_family():
    print(type(part).__name__, "centre", np.round(part.get_center()[:2], 2),
          "bbox", np.round(part.get_bounding_box()[[0, 2, 1, 4]], 2) if len(getattr(part, "points", ())) else "-")

"""Which arc/arrow direction bulges UP for the number-line jump arcs?"""
import numpy as np
from manim import ArcBetweenPoints, CurvedArrow, PI

start = np.array([-1.0, 0.0, 0.0])
end = np.array([1.0, 0.0, 0.0])

for name, mob in (
    ("ArcBetweenPoints(-PI/3)", ArcBetweenPoints(start, end, angle=-PI / 3)),
    ("ArcBetweenPoints(+PI/3)", ArcBetweenPoints(start, end, angle=PI / 3)),
    ("CurvedArrow(-PI/3)", CurvedArrow(start, end, angle=-PI / 3)),
    ("CurvedArrow(+PI/3)", CurvedArrow(start, end, angle=PI / 3)),
):
    top = mob.get_top()[1]
    print(f"{name:26s} apex y = {top:+.3f}  -> "
          f"{'UP' if top > 0.05 else 'DOWN / flat'}")

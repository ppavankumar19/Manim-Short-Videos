import importlib, sys
sys.path.insert(0, ".")
from manim import config
config.renderer = "cairo"
config.disable_caching = True
m = importlib.import_module("curves_open_closed_and_regions")
bt = m.board_text
items = [
    ("Understanding Curves & Regions", 27),
    ("Open \u00b7 Closed \u00b7 Interior \u00b7 Exterior \u00b7 Boundary", 18),
    ("OPEN", 13), ("CLOSED", 13), ("NOT SIMPLE", 13),
    ("the ends stay apart", 12), ("the path joins back", 12),
    ("the path crosses itself", 12),
    ("One Pencil, Many Curves", 20),
    ("A curve is drawn without lifting the pencil.", 17),
    ("a wavy path", 13), ("a loop", 13), ("a crossing path", 13),
    ("even a straight line", 13),
    ("YES \u2014 EVEN A STRAIGHT LINE IS A CURVE", 18),
    ("Any figure drawn in one continuous stroke.", 16),
    ("Open or Closed?", 20), ("Question 1: does the path close?", 17),
    ("the two ends stay apart", 14), ("the path comes back and closes", 14),
    ("Simple or Self-Crossing?", 20), ("Question 2: does it cross itself?", 17),
    ("never crosses itself", 14), ("it crosses itself here", 14),
    ("Two Different Questions", 20),
    ("Open or closed?  Simple or not simple?", 17),
    ("ASK BOTH QUESTIONS FOR EVERY CURVE", 18),
    ("Open or closed \u00b7 simple or not simple.", 16),
    ("A Closed Curve Separates the Plane", 20),
    ("Like the boundary wall of a park.", 17),
    ("A CLOSED FIGURE SEPARATES THE PLANE", 18),
    ("Inside \u00b7 On the wall \u00b7 Outside.", 16),
    ("Where Is the Point?", 20), ("Inside, on the edge, or outside?", 17),
    ("INSIDE \u00b7 ON THE EDGE \u00b7 OUTSIDE", 18),
    ("Each point has exactly one place.", 16),
    ("What Is a Region?", 20),
    ("The interior and the boundary together.", 17),
    ("REGION = INTERIOR + BOUNDARY", 18),
    ("the whole closed part", 13),
    ("From a Closed Curve to a Polygon", 20),
    ("Make the boundary from straight line segments.", 17),
    ("closed curve", 14), ("polygon", 14),
    ("A POLYGON IS A SIMPLE CLOSED FIGURE OF LINE SEGMENTS", 17),
    ("Triangles and quadrilaterals come next.", 16),
    ("YOUR TURN", 26),
    ("Classify each diagram, then locate P, Q and R.", 16),
    ("open or closed?", 13), ("simple or not simple?", 13),
    ("classify P, Q and R", 13),
    ("A \u00b7 INTERIOR", 15), ("B \u00b7 BOUNDARY", 15), ("C \u00b7 EXTERIOR", 15),
    ("Draw \u00b7 Classify \u00b7 Locate", 22),
    ("Thank You for Watching!", 30),
    ("See you in the next lesson :)", 22),
]
for s, size in items:
    t = bt(s, size, m.CHALK_WHITE, "BOLD")
    print(f"{s[:48]!r:52s} size={size:2d} w={t.width:5.2f} h={t.height:5.2f}")

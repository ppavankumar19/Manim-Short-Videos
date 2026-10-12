"""Badge clearance for every heading, sub-heading and banner in this video.

The corner badges are real mobjects built by the scene's own `_corner_badge`,
so this measures exact geometry: each heading's bounding box against each
badge's bounding box, and the clear air between them on both axes.  (The
shipped NEAR-BADGE check only looks at the badge's corner strip with its own
loose threshold, which is why a heading can pass it while the user can see the
overlap.)

    python audit_badge_clearance.py
"""
from __future__ import annotations

import sys

from manim import config

config.renderer = "cairo"
config.disable_caching = True

sys.path.insert(0, ".")
from triangles_vertices_sides_and_triangular_region import (  # noqa: E402
    BANNER_Y, BOARD_CX, BOARD_TOP, BRAND_WHITE, CHALK_WHITE, ROW_Y, STRIP_Y,
    SUB_Y, TrianglesVerticesSidesAndTriangularRegionStory, board_text,
)

CLEAR = 0.30          # the clearance the user asked for

scene = TrianglesVerticesSidesAndTriangularRegionStory()
badge_r = scene._corner_badge("Mathematics", corner="right",
                              y=BOARD_TOP - 0.16, font_size=12, scale=16 / 12)
badge_l = scene._corner_badge("dhimantAI", corner="left",
                              y=BOARD_TOP - 0.16, font_size=12, scale=16 / 12,
                              text_color=BRAND_WHITE)

BADGES = {"right": badge_r, "left": badge_l}
for name, b in BADGES.items():
    print(f"badge {name:5s} x[{b.get_left()[0]:+.3f}..{b.get_right()[0]:+.3f}] "
          f"y[{b.get_bottom()[1]:+.3f}..{b.get_top()[1]:+.3f}]")

ITEMS = (
    ("title", "Triangles Uncovered", 26, 1.98),
    ("title.sub", "Vertices · Sides · Angles · Triangular Region", 17, 1.42),
    ("s1.head", "How Many Sticks Close a Figure?", 20, ROW_Y),
    ("s2.head", "What Is a Triangle?", 20, ROW_Y),
    ("s3.head", "The Three Sides", 20, ROW_Y),
    ("s4.head", "The Three Vertices", 20, ROW_Y),
    ("s5.head", "Three Vertices, Three Angles", 20, ROW_Y),
    ("s6.head", "Naming the Triangle", 20, ROW_Y),
    ("s7.head", "Interior, Boundary, Exterior", 20, ROW_Y),
    ("s8.head", "The Triangular Region", 20, ROW_Y),
    ("s9.head", "YOUR TURN", 26, 2.78),
    ("s9.sub", "Four quick checks.", 16, 2.20),
    ("s10.head", "Build · Identify · Locate", 22, ROW_Y),
    # sub-headings (same line in every scene)
    ("s1.sub", "One stick, two sticks, three sticks.", 17, SUB_Y),
    ("s2.sub", "Simple · closed · three line segments.", 17, SUB_Y),
    ("s3.sub", "The three line segments of the figure.", 17, SUB_Y),
    ("s4.sub", "The points where the sides meet.", 17, SUB_Y),
    ("s5.sub", "Every vertex gives an angle.", 17, SUB_Y),
    ("s6.sub", "We use its three vertices.", 17, SUB_Y),
    ("s7.sub", "A triangle divides the plane into three parts.", 17, SUB_Y),
    ("s8.sub", "The interior together with the boundary.", 17, SUB_Y),
    # banners / strips (bottom rows, measured for completeness)
    ("s1.banner", "3 IS THE LEAST NUMBER OF SEGMENTS", 18, BANNER_Y),
    ("s2.banner", "3 LINE SEGMENTS = TRIANGLE", 18, BANNER_Y),
    ("s3.strip", "The three sides together form the boundary.", 16, STRIP_Y),
    ("s7.strip", "Three parts of the plane: interior, boundary, exterior.",
     16, STRIP_Y),
    ("s8.strip", "The region is the interior plus the boundary.", 16, STRIP_Y),
)

print(f"\n{'item':12s} {'width':>6s} {'x span':>17s} {'y span':>15s} "
      f"{'gap L':>7s} {'gap R':>7s}  verdict")
for tag, text, size, y in ITEMS:
    t = board_text(text, size, CHALK_WHITE, "BOLD")
    t.move_to([BOARD_CX, y, 0.0])
    tx0, tx1 = t.get_left()[0], t.get_right()[0]
    ty0, ty1 = t.get_bottom()[1], t.get_top()[1]

    def gap(b):
        gx = max(tx0 - b.get_right()[0], b.get_left()[0] - tx1)
        gy = max(ty0 - b.get_top()[1], b.get_bottom()[1] - ty1)
        return max(gx, gy)

    gl, gr = gap(badge_l), gap(badge_r)
    worst = min(gl, gr)
    verdict = "ok" if worst >= CLEAR else "TOO CLOSE"
    print(f"{tag:12s} {tx1 - tx0:6.2f} [{tx0:+.2f}..{tx1:+.2f}] "
          f"[{ty0:+.2f}..{ty1:+.2f}] {gl:7.2f} {gr:7.2f}  {verdict}")

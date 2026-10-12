"""Badge clearance for every heading, sub-heading and banner in this video.

The corner badges are real mobjects built by the scene's own `_corner_badge`,
so this measures exact geometry: each heading's bounding box against each
badge's bounding box, and the clear air between them on both axes.  (The
shipped NEAR-BADGE check only looks at the badge's corner strip with its own
loose threshold, which is why the s1 heading passed it while the user could see
the overlap.)

    python _badge_check_tmp.py
"""
from __future__ import annotations

import sys

from manim import config

config.renderer = "cairo"
config.disable_caching = True

sys.path.insert(0, ".")
from percentage_applications_and_estimation import (  # noqa: E402
    BANNER_Y, BOARD_CX, BOARD_TOP, BRAND_WHITE, CHALK_WHITE, CHALK_YELLOW,
    ROW_Y, STRIP_Y, SUB_Y, PercentageApplicationsAndEstimationStory,
    board_text,
)

CLEAR = 0.30          # the clearance the user asked for

scene = PercentageApplicationsAndEstimationStory()
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
    ("title", "Who Did Better?", 26, 1.98),
    ("title.sub", "225 of 300, or 200 of 250?", 17, 1.42),
    ("s1.head", "One Scale for Every Total", 20, ROW_Y),
    ("s2.head", "A 35% Increase Attaches a Block", 20, ROW_Y),
    ("s3.head", "Applying the 35% Increase", 20, ROW_Y),
    ("s4.head", "A 10% Decrease on a Price Tag", 20, ROW_Y),
    ("s5.head", "The Mental Percentage Toolkit", 20, ROW_Y),
    ("s6.head", "Estimating 15% on a Bill", 20, ROW_Y),
    ("s7.head", "Exact Lane and Estimate Lane", 20, ROW_Y),
    ("s8.head", "The Four-Move Decision Map", 20, ROW_Y),
    ("s9.head", "YOUR TURN", 26, 2.78),
    ("s9.sub", "Four quick checks.", 16, 2.2),
    ("s10.head", "Compare, Change, Estimate, Check", 18, ROW_Y),
    ("s1.sub", "Part over whole, times one hundred.", 17, SUB_Y),
    ("s2.sub", "The increase is measured from the original.", 17, SUB_Y),
    ("s3.sub", "Add the increase to the original figure.", 17, SUB_Y),
    ("s4.sub", "A decrease is taken away from one hundred.", 17, SUB_Y),
    ("s5.sub", "Ten percent first, then half, then add.", 17, SUB_Y),
    ("s6.sub", "Round the bill, then build fifteen percent.", 17, SUB_Y),
    ("s7.sub", "An estimate is a check, not exact arithmetic.", 17, SUB_Y),
    ("s8.sub", "Convert, change, estimate, check.", 17, SUB_Y),
    ("s10.sub", "Four rules to carry away.", 17, SUB_Y),
    ("title.banner", "ONE SCALE: OUT OF 100", 18, BANNER_Y),
    ("s1.banner", "GROUP B DID BETTER: 80% > 75%", 18, BANNER_Y),
    ("s2.banner", "A 35% INCREASE GIVES 135% OF THE ORIGINAL", 16, BANNER_Y),
    ("s3.banner", "NEW SALES = Rs 1,33,245", 18, BANNER_Y),
    ("s4.banner", "10% OFF -> YOU PAY 90%", 18, BANNER_Y),
    ("s5.banner", "5% IS HALF OF 10%, NOT OF 20%", 16, BANNER_Y),
    ("s6.banner", "ROUND THE BILL, THEN PAY ABOUT Rs 410", 16, BANNER_Y),
    ("s7.banner", "EXACT 406.13, ESTIMATE ABOUT 410", 16, BANNER_Y),
    ("s8.banner", "FOUR MOVES: CONVERT, INCREASE, DECREASE, ESTIMATE", 16, BANNER_Y),
    ("s5.strip", "Build hard percentages out of ten percent.", 16, STRIP_Y),
    ("s10.strip", "Compare, change, estimate, then check.", 16, STRIP_Y),
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

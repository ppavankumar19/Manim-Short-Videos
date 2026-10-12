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
from simple_vs_compound_interest_formula import (  # noqa: E402
    BANNER_Y, BOARD_CX, BOARD_TOP, BRAND_WHITE, CHALK_WHITE, CHALK_YELLOW,
    ROW_Y, STRIP_Y, SUB_Y, SimpleVsCompoundInterestFormulaStory,
    board_text,
)

CLEAR = 0.30          # the clearance the user asked for

scene = SimpleVsCompoundInterestFormulaStory()
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
    ("title", "Same Money, Two Methods", 24, 1.95),
    ("title.sub", "Rs 100 for 2 years at 10%: Rs 120 or Rs 121?", 17, 1.42),
    ("s1.head", "Ramesh's Method: Simple Interest", 20, ROW_Y),
    ("s2.head", "Sreenu's Method: Compound Interest", 20, ROW_Y),
    ("s3.head", "The One-Period Growth Factor", 20, ROW_Y),
    ("s4.head", "The Same Factor Multiplies Again", 20, ROW_Y),
    ("s5.head", "One Factor for Every Year", 20, ROW_Y),
    ("s6.head", "The Formula Gives the Amount", 20, ROW_Y),
    ("s7.head", "Apply It: Rs 5,000 at 8% for 2 Years", 20, ROW_Y),
    ("s8.head", "Simple and Compound Side by Side", 20, ROW_Y),
    ("s9.head", "YOUR TURN", 26, 2.78),
    ("s9.sub", "Four quick checks.", 16, 2.2),
    ("s10.head", "Simple · Compound · Growth", 20, ROW_Y),
    ("s1.sub", "The interest stays on the original principal.", 17, SUB_Y),
    ("s2.sub", "Each new amount becomes the next principal.", 17, SUB_Y),
    ("s3.sub", "Amount equals principal plus the interest on it.", 17, SUB_Y),
    ("s4.sub", "The year-one amount is the year-two principal.", 17, SUB_Y),
    ("s5.sub", "Year one, year two, up to year n.", 17, SUB_Y),
    ("s6.sub", "The amount is principal plus interest.", 17, SUB_Y),
    ("s7.sub", "Principal Rs 5,000, rate 8%, two years.", 17, SUB_Y),
    ("s8.sub", "One base stays locked, the other grows.", 17, SUB_Y),
    ("s1.banner", "THE SAME INTEREST EVERY YEAR", 18, BANNER_Y),
    ("s2.banner", "THE INTEREST EARNED ALSO EARNS INTEREST", 18, BANNER_Y),
    ("s4.banner", "TWO YEARS, TWO FACTORS, ONE POWER", 18, BANNER_Y),
    ("s8.banner", "AFTER ONE YEAR SI AND CI ARE THE SAME", 18, BANNER_Y),
    ("s1.strip", "Simple interest always uses the original principal.", 16, STRIP_Y),
    ("s6.strip", "The formula gives the amount, not the interest.", 16, STRIP_Y),
    ("s8.strip", "The base changes only from the second year on.", 16, STRIP_Y),
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

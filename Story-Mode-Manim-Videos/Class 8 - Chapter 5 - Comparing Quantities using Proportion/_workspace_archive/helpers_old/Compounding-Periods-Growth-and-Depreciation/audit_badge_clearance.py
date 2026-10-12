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
from compounding_periods_half_yearly_quarterly_depreciation import (  # noqa: E402
    BANNER_Y, BOARD_CX, BOARD_TOP, BRAND_WHITE, CHALK_WHITE, CHALK_YELLOW,
    ROW_Y, STRIP_Y, SUB_Y, CompoundingPeriodsHalfYearlyQuarterlyDepreciationStory,
    board_text,
)

CLEAR = 0.30          # the clearance the user asked for

scene = CompoundingPeriodsHalfYearlyQuarterlyDepreciationStory()
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
    ("title", "Compounding Periods, Growth & Depreciation", 26, 2.06),
    ("title.sub", "Half-Yearly · Quarterly · Growth · Depreciation", 17, 1.46),
    ("s1.head", "The Conversion Period", 20, ROW_Y),
    ("s2.head", "Half-Yearly: Two Changes at Once", 20, ROW_Y),
    ("s3.head", "Half-Yearly: Rs 1,000 at 10%", 20, ROW_Y),
    ("s4.head", "Quarterly: R/4 and 4n", 20, ROW_Y),
    ("s5.head", "Population Growth Is Compound", 20, ROW_Y),
    ("s6.head", "Depreciation: Keeping (100 - R)%", 20, ROW_Y),
    ("s7.head", "One Structure, Three Uses", 20, ROW_Y),
    ("s8.head", "Five Steps to Apply It", 20, ROW_Y),
    ("s9.head", "YOUR TURN", 26, 2.78),
    ("s9.sub", "Three questions and a quick check.", 16, 2.2),
    ("s10.head", "The Whole Lesson on One Board", 20, ROW_Y),
    ("s11.head", "Period · Rate · Factor · Repeat", 20, ROW_Y),
    ("s1.sub", "How often is the interest added?", 17, SUB_Y),
    ("s2.sub", "Halve the rate, double the periods.", 17, SUB_Y),
    ("s3.sub", "Rate 5% for each half-year, 2 periods.", 17, SUB_Y),
    ("s4.sub", "A year has four quarters.", 17, SUB_Y),
    ("s5.sub", "The new total becomes the next base.", 17, SUB_Y),
    ("s6.sub", "A reduction in value due to use and age.", 17, SUB_Y),
    ("s7.sub", "Growth multiplies up, depreciation down.", 17, SUB_Y),
    ("s8.sub", "Period, rate, factor, repeat.", 17, SUB_Y),
    ("s10.sub", "Period · Rate · Formula · Five Steps", 17, SUB_Y),
    ("s1.banner", "RATE AND PERIODS CHANGE TOGETHER", 18, BANNER_Y),
    ("s2.banner", "RATE AND PERIODS CHANGE TOGETHER", 18, BANNER_Y),
    ("s3.banner", "AMOUNT = Rs 1,102.50", 18, BANNER_Y),
    ("s5.banner", "6250 × (1.08)^2 = 7,290", 18, BANNER_Y),
    ("s6.banner", "25 × 0.9 × 0.9 = 20.25 m", 18, BANNER_Y),
    ("s8.banner", "PERIOD → RATE → FACTOR → REPEAT", 18, BANNER_Y),
    ("s10.banner", "PERIOD · RATE · FORMULA · FIVE STEPS", 18, BANNER_Y),
    ("s11.strip", "Period, rate, factor, repeat.", 16, STRIP_Y),
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

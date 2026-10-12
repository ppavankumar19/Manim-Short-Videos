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
from discounts_marked_price_and_rebate import (  # noqa: E402
    BANNER_Y, BOARD_CX, BOARD_TOP, BRAND_WHITE, CHALK_WHITE, CHALK_YELLOW,
    ROW_Y, STRIP_Y, SUB_Y, DiscountsMarkedPriceAndRebateStory,
    board_text,
)

CLEAR = 0.30          # the clearance the user asked for

scene = DiscountsMarkedPriceAndRebateStory()
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
    ("title", "Discounts, Marked Price & Rebate", 20, ROW_Y),
    ("title.sub", "The tag price is not always the price you pay.", 17, SUB_Y),
    ("s1.head", "The Three Parts of a Price", 20, ROW_Y),
    ("s1.sub", "Marked price, discount, selling price.", 17, SUB_Y),
    ("s2.head", "The Discount Comes First", 20, ROW_Y),
    ("s2.sub", "A book marked Rs 80 at 15% off.", 17, SUB_Y),
    ("s3.head", "Finding the Discount Percent", 20, ROW_Y),
    ("s3.sub", "A cycle marked Rs 3600, sold for Rs 3312.", 17, SUB_Y),
    ("s4.head", "Given the Discount, Find the SP", 20, ROW_Y),
    ("s4.sub", "A fan marked Rs 1600 with 6% off.", 17, SUB_Y),
    ("s5.head", "The Shortcut: What Remains", 20, ROW_Y),
    ("s5.sub", "If 6% is taken off, 94% remains.", 17, SUB_Y),
    ("s6.head", "Which Formula Do I Need?", 20, ROW_Y),
    ("s6.sub", "Look at what the question gives you.", 17, SUB_Y),
    ("s7.head", "Common Mistakes and Their Fixes", 20, ROW_Y),
    ("s7.sub", "Four wrong ideas, four corrections.", 17, SUB_Y),
    ("s8.head", "Does the Answer Make Sense?", 20, ROW_Y),
    ("s8.sub", "Check the selling price against the marked price.", 17, SUB_Y),
    ("s9.head", "YOUR TURN", 26, 2.78),
    ("s9.sub", "Four quick checks.", 16, 2.2),
    ("s10.head", "Marked Price to Selling Price", 22, ROW_Y),
    ("s6.banner", "THE BASE IS ALWAYS THE MARKED PRICE", 18, BANNER_Y),
    ("s1.strip", "The discount is always calculated from the marked price.", 16, STRIP_Y),
    ("s2.strip", "The discount is always calculated on the marked price.", 16, STRIP_Y),
    ("s3.strip", "Always divide by the marked price, and never by the selling price.", 16, STRIP_Y),
    ("s4.strip", "The amount is in rupees; the rate is a percentage of the marked price.", 16, STRIP_Y),
    ("s5.strip", "Both routes land on the same selling price, Rs 1504.", 16, STRIP_Y),
    ("s7.strip", "Check the base, the sign, and the units, every time.", 16, STRIP_Y),
    ("s8.strip", "Check SP < MP, and check that d plus (100 - d) makes 100.", 16, STRIP_Y),
    ("s9a.strip", "The base is the marked price, and SP is always smaller than MP.", 16, STRIP_Y),
    ("s10.strip", "Keep the marked price visible, subtract the discount, check the answer.", 16, STRIP_Y),
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

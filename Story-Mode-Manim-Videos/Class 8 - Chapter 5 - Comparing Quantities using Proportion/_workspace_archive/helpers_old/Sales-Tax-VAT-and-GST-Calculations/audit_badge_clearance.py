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
from sales_tax_vat_and_gst_calculations import (  # noqa: E402
    BANNER_Y, BOARD_CX, BOARD_TOP, BRAND_WHITE, CHALK_WHITE, CHALK_YELLOW,
    ROW_Y, STRIP_Y, SUB_Y, SalesTaxVatAndGstCalculationsStory,
    board_text,
)

CLEAR = 0.30          # the clearance the user asked for

scene = SalesTaxVatAndGstCalculationsStory()
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
    ("title", "The Tag Is Not the Bill", 26, 2.06),
    ("title.sub", "A pair of shoes, and a six percent tax.", 17, 1.44),
    ("s1.head", "A Tax Is a Percentage Increase", 20, ROW_Y),
    ("s2.head", "Sales Tax on a Pair of Shoes", 20, ROW_Y),
    ("s3.head", "Reading a VAT-Inclusive Bill", 20, ROW_Y),
    ("s4.head", "GST Uses the Same Structure", 20, ROW_Y),
    ("s5.head", "Finding the Price Before Tax", 20, ROW_Y),
    ("s6.head", "CGST and SGST in the Textbook", 20, ROW_Y),
    ("s7.head", "Forward or Backward?", 20, ROW_Y),
    ("s8.head", "The Classic Tax Error", 20, ROW_Y),
    ("s9.head", "YOUR TURN", 26, 2.78),
    ("s9.sub", "Four quick checks.", 16, 2.2),
    ("s10.head", "Base, Tax Rate, Bill", 22, ROW_Y),
    ("s1.sub", "The base price is the one hundred percent.", 17, SUB_Y),
    ("s2.sub", "Base Rs 450 and sales tax 6%.", 17, SUB_Y),
    ("s3.sub", "VAT is the same percentage idea.", 17, SUB_Y),
    ("s4.sub", "Base Rs 1,000 and GST at 5%.", 17, SUB_Y),
    ("s5.sub", "The bill is 118%, not 100%.", 17, SUB_Y),
    ("s6.sub", "A worked example, not a universal rule.", 17, SUB_Y),
    ("s7.sub", "What you were given decides the lane.", 17, SUB_Y),
    ("s8.sub", "Apply the rate to the base, never the bill.", 17, SUB_Y),
    ("s10.sub", "Four formulas to carry away.", 17, SUB_Y),
    ("title.banner", "BASE + TAX = THE FINAL BILL", 18, BANNER_Y),
    ("s1.banner", "A TAX IS A PERCENTAGE INCREASE", 18, BANNER_Y),
    ("s2.banner", "TAX Rs 27, FINAL BILL Rs 477", 18, BANNER_Y),
    ("s3.banner", "BASE Rs 354.45 + VAT Rs 17.72 = Rs 372.18", 16, BANNER_Y),
    ("s4.banner", "BASE + 5% GST = Rs 1,050", 18, BANNER_Y),
    ("s5.banner", "BASE = Rs 2,000, TAX = Rs 360", 18, BANNER_Y),
    ("s6.banner", "CGST Rs 180 + SGST Rs 180 = Rs 360", 17, BANNER_Y),
    ("s7.banner", "TAX ADDS, DISCOUNT REMOVES", 18, BANNER_Y),
    ("s8.banner", "NEVER APPLY THE RATE TO THE BILL", 18, BANNER_Y),
    ("title.strip", "The price on the tag is not always the bill you pay.", 16, STRIP_Y),
    ("s8.strip", "The rate is charged on the base, never on the total.", 15, STRIP_Y),
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

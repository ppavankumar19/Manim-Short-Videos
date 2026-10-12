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
from profit_loss_overhead_expenses_and_transactions import (  # noqa: E402
    BANNER_Y, BOARD_CX, BOARD_TOP, BRAND_WHITE, CHALK_WHITE, CHALK_YELLOW,
    ROW_Y, STRIP_Y, SUB_Y, ProfitLossOverheadExpensesAndTransactionsStory,
    board_text,
)

CLEAR = 0.30          # the clearance the user asked for

scene = ProfitLossOverheadExpensesAndTransactionsStory()
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
    ("title", "The Real Cost of a Purchase", 24, ROW_Y),
    ("title.sub", "A second-hand refrigerator.", 16, SUB_Y),
    ("s1.head", "Profit, Loss, or Neither?", 20, ROW_Y),
    ("s2.head", "The Percentage Is Taken on CP", 20, ROW_Y),
    ("s3.head", "The Refrigerator Ledger", 20, ROW_Y),
    ("s4.head", "Overheads Can Bring a Loss", 20, ROW_Y),
    ("s5.head", "Two Tables, Twenty Percent Each", 20, ROW_Y),
    ("s6.head", "The Whole Transaction", 20, ROW_Y),
    ("s7.head", "The Decision Process", 20, ROW_Y),
    ("s8.head", "Spoiled Stock Still Costs", 20, ROW_Y),
    ("s9.head", "YOUR TURN", 26, 2.78),
    ("s9.sub", "Two problems.", 16, 2.2),
    ("s10.head", "Purchase · Overheads · Percentage", 22, ROW_Y),
    ("s1.sub", "Ask which one is bigger before subtracting.", 17, SUB_Y),
    ("s2.sub", "Measured against the cost price.", 17, SUB_Y),
    ("s3.sub", "Add every expense to the purchase price.", 16, SUB_Y),
    ("s4.sub", "A flat bought and then repaired.", 16, SUB_Y),
    ("s5.sub", "Do a gain and a loss cancel?", 17, SUB_Y),
    ("s6.sub", "Add the two costs and the two selling prices.", 16, SUB_Y),
    ("s7.sub", "Five steps, every time.", 17, SUB_Y),
    ("s8.sub", "Overheads count even for what is not sold.", 16, SUB_Y),
    ("s10.sub", "The purchase price alone is never the cost.", 16, SUB_Y),
    ("s1.strip", "Always compare before you subtract.", 16, STRIP_Y),
    ("s3.strip", "The purchase price plus the overheads is the real cost.", 15, STRIP_Y),
    ("s6.strip", "Plus twenty and minus twenty did not give zero.", 16, STRIP_Y),
    ("s9.strip", "The bases were different every time.", 16, STRIP_Y),
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

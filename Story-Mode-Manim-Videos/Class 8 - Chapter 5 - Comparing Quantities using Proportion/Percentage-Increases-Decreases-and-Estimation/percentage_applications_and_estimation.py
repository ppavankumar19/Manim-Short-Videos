"""
Percentage Increases, Decreases & Quick Estimation Rules on Bills
Story-mode chalkboard lesson (Class 8 Maths, Chapter 5: Comparing Quantities
using Proportion).

LLM KEY / FUNCTION NAME: percentage_applications_and_estimation

Layout re-done for legibility: big chalk type inside the green board, and
drawn diagrams -- raffle tickets, two 10 x 10 percent squares, a bar model
that gains a 35% block, a hanging price tag, a till receipt with a number line
that snaps 477.80 to 480, and lane cards for exact versus estimated work.

Title + 10 scenes:
  0. 225 of 300 against 200 of 250 -- who did better?
  1. One scale: 3/4 = 75% and 4/5 = 80%; percentage = part / whole x 100.
  2. A 35% increase: the 100% bar gains a 35% block -> 135%.
  3. Sales Rs 98,700 up 35%: Rs 34,545 more, Rs 1,33,245 in all.
  4. A Rs 550 tag with 10% off pays Rs 495; increase 100+p, decrease 100-p.
  5. Mental toolkit: 10%, 5%, 15%, 20% built from one tenth.
  6. Estimating a Rs 477.80 bill with 15% off: about Rs 410.
  7. Exact versus estimate lanes.
  8. The decision map: convert, increase, decrease, estimate.
  9. Your turn, the THINK clock, the answers.
 10. Recap and thank-you.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_CH5 = next(p for p in _HERE.parents if (p / "ch5_kit.py").exists())
if str(_CH5) not in sys.path:
    sys.path.insert(0, str(_CH5))

from ch5_kit import *  # noqa: F401,F403,E402
from ch5_art import *  # noqa: F401,F403,E402
from ch5_widgets import *  # noqa: F401,F403,E402

INTRO_NARRATION = (
    "Percentage increases, decreases and quick estimation. <bookmark mark='b0'/> Rules for everyday bills."
)
NARRATION = {
    "title": (
        "Suppose two school groups are selling tickets for the annual function. "
        "<bookmark mark='b0'/>Group A sold 225 tickets out of 300. <bookmark "
        "mark='b1'/>Group B sold 200 tickets out of 250. <bookmark mark='b2'/>"
        "The two totals are different, so the numbers 225 and 200 cannot be "
        "compared directly. <bookmark mark='b3'/>Who actually did better? "
        "<bookmark mark='b4'/>A percentage puts different totals onto one "
        "common scale, and that scale is always out of one hundred."
    ),
    "s1": (
        "Now let us convert both groups to one common scale. <bookmark "
        "mark='b0'/>Both 225 out of 300 and 200 out of 250 can be written as "
        "fractions. 225 out of 300 is 3 over 4, which is 75 out of 100, so that "
        "is 75 percent. <bookmark mark='b1'/>200 out of 250 is 4 over 5, which "
        "is 80 out of 100, so that is 80 percent. <bookmark mark='b2'/>So group "
        "B is closer to the target. <bookmark mark='b3'/>The rule is: "
        "percentage equals part divided by whole, multiplied by one hundred. "
        "<bookmark mark='b4'/>And always name the whole, because the percentage "
        "is measured from that reference."
    ),
    "s2": (
        "Now think about a change. <bookmark mark='b0'/>Suppose a value grows "
        "by 35 percent. Start with the original value drawn as a full bar of "
        "one hundred percent. <bookmark mark='b1'/>A 35 percent increase "
        "attaches one more block to that bar. <bookmark mark='b2'/>The original "
        "hundred percent and the new thirty five percent together make one "
        "hundred and thirty five percent. <bookmark mark='b3'/>So a 35 percent "
        "increase means the new value is 135 percent of the original. <bookmark "
        "mark='b4'/>The increase is always measured from the original, never "
        "from the new value."
    ),
    "s3": (
        "Let us apply that to money. <bookmark mark='b0'/>Last month the sales "
        "were Rs 98,700. <bookmark mark='b1'/>This month they are up by 35 "
        "percent. <bookmark mark='b2'/>First find the increase: 35 over 100 "
        "times 98,700 is Rs 34,545. <bookmark mark='b3'/>Then add it to the "
        "original: 98,700 plus 34,545 gives Rs 1,33,245. <bookmark mark='b4'/>"
        "Here is the shortcut: 135 percent of 98,700 is the same Rs 1,33,245, "
        "because the new value is 135 percent of the old one."
    ),
    "s4": (
        "Now the other direction. <bookmark mark='b0'/>A price tag shows "
        "Rs 550, and the shop offers 10 percent off. <bookmark mark='b1'/>Ten "
        "percent of 550 is Rs 55. <bookmark mark='b2'/>Take it away: 550 minus "
        "55 is Rs 495, and that is what you pay. <bookmark mark='b3'/>Now "
        "compare the two changes on one panel. An increase of p percent gives "
        "100 percent plus p percent. <bookmark mark='b4'/>A decrease of p "
        "percent gives 100 percent minus p percent, so 10 percent off leaves 90 "
        "percent."
    ),
    "s5": (
        "Here is the mental toolkit. <bookmark mark='b0'/>Ten percent is one "
        "tenth, so move the decimal point one place. <bookmark mark='b1'/>Five "
        "percent is half of ten percent. <bookmark mark='b2'/>Fifteen percent "
        "is ten percent plus five percent, and twenty percent is simply two "
        "tens. <bookmark mark='b3'/>A common mistake is to say that five percent "
        "is half of twenty percent; the cross shows that this is wrong. "
        "<bookmark mark='b4'/>Now use 480: ten percent is 48, five percent is "
        "24, so fifteen percent is 72. Build hard percentages out of ten "
        "percent."
    ),
    "s6": (
        "Now use that on a bill. <bookmark mark='b0'/>The bill is Rs 477.80, "
        "which is awkward, so round it to Rs 480. <bookmark mark='b1'/>Ten "
        "percent of 480 is 48. <bookmark mark='b2'/>Five percent is half of "
        "that, so 24, and fifteen percent is 48 plus 24, that is 72. <bookmark "
        "mark='b3'/>Subtract that from the rounded bill: 480 minus 72 is 408. "
        "<bookmark mark='b4'/>So you pay about Rs 410, and the approximation "
        "sign stays on the board, because this is an estimate."
    ),
    "s7": (
        "Let us put the two lanes side by side. <bookmark mark='b0'/>The exact "
        "lane works with the real bill: fifteen percent of 477.80 is Rs 71.67, "
        "and 477.80 minus 71.67 is 406.13. <bookmark mark='b1'/>The mental lane "
        "rounded the bill to 480 and used 72, which gave about 408, or about "
        "410. <bookmark mark='b2'/>The two answers are close, so the estimate "
        "is sensible. <bookmark mark='b3'/>Remember: an estimate is a "
        "reasonableness check, not exact arithmetic. <bookmark mark='b4'/>The "
        "exact lane is only there to show that the quick answer is believable."
    ),
    "s8": (
        "So here is the decision map. <bookmark mark='b0'/>To convert, divide "
        "the part by the whole and multiply by one hundred. <bookmark "
        "mark='b1'/>To handle an increase, add the percentage to one hundred. "
        "<bookmark mark='b2'/>To handle a decrease, subtract it from one "
        "hundred. <bookmark mark='b3'/>To estimate, round the number first, and "
        "then build the percentage from ten percent. <bookmark mark='b4'/>Four "
        "moves: convert, change, estimate, and check."
    ),
    "s9q": (
        "Your turn. Four quick checks. <bookmark mark='b0'/>A: convert 18 out "
        "of 24 into a percentage. <bookmark mark='b1'/>B: find the price of an "
        "item marked Rs 800 with 10 percent off. <bookmark mark='b2'/>C: "
        "estimate 20 percent of Rs 357.30 by first rounding it to 360. "
        "<bookmark mark='b3'/>D: increase Rs 900 by 35 percent. Now pause the "
        "video, work all four out on paper, and then we will check every "
        "answer."
    ),
    "s9a": (
        "Let us check every answer. <bookmark mark='b0'/>A: 18 out of 24 is "
        "three quarters, so it is 75 percent. <bookmark mark='b1'/>B: ten "
        "percent of 800 is 80, so 800 minus 80 is Rs 720. <bookmark "
        "mark='b2'/>C: twenty percent of 360 is two tens of 36, which is 36 "
        "plus 36, so it is about Rs 72. <bookmark mark='b3'/>D: 135 percent of "
        "900 is Rs 1,215, because 900 plus 315 gives 1,215. Every answer used "
        "the whole as its base."
    ),
    "s10": (
        "Let us put it together. <bookmark mark='b0'/>One: compare, because a "
        "percentage is always out of one hundred. <bookmark mark='b1'/>Two: "
        "change, where an increase adds to one hundred percent and a decrease "
        "subtracts from it. <bookmark mark='b2'/>Three: estimate, by rounding "
        "first and then building the percentage from ten percent. <bookmark "
        "mark='b3'/>Four: check, because an estimate is a reasonableness check "
        "and not exact arithmetic. <bookmark mark='b4'/>Compare, change, "
        "estimate, check. <bookmark mark='b5'/>Thank you for watching, "
        "<bookmark mark='b6'/>and see you in the next lesson."
    ),
}
NARRATION = {"intro": INTRO_NARRATION, **NARRATION}


def fill_cells(grid, n, color):
    for i, c in enumerate(grid):
        c.set_fill(color if i < n else "#25384A", 1)
    return grid


class PercentageApplicationsAndEstimationStory(Ch5Scene):
    NARRATION = NARRATION
    TEXT_SCALE = 0.85     # medium type
    TIGHT_BOXES = True    # every box hugs its text
    STRICT_BOXES = True   # audit: boxes stay on the board with a gap between them
    AVOID_ART = True      # text/cards never sit on the teacher, students or badges
    INTRO_LINES = ('Percentage Changes', '& Estimation')
    INTRO_SUB = 'Increase, Decrease and Quick Bill Estimates'
    BEATS = ("intro", "title", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9",
             "s10")

    # -- 0 -----------------------------------------------------------------
    def beat_title(self):
        with self.narrate("title") as tr:
            self.heading("Percentage Changes & Estimation",
                         "Two groups, two different totals.")
            ca = part_card(ticket(2.2, "#7FE7DC", "GROUP A"), "GROUP A",
                           ["225 tickets sold", "out of 300"], CHALK_CYAN,
                           w=4.7, h=2.35, icon_h=0.95)
            cb = part_card(ticket(2.2, "#FFB347", "GROUP B"), "GROUP B",
                           ["200 tickets sold", "out of 250"], CHALK_AMBER,
                           w=4.7, h=2.35, icon_h=0.95)
            P(ca, CX - 2.55, 0.45)
            P(cb, CX + 2.55, 0.45)
            diff = P(chip("225 and 200: DIFFERENT TOTALS", CHALK_PINK, 26),
                     CX, -1.12)
            who = P(T("WHO DID BETTER?", 44, CHALK_YELLOW), CX, -1.82)
            strip = P(T("A percentage is a scale out of 100.", 26,
                        CHALK_WHITE), CX, -2.40)
            tidy(ca, cb, same=True)  # auto-tidy
            self.cue(tr, "b0", ca, sfx="pop")
            self.cue(tr, "b1", cb)
            self.cue(tr, "b2", diff)
            self.cue(tr, "b3", who, sfx="ding")
            self.cue(tr, "b4", strip, sfx="success")
            self.finish(tr)

    # -- 1: convert ------------------------------------------------------------
    def beat_s1(self):
        with self.narrate("s1") as tr:
            self.heading("Converting to One Scale")
            gA = hundred_grid(0.215, 0.03)
            gB = hundred_grid(0.215, 0.03)
            fill_cells(gA, 75, CHALK_CYAN)
            fill_cells(gB, 80, CHALK_AMBER)
            P(gA, CX - 2.55, 0.12)
            P(gB, CX + 2.55, 0.12)
            fA = P(M(r"\frac{225}{300}=\frac{3}{4}=75\%", 42, CHALK_CYAN),
                   CX - 2.55, 1.62)
            fB = P(M(r"\frac{200}{250}=\frac{4}{5}=80\%", 42, CHALK_AMBER),
                   CX + 2.55, 1.62)
            lA = P(T("GROUP A: 75 of 100", 26, CHALK_CYAN), CX - 2.55, -1.40)
            lB = P(T("GROUP B: 80 of 100", 26, CHALK_AMBER), CX + 2.55, -1.40)
            closer = P(T("B is closer to the target!", 26, CHALK_GREEN),
                       CX + 2.55, -1.40)
            star = Star(n=5, outer_radius=0.36, inner_radius=0.15,
                        fill_color=CHALK_YELLOW, fill_opacity=1,
                        stroke_color="#7A5A08", stroke_width=2.5)
            P(star, CX + 2.55 + 1.55, 1.10)
            rule = P(M(r"\%=\frac{\text{part}}{\text{whole}}\times 100",
                       40, CHALK_YELLOW), CX - 1.6, -2.12)
            note = P(T("name the WHOLE", 24, CHALK_PINK), CX + 3.5, -2.12)
            self.cue(tr, "b0", gA, fA, lA, sfx="pop", scale=0.95)
            self.cue(tr, "b1", gB, fB, lB)
            self.cue(tr, "b2", FadeOut(lB), FadeIn(closer), FadeIn(star),
                     sfx="ding")
            self.cue(tr, "b3", rule, sfx="ding")
            self.cue(tr, "b4", note, Indicate(rule, color=CHALK_PINK,
                                              scale_factor=1.05),
                     sfx="success")
            self.finish(tr)

    # -- 2: 35% increase -----------------------------------------------------
    def beat_s2(self):
        with self.narrate("s2") as tr:
            self.heading("A 35% Increase")
            orig = segbar(5.6, [(1.0, CHALK_CYAN, "ORIGINAL = 100%")], h=0.95,
                          size=28)
            block = segbar(1.96, [(1.0, CHALK_GREEN, "+35%")], h=0.95,
                           size=28)
            total_w = 5.6 + 1.96
            left = CX - total_w / 2
            P(orig, left + 2.8, 0.85)
            P(block, left + 5.6 + 0.98, 0.85)
            b_orig = brace_label(orig, "original value", UP, size=26)
            b_tot = brace_label(VGroup(orig, block), "100% + 35% = 135%",
                                DOWN, size=30, color=CHALK_YELLOW)
            arrow = Arrow(block.get_top() + UP * 0.1, block.get_top() + UP * 0.9,
                          buff=0, color=CHALK_GREEN, stroke_width=7)
            chip_ = P(chip("NEW VALUE = 135% OF THE ORIGINAL", CHALK_YELLOW,
                           28), CX, -1.55)
            strip = P(T("Measured from the original, never the new value.",
                        26, CHALK_WHITE, max_w=8.4), CX - 0.4, -2.30)
            self.cue(tr, "b0", orig, b_orig, sfx="pop")
            self.cue(tr, "b1", FadeIn(block, shift=DOWN * 1.1), FadeIn(arrow),
                     sfx="whoosh", rt=0.8)
            self.cue(tr, "b2", b_tot, sfx="click")
            self.cue(tr, "b3", chip_, sfx="ding")
            self.cue(tr, "b4", strip, sfx="success")
            self.finish(tr)

    # -- 3: money ----------------------------------------------------------------
    def beat_s3(self):
        with self.narrate("s3") as tr:
            self.heading("Applying It to Money")
            last = icon_chip(note_stack(3, 1.4, "#8FD3A0", "Rs 100", 20),
                             VGroup(T("LAST MONTH", 26, CHALK_GREEN),
                                    T("Rs 98,700", 34, CHALK_WHITE)).arrange(
                                 DOWN, buff=0.08), CHALK_GREEN, w=4.7, h=1.4,
                             icon_w=1.4)
            this = icon_chip(sticker("+35%", "UP", r=0.66, size=30),
                             VGroup(T("THIS MONTH", 26, CHALK_PINK),
                                    T("up by 35%", 34, CHALK_WHITE)).arrange(
                                 DOWN, buff=0.08), CHALK_PINK, w=4.7, h=1.4,
                             icon_w=1.3)
            P(last, CX - 2.55, 1.55)
            P(this, CX + 2.55, 1.55)
            r1 = P(calc_row("1", "INCREASE", r"\frac{35}{100}\times98700="
                            r"\text{Rs }34{,}545", CHALK_CYAN, w=9.6, h=0.95,
                            math_size=40), CX, 0.10)
            r2 = P(calc_row("2", "NEW VALUE", r"98700+34545=\text{Rs }1{,}33{,}245",
                            CHALK_YELLOW, w=9.6, h=0.95, math_size=40), CX,
                   -0.85)
            r3 = P(calc_row("3", "SHORTCUT", r"135\%\text{ of }98700=\text{Rs }"
                            r"1{,}33{,}245", CHALK_GREEN, w=9.6, h=0.95,
                            math_size=40), CX, -1.90)
            tk = tick_mark(r3.get_right() + LEFT * 0.4, 0.22)
            tidy(r1, r2, r3, same=True)  # auto-tidy
            self.cue(tr, "b0", last, sfx="pop")
            self.cue(tr, "b1", this)
            self.cue(tr, "b2", r1)
            self.cue(tr, "b3", r2)
            self.cue(tr, "b4", r3, tk, sfx="success")
            self.finish(tr)

    # -- 4: decrease ---------------------------------------------------------------
    def beat_s4(self):
        with self.narrate("s4") as tr:
            self.heading("A 10% Decrease")
            tag = P(shop_tag("Rs 550", w=2.9, h=1.3, size=38), -2.85, 1.35)
            stk = P(sticker("10%", "OFF", r=0.66), -1.55, 0.25)
            r1 = P(calc_row("1", "DISCOUNT", r"\frac{10}{100}\times550="
                            r"\text{Rs }55", CHALK_PINK, w=6.2, h=0.95,
                            math_size=40), 2.30, 1.40)
            r2 = P(calc_row("2", "YOU PAY", r"550-55=\text{Rs }495",
                            CHALK_GREEN, w=6.2, h=0.95, math_size=40), 2.30,
                   0.30)
            inc = tcard("INCREASE p%", [], CHALK_GREEN, w=4.8, h=1.7,
                        head_size=30)
            decr = tcard("DECREASE p%", [], CHALK_PINK, w=4.8, h=1.7,
                         head_size=30)
            mi = M(r"100\%+p\%", 46, CHALK_WHITE)
            md = M(r"100\%-p\%", 46, CHALK_WHITE)
            nd = T("10% off leaves 90%", 26, CHALK_YELLOW)
            ci = VGroup(T("INCREASE p%", 30, CHALK_GREEN), mi).arrange(
                DOWN, buff=0.22)
            cd = VGroup(T("DECREASE p%", 30, CHALK_PINK), md, nd).arrange(
                DOWN, buff=0.14)
            bi, bd = panel(4.8, 1.85, CHALK_GREEN), panel(4.8, 1.85, CHALK_PINK)
            ci.move_to(bi)
            cd.move_to(bd)
            inc = VGroup(bi, ci)
            decr = VGroup(bd, cd)
            P(inc, CX - 2.55, -1.50)
            P(decr, CX + 2.55, -1.50)
            tidy(r1, r2, same=True)  # auto-tidy
            tidy(inc, decr, same=True)  # auto-tidy
            self.cue(tr, "b0", tag, stk, sfx="pop", scale=0.9)
            self.cue(tr, "b1", r1)
            self.cue(tr, "b2", r2)
            self.cue(tr, "b3", inc)
            self.cue(tr, "b4", decr, sfx="ding")
            self.finish(tr)

    # -- 5: toolkit --------------------------------------------------------------------
    def beat_s5(self):
        with self.narrate("s5") as tr:
            self.heading("The Mental Toolkit")

            def kcard(head, line, color):
                return tcard(head, [line], color, w=4.8, h=1.2, head_size=32,
                             body_size=24, pad=0.10, gap=0.06)
            k1 = kcard("10% = one tenth", "move the point one place", CHALK_CYAN)
            k2 = kcard("5% = half of 10%", "halve the ten percent", CHALK_GREEN)
            k3 = kcard("15% = 10% + 5%", "add the two parts", CHALK_AMBER)
            k4 = kcard("20% = 2 x 10%", "two tens", CHALK_PURPLE)
            P(k1, CX - 2.55, 1.55)
            P(k2, CX + 2.55, 1.55)
            P(k3, CX - 2.55, 0.25)
            P(k4, CX + 2.55, 0.25)
            bad = mistake_card("5% = half of 20%", "5% is half of 10%",
                               w=5.6, h=1.25, size=24)
            P(bad, CX, -1.05)
            ex = P(calc_row("E", "480:", r"10\%=48,\ \ 5\%=24,\ \ 15\%=72",
                            CHALK_YELLOW, w=9.6, h=0.85, math_size=38), CX,
                   -2.10)
            tidy(ex)
            self.cue(tr, "b0", k1, sfx="pop")
            self.cue(tr, "b1", k2)
            self.cue(tr, "b2", k3, k4)
            self.cue(tr, "b3", bad, sfx="click")
            self.cue(tr, "b4", ex, sfx="success")
            self.finish(tr)

    # -- 6: bill -------------------------------------------------------------------
    def beat_s6(self):
        with self.narrate("s6") as tr:
            self.heading("Estimating a Bill")
            rc = P(receipt(2.3, 2.9, ("SHOP BILL", "Rs 477.80", "15% OFF"),
                           24, ("#2A2A2A", "#B02030", "#2A2A2A")), -3.15, 0.15)
            nl = NumberLine(x_range=[470, 490, 5], length=5.6,
                            include_numbers=True, font_size=24,
                            color=CHALK_WHITE, decimal_number_config={
                                "num_decimal_places": 0, "color": CHALK_WHITE},
                            stroke_width=3)
            P(nl, 2.35, 1.50)
            dot = Dot(nl.n2p(477.8), color=CHALK_RED, radius=0.14)
            dl = T("477.80", 24, CHALK_RED)
            dl.next_to(dot, UP, buff=0.18)
            dot2 = Dot(nl.n2p(480), color=CHALK_GREEN, radius=0.14)
            dl2 = T("about 480", 26, CHALK_GREEN)
            dl2.next_to(dot2, UP, buff=0.18)
            r1 = P(calc_row("1", "10%", r"10\%\text{ of }480=48", CHALK_CYAN,
                            w=6.2, h=0.8, math_size=38), 2.30, 0.50)
            r2 = P(calc_row("2", "15%", r"5\%=24,\ \ 15\%=48+24=72",
                            CHALK_AMBER, w=6.2, h=0.8, math_size=38), 2.30,
                   -0.38)
            r3 = P(calc_row("3", "PAY", r"480-72=408", CHALK_GREEN, w=6.2,
                            h=0.8, math_size=38), 2.30, -1.26)
            fin_t = VGroup(T("YOU PAY", 32, CHALK_YELLOW),
                           M(r"\approx", 50, CHALK_YELLOW),
                           T("Rs 410", 36, CHALK_WHITE)).arrange(RIGHT, buff=0.3)
            fin_b = panel(fin_t.width + 0.7, 0.85, CHALK_YELLOW)
            fin_t.move_to(fin_b)
            fin = P(VGroup(fin_b, fin_t), CX, -2.18)
            tidy(r1, r2, r3, same=True)  # auto-tidy
            self.cue(tr, "b0", rc, nl, dot, dl, sfx="pop")
            self.cue(tr, "b1", Transform(dot, dot2), FadeOut(dl),
                     FadeIn(dl2), r1, sfx="click", rt=0.9)
            self.cue(tr, "b2", r2)
            self.cue(tr, "b3", r3)
            self.cue(tr, "b4", fin, sfx="success")
            self.finish(tr)

    # -- 7: two lanes ------------------------------------------------------------------
    def beat_s7(self):
        with self.narrate("s7") as tr:
            self.heading("Exact Lane and Estimate Lane")

            def lane(head, rows, color):
                parts = [T(head, 32, color)] + [T(r, 26, CHALK_WHITE)
                                                for r in rows]
                col = VGroup(*parts).arrange(DOWN, buff=0.16)
                box = panel(4.8, 3.05, color)
                col.move_to(box)
                g = VGroup(box, col)
                g.box = box
                return g
            ex = lane("EXACT LANE", ["15% of 477.80", "= Rs 71.67",
                                     "477.80 - 71.67", "= Rs 406.13"],
                      CHALK_CYAN)
            es = lane("ESTIMATE LANE", ["round to 480", "15% of 480 = 72",
                                        "480 - 72 = 408", "about Rs 410"],
                      CHALK_AMBER)
            P(ex, CX - 2.55, 0.62)
            P(es, CX + 2.55, 0.62)
            close = P(chip("406 and 408: CLOSE, SO IT IS SENSIBLE",
                           CHALK_GREEN, 28), CX, -1.45)
            tk = tick_mark(close.get_left() + LEFT * 0.4, 0.22)
            strip = P(T("An estimate is a check, not exact arithmetic.", 26,
                        CHALK_WHITE, max_w=9.6), CX, -2.20)
            self.cue(tr, "b0", ex, sfx="pop")
            self.cue(tr, "b1", es)
            self.cue(tr, "b2", close, tk, sfx="ding")
            self.cue(tr, "b3", strip, sfx="success")
            self.cue(tr, "b4", Indicate(ex.box, color=CHALK_CYAN,
                                        scale_factor=1.03), sfx=None)
            self.finish(tr)

    # -- 8: decision map ------------------------------------------------------------------
    def beat_s8(self):
        with self.narrate("s8") as tr:
            self.heading("The Decision Map")
            c1 = tcard("CONVERT", [], CHALK_CYAN, w=4.8, h=1.7, head_size=32)
            m1 = M(r"\frac{\text{part}}{\text{whole}}\times100", 40)
            c1 = VGroup(c1[0], VGroup(T("CONVERT", 32, CHALK_CYAN),
                                      m1).arrange(DOWN, buff=0.12))
            c1[1].move_to(c1[0])
            c2 = tcard("INCREASE", ["add p to 100", "100% + p%"], CHALK_GREEN,
                       w=4.8, h=1.7, head_size=32, body_size=28)
            c3 = tcard("DECREASE", ["take p from 100", "100% - p%"], CHALK_PINK,
                       w=4.8, h=1.7, head_size=32, body_size=28)
            c4 = tcard("ESTIMATE", ["round first, then", "build from 10%"],
                       CHALK_AMBER, w=4.8, h=1.7, head_size=32, body_size=28)
            P(c1, CX - 2.55, 1.15)
            P(c2, CX + 2.55, 1.15)
            P(c3, CX - 2.55, -0.80)
            P(c4, CX + 2.55, -0.80)
            strip = P(T("Convert, change, estimate, check.", 28,
                        CHALK_YELLOW), CX, -2.2)
            tidy(c1, c2, c3, c4, same=True)  # auto-tidy
            self.cue(tr, "b0", c1, sfx="pop")
            self.cue(tr, "b1", c2)
            self.cue(tr, "b2", c3)
            self.cue(tr, "b3", c4)
            self.cue(tr, "b4", strip, sfx="success")
            self.finish(tr)

    # -- 9: your turn ----------------------------------------------------------------------
    def beat_s9(self):
        with self.narrate("s9q") as tr:
            self.heading("YOUR TURN", "Four quick checks.", CHALK_PINK)
            qa = q_card(pie(0.75, 0.62), "A  CONVERT",
                        ["18 out of 24", "as a percentage"], CHALK_CYAN)
            qb = q_card(coin_stack(4, 0.45),
                        "B  DISCOUNT", ["Rs 800, 10% off", "find the price"],
                        CHALK_GREEN)
            qc = q_card(calculator("20%", 1.2), "C  ESTIMATE",
                        ["20% of Rs 357.30", "round to 360 first"],
                        CHALK_AMBER)
            qd = q_card(note_stack(2, 1.4, "#8FD3A0", "Rs 100", 20),
                        "D  INCREASE", ["Rs 900 up 35%", "find the new value"],
                        CHALK_PINK)
            for q, (dx, y) in zip((qa, qb, qc, qd),
                                  [(-2.5, 0.70), (2.5, 0.70), (-2.5, -1.32),
                                   (2.5, -1.32)]):
                P(q, CX + dx, y)
            tidy(qa, qb, qc, qd, same=True)  # auto-tidy
            for q_ in (qa, qb, qc, qd):  # auto-tidy
                q_.scale(0.90)  # auto-tidy
            self.cue(tr, "b0", qa, sfx="pop")
            self.cue(tr, "b1", qb)
            self.cue(tr, "b2", qc)
            self.cue(tr, "b3", qd)
            self.finish(tr)
            self._qs = (qa, qb, qc, qd)
        self.think_clock()
        with self.narrate("s9a", reset=False) as tr:
            rows = [
                calc_row("A", "", r"\frac{18}{24}=\frac34=75\%", CHALK_CYAN,
                         w=9.6, h=1.05, math_size=40),
                calc_row("B", "", r"800-80=\text{Rs }720", CHALK_GREEN,
                         w=9.6, h=0.82, math_size=38),
                calc_row("C", "", r"20\%\text{ of }360=36+36\approx"
                         r"\text{Rs }72", CHALK_AMBER, w=9.6, h=0.82,
                         math_size=38),
                calc_row("D", "", r"135\%\text{ of }900=\text{Rs }1{,}215",
                         CHALK_PINK, w=9.6, h=0.82, math_size=38),
            ]
            for r, y in zip(rows, (1.16, 0.14, -0.78, -1.70)):
                P(r, CX, y)
            strip = P(T("Every answer used the whole as its base.", 26,
                        CHALK_WHITE), CX, -2.32)
            qa, qb, qc, qd = self._qs
            tidy(*rows, same=True)  # auto-tidy
            self.cue(tr, "b0", FadeOut(qa), FadeOut(qb), FadeOut(qc),
                     FadeOut(qd), FadeIn(rows[0]), sfx="click", rt=0.6)
            self.cue(tr, "b1", rows[1])
            self.cue(tr, "b2", rows[2])
            self.cue(tr, "b3", rows[3], strip, sfx="success")
            self.finish(tr)

    # -- 10 ----------------------------------------------------------------------------------
    def beat_s10(self):
        with self.narrate("s10") as tr:
            head = self.heading("Compare, Change, Estimate, Check")
            rows = [
                step_row("1", "COMPARE", "out of 100", CHALK_CYAN, h=0.88),
                step_row("2", "CHANGE", "100 + p up, 100 - p down", CHALK_GREEN,
                         h=0.88),
                step_row("3", "ESTIMATE", "round, then use 10%", CHALK_AMBER,
                         h=0.88),
                step_row("4", "CHECK", "estimate = reasonableness", CHALK_PINK,
                         h=0.88),
            ]
            for r, y in zip(rows, (1.60, 0.62, -0.36, -1.34)):
                P(r, CX, y)
            strip = P(T("Compare, change, estimate, check.", 28,
                        CHALK_YELLOW), CX, -2.25)
            thanks = P(T("Thank You for Watching!", 56, CHALK_WHITE,
                         max_w=9.4), CX, 0.55)
            bye = P(T("See you in the next lesson :)", 40, CHALK_YELLOW,
                      max_w=9.0), CX, -0.65)
            tidy(*rows, same=True)  # auto-tidy
            self.cue(tr, "b0", rows[0], sfx="pop")
            self.cue(tr, "b1", rows[1])
            self.cue(tr, "b2", rows[2])
            self.cue(tr, "b3", rows[3])
            self.cue(tr, "b4", strip, sfx="success")
            self.hold(tr, "b5")
            self.go(*[FadeOut(m) for m in (head, *rows, strip)], rt=0.55)
            self.cue(tr, "b5", FadeIn(thanks, shift=UP * 0.1), sfx=None)
            self.cue(tr, "b6", FadeIn(bye, shift=UP * 0.1), sfx=None)
            self.finish(tr)
        if not self.still:
            self.wait(END_HOLD)

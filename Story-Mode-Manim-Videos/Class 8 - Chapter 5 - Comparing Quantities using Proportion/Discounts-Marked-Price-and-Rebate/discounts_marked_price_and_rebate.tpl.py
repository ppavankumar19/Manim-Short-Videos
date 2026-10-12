"""
Finding Discounts & Marked Price: Calculating SP and Discount Percentages
Story-mode chalkboard lesson (Class 8 Maths, Chapter 5: Comparing Quantities
using Proportion).

LLM KEY / FUNCTION NAME: discounts_marked_price_and_rebate

Layout (re-done for legibility): every object sits INSIDE the green board
(ch5_kit.SAFE_*), headings are 36 pt, working text 26-30 pt, and the drawn
articles are shaded illustrations (ch5_art): a hanging price tag with a
starburst sticker, a hardcover book, a shirt, a bicycle, a ceiling fan, a
calculator, a 10 x 10 percent square and bar models with braces.

Title + 10 scenes:
  0. Title: the tag says Rs 1600, the sticker says 6% off.
  1. Marked price, discount (rebate), selling price: MP - Discount = SP.
  2. A book marked Rs 80 at 15% off: the 15% block is cut off the bar.
  3. A cycle marked Rs 3600 sold for Rs 3312: Rs 288 is 8% of the MARKED price.
  4. A fan marked Rs 1600 with 6% off: Rs 96 off, Rs 1504 payable.
  5. The shortcut on a 100-square: 6 cells off, 94 remain; both routes agree.
  6. Which route? Three question shapes.
  7. Common mistakes, each struck through beside its fix.
  8. Reasonableness checks: SP < MP and d + (100 - d) = 100.
  9. Your turn (four prompts, the silent THINK clock, then the answers).
 10. Recap and the spoken thank-you card.
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

INTRO_NARRATION = (
    "Discounts, marked price and rebate. <bookmark mark='b0'/> Finding the selling price and the discount percentage."
)
NARRATION = {}  # __NARRATION__
NARRATION = {"intro": INTRO_NARRATION, **NARRATION}


# ------------------------------------------------------------ local parts ---
def part_card(icon, head, body, color, w=3.1, h=3.0, icon_h=0.90):
    """An illustrated card: picture on top, bold name, short lines."""
    ic = fit(icon, w - 0.7, icon_h)
    head_t = T(head, 28, color, max_w=w - 0.3)
    body_t = lines(body, 24, CHALK_WHITE, buff=0.08, max_w=w - 0.3)
    content = VGroup(ic, head_t, body_t).arrange(DOWN, buff=0.14)
    box = panel(w, h, color)
    content.move_to(box.get_center())
    g = VGroup(box, content)
    g.box = box
    return g


def route_row(tag, given, todo, color, w=9.6, h=0.82):
    box = panel(w, h, color, radius=0.14, stroke=2.4)
    badge = num_badge(tag, color, r=0.26)
    badge.move_to(box.get_left() + RIGHT * (0.24 + badge.width / 2))
    g_ = T(given, 26, color)
    arr = Arrow(ORIGIN, RIGHT * 0.7, buff=0, stroke_width=5, tip_length=0.2,
                color=CHALK_WHITE)
    td = T(todo, 24, CHALK_WHITE)
    txt = VGroup(g_, arr, td).arrange(RIGHT, buff=0.28)
    fit(txt, w - badge.width - 0.8, h - 0.16)
    txt.next_to(badge, RIGHT, buff=0.30)
    g = VGroup(box, badge, txt)
    g.box = box
    return g


def mistake_card(wrong, fix, w=4.8, h=1.45, size=26):
    box = panel(w, h, CHALK_RED, opacity=0.78)
    cross = cross_mark(ORIGIN, size=0.2, color=CHALK_RED, width=6)
    wr = T(wrong, size, CHALK_RED)
    top = VGroup(cross, wr).arrange(RIGHT, buff=0.28)
    fit(top, w - 0.4, 0.5)
    fx = T(fix, size - 2, CHALK_GREEN, max_w=w - 0.4)
    both = VGroup(top, fx).arrange(DOWN, buff=0.26)
    both.move_to(box.get_center())
    g = VGroup(box, both)
    g.box = box
    return g


def q_card(icon, head, body, color, w=4.85, h=1.95):
    box = panel(w, h, color)
    ic = fit(icon, 1.35, h - 0.4)
    ic.move_to(box.get_left() + RIGHT * (0.2 + ic.width / 2 + 0.05))
    txt = VGroup(T(head, 28, color),
                 *[T(s, 24, CHALK_WHITE) for s in body]).arrange(
        DOWN, buff=0.1, aligned_edge=LEFT)
    fit(txt, w - 1.95, h - 0.3)
    txt.next_to(ic, RIGHT, buff=0.22)
    g = VGroup(box, ic, txt)
    g.box = box
    return g


class DiscountsMarkedPriceAndRebateStory(Ch5Scene):
    NARRATION = NARRATION
    TEXT_SCALE = 0.85     # medium type
    TIGHT_BOXES = True    # every box hugs its text
    STRICT_BOXES = True   # audit: boxes stay on the board with a gap between them
    AVOID_ART = True      # text/cards never sit on the teacher, students or badges
    INTRO_LINES = ('Discounts, Marked Price', '& Rebate')
    INTRO_SUB = 'Finding the Selling Price and Discount %'
    BEATS = ("intro", "title", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9",
             "s10")

    # -- 0: title ------------------------------------------------------------
    def beat_title(self):
        with self.narrate("title") as tr:
            self.heading("Discounts, Marked Price & Rebate",
                         "The tag price is not always the price you pay.")
            tag = P(shop_tag("Rs 1600", w=3.7, h=1.7, size=44), -2.05, 0.55)
            stk = P(sticker("6%", "OFF", r=0.62), 0.28, 1.12)
            c1 = tcard("MARKED PRICE", ["price on the article"], CHALK_GREEN,
                       w=4.35, h=1.15, head_size=28, body_size=24, pad=0.10,
                       gap=0.08)
            c2 = tcard("DISCOUNT / REBATE", ["the amount reduced"],
                       CHALK_AMBER, w=4.35, h=1.15, head_size=28,
                       body_size=24, pad=0.10, gap=0.08)
            c3 = tcard("SELLING PRICE", ["what is actually paid"], CHALK_CYAN,
                       w=4.35, h=1.15, head_size=28, body_size=24, pad=0.10,
                       gap=0.08)
            for c, y in zip((c1, c2, c3), (1.10, -0.10, -1.30)):
                P(c, 3.3, y)
            formula = P(M(r"\text{MP}-\text{Discount}=\text{SP}", 48,
                          CHALK_YELLOW), CX, -2.38)
            strip = P(lines(["The tagged price never", "disappears: the",
                             "discount is part of it."], 26, CHALK_WHITE,
                            buff=0.08, max_w=5.0), -2.0, -1.15)
            tidy(c1, c2, c3, same=True)  # auto-tidy
            self.cue(tr, "b0", tag, sfx="pop", scale=0.9)
            self.cue(tr, "b1", stk, sfx="click", scale=0.85)
            self.cue(tr, "b2", c1)
            self.cue(tr, "b3", c2)
            self.cue(tr, "b4", c3)
            self.cue(tr, "b5", formula, sfx="ding")
            self.cue(tr, "b6", strip, sfx="success")
            self.finish(tr)

    # -- 1: the three parts ------------------------------------------------
    def beat_s1(self):
        with self.narrate("s1") as tr:
            self.heading("The Three Parts of a Price",
                         "Marked price, discount, selling price.")
            cards = []
            specs = [
                (shop_tag("Rs 80", w=2.4, h=1.1, size=34), "MARKED PRICE",
                 ["price on", "the article", "(list price)"], CHALK_GREEN),
                (sticker("15%", "OFF", r=0.62), "DISCOUNT",
                 ["amount", "reduced", "(rebate)"], CHALK_AMBER),
                (coin_stack(4, 0.5), "SELLING PRICE",
                 ["price you", "actually pay", "(what you pay)"], CHALK_CYAN),
            ]
            for (ic, h_, b_, col), dx in zip(specs, (-3.33, 0.0, 3.33)):
                c = part_card(ic, h_, b_, col)
                P(c, CX + dx, 0.12)
                cards.append(c)
            formula = P(M(r"\text{MP}-\text{Discount}=\text{SP}", 50,
                          CHALK_YELLOW), CX, -1.88)
            strip = P(T("The discount is always taken on the MP.", 26,
                        CHALK_WHITE, max_w=9.6), CX, -2.38)
            self.cue(tr, "b0", cards[0], sfx="pop")
            self.cue(tr, "b1", cards[1])
            self.cue(tr, "b2", cards[2])
            self.cue(tr, "b3", formula, sfx="ding")
            self.cue(tr, "b4", Indicate(cards[0].box, color=CHALK_GREEN,
                                        scale_factor=1.05), sfx="pop")
            self.cue(tr, "b5", strip, sfx="success")
            self.finish(tr)

    # -- 2: the book ---------------------------------------------------------
    def beat_s2(self):
        with self.narrate("s2") as tr:
            self.heading("The Discount Comes First")
            bk = P(book(2.0), -3.0, 0.70)
            stk = P(sticker("15%", "OFF", r=0.72), -1.55, 1.55)
            bar = segbar(5.4, [(0.85, CHALK_GREEN, "SP = 85%"),
                               (0.15, CHALK_PINK, "15%")], h=0.80, size=24)
            P(bar, 2.30, 1.05)
            brace = brace_label(bar, "100% = MP = Rs 80", UP, size=26)
            pink = bar.segs[1]
            r1 = P(calc_row("1", "DISCOUNT", r"\frac{15}{100}\times 80="
                            r"\text{Rs }12", CHALK_GREEN, w=6.2, h=0.80,
                            math_size=40), 2.30, -0.80)
            r2 = P(calc_row("2", "SP", r"80-12=\text{Rs }68", CHALK_CYAN,
                            w=6.2, h=0.80, math_size=40), 2.30, -1.80)
            fbox = panel(3.3, 0.9, CHALK_YELLOW)
            fm = M(r"\text{MP}-\text{D}=\text{SP}", 40, CHALK_YELLOW)
            formula = VGroup(fbox, fm)
            P(formula, -3.0, -1.45)
            strip = P(T("Discount is on the MP, never on the SP.", 26,
                        CHALK_WHITE, max_w=9.6), CX, -2.38)
            tidy(r1, r2, same=True)  # auto-tidy
            self.cue(tr, "b0", bk, stk, sfx="pop", scale=0.9)
            self.cue(tr, "b1", bar, brace, sfx="click")
            self.cue(tr, "b2", r1)
            self.cue(tr, "b3", r2)
            dlab = T("15% = Rs 12 cut off", 26, CHALK_PINK)
            tgt = pink.get_center() + DOWN * 1.0
            P(dlab, tgt[0] - pink.width / 2 - 0.2 - dlab.width / 2, tgt[1])
            self.cue(tr, "b4", pink.animate.shift(DOWN * 1.0), FadeIn(dlab),
                     sfx="whoosh", rt=0.8)
            self.cue(tr, "b5", formula, sfx="ding")
            self.cue(tr, "b6", strip, sfx="success")
            self.finish(tr)

    # -- 3: the cycle ----------------------------------------------------------
    def beat_s3(self):
        with self.narrate("s3") as tr:
            self.heading("Finding the Discount Percent")
            tag = P(shop_tag("Rs 3600", w=2.5, h=1.15, size=32), -3.05, 1.40)
            bike = P(bicycle(3.3), -2.50, 0.30)
            W = 5.4
            mp = segbar(W, [(1.0, CHALK_AMBER, "MP = Rs 3600")], h=0.80,
                        size=26)
            sp = segbar(W, [(0.92, CHALK_GREEN, "SP = Rs 3312")], h=0.80,
                        size=26)
            P(mp, 2.60, 1.10)
            sp.move_to(np.array([mp.get_left()[0] + sp.width / 2, 0.30, 0]))
            gap_w = W * 0.08
            gap = Rectangle(width=gap_w, height=0.80, stroke_color=CHALK_PINK,
                            stroke_width=3, fill_color=CHALK_PINK,
                            fill_opacity=0.55)
            gap.move_to(np.array([sp.get_right()[0] + gap_w / 2, 0.30, 0]))
            rs = T("Rs 288", 28, CHALK_PINK)
            P(rs, SAFE_R - 0.05 - rs.width / 2, -0.28)
            on_mp = gap.copy().move_to(
                np.array([mp.get_right()[0] - gap_w / 2, 1.10, 0]))
            diff = P(T("DISCOUNT = 3600 - 3312 = Rs 288", 30, CHALK_AMBER,
                       max_w=9.4), CX, -1.00)
            pct = P(M(r"d\%=\frac{288}{3600}\times 100=8\%", 48,
                      CHALK_YELLOW), CX, -1.05)
            base = P(chip("THE BASE IS THE MARKED PRICE", CHALK_PINK, 28),
                     CX, -1.92)
            strip = P(T("Always divide by the MARKED price.", 26,
                        CHALK_WHITE), CX, -2.38)
            brace = brace_label(mp, "base = 100%", UP, size=24,
                                color=CHALK_PINK)
            self.cue(tr, "b0", tag, bike, sfx="pop", scale=0.9)
            self.cue(tr, "b1", mp, sp, sfx="click")
            self.cue(tr, "b2", gap, rs, diff)
            self.cue(tr, "b3", TransformFromCopy(gap, on_mp), brace, base,
                     rt=0.8)
            self.cue(tr, "b4", FadeOut(diff), FadeIn(pct, shift=UP * 0.06),
                     sfx="ding")
            self.cue(tr, "b5", strip, sfx="success")
            self.finish(tr)

    # -- 4: the fan ------------------------------------------------------------
    def beat_s4(self):
        with self.narrate("s4") as tr:
            self.heading("Given the Discount, Find the SP")
            fan = P(ceiling_fan(2.9), -2.75, 0.85)
            tag = P(shop_tag("Rs 1600", w=2.4, h=1.1, size=32), -3.25, -1.15)
            stk = P(sticker("6%", "OFF", r=0.68), -1.25, -1.05)
            r1 = P(calc_row("1", "DISCOUNT", r"\frac{6}{100}\times 1600="
                            r"\text{Rs }96", CHALK_GREEN, w=6.2, h=0.9,
                            math_size=38), 2.30, 1.50)
            r2 = P(calc_row("2", "SP", r"1600-96=\text{Rs }1504", CHALK_CYAN,
                            w=6.2, h=0.9, math_size=38), 2.30, 0.50)
            amt = chip("AMOUNT = Rs 96 (money)", CHALK_AMBER, 26, w=5.7)
            rate = chip("RATE = 6% (of the MP)", CHALK_PINK, 26, w=5.7)
            VGroup(amt, rate).arrange(DOWN, buff=0.22)
            P(VGroup(amt, rate), 2.30, -0.78)
            strip = P(T("Keep Rs and % apart: never mix them up.", 26,
                        CHALK_WHITE, max_w=9.6), CX, -2.38)
            tidy(r1, r2, same=True)  # auto-tidy
            tidy(amt, rate, same=True)  # auto-tidy
            self.cue(tr, "b0", fan, tag, stk, sfx="pop", scale=0.9)
            self.cue(tr, "b1", r1)
            self.cue(tr, "b2", r2)
            self.cue(tr, "b3", amt, rate)
            self.cue(tr, "b4", strip, sfx="success")
            self.finish(tr)

    # -- 5: the shortcut ---------------------------------------------------------
    def beat_s5(self):
        with self.narrate("s5") as tr:
            self.heading("The Shortcut: What Remains")
            grid = hundred_grid(0.255, 0.04)
            P(grid, -2.85, 0.0)
            for i, c in enumerate(grid):
                c.set_fill(CHALK_GREEN, 0.85)
            top_lab = lines(["100 squares", "= MP = Rs 1600"], 24, CHALK_WHITE,
                            buff=0.05)
            P(top_lab, -2.85, 1.98)
            low_lab = lines(["94% payable", "6% off = Rs 96"], 24,
                            CHALK_WHITE, buff=0.05)
            P(low_lab, -2.85, -1.82)
            r1 = P(calc_row("1", "ROUTE 1", r"1600-96=\text{Rs }1504",
                            CHALK_GREEN, w=5.5, h=0.9, math_size=38),
                   2.00, 1.35)
            r2 = P(calc_row("2", "ROUTE 2", r"\frac{94}{100}\times 1600="
                            r"\text{Rs }1504", CHALK_CYAN, w=5.5, h=0.9,
                            math_size=38), 2.00, 0.30)
            t1 = tick_mark(r1.get_right() + RIGHT * 0.40, 0.22)
            t2 = tick_mark(r2.get_right() + RIGHT * 0.40, 0.22)
            same = P(chip("BOTH ROUTES: Rs 1504", CHALK_YELLOW, 28), 2.10,
                     -0.70)
            formula = P(M(r"\text{SP}=\frac{100-d}{100}\times\text{MP}", 46,
                          CHALK_YELLOW), 2.10, -1.65)
            strip = P(T("Two routes are a free check.", 26, CHALK_WHITE),
                      2.10, -2.38)
            grid.set_opacity(1)
            tidy(r1, r2, same=True)  # auto-tidy
            self.cue(tr, "b0", grid, top_lab, sfx="pop", scale=0.96)
            cut = list(grid)[-6:]
            self.cue(tr, "b1", *[c.animate.set_fill(CHALK_PINK, 0.95)
                                 for c in cut], FadeIn(low_lab),
                     sfx="whoosh", rt=0.7)
            self.cue(tr, "b2", r1)
            self.cue(tr, "b3", r2)
            self.cue(tr, "b4", t1, t2, same, sfx="ding")
            self.cue(tr, "b5", formula, sfx="ding")
            self.cue(tr, "b6", strip, sfx="success")
            self.finish(tr)

    # -- 6: which route ----------------------------------------------------------
    def beat_s6(self):
        with self.narrate("s6") as tr:
            self.heading("Which Route Do I Need?",
                         "Look at what the question gives you.")
            r1 = P(route_row("1", "MP + D%", "find D first, then SP = MP - D",
                             CHALK_GREEN), CX, 1.20)
            r2 = P(route_row("2", "MP + SP", "D = MP - SP, then D/MP x 100",
                             CHALK_CYAN), CX, 0.25)
            r3 = P(route_row("3", "MP + D (Rs)", "SP = MP - D", CHALK_AMBER),
                   CX, -0.70)
            first = chip("FIRST: find D (or MP)", CHALK_YELLOW, 26)
            base = chip("BASE = MARKED PRICE", CHALK_PINK, 26)
            row = hrow(first, base, y=-1.68, gap=0.3)
            strip = P(T("Read twice, then pick the route.", 26, CHALK_WHITE),
                      CX, -2.42)
            tidy(r1, r2, r3, same=True)  # auto-tidy
            self.cue(tr, "b0", r1, sfx="pop")
            self.cue(tr, "b1", r2)
            self.cue(tr, "b2", r3)
            self.cue(tr, "b3", first)
            self.cue(tr, "b4", base)
            self.cue(tr, "b5", strip, sfx="success")
            self.finish(tr)

    # -- 7: mistakes -------------------------------------------------------------
    def beat_s7(self):
        with self.narrate("s7") as tr:
            self.heading("Common Mistakes and Their Fixes",
                         "Four wrong ideas, four corrections.")
            specs = [("d% = D / SP x 100", "divide by the MP"),
                     ("SP = MP + D", "SP = MP - D"),
                     ("Rs 96 = 6%", "Rs 96 amount, 6% rate"),
                     ("15% off = pay 15%", "you still pay 85%")]
            cards = []
            for (w_, f_), (dx, y) in zip(specs, [(-2.45, 0.95), (2.45, 0.95),
                                                 (-2.45, -0.62),
                                                 (2.45, -0.62)]):
                c = mistake_card(w_, f_)
                P(c, CX + dx, y)
                cards.append(c)
            checks = hrow(chip("BASE = MP", CHALK_GREEN, 24),
                          chip("SUBTRACT D", CHALK_YELLOW, 24),
                          chip("% vs Rs", CHALK_CYAN, 24), y=-1.72, gap=0.3)
            strip = P(T("Fix these four habits, keep the marks.", 26,
                        CHALK_WHITE, max_w=9.6), CX, -2.38)
            for k, c in enumerate(cards):
                self.cue(tr, f"b{k}", c, scale=0.94,
                         sfx="pop" if k == 0 else "click")
            self.cue(tr, "b4", checks, sfx="ding")
            self.cue(tr, "b5", strip, sfx="success")
            self.finish(tr)

    # -- 8: sense check -----------------------------------------------------------
    def beat_s8(self):
        with self.narrate("s8") as tr:
            self.heading("Does the Answer Make Sense?",
                         "Check the selling price against the marked price.")
            c1 = chip("SP < MP", CHALK_GREEN, 30, w=3.0)
            c2 = chip("d% + (100 - d)% = 100%", CHALK_CYAN, 28)
            hrow(c1, c2, y=1.30, gap=0.35)
            W = 8.6
            mp = segbar(W, [(1.0, CHALK_AMBER, "MP = Rs 1600  (100%)")],
                        h=0.72, size=26)
            sp = segbar(W, [(0.94, CHALK_GREEN, "SP = Rs 1504"),
                            (0.06, CHALK_PINK, "")], h=0.72, size=26)
            P(mp, CX, 0.62)
            sp.move_to(np.array([mp.get_left()[0] + sp.width / 2, -0.23, 0]))
            b94 = brace_label(sp.segs[0], "94% payable", DOWN, size=26,
                              color=CHALK_GREEN)
            b6 = brace_label(sp.segs[1], "6% off", DOWN, size=26,
                             color=CHALK_PINK)
            b6.label.shift(LEFT * 0.35)
            good = tick_mark([CX + 3.7, 1.30, 0], 0.26)
            check = P(chip("SP < MP: THE CHECK PASSES", CHALK_YELLOW, 28),
                      CX, -1.88)
            strip = P(T("Check SP < MP, and d + (100 - d) = 100.", 24,
                        CHALK_WHITE, max_w=9.6), CX, -2.42)
            self.cue(tr, "b0", c1, sfx="pop")
            self.cue(tr, "b1", c2)
            self.cue(tr, "b2", mp, sp, sfx="click")
            self.cue(tr, "b3", b94, b6, check, sfx="ding")
            self.cue(tr, "b4", strip, sfx="success")
            self.finish(tr)

    # -- 9: your turn -----------------------------------------------------------
    def beat_s9(self):
        with self.narrate("s9q") as tr:
            h = self.heading("YOUR TURN", "Four quick checks.", CHALK_PINK)
            qa = q_card(shirt(1.7), "A  SHIRT", ["MP Rs 450", "7% off: D, SP"],
                        CHALK_GREEN)
            qb = q_card(book(1.3), "B  ARTICLE", ["MP Rs 1000", "SP Rs 900: D%"],
                        CHALK_CYAN)
            table = VGroup(
                RoundedRectangle(corner_radius=0.05, width=1.5, height=0.20),
                Rectangle(width=0.14, height=0.9), Rectangle(width=0.14,
                                                             height=0.9))
            table[0].set_fill("#C98B4A", 1).set_stroke(OUTLINE, 3)
            table[1].set_fill("#A56F36", 1).set_stroke(OUTLINE, 3)
            table[2].set_fill("#A56F36", 1).set_stroke(OUTLINE, 3)
            table[1].next_to(table[0], DOWN, buff=0).align_to(table[0], LEFT
                                                              ).shift(RIGHT * 0.12)
            table[2].next_to(table[0], DOWN, buff=0).align_to(table[0], RIGHT
                                                              ).shift(LEFT * 0.12)
            qc = q_card(table, "C  TABLE", ["MP Rs 250", "5% off: use 95%"],
                        CHALK_AMBER)
            qd = q_card(calculator("SP<MP", 1.2), "D  CHECK",
                        ["is SP smaller", "than MP? always"], CHALK_PINK)
            pos = [(-2.5, 0.70), (2.5, 0.70), (-2.5, -1.32), (2.5, -1.32)]
            for q, (dx, y) in zip((qa, qb, qc, qd), pos):
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
            a1 = P(calc_row("A", "SHIRT", r"\frac{7}{100}\times450=31.50,"
                            r"\ \text{SP}=\text{Rs }418.50", CHALK_GREEN,
                            w=9.6, h=0.95, math_size=34), CX, 1.15)
            a2 = P(calc_row("B", "ARTICLE", r"D=100,\ \ \frac{100}{1000}"
                            r"\times100=10\%", CHALK_CYAN, w=9.6, h=0.95,
                            math_size=34), CX, 0.05)
            a3 = P(calc_row("C", "TABLE", r"\frac{95}{100}\times250="
                            r"\text{Rs }237.50", CHALK_AMBER, w=9.6, h=0.95,
                            math_size=34), CX, -1.05)
            strip = P(T("SP is smaller than MP, and the base was the MP.",
                        26, CHALK_WHITE, max_w=9.6), CX, -2.15)
            qa, qb, qc, qd = self._qs
            tidy(a1, a2, a3, same=True)  # auto-tidy
            self.cue(tr, "b0", FadeOut(qa), FadeOut(qb), FadeOut(qc),
                     FadeOut(qd), FadeIn(a1), sfx="click", rt=0.6)
            self.cue(tr, "b1", a2)
            self.cue(tr, "b2", a3)
            self.cue(tr, "b3", strip, sfx="success")
            self.finish(tr)

    # -- 10: recap + thanks --------------------------------------------------------
    def beat_s10(self):
        with self.narrate("s10") as tr:
            head = self.heading("Marked Price to Selling Price")
            rows = [
                step_row("1", "MARKED PRICE", "price on the article", CHALK_GREEN,
                         h=0.88, size=26),
                step_row("2", "DISCOUNT / REBATE", "SP = MP - D", CHALK_CYAN,
                         h=0.88, size=26),
                step_row("3", "DISCOUNT %", "(MP - SP) / MP x 100", CHALK_YELLOW,
                         h=0.88, size=26),
                step_row("4", "PRICE FLOW", "tag, reduce, pay, compare",
                         CHALK_AMBER, h=0.88, size=26),
            ]
            for r, y in zip(rows, (1.75, 0.70, -0.35, -1.40)):
                P(r, CX, y)
            strip = P(T("Keep MP visible, subtract D, check the answer.", 26,
                        CHALK_WHITE, max_w=9.6), CX, -2.35)
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

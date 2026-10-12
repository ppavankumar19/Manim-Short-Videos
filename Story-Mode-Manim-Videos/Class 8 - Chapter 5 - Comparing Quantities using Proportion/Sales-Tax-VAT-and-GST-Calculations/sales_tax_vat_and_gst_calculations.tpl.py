"""
Sales Tax, VAT & GST Calculations: Determining Original Prices and Total Bills
Story-mode chalkboard lesson (Class 8 Maths, Chapter 5: Comparing Quantities
using Proportion).

LLM KEY / FUNCTION NAME: sales_tax_vat_and_gst_calculations

Layout re-done for legibility: big chalk type inside the green board and drawn
diagrams -- a pair of sneakers with a hanging tag, a till receipt, a pharmacy
front, a shopping bag, a bar model whose tax layer attaches to the base, and a
tax block that splits into two equal halves.

The arithmetic is one model throughout: base price + percentage tax = bill.
Sales tax, VAT and GST are historical/textbook examples here, never current
tax advice, and the CGST/SGST equal split is the textbook's worked case.

Title + 10 scenes:
  0. The tag is not the bill: shoes at Rs 450 plus 6% tax.
  1. A tax is a percentage increase: base 100%, bill (100 + r)%.
  2. Sales tax on Rs 450 at 6%: Rs 27, bill Rs 477, or 1.06 x 450.
  3. A VAT bill: Rs 354.45 + 5% VAT = Rs 372.18.
  4. GST on Rs 1,000 at 5%: Rs 50, bill Rs 1,050.
  5. Working backward: Rs 2,360 incl. 18% GST -> base Rs 2,000, tax Rs 360.
  6. The textbook's CGST / SGST split of Rs 360.
  7. Forward or backward lane; tax adds, discount removes.
  8. The classic error: the rate applied to the bill.
  9. Your turn and the answers.
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
    "Sales tax, VAT and GST calculations. <bookmark mark='b0'/> Finding original prices and total bills."
)
NARRATION = {}  # __NARRATION__
NARRATION = {"intro": INTRO_NARRATION, **NARRATION}


class SalesTaxVatAndGstCalculationsStory(Ch5Scene):
    NARRATION = NARRATION
    TEXT_SCALE = 0.85     # medium type
    TIGHT_BOXES = True    # every box hugs its text
    STRICT_BOXES = True   # audit: boxes stay on the board with a gap between them
    AVOID_ART = True      # text/cards never sit on the teacher, students or badges
    INTRO_LINES = ('Sales Tax, VAT', '& GST')
    INTRO_SUB = 'Original Prices and Total Bills'
    BEATS = ("intro", "title", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9",
             "s10")

    # -- 0 -----------------------------------------------------------------
    def beat_title(self):
        with self.narrate("title") as tr:
            self.heading("Sales Tax, VAT & GST",
                         "The price tag is not the bill.")
            shoes = P(shoe_pair(3.1), -2.25, 0.85)
            tag = P(shop_tag("Rs 450", w=3.0, h=1.2, size=30), -2.9, -0.78)
            stk = P(sticker("+6%", "TAX", r=0.66, size=30), -1.05, -0.62)
            c1 = tcard("BASE PRICE", ["price before any tax"], CHALK_GREEN,
                       w=4.35, h=1.15, head_size=28, body_size=24, pad=0.10,
                       gap=0.08)
            c2 = tcard("TAX AMOUNT", ["the % that is added"], CHALK_AMBER,
                       w=4.35, h=1.15, head_size=28, body_size=24, pad=0.10,
                       gap=0.08)
            c3 = tcard("FINAL BILL", ["base price + the tax"], CHALK_CYAN,
                       w=4.35, h=1.15, head_size=28, body_size=24, pad=0.10,
                       gap=0.08)
            for c, y in zip((c1, c2, c3), (1.10, -0.10, -1.30)):
                P(c, 3.3, y)
            formula = P(M(r"\text{Bill}=\text{Base}+\text{Tax}", 48,
                          CHALK_YELLOW), CX, -2.38)
            tidy(c1, c2, c3, same=True)  # auto-tidy
            self.cue(tr, "b0", shoes, tag, sfx="pop", scale=0.9)
            self.cue(tr, "b1", stk, sfx="click", scale=0.85)
            self.cue(tr, "b2", c1)
            self.cue(tr, "b3", c2)
            self.cue(tr, "b4", c3, formula, sfx="ding")
            self.finish(tr)

    # -- 1: percentage increase ------------------------------------------------
    def beat_s1(self):
        with self.narrate("s1") as tr:
            self.heading("A Tax Is a Percentage Increase")
            base = segbar(5.6, [(1.0, CHALK_CYAN, "BASE = 100%")], h=0.95,
                          size=28)
            tax = segbar(1.5, [(1.0, CHALK_PINK, "+ r%")], h=0.95, size=28)
            left = CX - 7.1 / 2
            P(base, left + 2.8, 0.85)
            P(tax, left + 5.6 + 0.75, 0.85)
            b_base = brace_label(base, "base price", UP, size=26)
            b_tot = brace_label(VGroup(base, tax), "100 + r  (6% tax: 106%)",
                                DOWN, size=28, color=CHALK_YELLOW)
            formula = P(M(r"\text{Bill}=\frac{100+r}{100}\times\text{Base}",
                          50, CHALK_YELLOW), CX, -1.50)
            strip = P(T("The same % increase as the earlier lesson.", 26,
                        CHALK_WHITE, max_w=9.6), CX, -2.35)
            self.cue(tr, "b0", base, b_base, sfx="pop")
            self.cue(tr, "b1", FadeIn(tax, shift=DOWN * 1.1), sfx="whoosh",
                     rt=0.8)
            self.cue(tr, "b2", b_tot)
            self.cue(tr, "b3", formula, sfx="ding")
            self.cue(tr, "b4", strip, sfx="success")
            self.finish(tr)

    # -- 2: shoes ------------------------------------------------------------------
    def beat_s2(self):
        with self.narrate("s2") as tr:
            self.heading("Sales Tax on the Shoes")
            shoes = P(shoe_pair(2.6), -2.8, 1.45)
            tag = P(shop_tag("Rs 450", w=2.9, h=1.1, size=30), -3.0, 0.30)
            rc = P(receipt(2.4, 1.9, ("SHOES  450", "TAX 6%  27", "BILL  477"),
                           22, ("#2A2A2A", "#B02030", "#146B2E")), -2.8, -1.50)
            r1 = P(calc_row("1", "TAX", r"\frac{6}{100}\times450=\text{Rs }27",
                            CHALK_PINK, w=6.2, h=0.95, math_size=40), 2.30,
                   1.35)
            r2 = P(calc_row("2", "BILL", r"450+27=\text{Rs }477", CHALK_GREEN,
                            w=6.2, h=0.95, math_size=40), 2.30, 0.30)
            sc = P(chip("SHORTCUT: 106% OF 450", CHALK_YELLOW, 28, w=6.2),
                   2.30, -0.70)
            r3 = P(calc_row("", "", r"1.06\times450=\text{Rs }477",
                            CHALK_YELLOW, w=6.2, h=0.9, math_size=42), 2.30,
                   -1.65)
            tidy(r1, r2, r3, same=True)  # auto-tidy
            self.cue(tr, "b0", shoes, tag, sfx="pop")
            self.cue(tr, "b1", r1)
            self.cue(tr, "b2", r2, rc)
            self.cue(tr, "b3", sc, sfx="ding")
            self.cue(tr, "b4", r3, sfx="success")
            self.finish(tr)

    # -- 3: VAT bill -------------------------------------------------------------------
    def beat_s3(self):
        with self.narrate("s3") as tr:
            self.heading("A VAT Bill at the Medical Shop")
            ph = P(pharmacy(3.3), -2.6, 0.60)
            r1 = P(calc_row("1", "BEFORE VAT", r"\text{Rs }354.45",
                            CHALK_CYAN, w=6.2, h=0.9, math_size=40), 2.30,
                   1.40)
            r2 = P(calc_row("2", "VAT 5%", r"\frac{5}{100}\times354.45=17.72",
                            CHALK_PINK, w=6.2, h=1.0, math_size=36), 2.30,
                   0.35)
            r3 = P(calc_row("3", "TOTAL", r"354.45+17.72=\text{Rs }372.18",
                            CHALK_GREEN, w=6.2, h=0.9, math_size=34), 2.30,
                   -0.65)
            same = P(chip("VAT works like sales tax: the same % idea",
                          CHALK_YELLOW, 26, w=9.6), CX, -1.65)
            strip = P(T("Old rates: textbook examples, not advice for today.",
                        24, CHALK_WHITE, max_w=9.6), CX, -2.35)
            tidy(r1, r2, r3, same=True)  # auto-tidy
            self.cue(tr, "b0", ph, r1, sfx="pop")
            self.cue(tr, "b1", r2)
            self.cue(tr, "b2", r3)
            self.cue(tr, "b3", same, sfx="ding")
            self.cue(tr, "b4", strip, sfx="success")
            self.finish(tr)

    # -- 4: GST --------------------------------------------------------------------------
    def beat_s4(self):
        with self.narrate("s4") as tr:
            self.heading("GST: the Same Structure")
            goods = icon_chip(shopping_bag(1.0), "GOODS", CHALK_AMBER, w=2.9,
                              h=1.25, size=28, icon_w=1.0)
            serv = icon_chip(wrench(1.3), "SERVICES", CHALK_PURPLE, w=3.2,
                             h=1.25, size=28, icon_w=1.0)
            base = tcard("BASE Rs 1000", ["GST 5%"], CHALK_CYAN, w=3.5, h=1.25, head_size=26, body_size=26, pad=0.08, gap=0.06)
            hrow(goods, serv, base, y=1.40, gap=0.15)
            r1 = P(calc_row("1", "TAX", r"\frac{5}{100}\times1000=\text{Rs }50",
                            CHALK_PINK, w=9.6, h=0.95, math_size=40), CX, 0.20)
            r2 = P(calc_row("2", "BILL", r"1000+50=\text{Rs }1050",
                            CHALK_GREEN, w=9.6, h=0.9, math_size=40), CX,
                   -0.85)
            r3 = P(calc_row("", "SHORTCUT", r"105\%\text{ of }1000=\text{Rs }1050",
                            CHALK_YELLOW, w=9.6, h=0.9, math_size=40), CX,
                   -1.85)
            tidy(r1, r2, r3, same=True)  # auto-tidy
            self.cue(tr, "b0", goods, serv, sfx="pop")
            self.cue(tr, "b1", base)
            self.cue(tr, "b2", r1)
            self.cue(tr, "b3", r2)
            self.cue(tr, "b4", r3, sfx="success")
            self.finish(tr)

    # -- 5: backward ---------------------------------------------------------------------
    def beat_s5(self):
        with self.narrate("s5") as tr:
            self.heading("Working Backward")
            bill = P(chip("BILL Rs 2,360 includes 18% GST", CHALK_YELLOW, 28),
                     CX, 1.75)
            W = 7.6
            bar = segbar(W, [(100 / 118, CHALK_CYAN, "BASE = 100%"),
                             (18 / 118, CHALK_PINK, "18%")], h=0.85, size=26)
            P(bar, CX, 0.85)
            br = brace_label(bar, "118% = Rs 2,360", DOWN, size=28,
                             color=CHALK_YELLOW)
            fm = P(M(r"\text{Base}=\frac{2360\times100}{118}", 42,
                     CHALK_GREEN), CX, -1.15)
            base_c = chip("BASE Rs 2,000", CHALK_GREEN, 24, w=2.95)
            tax_c = chip("TAX Rs 360", CHALK_PINK, 24, w=2.75)
            bad = mistake_card("18% of 2360, subtract", "rate was on the base",
                               w=4.1, h=0.95, size=24)
            hrow(base_c, tax_c, bad, y=-2.15, gap=0.2)
            self.cue(tr, "b0", bill, sfx="pop")
            self.cue(tr, "b1", bar, sfx="click")
            self.cue(tr, "b2", br, fm, sfx="ding")
            self.cue(tr, "b3", base_c, tax_c, sfx="click")
            self.cue(tr, "b4", bad, sfx="success")
            self.finish(tr)

    # -- 6: CGST / SGST -------------------------------------------------------------------
    def beat_s6(self):
        with self.narrate("s6") as tr:
            self.heading("Splitting the GST")
            whole = segbar(6.4, [(1.0, CHALK_PINK, "TOTAL GST  Rs 360")],
                           h=1.1, size=30)
            P(whole, CX, 1.15)
            half = DashedLine(whole.get_top() + UP * 0.15,
                              whole.get_bottom() + DOWN * 0.15,
                              stroke_color=CHALK_YELLOW, stroke_width=4,
                              dash_length=0.12)
            P(half, CX, 1.15)
            left = segbar(3.1, [(1.0, CHALK_CYAN, "CGST Rs 180")], h=1.1,
                          size=28)
            right = segbar(3.1, [(1.0, CHALK_AMBER, "SGST Rs 180")], h=1.1,
                           size=28)
            P(left, CX - 2.3, -0.30)
            P(right, CX + 2.3, -0.30)
            cl = P(T("central GST", 26, CHALK_CYAN), CX - 2.3, -1.12)
            cr = P(T("state GST", 26, CHALK_AMBER), CX + 2.3, -1.12)
            eq = P(M(r"180+180=360", 48, CHALK_YELLOW), CX, -1.85)
            strip = P(T("An equal split: this worked example only.", 26,
                        CHALK_WHITE), CX, -2.42)
            self.cue(tr, "b0", whole, sfx="pop")
            self.cue(tr, "b1", half, sfx="click")
            self.cue(tr, "b2", FadeIn(left, shift=DOWN * 0.5), FadeIn(cl),
                     sfx="whoosh")
            self.cue(tr, "b3", FadeIn(right, shift=DOWN * 0.5), FadeIn(cr),
                     sfx="whoosh")
            self.cue(tr, "b4", eq, strip, sfx="success")
            self.finish(tr)

    # -- 7: forward / backward ---------------------------------------------------------------
    def beat_s7(self):
        with self.narrate("s7") as tr:
            self.heading("Forward or Backward?")

            def lane(head, sub, tex, color):
                box = panel(4.8, 2.25, color)
                col = VGroup(T(head, 30, color), T(sub, 24, CHALK_WHITE),
                             M(tex, 38, CHALK_WHITE)).arrange(DOWN, buff=0.16)
                fit(col, 4.5, 2.0)
                col.move_to(box)
                g = VGroup(box, col)
                g.box = box
                return g
            fw = lane("FORWARD", "base price is given",
                      r"\text{Bill}=\text{Base}\times\frac{100+r}{100}",
                      CHALK_GREEN)
            bw = lane("BACKWARD", "tax-inclusive bill is given",
                      r"\text{Base}=\text{Bill}\times\frac{100}{100+r}",
                      CHALK_CYAN)
            P(fw, CX - 2.55, 0.90)
            P(bw, CX + 2.55, 0.90)
            pick = P(chip("PICK THE LANE BY WHAT IS GIVEN", CHALK_YELLOW, 26),
                     CX, -0.60)
            add = chip("TAX  adds (+)", CHALK_GREEN, 28, w=4.5)
            rem = chip("DISCOUNT  removes (-)", CHALK_PINK, 28, w=4.9)
            both = hrow(add, rem, y=-1.50, gap=0.3)
            strip = P(T("Tax adds, discount removes.", 28, CHALK_YELLOW),
                      CX, -2.35)
            self.cue(tr, "b0", fw, sfx="pop")
            self.cue(tr, "b1", bw)
            self.cue(tr, "b2", pick)
            self.cue(tr, "b3", both, sfx="click")
            self.cue(tr, "b4", strip, sfx="success")
            self.finish(tr)

    # -- 8: classic error ------------------------------------------------------------------------
    def beat_s8(self):
        with self.narrate("s8") as tr:
            self.heading("The Classic Error")
            base = P(chip("BASE Rs 1000 | GST 18%", CHALK_CYAN, 28), CX, 1.65)
            r1 = P(calc_row("", "TAX", r"\frac{18}{100}\times1000=180,\ \ "
                            r"\text{Bill}=1180", CHALK_GREEN, w=9.6, h=1.0,
                            math_size=38), CX, 0.55)
            m1 = mistake_card("18% of the BILL", "rate belongs on the base",
                              w=4.8, h=1.3, size=26)
            m2 = mistake_card("bill minus 18%", "work backward instead",
                              w=4.8, h=1.3, size=26)
            P(m1, CX - 2.55, -0.75)
            P(m2, CX + 2.55, -0.75)
            rule = P(chip("RATE ON THE BASE;  BACKWARD: x 100/(100+r)",
                          CHALK_YELLOW, 26, w=9.6), CX, -2.05)
            tidy(m1, m2, same=True)  # auto-tidy
            self.cue(tr, "b0", base, sfx="pop")
            self.cue(tr, "b1", r1)
            self.cue(tr, "b2", m1, sfx="click")
            self.cue(tr, "b3", m2, sfx="click")
            self.cue(tr, "b4", rule, sfx="success")
            self.finish(tr)

    # -- 9: your turn ---------------------------------------------------------------------------------
    def beat_s9(self):
        with self.narrate("s9q") as tr:
            self.heading("YOUR TURN", "Four quick checks.", CHALK_PINK)
            qa = q_card(note_stack(2, 1.3, "#8FD3A0", "Rs 100", 18), "A  TAX",
                        ["Rs 800, tax 5%", "find tax and bill"], CHALK_GREEN)
            qb = q_card(calculator("1180", 1.2), "B  BACK",
                        ["bill Rs 1180, 18%", "find base and tax"], CHALK_CYAN)
            blk = VGroup(Rectangle(width=0.7, height=0.5),
                         Rectangle(width=0.7, height=0.5)).arrange(RIGHT,
                                                                   buff=0.05)
            blk[0].set_fill(CHALK_CYAN, 0.8).set_stroke(OUTLINE, 3)
            blk[1].set_fill(CHALK_AMBER, 0.8).set_stroke(OUTLINE, 3)
            qc = q_card(blk, "C  SPLIT", ["GST Rs 180", "split equally"],
                        CHALK_AMBER)
            qd = q_card(cross_mark(ORIGIN, 0.5, CHALK_RED, 10), "D  ERROR",
                        ["18% of 1180 right?", "same purchase"], CHALK_PINK)
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
                calc_row("A", "", r"\frac{5}{100}\times800=40,\ \ "
                         r"\text{bill }840", CHALK_GREEN, w=9.6, h=1.0,
                         math_size=38),
                calc_row("B", "", r"\frac{1180\times100}{118}=1000,\ \ "
                         r"\text{tax }180", CHALK_CYAN, w=9.6, h=1.05,
                         math_size=36),
                calc_row("C", "", r"180\div2=90\ \text{each}", CHALK_AMBER,
                         w=9.6, h=0.8, math_size=40),
                calc_row("D", "", r"\text{NO: the rate is on Rs }1000",
                         CHALK_PINK, w=9.6, h=0.8, math_size=40),
            ]
            for r, y in zip(rows, (1.16, 0.12, -0.80, -1.72)):
                P(r, CX, y)
            qa, qb, qc, qd = self._qs
            tidy(*rows, same=True)  # auto-tidy
            self.cue(tr, "b0", FadeOut(qa), FadeOut(qb), FadeOut(qc),
                     FadeOut(qd), FadeIn(rows[0]), sfx="click", rt=0.6)
            self.cue(tr, "b1", rows[1])
            self.cue(tr, "b2", rows[2])
            self.cue(tr, "b3", rows[3], sfx="success")
            self.finish(tr)

    # -- 10 -------------------------------------------------------------------------------------------
    def beat_s10(self):
        with self.narrate("s10") as tr:
            head = self.heading("Start at 100%, Add the Tax")
            rows = [
                step_row("1", "BASE", "start at 100%", CHALK_CYAN, h=0.88),
                step_row("2", "ADD TAX", "100 + r percent", CHALK_PINK,
                         h=0.88),
                step_row("3", "BACKWARD", "x 100 / (100 + r)", CHALK_GREEN,
                         h=0.88),
                step_row("4", "TAX vs DISCOUNT", "adds / removes", CHALK_AMBER,
                         h=0.88),
            ]
            for r, y in zip(rows, (1.60, 0.62, -0.36, -1.34)):
                P(r, CX, y)
            strip = P(T("Start at 100%, add the tax, work backward.", 26,
                        CHALK_YELLOW, max_w=9.6), CX, -2.30)
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

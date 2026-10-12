"""
Profit, Loss & Overhead Expenses: Solving Single and Double Transaction
Problems
Story-mode chalkboard lesson (Class 8 Maths, Chapter 5: Comparing Quantities
using Proportion).

LLM KEY / FUNCTION NAME: profit_loss_overhead_expenses_and_transactions

Layout re-done for legibility: big chalk type inside the green board and drawn
diagrams -- a refrigerator, delivery truck and spanner for the overheads, a
two-pan balance that tips towards profit or loss, a money-out / money-in
ledger, a flat, two tables, bananas, a bicycle and two TV sets.

Title + 10 scenes:
  0. Rs 5,000 + Rs 100 + Rs 500 = Rs 5,600 -- the real cost of a fridge.
  1. Profit, loss or neither: compare first (balance), then subtract.
  2. Percentage is on the cost price; dividing by SP is struck through.
  3. The refrigerator ledger: Rs 5,600 cost, Rs 7,000 sold, 25% profit.
  4. The flat ledger with a loss: 7.5%.
  5. The two-table trap: +20% and -20% do not cancel.
  6. The whole transaction: Rs 6,250 cost, Rs 6,000 sold, 4% loss.
  7. The five-step decision process.
  8. Spoiled bananas still cost.
  9. Your turn (bicycle, two TVs) and the answers.
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
    "Profit, loss and overhead expenses. <bookmark mark='b0'/> Solving single and double transaction problems."
)
NARRATION = {
    "title": (
        "The purchase price is not always the real cost. <bookmark mark='b0'/> "
        "A second-hand refrigerator is bought for five thousand rupees. "
        "<bookmark mark='b1'/> Then one hundred rupees go on transport, "
        "<bookmark mark='b2'/> and five hundred rupees on repairs. <bookmark "
        "mark='b3'/> So the money actually spent is five thousand plus one "
        "hundred plus five hundred, that is five thousand six hundred rupees. "
        "<bookmark mark='b4'/> Sold for seven thousand rupees, the real profit "
        "is seven thousand minus five thousand six hundred, which is one "
        "thousand four hundred rupees. <bookmark mark='b5'/> Not two thousand."
    ),
    "s1": (
        "First, decide whether a deal is a profit, a loss, or neither. "
        "<bookmark mark='b0'/> Cost price five hundred rupees, selling price "
        "six hundred and fifty: the selling price is bigger, so this is a "
        "profit of six hundred fifty minus five hundred, that is one hundred "
        "and fifty rupees. <bookmark mark='b1'/> Now change the selling price "
        "to four hundred and fifty: this time the cost price is bigger, so it "
        "is a loss of five hundred minus four hundred fifty, that is fifty "
        "rupees. <bookmark mark='b2'/> And when the selling "
        "price equals the cost price, there is neither a profit nor a loss. "
        "<bookmark mark='b3'/> So there are two formulas: profit is selling "
        "price minus cost price, and loss is cost price minus selling price. "
        "<bookmark mark='b4'/> Always ask which one is bigger before you "
        "subtract."
    ),
    "s2": (
        "Now the percentage. <bookmark mark='b0'/> A profit of one hundred "
        "fifty rupees on a cost price of five hundred rupees is a profit of "
        "thirty percent. <bookmark mark='b1'/> The difference is always "
        "measured against the cost price: profit percent is profit divided by "
        "cost price, times one hundred. <bookmark mark='b2'/> And loss percent "
        "is loss divided by cost price, times one hundred. <bookmark "
        "mark='b3'/> The cost price is the base. <bookmark mark='b4'/> A very "
        "common error is to divide by the selling price instead. That is "
        "wrong, and we cross it out."
    ),
    "s3": (
        "Let us keep a proper ledger for the refrigerator. <bookmark "
        "mark='b0'/> Purchase price five thousand rupees. <bookmark "
        "mark='b1'/> Add transport, one hundred rupees, <bookmark mark='b2'/> "
        "and repairs, five hundred rupees. <bookmark mark='b3'/> So the total "
        "cost price is five thousand six hundred rupees. <bookmark mark='b4'/> "
        "The selling price is seven thousand rupees, so the profit is one "
        "thousand four hundred rupees. <bookmark mark='b5'/> And the profit "
        "percent is one thousand four hundred divided by five thousand six "
        "hundred, times one hundred. That is twenty five percent."
    ),
    "s4": (
        "Here is the same idea with a loss. <bookmark mark='b0'/> A flat is "
        "bought for four lakh fifty thousand rupees. <bookmark mark='b1'/> Ten "
        "thousand rupees are spent on repairs and painting, <bookmark "
        "mark='b2'/> so the total cost price is four lakh sixty thousand "
        "rupees. <bookmark mark='b3'/> It is sold for four lakh twenty five "
        "thousand five hundred rupees, so the selling price is smaller. "
        "<bookmark mark='b4'/> The loss is four lakh sixty thousand minus four "
        "lakh twenty five thousand five hundred, that is thirty four thousand "
        "five hundred rupees. <bookmark mark='b5'/> And the loss percent is "
        "thirty four thousand five hundred divided by four lakh sixty "
        "thousand, times one hundred, which is seven point five percent."
    ),
    "s5": (
        "Now a trap. <bookmark mark='b0'/> Two tables are each sold for three "
        "thousand rupees. <bookmark mark='b1'/> One gives a gain of twenty "
        "percent, <bookmark mark='b2'/> and the other gives a loss of twenty "
        "percent. <bookmark mark='b3'/> Do the plus twenty and the minus "
        "twenty cancel? It is tempting to say zero percent. <bookmark "
        "mark='b4'/> But the percentages act on different cost prices. On the "
        "first table, three thousand rupees is one hundred and twenty percent "
        "of the cost price, so the cost price is three thousand divided by one "
        "point two, that is two thousand five hundred rupees. <bookmark "
        "mark='b5'/> On the second table, three thousand rupees is eighty "
        "percent of the cost price, so the cost price is three thousand "
        "divided by zero point eight, that is three thousand seven hundred and "
        "fifty rupees. The two bases are different."
    ),
    "s6": (
        "Now solve the whole transaction. <bookmark mark='b0'/> The total cost "
        "price is two thousand five hundred plus three thousand seven hundred "
        "fifty, that is six thousand two hundred and fifty rupees. <bookmark "
        "mark='b1'/> The total selling price is three thousand plus three "
        "thousand, that is six thousand rupees. <bookmark mark='b2'/> The "
        "selling price is smaller, so overall there is a loss of two hundred "
        "and fifty rupees. <bookmark mark='b3'/> And the loss percent is two "
        "hundred and fifty divided by six thousand two hundred fifty, times "
        "one hundred, which is four percent. <bookmark mark='b4'/> So plus "
        "twenty percent and minus twenty percent did not give zero percent "
        "here."
    ),
    "s7": (
        "Here is the decision process, in five steps. <bookmark mark='b0'/> "
        "Step one: find the purchase price. <bookmark mark='b1'/> Step two: "
        "add every overhead expense to get the total cost price. <bookmark "
        "mark='b2'/> Step three: find the total selling price. <bookmark "
        "mark='b3'/> Step four: compare the two. If the selling price is "
        "bigger there is a profit, and if it is smaller there is a loss. "
        "<bookmark mark='b4'/> Step five: divide by the cost price and "
        "multiply by one hundred for the percentage. <bookmark mark='b5'/> And "
        "when there are several items, compare the sum of the cost prices with "
        "the sum of the selling prices."
    ),
    "s8": (
        "One more reminder. <bookmark mark='b0'/> Overheads still count when "
        "part of the stock cannot be sold. <bookmark mark='b1'/> Bananas are "
        "bought for one thousand two hundred and fifty rupees, and two hundred "
        "and fifty rupees go on transport, so the total cost price is one "
        "thousand five hundred rupees. <bookmark mark='b2'/> Only some dozens "
        "are good enough to sell, and they bring in one thousand five hundred "
        "and seventy five rupees. <bookmark mark='b3'/> The spoiled bananas do "
        "not vanish from the cost: the money spent on them is still part of "
        "the cost price. <bookmark mark='b4'/> And the profit is one thousand "
        "five hundred seventy five minus one thousand five hundred, that is "
        "seventy five rupees, which is five percent."
    ),
    "s9q": (
        "Your turn. <bookmark mark='b0'/> First: a bicycle is bought for four "
        "thousand rupees, <bookmark mark='b1'/> with two hundred rupees for "
        "transport and three hundred rupees for repair. It is sold for five "
        "thousand four hundred rupees. Find the total cost price, the profit, "
        "and the profit percent. <bookmark mark='b2'/> Second: two television "
        "sets are each sold for nine thousand nine hundred rupees. <bookmark "
        "mark='b3'/> One gives a profit of ten percent, and the other gives a "
        "loss of ten percent. Did the plus ten and the minus ten cancel?"
    ),
    "s9a": (
        "Let us check. <bookmark mark='b0'/> For the bicycle, the overheads are "
        "two hundred plus three hundred, so the total cost price is four "
        "thousand five hundred rupees. <bookmark mark='b1'/> The profit is five "
        "thousand four hundred minus four thousand five hundred, that is nine "
        "hundred rupees, and the profit percent is nine hundred divided by four "
        "thousand five hundred, times one hundred, which is twenty percent. "
        "<bookmark mark='b2'/> For the television sets, the first cost price is "
        "nine thousand nine hundred divided by one point one, that is nine "
        "thousand rupees. <bookmark mark='b3'/> The second cost price is nine "
        "thousand nine hundred divided by zero point nine, that is eleven "
        "thousand rupees. The total cost price is twenty thousand rupees and "
        "the total selling price is nineteen thousand eight hundred, so there "
        "is a loss of two hundred rupees, which is one percent. The plus ten "
        "and the minus ten did not cancel."
    ),
    "s10": (
        "Let us put it together. <bookmark mark='b0'/> First add the overheads "
        "to the purchase price. <bookmark mark='b1'/> Then compare the total "
        "cost price with the selling price. <bookmark mark='b2'/> Take the "
        "percentage on the cost price, never on the selling price. <bookmark "
        "mark='b3'/> And for several items, compare the total cost with the "
        "total selling price. <bookmark mark='b4'/> The purchase price alone "
        "is never the real cost. <bookmark mark='b5'/> Thank you for watching, "
        "<bookmark mark='b6'/> and see you in the next lesson."
    ),
}
NARRATION = {"intro": INTRO_NARRATION, **NARRATION}


def ledger_row(text, color=CHALK_WHITE, w=4.5, h=0.62, size=26):
    box = panel(w, h, color, opacity=0.5, radius=0.10, stroke=2.0)
    t = T(text, size, color, max_w=w - 0.3)
    t.move_to(box)
    g = VGroup(box, t)
    g.box = box
    return g


class ProfitLossOverheadExpensesAndTransactionsStory(Ch5Scene):
    NARRATION = NARRATION
    TEXT_SCALE = 0.85     # medium type
    TIGHT_BOXES = True    # every box hugs its text
    STRICT_BOXES = True   # audit: boxes stay on the board with a gap between them
    AVOID_ART = True      # text/cards never sit on the teacher, students or badges
    INTRO_LINES = ('Profit, Loss', '& Overhead Expenses')
    INTRO_SUB = 'Single and Double Transaction Problems'
    BEATS = ("intro", "title", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9",
             "s10")

    # -- 0 -----------------------------------------------------------------
    def beat_title(self):
        with self.narrate("title") as tr:
            self.heading("Profit, Loss & Overheads",
                         "The purchase price is not the real cost.")
            c1 = part_card(fridge(1.9), "BOUGHT", ["Rs 5,000"], CHALK_CYAN,
                           w=3.1, h=2.35, icon_h=1.35)
            c2 = part_card(truck(2.3), "TRANSPORT", ["Rs 100"], CHALK_AMBER,
                           w=3.1, h=2.35, icon_h=1.35)
            c3 = part_card(wrench(2.2), "REPAIRS", ["Rs 500"], CHALK_PINK,
                           w=3.1, h=2.35, icon_h=1.35)
            for c, dx in zip((c1, c2, c3), (-3.33, 0, 3.33)):
                P(c, CX + dx, 0.48)
            tot = P(calc_row("", "COST", r"5000+100+500=\text{Rs }5{,}600",
                             CHALK_YELLOW, w=9.6, h=0.8, math_size=40),
                    CX, -1.15)
            prof = P(calc_row("", "SOLD", r"7000-5600=\text{Rs }1{,}400",
                              CHALK_GREEN, w=6.2, h=0.85, math_size=38),
                     CX - 1.65, -2.10)
            nope = P(mistake_card("Rs 2,000", "not this", w=3.0, h=0.95,
                                  size=26), 3.85, -2.10)
            tidy(c1, c2, c3, same=True)  # auto-tidy
            self.cue(tr, "b0", c1, sfx="pop")
            self.cue(tr, "b1", c2)
            self.cue(tr, "b2", c3)
            self.cue(tr, "b3", tot, sfx="ding")
            self.cue(tr, "b4", prof)
            self.cue(tr, "b5", nope, sfx="click")
            self.finish(tr)

    # -- 1: profit / loss / neither -----------------------------------------
    def beat_s1(self):
        with self.narrate("s1") as tr:
            self.heading("Profit, Loss or Neither?")
            bal = balance(10, "CP 500", "SP 650")
            fit(bal, 4.5, 3.3)
            P(bal, -2.05, 0.30)
            bal_loss = balance(-10, "CP 500", "SP 450")
            fit(bal_loss, 4.5, 3.3).move_to(bal.get_center())
            bal_same = balance(0, "CP 500", "SP 500")
            fit(bal_same, 4.5, 3.3).move_to(bal.get_center())
            o1 = P(calc_row("", "PROFIT", r"650-500=\text{Rs }150", CHALK_GREEN,
                            w=4.8, h=0.85, math_size=36), 3.05, 1.40)
            o2 = P(calc_row("", "LOSS", r"500-450=\text{Rs }50", CHALK_RED,
                            w=4.8, h=0.85, math_size=36), 3.05, 0.40)
            o3 = P(calc_row("", "NEITHER", r"\text{SP}=\text{CP}", CHALK_CYAN,
                            w=4.8, h=0.85, math_size=36), 3.05, -0.60)
            f1 = VGroup(panel(4.7, 0.9, CHALK_GREEN),
                        M(r"\text{Profit}=\text{SP}-\text{CP}", 38,
                          CHALK_GREEN))
            f1[1].move_to(f1[0])
            f2 = VGroup(panel(4.7, 0.9, CHALK_RED),
                        M(r"\text{Loss}=\text{CP}-\text{SP}", 38, CHALK_RED))
            f2[1].move_to(f2[0])
            hrow(f1, f2, y=-1.65, gap=0.35)
            strip = P(T("Ask which is bigger before you subtract.", 26,
                        CHALK_WHITE), CX, -2.42)
            tidy(o1, o2, o3, same=True)  # auto-tidy
            self.cue(tr, "b0", bal, o1, sfx="pop")
            self.cue(tr, "b1", Transform(bal, bal_loss), o2, sfx="click",
                     rt=0.9)
            self.cue(tr, "b2", Transform(bal, bal_same), o3, rt=0.9)
            self.cue(tr, "b3", f1, f2, sfx="ding")
            self.cue(tr, "b4", strip, sfx="success")
            self.finish(tr)

    # -- 2: percentage -------------------------------------------------------
    def beat_s2(self):
        with self.narrate("s2") as tr:
            self.heading("Profit and Loss Percent")
            cp = segbar(5.0, [(1.0, CHALK_AMBER, "COST PRICE = Rs 500")],
                        h=0.85, size=26)
            pf = segbar(1.5, [(1.0, CHALK_GREEN, "Rs 150")], h=0.85, size=26)
            left = CX - 6.5 / 2
            P(cp, left + 2.5, 1.05)
            P(pf, left + 5.0 + 0.75, 1.05)
            br = brace_label(cp, "100% = the cost price", UP, size=24,
                             color=CHALK_AMBER)
            r1 = P(calc_row("", "PROFIT %", r"\frac{150}{500}\times100=30\%",
                            CHALK_GREEN, w=9.6, h=1.0, math_size=40), CX,
                   0.00)
            f1 = VGroup(panel(4.8, 0.95, CHALK_GREEN),
                        M(r"\text{Profit}\%=\frac{\text{Profit}}{\text{CP}}"
                          r"\times100", 34, CHALK_GREEN))
            f1[1].move_to(f1[0])
            f2 = VGroup(panel(4.8, 0.95, CHALK_RED),
                        M(r"\text{Loss}\%=\frac{\text{Loss}}{\text{CP}}"
                          r"\times100", 34, CHALK_RED))
            f2[1].move_to(f2[0])
            hrow(f1, f2, y=-1.00, gap=0.35)
            base = P(chip("BASE = COST PRICE", CHALK_PINK, 28, w=4.8),
                     CX - 2.5, -2.04)
            bad = P(mistake_card("% = Profit / SP", "divide by the CP",
                                 w=4.8, h=0.95, size=20), CX + 2.5, -2.04)
            self.cue(tr, "b0", cp, pf, br, r1, sfx="pop")
            self.cue(tr, "b1", f1)
            self.cue(tr, "b2", f2)
            self.cue(tr, "b3", base, sfx="ding")
            self.cue(tr, "b4", bad, sfx="click")
            self.finish(tr)

    # -- ledger helper ---------------------------------------------------------
    def _ledger_frame(self):
        out = VGroup(panel(4.7, 3.6, CHALK_PINK, opacity=0.35),
                     T("MONEY OUT", 28, CHALK_PINK))
        out[1].move_to(out[0].get_top() + DOWN * 0.38)
        inn = VGroup(panel(4.7, 3.6, CHALK_GREEN, opacity=0.35),
                     T("MONEY IN", 28, CHALK_GREEN))
        inn[1].move_to(inn[0].get_top() + DOWN * 0.38)
        P(out, CX - 2.5, 0.28)
        P(inn, CX + 2.5, 0.28)
        return out, inn

    # -- 3: refrigerator ledger ---------------------------------------------------
    def beat_s3(self):
        with self.narrate("s3") as tr:
            self.heading("The Refrigerator Ledger")
            out, inn = self._ledger_frame()
            x0 = out[0].get_center()[0]
            rows = [ledger_row("Purchase  Rs 5,000", CHALK_WHITE),
                    ledger_row("+ Transport  Rs 100", CHALK_AMBER),
                    ledger_row("+ Repairs  Rs 500", CHALK_PINK)]
            for r, y in zip(rows, (1.00, 0.33, -0.34)):
                P(r, x0, y)
            total = VGroup(panel(4.4, 0.75, CHALK_YELLOW, opacity=0.9),
                           T("COST PRICE  Rs 5,600", 28, CHALK_YELLOW,
                             max_w=4.1))
            total[1].move_to(total[0])
            P(total, x0, -1.05)
            x1 = inn[0].get_center()[0]
            sp = P(ledger_row("Sold  Rs 7,000", CHALK_GREEN), x1, 1.00)
            profit = P(calc_row("", "", r"7000-5600=\text{Rs }1{,}400",
                                CHALK_GREEN, w=4.4, h=0.75, math_size=34),
                       x1, 0.30)
            fr = P(fridge(1.3), x1, -0.78)
            pct = P(calc_row("", "PROFIT %", r"\frac{1400}{5600}\times100=25\%",
                             CHALK_YELLOW, w=9.6, h=0.95, math_size=40), CX,
                    -2.12)
            tidy(*rows, same=True)  # auto-tidy
            self.cue(tr, "b0", out, inn, rows[0], sfx="pop")
            self.cue(tr, "b1", rows[1])
            self.cue(tr, "b2", rows[2])
            self.cue(tr, "b3", total, sfx="ding")
            self.cue(tr, "b4", sp, fr, profit)
            self.cue(tr, "b5", pct, sfx="success")
            self.finish(tr)

    # -- 4: the flat ----------------------------------------------------------------
    def beat_s4(self):
        with self.narrate("s4") as tr:
            self.heading("The Flat: a Loss")
            out, inn = self._ledger_frame()
            x0 = out[0].get_center()[0]
            rows = [ledger_row("Bought  Rs 4,50,000", CHALK_WHITE),
                    ledger_row("+ Repairs  Rs 10,000", CHALK_AMBER)]
            P(rows[0], x0, 1.00)
            P(rows[1], x0, 0.33)
            total = VGroup(panel(4.4, 0.75, CHALK_YELLOW, opacity=0.9),
                           T("COST  Rs 4,60,000", 28, CHALK_YELLOW,
                             max_w=4.1))
            total[1].move_to(total[0])
            P(total, x0, -1.05)
            x1 = inn[0].get_center()[0]
            sp = P(ledger_row("Sold  Rs 4,25,500", CHALK_GREEN), x1, 1.00)
            loss = P(ledger_row("Loss  Rs 34,500", CHALK_RED, size=28), x1,
                     0.30)
            smaller = P(T("SP is smaller than CP", 26, CHALK_RED), x1, -0.28)
            bd = P(building(0.75), x1, -1.02)
            pct = P(calc_row("", "LOSS %", r"\frac{34500}{460000}\times100=7.5\%",
                             CHALK_RED, w=9.6, h=0.95, math_size=40), CX, -2.12)
            self.cue(tr, "b0", out, inn, rows[0], sfx="pop")
            self.cue(tr, "b1", rows[1])
            self.cue(tr, "b2", total, sfx="ding")
            self.cue(tr, "b3", sp, smaller, bd)
            self.cue(tr, "b4", loss)
            self.cue(tr, "b5", pct, sfx="success")
            self.finish(tr)

    # -- 5: the two-table trap ------------------------------------------------------------
    def beat_s5(self):
        with self.narrate("s5") as tr:
            self.heading("The Two-Table Trap")

            def side(color, tcol, top, bot):
                box = panel(4.7, 2.25, color)
                tb = VGroup(table_icon(1.8), T("SP Rs 3,000", 28,
                                               CHALK_WHITE)).arrange(DOWN,
                                                                    buff=0.2)
                tb.move_to(box.get_center() + LEFT * 0.95)
                st = sticker(top, bot, r=0.80, size=30, color=tcol)
                st.move_to(box.get_center() + RIGHT * 1.45)
                return VGroup(box, tb), st
            cA, sA = side(CHALK_GREEN, CHALK_GREEN, "+20%", "GAIN")
            cB, sB = side(CHALK_RED, CHALK_RED, "-20%", "LOSS")
            P(cA, CX - 2.55, 0.95)
            P(cB, CX + 2.55, 0.95)
            sA.move_to(cA[0].get_center() + RIGHT * 1.45)
            sB.move_to(cB[0].get_center() + RIGHT * 1.45)
            tmp = P(chip("+20% and -20% = 0%  ???", CHALK_PINK, 28), CX, -0.50)
            x = cross_mark(tmp.get_right() + RIGHT * 0.45, 0.28, CHALK_RED, 7)
            r1 = P(calc_row("", "COST 1", r"\frac{3000}{1.2}=\text{Rs }2500",
                            CHALK_GREEN, w=4.7, h=0.95, math_size=34),
                   CX - 2.55, -1.55)
            r2 = P(calc_row("", "COST 2", r"\frac{3000}{0.8}=\text{Rs }3750",
                            CHALK_RED, w=4.7, h=0.95, math_size=34),
                   CX + 2.55, -1.55)
            strip = P(T("The two bases are different.", 26, CHALK_WHITE),
                      CX, -2.36)
            tidy(r1, r2, same=True)  # auto-tidy
            self.cue(tr, "b0", cA, cB, sfx="pop")
            self.cue(tr, "b1", sA)
            self.cue(tr, "b2", sB)
            self.cue(tr, "b3", tmp, x, sfx="click")
            self.cue(tr, "b4", r1)
            self.cue(tr, "b5", r2, strip, sfx="success")
            self.finish(tr)

    # -- 6: whole transaction -------------------------------------------------------------------
    def beat_s6(self):
        with self.narrate("s6") as tr:
            self.heading("The Whole Transaction")
            lvl = balance(0, "CP 6,250", "SP 6,250")
            fit(lvl, 4.4, 3.3)
            P(lvl, -2.15, 0.15)
            tip = balance(-9, "CP 6,250", "SP 6,000")
            fit(tip, 4.4, 3.3).move_to(lvl.get_center())
            r1 = P(calc_row("1", "COST", r"2500+3750=6250", CHALK_AMBER,
                            w=5.2, h=0.85, math_size=38), 3.0, 1.40)
            r2 = P(calc_row("2", "SOLD", r"3000+3000=6000", CHALK_CYAN,
                            w=5.2, h=0.85, math_size=38), 3.0, 0.40)
            lossc = P(chip("LOSS OF Rs 250", CHALK_RED, 30, w=5.2), 3.0,
                      -0.55)
            r3 = P(calc_row("", "LOSS %", r"\frac{250}{6250}\times100=4\%",
                            CHALK_YELLOW, w=5.2, h=1.0, math_size=36), 3.0,
                   -1.55)
            strip = P(T("+20% and -20% did not give 0%.", 26, CHALK_WHITE),
                      CX, -2.40)
            tidy(r1, r2, r3, same=True)  # auto-tidy
            self.cue(tr, "b0", lvl, r1, sfx="pop")
            self.cue(tr, "b1", r2)
            self.cue(tr, "b2", Transform(lvl, tip), lossc, sfx="click", rt=0.9)
            self.cue(tr, "b3", r3, sfx="ding")
            self.cue(tr, "b4", strip, sfx="success")
            self.finish(tr)

    # -- 7: five steps ------------------------------------------------------------------------------
    def beat_s7(self):
        with self.narrate("s7") as tr:
            self.heading("The Decision Process")
            specs = [("1", "PURCHASE PRICE", "find it", CHALK_CYAN),
                     ("2", "OVERHEADS", "add: total CP", CHALK_AMBER),
                     ("3", "SELLING PRICE", "find total SP", CHALK_GREEN),
                     ("4", "COMPARE", "SP bigger: profit", CHALK_PINK),
                     ("5", "PERCENT", "divide by CP, x 100", CHALK_YELLOW)]
            rows = [step_row(*s, h=0.74, size=26) for s in specs]
            for r, y in zip(rows, (1.70, 0.84, -0.02, -0.88, -1.74)):
                P(r, CX, y)
            strip = P(T("Several items: total CP against total SP.", 26,
                        CHALK_WHITE, max_w=9.6), CX, -2.35)
            tidy(*rows, same=True)  # auto-tidy
            for k, r in enumerate(rows):
                self.cue(tr, f"b{k}", r, sfx="pop" if k == 0 else "click")
            self.cue(tr, "b5", strip, sfx="success")
            self.finish(tr)

    # -- 8: bananas ------------------------------------------------------------------------------------
    def beat_s8(self):
        with self.narrate("s8") as tr:
            self.heading("Spoiled Stock Still Costs")
            ban = P(bananas(2.8), -2.9, 1.15)
            tr_ = P(truck(2.2), -2.9, -0.55)
            r1 = P(calc_row("1", "COST", r"1250+250=1500", CHALK_AMBER, w=6.0,
                            h=0.85, math_size=40), 2.35, 1.45)
            r2 = P(calc_row("2", "SOLD", r"\text{Rs }1575", CHALK_CYAN, w=6.0,
                            h=0.85, math_size=40), 2.35, 0.50)
            spoil = P(chip("SPOILED STOCK STILL COSTS", CHALK_RED, 26, w=6.0),
                      2.35, -0.40)
            r3 = P(calc_row("3", "PROFIT", r"1575-1500=75\ (5\%)",
                            CHALK_GREEN, w=6.0, h=0.85, math_size=40), 2.35,
                   -1.40)
            strip = P(T("Overheads count even when stock is lost.", 26,
                        CHALK_WHITE), CX, -2.35)
            tidy(r1, r2, r3, same=True)  # auto-tidy
            self.cue(tr, "b0", ban, sfx="pop")
            self.cue(tr, "b1", tr_, r1)
            self.cue(tr, "b2", r2)
            self.cue(tr, "b3", spoil, sfx="click")
            self.cue(tr, "b4", r3, strip, sfx="success")
            self.finish(tr)

    # -- 9: your turn -------------------------------------------------------------------------------------
    def beat_s9(self):
        with self.narrate("s9q") as tr:
            self.heading("YOUR TURN", "Two problems.", CHALK_PINK)
            q1 = q_card(bicycle(2.0), "1  BICYCLE",
                        ["Rs 4000 + 200 + 300 = cost", "sold Rs 5400: profit, %"],
                        CHALK_CYAN, w=9.6, h=1.5)
            q2 = q_card(tv(1.5), "2  TWO TVs",
                        ["each sold Rs 9900", "+10% on one, -10% on the other",
                         "do they cancel?"], CHALK_AMBER, w=9.6, h=1.75)
            P(q1, CX, 0.85)
            P(q2, CX, -0.95)
            tidy(q1, q2, same=True)  # auto-tidy
            self.cue(tr, "b0", q1, sfx="pop")
            self.cue(tr, "b2", q2)
            self.finish(tr)
            self._qs = (q1, q2)
        self.think_clock()
        with self.narrate("s9a", reset=False) as tr:
            a1 = P(calc_row("1", "CP", r"4000+200+300=\text{Rs }4500",
                            CHALK_CYAN, w=9.6, h=0.85, math_size=40), CX, 1.20)
            a2 = P(calc_row("1", "PROFIT", r"900,\ \ \frac{900}{4500}\times"
                            r"100=20\%", CHALK_GREEN, w=9.6, h=1.0,
                            math_size=38), CX, 0.20)
            a3 = P(calc_row("2", "COSTS", r"\frac{9900}{1.1}=9000,\ \ "
                            r"\frac{9900}{0.9}=11000", CHALK_AMBER, w=9.6,
                            h=1.0, math_size=36), CX, -0.85)
            a4 = P(calc_row("2", "TOTAL", r"20000\ \text{vs}\ 19800:\ "
                            r"\text{loss }1\%", CHALK_RED, w=9.6, h=0.85,
                            math_size=38), CX, -1.85)
            q1, q2 = self._qs
            tidy(a1, a2, a3, a4, same=True)  # auto-tidy
            self.cue(tr, "b0", FadeOut(q1), FadeOut(q2), FadeIn(a1),
                     sfx="click", rt=0.6)
            self.cue(tr, "b1", a2)
            self.cue(tr, "b2", a3)
            self.cue(tr, "b3", a4, sfx="success")
            self.finish(tr)

    # -- 10 ----------------------------------------------------------------------------------------------------
    def beat_s10(self):
        with self.narrate("s10") as tr:
            head = self.heading("Overheads, Compare, Percentage")
            rows = [
                step_row("1", "OVERHEADS", "add to the purchase price",
                         CHALK_AMBER, h=0.88),
                step_row("2", "COMPARE", "total CP with SP", CHALK_CYAN,
                         h=0.88),
                step_row("3", "PERCENT", "always on the CP", CHALK_GREEN,
                         h=0.88),
                step_row("4", "SEVERAL ITEMS", "total CP, total SP", CHALK_PINK,
                         h=0.88),
            ]
            for r, y in zip(rows, (1.60, 0.62, -0.36, -1.34)):
                P(r, CX, y)
            strip = P(T("The purchase price alone is never the real cost.",
                        26, CHALK_YELLOW, max_w=9.6), CX, -2.30)
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

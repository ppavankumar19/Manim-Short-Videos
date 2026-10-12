"""
Compound Ratio & Inverse Ratio: Applications in Business Profit Sharing
Story-mode chalkboard lesson (Class 8 Maths, Chapter 5: Comparing Quantities
using Proportion).

LLM KEY / FUNCTION NAME: compound_ratio_and_business_proportions

Layout re-done for legibility: big chalk type inside the green board; the two
partners are drawn figures (human_figure.Man) with money bags and time pies
(12 months = a full circle, 9 months = three quarters), ratios are shown as
counted tiles, the profit is cut into 17 equal blocks.

Title + 10 scenes:
  0. Ramayya (Rs 2,000, 12 months) and Gopalam (Rs 3,000, 9 months).
  1. A ratio is ordered; the inverse swaps the terms.
  2. Same time: profit follows the capital ratio 2 : 3.
  3. Same capital: profit follows the time ratio 4 : 3.
  4. Both different: the two ratios must be combined.
  5. Compound ratio rule: ac : bd (never a+c : b+d).
  6. (2 : 3) with (4 : 3) gives 8 : 9, cross-checked with money x time.
  7. From ratio to rupees: Rs 17,000 in 17 parts of Rs 1,000.
  8. The decision rule.
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
    "Compound ratio and inverse ratio. <bookmark mark='b0'/> Applications in "
    "business profit sharing."
)
NARRATION = {
    "title": (
        "Meet two partners. <bookmark mark='b0'/>Ramayya invests two thousand "
        "rupees, and keeps that money in the business for twelve months. "
        "<bookmark mark='b1'/>Gopalam invests three thousand rupees for nine "
        "months. <bookmark mark='b2'/>At the end of the year the business earns "
        "a profit. <bookmark mark='b3'/>Should the two partners share that "
        "profit equally? <bookmark mark='b4'/>No. Profit in a partnership is "
        "shared in the ratio of what each partner contributed."
    ),
    "s1": (
        "A ratio is an ordered comparison. <bookmark mark='b0'/>Three to two is "
        "not the same as two to three. <bookmark mark='b1'/>The order of the "
        "two terms matters. <bookmark mark='b2'/>If we swap the two terms of a "
        "ratio, we get its inverse ratio: a to b becomes b to a. <bookmark "
        "mark='b3'/>So the inverse of four to five is five to four. <bookmark "
        "mark='b4'/>Inverse means swap the terms. It never means add them, and "
        "it never means change their signs."
    ),
    "s2": (
        "Now suppose both partners keep their money in for the same time. "
        "<bookmark mark='b0'/>Ramayya invests two thousand rupees for twelve "
        "months. <bookmark mark='b1'/>Gopalam also invests for twelve months, "
        "but he puts in three thousand rupees. <bookmark mark='b2'/>The time is "
        "the same for both, so the time factor cancels. <bookmark mark='b3'/>The "
        "capitals are in the ratio two thousand to three thousand, which "
        "simplifies to two to three. <bookmark mark='b4'/>So the profit is "
        "divided in the ratio two to three."
    ),
    "s3": (
        "Now suppose both partners invest the same capital. <bookmark "
        "mark='b0'/>Each of them invests five thousand rupees. <bookmark "
        "mark='b1'/>But Ramayya keeps his money in for twelve months, while "
        "Gopalam keeps his in for only nine months. <bookmark mark='b2'/>The "
        "capital is the same for both, so the capital factor cancels. <bookmark "
        "mark='b3'/>The times are in the ratio twelve to nine, and that "
        "simplifies to four to three. <bookmark mark='b4'/>So here the profit "
        "follows the time ratio, four to three."
    ),
    "s4": (
        "But in our business, both the money and the time are different. "
        "<bookmark mark='b0'/>Ramayya gives two thousand rupees for twelve "
        "months. <bookmark mark='b1'/>Gopalam gives three thousand rupees for "
        "nine months. <bookmark mark='b2'/>The capital ratio is two to three. "
        "<bookmark mark='b3'/>The time ratio is twelve to nine, that is four to "
        "three. <bookmark mark='b4'/>Neither ratio alone can decide the profit, "
        "so the two ratios must be combined."
    ),
    "s5": (
        "To combine two ratios we use the compound ratio. <bookmark "
        "mark='b0'/>For the ratios a to b and c to d, multiply the first terms "
        "together, <bookmark mark='b1'/>and multiply the second terms together. "
        "<bookmark mark='b2'/>The compound ratio is a times c to b times d. "
        "<bookmark mark='b3'/>A common mistake is to add the terms instead, and "
        "write a plus c to b plus d. <bookmark mark='b4'/>That is wrong. A "
        "compound ratio multiplies corresponding terms; it never adds them."
    ),
    "s6": (
        "Let us apply the rule. <bookmark mark='b0'/>We multiply the capital "
        "ratio two to three <bookmark mark='b1'/>by the time ratio four to "
        "three. <bookmark mark='b2'/>Two times four is eight, and three times "
        "three is nine, so the compound ratio is eight to nine. <bookmark "
        "mark='b3'/>Let us cross-check with money multiplied by time. Two "
        "thousand times twelve is twenty four thousand, and three thousand times "
        "nine is twenty seven thousand. <bookmark mark='b4'/>Twenty four "
        "thousand to twenty seven thousand simplifies to eight to nine, so the "
        "compound ratio is correct."
    ),
    "s7": (
        "Now let us turn that ratio into rupees. <bookmark mark='b0'/>Suppose "
        "the profit for the year is seventeen thousand rupees. This total is an "
        "example, not a textbook figure. <bookmark mark='b1'/>The ratio is eight "
        "to nine, so the profit is divided into eight plus nine, that is "
        "seventeen, equal parts. <bookmark mark='b2'/>Seventeen thousand divided "
        "by seventeen gives one thousand rupees for each part. <bookmark "
        "mark='b3'/>Ramayya takes eight parts, that is eight thousand rupees. "
        "<bookmark mark='b4'/>Gopalam takes nine parts, that is nine thousand "
        "rupees, and eight thousand plus nine thousand is seventeen thousand. "
        "The whole profit is shared."
    ),
    "s8": (
        "Here is the decision rule to remember. <bookmark mark='b0'/>If the "
        "time is the same, share the profit in the ratio of the capitals. "
        "<bookmark mark='b1'/>If the capital is the same, share it in the ratio "
        "of the times. <bookmark mark='b2'/>If both the capital and the time are "
        "different, share it in the compound ratio of capital and time. "
        "<bookmark mark='b3'/>So the share of the profit follows capital "
        "multiplied by time."
    ),
    "s9q": (
        "Your turn. Four quick checks. <bookmark mark='b0'/>First: write the "
        "inverse of the ratio seven to five. <bookmark mark='b1'/>Second: find "
        "the compound ratio of three to four and two to three. <bookmark "
        "mark='b2'/>Third: compound three to four with the inverse of four to "
        "five. <bookmark mark='b3'/>And last: partner P invests four thousand "
        "rupees for six months, and partner Q invests three thousand rupees for "
        "eight months. In what ratio should they share the profit?"
    ),
    "s9a": (
        "<bookmark mark='b0'/>The inverse of seven to five is five to seven, "
        "because the inverse swaps the two terms. <bookmark mark='b1'/>The "
        "compound ratio of three to four and two to three is six to twelve, "
        "which simplifies to one to two. <bookmark mark='b2'/>Three to four, "
        "compounded with the inverse of four to five, is three times five to "
        "four times four, that is fifteen to sixteen. <bookmark mark='b3'/>And "
        "for P and Q, four thousand times six is twenty four thousand, and three "
        "thousand times eight is also twenty four thousand. So the ratio is one "
        "to one, and the two partners share the profit equally."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>The inverse ratio swaps the two "
        "terms: a to b becomes b to a. <bookmark mark='b1'/>The compound ratio "
        "multiplies corresponding terms: a to b and c to d give a times c to b "
        "times d. <bookmark mark='b2'/>In a partnership, a partner's share "
        "follows capital multiplied by time. <bookmark mark='b3'/>And when the "
        "profit is known, divide it into equal parts using the ratio. <bookmark "
        "mark='b4'/>Money and time together decide the share. <bookmark "
        "mark='b5'/>Thank you for watching, <bookmark mark='b6'/>and see you in "
        "the next lesson."
    ),
}
NARRATION = {"intro": INTRO_NARRATION, **NARRATION}

RAM = "#4F8EF7"
GOP = "#F0A23C"


def partner_card(name, amount, months, color, shirt, facing, w=4.7, h=2.55,
                 months_frac=None):
    """Man + money bag + time pie + the facts."""
    box = panel(w, h, color)
    man = person(ORIGIN, 2.0, facing, shirt)
    man.move_to(box.get_center() + LEFT * 1.6)
    frac = months_frac if months_frac is not None else months / 12.0
    bag = money_bag(0.9, label="Rs")
    pie_ = pie(frac, 0.42, color)
    icons = VGroup(bag, pie_).arrange(RIGHT, buff=0.25)
    txt = VGroup(T(name, 30, color), T(amount, 26, CHALK_WHITE),
                 T(f"{months} months", 26, CHALK_WHITE)).arrange(
        DOWN, buff=0.10, aligned_edge=LEFT)
    right = VGroup(txt, icons).arrange(DOWN, buff=0.18)
    fit(right, 2.75, h - 0.3)
    right.move_to(box.get_center() + RIGHT * 0.95)
    g = VGroup(box, man, right)
    g.box = box
    return g


def fact_card(name, amount, months, color, w=4.7, h=2.1, frac=None):
    """Compact card: bag + pie + the facts (no figure)."""
    box = panel(w, h, color)
    bag = money_bag(1.0, label="Rs")
    pie_ = pie(frac if frac is not None else months / 12.0, 0.5, color)
    icons = VGroup(bag, pie_).arrange(DOWN, buff=0.20)
    txt = VGroup(T(name, 30, color), T(amount, 28, CHALK_WHITE),
                 T(f"{months} months", 28, CHALK_WHITE)).arrange(
        DOWN, buff=0.10, aligned_edge=LEFT)
    both = VGroup(icons, txt).arrange(RIGHT, buff=0.35)
    fit(both, w - 0.4, h - 0.25)
    both.move_to(box)
    g = VGroup(box, both)
    g.box = box
    return g


def share_bar(a, b, y, w=8.4, ca=CHALK_CYAN, cb=CHALK_AMBER, la="RAMAYYA",
              lb="GOPALAM"):
    tot = a + b
    bar = segbar(w, [(a / tot, ca, f"{la}  {a}"), (b / tot, cb, f"{lb}  {b}")],
                 h=0.7, size=26)
    return P(bar, CX, y)


class CompoundRatioAndBusinessProportionsStory(Ch5Scene):
    NARRATION = NARRATION
    TEXT_SCALE = 0.85     # medium type
    TIGHT_BOXES = True    # every box hugs its text
    STRICT_BOXES = True   # audit: boxes stay on the board with a gap between them
    AVOID_ART = True      # text/cards never sit on the teacher, students or badges
    INTRO_LINES = ("Compound Ratio", "& Inverse Ratio")
    INTRO_SUB = "Applications in Business Profit Sharing"
    BEATS = ("intro", "title", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9",
             "s10")

    # -- 0 -----------------------------------------------------------------
    def beat_title(self):
        with self.narrate("title") as tr:
            self.heading("Business Profit Sharing")
            a = partner_card("RAMAYYA", "Rs 2,000", 12, CHALK_CYAN, RAM, RIGHT, h=2.30)
            b = partner_card("GOPALAM", "Rs 3,000", 9, CHALK_AMBER, GOP, LEFT, h=2.30)
            P(a, CX - 2.55, 0.98)
            P(b, CX + 2.55, 0.98)
            prof = P(icon_chip(money_bag(0.9), "PROFIT AT THE YEAR END",
                               CHALK_GREEN, w=9.6, h=0.85, size=28), CX, -1.00)
            ques = P(T("SHARE IT EQUALLY?", 40, CHALK_PINK), CX, -1.82)
            strip = P(T("Share by what each partner put in.", 28,
                        CHALK_YELLOW), CX, -2.44)
            tidy(a, b, same=True)  # auto-tidy
            self.cue(tr, "b0", a, sfx="pop")
            self.cue(tr, "b1", b)
            self.cue(tr, "b2", prof, sfx="click")
            self.cue(tr, "b3", ques, sfx="ding")
            self.cue(tr, "b4", strip, sfx="success")
            self.finish(tr)

    # -- 1: ordered ratio and inverse --------------------------------------------
    def beat_s1(self):
        with self.narrate("s1") as tr:
            self.heading("A Ratio Is Ordered")

            def rcard(a, b, color):
                box = panel(3.7, 2.2, color)
                t = M(rf"{a}:{b}", 60, color)
                tl = tiles(a, b, 0.34)
                col = VGroup(t, tl).arrange(DOWN, buff=0.22)
                col.move_to(box)
                return VGroup(box, col)
            c1 = rcard(3, 2, CHALK_CYAN)
            c2 = rcard(2, 3, CHALK_AMBER)
            P(c1, CX - 2.3, 0.95)
            P(c2, CX + 2.3, 0.95)
            ne = P(M(r"\neq", 70, CHALK_PINK), CX, 0.95)
            sw = P(M(r"a:b\ \longrightarrow\ b:a", 54, CHALK_YELLOW), CX, -0.75)
            ex = P(chip("INVERSE OF 4 : 5  IS  5 : 4", CHALK_GREEN, 30, w=7.2),
                   CX, -1.65)
            strip = P(T("Inverse = swap. Never add, never change signs.", 26,
                        CHALK_WHITE, max_w=9.6), CX, -2.40)
            self.cue(tr, "b0", c1, c2, ne, sfx="pop")
            self.cue(tr, "b1", Indicate(c1, color=CHALK_CYAN,
                                        scale_factor=1.04), sfx=None)
            self.cue(tr, "b2", sw, sfx="ding")
            self.cue(tr, "b3", ex)
            self.cue(tr, "b4", strip, sfx="success")
            self.finish(tr)

    # -- 2: same time ------------------------------------------------------------------
    def beat_s2(self):
        with self.narrate("s2") as tr:
            self.heading("Same Time: Share by Capital")
            a = fact_card("RAMAYYA", "Rs 2,000", 12, CHALK_CYAN)
            b = fact_card("GOPALAM", "Rs 3,000", 12, CHALK_AMBER)
            P(a, CX - 2.55, 0.95)
            P(b, CX + 2.55, 0.95)
            cancel = P(chip("TIME IS THE SAME: IT CANCELS", CHALK_PINK, 28),
                       CX, -0.45)
            r1 = P(calc_row("", "CAPITALS", r"2000:3000=2:3", CHALK_YELLOW,
                            w=9.6, h=0.85, math_size=44), CX, -1.30)
            bar = share_bar(2, 3, -2.12)
            tidy(a, b, same=True)  # auto-tidy
            self.cue(tr, "b0", a, sfx="pop")
            self.cue(tr, "b1", b)
            self.cue(tr, "b2", cancel, sfx="click")
            self.cue(tr, "b3", r1, sfx="ding")
            self.cue(tr, "b4", bar, sfx="success")
            self.finish(tr)

    # -- 3: same capital ------------------------------------------------------------------
    def beat_s3(self):
        with self.narrate("s3") as tr:
            self.heading("Same Capital: Share by Time")
            a = fact_card("RAMAYYA", "Rs 5,000", 12, CHALK_CYAN)
            b = fact_card("GOPALAM", "Rs 5,000", 9, CHALK_AMBER)
            P(a, CX - 2.55, 0.95)
            P(b, CX + 2.55, 0.95)
            cancel = P(chip("CAPITAL IS THE SAME: IT CANCELS", CHALK_PINK, 28),
                       CX, -0.45)
            r1 = P(calc_row("", "TIMES", r"12:9=4:3", CHALK_YELLOW, w=9.6,
                            h=0.85, math_size=44), CX, -1.30)
            bar = share_bar(4, 3, -2.12)
            tidy(a, b, same=True)  # auto-tidy
            self.cue(tr, "b0", a, sfx="pop")
            self.cue(tr, "b1", b)
            self.cue(tr, "b2", cancel, sfx="click")
            self.cue(tr, "b3", r1, sfx="ding")
            self.cue(tr, "b4", bar, sfx="success")
            self.finish(tr)

    # -- 4: both different -----------------------------------------------------------------
    def beat_s4(self):
        with self.narrate("s4") as tr:
            self.heading("Both Are Different")
            a = fact_card("RAMAYYA", "Rs 2,000", 12, CHALK_CYAN)
            b = fact_card("GOPALAM", "Rs 3,000", 9, CHALK_AMBER)
            P(a, CX - 2.55, 0.95)
            P(b, CX + 2.55, 0.95)
            cap = P(chip("CAPITAL  2 : 3", CHALK_GREEN, 30, w=4.7), CX - 2.55,
                    -0.55)
            tim = P(chip("TIME  12 : 9 = 4 : 3", CHALK_AMBER, 30, w=4.7),
                    CX + 2.55, -0.55)
            a1 = Arrow(cap.get_bottom(), cap.get_bottom() + DOWN * 0.6 +
                       RIGHT * 1.2, buff=0.05, color=CHALK_WHITE,
                       stroke_width=6)
            a2 = Arrow(tim.get_bottom(), tim.get_bottom() + DOWN * 0.6 +
                       LEFT * 1.2, buff=0.05, color=CHALK_WHITE,
                       stroke_width=6)
            comb = P(chip("NEITHER ALONE: COMBINE THE TWO RATIOS",
                          CHALK_YELLOW, 28, w=9.4, h=0.85), CX, -1.75)
            tidy(a, b, same=True)  # auto-tidy
            tidy(cap, tim, same=True)  # auto-tidy
            self.cue(tr, "b0", a, sfx="pop")
            self.cue(tr, "b1", b)
            self.cue(tr, "b2", cap)
            self.cue(tr, "b3", tim)
            self.cue(tr, "b4", a1, a2, comb, sfx="ding")
            self.finish(tr)

    # -- 5: compound ratio rule -----------------------------------------------------------------
    def beat_s5(self):
        with self.narrate("s5") as tr:
            self.heading("The Compound Ratio Rule")
            r1 = VGroup(panel(3.3, 1.2, CHALK_CYAN),
                        M(r"a:b", 60, CHALK_CYAN))
            r1[1].move_to(r1[0])
            r2 = VGroup(panel(3.3, 1.2, CHALK_AMBER),
                        M(r"c:d", 60, CHALK_AMBER))
            r2[1].move_to(r2[0])
            times = M(r"\times", 60, CHALK_WHITE)
            hrow(r1, times, r2, y=1.45, gap=0.45)
            self.show(r1, times, r2)
            f1 = P(chip("FIRST TERMS:  a x c", CHALK_CYAN, 28, w=4.7), CX - 2.55,
                   0.35)
            f2 = P(chip("SECOND TERMS:  b x d", CHALK_AMBER, 28, w=4.7),
                   CX + 2.55, 0.35)
            res = VGroup(panel(6.4, 1.15, CHALK_YELLOW),
                         M(r"ac:bd", 62, CHALK_YELLOW))
            res[1].move_to(res[0])
            P(res, CX, -0.65)
            bad = P(mistake_card("a + c : b + d", "never add the terms",
                                 w=6.4, h=1.1, size=30), CX, -1.95)
            tidy(f1, f2, same=True)  # auto-tidy
            self.cue(tr, "b0", f1, sfx="pop")
            self.cue(tr, "b1", f2)
            self.cue(tr, "b2", res, sfx="ding")
            self.cue(tr, "b3", bad, sfx="click")
            self.cue(tr, "b4", Indicate(res[0], color=CHALK_YELLOW,
                                        scale_factor=1.04), sfx="success")
            self.finish(tr)

    # -- 6: apply -------------------------------------------------------------------------------
    def beat_s6(self):
        with self.narrate("s6") as tr:
            self.heading("Apply the Rule")
            cap = chip("CAPITAL  2 : 3", CHALK_GREEN, 30, w=4.2)
            tim = chip("TIME  4 : 3", CHALK_AMBER, 30, w=4.2)
            x = M(r"\times", 50, CHALK_WHITE)
            hrow(cap, x, tim, y=1.60, gap=0.4)
            r1 = P(calc_row("", "", r"2\times4:3\times3=8:9", CHALK_YELLOW,
                            w=9.6, h=1.0, math_size=52), CX, 0.35)
            r2 = P(calc_row("", "CHECK", r"2000\times12:3000\times9="
                            r"24000:27000", CHALK_CYAN, w=9.6, h=1.0,
                            math_size=40), CX, -0.85)
            ok = P(chip("24000 : 27000  =  8 : 9   CORRECT", CHALK_GREEN, 30,
                        w=8.4), CX, -2.0)
            tidy(cap, tim, same=True)  # auto-tidy
            tidy(r1, r2, same=True)  # auto-tidy
            self.cue(tr, "b0", cap, sfx="pop")
            self.cue(tr, "b1", x, tim)
            self.cue(tr, "b2", r1, sfx="ding")
            self.cue(tr, "b3", r2)
            self.cue(tr, "b4", ok, sfx="success")
            self.finish(tr)

    # -- 7: rupees ----------------------------------------------------------------------------------
    def beat_s7(self):
        with self.narrate("s7") as tr:
            self.heading("From Ratio to Rupees")
            prof = P(icon_chip(money_bag(0.9), "PROFIT  Rs 17,000  (example)",
                               CHALK_GREEN, w=8.6, h=1.0, size=28), CX, 1.50)
            blocks = VGroup(*[Rectangle(width=0.50, height=0.62,
                                        stroke_color=OUTLINE, stroke_width=2.4,
                                        fill_color="#8FA9C7", fill_opacity=0.9)
                              for _ in range(17)]).arrange(RIGHT, buff=0.04)
            P(blocks, CX, 0.55)
            part = P(chip("Rs 17,000 / 17 = Rs 1,000 a part", CHALK_YELLOW, 28),
                     CX, -0.25)
            ca = tcard("RAMAYYA", ["8 parts = Rs 8,000"], CHALK_CYAN, w=4.7,
                       h=1.15, head_size=28, body_size=26, pad=0.10, gap=0.08)
            cb = tcard("GOPALAM", ["9 parts = Rs 9,000"], CHALK_AMBER, w=4.7,
                       h=1.15, head_size=28, body_size=26, pad=0.10, gap=0.08)
            P(ca, CX - 2.55, -1.40)
            P(cb, CX + 2.55, -1.40)
            tot = P(T("8,000 + 9,000 = 17,000: all shared.", 26,
                      CHALK_WHITE, max_w=9.6), CX, -2.35)
            tidy(ca, cb, same=True)  # auto-tidy
            self.cue(tr, "b0", prof, sfx="pop")
            self.cue(tr, "b1", blocks, sfx="click")
            self.cue(tr, "b2", part)
            self.cue(tr, "b3", ca, *[b.animate.set_fill(CHALK_CYAN, 0.95)
                                     for b in list(blocks)[:8]], sfx="pop")
            self.cue(tr, "b4", cb, *[b.animate.set_fill(CHALK_AMBER, 0.95)
                                     for b in list(blocks)[8:]], FadeIn(tot),
                     sfx="success")
            self.finish(tr)

    # -- 8: decision rule -----------------------------------------------------------------------------
    def beat_s8(self):
        with self.narrate("s8") as tr:
            self.heading("The Decision Rule")
            r1 = P(route_row("1", "SAME TIME", "share by the CAPITALS",
                             CHALK_CYAN, h=0.95, size=28, tsize=28), CX, 1.45)
            r2 = P(route_row("2", "SAME CAPITAL", "share by the TIMES",
                             CHALK_GREEN, h=0.95, size=28, tsize=28), CX, 0.38)
            r3 = P(route_row("3", "BOTH DIFFERENT", "COMPOUND ratio",
                             CHALK_AMBER, h=0.95, size=28, tsize=28), CX, -0.69)
            f = P(chip("SHARE  FOLLOWS  CAPITAL x TIME", CHALK_YELLOW, 32,
                       w=8.4, h=0.95), CX, -1.95)
            tidy(r1, r2, r3, same=True)  # auto-tidy
            self.cue(tr, "b0", r1, sfx="pop")
            self.cue(tr, "b1", r2)
            self.cue(tr, "b2", r3)
            self.cue(tr, "b3", f, sfx="success")
            self.finish(tr)

    # -- 9: your turn ----------------------------------------------------------------------------------
    def beat_s9(self):
        with self.narrate("s9q") as tr:
            self.heading("YOUR TURN", "Four quick checks.", CHALK_PINK)
            qa = q_card(block(1.2, 0.8, CHALK_CYAN, "7:5", 30), "A  INVERSE",
                        ["inverse of", "7 : 5 ?"], CHALK_CYAN)
            qb = q_card(block(1.2, 0.8, CHALK_GREEN, "x", 36), "B  COMPOUND",
                        ["3 : 4  and  2 : 3"], CHALK_GREEN)
            qc = q_card(block(1.2, 0.8, CHALK_AMBER, "1/x", 28), "C  MIXED",
                        ["3 : 4 with the", "inverse of 4 : 5"], CHALK_AMBER)
            qd = q_card(money_bag(0.9), "D  PARTNERS",
                        ["P: 4000 for 6 mo", "Q: 3000 for 8 mo"], CHALK_PINK)
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
                calc_row("A", "", r"7:5\ \to\ 5:7", CHALK_CYAN, w=9.6, h=0.85,
                         math_size=46),
                calc_row("B", "", r"3\times2:4\times3=6:12=1:2", CHALK_GREEN,
                         w=9.6, h=0.85, math_size=42),
                calc_row("C", "", r"3\times5:4\times4=15:16", CHALK_AMBER,
                         w=9.6, h=0.85, math_size=42),
                calc_row("D", "", r"24000:24000=1:1\ \text{(equal)}",
                         CHALK_PINK, w=9.6, h=0.85, math_size=42),
            ]
            for r, y in zip(rows, (1.15, 0.2, -0.75, -1.70)):
                P(r, CX, y)
            qa, qb, qc, qd = self._qs
            tidy(*rows, same=True)  # auto-tidy
            self.cue(tr, "b0", FadeOut(qa), FadeOut(qb), FadeOut(qc),
                     FadeOut(qd), FadeIn(rows[0]), sfx="click", rt=0.6)
            self.cue(tr, "b1", rows[1])
            self.cue(tr, "b2", rows[2])
            self.cue(tr, "b3", rows[3], sfx="success")
            self.finish(tr)

    # -- 10 -----------------------------------------------------------------------------------------------
    def beat_s10(self):
        with self.narrate("s10") as tr:
            head = self.heading("Inverse, Compound, Share")
            rows = [
                step_row("1", "INVERSE", "swap the terms: a:b to b:a",
                         CHALK_CYAN, h=0.88),
                step_row("2", "COMPOUND", "multiply: ac : bd", CHALK_AMBER,
                         h=0.88),
                step_row("3", "SHARE", "follows capital x time", CHALK_GREEN,
                         h=0.88),
                step_row("4", "RUPEES", "split the profit in equal parts",
                         CHALK_PINK, h=0.88),
            ]
            for r, y in zip(rows, (1.60, 0.62, -0.36, -1.34)):
                P(r, CX, y)
            strip = P(T("Money and time together decide the share.", 26,
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

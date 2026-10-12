"""
Simple Interest vs. Compound Interest: Deriving the Compound Interest Formula
Story-mode chalkboard lesson (Class 8 Maths, Chapter 5: Comparing Quantities
using Proportion).

LLM KEY / FUNCTION NAME: simple_vs_compound_interest_formula

Layout re-done for legibility: big chalk type inside the green board; Ramesh and
Sreenu are drawn figures (human_figure.Man), the principal sits in a padlocked
block while simple interest blocks stack beside it, the compound ladder merges
principal + interest into one new, bigger base, and the algebra is chalked big
and morphed step by step.

Title + 10 scenes:
  0. Same Rs 100, 10%, 2 years: Rs 120 vs Rs 121 -- where is the extra Re 1?
  1. Simple interest: interest on the ORIGINAL principal; SI = PTR/100.
  2. Compound interest: each new amount is the next principal.
  3. One period: A1 = P + PR/100 = P(1 + R/100).
  4. Year two: A2 = P(1 + R/100)^2.
  5. n years: A = P(1 + R/100)^n.
  6. The formula gives the amount; CI = A - P.
  7. Rs 5,000 at 8% for 2 years: A = Rs 5,832, CI = Rs 832.
  8. The two ladders side by side.
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
    "Simple interest versus compound interest. <bookmark mark='b0'/> Deriving the compound interest formula."
)
NARRATION = {
    "title": (
        "Ramesh and Sreenu lent the same money to two different borrowers. "
        "<bookmark mark='b0'/>Ramesh lent one hundred rupees at ten percent for "
        "two years, and got back one hundred and twenty rupees. <bookmark "
        "mark='b1'/>Sreenu lent one hundred rupees at the same ten percent, for "
        "the same two years, and got back one hundred and twenty one rupees. "
        "<bookmark mark='b2'/>Same principal, same rate, same time, and yet one "
        "rupee more. <bookmark mark='b3'/>Where did that extra rupee come from? "
        "<bookmark mark='b4'/>The two friends used two different methods. "
        "<bookmark mark='b5'/>Ramesh's method is simple interest, and Sreenu's "
        "method is compound interest."
    ),
    "s1": (
        "Ramesh uses simple interest. <bookmark mark='b0'/>The interest is "
        "always calculated on the original principal, so the base never "
        "changes. <bookmark mark='b1'/>One hundred rupees at ten percent gives "
        "ten rupees of interest every year. <bookmark mark='b2'/>Year one pays "
        "ten rupees, and year two pays ten rupees again, because the base is "
        "still the original one hundred. <bookmark mark='b3'/>Ten plus ten is "
        "twenty, so the amount is one hundred plus twenty, that is one hundred "
        "and twenty rupees. <bookmark mark='b4'/>Simple interest is P times T "
        "times R, divided by one hundred. <bookmark mark='b5'/>For example, two "
        "thousand five hundred rupees at twelve percent for three years gives "
        "nine hundred rupees of interest, <bookmark mark='b6'/>and the amount is "
        "three thousand four hundred rupees."
    ),
    "s2": (
        "Sreenu uses compound interest. <bookmark mark='b0'/>Here each new "
        "amount becomes the next principal, so the base itself grows. "
        "<bookmark mark='b1'/>In year one, ten percent of one hundred is ten "
        "rupees, so the amount is one hundred and ten rupees. <bookmark "
        "mark='b2'/>That one hundred and ten rupees is now the principal for "
        "year two. <bookmark mark='b3'/>In year two, ten percent of one hundred "
        "and ten is eleven rupees, so the amount becomes one hundred and twenty "
        "one rupees. <bookmark mark='b4'/>The second interest is eleven rupees, "
        "one rupee more than the first. <bookmark mark='b5'/>That extra rupee "
        "is ten percent of the first year's ten rupees of interest: <bookmark "
        "mark='b6'/>the interest itself earned interest."
    ),
    "s3": (
        "Watch one period only. <bookmark mark='b0'/>In one period the amount "
        "is the principal plus the interest on it: A one equals P plus P R over "
        "one hundred. <bookmark mark='b1'/>Take P outside the bracket, and the "
        "same amount is P times one plus R over one hundred. <bookmark "
        "mark='b2'/>The bracket, one plus R over one hundred, is the one period "
        "growth factor. <bookmark mark='b3'/>Whatever the principal is, "
        "<bookmark mark='b4'/>one period multiplies it by that same factor."
    ),
    "s4": (
        "Now the second year. <bookmark mark='b0'/>The amount from year one "
        "becomes the principal for year two. <bookmark mark='b1'/>So the same "
        "growth factor multiplies again. <bookmark mark='b2'/>A two equals P "
        "times one plus R over one hundred, times one plus R over one hundred "
        "once more. <bookmark mark='b3'/>Which is P into the square of one plus "
        "R over one hundred. <bookmark mark='b4'/>Two years means two factors, "
        "and two factors compress into one single power. <bookmark "
        "mark='b5'/>That power is the square, and every extra year adds one "
        "more."
    ),
    "s5": (
        "One factor for every year. <bookmark mark='b0'/>Year one multiplies by "
        "the growth factor, year two multiplies again, year three multiplies "
        "again, and so on up to year n. <bookmark mark='b1'/>Repeated "
        "multiplication by the same number compresses into a power. <bookmark "
        "mark='b2'/>So the amount after n years is A equals P times one plus R "
        "over one hundred, raised to the power n. <bookmark mark='b3'/>The "
        "exponent n is not a decoration. <bookmark mark='b4'/>It is the number "
        "of growth periods."
    ),
    "s6": (
        "Careful: this formula gives the amount. <bookmark mark='b0'/>The amount "
        "is the principal plus the interest, so it is not the interest itself. "
        "<bookmark mark='b1'/>The compound interest is the amount minus the "
        "principal. <bookmark mark='b2'/>So C I equals A minus P, which is P "
        "times one plus R over one hundred to the power n, minus P. <bookmark "
        "mark='b3'/>For one hundred rupees at ten percent for two years, the "
        "amount is one hundred and twenty one rupees, <bookmark mark='b4'/>and "
        "the interest is twenty one rupees."
    ),
    "s7": (
        "Let us use it with real numbers. Take P equals five thousand rupees, R "
        "equals eight percent, and n equals two years. <bookmark mark='b0'/>One "
        "plus eight over one hundred is one point zero eight, so the amount is "
        "five thousand times one point zero eight squared. <bookmark "
        "mark='b1'/>That is five thousand eight hundred and thirty two rupees. "
        "<bookmark mark='b2'/>The compound interest is the amount minus the "
        "principal. <bookmark mark='b3'/>Five thousand eight hundred and thirty "
        "two minus five thousand is eight hundred and thirty two rupees. "
        "<bookmark mark='b4'/>So the compound interest is eight hundred and "
        "thirty two rupees, <bookmark mark='b5'/>and not five thousand eight "
        "hundred and thirty two."
    ),
    "s8": (
        "Put the two ladders side by side. <bookmark mark='b0'/>On the simple "
        "interest ladder the principal stays locked at one hundred, so both "
        "years add the same ten rupees, and the amount is one hundred and "
        "twenty. <bookmark mark='b1'/>On the compound ladder the first year "
        "makes one hundred and ten, and that becomes the base, so the second "
        "year adds eleven rupees, and the amount is one hundred and twenty one. "
        "<bookmark mark='b2'/>Now look at the first year: both ladders add the "
        "same ten rupees, because both started from the original principal. "
        "<bookmark mark='b3'/>After that, simple interest keeps adding the same "
        "block, <bookmark mark='b4'/>while compound interest adds a bigger "
        "block, because its base grows."
    ),
    "s9q": (
        "Your turn. Four quick checks. <bookmark mark='b0'/>A: simple interest "
        "on two thousand rupees at five percent for three years. <bookmark "
        "mark='b1'/>B: compound interest on five thousand rupees at ten percent "
        "for two years. <bookmark mark='b2'/>C: every year the interest is "
        "calculated on five thousand rupees. <bookmark mark='b3'/>And next "
        "year's interest is calculated on the previous year's amount. <bookmark "
        "mark='b4'/>D: after the first year, are simple and compound interest "
        "different?"
    ),
    "s9a": (
        "Let us check the four answers. <bookmark mark='b0'/>A: two thousand "
        "times three times five, divided by one hundred, is three hundred "
        "rupees, so the amount is two thousand three hundred. <bookmark "
        "mark='b1'/>B: five thousand times one point one squared is six thousand "
        "and fifty, so the compound interest is one thousand and fifty. "
        "<bookmark mark='b2'/>C: interest on five thousand rupees every year is "
        "simple interest, and interest on the previous year's amount is compound "
        "interest. <bookmark mark='b3'/>D: no, after the first period they are "
        "the same, because both used the original principal."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>Simple interest keeps the original "
        "principal as the base, so every year adds the same interest. <bookmark "
        "mark='b1'/>Compound interest lets each new amount become the next base, "
        "so the interest itself grows. <bookmark mark='b2'/>We derived it: A "
        "one, then A two, then A equals P times one plus R over one hundred, to "
        "the power n. <bookmark mark='b3'/>And the formula gives the amount, so "
        "the compound interest is A minus P. <bookmark mark='b4'/>Simple stays "
        "on the original base; compound grows on the new base. <bookmark "
        "mark='b5'/>Thank you for watching, <bookmark mark='b6'/>and see you in "
        "the next lesson."
    ),
}
NARRATION = {"intro": INTRO_NARRATION, **NARRATION}

X0 = -2.55            # left edge of the ladder bars
BH = 0.72             # bar height
PW = 2.3              # principal block width (schematic)
IW = 1.0              # one interest block width (schematic)


def caption(text, y, color=CHALK_WHITE):
    t = T(text, 24, color)
    t.move_to([X0 - 0.25 - t.width / 2, y, 0])
    return t


def bar_row(y, parts):
    """Left-aligned run of blocks: parts = [(w, colour, text), ...]."""
    g = VGroup()
    x = X0
    for w, col, txt in parts:
        b = block(w, BH, col, txt, 26)
        b.move_to([x + w / 2, y, 0])
        g.add(b)
        x += w
    return g


class SimpleVsCompoundInterestFormulaStory(Ch5Scene):
    NARRATION = NARRATION
    TEXT_SCALE = 0.85     # medium type
    TIGHT_BOXES = True    # every box hugs its text
    STRICT_BOXES = True   # audit: boxes stay on the board with a gap between them
    AVOID_ART = True      # text/cards never sit on the teacher, students or badges
    INTRO_LINES = ('Simple vs', 'Compound Interest')
    INTRO_SUB = 'Deriving the Compound Interest Formula'
    BEATS = ("intro", "title", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9",
             "s10")

    # -- 0 -----------------------------------------------------------------
    def beat_title(self):
        with self.narrate("title") as tr:
            self.heading("Simple vs Compound Interest")

            def who(name, shirt, facing, lines_, color):
                box = panel(4.7, 2.55, color)
                man = person(ORIGIN, 2.2, facing, shirt)
                man.move_to(box.get_center() + LEFT * 1.55 + DOWN * 0.0)
                txt = VGroup(T(name, 30, color),
                             *[T(s, 24, CHALK_WHITE) for s in lines_]
                             ).arrange(DOWN, buff=0.10, aligned_edge=LEFT)
                fit(txt, 2.65, 2.2)
                txt.move_to(box.get_center() + RIGHT * 0.95)
                return VGroup(box, man, txt)
            a = who("RAMESH", "#4F8EF7", RIGHT, ["Rs 100 at 10%", "for 2 years",
                                                  "gets back Rs 120"],
                    CHALK_CYAN)
            b = who("SREENU", "#F0A23C", LEFT, ["Rs 100 at 10%", "for 2 years",
                                                 "gets back Rs 121"],
                    CHALK_AMBER)
            P(a, CX - 2.55, 0.90)
            P(b, CX + 2.55, 0.90)
            same = P(chip("SAME P, SAME RATE, SAME TIME  ...  Re 1 MORE",
                          CHALK_PINK, 26, w=9.6), CX, -0.82)
            ques = P(T("WHERE DID THE EXTRA Re 1 COME FROM?", 34,
                       CHALK_YELLOW, max_w=9.6), CX, -1.55)
            m1a = chip("METHOD 1", CHALK_CYAN, 26, w=4.6, h=0.7)
            m2a = chip("METHOD 2", CHALK_AMBER, 26, w=4.6, h=0.7)
            hrow(m1a, m2a, y=-2.30, gap=0.5)
            m1b = chip("SIMPLE INTEREST", CHALK_CYAN, 26, w=4.6, h=0.7)
            m2b = chip("COMPOUND INTEREST", CHALK_AMBER, 26, w=4.6, h=0.7)
            m1b.move_to(m1a)
            m2b.move_to(m2a)
            tidy(m1a, m2a, m1b, m2b, same=True)  # auto-tidy
            self.cue(tr, "b0", a, sfx="pop")
            self.cue(tr, "b1", b)
            self.cue(tr, "b2", same, sfx="click")
            self.cue(tr, "b3", ques, sfx="ding")
            self.cue(tr, "b4", m1a, m2a)
            self.cue(tr, "b5", ReplacementTransform(m1a, m1b),
                     ReplacementTransform(m2a, m2b), sfx="success")
            self.finish(tr)

    # -- 1: simple ---------------------------------------------------------------
    def beat_s1(self):
        with self.narrate("s1") as tr:
            self.heading("Simple Interest: the Base Never Changes")
            c0 = caption("START", 1.35)
            c1 = caption("YEAR 1", 0.50)
            c2 = caption("YEAR 2", -0.35)
            r0 = bar_row(1.35, [(PW, CHALK_CYAN, "Rs 100")])
            lock = P(padlock(0.75), X0 + PW + 0.55, 1.35)
            r1 = bar_row(0.50, [(PW, CHALK_CYAN, "Rs 100"),
                                (IW, CHALK_AMBER, "+10")])
            r2 = bar_row(-0.35, [(PW, CHALK_CYAN, "Rs 100"),
                                 (IW, CHALK_AMBER, "+10"),
                                 (IW, CHALK_AMBER, "+10")])
            k1 = tcard("EVERY YEAR", ["10% of 100 = 10"], CHALK_AMBER, w=3.6,
                       h=1.15, head_size=26, body_size=24, pad=0.10, gap=0.08)
            P(k1, 3.70, 1.20)
            k2 = tcard("AMOUNT", ["100 + 20 = Rs 120"], CHALK_GREEN, w=3.6,
                       h=1.15, head_size=26, body_size=24, pad=0.10, gap=0.08)
            P(k2, 3.70, 0.0)
            f = VGroup(panel(3.6, 1.1, CHALK_YELLOW),
                       M(r"\text{SI}=\frac{P\times T\times R}{100}", 32,
                         CHALK_YELLOW))
            f[1].move_to(f[0])
            P(f, 3.70, -1.25)
            ex = P(calc_row("", "", r"\frac{2500\times3\times12}{100}="
                            r"\text{Rs }900", CHALK_CYAN, w=5.8, h=0.95,
                            math_size=34), -1.5, -2.12)
            amt = P(chip("AMOUNT Rs 3,400", CHALK_GREEN, 26, w=3.7), 3.65,
                    -2.25)
            tidy(k1, k2, same=True)  # auto-tidy
            self.cue(tr, "b0", c0, r0, lock, sfx="pop")
            self.cue(tr, "b1", k1)
            self.cue(tr, "b2", c1, r1, c2, r2, sfx="click")
            self.cue(tr, "b3", k2, sfx="ding")
            self.cue(tr, "b4", f)
            self.cue(tr, "b5", ex)
            self.cue(tr, "b6", amt, sfx="success")
            self.finish(tr)

    # -- 2: compound -------------------------------------------------------------------
    def beat_s2(self):
        with self.narrate("s2") as tr:
            self.heading("Compound Interest: the Base Grows")
            c0 = caption("START", 1.35)
            c1 = caption("YEAR 1", 0.50)
            c2 = caption("YEAR 2", -0.35)
            r0 = bar_row(1.35, [(PW, CHALK_CYAN, "Rs 100")])
            r1 = bar_row(0.50, [(PW, CHALK_CYAN, "Rs 100"),
                                (IW, CHALK_AMBER, "+10")])
            merged = bar_row(0.50, [(PW + IW, CHALK_CYAN, "Rs 110")])
            r2 = bar_row(-0.35, [(PW + IW, CHALK_CYAN, "Rs 110"),
                                 (1.1, CHALK_PINK, "+11")])
            k0 = tcard("BASE GROWS", ["new amount = new base"], CHALK_YELLOW,
                       w=3.6, h=1.15, head_size=26, body_size=22, pad=0.10,
                       gap=0.08)
            P(k0, 3.70, 1.35)
            k1 = tcard("YEAR 1", ["10% of 100 = 10"], CHALK_AMBER, w=3.6,
                       h=1.15, head_size=26, body_size=24, pad=0.10, gap=0.08)
            P(k1, 3.70, 0.20)
            k2 = tcard("YEAR 2", ["10% of 110 = 11"], CHALK_PINK, w=3.6,
                       h=1.15, head_size=26, body_size=24, pad=0.10, gap=0.08)
            P(k2, 3.70, -0.95)
            e1 = P(chip("11 is Re 1 more than 10", CHALK_PINK, 26, w=4.7),
                   CX - 2.5, -1.85)
            e2 = P(chip("Re 1 = 10% of the first Rs 10", CHALK_YELLOW, 26,
                        w=4.9), CX + 2.5, -1.85)
            strip = P(T("The interest itself earned interest.", 28,
                        CHALK_WHITE), CX, -2.42)
            tidy(k0, k1, k2, same=True)  # auto-tidy
            self.cue(tr, "b0", c0, r0, k0, sfx="pop")
            self.cue(tr, "b1", c1, r1, k1, sfx="click")
            self.cue(tr, "b2", ReplacementTransform(r1, merged), sfx="whoosh",
                     rt=0.8)
            self.cue(tr, "b3", c2, r2, k2, sfx="click")
            self.cue(tr, "b4", e1)
            self.cue(tr, "b5", e2, sfx="ding")
            self.cue(tr, "b6", strip, sfx="success")
            self.finish(tr)

    # -- 3: one period --------------------------------------------------------------------
    def beat_s3(self):
        with self.narrate("s3") as tr:
            self.heading("One Period")
            m1 = P(M(r"A_1=P+\frac{PR}{100}", 66, CHALK_WHITE), CX, 0.85)
            m2 = P(M(r"A_1=P\left(1+\frac{R}{100}\right)", 66, CHALK_WHITE),
                   CX, 0.85)
            fac = P(chip("GROWTH FACTOR", CHALK_YELLOW, 28), CX + 1.7, -0.22)
            s_a = P(coin_stack(3, 0.5), CX - 3.2, -1.65)
            s_b = P(coin_stack(4, 0.5), CX + 3.2, -1.55)
            arr = Arrow(s_a.get_right() + RIGHT * 0.3, s_b.get_left() + LEFT *
                        0.3, buff=0, color=CHALK_WHITE, stroke_width=6)
            alab = P(M(r"\times\left(1+\frac{R}{100}\right)", 42,
                       CHALK_YELLOW), CX, -1.00)
            la = P(T("P", 34, CHALK_CYAN), s_a.get_bottom()[0], -2.30)
            lb = P(T("A1", 34, CHALK_GREEN), s_b.get_bottom()[0], -2.30)
            strip = P(T("one period multiplies it by that factor.", 26,
                        CHALK_WHITE), CX, -2.35)
            self.cue(tr, "b0", m1, sfx="pop")
            self.cue(tr, "b1", ReplacementTransform(m1, m2), sfx="ding",
                     rt=0.9)
            self.cue(tr, "b2", fac)
            self.cue(tr, "b3", s_a, la)
            self.cue(tr, "b4", arr, alab, s_b, lb, sfx="success")
            self.finish(tr)

    # -- 4: second year ----------------------------------------------------------------------
    def beat_s4(self):
        with self.narrate("s4") as tr:
            self.heading("Now the Second Year")
            sa = P(coin_stack(3, 0.42), CX - 3.6, 1.40)
            sb = P(coin_stack(4, 0.42), CX, 1.40)
            sc = P(coin_stack(5, 0.42), CX + 3.6, 1.40)
            a1 = Arrow(sa.get_right() + RIGHT * 0.2, sb.get_left() + LEFT * 0.2,
                       buff=0, color=CHALK_WHITE, stroke_width=6)
            a2 = Arrow(sb.get_right() + RIGHT * 0.2, sc.get_left() + LEFT * 0.2,
                       buff=0, color=CHALK_WHITE, stroke_width=6)
            la = P(T("P", 30, CHALK_CYAN), sa.get_center()[0], 0.62)
            lb = P(T("A1: new principal", 26, CHALK_GREEN), sb.get_center()[0],
                   0.62)
            lc = P(T("A2", 30, CHALK_AMBER), sc.get_center()[0], 0.62)
            m1 = P(M(r"A_2=P\left(1+\frac{R}{100}\right)\left(1+\frac{R}{100}"
                     r"\right)", 44, CHALK_WHITE), CX, -0.40)
            m2 = P(M(r"A_2=P\left(1+\frac{R}{100}\right)^{2}", 56,
                     CHALK_YELLOW), CX, -1.60)
            strip = P(T("Two factors become one square.", 26,
                        CHALK_WHITE, max_w=9.6), CX, -2.42)
            self.cue(tr, "b0", sa, sb, la, lb, a1, sfx="pop")
            self.cue(tr, "b1", a2, sc, lc, sfx="click")
            self.cue(tr, "b2", m1, sfx="ding")
            self.cue(tr, "b3", m2)
            self.cue(tr, "b5", strip, sfx="success")
            self.finish(tr)

    # -- 5: n years ----------------------------------------------------------------------------
    def beat_s5(self):
        with self.narrate("s5") as tr:
            self.heading("One Factor for Every Year")
            items = [block(0.95, 0.8, CHALK_CYAN, "P", 30)]
            for lab in ("x f", "x f", "x f", "...", "x f"):
                items.append(block(1.05, 0.8, CHALK_AMBER, lab, 28))
            items.append(block(0.95, 0.8, CHALK_GREEN, "A", 30))
            row = VGroup(*items).arrange(RIGHT, buff=0.18)
            P(row, CX, 1.40)
            yrs = VGroup(*[T(s, 24, CHALK_WHITE) for s in
                           ("", "yr 1", "yr 2", "yr 3", "", "yr n", "")])
            for t, b in zip(yrs, items):
                t.next_to(b, DOWN, buff=0.10)
            ch = chip("REPEATED MULTIPLYING  =  A POWER", CHALK_PINK, 28)
            P(ch, CX, 0.25)
            big = P(M(r"A=P\left(1+\frac{R}{100}\right)^{n}", 70,
                      CHALK_YELLOW), CX, -0.95)
            nch = P(chip("n = the number of growth periods", CHALK_CYAN, 28),
                    CX, -2.20)
            self.cue(tr, "b0", row, yrs, sfx="pop")
            self.cue(tr, "b1", ch)
            self.cue(tr, "b2", big, sfx="ding")
            self.cue(tr, "b3", Indicate(big, color=CHALK_PINK,
                                        scale_factor=1.08), sfx=None)
            self.cue(tr, "b4", nch, sfx="success")
            self.finish(tr)

    # -- 6: amount vs interest ----------------------------------------------------------------------
    def beat_s6(self):
        with self.narrate("s6") as tr:
            self.heading("The Formula Gives the Amount")
            bar = segbar(7.4, [(100 / 121, CHALK_CYAN, "PRINCIPAL"),
                               (21 / 121, CHALK_AMBER, "CI")], h=0.85, size=26)
            P(bar, CX, 0.95)
            brace = brace_label(bar, "AMOUNT = principal + interest", UP,
                                size=26)
            ci = P(chip("CI = A - P", CHALK_YELLOW, 34), CX - 2.6, 0.02)
            f = P(M(r"\text{CI}=P\left(1+\frac{R}{100}\right)^{n}-P", 54,
                    CHALK_WHITE), CX, -1.15)
            e1 = P(chip("A = Rs 121", CHALK_GREEN, 30, w=3.8), CX - 2.2, -2.25)
            e2 = P(chip("CI = Rs 21", CHALK_AMBER, 30, w=3.8), CX + 2.2, -2.25)
            tidy(e1, e2, same=True)  # auto-tidy
            self.cue(tr, "b0", bar, brace, sfx="pop")
            self.cue(tr, "b1", ci, sfx="ding")
            self.cue(tr, "b2", f)
            self.cue(tr, "b3", e1)
            self.cue(tr, "b4", e2, sfx="success")
            self.finish(tr)

    # -- 7: Rs 5000 at 8% -----------------------------------------------------------------------------
    def beat_s7(self):
        with self.narrate("s7") as tr:
            self.heading("Worked Example")
            giv = P(chip("P = Rs 5,000   R = 8%   n = 2", CHALK_CYAN, 28),
                    CX, 1.75)
            r1 = P(calc_row("1", "AMOUNT", r"5000\times1.08^{2}", CHALK_CYAN,
                            w=9.6, h=0.9, math_size=44), CX, 0.90)
            r2 = P(calc_row("", "", r"A=\text{Rs }5832", CHALK_GREEN, w=9.6,
                            h=0.9, math_size=44), CX, -0.10)
            r3 = P(calc_row("2", "CI = A - P", r"5832-5000=\text{Rs }832",
                            CHALK_AMBER, w=9.6, h=0.9, math_size=44), CX,
                   -1.10)
            fin = P(chip("CI = Rs 832", CHALK_YELLOW, 30, w=4.2), CX - 2.5,
                    -2.12)
            bad = P(mistake_card("Rs 5,832", "that is the amount", w=4.6,
                                 h=0.85, size=20), CX + 2.6, -2.12)
            tidy(r1, r2, r3, same=True)  # auto-tidy
            self.cue(tr, "b0", giv, r1, sfx="pop")
            self.cue(tr, "b1", r2)
            self.cue(tr, "b2", r3)
            self.cue(tr, "b4", fin, sfx="ding")
            self.cue(tr, "b5", bad, sfx="click")
            self.finish(tr)

    # -- 8: two ladders -------------------------------------------------------------------------------------
    def beat_s8(self):
        with self.narrate("s8") as tr:
            self.heading("The Two Ladders")

            def panel_(title, color, rows_):
                box = panel(4.8, 3.1, color)
                tt = T(title, 28, color, max_w=4.4)
                tt.move_to(box.get_top() + DOWN * 0.38)
                g = VGroup(box, tt)
                for k, parts in enumerate(rows_):
                    y = box.get_center()[1] + 0.35 - k * 0.95
                    x = box.get_left()[0] + 0.25
                    cap = T(f"Y{k + 1}", 24, CHALK_WHITE)
                    cap.move_to([x + cap.width / 2, y, 0])
                    g.add(cap)
                    xx = x + 0.7
                    for w, col, txt in parts:
                        b = block(w, 0.7, col, txt, 24)
                        b.move_to([xx + w / 2, y, 0])
                        g.add(b)
                        xx += w
                return g
            L = panel_("SIMPLE: base locked", CHALK_CYAN,
                       [[(1.5, CHALK_CYAN, "100"), (0.8, CHALK_AMBER, "+10")],
                        [(1.5, CHALK_CYAN, "100"), (0.8, CHALK_AMBER, "+10"),
                         (0.8, CHALK_AMBER, "+10")]])
            R = panel_("COMPOUND: base grows", CHALK_AMBER,
                       [[(1.5, CHALK_CYAN, "100"), (0.8, CHALK_AMBER, "+10")],
                        [(2.3, CHALK_CYAN, "110"), (0.95, CHALK_PINK, "+11")]])
            P(L, CX - 2.55, 0.50)
            P(R, CX + 2.55, 0.50)
            yr1 = P(chip("YEAR 1: both add the same Rs 10", CHALK_YELLOW, 26),
                    CX, -1.50)
            strip = P(T("Simple: the same block. Compound: a bigger block.",
                        26, CHALK_WHITE, max_w=9.6), CX, -2.30)
            self.cue(tr, "b0", L, sfx="pop")
            self.cue(tr, "b1", R)
            self.cue(tr, "b2", yr1, sfx="ding")
            self.cue(tr, "b3", Indicate(L, color=CHALK_CYAN,
                                        scale_factor=1.03), sfx=None)
            self.cue(tr, "b4", Indicate(R, color=CHALK_AMBER,
                                        scale_factor=1.03), FadeIn(strip),
                     sfx="success")
            self.finish(tr)

    # -- 9: your turn ----------------------------------------------------------------------------------------
    def beat_s9(self):
        with self.narrate("s9q") as tr:
            self.heading("YOUR TURN", "Four quick checks.", CHALK_PINK)
            qa = q_card(coin_stack(3, 0.5), "A  SIMPLE",
                        ["Rs 2000 at 5%", "for 3 years: SI"], CHALK_CYAN)
            qb = q_card(coin_stack(5, 0.5), "B  COMPOUND",
                        ["Rs 5000 at 10%", "for 2 years: CI"], CHALK_AMBER)
            qc = q_card(padlock(0.9), "C  WHICH KIND?",
                        ["always on Rs 5000", "or on last amount"], CHALK_GREEN)
            qd = q_card(block(1.0, 0.7, CHALK_PINK, "Y1", 28), "D  AFTER Y1",
                        ["are simple and", "compound different?"], CHALK_PINK)
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
            self.cue(tr, "b4", qd)
            self.finish(tr)
            self._qs = (qa, qb, qc, qd)
        self.think_clock()
        with self.narrate("s9a", reset=False) as tr:
            rows = [
                calc_row("A", "", r"\frac{2000\times3\times5}{100}=300,\ \ "
                         r"A=2300", CHALK_CYAN, w=9.6, h=1.0, math_size=38),
                calc_row("B", "", r"5000\times1.1^{2}=6050,\ \ "
                         r"\text{CI}=1050", CHALK_AMBER, w=9.6, h=0.9,
                         math_size=40),
                step_row("C", "original base: SIMPLE", "last amount: COMPOUND",
                         CHALK_GREEN, h=0.85),
                step_row("D", "NO", "same after the first period", CHALK_PINK,
                         h=0.85),
            ]
            for r, y in zip(rows, (1.10, 0.10, -0.85, -1.75)):
                P(r, CX, y)
            qa, qb, qc, qd = self._qs
            tidy(*rows, same=True)  # auto-tidy
            self.cue(tr, "b0", FadeOut(qa), FadeOut(qb), FadeOut(qc),
                     FadeOut(qd), FadeIn(rows[0]), sfx="click", rt=0.6)
            self.cue(tr, "b1", rows[1])
            self.cue(tr, "b2", rows[2])
            self.cue(tr, "b3", rows[3], sfx="success")
            self.finish(tr)

    # -- 10 ------------------------------------------------------------------------------------------------------
    def beat_s10(self):
        with self.narrate("s10") as tr:
            head = self.heading("Simple Stays, Compound Grows")
            rows = [
                step_row("1", "SIMPLE", "original base every year", CHALK_CYAN,
                         h=0.88),
                step_row("2", "COMPOUND", "each amount is the next base",
                         CHALK_AMBER, h=0.88),
                calc_row("3", "", r"A=P\left(1+\frac{R}{100}\right)^{n}",
                         CHALK_YELLOW, w=9.6, h=0.95, math_size=42),
                calc_row("4", "", r"\text{CI}=A-P", CHALK_GREEN, w=9.6, h=0.88,
                         math_size=44),
            ]
            for r, y in zip(rows, (1.60, 0.62, -0.38, -1.38)):
                P(r, CX, y)
            strip = P(T("Simple: original base. Compound: new base.", 26,
                        CHALK_YELLOW, max_w=9.6), CX, -2.35)
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

"""
Compounding Half-Yearly, Quarterly & Applications to Population Growth and
Depreciation
Story-mode chalkboard lesson (Class 8 Maths, Chapter 5: Comparing Quantities
using Proportion).

LLM KEY / FUNCTION NAME: compounding_periods_half_yearly_quarterly_depreciation

Layout re-done for legibility: big chalk type inside the green board; the
defining visual is the COMPOUNDING CLOCK -- one one-year dial cut into 1, 2 or
4 conversion periods -- followed by a growing village (houses), shrinking
percentage bars and a bouncing ball for depreciation.

Title + 11 scenes (thirteen narrated pieces):
  0. Rs 1,000 at 10%: Rs 1,100 yearly, Rs 1,102.50 half-yearly -- why?
  1. The conversion period: 1, 2 or 4 periods in a year.
  2. Half-yearly rule: R -> R/2 and n -> 2n together.
  3. Worked example: 1000(1.05)^2 = Rs 1,102.50, CI = Rs 102.50.
  4. Quarterly: R/4 and 4n.
  5. Population growth: 6250 x 1.08^2 = 7290.
  6. Depreciation: (100 - R)% is kept; the bouncing ball.
  7. One structure, three uses.
  8. The five-step decision map.
  9. Your turn and the answers.
 10. The summary board.
 11. Recap and thank-you.
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
    "Compounding half-yearly and quarterly. <bookmark mark='b0'/> With population growth and depreciation."
)
NARRATION = {
    "title": (
        "One thousand rupees at ten percent per annum. <bookmark mark='b0'/> "
        "Compounded every year, that money becomes one thousand one hundred "
        "rupees after one year. <bookmark mark='b1'/> But the same ten percent "
        "compounded half-yearly gives one thousand fifty rupees after six "
        "months, <bookmark mark='b2'/> and one thousand one hundred two rupees "
        "and fifty paise after a year. <bookmark mark='b3'/> Same money, same "
        "rate, more interest. <bookmark mark='b4'/> Why does the timing change "
        "the answer?"
    ),
    "s1": (
        "First, the conversion period. <bookmark mark='b0'/> The conversion "
        "period is the time interval after which the interest is added to the "
        "principal. <bookmark mark='b1'/> If interest is added once a year, the "
        "period is one full year: one turn of the clock. <bookmark mark='b2'/> "
        "If it is added every six months, that same year is cut into two equal "
        "periods. <bookmark mark='b3'/> And if it is added every three months, "
        "the year becomes four quarter periods. <bookmark mark='b4'/> So the "
        "conversion period fixes two things together, the rate for each period "
        "and how many periods there are."
    ),
    "s2": (
        "Now the half-yearly rule. <bookmark mark='b0'/> When the conversion "
        "period halves, two things change at the same time. <bookmark "
        "mark='b1'/> The rate for each period halves as well: R becomes R "
        "divided by two. <bookmark mark='b2'/> And the number of periods "
        "doubles: n becomes two n. <bookmark mark='b3'/> So the amount is P "
        "times one plus R over two hundred, all raised to two n. <bookmark "
        "mark='b4'/> Ten percent per annum compounded half-yearly means five "
        "percent for each half-year, <bookmark mark='b5'/> never ten percent "
        "every six months, and never change the exponent alone."
    ),
    "s3": (
        "Let us work it out. <bookmark mark='b0'/> Principal one thousand "
        "rupees, rate ten percent per annum, time one year, compounded "
        "half-yearly. <bookmark mark='b1'/> The rate for each half-year is ten "
        "divided by two, that is five percent. <bookmark mark='b2'/> And one "
        "year holds two half-yearly periods. <bookmark mark='b3'/> So the "
        "amount is one thousand times one point zero five squared, which is one "
        "thousand one hundred two rupees and fifty paise. <bookmark mark='b4'/> "
        "The compound interest is one thousand one hundred two point five minus "
        "one thousand, that is one hundred two rupees and fifty paise."
    ),
    "s4": (
        "A year has four quarters. <bookmark mark='b0'/> So when interest is "
        "compounded quarterly, the rate for one period becomes R divided by "
        "four, <bookmark mark='b1'/> and the number of periods becomes four n. "
        "<bookmark mark='b2'/> The amount is P times one plus R over four "
        "hundred, all raised to four n. <bookmark mark='b3'/> This is the same "
        "conversion-period rule, extended from two periods to four. <bookmark "
        "mark='b4'/> The rate and the number of periods always change together."
    ),
    "s5": (
        "The same structure answers questions about population. <bookmark "
        "mark='b0'/> A village has six thousand two hundred and fifty people, "
        "and the population grows by eight percent every year. <bookmark "
        "mark='b1'/> After one year the population is six thousand two hundred "
        "and fifty times one point zero eight, <bookmark mark='b2'/> and that "
        "new total becomes the base for the next year. <bookmark mark='b3'/> So "
        "after two years the population is six thousand two hundred and fifty "
        "times one point zero eight squared, which is seven thousand two "
        "hundred and ninety. <bookmark mark='b4'/> A repeated percentage "
        "increase is exactly the same structure as compound interest."
    ),
    "s6": (
        "Now depreciation, the mirror image. <bookmark mark='b0'/> Depreciation "
        "is a reduction in the value of an article due to use and age. "
        "<bookmark mark='b1'/> A quantity that loses R percent in each period "
        "keeps one hundred minus R percent. <bookmark mark='b2'/> Ten percent "
        "off leaves ninety percent, and the next reduction is taken from the "
        "new value. <bookmark mark='b3'/> So after two periods the value is P "
        "times zero point nine squared, and in general V is P times one minus R "
        "over one hundred, all raised to n. <bookmark mark='b4'/> A ball "
        "dropped from twenty five metres loses ten percent of its height at "
        "each bounce, so after two bounces it rises to twenty five times zero "
        "point nine squared, that is twenty point two five metres."
    ),
    "s7": (
        "One structure, three uses. <bookmark mark='b0'/> Money at compound "
        "interest and population growth both use P times one plus r, all raised "
        "to n. <bookmark mark='b1'/> Depreciation uses P times one minus r, "
        "raised to n. <bookmark mark='b2'/> A growth multiplier is greater than "
        "one, <bookmark mark='b3'/> and a depreciation multiplier is less than "
        "one. <bookmark mark='b4'/> So keep two decisions separate: how often "
        "the update happens, and whether the quantity rises or falls."
    ),
    "s8": (
        "Here is the decision map. <bookmark mark='b0'/> Step one: identify the "
        "conversion period. <bookmark mark='b1'/> Step two: find the rate for "
        "one period. <bookmark mark='b2'/> Step three: count the number of "
        "periods. <bookmark mark='b3'/> Step four: choose plus for growth, or "
        "minus for decrease. <bookmark mark='b4'/> Step five: apply that factor "
        "again and again. <bookmark mark='b5'/> Period, rate, factor, repeat: "
        "that is the whole method."
    ),
    "s9q": (
        "Your turn. Three questions. <bookmark mark='b0'/> First: twelve "
        "thousand rupees at ten percent per annum for one and a half years, "
        "compounded half-yearly. Find the amount. <bookmark mark='b1'/> Second: "
        "twelve percent per annum for two years, compounded quarterly. What is "
        "the rate for each period, and how many periods are there? <bookmark "
        "mark='b2'/> Third: a television costing twenty one thousand rupees "
        "depreciates by five percent in one year. What is it worth now? "
        "<bookmark mark='b3'/> And a quick check: for eight percent growth, "
        "which factor do you use, and for eight percent depreciation, which "
        "factor?"
    ),
    "s9a": (
        "Let us check. <bookmark mark='b0'/> For A, the rate is five percent per "
        "half-year and one and a half years is three periods, so the amount is "
        "twelve thousand times one point zero five cubed, that is thirteen "
        "thousand eight hundred ninety one rupees and fifty paise. <bookmark "
        "mark='b1'/> For B, twelve divided by four is three percent per "
        "quarter, and two years is eight quarters, so the amount is P times one "
        "point zero three raised to eight. <bookmark mark='b2'/> For C, five "
        "percent depreciation leaves ninety five percent, so twenty one "
        "thousand times zero point nine five is nineteen thousand nine hundred "
        "and fifty rupees. <bookmark mark='b3'/> And the quick check: for eight "
        "percent growth use one point zero eight, and for eight percent "
        "depreciation use zero point nine two, because one minus zero point "
        "zero eight is zero point nine two."
    ),
    "s10": (
        "Let us gather the whole lesson in one place. <bookmark mark='b0'/> The "
        "conversion period has three cases: annually, the rate is R and there "
        "are n periods; <bookmark mark='b1'/> half-yearly, the rate is R over "
        "two and the periods double to two n; <bookmark mark='b2'/> quarterly, "
        "the rate is R over four and the periods become four n. <bookmark "
        "mark='b3'/> Growth uses A equals P times one plus R over one hundred, "
        "all raised to n: that is compound interest and population. <bookmark "
        "mark='b4'/> Depreciation uses V equals P times one minus R over one "
        "hundred, all raised to n: the value keeps what is left. <bookmark "
        "mark='b5'/> And the five steps: identify the conversion period, find "
        "the rate for one period, count the number of periods, choose plus for "
        "growth or minus for decrease, and apply that factor again and again."
    ),
    "s11": (
        "One last look. <bookmark mark='b0'/> The compounding clock: annually, "
        "half-yearly, quarterly, with the rate and the number of periods "
        "changing together. <bookmark mark='b1'/> Growth uses P times one plus "
        "R over one hundred, all raised to n, <bookmark mark='b2'/> and "
        "depreciation uses P times one minus R over one hundred, raised to n. "
        "<bookmark mark='b3'/> Keep the two decisions separate: how often, and "
        "up or down. <bookmark mark='b4'/> Period, rate, factor, repeat. "
        "<bookmark mark='b5'/> Thank you for watching, <bookmark mark='b6'/> "
        "and see you in the next lesson."
    ),
}
NARRATION = {"intro": INTRO_NARRATION, **NARRATION}


def fmath(tex, color, w, h=1.0, size=44):
    box = panel(w, h, color)
    m = M(tex, size, color, max_w=w - 0.4)
    m.move_to(box)
    g = VGroup(box, m)
    g.box = box
    return g


class CompoundingPeriodsHalfYearlyQuarterlyDepreciationStory(Ch5Scene):
    NARRATION = NARRATION
    TEXT_SCALE = 0.85     # medium type
    TIGHT_BOXES = True    # every box hugs its text
    STRICT_BOXES = True   # audit: boxes stay on the board with a gap between them
    AVOID_ART = True      # text/cards never sit on the teacher, students or badges
    INTRO_LINES = ('Half-Yearly, Quarterly', '& Depreciation')
    INTRO_SUB = 'Compound Interest, Population Growth and Depreciation'
    BEATS = ("intro", "title", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9",
             "s10", "s11")

    # -- 0 -----------------------------------------------------------------
    def beat_title(self):
        with self.narrate("title") as tr:
            self.heading("Compounding More Often")
            def ycard(color, d, head, l1, l2):
                box = panel(4.7, 2.75, color)
                col = VGroup(d, T(head, 28, color), T(l1, 24, CHALK_WHITE),
                             T(l2, 24, CHALK_WHITE)).arrange(DOWN, buff=0.08)
                fit(col, 4.4, 2.5)
                col.move_to(box)
                g = VGroup(box, col)
                g.box = box
                return g
            ca = ycard(CHALK_CYAN, dial(1, 0.58, ["1 yr"], size=24),
                       "ANNUALLY", "Rs 1,000 -> Rs 1,100", "after 1 year")
            cb = ycard(CHALK_AMBER, dial(2, 0.58, ["6", "6"], size=24),
                       "HALF-YEARLY", "Rs 1,050 after 6 months",
                       "Rs 1,102.50 after 1 year")
            P(ca, CX - 2.55, 0.80)
            P(cb, CX + 2.55, 0.80)
            same = P(chip("SAME MONEY, SAME RATE, MORE INTEREST", CHALK_PINK,
                          28, w=9.6), CX, -1.00)
            why = P(T("WHY DOES THE TIMING CHANGE THE ANSWER?", 32,
                      CHALK_YELLOW, max_w=9.6), CX, -1.90)
            tidy(ca, cb, same=True)
            self.cue(tr, "b0", ca, sfx="pop")
            self.cue(tr, "b1", cb)
            self.cue(tr, "b2", Indicate(cb.box, color=CHALK_AMBER,
                                        scale_factor=1.04), sfx="click")
            self.cue(tr, "b3", same, sfx="ding")
            self.cue(tr, "b4", why, sfx="success")
            self.finish(tr)

    # -- 1: conversion period ---------------------------------------------------
    def beat_s1(self):
        with self.narrate("s1") as tr:
            self.heading("The Conversion Period")
            top = P(chip("TIME BETWEEN TWO INTEREST ADDITIONS", CHALK_YELLOW,
                         28, w=9.6), CX, 1.65)
            d1 = P(dial(1, 0.95, ["12 mo"], size=26), CX - 3.3, 0.20)
            d2 = P(dial(2, 0.95, ["6", "6"], size=28), CX, 0.20)
            d4 = P(dial(4, 0.95, ["3", "3", "3", "3"], size=28), CX + 3.3,
                   0.20)
            l1 = P(lines(["ANNUALLY", "1 period"], 26, CHALK_CYAN, buff=0.06),
                   CX - 3.3, -1.20)
            l2 = P(lines(["HALF-YEARLY", "2 periods"], 26, CHALK_AMBER,
                         buff=0.06), CX, -1.20)
            l4 = P(lines(["QUARTERLY", "4 periods"], 26, CHALK_GREEN,
                         buff=0.06), CX + 3.3, -1.20)
            bot = P(chip("IT FIXES: rate per period AND number of periods",
                         CHALK_PINK, 26, w=9.6), CX, -2.25)
            tidy(top, bot, same=True)  # auto-tidy
            self.cue(tr, "b0", top, sfx="pop")
            self.cue(tr, "b1", d1, l1)
            self.cue(tr, "b2", d2, l2)
            self.cue(tr, "b3", d4, l4)
            self.cue(tr, "b4", bot, sfx="success")
            self.finish(tr)

    # -- 2: half-yearly rule -------------------------------------------------------
    def beat_s2(self):
        with self.narrate("s2") as tr:
            self.heading("The Half-Yearly Rule")
            d = P(dial(2, 0.85, ["6", "6"], size=28), -3.0, 1.00)
            r1 = P(calc_row("1", "RATE", r"R\ \to\ \frac{R}{2}", CHALK_CYAN,
                            w=5.6, h=0.95, math_size=40), 2.65, 1.45)
            r2 = P(calc_row("2", "PERIODS", r"n\ \to\ 2n", CHALK_AMBER, w=5.6,
                            h=0.85, math_size=40), 2.65, 0.45)
            fm = P(fmath(r"A=P\left(1+\frac{R}{200}\right)^{2n}",
                         CHALK_YELLOW, 8.4, h=1.15, size=40), CX - 0.5, -0.75)
            ok = chip("10% p.a. = 5% per half-year", CHALK_GREEN, 26, w=4.7)
            bad = mistake_card("10% every six months", "never change one only",
                               w=5.0, h=1.05, size=22)
            hrow(ok, bad, y=-2.05, gap=0.3, cx=CX - 0.5)
            tidy(r1, r2, same=True)
            tidy(r1, r2, same=True)  # auto-tidy
            self.cue(tr, "b0", d, sfx="pop")
            self.cue(tr, "b1", r1)
            self.cue(tr, "b2", r2)
            self.cue(tr, "b3", fm, sfx="ding")
            self.cue(tr, "b4", ok)
            self.cue(tr, "b5", bad, sfx="click")
            self.finish(tr)

    # -- 3: worked example -----------------------------------------------------------
    def beat_s3(self):
        with self.narrate("s3") as tr:
            self.heading("Worked Example")
            giv = P(chip("P = Rs 1000  |  10% p.a.  |  1 year  |  half-yearly",
                         CHALK_CYAN, 26, w=9.6), CX, 1.65)
            c1 = P(calc_row("", "RATE", r"\frac{10}{2}=5\%", CHALK_AMBER,
                            w=4.7, h=1.0, math_size=40), CX - 2.55, 0.50)
            c2 = P(calc_row("", "PERIODS", r"1\text{ yr}=2\text{ halves}",
                            CHALK_GREEN, w=4.7, h=1.0, math_size=36), CX + 2.55,
                   0.50)
            r1 = P(calc_row("", "AMOUNT", r"1000\times1.05^{2}=\text{Rs }"
                            r"1102.50", CHALK_YELLOW, w=9.6, h=0.95,
                            math_size=42), CX, -0.65)
            r2 = P(calc_row("", "CI", r"1102.50-1000=\text{Rs }102.50",
                            CHALK_PINK, w=9.6, h=0.95, math_size=42), CX,
                   -1.75)
            tidy(c1, c2, same=True)
            tidy(r1, r2, same=True)
            tidy(c1, c2, same=True)  # auto-tidy
            tidy(r1, r2, same=True)  # auto-tidy
            self.cue(tr, "b0", giv, sfx="pop")
            self.cue(tr, "b1", c1)
            self.cue(tr, "b2", c2)
            self.cue(tr, "b3", r1, sfx="ding")
            self.cue(tr, "b4", r2, sfx="success")
            self.finish(tr)

    # -- 4: quarterly ----------------------------------------------------------------------
    def beat_s4(self):
        with self.narrate("s4") as tr:
            self.heading("Quarterly Compounding")
            d = P(dial(4, 0.85, ["3", "3", "3", "3"], size=28),
                  -3.0, 1.00)
            r1 = P(calc_row("1", "RATE", r"R\ \to\ \frac{R}{4}", CHALK_CYAN,
                            w=5.6, h=0.95, math_size=40), 2.65, 1.45)
            r2 = P(calc_row("2", "PERIODS", r"n\ \to\ 4n", CHALK_AMBER, w=5.6,
                            h=0.85, math_size=40), 2.65, 0.45)
            fm = P(fmath(r"A=P\left(1+\frac{R}{400}\right)^{4n}",
                         CHALK_YELLOW, 8.4, h=1.15, size=40), CX - 0.5, -0.75)
            ext = P(chip("The same rule, from 2 periods to 4.", CHALK_GREEN, 26,
                         w=9.6, h=0.6), CX, -1.88)
            tog = P(T("Rate and periods always change together.", 26,
                      CHALK_WHITE), CX, -2.42)
            tidy(r1, r2, same=True)
            tidy(r1, r2, same=True)  # auto-tidy
            self.cue(tr, "b0", d, sfx="pop")
            self.cue(tr, "b1", r1)
            self.cue(tr, "b2", r2)
            self.cue(tr, "b3", fm, ext, sfx="ding")
            self.cue(tr, "b4", tog, sfx="success")
            self.finish(tr)

    # -- 5: population -------------------------------------------------------------------------
    def beat_s5(self):
        with self.narrate("s5") as tr:
            self.heading("Population Growth")
            HS, GAP, HY = 0.80, 1.05, 1.42

            def xs(n):
                return [CX + (i - (n - 1) / 2.0) * GAP for i in range(n)]
            hs = [house(HS) for _ in range(5)]
            for h_, x in zip(hs[:3], xs(3)):
                h_.move_to([x, HY, 0])

            def grow(n):
                """Add house n and re-centre the whole row."""
                tgt = xs(n)
                anims = [h_.animate.move_to([x, HY, 0])
                         for h_, x in zip(hs[:n - 1], tgt[:n - 1])]
                hs[n - 1].move_to([tgt[n - 1], HY, 0])
                return anims + [FadeIn(hs[n - 1], shift=UP * 0.06)]
            lab = P(T("village: 6,250 people, +8% every year", 24,
                      CHALK_WHITE, max_w=9.0), CX, 0.70)
            r1 = P(calc_row("1", "AFTER 1 YEAR", r"6250\times1.08=6750",
                            CHALK_CYAN, w=8.6, h=0.80, math_size=36), CX, 0.00)
            nb = P(chip("the new total is the next base", CHALK_YELLOW, 24,
                        w=8.6, h=0.56), CX, -0.78)
            r2 = P(calc_row("2", "AFTER 2 YEARS", r"6250\times1.08^{2}=7290",
                            CHALK_GREEN, w=8.6, h=0.80, math_size=36), CX,
                   -1.52)
            strip = P(T("A repeated % rise = compound interest.", 24,
                        CHALK_WHITE, max_w=8.6), CX, -2.30)
            tidy(r1, nb, r2, same=True)
            tidy(r1, r2, same=True)  # auto-tidy
            self.cue(tr, "b0", VGroup(*hs[:3]), lab, sfx="pop")
            self.cue(tr, "b1", *grow(4), r1)
            self.cue(tr, "b2", nb)
            self.cue(tr, "b3", *grow(5), r2, sfx="ding")
            self.cue(tr, "b4", strip, sfx="success")
            self.finish(tr)

    # -- 6: depreciation ---------------------------------------------------------------------------
    def beat_s6(self):
        with self.narrate("s6") as tr:
            self.heading("Depreciation: the Mirror Image")
            top = P(chip("value falls with use and age", CHALK_YELLOW, 24),
                     -1.65, 1.80)
            b1 = segbar(5.4, [(0.9, CHALK_GREEN, "90% kept"),
                              (0.1, CHALK_PINK, "")], h=0.62, size=24)
            P(b1, -1.65, 0.85)
            b2 = segbar(5.4 * 0.9, [(0.9, CHALK_GREEN, "81% kept"),
                                    (0.1, CHALK_PINK, "")], h=0.62, size=24)
            b2.move_to(np.array([b1.get_left()[0] + b2.width / 2, 0.10, 0]))
            fm = P(fmath(r"V=P\left(1-\frac{R}{100}\right)^{n}", CHALK_YELLOW,
                         5.6, h=1.0, size=38), -1.65, -0.95)
            # a real chart: the ball's height after each bounce
            chart = BarChart(
                values=[25, 22.5, 20.25], bar_names=["0", "1", "2"],
                y_range=[0, 30, 10], y_length=2.0, x_length=3.3,
                bar_colors=[CHALK_CYAN, CHALK_AMBER, CHALK_GREEN],
                bar_width=0.6, bar_fill_opacity=0.9,
                x_axis_config={"font_size": 28, "color": CHALK_WHITE,
                               "stroke_width": 3},
                y_axis_config={"font_size": 24, "color": CHALK_WHITE,
                               "stroke_width": 3})
            vals = chart.get_bar_labels(font_size=26, color=CHALK_WHITE)
            ttl = T("ball height (m)", 24, CHALK_YELLOW)
            xl = T("bounce number", 24, CHALK_WHITE)
            bounce = VGroup(chart, vals, ttl, xl)
            ttl.next_to(chart, UP, buff=0.50)
            xl.next_to(chart, DOWN, buff=0.14)
            P(bounce, 3.45, 0.02)
            ans = P(calc_row("", "BALL", r"25\times0.9^{2}=20.25\text{ m}",
                             CHALK_GREEN, w=9.6, h=0.9, math_size=42), -1.65, -2.15)
            self.cue(tr, "b0", top, sfx="pop")
            self.cue(tr, "b1", b1)
            self.cue(tr, "b2", b2)
            self.cue(tr, "b3", fm, sfx="ding")
            self.cue(tr, "b4", bounce, ans, sfx="success")
            self.finish(tr)

    # -- 7: one structure ---------------------------------------------------------------------------
    def beat_s7(self):
        with self.narrate("s7") as tr:
            self.heading("One Structure, Three Uses")
            up = VGroup(panel(4.8, 2.3, CHALK_GREEN),
                        VGroup(T("GROWTH", 32, CHALK_GREEN),
                               M(r"P\left(1+r\right)^{n}", 54, CHALK_WHITE),
                               T("money and population", 24, CHALK_WHITE)
                               ).arrange(DOWN, buff=0.14))
            up[1].move_to(up[0])
            dn = VGroup(panel(4.8, 2.3, CHALK_PINK),
                        VGroup(T("DEPRECIATION", 32, CHALK_PINK),
                               M(r"P\left(1-r\right)^{n}", 54, CHALK_WHITE),
                               T("value that falls", 24, CHALK_WHITE)
                               ).arrange(DOWN, buff=0.14))
            dn[1].move_to(dn[0])
            P(up, CX - 2.55, 0.85)
            P(dn, CX + 2.55, 0.85)
            g1 = P(chip("multiplier > 1: it grows", CHALK_GREEN, 26, w=4.8),
                   CX - 2.55, -0.60)
            g2 = P(chip("multiplier < 1: it falls", CHALK_PINK, 26, w=4.8),
                   CX + 2.55, -0.60)
            strip = P(lines(["Two separate decisions:",
                             "HOW OFTEN it updates, and UP or DOWN."], 28,
                            CHALK_YELLOW, buff=0.10, max_w=9.6), CX, -1.75)
            up.box, dn.box = up[0], dn[0]
            tidy(up, dn, same=True)
            tidy(g1, g2, same=True)
            tidy(g1, g2, same=True)  # auto-tidy
            self.cue(tr, "b0", up, sfx="pop")
            self.cue(tr, "b1", dn)
            self.cue(tr, "b2", g1)
            self.cue(tr, "b3", g2)
            self.cue(tr, "b4", strip, sfx="success")
            self.finish(tr)

    # -- 8: decision map ------------------------------------------------------------------------------
    def beat_s8(self):
        with self.narrate("s8") as tr:
            self.heading("The Decision Map")
            specs = [("1", "PERIOD", "find the conversion period", CHALK_CYAN),
                     ("2", "RATE", "the rate for ONE period", CHALK_GREEN),
                     ("3", "COUNT", "the number of periods", CHALK_AMBER),
                     ("4", "SIGN", "plus grows, minus falls", CHALK_PINK),
                     ("5", "REPEAT", "apply that factor again", CHALK_PURPLE)]
            rows = [step_row(*s, h=0.74, size=26) for s in specs]
            for r, y in zip(rows, (1.66, 0.84, 0.02, -0.80, -1.62)):
                P(r, CX, y)
            strip = P(T("Period, rate, factor, repeat.", 30, CHALK_YELLOW),
                      CX, -2.40)
            tidy(*rows, same=True)
            tidy(*rows, same=True)  # auto-tidy
            for k, r in enumerate(rows):
                self.cue(tr, f"b{k}", r, sfx="pop" if k == 0 else "click")
            self.cue(tr, "b5", strip, sfx="success")
            self.finish(tr)

    # -- 9: your turn -----------------------------------------------------------------------------------
    def beat_s9(self):
        with self.narrate("s9q") as tr:
            self.heading("YOUR TURN", "Three questions and a check.", CHALK_PINK)
            qa = q_card(coin_stack(4, 0.5), "A  HALF-YEARLY",
                        ["Rs 12,000, 10% p.a.", "1.5 years: amount"], CHALK_CYAN)
            qb = q_card(dial(4, 0.5, None), "B  QUARTERLY",
                        ["12% p.a., 2 years:", "rate? periods?"], CHALK_GREEN)
            qc = q_card(tv(1.3), "C  DEPRECIATION",
                        ["Rs 21,000, loses", "5% in a year: value"], CHALK_AMBER)
            qd = q_card(block(1.0, 0.7, CHALK_PINK, "8%", 30), "D  FACTORS",
                        ["growth 8% vs", "depreciation 8%?"], CHALK_PINK)
            for q, (dx, y) in zip((qa, qb, qc, qd),
                                  [(-2.5, 0.70), (2.5, 0.70), (-2.5, -1.32),
                                   (2.5, -1.32)]):
                P(q, CX + dx, y)
            tidy(qa, qb, qc, qd, same=True)
            for q_ in (qa, qb, qc, qd):
                q_.scale(0.90)
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
                calc_row("A", "", r"12000\times1.05^{3}=\text{Rs }13891.50",
                         CHALK_CYAN, w=9.6, h=0.85, math_size=40),
                calc_row("B", "", r"\frac{12}{4}=3\%,\ \ 2\times4=8\ "
                         r"\text{periods}", CHALK_GREEN, w=9.6, h=1.0,
                         math_size=38),
                calc_row("C", "", r"21000\times0.95=\text{Rs }19950",
                         CHALK_AMBER, w=9.6, h=0.85, math_size=40),
                calc_row("D", "", r"\text{growth }1.08,\ \ \text{depreciation }"
                         r"0.92", CHALK_PINK, w=9.6, h=0.85, math_size=40),
            ]
            for r, y in zip(rows, (1.15, 0.15, -0.80, -1.72)):
                P(r, CX, y)
            tidy(*rows, same=True)
            qa, qb, qc, qd = self._qs
            tidy(*rows, same=True)  # auto-tidy
            self.cue(tr, "b0", FadeOut(qa), FadeOut(qb), FadeOut(qc),
                     FadeOut(qd), FadeIn(rows[0]), sfx="click", rt=0.6)
            self.cue(tr, "b1", rows[1])
            self.cue(tr, "b2", rows[2])
            self.cue(tr, "b3", rows[3], sfx="success")
            self.finish(tr)

    # -- 10: summary board -------------------------------------------------------------------------------
    def beat_s10(self):
        with self.narrate("s10") as tr:
            self.heading("The Whole Lesson on One Board")
            r1 = P(calc_row("", "ANNUAL", r"R,\ \ n", CHALK_CYAN, w=5.4,
                            h=0.85, math_size=38), -1.70, 1.35)
            r2 = P(calc_row("", "HALF-YEARLY", r"\frac{R}{2},\ \ 2n",
                            CHALK_AMBER, w=5.4, h=0.95, math_size=34), -1.70,
                   0.35)
            r3 = P(calc_row("", "QUARTERLY", r"\frac{R}{4},\ \ 4n",
                            CHALK_GREEN, w=5.4, h=0.95, math_size=34), -1.70,
                   -0.65)
            g = P(fmath(r"A=P\left(1+\frac{R}{100}\right)^{n}", CHALK_GREEN,
                        4.0, h=1.15, size=32), 3.45, 1.05)
            d = P(fmath(r"V=P\left(1-\frac{R}{100}\right)^{n}", CHALK_PINK,
                        4.0, h=1.15, size=32), 3.45, -0.30)
            chips = [chip(t, c, 24, w=1.85, h=0.7) for t, c in
                     (("PERIOD", CHALK_CYAN), ("RATE", CHALK_GREEN),
                      ("COUNT", CHALK_AMBER), ("+ OR -", CHALK_PINK),
                      ("REPEAT", CHALK_PURPLE))]
            steps = hrow(*chips, y=-1.80, gap=0.12)
            lab = P(T("the five steps", 26, CHALK_WHITE), CX, -2.40)
            tidy(r1, r2, r3, same=True)
            tidy(g, d, same=True)
            tidy(r1, r2, r3, same=True)  # auto-tidy
            self.cue(tr, "b0", r1, sfx="pop")
            self.cue(tr, "b1", r2)
            self.cue(tr, "b2", r3)
            self.cue(tr, "b3", g, sfx="click")
            self.cue(tr, "b4", d)
            self.cue(tr, "b5", steps, lab, sfx="success")
            self.finish(tr)

    # -- 11: recap + thanks ---------------------------------------------------------------------------------
    def beat_s11(self):
        with self.narrate("s11") as tr:
            head = self.heading("Period, Rate, Factor, Repeat")
            rows = [
                step_row("1", "CLOCK", "annual, half-yearly, quarterly",
                         CHALK_CYAN, h=0.88),
                calc_row("2", "GROWTH", r"P\left(1+\frac{R}{100}\right)^{n}",
                         CHALK_GREEN, w=9.6, h=0.95, math_size=38),
                calc_row("3", "FALL", r"P\left(1-\frac{R}{100}\right)^{n}",
                         CHALK_PINK, w=9.6, h=0.95, math_size=38),
                step_row("4", "TWO CHOICES", "how often, and up or down",
                         CHALK_AMBER, h=0.88),
            ]
            for r, y in zip(rows, (1.60, 0.60, -0.45, -1.45)):
                P(r, CX, y)
            strip = P(T("Period, rate, factor, repeat.", 30, CHALK_YELLOW),
                      CX, -2.30)
            thanks = P(T("Thank You for Watching!", 56, CHALK_WHITE,
                         max_w=9.4), CX, 0.55)
            bye = P(T("See you in the next lesson :)", 40, CHALK_YELLOW,
                      max_w=9.0), CX, -0.65)
            tidy(*rows, same=True)
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

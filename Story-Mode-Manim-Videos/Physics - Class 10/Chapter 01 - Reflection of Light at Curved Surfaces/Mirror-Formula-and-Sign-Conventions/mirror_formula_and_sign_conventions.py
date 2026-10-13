"""
Mirror Formula & Sign Conventions: How to Choose u, v and f Correctly
Story-mode chalkboard lesson (Class 10 Physics, TG Board, Chapter 1:
Reflection of Light at Curved Surfaces).

LLM KEY / FUNCTION NAME: mirror_formula_and_sign_conventions

Storyboard: storyboard.md (next to this file).  The one idea the video makes
unavoidable:  SIGN FIRST, SUBSTITUTE SECOND.

  * ONE persistent signed principal axis: the pole P is zero, the direction
    of the incident light is positive, the opposite direction is negative
    (the textbook's convention; every distance is measured from P);
  * a realistic silvered concave mirror, a lit candle as the object, the two
    principal rays, a real inverted image caught on a screen;
  * textbook example: u = -25 cm, f = -15 cm  ->  v = -37.5 cm;
  * the rule is taught as a DIRECTION rule (a small flipped diagram shows
    that "left / right" does not matter);
  * magnification is left out on purpose (a separate lesson);
  * the challenge uses the series' ten-second THINK clock (small, top right,
    the question stays fully visible).

Production rules kept: everything inside the green board, larger type
(TEXT_SCALE 0.92), boxes that hug their text, nothing on the corner badges,
every picture appears when the voice reaches its bookmark.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_PHYS = next(p for p in _HERE.parents if (p / "phys_kit.py").exists())
if str(_PHYS) not in sys.path:
    sys.path.insert(0, str(_PHYS))

from phys_kit import *  # noqa: F401,F403,E402

NARRATION = {
    "title": (
        "Mirror formula and sign conventions. <bookmark mark='b0'/> How to "
        "choose u, v and f correctly."
    ),
    "s1": (
        "The mirror formula is easy to write: one over f equals one over v "
        "plus one over u. <bookmark mark='b0'/> A student reads the problem: "
        "the object distance is twenty five centimetres, the focal length is "
        "fifteen centimetres, find the image distance. <bookmark mark='b1'/> "
        "And starts substituting straight away. <bookmark mark='b2'/> Stop. "
        "Are these distances positive or negative? <bookmark mark='b3'/> The "
        "numbers are not enough, their directions matter. <bookmark "
        "mark='b4'/> So remember: sign first, substitute second."
    ),
    "s2": (
        "Every mirror distance starts at one point: the pole, P. <bookmark "
        "mark='b0'/> Think of the pole as zero on a number line. <bookmark "
        "mark='b1'/> The object distance, the focal length and the image "
        "distance are all measured from P. <bookmark mark='b2'/> Not from the "
        "focus, not from the centre of curvature, and not from the object. "
        "<bookmark mark='b3'/> So start every mirror distance at P."
    ),
    "s3": (
        "Now the direction. Light from the object travels towards the "
        "mirror. <bookmark mark='b0'/> Look at the direction in which the "
        "incident light travels. <bookmark mark='b1'/> Distances measured in "
        "that direction are positive. <bookmark mark='b2'/> Distances "
        "measured against the incident light are negative. <bookmark "
        "mark='b3'/> So: follow the light, plus. Go against the light, minus. "
        "<bookmark mark='b4'/> Even if we flip the picture, the rule still "
        "holds, because it depends on the direction of the light, not on "
        "left or right."
    ),
    "s4": (
        "Now apply it. The object is twenty five centimetres from the pole. "
        "<bookmark mark='b0'/> Travel from P to the object: that is against "
        "the incident light, so u is minus twenty five centimetres. "
        "<bookmark mark='b1'/> The focus is fifteen centimetres from the "
        "pole, again against the incident light, so f is minus fifteen "
        "centimetres. <bookmark mark='b2'/> Magnitude plus direction gives "
        "the signed distance. <bookmark mark='b3'/> Do not just memorise "
        "concave means minus. Trace the distance from P and check its "
        "direction."
    ),
    "s5": (
        "Before calculating, let us predict where the image forms. "
        "<bookmark mark='b0'/> A ray parallel to the principal axis reflects "
        "through the focus. <bookmark mark='b1'/> A ray passing through the "
        "focus reflects parallel to the axis. <bookmark mark='b2'/> The two "
        "reflected rays meet in front of the mirror, on the same side as the "
        "object. This is a real image. <bookmark mark='b3'/> The distance "
        "from P to the image is against the incident light, so v will be "
        "negative. <bookmark mark='b4'/> Can the formula confirm this?"
    ),
    "s6": (
        "The mirror formula uses signed distances. <bookmark mark='b0'/> "
        "Here are our three quantities: u is minus twenty five, f is minus "
        "fifteen, and v is unknown. <bookmark mark='b1'/> Each one passes a "
        "sign check before it enters the formula. <bookmark mark='b2'/> Now "
        "substitute: one over minus fifteen equals one over v plus one over "
        "minus twenty five. <bookmark mark='b3'/> Signs are part of the data."
    ),
    "s7": (
        "Let us solve it step by step. <bookmark mark='b0'/> Start with one "
        "over f equals one over v plus one over u. <bookmark mark='b1'/> "
        "Substitute: minus one over fifteen equals one over v minus one over "
        "twenty five. <bookmark mark='b2'/> Move the object-distance term "
        "across: one over v equals minus one over fifteen plus one over "
        "twenty five. <bookmark mark='b3'/> The L C M of fifteen and twenty "
        "five is seventy five: minus five over seventy five plus three over "
        "seventy five. <bookmark mark='b4'/> That is minus two over seventy "
        "five. <bookmark mark='b5'/> Invert both sides: v equals minus "
        "seventy five over two. <bookmark mark='b6'/> So v equals minus "
        "thirty seven point five centimetres. <bookmark mark='b7'/> But what "
        "does the minus sign actually tell us?"
    ),
    "s8": (
        "Now put the answer back on the diagram. <bookmark mark='b0'/> The "
        "magnitude, thirty seven point five centimetres, tells us how far "
        "the image is from the pole. <bookmark mark='b1'/> The minus sign "
        "tells us the direction: against the incident light, on the same "
        "side as the object. <bookmark mark='b2'/> A screen placed there "
        "catches a sharp, real image. <bookmark mark='b3'/> The number tells "
        "us how far. The sign tells us which direction."
    ),
    "s9q": (
        "Your turn. Sign before formula. <bookmark mark='b0'/> A: an object "
        "is thirty centimetres in front of a concave mirror. What is u? "
        "<bookmark mark='b1'/> B: the focus is twenty centimetres in front "
        "of the mirror. What is f? <bookmark mark='b2'/> C: a calculation "
        "gives v equals minus forty centimetres. Which side of P is the "
        "image? <bookmark mark='b3'/> D: put these five steps in the correct "
        "order. Take your time, and pause the video if you need to."
    ),
    "s9a": (
        "Let us check. <bookmark mark='b0'/> A: the object is against the "
        "incident light, so u is minus thirty centimetres. <bookmark "
        "mark='b1'/> B: the focus is also against the light, so f is minus "
        "twenty centimetres. <bookmark mark='b2'/> C: a negative v means the "
        "image is against the incident light, forty centimetres from P. "
        "<bookmark mark='b3'/> D: mark P, find the direction of the light, "
        "assign the signs, substitute, then solve."
    ),
    "s10": (
        "Here is the whole method. <bookmark mark='b0'/> Step one: mark P as "
        "the origin. <bookmark mark='b1'/> Step two: find the direction of "
        "the incident light. <bookmark mark='b2'/> Step three: assign plus "
        "and minus. With the light is plus, against the light is minus. "
        "<bookmark mark='b3'/> Step four: write the signed values, u is "
        "minus twenty five and f is minus fifteen. <bookmark mark='b4'/> "
        "Step five: use the mirror formula. <bookmark mark='b5'/> Step six: "
        "v is minus thirty seven point five centimetres, and we put it back "
        "on the diagram. <bookmark mark='b6'/> Pole, direction, signs, "
        "formula, interpret. <bookmark mark='b7'/> Sign first, substitute "
        "second. <bookmark mark='b8'/> Thank you for watching, <bookmark "
        "mark='b9'/> and see you in the next lesson."
    ),
}

# ------------------------------------------------------------- geometry ------
PXM = -5.30                    # x of the pole P
AY = 0.35                      # y of the principal axis
K = 0.20                       # board units per centimetre
RY = -1.70                     # y of the signed ruler under the axis
PX, PW, PAN_TOP = 4.69, 3.50, 2.45     # right-hand panel
BX = -1.85                     # centre of the diagram zone (for banners)
PLUS, MINUS, LIGHT = CHALK_GREEN, "#FF7B7B", CHALK_YELLOW
MIN = "−"                 # a proper minus sign

U_CM, F_CM, V_CM, H_CM = 25.0, 15.0, 37.5, 4.0
HO = H_CM * K                  # object height on the board (0.8)
HI = HO * V_CM / U_CM          # image height (inverted, 1.5 x)


def xd(d):
    """board x of the point d cm to the right of P"""
    return PXM + K * d


def fitchip(txt, col, size, h=0.52):
    """A chip whose width follows its text."""
    lab = T(txt, size, col)
    box = panel(lab.width + 0.42, h, col, radius=0.14, stroke=2.4)
    lab.move_to(box.get_center())
    c = VGroup(box, lab)
    c.box, c.label = box, lab
    c._tight = True
    return c


def mm(tex, size=34, col=CHALK_WHITE):
    return M(tex, size, col)


class MirrorFormulaAndSignConventionsStory(PhysScene):
    NARRATION = NARRATION
    CLOCK_AT = (5.70, 2.55)        # small THINK clock, top right, no dimming
    BEATS = ("title", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9",
             "s10")

    # ------------------------------------------------- the persistent set -----
    def base(self, ruler=True, obj=True, dim=1.0, letters=True):
        """Mirror, principal axis, F / C marks, candle and the signed ruler."""
        mir = concave_mirror(PXM, AY, 6.0, 1.30, 1)
        axis = Line([PXM, AY, 0], [2.85, AY, 0], stroke_color=CHALK_WHITE,
                    stroke_width=2.4, stroke_opacity=0.9)
        parts = [axis, mir]
        marks = VGroup()
        if letters:
            for d, nm in ((0, "P"), (F_CM, "F"), (2 * F_CM, "C")):
                marks.add(Dot([xd(d), AY, 0], radius=0.055, color=CHALK_WHITE))
                marks.add(T(nm, 20, CHALK_WHITE).move_to(
                    [xd(d) + (0.22 if d == 0 else 0), AY + 0.30, 0]))
        parts.append(marks)
        cand = candle(HO).shift([xd(U_CM), AY, 0]) if obj else None
        if cand is not None:
            parts.append(cand)
        rul = None
        if ruler:
            rul = self.ruler()
            parts.append(rul)
        grp = Group(*parts)
        if dim < 1.0:
            grp.set_opacity(dim)
        self.add(grp)
        grp.mir, grp.axis, grp.marks, grp.cand, grp.rul = mir, axis, marks, cand, rul
        return grp

    def ruler(self):
        """The signed number line: P = 0, + towards the light, - against it."""
        x0, x1 = PXM - 1.05, xd(42)
        line = Line([x0, RY, 0], [x1, RY, 0], stroke_color=CHALK_WHITE,
                    stroke_width=3)
        ltip = arrow([x0 + 0.5, RY, 0], [x0, RY, 0], CHALK_WHITE, 3, 0.2)
        rtip = arrow([x1 - 0.5, RY, 0], [x1, RY, 0], CHALK_WHITE, 3, 0.2)
        g = VGroup(line, ltip, rtip)
        g.add(Line([PXM, RY - 0.13, 0], [PXM, RY + 0.13, 0],
                   stroke_color=CHALK_YELLOW, stroke_width=4))
        g.add(mm("0", 30, CHALK_YELLOW).move_to([PXM, RY - 0.38, 0]))
        for d in (10, 20, 30, 40):
            g.add(Line([xd(d), RY - 0.10, 0], [xd(d), RY + 0.10, 0],
                       stroke_color=CHALK_WHITE, stroke_width=2.6))
            g.add(mm(f"-{d}", 30).move_to([xd(d), RY - 0.38, 0]))
        g.sign_plus = T("+", 34, PLUS).move_to([PXM - 0.78, RY + 0.32, 0])
        g.sign_minus = T(MIN, 34, MINUS).move_to([xd(42) - 0.32, RY + 0.32, 0])
        g.add(g.sign_plus, g.sign_minus)
        return g

    def banner(self, txt, col=CHALK_YELLOW, size=24, y=-2.62, x=BX):
        c = chip(txt, col, size)
        c._tight = True
        return P(c, x, y)

    def incident(self, x_from=1.75, x_to=-4.35, y=1.85):
        """The 'direction of incident light' arrow along the top."""
        a = arrow([x_from, y, 0], [x_to, y, 0], LIGHT, 7, 0.28)
        lab = T("INCIDENT LIGHT", 20, LIGHT).move_to([(x_from + x_to) / 2,
                                                      y + 0.32, 0])
        return VGroup(a, lab)

    def dist_arrow(self, d, y, col, dashed=False):
        a = arrow([PXM, y, 0], [xd(d), y, 0], col, 4.5, 0.2)
        if dashed:
            a = VGroup(DashedLine([PXM, y, 0], [xd(d) - 0.2, y, 0],
                                  stroke_color=col, stroke_width=4.5,
                                  dash_length=0.15),
                       arrow([xd(d) - 0.35, y, 0], [xd(d), y, 0], col, 4.5, 0.2))
        return a

    # ------------------------------------------------------------ title ------
    def beat_title(self):
        with self.narrate("title") as tr:
            main = P(T("Mirror Formula &", 58, CHALK_AMBER, max_w=11.4), CX, 1.85)
            main2 = P(T("Sign Conventions", 58, CHALK_AMBER, max_w=11.4), CX, 1.05)
            mir = concave_mirror(CX - 2.9, -0.45, 4.0, 0.85, 1)
            cd = candle(0.70).shift([CX - 0.2, -0.45, 0])
            rule = Line([CX - 3.6, -1.75, 0], [CX + 3.6, -1.75, 0],
                        stroke_color=CHALK_GREEN, stroke_width=4)
            sub = P(T("How to Choose u, v and f Correctly", 34, CHALK_WHITE,
                      max_w=11.0), CX, -2.35)
            self.show(VGroup(main, main2), rt=0.7)
            self.cue(tr, "b0", FadeIn(mir), FadeIn(cd), rule, sub, sfx="ding",
                     rt=0.8)
            self.finish(tr)

    # ------------------------------------------------------------ scene 1 ----
    def beat_s1(self):
        with self.narrate("s1") as tr:
            self.heading("The Signs Are the Real Trap")
            self.base(ruler=False)
            f_card = VGroup(panel(PW, 1.25, CHALK_CYAN),
                            mm(r"\frac1f=\frac1v+\frac1u", 52, CHALK_WHITE))
            f_card[1].move_to(f_card[0])
            f_card.box = f_card[0]
            f_card._tight = True
            P(f_card, PX, 1.78)
            cards = []
            for k, (hd, bd, col) in enumerate((
                    ("OBJECT DISTANCE", "25 cm", CHALK_CYAN),
                    ("FOCAL LENGTH", "15 cm", CHALK_AMBER),
                    ("IMAGE DISTANCE", "?", CHALK_PINK))):
                c = tcard(hd, [bd], col, w=2.85, head_size=22, body_size=30,
                          pad=0.14, gap=0.06)
                c._tight = True
                P(c, -4.72 + 3.0 * k, -2.05)
                cards.append(c)
            subst = mm(r"\frac1{15}=\frac1v+\frac1{25}", 44, CHALK_WHITE)
            P(subst, PX, 0.25)
            stop = pchip("STOP", CHALK_RED, 46, h=0.95)
            P(stop, PX, -0.95)
            q = pcard("", ["ARE THESE DISTANCES", "+ OR " + MIN + " ?"], CHALK_PINK,
                      size=22)
            P(q, PX, -0.95)
            signs = VGroup()
            for c in cards:
                s_ = T("+ ?   " + MIN + " ?", 22, CHALK_PINK)
                s_.move_to(c.get_top() + UP * 0.30)
                signs.add(s_)
            rule = pchip("SIGN FIRST\nSUBSTITUTE SECOND", CHALK_YELLOW, 22)
            P(rule, PX, -2.35)
            self.cue(tr, "b0", FadeIn(f_card), sfx="pop")
            self.cue(tr, "b1", *[FadeIn(c) for c in cards], sfx="click")
            self.cue(tr, "b2", FadeIn(subst), FadeIn(stop, scale=1.3), sfx="ding")
            self.cue(tr, "b3", ReplacementTransform(stop, q), FadeIn(signs),
                     sfx="click")
            self.cue(tr, "b4", FadeIn(rule), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 2 ----
    def beat_s2(self):
        with self.narrate("s2") as tr:
            self.heading("Every Distance Starts at the Pole")
            g = self.base(ruler=True, dim=0.35)
            ring = Circle(radius=0.30, stroke_color=CHALK_YELLOW, stroke_width=5,
                          fill_color=CHALK_YELLOW, fill_opacity=0.18)
            ring.move_to([PXM, AY, 0])
            ptag = pchip("POLE = REFERENCE\nPOINT", CHALK_YELLOW, 24)
            P(ptag, PX, 1.7)
            zero = pchip("P = 0", CHALK_YELLOW, 34, h=0.75)
            P(zero, PX, 0.55)
            a_f = self.dist_arrow(F_CM, AY - 0.55, CHALK_AMBER)
            a_o = self.dist_arrow(U_CM, AY - 0.95, CHALK_CYAN)
            a_i = self.dist_arrow(36, AY - 1.35, CHALK_PINK, dashed=True)
            l_f = T("15 cm", 20, CHALK_AMBER).move_to([xd(F_CM) + 0.65, AY - 0.55, 0])
            l_o = T("25 cm", 20, CHALK_CYAN).move_to([xd(U_CM) + 0.65, AY - 0.95, 0])
            l_i = T("v = ?", 20, CHALK_PINK).move_to([xd(36) + 0.5, AY - 1.35, 0])
            wrong = DashedLine([xd(F_CM), AY - 0.30, 0], [xd(U_CM), AY - 0.30, 0],
                               stroke_color=CHALK_RED, stroke_width=4.5)
            cross = cross_mark([(xd(F_CM) + xd(U_CM)) / 2, AY - 0.30, 0], 0.22)
            wlab = T("NOT FROM F", 20, CHALK_RED).move_to(
                [(xd(F_CM) + xd(U_CM)) / 2, AY - 0.68 - 0.0, 0])
            wlab.shift(DOWN * 0.0)
            ban = self.banner("START EVERY MIRROR DISTANCE AT P")
            self.cue(tr, "b0", FadeIn(ring), FadeIn(ptag), sfx="pop")
            self.cue(tr, "b1", g.animate.set_opacity(1), FadeIn(zero),
                     sfx="ding")
            self.cue(tr, "b2", FadeIn(a_f), FadeIn(l_f), FadeIn(a_o),
                     FadeIn(l_o), FadeIn(a_i), FadeIn(l_i), sfx="click")
            self.cue(tr, "b3", FadeOut(a_f), FadeOut(l_f), FadeOut(a_o),
                     FadeOut(l_o), FadeOut(a_i), FadeOut(l_i), FadeIn(wrong),
                     FadeIn(cross), sfx="click")
            self.go(FadeOut(wrong), FadeOut(cross), rt=0.5)
            self.cue(tr, "b3", FadeIn(ban), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 3 ----
    def beat_s3(self):
        with self.narrate("s3") as tr:
            self.heading("Incident Light Decides the Signs")
            g = self.base(ruler=True)
            inc = self.incident()
            plus_band = Line([PXM, RY + 0.55, 0], [PXM - 1.0, RY + 0.55, 0],
                             stroke_color=PLUS, stroke_width=6)
            plus_arr = arrow([PXM - 0.15, RY + 0.55, 0], [PXM - 1.0, RY + 0.55, 0],
                             PLUS, 6, 0.2)
            minus_arr = arrow([PXM + 0.2, RY + 0.55, 0], [xd(42) - 0.55, RY + 0.55, 0],
                              MINUS, 6, 0.22)
            sw = lines(["WITH THE", "LIGHT"], 16, PLUS, buff=0.02).move_to([PXM - 0.65, RY + 0.98, 0])
            sa = T("AGAINST THE LIGHT", 20, MINUS).move_to([xd(20), RY + 0.95, 0])
            w_ = pchip("WITH THE LIGHT: +", PLUS, 22)
            a_ = pchip("AGAINST THE LIGHT: " + MIN, MINUS, 22)
            card = pcard("", ["FOLLOW THE LIGHT: +", "GO AGAINST IT: " + MIN],
                         CHALK_YELLOW, size=22)
            stack([w_, a_, card], top=PAN_TOP, gap=0.20)
            # the flipped drawing: mirror on the right, light to the right
            fx = 5.55
            fm = concave_mirror(fx, -1.55, 3.0, 0.95, -1)
            faxis = Line([3.15, -1.55, 0], [fx, -1.55, 0], stroke_color=CHALK_WHITE,
                         stroke_width=2.2)
            fa = arrow([3.5, -0.50, 0], [5.0, -0.50, 0], LIGHT, 5, 0.22)
            fp = T("+", 30, PLUS).move_to([5.0, -2.25, 0])
            fmn = T(MIN, 30, MINUS).move_to([3.45, -2.25, 0])
            fl = Line([3.25, -2.25, 0], [5.3, -2.25, 0], stroke_color=CHALK_WHITE,
                      stroke_width=2.4)
            fcand = candle(0.42).shift([3.7, -1.55, 0])
            flab = T("SAME RULE, FLIPPED PICTURE", 16, CHALK_YELLOW)
            fit(flab, 3.3)
            flab.move_to([PX, -0.05, 0])
            flip = VGroup(fm, faxis, fa, fp, fmn, fl, fcand, flab)
            self.cue(tr, "b0", FadeIn(inc), sfx="whoosh")
            self.cue(tr, "b1", Indicate(inc[0], color=CHALK_WHITE,
                                        scale_factor=1.08), sfx="click")
            self.cue(tr, "b2", FadeIn(plus_arr), FadeIn(sw), FadeIn(w_),
                     sfx="ding")
            self.cue(tr, "b3", FadeIn(minus_arr), FadeIn(sa), FadeIn(a_),
                     sfx="ding")
            self.cue(tr, "b4", FadeIn(card), sfx="success")
            self.cue(tr, "b4", FadeIn(flip), sfx=None)
            self.finish(tr)

    # ------------------------------------------------------------ scene 4 ----
    def beat_s4(self):
        with self.narrate("s4") as tr:
            self.heading("Sign u and f Before Calculating")
            g = self.base(ruler=True)
            inc = self.incident()
            self.add(inc)
            a_o = self.dist_arrow(U_CM, AY - 0.95, CHALK_CYAN)
            a_f = self.dist_arrow(F_CM, AY - 0.55, CHALK_AMBER)
            m_o = T("25 cm", 22, CHALK_CYAN).move_to([xd(U_CM) + 0.7, AY - 0.95, 0])
            m_f = T("15 cm", 22, CHALK_AMBER).move_to([xd(F_CM) + 0.7, AY - 0.55, 0])
            s_o = mm(r"u=-25\text{ cm}", 32, CHALK_CYAN).move_to(
                [xd(U_CM) + 1.1, AY - 0.95, 0])
            s_f = mm(r"f=-15\text{ cm}", 32, CHALK_AMBER).move_to(
                [xd(F_CM) + 1.1, AY - 0.55, 0])
            c_u = pcard("OBJECT DISTANCE u", ["25 cm, against the light",
                                              "u = " + MIN + "25 cm"],
                        CHALK_CYAN, size=21, head_size=22)
            c_f = pcard("FOCAL LENGTH f", ["15 cm, against the light",
                                           "f = " + MIN + "15 cm"],
                        CHALK_AMBER, size=21, head_size=22)
            eq = pcard("", ["MAGNITUDE", "+ DIRECTION", "= SIGNED DISTANCE"],
                       CHALK_GREEN, size=21)
            stack([c_u, c_f, eq], top=PAN_TOP, gap=0.18)
            ban = self.banner("TRACE THE DISTANCE FROM P  ·  CHECK ITS DIRECTION",
                              size=22)
            self.cue(tr, "b0", FadeIn(a_o), FadeIn(m_o), sfx="whoosh")
            self.cue(tr, "b1", ReplacementTransform(m_o, s_o), FadeIn(c_u),
                     sfx="ding")
            self.cue(tr, "b2", FadeIn(a_f), FadeIn(m_f), sfx="whoosh")
            self.go(ReplacementTransform(m_f, s_f), FadeIn(c_f), rt=0.6)
            self.cue(tr, "b3", FadeIn(eq), sfx="click")
            self.cue(tr, "b3", FadeIn(ban), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 5 ----
    def beat_s5(self):
        with self.narrate("s5") as tr:
            self.heading("Where Will the Image Form?")
            g = self.base(ruler=True)
            ty = AY + HO
            iy = AY - HI
            ix = xd(V_CM)
            Tp = (xd(U_CM), ty)
            m1 = (PXM + sag(HO), ty)
            m2 = (PXM + sag(HI), iy)
            r1 = VGroup(ray([Tp, m1], CHALK_YELLOW),
                        ray([m1, (ix, iy)], CHALK_YELLOW))
            r2 = VGroup(ray([Tp, m2], CHALK_CYAN),
                        ray([m2, (ix, iy)], CHALK_CYAN))
            img = candle(HI).rotate(PI, axis=RIGHT, about_point=ORIGIN)
            img.shift([ix, AY, 0])
            img_t = T("I", 22, CHALK_PINK).move_to([ix + 0.32, iy - 0.05, 0])
            a_i = self.dist_arrow(V_CM, AY - 1.45, CHALK_PINK)
            l1 = pchip("PARALLEL RAY\n" + "→ THROUGH F", CHALK_YELLOW, 20)
            l2 = pchip("RAY THROUGH F\n" + "→ PARALLEL", CHALK_CYAN, 20)
            l3 = pchip("REAL IMAGE", CHALK_PINK, 24, h=0.6)
            l4 = pchip("AGAINST THE LIGHT\n" + "v < 0", MINUS, 24)
            q = pcard("", ["CAN THE FORMULA", "CONFIRM THIS?"], CHALK_PINK,
                      size=24)
            stack([l1, l2, l3, l4, q], top=PAN_TOP, gap=0.16)
            self.cue(tr, "b0", FadeIn(r1), FadeIn(l1), sfx="whoosh", rt=0.9)
            self.cue(tr, "b1", FadeIn(r2), FadeIn(l2), sfx="whoosh", rt=0.9)
            self.cue(tr, "b2", FadeIn(img), FadeIn(img_t), FadeIn(l3), sfx="ding")
            self.cue(tr, "b3", FadeIn(a_i), FadeIn(l4), sfx="click")
            self.cue(tr, "b4", FadeIn(q), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 6 ----
    def beat_s6(self):
        with self.narrate("s6") as tr:
            self.heading("The Formula Uses Signed Distances")
            form = mm(r"\frac1f=\frac1v+\frac1u", 54, CHALK_WHITE)
            P(form, CX, 1.80)
            cards = []
            for k, (txt, col) in enumerate(((r"u=-25\text{ cm}", CHALK_CYAN),
                                            (r"f=-15\text{ cm}", CHALK_AMBER),
                                            (r"v=\,?", CHALK_PINK))):
                bx = panel(3.4, 1.05, col)
                tx = mm(txt, 44, col).move_to(bx)
                c = VGroup(bx, tx)
                c.box = bx
                c._tight = True
                P(c, CX - 3.9 + 3.9 * k, -0.42)
                cards.append(c)
            gate = pchip("SIGN CHECK", CHALK_YELLOW, 24, h=0.58, w=3.0)
            P(gate, CX - 1.95, 0.66)
            ticks = VGroup(tick_mark([cards[0].get_right()[0] - 0.35,
                                      cards[0].get_top()[1] - 0.0, 0], 0.2),
                           tick_mark([cards[1].get_right()[0] - 0.35,
                                      cards[1].get_top()[1] - 0.0, 0], 0.2))
            ticks.set_color(CHALK_GREEN)
            subst = mm(r"\frac1{-15}=\frac1v+\frac1{-25}", 54, CHALK_WHITE)
            P(subst, CX, -1.60)
            ban = self.banner("SIGNS ARE PART OF THE DATA", x=CX, y=-2.68)
            self.cue(tr, "b0", FadeIn(form), sfx="pop")
            self.cue(tr, "b1", *[FadeIn(c) for c in cards], sfx="click")
            self.cue(tr, "b2", FadeIn(gate), FadeIn(ticks), sfx="ding")
            self.cue(tr, "b3", FadeIn(subst), sfx="click")
            self.cue(tr, "b3", FadeIn(ban), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 7 ----
    def beat_s7(self):
        with self.narrate("s7") as tr:
            self.heading("Worked Example: Find v")
            given = VGroup()
            for k, (txt, col) in enumerate(((r"u=-25\text{ cm}", CHALK_CYAN),
                                            (r"f=-15\text{ cm}", CHALK_AMBER),
                                            (r"v=\,?", CHALK_PINK))):
                bx = panel(3.0, 0.75, col)
                tx = mm(txt, 34, col).move_to(bx)
                c = VGroup(bx, tx)
                c.box = bx
                c._tight = True
                P(c, CX - 3.45 + 3.45 * k, 1.95)
                given.add(c)
            WA, WB = 5.5, 4.6

            def row(tex, col, x, y, w, hgt=0.80, size=34):
                bx = panel(w, hgt, col, radius=0.14, stroke=2.4)
                tx = mm(tex, size, CHALK_WHITE).move_to(bx)
                r_ = VGroup(bx, tx)
                r_.box = bx
                r_._tight = True
                return P(r_, x, y)
            xa, xb = CX - 3.05, CX + 3.35
            rows = [
                row(r"\frac1f=\frac1v+\frac1u", CHALK_CYAN, xa, 1.0, WA),
                row(r"-\frac1{15}=\frac1v-\frac1{25}", CHALK_CYAN, xa, 0.08, WA),
                row(r"\frac1v=-\frac1{15}+\frac1{25}", CHALK_CYAN, xa, -0.84, WA),
                row(r"\frac1v=-\frac5{75}+\frac3{75}", CHALK_CYAN, xa, -1.76, WA),
                row(r"\frac1v=-\frac2{75}", CHALK_AMBER, xb, 1.0, WB),
                row(r"v=-\frac{75}{2}", CHALK_AMBER, xb, 0.08, WB),
            ]
            ans = VGroup(panel(WB, 1.0, CHALK_GREEN, opacity=0.9),
                         mm(r"v=-37.5\text{ cm}", 46, CHALK_GREEN))
            ans[1].move_to(ans[0])
            ans.box = ans[0]
            ans._tight = True
            P(ans, xb, -1.05)
            q = self.banner("WHAT DOES THE MINUS SIGN ACTUALLY TELL US?",
                            CHALK_PINK, 24, x=CX, y=-2.64)
            self.cue(tr, "b0", *[FadeIn(c) for c in given], sfx="pop")
            self.cue(tr, "b1", FadeIn(rows[0]), sfx="click")
            self.cue(tr, "b2", FadeIn(rows[1]), sfx="click")
            self.cue(tr, "b3", FadeIn(rows[2]), sfx="click")
            self.cue(tr, "b4", FadeIn(rows[3]), sfx="click")
            self.cue(tr, "b5", FadeIn(rows[4]), sfx="click")
            self.cue(tr, "b6", FadeIn(rows[5]), sfx="click")
            self.cue(tr, "b7", FadeIn(ans), sfx="success")
            self.cue(tr, "b7", FadeIn(q), sfx=None)
            self.finish(tr)

    # ------------------------------------------------------------ scene 8 ----
    def beat_s8(self):
        with self.narrate("s8") as tr:
            self.heading("Put the Answer Back on the Diagram")
            g = self.base(ruler=True)
            self.add(self.incident())
            iy = AY - HI
            ix = xd(V_CM)
            tick = Line([ix, RY - 0.2, 0], [ix, RY + 0.2, 0],
                        stroke_color=CHALK_PINK, stroke_width=5)
            vlab = mm(r"v=-37.5\text{ cm}", 28, CHALK_PINK).move_to(
                [ix - 0.1, RY - 0.82, 0])
            a_i = self.dist_arrow(V_CM, AY - 1.45, CHALK_PINK)
            mag = T("37.5 cm", 22, CHALK_PINK).move_to([xd(V_CM / 2), AY - 1.15, 0])
            scr = screen(ix + 0.18, AY - 0.55, 2.1)
            img = candle(HI).rotate(PI, axis=RIGHT, about_point=ORIGIN)
            img.shift([ix, AY, 0])
            c_mag = pchip("MAGNITUDE = 37.5 cm", CHALK_PINK, 22, h=0.6)
            c_min = pcard("", [], MINUS, size=20)
            minus_big = Line([-0.30, 0, 0], [0.30, 0, 0], stroke_color=MINUS, stroke_width=16)
            minus_cap = T("DIRECTION INFORMATION", 18, MINUS)
            mc = VGroup(minus_big, minus_cap).arrange(DOWN, buff=0.12)
            box_m = panel(PW, mc.height + 0.36, MINUS)
            mc.move_to(box_m)
            c_min = VGroup(box_m, mc)
            c_min.box = box_m
            c_min._tight = True
            c_scr = pchip("A SCREEN HERE CATCHES\nA SHARP, REAL IMAGE", CHALK_CYAN, 20)
            r1 = pcard("", ["THE NUMBER: HOW FAR", "THE SIGN: WHICH WAY"],
                       CHALK_YELLOW, size=21)
            stack([c_mag, c_min, c_scr, r1], top=PAN_TOP, gap=0.16)
            self.cue(tr, "b0", FadeIn(tick), FadeIn(vlab), FadeIn(a_i), FadeIn(mag),
                     FadeIn(c_mag), sfx="whoosh")
            self.cue(tr, "b1", FadeIn(c_min), Indicate(vlab, color=MINUS,
                                                       scale_factor=1.12),
                     sfx="ding")
            self.cue(tr, "b2", FadeIn(scr), FadeIn(img), FadeIn(c_scr),
                     sfx="pop")
            self.cue(tr, "b3", FadeIn(r1), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 9 ----
    def beat_s9(self):
        with self.narrate("s9q") as tr:
            self.heading("YOUR TURN", "Sign before formula.", CHALK_PINK)
            specs = [("A", "Object 30 cm in front. What is u?", CHALK_CYAN),
                     ("B", "Focus 20 cm in front. What is f?", CHALK_AMBER),
                     ("C", "A result v = " + MIN + "40 cm. Which side of P?", PLUS)]
            rows = [qa_row(l, q, "?", c, w=11.8, h=0.76, size=26)
                    for l, q, c in specs]
            for r_, y in zip(rows, (1.38, 0.50, -0.38)):
                P(r_, CX, y)
            # row D: five steps to put in order
            boxD = panel(11.8, 1.62, CHALK_PINK)
            P(boxD, CX, -1.95)
            badgeD = num_badge("D", CHALK_PINK, r=0.23, size=22)
            badgeD.move_to(boxD.get_left() + RIGHT * 0.30 + UP * 0.45)
            capD = T("Put the five steps in the correct order:", 24, CHALK_WHITE,
                     max_w=9.5)
            capD.next_to(badgeD, RIGHT, buff=0.22)
            names = ["SUBSTITUTE", "LIGHT DIRECTION", "MARK P", "ASSIGN SIGNS",
                     "SOLVE"]
            chips = [fitchip(n, CHALK_WHITE, 20) for n in names]
            order = [0, 1, 2, 3, 4]               # as shown
            gap = 0.22
            total = sum(c.box.width for c in chips) + gap * 4
            x = CX - total / 2
            for c in chips:
                c.move_to([x + c.box.width / 2, -2.30, 0])
                x += c.box.width + gap
            rowD = VGroup(boxD, badgeD, capD, *chips)
            rowD.box = boxD
            rowD._tight = True
            self.cue(tr, "b0", FadeIn(rows[0]), sfx="pop")
            self.cue(tr, "b1", FadeIn(rows[1]), sfx="click")
            self.cue(tr, "b2", FadeIn(rows[2]), sfx="click")
            self.cue(tr, "b3", FadeIn(rowD), sfx="click")
            self.finish(tr)
            self._rows, self._chips, self._ord = rows, chips, (names, gap)
        self.think_clock()
        with self.narrate("s9a", reset=False) as tr:
            ans = [("u = " + MIN + "30 cm", CHALK_CYAN),
                   ("f = " + MIN + "20 cm", CHALK_AMBER),
                   ("AGAINST THE LIGHT", PLUS)]
            for k in range(3):
                new = T(ans[k][0], 26, ans[k][1], max_w=4.3)
                new.move_to(self._rows[k].slot.get_center())
                new.align_to(self._rows[k].slot, RIGHT)
                self.cue(tr, f"b{k}", ReplacementTransform(self._rows[k].slot, new),
                         sfx="click", rt=0.5)
            names, gap = self._ord
            correct = ["MARK P", "LIGHT DIRECTION", "ASSIGN SIGNS", "SUBSTITUTE",
                       "SOLVE"]
            chips = {n: c for n, c in zip(names, self._chips)}
            total = sum(chips[n].box.width for n in correct) + gap * 4
            x = CX - total / 2
            moves = []
            for i, n in enumerate(correct):
                c = chips[n]
                tgt = [x + c.box.width / 2, -2.30, 0]
                moves.append(c.animate.move_to(tgt))
                c.box.set_stroke(CHALK_GREEN, 3)
                x += c.box.width + gap
            self.cue(tr, "b3", *moves, sfx="success", rt=1.2)
            self.finish(tr)

    # ----------------------------------------------------------- scene 10 ----
    def beat_s10(self):
        with self.narrate("s10") as tr:
            self.heading("The Whole Method")
            g = self.base(ruler=True, obj=True)
            inc = self.incident()
            steps = [("1  MARK P = 0", CHALK_YELLOW),
                     ("2  LIGHT DIRECTION", LIGHT),
                     ("3  ASSIGN + AND " + MIN, PLUS),
                     ("4  SIGNED u AND f", CHALK_CYAN),
                     ("5  MIRROR FORMULA", CHALK_AMBER),
                     ("6  READ v ON DIAGRAM", CHALK_PINK)]
            chips = [pchip(t, c, 22, h=0.56) for t, c in steps]
            stack(chips, top=PAN_TOP, gap=0.20)
            ring = Circle(radius=0.30, stroke_color=CHALK_YELLOW, stroke_width=5,
                          fill_color=CHALK_YELLOW, fill_opacity=0.18)
            ring.move_to([PXM, AY, 0])
            # plus / minus colouring on the ruler
            plus_arr = arrow([PXM - 0.15, RY + 0.55, 0], [PXM - 1.0, RY + 0.55, 0],
                             PLUS, 6, 0.2)
            minus_arr = arrow([PXM + 0.2, RY + 0.55, 0], [xd(42) - 0.55, RY + 0.55, 0],
                              MINUS, 6, 0.22)
            u_l = mm(r"u=-25", 30, CHALK_CYAN).move_to([xd(U_CM) + 0.1, AY - 0.80, 0])
            f_l = mm(r"f=-15", 30, CHALK_AMBER).move_to([xd(F_CM) - 0.05, AY - 0.80, 0])
            u_a = self.dist_arrow(U_CM, AY - 0.55, CHALK_CYAN)
            f_a = self.dist_arrow(F_CM, AY - 0.30, CHALK_AMBER)
            form = mm(r"\frac1f=\frac1v+\frac1u", 44, CHALK_WHITE)
            P(form, PX, -2.52)
            iy = AY - HI
            ix = xd(V_CM)
            scr = screen(ix + 0.18, AY - 0.55, 2.1)
            img = candle(HI).rotate(PI, axis=RIGHT, about_point=ORIGIN)
            img.shift([ix, AY, 0])
            v_l = mm(r"v=-37.5\text{ cm}", 28, CHALK_PINK).move_to(
                [ix - 0.1, RY - 0.82, 0])
            self.cue(tr, "b0", FadeIn(chips[0]), FadeIn(ring), sfx="pop")
            self.cue(tr, "b1", FadeIn(chips[1]), FadeIn(inc), sfx="whoosh")
            self.cue(tr, "b2", FadeIn(chips[2]), FadeIn(plus_arr),
                     FadeIn(minus_arr), sfx="ding")
            self.cue(tr, "b3", FadeIn(chips[3]), FadeIn(u_a), FadeIn(f_a),
                     FadeIn(u_l), FadeIn(f_l), sfx="click")
            self.cue(tr, "b4", FadeIn(chips[4]), FadeIn(form), sfx="click")
            self.cue(tr, "b5", FadeIn(chips[5]), FadeIn(scr), FadeIn(img),
                     FadeIn(v_l), sfx="success", snap="method")
            self.cue(tr, "b6", Indicate(img, color=CHALK_PINK, scale_factor=1.1),
                     sfx=None)
            self.hold(tr, "b7")
            keep = [m_ for m_ in self.mobjects if m_ not in self.fixtures]
            self.go(*[FadeOut(m_) for m_ in keep], rt=0.6)
            names = [("POLE", CHALK_YELLOW), ("DIRECTION", LIGHT),
                     ("SIGNS", PLUS), ("FORMULA", CHALK_AMBER),
                     ("INTERPRET", CHALK_PINK)]
            parts = []
            for k, (t, c) in enumerate(names):
                ch = chip(t, c, 26)
                ch._tight = True
                parts.append(ch)
                if k < len(names) - 1:
                    parts.append(arrow([0, 0, 0], [0.38, 0, 0], CHALK_WHITE, 5, 0.17))
            chain_row = VGroup(*parts).arrange(RIGHT, buff=0.14)
            fit(chain_row, 12.0)
            P(chain_row, CX, 0.65)
            slogan = P(T("SIGN FIRST. SUBSTITUTE SECOND.", 42, CHALK_YELLOW,
                         max_w=12.0), CX, -0.65)
            sub = P(T("Don't memorise the signs. Read the directions.", 28,
                      CHALK_WHITE, max_w=12.0), CX, -1.55)
            self.cue(tr, "b7", FadeIn(chain_row), FadeIn(slogan), FadeIn(sub),
                     sfx="success")
            self.hold(tr, "b8")
            self.go(FadeOut(chain_row), FadeOut(slogan), FadeOut(sub), rt=0.6)
            thanks = P(T("Thank You for Watching!", 60, CHALK_WHITE, max_w=11.8),
                       CX, 0.60)
            bye = P(T("See you in the next lesson :)", 44, CHALK_YELLOW,
                      max_w=11.0), CX, -0.75)
            self.cue(tr, "b8", FadeIn(thanks, shift=UP * 0.1), sfx=None)
            self.cue(tr, "b9", FadeIn(bye, shift=UP * 0.1), sfx=None)
            self.finish(tr)
        if not self.still:
            self.wait(END_HOLD)

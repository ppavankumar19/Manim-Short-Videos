"""
Magnification in Mirrors: Image Size, Orientation and the Formula m = -v/u
Story-mode chalkboard lesson (Class 10 Physics, TG Board, Chapter 1:
Reflection of Light at Curved Surfaces).

LLM KEY / FUNCTION NAME: mirror_magnification_image_size_and_orientation

Storyboard: storyboard.md (next to this file).  The idea made unavoidable:
    |m| tells the SIZE,  the SIGN of m tells the ORIENTATION.

  * the "magnification meter": a gauge for |m| (diminished / same size /
    enlarged) next to a live object candle and image candle;
  * heights carry signs (up +, down -), so m = h_i / h_o < 0 means inverted;
  * m = h_i/h_o = -v/u is shown as ONE relation, via the two similar
    triangles at the pole;
  * the textbook example continues the previous video:
        h_o = +4 cm, u = -25 cm, v = -37.5 cm  ->  m = -1.5, h_i = -6 cm
    (enlarged and inverted);
  * the challenge uses the series' ten-second THINK clock (small, top right,
    the questions stay fully visible).

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
        "Magnification in mirrors. <bookmark mark='b0'/> Image size, "
        "orientation, and the formula m equals minus v over u."
    ),
    "s1": (
        "One candle, and many possible images. <bookmark mark='b0'/> The "
        "image can be enlarged. <bookmark mark='b1'/> It can be the same "
        "size. <bookmark mark='b2'/> Or it can be diminished. <bookmark "
        "mark='b3'/> And sometimes the image is turned upside down: "
        "inverted. <bookmark mark='b4'/> Can one number describe both the "
        "size and the orientation? <bookmark mark='b5'/> Yes. It is called "
        "the magnification, m."
    ),
    "s2": (
        "Heights have signs too. <bookmark mark='b0'/> Measured upward from "
        "the principal axis, the object height, h o, is positive. "
        "<bookmark mark='b1'/> An upright image also has a positive height, "
        "h i. <bookmark mark='b2'/> If the image is inverted, its height is "
        "measured downward, so h i is negative. <bookmark mark='b3'/> Upward "
        "height: plus. Downward height: minus."
    ),
    "s3": (
        "Now let us build the idea of magnification. <bookmark mark='b0'/> "
        "Magnification is the height of the image divided by the height of "
        "the object. <bookmark mark='b1'/> In symbols, m equals h i over h "
        "o. <bookmark mark='b2'/> If the object is four centimetres tall and "
        "the image is eight, then eight over four is two. <bookmark "
        "mark='b3'/> The image is two times as tall as the object."
    ),
    "s4": (
        "The magnitude of m tells us the size. <bookmark mark='b0'/> If the "
        "absolute value of m is greater than one, the image is enlarged. "
        "<bookmark mark='b1'/> If it equals one, the image is the same size. "
        "<bookmark mark='b2'/> If it is less than one, the image is "
        "diminished. <bookmark mark='b3'/> So ignore the sign for a moment: "
        "the absolute value of m tells the size."
    ),
    "s5": (
        "The sign of m tells us the orientation. <bookmark mark='b0'/> Take "
        "an upright object. If the image is upright, h i is positive, so m "
        "is positive. The image is erect. <bookmark mark='b1'/> Now flip the "
        "image. Its size does not change, but h i becomes negative, so m "
        "becomes negative. The image is inverted. <bookmark mark='b2'/> The "
        "absolute value of m gives the size, and the sign of m gives the "
        "orientation."
    ),
    "s6": (
        "Why can we also write m equals minus v over u? <bookmark "
        "mark='b0'/> The textbook compares the two similar triangles formed "
        "by the object and the image at the pole of the mirror. <bookmark "
        "mark='b1'/> The height ratio turns into minus v over u. <bookmark "
        "mark='b2'/> So m equals h i over h o, which equals minus v over u. "
        "<bookmark mark='b3'/> Size information can come from heights, or "
        "from distances."
    ),
    "s7": (
        "Let us continue the textbook example from the last video. "
        "<bookmark mark='b0'/> The object height is plus four centimetres, u "
        "is minus twenty five, and v is minus thirty seven point five. "
        "<bookmark mark='b1'/> Start with h i over h o equals minus v over "
        "u. <bookmark mark='b2'/> Substitute: h i over four equals minus, "
        "minus thirty seven point five over minus twenty five. <bookmark "
        "mark='b3'/> The two minus signs inside cancel, leaving only the "
        "leading minus: minus thirty seven point five over twenty five. "
        "<bookmark mark='b4'/> That is minus one point five. So m equals "
        "minus one point five. <bookmark mark='b5'/> Then h i equals m times "
        "h o, minus one point five times four. <bookmark mark='b6'/> So h i "
        "equals minus six centimetres."
    ),
    "s8": (
        "Now read the answer physically. <bookmark mark='b0'/> The size "
        "first: six is greater than four, so the image is enlarged. "
        "<bookmark mark='b1'/> Now the sign: the minus tells us the image is "
        "below the principal axis. It is inverted. <bookmark mark='b2'/> In "
        "terms of magnification: the absolute value of m is one point five, "
        "greater than one, so enlarged. And m is negative, so inverted. "
        "<bookmark mark='b3'/> Minus one point five does not mean smaller. "
        "The size comes from the absolute value, one point five."
    ),
    "s9q": (
        "Your turn. Decode the magnification. <bookmark mark='b0'/> A: m "
        "equals plus two. What are the size and the orientation? <bookmark "
        "mark='b1'/> B: m equals minus zero point five. <bookmark "
        "mark='b2'/> C: m equals minus one. <bookmark mark='b3'/> D: u is "
        "minus twenty centimetres and v is minus forty centimetres. Find m. "
        "Take your time, and pause the video if you need to."
    ),
    "s9a": (
        "Let us check. <bookmark mark='b0'/> A: the absolute value of m is "
        "two, so enlarged. And m is positive, so erect. <bookmark "
        "mark='b1'/> B: the absolute value is zero point five, so "
        "diminished. And m is negative, so inverted. <bookmark mark='b2'/> "
        "C: the absolute value is one, so the same size. And m is negative, "
        "so inverted. <bookmark mark='b3'/> D: m equals minus v over u, "
        "which is minus two. The image is two times enlarged, and inverted."
    ),
    "s10": (
        "Here is how to decode m. <bookmark mark='b0'/> Question one: how "
        "big is the image? Look only at the absolute value of m. <bookmark "
        "mark='b1'/> Greater than one: enlarged. Equal to one: same size. "
        "Less than one: diminished. <bookmark mark='b2'/> Question two: "
        "which way does the image point? <bookmark mark='b3'/> Positive m: "
        "erect. Negative m: inverted. <bookmark mark='b4'/> In our example, "
        "m is minus one point five: enlarged, and inverted. <bookmark "
        "mark='b5'/> The magnitude of m gives the size. The sign of m gives "
        "the orientation. <bookmark mark='b6'/> So do not just calculate m. "
        "Read what m is telling you. <bookmark mark='b7'/> Thank you for "
        "watching, <bookmark mark='b8'/> and see you in the next lesson."
    ),
}

# ------------------------------------------------------------- geometry ------
PX, PW, PAN_TOP = 4.69, 3.50, 2.45     # right-hand panel
BX = -1.85                             # centre of the diagram zone
OBJC, IMGC, SIZEC = CHALK_CYAN, CHALK_PINK, CHALK_YELLOW
PLUS, MINUS = CHALK_GREEN, "#FF7B7B"
MIN = "−"
KH = 0.30                              # board units per cm (height displays)

# the mirror diagram of scene 6 (same drawing as the previous video)
PXM, AY, K = -5.30, 0.35, 0.20
U_CM, V_CM, H_CM = 25.0, 37.5, 4.0
HO, HI = H_CM * K, H_CM * K * V_CM / U_CM


def xd(d):
    return PXM + K * d


def mm(tex, size=34, col=CHALK_WHITE):
    return M(tex, size, col)


def candle_at(x, y0, h, inverted=False, op=1.0):
    c = candle(h, op)
    if inverted:
        c.rotate(PI, axis=RIGHT, about_point=ORIGIN)
    return c.shift([x, y0, 0])


def vbar(x, y0, h, col, w=0.55):
    """A vertical height bar standing on y0."""
    b = Rectangle(width=w, height=max(h, 0.02))
    paint(b, [col, col], op=0.55, lw=3, sheen=0.25, line=col)
    return b.move_to([x, y0 + h / 2, 0])


def vmeasure(x, y_from, y_to, col, w=4.5):
    return arrow([x, y_from, 0], [x, y_to, 0], col, w, 0.2)


class MirrorMagnificationImageSizeAndOrientationStory(PhysScene):
    NARRATION = NARRATION
    CLOCK_AT = (5.70, 2.55)        # small THINK clock, top right, no dimming
    BEATS = ("title", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9",
             "s10")

    def axis(self, y=0.0, x0=-6.35, x1=2.75):
        ln = Line([x0, y, 0], [x1, y, 0], stroke_color=CHALK_WHITE,
                  stroke_width=2.4, stroke_opacity=0.9)
        self.add(ln)
        return ln

    def banner(self, txt, col=CHALK_YELLOW, size=24, y=-2.62, x=BX):
        c = chip(txt, col, size)
        c._tight = True
        return P(c, x, y)

    def readout(self, tex, col, size=44, w=3.5, h=0.9):
        bx = panel(w, h, col)
        tx = mm(tex, size, col).move_to(bx)
        g = VGroup(bx, tx)
        g.box = bx
        g._tight = True
        return g

    # ------------------------------------------------------------ title ------
    def beat_title(self):
        with self.narrate("title") as tr:
            main = P(T("Magnification in Mirrors", 58, CHALK_AMBER, max_w=11.8),
                     CX, 1.55)
            ys = -0.65
            cs = VGroup(candle_at(CX - 1.9, ys, 0.55), candle_at(CX, ys, 1.0),
                        candle_at(CX + 1.9, ys, 1.5))
            line = Line([CX - 3.6, ys - 0.15, 0], [CX + 3.6, ys - 0.15, 0],
                        stroke_color=CHALK_GREEN, stroke_width=4)
            sub = P(T("Image Size, Orientation & m = " + MIN + "v/u", 34,
                      CHALK_WHITE, max_w=11.4), CX, -1.65)
            self.show(main, rt=0.7)
            self.cue(tr, "b0", FadeIn(cs), FadeIn(line), sub, sfx="ding", rt=0.8)
            self.finish(tr)

    # ------------------------------------------------------------ scene 1 ----
    def beat_s1(self):
        with self.narrate("s1") as tr:
            self.heading("What Does Magnification Tell Us?")
            ay = 0.25
            self.axis(ay, -6.35, 2.75)
            ox, ix = -3.4, 0.5
            obj = candle_at(ox, ay, 4 * KH)
            lab_o = pchip("OBJECT: 4 cm", OBJC, 20, h=0.5, w=2.4)
            P(lab_o, ox, -0.55)
            imgs = [candle_at(ix, ay, 8 * KH, False, 0.92),
                    candle_at(ix, ay, 4 * KH, False, 0.92),
                    candle_at(ix, ay, 2.4 * KH, False, 0.92),
                    candle_at(ix, ay, 4 * KH, True, 0.92)]
            names = [("ENLARGED", PLUS), ("SAME SIZE", CHALK_AMBER),
                     ("DIMINISHED", CHALK_PINK), ("INVERTED", MINUS)]
            chips = []
            for t, c in names:
                ch = pchip(t, c, 26, h=0.6, w=3.0)
                chips.append(P(ch, ix, -2.45))
            q = pcard("", ["CAN ONE NUMBER", "DESCRIBE BOTH SIZE", "AND ORIENTATION?"],
                      CHALK_PINK, size=22)
            P(q, PX, 1.2)
            big = VGroup(mm("m", 90, CHALK_YELLOW),
                         T("MAGNIFICATION", 24, CHALK_YELLOW)).arrange(DOWN, buff=0.15)
            bb = panel(PW, big.height + 0.4, CHALK_YELLOW)
            big.move_to(bb)
            bigc = VGroup(bb, big)
            bigc.box = bb
            bigc._tight = True
            P(bigc, PX, -1.0)
            self.add(obj, lab_o)
            self.cue(tr, "b0", FadeIn(imgs[0]), FadeIn(chips[0]), sfx="pop")
            self.cue(tr, "b1", ReplacementTransform(imgs[0], imgs[1]),
                     ReplacementTransform(chips[0], chips[1]), sfx="click")
            self.cue(tr, "b2", ReplacementTransform(imgs[1], imgs[2]),
                     ReplacementTransform(chips[1], chips[2]), sfx="click")
            self.cue(tr, "b3", ReplacementTransform(imgs[2], imgs[3]),
                     ReplacementTransform(chips[2], chips[3]), sfx="ding")
            self.cue(tr, "b4", FadeIn(q), sfx="click")
            self.cue(tr, "b5", FadeIn(bigc), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 2 ----
    def beat_s2(self):
        with self.narrate("s2") as tr:
            self.heading("Heights Have Signs Too")
            ay = 0.20
            self.axis(ay, -6.35, 2.75)
            ox, ix = -3.7, -0.4
            obj = candle_at(ox, ay, 4 * KH)
            lo = T("OBJECT", 20, OBJC).move_to([ox, ay - 0.35, 0])
            li = T("IMAGE", 20, IMGC).move_to([ix - 1.0, ay + 0.3, 0])
            self.add(obj, lo, li)
            a_o = vmeasure(ox + 0.55, ay, ay + 4 * KH, OBJC)
            t_o = mm(r"h_o>0", 34, PLUS).move_to([ox + 1.45, ay + 0.6, 0])
            up = candle_at(ix, ay, 6 * KH, False, 0.92)
            a_u = vmeasure(ix + 0.55, ay, ay + 6 * KH, IMGC)
            t_u = mm(r"h_i>0", 34, PLUS).move_to([ix + 1.45, ay + 0.9, 0])
            dn = candle_at(ix, ay, 6 * KH, True, 0.92)
            a_d = vmeasure(ix + 0.55, ay, ay - 6 * KH, IMGC)
            t_d = mm(r"h_i<0", 34, MINUS).move_to([ix + 1.45, ay - 0.9, 0])
            c_up = pchip("UPWARD HEIGHT: +", PLUS, 21, h=0.6)
            c_dn = pchip("DOWNWARD HEIGHT: " + MIN, MINUS, 21, h=0.6)
            stack([c_up, c_dn], top=1.2, gap=0.25)
            self.cue(tr, "b0", FadeIn(a_o), FadeIn(t_o), sfx="whoosh")
            self.cue(tr, "b1", FadeIn(up), FadeIn(a_u), FadeIn(t_u), sfx="click")
            self.cue(tr, "b2", ReplacementTransform(up, dn),
                     ReplacementTransform(a_u, a_d), ReplacementTransform(t_u, t_d),
                     sfx="ding", rt=1.0)
            self.cue(tr, "b3", FadeIn(c_up), FadeIn(c_dn), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 3 ----
    def beat_s3(self):
        with self.narrate("s3") as tr:
            self.heading("Magnification Is a Size Ratio")
            y0 = -1.45
            ho, hi = 4 * KH, 8 * KH
            bo = vbar(-4.8, y0, ho, OBJC)
            bi = vbar(-3.4, y0, hi, IMGC)
            lo = mm(r"h_o=4\text{ cm}", 28, OBJC).move_to([-4.8, y0 + ho + 0.4, 0])
            li = mm(r"h_i=8\text{ cm}", 28, IMGC).move_to([-3.4, y0 + hi + 0.4, 0])
            cap_o = T("OBJECT", 18, OBJC).move_to([-4.8, y0 - 0.3, 0])
            cap_i = T("IMAGE", 18, IMGC).move_to([-3.4, y0 - 0.3, 0])
            ghost = VGroup(vbar(-1.7, y0, ho, OBJC, 0.55),
                           vbar(-1.7, y0 + ho, ho, OBJC, 0.55))
            gl = T("2 × h_o", 22, OBJC).move_to([-1.7, y0 + hi + 0.4, 0])
            self.add(bo, bi, lo, li, cap_o, cap_i)
            f_words = self.readout(r"m=\frac{\text{image height}}{\text{object height}}",
                                   CHALK_WHITE, 34, w=5.4, h=1.15)
            P(f_words, 3.55, 1.7)
            f_sym = self.readout(r"m=\frac{h_i}{h_o}", CHALK_YELLOW, 52, w=5.4, h=1.2)
            P(f_sym, 3.55, 1.7)
            f_num = self.readout(r"\frac84=2", CHALK_CYAN, 52, w=5.4, h=1.15)
            P(f_num, 3.55, 0.3)
            txt = pcard("", ["THE IMAGE IS 2 TIMES", "THE OBJECT" + "’" + "S HEIGHT"],
                        CHALK_GREEN, size=24, w=5.4)
            P(txt, 3.55, -1.15)
            self.cue(tr, "b0", FadeIn(f_words), sfx="pop")
            self.cue(tr, "b1", ReplacementTransform(f_words, f_sym), sfx="ding")
            self.cue(tr, "b2", FadeIn(f_num), FadeIn(ghost), FadeIn(gl), sfx="click")
            self.cue(tr, "b3", FadeIn(txt), Indicate(bi, color=CHALK_WHITE,
                                                     scale_factor=1.05),
                     sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 4 ----
    def beat_s4(self):
        with self.narrate("s4") as tr:
            self.heading("The Magnitude of m Tells the Size")
            cx, cy, r = -3.7, -0.35, 1.95
            ang = lambda v: PI - PI * v / 2.0
            dim = Arc(radius=r, start_angle=ang(0), angle=-PI / 2,
                      arc_center=[cx, cy, 0], stroke_color=CHALK_PINK,
                      stroke_width=14)
            enl = Arc(radius=r, start_angle=ang(1), angle=-PI / 2,
                      arc_center=[cx, cy, 0], stroke_color=PLUS, stroke_width=14)
            ticks = VGroup()
            for v in (0, 0.5, 1, 1.5, 2):
                a = ang(v)
                p0 = np.array([cx + (r - 0.28) * math.cos(a), cy + (r - 0.28) * math.sin(a), 0])
                p1 = np.array([cx + (r + 0.05) * math.cos(a), cy + (r + 0.05) * math.sin(a), 0])
                ticks.add(Line(p0, p1, stroke_color=CHALK_WHITE, stroke_width=3))
                lab = mm(str(v).rstrip("0").rstrip(".") if v != int(v) else str(int(v)), 26)
                lab.move_to([cx + (r + 0.38) * math.cos(a), cy + (r + 0.30) * math.sin(a) - 0.0, 0])
                ticks.add(lab)

            def needle(v):
                a = ang(v)
                g = VGroup(Line([cx, cy, 0],
                                [cx + (r - 0.22) * math.cos(a), cy + (r - 0.22) * math.sin(a), 0],
                                stroke_color=CHALK_YELLOW, stroke_width=7),
                           Dot([cx, cy, 0], radius=0.11, color=CHALK_YELLOW))
                return g
            ned = needle(2.0)
            dial = VGroup(dim, enl, ticks)
            cap = T("|m|", 24, CHALK_YELLOW).move_to([cx, cy - 0.55, 0])
            y0 = -1.55
            ground = Line([-1.25, y0, 0], [2.75, y0, 0], stroke_color=CHALK_WHITE,
                          stroke_width=2.4)
            obj = candle_at(-0.35, y0, 4 * KH)
            hs = (8 * KH, 4 * KH, 2 * KH)
            ims = [candle_at(1.85, y0, h, False, 0.92) for h in hs]
            self.add(dial, cap, ground, obj)
            lo = T("OBJECT", 18, OBJC).move_to([-0.35, y0 - 0.32, 0])
            li = T("IMAGE", 18, IMGC).move_to([1.85, y0 - 0.32, 0])
            self.add(lo, li)
            vals = [("|m| = 2", "|m|>1", "ENLARGED", PLUS),
                    ("|m| = 1", "|m|=1", "SAME SIZE", CHALK_AMBER),
                    ("|m| = 0.5", "|m|<1", "DIMINISHED", CHALK_PINK)]
            conds, states, reads = [], [], []
            for (rd, cd, stt, col) in vals:
                c1 = self.readout(cd, col, 46, w=PW, h=0.85)
                c2 = pchip(stt, col, 28, h=0.66)
                r1 = mm(r"|m|=" + rd.split("= ")[1], 40, CHALK_YELLOW).move_to(
                    [cx, cy - 1.05, 0])
                conds.append(c1)
                states.append(c2)
                reads.append(r1)
            for c1, c2 in zip(conds, states):
                P(c1, PX, 1.75)
                P(c2, PX, 0.75)
            rule = pcard("", ["IGNORE THE SIGN", "FOR A MOMENT:", "|m| TELLS THE SIZE"],
                         CHALK_YELLOW, size=22)
            P(rule, PX, -1.1)
            self.cue(tr, "b0", FadeIn(ned), FadeIn(ims[0]), FadeIn(reads[0]),
                     FadeIn(conds[0]), FadeIn(states[0]), sfx="whoosh")
            n1, n2 = needle(1.0), needle(0.5)
            self.cue(tr, "b1", ReplacementTransform(ned, n1),
                     ReplacementTransform(ims[0], ims[1]),
                     ReplacementTransform(reads[0], reads[1]),
                     ReplacementTransform(conds[0], conds[1]),
                     ReplacementTransform(states[0], states[1]), sfx="click")
            self.cue(tr, "b2", ReplacementTransform(n1, n2),
                     ReplacementTransform(ims[1], ims[2]),
                     ReplacementTransform(reads[1], reads[2]),
                     ReplacementTransform(conds[1], conds[2]),
                     ReplacementTransform(states[1], states[2]), sfx="click")
            self.cue(tr, "b3", FadeIn(rule), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 5 ----
    def beat_s5(self):
        with self.narrate("s5") as tr:
            self.heading("The Sign of m Tells the Orientation")
            ay = 0.25
            self.axis(ay, -6.35, 2.75)
            ox, ix = -3.6, -0.3
            obj = candle_at(ox, ay, 4 * KH)
            lo = T("OBJECT: h_o > 0", 20, OBJC).move_to([ox, ay - 0.45, 0])
            self.add(obj, lo)
            up = candle_at(ix, ay, 6 * KH, False, 0.92)
            dn = candle_at(ix, ay, 6 * KH, True, 0.92)
            t_up = mm(r"h_i>0", 30, PLUS).move_to([ix + 1.2, ay + 0.8, 0])
            t_dn = mm(r"h_i<0", 30, MINUS).move_to([ix + 1.2, ay - 0.8, 0])
            r_up = self.readout(r"m=+1.5", PLUS, 50, h=0.95)
            r_dn = self.readout(r"m=-1.5", MINUS, 50, h=0.95)
            P(r_up, PX, 1.85)
            P(r_dn, PX, 1.85)
            s_up = pchip("m > 0:  ERECT", PLUS, 24, h=0.66)
            s_dn = pchip("m < 0:  INVERTED", MINUS, 24, h=0.66)
            P(s_up, PX, 0.8)
            P(s_dn, PX, 0.8)
            same = pcard("", ["SIZE DID NOT CHANGE.", "ONLY THE SIGN DID."], CHALK_YELLOW,
                         size=22)
            P(same, PX, -0.55)
            mem = pcard("", ["|m| GIVES THE SIZE", "SIGN GIVES ORIENTATION"],
                        CHALK_GREEN, size=22)
            P(mem, PX, -1.95)
            self.cue(tr, "b0", FadeIn(up), FadeIn(t_up), FadeIn(r_up), FadeIn(s_up),
                     sfx="pop")
            self.cue(tr, "b1", ReplacementTransform(up, dn),
                     ReplacementTransform(t_up, t_dn),
                     ReplacementTransform(r_up, r_dn),
                     ReplacementTransform(s_up, s_dn), FadeIn(same), sfx="ding",
                     rt=1.1)
            self.cue(tr, "b2", FadeIn(mem), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 6 ----
    def beat_s6(self):
        with self.narrate("s6") as tr:
            self.heading("Why Can We Also Write m = " + MIN + "v/u ?")
            mir = concave_mirror(PXM, AY, 6.0, 1.30, 1)
            axis = Line([PXM, AY, 0], [2.85, AY, 0], stroke_color=CHALK_WHITE,
                        stroke_width=2.4)
            marks = VGroup(Dot([PXM, AY, 0], radius=0.055, color=CHALK_WHITE),
                           T("P", 20, CHALK_WHITE).move_to([PXM + 0.22, AY + 0.30, 0]))
            xo, xi = xd(U_CM), xd(V_CM)
            obj = candle(HO).shift([xo, AY, 0])
            img = candle(HI).rotate(PI, axis=RIGHT, about_point=ORIGIN).shift([xi, AY, 0])
            self.add(axis, mir, marks, obj, img)
            Pp = np.array([PXM, AY, 0.0])
            tri_o = Polygon(Pp, [xo, AY, 0], [xo, AY + HO, 0])
            tri_o.set_fill(OBJC, 0.30).set_stroke(OBJC, 3)
            tri_i = Polygon(Pp, [xi, AY, 0], [xi, AY - HI, 0])
            tri_i.set_fill(IMGC, 0.30).set_stroke(IMGC, 3)
            rays = VGroup(ray([(xo, AY + HO), (PXM, AY)], CHALK_YELLOW),
                          ray([(PXM, AY), (xi, AY - HI)], CHALK_YELLOW))
            l_ho = mm(r"h_o", 30, OBJC).move_to([xo + 0.32, AY + HO / 2 + 0.05, 0])
            l_hi = mm(r"h_i", 30, IMGC).move_to([xi + 0.38, AY - HI / 2 - 0.05, 0])
            a_u = arrow([xo, AY - 0.55, 0], [PXM, AY - 0.55, 0], OBJC, 3.5, 0.17)
            a_v = arrow([xi, AY - 1.15, 0], [PXM, AY - 1.15, 0], IMGC, 3.5, 0.17)
            l_u = mm(r"u", 30, OBJC).move_to([(xo + PXM) / 2, AY - 0.85, 0])
            l_v = mm(r"v", 30, IMGC).move_to([(xi + PXM) / 2, AY - 1.45, 0])
            c0 = pchip("SIMILAR TRIANGLES\nAT THE POLE", CHALK_YELLOW, 22)
            P(c0, PX, 1.75)
            f1 = self.readout(r"\frac{h_i}{h_o}", CHALK_CYAN, 50, h=1.15)
            f2 = self.readout(r"-\frac vu", CHALK_PINK, 50, h=1.15)
            P(f1, PX, 0.35)
            P(f2, PX, 0.35)
            full = self.readout(r"m=\frac{h_i}{h_o}=-\frac vu", CHALK_GREEN, 50,
                                w=7.0, h=1.25)
            P(full, BX, -2.35)
            note = pcard("", ["SIZE INFORMATION", "FROM HEIGHTS", "OR FROM DISTANCES"],
                         CHALK_YELLOW, size=21)
            P(note, PX, -1.35)
            self.cue(tr, "b0", FadeIn(tri_o), FadeIn(tri_i), FadeIn(rays), FadeIn(c0),
                     sfx="pop")
            self.cue(tr, "b0", FadeIn(l_ho), FadeIn(l_hi), FadeIn(a_u), FadeIn(a_v),
                     FadeIn(l_u), FadeIn(l_v), sfx=None)
            self.cue(tr, "b1", FadeIn(f1), sfx="click")
            self.go(ReplacementTransform(f1, f2), rt=0.9)
            self.cue(tr, "b2", FadeIn(full), sfx="ding")
            self.cue(tr, "b3", FadeIn(note), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 7 ----
    def beat_s7(self):
        with self.narrate("s7") as tr:
            self.heading("Textbook Example: Find the Image Height")
            given = VGroup()
            for k, (txt, col) in enumerate(((r"h_o=+4\text{ cm}", OBJC),
                                            (r"u=-25\text{ cm}", CHALK_AMBER),
                                            (r"v=-37.5\text{ cm}", IMGC))):
                bx = panel(3.3, 0.78, col)
                tx = mm(txt, 34, col).move_to(bx)
                c = VGroup(bx, tx)
                c.box = bx
                c._tight = True
                P(c, CX - 3.7 + 3.7 * k, 1.95)
                given.add(c)

            def row(tex, col, x, y, w, hgt=0.84, size=34):
                bx = panel(w, hgt, col, radius=0.14, stroke=2.4)
                tx = mm(tex, size, CHALK_WHITE).move_to(bx)
                r_ = VGroup(bx, tx)
                r_.box = bx
                r_._tight = True
                return P(r_, x, y)
            WA, WB = 5.9, 5.0
            xa, xb = CX - 3.2, CX + 3.45
            rows = [
                row(r"\frac{h_i}{h_o}=-\frac vu", CHALK_CYAN, xa, 0.98, WA),
                row(r"\frac{h_i}{4}=-\frac{-37.5}{-25}", CHALK_CYAN, xa, 0.04, WA),
                row(r"\frac{h_i}{4}=-\frac{37.5}{25}", CHALK_CYAN, xa, -0.90, WA),
                row(r"m=-1.5", CHALK_AMBER, xa, -1.84, WA),
                row(r"h_i=m\,h_o=(-1.5)(4)", CHALK_AMBER, xb, 0.98, WB),
            ]
            ans = VGroup(panel(WB, 1.0, CHALK_GREEN, opacity=0.9),
                         mm(r"h_i=-6\text{ cm}", 46, CHALK_GREEN))
            ans[1].move_to(ans[0])
            ans.box = ans[0]
            ans._tight = True
            P(ans, xb, -0.2)
            self.cue(tr, "b0", *[FadeIn(c) for c in given], sfx="pop")
            self.cue(tr, "b1", FadeIn(rows[0]), sfx="click")
            self.cue(tr, "b2", FadeIn(rows[1]), sfx="click")
            self.cue(tr, "b3", FadeIn(rows[2]), sfx="click")
            self.cue(tr, "b4", FadeIn(rows[3]), sfx="click")
            self.cue(tr, "b5", FadeIn(rows[4]), sfx="click")
            self.cue(tr, "b6", FadeIn(ans), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 8 ----
    def beat_s8(self):
        with self.narrate("s8") as tr:
            self.heading("Read the Answer Physically")
            ay = 0.45
            self.axis(ay, -6.35, 2.75)
            ox, ix = -3.7, -0.5
            obj = candle_at(ox, ay, 4 * KH)
            img = candle_at(ix, ay, 6 * KH, True, 0.92)
            lo = T("OBJECT", 18, OBJC).move_to([ox, ay - 0.35, 0])
            li = T("IMAGE", 18, IMGC).move_to([ix, ay + 0.35, 0])
            a_o = vmeasure(ox + 0.55, ay, ay + 4 * KH, OBJC)
            a_i = vmeasure(ix + 0.55, ay, ay - 6 * KH, IMGC)
            t_o = mm(r"h_o=+4", 28, OBJC).move_to([ox + 1.5, ay + 0.6, 0])
            t_i = mm(r"h_i=-6", 28, IMGC).move_to([ix + 1.5, ay - 0.9, 0])
            self.add(obj, img, lo, li, a_o, a_i, t_o, t_i)
            big = self.readout(r"h_i=-6\text{ cm}", CHALK_GREEN, 46, h=0.95)
            P(big, PX, 1.9)
            c_enl = pchip("6 > 4  →  ENLARGED", PLUS, 24, h=0.62)
            P(c_enl, PX, 0.95)
            c_inv = pchip("MINUS: BELOW THE AXIS,\nINVERTED", MINUS, 21)
            P(c_inv, PX, 0.05)
            c_m = pcard("", ["m = " + MIN + "1.5", "|m| = 1.5 > 1", "ENLARGED", "m < 0: INVERTED"],
                        CHALK_YELLOW, size=20, gap=0.04)
            P(c_m, PX, -1.38)
            warn = self.banner(MIN + "1.5 DOES NOT MEAN " + "“" + "SMALLER" + "”"
                               + ".  THE SIZE COMES FROM |m| = 1.5.", CHALK_PINK, 22,
                               y=-2.62, x=CX)
            self.cue(tr, "b0", FadeIn(big), FadeIn(c_enl), sfx="pop")
            self.cue(tr, "b1", FadeIn(c_inv), sfx="ding")
            self.cue(tr, "b2", FadeIn(c_m), sfx="click")
            self.cue(tr, "b3", FadeIn(warn), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 9 ----
    def beat_s9(self):
        with self.narrate("s9q") as tr:
            self.heading("YOUR TURN", "Decode the magnification.", CHALK_PINK)
            specs = [("A", "m = +2.  Size and orientation?", CHALK_CYAN),
                     ("B", "m = " + MIN + "0.5.  Size and orientation?", CHALK_AMBER),
                     ("C", "m = " + MIN + "1.  Size and orientation?", PLUS),
                     ("D", "u = " + MIN + "20 cm,  v = " + MIN + "40 cm.  Find m.", CHALK_PINK)]
            rows = [qa_row(l, q, "?", c, w=11.8, h=0.76, size=26)
                    for l, q, c in specs]
            for r_, y in zip(rows, (1.38, 0.46, -0.46, -1.38)):
                P(r_, CX, y)
            for k, r_ in enumerate(rows):
                self.cue(tr, f"b{k}", FadeIn(r_), sfx="pop" if k == 0 else "click")
            self.finish(tr)
            self._rows = rows
        self.think_clock()
        with self.narrate("s9a", reset=False) as tr:
            ans = [("ENLARGED, ERECT", CHALK_CYAN), ("DIMINISHED, INVERTED", CHALK_AMBER),
                   ("SAME SIZE, INVERTED", PLUS), ("m = " + MIN + "2", CHALK_PINK)]
            for k in range(4):
                new = T(ans[k][0], 26, ans[k][1], max_w=4.4)
                new.move_to(self._rows[k].slot.get_center())
                new.align_to(self._rows[k].slot, RIGHT)
                self.cue(tr, f"b{k}", ReplacementTransform(self._rows[k].slot, new),
                         sfx="click" if k < 3 else "success", rt=0.5)
            bn = self.banner("2× ENLARGED  +  INVERTED", CHALK_GREEN, 26, y=-2.45,
                             x=CX)
            self.cue(tr, "b3", FadeIn(bn), sfx=None)
            self.finish(tr)

    # ----------------------------------------------------------- scene 10 ----
    def beat_s10(self):
        with self.narrate("s10") as tr:
            self.heading("How to Decode m")
            fm = self.readout(r"m=\frac{h_i}{h_o}=-\frac vu", CHALK_YELLOW, 46, w=7.0,
                              h=1.15)
            P(fm, CX, 1.72)
            q1 = chip("HOW BIG IS THE IMAGE?", CHALK_CYAN, 24)
            q1._tight = True
            P(q1, CX - 3.3, 0.72)
            w1 = [pchip("|m| > 1:  ENLARGED", PLUS, 22, h=0.55, w=5.4),
                  pchip("|m| = 1:  SAME SIZE", CHALK_AMBER, 22, h=0.55, w=5.4),
                  pchip("|m| < 1:  DIMINISHED", CHALK_PINK, 22, h=0.55, w=5.4)]
            for k, c in enumerate(w1):
                P(c, CX - 3.3, 0.0 - 0.72 * k)
            q2 = chip("WHICH WAY DOES IT POINT?", CHALK_CYAN, 24)
            q2._tight = True
            P(q2, CX + 3.3, 0.72)
            w2 = [pchip("m > 0:  ERECT", PLUS, 22, h=0.55, w=5.4),
                  pchip("m < 0:  INVERTED", MINUS, 22, h=0.55, w=5.4)]
            for k, c in enumerate(w2):
                P(c, CX + 3.3, 0.0 - 0.72 * k)
            ex = self.banner("EXAMPLE:  m = " + MIN + "1.5   →   |m| = 1.5 > 1: ENLARGED   ·   m < 0: INVERTED",
                             CHALK_YELLOW, 22, y=-2.25, x=CX)
            fin = self.banner("|m| → SIZE     SIGN OF m → ORIENTATION", CHALK_GREEN, 26,
                              y=-2.25, x=CX)
            self.cue(tr, "b0", FadeIn(fm), FadeIn(q1), sfx="pop")
            self.cue(tr, "b1", *[FadeIn(c) for c in w1], sfx="click")
            self.cue(tr, "b2", FadeIn(q2), sfx="click")
            self.cue(tr, "b3", *[FadeIn(c) for c in w2], sfx="click")
            self.cue(tr, "b4", FadeIn(ex), sfx="ding")
            self.cue(tr, "b5", ReplacementTransform(ex, fin), sfx="success")
            self.hold(tr, "b6")
            keep = [m_ for m_ in self.mobjects if m_ not in self.fixtures]
            self.go(*[FadeOut(m_) for m_ in keep], rt=0.6)
            slogan = P(T("DON" + "’" + "T JUST CALCULATE m.", 46, CHALK_YELLOW,
                         max_w=12.0), CX, 0.55)
            sub = P(T("READ WHAT m IS TELLING YOU.", 46, CHALK_WHITE, max_w=12.0),
                    CX, -0.45)
            self.cue(tr, "b6", FadeIn(slogan), FadeIn(sub), sfx="success")
            self.hold(tr, "b7")
            self.go(FadeOut(slogan), FadeOut(sub), rt=0.6)
            thanks = P(T("Thank You for Watching!", 60, CHALK_WHITE, max_w=11.8),
                       CX, 0.60)
            bye = P(T("See you in the next lesson :)", 44, CHALK_YELLOW,
                      max_w=11.0), CX, -0.75)
            self.cue(tr, "b7", FadeIn(thanks, shift=UP * 0.1), sfx=None)
            self.cue(tr, "b8", FadeIn(bye, shift=UP * 0.1), sfx=None)
            self.finish(tr)
        if not self.still:
            self.wait(END_HOLD)

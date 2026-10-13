"""
Focusing Sunlight & the Solar Cooker: How a Concave Mirror Concentrates Solar
Energy
Story-mode chalkboard lesson (Class 10 Physics, TG Board, Chapter 1:
Reflection of Light at Curved Surfaces, section 1.7).

LLM KEY / FUNCTION NAME: focusing_sunlight_and_solar_cooker

Storyboard: storyboard.md; the review notes (what was kept, what was changed
and why) are in storyboard_review.md, next to this file.

  * ONE sunlight geometry for the whole video: the Sun on the left, five
    parallel rays, a concave dish on the right (vertex at the right, opening
    to the Sun), focus F on the axis -- the viewer always finds the same
    picture;
  * the dish is a paraboloid (the drawing rule "parallel to the axis ->
    through F" is then exact); the mirror of scenes 3-4 and the quiz is the
    textbook's spherical mirror with P, F and C;
  * off-axis rays (scene 7) are reflected with the true law of reflection, so
    the bright region really leaves the vessel when the cooker is turned;
  * the "bright spot" on the screen (scene 4) and the vessel in front of /
    at / beyond F (scene 8) use the true width of the reflected ray bundle;
  * the heat meter is qualitative (no numbers), and the video never says the
    mirror makes energy: it redirects the sunlight that reaches it;
  * the challenge uses the series' ten-second THINK clock (small, top right).
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
        "Focusing sunlight and the solar cooker. <bookmark mark='b0'/> How a "
        "concave mirror concentrates solar energy."
    ),
    "s1": (
        "Sunlight is already falling on this cooking vessel. <bookmark "
        "mark='b0'/> But the light is spread over a large area, so the "
        "vessel heats up only slowly. <bookmark mark='b1'/> Now we bring in "
        "a concave mirror. What can it change? <bookmark mark='b2'/> The "
        "mirror collects light from a wide area, and redirects it towards "
        "one small region."
    ),
    "s2": (
        "Why do we draw the Sun's rays parallel? <bookmark mark='b0'/> Take "
        "a lamp close to the mirror. Its rays spread out at a large angle. "
        "<bookmark mark='b1'/> Move the lamp farther away, and the angle "
        "between the rays shrinks. <bookmark mark='b2'/> The Sun is about "
        "one hundred and fifty million kilometres away. Across the width of "
        "a mirror, its rays are almost exactly parallel. <bookmark "
        "mark='b3'/> So the mirror receives a bundle of nearly parallel "
        "sun rays."
    ),
    "s3": (
        "What does a concave mirror do to parallel rays? <bookmark "
        "mark='b0'/> Three rays travel parallel to the principal axis. "
        "<bookmark mark='b1'/> Each strikes the mirror at a different "
        "point, and reflects by the law of reflection. The dashed line is "
        "the normal. <bookmark mark='b2'/> The reflected rays turn inwards, "
        "and all cross at one point. <bookmark mark='b3'/> This point is the "
        "principal focus, F. <bookmark mark='b4'/> Remember: a ray parallel "
        "to the axis reflects through F."
    ),
    "s4": (
        "How can we actually see the focus? Hold a small paper screen in "
        "front of the mirror. <bookmark mark='b0'/> Close to the mirror, the "
        "bright patch is large and blurry. <bookmark mark='b1'/> Move the "
        "screen slowly, and the patch becomes smaller and brighter. "
        "<bookmark mark='b2'/> At one position it is the smallest and the "
        "brightest. This spot is the image of the Sun, at the focus. "
        "<bookmark mark='b3'/> The distance from the pole to the focus is "
        "the focal length, f. <bookmark mark='b4'/> Focused sunlight can burn "
        "paper, so this is shown as an animation. Never try it without a "
        "teacher."
    ),
    "s5": (
        "Why does the focal region get hot? <bookmark mark='b0'/> Each "
        "sunlight ray carries some energy, shown here as a small marker. "
        "<bookmark mark='b1'/> After reflection, the rays converge, and all "
        "the markers arrive in a much smaller region. <bookmark mark='b2'/> "
        "Before the mirror, the light is spread over a wide area. At the "
        "focus, many reflected rays arrive in a small region. <bookmark "
        "mark='b3'/> More of the collected sunlight reaches a smaller "
        "region, so the heating is stronger. <bookmark mark='b4'/> The "
        "mirror does not create energy. It only redirects the sunlight that "
        "reaches it."
    ),
    "s6": (
        "Now let us turn the ray rule into a solar cooker. <bookmark "
        "mark='b0'/> A large concave dish receives parallel sunlight. "
        "<bookmark mark='b1'/> Every reflected ray converges near the focus, "
        "F. <bookmark mark='b2'/> The cooking vessel is slid along the axis "
        "towards F. <bookmark mark='b3'/> When the vessel is at F, it "
        "receives all the concentrated light. <bookmark mark='b4'/> The "
        "vessel heats up strongly, enough to cook rice."
    ),
    "s7": (
        "Why must the cooker face the Sun? <bookmark mark='b0'/> When the "
        "dish points straight at the Sun, the rays are parallel to its "
        "axis, and they meet at F, on the vessel. <bookmark mark='b1'/> Turn "
        "the dish away, and the rays are no longer parallel to its axis. "
        "The bright region moves away from the vessel. <bookmark "
        "mark='b2'/> The vessel misses the concentrated light, and its "
        "temperature falls. <bookmark mark='b3'/> Turn the dish back towards "
        "the Sun, and the focus returns to the vessel. Always point the "
        "reflector towards the Sun."
    ),
    "s8": (
        "Can the vessel be placed anywhere? <bookmark mark='b0'/> Before F, "
        "the rays are still converging, and they spread over a larger part "
        "of the vessel. <bookmark mark='b1'/> At F, the ray bundle is the "
        "tightest, so the vessel receives the most concentrated light. "
        "<bookmark mark='b2'/> Beyond F, the rays have crossed and are "
        "spreading again. <bookmark mark='b3'/> Before F, spread. At F, most "
        "concentrated. After F, spread again. This is why the instruction "
        "says: place the vessel at the focus."
    ),
    "s9q": (
        "Your turn. <bookmark mark='b0'/> A: parallel rays strike a concave "
        "mirror. Where do the reflected rays go? <bookmark mark='b1'/> B: "
        "the vessel can be placed before F, at F, or beyond F. Where should "
        "it go? <bookmark mark='b2'/> C: which mirror is used: plane, "
        "convex or concave? <bookmark mark='b3'/> D: what happens if the "
        "vessel is far beyond F? Take your time, and pause the video if you "
        "need to."
    ),
    "s9a": (
        "Let us check. <bookmark mark='b0'/> A: the reflected rays all pass "
        "through the focus, F. <bookmark mark='b1'/> B: the vessel goes at "
        "F. <bookmark mark='b2'/> C: a concave mirror, because only it makes "
        "parallel rays converge. <bookmark mark='b3'/> D: the light is more "
        "spread out there, so move the vessel back towards F."
    ),
    "s10": (
        "Here is the whole story. <bookmark mark='b0'/> The Sun is far "
        "away, so its rays arrive nearly parallel. <bookmark mark='b1'/> "
        "They strike the concave reflector. <bookmark mark='b2'/> The "
        "reflected rays converge at the focus, F. <bookmark mark='b3'/> The "
        "vessel is placed at F. <bookmark mark='b4'/> Concentrated sunlight "
        "heats it strongly. <bookmark mark='b5'/> Parallel sun rays, concave "
        "reflector, focus, vessel, heating. Collect, reflect, focus, heat. "
        "<bookmark mark='b6'/> That is the optical idea behind the solar "
        "cooker. <bookmark mark='b7'/> Thank you for watching, <bookmark "
        "mark='b8'/> and see you in the next lesson."
    ),
}

# ------------------------------------------------------------- geometry ------
PX, PW, PAN_TOP = 4.85, 3.30, 2.45     # right-hand panel
SUNC, REFC = "#FFE066", "#FFB74D"      # incoming / reflected rays
AY = -0.20                             # principal axis
XP, FD, HALF = 2.40, 1.50, 1.90        # dish vertex, focal length, half aperture
FX = XP - FD                           # focus F
X0 = -5.00                             # where the rays start
OFFS = (-1.5, -0.75, 0.0, 0.75, 1.5)   # ray heights above the axis
METER = (-3.15, -2.62)                 # heat-meter centre


def hit_point(y0, th=0.0):
    """Where the horizontal ray at height y0 meets the (turned) dish, and the
    surface normal there."""
    V = np.array([XP, AY])
    c, sn = math.cos(th), math.sin(th)

    def pt(s):
        q = np.array([-s * s / (4 * FD), s])
        return V + np.array([c * q[0] - sn * q[1], sn * q[0] + c * q[1]])
    lo, hi = -HALF, HALF
    for _ in range(60):
        mid = (lo + hi) / 2
        if pt(mid)[1] < y0:
            lo = mid
        else:
            hi = mid
    s = (lo + hi) / 2
    p = pt(s)
    tl = np.array([-s / (2 * FD), 1.0])
    t = np.array([c * tl[0] - sn * tl[1], sn * tl[0] + c * tl[1]])
    n = np.array([t[1], -t[0]])
    return p, n / np.linalg.norm(n)


def focus_of(th=0.0):
    c, sn = math.cos(th), math.sin(th)
    return np.array([XP, AY]) + np.array([c * -FD, sn * -FD])


def bundle(th=0.0, ext=0.0, col_in=SUNC, col_out=REFC, w=3.2):
    """Five sunlight rays: incoming leg + reflected leg (true reflection)."""
    g = VGroup()
    for o in OFFS:
        p, n = hit_point(AY + o, th)
        d = np.array([1.0, 0.0])
        d2 = d - 2 * np.dot(d, n) * n
        Ft = focus_of(th)
        L = np.linalg.norm(p - Ft) + ext
        q = p + d2 * L
        g.add(ray([(X0, AY + o), tuple(p)], col_in, w))
        g.add(ray([tuple(p), tuple(q)], col_out, w))
    return g


def plain_rays(x_end, col=SUNC, w=3.2):
    return VGroup(*[ray([(X0, AY + o), (x_end, AY + o)], col, w) for o in OFFS])


def glow(p, r=0.30, col="#FFD54F"):
    g = VGroup()
    for k, (rr, op) in enumerate(((r * 2.0, 0.10), (r * 1.4, 0.18), (r * 0.9, 0.32),
                                  (r * 0.45, 0.85))):
        g.add(Circle(radius=rr, fill_color=col, fill_opacity=op, stroke_width=0)
              .move_to([p[0], p[1], 0]))
    return g


class FocusingSunlightAndSolarCookerStory(PhysScene):
    NARRATION = NARRATION
    CLOCK_AT = (5.70, 2.55)
    BEATS = ("title", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9",
             "s10")

    # ---------------------------------------------------------- helpers ------
    def banner(self, txt, col=CHALK_YELLOW, size=24, y=-2.62, x=-1.4):
        c = chip(txt, col, size)
        c._tight = True
        return P(c, x, y)

    def sun(self, x=-6.0, y=1.85, r=0.42):
        s = sun_icon(r).move_to([x, y, 0])
        lab = T("SUN", 18, SUNC).move_to([x, y - 0.78, 0])
        g = VGroup(s, lab)
        self.add(g)
        return g

    def axis_line(self, x1=XP):
        ln = Line([-5.5, AY, 0], [x1, AY, 0], stroke_color=CHALK_WHITE,
                  stroke_width=2.0, stroke_opacity=0.8)
        self.add(ln)
        return ln

    def dish(self, theta=0.0):
        d = parabolic_dish(XP, AY, FD, HALF, theta)
        return d

    def meter(self, level, label="HEAT AT THE VESSEL"):
        m = heat_meter(level, 4.2, 0.36, METER[0], METER[1])
        return m

    def meter_label(self, label="HEAT AT THE VESSEL"):
        t = T(label, 18, CHALK_WHITE).move_to([METER[0], METER[1] + 0.42, 0])
        self.add(t)
        return t

    # ------------------------------------------------------------ title ------
    def beat_title(self):
        with self.narrate("title") as tr:
            main = P(T("Focusing Sunlight", 58, CHALK_AMBER, max_w=11.4), CX, 1.95)
            main2 = P(T("& the Solar Cooker", 58, CHALK_AMBER, max_w=11.4), CX, 1.15)
            d = parabolic_dish(CX + 2.3, -0.55, 1.1, 1.15)
            rays = VGroup(*[ray([(CX - 3.2, -0.55 + o), (CX + 2.3 - o * o / 4.4,
                                                          -0.55 + o)], SUNC, 3)
                            for o in (-0.8, 0.0, 0.8)])
            refl = VGroup(*[ray([(CX + 2.3 - o * o / 4.4, -0.55 + o),
                                 (CX + 1.2, -0.55)], REFC, 3) for o in (-0.8, 0.8)])
            gl = glow([CX + 1.2, -0.55], 0.18)
            sub = P(T("How a Concave Mirror Concentrates Solar Energy", 30,
                      CHALK_WHITE, max_w=11.4), CX, -2.2)
            self.show(VGroup(main, main2), rt=0.7)
            self.cue(tr, "b0", FadeIn(d), FadeIn(rays), FadeIn(refl), FadeIn(gl),
                     sub, sfx="ding", rt=0.9)
            self.finish(tr)

    # ------------------------------------------------------------ scene 1 ----
    def beat_s1(self):
        with self.narrate("s1") as tr:
            self.heading("Why Not Just Put the Vessel in Sunlight?")
            self.sun()
            self.axis_line()
            vessel = pot(0.8, 0.55).move_to([FX, AY + 0.0, 0])
            straight = plain_rays(XP + 0.9)
            to_dish = plain_rays(XP - 0.0)
            hits = VGroup(*[ray([(X0, AY + o), tuple(hit_point(AY + o)[0])], SUNC, 3.2)
                            for o in OFFS])
            wide = DashedLine([-1.9, AY - 1.5, 0], [-1.9, AY + 1.5, 0],
                              stroke_color=CHALK_WHITE, stroke_width=3, dash_length=0.12)
            wlab = T("WIDE BEAM", 18, CHALK_WHITE).move_to([-1.9, AY + 1.85, 0])
            dish = self.dish()
            refl = VGroup(*[ray([tuple(hit_point(AY + o)[0]), (FX, AY)], REFC, 3.2)
                            for o in OFFS])
            self.meter_label()
            m0, m1, m2 = self.meter(0.10), self.meter(0.22), self.meter(0.22)
            c1 = pcard("", ["SUNLIGHT SPREAD", "OVER A LARGE AREA"], CHALK_YELLOW, size=21, w=PW)
            P(c1, PX, 1.2)
            c2 = pcard("", ["WHAT CAN THIS", "MIRROR CHANGE?"], CHALK_PINK, size=22, w=PW)
            P(c2, PX, -1.2)
            c3 = pcard("", ["WIDE AREA COLLECTED", "SMALL REGION LIT"], CHALK_GREEN,
                       size=20, w=PW)
            P(c3, PX, -1.2)
            self.show(vessel, straight, m0, rt=0.8)
            self.cue(tr, "b0", FadeIn(c1), FadeIn(wide), FadeIn(wlab),
                     ReplacementTransform(m0, m1), sfx="click", rt=1.6)
            self.cue(tr, "b1", FadeIn(dish), ReplacementTransform(straight, hits),
                     FadeIn(c2), sfx="whoosh", rt=1.0)
            self.cue(tr, "b2", FadeIn(refl), FadeIn(glow([FX, AY], 0.2)),
                     ReplacementTransform(c2, c3), sfx="ding")
            self.finish(tr)

    # ------------------------------------------------------------ scene 2 ----
    def beat_s2(self):
        with self.narrate("s2") as tr:
            self.heading("Why Are the Sun's Rays Drawn Parallel?")
            mx = 2.6
            span = 1.55
            bracket = VGroup(Line([mx, AY - span, 0], [mx, AY + span, 0],
                                  stroke_color="#C9D4DD", stroke_width=9),
                             T("MIRROR WIDTH", 16, CHALK_WHITE).move_to([mx - 0.0, AY - span - 0.35, 0]))
            self.add(bracket)

            def two_rays(xs, col=SUNC):
                return VGroup(ray([(xs, AY), (mx, AY + span)], col, 3.2),
                              ray([(xs, AY), (mx, AY - span)], col, 3.2))
            lamp = lambda x: VGroup(Circle(radius=0.16, fill_color="#FFE082", fill_opacity=1,
                                           stroke_color="#FF9800", stroke_width=2.4).move_to([x, AY, 0]),
                                    Circle(radius=0.34, fill_color="#FFE082", fill_opacity=0.2,
                                           stroke_width=0).move_to([x, AY, 0]))
            l_near, l_far = lamp(-0.4), lamp(-5.0)
            r_near, r_far = two_rays(-0.4), two_rays(-5.0)
            sun = sun_icon(0.42).move_to([-6.0, AY, 0])
            far_arrow = T("VERY FAR AWAY", 16, SUNC).move_to([-5.2, AY + 0.9, 0])
            par = VGroup(*[ray([(-4.2, AY + o), (mx, AY + o)], SUNC, 3.2)
                           for o in (-1.5, -0.75, 0.0, 0.75, 1.5)])
            c0 = pcard("", ["LAMP NEARBY:", "RAYS SPREAD OUT"], CHALK_PINK, size=21, w=PW)
            c1 = pcard("", ["LAMP FARTHER:", "SMALLER ANGLE"], CHALK_AMBER, size=21, w=PW)
            c2 = pcard("", ["THE SUN IS ABOUT", "150 MILLION km AWAY"], SUNC, size=21, w=PW)
            c3 = pcard("", ["NEARLY PARALLEL", "RAYS AT THE MIRROR"], CHALK_GREEN, size=21, w=PW)
            for c in (c0, c1, c2, c3):
                P(c, PX, 1.45)
            P(c3, PX, -0.5)
            P(c2, PX, 1.45)
            self.cue(tr, "b0", FadeIn(l_near), FadeIn(r_near), FadeIn(c0), sfx="pop")
            self.cue(tr, "b1", ReplacementTransform(l_near, l_far),
                     ReplacementTransform(r_near, r_far), ReplacementTransform(c0, c1),
                     sfx="whoosh", rt=1.4)
            self.cue(tr, "b2", FadeOut(l_far), FadeOut(r_far), FadeIn(sun),
                     FadeIn(far_arrow), ReplacementTransform(c1, c2), sfx="ding", rt=0.9)
            self.cue(tr, "b3", FadeIn(par), FadeIn(c3), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 3 ----
    def beat_s3(self):
        with self.narrate("s3") as tr:
            self.heading("What Does a Concave Mirror Do?")
            Pp, R = 2.6, 4.0
            mir = concave_mirror(Pp, AY, R, 1.30, -1)
            axis = Line([-5.5, AY, 0], [Pp, AY, 0], stroke_color=CHALK_WHITE,
                        stroke_width=2.2)
            Fx, Cx = Pp - R / 2, Pp - R
            marks = VGroup()
            for x, nm in ((Pp, "P"), (Fx, "F"), (Cx, "C")):
                marks.add(Dot([x, AY, 0], radius=0.06, color=CHALK_WHITE))
                marks.add(T(nm, 22, CHALK_WHITE).move_to([x + (0.0 if nm != "P" else 0.25), AY - 0.38, 0]))
            self.add(axis, mir, marks)
            hs = (1.0, 0.45, -0.75)
            hits = [(Pp - sag(h, R), AY + h) for h in hs]
            incoming = VGroup(*[ray([(X0, AY + h), hp], SUNC, 3.4)
                                for h, hp in zip(hs, hits)])
            refl = VGroup(*[ray([hp, (Fx, AY)], REFC, 3.4) for hp in hits])
            normal = DashedLine([hits[0][0], hits[0][1], 0], [Cx, AY, 0],
                                stroke_color=CHALK_CYAN, stroke_width=2.4, dash_length=0.12)
            nlab = T("NORMAL", 16, CHALK_CYAN).move_to([hits[0][0] - 1.0, hits[0][1] - 0.62, 0])
            gl = glow([Fx, AY], 0.2)
            flab = pchip("PRINCIPAL FOCUS F", CHALK_YELLOW, 22, h=0.58, w=3.1)
            P(flab, PX, 1.6)
            rule = pcard("", ["PARALLEL TO THE AXIS", "→ REFLECTS THROUGH F"],
                         CHALK_GREEN, size=21, w=PW)
            P(rule, PX, 0.1)
            self.cue(tr, "b0", FadeIn(incoming), sfx="whoosh", rt=0.9)
            self.cue(tr, "b1", FadeIn(normal), FadeIn(nlab), sfx="click")
            self.cue(tr, "b2", FadeIn(refl), sfx="whoosh", rt=0.9)
            self.cue(tr, "b3", FadeIn(gl), FadeIn(flab), sfx="ding")
            self.cue(tr, "b4", FadeIn(rule), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 4 ----
    def beat_s4(self):
        with self.narrate("s4") as tr:
            self.heading("Find the Focus: Smallest, Brightest Spot")
            Pp, R = 2.6, 4.0
            mir = concave_mirror(Pp, AY, R, 1.30, -1)
            axis = Line([-5.5, AY, 0], [Pp, AY, 0], stroke_color=CHALK_WHITE,
                        stroke_width=2.2)
            Fx = Pp - R / 2
            marks = VGroup(Dot([Pp, AY, 0], radius=0.06, color=CHALK_WHITE),
                           T("P", 22, CHALK_WHITE).move_to([Pp + 0.25, AY - 0.38, 0]))
            hs = (0.9, 0.45, 0.0, -0.45, -0.9)
            hits = [(Pp - sag(h, R), AY + h) for h in hs]
            incoming = VGroup(*[ray([(X0, AY + h), hp], SUNC, 3.0) for h, hp in zip(hs, hits)])
            refl = VGroup(*[ray([hp, (Fx - 0.0, AY)], REFC, 3.0) for hp in hits])
            self.add(axis, mir, marks, incoming, refl)

            def screen_at(x):
                xh = Pp - 0.05
                size = 0.9 * abs(x - Fx) / (xh - Fx)
                sz = max(size, 0.07)
                bright = min(1.0, 0.16 / sz + 0.12)
                paper = Rectangle(width=0.09, height=1.9)
                paint(paper, ["#D8DDE2", "#9AA3AB"], lw=1.6, sheen=0.2, line="#4A525A")
                paper.move_to([x, AY, 0])
                spot = Ellipse(width=0.16, height=2 * sz, fill_color="#FFB300",
                               fill_opacity=bright, stroke_width=0).move_to([x + 0.0, AY, 0])
                core = Ellipse(width=0.10, height=max(1.1 * sz, 0.05),
                               fill_color="#FFF3C4", fill_opacity=min(1.0, bright + 0.1),
                               stroke_width=0).move_to([x, AY, 0])
                return VGroup(paper, spot, core)
            s1, s2, s3 = screen_at(Pp - 0.55), screen_at(Pp - 1.20), screen_at(Fx)
            n0 = pchip("NOT THE FOCUS", CHALK_RED, 22, h=0.6, w=3.0)
            P(n0, PX, 1.7)
            n1 = pchip("SMALLER, BRIGHTER", CHALK_AMBER, 20, h=0.6, w=3.3)
            P(n1, PX, 1.7)
            n2 = pchip("SMALLEST + BRIGHTEST", CHALK_GREEN, 20, h=0.6, w=3.3)
            P(n2, PX, 1.7)
            flab = VGroup(T("F", 28, CHALK_YELLOW).move_to([Fx, AY - 1.15, 0]),
                          Line([Fx, AY - 0.95, 0], [Fx, AY - 0.15, 0], stroke_color=CHALK_YELLOW,
                               stroke_width=2.4))
            meas = VGroup(arrow([Fx, AY - 1.62, 0], [Pp, AY - 1.62, 0], CHALK_CYAN, 4, 0.18),
                          arrow([Pp, AY - 1.62, 0], [Fx, AY - 1.62, 0], CHALK_CYAN, 4, 0.18),
                          mm_("f = PF", 26, CHALK_CYAN).move_to([(Fx + Pp) / 2, AY - 1.95, 0]))
            safety = pcard("", ["ANIMATION ONLY:", "FOCUSED SUNLIGHT", "CAN BURN PAPER"],
                           CHALK_RED, size=20, w=PW)
            P(safety, PX, -0.45)
            self.cue(tr, "b0", FadeIn(s1), FadeIn(n0), sfx="pop", snap="near")
            self.cue(tr, "b1", ReplacementTransform(s1, s2), ReplacementTransform(n0, n1),
                     sfx="whoosh", rt=1.4)
            self.cue(tr, "b2", ReplacementTransform(s2, s3), ReplacementTransform(n1, n2),
                     FadeIn(flab), sfx="ding", rt=1.4)
            self.cue(tr, "b3", FadeIn(meas), sfx="click")
            self.cue(tr, "b4", FadeIn(safety), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 5 ----
    def beat_s5(self):
        with self.narrate("s5") as tr:
            self.heading("Why Does the Focal Region Get Hot?")
            self.sun()
            self.axis_line()
            dish = self.dish()
            self.add(dish)
            self.meter_label()
            incoming = VGroup(*[ray([(X0, AY + o), tuple(hit_point(AY + o)[0])], SUNC, 3.0)
                                for o in OFFS])
            refl = VGroup(*[ray([tuple(hit_point(AY + o)[0]), (FX, AY)], REFC, 3.0)
                            for o in OFFS])
            self.add(incoming)

            def marker(x, y):
                d = Polygon([x, y + 0.11, 0], [x + 0.09, y, 0], [x, y - 0.11, 0],
                            [x - 0.09, y, 0])
                d.set_fill("#FFFFFF", 1).set_stroke(SUNC, 2)
                return d
            marks = VGroup(*[marker(-3.2, AY + o) for o in OFFS])
            wide = VGroup(Line([-3.2 - 0.0, AY - 1.62, 0], [-3.2, AY + 1.62, 0],
                               stroke_color=CHALK_WHITE, stroke_width=2, stroke_opacity=0.5))
            paths = [[np.array([-3.2, AY + o, 0.0]), np.array([*hit_point(AY + o)[0], 0.0]),
                      np.array([FX + (0.07 * k - 0.14), AY + (0.05 * (k % 2) - 0.03), 0.0])]
                     for k, o in enumerate(OFFS)]
            m0, m1 = self.meter(0.15), self.meter(0.9)
            c0 = pcard("", ["EACH RAY CARRIES", "SOME ENERGY"], SUNC, size=21, w=PW)
            c1 = pcard("", ["BEFORE: LIGHT SPREAD", "OVER A WIDE AREA"], CHALK_PINK, size=19, w=PW)
            c2 = pcard("", ["AT THE FOCUS: MANY RAYS", "IN A SMALL REGION"], CHALK_GREEN,
                       size=19, w=PW)
            c3 = pchip("STRONGER HEATING", CHALK_RED, 22, h=0.6)
            c4 = pcard("", ["THE MIRROR DOES NOT", "CREATE ENERGY:", "IT REDIRECTS SUNLIGHT"],
                       CHALK_YELLOW, size=20, w=PW)
            stack([c0, c1, c2], top=PAN_TOP, gap=0.14, x=PX)
            P(c3, PX, -0.88)
            P(c4, PX, -2.0)
            self.add(m0)
            self.cue(tr, "b0", FadeIn(marks), FadeIn(c0), sfx="pop")
            moves = [MoveAlongPath(m, TX_path(p), run_time=2.4, rate_func=linear)
                     for m, p in zip(marks, paths)]
            self.cue(tr, "b1", FadeIn(refl), *moves, sfx="whoosh", rt=2.4)
            self.cue(tr, "b2", FadeIn(c1), FadeIn(c2), sfx="click")
            self.cue(tr, "b3", ReplacementTransform(m0, m1), FadeIn(c3), sfx="ding", rt=1.4)
            self.cue(tr, "b4", FadeIn(c4), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 6 ----
    def beat_s6(self):
        with self.narrate("s6") as tr:
            self.heading("Turn the Ray Rule into a Solar Cooker")
            self.sun()
            axis = self.axis_line()
            dish = self.dish()
            self.add(dish)
            incoming = VGroup(*[ray([(X0, AY + o), tuple(hit_point(AY + o)[0])], SUNC, 3.2)
                                for o in OFFS])
            refl = VGroup(*[ray([tuple(hit_point(AY + o)[0]), (FX, AY)], REFC, 3.2)
                            for o in OFFS])
            marks = VGroup(Dot([XP, AY, 0], radius=0.06, color=CHALK_WHITE),
                           T("P", 20, CHALK_WHITE).move_to([XP + 0.28, AY - 0.4, 0]),
                           Dot([FX, AY, 0], radius=0.06, color=CHALK_WHITE),
                           T("F", 22, CHALK_YELLOW).move_to([FX - 0.05, AY - 0.55, 0]))
            self.add(marks)
            gl = glow([FX, AY], 0.2)
            vessel = pot(0.8, 0.55).move_to([-2.6, AY, 0])
            vessel_f = pot(0.8, 0.55).move_to([FX, AY, 0])
            lock = pchip("VESSEL AT F", CHALK_YELLOW, 24, h=0.62)
            P(lock, PX, 1.7)
            self.meter_label()
            m0, m1 = self.meter(0.12), self.meter(0.95)
            heat = pcard("", ["CONCENTRATED", "SUNLIGHT HEATS", "THE VESSEL"], CHALK_RED,
                         size=21, w=PW)
            P(heat, PX, 0.2)
            st = steam(0.8).move_to([FX, AY + 0.62, 0])
            self.add(m0)
            self.cue(tr, "b0", FadeIn(incoming), sfx="whoosh", rt=0.9)
            self.cue(tr, "b1", FadeIn(refl), FadeIn(gl), sfx="ding")
            self.cue(tr, "b2", FadeIn(vessel), sfx="pop", rt=0.4)
            self.go(vessel.animate.move_to([FX, AY, 0]), rt=2.0)
            self.cue(tr, "b3", FadeIn(lock), sfx="click")
            self.cue(tr, "b4", ReplacementTransform(m0, m1), FadeIn(heat), FadeIn(st),
                     sfx="success", rt=1.6)
            self.finish(tr)

    # ------------------------------------------------------------ scene 7 ----
    def beat_s7(self):
        with self.narrate("s7") as tr:
            self.heading("Why Must the Cooker Face the Sun?")
            self.sun()
            self.axis_line()
            th = 0.26
            dish0 = self.dish(0.0)
            dish1 = self.dish(th)
            b0 = bundle(0.0, 0.0)
            b1 = bundle(th, 0.0)
            V = np.array([XP, AY, 0.0])
            Fp0, Fp1 = focus_of(0.0), focus_of(th)
            v0 = pot(0.8, 0.55).move_to([Fp0[0], Fp0[1], 0])
            v1 = pot(0.8, 0.55).move_to([Fp1[0], Fp1[1], 0])
            gl0 = glow(Fp0, 0.2)
            self.meter_label()
            m0, m1, m2 = self.meter(0.95), self.meter(0.18), self.meter(0.95)
            good = pchip("GOOD ALIGNMENT", CHALK_GREEN, 24, h=0.62)
            miss = pcard("", ["VESSEL MISSES THE", "CONCENTRATED REGION"], CHALK_RED,
                         size=20, w=PW)
            msg = pcard("", ["POINT THE REFLECTOR", "TOWARDS THE SUN"], CHALK_YELLOW,
                        size=20, w=PW)
            P(good, PX, 1.7)
            P(miss, PX, 0.4)
            P(msg, PX, -0.9)
            self.add(dish0, b0, v0, gl0, m0)
            self.cue(tr, "b0", FadeIn(good), sfx="pop")
            self.cue(tr, "b1", ReplacementTransform(dish0, dish1),
                     ReplacementTransform(b0, b1), ReplacementTransform(v0, v1),
                     FadeOut(gl0), FadeOut(good), sfx="whoosh", rt=1.8)
            self.cue(tr, "b2", ReplacementTransform(m0, m1), FadeIn(miss), sfx="click",
                     rt=1.2, snap="miss")
            back0 = self.dish(0.0)
            bb0 = bundle(0.0, 0.0)
            vb = pot(0.8, 0.55).move_to([Fp0[0], Fp0[1], 0])
            self.cue(tr, "b3", ReplacementTransform(dish1, back0),
                     ReplacementTransform(b1, bb0), ReplacementTransform(v1, vb),
                     FadeIn(glow(Fp0, 0.2)), FadeOut(miss), FadeIn(msg),
                     ReplacementTransform(m1, m2), sfx="ding",
                     rt=1.8)
            self.finish(tr)

    # ------------------------------------------------------------ scene 8 ----
    def beat_s8(self):
        with self.narrate("s8") as tr:
            self.heading("The Vessel Cannot Go Just Anywhere")
            self.sun()
            self.axis_line()
            dish = self.dish()
            ext = 1.6
            b = bundle(0.0, ext)
            self.add(dish, b)
            xs = {"A": FX + 0.85, "B": FX, "C": FX - 0.85}
            names = {"A": "A", "B": "B", "C": "C"}
            cols = {"A": CHALK_AMBER, "B": CHALK_GREEN, "C": CHALK_PINK}
            width = {k: 1.5 * abs(x - FX) / 1.5 for k, x in xs.items()}   # half-width

            def receiver(k, dim=1.0):
                x = xs[k]
                plate = Rectangle(width=0.16, height=1.05)
                paint(plate, ["#7A8591", "#2B3037"], lw=2, sheen=0.4, line="#0F1316")
                plate.move_to([x, AY, 0])
                hw = max(width[k], 0.06)
                sp = Ellipse(width=0.18, height=min(2 * hw, 1.0), fill_color="#FFE9A8",
                             fill_opacity=min(1.0, 0.16 / hw + 0.15), stroke_width=0)
                sp.move_to([x + 0.0, AY, 0])
                lab = T(names[k], 22, cols[k]).move_to([x, AY - 0.95, 0])
                g = VGroup(plate, sp, lab)
                g.set_opacity(dim)
                return g
            recs = {k: receiver(k, 0.28) for k in "ABC"}
            lit = {k: receiver(k, 1.0) for k in "ABC"}
            self.add(*recs.values())
            levels = {"A": 0.55, "B": 0.95, "C": 0.5}
            self.meter_label()
            ms = {k: self.meter(v) for k, v in levels.items()}
            note = {"A": ("A, BEFORE F:", "STILL CONVERGING,", "SPREAD ON THE VESSEL"),
                    "B": ("B, AT F:", "TIGHTEST BUNDLE,", "MOST CONCENTRATED"),
                    "C": ("C, BEYOND F:", "SPREADING AGAIN,", "LARGE SPOT")}
            cards = {k: pcard("", list(v), cols[k], size=20, w=PW) for k, v in note.items()}
            for k, c in cards.items():
                P(c, PX, 1.35 - {"A": 0, "B": 1.55, "C": 3.1}[k])
            final = pcard("", ["BEFORE F: SPREAD", "AT F: MOST", "CONCENTRATED", "AFTER F: SPREAD AGAIN"],
                          CHALK_YELLOW, size=18, w=PW, gap=0.07)
            P(final, PX, -1.55)
            self.add(ms["A"])
            cur = {"m": ms["A"]}
            self.cue(tr, "b0", ReplacementTransform(recs["A"], lit["A"]), FadeIn(cards["A"]),
                     sfx="pop")
            self.cue(tr, "b1", ReplacementTransform(lit["A"], recs["A"].copy().set_opacity(0.28)),
                     ReplacementTransform(recs["B"], lit["B"]), ReplacementTransform(ms["A"], ms["B"]),
                     FadeIn(cards["B"]), sfx="ding", rt=0.9)
            self.cue(tr, "b2", ReplacementTransform(lit["B"], recs["B"].copy().set_opacity(0.28)),
                     ReplacementTransform(recs["C"], lit["C"]), ReplacementTransform(ms["B"], ms["C"]),
                     FadeIn(cards["C"]), sfx="click", rt=0.9)
            self.cue(tr, "b3", FadeOut(cards["A"]), FadeOut(cards["B"]), FadeOut(cards["C"]),
                     FadeIn(final), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 9 ----
    def beat_s9(self):
        with self.narrate("s9q") as tr:
            self.heading("YOUR TURN", "Light, focus and the cooker.", CHALK_PINK)
            specs = [("A", "Parallel rays hit a concave mirror. Where do they go?", CHALK_CYAN),
                     ("B", "Vessel: before F, at F or beyond F?", CHALK_AMBER),
                     ("C", "Which mirror: plane, convex or concave?", CHALK_GREEN),
                     ("D", "What if the vessel is far beyond F?", CHALK_PINK)]
            rows = [qa_row(l, q, "?", c, w=11.8, h=0.76, size=26) for l, q, c in specs]
            for r_, y in zip(rows, (1.38, 0.46, -0.46, -1.38)):
                P(r_, CX, y)
            for k, r_ in enumerate(rows):
                self.cue(tr, f"b{k}", FadeIn(r_), sfx="pop" if k == 0 else "click")
            self.finish(tr)
            self._rows = rows
        self.think_clock()
        with self.narrate("s9a", reset=False) as tr:
            ans = [("THROUGH F", CHALK_CYAN), ("AT F", CHALK_AMBER),
                   ("CONCAVE", CHALK_GREEN), ("MORE SPREAD OUT", CHALK_PINK)]
            for k in range(4):
                new = T(ans[k][0], 26, ans[k][1], max_w=4.2)
                new.move_to(self._rows[k].slot.get_center())
                new.align_to(self._rows[k].slot, RIGHT)
                self.cue(tr, f"b{k}", ReplacementTransform(self._rows[k].slot, new),
                         sfx="click" if k < 3 else "success", rt=0.5)
            bn = self.banner("MOVE THE VESSEL BACK TOWARDS F", CHALK_GREEN, 24, y=-2.45, x=CX)
            self.cue(tr, "b3", FadeIn(bn), sfx=None)
            self.finish(tr)

    # ----------------------------------------------------------- scene 10 ----
    def beat_s10(self):
        with self.narrate("s10") as tr:
            self.heading("COLLECT, REFLECT, FOCUS, HEAT")
            self.sun()
            self.axis_line()
            steps = [("1  SUN FAR AWAY", SUNC), ("2  REFLECTION", REFC),
                     ("3  FOCAL POINT F", CHALK_YELLOW), ("4  VESSEL AT F", CHALK_CYAN),
                     ("5  HEATING", CHALK_RED)]
            chips = [pchip(t, c, 22, h=0.6) for t, c in steps]
            stack(chips, top=PAN_TOP, gap=0.22, x=PX)
            incoming = VGroup(*[ray([(X0, AY + o), tuple(hit_point(AY + o)[0])], SUNC, 3.2)
                                for o in OFFS])
            dish = self.dish()
            refl = VGroup(*[ray([tuple(hit_point(AY + o)[0]), (FX, AY)], REFC, 3.2)
                            for o in OFFS])
            gl = glow([FX, AY], 0.2)
            flab = T("F", 24, CHALK_YELLOW).move_to([FX - 0.05, AY - 0.55, 0])
            vessel = pot(0.8, 0.55).move_to([FX, AY, 0])
            self.meter_label()
            m0, m1 = self.meter(0.1), self.meter(0.95)
            self.add(m0)
            self.cue(tr, "b0", FadeIn(chips[0]), FadeIn(incoming), sfx="pop")
            self.cue(tr, "b1", FadeIn(chips[1]), FadeIn(dish), sfx="click")
            self.cue(tr, "b2", FadeIn(refl), FadeIn(gl), FadeIn(flab), FadeIn(chips[2]),
                     sfx="ding")
            self.cue(tr, "b3", FadeIn(vessel), FadeIn(chips[3]), sfx="click")
            self.cue(tr, "b4", ReplacementTransform(m0, m1), FadeIn(chips[4]), sfx="success",
                     rt=1.4, snap="method")
            self.hold(tr, "b5")
            keep = [m_ for m_ in self.mobjects if m_ not in self.fixtures]
            self.go(*[FadeOut(m_) for m_ in keep], rt=0.6)
            names = [("PARALLEL\nSUN RAYS", SUNC), ("CONCAVE\nREFLECTOR", REFC),
                     ("FOCUS F", CHALK_YELLOW), ("VESSEL", CHALK_CYAN),
                     ("HEATING /\nCOOKING", CHALK_RED)]
            parts = []
            for k, (t, c) in enumerate(names):
                ch = pchip(t, c, 22, w=2.1)
                parts.append(ch)
                if k < len(names) - 1:
                    parts.append(arrow([0, 0, 0], [0.4, 0, 0], CHALK_WHITE, 5, 0.17))
            row = VGroup(*parts).arrange(RIGHT, buff=0.12)
            fit(row, 12.3)
            P(row, CX, 0.85)
            slogan = P(T("COLLECT → REFLECT → FOCUS → HEAT", 44, CHALK_YELLOW,
                         max_w=12.2), CX, -0.55)
            self.cue(tr, "b5", FadeIn(row), FadeIn(slogan), sfx="success")
            idea = self.banner("THAT IS THE OPTICAL IDEA BEHIND THE SOLAR COOKER.",
                               CHALK_GREEN, 24, y=-1.75, x=CX)
            self.cue(tr, "b6", FadeIn(idea), sfx="ding")
            self.hold(tr, "b7")
            self.go(FadeOut(row), FadeOut(slogan), FadeOut(idea), rt=0.6)
            thanks = P(T("Thank You for Watching!", 60, CHALK_WHITE, max_w=11.8), CX, 0.60)
            bye = P(T("See you in the next lesson :)", 44, CHALK_YELLOW, max_w=11.0), CX, -0.75)
            self.cue(tr, "b7", FadeIn(thanks, shift=UP * 0.1), sfx=None)
            self.cue(tr, "b8", FadeIn(bye, shift=UP * 0.1), sfx=None)
            self.finish(tr)
        if not self.still:
            self.wait(END_HOLD)


def mm_(tex, size, col):
    return M(tex, size, col)


def TX_path(points):
    """An invisible smooth path through `points` (for MoveAlongPath)."""
    m = VMobject()
    m.set_points_as_corners([np.array(p, dtype=float) for p in points])
    m.set_stroke(opacity=0).set_fill(opacity=0)
    return m

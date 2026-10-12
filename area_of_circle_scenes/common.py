"""Shared constants, narration, and art for the Area of a Circle lesson.

Rewritten for a Class 5 audience.  Three rules this version follows:

  * Every sentence is short and names a thing a child has held: a coin, a
    chapati, a tree trunk, a pizza.  No "parallelogram", no "calculus",
    no "sector" before the picture has earned it.
  * The proof is the onion proof, not the pizza proof.  A circle is made
    of rings; pull each ring straight; stack them and a triangle appears.
    That is one physical action a ten-year-old can picture, instead of
    three ideas held at once.
  * The lesson greets the viewer at the start and thanks them at the end.

Timing is video-first: each scene's run_times are authored to a fixed
total (written in a comment at the foot of the scene), the narration is
written to that length, and tune_all.py fits the speaking rate to it.
"""
from __future__ import annotations

import sys
import os
import numpy as np
from manim import (
    ORIGIN, UP, DOWN, LEFT, RIGHT, IN, OUT, DL, UL, UR, DR,
    PI, TAU, DEGREES, BLACK, WHITE,
    MathTex, Tex, VGroup, VMobject, Circle, Sector, Annulus, Rectangle,
    Square, Line, Arc, ArcBetweenPoints, Dot, DashedLine, Arrow, Vector,
    Polygon, Ellipse, Brace, BraceBetweenPoints, Star,
    SurroundingRectangle, RoundedRectangle, Angle, RightAngle,
    FunctionGraph, ParametricFunction, NumberPlane,
    FadeIn, FadeOut, Write, Create, Uncreate, Indicate, DrawBorderThenFill,
    ReplacementTransform, Transform, TransformMatchingTex, TransformFromCopy,
    GrowFromCenter, GrowFromEdge, GrowArrow, SpinInFromNothing, ShrinkToCenter,
    FadeTransform, Flash, Wiggle, ShowPassingFlash, Circumscribe, FocusOn,
    ApplyWave, LaggedStart, LaggedStartMap, Succession, AnimationGroup,
    MoveAlongPath, Rotate, Rotating, SpiralIn,
    ValueTracker, DecimalNumber, Integer, always_redraw, TracedPath,
    ImageMobject, Group,
    Text, rate_functions, config,
)
from manim_voiceover import VoiceoverScene

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lesson_kit import (
    BG, INK, MUTED, ACCENT, SUCCESS, AMBER, ROSE, VIOLET, PANEL,
    txt as _kit_txt, heading as _kit_heading, punch, card, rule_line,
    overview_panel, blueprint_grid, FRAME_W, FRAME_H, END_HOLD,
)
from speech_service import get_speech_service
from sound_effects import load_all as load_sfx

# --------------------------------------------------------------- contrast --
# The shared palette is tuned for a flat dark slide.  This lesson sits on a
# lit backdrop, so the ink goes brighter and the greys lift off the ground.
INK = "#FFFFFF"
MUTED = "#B7C7DC"
ACCENT = "#4CC9FF"
SUCCESS = "#3DE0A6"
AMBER = "#FFC53D"
ROSE = "#FF8095"
VIOLET = "#CE93FF"

# 3b1b runs on a mid grey (#333333) rather than near-black, because
# colour reads louder off a lifted ground.  Same idea, kept blue.
BG_TOP = "#1A3A66"        # lit sky at the top of the frame
BG_BOTTOM = "#0B1730"     # deep, but not a black hole, at the bottom
GLOW = "#3F74BA"          # the soft pool of light behind the action


# ------------------------------------------------------------------ fonts --
# This lesson is for ten-year-olds, so the type is round and open rather
# than the Calibri the other two lessons use.  Headings get a geometric
# face whose bowls echo the circles the whole video is about.
FONT_BODY = "Arial Rounded MT"
FONT_HEAD = "Century Gothic"


def txt(s: str, size: int = 32, color: str = INK, weight: str = "NORMAL",
        font: str | None = None) -> Text:
    """Prose, in the lesson's own rounded face."""
    return Text(s, font=font or FONT_BODY, font_size=size, color=color,
                weight=weight)


def heading(s: str, color: str = AMBER, size: int = 40) -> Text:
    """Big friendly heading in the geometric face."""
    return txt(s, size, color, "BOLD", FONT_HEAD)


TEAL = "#2DD4BF"
SKY = "#38BDF8"
LIME = "#A3E635"
ORANGE = "#FB923C"
DOUGH = "#E8B96A"
DOUGH_DARK = "#C08A3E"
BRASS = "#D4A843"

SCENE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(SCENE_DIR, "images")

VOICEOVER_CACHE_DIR = os.path.join(SCENE_DIR, "media", "voiceovers")

# Filled in by tune_all.py once the animation lengths are settled.
BEAT_RATE = {
    "greeting": "+9%", "intro": "+9%", "title": "+9%", "hard": "+9%",
    "words": "+9%", "idea": "+9%", "rings": "+9%", "unroll": "+9%",
    "formula": "+9%", "pizza": "+9%", "working": "+9%", "example1": "+9%",
    "example2": "+9%", "summary": "+9%", "thanks": "+9%",
}


def scene_speech_service(beat: str):
    return get_speech_service(cache_dir=VOICEOVER_CACHE_DIR, rate=BEAT_RATE[beat])


NARRATION = {
    "greeting": (
        "Hello friends! Welcome back. "
        "Today we will solve a puzzle that is two thousand years old. "
        "And you will solve it yourself. "
        "Let us go!"
    ),
    "intro": (
        "Look around you. How many round things can you see? "
        "The wheels on a bus. The clock on the wall. "
        "A hot chapati on your plate. A one rupee coin. "
        "Circles are everywhere. "
        "Now here is my question. "
        "If I wanted to paint one circle, how much paint would I need? "
        "That is called the area."
    ),
    "title": (
        "So today, let us find the area of a circle. "
        "Where does pi r squared come from?"
    ),
    "hard": (
        "Finding the space inside a square is easy. "
        "Just count the little boxes. "
        "Four across, four down. Sixteen boxes. Done! "
        "Now try that with a circle. "
        "Look at the edge. It curves. The boxes do not fit. "
        "Some get cut in half, some in quarters. "
        "Counting boxes will never work here. "
        "We need a smarter trick."
    ),
    "words": (
        "Before the trick, three words. "
        "This dot in the middle is the centre. "
        "This line from the centre out to the edge is the radius. "
        "We call it r. "
        "And if you took a string and walked it all the way around, "
        "that distance is the circumference. "
        "People found long ago that it is always two times pi times r."
    ),
    "idea": (
        "Archimedes had a simple idea. "
        "If you cut a shape into pieces and move the pieces around, "
        "you still have exactly the same amount. "
        "Nothing is lost. "
        "So cut the circle up, and build a shape you already know."
    ),
    "rings": (
        "Here is the secret. A circle is not one shape. "
        "It is made of rings. Like the rings inside a tree trunk. "
        "A tiny ring in the middle. A bigger one around it. "
        "A bigger one around that. All the way out to the edge. "
        "Watch. Eight rings. Sixteen. Thirty two. "
        "The thinner they get, the more the circle is just rings."
    ),
    "unroll": (
        "Now the magic. Take each ring and pull it straight. "
        "The outside ring is the longest, "
        "because it goes all the way around. "
        "That length is two pi r. "
        "The next ring in is a little shorter. "
        "And the next one shorter still. "
        "Right at the centre, the ring is just a dot. "
        "Now stack them up, longest at the bottom, shortest on top. "
        "Look what appears. A triangle! "
        "The circle has become a triangle."
    ),
    "formula": (
        "And triangles are easy. "
        "Area is half of base times height. "
        "The base is the longest ring, two pi r. "
        "The height is the radius, r. "
        "So area is half, times two pi r, times r. "
        "The half and the two cancel out. "
        "And what is left is pi r squared. "
        "That is our answer!"
    ),
    "pizza": (
        "There is another way to see it. "
        "Cut the circle like a pizza. "
        "Lay the slices in a row, one up, one down. "
        "Cut thinner and thinner, and you get a rectangle. "
        "It is r tall, and pi r wide. "
        "Multiply, and you get pi r squared again."
    ),
    "working": (
        "Let us use it. "
        "Someone measured all the way around a circle "
        "and got twenty two centimetres. "
        "Can we find the area? First we need r. "
        "The way around is two pi r. So two pi r is twenty two. "
        "Put pi as twenty two by seven. Do the division. "
        "And r is three point five centimetres."
    ),
    "example1": (
        "Now the formula. Area is pi r squared. "
        "Twenty two by seven, times three point five, "
        "times three point five. "
        "Three point five times three point five is twelve point two five. "
        "And the area is thirty eight point five square centimetres."
    ),
    "example2": (
        "One more, and this time you try first. "
        "A round garden has a radius of seven metres. "
        "Pause the video and work it out. "
        "Ready? Area is pi r squared. "
        "Twenty two by seven, times seven, times seven. "
        "The sevens cancel. "
        "And the answer is one hundred and fifty four square metres."
    ),
    "summary": (
        "So remember. A circle is made of rings. "
        "Pull the rings straight and stack them, "
        "and you get a triangle. "
        "Half of two pi r, times r. That is pi r squared. "
        "Every single time."
    ),
    "thanks": (
        "And that is it! "
        "You just solved a two thousand year old puzzle. Well done. "
        "Thanks for watching. "
        "If this helped you, share it with a friend. "
        "See you in the next video!"
    ),
}

# ---------------------------------------------------------------- geometry --
R_CIRC = 1.35                 # the circle every proof scene uses
N_RINGS = 34                  # rings the onion proof is built from
RING_W = 5.6                  # stroke width that makes the bands just touch


def mtx(s: str, size: int = 36, color: str = INK) -> MathTex:
    """All on-screen mathematics goes through here."""
    return MathTex(s, font_size=size, color=color)


def ring_radii(n: int = N_RINGS, radius: float = R_CIRC):
    """Mid-radius of each ring, so none of them is degenerate at zero."""
    return [radius * (i + 0.5) / n for i in range(n)]


def ring_colour(t: float, radius: float = R_CIRC) -> str:
    """Outer rings warm, inner rings cool — so the stack reads as ordered."""
    f = t / radius
    stops = [(0.0, VIOLET), (0.35, ROSE), (0.7, ORANGE), (1.0, AMBER)]
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        if f <= b:
            k = 0.0 if b == a else (f - a) / (b - a)
            ca_rgb = [int(ca[i:i + 2], 16) for i in (1, 3, 5)]
            cb_rgb = [int(cb[i:i + 2], 16) for i in (1, 3, 5)]
            mix = [round(x + (y - x) * k) for x, y in zip(ca_rgb, cb_rgb)]
            return "#%02X%02X%02X" % tuple(mix)
    return AMBER


def unrolled_ring(t: float, alpha: float, centre, base_mid,
                  radius: float = R_CIRC, n: int = 96,
                  color: str | None = None, width: float = RING_W) -> VMobject:
    """One ring of radius `t`, part-way through being pulled straight.

    alpha = 1 -> a full circle of radius t, centred on `centre`
    alpha = 0 -> a straight segment of length 2*pi*t, sitting at the height
                 this ring occupies in the finished triangle whose base
                 midpoint is `base_mid`

    In between, the ring is an arc of radius t/alpha subtending 2*pi*alpha:
    the same length of "wire", bent less and less.  That is a real unroll,
    not a shape morph — the arc length never changes.
    """
    L = TAU * t
    centre = np.asarray(centre, dtype=float)
    base_mid = np.asarray(base_mid, dtype=float)

    # The ring's lowest point travels from the circle to its slot in the
    # triangle; everything else is built relative to it.
    a_circle = centre + np.array([0.0, -t, 0.0])
    a_tri = base_mid + np.array([0.0, radius - t, 0.0])
    anchor = a_tri + (a_circle - a_tri) * alpha

    s = np.linspace(-L / 2.0, L / 2.0, n)
    if alpha < 1e-4:
        pts = [anchor + np.array([x, 0.0, 0.0]) for x in s]
    else:
        rho = t / alpha
        phi = s / rho
        pts = [anchor + np.array([rho * np.sin(p), rho * (1 - np.cos(p)), 0.0])
               for p in phi]

    m = VMobject(stroke_color=color or ring_colour(t, radius),
                 stroke_width=width)
    m.set_points_as_corners(pts)
    return m


def ring_stack(alpha: float, centre, base_mid, n: int = N_RINGS,
               radius: float = R_CIRC, width: float = RING_W) -> VGroup:
    """Every ring of the circle at the same point in the unroll."""
    return VGroup(*[
        unrolled_ring(t, alpha, centre, base_mid, radius, width=width)
        for t in ring_radii(n, radius)
    ])


def wedge(i: int, n: int, color: str, radius: float = R_CIRC) -> Sector:
    """One pizza slice, for the secondary proof."""
    # CE 0.21 renamed Sector's first argument to `radius`
    return Sector(radius=radius, angle=TAU / n, start_angle=i * TAU / n,
                  fill_color=color, fill_opacity=0.9,
                  stroke_color=BG, stroke_width=1.5)


def sliced_circle(n: int, radius: float = R_CIRC,
                  c1: str = SKY, c2: str = ROSE) -> VGroup:
    return VGroup(*[wedge(i, n, c1 if i % 2 == 0 else c2, radius)
                    for i in range(n)])


def interlocked(n: int, radius: float = R_CIRC,
                c1: str = SKY, c2: str = ROSE) -> VGroup:
    """Slices laid out alternately up/down — the pizza proof's payoff.

    Two things matter here.  Each slice must point UP (apex down, arc on
    top) before every second one is flipped, and neighbours sit half an arc
    apart, not a whole one, because the up and down slices interleave.  The
    row then comes out pi*r wide and r tall, which is the whole point.
    """
    w = TAU * radius / (2 * n)
    g = VGroup()
    for i in range(n):
        s = wedge(0, n, c1 if i % 2 == 0 else c2, radius)
        s.rotate(PI / 2 - TAU / (2 * n), about_point=ORIGIN)   # point it up
        if i % 2:
            s.rotate(PI, about_point=ORIGIN)                   # flip it down
            s.shift(UP * radius)
        s.shift(RIGHT * (i * w - (n - 1) * w / 2))
        g.add(s)
    return g


# ------------------------------------------------------------ everyday art --
def bus_wheel(centre, r: float = 0.62) -> VGroup:
    c = np.asarray(centre, dtype=float)
    tyre = Circle(radius=r, stroke_color="#4B5563", stroke_width=10,
                  fill_color="#1F2937", fill_opacity=1).move_to(c)
    hub = Circle(radius=r * 0.30, stroke_color=MUTED, stroke_width=3,
                 fill_color="#9CA3AF", fill_opacity=1).move_to(c)
    spokes = VGroup(*[
        Line(c + r * 0.30 * np.array([np.cos(a), np.sin(a), 0]),
             c + r * 0.86 * np.array([np.cos(a), np.sin(a), 0]),
             stroke_color="#9CA3AF", stroke_width=4)
        for a in np.arange(0, TAU, TAU / 6)
    ])
    return VGroup(tyre, spokes, hub)


def wall_clock(centre, r: float = 0.62) -> VGroup:
    c = np.asarray(centre, dtype=float)
    face = Circle(radius=r, stroke_color=BRASS, stroke_width=7,
                  fill_color="#FFF7ED", fill_opacity=1).move_to(c)
    ticks = VGroup(*[
        Line(c + r * 0.82 * np.array([np.cos(a), np.sin(a), 0]),
             c + r * 0.94 * np.array([np.cos(a), np.sin(a), 0]),
             stroke_color="#57534E", stroke_width=3)
        for a in np.arange(0, TAU, TAU / 12)
    ])
    hour = Line(c, c + r * 0.45 * np.array([np.cos(PI / 3), np.sin(PI / 3), 0]),
                stroke_color="#1C1917", stroke_width=6)
    minute = Line(c, c + r * 0.75 * np.array([0, 1, 0]),
                  stroke_color="#1C1917", stroke_width=4)
    pin = Dot(c, radius=0.045, color="#1C1917")
    return VGroup(face, ticks, hour, minute, pin)


def chapati(centre, r: float = 0.62) -> VGroup:
    c = np.asarray(centre, dtype=float)
    base = Circle(radius=r, stroke_color=DOUGH_DARK, stroke_width=5,
                  fill_color=DOUGH, fill_opacity=1).move_to(c)
    spots = VGroup(*[
        Circle(radius=r * s, stroke_width=0, fill_color=DOUGH_DARK,
               fill_opacity=0.55).move_to(c + r * np.array([dx, dy, 0]))
        for s, dx, dy in ((0.13, -0.35, 0.22), (0.09, 0.30, -0.10),
                          (0.11, 0.10, 0.42), (0.07, -0.12, -0.40),
                          (0.08, 0.44, 0.34))
    ])
    return VGroup(base, spots)


def coin(centre, r: float = 0.52) -> VGroup:
    c = np.asarray(centre, dtype=float)
    body = Circle(radius=r, stroke_color="#A16207", stroke_width=5,
                  fill_color=BRASS, fill_opacity=1).move_to(c)
    rim = Circle(radius=r * 0.80, stroke_color="#A16207", stroke_width=2,
                 fill_opacity=0).move_to(c)
    one = mtx("1", 34, "#7C4A03").move_to(c)
    return VGroup(body, rim, one)


def tree_rings(centre, r: float = 1.0, n: int = 7) -> VGroup:
    """A tree-trunk cross section — the picture the ring idea leans on."""
    c = np.asarray(centre, dtype=float)
    bark = Circle(radius=r, stroke_color="#5B3A1E", stroke_width=8,
                  fill_color="#B98B57", fill_opacity=1).move_to(c)
    rings = VGroup(*[
        Circle(radius=r * (i + 1) / (n + 1), stroke_color="#7A5230",
               stroke_width=3, fill_opacity=0).move_to(c)
        for i in range(n)
    ])
    return VGroup(bark, rings)


def frac(num: str, den: str, size: int = 44, color: str = INK) -> VGroup:
    """A fraction built from separate parts.

    LaTeX renders \frac as one blob whose glyph indices shift with the
    content, which makes striking out just the denominator brittle.  Built
    this way, .num, .bar and .den are each their own mobject.
    """
    n = mtx(num, size, color)
    d = mtx(den, size, color)
    w = max(n.width, d.width) + 0.16
    bar = Line(LEFT * w / 2, RIGHT * w / 2, stroke_color=color,
               stroke_width=3.5)
    n.next_to(bar, UP, buff=0.10)
    d.next_to(bar, DOWN, buff=0.10)
    g = VGroup(n, bar, d)
    g.num, g.bar, g.den = n, bar, d
    return g


def strike(m, color: str = ROSE, pad: float = 0.09, width: float = 6.0) -> Line:
    """The pencil stroke you draw through a term that cancels."""
    a = m.get_corner(DL) + np.array([-pad, -pad, 0.0])
    b = m.get_corner(UR) + np.array([pad, pad, 0.0])
    return Line(a, b, stroke_color=color, stroke_width=width)


def cancel_pair(m1, m2, color: str = ROSE):
    """Two strokes plus the little arc that ties the cancelling terms."""
    s1, s2 = strike(m1, color), strike(m2, color)
    link = ArcBetweenPoints(m1.get_top() + UP * 0.10,
                            m2.get_top() + UP * 0.10,
                            angle=-PI / 2.6, stroke_color=color,
                            stroke_width=3, stroke_opacity=0.75)
    return s1, s2, link


def chip(m, color: str = "#050A14", opacity: float = 0.72,
         buff: float = 0.14) -> VGroup:
    """A soft dark plate behind a label so it reads over busy artwork."""
    plate = RoundedRectangle(
        width=m.width + 2 * buff, height=m.height + 2 * buff,
        corner_radius=0.10, stroke_width=0,
        fill_color=color, fill_opacity=opacity).move_to(m.get_center())
    return VGroup(plate, m)


def flower(centre, r: float = 0.13, petal: str = "#FF8FA3",
           heart: str = "#FFD166") -> VGroup:
    """Five petals round a bright centre."""
    c = np.asarray(centre, dtype=float)
    petals = VGroup(*[
        Ellipse(width=r * 1.05, height=r * 2.0, stroke_width=0,
                fill_color=petal, fill_opacity=0.95)
        .move_to(c + r * 0.95 * np.array([np.cos(a), np.sin(a), 0.0]))
        .rotate(a - PI / 2,
                about_point=c + r * 0.95 * np.array([np.cos(a), np.sin(a), 0.0]))
        for a in np.arange(0, TAU, TAU / 5)
    ])
    eye = Circle(radius=r * 0.52, stroke_width=0, fill_color=heart,
                 fill_opacity=1).move_to(c)
    return VGroup(petals, eye)


def garden(centre, radius: float = 1.55, seed: int = 5) -> VGroup:
    """A round garden: turf, blades of grass, and flowers in the beds."""
    c = np.asarray(centre, dtype=float)
    rng = np.random.default_rng(seed)

    soil = Circle(radius=radius, stroke_color="#6B8F3A", stroke_width=6,
                  fill_color="#2C6B34", fill_opacity=1).move_to(c)
    # mown stripes, lighter and darker green
    stripes = VGroup()
    for i in range(-4, 5):
        y = i * radius / 4.6
        half = np.sqrt(max(radius ** 2 - y ** 2, 0.0))
        if half < 0.05:
            continue
        stripes.add(Rectangle(width=2 * half, height=radius / 5.2,
                              stroke_width=0, fill_color="#37803D",
                              fill_opacity=0.55 if i % 2 == 0 else 0.0)
                    .move_to(c + np.array([0.0, y, 0.0])))

    blades = VGroup()
    for _ in range(70):
        a = rng.uniform(0, TAU)
        d = radius * np.sqrt(rng.uniform(0.0, 0.94))
        b = c + d * np.array([np.cos(a), np.sin(a), 0.0])
        h = rng.uniform(0.10, 0.20)
        lean = rng.uniform(-0.35, 0.35)
        blades.add(Line(b, b + np.array([lean * h, h, 0.0]),
                        stroke_color="#8FCB55", stroke_width=2,
                        stroke_opacity=rng.uniform(0.55, 0.95)))

    cols = [("#FF8FA3", "#FFD166"), ("#FFD1E8", "#FFB703"),
            ("#C7A8FF", "#FFE08A"), ("#FFFFFF", "#FFC53D")]
    blooms = VGroup()
    for k in range(11):
        a = rng.uniform(0, TAU)
        d = radius * np.sqrt(rng.uniform(0.05, 0.80))
        petal, heart = cols[k % len(cols)]
        blooms.add(flower(c + d * np.array([np.cos(a), np.sin(a), 0.0]),
                          rng.uniform(0.10, 0.15), petal, heart))

    return VGroup(soil, stripes, blades, blooms)


def _glow_array(w: int = 480, h: int = 270, strength: float = 0.62):
    """A smooth elliptical falloff as RGBA pixels.

    Stacking translucent ellipses gives visible rings — the eye picks out
    every step.  Painting the falloff per-pixel is banding-free.
    """
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt((((xx - w / 2) / (w * 0.60)) ** 2)
                + (((yy - h / 2) / (h * 0.72)) ** 2))
    a = np.clip(1.0 - d, 0.0, 1.0) ** 1.7
    # 8-bit alpha still steps visibly at low values; a whisper of noise
    # dithers those steps away.
    a = np.clip(a + np.random.default_rng(3).normal(0.0, 0.006, a.shape),
                0.0, 1.0)
    r, g, b = (int(GLOW[i:i + 2], 16) for i in (1, 3, 5))
    img = np.zeros((h, w, 4), dtype=np.uint8)
    img[..., 0], img[..., 1], img[..., 2] = r, g, b
    img[..., 3] = (a * strength * 255).astype(np.uint8)
    return img


def lesson_backdrop(dots: int = 34, seed: int = 11) -> Group:
    """A lit stage rather than a flat dark slide.

    A vertical gradient gives the frame a floor and a sky, one smooth pool
    of light lifts the middle so figures read against it, and a scatter of
    faint specks keeps the empty corners alive.
    """
    base = Rectangle(width=FRAME_W, height=FRAME_H, stroke_width=0)
    base.set_fill(color=[BG_TOP, BG_BOTTOM], opacity=1)

    glow = ImageMobject(_glow_array())
    glow.set(width=FRAME_W * 1.25)
    glow.move_to(ORIGIN)

    rng = np.random.default_rng(seed)
    specks = VGroup(*[
        Dot(np.array([rng.uniform(-FRAME_W / 2 + 0.3, FRAME_W / 2 - 0.3),
                      rng.uniform(-FRAME_H / 2 + 0.3, FRAME_H / 2 - 0.3), 0.0]),
            radius=rng.uniform(0.012, 0.032), color=WHITE,
            fill_opacity=rng.uniform(0.10, 0.32))
        for _ in range(dots)
    ])
    return Group(base, glow, specks)


def counting_grid(centre, side: float, n: int, color: str = SKY) -> VGroup:
    """An n x n grid of little boxes filling a square of the given side."""
    c = np.asarray(centre, dtype=float)
    cell = side / n
    g = VGroup()
    for i in range(n):
        for j in range(n):
            g.add(Rectangle(width=cell, height=cell,
                            stroke_color=color, stroke_width=2,
                            fill_color=color, fill_opacity=0.18)
                  .move_to(c + np.array([(i - n / 2 + 0.5) * cell,
                                         (j - n / 2 + 0.5) * cell, 0.0])))
    return g

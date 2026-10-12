"""Shared constants, narration, and art for "What is Trigonometry?".

This is the part-one video: it answers only "what is this subject and why
does it exist", for a school kid who has never met it.  The mechanics —
tan tables, worked examples, similar-triangle proofs — live in the
companion lesson, trigonometry_scenes ("Heights and Distances").

Three rules:
  * Explain the WORD before anything else.  "Trigonometry" is frightening
    until you see it is TRI + GONO + METRY, three-corners-measuring.
  * Never show arithmetic.  This video shows that the trick works; the
    other one shows how to do it.
  * Three beats leave the plane.  Rigidity and "the triangle is standing
    in the real world" are three-dimensional facts, so they are shown in
    three dimensions rather than asserted.

Timing is video-first: each scene's run_times are authored to a fixed
total, the narration is written to that length, and tune_all.py fits the
speaking rate to it.
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
    Polygon, Ellipse, Brace, BraceBetweenPoints, Star, Angle, RightAngle,
    SurroundingRectangle, RoundedRectangle, CurvedArrow,
    Line3D, Prism, Cube, Sphere, Dot3D, Surface, ThreeDAxes, ThreeDScene,
    FadeIn, FadeOut, Write, Create, Uncreate, Indicate, DrawBorderThenFill,
    ReplacementTransform, Transform, TransformMatchingTex, TransformFromCopy,
    GrowFromCenter, GrowFromEdge, GrowArrow, SpinInFromNothing, ShrinkToCenter,
    FadeTransform, Flash, Wiggle, ShowPassingFlash, Circumscribe, FocusOn,
    ApplyWave, LaggedStart, Succession, AnimationGroup, MoveAlongPath,
    Rotate, Rotating, SpiralIn,
    ValueTracker, DecimalNumber, Integer, always_redraw, TracedPath,
    ImageMobject, Group, Text, LineJointType, rate_functions, config,
)
from manim_voiceover import VoiceoverScene

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lesson_kit import (
    BG, PANEL, card, rule_line, blueprint_grid, FRAME_W, FRAME_H, END_HOLD,
)
from speech_service import get_speech_service
from sound_effects import load_all as load_sfx
from human_figure import Man, STANDING, POINTING_UP, LOOKING_UP, WALK_A, WALK_B

SCENE_DIR = os.path.dirname(os.path.abspath(__file__))
VOICEOVER_CACHE_DIR = os.path.join(SCENE_DIR, "media", "voiceovers")

# --------------------------------------------------------------- contrast --
# Same lifted stage as the circle lesson: colour reads louder off a lit
# ground than off near-black.
INK = "#FFFFFF"
MUTED = "#B7C7DC"
ACCENT = "#4CC9FF"
SUCCESS = "#3DE0A6"
AMBER = "#FFC53D"
ROSE = "#FF8095"
VIOLET = "#CE93FF"
SKY = "#38BDF8"
LIME = "#A3E635"
ORANGE = "#FB923C"

BG_TOP = "#1A3A66"
BG_BOTTOM = "#0B1730"
GLOW = "#3F74BA"

WOOD = "#8A5A2B"
WOOD_DARK = "#6B451F"
LEAD = "#94A3B8"
GROUND = "#1C3A22"
GROUND_HI = "#2E5C36"

# ------------------------------------------------------------------ fonts --
FONT_BODY = "Arial Rounded MT"
FONT_HEAD = "Century Gothic"


def txt(s: str, size: int = 32, color: str = INK, weight: str = "NORMAL",
        font: str | None = None) -> Text:
    return Text(s, font=font or FONT_BODY, font_size=size, color=color,
                weight=weight)


def heading(s: str, color: str = AMBER, size: int = 42) -> Text:
    return txt(s, size, color, "BOLD", FONT_HEAD)


def mtx(s: str, size: int = 36, color: str = INK) -> MathTex:
    return MathTex(s, font_size=size, color=color)


BEAT_RATE = {
    # One pace for the whole video: every beat's narration was written to
    # the length of the animation it rides on, so every rate lands here.
    "greeting": "+9%", "word": "+9%", "rigid": "+9%", "cannot": "+9%",
    "trick": "+9%", "names": "+9%", "ratio": "+9%", "used": "+9%",
    "summary": "+9%", "thanks": "+9%",
}


def scene_speech_service(beat: str):
    return get_speech_service(cache_dir=VOICEOVER_CACHE_DIR, rate=BEAT_RATE[beat])


NARRATION = {
    "greeting": (
        "Hello friends! Today, just one question. "
        "What is trigonometry? "
        "It sounds like a big, scary word. "
        "But by the end of this video, you will know exactly what it means."
    ),
    "word": (
        "Look at this word. Trigonometry. "
        "Long, and a bit frightening. "
        "But watch what happens when we break it apart. "
        "Tri means three. "
        "Gono means corners. "
        "And metry means measuring. "
        "Put them back together. "
        "Three. Corners. Measuring. "
        "Trigonometry is just measuring triangles."
    ),
    "rigid": (
        "But why triangles? Why not squares? "
        "Here is why. "
        "Take three sticks and bolt them at the corners. "
        "Now push it. Go on, push hard. It will not move. "
        "Now take four sticks and do the same. "
        "Push it, and it leans. It squashes. "
        "It even folds right out of the flat page. "
        "The triangle is the only shape that cannot wobble. "
        "So if you know just a few parts of a triangle, "
        "every other part is already decided."
    ),
    "cannot": (
        "Now here is the problem trigonometry was invented to solve. "
        "How tall is that tree? You cannot climb it. "
        "How wide is that river? You cannot swim across with a tape. "
        "How far away is that ship? You cannot walk to it. "
        "Your measuring tape is useless. "
        "So how did people ever measure these things?"
    ),
    "trick": (
        "Here is the trick, and it is beautiful. "
        "You do not go to the tree at all. "
        "You walk backwards, along the ground, "
        "counting the steps as you go. "
        "That distance, you can measure. "
        "Then you look up at the top, "
        "and you measure the angle your eyes tilt through. "
        "That angle, you can measure too. "
        "And look. Those two things, "
        "and the corner where the tree meets the ground, "
        "make a triangle. "
        "A triangle standing in the real world. "
        "And a triangle cannot wobble. "
        "So the height is already decided."
    ),
    "names": (
        "Let us give the three sides their names. "
        "This one along the ground is the side you walked. "
        "This one standing up is the side you want. "
        "And this one, from your eye to the top, "
        "is your line of sight. "
        "That is all a triangle is. "
        "The side you walk, the side you want, "
        "and the line you look along."
    ),
    "ratio": (
        "And now the last idea. "
        "Stand closer, and you get a small triangle. "
        "Stand further back, and you get a big one. "
        "But if the angle stays the same, "
        "the big triangle is just the small one blown up. "
        "So the height divided by the distance "
        "gives the very same number every time. "
        "That number has a name. We call it tan. "
        "Sin, cos and tan are not monsters. "
        "They are just names for numbers that never change."
    ),
    "used": (
        "And people use this everywhere. "
        "Builders use it to raise a wall straight. "
        "Sailors used it to cross oceans "
        "before anybody had a map. "
        "Engineers use it to fly a rocket into space. "
        "And right now, satellites above your head "
        "are using triangles to tell your phone exactly where you are. "
        "Every single one of these is a triangle underneath."
    ),
    "summary": (
        "So, what did we learn today? "
        "Trigonometry means measuring triangles. "
        "A triangle cannot wobble, "
        "so a few parts fix all the rest. "
        "Measure one distance and one angle. "
        "And the triangle hands you the thing you could never reach. "
        "That is it. That is the whole idea."
    ),
    "thanks": (
        "And that is trigonometry. "
        "Not scary at all, is it? "
        "Now you know what the word means. "
        "Thanks for watching, and see you next time!"
    ),
}


# ------------------------------------------------------------------- stage --
def _glow_array(w: int = 480, h: int = 270, strength: float = 0.62):
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt((((xx - w / 2) / (w * 0.60)) ** 2)
                + (((yy - h / 2) / (h * 0.72)) ** 2))
    a = np.clip(1.0 - d, 0.0, 1.0) ** 1.7
    a = np.clip(a + np.random.default_rng(3).normal(0.0, 0.006, a.shape),
                0.0, 1.0)
    r, g, b = (int(GLOW[i:i + 2], 16) for i in (1, 3, 5))
    img = np.zeros((h, w, 4), dtype=np.uint8)
    img[..., 0], img[..., 1], img[..., 2] = r, g, b
    img[..., 3] = (a * strength * 255).astype(np.uint8)
    return img


def lesson_backdrop(dots: int = 34, seed: int = 11) -> Group:
    """A lit stage: gradient ground, one smooth pool of light, faint specks."""
    base = Rectangle(width=FRAME_W, height=FRAME_H, stroke_width=0)
    base.set_fill(color=[BG_TOP, BG_BOTTOM], opacity=1)
    glow = ImageMobject(_glow_array())
    glow.set(width=FRAME_W * 1.25).move_to(ORIGIN)
    rng = np.random.default_rng(seed)
    specks = VGroup(*[
        Dot(np.array([rng.uniform(-FRAME_W / 2 + 0.3, FRAME_W / 2 - 0.3),
                      rng.uniform(-FRAME_H / 2 + 0.3, FRAME_H / 2 - 0.3), 0.0]),
            radius=rng.uniform(0.012, 0.032), color=WHITE,
            fill_opacity=rng.uniform(0.10, 0.32))
        for _ in range(dots)
    ])
    return Group(base, glow, specks)


def stage_3d(scene):
    """Match a 3D scene's ground colour to the 2D stage.

    Fixed-in-frame mobjects are drawn on top of the 3D pass, so the image
    backdrop cannot be used here; a flat colour from the middle of the 2D
    gradient keeps the cut between scenes from jumping.
    """
    scene.camera.background_color = "#13294B"


def chip(m, color: str = "#050A14", opacity: float = 0.72,
         buff: float = 0.14) -> VGroup:
    """A soft dark plate behind a label so it reads over busy artwork."""
    plate = RoundedRectangle(
        width=m.width + 2 * buff, height=m.height + 2 * buff,
        corner_radius=0.10, stroke_width=0,
        fill_color=color, fill_opacity=opacity).move_to(m.get_center())
    return VGroup(plate, m)


def right_triangle(corner, base: float, height: float, color: str = ACCENT,
                   fill: float = 0.16, width: float = 7.0):
    """A RIGHT-angled triangle with its square corner marked.

    Every triangle a student meets in trigonometry has a right angle in
    it, so every triangle this video shows has one too.  BEVEL joints keep
    the sharp corner from spiking (technique from the repo's
    manimce-public-animations/SHORT_ANIMS/pythagorean_theorem.py).
    """
    c = np.asarray(corner, dtype=float)
    a = c + RIGHT * base                      # along the ground
    b = c + UP * height                       # standing up
    tri = Polygon(c, a, b, stroke_color=color, stroke_width=width,
                  fill_color=color, fill_opacity=fill,
                  joint_type=LineJointType.BEVEL)
    mark = RightAngle(Line(c, a), Line(c, b), length=min(0.42, base * 0.22),
                      color=MUTED, stroke_width=4)
    return tri, mark, (c, a, b)


# ------------------------------------------------------------ crisp 3D ----
# manim CE's cairo renderer draws Surface-based solids (Sphere, Prism,
# Line3D, Dot3D) as hundreds of small flat-shaded quads.  The result is
# banded and soft — it looks blurred next to the crisp 2D scenes.  Flat
# VMobject polygons with set_shade_in_3d(True) project as real vectors, so
# they stay razor sharp at any camera angle and still depth-sort.

def line3(p1, p2, color: str = INK, width: float = 8.0,
          opacity: float = 1.0) -> Line:
    """A crisp 3D line — a vector, not a shaded cylinder."""
    m = Line(np.asarray(p1, float), np.asarray(p2, float),
             stroke_color=color, stroke_width=width, stroke_opacity=opacity)
    m.set_shade_in_3d(True)
    return m


def dot3(point, color: str = AMBER, r: float = 0.085) -> Dot:
    m = Dot(np.asarray(point, float), color=color, radius=r)
    m.set_shade_in_3d(True)
    return m


def face3(pts, color: str, opacity: float = 1.0,
          stroke: float = 1.0) -> Polygon:
    """One flat face in space."""
    m = Polygon(*[np.asarray(p, float) for p in pts],
                fill_color=color, fill_opacity=opacity,
                stroke_color=color, stroke_width=stroke,
                joint_type=LineJointType.BEVEL)
    m.set_shade_in_3d(True)
    return m


def box3(centre, dx: float, dy: float, dz: float, top: str,
         lit: str, dark: str) -> VGroup:
    """A solid box from five flat faces (the base is never seen)."""
    c = np.asarray(centre, dtype=float)
    hx, hy, hz = dx / 2, dy / 2, dz / 2
    V = {(sx, sy, sz): c + np.array([sx * hx, sy * hy, sz * hz])
         for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)}
    spec = [([(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)], top),
            ([(-1,-1,-1),(1,-1,-1),(1,-1,1),(-1,-1,1)], lit),
            ([(1,-1,-1),(1,1,-1),(1,1,1),(1,-1,1)], dark),
            ([(-1,1,-1),(1,1,-1),(1,1,1),(-1,1,1)], lit),
            ([(-1,-1,-1),(-1,1,-1),(-1,1,1),(-1,-1,1)], dark)]
    return VGroup(*[face3([V[k] for k in keys], col) for keys, col in spec])


def fir3(base, height: float, radius: float, tiers: int = 3,
         shades=("#4ADE80", "#2F9E4F", "#1E7A3C")) -> VGroup:
    """A low-poly fir crown: stacked pyramids, all flat crisp faces.

    Replaces a Sphere, which the cairo renderer bands badly.
    """
    b = np.asarray(base, dtype=float)
    g = VGroup()
    for t in range(tiers):
        f = 1.0 - t / (tiers + 0.6)
        r = radius * f
        z0 = b[2] + height * (0.30 * t)
        z1 = z0 + height * 0.52
        ring = [b + np.array([r * np.cos(a), r * np.sin(a), z0 - b[2]])
                for a in np.arange(0, TAU, TAU / 6)]
        apex = b + np.array([0.0, 0.0, z1 - b[2]])
        for i in range(6):
            col = shades[(i + t) % len(shades)]
            g.add(face3([ring[i], ring[(i + 1) % 6], apex], col))
    return g


def pyramid3(base_centre, w: float, d: float, h: float,
             lit, dark, front=None) -> VGroup:
    """A four-sided pyramid — a rocket nose, or a pitched roof."""
    c = np.asarray(base_centre, dtype=float)
    hw, hd = w / 2, d / 2
    corners = [c + np.array([-hw, -hd, 0.0]), c + np.array([hw, -hd, 0.0]),
               c + np.array([hw, hd, 0.0]), c + np.array([-hw, hd, 0.0])]
    apex = c + np.array([0.0, 0.0, h])
    cols = [front or lit, dark, lit, dark]
    return VGroup(*[face3([corners[i], corners[(i + 1) % 4], apex], cols[i])
                    for i in range(4)])


def roof3(base_centre, w: float, d: float, h: float, lit, dark) -> VGroup:
    """A pitched roof: two slopes meeting at a ridge, plus the gable ends."""
    c = np.asarray(base_centre, dtype=float)
    hw, hd = w / 2, d / 2
    fl = c + np.array([-hw, -hd, 0.0]); fr = c + np.array([hw, -hd, 0.0])
    bl = c + np.array([-hw, hd, 0.0]);  br = c + np.array([hw, hd, 0.0])
    rf = c + np.array([0.0, -hd, h]);   rb = c + np.array([0.0, hd, h])
    return VGroup(
        face3([fl, fr, rf], dark),            # front gable (the triangle)
        face3([bl, br, rb], dark),            # back gable
        face3([fl, rf, rb, bl], lit),         # left slope
        face3([fr, rf, rb, br], dark),        # right slope
    )


def panel3(centre, w: float, h: float, color, along=RIGHT) -> Polygon:
    """A flat plate standing in space — a solar wing."""
    c = np.asarray(centre, dtype=float)
    a = np.asarray(along, dtype=float)
    u = a / np.linalg.norm(a)
    v = np.array([0.0, 0.0, 1.0])
    return face3([c - u * w / 2 - v * h / 2, c + u * w / 2 - v * h / 2,
                  c + u * w / 2 + v * h / 2, c - u * w / 2 + v * h / 2],
                 color)


# ------------------------------------------------------------- 3D linkages --
def bars3d(pts, color: str = WOOD, diag_opacity: float = 0.0,
           thickness: float = 0.045) -> VGroup:
    """A stick linkage with bolted joints, built from 3D-safe primitives.

    The bracing diagonal is always present so every pose has the same
    submobject structure and Transform can morph between them cleanly; it
    is simply invisible until the brace goes in.
    """
    g = VGroup()
    n = len(pts)
    w = thickness * 240.0                    # cylinder thickness -> stroke
    for i in range(n):
        g.add(line3(pts[i], pts[(i + 1) % n], color, w))
    if n == 4:
        brace = line3(pts[1], pts[3], AMBER, w * 0.85)
        brace.set_stroke(opacity=diag_opacity)
        g.add(brace)
    for p in pts:
        g.add(dot3(p, LEAD, 0.10))
    return g


def quad_pts(origin, w: float, h: float, shear: float, fold: float = 0.0):
    """Four joints of a 4-bar linkage.

    `shear` leans it inside the plane; `fold` then hinges the last joint
    about the p0-p2 diagonal, keeping both bars at their exact lengths
    while taking the figure genuinely out of the plane.
    """
    origin = np.asarray(origin, dtype=float)
    p0 = origin
    p1 = origin + RIGHT * w
    top = np.array([np.sin(shear) * h, np.cos(shear) * h, 0.0])
    p2 = p1 + top
    p3 = p0 + top
    if fold:
        axis = p2 - p0
        u = axis / np.linalg.norm(axis)
        v = p3 - p0
        v_par = np.dot(v, u) * u
        v_perp = v - v_par
        p3 = p0 + v_par + v_perp * np.cos(fold) + np.cross(u, v_perp) * np.sin(fold)
    return [p0, p1, p2, p3]


def ground_plane(centre, w: float = 8.0, d: float = 6.0, step: float = 0.8) -> VGroup:
    """A patch of ground with a grid, for the scenes that stand in space."""
    c = np.asarray(centre, dtype=float)
    slab = Rectangle(width=w, height=d, fill_color=GROUND, fill_opacity=0.88,
                     stroke_width=0).move_to(c)
    grid = VGroup()
    for x in np.arange(-w / 2, w / 2 + 1e-6, step):
        grid.add(Line(c + np.array([x, -d / 2, 0.0]),
                      c + np.array([x, d / 2, 0.0]),
                      stroke_color=GROUND_HI, stroke_width=1.6,
                      stroke_opacity=0.55))
    for y in np.arange(-d / 2, d / 2 + 1e-6, step):
        grid.add(Line(c + np.array([-w / 2, y, 0.0]),
                      c + np.array([w / 2, y, 0.0]),
                      stroke_color=GROUND_HI, stroke_width=1.6,
                      stroke_opacity=0.55))
    return VGroup(slab, grid)


def arc_between_3d(centre, p_from, p_to, radius: float, color: str,
                   n: int = 48) -> VMobject:
    """An angle arc in the plane of two 3D rays (manim's Angle is 2D)."""
    centre = np.asarray(centre, dtype=float)
    u = (np.asarray(p_from, float) - centre)
    u = u / np.linalg.norm(u)
    w = (np.asarray(p_to, float) - centre)
    w = w / np.linalg.norm(w)
    nv = w - np.dot(w, u) * u
    nv = nv / np.linalg.norm(nv)
    span = float(np.arccos(np.clip(np.dot(u, w), -1.0, 1.0)))
    pts = [centre + radius * (np.cos(t) * u + np.sin(t) * nv)
           for t in np.linspace(0.0, span, n)]
    m = VMobject(stroke_color=color, stroke_width=5)
    m.set_points_as_corners(pts)
    return m


# --------------------------------------------------------- everyday things --
def tree(base, h: float = 3.0, spread: float = 1.15) -> VGroup:
    """A leafy tree — the thing you cannot climb."""
    b = np.asarray(base, dtype=float)
    trunk = Polygon(b + np.array([-0.16, 0.0, 0.0]),
                    b + np.array([0.16, 0.0, 0.0]),
                    b + np.array([0.10, h * 0.55, 0.0]),
                    b + np.array([-0.10, h * 0.55, 0.0]),
                    fill_color=WOOD, fill_opacity=1,
                    stroke_color=WOOD_DARK, stroke_width=2)
    crown = VGroup(*[
        Circle(radius=spread * s, fill_color=c, fill_opacity=1,
               stroke_width=0).move_to(b + np.array([dx, h * dy, 0.0]))
        for s, dx, dy, c in ((0.58, -0.42, 0.66, "#2F7D3A"),
                             (0.62, 0.42, 0.68, "#2F7D3A"),
                             (0.70, 0.00, 0.86, "#3B9A47"),
                             (0.50, -0.10, 0.60, "#276B32"))
    ])
    return VGroup(trunk, crown)


def river(centre, w: float = 4.6, h: float = 1.5) -> VGroup:
    c = np.asarray(centre, dtype=float)
    water = Rectangle(width=w, height=h, fill_color="#12507E", fill_opacity=1,
                      stroke_width=0).move_to(c)
    ripples = VGroup(*[
        Line(c + np.array([x, y, 0.0]), c + np.array([x + 0.5, y, 0.0]),
             stroke_color="#59A6DE", stroke_width=3, stroke_opacity=0.7)
        for x, y in ((-1.6, 0.35), (0.2, 0.10), (-0.7, -0.35),
                     (1.3, -0.20), (0.9, 0.45))
    ])
    return VGroup(water, ripples)


def boat(centre, scale: float = 1.0) -> VGroup:
    c = np.asarray(centre, dtype=float)
    hull = Polygon(c + np.array([-0.42, 0.0, 0.0]) * scale,
                   c + np.array([0.42, 0.0, 0.0]) * scale,
                   c + np.array([0.30, -0.18, 0.0]) * scale,
                   c + np.array([-0.30, -0.18, 0.0]) * scale,
                   fill_color="#C2410C", fill_opacity=1, stroke_width=0)
    mast = Line(c, c + UP * 0.52 * scale, stroke_color="#E7E5E4",
                stroke_width=3)
    sail = Polygon(c + np.array([0.03, 0.50, 0.0]) * scale,
                   c + np.array([0.03, 0.06, 0.0]) * scale,
                   c + np.array([0.38, 0.10, 0.0]) * scale,
                   fill_color="#F8FAFC", fill_opacity=0.96, stroke_width=0)
    return VGroup(hull, mast, sail)


def tape_measure(p1, p2, color: str = AMBER) -> VGroup:
    """A tape stretched between two points, with tick marks."""
    p1, p2 = np.asarray(p1, float), np.asarray(p2, float)
    body = Line(p1, p2, stroke_color=color, stroke_width=7)
    v = p2 - p1
    L = float(np.linalg.norm(v))
    u = v / max(L, 1e-6)
    n = np.array([-u[1], u[0], 0.0])
    ticks = VGroup(*[
        Line(p1 + u * t, p1 + u * t + n * 0.11, stroke_color=color,
             stroke_width=3)
        for t in np.arange(0.14, L, 0.24)
    ])
    return VGroup(body, ticks)


def cross_mark(centre, size: float = 0.30, color: str = ROSE) -> VGroup:
    c = np.asarray(centre, dtype=float)
    return VGroup(
        Line(c + np.array([-size, -size, 0.0]), c + np.array([size, size, 0.0]),
             stroke_color=color, stroke_width=9),
        Line(c + np.array([-size, size, 0.0]), c + np.array([size, -size, 0.0]),
             stroke_color=color, stroke_width=9),
    )


def tick_mark(centre, size: float = 0.26, color: str = SUCCESS) -> VGroup:
    c = np.asarray(centre, dtype=float)
    return VGroup(
        Line(c + np.array([-size, 0.05, 0.0]),
             c + np.array([-size * 0.25, -size * 0.65, 0.0]),
             stroke_color=color, stroke_width=9),
        Line(c + np.array([-size * 0.25, -size * 0.65, 0.0]),
             c + np.array([size, size * 0.75, 0.0]),
             stroke_color=color, stroke_width=9),
    )

"""Shared constants, narration, and art for the quadrilateral lesson.

TG Board Class 8 Mathematics — 3.2.3 Construction of a quadrilateral from
three sides and two diagonals (S.S.S.D.D).
Worked figure: ABCD with AB = 4.5, BC = 5.2, CD = 4.8, AC = 5, BD = 5.4.

Three rules this lesson follows:
  * On screen, mathematics is written in mathematics.  Lengths, corners and
    conditions appear as AB, |AC|, /_ABC, 5 = 8 - 3 -- never as English
    sentences.  The words live in the narration.
  * The construction is a real construction: real compass arcs, drawn at
    the exact solved coordinates, never eyeballed.
  * One beat leaves the plane entirely.  A quadrilateral's floppiness is a
    three-dimensional fact, so it is shown in three dimensions.
"""
from __future__ import annotations

import sys
import os
import numpy as np
from manim import (
    ORIGIN, UP, DOWN, LEFT, RIGHT, IN, OUT, DL, UL, UR, DR,
    PI, TAU, DEGREES,
    MathTex, Tex, VGroup, VMobject, Polygon, Line, Arc, Dot, DashedLine, Angle,
    RightAngle, Rectangle, Square, Circle, Ellipse, Sector, Star,
    SurroundingRectangle, RoundedRectangle, BraceBetweenPoints, Brace,
    Line3D, Prism, Cube, Surface, ThreeDAxes, Sphere, Dot3D, ThreeDScene,
    FadeIn, FadeOut, Write, Create, Uncreate, Indicate, DrawBorderThenFill,
    ReplacementTransform, Transform, TransformMatchingTex, TransformFromCopy,
    GrowFromCenter, GrowFromEdge, GrowArrow, SpinInFromNothing, ShrinkToCenter,
    Flash, Wiggle, ShowPassingFlash, Circumscribe, FocusOn, ApplyWave,
    LaggedStart, Succession, AnimationGroup, MoveAlongPath, Rotate, Rotating,
    ValueTracker, DecimalNumber, always_redraw, TracedPath, SpiralIn,
    Arrow, Vector, CurvedArrow, Text, LineJointType,
    rate_functions, config,
)
from manim_voiceover import VoiceoverScene

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lesson_kit import (
    BG, INK, MUTED, ACCENT, SUCCESS, AMBER, ROSE, VIOLET, PANEL,
    txt, heading, punch, card, rule_line, overview_panel,
    blueprint_grid, FRAME_W, FRAME_H, END_HOLD, FONT,
)
from speech_service import get_speech_service
from sound_effects import load_all as load_sfx

VOICEOVER_CACHE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "media", "voiceovers",
)

# edge-tts rate per beat, tuned by tune_all.py so the spoken length matches
# the animation length authored in each scene (video-first workflow).
BEAT_RATE = {
    # One pace for the whole lesson: every beat's narration was written to
    # the length of the animation it rides on, so every rate lands here.
    "intro": "+9%", "title": "+6%",
    "family": "+9%", "typesa": "+9%", "typesb": "+9%", "tree": "+9%",
    "rigid": "+9%", "data": "+9%",
    "count": "+9%", "choose": "+9%", "sss": "+9%", "construct": "+9%",
    "locate": "+9%", "verify": "+9%", "summary": "+9%", "overview": "+9%",
}


def scene_speech_service(beat: str):
    return get_speech_service(cache_dir=VOICEOVER_CACHE_DIR, rate=BEAT_RATE[beat])


NARRATION = {
    "intro": (
        "Look around this room. A window. A kite. Tiles. A field. "
        "Every one of them is four corners joined by four straight sides. "
        "That is a quadrilateral: A, B, C, D. "
        "But four sides hide something a triangle does not. "
        "And that hidden thing changes everything."
    ),
    "title": (
        "Constructing a quadrilateral, from three sides and two diagonals."
    ),
    "family": (
        "Before we build one, let us meet the whole family. "
        "Six four-sided shapes, lifted off the page so you can walk around them. "
        "A square. A rectangle. A parallelogram. "
        "A rhombus. A trapezium. And a kite. "
        "Every one of them has four corners, four sides and two diagonals. "
        "Turn them any way you like: the four angals inside "
        "always add to three hundred and sixty degrees. "
        "What separates them is only this. "
        "Which sides are equal, and which sides are parallel."
    ),
    "typesa": (
        "Start with the strictest one. "
        "A square: all four sides equal, and all four corners right angals. "
        "Now relax the sides but keep the corners, "
        "and you get a rectangle: opposite sides equal, every angal still ninety. "
        "Now let the corners tilt. "
        "The rectangle leans over into a parallelogram: "
        "opposite sides still equal, still parallel, opposite angals still equal, "
        "but not one right angal left."
    ),
    "typesb": (
        "Now the other branch. "
        "A rhombus: all four sides equal, like a square pushed over, "
        "and its two diagonals still cross at right angals. "
        "Loosen it further. "
        "A trapezium keeps just one pair of parallel sides. "
        "The other two go their own way. "
        "And a kite gives up parallel sides altogether, "
        "keeping two pairs of equal neighbours instead."
    ),
    "tree": (
        "So these are not six separate shapes. They are one family. "
        "A square is a rectangle, and it is also a rhombus. "
        "Every rectangle and every rhombus is a parallelogram. "
        "Every parallelogram is a trapezium. "
        "And every one of them is a quadrilateral. "
        "Climbing down this tree, you are only adding conditions. "
        "Which is exactly what our construction does: "
        "five measurements, and one shape is pinned down."
    ),
    "rigid": (
        "Here is the hidden thing. "
        "Join three sticks into a triangle. "
        "Push it as hard as you like. It will not move. "
        "Now join four sticks into a quadrilateral. "
        "The same four lengths, and it leans, it collapses, "
        "it folds out of the page. "
        "Four sides cannot fix a shape. "
        "That is why every roof truss and gate has a diagonal across it."
    ),
    "data": (
        "So the quadrilateral must be pinned down, and here is how. "
        "Three sides: A B, B C and C D. "
        "Then two diagonals: A C and B D. "
        "Notice what is missing. "
        "Side A D is never given. "
        "Five numbers, and only five."
    ),
    "count": (
        "Why five? Count the freedom. "
        "Four corners, two coordinates each, is eight numbers. "
        "But sliding the shape, or turning it, changes nothing, "
        "and that costs three. "
        "Eight minus three leaves five. "
        "Five is exactly what a quadrilateral needs. "
        "Not four, not six. Five."
    ),
    "choose": (
        "So where do we start? "
        "A compass can only build a triangle when all three lengths are in hand. "
        "Look at A B C. "
        "A B given, B C given, and A C given as a diagonal. "
        "Three out of three. "
        "Now look at A B D. "
        "A B given, B D given, but A D was never given. "
        "A compass cannot guess it."
    ),
    "sss": (
        "Why do three lengths settle a triangle? "
        "Put the base down. "
        "The third corner sits five from A, on this circle. "
        "It also sits five point two from B, on this one. "
        "Two circles meet in two points, mirror images. "
        "Pick the one above the line, and the triangle is fixed."
    ),
    "construct": (
        "So build it. "
        "First the base: A B, four point five, laid down along the ruler. "
        "Now open the compass to five, put the needle on A, "
        "and swing an arc. "
        "Open it to five point two, needle on B, and swing again. "
        "Where the two arcs cross is C, "
        "and the first triangle is finished."
    ),
    "locate": (
        "Two numbers are still unused: the diagonal B D, and the side C D. "
        "Swing an arc of five point four from B. "
        "Then swing four point eight from C. "
        "They cross on the far side of A C, and that crossing is the corner D. "
        "Join it up, and the quadrilateral is finished."
    ),
    "verify": (
        "Now check against the five given numbers. "
        "A B, four point five. B C, five point two. C D, four point eight. "
        "Diagonal A C, five. Diagonal B D, five point four. "
        "All five agree. A D falls out at one point one two."
    ),
    "summary": (
        "Five measured lengths pin a quadrilateral down. "
        "Find the triangle you already have, and build outward from there."
    ),
    "overview": (
        "So, the whole method. "
        "One: check you have five measurements. "
        "Two: find a triangle whose three lengths are given. "
        "Three: draw it with ruler and compass. "
        "Four: fix the last corner from the two left. "
        "Five: check every given length on the figure."
    ),
}

# ---------------------------------------------------------------- geometry --
# The real construction, solved exactly from the given lengths, never
# eyeballed:
#   A = (0, 0), B = (4.5, 0)                      [AB = 4.5]
#   C solves AC = 5, BC = 5.2                     -> (2.023, 4.572)
#   D solves BD = 5.4, CD = 4.8                   -> (-0.851, 0.727)
# then scaled and re-centred so the figure sits inside the frame.
AB, BC, CD, AC, BD = 4.5, 5.2, 4.8, 5.0, 5.4

SCALE = 0.78                              # cm of the question -> scene units
SHIFT = np.array([-0.15, -0.55, 0.0])     # centres the figure in frame


def _solve() -> tuple:
    a = np.array([0.0, 0.0, 0.0])
    b = np.array([AB, 0.0, 0.0])
    # C: |AC| = 5 from A, |BC| = 5.2 from B, above AB
    cx = (AC ** 2 - BC ** 2 + AB ** 2) / (2 * AB)
    cy = np.sqrt(AC ** 2 - cx ** 2)
    c = np.array([cx, cy, 0.0])
    # D: |BD| = 5.4 from B, |CD| = 4.8 from C, on the far side of AC from B
    bc_vec = c - b
    dist = float(np.linalg.norm(bc_vec))
    t = (BD ** 2 - CD ** 2 + dist ** 2) / (2 * dist)
    hgt = np.sqrt(BD ** 2 - t ** 2)
    unit = bc_vec / dist
    perp = np.array([-unit[1], unit[0], 0.0])
    d1 = b + unit * t + perp * hgt
    d2 = b + unit * t - perp * hgt
    d = d1 if d1[0] < d2[0] else d2
    return a, b, c, d


_A, _B, _C, _D = _solve()
_CENTRE = (_A + _B + _C + _D) / 4.0
A, B, C, D = [(p - _CENTRE) * SCALE + SHIFT for p in (_A, _B, _C, _D)]
AD = float(np.linalg.norm(_D - _A))       # 4.10..., the length nobody gave us

# ------------------------------------------------------------------ palette --
PAPER_TOP = "#0B1220"
PAPER_BOTTOM = "#101B2E"
WOOD = "#8A5A2B"
WOOD_DARK = "#6B451F"
GLASS = "#1E3A5F"
LEAD = "#94A3B8"


def mtx(s: str, size: int = 36, color: str = INK) -> MathTex:
    """All on-screen mathematics goes through here."""
    return MathTex(s, font_size=size, color=color)


def paper_backdrop() -> VGroup:
    """A soft drafting-paper wash with a faint grid."""
    sheet = Rectangle(width=FRAME_W, height=FRAME_H, stroke_width=0)
    sheet.set_fill(color=[PAPER_TOP, PAPER_BOTTOM], opacity=1)
    return VGroup(sheet, blueprint_grid(1.0, ACCENT, 0.06))


# ------------------------------------------------------- everyday four-gons --
def window_frame(centre, w=2.2, h=2.8) -> VGroup:
    """A four-pane window: the quadrilateral everyone has already seen."""
    c = np.asarray(centre, dtype=float)
    outer = Rectangle(width=w, height=h, fill_color=WOOD, fill_opacity=1,
                      stroke_color=WOOD_DARK, stroke_width=4).move_to(c)
    panes = VGroup()
    pw, ph = (w - 0.30) / 2, (h - 0.30) / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            pane = Rectangle(width=pw - 0.10, height=ph - 0.10,
                             fill_color=GLASS, fill_opacity=1,
                             stroke_color=WOOD_DARK, stroke_width=2)
            pane.move_to(c + np.array([sx * (pw + 0.10) / 2,
                                       sy * (ph + 0.10) / 2, 0.0]))
            panes.add(pane)
    glint = Line(c + np.array([-w * 0.30, h * 0.10, 0.0]),
                 c + np.array([-w * 0.10, h * 0.34, 0.0]),
                 stroke_color="#BFDBFE", stroke_width=3, stroke_opacity=0.55)
    return VGroup(outer, panes, glint)


def kite_shape(centre, w=1.9, h=2.6) -> VGroup:
    """A paper kite — a quadrilateral with two pairs of equal sides."""
    c = np.asarray(centre, dtype=float)
    top = c + np.array([0.0, h * 0.55, 0.0])
    bot = c + np.array([0.0, -h * 0.45, 0.0])
    lft = c + np.array([-w / 2, h * 0.12, 0.0])
    rgt = c + np.array([w / 2, h * 0.12, 0.0])
    body = Polygon(top, rgt, bot, lft, fill_color=ROSE, fill_opacity=0.75,
                   stroke_color="#FDA4AF", stroke_width=3)
    spine = VGroup(
        Line(top, bot, stroke_color="#FECDD3", stroke_width=2,
             stroke_opacity=0.8),
        Line(lft, rgt, stroke_color="#FECDD3", stroke_width=2,
             stroke_opacity=0.8),
    )
    tail = VMobject(stroke_color="#FDA4AF", stroke_width=3)
    tail.set_points_smoothly([
        bot,
        bot + np.array([0.30, -0.45, 0.0]),
        bot + np.array([-0.22, -0.90, 0.0]),
        bot + np.array([0.26, -1.35, 0.0]),
    ])
    return VGroup(body, spine, tail)


def tile_floor(centre, cols=4, rows=3, size=0.60) -> VGroup:
    """A patch of floor tiles in honest one-point perspective.

    Rows recede upward: each row is narrower and shorter than the one below
    it, and the tiles share grout lines instead of floating apart.
    """
    c = np.asarray(centre, dtype=float)
    W = cols * size
    depth = rows * size

    def pt(i, j):
        """Grid corner (i across, j back) mapped into the receding quad."""
        t = j / rows
        shrink = 1.0 - 0.26 * t                      # far edge is narrower
        x = (i / cols - 0.5) * W * shrink
        y = -depth / 2 + depth * (t ** 0.86)         # rows bunch up with depth
        return np.array([x, y, 0.0])

    tiles = VGroup()
    for j in range(rows):
        for i in range(cols):
            shade = "#274C74" if (i + j) % 2 == 0 else "#16304E"
            tiles.add(Polygon(pt(i, j), pt(i + 1, j), pt(i + 1, j + 1),
                              pt(i, j + 1),
                              fill_color=shade, fill_opacity=1,
                              stroke_color="#0C1A2B", stroke_width=2))
    edge = Polygon(pt(0, 0), pt(cols, 0), pt(cols, rows), pt(0, rows),
                   stroke_color="#4E7CA8", stroke_width=3, fill_opacity=0)
    g = VGroup(tiles, edge)
    g.move_to(c)
    return g


def field_plot(centre, w=2.6, h=1.7) -> VGroup:
    """A surveyed field: four corner posts, a fenced boundary, ploughed rows."""
    c = np.asarray(centre, dtype=float)
    p = [c + np.array(v) for v in (
        [-w / 2, -h / 2, 0.0], [w / 2, -h * 0.36, 0.0],
        [w * 0.34, h / 2, 0.0], [-w * 0.44, h * 0.30, 0.0],
    )]
    plot = Polygon(*p, fill_color="#1E4429", fill_opacity=1,
                   stroke_color=SUCCESS, stroke_width=3)
    furrows = VGroup(*[
        Line(p[0] + (p[3] - p[0]) * f, p[1] + (p[2] - p[1]) * f,
             stroke_color="#2F6B3D", stroke_width=2, stroke_opacity=0.85)
        for f in (0.22, 0.44, 0.66, 0.88)
    ])
    # corner posts — what a surveyor actually plants
    posts = VGroup(*[
        VGroup(Line(q, q + UP * 0.20, stroke_color="#C8B08A", stroke_width=3),
               Dot(q + UP * 0.20, radius=0.045, color="#E7C873"))
        for q in p
    ])
    return VGroup(plot, furrows, posts)


# ------------------------------------------------------- construction tools --
def compass(centre, radius: float, angle: float, color: str = ACCENT,
            scale: float = 1.0) -> VGroup:
    """A drafting compass actually set to `radius`, standing on `centre`.

    The needle leg ends exactly on `centre`, the pencil leg ends exactly on
    the arc at `angle`, and the hinge sits at the apex of the two equal legs.
    Because the needle is the pivot, `Rotate(comp, sweep, about_point=centre)`
    sweeps the pencil along the arc the way a real compass does.
    """
    centre = np.asarray(centre, dtype=float)
    r = float(radius)
    span = r / 2.0
    # Just long enough to span the radius: any longer and the apex towers
    # over the drawing instead of leaning across it.
    leg = span * 1.45
    needle_pt = centre
    pencil_pt = centre + r * np.array([np.cos(angle), np.sin(angle), 0.0])

    mid = (needle_pt + pencil_pt) / 2.0
    d = (pencil_pt - needle_pt) / max(r, 1e-6)
    n = np.array([-d[1], d[0], 0.0])
    if n[1] < 0:
        n = -n                                        # hinge above the chord
    hinge = mid + n * float(np.sqrt(max(leg ** 2 - span ** 2, 0.04)))

    w = 0.055 * scale
    leg_n = Line(hinge, needle_pt, stroke_color=color, stroke_width=4.5 * scale)
    leg_p = Line(hinge, pencil_pt, stroke_color=color, stroke_width=4.5 * scale)
    crossbar = Line(leg_n.point_from_proportion(0.62),
                    leg_p.point_from_proportion(0.62),
                    stroke_color=color, stroke_width=2 * scale,
                    stroke_opacity=0.50)

    # the sharp steel point that pins the paper
    u_n = (needle_pt - hinge) / max(float(np.linalg.norm(needle_pt - hinge)), 1e-6)
    perp_n = np.array([-u_n[1], u_n[0], 0.0])
    needle = Polygon(needle_pt,
                     needle_pt - u_n * 0.26 * scale + perp_n * w,
                     needle_pt - u_n * 0.26 * scale - perp_n * w,
                     fill_color=LEAD, fill_opacity=1, stroke_width=0)
    # steel collar, so the needle leg reads as metal
    collar = Line(needle_pt - u_n * 0.26 * scale, needle_pt - u_n * 0.66 * scale,
                  stroke_color=LEAD, stroke_width=7 * scale)

    # the lead, at the far end of the other leg
    u_p = (pencil_pt - hinge) / max(float(np.linalg.norm(pencil_pt - hinge)), 1e-6)
    perp_p = np.array([-u_p[1], u_p[0], 0.0])
    lead = Polygon(pencil_pt,
                   pencil_pt - u_p * 0.26 * scale + perp_p * w * 1.15,
                   pencil_pt - u_p * 0.26 * scale - perp_p * w * 1.15,
                   fill_color=AMBER, fill_opacity=1, stroke_width=0)
    # the wooden pencil clamped to the other leg
    barrel = Line(pencil_pt - u_p * 0.26 * scale, pencil_pt - u_p * 0.92 * scale,
                  stroke_color="#E7C873", stroke_width=10 * scale)
    ferrule = Line(pencil_pt - u_p * 0.92 * scale, pencil_pt - u_p * 1.06 * scale,
                   stroke_color=LEAD, stroke_width=10 * scale)

    # knurled grip above the hinge, so it reads as a tool you hold
    grip_dir = (hinge - mid) / max(float(np.linalg.norm(hinge - mid)), 1e-6)
    grip = Line(hinge, hinge + grip_dir * 0.46 * scale,
                stroke_color=color, stroke_width=7 * scale)
    knob = Dot(hinge + grip_dir * 0.46 * scale, radius=0.085 * scale,
               color=color)
    pivot = Dot(hinge, radius=0.055 * scale, color=LEAD)

    return VGroup(leg_n, leg_p, crossbar, grip, knob, pivot,
                  collar, needle, barrel, ferrule, lead)


def compass_icon(center=ORIGIN, scale: float = 1.0, color: str = ACCENT) -> VGroup:
    """Decorative compass for the title card (no radius to honour)."""
    return compass(np.asarray(center, dtype=float) + DOWN * 1.05 * scale,
                   1.05 * scale, 108 * DEGREES, color, scale)


def ruler(p1, p2, width: float = 0.34) -> VGroup:
    """A straight-edge lying along p1->p2, with tick marks."""
    p1, p2 = np.asarray(p1, dtype=float), np.asarray(p2, dtype=float)
    v = p2 - p1
    length = float(np.linalg.norm(v))
    angle = float(np.arctan2(v[1], v[0]))
    mid = (p1 + p2) / 2
    body = Rectangle(width=length + 0.5, height=width, fill_color="#E7C873",
                     fill_opacity=0.92, stroke_color="#B08A3E", stroke_width=2)
    ticks = VGroup(*[
        Line(np.array([x, width / 2, 0.0]),
             np.array([x, width / 2 - (0.13 if i % 5 else 0.20), 0.0]),
             stroke_color="#7C5E22", stroke_width=1.6)
        for i, x in enumerate(np.arange(-(length + 0.5) / 2 + 0.12,
                                        (length + 0.5) / 2, 0.28))
    ])
    g = VGroup(body, ticks)
    g.move_to(mid + np.array([0.0, 0.0, 0.0]))
    g.rotate(angle, about_point=mid)
    return g


def arc_from(centre, radius: float, p_target, sweep=70 * DEGREES,
             color: str = AMBER, width: float = 3.5) -> Arc:
    """A compass arc centred on `centre`, sweeping across `p_target`."""
    centre = np.asarray(centre, dtype=float)
    p_target = np.asarray(p_target, dtype=float)
    mid = float(np.arctan2(*(p_target - centre)[1::-1]))
    return Arc(radius=radius, start_angle=mid - sweep / 2, angle=sweep,
               arc_center=centre, stroke_color=color, stroke_width=width)


def full_circle(centre, radius: float, color: str = AMBER,
                width: float = 3.0, opacity: float = 0.9) -> Circle:
    return Circle(radius=radius, arc_center=np.asarray(centre, dtype=float),
                  stroke_color=color, stroke_width=width,
                  stroke_opacity=opacity)


def vertex(point, label: str, direction=UP, color: str = INK,
           size: int = 32) -> VGroup:
    """A construction point with its letter, set clear of the figure."""
    dot = Dot(np.asarray(point, dtype=float), color=color, radius=0.070)
    lbl = mtx(label, size, color).next_to(dot, direction, buff=0.18)
    return VGroup(dot, lbl)


def side_label(p1, p2, text: str, color: str = INK, size: int = 28,
               out=None, buff: float = 0.30) -> MathTex:
    """A length written alongside a segment, pushed off it perpendicularly."""
    p1, p2 = np.asarray(p1, dtype=float), np.asarray(p2, dtype=float)
    mid = (p1 + p2) / 2
    v = p2 - p1
    n = np.array([-v[1], v[0], 0.0])
    n = n / max(float(np.linalg.norm(n)), 1e-6)
    if out is not None and float(np.dot(n, np.asarray(out, dtype=float))) < 0:
        n = -n
    return mtx(text, size, color).move_to(mid + n * buff)


def stick(p1, p2, color: str = WOOD, width: float = 0.16) -> VGroup:
    """A wooden bar with a bolt at each end — a linkage, not a line."""
    p1, p2 = np.asarray(p1, dtype=float), np.asarray(p2, dtype=float)
    v = p2 - p1
    length = max(float(np.linalg.norm(v)), 1e-3)
    mid = (p1 + p2) / 2
    bar = Rectangle(width=length, height=width, fill_color=color,
                    fill_opacity=1, stroke_color=WOOD_DARK, stroke_width=1.5)
    bar.move_to(mid).rotate(float(np.arctan2(v[1], v[0])), about_point=mid)
    b1 = Dot(p1, radius=width * 0.62, color=LEAD)
    b2 = Dot(p2, radius=width * 0.62, color=LEAD)
    return VGroup(bar, b1, b2)


# ============================================================================
#  THE QUADRILATERAL FAMILY, IN THREE DIMENSIONS
# ============================================================================
# The lesson opens by meeting all six four-sided shapes before constructing
# one.  They are shown as thin solid plates lying on a drafting table rather
# than as flat outlines, because the camera can then walk around them: the
# same six shapes seen from three angles are far harder to confuse with each
# other than six line drawings stacked on a page.
#
# Every plate is built from an exact vertex list -- a rhombus really has four
# equal sides, a parallelogram's opposite sides really are parallel -- so the
# tick marks and chevrons drawn on top are claims the geometry can honour.

TEAL = "#2DD4BF"          # the sixth accent, for the kite
PLATE_DEPTH = 0.20        # how thick a plate stands off the table


def _centre(pts) -> list:
    """Re-centre a vertex list on the origin, as 3D points."""
    arr = np.array([[p[0], p[1], 0.0] for p in pts], dtype=float)
    return [p for p in (arr - arr.mean(axis=0))]


# Vertex lists, counter-clockwise, each about 2.3 units across.
FAMILY_PTS = {
    "square": _centre([(-0.90, -0.90), (0.90, -0.90), (0.90, 0.90), (-0.90, 0.90)]),
    "rectangle": _centre([(-1.20, -0.72), (1.20, -0.72), (1.20, 0.72), (-1.20, 0.72)]),
    "parallelogram": _centre([(-1.05, -0.75), (1.05, -0.75),
                              (1.67, 0.75), (-0.43, 0.75)]),
    "rhombus": _centre([(1.18, 0.0), (0.0, 0.86), (-1.18, 0.0), (0.0, -0.86)]),
    "trapezium": _centre([(-1.28, -0.75), (1.28, -0.75),
                          (0.68, 0.75), (-0.68, 0.75)]),
    "kite": _centre([(0.0, 1.24), (-0.86, 0.14), (0.0, -1.16), (0.86, 0.14)]),
}

FAMILY_COLOR = {
    "square": ACCENT, "rectangle": SUCCESS, "parallelogram": AMBER,
    "rhombus": ROSE, "trapezium": VIOLET, "kite": TEAL,
}

FAMILY_NAME = {
    "square": "Square", "rectangle": "Rectangle",
    "parallelogram": "Parallelogram", "rhombus": "Rhombus",
    "trapezium": "Trapezium", "kite": "Kite",
}

# The defining condition of each shape, written in mathematics.  a, b, c, d
# are the four sides in order; the angle symbol means every corner.
FAMILY_RULE = {
    "square": r"a\!=\!b\!=\!c\!=\!d,\;\; \angle = 90^\circ",
    "rectangle": r"a\!=\!c,\; b\!=\!d,\;\; \angle = 90^\circ",
    "parallelogram": r"a \parallel c,\; b \parallel d,\;\; a\!=\!c,\; b\!=\!d",
    "rhombus": r"a\!=\!b\!=\!c\!=\!d,\;\; d_1 \perp d_2",
    "trapezium": r"a \parallel c",
    "kite": r"a\!=\!d,\;\; b\!=\!c",
}

FAMILY_ORDER = ["square", "rectangle", "parallelogram",
                "rhombus", "trapezium", "kite"]


def _dim(color: str, amount: float) -> str:
    """Darken a palette colour toward the paper, for the unlit faces."""
    from manim import ManimColor, interpolate_color
    return interpolate_color(ManimColor(color), ManimColor(PAPER_TOP),
                             amount).to_hex()


def plate(pts, color: str = ACCENT, depth: float = PLATE_DEPTH,
          opacity: float = 0.95, stroke: str = INK) -> VGroup:
    """A flat polygon extruded into a solid slab standing on the table.

    Returned face by face -- bottom, then the sides in order, then the top --
    so `plate(...)[-1]` is always the lit top face that a mark sits on.
    """
    pts = [np.asarray(p, dtype=float) for p in pts]
    lift = OUT * (depth / 2.0)
    top = [p + lift for p in pts]
    bot = [p - lift for p in pts]

    faces = VGroup()
    faces.add(Polygon(*bot, fill_color=_dim(color, 0.65), fill_opacity=opacity,
                      stroke_width=0))
    n = len(pts)
    for i in range(n):
        j = (i + 1) % n
        faces.add(Polygon(bot[i], bot[j], top[j], top[i],
                          fill_color=_dim(color, 0.38), fill_opacity=opacity,
                          stroke_color=_dim(color, 0.55), stroke_width=1.5))
    faces.add(Polygon(*top, fill_color=color, fill_opacity=opacity,
                      stroke_color=stroke, stroke_width=3.5))
    return faces


def plate_top(pts, depth: float = PLATE_DEPTH) -> list:
    """The vertices of a plate's top face -- where marks and labels belong."""
    return [np.asarray(p, dtype=float) + OUT * (depth / 2.0) for p in pts]


def shifted(pts, offset) -> list:
    """A vertex list moved bodily to a new place on the table."""
    off = np.asarray(offset, dtype=float)
    return [np.asarray(p, dtype=float) + off for p in pts]


def table_top(w: float = 15.5, h: float = 9.5) -> VGroup:
    """The drafting table the plates lie on: a dark sheet plus a faint grid.

    Drawn in the xy-plane at z = 0, so a tilted camera reads it as a surface
    receding away rather than as a flat backdrop.
    """
    sheet = Rectangle(width=w, height=h, stroke_width=0)
    sheet.set_fill(color=PAPER_BOTTOM, opacity=1)
    lines = VGroup()
    for x in np.arange(-w / 2, w / 2 + 0.01, 1.0):
        lines.add(Line(np.array([x, -h / 2, 0.0]), np.array([x, h / 2, 0.0]),
                       stroke_color=ACCENT, stroke_width=1, stroke_opacity=0.10))
    for y in np.arange(-h / 2, h / 2 + 0.01, 1.0):
        lines.add(Line(np.array([-w / 2, y, 0.0]), np.array([w / 2, y, 0.0]),
                       stroke_color=ACCENT, stroke_width=1, stroke_opacity=0.10))
    return VGroup(sheet, lines)


def placard(mob, at, lift: float = 0.0):
    """Stand a flat mobject upright at `at`, facing the default camera.

    A caption lying in the table plane is squashed to nothing once the camera
    tilts; standing it in the xz-plane keeps it readable while it still
    travels with the shape it names.
    """
    at = np.asarray(at, dtype=float)
    mob.rotate(90 * DEGREES, axis=RIGHT)
    mob.move_to(at + OUT * lift)
    return mob


# --------------------------------------------------------- geometry marks --
def _unit(v):
    return v / max(float(np.linalg.norm(v)), 1e-9)


def ticks(p1, p2, count: int = 1, color: str = INK, size: float = 0.15,
          gap: float = 0.13, width: float = 4.0) -> VGroup:
    """Equal-length tick marks across the middle of a segment.

    One tick, two ticks, three ticks: the ordinary schoolbook notation for
    "these sides are the same length", and the only way to say it on screen
    without writing an English sentence there.
    """
    p1, p2 = np.asarray(p1, dtype=float), np.asarray(p2, dtype=float)
    u = _unit(p2 - p1)
    nrm = np.array([-u[1], u[0], 0.0])
    mid = (p1 + p2) / 2.0
    g = VGroup()
    for k in range(count):
        base = mid + u * ((k - (count - 1) / 2.0) * gap)
        g.add(Line(base - nrm * size, base + nrm * size,
                   stroke_color=color, stroke_width=width))
    return g


def chevrons(p1, p2, count: int = 1, color: str = ACCENT, size: float = 0.17,
             gap: float = 0.19, width: float = 4.0) -> VGroup:
    """Arrow-heads along a segment: the notation for "parallel to"."""
    p1, p2 = np.asarray(p1, dtype=float), np.asarray(p2, dtype=float)
    u = _unit(p2 - p1)
    nrm = np.array([-u[1], u[0], 0.0])
    mid = (p1 + p2) / 2.0
    g = VGroup()
    for k in range(count):
        tip = mid + u * ((k - (count - 1) / 2.0) * gap + gap / 2)
        g.add(Line(tip, tip - u * size + nrm * size,
                   stroke_color=color, stroke_width=width),
              Line(tip, tip - u * size - nrm * size,
                   stroke_color=color, stroke_width=width))
    return g


def corner_mark(v, a, b, size: float = 0.24, color: str = INK,
                width: float = 3.5) -> VGroup:
    """The little square that says the corner at `v` is a right angle."""
    v, a, b = (np.asarray(x, dtype=float) for x in (v, a, b))
    ua, ub = _unit(a - v) * size, _unit(b - v) * size
    return VGroup(Line(v + ua, v + ua + ub, stroke_color=color,
                       stroke_width=width),
                  Line(v + ub, v + ua + ub, stroke_color=color,
                       stroke_width=width))


def side_letters(pts, letters=("a", "b", "c", "d"), color: str = INK,
                 size: int = 28, buff: float = 0.42, upright: bool = False,
                 lift: float = 0.0) -> VGroup:
    """The side names a, b, c, d, set just outside each edge.

    The conditions on screen are written in terms of a, b, c and d, so the
    figure has to say which side is which -- an unlabelled figure asks the
    viewer to guess, and guessing is the one thing a construction lesson
    cannot afford.  Every vertex list here runs counter-clockwise, so the
    right-hand normal of an edge points out of the shape.
    """
    p = [np.asarray(q, dtype=float) for q in pts]
    g = VGroup()
    for i, ch in enumerate(letters):
        a, b = p[i], p[(i + 1) % len(p)]
        v = b - a
        out = np.array([v[1], -v[0], 0.0])
        out = out / max(float(np.linalg.norm(out)), 1e-9)
        m = mtx(ch, size, color)
        m.move_to((a + b) / 2.0 + out * buff + OUT * lift)
        if upright:
            m.rotate(90 * DEGREES, axis=RIGHT, about_point=m.get_center())
        g.add(m)
    return g


def corner_letters(pts, letters=("A", "B", "C", "D"), color: str = INK,
                   size: int = 30, buff: float = 0.42, upright: bool = False,
                   lift: float = 0.0) -> VGroup:
    """The corner names A, B, C, D, pushed outward away from the centre."""
    p = [np.asarray(q, dtype=float) for q in pts]
    centre = sum(p) / len(p)
    g = VGroup()
    for q, ch in zip(p, letters):
        out = q - centre
        out[2] = 0.0
        out = out / max(float(np.linalg.norm(out)), 1e-9)
        m = mtx(ch, size, color)
        m.move_to(q + out * buff + OUT * lift)
        if upright:
            m.rotate(90 * DEGREES, axis=RIGHT, about_point=m.get_center())
        g.add(m)
    return g


def angle_arc(v, a, b, radius: float = 0.42, color: str = ROSE,
              width: float = 4.0) -> Arc:
    """The arc of the angle at `v` between the rays to `a` and `b`.

    Built from the two directions directly, rather than with `Angle`, so it
    stays in the plane of the points it is given -- which for these lessons
    is the lit top face of a plate, not the table underneath it.
    """
    v, a, b = (np.asarray(x, dtype=float) for x in (v, a, b))
    t1 = float(np.arctan2(*(a - v)[1::-1]))
    t2 = float(np.arctan2(*(b - v)[1::-1]))
    sweep = (t2 - t1 + PI) % TAU - PI
    return Arc(radius=radius, start_angle=t1, angle=sweep, arc_center=v,
               stroke_color=color, stroke_width=width)


def diagonals(pts, color: str = MUTED, width: float = 3.0,
              dash: bool = True) -> VGroup:
    """Both diagonals of a quadrilateral, in the plane of the given points."""
    p = [np.asarray(q, dtype=float) for q in pts]
    make = DashedLine if dash else Line
    return VGroup(make(p[0], p[2], stroke_color=color, stroke_width=width),
                  make(p[1], p[3], stroke_color=color, stroke_width=width))


# ------------------------------------------------------------ crisp 3D ----
# manim CE's cairo renderer draws Surface-based solids (Sphere, Prism,
# Line3D, Dot3D) as hundreds of small flat-shaded quads, which comes out
# banded and soft — it looks blurred beside the crisp 2D scenes.  Flat
# VMobject polygons with set_shade_in_3d(True) project as real vectors, so
# they stay razor sharp at any camera angle and still depth-sort.

def line3(p1, p2, color=INK, width: float = 8.0, opacity: float = 1.0):
    """A crisp 3D line — a vector, not a shaded cylinder."""
    m = Line(np.asarray(p1, float), np.asarray(p2, float),
             stroke_color=color, stroke_width=width, stroke_opacity=opacity)
    m.set_shade_in_3d(True)
    return m


def dot3(point, color=AMBER, r: float = 0.085):
    m = Dot(np.asarray(point, float), color=color, radius=r)
    m.set_shade_in_3d(True)
    return m


def face3(pts, color, opacity: float = 1.0, stroke: float = 1.0):
    """One flat face in space."""
    m = Polygon(*[np.asarray(p, float) for p in pts],
                fill_color=color, fill_opacity=opacity,
                stroke_color=color, stroke_width=stroke,
                joint_type=LineJointType.BEVEL)
    m.set_shade_in_3d(True)
    return m


def box3(centre, dx: float, dy: float, dz: float, top, lit, dark):
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

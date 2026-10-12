"""Shared constants, narration, and art for the trigonometry lesson.

Heights and Distances — the angle of elevation.
Worked example: theta = 60 deg at d = 15 m  =>  h = 15*sqrt(3) ~= 25.98 m.

Two rules this lesson follows:
  * On screen, mathematics is written in mathematics.  Sides, angles and
    ratios appear as h, d, theta, tan(theta) -- never as the English words
    "opposite" / "adjacent" / "hypotenuse".  Words live in the narration.
  * The diagram is a scene, not a sketch: a real figure stands on real
    ground and looks up at a real tower, and one beat leaves the plane
    entirely to show the triangle standing in space.
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
    Line3D, Prism, Cube, Surface, ThreeDAxes, Sphere, Dot3D,
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
from human_figure import Man, STANDING, POINTING_UP, LOOKING_UP, WALK_A, WALK_B

VOICEOVER_CACHE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "media", "voiceovers",
)

# edge-tts rate per beat, tuned by tune_all.py so the spoken length matches
# the animation length authored in each scene (video-first workflow).
BEAT_RATE = {
    "intro": "-1%", "title": "+4%", "hook": "+9%", "triangle": "-2%",
    "space": "+9%", "ratio": "+4%", "similar": "+5%", "formal": "+9%",
    "working": "+9%", "example": "+9%", "summary": "+9%", "overview": "+9%",
}


def scene_speech_service(beat: str):
    return get_speech_service(cache_dir=VOICEOVER_CACHE_DIR, rate=BEAT_RATE[beat])


NARRATION = {
    "intro": (
        "Look up at a mountain. "
        "Look up at a tower. "
        "Look out at a ship on the sea. "
        "Now try to measure any one of them with a tape. "
        "You cannot. They are all out of reach. "
        "And yet we know their heights, down to the metre. "
        "Trigonometry is how. "
        "It trades climbing, for one angle."
    ),
    "title": (
        "Heights and distances. From one angle, a height."
    ),
    "hook": (
        "A tower, and a man standing on the ground. "
        "He wants its height, h. "
        "So he walks a measured distance out from the foot. "
        "He stops, and looks up at the very top. "
        "The distance along the ground he can measure. Call it d. "
        "The height h, he cannot reach."
    ),
    "triangle": (
        "Look at what his line of sight makes. "
        "From the foot of the tower, straight up, is h. "
        "Along the ground to his feet is d. "
        "From his eye to the top runs the third side. "
        "A right angle sits where the tower meets the ground. "
        "Theta is the angle he tilts his eyes through."
    ),
    "space": (
        "And this triangle is not a drawing on paper. "
        "It is standing in real space, on real ground. "
        "Turn the whole arrangement around and look from anywhere you like — "
        "nothing about it changes. "
        "Only when we look from exactly side on "
        "does it flatten into the neat picture we draw in our notebooks. "
        "The triangle on paper was always the shadow of a real one."
    ),
    "ratio": (
        "Now hold d fixed, and change theta instead. "
        "As theta opens up, the top of the triangle climbs, "
        "and h climbs with it. "
        "But keep your eye on the ratio, h over d. "
        "Pick any theta, and that ratio settles on one fixed number, "
        "whatever size you draw the triangle. "
        "A number that useful deserves a name. "
        "We call it tan theta."
    ),
    "similar": (
        "Here is why it is fixed. Stand closer. Stand further away. "
        "Same theta, a different triangle each time. "
        "But those triangles are similar, so every side scales together, "
        "and h over d does not move. "
        "Tan theta depends on theta alone."
    ),
    "formal": (
        "So tan theta equals h over d. "
        "We want h on its own, so multiply both sides by d. "
        "That d cancels the one underneath, and h stands alone. "
        "Read it the other way: h equals d tan theta. "
        "Everything on the right, you can measure from the ground."
    ),
    "working": (
        "Now put in real numbers. "
        "He walks fifteen metres out from the foot, so d is fifteen. "
        "He measures the angle at sixty degrees, so theta is sixty. "
        "h is the one thing we do not know. "
        "Drop them in: tan sixty equals h over fifteen."
    ),
    "example": (
        "Tan of sixty degrees is a value we know by heart: "
        "root three, about one point seven three two. "
        "So root three equals h over fifteen. "
        "Multiply across, and h is fifteen root three — "
        "about twenty five point nine eight metres. "
        "He is one point seven metres tall. "
        "That tower is about fifteen of him, stacked up."
    ),
    "summary": (
        "One angle. One distance. One ratio. "
        "And a height nobody had to climb for."
    ),
    "overview": (
        "So, the whole method. "
        "Set up the right triangle: h up, d along the ground, "
        "theta at the eye. "
        "Tan theta is h over d. "
        "Rearranged, h equals d tan theta. "
        "Measure the distance, measure the angle, and the height is yours."
    ),
}

# ------------------------------------------------------------- geometry ----
# The elevation diagram, sized so the angle at the observer is a true
# 60 degrees (h_visual / d_visual = tan 60 = sqrt(3)) and the triangle sits
# in the left half of the frame, leaving the right half for the algebra.
FOOT = np.array([-4.30, -2.10, 0.0])
H_VIS = 3.60
TOP = FOOT + UP * H_VIS
OBS = FOOT + RIGHT * (H_VIS / np.sqrt(3.0))
GROUND_Y = float(FOOT[1])

DIST_M = 15.0
ANGLE_DEG = 60.0
HEIGHT_M = DIST_M * np.sqrt(3.0)      # 25.980...

MAN_H = 0.95                           # figure height in scene units

SKY_TOP = "#0A1128"
SKY_BOTTOM = "#3B4B78"
GROUND_COLOR = "#16231A"
GROUND_HILITE = "#2B3D2A"
TOWER_BODY = "#37414F"
WINDOW = "#FDE68A"


def mtx(s: str, size: int = 36, color: str = INK) -> MathTex:
    """All on-screen mathematics goes through here."""
    return MathTex(s, font_size=size, color=color)


def sky_ground_backdrop(ground_y: float = GROUND_Y) -> VGroup:
    """Dusk sky over ground, full frame."""
    sky = Rectangle(width=FRAME_W, height=FRAME_H, stroke_width=0)
    sky.set_fill(color=[SKY_TOP, SKY_BOTTOM], opacity=1)
    sky.move_to(ORIGIN)
    gh = FRAME_H / 2 + ground_y
    ground = Rectangle(width=FRAME_W, height=gh, fill_color=GROUND_COLOR,
                       fill_opacity=1, stroke_width=0)
    ground.move_to(np.array([0.0, ground_y - gh / 2, 0.0]))
    horizon = Line(np.array([-FRAME_W / 2, ground_y, 0.0]),
                   np.array([FRAME_W / 2, ground_y, 0.0]),
                   stroke_color=GROUND_HILITE, stroke_width=2)
    return VGroup(sky, ground, horizon)


def realistic_tower(foot=FOOT, top=TOP, width: float = 0.86) -> VGroup:
    """Layered building silhouette with a lit window grid and an antenna."""
    h = float(np.linalg.norm(np.asarray(top) - np.asarray(foot)))
    centre = (np.asarray(foot) + np.asarray(top)) / 2
    body = Rectangle(width=width, height=h, fill_color=TOWER_BODY,
                     fill_opacity=1, stroke_color="#1F2937",
                     stroke_width=2).move_to(centre)
    shade = Rectangle(width=width * 0.38, height=h, fill_color="#1F2937",
                      fill_opacity=0.38, stroke_width=0)
    shade.move_to(body.get_left() + RIGHT * width * 0.19)
    windows = VGroup()
    rows = max(3, int(h // 0.46))
    for r in range(rows):
        wy = -h / 2 + 0.30 + r * ((h - 0.62) / max(rows - 1, 1))
        for wx in (-width * 0.23, width * 0.23):
            windows.add(Square(side_length=0.11, fill_color=WINDOW,
                               fill_opacity=0.88, stroke_width=0)
                        .move_to(centre + np.array([wx, wy, 0.0])))
    roof = Rectangle(width=width * 1.16, height=0.10, fill_color="#1F2937",
                     fill_opacity=1, stroke_width=0).move_to(np.asarray(top) + UP * 0.05)
    antenna = Line(np.asarray(top) + UP * 0.1, np.asarray(top) + UP * 0.52,
                   stroke_color="#9CA3AF", stroke_width=2)
    return VGroup(body, shade, windows, roof, antenna)


def elevation_angle(color: str = SUCCESS, radius: float = 0.62,
                    obs=None, foot=None, top=None) -> Angle:
    """The angle of elevation at the observer.

    `other_angle=True` because manim's default sweep between these two
    lines is the 300-degree reflex angle, which draws as a near-full circle.
    """
    obs = OBS if obs is None else obs
    foot = FOOT if foot is None else foot
    top = TOP if top is None else top
    return Angle(Line(obs, foot), Line(obs, top), radius=radius,
                 color=color, stroke_width=4, other_angle=True)


def right_angle_at_foot(size: float = 0.34) -> RightAngle:
    return RightAngle(Line(FOOT, OBS), Line(FOOT, TOP), length=size,
                      color=MUTED, stroke_width=3)


# ------------------------------------------------------- intro-beat art ----
def mountain(base_centre, width: float = 4.2, height: float = 2.6) -> VGroup:
    """A peak with a snow cap — something you cannot put a tape on."""
    b = np.asarray(base_centre, dtype=float)
    left = b + LEFT * width / 2
    right = b + RIGHT * width / 2
    peak = b + UP * height
    rock = Polygon(left, right, peak, fill_color="#3A4657", fill_opacity=1,
                   stroke_color="#5A6779", stroke_width=2)
    snow_y = height * 0.62
    snow_l = left + (peak - left) * (snow_y / height)
    snow_r = right + (peak - right) * (snow_y / height)
    snow = Polygon(snow_l, peak, snow_r,
                   fill_color="#E8EEF6", fill_opacity=1, stroke_width=0)
    ridge = Line(peak, b + DOWN * 0.02 + LEFT * width * 0.06,
                 stroke_color="#2B3542", stroke_width=2)
    return VGroup(rock, snow, ridge)


def ship(centre, scale: float = 1.0) -> VGroup:
    """A small boat — something you cannot walk a tape out to."""
    c = np.asarray(centre, dtype=float)
    hull = Polygon(c + np.array([-0.42, 0.0, 0.0]) * scale,
                   c + np.array([0.42, 0.0, 0.0]) * scale,
                   c + np.array([0.30, -0.16, 0.0]) * scale,
                   c + np.array([-0.30, -0.16, 0.0]) * scale,
                   fill_color="#B45309", fill_opacity=1, stroke_width=0)
    mast = Line(c, c + UP * 0.46 * scale, stroke_color="#D6D3D1", stroke_width=3)
    sail = Polygon(c + np.array([0.02, 0.44, 0.0]) * scale,
                   c + np.array([0.02, 0.05, 0.0]) * scale,
                   c + np.array([0.34, 0.09, 0.0]) * scale,
                   fill_color="#F1F5F9", fill_opacity=0.95, stroke_width=0)
    return VGroup(hull, mast, sail)


def star_field(n: int = 26, seed: int = 7, y_min: float = 0.4) -> VGroup:
    rng = np.random.default_rng(seed)
    stars = VGroup()
    for _ in range(n):
        x = rng.uniform(-FRAME_W / 2 + 0.4, FRAME_W / 2 - 0.4)
        y = rng.uniform(y_min, FRAME_H / 2 - 0.3)
        r = rng.uniform(0.014, 0.032)
        stars.add(Dot(np.array([x, y, 0.0]), radius=r, color="#E2E8F0")
                  .set_opacity(float(rng.uniform(0.45, 1.0))))
    return stars


def tape_measure(start, end, color: str = ROSE) -> VGroup:
    """A tape that will be shown failing to reach."""
    s, e = np.asarray(start, dtype=float), np.asarray(end, dtype=float)
    body = RoundedRectangle(corner_radius=0.06, width=0.44, height=0.30,
                            fill_color="#EAB308", fill_opacity=1,
                            stroke_color="#854D0E", stroke_width=2).move_to(s)
    band = Line(s, e, stroke_color=color, stroke_width=5)
    return VGroup(band, body)


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

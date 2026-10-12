"""
Boats and Streams Problems — When the River Changes Your Speed
Story-mode chalkboard lesson (Telangana Class 8 Maths, Chapter 2:
Linear Equations in One Variable, boat / stream problems).

Core idea: the river is moving too. Downstream the boat and the current point
the same way, so the speeds combine (x + s); upstream they oppose, so the
current takes speed away (x - s). Because the two journeys cover the SAME
fixed distance A-B, the two distance expressions must be equal -- and that is
where the equation comes from.

The current arrows never change direction: only the boat turns around.

Production pipeline (mirrors the rest of the Story-Mode series):
  - shared assets/background2.png chalkboard + student/teacher cutouts +
    dhimantAI (top-left) and Mathematics (top-right) corner badges.
  - VoiceoverScene + speech service; narration written as natural prose.
  - synced_voice.install_synced_voiceover() re-times every word against the
    real audio.
  - real per-line SRT export (carry-safe timestamps).
  - sound effects from sound_effects.py, chalk-styled Text/MathTex.
  - story_common.play_challenge_countdown() for the "YOUR TURN" clock.

Title + 10 beats:
  0. Title card -- the river in miniature.
  1. A Boat on a River -- out fast, back slow, 5 h and 6 h.
  2. Downstream -- boat + current arrows add: x + 2.
  3. Upstream -- boat against the current: x - 2.
  4. Speed x Time -- 5(x+2) and 6(x-2).
  5. Same Distance -- 5(x+2) = 6(x-2).
  6. Solve -- x = 22 km/h.
  7. Check -- 120 = 120.
  8. The Strategy -- direction, speed, distance.
  9. Student Challenge -- s = 3, 4 h / 6 h -> x = 15.
 10. Summary + the Thank-You template.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
_ROOT = next(p for p in _HERE.parents
        if (p / "speech_service.py").exists())
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from manim import (
    ORIGIN, UP, DOWN, LEFT, RIGHT, PI, TAU, BLACK,
    ImageMobject, MathTex, VGroup, VMobject, Line, DashedLine, Circle,
    Rectangle, RoundedRectangle, Polygon, Triangle, Arc, Arrow, DoubleArrow,
    Text, Write, FadeIn, FadeOut, Create, ReplacementTransform,
    TransformMatchingTex, TransformFromCopy, GrowArrow, Indicate, Flash,
    Circumscribe, SurroundingRectangle, MoveAlongPath, ArcBetweenPoints, config,
)
from manim_voiceover import VoiceoverScene
from manim_voiceover.tracker import AUDIO_OFFSET_RESOLUTION

from speech_service import get_speech_service
from sound_effects import load_all as load_sfx
from story_common import play_challenge_countdown
from synced_voice import install_synced_voiceover

# --------------------------------------------------------------- theme -----
CHALK_WHITE = "#F5F2E9"
BRAND_WHITE = "#FFFFFF"
CHALK_YELLOW = "#FFE066"
CHALK_PINK = "#FF8FA3"
CHALK_CYAN = "#7FE7DC"
CHALK_AMBER = "#E8B769"
CHALK_GREEN = "#9BE38A"
CHALK_RED = "#FF6B6B"
FONT = "Segoe Print"
MATH_COLOR = CHALK_WHITE

BOAT_COLOR = CHALK_CYAN       # the boat's own speed keeps one colour
STREAM_COLOR = CHALK_PINK     # the current keeps another
DOWN_COLOR = CHALK_GREEN
UP_COLOR = CHALK_AMBER

END_HOLD = 2.0
TRANSITION_HOLD = 0.35
MIN_RT = 0.12

# measured chalkboard safe bounds (shared across the series)
BOARD_LEFT = -4.6
BOARD_RIGHT = 5.6
BOARD_TOP = 3.3
BOARD_BOTTOM = -2.9
BOARD_CX = (BOARD_LEFT + BOARD_RIGHT) / 2   # 0.5
BOARD_CY = (BOARD_TOP + BOARD_BOTTOM) / 2   # 0.2

EQ_Y = 1.5          # main equation line
HEAD_Y = BOARD_TOP - 0.45
RIVER_CY = -1.55    # the reminder river strip at the bottom of a beat


def rt(seconds: float, floor: float = MIN_RT) -> float:
    return max(floor, float(seconds))


def board_text(s: str, size: int = 34, color: str = CHALK_WHITE,
               weight: str = "NORMAL") -> Text:
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def chalk_math(s: str, size: int = 34, color: str = MATH_COLOR) -> MathTex:
    return MathTex(s, font_size=size, color=color)


def align_equals(eq: MathTex, cx: float = BOARD_CX, cy: float = EQ_Y) -> MathTex:
    """Centre the whole equation line on the board."""
    eq.move_to(np.array([cx, cy, 0.0]))
    return eq


def check_mark(color: str = CHALK_GREEN, size: float = 0.4,
               width: float = 5) -> VGroup:
    a = np.array([-0.52, 0.16, 0.0]) * size
    b = np.array([-0.16, -0.30, 0.0]) * size
    c = np.array([0.52, 0.40, 0.0]) * size
    return VGroup(Line(a, b, color=color, stroke_width=width),
                  Line(b, c, color=color, stroke_width=width))


def tick_beside(target, color: str = CHALK_GREEN, size: float = 0.4,
                buff: float = 0.3) -> VGroup:
    mark = check_mark(color, size)
    mark.next_to(target, RIGHT, buff=buff)
    mark.shift(UP * (target.get_center()[1] - mark.get_center()[1]))
    return mark


def drop_shadow(mobj: VGroup, dx: float = 0.045, dy: float = -0.05,
                opacity: float = 0.3) -> VGroup:
    shadow = mobj.copy()
    shadow.set_fill(BLACK, opacity=opacity)
    shadow.set_stroke(width=0)
    shadow.shift(np.array([dx, dy, 0]))
    return VGroup(shadow, mobj)


# ------------------------------------------------------------ river kit -----
# Realistic-but-simple chalk scenery, drawn entirely from Manim primitives:
# a layered river with a wavy surface, grassy banks, a proper little boat with
# a curved hull and a wake, and villages with houses, windows, a jetty and a
# signpost at each end of the route.
def tree_icon(pos: np.ndarray, scale: float = 1.0) -> VGroup:
    """A chalk tree anchored at its base: trunk + three-tone foliage."""
    trunk = Rectangle(width=0.07, height=0.26, fill_color="#5A3B1E",
                      fill_opacity=1, stroke_width=0).move_to(UP * 0.13)
    fol_low = Circle(0.18, fill_color="#2E7D46", fill_opacity=0.95,
                     stroke_color=CHALK_GREEN, stroke_width=1.3).move_to(UP * 0.35)
    fol_mid = Circle(0.135, fill_color="#3B9A5B", fill_opacity=0.95,
                     stroke_color=CHALK_GREEN, stroke_width=1.1).move_to(
        UP * 0.40 + RIGHT * 0.1)
    fol_top = Circle(0.09, fill_color="#4FB06C", fill_opacity=0.95,
                     stroke_color=CHALK_GREEN, stroke_width=0.9).move_to(
        UP * 0.47 + LEFT * 0.06)
    tree = VGroup(trunk, fol_low, fol_mid, fol_top)
    return tree.scale(scale).move_to(np.array([pos[0], pos[1] + 0.26 * scale / 2, 0]))


def grass_tuft(pos: np.ndarray, color: str = CHALK_GREEN,
               height: float = 0.1) -> VGroup:
    """Three short blades fanning from one point."""
    blades = VGroup(*[
        Line(ORIGIN, height * np.array([np.sin(a), np.cos(a), 0]),
             stroke_color=color, stroke_width=1.2)
        for a in (-0.5, 0.0, 0.5)
    ])
    return blades.move_to(pos)


def wavy_line(cx: float, cy: float, half_w: float, amp: float = 0.03,
              cycles: float = 3.0, color: str = CHALK_CYAN,
              width: float = 1.6, opacity: float = 1.0) -> "VMobject":
    """A smooth sine ripple -- how chalk water actually looks."""
    vm = VMobject(stroke_color=color, stroke_width=width,
                  stroke_opacity=opacity)
    pts = [np.array([x, amp * np.sin(cycles * TAU * x / (2 * half_w)), 0])
           for x in np.linspace(-half_w, half_w, 60)]
    vm.set_points_smoothly(pts)
    return vm.move_to(np.array([cx, cy, 0]))


def boat_icon(scale: float = 1.0, facing: int = 1) -> VGroup:
    """A little chalk boat. `facing` is +1 pointing right (downstream) and
    -1 pointing left (upstream); the hull profile is mirrored accordingly."""
    f = facing
    hull = Polygon(
        np.array([-0.42 * f, 0.02, 0]), np.array([0.30 * f, 0.02, 0]),
        np.array([0.44 * f, 0.10, 0]),                    # raised bow
        np.array([0.30 * f, -0.13, 0]), np.array([0.0, -0.18, 0]),
        np.array([-0.30 * f, -0.13, 0]),
        stroke_color=BOAT_COLOR, stroke_width=2.3,
        fill_color="#1B3A4A", fill_opacity=0.95)
    deck = Line(np.array([-0.36 * f, 0.02, 0]), np.array([0.34 * f, 0.02, 0]),
                stroke_color=CHALK_WHITE, stroke_width=1.2, stroke_opacity=0.7)
    cabin = RoundedRectangle(corner_radius=0.02, width=0.24, height=0.15,
                             stroke_color=BOAT_COLOR, stroke_width=1.7,
                             fill_color="#204A5E", fill_opacity=0.95).move_to(
        np.array([-0.16 * f, 0.10, 0]))
    window = Rectangle(width=0.07, height=0.06, stroke_color=CHALK_CYAN,
                       stroke_width=1.0, fill_color="#7FE7DC",
                       fill_opacity=0.5).move_to(cabin.get_center())
    mast = Line(np.array([0.06 * f, 0.02, 0]), np.array([0.06 * f, 0.42, 0]),
                stroke_color=CHALK_WHITE, stroke_width=1.8)
    # a sail with a slight belly, leaning with the boat
    sail_pts = [np.array([0.06 * f, 0.40, 0]),
                np.array([0.26 * f, 0.24, 0]),
                np.array([0.20 * f, 0.05, 0]),
                np.array([0.06 * f, 0.06, 0])]
    sail = VMobject(stroke_color=CHALK_WHITE, stroke_width=1.6,
                    fill_color="#2E6E86", fill_opacity=0.9)
    sail.set_points_smoothly(sail_pts)
    flag = Polygon(np.array([0.06 * f, 0.42, 0]),
                   np.array([0.06 * f + 0.14 * f, 0.37, 0]),
                   np.array([0.06 * f, 0.32, 0]),
                   stroke_width=0, fill_color=CHALK_YELLOW, fill_opacity=0.95)
    hull_lbl = hull
    boat = VGroup(hull, deck, cabin, window, mast, sail, flag)
    boat.hull = hull_lbl
    return boat.scale(scale)


def boat_wake(boat: VGroup, facing: int = 1, color: str = CHALK_CYAN) -> VGroup:
    """Two short ripples trailing behind the hull."""
    c = boat.get_center()
    arcs = VGroup(*[
        Arc(radius=0.16 + 0.09 * k, start_angle=-0.9 if facing > 0 else 2.25,
            angle=1.5, stroke_color=color, stroke_width=1.4,
            stroke_opacity=0.7 - 0.15 * k).move_to(
            c + np.array([-0.5 * facing - 0.12 * k * facing, -0.16, 0]))
        for k in range(2)
    ])
    return arcs


def current_arrow(length: float = 0.55, color: str = STREAM_COLOR,
                  bow: float = 0.05) -> VGroup:
    """A slightly curved flow arrow, so the current reads as moving water."""
    path = ArcBetweenPoints(ORIGIN, np.array([length, 0, 0]), angle=bow)
    head = Triangle(stroke_width=0, fill_color=color, fill_opacity=1
                    ).scale(0.055).rotate(-PI / 2).move_to(
        np.array([length, 0, 0]))
    return VGroup(path.set_stroke(color=color, width=2.0), head)


def river_band(width: float = 9.0, cx: float = BOARD_CX, cy: float = RIVER_CY,
               height: float = 0.85, n_arrows: int = 6,
               banks: bool = True) -> VGroup:
    """A chalk river: layered water, wavy surface, grassy banks and drifting
    current arrows. `band.arrows` is the flowing group (animated as one) and
    `band.bank_top` / `band.bank_bottom` are the land lines villages stand on."""
    deep = Rectangle(width=width, height=height, stroke_width=0,
                     fill_color="#0E2E38", fill_opacity=0.85)
    shallow = Rectangle(width=width, height=height * 0.5, stroke_width=0,
                        fill_color="#17495A", fill_opacity=0.9).move_to(
        UP * height * 0.25)
    water = VGroup(deep, shallow)
    surface = wavy_line(0, height * 0.48, width / 2, amp=height * 0.035,
                        cycles=width / 2.2, color=CHALK_CYAN, width=1.8)
    # the boundary between deep and shallow water is a soft wave too
    mid_wave = wavy_line(0, 0, width / 2, amp=height * 0.03,
                         cycles=width / 3.1, color=CHALK_CYAN, width=1.2,
                         opacity=0.45)
    ripples = VGroup(*[
        wavy_line(x, y, 0.45, amp=height * 0.028, cycles=1.5,
                  color=CHALK_CYAN, width=1.0, opacity=0.5)
        for x, y in ((-width * 0.3, height * 0.1), (width * 0.05, -height * 0.2),
                     (width * 0.33, height * 0.14))
    ])
    band = VGroup(water, mid_wave, surface, ripples).move_to(np.array([cx, cy, 0]))

    bank_h = 0.2
    top_y = cy + height / 2            # land line at the top of the water
    bot_y = cy - height / 2            # land line at the bottom of the water
    if banks:
        for sign in (1, -1):
            edge_y = top_y if sign > 0 else bot_y
            strip = Rectangle(width=width, height=bank_h, stroke_width=0,
                              fill_color="#1E3B22", fill_opacity=0.85)
            strip.move_to(np.array([cx, edge_y + sign * bank_h / 2, 0]))
            edge = Line(np.array([cx - width / 2, edge_y, 0]),
                        np.array([cx + width / 2, edge_y, 0]),
                        stroke_color=CHALK_GREEN, stroke_width=1.8)
            tufts = VGroup(*[
                grass_tuft(np.array([cx + x, edge_y + sign * bank_h * 0.6, 0]),
                           height=0.07)
                for x in np.linspace(-width / 2 + 0.45, width / 2 - 0.45,
                                     max(4, int(width / 1.25)))
            ])
            band.add(strip, edge, tufts)

    arrows = VGroup()
    xs = np.linspace(-width / 2 + 0.7, width / 2 - 1.0, n_arrows)
    for k, x in enumerate(xs):
        yy = height * 0.2 if k % 2 == 0 else -height * 0.2
        arrows.add(current_arrow(0.46, bow=0.05 * (1 if k % 2 == 0 else -1)).move_to(
            np.array([x, yy, 0])))
    arrows.move_to(band.get_center())
    band.add(arrows)
    band.arrows = arrows
    band.land_top = np.array([0.0, top_y + bank_h, 0.0])
    band.land_bottom = np.array([0.0, bot_y - bank_h, 0.0])
    return band


def town_marker(letter: str, x: float, base_y: float,
                scale: float = 0.85, facing: int = 1) -> VGroup:
    """A little village that STANDS ON THE BANK: everything is built with its
    base at the origin and then shifted so `base_y` is the land line, so the
    houses never sit in the water. A short jetty is the only part that dips
    into the river. `facing` puts the jetty on the river side."""
    body = Rectangle(width=0.42, height=0.3, stroke_color=CHALK_AMBER,
                     stroke_width=1.8, fill_color="#4A3520", fill_opacity=0.95
                     ).move_to(np.array([0.12, 0.15, 0]))
    roof = Polygon(np.array([-0.11, 0.30, 0]), np.array([0.35, 0.30, 0]),
                   np.array([0.12, 0.52, 0]),
                   stroke_color=CHALK_AMBER, stroke_width=1.8,
                   fill_color="#6B4424", fill_opacity=0.98)
    chimney = Rectangle(width=0.06, height=0.12, stroke_width=0,
                        fill_color="#3A2A16", fill_opacity=0.95).move_to(
        np.array([0.28, 0.44, 0]))
    door = Rectangle(width=0.09, height=0.15, stroke_width=0,
                     fill_color="#22150B", fill_opacity=0.95).move_to(
        np.array([0.02, 0.075, 0]))
    window = VGroup(
        Rectangle(width=0.1, height=0.1, stroke_color=CHALK_YELLOW,
                  stroke_width=1, fill_color="#FFE066", fill_opacity=0.5
                  ).move_to(np.array([0.25, 0.16, 0])),
        Line(np.array([0.25, 0.11, 0]), np.array([0.25, 0.21, 0]),
             stroke_color=CHALK_YELLOW, stroke_width=0.8),
        Line(np.array([0.20, 0.16, 0]), np.array([0.30, 0.16, 0]),
             stroke_color=CHALK_YELLOW, stroke_width=0.8),
    )
    house = VGroup(body, roof, chimney, door, window)

    post = Line(np.array([-0.26, 0.0, 0]), np.array([-0.26, 0.3, 0]),
                stroke_color=CHALK_AMBER, stroke_width=2.2)
    board = RoundedRectangle(corner_radius=0.03, width=0.24, height=0.19,
                             stroke_color=CHALK_AMBER, stroke_width=1.8,
                             fill_color="#2A1D10", fill_opacity=0.95).move_to(
        np.array([-0.26, 0.39, 0]))
    letter_m = MathTex(letter, font_size=22, color=CHALK_YELLOW).move_to(
        board.get_center())
    sign = VGroup(post, board, letter_m)

    tree = tree_icon(np.array([0.62, 0.0, 0]), scale=0.62)

    # only the jetty reaches down into the water
    jetty = VGroup(
        Line(np.array([0.30 * facing, -0.04, 0]), np.array([0.72 * facing, -0.04, 0]),
             stroke_color="#6B4424", stroke_width=2.6),
        Line(np.array([0.70 * facing, -0.04, 0]), np.array([0.70 * facing, -0.18, 0]),
             stroke_color="#6B4424", stroke_width=1.8),
    )
    village = VGroup(house, sign, tree, jetty).scale(scale)
    village.shift(np.array([x, base_y, 0]))
    return village


def clock_badge(time_text: str, color: str = CHALK_YELLOW,
                scale: float = 1.0) -> VGroup:
    """A small chalk clock with the journey time next to it."""
    face = Circle(radius=0.28, stroke_color=color, stroke_width=2,
                  fill_color="#1B2430", fill_opacity=0.85)
    hands = VGroup(
        Line(face.get_center(), face.get_center() + UP * 0.15,
             stroke_color=color, stroke_width=1.8),
        Line(face.get_center(), face.get_center() + RIGHT * 0.19,
             stroke_color=color, stroke_width=1.8),
    )
    tick_marks = VGroup(*[
        Line(face.get_center() + 0.23 * np.array([np.sin(a), np.cos(a), 0]),
             face.get_center() + 0.28 * np.array([np.sin(a), np.cos(a), 0]),
             stroke_color=color, stroke_width=1.4)
        for a in np.linspace(0, TAU, 8, endpoint=False)
    ])
    lbl = board_text(time_text, 15, color, "BOLD").next_to(face, DOWN, buff=0.1)
    return VGroup(face, tick_marks, hands, lbl).scale(scale)


def card(width: float, height: float, color: str) -> RoundedRectangle:
    return RoundedRectangle(corner_radius=0.1, width=width, height=height,
                            stroke_color=color, stroke_width=2,
                            fill_color="#16202B", fill_opacity=0.9)


def summary_row(n: int, label: str, math_tex: str, color: str) -> VGroup:
    badge = Circle(radius=0.19, stroke_color=color, stroke_width=2,
                   fill_color=color, fill_opacity=0.18)
    num = board_text(str(n), 17, color, "BOLD").move_to(badge.get_center())
    return VGroup(VGroup(badge, num),
                  board_text(label, 18, CHALK_WHITE),
                  MathTex(math_tex, font_size=22)).arrange(RIGHT, buff=0.28)


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "Today we solve a puzzle about a boat on a river.<bookmark mark='b0'/> "
        "The same boat, travelling the same distance, can be fast in one "
        "direction and slow in the other.<bookmark mark='b1'/> Let's find out "
        "why!<bookmark mark='b2'/>"
    ),
    "scene1": (
        "Look at this river.<bookmark mark='b0'/> Town A is on the left and town "
        "B is on the right, and the water is flowing towards B.<bookmark "
        "mark='b1'/> Watch the boat travel downstream, with the current."
        "<bookmark mark='b2'/> Now it turns around and comes back upstream, "
        "against the current.<bookmark mark='b3'/> The same boat, and the same "
        "distance, but the return journey takes longer.<bookmark mark='b4'/> Why "
        "are the two journeys so different?<bookmark mark='b5'/> The river is "
        "moving too.<bookmark mark='b6'/>"
    ),
    "scene2": (
        "Let the boat's own speed in still water be x, and the speed of the "
        "stream be two kilometres per hour.<bookmark mark='b0'/> Downstream, the "
        "boat and the current point the same way.<bookmark mark='b1'/> The boat "
        "moves at x, and the water adds its own two.<bookmark mark='b2'/> So the "
        "downstream speed is x plus two.<bookmark mark='b3'/> With the current, "
        "we add.<bookmark mark='b4'/>"
    ),
    "scene3": (
        "Now the boat turns around, but the river keeps flowing the same way."
        "<bookmark mark='b0'/> Upstream, the boat pushes against the current."
        "<bookmark mark='b1'/> The current does not help it; the current takes "
        "speed away.<bookmark mark='b2'/> So the upstream speed is x minus two."
        "<bookmark mark='b3'/> Against the current, we subtract."
        "<bookmark mark='b4'/>"
    ),
    "scene4": (
        "Now let's bring in the times.<bookmark mark='b0'/> The downstream "
        "journey takes five hours, and the upstream journey takes six."
        "<bookmark mark='b1'/> Distance is speed times time.<bookmark mark='b2'/> "
        "Downstream, the distance is five times, x plus two.<bookmark mark='b3'/> "
        "Upstream, the distance is six times, x minus two.<bookmark mark='b4'/>"
    ),
    "scene5": (
        "Here is the key idea.<bookmark mark='b0'/> Both journeys start at one "
        "town and finish at the other.<bookmark mark='b1'/> So the distance is "
        "exactly the same in both directions.<bookmark mark='b2'/> That means "
        "five times, x plus two, must equal six times, x minus two.<bookmark "
        "mark='b3'/> The same distance creates the equation.<bookmark mark='b4'/>"
    ),
    "scene6": (
        "Now we solve it.<bookmark mark='b0'/> Opening the brackets gives five x "
        "plus ten, equals six x minus twelve.<bookmark mark='b1'/> Collecting the "
        "x terms on the right and the numbers on the left gives minus x equals "
        "minus twenty two.<bookmark mark='b2'/> So x equals twenty two."
        "<bookmark mark='b3'/> The boat's speed in still water is twenty two "
        "kilometres per hour.<bookmark mark='b4'/>"
    ),
    "scene7": (
        "Let's check that answer in the story.<bookmark mark='b0'/> Downstream "
        "the speed is twenty two plus two, which is twenty four, and in five "
        "hours the boat covers one hundred and twenty kilometres.<bookmark "
        "mark='b1'/> Upstream the speed is twenty two minus two, which is twenty, "
        "and in six hours the boat also covers one hundred and twenty "
        "kilometres.<bookmark mark='b2'/> Both journeys cover the same distance, "
        "so twenty two is correct.<bookmark mark='b3'/>"
    ),
    "scene8": (
        "Here is the method, in four steps.<bookmark mark='b0'/> First decide the "
        "direction: with the current, or against it.<bookmark mark='b1'/> Then "
        "add the stream speed downstream, and subtract it upstream."
        "<bookmark mark='b2'/> Next, multiply each speed by its own time, to get "
        "the two distances.<bookmark mark='b3'/> And because the route is the "
        "same, set those distances equal, and solve.<bookmark mark='b4'/>"
    ),
    "scene9_setup": (
        "Your turn!<bookmark mark='b0'/> A boat covers the same river distance "
        "downstream in four hours and upstream in six hours, and the stream flows "
        "at three kilometres per hour.<bookmark mark='b1'/> Let the boat's speed "
        "in still water be x.<bookmark mark='b2'/> Pause the video, and try it "
        "yourself.<bookmark mark='b3'/>"
    ),
    "scene9_reveal": (
        "Downstream the effective speed is x plus three, and upstream it is x "
        "minus three.<bookmark mark='b0'/> The distances are equal, so four "
        "times, x plus three, equals six times, x minus three.<bookmark "
        "mark='b1'/> Opening the brackets gives four x plus twelve, equals six x "
        "minus eighteen.<bookmark mark='b2'/> Rearranging gives thirty equals two "
        "x, so x equals fifteen.<bookmark mark='b3'/> The boat's speed in still "
        "water is fifteen kilometres per hour.<bookmark mark='b4'/> Well done — "
        "same distance, same equation.<bookmark mark='b5'/>"
    ),
    "scene10": (
        "Let's summarise.<bookmark mark='b0'/> With the current, add the stream "
        "speed; against the current, subtract it.<bookmark mark='b1'/> Then write "
        "each distance as speed times time.<bookmark mark='b2'/> If both journeys "
        "cover the same route, the two distances are equal.<bookmark mark='b3'/> "
        "Set them equal, solve for x, and check your answer in the story."
        "<bookmark mark='b4'/> The current changes the speed, and the same "
        "distance creates the equation. Thank you so much for watching, and I "
        "will see you in the next lesson!<bookmark mark='b5'/>"
    ),
}


class UpstreamDownstreamStory(VoiceoverScene):
    """Story-mode chalkboard lesson: upstream and downstream problems."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._srt_entries: list[tuple[float, float, str]] = []

    # -- backdrop ----------------------------------------------------------
    def add_background(self) -> None:
        assets_dir = Path(_ROOT) / "Story-Mode-Manim-Videos" / "assets"

        bg = ImageMobject(str(assets_dir / "background2.png"))
        bg.stretch_to_fit_width(config.frame_width)
        bg.stretch_to_fit_height(config.frame_height)
        bg.set_z_index(-10)

        student = ImageMobject(str(assets_dir / "student.png"))
        student.set_z_index(-5)
        student.height = 3.3
        student.move_to(np.array([
            -config.frame_width / 2 + student.width / 2 - 0.15,
            -config.frame_height / 2 + student.height / 2 - 0.1, 0]))

        teacher = ImageMobject(str(assets_dir / "teacher.png"))
        teacher.set_z_index(-5)
        teacher.height = 3.3
        teacher.move_to(np.array([
            config.frame_width / 2 - teacher.width / 2 + 0.45,
            -config.frame_height / 2 + teacher.height / 2 - 0.1, 0]))

        self.bg = bg
        self.student = student
        self.teacher = teacher
        self.badge = self._corner_badge("Mathematics", corner="right",
                                        y=BOARD_TOP - 0.16, font_size=12,
                                        scale=16 / 12)
        self.badge_l = self._corner_badge("dhimantAI", corner="left",
                                          y=BOARD_TOP - 0.16, font_size=12,
                                          scale=16 / 12, text_color=BRAND_WHITE)
        self.add(self.bg, self.student, self.teacher, self.badge, self.badge_l)

    def _corner_badge(self, text: str, *, corner: str, y: float | None = None,
                      font_size: int = 13, scale: float = 1.0,
                      text_color: str = CHALK_WHITE) -> VGroup:
        label = board_text(text, font_size, text_color, "BOLD")
        frame = RoundedRectangle(
            corner_radius=0.04, width=label.width + 0.24,
            height=label.height + 0.16,
            stroke_color=CHALK_AMBER, stroke_width=1.5,
            fill_color="#2A1D10", fill_opacity=0.45)
        label.move_to(frame.get_center())
        badge = VGroup(frame, label).scale(scale)
        yy = BOARD_TOP - 0.32 if y is None else y
        if corner == "left":
            badge.move_to(np.array([BOARD_LEFT + 0.55, yy, 0]))
            badge.shift(RIGHT * (BOARD_LEFT + 0.08 - badge.get_left()[0]))
        else:
            badge.move_to(np.array([BOARD_RIGHT - 0.6, yy, 0]))
            badge.shift(RIGHT * (BOARD_RIGHT - 0.013 - badge.get_right()[0]))
        badge.shift(UP * ((BOARD_TOP - 0.08) - badge.get_top()[1]))
        return badge

    def reset_board(self) -> None:
        self.clear()
        self.add(self.bg, self.student, self.teacher, self.badge, self.badge_l)

    # -- real SRT export ---------------------------------------------------
    def _capture_srt(self, tracker, words_per_line: int = 9) -> None:
        wbs = [wb for wb in tracker.data.get("word_boundaries", [])
               if wb.get("text", "").strip()]
        if not wbs:
            return
        starts = [tracker.start_t + wb["audio_offset"] / AUDIO_OFFSET_RESOLUTION
                  for wb in wbs]
        for i in range(0, len(wbs), words_per_line):
            chunk = wbs[i:i + words_per_line]
            end = starts[i + words_per_line] if i + words_per_line < len(starts) \
                else tracker.end_t
            text = " ".join(wb["text"] for wb in chunk)
            self._srt_entries.append((starts[i], end, text))

    def _write_real_srt(self) -> None:
        out_dir = _HERE / "media" / "videos" / "upstream_downstream_story"
        out_dir.mkdir(parents=True, exist_ok=True)

        def fmt(t: float) -> str:
            total_ms = int(round(max(t, 0.0) * 1000))
            h, rem = divmod(total_ms, 3_600_000)
            m, rem = divmod(rem, 60_000)
            s, ms = divmod(rem, 1000)
            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

        lines = []
        for idx, (start, end, text) in enumerate(self._srt_entries, 1):
            lines.append(str(idx))
            lines.append(f"{fmt(start)} --> {fmt(max(end, start + 0.3))}")
            lines.append(text)
            lines.append("")
        content = "\n".join(lines)
        (out_dir / f"{self.__class__.__name__}.real.srt").write_text(
            content, encoding="utf-8")
        print(f"[real SRT written] {out_dir}")
        (out_dir / "real.srt").write_text(content, encoding="utf-8")
        try:
            if (hasattr(self, "renderer") and hasattr(self.renderer, "file_writer")
                    and self.renderer.file_writer.movie_file_path):
                movie_dir = Path(self.renderer.file_writer.movie_file_path).parent
                (movie_dir / "real.srt").write_text(content, encoding="utf-8")
                (movie_dir / f"{self.__class__.__name__}.real.srt").write_text(
                    content, encoding="utf-8")
        except Exception:
            pass

    def construct(self):
        self.sfx = load_sfx()
        self.set_speech_service(get_speech_service(), create_subcaption=False)
        install_synced_voiceover(self)
        self.add_background()

        self.beat0_title()
        self.beat1_journey()
        self.beat2_downstream()
        self.beat3_upstream()
        self.beat4_distance()
        self.beat5_same()
        self.beat6_solve()
        self.beat7_check()
        self.beat8_strategy()
        self.beat9_challenge()
        self.beat10_summary()

        self._write_real_srt()

    # ================================================================ beats ==

    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Boats and Streams Problems", 38, CHALK_WHITE,
                               "BOLD").move_to(np.array([BOARD_CX, BOARD_CY + 1.65, 0]))
            self.play(Write(title), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            sub = board_text("When the river changes your speed", 21,
                             CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 0.95, 0]))
            self.play(Write(sub), run_time=rt(tracker.time_until_bookmark("b1") * 0.4))

            river = river_band(width=8.6, cy=-0.75, height=0.85, n_arrows=7)
            land_y = float(river.land_top[1])
            a = town_marker("A", BOARD_CX - 3.45, land_y, scale=0.8)
            b = town_marker("B", BOARD_CX + 3.45, land_y, scale=0.8)
            boat = boat_icon(0.85).move_to(np.array([BOARD_CX - 2.1, -0.55, 0]))
            tag = VGroup(board_text("same boat", 15, BOAT_COLOR),
                         board_text("same distance", 15, CHALK_WHITE),
                         board_text("different speed", 15, STREAM_COLOR)
                         ).arrange(RIGHT, buff=0.5).move_to(
                np.array([BOARD_CX, -1.9, 0]))
            self.play(Create(river), FadeIn(a), FadeIn(b),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.play(FadeIn(boat, shift=LEFT * 0.2), FadeIn(tag),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["pop"], gain=-13)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 1: the two journeys ------------------------------------------
    def beat1_journey(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("A Boat on a River", 25, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            river = river_band(width=8.6, cy=0.3, height=0.8, n_arrows=7)
            land_y = float(river.land_top[1])
            a = town_marker("A", BOARD_CX - 3.45, land_y, scale=0.85)
            b = town_marker("B", BOARD_CX + 3.45, land_y, scale=0.85)
            boat = boat_icon(0.85).move_to(np.array([BOARD_CX - 2.6, 0.2, 0]))
            wake = boat_wake(boat, facing=1)

            start_l, end_l = BOARD_CX - 2.6, BOARD_CX + 2.6
            self.play(Write(heading), Create(river), FadeIn(a), FadeIn(b),
                      FadeIn(boat),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.6))
            self.play(Indicate(river.arrows, color=STREAM_COLOR, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            # downstream: with the current, visibly quick
            t_down = clock_badge("5 h", DOWN_COLOR, scale=0.85).move_to(
                np.array([BOARD_CX + 2.2, 1.9, 0]))
            self.play(boat.animate.move_to(np.array([end_l, 0.2, 0])),
                      FadeIn(wake),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.play(FadeIn(t_down), run_time=rt(tracker.time_until_bookmark("b2") * 0.4))
            self.add_sound(self.sfx["ding"], gain=-13)

            # upstream: against the current, visibly slower
            turned = boat_icon(0.85, facing=-1).move_to(boat.get_center())
            t_up = clock_badge("6 h", UP_COLOR, scale=0.85).move_to(
                np.array([BOARD_CX - 2.2, -0.85, 0]))
            self.play(ReplacementTransform(boat, turned), FadeOut(wake),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.6))
            self.play(turned.animate.move_to(np.array([start_l, 0.2, 0])),
                      FadeIn(boat_wake(turned, facing=-1)),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            note = board_text("The same distance, but different times.", 17,
                              CHALK_WHITE).move_to(np.array([BOARD_CX, -1.35, 0]))
            self.play(FadeIn(t_up), FadeIn(note),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            question = board_text("Why are the two journeys so different?", 19,
                                  CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, -2.0, 0]))
            self.play(FadeOut(note), FadeIn(question), run_time=rt(
                tracker.time_until_bookmark("b5")))

            tag = board_text("The river is moving too!", 19, CHALK_YELLOW,
                             "BOLD").move_to(np.array([BOARD_CX, -2.5, 0]))
            self.play(FadeIn(tag), Flash(river.arrows, color=STREAM_COLOR,
                                         flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b6")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 2: downstream -------------------------------------------------
    def beat2_downstream(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("Downstream: With the Current", 23,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            y_boat, y_res = 1.7, 0.75
            x0 = BOARD_CX - 2.4
            boat_ar = Arrow(np.array([x0, y_boat, 0]), np.array([x0 + 1.9, y_boat, 0]),
                            buff=0, color=BOAT_COLOR, stroke_width=3,
                            max_tip_length_to_length_ratio=0.18, tip_length=0.16)
            cur_ar = Arrow(np.array([x0 + 1.9, y_boat, 0]),
                           np.array([x0 + 2.9, y_boat, 0]),
                           buff=0, color=STREAM_COLOR, stroke_width=3,
                           max_tip_length_to_length_ratio=0.18, tip_length=0.16)
            boat_lbl = MathTex("x", font_size=30, color=BOAT_COLOR).next_to(
                boat_ar, UP, buff=0.12)
            cur_lbl = MathTex("2", font_size=30, color=STREAM_COLOR).next_to(
                cur_ar, UP, buff=0.12)
            res_ar = Arrow(np.array([x0, y_res, 0]), np.array([x0 + 2.9, y_res, 0]),
                           buff=0, color=DOWN_COLOR, stroke_width=3.4,
                           max_tip_length_to_length_ratio=0.16, tip_length=0.16)
            res_lbl = MathTex("x+2", font_size=32, color=DOWN_COLOR).next_to(
                res_ar, UP, buff=0.12)
            guide = DashedLine(np.array([x0 + 2.9, y_boat, 0]),
                               np.array([x0 + 2.9, y_res, 0]),
                               stroke_color=CHALK_WHITE, stroke_width=1.2,
                               dash_length=0.08)

            self.play(GrowArrow(boat_ar), FadeIn(boat_lbl),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(Indicate(boat_ar, color=BOAT_COLOR, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.play(GrowArrow(cur_ar), FadeIn(cur_lbl),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(GrowArrow(res_ar), Create(guide),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.play(FadeIn(res_lbl),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.5))

            river = river_band(width=7.4, cy=-1.15, height=0.7, n_arrows=6)
            label = board_text("DOWNSTREAM", 18, DOWN_COLOR, "BOLD").move_to(
                np.array([BOARD_CX, -1.95, 0]))
            rule = board_text("with the current  ->  ADD", 19, CHALK_YELLOW,
                              "BOLD").move_to(np.array([BOARD_CX, -2.5, 0]))
            self.play(FadeIn(river), run_time=rt(tracker.time_until_bookmark("b3")))
            self.play(FadeIn(label), FadeIn(rule), Flash(res_lbl, color=DOWN_COLOR,
                                                         flash_radius=0.5),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 3: upstream ---------------------------------------------------
    def beat3_upstream(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()

            heading = board_text("Upstream: Against the Current", 23,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            y_boat, y_res = 1.7, 0.75
            x_right = BOARD_CX + 2.2       # the boat's starting (right) end
            boat_ar = Arrow(np.array([x_right, y_boat, 0]),
                            np.array([x_right - 1.9, y_boat, 0]),
                            buff=0, color=BOAT_COLOR, stroke_width=3,
                            max_tip_length_to_length_ratio=0.18, tip_length=0.16)
            # the current keeps pointing the SAME way it always did
            cur_ar = Arrow(np.array([x_right - 1.9, y_boat, 0]),
                           np.array([x_right - 0.9, y_boat, 0]),
                           buff=0, color=STREAM_COLOR, stroke_width=3,
                           max_tip_length_to_length_ratio=0.18, tip_length=0.16)
            boat_lbl = MathTex("x", font_size=30, color=BOAT_COLOR).next_to(
                boat_ar, UP, buff=0.12)
            cur_lbl = MathTex("2", font_size=30, color=STREAM_COLOR).next_to(
                cur_ar, UP, buff=0.12)
            res_ar = Arrow(np.array([x_right, y_res, 0]),
                           np.array([x_right - 0.9, y_res, 0]),
                           buff=0, color=UP_COLOR, stroke_width=3.4,
                           max_tip_length_to_length_ratio=0.2, tip_length=0.16)
            res_lbl = MathTex("x-2", font_size=32, color=UP_COLOR).next_to(
                res_ar, DOWN, buff=0.12)
            guide = DashedLine(np.array([x_right - 1.9, y_boat, 0]),
                               np.array([x_right - 1.9, y_res, 0]),
                               stroke_color=CHALK_WHITE, stroke_width=1.2,
                               dash_length=0.08)

            self.play(GrowArrow(boat_ar), FadeIn(boat_lbl),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(GrowArrow(cur_ar), FadeIn(cur_lbl),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(GrowArrow(res_ar), Create(guide),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.play(FadeIn(res_lbl), Flash(res_lbl, color=UP_COLOR,
                                             flash_radius=0.5),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.6))

            river = river_band(width=7.4, cy=-1.15, height=0.7, n_arrows=6)
            label = board_text("UPSTREAM", 18, UP_COLOR, "BOLD").move_to(
                np.array([BOARD_CX, -1.95, 0]))
            rule = board_text("against the current  ->  SUBTRACT", 19,
                              CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -2.5, 0]))
            self.play(FadeIn(river), run_time=rt(tracker.time_until_bookmark("b3")))
            self.play(FadeIn(label), FadeIn(rule),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 4: speed x time ----------------------------------------------
    def lane_row(self, label: str, color: str, time_text: str, speed_tex: str,
                 dist_tex: str, y: float) -> VGroup:
        """One journey lane: [name] [clock] -> [speed] -> [distance]."""
        name = board_text(label, 17, color, "BOLD")
        clock = clock_badge(time_text, color, scale=0.8)
        a1 = MathTex(r"\rightarrow", font_size=30, color=CHALK_WHITE)
        speed = MathTex(speed_tex, font_size=26, color=color)
        a2 = MathTex(r"\rightarrow", font_size=30, color=CHALK_WHITE)
        dist = MathTex(dist_tex, font_size=28, color=CHALK_WHITE)
        row = VGroup(name, clock, a1, speed, a2, dist).arrange(RIGHT, buff=0.3)
        row.move_to(np.array([BOARD_CX, y, 0]))
        row.name, row.clock = name, clock
        row.a1, row.speed, row.a2, row.dist = a1, speed, a2, dist
        return row

    def beat4_distance(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()

            heading = board_text("Distance = Speed x Time", 25, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            formula = MathTex(r"\text{Distance}", r"\;=\;", r"\text{Speed}\times\text{Time}",
                              font_size=30, color=CHALK_YELLOW).move_to(
                np.array([BOARD_CX, 2.15, 0]))
            self.play(Write(formula), run_time=rt(tracker.time_until_bookmark("b0") * 0.7))
            self.add_sound(self.sfx["ding"], gain=-13)

            down = self.lane_row("Downstream", DOWN_COLOR, "5 h", "x+2",
                                 "5(x+2)", 0.95)
            up = self.lane_row("Upstream", UP_COLOR, "6 h", "x-2", "6(x-2)", -0.15)

            self.play(FadeIn(down.name), FadeIn(down.clock),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(FadeIn(up.name), FadeIn(up.clock),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.6))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(FadeIn(down.a1), FadeIn(down.speed),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.4))
            self.play(TransformFromCopy(down.speed, down.dist), FadeIn(down.a2),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(up.a1), FadeIn(up.speed),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.5))
            self.play(TransformFromCopy(up.speed, up.dist), FadeIn(up.a2),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 5: same distance ---------------------------------------------
    def beat5_same(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            self.reset_board()

            heading = board_text("Same Distance!", 26, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            river = river_band(width=6.6, cy=1.2, height=0.55, n_arrows=4)
            land_y = float(river.land_top[1])
            a = town_marker("A", BOARD_CX - 3.6, land_y, scale=0.72)
            b = town_marker("B", BOARD_CX + 3.6, land_y, scale=0.72)
            span_l, span_r = BOARD_CX - 2.6, BOARD_CX + 2.6

            top_ar = DoubleArrow(np.array([span_l, 1.85, 0]),
                                 np.array([span_r, 1.85, 0]), buff=0,
                                 color=DOWN_COLOR, stroke_width=2.4,
                                 max_tip_length_to_length_ratio=0.1,
                                 tip_length=0.12)
            top_lbl = VGroup(MathTex("5(x+2)", font_size=28, color=DOWN_COLOR),
                             board_text("downstream, 5 h", 14, DOWN_COLOR)
                             ).arrange(DOWN, buff=0.02).next_to(top_ar, UP, buff=0.1)
            bot_ar = DoubleArrow(np.array([span_l, 0.45, 0]),
                                 np.array([span_r, 0.45, 0]), buff=0,
                                 color=UP_COLOR, stroke_width=2.4,
                                 max_tip_length_to_length_ratio=0.1,
                                 tip_length=0.12)
            bot_lbl = VGroup(MathTex("6(x-2)", font_size=28, color=UP_COLOR),
                             board_text("upstream, 6 h", 14, UP_COLOR)
                             ).arrange(DOWN, buff=0.02).next_to(bot_ar, DOWN, buff=0.1)

            self.play(Write(heading), Create(river), FadeIn(a), FadeIn(b),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.6))
            self.play(GrowArrow(top_ar), FadeIn(top_lbl),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(GrowArrow(bot_ar), FadeIn(bot_lbl),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            note = board_text("Both journeys cover the same A to B distance.",
                              18, CHALK_WHITE).move_to(
                np.array([BOARD_CX, -0.8, 0]))
            self.play(FadeIn(note),
                      Indicate(top_ar, color=DOWN_COLOR, scale_factor=1.0),
                      Indicate(bot_ar, color=UP_COLOR, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.6))
            self.play(Flash(note, color=CHALK_WHITE, flash_radius=0.8),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            eq = MathTex("5(x+2)", r"\;=\;", "6(x-2)", font_size=40)
            align_equals(eq, BOARD_CX, -1.6)
            eq_box = SurroundingRectangle(eq, color=DOWN_COLOR, buff=0.2,
                                          corner_radius=0.1, stroke_width=3)
            # the two distance expressions merge into one equation
            self.play(TransformFromCopy(top_lbl[0], eq[0][0:6]),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            self.play(TransformFromCopy(bot_lbl[0], eq[2]), FadeIn(eq[1]),
                      Create(eq_box),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)

            tail = board_text("The same distance creates the equation.", 18,
                              CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -2.45, 0]))
            self.play(FadeOut(note), FadeIn(tail),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-12)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 6: solve ------------------------------------------------------
    def beat6_solve(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("Solve for the Boat's Speed", 23, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            e1 = MathTex("5(x+2)", r"\;=\;", "6(x-2)", font_size=38)
            align_equals(e1, BOARD_CX, 1.75)
            self.play(Write(e1), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            e2 = MathTex("5x+10", r"\;=\;", "6x-12", font_size=38)
            align_equals(e2, BOARD_CX, 1.75)
            self.play(TransformMatchingTex(e1, e2),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.4))
            e3 = MathTex("5x-6x", r"\;=\;", "-12-10", font_size=38)
            align_equals(e3, BOARD_CX, 1.75)
            self.play(TransformMatchingTex(e2, e3),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            e4 = MathTex("-x", r"\;=\;", "-22", font_size=38)
            align_equals(e4, BOARD_CX, 1.75)
            self.play(TransformMatchingTex(e3, e4),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            e5 = MathTex("x", r"\;=\;", "22", font_size=42, color=CHALK_GREEN)
            align_equals(e5, BOARD_CX, 1.75)
            self.play(TransformMatchingTex(e4, e5),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            ans = MathTex("22", r"\text{ km/h}", font_size=44, color=CHALK_GREEN
                          ).move_to(np.array([BOARD_CX, 0.35, 0]))
            abox = SurroundingRectangle(ans, color=CHALK_GREEN, buff=0.22,
                                        corner_radius=0.1, stroke_width=3)
            note = board_text("boat speed in still water", 17, CHALK_GREEN,
                              "BOLD").next_to(abox, DOWN, buff=0.16)
            self.play(FadeOut(e5), run_time=rt(tracker.time_until_bookmark("b3") * 0.4))
            self.play(FadeIn(ans), Create(abox), FadeIn(note),
                      Flash(ans, color=CHALK_GREEN, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-12)

            check = board_text("Now let's test it on the river.", 18, CHALK_YELLOW,
                               "BOLD").move_to(np.array([BOARD_CX, -1.05, 0]))
            self.play(FadeIn(check), run_time=rt(tracker.time_until_bookmark("b4") * 0.6))
            self.play(Indicate(ans, color=CHALK_GREEN, scale_factor=1.06),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 7: check ------------------------------------------------------
    def beat7_check(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("Check Both Journeys", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            down = MathTex("22+2", "=", "24", r"\quad", r"24\times 5", "=", "120",
                           font_size=32, color=DOWN_COLOR).move_to(
                np.array([BOARD_CX, 1.55, 0]))
            down_lbl = board_text("downstream", 16, DOWN_COLOR, "BOLD").next_to(
                down, UP, buff=0.14)
            self.play(Write(down), FadeIn(down_lbl),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            up = MathTex("22-2", "=", "20", r"\quad", r"20\times 6", "=", "120",
                         font_size=32, color=UP_COLOR).move_to(
                np.array([BOARD_CX, 0.45, 0]))
            up_lbl = board_text("upstream", 16, UP_COLOR, "BOLD").next_to(
                up, UP, buff=0.14)
            self.play(Write(up), FadeIn(up_lbl),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            same = MathTex("120", r"\;=\;", "120", font_size=38, color=CHALK_GREEN
                           ).move_to(np.array([BOARD_CX, -0.75, 0]))
            ck = tick_beside(same, CHALK_GREEN, 0.34, 0.35)
            self.play(Write(same), run_time=rt(tracker.time_until_bookmark("b2") * 0.6))
            self.play(Create(ck), Flash(same, color=CHALK_GREEN, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            note = board_text("Both journeys cover the same 120 km.", 18,
                              CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.65, 0]))
            self.play(FadeIn(note), run_time=rt(tracker.time_until_bookmark("b3") * 0.6))
            self.play(Circumscribe(note, color=CHALK_YELLOW, stroke_width=3),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-12)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 8: the strategy ----------------------------------------------
    def beat8_strategy(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("The Four-Step Method", 25, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            c1 = VGroup(card(2.2, 1.75, BOAT_COLOR),
                        board_text("1. DIRECTION", 14, BOAT_COLOR, "BOLD"),
                        board_text("with or against?", 13, CHALK_WHITE))
            c1[1].move_to(c1[0].get_top() + DOWN * 0.3)
            c1[2].move_to(c1[0].get_center() + DOWN * 0.25)
            c2 = VGroup(card(2.2, 1.75, STREAM_COLOR),
                        board_text("2. SPEED", 14, STREAM_COLOR, "BOLD"),
                        MathTex("b+s,\\; b-s", font_size=21))
            c2[1].move_to(c2[0].get_top() + DOWN * 0.3)
            c2[2].move_to(c2[0].get_center() + DOWN * 0.25)
            c3 = VGroup(card(2.2, 1.75, CHALK_GREEN),
                        board_text("3. DISTANCE", 14, CHALK_GREEN, "BOLD"),
                        MathTex(r"\text{speed}\times\text{time}", font_size=19))
            c3[1].move_to(c3[0].get_top() + DOWN * 0.3)
            c3[2].move_to(c3[0].get_center() + DOWN * 0.25)
            c4 = VGroup(card(2.2, 1.75, CHALK_YELLOW),
                        board_text("4. EQUATE", 14, CHALK_YELLOW, "BOLD"),
                        board_text("same route -> equal", 12, CHALK_WHITE))
            c4[1].move_to(c4[0].get_top() + DOWN * 0.3)
            c4[2].move_to(c4[0].get_center() + DOWN * 0.25)
            cards = VGroup(c1, c2, c3, c4).arrange(RIGHT, buff=0.18).move_to(
                np.array([BOARD_CX, 0.55, 0]))
            cards.shift(RIGHT * (BOARD_CX - cards.get_center()[0]))

            marks = ["b0", "b1", "b2", "b3"]
            for c, m in zip(cards, marks):
                self.play(FadeIn(c, shift=DOWN * 0.12),
                          run_time=rt(tracker.time_until_bookmark(m)))
                self.add_sound(self.sfx["click"], gain=-15)

            strip = board_text("Direction  ->  Speed  ->  Distance  ->  Equation",
                               19, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.4, 0]))
            self.play(FadeIn(strip), Circumscribe(strip, color=CHALK_YELLOW,
                                                  stroke_width=3),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.6))
            self.play(Indicate(cards[3], color=CHALK_YELLOW, scale_factor=1.04),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 9: student challenge -----------------------------------------
    def beat9_challenge(self) -> None:
        with self.voiceover(text=NARRATION["scene9_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", 30, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y - 0.05, 0]))
            p1 = VGroup(board_text("Same river distance: downstream ", 16),
                        board_text("4 h", 16, DOWN_COLOR, "BOLD"),
                        board_text(", upstream ", 16),
                        board_text("6 h", 16, UP_COLOR, "BOLD"),
                        board_text(".", 16)).arrange(RIGHT, buff=0.05)
            p2 = VGroup(board_text("Stream speed: ", 16),
                        board_text("3 km/h", 16, STREAM_COLOR, "BOLD"),
                        board_text(".", 16)).arrange(RIGHT, buff=0.05)
            puzzle = VGroup(p1, p2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX, 2.15, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.play(FadeIn(puzzle, shift=DOWN * 0.1),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            q_d = MathTex("?", font_size=34, color=DOWN_COLOR).move_to(
                np.array([BOARD_CX - 1.9, 1.0, 0]))
            q_u = MathTex("?", font_size=34, color=UP_COLOR).move_to(
                np.array([BOARD_CX + 1.9, 1.0, 0]))
            lab_d = board_text("downstream speed", 15, DOWN_COLOR, "BOLD").next_to(
                q_d, DOWN, buff=0.12)
            lab_u = board_text("upstream speed", 15, UP_COLOR, "BOLD").next_to(
                q_u, DOWN, buff=0.12)
            ask = board_text("Let the boat's speed in still water be x.", 17,
                             BOAT_COLOR, "BOLD").move_to(
                np.array([BOARD_CX, 0.15, 0]))
            pause = board_text("Pause and try it", 19, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -0.55, 0]))
            self.play(FadeIn(q_d), FadeIn(q_u), FadeIn(lab_d), FadeIn(lab_u),
                      FadeIn(ask),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.play(FadeIn(pause), run_time=rt(tracker.time_until_bookmark("b3") * 0.85))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(Indicate(VGroup(q_d, q_u), color=CHALK_YELLOW, scale_factor=1.03),
                      run_time=rt(tracker.get_remaining_duration() * 0.9))
            self.challenge = VGroup(heading, puzzle, q_d, q_u, lab_d, lab_u, ask,
                                    pause)
            self._capture_srt(tracker)

        play_challenge_countdown(self, seconds=6, sfx=self.sfx)

        with self.voiceover(text=NARRATION["scene9_reveal"]) as tracker:
            q_d, q_u = self.challenge[2], self.challenge[3]
            self.play(FadeOut(self.challenge[7]), FadeOut(self.challenge[6]),
                      FadeOut(self.challenge[4]), FadeOut(self.challenge[5]),
                      run_time=0.3)
            d_val = MathTex("x+3", font_size=32, color=DOWN_COLOR).move_to(q_d)
            u_val = MathTex("x-3", font_size=32, color=UP_COLOR).move_to(q_u)
            self.play(ReplacementTransform(q_d, d_val), ReplacementTransform(q_u, u_val),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            e1 = MathTex("4(x+3)", r"\;=\;", "6(x-3)", font_size=36)
            align_equals(e1, BOARD_CX, -0.35)
            self.play(Write(e1), run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            e2 = MathTex("4x+12", r"\;=\;", "6x-18", font_size=36)
            align_equals(e2, BOARD_CX, -0.35)
            self.play(TransformMatchingTex(e1, e2),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            e3 = MathTex("30", r"\;=\;", "2x", font_size=36)
            align_equals(e3, BOARD_CX, -0.35)
            self.play(TransformMatchingTex(e2, e3),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            e4 = MathTex("x", r"\;=\;", "15", font_size=40, color=CHALK_GREEN)
            align_equals(e4, BOARD_CX, -0.35)
            self.play(TransformMatchingTex(e3, e4),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            ans = MathTex("15", r"\text{ km/h}", font_size=42, color=CHALK_GREEN
                          ).move_to(np.array([BOARD_CX, -1.5, 0]))
            abox = SurroundingRectangle(ans, color=CHALK_GREEN, buff=0.2,
                                        corner_radius=0.1, stroke_width=3)
            lbl = board_text("boat speed in still water", 16, CHALK_GREEN,
                             "BOLD").next_to(abox, DOWN, buff=0.14)
            self.play(FadeOut(e4), run_time=rt(tracker.time_until_bookmark("b3") * 0.4))
            self.play(FadeIn(ans), Create(abox), FadeIn(lbl),
                      Flash(ans, color=CHALK_GREEN, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-12)

            well = board_text("Same distance, same equation. Well done!", 16,
                              CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -2.62, 0]))
            self.play(FadeIn(well), run_time=rt(tracker.time_until_bookmark("b4") * 0.6))
            self.play(Flash(well, color=CHALK_YELLOW, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self.play(Indicate(ans, color=CHALK_GREEN, scale_factor=1.08),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 10: summary ---------------------------------------------------
    def beat10_summary(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("Summary", 31, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y - 0.05, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.4))

            chain = MathTex(r"t_d(b+s) \;=\; t_u(b-s)", font_size=28,
                            color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, 2.3, 0]))
            self.play(Write(chain), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            r1 = summary_row(1, "With the current:", r"v = b+s", DOWN_COLOR)
            r2 = summary_row(2, "Against the current:", r"v = b-s", UP_COLOR)
            r3 = summary_row(3, "Each distance:", r"\text{speed}\times\text{time}",
                             BOAT_COLOR)
            r4 = summary_row(4, "Same route:", r"t_d(b+s) = t_u(b-s)", STREAM_COLOR)
            rows = VGroup(r1, r2, r3, r4).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            rows.move_to(np.array([BOARD_CX, 0.55, 0]))
            rows.shift(RIGHT * (BOARD_CX - rows.get_center()[0]))

            self.play(FadeIn(r1, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(r2, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(r3, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(r4, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # the takeaway closes the summary ...
            take = board_text("Current changes the speed.", 22, CHALK_YELLOW,
                              "BOLD").move_to(np.array([BOARD_CX, -1.45, 0]))
            take2 = board_text("Same distance creates the equation.", 20,
                               CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX, -2.0, 0]))
            self.play(FadeIn(take), Flash(take, color=CHALK_YELLOW, flash_radius=0.9),
                      FadeIn(take2),
                      run_time=rt(tracker.time_until_bookmark("b5") * 0.3))
            self.add_sound(self.sfx["success"], gain=-11)

            summary = VGroup(heading, chain, rows, take, take2)
            self.play(FadeOut(summary),
                      run_time=rt(tracker.time_until_bookmark("b5") * 0.3))

            # ... so after the summary only the Thank-You template is left.
            thanks = board_text("Thank You for Watching!", 40, CHALK_WHITE, "BOLD")
            thanks2 = board_text("See you in the next lesson :)", 25, CHALK_CYAN)
            thanks_group = VGroup(thanks, thanks2).arrange(DOWN, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY, 0]))
            self.play(Write(thanks),
                      run_time=rt(tracker.time_until_bookmark("b5") * 0.4))
            self.add_sound(self.sfx["ding"], gain=-11)
            self.play(FadeIn(thanks2, shift=UP * 0.1),
                      run_time=rt(tracker.get_remaining_duration()))
            self.play(Circumscribe(thanks_group, color=CHALK_AMBER, stroke_width=3,
                                   time_width=0.5), run_time=0.3)
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(END_HOLD)


if __name__ == "__main__":
    pass

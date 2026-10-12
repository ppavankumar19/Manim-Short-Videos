"""
Percentage Increases, Decreases & Quick Estimation Rules on Bills
Story-mode chalkboard lesson (Class 8 Maths, Chapter 5: Comparing Quantities
using Proportion, Storymode 02).

LLM KEY / FUNCTION NAME: percentage_applications_and_estimation

Production pipeline (mirrors the rest of the Story-Mode series):
  - Shared assets/background2.png chalkboard backdrop + student/teacher
    cutouts + corner badges (dhimantAI top-left, Mathematics top-right).
  - VoiceoverScene + speech service; narration written as continuous prose.
  - Real per-word sync via <bookmark> tags + tracker timing, and a
    ground-truth SRT export from the service word boundaries.
  - Sound effects from sound_effects.py; chalk-styled Text (Segoe Print) and
    MathTex; shared story_common.play_challenge_countdown() for the THINK clock.
  - Text appears crisply and the board then HOLDS; diagram work is paced across
    its window, words are not.
  - Nothing on the board sits below y = -2.00: the burned-in caption grows up
    from the bottom of the frame.

The defining visual is the PERCENTAGE CONTROL PANEL: three modes (CONVERT,
CHANGE, ESTIMATE) stay on the board while every scene lights the one it needs.
Under it the lesson draws hundred-cell percentage squares that fill cell by
cell, the 100% original bar with a block that visibly ATTACHES for an increase
and a block that visibly LEAVES for a decrease, rupee notes and coins, a price
tag, a bill on a ruler that snaps from 477.80 to 480, and a ten-percent block
that splits in half to make five percent.

Title + 10 scenes:
  0. Title card: 225 of 300 against 200 of 250 -- who did better?
  1. Converting to one scale: 3/4 = 75% and 4/5 = 80%, and the rule
     percentage = part / whole x 100%.
  2. A 35% increase: the original is a full 100% bar and a 35% block attaches
     to it, so the new value is 135% of the original.
  3. Applying it: sales of Rs 98,700 up 35% -- the increase is Rs 34,545 and
     the new figure is Rs 1,33,245, the same as 135% of 98,700.
  4. A 10% decrease: a Rs 550 tag with 10% off pays Rs 495; the comparison
     panel sets increase p% -> 100% + p% and decrease p% -> 100% - p%.
  5. The mental toolkit: 10% = one tenth, 5% = half of 10%, 15% = 10% + 5%,
     20% = two tens -- demonstrated on 480 to give 72.
  6. Estimation on a bill: Rs 477.80 rounds to 480, 15% of that is 72, so the
     payment is about Rs 408, that is about Rs 410.
  7. Exact versus estimate: 15% of 477.80 is 71.67 and the exact answer is
     406.13 -- close enough to show that the estimate is sensible, and that an
     estimate is a reasonableness check, not exact arithmetic.
  8. The decision map: convert, increase, decrease, estimate.
  9. Your turn: four checks (18 of 24, 10% off Rs 800, 20% of 357.30, and a
     35% rise on Rs 900) after the series' centred ten-second THINK clock.
 10. Recap: compare, change, estimate, check -- and the spoken thank-you card.
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
    ORIGIN, UP, DOWN, LEFT, RIGHT, UL, UR, DL, DR, PI, TAU, DEGREES, BLACK,
    ImageMobject, MathTex, VGroup, Line, DashedLine, Circle, Rectangle,
    RoundedRectangle, Square, Polygon, Angle, RightAngle, Dot, Arrow,
    DoubleArrow, Text,
    Write, FadeIn, FadeOut, Create, ReplacementTransform, TransformMatchingTex,
    Transform, TransformFromCopy, GrowArrow, ValueTracker, always_redraw,
    Indicate, Flash, Circumscribe, SurroundingRectangle, LaggedStart,
    config,
)
from manim_voiceover import VoiceoverScene
from manim_voiceover.tracker import AUDIO_OFFSET_RESOLUTION

from speech_service import get_speech_service
from sound_effects import load_all as load_sfx
from story_common import play_challenge_countdown
from synced_voice import install_synced_voiceover
# --------------------------------------------------------------- theme -----
CHALK_WHITE = "#F5F2E9"
BRAND_WHITE = "#FFFFFF"  # pure white for the dhimantAI badge -- higher contrast than CHALK_WHITE
CHALK_YELLOW = "#FFE066"
CHALK_PINK = "#FF8FA3"
CHALK_CYAN = "#7FE7DC"
CHALK_AMBER = "#E8B769"
CHALK_GREEN = "#9BE38A"
CHALK_RED = "#FF6B6B"
FONT = "Segoe Print"
MATH_COLOR = CHALK_WHITE

END_HOLD = 2.0
TRANSITION_HOLD = 0.35
MIN_RT = 0.12

# Measured chalkboard safe bounds (shared across the series)
BOARD_LEFT = -4.6
BOARD_RIGHT = 5.6
BOARD_TOP = 3.3
BOARD_BOTTOM = -2.9
BOARD_CX = (BOARD_LEFT + BOARD_RIGHT) / 2  # 0.5
BOARD_CY = (BOARD_TOP + BOARD_BOTTOM) / 2  # 0.2

# The main equation line lives here for scenes 1-6 so the '=' never moves.
EQ_Y = 0.7


def rt(seconds: float, floor: float = MIN_RT) -> float:
    return max(floor, float(seconds))


TEXT_CAP = 0.85        # longest a text write may take


def quick(seconds: float, cap: float = TEXT_CAP) -> float:
    """A capped run-time for text.

    Narration windows are long (10-25 s), so a heading written across half of
    one takes seconds to appear and mid-render frames look like a truncated
    title ("A Geome...").  Writing is capped and the window's remaining time is
    spent on the diagram, which is what the narration is actually describing.
    """
    return rt(min(float(seconds), cap))


def leftover(tracker, mark: str) -> float:
    """Seconds still to run before the next bookmark of the narration."""
    return max(rt(tracker.time_until_bookmark(mark)), 0.0)


def board_text(s: str, size: int = 34, color: str = CHALK_WHITE,
               weight: str = "NORMAL") -> Text:
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def chalk_math(s: str, size: int = 34, color: str = MATH_COLOR) -> MathTex:
    return MathTex(s, font_size=size, color=color)


# ------------------------------------------------------- geometry helpers ----

UNIT_CM = 0.30          # 1 cm of the textbook drawing, in board units
SIDE_LONG = 2.40        # 8 cm
SIDE_SHORT = 1.80       # 6 cm
STICK_W = 7.0           # stroke width of a rigid stick
JOINT_R = 0.075


def quad_points(centre, theta=90 * DEGREES, a=SIDE_LONG, b=SIDE_SHORT):
    """Corners A (bottom-left), B (bottom-right), C (top-right), D (top-left)
    of a parallelogram whose sides AB = CD = a and BC = DA = b keep their
    lengths for every interior angle `theta` at A.  At theta = 90 deg it is a
    rectangle; every other value is a genuine shear of the same four sticks."""
    p = np.array(centre, dtype=float)
    dx, dy = b * np.cos(theta), b * np.sin(theta)
    A = p + np.array([-(a + dx) / 2.0, -dy / 2.0, 0.0])
    B = A + np.array([a, 0.0, 0.0])
    C = B + np.array([dx, dy, 0.0])
    D = A + np.array([dx, dy, 0.0])
    return A, B, C, D


def stick(p1, p2, color=CHALK_AMBER, width=STICK_W) -> VGroup:
    """One rigid stick: a dark outline, a painted body and a soft highlight
    down the middle, so the frame reads as physical material rather than as a
    thin line.  The joint pins cover the ends."""
    outline = Line(p1, p2, color="#241a10", stroke_width=width + 3.2,
                   stroke_opacity=0.9)
    body = Line(p1, p2, color=color, stroke_width=width)
    gloss = Line(p1, p2, color=CHALK_WHITE, stroke_width=width * 0.26,
                 stroke_opacity=0.34)
    grp = VGroup(outline, body, gloss)
    grp.body, grp.gloss = body, gloss
    return grp


def joint(p, color=CHALK_WHITE, r=JOINT_R) -> VGroup:
    """A movable joint: a small metal pin at a corner."""
    ring = Circle(radius=r, stroke_color=color, stroke_width=1.6,
                  fill_color="#1B2733", fill_opacity=0.95).move_to(p)
    pin = Dot(radius=r * 0.32, color=CHALK_AMBER).move_to(p)
    return VGroup(ring, pin)


def frame_at(theta, centre=np.array([BOARD_CX, 0.35, 0]), a=SIDE_LONG,
             b=SIDE_SHORT, color=CHALK_AMBER, with_joints=True) -> VGroup:
    """The four-stick frame at interior angle `theta`.  The corner positions
    come from `quad_points`, so the four side lengths are exactly preserved
    for every angle -- nothing is stretched during the shear."""
    A, B, C, D = quad_points(centre, theta, a, b)
    grp = VGroup(stick(A, B, color), stick(B, C, color),
                 stick(C, D, color), stick(D, A, color))
    if with_joints:
        grp.add(joint(A), joint(B), joint(C), joint(D))
    grp.corners = (A, B, C, D)
    grp.a, grp.b = a, b
    return grp


def outline_at(theta, centre, a=SIDE_LONG, b=SIDE_SHORT, color=CHALK_WHITE,
               opacity=0.35) -> Polygon:
    """A faint outline of one configuration, used to stack the three shapes
    that share the same four side lengths."""
    A, B, C, D = quad_points(centre, theta, a, b)
    poly = Polygon(A, B, C, D, color=color, stroke_width=2.2,
                   fill_opacity=0.0)
    poly.set_stroke(opacity=opacity)
    poly.corners = (A, B, C, D)
    return poly


def side_label(p1, p2, centroid, text, color=CHALK_CYAN, size=17,
               offset=0.22) -> Text:
    """A length label placed clear of its own side.

    The label is pushed out along the outward normal by its own half-extent
    *plus* `offset`, so no glyph can sit on the line.  With a fixed offset the
    "6 cm" labels of a vertical side were centred only 0.26 units out while the
    text is over a unit wide, so the side ran straight through the text (which
    is what made the edges look like broken tick marks)."""
    lab = board_text(text, size, color, "BOLD")
    mid = (np.array(p1, dtype=float) + np.array(p2, dtype=float)) / 2.0
    n = mid - np.array(centroid, dtype=float)
    n = n / (np.linalg.norm(n[:2]) or 1.0)
    half = (abs(n[0]) * lab.width + abs(n[1]) * lab.height) / 2.0
    return lab.move_to(mid + n * (half + offset))


def angle_mark(vertex, p1, p2, radius=0.32, color=CHALK_PINK,
               label=None, other_angle=None, right_angle=False) -> VGroup:
    """The angle at `vertex` between the two sides.

    A right angle gets the square symbol (the reversed L), never a curve: that
    is how a 90 degree corner is marked on a drawing.  Any other angle gets a
    chalk arc swept on the **interior** side of the corner, with an optional
    degree label on the bisector.

    `Angle` always sweeps counterclockwise from the first line unless told
    otherwise, and for some corner orientations that counterclockwise sweep is
    the *reflex* angle -- an arc of 240 or 300 degrees looping outside the
    figure.  The sweep is therefore chosen from the interior bisector, so the
    arc always lies between the two sides.  Pass `other_angle` explicitly to
    override."""
    l1 = Line(vertex, p1)
    l2 = Line(vertex, p2)
    v = np.array(vertex, dtype=float)
    d1 = np.array(p1, dtype=float) - v
    d2 = np.array(p2, dtype=float) - v
    d1 = d1 / (np.linalg.norm(d1[:2]) or 1.0)
    d2 = d2 / (np.linalg.norm(d2[:2]) or 1.0)
    bis = d1 + d2
    bis = bis / (np.linalg.norm(bis[:2]) or 1.0)
    if right_angle:
        mark = RightAngle(l1, l2, length=radius * 0.70, color=color,
                          stroke_width=2.8)
    else:
        if other_angle is None:
            t1 = float(np.arctan2(d1[1], d1[0]))
            t2 = float(np.arctan2(d2[1], d2[0]))
            ccw_mid = t1 + float((t2 - t1) % TAU) / 2.0
            beta = float(np.arctan2(bis[1], bis[0]))
            off = abs(((ccw_mid - beta) + PI) % TAU - PI)
            other_angle = off > PI / 2
        mark = Angle(l1, l2, radius=radius, color=color, stroke_width=2.4,
                     other_angle=bool(other_angle))
    grp = VGroup(mark)
    if label is not None:
        lab = board_text(label, 15, color, "BOLD").move_to(
            v + bis * (radius + 0.34))
        grp.add(lab)
        grp.label = lab
    grp.arc = mark
    return grp


def diagonal_stick(A, B, C, D, color=CHALK_GREEN, dashed=False) -> VGroup:
    """The fifth measurement: a stick along the diagonal BD.

    Built without the dark outline of a full stick: `Create` draws
    sub-mobjects in order, and a dark outline drawn first made the new diagonal
    read as a navy line on the dark board before it turned green."""
    if dashed:
        line = DashedLine(B, D, color=color, stroke_width=STICK_W * 0.55,
                          dash_length=0.14)
        return VGroup(line)
    body = Line(B, D, color=color, stroke_width=STICK_W * 0.72)
    gloss = Line(B, D, color=CHALK_WHITE, stroke_width=STICK_W * 0.22,
                 stroke_opacity=0.30)
    return VGroup(body, gloss)


def force_arrow(y, x_from, x_to, color=CHALK_RED, width=3.4) -> Arrow:
    """A sideways push against the frame."""
    return Arrow(np.array([x_from, y, 0.0]), np.array([x_to, y, 0.0]),
                 buff=0, color=color, stroke_width=width, tip_length=0.18)


def drawing_sheet(owner, x, y, w=3.0, h=2.4, color=CHALK_WHITE) -> VGroup:
    """A sheet of paper pinned to the board, with its owner's name above it."""
    paper = RoundedRectangle(corner_radius=0.08, width=w, height=h,
                             stroke_color=color, stroke_width=1.8,
                             fill_color="#F5F2E9", fill_opacity=0.09)
    paper.move_to(np.array([x, y, 0.0]))
    name = board_text(owner, 16, CHALK_AMBER, "BOLD").next_to(paper, UP,
                                                              buff=0.14)
    grp = VGroup(paper, name)
    grp.paper, grp.name = paper, name
    return grp


def sheet_shape(sheet, theta, a=1.55, b=1.15, color=CHALK_CYAN,
                opacity=1.0) -> VGroup:
    """A quadrilateral drawn on a sheet: outline plus corner dots."""
    A, B, C, D = quad_points(sheet.paper.get_center(), theta, a, b)
    poly = Polygon(A, B, C, D, color=color, stroke_width=3.0,
                   fill_color=color, fill_opacity=0.12 * opacity)
    poly.set_stroke(opacity=opacity)
    grp = VGroup(poly)
    grp.add(*[Dot(radius=0.045, color=color).move_to(p) for p in (A, B, C, D)])
    grp.corners = (A, B, C, D)
    grp.poly = poly
    return grp


def window_frame(centre=np.array([BOARD_CX, 0.45, 0]), theta=90 * DEGREES,
                 a=2.7, b=1.9, color=CHALK_AMBER,
                 with_brace=False) -> VGroup:
    """A window: outer frame, two vertical mullions, glass tint, and an
    optional diagonal brace between opposite corners."""
    A, B, C, D = quad_points(centre, theta, a, b)
    outer = VGroup(stick(A, B, color, STICK_W * 1.15),
                   stick(B, C, color, STICK_W * 1.15),
                   stick(C, D, color, STICK_W * 1.15),
                   stick(D, A, color, STICK_W * 1.15))
    p1 = A + (B - A) / 3.0
    p2 = D + (C - D) / 3.0
    p3 = A + (B - A) * 2.0 / 3.0
    p4 = D + (C - D) * 2.0 / 3.0
    mullions = VGroup(stick(p1, p2, color, STICK_W * 0.6),
                      stick(p3, p4, color, STICK_W * 0.6))
    glass = Polygon(A, B, C, D, color=CHALK_CYAN, stroke_width=0,
                    fill_color=CHALK_CYAN, fill_opacity=0.10)
    grp = VGroup(glass, outer, mullions)
    if with_brace:
        grp.add(diagonal_stick(A, B, C, D, CHALK_GREEN))
    grp.corners = (A, B, C, D)
    return grp


def summary_row(n: int, label: str, math_tex: str, color: str) -> VGroup:
    """One numbered recap row: badge, wording and the measurement it names
    (the same summary style used across the series)."""
    badge = Circle(radius=0.16, stroke_color=color, stroke_width=2,
                   fill_color=color, fill_opacity=0.18)
    num = board_text(str(n), 15, color, "BOLD").move_to(badge.get_center())
    return VGroup(VGroup(badge, num),
                  board_text(label, 15, CHALK_WHITE),
                  MathTex(math_tex, font_size=19, color=color)
                  ).arrange(RIGHT, buff=0.26)


def combo_card(code, meaning, color=CHALK_WHITE) -> VGroup:
    """One construction-combination card: the code plus its expansion.
    Kept compact -- five of them stack in the lower half of the board."""
    code_t = board_text(code, 15, color, "BOLD")
    mean_t = board_text(meaning, 12, CHALK_WHITE)
    box = RoundedRectangle(corner_radius=0.06,
                           width=max(code_t.width, mean_t.width) + 0.42,
                           height=0.50, stroke_color=color, stroke_width=1.5,
                           fill_color="#16202B", fill_opacity=0.75)
    code_t.move_to(box.get_center() + UP * 0.10)
    mean_t.move_to(box.get_center() + DOWN * 0.13)
    return VGroup(box, code_t, mean_t)


def choice_row(letter, text, color=CHALK_WHITE) -> VGroup:
    """One answer choice of the challenge, with a lettered badge."""
    badge = Circle(radius=0.19, stroke_color=color, stroke_width=2,
                   fill_color=color, fill_opacity=0.18)
    letter_t = board_text(letter, 16, color, "BOLD").move_to(badge.get_center())
    body = board_text(text, 17, CHALK_WHITE)
    grp = VGroup(VGroup(badge, letter_t), body).arrange(RIGHT, buff=0.26)
    grp.badge, grp.body = grp[0], grp[1]
    return grp

# ------------------------------------------------- construction furniture ----

from manim import Arc  # noqa: E402  (imported here so the base head stays put)

SCALE = 0.52            # board units per centimetre of the textbook drawing


def circle_intersection(c1, r1, c2, r2, upper=True):
    """Where two circles meet, on the chosen side of the line c1 -> c2.

    This is the mathematics behind "intersect the two arcs": with the four
    side lengths known, the fourth vertex is exactly this point."""
    c1 = np.array(c1, dtype=float)[:2]
    c2 = np.array(c2, dtype=float)[:2]
    d_vec = c2 - c1
    d = float(np.linalg.norm(d_vec))
    if d < 1e-6 or d > r1 + r2 or d < abs(r1 - r2):
        return None
    a = (d * d + r1 * r1 - r2 * r2) / (2.0 * d)
    h = float(np.sqrt(max(r1 * r1 - a * a, 0.0)))
    base = c1 + a * d_vec / d
    perp = np.array([-d_vec[1], d_vec[0]]) / d
    first = base + h * perp
    second = base - h * perp
    pick = first if ((first[1] > second[1]) == upper) else second
    return np.array([pick[0], pick[1], 0.0])


def compass_arc(centre, radius, start_deg, span_deg, color=CHALK_CYAN,
                width=2.6) -> Arc:
    """A compass arc: every point at `radius` from `centre`."""
    return Arc(radius=radius, start_angle=start_deg * DEGREES,
               angle=span_deg * DEGREES, arc_center=np.array(centre, dtype=float),
               color=color, stroke_width=width)


def locating_arc(centre, target, radius, spread=32, color=CHALK_CYAN) -> Arc:
    """The compass arc about `centre` that is *guaranteed* to pass through
    `target`.

    The sector is centred on the direction of the target, so the two arcs of
    the construction really do cross on the vertex they are locating.  An arc
    drawn in the wrong sector would sweep somewhere else entirely and the
    figure would show two arcs that never meet -- a construction that does
    not demonstrate what it claims."""
    ang = np.degrees(np.arctan2(target[1] - centre[1], target[0] - centre[0]))
    return compass_arc(centre, radius, ang - spread, 2 * spread, color)


COMPASS_STEEL = "#C2CCD4"      # the two legs
COMPASS_DARK = "#6E7A84"       # hinge / needle body
COMPASS_WOOD = "#E0A33C"       # pencil barrel
COMPASS_LEAD = "#2A2A2E"       # pencil graphite


def compass_tool(centre, pencil_at, away=None, hinge_dir=None,
                 leg_ratio=0.62) -> VGroup:
    """A pair of compasses with its needle on `centre` and its pencil tip on
    `pencil_at` — the tool that actually draws an arc.

    The hinge sits on the perpendicular bisector of the needle-pencil segment,
    on the side that points away from `away` (usually the figure's centre) so
    the body of the compass stays out of the drawing.  `leg_ratio` fixes the
    leg length as a fraction of the opening; a real compass drawing a wide arc
    is opened out like this."""
    O = np.array(centre, dtype=float)
    P = np.array(pencil_at, dtype=float)
    d = P - O
    r = float(np.linalg.norm(d[:2]))
    if r < 1e-3:
        return VGroup()
    u = d / r
    n = np.array([-u[1], u[0], 0.0])
    if hinge_dir is not None:
        hint = np.array(hinge_dir, dtype=float)
        if np.dot(n, hint) < 0:
            n = -n
    elif away is not None:
        # keep the hinge on the far side of the needle-pencil line
        if np.dot(n, np.array(away, dtype=float) - O) > 0:
            n = -n
    leg = leg_ratio * r
    h = float(np.sqrt(max(leg * leg - (r / 2.0) ** 2, 0.02)))
    H = (O + P) / 2.0 + n * h

    def metal(a, b, width=6.0):
        # a dark line under a steel-grey one: the same outlined look the
        # sticks and cards use, so the legs read as metal on the dark board
        return VGroup(
            Line(a, b, color="#242A30", stroke_width=width + 3.4),
            Line(a, b, color=COMPASS_STEEL, stroke_width=width),
        )

    legs = VGroup(metal(H, O), metal(H, P))
    hinge = VGroup(
        Circle(radius=0.09, stroke_color="#242A30", stroke_width=5.0,
               fill_color=COMPASS_DARK, fill_opacity=1.0).move_to(H),
        Circle(radius=0.060, stroke_color=COMPASS_STEEL, stroke_width=2.2,
               fill_color="#98A6B0", fill_opacity=1.0).move_to(H),
    )
    knob = metal(H, H + (O - H) / max(np.linalg.norm(O - H), 1e-3) * 0.24,
                 width=4.0)
    # the needle stands on the paper at the centre
    needle = Line(O, O + (H - O) / max(np.linalg.norm(H - O), 1e-3) * 0.13,
                  color="#242A30", stroke_width=3.6)
    needle_dot = Dot(radius=0.032, color="#242A30").move_to(O)
    # the pencil: barrel from the leg down to the tip, graphite at the end
    tip_dir = (P - H) / max(np.linalg.norm(P - H), 1e-3)
    barrel = VGroup(
        Line(P - tip_dir * 0.46, P - tip_dir * 0.07, color="#242A30",
             stroke_width=12.0),
        Line(P - tip_dir * 0.46, P - tip_dir * 0.07, color=COMPASS_WOOD,
             stroke_width=8.5),
    )
    lead = Line(P - tip_dir * 0.07, P, color=COMPASS_LEAD, stroke_width=6.0)
    return VGroup(legs, hinge, knob, needle, needle_dot, barrel, lead)


def compass_arc_drawer(centre, target, radius, spread, color,
                       away=None, hinge_dir=None, leg_ratio=0.62):
    """Return (arc, tool, sweep) for a compass drawing an arc of `radius`
    about `centre`, sweeping `2 * spread` degrees centred on `target`.

    Drive `sweep` from 0 to `2 * spread` with `sweep.animate.set_value(...)`:
    the arc grows behind the pencil tip and the compass rotates with it."""
    C = np.array(centre, dtype=float)
    ang = float(np.degrees(np.arctan2(target[1] - C[1], target[0] - C[0])))
    start = ang - spread
    sweep = ValueTracker(0.004)

    def tip_at():
        a = (start + sweep.get_value()) * DEGREES
        return C + radius * np.array([np.cos(a), np.sin(a), 0.0])

    arc = always_redraw(lambda: Arc(
        radius=radius, start_angle=start * DEGREES,
        angle=max(sweep.get_value(), 0.004) * DEGREES, arc_center=C,
        color=color, stroke_width=2.8))
    tool = always_redraw(lambda: compass_tool(
        C, tip_at(), away=away, hinge_dir=hinge_dir, leg_ratio=leg_ratio))
    return arc, tool, sweep


def radius_line(centre, point, color=CHALK_WHITE, label=None, size=15,
                dashed=True) -> VGroup:
    """The compass radius: a line from the centre out to the arc, optionally
    labelled with the radius that is set on the compass.

    The label is pushed out along the *perpendicular* to the radius, clear of
    the line by the label's own half-extent along that normal, so a wide label
    on a steep radius can never be clipped by its own line (a fixed vertical
    offset lands on the line whenever the radius is steep)."""
    maker = DashedLine if dashed else Line
    kwargs = {"dash_length": 0.1} if dashed else {}
    line = maker(np.array(centre, dtype=float), np.array(point, dtype=float),
                 color=color, stroke_width=1.7, **kwargs)
    if label is None:
        return VGroup(line)
    mid = (np.array(centre, dtype=float) + np.array(point, dtype=float)) / 2.0
    d = np.array(point, dtype=float) - np.array(centre, dtype=float)
    n = np.array([-d[1], d[0], 0.0])
    n = n / (np.linalg.norm(n[:2]) or 1.0)
    if n[1] < 0:                 # prefer the side above the radius
        n = -n
    lab = board_text(label, size, color, "BOLD")
    # clear the radius by the label's own half-extent along the normal, so a
    # wide label on a steep radius cannot be clipped by its own line
    half = (abs(n[0]) * lab.width + abs(n[1]) * lab.height) / 2.0
    lab.move_to(mid + n * (half + 0.13))
    return VGroup(line, lab)


def measure_card(label, color=CHALK_WHITE, size=18) -> VGroup:
    """One given measurement on a small card."""
    tex = MathTex(label, font_size=size, color=color)
    box = RoundedRectangle(corner_radius=0.08, width=tex.width + 0.46,
                           height=tex.height + 0.32, stroke_color=color,
                           stroke_width=1.8, fill_color="#16202B",
                           fill_opacity=0.8)
    tex.move_to(box.get_center())
    grp = VGroup(box, tex)
    grp.tex = tex
    return grp


def check_row(label, color=CHALK_GREEN, size=17) -> VGroup:
    """A verification row: a green tick plus the measurement it confirms."""
    mark = VGroup(
        Line(ORIGIN, np.array([0.09, -0.11, 0.0])),
        Line(np.array([0.09, -0.11, 0.0]), np.array([0.28, 0.17, 0.0])),
    ).set_stroke(color=color, width=4.0)
    txt = MathTex(label, font_size=size, color=CHALK_WHITE)
    return VGroup(mark, txt).arrange(RIGHT, buff=0.22)


def protractor(centre, color=CHALK_AMBER, radius=0.95) -> VGroup:
    """A semicircular protractor with 10-degree ticks: it is laid over the
    vertex while the given angle is set out, then taken away again."""
    body = Arc(radius=radius, start_angle=0.0, angle=180 * DEGREES,
               arc_center=np.array(centre, dtype=float), color=color,
               stroke_width=1.6, stroke_opacity=0.7)
    ticks = VGroup()
    for deg in range(0, 181, 10):
        a = deg * DEGREES
        direction = np.array([np.cos(a), np.sin(a), 0.0])
        outer = np.array(centre, dtype=float) + radius * direction
        inner = np.array(centre, dtype=float) + radius * 0.90 * direction
        ticks.add(Line(inner, outer, color=color, stroke_width=1.2,
                       stroke_opacity=0.65))
    return VGroup(body, ticks)


SCALE = 0.56            # board units per centimetre of the textbook drawing
AC_Y = 0.30             # the diagonal AC is drawn level, at this height


def triangle_apex(A, C, rA, rC, up=True):
    """The third vertex of a triangle whose other two vertices are A and C:
    the point at distance `rA` from A and `rC` from C, on the chosen side of
    the line A -> C.  This is exactly "intersect the two arcs"."""
    return circle_intersection(A, rA, C, rC, upper=up)


def example_frame(origin=None, scale=SCALE, base_y=None):
    """Textbook Example 3, built the way the construction builds it.

    A C = 5 cm is the diagonal, and it is the shared side of the two triangles:
    B is the point with A B = 4 cm and B C = 3.6 cm above the diagonal, and D
    is the point with A D = 4.8 cm and C D = 4.2 cm below it -- the textbook
    places the fourth vertex on the other side of the diagonal."""
    if origin is None:
        y = AC_Y if base_y is None else base_y
        origin = np.array([BOARD_CX - 1.4, y, 0.0])
    A = np.array(origin, dtype=float)
    C = A + np.array([5.0 * scale, 0.0, 0.0])
    B = triangle_apex(A, C, 4.0 * scale, 3.6 * scale, up=True)
    D = triangle_apex(A, C, 4.8 * scale, 4.2 * scale, up=False)
    return A, B, C, D


def practice_frame(origin=None, scale=0.40, base_y=None):
    """The practice set used for the challenge: P R = 5.5 is the diagonal,
    P Q = 4 and Q R = 3 above it, P S = 4.5 and R S = 5 below it."""
    if origin is None:
        y = AC_Y if base_y is None else base_y
        origin = np.array([BOARD_CX - 3.0, y, 0.0])
    P = np.array(origin, dtype=float)
    R = P + np.array([5.5 * scale, 0.0, 0.0])
    Q = triangle_apex(P, R, 4.0 * scale, 3.0 * scale, up=True)
    S = triangle_apex(P, R, 4.5 * scale, 5.0 * scale, up=False)
    return P, Q, R, S


def diamond_names(left, top, right, bottom, letters="ABCD", size=17,
                  color=CHALK_WHITE, pull=0.0) -> VGroup:
    """Vertex letters for this video's quadrilateral.

    The diagonal is drawn level, so the figure has one vertex on the left, one
    at the top, one on the right and one at the bottom, and each letter goes to
    the corner that is actually free.  The series' default quad-sides put the
    top vertex's letter down-right and the bottom vertex's letter up-left, which
    here would land them on the figure's own sides; and the bottom vertex is
    where the two locating arcs cross, so its letter is pushed out to the
    down-right, clear of both arcs (measured clearance 0.10-0.38)."""
    def place(letter, point, side, extra=None):
        lab = vertex_label(letter, point, side, color, size)
        if extra is not None:
            lab.shift(extra)
        if pull:
            # the small recap figures need the letter nearer its corner: the
            # fixed 0.10 offset is a large fraction of a 2-unit figure
            d = np.array(point, dtype=float) - lab.get_center()
            n = float(np.linalg.norm(d[:2]))
            if n > 1e-6:
                lab.shift(d / n * min(pull, max(n - 0.02, 0.0)))
        return lab

    return VGroup(place(letters[0], left, "UL"),
                  place(letters[1], top, "UR"),
                  place(letters[2], right, "UR"),
                  place(letters[3], bottom, "DR",
                        np.array([0.14, -0.20, 0.0])))


def vertex_label(letter, point, side="DL", color=CHALK_WHITE,
                 size=18) -> Text:
    """A vertex letter placed clear of its corner."""
    corner = {"DL": DL, "DR": DR, "UR": UR, "UL": UL}[side]
    return board_text(letter, size, color, "BOLD").next_to(
        np.array(point, dtype=float), corner, buff=0.10)


def quad_names(points, letters="PQRS", size=18, color=CHALK_WHITE) -> VGroup:
    """The four vertex letters, each outside its own corner."""
    sides = ("DL", "DR", "UR", "UL")
    return VGroup(*[vertex_label(letter, point, side, color, size)
                    for letter, point, side in zip(letters, points, sides)])


# (this section is spliced into a head whose own imports omit Ellipse and Arc;
#  Dot, Circle, Line, DashedLine, Polygon, Rectangle, RoundedRectangle, Square,
#  VGroup, DEGREES and np are already imported by the head)
from manim import Arc, Ellipse  # noqa: E402,F401

# Board layout shared by every scene of this video.
ROW_Y = 2.72             # every scene heading sits on this line
SUB_Y = 2.16             # the one-line sub-heading under it
BANNER_Y = -1.15         # the closing banner, above the strip
# The burned-in caption grows up from the bottom of the frame: a one-line cue
# starts at y = -3.38 and a wrapped two-line cue reaches y = -2.93 (measured on
# the series' own burned 360p cuts), so every closing strip sits at -1.80 and
# nothing at all sits below CAPTION_SAFE_Y = -2.00 -- audited by the
# IN-CAPTION-BAND check.
STRIP_Y = -1.80
CAPTION_SAFE_Y = -2.00

# The three content lines.  PANEL_Y carries the percentage control panel, which
# stays on the board in every teaching scene; ROW_A holds the diagram, ROW_B the
# numbers under it and ROW_C the rule chip above the banner.  The rows are set
# so that no two texts come within the 0.22 units the clearance audit asks for,
# including the banner text sitting at -1.15.
PANEL_Y = 1.52
ROW_A = 0.88
ROW_B = 0.02
ROW_C = -0.60

PANEL_FILL = "#16202B"
MODE_W = 1.58            # one control-panel mode chip
MODE_H = 0.44
CHIP_H = 0.50
CARD_W = 3.30
CARD_H = 0.94
MARK_SIZE = 18
DOT_R = 0.075
COIN_R = 0.17

# The figures this video works with.  The bill is the series' own estimation
# example: it rounds to a number that is easier without changing much.
GROUP_A = ("Group A", 225, 300, CHALK_GREEN)
GROUP_B = ("Group B", 200, 250, CHALK_CYAN)
SALES = "Rs 98,700"
BILL = 477.80
ROUNDED_BILL = 480.0

# The miniature number line the bill snaps along (470 ... 490).
NL_LO, NL_HI = 470.0, 490.0
NL_W = 4.60
NL_Y = 0.95
MODES = (("CONVERT", CHALK_GREEN), ("CHANGE", CHALK_AMBER),
         ("ESTIMATE", CHALK_CYAN))


# ---------------------------------------------------------------- furniture --
def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


def write_board_file(path, text: str) -> None:
    """Write a board artefact (the ground-truth SRT), surviving Windows' limit.

    This topic's media folder is 211 characters deep and `<Class>.real.srt`
    pushes the full name to exactly 260 -- one over what a plain open accepts on
    a machine whose long-path support is off (measured here:
    LongPathsEnabled = 0).  The write therefore falls back to the `\\\\?\\` form,
    which the OS always accepts.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        path.write_text(text, encoding="utf-8")
    except OSError:
        with open("\\\\?\\" + str(path.resolve()), "w",
                  encoding="utf-8") as handle:
            handle.write(text)


def row_centres(half_widths, gap, cx=BOARD_CX):
    """x centres for a row of elements whose ink is `gap` apart.

    The row's combined ink is centred on `cx` (the green board's centre line) and
    the elements of a row are not equally wide, so equal centre spacing is NOT
    equal spacing on the board: this returns the centres that leave exactly `gap`
    units of clear air between neighbours.
    """
    total = 2.0 * sum(half_widths) + gap * (len(half_widths) - 1)
    x = cx - total / 2.0
    centres = []
    for half in half_widths:
        centres.append(x + half)
        x += 2.0 * half + gap
    return tuple(centres)


def panel(width, height, color=CHALK_WHITE, opacity=0.6, radius=0.10,
          stroke=1.9):
    """A rounded panel: the box every card and chip is drawn on."""
    return RoundedRectangle(corner_radius=radius, width=width, height=height,
                            stroke_color=color, stroke_width=stroke,
                            fill_color=PANEL_FILL, fill_opacity=opacity)


def chip(text, color=CHALK_CYAN, size=15, width=None, height=CHIP_H,
         fill=PANEL_FILL):
    """A small labelled chip."""
    lab = board_text(text, size, color, "BOLD")
    box = RoundedRectangle(corner_radius=0.09,
                           width=width or (lab.width + 0.40), height=height,
                           stroke_color=color, stroke_width=1.7,
                           fill_color=fill, fill_opacity=0.7)
    lab.move_to(box.get_center())
    grp = VGroup(box, lab)
    grp.box, grp.label = box, lab
    return grp


def mode_panel(active="CONVERT"):
    """The percentage control panel: three modes, the live one lit.

    It sits on the same line of the board in every teaching scene, so the
    viewer always knows which of the three moves the board is on.  The inactive
    modes stay visible but dimmed -- they are furniture, never a surprise.
    """
    row = VGroup()
    for name, color in MODES:
        lit = active in (name, "ALL")
        c = chip(name, color if lit else CHALK_WHITE, size=13, width=MODE_W,
                 height=MODE_H)
        if not lit:
            c.set_opacity(0.40)
        row.add(c)
    row.arrange(RIGHT, buff=0.26)
    return at(row, BOARD_CX, PANEL_Y)


def percent_grid(fill_n, color=CHALK_GREEN, cell=0.100, gap=0.012,
                 rows=10, cols=10):
    """The hundred-cell percentage square: `fill_n` cells lit, the rest waiting.

    The cells are lit one at a time (the caller runs a LaggedStart over
    `grp.lit`), so "75 out of 100" is something the viewer watches happen rather
    than a number that is simply asserted.
    """
    step = cell + gap
    cells, lit = VGroup(), VGroup()
    for i in range(rows * cols):
        r, c = divmod(i, cols)
        sq = Square(side_length=cell, stroke_color=CHALK_WHITE,
                    stroke_width=0.8, fill_color=color, fill_opacity=0.06)
        sq.set_stroke(opacity=0.40)
        sq.move_to(np.array([(c - (cols - 1) / 2.0) * step,
                             ((rows - 1) / 2.0 - r) * step, 0.0]))
        cells.add(sq)
        if i < fill_n:
            lit.add(sq)
    grp = VGroup(cells)
    grp.cells, grp.lit = cells, lit
    return grp


def pct_bar(width=2.20, height=0.50, color=CHALK_GREEN,
            label="100% ORIGINAL", size=14):
    """The whole, drawn as one bar: every change is measured from this."""
    box = RoundedRectangle(corner_radius=0.05, width=width, height=height,
                           stroke_color=color, stroke_width=2.0,
                           fill_color=color, fill_opacity=0.22)
    grp = VGroup(box)
    grp.box = box
    if label:
        lab = board_text(label, size, CHALK_WHITE, "BOLD")
        lab.move_to(box.get_center())
        grp.add(lab)
        grp.label = lab
    return grp


def pct_block(width, height=0.50, color=CHALK_AMBER, label=None, size=13):
    """One coloured block: the piece that attaches (or leaves) the 100% bar."""
    box = Rectangle(width=width, height=height, stroke_color=color,
                    stroke_width=2.2, fill_color=color, fill_opacity=0.34)
    grp = VGroup(box)
    grp.box = box
    if label:
        lab = board_text(label, size, CHALK_WHITE, "BOLD")
        lab.move_to(box.get_center())
        grp.add(lab)
        grp.label = lab
    return grp


def decade_row(n=10, cell=0.26, gap=0.03, color=CHALK_CYAN, height=0.52):
    """Ten equal blocks: one block is one tenth, so the row is the whole 100%.

    A decrease is drawn by letting the last block detach and leave, which is
    visibly the opposite of the block that attaches for an increase.
    """
    row = VGroup()
    for _ in range(n):
        row.add(Rectangle(width=cell, height=height, stroke_color=color,
                          stroke_width=1.6, fill_color=color,
                          fill_opacity=0.30))
    row.arrange(RIGHT, buff=gap)
    row.cell_w = cell
    return row


def split_block(width=1.20, height=0.54, color=CHALK_AMBER):
    """One ten-percent block that halves into two five-percent blocks.

    Both halves, their labels and the divider live in ONE VGroup, so the halves
    can slide apart without their wording being left behind.
    """
    half = (width - 0.06) / 2.0
    boxes = VGroup(
        Rectangle(width=half, height=height, stroke_color=color,
                  stroke_width=2.0, fill_color=color, fill_opacity=0.32),
        Rectangle(width=half, height=height, stroke_color=color,
                  stroke_width=2.0, fill_color=color, fill_opacity=0.32),
    ).arrange(RIGHT, buff=0.06)
    left = VGroup(boxes[0],
                  board_text("5%", 13, CHALK_WHITE, "BOLD"
                             ).move_to(boxes[0].get_center()))
    right = VGroup(boxes[1],
                   board_text("5%", 13, CHALK_WHITE, "BOLD"
                              ).move_to(boxes[1].get_center()))
    grp = VGroup(left, right)
    grp.half_l, grp.half_r = left, right
    return grp


def money_note(width=1.70, height=0.80, color=CHALK_GREEN,
               text="Rs 34,545", size=13):
    """A drawn rupee note: a filled, shaded rectangle with a printed frame."""
    body = RoundedRectangle(corner_radius=0.06, width=width, height=height,
                            stroke_color=color, stroke_width=2.2,
                            fill_color=color, fill_opacity=0.24)
    inner = RoundedRectangle(corner_radius=0.04, width=width - 0.22,
                             height=height - 0.22, stroke_color=color,
                             stroke_width=1.1, fill_color=color,
                             fill_opacity=0.10)
    inner.set_stroke(opacity=0.6)
    inner.move_to(body.get_center())
    lab = board_text(text, size, CHALK_WHITE, "BOLD").move_to(body.get_center())
    grp = VGroup(body, inner, lab)
    grp.box, grp.label = body, lab
    return grp


def coin_stack(cx, cy, n=3, scale=1.0, color=CHALK_YELLOW):
    """A stack of coins: filled discs with thickness, drawn bottom-up."""
    discs = VGroup()
    for i in range(n):
        e = Ellipse(width=0.46 * scale, height=0.16 * scale,
                    stroke_color=color, stroke_width=1.5,
                    fill_color=color, fill_opacity=0.38)
        e.move_to(np.array([cx, cy + 0.075 * i * scale, 0.0]))
        discs.add(e)
    return discs


def money_bag(cx, cy, scale=1.0, color=CHALK_AMBER, text="SALES",
              size=15, coins=True):
    """The money bag: a filled, shaded bag with a tied neck (and coins)."""
    body = Ellipse(width=0.94 * scale, height=0.78 * scale, stroke_color=color,
                   stroke_width=2.6, fill_color=color, fill_opacity=0.24)
    body.move_to(np.array([cx, cy - 0.12 * scale, 0.0]))
    neck = Polygon(np.array([cx - 0.19 * scale, cy + 0.16 * scale, 0.0]),
                   np.array([cx + 0.19 * scale, cy + 0.16 * scale, 0.0]),
                   np.array([cx + 0.30 * scale, cy - 0.04 * scale, 0.0]),
                   np.array([cx - 0.30 * scale, cy - 0.04 * scale, 0.0]),
                   stroke_color=color, stroke_width=2.2,
                   fill_color=color, fill_opacity=0.24)
    tie = Line(np.array([cx - 0.30 * scale, cy + 0.15 * scale, 0.0]),
               np.array([cx + 0.30 * scale, cy + 0.15 * scale, 0.0]),
               stroke_color=CHALK_RED, stroke_width=3.4)
    # the label sits clear of the bag's own neck, so the audit's polygon
    # clearance check stays green
    lab = board_text(text, size, CHALK_WHITE, "BOLD")
    lab.move_to(np.array([cx, cy - 0.30 * scale, 0.0]))
    grp = VGroup(body, neck, tie, lab)
    grp.label = lab
    if coins:
        grp.add(coin_stack(cx - 0.60 * scale, cy - 0.44 * scale, 3, scale))
        grp.add(coin_stack(cx + 0.60 * scale, cy - 0.44 * scale, 3, scale))
    return grp


def price_tag(width=2.30, height=0.86, color=CHALK_PINK, text="Rs 550",
              size=15):
    """A shop price tag: a filled tag shape, a punched hole and a string."""
    tip = height * 0.5
    body = Polygon(
        np.array([-width / 2, height / 2, 0.0]),
        np.array([width / 2 - tip, height / 2, 0.0]),
        np.array([width / 2, 0.0, 0.0]),
        np.array([width / 2 - tip, -height / 2, 0.0]),
        np.array([-width / 2, -height / 2, 0.0]),
        stroke_color=color, stroke_width=2.4, fill_color=color,
        fill_opacity=0.24)
    hole = Circle(radius=0.072, stroke_color=color, stroke_width=1.6,
                  fill_color=PANEL_FILL, fill_opacity=0.9)
    hole.move_to(np.array([-width / 2 + 0.20, 0.0, 0.0]))
    loop = Arc(radius=0.16, start_angle=150 * DEGREES, angle=120 * DEGREES,
               arc_center=np.array([-width / 2 + 0.02, 0.22, 0.0]),
               stroke_color=CHALK_WHITE, stroke_width=1.8)
    lab = board_text(text, size, CHALK_WHITE, "BOLD")
    lab.move_to(np.array([-width / 2 + 0.34 + (width - tip - 0.40) / 2.0,
                          0.0, 0.0]))
    grp = VGroup(body, hole, loop, lab)
    grp.body, grp.label = body, lab
    return grp


def receipt(width=1.70, height=1.00, color=CHALK_CYAN, head="BILL",
            value="Rs 477.80"):
    """The bill itself: a filled slip with a heading and the amount on it.

    The ruled lines are thin filled bars rather than strokes, so no line ever
    runs through the lettering.
    """
    body = RoundedRectangle(corner_radius=0.06, width=width, height=height,
                            stroke_color=color, stroke_width=2.2,
                            fill_color=color, fill_opacity=0.18)
    h = board_text(head, 13, color, "BOLD")
    h.move_to(body.get_center() + UP * 0.30)
    v = board_text(value, 13, CHALK_WHITE, "BOLD")
    v.move_to(body.get_center() + DOWN * 0.26)
    bars = VGroup()
    for yy in (0.10, 0.02):
        b = Rectangle(width=width - 0.46, height=0.035, stroke_width=0,
                      fill_color=CHALK_WHITE, fill_opacity=0.35)
        b.move_to(body.get_center() + UP * yy)
        bars.add(b)
    grp = VGroup(body, bars, h, v)
    grp.box, grp.head, grp.value = body, h, v
    return grp


def nl_x(value):
    """The board x of a number on the ruler."""
    mid = (NL_LO + NL_HI) / 2.0
    return BOARD_CX + (float(value) - mid) / (NL_HI - NL_LO) * NL_W


def number_ruler(lo=NL_LO, hi=NL_HI, y=NL_Y, width=NL_W, step=5,
                 color=CHALK_WHITE, size=13):
    """The ruler the bill snaps along: a bar with a tick and a label each step."""
    axis = Line(np.array([BOARD_CX - width / 2, y, 0.0]),
                np.array([BOARD_CX + width / 2, y, 0.0]),
                stroke_color=color, stroke_width=2.2)
    ticks, labels = VGroup(), VGroup()
    v = lo
    while v <= hi + 1e-6:
        x = nl_x(v)
        ticks.add(Line(np.array([x, y, 0.0]), np.array([x, y - 0.14, 0.0]),
                       stroke_color=color, stroke_width=1.8))
        lab = board_text(f"{int(v)}", size, color, "BOLD")
        lab.move_to(np.array([x, y - 0.34, 0.0]))
        labels.add(lab)
        v += step
    grp = VGroup(axis, ticks, labels)
    grp.axis, grp.ticks, grp.labels = axis, ticks, labels
    return grp


def note_card(head, lines, color=CHALK_CYAN, width=3.40, height=1.05,
              head_size=15, line_size=13):
    """A card with a bold head line and one or two body lines under it.

    The head and the body are held 0.26 units apart, so the pair passes the
    clearance audit (which flags any two texts closer than 0.22).
    """
    box = panel(width, height, color)
    h = board_text(head, head_size, color, "BOLD")
    body = VGroup(*[board_text(line, line_size, CHALK_WHITE, "BOLD")
                    for line in lines]).arrange(DOWN, buff=0.24)
    h.move_to(box.get_center() + UP * 0.26)
    body.move_to(box.get_center() + DOWN * 0.26)
    grp = VGroup(box, h, body)
    grp.box, grp.head, grp.body = box, h, body
    return grp


def cross_out(mob, color=CHALK_RED, pad=0.10):
    """A drawn cross over a mobject (Segoe Print has no cross glyph)."""
    x0, y0 = mob.get_left()[0] - pad, mob.get_bottom()[1] - pad
    x1, y1 = mob.get_right()[0] + pad, mob.get_top()[1] + pad
    return VGroup(
        Line(np.array([x0, y0, 0.0]), np.array([x1, y1, 0.0]),
             stroke_color=color, stroke_width=4.2),
        Line(np.array([x0, y1, 0.0]), np.array([x1, y0, 0.0]),
             stroke_color=color, stroke_width=4.2))


def wrong_card(text, color=CHALK_RED, width=2.30, height=0.85, size=13):
    """A card holding a WRONG statement, with a drawn cross over it.

    The cross occupies the card's top half and the statement its bottom half, so
    the strike-through is unmistakable yet never comes within the 0.04 units the
    audit allows between a stroke and the lettering.  The whole card is ONE
    board object, so the strokes are never read as a line running into a box.
    """
    box = panel(width, height, color, opacity=0.7)
    cross = VGroup(
        Line(np.array([-width / 2 + 0.45, 0.10, 0.0]),
             np.array([-width / 2 + 0.90, 0.38, 0.0]),
             stroke_color=color, stroke_width=4.2),
        Line(np.array([-width / 2 + 0.45, 0.38, 0.0]),
             np.array([-width / 2 + 0.90, 0.10, 0.0]),
             stroke_color=color, stroke_width=4.2),
    )
    cross.move_to(box.get_center() + UP * (height / 2 - 0.24))
    cross.shift(RIGHT * 0.10)
    lab = board_text(text, size, color, "BOLD")
    lab.move_to(box.get_center() + DOWN * (height / 2 - 0.22))
    grp = VGroup(box, cross, lab)
    grp.box, grp.cross, grp.label = box, cross, lab
    return grp


def tick(p, color=CHALK_GREEN, s=0.16):
    """A drawn tick (Segoe Print has no tick glyph)."""
    a = np.array([p[0] - s * 0.60, p[1] + s * 0.05, 0.0])
    b = np.array([p[0] - s * 0.05, p[1] - s * 0.55, 0.0])
    c = np.array([p[0] + s * 0.65, p[1] + s * 0.75, 0.0])
    return VGroup(Line(a, b, stroke_color=color, stroke_width=3.4),
                  Line(b, c, stroke_color=color, stroke_width=3.4))


def arrow_between(p1, p2, color=CHALK_YELLOW, width=3.0, tip=0.20):
    """A short arrow from one board point to another."""
    return Arrow(np.array([p1[0], p1[1], 0.0]), np.array([p2[0], p2[1], 0.0]),
                 buff=0.0, stroke_color=color, stroke_width=width,
                 tip_length=tip, max_tip_length_to_length_ratio=0.35)


# ----------------------------------------------------------------


NARRATION = {
    "title": (
        "Suppose two school groups are selling tickets for the annual function. "
        "<bookmark mark='b0'/>Group A sold 225 tickets out of 300. <bookmark "
        "mark='b1'/>Group B sold 200 tickets out of 250. <bookmark mark='b2'/>"
        "The two totals are different, so the numbers 225 and 200 cannot be "
        "compared directly. <bookmark mark='b3'/>Who actually did better? "
        "<bookmark mark='b4'/>A percentage puts different totals onto one "
        "common scale, and that scale is always out of one hundred."
    ),
    "s1": (
        "Now let us convert both groups to one common scale. <bookmark "
        "mark='b0'/>Both 225 out of 300 and 200 out of 250 can be written as "
        "fractions. 225 out of 300 is 3 over 4, which is 75 out of 100, so that "
        "is 75 percent. <bookmark mark='b1'/>200 out of 250 is 4 over 5, which "
        "is 80 out of 100, so that is 80 percent. <bookmark mark='b2'/>So group "
        "B is closer to the target. <bookmark mark='b3'/>The rule is: "
        "percentage equals part divided by whole, multiplied by one hundred. "
        "<bookmark mark='b4'/>And always name the whole, because the percentage "
        "is measured from that reference."
    ),
    "s2": (
        "Now think about a change. <bookmark mark='b0'/>Suppose a value grows "
        "by 35 percent. Start with the original value drawn as a full bar of "
        "one hundred percent. <bookmark mark='b1'/>A 35 percent increase "
        "attaches one more block to that bar. <bookmark mark='b2'/>The original "
        "hundred percent and the new thirty five percent together make one "
        "hundred and thirty five percent. <bookmark mark='b3'/>So a 35 percent "
        "increase means the new value is 135 percent of the original. <bookmark "
        "mark='b4'/>The increase is always measured from the original, never "
        "from the new value."
    ),
    "s3": (
        "Let us apply that to money. <bookmark mark='b0'/>Last month the sales "
        "were Rs 98,700. <bookmark mark='b1'/>This month they are up by 35 "
        "percent. <bookmark mark='b2'/>First find the increase: 35 over 100 "
        "times 98,700 is Rs 34,545. <bookmark mark='b3'/>Then add it to the "
        "original: 98,700 plus 34,545 gives Rs 1,33,245. <bookmark mark='b4'/>"
        "Here is the shortcut: 135 percent of 98,700 is the same Rs 1,33,245, "
        "because the new value is 135 percent of the old one."
    ),
    "s4": (
        "Now the other direction. <bookmark mark='b0'/>A price tag shows "
        "Rs 550, and the shop offers 10 percent off. <bookmark mark='b1'/>Ten "
        "percent of 550 is Rs 55. <bookmark mark='b2'/>Take it away: 550 minus "
        "55 is Rs 495, and that is what you pay. <bookmark mark='b3'/>Now "
        "compare the two changes on one panel. An increase of p percent gives "
        "100 percent plus p percent. <bookmark mark='b4'/>A decrease of p "
        "percent gives 100 percent minus p percent, so 10 percent off leaves 90 "
        "percent."
    ),
    "s5": (
        "Here is the mental toolkit. <bookmark mark='b0'/>Ten percent is one "
        "tenth, so move the decimal point one place. <bookmark mark='b1'/>Five "
        "percent is half of ten percent. <bookmark mark='b2'/>Fifteen percent "
        "is ten percent plus five percent, and twenty percent is simply two "
        "tens. <bookmark mark='b3'/>A common mistake is to say that five percent "
        "is half of twenty percent; the cross shows that this is wrong. "
        "<bookmark mark='b4'/>Now use 480: ten percent is 48, five percent is "
        "24, so fifteen percent is 72. Build hard percentages out of ten "
        "percent."
    ),
    "s6": (
        "Now use that on a bill. <bookmark mark='b0'/>The bill is Rs 477.80, "
        "which is awkward, so round it to Rs 480. <bookmark mark='b1'/>Ten "
        "percent of 480 is 48. <bookmark mark='b2'/>Five percent is half of "
        "that, so 24, and fifteen percent is 48 plus 24, that is 72. <bookmark "
        "mark='b3'/>Subtract that from the rounded bill: 480 minus 72 is 408. "
        "<bookmark mark='b4'/>So you pay about Rs 410, and the approximation "
        "sign stays on the board, because this is an estimate."
    ),
    "s7": (
        "Let us put the two lanes side by side. <bookmark mark='b0'/>The exact "
        "lane works with the real bill: fifteen percent of 477.80 is Rs 71.67, "
        "and 477.80 minus 71.67 is 406.13. <bookmark mark='b1'/>The mental lane "
        "rounded the bill to 480 and used 72, which gave about 408, or about "
        "410. <bookmark mark='b2'/>The two answers are close, so the estimate "
        "is sensible. <bookmark mark='b3'/>Remember: an estimate is a "
        "reasonableness check, not exact arithmetic. <bookmark mark='b4'/>The "
        "exact lane is only there to show that the quick answer is believable."
    ),
    "s8": (
        "So here is the decision map. <bookmark mark='b0'/>To convert, divide "
        "the part by the whole and multiply by one hundred. <bookmark "
        "mark='b1'/>To handle an increase, add the percentage to one hundred. "
        "<bookmark mark='b2'/>To handle a decrease, subtract it from one "
        "hundred. <bookmark mark='b3'/>To estimate, round the number first, and "
        "then build the percentage from ten percent. <bookmark mark='b4'/>Four "
        "moves: convert, change, estimate, and check."
    ),
    "s9q": (
        "Your turn. Four quick checks. <bookmark mark='b0'/>A: convert 18 out "
        "of 24 into a percentage. <bookmark mark='b1'/>B: find the price of an "
        "item marked Rs 800 with 10 percent off. <bookmark mark='b2'/>C: "
        "estimate 20 percent of Rs 357.30 by first rounding it to 360. "
        "<bookmark mark='b3'/>D: increase Rs 900 by 35 percent. Now pause the "
        "video, work all four out on paper, and then we will check every "
        "answer."
    ),
    "s9a": (
        "Let us check every answer. <bookmark mark='b0'/>A: 18 out of 24 is "
        "three quarters, so it is 75 percent. <bookmark mark='b1'/>B: ten "
        "percent of 800 is 80, so 800 minus 80 is Rs 720. <bookmark "
        "mark='b2'/>C: twenty percent of 360 is two tens of 36, which is 36 "
        "plus 36, so it is about Rs 72. <bookmark mark='b3'/>D: 135 percent of "
        "900 is Rs 1,215, because 900 plus 315 gives 1,215. Every answer used "
        "the whole as its base."
    ),
    "s10": (
        "Let us put it together. <bookmark mark='b0'/>One: compare, because a "
        "percentage is always out of one hundred. <bookmark mark='b1'/>Two: "
        "change, where an increase adds to one hundred percent and a decrease "
        "subtracts from it. <bookmark mark='b2'/>Three: estimate, by rounding "
        "first and then building the percentage from ten percent. <bookmark "
        "mark='b3'/>Four: check, because an estimate is a reasonableness check "
        "and not exact arithmetic. <bookmark mark='b4'/>Compare, change, "
        "estimate, check. <bookmark mark='b5'/>Thank you for watching, "
        "<bookmark mark='b6'/>and see you in the next lesson."
    ),
}


class PercentageApplicationsAndEstimationStory(VoiceoverScene):
    """Story-mode chalkboard lesson: why four side measurements are not
    enough, and how a fifth independent measurement makes a quadrilateral
    unique (Class 8, Chapter 3: Construction of Quadrilaterals)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._srt_entries: list[tuple[float, float, str]] = []

    # -- backdrop (mirrors every Story-Mode video) -------------------------
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
            -config.frame_height / 2 + student.height / 2 - 0.1,
            0,
        ]))

        teacher = ImageMobject(str(assets_dir / "teacher.png"))
        teacher.set_z_index(-5)
        teacher.height = 3.3
        teacher.move_to(np.array([
            config.frame_width / 2 - teacher.width / 2 + 0.45,
            -config.frame_height / 2 + teacher.height / 2 - 0.1,
            0,
        ]))

        self.bg = bg
        self.student = student
        self.teacher = teacher

        # Both corner badges share the same chalk-stamped ribbon style and
        # are rendered at font_size=12 then scaled up (manim/Pango shows
        # per-glyph spacing artifacts in this font at small sizes above 12;
        # scaling the finished badge is artifact-free). Left = dhimantAI
        # brand badge (no topic label), right = Mathematics -- matches the
        # rest of the Story-Mode series.
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
            corner_radius=0.04, width=label.width + 0.24, height=label.height + 0.16,
            stroke_color=CHALK_AMBER, stroke_width=1.5,
            fill_color="#2A1D10", fill_opacity=0.45,
        )
        label.move_to(frame.get_center())
        badge = VGroup(frame, label)
        badge.scale(scale)

        yy = BOARD_TOP - 0.32 if y is None else y
        if corner == "left":
            badge.move_to(np.array([BOARD_LEFT + 0.55, yy, 0]))
            badge.shift(RIGHT * (BOARD_LEFT + 0.08 - badge.get_left()[0]))
        else:
            badge.move_to(np.array([BOARD_RIGHT - 0.6, yy, 0]))
            # Right margin is smaller than the left corner's 0.08 to
            # compensate for the background art's perspective (same fix as
            # the rest of the Story-Mode series).
            badge.shift(RIGHT * (BOARD_RIGHT - 0.013 - badge.get_right()[0]))
        # Snap the TOP edge to the same 0.08 margin used horizontally, so
        # both badges sit with equal spacing from the board's edges.
        badge.shift(UP * ((BOARD_TOP - 0.08) - badge.get_top()[1]))
        return badge

    def reset_board(self) -> None:
        self.clear()
        self.add(self.bg, self.student, self.teacher, self.badge, self.badge_l)

    def appear(self, mob, tracker, mark: str, run_time: float = 0.45,
               shift=UP * 0.06) -> None:
        """Bring text, a card or a label on screen crisply, then hold for the
        rest of the narration window.

        Text spread across a whole window sits half-transparent for seconds: a
        heading then reads as truncated lettering and a measurement card reads
        as an empty box.  Diagram work can be paced across the window, words
        cannot -- so the entrance is short and the board then holds, which is
        also what the narration is describing."""
        budget = leftover(tracker, mark)
        self.play(FadeIn(mob, shift=shift),
                  run_time=min(run_time, max(budget, 0.05)))
        self.wait(leftover(tracker, mark))

    def draw_with_compass(self, centre, target, radius, spread, color,
                          tracker, mark: str, away=None, hinge_dir=None,
                          leg_ratio=0.62, fade_tool: bool = True) -> None:
        """Draw one arc the way it is drawn on paper: a pair of compasses, its
        needle on `centre` and its pencil tracing the arc."""
        arc, tool, sweep = compass_arc_drawer(
            centre, target, radius, spread, color, away=away,
            hinge_dir=hinge_dir, leg_ratio=leg_ratio)
        self.add(arc, tool)
        # the pencil sweeps for the rest of the window, and putting the
        # compass back down afterwards stays inside that window
        budget = leftover(tracker, mark)
        sweep_time = max(budget - (0.35 if fade_tool else 0.0), 0.4)
        self.play(sweep.animate.set_value(2 * spread), run_time=sweep_time)
        if fade_tool:
            self.play(FadeOut(tool), run_time=0.3)
        self.wait(leftover(tracker, mark))
        self.arc = arc
        self.tool = tool

    # -- real SRT export ---------------------------------------------------
    def _capture_srt(self, tracker, words_per_line: int = 9) -> None:
        """Ground-truth export, with one change: a final chunk of one or two
        words is folded into the caption before it.  A stand-alone last word
        keeps its own half-second caption, which lands mostly in silence at the
        end of the piece and reads badly."""
        wbs = [wb for wb in tracker.data.get("word_boundaries", [])
               if wb.get("text", "").strip()]
        if not wbs:
            return
        starts = [tracker.start_t + wb["audio_offset"] / AUDIO_OFFSET_RESOLUTION
                  for wb in wbs]
        chunks = []
        for i in range(0, len(wbs), words_per_line):
            chunk = wbs[i:i + words_per_line]
            end = starts[i + words_per_line] if i + words_per_line < len(starts) \
                else tracker.end_t
            chunks.append([starts[i], end, list(chunk)])
        if len(chunks) > 1 and len(chunks[-1][2]) <= 2:
            tail = chunks.pop()
            chunks[-1][1] = tail[1]
            chunks[-1][2].extend(tail[2])
        for start, end, chunk in chunks:
            text = " ".join(wb["text"] for wb in chunk)
            self._srt_entries.append((start, end, text))

    def _write_real_srt(self) -> None:
        out_dir = _HERE / "media" / "videos" / "percentage_applications_and_estimation"
        out_dir.mkdir(parents=True, exist_ok=True)
        srt_path = out_dir / f"{self.__class__.__name__}.real.srt"

        def fmt(t: float) -> str:
            # carry-safe: rounding must never produce ",1000" (4-digit ms),
            # which is an invalid SRT timestamp that caption parsers drop.
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
        write_board_file(srt_path, "\n".join(lines))
        print(f"[real SRT written] {srt_path}")
        write_board_file(out_dir / "real.srt", "\n".join(lines))
        try:
            if (hasattr(self, "renderer") and hasattr(self.renderer, "file_writer")
                    and self.renderer.file_writer.movie_file_path):
                movie_dir = Path(self.renderer.file_writer.movie_file_path).parent
                write_board_file(movie_dir / "real.srt", "\n".join(lines))
                write_board_file(
                    movie_dir / f"{self.__class__.__name__}.real.srt",
                    "\n".join(lines))
        except Exception:
            pass



    def construct(self):
        self.sfx = load_sfx()
        self.set_speech_service(get_speech_service(), create_subcaption=False)
        install_synced_voiceover(self)

        self.add_background()

        self.beat_title()
        self.beat_s1()
        self.beat_s2()
        self.beat_s3()
        self.beat_s4()
        self.beat_s5()
        self.beat_s6()
        self.beat_s7()
        self.beat_s8()
        self.beat_s9()
        self.beat_s10()

        self._write_real_srt()

    # ================================================================ beats ==
    # Percentage Increases, Decreases & Quick Estimation Rules on Bills
    # (Class 8 Maths, Chapter 5, Storymode 02).
    #
    # SYNC RULE for every reveal: wait for the narration bookmark that ends the
    # phrase describing a thing, and only then bring it on.  Playing first and
    # waiting afterwards shows the picture a whole window early, which reads as
    # broken sync.
    #
    # Layout rules, so the audits stay clean:
    #   * the heading sits on the board's own heading line (2.72) and its
    #     sub-heading at 2.16, the closing banner at -1.15 and the closing strip
    #     at -1.80 -- nothing at all below CAPTION_SAFE_Y = -2.00;
    #   * the percentage control panel (CONVERT / CHANGE / ESTIMATE) stays on
    #     PANEL_Y in every teaching scene, so the two rows under it (ROW_A and
    #     ROW_B) and the rule chip on ROW_C never move;
    #   * every row of cards is centred on BOARD_CX (`hrow`), and two texts never
    #     come closer than the 0.22 units the clearance audit asks for -- which
    #     is why the cards space their own lines by 0.22 or more;
    #   * a drawn cross always lives in the same VGroup as the card it strikes
    #     through (otherwise the clearance audit reads the strokes as a line
    #     running into somebody else's card);
    #   * the challenge uses the series' shared 10-second THINK clock, dead
    #     centre of the board, and the question cards sit in the four corners so
    #     the clock never covers one.

    def closing(self, tracker, mob=None, color=CHALK_YELLOW, run_time=None):
        """Consume the tail of the narration window on the last reveal."""
        budget = rt(tracker.get_remaining_duration()) if run_time is None \
            else run_time
        if mob is None:
            self.wait(max(budget, 0.0))
        else:
            self.play(Indicate(mob, color=color, scale_factor=1.03),
                      run_time=max(budget, MIN_RT))

    def hrow(self, *mobs, y, gap=0.45, cx=BOARD_CX):
        """One row of board objects: centred on the board, equal air between."""
        row = VGroup(*mobs).arrange(RIGHT, buff=gap)
        return at(row, cx, y)

    def q_card(self, title, pict, color=CHALK_CYAN, width=3.00, pad=0.12,
               title_size=13, buff=0.26):
        """One 'your turn' card: a prompt above its small diagram."""
        head = board_text(title, title_size, color, "BOLD")
        content = VGroup(head, pict).arrange(DOWN, buff=buff)
        box = RoundedRectangle(corner_radius=0.10, width=width,
                               height=content.height + 2 * pad,
                               stroke_color=color, stroke_width=1.9,
                               fill_color=PANEL_FILL, fill_opacity=0.55)
        content.move_to(box.get_center())
        return VGroup(box, content)

    def answer_row(self, tag, headline, note, color, width=8.60, height=0.62,
                   pad=0.34, buff=0.36):
        """One revealed answer: its letter, the result and a short note.

        The row is laid out in FIXED COLUMNS rather than centred in its box, so
        the tag column and the text column are the same vertical line in every
        row (centring put each letter at a different x).  The box itself stays
        centred on BOARD_CX.  The same helper draws the recap list.
        """
        lab = board_text(tag, 17, color, "BOLD")
        name = board_text(headline, 17, color, "BOLD")
        txt = board_text(note, 15, CHALK_WHITE, "BOLD")
        row = VGroup(lab, name, txt).arrange(RIGHT, buff=buff)
        box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                               stroke_color=color, stroke_width=1.8,
                               fill_color=PANEL_FILL, fill_opacity=0.6)
        row.move_to(np.array([box.get_left()[0] + pad + row.width / 2.0,
                              box.get_center()[1], 0.0]))
        return VGroup(box, row)

    # -- Scene 0: title -- 225 of 300 against 200 of 250 ----------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = at(board_text("Who Did Better?", 26, CHALK_PINK, "BOLD"),
                       BOARD_CX, 1.98)
            sub = at(board_text("225 of 300, or 200 of 250?", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, 1.42)

            # the two hundred-cell squares: A lights 75 cells, B lights 80.
            # The percentage figures sit BELOW their square, never on it: a
            # grid cell is a Rectangle -- and so a Polygon -- to the audit, and
            # a letter sitting on a cell's own outline is a TEXT-ON-SIDE defect.
            ga = at(percent_grid(75, CHALK_GREEN), -1.85, 0.62)
            gb = at(percent_grid(80, CHALK_CYAN), 2.35, 0.62)
            p75 = at(board_text("75%", 22, CHALK_GREEN, "BOLD"), -1.85, -0.12)
            p80 = at(board_text("80%", 22, CHALK_CYAN, "BOLD"), 2.35, -0.12)
            cap_a = at(board_text("Group A: 225 out of 300", 14, CHALK_WHITE,
                                  "BOLD"), -1.85, -0.60)
            cap_b = at(board_text("Group B: 200 out of 250", 14, CHALK_WHITE,
                                  "BOLD"), 2.35, -0.60)
            ask = at(chalk_math("?", size=44, color=CHALK_YELLOW),
                     BOARD_CX, 0.62)

            banner = at(board_text("ONE SCALE: OUT OF 100", 18, CHALK_YELLOW,
                                   "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("A percentage puts different totals on one "
                                  "common scale.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(title, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(ga, scale=0.95), run_time=0.40)
            self.play(LaggedStart(*[c.animate.set_fill(CHALK_GREEN, 0.62)
                                    for c in ga.lit], lag_ratio=0.02),
                      run_time=0.70)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(gb, scale=0.95), run_time=0.40)
            self.play(LaggedStart(*[c.animate.set_fill(CHALK_CYAN, 0.62)
                                    for c in gb.lit], lag_ratio=0.02),
                      run_time=0.70)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(p75, scale=0.9), FadeIn(p80, scale=0.9),
                      run_time=0.45)
            self.play(FadeIn(cap_a, shift=UP * 0.06),
                      FadeIn(cap_b, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(ask, scale=0.9), FadeIn(banner, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: convert both to one scale -----------------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("One Scale for Every Total", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Part over whole, times one hundred.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)
            panel = mode_panel("CONVERT")

            ca = chip("225 : 300 = 3 : 4", CHALK_GREEN, size=14)
            cb = chip("200 : 250 = 4 : 5", CHALK_CYAN, size=14)
            ha, hb = ca.width / 2.0, cb.width / 2.0
            xa, xb = row_centres((ha, hb), 0.55)
            ca = at(ca, xa, ROW_A)
            cb = at(cb, xb, ROW_A)

            row_b = VGroup(
                chip("= 75 OUT OF 100 = 75%", CHALK_GREEN, size=14),
                chip("= 80 OUT OF 100 = 80%", CHALK_CYAN, size=14),
            )
            ha, hb = row_b[0].width / 2.0, row_b[1].width / 2.0
            xa, xb = row_centres((ha, hb), 0.50)
            r75 = at(row_b[0], xa, ROW_B)
            r80 = at(row_b[1], xb, ROW_B)

            rule = at(chip("PERCENTAGE = PART / WHOLE x 100", CHALK_YELLOW,
                           size=14), BOARD_CX, ROW_C)
            banner = at(board_text("GROUP B DID BETTER: 80% > 75%", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Always name the whole: 300 for A and 250 "
                                  "for B.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), FadeIn(panel, scale=0.95),
                      run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(ca, shift=UP * 0.06), FadeIn(cb, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(r75, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(r80, scale=0.9), FadeIn(banner, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(rule, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: a 35% increase -- the block ATTACHES ------------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("A 35% Increase Attaches a Block", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The increase is measured from the original.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)
            panel = mode_panel("CHANGE")

            bar = at(pct_bar(2.20, 0.50, CHALK_GREEN, "100% ORIGINAL", 14),
                     -2.20, ROW_A)
            block = pct_block(0.77, 0.50, CHALK_AMBER, "35%", 13)
            block.move_to(np.array([3.90, ROW_A, 0.0]))
            merged = at(chip("= 135% OF ORIGINAL", CHALK_YELLOW, size=14),
                        1.75, ROW_A)
            rule = at(chip("NEW VALUE = 135% OF THE ORIGINAL", CHALK_CYAN,
                           size=14), BOARD_CX, ROW_B)
            note = at(chip("THE INCREASE IS MEASURED FROM THE ORIGINAL",
                           CHALK_AMBER, size=13), BOARD_CX, ROW_C)
            banner = at(board_text("A 35% INCREASE GIVES 135% OF THE ORIGINAL",
                                   16, CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The increase is measured from the original, "
                                  "not the new value.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), FadeIn(panel, scale=0.95),
                      run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(bar, scale=0.95), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(block, scale=0.9), run_time=0.30)
            self.play(block.animate.next_to(bar, RIGHT, buff=0.0),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(merged, shift=UP * 0.06), FadeIn(rule, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(note, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: applying the increase to Rs 98,700 --------------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Applying the 35% Increase", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Add the increase to the original figure.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)
            panel = mode_panel("CHANGE")

            bag = at(money_bag(0.0, 0.0, 0.86, CHALK_AMBER, "SALES"),
                     -3.30, ROW_A)
            note = at(money_note(1.70, 0.80, CHALK_GREEN, "Rs 34,545"),
                      -1.20, ROW_A)
            up = at(chip("UP 35% THIS MONTH", CHALK_AMBER, size=14), 2.30, ROW_A)

            before = chip("SALES = Rs 98,700 (100%)", CHALK_CYAN, size=14)
            after = chip("98,700 + 34,545 = Rs 1,33,245", CHALK_GREEN, size=14)
            hb, ha = before.width / 2.0, after.width / 2.0
            xb, xa = row_centres((hb, ha), 0.50)
            before = at(before, xb, ROW_B)
            after = at(after, xa, ROW_B)

            route = at(chip("INCREASE = 35% OF 98,700 = Rs 34,545", CHALK_AMBER,
                            size=14), BOARD_CX, ROW_C)
            short = chip("SHORTCUT: 135% OF 98,700 = Rs 1,33,245",
                         CHALK_YELLOW, size=14)
            short.move_to(route.get_center())

            banner = at(board_text("NEW SALES = Rs 1,33,245", 18, CHALK_YELLOW,
                                   "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("A 35% rise gives 135% of the original "
                                  "figure.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), FadeIn(panel, scale=0.95),
                      run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(bag, scale=0.9), FadeIn(before, shift=UP * 0.06),
                      run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(up, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(note, scale=0.9), FadeIn(route, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(after, shift=UP * 0.06),
                      FadeIn(banner, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(Transform(route, short), FadeIn(strip, shift=UP * 0.06),
                      run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: a 10% decrease -- the block DETACHES and leaves -------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("A 10% Decrease on a Price Tag", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A decrease is taken away from one hundred.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)
            panel = mode_panel("CHANGE")

            tag = at(price_tag(2.30, 0.86, CHALK_PINK, "Rs 550"), -3.10, ROW_A)
            tens = at(decade_row(10, 0.26, 0.03, CHALK_CYAN, 0.52), 1.50,
                      ROW_A)
            last = tens[9]
            tag10 = board_text("10%", 13, CHALK_RED, "BOLD")
            tag10.move_to(np.array([last.get_center()[0], ROW_A - 0.44, 0.0]))

            part = chip("10% OF 550 = Rs 55", CHALK_RED, size=14)
            rest = chip("550 - 55 = Rs 495", CHALK_GREEN, size=14)
            hp, hr = part.width / 2.0, rest.width / 2.0
            xp, xr = row_centres((hp, hr), 0.50)
            part = at(part, xp, ROW_B)
            rest = at(rest, xr, ROW_B)

            inc = chip("INCREASE p% -> 100% + p%", CHALK_GREEN, size=14)
            dec = chip("DECREASE p% -> 100% - p%", CHALK_RED, size=14)
            hi, hd = inc.width / 2.0, dec.width / 2.0
            xi, xd = row_centres((hi, hd), 0.50)
            inc = at(inc, xi, ROW_C)
            dec = at(dec, xd, ROW_C)

            banner = at(board_text("10% OFF -> YOU PAY 90%", 18, CHALK_YELLOW,
                                   "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("A decrease is taken away from one hundred "
                                  "percent.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), FadeIn(panel, scale=0.95),
                      run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(tag, scale=0.9), FadeIn(tens, shift=UP * 0.06),
                      run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(last.animate.set_fill(CHALK_RED, 0.55
                                            ).set_stroke(CHALK_RED),
                      FadeIn(tag10, scale=0.9), FadeIn(part, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(last.animate.shift(RIGHT * 1.10 + DOWN * 0.55
                                         ).set_fill(CHALK_RED, 0.10
                                                    ).set_stroke(opacity=0.25),
                      tag10.animate.shift(RIGHT * 1.10 + DOWN * 0.55
                                          ).set_opacity(0.15),
                      FadeIn(rest, scale=0.9), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(inc, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(dec, scale=0.9), FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: the mental toolkit, and the doubled-halving mistake ---------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Mental Percentage Toolkit", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Ten percent first, then half, then add.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)
            panel = mode_panel("ESTIMATE")

            whole = at(pct_block(1.20, 0.54, CHALK_AMBER, "10%", 14),
                       -2.00, ROW_A)
            halves = split_block(1.20, 0.54, CHALK_AMBER)
            halves.move_to(whole.get_center())

            rules = VGroup(
                chip("10% = ONE TENTH", CHALK_GREEN, size=12),
                chip("5% = HALF OF 10%", CHALK_CYAN, size=12),
                chip("15% = 10% + 5%", CHALK_AMBER, size=12),
                chip("20% = 2 x 10%", CHALK_PINK, size=12),
            )
            halves_w = [c.width / 2.0 for c in rules]
            centres = row_centres(halves_w, 0.28)
            for c, x in zip(rules, centres):
                at(c, x, ROW_B)

            wrong = wrong_card("5% = HALF OF 20%", CHALK_RED, width=2.30,
                               height=0.85, size=13)
            wrong.move_to(np.array([2.90, ROW_A, 0.0]))
            wrong_cross = wrong.cross
            wrong_cross.set_stroke(opacity=0)

            demo = at(chip("ON 480:  10% = 48,  5% = 24,  SO 15% = 72",
                           CHALK_YELLOW, size=14), BOARD_CX, ROW_C)
            banner = at(board_text("5% IS HALF OF 10%, NOT OF 20%", 16,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Build hard percentages out of ten percent.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), FadeIn(panel, scale=0.95),
                      run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(whole, scale=0.9), FadeIn(rules[0], scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(ReplacementTransform(whole, halves), run_time=0.45)
            self.play(halves.half_l.animate.shift(LEFT * 0.07),
                      halves.half_r.animate.shift(RIGHT * 0.07),
                      FadeIn(rules[1], scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(rules[2], scale=0.9), FadeIn(rules[3], scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(wrong, scale=0.9), run_time=0.40)
            self.play(wrong_cross.animate.set_stroke(opacity=1),
                      FadeIn(banner, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(demo, scale=0.9), FadeIn(strip, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: estimating 15% on the bill ---------------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("Estimating 15% on a Bill", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Round the bill, then build fifteen percent.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)
            panel = mode_panel("ESTIMATE")

            bill = at(receipt(1.70, 1.00, CHALK_CYAN, "BILL", "Rs 477.80"),
                      -3.35, ROW_A)
            ruler = number_ruler()
            start_x = nl_x(BILL)
            dot = Dot(radius=0.10, color=CHALK_PINK)
            dot.move_to(np.array([start_x, NL_Y, 0.0]))

            ten = chip("10% OF 480 = Rs 48", CHALK_GREEN, size=13)
            five = chip("5% = HALF OF THAT = Rs 24", CHALK_CYAN, size=13)
            fifteen = chip("15% = 48 + 24 = Rs 72", CHALK_AMBER, size=13)
            t1, t2, t3 = (ten, five, fifteen)
            w1, w2, w3 = t1.width / 2.0, t2.width / 2.0, t3.width / 2.0
            c1, c2, c3 = row_centres((w1, w2, w3), 0.30)
            ten = at(t1, c1, ROW_B)
            five = at(t2, c2, ROW_B)
            fifteen = at(t3, c3, ROW_B)

            step = chip("APPROX Rs 480 - Rs 72 = Rs 408", CHALK_YELLOW, size=14)
            approx = chalk_math(r"\approx", size=30, color=CHALK_YELLOW)
            paid = chip("ABOUT Rs 410", CHALK_GREEN, size=14)
            hs, hp = step.width / 2.0, paid.width / 2.0
            xs, xp = row_centres((hs, hp), 0.90)
            step = at(step, xs, ROW_C)
            approx.move_to(np.array([(xs + hs + xp - hp) / 2.0, ROW_C, 0.0]))
            paid = at(paid, xp, ROW_C)

            banner = at(board_text("ROUND THE BILL, THEN PAY ABOUT Rs 410", 16,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Round the bill, then build fifteen percent "
                                  "from ten percent.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), FadeIn(panel, scale=0.95),
                      run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(bill, scale=0.9), FadeIn(ruler, shift=UP * 0.06),
                      run_time=0.45)
            self.play(FadeIn(dot, scale=0.9), run_time=0.25)
            self.play(dot.animate.move_to(np.array([nl_x(ROUNDED_BILL), NL_Y,
                                                    0.0])), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(ten, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(five, scale=0.9), FadeIn(fifteen, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(step, scale=0.9), FadeIn(approx, scale=0.9),
                      run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(paid, scale=0.9), FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: the exact lane beside the estimate lane --------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Exact Lane and Estimate Lane", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("An estimate is a check, not exact arithmetic.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)
            panel = mode_panel("ESTIMATE")

            exact = note_card("EXACT LANE", ["15% of 477.80 = 71.67"],
                              CHALK_CYAN, width=4.30, height=1.00,
                              head_size=14, line_size=13)
            mental = note_card("MENTAL LANE", ["15% of 480 = 72"],
                               CHALK_GREEN, width=4.30, height=1.00,
                               head_size=14, line_size=13)
            he, hm = exact.width / 2.0, mental.width / 2.0
            xe, xm = row_centres((he, hm), 0.45)
            exact = at(exact, xe, ROW_A)
            mental = at(mental, xm, ROW_A)

            l1 = chip("477.80 - 71.67 = 406.13", CHALK_CYAN, size=14)
            l2 = chip("480 - 72 = 408, ABOUT 410", CHALK_GREEN, size=14)
            h1, h2 = l1.width / 2.0, l2.width / 2.0
            x1, x2 = row_centres((h1, h2), 0.50)
            l1 = at(l1, x1, ROW_B)
            l2 = at(l2, x2, ROW_B)

            check = chip("AN ESTIMATE IS A REASONABLENESS CHECK, NOT EXACT "
                         "ARITHMETIC", CHALK_YELLOW, size=13)
            mark = tick((0.0, 0.0), CHALK_GREEN, 0.18)
            hk, hc = mark.width / 2.0, check.width / 2.0
            xk, xc = row_centres((hk, hc), 0.35)
            mark.move_to(np.array([xk, ROW_C, 0.0]))
            check = at(check, xc, ROW_C)

            banner = at(board_text("EXACT 406.13, ESTIMATE ABOUT 410", 16,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("An estimate is a reasonableness check, not "
                                  "exact arithmetic.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), FadeIn(panel, scale=0.95),
                      run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(exact, scale=0.95), FadeIn(l1, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(mental, scale=0.95), FadeIn(l2, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(mark), FadeIn(check, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the four-move decision map ---------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Four-Move Decision Map", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Convert, change, estimate, check.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)
            panel = mode_panel("ALL")

            c1 = note_card("CONVERT", ["part / whole x 100"], CHALK_GREEN,
                           width=2.20, height=1.05, head_size=14,
                           line_size=12)
            c2 = note_card("INCREASE", ["100% + p%"], CHALK_AMBER,
                           width=2.20, height=1.05, head_size=14,
                           line_size=12)
            c3 = note_card("DECREASE", ["100% - p%"], CHALK_CYAN,
                           width=2.20, height=1.05, head_size=14,
                           line_size=12)
            c4 = note_card("ESTIMATE", ["round, then use 10%"], CHALK_PINK,
                           width=2.20, height=1.05, head_size=14,
                           line_size=12)
            hw = [c.width / 2.0 for c in (c1, c2, c3, c4)]
            xs = row_centres(hw, 0.28)
            c1, c2, c3, c4 = (at(c, x, 0.72) for c, x in zip((c1, c2, c3, c4),
                                                             xs))

            flow = at(chip("CONVERT -> CHANGE -> ESTIMATE -> CHECK",
                           CHALK_YELLOW, size=15), BOARD_CX, ROW_C)
            banner = at(board_text("FOUR MOVES: CONVERT, INCREASE, DECREASE, "
                                   "ESTIMATE", 16, CHALK_YELLOW, "BOLD"),
                        BOARD_CX, BANNER_Y)
            strip = at(board_text("Round first, then build the percentage from "
                                  "ten percent.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), FadeIn(panel, scale=0.95),
                      run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(c1, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(c2, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(c3, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(c4, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(flow, scale=0.9), FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 9: your turn (questions, the silent clock, then the answers) ---
    def beat_s9(self) -> None:
        with self.voiceover(text=NARRATION["s9q"]) as tracker:
            self.reset_board()

            heading = at(board_text("YOUR TURN", 26, CHALK_PINK, "BOLD"),
                         BOARD_CX, 2.78)
            sub = at(board_text("Four quick checks.", 16, CHALK_WHITE, "BOLD"),
                     BOARD_CX, 2.20)

            pic_a = chalk_math(r"\frac{18}{24} \to \; ?\%", size=18,
                               color=CHALK_GREEN)
            pic_b = board_text("800 - 10% = ?", 14, CHALK_CYAN, "BOLD")
            pic_c = board_text("round 360, 20% = ?", 14, CHALK_AMBER, "BOLD")
            pic_d = board_text("900 + 35% = ?", 14, CHALK_PINK, "BOLD")

            qa = at(self.q_card("convert 18 out of 24", pic_a, CHALK_GREEN),
                    -2.80, 0.92)
            qb = at(self.q_card("Rs 800 with 10% off", pic_b, CHALK_CYAN),
                    3.70, 0.92)
            qc = at(self.q_card("estimate 20% of 357.30", pic_c, CHALK_AMBER),
                    -2.80, -1.02)
            qd = at(self.q_card("increase Rs 900 by 35%", pic_d, CHALK_PINK),
                    3.70, -1.02)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(qa, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(qb, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(qc, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(qd, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self._capture_srt(tracker)

        # The ten-second THINK pause is deliberately SILENT: the questions have
        # just been read, so the clock ticks alone, with no narration to sync
        # against.
        play_challenge_countdown(self, seconds=10, sfx=self.sfx,
                                 position=np.array([BOARD_CX, BOARD_CY, 0]))

        with self.voiceover(text=NARRATION["s9a"]) as tracker:
            self.wait(leftover(tracker, "b0"))
            self.play(FadeOut(qa), FadeOut(qb), FadeOut(qc), FadeOut(qd),
                      run_time=0.50)
            a1 = at(self.answer_row("A", "18 of 24 = 75%",
                                    "18 / 24 = 3 / 4 = 75%", CHALK_GREEN),
                    BOARD_CX, 1.62)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "Rs 800 - 10% = Rs 720",
                                    "10% of 800 = Rs 80", CHALK_CYAN),
                    BOARD_CX, 0.82)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "about 20% of 360 = Rs 72",
                                    "10% = 36, so 20% = 72", CHALK_AMBER),
                    BOARD_CX, 0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "Rs 900 + 35% = Rs 1,215",
                                    "135% of 900 = Rs 1,215", CHALK_PINK),
                    BOARD_CX, -0.78)
            self.play(FadeIn(a4, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, a4)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap and the spoken thank-you ----------------------------
    def beat_s10(self) -> None:
        with self.voiceover(text=NARRATION["s10"]) as tracker:
            self.reset_board()

            heading = at(board_text("Compare, Change, Estimate, Check", 18,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Four rules to carry away.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            r1 = at(self.answer_row("1", "COMPARE",
                                    "always out of one hundred", CHALK_GREEN),
                    BOARD_CX, 1.48)
            r2 = at(self.answer_row("2", "CHANGE",
                                    "increase adds, decrease subtracts",
                                    CHALK_CYAN), BOARD_CX, 0.72)
            r3 = at(self.answer_row("3", "ESTIMATE",
                                    "round, then build from 10%", CHALK_YELLOW),
                    BOARD_CX, -0.04)
            r4 = at(self.answer_row("4", "CHECK",
                                    "an estimate is a reasonableness check",
                                    CHALK_AMBER), BOARD_CX, -0.80)
            strip = at(board_text("Compare, change, estimate, then check.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)
            thanks = at(board_text("Thank You for Watching!", 30, CHALK_WHITE,
                                   "BOLD"), BOARD_CX, 0.62)
            bye = at(board_text("See you in the next lesson :)", 22, CHALK_YELLOW,
                                "BOLD"), BOARD_CX, -0.32)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(r1, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(r2, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(r3, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(r4, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            # The four rules stay on the board through the whole closing
            # sentence: the strip is written on its own bookmark as the voice
            # says "Compare, change, estimate, check.", and only the bookmark in
            # front of "Thank you for watching," clears the board and brings in
            # the card.
            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeOut(heading), FadeOut(sub), FadeOut(r1), FadeOut(r2),
                      FadeOut(r3), FadeOut(r4), FadeOut(strip), run_time=0.55)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.50)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.closing(tracker, thanks, run_time=0.90)
            self._capture_srt(tracker)

        self.wait(END_HOLD)

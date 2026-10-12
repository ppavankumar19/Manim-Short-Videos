"""
Understanding Negative Exponents: Reciprocal Rules and Multiplicative Inverses
Story-mode chalkboard lesson (Telangana Class 8 Maths, Chapter 4:
Exponents and Powers, Storymode 02).

LLM KEY / FUNCTION NAME: scientific_notation_large_and_small_numbers

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

The defining visual is the EXPONENT STAIRCASE: 10^3 down to 10^-3, one row per
power, indented as it descends, with a "one step down" note that divides by the
staircase's OWN base (10 in the tens scenes, 2 in the powers-of-two scene -- the
base is never left behind).  The second persistent visual is the RECIPROCAL
MIRROR: a^m and a^-m on either side of a dashed axis, with their product
collapsing to 1.

Title + 10 scenes:
  0. Title card.
  1. From huge numbers to tiny numbers: the Sun's 1.4 x 10^9 m against a hair's
     0.000005 m, and the question "can exponents take us below one?".
  2. Follow the pattern: 10^3, 10^2, 10^1, 10^0 with a "/10" between the steps.
  3. Crossing zero: 10^-1, 10^-2, 10^-3 derived from the same rule, with
     10^-1 = 1/10 highlighted.
  4. Any base works: the same staircase in powers of two, dividing by 2.
  5. The rule: a^-m = 1/a^m, the reverse 1/a^m = a^-m, and a != 0.
  6. Not a negative number: 2^-3 = 1/8 against -2^3 = -8.
  7. Multiplicative inverses: the reciprocal mirror, 8 x 1/8 = 1 and
     a^m x a^-m = a^0 = 1.
  8. Flip the sign: 3^-5 pairs with 3^5, 4^-3 with 4^3, x^-n with x^n.
  9. Your turn: 10^-4 rewritten, 5^-2 evaluated, the inverse of 7^-3, after the
     series' centred ten-second THINK clock.
 10. Recap and thank-you.
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


from manim import Ellipse  # noqa: E402  (the base head does not import it)

# Board layout shared by every scene of this video.
ROW_Y = 2.72             # every scene heading sits on this line
BANNER_Y = -1.30         # the closing banner, above the strip
# The burned-in caption grows up from the bottom of the frame: a one-line cue
# starts at y = -3.38 and a wrapped two-line cue reaches y = -2.93 (measured on
# the series' own burned 360p cuts), so every closing strip sits at -1.80 and
# nothing at all sits below y = -2.00 -- audited by the IN-CAPTION-BAND check.
STRIP_Y = -1.80

PANEL_FILL = "#16202B"
TRACK_PITCH = 0.46       # one place on the decimal elevator
TRACK_Y = 0.95           # where the numeral itself is laid out
COUNT_Y = 1.78           # where the place counter sits, above the numeral


# ---------------------------------------------------------------- furniture --
def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


def decimal_slots(digits, point_pos, y=0.95, pitch=TRACK_PITCH, size=34,
                  color=CHALK_WHITE, cx=None):
    """Lay a numeral out digit by digit along a place-value track.

    `point_pos` is how many digits sit LEFT of the decimal point to begin with
    (9 for 300000000, 1 for 0.000003).  The point itself is not a glyph -- it is
    the travelling marker -- so the marker has somewhere honest to walk to:
    `positions[p]` is the x of the point when p digits are in front of it.
    """
    cx = BOARD_CX if cx is None else cx
    n = len(digits)
    xs = [cx - (n - 1) * pitch / 2.0 + i * pitch for i in range(n)]
    glyphs = VGroup(*[chalk_math(ch, size=size, color=color).move_to(
        np.array([x, y, 0.0])) for ch, x in zip(digits, xs)])
    grp = VGroup(glyphs)
    grp.xs = xs
    grp.glyphs = list(glyphs)
    grp.positions = ([xs[0] - pitch / 2.0]
                     + [xs[i] + pitch / 2.0 for i in range(n)])
    grp.point_pos = point_pos
    return grp


def deci_marker(x, y, color=CHALK_RED, radius=0.065):
    """The travelling decimal point."""
    return Dot(radius=radius, color=color).move_to(np.array([x, y, 0.0]))


def card(mob, color=CHALK_WHITE, pad_x=0.54, pad_y=0.36, fill=0.55,
         stroke=1.9):
    """A rounded chalk card wrapped snugly around one expression."""
    box = RoundedRectangle(corner_radius=0.10, width=mob.width + pad_x,
                           height=mob.height + pad_y, stroke_color=color,
                           stroke_width=stroke, fill_color=PANEL_FILL,
                           fill_opacity=fill)
    mob.move_to(box.get_center())
    grp = VGroup(box, mob)
    grp.body = mob
    return grp


def law_card(maths, note, color=CHALK_CYAN, width=4.2, height=1.35,
             note_size=14, math_up=0.30, note_down=0.34):
    """One dashboard cell: an expression, with its one-line rule underneath."""
    box = RoundedRectangle(corner_radius=0.12, width=width, height=height,
                           stroke_color=color, stroke_width=2.0,
                           fill_color=PANEL_FILL, fill_opacity=0.55)
    maths.move_to(box.get_center() + UP * math_up)
    note_mob = board_text(note, note_size, color, "BOLD")
    note_mob.move_to(box.get_center() + DOWN * note_down)
    return VGroup(box, maths, note_mob)


def chip(text, color=CHALK_CYAN, size=15, width=None, height=0.50):
    """A small labelled chip."""
    lab = board_text(text, size, color, "BOLD")
    box = RoundedRectangle(corner_radius=0.09,
                           width=width or (lab.width + 0.42), height=height,
                           stroke_color=color, stroke_width=1.7,
                           fill_color=PANEL_FILL, fill_opacity=0.7)
    lab.move_to(box.get_center())
    return VGroup(box, lab)


def sun(radius=0.30, body=CHALK_AMBER, ray=CHALK_YELLOW):
    """The Sun: a chalk disc with eight rays (300,000,000 m across)."""
    disc = Circle(radius=radius, stroke_color=ray, stroke_width=2.2,
                  fill_color=body, fill_opacity=0.9)
    rays = VGroup()
    for k in range(8):
        ang = k * np.pi / 4.0
        start = np.array([np.cos(ang), np.sin(ang), 0.0]) * (radius + 0.05)
        end = np.array([np.cos(ang), np.sin(ang), 0.0]) * (radius + 0.17)
        rays.add(Line(start, end, stroke_color=ray, stroke_width=2.8))
    return VGroup(rays, disc)


def chip_icon(size=0.60, body="#33424E", trace=CHALK_CYAN):
    """A computer chip: a body with legs and one highlighted wire across it
    (the wire that is 0.000003 m across).  (The labelled `chip` helper above is
    a different thing -- a small caption box.)"""
    box = RoundedRectangle(corner_radius=0.07, width=size, height=size,
                           stroke_color=CHALK_WHITE, stroke_width=2.0,
                           fill_color=body, fill_opacity=0.9)
    legs = VGroup()
    for i in range(3):
        off = (i - 1) * size / 3.0
        legs.add(Line(np.array([-size / 2 - 0.13, off, 0.0]),
                      np.array([-size / 2, off, 0.0]),
                      stroke_color=CHALK_WHITE, stroke_width=2.0))
        legs.add(Line(np.array([size / 2, off, 0.0]),
                      np.array([size / 2 + 0.13, off, 0.0]),
                      stroke_color=CHALK_WHITE, stroke_width=2.0))
    wire = Line(np.array([-size / 2, -size / 6.0, 0.0]),
                np.array([size / 2, -size / 6.0, 0.0]), color=trace,
                stroke_width=3.6)
    return VGroup(box, legs, wire)


def plant_cell(w=0.98, h=0.74, wall=CHALK_GREEN, fill="#17301F"):
    """A plant cell: wall, nucleus, vacuole and a few organelles
    (0.00001275 m across)."""
    outer = RoundedRectangle(corner_radius=0.15, width=w, height=h,
                             stroke_color=wall, stroke_width=2.6,
                             fill_color=fill, fill_opacity=0.9)
    inner = RoundedRectangle(corner_radius=0.13, width=w - 0.10,
                             height=h - 0.10, stroke_color=wall,
                             stroke_width=1.3)
    nucleus = Circle(radius=0.105, stroke_color=CHALK_PINK, stroke_width=1.8,
                     fill_color=CHALK_PINK, fill_opacity=0.55
                     ).move_to(np.array([-0.17, 0.09, 0.0]))
    vacuole = Ellipse(width=0.34, height=0.24, stroke_color=CHALK_CYAN,
                      stroke_width=1.5, fill_color=CHALK_CYAN,
                      fill_opacity=0.25).move_to(np.array([0.17, -0.08, 0.0]))
    dots = VGroup(*[Dot(radius=0.026, color=CHALK_YELLOW).move_to(p)
                    for p in ((0.24, 0.17, 0.0), (-0.29, -0.15, 0.0),
                              (0.02, -0.24, 0.0))])
    return VGroup(outer, inner, nucleus, vacuole, dots)


def scale_marks(ks, y=0.90, dy=0.45, step=1.35, size=22, value_size=16,
                small=CHALK_PINK, large=CHALK_GREEN):
    """The powers-of-ten scale ruler: one tick per exponent, value beneath."""
    axis = Line(np.array([BOARD_CX - 3 * step - 0.70, y, 0.0]),
                np.array([BOARD_CX + 3 * step + 0.70, y, 0.0]),
                color=CHALK_WHITE, stroke_width=2.2)
    ticks, labels = VGroup(), VGroup()
    for i, k in enumerate(ks):
        x = BOARD_CX + k * step
        ticks.add(Line(np.array([x, y - 0.13, 0.0]),
                       np.array([x, y + 0.13, 0.0]), color=CHALK_WHITE,
                       stroke_width=2.4))
        col = large if k > 0 else (CHALK_WHITE if k == 0 else small)
        labels.add(chalk_math(f"10^{{{k}}}", size=size, color=col).move_to(
            np.array([x, y + dy, 0.0])))
        val = {0: "1", 1: "10", 2: "100", 3: "1000", -1: "1/10",
               -2: "1/100", -3: "1/1000"}[k]
        labels.add(chalk_math(val, size=value_size, color=CHALK_WHITE).move_to(
            np.array([x, y - dy, 0.0])))
    grp = VGroup(axis, ticks, labels)
    grp.axis = axis
    grp.ticks = ticks
    grp.labels = labels
    return grp


def q_card(title, body, color=CHALK_CYAN, width=3.7, height=0.92,
           head_up=0.28, body_down=0.22):
    """One 'your turn' question card: the prompt over the expression."""
    head = board_text(title, 13, color, "BOLD")
    box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                           stroke_color=color, stroke_width=1.9,
                           fill_color=PANEL_FILL, fill_opacity=0.55)
    head.move_to(box.get_center() + UP * head_up)
    body.move_to(box.get_center() + DOWN * body_down)
    return VGroup(box, head, body)


def answer_row(tag, maths, note, color, width=8.0, height=0.70):
    """One revealed answer: its letter, the expression and a short note."""
    lab = board_text(tag, 17, color, "BOLD")
    txt = board_text(note, 16, CHALK_WHITE, "BOLD")
    row = VGroup(lab, maths, txt).arrange(RIGHT, buff=0.40)
    box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                           stroke_color=color, stroke_width=1.8,
                           fill_color=PANEL_FILL, fill_opacity=0.6)
    row.move_to(box.get_center())
    return VGroup(box, row)


# ----------------------------------------------------------------


NARRATION = {
    "title": (
        "Standard form with powers of ten. <bookmark mark='b0'/>Among all the "
        "exponent laws, this one is the most useful in science: it writes very "
        "large and very small numbers compactly. <bookmark mark='b1'/>Move the "
        "decimal point, count the places, and write the power of ten."
    ),
    "s1": (
        "Standard form begins with two extremes. <bookmark mark='b0'/>The Sun "
        "is about three hundred million metres away. <bookmark mark='b1'/>A "
        "wire inside a computer chip is about zero point zero zero zero zero "
        "zero three metres across. <bookmark mark='b2'/>Powers of ten write "
        "both: three times ten to the power eight, and three times ten to the "
        "power minus six."
    ),
    "s2": (
        "Powers of ten are really a scale. <bookmark mark='b0'/>Ten to the "
        "power zero is one, in the middle. <bookmark mark='b1'/>To the right "
        "the numbers grow: ten, one hundred, one thousand. <bookmark "
        "mark='b2'/>To the left they shrink below one: one tenth, one "
        "hundredth, one thousandth. <bookmark mark='b3'/>So a positive "
        "exponent means a large scale, and a negative exponent means a small "
        "scale."
    ),
    "s3": (
        "Now convert a large number: three hundred million. <bookmark "
        "mark='b0'/>The decimal point sits at the right-hand end. <bookmark "
        "mark='b1'/>Move it left, one place at a time, until a single non-zero "
        "digit stands in front of it: that is eight places. <bookmark "
        "mark='b2'/>So three hundred million is three times ten to the power "
        "eight."
    ),
    "s4": (
        "Here is a second large number: six thousand and twenty million. "
        "<bookmark mark='b0'/>Again the decimal point begins at the right-hand "
        "end. <bookmark mark='b1'/>Move it left until only one non-zero digit "
        "stands in front: <bookmark mark='b2'/>one, <bookmark mark='b3'/>two, "
        "<bookmark mark='b4'/>three, <bookmark mark='b5'/>four, <bookmark "
        "mark='b6'/>five, <bookmark mark='b7'/>six, <bookmark mark='b8'/>seven, "
        "<bookmark mark='b9'/>eight, <bookmark mark='b10'/>nine places. "
        "<bookmark mark='b11'/>The digits we keep are six, zero, two. "
        "<bookmark mark='b12'/>So the number is six point zero two times ten "
        "to the power nine."
    ),
    "s5": (
        "Now a very small number: the wire inside a chip is zero point zero "
        "zero zero zero zero three metres across. <bookmark mark='b0'/>This "
        "time the decimal point starts at the left. <bookmark mark='b1'/>Move "
        "it right until only one non-zero digit stands in front: that is six "
        "places, and the digit is three. <bookmark mark='b2'/>Because we moved "
        "right, into a number that was smaller than one, the exponent is "
        "negative: three times ten to the power minus six."
    ),
    "s6": (
        "A plant cell is even more interesting: it is zero point zero zero "
        "zero zero one two seven five metres across. <bookmark mark='b0'/>The "
        "significant digits are one, two, seven and five, and they do not "
        "change. <bookmark mark='b1'/>Move the decimal point right: <bookmark "
        "mark='b2'/>one, <bookmark mark='b3'/>two, <bookmark mark='b4'/>three, "
        "<bookmark mark='b5'/>four, <bookmark mark='b6'/>five places. "
        "<bookmark mark='b7'/>So the standard form is one point two seven five "
        "times ten to the power minus five. The quantity is the same; only the "
        "way we write it has changed."
    ),
    "s7": (
        "Now the other direction: from standard form back to usual form. "
        "<bookmark mark='b0'/>Four point six seven times ten to the power "
        "four: the exponent is positive, so the decimal point moves right four "
        "places, giving forty six thousand seven hundred. <bookmark "
        "mark='b1'/>Three point zero two times ten to the power minus six: the "
        "exponent is negative, so the decimal point moves left six places, "
        "giving zero point zero zero zero zero zero three zero two. <bookmark "
        "mark='b2'/>These directions are for going back to usual form; making "
        "standard form moves the decimal the other way."
    ),
    "s8": (
        "Here is the complete map. <bookmark mark='b0'/>A large number in "
        "usual form moves its decimal point left and takes a positive "
        "exponent. <bookmark mark='b1'/>A small number moves its decimal point "
        "right and takes a negative exponent. <bookmark mark='b2'/>Coming back "
        "from standard form the movements reverse: a positive exponent moves "
        "the decimal right, and a negative exponent moves it left. Always ask "
        "which direction you are converting."
    ),
    "s9q": (
        "Your turn. <bookmark mark='b0'/>Three conversions. Write zero point zero "
        "zero zero zero four five six in standard form. Write six thousand and twenty "
        "million in standard form. And write five point eight times ten to the power "
        "seven in usual form."
    ),
    "s9a": (
        "<bookmark mark='b0'/>For the first, the decimal moves right five places, so "
        "it is four point five six times ten to the power minus five. <bookmark "
        "mark='b1'/>For the second, the decimal moves left nine places: six point "
        "zero two times ten to the power nine. <bookmark mark='b2'/>And for the third "
        "the exponent is positive seven, so the decimal moves right seven places: "
        "fifty eight million."
    ),
    "s10": (
        "One last look at the whole idea. <bookmark mark='b0'/>Move the decimal "
        "point, count the places, choose the sign, and write times ten to the power: "
        "three hundred million is three times ten to the power eight. <bookmark "
        "mark='b1'/>And zero point zero zero zero zero zero three is three times ten "
        "to the power minus six. <bookmark mark='b2'/>Powers of ten let us write the "
        "very large and the very small compactly. <bookmark mark='b3'/>Thank you for "
        "watching the chapter, <bookmark mark='b4'/>and see you in the next lesson."
    ),
}


class StandardFormStory(VoiceoverScene):
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
        out_dir = _HERE / "media" / "videos" / "scientific_notation_large_and_small_numbers"
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
        srt_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"[real SRT written] {srt_path}")
        (out_dir / "real.srt").write_text("\n".join(lines), encoding="utf-8")
        try:
            if (hasattr(self, "renderer") and hasattr(self.renderer, "file_writer")
                    and self.renderer.file_writer.movie_file_path):
                movie_dir = Path(self.renderer.file_writer.movie_file_path).parent
                (movie_dir / "real.srt").write_text("\n".join(lines), encoding="utf-8")
                (movie_dir / f"{self.__class__.__name__}.real.srt").write_text(
                    "\n".join(lines), encoding="utf-8")
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
    # Standard Form with Powers of 10 (Class 8, Chapter 4, Storymode 05 -- the
    # closing video of the five-part sequence).
    #
    # SYNC RULE for every reveal: wait for the narration bookmark that ends the
    # phrase describing a thing, and only then bring it on.  Playing first and
    # waiting afterwards shows the picture a whole window early, which reads as
    # broken sync.
    #
    # Layout rules, so the audits stay clean:
    #   * the heading sits on ROW_Y (2.72), the closing strip on STRIP_Y (-1.80);
    #     nothing at all sits below y = -2.00;
    #   * the visual identity is the DECIMAL-POINT ELEVATOR: the numeral is laid
    #     out slot by slot and the decimal marker walks it one place at a time
    #     while a counter ticks, so the exponent is counted, not announced;
    #   * nothing is placed on a line, and no card, digit or chip is placed over
    #     another element -- checked by audit_clearance.py and
    #     audit_sync_overlap.py;
    #   * the challenge uses the series' shared 10-second THINK clock, dead
    #     centre of the board, with the question cards around it.
    ROW_Y = 2.72
    BANNER_Y = -1.30
    STRIP_Y = -1.80
    TRACK_Y = 0.95
    COUNT_Y = 1.78

    def closing(self, tracker, mob=None, color=CHALK_YELLOW, run_time=None):
        """Consume the tail of the narration window on the last reveal."""
        budget = rt(tracker.get_remaining_duration()) if run_time is None \
            else run_time
        if mob is None:
            self.wait(max(budget, 0.0))
        else:
            self.play(Indicate(mob, color=color, scale_factor=1.03),
                      run_time=max(budget, MIN_RT))

    def run_elevator(self, tracker, mark, track, marker, counter, target,
                     next_mark=None, max_rt=0.90):
        """Walk the decimal point to `target`, in step with the narration.

        Where the voice does not count aloud (scenes 3 and 5) the walk is spread
        across the whole narration window, so the marker can never reach the end
        while the sentence is still being spoken; `next_mark` is the bookmark
        that closes that window."""
        self.wait(leftover(tracker, mark))
        start = track.point_pos
        n = abs(target - start)
        step = 1 if target > start else -1
        span = max(tracker.time_until_bookmark(next_mark), 0.0) \
            if next_mark else 0.0
        step_rt = min(max(span / n, 0.22), max_rt) if span else 0.22
        for k in range(1, n + 1):
            pos = start + k * step
            new_counter = at(board_text(str(k), 20, CHALK_CYAN, "BOLD"),
                             BOARD_CX, COUNT_Y)
            self.play(marker.animate.move_to(
                np.array([track.positions[pos], TRACK_Y, 0.0])),
                Transform(counter, new_counter), run_time=step_rt)
            self.add_sound(self.sfx["click"], gain=-26)
        track.point_pos = target

    def run_elevator_marked(self, tracker, marks, track, marker, counter,
                            direction=-1, step_rt=0.30):
        """One place per narration bookmark -- used where the voice counts
        aloud, so the counter shows the number being spoken as it is said."""
        for k, mark in enumerate(marks, start=1):
            self.wait(leftover(tracker, mark))
            pos = track.point_pos + direction
            new_counter = at(board_text(str(k), 20, CHALK_CYAN, "BOLD"),
                             BOARD_CX, COUNT_Y)
            self.play(marker.animate.move_to(
                np.array([track.positions[pos], TRACK_Y, 0.0])),
                Transform(counter, new_counter), run_time=step_rt)
            self.add_sound(self.sfx["click"], gain=-26)
            track.point_pos = pos

    def elevator(self, digits, point_pos, note="the decimal point",
                 label_x=3.95):
        """A ready-made elevator: the track, its marker and its counter.

        `label_x` moves the little legend to whichever end is free -- scenes 5
        and 6 use the right-hand side for their drawing."""
        track = decimal_slots(digits, point_pos, y=TRACK_Y,
                                 pitch=0.44, size=34)
        marker = deci_marker(track.positions[point_pos], TRACK_Y)
        counter = at(board_text("0", 20, CHALK_CYAN, "BOLD"), BOARD_CX, COUNT_Y)
        label = at(board_text(note, 14, CHALK_WHITE, "BOLD"), label_x, TRACK_Y)
        return track, marker, counter, label

    # -- Scene 0: title ------------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            heading = at(board_text("Standard Form with Powers of 10", 24,
                                    CHALK_WHITE, "BOLD"), BOARD_CX, 2.10)
            sub = at(board_text("Writing Very Large and Very Small Numbers", 17,
                                CHALK_AMBER, "BOLD"), BOARD_CX, 1.45)
            big = at(chalk_math(r"300,000,000 = 3 \times 10^8", size=32,
                                color=CHALK_CYAN), BOARD_CX, 0.65)
            small = at(chalk_math(r"0.000003 = 3 \times 10^{-6}", size=32,
                                  color=CHALK_YELLOW), BOARD_CX, -0.35)
            promise = at(board_text("Move the decimal, count the places, write "
                                    "the power.", 16, CHALK_WHITE, "BOLD"),
                         BOARD_CX, -1.25)
            strip = at(board_text("One notation for both extremes.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(sub, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(big, shift=UP * 0.08),
                      FadeIn(small, shift=UP * 0.08), run_time=0.6)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(promise, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, big, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: from the cosmic to the microscopic -------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("One Notation for Both Extremes", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sun_grp = at(sun(0.28), -2.60, 1.98)
            big = at(law_card(board_text("300,000,000 m", 24, CHALK_WHITE,
                                         "BOLD"),
                              "the Sun's distance", CHALK_WHITE, width=3.30,
                              height=1.10), -2.60, 0.92)
            wire = at(chip_icon(0.58), 3.40, 1.98)
            small = at(law_card(board_text("0.000003 m", 24, CHALK_WHITE,
                                           "BOLD"),
                                "the wire in a chip", CHALK_WHITE, width=3.30,
                                height=1.10), 3.40, 0.92)
            zoom = DoubleArrow(np.array([-0.85, 0.92, 0.0]),
                               np.array([1.65, 0.92, 0.0]), buff=0,
                               stroke_width=3.0, color=CHALK_WHITE,
                               max_tip_length_to_length_ratio=0.10)
            zoom_lab = at(board_text("same notation", 13, CHALK_WHITE, "BOLD"),
                          BOARD_CX, 0.42)
            question = at(board_text("Can one notation handle both?", 19,
                                     CHALK_PINK, "BOLD"), BOARD_CX, 1.98)
            ans_big = at(chalk_math(r"= 3 \times 10^8", size=30,
                                    color=CHALK_CYAN), -2.60, -0.40)
            ans_small = at(chalk_math(r"= 3 \times 10^{-6}", size=30,
                                      color=CHALK_YELLOW), 3.40, -0.40)
            strip = at(board_text("The exponent tells the scale.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(sun_grp, scale=0.8), FadeIn(big, shift=UP * 0.08),
                      run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(wire, scale=0.8), FadeIn(small, shift=UP * 0.08),
                      FadeIn(question, shift=UP * 0.08), run_time=0.6)
            self.play(GrowArrow(zoom), FadeIn(zoom_lab), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(ans_big, shift=UP * 0.08),
                      FadeIn(ans_small, shift=UP * 0.08), run_time=0.6)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, question, color=CHALK_PINK)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: powers of ten are a scale ----------------------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Exponent Tells the Scale", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            ruler = scale_marks([-3, -2, -1, 0, 1, 2, 3])
            left_tag = at(board_text("\u2190  SMALLER", 15, CHALK_PINK, "BOLD"),
                          -3.20, 1.95)
            right_tag = at(board_text("LARGER  \u2192", 15, CHALK_GREEN, "BOLD"),
                           4.20, 1.95)
            pos_note = at(chip("positive exponent: large scale", CHALK_GREEN,
                               size=16), 2.65, -0.95)
            neg_note = at(chip("negative exponent: small scale", CHALK_PINK,
                               size=16), -1.85, -0.95)
            strip = at(board_text("POWERS OF TEN ARE A SCALE.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(ruler.axis), FadeIn(ruler.ticks[3]),
                      FadeIn(VGroup(ruler.labels[6], ruler.labels[7])),
                      run_time=0.7)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(VGroup(*ruler.ticks[4:]), scale=0.85),
                      FadeIn(VGroup(*ruler.labels[8:])),
                      FadeIn(right_tag, shift=LEFT * 0.08), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(VGroup(*ruler.ticks[:3]), scale=0.85),
                      FadeIn(VGroup(*ruler.labels[:6])),
                      FadeIn(left_tag, shift=RIGHT * 0.08), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(pos_note, scale=0.9), FadeIn(neg_note, scale=0.9),
                      run_time=0.55)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: 300 000 000 -> 3 x 10^8 ------------------------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Large \u2192 Positive Exponent", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            track, marker, counter, label = self.elevator("300000000", 9)
            result = at(chalk_math(r"3 \times 10^8", size=36,
                                   color=CHALK_GREEN), BOARD_CX, -0.05)
            rule = at(chip("decimal moved LEFT 8 places \u2192 +8", CHALK_GREEN,
                           size=17), BOARD_CX, -0.95)
            strip = at(board_text("MOVE LEFT, COUNT, EXPONENT IS POSITIVE.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(track), FadeIn(marker, scale=0.8),
                      FadeIn(counter), FadeIn(label), run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.run_elevator(tracker, "b1", track, marker, counter, 1,
                              next_mark="b2")

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(result, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(rule, scale=0.9), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, result, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: 6 020 000 000 -> 6.02 x 10^9 -------------------------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("Count the Moves", 22, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            track, marker, counter, label = self.elevator("6020000000", 10)
            rings = VGroup(*[SurroundingRectangle(track.glyphs[i], buff=0.05,
                                                  color=CHALK_GREEN,
                                                  stroke_width=2.6)
                             for i in range(3)])
            result = at(chalk_math(r"6.02 \times 10^9", size=36,
                                   color=CHALK_GREEN), BOARD_CX, -0.05)
            keep = at(chip("the digits we keep: 602", CHALK_GREEN, size=16),
                      3.60, -0.95)
            strip = at(board_text("LARGE NUMBER \u2192 POSITIVE EXPONENT.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(track), FadeIn(marker, scale=0.8),
                      FadeIn(counter), FadeIn(label), run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.run_elevator_marked(tracker, [f"b{k}" for k in range(2, 11)],
                                     track, marker, counter, direction=-1)

            self.wait(leftover(tracker, "b11"))
            self.play(FadeIn(rings), run_time=0.5)
            self.play(FadeIn(keep, scale=0.9), run_time=0.45)

            self.wait(leftover(tracker, "b12"))
            self.play(FadeIn(result, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, result, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: 0.000003 -> 3 x 10^-6 --------------------------------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("Small \u2192 Negative Exponent", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            track, marker, counter, label = self.elevator(
                "0000003", 1, label_x=-2.30)
            result = at(chalk_math(r"3 \times 10^{-6}", size=36,
                                   color=CHALK_YELLOW), BOARD_CX, -0.05)
            signed = at(chip("six places, and the exponent is \u22126",
                             CHALK_PINK, size=16), BOARD_CX, -0.95)
            strip = at(board_text("SMALL NUMBER \u2192 NEGATIVE EXPONENT.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            wire = at(chip_icon(0.54), 4.15, 1.55)
            wire_lab = at(board_text("a wire in a chip", 13, CHALK_CYAN, "BOLD"),
                          4.15, 0.90)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(track), FadeIn(marker, scale=0.8),
                      FadeIn(counter), FadeIn(label), run_time=0.6)
            self.play(FadeIn(wire, scale=0.85), FadeIn(wire_lab),
                      run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.run_elevator(tracker, "b1", track, marker, counter, 7,
                              next_mark="b2")

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(result, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(signed, scale=0.9), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, result, color=CHALK_YELLOW)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: 0.00001275 -> 1.275 x 10^-5 --------------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("Keep the Digits \u2014 Change the Scale",
                                    21, CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            track, marker, counter, label = self.elevator(
                "000001275", 1, label_x=-2.55)
            rings = VGroup(*[SurroundingRectangle(track.glyphs[i], buff=0.05,
                                                  color=CHALK_CYAN,
                                                  stroke_width=2.6)
                             for i in range(5, 9)])
            result = at(chalk_math(r"1.275 \times 10^{-5}", size=34,
                                   color=CHALK_CYAN), BOARD_CX, -0.05)
            same = at(chip("same quantity, different representation",
                           CHALK_CYAN, size=16), BOARD_CX, -0.95)
            strip = at(board_text("KEEP THE DIGITS \u2014 CHANGE THE SCALE.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            cell = at(plant_cell(0.98, 0.74), 4.10, 1.60)
            cell_lab = at(board_text("a plant cell", 13, CHALK_GREEN, "BOLD"),
                          4.10, 0.95)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(track), FadeIn(marker, scale=0.8),
                      FadeIn(counter), FadeIn(label), run_time=0.6)
            self.play(FadeIn(cell, scale=0.85), FadeIn(cell_lab),
                      FadeIn(rings), run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.run_elevator_marked(tracker, [f"b{k}" for k in range(2, 7)],
                                     track, marker, counter, direction=1)

            self.wait(leftover(tracker, "b7"))
            self.play(FadeIn(result, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(same, scale=0.9), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, result, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: standard form back to usual form ---------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Standard Form \u2192 Usual Form", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            row1 = at(card(VGroup(
                chalk_math(r"4.67 \times 10^4 = 46700", size=28,
                           color=CHALK_CYAN),
                board_text("positive \u2192 decimal right 4", 14, CHALK_GREEN,
                           "BOLD")).arrange(RIGHT, buff=0.60),
                CHALK_CYAN, pad_y=0.24), BOARD_CX, 1.35)
            row2 = at(card(VGroup(
                chalk_math(r"3.02 \times 10^{-6} = 0.00000302", size=24,
                           color=CHALK_PINK),
                board_text("negative \u2192 decimal left 6", 14, CHALK_PINK,
                           "BOLD")).arrange(RIGHT, buff=0.60),
                CHALK_PINK, pad_y=0.24), BOARD_CX, 0.05)
            warn = at(chip("these directions are for the reverse conversion",
                           CHALK_YELLOW, size=16), BOARD_CX, -1.05)
            strip = at(board_text("POSITIVE \u2192 RIGHT;  NEGATIVE \u2192 "
                                  "LEFT.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(row1, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(row2, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(warn, scale=0.9), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, warn)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the complete map -------------------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("Which Direction Am I Converting?", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            rows = VGroup(
                at(card(VGroup(
                    chalk_math(r"6020000000 \rightarrow 6.02 \times 10^9",
                               size=20, color=CHALK_WHITE),
                    board_text("large: decimal left \u2192 positive", 13,
                               CHALK_GREEN, "BOLD")).arrange(RIGHT, buff=0.55),
                    CHALK_GREEN, pad_y=0.22), BOARD_CX, 1.75),
                at(card(VGroup(
                    chalk_math(r"0.00001275 \rightarrow 1.275 \times 10^{-5}",
                               size=20, color=CHALK_WHITE),
                    board_text("small: decimal right \u2192 negative", 13,
                               CHALK_PINK, "BOLD")).arrange(RIGHT, buff=0.55),
                    CHALK_PINK, pad_y=0.22), BOARD_CX, 0.85),
                at(card(VGroup(
                    chalk_math(r"4.67 \times 10^4 \rightarrow 46700", size=20,
                               color=CHALK_WHITE),
                    board_text("positive \u2192 decimal right", 13, CHALK_GREEN,
                               "BOLD")).arrange(RIGHT, buff=0.55),
                    CHALK_GREEN, pad_y=0.22), BOARD_CX, -0.05),
                at(card(VGroup(
                    chalk_math(r"3.02 \times 10^{-6} \rightarrow 0.00000302",
                               size=20, color=CHALK_WHITE),
                    board_text("negative \u2192 decimal left", 13, CHALK_PINK,
                               "BOLD")).arrange(RIGHT, buff=0.55),
                    CHALK_PINK, pad_y=0.22), BOARD_CX, -0.95),
            )
            strip = at(board_text("FIRST ASK WHICH WAY YOU ARE CONVERTING.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(rows[0], shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(rows[1], shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(rows[2], shift=UP * 0.08),
                      FadeIn(rows[3], shift=UP * 0.08), run_time=0.6)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 9: your turn -- three conversions, then the 10-second clock ---
    def beat_s9(self) -> None:
        with self.voiceover(text=NARRATION["s9q"]) as tracker:
            self.reset_board()

            heading = at(board_text("YOUR TURN", 26, CHALK_PINK, "BOLD"),
                         BOARD_CX, ROW_Y)
            qa = at(q_card("small \u2192 standard form",
                           chalk_math("0.0000456", size=20, color=CHALK_WHITE)),
                    -2.55, 1.45)
            qb = at(q_card("large \u2192 standard form",
                           chalk_math("6020000000", size=18,
                                      color=CHALK_WHITE)),
                    3.55, 1.45)
            qc = at(q_card("standard \u2192 usual form",
                           chalk_math(r"5.8 \times 10^{7}", size=20,
                                      color=CHALK_WHITE)),
                    -2.55, 0.20)

            ans_a = at(answer_row("A",
                                  chalk_math(r"0.0000456 = 4.56 \times 10^{-5}",
                                             26, color=CHALK_CYAN),
                                  "right 5 places", CHALK_CYAN),
                       BOARD_CX, 1.55)
            ans_b = at(answer_row("B",
                                  chalk_math(r"6020000000 = 6.02 \times 10^9",
                                             26, color=CHALK_YELLOW),
                                  "left 9 places", CHALK_YELLOW),
                       BOARD_CX, 0.70)
            ans_c = at(answer_row("C",
                                  chalk_math(r"5.8 \times 10^{7} = 58000000", 26,
                                             color=CHALK_PINK),
                                  "right 7 places", CHALK_PINK),
                       BOARD_CX, -0.15)
            done = at(board_text("SMALL \u2192 NEGATIVE   \u00b7   LARGE \u2192 "
                                 "POSITIVE", 18, CHALK_YELLOW, "BOLD"),
                      BOARD_CX, -1.05)
            strip = at(board_text("MOVE, COUNT, CHOOSE THE SIGN, WRITE.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.5)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(q, shift=RIGHT * 0.10)
                                    for q in (qa, qb, qc)], lag_ratio=0.22),
                      run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)

            self._capture_srt(tracker)

        # The ten-second THINK pause is deliberately SILENT -- the
        # questions have just been read, so the clock ticks alone, with
        # no narration to sync against.
        play_challenge_countdown(self, seconds=10, sfx=self.sfx,
                                 position=np.array([BOARD_CX, BOARD_CY, 0]))

        with self.voiceover(text=NARRATION["s9a"]) as tracker:

            self.wait(leftover(tracker, "b0"))
            self.play(FadeOut(qa), FadeOut(qb), FadeOut(qc), run_time=0.5)
            self.play(FadeIn(ans_a, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(ans_b, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(ans_c, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(done, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, done)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap -----------------------------------------------------
    def beat_s10(self) -> None:
        with self.voiceover(text=NARRATION["s10"]) as tracker:
            self.reset_board()

            heading = at(board_text("Move \u2192 Count \u2192 Sign \u2192 Write",
                                    22, CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            steps = at(VGroup(
                chip("MOVE", CHALK_CYAN, size=16),
                chip("COUNT", CHALK_CYAN, size=16),
                chip("CHOOSE THE SIGN", CHALK_YELLOW, size=16),
                chip("WRITE  \u00d7 10\u207f", CHALK_YELLOW, size=16),
            ).arrange(RIGHT, buff=0.32), BOARD_CX, 1.35)
            big = at(chalk_math(r"300,000,000 = 3 \times 10^8", size=30,
                                color=CHALK_CYAN), BOARD_CX, 0.35)
            small = at(chalk_math(r"0.000003 = 3 \times 10^{-6}", size=30,
                                  color=CHALK_YELLOW), BOARD_CX, -0.45)
            strip = at(board_text("POWERS OF 10 WRITE THE VERY LARGE AND THE "
                                  "VERY SMALL.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            thanks = at(board_text("Thank You for Watching!", 30, CHALK_WHITE,
                                   "BOLD"), BOARD_CX, 0.62)
            bye = at(board_text("See you in the next lesson :)", 22,
                                CHALK_YELLOW, "BOLD"), BOARD_CX, -0.32)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(steps, shift=UP * 0.08),
                      FadeIn(big, shift=UP * 0.08), run_time=0.7)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(small, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["success"], gain=-11)

            # the closing card is narrated: it appears as the voice says
            # "Thank you for watching the chapter,", the goodbye line as the
            # voice says "and see you in the next lesson."
            self.wait(leftover(tracker, "b3"))
            self.play(FadeOut(heading), FadeOut(steps), FadeOut(big),
                      FadeOut(small), FadeOut(strip), run_time=0.5)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.5)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.closing(tracker, thanks, run_time=1.2)
            self._capture_srt(tracker)

        self.wait(END_HOLD)







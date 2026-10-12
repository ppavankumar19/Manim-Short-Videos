"""
Understanding Negative Exponents: Reciprocal Rules and Multiplicative Inverses
Story-mode chalkboard lesson (Telangana Class 8 Maths, Chapter 4:
Exponents and Powers, Storymode 02).

LLM KEY / FUNCTION NAME: laws_of_exponents_power_product_quotient_zero

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


# Board layout shared by every scene of this video.
ROW_Y = 2.72             # every scene heading sits on this line
BANNER_Y = -1.30         # the closing banner, above the strip
# The burned-in caption grows up from the bottom of the frame: a one-line cue
# starts at y = -3.38 and a wrapped two-line cue reaches y = -2.93 (measured on
# the series' own burned 360p cuts), so every closing strip sits at -1.80 and
# nothing at all sits below y = -2.00 -- audited by the IN-CAPTION-BAND check.
STRIP_Y = -1.80

TILE_W = 0.42            # one factor block
TILE_H = 0.52
TILE_BUFF = 0.09
PANEL_FILL = "#16202B"

GRID_DX = 2.85           # the two columns of every four-cell dashboard
GRID_X = (0.5 - GRID_DX, 0.5 + GRID_DX)
GRID_DY = 1.60           # the two rows of it
GRID_Y = (1.25, -0.35)


# ---------------------------------------------------------------- furniture --
def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


def tile(label, color=CHALK_WHITE, size=22, w=TILE_W, h=TILE_H, fill=0.55):
    """One copy of the base as a factor block."""
    lab = chalk_math(label, size=size, color=color)
    box = RoundedRectangle(corner_radius=0.06, width=w, height=h,
                           stroke_color=color, stroke_width=1.8,
                           fill_color=PANEL_FILL, fill_opacity=fill)
    lab.move_to(box.get_center())
    grp = VGroup(box, lab)
    grp.label = lab
    return grp


def tile_run(n, label="2", color=CHALK_WHITE, size=22, buff=TILE_BUFF):
    """`n` factor blocks in a row: returns (group, [tiles])."""
    tiles = [tile(label, color, size=size) for _ in range(n)]
    grp = VGroup(*tiles).arrange(RIGHT, buff=buff)
    grp.tiles = list(grp)
    return grp, list(grp)


def cancel_mark(target, color=CHALK_RED, width=3.4, pad=0.04):
    """The red slash that cancels one factor block."""
    a = target.get_corner(np.array([-1.0, -1.0, 0.0])) + np.array([-pad, -pad, 0])
    b = target.get_corner(np.array([1.0, 1.0, 0.0])) + np.array([pad, pad, 0])
    return Line(a, b, color=color, stroke_width=width)


def frac_bar(x_left, x_right, y, color=CHALK_WHITE, width=2.6):
    """A quotient's fraction bar."""
    return Line(np.array([x_left, y, 0.0]), np.array([x_right, y, 0.0]),
                color=color, stroke_width=width)


def card(mob, color=CHALK_WHITE, pad_x=0.54, pad_y=0.38, fill=0.55,
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
    """One dashboard cell: the law, with its one-line rule underneath.

    `math_up` / `note_down` are tightened for a card that has to stay clear of
    the caption band below it."""
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


def q_card(title, body, color=CHALK_CYAN, width=3.7, height=0.78,
           head_up=0.20, body_down=0.16):
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


def mark_no(size=1.0, color=CHALK_RED):
    """A drawn chalk cross (the board font has no cross glyph)."""
    cross = VGroup(
        Line(np.array([-0.10, -0.10, 0.0]), np.array([0.10, 0.10, 0.0])),
        Line(np.array([-0.10, 0.10, 0.0]), np.array([0.10, -0.10, 0.0])),
    ).set_stroke(color=color, width=4.2)
    cross.scale(size)
    return cross


# ----------------------------------------------------------------


NARRATION = {
    "title": (
        "Advanced laws of exponents. <bookmark mark='b0'/>Power of a power, "
        "power of a product, power of a fraction, and the zero exponent. "
        "<bookmark mark='b1'/>First recognise the structure, then choose the "
        "law."
    ),
    "s1": (
        "In the last video we multiplied powers with the same base and added "
        "the exponents. <bookmark mark='b0'/>But look at this: a to the power "
        "m, all raised to the power n. <bookmark mark='b1'/>Should we add the "
        "exponents again? <bookmark mark='b2'/>The structure is different, so "
        "the rule is different. First recognise the structure."
    ),
    "s2": (
        "Take a small example: two cubed, all squared. <bookmark mark='b0'/>"
        "The inner power is three factors of two: one group. <bookmark "
        "mark='b1'/>The outer exponent two makes two copies of that whole "
        "group. <bookmark mark='b2'/>So there are two groups with three "
        "factors each: six factors altogether. That is two to the power six, "
        "because three times two is six. <bookmark mark='b3'/>So a power "
        "raised to another power multiplies the exponents."
    ),
    "s3": (
        "Now with letters. <bookmark mark='b0'/>A to the power m, all raised "
        "to the power n, means n copies of a to the power m. <bookmark "
        "mark='b1'/>That is m plus m plus m, n times over, which is m times n "
        "factors of a. <bookmark mark='b2'/>So the exponents multiply: a to "
        "the power m, all raised to the power n, is a to the power m n."
    ),
    "s4": (
        "Next, a product inside the brackets: two times three, all to the "
        "power four. <bookmark mark='b0'/>The outer exponent four makes four "
        "copies of the bracket. <bookmark mark='b1'/>Now regroup: all the twos "
        "together, and all the threes together. <bookmark mark='b2'/>That "
        "gives two to the power four times three to the power four. <bookmark "
        "mark='b3'/>In general, a b all to the power m is a to the power m "
        "times b to the power m: the exponent reaches every factor."
    ),
    "s5": (
        "Fractions work the same way: two fifths, all cubed. <bookmark "
        "mark='b0'/>That is two fifths, times two fifths, times two fifths. "
        "<bookmark mark='b1'/>The numerators group: two times two times two, "
        "which is two cubed. The denominators group: five times five times "
        "five, which is five cubed. <bookmark mark='b2'/>A fraction inside "
        "brackets is powered on the top and on the bottom."
    ),
    "s6": (
        "Why is any non-zero number to the power zero equal to one? <bookmark "
        "mark='b0'/>Start with a to the power four over a to the power four. "
        "<bookmark mark='b1'/>By ordinary division, anything divided by itself "
        "is one. <bookmark mark='b2'/>But by the quotient law the exponents "
        "subtract: four minus four is zero, so it is also a to the power zero. "
        "<bookmark mark='b3'/>Both answers describe the same quantity, so a to "
        "the power zero is one, for any non-zero a."
    ),
    "s7": (
        "Now look at the four shapes together. <bookmark mark='b0'/>A power "
        "raised to another power: multiply the exponents. <bookmark "
        "mark='b1'/>A product inside brackets: distribute the power to both "
        "factors. <bookmark mark='b2'/>A fraction inside brackets: power the "
        "top and the bottom. And an exponent of zero: the answer is simply one."
    ),
    "s8": (
        "Four mistakes to avoid. <bookmark mark='b0'/>First: x squared, all "
        "cubed, is x to the power six, not x to the power five, because the "
        "exponents multiply. <bookmark mark='b1'/>Second: a b all cubed is a "
        "cubed b cubed, not a cubed b. <bookmark mark='b2'/>Third: a over b, "
        "all squared, is a squared over b squared. <bookmark mark='b3'/>And "
        "fourth: seven to the power zero is one, not zero."
    ),
    "s9q": (
        "Your turn. <bookmark mark='b0'/>Four questions, one for each law. Simplify "
        "three to the power four, all squared. Simplify five x, all cubed. Simplify "
        "three sevenths, all squared. And work out minus six, all to the power zero."
    ),
    "s9a": (
        "<bookmark mark='b0'/>Three to the power four, all squared, multiplies the "
        "exponents: three to the power eight. <bookmark mark='b1'/>Five x, all cubed, "
        "is five cubed x cubed: one hundred and twenty five x cubed. <bookmark "
        "mark='b2'/>Three sevenths squared is three squared over seven squared, that "
        "is nine over forty nine. And minus six to the power zero is one."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>A power of a power multiplies the "
        "exponents. A power of a product distributes to every factor. <bookmark "
        "mark='b1'/>A power of a fraction powers the top and the bottom. And any "
        "non-zero base to the power zero is one. <bookmark mark='b2'/>See the "
        "structure, then choose the law. <bookmark mark='b3'/>Thank you for watching, "
        "<bookmark mark='b4'/>and see you in the next lesson."
    ),
}


class AdvancedExponentLawsStory(VoiceoverScene):
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
        out_dir = _HERE / "media" / "videos" / "laws_of_exponents_power_product_quotient_zero"
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
    # Advanced Laws of Exponents (Class 8, Chapter 4, Storymode 04).
    #
    # SYNC RULE for every reveal: wait for the narration bookmark that ends the
    # phrase describing a thing, and only then bring it on.  Playing first and
    # waiting afterwards shows the picture a whole window early, which reads as
    # broken sync.
    #
    # Layout rules, so the audits stay clean:
    #   * the heading sits on ROW_Y (2.72), the closing strip on STRIP_Y (-1.80);
    #     nothing at all sits below y = -2.00;
    #   * the visual identity is "the exponent knows what is inside the brackets":
    #     the outer exponent duplicates the whole group, splits horizontally over
    #     a product, splits vertically over a fraction, and the zero-exponent
    #     scene reuses storymode 03's cancellation;
    #   * nothing is placed on a line, and no card, tile or chip is placed over
    #     another element -- checked by audit_clearance.py and
    #     audit_sync_overlap.py;
    #   * the challenge uses the series' shared 10-second THINK clock, dead
    #     centre of the board, with the question cards on the LEFT while it runs.
    ROW_Y = 2.72
    BANNER_Y = -1.30
    STRIP_Y = -1.80

    def closing(self, tracker, mob=None, color=CHALK_YELLOW, run_time=None):
        """Consume the tail of the narration window on the last reveal."""
        budget = rt(tracker.get_remaining_duration()) if run_time is None \
            else run_time
        if mob is None:
            self.wait(max(budget, 0.0))
        else:
            self.play(Indicate(mob, color=color, scale_factor=1.03),
                      run_time=max(budget, MIN_RT))

    def chain_positions(self, n, y, cx=None):
        """The x centres of an n-tile chain centred on the board."""
        cx = BOARD_CX if cx is None else cx
        width = n * TILE_W + (n - 1) * TILE_BUFF
        x0 = cx - width / 2.0 + TILE_W / 2.0
        return [np.array([x0 + i * (TILE_W + TILE_BUFF), y, 0.0])
                for i in range(n)]

    # -- Scene 0: title ------------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            heading = at(board_text("Advanced Laws of Exponents", 26,
                                    CHALK_WHITE, "BOLD"), BOARD_CX, 2.15)
            sub = at(board_text("Power of a Power  \u00b7  Product  \u00b7  "
                                "Fraction  \u00b7  Zero", 16, CHALK_AMBER,
                                "BOLD"), BOARD_CX, 1.50)
            laws = VGroup(
                at(chalk_math(r"(a^m)^n = a^{mn}", size=28, color=CHALK_CYAN),
                   GRID_X[0], 0.85),
                at(chalk_math(r"(ab)^m = a^m b^m", size=28,
                              color=CHALK_YELLOW), GRID_X[1], 0.85),
                at(chalk_math(r"(a/b)^m = a^m/b^m", size=28, color=CHALK_PINK),
                   GRID_X[0], -0.15),
                at(chalk_math(r"a^0 = 1", size=28, color=CHALK_GREEN),
                   GRID_X[1], -0.15),
            )
            promise = at(board_text("See the structure, then choose the law.",
                                    16, CHALK_WHITE, "BOLD"),
                         BOARD_CX, -1.05)
            strip = at(board_text("Four new laws, four different structures.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(sub, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.08) for m in laws],
                                  lag_ratio=0.25), run_time=1.1)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(promise, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, laws, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: one chapter, different structures ---------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("Same Exponents, Different Structures", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            same_base = at(law_card(chalk_math(r"a^m \times a^n", size=28,
                                               color=CHALK_WHITE),
                                    "video 3: same-base product", CHALK_WHITE,
                                    width=4.0, height=1.40),
                           GRID_X[0], 1.45)
            power = at(law_card(chalk_math(r"(a^m)^n", size=28,
                                           color=CHALK_CYAN),
                                "power of a power", CHALK_CYAN,
                                width=4.0, height=1.40),
                       GRID_X[1], 1.45)
            product = at(law_card(chalk_math(r"(ab)^m", size=28,
                                             color=CHALK_YELLOW),
                                  "power of a product", CHALK_YELLOW,
                                  width=4.0, height=1.40),
                         GRID_X[0], -0.15)
            fraction = at(law_card(chalk_math(r"(a/b)^m", size=28,
                                              color=CHALK_PINK),
                                   "power of a fraction", CHALK_PINK,
                                   width=4.0, height=1.40),
                          GRID_X[1], -0.15)
            query = at(chalk_math("?", size=40, color=CHALK_PINK),
                       BOARD_CX, 1.45)
            banner = at(board_text("First recognise the structure.", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The shape decides the rule.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(same_base, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(power, shift=UP * 0.08), FadeIn(query, scale=0.7),
                      run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(product, shift=UP * 0.08),
                      FadeIn(fraction, shift=UP * 0.08), run_time=0.6)
            self.play(FadeIn(banner, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: power of a power -- the groups duplicate -------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("Groups \u00d7 Factors in Each Group", 21,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            start = at(chalk_math(r"(2^3)^2", size=38, color=CHALK_WHITE),
                       BOARD_CX, 1.95)
            run_a, tiles_a = tile_run(3, "2", CHALK_CYAN)
            run_b, tiles_b = tile_run(3, "2", CHALK_PINK)
            at(run_a, -0.75, 1.10)
            at(run_b, 1.75, 1.10)
            lab_a = at(board_text("3 factors", 14, CHALK_CYAN, "BOLD"),
                       -2.75, 1.10)
            lab_b = at(board_text("3 factors", 14, CHALK_PINK, "BOLD"),
                       3.75, 1.10)
            maths = at(chalk_math(r"2 \times 3 = 6", size=26, color=CHALK_YELLOW),
                       BOARD_CX, 0.25)
            groups = at(chip("2 groups \u00d7 3 factors", CHALK_CYAN, size=15),
                        3.60, 0.25)
            law = at(card(chalk_math(r"(a^m)^n = a^{mn}", size=32,
                                     color=CHALK_GREEN), CHALK_GREEN),
                     BOARD_CX, -0.80)
            strip = at(board_text("POWER OF A POWER \u2014 MULTIPLY THE "
                                  "EXPONENTS.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(start, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(run_a, shift=UP * 0.08), FadeIn(lab_a),
                      run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(run_b, shift=UP * 0.08), FadeIn(lab_b),
                      run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            targets = self.chain_positions(6, 1.10)
            self.play(*[t.animate.move_to(p) for t, p in
                        zip(list(tiles_a) + list(tiles_b), targets)],
                      FadeOut(lab_a), FadeOut(lab_b), run_time=0.8)
            self.play(FadeIn(maths, shift=UP * 0.08), FadeIn(groups, scale=0.85),
                      run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(law, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, law, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: the general power-of-a-power law ---------------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Multiply the Exponents", 23, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            start = at(chalk_math(r"(a^m)^n", size=54, color=CHALK_WHITE),
                       BOARD_CX, 1.85)
            copies = at(chip("n copies of a to the power m", CHALK_CYAN,
                             size=16), BOARD_CX, 0.95)
            added = at(chalk_math(r"m + m + \cdots + m = mn", size=32,
                                  color=CHALK_YELLOW), BOARD_CX, 0.00)
            law = at(card(chalk_math(r"(a^m)^n = a^{mn}", size=32,
                                     color=CHALK_GREEN), CHALK_GREEN),
                     BOARD_CX, -1.00)
            mult = at(chip("multiply, never add", CHALK_GREEN, size=15),
                      3.85, -1.00)
            strip = at(board_text("NEVER ADD THE EXPONENTS HERE.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(start, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(copies, scale=0.85), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(added, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(law, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(mult, scale=0.85), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, law, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: power of a product -- the exponent splits horizontally -----
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Exponent Reaches Every Factor", 21,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            start = at(chalk_math(r"(2 \times 3)^4", size=38, color=CHALK_WHITE),
                       BOARD_CX, 2.00)
            copies = at(chalk_math(r"(2 \times 3)(2 \times 3)(2 \times 3)"
                                   r"(2 \times 3)", size=24, color=CHALK_WHITE),
                        BOARD_CX, 1.10)
            twos = at(chalk_math(r"2 \times 2 \times 2 \times 2 = 2^4", size=28,
                                 color=CHALK_CYAN), BOARD_CX, 0.40)
            threes = at(chalk_math(r"3 \times 3 \times 3 \times 3 = 3^4", size=28,
                                   color=CHALK_PINK), BOARD_CX, -0.30)
            law = at(card(chalk_math(r"(ab)^m = a^m b^m", size=32,
                                     color=CHALK_GREEN), CHALK_GREEN),
                     BOARD_CX, -1.30)
            dist = at(chip("distribute the power", CHALK_GREEN, size=15),
                      3.90, -1.30)
            strip = at(board_text("THE OUTER EXPONENT APPLIES TO BOTH.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(start, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(copies, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(twos, shift=UP * 0.08),
                      FadeIn(threes, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(law, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(dist, scale=0.85), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, law, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: power of a fraction -- the exponent splits vertically ------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("Power the Top and the Bottom", 21,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            start = at(chalk_math(r"(2/5)^3", size=44, color=CHALK_WHITE),
                       BOARD_CX, 1.85)
            law = at(law_card(chalk_math(r"(a/b)^m = a^m/b^m", size=24,
                                         color=CHALK_GREEN),
                              "top and bottom", CHALK_GREEN,
                              width=2.60, height=1.00), 3.85, 1.85)
            copies = at(chalk_math(r"(2/5) \times (2/5) \times (2/5)", size=30,
                                   color=CHALK_WHITE), BOARD_CX, 0.80)
            grouped = at(chalk_math(r"\frac{2 \times 2 \times 2}{5 \times 5 "
                                    r"\times 5} = \frac{2^3}{5^3}", size=28,
                                    color=CHALK_CYAN), BOARD_CX, -0.55)
            strip = at(board_text("POWER THE NUMERATOR AND THE DENOMINATOR.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(start, shift=UP * 0.08),
                      FadeIn(law, scale=0.9), run_time=0.6)
            self.play(FadeIn(copies, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(grouped, shift=UP * 0.08), run_time=0.65)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, grouped, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: why a non-zero number to the power zero is one -------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("Zero Exponent Does Not Mean Zero", 21,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            one = at(chalk_math(r"\frac{a^4}{a^4} = 1", size=34,
                                color=CHALK_GREEN), BOARD_CX, 1.70)
            quotient = at(chalk_math(r"\frac{a^4}{a^4} = a^{4-4} = a^0",
                                     size=32, color=CHALK_CYAN),
                          BOARD_CX, 0.45)
            minus = at(chalk_math(r"4 - 4 = 0", size=30, color=CHALK_YELLOW),
                       BOARD_CX, -0.45)
            law = at(law_card(chalk_math("a^0 = 1", size=30, color=CHALK_GREEN),
                              "for any non-zero a", CHALK_GREEN,
                              width=4.00, height=1.05, math_up=0.26,
                              note_down=0.32), BOARD_CX, -1.40)
            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(one, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(quotient, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(minus, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(law, scale=0.9), run_time=0.5)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, law, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: which law should I use? ------------------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Structure Chooses the Law", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            lanes = VGroup(
                at(law_card(chalk_math(r"(a^m)^n", size=28, color=CHALK_CYAN),
                            "power on power \u2192 multiply", CHALK_CYAN),
                   GRID_X[0], GRID_Y[0]),
                at(law_card(chalk_math(r"(ab)^m", size=28,
                                       color=CHALK_YELLOW),
                            "product \u2192 distribute", CHALK_YELLOW),
                   GRID_X[1], GRID_Y[0]),
                at(law_card(chalk_math(r"(a/b)^m", size=28, color=CHALK_PINK),
                            "fraction \u2192 top and bottom", CHALK_PINK),
                   GRID_X[0], GRID_Y[1]),
                at(law_card(chalk_math(r"a^0", size=28, color=CHALK_GREEN),
                            "zero exponent \u2192 one", CHALK_GREEN),
                   GRID_X[1], GRID_Y[1]),
            )
            strip = at(board_text("RECOGNISE FIRST, THEN APPLY.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(lanes[0], shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(lanes[1], shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(lanes[2], shift=UP * 0.08),
                      FadeIn(lanes[3], shift=UP * 0.08), run_time=0.6)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, lanes, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: four mistakes to avoid -------------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("Don't Mix the Rules", 22, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            arrow = board_text("\u2192", 20, CHALK_WHITE, "BOLD")
            row1 = at(card(VGroup(
                chalk_math(r"(x^2)^3 = x^{2+3} = x^5", size=24,
                           color=CHALK_RED),
                mark_no(0.85),
                arrow.copy(),
                chalk_math(r"x^6", size=26, color=CHALK_GREEN)
            ).arrange(RIGHT, buff=0.36), CHALK_RED, pad_y=0.22),
                BOARD_CX, 1.85)
            row2 = at(card(VGroup(
                chalk_math(r"(ab)^3 = a^3 b", size=24, color=CHALK_RED),
                mark_no(0.85),
                arrow.copy(),
                chalk_math(r"a^3 b^3", size=26, color=CHALK_GREEN)
            ).arrange(RIGHT, buff=0.36), CHALK_RED, pad_y=0.22),
                BOARD_CX, 1.00)
            row3 = at(card(VGroup(
                chalk_math(r"(a/b)^2 = a^2/b", size=24, color=CHALK_RED),
                mark_no(0.85),
                arrow.copy(),
                chalk_math(r"a^2/b^2", size=26, color=CHALK_GREEN)
            ).arrange(RIGHT, buff=0.36), CHALK_RED, pad_y=0.22),
                BOARD_CX, -0.05)
            row4 = at(card(VGroup(
                chalk_math(r"7^0 = 0", size=24, color=CHALK_RED),
                mark_no(0.85),
                arrow.copy(),
                chalk_math(r"1", size=26, color=CHALK_GREEN)
            ).arrange(RIGHT, buff=0.36), CHALK_RED, pad_y=0.22),
                BOARD_CX, -1.05)
            strip = at(board_text("LOOK AT THE WHOLE EXPRESSION.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(row1, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(row2, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(row3, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(row4, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 9: your turn -- four questions, then the 10-second clock ------
    def beat_s9(self) -> None:
        with self.voiceover(text=NARRATION["s9q"]) as tracker:
            self.reset_board()

            heading = at(board_text("YOUR TURN", 26, CHALK_PINK, "BOLD"),
                         BOARD_CX, ROW_Y)
            qa = at(q_card("power of a power",
                           chalk_math(r"(3^4)^2", size=20, color=CHALK_WHITE),
                           height=0.92, head_up=0.28, body_down=0.22),
                    -2.55, 1.45)
            qb = at(q_card("power of a product",
                           chalk_math(r"(5x)^3", size=20, color=CHALK_WHITE),
                           height=0.92, head_up=0.28, body_down=0.22),
                    3.55, 1.45)
            qc = at(q_card("power of a fraction",
                           chalk_math(r"(3/7)^2", size=20, color=CHALK_WHITE),
                           height=0.92, head_up=0.28, body_down=0.22),
                    -2.55, 0.20)
            qd = at(q_card("zero exponent",
                           chalk_math(r"(-6)^0", size=20, color=CHALK_WHITE),
                           height=0.92, head_up=0.28, body_down=0.22),
                    3.55, 0.20)

            ans_a = at(answer_row("A",
                                  chalk_math(r"(3^4)^2 = 3^{8}", 28,
                                             color=CHALK_CYAN),
                                  "multiply the exponents", CHALK_CYAN),
                       BOARD_CX, 1.55)
            ans_b = at(answer_row("B",
                                  chalk_math(r"(5x)^3 = 5^3 x^3", 28,
                                             color=CHALK_YELLOW),
                                  "distribute the power", CHALK_YELLOW),
                       BOARD_CX, 0.70)
            ans_c = at(answer_row("C",
                                  chalk_math(r"(3/7)^2 = 3^2/7^2 = 9/49", 28,
                                             color=CHALK_PINK),
                                  "top and bottom", CHALK_PINK),
                       BOARD_CX, -0.15)
            ans_d = at(answer_row("D",
                                  chalk_math(r"(-6)^0 = 1", 28,
                                             color=CHALK_GREEN),
                                  "zero exponent", CHALK_GREEN),
                       BOARD_CX, -1.00)
            done = at(board_text("RECOGNISE FIRST, SIMPLIFY SECOND.", 18,
                                 CHALK_YELLOW, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.5)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(q, shift=RIGHT * 0.10)
                                    for q in (qa, qb, qc, qd)],
                                  lag_ratio=0.20), run_time=1.0)
            self.add_sound(self.sfx["pop"], gain=-13)

            self._capture_srt(tracker)

        # The ten-second THINK pause is deliberately SILENT -- the
        # questions have just been read, so the clock ticks alone, with
        # no narration to sync against.
        play_challenge_countdown(self, seconds=10, sfx=self.sfx,
                                 position=np.array([BOARD_CX, BOARD_CY, 0]))

        with self.voiceover(text=NARRATION["s9a"]) as tracker:

            self.wait(leftover(tracker, "b0"))
            self.play(FadeOut(qa), FadeOut(qb), FadeOut(qc), FadeOut(qd),
                      run_time=0.5)
            self.play(FadeIn(ans_a, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(ans_b, shift=UP * 0.08),
                      FadeIn(ans_c, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(ans_d, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(done, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, done)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap -----------------------------------------------------
    def beat_s10(self) -> None:
        with self.voiceover(text=NARRATION["s10"]) as tracker:
            self.reset_board()

            heading = at(board_text("Recognise \u2192 Apply \u2192 Simplify", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            lanes = VGroup(
                at(law_card(chalk_math(r"(a^m)^n = a^{mn}", size=24,
                                       color=CHALK_CYAN),
                            "power on power \u2192 multiply", CHALK_CYAN),
                   GRID_X[0], GRID_Y[0]),
                at(law_card(chalk_math(r"(ab)^m = a^m b^m", size=24,
                                       color=CHALK_YELLOW),
                            "product \u2192 distribute", CHALK_YELLOW),
                   GRID_X[1], GRID_Y[0]),
                at(law_card(chalk_math(r"(a/b)^m = a^m/b^m", size=24,
                                       color=CHALK_PINK),
                            "fraction \u2192 top and bottom", CHALK_PINK),
                   GRID_X[0], GRID_Y[1]),
                at(law_card(chalk_math("a^0 = 1", size=24, color=CHALK_GREEN),
                            "zero exponent \u2192 one", CHALK_GREEN),
                   GRID_X[1], GRID_Y[1]),
            )
            strip = at(board_text("SEE THE STRUCTURE, THEN CHOOSE THE LAW.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            thanks = at(board_text("Thank You for Watching!", 30, CHALK_WHITE,
                                   "BOLD"), BOARD_CX, 0.62)
            bye = at(board_text("See you in the next lesson :)", 22,
                                CHALK_YELLOW, "BOLD"), BOARD_CX, -0.32)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(lanes[0], shift=UP * 0.08),
                      FadeIn(lanes[1], shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(lanes[2], shift=UP * 0.08),
                      FadeIn(lanes[3], shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["success"], gain=-11)

            # the closing card is narrated: it appears as the voice says
            # "Thank you for watching,", the goodbye line as the voice says
            # "and see you in the next lesson."
            self.wait(leftover(tracker, "b3"))
            self.play(FadeOut(heading), FadeOut(lanes), FadeOut(strip),
                      run_time=0.5)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.5)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.closing(tracker, thanks, run_time=1.2)
            self._capture_srt(tracker)

        self.wait(END_HOLD)



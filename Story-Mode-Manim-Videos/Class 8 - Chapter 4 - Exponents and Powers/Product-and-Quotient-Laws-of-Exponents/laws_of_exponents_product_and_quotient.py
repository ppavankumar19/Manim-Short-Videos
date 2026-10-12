"""
Understanding Negative Exponents: Reciprocal Rules and Multiplicative Inverses
Story-mode chalkboard lesson (Telangana Class 8 Maths, Chapter 4:
Exponents and Powers, Storymode 02).

LLM KEY / FUNCTION NAME: laws_of_exponents_product_and_quotient

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
SUB_Y = 2.20             # the one-line sub-heading under it
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
    a, b = target.get_corner(np.array([-1.0, -1.0, 0.0])), \
        target.get_corner(np.array([1.0, 1.0, 0.0]))
    a = a + np.array([-pad, -pad, 0.0])
    b = b + np.array([pad, pad, 0.0])
    return Line(a, b, color=color, stroke_width=width)


def frac_bar(x_left, x_right, y, color=CHALK_WHITE, width=2.6):
    """The fraction bar of a quotient."""
    return Line(np.array([x_left, y, 0.0]), np.array([x_right, y, 0.0]),
                color=color, stroke_width=width)


def mark_no(size=1.0, color=CHALK_RED):
    """A drawn chalk cross (the board font has no cross glyph)."""
    cross = VGroup(
        Line(np.array([-0.10, -0.10, 0.0]), np.array([0.10, 0.10, 0.0])),
        Line(np.array([-0.10, 0.10, 0.0]), np.array([0.10, -0.10, 0.0])),
    ).set_stroke(color=color, width=4.2)
    cross.scale(size)
    return cross


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


def chip(text, color=CHALK_CYAN, size=15, width=None, height=0.50):
    """A small labelled chip."""
    lab = board_text(text, size, color, "BOLD")
    box = RoundedRectangle(corner_radius=0.09,
                           width=width or (lab.width + 0.42), height=height,
                           stroke_color=color, stroke_width=1.7,
                           fill_color=PANEL_FILL, fill_opacity=0.7)
    lab.move_to(box.get_center())
    return VGroup(box, lab)


def zone_card(title, lines, color=CHALK_WHITE, width=4.2, height=2.60,
              title_size=18, line_size=30, note_size=16, note=None):
    """A titled panel holding the power, the arrow note and the result."""
    head = board_text(title, title_size, color, "BOLD")
    body = VGroup(*lines).arrange(DOWN, buff=0.26)
    box = RoundedRectangle(corner_radius=0.12, width=width, height=height,
                           stroke_color=color, stroke_width=2.0,
                           fill_color=PANEL_FILL, fill_opacity=0.55)
    head.move_to(box.get_center() + UP * (height / 2 - 0.30))
    if note is None:
        body.move_to(box.get_center() + DOWN * 0.20)
    else:
        note_mob = board_text(note, note_size, CHALK_YELLOW, "BOLD")
        stack = VGroup(body, note_mob).arrange(DOWN, buff=0.28)
        stack.move_to(box.get_center() + DOWN * 0.30)
        body = stack
    grp = VGroup(box, head, body)
    grp.body = body
    return grp


def q_card(title, body, color=CHALK_CYAN, width=3.7, height=0.92,
           head_up=0.24, body_down=0.22):
    """One 'your turn' question card: the prompt over the expression.

    `head_up` / `body_down` are opened up for a card whose expression is a
    fraction, so the taller math keeps its clearance from the card edge."""
    head = board_text(title, 14, color, "BOLD")
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
        "The product and quotient laws of exponents. <bookmark mark='b0'/>When "
        "powers with the same base are multiplied, the exponents are added. "
        "<bookmark mark='b1'/>When they are divided, the exponents are "
        "subtracted."
    ),
    "s1": (
        "Suppose we want two to the power four, times two to the power three. "
        "<bookmark mark='b0'/>We could expand both: four twos, and then three "
        "more twos. <bookmark mark='b1'/>That is seven twos multiplied "
        "together, which is two to the power seven. <bookmark mark='b2'/>"
        "Expanding everything every time is slow. There must be a shortcut."
    ),
    "s2": (
        "Let us watch the factors instead. <bookmark mark='b0'/>Two to the "
        "power four is four tiles, and two to the power three is three tiles. "
        "<bookmark mark='b1'/>Multiply, and the two groups join into one chain "
        "of seven. <bookmark mark='b2'/>So four plus three gives the new "
        "exponent, seven. <bookmark mark='b3'/>For any base: a to the power m "
        "times a to the power n is a to the power m plus n."
    ),
    "s3": (
        "Does the same rule work when an exponent is negative? <bookmark "
        "mark='b0'/>Look at three squared times three to the power minus four. "
        "<bookmark mark='b1'/>The base is the same, so add the exponents: two "
        "plus minus four. <bookmark mark='b2'/>That is minus two, so the "
        "answer is three to the power minus two. <bookmark mark='b3'/>And from "
        "the last lesson, that is one over three squared, or one ninth."
    ),
    "s4": (
        "Now division. <bookmark mark='b0'/>Take a to the power seven over a "
        "to the power three: seven factors on top, three below. <bookmark "
        "mark='b1'/>Every factor below can cancel one on top. Three pairs "
        "cancel, leaving four factors. <bookmark mark='b2'/>So the exponent is "
        "seven minus three, which is four. <bookmark mark='b3'/>In general, a "
        "to the power m over a to the power n is a to the power m minus n."
    ),
    "s5": (
        "Let us use the textbook's example: four to the power seven over four "
        "to the power four. <bookmark mark='b0'/>The bases are the same. "
        "<bookmark mark='b1'/>Subtract the exponents, top minus bottom: seven "
        "minus four. <bookmark mark='b2'/>That is three, so the answer is four "
        "cubed. <bookmark mark='b3'/>And four cubed is sixty four."
    ),
    "s6": (
        "What if the bottom exponent is bigger? <bookmark mark='b0'/>Look at "
        "five squared over five to the power five. <bookmark mark='b1'/>The "
        "base is the same, so subtract: two minus five. <bookmark mark='b2'/>"
        "That is minus three, so the answer is five to the power minus three. "
        "<bookmark mark='b3'/>A negative exponent is a perfectly good answer: "
        "it is one over five cubed, which is one over one hundred and twenty "
        "five."
    ),
    "s7": (
        "Now put the two laws side by side. <bookmark mark='b0'/>For a "
        "product, the factor groups join, so the exponents are added: a to the "
        "power m times a to the power n is a to the power m plus n. <bookmark "
        "mark='b1'/>For a quotient, matching factors cancel, so the exponents "
        "are subtracted: a to the power m over a to the power n is a to the "
        "power m minus n. <bookmark mark='b2'/>In both laws the base stays "
        "exactly the same."
    ),
    "s8": (
        "Here are three mistakes to avoid. <bookmark mark='b0'/>First: x to "
        "the power minus three times x to the power minus two is x to the "
        "power minus five, not minus six. <bookmark mark='b1'/>Second: two "
        "cubed times three to the fourth has different bases, so the exponents "
        "cannot be added. <bookmark mark='b2'/>Third: a squared over a to the "
        "power five is a to the power minus three, not a cubed. <bookmark "
        "mark='b3'/>Read the operation carefully."
    ),
    "s9q": (
        "Your turn. <bookmark mark='b0'/>Three questions. Simplify two to the power "
        "minus three times two to the power minus two. Simplify seven to the power "
        "minus two times seven to the power five. And simplify four to the power "
        "seven over four to the power four."
    ),
    "s9a": (
        "<bookmark mark='b0'/>For the first, the exponents add: minus three plus "
        "minus two is minus five, so two to the power minus five. <bookmark "
        "mark='b1'/>For the second, minus two plus five is three, so seven cubed. "
        "<bookmark mark='b2'/>And for the third, seven minus four is three, so four "
        "cubed, which is sixty four."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>When powers with the same base are "
        "multiplied, the factor groups join, so the exponents are added. <bookmark "
        "mark='b1'/>When they are divided, matching factors cancel, so the exponents "
        "are subtracted. <bookmark mark='b2'/>Keep the base, and remember: "
        "multiplication adds, division subtracts. <bookmark mark='b3'/>Thank you for "
        "watching, <bookmark mark='b4'/>and see you in the next lesson."
    ),
}


class ProductQuotientLawsStory(VoiceoverScene):
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
        out_dir = _HERE / "media" / "videos" / "laws_of_exponents_product_and_quotient"
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
    # Product & Quotient Laws of Exponents (Class 8, Chapter 4, Storymode 03).
    #
    # SYNC RULE for every reveal: wait for the narration bookmark that ends the
    # phrase describing a thing, and only then bring it on.  Playing first and
    # waiting afterwards shows the picture a whole window early, which reads as
    # broken sync.
    #
    # Layout rules, so the audits stay clean:
    #   * the heading sits on ROW_Y (2.72), the closing strip on STRIP_Y (-1.80);
    #     nothing at all sits below y = -2.00;
    #   * the FACTOR BLOCKS are the same mobjects throughout -- the two groups
    #     physically slide together for the product, and the matched tiles are
    #     slashed and removed for the quotient (no clear-and-redraw);
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

            heading = at(board_text("Product & Quotient Laws", 28, CHALK_WHITE,
                                    "BOLD"), BOARD_CX, 2.20)
            sub = at(board_text("Multiplying and Dividing Powers with the Same "
                                "Base", 17, CHALK_AMBER, "BOLD"),
                     BOARD_CX, 1.55)
            law1 = at(chalk_math(r"a^m \times a^n = a^{m+n}", size=38,
                                 color=CHALK_CYAN), BOARD_CX, 0.78)
            law2 = at(chalk_math(r"\frac{a^m}{a^n} = a^{m-n}", size=38,
                                 color=CHALK_YELLOW), BOARD_CX, -0.18)
            promise = at(board_text("Same base: the exponents do the "
                                    "arithmetic.", 16, CHALK_WHITE, "BOLD"),
                         BOARD_CX, -1.15)
            strip = at(board_text("Multiply  \u2192  add;   divide  \u2192  "
                                  "subtract.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(sub, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(law1, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(promise, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(law2, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, law1, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: expanding everything gets messy ----------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("There Must Be a Faster Way", 24,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            start = at(chalk_math(r"2^4 \times 2^3", size=44,
                                  color=CHALK_WHITE), BOARD_CX, 1.60)
            expand = at(chalk_math(r"2 \times 2 \times 2 \times 2 \times 2 "
                                   r"\times 2 \times 2", size=26,
                                   color=CHALK_WHITE), BOARD_CX, 0.60)
            joined = at(chalk_math("2^7", size=48, color=CHALK_YELLOW),
                        BOARD_CX, -0.40)
            banner = at(board_text("There must be a shortcut.", 20,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Expanding everything every time is slow.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(start, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(expand, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(ReplacementTransform(expand, joined), run_time=0.7)
            self.play(FadeIn(banner, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, joined, color=CHALK_YELLOW)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: why product exponents add (the factor blocks join) ---------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("Multiplication Joins Factors", 24,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            run_a, tiles_a = tile_run(4, "2", CHALK_CYAN)
            run_b, tiles_b = tile_run(3, "2", CHALK_PINK)
            cross = chalk_math(r"\times", size=30, color=CHALK_WHITE)
            row = at(VGroup(run_a, cross, run_b).arrange(RIGHT, buff=0.40),
                     BOARD_CX, 1.28)
            lab_a = at(board_text("4 factors", 15, CHALK_CYAN, "BOLD"),
                       run_a.get_center()[0], 1.86)
            lab_b = at(board_text("3 factors", 15, CHALK_PINK, "BOLD"),
                       run_b.get_center()[0], 1.86)
            plus = at(board_text("4 + 3 = 7", 19, CHALK_YELLOW, "BOLD"),
                      BOARD_CX, 1.86)
            power = at(chalk_math(r"2^{4+3} = 2^{7}", size=36,
                                  color=CHALK_GREEN), BOARD_CX, 0.28)
            law = at(card(chalk_math(r"a^m \times a^n = a^{m+n}", size=34,
                                     color=CHALK_GREEN), CHALK_GREEN),
                     BOARD_CX, -1.00)
            strip = at(board_text("KEEP THE BASE \u2014 ADD THE EXPONENTS.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(run_a, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(cross, scale=0.8), run_time=0.35)
            self.play(FadeIn(run_b, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(lab_a), FadeIn(lab_b), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            all_tiles = list(tiles_a) + list(tiles_b)
            targets = self.chain_positions(7, 1.28)
            self.play(*[t.animate.move_to(p)
                        for t, p in zip(all_tiles, targets)],
                      FadeOut(cross), FadeOut(lab_a), FadeOut(lab_b),
                      run_time=0.9)
            self.play(FadeIn(plus, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeOut(plus),
                      FadeIn(power, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(law, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, law, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: the product law with a negative exponent -------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Keep the Base, Add the Exponents", 23,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            start = at(chalk_math(r"3^2 \times 3^{-4}", size=44,
                                  color=CHALK_WHITE), BOARD_CX, 1.60)
            same = at(chip("the same base", CHALK_GREEN, size=15), 3.85, 1.60)
            add = at(chalk_math(r"2 + (-4) = -2", size=40, color=CHALK_YELLOW),
                     BOARD_CX, 0.75)
            result = at(card(chalk_math(r"3^2 \times 3^{-4} = 3^{-2}", size=38,
                                        color=CHALK_GREEN), CHALK_GREEN),
                        BOARD_CX, -0.10)
            back = at(chalk_math(r"3^{-2} = 1/3^2 = 1/9", size=30,
                                 color=CHALK_CYAN), BOARD_CX, -1.15)
            strip = at(board_text("The law holds for integer exponents.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(start, shift=UP * 0.08),
                      FadeIn(same, scale=0.8), run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(add, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(result, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(back, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, back, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: why quotient exponents subtract (the factors cancel) -------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("Division Cancels Matching Factors", 23,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            top, top_tiles = tile_run(7, "a", CHALK_WHITE)
            bot, bot_tiles = tile_run(3, "a", CHALK_WHITE)
            at(top, BOARD_CX, 1.55)
            at(bot, bot_tiles[1].get_center()[0], 0.62)
            bar = frac_bar(top.get_left()[0] - 0.10, top.get_right()[0] + 0.10,
                           1.08)
            marks = VGroup(*[cancel_mark(t)
                             for t in (top_tiles[0], top_tiles[1],
                                       top_tiles[2])],
                           *[cancel_mark(t) for t in bot_tiles])
            left_label = at(board_text("7 factors", 15, CHALK_CYAN, "BOLD"),
                            -2.95, 1.55)
            below_label = at(board_text("3 factors", 15, CHALK_PINK, "BOLD"),
                             -2.95, 0.62)
            minus = at(board_text("7 - 3 = 4", 19, CHALK_YELLOW, "BOLD"),
                       3.55, 0.20)
            law = at(card(chalk_math(r"\frac{a^m}{a^n} = a^{m-n}", size=34,
                                     color=CHALK_PINK), CHALK_PINK),
                     BOARD_CX, -0.90)
            strip = at(board_text("DIVISION CANCELS MATCHING FACTORS.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(top, shift=UP * 0.08), run_time=0.6)
            self.play(FadeIn(bar), FadeIn(bot, shift=DOWN * 0.08),
                      run_time=0.55)
            self.play(FadeIn(left_label), FadeIn(below_label), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            # the matched factors go label-first, so the slash crosses an empty
            # block rather than running through the glyph
            self.play(*[FadeOut(t.label) for t in
                        (top_tiles[0], top_tiles[1], top_tiles[2], *bot_tiles)],
                      LaggedStart(*[FadeIn(m, scale=0.7) for m in marks],
                                  lag_ratio=0.16), run_time=1.0)
            self.play(FadeOut(VGroup(*top_tiles[:3])),
                      FadeOut(VGroup(*bot_tiles)),
                      FadeOut(left_label), FadeOut(below_label),
                      run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            rest = self.chain_positions(4, 0.20)
            self.play(*[t.animate.move_to(p) for t, p in
                        zip(top_tiles[3:], rest)],
                      FadeOut(bar), FadeOut(marks), run_time=0.7)
            self.play(FadeIn(minus, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(law, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, law, color=CHALK_PINK)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: apply the quotient law -- 4^7 / 4^4 ------------------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("Top Exponent Minus Bottom Exponent", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            frac = at(chalk_math(r"\frac{4^7}{4^4}", size=48,
                                 color=CHALK_WHITE), BOARD_CX, 1.55)
            same = at(chip("the same base", CHALK_GREEN, size=15), 3.85, 1.55)
            sub_line = at(chalk_math(r"7 - 4 = 3", size=40,
                                     color=CHALK_YELLOW), BOARD_CX, 0.45)
            result = at(card(chalk_math(r"\frac{4^7}{4^4} = 4^{7-4} = 4^3",
                                        size=32, color=CHALK_PINK),
                             CHALK_PINK), BOARD_CX, -0.70)
            value = at(card(chalk_math("4^3 = 64", size=24,
                                         color=CHALK_CYAN), CHALK_CYAN),
                             4.30, -0.70)
            strip = at(board_text("Numerator exponent minus denominator "
                                  "exponent.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(frac, shift=UP * 0.08),
                      FadeIn(same, scale=0.8), run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(sub_line, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(result, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(value, scale=0.85), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, value, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: when the answer exponent is negative -----------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("A Negative Answer Is Fine", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            frac = at(chalk_math(r"\frac{5^2}{5^5}", size=48,
                                 color=CHALK_WHITE), BOARD_CX, 1.55)
            same = at(chip("the same base", CHALK_GREEN, size=15), 3.85, 1.55)
            sub_line = at(chalk_math(r"2 - 5 = -3", size=40,
                                     color=CHALK_YELLOW), BOARD_CX, 0.45)
            result = at(card(chalk_math(r"\frac{5^2}{5^5} = 5^{-3}", size=34,
                                        color=CHALK_PINK), CHALK_PINK),
                        BOARD_CX, -0.70)
            recip = at(card(chalk_math(r"= 1/5^3 = 1/125", size=22,
                                         color=CHALK_CYAN), CHALK_CYAN),
                             4.05, -0.70)
            strip = at(board_text("A negative exponent is a valid answer.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(frac, shift=UP * 0.08),
                      FadeIn(same, scale=0.8), run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(sub_line, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(result, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(recip, scale=0.85), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, recip, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: product against quotient -----------------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Same Base Is the Key", 22, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            product = at(zone_card(
                "PRODUCT",
                [chalk_math(r"a^m \times a^n", size=30, color=CHALK_WHITE),
                 chalk_math(r"= a^{m+n}", size=30, color=CHALK_WHITE)],
                CHALK_CYAN, width=4.2, height=2.80,
                note="JOIN  \u2192  ADD"), -2.35, 0.55)
            quotient = at(zone_card(
                "QUOTIENT",
                [chalk_math(r"\frac{a^m}{a^n}", size=30, color=CHALK_WHITE),
                 chalk_math(r"= a^{m-n}", size=30, color=CHALK_WHITE)],
                CHALK_PINK, width=4.2, height=2.80,
                note="CANCEL  \u2192  SUBTRACT"), 3.35, 0.55)
            key = at(board_text("SAME\nBASE", 18, CHALK_YELLOW, "BOLD"),
                     BOARD_CX, 0.55)
            strip = at(board_text("a is not zero, and the exponents are "
                                  "integers.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(product, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(quotient, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(key, scale=0.8), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, key, color=CHALK_YELLOW)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: three mistakes to avoid ------------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("Three Mistakes to Avoid", 22, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            row1 = at(card(VGroup(
                chalk_math(r"x^{-3} \times x^{-2} = x^{-6}", size=24,
                           color=CHALK_RED),
                mark_no(0.85),
                board_text("\u2192", 20, CHALK_WHITE, "BOLD"),
                chalk_math(r"x^{-5}", size=26, color=CHALK_GREEN)
            ).arrange(RIGHT, buff=0.38), CHALK_RED, pad_y=0.30),
                BOARD_CX, 1.62)
            row2 = at(card(VGroup(
                chalk_math(r"2^{3} \times 3^{4}", size=24, color=CHALK_WHITE),
                mark_no(0.85),
                chalk_math(r"2 \neq 3", size=24, color=CHALK_PINK),
                board_text("different bases", 15, CHALK_PINK, "BOLD")
            ).arrange(RIGHT, buff=0.38), CHALK_RED, pad_y=0.30),
                BOARD_CX, 0.66)
            row3 = at(card(VGroup(
                chalk_math(r"\frac{a^2}{a^5} = a^{5-2}", size=24,
                           color=CHALK_RED),
                mark_no(0.85),
                board_text("\u2192", 20, CHALK_WHITE, "BOLD"),
                chalk_math(r"a^{-3}", size=26, color=CHALK_GREEN)
            ).arrange(RIGHT, buff=0.38), CHALK_RED, pad_y=0.30),
                BOARD_CX, -0.45)
            banner = at(board_text("Read the operation carefully.", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Same base first; then add or subtract.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(row1, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(row2, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(row3, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(banner, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 9: your turn -- three questions, then the 10-second clock -----
    def beat_s9(self) -> None:
        with self.voiceover(text=NARRATION["s9q"]) as tracker:
            self.reset_board()

            heading = at(board_text("YOUR TURN", 26, CHALK_PINK, "BOLD"),
                         BOARD_CX, 2.78)
            sub = at(board_text("Product  \u00b7  Quotient  \u00b7  Same base",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, 2.24)

            qa = at(q_card("Simplify",
                           chalk_math(r"2^{-3} \times 2^{-2}", size=20,
                                      color=CHALK_WHITE)), -2.55, 1.50)
            qb = at(q_card("Simplify",
                           chalk_math(r"7^{-2} \times 7^{5}", size=20,
                                      color=CHALK_WHITE)), -2.55, 0.35)
            qc = at(q_card("Simplify",
                           chalk_math(r"\frac{4^7}{4^4}", size=18,
                                      color=CHALK_WHITE),
                           height=1.10, head_up=0.32, body_down=0.28),
                    -2.55, -0.90)

            ans_a = at(answer_row("A",
                                  chalk_math(r"2^{-3+(-2)} = 2^{-5}", 28,
                                             color=CHALK_GREEN),
                                  "add the exponents", CHALK_GREEN),
                       BOARD_CX, 1.30)
            ans_b = at(answer_row("B",
                                  chalk_math(r"7^{-2+5} = 7^{3}", 28,
                                             color=CHALK_YELLOW),
                                  "add the exponents", CHALK_YELLOW),
                       BOARD_CX, 0.45)
            ans_c = at(answer_row("C",
                                  chalk_math(r"4^{7-4} = 4^{3} = 64", 28,
                                             color=CHALK_PINK),
                                  "subtract the exponents", CHALK_PINK),
                       BOARD_CX, -0.40)
            done = at(board_text("KEEP THE BASE  \u2192  ADD OR SUBTRACT", 18,
                                 CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(sub, shift=UP * 0.08), run_time=0.4)

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
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, done)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap -----------------------------------------------------
    def beat_s10(self) -> None:
        with self.voiceover(text=NARRATION["s10"]) as tracker:
            self.reset_board()

            heading = at(board_text("Join or Cancel", 24, CHALK_AMBER, "BOLD"),
                         BOARD_CX, ROW_Y)
            product = at(card(VGroup(
                chalk_math(r"a^m \times a^n = a^{m+n}", size=34,
                           color=CHALK_CYAN),
                board_text("JOIN  \u2192  ADD", 16, CHALK_CYAN, "BOLD")
            ).arrange(DOWN, buff=0.26), CHALK_CYAN), BOARD_CX, 1.15)
            quotient = at(card(VGroup(
                chalk_math(r"\frac{a^m}{a^n} = a^{m-n}", size=34,
                           color=CHALK_PINK),
                board_text("CANCEL  \u2192  SUBTRACT", 16, CHALK_PINK, "BOLD")
            ).arrange(DOWN, buff=0.26), CHALK_PINK), BOARD_CX, -0.45)
            notzero = at(chalk_math(r"a \neq 0", size=22, color=CHALK_YELLOW),
                         4.45, -0.45)
            strip = at(board_text("Same non-zero base, integer exponents.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            thanks = at(board_text("Thank You for Watching!", 30, CHALK_WHITE,
                                   "BOLD"), BOARD_CX, 0.62)
            bye = at(board_text("See you in the next lesson :)", 22,
                                CHALK_YELLOW, "BOLD"), BOARD_CX, -0.32)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(product, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(quotient, shift=UP * 0.08),
                      FadeIn(notzero), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["success"], gain=-11)

            # the closing card is narrated: it appears as the voice says
            # "Thank you for watching,", the goodbye line as the voice says
            # "and see you in the next lesson."
            self.wait(leftover(tracker, "b3"))
            self.play(FadeOut(heading), FadeOut(product), FadeOut(quotient),
                      FadeOut(notzero), FadeOut(strip), run_time=0.5)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.5)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.closing(tracker, thanks, run_time=1.2)
            self._capture_srt(tracker)

        self.wait(END_HOLD)



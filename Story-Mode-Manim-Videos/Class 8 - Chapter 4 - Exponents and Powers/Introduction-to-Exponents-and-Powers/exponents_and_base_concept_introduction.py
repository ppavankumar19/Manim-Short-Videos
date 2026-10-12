"""
Introduction to Exponents & Powers: Understanding Base, Exponent, Power and
Exponential Notation
Story-mode chalkboard lesson (Telangana Class 8 Maths, Chapter 4:
Exponents and Powers, Storymode 01).

LLM KEY / FUNCTION NAME: exponents_and_base_concept_introduction

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

The defining visual is the POWER COMPRESSOR.  One repeated factor survives as
the base, the rest of the chain collapses, and the count of factors rides up
into the exponent position -- so the exponent is seen to come from counting, and
`4 x 4 x 4 x 4 x 4  ->  4^5` keeps the same 4 object throughout.

Title + 10 scenes:
  0. Title card.
  1. There must be a shorter way: the chain of six 3s, the counter, and the
     first compression into 3^6.
  2. What the exponent counts: six equal factors, braced and counted, = 3^6.
  3. Base, exponent and power: the vocabulary, with the spotlight moving from
     the base to the exponent, then the whole expression named a power.
  4. The power compressor: 4x4x4x4x4 -> 4^5 and back again.
  5. A very important difference: 4^5 = 1024 against 4 x 5 = 20.
  6. Powers of ten: 10^1, 10^2, 10^3 ... 10^9 and the zeros they add.
  7. Why exponents are useful: the Sun's 1,40,00,00,000 m as 1.4 x 10^9 m.
  8. When numbers grow fast: the chessboard grain doubling.
  9. Your turn: write 7x7x7x7, expand 2^5, name the base and exponent of 10^6,
     after the series' centred ten-second THINK clock.
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


from manim import Brace  # noqa: E402  (this section is spliced into a head
#                                         whose own imports omit Brace)

# Board layout shared by every scene of this video.
COLUMN_X = 3.05          # the series' right-hand note column
LEFT_X = -2.40           # left half of a two-column comparison
RIGHT_X = 3.40           # right half of a two-column comparison
ROW_Y = 2.72             # every scene heading sits on this line
SUB_Y = 2.20             # the one-line sub-heading under it
BANNER_Y = -1.15         # the closing banner, above the strip
# The burned-in caption grows up from the bottom of the frame: a one-line cue
# starts at y = -3.38 and a wrapped two-line cue reaches y = -2.93 (measured on
# the burned 360p cuts), so every closing strip sits at -1.80 and nothing at all
# sits below CAPTION_SAFE_Y = -2.00 -- audited by the IN-CAPTION-BAND check.
STRIP_Y = -1.80
CAPTION_SAFE_Y = -2.00

TILE_W = 0.60            # one factor tile
TILE_H = 0.72
PANEL_FILL = "#16202B"

# The factor chains and the three-question challenge are laid out from these,
# so every scene keeps the same rhythm.
CHAIN_BUFF = 0.18
CHAIN_Y = 1.02


# ---------------------------------------------------------------- furniture --
def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


def tile(label, color=CHALK_WHITE, size=26, w=TILE_W, h=TILE_H, fill=0.55):
    """One repeated factor as a chalk tile: a rounded box around its digit."""
    lab = chalk_math(label, size=size, color=color)
    box = RoundedRectangle(corner_radius=0.07, width=w, height=h,
                           stroke_color=color, stroke_width=1.9,
                           fill_color=PANEL_FILL, fill_opacity=fill)
    lab.move_to(box.get_center())
    grp = VGroup(box, lab)
    grp.label = lab
    return grp


def cross_sign(color=CHALK_WHITE, size=24):
    """The multiplication sign between two factor tiles."""
    return board_text("\u00d7", size, color, "BOLD")


def chain_of(n, label="3", color=CHALK_WHITE, size=26, buff=CHAIN_BUFF):
    """`n` factor tiles with multiplication signs between them."""
    parts = []
    for i in range(n):
        if i:
            parts.append(cross_sign(size=int(size * 0.85)))
        parts.append(tile(label, color, size=size))
    grp = VGroup(*parts).arrange(RIGHT, buff=buff)
    grp.tiles = [parts[i] for i in range(0, len(parts), 2)]
    grp.crosses = [parts[i] for i in range(1, len(parts), 2)]
    return grp


def count_badge(value, color=CHALK_CYAN, size=15, radius=0.18):
    """The counter that visits each factor in turn."""
    lab = board_text(str(value), size, color, "BOLD")
    ring = Circle(radius=radius, stroke_color=color, stroke_width=1.6,
                  fill_color=PANEL_FILL, fill_opacity=0.7)
    ring.move_to(lab.get_center())
    return VGroup(ring, lab)


def brace_note(group, text, color=CHALK_CYAN, size=15, buff=0.10):
    """A brace under `group` carrying a small label."""
    brace = Brace(group, DOWN, buff=buff, color=color)
    note = board_text(text, size, color, "BOLD")
    note.next_to(brace, DOWN, buff=0.08)
    return VGroup(brace, note)


def panel(title, lines, color=CHALK_WHITE, width=4.0, height=1.40,
          title_size=20, line_size=15):
    """A rounded card with a heading and one or two body lines.

    The offsets are measured so the heading, the body lines and the box edge all
    keep at least 0.24 units between their ink, which is the series' clearance
    standard."""
    head = board_text(title, title_size, color, "BOLD")
    body = VGroup(*[board_text(l, line_size, CHALK_WHITE, "BOLD")
                    for l in lines]).arrange(DOWN, buff=0.24)
    box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                           stroke_color=color, stroke_width=2.0,
                           fill_color=PANEL_FILL, fill_opacity=0.55)
    head.move_to(box.get_center() + UP * (height / 2 - 0.21))
    body.move_to(box.get_center() + DOWN * (0.30 if len(lines) > 1 else 0.22))
    return VGroup(box, head, body)


def machine(title, subtitle="", color=CHALK_CYAN, width=2.30, height=1.55,
            size=16):
    """The Power Compressor: the box the factors travel through."""
    head = board_text(title, size, color, "BOLD")
    box = RoundedRectangle(corner_radius=0.12, width=width, height=height,
                           stroke_color=color, stroke_width=2.4,
                           fill_color=PANEL_FILL, fill_opacity=0.7)
    head.move_to(box.get_center() + UP * (0.20 if subtitle else 0.0))
    grp = VGroup(box, head)
    if subtitle:
        sub = board_text(subtitle, size - 3, CHALK_YELLOW, "BOLD")
        sub.move_to(box.get_center() + DOWN * 0.28)
        grp.add(sub)
        grp.sub = sub
    return grp


def chip(text, color=CHALK_CYAN, size=15, width=None, height=0.52):
    """A small labelled chip."""
    lab = board_text(text, size, color, "BOLD")
    box = RoundedRectangle(corner_radius=0.09,
                           width=width or (lab.width + 0.42), height=height,
                           stroke_color=color, stroke_width=1.7,
                           fill_color=PANEL_FILL, fill_opacity=0.7)
    lab.move_to(box.get_center())
    return VGroup(box, lab)


def sun(radius=0.72, body=CHALK_AMBER, ray=CHALK_YELLOW):
    """The stylised Sun of the large-number scene (body plus eight rays)."""
    disc = Circle(radius=radius, stroke_color=ray, stroke_width=2.4,
                  fill_color=body, fill_opacity=0.9)
    rays = VGroup()
    for k in range(8):
        ang = k * np.pi / 4.0
        start = np.array([np.cos(ang), np.sin(ang), 0.0]) * (radius + 0.10)
        end = np.array([np.cos(ang), np.sin(ang), 0.0]) * (radius + 0.30)
        rays.add(Line(start, end, stroke_color=ray, stroke_width=3.0))
    return VGroup(rays, disc)


def chessboard(rows=2, cols=6, sq=0.62, light="#D9CDB4", dark="#5C6B57"):
    """A stretch of chessboard: alternating squares, top row first."""
    squares = VGroup()
    for r in range(rows):
        for c in range(cols):
            fill = light if (r + c) % 2 == 0 else dark
            squares.add(Square(side_length=sq, stroke_color=CHALK_WHITE,
                               stroke_width=1.2, fill_color=fill,
                               fill_opacity=0.85))
    grid = VGroup()
    for r in range(rows):
        row = VGroup(*squares[r * cols:(r + 1) * cols]).arrange(RIGHT, buff=0)
        grid.add(row)
    grid.arrange(DOWN, buff=0)
    grid.squares = squares
    return grid


def mark_yes(size=1.0, color=CHALK_GREEN):
    """A drawn chalk tick (the board font has no tick glyph)."""
    tick = VGroup(
        Line(ORIGIN, np.array([0.09, -0.11, 0.0])),
        Line(np.array([0.09, -0.11, 0.0]), np.array([0.28, 0.17, 0.0])),
    ).set_stroke(color=color, width=4.2)
    tick.scale(size)
    return tick


# ----------------------------------------------------------------


NARRATION = {
    "title": (
        "Exponents and powers. <bookmark mark='b0'/>A short way to write "
        "repeated multiplication: base, exponent and power. <bookmark "
        "mark='b1'/>Let us see why we need it."
    ),
    "s1": (
        "Start with a simple product: three times three times three. <bookmark "
        "mark='b0'/>Now keep going, up to six factors of three. <bookmark "
        "mark='b1'/>Every single three has to be written out. <bookmark "
        "mark='b2'/>Do we really need to write three six times? There must be "
        "a shorter way."
    ),
    "s2": (
        "Let us count them. <bookmark mark='b0'/>Three times three times "
        "three times three times three times three: six equal factors. "
        "<bookmark mark='b1'/>That small raised number tells us how many times "
        "the base is used as a factor. <bookmark mark='b2'/>So three to the "
        "power six means six threes multiplied together."
    ),
    "s3": (
        "Look closely at three to the power six. <bookmark mark='b0'/>The "
        "large number at the bottom is the base: three, the number that is "
        "multiplied again and again. <bookmark mark='b1'/>The small raised "
        "number is the exponent: six, the number of factors. <bookmark "
        "mark='b2'/>The whole expression is called a power. We read it as "
        "three raised to the power six."
    ),
    "s4": (
        "Now send five factors of four through the power compressor. <bookmark "
        "mark='b0'/>In they go: four times four times four times four times "
        "four. <bookmark mark='b1'/>The machine counts five factors and writes "
        "four to the power five. <bookmark mark='b2'/>Send it back the other "
        "way, and four to the power five expands into five fours multiplied."
    ),
    "s5": (
        "Here is a mistake to avoid. <bookmark mark='b0'/>Four to the power "
        "five is not four times five. <bookmark mark='b1'/>Four to the power "
        "five means five fours multiplied, which is one thousand and twenty "
        "four. <bookmark mark='b2'/>Four times five is only twenty. The "
        "exponent counts factors, not how many times to multiply."
    ),
    "s6": (
        "Powers of ten are the most useful of all. <bookmark mark='b0'/>Ten to "
        "the power one is ten, and ten squared is ten times ten: one hundred. "
        "<bookmark mark='b1'/>Ten cubed is one thousand. Every new factor of "
        "ten adds another zero. <bookmark mark='b2'/>Ten to the power nine is "
        "a one followed by nine zeros: one thousand million."
    ),
    "s7": (
        "Now the reason we need all this. <bookmark mark='b0'/>The Sun is "
        "about fourteen crore metres across: a one and a four, followed by "
        "eight zeros. <bookmark mark='b1'/>In exponential form that is one "
        "point four times ten to the power nine. <bookmark mark='b2'/>The same "
        "short line writes the distance to the Sun, or the age of the universe."
    ),
    "s8": (
        "Numbers can also grow very fast. <bookmark mark='b0'/>One grain on "
        "the first square of a chessboard, two on the next, four on the next, "
        "then eight, sixteen, thirty two. <bookmark mark='b1'/>Every square "
        "doubles the one before it. <bookmark mark='b2'/>By the last square "
        "the number is enormous, and only exponents can write it comfortably."
    ),
    "s9q": (
        "Your turn. <bookmark mark='b0'/>Three questions. Write seven times seven "
        "times seven times seven in exponential form. Expand two to the power five. "
        "Name the base and the exponent in ten to the power six."
    ),
    "s9a": (
        "<bookmark mark='b0'/>Seven is repeated four times, so that is seven to the "
        "power four. <bookmark mark='b1'/>Two to the power five is five twos "
        "multiplied together. <bookmark mark='b2'/>And in ten to the power six, ten "
        "is the base and six is the exponent."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>The base is the number that repeats. The "
        "exponent counts how many times it is used as a factor. <bookmark "
        "mark='b1'/>The power is the compact expression that writes it in one place. "
        "<bookmark mark='b2'/>Remember: exponents make repeated multiplication short. "
        "<bookmark mark='b3'/>Thank you for watching, <bookmark mark='b4'/>and see you "
        "in the next lesson."
    ),
}


class ExponentsAndBaseConceptStory(VoiceoverScene):
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
        out_dir = _HERE / "media" / "videos" / "exponents_and_base_concept_introduction"
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
    # Introduction to Exponents & Powers (Class 8, Chapter 4, Storymode 01).
    #
    # SYNC RULE for every reveal: wait for the narration bookmark that ends the
    # phrase describing a thing, and only then bring it on.  Playing first and
    # waiting afterwards shows the picture a whole window early, which reads as
    # broken sync.
    #
    # Layout rules, so the audits stay clean:
    #   * the heading sits on the board's own heading line (2.72), the closing
    #     strip on STRIP_Y (-1.80); nothing at all sits below CAPTION_SAFE_Y;
    #   * two-column work is centred on the board's left and right halves;
    #   * nothing is placed on a line, and no card, tile or chip is placed over
    #     another element -- checked by audit_clearance.py and
    #     audit_sync_overlap.py;
    #   * the challenge uses the series' shared 10-second THINK clock, dead
    #     centre of the board, and the three question cards sit on the LEFT
    #     while it runs so the badge never covers them.
    ROW_Y = 2.72
    BANNER_Y = -1.15
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

    def rule_row(self, label, detail, color=CHALK_WHITE, width=8.8,
                 height=0.66, size=18):
        """One recap row: a coloured label badge, then what it means."""
        badge = board_text(label, size, color, "BOLD")
        body = board_text(detail, size - 3, CHALK_WHITE, "BOLD")
        row = VGroup(badge, body).arrange(RIGHT, buff=0.34)
        box = RoundedRectangle(corner_radius=0.09, width=width, height=height,
                               stroke_color=color, stroke_width=1.7,
                               fill_color=PANEL_FILL, fill_opacity=0.7)
        row.move_to(box.get_center())
        return VGroup(box, row)

    def q_card(self, title, body, color=CHALK_CYAN, width=3.7, height=0.92):
        """One 'your turn' question card: the prompt over the expression."""
        head = board_text(title, 14, color, "BOLD")
        box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                               stroke_color=color, stroke_width=1.9,
                               fill_color=PANEL_FILL, fill_opacity=0.55)
        head.move_to(box.get_center() + UP * 0.24)
        body.move_to(box.get_center() + DOWN * 0.22)
        return VGroup(box, head, body)

    def answer_row(self, tag, maths, note, color, width=7.6, height=0.70):
        """One revealed answer: its letter, the expression and a short note."""
        lab = board_text(tag, 17, color, "BOLD")
        txt = board_text(note, 16, CHALK_WHITE, "BOLD")
        row = VGroup(lab, maths, txt).arrange(RIGHT, buff=0.40)
        box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                               stroke_color=color, stroke_width=1.8,
                               fill_color=PANEL_FILL, fill_opacity=0.6)
        row.move_to(box.get_center())
        return VGroup(box, row)

    # -- Scene 0: title ------------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            heading = at(board_text("Introduction to Exponents & Powers", 26,
                                    CHALK_WHITE, "BOLD"), BOARD_CX, 2.05)
            sub = at(board_text("Base  \u00b7  Exponent  \u00b7  Power", 20,
                                CHALK_AMBER, "BOLD"), BOARD_CX, 1.40)
            show = at(chalk_math(r"3^6 = 3 \times 3 \times 3 \times 3 "
                                 r"\times 3 \times 3", size=30,
                                 color=CHALK_CYAN), BOARD_CX, 0.52)
            promise = at(board_text("A short way to write repeated "
                                    "multiplication.", 16, CHALK_WHITE, "BOLD"),
                         BOARD_CX, BANNER_Y)
            strip = at(board_text("Exponent notation saves space.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(sub, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(show, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(promise, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, show, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: there must be a shorter way --------------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("There Must Be a Shorter Way", 24,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            chain = at(chain_of(6, "3", CHALK_WHITE, size=26), BOARD_CX, 1.02)
            counts = VGroup(*[
                at(count_badge(i + 1), chain.tiles[i].get_center()[0],
                   chain.tiles[i].get_center()[1] + 0.78)
                for i in range(6)])
            note = at(board_text("Six factors of three, every one written out.",
                                 17, CHALK_WHITE, "BOLD"), BOARD_CX, -0.22)
            question = at(board_text("Do we really need to write three six "
                                     "times?", 19, CHALK_PINK, "BOLD"),
                          BOARD_CX, -0.22)
            result = at(board_text("There must be a shorter way.", 20,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, -1.10)
            strip = at(board_text("Repeated multiplication is long to write.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.06)
                                    for t in chain.tiles], lag_ratio=0.16),
                      run_time=1.0)
            self.play(LaggedStart(*[FadeIn(c, scale=0.7)
                                    for c in chain.crosses], lag_ratio=0.14),
                      run_time=0.6)
            self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in counts],
                                  lag_ratio=0.14), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(note, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b2"))
            self.play(ReplacementTransform(note, question), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            # the compression: ONE three stays behind as the base, the other
            # five leave, and the count rides up into the exponent position
            base = chain.tiles[0]
            self.play(FadeOut(*chain.crosses), FadeOut(*chain.tiles[1:]),
                      FadeOut(counts),
                      base.animate.move_to(np.array([BOARD_CX - 0.24, 1.02,
                                                     0.0])),
                      run_time=0.75)
            sup = board_text("6", 30, CHALK_YELLOW, "BOLD")
            sup.move_to(base.get_corner(UR) + np.array([0.16, 0.05, 0.0]))
            self.play(FadeIn(sup, scale=0.6), FadeIn(result, shift=UP * 0.08),
                      run_time=0.6)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, sup, color=CHALK_YELLOW)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: what the exponent really counts ----------------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("What Does the Exponent Count?", 23,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            chain = at(chain_of(6, "3", CHALK_WHITE, size=24, buff=0.16),
                       BOARD_CX, 1.38)
            counts = VGroup(*[
                at(count_badge(i + 1), chain.tiles[i].get_center()[0],
                   chain.tiles[i].get_center()[1] + 0.72)
                for i in range(6)])
            brace = brace_note(chain, "6 factors", CHALK_CYAN, size=15)
            power = at(chalk_math("3^6", size=54, color=CHALK_WHITE),
                       BOARD_CX, -0.32)
            banner = at(board_text("EXPONENT = NUMBER OF TIMES THE BASE IS "
                                   "USED AS A FACTOR", 16, CHALK_YELLOW,
                                   "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The exponent counts equal factors.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.06)
                                    for t in chain.tiles], lag_ratio=0.14),
                      run_time=0.9)
            self.play(LaggedStart(*[FadeIn(c, scale=0.7)
                                    for c in chain.crosses], lag_ratio=0.12),
                      run_time=0.55)
            # the counter visits the six factors in step with the voice naming
            # them ("three times three times three ... six equal factors"), so
            # it spreads across whatever is left of that phrase's window
            visit_rt = max(tracker.time_until_bookmark("b1") - 0.10, 0.60)
            self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in counts],
                                  lag_ratio=0.16), run_time=min(visit_rt, 3.20))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(brace, shift=DOWN * 0.06), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(power, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(banner, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, power, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: base, exponent and power -----------------------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Base, Exponent and Power", 24,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            big = at(chalk_math("3^6", size=64, color=CHALK_WHITE),
                     BOARD_CX, 1.15)
            base_card = panel("BASE", ["the number that is repeated",
                                       "here it is the 3"],
                              CHALK_CYAN, width=4.1, height=1.40)
            exp_card = panel("EXPONENT", ["how many times it is used",
                                          "here it is the 6"],
                             CHALK_PINK, width=4.1, height=1.40)
            at(base_card, -2.25, -0.15)
            at(exp_card, 3.25, -0.15)
            cards = VGroup(base_card, exp_card)

            p_label = board_text("POWER", 17, CHALK_GREEN, "BOLD")
            p_body = board_text("the whole expression, read as three raised "
                                "to the power six", 15, CHALK_WHITE, "BOLD")
            p_row = VGroup(p_label, p_body).arrange(RIGHT, buff=0.30)
            p_box = RoundedRectangle(corner_radius=0.09,
                                     width=p_row.width + 0.60, height=0.56,
                                     stroke_color=CHALK_GREEN, stroke_width=1.8,
                                     fill_color=PANEL_FILL, fill_opacity=0.7)
            p_row.move_to(p_box.get_center())
            power_card = at(VGroup(p_box, p_row), BOARD_CX, -1.30)
            ring = SurroundingRectangle(base_card, color=CHALK_CYAN, buff=0.05,
                                        corner_radius=0.12, stroke_width=3.0)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(big, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(cards, shift=UP * 0.08), FadeIn(ring),
                      run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(Transform(ring, SurroundingRectangle(
                exp_card, color=CHALK_PINK, buff=0.05, corner_radius=0.12,
                stroke_width=3.0)), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(power_card, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, power_card, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: the power compressor ---------------------------------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Power Compressor", 24, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            comp = at(machine("POWER", "COMPRESSOR", CHALK_CYAN), BOARD_CX,
                      0.95)
            factors = at(chalk_math(r"4 \times 4 \times 4 \times 4 \times 4",
                                    size=26, color=CHALK_WHITE), -2.95, 0.95)
            out = at(chalk_math("4^5", size=48, color=CHALK_YELLOW), 3.55, 0.95)
            arrow_in = Arrow(factors.get_right() + RIGHT * 0.16,
                             comp.get_left() + LEFT * 0.10, buff=0,
                             stroke_width=3.0, color=CHALK_CYAN,
                             max_tip_length_to_length_ratio=0.16)
            arrow_out = Arrow(comp.get_right() + RIGHT * 0.10,
                              out.get_left() + LEFT * 0.16, buff=0,
                              stroke_width=3.0, color=CHALK_YELLOW,
                              max_tip_length_to_length_ratio=0.16)
            count_note = at(board_text("it counts five factors", 15,
                                       CHALK_YELLOW, "BOLD"), BOARD_CX, -0.16)
            expanded = at(chalk_math(r"4 \times 4 \times 4 \times 4 \times 4",
                                     size=22, color=CHALK_YELLOW), 3.55, 0.95)
            banner = at(board_text("COMPRESS  \u2194  EXPAND", 22,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, -0.82)
            strip = at(board_text("Five fours multiplied, or four to the "
                                  "power five.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(comp, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(factors, shift=RIGHT * 0.10),
                      GrowArrow(arrow_in), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(count_note, scale=0.8), GrowArrow(arrow_out),
                      FadeIn(out, shift=LEFT * 0.10), run_time=0.6)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(Transform(out, expanded), FadeOut(arrow_out),
                      FadeOut(count_note), run_time=0.7)
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(banner, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, banner)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: a very important difference --------------------------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("A Very Important Difference", 24,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            l_box = RoundedRectangle(corner_radius=0.10, width=4.3, height=1.9,
                                     stroke_color=CHALK_CYAN, stroke_width=2.0,
                                     fill_color=PANEL_FILL, fill_opacity=0.55)
            l_head = chalk_math("4^5", size=42, color=CHALK_CYAN)
            l_body = chalk_math(r"4 \times 4 \times 4 \times 4 \times 4 = 1024",
                                size=22, color=CHALK_WHITE)
            l_head.move_to(l_box.get_center() + UP * 0.52)
            l_body.move_to(l_box.get_center() + DOWN * 0.36)
            left_card = at(VGroup(l_box, l_head, l_body), -2.15, 0.42)

            r_box = RoundedRectangle(corner_radius=0.10, width=2.9, height=1.9,
                                     stroke_color=CHALK_RED, stroke_width=2.0,
                                     fill_color=PANEL_FILL, fill_opacity=0.55)
            r_head = chalk_math(r"4 \times 5", size=42, color=CHALK_RED)
            r_body = chalk_math("= 20", size=26, color=CHALK_WHITE)
            r_head.move_to(r_box.get_center() + UP * 0.52)
            r_body.move_to(r_box.get_center() + DOWN * 0.36)
            right_card = at(VGroup(r_box, r_head, r_body), 3.45, 0.42)

            neq = at(chalk_math(r"\neq", size=64, color=CHALK_PINK), 1.00, 0.42)
            banner = at(board_text("THE EXPONENT COUNTS FACTORS", 19,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Not the number to multiply by.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(left_card, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(right_card, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(neq, scale=0.7), run_time=0.45)
            self.play(FadeIn(banner, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, neq, color=CHALK_PINK)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: powers of ten ----------------------------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("Powers of Ten", 24, CHALK_AMBER, "BOLD"),
                         BOARD_CX, ROW_Y)
            r1 = at(chalk_math(r"10^1 = 10", size=30, color=CHALK_WHITE),
                    BOARD_CX, 1.62)
            r2 = at(chalk_math(r"10^2 = 10 \times 10 = 100", size=30,
                               color=CHALK_WHITE), BOARD_CX, 1.02)
            r3 = at(chalk_math(r"10^3 = 10 \times 10 \times 10 = 1000", size=30,
                               color=CHALK_WHITE), BOARD_CX, 0.42)
            more = at(chip("+ one more zero", CHALK_CYAN, size=15), 4.20, 0.42)
            r9 = at(chalk_math(r"10^9 = 1000000000", size=34,
                               color=CHALK_YELLOW), BOARD_CX, -0.42)
            note = at(board_text("nine zeros after the one", 16, CHALK_CYAN,
                                 "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Powers of ten write large place values "
                                  "compactly.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(r1, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(r2, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(r3, shift=UP * 0.08), FadeIn(more, scale=0.8),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(r9, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(note, shift=UP * 0.08), run_time=0.4)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, r9, color=CHALK_YELLOW)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: why exponents are useful for large numbers -----------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Why Exponents Are Useful", 24, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sun_grp = at(sun(0.60), -2.95, 1.45)
            sun_lab = at(board_text("the Sun", 17, CHALK_AMBER, "BOLD"),
                         -2.95, 0.36)
            l_box = RoundedRectangle(corner_radius=0.10, width=5.0, height=1.25,
                                     stroke_color=CHALK_RED, stroke_width=2.0,
                                     fill_color=PANEL_FILL, fill_opacity=0.55)
            l_num = board_text("1,40,00,00,000 m", 26, CHALK_WHITE, "BOLD")
            l_note = board_text("long to read, long to write", 15, CHALK_RED,
                                "BOLD")
            l_num.move_to(l_box.get_center() + UP * 0.22)
            l_note.move_to(l_box.get_center() + DOWN * 0.30)
            long_card = at(VGroup(l_box, l_num, l_note), 2.35, 1.45)

            down_arrow = Arrow(np.array([2.35, 0.72, 0.0]),
                               np.array([2.35, 0.20, 0.0]), buff=0,
                               stroke_width=3.0, color=CHALK_GREEN,
                               max_tip_length_to_length_ratio=0.35)
            c_math = chalk_math(r"1.4 \times 10^9", size=44, color=CHALK_GREEN)
            c_unit = board_text("metres", 20, CHALK_WHITE, "BOLD")
            c_row = VGroup(c_math, c_unit).arrange(RIGHT, buff=0.30)
            c_box = RoundedRectangle(corner_radius=0.10,
                                     width=c_row.width + 0.70, height=0.86,
                                     stroke_color=CHALK_GREEN, stroke_width=2.2,
                                     fill_color=PANEL_FILL, fill_opacity=0.6)
            c_row.move_to(c_box.get_center())
            compact = at(VGroup(c_box, c_row), BOARD_CX, -0.42)
            reading = at(board_text("10 raised to the power 9", 16, CHALK_CYAN,
                                    "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The same idea writes the distance to the Sun, "
                                  "or the age of the universe.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(sun_grp, scale=0.85), run_time=0.5)
            self.play(FadeIn(sun_lab, shift=UP * 0.06), run_time=0.35)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(long_card, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(GrowArrow(down_arrow), FadeIn(compact, shift=UP * 0.08),
                      run_time=0.65)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(reading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, compact, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: when numbers grow fast (the chessboard) --------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("When Numbers Grow Fast", 24, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            grid = at(chessboard(2, 6, sq=0.66), BOARD_CX, 1.30)
            grains = VGroup(*[
                at(board_text(g, 13, CHALK_WHITE, "BOLD"),
                   grid.squares[i].get_center()[0], 1.63)
                for i, g in enumerate(("1", "2", "4", "8", "16", "32"))])
            note = at(board_text("every square doubles the one before it", 17,
                                 CHALK_CYAN, "BOLD"), BOARD_CX, 0.28)
            banner = at(board_text("Exponents write that growth compactly.", 19,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, -0.65)
            strip = at(board_text("Doubling again and again grows enormous "
                                  "numbers.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(grid, shift=UP * 0.08), run_time=0.6)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(g, scale=0.7) for g in grains],
                                  lag_ratio=0.22), run_time=1.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(note, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            # the board shrinks away, the way the 64 squares hide the total
            centre = grid.get_center()
            self.play(*[m.animate.scale(0.60, about_point=centre)
                        for m in (grid, *grains)], run_time=0.8)
            self.play(FadeIn(banner, shift=UP * 0.08), run_time=0.5)
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
            sub = at(board_text("Choose the rule before you calculate.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, 2.24)

            qa = at(self.q_card("Write in exponential form",
                                chalk_math(r"7 \times 7 \times 7 \times 7",
                                           size=20, color=CHALK_WHITE)),
                    -2.55, 1.45)
            qb = at(self.q_card("Expand it",
                                chalk_math("2^5", size=22, color=CHALK_WHITE)),
                    -2.55, 0.31)
            qc = at(self.q_card("Name the base and the exponent",
                                chalk_math("10^6", size=22, color=CHALK_WHITE)),
                    -2.55, -0.83)

            ans_a = at(self.answer_row("A",
                                       chalk_math("7^4", size=30,
                                                  color=CHALK_GREEN),
                                       "four factors of seven", CHALK_GREEN),
                       BOARD_CX, 1.30)
            ans_b = at(self.answer_row("B",
                                       chalk_math(r"2 \times 2 \times 2 \times "
                                                  r"2 \times 2", size=24,
                                                  color=CHALK_YELLOW),
                                       "five twos multiplied", CHALK_YELLOW),
                       BOARD_CX, 0.45)
            ans_c = at(self.answer_row("C",
                                       chalk_math("10^6", size=26,
                                                  color=CHALK_PINK),
                                       "base 10, exponent 6", CHALK_PINK),
                       BOARD_CX, -0.40)
            done = at(board_text("Write  \u2192  Expand  \u2192  Identify", 18,
                                 CHALK_YELLOW, "BOLD"), BOARD_CX, -1.30)

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

            heading = at(board_text("Base  \u00b7  Exponent  \u00b7  Power", 24,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            rows = VGroup(
                self.rule_row("BASE", "the number that is repeated  "
                              "(3 in three to the power six)", CHALK_CYAN),
                self.rule_row("EXPONENT", "how many times it is used  "
                              "(6 in three to the power six)", CHALK_PINK),
                self.rule_row("POWER", "the compact expression for it all",
                              CHALK_GREEN),
            )
            at(rows[0], BOARD_CX, 1.55)
            at(rows[1], BOARD_CX, 0.70)
            at(rows[2], BOARD_CX, -0.15)
            final = at(board_text("Exponents make repeated multiplication "
                                  "short.", 20, CHALK_YELLOW, "BOLD"),
                       BOARD_CX, BANNER_Y)
            strip = at(board_text("BASE and REPEAT COUNT give the POWER "
                                  "NOTATION.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            thanks = at(board_text("Thank You for Watching!", 30, CHALK_WHITE,
                                   "BOLD"), BOARD_CX, 0.62)
            bye = at(board_text("See you in the next lesson :)", 22,
                                CHALK_YELLOW, "BOLD"), BOARD_CX, -0.32)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(rows[0], shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(rows[1], shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(rows[2], shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(final, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["success"], gain=-11)

            # the closing card is narrated: it appears as the voice says
            # "Thank you for watching,", and the goodbye line as the voice
            # says "and see you in the next lesson."
            self.wait(leftover(tracker, "b3"))
            self.play(FadeOut(heading), FadeOut(rows[0]), FadeOut(rows[1]),
                      FadeOut(rows[2]), FadeOut(final), FadeOut(strip),
                      run_time=0.5)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.5)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.closing(tracker, thanks, run_time=1.2)
            self._capture_srt(tracker)

        self.wait(END_HOLD)




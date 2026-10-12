"""
Mastering Basic Divisibility Rules: Quick Tests for 2, 3, 5, 6, 9 and 10
Story-mode chalkboard lesson (Telangana Class 6 Maths, Chapter 3:
Playing with Numbers, Storymode 01).

LLM KEY / FUNCTION NAME: divisibility_rules_basic_2_3_5_6_9_10

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

The defining visual is the Divisibility Scanner: six rules collapse into three
ways of looking at a number --

  * 2, 5, 10  ->  inspect the ones digit only,
  * 3, 9      ->  add all the digits and test that sum,
  * 6         ->  pass the test for 2 AND the test for 3.

Title + 10 scenes:
  0. Title card.
  1. Hasini's 125 chocolates: guessing by dividing is slow.
  2. What "divisible" means: remainder 0 (24 / 4) versus remainder 1 (29 / 4).
  3. Divisibility by 2: the ones digit 0, 2, 4, 6, 8.
  4. Divisibility by 5 and 10, and the last-digit family.
  5. Divisibility by 3: 27 versus 37, then the digit sum of 36129.
  6. Divisibility by 9: the same digit sum, a stronger test (9846).
  7. Divisibility by 6: the test for 2 and the test for 3 together (7224).
  8. One dashboard: last digit / digit sum / combine both.
  9. Your turn: which of 2, 3, 5, 6, 9, 10 divide 12345 exactly?
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
COLUMN_X = 3.05          # the series' right-hand note column
LEFT_X = -2.40           # left half of a two-column comparison
RIGHT_X = 3.40           # right half of a two-column comparison
ROW_Y = 2.72             # every scene heading sits on this line
# The burned-in captions grow upward from the bottom of the frame: a one-line
# cue starts at y = -3.33 and a two-line cue reaches y = -2.33.  Every closing
# strip therefore sits at -1.95, with nothing below -2.15 (audited by the
# IN-CAPTION-BAND check).
STRIP_Y = -1.95

TILE_W = 0.40            # one digit tile
TILE_H = 0.54
PANEL_FILL = "#16202B"


# ---------------------------------------------------------------- furniture --
def number_card(value, color=CHALK_WHITE, size=26, stroke=CHALK_AMBER):
    """A number on its own small chalk card."""
    tex = chalk_math(str(value), size=size, color=color)
    box = RoundedRectangle(corner_radius=0.08, width=tex.width + 0.44,
                           height=tex.height + 0.30, stroke_color=stroke,
                           stroke_width=1.8, fill_color=PANEL_FILL,
                           fill_opacity=0.8)
    tex.move_to(box.get_center())
    grp = VGroup(box, tex)
    grp.tex = tex
    return grp


def badge_card(label, color=CHALK_WHITE, size=26, width=None, height=0.62,
               text_size=None):
    """A single number or symbol in a rounded badge (a divisor chip)."""
    tex = board_text(label, text_size or int(size * 0.72), color, "BOLD")
    box = RoundedRectangle(corner_radius=0.10,
                           width=width or max(tex.width + 0.44, height),
                           height=height, stroke_color=color, stroke_width=2.0,
                           fill_color=PANEL_FILL, fill_opacity=0.75)
    tex.move_to(box.get_center())
    grp = VGroup(box, tex)
    grp.tex = tex
    return grp


def digit_tiles(number, size=26, color=CHALK_WHITE, buff=0.10):
    """Each digit of `number` as its own tile: returns (group, [tiles])."""
    tiles = []
    for ch in str(number):
        lab = chalk_math(ch, size=size, color=color)
        box = RoundedRectangle(corner_radius=0.06, width=TILE_W, height=TILE_H,
                               stroke_color=CHALK_WHITE, stroke_width=1.5,
                               fill_color=PANEL_FILL, fill_opacity=0.5)
        lab.move_to(box.get_center())
        tiles.append(VGroup(box, lab))
    grp = VGroup(*tiles).arrange(RIGHT, buff=buff)
    for i, tile in enumerate(grp):
        tile.index = i
    return grp, list(grp)


def tile_ring(tile, color=CHALK_YELLOW, buff=0.07):
    """The magnifying ring that picks one digit out of a number."""
    return RoundedRectangle(corner_radius=0.08, width=TILE_W + 2 * buff + 0.08,
                            height=TILE_H + 2 * buff + 0.08, stroke_color=color,
                            stroke_width=3.0).move_to(tile.get_center())


def mark_yes(size=1.0, color=CHALK_GREEN):
    """A chalk tick (the same stroke used by check_row)."""
    tick = VGroup(
        Line(ORIGIN, np.array([0.09, -0.11, 0.0])),
        Line(np.array([0.09, -0.11, 0.0]), np.array([0.28, 0.17, 0.0])),
    ).set_stroke(color=color, width=4.2)
    tick.scale(size)
    return tick


def mark_no(size=1.0, color=CHALK_RED):
    """A chalk cross."""
    cross = VGroup(
        Line(np.array([-0.10, -0.10, 0.0]), np.array([0.10, 0.10, 0.0])),
        Line(np.array([-0.10, 0.10, 0.0]), np.array([0.10, -0.10, 0.0])),
    ).set_stroke(color=color, width=4.2)
    cross.scale(size)
    return cross


def verdict(ok, text, color=None, size=15, buff=0.20):
    """A tick or a cross beside the reason it is there."""
    m = mark_yes(size=0.95) if ok else mark_no(size=0.95)
    t = board_text(text, size, color or (CHALK_GREEN if ok else CHALK_PINK),
                   "BOLD")
    return VGroup(m, t).arrange(RIGHT, buff=buff)


def chocolate_groups(n_groups, per_group=4, cols=3, r=0.05, buff=0.05,
                     pad=0.10, color=CHALK_YELLOW):
    """`n_groups` little share-boxes, each holding `per_group` chocolates."""
    boxes = []
    for _ in range(n_groups):
        dots = VGroup(*[Dot(radius=r, color=color) for _ in range(per_group)])
        dots.arrange_in_grid(rows=2, cols=2, buff=buff)
        box = RoundedRectangle(corner_radius=0.05, width=dots.width + 2 * pad,
                               height=dots.height + 2 * pad,
                               stroke_color=CHALK_WHITE, stroke_width=1.3,
                               stroke_opacity=0.75)
        dots.move_to(box.get_center())
        boxes.append(VGroup(box, dots))
    rows = (n_groups + cols - 1) // cols
    return VGroup(*boxes).arrange_in_grid(rows=rows, cols=cols, buff=0.16)


def rule_line(label, detail, color=CHALK_WHITE, width=None, size=17):
    """One divisibility rule as a card: the divisor badge and its test."""
    badge = board_text(label, size, color, "BOLD")
    body = board_text(detail, size - 2, CHALK_WHITE, "BOLD")
    box = RoundedRectangle(corner_radius=0.09,
                           width=width or max(badge.width + body.width + 0.90,
                                              2.4),
                           height=0.60, stroke_color=color, stroke_width=1.7,
                           fill_color=PANEL_FILL, fill_opacity=0.7)
    badge.move_to(box.get_center() + LEFT * (box.width / 2 - badge.width / 2
                                             - 0.16))
    body.next_to(badge, RIGHT, buff=0.24)
    grp = VGroup(box, badge, body)
    grp.badge, grp.body = badge, body
    return grp


def zone_panel(title, lines, color=CHALK_WHITE, width=3.0, height=2.35,
               size=16, line_size=14):
    """One of the three 'families of rules' panels of the dashboard scene."""
    head = board_text(title, size, color, "BOLD")
    body = VGroup(*[board_text(l, line_size, CHALK_WHITE, "BOLD")
                    for l in lines]).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                           stroke_color=color, stroke_width=2.0,
                           fill_color=PANEL_FILL, fill_opacity=0.55)
    head.move_to(box.get_center() + UP * (height / 2 - 0.34))
    body.move_to(box.get_center() + DOWN * 0.22)
    return VGroup(box, head, body)


def column_card(mob, y, x=COLUMN_X):
    return mob.move_to(np.array([x, y, 0]))


def column_note(text, y, x=COLUMN_X, size=15, color=CHALK_WHITE):
    return board_text(text, size, color, "BOLD").move_to(np.array([x, y, 0]))


def gate(label, detail, color=CHALK_WHITE, width=2.7, height=1.05):
    """A scanner gate: the test it runs, over the evidence for it."""
    head = board_text(label, 17, color, "BOLD")
    body = board_text(detail, 14, CHALK_WHITE, "BOLD")
    box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                           stroke_color=color, stroke_width=2.0,
                           fill_color=PANEL_FILL, fill_opacity=0.6)
    head.move_to(box.get_center() + UP * 0.24)
    body.move_to(box.get_center() + DOWN * 0.20)
    return VGroup(box, head, body)


NARRATION = {
    "title": (
        "Every number carries a clue about its divisors. <bookmark "
        "mark='b0'/>Here are the quick tests for six divisors, with no long "
        "division at all. <bookmark mark='b1'/>Look, add, combine."
    ),
    "scene1": (
        "Hasini has one hundred and twenty five chocolates to share. <bookmark "
        "mark='b0'/>Traders shared grain this way for centuries. <bookmark "
        "mark='b1'/>Five at a time gives twenty five groups; <bookmark "
        "mark='b2'/>six leaves five over. <bookmark mark='b3'/>Every guess "
        "costs a division. <bookmark mark='b4'/>So can we tell without "
        "dividing? <bookmark mark='b5'/>Yes, with a divisibility rule."
    ),
    "scene2": (
        "What does divisible mean? <bookmark mark='b0'/>Twenty four divided by "
        "four is six equal groups, <bookmark mark='b1'/>remainder zero. "
        "<bookmark mark='b2'/>Twenty nine leaves <bookmark mark='b3'/>one over. "
        "<bookmark mark='b4'/>Remainder zero: that is the test. <bookmark "
        "mark='b5'/>Now inspect the digits."
    ),
    "scene3": (
        "Divisibility by two. <bookmark mark='b0'/>Take nine hundred fifty "
        "three <bookmark mark='b1'/>and nine thousand five hundred thirty four. "
        "<bookmark mark='b2'/>Only the ones digit matters. <bookmark "
        "mark='b3'/>Even endings: zero, two, four, six, eight. <bookmark "
        "mark='b4'/>The second passes; <bookmark mark='b5'/>the first does not. "
        "<bookmark mark='b6'/>Ignore every other digit."
    ),
    "scene4": (
        "Divisibility by five and ten. <bookmark mark='b0'/>Five thousand "
        "seven hundred eighty five ends in five: <bookmark mark='b1'/>five "
        "divides it. <bookmark mark='b2'/>One thousand two hundred fifty ends "
        "in zero: <bookmark mark='b3'/>five and ten divide it. <bookmark "
        "mark='b4'/>Two needs even; five needs zero or five; ten needs zero. "
        "<bookmark mark='b5'/>Three rules, one glance."
    ),
    "scene5": (
        "Divisibility by three is different. <bookmark mark='b0'/>Twenty seven "
        "and thirty seven both end in seven, <bookmark mark='b1'/>yet only "
        "twenty seven divides by three. <bookmark mark='b2'/>Add the digits of "
        "thirty six thousand one hundred twenty nine. <bookmark mark='b3'/>"
        "Three, six, one, two, nine: twenty one, which three divides. <bookmark "
        "mark='b4'/>So the number does too."
    ),
    "scene6": (
        "Divisibility by nine: the same digits, a stronger question. "
        "<bookmark mark='b0'/>Nine thousand eight hundred forty six. <bookmark "
        "mark='b1'/>Nine, eight, four, six: twenty seven, which is nine times "
        "three. <bookmark mark='b2'/>So nine divides it. <bookmark "
        "mark='b3'/>Same digits, stronger question."
    ),
    "scene7": (
        "Divisibility by six needs two tests. <bookmark mark='b0'/>Seven "
        "thousand two hundred twenty four ends in four, an even digit. "
        "<bookmark mark='b1'/>Seven, two, two, four: fifteen, and three "
        "divides fifteen. <bookmark mark='b2'/>Both pass, so six divides it. "
        "<bookmark mark='b3'/>Remember the word both."
    ),
    "scene8": (
        "Now use it. <bookmark mark='b0'/>Three hundred seventy two runners "
        "want equal teams of six. <bookmark mark='b1'/>Test two: the number "
        "ends in two. <bookmark mark='b2'/>Test three: three, seven, two, "
        "twelve. <bookmark mark='b3'/>Both pass: sixty two teams, nobody out."
    ),
    "scene9": (
        "Which of two, three, five, six, nine and ten divide twelve thousand "
        "three hundred forty five? <bookmark mark='b0'/>Pause and decide. "
        "<bookmark mark='b1'/>The last digit is five, which is odd: two fails, "
        "and six too. <bookmark mark='b2'/>Five passes, and ten fails. "
        "<bookmark mark='b3'/>The digits add to fifteen: three passes, nine "
        "fails. <bookmark mark='b4'/>Divisible by three and five."
    ),
    "scene10": (
        "All six rules, in three ideas. <bookmark mark='b0'/>Last digit: two "
        "needs even; five needs zero or five; ten needs zero. <bookmark "
        "mark='b1'/>Add the digits: three needs a sum divisible by three; nine "
        "by nine. <bookmark mark='b2'/>Combine: six needs two and three "
        "together. <bookmark mark='b3'/>Look, add, combine. <bookmark "
        "mark='b4'/>Thank you for watching. See you next lesson."
    ),
}


class DivisibilityRulesBasicStory(VoiceoverScene):
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
        out_dir = _HERE / "media" / "videos" / "divisibility_rules_basic_2_3_5_6_9_10"
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

        self.beat0_title()
        self.beat1_chocolate()
        self.beat2_divisible()
        self.beat3_rule2()
        self.beat4_rule5_10()
        self.beat5_rule3()
        self.beat6_rule9()
        self.beat7_rule6()
        self.beat8_application()
        self.beat9_challenge()
        self.beat10_recap()

        self._write_real_srt()

    # ================================================================ beats ==
    # Basic Divisibility Rules for 2, 3, 5, 6, 9 and 10.
    #
    # SYNC RULE for every reveal: wait for the narration bookmark that ends the
    # phrase describing a thing, and only then bring it on.  Playing first and
    # waiting afterwards shows the picture a whole window early (the board was
    # giving away "remainder zero" while the voice was still saying "twenty four
    # divided by four"), which reads as broken sync.
    #
    # Layout rules, so the audits stay clean:
    #   * the heading sits on ROW_Y, the closing strip on STRIP_Y (-1.95);
    #     nothing at all sits below CAPTION_SAFE_Y (-2.15);
    #   * two-column work is centred on LEFT_X and RIGHT_X;
    #   * nothing is placed on a line, and no card, chip or dot is placed over
    #     another element -- checked by audit_clearance.py and
    #     audit_sync_overlap.py.
    def closing(self, tracker, mob=None, color=CHALK_YELLOW, run_time=None):
        """Consume the tail of the narration window on the last reveal."""
        budget = rt(tracker.get_remaining_duration()) if run_time is None \
            else run_time
        if mob is None:
            self.wait(max(budget, 0.0))
        else:
            self.play(Indicate(mob, color=color, scale_factor=1.03),
                      run_time=max(budget, MIN_RT))

    # -- Scene 0: title ------------------------------------------------------
    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Divisibility Rules", 33, CHALK_WHITE,
                               "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 1.62, 0]))
            sub = board_text("Quick Tests for 2, 3, 5, 6, 9 and 10", 20,
                             CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 0.86, 0]))
            chips = VGroup(*[badge_card(d, CHALK_CYAN, size=26)
                             for d in ("2", "3", "5", "6", "9", "10")]
                           ).arrange(RIGHT, buff=0.28).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.16, 0]))
            promise = board_text("Check divisibility without doing the "
                                 "division.", 17, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -1.32, 0]))
            tag = board_text("Look  ·  Add  ·  Combine", 19, CHALK_GREEN,
                             "BOLD").move_to(np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(title, shift=UP * 0.10), run_time=0.5)
            self.play(FadeIn(sub, shift=UP * 0.10), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in chips],
                                  lag_ratio=0.15), run_time=1.0)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(promise, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(tag, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, tag)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: the hook -- sharing, and why the idea is old --------------
    def beat1_chocolate(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("Hasini's Birthday", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            lot = measure_card(r"125\text{ chocolates}", CHALK_YELLOW, 22
                               ).move_to(np.array([BOARD_CX, 2.24, 0]))
            hook = board_text("Traders shared grain this way for centuries.",
                              16, CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX, 1.78, 0]))

            attempts = VGroup()
            for divisor, verdict_text, ok in (
                    ("5", "25 groups,  nothing left", True),
                    ("6", "20 groups,  5 left over", False)):
                attempts.add(VGroup(
                    badge_card(divisor, CHALK_CYAN, size=20, width=0.58,
                               height=0.44),
                    board_text(verdict_text, 15,
                               CHALK_GREEN if ok else CHALK_PINK, "BOLD"),
                    mark_yes(0.9) if ok else mark_no(0.9),
                ).arrange(RIGHT, buff=0.30))
            attempts.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX + 0.05, 0.80, 0]))

            ask = board_text("Can we tell without dividing?", 20, CHALK_GREEN,
                             "BOLD").move_to(np.array([BOARD_CX, -1.16, 0]))
            ask_box = SurroundingRectangle(ask, color=CHALK_GREEN, buff=0.20,
                                           corner_radius=0.10, stroke_width=2.4)
            strip = board_text("Every guess costs another division.", 16,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(lot, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(hook, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(attempts[0], shift=RIGHT * 0.12), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(attempts[1], shift=RIGHT * 0.12), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(ask, shift=UP * 0.08), Create(ask_box),
                      run_time=0.55)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b5"))
            self.closing(tracker, ask_box, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: what does "divisible" mean? --------------------------------
    def beat2_divisible(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("What Does \u201cDivisible\u201d Mean?", 23,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, ROW_Y, 0]))
            l_head = number_card(24, CHALK_WHITE, size=24).move_to(
                np.array([LEFT_X, 2.02, 0]))
            r_head = number_card(29, CHALK_WHITE, size=24).move_to(
                np.array([RIGHT_X, 2.02, 0]))

            # The two share-box grids are TOP-aligned, so the three-row grid of
            # 29 sets the height and the verdict rows below are clear of both.
            l_grid = chocolate_groups(6, per_group=4, cols=3).scale(0.80)
            r_grid = chocolate_groups(7, per_group=4, cols=3).scale(0.80)
            l_grid.shift(UP * (1.42 - l_grid.get_top()[1]))
            r_grid.shift(UP * (1.42 - r_grid.get_top()[1]))
            l_grid.move_to(np.array([LEFT_X, l_grid.get_center()[1], 0]))
            r_grid.move_to(np.array([RIGHT_X, r_grid.get_center()[1], 0]))
            # the one left-over chocolate sits beside the seventh share-box,
            # not under it where the verdict row runs
            lone = Dot(radius=0.06, color=CHALK_YELLOW).next_to(
                r_grid[-1], RIGHT, buff=0.18)

            l_rem = verdict(True, "Remainder 0", size=15).move_to(
                np.array([LEFT_X, -0.22, 0]))
            r_rem = verdict(False, "Remainder 1", size=15).move_to(
                np.array([RIGHT_X, -0.22, 0]))
            l_tag = board_text("DIVISIBLE", 18, CHALK_GREEN, "BOLD").move_to(
                np.array([LEFT_X, -0.78, 0]))
            r_tag = board_text("NOT DIVISIBLE", 18, CHALK_PINK, "BOLD"
                               ).move_to(np.array([RIGHT_X, -0.78, 0]))

            rule = board_text("Remainder 0  \u2192  exactly divisible", 19,
                              CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -1.40, 0]))
            rule_box = SurroundingRectangle(rule, color=CHALK_GREEN, buff=0.20,
                                            corner_radius=0.10, stroke_width=2.4)
            strip = board_text("Now let us inspect the digits.", 16,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(l_head), FadeIn(r_head), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(b) for b in l_grid], lag_ratio=0.16),
                      run_time=1.1)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(l_rem), FadeIn(l_tag), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(LaggedStart(*[FadeIn(b) for b in r_grid], lag_ratio=0.14),
                      run_time=1.2)
            self.play(FadeIn(lone, scale=0.6), run_time=0.3)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(r_rem), FadeIn(r_tag), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(rule, shift=UP * 0.08), Create(rule_box),
                      run_time=0.5)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.45)
            self.closing(tracker, rule_box, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: divisibility by 2 ------------------------------------------
    def beat3_rule2(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()

            heading = board_text("Divisibility by 2", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            tiles = VGroup()
            rings = VGroup()
            verdicts = VGroup()
            for value in ("953", "9534"):
                grp, parts = digit_tiles(value, size=29)
                tiles.add(grp)
                rings.add(tile_ring(parts[-1]))
                ok = value[-1] in "02468"
                verdicts.add(VGroup(
                    mark_yes(1.0) if ok else mark_no(1.0),
                    board_text("yes" if ok else "no", 16,
                               CHALK_GREEN if ok else CHALK_PINK, "BOLD"),
                ).arrange(RIGHT, buff=0.16))
            tiles.arrange(RIGHT, buff=1.00).move_to(
                np.array([BOARD_CX, 1.94, 0]))
            for ring, tile_row in zip(rings, tiles):
                ring.move_to(tile_row[-1].get_center())
            verdicts.arrange(RIGHT, buff=1.62).move_to(
                np.array([BOARD_CX - 0.02, 1.16, 0]))
            # the "yes" verdict belongs to the second number, the "no" to the
            # first, so they are revealed separately, under their own number
            yes_mark = verdicts[1].move_to(np.array([tiles[1].get_center()[0],
                                                     1.16, 0]))
            no_mark = verdicts[0].move_to(np.array([tiles[0].get_center()[0],
                                                    1.16, 0]))

            even_head = board_text("Even ending digits", 17, CHALK_CYAN, "BOLD"
                                   ).move_to(np.array([BOARD_CX, 0.36, 0]))
            even_tiles = VGroup(*[badge_card(d, CHALK_GREEN, size=22, width=0.54,
                                             height=0.52)
                                  for d in ("0", "2", "4", "6", "8")]
                                ).arrange(RIGHT, buff=0.22).move_to(
                np.array([BOARD_CX, -0.26, 0]))

            rule = board_text("Divisible by 2  \u2192  the ones digit is "
                              "0, 2, 4, 6 or 8", 19, CHALK_YELLOW, "BOLD"
                              ).move_to(np.array([BOARD_CX, -1.28, 0]))
            rule_box = SurroundingRectangle(rule, color=CHALK_YELLOW, buff=0.20,
                                            corner_radius=0.10, stroke_width=2.4)
            strip = board_text("For 2, ignore every digit except the last one.",
                               16, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(tiles[0]), run_time=0.35)
            self.play(Create(rings[0]), run_time=0.3)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(tiles[1]), run_time=0.35)
            self.play(Create(rings[1]), run_time=0.3)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(Indicate(rings, color=CHALK_YELLOW, scale_factor=1.06),
                      run_time=0.6)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(even_head, shift=UP * 0.08), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.10)
                                    for t in even_tiles], lag_ratio=0.16),
                      run_time=0.8)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(yes_mark, shift=DOWN * 0.08), run_time=0.4)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(no_mark, shift=DOWN * 0.08), run_time=0.4)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(rule, shift=UP * 0.08), Create(rule_box),
                      run_time=0.55)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, rule_box)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: divisibility by 5 and 10 -----------------------------------
    def beat4_rule5_10(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()

            heading = board_text("Divisibility by 5 and 10", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))

            l_tiles, l_parts = digit_tiles("5785", size=24)
            l_tiles.move_to(np.array([LEFT_X, 2.00, 0]))
            l_ring = tile_ring(l_parts[-1], CHALK_YELLOW)
            r_tiles, r_parts = digit_tiles("1250", size=24)
            r_tiles.move_to(np.array([RIGHT_X, 2.00, 0]))
            r_ring = tile_ring(r_parts[-1], CHALK_YELLOW)

            l_checks = VGroup(verdict(True, "ones digit 5  \u2192  \u00f75",
                                      size=15)).move_to(
                np.array([LEFT_X, 1.22, 0]))
            r_checks = VGroup(
                verdict(True, "ones digit 0  \u2192  \u00f75", size=15),
                verdict(True, "ones digit 0  \u2192  \u00f710", size=15),
            ).arrange(DOWN, buff=0.18).move_to(np.array([RIGHT_X, 1.13, 0]))

            rules = VGroup(
                rule_line("2", "0, 2, 4, 6, 8", CHALK_CYAN, width=2.9),
                rule_line("5", "0 or 5", CHALK_GREEN, width=2.9),
                rule_line("10", "0", CHALK_PINK, width=2.9),
            ).arrange(RIGHT, buff=0.32).move_to(
                np.array([BOARD_CX, -0.34, 0]))
            title = board_text("LAST-DIGIT RULES", 20, CHALK_YELLOW, "BOLD"
                               ).move_to(np.array([BOARD_CX, -1.32, 0]))
            title_box = SurroundingRectangle(title, color=CHALK_YELLOW,
                                             buff=0.18, corner_radius=0.10,
                                             stroke_width=2.4)
            strip = board_text("Three rules, one glance.", 16, CHALK_WHITE,
                               "BOLD").move_to(np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(l_tiles), run_time=0.35)
            self.play(Create(l_ring), run_time=0.3)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(l_checks), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(r_tiles), run_time=0.35)
            self.play(Create(r_ring), run_time=0.3)

            self.wait(leftover(tracker, "b3"))
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.10)
                                    for c in r_checks], lag_ratio=0.3),
                      run_time=0.7)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.08)
                                    for r in rules], lag_ratio=0.22),
                      run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(title, shift=UP * 0.08), Create(title_box),
                      run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, title_box)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: divisibility by 3 ------------------------------------------
    def beat5_rule3(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            self.reset_board()

            heading = board_text("Divisibility by 3", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))

            l_grp, l_parts = digit_tiles("27", size=24)
            r_grp, r_parts = digit_tiles("37", size=24)
            l_grp.move_to(np.array([LEFT_X, 2.02, 0]))
            r_grp.move_to(np.array([RIGHT_X, 2.02, 0]))
            l_ring = tile_ring(l_parts[-1])
            r_ring = tile_ring(r_parts[-1])
            same = board_text("Same last digit \u2014 different answer.", 17,
                              CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, 1.38, 0]))
            l_mark = verdict(True, "27 \u00f7 3", size=15).move_to(
                np.array([LEFT_X, 0.94, 0]))
            r_mark = verdict(False, "37 \u00f7 3", size=15).move_to(
                np.array([RIGHT_X, 0.94, 0]))

            big, big_parts = digit_tiles("36129", size=27)
            big.move_to(np.array([BOARD_CX, 0.16, 0]))
            expr = chalk_math(r"3+6+1+2+9 = 21", size=30, color=CHALK_YELLOW
                              ).move_to(np.array([BOARD_CX, -0.60, 0]))
            result = board_text("21 \u00f7 3 is exact  \u2192  36129 is "
                                "divisible by 3", 18, CHALK_GREEN, "BOLD"
                                ).move_to(np.array([BOARD_CX, -1.30, 0]))
            result_box = SurroundingRectangle(result, color=CHALK_GREEN,
                                              buff=0.18, corner_radius=0.10,
                                              stroke_width=2.4)
            strip = board_text("Digit sum divisible by 3  \u2192  number "
                               "divisible by 3.", 16, CHALK_WHITE, "BOLD"
                               ).move_to(np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(l_grp), FadeIn(r_grp), run_time=0.45)
            self.play(Create(l_ring), Create(r_ring), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(same, shift=UP * 0.08), run_time=0.4)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(l_mark), FadeIn(r_mark), run_time=0.45)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(big), run_time=0.5)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(expr, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(result, shift=UP * 0.08), Create(result_box),
                      run_time=0.55)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, result_box, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: divisibility by 9 ------------------------------------------
    def beat6_rule9(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("Divisibility by 9", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            num, parts = digit_tiles("9846", size=27)
            num.move_to(np.array([BOARD_CX, 2.00, 0]))
            expr = chalk_math(r"9+8+4+6 = 27", size=30, color=CHALK_YELLOW
                              ).move_to(np.array([BOARD_CX, 1.22, 0]))
            times = chalk_math(r"27 = 9 \times 3", size=28, color=CHALK_CYAN
                               ).move_to(np.array([BOARD_CX, 0.56, 0]))
            result = board_text("9846 is divisible by 9", 19, CHALK_GREEN,
                                "BOLD").move_to(
                np.array([BOARD_CX, -0.18, 0]))
            result_box = SurroundingRectangle(result, color=CHALK_GREEN,
                                              buff=0.18, corner_radius=0.10,
                                              stroke_width=2.4)
            rules = VGroup(
                rule_line("\u00f73", "sum divisible by 3", CHALK_CYAN,
                          width=3.6),
                rule_line("\u00f79", "sum divisible by 9", CHALK_GREEN,
                          width=3.6),
            ).arrange(RIGHT, buff=0.36).move_to(
                np.array([BOARD_CX, -1.16, 0]))
            strip = board_text("3 and 9  \u2192  ADD THE DIGITS", 18,
                               CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(num), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(expr, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(times, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(result, shift=UP * 0.08), Create(result_box),
                      run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.08)
                                    for r in rules], lag_ratio=0.25),
                      run_time=0.8)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.45)
            self.closing(tracker, result_box, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: divisibility by 6 ------------------------------------------
    def beat7_rule6(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("Divisibility by 6", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            num, parts = digit_tiles("7224", size=27)
            num.move_to(np.array([BOARD_CX, 2.04, 0]))

            gate_two = gate("\u00f72 test", "last digit 4", CHALK_CYAN)
            gate_two.move_to(np.array([LEFT_X, 1.06, 0]))
            gate_three = gate("\u00f73 test", "7+2+2+4 = 15", CHALK_PINK)
            gate_three.move_to(np.array([RIGHT_X, 1.06, 0]))
            tick_two = mark_yes(0.95).move_to(gate_two.get_corner(UR)
                                              + np.array([-0.24, -0.26, 0]))
            tick_three = mark_yes(0.95).move_to(gate_three.get_corner(UR)
                                                + np.array([-0.24, -0.26, 0]))
            gate_two = VGroup(gate_two, tick_two)
            gate_three = VGroup(gate_three, tick_three)

            six = badge_card("6", CHALK_GREEN, size=30, width=0.86, height=0.86
                             ).move_to(np.array([BOARD_CX, 0.02, 0]))
            left_arrow = Arrow(gate_two.get_bottom() + DOWN * 0.04,
                               six.get_left() + LEFT * 0.06, buff=0,
                               color=CHALK_CYAN, stroke_width=2.6,
                               tip_length=0.16,
                               max_stroke_width_to_length_ratio=10)
            right_arrow = Arrow(gate_three.get_bottom() + DOWN * 0.04,
                                six.get_right() + RIGHT * 0.06, buff=0,
                                color=CHALK_PINK, stroke_width=2.6,
                                tip_length=0.16,
                                max_stroke_width_to_length_ratio=10)

            result = board_text("7224 is divisible by 6", 19, CHALK_GREEN,
                                "BOLD").move_to(np.array([BOARD_CX, -0.92, 0]))
            result_box = SurroundingRectangle(result, color=CHALK_GREEN,
                                              buff=0.18, corner_radius=0.10,
                                              stroke_width=2.4)
            strip = board_text("Divisible by 6  =  divisible by BOTH 2 and 3.",
                               16, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(num), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(gate_two), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(gate_three), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(GrowArrow(left_arrow), GrowArrow(right_arrow),
                      run_time=0.6)
            self.play(FadeIn(six, scale=0.7), run_time=0.4)
            self.play(FadeIn(result, shift=UP * 0.08), Create(result_box),
                      run_time=0.5)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.45)
            self.closing(tracker, result_box, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: real life -- 372 runners into teams of six -----------------
    def beat8_application(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("Use It: Relay Teams of Six", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            lot = measure_card(r"372\text{ runners}", CHALK_YELLOW, 22
                               ).move_to(np.array([BOARD_CX, 2.02, 0]))

            gate_two = gate("\u00f72 test", "ends in 2", CHALK_CYAN)
            gate_two.move_to(np.array([LEFT_X, 1.02, 0]))
            gate_three = gate("\u00f73 test", "3+7+2 = 12", CHALK_PINK)
            gate_three.move_to(np.array([RIGHT_X, 1.02, 0]))
            tick_two = mark_yes(0.95).move_to(gate_two.get_corner(UR)
                                              + np.array([-0.24, -0.26, 0]))
            tick_three = mark_yes(0.95).move_to(gate_three.get_corner(UR)
                                                + np.array([-0.24, -0.26, 0]))
            gate_two = VGroup(gate_two, tick_two)
            gate_three = VGroup(gate_three, tick_three)

            six = badge_card("6", CHALK_GREEN, size=30, width=0.86, height=0.86
                             ).move_to(np.array([BOARD_CX, -0.02, 0]))
            left_arrow = Arrow(gate_two.get_bottom() + DOWN * 0.04,
                               six.get_left() + LEFT * 0.06, buff=0,
                               color=CHALK_CYAN, stroke_width=2.6,
                               tip_length=0.16,
                               max_stroke_width_to_length_ratio=10)
            right_arrow = Arrow(gate_three.get_bottom() + DOWN * 0.04,
                                six.get_right() + RIGHT * 0.06, buff=0,
                                color=CHALK_PINK, stroke_width=2.6,
                                tip_length=0.16,
                                max_stroke_width_to_length_ratio=10)

            answer = board_text("62 teams  \u00b7  nobody left out",
                                21, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -0.98, 0]))
            answer_box = SurroundingRectangle(answer, color=CHALK_GREEN,
                                              buff=0.20, corner_radius=0.10,
                                              stroke_width=2.4)
            strip = board_text("6 \u00d7 62 = 372, and no long division.",
                               16, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(lot, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(gate_two), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(gate_three), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(GrowArrow(left_arrow), GrowArrow(right_arrow),
                      run_time=0.6)
            self.play(FadeIn(six, scale=0.7), run_time=0.4)
            self.play(FadeIn(answer, shift=UP * 0.08), Create(answer_box),
                      run_time=0.5)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.45)
            self.closing(tracker, answer_box, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 9: your turn -- test 12345 ------------------------------------
    def beat9_challenge(self) -> None:
        with self.voiceover(text=NARRATION["scene9"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", 26, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, 2.62, 0]))
            sub = board_text("Which of these divide 12345?", 18,
                             CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, 2.24, 0]))

            divisors = ("2", "3", "5", "6", "9", "10")
            buttons = VGroup(*[badge_card(d, CHALK_AMBER, size=26, width=0.80,
                                          height=0.64) for d in divisors]
                             ).arrange(RIGHT, buff=0.44).move_to(
                np.array([BOARD_CX, 1.66, 0]))
            marks = {d: (mark_no(1.0, CHALK_RED) if d in ("2", "6", "9", "10")
                         else mark_yes(1.0)).move_to(
                np.array([buttons[i].get_center()[0], 1.16, 0]))
                for i, d in enumerate(divisors)}

            num, parts = digit_tiles("12345", size=31)
            num.move_to(np.array([BOARD_CX, 0.46, 0]))

            why_three = board_text("1+2+3+4+5 = 15  \u2192  divisible by 3",
                                   22, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -0.46, 0]))
            why_five = board_text("ends in 5  \u2192  divisible by 5", 22,
                                  CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -1.02, 0]))
            answer = board_text("12345 is divisible by 3 and by 5.", 20,
                                CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.68, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(sub), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.08)
                                    for b in buttons], lag_ratio=0.12),
                      run_time=0.8)
            self.play(FadeIn(num), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            # the shared THINK clock, centred on the board (story_common)
            play_challenge_countdown(self, seconds=4, sfx=self.sfx,
                                     position=np.array([BOARD_CX, BOARD_CY, 0]))

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(marks["2"], scale=0.7),
                      FadeIn(marks["6"], scale=0.7), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(marks["5"], scale=0.7),
                      FadeIn(marks["10"], scale=0.7), run_time=0.5)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(marks["3"], scale=0.7),
                      FadeIn(marks["9"], scale=0.7),
                      FadeIn(why_three, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(why_five, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(answer, shift=UP * 0.08), run_time=0.5)
            self.closing(tracker, answer, color=CHALK_YELLOW)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap and thank-you ---------------------------------------
    def beat10_recap(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("Divisibility Rules", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            rows = VGroup(
                rule_line("LAST DIGIT", "2: 0,2,4,6,8   \u00b7   5: 0 or 5"
                                        "   \u00b7   10: 0", CHALK_CYAN,
                          width=8.6, size=19),
                rule_line("ADD THE DIGITS", "3: sum \u00f7 3   \u00b7   "
                                            "9: sum \u00f7 9", CHALK_GREEN,
                          width=8.6, size=19),
                rule_line("COMBINE TWO TESTS", "6: divisible by 2 AND by 3",
                          CHALK_PINK, width=8.6, size=19),
            ).arrange(DOWN, buff=0.24, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX, 1.08, 0]))

            examples = board_text("452 \u2192 2     5785 \u2192 5     "
                                  "9846 \u2192 9     7224 \u2192 6", 18,
                                  CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -0.52, 0]))
            message = board_text("LOOK.  ADD.  COMBINE.", 24, CHALK_YELLOW,
                                 "BOLD").move_to(
                np.array([BOARD_CX, -1.18, 0]))
            promise = board_text("Check divisibility without doing the "
                                 "division.", 16, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            thanks = board_text("Thank You for Watching!", 30, CHALK_WHITE,
                                "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 0.42, 0]))
            bye = board_text("See you in the next lesson :)", 22, CHALK_YELLOW,
                             "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY - 0.52, 0]))
            board_group = VGroup(heading, rows, examples, message, promise)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(rows[0], shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(rows[1], shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(rows[2], shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(examples, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(message, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(promise, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)

            self.wait(leftover(tracker, "b4"))
            # the closing card, over the same board
            self.play(FadeOut(board_group), run_time=0.5)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.5)
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.play(Indicate(thanks, color=CHALK_YELLOW, scale_factor=1.03),
                      run_time=rt(tracker.get_remaining_duration()))
            self._capture_srt(tracker)

        self.wait(END_HOLD)

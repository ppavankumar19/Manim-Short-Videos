"""
Advanced Divisibility Tests: How to Instantly Test Divisibility by 4, 8 and 11
Story-mode chalkboard lesson (Telangana Class 6 Maths, Chapter 3:
Playing with Numbers, Storymode 02).

LLM KEY / FUNCTION NAME: divisibility_rules_advanced_4_8_11

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
  - Nothing on the board sits below CAPTION_SAFE_Y (-2.00): the burned-in
    caption grows up from the bottom of the frame.

The defining visual is the scanner from the previous video, upgraded with three
new modes:

  * 4  ->  a TWO-digit lens over the end of the number, because 100 divides by 4,
  * 8  ->  a THREE-digit lens, because 1000 divides by 8,
  * 11 ->  an alternating-position sorter: digits jump into odd/even baskets,
           the two sums are compared, and the difference must be 0 or a
           multiple of 11.

Cold open + title + 11 scenes:
  C. Why these tests? -- the calendar, a tiler and a bank (real-world hook).
  0. Title card.
  1. The scanner gains three modes: 4, 8 and 11.
  2. Why 4 needs only two digits (76532 = 76500 + 32, and 100 = 4 x 25).
  3. Apply it to the textbook's 56496 (last two digits 96 = 4 x 24).
  4. Why 8 needs three digits (1000 = 8 x 125, 93624 = 93000 + 624).
  5. Two lenses on one number (2104): 4 looks at two, 8 looks at three.
  6. Divisibility by 11: 1221 -> (1+2) and (2+1), difference 0.
  7. The same test failing: 6535 -> 10 - 9 = 1, so not divisible by 11.
  8. Three rules, three clues: last 2 / last 3 / alternating sums.
  9. A real stadium: 56496 seats into four-seat boxes, nothing left over.
 10. Your turn, staged: 726352 by 4 and 8 on the left, cleared, then 10824 by
    11 centred in larger type.
 11. Recap and thank-you.
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
# The burned-in caption grows up from the bottom of the frame: a one-line cue
# starts at y = -3.38 and a wrapped two-line cue reaches y = -2.93 (measured on
# the burned 360p cut).  The production audit still asked for the closing
# banners to move clear of the subtitle zone, so the strip was lifted 0.15 --
# roughly 15% of the banner band it lives in -- from -1.95 to -1.80, and the row
# above it was lifted with it.  The lowest ink on the board is now the strip's
# own baseline at -1.93 and nothing at all sits below CAPTION_SAFE_Y = -2.00 --
# audited by the IN-CAPTION-BAND check in audit_sync_overlap.py.
STRIP_Y = -1.80

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


def digit_tiles(number, size=26, color=CHALK_WHITE, buff=0.10,
                tile_w=TILE_W, tile_h=TILE_H):
    """Each digit of `number` as its own tile: returns (group, [tiles])."""
    tiles = []
    for ch in str(number):
        lab = chalk_math(ch, size=size, color=color)
        box = RoundedRectangle(corner_radius=0.06, width=tile_w, height=tile_h,
                               stroke_color=CHALK_WHITE, stroke_width=1.5,
                               fill_color=PANEL_FILL, fill_opacity=0.5)
        lab.move_to(box.get_center())
        tiles.append(VGroup(box, lab))
    grp = VGroup(*tiles).arrange(RIGHT, buff=buff)
    return grp, list(grp)


def tile_ring(tile, color=CHALK_YELLOW, buff=0.07):
    """A ring around a single digit."""
    return RoundedRectangle(corner_radius=0.08, width=TILE_W + 2 * buff + 0.08,
                            height=TILE_H + 2 * buff + 0.08, stroke_color=color,
                            stroke_width=3.0).move_to(tile.get_center())


def digit_lens(tiles, k, color=CHALK_YELLOW, buff=0.10, width_pad=0.32):
    """The scanner lens: a window over the last `k` tiles of a number."""
    last = tiles[-k:]
    left, right = last[0].get_left()[0], last[-1].get_right()[0]
    top, bottom = last[0].get_top()[1], last[0].get_bottom()[1]
    box = RoundedRectangle(corner_radius=0.10,
                           width=(right - left) + width_pad,
                           height=(top - bottom) + 2 * buff + 0.08,
                           stroke_color=color, stroke_width=3.2)
    box.move_to(np.array([(left + right) / 2.0, (top + bottom) / 2.0, 0]))
    return box


def dim_outside(tiles, k):
    """The original tiles outside the lens, so they can be faded in place.

    Fading a *copy* over the original would draw every digit twice (and the
    audits rightly report the two glyphs as text-in-text)."""
    return VGroup(*[tile for i, tile in enumerate(tiles)
                    if i < len(tiles) - k])


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


def rule_line(label, detail, color=CHALK_WHITE, width=None, size=17):
    """One rule as a card: the divisor badge and its test."""
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


def zone_panel(title, lines, color=CHALK_WHITE, width=3.0, height=2.30,
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


def basket(label, terms, total, color=CHALK_WHITE, width=3.4, height=1.45,
           size=16):
    """One alternating-position basket for the 11 test: label, sum, total."""
    head = board_text(label, size, color, "BOLD")
    body = chalk_math(terms, size=26, color=CHALK_YELLOW)
    box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                           stroke_color=color, stroke_width=2.0,
                           fill_color=PANEL_FILL, fill_opacity=0.6)
    head.move_to(box.get_center() + UP * 0.42)
    body.move_to(box.get_center() + DOWN * 0.16)
    grp = VGroup(box, head, body)
    grp.head, grp.body, grp.total = head, body, total
    return grp


def place_tags(tiles, letters=("odd", "even"), color=CHALK_CYAN, size=11,
               y_shift=-0.42):
    """Label each digit with the parity of its place, counting from the right."""
    tags = VGroup()
    for i, tile in enumerate(reversed(tiles)):        # right to left
        word = letters[i % 2]
        tags.add(board_text(word, size, color, "BOLD").move_to(
            tile.get_center() + DOWN * abs(y_shift)))
    return tags


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
    # Cold open: the production audit asked for a real-world hook before the
    # title card, so the video no longer opens on "three more divisibility
    # tests" with no reason to care.
    "hook": (
        "These tests are not only for the classroom. <bookmark mark='b0'/>A "
        "leap year arrives every four years. <bookmark mark='b1'/>A tiler "
        "checks whether eight tiles fit the wall. <bookmark mark='b2'/>A bank "
        "reads eleven on long account numbers."
    ),
    "title": (
        "Three more divisibility tests. <bookmark mark='b0'/>Four, eight and "
        "eleven need more than the last digit, and more than the digit sum. "
        "<bookmark mark='b1'/>Zoom in, zoom deeper, and alternate."
    ),
    "scene1": (
        "The scanner knows six rules: two, three, five, six, nine and ten. "
        "<bookmark mark='b0'/>Three new numbers join them: four, eight and "
        "eleven. <bookmark mark='b1'/>One digit is not enough for these. "
        "<bookmark mark='b2'/>Four and eight look deeper; eleven needs a new "
        "idea."
    ),
    "scene2": (
        "Divisibility by four. <bookmark mark='b0'/>Seventy six thousand five "
        "hundred thirty two is seventy six thousand five hundred, plus thirty "
        "two. <bookmark mark='b1'/>The first part is a multiple of one hundred, "
        "which divides by four. <bookmark mark='b2'/>So it is already divisible "
        "by four. <bookmark mark='b3'/>Only thirty two is left, and it divides "
        "by four."
    ),
    "scene3": (
        "Now use it on fifty six thousand four hundred ninety six. <bookmark "
        "mark='b0'/>The lens closes on ninety six. <bookmark mark='b1'/>Ninety "
        "six is four times twenty four, so it passes. <bookmark mark='b2'/>So "
        "the whole number divides by four. <bookmark mark='b3'/>The test works "
        "above one hundred."
    ),
    "scene4": (
        "Divisibility by eight. <bookmark mark='b0'/>One hundred fails, but "
        "one thousand works: eight times one hundred twenty five. <bookmark "
        "mark='b1'/>Break ninety three thousand six hundred twenty four into "
        "two parts: ninety three thousand, plus six hundred twenty four. "
        "<bookmark mark='b2'/>That part is a multiple of one thousand, so eight "
        "already divides it. <bookmark mark='b3'/>And six hundred twenty four "
        "divides by eight exactly."
    ),
    "scene5": (
        "Do not mix the two. Take two thousand one hundred four. <bookmark "
        "mark='b0'/>For four, the last two digits are zero four: four itself. "
        "<bookmark mark='b1'/>For eight, the last three: one hundred four, "
        "eight times thirteen. <bookmark mark='b2'/>Four looks at two digits, "
        "eight at three."
    ),
    "scene6": (
        "Divisibility by eleven. <bookmark mark='b0'/>Count the places from the "
        "right: odd, even, odd, even. <bookmark mark='b1'/>Odd places: one plus "
        "two is three. <bookmark mark='b2'/>Even places: two plus one is three. "
        "<bookmark mark='b3'/>Compare: three minus three is zero. <bookmark "
        "mark='b4'/>Zero: eleven divides it."
    ),
    "scene7": (
        "Now a number that fails. <bookmark mark='b0'/>Six thousand five "
        "hundred thirty five. <bookmark mark='b1'/>Odd places: five plus five, "
        "ten. Even places: three plus six, nine. <bookmark mark='b2'/>Ten minus "
        "nine is one. <bookmark mark='b3'/>One is not zero and not a multiple "
        "of eleven."
    ),
    "scene8": (
        "Three advanced rules, three clues. <bookmark mark='b0'/>For four, zoom "
        "into the last two digits. <bookmark mark='b1'/>For eight, zoom into "
        "the last three. <bookmark mark='b2'/>For eleven, split the digits into "
        "two alternating groups and compare their sums."
    ),
    # The second audit addition: one 10-15 s real-world application between the
    # dashboard and "Your Turn", using the textbook's own 56496.
    "apply": (
        "Fifty six thousand four hundred ninety six seats go into four-seat "
        "boxes. <bookmark mark='b0'/>Does anything stay empty? <bookmark "
        "mark='b1'/>The last two digits, ninety six, divide by four. <bookmark "
        "mark='b2'/>So the whole number does. <bookmark mark='b3'/>No seat is "
        "left over."
    ),
    "scene9": (
        "Your turn. <bookmark mark='b0'/>First, seven hundred twenty six "
        "thousand three hundred fifty two. <bookmark mark='b1'/>Pause and "
        "decide. <bookmark mark='b2'/>Last two digits, fifty two: four divides "
        "it. Last three digits, three hundred fifty two: eight divides it too. "
        "<bookmark mark='b3'/>So that number passes both tests. <bookmark "
        "mark='b4'/>Now a second number: ten thousand eight hundred twenty "
        "four. <bookmark mark='b5'/>Odd places thirteen, even places two. "
        "<bookmark mark='b6'/>Thirteen minus two is eleven, so eleven divides "
        "it."
    ),
    "scene10": (
        "One last look. <bookmark mark='b0'/>Four: the last two digits. "
        "<bookmark mark='b1'/>Eight: the last three digits. <bookmark "
        "mark='b2'/>Eleven: alternate the places, add each group, compare. "
        "<bookmark mark='b3'/>Zoom, zoom more, alternate. <bookmark "
        "mark='b4'/>Thank you for watching, and see you in the next lesson."
    ),
}


class DivisibilityRulesAdvancedStory(VoiceoverScene):
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
        out_dir = _HERE / "media" / "videos" / "divisibility_rules_advanced_4_8_11"
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

        self.beat_cold_open()
        self.beat0_title()
        self.beat1_hook()
        self.beat2_why4()
        self.beat3_apply4()
        self.beat4_why8()
        self.beat5_two_lenses()
        self.beat6_rule11()
        self.beat7_11_fails()
        self.beat8_dashboard()
        self.beat_apply()
        self.beat9_challenge()
        self.beat10_recap()

        self._write_real_srt()

    # ================================================================ beats ==
    # Advanced Divisibility Rules for 4, 8 and 11.
    #
    # SYNC RULE for every reveal: wait for the narration bookmark that ends the
    # phrase describing a thing, and only then bring it on.  Playing first and
    # waiting afterwards shows the picture a whole window early, which reads as
    # broken sync.
    #
    # Layout rules, so the audits stay clean:
    #   * the heading sits on ROW_Y, the closing strip on STRIP_Y (-1.80, lifted
    #     0.15 clear of the subtitle zone after the production audit);
    #     nothing at all sits below CAPTION_SAFE_Y (-2.00);
    #   * two-column work is centred on LEFT_X and RIGHT_X;
    #   * nothing is placed on a line, and no card, chip or dot is placed over
    #     another element -- checked by audit_clearance.py and
    #     audit_sync_overlap.py.
    #
    # Scene order: a real-world cold open, the title, the six known rules, why 4
    # and 8 need two and three digits (with the textbook's 56496 and 93624), the
    # two lenses, the alternating test for 11 and a number that fails it, the
    # three-clue dashboard, a stadium-sized application, the staged challenge and
    # the recap.
    def closing(self, tracker, mob=None, color=CHALK_YELLOW, run_time=None):
        """Consume the tail of the narration window on the last reveal."""
        budget = rt(tracker.get_remaining_duration()) if run_time is None \
            else run_time
        if mob is None:
            self.wait(max(budget, 0.0))
        else:
            self.play(Indicate(mob, color=color, scale_factor=1.03),
                      run_time=max(budget, MIN_RT))

    # -- Scene 0a: cold open -- why anyone cares ------------------------------
    # The production audit's first note: the video used to open on "three more
    # divisibility tests", a promise with nothing behind it.  This scene runs
    # BEFORE the title card and grounds 4, 8 and 11 in places the class has
    # already met them: the calendar, tiling, and a bank account number.
    def beat_cold_open(self) -> None:
        with self.voiceover(text=NARRATION["hook"]) as tracker:
            self.reset_board()

            heading = board_text("Why These Tests?", 26, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))

            rows = VGroup(
                VGroup(badge_card("4", CHALK_CYAN, size=24, width=0.72,
                                  height=0.62),
                       board_text("a leap year comes every four years", 16,
                                  CHALK_WHITE, "BOLD")).arrange(RIGHT, buff=0.30),
                VGroup(badge_card("8", CHALK_GREEN, size=24, width=0.72,
                                  height=0.62),
                       board_text("a tiler checks if eight tiles fit", 16,
                                  CHALK_WHITE, "BOLD")).arrange(RIGHT, buff=0.30),
                VGroup(badge_card("11", CHALK_PINK, size=24, width=0.72,
                                  height=0.62),
                       board_text("a bank reads long account numbers", 16,
                                  CHALK_WHITE, "BOLD")).arrange(RIGHT, buff=0.30),
            ).arrange(DOWN, buff=0.42).move_to(
                np.array([BOARD_CX, 0.62, 0]))
            punch = board_text("The tests are already around you.", 18,
                               CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.16, 0]))
            strip = board_text("Look for them outside the textbook.", 16,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(rows[0], shift=RIGHT * 0.10), run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(rows[1], shift=RIGHT * 0.10), run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(rows[2], shift=RIGHT * 0.10), run_time=0.5)
            self.play(FadeIn(punch, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, punch)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 0: title ------------------------------------------------------
    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Advanced Divisibility Tests", 30, CHALK_WHITE,
                               "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 1.62, 0]))
            sub = board_text("Quick Tests for 4, 8 and 11", 20, CHALK_YELLOW,
                             "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 0.86, 0]))
            chips = VGroup(*[badge_card(d, CHALK_CYAN, size=30, width=0.96,
                                        height=0.80)
                             for d in ("4", "8", "11")]
                           ).arrange(RIGHT, buff=0.60).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.24, 0]))
            promise = board_text("Test divisibility without dividing the whole "
                                 "number.", 16, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -1.20, 0]))
            tag = board_text("Zoom  ·  Zoom deeper  ·  Alternate", 19,
                             CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(title, shift=UP * 0.10), run_time=0.5)
            self.play(FadeIn(sub, shift=UP * 0.10), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in chips],
                                  lag_ratio=0.18), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(promise, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(tag, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, tag)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: the scanner gains three modes ------------------------------
    def beat1_hook(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("New Numbers, New Patterns", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            known = VGroup(*[badge_card(d, CHALK_WHITE, size=20, width=0.62,
                                        height=0.50)
                             for d in ("2", "3", "5", "6", "9", "10")]
                           ).arrange(RIGHT, buff=0.30).move_to(
                np.array([BOARD_CX, 1.98, 0]))
            known_note = board_text("the six rules you already know", 15,
                                    CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, 1.52, 0]))

            fresh = VGroup(*[badge_card(d, CHALK_CYAN, size=30, width=0.96,
                                        height=0.80)
                             for d in ("4", "8", "11")]
                           ).arrange(RIGHT, buff=0.60).move_to(
                np.array([BOARD_CX, 0.66, 0]))
            fresh_note = board_text("three new rules", 16, CHALK_CYAN, "BOLD"
                                    ).move_to(np.array([BOARD_CX, 0.06, 0]))

            question = board_text("One digit is not enough.", 19, CHALK_PINK,
                                  "BOLD").move_to(np.array([BOARD_CX, -0.60, 0]))
            answer = board_text("Four and eight look deeper.  Eleven "
                                "alternates.", 17, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -1.18, 0]))
            strip = board_text("Find the pattern. Avoid full division.", 16,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.08)
                                    for c in known], lag_ratio=0.12),
                      run_time=0.7)
            self.play(FadeIn(known_note), run_time=0.35)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in fresh],
                                  lag_ratio=0.25), run_time=0.9)
            self.play(FadeIn(fresh_note), run_time=0.35)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(question, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(answer, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["click"], gain=-15)
            self.closing(tracker, answer, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: why 4 needs only two digits --------------------------------
    def beat2_why4(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("Why 4 Needs Only Two Digits", 23,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, ROW_Y, 0]))
            num, tiles = digit_tiles("76532", size=27)
            num.move_to(np.array([BOARD_CX, 2.02, 0]))
            split = chalk_math(r"76532 = 76500 + 32", size=28, color=CHALK_YELLOW
                               ).move_to(np.array([BOARD_CX, 1.22, 0]))
            hundred = chalk_math(r"76500 = 765 \times 100"
                                 r"\qquad 100 \div 4 = 25", size=24,
                                 color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, 0.54, 0]))
            note = board_text("the first part is already divisible by 4", 16,
                              CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -0.12, 0]))
            # One row rather than two: the banner lift left no room for a
            # separate "32 / 4 = 8" line above a boxed verdict, so the last
            # division and the verdict share the closing row.
            tail = VGroup(
                chalk_math(r"32 \div 4 = 8", size=26, color=CHALK_YELLOW),
                board_text("so 76532 is divisible by 4", 18, CHALK_GREEN,
                           "BOLD"),
            ).arrange(RIGHT, buff=0.42).move_to(
                np.array([BOARD_CX, -0.86, 0]))
            strip = board_text("For 4  \u2192  the last 2 digits.", 16,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))
            result_box = SurroundingRectangle(tail, color=CHALK_GREEN,
                                              buff=0.16, corner_radius=0.10,
                                              stroke_width=2.4)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(num), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(split, shift=UP * 0.08), run_time=0.5)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(hundred, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(note, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(tail, shift=UP * 0.08), Create(result_box),
                      run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, result_box, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: apply the rule -- 56496 ------------------------------------
    def beat3_apply4(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()

            heading = board_text("Last 2 Digits", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            num, tiles = digit_tiles("56496", size=29)
            num.move_to(np.array([BOARD_CX, 1.98, 0]))
            lens = digit_lens(tiles, 2)
            faded = dim_outside(tiles, 2)
            working = chalk_math(r"96 = 4 \times 24", size=28, color=CHALK_YELLOW
                                 ).move_to(np.array([BOARD_CX, 0.98, 0]))
            tick = mark_yes(1.05).move_to(
                np.array([BOARD_CX - 1.62, 0.34, 0]))
            rule_card = rule_line("DIVISIBILITY BY 4", "test the last two digits",
                                  CHALK_CYAN, width=7.0, size=18).move_to(
                np.array([BOARD_CX, -1.14, 0]))
            strip = board_text("Works for numbers greater than 100.", 16,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(num), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(lens), faded.animate.set_opacity(0.22),
                      run_time=0.6)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(working, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(tick, scale=0.6), run_time=0.3)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            result = board_text("56496 is divisible by 4", 18, CHALK_GREEN,
                                "BOLD").move_to(
                np.array([BOARD_CX, -0.34, 0]))
            result_box = SurroundingRectangle(result, color=CHALK_GREEN,
                                              buff=0.18, corner_radius=0.10,
                                              stroke_width=2.4)
            self.play(FadeIn(result, shift=UP * 0.08), Create(result_box),
                      run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(rule_card, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, rule_card, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: why 8 needs three digits -----------------------------------
    def beat4_why8(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()

            heading = board_text("Why 8 Needs Three Digits", 23, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            hundred = VGroup(
                badge_card("100", CHALK_PINK, size=22, width=1.10, height=0.56),
                mark_no(0.95),
                badge_card("1000 = 8 \u00d7 125", CHALK_GREEN, size=20,
                           width=2.60, height=0.56),
                mark_yes(0.95),
            ).arrange(RIGHT, buff=0.24).move_to(
                np.array([BOARD_CX, 2.02, 0]))

            num, tiles = digit_tiles("93624", size=27)
            num.move_to(np.array([BOARD_CX, 1.24, 0]))
            split = chalk_math(r"93624 = 93000 + 624", size=26,
                               color=CHALK_YELLOW).move_to(
                np.array([BOARD_CX, 0.50, 0]))
            note = board_text("93000 is a multiple of 1000, so it is already "
                              "divisible by 8", 15, CHALK_GREEN, "BOLD"
                              ).move_to(np.array([BOARD_CX, -0.20, 0]))
            result = board_text("624 = 8 \u00d7 78, so 93624 is divisible by 8",
                                17, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -1.02, 0]))
            result_box = SurroundingRectangle(result, color=CHALK_GREEN,
                                              buff=0.18, corner_radius=0.10,
                                              stroke_width=2.4)
            strip = board_text("For 8  \u2192  the last 3 digits.", 16,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(hundred), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(num), run_time=0.4)
            self.play(FadeIn(split, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(note, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(result, shift=UP * 0.08), Create(result_box),
                      run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, result_box, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: two lenses, two different widths ---------------------------
    def beat5_two_lenses(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            self.reset_board()

            heading = board_text("Don't Mix the Two", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            num, tiles = digit_tiles("2104", size=29)
            num.move_to(np.array([BOARD_CX, 1.90, 0]))
            lens_two = digit_lens(tiles, 2, CHALK_CYAN)
            lens_three = digit_lens(tiles, 3, CHALK_PINK)

            four_line = board_text("for 4: last two \u2192 04 = 4", 17,
                                   CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX, 1.02, 0]))
            eight_line = board_text("for 8: last three \u2192 104 = 8 \u00d7 13",
                                    17, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, 0.30, 0]))
            memory = board_text("4 \u2192 TWO digits          8 \u2192 THREE digits",
                                22, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -0.66, 0]))
            strip = board_text("4 looks at two digits; 8 looks at three.", 16,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(num), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(lens_two), run_time=0.4)
            self.play(FadeIn(four_line, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(ReplacementTransform(lens_two, lens_three), run_time=0.5)
            self.play(FadeIn(eight_line, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(memory, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, memory)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: divisibility by 11 -- 1221 ---------------------------------
    def beat6_rule11(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("Divisibility by 11", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            num, tiles = digit_tiles("1221", size=29)
            num.move_to(np.array([BOARD_CX - 0.55, 2.02, 0]))
            tags = place_tags(tiles, color=CHALK_CYAN, size=11, y_shift=-0.46)
            start = board_text("start from the right  \u2190", 14, CHALK_YELLOW,
                               "BOLD").move_to(np.array([3.55, 2.02, 0]))

            odd = basket("odd places", "1 + 2", 3, CHALK_CYAN, width=3.4
                         ).move_to(np.array([LEFT_X, 0.50, 0]))
            even = basket("even places", "2 + 1", 3, CHALK_PINK, width=3.4
                          ).move_to(np.array([RIGHT_X, 0.50, 0]))
            diff = chalk_math(r"3 - 3 = 0", size=30, color=CHALK_YELLOW
                              ).move_to(np.array([BOARD_CX, -0.62, 0]))
            result = board_text("1221 is divisible by 11", 18, CHALK_GREEN,
                                "BOLD").move_to(
                np.array([BOARD_CX, -1.16, 0]))
            result_box = SurroundingRectangle(result, color=CHALK_GREEN,
                                              buff=0.14, corner_radius=0.10,
                                              stroke_width=2.4)
            strip = board_text("Alternate  \u2192  Add  \u2192  Compare.", 16,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(num), run_time=0.4)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(t, scale=0.7) for t in tags],
                                  lag_ratio=0.18), run_time=0.7)
            self.play(FadeIn(start), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(odd, shift=UP * 0.10), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(even, shift=UP * 0.10), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(diff, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(result, shift=UP * 0.08), Create(result_box),
                      run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, result_box, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: the same test failing -- 6535 ------------------------------
    def beat7_11_fails(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("When the Test Fails", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            num, tiles = digit_tiles("6535", size=29)
            num.move_to(np.array([BOARD_CX - 0.55, 2.02, 0]))
            tags = place_tags(tiles, color=CHALK_CYAN, size=11, y_shift=-0.46)

            odd = basket("odd places", "5 + 5", 10, CHALK_CYAN, width=3.4
                         ).move_to(np.array([LEFT_X, 0.50, 0]))
            even = basket("even places", "3 + 6", 9, CHALK_PINK, width=3.4
                          ).move_to(np.array([RIGHT_X, 0.50, 0]))
            diff = chalk_math(r"10 - 9 = 1", size=30, color=CHALK_YELLOW
                              ).move_to(np.array([BOARD_CX, -0.62, 0]))
            result = board_text("6535 is not divisible by 11", 18, CHALK_PINK,
                                "BOLD").move_to(
                np.array([BOARD_CX, -1.16, 0]))
            result_box = SurroundingRectangle(result, color=CHALK_PINK,
                                              buff=0.14, corner_radius=0.10,
                                              stroke_width=2.4)
            strip = VGroup(
                board_text("1221 \u2192 0", 17, CHALK_WHITE, "BOLD"),
                mark_yes(0.85),
                board_text("6535 \u2192 1", 17, CHALK_WHITE, "BOLD"),
                mark_no(0.85),
            ).arrange(RIGHT, buff=0.30).move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(num), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(t, scale=0.7) for t in tags],
                                  lag_ratio=0.18), run_time=0.7)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(odd), FadeIn(even), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(diff, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(result, shift=UP * 0.08), Create(result_box),
                      run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, result_box, color=CHALK_PINK)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: three rules, three clues -----------------------------------
    def beat8_dashboard(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("Three Advanced Rules, Three Clues", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, ROW_Y, 0]))
            panels = VGroup(
                zone_panel("\u00f74  LAST 2 DIGITS",
                           ["56496 \u2192 96", "96 = 4 \u00d7 24"],
                           CHALK_CYAN, size=14),
                zone_panel("\u00f78  LAST 3 DIGITS",
                           ["93624 \u2192 624", "624 = 8 \u00d7 78"],
                           CHALK_GREEN, size=14),
                zone_panel("\u00f711  ALTERNATING SUMS",
                           ["1221 \u2192 3 and 3", "3 - 3 = 0"],
                           CHALK_PINK, size=14),
            ).arrange(RIGHT, buff=0.30).move_to(
                np.array([BOARD_CX, 0.90, 0]))
            memory = board_text("4 \u2192 2 digits     8 \u2192 3 digits     "
                                "11 \u2192 2 alternating groups", 18,
                                CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -0.86, 0]))
            strip = board_text("Three clues instead of three tricks.", 16,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(panels[0], shift=UP * 0.10), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(panels[1], shift=UP * 0.10), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(panels[2], shift=UP * 0.10), run_time=0.55)
            self.play(FadeIn(memory, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, memory)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8b: the rule doing real work -- 56496 seats -------------------
    # The audit's second note: a 10-15 s real-world application before "Your
    # Turn", so the three tests are shown deciding something a viewer cares
    # about.  The textbook's own 56496 carries it.
    def beat_apply(self) -> None:
        with self.voiceover(text=NARRATION["apply"]) as tracker:
            self.reset_board()

            heading = board_text("Real Seats, Real Boxes", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            num, tiles = digit_tiles("56496", size=28)
            num.move_to(np.array([BOARD_CX, 1.86, 0]))
            lens = digit_lens(tiles, 2, CHALK_CYAN)
            box_row = VGroup(
                board_text("boxes of four seats", 15, CHALK_WHITE, "BOLD"),
                *[badge_card("4", CHALK_CYAN, size=18, width=0.56, height=0.50)
                  for _ in range(4)],
            ).arrange(RIGHT, buff=0.24).move_to(
                np.array([BOARD_CX, 1.00, 0]))
            work = chalk_math(r"96 \div 4 = 24", size=28, color=CHALK_YELLOW
                              ).move_to(np.array([BOARD_CX, 0.28, 0]))
            result = board_text("so 56496 divides by four", 18, CHALK_GREEN,
                                "BOLD").move_to(
                np.array([BOARD_CX, -0.30, 0]))
            result_box = SurroundingRectangle(result, color=CHALK_GREEN,
                                              buff=0.15, corner_radius=0.10,
                                              stroke_width=2.4)
            call = verdict(True, "no seat is left over", size=16).move_to(
                np.array([BOARD_CX, -1.05, 0]))
            strip = board_text("The rule decides before the boxes are packed.",
                               16, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(num), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(box_row, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(lens), run_time=0.45)
            self.play(FadeIn(work, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(result, shift=UP * 0.08), Create(result_box),
                      run_time=0.5)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(call, scale=0.85), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, call, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # The audit called the old single-window challenge "cramped": two six-digit
    # numbers, five checks and two verdicts on the board at once.  It is now
    # staged sequentially -- the 4 and 8 work on the left, then it clears, then
    # the centred 11 check in larger type.
    def beat9_challenge(self) -> None:
        with self.voiceover(text=NARRATION["scene9"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", 26, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, 2.62, 0]))
            sub = board_text("Choose the rule before you calculate.", 17,
                             CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, 2.10, 0]))

            # --- first number: 4 and 8, worked on the left -------------------
            a_num, a_tiles = digit_tiles("726352", size=25)
            a_num.move_to(np.array([LEFT_X - 0.15, 1.58, 0]))
            a_four = VGroup(
                board_text("last two: 52 = 4 \u00d7 13", 15, CHALK_CYAN,
                           "BOLD"), mark_yes(0.85),
            ).arrange(RIGHT, buff=0.18).move_to(
                np.array([LEFT_X - 0.15, 0.94, 0]))
            a_eight = VGroup(
                board_text("last three: 352 = 8 \u00d7 44", 15, CHALK_GREEN,
                           "BOLD"), mark_yes(0.85),
            ).arrange(RIGHT, buff=0.18).move_to(
                np.array([LEFT_X - 0.15, 0.44, 0]))
            answer_a = board_text("726352 is divisible by 4 and by 8.", 17,
                                  CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -0.72, 0]))
            answer_a_box = SurroundingRectangle(answer_a, color=CHALK_GREEN,
                                                buff=0.16, corner_radius=0.10,
                                                stroke_width=2.4)
            group_a = VGroup(a_num, a_four, a_eight, answer_a, answer_a_box)

            # --- second number: 11, centred, larger type ---------------------
            b_num, b_tiles = digit_tiles("10824", size=32)
            b_num.move_to(np.array([BOARD_CX, 1.48, 0]))
            b_odd = board_text("odd places:  4 + 8 + 1 = 13", 20, CHALK_CYAN,
                               "BOLD").move_to(
                np.array([BOARD_CX - 1.95, 0.62, 0]))
            b_even = board_text("even places:  2 + 0 = 2", 20, CHALK_PINK,
                                "BOLD").move_to(
                np.array([BOARD_CX + 2.26, 0.62, 0]))
            b_diff = VGroup(
                chalk_math(r"13 - 2 = 11", size=30, color=CHALK_YELLOW),
                mark_yes(1.0),
            ).arrange(RIGHT, buff=0.26).move_to(
                np.array([BOARD_CX, -0.25, 0]))
            answer_b = board_text("10824 is divisible by 11.", 19, CHALK_PINK,
                                  "BOLD").move_to(
                np.array([BOARD_CX, -1.05, 0]))
            answer_b_box = SurroundingRectangle(answer_b, color=CHALK_PINK,
                                                buff=0.16, corner_radius=0.10,
                                                stroke_width=2.4)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(sub), run_time=0.4)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(a_num, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            # the shared THINK clock, centred on the board (story_common)
            play_challenge_countdown(self, seconds=4, sfx=self.sfx,
                                     position=np.array([BOARD_CX, BOARD_CY, 0]))

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(a_four, shift=UP * 0.08),
                      FadeIn(a_eight, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(answer_a, shift=UP * 0.08), Create(answer_a_box),
                      run_time=0.5)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeOut(group_a), run_time=0.4)
            self.play(FadeIn(b_num, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(b_odd, shift=UP * 0.08),
                      FadeIn(b_even, shift=UP * 0.08), run_time=0.7)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(b_diff, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(answer_b, shift=UP * 0.08), Create(answer_b_box),
                      run_time=0.5)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, answer_b_box, color=CHALK_PINK)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap and thank-you ---------------------------------------
    def beat10_recap(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("Advanced Divisibility Rules", 24,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, ROW_Y, 0]))
            rows = VGroup(
                rule_line("4", "last 2 digits   (564 | 96)", CHALK_CYAN,
                          width=8.6, size=19),
                rule_line("8", "last 3 digits   (93 | 624)", CHALK_GREEN,
                          width=8.6, size=19),
                rule_line("11", "alternating sums   (1221: 3 - 3 = 0)",
                          CHALK_PINK, width=8.6, size=19),
            ).arrange(DOWN, buff=0.24, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX, 1.24, 0]))
            examples = VGroup(
                VGroup(board_text("96 \u00f7 4", 18, CHALK_WHITE, "BOLD"),
                       mark_yes(0.9)).arrange(RIGHT, buff=0.20),
                VGroup(board_text("624 \u00f7 8", 18, CHALK_WHITE, "BOLD"),
                       mark_yes(0.9)).arrange(RIGHT, buff=0.20),
                VGroup(board_text("1221 \u2192 0", 18, CHALK_WHITE, "BOLD"),
                       mark_yes(0.9)).arrange(RIGHT, buff=0.20),
            ).arrange(RIGHT, buff=0.62).move_to(
                np.array([BOARD_CX, -0.52, 0]))
            message = board_text("ZOOM.  ZOOM MORE.  ALTERNATE.", 23,
                                 CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.12, 0]))
            promise = board_text("Test divisibility without dividing the whole "
                                 "number.", 16, CHALK_WHITE, "BOLD").move_to(
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
            self.play(FadeOut(board_group), run_time=0.5)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.5)
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.play(Indicate(thanks, color=CHALK_YELLOW, scale_factor=1.03),
                      run_time=rt(tracker.get_remaining_duration()))
            self._capture_srt(tracker)

        self.wait(END_HOLD)

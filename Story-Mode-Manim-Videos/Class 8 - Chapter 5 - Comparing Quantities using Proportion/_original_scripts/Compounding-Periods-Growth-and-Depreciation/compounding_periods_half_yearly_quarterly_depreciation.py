"""
Compounding Half-Yearly, Quarterly & Applications to Population Growth and
Depreciation
Story-mode chalkboard lesson (Class 8 Maths, Chapter 5: Comparing Quantities
using Proportion, Storymode 04).

LLM KEY / FUNCTION NAME: compounding_periods_half_yearly_quarterly_depreciation

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

The defining visual is the COMPOUNDING CLOCK: one one-year dial that physically
splits into two six-month sectors and then into four quarter sectors, while the
rate card splits with it (R -> R/2 -> R/4) and the period counter moves
(n -> 2n -> 4n).  The same P(1 + r)^n structure then drives a rising village and
a shrinking value bar with a ball that loses height at every bounce.

Title + 11 scenes (thirteen pieces):
  0. Title card: the lesson's four parts, chalked on a bare board.
  1. The conversion period: the interval after which interest is added.
  2. The half-yearly rule: the rate halves AND the periods double together.
  3. The worked example: 1000(1.05)^2 = Rs 1,102.50, CI = Rs 102.50.
  4. Quarterly: R/4 and 4n, the same rule extended to four periods.
  5. Population growth: the new total is the next period's base.
  6. Depreciation: (100 - R)% is kept, and the bouncing ball.
  7. One structure, three uses: growth up, depreciation down.
  8. The five-step decision map.
  9. Your turn: half-yearly, quarterly, depreciation and the quick check after
     the series' centred ten-second THINK clock.
 10. The summary: the three conversion periods, the two mixed formulas and the
     five steps gathered on one board.
 11. Recap: period, rate, factor, repeat -- and the spoken thank-you card.
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


# (this section is spliced into a head whose own imports omit Arc, Ellipse and
#  Sector; Dot, Circle, Line, DashedLine, Rectangle, Polygon, RoundedRectangle,
#  Square, Arrow, VGroup, UP, DOWN, LEFT, RIGHT, DEGREES, TAU, PI and np are
#  already imported by the head)
from manim import Arc, Ellipse, Sector  # noqa: E402,F401

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

# The two content bands.  Cards are 0.94 tall, so their TEXT boxes stay at least
# 0.25 units apart vertically at these centres -- the audits measure text.
BAND_A = 0.70            # the upper band (the working, the formula cards)
BAND_B = -0.50           # the lower band (the result of the upper band)

PANEL_FILL = "#16202B"
CARD_W = 3.30            # the standard card width
CARD_H = 0.94            # the standard card height
CHIP_H = 0.50
MARK_SIZE = 18           # ONE letter size for every labelled figure
CLOCK_R = 0.85           # the compounding dial's radius
CLOCK_FILL = "#0E1A14"
PLOT_COLORS = (CHALK_GREEN, CHALK_CYAN, CHALK_AMBER, CHALK_PINK)

# The figures this video works with.  The textbook's own numbers: Rs 1,000 at
# 10% p.a. compounded half-yearly, a village of 6,250 growing 8% a year, a ball
# dropped from 25 m losing 10% at each bounce, and the challenge amounts.
PRINCIPAL = 1000
RATE_PA = 10
AMOUNT_HALF = 1102.50
CI_HALF = 102.50
VILLAGE0 = 6250
GROWTH_PC = 8
VILLAGE2 = 7290
BALL_H0 = 25
BALL_H2 = 20.25
TV_PRICE = 21000
CHALLENGE_A = "Rs 13,891.50"


# ---------------------------------------------------------------- furniture --
def write_text_long(path, text: str) -> None:
    """Write a text file, through the extended-length path when needed.

    This topic's media paths -- `...\\media\\videos\\
    compounding_periods_half_yearly_quarterly_depreciation\\360p30\\<Class>.real.srt`
    -- run past the 260-character MAX_PATH limit, which is why the chapter
    pipeline renders into the short `D:\\m3` media dir and copies the result back
    here.  The copy-back and this ground-truth SRT write therefore fall back to
    the ``\\\\?\\`` extended form when the plain path is too long for the OS.
    """
    try:
        Path(path).write_text(text, encoding="utf-8")
    except OSError:
        with open("\\\\?\\" + str(Path(path).resolve()), "w",
                  encoding="utf-8") as fh:
            fh.write(text)


def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


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


def chip(text, color=CHALK_CYAN, size=14, width=None, height=CHIP_H,
         fill=PANEL_FILL):
    """A small labelled chip.  Its box is cut to its own label, so the lettering
    can never spill outside the panel (the audit measures that overflow)."""
    lab = board_text(text, size, color, "BOLD")
    box = RoundedRectangle(corner_radius=0.09,
                           width=width or (lab.width + 0.40), height=height,
                           stroke_color=color, stroke_width=1.7,
                           fill_color=fill, fill_opacity=0.7)
    lab.move_to(box.get_center())
    grp = VGroup(box, lab)
    grp.box, grp.label = box, lab
    return grp


def note_card(head, lines, color=CHALK_CYAN, width=None, head_size=15,
              line_size=13, gap=0.28, buff=0.24, pad=0.44):
    """A card with a bold head line and one or two body lines under it.

    Head and body are held `gap` apart and the box is cut to the finished
    content, so the pair passes both the clearance audit (which flags any two
    texts closer than 0.22) and the overflow check (a fixed box height once let
    a two-line body hang out of its card).
    """
    h = board_text(head, head_size, color, "BOLD")
    body = VGroup(*[board_text(line, line_size, CHALK_WHITE, "BOLD")
                    for line in lines]).arrange(DOWN, buff=buff)
    content = VGroup(h, body).arrange(DOWN, buff=gap)
    box = panel(width or (content.width + pad), content.height + pad, color)
    content.move_to(box.get_center())
    grp = VGroup(box, content)
    grp.box, grp.head, grp.body = box, h, body
    return grp


def coin_stack(cx, cy, n=3, scale=1.0, color=CHALK_YELLOW):
    """A stack of rupee coins: filled discs WITH THICKNESS, drawn bottom-up.

    Each coin is a dark milled edge under a bright face, so the stack reads as
    real metal on the board rather than as a flat outline.
    """
    discs = VGroup()
    for i in range(n):
        y = cy + 0.072 * i * scale
        edge = Ellipse(width=0.44 * scale, height=0.16 * scale, stroke_width=0,
                       fill_color="#8A6A18", fill_opacity=0.85)
        edge.move_to(np.array([cx, y - 0.030 * scale, 0.0]))
        face = Ellipse(width=0.44 * scale, height=0.16 * scale,
                       stroke_color=color, stroke_width=1.5,
                       fill_color=color, fill_opacity=0.45)
        face.move_to(np.array([cx, y, 0.0]))
        discs.add(edge, face)
    return discs


def note_stack(cx, cy, n=3, text="Rs 1000", size=12, color=CHALK_YELLOW):
    """A bundle of drawn rupee notes: filled rectangles fanned out, top labelled.

    The rectangles are cut to the label plus 0.22 of chalk margin on every side
    (a `Rectangle` is a `Polygon` to the audit, which samples its perimeter
    against lettering).
    """
    lab = board_text(text, size, color, "BOLD")
    w = lab.width + 0.44
    h = max(lab.height + 0.24, 0.40)
    grp = VGroup()
    for i in range(n):
        b = Rectangle(width=w, height=h, stroke_color=color, stroke_width=1.5,
                      fill_color=color, fill_opacity=0.18)
        b.move_to(np.array([cx - 0.045 * (n - 1 - i),
                            cy - 0.050 * (n - 1 - i), 0.0]))
        grp.add(b)
    lab.move_to(grp[-1].get_center())
    grp.add(lab)
    grp.label = lab
    return grp


def clock_face(cx, cy, r=CLOCK_R, color=CHALK_CYAN):
    """The one-year dial: a filled face with a chalk rim and twelve ticks.

    The ticks stay in the outer tenth of the dial, clear of the words chalked
    at its centre (a tick crossing the middle of the dial ran through the
    period label).
    """
    rim = Circle(radius=r, stroke_color=color, stroke_width=2.6,
                 fill_color=CLOCK_FILL, fill_opacity=0.55)
    rim.move_to(np.array([cx, cy, 0.0]))
    ticks = VGroup()
    for k in range(12):
        a = (90 - 30 * k) * DEGREES
        d = np.array([np.cos(a), np.sin(a), 0.0])
        p = np.array([cx, cy, 0.0])
        ticks.add(Line(p + d * r * 0.90, p + d * r * 0.99,
                       stroke_color=color, stroke_width=1.3))
    return VGroup(rim, ticks)


def clock_sectors(cx, cy, n, r=CLOCK_R, colors=PLOT_COLORS):
    """The dial's fill, cut into `n` equal pie sectors.

    n = 1 is the whole year, n = 2 is two half-years and n = 4 is four
    quarters.  Each piece is a *filled* sector with its own chalk rim, so the
    same object is seen to split rather than being redrawn.
    """
    c = np.array([cx, cy, 0.0])
    grp = VGroup()
    for k in range(n):
        col = colors[k % len(colors)]
        grp.add(Sector(radius=r * 0.93,
                       start_angle=90 * DEGREES - k * TAU / n,
                       angle=TAU / n, arc_center=c,
                       stroke_color=col, stroke_width=1.8,
                       fill_color=col, fill_opacity=0.26))
    return grp


def dial_label(cx, cy, text, color=CHALK_WHITE, size=13):
    """The words chalked inside the dial (1 YEAR, HALF-YEARLY, QUARTERLY).

    Kept short and small: the widest label must stay inside the ring of ticks.
    """
    return board_text(text, size, color, "BOLD").move_to(
        np.array([cx, cy, 0.0]))


def rate_card(sym, color=CHALK_AMBER, size=24, width=1.46, height=0.62):
    """The rate the dial carries -- a maths object in its own chalk box."""
    tex = chalk_math(sym, size=size, color=color)
    box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                           stroke_color=color, stroke_width=2.0,
                           fill_color=PANEL_FILL, fill_opacity=0.65)
    tex.move_to(box.get_center())
    grp = VGroup(box, tex)
    grp.box, grp.tex = box, tex
    return grp


def person_icon(cx, cy, color=CHALK_CYAN, scale=1.0):
    """A small filled figure: a round head over a pair of shoulders."""
    head = Circle(radius=0.10 * scale, stroke_width=0,
                  fill_color=color, fill_opacity=0.9)
    head.move_to(np.array([cx, cy + 0.15 * scale, 0.0]))
    body = Ellipse(width=0.38 * scale, height=0.26 * scale, stroke_width=0,
                   fill_color=color, fill_opacity=0.5)
    body.move_to(np.array([cx, cy - 0.10 * scale, 0.0]))
    return VGroup(body, head)


def house(cx, cy, s=1.0, color=CHALK_AMBER):
    """A drawn house: a filled wall, a pitched roof and a doorway."""
    body = Rectangle(width=0.46 * s, height=0.34 * s, stroke_color=color,
                     stroke_width=1.5, fill_color=color, fill_opacity=0.40)
    body.move_to(np.array([cx, cy - 0.07 * s, 0.0]))
    roof = Polygon(np.array([cx - 0.30 * s, cy + 0.10 * s, 0.0]),
                   np.array([cx + 0.30 * s, cy + 0.10 * s, 0.0]),
                   np.array([cx, cy + 0.34 * s, 0.0]),
                   stroke_color=CHALK_PINK, stroke_width=1.5,
                   fill_color=CHALK_PINK, fill_opacity=0.42)
    door = Rectangle(width=0.12 * s, height=0.17 * s, stroke_width=0,
                     fill_color=PANEL_FILL, fill_opacity=0.9)
    door.move_to(np.array([cx, cy - 0.16 * s, 0.0]))
    return VGroup(body, roof, door)


def village(cx, cy, color=CHALK_AMBER, s=1.15):
    """A drawn village: three houses and their people -- the population that
    grows.  Walls, pitched roofs, doorways and round heads over shoulders are
    all filled shapes, so nothing here reads as a bare outline."""
    grp = VGroup()
    for k, dx in enumerate((-0.62, 0.0, 0.62)):
        size = s if k == 1 else s * 0.84
        grp.add(house(cx + dx, cy + (0.06 if k == 1 else 0.0), size, color))
    for dx in (-0.46, 0.02, 0.50, 0.80):
        grp.add(person_icon(cx + dx, cy - 0.46 * s, CHALK_CYAN, 0.95))
    return grp


def car_icon(cx, cy, s=1.0, color=CHALK_PINK):
    """A drawn car: a filled body, a cabin and two solid wheels."""
    body = RoundedRectangle(corner_radius=0.06, width=0.86 * s,
                            height=0.24 * s, stroke_color=color,
                            stroke_width=1.8, fill_color=color,
                            fill_opacity=0.34)
    body.move_to(np.array([cx, cy, 0.0]))
    cabin = RoundedRectangle(corner_radius=0.05, width=0.44 * s,
                             height=0.20 * s, stroke_color=color,
                             stroke_width=1.6, fill_color=color,
                             fill_opacity=0.26)
    cabin.move_to(np.array([cx - 0.04 * s, cy + 0.20 * s, 0.0]))
    wheels = VGroup()
    for dx in (-0.26 * s, 0.26 * s):
        wheels.add(Circle(radius=0.085 * s, stroke_width=0,
                          fill_color="#1B2733", fill_opacity=1.0).move_to(
            np.array([cx + dx, cy - 0.14 * s, 0.0])))
    return VGroup(body, cabin, wheels)


def tv_icon(cx, cy, s=1.0, color=CHALK_CYAN):
    """A drawn television: a filled screen on a narrow stand."""
    screen = RoundedRectangle(corner_radius=0.05, width=0.74 * s,
                              height=0.54 * s, stroke_color=color,
                              stroke_width=2.0, fill_color=color,
                              fill_opacity=0.28)
    screen.move_to(np.array([cx, cy + 0.10 * s, 0.0]))
    neck = Rectangle(width=0.16 * s, height=0.10 * s, stroke_width=0,
                     fill_color=color, fill_opacity=0.55)
    neck.move_to(np.array([cx, cy - 0.22 * s, 0.0]))
    foot = Rectangle(width=0.50 * s, height=0.06 * s, stroke_width=0,
                     fill_color=color, fill_opacity=0.45)
    foot.move_to(np.array([cx, cy - 0.30 * s, 0.0]))
    return VGroup(screen, neck, foot)


def value_bar(cx, cy, w=1.60, h=0.66, frac=1.0, color=CHALK_GREEN,
              label="100%"):
    """A value drawn as a filled bar: what is left after each depreciation.

    The bar and its label are ONE board object, so the label is never read as
    chalk sitting inside somebody else's filled box.
    """
    frame = Rectangle(width=w, height=h, stroke_color=CHALK_WHITE,
                      stroke_width=1.6, fill_color=PANEL_FILL,
                      fill_opacity=0.5)
    frame.move_to(np.array([cx, cy, 0.0]))
    fw = max(w * frac, 0.03)
    fill = Rectangle(width=fw, height=h - 0.08, stroke_width=0,
                     fill_color=color, fill_opacity=0.45)
    fill.move_to(np.array([cx - w / 2.0 + fw / 2.0, cy, 0.0]))
    lab = board_text(label, 13, color, "BOLD").move_to(np.array([cx, cy, 0.0]))
    grp = VGroup(frame, fill, lab)
    grp.frame, grp.fill, grp.label = frame, fill, lab
    return grp


def bounce_arc(p1, p2, peak, color=CHALK_WHITE, width=2.0):
    """One bounce: the arc a ball traces between two touches of the ground."""
    a = abs(p2[0] - p1[0]) / 2.0
    s = max(peak, 1e-3)
    radius = (a * a + s * s) / (2.0 * s)
    mx = (p1[0] + p2[0]) / 2.0
    cy = p1[1] - (radius - s)
    start = np.degrees(np.arctan2(p1[1] - cy, p1[0] - mx))
    ang = np.degrees(2.0 * np.arcsin(min(a / radius, 1.0)))
    return Arc(radius=radius, start_angle=start * DEGREES,
               angle=ang * DEGREES, arc_center=np.array([mx, cy, 0.0]),
               color=color, stroke_width=width)


def ball_icon(cx, cy, r=0.14, color=CHALK_PINK):
    """The ball itself: a filled disc with a highlight."""
    body = Circle(radius=r, stroke_width=0, fill_color=color,
                  fill_opacity=0.85).move_to(np.array([cx, cy, 0.0]))
    gloss = Circle(radius=r * 0.34, stroke_width=0, fill_color=CHALK_WHITE,
                   fill_opacity=0.45).move_to(
        np.array([cx - r * 0.30, cy + r * 0.30, 0.0]))
    return VGroup(body, gloss)


def bounce_track(cx, cy, h0=0.85, drop=0.9, width=1.90, color=CHALK_WHITE,
                 marker=CHALK_AMBER):
    """The textbook's bouncing ball, with all THREE HEIGHTS DRAWN.

    `cy` is the ground line, `h0` the release height (25 m).  The ball falls
    and each bounce rises to `drop` of the previous height: 22.5 m, then
    20.25 m.  The drop is a dashed vertical and every one of the three heights
    carries its own dashed level marker, so the decreasing heights are measured
    on the board instead of merely being asserted in words.  The marker lines
    are short, so they can never run into a label or the ball.
    """
    x0 = cx - width / 2.0                     # where the ball is released
    h1, h2 = h0 * drop, h0 * drop * drop
    w1, w2 = width * 0.52, width * 0.48
    p1 = (x0 + w1, cy)
    p2 = (p1[0] + w2, cy)

    ground = Line(np.array([x0 - 0.16, cy, 0.0]),
                  np.array([p2[0] + 0.16, cy, 0.0]),
                  stroke_color=color, stroke_width=1.8)
    fall = DashedLine(np.array([x0, cy, 0.0]), np.array([x0, cy + h0, 0.0]),
                      color=color, stroke_width=1.4, dash_length=0.07)
    grp = VGroup(ground, fall)
    for xa, xb, h in ((x0 + 0.20, x0 + 0.80, h0),
                      (p1[0] - 0.30, p1[0] + 0.30, h1),
                      (p2[0] - 0.34, p2[0] + 0.10, h2)):
        grp.add(DashedLine(np.array([xa, cy + h, 0.0]),
                           np.array([xb, cy + h, 0.0]),
                           color=marker, stroke_width=1.3, dash_length=0.07))
    grp.add(bounce_arc((x0, cy), p1, h1, color))
    grp.add(bounce_arc(p1, p2, h2, color))
    grp.add(ball_icon(x0, cy + h0))
    grp.ground, grp.heights = ground, (h0, h1, h2)
    return grp


def meter(cx, cy, up=1.0, down=1.0, w=0.32):
    """Growth against depreciation: one bar up, one bar down, one baseline."""
    base = Line(np.array([cx - 0.60, cy, 0.0]), np.array([cx + 0.60, cy, 0.0]),
                stroke_color=CHALK_WHITE, stroke_width=2.0)
    upbar = Rectangle(width=w, height=0.46 * up, stroke_width=0,
                      fill_color=CHALK_GREEN, fill_opacity=0.5)
    upbar.move_to(np.array([cx - 0.32, cy + 0.23 * up, 0.0]))
    dnbar = Rectangle(width=w, height=0.46 * down, stroke_width=0,
                      fill_color=CHALK_PINK, fill_opacity=0.5)
    dnbar.move_to(np.array([cx + 0.32, cy - 0.23 * down, 0.0]))
    up_lab = board_text("+", 16, CHALK_GREEN, "BOLD").move_to(
        np.array([cx - 0.32, cy + 0.46 * up + 0.16, 0.0]))
    dn_lab = board_text("-", 16, CHALK_PINK, "BOLD").move_to(
        np.array([cx + 0.32, cy - 0.46 * down - 0.16, 0.0]))
    up_grp = VGroup(base, upbar, up_lab)
    dn_grp = VGroup(dnbar, dn_lab)
    up_grp.label, dn_grp.label = up_lab, dn_lab
    return up_grp, dn_grp


def wrong_card(text, color=CHALK_RED, width=2.60, height=1.05, size=15):
    """A card holding a WRONG statement, with a drawn cross over it.

    The cross occupies the card's top half and the statement its bottom half, so
    the strike-through is unmistakable yet never comes within the 0.04 units the
    audit allows between a stroke and the lettering.  The whole card is ONE
    board object, so the strokes are never read as a line running into a box.
    """
    box = panel(width, height, color, opacity=0.7)
    cross = VGroup(
        Line(np.array([-width / 2 + 0.55, 0.14, 0.0]),
             np.array([-width / 2 + 1.05, 0.50, 0.0]),
             stroke_color=color, stroke_width=4.2),
        Line(np.array([-width / 2 + 0.55, 0.50, 0.0]),
             np.array([-width / 2 + 1.05, 0.14, 0.0]),
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
        "One thousand rupees at ten percent per annum. <bookmark mark='b0'/> "
        "Compounded every year, that money becomes one thousand one hundred "
        "rupees after one year. <bookmark mark='b1'/> But the same ten percent "
        "compounded half-yearly gives one thousand fifty rupees after six "
        "months, <bookmark mark='b2'/> and one thousand one hundred two rupees "
        "and fifty paise after a year. <bookmark mark='b3'/> Same money, same "
        "rate, more interest. <bookmark mark='b4'/> Why does the timing change "
        "the answer?"
    ),
    "s1": (
        "First, the conversion period. <bookmark mark='b0'/> The conversion "
        "period is the time interval after which the interest is added to the "
        "principal. <bookmark mark='b1'/> If interest is added once a year, the "
        "period is one full year: one turn of the clock. <bookmark mark='b2'/> "
        "If it is added every six months, that same year is cut into two equal "
        "periods. <bookmark mark='b3'/> And if it is added every three months, "
        "the year becomes four quarter periods. <bookmark mark='b4'/> So the "
        "conversion period fixes two things together, the rate for each period "
        "and how many periods there are."
    ),
    "s2": (
        "Now the half-yearly rule. <bookmark mark='b0'/> When the conversion "
        "period halves, two things change at the same time. <bookmark "
        "mark='b1'/> The rate for each period halves as well: R becomes R "
        "divided by two. <bookmark mark='b2'/> And the number of periods "
        "doubles: n becomes two n. <bookmark mark='b3'/> So the amount is P "
        "times one plus R over two hundred, all raised to two n. <bookmark "
        "mark='b4'/> Ten percent per annum compounded half-yearly means five "
        "percent for each half-year, <bookmark mark='b5'/> never ten percent "
        "every six months, and never change the exponent alone."
    ),
    "s3": (
        "Let us work it out. <bookmark mark='b0'/> Principal one thousand "
        "rupees, rate ten percent per annum, time one year, compounded "
        "half-yearly. <bookmark mark='b1'/> The rate for each half-year is ten "
        "divided by two, that is five percent. <bookmark mark='b2'/> And one "
        "year holds two half-yearly periods. <bookmark mark='b3'/> So the "
        "amount is one thousand times one point zero five squared, which is one "
        "thousand one hundred two rupees and fifty paise. <bookmark mark='b4'/> "
        "The compound interest is one thousand one hundred two point five minus "
        "one thousand, that is one hundred two rupees and fifty paise."
    ),
    "s4": (
        "A year has four quarters. <bookmark mark='b0'/> So when interest is "
        "compounded quarterly, the rate for one period becomes R divided by "
        "four, <bookmark mark='b1'/> and the number of periods becomes four n. "
        "<bookmark mark='b2'/> The amount is P times one plus R over four "
        "hundred, all raised to four n. <bookmark mark='b3'/> This is the same "
        "conversion-period rule, extended from two periods to four. <bookmark "
        "mark='b4'/> The rate and the number of periods always change together."
    ),
    "s5": (
        "The same structure answers questions about population. <bookmark "
        "mark='b0'/> A village has six thousand two hundred and fifty people, "
        "and the population grows by eight percent every year. <bookmark "
        "mark='b1'/> After one year the population is six thousand two hundred "
        "and fifty times one point zero eight, <bookmark mark='b2'/> and that "
        "new total becomes the base for the next year. <bookmark mark='b3'/> So "
        "after two years the population is six thousand two hundred and fifty "
        "times one point zero eight squared, which is seven thousand two "
        "hundred and ninety. <bookmark mark='b4'/> A repeated percentage "
        "increase is exactly the same structure as compound interest."
    ),
    "s6": (
        "Now depreciation, the mirror image. <bookmark mark='b0'/> Depreciation "
        "is a reduction in the value of an article due to use and age. "
        "<bookmark mark='b1'/> A quantity that loses R percent in each period "
        "keeps one hundred minus R percent. <bookmark mark='b2'/> Ten percent "
        "off leaves ninety percent, and the next reduction is taken from the "
        "new value. <bookmark mark='b3'/> So after two periods the value is P "
        "times zero point nine squared, and in general V is P times one minus R "
        "over one hundred, all raised to n. <bookmark mark='b4'/> A ball "
        "dropped from twenty five metres loses ten percent of its height at "
        "each bounce, so after two bounces it rises to twenty five times zero "
        "point nine squared, that is twenty point two five metres."
    ),
    "s7": (
        "One structure, three uses. <bookmark mark='b0'/> Money at compound "
        "interest and population growth both use P times one plus r, all raised "
        "to n. <bookmark mark='b1'/> Depreciation uses P times one minus r, "
        "raised to n. <bookmark mark='b2'/> A growth multiplier is greater than "
        "one, <bookmark mark='b3'/> and a depreciation multiplier is less than "
        "one. <bookmark mark='b4'/> So keep two decisions separate: how often "
        "the update happens, and whether the quantity rises or falls."
    ),
    "s8": (
        "Here is the decision map. <bookmark mark='b0'/> Step one: identify the "
        "conversion period. <bookmark mark='b1'/> Step two: find the rate for "
        "one period. <bookmark mark='b2'/> Step three: count the number of "
        "periods. <bookmark mark='b3'/> Step four: choose plus for growth, or "
        "minus for decrease. <bookmark mark='b4'/> Step five: apply that factor "
        "again and again. <bookmark mark='b5'/> Period, rate, factor, repeat: "
        "that is the whole method."
    ),
    "s9q": (
        "Your turn. Three questions. <bookmark mark='b0'/> First: twelve "
        "thousand rupees at ten percent per annum for one and a half years, "
        "compounded half-yearly. Find the amount. <bookmark mark='b1'/> Second: "
        "twelve percent per annum for two years, compounded quarterly. What is "
        "the rate for each period, and how many periods are there? <bookmark "
        "mark='b2'/> Third: a television costing twenty one thousand rupees "
        "depreciates by five percent in one year. What is it worth now? "
        "<bookmark mark='b3'/> And a quick check: for eight percent growth, "
        "which factor do you use, and for eight percent depreciation, which "
        "factor?"
    ),
    "s9a": (
        "Let us check. <bookmark mark='b0'/> For A, the rate is five percent per "
        "half-year and one and a half years is three periods, so the amount is "
        "twelve thousand times one point zero five cubed, that is thirteen "
        "thousand eight hundred ninety one rupees and fifty paise. <bookmark "
        "mark='b1'/> For B, twelve divided by four is three percent per "
        "quarter, and two years is eight quarters, so the amount is P times one "
        "point zero three raised to eight. <bookmark mark='b2'/> For C, five "
        "percent depreciation leaves ninety five percent, so twenty one "
        "thousand times zero point nine five is nineteen thousand nine hundred "
        "and fifty rupees. <bookmark mark='b3'/> And the quick check: for eight "
        "percent growth use one point zero eight, and for eight percent "
        "depreciation use zero point nine two, because one minus zero point "
        "zero eight is zero point nine two."
    ),
    "s10": (
        "Let us gather the whole lesson in one place. <bookmark mark='b0'/> The "
        "conversion period has three cases: annually, the rate is R and there "
        "are n periods; <bookmark mark='b1'/> half-yearly, the rate is R over "
        "two and the periods double to two n; <bookmark mark='b2'/> quarterly, "
        "the rate is R over four and the periods become four n. <bookmark "
        "mark='b3'/> Growth uses A equals P times one plus R over one hundred, "
        "all raised to n: that is compound interest and population. <bookmark "
        "mark='b4'/> Depreciation uses V equals P times one minus R over one "
        "hundred, all raised to n: the value keeps what is left. <bookmark "
        "mark='b5'/> And the five steps: identify the conversion period, find "
        "the rate for one period, count the number of periods, choose plus for "
        "growth or minus for decrease, and apply that factor again and again."
    ),
    "s11": (
        "One last look. <bookmark mark='b0'/> The compounding clock: annually, "
        "half-yearly, quarterly, with the rate and the number of periods "
        "changing together. <bookmark mark='b1'/> Growth uses P times one plus "
        "R over one hundred, all raised to n, <bookmark mark='b2'/> and "
        "depreciation uses P times one minus R over one hundred, raised to n. "
        "<bookmark mark='b3'/> Keep the two decisions separate: how often, and "
        "up or down. <bookmark mark='b4'/> Period, rate, factor, repeat. "
        "<bookmark mark='b5'/> Thank you for watching, <bookmark mark='b6'/> "
        "and see you in the next lesson."
    ),
}


class CompoundingPeriodsHalfYearlyQuarterlyDepreciationStory(VoiceoverScene):
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
        out_dir = _HERE / "media" / "videos" / "compounding_periods_half_yearly_quarterly_depreciation"
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
        write_text_long(srt_path, "\n".join(lines))
        print(f"[real SRT written] {srt_path}")
        write_text_long(out_dir / "real.srt", "\n".join(lines))
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
        self.beat_s11()

        self._write_real_srt()

    # ================================================================ beats ==
    # Compounding Half-Yearly, Quarterly & Applications to Population Growth
    # and Depreciation (Class 8 Maths, Chapter 5, Storymode 04).
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
    #   * two texts never come closer than the 0.22 units the clearance audit
    #     asks for, which is why every card cuts its own box to its content;
    #   * the compounding clock is the same furniture in every scene, and the
    #     SAME sector object is transformed from one period to two to four, so
    #     the dial is seen to split rather than being redrawn;
    #   * a drawn cross always lives in the same VGroup as the card it strikes
    #     through (otherwise the clearance audit reads the strokes as a line
    #     running into a box);
    #   * the challenge uses the series' shared 10-second THINK clock, dead
    #     centre of the board, and the question cards sit in the four corners so
    #     the badge never covers one.

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

    def q_card(self, title, pict, color=CHALK_CYAN, width=3.20, pad=0.12,
               title_size=13, buff=0.26):
        """One 'your turn' card: a prompt above its small worked figure."""
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

    def formula_block(self, head, tex, color, x, y, head_size=13, buff=0.32):
        """One labelled formula for the summary board: a bold head line over a
        full-height maths object.

        The 0.32 gap between the head and the formula is the room the exponent
        gets: the audit measures text boxes, so nothing may come closer than
        0.22 to the raised power (`\\frac` plus a full-size superscript, never a
        cramped `\\tfrac`).
        """
        h = board_text(head, head_size, color, "BOLD")
        grp = VGroup(h, tex).arrange(DOWN, buff=buff)
        grp.head, grp.tex = h, tex
        return at(grp, x, y)

    # -- Scene 0: title ------------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = at(board_text("Compounding Periods, Growth & Depreciation",
                                  26, CHALK_PINK, "BOLD"), BOARD_CX, 2.06)
            sub = at(board_text("Half-Yearly · Quarterly · Growth · "
                                "Depreciation", 17, CHALK_WHITE, "BOLD"),
                     BOARD_CX, 1.46)

            self.play(FadeIn(title, shift=UP * 0.08), run_time=0.55)
            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            # the card is bare by design, so each of the narrated numbers
            # spotlights the line that carries the lesson's four parts
            self.wait(leftover(tracker, "b1"))
            self.play(Indicate(sub, color=CHALK_YELLOW, scale_factor=1.03),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Indicate(title, color=CHALK_PINK, scale_factor=1.02),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(Indicate(sub, color=CHALK_YELLOW, scale_factor=1.03),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(Indicate(title, color=CHALK_PINK, scale_factor=1.02),
                      run_time=0.70)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: the conversion period, and the dial that splits -------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Conversion Period", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("How often is the interest added?", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            face = clock_face(-2.45, 0.45)
            sec1 = clock_sectors(-2.45, 0.45, 1)
            lab1 = dial_label(-2.45, 0.45, "1 YEAR")
            note = at(chip("ONE PERIOD EACH YEAR", CHALK_GREEN, size=13),
                      2.90, -0.55)
            rate1 = at(chip("RATE: R PER YEAR", CHALK_AMBER, size=14),
                       2.90, 1.15)
            per1 = at(chip("PERIODS: n", CHALK_CYAN, size=14), 2.90, 0.35)
            rate2 = at(chip("RATE: R/2 PER PERIOD", CHALK_AMBER, size=14),
                       2.90, 1.15)
            rate3 = at(chip("RATE: R/4 PER PERIOD", CHALK_AMBER, size=14),
                       2.90, 1.15)
            per3 = at(chip("PERIODS: 4n", CHALK_CYAN, size=14), 2.90, 0.35)
            sec2 = clock_sectors(-2.45, 0.45, 2)
            sec4 = clock_sectors(-2.45, 0.45, 4)
            lab2 = dial_label(-2.45, 0.45, "HALF-YEARLY")
            lab3 = dial_label(-2.45, 0.45, "QUARTERLY")

            banner = at(board_text("RATE AND PERIODS CHANGE TOGETHER", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The conversion period fixes the rate and "
                                  "the number of periods.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(face), FadeIn(sec1), FadeIn(lab1),
                      FadeIn(note, scale=0.95), run_time=0.65)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(rate1, shift=RIGHT * 0.10),
                      FadeIn(per1, shift=RIGHT * 0.10), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(ReplacementTransform(sec1, sec2),
                      ReplacementTransform(rate1, rate2),
                      ReplacementTransform(lab1, lab2), run_time=0.75)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b3"))
            self.play(ReplacementTransform(sec2, sec4),
                      ReplacementTransform(rate2, rate3),
                      ReplacementTransform(lab2, lab3),
                      ReplacementTransform(per1, per3), run_time=0.85)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: the half-yearly rule -- both things change together ---------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("Half-Yearly: Two Changes at Once", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Halve the rate, double the periods.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            changes = self.hrow(
                chip("RATE HALVES: R → R/2", CHALK_AMBER, size=13),
                chip("PERIODS DOUBLE: n → 2n", CHALK_CYAN, size=13),
                y=1.55, gap=0.55)

            face = clock_face(-2.70, 0.35, r=0.80)
            sec1 = clock_sectors(-2.70, 0.35, 1, r=0.80)
            lab1 = dial_label(-2.70, 0.35, "1 YEAR")
            sec2 = clock_sectors(-2.70, 0.35, 2, r=0.80)
            lab2 = dial_label(-2.70, 0.35, "HALF-YEARLY")

            # a display-style fraction and a full-height power: the exponent is
            # never cramped, and the formula sits on the board's centre line
            # between the dial (left) and the struck-through card (right)
            tex1 = at(chalk_math(r"A = P\left(1 + \frac{R}{100}\right)^{n}",
                                 size=26, color=CHALK_WHITE), BOARD_CX, 0.15)
            tex2 = at(chalk_math(r"A = P\left(1 + \frac{R}{200}\right)^{2n}",
                                 size=26, color=CHALK_YELLOW), BOARD_CX, 0.15)

            wrong = wrong_card("10% EVERY 6 MONTHS", CHALK_RED, width=2.60,
                               height=1.05, size=14)
            wrong.move_to(np.array([3.80, 0.35, 0.0]))
            wrong_cross = wrong.cross
            wrong_cross.set_stroke(opacity=0)

            banner = at(board_text("RATE AND PERIODS CHANGE TOGETHER", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Half-yearly means 5% each half-year, never "
                                  "10% every six months.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(changes, shift=UP * 0.06), FadeIn(face),
                      FadeIn(sec1), FadeIn(lab1), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(ReplacementTransform(sec1, sec2),
                      ReplacementTransform(lab1, lab2), run_time=0.55)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b2"))
            self.play(Indicate(changes[1], color=CHALK_CYAN, scale_factor=1.06),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(tex1, shift=UP * 0.06), run_time=0.40)
            self.play(TransformMatchingTex(tex1, tex2), run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(wrong, scale=0.92), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b5"))
            self.play(wrong_cross.animate.set_stroke(opacity=1),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: the worked half-yearly example ------------------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Half-Yearly: Rs 1,000 at 10%", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Rate 5% for each half-year, 2 periods.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            given = self.hrow(
                chip("P = Rs 1,000", CHALK_GREEN, size=13),
                chip("R = 10% p.a.", CHALK_AMBER, size=13),
                chip("TIME = 1 YEAR", CHALK_CYAN, size=13),
                y=1.45, gap=0.50)
            # the money itself, drawn: rupee coins with thickness beside the
            # principal and beside the payout, and a fanned bundle of notes
            # under each -- the working keeps its own clear column between them
            coins = coin_stack(-4.15, 1.42, 3)
            coins2 = coin_stack(3.30, 0.85, 4)
            seed = note_stack(-3.35, -0.45, 3, "Rs 1,000", 11, CHALK_YELLOW)
            paid = note_stack(4.05, -0.45, 3, "Rs 1,102.50", 11, CHALK_GREEN)

            rate = at(chip("RATE PER PERIOD = 10/2 = 5%", CHALK_AMBER, size=13),
                      -2.60, 0.78)
            periods = at(chip("PERIODS = 2", CHALK_CYAN, size=13), 0.85, 0.78)
            amount = at(chalk_math(r"A = 1000(1.05)^{2} = 1102.50", size=28,
                                   color=CHALK_GREEN), BOARD_CX, -0.45)

            banner = at(board_text("AMOUNT = Rs 1,102.50", 18, CHALK_YELLOW,
                                   "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("CI = 1102.50 - 1000 = Rs 102.50", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(given, shift=UP * 0.06),
                      FadeIn(coins, scale=0.9),
                      FadeIn(seed, scale=0.92), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(rate, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(periods, shift=LEFT * 0.10),
                      FadeIn(coins2, scale=0.9), FadeIn(paid, scale=0.92),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(amount, shift=UP * 0.06),
                      FadeIn(banner, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: quarterly -- the same rule, extended to four periods -------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("Quarterly: R/4 and 4n", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A year has four quarters.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            face = clock_face(-2.55, 0.35)
            sec4 = clock_sectors(-2.55, 0.35, 4)
            lab4 = dial_label(-2.55, 0.35, "QUARTERLY")
            extend = at(chip("SAME RULE, EXTENDED", CHALK_GREEN, size=13),
                        0.45, 0.35)
            rate = at(chip("RATE = R/4 PER QUARTER", CHALK_AMBER, size=13),
                      2.90, 1.25)
            periods = at(chip("PERIODS = 4n", CHALK_CYAN, size=14), 2.90, 0.55)
            formula = at(chalk_math(r"A = P\left(1 + \frac{R}{400}\right)^{4n}",
                                    size=26, color=CHALK_YELLOW), 2.90, -0.40)

            banner = at(board_text("THE SAME CONVERSION-PERIOD RULE", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Quarterly extends the rule from two periods "
                                  "to four.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(face), FadeIn(sec4), FadeIn(lab4),
                      FadeIn(extend, scale=0.95), run_time=0.65)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(rate, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(periods, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(formula, shift=UP * 0.06),
                      FadeIn(banner, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: population growth -- the new total is the next base --------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("Population Growth Is Compound", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The new total becomes the next base.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fact = at(chip("VILLAGE = 6,250 PEOPLE", CHALK_CYAN, size=13),
                      -2.45, 1.35)
            grow = at(chip("GROWTH = 8% EACH YEAR", CHALK_GREEN, size=13),
                      2.55, 1.35)
            town = village(-2.45, 0.30)
            bars = VGroup(
                Rectangle(width=0.30, height=0.30, stroke_width=0,
                          fill_color=CHALK_GREEN, fill_opacity=0.45),
                Rectangle(width=0.30, height=0.45, stroke_width=0,
                          fill_color=CHALK_GREEN, fill_opacity=0.55),
                Rectangle(width=0.30, height=0.62, stroke_width=0,
                          fill_color=CHALK_GREEN, fill_opacity=0.65),
            ).arrange(RIGHT, buff=0.14, aligned_edge=DOWN)
            bars.move_to(np.array([2.55, 0.10, 0.0]))
            rising = arrow_between((2.05, -0.02), (3.15, 0.70), CHALK_YELLOW)

            y1 = at(chip("YEAR 1: 6250 × 1.08 = 6750", CHALK_AMBER, size=13),
                    -2.30, -0.62)
            y2 = at(chip("YEAR 2: 6750 × 1.08 = 7290", CHALK_PINK, size=13),
                    2.85, -0.62)
            banner = at(board_text("6250 × (1.08)^2 = 7,290", 18, CHALK_YELLOW,
                                   "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Repeated increase uses the new total each "
                                  "time.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(town, scale=0.92),
                      FadeIn(fact, shift=UP * 0.06),
                      FadeIn(grow, shift=UP * 0.06), run_time=0.65)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(y1, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(LaggedStart(*[FadeIn(b, scale=0.85) for b in bars],
                                  lag_ratio=0.3),
                      GrowArrow(rising), run_time=0.65)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(y2, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: depreciation -- what remains, and the bouncing ball --------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("Depreciation: Keeping (100 - R)%", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A reduction in value due to use and age.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            keeps = at(chip("KEEPS (100 - R)% EACH TIME", CHALK_CYAN, size=13),
                       2.70, 1.38)
            # the depreciating assets, drawn and shaded: a television and a car
            tv = tv_icon(-3.55, 0.62)
            car = car_icon(-2.45, 0.56)
            bar_full = value_bar(-2.55, -0.05, frac=1.0, label="100%",
                                 color=CHALK_GREEN)
            bar_90 = value_bar(-2.55, -0.05, frac=0.90, label="90%",
                               color=CHALK_AMBER)
            # the ball loses a tenth of its height at every bounce: the drop and
            # all three heights (25 m, 22.5 m, 20.25 m) are drawn on the board
            ball = bounce_track(2.70, -0.10)

            formula = at(chalk_math(r"V = P\left(1 - \frac{R}{100}\right)^{n}",
                                    size=26, color=CHALK_YELLOW), -2.60, 1.38)
            ball_note = at(chip("25 → 22.5 → 20.25 m", CHALK_PINK,
                                size=13), 2.70, -0.66)

            banner = at(board_text("25 × 0.9 × 0.9 = 20.25 m", 18, CHALK_YELLOW,
                                   "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Depreciation keeps the remaining value "
                                  "each time.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(tv, scale=0.92), FadeIn(car, scale=0.92),
                      FadeIn(bar_full), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(keeps, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(ReplacementTransform(bar_full, bar_90), run_time=0.55)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(formula, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(ball), FadeIn(ball_note, shift=UP * 0.06),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.75)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: one structure, three uses ----------------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("One Structure, Three Uses", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Growth multiplies up, depreciation down.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            up_card = at(note_card("GROWTH", ["P(1 + r)^n"], CHALK_GREEN),
                         -2.30, 1.10)
            down_card = at(note_card("DEPRECIATION", ["P(1 - r)^n"], CHALK_PINK),
                           2.30, 1.10)
            how = at(chip("HOW OFTEN?", CHALK_CYAN, size=14), -1.20, 0.05)
            which = at(chip("UP OR DOWN?", CHALK_AMBER, size=14), 0.70, 0.05)
            up_bar, down_bar = meter(3.70, -0.25)

            banner = at(board_text("GROWTH ADDS, DEPRECIATION KEEPS", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("They differ only in the sign of the "
                                  "factor.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(up_card, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(down_card, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(up_bar, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(down_bar, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(how, shift=UP * 0.06),
                      FadeIn(which, shift=UP * 0.06),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the five-step decision map ---------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("Five Steps to Apply It", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Period, rate, factor, repeat.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            steps = self.hrow(
                chip("1 · CONVERSION PERIOD", CHALK_GREEN, size=13),
                chip("2 · RATE PER PERIOD", CHALK_AMBER, size=13),
                chip("3 · NUMBER OF PERIODS", CHALK_CYAN, size=13),
                y=1.35, gap=0.40)
            steps2 = self.hrow(
                chip("4 · PLUS FOR GROWTH", CHALK_GREEN, size=13),
                chip("5 · MINUS FOR DECREASE", CHALK_PINK, size=13),
                y=0.45, gap=0.50)
            rule = at(chip("RATE AND PERIODS CHANGE TOGETHER", CHALK_YELLOW,
                           size=13), BOARD_CX, -0.60)

            banner = at(board_text("PERIOD → RATE → FACTOR → REPEAT", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Five steps, every time.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(steps[0], shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(steps[1], shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(steps[2], shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(steps2[0], shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(steps2[1], shift=UP * 0.06),
                      FadeIn(rule, scale=0.95), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
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
            sub = at(board_text("Three questions and a quick check.", 16,
                                CHALK_WHITE, "BOLD"), BOARD_CX, 2.20)

            pic_a = VGroup(
                board_text("Rs 12,000 · 10% p.a.", 12, CHALK_GREEN, "BOLD"),
                board_text("time 1.5 years", 12, CHALK_GREEN, "BOLD"),
            ).arrange(DOWN, buff=0.24)
            pic_b = VGroup(
                board_text("12% p.a. · 2 years", 12, CHALK_CYAN, "BOLD"),
                board_text("rate? periods?", 12, CHALK_CYAN, "BOLD"),
            ).arrange(DOWN, buff=0.24)
            pic_c = VGroup(
                board_text("TV = Rs 21,000", 12, CHALK_AMBER, "BOLD"),
                board_text("5% in one year", 12, CHALK_AMBER, "BOLD"),
            ).arrange(DOWN, buff=0.24)
            pic_d = VGroup(
                board_text("8% growth → ?", 12, CHALK_PINK, "BOLD"),
                board_text("8% fall → ?", 12, CHALK_PINK, "BOLD"),
            ).arrange(DOWN, buff=0.24)

            qa = at(self.q_card("A · HALF-YEARLY", pic_a, CHALK_GREEN),
                    -2.72, 1.05)
            qb = at(self.q_card("B · QUARTERLY", pic_b, CHALK_CYAN), 3.72, 1.05)
            qc = at(self.q_card("C · DEPRECIATION", pic_c, CHALK_AMBER),
                    -2.72, -1.05)
            qd = at(self.q_card("D · QUICK CHECK", pic_d, CHALK_PINK),
                    3.72, -1.05)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(qa, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(qb, shift=LEFT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(qc, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(qd, shift=LEFT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)
            self.closing(tracker, qd)
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
            a1 = at(self.answer_row("A", "Rs 12,000 × (1.05)^3",
                                    "= Rs 13,891.50 · 5%, 3 periods",
                                    CHALK_GREEN), BOARD_CX, 1.62)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "3% per quarter, 8 quarters",
                                    "A = P(1.03)^8", CHALK_CYAN),
                    BOARD_CX, 0.82)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "Rs 21,000 × 0.95",
                                    "= Rs 19,950 · 95% remains", CHALK_AMBER),
                    BOARD_CX, 0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "growth 1.08",
                                    "depreciation 0.92 · 1 - 0.08", CHALK_PINK),
                    BOARD_CX, -0.78)
            self.play(FadeIn(a4, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, a4)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 10: the whole lesson gathered on one board --------------------
    def beat_s10(self) -> None:
        """The summary: the conversion period's three cases, the two mixed
        formulas, and the five-step map -- one board, in the order the lesson
        taught them."""
        with self.voiceover(text=NARRATION["s10"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Whole Lesson on One Board", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Period · Rate · Formula · Five Steps", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            cases = self.hrow(
                chip("ANNUAL: R · n", CHALK_GREEN, size=13),
                chip("HALF-YEARLY: R/2 · 2n", CHALK_AMBER, size=13),
                chip("QUARTERLY: R/4 · 4n", CHALK_CYAN, size=13),
                y=1.45, gap=0.45)

            growth = self.formula_block(
                "GROWTH: MONEY & POPULATION",
                chalk_math(r"A = P\left(1 + \frac{R}{100}\right)^{n}", size=26,
                           color=CHALK_GREEN), CHALK_GREEN, -2.55, 0.42)
            decay = self.formula_block(
                "DEPRECIATION: VALUE",
                chalk_math(r"V = P\left(1 - \frac{R}{100}\right)^{n}", size=26,
                           color=CHALK_PINK), CHALK_PINK, 2.55, 0.42)

            chain = at(chip("1 PERIOD → 2 RATE → 3 COUNT → 4 +/- → 5 REPEAT",
                            CHALK_YELLOW, size=13), BOARD_CX, -0.66)
            banner = at(board_text("PERIOD · RATE · FORMULA · FIVE STEPS", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("One structure: period, rate, factor, "
                                  "repeat.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(cases[0], shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(cases[1], shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(cases[2], shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(growth, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(decay, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(chain, scale=0.95),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.80)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, chain)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 11: recap and the spoken thank-you ----------------------------
    def beat_s11(self) -> None:
        with self.voiceover(text=NARRATION["s11"]) as tracker:
            self.reset_board()

            heading = at(board_text("Period · Rate · Factor · Repeat", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)

            r1 = at(self.answer_row("1", "CONVERSION PERIOD",
                                    "annually, half-yearly, quarterly",
                                    CHALK_GREEN), BOARD_CX, 1.48)
            r2 = at(self.answer_row("2", "GROWTH",
                                    "P(1 + R/100)^n: money and people",
                                    CHALK_CYAN), BOARD_CX, 0.72)
            r3 = at(self.answer_row("3", "DEPRECIATION",
                                    "P(1 - R/100)^n: the remaining value",
                                    CHALK_PINK), BOARD_CX, -0.04)
            r4 = at(self.answer_row("4", "TWO DECISIONS",
                                    "how often, and up or down",
                                    CHALK_AMBER), BOARD_CX, -0.80)
            strip = at(board_text("Period, rate, factor, repeat.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)
            thanks = at(board_text("Thank You for Watching!", 30, CHALK_WHITE,
                                   "BOLD"), BOARD_CX, 0.62)
            bye = at(board_text("See you in the next lesson :)", 22, CHALK_YELLOW,
                                "BOLD"), BOARD_CX, -0.32)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)

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

            # The list stays on the board through the whole closing sentence:
            # the strip is written on its own bookmark as the voice says
            # "Period, rate, factor, repeat.", and only the bookmark in front of
            # "Thank you for watching," clears the board and brings in the card.
            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeOut(heading), FadeOut(r1), FadeOut(r2), FadeOut(r3),
                      FadeOut(r4), FadeOut(strip), run_time=0.55)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.50)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.closing(tracker, thanks, run_time=0.90)
            self._capture_srt(tracker)

        self.wait(END_HOLD)

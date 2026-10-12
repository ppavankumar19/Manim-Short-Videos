"""
Profit, Loss & Overhead Expenses: Solving Single and Double Transaction
Problems
Story-mode chalkboard lesson (Class 8 Maths, Chapter 5: Comparing Quantities
using Proportion, Storymode 02).

LLM KEY / FUNCTION NAME: profit_loss_overhead_expenses_and_transactions

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

The defining visual is the TRANSACTION LEDGER: a two-column book (MONEY OUT
against MONEY IN) that every scene keeps on the board.  The purchase price sits
at the head of the money-out column, the expense tags -- truck for transport,
spanner for repairs -- dock under it, and all of them flow into one shaded
TOTAL COST PRICE box.  A two-pan balance compares money out with money in (the
money-in side rising is a profit, the money-out side rising is a loss), two
item ledgers physically merge into one total ledger, and the tempting
"+20% and -20% give 0%" is stopped, pulled apart and replaced by the two real
cost prices it was hiding.

Title + 10 scenes:
  0. Title: the purchase price is not the real cost -- Rs 5,600, not Rs 5,000.
  1. Profit, loss, or neither: compare first, then subtract -- with the balance.
  2. The percentage: profit and loss percent are both taken on the cost price,
     and the tempting profit/SP x 100 is struck through.
  3. The refrigerator ledger: Rs 5,000 + Rs 100 + Rs 500 = Rs 5,600 cost,
     Rs 7,000 sold, Rs 1,400 profit, 25%.
  4. The same ledger with a loss: the flat, Rs 4,60,000 cost, Rs 4,25,500 sold,
     Rs 34,500 lost, 7.5%.
  5. The two-item trap: +20% and -20% do NOT cancel -- the two cost prices are
     recovered from their different bases.
  6. The whole transaction: Rs 6,250 cost against Rs 6,000 selling price, a
     loss of Rs 250, that is 4%.
  7. The decision process: five steps, and the totals for several items.
  8. Spoiled stock still costs: the bananas, and the overheads that stay.
  9. Your turn: two problems after the series' centred ten-second THINK clock.
 10. Recap: overheads, comparison, percentage base, totals -- and the spoken
     thank-you card.
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


# (this section is spliced into a head whose own imports omit Arc, Ellipse,
#  Rotate and Sector; Dot, Circle, Line, Polygon, Square, RoundedRectangle,
#  Arrow, VGroup, DEGREES, PI and np are already imported by the head)
from manim import Arc, Ellipse, Rotate, Sector  # noqa: E402,F401

# Board grid shared by every scene of this video.
ROW_Y = 2.72             # every scene heading sits on this line
SUB_Y = 2.16             # the one-line sub-heading under it
BANNER_Y = -1.15         # the banner line (kept clear: the ledgers reach it)
# The burned-in caption grows up from the bottom of the frame: a one-line cue
# starts at y = -3.38 and a wrapped two-line cue reaches y = -2.93 (measured on
# the series' own burned 360p cuts), so every closing strip sits at -1.80 and
# nothing at all sits below CAPTION_SAFE_Y = -2.00 -- audited by the
# IN-CAPTION-BAND check.
STRIP_Y = -1.80
CAPTION_SAFE_Y = -2.00

BAND_A = 0.75            # the upper content band
BAND_B = -0.65           # the lower content band

PANEL_FILL = "#16202B"
CARD_W = 3.30            # the standard card width
CARD_H = 0.94            # the standard card height
CHIP_H = 0.50
MARK_SIZE = 15           # ONE letter size for every row tag

# -- the transaction ledger -------------------------------------------------
# Absolute board coordinates: the ledger is centred on the board's own centre
# line, so every scene's ledger is the same object in the same place.
LEDGER_W = 9.00          # wider than 8.00 on purpose: a full-width panel must
LEDGER_H = 2.94          # never read as a card the clearance audit measures
LEDGER_CY = 0.16         # the frame spans y [-1.31 .. 1.63]
LEDGER_SPLIT = 5.20      # divider at x = BOARD_CX - LEDGER_W/2 + LEDGER_SPLIT
LED_TITLE_Y = 1.36
LED_COL_Y = 0.90
LED_ROW_Y = (0.44, -0.04, -0.52)     # three stacked item rows, 0.48 apart
LED_TOTAL_Y = -1.00
LED_OUT_L, LED_OUT_R = -3.80, 0.85   # the money-out column
LED_IN_L, LED_IN_R = 1.60, 4.80      # the money-in column
LED_OUT_CX = (LED_OUT_L + LED_OUT_R) / 2.0   # -1.475
LED_IN_CX = (LED_IN_L + LED_IN_R) / 2.0      # 3.20

# The example figures this video works with: examples on the board, never
# textbook facts.
FRIDGE_BUY, FRIDGE_MOVE, FRIDGE_FIX, FRIDGE_SELL = 5000, 100, 500, 7000
FLAT_BUY, FLAT_FIX, FLAT_SELL = 450000, 10000, 425500
TABLE_SP, PLUS_PC, MINUS_PC = 3000, 20, 20
BANANA_BUY, BANANA_MOVE, BANANA_SELL = 1250, 250, 1575
CYCLE_BUY, CYCLE_MOVE, CYCLE_FIX, CYCLE_SELL = 4000, 200, 300, 5400
TV_SP = 9900


# --------------------------------------------------------------- furniture --
def write_text_long(path, text: str) -> None:
    """Write a text file, through the extended-length path when needed.

    This topic's media paths -- `...\\media\\videos\\
    profit_loss_overhead_expenses_and_transactions\\360p30\\<Class>.real.srt` --
    run past the 260-character MAX_PATH limit, which is why the chapter pipeline
    renders into the short `D:\\m3` media dir and copies the result back here.
    The copy-back and this ground-truth SRT write therefore fall back to the
    ``\\\\?\\`` extended form when the plain path is too long for the OS.
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


def panel(width, height, color=CHALK_WHITE, opacity=0.6, radius=0.10,
          stroke=1.9):
    """A rounded panel: the box every card, chip and ledger is drawn on."""
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


def two_col_row(lab, val, span, color=CHALK_WHITE, size=13):
    """One ledger line: its label flush left, its amount flush right.

    The row is built at the origin with a FIXED width `span`, so `at()` puts
    the label column and the amount column on the same two vertical lines in
    every row of every ledger of this video.  Fixed columns, not centring: a
    centred row puts each label at a different x.
    """
    a = board_text(lab, size, color, "BOLD")
    b = board_text(val, size, CHALK_WHITE, "BOLD")
    a.move_to(np.array([-span / 2.0 + a.width / 2.0, 0.0, 0.0]))
    b.move_to(np.array([span / 2.0 - b.width / 2.0, 0.0, 0.0]))
    grp = VGroup(a, b)
    grp.label, grp.value = a, b
    return grp


def ledger_line(lab, val, y, color=CHALK_WHITE, size=13,
                x_left=LED_OUT_L, x_right=LED_OUT_R):
    """One ledger line already pinned to its row of the money-out column."""
    return at(two_col_row(lab, val, x_right - x_left, color, size),
              (x_left + x_right) / 2.0, y)


def ledger_frame(width=LEDGER_W, height=LEDGER_H, cx=BOARD_CX, cy=LEDGER_CY,
                 split=LEDGER_SPLIT, title="TRANSACTION LEDGER",
                 left_head="MONEY OUT", right_head="MONEY IN",
                 color=CHALK_AMBER, rule_bot=None):
    """The two-column TRANSACTION LEDGER: one panel, one column rule.

    The rule and the panel are ONE mobject, so the clearance audit never reads
    the rule as a line running into a *foreign* box.  It is still a chalk
    stroke, though, so it must never cross any lettering either: the ledger's
    own title therefore sits over the money-out column, clear of the rule's
    x, and a scene whose lower rows straddle the rule (the merged total ledger)
    passes a `rule_bot` that stops the rule above them.
    """
    box = panel(width, height, color, opacity=0.56, radius=0.14, stroke=2.2)
    box.move_to(np.array([cx, cy, 0.0]))
    rx = cx - width / 2.0 + split
    y0 = box.get_bottom()[1] + 0.16 if rule_bot is None else float(rule_bot)
    rule = Line(np.array([rx, y0, 0.0]),
                np.array([rx, box.get_top()[1] - 0.16, 0.0]),
                stroke_color=color, stroke_width=1.6, stroke_opacity=0.7)
    head = board_text(title, 15, color, "BOLD")
    head.move_to(np.array([cx - 1.10, box.get_top()[1] - 0.28, 0.0]))
    lh = board_text(left_head, 12, CHALK_CYAN, "BOLD")
    lh.move_to(np.array([(box.get_left()[0] + rx) / 2.0,
                         box.get_top()[1] - 0.74, 0.0]))
    rh = board_text(right_head, 12, CHALK_PINK, "BOLD")
    rh.move_to(np.array([(rx + box.get_right()[0]) / 2.0,
                         box.get_top()[1] - 0.74, 0.0]))
    grp = VGroup(box, rule, head, lh, rh)
    grp.box, grp.rule, grp.head = box, rule, head
    grp.left_head, grp.right_head = lh, rh
    return grp


def total_box(text, cx=LED_OUT_CX, cy=LED_TOTAL_Y, color=CHALK_GREEN,
              width=4.55, height=0.50, size=13):
    """The shaded TOTAL COST PRICE box every expense of the column flows into."""
    box = RoundedRectangle(corner_radius=0.08, width=width, height=height,
                           stroke_color=color, stroke_width=1.9,
                           fill_color=color, fill_opacity=0.20)
    box.move_to(np.array([cx, cy, 0.0]))
    lab = board_text(text, size, CHALK_WHITE, "BOLD")
    lab.move_to(box.get_center())
    grp = VGroup(box, lab)
    grp.box, grp.label = box, lab
    return grp


def result_box(text, cx=BOARD_CX, cy=-0.60, color=CHALK_RED,
               width=5.40, height=0.54, size=15):
    """A shaded result strip under the ledger: the overall profit or loss."""
    box = RoundedRectangle(corner_radius=0.08, width=width, height=height,
                           stroke_color=color, stroke_width=1.9,
                           fill_color=color, fill_opacity=0.20)
    box.move_to(np.array([cx, cy, 0.0]))
    lab = board_text(text, size, color, "BOLD")
    lab.move_to(box.get_center())
    grp = VGroup(box, lab)
    grp.box, grp.label = box, lab
    return grp


def math_card(tex, color=CHALK_GREEN, width=3.20, height=1.00, size=22):
    """A card whose whole content is one piece of board maths.

    Nothing else lives in the card, so no two texts can come too close.
    """
    box = panel(width, height, color)
    m = chalk_math(tex, size=size, color=CHALK_WHITE)
    m.move_to(box.get_center())
    grp = VGroup(box, m)
    grp.box, grp.math = box, m
    return grp


def formula_card(head, tex, color=CHALK_GREEN, width=3.20, height=1.52,
                 head_size=15, tex_size=24):
    """A card whose head names a formula and whose body IS that formula."""
    box = panel(width, height, color)
    h = board_text(head, head_size, color, "BOLD")
    m = chalk_math(tex, size=tex_size, color=CHALK_WHITE)
    h.move_to(box.get_center() + np.array([0.0, 0.52, 0.0]))
    m.move_to(box.get_center() + np.array([0.0, -0.30, 0.0]))
    grp = VGroup(box, h, m)
    grp.box, grp.head, grp.math = box, h, m
    return grp


def mini_ledger(head, rows, color=CHALK_GREEN, width=4.10, head_size=13,
                size=12):
    """One item's own small ledger: its head over its label/amount rows."""
    h = board_text(head, head_size, color, "BOLD")
    body = VGroup(*[two_col_row(lab, val, width - 0.70, CHALK_WHITE, size)
                    for lab, val in rows]).arrange(DOWN, buff=0.28)
    content = VGroup(h, body).arrange(DOWN, buff=0.30)
    box = panel(width, content.height + 0.34, color, opacity=0.55)
    content.move_to(box.get_center())
    grp = VGroup(box, content)
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


def wrong_card(text, color=CHALK_RED, width=2.60, height=1.05, size=15):
    """A card holding a WRONG statement, with a drawn cross over it.

    The cross occupies the card's top half and the statement its bottom half, so
    the strike-through is unmistakable yet never comes within the 0.04 units the
    clearance audit allows between a stroke and the lettering.  The whole card is
    ONE board object, so the strokes are never read as a line running into a
    box.  The caller reveals the cross by animating `.cross` to full stroke.
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
    cross.move_to(box.get_center() + np.array([0.10, height / 2 - 0.24, 0.0]))
    lab = board_text(text, size, color, "BOLD")
    lab.move_to(box.get_center() + np.array([0.0, -(height / 2 - 0.22), 0.0]))
    grp = VGroup(box, cross, lab)
    grp.box, grp.cross, grp.label = box, cross, lab
    return grp


def arrow_between(p1, p2, color=CHALK_YELLOW, width=3.0, tip=0.20):
    """A short arrow from one board point to another."""
    return Arrow(np.array([p1[0], p1[1], 0.0]), np.array([p2[0], p2[1], 0.0]),
                 buff=0.0, stroke_color=color, stroke_width=width,
                 tip_length=tip, max_tip_length_to_length_ratio=0.35)


# -- the drawn items --------------------------------------------------------
def refrigerator(cx, cy, scale=1.0, color=CHALK_CYAN):
    """A filled, shaded refrigerator: body, freezer seam, handles, feet."""
    w, h = 0.60 * scale, 0.90 * scale
    body = RoundedRectangle(corner_radius=0.07 * scale, width=w, height=h,
                            stroke_color=color, stroke_width=2.0,
                            fill_color=color, fill_opacity=0.22)
    body.move_to(np.array([cx, cy, 0.0]))
    sy = cy + h * 0.16
    seam = Line(np.array([cx - w / 2 + 0.04, sy, 0.0]),
                np.array([cx + w / 2 - 0.04, sy, 0.0]),
                stroke_color=color, stroke_width=1.6)
    handles = VGroup(
        Line(np.array([cx + w / 2 - 0.09, sy + 0.07, 0.0]),
             np.array([cx + w / 2 - 0.09, sy + 0.22 * scale, 0.0]),
             stroke_color=CHALK_AMBER, stroke_width=2.6),
        Line(np.array([cx + w / 2 - 0.09, sy - 0.24 * scale, 0.0]),
             np.array([cx + w / 2 - 0.09, sy - 0.07, 0.0]),
             stroke_color=CHALK_AMBER, stroke_width=2.6))
    feet = VGroup(*[
        Rectangle(width=0.10 * scale, height=0.06 * scale, stroke_width=0,
                  fill_color=color, fill_opacity=0.7).move_to(
            np.array([cx + dx * w / 3.0, cy - h / 2 - 0.03 * scale, 0.0]))
        for dx in (-1.0, 1.0)])
    return VGroup(body, seam, handles, feet)


def flat_icon(cx, cy, scale=1.0, color=CHALK_AMBER):
    """A filled block of flats: body, lit windows, a door and a roof slab."""
    w, h = 0.86 * scale, 0.74 * scale
    body = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.0,
                     fill_color=color, fill_opacity=0.18)
    body.move_to(np.array([cx, cy, 0.0]))
    roof = Line(np.array([cx - w / 2 - 0.06 * scale, cy + h / 2, 0.0]),
                np.array([cx + w / 2 + 0.06 * scale, cy + h / 2, 0.0]),
                stroke_color=color, stroke_width=4.0)
    windows = VGroup()
    for r in range(2):
        for c in range(3):
            win = Rectangle(width=0.16 * scale, height=0.14 * scale,
                            stroke_width=0, fill_color=CHALK_YELLOW,
                            fill_opacity=0.55)
            win.move_to(np.array([cx + (c - 1) * 0.26 * scale,
                                  cy + 0.17 * scale - r * 0.30 * scale, 0.0]))
            windows.add(win)
    door = Rectangle(width=0.16 * scale, height=0.20 * scale, stroke_width=0,
                     fill_color=color, fill_opacity=0.6)
    door.move_to(np.array([cx, cy - h / 2 + 0.10 * scale, 0.0]))
    return VGroup(body, windows, door, roof)


def table_icon(cx, cy, scale=1.0, color=CHALK_AMBER):
    """A filled table: a solid top over two legs and a rail."""
    w, h = 0.80 * scale, 0.50 * scale
    top = Rectangle(width=w, height=0.13 * scale, stroke_color=color,
                    stroke_width=1.8, fill_color=color, fill_opacity=0.55)
    top.move_to(np.array([cx, cy + h / 2 - 0.065 * scale, 0.0]))
    legs = VGroup(*[
        Rectangle(width=0.09 * scale, height=h - 0.16 * scale, stroke_width=0,
                  fill_color=color, fill_opacity=0.40).move_to(
            np.array([cx + sx * (w / 2 - 0.08 * scale),
                      cy - 0.08 * scale, 0.0]))
        for sx in (-1.0, 1.0)])
    rail = Rectangle(width=w * 0.66, height=0.07 * scale, stroke_width=0,
                     fill_color=color, fill_opacity=0.35)
    rail.move_to(np.array([cx, cy - h / 2 + 0.14 * scale, 0.0]))
    return VGroup(top, legs, rail)


def bicycle_icon(cx, cy, scale=1.0, color=CHALK_CYAN):
    """A filled bicycle: two solid-tyred wheels, a frame, a seat and bars."""
    r = 0.20 * scale

    def wheel(dx):
        c = np.array([cx + dx, cy - 0.10 * scale, 0.0])
        return VGroup(
            Circle(radius=r, stroke_color=color, stroke_width=3.0,
                   fill_color=color, fill_opacity=0.12).move_to(c),
            Circle(radius=r * 0.24, stroke_width=0, fill_color=color,
                   fill_opacity=0.9).move_to(c))

    p0 = np.array([cx - 0.30 * scale, cy - 0.10 * scale, 0.0])
    p1 = np.array([cx - 0.02 * scale, cy + 0.22 * scale, 0.0])
    p2 = np.array([cx + 0.10 * scale, cy - 0.10 * scale, 0.0])
    p3 = np.array([cx + 0.30 * scale, cy - 0.10 * scale, 0.0])
    frame = VGroup(
        Line(p0, p1, stroke_color=color, stroke_width=3.0),
        Line(p1, p2, stroke_color=color, stroke_width=3.0),
        Line(p2, p3, stroke_color=color, stroke_width=3.0),
        Line(p0, p2, stroke_color=color, stroke_width=3.0))
    seat = Rectangle(width=0.17 * scale, height=0.06 * scale, stroke_width=0,
                     fill_color=CHALK_AMBER, fill_opacity=0.9)
    seat.move_to(np.array([cx - 0.06 * scale, cy + 0.26 * scale, 0.0]))
    bars = Line(np.array([cx + 0.10 * scale, cy + 0.20 * scale, 0.0]),
                np.array([cx + 0.24 * scale, cy + 0.30 * scale, 0.0]),
                stroke_color=CHALK_AMBER, stroke_width=3.0)
    return VGroup(wheel(-0.30 * scale), wheel(0.30 * scale), frame, seat, bars)


def tv_icon(cx, cy, scale=1.0, color=CHALK_PINK):
    """A filled television: a lit screen in a case, on a stand, with aerials."""
    w, h = 0.72 * scale, 0.50 * scale
    body = RoundedRectangle(corner_radius=0.05 * scale, width=w, height=h,
                            stroke_color=color, stroke_width=2.0,
                            fill_color=color, fill_opacity=0.22)
    body.move_to(np.array([cx, cy, 0.0]))
    screen = Rectangle(width=w - 0.14 * scale, height=h - 0.14 * scale,
                       stroke_width=0, fill_color=CHALK_CYAN,
                       fill_opacity=0.30)
    screen.move_to(np.array([cx, cy, 0.0]))
    stand = Polygon(np.array([cx - 0.14 * scale, cy - h / 2, 0.0]),
                    np.array([cx + 0.14 * scale, cy - h / 2, 0.0]),
                    np.array([cx + 0.06 * scale, cy - h / 2 - 0.09 * scale, 0.0]),
                    np.array([cx - 0.06 * scale, cy - h / 2 - 0.09 * scale, 0.0]),
                    stroke_width=0, fill_color=color, fill_opacity=0.55)
    aerials = VGroup(
        Line(np.array([cx - 0.02 * scale, cy + h / 2, 0.0]),
             np.array([cx - 0.17 * scale, cy + h / 2 + 0.17 * scale, 0.0]),
             stroke_color=color, stroke_width=2.0),
        Line(np.array([cx + 0.02 * scale, cy + h / 2, 0.0]),
             np.array([cx + 0.17 * scale, cy + h / 2 + 0.17 * scale, 0.0]),
             stroke_color=color, stroke_width=2.0))
    return VGroup(body, screen, stand, aerials)


def banana_bunch(cx, cy, scale=1.0, color=CHALK_YELLOW):
    """A bunch of bananas: three thick filled crescents over a stalk.

    The crescents are drawn as fat chalk arcs (a filled band, not a hairline),
    each with a chalk highlight down its back, so the bunch reads as solid
    fruit and not as three bare outlines.
    """
    fruit = VGroup()
    for dx in (-0.17, 0.0, 0.17):
        c = np.array([cx + dx * scale, cy + 0.06 * scale, 0.0])
        fruit.add(Arc(radius=0.30 * scale, start_angle=200 * DEGREES,
                      angle=140 * DEGREES, arc_center=c,
                      stroke_color=color, stroke_width=12.0 * scale))
        fruit.add(Arc(radius=0.30 * scale, start_angle=205 * DEGREES,
                      angle=130 * DEGREES, arc_center=c,
                      stroke_color=CHALK_WHITE, stroke_width=3.0 * scale,
                      stroke_opacity=0.35))
    stalk = Rectangle(width=0.10 * scale, height=0.16 * scale, stroke_width=0,
                      fill_color="#8A6B2A", fill_opacity=0.9)
    stalk.move_to(np.array([cx, cy - 0.14 * scale, 0.0]))
    return VGroup(stalk, fruit)


def truck_icon(cx, cy, scale=1.0, color=CHALK_CYAN):
    """A filled delivery truck: cargo box, cab and two wheels."""
    box = Rectangle(width=0.50 * scale, height=0.30 * scale,
                    stroke_color=color, stroke_width=1.8,
                    fill_color=color, fill_opacity=0.30)
    box.move_to(np.array([cx - 0.09 * scale, cy + 0.06 * scale, 0.0]))
    cab = Polygon(np.array([cx + 0.17 * scale, cy - 0.09 * scale, 0.0]),
                  np.array([cx + 0.38 * scale, cy - 0.09 * scale, 0.0]),
                  np.array([cx + 0.38 * scale, cy + 0.04 * scale, 0.0]),
                  np.array([cx + 0.25 * scale, cy + 0.15 * scale, 0.0]),
                  np.array([cx + 0.17 * scale, cy + 0.15 * scale, 0.0]),
                  stroke_color=color, stroke_width=1.8,
                  fill_color=color, fill_opacity=0.30)
    wheels = VGroup(*[
        Circle(radius=0.075 * scale, stroke_width=0, fill_color=CHALK_WHITE,
               fill_opacity=0.75).move_to(
            np.array([cx + dx * scale, cy - 0.16 * scale, 0.0]))
        for dx in (-0.20, 0.28)])
    return VGroup(box, cab, wheels)


def wrench_icon(cx, cy, scale=1.0, color=CHALK_AMBER):
    """A filled spanner: a thick handle under an open two-jaw head."""
    handle = Line(np.array([cx - 0.05 * scale, cy - 0.20 * scale, 0.0]),
                  np.array([cx + 0.04 * scale, cy + 0.10 * scale, 0.0]),
                  stroke_color=color, stroke_width=7.0 * scale)
    jaws = VGroup(
        Polygon(np.array([cx + 0.01 * scale, cy + 0.09 * scale, 0.0]),
                np.array([cx + 0.17 * scale, cy + 0.15 * scale, 0.0]),
                np.array([cx + 0.15 * scale, cy + 0.30 * scale, 0.0]),
                np.array([cx + 0.03 * scale, cy + 0.24 * scale, 0.0]),
                stroke_width=0, fill_color=color, fill_opacity=0.85),
        Polygon(np.array([cx - 0.04 * scale, cy + 0.09 * scale, 0.0]),
                np.array([cx + 0.09 * scale, cy + 0.02 * scale, 0.0]),
                np.array([cx + 0.19 * scale, cy + 0.04 * scale, 0.0]),
                np.array([cx + 0.06 * scale, cy + 0.14 * scale, 0.0]),
                stroke_width=0, fill_color=color, fill_opacity=0.85))
    return VGroup(handle, jaws)


def balance_rig(cx, cy, scale=1.0, arm_color=CHALK_AMBER):
    """The two-pan balance that compares money out with money in.

    Returns `(stand, tracker, moving)`.  `stand` is the fixed post and base;
    `moving` is an `always_redraw` beam, ropes and pair of pans driven by
    `tracker`, so `tracker.animate.set_value(v)` is the whole comparison:

        v > 0  the money-in pan rises  -> a profit,
        v < 0  the money-out pan rises -> a loss.

    The pans are shallow filled dishes (never bare outlines), and `moving` is
    added straight to the scene -- the same pattern the series' own compasses
    use -- so the audit sees the real pose of every stroke.
    """
    pivot = np.array([cx, cy + 0.66 * scale, 0.0])
    arm = 1.24 * scale
    stand = VGroup(
        Polygon(np.array([cx - 0.30 * scale, cy - 0.66 * scale, 0.0]),
                np.array([cx + 0.30 * scale, cy - 0.66 * scale, 0.0]),
                np.array([cx + 0.13 * scale, pivot[1], 0.0]),
                np.array([cx - 0.13 * scale, pivot[1], 0.0]),
                stroke_color=arm_color, stroke_width=1.8,
                fill_color=arm_color, fill_opacity=0.22),
        RoundedRectangle(corner_radius=0.04, width=1.30 * scale,
                         height=0.14 * scale, stroke_color=arm_color,
                         stroke_width=1.8, fill_color=arm_color,
                         fill_opacity=0.30).move_to(
            np.array([cx, cy - 0.66 * scale - 0.07 * scale, 0.0])))
    tracker = ValueTracker(0.0)

    def build():
        ang = float(tracker.get_value()) * 12 * DEGREES
        d = np.array([np.cos(ang), np.sin(ang), 0.0])
        left, right = pivot - d * arm, pivot + d * arm
        grp = VGroup(Line(left, right, stroke_color=arm_color,
                          stroke_width=7.0))
        for end in (left, right):
            pan_y = end[1] - 0.46 * scale
            grp.add(Line(end, np.array([end[0] - 0.26 * scale, pan_y, 0.0]),
                         stroke_color=arm_color, stroke_width=1.6),
                    Line(end, np.array([end[0] + 0.26 * scale, pan_y, 0.0]),
                         stroke_color=arm_color, stroke_width=1.6),
                    Polygon(np.array([end[0] - 0.34 * scale, pan_y, 0.0]),
                            np.array([end[0] + 0.34 * scale, pan_y, 0.0]),
                            np.array([end[0] + 0.24 * scale,
                                      pan_y - 0.13 * scale, 0.0]),
                            np.array([end[0] - 0.24 * scale,
                                      pan_y - 0.13 * scale, 0.0]),
                            stroke_color=CHALK_YELLOW, stroke_width=1.6,
                            fill_color=CHALK_YELLOW, fill_opacity=0.24))
        return grp

    return stand, tracker, always_redraw(build)


# ----------------------------------------------------------------


NARRATION = {
    "title": (
        "The purchase price is not always the real cost. <bookmark mark='b0'/> "
        "A second-hand refrigerator is bought for five thousand rupees. "
        "<bookmark mark='b1'/> Then one hundred rupees go on transport, "
        "<bookmark mark='b2'/> and five hundred rupees on repairs. <bookmark "
        "mark='b3'/> So the money actually spent is five thousand plus one "
        "hundred plus five hundred, that is five thousand six hundred rupees. "
        "<bookmark mark='b4'/> Sold for seven thousand rupees, the real profit "
        "is seven thousand minus five thousand six hundred, which is one "
        "thousand four hundred rupees. <bookmark mark='b5'/> Not two thousand."
    ),
    "s1": (
        "First, decide whether a deal is a profit, a loss, or neither. "
        "<bookmark mark='b0'/> Cost price five hundred rupees, selling price "
        "six hundred and fifty: the selling price is bigger, so this is a "
        "profit of six hundred fifty minus five hundred, that is one hundred "
        "and fifty rupees. <bookmark mark='b1'/> Now change the selling price "
        "to four hundred and fifty: this time the cost price is bigger, so it "
        "is a loss of five hundred minus four hundred fifty, that is fifty "
        "rupees. <bookmark mark='b2'/> And when the selling "
        "price equals the cost price, there is neither a profit nor a loss. "
        "<bookmark mark='b3'/> So there are two formulas: profit is selling "
        "price minus cost price, and loss is cost price minus selling price. "
        "<bookmark mark='b4'/> Always ask which one is bigger before you "
        "subtract."
    ),
    "s2": (
        "Now the percentage. <bookmark mark='b0'/> A profit of one hundred "
        "fifty rupees on a cost price of five hundred rupees is a profit of "
        "thirty percent. <bookmark mark='b1'/> The difference is always "
        "measured against the cost price: profit percent is profit divided by "
        "cost price, times one hundred. <bookmark mark='b2'/> And loss percent "
        "is loss divided by cost price, times one hundred. <bookmark "
        "mark='b3'/> The cost price is the base. <bookmark mark='b4'/> A very "
        "common error is to divide by the selling price instead. That is "
        "wrong, and we cross it out."
    ),
    "s3": (
        "Let us keep a proper ledger for the refrigerator. <bookmark "
        "mark='b0'/> Purchase price five thousand rupees. <bookmark "
        "mark='b1'/> Add transport, one hundred rupees, <bookmark mark='b2'/> "
        "and repairs, five hundred rupees. <bookmark mark='b3'/> So the total "
        "cost price is five thousand six hundred rupees. <bookmark mark='b4'/> "
        "The selling price is seven thousand rupees, so the profit is one "
        "thousand four hundred rupees. <bookmark mark='b5'/> And the profit "
        "percent is one thousand four hundred divided by five thousand six "
        "hundred, times one hundred. That is twenty five percent."
    ),
    "s4": (
        "Here is the same idea with a loss. <bookmark mark='b0'/> A flat is "
        "bought for four lakh fifty thousand rupees. <bookmark mark='b1'/> Ten "
        "thousand rupees are spent on repairs and painting, <bookmark "
        "mark='b2'/> so the total cost price is four lakh sixty thousand "
        "rupees. <bookmark mark='b3'/> It is sold for four lakh twenty five "
        "thousand five hundred rupees, so the selling price is smaller. "
        "<bookmark mark='b4'/> The loss is four lakh sixty thousand minus four "
        "lakh twenty five thousand five hundred, that is thirty four thousand "
        "five hundred rupees. <bookmark mark='b5'/> And the loss percent is "
        "thirty four thousand five hundred divided by four lakh sixty "
        "thousand, times one hundred, which is seven point five percent."
    ),
    "s5": (
        "Now a trap. <bookmark mark='b0'/> Two tables are each sold for three "
        "thousand rupees. <bookmark mark='b1'/> One gives a gain of twenty "
        "percent, <bookmark mark='b2'/> and the other gives a loss of twenty "
        "percent. <bookmark mark='b3'/> Do the plus twenty and the minus "
        "twenty cancel? It is tempting to say zero percent. <bookmark "
        "mark='b4'/> But the percentages act on different cost prices. On the "
        "first table, three thousand rupees is one hundred and twenty percent "
        "of the cost price, so the cost price is three thousand divided by one "
        "point two, that is two thousand five hundred rupees. <bookmark "
        "mark='b5'/> On the second table, three thousand rupees is eighty "
        "percent of the cost price, so the cost price is three thousand "
        "divided by zero point eight, that is three thousand seven hundred and "
        "fifty rupees. The two bases are different."
    ),
    "s6": (
        "Now solve the whole transaction. <bookmark mark='b0'/> The total cost "
        "price is two thousand five hundred plus three thousand seven hundred "
        "fifty, that is six thousand two hundred and fifty rupees. <bookmark "
        "mark='b1'/> The total selling price is three thousand plus three "
        "thousand, that is six thousand rupees. <bookmark mark='b2'/> The "
        "selling price is smaller, so overall there is a loss of two hundred "
        "and fifty rupees. <bookmark mark='b3'/> And the loss percent is two "
        "hundred and fifty divided by six thousand two hundred fifty, times "
        "one hundred, which is four percent. <bookmark mark='b4'/> So plus "
        "twenty percent and minus twenty percent did not give zero percent "
        "here."
    ),
    "s7": (
        "Here is the decision process, in five steps. <bookmark mark='b0'/> "
        "Step one: find the purchase price. <bookmark mark='b1'/> Step two: "
        "add every overhead expense to get the total cost price. <bookmark "
        "mark='b2'/> Step three: find the total selling price. <bookmark "
        "mark='b3'/> Step four: compare the two. If the selling price is "
        "bigger there is a profit, and if it is smaller there is a loss. "
        "<bookmark mark='b4'/> Step five: divide by the cost price and "
        "multiply by one hundred for the percentage. <bookmark mark='b5'/> And "
        "when there are several items, compare the sum of the cost prices with "
        "the sum of the selling prices."
    ),
    "s8": (
        "One more reminder. <bookmark mark='b0'/> Overheads still count when "
        "part of the stock cannot be sold. <bookmark mark='b1'/> Bananas are "
        "bought for one thousand two hundred and fifty rupees, and two hundred "
        "and fifty rupees go on transport, so the total cost price is one "
        "thousand five hundred rupees. <bookmark mark='b2'/> Only some dozens "
        "are good enough to sell, and they bring in one thousand five hundred "
        "and seventy five rupees. <bookmark mark='b3'/> The spoiled bananas do "
        "not vanish from the cost: the money spent on them is still part of "
        "the cost price. <bookmark mark='b4'/> And the profit is one thousand "
        "five hundred seventy five minus one thousand five hundred, that is "
        "seventy five rupees, which is five percent."
    ),
    "s9q": (
        "Your turn. <bookmark mark='b0'/> First: a bicycle is bought for four "
        "thousand rupees, <bookmark mark='b1'/> with two hundred rupees for "
        "transport and three hundred rupees for repair. It is sold for five "
        "thousand four hundred rupees. Find the total cost price, the profit, "
        "and the profit percent. <bookmark mark='b2'/> Second: two television "
        "sets are each sold for nine thousand nine hundred rupees. <bookmark "
        "mark='b3'/> One gives a profit of ten percent, and the other gives a "
        "loss of ten percent. Did the plus ten and the minus ten cancel?"
    ),
    "s9a": (
        "Let us check. <bookmark mark='b0'/> For the bicycle, the overheads are "
        "two hundred plus three hundred, so the total cost price is four "
        "thousand five hundred rupees. <bookmark mark='b1'/> The profit is five "
        "thousand four hundred minus four thousand five hundred, that is nine "
        "hundred rupees, and the profit percent is nine hundred divided by four "
        "thousand five hundred, times one hundred, which is twenty percent. "
        "<bookmark mark='b2'/> For the television sets, the first cost price is "
        "nine thousand nine hundred divided by one point one, that is nine "
        "thousand rupees. <bookmark mark='b3'/> The second cost price is nine "
        "thousand nine hundred divided by zero point nine, that is eleven "
        "thousand rupees. The total cost price is twenty thousand rupees and "
        "the total selling price is nineteen thousand eight hundred, so there "
        "is a loss of two hundred rupees, which is one percent. The plus ten "
        "and the minus ten did not cancel."
    ),
    "s10": (
        "Let us put it together. <bookmark mark='b0'/> First add the overheads "
        "to the purchase price. <bookmark mark='b1'/> Then compare the total "
        "cost price with the selling price. <bookmark mark='b2'/> Take the "
        "percentage on the cost price, never on the selling price. <bookmark "
        "mark='b3'/> And for several items, compare the total cost with the "
        "total selling price. <bookmark mark='b4'/> The purchase price alone "
        "is never the real cost. <bookmark mark='b5'/> Thank you for watching, "
        "<bookmark mark='b6'/> and see you in the next lesson."
    ),
}


class ProfitLossOverheadExpensesAndTransactionsStory(VoiceoverScene):
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
        out_dir = _HERE / "media" / "videos" / "profit_loss_overhead_expenses_and_transactions"
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

        self._write_real_srt()

    # ================================================================ beats ==
    # Profit, Loss & Overhead Expenses: Solving Single and Double Transaction
    # Problems (Class 8 Maths, Chapter 5, Storymode 02).
    #
    # SYNC RULE for every reveal: wait for the narration bookmark that starts
    # the phrase naming a thing, and only then bring it on.  Playing first and
    # waiting afterwards shows the picture a whole window early, which reads as
    # broken sync.
    #
    # Layout rules, so the audits stay clean:
    #   * the heading sits on the board's own heading line (2.72) and its
    #     sub-heading at 2.16, the closing strip at -1.80 -- nothing at all
    #     below CAPTION_SAFE_Y = -2.00;
    #   * every stacked pair of texts is at least 0.22 units apart, which is why
    #     the ledger rows sit 0.48 apart and every reveal is a short fade;
    #   * a drawn cross always lives in the SAME VGroup as the card it strikes
    #     through (`wrong_card`), so the audit never reads the strokes as a line
    #     running into somebody else's box;
    #   * the answer rows, the five steps and the recap list share one set of
    #     fixed columns (`answer_row`), so A/B/C/D and 1/2/3/4 sit on one
    #     vertical line;
    #   * the challenge uses the series' shared 10-second THINK clock, dead
    #     centre of the board, with the question cards in the four corners.

    def closing(self, tracker, mob=None, color=CHALK_YELLOW, run_time=None):
        """Consume the tail of the narration window on the last reveal."""
        budget = rt(tracker.get_remaining_duration()) if run_time is None \
            else run_time
        if mob is None:
            self.wait(max(budget, 0.0))
        else:
            self.play(Indicate(mob, color=color, scale_factor=1.03),
                      run_time=max(budget, MIN_RT))

    def answer_row(self, tag, headline, note, color, width=8.60, height=0.62,
                   pad=0.30):
        """One revealed row: its tag, the result and a short note.

        The cells sit in FIXED columns, not centred: the tag column and the
        name column are the same two vertical lines in every row of every list
        of this video (which is what keeps A/B/C/D and 1/2/3/4 on one line) and
        the note is flush with the row's own right edge.  Centring put each tag
        at a different x.
        """
        box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                               stroke_color=color, stroke_width=1.8,
                               fill_color=PANEL_FILL, fill_opacity=0.60)
        lab = board_text(tag, 15, color, "BOLD")
        name = board_text(headline, 14, color, "BOLD")
        txt = board_text(note, 13, CHALK_WHITE, "BOLD")
        x0 = box.get_left()[0] + pad
        cy = box.get_center()[1]
        lab.move_to(np.array([x0 + 0.19, cy, 0.0]))
        name.move_to(np.array([x0 + 0.62 + name.width / 2.0, cy, 0.0]))
        txt.move_to(np.array([box.get_right()[0] - pad - txt.width / 2.0,
                              cy, 0.0]))
        grp = VGroup(box, lab, name, txt)
        grp.box, grp.tag, grp.name, grp.note = box, lab, name, txt
        return grp

    def q_card(self, title, lines, color=CHALK_CYAN, width=3.50, pad=0.14,
               title_size=13, line_size=12, buff=0.28):
        """One 'your turn' card: a prompt over the figures it asks about."""
        head = board_text(title, title_size, color, "BOLD")
        body = VGroup(*[board_text(line, line_size, CHALK_WHITE, "BOLD")
                        for line in lines]).arrange(DOWN, buff=0.24)
        content = VGroup(head, body).arrange(DOWN, buff=buff)
        box = RoundedRectangle(corner_radius=0.10, width=width,
                               height=content.height + 2 * pad,
                               stroke_color=color, stroke_width=1.9,
                               fill_color=PANEL_FILL, fill_opacity=0.55)
        content.move_to(box.get_center())
        grp = VGroup(box, content)
        grp.box, grp.head, grp.body = box, head, body
        return grp

    # -- Scene 0: title ------------------------------------------------------
    # The purchase price is not the real cost: the refrigerator, the two
    # expense tags that dock under it, the total cost price they flow into and
    # the profit that remains -- with the tempting "Rs 2,000" struck through.
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Real Cost of a Purchase", 24,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A second-hand refrigerator.", 16,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fridge = at(refrigerator(0.0, 0.0, 1.35, CHALK_CYAN), -3.70, 0.95)
            buy = at(chip("BOUGHT FOR Rs 5,000", CHALK_CYAN, size=14),
                     -0.60, 1.45)
            truck = at(truck_icon(0.0, 0.0, 1.15), -2.45, 0.70)
            move_tag = at(chip("TRANSPORT Rs 100", CHALK_YELLOW, size=14),
                          -0.60, 0.70)
            spanner = at(wrench_icon(0.0, 0.0, 1.15), -2.45, -0.05)
            fix_tag = at(chip("REPAIRS Rs 500", CHALK_YELLOW, size=14),
                         -0.60, -0.05)
            flow = arrow_between((-0.60, -0.36), (-0.60, -0.71), CHALK_GREEN)
            total = total_box("TOTAL COST PRICE = Rs 5,600", -0.60, -1.05,
                              CHALK_GREEN, width=3.60)
            sold = at(chip("SOLD FOR Rs 7,000", CHALK_PINK, size=14), 3.50, 1.45)
            real = at(board_text("REAL PROFIT", 15, CHALK_GREEN, "BOLD"),
                      3.50, 0.75)
            amount = at(chip("Rs 1,400", CHALK_GREEN, size=20), 3.50, 0.15)
            wrong = wrong_card("Rs 2,000", CHALK_RED, width=2.20, height=1.00,
                               size=16)
            wrong.move_to(np.array([3.50, -0.90, 0.0]))
            wrong_cross = wrong.cross
            wrong_cross.set_stroke(opacity=0)
            strip = at(board_text("Rs 5,000 + Rs 100 + Rs 500 = Rs 5,600 is "
                                  "the real cost.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(fridge, scale=0.92),
                      FadeIn(buy, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(truck, shift=RIGHT * 0.10),
                      FadeIn(move_tag, shift=RIGHT * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(spanner, shift=RIGHT * 0.10),
                      FadeIn(fix_tag, shift=RIGHT * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(GrowArrow(flow), FadeIn(total, scale=0.94), run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(sold, shift=UP * 0.06), FadeIn(real, shift=UP * 0.06),
                      FadeIn(amount, scale=0.90), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(wrong, scale=0.92),
                      wrong_cross.animate.set_stroke(opacity=1),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: profit, loss, or neither -- and the two-pan balance ---------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("Profit, Loss, or Neither?", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Ask which one is bigger before subtracting.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            r1 = at(self.answer_row("1", "SP 650 > CP 500", "PROFIT Rs 150",
                                    CHALK_GREEN, width=5.20, height=0.56),
                    -1.85, 1.30)
            r2 = at(self.answer_row("2", "SP 450 < CP 500", "LOSS Rs 50",
                                    CHALK_RED, width=5.20, height=0.56),
                    -1.85, 0.60)
            r3 = at(self.answer_row("3", "SP 500 = CP 500", "NEITHER",
                                    CHALK_YELLOW, width=5.20, height=0.56),
                    -1.85, -0.10)
            f1 = chip("PROFIT = SP - CP", CHALK_GREEN, size=14)
            f2 = chip("LOSS = CP - SP", CHALK_PINK, size=14)
            formulas = VGroup(f1, f2).arrange(RIGHT, buff=0.45)
            at(formulas, -1.85, -0.95)

            stand, beam, moving = balance_rig(2.95, 0.55, 0.80)
            out_lbl = at(board_text("MONEY OUT", 11, CHALK_CYAN, "BOLD"),
                         1.96, 0.20)
            in_lbl = at(board_text("MONEY IN", 11, CHALK_PINK, "BOLD"),
                        3.94, 0.20)

            strip = at(board_text("Always compare before you subtract.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(r1, shift=UP * 0.06), FadeIn(stand, scale=0.94),
                      FadeIn(moving), FadeIn(out_lbl), FadeIn(in_lbl),
                      beam.animate.set_value(1.0), run_time=0.70)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(r2, shift=UP * 0.06), beam.animate.set_value(-1.0),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(r3, shift=UP * 0.06), beam.animate.set_value(0.0),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(f1, scale=0.92), FadeIn(f2, scale=0.92),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: the percentage is taken on the cost price -------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Percentage Is Taken on CP", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Measured against the cost price.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            example = at(chip("Rs 150 ON CP Rs 500 = 30%", CHALK_CYAN, size=13),
                         BOARD_CX, 0.95)
            base = at(chip("THE BASE IS ALWAYS CP", CHALK_YELLOW, size=13),
                      BOARD_CX, 0.15)
            pc = formula_card("PROFIT PERCENT",
                              r"\frac{\text{Profit}}{\text{CP}} \times 100",
                              CHALK_GREEN)
            at(pc, -2.70, 0.85)
            lc = formula_card("LOSS PERCENT",
                              r"\frac{\text{Loss}}{\text{CP}} \times 100",
                              CHALK_PINK)
            at(lc, 3.70, 0.85)
            wrong = wrong_card("PROFIT / SP × 100", CHALK_RED, width=2.90,
                               height=1.10, size=15)
            wrong.move_to(np.array([BOARD_CX, -0.75, 0.0]))
            wrong_cross = wrong.cross
            wrong_cross.set_stroke(opacity=0)
            strip = at(board_text("Never divide the difference by the selling "
                                  "price.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(example, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(pc, scale=0.94), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(lc, scale=0.94), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(base, scale=0.92), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(wrong, scale=0.92),
                      wrong_cross.animate.set_stroke(opacity=1),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: the refrigerator ledger -- an overhead profit ---------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Refrigerator Ledger", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Add every expense to the purchase price.", 16,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            frame = ledger_frame()
            fridge = at(refrigerator(0.0, 0.0, 0.58, CHALK_CYAN), -3.35, 1.36)
            out1 = ledger_line("Purchase price", "Rs 5,000", LED_ROW_Y[0],
                               CHALK_CYAN)
            out2 = ledger_line("Transport", "Rs 100", LED_ROW_Y[1], CHALK_YELLOW)
            out3 = ledger_line("Repairs", "Rs 500", LED_ROW_Y[2], CHALK_YELLOW)
            total = total_box("TOTAL COST PRICE = Rs 5,600")
            in1 = ledger_line("Selling price", "Rs 7,000", LED_ROW_Y[0],
                              CHALK_PINK, x_left=LED_IN_L, x_right=LED_IN_R)
            in2 = ledger_line("Profit", "Rs 1,400", LED_ROW_Y[1], CHALK_GREEN,
                              x_left=LED_IN_L, x_right=LED_IN_R)
            in3 = at(chalk_math(r"1400 \div 5600 \times 100 = 25\%", size=21,
                                color=CHALK_GREEN), LED_IN_CX, LED_ROW_Y[2])
            strip = at(board_text("The purchase price plus the overheads is the "
                                  "real cost.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(frame, scale=0.97), FadeIn(fridge, scale=0.92),
                      FadeIn(out1, shift=RIGHT * 0.06), run_time=0.65)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(out2, shift=RIGHT * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(out3, shift=RIGHT * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(total, scale=0.94), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(in1, shift=RIGHT * 0.06),
                      FadeIn(in2, shift=RIGHT * 0.06), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(in3, shift=UP * 0.06), FadeIn(strip, shift=UP * 0.06),
                      run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, total)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: the same ledger with a loss ---------------------------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("Overheads Can Bring a Loss", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A flat bought and then repaired.", 16,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            frame = ledger_frame()
            flat = at(flat_icon(0.0, 0.0, 0.72, CHALK_AMBER), -3.30, 1.35)
            out1 = ledger_line("Purchase price", "Rs 4,50,000", LED_ROW_Y[0],
                               CHALK_CYAN)
            out2 = ledger_line("Repairs, painting", "Rs 10,000", LED_ROW_Y[1],
                               CHALK_YELLOW)
            total = total_box("TOTAL COST PRICE = Rs 4,60,000")
            in1 = ledger_line("Selling price", "Rs 4,25,500", LED_ROW_Y[0],
                              CHALK_PINK, x_left=LED_IN_L, x_right=LED_IN_R)
            in2 = ledger_line("Loss", "Rs 34,500", LED_ROW_Y[1], CHALK_RED,
                              x_left=LED_IN_L, x_right=LED_IN_R)
            in3 = at(chalk_math(r"34500 \div 460000 \times 100 = 7.5\%",
                                size=21, color=CHALK_RED), LED_IN_CX,
                     LED_ROW_Y[2])
            strip = at(board_text("The overheads still belong to the cost.", 15,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(frame, scale=0.97), FadeIn(flat, scale=0.92),
                      FadeIn(out1, shift=RIGHT * 0.06), run_time=0.65)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(out2, shift=RIGHT * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(total, scale=0.94), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(in1, shift=RIGHT * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(in2, shift=RIGHT * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(in3, shift=UP * 0.06), FadeIn(strip, shift=UP * 0.06),
                      run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, total)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: the two-item trap -- +20% and -20% do NOT cancel ------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("Two Tables, Twenty Percent Each", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Do a gain and a loss cancel?", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            table1 = at(table_icon(0.0, 0.0, 0.95), -2.70, 1.15)
            table2 = at(table_icon(0.0, 0.0, 0.95), 3.88, 1.15)
            sp1 = at(chip("SOLD FOR Rs 3,000", CHALK_CYAN, size=13), -2.70, 0.55)
            sp2 = at(chip("SOLD FOR Rs 3,000", CHALK_CYAN, size=13), 3.88, 0.55)
            gain = at(chip("+20% GAIN", CHALK_GREEN, size=14), -2.70, -0.15)
            loss = at(chip("-20% LOSS", CHALK_PINK, size=14), 3.88, -0.15)
            zero = wrong_card("0%", CHALK_RED, width=1.40, height=1.00, size=20)
            zero.move_to(np.array([BOARD_CX, -0.15, 0.0]))
            zero_cross = zero.cross
            zero_cross.set_stroke(opacity=0)
            base1 = at(math_card(r"\text{CP} = \frac{3000}{1.2} = "
                                 r"\text{Rs}\,2500", CHALK_GREEN, width=3.10,
                                 height=1.00, size=20), -2.70, -1.00)
            base2 = at(math_card(r"\text{CP} = \frac{3000}{0.8} = "
                                 r"\text{Rs}\,3750", CHALK_PINK, width=3.10,
                                 height=1.00, size=20), 3.88, -1.00)
            strip = at(board_text("The two cost prices are different.", 15,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(table1, scale=0.92), FadeIn(table2, scale=0.92),
                      FadeIn(sp1, shift=UP * 0.06), FadeIn(sp2, shift=UP * 0.06),
                      run_time=0.65)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(gain, scale=0.92), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(loss, scale=0.92), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            # the tempting cancellation: the two labels head for the middle and
            # a "0%" card appears between them -- then it is stopped
            self.wait(leftover(tracker, "b3"))
            self.play(gain.animate.move_to(np.array([-1.25, -0.15, 0.0])),
                      loss.animate.move_to(np.array([2.25, -0.15, 0.0])),
                      FadeIn(zero, scale=0.92), run_time=0.65)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b4"))
            self.play(zero_cross.animate.set_stroke(opacity=1),
                      gain.animate.move_to(np.array([-2.70, -0.15, 0.0])),
                      loss.animate.move_to(np.array([3.88, -0.15, 0.0])),
                      run_time=0.70)
            self.play(FadeIn(base1, scale=0.94), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(base2, scale=0.94), FadeIn(strip, shift=UP * 0.06),
                      run_time=0.60)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: the whole transaction -- two ledgers merge into one ---------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Whole Transaction", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Add the two costs and the two selling prices.",
                                16, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            m1 = at(mini_ledger("TABLE 1", [("Cost price", "Rs 2,500"),
                                            ("Selling price", "Rs 3,000"),
                                            ("Gain", "Rs 500")], CHALK_GREEN),
                    -2.15, 0.88)
            m2 = at(mini_ledger("TABLE 2", [("Cost price", "Rs 3,750"),
                                            ("Selling price", "Rs 3,000"),
                                            ("Loss", "Rs 500")], CHALK_PINK),
                    3.15, 0.88)
            frame = ledger_frame(width=9.00, height=2.80, cy=0.10,
                                 rule_bot=-0.20)
            out1 = ledger_line("Total cost price", "Rs 6,250", 0.16, CHALK_GREEN)
            in1 = ledger_line("Total selling price", "Rs 6,000", 0.16,
                              CHALK_PINK, x_left=LED_IN_L, x_right=LED_IN_R)
            result = result_box("OVERALL: A LOSS OF Rs 250", BOARD_CX, -0.60,
                                CHALK_RED, width=5.40)
            pct = at(chalk_math(r"250 \div 6250 \times 100 = 4\%", size=21,
                                color=CHALK_RED), BOARD_CX, -1.10)
            strip = at(board_text("Plus twenty and minus twenty did not give "
                                  "zero.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            # the two item ledgers are physically drawn together and the one
            # total ledger takes their place
            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(m1, scale=0.93), FadeIn(m2, scale=0.93),
                      run_time=0.60)
            self.play(m1.animate.move_to(np.array([-1.85, 0.88, 0.0])),
                      m2.animate.move_to(np.array([2.85, 0.88, 0.0])),
                      run_time=0.55)
            self.play(FadeOut(m1), FadeOut(m2), FadeIn(frame, scale=0.97),
                      FadeIn(out1, shift=RIGHT * 0.06), run_time=0.65)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(in1, shift=RIGHT * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(result, scale=0.94), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(pct, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, result)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: the decision process ---------------------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Decision Process", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Five steps, every time.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            r1 = at(self.answer_row("1", "FIND THE PURCHASE PRICE",
                                    "what was paid for the item", CHALK_CYAN,
                                    height=0.50), BOARD_CX, 1.50)
            r2 = at(self.answer_row("2", "ADD THE OVERHEADS",
                                    "transport, repair, labour, storage",
                                    CHALK_YELLOW, height=0.50),
                    BOARD_CX, 0.88)
            r3 = at(self.answer_row("3", "FIND THE TOTAL SELLING PRICE",
                                    "what the buyer paid you", CHALK_GREEN,
                                    height=0.50), BOARD_CX, 0.26)
            r4 = at(self.answer_row("4", "COMPARE THE TWO",
                                    "SP bigger: profit, smaller: loss",
                                    CHALK_PINK, height=0.50), BOARD_CX, -0.36)
            r5 = at(self.answer_row("5", "DIVIDE BY THE COST PRICE",
                                    "then multiply by one hundred", CHALK_AMBER,
                                    height=0.50), BOARD_CX, -0.98)
            strip = at(board_text("For several items, compare the totals.", 15,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

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

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(r5, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: spoiled stock still costs ----------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("Spoiled Stock Still Costs", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Overheads count even for what is not sold.", 16,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            frame = ledger_frame()
            bananas = at(banana_bunch(0.0, 0.0, 0.62, CHALK_YELLOW), -3.35, 1.40)
            spoil = at(chip("SPOILED, NOT FREE", CHALK_RED, size=12), 3.35, 1.36)
            out1 = ledger_line("Bananas bought", "Rs 1,250", LED_ROW_Y[0],
                               CHALK_CYAN)
            out2 = ledger_line("Transport", "Rs 250", LED_ROW_Y[1], CHALK_YELLOW)
            total = total_box("TOTAL COST PRICE = Rs 1,500")
            in1 = ledger_line("Dozens sold", "Rs 1,575", LED_ROW_Y[0],
                              CHALK_PINK, x_left=LED_IN_L, x_right=LED_IN_R)
            in2 = ledger_line("Profit", "Rs 75", LED_ROW_Y[1], CHALK_GREEN,
                              x_left=LED_IN_L, x_right=LED_IN_R)
            in3 = at(chalk_math(r"75 \div 1500 \times 100 = 5\%", size=21,
                                color=CHALK_GREEN), LED_IN_CX, LED_ROW_Y[2])
            strip = at(board_text("Spoiled bananas are still part of the cost "
                                  "price.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(frame, scale=0.97), FadeIn(bananas, scale=0.92),
                      run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(out1, shift=RIGHT * 0.06),
                      FadeIn(out2, shift=RIGHT * 0.06),
                      FadeIn(total, scale=0.94), run_time=0.65)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(in1, shift=RIGHT * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(spoil, scale=0.92), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(in2, shift=RIGHT * 0.06),
                      FadeIn(in3, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, total)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 9: your turn (questions, the silent clock, then the answers) ---
    def beat_s9(self) -> None:
        with self.voiceover(text=NARRATION["s9q"]) as tracker:
            self.reset_board()

            heading = at(board_text("YOUR TURN", 26, CHALK_PINK, "BOLD"),
                         BOARD_CX, 2.78)
            sub = at(board_text("Two problems.", 16, CHALK_WHITE, "BOLD"),
                     BOARD_CX, 2.20)

            qa = at(self.q_card("A bicycle",
                                ["BOUGHT Rs 4,000",
                                 "TRANSPORT Rs 200, REPAIR Rs 300",
                                 "SOLD Rs 5,400"], CHALK_GREEN), -2.70, 0.90)
            qb = at(self.q_card("Find",
                                ["THE TOTAL COST PRICE",
                                 "THE PROFIT",
                                 "THE PROFIT PERCENT"], CHALK_YELLOW),
                    3.70, 0.90)
            qc = at(self.q_card("Two television sets",
                                ["EACH SOLD Rs 9,900",
                                 "ONE +10%, ONE -10%",
                                 "DID THEY CANCEL?"], CHALK_CYAN),
                    -2.70, -1.00)
            qd = at(self.q_card("Find",
                                ["BOTH COST PRICES",
                                 "TOTAL CP, TOTAL SP",
                                 "OVERALL PROFIT OR LOSS"], CHALK_PINK),
                    3.70, -1.00)

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
            a1 = at(self.answer_row("A", "TOTAL CP = Rs 4,500",
                                    "4,000 + 200 + 300", CHALK_GREEN),
                    BOARD_CX, 1.58)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "PROFIT = Rs 900",
                                    "5,400 - 4,500; that is 20%", CHALK_YELLOW),
                    BOARD_CX, 0.78)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "FIRST TV: CP = Rs 9,000",
                                    "9,900 / 1.1", CHALK_CYAN),
                    BOARD_CX, -0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "SECOND TV: CP = Rs 11,000",
                                    "total loss Rs 200 = 1%", CHALK_PINK),
                    BOARD_CX, -0.82)
            self.play(FadeIn(a4, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, a4)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap and the spoken thank-you ----------------------------
    def beat_s10(self) -> None:
        with self.voiceover(text=NARRATION["s10"]) as tracker:
            self.reset_board()

            heading = at(board_text("Purchase · Overheads · Percentage", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)

            r1 = at(self.answer_row("1", "ADD THE OVERHEADS",
                                    "purchase + transport + repair", CHALK_GREEN),
                    BOARD_CX, 1.48)
            r2 = at(self.answer_row("2", "COMPARE WITH THE SP",
                                    "bigger: profit, smaller: loss",
                                    CHALK_CYAN), BOARD_CX, 0.72)
            r3 = at(self.answer_row("3", "PERCENT ON THE COST PRICE",
                                    "divide by CP, not by SP", CHALK_YELLOW),
                    BOARD_CX, -0.04)
            r4 = at(self.answer_row("4", "MANY ITEMS",
                                    "compare total cost with total SP",
                                    CHALK_AMBER), BOARD_CX, -0.80)
            strip = at(board_text("The purchase price alone is never the real "
                                  "cost.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)
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
            # the strip is written on its own bookmark as the voice says "The
            # purchase price alone is never the real cost.", and only the
            # bookmark in front of "Thank you for watching," clears the board
            # and brings in the card.
            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeOut(heading), FadeOut(r1), FadeOut(r2), FadeOut(r3),
                      FadeOut(r4), FadeOut(strip), run_time=0.35)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.35)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.30)
            # 0.60 rather than 0.90: this piece's own audio runs the closing
            # sentence a little faster than the draft SRT assumes, and this
            # keeps every piece at 0.00 s stretch
            self.closing(tracker, thanks, run_time=0.60)
            self._capture_srt(tracker)

        self.wait(END_HOLD)

"""
Simple Interest vs. Compound Interest: Deriving the Compound Interest Formula
Story-mode chalkboard lesson (Class 8 Maths, Chapter 5: Comparing Quantities
using Proportion, Storymode 02).

LLM KEY / FUNCTION NAME: simple_vs_compound_interest_formula

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
  - All money is written "Rs" (the rupee glyph is not in the board font).

The defining visual is TWO MONEY LADDERS: on Ramesh's simple-interest ladder a
drawn padlock fixes the principal block while identical interest blocks stack
beside it; on Sreenu's compound ladder the principal and its interest merge into
one block that slides down to become the next year's principal, from which a
larger interest block is cut.  The ladders then give way to algebra, transformed
with TransformMatchingTex so P and the growth factor stay continuous through
P + PR/100 -> P(1 + R/100) -> P(1 + R/100)^2 -> P(1 + R/100)^n.

Title + 10 scenes:
  0. Title: the same Rs 100 at the same 10% for the same 2 years gives Rs 120 by
     one method and Rs 121 by the other -- where did the extra Re 1 come from?
  1. Simple interest: the interest is always on the ORIGINAL principal, so it is
     Rs 10 every year; SI = PTR/100, and Rs 2,500 at 12% for 3 years gives
     Rs 900.
  2. Compound interest: each new amount becomes the next principal, so year two
     earns Rs 11 and the amount is Rs 121 -- the extra rupee is interest on the
     first year's interest.
  3. The one-period growth factor: A1 = P + PR/100 = P(1 + R/100).
  4. Year two: the same factor multiplies again, giving A2 = P(1 + R/100)^2.
  5. n years: one factor per year compresses into a power, A = P(1 + R/100)^n --
     and the exponent counts the growth periods.
  6. The formula gives the AMOUNT, so CI = A - P = P(1 + R/100)^n - P.
  7. Apply it: Rs 5,000 at 8% for 2 years gives Rs 5,832, so CI is Rs 832.
  8. The two ladders side by side, and why SI and CI agree after one period.
  9. Your turn: three exercises and the quick check, after the series' centred
     ten-second THINK clock.
 10. Recap of the derivation, and the spoken thank-you card.
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


# (this section is spliced into a head whose own imports omit Arc and Ellipse;
#  Dot, Circle, Line, Polygon, RoundedRectangle, VGroup, DEGREES and np are
#  already imported by the head)
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

# The two content bands.  The band centre is where a row of cards is pinned.
BAND_A = 0.72            # the upper band (ladders, formula rows)
BAND_B = -0.45           # the lower band (results, secondary rows)

PANEL_FILL = "#16202B"
CARD_W = 3.60            # the account card width
CARD_H = 1.36            # the account card height (three stacked lines)
CHIP_H = 0.50            # every small label box
LADDER_W = 2.30          # a big ladder block
LADDER_H = 0.62
ROW_STEP = 0.72
SMALL_W = 1.86           # a small ladder block (the side-by-side comparison)
SMALL_H = 0.42
SMALL_STEP = 0.55
MARK_SIZE = 18
COIN_R = 0.17

# The figures this video works with.  The textbook example is the Rs 2,500 one
# for simple interest; the compound-interest figures are the video's own, and
# the challenge amounts are marked on screen as exercises.
PRINCIPAL = 100
RATE = 10
SI_EXAMPLE = (2500, 12, 3, 900, 3400)      # P, R, T, SI, amount
CI_EXAMPLE = (5000, 8, 2, 5832, 832)       # P, R, n, amount, CI
CHECK_A = (2000, 5, 3, 300, 2300)          # P, R, T, SI, amount
CHECK_B = (5000, 10, 2, 6050, 1050)        # P, R, n, amount, CI


# ---------------------------------------------------------------- furniture --
def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


def row_centres(half_widths, gap, cx=BOARD_CX):
    """x centres for a row of elements whose ink is `gap` apart.

    The row's combined ink is centred on `cx` (the green board's centre line)
    and the elements of a row are not equally wide, so equal centre spacing is
    NOT equal spacing on the board: this returns the centres that leave exactly
    `gap` units of clear air between neighbours.
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


def coin_stack(cx, cy, n=3, scale=1.0, color=CHALK_YELLOW):
    """A stack of rupee coins: filled discs with thickness, drawn bottom-up."""
    discs = VGroup()
    for i in range(n):
        e = Ellipse(width=0.40 * scale, height=0.14 * scale,
                    stroke_color=color, stroke_width=1.4,
                    fill_color=color, fill_opacity=0.38)
        e.move_to(np.array([cx, cy + 0.065 * i * scale, 0.0]))
        discs.add(e)
    return discs


def rupee_note(cx, cy, scale=1.0, color=CHALK_YELLOW):
    """A drawn rupee note: a filled note with its own printed band."""
    body = RoundedRectangle(corner_radius=0.05, width=0.62 * scale,
                            height=0.36 * scale, stroke_color=color,
                            stroke_width=1.6, fill_color=color,
                            fill_opacity=0.30)
    body.move_to(np.array([cx, cy, 0.0]))
    band = Circle(radius=0.09 * scale, stroke_color=color, stroke_width=1.2,
                  fill_color=color, fill_opacity=0.30)
    band.move_to(np.array([cx, cy, 0.0]))
    return VGroup(body, band)


def method_card(name, method, result, color=CHALK_GREEN, kind="coins",
                width=CARD_W, height=CARD_H, name_size=15, line_size=14,
                result_size=14, buff=0.26):
    """One friend's method card: who, which interest, and the money it makes.

    The money (filled coins or a filled note) sits in the card's left margin, so
    the two friends read as two money handlers and not just two rows of words.
    The card's three lines are held `buff` apart -- 0.26, the tightest the
    clearance audit allows two texts to come is 0.22.
    """
    box = panel(width, height, color)
    icon = (coin_stack(-width / 2 + 0.40, -0.14, 3, 0.95, color)
            if kind == "coins"
            else rupee_note(-width / 2 + 0.40, -0.02, 1.05, color))
    head = board_text(name, name_size, color, "BOLD")
    line = board_text(method, line_size, CHALK_WHITE, "BOLD")
    res = board_text(result, result_size, CHALK_YELLOW, "BOLD")
    txt = VGroup(head, line, res).arrange(DOWN, buff=buff, aligned_edge=LEFT)
    txt.move_to(np.array([-width / 2 + 0.92 + txt.width / 2.0, 0.0, 0.0]))
    grp = VGroup(box, icon, txt)
    grp.box, grp.head, grp.line, grp.result, grp.icon = box, head, line, res, icon
    return grp


def padlock(cx, cy, scale=1.0, color=CHALK_RED):
    """The drawn padlock that fixes a simple-interest principal.

    A filled body, a shackle arc over it and a keyhole dot.  It is always
    returned inside the same VGroup as the block it locks, so the audit never
    reads its strokes as a line running into a card.
    """
    body = RoundedRectangle(corner_radius=0.05, width=0.40 * scale,
                            height=0.30 * scale, stroke_color=color,
                            stroke_width=2.0, fill_color=PANEL_FILL,
                            fill_opacity=0.92)
    body.move_to(np.array([cx, cy - 0.05 * scale, 0.0]))
    shackle = Arc(radius=0.12 * scale, start_angle=0.0, angle=PI,
                  stroke_color=color, stroke_width=2.0)
    shackle.move_to(np.array([cx, cy + 0.10 * scale, 0.0]))
    key = Dot(radius=0.03 * scale, color=color).move_to(
        np.array([cx, cy - 0.05 * scale, 0.0]))
    return VGroup(body, shackle, key)


def block_row(label, color=CHALK_GREEN, width=LADDER_W, height=LADDER_H,
              size=13, opacity=0.42, lock_dx=None, text_color=CHALK_WHITE):
    """One solid block of a money ladder, carrying its own amount.

    `lock_dx` is the padlock's x offset from the block's centre (None = no
    padlock).  A lock inside the block's left margin shifts the amount to the
    right; a lock placed outside the block leaves the amount centred.  The
    label is sized so that no word ever touches its own block's edge, and the
    padlock is a member of this block's own VGroup.
    """
    box = RoundedRectangle(corner_radius=0.08, width=width, height=height,
                           stroke_color=color, stroke_width=1.9,
                           fill_color=color, fill_opacity=opacity)
    lab = board_text(label, size, text_color, "BOLD")
    parts = [box]
    inside = lock_dx is not None and lock_dx > -width / 2.0 + 0.06
    if lock_dx is not None:
        parts.append(padlock(lock_dx, 0.0,
                             0.86 * (0.6 + 0.4 * height / LADDER_H)))
    if inside:
        lab.move_to(box.get_center() + RIGHT * 0.28)
    else:
        lab.move_to(box.get_center())
    parts.append(lab)
    grp = VGroup(*parts)
    grp.box, grp.label = box, lab
    return grp


def ladder(x, rows, width=LADDER_W, height=LADDER_H, step=ROW_STEP, size=13,
           y0=-0.42):
    """A column of money blocks, bottom row first.

    `rows` is a list of (label, colour, lock_dx or None).  The blocks are
    returned separately (not as one group) so a single block can be animated --
    merged, slid down, or indicated -- on its own.
    """
    out = []
    for i, row in enumerate(rows):
        label, color = row[0], row[1]
        lock_dx = row[2] if len(row) > 2 else None
        h = row[3] if len(row) > 3 else height
        w = row[4] if len(row) > 4 else width
        out.append(at(block_row(label, color, w, h, size, lock_dx=lock_dx),
                      x, y0 + i * step))
    return out


def factor_card(color=CHALK_AMBER, width=2.30, height=0.78, size=24):
    """The one-period growth factor, boxed: the object that multiplies."""
    box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                           stroke_color=color, stroke_width=2.1,
                           fill_color=PANEL_FILL, fill_opacity=0.55)
    tex = chalk_math(r"\left(1+\frac{R}{100}\right)", size=size, color=color)
    tex.move_to(box.get_center())
    grp = VGroup(box, tex)
    grp.box, grp.tex = box, tex
    return grp


def note_card(head, lines, color=CHALK_CYAN, width=3.40, height=1.05,
              head_size=15, line_size=13, buff=0.28):
    """A card with a bold head line and one or two body lines under it.

    The head and the body are laid out as ONE stack, so the gap between the head
    and the first body line is the full 0.28 the clearance audit asks for.
    """
    box = panel(width, height, color)
    parts = [board_text(head, head_size, color, "BOLD")]
    parts += [board_text(line, line_size, CHALK_WHITE, "BOLD")
              for line in lines]
    txt = VGroup(*parts).arrange(DOWN, buff=buff)
    txt.move_to(box.get_center())
    grp = VGroup(box, txt)
    grp.box, grp.head, grp.body = box, parts[0], VGroup(*parts[1:])
    return grp


def cross_out(mob, color=CHALK_RED, pad=0.10):
    """A drawn cross over a mobject (Segoe Print has no cross glyph).

    The cross is returned as part of a VGroup with its target by the caller, so
    the two are one board object and the audit never reads the strokes as a
    line running through somebody else's card.
    """
    x0, y0 = mob.get_left()[0] - pad, mob.get_bottom()[1] - pad
    x1, y1 = mob.get_right()[0] + pad, mob.get_top()[1] + pad
    return VGroup(
        Line(np.array([x0, y0, 0.0]), np.array([x1, y1, 0.0]),
             stroke_color=color, stroke_width=4.2),
        Line(np.array([x0, y1, 0.0]), np.array([x1, y0, 0.0]),
             stroke_color=color, stroke_width=4.2))


def wrong_card(text, color=CHALK_RED, width=3.10, height=1.05, size=15):
    """A card holding a WRONG statement, with a drawn cross over it.

    The cross occupies the card's top half and the statement its bottom half, so
    the strike-through is unmistakable yet never comes within the 0.04 units the
    audit allows between a stroke and the lettering.  The whole card is ONE
    board object, so the strokes are never read as a line running into a box.
    """
    box = panel(width, height, color, opacity=0.7)
    cross = VGroup(
        Line(np.array([-width / 2 + 0.60, 0.14, 0.0]),
             np.array([-width / 2 + 1.10, 0.50, 0.0]),
             stroke_color=color, stroke_width=4.2),
        Line(np.array([-width / 2 + 0.60, 0.50, 0.0]),
             np.array([-width / 2 + 1.10, 0.14, 0.0]),
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
        "Ramesh and Sreenu lent the same money to two different borrowers. "
        "<bookmark mark='b0'/>Ramesh lent one hundred rupees at ten percent for "
        "two years, and got back one hundred and twenty rupees. <bookmark "
        "mark='b1'/>Sreenu lent one hundred rupees at the same ten percent, for "
        "the same two years, and got back one hundred and twenty one rupees. "
        "<bookmark mark='b2'/>Same principal, same rate, same time, and yet one "
        "rupee more. <bookmark mark='b3'/>Where did that extra rupee come from? "
        "<bookmark mark='b4'/>The two friends used two different methods. "
        "<bookmark mark='b5'/>Ramesh's method is simple interest, and Sreenu's "
        "method is compound interest."
    ),
    "s1": (
        "Ramesh uses simple interest. <bookmark mark='b0'/>The interest is "
        "always calculated on the original principal, so the base never "
        "changes. <bookmark mark='b1'/>One hundred rupees at ten percent gives "
        "ten rupees of interest every year. <bookmark mark='b2'/>Year one pays "
        "ten rupees, and year two pays ten rupees again, because the base is "
        "still the original one hundred. <bookmark mark='b3'/>Ten plus ten is "
        "twenty, so the amount is one hundred plus twenty, that is one hundred "
        "and twenty rupees. <bookmark mark='b4'/>Simple interest is P times T "
        "times R, divided by one hundred. <bookmark mark='b5'/>For example, two "
        "thousand five hundred rupees at twelve percent for three years gives "
        "nine hundred rupees of interest, <bookmark mark='b6'/>and the amount is "
        "three thousand four hundred rupees."
    ),
    "s2": (
        "Sreenu uses compound interest. <bookmark mark='b0'/>Here each new "
        "amount becomes the next principal, so the base itself grows. "
        "<bookmark mark='b1'/>In year one, ten percent of one hundred is ten "
        "rupees, so the amount is one hundred and ten rupees. <bookmark "
        "mark='b2'/>That one hundred and ten rupees is now the principal for "
        "year two. <bookmark mark='b3'/>In year two, ten percent of one hundred "
        "and ten is eleven rupees, so the amount becomes one hundred and twenty "
        "one rupees. <bookmark mark='b4'/>The second interest is eleven rupees, "
        "one rupee more than the first. <bookmark mark='b5'/>That extra rupee "
        "is ten percent of the first year's ten rupees of interest: <bookmark "
        "mark='b6'/>the interest itself earned interest."
    ),
    "s3": (
        "Watch one period only. <bookmark mark='b0'/>In one period the amount "
        "is the principal plus the interest on it: A one equals P plus P R over "
        "one hundred. <bookmark mark='b1'/>Take P outside the bracket, and the "
        "same amount is P times one plus R over one hundred. <bookmark "
        "mark='b2'/>The bracket, one plus R over one hundred, is the one period "
        "growth factor. <bookmark mark='b3'/>Whatever the principal is, "
        "<bookmark mark='b4'/>one period multiplies it by that same factor."
    ),
    "s4": (
        "Now the second year. <bookmark mark='b0'/>The amount from year one "
        "becomes the principal for year two. <bookmark mark='b1'/>So the same "
        "growth factor multiplies again. <bookmark mark='b2'/>A two equals P "
        "times one plus R over one hundred, times one plus R over one hundred "
        "once more. <bookmark mark='b3'/>Which is P into the square of one plus "
        "R over one hundred. <bookmark mark='b4'/>Two years means two factors, "
        "and two factors compress into one single power. <bookmark "
        "mark='b5'/>That power is the square, and every extra year adds one "
        "more."
    ),
    "s5": (
        "One factor for every year. <bookmark mark='b0'/>Year one multiplies by "
        "the growth factor, year two multiplies again, year three multiplies "
        "again, and so on up to year n. <bookmark mark='b1'/>Repeated "
        "multiplication by the same number compresses into a power. <bookmark "
        "mark='b2'/>So the amount after n years is A equals P times one plus R "
        "over one hundred, raised to the power n. <bookmark mark='b3'/>The "
        "exponent n is not a decoration. <bookmark mark='b4'/>It is the number "
        "of growth periods."
    ),
    "s6": (
        "Careful: this formula gives the amount. <bookmark mark='b0'/>The amount "
        "is the principal plus the interest, so it is not the interest itself. "
        "<bookmark mark='b1'/>The compound interest is the amount minus the "
        "principal. <bookmark mark='b2'/>So C I equals A minus P, which is P "
        "times one plus R over one hundred to the power n, minus P. <bookmark "
        "mark='b3'/>For one hundred rupees at ten percent for two years, the "
        "amount is one hundred and twenty one rupees, <bookmark mark='b4'/>and "
        "the interest is twenty one rupees."
    ),
    "s7": (
        "Let us use it with real numbers. Take P equals five thousand rupees, R "
        "equals eight percent, and n equals two years. <bookmark mark='b0'/>One "
        "plus eight over one hundred is one point zero eight, so the amount is "
        "five thousand times one point zero eight squared. <bookmark "
        "mark='b1'/>That is five thousand eight hundred and thirty two rupees. "
        "<bookmark mark='b2'/>The compound interest is the amount minus the "
        "principal. <bookmark mark='b3'/>Five thousand eight hundred and thirty "
        "two minus five thousand is eight hundred and thirty two rupees. "
        "<bookmark mark='b4'/>So the compound interest is eight hundred and "
        "thirty two rupees, <bookmark mark='b5'/>and not five thousand eight "
        "hundred and thirty two."
    ),
    "s8": (
        "Put the two ladders side by side. <bookmark mark='b0'/>On the simple "
        "interest ladder the principal stays locked at one hundred, so both "
        "years add the same ten rupees, and the amount is one hundred and "
        "twenty. <bookmark mark='b1'/>On the compound ladder the first year "
        "makes one hundred and ten, and that becomes the base, so the second "
        "year adds eleven rupees, and the amount is one hundred and twenty one. "
        "<bookmark mark='b2'/>Now look at the first year: both ladders add the "
        "same ten rupees, because both started from the original principal. "
        "<bookmark mark='b3'/>After that, simple interest keeps adding the same "
        "block, <bookmark mark='b4'/>while compound interest adds a bigger "
        "block, because its base grows."
    ),
    "s9q": (
        "Your turn. Four quick checks. <bookmark mark='b0'/>A: simple interest "
        "on two thousand rupees at five percent for three years. <bookmark "
        "mark='b1'/>B: compound interest on five thousand rupees at ten percent "
        "for two years. <bookmark mark='b2'/>C: every year the interest is "
        "calculated on five thousand rupees. <bookmark mark='b3'/>And next "
        "year's interest is calculated on the previous year's amount. <bookmark "
        "mark='b4'/>D: after the first year, are simple and compound interest "
        "different?"
    ),
    "s9a": (
        "Let us check the four answers. <bookmark mark='b0'/>A: two thousand "
        "times three times five, divided by one hundred, is three hundred "
        "rupees, so the amount is two thousand three hundred. <bookmark "
        "mark='b1'/>B: five thousand times one point one squared is six thousand "
        "and fifty, so the compound interest is one thousand and fifty. "
        "<bookmark mark='b2'/>C: interest on five thousand rupees every year is "
        "simple interest, and interest on the previous year's amount is compound "
        "interest. <bookmark mark='b3'/>D: no, after the first period they are "
        "the same, because both used the original principal."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>Simple interest keeps the original "
        "principal as the base, so every year adds the same interest. <bookmark "
        "mark='b1'/>Compound interest lets each new amount become the next base, "
        "so the interest itself grows. <bookmark mark='b2'/>We derived it: A "
        "one, then A two, then A equals P times one plus R over one hundred, to "
        "the power n. <bookmark mark='b3'/>And the formula gives the amount, so "
        "the compound interest is A minus P. <bookmark mark='b4'/>Simple stays "
        "on the original base; compound grows on the new base. <bookmark "
        "mark='b5'/>Thank you for watching, <bookmark mark='b6'/>and see you in "
        "the next lesson."
    ),
}


class SimpleVsCompoundInterestFormulaStory(VoiceoverScene):
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
        out_dir = _HERE / "media" / "videos" / "simple_vs_compound_interest_formula"
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
    # Simple Interest vs. Compound Interest: Deriving the Compound Interest
    # Formula (Class 8 Maths, Chapter 5, Storymode 02).
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
    #   * every row of cards is centred on BOARD_CX (`hrow`), and two texts never
    #     come closer than the 0.22 units the clearance audit asks for -- which
    #     is why every card holds its own lines 0.26 or more apart;
    #   * the SIMPLE-INTEREST ladder keeps its principal block LOCKED with the
    #     drawn padlock: P + I never becomes the next principal there, or the
    #     ladder would accidentally depict compound interest;
    #   * in the COMPOUND ladder the amount really does become the next
    #     principal: the P and I blocks are replaced in ONE play by the merged
    #     A1 block, which then slides down into the principal slot;
    #   * a drawn cross always lives in the same VGroup as the card it strikes
    #     through (otherwise the clearance audit reads the strokes as a line
    #     running into a card);
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

    def method_row(self, y=0.50):
        """Ramesh's and Sreenu's account cards, side by side."""
        ca, cb = row_centres((CARD_W / 2, CARD_W / 2), 0.50)
        a = at(method_card("RAMESH'S METHOD", "Simple Interest",
                           "Rs 100 gives Rs 120", CHALK_GREEN, "coins"), ca, y)
        b = at(method_card("SREENU'S METHOD", "Compound Interest",
                           "Rs 100 gives Rs 121", CHALK_PINK, "note"), cb, y)
        return a, b

    def q_card(self, title, pict, color=CHALK_CYAN, width=3.10, pad=0.12,
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

    # -- Scene 0: title -- the same money, two methods, two answers ----------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = at(board_text("Same Money, Two Methods", 24, CHALK_PINK,
                                  "BOLD"), BOARD_CX, 2.06)
            sub = at(board_text("Rs 100 for 2 years at 10%: Rs 120 or Rs 121?",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, 1.40)

            a_card, b_card = self.method_row(y=0.45)
            same = at(chip("SAME PRINCIPAL · SAME RATE · SAME TIME",
                           CHALK_CYAN, 14), BOARD_CX, -0.60)
            banner = at(board_text("WHERE DID THE EXTRA Re 1 COME FROM?", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Same principal, same rate, same time: one "
                                  "rupee more.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(title, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(a_card, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(b_card, shift=LEFT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(same, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(Indicate(a_card, color=CHALK_GREEN, scale_factor=1.02),
                      Indicate(b_card, color=CHALK_PINK, scale_factor=1.02),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: simple interest -- the base is locked at the principal ------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("Ramesh's Method: Simple Interest", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The interest stays on the original principal.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # the money ladder: the principal is LOCKED, and the two interest
            # blocks are identical because the base never moves
            base, i1, i2, total = ladder(
                -2.45,
                [("Principal Rs 100", CHALK_GREEN, -0.85),
                 ("Interest Rs 10", CHALK_YELLOW),
                 ("Interest Rs 10", CHALK_YELLOW),
                 ("Amount Rs 120", CHALK_CYAN)],
                height=0.54, step=0.62, size=13, y0=-0.45)

            formula = at(chalk_math(r"SI = \frac{P \times T \times R}{100}",
                                    size=24, color=CHALK_WHITE), 2.55, 1.05)
            data = at(chip("Rs 2,500 at 12% for 3 years", CHALK_AMBER, 14),
                      2.55, 0.30)
            result = at(chip("SI = Rs 900, Amount = Rs 3,400", CHALK_GREEN, 13),
                        2.55, -0.42)

            banner = at(board_text("THE SAME INTEREST EVERY YEAR", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Simple interest always uses the original "
                                  "principal.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(base, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(i1, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(i2, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(total, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(formula, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(data, shift=UP * 0.06),
                      FadeIn(result, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: compound interest -- the amount becomes the next principal --
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("Sreenu's Method: Compound Interest", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Each new amount becomes the next principal.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            p_block = at(block_row("Principal Rs 100", CHALK_GREEN),
                         -2.45, -0.45)
            i1 = at(block_row("Interest Rs 10", CHALK_YELLOW), -2.45, 0.17)
            a1 = at(block_row("Amount Rs 110", CHALK_CYAN), -2.45, -0.14)
            i2 = at(block_row("Interest Rs 11", CHALK_AMBER, width=2.60,
                              height=0.70), -2.45, 0.17)
            a2 = at(block_row("Amount Rs 121", CHALK_CYAN), -2.45, -0.14)
            slot = np.array([-2.45, -0.45, 0.0])

            y1 = at(chip("Year 1: 10% of Rs 100 = Rs 10", CHALK_GREEN, 14),
                    2.55, 0.90)
            y2 = at(chip("Year 2: 10% of Rs 110 = Rs 11", CHALK_AMBER, 14),
                    2.55, 0.18)
            more = at(chip("The second interest is Re 1 more", CHALK_PINK, 14),
                      2.55, -0.54)
            extra = at(chip("The extra Re 1 is 10% of Rs 10", CHALK_PINK, 14),
                       2.55, -0.54)

            banner = at(board_text("THE INTEREST EARNED ALSO EARNS INTEREST", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The extra rupee is interest on the first "
                                  "year's interest.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(p_block, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(i1, shift=UP * 0.06),
                      FadeIn(y1, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            # the principal and its interest MERGE into one A1 block, which then
            # slides down into the principal slot and becomes year two's base
            self.wait(leftover(tracker, "b2"))
            self.play(FadeOut(p_block, shift=UP * 0.10),
                      FadeOut(i1, shift=DOWN * 0.10),
                      FadeIn(a1, scale=1.04), run_time=0.60)
            self.play(a1.animate.move_to(slot), run_time=0.55)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(i2, scale=0.95),
                      FadeIn(y2, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeOut(a1, shift=UP * 0.10),
                      FadeOut(i2, shift=DOWN * 0.10),
                      FadeIn(a2, scale=1.04), run_time=0.60)
            self.play(a2.animate.move_to(slot), run_time=0.55)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(more, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b6"))
            self.play(Transform(more, extra),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: one period -- the growth factor -----------------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("The One-Period Growth Factor", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Amount equals principal plus the interest on "
                                "it.", 17, CHALK_WHITE, "BOLD"),
                     BOARD_CX, SUB_Y)

            p_block = at(block_row("Principal Rs 100", CHALK_GREEN, width=2.10,
                                   height=0.58, size=13), -3.15, 0.95)
            m1 = at(chalk_math(r"A_1 = P + \frac{P \times R}{100}", size=26,
                               color=CHALK_WHITE), 1.30, 0.95)
            m2 = at(chalk_math(r"A_1 = P\left(1+\frac{R}{100}\right)", size=26,
                               color=CHALK_WHITE), 1.30, 0.95)
            gf = at(factor_card(CHALK_AMBER, 2.80, 0.90, 28), 2.55, -0.30)
            tag = at(chip("ONE-PERIOD GROWTH FACTOR", CHALK_AMBER, 14),
                     -2.05, -0.30)

            banner = at(board_text("EVERY PERIOD MULTIPLIES BY THIS FACTOR", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The bracket is the one-period growth "
                                  "factor.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(p_block, shift=RIGHT * 0.10),
                      FadeIn(m1, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(TransformMatchingTex(m1, m2), run_time=0.80)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(gf, scale=0.95), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(tag, shift=UP * 0.06),
                      Indicate(p_block, color=CHALK_GREEN, scale_factor=1.04),
                      run_time=0.65)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: year two -- the same factor multiplies again ---------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Same Factor Multiplies Again", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The year-one amount is the year-two principal.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            m_a = at(chalk_math(r"A_2 = P\left(1+\frac{R}{100}\right)", size=26,
                                color=CHALK_WHITE), BOARD_CX, 1.25)
            m_b = at(chalk_math(
                r"A_2 = P\left(1+\frac{R}{100}\right)"
                r"\left(1+\frac{R}{100}\right)", size=24, color=CHALK_WHITE),
                BOARD_CX, 1.25)
            m_c = at(chalk_math(r"A_2 = P\left(1+\frac{R}{100}\right)^2", size=26,
                                color=CHALK_WHITE), BOARD_CX, 1.25)

            gf1 = at(factor_card(CHALK_GREEN, 2.30, 0.78, 24), -1.15, 0.30)
            gf2 = at(factor_card(CHALK_PINK, 2.30, 0.78, 24), 2.15, 0.30)
            times = at(chalk_math(r"\times", size=26, color=CHALK_WHITE),
                       BOARD_CX, 0.30)
            y1 = at(chip("YEAR 1", CHALK_GREEN, 12), -1.15, -0.45)
            y2 = at(chip("YEAR 2", CHALK_PINK, 12), 2.15, -0.45)

            banner = at(board_text("TWO YEARS, TWO FACTORS, ONE POWER", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The same growth factor multiplies once "
                                  "more.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(m_a, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(gf1, scale=0.95),
                      FadeIn(y1, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(times, scale=0.95), FadeIn(gf2, scale=0.95),
                      FadeIn(y2, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(TransformMatchingTex(m_a, m_b), run_time=0.75)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(TransformMatchingTex(m_b, m_c), run_time=0.75)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: n years -- repeated multiplication becomes a power ---------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("One Factor for Every Year", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Year one, year two, up to year n.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            m_a = at(chalk_math(r"A = P\left(1+\frac{R}{100}\right)^2", size=26,
                                color=CHALK_WHITE), BOARD_CX, -0.40)
            m_b = at(chalk_math(r"A = P\left(1+\frac{R}{100}\right)^n", size=26,
                                color=CHALK_YELLOW), BOARD_CX, -0.40)

            chain = self.hrow(
                chip("YEAR 1", CHALK_GREEN, 12),
                chalk_math(r"\times", size=20, color=CHALK_WHITE),
                chip("YEAR 2", CHALK_CYAN, 12),
                chalk_math(r"\times", size=20, color=CHALK_WHITE),
                chip("YEAR 3", CHALK_PINK, 12),
                chalk_math(r"\cdots", size=20, color=CHALK_WHITE),
                chip("YEAR n", CHALK_AMBER, 12), y=0.62, gap=0.26)
            note = at(chip("n = NUMBER OF GROWTH PERIODS", CHALK_AMBER, 11),
                      -2.75, -0.40)

            banner = at(board_text("ONE FACTOR EVERY YEAR MAKES A POWER", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The exponent counts the number of growth "
                                  "periods.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(m_a, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(chain, shift=UP * 0.06), run_time=0.70)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(TransformMatchingTex(m_a, m_b), run_time=0.75)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(note, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: the formula gives the AMOUNT --------------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Formula Gives the Amount", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The amount is principal plus interest.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            m_a = at(chalk_math(r"A = P\left(1+\frac{R}{100}\right)^n", size=26,
                                color=CHALK_YELLOW), BOARD_CX, 1.30)
            m_b = at(chalk_math(
                r"CI = A - P = P\left(1+\frac{R}{100}\right)^n - P", size=26,
                color=CHALK_YELLOW), BOARD_CX, 1.30)

            amount = at(block_row("Amount Rs 121", CHALK_CYAN, width=3.20,
                                  height=0.58, size=14), BOARD_CX, 0.45)
            principal = at(block_row("Principal Rs 100", CHALK_GREEN, width=2.60,
                                     height=0.56, size=14), -1.60, -0.32)
            plus = at(chalk_math("+", size=26, color=CHALK_WHITE),
                      BOARD_CX, -0.32)
            interest = at(block_row("Interest Rs 21", CHALK_AMBER, width=2.60,
                                    height=0.56, size=14), 2.60, -0.32)

            banner = at(board_text("THE FORMULA GIVES THE AMOUNT", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The formula gives the amount, not the "
                                  "interest.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(m_a, shift=UP * 0.06),
                      FadeIn(amount, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(principal, shift=RIGHT * 0.10),
                      FadeIn(plus, scale=0.95), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(interest, shift=LEFT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(TransformMatchingTex(m_a, m_b), run_time=0.80)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: applying the formula ---------------------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Apply It: Rs 5,000 at 8% for 2 Years", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Principal Rs 5,000, rate 8%, two years.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            inputs = self.hrow(chip("P = Rs 5,000", CHALK_GREEN, 14),
                               chip("R = 8%", CHALK_AMBER, 14),
                               chip("n = 2 years", CHALK_CYAN, 14),
                               y=1.32, gap=0.40)
            m_a = at(chalk_math(r"A = 5000\left(\frac{108}{100}\right)^2",
                                size=26, color=CHALK_WHITE), BOARD_CX, 0.48)
            m_b = at(chalk_math(
                r"A = 5000\left(\frac{108}{100}\right)^2 = 5832", size=26,
                color=CHALK_WHITE), BOARD_CX, 0.48)
            amount = at(chip("AMOUNT = Rs 5,832", CHALK_GREEN, 15), -1.85, -0.42)
            ci_rule = at(chip("CI = AMOUNT - PRINCIPAL", CHALK_AMBER, 14),
                         2.05, -0.42)
            ci_num = at(chip("CI = Rs 5,832 - Rs 5,000 = Rs 832", CHALK_AMBER, 13),
                        2.05, -0.42)

            banner = at(board_text("CI IS THE AMOUNT MINUS THE PRINCIPAL", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Compound interest is the amount minus the "
                                  "principal.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(inputs, shift=UP * 0.06),
                      FadeIn(m_a, shift=UP * 0.06), run_time=0.65)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(TransformMatchingTex(m_a, m_b), run_time=0.70)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(amount, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(ci_rule, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(Transform(ci_rule, ci_num), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the two ladders side by side --------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("Simple and Compound Side by Side", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("One base stays locked, the other grows.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            head_l = at(board_text("SIMPLE INTEREST", 13, CHALK_GREEN, "BOLD"),
                        -2.40, 1.68)
            head_r = at(board_text("COMPOUND INTEREST", 13, CHALK_PINK, "BOLD"),
                        2.90, 1.68)
            sy = (-0.50, 0.05, 0.60, 1.15)

            s_base = at(block_row("Principal Rs 100", CHALK_GREEN, SMALL_W,
                                  SMALL_H, 12, lock_dx=-SMALL_W / 2 - 0.14),
                        -2.40, sy[0])
            s_i1 = at(block_row("Interest Rs 10", CHALK_YELLOW, SMALL_W,
                                SMALL_H, 12), -2.40, sy[1])
            s_i2 = at(block_row("Interest Rs 10", CHALK_YELLOW, SMALL_W,
                                SMALL_H, 12), -2.40, sy[2])
            s_amt = at(block_row("Amount Rs 120", CHALK_CYAN, SMALL_W, SMALL_H,
                                 12), -2.40, sy[3])

            c_base = at(block_row("Principal Rs 100", CHALK_GREEN, SMALL_W,
                                  SMALL_H, 12), 2.90, sy[0])
            c_new = at(block_row("Base Rs 110", CHALK_CYAN, SMALL_W, SMALL_H,
                                 12), 2.90, sy[1])
            c_i2 = at(block_row("Interest Rs 11", CHALK_AMBER, 2.06, 0.50, 12),
                      2.90, sy[2])
            c_amt = at(block_row("Amount Rs 121", CHALK_PINK, SMALL_W, SMALL_H,
                                 12), 2.90, sy[3])

            mid = at(chip("YEAR 1: BOTH ADD Rs 10", CHALK_YELLOW, 12),
                     BOARD_CX, sy[1])
            banner = at(board_text("AFTER ONE YEAR SI AND CI ARE THE SAME", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The base changes only from the second year "
                                  "on.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.05)
                                    for m in (s_base, s_i1, s_i2, s_amt)],
                                  lag_ratio=0.18),
                      FadeIn(head_l, shift=UP * 0.06), run_time=0.95)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.05)
                                    for m in (c_base, c_new, c_i2, c_amt)],
                                  lag_ratio=0.18),
                      FadeIn(head_r, shift=UP * 0.06), run_time=0.95)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(mid, scale=0.92), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(Indicate(s_i1, color=CHALK_YELLOW, scale_factor=1.06),
                      Indicate(s_i2, color=CHALK_YELLOW, scale_factor=1.06),
                      run_time=0.70)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(banner, shift=UP * 0.06),
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

            pic_a = chalk_math(r"P = 2000,\ R = 5\%,\ T = 3", size=18,
                               color=CHALK_GREEN)
            pic_b = chalk_math(r"P = 5000,\ R = 10\%,\ n = 2", size=18,
                               color=CHALK_CYAN)
            pic_c = VGroup(
                board_text("on Rs 5,000 every year", 11, CHALK_AMBER, "BOLD"),
                board_text("on last year's amount", 11, CHALK_AMBER,
                           "BOLD")).arrange(DOWN, buff=0.24)
            pic_d = chalk_math(r"SI \;=\; CI", size=20, color=CHALK_PINK)

            qa = at(self.q_card("A · Simple interest", pic_a, CHALK_GREEN),
                    -2.75, 0.95)
            qb = at(self.q_card("B · Compound interest", pic_b, CHALK_CYAN),
                    3.75, 0.95)
            qc = at(self.q_card("C · Which method?", pic_c, CHALK_AMBER),
                    -2.75, -1.10)
            qd = at(self.q_card("D · After year one?", pic_d, CHALK_PINK),
                    3.75, -1.10)

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
            a1 = at(self.answer_row("A", "SI = Rs 300",
                                    "amount = Rs 2,300", CHALK_GREEN),
                    BOARD_CX, 1.62)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "A = Rs 6,050",
                                    "CI = Rs 1,050", CHALK_CYAN),
                    BOARD_CX, 0.82)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "Rs 5,000 each year is SI",
                                    "on the last amount is CI", CHALK_AMBER),
                    BOARD_CX, 0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "No, they match",
                                    "one period, same principal", CHALK_PINK),
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

            heading = at(board_text("Simple · Compound · Growth", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)

            r1 = at(self.answer_row("1", "SIMPLE INTEREST",
                                    "the base stays the original principal",
                                    CHALK_GREEN), BOARD_CX, 1.48)
            r2 = at(self.answer_row("2", "COMPOUND INTEREST",
                                    "the amount becomes the next base",
                                    CHALK_CYAN), BOARD_CX, 0.72)
            r3 = at(self.answer_row("3", "DERIVATION",
                                    "A1, then A2, then A = P(1+R/100)^n",
                                    CHALK_YELLOW), BOARD_CX, -0.04)
            r4 = at(self.answer_row("4", "COMPOUND INTEREST",
                                    "CI = A - P: amount minus principal",
                                    CHALK_AMBER), BOARD_CX, -0.80)
            strip = at(board_text("Simple stays on the original base; compound "
                                  "grows on the new base.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)
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
            # the strip is written on its own bookmark as the voice says "Simple
            # stays on the original base; compound grows on the new base.", and
            # only the bookmark in front of "Thank you for watching," clears the
            # board and brings in the card.
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

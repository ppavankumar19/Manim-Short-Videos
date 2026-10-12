"""
Sales Tax, VAT & GST Calculations: Determining Original Prices and Total Bills
Story-mode chalkboard lesson (Class 8 Maths, Chapter 5: Comparing Quantities
using Proportion, Storymode 03).

LLM KEY / FUNCTION NAME: sales_tax_vat_and_gst_calculations

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

The defining visual is THE BILL BAR AND ITS TAX LAYER: one bar is 100% of the
base price, a translucent tax layer descends from above and attaches flush
against its right end, and the two then merge into the (100 + r)% total while a
drawn receipt grows beside them.  The reverse direction is a 118% bar whose 18%
layer is marked, then left behind as the bar shrinks back to the 100% base, and
the GST split is one tax block physically halving into CGST and SGST.  Shoes, a
medical-shop receipt, goods-and-services icons, a two-lane decision board and
an error detector with drawn crosses complete the kit.

The arithmetic is one model throughout: base price + percentage tax = bill.
Sales tax, VAT and GST are historical/textbook examples here, never current tax
advice, and the CGST/SGST equal split is framed as the textbook's worked case.

Title + 10 scenes:
  0. Title card: the tag is not the bill -- shoes at Rs 450 plus 6% tax.
  1. A tax is a percentage increase: the original is 100% and the bill is
     (100 + r)%, so the bill bar grows a tax layer.
  2. Sales tax on Rs 450 at 6%: tax Rs 27, bill Rs 477, or 1.06 x 450.
  3. A VAT-inclusive medical bill: Rs 354.45 plus 5% VAT of Rs 17.72 gives
     Rs 372.18 -- and the historical rates are flagged as examples.
  4. GST uses the same structure: Rs 1,000 plus 5% GST of Rs 50 is Rs 1,050.
  5. Working backward: a Rs 2,360 bill including 18% GST is 118%, so the base
     is 2,360 x 100/118 = Rs 2,000 and the tax is Rs 360.
  6. The textbook's CGST/SGST split: Rs 360 halves into Rs 180 and Rs 180.
  7. Forward or backward: a two-lane decision board, and tax kept separate
     from discount.
  8. The classic error: the rate applied to the tax-added bill instead of the
     base, struck through with a drawn cross.
  9. Your turn: four checks after the series' centred ten-second THINK clock.
 10. Recap: the four formulas -- and the spoken thank-you card.
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

# The three content lines.  ROW_A carries the diagram (the bill bar and the
# drawn items), ROW_B the numbers worked under it and ROW_C the rule chip above
# the banner.  The rows are set so that no two texts come within the 0.22 units
# the clearance audit asks for, including the banner text sitting at -1.15.
ROW_A = 0.90
ROW_B = 0.04
ROW_C = -0.62

PANEL_FILL = "#16202B"
CHIP_H = 0.50
CARD_W = 3.30
CARD_H = 0.94
MARK_SIZE = 18
DOT_R = 0.075
COIN_R = 0.17

# The example figures this video works with.  They are held as data so the board
# and the narration can never drift apart, and every rate here is a textbook or
# historical example -- never current tax advice.
SHOE_PRICE = 450
SHOE_RATE = 6
SHOE_TAX = 27
SHOE_BILL = 477
VAT_BASE = "Rs 354.45"
VAT_TAX = "Rs 17.72"
VAT_BILL = "Rs 372.18"
GST_BASE = 1000
GST_RATE = 5
GST_TAX = 50
GST_BILL = 1050
REV_BILL = 2360
REV_RATE = 18
REV_BASE = 2000
REV_TAX = 360


# ---------------------------------------------------------------- furniture --
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


def bill_bar(width=2.40, height=0.54, color=CHALK_GREEN,
             label="BASE PRICE = 100%", size=13):
    """The persistent bill bar: one filled bar IS the whole 100% base price.

    The same bar -- same colour, same height, same label position -- is the
    anchor of every teaching scene, so "the base price" always looks the same
    and the tax layer is always seen attaching to that one object.
    """
    box = RoundedRectangle(corner_radius=0.05, width=width, height=height,
                           stroke_color=color, stroke_width=2.2,
                           fill_color=color, fill_opacity=0.22)
    grp = VGroup(box)
    grp.box = box
    if label:
        lab = board_text(label, size, CHALK_WHITE, "BOLD")
        lab.move_to(box.get_center())
        grp.add(lab)
        grp.label = lab
    return grp


def tax_layer(width=0.62, height=0.54, color=CHALK_AMBER, label="TAX",
              size=12):
    """The translucent tax layer that attaches above the 100% bar.

    It is deliberately see-through: the viewer must read it as a layer ADDED on
    top of the base price, never as a second base price.
    """
    box = RoundedRectangle(corner_radius=0.05, width=width, height=height,
                           stroke_color=color, stroke_width=2.2,
                           fill_color=color, fill_opacity=0.20)
    grp = VGroup(box)
    grp.box = box
    if label:
        lab = board_text(label, size, color, "BOLD")
        lab.move_to(box.get_center())
        grp.add(lab)
        grp.label = lab
    return grp


def rate_bar(base_w=2.60, rate=18, height=0.58, base_color=CHALK_GREEN,
             tax_color=CHALK_AMBER, base_label="100% = BASE PRICE",
             tax_label=None, size=13, tax_size=11):
    """The (100 + r)% bar: the base portion and the marked tax portion.

    The two portions sit flush against each other in ONE group, so the bar can
    be shrunk back to its 100% portion by taking the tax portion away.  The tax
    portion is proportional (r% of the base width), which is what makes it
    visibly the smaller part.
    """
    tax_w = max(base_w * rate / 100.0, 0.34)
    base = RoundedRectangle(corner_radius=0.04, width=base_w, height=height,
                            stroke_color=base_color, stroke_width=2.2,
                            fill_color=base_color, fill_opacity=0.22)
    tax = RoundedRectangle(corner_radius=0.04, width=tax_w, height=height,
                           stroke_color=tax_color, stroke_width=2.2,
                           fill_color=tax_color, fill_opacity=0.34)
    bar = VGroup(base, tax).arrange(RIGHT, buff=0.0)
    grp = VGroup(bar)
    grp.base, grp.tax = base, tax
    lab = board_text(base_label, size, CHALK_WHITE, "BOLD")
    lab.move_to(base.get_center())
    grp.add(lab)
    grp.label = lab
    if tax_label:
        # the tax label sits ABOVE its own thin portion: the portion is only a
        # sliver, so a label inside it could not be read
        tl = board_text(tax_label, tax_size, tax_color, "BOLD")
        tl.move_to(np.array([tax.get_center()[0],
                             tax.get_top()[1] + 0.19, 0.0]))
        grp.add(tl)
        grp.tax_label = tl
    return grp


def tax_split(width=3.60, height=0.66, color=CHALK_AMBER, left="CGST Rs 180",
              right="SGST Rs 180", size=12):
    """One tax block that physically halves into two labelled blocks.

    Both halves, their wording and the gap between them live in ONE group, so
    the block can be split apart without the labels being left behind.  Pass
    `left=None` / `right=None` to get the two bare halves and label them one
    bookmark at a time.
    """
    half = (width - 0.10) / 2.0
    boxes = VGroup(
        RoundedRectangle(corner_radius=0.05, width=half, height=height,
                         stroke_color=color, stroke_width=2.0,
                         fill_color=color, fill_opacity=0.32),
        RoundedRectangle(corner_radius=0.05, width=half, height=height,
                         stroke_color=color, stroke_width=2.0,
                         fill_color=color, fill_opacity=0.32),
    ).arrange(RIGHT, buff=0.10)
    halves = []
    for box, lab in zip(boxes, (left, right)):
        if lab is None:
            halves.append(VGroup(box))
        else:
            halves.append(VGroup(box, board_text(lab, size, CHALK_WHITE,
                                                 "BOLD"
                                                 ).move_to(box.get_center())))
    grp = VGroup(*halves)
    grp.half_l, grp.half_r = halves[0], halves[1]
    grp.boxes = boxes
    return grp


def whole_tax_block(width=3.60, height=0.66, color=CHALK_AMBER,
                    label="GST = Rs 360", size=13):
    """The undivided tax block the split is made from."""
    box = RoundedRectangle(corner_radius=0.05, width=width, height=height,
                           stroke_color=color, stroke_width=2.0,
                           fill_color=color, fill_opacity=0.32)
    lab = board_text(label, size, CHALK_WHITE, "BOLD")
    lab.move_to(box.get_center())
    grp = VGroup(box, lab)
    grp.box, grp.label = box, lab
    return grp


def receipt(width=1.80, height=1.10, color=CHALK_CYAN, head="BILL",
            value="Rs 477", size=12):
    """The bill itself: a filled slip with a heading and the amount on it.

    The ruled lines are thin filled bars rather than strokes, so no line ever
    runs through the lettering.
    """
    body = RoundedRectangle(corner_radius=0.06, width=width, height=height,
                            stroke_color=color, stroke_width=2.2,
                            fill_color=color, fill_opacity=0.18)
    h = board_text(head, size, color, "BOLD")
    h.move_to(body.get_center() + UP * 0.34)
    v = board_text(value, size, CHALK_WHITE, "BOLD")
    v.move_to(body.get_center() + DOWN * 0.32)
    bars = VGroup()
    for yy in (0.12, 0.04):
        b = Rectangle(width=width - 0.48, height=0.035, stroke_width=0,
                      fill_color=CHALK_WHITE, fill_opacity=0.35)
        b.move_to(body.get_center() + UP * yy)
        bars.add(b)
    grp = VGroup(body, bars, h, v)
    grp.box, grp.head, grp.value = body, h, v
    return grp


def med_receipt(width=1.95, height=1.30, color=CHALK_CYAN, head="MEDICAL",
                value="Rs 372.18", size=12):
    """The medical-shop receipt: a filled slip with a drawn medical cross.

    The cross is two filled bars (no outline glyph, no bare stroke), so it
    reads as printed ink on the slip.
    """
    body = RoundedRectangle(corner_radius=0.06, width=width, height=height,
                            stroke_color=color, stroke_width=2.2,
                            fill_color=color, fill_opacity=0.18)
    cross = VGroup(
        Rectangle(width=0.10, height=0.34, stroke_width=0,
                  fill_color=CHALK_WHITE, fill_opacity=0.55),
        Rectangle(width=0.34, height=0.10, stroke_width=0,
                  fill_color=CHALK_WHITE, fill_opacity=0.55),
    )
    cross.move_to(body.get_center())
    h = board_text(head, size, color, "BOLD")
    h.move_to(body.get_center() + UP * 0.46)
    v = board_text(value, size, CHALK_WHITE, "BOLD")
    v.move_to(body.get_center() + DOWN * 0.46)
    bars = VGroup()
    for yy in (-0.20, -0.28):
        b = Rectangle(width=width - 0.48, height=0.035, stroke_width=0,
                      fill_color=CHALK_WHITE, fill_opacity=0.35)
        b.move_to(body.get_center() + UP * yy)
        bars.add(b)
    grp = VGroup(body, cross, bars, h, v)
    grp.box, grp.head, grp.value = body, h, v
    return grp


def price_tag(width=2.00, height=0.82, color=CHALK_PINK, text="Rs 450",
              size=14):
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


def shoe_pair(cx, cy, scale=1.0, color=CHALK_PINK):
    """A pair of shoes: two filled, shaded shoes (sole, upper and a lace)."""
    shoes = VGroup()
    for dx in (-0.34 * scale, 0.34 * scale):
        sole = Polygon(
            np.array([cx + dx - 0.32 * scale, cy - 0.13 * scale, 0.0]),
            np.array([cx + dx + 0.27 * scale, cy - 0.13 * scale, 0.0]),
            np.array([cx + dx + 0.33 * scale, cy - 0.03 * scale, 0.0]),
            np.array([cx + dx - 0.36 * scale, cy - 0.03 * scale, 0.0]),
            stroke_color=color, stroke_width=1.9,
            fill_color=color, fill_opacity=0.34)
        upper = Polygon(
            np.array([cx + dx - 0.28 * scale, cy - 0.02 * scale, 0.0]),
            np.array([cx + dx + 0.05 * scale, cy - 0.02 * scale, 0.0]),
            np.array([cx + dx + 0.00 * scale, cy + 0.25 * scale, 0.0]),
            np.array([cx + dx - 0.22 * scale, cy + 0.23 * scale, 0.0]),
            stroke_color=color, stroke_width=1.9,
            fill_color=color, fill_opacity=0.26)
        lace = Line(np.array([cx + dx - 0.19 * scale, cy + 0.09 * scale, 0.0]),
                    np.array([cx + dx - 0.01 * scale, cy + 0.12 * scale, 0.0]),
                    stroke_color=CHALK_WHITE, stroke_width=1.6)
        shoes.add(sole, upper, lace)
    return shoes


def goods_icon(cx, cy, scale=1.0, color=CHALK_GREEN):
    """Goods: a filled parcel with a printed band and tape."""
    body = Rectangle(width=0.64 * scale, height=0.56 * scale,
                     stroke_color=color, stroke_width=2.0,
                     fill_color=color, fill_opacity=0.26)
    body.move_to(np.array([cx, cy, 0.0]))
    band = Rectangle(width=0.10 * scale, height=0.56 * scale, stroke_width=0,
                     fill_color=CHALK_WHITE, fill_opacity=0.45)
    band.move_to(body.get_center())
    tape = Rectangle(width=0.64 * scale, height=0.10 * scale, stroke_width=0,
                     fill_color=CHALK_WHITE, fill_opacity=0.45)
    tape.move_to(body.get_center())
    return VGroup(body, band, tape)


def service_icon(cx, cy, scale=1.0, color=CHALK_CYAN):
    """Services: a filled badge holding a drawn spanner."""
    disc = Circle(radius=0.32 * scale, stroke_color=color, stroke_width=2.0,
                  fill_color=color, fill_opacity=0.26)
    disc.move_to(np.array([cx, cy, 0.0]))
    handle = Rectangle(width=0.42 * scale, height=0.09 * scale,
                       stroke_color=CHALK_WHITE, stroke_width=0.0,
                       fill_color=CHALK_WHITE, fill_opacity=0.55)
    handle.move_to(np.array([cx, cy - 0.10 * scale, 0.0]))
    handle.rotate(-35 * DEGREES)
    jaw = Circle(radius=0.11 * scale, stroke_color=CHALK_WHITE,
                 stroke_width=2.0, fill_color=PANEL_FILL, fill_opacity=0.85)
    jaw.move_to(handle.get_end())
    return VGroup(disc, handle, jaw)


def money_note(width=1.54, height=0.74, color=CHALK_GREEN, text="Rs 27",
               size=13):
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


def name_card(head, sub, color=CHALK_CYAN, width=2.40, head_size=12,
              sub_size=10, gap=0.24, pad=0.16):
    """A small two-line card: the name of a quantity and its one-line gloss.

    Used for the three quantities of the title card.  The two lines are held
    0.24 apart and the box is sized to them, so the gloss can never be squeezed
    against the name.
    """
    h = board_text(head, head_size, color, "BOLD")
    s = board_text(sub, sub_size, CHALK_WHITE, "BOLD")
    inner = VGroup(h, s).arrange(DOWN, buff=gap)
    box = panel(width, inner.height + 2 * pad, color, radius=0.09)
    inner.move_to(box.get_center())
    grp = VGroup(box, h, s)
    grp.box, grp.head, grp.sub = box, h, s
    return grp


def lane_card(head, lines, color=CHALK_CYAN, width=4.20, head_size=15,
              line_size=12, gap=0.30, buff=0.26, pad=0.26):
    """One lane of the forward/backward decision board.

    The head and the body are separated by `gap` (0.30) and the body's own lines
    by `buff` (0.26), so the card passes the clearance audit (which flags any
    two texts closer than 0.22).  The box is sized to the text it carries, so
    the wording can never stick out of its own panel.
    """
    h = board_text(head, head_size, color, "BOLD")
    body = VGroup(*[board_text(line, line_size, CHALK_WHITE, "BOLD")
                    for line in lines]).arrange(DOWN, buff=buff)
    inner = VGroup(h, body).arrange(DOWN, buff=gap)
    box = panel(width, inner.height + 2 * pad, color)
    inner.move_to(box.get_center())
    grp = VGroup(box, h, body)
    grp.box, grp.head, grp.body = box, h, body
    return grp


def note_card(head, lines, color=CHALK_CYAN, width=3.40, height=1.05,
              head_size=15, line_size=13):
    """A card with a bold head line and ONE body line under it.

    A second body line would leave less than the 0.22 units the clearance audit
    asks for between the head and the body, so this card carries one line; the
    two-line board is `lane_card`.
    """
    box = panel(width, height, color)
    h = board_text(head, head_size, color, "BOLD")
    body = VGroup(*[board_text(line, line_size, CHALK_WHITE, "BOLD")
                    for line in lines]).arrange(DOWN, buff=0.24)
    h.move_to(box.get_center() + UP * 0.27)
    body.move_to(box.get_center() + DOWN * 0.27)
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


def wrong_card(text, color=CHALK_RED, width=2.60, height=1.00, size=13):
    """A card holding a WRONG statement, with a drawn cross over it.

    The cross occupies the card's top half and the statement its bottom half, so
    the strike-through is unmistakable yet never comes within the 0.04 units the
    audit allows between a stroke and the lettering.  The whole card is ONE
    board object, so the strokes are never read as a line running into a box.
    """
    box = panel(width, height, color, opacity=0.7)
    cross = VGroup(
        Line(np.array([-width / 2 + 0.50, 0.12, 0.0]),
             np.array([-width / 2 + 0.98, 0.42, 0.0]),
             stroke_color=color, stroke_width=4.2),
        Line(np.array([-width / 2 + 0.50, 0.42, 0.0]),
             np.array([-width / 2 + 0.98, 0.12, 0.0]),
             stroke_color=color, stroke_width=4.2),
    )
    cross.move_to(box.get_center() + UP * (height / 2.0 - 0.24))
    cross.shift(RIGHT * 0.10)
    lab = board_text(text, size, color, "BOLD")
    lab.move_to(box.get_center() + DOWN * (height / 2.0 - 0.24))
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
        "Meet the price tag, then meet the bill. <bookmark mark='b0'/>A pair of "
        "shoes is marked at four hundred and fifty rupees. <bookmark "
        "mark='b1'/>At the counter, a sales tax of six percent is added. "
        "<bookmark mark='b2'/>Three quantities are involved: the base price, "
        "the price before any tax; <bookmark mark='b3'/>the tax amount, the "
        "percentage that is added; <bookmark mark='b4'/>and the final bill, the "
        "base price plus the tax. So the tag and the bill show two different "
        "numbers."
    ),
    "s1": (
        "A tax is just a percentage increase. <bookmark mark='b0'/>The original "
        "price is taken as one hundred percent. <bookmark mark='b1'/>Adding a "
        "tax of r percent gives one hundred plus r percent. <bookmark "
        "mark='b2'/>With six percent, the total becomes one hundred and six "
        "percent. <bookmark mark='b3'/>So the final bill is one hundred plus r, "
        "divided by one hundred, times the base price. <bookmark mark='b4'/>This "
        "is exactly the percentage increase we met in the earlier lesson."
    ),
    "s2": (
        "Now the same shoes, with the numbers filled in. <bookmark "
        "mark='b0'/>The base price is four hundred and fifty rupees. <bookmark "
        "mark='b1'/>Sales tax is six percent, so the tax is six over one hundred "
        "times four hundred and fifty, which is twenty seven rupees. <bookmark "
        "mark='b2'/>Add it to the base price: four hundred and fifty plus twenty "
        "seven is four hundred and seventy seven rupees. <bookmark mark='b3'/>"
        "Here is the shortcut: one hundred and six percent of four hundred and "
        "fifty. <bookmark mark='b4'/>That is one point zero six times four "
        "hundred and fifty, which is again four hundred and seventy seven "
        "rupees."
    ),
    "s3": (
        "A tax can also be written on the bill. <bookmark mark='b0'/>Here is a "
        "medical bill: the amount before value added tax is three hundred and "
        "fifty four rupees and forty five paise. <bookmark mark='b1'/>The value "
        "added tax is five percent, which is seventeen rupees and seventy two "
        "paise. <bookmark mark='b2'/>The total is three hundred and seventy two "
        "rupees and eighteen paise, so the base plus the tax gives the bill. "
        "<bookmark mark='b3'/>Value added tax works exactly like the sales tax "
        "we just used: both are the same percentage idea. <bookmark "
        "mark='b4'/>And remember, these older rates are textbook and historical "
        "examples, not advice about the taxes of today."
    ),
    "s4": (
        "Goods and services tax uses the same structure. <bookmark "
        "mark='b0'/>GST is an indirect tax on goods and services, and it is "
        "charged on the base price. <bookmark mark='b1'/>Take a base price of "
        "one thousand rupees, with GST at five percent. <bookmark mark='b2'/>"
        "Five percent of one thousand is fifty rupees, so the tax amount is "
        "fifty rupees. <bookmark mark='b3'/>Add it to the base: one thousand "
        "plus fifty is one thousand and fifty rupees. <bookmark mark='b4'/>The "
        "shortcut is unchanged: one hundred and five percent of one thousand is "
        "also one thousand and fifty."
    ),
    "s5": (
        "Now the other direction. <bookmark mark='b0'/>A bill of two thousand "
        "three hundred and sixty rupees already includes GST at eighteen "
        "percent. <bookmark mark='b1'/>So this bill is not one hundred percent: "
        "it is one hundred and eighteen percent of the base price. <bookmark "
        "mark='b2'/>To recover the base price we divide: two thousand three "
        "hundred and sixty times one hundred, over one hundred and eighteen. "
        "<bookmark mark='b3'/>That gives a base price of two thousand rupees, "
        "and the tax is the rest, three hundred and sixty rupees. <bookmark "
        "mark='b4'/>Never take eighteen percent of two thousand three hundred "
        "and sixty and subtract it: the rate was charged on the base, not on the "
        "bill."
    ),
    "s6": (
        "Here is a worked example from the textbook. <bookmark mark='b0'/>The "
        "total GST on that purchase is three hundred and sixty rupees. <bookmark "
        "mark='b1'/>In this worked example the tax is divided into two equal "
        "parts. <bookmark mark='b2'/>One half is central GST, one hundred and "
        "eighty rupees. <bookmark mark='b3'/>The other half is state GST, "
        "another one hundred and eighty rupees. <bookmark mark='b4'/>So one "
        "block of three hundred and sixty splits into one hundred and eighty and "
        "one hundred and eighty. That equal split belongs to this worked "
        "example, not to every bill."
    ),
    "s7": (
        "Now a two lane decision board. <bookmark mark='b0'/>If the base price "
        "is given, go forward: find the tax, then add it, or use the bill equals "
        "the base times one hundred plus r, over one hundred. <bookmark "
        "mark='b1'/>If the tax-inclusive bill is given, go backward: recover the "
        "base with base equals bill times one hundred, over one hundred plus r. "
        "<bookmark mark='b2'/>Which lane you use depends only on what you were "
        "given. <bookmark mark='b3'/>And keep tax separate from discount: a "
        "discount is taken away from the price, while a tax is added to the "
        "base. <bookmark mark='b4'/>Tax adds, discount removes."
    ),
    "s8": (
        "Here is the classic error. <bookmark mark='b0'/>Take a base price of "
        "one thousand rupees, with GST at eighteen percent. <bookmark "
        "mark='b1'/>The tax is eighteen percent of one thousand, which is one "
        "hundred and eighty rupees, so the bill is one thousand one hundred and "
        "eighty. <bookmark mark='b2'/>The mistake is to apply the rate to the "
        "bill: eighteen percent of one thousand one hundred and eighty is not "
        "the tax for this purchase. <bookmark mark='b3'/>The same mistake is to "
        "subtract the rate straight off a tax-inclusive bill. <bookmark "
        "mark='b4'/>The rate is always applied to the base, and a tax-inclusive "
        "bill is worked backward with one hundred over one hundred plus r."
    ),
    "s9q": (
        "Your turn. Four quick checks. <bookmark mark='b0'/>A: an item costs "
        "eight hundred rupees, and the tax is five percent. What is the tax, and "
        "what is the bill? <bookmark mark='b1'/>B: a bill of one thousand one "
        "hundred and eighty rupees includes GST at eighteen percent. What is the "
        "base price, and what is the tax? <bookmark mark='b2'/>C: a total GST of "
        "one hundred and eighty rupees is split equally into central GST and "
        "state GST. How much is each part? <bookmark mark='b3'/>D: here is the "
        "error to spot. Eighteen percent of one thousand rupees is one hundred "
        "and eighty rupees, so is eighteen percent of one thousand one hundred "
        "and eighty the right tax for the same purchase? Pause the video, work "
        "all four out, and then we will check every answer."
    ),
    "s9a": (
        "Let us check every answer. <bookmark mark='b0'/>A: five percent of "
        "eight hundred is forty rupees, so the tax is forty rupees and the bill "
        "is eight hundred and forty rupees. <bookmark mark='b1'/>B: the bill is "
        "one hundred and eighteen percent, so the base is one thousand one "
        "hundred and eighty times one hundred over one hundred and eighteen, "
        "which is one thousand rupees, and the tax is one hundred and eighty "
        "rupees. <bookmark mark='b2'/>C: one hundred and eighty split equally is "
        "ninety and ninety, so central GST is ninety rupees and state GST is "
        "ninety rupees. <bookmark mark='b3'/>D: no. Eighteen percent of one "
        "thousand one hundred and eighty is not the tax for this purchase. The "
        "rate belongs on the base of one thousand rupees."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>Start at one hundred percent, the "
        "base price. <bookmark mark='b1'/>Add the tax to reach one hundred plus "
        "r percent. <bookmark mark='b2'/>Work backward with one hundred divided "
        "by one hundred plus r when the tax-inclusive total is given. <bookmark "
        "mark='b3'/>And keep the tax separate from a discount: a tax adds to the "
        "base, a discount takes off the price. <bookmark mark='b4'/>So start at "
        "one hundred percent, add the tax, and work backward with one hundred "
        "divided by one hundred plus r. <bookmark mark='b5'/>Thank you for "
        "watching, <bookmark mark='b6'/>and see you in the next lesson."
    ),
}


class SalesTaxVatAndGstCalculationsStory(VoiceoverScene):
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
        out_dir = _HERE / "media" / "videos" / "sales_tax_vat_and_gst_calculations"
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
    # Sales Tax, VAT & GST Calculations: Determining Original Prices and Total
    # Bills (Class 8 Maths, Chapter 5, Storymode 03).
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
    #   * ROW_A holds the diagram, ROW_B the numbers worked under it and ROW_C
    #     the rule chip above the banner, so nothing ever moves line by line;
    #   * every row of cards is centred on BOARD_CX (`hrow`, `row_centres`), and
    #     two texts never come closer than the 0.22 units the clearance audit
    #     asks for -- which is why a card's own lines are spaced by 0.26 or more
    #     and its head sits 0.30 above its body;
    #   * the BASE PRICE and the TAX-INCLUSIVE BILL are never the same object on
    #     screen: the bill bar is the base, and the translucent tax layer is
    #     visibly something ADDED to it;
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

    def even_row(self, *mobs, y, gap=0.45, cx=BOARD_CX):
        """One row whose elements are spaced by their own ink, not by centre."""
        halves = [m.width / 2.0 for m in mobs]
        centres = row_centres(halves, gap, cx)
        for m, x in zip(mobs, centres):
            at(m, x, y)
        return VGroup(*mobs)

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

    def checked_row(self, text, color=CHALK_GREEN, size=12):
        """A chip that carries a drawn tick just OUTSIDE its box.

        The tick is kept clear of the chip's box (and so of its lettering) and
        is far too small to be read as a line running into a panel.
        """
        c = chip(text, color, size=size)
        k = tick((0.0, 0.0), color, 0.16)
        row = VGroup(k, c).arrange(RIGHT, buff=0.18)
        row.chip, row.tick = c, k
        return row

    # -- Scene 0: the tag is not the bill ------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = at(board_text("The Tag Is Not the Bill", 26, CHALK_PINK,
                                  "BOLD"), BOARD_CX, 2.06)
            sub = at(board_text("A pair of shoes, and a six percent tax.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, 1.44)

            shoes = at(shoe_pair(0.0, 0.0, 0.85, CHALK_PINK), -3.70, 0.82)
            tag = at(price_tag(2.00, 0.74, CHALK_PINK, "Rs 450", 14),
                     -1.85, 0.82)
            rate = at(chip("SALES TAX 6%", CHALK_AMBER, size=14), 0.85, 0.82)
            bill = at(receipt(1.60, 1.00, CHALK_CYAN, "BILL", "Rs 477", 12),
                      3.75, 0.82)

            q1 = name_card("BASE PRICE", "before tax", CHALK_GREEN)
            q2 = name_card("TAX AMOUNT", "the percentage added", CHALK_AMBER)
            q3 = name_card("FINAL BILL", "base plus tax", CHALK_YELLOW)
            row = self.even_row(q1, q2, q3, y=-0.45, gap=0.45)

            banner = at(board_text("BASE + TAX = THE FINAL BILL", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The price on the tag is not always the bill "
                                  "you pay.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(title, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(shoes, scale=0.9), FadeIn(tag, scale=0.9),
                      run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(rate, scale=0.9), FadeIn(bill, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(q1, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(q2, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(q3, shift=UP * 0.06),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: a tax is a percentage increase -----------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("A Tax Is a Percentage Increase", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The base price is the one hundred percent.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            bar = at(bill_bar(2.40, 0.54, CHALK_GREEN, "BASE PRICE = 100%", 13),
                     -2.80, ROW_A)
            layer = tax_layer(0.62, 0.54, CHALK_AMBER, "6%", 12)
            layer_start = np.array([-1.29, ROW_A + 0.72, 0.0])
            layer.move_to(layer_start)
            merged = at(bill_bar(3.02, 0.54, CHALK_YELLOW, "106% = THE BILL",
                                 13), -2.49, ROW_A)
            rate = at(chip("6% GIVES 106%", CHALK_AMBER, size=13), 0.85, ROW_A)
            # the bill grows as the layer joins the bar
            rec = at(receipt(1.70, 1.06, CHALK_CYAN, "BILL", "Rs 477", 12),
                     3.60, ROW_A)
            rec.scale(0.66)

            formula = at(chip("FINAL BILL = (100 + r) / 100 x BASE PRICE",
                              CHALK_YELLOW, size=13), BOARD_CX, ROW_B)
            idea = at(chip("SAME AS A PERCENTAGE INCREASE", CHALK_PINK,
                           size=13), BOARD_CX, ROW_C)
            banner = at(board_text("A TAX IS A PERCENTAGE INCREASE", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Adding r percent makes the bill one hundred "
                                  "plus r percent of the base.", 15,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(bar, scale=0.95), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(layer, scale=0.9), run_time=0.35)
            self.play(layer.animate.move_to(np.array([-1.29, ROW_A, 0.0])),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(ReplacementTransform(VGroup(bar, layer), merged),
                      FadeIn(rate, scale=0.9), run_time=0.50)
            self.play(FadeIn(rec, scale=0.80), run_time=0.30)
            self.play(rec.animate.scale(1.0 / 0.66), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(formula, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(idea, shift=UP * 0.06),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: sales tax on Rs 450 at 6% ----------------------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("Sales Tax on a Pair of Shoes", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Base Rs 450 and sales tax 6%.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            shoes = at(shoe_pair(0.0, 0.0, 0.85, CHALK_PINK), -3.72, ROW_A)
            tag = at(price_tag(2.00, 0.82, CHALK_PINK, "Rs 450", 14),
                     -1.85, ROW_A)
            tax = at(chip("TAX 6% OF 450 = Rs 27", CHALK_AMBER, size=13),
                     1.20, ROW_A)
            bill = at(chip("BILL = Rs 477", CHALK_YELLOW, size=13), 3.75, ROW_A)

            m1 = chip("6/100 x 450 = Rs 27", CHALK_AMBER, size=13)
            m2 = chip("450 + 27 = Rs 477", CHALK_GREEN, size=13)
            row = self.even_row(m1, m2, y=ROW_B, gap=0.50)

            short = at(chip("SHORTCUT: 106% OF 450 = 1.06 x 450 = Rs 477",
                            CHALK_YELLOW, size=13), BOARD_CX, ROW_C)
            banner = at(board_text("TAX Rs 27, FINAL BILL Rs 477", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The bill is the base price plus the tax.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(shoes, scale=0.9), FadeIn(tag, scale=0.9),
                      run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(tax, scale=0.9), run_time=0.40)
            self.play(FadeIn(m1, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(bill, scale=0.9), FadeIn(m2, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(short, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: reading a VAT-inclusive bill -------------------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Reading a VAT-Inclusive Bill", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("VAT is the same percentage idea.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            slip = at(med_receipt(1.95, 1.30, CHALK_CYAN, "MEDICAL",
                                  "Rs 372.18", 12), -3.40, 0.96)
            before = at(chip("PRE-VAT = Rs 354.45", CHALK_CYAN, size=13),
                        -0.75, 0.96)
            vat = at(chip("+ VAT 5% = Rs 17.72", CHALK_AMBER, size=13),
                     2.15, 0.96)

            b1 = chip("BASE + VAT = THE BILL", CHALK_YELLOW, size=13)
            b2 = chip("354.45 + 17.72 = Rs 372.18", CHALK_GREEN, size=13)
            row = self.even_row(b1, b2, y=ROW_B, gap=0.50)

            same = at(chip("VAT = THE SAME PERCENTAGE IDEA", CHALK_CYAN,
                           size=12), BOARD_CX, ROW_C)
            note = at(chip("HISTORICAL RATES, NOT TODAY'S TAX ADVICE",
                           CHALK_PINK, size=12), BOARD_CX, ROW_C)
            banner = at(board_text("BASE Rs 354.45 + VAT Rs 17.72 = Rs 372.18",
                                   16, CHALK_YELLOW, "BOLD"),
                        BOARD_CX, BANNER_Y)
            strip = at(board_text("Sales tax, VAT and GST share one arithmetic "
                                  "model.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(slip, scale=0.9), FadeIn(before, scale=0.9),
                      run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(vat, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(b1, shift=UP * 0.06), FadeIn(b2, shift=UP * 0.06),
                      FadeIn(banner, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(same, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeOut(same), FadeIn(note, scale=0.9),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: GST uses the same structure --------------------------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("GST Uses the Same Structure", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Base Rs 1,000 and GST at 5%.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            goods = at(goods_icon(0.0, 0.0, 1.0, CHALK_GREEN), -3.85, ROW_A)
            service = at(service_icon(0.0, 0.0, 1.0, CHALK_CYAN), -2.85, ROW_A)
            label = at(chip("GST: AN INDIRECT TAX ON GOODS AND SERVICES",
                            CHALK_CYAN, size=12), 1.30, ROW_A)

            rate = chip("BASE = Rs 1,000 · GST = 5%", CHALK_GREEN, size=13)
            rate.move_to(np.array([BOARD_CX, ROW_B, 0.0]))
            tax = at(chip("TAX = 5/100 x 1,000 = Rs 50", CHALK_AMBER, size=13),
                     BOARD_CX, ROW_B)
            add = at(chip("BILL = 1,000 + 50 = Rs 1,050", CHALK_GREEN,
                          size=13), BOARD_CX, ROW_C)
            short = at(chip("SHORTCUT: 105% OF 1,000 = Rs 1,050",
                            CHALK_YELLOW, size=13), BOARD_CX, ROW_B)

            banner = at(board_text("BASE + 5% GST = Rs 1,050", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("GST is indirect, but the arithmetic is "
                                  "unchanged.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(goods, scale=0.9), FadeIn(service, scale=0.9),
                      FadeIn(label, scale=0.9), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(rate, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeOut(rate), FadeIn(tax, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(add, scale=0.9), FadeIn(banner, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeOut(tax), FadeIn(short, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: working backward from a tax-inclusive bill -----------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("Finding the Price Before Tax", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The bill is 118%, not 100%.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            # the 118% bar: the base portion plus the marked 18% tax portion
            rb = rate_bar(2.60, REV_RATE, 0.58, CHALK_GREEN, CHALK_AMBER,
                          "118% = THE BILL", "18%", 13, 11)
            rb.move_to(np.array([-2.85, 0.94, 0.0]))
            base_lab = board_text("100% = BASE PRICE", 13, CHALK_WHITE, "BOLD")
            base_lab.move_to(rb.base.get_center())

            bill = chip("BILL INCL. 18% GST = Rs 2,360", CHALK_CYAN, size=13)
            bill.move_to(np.array([BOARD_CX, ROW_B, 0.0]))
            div = at(chip("2,360 x 100/118", CHALK_AMBER, size=13),
                     BOARD_CX, ROW_B)
            r1 = chip("BASE = Rs 2,000", CHALK_GREEN, size=13)
            r2 = chip("TAX = Rs 360", CHALK_AMBER, size=13)
            res = self.even_row(r1, r2, y=ROW_B, gap=0.50)

            formula = at(chip("BASE = BILL x 100 / (100 + r)", CHALK_YELLOW,
                              size=13), BOARD_CX, ROW_C)
            banner = at(board_text("BASE = Rs 2,000, TAX = Rs 360", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            warn = at(board_text("NEVER SUBTRACT THE RATE OFF THE BILL", 16,
                                 CHALK_RED, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Work backward with 100 divided by 100 plus "
                                  "r.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(bill, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(rb, scale=0.95), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeOut(bill), FadeIn(div, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            # the tax portion leaves and the bar is the 100% base again -- only
            # NOW does the reverse formula go on the board
            self.wait(leftover(tracker, "b3"))
            self.play(FadeOut(rb.tax), FadeOut(rb.tax_label),
                      FadeOut(rb.label), FadeIn(base_lab, scale=0.9),
                      FadeOut(div), run_time=0.55)
            self.play(FadeIn(res, shift=UP * 0.06), run_time=0.45)
            self.play(FadeIn(formula, scale=0.9),
                      FadeIn(banner, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeOut(banner), FadeIn(warn, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: the textbook's CGST / SGST split ---------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("CGST and SGST in the Textbook", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A worked example, not a universal rule.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            whole = at(whole_tax_block(3.60, 0.66, CHALK_AMBER,
                                       "GST = Rs 360", 13), -1.60, ROW_A)
            # the two bare halves: the CGST and SGST wording arrives one
            # bookmark at a time, so the split itself is what b2 shows
            split = tax_split(3.60, 0.66, CHALK_AMBER, None, None, 12)
            split.move_to(np.array([-1.60, ROW_A, 0.0]))
            cgst = board_text("CGST Rs 180", 12, CHALK_WHITE, "BOLD")
            cgst.move_to(split.half_l.get_center())
            sgst = board_text("SGST Rs 180", 12, CHALK_WHITE, "BOLD")
            sgst.move_to(split.half_r.get_center())
            tag = at(chip("THE TEXTBOOK HALVES IT", CHALK_CYAN, size=13),
                     3.05, ROW_A)

            h1 = chip("360 / 2 = Rs 180 EACH", CHALK_GREEN, size=13)
            h2 = chip("180 + 180 = Rs 360", CHALK_AMBER, size=13)
            row = self.even_row(h1, h2, y=ROW_B, gap=0.50)

            note = at(chip("THIS IS THE WORKED CASE, NOT EVERY BILL",
                           CHALK_PINK, size=12), BOARD_CX, ROW_C)
            banner = at(board_text("CGST Rs 180 + SGST Rs 180 = Rs 360", 17,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The equal split belongs to this worked "
                                  "example.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(whole, scale=0.95), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(tag, scale=0.9), FadeIn(h1, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            # the one tax block physically halves, and the CGST half is named
            self.wait(leftover(tracker, "b2"))
            self.play(ReplacementTransform(whole, split), run_time=0.55)
            self.play(FadeIn(cgst, scale=0.9), run_time=0.35)
            self.play(split.half_l.animate.shift(LEFT * 0.10),
                      split.half_r.animate.shift(RIGHT * 0.10),
                      cgst.animate.shift(LEFT * 0.10), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            # the SGST wording follows its own half, which has already shifted
            sgst.shift(RIGHT * 0.10)
            self.play(FadeIn(sgst, scale=0.9), FadeIn(h2, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(note, scale=0.9), FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: forward or backward -- the two-lane decision board ---------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Forward or Backward?", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("What you were given decides the lane.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            lane1 = lane_card("BASE PRICE GIVEN",
                              ["tax = r% of the base",
                               "bill = base + tax"], CHALK_GREEN,
                              width=4.20, head_size=14, line_size=12)
            lane2 = lane_card("TAX-INCLUSIVE BILL GIVEN",
                              ["base = bill x 100 / (100 + r)",
                               "the tax is bill - base"], CHALK_CYAN,
                              width=4.20, head_size=14, line_size=12)
            self.even_row(lane1, lane2, y=0.80, gap=0.45)

            ask = chip("THE LANE FOLLOWS WHAT YOU WERE GIVEN", CHALK_YELLOW,
                       size=13)
            ask.move_to(np.array([BOARD_CX, -0.48, 0.0]))
            adds = chip("TAX ADDS TO THE BASE", CHALK_GREEN, size=13)
            takes = chip("DISCOUNT TAKES OFF THE PRICE", CHALK_RED, size=13)
            keep = self.even_row(adds, takes, y=-0.48, gap=0.50)

            banner = at(board_text("TAX ADDS, DISCOUNT REMOVES", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Given the base go forward; given the bill go "
                                  "backward.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(lane1, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(lane2, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(ask, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeOut(ask), FadeIn(keep, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the classic error, and the correction ----------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Classic Tax Error", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Apply the rate to the base, never the bill.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            start = chip("BASE = Rs 1,000 · GST = 18%", CHALK_CYAN, size=13)
            start.move_to(np.array([BOARD_CX, ROW_B, 0.0]))
            tax = chip("18% OF Rs 1,000 = Rs 180", CHALK_GREEN, size=13)
            bill = chip("BILL = Rs 1,180", CHALK_YELLOW, size=13)
            known = self.even_row(tax, bill, y=ROW_B, gap=0.50)

            wrong1 = wrong_card("18% OF Rs 1,180", CHALK_RED, 2.70, 1.00, 13)
            wrong1.move_to(np.array([-2.45, 1.00, 0.0]))
            c1 = wrong1.cross
            c1.set_stroke(opacity=0)
            wrong2 = wrong_card("1180 - 18% = ?", CHALK_RED, 2.70, 1.00, 13)
            wrong2.move_to(np.array([1.75, 1.00, 0.0]))
            c2 = wrong2.cross
            c2.set_stroke(opacity=0)

            good1 = self.checked_row("18% OF Rs 1,000 = Rs 180", CHALK_GREEN)
            good2 = self.checked_row("Rs 1,180 x 100/118 = Rs 1,000",
                                     CHALK_CYAN)
            fix = self.even_row(good1, good2, y=ROW_C, gap=0.45)

            banner = at(board_text("NEVER APPLY THE RATE TO THE BILL", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The rate is charged on the base, never on "
                                  "the total.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(start, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeOut(start), FadeIn(known, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(wrong1, scale=0.9), run_time=0.40)
            self.play(c1.animate.set_stroke(opacity=1), run_time=0.40)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(wrong2, scale=0.9), run_time=0.40)
            self.play(c2.animate.set_stroke(opacity=1), run_time=0.40)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(fix, shift=UP * 0.06),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, banner)
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

            pic_a = board_text("Rs 800 + 5% tax = ?", 14, CHALK_GREEN, "BOLD")
            pic_b = board_text("Rs 1,180 incl. 18% = ?", 13, CHALK_CYAN,
                               "BOLD")
            pic_c = board_text("GST Rs 180, split equally?", 13, CHALK_AMBER,
                               "BOLD")
            pic_d = VGroup(board_text("18% of Rs 1,180:", 12, CHALK_PINK,
                                      "BOLD"),
                           board_text("right for Rs 1,000?", 12, CHALK_PINK,
                                      "BOLD")).arrange(DOWN, buff=0.24)

            qa = at(self.q_card("A: tax and bill", pic_a, CHALK_GREEN),
                    -2.80, 0.92)
            qb = at(self.q_card("B: base and tax", pic_b, CHALK_CYAN),
                    3.70, 0.92)
            qc = at(self.q_card("C: CGST and SGST", pic_c, CHALK_AMBER),
                    -2.80, -1.02)
            qd = at(self.q_card("D: spot the error", pic_d, CHALK_PINK),
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
            a1 = at(self.answer_row("A", "tax Rs 40, bill Rs 840",
                                    "5% of Rs 800 = Rs 40", CHALK_GREEN),
                    BOARD_CX, 1.62)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "base Rs 1,000, tax Rs 180",
                                    "1,180 x 100/118 = Rs 1,000", CHALK_CYAN),
                    BOARD_CX, 0.82)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "CGST Rs 90, SGST Rs 90",
                                    "180 split equally: 90 + 90", CHALK_AMBER),
                    BOARD_CX, 0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "No: 18% of Rs 1,180 is wrong",
                                    "the rate belongs on Rs 1,000",
                                    CHALK_PINK), BOARD_CX, -0.78)
            self.play(FadeIn(a4, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, a4)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap and the spoken thank-you ----------------------------
    def beat_s10(self) -> None:
        with self.voiceover(text=NARRATION["s10"]) as tracker:
            self.reset_board()

            heading = at(board_text("Base, Tax Rate, Bill", 22, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Four formulas to carry away.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            r1 = at(self.answer_row("1", "TAX",
                                    "tax = r / 100 x base price", CHALK_GREEN),
                    BOARD_CX, 1.48)
            r2 = at(self.answer_row("2", "BILL",
                                    "bill = base + tax = (100 + r)/100 x base",
                                    CHALK_CYAN), BOARD_CX, 0.72)
            r3 = at(self.answer_row("3", "REVERSE",
                                    "base = bill x 100 / (100 + r)",
                                    CHALK_YELLOW), BOARD_CX, -0.04)
            r4 = at(self.answer_row("4", "TAX OR DISCOUNT",
                                    "tax adds to the base; discount removes",
                                    CHALK_AMBER), BOARD_CX, -0.80)
            strip = at(board_text("Start at 100%, add the tax, work backward "
                                  "with 100/(100 + r).", 15, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)
            thanks = at(board_text("Thank You for Watching!", 30, CHALK_WHITE,
                                   "BOLD"), BOARD_CX, 0.62)
            bye = at(board_text("See you in the next lesson :)", 22,
                                CHALK_YELLOW, "BOLD"), BOARD_CX, -0.32)

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

            # The list stays on the board through the whole closing sentence:
            # the strip is written on its own bookmark as the voice says "Start
            # at one hundred percent, add the tax, and work backward...", and
            # only the bookmark in front of "Thank you for watching," clears the
            # board and brings in the card.
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

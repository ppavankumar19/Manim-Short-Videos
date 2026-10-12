"""
Finding Discounts & Marked Price: Calculating SP and Discount Percentages
Story-mode chalkboard lesson (Class 8 Maths, Chapter 5: Comparing Quantities
using Proportion, Storymode 02).

LLM KEY / FUNCTION NAME: discounts_marked_price_and_rebate

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

The defining visual is THE SHOP TAG AND THE CUT PRICE BAR: the marked price
written on a tag (the price that never disappears), the glossy percent sticker
stuck on it, the drawn book / bicycle / ceiling fan that carry their own price
plates, the 100% = marked-price bar with the discount portion physically cut
off it and slid aside, and the two bars whose visible gap is the discount in
rupees before it moves up to become the discount percentage.

Title + 10 scenes:
  0. Title card: the tag says Rs 1600, the sticker says 6% off, and the three
     quantities (marked price, discount or rebate, selling price) are named.
  1. The three parts and the one relation MP - Discount = SP.
  2. A book marked Rs 80 at 15% off: find the discount, then the selling price.
  3. A cycle marked Rs 3600 sold for Rs 3312: the Rs 288 gap becomes 8%, and the
     base is the MARKED PRICE, not the selling price.
  4. A fan marked Rs 1600 with 6% off: Rs 96 off, Rs 1504 payable -- and the
     discount AMOUNT is kept apart from the discount RATE.
  5. The shortcut: 6% off leaves 94%, so SP = 94/100 x 1600; both routes land on
     Rs 1504, and SP = (100 - d)/100 x MP.
  6. Which formula? A decision board for the three question shapes.
  7. Common mistakes, each struck through with a drawn cross beside its fix.
  8. Reasonableness: a discount means SP < MP, and d% off leaves (100 - d)%.
  9. Your turn: four corner prompts, the series' centred ten-second THINK clock,
     then the answers for A, B and C.
 10. Recap: the price flow tag, reduce, pay, compare -- and the spoken
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


# (this section is spliced into a head whose own imports omit Ellipse, Arc and
#  Sector; Dot, Circle, Line, DashedLine, Rectangle, RoundedRectangle, Polygon,
#  DoubleArrow, VGroup, DEGREES, PI, TAU and np are already imported by the head)
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

# The content bands.  Cards are about a unit tall, so their TEXT boxes keep the
# 0.22 units of air the clearance audit asks for at these centres.
BAND_A = 1.05            # the upper band (the part cards, the decision cards)
BAND_B = -0.45           # the lower band (the one-line rule under them)

PANEL_FILL = "#16202B"
CARD_W = 3.00            # the standard card width
CARD_H = 1.10            # the standard card height
CHIP_H = 0.50
BAR_W = 4.20             # the price bar: 100% = the marked price
BAR_H = 0.46

# The example figures this video works with.  Every one is an on-screen example,
# never a textbook fact.
TITLE_MP = 1600
BOOK = (80, 15)          # a book: Rs 80 marked, 15% off
CYCLE = (3600, 3312)     # a cycle: Rs 3600 marked, sold for Rs 3312
FAN = (1600, 6)          # a fan: Rs 1600 marked, 6% off
QUIZ = ((450, 7), (1000, 900), (250, 5))


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


def cross_mark(point, size=0.21, color=CHALK_RED, width=4.2):
    """A drawn cross (Segoe Print has no cross glyph).

    Kept just under 0.45 units across so it can never be read as a figure a
    chalk line runs into; it is always placed inside the same VGroup as what it
    strikes through.
    """
    x, y = float(point[0]), float(point[1])
    return VGroup(
        Line(np.array([x - size, y - size, 0.0]),
             np.array([x + size, y + size, 0.0]),
             stroke_color=color, stroke_width=width),
        Line(np.array([x - size, y + size, 0.0]),
             np.array([x + size, y - size, 0.0]),
             stroke_color=color, stroke_width=width))


def tick(point, color=CHALK_GREEN, s=0.16):
    """A drawn tick (Segoe Print has no tick glyph)."""
    a = np.array([point[0] - s * 0.60, point[1] + s * 0.05, 0.0])
    b = np.array([point[0] - s * 0.05, point[1] - s * 0.55, 0.0])
    c = np.array([point[0] + s * 0.65, point[1] + s * 0.75, 0.0])
    return VGroup(Line(a, b, stroke_color=color, stroke_width=3.4),
                  Line(b, c, stroke_color=color, stroke_width=3.4))


def price_panel(cx, cy, price, color=CHALK_AMBER, size=14):
    """The little price plate a drawn article carries.

    The plate is sized from its own text, so the rupees always sit inside it
    with air to spare.
    """
    lab = board_text(price, size, CHALK_WHITE, "BOLD")
    tag = RoundedRectangle(corner_radius=0.05, width=lab.width + 0.34,
                           height=lab.height + 0.22, stroke_color=color,
                           stroke_width=1.6, fill_color="#2A1D10",
                           fill_opacity=0.75)
    tag.move_to(np.array([float(cx), float(cy), 0.0]))
    lab.move_to(tag.get_center())
    grp = VGroup(tag, lab)
    grp.tag, grp.label = tag, lab
    return grp


def price_tag(price="Rs 1600", cx=BOARD_CX, cy=0.0, color=CHALK_AMBER,
              width=2.50, height=1.24, size=24):
    """The tagged price of an article: a filled tag with a punched hole.

    This is the one object that stays on the board of every scene, so the
    tagged price is never lost when the discount is cut away from it.
    """
    x0, x1 = cx - width / 2.0, cx + width / 2.0
    y0, y1 = cy - height / 2.0, cy + height / 2.0
    body = Polygon(np.array([x0, cy, 0.0]),
                   np.array([x0 + 0.34, y1, 0.0]),
                   np.array([x1, y1, 0.0]),
                   np.array([x1, y0, 0.0]),
                   np.array([x0 + 0.34, y0, 0.0]),
                   stroke_color=color, stroke_width=2.4,
                   fill_color=color, fill_opacity=0.26)
    hole = Circle(radius=0.085, stroke_color=color, stroke_width=1.4,
                  fill_color="#0E1620", fill_opacity=0.95)
    hole.move_to(np.array([x0 + 0.52, cy + height * 0.30, 0.0]))
    gloss = Polygon(np.array([x0 + 0.42, y1 - 0.11, 0.0]),
                    np.array([x1 - 0.10, y1 - 0.11, 0.0]),
                    np.array([x1 - 0.22, y1 - 0.03, 0.0]),
                    np.array([x0 + 0.48, y1 - 0.03, 0.0]),
                    stroke_width=0, fill_color=CHALK_WHITE, fill_opacity=0.16)
    lab = board_text(price, size, CHALK_WHITE, "BOLD")
    lab.move_to(np.array([cx + 0.10, cy - 0.02, 0.0]))
    grp = VGroup(body, hole, gloss, lab)
    grp.body, grp.label = body, lab
    return grp


def price_sticker(text="6% OFF", cx=BOARD_CX, cy=0.0, r=0.50,
                  color=CHALK_PINK, size=15):
    """The glossy percent badge that is stuck over the tag.

    The gloss is a filled slanted slip (never an arc stroke): a stroke would be
    read as a chalk line running through the badge's own lettering.
    """
    cx, cy = float(cx), float(cy)
    disc = Circle(radius=r, stroke_color=color, stroke_width=2.2,
                  fill_color=color, fill_opacity=0.32)
    disc.move_to(np.array([cx, cy, 0.0]))
    gloss = Polygon(np.array([cx - 0.60 * r, cy + 0.44 * r, 0.0]),
                    np.array([cx + 0.06 * r, cy + 0.66 * r, 0.0]),
                    np.array([cx + 0.20 * r, cy + 0.54 * r, 0.0]),
                    np.array([cx - 0.46 * r, cy + 0.34 * r, 0.0]),
                    stroke_width=0, fill_color=CHALK_WHITE, fill_opacity=0.22)
    lab = board_text(text, size, CHALK_WHITE, "BOLD")
    lab.move_to(disc.get_center())
    grp = VGroup(disc, gloss, lab)
    grp.disc, grp.label = disc, lab
    return grp


def coin_stack(cx, cy, n=3, scale=1.0, color=CHALK_YELLOW):
    """A stack of coins: filled discs with thickness, drawn bottom-up."""
    discs = VGroup()
    for i in range(n):
        e = Ellipse(width=0.46 * scale, height=0.16 * scale,
                    stroke_color=color, stroke_width=1.5,
                    fill_color=color, fill_opacity=0.40)
        e.move_to(np.array([cx, cy + 0.075 * i * scale, 0.0]))
        discs.add(e)
    return discs


def note_stack(cx, cy, n=3, scale=1.0, color=CHALK_GREEN):
    """Drawn currency notes: filled slips with a band across each one."""
    notes = VGroup()
    for i in range(n):
        body = RoundedRectangle(corner_radius=0.03, width=0.94 * scale,
                                height=0.34 * scale, stroke_color=color,
                                stroke_width=1.5, fill_color=color,
                                fill_opacity=0.26)
        band = Rectangle(width=0.94 * scale, height=0.05 * scale,
                         stroke_width=0, fill_color=color, fill_opacity=0.55)
        band.move_to(body.get_center())
        slip = VGroup(body, band)
        slip.move_to(np.array([cx + 0.05 * i * scale,
                               cy + 0.10 * i * scale, 0.0]))
        notes.add(slip)
    return notes


def book_icon(cx, cy, price="Rs 80", color=CHALK_CYAN, scale=1.0):
    """A closed book with a page block, a spine and its price plate."""
    w, h = 1.30 * scale, 1.02 * scale
    cover = RoundedRectangle(corner_radius=0.06, width=w, height=h,
                             stroke_color=color, stroke_width=2.2,
                             fill_color=color, fill_opacity=0.28)
    cover.move_to(np.array([float(cx), float(cy), 0.0]))
    pages = Rectangle(width=w * 0.78, height=h * 0.80, stroke_width=0,
                      fill_color=CHALK_WHITE, fill_opacity=0.16)
    pages.align_to(cover, RIGHT).shift(LEFT * 0.07)
    spine = Rectangle(width=0.13 * scale, height=h * 0.90, stroke_width=0,
                      fill_color=color, fill_opacity=0.55)
    spine.move_to(np.array([cx - w / 2 + 0.09 * scale, cy, 0.0]))
    plate = price_panel(cx + 0.14 * scale, cy - h * 0.27, price, color, size=14)
    return VGroup(cover, pages, spine, plate)


def cycle_icon(cx, cy, price="Rs 3600", color=CHALK_AMBER, scale=1.0):
    """A bicycle: two spoked wheels with solid hubs and a filled frame."""
    r = 0.32 * scale
    wheels = VGroup()
    for wx in (cx - 0.54 * scale, cx + 0.54 * scale):
        tyre = Circle(radius=r, stroke_width=0,
                      fill_color=color, fill_opacity=0.55)
        rim = Circle(radius=r * 0.60, stroke_width=0,
                     fill_color=PANEL_FILL, fill_opacity=0.95)
        hub = Circle(radius=r * 0.16, stroke_width=0,
                     fill_color=CHALK_WHITE, fill_opacity=0.85)
        spoked = VGroup(tyre, rim, hub)
        spoked.move_to(np.array([wx, cy - 0.34 * scale, 0.0]))
        for k in range(4):
            ang = k * PI / 4.0
            a = spoked.get_center() + np.array([np.cos(ang), np.sin(ang), 0.0]) \
                * r * 0.55
            b = spoked.get_center() + np.array([-np.cos(ang), -np.sin(ang), 0.0]) \
                * r * 0.55
            spoked.add(Line(a, b, stroke_color=color, stroke_width=1.1))
        wheels.add(spoked)
    frame = Polygon(np.array([cx - 0.54 * scale, cy - 0.34 * scale, 0.0]),
                    np.array([cx + 0.02 * scale, cy + 0.22 * scale, 0.0]),
                    np.array([cx + 0.36 * scale, cy - 0.34 * scale, 0.0]),
                    stroke_color=color, stroke_width=2.4,
                    fill_color=color, fill_opacity=0.18)
    seat = Ellipse(width=0.30 * scale, height=0.13 * scale, stroke_width=0,
                   fill_color=CHALK_WHITE, fill_opacity=0.35)
    seat.move_to(np.array([cx - 0.30 * scale, cy + 0.32 * scale, 0.0]))
    handle = Line(np.array([cx + 0.02 * scale, cy + 0.22 * scale, 0.0]),
                  np.array([cx + 0.30 * scale, cy + 0.44 * scale, 0.0]),
                  stroke_color=color, stroke_width=2.6)
    plate = price_panel(cx + 0.44 * scale, cy + 0.66 * scale, price, color,
                        size=13)
    return VGroup(wheels, frame, seat, handle, plate)


def fan_icon(cx, cy, price="Rs 1600", color=CHALK_CYAN, scale=1.0):
    """A ceiling fan: three solid blades on a hub, on a short down-rod."""
    blades = VGroup()
    for k in range(3):
        blade = RoundedRectangle(corner_radius=0.06, width=0.72 * scale,
                                 height=0.20 * scale, stroke_color=color,
                                 stroke_width=1.6, fill_color=color,
                                 fill_opacity=0.32)
        blade.move_to(np.array([cx + 0.44 * scale, cy, 0.0]))
        blade.rotate(k * TAU / 3.0, about_point=np.array([cx, cy, 0.0]))
        blades.add(blade)
    hub = Circle(radius=0.15 * scale, stroke_color=color, stroke_width=1.8,
                 fill_color=color, fill_opacity=0.65)
    hub.move_to(np.array([float(cx), float(cy), 0.0]))
    rod = Rectangle(width=0.09 * scale, height=0.34 * scale, stroke_width=0,
                    fill_color=color, fill_opacity=0.5)
    rod.move_to(np.array([cx, cy + 0.40 * scale, 0.0]))
    canopy = Ellipse(width=0.34 * scale, height=0.14 * scale,
                     stroke_color=color, stroke_width=1.6,
                     fill_color=color, fill_opacity=0.26)
    canopy.move_to(np.array([cx, cy + 0.60 * scale, 0.0]))
    plate = price_panel(cx, cy - 0.60 * scale, price, color, size=13)
    return VGroup(blades, hub, rod, canopy, plate)


def list_card(head, lines, color=CHALK_CYAN, width=2.90, head_size=15,
              line_size=13, gap=0.26, pad=0.16, height=None):
    """A named part card: a bold head over one or two body lines.

    The card's height is computed from the real text heights, so the head and
    the body keep exactly `gap` (>= the 0.22 the clearance audit asks for) even
    though different lines have different ascenders and descenders.  Pass
    `height` to force a row of cards to one common height.
    """
    body = VGroup(*[board_text(t, line_size, CHALK_WHITE, "BOLD")
                    for t in lines]).arrange(DOWN, buff=gap)
    head_t = board_text(head, head_size, color, "BOLD")
    content = head_t.height + gap + body.height
    box = panel(width, height if height is not None else content + 2 * pad,
                color)
    head_t.move_to(box.get_center() + UP * (content / 2.0 - head_t.height / 2.0))
    body.move_to(head_t.get_center()
                 + DOWN * (head_t.height / 2.0 + gap + body.height / 2.0))
    grp = VGroup(box, head_t, body)
    grp.box, grp.head, grp.body = box, head_t, body
    return grp


def mistake_card(wrong, fix, color=CHALK_RED, width=4.05, height=1.10,
                 wrong_size=15, fix_size=12, fix_color=CHALK_GREEN):
    """A wrong statement struck through by a drawn cross, with its correction.

    The cross occupies the card's top half beside the wrong wording and the fix
    sits in the bottom half, so the strike-through is unmistakable yet never
    comes within the 0.04 units the audit allows between a stroke and a letter.
    The whole card is ONE board object.
    """
    box = panel(width, height, color, opacity=0.62)
    cross = cross_mark(np.array([0.0, 0.0, 0.0]), size=0.20, color=color)
    wrong_t = board_text(wrong, wrong_size, color, "BOLD")
    top = VGroup(cross, wrong_t).arrange(RIGHT, buff=0.30)
    top.move_to(box.get_center() + UP * 0.26)
    fix_t = board_text(fix, fix_size, fix_color, "BOLD")
    fix_t.move_to(box.get_center() + DOWN * 0.26)
    grp = VGroup(box, top, fix_t)
    grp.box, grp.cross, grp.wrong, grp.fix = box, cross, wrong_t, fix_t
    return grp


def split_bar(cx, cy, width=BAR_W, height=BAR_H, cut=0.15, sp_text="",
              sp_size=14, slide=1.10, mp_note="", mp_size=14,
              color_sp=CHALK_GREEN, color_disc=CHALK_PINK, slot_side="right"):
    """The 100% = marked-price bar with the discount portion cut off it.

    The bar is drawn as the whole marked price: the selling-price part stays and
    the discount part is physically cut away and slides aside, which is exactly
    the relation on the board -- marked price minus discount equals selling
    price.  Everything (both parts, their labels, the cut line) is ONE board
    object, so none of its own labels can ever be read as sitting inside
    somebody else's box.

    Attributes:
        .sp        the selling-price part that stays behind
        .disc      the discount part that is cut away
        .delta     the shift that separates the discount part from the bar
        .slot_x    where the (left-aligned) discount label starts
        .slot_y    the line that label is written on
        .cut_x     the x of the cut
    """
    disc_w = width * cut
    sp_w = width - disc_w
    x_left = cx - width / 2.0
    sp = Rectangle(width=sp_w, height=height, stroke_color=color_sp,
                   stroke_width=1.8, fill_color=color_sp, fill_opacity=0.32)
    sp.move_to(np.array([x_left + sp_w / 2.0, cy, 0.0]))
    disc = Rectangle(width=disc_w, height=height, stroke_color=color_disc,
                     stroke_width=1.8, fill_color=color_disc, fill_opacity=0.44)
    disc.move_to(np.array([x_left + sp_w + disc_w / 2.0, cy, 0.0]))
    cut_mark = DashedLine(
        np.array([x_left + sp_w, cy - height / 2.0 - 0.10, 0.0]),
        np.array([x_left + sp_w, cy + height / 2.0 + 0.10, 0.0]),
        stroke_color=CHALK_RED, stroke_width=2.0, dash_length=0.07)
    cut_mark.set_stroke(opacity=0)
    parts = [sp, disc, cut_mark]
    if sp_text:
        lab = board_text(sp_text, sp_size, color_sp, "BOLD")
        lab.move_to(sp.get_center())
        parts.append(lab)
        grp_lab = lab
    else:
        grp_lab = None
    if mp_note:
        note = board_text(mp_note, mp_size, CHALK_WHITE, "BOLD")
        note.move_to(np.array([cx, cy + height / 2.0 + 0.30, 0.0]))
        parts.append(note)
    grp = VGroup(*parts)
    grp.sp, grp.disc, grp.cut_mark, grp.sp_label = sp, disc, cut_mark, grp_lab
    grp.delta = np.array([float(slide), 0.0, 0.0])
    if slot_side == "left":
        # the label sits in the air the cut part leaves behind, between the
        # selling-price bar and the block that was cut off
        grp.slot_x = x_left + sp_w + 0.28
    else:
        grp.slot_x = x_left + sp_w + disc_w / 2.0 + slide + disc_w / 2.0 + 0.28
    grp.slot_y = cy
    grp.cut_x = x_left + sp_w
    return grp


def bar_arrow(cx, cy, width=BAR_W, color=CHALK_WHITE):
    """The full-width arrow under the bar: this whole bar is 100% = MP."""
    return DoubleArrow(np.array([cx - width / 2.0, cy, 0.0]),
                       np.array([cx + width / 2.0, cy, 0.0]),
                       buff=0.0, stroke_color=color, stroke_width=2.0,
                       tip_length=0.14, max_tip_length_to_length_ratio=0.2)


def price_pair(cx, cy, width, mp_text="", sp_text="", frac=0.94, height=BAR_H,
               color_mp=CHALK_AMBER, color_sp=CHALK_GREEN, size=15):
    """Two bars end to end: the marked price and the smaller selling price.

    Both are left-aligned, so the rupees the discount took off are visible as
    the gap at the right-hand end.  The pair is one board object.
    """
    x_left = cx - width / 2.0
    mp = Rectangle(width=width, height=height, stroke_color=color_mp,
                   stroke_width=1.8, fill_color=color_mp, fill_opacity=0.28)
    mp.move_to(np.array([x_left + width / 2.0, cy, 0.0]))
    sp = Rectangle(width=width * frac, height=height, stroke_color=color_sp,
                   stroke_width=1.8, fill_color=color_sp, fill_opacity=0.32)
    sp.move_to(np.array([x_left + width * frac / 2.0, cy - 0.55, 0.0]))
    gap = Rectangle(width=width * (1.0 - frac), height=height,
                    stroke_color=CHALK_PINK, stroke_width=1.8,
                    fill_color=CHALK_PINK, fill_opacity=0.46)
    gap.move_to(np.array([x_left + width * frac + width * (1.0 - frac) / 2.0,
                          cy, 0.0]))
    parts = [mp, sp, gap]
    if mp_text:
        lab = board_text(mp_text, size, CHALK_WHITE, "BOLD")
        lab.move_to(mp.get_center())
        parts.append(lab)
    if sp_text:
        lab = board_text(sp_text, size, CHALK_WHITE, "BOLD")
        lab.move_to(sp.get_center())
        parts.append(lab)
    grp = VGroup(*parts)
    grp.mp, grp.sp, grp.gap = mp, sp, gap
    grp.gap_delta = np.array([-0.30, 0.55, 0.0])
    grp.gap_slot = np.array([gap.get_center()[0], gap.get_center()[1], 0.0])
    return grp


# ----------------------------------------------------------------


NARRATION = {
    "title": (
        "Look at this price tag. The price written on it is one thousand six "
        "hundred rupees. <bookmark mark='b0'/> But that sticker says six "
        "percent off, <bookmark mark='b1'/> so the price you pay is not the "
        "price on the tag. Three quantities are at work here. The first is the "
        "marked price: the price written on the article, also called the list "
        "price. <bookmark mark='b2'/> The second is the discount: the amount "
        "reduced, and the same idea is also called a rebate. <bookmark "
        "mark='b3'/> The third is the selling price: what is actually paid. "
        "<bookmark mark='b4'/> One relation ties all three together: marked "
        "price minus discount equals selling price. <bookmark mark='b5'/> And "
        "the tagged price never disappears, because the discount is always "
        "calculated from it, <bookmark mark='b6'/> and never from the selling "
        "price."
    ),
    "s1": (
        "The price tag has three parts, and each part has a name. <bookmark "
        "mark='b0'/> The marked price is the price written on the article; it "
        "is also called the list price, or the catalogue price. <bookmark "
        "mark='b1'/> The discount is the amount that is reduced from that "
        "price, and the same idea is also called a rebate. <bookmark "
        "mark='b2'/> The selling price is what is actually paid at the "
        "counter. <bookmark mark='b3'/> One relation ties the three together: "
        "marked price minus discount equals selling price. <bookmark "
        "mark='b4'/> The tagged price never disappears, because the discount "
        "is always calculated from the marked price. <bookmark mark='b5'/> So "
        "keep the marked price on the board: the discount is only a part of "
        "it."
    ),
    "s2": (
        "A book is marked eighty rupees, and the shop gives fifteen percent "
        "off. <bookmark mark='b0'/> The marked price is the whole bar: one "
        "hundred percent, that is eighty rupees. <bookmark mark='b1'/> Step "
        "one is to find the discount, which is fifteen percent of the marked "
        "price: fifteen over one hundred times eighty is twelve rupees. "
        "<bookmark mark='b2'/> Step two is the selling price: remove that "
        "discount from the marked price, so eighty minus twelve is sixty eight "
        "rupees. <bookmark mark='b3'/> You can see the fifteen percent block "
        "cut away from the bar, and the selling price is what remains. "
        "<bookmark mark='b4'/> So marked price minus discount equals selling "
        "price. <bookmark mark='b5'/> And the discount is always calculated on "
        "the marked price, never on the selling price, <bookmark mark='b6'/> "
        "because the marked price is the base for every discount."
    ),
    "s3": (
        "Now let us find a discount percentage. <bookmark mark='b0'/> A "
        "bicycle is marked three thousand six hundred rupees, and it is sold "
        "for three thousand three hundred and twelve rupees. <bookmark "
        "mark='b1'/> The difference between the two prices is two hundred and "
        "eighty eight rupees, and you can see that gap at the end of the bars. "
        "<bookmark mark='b2'/> Now the discount percentage: its base is the "
        "marked price, never the selling price. <bookmark mark='b3'/> The gap "
        "is measured against the whole bar, so the percentage is two hundred "
        "and eighty eight divided by three thousand six hundred, times one "
        "hundred. <bookmark mark='b4'/> That is eight percent. <bookmark "
        "mark='b5'/> Always divide by the marked price, and never by the "
        "selling price."
    ),
    "s4": (
        "Now the other direction: the discount percentage is given, and we "
        "must find the selling price. <bookmark mark='b0'/> A ceiling fan is "
        "marked one thousand six hundred rupees, with six percent off. The "
        "discount is six percent of the marked price: six over one hundred "
        "times one thousand six hundred is ninety six rupees. <bookmark "
        "mark='b1'/> The selling price is the marked price minus the discount, "
        "so one thousand six hundred minus ninety six is one thousand five "
        "hundred and four rupees. <bookmark mark='b2'/> Notice that the "
        "discount amount is ninety six rupees, while the discount rate is six "
        "percent. <bookmark mark='b3'/> One is money, the other is a "
        "percentage of the marked price, <bookmark mark='b4'/> so keep the "
        "amount in rupees and the rate in percent, and never mix the two up."
    ),
    "s5": (
        "There is a shortcut, and it comes from one simple idea. <bookmark "
        "mark='b0'/> If six percent is taken off the marked price, then ninety "
        "four percent is still payable. <bookmark mark='b1'/> Route one: find "
        "the discount first, ninety six rupees, and subtract it from one "
        "thousand six hundred. <bookmark mark='b2'/> Route two: find the "
        "remaining percent first, ninety four percent, and multiply it by one "
        "thousand six hundred. <bookmark mark='b3'/> Both routes give one "
        "thousand five hundred and four rupees. <bookmark mark='b4'/> So the "
        "shortcut is: selling price equals one hundred minus d, over one "
        "hundred, times the marked price. <bookmark mark='b5'/> Use whichever "
        "route you like, but check that the two routes agree. <bookmark "
        "mark='b6'/> Two different routes are a free check on your answer."
    ),
    "s6": (
        "There are three questions you can be asked, and each one has its own "
        "route. <bookmark mark='b0'/> If the marked price and the discount "
        "percentage are given, find the discount first, and then subtract it "
        "from the marked price. <bookmark mark='b1'/> If the marked price and "
        "the selling price are given, find the discount by subtraction, and "
        "then divide that discount by the marked price, times one hundred. "
        "<bookmark mark='b2'/> If the marked price and the discount amount are "
        "given, the selling price is simply marked price minus discount. "
        "<bookmark mark='b3'/> In every case the first move is the same: find "
        "the discount, or find the marked price. <bookmark mark='b4'/> And in "
        "every case the base for a percentage is the marked price. <bookmark "
        "mark='b5'/> Read the question twice, and pick the route that fits the "
        "quantities you were given."
    ),
    "s7": (
        "Now the mistakes that cost marks, and the fix for each one. <bookmark "
        "mark='b0'/> The first mistake is calculating the discount percentage "
        "on the selling price instead of the marked price. <bookmark "
        "mark='b1'/> The second is adding the discount to the marked price, "
        "instead of subtracting it. <bookmark mark='b2'/> The third is "
        "confusing the discount amount, ninety six rupees, with the discount "
        "rate, six percent. <bookmark mark='b3'/> The fourth is reading "
        "fifteen percent off as if you pay fifteen percent, when eighty five "
        "percent is still payable. <bookmark mark='b4'/> So check three things "
        "every time: the base is the marked price, the discount is subtracted, "
        "and the rate is a percentage while the amount is in rupees. <bookmark "
        "mark='b5'/> Fix those four habits, and the marks stop leaking away."
    ),
    "s8": (
        "Before you write the answer, check that it makes sense. <bookmark "
        "mark='b0'/> A discount always makes the selling price smaller than "
        "the marked price, so the selling price must be less than the marked "
        "price. <bookmark mark='b1'/> And if d percent is taken off, then one "
        "hundred minus d percent is still payable. <bookmark mark='b2'/> Here "
        "the marked price is one thousand six hundred rupees, and the selling "
        "price is one thousand five hundred and four rupees, which is smaller. "
        "<bookmark mark='b3'/> Six percent off leaves ninety four percent "
        "payable, and six plus ninety four is one hundred. <bookmark "
        "mark='b4'/> So two checks every time: the selling price must be "
        "smaller than the marked price, and the two percentages must add up to "
        "one hundred. Write those two lines on your rough sheet before you "
        "answer."
    ),
    "s9q": (
        "Your turn. Four quick checks. <bookmark mark='b0'/> First: a shirt is "
        "marked four hundred and fifty rupees with seven percent off. Find the "
        "discount, and then the selling price. <bookmark mark='b1'/> Second: "
        "an article is marked one thousand rupees and sold for nine hundred "
        "rupees. Find the discount, and then the discount percentage. "
        "<bookmark mark='b2'/> Third: a table is marked two hundred and fifty "
        "rupees with five percent off. Find the selling price directly, using "
        "the percent that remains. <bookmark mark='b3'/> And last: check that "
        "every selling price you write is smaller than its marked price. Take "
        "your time, and pause the video if you need to."
    ),
    "s9a": (
        "Let us check. <bookmark mark='b0'/> For the shirt: seven percent of "
        "four hundred and fifty is thirty one rupees fifty, so the selling "
        "price is four hundred and fifty minus thirty one fifty, which is four "
        "hundred and eighteen rupees fifty. <bookmark mark='b1'/> For the "
        "article: the discount is one thousand minus nine hundred, that is one "
        "hundred rupees, and one hundred divided by one thousand, times one "
        "hundred, is ten percent. <bookmark mark='b2'/> For the table: five "
        "percent off leaves ninety five percent, and ninety five over one "
        "hundred times two hundred and fifty is two hundred and thirty seven "
        "rupees fifty. <bookmark mark='b3'/> And in all three the selling "
        "price is smaller than the marked price, and the base was the marked "
        "price. Check both of those every time, and your answers will be right."
    ),
    "s10": (
        "The whole chapter in four lines. <bookmark mark='b0'/> One: the "
        "marked price is the price written on the article, and the discount, "
        "or rebate, is calculated from it. <bookmark mark='b1'/> Two: the "
        "selling price is what is actually paid, and selling price equals "
        "marked price minus discount. <bookmark mark='b2'/> Three: the "
        "discount percentage is the discount divided by the marked price, "
        "times one hundred. <bookmark mark='b3'/> Four: the price flow is tag, "
        "reduce, pay, compare. <bookmark mark='b4'/> So keep the marked price "
        "visible, subtract the discount, and check the answer against the tag. "
        "<bookmark mark='b5'/> Thank you for watching, <bookmark mark='b6'/> "
        "and see you in the next lesson."
    ),
}


class DiscountsMarkedPriceAndRebateStory(VoiceoverScene):
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
        out_dir = _HERE / "media" / "videos" / "discounts_marked_price_and_rebate"
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
    # Discounts, Marked Price & Rebate (Class 8 Maths, Chapter 5, Storymode 02).
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
    #   * every row of cards is centred on BOARD_CX (`hrow` / `row_centres`) and
    #     two texts never come closer than the 0.22 units the clearance audit
    #     asks for -- which is why every card spaces its own lines by 0.26;
    #   * the marked price never leaves the board: the tag stays up through the
    #     scene while the discount is cut away from the bar, and the discount
    #     AMOUNT (rupees) is always drawn apart from the discount RATE (percent);
    #   * a drawn cross always lives in the same VGroup as the statement it
    #     strikes through (otherwise the audit reads the strokes as a line
    #     running into somebody else's card);
    #   * the challenge uses the series' shared 10-second THINK clock, dead
    #     centre of the board, and the four prompt cards sit in the four corners
    #     so the badge never covers one.

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

    def answer_row(self, tag, headline, note, color, width=8.60, height=0.62,
                   pad=0.30, buff=0.34):
        """One revealed step or answer: its number, the work and the result.

        The row is laid out in FIXED COLUMNS rather than centred in its box, so
        the number column and the text columns are the same vertical line in
        every row (centring put each number at a different x).  The box itself
        stays where the caller puts it.  The same helper draws the recap list.
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
        grp = VGroup(box, row)
        grp.box, grp.row = box, row
        return grp

    def q_card(self, title, pict, color=CHALK_CYAN, width=3.00, pad=0.14,
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

    # -- Scene 0: title ------------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            heading = at(board_text("Discounts, Marked Price & Rebate", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The tag price is not always the price you pay.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            tag = at(price_tag("Rs 1600", size=24), BOARD_CX, 1.05)
            sticker = price_sticker("6% OFF", 2.45, 1.45, r=0.52)

            c1 = chip("MARKED PRICE (MP)", CHALK_GREEN, size=15)
            c2 = chip("DISCOUNT / REBATE", CHALK_AMBER, size=15)
            c3 = chip("SELLING PRICE (SP)", CHALK_CYAN, size=15)
            self.hrow(c1, c2, c3, y=-0.30, gap=0.45)

            formula = at(chalk_math(r"\text{MP} - \text{Discount} = \text{SP}",
                                    size=30, color=CHALK_YELLOW),
                         BOARD_CX, BANNER_Y)
            strip = at(board_text("The tagged price never disappears: the "
                                  "discount is a part of it.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(tag, scale=0.9), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(sticker, scale=0.85), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(c1, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(c2, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(c3, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(formula, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: the three parts, and the relation --------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Three Parts of a Price", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Marked price, discount, selling price.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            c1 = list_card("MARKED PRICE",
                           ["price written on the article",
                            "also called the list price"], CHALK_GREEN,
                           width=2.90, height=1.47)
            c2 = list_card("DISCOUNT",
                           ["the amount reduced",
                            "also called the rebate"], CHALK_AMBER,
                           width=2.90, height=1.47)
            c3 = list_card("SELLING PRICE",
                           ["what is actually paid",
                            "SP = MP - D"], CHALK_CYAN,
                           width=2.90, height=1.47)
            for card, cx in zip((c1, c2, c3),
                                row_centres((1.45, 1.45, 1.45), 0.45)):
                at(card, cx, 1.02)

            formula = at(chalk_math(r"\text{MP} - \text{Discount} = \text{SP}",
                                    size=28, color=CHALK_YELLOW), 1.60, -0.45)
            tag = at(price_tag("Rs 80", size=22), -3.20, -0.45)
            strip = at(board_text("The discount is always calculated from the "
                                  "marked price.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(c1, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(c2, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(c3, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(formula, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(tag, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: the book -- find the discount, then the SP -----------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Discount Comes First", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A book marked Rs 80 at 15% off.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            book = at(book_icon(0, 0, "Rs 80", CHALK_CYAN, scale=1.0),
                      -3.35, 1.42)
            sticker = price_sticker("15% OFF", -2.05, 1.60, r=0.48)

            r1 = at(self.answer_row("1", "DISCOUNT = 15/100 × 80", "= Rs 12",
                                    CHALK_GREEN, width=6.30), 1.75, 1.60)
            r2 = at(self.answer_row("2", "SP = 80 - 12", "= Rs 68", CHALK_CYAN,
                                    width=6.30), 1.75, 0.90)

            # the marked price bar: 100% is Rs 80, and the 15% block is cut off
            bar = split_bar(-1.0, 0.05, width=BAR_W, cut=0.15,
                            sp_text="SP = 85% of MP", sp_size=14, slide=1.10)
            arrow = bar_arrow(-1.0, -0.32, width=BAR_W)
            mp_lab = at(board_text("100% = MP = Rs 80", 14, CHALK_WHITE,
                                   "BOLD"), -1.0, -0.48)
            d_lab = board_text("DISCOUNT 15% = Rs 12", 14, CHALK_PINK, "BOLD")
            d_lab.move_to(np.array([bar.slot_x + d_lab.width / 2.0,
                                    bar.slot_y, 0.0]))
            coins = at(coin_stack(0, 0, 3, 0.9), 4.60, -0.55)

            formula = at(chalk_math(r"\text{MP} - \text{Discount} = \text{SP}",
                                    size=28, color=CHALK_YELLOW),
                         BOARD_CX, BANNER_Y)
            strip = at(board_text("The discount is always calculated on the "
                                  "marked price.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(book, scale=0.9), FadeIn(sticker, scale=0.85),
                      run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(bar, scale=0.95), FadeIn(arrow), FadeIn(mp_lab),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(r1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(r2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(bar.disc.animate.shift(bar.delta),
                      bar.cut_mark.animate.set_stroke(opacity=1),
                      FadeIn(d_lab, shift=UP * 0.06), FadeIn(coins, scale=0.9),
                      run_time=0.70)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(formula, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: the cycle -- from the two prices to the discount percent ---
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Finding the Discount Percent", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A cycle marked Rs 3600, sold for Rs 3312.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            bike = at(cycle_icon(0, 0, "Rs 3600", CHALK_AMBER, scale=0.92),
                      -3.50, 1.30)
            pair = price_pair(1.00, 1.10, 6.00, mp_text="MP = Rs 3600",
                              sp_text="SP = Rs 3312", frac=0.92)
            rs = at(board_text("Rs 288", 16, CHALK_PINK, "BOLD"), 4.45, 1.10)

            diff = at(chip("DISCOUNT = 3600 - 3312 = Rs 288", CHALK_AMBER,
                           size=14), BOARD_CX, -0.35)
            base = at(chip("THE BASE IS THE MARKED PRICE", CHALK_PINK,
                           size=14), BOARD_CX, -0.95)
            percent = at(chip("d% = 288/3600 × 100 = 8%", CHALK_YELLOW,
                              size=15), BOARD_CX, -0.35)
            strip = at(board_text("Always divide by the marked price, and never "
                                  "by the selling price.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(bike, scale=0.9), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(pair, scale=0.96), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(rs, scale=0.9), FadeIn(diff, shift=UP * 0.06),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(base, shift=UP * 0.06),
                      pair.gap.animate.shift(pair.gap_delta),
                      rs.animate.shift(pair.gap_delta), run_time=0.65)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeOut(diff), FadeIn(percent, shift=UP * 0.06),
                      run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: the fan -- given the percent, find the selling price -------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("Given the Discount, Find the SP", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A fan marked Rs 1600 with 6% off.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fan = at(fan_icon(0, 0, "Rs 1600", CHALK_CYAN, scale=0.95),
                     -3.55, 1.30)
            sticker = price_sticker("6% OFF", -2.62, 1.70, r=0.46)

            r1 = at(self.answer_row("1", "DISCOUNT = 6/100 × 1600", "= Rs 96",
                                    CHALK_GREEN, width=6.40), 1.80, 1.55)
            r2 = at(self.answer_row("2", "SP = 1600 - 96", "= Rs 1504",
                                    CHALK_CYAN, width=6.40), 1.80, 0.85)

            amt = chip("DISCOUNT AMOUNT = Rs 96", CHALK_AMBER, size=14)
            neq = chalk_math(r"\neq", size=26, color=CHALK_RED)
            rate = chip("DISCOUNT RATE = 6%", CHALK_PINK, size=14)
            self.hrow(amt, neq, rate, y=-0.45, gap=0.45)
            notes = at(note_stack(0, 0, 3, 0.9), 4.20, -0.45)

            strip = at(board_text("The amount is in rupees; the rate is a "
                                  "percentage of the marked price.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(fan, scale=0.9), FadeIn(sticker, scale=0.85),
                      run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(r1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(r2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(amt, scale=0.9), FadeIn(rate, scale=0.9),
                      FadeIn(neq, scale=0.9), FadeIn(notes, scale=0.9),
                      run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: the shortcut -- what remains is (100 - d)% ----------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Shortcut: What Remains", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("If 6% is taken off, 94% remains.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            r1 = at(self.answer_row("1", "FIND D, THEN SUBTRACT",
                                    "Rs 96, then 1600 - 96", CHALK_GREEN,
                                    width=8.60), BOARD_CX, 1.60)
            r2 = at(self.answer_row("2", "FIND WHAT REMAINS",
                                    "94/100 × 1600 = Rs 1504", CHALK_CYAN,
                                    width=8.60), BOARD_CX, 0.90)

            # the same thousand-six-hundred bar: 6% is cut away, 94% stays
            bar = split_bar(-1.0, 0.05, width=BAR_W, cut=0.06,
                            sp_text="SP = 94% of MP", sp_size=14, slide=1.60,
                            slot_side="left")
            arrow = bar_arrow(-1.0, -0.32, width=BAR_W)
            mp_lab = at(board_text("100% = MP = Rs 1600", 14, CHALK_WHITE,
                                   "BOLD"), -1.0, -0.48)
            d_lab = board_text("6% = Rs 96", 14, CHALK_PINK, "BOLD")
            d_lab.move_to(np.array([bar.slot_x + d_lab.width / 2.0,
                                    bar.slot_y, 0.0]))

            tick1 = tick(np.array([5.05, 1.60, 0.0]))
            tick2 = tick(np.array([5.05, 0.90, 0.0]))
            same = at(chip("BOTH ROUTES GIVE Rs 1504", CHALK_YELLOW, size=14),
                      3.15, -0.55)
            formula = at(chalk_math(
                r"SP = \frac{100 - d}{100} \times MP", size=24,
                color=CHALK_YELLOW), BOARD_CX, BANNER_Y)
            strip = at(board_text("Both routes land on the same selling price, "
                                  "Rs 1504.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(bar, scale=0.95), FadeIn(arrow), FadeIn(mp_lab),
                      run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(bar.disc.animate.shift(bar.delta),
                      bar.cut_mark.animate.set_stroke(opacity=1),
                      FadeIn(d_lab, shift=UP * 0.06), run_time=0.65)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(r1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(r2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(tick1, scale=0.8), FadeIn(tick2, scale=0.8),
                      FadeIn(same, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(formula, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: which formula? --------------------------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("Which Formula Do I Need?", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Look at what the question gives you.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            c1 = list_card("MP + DISCOUNT %",
                           ["find the discount", "then SP = MP - D"],
                           CHALK_GREEN, width=2.90, height=1.47)
            c2 = list_card("MP + SP",
                           ["find D = MP - SP", "then D / MP × 100"],
                           CHALK_CYAN, width=2.90, height=1.47)
            c3 = list_card("MP + DISCOUNT Rs",
                           ["SP = MP - D", "the discount is given"],
                           CHALK_AMBER, width=2.90, height=1.47)
            for card, cx in zip((c1, c2, c3),
                                row_centres((1.45, 1.45, 1.45), 0.45)):
                at(card, cx, 1.05)

            first = at(chip("FIRST FIND THE DISCOUNT", CHALK_YELLOW, size=15),
                       BOARD_CX, BAND_B)
            banner = at(board_text("THE BASE IS ALWAYS THE MARKED PRICE", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Read the question twice, and pick the route "
                                  "that fits.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(c1, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(c2, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(c3, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(first, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: the four mistakes, and the fix for each --------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Common Mistakes and Their Fixes", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Four wrong ideas, four corrections.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            cards = (
                ("d% = D / SP × 100", "the base is the marked price, not SP"),
                ("SP = MP + D", "subtract: SP = MP - D"),
                ("6% = Rs 6", "6% is the rate, Rs 96 the amount"),
                ("15% off means pay 15%", "85% is still payable"),
            )
            centres = row_centres((2.025, 2.025), 0.42)
            rows = (1.10, -0.30)
            built = []
            for i, (wrong, fix) in enumerate(cards):
                card = mistake_card(wrong, fix, CHALK_RED, width=4.05,
                                    height=1.10)
                at(card, centres[i % 2], rows[i // 2])
                built.append(card)
            m1, m2, m3, m4 = built

            checks = self.hrow(chip("BASE = MP", CHALK_GREEN, size=14),
                               chip("SUBTRACT, NEVER ADD", CHALK_YELLOW,
                                    size=14),
                               chip("RATE % vs AMOUNT Rs", CHALK_CYAN,
                                    size=14), y=-1.15, gap=0.40)
            strip = at(board_text("Check the base, the sign, and the units, "
                                  "every time.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(m1, scale=0.92), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(m2, scale=0.92), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(m3, scale=0.92), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(m4, scale=0.92), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(checks, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: does the answer make sense? --------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("Does the Answer Make Sense?", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Check the selling price against the marked "
                                "price.", 17, CHALK_WHITE, "BOLD"),
                     BOARD_CX, SUB_Y)

            c1 = list_card("A DISCOUNT SHRINKS SP",
                           ["so always check SP < MP"], CHALK_GREEN,
                           width=3.60, height=1.05, head_size=14)
            c2 = list_card("d% OFF LEAVES (100 - d)%",
                           ["6% off leaves 94% payable"], CHALK_PINK,
                           width=3.60, height=1.05, head_size=14)
            for card, cx in zip((c1, c2), row_centres((1.80, 1.80), 0.50)):
                at(card, cx, 1.20)

            pair = price_pair(0.50, 0.20, 5.60, mp_text="MP = Rs 1600 = 100%",
                              sp_text="SP = Rs 1504 = 94%", frac=0.94)
            check = at(chip("SO SP < MP: THE CHECK PASSES", CHALK_YELLOW,
                            size=15), BOARD_CX, BANNER_Y)
            good = tick(np.array([3.35, -0.35, 0.0]))
            strip = at(board_text("Check SP < MP, and check that d plus "
                                  "(100 - d) makes 100.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(c1, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(c2, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(pair, scale=0.96), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(good, scale=0.8), FadeIn(check, scale=0.9),
                      run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
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

            pic_a = VGroup(board_text("MP = Rs 450, 7% off", 12, CHALK_GREEN,
                                      "BOLD"),
                           board_text("find D, then SP", 12, CHALK_GREEN,
                                      "BOLD")).arrange(DOWN, buff=0.26)
            pic_b = VGroup(board_text("MP = Rs 1000", 12, CHALK_CYAN, "BOLD"),
                           board_text("SP = Rs 900: find D%", 12, CHALK_CYAN,
                                      "BOLD")).arrange(DOWN, buff=0.26)
            pic_c = VGroup(board_text("MP = Rs 250, 5% off", 12, CHALK_AMBER,
                                      "BOLD"),
                           board_text("find SP using 95%", 12, CHALK_AMBER,
                                      "BOLD")).arrange(DOWN, buff=0.26)
            pic_d = VGroup(board_text("is SP smaller than MP?", 12, CHALK_PINK,
                                      "BOLD"),
                           board_text("check every answer", 12, CHALK_PINK,
                                      "BOLD")).arrange(DOWN, buff=0.26)

            qa = at(self.q_card("A · SHIRT", pic_a, CHALK_GREEN), -2.85, 0.80)
            qb = at(self.q_card("B · ARTICLE", pic_b, CHALK_CYAN), 3.65, 0.80)
            qc = at(self.q_card("C · TABLE", pic_c, CHALK_AMBER), -2.85, -0.95)
            qd = at(self.q_card("D · CHECK", pic_d, CHALK_PINK), 3.65, -0.95)

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

            # the questions are read: hold the board for the rest of the window
            self.closing(tracker)
            self._capture_srt(tracker)

        # The ten-second THINK pause is deliberately SILENT: the questions have
        # just been read, so the clock ticks alone, with no narration to sync
        # against.
        play_challenge_countdown(self, seconds=10, sfx=self.sfx,
                                 position=np.array([BOARD_CX, BOARD_CY, 0]))

        with self.voiceover(text=NARRATION["s9a"]) as tracker:
            self.wait(leftover(tracker, "b0"))
            self.play(FadeOut(qa), FadeOut(qb), FadeOut(qc), FadeOut(qd),
                      run_time=0.55)
            a1 = at(self.answer_row("A", "discount Rs 31.50",
                                    "SP = 450 - 31.50 = Rs 418.50",
                                    CHALK_GREEN), BOARD_CX, 1.50)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "discount Rs 100",
                                    "d% = 100/1000 × 100 = 10%", CHALK_CYAN),
                    BOARD_CX, 0.70)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "95% remains",
                                    "SP = 95/100 × 250 = Rs 237.50",
                                    CHALK_AMBER), BOARD_CX, -0.10)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            strip = at(board_text("The base is the marked price, and SP is "
                                  "always smaller than MP.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap and the spoken thank-you ----------------------------
    def beat_s10(self) -> None:
        with self.voiceover(text=NARRATION["s10"]) as tracker:
            self.reset_board()

            heading = at(board_text("Marked Price to Selling Price", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)

            r1 = at(self.answer_row("1", "MARKED PRICE",
                                    "the price written on the article (MP)",
                                    CHALK_GREEN), BOARD_CX, 1.48)
            r2 = at(self.answer_row("2", "DISCOUNT OR REBATE",
                                    "the amount reduced: SP = MP - D",
                                    CHALK_CYAN), BOARD_CX, 0.72)
            r3 = at(self.answer_row("3", "DISCOUNT PERCENT",
                                    "D% = (MP - SP) / MP × 100",
                                    CHALK_YELLOW), BOARD_CX, -0.04)
            r4 = at(self.answer_row("4", "THE PRICE FLOW",
                                    "tag, reduce, pay, compare", CHALK_AMBER),
                    BOARD_CX, -0.80)
            strip = at(board_text("Keep the marked price visible, subtract the "
                                  "discount, check the answer.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)
            thanks = at(board_text("Thank You for Watching!", 30, CHALK_WHITE,
                                   "BOLD"), BOARD_CX, 0.62)
            bye = at(board_text("See you in the next lesson :)", 22,
                                CHALK_YELLOW, "BOLD"), BOARD_CX, -0.32)

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

            # The four lines stay on the board through the whole closing
            # sentence: the strip is written on its own bookmark as the voice
            # says it, and only the bookmark in front of "Thank you for
            # watching," clears the board and brings in the card.
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

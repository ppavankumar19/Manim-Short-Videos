"""
Compound Ratio & Inverse Ratio: Applications in Business Profit Sharing
Story-mode chalkboard lesson (Class 8 Maths, Chapter 5: Comparing Quantities
using Proportion, Storymode 01).

LLM KEY / FUNCTION NAME: compound_ratio_and_business_proportions

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

The defining visual is TWO PARTNERS AND ONE PROFIT BAG: Ramayya's money and
time card, Gopalam's money and time card, the profit bag between them, the two
ratios that must be combined, the compound-ratio machine the ratio cards go
into, and the equal profit blocks that physically move to the two partners.

Title + 10 scenes:
  0. Title card: two partners, one profit, and the question of an equal share.
  1. A ratio is ordered; the inverse ratio swaps the terms.
  2. Same time: the time factor cancels, so the profit follows the capital
     ratio 2 : 3.
  3. Same capital: the capital factor cancels, so the profit follows the time
     ratio 4 : 3.
  4. Both different: neither ratio alone is enough, so they must be combined.
  5. The compound ratio rule: a:b and c:d give ac:bd -- and the common
     (a + c):(b + d) mistake, struck through with a drawn cross.
  6. Applying it: (2:3) and (4:3) give 8:9, cross-checked with money x time.
  7. From ratio to rupees: Rs 17,000 in 17 equal parts of Rs 1,000.
  8. The decision map: same time, same capital, or both different.
  9. Your turn: inverse, compound, and a two-partner challenge after the
     series' centred ten-second THINK clock.
 10. Recap: inverse, compound, partnership -- and the spoken thank-you card.
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


# (this section is spliced into a head whose own imports omit Ellipse, Arc,
#  Sector and Rotate; Dot, Circle, Line, Polygon, RoundedRectangle, VGroup,
#  DEGREES and np are already imported by the head)
from manim import Arc, Ellipse, Rotate, Sector  # noqa: E402,F401

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
BAND_A = 0.70            # the upper band (partner cards, input cards)
BAND_B = -0.50           # the lower band (the result of the upper band)

PANEL_FILL = "#16202B"
CARD_W = 3.30            # the standard card width
CARD_H = 0.94            # the standard card height
CHIP_H = 0.50
MARK_SIZE = 18           # ONE letter size for every labelled figure
DOT_R = 0.075
COIN_R = 0.17

# The example figures this video works with.  Both the profit total and the
# challenge amounts are marked on screen as examples, never as textbook facts.
RAMAYYA = ("Ramayya", "Rs 2,000", "for 12 months", CHALK_GREEN)
GOPALAM = ("Gopalam", "Rs 3,000", "for 9 months", CHALK_PINK)
CAP_RATIO = (2, 3)
TIME_RATIO = (4, 3)
COMPOUND = (8, 9)
PROFIT_TOTAL = 17000
PART_VALUE = 1000


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


def person_icon(cx, cy, color=CHALK_CYAN, scale=1.0):
    """A small filled figure: a round head over a pair of shoulders."""
    head = Circle(radius=0.105 * scale, stroke_width=0,
                  fill_color=color, fill_opacity=0.9)
    head.move_to(np.array([cx, cy + 0.15 * scale, 0.0]))
    body = Ellipse(width=0.40 * scale, height=0.28 * scale, stroke_width=0,
                   fill_color=color, fill_opacity=0.5)
    body.move_to(np.array([cx, cy - 0.10 * scale, 0.0]))
    return VGroup(body, head)


def partner_card(name, money, months, color=CHALK_GREEN, width=CARD_W,
                 height=CARD_H, name_size=17, line_size=13):
    """One partner's card: their name, their money and their time.

    The figure (a filled head over shoulders) sits in the card's left margin, so
    the two partners read as two people and not just two rows of numbers.  The
    card's own two lines are spaced 0.22 apart -- the tightest the clearance
    audit allows two texts to come.
    """
    box = panel(width, height, color)
    icon = person_icon(-width / 2 + 0.42, 0.0, color)
    head = board_text(name, name_size, color, "BOLD")
    line = board_text(f"{money} · {months}", line_size, CHALK_WHITE, "BOLD")
    txt = VGroup(head, line).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
    txt.move_to(np.array([-width / 2 + 0.95 + txt.width / 2.0, 0.0, 0.0]))
    grp = VGroup(box, icon, txt)
    grp.box, grp.icon, grp.line, grp.name = box, icon, line, head
    return grp


def ratio_card(a, b, color=CHALK_AMBER, width=1.62, height=0.72, size=26):
    """A ratio written in a box -- the object that slides and flips."""
    tex = chalk_math(f"{a} : {b}", size=size, color=color)
    box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                           stroke_color=color, stroke_width=2.0,
                           fill_color=PANEL_FILL, fill_opacity=0.6)
    tex.move_to(box.get_center())
    grp = VGroup(box, tex)
    grp.box, grp.tex = box, tex
    return grp


def money_bag(cx, cy, scale=1.0, color=CHALK_AMBER, text="PROFIT",
              size=16, coins=True):
    """The profit bag: a filled, shaded bag with a tied neck (and coins)."""
    body = Ellipse(width=0.94 * scale, height=0.78 * scale, stroke_color=color,
                   stroke_width=2.6, fill_color=color, fill_opacity=0.24)
    body.move_to(np.array([cx, cy - 0.12 * scale, 0.0]))
    neck = Polygon(np.array([cx - 0.19 * scale, cy + 0.16 * scale, 0.0]),
                   np.array([cx + 0.19 * scale, cy + 0.16 * scale, 0.0]),
                   np.array([cx + 0.30 * scale, cy - 0.04 * scale, 0.0]),
                   np.array([cx - 0.30 * scale, cy - 0.04 * scale, 0.0]),
                   stroke_color=color, stroke_width=2.2,
                   fill_color=color, fill_opacity=0.24)
    tie = Line(np.array([cx - 0.30 * scale, cy + 0.15 * scale, 0.0]),
               np.array([cx + 0.30 * scale, cy + 0.15 * scale, 0.0]),
               stroke_color=CHALK_RED, stroke_width=3.4)
    # the label sits clear of the bag's own neck, so the audit's polygon
    # clearance check stays green
    lab = board_text(text, size, CHALK_WHITE, "BOLD")
    lab.move_to(np.array([cx, cy - 0.30 * scale, 0.0]))
    grp = VGroup(body, neck, tie, lab)
    grp.label = lab
    if coins:
        grp.add(coin_stack(cx - 0.60 * scale, cy - 0.44 * scale, 3, scale))
        grp.add(coin_stack(cx + 0.60 * scale, cy - 0.44 * scale, 3, scale))
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


def profit_blocks(count, color=CHALK_GREEN, side=0.24, gap=0.08, rows=1):
    """`count` equal solid blocks -- one block for one equal part of a profit.

    With `rows` > 1 the blocks are laid out in that many rows (bottom row
    first) and the whole block area is centred on the origin, so `at()` places
    it anywhere on the board.
    """
    per_row = int(np.ceil(count / rows))
    blocks = VGroup()
    for i in range(count):
        r, c = divmod(i, per_row)
        b = Square(side_length=side, stroke_color=color, stroke_width=1.6,
                   fill_color=color, fill_opacity=0.42)
        b.move_to(np.array([(c - (per_row - 1) / 2.0) * (side + gap),
                            (r - (rows - 1) / 2.0) * (side + gap), 0.0]))
        blocks.add(b)
    return blocks


def machine(width=4.60, height=1.50, title="COMPOUND RATIO MACHINE",
            color=CHALK_CYAN, formula=None, size=15):
    """The share machine: a filled box that two ratio cards go into.

    Its own heading and its own output formula live inside the one box, so the
    whole machine is a single board object.
    """
    box = RoundedRectangle(corner_radius=0.12, width=width, height=height,
                           stroke_color=color, stroke_width=2.4,
                           fill_color=PANEL_FILL, fill_opacity=0.62)
    head = board_text(title, size, color, "BOLD")
    head.move_to(box.get_top() + DOWN * 0.27)
    parts = [box, head]
    if formula is not None:
        parts.append(formula)
    grp = VGroup(*parts)
    grp.box, grp.head = box, head
    return grp


def funnel(cx, cy, width=0.80, height=0.46, color=CHALK_AMBER):
    """A small filled funnel: what goes into the machine on its left."""
    top = Line(np.array([cx - width / 2, cy + height / 2, 0.0]),
               np.array([cx + width / 2, cy + height / 2, 0.0]),
               stroke_color=color, stroke_width=2.4)
    left = Line(np.array([cx - width / 2, cy + height / 2, 0.0]),
                np.array([cx, cy - height / 2, 0.0]),
                stroke_color=color, stroke_width=2.4)
    right = Line(np.array([cx + width / 2, cy + height / 2, 0.0]),
                 np.array([cx, cy - height / 2, 0.0]),
                 stroke_color=color, stroke_width=2.4)
    body = Polygon(np.array([cx - width / 2, cy + height / 2, 0.0]),
                   np.array([cx + width / 2, cy + height / 2, 0.0]),
                   np.array([cx, cy - height / 2, 0.0]),
                   stroke_width=0, fill_color=color, fill_opacity=0.20)
    return VGroup(body, top, left, right)


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


def note_card(head, lines, color=CHALK_CYAN, width=3.40, height=1.05,
              head_size=15, line_size=13):
    """A card with a bold head line and one or two body lines under it.

    The head and the body are held 0.275 units apart, so the pair passes the
    clearance audit (which flags any two texts closer than 0.22).
    """
    box = panel(width, height, color)
    h = board_text(head, head_size, color, "BOLD")
    body = VGroup(*[board_text(line, line_size, CHALK_WHITE, "BOLD")
                    for line in lines]).arrange(DOWN, buff=0.24)
    h.move_to(box.get_center() + UP * 0.26)
    body.move_to(box.get_center() + DOWN * 0.26)
    grp = VGroup(box, h, body)
    grp.box, grp.head, grp.body = box, h, body
    return grp


def ratio_math(a, b, color=CHALK_AMBER, size=26):
    """A ratio as board maths."""
    return chalk_math(f"{a} : {b}", size=size, color=color)


def rupe(text, color=CHALK_WHITE, size=15):
    """A rupee amount as board text (the word 'Rs', which always renders)."""
    return board_text(text, size, color, "BOLD")


# ----------------------------------------------------------------


NARRATION = {
    "title": (
        "Meet two partners. <bookmark mark='b0'/>Ramayya invests two thousand "
        "rupees, and keeps that money in the business for twelve months. "
        "<bookmark mark='b1'/>Gopalam invests three thousand rupees for nine "
        "months. <bookmark mark='b2'/>At the end of the year the business earns "
        "a profit. <bookmark mark='b3'/>Should the two partners share that "
        "profit equally? <bookmark mark='b4'/>No. Profit in a partnership is "
        "shared in the ratio of what each partner contributed."
    ),
    "s1": (
        "A ratio is an ordered comparison. <bookmark mark='b0'/>Three to two is "
        "not the same as two to three. <bookmark mark='b1'/>The order of the "
        "two terms matters. <bookmark mark='b2'/>If we swap the two terms of a "
        "ratio, we get its inverse ratio: a to b becomes b to a. <bookmark "
        "mark='b3'/>So the inverse of four to five is five to four. <bookmark "
        "mark='b4'/>Inverse means swap the terms. It never means add them, and "
        "it never means change their signs."
    ),
    "s2": (
        "Now suppose both partners keep their money in for the same time. "
        "<bookmark mark='b0'/>Ramayya invests two thousand rupees for twelve "
        "months. <bookmark mark='b1'/>Gopalam also invests for twelve months, "
        "but he puts in three thousand rupees. <bookmark mark='b2'/>The time is "
        "the same for both, so the time factor cancels. <bookmark mark='b3'/>The "
        "capitals are in the ratio two thousand to three thousand, which "
        "simplifies to two to three. <bookmark mark='b4'/>So the profit is "
        "divided in the ratio two to three."
    ),
    "s3": (
        "Now suppose both partners invest the same capital. <bookmark "
        "mark='b0'/>Each of them invests five thousand rupees. <bookmark "
        "mark='b1'/>But Ramayya keeps his money in for twelve months, while "
        "Gopalam keeps his in for only nine months. <bookmark mark='b2'/>The "
        "capital is the same for both, so the capital factor cancels. <bookmark "
        "mark='b3'/>The times are in the ratio twelve to nine, and that "
        "simplifies to four to three. <bookmark mark='b4'/>So here the profit "
        "follows the time ratio, four to three."
    ),
    "s4": (
        "But in our business, both the money and the time are different. "
        "<bookmark mark='b0'/>Ramayya gives two thousand rupees for twelve "
        "months. <bookmark mark='b1'/>Gopalam gives three thousand rupees for "
        "nine months. <bookmark mark='b2'/>The capital ratio is two to three. "
        "<bookmark mark='b3'/>The time ratio is twelve to nine, that is four to "
        "three. <bookmark mark='b4'/>Neither ratio alone can decide the profit, "
        "so the two ratios must be combined."
    ),
    "s5": (
        "To combine two ratios we use the compound ratio. <bookmark "
        "mark='b0'/>For the ratios a to b and c to d, multiply the first terms "
        "together, <bookmark mark='b1'/>and multiply the second terms together. "
        "<bookmark mark='b2'/>The compound ratio is a times c to b times d. "
        "<bookmark mark='b3'/>A common mistake is to add the terms instead, and "
        "write a plus c to b plus d. <bookmark mark='b4'/>That is wrong. A "
        "compound ratio multiplies corresponding terms; it never adds them."
    ),
    "s6": (
        "Let us apply the rule. <bookmark mark='b0'/>We multiply the capital "
        "ratio two to three <bookmark mark='b1'/>by the time ratio four to "
        "three. <bookmark mark='b2'/>Two times four is eight, and three times "
        "three is nine, so the compound ratio is eight to nine. <bookmark "
        "mark='b3'/>Let us cross-check with money multiplied by time. Two "
        "thousand times twelve is twenty four thousand, and three thousand times "
        "nine is twenty seven thousand. <bookmark mark='b4'/>Twenty four "
        "thousand to twenty seven thousand simplifies to eight to nine, so the "
        "compound ratio is correct."
    ),
    "s7": (
        "Now let us turn that ratio into rupees. <bookmark mark='b0'/>Suppose "
        "the profit for the year is seventeen thousand rupees. This total is an "
        "example, not a textbook figure. <bookmark mark='b1'/>The ratio is eight "
        "to nine, so the profit is divided into eight plus nine, that is "
        "seventeen, equal parts. <bookmark mark='b2'/>Seventeen thousand divided "
        "by seventeen gives one thousand rupees for each part. <bookmark "
        "mark='b3'/>Ramayya takes eight parts, that is eight thousand rupees. "
        "<bookmark mark='b4'/>Gopalam takes nine parts, that is nine thousand "
        "rupees, and eight thousand plus nine thousand is seventeen thousand. "
        "The whole profit is shared."
    ),
    "s8": (
        "Here is the decision rule to remember. <bookmark mark='b0'/>If the "
        "time is the same, share the profit in the ratio of the capitals. "
        "<bookmark mark='b1'/>If the capital is the same, share it in the ratio "
        "of the times. <bookmark mark='b2'/>If both the capital and the time are "
        "different, share it in the compound ratio of capital and time. "
        "<bookmark mark='b3'/>So the share of the profit follows capital "
        "multiplied by time."
    ),
    "s9q": (
        "Your turn. Four quick checks. <bookmark mark='b0'/>First: write the "
        "inverse of the ratio seven to five. <bookmark mark='b1'/>Second: find "
        "the compound ratio of three to four and two to three. <bookmark "
        "mark='b2'/>Third: compound three to four with the inverse of four to "
        "five. <bookmark mark='b3'/>And last: partner P invests four thousand "
        "rupees for six months, and partner Q invests three thousand rupees for "
        "eight months. In what ratio should they share the profit?"
    ),
    "s9a": (
        "<bookmark mark='b0'/>The inverse of seven to five is five to seven, "
        "because the inverse swaps the two terms. <bookmark mark='b1'/>The "
        "compound ratio of three to four and two to three is six to twelve, "
        "which simplifies to one to two. <bookmark mark='b2'/>Three to four, "
        "compounded with the inverse of four to five, is three times five to "
        "four times four, that is fifteen to sixteen. <bookmark mark='b3'/>And "
        "for P and Q, four thousand times six is twenty four thousand, and three "
        "thousand times eight is also twenty four thousand. So the ratio is one "
        "to one, and the two partners share the profit equally."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>The inverse ratio swaps the two "
        "terms: a to b becomes b to a. <bookmark mark='b1'/>The compound ratio "
        "multiplies corresponding terms: a to b and c to d give a times c to b "
        "times d. <bookmark mark='b2'/>In a partnership, a partner's share "
        "follows capital multiplied by time. <bookmark mark='b3'/>And when the "
        "profit is known, divide it into equal parts using the ratio. <bookmark "
        "mark='b4'/>Money and time together decide the share. <bookmark "
        "mark='b5'/>Thank you for watching, <bookmark mark='b6'/>and see you in "
        "the next lesson."
    ),
}


class CompoundRatioAndBusinessProportionsStory(VoiceoverScene):
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
        out_dir = _HERE / "media" / "videos" / "compound_ratio_and_business_proportions"
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
    # Compound Ratio & Inverse Ratio: Applications in Business Profit Sharing
    # (Class 8 Maths, Chapter 5, Storymode 01).
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
    #     is why the cards space their own lines by 0.22 or more;
    #   * the two partners' cards are the same furniture in every scene, so
    #     Ramayya and Gopalam stay recognisable;
    #   * a drawn cross always lives in the same VGroup as the chip it strikes
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

    def partner_row(self, months_a="12 months", months_b="9 months",
                    money_b="Rs 3,000", y=BAND_A):
        """The two partners' cards, side by side and centred on the board."""
        ca, cb = row_centres((CARD_W / 2, CARD_W / 2), 0.50)
        a = at(partner_card(RAMAYYA[0], RAMAYYA[1], months_a, RAMAYYA[3]), ca, y)
        b = at(partner_card(GOPALAM[0], money_b, months_b, GOPALAM[3]), cb, y)
        return a, b

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

    # -- Scene 0: title ------------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = at(board_text("Two Partners, One Profit", 26, CHALK_PINK,
                                  "BOLD"), BOARD_CX, 2.06)
            sub = at(board_text("Ramayya and Gopalam: money and time together.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, 1.46)

            a_card, b_card = self.partner_row()
            bag = money_bag(BOARD_CX, -0.32, 1.02)

            ask = at(board_text("SHOULD THEY SHARE IT EQUALLY?", 18,
                                CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Profit is shared in the ratio of what each "
                                  "partner contributed.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(title, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(a_card, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(b_card, shift=LEFT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(bag, scale=0.9), run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(ask, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: a ratio is ordered; the inverse swaps the terms -------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("A Ratio Is an Ordered Comparison", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Three to two is not two to three.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            c32 = ratio_card(3, 2, CHALK_GREEN)
            neq = chalk_math(r"\neq", size=30, color=CHALK_RED)
            c23 = ratio_card(2, 3, CHALK_PINK)
            row = self.hrow(c32, neq, c23, y=BAND_A, gap=0.60)

            # the inverse: one card turns over on the spot and reads b : a
            swap = at(ratio_card("a", "b", CHALK_AMBER, width=1.90, height=0.80,
                                 size=28), -0.20, BAND_B)
            flipped = at(ratio_card("b", "a", CHALK_PINK, width=1.90,
                                    height=0.80, size=28), -0.20, BAND_B)
            tag = at(chip("INVERSE", CHALK_PINK, size=14), 1.90, BAND_B)

            banner = at(board_text("THE INVERSE OF 4 : 5 IS 5 : 4", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Inverse means swap the two terms, never add "
                                  "them.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(c32, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(neq, scale=0.9), FadeIn(c23, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(swap, shift=UP * 0.08), run_time=0.40)
            self.play(Rotate(swap, PI, axis=UP), run_time=0.45)
            self.play(Transform(swap, flipped), FadeIn(tag, scale=0.9),
                      run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: the same time -- the time factor cancels --------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("Same Time for Both Partners", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The time factor cancels.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            a_card, b_card = self.partner_row(months_a="12 months",
                                              months_b="12 months")
            flow = self.hrow(
                chip("SAME TIME · 12 MONTHS EACH", CHALK_CYAN, size=13),
                chip("TIME CANCELS", CHALK_YELLOW, size=13),
                chip("CAPITAL 2000 : 3000 = 2 : 3", CHALK_GREEN, size=13),
                y=BAND_B, gap=0.40)
            banner = at(board_text("SO THE PROFIT IS DIVIDED 2 : 3", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("With the same time, the profit is divided "
                                  "2 : 3.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(a_card, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(b_card, shift=LEFT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(flow, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: the same capital -- the capital factor cancels --------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Same Capital, Different Time", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The capital factor cancels.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            ca, cb = row_centres((CARD_W / 2, CARD_W / 2), 0.50)
            a_card = at(partner_card("Ramayya", "Rs 5,000", "12 months",
                                     CHALK_GREEN), ca, BAND_A)
            b_card = at(partner_card("Gopalam", "Rs 5,000", "9 months",
                                     CHALK_PINK), cb, BAND_A)
            flow = self.hrow(
                chip("SAME CAPITAL · Rs 5,000 EACH", CHALK_CYAN, size=13),
                chip("CAPITAL CANCELS", CHALK_YELLOW, size=13),
                chip("TIME 12 : 9 = 4 : 3", CHALK_AMBER, size=13),
                y=BAND_B, gap=0.40)
            banner = at(board_text("SO THE PROFIT FOLLOWS 4 : 3", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("With the same capital, the profit follows "
                                  "the time ratio 4 : 3.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(a_card, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(b_card, shift=LEFT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(flow, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: both the money and the time differ -------------------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("Both Capital and Time Differ", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Neither ratio alone is enough.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            a_card, b_card = self.partner_row()
            cap = at(chip("CAPITAL 2000 : 3000 = 2 : 3", CHALK_GREEN, size=13),
                     -2.10, BAND_B)
            tim = at(chip("TIME 12 : 9 = 4 : 3", CHALK_AMBER, size=13),
                     1.25, BAND_B)
            comb = at(chip("COMBINE BOTH", CHALK_PINK, size=14), 3.85, BAND_B)

            banner = at(board_text("NEITHER RATIO ALONE CAN DECIDE", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("When both differ, the two ratios must be "
                                  "combined.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(a_card, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(b_card, shift=LEFT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(cap, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(tim, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(comb, scale=0.9),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: the compound ratio rule, and the mistake --------------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Compound Ratio Rule", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Multiply the corresponding terms.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            box = at(machine(4.60, 1.50), BOARD_CX, 0.62)
            slot1 = np.array([-2.60, 0.92, 0.0])
            slot2 = np.array([-2.60, 0.22, 0.0])
            in1 = at(ratio_card(2, 3, CHALK_GREEN, width=1.50, height=0.62,
                                size=22), -3.55, 0.92)
            in2 = at(ratio_card(4, 3, CHALK_AMBER, width=1.50, height=0.62,
                                size=22), -3.55, 0.22)
            formula = at(chalk_math(r"a:b \times c:d \rightarrow ac:bd", size=24,
                                    color=CHALK_YELLOW), BOARD_CX, 0.34)
            out = at(ratio_card("ac", "bd", CHALK_YELLOW, width=1.90,
                                height=0.70, size=24), BOARD_CX, -0.78)

            # the wrong idea: its card carries the drawn cross in the top half
            # and the formula under it, so the strike-through never runs into
            # the lettering (the audit measures that clearance)
            wrong = wrong_card("(a + c) : (b + d)", CHALK_RED, width=2.60,
                               height=1.05, size=15)
            wrong.move_to(np.array([3.85, 0.62, 0.0]))
            wrong_cross = wrong.cross
            wrong_cross.set_stroke(opacity=0)

            strip = at(board_text("A compound ratio multiplies corresponding "
                                  "terms; it never adds them.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(box, scale=0.95), FadeIn(in1, shift=RIGHT * 0.10),
                      FadeIn(in2, shift=RIGHT * 0.10), run_time=0.60)
            self.play(in1.animate.move_to(slot1), in2.animate.move_to(slot2),
                      run_time=0.55)
            self.play(FadeOut(in1), FadeOut(in2), run_time=0.35)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(formula, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(out, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(wrong, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(wrong_cross.animate.set_stroke(opacity=1),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: applying the rule, and the money x time cross-check ---------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("Applying the Compound Ratio", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Two to three, compounded with four to three.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            c1 = ratio_card(2, 3, CHALK_GREEN)
            times = chalk_math(r"\times", size=24, color=CHALK_WHITE)
            c2 = ratio_card(4, 3, CHALK_AMBER)
            arrow = arrow_between((0.0, 0.0), (0.60, 0.0), CHALK_YELLOW)
            c3 = ratio_card(8, 9, CHALK_YELLOW)
            row = self.hrow(c1, times, c2, arrow, c3, y=BAND_A, gap=0.42)

            m1 = chip("Rs 2000 × 12 = Rs 24,000", CHALK_GREEN, size=13)
            m2 = chip("Rs 3000 × 9 = Rs 27,000", CHALK_PINK, size=13)
            m3 = chip("24,000 : 27,000 = 8 : 9", CHALK_YELLOW, size=13)
            row2 = self.hrow(m1, m2, m3, y=BAND_B, gap=0.42)

            banner = at(board_text("CAPITAL AND TIME GIVE 8 : 9", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Money times time gives the same ratio, "
                                  "8 : 9.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(c1, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(times, scale=0.9), FadeIn(c2, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(GrowArrow(arrow), FadeIn(c3, scale=0.9), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(m1, shift=UP * 0.06), FadeIn(m2, shift=UP * 0.06),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(m3, shift=UP * 0.06),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: from the ratio to rupees -----------------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("From Ratio to Rupees", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Divide the profit into equal parts.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            total = at(chip("PROFIT (EXAMPLE) = Rs 17,000", CHALK_GREEN,
                            size=14), -1.85, 1.32)
            parts = at(chip("8 + 9 = 17 EQUAL PARTS OF Rs 1,000", CHALK_AMBER,
                            size=13), 2.25, 1.32)

            blocks = profit_blocks(17, CHALK_CYAN, side=0.26, gap=0.08)
            for b in blocks[:8]:
                b.set_fill(CHALK_GREEN, 0.5).set_stroke(CHALK_GREEN)
            for b in blocks[8:]:
                b.set_fill(CHALK_PINK, 0.5).set_stroke(CHALK_PINK)
            at(blocks, BOARD_CX, 0.30)

            left_t = [np.array([-1.85 + (c - 1.5) * 0.34,
                                0.60 + (1 - r) * 0.34, 0.0])
                      for r in range(2) for c in range(4)]
            right_t = [np.array([2.25 + (c - 2.0) * 0.34,
                                 0.60 + (1 - r) * 0.34, 0.0])
                       for r in range(2) for c in range(5)][:9]

            ra = at(chip("RAMAYYA: 8 × Rs 1,000 = Rs 8,000", CHALK_GREEN,
                         size=13), -1.85, -0.62)
            go = at(chip("GOPALAM: 9 × Rs 1,000 = Rs 9,000", CHALK_PINK,
                         size=13), 2.25, -0.62)
            each = at(chip("EACH PART = Rs 1,000", CHALK_CYAN, size=13),
                      BOARD_CX, -1.32)

            strip = at(board_text("Rs 8,000 + Rs 9,000 = Rs 17,000: the whole "
                                  "profit is shared.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(total, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(parts, shift=UP * 0.06),
                      LaggedStart(*[FadeIn(b, scale=0.8) for b in blocks],
                                  lag_ratio=0.05), run_time=0.80)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(each, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(*[b.animate.move_to(t)
                        for b, t in zip(blocks[:8], left_t)],
                      FadeIn(ra, shift=UP * 0.06), run_time=0.70)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(*[b.animate.move_to(t)
                        for b, t in zip(blocks[8:], right_t)],
                      FadeIn(go, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.75)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the decision map -------------------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("Which Ratio Decides the Share?", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Time, capital, or both.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            c1 = note_card("SAME TIME", ["use the capital ratio"], CHALK_GREEN,
                           width=2.80, height=1.05)
            c2 = note_card("SAME CAPITAL", ["use the time ratio"], CHALK_CYAN,
                           width=2.80, height=1.05)
            c3 = note_card("BOTH DIFFERENT", ["use the compound ratio"],
                           CHALK_AMBER, width=2.80, height=1.05)
            row = self.hrow(c1, c2, c3, y=0.95, gap=0.45)

            rule = at(chip("PROFIT SHARE FOLLOWS CAPITAL × TIME", CHALK_YELLOW,
                           size=15), BOARD_CX, BAND_B)
            banner = at(board_text("BOTH DIFFERENT MEANS COMPOUND RATIO", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("A partner's share follows capital multiplied "
                                  "by time.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(c1, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(c2, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(c3, shift=UP * 0.06),
                      FadeIn(banner, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(rule, scale=0.9), FadeIn(strip, shift=UP * 0.06),
                      run_time=0.50)
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

            pic_a = chalk_math(r"7 : 5 \;\rightarrow\; ?", size=20,
                               color=CHALK_GREEN)
            pic_b = chalk_math(r"3 : 4 \times 2 : 3", size=20, color=CHALK_CYAN)
            pic_c = chalk_math(r"3 : 4 \times 5 : 4", size=20, color=CHALK_AMBER)
            pic_d = VGroup(board_text("P: Rs 4,000, 6 months", 12, CHALK_PINK,
                                      "BOLD"),
                           board_text("Q: Rs 3,000, 8 months", 12, CHALK_PINK,
                                      "BOLD")).arrange(DOWN, buff=0.24)

            qa = at(self.q_card("inverse of 7 : 5", pic_a, CHALK_GREEN),
                    -2.80, 0.92)
            qb = at(self.q_card("compound 3 : 4 and 2 : 3", pic_b, CHALK_CYAN),
                    3.70, 0.92)
            qc = at(self.q_card("3 : 4 with the inverse of 4 : 5", pic_c,
                                CHALK_AMBER), -2.80, -1.02)
            qd = at(self.q_card("P and Q: what ratio?", pic_d, CHALK_PINK),
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
            a1 = at(self.answer_row("A", "inverse of 7 : 5 is 5 : 7",
                                    "the inverse swaps the terms", CHALK_GREEN),
                    BOARD_CX, 1.62)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "3 : 4 and 2 : 3 give 6 : 12",
                                    "which simplifies to 1 : 2", CHALK_CYAN),
                    BOARD_CX, 0.82)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "3 : 4 with 5 : 4 give 15 : 16",
                                    "3 × 5 to 4 × 4", CHALK_AMBER),
                    BOARD_CX, 0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "Rs 24,000 : Rs 24,000",
                                    "so the ratio is 1 : 1", CHALK_PINK),
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

            heading = at(board_text("Inverse · Compound · Partnership", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)

            r1 = at(self.answer_row("1", "INVERSE RATIO",
                                    "swap the terms: a : b becomes b : a",
                                    CHALK_GREEN), BOARD_CX, 1.48)
            r2 = at(self.answer_row("2", "COMPOUND RATIO",
                                    "multiply corresponding terms: ac : bd",
                                    CHALK_CYAN), BOARD_CX, 0.72)
            r3 = at(self.answer_row("3", "PARTNERSHIP",
                                    "the share follows capital × time",
                                    CHALK_YELLOW), BOARD_CX, -0.04)
            r4 = at(self.answer_row("4", "SHARE THE PROFIT",
                                    "divide it into equal parts using the ratio",
                                    CHALK_AMBER), BOARD_CX, -0.80)
            strip = at(board_text("Money and time together decide the share.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)
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
            # the strip is written on its own bookmark as the voice says "Money
            # and time together decide the share.", and only the bookmark in
            # front of "Thank you for watching," clears the board and brings in
            # the card.
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

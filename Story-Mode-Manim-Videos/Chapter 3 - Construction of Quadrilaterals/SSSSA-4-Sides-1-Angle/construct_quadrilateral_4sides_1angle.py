"""
How to Construct a Quadrilateral Given 4 Sides and 1 Angle -- the S.S.S.S.A Method
Story-mode chalkboard lesson (Telangana Class 8 Maths, Chapter 3:
Construction of Quadrilaterals, Storymode 02).

LLM KEY / FUNCTION NAME: construct_quadrilateral_4sides_1angle

Production pipeline (mirrors the rest of the Story-Mode series):
  - Shared assets/background2.png chalkboard backdrop + student/teacher
    cutouts + corner badges (dhimantAI top-left, Mathematics top-right).
  - VoiceoverScene + speech service; narration written as continuous prose.
  - Real per-word sync via <bookmark> tags + tracker timing, and a
    ground-truth SRT export from the service word boundaries.
  - Sound effects from sound_effects.py; chalk-styled Text (Segoe Print) and
    MathTex; shared story_common.play_challenge_countdown() for the THINK clock.

The defining visual: the five given measurements split into 3 + 2 -- two sides
and the included angle build triangle PQR, and the remaining two side lengths
become the radii of two compass arcs whose intersection is the fourth vertex.

Title + 10 scenes:
  0. Title card.
  1. The five given measurements (Example 1 data).
  2. Rough sketch, every measurement marked.
  3. Which three measurements to use first (S.A.S).
  4. Draw PQ and set out the 120 degree angle at Q.
  5. Compass arc of 5.2 cm about Q fixes R.
  6. Two arcs (4 cm about P, 5.5 cm about R) locate S.
  7. Join PS and SR, then verify all five measurements.
  8. The reusable S.S.S.S.A method.
  9. Your turn: Exercise 3.1(a) -- plan the construction.
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


def example_frame(origin=None, scale=SCALE):
    """Textbook Example 1, built exactly as the construction does it.

    The given angle is the *interior* angle at Q.  P Q = 4.5 cm runs to the
    right of P, so the ray Q P points back to the left (180 degrees) and the
    angle of 120 degrees at Q is the wedge between Q P and Q R that opens
    upward inside the quadrilateral: Q R therefore leaves Q at
    180 - 120 = 60 degrees above the base.  S is then the intersection of the
    4 cm arc about P and the 5.5 cm arc about R."""
    if origin is None:
        origin = np.array([BOARD_CX - 2.1, -0.9, 0.0])
    P = np.array(origin, dtype=float)
    Q = P + np.array([4.5 * scale, 0.0, 0.0])
    ang = (180 - 120) * DEGREES
    R = Q + 5.2 * scale * np.array([np.cos(ang), np.sin(ang), 0.0])
    S = circle_intersection(P, 4.0 * scale, R, 5.5 * scale, upper=True)
    return P, Q, R, S


def exercise_frame(origin=None, scale=SCALE):
    """Exercise 3.1(a): A B = 5.5, B C = 3.5, C D = 4, A D = 5, angle A = 45."""
    if origin is None:
        origin = np.array([BOARD_CX - 0.4, -0.5, 0.0])
    A = np.array(origin, dtype=float)
    B = A + np.array([5.5 * scale, 0.0, 0.0])
    a = 45 * DEGREES
    D = A + 5.0 * scale * np.array([np.cos(a), np.sin(a), 0.0])
    C = circle_intersection(B, 3.5 * scale, D, 4.0 * scale, upper=True)
    return A, B, C, D


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


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "How do we construct a quadrilateral when we are given four sides and "
        "one angle?<bookmark mark='b0'/> We will build it in four clear steps, "
        "and we will see exactly why each one works.<bookmark mark='b1'/>"
    ),
    "scene1": (
        "Here is our problem.<bookmark mark='b0'/> We are given five "
        "measurements. P Q is four point five centimetres. Q R is five point "
        "two centimetres. R S is five point five centimetres. P S is four "
        "centimetres.<bookmark mark='b0b'/> And angle R Q P is one hundred and "
        "twenty degrees.<bookmark mark='b1'/> Four sides and one angle: that is "
        "the combination.<bookmark mark='b2'/> So where should we start?"
        "<bookmark mark='b3'/>"
    ),
    "scene2": (
        "We start with a rough sketch.<bookmark mark='b0'/> Draw the "
        "quadrilateral P Q R S, going round in order, and mark every "
        "measurement on it.<bookmark mark='b1'/> This sketch is not to scale. "
        "It is only here to show us which measurements belong together."
        "<bookmark mark='b2'/> Look closely at the angle: it sits at Q, "
        "between Q P and Q R.<bookmark mark='b3'/>"
    ),
    "scene3": (
        "Now we look for a triangle that we can build straight away."
        "<bookmark mark='b0'/> We know P Q, we know Q R, and we know the angle "
        "between them.<bookmark mark='b1'/> Two sides and the included angle: "
        "that is side, angle, side.<bookmark mark='b2'/> So triangle P Q R is "
        "the one to construct first.<bookmark mark='b3'/>"
    ),
    "scene4": (
        "Let us construct it accurately.<bookmark mark='b0'/> Draw P Q, four "
        "point five centimetres long, and label the ends P and Q."
        "<bookmark mark='b1'/> At Q, set out the angle of one hundred and "
        "twenty degrees from Q P.<bookmark mark='b2'/> R must lie somewhere "
        "along that ray. The angle fixes its direction, but not yet its "
        "distance.<bookmark mark='b3'/>"
    ),
    "scene5": (
        "So we set the compass to five point two centimetres.<bookmark "
        "mark='b0'/> With the compass point at Q, we draw an arc that cuts the "
        "ray.<bookmark mark='b1'/> Where the arc cuts the ray, that is R."
        "<bookmark mark='b2'/> Triangle P Q R is now completely fixed."
        "<bookmark mark='b3'/>"
    ),
    "scene6": (
        "Only one vertex is left: S.<bookmark mark='b0'/> We know P S is four "
        "centimetres, so S must lie on the arc of radius four about P."
        "<bookmark mark='b1'/> We also know R S is five point five "
        "centimetres, so S must lie on the arc of radius five point five about "
        "R.<bookmark mark='b2'/> Those two arcs meet at exactly one point on "
        "this side, and that point satisfies both distances.<bookmark "
        "mark='b3'/> There is S.<bookmark mark='b4'/>"
    ),
    "scene7": (
        "Now we finish the figure.<bookmark mark='b0'/> Join P to S, and join S "
        "to R.<bookmark mark='b1'/> Those two sides complete the quadrilateral "
        "P Q R S.<bookmark mark='b2'/> Let us check every measurement: P Q is "
        "four point five, Q R is five point two, R S is five point five, P S is "
        "four, and angle R Q P is one hundred and twenty degrees. All five are "
        "used.<bookmark mark='b3'/>"
    ),
    "scene8": (
        "This is the method, and it works for every problem of this kind."
        "<bookmark mark='b0'/> First sketch the figure and mark what is given. "
        "Then build the first triangle from two sides and the included angle. "
        "Then use the two remaining lengths as radii, and intersect those arcs. "
        "Finally join the last sides, and verify.<bookmark mark='b1'/> Sketch, "
        "triangle, arcs, join.<bookmark mark='b2'/>"
    ),
    "scene9_setup": (
        "Your turn.<bookmark mark='b0'/> In quadrilateral A B C D, A B is five "
        "point five centimetres, B C is three point five centimetres, C D is "
        "four centimetres, A D is five centimetres, and angle A is forty five "
        "degrees.<bookmark mark='b1'/> Which triangle should you construct "
        "first?<bookmark mark='b2'/> Pause the video and decide.<bookmark "
        "mark='b3'/>"
    ),
    "scene9_reveal": (
        "Let us check.<bookmark mark='b0'/> The angle is at A, between A B and "
        "A D, and we know both of those sides.<bookmark mark='b1'/> So triangle "
        "B A D comes first, from A B, A D and the angle of forty five degrees."
        "<bookmark mark='b2'/> Then C is found by two arcs: radius three point "
        "five about B, and radius four about D. Where they cross is C, and the "
        "quadrilateral A B C D is complete.<bookmark mark='b3'/>"
    ),
    "scene10": (
        "Let us put the method together.<bookmark mark='b0'/> Three "
        "measurements build the triangle: two sides and the included angle."
        "<bookmark mark='b1'/> Two more measurements locate the fourth vertex, "
        "as the intersection of two arcs.<bookmark mark='b2'/> Sketch, "
        "triangle, arcs, join, verify. That is the four sides and one angle "
        "method.<bookmark mark='b3'/> Thank you for watching!"
        "<bookmark mark='b4'/> See you in the next lesson!<bookmark mark='b5'/>"
    ),
}

class ConstructQuadrilateral4Sides1AngleStory(VoiceoverScene):
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
        wbs = [
            wb for wb in tracker.data.get("word_boundaries", [])
            if wb.get("text", "").strip()
        ]
        if not wbs:
            return
        starts = [tracker.start_t + wb["audio_offset"] / AUDIO_OFFSET_RESOLUTION
                  for wb in wbs]
        for i in range(0, len(wbs), words_per_line):
            chunk = wbs[i:i + words_per_line]
            chunk_starts = starts[i:i + words_per_line]
            end = starts[i + words_per_line] if i + words_per_line < len(starts) \
                else tracker.end_t
            text = " ".join(wb["text"] for wb in chunk)
            self._srt_entries.append((chunk_starts[0], end, text))

    def _write_real_srt(self) -> None:
        out_dir = _HERE / "media" / "videos" / "construct_quadrilateral_4sides_1angle"
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
        self.beat1_data()
        self.beat2_sketch()
        self.beat3_choose()
        self.beat4_side_angle()
        self.beat5_triangle()
        self.beat6_locate_s()
        self.beat7_complete()
        self.beat8_method()
        self.beat9_challenge()
        self.beat10_recap()

        self._write_real_srt()

    # ================================================================ beats ==

    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Construct a Quadrilateral", 33, CHALK_WHITE,
                               "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 1.85, 0]))
            sub = board_text("Four Sides and One Angle", 22,
                             CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 0.95, 0]))
            self.appear(title, tracker, "b0", 0.45)
            self.appear(sub, tracker, "b0", 0.45)
            self.play(Indicate(sub, color=CHALK_YELLOW, scale_factor=1.04),
                      run_time=max(leftover(tracker, "b0"), 0.4))
            self.add_sound(self.sfx["ding"], gain=-13)

            # opening figure matches the rest of the chapter's title cards: a
            # small quadrilateral centred under the title, with THIS video's
            # defining measurement — the given angle at Q — drawn and flashed,
            # and the same arrow-style step line
            P, Q, R, S = example_frame(origin=np.array([BOARD_CX - 0.75, -0.78, 0]),
                                       scale=0.30)
            outline = Polygon(P, Q, R, S, color=CHALK_WHITE, stroke_width=2.2,
                              fill_color=CHALK_WHITE, fill_opacity=0.05)
            outline.set_stroke(opacity=0.45)
            given = angle_mark(Q, P, R, radius=0.30, color=CHALK_YELLOW,
                               label="120°")
            names = quad_names((P, Q, R, S), "PQRS", 15)
            tag = board_text("Angle → Triangle → Arcs → Join", 18,
                             CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))
            self.play(FadeIn(outline), FadeIn(names), run_time=min(
                leftover(tracker, "b1"), 1.0))
            self.play(Create(given.arc), FadeIn(given.label), run_time=0.8)
            self.play(Flash(given.arc, color=CHALK_YELLOW, flash_radius=0.6),
                      run_time=0.6)
            self.appear(tag, tracker, "b1", 0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: the five given measurements --------------------------------
    def beat1_data(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("Four Sides and One Angle", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            # the whole block is centred on the board's centre line: the five
            # measurements, the strip that names the combination, the question
            cards = VGroup(
                measure_card(r"PQ=4.5", CHALK_CYAN),
                measure_card(r"QR=5.2", CHALK_CYAN),
                measure_card(r"RS=5.5", CHALK_CYAN),
                measure_card(r"PS=4", CHALK_CYAN),
                measure_card(r"\angle RQP=120^\circ", CHALK_YELLOW),
            ).arrange(DOWN, buff=0.24).move_to(
                np.array([BOARD_CX, 0.55, 0]))

            # heading and the four side cards together, then hold to the mark:
            # an entrance bounded by an already-reached mark would play in a
            # single frame, which pops instead of animating
            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.12)
                                    for c in cards[:4]], lag_ratio=0.22),
                      run_time=1.0)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            # the 120 degree card is introduced by its own sentence, crisply
            self.wait(leftover(tracker, "b0b"))
            self.play(FadeIn(cards[4], shift=RIGHT * 0.12), run_time=0.45)
            self.play(Indicate(cards[4], color=CHALK_YELLOW, scale_factor=1.08),
                      run_time=0.9)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b1"))

            strip = board_text("4 Sides + 1 Angle", 21, CHALK_GREEN, "BOLD"
                               ).move_to(np.array([BOARD_CX, -1.79, 0]))
            box = SurroundingRectangle(strip, color=CHALK_GREEN, buff=0.16,
                                       corner_radius=0.1, stroke_width=2.6)
            self.play(FadeIn(strip, shift=UP * 0.1), Create(box), run_time=0.6)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["click"], gain=-15)

            ask = board_text("Where should we start?", 19, CHALK_WHITE, "BOLD"
                             ).move_to(np.array([BOARD_CX, -2.54, 0]))
            self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: the rough sketch -------------------------------------------
    def beat2_sketch(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 1 — Rough Sketch", 22, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            # the rough sketch is deliberately *not* to scale: a free shape --
            # but the corner at Q still opens to the given 120 degrees, so the
            # marked angle is the angle that is actually drawn
            rough_pts = (np.array([-1.5, -0.7, 0]), np.array([1.9, -0.9, 0]),
                         np.array([3.14, 0.98, 0]), np.array([-1.9, 1.5, 0]))
            rough = Polygon(*rough_pts, color=CHALK_WHITE, stroke_width=2.6,
                            fill_color=CHALK_WHITE, fill_opacity=0.05)
            rough.corners = rough_pts
            centre = rough.get_center()
            names = quad_names(rough.corners, "PQRS", 18)
            lab_pq = side_label(rough.corners[0], rough.corners[1], centre,
                                "4.5", CHALK_CYAN, 16, 0.18)
            lab_qr = side_label(rough.corners[1], rough.corners[2], centre,
                                "5.2", CHALK_CYAN, 16, 0.18)
            lab_rs = side_label(rough.corners[2], rough.corners[3], centre,
                                "5.5", CHALK_CYAN, 16, 0.18)
            lab_ps = side_label(rough.corners[3], rough.corners[0], centre,
                                "4", CHALK_CYAN, 16, 0.18)
            q_arc = angle_mark(rough.corners[1], rough.corners[0],
                               rough.corners[2], radius=0.42,
                               color=CHALK_YELLOW, label="120°")
            note = board_text("Not to scale", 17, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.0, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(Create(rough), FadeIn(names), run_time=1.6)
            self.play(FadeIn(note), run_time=0.4)
            self.wait(leftover(tracker, "b0"))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(FadeIn(lab_pq), run_time=min(leftover(tracker, "b1"), 0.5))
            self.play(FadeIn(lab_qr), run_time=min(leftover(tracker, "b1"), 0.5))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            self.play(FadeIn(lab_rs), FadeIn(lab_ps), run_time=min(
                leftover(tracker, "b2"), 0.8))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b2"))

            self.play(Create(q_arc.arc), FadeIn(q_arc.label),
                      Indicate(names[1], color=CHALK_YELLOW, scale_factor=1.5),
                      run_time=min(leftover(tracker, "b3"), 1.6))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["ding"], gain=-13)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: which three measurements come first ------------------------
    def beat3_choose(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()

            heading = board_text("Use 3 of the 5 Measurements First", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            P, Q, R, S = example_frame()
            full = Polygon(P, Q, R, S, color=CHALK_WHITE, stroke_width=2.2,
                           fill_opacity=0.0)
            full.set_stroke(opacity=0.30)
            names = quad_names((P, Q, R, S), "PQRS", 18)
            tri = Polygon(P, Q, R, color=CHALK_CYAN, stroke_width=3.2,
                          fill_color=CHALK_CYAN, fill_opacity=0.16)
            tri_pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=4.0)
            tri_qr = Line(Q, R, color=CHALK_YELLOW, stroke_width=4.0)
            lab_pq = board_text("PQ = 4.5", 16, CHALK_YELLOW, "BOLD").move_to(
                (P + Q) / 2 + DOWN * 0.32)
            centroid = np.array([P, Q, R, S], dtype=float).mean(axis=0)
            lab_qr = side_label(Q, R, centroid, "QR = 5.2", CHALK_YELLOW, 16,
                                0.20)
            q_arc = angle_mark(Q, P, R, radius=0.5, color=CHALK_PINK,
                               label="120°")
            # the two cards that name the chosen measurements sit in the free
            # right-hand column, clear of the figure's vertex letters, of the
            # QR label and of the board's frame
            sas = measure_card(r"\text{Side}+\text{Angle}+\text{Side}",
                               CHALK_GREEN, 16).move_to(
                np.array([BOARD_CX + 3.1, -0.55, 0]))
            sas2 = measure_card(r"\text{S.A.S}", CHALK_GREEN, 16).move_to(
                np.array([BOARD_CX + 3.1, -1.15, 0]))
            note = board_text("Three measurements fix this triangle.", 17,
                              CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.3, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(full), FadeIn(names), run_time=0.6)
            self.play(Create(tri_pq), FadeIn(lab_pq), run_time=1.4)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(Create(tri_qr), FadeIn(lab_qr), run_time=min(
                leftover(tracker, "b1"), 1.2))
            self.play(FadeIn(tri), run_time=min(leftover(tracker, "b1"), 1.0))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            self.play(Create(q_arc.arc), FadeIn(q_arc.label), run_time=min(
                leftover(tracker, "b2"), 1.2))
            self.play(FadeIn(sas, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(sas2, shift=UP * 0.1), run_time=0.45)
            self.play(FadeIn(note), Flash(tri, color=CHALK_CYAN,
                                          flash_radius=0.8), run_time=0.7)
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: draw PQ and set out the angle ------------------------------
    def beat4_side_angle(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 2 — PQ and the 120° Angle", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            P, Q, R, S = example_frame()
            base = Line(P, Q, color=CHALK_WHITE, stroke_width=4.5)
            names = VGroup(vertex_label("P", P, "DL"), vertex_label("Q", Q, "DR"))
            lab_pq = board_text("PQ = 4.5 cm", 17, CHALK_CYAN, "BOLD").move_to(
                (P + Q) / 2 + DOWN * 0.30)
            ray = DashedLine(Q, R + 0.25 * (R - Q),
                             color=CHALK_YELLOW, stroke_width=2.0,
                             dash_length=0.14)
            prot = protractor(Q, radius=1.05)
            q_arc = angle_mark(Q, P, R, radius=0.52, color=CHALK_PINK,
                               label="120°")
            note = board_text("R must lie somewhere on this ray.", 19,
                              CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -1.85, 0]))

            self.appear(heading, tracker, "b0", 0.45)
            self.play(Create(base), FadeIn(names), run_time=0.7)
            self.play(FadeIn(lab_pq), run_time=0.5)
            self.wait(leftover(tracker, "b0"))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(FadeIn(prot, scale=0.9), run_time=min(
                leftover(tracker, "b1"), 1.0))
            self.play(Create(ray), FadeOut(prot), run_time=min(
                leftover(tracker, "b1"), 1.3))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.wait(leftover(tracker, "b1"))

            self.play(Create(q_arc.arc), FadeIn(q_arc.label),
                      Indicate(q_arc.arc, color=CHALK_PINK, scale_factor=1.06),
                      run_time=min(leftover(tracker, "b2"), 1.4))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b2"))

            self.play(Indicate(ray, color=CHALK_YELLOW, scale_factor=1.0),
                      run_time=0.8)
            self.appear(note, tracker, "b3", 0.5)
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: the compass arc that fixes R -------------------------------
    def beat5_triangle(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            self.reset_board()

            heading = board_text("Triangle PQR is Fixed", 22, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            P, Q, R, S = example_frame()
            base = Line(P, Q, color=CHALK_WHITE, stroke_width=4.5)
            ray = DashedLine(Q, R, color=CHALK_YELLOW,
                             stroke_width=1.8, dash_length=0.14)
            names = VGroup(vertex_label("P", P, "DL"), vertex_label("Q", Q, "DR"))
            lab_pq = board_text("PQ = 4.5 cm", 16, CHALK_CYAN, "BOLD").move_to(
                (P + Q) / 2 + DOWN * 0.30)
            arc = None            # the compass draws this arc (see below)
            rad = radius_line(Q, Q + 5.2 * SCALE * np.array(
                [np.cos(28 * DEGREES), np.sin(28 * DEGREES), 0.0]),
                CHALK_GREEN, "5.2 cm")
            r_dot = Dot(radius=0.085, color=CHALK_YELLOW).move_to(R)
            r_name = vertex_label("R", R, "UR", CHALK_WHITE)
            tri = Polygon(P, Q, R, color=CHALK_CYAN, stroke_width=2.4,
                          fill_color=CHALK_CYAN, fill_opacity=0.12)
            # "QR = 5.2 cm" sits out to the right of the triangle, below the
            # corner at R: inside the triangle the label is wider than the
            # triangle itself and its end ran into the P-R side, and just
            # outside the Q-R side the compass arc (which passes through R)
            # grazed it
            lab_qr = board_text("QR = 5.2 cm", 16, CHALK_GREEN, "BOLD").move_to(
                (Q + R) / 2 + np.array([0.94, -0.28, 0]))
            note = board_text("Three measurements used. Two still left: "
                              "PS = 4, RS = 5.5.", 18, CHALK_WHITE, "BOLD"
                              ).move_to(np.array([BOARD_CX, -2.1, 0]))

            self.appear(heading, tracker, "b0", 0.45)
            self.play(Create(base), FadeIn(names), FadeIn(ray), FadeIn(lab_pq),
                      run_time=0.9)
            self.play(FadeIn(rad), run_time=0.5)
            self.wait(leftover(tracker, "b0"))
            self.add_sound(self.sfx["pop"], gain=-13)

            # the compass is set to 5.2 cm and the pencil draws the arc
            self.draw_with_compass(Q, R, 5.2 * SCALE, 26, CHALK_GREEN,
                                   tracker, "b1", hinge_dir=(1.0, -0.6, 0.0))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(FadeIn(r_dot, scale=0.5), FadeIn(r_name),
                      Indicate(r_dot, color=CHALK_YELLOW, scale_factor=1.8),
                      run_time=min(leftover(tracker, "b2"), 1.0))
            self.play(FadeIn(tri), FadeIn(lab_qr), FadeOut(rad), FadeOut(ray),
                      run_time=min(leftover(tracker, "b2"), 1.0))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b2"))

            self.play(Flash(tri, color=CHALK_CYAN, flash_radius=0.7),
                      run_time=0.8)
            self.appear(note, tracker, "b3", 0.5)
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: two arcs locate S ------------------------------------------
    def beat6_locate_s(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 3 — Locate S", 22, CHALK_AMBER, "BOLD"
                                 ).move_to(np.array([BOARD_CX, 2.72, 0]))
            P, Q, R, S = example_frame()
            tri = Polygon(P, Q, R, color=CHALK_CYAN, stroke_width=2.4,
                          fill_color=CHALK_CYAN, fill_opacity=0.12)
            names = quad_names((P, Q, R, S), "PQRS", 17)
            tri_names = VGroup(*[names[i] for i in (0, 1, 2)])
            arc_p = locating_arc(P, S, 4.0 * SCALE, 18, CHALK_PINK)
            arc_r = locating_arc(R, S, 5.5 * SCALE, 16, CHALK_GREEN)
            rad_p = radius_line(P, S, CHALK_PINK, "PS = 4 cm")
            rad_r = radius_line(R, S, CHALK_GREEN, "RS = 5.5 cm")
            s_dot = Dot(radius=0.09, color=CHALK_YELLOW).move_to(S)
            # S sits a touch further out so the pink arc, which is drawn
            # through S, cannot run into the letter
            s_name = vertex_label("S", S, "UL", CHALK_WHITE).shift(
                np.array([-0.12, 0.12, 0]))
            guide1 = DashedLine(P, S, color=CHALK_WHITE, stroke_width=1.8,
                                dash_length=0.12)
            guide2 = DashedLine(R, S, color=CHALK_WHITE, stroke_width=1.8,
                                dash_length=0.12)
            note = board_text("S satisfies both distances.", 19, CHALK_GREEN,
                              "BOLD").move_to(np.array([BOARD_CX, -2.2, 0]))

            self.appear(heading, tracker, "b0", 0.45)
            self.play(FadeIn(tri), FadeIn(tri_names), run_time=0.6)
            self.play(FadeIn(rad_p), run_time=0.5)
            self.wait(leftover(tracker, "b0"))
            self.add_sound(self.sfx["pop"], gain=-13)

            # first arc: needle on P, pencil tracing the 4 cm arc
            self.draw_with_compass(P, S, 4.0 * SCALE, 18, CHALK_PINK,
                                   tracker, "b1", hinge_dir=(1.0, -0.5, 0.0))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            # second arc: needle on R.  The compass is not re-set here -- the
            # arc about R sweeps across the figure, so the tool would have to
            # sit on top of it; this arc is drawn while the first tool is put
            # away.
            self.play(FadeIn(rad_r), run_time=0.4)
            # both arcs of the pair come from the instrument
            self.draw_with_compass(R, S, 5.5 * SCALE, 16, CHALK_GREEN,
                                   tracker, "b2", hinge_dir=(0.3, 1.0, 0.0),
                                   leg_ratio=0.52)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(FadeIn(s_dot, scale=0.5), FadeIn(s_name),
                      Indicate(s_dot, color=CHALK_YELLOW, scale_factor=2.0),
                      run_time=min(leftover(tracker, "b3"), 1.0))
            self.play(Create(guide1), Create(guide2), FadeOut(rad_p),
                      FadeOut(rad_r), run_time=min(leftover(tracker, "b3"), 1.2))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b3"))

            self.play(Flash(s_dot, color=CHALK_GREEN, flash_radius=0.6),
                      run_time=0.8)
            self.appear(note, tracker, "b4", 0.5)
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: join the last two sides and verify -------------------------
    def beat7_complete(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("Required Quadrilateral PQRS", 22, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            P, Q, R, S = example_frame()
            qp = Line(P, Q, color=CHALK_WHITE, stroke_width=4.0)
            qr = Line(Q, R, color=CHALK_WHITE, stroke_width=4.0)
            ps = Line(P, S, color=CHALK_GREEN, stroke_width=4.0)
            sr = Line(S, R, color=CHALK_GREEN, stroke_width=4.0)
            quad = Polygon(P, Q, R, S, color=CHALK_CYAN, stroke_width=2.2,
                           fill_color=CHALK_CYAN, fill_opacity=0.10)
            names = quad_names((P, Q, R, S), "PQRS", 17)
            checks = VGroup(
                check_row(r"PQ=4.5", CHALK_GREEN, 15),
                check_row(r"QR=5.2", CHALK_GREEN, 15),
                check_row(r"RS=5.5", CHALK_GREEN, 15),
                check_row(r"PS=4", CHALK_GREEN, 15),
                check_row(r"\angle RQP=120^\circ", CHALK_YELLOW, 15),
            ).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX + 3.0, 0.0, 0]))
            title = board_text("All five measurements used.", 19, CHALK_GREEN,
                               "BOLD").move_to(np.array([BOARD_CX, -2.35, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(Create(qp), Create(qr), FadeIn(names), run_time=0.9)
            self.play(Create(ps), run_time=1.0)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(Create(sr), run_time=min(leftover(tracker, "b1"), 1.0))
            self.play(FadeIn(quad), run_time=min(leftover(tracker, "b1"), 0.8))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            self.play(FadeIn(title, shift=UP * 0.1), run_time=0.5)
            self.play(Flash(quad, color=CHALK_CYAN, flash_radius=0.8),
                      run_time=min(leftover(tracker, "b2"), 0.9))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b2"))

            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1)
                                    for c in checks], lag_ratio=0.22),
                      run_time=min(leftover(tracker, "b3"), 1.6))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the reusable method ----------------------------------------
    def beat8_method(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("The Four-Step Method", 23, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            steps = VGroup(
                combo_card("1. SKETCH", "mark all 5 measurements", CHALK_CYAN),
                combo_card("2. TRIANGLE", "2 sides + included angle",
                           CHALK_GREEN),
                combo_card("3. TWO ARCS", "remaining lengths as radii",
                           CHALK_PINK),
                combo_card("4. JOIN", "complete and verify", CHALK_YELLOW),
            ).arrange(DOWN, buff=0.20, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX - 2.35, 0.35, 0]))
            P, Q, R, S = example_frame(origin=np.array([BOARD_CX + 2.2, 0.55, 0]),
                                       scale=0.30)
            mini = VGroup(
                Polygon(P, Q, R, S, color=CHALK_WHITE, stroke_width=2.0,
                        fill_opacity=0.0),
                Line(P, Q, color=CHALK_YELLOW, stroke_width=3.0),
                Line(Q, R, color=CHALK_YELLOW, stroke_width=3.0),
                locating_arc(P, S, 4.0 * 0.30, 30, CHALK_PINK),
                locating_arc(R, S, 5.5 * 0.30, 35, CHALK_GREEN),
                Dot(radius=0.07, color=CHALK_YELLOW).move_to(S),
            )
            names = quad_names((P, Q, R, S), "PQRS", 14)
            names[3].shift(np.array([-0.10, 0.10, 0]))   # clear of the pink arc
            note = board_text("Sketch → Triangle → Arcs → Join → Verify", 18,
                              CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.35, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(steps), run_time=1.2)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(mini[0]), FadeIn(names), FadeIn(mini[1]),
                      FadeIn(mini[2]), run_time=min(leftover(tracker, "b1"), 1.0))
            self.play(Create(mini[3]), Create(mini[4]), FadeIn(mini[5]),
                      run_time=min(leftover(tracker, "b1"), 1.6))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b1"))

            self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
            self.play(Circumscribe(steps[0], color=CHALK_CYAN, stroke_width=2.4,
                                   time_width=0.6),
                      run_time=min(leftover(tracker, "b2"), 1.2))
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 9: student challenge ------------------------------------------
    def beat9_challenge(self) -> None:
        with self.voiceover(text=NARRATION["scene9_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", 30, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, 2.62, 0]))
            A, B, C, D = exercise_frame(origin=np.array([BOARD_CX - 2.6, -0.35, 0]),
                                       scale=0.40)
            rough = Polygon(A, B, C, D, color=CHALK_WHITE, stroke_width=2.4,
                            fill_color=CHALK_WHITE, fill_opacity=0.06)
            names = quad_names((A, B, C, D), "ABCD", 16)
            a_arc = angle_mark(A, B, D, radius=0.36, color=CHALK_YELLOW,
                               label="45°")
            cards = VGroup(
                measure_card(r"AB=5.5", CHALK_CYAN, 15),
                measure_card(r"BC=3.5", CHALK_CYAN, 15),
                measure_card(r"CD=4", CHALK_CYAN, 15),
                measure_card(r"AD=5", CHALK_CYAN, 15),
                measure_card(r"\angle A=45^\circ", CHALK_YELLOW, 15),
            ).arrange(DOWN, buff=0.20).move_to(
                np.array([BOARD_CX + 2.4, 0.55, 0]))
            # the question is centred on the board's centre line, under the
            # figure, where the eye already is
            ask = board_text("Which triangle comes first?", 18, CHALK_WHITE,
                             "BOLD").move_to(np.array([BOARD_CX, -2.45, 0]))
            pause = board_text("Pause and decide.", 18, CHALK_YELLOW, "BOLD"
                               ).move_to(np.array([BOARD_CX + 2.4, -1.9, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(rough), FadeIn(names), run_time=0.7)
            self.play(Create(a_arc.arc), FadeIn(a_arc.label), run_time=1.0)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.10)
                                    for c in cards], lag_ratio=0.18),
                      run_time=min(leftover(tracker, "b1"), 1.6))
            self.wait(leftover(tracker, "b1"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.appear(ask, tracker, "b2", 0.5, shift=RIGHT * 0.12)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(pause, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b3")))

            self.challenge = {"rough": rough, "names": names, "cards": cards,
                              "ask": ask, "pause": pause, "a_arc": a_arc,
                              "points": (A, B, C, D)}
            self._capture_srt(tracker)

        play_challenge_countdown(self, seconds=4, sfx=self.sfx,
                                 position=np.array([BOARD_CX - 3.7, 0.4, 0]))

        with self.voiceover(text=NARRATION["scene9_reveal"]) as tracker:
            ch = self.challenge
            A, B, C, D = ch["points"]
            rough, names = ch["rough"], ch["names"]

            self.play(FadeOut(ch["pause"]), run_time=min(
                leftover(tracker, "b0"), 0.5))
            tri_bad = Polygon(B, A, D, color=CHALK_GREEN, stroke_width=3.0,
                              fill_color=CHALK_GREEN, fill_opacity=0.14)
            lab_ab = board_text("AB = 5.5", 15, CHALK_GREEN, "BOLD").move_to(
                (A + B) / 2 + DOWN * 0.28)
            # "AD = 5" goes outside the A-D side, clear of it by its own
            # half-extent: a fixed offset laid it straight across the side
            lab_ad = side_label(A, D, (A + B + D) / 3.0, "AD = 5", CHALK_GREEN,
                                15, 0.18)
            self.play(Create(tri_bad),
                      Indicate(ch["a_arc"].arc, color=CHALK_YELLOW,
                               scale_factor=1.08),
                      run_time=min(leftover(tracker, "b1"), 1.2))
            self.play(FadeIn(lab_ab), FadeIn(lab_ad), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            # the badge goes below the card stack: beside the crossing arcs it
            # crowded the vertex C and the two arc ends
            badge = board_text("First triangle: BAD", 18, CHALK_GREEN, "BOLD"
                               ).move_to(np.array([BOARD_CX + 2.4, -1.65, 0]))
            self.appear(badge, tracker, "b2", 0.5)
            self.add_sound(self.sfx["ding"], gain=-13)

            arc_b = compass_arc(B, 3.5 * 0.40, 40, 80, CHALK_PINK)
            arc_d = compass_arc(D, 4.0 * 0.40, 300, 70, CHALK_CYAN)
            c_dot = Dot(radius=0.08, color=CHALK_YELLOW).move_to(C)
            # the sketch already carries the letter C -- reuse it instead of
            # stacking a second copy on the same corner
            c_name = names[2]
            quad = Polygon(A, B, C, D, color=CHALK_CYAN, stroke_width=2.4,
                           fill_color=CHALK_CYAN, fill_opacity=0.12)
            self.play(Create(arc_b), Create(arc_d), run_time=min(
                leftover(tracker, "b3"), 1.6))
            self.play(FadeIn(c_dot, scale=0.5), FadeIn(quad),
                      Indicate(c_dot, color=CHALK_YELLOW, scale_factor=2.0),
                      Circumscribe(c_name, color=CHALK_YELLOW, fade_out=True),
                      run_time=min(leftover(tracker, "b3"), 1.0))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap ------------------------------------------------------
    def beat10_recap(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("Four Sides and One Angle", 23, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            P, Q, R, S = example_frame(origin=np.array([BOARD_CX - 4.1, -1.3, 0]),
                                       scale=0.34)
            tri = Polygon(P, Q, R, color=CHALK_YELLOW, stroke_width=3.4,
                          fill_color=CHALK_YELLOW, fill_opacity=0.16)
            quad = Polygon(P, Q, R, S, color=CHALK_CYAN, stroke_width=2.4,
                           fill_color=CHALK_CYAN, fill_opacity=0.10)
            names = quad_names((P, Q, R, S), "PQRS", 17)
            names[3].shift(np.array([-0.12, 0.12, 0]))   # clear of the pink arc
            arc_p = locating_arc(P, S, 4.0 * 0.34, 18, CHALK_PINK)
            arc_r = locating_arc(R, S, 5.5 * 0.34, 16, CHALK_GREEN)
            s_dot = Dot(radius=0.09, color=CHALK_YELLOW).move_to(S)

            rows = VGroup(
                summary_row(1, "Two sides + included angle:",
                            r"\triangle PQR", CHALK_YELLOW),
                summary_row(2, "Remaining two sides as radii:",
                            r"PS,\ RS", CHALK_PINK),
                summary_row(3, "Intersection gives the fourth vertex:",
                            r"S", CHALK_GREEN),
            ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX + 1.9, 1.35, 0]))
            final = board_text("3 measurements build the triangle, "
                               "2 more locate the fourth vertex.", 19,
                               CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -1.85, 0]))
            small = board_text("Sketch → Triangle → Arcs → Join → Verify", 17,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.3, 0]))

            self.appear(heading, tracker, "b0", 0.45)
            self.play(FadeIn(quad), FadeIn(names), Create(tri), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(rows[0], shift=RIGHT * 0.12), run_time=0.5)
            self.play(Create(arc_p), Create(arc_r), FadeIn(s_dot),
                      FadeIn(rows[1], shift=RIGHT * 0.12), run_time=min(
                          leftover(tracker, "b1"), 1.6))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b1"))

            self.play(Indicate(s_dot, color=CHALK_YELLOW, scale_factor=2.0),
                      FadeIn(rows[2], shift=RIGHT * 0.12), run_time=0.8)
            self.add_sound(self.sfx["success"], gain=-11)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeIn(final, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(small),
                      Circumscribe(quad, color=CHALK_AMBER, stroke_width=3,
                                   time_width=0.5),
                      run_time=min(leftover(tracker, "b3"), 1.2))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b3"))

            summary = VGroup(quad, names, tri, arc_p, arc_r, s_dot, rows,
                             final, small)
            thanks = board_text("Thank You for Watching!", 40, CHALK_WHITE,
                                "BOLD")
            thanks2 = board_text("See you in the next lesson :)", 25, CHALK_CYAN)
            thanks_group = VGroup(thanks, thanks2).arrange(
                DOWN, buff=0.3).move_to(np.array([BOARD_CX, BOARD_CY, 0]))
            self.play(FadeOut(summary), FadeOut(heading), run_time=min(
                leftover(tracker, "b4") * 0.5, 0.8))
            self.play(FadeIn(thanks, shift=UP * 0.1), run_time=0.6)
            self.add_sound(self.sfx["success"], gain=-11)
            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(thanks2, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b5"))
            self.play(Circumscribe(thanks_group, color=CHALK_AMBER,
                                   stroke_width=3, time_width=0.5),
                      run_time=0.25)
            self.play(Indicate(thanks, color=CHALK_WHITE, scale_factor=1.01),
                      run_time=rt(tracker.get_remaining_duration()))
            self._capture_srt(tracker)

        self.wait(END_HOLD)


if __name__ == "__main__":
    pass

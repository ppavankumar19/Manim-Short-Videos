"""
Point, Line Segment, Line & Ray: The Fundamental Building Blocks of Geometry
Story-mode chalkboard lesson (Telangana Class 6 Maths, Chapter 4: Basic
Geometrical Ideas, Storymode 01).

LLM KEY / FUNCTION NAME: fundamental_geometric_building_blocks_point_line_ray

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

The defining visual is ONE OBJECT EVOLVING: a single point A stays alive while a
second point B joins it (segment AB, two endpoints), one end is released (ray
AB, one endpoint) and then the other (line AB, no endpoints), with the endpoint
counter riding from 2 to 1 to 0 beside the same drawing.

Title + 10 scenes:
  0. Title card: the four objects and their endpoint counts.
  1. Geometry is all around us: everyday objects reduce to points, segments
     and endless paths.
  2. A point marks a location: the pencil dot sharpened smaller and smaller,
     the ideal mark, and the naming letters A, B, C.
  3. Line segment: the curved routes fade, the straight join remains, two
     endpoints and a definite length (the ruler).
  4. Line: both ends extend past the frame with arrowheads, 2 -> 0 endpoints,
     A and B are points on the line, and the small-letter name l.
  5. Ray: the torch beam from its initial point, one endpoint, ray AB.
  6. The endpoint test: segment / ray / line with counters 2 / 1 / 0.
  7. Points on the same line: C, A, B on one straight line and the two opposite
     rays from A.
  8. Ray naming: ray OA = ray OB, ray AO is different -- the first letter names
     the starting point.
  9. Your turn: name each diagram, then ray OA against ray OB, after the
     series' centred ten-second THINK clock.
 10. Recap: point -> segment -> ray -> line, and the spoken thank-you card.
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


# (this section is spliced into a head whose own imports omit ArcBetweenPoints,
#  Brace and Ellipse)
from manim import ArcBetweenPoints, Brace, Ellipse  # noqa: E402,F401

# Board layout shared by every scene of this video.
ROW_Y = 2.72             # every scene heading sits on this line
SUB_Y = 2.16             # the one-line sub-heading under it
BANNER_Y = -1.15         # the closing banner, above the strip
# The burned-in caption grows up from the bottom of the frame: a one-line cue
# starts at y = -3.38 and a wrapped two-line cue reaches y = -2.93 (measured on
# the burned 360p cuts), so every closing strip sits at -1.80 and nothing at all
# sits below CAPTION_SAFE_Y = -2.00 -- audited by the IN-CAPTION-BAND check.
STRIP_Y = -1.80
CAPTION_SAFE_Y = -2.00

PANEL_FILL = "#16202B"
LINE_W = 3.6             # chalk stroke width for the geometry itself
TICK_HALF = 0.17         # half-length of an endpoint tick
DOT_R = 0.072            # radius of a chalk point
MARK_SIZE = 18           # ONE size for every point letter in the video
LABEL_DY = 0.34          # ONE offset: every letter sits this far below its dot
                         # (A, B, C / O / P, Q / R / S, T all use it, so the
                         # naming looks the same in every scene and no letter
                         # ever lands on a line, a dot or another label)


# ---------------------------------------------------------------- furniture --
def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


def row_centres(half_widths, gap, cx=BOARD_CX):
    """x centres for a row of figures whose ink is `gap` apart.

    The row's combined ink is centred on `cx` (the green board's centre line)
    and the figures of a row are not all equally wide, so equal centre spacing
    is NOT equal spacing on the board: this returns the centres that leave
    exactly `gap` units of clear air between neighbours.
    """
    total = 2.0 * sum(half_widths) + gap * (len(half_widths) - 1)
    x = cx - total / 2.0
    centres = []
    for half in half_widths:
        centres.append(x + half)
        x += 2.0 * half + gap
    return tuple(centres)


def straight(x1, x2, y, color=CHALK_WHITE, width=LINE_W):
    """A plain straight chalk line between two x positions."""
    return Line(np.array([x1, y, 0.0]), np.array([x2, y, 0.0]),
                stroke_color=color, stroke_width=width)


def ray_line(x1, x2, y, color=CHALK_WHITE, width=LINE_W, tip=0.26):
    """A ray: a straight line with one arrowhead at (x2, y)."""
    return Arrow(np.array([x1, y, 0.0]), np.array([x2, y, 0.0]), buff=0.0,
                 color=color, stroke_color=color, stroke_width=width,
                 tip_length=tip, max_tip_length_to_length_ratio=0.30)


def both_way_line(x1, x2, y, color=CHALK_WHITE, width=LINE_W, tip=0.24):
    """A line: a straight line with an arrowhead at each end."""
    return DoubleArrow(np.array([x1, y, 0.0]), np.array([x2, y, 0.0]), buff=0.0,
                       color=color, stroke_color=color, stroke_width=width,
                       tip_length=tip, max_tip_length_to_length_ratio=0.30)


def end_tick(x, y, color=CHALK_AMBER, half=TICK_HALF, width=3.0):
    """The short cross-stroke that marks an endpoint (or a definite length)."""
    return Line(np.array([x, y - half, 0.0]), np.array([x, y + half, 0.0]),
                stroke_color=color, stroke_width=width)


def dot_point(name=None, x=0.0, y=0.0, color=CHALK_CYAN, size=MARK_SIZE,
              label_dy=LABEL_DY, r=DOT_R):
    """One chalk point with its capital-letter name under it."""
    dot = Dot(radius=r, color=color, fill_opacity=1.0)
    dot.move_to(np.array([float(x), float(y), 0.0]))
    grp = VGroup(dot)
    if name:
        lab = board_text(name, size, color, "BOLD")
        lab.move_to(np.array([float(x), float(y) - label_dy, 0.0]))
        grp.add(lab)
        grp.label = lab
    grp.dot = dot
    return grp


def pair_dots(x1, x2, y, names=("A", "B"), color=CHALK_CYAN, size=MARK_SIZE,
              label_dy=LABEL_DY):
    """Two labelled points on one horizontal line."""
    return VGroup(dot_point(names[0], x1, y, color, size=size,
                            label_dy=label_dy),
                  dot_point(names[1], x2, y, color, size=size,
                            label_dy=label_dy))


def chip(text, color=CHALK_CYAN, size=15, width=None, height=0.50):
    """A small labelled chip."""
    lab = board_text(text, size, color, "BOLD")
    box = RoundedRectangle(corner_radius=0.09,
                           width=width or (lab.width + 0.40), height=height,
                           stroke_color=color, stroke_width=1.7,
                           fill_color=PANEL_FILL, fill_opacity=0.7)
    lab.move_to(box.get_center())
    return VGroup(box, lab)


def card(title, lines, color=CHALK_WHITE, width=3.9, height=1.30,
         title_size=19, line_size=15):
    """A rounded card with a heading and one or two body lines."""
    head = board_text(title, title_size, color, "BOLD")
    body = VGroup(*[board_text(line, line_size, CHALK_WHITE, "BOLD")
                    for line in lines]).arrange(DOWN, buff=0.22)
    box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                           stroke_color=color, stroke_width=2.0,
                           fill_color=PANEL_FILL, fill_opacity=0.55)
    head.move_to(box.get_center() + UP * (height / 2 - 0.24))
    body.move_to(box.get_center() - DOWN * (0.20 if len(lines) > 1 else 0.14))
    return VGroup(box, head, body)


def ruler(length=3.40, height=0.30, color=CHALK_AMBER, ticks=8):
    """The measuring ruler, drawn only where a length is definite."""
    box = RoundedRectangle(corner_radius=0.04, width=length, height=height,
                           stroke_color=color, stroke_width=1.6,
                           fill_color=PANEL_FILL, fill_opacity=0.55)
    marks = VGroup()
    for i in range(ticks + 1):
        x = -length / 2 + length * i / ticks
        drop = 0.15 if i % 2 else 0.10
        marks.add(Line(np.array([x, height / 2, 0.0]),
                       np.array([x, height / 2 - drop, 0.0]),
                       stroke_color=color, stroke_width=1.2))
    return VGroup(box, marks)


def curve_path(x1, x2, y, angle=1.0, color=CHALK_WHITE, width=2.0):
    """One curved route between two points (the paths that are not straight)."""
    return ArcBetweenPoints(np.array([x1, y, 0.0]), np.array([x2, y, 0.0]),
                            angle=angle, stroke_color=color,
                            stroke_width=width)


def torch_icon(color=CHALK_AMBER, scale=1.0):
    """A real torch, lying on its side and pointing right.

    Built from Manim primitives, not a bare rectangle: a tapered barrel with a
    highlight stripe and three grip rings, a switch, a flaring head, and a
    bright lens disc inside a two-step glow.  The barrel's mouth (the lens) is
    where the light -- and therefore the ray -- comes out; `place_torch` pins
    the icon by that lens, and `light_cone` draws the beam itself.
    """
    barrel = Polygon(np.array([-1.02, -0.16, 0.0]),
                     np.array([-0.34, -0.20, 0.0]),
                     np.array([-0.34, 0.20, 0.0]),
                     np.array([-1.02, 0.16, 0.0]),
                     stroke_color=color, stroke_width=1.8,
                     fill_color=color, fill_opacity=0.22)
    shine = Polygon(np.array([-0.98, 0.04, 0.0]),
                    np.array([-0.40, 0.07, 0.0]),
                    np.array([-0.40, 0.13, 0.0]),
                    np.array([-0.98, 0.10, 0.0]),
                    stroke_width=0, fill_color=CHALK_WHITE,
                    fill_opacity=0.22)
    grip = VGroup(*[Line(np.array([x, -0.175, 0.0]),
                         np.array([x, 0.175, 0.0]),
                         stroke_color=color, stroke_width=1.1,
                         stroke_opacity=0.85)
                    for x in (-0.94, -0.82, -0.70)])
    head = Polygon(np.array([-0.36, -0.21, 0.0]),
                   np.array([-0.10, -0.31, 0.0]),
                   np.array([-0.10, 0.31, 0.0]),
                   np.array([-0.36, 0.21, 0.0]),
                   stroke_color=CHALK_YELLOW, stroke_width=1.8,
                   fill_color=CHALK_YELLOW, fill_opacity=0.45)
    switch = Dot(radius=0.030, color=CHALK_PINK, fill_opacity=1.0)
    switch.move_to(np.array([-0.86, -0.07, 0.0]))
    glow = VGroup(*[Circle(radius=r, stroke_width=0,
                           fill_color=CHALK_YELLOW, fill_opacity=op)
                    for r, op in ((0.30, 0.10), (0.21, 0.18))])
    for g in glow:
        g.move_to(np.array([-0.06, 0.0, 0.0]))
    lens = Circle(radius=0.115, stroke_color=CHALK_YELLOW, stroke_width=1.5,
                  fill_color=CHALK_WHITE, fill_opacity=0.95)
    lens.move_to(np.array([-0.06, 0.0, 0.0]))
    grp = VGroup(barrel, shine, grip, head, switch, glow, lens).scale(scale)
    grp.lens = lens
    return grp


def place_torch(torch, lens_x, lens_y):
    """Pin a torch so that its lens sits exactly on (lens_x, lens_y)."""
    c = torch.lens.get_center()
    return torch.shift(np.array([float(lens_x) - c[0], float(lens_y) - c[1],
                                 0.0]))


def light_cone(x0, x1, y, half0=0.11, half1=0.62, color=CHALK_YELLOW,
               opacity=0.15):
    """The beam the ray travels in: a translucent cone widening from the lens."""
    return Polygon(np.array([x0, y - half0, 0.0]),
                   np.array([x0, y + half0, 0.0]),
                   np.array([x1, y + half1, 0.0]),
                   np.array([x1, y - half1, 0.0]),
                   stroke_width=0, fill_color=color, fill_opacity=opacity)


def object_icon(kind, color=CHALK_CYAN, size=0.62):
    """A small chalk drawing of one everyday object, centred on the origin.

    Each one is built from filled, shaded primitives so it reads as the real
    thing and not as an outline: a closed book (cream page block, shaded cover,
    spine, ruled lines, ribbon), a screen (dark bezel, lit glass with a sheen,
    trapezoid stand and base), a rangoli (shaded disc, a ring of eight petals,
    two rings and a petalled centre) and a five-pointed star with a halo.
    """
    s = float(size)
    if kind == "book":
        pages = RoundedRectangle(corner_radius=0.03, width=s * 0.72,
                                 height=s * 0.92, stroke_color=CHALK_WHITE,
                                 stroke_width=1.1, fill_color=CHALK_WHITE,
                                 fill_opacity=0.88)
        pages.shift(RIGHT * s * 0.07)
        cover = RoundedRectangle(corner_radius=0.04, width=s * 0.70,
                                 height=s * 0.98, stroke_color=color,
                                 stroke_width=1.9, fill_color=color,
                                 fill_opacity=0.30)
        cover.shift(LEFT * s * 0.05)
        spine = RoundedRectangle(corner_radius=0.02, width=s * 0.14,
                                 height=s * 0.98, stroke_color=color,
                                 stroke_width=1.3, fill_color=color,
                                 fill_opacity=0.80)
        spine.align_to(cover, LEFT).shift(RIGHT * s * 0.07)
        rules = VGroup(*[
            Line(np.array([-s * 0.10, s * (0.26 - 0.17 * k), 0.0]),
                 np.array([s * 0.27, s * (0.26 - 0.17 * k), 0.0]),
                 stroke_color=CHALK_WHITE, stroke_width=1.3,
                 stroke_opacity=0.85) for k in range(3)])
        ribbon = Polygon(np.array([s * 0.16, s * 0.49, 0.0]),
                         np.array([s * 0.25, s * 0.49, 0.0]),
                         np.array([s * 0.25, s * 0.30, 0.0]),
                         np.array([s * 0.205, s * 0.36, 0.0]),
                         np.array([s * 0.16, s * 0.30, 0.0]),
                         stroke_width=0, fill_color=CHALK_PINK,
                         fill_opacity=0.85)
        return VGroup(pages, cover, spine, rules, ribbon)
    if kind == "screen":
        bezel = RoundedRectangle(corner_radius=0.06, width=s * 1.34,
                                 height=s * 0.92, stroke_color=color,
                                 stroke_width=2.2, fill_color=BLACK,
                                 fill_opacity=0.55)
        bezel.shift(UP * s * 0.12)
        glass = RoundedRectangle(corner_radius=0.04, width=s * 1.16,
                                 height=s * 0.74, stroke_color=color,
                                 stroke_width=1.0, fill_color=CHALK_CYAN,
                                 fill_opacity=0.30)
        glass.move_to(bezel.get_center())
        lit = RoundedRectangle(corner_radius=0.04, width=s * 0.86,
                               height=s * 0.50, stroke_width=0,
                               fill_color=CHALK_CYAN, fill_opacity=0.45)
        lit.move_to(bezel.get_center())
        sheen = Polygon(bezel.get_center() + np.array([-s * 0.56, s * 0.34, 0]),
                        bezel.get_center() + np.array([-s * 0.20, s * 0.34, 0]),
                        bezel.get_center() + np.array([-s * 0.48, -s * 0.34, 0]),
                        bezel.get_center() + np.array([-s * 0.58, -s * 0.34, 0]),
                        stroke_width=0, fill_color=CHALK_WHITE,
                        fill_opacity=0.14)
        neck = Polygon(bezel.get_bottom() + np.array([-s * 0.14, 0.0, 0]),
                       bezel.get_bottom() + np.array([s * 0.14, 0.0, 0]),
                       bezel.get_bottom() + np.array([s * 0.20, -s * 0.14, 0]),
                       bezel.get_bottom() + np.array([-s * 0.20, -s * 0.14, 0]),
                       stroke_color=color, stroke_width=1.4,
                       fill_color=color, fill_opacity=0.30)
        base = RoundedRectangle(corner_radius=0.03, width=s * 0.72,
                                height=s * 0.10, stroke_color=color,
                                stroke_width=1.4, fill_color=color,
                                fill_opacity=0.55)
        base.next_to(neck, DOWN, buff=0.0)
        led = Dot(radius=s * 0.035, color=CHALK_GREEN, fill_opacity=1.0)
        led.move_to(bezel.get_corner(DL) + np.array([s * 0.11, s * 0.08, 0]))
        return VGroup(bezel, glass, lit, sheen, neck, base, led)
    if kind == "rangoli":
        disc = Circle(radius=s * 0.58, stroke_color=color, stroke_width=1.7,
                      fill_color=CHALK_PINK, fill_opacity=0.14)
        petals = VGroup()
        for k in range(8):
            ang = TAU * k / 8.0
            petal = Ellipse(width=s * 0.24, height=s * 0.40,
                            stroke_color=color, stroke_width=1.1,
                            fill_color=(CHALK_PINK if k % 2 else CHALK_YELLOW),
                            fill_opacity=0.45)
            petal.move_to(np.array([np.cos(ang) * s * 0.30,
                                    np.sin(ang) * s * 0.30, 0.0]))
            petal.rotate(ang - PI / 2.0)
            petals.add(petal)
        rings = VGroup(Circle(radius=s * 0.46, stroke_color=CHALK_YELLOW,
                              stroke_width=1.2),
                       Circle(radius=s * 0.18, stroke_color=color,
                              stroke_width=1.2))
        core = Dot(radius=s * 0.075, color=CHALK_YELLOW, fill_opacity=1.0)
        dots = VGroup(*[Dot(radius=s * 0.030, color=CHALK_WHITE,
                            fill_opacity=0.9).move_to(
                                np.array([np.cos(TAU * (k + 0.5) / 8.0) * s * 0.41,
                                          np.sin(TAU * (k + 0.5) / 8.0) * s * 0.41,
                                          0.0])) for k in range(8)])
        return VGroup(disc, petals, rings, dots, core)
    if kind == "star":
        pts, halo_pts = [], []
        for k in range(10):
            ang = PI / 2.0 + k * PI / 5.0
            r = s * 0.60 if k % 2 == 0 else s * 0.24
            pts.append(np.array([np.cos(ang) * r, np.sin(ang) * r, 0.0]))
            halo_pts.append(np.array([np.cos(ang) * r * 1.22,
                                      np.sin(ang) * r * 1.22, 0.0]))
        halo = Polygon(*halo_pts, stroke_width=0, fill_color=CHALK_YELLOW,
                       fill_opacity=0.12)
        star = Polygon(*pts, stroke_color=CHALK_YELLOW, stroke_width=1.7,
                       fill_color=CHALK_YELLOW, fill_opacity=0.38)
        inner = Polygon(*[p * 0.52 for p in pts], stroke_width=0,
                        fill_color=CHALK_WHITE, fill_opacity=0.20)
        sparks = VGroup(*[
            Line(np.array([np.cos(a) * s * 0.72, np.sin(a) * s * 0.72, 0.0]),
                 np.array([np.cos(a) * s * 0.88, np.sin(a) * s * 0.88, 0.0]),
                 stroke_color=CHALK_YELLOW, stroke_width=1.3,
                 stroke_opacity=0.8)
            for a in (PI / 4.0, 3 * PI / 4.0, 5 * PI / 4.0, 7 * PI / 4.0)])
        return VGroup(halo, star, inner, sparks)
    raise ValueError(f"unknown object icon: {kind!r}")


def pictogram(kind, width=2.20, color=CHALK_WHITE, names=(), label_size=MARK_SIZE,
              label_dy=LABEL_DY, marks=True, dot_color=CHALK_CYAN):
    """A small self-contained diagram of one linear object, centred on the
    origin so `at()` can place it exactly.

    `kind` is "point" / "segment" / "ray" / "line"; `names` are the capital
    letters drawn under the dots (P, Q for a segment, R for a ray, S and T for
    the two points inside a line).
    """
    half = float(width) / 2.0
    parts: list = []
    if kind == "point":
        parts.append(Dot(radius=DOT_R, color=dot_color, fill_opacity=1.0))
    elif kind == "segment":
        parts.append(straight(-half, half, 0.0, color))
        parts.append(Dot(radius=DOT_R, color=dot_color, fill_opacity=1.0)
                     .move_to(np.array([-half, 0.0, 0.0])))
        parts.append(Dot(radius=DOT_R, color=dot_color, fill_opacity=1.0)
                     .move_to(np.array([half, 0.0, 0.0])))
        if marks:
            parts.append(end_tick(-half, 0.0, half=TICK_HALF * 0.9))
            parts.append(end_tick(half, 0.0, half=TICK_HALF * 0.9))
    elif kind == "ray":
        parts.append(Arrow(np.array([-half, 0.0, 0.0]),
                           np.array([half, 0.0, 0.0]), buff=0.0, color=color,
                           stroke_color=color, stroke_width=LINE_W,
                           tip_length=0.22,
                           max_tip_length_to_length_ratio=0.30))
        parts.append(Dot(radius=DOT_R, color=dot_color, fill_opacity=1.0)
                     .move_to(np.array([-half, 0.0, 0.0])))
        if marks:
            parts.append(end_tick(-half, 0.0, half=TICK_HALF * 0.9))
    elif kind == "line":
        parts.append(DoubleArrow(np.array([-half, 0.0, 0.0]),
                                 np.array([half, 0.0, 0.0]), buff=0.0,
                                 color=color, stroke_color=color,
                                 stroke_width=LINE_W, tip_length=0.20,
                                 max_tip_length_to_length_ratio=0.30))
        if names:
            for name, x in zip(names, (-half * 0.55, half * 0.55)):
                parts.append(Dot(radius=DOT_R, color=dot_color,
                                 fill_opacity=1.0)
                             .move_to(np.array([x, 0.0, 0.0])))
    else:
        raise ValueError(f"unknown pictogram: {kind!r}")

    grp = VGroup(*parts)
    if names:
        xs = {"point": [0.0],
              "segment": [-half, half],
              "ray": [-half, 0.0],
              "line": [-half * 0.55, half * 0.55]}[kind]
        for x, name in zip(xs, names):
            lab = board_text(name, label_size, color, "BOLD")
            lab.move_to(np.array([x, -label_dy, 0.0]))
            grp.add(lab)
    return grp


def place_line(pict, x, y):
    """Pin a pictogram so that its own straight drawing sits exactly on (x, y).

    The capital letters under the dots are part of the group, so centring the
    group would push the drawing off its row; this keeps the *drawing* -- not
    the bounding box -- on the row, which is what makes two pictograms line up.
    """
    centre = pict.get_center()
    pict.shift(np.array([float(x) - centre[0], float(y) - centre[1], 0.0]))
    return pict


# ----------------------------------------------------------------


NARRATION = {
    "title": (
        "Geometry begins with the simplest things: <bookmark mark='b0'/>a point, a "
        "line segment, a line, and a ray. <bookmark mark='b1'/>Let us build all "
        "four of them from one point, one step at a time."
    ),
    "s1": (
        "Geometry is all around us: the straight edge of a book, the frame of a "
        "television screen, the lines of a rangoli, the shape of a building. "
        "<bookmark mark='b0'/>But every one of those shapes is built from simpler "
        "ideas. <bookmark mark='b1'/>A rectangle is made of straight pieces, a "
        "rangoli is made of lines and points, and a star in the sky is simply a "
        "point very far away. <bookmark mark='b2'/>So what is the simplest thing we "
        "can draw in geometry?"
    ),
    "s2": (
        "Start with a point. <bookmark mark='b0'/>A pencil pressed on paper leaves a "
        "dot. Sharpen the pencil and the dot becomes smaller; sharpen it again and "
        "again, and the dot becomes smaller and smaller. <bookmark mark='b1'/>In "
        "geometry we keep the idea and not the ink: a point marks a location, and it "
        "has no size at all. <bookmark mark='b2'/>We name a point with a capital "
        "letter, like A, or B, or C."
    ),
    "s3": (
        "Now add a second point, B. <bookmark mark='b0'/>Join A to B. Many curved "
        "paths are possible, but only one of them is straight, and that straight "
        "path is the shortest. <bookmark mark='b1'/>This is a line segment. It has "
        "two endpoints, A and B, and it has a definite length, so a ruler can "
        "measure it. <bookmark mark='b2'/>We write it as segment AB."
    ),
    "s4": (
        "Now extend the segment beyond A and beyond B, without stopping. <bookmark "
        "mark='b0'/>It goes on and on in both directions, so we draw arrowheads at "
        "both ends. <bookmark mark='b1'/>A and B are not endpoints any more; they "
        "are simply points lying on the line. <bookmark mark='b2'/>So a line has no "
        "endpoints at all, and we may also name it with a small letter, like l."
    ),
    "s5": (
        "A torch gives us the next idea. <bookmark mark='b0'/>Its light starts at "
        "one point and spreads in one direction, and it never stops. <bookmark "
        "mark='b1'/>In geometry that is a ray: it has exactly one endpoint, called "
        "the initial point, and it goes on endlessly in one direction. <bookmark "
        "mark='b2'/>We write it as ray AB, and the rays of the sun and the rays of a "
        "light are everyday examples."
    ),
    "s6": (
        "How do we tell these three apart? <bookmark mark='b0'/>Count the endpoints. "
        "A line segment has two. <bookmark mark='b1'/>A ray has one. <bookmark "
        "mark='b2'/>A line has none. <bookmark mark='b3'/>And remember: only the "
        "line segment has a definite length, because the ray and the line go on "
        "forever."
    ),
    "s7": (
        "Now put three points on one straight line: C, A and B. <bookmark "
        "mark='b0'/>A lies between C and B, and all three points lie on the same "
        "line. <bookmark mark='b1'/>From A we can draw a ray towards B, and another "
        "ray towards C. <bookmark mark='b2'/>Both rays start at A, and they travel "
        "in opposite directions."
    ),
    "s8": (
        "There is one more rule about naming a ray. <bookmark mark='b0'/>Look at ray "
        "OA: it starts at O and it passes through A and B. <bookmark mark='b1'/>Ray "
        "OB starts at the same point and travels in the same direction, so ray OA "
        "and ray OB are the same ray. <bookmark mark='b2'/>But ray AO starts at A, "
        "so ray AO is a different ray. The first letter always names the starting "
        "point."
    ),
    "s9q": (
        "Your turn. Four quick checks. <bookmark mark='b0'/>For each diagram, say "
        "whether it is a point, a line segment, a line, or a ray. <bookmark "
        "mark='b1'/>Two endpoints joined. <bookmark mark='b2'/>One endpoint with an "
        "arrow. <bookmark mark='b3'/>Arrows at both ends. <bookmark mark='b4'/>And "
        "last of all: can ray OA also be named ray OB?"
    ),
    "s9a": (
        "<bookmark mark='b0'/>The first diagram has two endpoints, so it is the line "
        "segment PQ. <bookmark mark='b1'/>The second has one endpoint and one arrow, "
        "so it is a ray. <bookmark mark='b2'/>The third has arrows at both ends, so "
        "it is a line. <bookmark mark='b3'/>And yes, ray OA can also be named ray "
        "OB, because both start at O and travel in the same direction through the "
        "same straight path."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>A point marks a location. <bookmark "
        "mark='b1'/>Join two points and you have a line segment, with two endpoints "
        "and a definite length. <bookmark mark='b2'/>Extend it one way and it "
        "becomes a ray, with one endpoint; extend it both ways and it becomes a "
        "line, with no endpoints. <bookmark mark='b3'/>From a point, geometry "
        "begins. <bookmark mark='b4'/>Thank you for watching, <bookmark "
        "mark='b5'/>and see you in the next lesson."
    ),
}


class FundamentalGeometricBuildingBlocksStory(VoiceoverScene):
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
        out_dir = _HERE / "media" / "videos" / "fundamental_geometric_building_blocks_point_line_ray"
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
    # Point, Line Segment, Line & Ray (Class 6 Maths, Chapter 4, Storymode 01).
    #
    # SYNC RULE for every reveal: wait for the narration bookmark that ends the
    # phrase describing a thing, and only then bring it on.  Playing first and
    # waiting afterwards shows the picture a whole window early, which reads as
    # broken sync.
    #
    # Layout rules, so the audits stay clean:
    #   * the heading sits on the board's own heading line (2.72) and its
    #     sub-heading at 2.24, the closing banner at -1.15 and the closing strip
    #     at -1.80 -- nothing at all below CAPTION_SAFE_Y = -2.00;
    #   * every diagram is built centred on the origin and then pinned with
    #     `place_line` / `at`, so a heading, a card and a diagram all share the
    #     board centre and two pictograms on one row line up exactly;
    #   * one row per idea, with at least 0.22 units of clear air between the
    #     ink of neighbouring rows (checked by audit_clearance.py);
    #   * the challenge uses the series' shared 10-second THINK clock, dead
    #     centre of the board, and the four question cards sit in the four
    #     corners so the badge never covers one.
    ROW_Y = 2.72
    SUB_Y = 2.10
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

    def q_card(self, title, pict, color=CHALK_CYAN, width=3.00, pad=0.22,
               title_size=13, buff=0.20):
        """One 'your turn' card: a one-line prompt above its small diagram.

        The box is sized around the finished content, so the clearance between
        the ink and the card's own edge is `pad` by construction.
        """
        head = board_text(title, title_size, color, "BOLD")
        content = VGroup(head, pict).arrange(DOWN, buff=buff)
        box = RoundedRectangle(corner_radius=0.10, width=width,
                               height=content.height + 2 * pad,
                               stroke_color=color, stroke_width=1.9,
                               fill_color=PANEL_FILL, fill_opacity=0.55)
        content.move_to(box.get_center())
        return VGroup(box, content)

    def ask_card(self, title, lines, color=CHALK_CYAN, width=3.00, pad=0.22,
                 title_size=15, line_size=14, buff=0.26):
        """One 'your turn' card that asks its question in words."""
        head = board_text(title, title_size, color, "BOLD")
        body = VGroup(*[board_text(line, line_size, CHALK_WHITE, "BOLD")
                        for line in lines]).arrange(DOWN, buff=0.26)
        content = VGroup(head, body).arrange(DOWN, buff=buff)
        box = RoundedRectangle(corner_radius=0.10, width=width,
                               height=content.height + 2 * pad,
                               stroke_color=color, stroke_width=1.9,
                               fill_color=PANEL_FILL, fill_opacity=0.55)
        content.move_to(box.get_center())
        return VGroup(box, content)

    def answer_row(self, tag, headline, note, color, width=8.60, height=0.62,
                   pad=0.34, buff=0.36):
        """One revealed answer: its letter, the object's name and a short note.

        The row is laid out in FIXED COLUMNS rather than centred in its box:
        every row starts at the box's left edge plus `pad`, then tag, name and
        note follow with one constant `buff` between them.  Centring each row
        put the letter at a different x in every row (the names differ in
        width), so A, B, C and D were not on one vertical line; the box itself
        stays centred on BOARD_CX.
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

            title = at(board_text("Point, Line Segment, Line & Ray", 29,
                                  CHALK_PINK, "BOLD"), BOARD_CX, 1.62)
            sub = at(board_text("The Building Blocks of Geometry", 20,
                                CHALK_WHITE, "BOLD"), BOARD_CX, 0.96)

            specs = (("POINT", "point", "0", CHALK_CYAN),
                     ("SEGMENT", "segment", "2", CHALK_GREEN),
                     ("RAY", "ray", "1", CHALK_YELLOW),
                     ("LINE", "line", "0", CHALK_AMBER))
            # ONE centred row: the four pictograms are all 1.60 wide, so equal
            # centre spacing is also equal air, and row_centres lands the row's
            # ink on the board axis.  (The old columns ran -3.45..+3.45, i.e.
            # they were centred on 0.0, half a unit left of BOARD_CX.)
            xs = row_centres((0.80, 0.80, 0.80, 0.80), 0.70)
            labels, pics, counts = VGroup(), VGroup(), VGroup()
            for x, (name, kind, count, color) in zip(xs, specs):
                labels.add(at(board_text(name, 14, color, "BOLD"), x, 0.26))
                pics.add(place_line(pictogram(kind, width=1.60, color=color,
                                              marks=False, dot_color=color),
                                    x, -0.30))
                counts.add(at(board_text(count, 15, CHALK_WHITE, "BOLD"),
                              x, -0.86))
            strip = at(board_text("Every shape begins with these four ideas.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(title, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(sub, shift=UP * 0.08), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.06) for m in labels],
                                  lag_ratio=0.18), run_time=0.55)
            self.play(LaggedStart(*[FadeIn(m, scale=0.85) for m in pics],
                                  lag_ratio=0.18), run_time=0.60)

            self.wait(leftover(tracker, "b1"))
            self.play(LaggedStart(*[FadeIn(m, scale=0.80) for m in counts],
                                  lag_ratio=0.18), run_time=0.55)
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: geometry is all around us ----------------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("Every Shape Starts with Simple Ideas", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Geometry is all around us.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            # the everyday objects are drawn as real, shaded things (a closed
            # book, a lit screen, a petalled rangoli, a five-pointed star) and
            # the row is centred on the board axis with equal air between the
            # four -- measured, not guessed, because the four icons differ in
            # width (0.6 to 1.0)
            kinds = ("book", "screen", "rangoli", "star")
            icons = [object_icon(k, size=0.72) for k in kinds]
            icon_names = [board_text(k, 15, CHALK_CYAN, "BOLD") for k in kinds]
            xicon = row_centres([max(i.width, n.width) / 2.0
                                 for i, n in zip(icons, icon_names)], 1.30)
            icons_row, names_row = VGroup(), VGroup()
            for x, ic, nm in zip(xicon, icons, icon_names):
                icons_row.add(at(ic, x, 1.28))
                names_row.add(at(nm, x, 0.52))

            # the three reductions below are centred on the same axis, with the
            # tiny "point" column measured by its caption (its ink is one dot)
            lower = (("point", "a point", CHALK_CYAN),
                     ("segment", "a straight piece", CHALK_GREEN),
                     ("ray", "an arrowed path", CHALK_YELLOW))
            raw = [pictogram(kind, width=1.80, color=color, marks=False,
                             dot_color=color) for kind, _, color in lower]
            cap = [board_text(label, 15, CHALK_WHITE, "BOLD")
                   for _, label, _ in lower]
            xlow = row_centres([max(p.width, c.width) / 2.0
                                for p, c in zip(raw, cap)], 1.25)
            pics, labs = VGroup(), VGroup()
            for x, pict, label, (_, _, color) in zip(xlow, raw, cap, lower):
                pics.add(place_line(pict, x, -0.18))
                labs.add(at(label, x, -0.68))
            banner = at(board_text("EVERY SHAPE IS BUILT FROM SIMPLE PIECES", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            # the everyday objects arrive while the voice names them
            self.play(LaggedStart(*[FadeIn(m, scale=0.85) for m in icons_row],
                                  lag_ratio=0.30),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.80, 0.9))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.05)
                                    for m in names_row],
                                  lag_ratio=0.20), run_time=0.50)

            self.wait(leftover(tracker, "b1"))
            self.play(LaggedStart(*[FadeIn(m, scale=0.90) for m in pics],
                                  lag_ratio=0.25), run_time=0.60)
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.05) for m in labs],
                                  lag_ratio=0.25), run_time=0.55)
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            question = at(board_text("What is the simplest thing we can draw?",
                                     18, CHALK_PINK, "BOLD"),
                          BOARD_CX, STRIP_Y)
            self.play(FadeIn(question, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, question)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: a point marks a location -----------------------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("A Point Marks a Location", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Start with the simplest object of all.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # the pencil dot, sharpened smaller and smaller; it stands as the
            # left half of a two-part comparison ("the ink" against "the idea"),
            # so the comparison is centred as ONE block on the board axis (the
            # old pair ran -4.28..+3.55, centred 0.36 left of BOARD_CX)
            dx = 0.85
            shrink = VGroup()
            for i, radius in enumerate((0.145, 0.105, 0.075, 0.052)):
                x = -3.30 + i * 0.70 + dx
                shrink.add(Dot(radius=radius, color=CHALK_WHITE,
                               fill_opacity=1.0).move_to(
                                   np.array([x, 1.25, 0.0])))
            shrink_note = at(board_text("a pencil dot, sharpened and sharpened",
                                        14, CHALK_WHITE, "BOLD"), -2.25 + dx,
                             0.42)
            ideal = dot_point("A", 2.10 + dx, 1.25, CHALK_CYAN)
            ideal_note = at(board_text("a location, with no size at all", 14,
                                       CHALK_WHITE, "BOLD"), 2.10 + dx, 0.42)

            pts = VGroup(*[dot_point(name, x, -0.35, CHALK_CYAN)
                           for name, x in (("A", -2.80), ("B", 0.50),
                                           ("C", 3.80))])

            banner = at(board_text("POINT = A LOCATION", 19, CHALK_YELLOW, "BOLD"),
                        BOARD_CX, BANNER_Y)
            strip = at(board_text("Named with a capital letter: A, B, C.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(m, scale=0.7) for m in shrink],
                                  lag_ratio=0.22), run_time=0.70)
            self.play(FadeIn(shrink_note, shift=UP * 0.05), run_time=0.40)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(ideal, scale=0.85), run_time=0.45)
            self.play(FadeIn(ideal_note, shift=UP * 0.05), run_time=0.40)
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(LaggedStart(*[FadeIn(m, scale=0.8) for m in pts],
                                  lag_ratio=0.25), run_time=0.60)
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: the line segment -------------------------------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Join Two Points: the Line Segment", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Only one of the paths between them is straight.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # The segment IS this scene's picture, so it is centred on the
            # board axis with the ruler directly under it and the "definite
            # length" caption under the ruler.  (The old drawing ran -2.60..1.00
            # at centre -0.80 with its ruler at -1.35, and the caption sat out
            # at +2.35: every row of the frame leaned a different way.)
            seg_len = 3.60
            yseg = 0.75
            xa, xb = BOARD_CX - seg_len / 2.0, BOARD_CX + seg_len / 2.0
            notation = at(chalk_math(r"\overline{AB}", size=34, color=CHALK_GREEN),
                          -1.90, 1.45)
            counter = at(chip("2 ENDPOINTS", CHALK_GREEN), 2.30, 1.45)

            curves = VGroup(curve_path(xa, xb, yseg, 0.30, CHALK_WHITE, 1.8),
                            curve_path(xa, xb, yseg, -0.30, CHALK_WHITE, 1.8),
                            curve_path(xa, xb, yseg, 0.14, CHALK_WHITE, 1.5))
            seg = straight(xa, xb, yseg, CHALK_GREEN)
            pts = pair_dots(xa, xb, yseg, ("A", "B"), CHALK_CYAN)
            ruler_mob = at(ruler(seg_len - 0.20, 0.30), BOARD_CX, -0.10)
            len_note = at(board_text("a definite length", 15, CHALK_AMBER,
                                     "BOLD"), BOARD_CX, -0.58)
            banner = at(board_text("LINE SEGMENT = TWO ENDPOINTS", 19,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The shortest path between A and B.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(notation, scale=0.9), FadeIn(counter, scale=0.9),
                      run_time=0.50)

            # the curved routes are tried, then the straight one wins
            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.25),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.55, 1.0))
            self.play(FadeOut(curves), run_time=0.45)
            self.play(Create(seg), FadeIn(pts), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(ruler_mob, shift=UP * 0.06),
                      FadeIn(len_note, shift=UP * 0.06), run_time=0.50)
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: the line ---------------------------------------------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("Extend Both Ways: the Line", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Past A, past B, and on without stopping.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # A and B are the points left over from the segment, so they stay
            # centred on the board axis and the endless line is drawn
            # symmetrically through them; the endpoint counter is one centred
            # chip.  (The old pair sat at centre -0.60 and the chip was parked
            # out at -3.20, three and a half units off the axis.)
            yline = 1.20
            xa, xb = BOARD_CX - 1.30, BOARD_CX + 1.30
            seg = straight(xa, xb, yline, CHALK_GREEN)
            pts = pair_dots(xa, xb, yline, ("A", "B"), CHALK_CYAN)
            extended = both_way_line(-4.30, 5.30, yline, CHALK_AMBER)
            small_l = at(board_text("l", 22, CHALK_AMBER, "BOLD"), 4.50, 1.62)

            counter_old = at(chip("2 ENDPOINTS", CHALK_GREEN), BOARD_CX, 0.20)
            counter_new = at(chip("NO ENDPOINTS", CHALK_AMBER), BOARD_CX, 0.20)
            note = at(board_text("A and B are points on the line, not endpoints.",
                                 16, CHALK_WHITE, "BOLD"), BOARD_CX, -0.55)
            banner = at(board_text("A LINE HAS NO ENDPOINTS", 19, CHALK_YELLOW,
                                   "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("A line may also be named by a small letter.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(seg), FadeIn(pts), FadeIn(counter_old, scale=0.9),
                      run_time=0.55)

            self.wait(leftover(tracker, "b0"))
            self.play(ReplacementTransform(seg, extended),
                      ReplacementTransform(counter_old, counter_new),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.55, 1.1))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(note, shift=UP * 0.06), run_time=0.45)
            self.play(Indicate(pts, color=CHALK_WHITE, scale_factor=1.05),
                      run_time=0.60)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(small_l, scale=0.85), run_time=0.40)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: the ray ----------------------------------------------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("One Starting Point: the Ray", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The light of a torch begins at one point.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # The ray comes OUT of a real torch: a shaded barrel with grip
            # rings and a switch, a flaring head and a glowing lens, and the
            # translucent beam that widens from that lens -- the ray is drawn
            # inside it, so the picture reads "light starts at one point and
            # spreads in one direction".
            xa, xb, yray = -2.90, 0.60, 1.20
            torch = place_torch(torch_icon(), xa - 0.12, yray)
            # the beam widens to 0.90 at the far end: wide enough to read as
            # light, narrow enough that its edges clear every caption (the
            # letters under A and B sit 0.05-0.13 clear of the lower edge, and
            # the sub-heading 0.09 clear of the upper one)
            light = light_cone(xa - 0.10, 4.95, yray, half0=0.13, half1=0.90)
            beam_start = straight(xa, xb, yray, CHALK_YELLOW)
            beam = ray_line(xa, 4.80, yray, CHALK_YELLOW)
            start_dot = dot_point("A", xa, yray, CHALK_CYAN)
            through_b = dot_point("B", xb, yray, CHALK_CYAN)

            initial = at(board_text("INITIAL POINT", 15, CHALK_PINK, "BOLD"),
                         -1.30, 0.72)
            notation = at(chalk_math(r"\overrightarrow{AB}", size=34,
                                     color=CHALK_YELLOW), -1.70, 0.10)
            counter = at(chip("1 ENDPOINT", CHALK_YELLOW), 1.90, 0.10)
            banner = at(board_text("1 ENDPOINT + 1 ENDLESS DIRECTION", 19,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Sun rays, light rays and torch rays all work "
                                  "this way.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(torch, scale=0.9), FadeIn(start_dot), run_time=0.50)
            self.play(Create(beam_start), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(ReplacementTransform(beam_start, beam), FadeIn(light),
                      FadeIn(through_b), run_time=0.65)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(FadeIn(initial, shift=UP * 0.06), run_time=0.45)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(counter, scale=0.9), run_time=0.45)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(notation, scale=0.9), run_time=0.45)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, notation)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: the endpoint test ------------------------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Endpoint Test", 20, CHALK_AMBER, "BOLD"),
                         BOARD_CX, ROW_Y)
            sub = at(board_text("Count the endpoints: two, one, none.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            rows = (("SEGMENT", "segment", "2 ENDPOINTS", CHALK_GREEN, 1.45,
                     ("A", "B")),
                    ("RAY", "ray", "1 ENDPOINT", CHALK_YELLOW, 0.50, ("R",)),
                    ("LINE", "line", "0 ENDPOINTS", CHALK_AMBER, -0.45,
                     ("S", "T")))
            # ONE centred three-column row -- label | diagram | counter -- with
            # the same 0.75 of air either side of the diagram.  (The old row ran
            # -4.38..+3.24, so its centre sat 1.07 left of the board axis.)
            tags, pics, counts = VGroup(), VGroup(), VGroup()
            for label, kind, count, color, y, nm in rows:
                tags.add(at(board_text(label, 15, color, "BOLD"), -2.70, y))
                pics.add(place_line(pictogram(kind, width=3.00, color=color,
                                              names=nm,
                                              marks=(kind != "line")), 0.10, y))
                counts.add(at(chip(count, color, size=15), 3.30, y))
            banner = at(board_text("2 → SEGMENT   ·   1 → RAY   ·   0 → LINE", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Only the segment has a definite length.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(tags, shift=UP * 0.05), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(pics[0], scale=0.9), FadeIn(counts[0], scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(pics[1], scale=0.9), FadeIn(counts[1], scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(pics[2], scale=0.9), FadeIn(counts[2], scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: points on the same line ------------------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Points on the Same Line", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("C, A and B lie on one straight line.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # C, A and B on one line, the whole diagram centred on the board
            # axis: the line, the three points and the two opposite rays are
            # symmetric about A, and the two ray names sit under the ray tips.
            # (The old line ran -3.40..+3.40 and the points -2.20..+2.00, i.e.
            # centred on 0.0 and -0.10.)  Every letter now sits the one marker
            # offset BELOW its point, as it does in every other scene.
            yline = 1.05
            xc, xa, xb = -1.70, 0.30, 2.50
            base = straight(-2.90, 3.90, yline, CHALK_WHITE, 2.2)
            pts = VGroup(*[dot_point(name, x, yline, color)
                           for name, x, color in (("C", xc, CHALK_CYAN),
                                                  ("A", xa, CHALK_PINK),
                                                  ("B", xb, CHALK_CYAN))])
            # the two rays replace the plain line: one to B, one to C
            ray_ab = ray_line(xa, 3.90, yline, CHALK_CYAN)
            ray_ac = Arrow(np.array([xa, yline, 0.0]),
                           np.array([-2.90, yline, 0.0]), buff=0.0,
                           color=CHALK_PINK, stroke_color=CHALK_PINK,
                           stroke_width=LINE_W, tip_length=0.24,
                           max_tip_length_to_length_ratio=0.30)
            note = at(board_text("Both rays start at A.", 16, CHALK_WHITE, "BOLD"),
                      BOARD_CX, -0.20)
            notation_c = at(chalk_math(r"\overrightarrow{AC}", size=32,
                                       color=CHALK_PINK), -2.90, -0.80)
            notation_b = at(chalk_math(r"\overrightarrow{AB}", size=32,
                                       color=CHALK_CYAN), 3.90, -0.80)
            banner = at(board_text("SAME STRAIGHT LINE", 19, CHALK_YELLOW, "BOLD"),
                        BOARD_CX, BANNER_Y)
            strip = at(board_text("Two rays, one starting point, opposite "
                                  "directions.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(base), run_time=0.55)
            self.play(LaggedStart(*[FadeIn(m, scale=0.8) for m in pts],
                                  lag_ratio=0.25), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.45)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeOut(base), Create(ray_ab), FadeIn(notation_b, scale=0.9),
                      run_time=0.55)
            self.play(Create(ray_ac), FadeIn(notation_c, scale=0.9),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(note, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, note)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: why the order of the letters matters -----------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("Why the Order of Letters Matters", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The first letter names the starting point.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # the three points sit on the ray in the middle of the board, the
            # letters below them at the one marker offset (they used to be
            # labelled from above, the only scene in the video that did)
            yray = 1.45
            xo, xa, xb = -2.10, 0.80, 2.80
            beam = ray_line(xo, 4.80, yray, CHALK_YELLOW)
            pts = VGroup(*[dot_point(name, x, yray, color)
                           for name, x, color in (("O", xo, CHALK_PINK),
                                                  ("A", xa, CHALK_CYAN),
                                                  ("B", xb, CHALK_CYAN))])

            same = at(self.ask_card("ray OA = ray OB",
                                    ["same start, same direction"],
                                    CHALK_GREEN, width=4.20), -1.75, -0.05)
            differ = at(self.ask_card("ray AO is different",
                                      ["the start changes to A"],
                                      CHALK_PINK, width=4.20), 2.75, -0.05)
            banner = at(board_text("THE FIRST LETTER NAMES THE INITIAL POINT",
                                   18, CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Ray AO starts at A, so it is a different ray.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(beam), FadeIn(pts), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Indicate(pts[0], color=CHALK_PINK, scale_factor=1.15),
                      run_time=0.55)
            self.play(FadeIn(same, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Indicate(pts[1], color=CHALK_CYAN, scale_factor=1.15),
                      run_time=0.55)
            self.play(FadeIn(differ, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 9: your turn (questions, the silent clock, then the answers) ---
    def beat_s9(self) -> None:
        with self.voiceover(text=NARRATION["s9q"]) as tracker:
            self.reset_board()

            heading = at(board_text("YOUR TURN", 26, CHALK_PINK, "BOLD"),
                         BOARD_CX, 2.78)
            sub = at(board_text("Name each object, then answer the last question.",
                                16, CHALK_WHITE, "BOLD"), BOARD_CX, 2.22)

            qa = at(self.q_card("name this object",
                                pictogram("segment", width=1.90, color=CHALK_GREEN,
                                          names=("P", "Q")),
                                CHALK_GREEN), -2.75, 1.25)
            qb = at(self.q_card("name this object",
                                pictogram("ray", width=1.90, color=CHALK_YELLOW,
                                          names=("R",)),
                                CHALK_YELLOW), 3.75, 1.25)
            qc = at(self.q_card("name this object",
                                pictogram("line", width=1.90, color=CHALK_AMBER,
                                          names=("S", "T")),
                                CHALK_AMBER), -2.75, -1.15)
            qd = at(self.ask_card("ray OA", ["can it also be",
                                             "named ray OB?"],
                                  CHALK_CYAN, width=3.00), 3.75, -1.15)

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
            a1 = at(self.answer_row("A", "LINE SEGMENT PQ", "2 endpoints",
                                    CHALK_GREEN), BOARD_CX, 1.62)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "RAY", "1 endpoint", CHALK_YELLOW),
                    BOARD_CX, 0.82)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "LINE", "0 endpoints", CHALK_AMBER),
                    BOARD_CX, 0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "YES — ray OA = ray OB",
                                    "both start at O", CHALK_CYAN),
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

            heading = at(board_text("One Idea, Four Objects", 24, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)

            stages = (("POINT", "point", "marks a location", CHALK_CYAN, ()),
                      ("SEGMENT", "segment", "2 endpoints", CHALK_GREEN,
                       ("A", "B")),
                      ("RAY", "ray", "1 endpoint", CHALK_YELLOW, ("A",)),
                      ("LINE", "line", "0 endpoints", CHALK_AMBER, ()))
            # Four fixed columns centred as ONE block on the board axis (they
            # used to run -3.45..+3.45, i.e. centred on 0.0), every picture
            # letter at the video's one marker offset BELOW its endpoint, and
            # each of the three text rows sitting under its own column -- the
            # last row used to be one centred sentence that belonged to no
            # column in particular.
            xs = [BOARD_CX - 3.45 + i * 2.30 for i in range(4)]
            names, pics, notes, rules = VGroup(), VGroup(), VGroup(), VGroup()
            for x, (label, kind, note, color, marks) in zip(xs, stages):
                names.add(at(board_text(label, 16, color, "BOLD"), x, 1.48))
                pics.add(place_line(pictogram(kind, width=1.70, color=color,
                                              names=marks, marks=False),
                                    x, 0.88))
                notes.add(at(board_text(note, 14, CHALK_WHITE, "BOLD"), x, 0.10))
            for x, entry in zip(xs, ("POINT = LOCATION", "SEGMENT = 2",
                                     "RAY = 1", "LINE = 0")):
                rules.add(at(board_text(entry, 13, CHALK_WHITE, "BOLD"),
                             x, -0.45))
            final = at(board_text("FROM A POINT, GEOMETRY BEGINS", 20,
                                  CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Location → Connection → One Way → Both Ways",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)
            thanks = at(board_text("Thank You for Watching!", 30, CHALK_WHITE,
                                   "BOLD"), BOARD_CX, 0.62)
            bye = at(board_text("See you in the next lesson :)", 22, CHALK_YELLOW,
                                "BOLD"), BOARD_CX, -0.32)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(names[0], shift=UP * 0.06),
                      FadeIn(pics[0], scale=0.9),
                      FadeIn(notes[0], shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(names[1], shift=UP * 0.06),
                      FadeIn(pics[1], scale=0.9),
                      FadeIn(notes[1], shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(names[2], shift=UP * 0.06),
                      FadeIn(pics[2], scale=0.9),
                      FadeIn(notes[2], shift=UP * 0.06),
                      FadeIn(names[3], shift=UP * 0.06),
                      FadeIn(pics[3], scale=0.9),
                      FadeIn(notes[3], shift=UP * 0.06), run_time=0.70)
            self.play(FadeIn(rules, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(final, shift=UP * 0.06), run_time=0.45)

            # the closing card is narrated: it appears as the voice says
            # "Thank you for watching,", the goodbye line as the voice says
            # "and see you in the next lesson."
            self.wait(leftover(tracker, "b4"))
            self.play(FadeOut(heading), FadeOut(names), FadeOut(pics),
                      FadeOut(notes), FadeOut(rules), FadeOut(final),
                      FadeOut(strip), run_time=0.55)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.50)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.closing(tracker, thanks, run_time=1.1)
            self._capture_srt(tracker)

        self.wait(END_HOLD)

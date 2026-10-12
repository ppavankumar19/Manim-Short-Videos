"""
Understanding Curves & Regions: Open, Closed, Interior, Exterior & Boundary
Story-mode chalkboard lesson (Telangana Class 6 Maths, Chapter 4: Basic
Geometrical Ideas, Storymode 02).

LLM KEY / FUNCTION NAME: curves_open_closed_and_regions

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

The defining visual is ONE PENCIL PATH: an open wave, a closed loop and a
self-crossing figure eight are drawn in turn, and the closed loop then becomes
the park boundary whose interior, boundary and exterior separate the plane.

Title + 10 scenes:
  0. Title card: curve, open/closed, simple/self-crossing, region.
  1. One pencil, many curves: even a straight line is a curve.
  2. Open or closed: does the path come back and close?
  3. Simple or self-crossing: does the path cross itself?
  4. Two different questions: open/closed vs simple/not-simple.
  5. A closed curve separates the plane: boundary wall, interior, exterior.
  6. Where is the point: inside, on the edge, or outside?
  7. Region = interior + boundary.
  8. From a closed curve to a polygon: the line-segment bridge.
  9. Your turn: classify four diagrams after the centred ten-second THINK clock.
 10. Recap: draw -> classify -> locate, and the spoken thank-you card.
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


# (this section is spliced into a head whose own imports omit Ellipse and
#  VMobject; everything else -- Dot, RoundedRectangle, VGroup, PI, np -- is
#  already imported by the head)
from manim import Ellipse, VMobject  # noqa: E402,F401

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
STROKE_W = 3.4           # chalk stroke width for the curves themselves
DOT_R = 0.072            # radius of a chalk point
LOOP_SPEED = 2.4         # rad/s of the title card's travelling trace point
                         # (a full lap of the closed loop every ~2.6 s)


# ---------------------------------------------------------------- furniture --
def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


def row_centres(half_widths, gap, cx=BOARD_CX):
    """x centres for a row of figures whose ink is `gap` apart.

    The row's combined ink is centred on `cx` (the green board's centre line)
    and the four figures of "one pencil, many curves" are not equally wide, so
    equal centre spacing is NOT equal spacing on the board: this returns the
    centres that leave exactly `gap` units of clear air between neighbours.
    """
    total = 2.0 * sum(half_widths) + gap * (len(half_widths) - 1)
    x = cx - total / 2.0
    centres = []
    for half in half_widths:
        centres.append(x + half)
        x += 2.0 * half + gap
    return tuple(centres)


def loop_point(cx, cy, w, h, phase):
    """A point on a closed oval loop at `phase` radians (0 = right vertex).

    The title card's trace point is driven by this instead of by Rotate: a
    rotation about the centre would trace a circle and leave the oval, while
    the parametric point stays on the drawn loop at every angle.
    """
    return np.array([float(cx) + (w / 2.0) * np.cos(phase),
                     float(cy) + (h / 2.0) * np.sin(phase), 0.0])


def straight_line(x1, x2, y, color=CHALK_WHITE, width=STROKE_W):
    """A plain straight chalk line between two x positions."""
    from manim import Line  # noqa: E402  (already imported by the head)
    return Line(np.array([x1, y, 0.0]), np.array([x2, y, 0.0]),
                stroke_color=color, stroke_width=width)


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


def dot_point(name=None, x=0.0, y=0.0, color=CHALK_CYAN, size=20,
              label_dy=0.34, r=DOT_R):
    """One chalk point with its capital-letter name under (or over) it."""
    dot = Dot(radius=r, color=color, fill_opacity=1.0)
    dot.move_to(np.array([float(x), float(y), 0.0]))
    grp = VGroup(dot)
    if name:
        lab = board_text(name, size, color, "BOLD")
        lab.move_to(np.array([float(x), float(y) + label_dy, 0.0]))
        grp.add(lab)
        grp.label = lab
    grp.dot = dot
    return grp


def open_wave(color=CHALK_CYAN, width=2.70, amp=0.52, cycles=1.5, n=60,
              stroke=STROKE_W):
    """An open wavy path: two free ends, no self-crossing."""
    xs = np.linspace(-width / 2.0, width / 2.0, n)
    ys = amp * np.sin(2.0 * PI * cycles * xs / width)
    pts = np.stack([xs, ys, np.zeros_like(xs)], axis=1)
    vm = VMobject().set_points_smoothly(pts)
    vm.set_stroke(color, stroke)
    return vm


def oval(color=CHALK_GREEN, w=2.50, h=1.70, stroke=STROKE_W):
    """A smooth closed loop (the simple closed curve)."""
    return Ellipse(width=w, height=h, stroke_color=color, stroke_width=stroke)


def figure_eight(color=CHALK_PINK, a=0.95, n=120, stroke=STROKE_W):
    """A closed self-crossing curve: the lemniscate (a figure eight)."""
    t = np.linspace(0.0, 2.0 * PI, n, endpoint=False)
    denom = 1.0 + np.sin(t) ** 2
    x = a * np.cos(t) / denom
    y = a * np.sin(t) * np.cos(t) / denom
    pts = np.stack([x, y, np.zeros_like(x)], axis=1)
    vm = VMobject().set_points_smoothly(pts)
    vm.set_stroke(color, stroke)
    return vm


def interior_fill(w=2.50, h=1.70, color=CHALK_CYAN, opacity=0.22):
    """The shaded interior of a closed figure (drawn behind its boundary)."""
    return Ellipse(width=w, height=h, stroke_width=0, fill_color=color,
                   fill_opacity=opacity)


# ----------------------------------------------------------------


NARRATION = {
    "title": (
        "A curve is one of the first ideas in geometry. <bookmark mark='b0'/>It "
        "is a drawing made without lifting the pencil from the paper. <bookmark "
        "mark='b1'/>Some curves close up, and some stay open; and a closed curve "
        "separates the plane into an inside and an outside. Let us learn how to "
        "tell them apart."
    ),
    "s1": (
        "Imagine drawing with a pencil, and never lifting it from the paper. "
        "<bookmark mark='b0'/>You might draw a wavy path, or a loop, or a path "
        "that crosses itself. <bookmark mark='b1'/>And here is a surprise: in "
        "geometry, even a straight line is a curve. <bookmark mark='b2'/>So a "
        "curve is any figure drawn in one continuous stroke, without lifting the "
        "pencil."
    ),
    "s2": (
        "Now ask the first question: does the path close? <bookmark mark='b0'/>"
        "Look at this wavy path. Its two ends stay apart, so it is an open "
        "curve. <bookmark mark='b1'/>Now look at this loop. The pencil comes all "
        "the way back to its starting point, so the path closes. <bookmark "
        "mark='b2'/>That is a closed curve."
    ),
    "s3": (
        "The second question is: does the path cross itself? <bookmark "
        "mark='b0'/>This loop never crosses itself, so it is a simple curve. "
        "<bookmark mark='b1'/>But this figure crosses itself, right here, where "
        "the two parts meet. <bookmark mark='b2'/>So it is not simple. A simple "
        "curve is simply one that does not cross itself."
    ),
    "s4": (
        "These are two different questions. <bookmark mark='b0'/>This wavy path "
        "is open, because its ends stay apart, and simple, because it never "
        "crosses itself. <bookmark mark='b1'/>This oval is closed, and it is "
        "simple too. <bookmark mark='b2'/>But this figure is closed and it "
        "crosses itself, so it is not simple. Open or closed, and simple or not "
        "simple, are two separate questions."
    ),
    "s5": (
        "Now watch what a closed curve does. <bookmark mark='b0'/>It is like the "
        "boundary wall of a park. <bookmark mark='b1'/>The wall splits the plane "
        "into three parts: the inside, which we call the interior; the wall "
        "itself, the boundary; and the outside, the exterior. <bookmark "
        "mark='b2'/>To get from outside the park to inside, you must cross the "
        "boundary."
    ),
    "s6": (
        "So when you see a closed figure, ask: where is each point? <bookmark "
        "mark='b0'/>A point inside is in the interior. <bookmark mark='b1'/>A "
        "point exactly on the edge is on the boundary. <bookmark mark='b2'/>And "
        "a point outside is in the exterior."
    ),
    "s7": (
        "Now we can say what a region is. <bookmark mark='b0'/>The region is the "
        "interior and the boundary taken together. <bookmark mark='b1'/>The "
        "interior alone is not the whole region; the edge is part of the region "
        "too. <bookmark mark='b2'/>Region equals interior plus boundary."
    ),
    "s8": (
        "One more step connects curves to the shapes we study next. <bookmark "
        "mark='b0'/>If a simple closed curve is made of straight line segments, "
        "<bookmark mark='b1'/>it is called a polygon. <bookmark mark='b2'/>So a "
        "polygon is a special kind of simple closed figure, and we will meet it "
        "very soon."
    ),
    "s9q": (
        "Your turn. Four quick checks. <bookmark mark='b0'/>For each diagram, say "
        "whether the curve is open or closed, and simple or not simple. <bookmark "
        "mark='b1'/>A wavy path with two free ends. <bookmark mark='b2'/>A closed "
        "oval. <bookmark mark='b3'/>A path that crosses itself. <bookmark "
        "mark='b4'/>And last of all: in this closed figure, point P is inside, "
        "point Q is on the edge, and point R is outside. Classify P, Q and R."
    ),
    "s9a": (
        "<bookmark mark='b0'/>The first is open, because its ends do not meet, "
        "and simple, because it never crosses itself. <bookmark mark='b1'/>The "
        "second is closed and simple: a smooth oval. <bookmark mark='b2'/>The "
        "third crosses itself, so it is not simple. <bookmark mark='b3'/>And in "
        "the last figure, P is in the interior, Q is on the boundary, and R is in "
        "the exterior."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>A curve is drawn without lifting the "
        "pencil. <bookmark mark='b1'/>If the ends stay apart, it is open; if they "
        "join, it is closed. <bookmark mark='b2'/>And if it never crosses itself, "
        "it is simple. <bookmark mark='b3'/>A closed curve gives us interior, "
        "boundary and exterior, and the region is the interior plus the "
        "boundary. <bookmark mark='b4'/>Draw, classify, locate. <bookmark "
        "mark='b5'/>Thank you for watching, <bookmark mark='b6'/>and see you in "
        "the next lesson."
    ),
}


class CurvesOpenClosedRegionsStory(VoiceoverScene):
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
        out_dir = _HERE / "media" / "videos" / "curves_open_closed_and_regions"
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
    # Curves & Regions (Class 6 Maths, Chapter 4, Storymode 02).
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
    #   * every curve is built centred on the origin and then pinned with `at`,
    #     so a heading, a card and a diagram all share the board centre;
    #   * one row per idea, with at least 0.22 units of clear air between the
    #     ink of neighbouring rows (checked by audit_clearance.py);
    #   * the challenge uses the series' shared 10-second THINK clock, dead
    #     centre of the board, and the four question cards sit in the four
    #     corners so the badge never covers one.

    def closing(self, tracker, mob=None, color=CHALK_YELLOW, run_time=None):
        """Consume the tail of the narration window on the last reveal."""
        budget = rt(tracker.get_remaining_duration()) if run_time is None \
            else run_time
        if mob is None:
            self.wait(max(budget, 0.0))
        else:
            self.play(Indicate(mob, color=color, scale_factor=1.03),
                      run_time=max(budget, MIN_RT))

    def q_card(self, title, pict, color=CHALK_CYAN, width=3.00, pad=0.18,
               title_size=13, buff=0.24):
        """One 'your turn' card: a one-line prompt above its small diagram."""
        head = board_text(title, title_size, color, "BOLD")
        content = VGroup(head, pict).arrange(DOWN, buff=buff)
        box = RoundedRectangle(corner_radius=0.10, width=width,
                               height=content.height + 2 * pad,
                               stroke_color=color, stroke_width=1.9,
                               fill_color=PANEL_FILL, fill_opacity=0.55)
        content.move_to(box.get_center())
        return VGroup(box, content)

    def curve_card(self, title, curve, color, width=2.80, pad=0.24,
                   title_size=14, buff=0.20):
        """A titled card around a small curve (used in the 2-question scene)."""
        head = board_text(title, title_size, color, "BOLD")
        content = VGroup(head, curve).arrange(DOWN, buff=buff)
        box = RoundedRectangle(corner_radius=0.10, width=width,
                               height=content.height + 2 * pad,
                               stroke_color=color, stroke_width=1.9,
                               fill_color=PANEL_FILL, fill_opacity=0.55)
        content.move_to(box.get_center())
        return VGroup(box, content)

    def region_mini(self, color=CHALK_GREEN, w=1.40, h=0.64):
        """A small closed figure with P inside, Q on the edge, R outside.

        The letters sit *around* the drawing, so the card stays short enough to
        keep clear of the caption band below the board -- but each one is also
        a clear 0.2+ away from the curve: Q's letter sits ABOVE the top vertex
        (beside it, the arc curved under the letter and touched it) and R's
        letter is a full step to the right of the right vertex."""
        oval = Ellipse(width=w, height=h, stroke_color=color, stroke_width=2.6)
        fill = Ellipse(width=w, height=h, stroke_width=0, fill_color=CHALK_CYAN,
                       fill_opacity=0.18)
        # P -- inside the edge, its letter beside the dot, all well within
        pdot = Dot(radius=DOT_R, color=CHALK_CYAN, fill_opacity=1.0).move_to(
            np.array([-0.36, 0.0, 0.0]))
        plab = board_text("P", 13, CHALK_CYAN, "BOLD").move_to(
            np.array([-0.16, 0.0, 0.0]))
        # Q -- exactly on the edge, the letter above the top vertex
        qdot = Dot(radius=DOT_R, color=CHALK_AMBER, fill_opacity=1.0).move_to(
            np.array([0.0, h / 2.0, 0.0]))
        qlab = board_text("Q", 13, CHALK_AMBER, "BOLD").move_to(
            np.array([0.0, h / 2.0 + 0.32, 0.0]))
        # R -- outside the edge
        rdot = Dot(radius=DOT_R, color=CHALK_PINK, fill_opacity=1.0).move_to(
            np.array([w / 2.0 + 0.22, 0.0, 0.0]))
        rlab = board_text("R", 13, CHALK_PINK, "BOLD").move_to(
            np.array([w / 2.0 + 0.44, 0.0, 0.0]))
        return VGroup(fill, oval, pdot, plab, qdot, qlab, rdot, rlab)

    def answer_row(self, tag, headline, note, color, width=8.60, height=0.62,
                   pad=0.34, buff=0.36):
        """One revealed answer: its letter, the result and a short note.

        The row is laid out in FIXED COLUMNS, not centred in the box: every row
        starts at the box's left edge plus `pad`, then tag, sentence and note
        follow with one constant `buff` between them.  Centring each row put the
        letter at a different x in every row (the sentences differ in width), so
        the answers scene read "A  OPEN + SIMPLE" / "B   CLOSED ..." with the
        letters and gaps all out of line; the recap rows had the same defect.
        With the row anchored left the tag column is one vertical line and the
        sentence column starts at the same x in every row, while the box itself
        stays centred on BOARD_CX.  The widest row (D: P interior · Q boundary ·
        R exterior / inside · on · outside) is 7.08 wide against 7.92 of room.
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

            title = at(board_text("Understanding Curves & Regions", 27,
                                  CHALK_PINK, "BOLD"), BOARD_CX, 1.66)
            sub = at(board_text("Open · Closed · Interior · Exterior · Boundary",
                                18, CHALK_WHITE, "BOLD"), BOARD_CX, 1.06)

            specs = (("OPEN", "open_wave", "the ends stay apart", CHALK_CYAN),
                     ("CLOSED", "oval", "the path joins back", CHALK_GREEN),
                     ("NOT SIMPLE", "eight", "the path crosses itself",
                      CHALK_PINK))
            # One evenly spaced row: the three figures' ink is centred on the
            # board axis and every label/caption sits clear of its own curve
            # (the old card put OPEN on the wave's crest, CLOSED on the oval's
            # top and "the path joins back" across the oval's lower arc).
            # The three rows are stacked with >= 0.20 of clear air everywhere:
            # heading 1.66 / sub 1.06 / labels 0.52 / figures -0.38 /
            # captions -1.20, each caption still a clear 0.20 under its curve
            # and 0.41 above the closing strip.
            loop_w, loop_h = 1.50, 1.05
            xs = row_centres((0.85, loop_w / 2.0, 0.55), 1.10)
            lab_y, pic_y, note_y = 0.52, -0.38, -1.20
            labels, pics, notes = VGroup(), VGroup(), VGroup()
            for x, (label, kind, note, color) in zip(xs, specs):
                labels.add(at(board_text(label, 14, color, "BOLD"), x, lab_y))
                curve = (open_wave(color, width=1.70, amp=0.40) if kind == "open_wave"
                         else oval(color, w=loop_w, h=loop_h) if kind == "oval"
                         else figure_eight(color, a=0.55))
                pics.add(at(curve, x, pic_y))
                notes.add(at(board_text(note, 12, CHALK_WHITE, "BOLD"), x, note_y))
            strip = at(board_text("A curve is drawn without lifting the pencil.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            # The pencil tip that drew the closed loop keeps travelling round
            # it for the whole hold -- through the waits and the closing
            # Indicate -- because the phase is advanced on every frame, not by
            # a fixed-length Rotate.  (A Rotate about the centre would trace a
            # circle and leave the oval, so the point is parametric.)  It is
            # chalk-yellow, not green, so the travelling tip stays visible
            # against the green loop it is drawing.
            phase = ValueTracker(0.0)
            trace = Dot(radius=0.055, color=CHALK_YELLOW, fill_opacity=1.0)
            trace.move_to(loop_point(xs[1], pic_y, loop_w, loop_h, 0.0))
            trace.add_updater(lambda m: m.move_to(
                loop_point(xs[1], pic_y, loop_w, loop_h, phase.get_value())))
            phase.add_updater(lambda m, dt: m.increment_value(dt * LOOP_SPEED))

            self.play(FadeIn(title, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.06) for m in labels],
                                  lag_ratio=0.18), run_time=0.55)
            self.play(LaggedStart(*[Create(m) for m in pics], lag_ratio=0.22),
                      run_time=0.75)
            self.add(phase)
            self.play(FadeIn(trace, scale=0.7), run_time=0.30)

            self.wait(leftover(tracker, "b1"))
            self.play(LaggedStart(*[FadeIn(m, scale=0.85) for m in notes],
                                  lag_ratio=0.18), run_time=0.55)
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: one pencil, many curves ------------------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("One Pencil, Many Curves", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A curve is drawn without lifting the pencil.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            xa = row_centres((0.95, 0.725, 0.62, 0.85), 0.75)
            pic_y, name_y = 1.10, 0.22
            wave = at(open_wave(CHALK_CYAN, width=1.90, amp=0.45), xa[0], pic_y)
            loop = at(oval(CHALK_GREEN, w=1.45, h=1.00), xa[1], pic_y)
            eight = at(figure_eight(CHALK_PINK, a=0.62), xa[2], pic_y)
            line = at(straight_line(xa[3] - 0.85, xa[3] + 0.85, pic_y, CHALK_YELLOW),
                      xa[3], pic_y)
            names = VGroup(*[
                at(board_text(n, 13, c, "BOLD"), x, name_y)
                for n, c, x in (("a wavy path", CHALK_CYAN, xa[0]),
                                ("a loop", CHALK_GREEN, xa[1]),
                                ("a crossing path", CHALK_PINK, xa[2]),
                                ("even a straight line", CHALK_YELLOW, xa[3]))])

            banner = at(board_text("YES — EVEN A STRAIGHT LINE IS A CURVE", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Any figure drawn in one continuous stroke.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(wave), Create(loop), Create(eight), run_time=1.1)
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.05) for m in names],
                                  lag_ratio=0.2), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(line), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: open or closed ---------------------------------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("Open or Closed?", 20, CHALK_AMBER, "BOLD"),
                         BOARD_CX, ROW_Y)
            sub = at(board_text("Question 1: does the path close?", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # Two columns, one evenly spaced row: the pair's ink is centred on
            # the board axis, the captions sit UNDER their figure (the old card
            # ran "the path comes back and closes" straight through the oval's
            # lower arc) and the chips sit clear below the captions.
            yc, note_y, chip_y = 1.25, 0.26, -0.45
            xs = row_centres((1.35, 1.10), 1.50)
            wave = at(open_wave(CHALK_CYAN, width=2.70, amp=0.55), xs[0], yc)
            open_note = at(board_text("the two ends stay apart", 14, CHALK_WHITE,
                                      "BOLD"), xs[0], note_y)
            open_chip = at(chip("OPEN CURVE", CHALK_CYAN), xs[0], chip_y)
            oval_mob = at(oval(CHALK_GREEN, w=2.20, h=1.10), xs[1], yc)
            close_note = at(board_text("the path comes back and closes", 14,
                                       CHALK_WHITE, "BOLD"), xs[1], note_y)
            close_chip = at(chip("CLOSED CURVE", CHALK_GREEN), xs[1], chip_y)

            banner = at(board_text("QUESTION 1: DOES THE PATH CLOSE?", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("If the ends meet, the curve is closed.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(wave), run_time=0.70)
            self.play(FadeIn(open_note, shift=UP * 0.05),
                      FadeIn(open_chip, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(oval_mob), run_time=0.70)
            self.play(FadeIn(close_note, shift=UP * 0.05),
                      FadeIn(close_chip, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: simple or self-crossing ------------------------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Simple or Self-Crossing?", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Question 2: does it cross itself?", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # Same two-column shape as the open/closed frame: both figures end
            # on a common line (y = 0.70) so the captions can sit clear below
            # them -- "never crosses itself" used to cut the oval's lower arc
            # and "it crosses itself here" the figure-eight itself.
            note_y, chip_y = 0.30, -0.45
            ox, ex = row_centres((1.10, 1.15), 1.50)
            oval_mob = at(oval(CHALK_GREEN, w=2.20, h=1.10), ox, 1.25)
            simple_note = at(board_text("never crosses itself", 14, CHALK_WHITE,
                                        "BOLD"), ox, note_y)
            simple_chip = at(chip("SIMPLE", CHALK_GREEN), ox, chip_y)

            eight = at(figure_eight(CHALK_PINK, a=1.15), ex, 1.11)
            cross = at(Dot(radius=0.055, color=CHALK_YELLOW, fill_opacity=1.0),
                       ex, 1.11)
            cross_note = at(board_text("it crosses itself here", 14, CHALK_WHITE,
                                       "BOLD"), ex, note_y)
            not_chip = at(chip("NOT SIMPLE", CHALK_PINK), ex, chip_y)

            banner = at(board_text("SIMPLE = DOES NOT CROSS ITSELF", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Simple means no crossing, not easy.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(oval_mob), run_time=0.65)
            self.play(FadeIn(simple_note, shift=UP * 0.05),
                      FadeIn(simple_chip, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(eight), run_time=0.65)
            self.play(FadeIn(cross, scale=0.8),
                      FadeIn(cross_note, shift=UP * 0.05),
                      FadeIn(not_chip, scale=0.9), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: two different questions ------------------------------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("Two Different Questions", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Open or closed?  Simple or not simple?", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # three equal cards, evenly spaced and centred on the board axis
            xs = row_centres((1.40, 1.40, 1.40), 0.30)
            ca = at(self.curve_card("OPEN + SIMPLE",
                                    open_wave(CHALK_CYAN, width=2.10, amp=0.40),
                                    CHALK_CYAN), xs[0], 0.45)
            cb = at(self.curve_card("CLOSED + SIMPLE",
                                    oval(CHALK_GREEN, w=1.50, h=1.10),
                                    CHALK_GREEN), xs[1], 0.45)
            cc = at(self.curve_card("CLOSED, NOT SIMPLE",
                                    figure_eight(CHALK_PINK, a=0.55),
                                    CHALK_PINK), xs[2], 0.45)

            banner = at(board_text("ASK BOTH QUESTIONS FOR EVERY CURVE", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Open or closed · simple or not simple.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(ca, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(cb, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(cc, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: a closed curve separates the plane -------------------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("A Closed Curve Separates the Plane", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Like the boundary wall of a park.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # the park wall is centred on the board axis; the BOUNDARY chip now
            # sits a clear 0.25 above the wall (it used to cut the oval's top)
            # and the traveller crosses the wall just under the EXTERIOR chip
            yc, w, h = 0.30, 3.20, 1.60
            wall = at(oval(CHALK_GREEN, w=w, h=h), BOARD_CX, yc)
            inside = at(interior_fill(w, h, CHALK_CYAN, 0.20), BOARD_CX, yc)
            boundary_chip = at(chip("BOUNDARY", CHALK_AMBER), BOARD_CX, 1.60)
            interior_chip = at(chip("INTERIOR", CHALK_CYAN), BOARD_CX, yc)
            exterior_chip = at(chip("EXTERIOR", CHALK_PINK), BOARD_CX + 2.80, yc)
            traveller = Dot(radius=0.06, color=CHALK_YELLOW, fill_opacity=1.0)
            traveller.move_to(np.array([BOARD_CX + 2.10, -0.35, 0.0]))

            banner = at(board_text("A CLOSED FIGURE SEPARATES THE PLANE", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Inside · On the wall · Outside.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(inside), Create(wall), run_time=0.70)
            self.play(FadeIn(boundary_chip, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(interior_chip, scale=0.9),
                      FadeIn(exterior_chip, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(traveller, scale=0.8), run_time=0.35)
            self.play(traveller.animate.move_to(
                np.array([BOARD_CX + 0.40, -0.35, 0.0])), run_time=1.1)
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: where is the point -----------------------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("Where Is the Point?", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Inside, on the edge, or outside?", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # the test oval is centred on the board axis, A sits well inside it,
            # B's letter 0.25 clear of the left vertex, C's letter 0.26 clear of
            # the right vertex, and the three result chips are one evenly
            # spaced, board-centred row
            yc, w, h = 0.75, 2.60, 1.50
            wall = at(oval(CHALK_GREEN, w=w, h=h), BOARD_CX, yc)
            inside = at(interior_fill(w, h, CHALK_CYAN, 0.18), BOARD_CX, yc)
            pa = dot_point("A", BOARD_CX, yc + 0.10, CHALK_CYAN, size=18,
                           label_dy=-0.34)
            pb = VGroup(Dot(radius=DOT_R, color=CHALK_AMBER,
                            fill_opacity=1.0).move_to(
                            np.array([BOARD_CX - w / 2.0, yc, 0.0])),
                        at(board_text("B", 18, CHALK_AMBER, "BOLD"),
                           BOARD_CX - w / 2.0 - 0.34, yc))
            pc = dot_point("C", BOARD_CX + w / 2.0 + 0.35, yc, CHALK_PINK,
                           size=18, label_dy=-0.34)

            chips = VGroup(chip("A · INTERIOR", CHALK_CYAN),
                           chip("B · BOUNDARY", CHALK_AMBER),
                           chip("C · EXTERIOR", CHALK_PINK))
            chips.arrange(RIGHT, buff=0.40).move_to(
                np.array([BOARD_CX, -0.60, 0.0]))
            chip_a, chip_b, chip_c = chips

            banner = at(board_text("INSIDE · ON THE EDGE · OUTSIDE", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Each point has exactly one place.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(inside), Create(wall), run_time=0.60)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(pa, scale=0.8), FadeIn(chip_a, scale=0.9),
                      run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(pb, scale=0.8), FadeIn(chip_b, scale=0.9),
                      run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(pc, scale=0.8), FadeIn(chip_c, scale=0.9),
                      run_time=0.45)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: what a region is -------------------------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("What Is a Region?", 20, CHALK_AMBER, "BOLD"),
                         BOARD_CX, ROW_Y)
            sub = at(board_text("The interior and the boundary together.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # the wall is paired with the right-hand REGION column, so the two
            # together are centred on the board axis (union -3.30..+4.30); the
            # BOUNDARY chip keeps 0.30 of air above the wall's top edge
            yc, w, h = 0.20, 3.00, 1.70
            wall = at(oval(CHALK_GREEN, w=w, h=h), -1.80, yc)
            inside = at(interior_fill(w, h, CHALK_CYAN, 0.20), -1.80, yc)
            interior_chip = at(chip("INTERIOR", CHALK_CYAN), -1.80, yc)
            boundary_chip = at(chip("BOUNDARY", CHALK_AMBER), -1.80, 1.60)
            region_chip = at(chip("REGION", CHALK_YELLOW, width=3.20, height=0.9),
                             2.70, 0.55)
            region_note = at(board_text("the whole closed part", 13, CHALK_WHITE,
                                        "BOLD"), 2.70, -0.32)

            banner = at(board_text("REGION = INTERIOR + BOUNDARY", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The edge is part of the region too.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(inside), Create(wall), run_time=0.60)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(interior_chip, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(boundary_chip, scale=0.9),
                      Indicate(wall, color=CHALK_AMBER, scale_factor=1.04),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(region_chip, scale=0.9),
                      FadeIn(region_note, shift=UP * 0.05), run_time=0.55)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: from a closed curve to a polygon ---------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("From a Closed Curve to a Polygon", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Make the boundary from straight line segments.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # oval + arrow + hexagon are one row, centred on the board axis,
            # with both names a clear 0.3 below their figure
            xs = row_centres((0.95, 0.70), 2.60)
            yc, lab_y = 0.85, -0.25
            oval_mob = at(oval(CHALK_GREEN, w=1.90, h=1.40), xs[0], yc)
            oval_lab = at(board_text("closed curve", 14, CHALK_WHITE, "BOLD"),
                          xs[0], lab_y)
            # a hexagon built from six straight segments
            pts = [np.array([0.70 * np.cos(a), 0.70 * np.sin(a), 0.0])
                   for a in np.linspace(np.pi / 6, 2 * np.pi + np.pi / 6, 7)]
            hexagon = Polygon(*pts, stroke_color=CHALK_CYAN, stroke_width=3.0)
            hexagon.move_to(np.array([xs[1], yc, 0.0]))
            poly_lab = at(board_text("polygon", 14, CHALK_WHITE, "BOLD"),
                          xs[1], lab_y)
            arrow = Arrow(np.array([xs[0] + 1.30, yc, 0.0]),
                          np.array([xs[1] - 1.05, yc, 0.0]), buff=0.15,
                          color=CHALK_AMBER, stroke_width=3.0,
                          tip_length=0.22)

            banner = at(board_text("A POLYGON IS A SIMPLE CLOSED FIGURE OF "
                                   "LINE SEGMENTS", 17, CHALK_YELLOW, "BOLD"),
                        BOARD_CX, BANNER_Y)
            strip = at(board_text("Triangles and quadrilaterals come next.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(oval_mob), FadeIn(oval_lab, shift=UP * 0.05),
                      run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(hexagon), FadeIn(poly_lab, shift=UP * 0.05),
                      run_time=0.60)
            self.play(Create(arrow), run_time=0.40)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
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
                         BOARD_CX, ROW_Y)
            sub = at(board_text("Classify each diagram, then locate P, Q and R.",
                                16, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # the four question cards are the series' corner grid about the
            # board axis (union -4.25..+5.25, centre 0.5), raised just enough
            # that no card's box dips into the caption band; the P/Q/R card
            # keeps 0.30 between its prompt and the mini figure (Q's letter sits
            # above the mini's top vertex, so 0.20 left them touching)
            qa = at(self.q_card("open or closed?",
                                open_wave(CHALK_CYAN, width=1.70, amp=0.30),
                                CHALK_CYAN), -2.75, 1.00)
            qb = at(self.q_card("open or closed?",
                                oval(CHALK_GREEN, w=1.30, h=0.90),
                                CHALK_GREEN), 3.75, 1.00)
            qc = at(self.q_card("simple or not simple?",
                                figure_eight(CHALK_PINK, a=0.42),
                                CHALK_PINK), -2.75, -0.95)
            qd = at(self.q_card("classify P, Q and R",
                                self.region_mini(CHALK_GREEN),
                                CHALK_AMBER, pad=0.14, buff=0.30), 3.75, -0.95)

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
            a1 = at(self.answer_row("A", "OPEN + SIMPLE",
                                    "two free ends, no crossing", CHALK_CYAN),
                    BOARD_CX, 1.62)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "CLOSED + SIMPLE", "a smooth oval",
                                    CHALK_GREEN), BOARD_CX, 0.82)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "NOT SIMPLE", "it crosses itself",
                                    CHALK_PINK), BOARD_CX, 0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "P interior · Q boundary · R exterior",
                                    "inside · on · outside", CHALK_AMBER),
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

            heading = at(board_text("Draw · Classify · Locate", 22, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)

            r1 = at(self.answer_row("1", "DOES IT CLOSE?", "open or closed",
                                    CHALK_CYAN, width=8.60, height=0.62),
                    BOARD_CX, 1.45)
            r2 = at(self.answer_row("2", "DOES IT CROSS ITSELF?",
                                    "simple or not simple", CHALK_GREEN,
                                    width=8.60, height=0.62), BOARD_CX, 0.55)
            r3 = at(self.answer_row("3", "WHERE IS THE POINT?",
                                    "interior · boundary · exterior",
                                    CHALK_AMBER, width=8.60, height=0.62),
                    BOARD_CX, -0.35)
            banner = at(board_text("REGION = INTERIOR + BOUNDARY", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Draw · Classify · Locate", 16, CHALK_WHITE,
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
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)

            # The closing paragraph is narrated in full before the board gives
            # way: the three rows and the rule line stay up through it, the
            # strip is written on its own bookmark as the voice says "Draw,
            # classify, locate.", and ONLY the bookmark in front of "Thank you
            # for watching," clears the board and brings in the card -- the old
            # cut cleared everything on b4, one phrase early, so the frame
            # jumped ahead of the voice.
            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeOut(heading), FadeOut(r1), FadeOut(r2), FadeOut(r3),
                      FadeOut(banner), FadeOut(strip), run_time=0.55)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.50)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.closing(tracker, thanks, run_time=1.2)
            self._capture_srt(tracker)

        self.wait(END_HOLD)

"""
Triangles Uncovered: Vertices, Sides, Angles, and Triangular Regions
Story-mode chalkboard lesson (Telangana Class 6 Maths, Chapter 4: Basic
Geometrical Ideas, Storymode 05).

LLM KEY / FUNCTION NAME: triangles_vertices_sides_and_triangular_region

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

The defining visual is THREE STICKS BECOME A TRIANGLE: one stick cannot close
anything, two sticks still leave the ends apart, and the third stick closes the
figure -- and that same triangle is then taken apart in layers (sides, vertices,
the angle at every corner, the three-letter name, the interior, the boundary and
the exterior, and finally the triangular region).

Title + 10 scenes:
  0. Title card: three sides, three vertices, three angles.
  1. How many sticks close a figure? One, two, three -- the ends meet.
  2. What is a triangle: simple, closed, three line segments.
  3. The three sides AB, BC, CA -- the boundary of the figure.
  4. The three vertices A, B, C -- corners, not sides.
  5. Three vertices give three angles: BAC, ABC, ACB.
  6. Naming the triangle: triangle ABC, BCA, CAB.
  7. Interior, boundary and exterior (points P, Q and R).
  8. The triangular region: interior together with the boundary.
  9. Your turn: name the sides, the vertices, the angle at Q, and sort X, Y and
     Z -- after the series' centred ten-second THINK clock.
 10. Recap: 3-3-3 plus the region, and the spoken thank-you card.
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


# (this section is spliced into a head whose own imports omit Arc, Sector and
#  Rotate; Dot, Line, Arrow, Circle, Polygon, VGroup and np are already there)
from manim import Arc, Rotate, Sector  # noqa: E402,F401

# Board layout shared by every scene of this video.
ROW_Y = 2.72             # every scene heading sits on this line
SUB_Y = 2.16             # the one-line sub-heading under it
BANNER_Y = -1.15         # the closing banner, above the strip
# The burned-in caption grows up from the bottom of the frame: a one-line cue
# starts at y = -3.38 and a wrapped two-line cue reaches y = -2.93 (measured on
# the burned caps), so every closing strip sits at -1.80 and nothing at all sits
# below CAPTION_SAFE_Y = -2.00 -- audited by the IN-CAPTION-BAND check.
STRIP_Y = -1.80
CAPTION_SAFE_Y = -2.00

PANEL_FILL = "#16202B"
SIDE_W = 4.4             # stroke width of a chalk side
STICK_W = 7.0            # stroke width of a matchstick
DOT_R = 0.082            # radius of a point dot
CORNER_R = 0.46          # radius of a corner's angle mark
MARK_SIZE = 18           # ONE letter size for every corner letter
LABEL_R = 0.40           # every corner letter sits this far out along the
                         # bisector of its own corner, in every scene
SIDE_LAB_R = 0.26        # every side name sits this far off its own line

# The persistent triangle A-B-C: a clean, well-proportioned SCALENE triangle
# (no two sides equal and no two angles equal -- the general case this lesson
# is about) whose ink is centred on the board axis:
#   base BC 3.00 wide on y = -0.45, apex A at (0.15, 1.30), height 1.75,
#   sides 2.09 / 2.65 / 3.00, angles 57 / 43 / 80 degrees.
#   A apex, B bottom-left, C bottom-right
TRI_A = (0.15, 1.30)
TRI_B = (-1.00, -0.45)
TRI_C = (2.00, -0.45)
TRI_CEN = (BOARD_CX, 0.425)          # the ink's bounding-box centre

# The right-hand column carries the labels of whatever the scene is naming.
# The figure is the diagram block and keeps the board's centre line; the column
# is its deliberate side label column, left-aligned just right of the figure's
# rightmost label (2.45) so every label starts on the same vertical line and
# none of them can reach the board's edge or run across the figure.
COL_L = 2.70
COL_W = 2.70             # the widest a column item may be
COL_ROWS = (1.20, 0.50, -0.20)
COL_NOTE_Y = -0.95


# ---------------------------------------------------------------- furniture --
def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


def at_left(mob, x, y):
    """Pin a mobject by its LEFT edge (and vertical centre).

    The right-hand column's labels are left-aligned on `COL_L`, so however wide
    a chip is, every one of them starts on the same vertical line -- and none of
    them can drift across the figure or off the green board.
    """
    mob.move_to(np.array([float(x) + mob.width / 2.0, float(y), 0.0]))
    return mob


def tri_pts(scale=1.0, cx=TRI_CEN[0], cy=TRI_CEN[1]):
    """The triangle's three vertices, scaled about the ink's own centre and
    moved so that centre sits at (cx, cy) -- so `cx=BOARD_CX` centres the figure
    on the board in every scene, at any size."""
    return [(cx + (p[0] - TRI_CEN[0]) * scale,
             cy + (p[1] - TRI_CEN[1]) * scale) for p in (TRI_A, TRI_B, TRI_C)]


def tri_centroid(pts):
    """The average of the three vertices (used to keep normals outward)."""
    return tuple(np.mean(np.array([[*p, 0.0] for p in pts], dtype=float),
                         axis=0)[:2])


def corner_label_dx(pts, i, r=LABEL_R):
    """The offset that puts corner `i`'s letter just outside its own corner.

    The letter goes `r` units along the bisector of the corner's interior
    angle, away from the figure -- the textbook place for a corner letter, and
    the same rule at every corner and in every scene, so A, B and C always look
    alike and none of them can sit on a side.
    """
    p = np.array(pts[i], dtype=float)
    q = np.array(pts[(i + 1) % 3], dtype=float)
    o = np.array(pts[(i - 1) % 3], dtype=float)
    u = (q - p) / np.linalg.norm(q - p)
    w = (o - p) / np.linalg.norm(o - p)
    b = u + w
    b = b / np.linalg.norm(b)
    return (-b[0] * r, -b[1] * r)


def side_label_pos(pts, i, r=SIDE_LAB_R):
    """Where side `i` (corner i -> corner i+1) has its name written.

    `r` units off the middle of the side, on the outside: so a side name can
    never land on its side, and every side name is the same distance out.
    """
    p = np.array(pts[i], dtype=float)
    q = np.array(pts[(i + 1) % 3], dtype=float)
    mid = (p + q) / 2.0
    d = (q - p) / np.linalg.norm(q - p)
    n = np.array([-d[1], d[0]])
    cen = np.array(tri_centroid(pts))
    if np.dot(n, cen - mid) > 0.0:
        n = -n
    out = mid + n * r
    return (float(out[0]), float(out[1]))


def tri_fill(pts, opacity=0.16, color=CHALK_CYAN):
    """The soft interior tint of the triangle."""
    return Polygon(np.array([pts[0][0], pts[0][1], 0.0]),
                   np.array([pts[1][0], pts[1][1], 0.0]),
                   np.array([pts[2][0], pts[2][1], 0.0]),
                   stroke_width=0, fill_color=color, fill_opacity=opacity)


def tri_side(p1, p2, color=CHALK_GREEN, width=SIDE_W):
    """One thick chalk side -- one of the three line segments."""
    return Line(np.array([float(p1[0]), float(p1[1]), 0.0]),
                np.array([float(p2[0]), float(p2[1]), 0.0]),
                stroke_color=color, stroke_width=width)


def match_stick(p1, p2, color=CHALK_AMBER, width=STICK_W):
    """The same segment as a matchstick: the stick plus its head."""
    line = tri_side(p1, p2, color, width)
    head = Dot(radius=0.085, color=CHALK_RED, fill_opacity=1.0)
    head.move_to(np.array([float(p2[0]), float(p2[1]), 0.0]))
    grp = VGroup(line, head)
    grp.line = line
    grp.head = head
    return grp


def corner_arc(vertex, p, q, radius=CORNER_R, color=CHALK_AMBER, width=2.8):
    """The angle mark in the corner at `vertex`, drawn between the two sides
    that run from it towards `p` and `q` (the shorter way round)."""
    v = np.array([float(vertex[0]), float(vertex[1]), 0.0])
    a1 = np.arctan2(p[1] - vertex[1], p[0] - vertex[0])
    a2 = np.arctan2(q[1] - vertex[1], q[0] - vertex[0])
    sweep = (a2 - a1 + np.pi) % (2.0 * np.pi) - np.pi
    return Arc(radius=radius, start_angle=a1, angle=sweep, arc_center=v,
               stroke_color=color, stroke_width=width)


def corner_wedge(vertex, p, q, radius=CORNER_R, color=CHALK_AMBER,
                 opacity=0.20):
    """The light fill of one corner's angle mark."""
    v = np.array([float(vertex[0]), float(vertex[1]), 0.0])
    a1 = np.arctan2(p[1] - vertex[1], p[0] - vertex[0])
    a2 = np.arctan2(q[1] - vertex[1], q[0] - vertex[0])
    sweep = (a2 - a1 + np.pi) % (2.0 * np.pi) - np.pi
    return Sector(radius=radius, start_angle=a1, angle=sweep, stroke_width=0,
                  fill_color=color, fill_opacity=opacity, arc_center=v)


def dot_point(name=None, x=0.0, y=0.0, color=CHALK_CYAN, size=MARK_SIZE,
              label_dx=(0.0, 0.0), r=DOT_R):
    """One chalk point with its letter beside it."""
    dot = Dot(radius=r, color=color, fill_opacity=1.0)
    dot.move_to(np.array([float(x), float(y), 0.0]))
    grp = VGroup(dot)
    if name:
        lab = board_text(name, size, color, "BOLD")
        lab.move_to(np.array([float(x) + label_dx[0], float(y) + label_dx[1],
                              0.0]))
        grp.add(lab)
        grp.label = lab
    grp.dot = dot
    return grp


def chip(text, color=CHALK_CYAN, size=15, width=None, height=0.46):
    """A small labelled chip."""
    lab = board_text(text, size, color, "BOLD")
    box = RoundedRectangle(corner_radius=0.09,
                           width=width or (lab.width + 0.40), height=height,
                           stroke_color=color, stroke_width=1.7,
                           fill_color=PANEL_FILL, fill_opacity=0.7)
    lab.move_to(box.get_center())
    return VGroup(box, lab)


def mark_yes(p, color=CHALK_GREEN, s=0.17):
    """A drawn tick (Segoe Print has no tick glyph)."""
    a = np.array([p[0] - s * 0.60, p[1] + s * 0.05, 0.0])
    b = np.array([p[0] - s * 0.05, p[1] - s * 0.55, 0.0])
    c = np.array([p[0] + s * 0.65, p[1] + s * 0.75, 0.0])
    return VGroup(Line(a, b, stroke_color=color, stroke_width=3.4),
                  Line(b, c, stroke_color=color, stroke_width=3.4))


def mark_no(p, color=CHALK_RED, s=0.17):
    """A drawn cross."""
    return VGroup(
        Line(np.array([p[0] - s * 0.6, p[1] - s * 0.6, 0.0]),
             np.array([p[0] + s * 0.6, p[1] + s * 0.6, 0.0]),
             stroke_color=color, stroke_width=3.4),
        Line(np.array([p[0] - s * 0.6, p[1] + s * 0.6, 0.0]),
             np.array([p[0] + s * 0.6, p[1] - s * 0.6, 0.0]),
             stroke_color=color, stroke_width=3.4))


# ----------------------------------------------------------------


NARRATION = {
    "title": (
        "A triangle has three sides, three vertices and three angles. <bookmark "
        "mark='b0'/>The three sides are line segments, and together they close "
        "the figure. <bookmark mark='b1'/>A triangle also separates the plane "
        "around it into an interior, a boundary and an exterior."
    ),
    "s1": (
        "How many sticks do we need to close a figure? <bookmark mark='b0'/>One "
        "stick cannot close anything: its two ends are far apart. <bookmark "
        "mark='b1'/>Two sticks make a V, and the two free ends are still open. "
        "<bookmark mark='b2'/>Add a third stick, and the ends meet. The figure "
        "closes. <bookmark mark='b3'/>So three is the least number of line "
        "segments needed to make a closed figure."
    ),
    "s2": (
        "The textbook calls this a triangle. <bookmark mark='b0'/>A triangle is "
        "a simple closed figure formed by three line segments. Simple, because "
        "the sides do not cross each other. <bookmark mark='b1'/>Closed, because "
        "the ends join up. <bookmark mark='b2'/>And exactly three line segments: "
        "no more, and no fewer."
    ),
    "s3": (
        "Now let us name the parts. <bookmark mark='b0'/>The three line segments "
        "are the sides of the triangle: side AB, <bookmark mark='b1'/>side BC, "
        "<bookmark mark='b2'/>and side CA. <bookmark mark='b3'/>The three sides "
        "together form the boundary of the triangle."
    ),
    "s4": (
        "The three points where the sides meet are the vertices. <bookmark "
        "mark='b0'/>Point A is one vertex, <bookmark mark='b1'/>point B is the "
        "second, <bookmark mark='b2'/>and point C is the third. <bookmark "
        "mark='b3'/>So a vertex is a corner of the triangle, and it is not the "
        "same as a side."
    ),
    "s5": (
        "At every vertex, the two sides of the triangle form an angle. <bookmark "
        "mark='b0'/>At vertex A we have angle BAC, <bookmark mark='b1'/>at "
        "vertex B we have angle ABC, <bookmark mark='b2'/>and at vertex C we "
        "have angle ACB. <bookmark mark='b3'/>So the three vertices give three "
        "angles."
    ),
    "s6": (
        "How do we name a triangle? <bookmark mark='b0'/>We use its three "
        "vertices. <bookmark mark='b1'/>Going around the figure in order, A then "
        "B then C, gives the name triangle ABC. <bookmark mark='b2'/>The same "
        "triangle can also be read as triangle BCA or triangle CAB."
    ),
    "s7": (
        "A triangle divides the plane around it into three parts. <bookmark "
        "mark='b0'/>Point P lies inside the triangle, so it is in the interior. "
        "<bookmark mark='b1'/>Point Q lies on one of the sides, so it is on the "
        "boundary. <bookmark mark='b2'/>Point R lies outside the triangle, so it "
        "is in the exterior."
    ),
    "s8": (
        "Now we can name the whole figure. <bookmark mark='b0'/>The boundary of "
        "the triangle together with its interior is called the triangular region. "
        "<bookmark mark='b1'/>So the region is not only the shaded inside: "
        "<bookmark mark='b2'/>it also includes the three sides themselves."
    ),
    "s9q": (
        "Your turn. Four quick checks. <bookmark mark='b0'/>First: name the three "
        "sides of triangle PQR. <bookmark mark='b1'/>Second: name its three "
        "vertices. <bookmark mark='b2'/>Third: name the angle at Q. <bookmark "
        "mark='b3'/>And last of all: point X, point Y and point Z. Which of them "
        "is in the interior, which is on the boundary, and which is in the "
        "exterior?"
    ),
    "s9a": (
        "<bookmark mark='b0'/>The three sides of triangle PQR are PQ, QR and RP. "
        "<bookmark mark='b1'/>Its three vertices are P, Q and R. <bookmark "
        "mark='b2'/>The angle at Q is angle PQR, because the vertex Q stays in "
        "the middle. <bookmark mark='b3'/>And point X is in the interior, point Y "
        "is on the boundary, and point Z is in the exterior."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>A triangle is a simple closed figure "
        "made from three line segments. <bookmark mark='b1'/>It has three sides, "
        "three vertices and three angles. <bookmark mark='b2'/>And its boundary "
        "together with its interior is the triangular region. <bookmark "
        "mark='b3'/>Build the triangle, identify its parts, <bookmark "
        "mark='b4'/>and locate the points. <bookmark mark='b5'/>Thank you for "
        "watching, <bookmark mark='b6'/>and see you in the next lesson."
    ),
}


class TrianglesVerticesSidesAndTriangularRegionStory(VoiceoverScene):
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
        out_dir = _HERE / "media" / "videos" / "triangles_vertices_sides_and_triangular_region"
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
    # Triangles (Class 6 Maths, Chapter 4, Storymode 05).
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
    #   * the persistent triangle A-B-C is fixed (TRI_A / TRI_B / TRI_C) so every
    #     scene draws exactly the same figure, and the three vertex letters are
    #     offset outward so no letter sits on a side;
    #   * the figure is the diagram block and stays centred on BOARD_CX, and the
    #     right-hand column (COL_L, left-aligned, capped at COL_W) carries
    #     whatever that scene is naming as its deliberate side label column;
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

    def figure(self, scale=1.0, cx=None, cy=None, fill_op=0.14,
               side_color=CHALK_GREEN, letters="ABC", dot_size=MARK_SIZE):
        """The persistent triangle, drawn as three thick chalk sides with a
        tinted interior and a solid dot plus an offset letter at each corner.

        Every corner letter is placed by the one rule (`corner_label_dx`: the
        same distance out along the corner's own outward bisector), so A, B and
        C look the same in every scene and none of them can sit on a side.
        """
        pts = tri_pts(scale, TRI_CEN[0] if cx is None else cx,
                      TRI_CEN[1] if cy is None else cy)
        a, b, c = pts
        grp = VGroup()
        fill = VGroup()
        if fill_op:
            fill = tri_fill(pts, fill_op)
            grp.add(fill)
        sides = VGroup(tri_side(a, b, side_color), tri_side(b, c, side_color),
                       tri_side(c, a, side_color))
        grp.add(sides)
        verts = VGroup()
        for i, (p, letter) in enumerate(zip(pts, letters)):
            if letter:
                dx, dy = corner_label_dx(pts, i)
                verts.add(dot_point(letter, p[0], p[1], CHALK_PINK,
                                    size=dot_size, label_dx=(dx, dy)))
        grp.add(verts)
        grp.fill = fill
        grp.sides = sides
        grp.verts = verts
        grp.points = pts
        return grp

    def col_item(self, head, note, color, y, x=COL_L, width=COL_W, height=0.92,
                 head_size=15, note_size=12):
        """One row of the right-hand column: a keyword and its note inside one
        card, spaced so no two words on the board come closer than 0.22 units.

        The card is capped to `COL_W` and left-aligned on `COL_L`, so the column
        never reaches across the figure's corner letters nor off the green board.
        """
        h = board_text(head, head_size, color, "BOLD")
        n = board_text(note, note_size, CHALK_WHITE, "BOLD")
        box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                               stroke_color=color, stroke_width=1.8,
                               fill_color=PANEL_FILL, fill_opacity=0.55)
        h.move_to(box.get_center() + UP * 0.26)
        n.move_to(box.get_center() + DOWN * 0.26)
        grp = VGroup(box, h, n)
        grp.box = box
        grp.head = h
        grp.note = n
        return at_left(grp, x, y)

    def q_card(self, title, pict, color=CHALK_CYAN, width=3.00, pad=0.12,
               title_size=13, buff=0.28):
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

    def mini_triangle(self, letters="PQR", color=CHALK_GREEN, arc=False,
                      points=()):
        """A small triangle for the challenge cards (centred on the origin).

        It is the SAME shape the lesson builds (A->P, B->Q, C->R), scaled to a
        card-sized thumbnail, and its corner letters use the same
        outward-bisector rule as the big figure, so no letter ever sits on a
        side and no dot ever lands inside a letter.  Pass `letters=""` for the
        card that carries the region points, so X, Y and Z have the whole
        thumbnail to themselves.
        """
        pts = [np.array([(x - TRI_CEN[0]) * 0.34, (y - TRI_CEN[1]) * 0.34, 0.0])
               for x, y in (TRI_A, TRI_B, TRI_C)]
        p, q, r = pts
        parts = [Polygon(p.copy(), q.copy(), r.copy(), stroke_color=color,
                         stroke_width=2.6, fill_color=CHALK_CYAN,
                         fill_opacity=0.16)]
        for i, (pt, letter) in enumerate(zip(pts, letters)):
            if letter:
                dx, dy = corner_label_dx(pts, i, 0.22)
                parts.append(dot_point(letter, pt[0], pt[1], CHALK_PINK,
                                       size=12, label_dx=(dx, dy), r=0.045))
        if arc:
            parts.append(corner_arc(q, p, r, 0.15, CHALK_AMBER, 2.0))
        # X inside, Y exactly on the base, Z out beyond side AB -- the same
        # three regions the lesson names, drawn on the same thumbnail shape.
        spots = {"in": ((-0.14, -0.14), (0.22, 0.0)),
                 "on": ((0.30, -0.298), (0.02, -0.21)),
                 "out": ((-0.549, 0.154), (-0.20, 0.06))}
        for name, kind in points:
            (px, py), (dx, dy) = spots[kind]
            col = {"in": CHALK_CYAN, "on": CHALK_AMBER,
                   "out": CHALK_PINK}[kind]
            parts.append(dot_point(name, px, py, col, size=10,
                                   label_dx=(dx, dy), r=0.045))
        return VGroup(*parts)

    # -- Scene 0: title ------------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = at(board_text("Triangles Uncovered", 26, CHALK_PINK,
                                  "BOLD"), BOARD_CX, 1.98)
            sub = at(board_text("Vertices · Sides · Angles · Triangular Region",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, 1.42)

            # the figure is the diagram block: centred on the board axis, with
            # the four counts left-aligned in its side label column at the right
            fig = self.figure(scale=0.72, cx=BOARD_CX, cy=-0.32, fill_op=0.16)
            c1 = at_left(chip("3 SIDES", CHALK_GREEN, size=14), COL_L, 0.88)
            c2 = at_left(chip("3 VERTICES", CHALK_PINK, size=14), COL_L, 0.16)
            c3 = at_left(chip("3 ANGLES", CHALK_AMBER, size=14), COL_L, -0.56)
            c4 = at_left(chip("interior · boundary · exterior", CHALK_CYAN,
                              size=12, width=COL_W), COL_L, -1.28)

            strip = at(board_text("Three sides, three vertices, three angles.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(title, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(fig.fill), Create(fig.sides), FadeIn(fig.verts),
                      run_time=0.85)
            self.play(FadeIn(c1, scale=0.9), FadeIn(c2, scale=0.9),
                      FadeIn(c3, scale=0.9), run_time=0.55)
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(c4, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.closing(tracker, c4)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: how many sticks close a figure -----------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("How Many Sticks Close a Figure?", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("One stick, two sticks, three sticks.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            a, b, c = tri_pts(0.86, BOARD_CX, -0.22)
            s1 = match_stick(a, b)
            s2 = match_stick(b, c)
            s3 = match_stick(c, a)
            fill = tri_fill((a, b, c), 0.16)

            k1 = at_left(chip("1 STICK · OPEN", CHALK_RED, size=14), COL_L, 1.15)
            k2 = at_left(chip("2 STICKS · OPEN", CHALK_RED, size=14), COL_L, 0.45)
            k3 = at_left(chip("3 STICKS · CLOSED", CHALK_GREEN, size=14), COL_L,
                         -0.25)

            banner = at(board_text("3 IS THE LEAST NUMBER OF SEGMENTS", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Three line segments are enough to close the "
                                  "figure.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(s1.line), FadeIn(s1.head), FadeIn(k1, scale=0.9),
                      run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(s2.line), FadeIn(s2.head), FadeIn(k2, scale=0.9),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Create(s3.line), FadeIn(s3.head), FadeIn(fill),
                      FadeIn(k3, scale=0.9), run_time=0.70)
            self.add_sound(self.sfx["success"], gain=-12)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: what is a triangle -----------------------------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("What Is a Triangle?", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Simple · closed · three line segments.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(scale=0.72, cx=BOARD_CX, cy=0.18, fill_op=0.14)

            i1 = self.col_item("SIMPLE", "the sides do not cross", CHALK_GREEN,
                               0.80)
            i2 = self.col_item("CLOSED", "the ends join up", CHALK_CYAN, -0.40)

            banner = at(board_text("3 LINE SEGMENTS = TRIANGLE", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("A simple closed figure formed by three line "
                                  "segments.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(fig.fill), Create(fig.sides), FadeIn(fig.verts),
                      run_time=0.70)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(i1, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(i2, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: the three sides --------------------------------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Three Sides", 20, CHALK_AMBER, "BOLD"),
                         BOARD_CX, ROW_Y)
            sub = at(board_text("The three line segments of the figure.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill_op=0.10)
            a, b, c = fig.points
            l_ab = at(board_text("AB", 17, CHALK_GREEN, "BOLD"),
                      *side_label_pos(fig.points, 0))
            l_bc = at(board_text("BC", 17, CHALK_GREEN, "BOLD"),
                      *side_label_pos(fig.points, 1))
            l_ca = at(board_text("CA", 17, CHALK_GREEN, "BOLD"),
                      *side_label_pos(fig.points, 2))

            k1 = at_left(chip("SIDE 1 · AB", CHALK_GREEN, size=14), COL_L,
                         COL_ROWS[0])
            k2 = at_left(chip("SIDE 2 · BC", CHALK_GREEN, size=14), COL_L,
                         COL_ROWS[1])
            k3 = at_left(chip("SIDE 3 · CA", CHALK_GREEN, size=14), COL_L,
                         COL_ROWS[2])
            note = at_left(board_text("the sides form the boundary", 12,
                                      CHALK_WHITE, "BOLD"), COL_L, COL_NOTE_Y)

            strip = at(board_text("The three sides together form the boundary.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(fig.fill), Create(fig.sides), FadeIn(fig.verts),
                      run_time=0.75)

            self.wait(leftover(tracker, "b0"))
            self.play(Indicate(fig.sides[0], color=CHALK_YELLOW, scale_factor=1.02),
                      FadeIn(l_ab, scale=0.9), FadeIn(k1, scale=0.9),
                      run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Indicate(fig.sides[1], color=CHALK_YELLOW, scale_factor=1.02),
                      FadeIn(l_bc, scale=0.9), FadeIn(k2, scale=0.9),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Indicate(fig.sides[2], color=CHALK_YELLOW, scale_factor=1.02),
                      FadeIn(l_ca, scale=0.9), FadeIn(k3, scale=0.9),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(Indicate(fig.sides, color=CHALK_GREEN, scale_factor=1.03),
                      FadeIn(note, shift=UP * 0.05),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: the three vertices -----------------------------------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Three Vertices", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The points where the sides meet.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill_op=0.10)
            k1 = at_left(chip("VERTEX A", CHALK_PINK, size=14), COL_L,
                         COL_ROWS[0])
            k2 = at_left(chip("VERTEX B", CHALK_PINK, size=14), COL_L,
                         COL_ROWS[1])
            k3 = at_left(chip("VERTEX C", CHALK_PINK, size=14), COL_L,
                         COL_ROWS[2])
            note = at_left(board_text("a corner, not a side", 12, CHALK_WHITE,
                                      "BOLD"), COL_L, COL_NOTE_Y)

            strip = at(board_text("A vertex is a corner of the triangle.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(fig.fill), Create(fig.sides), run_time=0.60)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(fig.verts[0], scale=0.85), FadeIn(k1, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(fig.verts[1], scale=0.85), FadeIn(k2, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(fig.verts[2], scale=0.85), FadeIn(k3, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(Indicate(fig.verts, color=CHALK_PINK, scale_factor=1.15),
                      FadeIn(note, shift=UP * 0.05),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: three vertices give three angles ---------------------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("Three Vertices, Three Angles", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Every vertex gives an angle.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill_op=0.10)
            a, b, c = fig.points
            arc_a = corner_arc(a, b, c, CORNER_R, CHALK_GREEN, 3.0)
            arc_b = corner_arc(b, a, c, CORNER_R, CHALK_CYAN, 3.0)
            arc_c = corner_arc(c, a, b, CORNER_R, CHALK_PINK, 3.0)

            def angle_row(pre, tex, color, y):
                p = board_text(pre, 15, color, "BOLD")
                m = chalk_math(tex, size=24, color=color)
                return at_left(VGroup(p, m).arrange(RIGHT, buff=0.26), COL_L, y)

            r1 = angle_row("at A", r"\angle BAC", CHALK_GREEN, 1.25)
            r2 = angle_row("at B", r"\angle ABC", CHALK_CYAN, 0.45)
            r3 = angle_row("at C", r"\angle ACB", CHALK_PINK, -0.35)
            note = at_left(board_text("the vertex is the middle letter", 12,
                                      CHALK_WHITE, "BOLD"), COL_L, -1.05)

            strip = at(board_text("Three vertices give three angles.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(fig.fill), Create(fig.sides), FadeIn(fig.verts),
                      run_time=0.70)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(arc_a), FadeIn(r1, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(arc_b), FadeIn(r2, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Create(arc_c), FadeIn(r3, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(Indicate(VGroup(arc_a, arc_b, arc_c), color=CHALK_YELLOW,
                               scale_factor=1.04),
                      FadeIn(note, shift=UP * 0.05),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: naming the triangle ----------------------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("Naming the Triangle", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("We use its three vertices.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill_op=0.14)
            name = at_left(chalk_math(r"\triangle ABC", size=38,
                                      color=CHALK_YELLOW), COL_L, 0.95)
            n1 = at_left(board_text("the vertices in order", 12, CHALK_WHITE,
                                    "BOLD"), COL_L, 0.20)
            n2 = at_left(board_text("BCA and CAB name it too", 12, CHALK_WHITE,
                                    "BOLD"), COL_L, -0.55)

            strip = at(board_text("Name a triangle by its three vertices, in "
                                  "order.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(fig.fill), Create(fig.sides), FadeIn(fig.verts),
                      run_time=0.75)

            self.wait(leftover(tracker, "b0"))
            self.play(Indicate(fig.verts, color=CHALK_PINK, scale_factor=1.12),
                      run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Indicate(fig.sides[0], color=CHALK_YELLOW, scale_factor=1.02),
                      run_time=0.24)
            self.play(Indicate(fig.sides[1], color=CHALK_YELLOW, scale_factor=1.02),
                      run_time=0.24)
            self.play(Indicate(fig.sides[2], color=CHALK_YELLOW, scale_factor=1.02),
                      run_time=0.24)
            self.play(FadeIn(name, scale=0.9), FadeIn(n1, shift=UP * 0.05),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(n2, shift=UP * 0.05),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: interior, boundary, exterior -------------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Interior, Boundary, Exterior", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A triangle divides the plane into three parts.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill_op=0.18)
            # P sits in the open interior, Q exactly ON the base (its letter
            # just below the base, in the air under the figure), and R outside
            # to the upper left, across side AB -- so the three points are far
            # apart and each one's region reads at a glance.  (The old cut put
            # them all in the right-hand half, where the column sits.)
            p_pt = dot_point("P", 0.30, 0.30, CHALK_CYAN, size=MARK_SIZE,
                             label_dx=(0.22, 0.16))
            q_pt = dot_point("Q", 0.60, -0.45, CHALK_AMBER, size=MARK_SIZE,
                             label_dx=(0.0, -0.31))
            r_pt = dot_point("R", -0.885, 0.727, CHALK_PINK, size=MARK_SIZE,
                             label_dx=(-0.24, 0.20))

            k1 = at_left(chip("P · INTERIOR", CHALK_CYAN, size=14), COL_L,
                         COL_ROWS[0])
            k2 = at_left(chip("Q · BOUNDARY", CHALK_AMBER, size=14), COL_L,
                         COL_ROWS[1])
            k3 = at_left(chip("R · EXTERIOR", CHALK_PINK, size=14), COL_L,
                         COL_ROWS[2])
            note = at_left(board_text("inside · on a side · outside", 12,
                                      CHALK_WHITE, "BOLD"), COL_L, COL_NOTE_Y)

            strip = at(board_text("Three parts of the plane: interior, boundary, "
                                  "exterior.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(fig.fill), Create(fig.sides), FadeIn(fig.verts),
                      run_time=0.70)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(p_pt, scale=0.85), FadeIn(k1, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(q_pt, scale=0.85), FadeIn(k2, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(r_pt, scale=0.85), FadeIn(k3, scale=0.9),
                      run_time=0.50)
            self.play(FadeIn(note, shift=UP * 0.05),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the triangular region --------------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Triangular Region", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The interior together with the boundary.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill_op=0.22)
            a, b, c = fig.points
            glow = VGroup(tri_side(a, b, CHALK_YELLOW, 7.5),
                          tri_side(b, c, CHALK_YELLOW, 7.5),
                          tri_side(c, a, CHALK_YELLOW, 7.5))

            k1 = at_left(chip("INTERIOR", CHALK_CYAN, size=14), COL_L, 1.15)
            k2 = at_left(chip("+ BOUNDARY", CHALK_GREEN, size=14), COL_L, 0.45)
            k3 = at_left(chip("= THE REGION", CHALK_YELLOW, size=14), COL_L,
                         -0.35)
            note = at_left(board_text("the region includes the sides", 12,
                                      CHALK_WHITE, "BOLD"), COL_L, -1.05)

            strip = at(board_text("The region is the interior plus the boundary.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(fig.sides), FadeIn(fig.verts), run_time=0.60)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(fig.fill), FadeIn(k1, scale=0.9), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(glow), FadeIn(k2, scale=0.9), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Indicate(VGroup(fig.fill, glow), color=CHALK_YELLOW,
                               scale_factor=1.03),
                      FadeIn(k3, scale=0.9), FadeIn(note, shift=UP * 0.05),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.65)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, k3)
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

            qa = at(self.q_card("name the sides",
                                self.mini_triangle("PQR", CHALK_GREEN),
                                CHALK_GREEN), -2.80, 0.92)
            qb = at(self.q_card("name the vertices",
                                self.mini_triangle("PQR", CHALK_CYAN),
                                CHALK_CYAN), 3.70, 0.92)
            qc = at(self.q_card("name the angle at Q",
                                self.mini_triangle("PQR", CHALK_AMBER, arc=True),
                                CHALK_AMBER), -2.80, -1.02)
            qd = at(self.q_card("X, Y, Z belong where?",
                                self.mini_triangle("", CHALK_PINK,
                                                   points=(("X", "in"),
                                                           ("Y", "on"),
                                                           ("Z", "out"))),
                                CHALK_PINK), 3.70, -1.02)

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
            a1 = at(self.answer_row("A", "PQ · QR · RP",
                                    "the three line segments", CHALK_GREEN),
                    BOARD_CX, 1.62)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "P · Q · R", "the three corners",
                                    CHALK_CYAN), BOARD_CX, 0.82)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "angle PQR", "Q stays in the middle",
                                    CHALK_AMBER), BOARD_CX, 0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "X · Y · Z sorted",
                                    "interior · boundary · exterior",
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

            heading = at(board_text("Build · Identify · Locate", 22, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)

            r1 = at(self.answer_row("1", "3 SIDES · 3 VERTICES · 3 ANGLES",
                                    "the parts of a triangle", CHALK_GREEN),
                    BOARD_CX, 1.48)
            r2 = at(self.answer_row("2", "THREE LINE SEGMENTS",
                                    "simple and closed", CHALK_CYAN),
                    BOARD_CX, 0.72)
            r3 = at(self.answer_row("3", "TRIANGULAR REGION",
                                    "interior together with the boundary",
                                    CHALK_YELLOW), BOARD_CX, -0.04)
            r4 = at(self.answer_row("4", "BUILD · IDENTIFY · LOCATE",
                                    "name it, then sort the points",
                                    CHALK_AMBER), BOARD_CX, -0.80)
            strip = at(board_text("Build it, identify its parts, then locate the "
                                  "points.", 16, CHALK_WHITE, "BOLD"),
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
            # the strip is written on its own bookmark as the voice says "and
            # locate the points.", and only the bookmark in front of "Thank you
            # for watching," clears the board and brings in the card.  (The old
            # cut brought the strip on one bookmark early, with r4, and then
            # cleared everything on the next one, so the frame ran ahead of the
            # voice.)
            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeOut(heading), FadeOut(r1), FadeOut(r2), FadeOut(r3),
                      FadeOut(r4), FadeOut(strip), run_time=0.55)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.50)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            # 0.90 rather than 1.20: this piece's own audio runs the closing
            # sentence a little slower than the draft SRT assumes, and this
            # keeps every piece at 0.00 s stretch
            self.closing(tracker, thanks, run_time=0.90)
            self._capture_srt(tracker)

        self.wait(END_HOLD)

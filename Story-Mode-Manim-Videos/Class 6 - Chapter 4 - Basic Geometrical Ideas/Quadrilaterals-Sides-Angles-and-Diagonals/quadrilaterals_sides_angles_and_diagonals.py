"""
Exploring Quadrilaterals: Sides, Angles, Diagonals, and Opposite vs. Adjacent
Elements
Story-mode chalkboard lesson (Telangana Class 6 Maths, Chapter 4: Basic
Geometrical Ideas, Storymode 06).

LLM KEY / FUNCTION NAME: quadrilaterals_sides_angles_and_diagonals

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

The defining visual is ONE PERSISTENT QUADRILATERAL used as a relationship map:
the boundary is built segment by segment, then each idea is revealed by changing
only the emphasis -- the sides traced, the corners pulsed, an arc drawn at every
corner, two adjacent sides brought together on their shared vertex, two opposite
sides shown across the shape, and finally the opposite vertices joined by the two
dashed diagonals.

Title + 10 scenes:
  0. Title card: four sides, four vertices, four angles, two diagonals.
  1. From triangle to quadrilateral: the third side opens into two.
  2. The definition: simple, closed, four line segments.
  3. The four sides and the four vertices.
  4. Four corners give four angles.
  5. Adjacent: the neighbours that share a vertex.
  6. Opposite: the elements across the shape, sides and angles.
  7. Diagonals: joining the opposite vertices.
  8. The relationship map: adjacent, opposite, diagonal.
  9. Your turn: opposite side, opposite angle, adjacent sides, the diagonals --
     after the series' centred ten-second THINK clock.
 10. Recap: 4-4-4-2 plus adjacent/opposite, and the spoken thank-you card.
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


# (this section is spliced into a head whose own imports omit Arc and Sector;
#  Dot, Line, DashedLine, Arrow, Circle, Polygon, VGroup and np are there)
from manim import Arc, Sector  # noqa: E402,F401

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
DIAG_W = 3.2             # stroke width of a diagonal
DOT_R = 0.084            # radius of a point dot
CORNER_R = 0.42          # radius of a corner's angle mark
MARK_SIZE = 18           # ONE letter size for every corner letter
LABEL_R = 0.40           # every corner letter sits this far out along the
                         # bisector of its own corner, in every scene
SIDE_LAB_R = 0.30        # every side name sits this far off its own line

# The persistent quadrilateral A-B-C-D, in order round the boundary.  It is a
# general convex quadrilateral -- deliberately NOT a special one (no pair of
# sides parallel, no two angles equal), because this section is about the
# general structure -- but it is drawn clean and well proportioned: a 3.05 x
# 1.77 figure whose ink is centred on the board axis.
#   A top-left, B top-right, C bottom-right, D bottom-left
QUAD_CEN = (BOARD_CX, 0.51)          # the ink's bounding-box centre
QUAD_LOCAL = ((-1.525, 0.885), (1.325, 0.615),
              (1.525, -0.855), (-1.175, -0.885))

# The right-hand column carries the labels of whatever the scene is naming.
# The figure is the diagram block and keeps the board's centre line; the column
# is its deliberate side label column, left-aligned just right of the figure's
# rightmost corner letter (2.41) so every label starts on the same vertical
# line and none of them can reach the board's edge or run across the figure.
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


def quad_pts(scale=1.0, cx=QUAD_CEN[0], cy=QUAD_CEN[1]):
    """The quadrilateral's four vertices, scaled and moved as one figure.

    `QUAD_LOCAL` is already centred on its own bounding box, so passing
    `cx=BOARD_CX` centres the figure's ink on the board axis -- which is what
    every scene does, so the same quadrilateral is centred in every frame.
    """
    return [(cx + p[0] * scale, cy + p[1] * scale) for p in QUAD_LOCAL]


def quad_centroid(pts):
    """The average of the four vertices (used to keep normals outward)."""
    return tuple(np.mean(np.array([[*p, 0.0] for p in pts], dtype=float),
                         axis=0)[:2])


def corner_label_dx(pts, i, r=LABEL_R):
    """The offset that puts corner `i`'s letter just outside its own corner.

    The letter goes `r` units along the bisector of the corner's interior
    angle, away from the figure -- the textbook place for a corner letter.
    Using the same rule at every corner and in every scene is what makes the
    four letters look alike (the old offsets were four hand-picked pairs of
    different direction, so A, B, C and D each sat a different way).
    """
    p = np.array(pts[i], dtype=float)
    q = np.array(pts[(i + 1) % 4], dtype=float)
    o = np.array(pts[(i - 1) % 4], dtype=float)
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
    q = np.array(pts[(i + 1) % 4], dtype=float)
    mid = (p + q) / 2.0
    d = (q - p) / np.linalg.norm(q - p)
    n = np.array([-d[1], d[0]])
    cen = np.array(quad_centroid(pts))
    if np.dot(n, cen - mid) > 0.0:
        n = -n
    out = mid + n * r
    return (float(out[0]), float(out[1]))


def quad_fill(pts, opacity=0.14, color=CHALK_CYAN):
    """The soft interior tint of the quadrilateral."""
    return Polygon(*[np.array([p[0], p[1], 0.0]) for p in pts],
                   stroke_width=0, fill_color=color, fill_opacity=opacity)


def quad_side(p1, p2, color=CHALK_GREEN, width=SIDE_W):
    """One thick chalk side -- one of the four line segments."""
    return Line(np.array([float(p1[0]), float(p1[1]), 0.0]),
                np.array([float(p2[0]), float(p2[1]), 0.0]),
                stroke_color=color, stroke_width=width)


def diag(p1, p2, color=CHALK_YELLOW, width=DIAG_W, dash=0.16):
    """One dashed diagonal: the convention for a segment across the inside."""
    return DashedLine(np.array([float(p1[0]), float(p1[1]), 0.0]),
                      np.array([float(p2[0]), float(p2[1]), 0.0]),
                      color=color, stroke_color=color, stroke_width=width,
                      dash_length=dash)


def corner_arc(vertex, p, q, radius=CORNER_R, color=CHALK_AMBER, width=2.8):
    """The angle mark in the corner at `vertex`, drawn between the two sides
    that run from it towards `p` and `q` (the shorter way round)."""
    v = np.array([float(vertex[0]), float(vertex[1]), 0.0])
    a1 = np.arctan2(p[1] - vertex[1], p[0] - vertex[0])
    a2 = np.arctan2(q[1] - vertex[1], q[0] - vertex[0])
    sweep = (a2 - a1 + np.pi) % (2.0 * np.pi) - np.pi
    return Arc(radius=radius, start_angle=a1, angle=sweep, arc_center=v,
               stroke_color=color, stroke_width=width)


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
        "A quadrilateral is a simple closed polygon with four sides. <bookmark "
        "mark='b0'/>It has four vertices and four angles, <bookmark "
        "mark='b1'/>and it also has two diagonals."
    ),
    "s1": (
        "In the last lesson we closed a figure with three line segments: a "
        "triangle. <bookmark mark='b0'/>What happens if we add one more corner? "
        "<bookmark mark='b1'/>Watch the side CA. It opens out into two new "
        "sides, CD and DA, and the figure closes again. <bookmark mark='b2'/>Now "
        "the figure has four sides, so it is a quadrilateral."
    ),
    "s2": (
        "Let us build it segment by segment. <bookmark mark='b0'/>Here is side "
        "AB. <bookmark mark='b1'/>Attach side BC. <bookmark mark='b2'/>Attach "
        "side CD: the figure is still open. <bookmark mark='b3'/>Attach side DA, "
        "and the ends meet. The figure closes. <bookmark mark='b4'/>Simple, "
        "because the sides do not cross; closed, because the ends join up; and "
        "four sides. That is a quadrilateral, and like every closed figure it "
        "has an interior, a boundary and an exterior."
    ),
    "s3": (
        "The four line segments are the sides: side AB, <bookmark mark='b0'/>"
        "side BC, <bookmark mark='b1'/>side CD, <bookmark mark='b2'/>and side "
        "DA, which brings us back to A. <bookmark mark='b3'/>The four points A, "
        "B, C and D are its vertices. <bookmark mark='b4'/>So the sides form the "
        "boundary, <bookmark mark='b5'/>and the vertices are the corners where "
        "two sides meet."
    ),
    "s4": (
        "At every vertex, the two sides form an angle. <bookmark mark='b0'/>At "
        "corner A we have angle A, <bookmark mark='b1'/>at corner B angle B, "
        "<bookmark mark='b2'/>at corner C angle C, <bookmark mark='b3'/>and at "
        "corner D angle D. <bookmark mark='b4'/>So four vertices give four "
        "angles."
    ),
    "s5": (
        "Now compare the sides. <bookmark mark='b0'/>Side AB and side BC meet at "
        "the vertex B, so they are adjacent. <bookmark mark='b1'/>Side AB and "
        "side DA meet at the vertex A, so they are adjacent as well. <bookmark "
        "mark='b2'/>Adjacent sides always share a vertex."
    ),
    "s6": (
        "Some elements are across from each other instead. <bookmark "
        "mark='b0'/>Side AB and side CD do not meet at all, so they are opposite "
        "sides. <bookmark mark='b1'/>Side BC and side DA are the other pair of "
        "opposite sides. <bookmark mark='b2'/>Angles have opposites too: angle A "
        "is opposite angle C, and angle B is opposite angle D. <bookmark "
        "mark='b3'/>So adjacent means next to, and opposite means across."
    ),
    "s7": (
        "Now join the opposite vertices. <bookmark mark='b0'/>The vertices A and "
        "C are opposite, and joining them gives the segment AC. <bookmark "
        "mark='b1'/>The vertices B and D are opposite, and joining them gives the "
        "segment BD. <bookmark mark='b2'/>These two segments are the diagonals "
        "of the quadrilateral: a diagonal joins two opposite vertices."
    ),
    "s8": (
        "Let us put the whole relationship map together. <bookmark "
        "mark='b0'/>Adjacent elements share a corner: AB and BC share the vertex "
        "B. <bookmark mark='b1'/>Opposite elements lie across the shape: AB and "
        "CD share no vertex. <bookmark mark='b2'/>And a diagonal connects the "
        "opposite corners: AC joins A and C. <bookmark mark='b3'/>So ask "
        "yourself: are they next to each other, across from each other, or "
        "joined across?"
    ),
    "s9q": (
        "Your turn. Four quick checks on quadrilateral PQRS. <bookmark "
        "mark='b0'/>First: which side is opposite QR? <bookmark mark='b1'/>"
        "Second: which angle is opposite angle P? <bookmark mark='b2'/>Third: "
        "which sides are adjacent to PQ? <bookmark mark='b3'/>And last of all: "
        "join the opposite vertices, and name the two diagonals."
    ),
    "s9a": (
        "<bookmark mark='b0'/>The side opposite QR is PS. <bookmark "
        "mark='b1'/>The angle opposite angle P is angle R. <bookmark "
        "mark='b2'/>The sides adjacent to PQ are PS and QR, because each of them "
        "shares a vertex with PQ. <bookmark mark='b3'/>And the two diagonals are "
        "PR and QS: they join the opposite vertices P with R, and Q with S."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>A quadrilateral is a simple closed "
        "polygon with four sides, <bookmark mark='b1'/>four vertices and four "
        "angles. <bookmark mark='b2'/>Adjacent elements are next to each other, "
        "and opposite elements are across the shape. <bookmark mark='b3'/>And "
        "its two diagonals join the opposite vertices. <bookmark mark='b4'/>"
        "Build it, compare its parts, and connect the corners. <bookmark "
        "mark='b5'/>Thank you for watching, <bookmark mark='b6'/>and see you in "
        "the next lesson."
    ),
}


class QuadrilateralsSidesAnglesAndDiagonalsStory(VoiceoverScene):
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
        out_dir = _HERE / "media" / "videos" / "quadrilaterals_sides_angles_and_diagonals"
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
    # Quadrilaterals (Class 6 Maths, Chapter 4, Storymode 06).
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
    #   * the persistent quadrilateral A-B-C-D is fixed (QUAD_A .. QUAD_D) so
    #     every scene draws exactly the same figure, and the four vertex letters
    #     are offset outward so no letter sits on a side;
    #   * the figure occupies the left two thirds and the right-hand column
    #     (COL_L, left-aligned) carries whatever that scene is naming, so nothing
    #     has to be written across the boundary;
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
               side_color=CHALK_GREEN, letters="ABCD", dot_size=MARK_SIZE):
        """The persistent quadrilateral, drawn as four thick chalk sides with a
        tinted interior and a solid dot plus an offset letter at each corner.

        Every corner letter is placed by the one rule (`corner_label_dx`: the
        same distance out along the corner's own outward bisector), so A, B, C
        and D look the same in every scene and none of them can sit on a side.
        """
        pts = quad_pts(scale, QUAD_CEN[0] if cx is None else cx,
                       QUAD_CEN[1] if cy is None else cy)
        a, b, c, d = pts
        grp = VGroup()
        fill = VGroup()
        if fill_op:
            fill = quad_fill(pts, fill_op)
            grp.add(fill)
        sides = VGroup(quad_side(a, b, side_color), quad_side(b, c, side_color),
                       quad_side(c, d, side_color), quad_side(d, a, side_color))
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

        The card is capped to `COL_W` so the column never reaches across the
        figure's corner letters nor off the green board.
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

    def mini_quad(self, letters="PQRS", color=CHALK_GREEN, arc=None,
                  diags=False):
        """A small quadrilateral for the challenge cards (centred on the
        origin): four sides, a solid dot and an offset letter at each corner,
        optionally the angle mark at P or the two dashed diagonals.

        It is the SAME shape the lesson builds (A->P, B->Q, C->R, D->S),
        scaled to a card-sized thumbnail, and its letters use the same
        outward-bisector rule as the big figure, scaled with it, so no letter
        ever sits on a side and no dot ever lands inside a letter.
        """
        pts = [np.array([x * 0.34, y * 0.34, 0.0]) for x, y in QUAD_LOCAL]
        p, q, r, s = pts
        parts = [Polygon(*[pt.copy() for pt in pts],
                         stroke_color=color, stroke_width=2.6,
                         fill_color=CHALK_CYAN, fill_opacity=0.16)]
        for i, (pt, letter) in enumerate(zip(pts, letters)):
            if letter:
                dx, dy = corner_label_dx(pts, i, 0.22)
                parts.append(dot_point(letter, pt[0], pt[1], CHALK_PINK,
                                       size=12, label_dx=(dx, dy), r=0.045))
        if arc == "P":
            parts.append(corner_arc(p, q, s, 0.13, CHALK_AMBER, 2.0))
        if diags:
            parts.append(diag(p, r, CHALK_YELLOW, 2.0, dash=0.08))
            parts.append(diag(q, s, CHALK_PINK, 2.0, dash=0.08))
        return VGroup(*parts)

    # -- Scene 0: title ------------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = at(board_text("Exploring Quadrilaterals", 25, CHALK_PINK,
                                  "BOLD"), BOARD_CX, 2.06)
            sub = at(board_text("Sides · Vertices · Angles · Diagonals", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, 1.42)

            # the figure is the diagram block: centred on the board axis, with
            # the four counts in its side label column at the right
            fig = self.figure(scale=0.72, cx=BOARD_CX, cy=-0.25, fill_op=0.16)
            a, b, c, d = fig.points
            diag1 = diag(a, c)
            diag2 = diag(b, d)

            # the four counts, left-aligned in the figure's side label column
            c1 = at_left(chip("4 SIDES", CHALK_GREEN, size=14), COL_L, 0.88)
            c2 = at_left(chip("4 VERTICES", CHALK_PINK, size=14), COL_L, 0.16)
            c3 = at_left(chip("4 ANGLES", CHALK_AMBER, size=14), COL_L, -0.56)
            c4 = at_left(chip("2 DIAGONALS", CHALK_YELLOW, size=14), COL_L,
                         -1.28)

            strip = at(board_text("A simple closed polygon with four sides.",
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
            self.play(FadeIn(diag1), FadeIn(diag2), FadeIn(c4, scale=0.9),
                      run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.closing(tracker, c4)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: from a triangle to a quadrilateral -------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            # On-screen heading only -- the narration is untouched.  The old
            # "What Happens When We Add a Fourth Corner?" was 6.68 wide and ran
            # straight into the top-right "Mathematics" badge (badge x
            # [+3.79..+5.59] y [+2.82..+3.22], heading right edge +3.84, i.e.
            # the boxes actually overlapped).  This keeps the meaning on the
            # same heading line, size, colour and weight, and clears both
            # badges by more than a unit.
            heading = at(board_text("Adding a Fourth Corner", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A triangle grows one more side.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            a, b, c, d = quad_pts()
            t_ab = quad_side(a, b, CHALK_AMBER, 5.0)
            t_bc = quad_side(b, c, CHALK_AMBER, 5.0)
            t_ca = quad_side(c, a, CHALK_AMBER, 5.0)
            va = dot_point("A", a[0], a[1], CHALK_PINK, size=MARK_SIZE,
                           label_dx=corner_label_dx((a, b, c, d), 0))
            vb = dot_point("B", b[0], b[1], CHALK_PINK, size=MARK_SIZE,
                           label_dx=corner_label_dx((a, b, c, d), 1))
            vc = dot_point("C", c[0], c[1], CHALK_PINK, size=MARK_SIZE,
                           label_dx=corner_label_dx((a, b, c, d), 2))
            vd = dot_point("D", d[0], d[1], CHALK_PINK, size=MARK_SIZE,
                           label_dx=corner_label_dx((a, b, c, d), 3))
            s_cd = quad_side(c, d, CHALK_GREEN)
            s_da = quad_side(d, a, CHALK_GREEN)
            g_ab = quad_side(a, b, CHALK_GREEN)
            g_bc = quad_side(b, c, CHALK_GREEN)
            fill = quad_fill((a, b, c, d), 0.16)

            k1 = at_left(chip("3 SIDES · TRIANGLE", CHALK_AMBER, size=12),
                         COL_L, 0.85)
            k2 = at_left(chip("4 SIDES · QUADRILATERAL", CHALK_GREEN, size=12),
                         COL_L, 0.15)

            banner = at(board_text("THE THIRD SIDE OPENS IN TWO", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Adding a fourth corner gives a quadrilateral.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(t_ab), Create(t_bc), Create(t_ca), FadeIn(va),
                      FadeIn(vb), FadeIn(vc), run_time=0.75)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(k1, scale=0.9), run_time=0.40)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(vd, scale=0.85), run_time=0.45)
            self.play(Indicate(vd, color=CHALK_PINK, scale_factor=1.30),
                      run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeOut(t_ca), FadeOut(t_ab), FadeOut(t_bc),
                      Create(s_cd), Create(s_da), Create(g_ab), Create(g_bc),
                      FadeIn(fill), run_time=0.85)
            self.play(FadeIn(k2, scale=0.9),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-12)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: the definition, built segment by segment -------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("What Makes It a Quadrilateral?", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Simple · closed · four line segments.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            a, b, c, d = quad_pts()
            s_ab = quad_side(a, b)
            s_bc = quad_side(b, c)
            s_cd = quad_side(c, d)
            s_da = quad_side(d, a)
            fill = quad_fill((a, b, c, d), 0.16)
            va = dot_point("A", a[0], a[1], CHALK_PINK, size=MARK_SIZE,
                           label_dx=corner_label_dx((a, b, c, d), 0))
            vb = dot_point("B", b[0], b[1], CHALK_PINK, size=MARK_SIZE,
                           label_dx=corner_label_dx((a, b, c, d), 1))
            vc = dot_point("C", c[0], c[1], CHALK_PINK, size=MARK_SIZE,
                           label_dx=corner_label_dx((a, b, c, d), 2))
            vd = dot_point("D", d[0], d[1], CHALK_PINK, size=MARK_SIZE,
                           label_dx=corner_label_dx((a, b, c, d), 3))

            k1 = at_left(chip("SIDE 1 · AB", CHALK_GREEN, size=14), COL_L, 1.42)
            k2 = at_left(chip("SIDE 2 · BC", CHALK_GREEN, size=14), COL_L, 0.78)
            k3 = at_left(chip("SIDE 3 · CD", CHALK_GREEN, size=14), COL_L, 0.14)
            k4 = at_left(chip("SIDE 4 · DA", CHALK_GREEN, size=14), COL_L,
                         -0.50)

            banner = at(board_text("4 SEGMENTS = QUADRILATERAL", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Simple, closed, and made of four line "
                                  "segments.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(s_ab), FadeIn(va), FadeIn(vb), FadeIn(k1, scale=0.9),
                      run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(s_bc), FadeIn(k2, scale=0.9), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Create(s_cd), FadeIn(vc), FadeIn(k3, scale=0.9),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(Create(s_da), FadeIn(vd), FadeIn(fill),
                      FadeIn(k4, scale=0.9), run_time=0.70)
            self.add_sound(self.sfx["success"], gain=-12)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: the four sides and the four vertices -----------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Four Sides and the Four Vertices", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The boundary and its corners.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill_op=0.11)
            l_ab = at(board_text("AB", 17, CHALK_GREEN, "BOLD"),
                      *side_label_pos(fig.points, 0))
            l_bc = at(board_text("BC", 17, CHALK_GREEN, "BOLD"),
                      *side_label_pos(fig.points, 1))
            l_cd = at(board_text("CD", 17, CHALK_GREEN, "BOLD"),
                      *side_label_pos(fig.points, 2))
            l_da = at(board_text("DA", 17, CHALK_GREEN, "BOLD"),
                      *side_label_pos(fig.points, 3))

            k1 = at_left(chip("4 SIDES · BOUNDARY", CHALK_GREEN, size=13),
                         COL_L, 0.95)
            k2 = at_left(chip("4 VERTICES · CORNERS", CHALK_PINK, size=13),
                         COL_L, 0.15)
            note = at_left(board_text("every side joins two vertices", 12,
                                      CHALK_WHITE, "BOLD"), COL_L, -0.65)

            strip = at(board_text("The sides form the boundary, and the corners "
                                  "are the vertices.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(fig.fill), Create(fig.sides), run_time=0.70)

            self.wait(leftover(tracker, "b0"))
            self.play(Indicate(fig.sides[0], color=CHALK_YELLOW, scale_factor=1.02),
                      FadeIn(l_ab, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Indicate(fig.sides[1], color=CHALK_YELLOW, scale_factor=1.02),
                      FadeIn(l_bc, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Indicate(fig.sides[2], color=CHALK_YELLOW, scale_factor=1.02),
                      FadeIn(l_cd, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(Indicate(fig.sides[3], color=CHALK_YELLOW, scale_factor=1.02),
                      FadeIn(l_da, scale=0.9), FadeIn(k1, scale=0.9),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(fig.verts, scale=0.9), FadeIn(k2, scale=0.9),
                      run_time=0.60)
            self.add_sound(self.sfx["success"], gain=-12)

            self.wait(leftover(tracker, "b5"))
            self.play(Indicate(fig.verts, color=CHALK_PINK, scale_factor=1.12),
                      FadeIn(note, shift=UP * 0.05),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: four corners, four angles ----------------------------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("Four Corners, Four Angles", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Every corner holds an angle.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill_op=0.11)
            a, b, c, d = fig.points
            col_a, col_b, col_c, col_d = (CHALK_GREEN, CHALK_CYAN, CHALK_PINK,
                                          CHALK_AMBER)
            arc_a = corner_arc(a, b, d, CORNER_R, col_a, 3.0)
            arc_b = corner_arc(b, c, a, CORNER_R, col_b, 3.0)
            arc_c = corner_arc(c, d, b, CORNER_R, col_c, 3.0)
            arc_d = corner_arc(d, a, c, CORNER_R, col_d, 3.0)

            r1 = at(chalk_math(r"\angle A", size=26, color=col_a),
                    COL_L + COL_W / 2.0, 1.25)
            r2 = at(chalk_math(r"\angle B", size=26, color=col_b),
                    COL_L + COL_W / 2.0, 0.55)
            r3 = at(chalk_math(r"\angle C", size=26, color=col_c),
                    COL_L + COL_W / 2.0, -0.15)
            r4 = at(chalk_math(r"\angle D", size=26, color=col_d),
                    COL_L + COL_W / 2.0, -0.85)

            strip = at(board_text("Four vertices give four angles.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(fig.fill), Create(fig.sides), FadeIn(fig.verts),
                      run_time=0.70)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(arc_a), FadeIn(r1, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(arc_b), FadeIn(r2, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Create(arc_c), FadeIn(r3, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(Create(arc_d), FadeIn(r4, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(Indicate(VGroup(arc_a, arc_b, arc_c, arc_d),
                               color=CHALK_YELLOW, scale_factor=1.04),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: adjacent sides share a vertex ------------------------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("Adjacent Means Next To", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Adjacent sides share a vertex.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill_op=0.11)
            a, b, c, d = fig.points
            hl_ab = quad_side(a, b, CHALK_YELLOW, 7.0)
            hl_bc = quad_side(b, c, CHALK_CYAN, 7.0)
            hl_da = quad_side(d, a, CHALK_GREEN, 7.0)

            k1 = at_left(chip("AB and BC · meet at B", CHALK_CYAN, size=13),
                         COL_L, 0.85)
            k2 = at_left(chip("AB and DA · meet at A", CHALK_GREEN, size=13),
                         COL_L, 0.15)

            banner = at(board_text("ADJACENT SIDES SHARE A CORNER", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Neighbouring sides always share a vertex.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(fig.fill), Create(fig.sides), FadeIn(fig.verts),
                      run_time=0.70)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(hl_ab), Create(hl_bc), run_time=0.50)
            self.play(Indicate(fig.verts[1], color=CHALK_YELLOW,
                               scale_factor=1.35),
                      FadeIn(k1, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(hl_da), run_time=0.40)
            self.play(Indicate(fig.verts[0], color=CHALK_YELLOW,
                               scale_factor=1.35),
                      FadeIn(k2, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: opposite means across --------------------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("Opposite Means Across", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Opposite elements never meet.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill_op=0.11)
            a, b, c, d = fig.points
            hl_ab = quad_side(a, b, CHALK_YELLOW, 7.0)
            hl_cd = quad_side(c, d, CHALK_YELLOW, 7.0)
            hl_bc = quad_side(b, c, CHALK_CYAN, 7.0)
            hl_da = quad_side(d, a, CHALK_CYAN, 7.0)

            arc_a = corner_arc(a, b, d, CORNER_R, CHALK_GREEN, 3.0)
            arc_c = corner_arc(c, d, b, CORNER_R, CHALK_GREEN, 3.0)
            arc_b = corner_arc(b, c, a, CORNER_R, CHALK_PINK, 3.0)
            arc_d = corner_arc(d, a, c, CORNER_R, CHALK_PINK, 3.0)

            k1 = at_left(chip("AB opposite CD", CHALK_YELLOW, size=14),
                         COL_L, 1.20)
            k2 = at_left(chip("BC opposite DA", CHALK_YELLOW, size=14),
                         COL_L, 0.50)
            k3 = at_left(chip("A opposite C · B opposite D", CHALK_WHITE,
                              size=12), COL_L, -0.20)
            k4 = at_left(chip("ACROSS, NOT NEXT TO", CHALK_CYAN, size=12),
                         COL_L, -0.90)

            banner = at(board_text("NEXT TO OR ACROSS?", 18, CHALK_YELLOW,
                                   "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Opposite elements lie across the shape.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(fig.fill), Create(fig.sides), FadeIn(fig.verts),
                      run_time=0.70)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(hl_ab), Create(hl_cd), FadeIn(k1, scale=0.9),
                      run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(hl_bc), Create(hl_da), FadeIn(k2, scale=0.9),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Create(arc_a), Create(arc_c), FadeIn(k3, scale=0.9),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(Create(arc_b), Create(arc_d), FadeIn(k4, scale=0.9),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.65)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: diagonals join opposite vertices ---------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Diagonals Join Opposite Vertices", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The two segments across the inside.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill_op=0.11)
            a, b, c, d = fig.points
            # each diagonal carries its own colour, and its chip matches, so
            # AC and BD can be told apart at a glance
            diag_ac = diag(a, c, CHALK_YELLOW)
            diag_bd = diag(b, d, CHALK_PINK)

            k1 = at_left(chip("AC · a diagonal", CHALK_YELLOW, size=14,
                              width=COL_W), COL_L, 0.85)
            k2 = at_left(chip("BD · a diagonal", CHALK_PINK, size=14,
                              width=COL_W), COL_L, 0.15)

            banner = at(board_text("OPPOSITE VERTICES = DIAGONAL", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The two diagonals of ABCD are AC and BD.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(fig.fill), Create(fig.sides), FadeIn(fig.verts),
                      run_time=0.70)

            self.wait(leftover(tracker, "b0"))
            self.play(Indicate(fig.verts[0], color=CHALK_YELLOW,
                               scale_factor=1.35),
                      Indicate(fig.verts[2], color=CHALK_YELLOW,
                               scale_factor=1.35), run_time=0.55)
            self.play(Create(diag_ac), FadeIn(k1, scale=0.9), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Indicate(fig.verts[1], color=CHALK_YELLOW,
                               scale_factor=1.35),
                      Indicate(fig.verts[3], color=CHALK_YELLOW,
                               scale_factor=1.35), run_time=0.55)
            self.play(Create(diag_bd), FadeIn(k2, scale=0.9), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Indicate(VGroup(diag_ac, diag_bd), color=CHALK_YELLOW,
                               scale_factor=1.03),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the relationship map ---------------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Relationship Map", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Adjacent, opposite, or diagonal.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill_op=0.11)
            a, b, c, d = fig.points
            hl_ab = quad_side(a, b, CHALK_YELLOW, 7.0)
            hl_bc = quad_side(b, c, CHALK_YELLOW, 7.0)
            hl_cd = quad_side(c, d, CHALK_CYAN, 7.0)
            diag_ac = diag(a, c)

            k1 = self.col_item("ADJACENT", "share a corner", CHALK_YELLOW, 1.15)
            k2 = self.col_item("OPPOSITE", "across the shape", CHALK_CYAN, 0.05)
            k3 = self.col_item("DIAGONAL", "join opposite vertices", CHALK_PINK,
                               -1.05)

            strip = at(board_text("Next to is adjacent, across is opposite.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(fig.fill), Create(fig.sides), FadeIn(fig.verts),
                      run_time=0.70)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(hl_ab), Create(hl_bc),
                      Indicate(fig.verts[1], color=CHALK_YELLOW,
                               scale_factor=1.35),
                      FadeIn(k1, scale=0.9), run_time=0.65)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeOut(hl_bc), Create(hl_cd), FadeIn(k2, scale=0.9),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Create(diag_ac),
                      Indicate(VGroup(fig.verts[0], fig.verts[2]),
                               color=CHALK_YELLOW, scale_factor=1.30),
                      FadeIn(k3, scale=0.9), run_time=0.65)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.50)
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
            sub = at(board_text("Four quick checks.", 16, CHALK_WHITE, "BOLD"),
                     BOARD_CX, 2.20)

            qa = at(self.q_card("opposite of QR?",
                                self.mini_quad("PQRS", CHALK_GREEN),
                                CHALK_GREEN), -2.80, 0.92)
            qb = at(self.q_card("opposite of angle P?",
                                self.mini_quad("PQRS", CHALK_CYAN, arc="P"),
                                CHALK_CYAN), 3.70, 0.92)
            qc = at(self.q_card("adjacent to PQ?",
                                self.mini_quad("PQRS", CHALK_AMBER),
                                CHALK_AMBER), -2.80, -1.02)
            qd = at(self.q_card("join opposite corners",
                                self.mini_quad("PQRS", CHALK_PINK),
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
            a1 = at(self.answer_row("A", "PS is opposite QR",
                                    "across the quadrilateral", CHALK_GREEN),
                    BOARD_CX, 1.62)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "angle R", "R is opposite P",
                                    CHALK_CYAN), BOARD_CX, 0.82)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "PS and QR",
                                    "each shares a vertex with PQ",
                                    CHALK_AMBER), BOARD_CX, 0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "PR and QS",
                                    "the two diagonals of PQRS", CHALK_PINK),
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

            heading = at(board_text("Build · Compare · Connect", 22, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)

            r1 = at(self.answer_row("1", "4 SIDES · 4 VERTICES · 4 ANGLES",
                                    "the parts of a quadrilateral", CHALK_GREEN),
                    BOARD_CX, 1.48)
            r2 = at(self.answer_row("2", "ADJACENT = NEXT TO",
                                    "adjacent sides share a vertex", CHALK_CYAN),
                    BOARD_CX, 0.72)
            r3 = at(self.answer_row("3", "OPPOSITE = ACROSS",
                                    "AB with CD, BC with DA", CHALK_YELLOW),
                    BOARD_CX, -0.04)
            r4 = at(self.answer_row("4", "2 DIAGONALS",
                                    "they join the opposite vertices",
                                    CHALK_AMBER), BOARD_CX, -0.80)
            strip = at(board_text("Ask: are they next to each other, or across?",
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
            # the strip is written on its own bookmark as the voice says "Build
            # it, compare its parts, and connect the corners.", and only the
            # bookmark in front of "Thank you for watching," clears the board
            # and brings in the card.  (The old cut cleared everything on b4,
            # one phrase early, so the frame ran ahead of the voice.)
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

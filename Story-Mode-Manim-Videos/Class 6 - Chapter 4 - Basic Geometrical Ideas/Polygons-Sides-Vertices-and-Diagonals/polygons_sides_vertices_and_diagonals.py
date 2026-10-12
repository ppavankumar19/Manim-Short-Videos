"""
Polygons Explained: Sides, Vertices, Adjacent Elements & Diagonals
Story-mode chalkboard lesson (Telangana Class 6 Maths, Chapter 4: Basic
Geometrical Ideas, Storymode 03).

LLM KEY / FUNCTION NAME: polygons_sides_vertices_and_diagonals

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

The defining visual is ONE PERSISTENT QUADRILATERAL ABCD, built piece by piece:
the straight sides snap closed, the boundary is traced, the vertices pulse, the
adjacent and opposite parts are highlighted, and the two dashed diagonals are
drawn across the same figure.  Diagrams are drawn realistically -- solid vertex
dots, thick chalk sides, a soft interior tint and dashed diagonals.

Title + 10 scenes:
  0. Title card.
  1. From a closed curve to a polygon: the smooth boundary straightens.
  2. What a polygon must have: segments + closed + simple, three is the start.
  3. Sides and vertices of triangle ABC.
  4. Quadrilateral ABCD: four sides, four vertices.
  5. Adjacent sides (AB with BC and DA) and neighbouring vertices.
  6. Opposite side CD and the opposite vertex pairs A-C and B-D.
  7. Diagonals AC and BD join the opposite vertices.
  8. Side vs diagonal: boundary against the interior connection.
  9. Your turn: quadrilateral PQRS after the centred ten-second THINK clock.
 10. Recap: sides -> vertices -> adjacent -> diagonals, and the spoken
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


# (this section is spliced into a head whose own imports omit DashedLine,
#  Ellipse and Polygon; Dot, RoundedRectangle, VGroup, PI and np are already
#  imported by the head)
from manim import DashedLine, Ellipse, Polygon  # noqa: E402,F401

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
SIDE_W = 4.6             # stroke width of a boundary side
DOT_R = 0.078            # radius of a vertex dot
MARK_SIZE = 18           # ONE letter size for every labelled figure
LABEL_DX = 0.30          # every corner letter sits this far out sideways ...
LABEL_DY = 0.34          # ... and this far out vertically, in every scene, so
                         # no letter ever lands on a side or on another label

# The persistent quadrilateral ABCD: a clean, symmetric convex trapezium whose
# ink is centred on the board axis.  AB is the long bottom side, DC the shorter
# top side centred over it -- a well-proportioned textbook quadrilateral whose
# two diagonals cross exactly on the board's centre line (0.5, 0.47).
#   A bottom-left, B bottom-right, C top-right, D top-left (anti-clockwise)
QUAD_PTS = {"A": (BOARD_CX - 1.85, -0.34), "B": (BOARD_CX + 1.85, -0.34),
            "C": (BOARD_CX + 1.05, 1.28), "D": (BOARD_CX - 1.05, 1.28)}
QUAD_CENTRE = (BOARD_CX, 0.47)      # the ink's own centre
QUAD_LABEL_DX = {"A": (-LABEL_DX, -LABEL_DY), "B": (LABEL_DX, -LABEL_DY),
                 "C": (LABEL_DX, LABEL_DY), "D": (-LABEL_DX, LABEL_DY)}

# The triangle ABC used by the first three scenes, centred on the same axis.
TRI_PTS = {"A": (BOARD_CX - 1.60, -0.34), "B": (BOARD_CX + 1.60, -0.34),
           "C": (BOARD_CX, 1.28)}
TRI_LABEL_DX = {"A": (-LABEL_DX, -LABEL_DY), "B": (LABEL_DX, -LABEL_DY),
                "C": (0.0, LABEL_DY)}


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


def chip(text, color=CHALK_CYAN, size=15, width=None, height=0.50):
    """A small labelled chip."""
    lab = board_text(text, size, color, "BOLD")
    box = RoundedRectangle(corner_radius=0.09,
                           width=width or (lab.width + 0.40), height=height,
                           stroke_color=color, stroke_width=1.7,
                           fill_color=PANEL_FILL, fill_opacity=0.7)
    lab.move_to(box.get_center())
    return VGroup(box, lab)


def card(title, lines, color=CHALK_WHITE, width=4.0, height=1.30,
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


def side_seg(p1, p2, color=CHALK_GREEN, width=SIDE_W):
    """One thick boundary side."""
    return Line(np.array([*p1, 0.0]), np.array([*p2, 0.0]),
                stroke_color=color, stroke_width=width)


def diag(p1, p2, color=CHALK_AMBER, width=3.2):
    """A diagonal: dashed, the textbook convention."""
    return DashedLine(np.array([*p1, 0.0]), np.array([*p2, 0.0]),
                      dash_length=0.15, stroke_color=color, stroke_width=width)


def vertex(name, pt, color=CHALK_CYAN, size=MARK_SIZE, label_dx=(0.0, 0.0)):
    """A solid corner dot with its capital-letter name beside it."""
    dot = Dot(radius=DOT_R, color=color, fill_opacity=1.0).move_to(
        np.array([pt[0], pt[1], 0.0]))
    lab = board_text(name, size, color, "BOLD").move_to(
        np.array([pt[0] + label_dx[0], pt[1] + label_dx[1], 0.0]))
    grp = VGroup(dot, lab)
    grp.dot = dot
    grp.label = lab
    return grp


def poly_outline(points, color=CHALK_GREEN, width=SIDE_W, fill=CHALK_CYAN,
                 opacity=0.12):
    """A filled polygon outline (soft interior tint, thick chalk sides)."""
    return Polygon(*[np.array([*p, 0.0]) for p in points],
                   stroke_color=color, stroke_width=width,
                   fill_color=fill, fill_opacity=opacity)


def quad_vertices():
    """The four labelled corner dots of quadrilateral ABCD."""
    return quad_verts(QUAD_PTS)


def quad_points(scale=1.0, dx=0.0, dy=0.0):
    """The four corners of ABCD, shrunk about the figure's own centre.

    `scale` lets the same clean quadrilateral appear full size in the teaching
    scenes and smaller in the curve -> polygon comparison; the letters keep the
    one outward offset, so they look the same in both.
    """
    cx, cy = QUAD_CENTRE
    return {n: (cx + scale * (p[0] - cx) + dx,
                cy + scale * (p[1] - cy) + dy) for n, p in QUAD_PTS.items()}


def quad_shape(points, color=CHALK_GREEN, width=4.0):
    """The quadrilateral outline through `points` (A, B, C, D in order)."""
    return poly_outline([points[n] for n in "ABCD"], color, width)


def quad_verts(points, color=CHALK_CYAN, size=MARK_SIZE):
    """Its four solid corner dots, each with its letter just outside."""
    return VGroup(*[vertex(n, points[n], color, size, label_dx=QUAD_LABEL_DX[n])
                    for n in "ABCD"])


def tri_shape(color=CHALK_GREEN, width=4.0):
    """The triangle ABC outline."""
    return poly_outline([TRI_PTS[n] for n in "ABC"], color, width)


def tri_verts(color=CHALK_CYAN, size=MARK_SIZE):
    """Its three solid corner dots, each with its letter just outside."""
    return VGroup(*[vertex(n, TRI_PTS[n], color, size, label_dx=TRI_LABEL_DX[n])
                    for n in "ABC"])


def qpoint(name):
    """One corner of the persistent quadrilateral ABCD."""
    return QUAD_PTS[name]


def qvert(name, color=CHALK_CYAN, size=MARK_SIZE):
    """One labelled corner of the persistent quadrilateral."""
    return vertex(name, QUAD_PTS[name], color, size,
                  label_dx=QUAD_LABEL_DX[name])


def tpoint(name):
    """One corner of triangle ABC."""
    return TRI_PTS[name]


def tvert(name, color=CHALK_CYAN, size=MARK_SIZE):
    """One labelled corner of triangle ABC."""
    return vertex(name, TRI_PTS[name], color, size,
                  label_dx=TRI_LABEL_DX[name])


def open_chain(color=CHALK_WHITE, width=SIDE_W):
    """Three segments arranged as an open zig-zag (not yet a polygon).

    Symmetric about the origin, so `at(chain, BOARD_CX, y)` centres it.
    """
    a = (-1.55, 0.45)
    b = (-0.50, -0.35)
    c = (0.50, 0.45)
    d = (1.55, -0.15)
    segs = VGroup(side_seg(a, b, color, width),
                  side_seg(b, c, color, width),
                  side_seg(c, d, color, width))
    return segs


# ----------------------------------------------------------------


NARRATION = {
    "title": (
        "A polygon is the next idea in geometry. <bookmark mark='b0'/>It is a "
        "simple closed figure made from a definite number of straight line "
        "segments. <bookmark mark='b1'/>Inside every polygon we find sides, "
        "vertices, and diagonals. Let us learn their names."
    ),
    "s1": (
        "We already know a simple closed curve. <bookmark mark='b0'/>But a "
        "smooth curve like this is not a polygon. <bookmark mark='b1'/>When its "
        "boundary becomes straight line segments, <bookmark mark='b2'/>the "
        "figure is called a polygon."
    ),
    "s2": (
        "What must a polygon have? <bookmark mark='b0'/>It must be made of line "
        "segments, it must be closed, and it must not cross itself. <bookmark "
        "mark='b1'/>Here are three segments, open, so it is not a polygon yet. "
        "<bookmark mark='b2'/>Join the ends and it closes into a triangle. "
        "<bookmark mark='b3'/>Three sides is the smallest number that can close."
    ),
    "s3": (
        "Look at triangle ABC. <bookmark mark='b0'/>Its three line segments are "
        "its sides. <bookmark mark='b1'/>Its three corner points, A, B and C, "
        "are its vertices. <bookmark mark='b2'/>Each vertex is the place where "
        "two sides meet."
    ),
    "s4": (
        "Now add a fourth vertex and build quadrilateral ABCD. <bookmark "
        "mark='b0'/>Its four sides are AB, BC, CD, and DA. <bookmark "
        "mark='b1'/>It has four vertices: A, B, C and D."
    ),
    "s5": (
        "Some parts are next to each other. <bookmark mark='b0'/>Side AB shares "
        "vertex B with side BC, and shares vertex A with side DA. <bookmark "
        "mark='b1'/>So AB is adjacent to BC, and adjacent to DA. <bookmark "
        "mark='b2'/>Adjacent means next to, sharing a corner."
    ),
    "s6": (
        "Now look across the quadrilateral. <bookmark mark='b0'/>Side CD does "
        "not touch side AB, so CD is the side opposite AB. <bookmark "
        "mark='b1'/>Vertex A and vertex C are opposite vertices, <bookmark "
        "mark='b2'/>and so are B and D."
    ),
    "s7": (
        "Join the opposite vertices. <bookmark mark='b0'/>The segment from A to "
        "C is a diagonal. <bookmark mark='b1'/>The segment from B to D is the "
        "second diagonal. <bookmark mark='b2'/>So quadrilateral ABCD has two "
        "diagonals: AC and BD."
    ),
    "s8": (
        "Do not mix up a side and a diagonal. <bookmark mark='b0'/>A side is "
        "part of the boundary, like AB. <bookmark mark='b1'/>A diagonal joins "
        "opposite vertices across the inside, like AC. <bookmark mark='b2'/>BC "
        "and DA are sides, while BD is a diagonal."
    ),
    "s9q": (
        "Your turn. Four quick checks on quadrilateral PQRS. <bookmark "
        "mark='b0'/>First, name the four sides. <bookmark mark='b1'/>Second, "
        "name the sides adjacent to PQ. <bookmark mark='b2'/>Third, name the "
        "two diagonals. <bookmark mark='b3'/>And last of all: is this open "
        "chain a polygon?"
    ),
    "s9a": (
        "<bookmark mark='b0'/>The four sides are PQ, QR, RS, and SP. <bookmark "
        "mark='b1'/>The sides adjacent to PQ are QR and PS, because they share "
        "an endpoint with PQ. <bookmark mark='b2'/>The diagonals are PR and QS. "
        "<bookmark mark='b3'/>And no, the open chain is not a polygon, because "
        "it is not closed."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>A polygon is a simple closed figure "
        "made of line segments. <bookmark mark='b1'/>Its boundary segments are "
        "its sides, and its corner points are its vertices. <bookmark "
        "mark='b2'/>Sides that share a vertex are adjacent. <bookmark "
        "mark='b3'/>And line segments that join opposite vertices are diagonals. "
        "<bookmark mark='b4'/>Know the parts, and you understand the polygon. "
        "<bookmark mark='b5'/>Thank you for watching, <bookmark mark='b6'/>and "
        "see you in the next lesson."
    ),
}


class PolygonsSidesVerticesDiagonalsStory(VoiceoverScene):
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
        out_dir = _HERE / "media" / "videos" / "polygons_sides_vertices_and_diagonals"
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
    # Polygons (Class 6 Maths, Chapter 4, Storymode 03).
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
    #   * the persistent quadrilateral and triangle use the fixed, audited
    #     Q_FINAL / T_FINAL coordinates (scale 0.72) so their corner letters
    #     always clear the sub-heading above and the banner below;
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
        row (centring put each number at a different x).  The box itself stays
        centred on BOARD_CX.
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

    def mini_quad(self, names=("P", "Q", "R", "S"), color=CHALK_GREEN, s=0.30,
                  diags=False, hl=None):
        """A small labelled quadrilateral PQRS for the challenge cards.

        It is the SAME clean quadrilateral the lesson builds (A->P, B->Q, C->R,
        D->S), scaled about its own centre to a card-sized thumbnail, so the
        challenge asks about the shape the learner has just met.  The letters
        keep the one marker style -- all four at the same offset -- scaled with
        the figure so they stay just outside their corners in a 3.00-wide card.
        """
        cx, cy = QUAD_CENTRE
        pts = {n: ((QUAD_PTS[k][0] - cx) * s, (QUAD_PTS[k][1] - cy) * s)
               for n, k in zip(names, "ABCD")}
        outline = Polygon(*[np.array([*pts[n], 0.0]) for n in names],
                          stroke_color=color, stroke_width=3.2,
                          fill_color=CHALK_CYAN, fill_opacity=0.10)
        offs = {"P": (-0.20, -0.24), "Q": (0.20, -0.24),
                "R": (0.20, 0.24), "S": (-0.20, 0.24)}
        verts = VGroup(*[vertex(n, pts[n], CHALK_CYAN, size=13,
                                label_dx=offs[n]) for n in names])
        parts = [outline, verts]
        if diags:
            parts.append(diag(pts[names[0]], pts[names[2]], CHALK_AMBER, 2.6))
            parts.append(diag(pts[names[1]], pts[names[3]], CHALK_PINK, 2.6))
        if hl == "PQ":
            parts.append(side_seg(pts[names[0]], pts[names[1]],
                                  CHALK_YELLOW, 5.0))
        return VGroup(*parts)

    def mini_open(self, color=CHALK_WHITE):
        """A small open chain (not a polygon) for the challenge."""
        a, b, c, d = (-1.2, 0.4), (-0.3, -0.3), (0.5, 0.3), (1.2, -0.2)
        return VGroup(side_seg(a, b, color, 3.0), side_seg(b, c, color, 3.0),
                      side_seg(c, d, color, 3.0))

    # -- Scene 0: title ------------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = at(board_text("Polygons Explained", 28, CHALK_PINK, "BOLD"),
                       BOARD_CX, 1.66)
            sub = at(board_text("Sides · Vertices · Adjacent Elements · "
                                "Diagonals", 18, CHALK_WHITE, "BOLD"),
                     BOARD_CX, 1.00)

            specs = (("SIDE", "side", "the boundary", CHALK_GREEN),
                     ("VERTEX", "vertex", "a corner point", CHALK_CYAN),
                     ("DIAGONAL", "diagonal", "joins opposite vertices",
                      CHALK_AMBER))
            # One centred row: the three captions differ in width, so the
            # columns are placed by equal air (row_centres) and the row's ink is
            # centred on the board axis.  The old columns ran -2.20..+2.20, i.e.
            # centred on 0.0, half a unit left of BOARD_CX.
            labels, figs, notes = VGroup(), VGroup(), VGroup()
            raw_figs, caps = [], []
            for label, kind, note, color in specs:
                if kind == "side":
                    fig = VGroup(side_seg((-0.8, 0.0), (0.8, 0.0), color, 4.6),
                                 Dot(radius=DOT_R, color=CHALK_CYAN,
                                     fill_opacity=1.0).move_to(
                                     np.array([-0.8, 0.0, 0.0])),
                                 Dot(radius=DOT_R, color=CHALK_CYAN,
                                     fill_opacity=1.0).move_to(
                                     np.array([0.8, 0.0, 0.0])))
                elif kind == "vertex":
                    fig = Dot(radius=0.11, color=color, fill_opacity=1.0)
                else:
                    fig = diag((-0.8, 0.0), (0.8, 0.0), color, 3.2)
                raw_figs.append(fig)
                caps.append((board_text(label, 14, color, "BOLD"),
                             board_text(note, 12, CHALK_WHITE, "BOLD")))
            xs = row_centres([max(f.width, c[0].width, c[1].width) / 2.0
                              for f, c in zip(raw_figs, caps)], 0.55)
            for x, fig, (lab, note) in zip(xs, raw_figs, caps):
                figs.add(at(fig, x, -0.18))
                labels.add(at(lab, x, 0.34))
                notes.add(at(note, x, -0.74))
            strip = at(board_text("A simple closed figure made of line "
                                  "segments.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(title, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            # the parts are drawn first, then NAMED on the line that names them
            # ("sides, vertices, and diagonals ... let us learn their names")
            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[Create(m) for m in figs], lag_ratio=0.22),
                      run_time=0.75)

            self.wait(leftover(tracker, "b1"))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.06) for m in labels],
                                  lag_ratio=0.18), run_time=0.55)
            self.play(LaggedStart(*[FadeIn(m, scale=0.85) for m in notes],
                                  lag_ratio=0.18), run_time=0.55)
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: from a closed curve to a polygon ---------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("From a Closed Curve to a Polygon", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The smooth boundary becomes straight "
                                "segments.", 17, CHALK_WHITE, "BOLD"),
                     BOARD_CX, SUB_Y)

            # the SAME clean quadrilateral, shown at 0.85 here so the oval, the
            # arrow and the polygon form one centred row: the oval's ink on the
            # left, the arrow centred in the gap between them, the polygon on
            # the right, each caption under its own figure.  Block ink+labels
            # [-3.52..+4.52] -> centre +0.50.  (It used to run -3.85..+4.80 with
            # the arrow butted against the polygon's left corner.)
            ymid = 0.50
            curve = at(Ellipse(width=1.70, height=1.30, stroke_color=CHALK_WHITE,
                               stroke_width=3.2), -2.43, ymid)
            curve_lab = at(board_text("a smooth closed curve", 14, CHALK_WHITE,
                                      "BOLD"), -2.43, -0.62)
            pts = quad_points(0.85, dx=2.57 - BOARD_CX, dy=ymid - QUAD_CENTRE[1])
            poly = quad_shape(pts, CHALK_GREEN, 3.4)
            verts = quad_verts(pts, CHALK_CYAN, MARK_SIZE)
            poly_lab = at(board_text("polygon", 15, CHALK_GREEN, "BOLD"),
                          2.57, -0.62)
            arrow = Arrow(np.array([curve.get_right()[0] + 0.45, ymid, 0.0]),
                          np.array([poly.get_left()[0] - 0.45, ymid, 0.0]),
                          buff=0.0, color=CHALK_AMBER, stroke_width=3.0,
                          tip_length=0.22)

            banner = at(board_text("POLYGON = SIMPLE + CLOSED + LINE SEGMENTS",
                                   17, CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The corners appear when the boundary "
                                  "straightens.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(curve), FadeIn(curve_lab, shift=UP * 0.05),
                      run_time=0.65)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(poly), FadeIn(verts, scale=0.8), Create(arrow),
                      FadeIn(poly_lab, scale=0.9), run_time=0.70)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: what must a polygon have -----------------------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("What Must a Polygon Have?", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Line segments, closed, and no crossing.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # the chain and the triangle are both centred on the board axis;
            # their captions are side labels, parked clear of the figure
            chain = at(open_chain(CHALK_WHITE, 4.0), BOARD_CX, 0.90)
            open_note = at(board_text("not closed", 14, CHALK_PINK, "BOLD"),
                           3.30, 0.90)
            tri = tri_shape(CHALK_GREEN, 4.0)
            tverts = tri_verts()
            closed_note = at(board_text("closed", 14, CHALK_GREEN, "BOLD"),
                             3.30, 0.30)

            banner = at(board_text("SIMPLE + CLOSED + LINE SEGMENTS", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("3 sides is the smallest number.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(chain), FadeIn(open_note, shift=UP * 0.05),
                      run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeOut(chain), FadeOut(open_note), run_time=0.40)
            self.play(Create(tri), FadeIn(tverts, scale=0.8),
                      FadeIn(closed_note, shift=UP * 0.05), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: sides and vertices of a triangle ---------------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Sides and Vertices", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Triangle ABC: three sides, three corners.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            tri = tri_shape(CHALK_GREEN, 4.0)
            verts = tri_verts()
            side_ab = side_seg(tpoint("A"), tpoint("B"), CHALK_CYAN, 5.5)
            side_bc = side_seg(tpoint("B"), tpoint("C"), CHALK_YELLOW, 5.5)
            side_ca = side_seg(tpoint("C"), tpoint("A"), CHALK_PINK, 5.5)

            sides_chip = at(chip("SIDES", CHALK_GREEN), -3.30, 1.55)
            verts_chip = at(chip("VERTICES", CHALK_CYAN), 3.30, 1.55)
            banner = at(board_text("SIDES MEET AT VERTICES", 18, CHALK_YELLOW,
                                   "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("A triangle has three sides and three "
                                  "vertices.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(tri), FadeIn(verts, scale=0.8), run_time=0.60)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(side_ab), FadeIn(sides_chip, scale=0.9),
                      run_time=0.45)
            self.play(Create(side_bc), Create(side_ca), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(LaggedStart(*[Indicate(v, color=CHALK_CYAN,
                                             scale_factor=1.2)
                                    for v in verts], lag_ratio=0.25),
                      FadeIn(verts_chip, scale=0.9), run_time=0.70)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Indicate(verts[1], color=CHALK_YELLOW, scale_factor=1.3),
                      Indicate(side_ab, color=CHALK_YELLOW, scale_factor=1.05),
                      Indicate(side_bc, color=CHALK_YELLOW, scale_factor=1.05),
                      run_time=0.65)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: building quadrilateral ABCD --------------------------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("Building Quadrilateral ABCD", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Four sides, four vertices.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            outline = quad_shape(QUAD_PTS, CHALK_GREEN, 4.0)
            verts = quad_verts(QUAD_PTS)
            side_ab = side_seg(qpoint("A"), qpoint("B"), CHALK_CYAN, 5.5)
            side_bc = side_seg(qpoint("B"), qpoint("C"), CHALK_YELLOW, 5.5)
            side_cd = side_seg(qpoint("C"), qpoint("D"), CHALK_PINK, 5.5)
            side_da = side_seg(qpoint("D"), qpoint("A"), CHALK_WHITE, 5.5)
            sides_chip = at(chip("4 SIDES", CHALK_GREEN), -3.30, 1.55)
            verts_chip = at(chip("4 VERTICES", CHALK_CYAN), 3.30, 1.55)

            strip = at(board_text("A quadrilateral is a polygon with four "
                                  "sides.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(outline), FadeIn(verts, scale=0.8), run_time=0.60)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(side_ab), FadeIn(sides_chip, scale=0.9),
                      run_time=0.40)
            self.play(Create(side_bc), run_time=0.30)
            self.play(Create(side_cd), run_time=0.30)
            self.play(Create(side_da), run_time=0.30)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(LaggedStart(*[Indicate(v, color=CHALK_CYAN,
                                             scale_factor=1.15)
                                    for v in verts], lag_ratio=0.22),
                      FadeIn(verts_chip, scale=0.9), run_time=0.70)
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: adjacent = next to -----------------------------------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("Adjacent = Next To", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Sides that share a corner.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            outline = quad_shape(QUAD_PTS, CHALK_GREEN, 4.0)
            verts = quad_verts(QUAD_PTS)
            side_ab = side_seg(qpoint("A"), qpoint("B"), CHALK_CYAN, 5.5)
            side_bc = side_seg(qpoint("B"), qpoint("C"), CHALK_YELLOW, 5.5)
            side_da = side_seg(qpoint("D"), qpoint("A"), CHALK_PINK, 5.5)

            banner = at(board_text("ADJACENT = SHARING A CORNER", 18,
                                   CHALK_AMBER, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("AB is adjacent to BC and to DA — they share "
                                  "a corner.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(outline), FadeIn(verts, scale=0.8), run_time=0.60)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(side_ab), run_time=0.45)
            self.play(Indicate(verts[0], color=CHALK_CYAN, scale_factor=1.25),
                      Indicate(verts[1], color=CHALK_CYAN, scale_factor=1.25),
                      run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(side_bc), Create(side_da), run_time=0.55)
            self.play(Indicate(verts[1], color=CHALK_YELLOW, scale_factor=1.25),
                      Indicate(verts[0], color=CHALK_YELLOW, scale_factor=1.25),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: adjacent vs opposite ---------------------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("Across, Not Next To", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The side and vertices opposite AB.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            outline = quad_shape(QUAD_PTS, CHALK_GREEN, 4.0)
            verts = quad_verts(QUAD_PTS)
            side_ab = side_seg(qpoint("A"), qpoint("B"), CHALK_CYAN, 5.5)
            side_cd = side_seg(qpoint("C"), qpoint("D"), CHALK_PINK, 5.5)

            banner = at(board_text("OPPOSITE VERTICES: A and C · B and D", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("CD is the side opposite AB — they do not "
                                  "share a corner.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(outline), FadeIn(verts, scale=0.8), run_time=0.60)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(side_ab), Create(side_cd), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Indicate(verts[0], color=CHALK_AMBER, scale_factor=1.3),
                      Indicate(verts[2], color=CHALK_AMBER, scale_factor=1.3),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Indicate(verts[1], color=CHALK_YELLOW, scale_factor=1.3),
                      Indicate(verts[3], color=CHALK_YELLOW, scale_factor=1.3),
                      run_time=0.60)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: diagonals --------------------------------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Diagonals Cut Across", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Join the opposite vertices.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            outline = quad_shape(QUAD_PTS, CHALK_GREEN, 4.0)
            verts = quad_verts(QUAD_PTS)
            # each diagonal carries its own colour (and its own chip, on the
            # matching side, so the pair is symmetric about the board axis), so
            # AC and BD can be told apart at a glance
            d_ac = diag(qpoint("A"), qpoint("C"), CHALK_AMBER, 4.0)
            d_bd = diag(qpoint("B"), qpoint("D"), CHALK_PINK, 4.0)

            diag_ac = at(chip("AC", CHALK_AMBER, width=1.20), -3.30, 1.55)
            diag_bd = at(chip("BD", CHALK_PINK, width=1.20), 3.30, 1.55)
            banner = at(board_text("DIAGONAL = JOIN OPPOSITE VERTICES", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Quadrilateral ABCD has two diagonals: AC "
                                  "and BD.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(outline), FadeIn(verts, scale=0.8), run_time=0.60)

            self.wait(leftover(tracker, "b0"))
            self.play(Indicate(verts[0], color=CHALK_AMBER, scale_factor=1.3),
                      Indicate(verts[2], color=CHALK_AMBER, scale_factor=1.3),
                      run_time=0.50)
            self.play(Create(d_ac), FadeIn(diag_ac, scale=0.9), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Indicate(verts[1], color=CHALK_PINK, scale_factor=1.3),
                      Indicate(verts[3], color=CHALK_PINK, scale_factor=1.3),
                      run_time=0.50)
            self.play(Create(d_bd), FadeIn(diag_bd, scale=0.9), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: side or diagonal -------------------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("Side or Diagonal?", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Boundary segment, or opposite-vertex "
                                "connection?", 17, CHALK_WHITE, "BOLD"),
                     BOARD_CX, SUB_Y)

            outline = quad_shape(QUAD_PTS, CHALK_GREEN, 4.0)
            verts = quad_verts(QUAD_PTS)
            side_ab = side_seg(qpoint("A"), qpoint("B"), CHALK_CYAN, 5.5)
            d_ac = diag(qpoint("A"), qpoint("C"), CHALK_AMBER, 3.4)

            banner = at(board_text("BOUNDARY = SIDE · OPPOSITE VERTICES = "
                                   "DIAGONAL", 17, CHALK_YELLOW, "BOLD"),
                        BOARD_CX, BANNER_Y)
            strip = at(board_text("AB is a side; AC is a diagonal — a diagonal "
                                  "is never on the boundary.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(outline), FadeIn(verts, scale=0.8), run_time=0.60)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(side_ab), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(d_ac), run_time=0.45)
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
                         BOARD_CX, 2.78)
            sub = at(board_text("Four checks on quadrilateral PQRS.", 16,
                                CHALK_WHITE, "BOLD"), BOARD_CX, 2.20)

            qa = at(self.q_card("name the four sides", self.mini_quad(),
                                CHALK_GREEN), -2.75, 0.95)
            qb = at(self.q_card("adjacent to PQ?",
                                self.mini_quad(hl="PQ"), CHALK_YELLOW),
                    3.75, 0.95)
            qc = at(self.q_card("name the diagonals",
                                self.mini_quad(diags=True), CHALK_AMBER),
                    -2.75, -1.00)
            qd = at(self.q_card("is this a polygon?", self.mini_open(),
                                CHALK_CYAN), 3.75, -1.00)

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
            a1 = at(self.answer_row("A", "PQ · QR · RS · SP", "the four sides",
                                    CHALK_GREEN), BOARD_CX, 1.62)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "QR and PS",
                                    "share an endpoint with PQ", CHALK_YELLOW),
                    BOARD_CX, 0.82)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "PR and QS", "join opposite vertices",
                                    CHALK_AMBER), BOARD_CX, 0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "NO — not a polygon",
                                    "an open chain is not closed", CHALK_PINK),
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

            heading = at(board_text("Know the Parts", 22, CHALK_AMBER, "BOLD"),
                         BOARD_CX, ROW_Y)

            r1 = at(self.answer_row("1", "POLYGON",
                                    "simple + closed + line segments",
                                    CHALK_GREEN), BOARD_CX, 1.48)
            r2 = at(self.answer_row("2", "SIDES · VERTICES",
                                    "boundary segments · corner points",
                                    CHALK_CYAN), BOARD_CX, 0.72)
            r3 = at(self.answer_row("3", "ADJACENT",
                                    "sides sharing a corner", CHALK_YELLOW),
                    BOARD_CX, -0.04)
            r4 = at(self.answer_row("4", "DIAGONALS",
                                    "join opposite vertices", CHALK_AMBER),
                    BOARD_CX, -0.80)
            strip = at(board_text("Know the parts — understand the polygon.",
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
            # the strip is written on its own bookmark as the voice says "Know
            # the parts, and you understand the polygon.", and only the bookmark
            # in front of "Thank you for watching," clears the board and brings
            # in the card.  (The old cut cleared everything on b4, one phrase
            # early, so the frame ran ahead of the voice.)
            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeOut(heading), FadeOut(r1), FadeOut(r2), FadeOut(r3),
                      FadeOut(r4), FadeOut(strip), run_time=0.55)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.50)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.closing(tracker, thanks, run_time=1.1)
            self._capture_srt(tracker)

        self.wait(END_HOLD)

"""
Constructing Special Quadrilaterals: Rhombus, Parallelogram and Square
Story-mode chalkboard lesson (Telangana Class 8 Maths, Chapter 3:
Construction of Quadrilaterals, Storymode 07).

LLM KEY / FUNCTION NAME: construct_special_quadrilaterals_rhombus_parallelogram

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

The defining idea: a special quadrilateral is named information.  The
parallelogram is given two sides and one angle, and its angle properties supply
the other three angles; the rhombus is given its two diagonals, and the
perpendicular-bisecting property places all four vertices; the square is the
rhombus construction with the extra condition that the diagonals are equal.
Every figure is built from the given numbers with vectors, never by hand.

Title + 10 scenes:
  0. Title card.
  1. Three short lists of measurements -- and why they are enough.
  2. Parallelogram B E L T: derive the missing angles from the properties.
  3. Construct B E L T: S.A.S triangle, then two 135 degree rays meet at T.
  4. Rhombus A B C D: read the two diagonal properties.
  5. Construct the rhombus: A C, its perpendicular bisector, B and D at 3 cm.
  6. From rhombus to square: equal diagonals, then square J U M P.
  7. Three shapes, three property strategies.
  8. The reusable method: analyse before you draw.
  9. Your turn: a parallelogram's angles and a rhombus's half-diagonals.
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


PARA_SCALE = 0.72       # board units per centimetre
RHOMB_SCALE = 0.68
SQUARE_SCALE = 0.80
PARA_CENTRE = np.array([BOARD_CX - 1.65, 0.20, 0.0])
RHOMB_CENTRE = np.array([BOARD_CX - 1.50, 0.05, 0.0])
SQUARE_CENTRE = np.array([BOARD_CX - 1.50, 0.05, 0.0])


def unit(deg):
    """The unit vector at `deg` degrees."""
    a = deg * DEGREES
    return np.array([np.cos(a), np.sin(a), 0.0])


def ray_point(vertex, deg, length):
    """The point `length` away from `vertex` in the direction `deg`."""
    return np.array(vertex, dtype=float) + length * unit(deg)


def dir_deg(p, q) -> float:
    """The direction from `p` to `q`, in degrees."""
    d = np.array(q, dtype=float) - np.array(p, dtype=float)
    return float(np.degrees(np.arctan2(d[1], d[0])))


def dist(p, q) -> float:
    """How far apart two points are, in board units."""
    return float(np.linalg.norm(np.array(p, dtype=float)
                                - np.array(q, dtype=float)))


def mid(p, q):
    """The midpoint of two points."""
    return (np.array(p, dtype=float) + np.array(q, dtype=float)) / 2.0


def to_board(points, centre, scale):
    """Map centimetre coordinates onto the board: the figure's bounding box
    centre goes to `centre`, and one centimetre becomes `scale` board units."""
    pts = [np.array(p, dtype=float) for p in points]
    lo = np.min(np.array([p[:2] for p in pts]), axis=0)
    hi = np.max(np.array([p[:2] for p in pts]), axis=0)
    c = (lo + hi) / 2.0
    return [np.array([centre[0] + (p[0] - c[0]) * scale,
                      centre[1] + (p[1] - c[1]) * scale, 0.0]) for p in pts]


def perpendicular_ends(p, direction_deg, length):
    """The two ends of the segment of `length` through `p`, perpendicular to
    `direction_deg` -- the line the other diagonal lies on."""
    return (ray_point(p, direction_deg + 90.0, length),
            ray_point(p, direction_deg - 90.0, length))


# ------------------------------------------------------------- the figures --
def parallelogram_frame(centre=None, scale=PARA_SCALE,
                        be=4.2, el=5.0, angle_t=45.0):
    """Parallelogram B E L T.

    B E = 4.2 cm and E L = 5 cm with the angle at T = 45 degrees.  Because the
    opposite angles of a parallelogram are equal, the angle at E is also 45, so
    triangle B E L is fixed by S.A.S; T is then B + (L - E), which is where the
    two 135 degree rays from B and from L meet."""
    b = np.array([0.0, 0.0, 0.0])
    e = ray_point(b, 0.0, be)
    l = ray_point(e, 180.0 - angle_t, el)          # angle at E = angle at T
    t = b + (l - e)
    B, E, L, T = to_board((b, e, l, t),
                          PARA_CENTRE if centre is None else centre, scale)
    return {
        "quad": (B, E, L, T),
        "model": (b, e, l, t),
        "be_deg": dir_deg(B, E), "el_deg": dir_deg(E, L),
        "eb_deg": dir_deg(E, B), "ebt_deg": dir_deg(B, T),
        "le_deg": dir_deg(L, E), "lt_deg": dir_deg(L, T),
    }


def rhombus_frame(centre=None, scale=RHOMB_SCALE, ac=4.5, bd=6.0):
    """Rhombus A B C D from its two diagonals.

    A C and B D bisect each other at right angles, so with O at their crossing
    A and C are half of A C either side of O, and B and D are half of B D."""
    a = np.array([-ac / 2.0, 0.0, 0.0])
    c = np.array([ac / 2.0, 0.0, 0.0])
    b = np.array([0.0, bd / 2.0, 0.0])
    d = np.array([0.0, -bd / 2.0, 0.0])
    A, B, C, D = to_board((a, b, c, d),
                          RHOMB_CENTRE if centre is None else centre, scale)
    return {
        "quad": (A, B, C, D),
        "model": (a, b, c, d),
        "ac_deg": dir_deg(A, C), "bd_deg": dir_deg(B, D),
        "half_ac": ac / 2.0, "half_bd": bd / 2.0,
        "diag": (ac, bd),
    }


def square_frame(centre=None, scale=SQUARE_SCALE, diag=4.2):
    """Square J U M P from one diagonal.

    In a square the diagonals are equal and bisect each other at right angles,
    so the other diagonal is the same length, and every vertex is half a
    diagonal from the crossing point O."""
    half = diag / 2.0
    j = np.array([-half, 0.0, 0.0])
    u = np.array([half, 0.0, 0.0])
    m = np.array([0.0, half, 0.0])
    p = np.array([0.0, -half, 0.0])
    J, M, U, P = to_board((j, m, u, p),
                          SQUARE_CENTRE if centre is None else centre, scale)
    return {
        "quad": (J, M, U, P),
        "model": (j, m, u, p),
        "ju_deg": dir_deg(J, U), "mp_deg": dir_deg(M, P),
        "half": half, "diag": diag,
    }


def labelled_shapes(centre=None, scale=0.30):
    """Small versions of all three shapes, for the comparison and the recap:
    returns (parallelogram, rhombus, square) point sets, each centred on its
    own centre argument."""
    return (parallelogram_frame(centre, scale)["quad"],
            rhombus_frame(centre, scale)["quad"],
            square_frame(centre, scale)["quad"])


def side_label(p1, p2, centroid, text, color=CHALK_CYAN, size=17,
               offset=0.22):
    """A length label placed clear of its own side, pushed along the true
    outward normal (the earlier version pushed along centroid -> midpoint, which
    is not perpendicular, so a label could sit on its own side)."""
    lab = board_text(text, size, color, "BOLD")
    p1 = np.array(p1, dtype=float)
    p2 = np.array(p2, dtype=float)
    m = (p1 + p2) / 2.0
    d = p2 - p1
    n = np.array([-d[1], d[0], 0.0])
    n = n / (np.linalg.norm(n[:2]) or 1.0)
    if np.dot(n, m - np.array(centroid, dtype=float)) < 0:
        n = -n
    half = (abs(n[0]) * lab.width + abs(n[1]) * lab.height) / 2.0
    return lab.move_to(m + n * (half + offset))


def degree_card(label, color=CHALK_AMBER, size=17) -> VGroup:
    """A card for an angle: LaTeX for the angle symbol, since Segoe Print has
    no glyph for it."""
    tex = MathTex(label, font_size=size, color=color)
    box = RoundedRectangle(corner_radius=0.08, width=tex.width + 0.46,
                           height=tex.height + 0.32, stroke_color=color,
                           stroke_width=1.8, fill_color="#16202B",
                           fill_opacity=0.8)
    tex.move_to(box.get_center())
    grp = VGroup(box, tex)
    grp.tex = tex
    return grp


def value_card(label, color=CHALK_GREEN, size=16) -> VGroup:
    """A card for a derived value, e.g. 180 - 45 = 135."""
    tex = MathTex(label, font_size=size, color=color)
    box = RoundedRectangle(corner_radius=0.08, width=tex.width + 0.44,
                           height=tex.height + 0.28, stroke_color=color,
                           stroke_width=1.8, fill_color="#16202B",
                           fill_opacity=0.8)
    tex.move_to(box.get_center())
    grp = VGroup(box, tex)
    grp.tex = tex
    return grp


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


NARRATION = {
    "title": (
        "Three special quadrilaterals, and three surprisingly short lists of "
        "measurements.<bookmark mark='b0'/> Each of them carries a property "
        "that supplies whatever is missing.<bookmark mark='b1'/>"
    ),
    "scene1": (
        "Look at what each shape is given.<bookmark mark='b0'/> A "
        "parallelogram: two sides and one angle. Only three "
        "measurements.<bookmark mark='b0b'/> A rhombus: two diagonals. Only "
        "two.<bookmark mark='b1'/> A square: a single diagonal. Can that "
        "really be enough?<bookmark mark='b2'/> It can, because the name of "
        "the shape is information too: its properties give us the measurements "
        "that were never listed.<bookmark mark='b3'/>"
    ),
    "scene2": (
        "Start with the parallelogram B E L T.<bookmark mark='b0'/> We are "
        "given B E, four point two centimetres, E L, five centimetres, and the "
        "angle at T, forty five degrees.<bookmark mark='b1'/> In a "
        "parallelogram opposite angles are equal, so the angle at E is also "
        "forty five degrees.<bookmark mark='b2'/> And consecutive angles are "
        "supplementary: one hundred and eighty minus forty five is one hundred "
        "and thirty five.<bookmark mark='b3'/> So the angle at L is one "
        "hundred and thirty five degrees, and so is the angle at "
        "B.<bookmark mark='b4'/> Four angles, from one given "
        "angle.<bookmark mark='b5'/>"
    ),
    "scene3": (
        "Now the construction is straightforward.<bookmark mark='b0'/> Draw B "
        "E, four point two centimetres.<bookmark mark='b1'/> At E set out "
        "forty five degrees and mark E L, five centimetres: that is triangle B "
        "E L by side, angle, side.<bookmark mark='b2'/> At B, set out one "
        "hundred and thirty five degrees and draw the ray.<bookmark "
        "mark='b3'/> At L, set out one hundred and thirty five degrees as "
        "well, and draw the second ray.<bookmark mark='b4'/> The two rays meet "
        "at T, and the parallelogram is complete.<bookmark mark='b5'/>"
    ),
    "scene4": (
        "Now the rhombus.<bookmark mark='b0'/> A rhombus is given by its two "
        "diagonals: A C is four point five centimetres and B D is six. Only two "
        "measurements, but a rhombus has two properties we can use.<bookmark "
        "mark='b1'/> Its diagonals are perpendicular: they cross at right "
        "angles, at O.<bookmark mark='b2'/> And they bisect each other, so O "
        "is the midpoint of both.<bookmark mark='b3'/> Which means O B and O D "
        "are each half of six: three centimetres.<bookmark mark='b4'/>"
    ),
    "scene5": (
        "So this is how we construct it.<bookmark mark='b0'/> Draw A C, four "
        "point five centimetres, and mark its midpoint O.<bookmark "
        "mark='b1'/> Through O draw the perpendicular to A C: that is the line "
        "the other diagonal lies on.<bookmark mark='b2'/> Set the compasses to "
        "three centimetres, put the needle at O, and mark the perpendicular on "
        "both sides.<bookmark mark='b3'/> Those marks are B and D, because each "
        "is three centimetres from O, exactly half of B D.<bookmark "
        "mark='b4'/> Join A to B, B to C, C to D and D to A: the rhombus is "
        "complete, and we never needed its side lengths.<bookmark mark='b5'/>"
    ),
    "scene6": (
        "Here is a question worth asking: what if the two diagonals of the "
        "rhombus were equal?<bookmark mark='b0'/> Watch the shorter diagonal "
        "grow until both are the same length.<bookmark mark='b1'/> The rhombus "
        "becomes a square, because equal diagonals that bisect each other at "
        "right angles always give a square.<bookmark mark='b2'/> So we can "
        "construct square J U M P with diagonal four point two centimetres the "
        "same way: draw J U, find its midpoint, and draw the perpendicular "
        "through it.<bookmark mark='b3'/> The other diagonal is equal, so it is "
        "also four point two centimetres, and O M and O P are two point one "
        "centimetres each.<bookmark mark='b4'/> Mark M and P, join the four "
        "vertices, and the square is complete.<bookmark mark='b5'/>"
    ),
    "scene7": (
        "Three shapes, three strategies.<bookmark mark='b0'/> For the "
        "parallelogram, opposite angles are equal and consecutive angles add to "
        "one hundred and eighty degrees: that gives the missing "
        "angles.<bookmark mark='b1'/> For the rhombus, the diagonals bisect "
        "each other at right angles: that gives every vertex from the "
        "diagonals.<bookmark mark='b2'/> For the square the diagonals are equal "
        "as well: the same construction, with one extra condition.<bookmark "
        "mark='b3'/> So which property gives the missing information?<bookmark "
        "mark='b4'/>"
    ),
    "scene8": (
        "That is the method for every special quadrilateral.<bookmark "
        "mark='b0'/> Identify the shape. Recall its properties. Derive the "
        "measurements that are missing. Then construct.<bookmark mark='b1'/> "
        "Analyse before you draw: the property tells you what to do with the "
        "ruler, the compasses and the protractor.<bookmark mark='b2'/>"
    ),
    "scene9_setup": (
        "Your turn, two quick ones.<bookmark mark='b0'/> A parallelogram has "
        "angle A equal to sixty five degrees. What are the other three "
        "angles?<bookmark mark='b1'/> And a rhombus has diagonals A C of eight "
        "centimetres and B D of six. How far is each vertex from the point "
        "where the diagonals cross?<bookmark mark='b2'/> Pause the video and "
        "work them out.<bookmark mark='b3'/>"
    ),
    "scene9_reveal": (
        "Let us check.<bookmark mark='b0'/> In the parallelogram the angle "
        "opposite A is C, so C is sixty five degrees; and the angles next to A "
        "are supplementary, so B and D are one hundred and eighty minus sixty "
        "five: one hundred and fifteen degrees each.<bookmark mark='b1'/> In "
        "the rhombus, O is the midpoint of both diagonals, so O A and O C are "
        "four centimetres, and O B and O D are three.<bookmark mark='b2'/> Draw "
        "the perpendicular diagonals, mark those distances, and join the ends: "
        "that is the rhombus.<bookmark mark='b3'/>"
    ),
    "scene10": (
        "One idea holds all three together.<bookmark mark='b0'/> A special "
        "shape comes with extra information: use its properties to find the "
        "missing measurements, and then construct.<bookmark mark='b1'/> Know "
        "the shape. Use its properties. Construct it.<bookmark mark='b2'/> "
        "Thank you for watching!<bookmark mark='b3'/> See you in the next "
        "lesson!<bookmark mark='b4'/>"
    ),
}


class ConstructSpecialQuadrilateralsRhombusParallelogramStory(VoiceoverScene):
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
        out_dir = _HERE / "media" / "videos" / "construct_special_quadrilaterals_rhombus_parallelogram"
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
        self.beat1_special()
        self.beat2_parallelogram()
        self.beat3_construct_belt()
        self.beat4_rhombus_props()
        self.beat5_construct_rhombus()
        self.beat6_square()
        self.beat7_compare()
        self.beat8_method()
        self.beat9_challenge()
        self.beat10_recap()

        self._write_real_srt()

    # ================================================================ beats ==

    # -- the SRT export, with a short tail folded into the caption before it --
    def _capture_srt(self, tracker, words_per_line: int = 9) -> None:
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

    # -- instruments ---------------------------------------------------------
    def put_down_tool(self, tool, run_time: float = 0.3) -> None:
        """Lay a pair of compasses down: fade a static copy and drop the live
        `always_redraw` object, whose updater would rebuild it every frame."""
        snap = tool.copy()
        snap.clear_updaters()
        self.remove(tool)
        self.add(snap)
        self.play(FadeOut(snap), run_time=run_time)

    def compass_on(self, centre, target, radius, spread, color,
                   hinge_dir=None, leg_ratio=0.62, bias: float = 0.0):
        v = np.array(centre, dtype=float)
        ang = float(np.degrees(np.arctan2(target[1] - v[1], target[0] - v[0])))
        start = ang - spread + bias
        sweep = ValueTracker(0.004)

        def tip_at():
            a = (start + sweep.get_value()) * DEGREES
            return v + radius * np.array([np.cos(a), np.sin(a), 0.0])

        arc = always_redraw(lambda: Arc(
            radius=radius, start_angle=start * DEGREES,
            angle=max(sweep.get_value(), 0.004) * DEGREES, arc_center=v,
            color=color, stroke_width=2.8))
        tool = always_redraw(lambda: compass_tool(
            v, tip_at(), hinge_dir=hinge_dir, leg_ratio=leg_ratio))
        self.add(arc, tool)
        self.arc, self.tool, self.sweep = arc, tool, sweep
        return sweep

    def sweep_compass(self, tracker, mark: str, spread: float,
                      put_down: bool = True, reserve: float = 0.0,
                      hold: bool = True) -> None:
        budget = leftover(tracker, mark)
        sweep_time = max(budget - (0.35 if put_down else 0.0) - reserve, 0.4)
        self.play(self.sweep.animate.set_value(2 * spread), run_time=sweep_time)
        if put_down:
            self.put_down_tool(self.tool)
        if hold:
            self.wait(leftover(tracker, mark))

    def setout_arm(self, vertex, start_deg, end_deg, length, radius, color,
                   stroke: float = 3.4):
        """An arm that swings from one direction to the other while the angle
        arc grows under it."""
        v = np.array(vertex, dtype=float)
        sweep = ValueTracker(0.0)

        def now() -> float:
            return start_deg + (end_deg - start_deg) * sweep.get_value()

        arm = always_redraw(lambda: Line(
            v, ray_point(v, now(), length), color=color, stroke_width=stroke))
        arc = always_redraw(lambda: Arc(
            radius=radius, start_angle=start_deg * DEGREES,
            angle=(end_deg - start_deg) * sweep.get_value() * DEGREES,
            arc_center=v, color=color, stroke_width=2.6))
        self.add(arc, arm)
        self.arm, self.arm_sweep, self.arm_arc = arm, sweep, arc
        return sweep

    def vertex_letters(self, points, offsets, letters="ABCD", size=17,
                       color=CHALK_WHITE):
        out = []
        for letter, p, off in zip(letters, points, offsets):
            out.append(board_text(letter, size, color, "BOLD").move_to(
                np.array(p, dtype=float) + np.array([off[0], off[1], 0.0])))
        return VGroup(*out)

    def column_card(self, mob, y, x=3.05):
        return mob.move_to(np.array([x, y, 0]))

    def column_note(self, text, y, x=3.05, size=16, color=CHALK_WHITE):
        return board_text(text, size, color, "BOLD").move_to(
            np.array([x, y, 0]))

    def ray_line(self, vertex, direction_deg, length, color=CHALK_PINK,
                 width=3.2, dashed=False):
        end = ray_point(vertex, direction_deg, length)
        if dashed:
            return DashedLine(np.array(vertex, dtype=float), end, color=color,
                              stroke_width=width, dash_length=0.14)
        return Line(np.array(vertex, dtype=float), end, color=color,
                    stroke_width=width)

    def shape_sketch(self, pts, color=CHALK_WHITE, fill=CHALK_WHITE,
                     width=2.4, opacity=0.10):
        return Polygon(*pts, color=color, stroke_width=width,
                       fill_color=fill, fill_opacity=opacity)

    # -- Scene 0: title ------------------------------------------------------
    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Special Quadrilaterals", 34, CHALK_WHITE,
                               "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 2.00, 0]))
            sub = board_text("Parallelogram · Rhombus · Square", 20,
                             CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 1.12, 0]))
            self.play(FadeIn(title, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(sub, color=CHALK_YELLOW, scale_factor=1.03),
                      run_time=max(leftover(tracker, "b0"), 0.4))
            self.add_sound(self.sfx["ding"], gain=-13)

            # one small figure of each kind, with its name
            p_pts = parallelogram_frame(
                centre=np.array([BOARD_CX - 3.0, -0.85, 0]), scale=0.24)["quad"]
            r_pts = rhombus_frame(
                centre=np.array([BOARD_CX, -0.85, 0]), scale=0.30)["quad"]
            s_pts = square_frame(
                centre=np.array([BOARD_CX + 3.0, -0.85, 0]), scale=0.34)["quad"]
            figs = VGroup(
                VGroup(self.shape_sketch(p_pts, CHALK_WHITE, CHALK_CYAN,
                                         opacity=0.14),
                       board_text("PARALLELOGRAM", 13, CHALK_CYAN, "BOLD"
                                  ).move_to(np.array([BOARD_CX - 3.0, -2.05, 0]))),
                VGroup(self.shape_sketch(r_pts, CHALK_WHITE, CHALK_PINK,
                                         opacity=0.14),
                       board_text("RHOMBUS", 13, CHALK_PINK, "BOLD").move_to(
                           np.array([BOARD_CX, -2.05, 0]))),
                VGroup(self.shape_sketch(s_pts, CHALK_WHITE, CHALK_GREEN,
                                         opacity=0.14),
                       board_text("SQUARE", 13, CHALK_GREEN, "BOLD").move_to(
                           np.array([BOARD_CX + 3.0, -2.05, 0]))),
            )
            tag = board_text("Property → Missing Information → Construction",
                             17, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, 0.35, 0]))

            self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.1) for f in figs],
                                  lag_ratio=0.3),
                      run_time=min(leftover(tracker, "b1"), 1.4))
            self.appear(tag, tracker, "b1", 0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: three short lists of measurements --------------------------
    def beat1_special(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("Special Shape = Extra Information", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            cols = (BOARD_CX - 3.05, BOARD_CX, BOARD_CX + 3.05)
            names = ("PARALLELOGRAM", "RHOMBUS", "SQUARE")
            givens = (("Given:", "2 sides", "+ 1 angle"),
                      ("Given:", "2 diagonals", ""),
                      ("Given:", "1 diagonal", ""))
            asks = ("Only 3 measurements?", "Only 2 measurements?",
                    "Can this be enough?")
            props = (("Opposite angles equal;", "consecutive angles",
                      "supplementary"),
                     ("Diagonals bisect", "each other at 90°", ""),
                     ("Equal perpendicular-", "bisecting diagonals", ""))

            boxes, heads, give_txt, qmarks, prop_txt = (VGroup() for _ in range(5))
            for x, name, gv, pk in zip(cols, names, givens, props):
                box = RoundedRectangle(corner_radius=0.14, width=3.05,
                                       height=2.90, stroke_color=CHALK_WHITE,
                                       stroke_width=2.0, fill_color="#16202B",
                                       fill_opacity=0.45).move_to(
                    np.array([x, 0.30, 0]))
                head = board_text(name, 15, CHALK_YELLOW, "BOLD").move_to(
                    np.array([x, 1.50, 0]))
                # empty entries would become empty Text mobjects
                give = VGroup(*[board_text(line, 14, colour, "BOLD")
                                for line, colour in zip(gv, (CHALK_WHITE,
                                                             CHALK_CYAN,
                                                             CHALK_CYAN))
                                if line]).arrange(DOWN, buff=0.10).move_to(
                    np.array([x, 0.80, 0]))
                qm = board_text("?", 30, CHALK_PINK, "BOLD").move_to(
                    np.array([x, -0.25, 0]))
                prop = VGroup(*[board_text(line, 13, CHALK_GREEN, "BOLD")
                                for line in pk if line]
                              ).arrange(DOWN, buff=0.08).move_to(
                    np.array([x, -0.35, 0]))
                boxes.add(box)
                heads.add(head)
                give_txt.add(give)
                qmarks.add(qm)
                prop_txt.add(prop)

            question = board_text(asks[0], 14, CHALK_WHITE, "BOLD").move_to(
                np.array([cols[0], -0.85, 0]))
            question2 = board_text(asks[1], 14, CHALK_WHITE, "BOLD").move_to(
                np.array([cols[1], -0.85, 0]))
            question3 = board_text(asks[2], 14, CHALK_WHITE, "BOLD").move_to(
                np.array([cols[2], -0.85, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(boxes), LaggedStart(*[
                FadeIn(h, shift=UP * 0.08) for h in heads], lag_ratio=0.2),
                run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(give_txt[0]), FadeIn(qmarks[0]), FadeIn(question),
                      run_time=0.6)
            self.wait(leftover(tracker, "b0b"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(give_txt[1]), FadeIn(qmarks[1]), FadeIn(question2),
                      run_time=0.6)
            self.wait(leftover(tracker, "b1"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(give_txt[2]), FadeIn(qmarks[2]), FadeIn(question3),
                      run_time=0.6)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["click"], gain=-15)

            # the property is the key: each question mark turns into one
            self.play(*[FadeOut(q) for q in qmarks],
                      *[FadeIn(p, shift=UP * 0.08) for p in prop_txt],
                      *[FadeOut(q) for q in (question, question2, question3)],
                      run_time=min(leftover(tracker, "b3"), 1.2))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: parallelogram, find the missing angles ---------------------
    def beat2_parallelogram(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("Use the Properties First", 21, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            d = parallelogram_frame()
            B, E, L, T = d["quad"]
            names = self.vertex_letters(
                (B, E, L, T), ((-0.10, -0.28), (0.12, -0.30), (0.30, 0.10),
                               (-0.30, 0.10)), letters="BELT")
            quad = self.shape_sketch((B, E, L, T), CHALK_WHITE, CHALK_WHITE,
                                     width=2.2, opacity=0.08)
            card_be = self.column_card(measure_card(r"BE=4.2\text{ cm}", CHALK_CYAN), 1.55)
            card_el = self.column_card(measure_card(r"EL=5\text{ cm}", CHALK_CYAN), 0.95)
            card_t = self.column_card(degree_card(r"\angle T = 45^\circ",
                                                  CHALK_YELLOW), 0.35)
            # the angle at T is between the sides T L and T B -- T E is the
            # diagonal and does not bound it
            ang_t = angle_mark(T, L, B, radius=0.46, color=CHALK_YELLOW,
                               label=None)
            ang_t_lab = board_text("45°", 15, CHALK_YELLOW, "BOLD").move_to(
                np.array(T, dtype=float) + 1.05 * unit(
                    (dir_deg(T, L) + dir_deg(T, B)) / 2.0))
            note_opp = self.column_note("Opposite angles\nare equal", -0.55,
                                       color=CHALK_YELLOW)
            ang_e = angle_mark(E, B, L, radius=0.46, color=CHALK_YELLOW,
                               label=None)
            ang_e_lab = board_text("45°", 15, CHALK_YELLOW, "BOLD").move_to(
                np.array(E, dtype=float) + 0.90 * unit(
                    (dir_deg(E, B) + dir_deg(E, L)) / 2.0))
            note_sup = self.column_note("Consecutive angles\nadd to 180°", -1.25,
                                       color=CHALK_PINK)
            calc = self.column_card(value_card(r"180^\circ - 45^\circ = "
                                               r"135^\circ", CHALK_PINK), -2.15)
            ang_l = angle_mark(L, E, T, radius=0.50, color=CHALK_PINK,
                               label="135°")
            ang_b = angle_mark(B, E, T, radius=0.50, color=CHALK_PINK,
                               label="135°")
            allfour = board_text("45°, 135°, 45°, 135° — from one given angle",
                                 17, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(quad), FadeIn(names), FadeIn(card_be),
                      FadeIn(card_el), FadeIn(card_t), run_time=0.8)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(ang_t), FadeIn(ang_t_lab), run_time=0.5)
            self.wait(leftover(tracker, "b1"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(note_opp), FadeIn(ang_e), FadeIn(ang_e_lab),
                      run_time=min(leftover(tracker, "b2"), 0.9))
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(note_sup), FadeIn(calc),
                      FadeIn(ang_l),
                      run_time=min(leftover(tracker, "b3"), 0.9))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(ang_b), run_time=0.4)
            self.wait(leftover(tracker, "b4"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(allfour, shift=UP * 0.08),
                      Circumscribe(quad, color=CHALK_AMBER, stroke_width=3,
                                   time_width=0.5),
                      run_time=min(leftover(tracker, "b5"), 1.1))
            self.wait(leftover(tracker, "b5"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: construct the parallelogram --------------------------------
    def beat3_construct_belt(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 2 — Build Triangle BEL", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            d = parallelogram_frame()
            B, E, L, T = d["quad"]
            names = self.vertex_letters(
                (B, E), ((-0.10, -0.28), (0.12, -0.30)), letters="BE")
            be = Line(B, E, color=CHALK_YELLOW, stroke_width=4.2)
            lab_be = board_text("4.2 cm", 15, CHALK_YELLOW, "BOLD").move_to(
                (B + E) / 2 + DOWN * 0.30)
            lab_e = board_text("45°", 15, CHALK_YELLOW, "BOLD").move_to(
                np.array(E, dtype=float) + 0.86 * unit(
                    (d["eb_deg"] + d["el_deg"]) / 2.0))
            ray_el = self.ray_line(E, d["el_deg"], dist(E, L),
                                   CHALK_AMBER, 3.2)
            l_dot = Dot(radius=0.10, color=CHALK_YELLOW).move_to(L)
            # radially clear of the arc that marks L
            l_name = board_text("L", 17, CHALK_WHITE, "BOLD").move_to(
                L + 0.42 * unit(d["el_deg"]))
            el = Line(E, L, color=CHALK_YELLOW, stroke_width=4.0)
            lab_el = side_label(E, L, B, "5 cm", CHALK_YELLOW, 15, 0.20)
            tri = Polygon(B, E, L, color=CHALK_CYAN, stroke_width=2.6,
                          fill_color=CHALK_CYAN, fill_opacity=0.16)
            card_be = self.column_card(measure_card(r"BE=4.2\text{ cm}", CHALK_CYAN), 1.55)
            card_el = self.column_card(measure_card(r"EL=5\text{ cm}", CHALK_CYAN), 0.95)
            note_tri = self.column_note("Triangle B E L is fixed\nby S.A.S.",
                                        -0.10)
            # outside the figure: the triangle's own diagonal runs through
            # the middle of both 135 degree corners
            lab_b = board_text("135°", 15, CHALK_PINK, "BOLD").move_to(
                np.array(B, dtype=float) + 1.30 * unit(-35.0))
            lab_l = board_text("135°", 15, CHALK_PINK, "BOLD").move_to(
                np.array(L, dtype=float) + 1.00 * unit(20.0))
            t_dot = Dot(radius=0.10, color=CHALK_YELLOW).move_to(T)
            t_name = board_text("T", 17, CHALK_WHITE, "BOLD").move_to(
                T + np.array([-0.30, 0.10, 0]))
            quad = Polygon(B, E, L, T, color=CHALK_CYAN, stroke_width=2.4,
                           fill_color=CHALK_CYAN, fill_opacity=0.10)
            done = board_text("PARALLELOGRAM COMPLETE", 16, CHALK_GREEN, "BOLD"
                              ).move_to(np.array([3.05, -1.85, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.wait(leftover(tracker, "b0"))

            self.play(Create(be), FadeIn(names), FadeIn(lab_be), FadeIn(card_be),
                      run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b1"))

            self.setout_arm(E, d["eb_deg"], d["el_deg"], dist(E, L) * 0.55,
                            0.52, CHALK_AMBER)
            self.play(self.arm_sweep.animate.set_value(1.0), run_time=min(
                leftover(tracker, "b2"), 0.9))
            self.play(Transform(self.arm, ray_el), FadeIn(lab_e),
                      run_time=min(leftover(tracker, "b2"), 0.5))
            self.play(FadeOut(self.arm_arc), run_time=0.25)
            self.compass_on(E, L, dist(E, L), 10, CHALK_GREEN,
                            hinge_dir=(1.0, -1.0, 0.0), leg_ratio=0.55)
            self.sweep_compass(tracker, "b2", 10)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(FadeIn(l_dot, scale=0.5), FadeIn(l_name), Create(el),
                      FadeIn(lab_el), FadeIn(card_el), FadeIn(tri),
                      FadeIn(note_tri),
                      run_time=min(leftover(tracker, "b3"), 1.1))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b3"))

            self.setout_arm(B, d["be_deg"], d["ebt_deg"], dist(B, T) * 0.62,
                            0.60, CHALK_PINK)
            self.play(self.arm_sweep.animate.set_value(1.0), run_time=min(
                leftover(tracker, "b4"), 0.9))
            self.play(Transform(self.arm,
                                self.ray_line(B, d["ebt_deg"],
                                              dist(B, T) * 1.05, CHALK_PINK,
                                              3.0)),
                      FadeIn(lab_b), run_time=min(leftover(tracker, "b4"), 0.5))
            self.play(FadeOut(self.arm_arc), run_time=0.25)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b4"))

            self.setout_arm(L, d["le_deg"], d["lt_deg"], dist(L, T) * 0.62,
                            0.60, CHALK_PINK)
            self.play(self.arm_sweep.animate.set_value(1.0), run_time=min(
                leftover(tracker, "b5"), 0.9))
            self.play(Transform(self.arm,
                                self.ray_line(L, d["lt_deg"],
                                              dist(L, T) * 1.05, CHALK_PINK,
                                              3.0)),
                      FadeIn(lab_l), run_time=min(leftover(tracker, "b5"), 0.5))
            self.play(FadeOut(self.arm_arc), run_time=0.25)

            self.play(FadeIn(t_dot, scale=0.5), FadeIn(t_name), FadeIn(quad),
                      FadeIn(done, shift=UP * 0.08),
                      Circumscribe(t_dot, color=CHALK_YELLOW,
                                   stroke_width=2.6),
                      run_time=min(leftover(tracker, "b5"), 1.2))
            self.wait(leftover(tracker, "b5"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)
    # -- Scene 4: the rhombus diagonal properties ----------------------------
    def beat4_rhombus_props(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()

            heading = board_text("RHOMBUS ABCD — Read the Diagonals", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            r = rhombus_frame()
            A, B, C, D = r["quad"]
            O = mid(A, C)
            names = self.vertex_letters(
                (A, B, C, D), ((-0.30, 0.02), (0.06, 0.26), (0.26, 0.02),
                               (0.06, -0.34)))
            ac = Line(A, C, color=CHALK_YELLOW, stroke_width=4.0)
            bd = Line(B, D, color=CHALK_PINK, stroke_width=4.0)
            o_dot = Dot(radius=0.09, color=CHALK_GREEN).move_to(O)
            o_name = board_text("O", 15, CHALK_GREEN, "BOLD").move_to(
                O + np.array([-0.36, -0.34, 0]))
            quad = self.shape_sketch((A, B, C, D), CHALK_WHITE, CHALK_WHITE,
                                     width=2.2, opacity=0.08)
            card_ac = self.column_card(measure_card(r"AC=4.5\text{ cm}", CHALK_YELLOW), 1.75)
            card_bd = self.column_card(measure_card(r"BD=6\text{ cm}", CHALK_PINK), 1.15)
            right = angle_mark(O, C, B, radius=0.26, color=CHALK_GREEN,
                               right_angle=True)
            right_lab = board_text("90°", 13, CHALK_GREEN, "BOLD").move_to(
                O + np.array([0.50, 0.44, 0]))
            note_perp = self.column_note("Diagonals are\nperpendicular", 0.35,
                                         color=CHALK_GREEN)
            mid_ticks = VGroup(
                Line(O + np.array([-0.06, 0.20, 0]),
                     O + np.array([0.06, 0.20, 0]), color=CHALK_WHITE,
                     stroke_width=2.4),
                Line(O + np.array([-0.06, -0.20, 0]),
                     O + np.array([0.06, -0.20, 0]), color=CHALK_WHITE,
                     stroke_width=2.4),
                Line(O + np.array([0.20, -0.06, 0]),
                     O + np.array([0.20, 0.06, 0]), color=CHALK_WHITE,
                     stroke_width=2.4),
                Line(O + np.array([-0.20, -0.06, 0]),
                     O + np.array([-0.20, 0.06, 0]), color=CHALK_WHITE,
                     stroke_width=2.4))
            note_bis = self.column_note("Diagonals bisect\neach other", -0.45,
                                        color=CHALK_WHITE)
            boxed = self.column_card(value_card(
                r"OB = OD = \tfrac{6}{2} = 3\text{ cm}", CHALK_GREEN), -1.35)
            strip = board_text("BISECT + PERPENDICULAR", 16, CHALK_GREEN, "BOLD"
                               ).move_to(np.array([BOARD_CX + 0.45, -2.50, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(quad), FadeIn(names), Create(ac), Create(bd),
                      FadeIn(o_dot), FadeIn(o_name), FadeIn(card_ac),
                      FadeIn(card_bd), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(right), FadeIn(right_lab), FadeIn(note_perp),
                      run_time=min(leftover(tracker, "b1"), 0.8))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            self.play(FadeIn(mid_ticks), FadeIn(note_bis),
                      run_time=min(leftover(tracker, "b2"), 0.8))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b2"))

            self.play(Indicate(mid_ticks, color=CHALK_WHITE,
                               scale_factor=1.15),
                      run_time=min(leftover(tracker, "b3"), 0.7))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b3"))

            self.play(FadeIn(boxed, shift=UP * 0.08),
                      FadeIn(strip, shift=UP * 0.08),
                      run_time=min(leftover(tracker, "b4"), 0.8))
            self.wait(leftover(tracker, "b4"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: construct the rhombus --------------------------------------
    def beat5_construct_rhombus(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 2 — Draw A C and Its Bisector", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            r = rhombus_frame()
            A, B, C, D = r["quad"]
            O = mid(A, C)
            names = self.vertex_letters(
                (A, C), ((-0.30, 0.02), (0.26, 0.02)), letters="AC")
            ac = Line(A, C, color=CHALK_YELLOW, stroke_width=4.2)
            # left of the perpendicular, clear of the compasses' legs
            lab_ac = board_text("4.5 cm", 15, CHALK_YELLOW, "BOLD").move_to(
                (A + C) / 2 + np.array([-0.78, -0.28, 0]))
            o_dot = Dot(radius=0.09, color=CHALK_GREEN).move_to(O)
            o_name = board_text("O", 15, CHALK_GREEN, "BOLD").move_to(
                O + np.array([-0.32, 0.30, 0]))
            card_ac = self.column_card(measure_card(r"AC=4.5\text{ cm}", CHALK_YELLOW), 1.55)
            perp_end_a, perp_end_b = perpendicular_ends(
                O, r["ac_deg"], dist(O, B) * 1.22)
            perp = DashedLine(perp_end_a, perp_end_b, color=CHALK_WHITE,
                              stroke_width=2.2, dash_length=0.16)
            note_perp = self.column_note("The perpendicular\nthrough O", 0.55)
            card_3 = self.column_card(value_card(r"\tfrac{6}{2} = 3\text{ cm}",
                                                 CHALK_GREEN), -0.35)
            b_dot = Dot(radius=0.10, color=CHALK_YELLOW).move_to(B)
            b_name = board_text("B", 17, CHALK_WHITE, "BOLD").move_to(
                B + np.array([0.34, 0.26, 0]))
            d_dot = Dot(radius=0.10, color=CHALK_YELLOW).move_to(D)
            d_name = board_text("D", 17, CHALK_WHITE, "BOLD").move_to(
                D + np.array([0.34, -0.34, 0]))
            sides = VGroup(
                Line(A, B, color=CHALK_GREEN, stroke_width=4.0),
                Line(B, C, color=CHALK_GREEN, stroke_width=4.0),
                Line(C, D, color=CHALK_GREEN, stroke_width=4.0),
                Line(D, A, color=CHALK_GREEN, stroke_width=4.0))
            quad = Polygon(A, B, C, D, color=CHALK_CYAN, stroke_width=2.4,
                           fill_color=CHALK_CYAN, fill_opacity=0.10)
            done = board_text("RHOMBUS COMPLETE", 16, CHALK_GREEN, "BOLD"
                              ).move_to(np.array([3.05, -1.45, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(Create(ac), FadeIn(names), FadeIn(lab_ac), FadeIn(o_dot),
                      FadeIn(o_name), FadeIn(card_ac), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(Create(perp), FadeIn(note_perp), run_time=min(
                leftover(tracker, "b1"), 0.8))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            # the compasses carry half of B D to both sides of O
            self.compass_on(O, B, dist(O, B), 12, CHALK_GREEN,
                            hinge_dir=(-1.0, 1.0, 0.0), leg_ratio=0.5)
            self.sweep_compass(tracker, "b2", 12, put_down=False)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(FadeIn(b_dot, scale=0.5), FadeIn(b_name),
                      FadeIn(card_3), run_time=min(
                          leftover(tracker, "b3"), 0.8))
            self.compass_on(O, D, dist(O, D), 12, CHALK_GREEN,
                            hinge_dir=(1.0, -1.0, 0.0), leg_ratio=0.5)
            self.sweep_compass(tracker, "b3", 12)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(FadeIn(d_dot, scale=0.5), FadeIn(d_name),
                      run_time=min(leftover(tracker, "b4"), 0.8))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b4"))

            self.play(Create(sides), FadeIn(quad), FadeIn(done, shift=UP * 0.08),
                      Circumscribe(quad, color=CHALK_AMBER, stroke_width=3,
                                   time_width=0.5),
                      run_time=min(leftover(tracker, "b5"), 1.2))
            self.wait(leftover(tracker, "b5"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: from rhombus to square -------------------------------------
    def beat6_square(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("From Rhombus to Square", 21, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            r = rhombus_frame()
            A, B, C, D = r["quad"]
            O = mid(A, C)
            names = self.vertex_letters(
                (A, B, C, D), ((-0.30, 0.02), (0.06, 0.26), (0.26, 0.02),
                               (0.06, -0.34)))
            rh = VGroup(
                Polygon(A, B, C, D, color=CHALK_WHITE, stroke_width=2.4,
                        fill_color=CHALK_CYAN, fill_opacity=0.10),
                Line(A, C, color=CHALK_YELLOW, stroke_width=3.6),
                Line(B, D, color=CHALK_PINK, stroke_width=3.6))
            sq = square_frame(centre=RHOMB_CENTRE, scale=RHOMB_SCALE, diag=6.0)
            J, M_, U, P_ = sq["quad"]
            sq_group = VGroup(
                Polygon(J, M_, U, P_, color=CHALK_WHITE, stroke_width=2.4,
                        fill_color=CHALK_GREEN, fill_opacity=0.10),
                Line(J, U, color=CHALK_YELLOW, stroke_width=3.6),
                Line(M_, P_, color=CHALK_PINK, stroke_width=3.6))
            ask = board_text("What if both diagonals are equal?", 17,
                             CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX + 0.85, -2.68, 0]))
            note_sq = self.column_note("Equal diagonals, bisecting\nat right "
                                       "angles: a square", 0.55, color=CHALK_GREEN)
            card_sq = self.column_card(value_card(r"4.2 \div 2 = 2.1\text{ cm}",
                                                  CHALK_GREEN), -0.45)
            # the exercise construction
            s = square_frame()
            J2, M2, U2, P2 = s["quad"]
            O2 = mid(J2, U2)
            perp_a, perp_b = perpendicular_ends(O2, s["ju_deg"],
                                                dist(O2, M2) * 1.05)
            perp = DashedLine(perp_a, perp_b, color=CHALK_WHITE,
                              stroke_width=2.2, dash_length=0.16)
            o2_dot = Dot(radius=0.09, color=CHALK_GREEN).move_to(O2)
            o2_name = board_text("O", 15, CHALK_GREEN, "BOLD").move_to(
                O2 + np.array([-0.32, 0.30, 0]))
            m_dot = Dot(radius=0.10, color=CHALK_YELLOW).move_to(M2)
            p_dot = Dot(radius=0.10, color=CHALK_YELLOW).move_to(P2)
            u_dot = Dot(radius=0.10, color=CHALK_YELLOW).move_to(U2)
            j_dot = Dot(radius=0.10, color=CHALK_YELLOW).move_to(J2)
            j_name = board_text("J", 17, CHALK_WHITE, "BOLD").move_to(
                J2 + np.array([-0.30, 0.02, 0]))
            u_name = board_text("U", 17, CHALK_WHITE, "BOLD").move_to(
                U2 + np.array([0.26, 0.02, 0]))
            m_name = board_text("M", 17, CHALK_WHITE, "BOLD").move_to(
                M2 + np.array([0.06, 0.26, 0]))
            p_name = board_text("P", 17, CHALK_WHITE, "BOLD").move_to(
                P2 + np.array([0.06, -0.34, 0]))
            ju = Line(J2, U2, color=CHALK_YELLOW, stroke_width=4.2)
            lab_ju = board_text("4.2 cm", 15, CHALK_YELLOW, "BOLD").move_to(
                (J2 + U2) / 2 + np.array([-0.62, -0.52, 0]))
            jump = VGroup(Line(J2, M2, color=CHALK_GREEN, stroke_width=4.0),
                          Line(M2, U2, color=CHALK_GREEN, stroke_width=4.0),
                          Line(U2, P2, color=CHALK_GREEN, stroke_width=4.0),
                          Line(P2, J2, color=CHALK_GREEN, stroke_width=4.0))
            jump_quad = Polygon(J2, M2, U2, P2, color=CHALK_CYAN,
                                stroke_width=2.4, fill_color=CHALK_CYAN,
                                fill_opacity=0.10)
            done = board_text("SQUARE COMPLETE", 16, CHALK_GREEN, "BOLD"
                              ).move_to(np.array([3.05, -1.45, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(rh), FadeIn(names), run_time=0.8)
            self.play(FadeIn(ask, shift=UP * 0.08), run_time=min(
                leftover(tracker, "b0"), 0.6))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(Transform(rh, sq_group), FadeOut(names),
                      run_time=min(
                leftover(tracker, "b1"), 1.4))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.wait(leftover(tracker, "b1"))

            self.play(FadeIn(note_sq), FadeIn(card_sq), run_time=min(
                leftover(tracker, "b2"), 0.7))
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["ding"], gain=-13)

            # the exercise: square J U M P from its diagonal
            self.play(FadeOut(rh), FadeOut(ask), FadeOut(note_sq),
                      FadeOut(card_sq), run_time=0.5)
            self.play(Create(ju), FadeIn(j_dot), FadeIn(u_dot), FadeIn(j_name),
                      FadeIn(u_name), FadeIn(lab_ju), FadeIn(o2_dot),
                      FadeIn(o2_name), run_time=0.9)
            self.play(Create(perp), run_time=min(
                leftover(tracker, "b3"), 0.8))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b3"))

            self.compass_on(O2, M2, dist(O2, M2), 12, CHALK_GREEN,
                            hinge_dir=(-1.0, 1.0, 0.0), leg_ratio=0.5)
            self.sweep_compass(tracker, "b4", 12, put_down=False)
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(FadeIn(m_dot, scale=0.5), FadeIn(m_name),
                      run_time=min(leftover(tracker, "b4"), 0.7))
            self.compass_on(O2, P2, dist(O2, P2), 12, CHALK_GREEN,
                            hinge_dir=(1.0, -1.0, 0.0), leg_ratio=0.5)
            self.sweep_compass(tracker, "b4", 12)
            self.play(FadeIn(p_dot, scale=0.5), FadeIn(p_name),
                      run_time=min(leftover(tracker, "b4"), 0.7))
            self.wait(leftover(tracker, "b4"))

            self.play(Create(jump), FadeIn(jump_quad),
                      FadeIn(done, shift=UP * 0.08),
                      Circumscribe(jump_quad, color=CHALK_AMBER,
                                   stroke_width=3, time_width=0.5),
                      run_time=min(leftover(tracker, "b5"), 1.2))
            self.wait(leftover(tracker, "b5"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: three shapes, three property strategies --------------------
    def beat7_compare(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("Which Property Unlocks the Construction?", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            cols = (BOARD_CX - 3.0, BOARD_CX, BOARD_CX + 3.0)
            names = ("PARALLELOGRAM", "RHOMBUS", "SQUARE")
            colors = (CHALK_CYAN, CHALK_PINK, CHALK_GREEN)
            keys = (("Opposite angles equal", "consecutive angles",
                     "sum to 180°"),
                    ("Diagonals bisect", "each other at 90°", ""),
                    ("Equal diagonals,", "perpendicular", "bisectors", ""))
            effects = (("→ the missing angles",),
                       ("→ every vertex from", "the diagonals"),
                       ("→ one more condition",))

            heads, figs, keys_txt, eff_txt = (VGroup() for _ in range(4))
            for i, (x, name, col) in enumerate(zip(cols, names, colors)):
                heads.add(board_text(name, 15, col, "BOLD").move_to(
                    np.array([x, 2.20, 0])))
                if i == 0:
                    pts = parallelogram_frame(centre=np.array([x, 1.00, 0]),
                                              scale=0.22)["quad"]
                elif i == 1:
                    pts = rhombus_frame(centre=np.array([x, 1.00, 0]),
                                        scale=0.26)["quad"]
                else:
                    pts = square_frame(centre=np.array([x, 1.00, 0]),
                                       scale=0.30)["quad"]
                figs.add(Polygon(*pts, color=CHALK_WHITE, stroke_width=2.2,
                                 fill_color=col, fill_opacity=0.12))
                keys_txt.add(VGroup(*[board_text(line, 13, col, "BOLD")
                                      for line in keys[i] if line]).arrange(
                    DOWN, buff=0.08).move_to(np.array([x, -0.30, 0])))
                eff_txt.add(VGroup(*[board_text(line, 13, CHALK_WHITE, "BOLD")
                                     for line in effects[i]]).arrange(
                    DOWN, buff=0.06).move_to(np.array([x, -1.10, 0])))

            question = board_text("So which property gives the missing "
                                  "information?", 17, CHALK_YELLOW, "BOLD"
                                  ).move_to(np.array([BOARD_CX, -1.95, 0]))
            flow = board_text("Given + Special Property → New Information → "
                              "Construction", 16, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(heads), run_time=0.7)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(figs[0], shift=UP * 0.08), FadeIn(keys_txt[0]),
                      FadeIn(eff_txt[0]), run_time=min(
                          leftover(tracker, "b1"), 0.9))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            self.play(FadeIn(figs[1], shift=UP * 0.08), FadeIn(keys_txt[1]),
                      FadeIn(eff_txt[1]), run_time=min(
                          leftover(tracker, "b2"), 0.9))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeIn(figs[2], shift=UP * 0.08), FadeIn(keys_txt[2]),
                      FadeIn(eff_txt[2]), run_time=min(
                          leftover(tracker, "b3"), 0.9))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b3"))

            self.play(FadeIn(question, shift=UP * 0.08), run_time=min(
                leftover(tracker, "b4"), 0.6))
            self.play(FadeIn(flow, shift=UP * 0.08), run_time=min(
                leftover(tracker, "b4"), 0.6))
            self.wait(leftover(tracker, "b4"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the method -------------------------------------------------
    def beat8_method(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("Analyse Before You Draw", 23, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            steps = VGroup(
                combo_card("1. IDENTIFY", "parallelogram? rhombus? square?",
                           CHALK_CYAN),
                combo_card("2. RECALL", "its angles, sides, diagonals",
                           CHALK_GREEN),
                combo_card("3. DERIVE", "180 - 45 = 135   or   6 / 2 = 3",
                           CHALK_PINK),
                combo_card("4. CONSTRUCT", "with ruler, compasses, protractor",
                           CHALK_YELLOW),
            ).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to(
                np.array([2.85, 0.55, 0]))
            flow = board_text("Shape → Property → Derived Measurement → "
                              "Construction", 16, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))
            # a small worked reminder on the left
            r = rhombus_frame(centre=np.array([BOARD_CX - 2.6, 0.45, 0]),
                              scale=0.32)
            A, B, C, D = r["quad"]
            O = mid(A, C)
            sketch = VGroup(
                Polygon(A, B, C, D, color=CHALK_WHITE, stroke_width=2.2,
                        fill_color=CHALK_WHITE, fill_opacity=0.06),
                Line(A, C, color=CHALK_YELLOW, stroke_width=2.8),
                Line(B, D, color=CHALK_PINK, stroke_width=2.8),
                Dot(radius=0.07, color=CHALK_GREEN).move_to(O),
                board_text("6 / 2 = 3", 14, CHALK_GREEN, "BOLD").move_to(
                    np.array([BOARD_CX - 2.6, -1.35, 0])))
            note = board_text("The property supplies\nwhat was not given", 15,
                              CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX - 2.6, -2.05, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(steps), run_time=1.1)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(sketch, shift=UP * 0.08), run_time=min(
                leftover(tracker, "b1"), 0.8))
            self.play(FadeIn(note, shift=UP * 0.08), run_time=min(
                leftover(tracker, "b1"), 0.5))
            self.wait(leftover(tracker, "b1"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(flow, shift=UP * 0.1),
                      Circumscribe(steps[1], color=CHALK_GREEN,
                                   stroke_width=2.4, time_width=0.6),
                      run_time=min(leftover(tracker, "b2"), 1.0))
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
            tag = board_text("Property first — construction second", 15,
                             CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, 2.24, 0]))

            # challenge A: a parallelogram whose angle A really is 65 degrees
            ca_c = np.array([BOARD_CX - 3.05, 0.30, 0])
            a4 = np.array([0.0, 0.0, 0.0])
            b4 = ray_point(a4, 0.0, 4.0)
            d4 = ray_point(a4, 65.0, 4.5)
            c4 = b4 + (d4 - a4)
            A1, B1, C1, D1 = to_board((a4, b4, c4, d4), ca_c, 0.34)
            qa = Polygon(A1, B1, C1, D1, color=CHALK_WHITE, stroke_width=2.2,
                         fill_color=CHALK_CYAN, fill_opacity=0.10)
            na = self.vertex_letters(
                (A1, B1, C1, D1), ((-0.24, -0.24), (0.10, -0.26), (0.24, 0.10),
                                   (-0.24, 0.10)))
            ang_a = angle_mark(A1, B1, D1, radius=0.30, color=CHALK_YELLOW,
                               label="65°")
            hand_a = board_text("A parallelogram with angle A = 65°", 15,
                                CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX - 3.05, -1.35, 0]))
            ask_a = board_text("What are the other three angles?", 15,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX - 3.05, -1.85, 0]))
            ans_a = board_text("65°, 115°, 115°", 16, CHALK_GREEN, "BOLD"
                               ).move_to(np.array([BOARD_CX - 3.05, -2.40, 0]))

            # challenge B: a rhombus with diagonals 8 and 6
            rb = rhombus_frame(centre=np.array([BOARD_CX + 2.55, 0.30, 0]),
                               scale=0.42, ac=8.0, bd=6.0)
            A2, B2, C2, D2 = rb["quad"]
            O2 = mid(A2, C2)
            qb = Polygon(A2, B2, C2, D2, color=CHALK_WHITE, stroke_width=2.2,
                         fill_color=CHALK_PINK, fill_opacity=0.10)
            diag_b = VGroup(Line(A2, C2, color=CHALK_YELLOW, stroke_width=3.0),
                            Line(B2, D2, color=CHALK_PINK, stroke_width=3.0))
            o2_dot = Dot(radius=0.08, color=CHALK_GREEN).move_to(O2)
            o2_name = board_text("O", 14, CHALK_GREEN, "BOLD").move_to(
                O2 + np.array([0.20, 0.14, 0]))
            hand_b = board_text("A rhombus: AC = 8 cm, BD = 6 cm", 15,
                                CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX + 2.55, -1.35, 0]))
            ask_b = board_text("How far is each vertex from O?", 15,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX + 2.55, -1.85, 0]))
            half_labels = VGroup(
                board_text("4 cm", 14, CHALK_YELLOW, "BOLD").move_to(
                    mid(O2, A2) + np.array([0.0, -0.30, 0])),
                board_text("4 cm", 14, CHALK_YELLOW, "BOLD").move_to(
                    mid(O2, C2) + np.array([0.0, -0.30, 0])),
                board_text("3 cm", 14, CHALK_PINK, "BOLD").move_to(
                    mid(O2, B2) + np.array([0.42, 0.0, 0])),
                board_text("3 cm", 14, CHALK_PINK, "BOLD").move_to(
                    mid(O2, D2) + np.array([0.42, 0.0, 0])))
            ans_b = board_text("OA = OC = 4 cm, OB = OD = 3 cm", 15,
                               CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX + 2.55, -2.40, 0]))
            pause = board_text("Pause and work them out.", 17, CHALK_YELLOW,
                               "BOLD").move_to(
                np.array([BOARD_CX, -2.70, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(tag), run_time=0.4)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(qa), FadeIn(na), FadeIn(ang_a), FadeIn(hand_a),
                      FadeIn(ask_a), run_time=0.8)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b1"))

            self.play(FadeIn(qb), FadeIn(diag_b), FadeIn(o2_dot),
                      FadeIn(o2_name), FadeIn(hand_b), FadeIn(ask_b),
                      run_time=0.8)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeIn(pause, shift=UP * 0.08), run_time=0.5)
            self.wait(leftover(tracker, "b3"))

            self.challenge = {"qa": qa, "na": na, "ang_a": ang_a, "hand_a": hand_a,
                              "ask_a": ask_a, "qb": qb, "diag_b": diag_b,
                              "o2_dot": o2_dot, "o2_name": o2_name,
                              "hand_b": hand_b, "ask_b": ask_b, "pause": pause,
                              "half": half_labels, "ans_a": ans_a, "ans_b": ans_b,
                              "pts_a": (A1, B1, C1, D1), "pts_b": (A2, B2, C2, D2)}
            self._capture_srt(tracker)

        play_challenge_countdown(self, seconds=4, sfx=self.sfx,
                                 position=np.array([BOARD_CX, BOARD_CY, 0]))

        with self.voiceover(text=NARRATION["scene9_reveal"]) as tracker:
            ch = self.challenge
            A1, B1, C1, D1 = ch["pts_a"]
            A2, B2, C2, D2 = ch["pts_b"]
            O2 = mid(A2, C2)

            self.play(FadeOut(ch["pause"]), FadeOut(ch["ang_a"]),
                      run_time=0.4)
            self.wait(leftover(tracker, "b0"))
            self.add_sound(self.sfx["pop"], gain=-13)

            # the parallelogram's four angles
            angs = VGroup(
                angle_mark(A1, B1, D1, radius=0.26, color=CHALK_YELLOW,
                           label="65°"),
                angle_mark(B1, A1, C1, radius=0.26, color=CHALK_GREEN,
                           label="115°"),
                angle_mark(C1, B1, D1, radius=0.26, color=CHALK_GREEN,
                           label="115°"),
                angle_mark(D1, A1, C1, radius=0.26, color=CHALK_YELLOW,
                           label="65°"))
            self.play(FadeIn(angs), run_time=min(leftover(tracker, "b1"), 1.2))
            self.play(FadeIn(ch["ans_a"], shift=UP * 0.06), run_time=min(
                leftover(tracker, "b1"), 0.5))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b1"))

            # the rhombus's half-diagonals
            right = angle_mark(O2, C2, B2, radius=0.22, color=CHALK_GREEN,
                               right_angle=True)
            sides_b = VGroup(
                Line(A2, B2, color=CHALK_GREEN, stroke_width=3.0),
                Line(B2, C2, color=CHALK_GREEN, stroke_width=3.0),
                Line(C2, D2, color=CHALK_GREEN, stroke_width=3.0),
                Line(D2, A2, color=CHALK_GREEN, stroke_width=3.0))
            self.play(FadeIn(right), FadeIn(ch["half"]), run_time=min(
                leftover(tracker, "b2"), 1.0))
            self.play(FadeIn(ch["ans_b"], shift=UP * 0.06), run_time=min(
                leftover(tracker, "b2"), 0.5))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b2"))

            self.play(Create(sides_b), run_time=min(leftover(tracker, "b3"), 1.0))
            self.play(Circumscribe(ch["qb"], color=CHALK_AMBER, stroke_width=3,
                                   time_width=0.5),
                      run_time=min(leftover(tracker, "b3"), 0.8))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap -----------------------------------------------------
    def beat10_recap(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("Know the Shape. Use Its Properties.", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            cols = (BOARD_CX - 3.0, BOARD_CX, BOARD_CX + 3.0)
            names = ("PARALLELOGRAM", "RHOMBUS", "SQUARE")
            colors = (CHALK_CYAN, CHALK_PINK, CHALK_GREEN)
            props = (("Opposite angles equal,", "consecutive angles add to 180°"),
                     ("Diagonals bisect", "at right angles"),
                     ("Equal perpendicular-", "bisecting diagonals"))
            figs, prop_txt, name_txt = (VGroup() for _ in range(3))
            for i, (x, name, col) in enumerate(zip(cols, names, colors)):
                name_txt.add(board_text(name, 14, col, "BOLD").move_to(
                    np.array([x, 2.18, 0])))
                if i == 0:
                    pts = parallelogram_frame(centre=np.array([x, 1.10, 0]),
                                              scale=0.22)["quad"]
                elif i == 1:
                    pts = rhombus_frame(centre=np.array([x, 1.10, 0]),
                                        scale=0.26)["quad"]
                else:
                    pts = square_frame(centre=np.array([x, 1.10, 0]),
                                       scale=0.30)["quad"]
                figs.add(Polygon(*pts, color=CHALK_WHITE, stroke_width=2.2,
                                 fill_color=col, fill_opacity=0.12))
                prop_txt.add(VGroup(*[board_text(line, 13, col, "BOLD")
                                      for line in props[i]]).arrange(
                    DOWN, buff=0.08).move_to(np.array([x, -0.35, 0])))
            chain = board_text("Special properties → missing measurements → "
                               "construction", 16, CHALK_GREEN, "BOLD"
                               ).move_to(np.array([BOARD_CX, -1.45, 0]))
            chain_box = SurroundingRectangle(chain, color=CHALK_GREEN, buff=0.16,
                                             corner_radius=0.1, stroke_width=2.4)
            final = board_text("Know the Shape. Use Its Properties. Construct "
                               "It.", 17, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.15, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(name_txt), FadeIn(figs), run_time=0.8)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(prop_txt[0]), run_time=min(
                leftover(tracker, "b1"), 0.6))
            self.wait(leftover(tracker, "b1"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(prop_txt[1]), FadeIn(prop_txt[2]),
                      run_time=min(leftover(tracker, "b2"), 0.7))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.play(FadeIn(chain, shift=UP * 0.08), Create(chain_box),
                      FadeIn(final, shift=UP * 0.08), run_time=min(
                          leftover(tracker, "b2"), 0.7))
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["success"], gain=-11)

            summary = VGroup(name_txt, figs, prop_txt, chain, chain_box, final)
            thanks = board_text("Thank You for Watching!", 40, CHALK_WHITE,
                                "BOLD")
            thanks2 = board_text("See you in the next lesson :)", 25,
                                 CHALK_CYAN)
            thanks_group = VGroup(thanks, thanks2).arrange(
                DOWN, buff=0.3).move_to(np.array([BOARD_CX, BOARD_CY, 0]))
            self.play(FadeOut(summary), FadeOut(heading), run_time=0.4)
            self.play(FadeIn(thanks, shift=UP * 0.1), run_time=0.5)
            self.add_sound(self.sfx["success"], gain=-11)
            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(thanks2, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b4"))
            self.play(Circumscribe(thanks_group, color=CHALK_AMBER,
                                   stroke_width=3, time_width=0.5),
                      run_time=0.25)
            self.play(Indicate(thanks, color=CHALK_WHITE, scale_factor=1.01),
                      run_time=rt(tracker.get_remaining_duration()))
            self._capture_srt(tracker)

        self.wait(END_HOLD)

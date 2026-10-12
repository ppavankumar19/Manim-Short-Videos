"""
How to Construct a Quadrilateral Given 3 Sides and 2 Diagonals
Story-mode chalkboard lesson (Telangana Class 8 Maths, Chapter 3:
Construction of Quadrilaterals, Storymode 04).

LLM KEY / FUNCTION NAME: construct_quadrilateral_3sides_2diagonals

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
  - Every construction arc is drawn by a pair of compasses (hinge, legs,
    needle, pencil) -- both arcs of each pair, never one.

The defining visual: the five measurements are sorted 3 + 2.  Two sides and the
diagonal A C (all three known) build triangle A B C by S.S.S; the remaining
side C D and the other diagonal B D then locate D on the far side of A C.  The
fifth side, A D, is never given -- the construction fixes it.

Title + 10 scenes:
  0. Title card.
  1. The five given measurements sorted into 3 sides and 2 diagonals.
  2. Rough sketch: find the triangle whose three lengths are known.
  3. The 3 + 2 plan: "3 build, 2 locate".
  4. Draw the diagonal A C and set the compasses to A B = 4.5.
  5. The second arc fixes B -- triangle A B C complete.
  6. The side C D and the diagonal B D locate D on the far side of A C.
  7. Complete A B C D and verify all five measurements.
  8. The reusable method (and why A B D cannot be built first).
  9. Your turn: Exercise 3.3(a) -- quadrilateral G O L D.
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


SCALE = 0.56            # board units per centimetre of the textbook drawing
AC_Y = -0.40            # the diagonal AC is drawn level, at this height
                        # (this quadrilateral is tall: the apex B reaches 4.5 cm
                        # above AC, so the base sits lower than in storyboard 03)


def example_frame(origin=None, scale=SCALE, base_y=None):
    """Textbook Example 5, built the way the construction builds it.

    A C = 5 cm is a diagonal and the shared side of the two triangles.  B is
    the point with A B = 4.5 and B C = 5.2 above it (so triangle A B C is fixed
    by its three sides), and D is the point with B D = 5.4 and C D = 4.8 on the
    other side of A C -- the textbook's instruction.  A D is never given."""
    if origin is None:
        y = AC_Y if base_y is None else base_y
        origin = np.array([BOARD_CX - 1.6, y, 0.0])
    A = np.array(origin, dtype=float)
    C = A + np.array([5.0 * scale, 0.0, 0.0])
    B = circle_intersection(A, 4.5 * scale, C, 5.2 * scale, upper=True)
    D = circle_intersection(B, 5.4 * scale, C, 4.8 * scale, upper=False)
    return A, B, C, D


def side_label(p1, p2, centroid, text, color=CHALK_CYAN, size=17,
               offset=0.22):
    """A length label placed clear of its own side.

    Overrides the version earlier in this file, which pushed the label along
    the centroid -> midpoint direction: that direction is not perpendicular to
    the side, so the label was moved by less than the half-extent it actually
    needs and a tall side (this quadrilateral's A B is 66 degrees) ran straight
    through its own label.  Here the push is along the true outward normal."""
    lab = board_text(text, size, color, "BOLD")
    p1 = np.array(p1, dtype=float)
    p2 = np.array(p2, dtype=float)
    mid = (p1 + p2) / 2.0
    d = p2 - p1
    n = np.array([-d[1], d[0], 0.0])
    n = n / (np.linalg.norm(n[:2]) or 1.0)
    if np.dot(n, mid - np.array(centroid, dtype=float)) < 0:
        n = -n
    half = (abs(n[0]) * lab.width + abs(n[1]) * lab.height) / 2.0
    return lab.move_to(mid + n * (half + offset))


def practice_frame(origin=None, scale=0.34, base_y=-0.25):
    """Exercise 3.3(a): quadrilateral G O L D.

    O L = 7.5, L D = 5 and D G = 5.5 with the diagonal G L = 6 build triangle
    G L D by S.S.S; the diagonal O D = 10 and the side O L = 7.5 then locate O
    on the far side of G L.  G O is not given.  O hangs well below the
    diagonal, so this figure is drawn a little smaller than the example: at
    0.34 the two locating arcs still finish inside the board.  It sits a little
    right of the board's left edge (BOARD_CX - 2.3) so that it reads as centred
    in the left half instead of hugging the margin."""
    if origin is None:
        y = base_y if base_y is None else base_y
        origin = np.array([BOARD_CX - 2.3, y, 0.0])
    G = np.array(origin, dtype=float)
    L = G + np.array([6.0 * scale, 0.0, 0.0])
    D = circle_intersection(G, 5.5 * scale, L, 5.0 * scale, upper=True)
    O = circle_intersection(L, 7.5 * scale, D, 10.0 * scale, upper=False)
    return G, O, L, D


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
        "How do we construct a quadrilateral when we are given three sides and "
        "two diagonals?<bookmark mark='b0'/> There is no angle and no fourth "
        "side, so first we must sort the measurements and find a triangle we "
        "can build.<bookmark mark='b1'/>"
    ),
    "scene1": (
        "Here is our problem.<bookmark mark='b0'/> Three sides: A B is four "
        "point five centimetres, B C is five point two, and C D is four point "
        "eight.<bookmark mark='b0b'/> And two diagonals: A C is five "
        "centimetres, and B D is five point four.<bookmark mark='b1'/> Three "
        "sides and two diagonals: that is the measurement set.<bookmark "
        "mark='b2'/> So which three should we use first?<bookmark mark='b3'/>"
    ),
    "scene2": (
        "A diagonal joins opposite corners, so it belongs to a triangle."
        "<bookmark mark='b0'/> "
        "Look at the triangle A B C: we know A B is four point five, B C is "
        "five point two, and the diagonal A C is five.<bookmark mark='b1'/> "
        "Three known lengths, all in one triangle.<bookmark mark='b2'/> So "
        "triangle A B C can be built first, by side, side, side."
        "<bookmark mark='b3'/>"
    ),
    "scene3": (
        "That is the whole plan.<bookmark mark='b0'/> Three measurements build "
        "the first triangle: two sides and the diagonal between them."
        "<bookmark mark='b1'/> The other two measurements, the side C D and the "
        "diagonal B D, locate the fourth vertex.<bookmark mark='b2'/> Three "
        "build, and two locate.<bookmark mark='b3'/>"
    ),
    "scene4": (
        "Let us construct it accurately.<bookmark mark='b0'/> Draw the diagonal "
        "A C, five centimetres long, and label the ends A and C.<bookmark "
        "mark='b1'/> Set the compasses to four point five centimetres, the "
        "length of A B,<bookmark mark='b2'/> and put the needle at A. Every "
        "point on this arc is four point five centimetres from A, so B lies "
        "somewhere on it.<bookmark mark='b3'/>"
    ),
    "scene5": (
        "Now set the compasses to five point two centimetres and put the needle "
        "at C.<bookmark mark='b0'/> Draw the second arc, and where the two arcs "
        "cross, that point is B.<bookmark mark='b1'/> Join A to B and B to C: "
        "triangle A B C is fixed by its three sides.<bookmark mark='b2'/>"
    ),
    "scene6": (
        "Only the fourth vertex is left.<bookmark mark='b0'/> D lies on the "
        "other side of the diagonal A C, and it must be five point four "
        "centimetres from B and four point eight centimetres from C."
        "<bookmark mark='b1'/> So set the compasses to five point four, the "
        "diagonal B D, and draw an arc about B.<bookmark mark='b2'/> Then set "
        "them to four point eight, the side C D, and draw an arc about C."
        "<bookmark mark='b3'/> Where those two arcs cross is D: one diagonal "
        "and one side have located it.<bookmark mark='b4'/>"
    ),
    "scene7": (
        "Now we finish the figure.<bookmark mark='b0'/> Join C to D, join the "
        "diagonal B to D, and join A to D to close the quadrilateral."
        "<bookmark mark='b1'/> Let us check every measurement: A B is four "
        "point five, B C is five point two, C D is four point eight, the "
        "diagonal A C is five, and the diagonal B D is five point four. All "
        "five are used.<bookmark mark='b2'/> And A D was never given: the "
        "construction decided it.<bookmark mark='b3'/>"
    ),
    "scene8": (
        "This is the method, and it works for every problem of this kind."
        "<bookmark mark='b0'/> First sketch the figure and mark what is given. "
        "Then find the triangle whose three lengths are all known, and build "
        "that one. Then use the remaining side and diagonal as radii, and "
        "intersect those arcs. Finally join the last sides, and verify."
        "<bookmark mark='b1'/> Could we have started with triangle A B D "
        "instead? No: A D is not given, so that triangle has only two known "
        "sides.<bookmark mark='b2'/>"
    ),
    "scene9_setup": (
        "Your turn.<bookmark mark='b0'/> In quadrilateral G O L D, G L is six "
        "centimetres, L D is five centimetres, D G is five point five "
        "centimetres, O L is seven point five centimetres, and the diagonal "
        "O D is ten centimetres.<bookmark mark='b1'/> Which triangle should you "
        "construct first?<bookmark mark='b2'/> Pause the video and decide."
        "<bookmark mark='b3'/>"
    ),
    "scene9_reveal": (
        "Let us check.<bookmark mark='b0'/> The diagonal is G L, so the two "
        "triangles are G O L and G L D.<bookmark mark='b1'/> In triangle G L D "
        "we know G L is six, L D is five, and D G is five point five: three "
        "known lengths, so triangle G L D comes first.<bookmark mark='b2'/> "
        "Then O is found by two arcs: radius seven point five about L, and "
        "radius ten about D. Where they cross is O, and the quadrilateral "
        "G O L D is complete.<bookmark mark='b3'/>"
    ),
    "scene10": (
        "Let us put the method together.<bookmark mark='b0'/> Two sides and one "
        "diagonal build the first triangle.<bookmark mark='b1'/> One side and "
        "one diagonal locate the fourth vertex, as the intersection of two "
        "arcs.<bookmark mark='b2'/> Triangle first, then the missing vertex."
        "<bookmark mark='b3'/> Thank you for watching!<bookmark mark='b4'/> See "
        "you in the next lesson!<bookmark mark='b5'/>"
    ),
}


class ConstructQuadrilateral3Sides2DiagonalsStory(VoiceoverScene):
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
        out_dir = _HERE / "media" / "videos" / "construct_quadrilateral_3sides_2diagonals"
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
        self.beat2_choose()
        self.beat3_plan()
        self.beat4_diagonal()
        self.beat5_triangle()
        self.beat6_locate_d()
        self.beat7_complete()
        self.beat8_method()
        self.beat9_challenge()
        self.beat10_recap()

        self._write_real_srt()

    # ================================================================ beats ==

    def compass_on(self, centre, target, radius, spread, color,
                   hinge_dir=None, leg_ratio=0.62, bias: float = 0.0):
        """Put a pair of compasses on the board with its needle on `centre` and
        its pencil at the start of the arc, ready to sweep.

        The sector is centred on the direction of `target` (so the arc really
        passes through the point being located); `bias` rotates the whole
        sector by that many degrees when one tail of a symmetric arc would
        stray over the figure or off the board."""
        C = np.array(centre, dtype=float)
        ang = float(np.degrees(np.arctan2(target[1] - C[1], target[0] - C[0])))
        start = ang - spread + bias
        sweep = ValueTracker(0.004)

        def tip_at():
            a = (start + sweep.get_value()) * DEGREES
            return C + radius * np.array([np.cos(a), np.sin(a), 0.0])

        arc = always_redraw(lambda: Arc(
            radius=radius, start_angle=start * DEGREES,
            angle=max(sweep.get_value(), 0.004) * DEGREES, arc_center=C,
            color=color, stroke_width=2.8))
        tool = always_redraw(lambda: compass_tool(
            C, tip_at(), hinge_dir=hinge_dir, leg_ratio=leg_ratio))
        self.add(arc, tool)
        self.arc, self.tool, self.sweep = arc, tool, sweep
        return sweep

    def put_down_tool(self, tool, run_time: float = 0.3) -> None:
        """Lay a pair of compasses down on the desk.

        The tool is an `always_redraw` mobject: its updater rebuilds it at full
        opacity on every frame, so `FadeOut` on the live object never shows and
        the compasses stayed standing on the board over the finished drawing.
        Fade a static copy instead and drop the live one."""
        snap = tool.copy()
        snap.clear_updaters()
        self.remove(tool)
        self.add(snap)
        self.play(FadeOut(snap), run_time=run_time)

    def sweep_compass(self, tracker, mark: str, spread: float,
                      put_down: bool = True, reserve: float = 0.0,
                      hold: bool = True) -> None:
        """Sweep the compasses already on the board to the end of the arc, then
        (by default) lay them down -- all inside the current window.  `reserve`
        keeps that many seconds of the window for the animation that follows
        (a note appearing, the second arc of the pair), and `hold=False` leaves
        that remainder to the caller instead of waiting it out."""
        budget = leftover(tracker, mark)
        sweep_time = max(budget - (0.35 if put_down else 0.0) - reserve, 0.4)
        self.play(self.sweep.animate.set_value(2 * spread), run_time=sweep_time)
        if put_down:
            self.put_down_tool(self.tool)
        if hold:
            self.wait(leftover(tracker, mark))

    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Construct a Quadrilateral", 33, CHALK_WHITE,
                               "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 1.85, 0]))
            sub = board_text("Three Sides and Two Diagonals", 20,
                             CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 0.95, 0]))
            self.play(FadeIn(title, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(sub, color=CHALK_YELLOW, scale_factor=1.04),
                      run_time=max(leftover(tracker, "b0"), 0.4))
            self.add_sound(self.sfx["ding"], gain=-13)

            # the defining measurements of THIS case are the two diagonals
            A, B, C, D = example_frame(origin=np.array([BOARD_CX - 1.0, -0.72, 0]),
                                       scale=0.26)
            outline = Polygon(A, B, C, D, color=CHALK_WHITE, stroke_width=2.2,
                              fill_color=CHALK_WHITE, fill_opacity=0.05)
            outline.set_stroke(opacity=0.45)
            diag = VGroup(Line(A, C, color=CHALK_YELLOW, stroke_width=3.0),
                          Line(B, D, color=CHALK_AMBER, stroke_width=3.0))
            names = diamond_names(A, B, C, D, "ABCD", 14, pull=0.05)
            tag = board_text("Analyse → Triangle → Arcs → Join", 18,
                             CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))
            self.play(FadeIn(outline), FadeIn(names), run_time=min(
                leftover(tracker, "b1"), 1.0))
            self.play(Create(diag), run_time=0.8)
            self.play(Flash(diag, color=CHALK_YELLOW, flash_radius=0.7),
                      run_time=0.6)
            self.appear(tag, tracker, "b1", 0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: three sides and two diagonals ------------------------------
    def beat1_data(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("Three Sides and Two Diagonals", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            # each caption sits directly above its own row with the same
            # ~0.2 gap, so "2 diagonals" can no longer read as part of the
            # three-side row above it
            lab_sides = board_text("3 sides", 17, CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX, 2.20, 0]))
            sides = VGroup(
                measure_card(r"AB=4.5", CHALK_CYAN),
                measure_card(r"BC=5.2", CHALK_CYAN),
                measure_card(r"CD=4.8", CHALK_CYAN),
            ).arrange(RIGHT, buff=0.30).move_to(
                np.array([BOARD_CX, 1.68, 0]))
            lab_diags = board_text("2 diagonals", 17, CHALK_AMBER, "BOLD"
                                   ).move_to(np.array([BOARD_CX, 1.13, 0]))
            diags = VGroup(
                measure_card(r"AC=5", CHALK_YELLOW),
                measure_card(r"BD=5.4", CHALK_AMBER),
            ).arrange(RIGHT, buff=0.30).move_to(
                np.array([BOARD_CX, 0.60, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(lab_sides), run_time=0.35)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.12)
                                    for c in sides], lag_ratio=0.25),
                      run_time=1.0)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.wait(leftover(tracker, "b0b"))
            self.play(FadeIn(lab_diags), run_time=0.35)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.12)
                                    for c in diags], lag_ratio=0.30),
                      run_time=0.9)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b1"))

            strip = board_text("3 Sides + 2 Diagonals", 21, CHALK_GREEN, "BOLD"
                               ).move_to(np.array([BOARD_CX, -1.75, 0]))
            box = SurroundingRectangle(strip, color=CHALK_GREEN, buff=0.16,
                                       corner_radius=0.1, stroke_width=2.6)
            self.play(FadeIn(strip, shift=UP * 0.1), Create(box), run_time=0.6)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["click"], gain=-15)

            ask = board_text("Which three should we use first?", 19,
                             CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.50, 0]))
            self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: find the triangle whose three lengths are known ------------
    def beat2_choose(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("Find a Complete Triangle", 22, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            A, B, C, D = example_frame()
            full = Polygon(A, B, C, D, color=CHALK_WHITE, stroke_width=2.0,
                           fill_opacity=0.0)
            full.set_stroke(opacity=0.28)
            names = diamond_names(A, B, C, D, "ABCD", 17)
            tri = Polygon(A, B, C, color=CHALK_CYAN, stroke_width=3.0,
                          fill_color=CHALK_CYAN, fill_opacity=0.16)
            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=4.0)
            bc = Line(B, C, color=CHALK_YELLOW, stroke_width=4.0)
            diag = Line(A, C, color=CHALK_YELLOW, stroke_width=4.0)
            diamond_line = Line(B, D, color=CHALK_AMBER, stroke_width=2.6)
            diamond_line.set_stroke(opacity=0.45)
            centroid = np.array([A, B, C, D], dtype=float).mean(axis=0)
            lab_ab = side_label(A, B, centroid, "4.5", CHALK_YELLOW, 16, 0.18)
            lab_bc = side_label(B, C, centroid, "5.2", CHALK_YELLOW, 16, 0.18)
            lab_ac = board_text("AC = 5", 16, CHALK_YELLOW, "BOLD").move_to(
                (A + C) / 2 + DOWN * 0.62)
            sss = combo_card("Side + Side + Side", "three known lengths",
                              CHALK_GREEN).move_to(
                np.array([BOARD_CX + 3.1, 0.55, 0]))
            note = board_text("One diagonal turns two sides into a triangle.",
                              18, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(full), FadeIn(names), FadeIn(diamond_line),
                      run_time=0.7)
            self.play(FadeIn(tri), run_time=0.5)
            self.play(Create(ab), FadeIn(lab_ab), run_time=0.7)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(Create(bc), FadeIn(lab_bc), run_time=0.7)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            self.play(Create(diag), FadeIn(lab_ac), run_time=0.7)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeIn(sss, shift=RIGHT * 0.12), FadeIn(note, shift=UP * 0.1),
                      Circumscribe(tri, color=CHALK_CYAN, stroke_width=2.6,
                                   time_width=0.6),
                      run_time=0.9)
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: the 3 + 2 plan ---------------------------------------------
    def beat3_plan(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()

            heading = board_text("3 Build. 2 Locate.", 23, CHALK_AMBER, "BOLD"
                                 ).move_to(np.array([BOARD_CX, 2.72, 0]))
            build_cards = VGroup(
                measure_card(r"AB=4.5", CHALK_YELLOW),
                measure_card(r"BC=5.2", CHALK_YELLOW),
                measure_card(r"AC=5", CHALK_YELLOW),
            ).arrange(DOWN, buff=0.22).move_to(
                np.array([BOARD_CX - 2.6, 0.55, 0]))
            locate_cards = VGroup(
                measure_card(r"CD=4.8", CHALK_CYAN),
                measure_card(r"BD=5.4", CHALK_AMBER),
            ).arrange(DOWN, buff=0.22).move_to(
                np.array([BOARD_CX + 2.7, 0.75, 0]))
            lab_build = board_text("BUILD", 18, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX - 2.6, 1.85, 0]))
            lab_locate = board_text("LOCATE", 18, CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX + 2.7, 1.75, 0]))
            tri = Polygon(np.array([-0.7, -1.4, 0]), np.array([0.05, 0.35, 0]),
                          np.array([0.8, -1.4, 0]), color=CHALK_CYAN,
                          stroke_width=2.6, fill_color=CHALK_CYAN,
                          fill_opacity=0.16)
            tri.move_to(np.array([BOARD_CX - 2.6, -1.45, 0]))
            tri.scale(0.65)
            d_dot = Dot(radius=0.09, color=CHALK_YELLOW).move_to(
                np.array([BOARD_CX + 2.7, -1.0, 0]))
            d_lab = board_text("D", 17, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX + 2.95, -1.0, 0]))
            flow = board_text("3 measurements → triangle → 2 measurements → D",
                              17, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.45, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(lab_build), run_time=0.35)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.12)
                                    for c in build_cards], lag_ratio=0.25),
                      run_time=1.0)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(Create(tri), run_time=0.8)
            self.wait(leftover(tracker, "b1"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(lab_locate), run_time=0.35)
            self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.12)
                                    for c in locate_cards], lag_ratio=0.30),
                      run_time=0.9)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeIn(d_dot, scale=0.5), FadeIn(d_lab),
                      Circumscribe(d_dot, color=CHALK_YELLOW, fade_out=True),
                      run_time=0.7)
            self.play(FadeIn(flow, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: draw the diagonal and the first arc ------------------------
    def beat4_diagonal(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 1 — Draw the Diagonal AC", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            A, B, C, D = example_frame()
            base = Line(A, C, color=CHALK_WHITE, stroke_width=4.5)
            names = VGroup(vertex_label("A", A, "UL"), vertex_label("C", C, "DR"))
            lab_ac = board_text("AC = 5 cm", 17, CHALK_CYAN, "BOLD").move_to(
                (A + C) / 2 + DOWN * 0.62)
            note = board_text("Every point on this arc is 4.5 cm from A.", 18,
                              CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(Create(base), FadeIn(names), FadeIn(lab_ac), run_time=0.8)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.wait(leftover(tracker, "b1"))
            self.compass_on(A, B, 4.5 * SCALE, 17, CHALK_CYAN,
                            hinge_dir=(1.0, -1.0, 0.0))
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.sweep_compass(tracker, "b3", 17, reserve=0.5, hold=False)
            self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: the second arc fixes B -------------------------------------
    def beat5_triangle(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 2 — Complete the Triangle", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            A, B, C, D = example_frame()
            base = Line(A, C, color=CHALK_WHITE, stroke_width=4.5)
            names = VGroup(vertex_label("A", A, "UL"), vertex_label("C", C, "DR"))
            lab_ac = board_text("AC = 5 cm", 17, CHALK_CYAN, "BOLD").move_to(
                (A + C) / 2 + DOWN * 0.62)
            arc_a = locating_arc(A, B, 4.5 * SCALE, 17, CHALK_CYAN)
            b_dot = Dot(radius=0.09, color=CHALK_YELLOW).move_to(B)
            # directly above B, in the wedge the two arcs open upwards: the
            # series' up-right slot put the letter on the arcs themselves
            b_name = board_text("B", 18, CHALK_WHITE, "BOLD").move_to(
                B + np.array([0.0, 0.30, 0]))
            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=4.0)
            bc = Line(B, C, color=CHALK_YELLOW, stroke_width=4.0)
            tri = Polygon(A, B, C, color=CHALK_CYAN, stroke_width=2.6,
                          fill_color=CHALK_CYAN, fill_opacity=0.16)
            centroid = np.array([A, B, C, D], dtype=float).mean(axis=0)
            lab_ab = side_label(A, B, centroid, "AB = 4.5 cm", CHALK_YELLOW, 16,
                                0.18)
            lab_bc = side_label(C, B, B + C - centroid, "BC = 5.2 cm",
                                CHALK_YELLOW, 16, 0.18)
            note = board_text("Three sides fix this triangle.", 19, CHALK_GREEN,
                              "BOLD").move_to(np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(Create(base), FadeIn(names), FadeIn(lab_ac), run_time=0.8)
            self.play(Create(arc_a), run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.compass_on(C, B, 5.2 * SCALE, 15, CHALK_GREEN,
                            hinge_dir=(1.0, 1.0, 0.0))
            self.sweep_compass(tracker, "b1", 15)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(FadeIn(b_dot, scale=0.5), FadeIn(b_name),
                      Indicate(b_dot, color=CHALK_YELLOW, scale_factor=1.9),
                      run_time=min(leftover(tracker, "b2"), 1.0))
            self.play(Create(ab), FadeIn(lab_ab), Create(bc), FadeIn(lab_bc),
                      run_time=min(leftover(tracker, "b2"), 1.2))
            self.play(FadeIn(tri), run_time=0.6)
            self.play(FadeIn(note, shift=UP * 0.1),
                      Flash(tri, color=CHALK_CYAN, flash_radius=0.7),
                      run_time=0.8)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: the side and the diagonal locate D -------------------------
    def beat6_locate_d(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 3 — Locate D", 22, CHALK_AMBER, "BOLD"
                                 ).move_to(np.array([BOARD_CX, 2.72, 0]))
            A, B, C, D = example_frame()
            tri = Polygon(A, B, C, color=CHALK_CYAN, stroke_width=2.4,
                          fill_color=CHALK_CYAN, fill_opacity=0.14)
            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=3.4)
            bc = Line(B, C, color=CHALK_YELLOW, stroke_width=3.4)
            diag = Line(A, C, color=CHALK_YELLOW, stroke_width=4.0)
            names = VGroup(vertex_label("A", A, "UL", CHALK_WHITE, 17),
                           vertex_label("B", B, "UR", CHALK_WHITE, 17),
                           vertex_label("C", C, "DR", CHALK_WHITE, 17))
            # the two distances that locate D, on cards: a label hung on the
            # B -> D radius landed on the A B side of the triangle
            rad_b = radius_line(B, D, CHALK_AMBER)
            rad_c = radius_line(C, D, CHALK_PINK)
            card_bd = measure_card(r"BD=5.4", CHALK_AMBER, 16).move_to(
                np.array([BOARD_CX + 2.75, -0.55, 0]))
            card_bd_lab = board_text("diagonal BD", 15, CHALK_AMBER, "BOLD"
                                     ).move_to(np.array([BOARD_CX + 2.75, -1.02, 0]))
            card_cd = measure_card(r"CD=4.8", CHALK_PINK, 16).move_to(
                np.array([BOARD_CX + 2.75, -1.60, 0]))
            card_cd_lab = board_text("side CD", 15, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX + 2.75, -2.07, 0]))
            d_dot = Dot(radius=0.09, color=CHALK_YELLOW).move_to(D)
            d_name = vertex_label("D", D, "DR", CHALK_WHITE).shift(
                np.array([0.14, -0.20, 0]))
            guide_c = DashedLine(C, D, color=CHALK_WHITE, stroke_width=1.8,
                                 dash_length=0.12)
            guide_a = DashedLine(A, D, color=CHALK_WHITE, stroke_width=1.8,
                                 dash_length=0.12)
            note = board_text("One diagonal and one side have located D.", 19,
                              CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.62, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(tri), FadeIn(ab), FadeIn(bc), FadeIn(diag),
                      FadeIn(names), run_time=0.8)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            # the two distances that locate D, shown before either arc
            self.play(FadeIn(rad_b), FadeIn(rad_c), FadeIn(card_bd),
                      FadeIn(card_bd_lab), FadeIn(card_cd), FadeIn(card_cd_lab),
                      run_time=0.7)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            self.compass_on(B, D, 5.4 * SCALE, 16, CHALK_AMBER,
                            hinge_dir=(1.0, 1.0, 0.0))
            self.sweep_compass(tracker, "b2", 16)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            # the tail of a symmetric arc about C would poke back over the
            # diagonal, so this sector is rotated 8 degrees further down
            self.compass_on(C, D, 4.8 * SCALE, 14, CHALK_PINK,
                            hinge_dir=(1.0, -1.0, 0.0), bias=8.0)
            self.sweep_compass(tracker, "b3", 14)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(FadeIn(d_dot, scale=0.5), FadeIn(d_name),
                      Indicate(d_dot, color=CHALK_YELLOW, scale_factor=1.9),
                      run_time=0.9)
            self.play(Create(guide_c), Create(guide_a), run_time=0.8)
            self.play(FadeIn(note, shift=UP * 0.1),
                      Flash(d_dot, color=CHALK_GREEN, flash_radius=0.6),
                      run_time=0.8)
            self.wait(leftover(tracker, "b4"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: complete the quadrilateral and verify ----------------------
    def beat7_complete(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("Required Quadrilateral ABCD", 22, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            A, B, C, D = example_frame()
            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=4.0)
            bc = Line(B, C, color=CHALK_YELLOW, stroke_width=4.0)
            diag_ac = Line(A, C, color=CHALK_YELLOW, stroke_width=3.4)
            cd = Line(C, D, color=CHALK_GREEN, stroke_width=4.0)
            bd = Line(B, D, color=CHALK_AMBER, stroke_width=3.4)
            ad = Line(A, D, color=CHALK_GREEN, stroke_width=4.0)
            quad = Polygon(A, B, C, D, color=CHALK_CYAN, stroke_width=2.2,
                           fill_color=CHALK_CYAN, fill_opacity=0.10)
            names = diamond_names(A, B, C, D, "ABCD", 17)
            checks = VGroup(
                check_row(r"AB=4.5", CHALK_GREEN, 15),
                check_row(r"BC=5.2", CHALK_GREEN, 15),
                check_row(r"CD=4.8", CHALK_GREEN, 15),
                check_row(r"AC=5", CHALK_YELLOW, 15),
                check_row(r"BD=5.4", CHALK_AMBER, 15),
            ).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX + 3.0, 0.1, 0]))
            note = board_text("AD was never given: the construction fixed it.",
                              18, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(quad), FadeIn(names), Create(ab), Create(bc),
                      Create(diag_ac), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(Create(cd), run_time=min(leftover(tracker, "b1"), 0.8))
            self.play(Create(bd), run_time=min(leftover(tracker, "b1"), 0.8))
            self.play(Create(ad), run_time=min(leftover(tracker, "b1"), 0.8))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1)
                                    for c in checks], lag_ratio=0.22),
                      run_time=min(leftover(tracker, "b2"), 1.6))
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(note, shift=UP * 0.1),
                      Circumscribe(ad, color=CHALK_GREEN, stroke_width=2.6,
                                   time_width=0.6),
                      run_time=min(leftover(tracker, "b3"), 1.0))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the reusable method ----------------------------------------
    def beat8_method(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("Analyse First", 23, CHALK_AMBER, "BOLD"
                                 ).move_to(np.array([BOARD_CX, 2.72, 0]))
            steps = VGroup(
                combo_card("1. SKETCH", "mark 3 sides + 2 diagonals", CHALK_CYAN),
                combo_card("2. FIND THE TRIANGLE", "the three known lengths",
                           CHALK_GREEN),
                combo_card("3. TWO ARCS", "side + diagonal as radii", CHALK_PINK),
                combo_card("4. JOIN", "complete and verify", CHALK_YELLOW),
            ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX - 2.3, 0.35, 0]))
            A, B, C, D = example_frame(origin=np.array([BOARD_CX + 2.3, 0.55, 0]),
                                       scale=0.28)
            mini = VGroup(
                Polygon(A, B, C, D, color=CHALK_WHITE, stroke_width=2.0,
                        fill_opacity=0.0),
                Line(A, C, color=CHALK_YELLOW, stroke_width=3.0),
                Line(B, D, color=CHALK_AMBER, stroke_width=2.4),
                Polygon(A, B, C, color=CHALK_CYAN, stroke_width=1.6,
                        fill_color=CHALK_CYAN, fill_opacity=0.18),
                locating_arc(B, D, 5.4 * 0.28, 20, CHALK_AMBER),
                locating_arc(C, D, 4.8 * 0.28, 20, CHALK_PINK),
                Dot(radius=0.07, color=CHALK_YELLOW).move_to(D),
            )
            names = diamond_names(A, B, C, D, "ABCD", 13, pull=0.05)
            note = board_text("Start with the triangle whose 3 lengths are "
                              "known.", 17, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(steps), run_time=1.2)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(mini[0]), FadeIn(names), FadeIn(mini[1]),
                      FadeIn(mini[2]), run_time=min(leftover(tracker, "b1"), 1.0))
            self.play(FadeIn(mini[3]), Create(mini[4]), Create(mini[5]),
                      FadeIn(mini[6]), run_time=min(leftover(tracker, "b1"), 1.6))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b1"))

            self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
            self.play(Circumscribe(steps[1], color=CHALK_GREEN, stroke_width=2.4,
                                   time_width=0.6),
                      run_time=min(leftover(tracker, "b2"), 1.2))
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 9: student challenge (Exercise 3.3(a)) ------------------------
    def beat9_challenge(self) -> None:
        with self.voiceover(text=NARRATION["scene9_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", 30, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, 2.62, 0]))
            tag = board_text("Exercise 3.3(a) — quadrilateral GOLD", 15,
                             CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, 2.24, 0]))
            G, O, L, D = practice_frame()
            rough = Polygon(G, O, L, D, color=CHALK_WHITE, stroke_width=2.4,
                            fill_color=CHALK_WHITE, fill_opacity=0.06)
            diag = Line(G, L, color=CHALK_YELLOW, stroke_width=3.6)
            diag2 = Line(O, D, color=CHALK_AMBER, stroke_width=3.0)
            # hand-placed: the automatic corner slots put two letters on the
            # two arcs that cross at O
            names = VGroup(
                board_text("G", 15, CHALK_WHITE, "BOLD").move_to(
                    G + np.array([-0.30, 0.02, 0])),
                board_text("O", 15, CHALK_WHITE, "BOLD").move_to(
                    O + np.array([-0.30, -0.28, 0])),
                board_text("L", 15, CHALK_WHITE, "BOLD").move_to(
                    L + np.array([0.26, -0.02, 0])),
                board_text("D", 15, CHALK_WHITE, "BOLD").move_to(
                    D + np.array([-0.02, 0.30, 0])),
            )
            cards = VGroup(
                measure_card(r"OL=7.5", CHALK_CYAN, 15),
                measure_card(r"GL=6", CHALK_YELLOW, 15),
                measure_card(r"LD=5", CHALK_CYAN, 15),
                measure_card(r"DG=5.5", CHALK_CYAN, 15),
                measure_card(r"OD=10", CHALK_AMBER, 15),
            ).arrange(DOWN, buff=0.20).move_to(
                np.array([BOARD_CX + 2.4, 0.55, 0]))
            ask = board_text("Which triangle comes first?", 18, CHALK_WHITE,
                             "BOLD").move_to(
                np.array([BOARD_CX + 0.30, -2.45, 0]))
            pause = board_text("Pause and decide.", 18, CHALK_YELLOW, "BOLD"
                               ).move_to(np.array([BOARD_CX + 2.4, -1.9, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(tag), run_time=0.4)
            self.play(FadeIn(rough), FadeIn(names), FadeIn(diag), FadeIn(diag2),
                      run_time=0.8)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.10)
                                    for c in cards], lag_ratio=0.18),
                      run_time=min(leftover(tracker, "b1"), 1.6))
            self.wait(leftover(tracker, "b1"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(ask, shift=RIGHT * 0.12), run_time=0.5)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(pause, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b3"))

            self.challenge = {"rough": rough, "names": names, "cards": cards,
                              "ask": ask, "pause": pause, "diag": diag,
                              "points": (G, O, L, D)}
            self._capture_srt(tracker)

        play_challenge_countdown(self, seconds=4, sfx=self.sfx,
                                 position=np.array([BOARD_CX + 1.35, 0.5, 0]))

        with self.voiceover(text=NARRATION["scene9_reveal"]) as tracker:
            ch = self.challenge
            G, O, L, D = ch["points"]
            names = ch["names"]

            # the question and the pause prompt have done their job: clearing
            # both leaves the bottom of the board free for the arc about L,
            # whose pencil sweeps down to y = -2.44
            self.play(FadeOut(ch["pause"]), FadeOut(ch["ask"]), run_time=0.4)
            self.wait(leftover(tracker, "b0"))
            tri = Polygon(G, L, D, color=CHALK_GREEN, stroke_width=3.0,
                          fill_color=CHALK_GREEN, fill_opacity=0.14)
            centroid = np.array([G, O, L, D], dtype=float).mean(axis=0)
            # clear of the figure, of the O -> D diagonal (which crosses G L)
            # and of both pairs of compasses: their needles sit on L and D and
            # every part of the instrument stays to the left of the figure
            lab_gl = board_text("GL = 6", 15, CHALK_GREEN, "BOLD").move_to(
                L + np.array([0.66, -0.50, 0]))
            lab_ld = side_label(L, D, centroid, "LD = 5", CHALK_GREEN, 15, 0.18)
            lab_dg = side_label(D, G, centroid, "DG = 5.5", CHALK_GREEN, 15, 0.18)
            self.play(Create(tri),
                      Circumscribe(ch["diag"], color=CHALK_YELLOW,
                                   stroke_width=2.4, time_width=0.6),
                      run_time=min(leftover(tracker, "b1"), 1.2))
            self.play(FadeIn(lab_gl), FadeIn(lab_ld), FadeIn(lab_dg),
                      run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            badge = board_text("First triangle: GLD", 18, CHALK_GREEN, "BOLD"
                               ).move_to(np.array([BOARD_CX + 2.4, -1.75, 0]))
            self.play(FadeIn(badge, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["ding"], gain=-13)

            first_tool = None
            # leg_ratio 0.52: a compass opened out for a wide arc keeps its
            # hinge near the needle-pencil line, so the instrument stays on the
            # left of the figure instead of sweeping across the L letter and
            # the G L label
            self.compass_on(L, O, 7.5 * 0.34, 14, CHALK_CYAN,
                            hinge_dir=(-1.0, -1.0, 0.0), bias=4.0,
                            leg_ratio=0.52)
            first_tool = self.tool
            # fixed sweeps, not "use the whole window": the pair of arcs, the
            # two compasses being laid down and the appearance of O all have to
            # fit inside this one narration window
            self.play(self.sweep.animate.set_value(28), run_time=2.2)
            self.compass_on(D, O, 10.0 * 0.34, 14, CHALK_PINK,
                            hinge_dir=(1.0, -1.0, 0.0), bias=4.0,
                            leg_ratio=0.52)
            self.play(self.sweep.animate.set_value(28), run_time=2.2)
            self.put_down_tool(first_tool)
            self.put_down_tool(self.tool)
            o_dot = Dot(radius=0.08, color=CHALK_YELLOW).move_to(O)
            o_name = names[1]
            quad = Polygon(G, O, L, D, color=CHALK_CYAN, stroke_width=2.4,
                           fill_color=CHALK_CYAN, fill_opacity=0.12)
            self.play(FadeIn(o_dot, scale=0.5), FadeIn(quad),
                      Indicate(o_dot, color=CHALK_YELLOW, scale_factor=2.0),
                      Circumscribe(o_name, color=CHALK_YELLOW, fade_out=True),
                      run_time=min(leftover(tracker, "b3"), 1.0))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap ------------------------------------------------------
    def beat10_recap(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("Three Sides and Two Diagonals", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            # the recap figure is nudged a little right of the left edge, so it
            # reads as centred in the left half instead of hugging the margin
            A, B, C, D = example_frame(origin=np.array([BOARD_CX - 3.35, 0.55, 0]),
                                       scale=0.30)
            diag_ac = Line(A, C, color=CHALK_YELLOW, stroke_width=3.2)
            diag_bd = Line(B, D, color=CHALK_AMBER, stroke_width=2.8)
            tri = Polygon(A, B, C, color=CHALK_YELLOW, stroke_width=3.0,
                          fill_color=CHALK_YELLOW, fill_opacity=0.16)
            quad = Polygon(A, B, C, D, color=CHALK_CYAN, stroke_width=2.2,
                           fill_color=CHALK_CYAN, fill_opacity=0.10)
            names = diamond_names(A, B, C, D, "ABCD", 15, pull=0.05)
            arc_b = locating_arc(B, D, 5.4 * 0.30, 18, CHALK_AMBER)
            arc_c = locating_arc(C, D, 4.8 * 0.30, 18, CHALK_PINK)
            d_dot = Dot(radius=0.08, color=CHALK_YELLOW).move_to(D)

            rows = VGroup(
                summary_row(1, "Two sides + one diagonal:",
                            r"\triangle ABC", CHALK_YELLOW),
                summary_row(2, "One side + one diagonal:",
                            r"D", CHALK_AMBER),
                summary_row(3, "The fifth side is fixed by the drawing:",
                            r"AD", CHALK_GREEN),
            ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX + 1.8, 1.35, 0]))
            final = board_text("3 build, 2 locate.", 18, CHALK_GREEN, "BOLD"
                               ).move_to(np.array([BOARD_CX, -1.90, 0]))
            take = board_text("Sketch, find the triangle, intersect, join.", 16,
                              CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.45, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(quad), FadeIn(names), Create(tri), Create(diag_ac),
                      Create(diag_bd), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(rows[0], shift=RIGHT * 0.12), run_time=0.5)
            self.play(Create(arc_b), Create(arc_c), FadeIn(d_dot),
                      FadeIn(rows[1], shift=RIGHT * 0.12),
                      run_time=min(leftover(tracker, "b1"), 1.6))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b1"))

            self.play(Indicate(d_dot, color=CHALK_YELLOW, scale_factor=2.0),
                      FadeIn(rows[2], shift=RIGHT * 0.12), run_time=0.8)
            self.add_sound(self.sfx["success"], gain=-11)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeIn(final, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(take),
                      Circumscribe(quad, color=CHALK_AMBER, stroke_width=3,
                                   time_width=0.5),
                      run_time=min(leftover(tracker, "b3"), 1.2))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b3"))

            summary = VGroup(quad, names, tri, diag_ac, diag_bd, arc_b, arc_c,
                             d_dot, rows, final, take)
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

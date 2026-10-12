"""
How to Construct a Quadrilateral Given 2 Adjacent Sides and 3 Angles
Story-mode chalkboard lesson (Telangana Class 8 Maths, Chapter 3:
Construction of Quadrilaterals, Storymode 05).

LLM KEY / FUNCTION NAME: construct_quadrilateral_2sides_3angles

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
  - Angles are set out the way the textbook sets them out: a protractor for the
    100 degree angle, a bisected 60/90 pair for the 75 degree angle, and the
    pair of compasses for the standard 120 degree angle.

The defining visual: the five measurements sort 3 + 2.  The two adjacent sides
P Q and Q R with the angle between them, angle Q, build triangle P Q R by
S.A.S; the remaining two angles, at P and at R, are two RAYS whose crossing is
the fourth vertex.  Where the earlier videos of this chapter located the last
vertex with two compass arcs, here it is located by two intersecting rays.

Title + 10 scenes:
  0. Title card.
  1. The five given measurements: 2 adjacent sides and 3 angles.
  2. Find the S.A.S triangle: P Q, angle Q, Q R.
  3. The 3 + 2 plan: "3 build, 2 locate".
  4. Draw P Q and set out the 100 degree angle at Q with the protractor.
  5. Measure Q R = 4.8 along that ray: triangle P Q R is fixed.
  6. The 75 degree angle at P gives the first ray -- one direction for S.
  7. The 120 degree angle at R gives the second ray: they cross at S.
  8. Complete and verify P Q R S, then the reusable method.
  9. Your turn: quadrilateral A B C D.
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


SCALE = 0.55            # board units per centimetre of the textbook drawing
PRACTICE_SCALE = 0.46
# The figure is long and narrow (S P = 7.4 cm against P Q = 4 cm), so it is
# placed a little left of centre on the board with the step column on the right.
EXAMPLE_CENTRE = np.array([BOARD_CX - 1.8, 0.05, 0.0])
PRACTICE_CENTRE = np.array([BOARD_CX - 1.9, -0.15, 0.0])


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


def ray_intersection(p1, d1, p2, d2):
    """Where the ray from `p1` at `d1` degrees meets the ray from `p2` at `d2`.

    Returns (point, t, s) with `t` and `s` the distances along each ray, so the
    caller can insist that the crossing lies *in front of* both rays -- the
    construction has no meaning otherwise."""
    p1 = np.array(p1, dtype=float)
    p2 = np.array(p2, dtype=float)
    u, v = unit(d1)[:2], unit(d2)[:2]
    a = np.array([[u[0], -v[0]], [u[1], -v[1]]])
    t, s = np.linalg.solve(a, (p2 - p1)[:2])
    return p1 + t * unit(d1), float(t), float(s)


def crossing(p1, arm1, angle1, p2, arm2, angle2):
    """`p1` and `p2` are joined by a known arm; the two remaining angles are
    set out from those arms.  The fourth vertex is the crossing that lies in
    front of both rays (the other three sign combinations point away)."""
    for s1 in (-1.0, 1.0):
        for s2 in (-1.0, 1.0):
            point, t, s = ray_intersection(p1, arm1 + s1 * angle1,
                                           p2, arm2 + s2 * angle2)
            if t > 1e-6 and s > 1e-6:
                return point, arm1 + s1 * angle1, arm2 + s2 * angle2
    raise ValueError("the two rays do not meet in front of both vertices")


def to_board(points, centre, scale):
    """Map centimetre coordinates onto the board: the figure's bounding box
    centre goes to `centre`, and one centimetre becomes `scale` board units."""
    pts = [np.array(p, dtype=float) for p in points]
    lo = np.min(np.array([p[:2] for p in pts]), axis=0)
    hi = np.max(np.array([p[:2] for p in pts]), axis=0)
    mid = (lo + hi) / 2.0
    return [np.array([centre[0] + (p[0] - mid[0]) * scale,
                      centre[1] + (p[1] - mid[1]) * scale, 0.0]) for p in pts]


def _build(p, q, side_qr, angle_q, angle_p, angle_r, centre, scale):
    """Shared construction: the S.A.S triangle first, then the crossing.

    Returns the four board points as `quad` (first, second, third = the S.A.S
    triangle, fourth = the crossing), the model-centimetre points, and every
    direction the animation needs."""
    r = ray_point(q, dir_deg(q, p) - angle_q, side_qr)
    s, ps_deg, rs_deg = crossing(p, dir_deg(p, q), angle_p,
                                 r, dir_deg(r, q), angle_r)
    a, b, c, d = to_board((p, q, r, s), centre, scale)
    return {
        "quad": (a, b, c, d),
        "model": (p, q, r, s),
        "pq_deg": dir_deg(a, b), "qr_deg": dir_deg(b, c),
        "qp_deg": dir_deg(b, a), "rq_deg": dir_deg(c, b),
        "ps_deg": dir_deg(a, d), "rs_deg": dir_deg(c, d),
        "sp_deg": dir_deg(d, a), "sr_deg": dir_deg(d, c),
        "pr_deg": dir_deg(a, c),
    }


def example_construction(centre=None, scale=SCALE):
    """Textbook Example 6, built the way the construction builds it.

    P Q = 4 cm and Q R = 4.8 cm with the angle at Q = 100 degrees fix triangle
    P Q R by S.A.S; the angles at P (75 degrees from P Q) and at R (120 degrees
    from R Q) then give two rays that cross at S.  P S and R S are not given --
    they are what the construction produces."""
    c = EXAMPLE_CENTRE if centre is None else centre
    return _build(np.array([0.0, 0.0, 0.0]), np.array([4.0, 0.0, 0.0]),
                  4.8, 100.0, 75.0, 120.0, c, scale)


def example_frame(centre=None, scale=SCALE):
    """The four vertices of Example 6 as (P, Q, R, S)."""
    return example_construction(centre, scale)["quad"]


def practice_construction(centre=None, scale=PRACTICE_SCALE):
    """Exercise data for the student challenge: A B = 5 cm, B C = 4 cm, the
    angle at B = 110 degrees, and the angles at A = 70 and at C = 120."""
    c = PRACTICE_CENTRE if centre is None else centre
    return _build(np.array([0.0, 0.0, 0.0]), np.array([5.0, 0.0, 0.0]),
                  4.0, 110.0, 70.0, 120.0, c, scale)


def practice_frame(centre=None, scale=PRACTICE_SCALE):
    """The four vertices of the practice quadrilateral as (A, B, C, D)."""
    return practice_construction(centre, scale)["quad"]


def side_label(p1, p2, centroid, text, color=CHALK_CYAN, size=17,
               offset=0.22):
    """A length label placed clear of its own side.

    Overrides the version earlier in this file, which pushed the label along
    the centroid -> midpoint direction: that direction is not perpendicular to
    the side, so the label was moved by less than the half-extent it actually
    needs and a steep side ran straight through its own label.  Here the push
    is along the true outward normal."""
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


def degree_card(label, color=CHALK_AMBER, size=17) -> VGroup:
    """A measurement card for an angle: the same look as `measure_card`, and
    LaTeX for the angle symbol -- Segoe Print has no glyph for the angle sign,
    so the card's content is typeset rather than chalk-written."""
    tex = MathTex(label, font_size=size, color=color)
    box = RoundedRectangle(corner_radius=0.08, width=tex.width + 0.46,
                           height=tex.height + 0.32, stroke_color=color,
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
        "How do we construct a quadrilateral from two adjacent sides and three "
        "angles?<bookmark mark='b0'/> Two lengths and three angles: the plan "
        "has to sort them before anything is drawn.<bookmark mark='b1'/>"
    ),
    "scene1": (
        "Here is our problem.<bookmark mark='b0'/> Two adjacent sides: P Q is "
        "four centimetres, and Q R is four point eight.<bookmark mark='b0b'/> "
        "Three angles: angle P is seventy five degrees, angle Q is one "
        "hundred, and angle R is one hundred and twenty.<bookmark mark='b1'/> "
        "Two sides and three angles.<bookmark mark='b2'/> So where do we "
        "begin?<bookmark mark='b3'/>"
    ),
    "scene2": (
        "A diagonal was not given this time.<bookmark mark='b0'/> So look for "
        "the triangle we can already build: P Q is four, Q R is four point "
        "eight, and they meet at Q.<bookmark mark='b1'/> The angle between "
        "them, angle Q, is one hundred degrees.<bookmark mark='b2'/> Side, "
        "angle, side: triangle P Q R is fixed.<bookmark mark='b3'/> The other "
        "two angles come later.<bookmark mark='b4'/>"
    ),
    "scene3": (
        "Here is the whole plan.<bookmark mark='b0'/> Three measurements build "
        "the first triangle: the side P Q, the angle Q, and the side Q "
        "R.<bookmark mark='b1'/> The other two, the angle at P and the angle "
        "at R, locate the fourth vertex.<bookmark mark='b2'/> Three build, and "
        "two locate.<bookmark mark='b3'/>"
    ),
    "scene4": (
        "Now we construct it accurately.<bookmark mark='b0'/> Draw the side P "
        "Q, four centimetres long, and label the ends P and Q.<bookmark "
        "mark='b1'/> At Q, set out an angle of one hundred degrees from Q "
        "P.<bookmark mark='b2'/> The new ray is the direction of Q R, so R "
        "must lie somewhere on it.<bookmark mark='b3'/>"
    ),
    "scene5": (
        "Set the compasses to four point eight centimetres, the length of Q "
        "R.<bookmark mark='b0'/> With the needle at Q, mark that distance "
        "along the ray.<bookmark mark='b1'/> That point is R.<bookmark "
        "mark='b2'/> Join P to R, and triangle P Q R is fixed by side, angle, "
        "side.<bookmark mark='b3'/>"
    ),
    "scene6": (
        "Only the fourth vertex is left.<bookmark mark='b0'/> At P, set out an "
        "angle of seventy five degrees from P Q, on the inside of the "
        "figure.<bookmark mark='b1'/> Every point on this ray makes seventy "
        "five degrees with P Q, so S lies somewhere on it.<bookmark "
        "mark='b2'/> An angle gives a direction, not a distance.<bookmark "
        "mark='b3'/> Seventy five degrees is half way between sixty and "
        "ninety.<bookmark mark='b4'/>"
    ),
    "scene7": (
        "Now the angle at R.<bookmark mark='b0'/> With the compasses, mark one "
        "hundred and twenty degrees from R Q<bookmark mark='b1'/> and draw the "
        "second ray.<bookmark mark='b2'/> This ray is another set of possible "
        "places for S, and the two rays cross at exactly one "
        "point.<bookmark mark='b3'/> That point is S: two directions agree "
        "there.<bookmark mark='b4'/>"
    ),
    "scene8": (
        "We finish the figure: join P to S and R to S.<bookmark mark='b0'/> "
        "Let us check every measurement: P Q is four, Q R is four point eight, "
        "angle P is seventy five degrees, angle Q is one hundred, and angle R "
        "is one hundred and twenty.<bookmark mark='b1'/> Here is the method: "
        "sketch the figure, build the side angle side triangle, draw the two "
        "remaining angle rays, and their crossing gives the last "
        "vertex.<bookmark mark='b2'/>"
    ),
    "scene9_setup": (
        "Your turn.<bookmark mark='b0'/> Construct quadrilateral A B C D: A B "
        "is five centimetres, B C is four centimetres, angle A is seventy "
        "degrees, angle B is one hundred and ten degrees, and angle C is one "
        "hundred and twenty degrees.<bookmark mark='b1'/> Which three "
        "measurements should you use first?<bookmark mark='b2'/> Pause the "
        "video and decide.<bookmark mark='b3'/>"
    ),
    "scene9_reveal": (
        "Let us check.<bookmark mark='b0'/> A B and B C are the two adjacent "
        "sides, and they meet at B.<bookmark mark='b1'/> So the triangle is A "
        "B C, built by side, angle, side.<bookmark mark='b2'/> Then the angles "
        "at A and C give two rays, and where they cross is D.<bookmark "
        "mark='b3'/>"
    ),
    "scene10": (
        "Let us put it together.<bookmark mark='b0'/> Two adjacent sides and "
        "the angle between them build the first triangle.<bookmark mark='b1'/> "
        "The other two angles give two rays, and their crossing is the fourth "
        "vertex.<bookmark mark='b2'/> Side angle side builds; angle angle "
        "locates.<bookmark mark='b3'/> Thank you for watching!<bookmark "
        "mark='b4'/> See you in the next lesson!<bookmark mark='b5'/>"
    ),
}


class ConstructQuadrilateral2Sides3AnglesStory(VoiceoverScene):
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
        out_dir = _HERE / "media" / "videos" / "construct_quadrilateral_2sides_3angles"
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
        self.beat4_build()
        self.beat5_triangle()
        self.beat6_first_ray()
        self.beat7_second_ray()
        self.beat8_complete()
        self.beat9_challenge()
        self.beat10_recap()

        self._write_real_srt()

    # ================================================================ beats ==

    # -- real SRT export -----------------------------------------------------
    def _capture_srt(self, tracker, words_per_line: int = 9) -> None:
        """Same ground-truth export as the rest of the series, with one change:
        a final chunk of one or two words is folded into the caption before it.
        A stand-alone last word keeps its own half-second caption, which lands
        mostly in silence at the end of the piece and reads badly."""
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
        """Lay a pair of compasses down on the desk.

        The tool is an `always_redraw` mobject: its updater rebuilds it at full
        opacity on every frame, so `FadeOut` on the live object never shows.
        Fade a static copy instead and drop the live one."""
        snap = tool.copy()
        snap.clear_updaters()
        self.remove(tool)
        self.add(snap)
        self.play(FadeOut(snap), run_time=run_time)

    def compass_on(self, centre, target, radius, spread, color,
                   hinge_dir=None, leg_ratio=0.62, bias: float = 0.0):
        """Park a pair of compasses with its needle on `centre` and its pencil
        at the start of the arc, ready to sweep.  `bias` rotates the whole
        sector when a symmetric arc would stray over the figure."""
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
                      hold: bool = True, seconds: float | None = None) -> None:
        """Sweep the compasses already on the board to the end of the arc."""
        budget = leftover(tracker, mark) if seconds is None else seconds
        span = 2 * spread if seconds is None else spread
        sweep_time = max(budget - (0.35 if put_down else 0.0) - reserve, 0.4)
        self.play(self.sweep.animate.set_value(span), run_time=sweep_time)
        if put_down:
            self.put_down_tool(self.tool)
        if hold and seconds is None:
            self.wait(leftover(tracker, mark))

    def setout_arm(self, vertex, start_deg, end_deg, length, radius, color,
                   stroke: float = 3.4):
        """An arm that swings from one direction to the other while the angle
        arc grows under it -- how an angle is set out on paper."""
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

    def vertex_letters(self, points, offsets, letters="PQRS", size=17,
                       color=CHALK_WHITE):
        """Vertex letters placed by hand, one offset each -- the automatic
        corners put a letter inside this elongated figure."""
        out = []
        for letter, p, off in zip(letters, points, offsets):
            shift = np.array([off[0], off[1], 0.0])
            out.append(board_text(letter, size, color, "BOLD").move_to(
                np.array(p, dtype=float) + shift))
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

    def bisect_inset(self, centre, scale=1.0):
        """A compact '75 degrees between 60 and 90' inset: the two standard
        angles, the bisector between them, and the arithmetic."""
        v = np.array(centre, dtype=float)
        base = Line(v, v + np.array([1.05, 0, 0]), color=CHALK_WHITE,
                    stroke_width=2.0)
        a60 = Line(v, v + np.array([np.cos(60 * DEGREES),
                                    np.sin(60 * DEGREES), 0]) * 0.92,
                   color=CHALK_CYAN, stroke_width=2.0)
        a90 = Line(v, v + np.array([0, 0.92, 0]), color=CHALK_AMBER,
                   stroke_width=2.0)
        bis = DashedLine(v, v + np.array([np.cos(75 * DEGREES),
                                          np.sin(75 * DEGREES), 0]) * 1.0,
                         color=CHALK_GREEN, stroke_width=2.2, dash_length=0.08)
        arc60 = Arc(radius=0.46, start_angle=0, angle=60 * DEGREES,
                    arc_center=v, color=CHALK_CYAN, stroke_width=1.6)
        arc90 = Arc(radius=0.58, start_angle=0, angle=90 * DEGREES,
                    arc_center=v, color=CHALK_AMBER, stroke_width=1.6)
        l60 = board_text("60°", 13, CHALK_CYAN, "BOLD").move_to(
            v + np.array([0.80, 0.14, 0]))
        l90 = board_text("90°", 13, CHALK_AMBER, "BOLD").move_to(
            v + np.array([-0.05, 1.16, 0]))
        l75 = board_text("75°", 13, CHALK_GREEN, "BOLD").move_to(
            v + np.array([1.05, 0.86, 0]))
        eq = board_text("75° = (60° + 90°)/2", 13, CHALK_GREEN, "BOLD"
                        ).move_to(v + np.array([1.02, -0.36, 0]))
        grp = VGroup(base, a60, a90, arc60, arc90, bis, l60, l90, l75, eq)
        grp.scale(scale, about_point=v)
        return grp

    # -- Scene 0: title ------------------------------------------------------
    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Construct a Quadrilateral", 33, CHALK_WHITE,
                               "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 1.85, 0]))
            sub = board_text("Two Sides and Three Angles", 20, CHALK_YELLOW,
                             "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 0.95, 0]))
            self.play(FadeIn(title, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(sub, color=CHALK_YELLOW, scale_factor=1.04),
                      run_time=max(leftover(tracker, "b0"), 0.4))
            self.add_sound(self.sfx["ding"], gain=-13)

            # the signature of this case: the S.A.S triangle and the two rays
            d = example_construction(
                centre=np.array([BOARD_CX + 0.35, -0.72, 0]), scale=0.24)
            P, Q, R, S = d["quad"]
            outline = Polygon(P, Q, R, S, color=CHALK_WHITE, stroke_width=2.2)
            outline.set_stroke(opacity=0.40)
            pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=3.4)
            qr = Line(Q, R, color=CHALK_YELLOW, stroke_width=3.4)
            ang_q = angle_mark(Q, P, R, radius=0.34, color=CHALK_AMBER,
                               label="100°")
            ray_p = self.ray_line(P, d["ps_deg"], dist(P, S) * 1.05,
                                  CHALK_CYAN, 2.6, True)
            ray_r = self.ray_line(R, d["rs_deg"], dist(R, S) * 1.05,
                                  CHALK_PINK, 2.6, True)
            names = self.vertex_letters(
                (P, Q, R, S), ((-0.22, -0.10), (0.10, -0.24), (0.24, 0.02),
                               (-0.08, 0.24)), size=14)
            tag = board_text("Sides → Triangle → Rays → Meet", 18, CHALK_GREEN,
                             "BOLD").move_to(np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(outline), FadeIn(names), run_time=min(
                leftover(tracker, "b1"), 0.8))
            self.play(Create(pq), Create(qr), FadeIn(ang_q), run_time=0.9)
            self.play(Create(ray_p), Create(ray_r), run_time=0.9)
            self.play(Flash(VGroup(ray_p, ray_r), color=CHALK_YELLOW,
                            flash_radius=0.6), run_time=0.5)
            self.appear(tag, tracker, "b1", 0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: two adjacent sides and three angles ------------------------
    def beat1_data(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("Two Sides and Three Angles", 22, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            lab_sides = board_text("2 adjacent sides", 17, CHALK_CYAN, "BOLD"
                                   ).move_to(np.array([BOARD_CX, 2.20, 0]))
            sides = VGroup(
                measure_card(r"PQ=4\text{ cm}", CHALK_CYAN),
                measure_card(r"QR=4.8\text{ cm}", CHALK_CYAN),
            ).arrange(RIGHT, buff=0.34).move_to(
                np.array([BOARD_CX, 1.68, 0]))
            lab_angles = board_text("3 angles", 17, CHALK_AMBER, "BOLD"
                                    ).move_to(np.array([BOARD_CX, 1.13, 0]))
            angles = VGroup(
                degree_card(r"\angle P = 75^\circ", CHALK_YELLOW),
                degree_card(r"\angle Q = 100^\circ", CHALK_AMBER),
                degree_card(r"\angle R = 120^\circ", CHALK_PINK),
            ).arrange(RIGHT, buff=0.30).move_to(
                np.array([BOARD_CX, 0.60, 0]))
            strip = board_text("S.A.S.A.A", 22, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -1.28, 0]))
            box = SurroundingRectangle(strip, color=CHALK_GREEN, buff=0.16,
                                       corner_radius=0.1, stroke_width=2.6)
            spell = board_text("Side – Angle – Side – Angle – Angle", 16,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -1.86, 0]))
            ask = board_text("Where do we begin?", 19, CHALK_WHITE, "BOLD"
                             ).move_to(np.array([BOARD_CX, -2.50, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(lab_sides), run_time=0.35)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.12)
                                    for c in sides], lag_ratio=0.28),
                      run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.wait(leftover(tracker, "b0b"))
            self.play(FadeIn(lab_angles), run_time=0.35)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.12)
                                    for c in angles], lag_ratio=0.22),
                      run_time=1.1)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b1"))

            self.play(FadeIn(strip, shift=UP * 0.1), Create(box),
                      FadeIn(spell), run_time=0.7)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: find the S.A.S triangle ------------------------------------
    def beat2_choose(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("Find the Side – Angle – Side Triangle", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            d = example_construction()
            P, Q, R, S = d["quad"]
            names = self.vertex_letters(
                (P, Q, R, S), ((-0.28, -0.10), (0.12, -0.30), (0.50, -0.40),
                               (-0.14, 0.34)))
            full = Polygon(P, Q, R, S, color=CHALK_WHITE, stroke_width=2.0)
            full.set_stroke(opacity=0.28)
            pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=4.0)
            qr = Line(Q, R, color=CHALK_YELLOW, stroke_width=4.0)
            ang_q = angle_mark(Q, P, R, radius=0.52, color=CHALK_YELLOW,
                               label="100°")
            tri = Polygon(P, Q, R, color=CHALK_CYAN, stroke_width=3.0,
                          fill_color=CHALK_CYAN, fill_opacity=0.16)
            ray_p = self.ray_line(P, d["ps_deg"], 4.40, CHALK_CYAN, 2.2, True)
            ray_r = self.ray_line(R, d["rs_deg"], 2.60, CHALK_PINK, 2.2, True)
            s_dot = Dot(radius=0.08, color=CHALK_YELLOW).move_to(S)

            c_pq = self.column_card(measure_card(r"PQ=4\text{ cm}", CHALK_YELLOW), 1.55)
            c_q = self.column_card(degree_card(r"\angle Q = 100^\circ", CHALK_YELLOW), 0.95)
            c_qr = self.column_card(measure_card(r"QR=4.8\text{ cm}", CHALK_YELLOW), 0.35)
            sas = board_text("Side – Angle – Side", 18, CHALK_GREEN, "BOLD"
                             ).move_to(np.array([3.05, -0.32, 0]))
            sas_short = board_text("S.A.S", 16, CHALK_GREEN, "BOLD").move_to(
                np.array([3.05, -0.72, 0]))
            later_lab = board_text("USE LATER", 15, CHALK_PINK, "BOLD"
                                   ).move_to(np.array([3.05, -1.15, 0]))
            later = VGroup(
                degree_card(r"\angle P = 75^\circ", CHALK_CYAN, 15),
                degree_card(r"\angle R = 120^\circ", CHALK_PINK, 15),
            ).arrange(DOWN, buff=0.18).move_to(np.array([3.05, -2.00, 0]))
            later_box = SurroundingRectangle(later, color=CHALK_PINK, buff=0.14,
                                             corner_radius=0.1,
                                             stroke_width=2.0)
            note = board_text("The included angle\ntells us the first "
                              "triangle.", 16, CHALK_WHITE, "BOLD").move_to(
                np.array([3.05, 2.26, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(full), FadeIn(names), FadeIn(ray_p), FadeIn(ray_r),
                      FadeIn(s_dot), run_time=0.8)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(Create(pq), FadeIn(c_pq), run_time=0.7)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            self.play(FadeIn(c_q), run_time=0.4)
            self.play(Create(qr), FadeIn(c_qr), FadeIn(ang_q),
                      run_time=min(leftover(tracker, "b2"), 0.9))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeIn(tri), FadeIn(sas), FadeIn(sas_short),
                      Circumscribe(tri, color=CHALK_CYAN, stroke_width=2.6,
                                   time_width=0.6),
                      run_time=min(leftover(tracker, "b3"), 1.0))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)

            self.play(FadeIn(later_lab), FadeIn(later), Create(later_box),
                      run_time=0.6)
            self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b4"))
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: the 3 + 2 plan ---------------------------------------------
    def beat3_plan(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()

            heading = board_text("3 Build. 2 Locate.", 23, CHALK_AMBER, "BOLD"
                                 ).move_to(np.array([BOARD_CX, 2.72, 0]))
            lab_build = board_text("BUILD", 18, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX - 2.5, 2.18, 0]))
            build_cards = VGroup(
                measure_card(r"PQ=4\text{ cm}", CHALK_YELLOW),
                degree_card(r"\angle Q = 100^\circ", CHALK_YELLOW),
                measure_card(r"QR=4.8\text{ cm}", CHALK_YELLOW),
            ).arrange(DOWN, buff=0.22).move_to(
                np.array([BOARD_CX - 2.5, 1.05, 0]))
            tri = Polygon(np.array([-0.62, -1.30, 0]), np.array([0.04, 0.30, 0]),
                          np.array([0.70, -1.30, 0]), color=CHALK_CYAN,
                          stroke_width=2.6, fill_color=CHALK_CYAN,
                          fill_opacity=0.16)
            tri.move_to(np.array([BOARD_CX - 2.5, -1.55, 0]))
            tri.scale(0.72)
            ang_t = angle_mark(tri.get_vertices()[0], tri.get_vertices()[1],
                               tri.get_vertices()[2], radius=0.22,
                               color=CHALK_YELLOW)

            lab_locate = board_text("LOCATE", 18, CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX + 2.6, 2.18, 0]))
            locate_cards = VGroup(
                degree_card(r"\angle P = 75^\circ", CHALK_CYAN),
                degree_card(r"\angle R = 120^\circ", CHALK_PINK),
            ).arrange(DOWN, buff=0.22).move_to(
                np.array([BOARD_CX + 2.6, 1.32, 0]))
            # a miniature of the two rays meeting
            mv = np.array([BOARD_CX + 2.6, -1.55, 0])
            m_base = Line(mv + np.array([-0.75, -0.42, 0]),
                          mv + np.array([0.80, -0.42, 0]), color=CHALK_WHITE,
                          stroke_width=2.0)
            m_ray_a = Line(mv + np.array([-0.75, -0.42, 0]),
                           mv + np.array([0.55, 0.62, 0]), color=CHALK_CYAN,
                           stroke_width=2.4)
            m_ray_b = Line(mv + np.array([0.80, -0.42, 0]),
                           mv + np.array([-0.30, 0.70, 0]), color=CHALK_PINK,
                           stroke_width=2.4)
            m_dot = Dot(radius=0.08, color=CHALK_YELLOW).move_to(
                mv + np.array([0.13, 0.05, 0]))
            m_s = board_text("S", 15, CHALK_WHITE, "BOLD").move_to(
                mv + np.array([0.48, 0.32, 0]))
            flow = board_text("3 measurements → triangle, 2 angles → rays", 17,
                              CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.45, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(lab_build), run_time=0.35)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.12)
                                    for c in build_cards], lag_ratio=0.25),
                      run_time=1.0)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(Create(tri), FadeIn(ang_t), run_time=0.8)
            self.wait(leftover(tracker, "b1"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(lab_locate), run_time=0.35)
            self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.12)
                                    for c in locate_cards], lag_ratio=0.28),
                      run_time=0.9)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b2"))

            self.play(Create(m_base), Create(m_ray_a), Create(m_ray_b),
                      FadeIn(m_dot), FadeIn(m_s), run_time=0.9)
            self.play(FadeIn(flow, shift=UP * 0.1),
                      Circumscribe(m_dot, color=CHALK_YELLOW, stroke_width=2.4),
                      run_time=min(leftover(tracker, "b3"), 1.0))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: draw P Q and set out 100 degrees at Q ----------------------
    def beat4_build(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 2 — Build Triangle PQR by S.A.S", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            d = example_construction()
            P, Q, R, S = d["quad"]
            names = self.vertex_letters(
                (P, Q), ((-0.28, -0.10), (0.12, -0.30)))
            pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=4.2)
            lab_pq = board_text("4 cm", 15, CHALK_YELLOW, "BOLD").move_to(
                (P + Q) / 2 + DOWN * 0.32)
            prot = protractor(Q, color=CHALK_AMBER, radius=0.95)
            tick_deg = d["qr_deg"]
            tick_dot = Dot(radius=0.07, color=CHALK_YELLOW).move_to(
                np.array(Q, dtype=float) + 0.95 * unit(tick_deg))
            ang_q = angle_mark(Q, P, R, radius=0.55, color=CHALK_AMBER)
            ang_lab = board_text("100°", 15, CHALK_AMBER, "BOLD").move_to(
                np.array(Q, dtype=float) + 1.30 * unit(
                    (d["qp_deg"] + tick_deg) / 2.0))
            ray_qr = self.ray_line(Q, tick_deg, dist(Q, R) * 1.10, CHALK_AMBER,
                                   3.2)
            note = self.column_note("R must lie\nsomewhere on this ray.", -0.75)
            card_pq = self.column_card(measure_card(r"PQ=4\text{ cm}", CHALK_YELLOW), 1.35)
            card_q = self.column_card(degree_card(r"\angle Q = 100^\circ", CHALK_AMBER), 0.55)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.wait(leftover(tracker, "b0"))

            self.play(Create(pq), FadeIn(names), FadeIn(lab_pq), FadeIn(card_pq),
                      run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b1"))

            # the protractor is laid on the base, the 100 degree graduation
            # marked, and the ray drawn through it
            self.play(FadeIn(prot), run_time=0.6)
            self.play(FadeIn(tick_dot, scale=0.5), run_time=0.35)
            self.play(FadeIn(ang_q), FadeIn(ang_lab), FadeIn(card_q),
                      run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeOut(prot), run_time=0.4)
            self.play(Create(ray_qr), FadeIn(note, shift=UP * 0.08),
                      run_time=min(leftover(tracker, "b3"), 1.0))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["ding"], gain=-13)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: measure 4.8 along the ray -- that point is R ---------------
    def beat5_triangle(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 2 — Complete the Triangle", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            d = example_construction()
            P, Q, R, S = d["quad"]
            names = self.vertex_letters(
                (P, Q, R), ((-0.28, -0.10), (0.12, -0.30), (0.50, -0.40)))
            pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=4.2)
            lab_pq = board_text("4 cm", 15, CHALK_YELLOW, "BOLD").move_to(
                (P + Q) / 2 + DOWN * 0.32)
            ray_qr = self.ray_line(Q, d["qr_deg"], dist(Q, R) * 1.10,
                                   CHALK_AMBER, 3.2)
            ang_q = angle_mark(Q, P, R, radius=0.55, color=CHALK_AMBER)
            ang_lab = board_text("100°", 15, CHALK_AMBER, "BOLD").move_to(
                np.array(Q, dtype=float) + 1.04 * unit(
                    (d["qp_deg"] + d["qr_deg"]) / 2.0))
            r_dot = Dot(radius=0.10, color=CHALK_YELLOW).move_to(R)
            qr = Line(Q, R, color=CHALK_YELLOW, stroke_width=4.2)
            lab_qr = side_label(Q, R, P, "4.8 cm", CHALK_YELLOW, 15, 0.20)
            pr = DashedLine(P, R, color=CHALK_WHITE, stroke_width=2.0,
                            dash_length=0.14)
            tri = Polygon(P, Q, R, color=CHALK_CYAN, stroke_width=2.6,
                          fill_color=CHALK_CYAN, fill_opacity=0.16)
            card_qr = self.column_card(measure_card(r"QR=4.8\text{ cm}", CHALK_YELLOW),
                                       1.35)
            card_q = self.column_card(degree_card(r"\angle Q = 100^\circ", CHALK_AMBER), 0.55)
            note = self.column_note("Triangle P Q R is fixed\nby S.A.S.", -0.75)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(Create(pq), FadeIn(names), FadeIn(lab_pq), FadeIn(ang_q),
                      FadeIn(ang_lab), FadeIn(ray_qr), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            # the compasses carry the 4.8 cm from the card to the ray
            self.compass_on(Q, R, dist(Q, R), 11, CHALK_GREEN,
                            hinge_dir=(1.0, -1.0, 0.0), leg_ratio=0.55)
            self.sweep_compass(tracker, "b1", 11)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(FadeIn(r_dot, scale=0.5),
                      Indicate(r_dot, color=CHALK_YELLOW, scale_factor=1.9),
                      run_time=min(leftover(tracker, "b2"), 0.8))
            self.play(Create(qr), FadeIn(lab_qr), FadeIn(card_qr),
                      run_time=min(leftover(tracker, "b2"), 0.9))
            self.play(FadeIn(card_q), run_time=0.3)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(Create(pr), FadeIn(tri), run_time=min(
                leftover(tracker, "b3"), 0.9))
            self.play(FadeIn(note, shift=UP * 0.08),
                      Flash(tri, color=CHALK_CYAN, flash_radius=0.7),
                      run_time=0.8)
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: the 75 degree angle at P gives one ray ---------------------
    def beat6_first_ray(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 3 — Set Out the Angle at P", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            d = example_construction()
            P, Q, R, S = d["quad"]
            names = self.vertex_letters(
                (P, Q, R), ((-0.28, -0.10), (0.12, -0.30), (0.50, -0.40)))
            pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=4.2)
            qr = Line(Q, R, color=CHALK_YELLOW, stroke_width=4.2)
            tri = Polygon(P, Q, R, color=CHALK_CYAN, stroke_width=2.4,
                          fill_color=CHALK_CYAN, fill_opacity=0.14)
            ang_q = angle_mark(Q, P, R, radius=0.55, color=CHALK_AMBER)
            ang_lab_q = board_text("100°", 15, CHALK_AMBER, "BOLD").move_to(
                np.array(Q, dtype=float) + 1.30 * unit(
                    (d["qp_deg"] + d["qr_deg"]) / 2.0))
            card_p = self.column_card(degree_card(r"\angle P = 75^\circ", CHALK_YELLOW),
                                      1.55)
            note = self.column_note("S could be somewhere\non this ray.", -0.30)
            inset = self.bisect_inset(np.array([2.35, -1.85, 0]), scale=0.92)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(tri), FadeIn(names), Create(pq), Create(qr),
                      FadeIn(ang_q), FadeIn(ang_lab_q), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            # the arm swings from P Q round to 75 degrees, the arc growing under
            # it: the angle is set out, not guessed
            self.setout_arm(P, d["pq_deg"], d["ps_deg"], dist(P, S) * 0.62,
                            0.80, CHALK_YELLOW)
            self.play(self.arm_sweep.animate.set_value(1.0), run_time=min(
                leftover(tracker, "b1"), 1.6))
            ang_p = board_text("75°", 15, CHALK_YELLOW, "BOLD").move_to(
                np.array(P, dtype=float) + 1.15 * unit(
                    d["ps_deg"] + 35.0))
            self.play(FadeIn(ang_p), FadeIn(card_p),
                      run_time=min(leftover(tracker, "b1"), 0.6))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            ray_p = self.ray_line(P, d["ps_deg"], dist(P, S) * 1.06, CHALK_CYAN,
                                  3.2)
            self.play(Transform(self.arm, ray_p), FadeIn(note, shift=UP * 0.08),
                      run_time=min(leftover(tracker, "b2"), 1.0))
            self.play(FadeOut(self.arm_arc), run_time=0.3)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["ding"], gain=-13)

            # a dot that can sit anywhere on the ray: an angle gives a
            # direction, not a distance
            walker = Dot(radius=0.09, color=CHALK_YELLOW).move_to(
                ray_point(P, d["ps_deg"], dist(P, S) * 0.30))
            self.play(FadeIn(walker), run_time=0.3)
            self.play(walker.animate.move_to(
                ray_point(P, d["ps_deg"], dist(P, S) * 1.02)),
                run_time=min(leftover(tracker, "b3"), 1.8))
            self.play(FadeOut(walker), run_time=0.3)
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(inset, shift=UP * 0.08), run_time=0.7)
            self.wait(leftover(tracker, "b4"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: the 120 degree angle at R, and the two rays meet -----------
    def beat7_second_ray(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 4 — The Angle at R Finds S", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            d = example_construction()
            P, Q, R, S = d["quad"]
            names = self.vertex_letters(
                (P, Q, R), ((-0.28, -0.10), (0.12, -0.30), (0.50, -0.40)))
            pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=4.2)
            qr = Line(Q, R, color=CHALK_YELLOW, stroke_width=4.2)
            tri = Polygon(P, Q, R, color=CHALK_CYAN, stroke_width=2.4,
                          fill_color=CHALK_CYAN, fill_opacity=0.14)
            ray_p = self.ray_line(P, d["ps_deg"], dist(P, S) * 1.06, CHALK_CYAN,
                                  3.2)
            ang_p = board_text("75°", 15, CHALK_YELLOW, "BOLD").move_to(
                np.array(P, dtype=float) + 1.15 * unit(
                    d["ps_deg"] + 35.0))
            card_r = self.column_card(degree_card(r"\angle R = 120^\circ", CHALK_PINK), 1.55)

            # the standard construction of 120 degrees: an arc about R, then the
            # same opening stepped round twice.  The two steps are 60 degrees
            # each, and the sign follows the interior of the angle: the chord of
            # a 60 degree step is exactly the compass opening, so the arcs of the
            # steps really do meet on the base arc.
            r_len = 1.05
            signed = ((d["rs_deg"] - d["rq_deg"] + 180.0) % 360.0) - 180.0
            step = 60.0 if signed > 0 else -60.0
            a1 = ray_point(R, d["rq_deg"], r_len)
            a2 = ray_point(R, d["rq_deg"] + step, r_len)
            a3 = ray_point(R, d["rq_deg"] + 2 * step, r_len)
            # the base arc sweeps from a3 round to a1 and passes through a2
            mid = a2
            dots = VGroup(*[Dot(radius=0.07, color=CHALK_PINK).move_to(p)
                            for p in (a1, a2, a3)])
            chord1 = Line(a1, a2, color=CHALK_PINK, stroke_width=2.0)
            chord2 = Line(a2, a3, color=CHALK_PINK, stroke_width=2.0)
            ray_r = self.ray_line(R, d["rs_deg"], dist(R, S) * 1.06, CHALK_PINK,
                                  3.2)
            s_dot = Dot(radius=0.11, color=CHALK_YELLOW).move_to(S)
            s_name = board_text("S", 17, CHALK_WHITE, "BOLD").move_to(
                S + np.array([-0.10, 0.30, 0]))
            note = self.column_note("The two rays cross\nat exactly one point.",
                                    -0.35)
            agree = board_text("Two directions agree at one point.", 17, CHALK_GREEN,
                               "BOLD").move_to(np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(tri), FadeIn(names), Create(pq), Create(qr),
                      Create(ray_p), FadeIn(ang_p), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            # the base arc, then the same opening stepped round twice: the
            # chord of each 60 degree step is exactly the opening, so the arcs
            # of the steps really do land on the base arc
            self.compass_on(R, mid, r_len, 60, CHALK_PINK,
                            hinge_dir=(1.0, 0.6, 0.0), leg_ratio=0.52)
            self.play(self.sweep.animate.set_value(120), run_time=min(
                leftover(tracker, "b1") * 0.42, 1.7))
            self.play(FadeIn(dots[0], scale=0.5), run_time=0.25)
            first = self.tool
            self.compass_on(a1, a2, r_len, 12, CHALK_PINK,
                            hinge_dir=(-1.0, -0.4, 0.0), leg_ratio=0.6)
            self.play(self.sweep.animate.set_value(24), run_time=0.75)
            self.play(FadeIn(dots[1], scale=0.5), FadeIn(chord1), run_time=0.3)
            self.compass_on(a2, a3, r_len, 12, CHALK_PINK,
                            hinge_dir=(1.0, 0.4, 0.0), leg_ratio=0.6)
            self.play(self.sweep.animate.set_value(24), run_time=0.75)
            self.play(FadeIn(dots[2], scale=0.5), FadeIn(chord2),
                      FadeOut(first), run_time=0.4)
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.wait(leftover(tracker, "b1"))

            # the ray through the 120 degree mark
            self.play(FadeIn(card_r), run_time=0.3)
            self.play(Create(ray_r), run_time=min(leftover(tracker, "b2"), 0.9))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeIn(s_dot, scale=0.5), FadeIn(s_name),
                      Indicate(s_dot, color=CHALK_YELLOW, scale_factor=2.1),
                      run_time=min(leftover(tracker, "b3"), 1.0))
            self.play(FadeIn(note, shift=UP * 0.08), run_time=0.5)
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeOut(VGroup(dots, chord1, chord2)),
                      FadeIn(agree, shift=UP * 0.1),
                      Circumscribe(s_dot, color=CHALK_GREEN, stroke_width=2.6),
                      run_time=min(leftover(tracker, "b4"), 1.0))
            self.wait(leftover(tracker, "b4"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: complete, verify, generalise -------------------------------
    def beat8_complete(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("Required Quadrilateral PQRS", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            d = example_construction()
            P, Q, R, S = d["quad"]
            names = self.vertex_letters(
                (P, Q, R, S), ((-0.28, -0.10), (0.12, -0.30), (0.50, -0.40),
                               (-0.14, 0.34)))
            pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=4.0)
            qr = Line(Q, R, color=CHALK_YELLOW, stroke_width=4.0)
            ps = Line(P, S, color=CHALK_GREEN, stroke_width=4.2)
            rs = Line(R, S, color=CHALK_GREEN, stroke_width=4.2)
            ray_p = self.ray_line(P, d["ps_deg"], dist(P, S) * 1.06, CHALK_CYAN,
                                  2.4)
            ray_r = self.ray_line(R, d["rs_deg"], dist(R, S) * 1.06, CHALK_PINK,
                                  2.4)
            quad = Polygon(P, Q, R, S, color=CHALK_CYAN, stroke_width=2.4,
                           fill_color=CHALK_CYAN, fill_opacity=0.10)
            ang_p = angle_mark(P, Q, S, radius=0.62, color=CHALK_YELLOW,
                               label="75°")
            ang_q = angle_mark(Q, P, R, radius=0.55, color=CHALK_AMBER,
                               label="100°")
            ang_r = angle_mark(R, Q, S, radius=0.62, color=CHALK_PINK,
                               label="120°")
            checks = VGroup(
                check_row(r"PQ=4\text{ cm}", CHALK_GREEN, 15),
                check_row(r"QR=4.8\text{ cm}", CHALK_GREEN, 15),
                check_row(r"75^\circ", CHALK_YELLOW, 15),
                check_row(r"100^\circ", CHALK_AMBER, 15),
                check_row(r"120^\circ", CHALK_PINK, 15),
            ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(
                np.array([3.05, 0.80, 0]))
            steps = VGroup(
                combo_card("1. SKETCH", "2 adjacent sides + 3 angles",
                           CHALK_CYAN),
                combo_card("2. SAS TRIANGLE", "the two sides and angle Q",
                           CHALK_GREEN),
                combo_card("3. TWO ANGLE RAYS", "from P and from R",
                           CHALK_PINK),
                combo_card("4. INTERSECT", "their meeting is the 4th vertex",
                           CHALK_YELLOW),
            ).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to(
                np.array([2.62, 0.35, 0]))
            flow = board_text("Sketch → SAS → Rays → Intersection", 17,
                              CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(quad), FadeIn(names), Create(pq), Create(qr),
                      FadeIn(ray_p), FadeIn(ray_r), run_time=0.8)
            self.play(Create(ps), Create(rs), run_time=min(
                leftover(tracker, "b0"), 1.0))
            self.play(FadeIn(ang_p), FadeIn(ang_q), FadeIn(ang_r),
                      run_time=min(leftover(tracker, "b0"), 1.0))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1)
                                    for c in checks], lag_ratio=0.20),
                      run_time=min(leftover(tracker, "b1"), 1.6))
            self.wait(leftover(tracker, "b1"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeOut(checks), FadeOut(ang_p), FadeOut(ang_q), FadeOut(ang_r),
                      run_time=0.5)
            self.play(FadeIn(steps), run_time=min(leftover(tracker, "b2"), 1.2))
            self.play(FadeIn(flow, shift=UP * 0.1),
                      Circumscribe(quad, color=CHALK_AMBER, stroke_width=3,
                                   time_width=0.5),
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
            tag = board_text("Quadrilateral A B C D", 15, CHALK_WHITE, "BOLD"
                             ).move_to(np.array([BOARD_CX, 2.24, 0]))
            d = practice_construction()
            A, B, C, D = d["quad"]
            names = self.vertex_letters(
                (A, B, C, D), ((-0.28, -0.10), (0.12, -0.30), (0.50, -0.40),
                               (-0.34, 0.06)), letters="ABCD")
            rough = Polygon(A, B, C, D, color=CHALK_WHITE, stroke_width=2.4,
                            fill_color=CHALK_WHITE, fill_opacity=0.06)
            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=3.4)
            bc = Line(B, C, color=CHALK_YELLOW, stroke_width=3.4)
            cards = VGroup(
                measure_card(r"AB=5\text{ cm}", CHALK_CYAN, 15),
                measure_card(r"BC=4\text{ cm}", CHALK_CYAN, 15),
                degree_card(r"\angle A = 70^\circ", CHALK_YELLOW, 15),
                degree_card(r"\angle B = 110^\circ", CHALK_AMBER, 15),
                degree_card(r"\angle C = 120^\circ", CHALK_PINK, 15),
            ).arrange(DOWN, buff=0.16).move_to(np.array([3.05, 0.75, 0]))
            ask = board_text("Which three measurements should you use "
                             "first?", 16, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX + 0.80, -2.62, 0]))
            prompt = board_text("What is their included angle?", 16,
                                CHALK_YELLOW, "BOLD").move_to(
                np.array([3.05, -1.35, 0]))
            pause = board_text("Pause and decide.", 17, CHALK_YELLOW, "BOLD"
                               ).move_to(np.array([3.05, -2.05, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(tag), run_time=0.4)
            self.play(FadeIn(rough), FadeIn(names), run_time=0.7)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.10)
                                    for c in cards], lag_ratio=0.16),
                      run_time=min(leftover(tracker, "b1"), 1.6))
            self.play(Create(ab), Create(bc), run_time=min(
                leftover(tracker, "b1"), 0.8))
            self.wait(leftover(tracker, "b1"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(ask, shift=RIGHT * 0.12),
                      FadeIn(prompt, shift=RIGHT * 0.12), run_time=0.5)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(pause, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b3"))

            self.challenge = {"rough": rough, "names": names, "cards": cards,
                              "ask": ask, "pause": pause, "ab": ab, "bc": bc,
                              "prompt": prompt, "points": (A, B, C, D),
                              "data": d}
            self._capture_srt(tracker)

        play_challenge_countdown(self, seconds=4, sfx=self.sfx,
                                 position=np.array([BOARD_CX, BOARD_CY, 0]))

        with self.voiceover(text=NARRATION["scene9_reveal"]) as tracker:
            ch = self.challenge
            A, B, C, D = ch["points"]
            d = ch["data"]
            names = ch["names"]

            # the question and the pause prompt have done their job
            self.play(FadeOut(ch["pause"]), FadeOut(ch["ask"]),
                      FadeOut(ch["prompt"]), run_time=0.4)
            self.wait(leftover(tracker, "b0"))

            tri = Polygon(A, B, C, color=CHALK_GREEN, stroke_width=3.0,
                          fill_color=CHALK_GREEN, fill_opacity=0.14)
            badge = board_text("First triangle: A B C", 17, CHALK_GREEN,
                               "BOLD").move_to(np.array([3.05, -1.55, 0]))
            badge2 = board_text("built by S.A.S", 15, CHALK_GREEN, "BOLD"
                                ).move_to(np.array([3.05, -1.93, 0]))
            self.play(Create(tri),
                      Indicate(ch["cards"][3], color=CHALK_AMBER,
                               scale_factor=1.12),
                      Circumscribe(tri, color=CHALK_GREEN, stroke_width=2.6,
                                   time_width=0.6),
                      run_time=min(leftover(tracker, "b1"), 1.2))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            ray_a = self.ray_line(A, d["ps_deg"], dist(A, D) * 1.02, CHALK_CYAN,
                                  3.0)
            ray_c = self.ray_line(C, d["rs_deg"], dist(C, D) * 1.08, CHALK_PINK,
                                  3.0)
            d_dot = Dot(radius=0.10, color=CHALK_YELLOW).move_to(D)
            self.play(FadeIn(badge, shift=UP * 0.1), FadeIn(badge2),
                      run_time=0.5)
            self.play(Create(ray_a), Create(ray_c), run_time=min(
                leftover(tracker, "b2"), 1.4))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b2"))

            quad = Polygon(A, B, C, D, color=CHALK_CYAN, stroke_width=2.4,
                           fill_color=CHALK_CYAN, fill_opacity=0.12)
            built = board_text("S.A.S builds. Two angles locate.", 16,
                               CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))
            self.play(FadeIn(d_dot, scale=0.5), FadeIn(quad),
                      FadeIn(built, shift=UP * 0.08),
                      Indicate(d_dot, color=CHALK_YELLOW, scale_factor=2.1),
                      Circumscribe(names[3], color=CHALK_YELLOW,
                                   fade_out=True),
                      run_time=min(leftover(tracker, "b3"), 1.0))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap -----------------------------------------------------
    def beat10_recap(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("Two Sides and Three Angles", 22, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            d = example_construction(
                centre=np.array([BOARD_CX - 3.05, 0.35, 0]), scale=0.36)
            P, Q, R, S = d["quad"]
            names = self.vertex_letters(
                (P, Q, R, S), ((-0.24, -0.09), (0.10, -0.26), (0.34, -0.22),
                               (-0.14, 0.30)), size=15)
            pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=3.4)
            qr = Line(Q, R, color=CHALK_YELLOW, stroke_width=3.4)
            tri = Polygon(P, Q, R, color=CHALK_YELLOW, stroke_width=3.0,
                          fill_color=CHALK_YELLOW, fill_opacity=0.16)
            ray_p = self.ray_line(P, d["ps_deg"], dist(P, S) * 1.06, CHALK_CYAN,
                                  2.6)
            ray_r = self.ray_line(R, d["rs_deg"], dist(R, S) * 1.06, CHALK_PINK,
                                  2.6)
            quad = Polygon(P, Q, R, S, color=CHALK_CYAN, stroke_width=2.2,
                           fill_color=CHALK_CYAN, fill_opacity=0.10)
            ang_q = angle_mark(Q, P, R, radius=0.36, color=CHALK_AMBER)
            s_dot = Dot(radius=0.08, color=CHALK_YELLOW).move_to(S)

            rows = VGroup(
                summary_row(1, "Two adjacent sides + the angle:",
                            r"\triangle PQR", CHALK_YELLOW),
                summary_row(2, "The other two angles:",
                            r"rays", CHALK_CYAN),
                summary_row(3, "Their crossing:", r"S", CHALK_GREEN),
            ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX + 1.6, 1.20, 0]))
            final = board_text("Side–Angle–Side builds the triangle.", 17,
                               CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -1.90, 0]))
            take = board_text("Angle–Angle locates the fourth vertex.", 16,
                              CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.45, 0]))
            acr = board_text("S.A.S.A.A", 18, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX - 3.05, -1.90, 0]))
            acr_box = SurroundingRectangle(acr, color=CHALK_GREEN, buff=0.14,
                                          corner_radius=0.1, stroke_width=2.4)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(quad), FadeIn(names), Create(tri), Create(pq),
                      Create(qr), FadeIn(ang_q), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(rows[0], shift=RIGHT * 0.12), run_time=0.5)
            self.play(Create(ray_p), Create(ray_r),
                      FadeIn(rows[1], shift=RIGHT * 0.12),
                      run_time=min(leftover(tracker, "b1"), 1.4))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b1"))

            self.play(FadeIn(s_dot, scale=0.5),
                      FadeIn(rows[2], shift=RIGHT * 0.12),
                      Indicate(s_dot, color=CHALK_YELLOW, scale_factor=2.0),
                      run_time=min(leftover(tracker, "b2"), 1.0))
            self.add_sound(self.sfx["success"], gain=-11)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeIn(final, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(take), FadeIn(acr), Create(acr_box),
                      Circumscribe(quad, color=CHALK_AMBER, stroke_width=3,
                                   time_width=0.5),
                      run_time=min(leftover(tracker, "b3"), 1.2))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b3"))

            summary = VGroup(quad, names, tri, pq, qr, ray_p, ray_r, ang_q,
                             s_dot, rows, final, take, acr, acr_box)
            thanks = board_text("Thank You for Watching!", 40, CHALK_WHITE,
                                "BOLD")
            thanks2 = board_text("See you in the next lesson :)", 25,
                                 CHALK_CYAN)
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

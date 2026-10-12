"""
Understanding Angles: Vertex, Arms, and Angle Regions
Story-mode chalkboard lesson (Telangana Class 6 Maths, Chapter 4: Basic
Geometrical Ideas, Storymode 04).

LLM KEY / FUNCTION NAME: angles_vertex_arms_and_regions

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

The defining visual is the OPENING-DOOR ANGLE: one persistent vertex O, one arm
held fixed, and a second ray that swings open like a door -- then the same angle
is revealed in layers (vertex, arms, the three-letter name with the vertex in
the middle, the filled interior marker, the boundary arms and the exterior).

Title + 10 scenes:
  0. Title card: two rays, one vertex, three regions.
  1. What makes an angle: the opening door and the clock hands.
  2. Building angle AOB from the common endpoint O.
  3. The vertex and the two arms (also called sides).
  4. The naming rule: with three letters the vertex is the middle letter.
  5. angle AOB = angle BOA, and the short name angle O.
  6. The interior: the region between the arms (point X).
  7. Boundary and exterior (points S and Z) -- three parts of the plane.
  8. Sorting points on angle PQR: M interior, N boundary, T exterior.
  9. Your turn: vertex/arms, two names, region sorting, the wrong name --
     after the series' centred ten-second THINK clock.
 10. Recap: build -> name -> locate, and the spoken thank-you card.
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


# (this section is spliced into a head whose own imports omit Arc, Rotate and
#  Sector; Dot, Line, Arrow, Circle, Polygon, VGroup and np are already there)
from manim import Arc, Rotate, Sector  # noqa: E402,F401

# Board layout shared by every scene of this video.
ROW_Y = 2.72             # every scene heading sits on this line
SUB_Y = 2.16             # the one-line sub-heading under it
BANNER_Y = -1.34         # the closing banner, above the strip
# The angle scenes sit a little lower on the board than the heading grid alone
# would put them, so the figure, its banner and its strip read as one block.
FIG_DROP = 0.12
# The burned-in caption grows up from the bottom of the frame: a one-line cue
# starts at y = -3.38 and a wrapped two-line cue reaches y = -2.93 (measured on
# the burned caps), so every closing strip sits at -1.80 and nothing at all sits
# below CAPTION_SAFE_Y = -2.00 -- audited by the IN-CAPTION-BAND check.
STRIP_Y = -1.86
CAPTION_SAFE_Y = -2.00

PANEL_FILL = "#16202B"
RAY_W = 4.2              # stroke width of an arm (ray)
DOT_R = 0.078            # radius of a point dot

# The persistent angle O-A-B: one arm along the x axis, the other at 40 degrees,
# fixed so every scene draws the same opening.
O_PT = (-2.30, -0.97)
ANG_A = 40.0
ANG_B = 0.0
RAY_A_LEN = 3.30
RAY_B_LEN = 4.10
A_PT = (O_PT[0] + RAY_A_LEN * np.cos(np.radians(ANG_A)),
        O_PT[1] + RAY_A_LEN * np.sin(np.radians(ANG_A)))
B_PT = (O_PT[0] + RAY_B_LEN, O_PT[1])
A_LABEL = (A_PT[0] + 0.26, A_PT[1] + 0.20)
B_LABEL = (B_PT[0] + 0.24, B_PT[1] - 0.02)

MARK_R = 0.88            # radius of the angle marker (arc + light fill)

# Scene 1's two everyday openings, placed symmetrically about BOARD_CX (0.50),
# and the two columns of the challenge cards, so both are centred on the board.
DOOR_X = -2.20
CLOCK_X = 3.20
CARD_L = -2.75
CARD_R = 3.75


# ---------------------------------------------------------------- furniture --
def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


def chip(text, color=CHALK_CYAN, size=15, width=None, height=0.50):
    """A small labelled chip."""
    lab = board_text(text, size, color, "BOLD")
    box = RoundedRectangle(corner_radius=0.09,
                           width=width or (lab.width + 0.40), height=height,
                           stroke_color=color, stroke_width=1.7,
                           fill_color=PANEL_FILL, fill_opacity=0.7)
    lab.move_to(box.get_center())
    return VGroup(box, lab)


def card(title, lines, color=CHALK_WHITE, width=4.0, height=1.20,
         title_size=18, line_size=15):
    """A rounded card with a heading and one or two body lines."""
    head = board_text(title, title_size, color, "BOLD")
    body = VGroup(*[board_text(line, line_size, CHALK_WHITE, "BOLD")
                    for line in lines]).arrange(DOWN, buff=0.20)
    box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                           stroke_color=color, stroke_width=2.0,
                           fill_color=PANEL_FILL, fill_opacity=0.55)
    head.move_to(box.get_center() + UP * (height / 2 - 0.24))
    body.move_to(box.get_center() - DOWN * (0.18 if len(lines) > 1 else 0.12))
    return VGroup(box, head, body)


def dot_point(name=None, x=0.0, y=0.0, color=CHALK_CYAN, size=20,
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


def ray_from(start, degrees, length, color=CHALK_WHITE, width=RAY_W,
             tip=0.24):
    """One thick ray: a straight line from `start` with an arrowhead."""
    start = np.array([float(start[0]), float(start[1]), 0.0])
    end = start + np.array([np.cos(np.radians(degrees)),
                            np.sin(np.radians(degrees)), 0.0]) * float(length)
    return Arrow(start, end, buff=0.0, color=color, stroke_color=color,
                 stroke_width=width, tip_length=tip,
                 max_tip_length_to_length_ratio=0.30)


def arc_at(start, a1, a2, radius=MARK_R, color=CHALK_AMBER, width=2.8):
    """The arc that marks the opening between two ray directions."""
    arc = Arc(radius=radius, start_angle=np.radians(a1),
              angle=np.radians(a2 - a1), stroke_color=color,
              stroke_width=width)
    arc.shift(np.array([float(start[0]), float(start[1]), 0.0]))
    return arc


def wedge_at(start, a1, a2, radius=MARK_R, color=CHALK_CYAN, opacity=0.22):
    """The light fill of the angle marker between the arms."""
    sec = Sector(radius=radius, start_angle=np.radians(a1),
                 angle=np.radians(a2 - a1), stroke_width=0,
                 fill_color=color, fill_opacity=opacity)
    return sec.shift(np.array([float(start[0]), float(start[1]), 0.0]))


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


def door_icon(color=CHALK_AMBER, w=1.06, h=1.52):
    """A real door, ajar, drawn with Manim's own primitives.

    It has everything a door has: the frame it hangs in (two jambs and a
    lintel), the leaf itself standing in perspective -- the hinge edge full
    height, the free edge nearer the viewer and so shorter -- with its two
    raised panels, its knob and its hinges, the floor line under it, and the
    arc the leaf sweeps as it opens.  The angle between the leaf and the
    threshold is exactly the angle this scene is about.

    The leaf and its panels are Polygons (not Rectangles) so that the layout
    audit never reads a door part as a card with chalk drawn behind it."""
    hinge = np.array([0.0, 0.0, 0.0])
    left = Line(hinge + DOWN * 0.10 + LEFT * 0.06,
                hinge + UP * (h + 0.08) + LEFT * 0.06,
                stroke_color=color, stroke_width=5.0)
    right = Line(hinge + RIGHT * w + DOWN * 0.10,
                 hinge + RIGHT * w + UP * (h + 0.04),
                 stroke_color=color, stroke_width=5.0)
    lintel = Line(hinge + LEFT * 0.06 + UP * (h + 0.08),
                  hinge + RIGHT * w + UP * (h + 0.04),
                  stroke_color=color, stroke_width=5.0)
    frame = VGroup(left, right, lintel)
    threshold = Line(hinge, hinge + RIGHT * w, stroke_color=CHALK_WHITE,
                     stroke_width=1.8, stroke_opacity=0.45)
    p00 = hinge + DOWN * 0.06
    p01 = hinge + UP * (h - 0.02)
    p10 = hinge + RIGHT * (w * 0.60) + DOWN * 0.16
    p11 = hinge + RIGHT * (w * 0.60) + UP * (h - 0.26)
    panel = Polygon(p00, p10, p11, p01, stroke_color=CHALK_WHITE,
                    stroke_width=2.8, fill_color=color, fill_opacity=0.26)

    def inside(u, v):
        """Bilinear point inside the leaf, so its panels stay glued to it."""
        return (p00 * (1 - u) * (1 - v) + p10 * u * (1 - v)
                + p11 * u * v + p01 * (1 - u) * v)

    def panel_rect(u0, u1, v0, v1):
        return Polygon(inside(u0, v0), inside(u1, v0), inside(u1, v1),
                       inside(u0, v1), stroke_color=CHALK_WHITE,
                       stroke_width=1.4, stroke_opacity=0.70,
                       fill_color=CHALK_WHITE, fill_opacity=0.04)

    panels = VGroup(panel_rect(0.16, 0.84, 0.56, 0.86),
                    panel_rect(0.16, 0.84, 0.14, 0.44))
    knob = VGroup(
        Circle(radius=0.080, stroke_color=CHALK_WHITE, stroke_width=2.2,
               fill_color=PANEL_FILL, fill_opacity=0.90),
        Circle(radius=0.032, stroke_color=CHALK_WHITE, stroke_width=1.2,
               fill_color=CHALK_WHITE, fill_opacity=0.95))
    knob.move_to(inside(0.78, 0.50))
    hinges = VGroup()
    for v in (0.24, 0.76):
        hinge_tab = Rectangle(width=0.055, height=0.15, stroke_color=color,
                              stroke_width=1.6, fill_color=color,
                              fill_opacity=0.75)
        hinge_tab.move_to(inside(0.03, v))
        hinges.add(hinge_tab)
    leaf = VGroup(panel, panels, knob, hinges)
    floor = Line(hinge + LEFT * 0.34 + DOWN * 0.11,
                 hinge + RIGHT * (w + 0.34) + DOWN * 0.11,
                 stroke_color=CHALK_WHITE, stroke_width=1.5,
                 stroke_opacity=0.35)
    sweep = Arc(radius=w * 0.66, start_angle=-0.15, angle=np.radians(50.0),
                arc_center=hinge, stroke_color=color, stroke_width=2.2)
    # The angle itself: a translucent wedge between the leaf and the threshold
    # with its arc drawn on top, so the opening the door makes is unmistakable.
    wedge = Sector(radius=w * 0.42, start_angle=0.0, angle=np.radians(44.0),
                   stroke_width=0, fill_color=CHALK_CYAN, fill_opacity=0.32,
                   arc_center=hinge)
    opening = Arc(radius=w * 0.42, start_angle=0.0, angle=np.radians(44.0),
                  arc_center=hinge, stroke_color=CHALK_YELLOW,
                  stroke_width=3.0)
    swing = VGroup(sweep, wedge, opening)
    grp = VGroup(frame, floor, threshold, swing, leaf)
    grp.frame = frame
    grp.threshold = threshold
    grp.swing = swing
    grp.leaf = leaf
    grp.hinge = hinge
    return grp


def clock_icon(color=CHALK_CYAN, r=0.66):
    """A real clock face: the rim, twelve hour marks, the two hands and the
    centre pin -- the textbook's second everyday angle."""
    rim = Circle(radius=r, stroke_color=color, stroke_width=3.0)
    face = Circle(radius=r * 0.90, stroke_color=color, stroke_width=1.0,
                  fill_color=PANEL_FILL, fill_opacity=0.55)
    marks = VGroup()
    for i in range(12):
        ang = np.radians(90.0 - i * 30.0)
        d = np.array([np.cos(ang), np.sin(ang), 0.0])
        marks.add(Line(d * (r * 0.78), d * (r * 0.90),
                       stroke_color=CHALK_WHITE,
                       stroke_width=2.6 if i % 3 == 0 else 1.3))
    pin = Dot(radius=0.038, color=CHALK_WHITE, fill_opacity=1.0)
    hand1 = Line(ORIGIN, UP * r * 0.52, stroke_color=CHALK_WHITE,
                 stroke_width=3.6)
    hand2 = Line(ORIGIN, RIGHT * r * 0.76, stroke_color=CHALK_YELLOW,
                 stroke_width=3.0)
    grp = VGroup(rim, face, marks, hand1, hand2, pin)
    grp.face = VGroup(rim, face, marks)
    grp.hand1 = hand1
    grp.hand2 = hand2
    return grp


# ----------------------------------------------------------------


NARRATION = {
    "title": (
        "An angle is made by two rays that start at the same point. <bookmark "
        "mark='b0'/>The common point is the vertex, and the two rays are the "
        "arms of the angle. <bookmark mark='b1'/>An angle also separates the "
        "plane into an interior, a boundary and an exterior."
    ),
    "s1": (
        "We see angles everywhere. <bookmark mark='b0'/>Think of a door: as it "
        "opens, the space between the door and the frame grows wider. <bookmark "
        "mark='b1'/>Now think of the hands of a clock: as they move apart, they "
        "also make an angle. <bookmark mark='b2'/>If we keep only the two "
        "directions, we are left with two rays starting at one point."
    ),
    "s2": (
        "Let us build that angle. <bookmark mark='b0'/>Start with a point O, and "
        "draw one ray from it, ray OB. <bookmark mark='b1'/>Now draw a second "
        "ray from the same point O: ray OA. <bookmark mark='b2'/>The opening "
        "between them is the angle, and we write it as angle AOB. Two rays with "
        "a common endpoint make an angle."
    ),
    "s3": (
        "Every angle has two named parts. <bookmark mark='b0'/>The common "
        "endpoint is the vertex, so here the vertex is O. <bookmark "
        "mark='b1'/>The two rays are the arms: ray OA is one arm, <bookmark "
        "mark='b2'/>and ray OB is the other. The arms are also called the sides "
        "of the angle."
    ),
    "s4": (
        "Now the naming rule. <bookmark mark='b0'/>With three letters, the "
        "vertex must be the middle letter: angle AOB is correct. <bookmark "
        "mark='b1'/>Angle BOA is also correct, because O is still in the "
        "middle. <bookmark mark='b2'/>But angle OAB has A in the middle, and "
        "angle ABO has B in the middle. <bookmark mark='b3'/>Those are not "
        "names of this angle, because the vertex O is not in the middle."
    ),
    "s5": (
        "Notice that angle AOB and angle BOA name the same angle. <bookmark "
        "mark='b0'/>Reading the arms in the other order does not change the "
        "opening. <bookmark mark='b1'/>And when there is only one angle at O, we "
        "may name it simply as angle O."
    ),
    "s6": (
        "An angle divides the plane around it. <bookmark mark='b0'/>The region "
        "between the two arms is called the interior of the angle. <bookmark "
        "mark='b1'/>A point X that lies between the arms is in the interior. "
        "<bookmark mark='b2'/>The interior follows the arms outward, however far "
        "they are extended."
    ),
    "s7": (
        "What about the arms themselves? <bookmark mark='b0'/>A point S on one "
        "of the arms lies on the angle itself; the arms are its boundary. "
        "<bookmark mark='b1'/>A point Z outside the opening is in the exterior. "
        "<bookmark mark='b2'/>So an angle separates the plane into three parts: "
        "interior, boundary and exterior."
    ),
    "s8": (
        "Let us sort three points on one angle. <bookmark mark='b0'/>Here is "
        "angle PQR, with its vertex at Q. <bookmark mark='b1'/>Point N lies on "
        "an arm, so it is on the boundary. <bookmark mark='b2'/>Point M is "
        "between the arms, so it is in the interior, and point T is outside, in "
        "the exterior."
    ),
    "s9q": (
        "Your turn. Four quick checks. <bookmark mark='b0'/>First: in angle COD, "
        "name the vertex and the two arms. <bookmark mark='b1'/>Second: this "
        "angle has vertex Q. Give two valid three-letter names. <bookmark "
        "mark='b2'/>Third: point M, point N and point T. <bookmark mark='b3'/>"
        "And last of all: which of these names is wrong?"
    ),
    "s9a": (
        "<bookmark mark='b0'/>In angle COD the vertex is O, and the arms are OC "
        "and OD. <bookmark mark='b1'/>For the second: angle AQB and angle BQA, "
        "because the vertex Q stays in the middle. <bookmark mark='b2'/>And "
        "point M is in the interior, point N is on the boundary, and point T is "
        "in the exterior. <bookmark mark='b3'/>The wrong name is angle ABO, "
        "because its middle letter is B and not the vertex O."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>Two rays with a common endpoint make "
        "an angle. <bookmark mark='b1'/>That common endpoint is the vertex, and "
        "the two rays are the arms. <bookmark mark='b2'/>When you name an angle "
        "with three letters, the vertex goes in the middle. <bookmark "
        "mark='b3'/>And the angle separates the plane into its interior, its "
        "boundary and its exterior. <bookmark mark='b4'/>Build, name, locate. "
        "<bookmark mark='b5'/>Thank you for watching, <bookmark mark='b6'/>and "
        "see you in the next lesson."
    ),
}


class AnglesVertexArmsRegionsStory(VoiceoverScene):
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
        out_dir = _HERE / "media" / "videos" / "angles_vertex_arms_and_regions"
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
    # Angles (Class 6 Maths, Chapter 4, Storymode 04).
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
    #   * the persistent angle O-A-B is fixed (O_PT / A_PT / B_PT) so every
    #     scene draws exactly the same opening; its one arm runs along the
    #     bottom-left and the free space to the right carries the labels;
    #   * the angle marker (the light fill + its arc) is deliberately small, so
    #     the words of the interior, the arms and the exterior sit in open board
    #     rather than inside a filled shape;
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

    def q_card(self, title, pict, color=CHALK_CYAN, width=3.00, pad=0.14,
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
                   buff=0.36):
        """One revealed answer, laid out in fixed columns: the letter, then the
        result, then the note.  Every row starts at the same x, so A, B, C and D
        line up down the board and the spacing is identical on every row."""
        lab = board_text(tag, 17, color, "BOLD")
        name = board_text(headline, 17, color, "BOLD")
        txt = board_text(note, 14, CHALK_WHITE, "BOLD")
        row = VGroup(lab, name, txt).arrange(RIGHT, buff=buff)
        box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                               stroke_color=color, stroke_width=1.8,
                               fill_color=PANEL_FILL, fill_opacity=0.6)
        box.move_to(np.array([BOARD_CX, 0.0, 0.0]))
        row.move_to(box.get_center())
        left = BOARD_CX - width / 2.0 + 0.34
        row.shift(np.array([left - row.get_left()[0], 0.0, 0.0]))
        return VGroup(box, row)

    def mini_angle(self, vertex="O", arms=("C", "D"), color=CHALK_GREEN,
                   points=(), show_arms=True):
        """A small angle for the challenge cards (centred on the origin):
        two arrowed rays from one vertex, the arc mark and the letters.

        Every letter is placed in open space -- a letter inside this narrow
        wedge would sit on one of the arms, which the clearance audit rejects --
        so a region point's letter stands just outside the opening and reads as
        its label."""
        o = np.array([0.0, 0.0, 0.0])
        len1, len2 = 0.98, 0.88
        r1 = ray_from(o, 0.0, len1, color, 3.2, 0.20)
        r2 = ray_from(o, 45.0, len2, color, 3.2, 0.20)
        arc = arc_at(o, 0.0, 45.0, 0.36, CHALK_AMBER, 2.6)
        end1 = o + np.array([len1, 0.0, 0.0])
        end2 = o + np.array([len2 * np.cos(np.radians(45)),
                             len2 * np.sin(np.radians(45)), 0.0])
        parts = [r1, r2, arc,
                 dot_point(vertex, o[0], o[1], CHALK_PINK, size=13,
                           label_dx=(0.04, -0.28))]
        if show_arms:
            parts.append(dot_point(arms[0], end1[0], end1[1], CHALK_CYAN,
                                   size=13, label_dx=(0.18, -0.08)))
            parts.append(dot_point(arms[1], end2[0], end2[1], CHALK_CYAN,
                                   size=13, label_dx=(0.06, 0.26)))
        spots = {"in": ((0.35, 0.27), (0.36, 0.12)),
                 "on": ((0.74, 0.0), (0.0, -0.32)),
                 "out": ((-0.38, 0.35), (-0.10, 0.30))}
        for name, kind in points:
            (px, py), (dx, dy) = spots[kind]
            col = {"in": CHALK_CYAN, "on": CHALK_AMBER,
                   "out": CHALK_PINK}[kind]
            parts.append(dot_point(name, px, py, col, size=12,
                                   label_dx=(dx, dy)))
        return VGroup(*parts)

    def ask_card(self, title, lines, color=CHALK_CYAN, width=3.00, pad=0.14,
                 title_size=15, line_size=12, buff=0.26):
        """A 'your turn' card whose question is written in words."""
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

    # -- Scene 0: title ------------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = at(board_text("Understanding Angles", 28, CHALK_PINK,
                                  "BOLD"), BOARD_CX, 1.66)
            sub = at(board_text("Vertex · Arms · Angle Regions", 18, CHALK_WHITE,
                                "BOLD"), BOARD_CX, 1.00)

            o = np.array([-0.60, -1.05, 0.0])
            r1 = ray_from(o, 0.0, 2.40, CHALK_GREEN, 4.0)
            r2 = ray_from(o, 40.0, 1.90, CHALK_GREEN, 4.0)
            arc = arc_at(o, 0.0, 40.0, 0.62, CHALK_AMBER, 2.6)
            wedge = wedge_at(o, 0.0, 40.0, 0.62, CHALK_CYAN, 0.20)
            vert = dot_point("O", o[0], o[1], CHALK_PINK, size=18,
                             label_dx=(-0.24, -0.28))
            labs = VGroup(at(board_text("arms", 14, CHALK_GREEN, "BOLD"),
                             0.10, 0.05),
                          at(board_text("vertex", 14, CHALK_PINK, "BOLD"),
                             -1.15, -0.72))
            verts_lab = at(board_text("A", 18, CHALK_WHITE, "BOLD"),
                           o[0] + 1.90 * np.cos(np.radians(40)) + 0.10,
                           o[1] + 1.90 * np.sin(np.radians(40)) + 0.22)
            strip = at(board_text("Two rays with one common endpoint make an "
                                  "angle.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(title, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(wedge), Create(r1), Create(r2), Create(arc),
                      FadeIn(vert), run_time=0.85)
            self.play(FadeIn(labs, shift=UP * 0.05), FadeIn(verts_lab),
                      run_time=0.55)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: what makes an angle ----------------------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("What Makes an Angle?", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A door opening, and the hands of a clock.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # The door and the clock are the two everyday openings; they sit
            # symmetrically about the board's own centre line (0.50).
            door = door_icon()
            shift = np.array([DOOR_X, 0.62, 0.0]) - door.get_center()
            door.shift(shift)
            hinge = door.hinge + shift
            door_lab = at(board_text("a door opening", 14, CHALK_WHITE, "BOLD"),
                          DOOR_X, -0.66)
            clock = at(clock_icon(), CLOCK_X, 0.72)
            clock_lab = at(board_text("clock hands", 14, CHALK_WHITE, "BOLD"),
                           CLOCK_X, -0.66)

            banner = at(board_text("AN ANGLE APPEARS", 19, CHALK_YELLOW, "BOLD"),
                        BOARD_CX, BANNER_Y)
            strip = at(board_text("Keep only the two directions and you have "
                                  "two rays from one point.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(door.frame), Create(door.threshold),
                      Create(door.leaf), FadeIn(door_lab, shift=UP * 0.05),
                      run_time=0.60)
            self.play(Rotate(door.leaf, angle=-0.30, about_point=hinge),
                      Create(door.swing), run_time=0.80)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(clock.face), Create(clock.hand1),
                      Create(clock.hand2), FadeIn(clock_lab, shift=UP * 0.05),
                      run_time=0.60)
            self.play(Rotate(clock.hand2, angle=0.95,
                             about_point=clock.get_center()), run_time=0.80)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeOut(door), FadeOut(door_lab), FadeOut(clock),
                      FadeOut(clock_lab), run_time=0.50)
            o = np.array([O_PT[0], O_PT[1], 0.0])
            bare_r1 = ray_from(o, ANG_B, RAY_B_LEN, CHALK_GREEN, RAY_W)
            bare_r2 = ray_from(o, ANG_A, RAY_A_LEN, CHALK_GREEN, RAY_W)
            bare_arc = arc_at(o, ANG_B, ANG_A, MARK_R, CHALK_AMBER, 2.8)
            bare_vert = dot_point("O", o[0], o[1], CHALK_PINK, size=20,
                                  label_dx=(-0.24, -0.26))
            self.play(Create(bare_r1), Create(bare_r2), Create(bare_arc),
                      FadeIn(bare_vert), run_time=0.75)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: two rays form an angle -------------------------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("Two Rays Form an Angle", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("They start at the same point, O.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            o = np.array([O_PT[0], O_PT[1], 0.0])
            ray_b = ray_from(o, ANG_B, RAY_B_LEN, CHALK_GREEN, RAY_W)
            ray_a = ray_from(o, ANG_A, RAY_A_LEN, CHALK_GREEN, RAY_W)
            vert = dot_point("O", o[0], o[1], CHALK_PINK, size=20,
                             label_dx=(-0.24, -0.26))
            end_a = dot_point("A", A_PT[0], A_PT[1], CHALK_CYAN, size=18,
                              label_dx=(A_LABEL[0] - A_PT[0],
                                        A_LABEL[1] - A_PT[1]))
            end_b = dot_point("B", B_PT[0], B_PT[1], CHALK_CYAN, size=18,
                              label_dx=(0.24, 0.22))
            arc = arc_at(o, ANG_B, ANG_A, MARK_R, CHALK_AMBER, 2.8)
            wedge = wedge_at(o, ANG_B, ANG_A, MARK_R, CHALK_CYAN, 0.20)
            name = at(chalk_math(r"\angle AOB", size=32, color=CHALK_YELLOW),
                      3.30, 0.60)

            banner = at(board_text("2 RAYS + 1 ENDPOINT = ANGLE", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The opening between the rays is the angle.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(ray_b), FadeIn(vert), FadeIn(end_b),
                      run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(ray_a), FadeIn(end_a), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(wedge), Create(arc), run_time=0.50)
            self.play(FadeIn(name, scale=0.9), run_time=0.45)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: vertex and arms --------------------------------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Vertex and Arms", 20, CHALK_AMBER, "BOLD"),
                         BOARD_CX, ROW_Y)
            sub = at(board_text("The common endpoint and the two rays.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            o = np.array([O_PT[0], O_PT[1], 0.0])
            ray_b = ray_from(o, ANG_B, RAY_B_LEN, CHALK_GREEN, RAY_W)
            ray_a = ray_from(o, ANG_A, RAY_A_LEN, CHALK_GREEN, RAY_W)
            arc = arc_at(o, ANG_B, ANG_A, MARK_R, CHALK_AMBER, 2.8)
            wedge = wedge_at(o, ANG_B, ANG_A, MARK_R, CHALK_CYAN, 0.20)
            vert = dot_point("O", o[0], o[1], CHALK_PINK, size=22,
                             label_dx=(-0.26, -0.28))
            end_a = dot_point("A", A_PT[0], A_PT[1], CHALK_CYAN, size=18,
                              label_dx=(A_LABEL[0] - A_PT[0],
                                        A_LABEL[1] - A_PT[1]))
            end_b = dot_point("B", B_PT[0], B_PT[1], CHALK_CYAN, size=18,
                              label_dx=(B_LABEL[0] - B_PT[0],
                                        B_LABEL[1] - B_PT[1]))

            r1 = at(board_text("VERTEX", 15, CHALK_PINK, "BOLD"), 3.30, 1.30)
            r2 = at(board_text("the common endpoint", 13, CHALK_WHITE, "BOLD"),
                    3.30, 0.86)
            r3 = at(board_text("ARM 1 · OA", 15, CHALK_CYAN, "BOLD"),
                    3.30, 0.22)
            r4 = at(board_text("ARM 2 · OB", 15, CHALK_GREEN, "BOLD"),
                    3.30, -0.50)
            r5 = at(board_text("also called sides", 13, CHALK_WHITE, "BOLD"),
                    3.30, -0.94)

            strip = at(board_text("The two rays are the arms, also called the "
                                  "sides.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(ray_b), Create(ray_a), Create(arc), FadeIn(wedge),
                      FadeIn(vert), FadeIn(end_a), FadeIn(end_b), run_time=0.70)

            self.wait(leftover(tracker, "b0"))
            self.play(Indicate(vert, color=CHALK_PINK, scale_factor=1.35),
                      FadeIn(r1, shift=UP * 0.05), FadeIn(r2, shift=UP * 0.05),
                      run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Indicate(ray_a, color=CHALK_CYAN, scale_factor=1.02),
                      FadeIn(r3, shift=UP * 0.05), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Indicate(ray_b, color=CHALK_GREEN, scale_factor=1.02),
                      FadeIn(r4, shift=UP * 0.05), FadeIn(r5, shift=UP * 0.05),
                      run_time=0.60)
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: the naming rule --------------------------------------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Middle Letter", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("With three letters, the vertex goes in the "
                                "middle.", 17, CHALK_WHITE, "BOLD"),
                     BOARD_CX, SUB_Y)

            o = np.array([O_PT[0], O_PT[1], 0.0])
            ray_b = ray_from(o, ANG_B, RAY_B_LEN, CHALK_GREEN, RAY_W)
            ray_a = ray_from(o, ANG_A, RAY_A_LEN, CHALK_GREEN, RAY_W)
            arc = arc_at(o, ANG_B, ANG_A, MARK_R, CHALK_AMBER, 2.8)
            wedge = wedge_at(o, ANG_B, ANG_A, MARK_R, CHALK_CYAN, 0.20)
            vert = dot_point("O", o[0], o[1], CHALK_PINK, size=22,
                             label_dx=(-0.26, -0.28))
            end_a = dot_point("A", A_PT[0], A_PT[1], CHALK_CYAN, size=18,
                              label_dx=(A_LABEL[0] - A_PT[0],
                                        A_LABEL[1] - A_PT[1]))
            end_b = dot_point("B", B_PT[0], B_PT[1], CHALK_CYAN, size=18,
                              label_dx=(B_LABEL[0] - B_PT[0],
                                        B_LABEL[1] - B_PT[1]))

            row_y = (1.34, 0.62, -0.10, -0.82)
            n1 = at(chalk_math(r"\angle AOB", size=30, color=CHALK_GREEN),
                    2.95, row_y[0])
            n2 = at(chalk_math(r"\angle BOA", size=30, color=CHALK_GREEN),
                    2.95, row_y[1])
            n3 = at(chalk_math(r"\angle OAB", size=30, color=CHALK_RED),
                    2.95, row_y[2])
            n4 = at(chalk_math(r"\angle ABO", size=30, color=CHALK_RED),
                    2.95, row_y[3])
            m1 = mark_yes((4.20, row_y[0]))
            m2 = mark_yes((4.20, row_y[1]))
            m3 = mark_no((4.20, row_y[2]))
            m4 = mark_no((4.20, row_y[3]))

            strip = at(board_text("The middle letter must be the vertex O.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(ray_b), Create(ray_a), Create(arc), FadeIn(wedge),
                      FadeIn(vert), FadeIn(end_a), FadeIn(end_b), run_time=0.70)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(n1, scale=0.9), Create(m1), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(n2, scale=0.9), Create(m2), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(n3, scale=0.9), Create(m3),
                      FadeIn(n4, scale=0.9), Create(m4), run_time=0.70)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: AOB = BOA, and the short name ------------------------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("Same Angle, Two Names", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Reading the arms in the other order.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            o = np.array([O_PT[0], O_PT[1], 0.0])
            ray_b = ray_from(o, ANG_B, RAY_B_LEN, CHALK_GREEN, RAY_W)
            ray_a = ray_from(o, ANG_A, RAY_A_LEN, CHALK_GREEN, RAY_W)
            arc = arc_at(o, ANG_B, ANG_A, MARK_R, CHALK_AMBER, 2.8)
            wedge = wedge_at(o, ANG_B, ANG_A, MARK_R, CHALK_CYAN, 0.20)
            vert = dot_point("O", o[0], o[1], CHALK_PINK, size=22,
                             label_dx=(-0.26, -0.28))
            end_a = dot_point("A", A_PT[0], A_PT[1], CHALK_CYAN, size=18,
                              label_dx=(A_LABEL[0] - A_PT[0],
                                        A_LABEL[1] - A_PT[1]))
            end_b = dot_point("B", B_PT[0], B_PT[1], CHALK_CYAN, size=18,
                              label_dx=(B_LABEL[0] - B_PT[0],
                                        B_LABEL[1] - B_PT[1]))
            hl_a = ray_from(o, ANG_A, RAY_A_LEN, CHALK_CYAN, 6.0)

            equal = at(chalk_math(r"\angle AOB = \angle BOA", size=28,
                                  color=CHALK_YELLOW), 3.20, 0.70)
            short = at(chip("angle O", CHALK_CYAN, size=16), 3.20, -0.20)
            short_note = at(board_text("only with one angle at O", 13,
                                       CHALK_WHITE, "BOLD"), 3.60, -0.95)

            strip = at(board_text("Reversing the arms does not change the "
                                  "angle.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(ray_b), Create(ray_a), Create(arc), FadeIn(wedge),
                      FadeIn(vert), FadeIn(end_a), FadeIn(end_b), run_time=0.70)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(hl_a), run_time=0.30)
            self.play(Indicate(ray_b, color=CHALK_YELLOW, scale_factor=1.02),
                      run_time=0.45)
            self.play(FadeOut(hl_a), run_time=0.25)
            self.play(FadeIn(equal, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(short, scale=0.9),
                      FadeIn(short_note, shift=UP * 0.05), run_time=0.50)
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: the interior -----------------------------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Interior", 20, CHALK_AMBER, "BOLD"),
                         BOARD_CX, ROW_Y)
            sub = at(board_text("The region between the two arms.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            o = np.array([O_PT[0], O_PT[1], 0.0])
            ray_b = ray_from(o, ANG_B, RAY_B_LEN, CHALK_GREEN, RAY_W)
            ray_a = ray_from(o, ANG_A, RAY_A_LEN, CHALK_GREEN, RAY_W)
            arc = arc_at(o, ANG_B, ANG_A, MARK_R, CHALK_AMBER, 2.8)
            wedge = wedge_at(o, ANG_B, ANG_A, MARK_R, CHALK_CYAN, 0.22)
            vert = dot_point("O", o[0], o[1], CHALK_PINK, size=22,
                             label_dx=(-0.26, -0.28))
            interior_lab = at(board_text("INTERIOR", 14, CHALK_CYAN, "BOLD"),
                              0.55, -0.45)
            x_pt = dot_point("X", -0.80, -0.30, CHALK_CYAN, size=18,
                             label_dx=(-0.06, -0.28))
            banner = at(board_text("INTERIOR = BETWEEN THE ARMS", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The interior follows the arms outward.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(ray_b), Create(ray_a), FadeIn(vert), run_time=0.60)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(wedge), Create(arc),
                      FadeIn(interior_lab, shift=UP * 0.05), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(x_pt, scale=0.85), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: boundary and exterior --------------------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Boundary and Exterior", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("On an arm, or outside the opening.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            o = np.array([O_PT[0], O_PT[1], 0.0])
            ray_b = ray_from(o, ANG_B, RAY_B_LEN, CHALK_GREEN, RAY_W)
            ray_a = ray_from(o, ANG_A, RAY_A_LEN, CHALK_GREEN, RAY_W)
            arc = arc_at(o, ANG_B, ANG_A, MARK_R, CHALK_AMBER, 2.8)
            wedge = wedge_at(o, ANG_B, ANG_A, MARK_R, CHALK_CYAN, 0.20)
            vert = dot_point("O", o[0], o[1], CHALK_PINK, size=22,
                             label_dx=(-0.26, -0.28))
            s_pt = dot_point("S", 0.60, -0.97, CHALK_AMBER, size=18,
                             label_dx=(0.0, -0.30))
            z_pt = dot_point("Z", -1.40, 0.60, CHALK_PINK, size=18,
                             label_dx=(-0.06, 0.26))
            c1 = at(chip("INTERIOR", CHALK_CYAN, size=14), 3.30, 0.62)
            c2 = at(chip("BOUNDARY", CHALK_AMBER, size=14), 3.30, -0.10)
            c3 = at(chip("EXTERIOR", CHALK_PINK, size=14), 3.30, -0.82)
            traveller = Dot(radius=0.06, color=CHALK_YELLOW, fill_opacity=1.0)
            traveller.move_to(np.array([-1.40, 0.60, 0.0]))

            strip = at(board_text("Interior, boundary and exterior — three "
                                  "parts of the plane.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(ray_b), Create(ray_a), Create(arc), FadeIn(wedge),
                      FadeIn(vert), run_time=0.65)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(s_pt, scale=0.85), FadeIn(c1, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(z_pt, scale=0.85), FadeIn(c2, scale=0.9),
                      FadeIn(c3, scale=0.9), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(traveller, scale=0.8), run_time=0.30)
            self.play(traveller.animate.move_to(np.array([-0.80, -0.30, 0.0])),
                      run_time=1.05)
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: where does each point belong -------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("Where Does Each Point Belong?", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Angle PQR, with its vertex at Q.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            o = np.array([O_PT[0], O_PT[1], 0.0])
            ray_b = ray_from(o, ANG_B, RAY_B_LEN, CHALK_GREEN, RAY_W)
            ray_a = ray_from(o, ANG_A, RAY_A_LEN, CHALK_GREEN, RAY_W)
            arc = arc_at(o, ANG_B, ANG_A, MARK_R, CHALK_AMBER, 2.8)
            wedge = wedge_at(o, ANG_B, ANG_A, MARK_R, CHALK_CYAN, 0.20)
            vert = dot_point("Q", o[0], o[1], CHALK_PINK, size=20,
                             label_dx=(-0.28, -0.26))
            end_p = dot_point("P", A_PT[0], A_PT[1], CHALK_CYAN, size=18,
                              label_dx=(A_LABEL[0] - A_PT[0],
                                        A_LABEL[1] - A_PT[1]))
            end_r = dot_point("R", B_PT[0], B_PT[1], CHALK_CYAN, size=18,
                              label_dx=(B_LABEL[0] - B_PT[0],
                                        B_LABEL[1] - B_PT[1]))
            m_pt = dot_point("M", -0.80, -0.30, CHALK_CYAN, size=18,
                             label_dx=(-0.06, -0.28))
            n_pt = dot_point("N", 0.60, -0.97, CHALK_AMBER, size=18,
                             label_dx=(0.0, -0.30))
            t_pt = dot_point("T", -1.40, 0.60, CHALK_PINK, size=18,
                             label_dx=(-0.06, 0.26))
            c1 = at(chip("M · INTERIOR", CHALK_CYAN, size=14), 3.30, 0.62)
            c2 = at(chip("N · BOUNDARY", CHALK_AMBER, size=14), 3.30, -0.10)
            c3 = at(chip("T · EXTERIOR", CHALK_PINK, size=14), 3.30, -0.82)

            strip = at(board_text("Every other point lies in one of the three "
                                  "regions.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(ray_b), Create(ray_a), Create(arc), FadeIn(wedge),
                      FadeIn(vert), FadeIn(end_p), FadeIn(end_r), run_time=0.70)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(n_pt, scale=0.85), FadeIn(c2, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(m_pt, scale=0.85), FadeIn(c1, scale=0.9),
                      FadeIn(t_pt, scale=0.85), FadeIn(c3, scale=0.9),
                      run_time=0.70)
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

            qa = at(self.q_card("vertex? arms?",
                                self.mini_angle("O", ("C", "D"), CHALK_GREEN),
                                CHALK_GREEN), CARD_L, 0.92)
            qb = at(self.q_card("give two names",
                                self.mini_angle("Q", ("A", "B"), CHALK_CYAN),
                                CHALK_CYAN), CARD_R, 0.92)
            qc = at(self.q_card("classify M, N, T",
                                self.mini_angle("Q", ("P", "R"), CHALK_AMBER,
                                                points=(("M", "in"),
                                                        ("N", "on"),
                                                        ("T", "out")),
                                                show_arms=False),
                                CHALK_AMBER), CARD_L, -0.98)
            qd = at(self.ask_card("which name is wrong?",
                                  ["angle AOB", "angle BOA", "angle ABO"],
                                  CHALK_PINK, width=3.00), CARD_R, -0.98)

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
            a1 = at(self.answer_row("A", "vertex O · arms OC and OD",
                                    "the common endpoint and the rays",
                                    CHALK_GREEN), BOARD_CX, 1.62)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "angle AQB = angle BQA",
                                    "vertex Q in the middle", CHALK_CYAN),
                    BOARD_CX, 0.82)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "M interior · N boundary · T exterior",
                                    "between · on an arm · outside",
                                    CHALK_AMBER), BOARD_CX, 0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "angle ABO is wrong",
                                    "the middle letter must be the vertex",
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

            heading = at(board_text("Build · Name · Locate", 22, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)

            r1 = at(self.answer_row("1", "TWO RAYS + ONE POINT",
                                    "this is how an angle is formed",
                                    CHALK_GREEN), BOARD_CX, 1.48)
            r2 = at(self.answer_row("2", "VERTEX · ARMS",
                                    "common endpoint · the two rays (sides)",
                                    CHALK_CYAN), BOARD_CX, 0.72)
            r3 = at(self.answer_row("3", "THE VERTEX IN THE MIDDLE",
                                    "angle AOB = angle BOA", CHALK_YELLOW),
                    BOARD_CX, -0.04)
            r4 = at(self.answer_row("4", "INTERIOR · BOUNDARY · EXTERIOR",
                                    "between · on an arm · outside",
                                    CHALK_AMBER), BOARD_CX, -0.80)
            strip = at(board_text("Build the angle, name it, then locate the "
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
            self.play(FadeIn(r4, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)

            # The closing strip now goes up with the last recap row, so the whole
            # "...interior, boundary and exterior. Build, name, locate." stretch
            # plays with the finished board in front of the learner; the board is
            # only cleared when the voice actually says "Thank you for watching,".
            self.wait(leftover(tracker, "b4"))

            # "Thank you for watching," -- only now does the recap give way to
            # the thank-you card, so no earlier sentence is cut off.
            self.wait(leftover(tracker, "b5"))
            self.play(FadeOut(heading), FadeOut(r1), FadeOut(r2), FadeOut(r3),
                      FadeOut(r4), FadeOut(strip), run_time=0.55)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.50)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.closing(tracker, thanks, run_time=1.2)
            self._capture_srt(tracker)

        self.wait(END_HOLD)

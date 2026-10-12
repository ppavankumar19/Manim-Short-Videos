"""
Angles and Parallel Lines: the Six Relationships, and the Equation They Give
Story-mode chalkboard lesson (Class 8 Mathematics, Chapter 2: Linear Equations
in One Variable -- Applications of Angles and Parallel Lines).

LLM KEY / FUNCTION NAME: parallel_lines_and_angles

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

The defining visual is ONE FIGURE: two parallel lines, each carrying the same
chevron arrow mark, cut by a single transversal, making eight angles.  Every
relationship is then revealed by changing only the emphasis -- the pair of
wedges is lit in its own colour while the other six stay pale -- and the video
ends by turning one of those rules into a linear equation and solving it.

Title + 10 scenes:
  0. Title card: eight angles, six relationships, one equation.
  1. Parallel lines and the transversal: what the words mean.
  2. Eight angles at two crossings, and the interior/exterior regions.
  3. Vertically opposite angles are equal; a linear pair adds to 180.
  4. Corresponding angles are equal (1=5, 2=6, 3=7, 4=8).
  5. Alternate interior angles are equal (4=5, 3=6).
  6. Same-side interior angles add to 180 (3+5, 4+6).
  7. The two exterior rules: alternate exterior equal, same-side exterior 180.
  8. The application: same-side interior -> (3x+20)+(5x-8)=180 -> x=21,
     and the angles 83 and 97 degrees.
  9. Your turn: name each relationship, then find x -- after the series'
     centred ten-second THINK clock.
 10. The six relationships in one list, and the spoken thank-you card.
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
#  Dot, Line, Arrow, Circle, Polygon, VGroup and np are already there)
from manim import Arc, Sector  # noqa: E402,F401

# Board layout shared by every scene of this video.
ROW_Y = 2.72             # every scene heading sits on this line
SUB_Y = 2.16             # the one-line sub-heading under it
BANNER_Y = -1.15         # the closing banner, above the strip
# The burned-in caption grows up from the bottom of the frame: a one-line cue
# starts at y = -3.38 and a wrapped two-line cue reaches y = -2.93, so every
# closing strip sits at -1.80 and nothing at all sits below
# CAPTION_SAFE_Y = -2.00 -- audited by the IN-CAPTION-BAND check.
STRIP_Y = -1.80
CAPTION_SAFE_Y = -2.00
PANEL_FILL = "#16202B"

# The figure: two horizontal parallel lines cut by one steep transversal.
# The lines sit high enough that the lowest wedges and arcs stay clear of the
# closing banner at BANNER_Y, and the transversal stops well above it too.
PAR_Y1 = 1.35            # the upper parallel line
PAR_Y2 = -0.25           # the lower parallel line
PAR_X0 = -3.30
PAR_X1 = 1.30
TRA_TOP = (0.596, 1.85)
TRA_BOT = (-0.360, -0.72)
U_CROSS = (0.410, 1.35)  # where the transversal meets the upper line
L_CROSS = (-0.186, -0.25)  # where it meets the lower line
TRA_ANG = 69.6           # the transversal's "up" direction, in degrees
SECT_R = 0.62            # radius of every angle wedge
LINE_W = 4.0

# The eight angles.  At each crossing the four wedges are, counter-clockwise:
# top-left, top-right, bottom-left, bottom-right.  Numbering (the textbook
# convention): 1-4 at the upper crossing, 5-8 at the lower one, so that
#   1 2 7 8 are exterior, 3 4 5 6 are interior,
#   1=5, 2=6, 3=7, 4=8 correspond, and 3+5, 4+6 are same-side interior.
ANGLE_SPEC = {
    1: (U_CROSS, TRA_ANG, 180.0),
    2: (U_CROSS, 0.0, TRA_ANG),
    3: (U_CROSS, 180.0, TRA_ANG + 180.0),
    4: (U_CROSS, TRA_ANG + 180.0, 360.0),
    5: (L_CROSS, TRA_ANG, 180.0),
    6: (L_CROSS, 0.0, TRA_ANG),
    7: (L_CROSS, 180.0, TRA_ANG + 180.0),
    8: (L_CROSS, TRA_ANG + 180.0, 360.0),
}
INTERIOR = (3, 4, 5, 6)
EXTERIOR = (1, 2, 7, 8)
CORRESPONDING = ((1, 5), (2, 6), (3, 7), (4, 8))
ALT_INTERIOR = ((4, 5), (3, 6))
SAME_SIDE_INTERIOR = ((3, 5), (4, 6))
ALT_EXTERIOR = ((2, 7), (1, 8))
SAME_SIDE_EXTERIOR = ((1, 7), (2, 8))
VERTICAL = ((1, 4), (2, 3), (5, 8), (6, 7))

# The six relationships, in the order this video teaches them.
CHALK_VIOLET = "#B58CF0"
RULE_COLOR = {
    "vertical": CHALK_VIOLET,
    "corresponding": CHALK_PINK,
    "alt_interior": CHALK_RED,
    "same_side_interior": CHALK_GREEN,
    "alt_exterior": CHALK_CYAN,
    "same_side_exterior": CHALK_YELLOW,
}

# The right-hand column: the labels of whatever the scene is naming.
COL_X = 3.60


# ---------------------------------------------------------------- furniture --
def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


def pt(p):
    """A board coordinate as a 3-D point."""
    return np.array([float(p[0]), float(p[1]), 0.0])


def par_pair(color=CHALK_WHITE, width=LINE_W):
    """The two parallel lines, each with the same chevron arrow mark at its
    right-hand end -- the sign that says "these two are parallel"."""
    l1 = Line(pt((PAR_X0, PAR_Y1)), pt((PAR_X1, PAR_Y1)), stroke_color=color,
              stroke_width=width)
    l2 = Line(pt((PAR_X0, PAR_Y2)), pt((PAR_X1, PAR_Y2)), stroke_color=color,
              stroke_width=width)
    m1 = chevron(PAR_X1 - 0.30, PAR_Y1, color)
    m2 = chevron(PAR_X1 - 0.30, PAR_Y2, color)
    grp = VGroup(l1, l2)
    grp.marks = VGroup(m1, m2)
    grp.l1 = l1
    grp.l2 = l2
    return grp


def chevron(x, y, color=CHALK_WHITE, s=0.17):
    """A small ">" arrowhead on a line: the parallel mark."""
    a = np.array([float(x), float(y) + s, 0.0])
    b = np.array([float(x) + s * 0.85, float(y), 0.0])
    c = np.array([float(x), float(y) - s, 0.0])
    return VGroup(Line(a, b, stroke_color=color, stroke_width=3.0),
                  Line(b, c, stroke_color=color, stroke_width=3.0))


def transversal(color=CHALK_AMBER, width=LINE_W):
    """The third line, long enough to stick out past both parallel lines."""
    return Line(pt(TRA_BOT), pt(TRA_TOP), stroke_color=color,
                stroke_width=width)


def sector_at(vertex, a1, a2, radius=SECT_R, color=CHALK_CYAN, opacity=0.22):
    """The translucent wedge of one angle."""
    return Sector(radius=radius, start_angle=np.radians(a1),
                  angle=np.radians(a2 - a1), stroke_width=0,
                  fill_color=color, fill_opacity=opacity, arc_center=pt(vertex))


def arc_at(vertex, a1, a2, radius=SECT_R, color=CHALK_AMBER, width=2.8):
    """The arc that marks one angle."""
    return Arc(radius=radius, start_angle=np.radians(a1),
               angle=np.radians(a2 - a1), arc_center=pt(vertex),
               stroke_color=color, stroke_width=width)


def angle_sector(n, radius=SECT_R, color=CHALK_CYAN, opacity=0.22):
    v, a1, a2 = ANGLE_SPEC[n]
    return sector_at(v, a1, a2, radius, color, opacity)


def angle_arc(n, radius=SECT_R, color=CHALK_AMBER, width=2.8):
    v, a1, a2 = ANGLE_SPEC[n]
    return arc_at(v, a1, a2, radius, color, width)


def angle_pos(n, dist=0.42):
    """Where the number of angle `n` is written: inside its own wedge, on the
    bisector, far enough from both bounding lines that the digits never touch
    a line."""
    (vx, vy), a1, a2 = ANGLE_SPEC[n]
    mid = np.radians((a1 + a2) / 2.0)
    return (vx + dist * np.cos(mid), vy + dist * np.sin(mid))


def band(color=CHALK_CYAN, opacity=0.10):
    """The translucent strip between the parallel lines: the interior."""
    poly = Polygon(pt((PAR_X0, PAR_Y2)), pt((PAR_X1, PAR_Y2)),
                   pt((PAR_X1, PAR_Y1)), pt((PAR_X0, PAR_Y1)),
                   stroke_width=0, fill_color=color, fill_opacity=opacity)
    return poly


def dot_point(name=None, x=0.0, y=0.0, color=CHALK_CYAN, size=20,
              label_dx=(0.0, 0.0), r=0.08):
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


# ----------------------------------------------------------------


NARRATION = {
    "title": (
        "A transversal cutting two parallel lines makes eight angles. <bookmark "
        "mark='b0'/>Those eight angles are linked by six relationships, "
        "<bookmark mark='b1'/>and those relationships turn a diagram into an "
        "equation."
    ),
    "s1": (
        "Two lines in the same plane that never meet are called parallel lines. "
        "<bookmark mark='b0'/>Here they are, with the same arrow mark on each. "
        "<bookmark mark='b1'/>A line that cuts across them is called a "
        "transversal. <bookmark mark='b2'/>It crosses both parallel lines and "
        "makes eight angles, four at each crossing. <bookmark mark='b3'/>The "
        "whole lesson lives in that one figure."
    ),
    "s2": (
        "At each crossing there are four angles, so the figure has eight angles "
        "in all. <bookmark mark='b0'/>We number them from one to eight, going "
        "around each crossing. <bookmark mark='b1'/>Angles three, four, five and "
        "six lie between the two parallel lines: these are the interior angles. "
        "<bookmark mark='b2'/>Angles one, two, seven and eight lie outside the "
        "lines: these are the exterior angles."
    ),
    "s3": (
        "Start at the upper crossing. <bookmark mark='b0'/>Angles one and four "
        "are vertically opposite, so they are equal. <bookmark mark='b1'/>Angles "
        "one and two lie side by side on the straight line, so they form a "
        "linear pair and add up to one hundred and eighty degrees. <bookmark "
        "mark='b2'/>The same is true at the lower crossing."
    ),
    "s4": (
        "Corresponding angles sit in the same position at the two crossings. "
        "<bookmark mark='b0'/>Angle one and angle five are both at the top left, "
        "so they correspond, and they are equal. <bookmark mark='b1'/>Angle two "
        "and angle six are both at the top right, so they are equal as well. "
        "<bookmark mark='b2'/>In the same way, angle three equals angle seven, "
        "and angle four equals angle eight."
    ),
    "s5": (
        "Now look between the parallel lines. <bookmark mark='b0'/>Angles four "
        "and five are on opposite sides of the transversal, so they are "
        "alternate interior angles, and they are equal. <bookmark mark='b1'/>"
        "Angles three and six are the other alternate interior pair, and they "
        "are equal too. <bookmark mark='b2'/>Alternate interior angles are "
        "always equal when the lines are parallel."
    ),
    "s6": (
        "One pair of interior angles behaves differently. <bookmark "
        "mark='b0'/>Angles three and five are on the same side of the "
        "transversal, between the parallel lines. <bookmark mark='b1'/>Because "
        "the lines are parallel, these same-side interior angles add up to one "
        "hundred and eighty degrees. <bookmark mark='b2'/>Angles four and six "
        "are the other such pair, and they also add up to one hundred and eighty "
        "degrees."
    ),
    "s7": (
        "The exterior angles have their own two rules. <bookmark mark='b0'/>"
        "Angles two and seven are on opposite sides of the transversal, outside "
        "the parallel lines: they are alternate exterior angles, and they are "
        "equal. <bookmark mark='b1'/>Angles one and eight are the other "
        "alternate exterior pair, and they are equal too. <bookmark "
        "mark='b2'/>Angles one and seven are on the same side, so they are "
        "same-side exterior angles, and they add up to one hundred and eighty "
        "degrees. <bookmark mark='b3'/>Angles two and eight do the same, so both "
        "exterior rules are now in place."
    ),
    "s8": (
        "This is why the rules matter: every one of them turns a diagram into an "
        "equation. <bookmark mark='b0'/>Step one: identify the pair. Angles three "
        "and five are same-side interior angles, so they add up to one hundred "
        "and eighty degrees. <bookmark mark='b1'/>Step two: read the measures off "
        "the diagram: three x plus twenty, and five x minus eight. <bookmark "
        "mark='b2'/>Step three: form the equation. Eight x plus twelve equals one "
        "hundred and eighty, so eight x is one hundred and sixty-eight. <bookmark "
        "mark='b3'/>Step four: solve, and x is twenty-one. <bookmark mark='b4'/>"
        "Step five: interpret. The angles are eighty-three degrees and "
        "ninety-seven degrees, and they do add up to one hundred and eighty."
    ),
    "s9": (
        "Let us use a second pair. <bookmark mark='b0'/>These two angles are in "
        "the same position at the two crossings, so they are corresponding "
        "angles, and corresponding angles are equal. <bookmark mark='b1'/>The "
        "diagram gives them as five x, and two x plus twenty-four. <bookmark "
        "mark='b2'/>Equal angles give an equation: five x equals two x plus "
        "twenty-four. Subtracting two x from both sides leaves three x equals "
        "twenty-four. <bookmark mark='b3'/>So x is eight. <bookmark mark='b4'/>"
        "Both angles are forty degrees, which is exactly what equal angles should "
        "be."
    ),
    "s9q": (
        "Your turn. Four quick checks. <bookmark mark='b0'/>First: this pair sit "
        "in the same position at the two crossings. Are they equal, or do they "
        "add up to one hundred and eighty? <bookmark mark='b1'/>Second: this "
        "pair lie between the parallel lines, on opposite sides of the "
        "transversal. <bookmark mark='b2'/>Third: this pair lie between the "
        "lines, on the same side. <bookmark mark='b3'/>And last of all: two "
        "corresponding angles are two x plus ten and three x minus thirty. Find "
        "x."
    ),
    "s9a": (
        "<bookmark mark='b0'/>The first pair are corresponding angles, so they "
        "are equal. <bookmark mark='b1'/>The second pair are alternate interior "
        "angles, so they are equal as well. <bookmark mark='b2'/>The third pair "
        "are same-side interior angles, so they add up to one hundred and eighty "
        "degrees. <bookmark mark='b3'/>And for the last one: two x plus ten "
        "equals three x minus thirty, so x is forty, and each angle is ninety "
        "degrees."
    ),
    "s10": (
        "One last look at all six relationships. <bookmark mark='b0'/>"
        "Corresponding angles are equal, <bookmark mark='b1'/>alternate interior "
        "angles are equal, and so are alternate exterior angles. <bookmark "
        "mark='b2'/>Vertically opposite angles are equal too. <bookmark "
        "mark='b3'/>Same-side interior angles add up to one hundred and eighty "
        "degrees, and same-side exterior angles do the same. <bookmark "
        "mark='b4'/>Geometry gives the rule, and the equation finds x. <bookmark "
        "mark='b5'/>Thank you for watching, <bookmark mark='b6'/>and see you in "
        "the next lesson."
    ),
}


class ParallelLinesAndAnglesStory(VoiceoverScene):
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
        out_dir = _HERE / "media" / "videos" / "parallel_lines_and_angles"
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
        self.beat_s9q()
        self.beat_s10()

        self._write_real_srt()

    # ================================================================ beats ==
    # Angles and parallel lines (Class 8, Chapter 2, "Applications of Angles
    # and Parallel Lines").
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
    #   * the figure is fixed (PAR_Y1/PAR_Y2, TRA_TOP/TRA_BOT) so every scene
    #     draws the same two parallel lines and the same transversal, and the
    #     transversal stops above the banner line so no banner is ever crossed
    #     by a chalk line;
    #   * the eight numbers sit inside their own wedges, on the bisector, clear
    #     of both lines that bound the wedge and of the arc;
    #   * the right-hand column (COL_X) carries the rule of the scene, so no
    #     text has to be written across the figure;
    #   * the challenge uses the series' shared 10-second THINK clock, dead
    #     centre of the board, with the four question cards in the corners.

    def closing(self, tracker, mob=None, color=CHALK_YELLOW, run_time=None):
        """Consume the tail of the narration window on the last reveal."""
        budget = rt(tracker.get_remaining_duration()) if run_time is None \
            else run_time
        if mob is None:
            self.wait(max(budget, 0.0))
        else:
            self.play(Indicate(mob, color=color, scale_factor=1.03),
                      run_time=max(budget, MIN_RT))

    def figure(self, fill=0.10, band_on=False, marks=True, numbers=(),
               num_color=CHALK_WHITE, num_size=15, scale=1.0,
               about=(-1.00, 0.30), hot=(), hot_color=CHALK_YELLOW,
               hot_opacity=0.38):
        """The whole figure: the two parallel lines, the transversal, the eight
        translucent wedges with their arcs, and (optionally) the eight numbers
        and a pair of wedges picked out in one rule colour."""
        grp = VGroup()
        if band_on:
            grp.add(band())
        pair = par_pair()
        tra = transversal()
        grp.add(pair.l1, pair.l2, tra)
        if marks:
            grp.add(pair.marks)
        wedges, arcs = VGroup(), VGroup()
        for n in range(1, 9):
            # Only the *chosen* pair is filled: filling all eight wedges would
            # paint a full disc around each crossing, which hides the very
            # structure this lesson is about.
            if fill > 0:
                wedges.add(angle_sector(n, color=CHALK_CYAN, opacity=fill))
            arcs.add(angle_arc(n, color=CHALK_AMBER, width=2.0))
        for n in hot:
            wedges.add(angle_sector(n, color=hot_color, opacity=hot_opacity))
            arcs.add(angle_arc(n, color=hot_color, width=3.4))
        grp.add(wedges, arcs)
        nums = VGroup()
        for n in numbers:
            x, y = angle_pos(n)
            nums.add(at(board_text(str(n), num_size, num_color, "BOLD"), x, y))
        if len(nums):
            grp.add(nums)
        if scale != 1.0:
            grp.scale(scale, about_point=pt(about))
        grp.pair, grp.tra, grp.wedges, grp.arcs, grp.nums = (pair, tra,
                                                             wedges, arcs, nums)
        return grp

    def numbers(self, ns, color=CHALK_WHITE, size=15, scale=1.0,
                about=(-1.00, 0.30)):
        """The numbers of the given angles, in place."""
        grp = VGroup()
        for n in ns:
            x, y = angle_pos(n)
            grp.add(at(board_text(str(n), size, color, "BOLD"), x, y))
        if scale != 1.0:
            grp.scale(scale, about_point=pt(about))
        return grp

    def highlight(self, ns, color, opacity=0.38, width=3.4, scale=1.0,
                 about=(-1.00, 0.30)):
        """The wedges of the given angles, over-drawn in one rule colour."""
        grp = VGroup()
        for n in ns:
            grp.add(angle_sector(n, color=color, opacity=opacity))
            grp.add(angle_arc(n, color=color, width=width))
        if scale != 1.0:
            grp.scale(scale, about_point=pt(about))
        return grp

    def col_item(self, head, note, color, y, x=COL_X, width=3.20, height=0.92,
                 head_size=15, note_size=13):
        """One row of the right-hand column: a keyword and its note inside one
        card, spaced so no two words on the board come closer than 0.22 units."""
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
        return at(grp, x, y)

    def q_card(self, title, pict, color=CHALK_CYAN, width=3.00, pad=0.12,
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

    def ask_card(self, title, lines, color=CHALK_CYAN, width=3.00, pad=0.12,
                 title_size=13, line_size=12, buff=0.32):
        """A 'your turn' card whose question is written in words."""
        head = board_text(title, title_size, color, "BOLD")
        body = VGroup(*[board_text(line, line_size, CHALK_WHITE, "BOLD")
                        for line in lines]).arrange(DOWN, buff=0.24)
        content = VGroup(head, body).arrange(DOWN, buff=buff)
        box = RoundedRectangle(corner_radius=0.10, width=width,
                               height=content.height + 2 * pad,
                               stroke_color=color, stroke_width=1.9,
                               fill_color=PANEL_FILL, fill_opacity=0.55)
        content.move_to(box.get_center())
        return VGroup(box, content)

    def answer_row(self, tag, headline, note, color, width=8.60, height=0.50):
        """One revealed answer: its letter, the result and a short note."""
        lab = board_text(tag, 16, color, "BOLD")
        name = board_text(headline, 16, color, "BOLD")
        txt = board_text(note, 14, CHALK_WHITE, "BOLD")
        row = VGroup(lab, name, txt).arrange(RIGHT, buff=0.42)
        box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                               stroke_color=color, stroke_width=1.8,
                               fill_color=PANEL_FILL, fill_opacity=0.6)
        row.move_to(box.get_center())
        return VGroup(box, row)

    def rule_row(self, tag, name, note, color, hot, y, width=8.60,
                 height=0.58, pict_scale=0.16):
        """One row of the six-rule recap: the rule's own picture on the left
        (the parallel lines with its pair lit in the rule colour), then the
        number, the name and the equation.

        The picture sits inside the row's own box and is returned inside the
        same VGroup, so the row is one object: the layout audit never reads it
        as a figure drawn behind somebody else's card."""
        pict = self.figure(fill=0.0, marks=False, hot=hot, hot_color=color,
                           scale=pict_scale, about=(-1.00, 0.30))
        tagt = board_text(tag, 15, color, "BOLD")
        nm = board_text(name, 15, color, "BOLD")
        nt = board_text(note, 13, CHALK_WHITE, "BOLD")
        text = VGroup(tagt, nm, nt).arrange(RIGHT, buff=0.30)
        box = RoundedRectangle(corner_radius=0.09, width=width, height=height,
                               stroke_color=color, stroke_width=1.7,
                               fill_color=PANEL_FILL, fill_opacity=0.55)
        box.move_to(np.array([BOARD_CX, float(y), 0.0]))
        pict.move_to(np.array([BOARD_CX - width / 2 + 0.62, float(y), 0.0]))
        text.next_to(pict, RIGHT, buff=0.30)
        text.move_to(np.array([text.get_center()[0], float(y), 0.0]))
        return VGroup(box, pict, text)

    # -- Scene 0: title ------------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = at(board_text("Angles and Parallel Lines", 25, CHALK_PINK,
                                  "BOLD"), BOARD_CX, 2.06)
            sub = at(board_text("When a transversal cuts two parallel lines", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, 1.42)

            fig = self.figure(fill=0.0, scale=0.55, about=(-1.30, 0.10))
            c1 = at(chip("8 ANGLES", CHALK_CYAN, size=15), COL_X, 0.88)
            c2 = at(chip("6 RELATIONSHIPS", CHALK_GREEN, size=15), COL_X, 0.16)
            c3 = at(chip("1 EQUATION", CHALK_YELLOW, size=15), COL_X, -0.56)
            strip = at(board_text("Two parallel lines and a transversal make "
                                  "eight angles.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(title, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(fig), run_time=0.90)
            self.play(FadeIn(c1, scale=0.9), FadeIn(strip, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(c2, scale=0.9), FadeIn(c3, scale=0.9),
                      run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.closing(tracker, c3)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: the lines and the transversal ------------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("Parallel Lines and a Transversal", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Two lines that never meet, cut by one line.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            pair = par_pair()
            tra = transversal()

            arcs = VGroup(*[angle_arc(n, width=2.0) for n in range(1, 9)])

            i1 = self.col_item("PARALLEL LINES", "they never meet", CHALK_WHITE,
                               0.85)
            i2 = self.col_item("TRANSVERSAL", "one line across", CHALK_AMBER,
                               -0.35)

            banner = at(board_text("ONE LINE CROSSES TWO PARALLEL LINES", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("A transversal cutting parallel lines makes "
                                  "eight angles.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(pair.l1), Create(pair.l2),
                      FadeIn(i1, shift=RIGHT * 0.10), run_time=0.70)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(pair.marks), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Create(tra), FadeIn(i2, shift=RIGHT * 0.10),
                      run_time=0.65)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(Create(arcs), run_time=0.70)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: the eight angles and the two regions -----------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("Eight Angles, Two Regions", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Four angles at each crossing.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill=0.0, band_on=False)
            nums_up = self.numbers((1, 2, 3, 4))
            nums_low = self.numbers((5, 6, 7, 8))
            inter = band()

            i1 = self.col_item("INTERIOR", "angles 3, 4, 5, 6", CHALK_GREEN,
                               0.85)
            i2 = self.col_item("EXTERIOR", "angles 1, 2, 7, 8", CHALK_CYAN,
                               -0.35)

            strip = at(board_text("Angles 3, 4, 5 and 6 lie between the parallel "
                                  "lines.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(fig), run_time=0.80)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(nums_up, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(nums_low, scale=0.9), FadeIn(inter),
                      FadeIn(i1, shift=RIGHT * 0.10), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(i2, shift=RIGHT * 0.10),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: vertically opposite and the linear pair --------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Vertically Opposite and Linear Pairs", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("What happens at one crossing.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            v = RULE_COLOR["vertical"]
            fig = self.figure(fill=0.0, numbers=range(1, 9), num_size=14)
            hi1 = self.highlight((1, 4), v)
            hi2 = self.highlight((1, 2), v)
            hi3 = self.highlight((5, 8), v)

            i1 = self.col_item("VERTICALLY OPPOSITE", "angle 1 = angle 4", v,
                               0.85)
            i2 = self.col_item("LINEAR PAIR", "angle 1 + angle 2 = 180", v,
                               -0.35)

            banner = at(board_text("VERTICALLY OPPOSITE ANGLES ARE EQUAL", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Angles on a straight line add up to 180 "
                                  "degrees.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(fig), run_time=0.80)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(hi1), FadeIn(i1, shift=RIGHT * 0.10), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(hi2), FadeIn(i2, shift=RIGHT * 0.10), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(hi3), run_time=0.50)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: corresponding angles ---------------------------------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("Corresponding Angles", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The same position at each crossing.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            c = RULE_COLOR["corresponding"]
            fig = self.figure(fill=0.0, numbers=range(1, 9), num_size=14)
            hi1 = self.highlight((1, 5), c)
            hi2 = self.highlight((2, 6), c)
            hi3 = self.highlight((3, 7, 4, 8), c)

            i1 = self.col_item("1 AND 5", "both at the top left", c, 0.85)
            i2 = self.col_item("2 AND 6", "both at the top right", c, -0.35)

            banner = at(board_text("CORRESPONDING ANGLES ARE EQUAL", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Angle 3 = angle 7, and angle 4 = angle 8.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(fig), run_time=0.80)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(hi1), FadeIn(i1, shift=RIGHT * 0.10), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(hi2), FadeIn(i2, shift=RIGHT * 0.10), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(hi3), run_time=0.55)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: alternate interior angles ----------------------------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("Alternate Interior Angles", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Opposite sides, between the lines.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            c = RULE_COLOR["alt_interior"]
            fig = self.figure(fill=0.0, band_on=True, numbers=range(1, 9),
                              num_size=14)
            hi1 = self.highlight((4, 5), c)
            hi2 = self.highlight((3, 6), c)

            i1 = self.col_item("4 AND 5", "opposite sides, inside", c, 0.85)
            i2 = self.col_item("3 AND 6", "opposite sides, inside", c, -0.35)

            banner = at(board_text("ALTERNATE INTERIOR ANGLES ARE EQUAL", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Both alternate interior pairs are equal.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(fig), run_time=0.80)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(hi1), FadeIn(i1, shift=RIGHT * 0.10), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(hi2), FadeIn(i2, shift=RIGHT * 0.10), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: same-side interior angles ----------------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("Same-Side Interior Angles", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Between the lines, on one side.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            c = RULE_COLOR["same_side_interior"]
            fig = self.figure(fill=0.0, band_on=True, numbers=range(1, 9),
                              num_size=14)
            hi1 = self.highlight((3, 5), c)
            hi2 = self.highlight((4, 6), c)

            i1 = self.col_item("3 AND 5", "angle 3 + angle 5 = 180", c, 0.85)
            i2 = self.col_item("4 AND 6", "angle 4 + angle 6 = 180", c, -0.35)

            banner = at(board_text("SAME-SIDE INTERIOR ANGLES ADD TO 180", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Together they make a straight angle.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(fig), run_time=0.80)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(hi1), FadeIn(i1, shift=RIGHT * 0.10), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(hi2), FadeIn(i2, shift=RIGHT * 0.10),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: the two exterior rules -------------------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Two Exterior Rules", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Outside the parallel lines.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            ca = RULE_COLOR["alt_exterior"]
            cs = RULE_COLOR["same_side_exterior"]
            fig = self.figure(fill=0.0, numbers=range(1, 9), num_size=14)
            hi1 = self.highlight((2, 7), ca)
            hi2 = self.highlight((1, 8), ca)
            hi3 = self.highlight((1, 7), cs)
            hi4 = self.highlight((2, 8), cs)

            i1 = self.col_item("ALTERNATE EXTERIOR", "2 = 7 and 1 = 8", ca, 0.85)
            i2 = self.col_item("SAME-SIDE EXTERIOR", "1 + 7 = 180, 2 + 8 = 180",
                               cs, -0.35)

            banner = at(board_text("EXTERIOR PAIRS: EQUAL OR 180", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Outside the lines: two pairs equal, two pairs "
                                  "180.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(fig), run_time=0.80)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(hi1), FadeIn(i1, shift=RIGHT * 0.10), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(hi2), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(hi3), FadeIn(i2, shift=RIGHT * 0.10), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(hi4), FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: from the rule to a linear equation -------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("From the Rule to an Equation", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Same-side interior angles: they add to 180.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            c = RULE_COLOR["same_side_interior"]
            fig = self.figure(fill=0.0, band_on=True, hot=(3, 5),
                              hot_color=c, numbers=range(1, 9), num_size=14)

            r1 = at(chalk_math(r"(3x + 20) + (5x - 8) = 180", size=26, color=c),
                    COL_X, 1.45)
            r2 = at(chalk_math(r"8x + 12 = 180", size=26, color=CHALK_WHITE),
                    COL_X, 0.80)
            r3 = at(chalk_math(r"8x = 168", size=26, color=CHALK_WHITE),
                    COL_X, 0.15)
            r4 = at(chalk_math(r"x = 21", size=26, color=CHALK_YELLOW),
                    COL_X, -0.50)
            r5 = at(chalk_math(r"83^\circ \text{ and } 97^\circ", size=24,
                               color=c), COL_X, -1.15)

            strip = at(board_text("x = 21, so the angles are 83 and 97 degrees.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(fig), run_time=0.80)

            self.wait(leftover(tracker, "b0"))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(r1, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(r2, scale=0.9), run_time=0.40)
            self.play(FadeIn(r3, scale=0.9), run_time=0.40)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(r4, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(r5, scale=0.9), FadeIn(strip, shift=UP * 0.06),
                      run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 9: the same routine on a second pair --------------------------
    def beat_s9(self) -> None:
        with self.voiceover(text=NARRATION["s9"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Same Routine, Another Pair", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Corresponding angles: the two are equal.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            c = RULE_COLOR["corresponding"]
            fig = self.figure(fill=0.0, numbers=range(1, 9), num_size=14,
                              hot=(1, 5), hot_color=c)

            r1 = at(chalk_math(r"5x = 2x + 24", size=26, color=c), COL_X, 1.45)
            r2 = at(chalk_math(r"3x = 24", size=26, color=CHALK_WHITE), COL_X,
                    0.80)
            r3 = at(chalk_math(r"x = 8", size=26, color=CHALK_YELLOW), COL_X,
                    0.15)
            r4 = at(chalk_math(r"40^\circ \text{ and } 40^\circ", size=24,
                               color=c), COL_X, -0.50)

            banner = at(board_text("EQUAL ANGLES GIVE AN EQUATION", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("x = 8, and both angles are 40 degrees.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(fig), run_time=0.80)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(r1, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(r2, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(r3, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(r4, scale=0.9), FadeIn(strip, shift=UP * 0.06),
                      run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 10: your turn (questions, the silent clock, then the answers) --
    def beat_s9q(self) -> None:
        with self.voiceover(text=NARRATION["s9q"]) as tracker:
            self.reset_board()

            heading = at(board_text("YOUR TURN", 26, CHALK_PINK, "BOLD"),
                         BOARD_CX, 2.78)
            sub = at(board_text("Four quick checks.", 16, CHALK_WHITE, "BOLD"),
                     BOARD_CX, 2.20)

            mini = dict(scale=0.30, about=(-1.00, 0.30), fill=0.0)
            qa = at(self.q_card("same position",
                                self.figure(hot=(1, 5), hot_color=CHALK_YELLOW,
                                            **mini), CHALK_CYAN), -2.80, 0.92)
            qb = at(self.q_card("opposite sides",
                                self.figure(hot=(4, 5), hot_color=CHALK_YELLOW,
                                            **mini), CHALK_CYAN), 3.70, 0.92)
            qc = at(self.q_card("same side",
                                self.figure(hot=(3, 5), hot_color=CHALK_YELLOW,
                                            **mini), CHALK_CYAN), -2.80, -1.02)
            qd = at(self.ask_card("corresponding angles",
                                  ["2x + 10  and  3x - 30", "find x"],
                                  CHALK_PINK, line_size=13), 3.70, -1.02)

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
            a1 = at(self.answer_row("A", "corresponding",
                                    "the pair are equal", CHALK_PINK),
                    BOARD_CX, 1.62)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "alternate interior",
                                    "the pair are equal", CHALK_RED),
                    BOARD_CX, 0.82)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "same-side interior",
                                    "they add to 180 degrees",
                                    RULE_COLOR["same_side_interior"]),
                    BOARD_CX, 0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "x = 40",
                                    "2x + 10 = 3x - 30, so each angle is 90",
                                    CHALK_YELLOW), BOARD_CX, -0.78)
            self.play(FadeIn(a4, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, a4)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 10: the six rules, then the spoken thank-you ------------------
    def beat_s10(self) -> None:
        with self.voiceover(text=NARRATION["s10"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Six Relationships", 22, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)

            rows = [("1", "CORRESPONDING", "angle 1 = angle 5", (1, 5),
                     RULE_COLOR["corresponding"]),
                    ("2", "ALTERNATE INTERIOR", "angle 4 = angle 5", (4, 5),
                     RULE_COLOR["alt_interior"]),
                    ("3", "ALTERNATE EXTERIOR", "angle 2 = angle 7", (2, 7),
                     RULE_COLOR["alt_exterior"]),
                    ("4", "VERTICALLY OPPOSITE", "angle 1 = angle 4", (1, 4),
                     RULE_COLOR["vertical"]),
                    ("5", "SAME-SIDE INTERIOR", "angle 3 + angle 5 = 180",
                     (3, 5), RULE_COLOR["same_side_interior"]),
                    ("6", "SAME-SIDE EXTERIOR", "angle 1 + angle 7 = 180",
                     (1, 7), RULE_COLOR["same_side_exterior"])]
            ys = (2.05, 1.39, 0.73, 0.07, -0.59, -1.25)
            r = [self.rule_row(t, h, n, c, hot, y)
                 for (t, h, n, hot, c), y in zip(rows, ys)]

            strip = at(board_text("Geometry gives the rule, and the equation "
                                  "finds x.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)
            thanks = at(board_text("Thank You for Watching!", 30, CHALK_WHITE,
                                   "BOLD"), BOARD_CX, 0.62)
            bye = at(board_text("See you in the next lesson :)", 22, CHALK_YELLOW,
                                "BOLD"), BOARD_CX, -0.32)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(r[0], shift=UP * 0.06), run_time=0.40)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(r[1], shift=UP * 0.06), run_time=0.35)
            self.play(FadeIn(r[2], shift=UP * 0.06), run_time=0.35)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(r[3], shift=UP * 0.06), run_time=0.40)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(r[4], shift=UP * 0.06), run_time=0.35)
            self.play(FadeIn(r[5], shift=UP * 0.06), run_time=0.35)
            self.add_sound(self.sfx["success"], gain=-11)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeOut(heading), *[FadeOut(x) for x in r],
                      FadeOut(strip), run_time=0.55)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.50)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.closing(tracker, thanks, run_time=1.2)
            self._capture_srt(tracker)

        self.wait(END_HOLD)

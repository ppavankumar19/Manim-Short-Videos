"""
Why 4 Sides Aren't Enough -- the 5-Measurement Rule
Story-mode chalkboard lesson (Telangana Class 8 Maths, Chapter 3:
Construction of Quadrilaterals, Storymode 01).

LLM KEY / FUNCTION NAME: quadrilateral_uniqueness_and_five_measurements

Production pipeline (mirrors the rest of the Story-Mode series):
  - Shared assets/background2.png chalkboard backdrop + student/teacher
    cutouts + corner badges (dhimantAI top-left, Mathematics top-right).
  - VoiceoverScene + speech service; narration written as continuous prose.
  - Real per-word sync via <bookmark> tags + tracker timing, and a
    ground-truth SRT export from the service word boundaries.
  - Sound effects from sound_effects.py; chalk-styled Text (Segoe Print)
    and MathTex; shared story_common.play_challenge_countdown() for the
    YOUR TURN THINK clock.

The defining visual: a rigid-stick quadrilateral whose four sides never
change length, sheared continuously rectangle -> parallelogram -> back, and
then locked by a fifth stick along the diagonal BD.

Title + 10 scenes:
  0. Title card.
  1. Kamal and Joseph, same four sides, different shapes.
  2. Four sticks (8, 8, 6, 6) assemble into a rectangle.
  3. The shear: angles change, lengths do not.
  4. What unique means: the three shapes are not congruent.
  5. The fifth measurement: diagonal BD locks the frame.
  6. Why it works: two triangles fixed by SSS.
  7. The five-measurement rule and the construction combinations.
  8. Real world: a window frame and its diagonal brace.
  9. Your turn: which fifth measurement is independent?
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
    Indicate, Flash, Circumscribe, SurroundingRectangle, config,
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
               label=None, other_angle=False, right_angle=False) -> VGroup:
    """The angle at `vertex` between the two sides.

    A right angle gets the square symbol (the reversed L), never a curve: that
    is how a 90 degree corner is marked on a drawing.  Any other angle gets a
    chalk arc, with an optional degree label on the bisector."""
    l1 = Line(vertex, p1)
    l2 = Line(vertex, p2)
    if right_angle:
        mark = RightAngle(l1, l2, length=radius * 0.70, color=color,
                          stroke_width=2.8)
    else:
        # the interior angle: a parallelogram corner is always under 180
        # degrees, so the arc must sweep between the two sides, never outside
        mark = Angle(l1, l2, radius=radius, color=color, stroke_width=2.4)
    grp = VGroup(mark)
    if label is not None:
        v = np.array(vertex, dtype=float)
        d1 = np.array(p1, dtype=float) - v
        d2 = np.array(p2, dtype=float) - v
        d1 = d1 / (np.linalg.norm(d1[:2]) or 1.0)
        d2 = d2 / (np.linalg.norm(d2[:2]) or 1.0)
        bis = d1 + d2
        bis = bis / (np.linalg.norm(bis[:2]) or 1.0)
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

# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "Why are four sides not enough?<bookmark mark='b0'/> Today we build a "
        "quadrilateral out of four rigid sticks, and we find out what it takes "
        "to fix its shape completely.<bookmark mark='b1'/>"
    ),
    "scene1": (
        "Kamal and Joseph are both asked to draw a frame eight centimetres "
        "long and six centimetres wide.<bookmark mark='b0'/> Kamal draws a "
        "rectangle, and Joseph draws a slanted frame.<bookmark mark='b1'/> "
        "Every side matches: eight, six, eight, six.<bookmark mark='b2'/> So "
        "if the measurements match, why are the shapes different?"
        "<bookmark mark='b3'/>"
    ),
    "scene2": (
        "Let us build the frame ourselves.<bookmark mark='b0'/> Here are four "
        "rigid sticks: two of length eight centimetres, and two of length six."
        "<bookmark mark='b1'/> We join them at the corners, and they form a "
        "rectangle.<bookmark mark='b2'/> The four side lengths are now fixed. "
        "<bookmark mark='b3'/>"
    ),
    "scene3": (
        "But watch the joints.<bookmark mark='b0'/> If we push the top of the "
        "frame sideways, the angles change, and the rectangle leans into a "
        "parallelogram.<bookmark mark='b1'/> Push the other way, and it leans "
        "the other way.<bookmark mark='b2'/> All three shapes have exactly the "
        "same four side lengths.<bookmark mark='b3'/> The angles changed, but "
        "the lengths did not.<bookmark mark='b4'/>"
    ),
    "scene4": (
        "So what does unique really mean?<bookmark mark='b0'/> It means that "
        "everyone using the same measurements must end up with the same shape, "
        "allowing for turning, sliding or flipping it.<bookmark mark='b1'/> "
        "But these three shapes are not congruent: their angles are different."
        "<bookmark mark='b2'/> Four side measurements are not enough."
        "<bookmark mark='b3'/>"
    ),
    "scene5": (
        "So let us add one more measurement.<bookmark mark='b0'/> We fix a "
        "fifth stick along the diagonal, from B to D.<bookmark mark='b1'/> Now "
        "push the frame again, with exactly the same force as before."
        "<bookmark mark='b2'/> The frame does not move: the diagonal holds it "
        "in place.<bookmark mark='b3'/> Four sides plus one fixed diagonal "
        "gives a fixed shape.<bookmark mark='b4'/>"
    ),
    "scene6": (
        "Why does one diagonal do so much?<bookmark mark='b0'/> It cuts the "
        "quadrilateral into two triangles.<bookmark mark='b1'/> In triangle A "
        "B D we know the three sides: A B, A D and the diagonal B D."
        "<bookmark mark='b2'/> In triangle B C D we know B C, C D and the same "
        "diagonal B D.<bookmark mark='b3'/> Three sides fix a triangle, so "
        "both triangles are fixed, and the quadrilateral is fixed with them."
        "<bookmark mark='b4'/>"
    ),
    "scene7": (
        "This gives us the five measurement rule.<bookmark mark='b0'/> Four "
        "sides, plus one suitable independent measurement.<bookmark mark='b1'/> "
        "A diagonal works, and so do some combinations of sides, angles and "
        "diagonals.<bookmark mark='b2'/> The measurements must be independent "
        "and consistent, and not repeat what we already know.<bookmark "
        "mark='b3'/>"
    ),
    "scene8": (
        "Builders use exactly this idea.<bookmark mark='b0'/> A window frame "
        "on its own can lean, just like our four sticks.<bookmark mark='b1'/> "
        "Fit one diagonal brace, and the frame becomes rigid.<bookmark "
        "mark='b2'/>"
    ),
    "scene9_setup": (
        "Your turn.<bookmark mark='b0'/> Our frame has sides eight, six, eight "
        "and six.<bookmark mark='b1'/> Which extra measurement will fix its "
        "shape?<bookmark mark='b2'/> Option A, measure an eight centimetre "
        "side again. Option B, fix the length of the diagonal B D. Option C, "
        "state that the perimeter is twenty eight centimetres.<bookmark "
        "mark='b3'/> Pause the video and choose.<bookmark mark='b4'/>"
    ),
    "scene9_reveal": (
        "Let us check.<bookmark mark='b0'/> Option A only repeats information "
        "we already have.<bookmark mark='b1'/> And the perimeter is eight plus "
        "six plus eight plus six, which is twenty eight, so option C adds "
        "nothing new either.<bookmark mark='b2'/> Option B fixes the diagonal, "
        "and that locks the frame.<bookmark mark='b3'/> The fifth measurement "
        "must add new information.<bookmark mark='b4'/>"
    ),
    "scene10": (
        "Let us put it together.<bookmark mark='b0'/> Four sides alone allow "
        "many different shapes.<bookmark mark='b1'/> Add one suitable "
        "independent measurement, and the quadrilateral becomes unique."
        "<bookmark mark='b2'/> Five independent measurements determine a "
        "unique quadrilateral.<bookmark mark='b3'/> Thank you for watching!"
        "<bookmark mark='b4'/> See you in the next lesson!<bookmark mark='b5'/>"
    ),
}

class QuadrilateralUniquenessStory(VoiceoverScene):
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
        out_dir = _HERE / "media" / "videos" / "quadrilateral_uniqueness_and_five_measurements"
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
        # re-time every narration clip against the audio it will actually
        # play, so the bookmarks follow the real speech
        install_synced_voiceover(self)

        self.add_background()

        self.beat0_title()
        self.beat1_sheets()
        self.beat2_sticks()
        self.beat3_shear()
        self.beat4_unique()
        self.beat5_diagonal()
        self.beat6_triangles()
        self.beat7_rule()
        self.beat8_window()
        self.beat9_challenge()
        self.beat10_recap()

        self._write_real_srt()

    # ================================================================ beats ==

    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Why 4 Sides Aren't Enough", 34, CHALK_WHITE,
                               "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 1.85, 0]))
            sub = board_text("The 5-Measurement Rule for Quadrilaterals", 21,
                             CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 0.95, 0]))
            # written quickly (a slow write looks like a clipped title) and
            # spaced so the descender of "Enough" cannot touch the subtitle
            self.play(FadeIn(title, shift=UP * 0.1), run_time=quick(
                tracker.time_until_bookmark("b0") * 0.5))
            self.play(FadeIn(sub, shift=UP * 0.1), run_time=quick(
                tracker.time_until_bookmark("b0") * 0.5))
            self.play(Indicate(sub, color=CHALK_YELLOW, scale_factor=1.04),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # the whole idea in one picture: a leaning frame, then its brace
            lean = frame_at(58 * DEGREES,
                            centre=np.array([BOARD_CX, -1.15, 0]),
                            a=1.6, b=1.2)
            brace = diagonal_stick(*lean.corners, CHALK_GREEN)
            tag = board_text("4 sides + 1 suitable measurement = 1 shape", 18,
                             CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX, -2.5, 0]))
            self.play(FadeIn(lean, shift=DOWN * 0.1), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.5))
            self.play(Create(brace), FadeIn(tag, shift=UP * 0.1),
                      Flash(brace, color=CHALK_GREEN, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: Kamal and Joseph, same sides, different shapes -------------
    def beat1_sheets(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("A Geometry Challenge", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            kamal = drawing_sheet("Kamal", BOARD_CX - 1.95, 0.35,
                                  w=3.4, h=3.0)
            joseph = drawing_sheet("Joseph", BOARD_CX + 1.95, 0.35,
                                   w=3.4, h=3.0)
            # smaller figures: the drawing, its four labels and the sheet border
            # all have to fit inside the sheet
            k_shape = sheet_shape(kamal, 90 * DEGREES, a=1.30, b=0.95,
                                  color=CHALK_CYAN)
            j_shape = sheet_shape(joseph, 56 * DEGREES, a=1.30, b=0.95,
                                  color=CHALK_PINK)
            sides = ("8 cm", "6 cm", "8 cm", "6 cm")

            def labels(shape, sheet, colour):
                return VGroup(*[
                    side_label(shape.corners[i], shape.corners[(i + 1) % 4],
                               sheet.paper.get_center(), sides[i], colour,
                               14, 0.16)
                    for i in range(4)])

            k_lab = labels(k_shape, kamal, CHALK_CYAN)
            j_lab = labels(j_shape, joseph, CHALK_PINK)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=quick(
                tracker.time_until_bookmark("b0") * 0.25))
            self.play(FadeIn(kamal), FadeIn(joseph), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.5))
            self.play(Create(k_shape.poly), FadeIn(k_lab), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(Create(j_shape.poly), FadeIn(j_lab), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)

            tag = board_text("Same Four Sides. Different Shapes!", 20,
                             CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.35, 0]))
            self.play(*[Indicate(k_lab[i], color=CHALK_WHITE, scale_factor=1.2)
                        for i in range(4)],
                      *[Indicate(j_lab[i], color=CHALK_WHITE, scale_factor=1.2)
                        for i in range(4)],
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.4))
            self.play(FadeIn(tag, shift=UP * 0.1),
                      Flash(k_shape.poly, color=CHALK_CYAN, flash_radius=0.5),
                      Flash(j_shape.poly, color=CHALK_PINK, flash_radius=0.5),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            question = board_text(
                "If the measurements match, why don't the shapes?", 18,
                CHALK_WHITE, "BOLD").move_to(np.array([BOARD_CX, -2.15, 0]))
            self.play(FadeIn(question, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: four rigid sticks build the frame --------------------------
    def beat2_sticks(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("Four Sticks, One Rectangle", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            # two long sticks (8 cm) and two short ones (6 cm), laid out loose
            l1 = stick(np.array([-3.5, 1.9, 0]), np.array([-0.7, 1.9, 0]),
                       CHALK_AMBER)
            l2 = stick(np.array([0.9, 1.9, 0]), np.array([3.7, 1.9, 0]),
                       CHALK_AMBER)
            s1 = stick(np.array([-3.5, 0.45, 0]), np.array([-1.9, 0.45, 0]),
                       CHALK_CYAN)
            s2 = stick(np.array([0.9, 0.45, 0]), np.array([2.5, 0.45, 0]),
                       CHALK_CYAN)
            l_lab = board_text("8 cm", 16, CHALK_AMBER, "BOLD").next_to(
                l1, UP, buff=0.12)
            l2_lab = board_text("8 cm", 16, CHALK_AMBER, "BOLD").next_to(
                l2, UP, buff=0.12)
            s_lab = board_text("6 cm", 16, CHALK_CYAN, "BOLD").next_to(
                s1, DOWN, buff=0.12)
            s2_lab = board_text("6 cm", 16, CHALK_CYAN, "BOLD").next_to(
                s2, DOWN, buff=0.12)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=quick(
                tracker.time_until_bookmark("b0") * 0.5))
            self.play(FadeIn(l1), FadeIn(l2), FadeIn(l_lab), FadeIn(l2_lab),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.play(FadeIn(s1), FadeIn(s2), FadeIn(s_lab), FadeIn(s2_lab),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            # the sticks travel to their places and the joints pin them
            target = frame_at(90 * DEGREES,
                              centre=np.array([BOARD_CX, 0.15, 0]),
                              with_joints=False)
            self.play(ReplacementTransform(l1, target[0]),
                      ReplacementTransform(s1, target[1]),
                      ReplacementTransform(l2, target[2]),
                      ReplacementTransform(s2, target[3]),
                      FadeOut(l_lab), FadeOut(l2_lab), FadeOut(s_lab),
                      FadeOut(s2_lab),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.6))
            pin = VGroup(*[joint(p) for p in target.corners])
            self.play(FadeIn(pin, scale=0.5), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.4))
            self.add_sound(self.sfx["click"], gain=-15)

            A, B, C, D = target.corners
            centre = target.get_center()
            a_lab = side_label(A, B, centre, "8 cm", CHALK_AMBER, 17, 0.32)
            b_lab = side_label(B, C, centre, "6 cm", CHALK_CYAN, 17, 0.32)
            c_lab = side_label(C, D, centre, "8 cm", CHALK_AMBER, 17, 0.32)
            d_lab = side_label(D, A, centre, "6 cm", CHALK_CYAN, 17, 0.32)
            self.play(FadeIn(a_lab), FadeIn(b_lab), FadeIn(c_lab),
                      FadeIn(d_lab), run_time=rt(
                          tracker.time_until_bookmark("b2") * 0.5))
            self.add_sound(self.sfx["ding"], gain=-13)

            rule = MathTex(r"AB=CD=8\ \text{cm}", r"\qquad",
                           r"BC=DA=6\ \text{cm}", font_size=30,
                           color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, -2.15, 0]))
            # the lengths rule fades in whole, then is emphasised for the rest
            # of its window (a capped write here would leave the beat short)
            self.play(FadeIn(rule, shift=UP * 0.08), run_time=quick(
                tracker.time_until_bookmark("b3") * 0.35))
            self.play(Indicate(rule, color=CHALK_GREEN, scale_factor=1.05),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: the shear ---------------------------------------------------
    def beat3_shear(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()

            heading = board_text("The Angles Changed. The Lengths Didn't!", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            centre = np.array([BOARD_CX, 0.35, 0])
            theta = ValueTracker(90 * DEGREES)

            def live_frame():
                th = theta.get_value()
                deg = th / DEGREES
                grp = frame_at(th, centre)
                A, B, C, D = grp.corners
                labs = VGroup(
                    side_label(A, B, grp.get_center(), "8 cm", CHALK_AMBER,
                               16, 0.32),
                    side_label(B, C, grp.get_center(), "6 cm", CHALK_CYAN,
                               16, 0.32),
                    side_label(C, D, grp.get_center(), "8 cm", CHALK_AMBER,
                               16, 0.32),
                    side_label(D, A, grp.get_center(), "6 cm", CHALK_CYAN,
                               16, 0.32),
                    # at the rectangle the corner is marked with the square
                    # (reversed L) symbol; every other angle gets an arc and
                    # its degree reading
                    angle_mark(A, B, D,
                               color=CHALK_PINK,
                               label=(None if abs(deg - 90) < 3
                                      else f"{int(round(deg))}°"),
                               right_angle=abs(deg - 90) < 3),
                )
                return VGroup(grp, labs)

            live = always_redraw(live_frame)
            self.play(FadeIn(heading, shift=UP * 0.08), run_time=quick(
                tracker.time_until_bookmark("b0") * 0.5))
            self.play(FadeIn(live), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            push = force_arrow(1.15, 4.6, 3.15)
            self.play(GrowArrow(push), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.25))
            self.play(theta.animate.set_value(56 * DEGREES),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.75))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(theta.animate.set_value(124 * DEGREES),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.8))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(theta.animate.set_value(90 * DEGREES),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.2))

            # the three configurations side by side, each labelled with its
            # interior angle -- far clearer than three overlapping outlines
            trio = VGroup()
            for x, th, name, col in (
                    (BOARD_CX - 2.75, 90 * DEGREES, "90°", CHALK_WHITE),
                    (BOARD_CX, 56 * DEGREES, "56°", CHALK_CYAN),
                    (BOARD_CX + 2.75, 124 * DEGREES, "124°", CHALK_PINK)):
                A, B, C, D = quad_points(np.array([x, 0.15, 0]), th, 1.35, 1.0)
                poly = Polygon(A, B, C, D, color=col, stroke_width=2.8,
                               fill_color=col, fill_opacity=0.10)
                lab = board_text(name, 17, col, "BOLD").next_to(
                    poly, DOWN, buff=0.24)
                trio.add(VGroup(poly, lab))
            tag = board_text("Same 8, 6, 8, 6 — three different shapes", 19,
                             CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -2.3, 0]))
            # clear the live frame first: cross-fading it into the trio left the
            # old side labels sitting on the new shapes for a second
            self.play(FadeOut(push), FadeOut(live), run_time=rt(
                tracker.time_until_bookmark("b3") * 0.45))
            self.play(FadeIn(trio), FadeIn(tag, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            note = board_text("The angles changed. The lengths didn't!", 20,
                              CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.75, 0]))
            self.play(FadeIn(note, shift=UP * 0.1),
                      Flash(note, color=CHALK_GREEN, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: what "unique" means ----------------------------------------
    def beat4_unique(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()

            heading = board_text("What Does Unique Mean?", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            xs = [BOARD_CX - 2.75, BOARD_CX, BOARD_CX + 2.75]
            thetas = [90 * DEGREES, 56 * DEGREES, 124 * DEGREES]
            colours = [CHALK_WHITE, CHALK_CYAN, CHALK_PINK]
            shapes, labels = VGroup(), VGroup()
            for x, th, col in zip(xs, thetas, colours):
                A, B, C, D = quad_points(np.array([x, 0.75, 0]), th, 1.35, 1.0)
                poly = Polygon(A, B, C, D, color=col, stroke_width=3,
                               fill_color=col, fill_opacity=0.10)
                poly.corners = (A, B, C, D)
                shapes.add(poly)
            for i, (x, col) in enumerate(zip(xs, colours), start=1):
                labels.add(board_text(f"Shape {i}", 17, col, "BOLD").move_to(
                    np.array([x, -0.75, 0])))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=quick(
                tracker.time_until_bookmark("b0") * 0.6))
            self.play(FadeIn(shapes[0]),
                      FadeIn(labels[0]), run_time=rt(
                          tracker.time_until_bookmark("b0")))
            self.play(FadeIn(shapes[1]), FadeIn(labels[1]), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(FadeIn(shapes[2]), FadeIn(labels[2]), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.5))
            meaning = board_text(
                "Unique: everyone gets the same shape, up to turn, slide or flip",
                17, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.5, 0]))
            self.play(FadeIn(meaning, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.5))
            self.add_sound(self.sfx["ding"], gain=-13)

            # slide shape 2 onto shape 1, side AB on side AB: the tops diverge
            A1, B1 = shapes[0].corners[0], shapes[0].corners[1]
            A2, B2 = shapes[1].corners[0], shapes[1].corners[1]
            shift = (A1 + B1) / 2 - (A2 + B2) / 2
            moved = shapes[1].copy().shift(shift)
            dash = DashedLine(shapes[0].corners[2], moved.corners[2],
                              color=CHALK_RED, stroke_width=2.4,
                              dash_length=0.1)
            not_congruent = board_text("Not Congruent", 20, CHALK_RED, "BOLD"
                                       ).move_to(np.array([BOARD_CX, -2.05, 0]))
            apex = Dot(radius=0.07, color=CHALK_RED).move_to(moved.corners[2])
            self.play(FadeOut(labels[1]), FadeOut(shapes[1]),
                      FadeIn(moved), run_time=rt(
                          tracker.time_until_bookmark("b2") * 0.5))
            self.play(Create(dash), FadeIn(not_congruent, shift=UP * 0.1),
                      FadeIn(apex), Indicate(apex, color=CHALK_RED,
                                             scale_factor=2.0),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            self.add_sound(self.sfx["click"], gain=-15)

            conclusion = board_text("Four side measurements are not enough.", 21,
                                    CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.45, 0]))
            self.play(FadeIn(conclusion, shift=UP * 0.1),
                      Flash(conclusion, color=CHALK_GREEN, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: the fifth measurement --------------------------------------
    def beat5_diagonal(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            self.reset_board()

            heading = board_text("The Fifth Measurement", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            centre = np.array([BOARD_CX, 0.3, 0])
            frame = frame_at(90 * DEGREES, centre)
            A, B, C, D = frame.corners
            v_lab = VGroup(
                board_text("A", 18, CHALK_WHITE, "BOLD").next_to(
                    np.array([A[0], A[1], 0]), DL, buff=0.06),
                board_text("B", 18, CHALK_WHITE, "BOLD").next_to(
                    np.array([B[0], B[1], 0]), DR, buff=0.06),
                board_text("C", 18, CHALK_WHITE, "BOLD").next_to(
                    np.array([C[0], C[1], 0]), UR, buff=0.06),
                board_text("D", 18, CHALK_WHITE, "BOLD").next_to(
                    np.array([D[0], D[1], 0]), UL, buff=0.06),
            )
            self.play(FadeIn(heading, shift=UP * 0.08), run_time=quick(
                tracker.time_until_bookmark("b0") * 0.6))
            self.play(FadeIn(frame), FadeIn(v_lab), run_time=rt(
                tracker.time_until_bookmark("b0")))
            ask = board_text("What if we add one more measurement?", 19,
                             CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.5, 0]))
            self.play(FadeIn(ask, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))
            self.add_sound(self.sfx["pop"], gain=-13)

            dashed = diagonal_stick(A, B, C, D, CHALK_GREEN, dashed=True)
            # the label sits off the diagonal: on it, chalk text is unreadable
            bd_lab = board_text("BD", 18, CHALK_GREEN, "BOLD").move_to(
                (B + D) / 2 + np.array([0.38, 0.50, 0]))
            self.play(Create(dashed), FadeIn(bd_lab), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            brace = diagonal_stick(A, B, C, D, CHALK_GREEN)
            self.play(ReplacementTransform(dashed, brace),
                      Flash(brace, color=CHALK_GREEN, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.35))
            push = force_arrow(0.95, 4.65, 3.2)
            self.play(GrowArrow(push), run_time=rt(
                tracker.time_until_bookmark("b2") * 0.25))
            # the rail is held: the push does nothing but the frame quivers
            wobble = frame_at(88 * DEGREES, centre)
            self.play(Transform(frame, wobble),
                      Transform(brace, diagonal_stick(
                          *quad_points(centre, 88 * DEGREES), CHALK_GREEN)),
                      FadeIn(v_lab, scale=1.0),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.4))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            back = frame_at(90 * DEGREES, centre)
            held = board_text("The diagonal holds it in place.", 19,
                              CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -1.5, 0]))
            # the old question leaves before the new line arrives: cross-fading
            # both at y = -1.5 printed them on top of each other
            self.play(FadeOut(ask), FadeOut(push),
                      Transform(frame, back),
                      Transform(brace, diagonal_stick(
                          *quad_points(centre, 90 * DEGREES), CHALK_GREEN)),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            self.play(FadeIn(held, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            rule = MathTex(r"AB,\ BC,\ CD,\ DA,\ BD", font_size=32,
                           color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, -2.2, 0]))
            box = SurroundingRectangle(rule, color=CHALK_GREEN, buff=0.18,
                                       corner_radius=0.1, stroke_width=3)
            # the rule is written quickly and then boxed, instead of being
            # drawn across the whole (long) window
            self.play(FadeIn(rule, shift=UP * 0.08), run_time=quick(
                tracker.time_until_bookmark("b4") * 0.4))
            self.play(Create(box),
                      Flash(rule, color=CHALK_GREEN, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: why the diagonal works -------------------------------------
    def beat6_triangles(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("Two Fixed Triangles", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            centre = np.array([BOARD_CX, 0.35, 0])
            A, B, C, D = quad_points(centre, 90 * DEGREES)
            tri1 = Polygon(A, B, D, color=CHALK_CYAN, stroke_width=0,
                           fill_color=CHALK_CYAN, fill_opacity=0.22)
            tri2 = Polygon(B, C, D, color=CHALK_PINK, stroke_width=0,
                           fill_color=CHALK_PINK, fill_opacity=0.22)
            sides = VGroup(stick(A, B), stick(B, C), stick(C, D), stick(D, A))
            brace = diagonal_stick(A, B, C, D, CHALK_GREEN)
            names = VGroup(
                board_text("A", 18, CHALK_WHITE, "BOLD").next_to(
                    np.array([A[0], A[1], 0]), DL, buff=0.06),
                board_text("B", 18, CHALK_WHITE, "BOLD").next_to(
                    np.array([B[0], B[1], 0]), DR, buff=0.06),
                board_text("C", 18, CHALK_WHITE, "BOLD").next_to(
                    np.array([C[0], C[1], 0]), UR, buff=0.06),
                board_text("D", 18, CHALK_WHITE, "BOLD").next_to(
                    np.array([D[0], D[1], 0]), UL, buff=0.06),
            )
            self.play(FadeIn(heading, shift=UP * 0.08), run_time=quick(
                tracker.time_until_bookmark("b0") * 0.6))
            self.play(FadeIn(sides), FadeIn(names), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.45))
            self.play(Create(brace), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.55))
            self.add_sound(self.sfx["pop"], gain=-13)

            l1 = board_text("AB, AD, BD", 18, CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX - 2.5, -1.35, 0]))
            self.play(FadeIn(tri1), Indicate(brace, color=CHALK_GREEN,
                                             scale_factor=1.05),
                      FadeIn(l1), run_time=rt(
                          tracker.time_until_bookmark("b1") * 0.6))
            self.play(Indicate(l1, color=CHALK_WHITE, scale_factor=1.15),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.4))
            self.add_sound(self.sfx["click"], gain=-15)

            l2 = board_text("BC, CD, BD", 18, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX + 2.5, -1.35, 0]))
            self.play(FadeIn(tri2), FadeIn(l2), run_time=rt(
                tracker.time_until_bookmark("b2") * 0.6))
            self.play(Indicate(l2, color=CHALK_WHITE, scale_factor=1.15),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.4))
            self.add_sound(self.sfx["click"], gain=-15)

            # the triangles part along the diagonal with their vertex letters,
            # so no letter is left floating away from the shape it names
            sep1 = tri1.copy().shift(LEFT * 0.55 + UP * 0.18)
            sep2 = tri2.copy().shift(RIGHT * 0.55 + DOWN * 0.18)
            sss = board_text("Three sides fix a triangle (SSS).", 19,
                             CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -2.05, 0]))
            self.play(FadeOut(tri1), FadeOut(tri2), FadeOut(names),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.3))
            self.play(FadeIn(sep1), FadeIn(sep2), run_time=rt(
                tracker.time_until_bookmark("b3") * 0.35))
            self.play(FadeIn(sss, shift=UP * 0.1),
                      FadeOut(sep1), FadeOut(sep2), FadeIn(tri1), FadeIn(tri2),
                      FadeIn(names),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.35))
            self.add_sound(self.sfx["ding"], gain=-13)

            done = board_text("Two fixed triangles make one fixed quadrilateral.",
                              19, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.4, 0]))
            self.play(FadeIn(done, shift=UP * 0.1),
                      Flash(brace, color=CHALK_GREEN, flash_radius=0.8),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: the five-measurement rule ----------------------------------
    def beat7_rule(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("FIVE INDEPENDENT MEASUREMENTS", 20, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            centre = np.array([BOARD_CX - 2.4, 1.15, 0])
            A, B, C, D = quad_points(centre, 66 * DEGREES, 1.5, 1.15)
            quad = Polygon(A, B, C, D, color=CHALK_WHITE, stroke_width=3,
                           fill_color=CHALK_WHITE, fill_opacity=0.08)
            sides = VGroup(stick(A, B, CHALK_YELLOW, 5.5),
                           stick(B, C, CHALK_YELLOW, 5.5),
                           stick(C, D, CHALK_YELLOW, 5.5),
                           stick(D, A, CHALK_YELLOW, 5.5))
            names = VGroup(
                board_text("A", 16, CHALK_WHITE, "BOLD").next_to(
                    np.array([A[0], A[1], 0]), DL, buff=0.05),
                board_text("B", 16, CHALK_WHITE, "BOLD").next_to(
                    np.array([B[0], B[1], 0]), DR, buff=0.05),
                board_text("C", 16, CHALK_WHITE, "BOLD").next_to(
                    np.array([C[0], C[1], 0]), UR, buff=0.05),
                board_text("D", 16, CHALK_WHITE, "BOLD").next_to(
                    np.array([D[0], D[1], 0]), UL, buff=0.05),
            )
            # the heading is written quickly, then the figure assembles for the
            # rest of the window
            self.play(FadeIn(heading, shift=UP * 0.08), run_time=quick(
                tracker.time_until_bookmark("b0") * 0.5))
            self.play(FadeIn(quad), FadeIn(names), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.5))
            self.play(FadeIn(sides), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            brace = diagonal_stick(A, B, C, D, CHALK_GREEN, dashed=True)
            four = board_text("4 sides", 18, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX + 2.35, 1.55, 0]))
            plus = board_text("+ 1 diagonal", 18, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX + 2.35, 1.05, 0]))
            boxed = SurroundingRectangle(VGroup(four, plus), color=CHALK_WHITE,
                                         buff=0.18, corner_radius=0.1,
                                         stroke_width=2.6)
            self.play(Create(brace), FadeIn(four), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.6))
            self.play(FadeIn(plus), Create(boxed),
                      Flash(boxed, color=CHALK_WHITE, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.4))
            self.add_sound(self.sfx["ding"], gain=-13)

            combos = VGroup(
                combo_card("SSSSD", "4 sides + 1 diagonal", CHALK_GREEN),
                combo_card("SSSSA", "4 sides + 1 angle"),
                combo_card("SSSDD", "3 sides + 2 diagonals"),
                combo_card("SASAA", "2 sides + 3 angles"),
                combo_card("SASAS", "3 sides + 2 angles"),
            ).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX + 2.35, -0.95, 0]))
            self.play(FadeIn(combos), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            note = board_text("Independent, suitable, consistent", 19,
                              CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX - 2.2, -1.9, 0]))
            self.play(FadeIn(note, shift=UP * 0.1),
                      Circumscribe(combos[0], color=CHALK_GREEN,
                                   stroke_width=2.6, time_width=0.6),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the window frame -------------------------------------------
    def beat8_window(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("Make the Frame Rigid", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            centre = np.array([BOARD_CX, 0.35, 0])
            theta = ValueTracker(90 * DEGREES)
            # 0 = no brace, 1 = braced: the window is redrawn from these two
            # trackers, so the brace appears without transforming a redrawn
            # mobject (which corrupts manim's partial-movie cache)
            braced = ValueTracker(0.0)

            def live_window():
                return window_frame(centre, theta.get_value(),
                                    with_brace=braced.get_value() > 0.5)

            live = always_redraw(live_window)
            self.play(FadeIn(heading, shift=UP * 0.08), run_time=quick(
                tracker.time_until_bookmark("b0") * 0.7))
            self.play(FadeIn(live), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            push = force_arrow(1.25, 4.9, 3.4)
            self.play(GrowArrow(push), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.25))
            self.play(theta.animate.set_value(64 * DEGREES),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.75))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(braced.animate.set_value(1.0), run_time=rt(
                tracker.time_until_bookmark("b2") * 0.3))
            self.add_sound(self.sfx["click"], gain=-15)
            note = board_text("One diagonal brace makes it rigid.", 20,
                              CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.2, 0]))
            self.play(theta.animate.set_value(90 * DEGREES),
                      FadeIn(note, shift=UP * 0.1),
                      FadeOut(push), run_time=rt(
                          tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 9: student challenge ------------------------------------------
    def beat9_challenge(self) -> None:
        with self.voiceover(text=NARRATION["scene9_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", 30, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, 2.62, 0]))
            # the figure sits further left and the options further right, so the
            # THINK clock fits in the gap between them without covering either
            centre = np.array([BOARD_CX - 2.9, 0.9, 0])
            frame = frame_at(74 * DEGREES, centre, 1.5, 1.15)
            # vertex letters, as in every other figure in the video: without
            # them the diagonal BD in the reveal has nothing to refer to
            A, B, C, D = frame.corners
            names = VGroup(
                board_text("A", 16, CHALK_WHITE, "BOLD").next_to(
                    np.array([A[0], A[1], 0]), DL, buff=0.08),
                board_text("B", 16, CHALK_WHITE, "BOLD").next_to(
                    np.array([B[0], B[1], 0]), DR, buff=0.08),
                board_text("C", 16, CHALK_WHITE, "BOLD").next_to(
                    np.array([C[0], C[1], 0]), UR, buff=0.08),
                board_text("D", 16, CHALK_WHITE, "BOLD").next_to(
                    np.array([D[0], D[1], 0]), UL, buff=0.08),
            )
            given = MathTex(r"8,\ 6,\ 8,\ 6", font_size=30, color=CHALK_YELLOW
                            ).move_to(np.array([BOARD_CX - 2.9, -0.35, 0]))
            ask = VGroup(
                board_text("Which extra measurement", 17, CHALK_WHITE, "BOLD"),
                board_text("fixes the shape?", 17, CHALK_WHITE, "BOLD"),
            ).arrange(DOWN, buff=0.06).move_to(
                np.array([BOARD_CX - 2.9, -1.0, 0]))
            choices = VGroup(
                choice_row("A", "Measure an 8 cm side again", CHALK_WHITE),
                choice_row("B", "Fix the length of diagonal BD", CHALK_GREEN),
                choice_row("C", "State the perimeter is 28 cm", CHALK_WHITE),
            ).arrange(DOWN, buff=0.52, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX + 2.65, 0.55, 0]))
            for row in choices:
                row[1].scale(0.94)
            pause = board_text("Pause and choose.", 18, CHALK_YELLOW, "BOLD"
                               ).move_to(np.array([BOARD_CX - 2.9, -1.75, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), FadeIn(frame),
                      FadeIn(names),
                      run_time=quick(
                          tracker.time_until_bookmark("b0") * 0.6))
            self.play(FadeIn(given, shift=UP * 0.08), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(FadeIn(ask, shift=RIGHT * 0.12), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            for k, mark in enumerate(("b2",)):
                self.play(FadeIn(choices, shift=RIGHT * 0.12), run_time=rt(
                    tracker.time_until_bookmark(mark) * 0.7))
                self.play(Indicate(choices[k], color=CHALK_WHITE,
                                   scale_factor=1.04), run_time=rt(
                                       tracker.time_until_bookmark(mark) * 0.3))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(pause, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b4")))

            self.challenge = {"frame": frame, "centre": centre,
                              "choices": choices, "ask": ask, "given": given,
                              "pause": pause, "names": names}
            self._capture_srt(tracker)

        # the clock goes in the gap between the figure and the options: at board
        # centre its disc covered the B and C option badges
        play_challenge_countdown(self, seconds=4, sfx=self.sfx,
                                 position=np.array([BOARD_CX, 0.55, 0]))

        with self.voiceover(text=NARRATION["scene9_reveal"]) as tracker:
            ch = self.challenge
            frame, centre = ch["frame"], ch["centre"]
            choices = ch["choices"]

            self.play(FadeOut(ch["pause"]), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.5))
            dim_a = board_text("Repeats what we know.", 16, CHALK_RED, "BOLD"
                               ).next_to(choices[0], DOWN, aligned_edge=LEFT,
                                         buff=0.16)
            self.play(FadeOut(choices[0]), FadeIn(dim_a), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            perimeter = MathTex(r"8+6+8+6=28", font_size=26, color=CHALK_RED
                                ).move_to(np.array([BOARD_CX - 2.5, -1.75, 0]))
            dim_c = board_text("Already known from the sides.", 16, CHALK_RED,
                               "BOLD").next_to(choices[2], DOWN,
                                               aligned_edge=LEFT, buff=0.16)
            self.play(FadeIn(perimeter, shift=UP * 0.08), run_time=quick(
                tracker.time_until_bookmark("b2") * 0.5))
            self.play(FadeOut(choices[2]), FadeIn(dim_c), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            A, B, C, D = frame.corners
            brace = diagonal_stick(A, B, C, D, CHALK_GREEN)
            bd_lab = board_text("BD", 17, CHALK_GREEN, "BOLD").move_to(
                (B + D) / 2 + np.array([0.30, 0.39, 0]))
            answer = board_text("Option B: fix the diagonal BD.", 20,
                                CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX - 2.5, -2.25, 0]))
            self.play(Indicate(choices[1], color=CHALK_GREEN,
                               scale_factor=1.08),
                      Create(brace), FadeIn(bd_lab),
                      # light up the two vertices the diagonal joins
                      Indicate(ch["names"][1], color=CHALK_GREEN,
                               scale_factor=1.6),
                      Indicate(ch["names"][3], color=CHALK_GREEN,
                               scale_factor=1.6),
                      Flash(brace, color=CHALK_GREEN, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.6))
            self.play(FadeIn(answer, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b3") * 0.4))
            self.add_sound(self.sfx["ding"], gain=-13)

            closing = board_text("The fifth measurement must add new information.",
                                 18, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, 2.05, 0]))
            self.play(FadeIn(closing, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap ------------------------------------------------------
    def beat10_recap(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("Five Independent Measurements", 24,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            centre = np.array([BOARD_CX, 1.15, 0])
            theta = ValueTracker(90 * DEGREES)

            def live_frame():
                grp = frame_at(theta.get_value(), centre, 1.95, 1.4)
                return grp

            live = always_redraw(live_frame)
            # the recap rows, as in the rest of the series: one numbered row per
            # recap sentence, each with the measurement it refers to
            rows = VGroup(
                summary_row(1, "Four sides alone:", r"4\ \text{sides}",
                            CHALK_CYAN),
                summary_row(2, "Add one suitable measurement:",
                            r"+1\ \text{measurement}", CHALK_GREEN),
                summary_row(3, "Five independent measurements:",
                            r"5\ \text{measurements}", CHALK_YELLOW),
            ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
            rows.move_to(np.array([BOARD_CX, -0.85, 0]))
            rows.shift(RIGHT * (BOARD_CX - rows.get_center()[0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=quick(
                tracker.time_until_bookmark("b0") * 0.5))
            self.play(FadeIn(live), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.5))
            self.play(theta.animate.set_value(58 * DEGREES), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(theta.animate.set_value(90 * DEGREES),
                      FadeIn(rows[0], shift=RIGHT * 0.12), run_time=rt(
                          tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            A, B, C, D = quad_points(centre, 90 * DEGREES, 1.95, 1.4)
            brace = diagonal_stick(A, B, C, D, CHALK_GREEN)
            self.play(Create(brace), FadeIn(rows[1], shift=RIGHT * 0.12),
                      run_time=rt(
                          tracker.time_until_bookmark("b2") * 0.5))
            self.play(FadeIn(rows[2], shift=RIGHT * 0.12), run_time=rt(
                tracker.time_until_bookmark("b2") * 0.5))
            self.add_sound(self.sfx["success"], gain=-11)

            five = MathTex(r"AB,\ BC,\ CD,\ DA,\ BD", font_size=28,
                           color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, -2.15, 0]))
            fbox = SurroundingRectangle(five, color=CHALK_GREEN, buff=0.16,
                                        corner_radius=0.1, stroke_width=3)
            self.play(FadeIn(five, shift=UP * 0.08), run_time=quick(
                tracker.time_until_bookmark("b3") * 0.4))
            self.play(Create(fbox),
                      Flash(five, color=CHALK_GREEN, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            final = board_text(
                "Five independent measurements determine a unique quadrilateral.",
                18, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -2.72, 0]))
            self.play(FadeIn(final, shift=UP * 0.1),
                      Circumscribe(five, color=CHALK_AMBER, stroke_width=3,
                                   time_width=0.5),
                      run_time=rt(tracker.get_remaining_duration() * 0.6))
            self.add_sound(self.sfx["ding"], gain=-13)

            summary = VGroup(live, rows, brace, five, fbox, final)
            thanks = board_text("Thank You for Watching!", 40, CHALK_WHITE,
                                "BOLD")
            thanks2 = board_text("See you in the next lesson :)", 25,
                                 CHALK_CYAN)
            thanks_group = VGroup(thanks, thanks2).arrange(DOWN, buff=0.3
                                                           ).move_to(
                np.array([BOARD_CX, BOARD_CY, 0]))
            self.play(FadeOut(summary), FadeOut(heading), run_time=rt(
                tracker.time_until_bookmark("b4") * 0.35))
            self.play(Write(thanks), run_time=rt(
                tracker.time_until_bookmark("b4") * 0.65))
            self.add_sound(self.sfx["success"], gain=-11)
            self.play(FadeIn(thanks2, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b5")))
            self.play(Circumscribe(thanks_group, color=CHALK_AMBER,
                                   stroke_width=3, time_width=0.5),
                      run_time=0.25)
            self.play(Indicate(thanks, color=CHALK_WHITE, scale_factor=1.01),
                      run_time=rt(tracker.get_remaining_duration()))
            self._capture_srt(tracker)

        self.wait(END_HOLD)


if __name__ == "__main__":
    pass


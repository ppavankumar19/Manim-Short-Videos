"""
Commutative & Associative Properties of Whole Numbers
Story-mode chalkboard lesson (Telangana Class 6 Maths, Chapter 2: Whole
Numbers, Section 2.4 — properties of whole numbers).

The whole video turns on ONE visual distinction:
  * commutative -> the number tiles physically SWAP places;
  * associative -> the numbers keep their order and only the GROUPING bracket
    moves.
Every scene keeps that difference visible, and grouping is always shown before
anything is evaluated.

Production pipeline (mirrors the rest of the Story-Mode series):
  - shared assets/background2.png chalkboard + student/teacher cutouts +
    dhimantAI (top-left) and Mathematics (top-right) corner badges.
  - VoiceoverScene + speech service; narration written as natural prose.
  - synced_voice.install_synced_voiceover() re-times every word against the
    real audio.
  - real per-line SRT export (carry-safe timestamps).
  - sound effects from sound_effects.py, chalk-styled Text/MathTex.
  - story_common.play_challenge_countdown() for the "YOUR TURN" clock.

Title + 10 scenes:
  0. Title card.
  1. Can We Calculate Smarter? -- 196 + 57 + 4, the 4 moves, (196+4) = 200.
  2. Commutative Property of Addition -- 3 + 4 -> 4 + 3 = 7.
  3. Commutative Property of Multiplication -- the 4x3 dot grid turns 3x4.
  4. The Commutative Rule -- a+b=b+a and a*b=b*a.
  5. Associative Property of Addition -- (3+4)+5 = 3+(4+5) = 12.
  6. Associative Property of Multiplication -- (5x6)x2 = 5x(6x2) = 60.
  7. Commutative vs Associative -- order changes vs grouping changes.
  8. Easier Calculations -- 196+57+4 -> (196+4)+57 -> 257.
  9. Student Challenge -- 238+695+162 = 1095 with the THINK clock.
 10. Summary + the Thank-You template.
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
    ORIGIN, UP, DOWN, LEFT, RIGHT, PI, TAU, DEGREES, BLACK,
    ImageMobject, MathTex, VGroup, Line, DashedLine, Circle, Dot, Triangle,
    Rectangle, RoundedRectangle, Polygon, Arrow, DoubleArrow, Text,
    Write, FadeIn, FadeOut, Create, Transform, ReplacementTransform, TransformMatchingTex,
    TransformFromCopy, GrowArrow, Indicate, Flash, Circumscribe,
    SurroundingRectangle, MoveAlongPath, ArcBetweenPoints, config,
)
from manim_voiceover import VoiceoverScene
from manim_voiceover.tracker import AUDIO_OFFSET_RESOLUTION

from speech_service import get_speech_service
from sound_effects import load_all as load_sfx
from story_common import play_challenge_countdown
from synced_voice import install_synced_voiceover

# --------------------------------------------------------------- theme -----
CHALK_WHITE = "#F5F2E9"
BRAND_WHITE = "#FFFFFF"
CHALK_YELLOW = "#FFE066"
CHALK_PINK = "#FF8FA3"
CHALK_CYAN = "#7FE7DC"
CHALK_AMBER = "#E8B769"
CHALK_GREEN = "#9BE38A"
CHALK_RED = "#FF6B6B"
FONT = "Segoe Print"
MATH_COLOR = CHALK_WHITE

TILE_COLOR = CHALK_CYAN       # the movable number tiles
SWAP_COLOR = CHALK_GREEN      # commutative: things exchange places
GROUP_COLOR = CHALK_PINK      # associative: the grouping bracket
DOT_COLOR = CHALK_AMBER       # counting counters
RESULT_COLOR = CHALK_GREEN

END_HOLD = 2.0
TRANSITION_HOLD = 0.35
MIN_RT = 0.12

# measured chalkboard safe bounds (shared across the series)
BOARD_LEFT = -4.6
BOARD_RIGHT = 5.6
BOARD_TOP = 3.3
BOARD_BOTTOM = -2.9
BOARD_CX = (BOARD_LEFT + BOARD_RIGHT) / 2   # 0.5
BOARD_CY = (BOARD_TOP + BOARD_BOTTOM) / 2   # 0.2

HEAD_Y = BOARD_TOP - 0.45


def rt(seconds: float, floor: float = MIN_RT) -> float:
    return max(floor, float(seconds))


def board_text(s: str, size: int = 34, color: str = CHALK_WHITE,
               weight: str = "NORMAL") -> Text:
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def chalk_math(s: str, size: int = 34, color: str = MATH_COLOR) -> MathTex:
    return MathTex(s, font_size=size, color=color)


def centre_on(mob, cx: float = BOARD_CX, cy: float = 0.0):
    mob.move_to(np.array([cx, cy, 0.0]))
    return mob


def check_mark(color: str = CHALK_GREEN, size: float = 0.4,
               width: float = 5) -> VGroup:
    a = np.array([-0.52, 0.16, 0.0]) * size
    b = np.array([-0.16, -0.30, 0.0]) * size
    c = np.array([0.52, 0.40, 0.0]) * size
    return VGroup(Line(a, b, color=color, stroke_width=width),
                  Line(b, c, color=color, stroke_width=width))


def tick_beside(target, color: str = CHALK_GREEN, size: float = 0.4,
                buff: float = 0.3) -> VGroup:
    mark = check_mark(color, size)
    mark.next_to(target, RIGHT, buff=buff)
    mark.shift(UP * (target.get_center()[1] - mark.get_center()[1]))
    return mark


def drop_shadow(mobj: VGroup, dx: float = 0.045, dy: float = -0.05,
                opacity: float = 0.3) -> VGroup:
    shadow = mobj.copy()
    shadow.set_fill(BLACK, opacity=opacity)
    shadow.set_stroke(width=0)
    shadow.shift(np.array([dx, dy, 0]))
    return VGroup(shadow, mobj)


# ------------------------------------------------------- property furniture --
def num_tile(value, color: str = TILE_COLOR, size: float = 1.0,
             font: int = 32) -> VGroup:
    """A movable number tile: the object that swaps for commutativity."""
    box = RoundedRectangle(corner_radius=0.08, width=size, height=size * 0.82,
                           stroke_color=color, stroke_width=2.2,
                           fill_color="#16202B", fill_opacity=0.85)
    lab = MathTex(str(value), font_size=font, color=color).move_to(box.get_center())
    grp = VGroup(box, lab)
    grp.box, grp.lab = box, lab
    return grp


def plus_sign(color: str = CHALK_WHITE, font: int = 32,
              at=np.array([0.0, 0.0, 0.0])) -> MathTex:
    return MathTex("+", font_size=font, color=color).move_to(at)


def counter_group(n: int, color: str = DOT_COLOR, cols: int | None = None,
                  r: float = 0.1, buff: float = 0.17,
                  pad: float = 0.16) -> VGroup:
    """A little collection of counters inside its own outline."""
    cols = cols or min(n, 3)
    dots = VGroup(*[Dot(radius=r, color=color) for _ in range(n)])
    dots.arrange_in_grid(rows=max(1, -(-n // cols)), cols=cols, buff=buff)
    outline = RoundedRectangle(corner_radius=0.1, width=dots.width + 2 * pad,
                               height=dots.height + 2 * pad,
                               stroke_color=color, stroke_width=1.8,
                               stroke_opacity=0.75,
                               fill_color=color, fill_opacity=0.10)
    outline.move_to(dots.get_center())
    grp = VGroup(outline, dots)
    grp.outline, grp.dots = outline, dots
    return grp


def dot_grid(rows: int, cols: int, *, spacing: float = 0.52, r: float = 0.085,
             color: str = DOT_COLOR) -> VGroup:
    """The same twelve dots in a rectangular arrangement; `grid_targets` gives
    the positions for the transposed arrangement so the dots can move."""
    grp = VGroup(*[Dot(radius=r, color=color) for _ in range(rows * cols)])
    grp.arrange_in_grid(rows=rows, cols=cols, buff=spacing)
    grp.rows, grp.cols, grp.spacing = rows, cols, spacing
    return grp


def grid_targets(grid: VGroup, rows: int, cols: int,
                 centre) -> list[np.ndarray]:
    """Row-major target points for the same dots in a rows x cols arrangement."""
    w = (cols - 1) * grid.spacing
    h = (rows - 1) * grid.spacing
    centre = np.array(centre, dtype=float)
    targets = []
    for i in range(rows * cols):
        rr, cc = divmod(i, cols)
        targets.append(centre + np.array([-w / 2 + cc * grid.spacing,
                                          h / 2 - rr * grid.spacing, 0.0]))
    return targets


def capsule(color: str = DOT_COLOR, w: float = 0.42, h: float = 0.2,
            show_dots: bool = False) -> VGroup:
    """A small capsule holding two counters (Scene 6 keeps 30 of them)."""
    box = RoundedRectangle(corner_radius=h / 2, width=w, height=h,
                           stroke_color=color, stroke_width=1.3,
                           fill_color="#16202B", fill_opacity=0.75)
    d1 = Dot(radius=0.035, color=color).move_to(box.get_center() + LEFT * 0.08)
    d2 = Dot(radius=0.035, color=color).move_to(box.get_center() + RIGHT * 0.08)
    grp = VGroup(box, d1, d2)
    grp.dots = VGroup(d1, d2)
    grp.dots.set_opacity(1.0 if show_dots else 0.0)
    return grp


def bracket_around(parts, color: str = GROUP_COLOR, buff: float = 0.16,
                   radius: float = 0.12) -> RoundedRectangle:
    """The grouping outline -- the object that moves for associativity."""
    box = RoundedRectangle(corner_radius=radius,
                           width=parts.width + 2 * buff,
                           height=parts.height + 2 * buff * 0.7,
                           stroke_color=color, stroke_width=2.6)
    box.move_to(parts.get_center())
    return box


def notebook_stack(color: str = CHALK_AMBER, n: int = 4,
                   w: float = 0.52, h: float = 0.09) -> VGroup:
    """A small stack of notebooks standing in for a quantity."""
    slabs = VGroup(*[
        RoundedRectangle(corner_radius=0.02, width=w, height=h,
                         stroke_color=color, stroke_width=0.8,
                         fill_color=color, fill_opacity=0.28 + 0.12 * i)
        for i in range(n)
    ]).arrange(DOWN, buff=0.035)
    return slabs


def summary_row(n: int, label: str, math_tex: str, color: str) -> VGroup:
    badge = Circle(radius=0.19, stroke_color=color, stroke_width=2,
                   fill_color=color, fill_opacity=0.18)
    num = board_text(str(n), 17, color, "BOLD").move_to(badge.get_center())
    return VGroup(VGroup(badge, num),
                  board_text(label, 16, CHALK_WHITE),
                  MathTex(math_tex, font_size=20)).arrange(RIGHT, buff=0.26)


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "Today we meet two properties of whole numbers.<bookmark mark='b0'/> "
        "Changing the order, and changing the grouping.<bookmark mark='b1'/> "
        "Let's start with a quick maths challenge!<bookmark mark='b2'/>"
    ),
    "scene1": (
        "Here is a quick challenge: one hundred ninety six, plus fifty seven, "
        "plus four.<bookmark mark='b0'/> Do we have to add from left to right?"
        "<bookmark mark='b1'/> Watch carefully: the four moves next to the one "
        "hundred ninety six.<bookmark mark='b2'/> And one hundred ninety six "
        "plus four is two hundred, so we only need two hundred plus fifty "
        "seven. That looks easier!<bookmark mark='b3'/>"
    ),
    "scene2": (
        "Let's begin with two small groups of counters: three and four."
        "<bookmark mark='b0'/> Together they make seven.<bookmark mark='b1'/> "
        "Now the two groups change places; they still make seven.<bookmark "
        "mark='b2'/> Three plus four equals four plus three. This is the "
        "commutative property: changing the order does not change the sum."
        "<bookmark mark='b3'/>"
    ),
    "scene3": (
        "The same idea works for multiplication.<bookmark mark='b0'/> Here are "
        "twelve dots in four rows of three, so four times three is twelve."
        "<bookmark mark='b1'/> Now look at the very same twelve dots in three "
        "rows of four.<bookmark mark='b2'/> Three times four is also twelve, "
        "so four times three equals three times four.<bookmark mark='b3'/>"
    ),
    "scene4": (
        "We can write this rule with letters.<bookmark mark='b0'/> For "
        "addition: a plus b equals b plus a.<bookmark mark='b1'/> And for "
        "multiplication: a times b equals b times a.<bookmark mark='b2'/> "
        "Changing the order never changes the answer.<bookmark mark='b3'/>"
    ),
    "scene5": (
        "Now something different. Three, four and five.<bookmark mark='b0'/> "
        "If we add the first two first: three plus four is seven, and seven "
        "plus five is twelve.<bookmark mark='b1'/> Look — the numbers are "
        "still in the same order; only the grouping has changed.<bookmark "
        "mark='b2'/> Now add the last two first: four plus five is nine, and "
        "three plus nine is twelve again.<bookmark mark='b3'/> So three plus "
        "four, in a group, plus five, equals three plus, four plus five. That "
        "is the associative property.<bookmark mark='b4'/>"
    ),
    "scene6": (
        "Multiplication obeys the same rule.<bookmark mark='b0'/> Here are "
        "five rows of six capsules, so five times six is thirty.<bookmark "
        "mark='b1'/> Each capsule holds two dots, so thirty times two is "
        "sixty.<bookmark mark='b2'/> But we could also start inside each row: "
        "six times two is twelve, and five rows of twelve make sixty."
        "<bookmark mark='b3'/> Different grouping, the same product."
        "<bookmark mark='b4'/>"
    ),
    "scene7": (
        "Let's keep these two ideas apart.<bookmark mark='b0'/> On the left, "
        "the commutative property: the order of the numbers changes."
        "<bookmark mark='b1'/> On the right, the associative property: the "
        "order stays the same and only the grouping changes.<bookmark "
        "mark='b2'/> Order, and grouping. Two different actions.<bookmark "
        "mark='b3'/>"
    ),
    "scene8": (
        "Now back to our challenge: one hundred ninety six, plus fifty seven, "
        "plus four.<bookmark mark='b0'/> First, let's group the last two "
        "terms.<bookmark mark='b1'/> Inside the bracket we can swap them — "
        "that uses the commutative property.<bookmark mark='b2'/> Then we "
        "regroup, and that uses the associative property.<bookmark mark='b3'/> "
        "Now one hundred ninety six plus four is two hundred, and two hundred "
        "plus fifty seven is two hundred and fifty seven.<bookmark mark='b4'/>"
    ),
    "scene9_setup": (
        "Your turn!<bookmark mark='b0'/> Find the sum of two hundred thirty "
        "eight, six hundred ninety five, and one hundred sixty two.<bookmark "
        "mark='b1'/> Which two numbers can make a round hundred?<bookmark "
        "mark='b2'/> Pause the video and try it.<bookmark mark='b3'/>"
    ),
    "scene9_reveal": (
        "Let's check.<bookmark mark='b0'/> Two hundred thirty eight and one "
        "hundred sixty two make four hundred.<bookmark mark='b1'/> So we put "
        "those two together in one group, and add six hundred ninety five."
        "<bookmark mark='b2'/> Four hundred plus six hundred ninety five is "
        "one thousand and ninety five.<bookmark mark='b3'/>"
    ),
    "scene10": (
        "Let's recap.<bookmark mark='b0'/> Commutative means changing the "
        "order: a plus b equals b plus a, and a times b equals b times a."
        "<bookmark mark='b1'/> Associative means changing the grouping: a plus "
        "b, in a group, plus c, equals a plus, b plus c; and a times b, in a "
        "group, times c, equals a times, b times c.<bookmark mark='b2'/> Both "
        "work for addition and multiplication of whole numbers.<bookmark "
        "mark='b3'/> Thank you for watching!<bookmark mark='b4'/>"
    ),
}


class CommutativeAssociativeStory(VoiceoverScene):
    """Story-mode chalkboard lesson: properties of whole numbers (Class 6)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._srt_entries: list[tuple[float, float, str]] = []

    # -- backdrop ----------------------------------------------------------
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
            -config.frame_height / 2 + student.height / 2 - 0.1, 0]))

        teacher = ImageMobject(str(assets_dir / "teacher.png"))
        teacher.set_z_index(-5)
        teacher.height = 3.3
        teacher.move_to(np.array([
            config.frame_width / 2 - teacher.width / 2 + 0.45,
            -config.frame_height / 2 + teacher.height / 2 - 0.1, 0]))

        self.bg = bg
        self.student = student
        self.teacher = teacher
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
            corner_radius=0.04, width=label.width + 0.24,
            height=label.height + 0.16,
            stroke_color=CHALK_AMBER, stroke_width=1.5,
            fill_color="#2A1D10", fill_opacity=0.45)
        label.move_to(frame.get_center())
        badge = VGroup(frame, label).scale(scale)
        yy = BOARD_TOP - 0.32 if y is None else y
        if corner == "left":
            badge.move_to(np.array([BOARD_LEFT + 0.55, yy, 0]))
            badge.shift(RIGHT * (BOARD_LEFT + 0.08 - badge.get_left()[0]))
        else:
            badge.move_to(np.array([BOARD_RIGHT - 0.6, yy, 0]))
            badge.shift(RIGHT * (BOARD_RIGHT - 0.013 - badge.get_right()[0]))
        badge.shift(UP * ((BOARD_TOP - 0.08) - badge.get_top()[1]))
        return badge

    def reset_board(self) -> None:
        self.clear()
        self.add(self.bg, self.student, self.teacher, self.badge, self.badge_l)

    # -- real SRT export ---------------------------------------------------
    def _capture_srt(self, tracker, words_per_line: int = 9) -> None:
        wbs = [wb for wb in tracker.data.get("word_boundaries", [])
               if wb.get("text", "").strip()]
        if not wbs:
            return
        starts = [tracker.start_t + wb["audio_offset"] / AUDIO_OFFSET_RESOLUTION
                  for wb in wbs]
        for i in range(0, len(wbs), words_per_line):
            chunk = wbs[i:i + words_per_line]
            end = starts[i + words_per_line] if i + words_per_line < len(starts) \
                else tracker.end_t
            text = " ".join(wb["text"] for wb in chunk)
            self._srt_entries.append((starts[i], end, text))

    def _write_real_srt(self) -> None:
        out_dir = _HERE / "media" / "videos" / "commutative_associative_story"
        out_dir.mkdir(parents=True, exist_ok=True)

        def fmt(t: float) -> str:
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
        content = "\n".join(lines)
        (out_dir / f"{self.__class__.__name__}.real.srt").write_text(
            content, encoding="utf-8")
        print(f"[real SRT written] {out_dir}")
        (out_dir / "real.srt").write_text(content, encoding="utf-8")
        try:
            if (hasattr(self, "renderer") and hasattr(self.renderer, "file_writer")
                    and self.renderer.file_writer.movie_file_path):
                movie_dir = Path(self.renderer.file_writer.movie_file_path).parent
                (movie_dir / "real.srt").write_text(content, encoding="utf-8")
                (movie_dir / f"{self.__class__.__name__}.real.srt").write_text(
                    content, encoding="utf-8")
        except Exception:
            pass

    def construct(self):
        self.sfx = load_sfx()
        self.set_speech_service(get_speech_service(), create_subcaption=False)
        install_synced_voiceover(self)
        self.add_background()

        self.beat0_title()
        self.beat1_challenge()
        self.beat2_comm_add()
        self.beat3_comm_mul()
        self.beat4_comm_rule()
        self.beat5_assoc_add()
        self.beat6_assoc_mul()
        self.beat7_contrast()
        self.beat8_apply()
        self.beat9_challenge()
        self.beat10_summary()

        self._write_real_srt()

    # ================================================================ beats ==

    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Commutative & Associative Properties", 26,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 1.6, 0]))
            self.play(Write(title), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            sub = board_text("Order and grouping", 21, CHALK_YELLOW, "BOLD"
                             ).move_to(np.array([BOARD_CX, BOARD_CY + 0.9, 0]))
            t1 = num_tile(3, TILE_COLOR, 0.9)
            t2 = num_tile(4, TILE_COLOR, 0.9)
            eq = MathTex("3+4=4+3", font_size=34, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, -0.9, 0]))
            self.play(Write(sub), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.4))
            self.play(FadeIn(VGroup(t1, t2).arrange(RIGHT, buff=0.5).move_to(
                np.array([BOARD_CX, -0.05, 0]))), FadeIn(eq),
                run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(Indicate(eq, color=CHALK_YELLOW, scale_factor=1.05),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: can we calculate smarter? ---------------------------------
    def beat1_challenge(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("A Quick Maths Challenge", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            tiles = [num_tile(196, TILE_COLOR, 1.35), num_tile(57, TILE_COLOR, 1.0),
                     num_tile(4, TILE_COLOR, 0.95)]
            xs = [-2.55, 0.15, 2.45]
            for t, x in zip(tiles, xs):
                t.move_to(np.array([x, 0.75, 0]))
            plus1 = plus_sign(at=np.array([-1.05, 0.75, 0]))
            plus2 = plus_sign(at=np.array([1.45, 0.75, 0]))
            row = VGroup(*tiles, plus1, plus2)

            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))
            self.play(FadeIn(row, shift=DOWN * 0.12), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            ask = board_text("Can we change the order and grouping?", 19,
                             CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX, -0.35, 0]))
            self.play(Indicate(tiles[0], color=CHALK_YELLOW, scale_factor=1.05),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.play(Indicate(tiles[2], color=CHALK_YELLOW, scale_factor=1.05),
                      FadeIn(ask, shift=UP * 0.1),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # the 4 swaps with the 57 -- the commutative move
            self.play(tiles[2].animate.move_to(np.array([xs[1], 0.75, 0])),
                      tiles[1].animate.move_to(np.array([xs[2], 0.75, 0])),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.6))
            moved = MathTex("196+4+57", font_size=34, color=SWAP_COLOR).move_to(
                np.array([BOARD_CX, -1.25, 0]))
            self.play(Write(moved), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            br = bracket_around(VGroup(tiles[0], tiles[2]), SWAP_COLOR)
            easy = MathTex("(196+4)+57", font_size=34, color=GROUP_COLOR
                           ).move_to(np.array([BOARD_CX, -1.9, 0]))
            pair = MathTex("196+4=200", font_size=30, color=RESULT_COLOR
                           ).move_to(np.array([BOARD_CX, -2.5, 0]))
            tag = board_text("That looks easier!", 18, CHALK_YELLOW, "BOLD"
                             ).move_to(np.array([BOARD_CX, 1.6, 0]))
            # three beats inside one window: the bracket, the sum, then the tag
            # on "That looks easier!"
            self.play(Create(br), FadeIn(easy), run_time=rt(
                tracker.time_until_bookmark("b3") * 0.5))
            self.play(FadeIn(pair),
                      Flash(pair, color=RESULT_COLOR, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            self.play(FadeIn(tag), run_time=rt(
                tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: commutative property of addition ---------------------------
    def beat2_comm_add(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("Commutative Property of Addition", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            ga = counter_group(3, DOT_COLOR)
            gb = counter_group(4, CHALK_PINK, cols=2)
            ga.move_to(np.array([-2.0, 0.9, 0]))
            gb.move_to(np.array([2.6, 0.9, 0]))
            plus = plus_sign(at=np.array([0.35, 0.9, 0]))
            numbers = VGroup(
                MathTex("3", font_size=26, color=DOT_COLOR).next_to(ga, DOWN, buff=0.16),
                MathTex("4", font_size=26, color=CHALK_PINK).next_to(gb, DOWN, buff=0.16),
            )

            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))
            self.play(FadeIn(ga), FadeIn(gb), FadeIn(plus), FadeIn(numbers),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            seven = MathTex("3+4=7", font_size=34, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, -0.55, 0]))
            self.play(Write(seven), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(ga.animate.move_to(np.array([2.6, 0.9, 0])),
                      gb.animate.move_to(np.array([-2.0, 0.9, 0])),
                      numbers[0].animate.next_to(np.array([2.6, 0.9, 0]),
                                                 DOWN, buff=0.9),
                      numbers[1].animate.next_to(np.array([-2.0, 0.9, 0]),
                                                 DOWN, buff=0.9),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            seven2 = MathTex("4+3=7", font_size=34, color=CHALK_WHITE).move_to(
                seven)
            rule = MathTex("3+4=4+3", font_size=36, color=SWAP_COLOR).move_to(
                np.array([BOARD_CX, -1.5, 0]))
            rbox = SurroundingRectangle(rule, color=SWAP_COLOR, buff=0.16,
                                        corner_radius=0.1, stroke_width=3)
            lbl = board_text("COMMUTATIVE PROPERTY", 19, SWAP_COLOR, "BOLD"
                             ).move_to(np.array([BOARD_CX, -2.15, 0]))
            note = board_text("Changing the order does not change the sum.", 16,
                              CHALK_WHITE).move_to(
                np.array([BOARD_CX, -2.6, 0]))
            self.play(TransformMatchingTex(seven, seven2),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.4))
            self.play(Write(rule), Create(rbox), FadeIn(lbl), FadeIn(note),
                      Flash(rule, color=SWAP_COLOR, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: commutative property of multiplication ---------------------
    def beat3_comm_mul(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()

            heading = board_text("Commutative Property of Multiplication", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            grid = dot_grid(4, 3, spacing=0.56)
            grid.move_to(np.array([BOARD_CX, 0.35, 0]))
            rows = MathTex(r"4\times3=12", font_size=32, color=DOT_COLOR
                           ).move_to(np.array([BOARD_CX, 1.75, 0]))

            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.play(FadeIn(grid, shift=DOWN * 0.12), Write(rows),
                      *[Indicate(grid[i * 3:(i + 1) * 3], color=CHALK_YELLOW,
                                 scale_factor=1.15) for i in range(4)],
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.add_sound(self.sfx["click"], gain=-15)

            targets = grid_targets(grid, 3, 4, grid.get_center())
            self.play(*[d.animate.move_to(t) for d, t in zip(grid, targets)],
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.6))
            cols = MathTex(r"3\times4=12", font_size=32, color=DOT_COLOR
                           ).move_to(np.array([BOARD_CX, -1.4, 0]))
            self.play(Write(cols), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            rule = MathTex(r"4\times3=3\times4", font_size=34, color=SWAP_COLOR
                           ).move_to(np.array([BOARD_CX, -2.05, 0]))
            rbox = SurroundingRectangle(rule, color=SWAP_COLOR, buff=0.14,
                                        corner_radius=0.1, stroke_width=3)
            note = board_text("The order changed. The product stayed the same.",
                              17, CHALK_WHITE).move_to(
                np.array([BOARD_CX, -2.6, 0]))
            self.play(FadeOut(rows), Write(rule), Create(rbox), FadeIn(note),
                      Flash(rule, color=SWAP_COLOR, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: the commutative rule ---------------------------------------
    def beat4_comm_rule(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()

            heading = board_text("COMMUTATIVE — Change the Order", 22,
                                 SWAP_COLOR, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            ta = num_tile("a", TILE_COLOR, 1.1)
            tb = num_tile("b", TILE_COLOR, 1.1)
            ta.move_to(np.array([-1.5, 1.4, 0]))
            tb.move_to(np.array([2.0, 1.4, 0]))
            plus = plus_sign(at=np.array([0.25, 1.4, 0]), font=34)

            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))
            self.play(FadeIn(ta), FadeIn(tb), FadeIn(plus),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.6))
            add_rule = MathTex("a+b=b+a", font_size=36, color=CHALK_WHITE
                               ).move_to(np.array([BOARD_CX, 0.35, 0]))
            self.play(Write(add_rule), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(ta.animate.move_to(np.array([2.0, 1.4, 0])),
                      tb.animate.move_to(np.array([-1.5, 1.4, 0])),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            # BOTH rules stay on the board: transforming one into the other
            # left the first rule's box around an empty space
            mul_rule = MathTex(r"a\times b=b\times a", font_size=36,
                               color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, -0.6, 0]))
            self.play(Write(mul_rule),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            b1 = SurroundingRectangle(add_rule, color=SWAP_COLOR, buff=0.16,
                                      corner_radius=0.1, stroke_width=3)
            b2 = SurroundingRectangle(mul_rule, color=SWAP_COLOR, buff=0.16,
                                      corner_radius=0.1, stroke_width=3)
            note = board_text("Order does not matter.", 18, CHALK_YELLOW, "BOLD"
                              ).move_to(np.array([BOARD_CX, -1.6, 0]))
            self.play(Create(b1), Create(b2), FadeIn(note),
                      Flash(mul_rule, color=SWAP_COLOR, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: associative property of addition ---------------------------
    def beat5_assoc_add(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            self.reset_board()

            heading = board_text("ASSOCIATIVE — Change the Grouping", 21,
                                 GROUP_COLOR, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            g1 = counter_group(3, DOT_COLOR)
            g2 = counter_group(4, CHALK_PINK, cols=2)
            g3 = counter_group(5, CHALK_CYAN, cols=3)
            g1.move_to(np.array([-2.7, 1.15, 0]))
            g2.move_to(np.array([0.3, 1.15, 0]))
            g3.move_to(np.array([3.2, 1.15, 0]))
            plus1 = plus_sign(at=np.array([-1.25, 1.15, 0]), font=28)
            plus2 = plus_sign(at=np.array([1.75, 1.15, 0]), font=28)

            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(g3), FadeIn(plus1),
                      FadeIn(plus2),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            br1 = bracket_around(VGroup(g1, g2), GROUP_COLOR)
            step1 = MathTex("(3+4)+5=7+5=12", font_size=30, color=GROUP_COLOR
                            ).move_to(np.array([BOARD_CX, -0.35, 0]))
            self.play(Create(br1), Write(step1), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            br2 = bracket_around(VGroup(g2, g3), GROUP_COLOR)
            note = board_text("Same order — only the grouping moves.", 17,
                              CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.15, 0]))
            self.play(Transform(br1, br2), FadeIn(note), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            step2 = MathTex("3+(4+5)=3+9=12", font_size=30, color=GROUP_COLOR
                            ).move_to(np.array([BOARD_CX, -1.75, 0]))
            self.play(Write(step2), run_time=rt(
                tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            rule = MathTex("(3+4)+5=3+(4+5)", font_size=32, color=CHALK_WHITE
                           ).move_to(np.array([BOARD_CX, -2.4, 0]))
            lbl = board_text("ASSOCIATIVE PROPERTY", 17, GROUP_COLOR, "BOLD"
                             ).move_to(np.array([BOARD_CX, 0.25, 0]))
            self.play(FadeOut(step1), FadeOut(step2), FadeOut(note),
                      Write(rule), FadeIn(lbl),
                      Flash(rule, color=GROUP_COLOR, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: associative property of multiplication ---------------------
    def beat6_assoc_mul(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("ASSOCIATIVE — Multiplication", 21,
                                 GROUP_COLOR, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            top = MathTex(r"(5\times6)\times2", font_size=32,
                          color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, 1.9, 0]))

            caps = VGroup()
            for i in range(30):
                c = capsule(DOT_COLOR)
                caps.add(c)
            caps.arrange_in_grid(rows=5, cols=6, buff=0.14)
            caps.move_to(np.array([BOARD_CX, 0.15, 0]))
            rows = [VGroup(*caps[i * 6:(i + 1) * 6]) for i in range(5)]

            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0")))
            # the capsules and their rows appear with "Here are five rows of six
            # capsules", and the product lands on "so five times six is thirty"
            self.play(FadeIn(caps, shift=DOWN * 0.1), Write(top),
                      *[Indicate(r, color=CHALK_YELLOW, scale_factor=1.04)
                        for r in rows],
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.4))
            self.add_sound(self.sfx["pop"], gain=-13)

            step1 = MathTex(r"5\times6=30", font_size=30, color=DOT_COLOR
                            ).move_to(np.array([BOARD_CX, -1.45, 0]))
            self.play(Write(step1), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # one running equation at a time: each step replaces the last
            step2 = MathTex(r"30\times2=60", font_size=30, color=DOT_COLOR
                            ).move_to(step1)
            self.play(*[FadeIn(c.dots) for c in caps], FadeOut(step1),
                      Write(step2),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            br = bracket_around(rows[0], GROUP_COLOR, buff=0.1)
            step3 = MathTex(r"5\times12=60", font_size=30, color=GROUP_COLOR
                            ).move_to(step1)
            self.play(Create(br), FadeOut(step2), Write(step3),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            rule = MathTex(r"(5\times6)\times2=5\times(6\times2)", font_size=28,
                           color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, -2.35, 0]))
            self.play(FadeOut(step3), Write(rule),
                      Flash(br, color=GROUP_COLOR, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: commutative vs associative ---------------------------------
    def beat7_contrast(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("Order vs Grouping", 24, CHALK_AMBER, "BOLD"
                                 ).move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            divider = DashedLine(np.array([BOARD_CX, 2.2, 0]),
                                 np.array([BOARD_CX, -2.3, 0]),
                                 color=CHALK_WHITE, stroke_width=1.4,
                                 stroke_opacity=0.35)
            left_lbl = board_text("COMMUTATIVE", 18, SWAP_COLOR, "BOLD"
                                  ).move_to(np.array([-2.1, 1.9, 0]))
            right_lbl = board_text("ASSOCIATIVE", 18, GROUP_COLOR, "BOLD"
                                   ).move_to(np.array([3.1, 1.9, 0]))
            cap_l = board_text("change the order", 15, CHALK_WHITE).move_to(
                np.array([-2.1, 1.5, 0]))
            cap_r = board_text("change the grouping", 15, CHALK_WHITE).move_to(
                np.array([3.1, 1.5, 0]))

            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))
            self.play(Create(divider), FadeIn(left_lbl), FadeIn(right_lbl),
                      FadeIn(cap_l), FadeIn(cap_r),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            # left column: two tiles swap
            la = num_tile(3, SWAP_COLOR, 0.8, 26)
            lb = num_tile(4, SWAP_COLOR, 0.8, 26)
            la.move_to(np.array([-3.0, 0.5, 0]))
            lb.move_to(np.array([-1.2, 0.5, 0]))
            lplus = plus_sign(at=np.array([-2.1, 0.5, 0]), font=26)
            l_eq = MathTex("3+4", font_size=28, color=SWAP_COLOR).move_to(
                np.array([-2.1, -0.5, 0]))
            self.play(FadeIn(la), FadeIn(lb), FadeIn(lplus), Write(l_eq),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.play(la.animate.move_to(np.array([-1.2, 0.5, 0])),
                      lb.animate.move_to(np.array([-3.0, 0.5, 0])),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.play(TransformMatchingTex(l_eq, MathTex(
                "4+3", font_size=28, color=SWAP_COLOR).move_to(
                    np.array([-2.1, -0.5, 0]))),
                run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            # right column: three tiles, only the bracket moves
            ra = num_tile(3, GROUP_COLOR, 0.62, 22)
            rb = num_tile(4, GROUP_COLOR, 0.62, 22)
            rc = num_tile(5, GROUP_COLOR, 0.62, 22)
            ra.move_to(np.array([1.6, 0.5, 0]))
            rb.move_to(np.array([2.6, 0.5, 0]))
            rc.move_to(np.array([3.6, 0.5, 0]))
            r_eq = MathTex("(3+4)+5", font_size=24, color=GROUP_COLOR).move_to(
                np.array([2.6, -0.5, 0]))
            rbr1 = bracket_around(VGroup(ra, rb), GROUP_COLOR, buff=0.1)
            rbr2 = bracket_around(VGroup(rb, rc), GROUP_COLOR, buff=0.1)
            self.play(FadeIn(ra), FadeIn(rb), FadeIn(rc), Write(r_eq),
                      Create(rbr1),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            self.play(Transform(rbr1, rbr2),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            self.play(TransformMatchingTex(r_eq, MathTex(
                "3+(4+5)", font_size=24, color=GROUP_COLOR).move_to(
                    np.array([2.6, -0.5, 0]))),
                run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            table = board_text("Commutative → order          "
                               "Associative → grouping", 17, CHALK_YELLOW,
                               "BOLD").move_to(np.array([BOARD_CX, -1.6, 0]))
            verdict = board_text("Order is not grouping.", 19, CHALK_CYAN,
                                 "BOLD").move_to(np.array([BOARD_CX, -2.2, 0]))
            self.play(FadeIn(table, shift=UP * 0.1), FadeIn(verdict),
                      Flash(verdict, color=CHALK_CYAN, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: applying both properties -----------------------------------
    def beat8_apply(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("Rearrange. Regroup. Simplify.", 23,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            stacks = VGroup()
            for value, x in (("196", -3.1), ("57", -1.4), ("4", 0.3)):
                st = notebook_stack(CHALK_AMBER if value == "196" else
                                    (CHALK_PINK if value == "57" else CHALK_CYAN))
                lab = MathTex(value, font_size=20, color=CHALK_WHITE)
                grp = VGroup(st, lab).arrange(DOWN, buff=0.1).move_to(
                    np.array([x, 2.1, 0]))
                stacks.add(grp)
            title = MathTex("196+57+4", font_size=36, color=CHALK_WHITE
                            ).move_to(np.array([BOARD_CX, 1.1, 0]))

            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))
            self.play(FadeIn(stacks, shift=DOWN * 0.1), Write(title),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            step1 = MathTex("196+(57+4)", font_size=34, color=GROUP_COLOR
                            ).move_to(np.array([BOARD_CX, 1.1, 0]))
            self.play(TransformMatchingTex(title, step1),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            step2 = MathTex("196+(4+57)", font_size=34, color=SWAP_COLOR
                            ).move_to(np.array([BOARD_CX, 1.1, 0]))
            tag1 = board_text("Commutative Property", 16, SWAP_COLOR, "BOLD"
                              ).move_to(np.array([3.9, 1.1, 0]))
            self.play(TransformMatchingTex(step1, step2), FadeIn(tag1),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            step3 = MathTex("(196+4)+57", font_size=34, color=GROUP_COLOR
                            ).move_to(np.array([BOARD_CX, 1.1, 0]))
            tag2 = board_text("Associative Property", 16, GROUP_COLOR, "BOLD"
                              ).move_to(np.array([3.9, 0.6, 0]))
            self.play(TransformMatchingTex(step2, step3), FadeOut(tag1),
                      FadeIn(tag2),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            step4 = MathTex("200+57", font_size=36, color=RESULT_COLOR).move_to(
                np.array([BOARD_CX, -0.1, 0]))
            ans = MathTex("257", font_size=44, color=RESULT_COLOR).move_to(
                np.array([BOARD_CX, -1.1, 0]))
            abox = SurroundingRectangle(ans, color=RESULT_COLOR, buff=0.2,
                                        corner_radius=0.1, stroke_width=3)
            self.play(TransformMatchingTex(step3, step4), FadeOut(tag2),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.5))
            self.play(Write(ans), Create(abox),
                      Flash(ans, color=RESULT_COLOR, flash_radius=0.8),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 9: student challenge -----------------------------------------
    def beat9_challenge(self) -> None:
        with self.voiceover(text=NARRATION["scene9_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", 30, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y - 0.05, 0]))
            tiles = [num_tile(238, TILE_COLOR, 1.25), num_tile(695, TILE_COLOR, 1.25),
                     num_tile(162, TILE_COLOR, 1.25)]
            xs = [-2.7, 0.1, 2.9]
            for t, x in zip(tiles, xs):
                t.move_to(np.array([x, 1.15, 0]))
            plus1 = plus_sign(at=np.array([-1.3, 1.15, 0]))
            plus2 = plus_sign(at=np.array([1.5, 1.15, 0]))
            ask = board_text("Which two numbers can make a round hundred?", 18,
                             CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, 0.1, 0]))
            hint = board_text("Pause and try it.", 18, CHALK_WHITE, "BOLD"
                              ).move_to(np.array([BOARD_CX, -1.9, 0]))

            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.play(FadeIn(VGroup(*tiles, plus1, plus2), shift=DOWN * 0.12),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(FadeIn(ask, shift=RIGHT * 0.12), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(hint, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b3")))
            # absorb the tail of this piece's audio so the countdown that
            # follows starts exactly when "Pause and try it." has finished
            self.play(Indicate(hint, color=CHALK_YELLOW, scale_factor=1.03),
                      run_time=rt(tracker.get_remaining_duration()))

            self.challenge = {"tiles": tiles, "plus1": plus1, "plus2": plus2,
                              "ask": ask, "hint": hint, "xs": xs}
            self._capture_srt(tracker)

        play_challenge_countdown(self, seconds=4, sfx=self.sfx)

        with self.voiceover(text=NARRATION["scene9_reveal"]) as tracker:
            ch = self.challenge
            tiles, xs = ch["tiles"], ch["xs"]
            highlight = SurroundingRectangle(VGroup(tiles[0], tiles[2]),
                                             color=CHALK_YELLOW, buff=0.14,
                                             corner_radius=0.1, stroke_width=2.6)
            self.play(FadeOut(ch["hint"]), Create(highlight), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.5))
            self.play(Transform(highlight, SurroundingRectangle(
                          VGroup(tiles[0], tiles[2]), color=RESULT_COLOR,
                          buff=0.14, corner_radius=0.1, stroke_width=2.6)),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # 162 moves next to 238 -- commutative
            self.play(tiles[2].animate.move_to(np.array([xs[1], 1.15, 0])),
                      tiles[1].animate.move_to(np.array([xs[2], 1.15, 0])),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.play(FadeOut(highlight), FadeOut(ch["ask"]),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            br = bracket_around(VGroup(tiles[0], tiles[2]), GROUP_COLOR)
            step = MathTex("(238+162)+695", font_size=32, color=GROUP_COLOR
                           ).move_to(np.array([BOARD_CX, -0.35, 0]))
            self.play(Create(br), Write(step), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            val = MathTex("400+695", font_size=34, color=RESULT_COLOR).move_to(
                np.array([BOARD_CX, -1.1, 0]))
            ans = MathTex("1095", font_size=44, color=RESULT_COLOR).move_to(
                np.array([BOARD_CX, -2.0, 0]))
            abox = SurroundingRectangle(ans, color=RESULT_COLOR, buff=0.2,
                                        corner_radius=0.1, stroke_width=3)
            self.play(TransformMatchingTex(step, val), run_time=rt(
                tracker.time_until_bookmark("b3") * 0.5))
            self.play(Write(ans), Create(abox),
                      Flash(ans, color=RESULT_COLOR, flash_radius=0.8),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 10: summary + thanks -----------------------------------------
    def beat10_summary(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("Commutative & Associative", 26, CHALK_AMBER,
                                 "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y - 0.05, 0]))
            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0")))

            def card(title, caption, color, x, lines_tex):
                box = RoundedRectangle(corner_radius=0.1, width=4.2, height=2.1,
                                       stroke_color=color, stroke_width=2.2,
                                       fill_color="#16202B", fill_opacity=0.8)
                box.move_to(np.array([x, 0.45, 0]))
                head = board_text(title, 17, color, "BOLD").move_to(
                    box.get_top() + DOWN * 0.26)
                cap = board_text(caption, 14, CHALK_WHITE).move_to(
                    box.get_top() + DOWN * 0.58)
                eqs = VGroup(*[MathTex(t, font_size=24, color=color)
                               for t in lines_tex]).arrange(DOWN, buff=0.16)
                eqs.move_to(box.get_center() + DOWN * 0.32)
                return VGroup(box, head, cap, eqs)

            left = card("COMMUTATIVE", "change the order", SWAP_COLOR, -1.7,
                        ["a+b=b+a", r"a\times b=b\times a"])
            right = card("ASSOCIATIVE", "change the grouping", GROUP_COLOR, 3.2,
                         ["(a+b)+c=a+(b+c)", r"(a\times b)\times c=a\times(b\times c)"])
            self.play(FadeIn(left, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(FadeIn(right, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["pop"], gain=-13)

            take = board_text("Both work for addition and multiplication of "
                              "whole numbers.", 18, CHALK_YELLOW, "BOLD"
                              ).move_to(np.array([BOARD_CX, -1.5, 0]))
            take2 = board_text("Commutative → order      Associative → grouping",
                               15, CHALK_CYAN).move_to(
                np.array([BOARD_CX, -2.05, 0]))
            self.play(FadeIn(take), FadeIn(take2),
                      Flash(take, color=CHALK_YELLOW, flash_radius=0.9),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.6))
            self.add_sound(self.sfx["success"], gain=-11)

            row = summary_row(1, "Addition and multiplication follow both "
                                 "properties:", r"a+b=b+a", CHALK_WHITE)
            row.move_to(np.array([BOARD_CX, -2.5, 0]))
            self.play(FadeIn(row), run_time=rt(
                tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            summary = VGroup(heading, left, right, take, take2, row)
            self.play(FadeOut(summary), run_time=rt(
                tracker.time_until_bookmark("b3")))

            thanks = board_text("Thank You for Watching!", 40, CHALK_WHITE,
                                "BOLD")
            thanks2 = board_text("See you in the next lesson :)", 25, CHALK_CYAN)
            thanks_group = VGroup(thanks, thanks2).arrange(DOWN, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY, 0]))
            self.play(Write(thanks), run_time=rt(
                tracker.time_until_bookmark("b4") * 0.5))
            self.add_sound(self.sfx["ding"], gain=-11)
            self.play(FadeIn(thanks2, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b4")))
            self.play(Circumscribe(thanks_group, color=CHALK_AMBER,
                                   stroke_width=3, time_width=0.5), run_time=0.3)
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(END_HOLD)


if __name__ == "__main__":
    pass

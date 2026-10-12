"""
Geometric Dot Patterns (and the mental-maths shortcuts they reveal)
Story-mode chalkboard lesson (Telangana Class 6 Maths, Chapter 2: Whole
Numbers, Patterns in Whole Numbers, pages 25-28).

Two halves, one idea:
  Part A -- the SAME dots rearrange themselves into a line, a rectangle, a
            square and a triangle (no dot is ever added or removed while a
            shape is only being rearranged);
  Part B -- the shapes give way to number tiles and the same "find the
            pattern" thinking turns 9 into 10-1 and 99 into 100-1, so
            296+99 and 65x99 can be done in the head.

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
  1. Same Dots, Different Patterns -- six dots: line, rectangle, triangle.
  2. Numbers as Lines -- 2, 3, 4, 5, ...
  3. Rectangular Patterns -- 2 x 3 = 6.
  4. Square Numbers -- 2x2, 3x3, 4x4 -> 4, 9, 16.
  5. Triangular Numbers -- 3, 6, 10, ...
  6. Nearby Round Numbers -- 296 +/- 9 and 296 +/- 99.
  7. Multiplication -- 65 x 99 = 6435.
  8. Real World -- 46 x 25 = 1150 stickers.
  9. Student Challenge -- the next triangle and 65 x 999.
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
    Rectangle, RoundedRectangle, Polygon, Arrow, DoubleArrow, Text, Brace,
    Write, FadeIn, FadeOut, Create, Transform, ReplacementTransform,
    TransformMatchingTex, TransformFromCopy, GrowArrow, Indicate, Flash,
    Circumscribe, CurvedArrow, SurroundingRectangle, MoveAlongPath,
    ArcBetweenPoints, config,
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

DOT_COLOR = CHALK_AMBER       # the dots themselves
SHAPE_COLOR = CHALK_GREEN     # outlines / braces around a shape
TILE_COLOR = CHALK_CYAN       # number tiles
DIST_COLOR = CHALK_PINK       # the two distribution arrows
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


# ---------------------------------------------------------- the dot kit -----
def dot_line(n: int, spacing: float = 0.62, r: float = 0.1,
             color: str = DOT_COLOR) -> VGroup:
    grp = VGroup(*[Dot(radius=r, color=color) for _ in range(n)])
    grp.arrange(RIGHT, buff=spacing)
    grp.spacing = spacing
    return grp


def dot_grid(rows: int, cols: int, *, spacing: float = 0.52, r: float = 0.09,
             color: str = DOT_COLOR) -> VGroup:
    grp = VGroup(*[Dot(radius=r, color=color) for _ in range(rows * cols)])
    grp.arrange_in_grid(rows=rows, cols=cols, buff=spacing)
    grp.rows, grp.cols, grp.spacing = rows, cols, spacing
    return grp


def grid_targets(grid: VGroup, rows: int, cols: int, centre) -> list[np.ndarray]:
    w = (cols - 1) * grid.spacing
    h = (rows - 1) * grid.spacing
    centre = np.array(centre, dtype=float)
    out = []
    for i in range(rows * cols):
        rr, cc = divmod(i, cols)
        out.append(centre + np.array([-w / 2 + cc * grid.spacing,
                                      h / 2 - rr * grid.spacing, 0.0]))
    return out


def triangle_rows(max_rows: int, *, spacing: float = 0.62, r: float = 0.1,
                  color: str = DOT_COLOR, top_y: float = 0.9,
                  cx: float = BOARD_CX) -> list[VGroup]:
    """Rows of 1, 2, 3, ... dots stacked into a triangle (top row first)."""
    rows = []
    for i in range(max_rows):
        row = VGroup(*[Dot(radius=r, color=color) for _ in range(i + 1)])
        row.arrange(RIGHT, buff=spacing)
        row.move_to(np.array([cx, top_y - i * spacing, 0.0]))
        rows.append(row)
    return rows


def row_label(row: VGroup, text: str, color: str = SHAPE_COLOR,
              size: int = 22) -> MathTex:
    return MathTex(text, font_size=size, color=color).next_to(row, RIGHT,
                                                              buff=0.28)


def brace_label(target, text: str, direction, color: str = SHAPE_COLOR,
                size: int = 17, buff: float = 0.22) -> VGroup:
    brace = Brace(target, direction=direction, color=color, buff=buff)
    label = board_text(text, size, color, "BOLD")
    label.next_to(brace, direction, buff=0.12)
    return VGroup(brace, label)


def packet_icon(color: str = CHALK_CYAN) -> VGroup:
    """A simplified sticker packet: sticker circle on top, count underneath.

    The box is tall enough that the "25" clears the circle -- at the old height
    the count sat across the circle's lower edge."""
    box = RoundedRectangle(corner_radius=0.06, width=0.85, height=1.0,
                           stroke_color=color, stroke_width=2,
                           fill_color="#16202B", fill_opacity=0.85)
    sticker = Circle(radius=0.2, stroke_color=color, stroke_width=1.6,
                     fill_color=color, fill_opacity=0.25).move_to(
        box.get_center() + UP * 0.17)
    star = MathTex(r"\star", font_size=20, color=color).move_to(
        sticker.get_center())
    tag = board_text("25", 16, color, "BOLD").move_to(
        box.get_center() + DOWN * 0.28)
    grp = VGroup(box, sticker, star, tag)
    grp.box = box
    return grp


def dist_arrow(mult, term, color: str = DIST_COLOR,
               bow: float = 45 * DEGREES) -> CurvedArrow:
    return CurvedArrow(mult.get_top() + UP * 0.06, term.get_top() + UP * 0.06,
                       angle=-bow, color=color, stroke_width=2.6,
                       tip_length=0.15)


def summary_row(n: int, label: str, math_tex: str, color: str) -> VGroup:
    badge = Circle(radius=0.16, stroke_color=color, stroke_width=2,
                   fill_color=color, fill_opacity=0.18)
    num = board_text(str(n), 15, color, "BOLD").move_to(badge.get_center())
    return VGroup(VGroup(badge, num),
                  board_text(label, 14, CHALK_WHITE),
                  MathTex(math_tex, font_size=18)).arrange(RIGHT, buff=0.24)


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "Today we look at patterns made from dots.<bookmark mark='b0'/> We "
        "will build lines, rectangles, squares and triangles, and then use "
        "those patterns to calculate faster.<bookmark mark='b1'/> Let's start "
        "with a dot puzzle!<bookmark mark='b2'/>"
    ),
    "scene1": (
        "Here are six dots, scattered around.<bookmark mark='b0'/> Can six "
        "dots make different shapes, without adding or removing a single dot?"
        "<bookmark mark='b1'/> Watch: they line up in a row; then they become "
        "two rows of three; and then a triangle.<bookmark mark='b2'/> Six "
        "equals two times three, and six is also one plus two plus three."
        "<bookmark mark='b3'/>"
    ),
    "scene2": (
        "Let's begin with the simplest pattern: a line.<bookmark mark='b0'/> "
        "Two dots; one more makes three; one more makes four; and one more "
        "makes five.<bookmark mark='b1'/> Each step adds exactly one more dot, "
        "so we get two, three, four, five, and on and on.<bookmark mark='b2'/>"
    ),
    "scene3": (
        "Now take six dots and arrange them as a rectangle: two rows, with "
        "three dots in each row.<bookmark mark='b0'/> The first row has three "
        "dots, and the second row has three dots, so three plus three is six."
        "<bookmark mark='b1'/> Two rows of three is the same as two times "
        "three. A rectangle reveals multiplication!<bookmark mark='b2'/>"
    ),
    "scene4": (
        "What if the rows and the columns are equal?<bookmark mark='b0'/> Two "
        "rows of two give four dots.<bookmark mark='b1'/> Three rows of three "
        "give nine dots.<bookmark mark='b2'/> And four rows of four give "
        "sixteen dots. These are the square numbers: four, nine, sixteen, and "
        "so on.<bookmark mark='b3'/>"
    ),
    "scene5": (
        "Now let's build triangles.<bookmark mark='b0'/> A triangle starts "
        "with one dot, then a row of two: one plus two is three.<bookmark "
        "mark='b1'/> Add a row of three, and we have one plus two plus three, "
        "which is six.<bookmark mark='b2'/> What happens if we add one more "
        "row? Four dots in the bottom row give one plus two plus three plus "
        "four, which is ten.<bookmark mark='b3'/> So the triangular numbers "
        "are three, six, ten, and so on.<bookmark mark='b4'/>"
    ),
    "scene6": (
        "Patterns can make calculations easier too.<bookmark mark='b0'/> Look "
        "at two hundred ninety six plus nine. Nine is almost ten, because nine "
        "is ten minus one.<bookmark mark='b1'/> So we add ten, and then take "
        "one away.<bookmark mark='b2'/> For subtraction, two hundred ninety "
        "six minus nine: take away ten, and add one back.<bookmark mark='b3'/> "
        "Now with ninety nine, which is one hundred minus one. Two hundred "
        "ninety six plus ninety nine: add one hundred, then take one away."
        "<bookmark mark='b4'/> And two hundred ninety six minus ninety nine: "
        "subtract one hundred, then add one back.<bookmark mark='b5'/>"
    ),
    "scene7": (
        "The same idea works for multiplication.<bookmark mark='b0'/> Sixty "
        "five times ninety nine. Ninety nine is one hundred minus one."
        "<bookmark mark='b1'/> So we write sixty five times, one hundred minus "
        "one, in a bracket.<bookmark mark='b2'/> Now multiply sixty five by "
        "both terms: sixty five times one hundred is six thousand five "
        "hundred, and sixty five times one is sixty five.<bookmark mark='b3'/> "
        "Six thousand five hundred minus sixty five is six thousand four "
        "hundred and thirty five.<bookmark mark='b4'/>"
    ),
    "scene8": (
        "Here is a practical example.<bookmark mark='b0'/> A packet holds "
        "twenty five stickers, and we have forty six packets.<bookmark "
        "mark='b1'/> Twenty five is twenty plus five.<bookmark mark='b2'/> So "
        "we calculate forty six times, twenty plus five, in a bracket. That is "
        "forty six times twenty, which is nine hundred and twenty, plus forty "
        "six times five, which is two hundred and thirty.<bookmark mark='b3'/> "
        "Nine hundred and twenty plus two hundred and thirty is one thousand, "
        "one hundred and fifty stickers.<bookmark mark='b4'/>"
    ),
    "scene9_setup": (
        "Your turn!<bookmark mark='b0'/> Two questions. First, here is a "
        "triangle of six dots: how many dots do we need for the next "
        "triangle?<bookmark mark='b1'/> Second: sixty five times nine hundred "
        "and ninety nine.<bookmark mark='b2'/> Pause the video and try both."
        "<bookmark mark='b3'/>"
    ),
    "scene9_reveal": (
        "Let's check.<bookmark mark='b0'/> The next triangle needs a bottom "
        "row of four dots, so one plus two plus three plus four is ten."
        "<bookmark mark='b1'/> And for the multiplication, nine hundred and "
        "ninety nine is one thousand minus one.<bookmark mark='b2'/> Sixty "
        "five times one thousand is sixty five thousand, and we subtract sixty "
        "five: sixty four thousand, nine hundred and thirty five.<bookmark "
        "mark='b3'/>"
    ),
    "scene10": (
        "Let's recap.<bookmark mark='b0'/> Dots can make a line, a rectangle, "
        "a square or a triangle.<bookmark mark='b1'/> The square numbers are "
        "four, nine and sixteen, and the triangular numbers are three, six and "
        "ten.<bookmark mark='b2'/> For quick calculations, remember that nine "
        "is ten minus one, and ninety nine is one hundred minus one.<bookmark "
        "mark='b3'/> See the pattern, and simplify the calculation.<bookmark "
        "mark='b4'/> Thank you for watching!<bookmark mark='b5'/> See you in "
        "the next lesson!<bookmark mark='b6'/>"
    ),
}


class DotPatternsStory(VoiceoverScene):
    """Story-mode chalkboard lesson: geometric dot patterns + shortcuts."""

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
        out_dir = _HERE / "media" / "videos" / "dot_patterns_story"
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
        self.beat1_shapes()
        self.beat2_line()
        self.beat3_rectangle()
        self.beat4_square()
        self.beat5_triangle()
        self.beat6_round()
        self.beat7_multiply()
        self.beat8_real()
        self.beat9_challenge()
        self.beat10_summary()

        self._write_real_srt()

    # ================================================================ beats ==

    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Geometric Dot Patterns", 36, CHALK_WHITE,
                               "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 1.6, 0]))
            self.play(Write(title), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            sub = board_text("See the pattern — simplify the calculation", 19,
                             CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 0.9, 0]))
            grid = dot_grid(2, 3, spacing=0.5, r=0.1)
            grid.move_to(np.array([BOARD_CX, -0.7, 0]))
            eq = MathTex(r"2\times3=6", font_size=32, color=SHAPE_COLOR
                         ).move_to(np.array([3.4, -0.7, 0]))
            self.play(Write(sub), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.4))
            self.play(FadeIn(grid, shift=DOWN * 0.1), Write(eq),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(Indicate(eq, color=CHALK_YELLOW, scale_factor=1.05),
                      run_time=rt(tracker.get_remaining_duration()))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: same dots, different patterns ------------------------------
    def beat1_shapes(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("A Dot Puzzle", 24, CHALK_AMBER, "BOLD"
                                 ).move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            scattered = [np.array([-3.0, 0.6, 0]), np.array([-1.2, 1.3, 0]),
                         np.array([0.9, 0.9, 0]), np.array([2.6, 1.4, 0]),
                         np.array([1.7, -0.5, 0]), np.array([-2.2, -0.7, 0])]
            dots = VGroup(*[Dot(radius=0.11, color=DOT_COLOR).move_to(p)
                            for p in scattered])
            count = MathTex("6", font_size=40, color=CHALK_YELLOW).move_to(
                np.array([4.15, 0.45, 0]))

            self.play(Write(heading), *[FadeIn(d, scale=0.6) for d in dots],
                      Write(count),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            ask = board_text("Can six dots make different shapes?", 19,
                             CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX, -1.5, 0]))
            self.play(FadeIn(ask, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # the line is centred on the board, matching the rectangle and the
            # triangle (it used to sit half a unit to the left of them)
            line_pos = [np.array([BOARD_CX - 1.8 + i * 0.72, 0.3, 0])
                        for i in range(6)]
            self.play(*[d.animate.move_to(p) for d, p in zip(dots, line_pos)],
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.3))
            rect = dot_grid(2, 3, spacing=0.52, r=0.11)
            rect.move_to(np.array([BOARD_CX, 0.3, 0]))
            self.play(*[d.animate.move_to(p) for d, p in zip(dots, rect)],
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.35))
            tri = VGroup(*triangle_rows(3, spacing=0.6, r=0.11, top_y=0.75))
            tri_targets = [d.get_center() for row in tri for d in row]
            self.play(*[d.animate.move_to(p)
                        for d, p in zip(dots, tri_targets)],
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            eq1 = MathTex("6=2\\times3", font_size=30, color=SHAPE_COLOR
                          ).move_to(np.array([-2.3, -1.5, 0]))
            eq2 = MathTex("6=1+2+3", font_size=30, color=SHAPE_COLOR).move_to(
                np.array([1.6, -1.5, 0]))
            tag = board_text("Same number. Different patterns.", 18,
                             CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -2.25, 0]))
            # the question goes out on its own before the equations arrive: a
            # single cross-fading play left the two texts on top of each other
            self.play(FadeOut(ask), run_time=rt(
                tracker.get_remaining_duration() * 0.25))
            self.play(Write(eq1), Write(eq2), FadeIn(tag),
                      Flash(eq2, color=SHAPE_COLOR, flash_radius=0.6),
                      run_time=rt(tracker.get_remaining_duration()))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: numbers as lines ------------------------------------------
    def beat2_line(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("Line Pattern", 25, CHALK_AMBER, "BOLD"
                                 ).move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))

            line = dot_line(2, spacing=0.62, r=0.12).move_to(
                np.array([BOARD_CX, 0.7, 0]))
            count = MathTex("2", font_size=38, color=CHALK_YELLOW).next_to(
                line, UP, buff=0.45)
            self.play(FadeIn(line, shift=RIGHT * 0.2), Write(count),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            # the line grows one dot at a time and stays centred
            grown = [line]
            for i in range(3):
                nxt = dot_line(len(line) + 1, spacing=0.62, r=0.12).move_to(
                    np.array([BOARD_CX, 0.7, 0]))
                new_dot = nxt[-1]
                nxt.remove(new_dot)
                frac = (i + 1) / 3
                self.play(Transform(line, nxt), FadeIn(new_dot),
                          Transform(count, MathTex(str(len(line) + 1),
                                                   font_size=38,
                                                   color=CHALK_YELLOW
                                                   ).next_to(nxt, UP, buff=0.45)),
                          run_time=rt(tracker.time_until_bookmark("b1") * frac))
                line = VGroup(*nxt, new_dot)
                grown.append(line)
                self.add_sound(self.sfx["click"], gain=-15)

            seq = MathTex("2,\\,3,\\,4,\\,5,\\,\\ldots", font_size=34,
                          color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, -0.9, 0]))
            note = board_text("Each step adds one more dot.", 19, CHALK_CYAN,
                              "BOLD").move_to(np.array([BOARD_CX, -1.7, 0]))
            self.play(Write(seq), FadeIn(note, shift=UP * 0.1),
                      run_time=rt(tracker.get_remaining_duration()))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: rectangular patterns ---------------------------------------
    def beat3_rectangle(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()

            heading = board_text("Rows × Columns = Total Dots", 23, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            grid = dot_grid(2, 3, spacing=0.62, r=0.12).move_to(
                np.array([BOARD_CX, 0.75, 0]))
            rows = [VGroup(*grid[i * 3:(i + 1) * 3]) for i in range(2)]

            self.play(Write(heading), FadeIn(grid, shift=DOWN * 0.1),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            r1 = brace_label(rows[0], "3", UP, SHAPE_COLOR, 20, 0.1)
            r2 = brace_label(rows[1], "3", DOWN, SHAPE_COLOR, 20, 0.1)
            self.play(Indicate(rows[0], color=CHALK_YELLOW, scale_factor=1.15),
                      Create(r1), run_time=rt(
                          tracker.time_until_bookmark("b1") * 0.5))
            self.play(Indicate(rows[1], color=CHALK_YELLOW, scale_factor=1.15),
                      Create(r2), run_time=rt(
                          tracker.time_until_bookmark("b1") * 0.5))
            self.add_sound(self.sfx["click"], gain=-15)

            frame = SurroundingRectangle(grid, color=SHAPE_COLOR, buff=0.3,
                                         corner_radius=0.1, stroke_width=2.6)
            add = MathTex("3+3=6", font_size=32, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, -1.5, 0]))
            self.play(Create(frame), Write(add), run_time=rt(
                tracker.time_until_bookmark("b1")))
            rule = MathTex(r"2\times3=6", font_size=38, color=SHAPE_COLOR
                           ).move_to(np.array([BOARD_CX, -1.5, 0]))
            rbox = SurroundingRectangle(rule, color=SHAPE_COLOR, buff=0.16,
                                        corner_radius=0.1, stroke_width=3)
            tag = board_text("A rectangle reveals multiplication!", 18,
                             CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -2.3, 0]))
            self.play(TransformMatchingTex(add, rule), Create(rbox), FadeIn(tag),
                      Flash(rule, color=SHAPE_COLOR, flash_radius=0.7),
                      run_time=rt(tracker.get_remaining_duration()))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: square numbers --------------------------------------------
    def beat4_square(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()

            heading = board_text("SQUARE NUMBERS", 24, SHAPE_COLOR, "BOLD"
                                 ).move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            grid = dot_grid(2, 2, spacing=0.55, r=0.11).move_to(
                np.array([BOARD_CX, 0.7, 0]))
            eq = MathTex(r"2\times2=4", font_size=32, color=CHALK_WHITE
                         ).move_to(np.array([BOARD_CX, -1.2, 0]))
            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            # b0 -> b1: "Two rows of two give four dots."
            self.play(FadeIn(grid, shift=DOWN * 0.1), Write(eq), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)

            # grow 2x2 -> 3x3 -> 4x4, keeping the old dots
            current = list(grid)
            for k, (rows, cols) in enumerate(((3, 3), (4, 4)), start=1):
                target = dot_grid(rows, cols, spacing=0.55, r=0.11).move_to(
                    np.array([BOARD_CX, 0.7, 0]))
                targets = grid_targets(grid, rows, cols, target.get_center())
                new_dots = VGroup(*[Dot(radius=0.11, color=DOT_COLOR)
                                    for _ in range(rows * cols - len(current))])
                new_targets = targets[len(current):]
                for d, p in zip(new_dots, new_targets):
                    d.move_to(p + UP * 0.5)
                # k=1 lands on "Three rows of three give nine dots." (b1 -> b2),
                # k=2 on the first half of "And four rows of four ..." (b2 -> b3).
                mark = "b2" if k == 1 else "b3"
                # k=2 shares its window with "These are the square numbers:",
                # so the 4x4 growth finishes on "four give sixteen dots."
                frac = 1.0 if k == 1 else 0.34
                label = (r"3\times3=9" if k == 1 else r"4\times4=16")
                new_eq = MathTex(label, font_size=32, color=CHALK_WHITE
                                 ).move_to(eq)
                self.play(*[d.animate.move_to(p)
                            for d, p in zip(current, targets[:len(current)])],
                          *[FadeIn(d, shift=DOWN * 0.3) for d in new_dots],
                          TransformMatchingTex(eq, new_eq),
                          run_time=rt(tracker.time_until_bookmark(mark) * frac))
                current = list(current) + list(new_dots)
                eq = new_eq
                self.add_sound(self.sfx["click"], gain=-15)

            # second half of b2 -> b3: "These are the square numbers: four,
            # nine, sixteen, and so on."
            seq = MathTex("4,\\ 9,\\ 16,\\ \\ldots", font_size=34,
                          color=SHAPE_COLOR).move_to(
                np.array([BOARD_CX, -1.9, 0]))
            note = board_text("Equal rows and columns.", 17, CHALK_WHITE
                              ).move_to(np.array([BOARD_CX, -2.5, 0]))
            self.play(Write(seq), FadeIn(note),
                      run_time=rt(tracker.get_remaining_duration()))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: triangular numbers ----------------------------------------
    def beat5_triangle(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            self.reset_board()

            heading = board_text("Triangle = Growing Rows", 23, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            rows = triangle_rows(4, spacing=0.62, r=0.11, top_y=1.05, cx=-2.5)
            row_labels = [row_label(rows[i], str(i + 1), SHAPE_COLOR, 20)
                          for i in range(4)]
            sums = {1: "1+2=3", 2: "1+2+3=6", 3: "1+2+3+4=10"}
            eq = MathTex(sums[1], font_size=28, color=CHALK_WHITE).move_to(
                np.array([2.4, 0.75, 0]))

            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            # b0 -> b1: "A triangle starts with one dot, then a row of two:
            # one plus two is three."
            self.play(FadeIn(rows[0], shift=DOWN * 0.1),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.35))
            self.play(FadeIn(rows[1], shift=DOWN * 0.1), FadeIn(row_labels[0]),
                      FadeIn(row_labels[1]), Write(eq),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)

            # b1 -> b2: "Add a row of three, and we have one plus two plus
            # three, which is six."
            eq2 = MathTex(sums[2], font_size=28, color=CHALK_WHITE).move_to(eq)
            self.play(FadeIn(rows[2], shift=DOWN * 0.1), FadeIn(row_labels[2]),
                      TransformMatchingTex(eq, eq2),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            # b2 -> b3: "What happens if we add one more row? Four dots in the
            # bottom row give one plus two plus three plus four, which is ten."
            self.play(*[Indicate(rows[i], color=CHALK_YELLOW, scale_factor=1.1)
                        for i in range(3)],
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.15))
            ask = board_text("What happens if we add one more row?", 17,
                             CHALK_CYAN, "BOLD").move_to(
                np.array([2.4, 0.15, 0]))
            eq3 = MathTex(sums[3], font_size=28, color=CHALK_WHITE).move_to(eq2)
            self.play(FadeIn(ask, shift=UP * 0.1),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.2))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.play(FadeIn(rows[3], shift=DOWN * 0.1), FadeIn(row_labels[3]),
                      FadeOut(ask), TransformMatchingTex(eq2, eq3),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            # b3 -> b4: "So the triangular numbers are three, six, ten, and so
            # on."
            seq = MathTex("3,\\ 6,\\ 10,\\ \\ldots", font_size=34,
                          color=SHAPE_COLOR).move_to(
                np.array([2.4, -1.5, 0]))
            sbox = SurroundingRectangle(seq, color=SHAPE_COLOR, buff=0.16,
                                        corner_radius=0.1, stroke_width=3)
            note = board_text("Each new row has one more dot.", 17, CHALK_WHITE
                              ).move_to(np.array([BOARD_CX, -2.35, 0]))
            self.play(Write(seq), Create(sbox), FadeIn(note),
                      Flash(seq, color=SHAPE_COLOR, flash_radius=0.7),
                      run_time=rt(tracker.get_remaining_duration()))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: nearby round numbers ---------------------------------------
    def beat6_round(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("Use Round Numbers!", 25, CHALK_AMBER, "BOLD"
                                 ).move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            main = MathTex("296+9", font_size=44, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, 0.9, 0]))
            self.play(Write(heading), Write(main), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.5))
            nine = board_text("9 is almost 10", 17, CHALK_CYAN, "BOLD").move_to(
                np.array([3.6, 1.5, 0]))
            self.play(Indicate(main, color=CHALK_YELLOW, scale_factor=1.04),
                      FadeIn(nine), run_time=rt(
                          tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            step = MathTex("9=10-1", font_size=34, color=SHAPE_COLOR).move_to(
                np.array([BOARD_CX, 0.0, 0]))
            self.play(Write(step), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            # b1 -> b2: "So we add ten, and then take one away."
            full = MathTex("296+10-1", font_size=40, color=CHALK_WHITE).move_to(
                main)
            self.play(TransformMatchingTex(main, full), FadeOut(step),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.4))

            ans1 = MathTex("306-1=305", font_size=36, color=RESULT_COLOR
                           ).move_to(np.array([BOARD_CX, -0.9, 0]))
            b1 = SurroundingRectangle(ans1, color=RESULT_COLOR, buff=0.16,
                                      corner_radius=0.1, stroke_width=3)
            self.play(FadeOut(full), Write(ans1), Create(b1),
                      Flash(ans1, color=RESULT_COLOR, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # b2 -> b3: "For subtraction, ... take away ten, and add one back."
            ans2 = MathTex("296-9=296-10+1=287", font_size=30,
                           color=RESULT_COLOR).move_to(
                np.array([BOARD_CX, -1.7, 0]))
            self.play(FadeOut(b1), Write(ans2), run_time=rt(
                tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # b3 -> b4: "Now with ninety nine, which is one hundred minus one."
            ans3 = MathTex("296+99=296+100-1=395", font_size=30,
                           color=RESULT_COLOR).move_to(
                np.array([BOARD_CX, -2.25, 0]))
            self.play(FadeOut(ans1), FadeOut(ans2), Write(ans3), run_time=rt(
                tracker.time_until_bookmark("b4")))

            # b4 -> b5: "And two hundred ninety six minus ninety nine ...",
            # then the recap of both rules.
            ans4 = MathTex("296-99=296-100+1=197", font_size=30,
                           color=RESULT_COLOR).move_to(ans2)
            self.play(TransformMatchingTex(ans3, ans4), run_time=rt(
                tracker.time_until_bookmark("b5") * 0.6))
            self.add_sound(self.sfx["success"], gain=-11)

            rule = board_text("9 = 10 − 1       99 = 100 − 1", 22,
                              CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.7, 0]))
            self.play(FadeOut(ans4), FadeIn(rule, shift=UP * 0.1), run_time=rt(
                tracker.get_remaining_duration()))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: multiplication shortcut ------------------------------------
    def beat7_multiply(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("Multiply by 100, Subtract Once", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            main = MathTex(r"65\times99", font_size=44, color=CHALK_WHITE
                           ).move_to(np.array([BOARD_CX, 0.85, 0]))
            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            # b0 -> b1: "Sixty five times ninety nine. Ninety nine is one
            # hundred minus one."
            self.play(Write(main), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.45))
            note = MathTex("99=100-1", font_size=32, color=SHAPE_COLOR).move_to(
                np.array([3.5, 1.4, 0]))
            self.play(Indicate(main, color=CHALK_YELLOW, scale_factor=1.04),
                      Write(note), run_time=rt(
                          tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            bracketed = MathTex("65", "(", "100", "-", "1", ")", font_size=42
                                ).move_to(main)
            self.play(TransformMatchingTex(main, bracketed), FadeOut(note),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            a1 = dist_arrow(bracketed[0], bracketed[2], DIST_COLOR)
            a2 = dist_arrow(bracketed[0], bracketed[4], DIST_COLOR)
            self.play(Create(a1), Create(a2), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            step = MathTex(r"(65\times100)-(65\times1)", font_size=30,
                           color=DIST_COLOR).move_to(
                np.array([BOARD_CX, -0.75, 0]))
            self.play(FadeOut(a1), FadeOut(a2), Write(step), run_time=rt(
                tracker.time_until_bookmark("b3") * 0.5))
            val = MathTex("6500-65", font_size=38, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, -0.75, 0]))
            self.play(TransformMatchingTex(step, val), run_time=rt(
                tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            ans = MathTex("6435", font_size=46, color=RESULT_COLOR).move_to(
                np.array([BOARD_CX, -1.85, 0]))
            abox = SurroundingRectangle(ans, color=RESULT_COLOR, buff=0.18,
                                        corner_radius=0.1, stroke_width=3)
            tag = board_text("Almost 100? Multiply by 100, then subtract once.",
                             16, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -2.5, 0]))
            self.play(FadeOut(bracketed), FadeOut(val), Write(ans), Create(abox),
                      FadeIn(tag), Flash(ans, color=RESULT_COLOR,
                                         flash_radius=0.8),
                      run_time=rt(tracker.get_remaining_duration()))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: real-world application -------------------------------------
    def beat8_real(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("Break Numbers Into Easy Parts", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            packets = VGroup(*[packet_icon(CHALK_CYAN) for _ in range(3)]
                             ).arrange(RIGHT, buff=0.2).move_to(
                np.array([-3.0, 0.9, 0]))
            lab1 = board_text("25 stickers per packet", 15, CHALK_CYAN, "BOLD"
                              ).next_to(packets, DOWN, buff=0.2)
            lab2 = board_text("46 packets", 15, CHALK_WHITE, "BOLD").next_to(
                lab1, DOWN, buff=0.12)

            self.play(Write(heading), FadeIn(packets, shift=UP * 0.1),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            # b0 -> b1: "A packet holds twenty five stickers, and we have
            # forty six packets."
            self.play(FadeIn(lab1), FadeIn(lab2), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.5))

            e1 = MathTex(r"46\times25", font_size=36, color=CHALK_WHITE
                         ).move_to(np.array([2.0, 0.9, 0]))
            self.play(Write(e1), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            split = MathTex("25=20+5", font_size=32, color=SHAPE_COLOR).move_to(
                np.array([2.0, 0.2, 0]))
            self.play(Write(split), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            e2 = MathTex("46(20+5)", font_size=34, color=CHALK_WHITE).move_to(
                e1)
            self.play(TransformMatchingTex(e1, e2), FadeOut(split),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.4))
            step = MathTex(r"(46\times20)+(46\times5)", font_size=28,
                           color=DIST_COLOR).move_to(
                np.array([2.0, -0.6, 0]))
            self.play(Write(step), run_time=rt(
                tracker.time_until_bookmark("b3") * 0.3))
            val = MathTex("920+230", font_size=32, color=CHALK_WHITE).move_to(
                np.array([2.0, -1.35, 0]))
            self.play(TransformMatchingTex(step, val), run_time=rt(
                tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            ans = board_text("1150 stickers", 30, RESULT_COLOR, "BOLD").move_to(
                np.array([2.0, -2.2, 0]))
            abox = SurroundingRectangle(ans, color=RESULT_COLOR, buff=0.16,
                                        corner_radius=0.1, stroke_width=3)
            self.play(FadeOut(e2), FadeOut(val), Write(ans), Create(abox),
                      Flash(ans, color=RESULT_COLOR, flash_radius=0.8),
                      run_time=rt(tracker.get_remaining_duration()))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 9: student challenge -----------------------------------------
    def beat9_challenge(self) -> None:
        with self.voiceover(text=NARRATION["scene9_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", 30, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y - 0.05, 0]))
            rows = triangle_rows(3, spacing=0.5, r=0.09, top_y=1.0, cx=-2.4)
            tri = VGroup(*rows)
            ask_t = board_text("How many dots for the next triangle?", 15,
                               CHALK_CYAN, "BOLD").next_to(tri, DOWN, buff=0.3)
            q_b = MathTex(r"65\times999=?", font_size=38, color=CHALK_WHITE
                          ).move_to(np.array([2.5, 0.6, 0]))
            pause = board_text("Pause and try both.", 19, CHALK_YELLOW, "BOLD"
                               ).move_to(np.array([BOARD_CX, -2.2, 0]))

            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.play(FadeIn(tri, shift=DOWN * 0.1), FadeIn(ask_t),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(Write(q_b),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(pause, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b3")))
            self.play(Indicate(pause, color=CHALK_YELLOW, scale_factor=1.03),
                      run_time=rt(tracker.get_remaining_duration()))

            self.challenge = {"rows": rows, "tri": tri, "ask_t": ask_t,
                              "q_b": q_b, "pause": pause}
            self._capture_srt(tracker)

        play_challenge_countdown(self, seconds=4, sfx=self.sfx)

        with self.voiceover(text=NARRATION["scene9_reveal"]) as tracker:
            ch = self.challenge
            rows, tri = ch["rows"], ch["tri"]
            self.play(FadeOut(ch["pause"]), run_time=rt(
                tracker.time_until_bookmark("b0")))

            # b0 -> b1: "The next triangle needs a bottom row of four dots, so
            # one plus two plus three plus four is ten."
            row4 = triangle_rows(4, spacing=0.5, r=0.09, top_y=1.0, cx=-2.4)[3]
            sum_eq = MathTex("1+2+3+4=10", font_size=28, color=RESULT_COLOR
                             ).move_to(np.array([-2.4, -1.9, 0]))
            sbox = SurroundingRectangle(sum_eq, color=RESULT_COLOR, buff=0.14,
                                        corner_radius=0.1, stroke_width=3)
            self.play(FadeIn(row4, shift=DOWN * 0.2), FadeOut(ch["ask_t"]),
                      Write(sum_eq), Create(sbox),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)

            # b1 -> b2: "And for the multiplication, nine hundred and ninety
            # nine is one thousand minus one."
            note = MathTex("999=1000-1", font_size=30, color=SHAPE_COLOR
                           ).move_to(np.array([2.5, -0.2, 0]))
            self.play(FadeOut(ch["q_b"]), Write(note), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # b2 -> b3: "Sixty five times one thousand is sixty five thousand,
            # and we subtract sixty five: sixty four thousand, nine hundred and
            # thirty five."
            e2 = MathTex("65(1000-1)", font_size=32, color=CHALK_WHITE).move_to(
                np.array([2.5, -0.95, 0]))
            e3 = MathTex("65000-65", font_size=32, color=CHALK_WHITE).move_to(
                np.array([2.5, -1.6, 0]))
            ans = MathTex("64935", font_size=40, color=RESULT_COLOR).move_to(
                np.array([2.5, -2.25, 0]))
            abox = SurroundingRectangle(ans, color=RESULT_COLOR, buff=0.16,
                                        corner_radius=0.1, stroke_width=3)
            self.play(TransformMatchingTex(note, e2), run_time=rt(
                tracker.time_until_bookmark("b3") * 0.35))
            self.play(TransformMatchingTex(e2, e3), run_time=rt(
                tracker.time_until_bookmark("b3") * 0.35))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(Write(ans), Create(abox),
                      Flash(ans, color=RESULT_COLOR, flash_radius=0.8),
                      run_time=rt(tracker.get_remaining_duration()))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 10: summary + thanks -----------------------------------------
    def beat10_summary(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("GEOMETRIC DOT PATTERNS", 24, CHALK_AMBER,
                                 "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y - 0.05, 0]))
            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # b0 -> b1: "Dots can make a line, a rectangle, a square or a
            # triangle."
            shapes = VGroup()
            specs = [
                ("Line", dot_line(4, spacing=0.3, r=0.07)),
                ("Rectangle", dot_grid(2, 3, spacing=0.3, r=0.07)),
                ("Square", dot_grid(3, 3, spacing=0.3, r=0.07)),
                ("Triangle", VGroup(*triangle_rows(3, spacing=0.32, r=0.07,
                                                   top_y=0.32, cx=0.0))),
            ]
            # four evenly spaced columns centred on the board, every shape on a
            # common baseline and every label on a common line, so the row reads
            # as one row instead of four staggered ones
            xs = [BOARD_CX - 2.85, BOARD_CX - 0.95, BOARD_CX + 0.95,
                  BOARD_CX + 2.85]
            for (name, shape), x in zip(specs, xs):
                shape.move_to(np.array([x, 1.45, 0]))
                lab = board_text(name, 14, CHALK_WHITE, "BOLD")
                shapes.add(VGroup(shape, lab))
            base_y = min(grp[0].get_bottom()[1] for grp in shapes)
            lab_y = base_y - 0.34
            for grp in shapes:
                grp[0].align_to(np.array([0.0, base_y, 0.0]), DOWN)
                grp[1].move_to(np.array([grp[0].get_center()[0], lab_y, 0]))
            self.play(FadeIn(shapes, shift=DOWN * 0.1), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)

            # b1 -> b2: "The square numbers are four, nine and sixteen, and
            # the triangular numbers are three, six and ten."
            seq1 = MathTex("4,\\ 9,\\ 16,\\ \\ldots", font_size=30,
                           color=SHAPE_COLOR).move_to(
                np.array([-1.9, 0.35, 0]))
            seq2 = MathTex("3,\\ 6,\\ 10,\\ \\ldots", font_size=30,
                           color=SHAPE_COLOR).move_to(
                np.array([2.6, 0.35, 0]))
            self.play(Write(seq1), Write(seq2), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # b2 -> b3: "For quick calculations, remember that nine is ten
            # minus one, and ninety nine is one hundred minus one."
            shortcuts = VGroup(
                MathTex("9=10-1", font_size=30, color=CHALK_WHITE),
                MathTex("99=100-1", font_size=30, color=CHALK_WHITE),
            ).arrange(RIGHT, buff=1.4).move_to(np.array([BOARD_CX, -0.5, 0]))
            self.play(Write(shortcuts), run_time=rt(
                tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # b3 -> b4: the takeaway line and the recap rows land exactly on
            # "See the pattern, and simplify the calculation."
            take = board_text("See the Pattern. Simplify the Calculation.", 20,
                              CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.25, 0]))
            rows_sum = VGroup(
                summary_row(1, "Line · rectangle · square · triangle:",
                            r"2\times3=6", CHALK_WHITE),
                summary_row(2, "Nearby round numbers:",
                            r"296+99=395", SHAPE_COLOR),
                summary_row(3, "Multiplication pattern:",
                            r"65\times99=6435", DIST_COLOR),
            ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX, -2.2, 0]))
            rows_sum.shift(RIGHT * (BOARD_CX - rows_sum.get_center()[0]))
            self.play(FadeIn(take), FadeIn(rows_sum),
                      Flash(take, color=CHALK_YELLOW, flash_radius=0.9),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.6))
            self.add_sound(self.sfx["success"], gain=-11)
            self.play(Indicate(rows_sum, color=CHALK_YELLOW, scale_factor=1.02),
                      run_time=rt(tracker.time_until_bookmark("b4")))

            summary = VGroup(heading, shapes, seq1, seq2, shortcuts, take,
                             rows_sum)
            thanks = board_text("Thank You for Watching!", 40, CHALK_WHITE,
                                "BOLD")
            thanks2 = board_text("See you in the next lesson :)", 25, CHALK_CYAN)
            thanks_group = VGroup(thanks, thanks2).arrange(DOWN, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY, 0]))
            # b4 -> b5: "Thank you for watching!" — clear the recap, write the
            # card; b5 -> b6: "See you in the next lesson!" — the second line
            self.play(FadeOut(summary), run_time=rt(
                tracker.time_until_bookmark("b5") * 0.45))
            self.play(Write(thanks), run_time=rt(
                tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["ding"], gain=-11)
            self.play(FadeIn(thanks2, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b6")))
            self.play(Circumscribe(thanks_group, color=CHALK_AMBER,
                                   stroke_width=3, time_width=0.5), run_time=0.25)
            self.add_sound(self.sfx["success"], gain=-11)
            self.play(Indicate(thanks, color=CHALK_WHITE, scale_factor=1.01),
                      run_time=rt(tracker.get_remaining_duration()))
            self._capture_srt(tracker)

        self.wait(END_HOLD)


if __name__ == "__main__":
    pass

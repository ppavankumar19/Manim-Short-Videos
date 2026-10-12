"""
Distributive Property of Whole Numbers (with the identity elements 0 and 1)
Story-mode chalkboard lesson (Telangana Class 6 Maths, Chapter 2: Whole
Numbers, Section 2.4 — properties of whole numbers, page 24 + Exercise 2.2).

The defining visual is a 5 x 4 rectangle of twenty dots that SPLITS into a
2 x 4 and a 3 x 4 rectangle: not one dot is added or removed.  Only after that
picture does the symbolic rule `a(b+c) = ab + ac` appear (two separate arrows,
one reaching each term).  The identity elements use a separate, quieter
animation in which the SAME seven counters stay on the board and simply do not
change.

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
  1. Can We Split a Multiplication? -- the 5x4 grid divides into 2+3 rows.
  2. The Total Does Not Change -- 8 + 12 = 20.
  3. Multiply Both Parts -- (2+3)x4 = 2x4 + 3x4.
  4. The Distributive Rule -- a(b+c) = ab + ac.
  5. Worked Example -- 12 x 75 = 900.
  6. Zero: the Additive Identity -- 7 + 0 = 7.
  7. One: the Multiplicative Identity -- 1 x 7 = 7 x 1 = 7.
  8. The Milk Vendor -- (56+44) x 30 = Rs 3000.
  9. Student Challenge -- 5(7+8) = 75 and the identity check.
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

DOT_COLOR = CHALK_AMBER       # the counters
SPLIT_COLOR = CHALK_GREEN     # the split of the rectangle
DIST_COLOR = CHALK_PINK       # the distribution arrows
TILE_COLOR = CHALK_CYAN       # number tiles
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


# ------------------------------------------------------- story furniture ----
def num_tile(value, color: str = TILE_COLOR, size: float = 1.0,
             font: int = 32) -> VGroup:
    box = RoundedRectangle(corner_radius=0.08, width=size, height=size * 0.82,
                           stroke_color=color, stroke_width=2.2,
                           fill_color="#16202B", fill_opacity=0.85)
    lab = MathTex(str(value), font_size=font, color=color).move_to(box.get_center())
    grp = VGroup(box, lab)
    grp.box, grp.lab = box, lab
    return grp


def counter_group(n: int, color: str = DOT_COLOR, cols: int | None = None,
                  r: float = 0.1, buff: float = 0.17,
                  pad: float = 0.16) -> VGroup:
    """A little collection of counters inside its own outline (n may be 0)."""
    cols = cols or min(max(n, 1), 3)
    dots = VGroup(*[Dot(radius=r, color=color) for _ in range(n)])
    if n:
        dots.arrange_in_grid(rows=max(1, -(-n // cols)), cols=cols, buff=buff)
    w = dots.width if n else 0.5
    h = dots.height if n else 0.32
    outline = RoundedRectangle(corner_radius=0.1, width=w + 2 * pad,
                               height=h + 2 * pad,
                               stroke_color=color, stroke_width=1.8,
                               stroke_opacity=0.75,
                               fill_color=color, fill_opacity=0.10)
    if n:
        outline.move_to(dots.get_center())
    grp = VGroup(outline, dots)
    grp.outline, grp.dots = outline, dots
    return grp


def dot_grid(rows: int, cols: int, *, spacing: float = 0.5, r: float = 0.085,
             color: str = DOT_COLOR) -> VGroup:
    grp = VGroup(*[Dot(radius=r, color=color) for _ in range(rows * cols)])
    grp.arrange_in_grid(rows=rows, cols=cols, buff=spacing)
    grp.rows, grp.cols, grp.spacing = rows, cols, spacing
    return grp


def row_of(grid: VGroup, index: int) -> VGroup:
    """The dots of one row of a grid built row-major."""
    n = grid.cols
    return VGroup(*grid[index * n:(index + 1) * n])


def dist_arrow(mult, term, color: str = DIST_COLOR,
               lift: float = 0.55, bow: float = 45 * DEGREES) -> CurvedArrow:
    """One multiplication arrow from the multiplier to a term inside the
    bracket -- the property is taught as TWO arrows, never one."""
    start = mult.get_top() + UP * 0.06
    end = term.get_top() + UP * 0.06
    arc = CurvedArrow(start, end, angle=-bow, color=color, stroke_width=2.6,
                      tip_length=0.15)
    return arc


def milk_can(label: str, color: str = CHALK_CYAN) -> VGroup:
    """A simple milk container with its quantity attached."""
    body = RoundedRectangle(corner_radius=0.1, width=0.85, height=1.15,
                            stroke_color=color, stroke_width=2,
                            fill_color="#16202B", fill_opacity=0.8)
    neck = Rectangle(width=0.3, height=0.14, stroke_color=color,
                     stroke_width=1.6, fill_color="#16202B",
                     fill_opacity=0.8).next_to(body, UP, buff=0)
    cap = RoundedRectangle(corner_radius=0.03, width=0.38, height=0.12,
                           stroke_color=color, stroke_width=1.4,
                           fill_color=color, fill_opacity=0.3).next_to(
        neck, UP, buff=0)
    lab = MathTex(label, font_size=24, color=CHALK_WHITE).next_to(body, DOWN,
                                                                  buff=0.16)
    grp = VGroup(cap, neck, body, lab)
    grp.body, grp.label = body, lab
    return grp


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
        "Today we meet the distributive property of whole numbers.<bookmark "
        "mark='b0'/> We will also meet two very special numbers: zero and one."
        "<bookmark mark='b1'/> Let's begin with a multiplication puzzle!"
        "<bookmark mark='b2'/>"
    ),
    "scene1": (
        "Here are twenty dots, arranged in five rows of four.<bookmark "
        "mark='b0'/> So five times four is twenty.<bookmark mark='b1'/> Now "
        "watch carefully: we draw a line after the second row.<bookmark "
        "mark='b2'/> The rows move apart, but not a single dot has been added "
        "or taken away. Can two smaller groups give the same total?<bookmark "
        "mark='b3'/>"
    ),
    "scene2": (
        "Let's count each group.<bookmark mark='b0'/> The first group has two "
        "rows of four, so two times four is eight.<bookmark mark='b1'/> The "
        "second group has three rows of four, so three times four is twelve."
        "<bookmark mark='b2'/> Eight plus twelve is twenty, exactly the same "
        "total.<bookmark mark='b3'/> So five times four equals two times four, "
        "plus three times four. Two plus three, in a bracket, times four, "
        "gives the same split.<bookmark mark='b4'/>"
    ),
    "scene3": (
        "Now let's see why that split works.<bookmark mark='b0'/> The "
        "multiplier is four, and it stands outside the bracket.<bookmark "
        "mark='b1'/> So four multiplies the first term, two; that gives two "
        "times four.<bookmark mark='b2'/> And four also multiplies the second "
        "term, three; that gives three times four.<bookmark mark='b3'/> "
        "Multiply every term inside the bracket, and eight plus twelve is "
        "twenty.<bookmark mark='b4'/>"
    ),
    "scene4": (
        "We can write this rule with letters.<bookmark mark='b0'/> The "
        "multiplier a reaches the first term, b, so we get a times b."
        "<bookmark mark='b1'/> And it reaches the second term, c, as well."
        "<bookmark mark='b2'/> So a times, b plus c, equals a b plus a c. That "
        "is the distributive property: multiply each term inside the bracket."
        "<bookmark mark='b3'/>"
    ),
    "scene5": (
        "Let's use it to make a big multiplication easier: twelve times "
        "seventy five.<bookmark mark='b0'/> Now seventy five is seventy plus "
        "five.<bookmark mark='b1'/> So twelve times seventy five is twelve "
        "times, seventy plus five, in a bracket.<bookmark mark='b2'/> Now "
        "distribute: twelve times seventy is eight hundred and forty, and "
        "twelve times five is sixty.<bookmark mark='b3'/> Eight hundred and "
        "forty plus sixty is nine hundred. A big multiplication became two "
        "easy ones!<bookmark mark='b4'/>"
    ),
    "scene6": (
        "Now let's meet two special numbers, starting with zero.<bookmark "
        "mark='b0'/> Here are seven counters, and next to them an empty "
        "container, which holds zero counters.<bookmark mark='b1'/> When we "
        "add the empty container to the seven counters, the group does not "
        "change at all.<bookmark mark='b2'/> Seven plus zero is seven. Zero is "
        "the additive identity, because adding zero leaves the number "
        "unchanged.<bookmark mark='b3'/>"
    ),
    "scene7": (
        "Now, the number one.<bookmark mark='b0'/> One group of seven counters "
        "is just seven.<bookmark mark='b1'/> And those same seven counters can "
        "be shown as seven groups of one, which is still seven.<bookmark "
        "mark='b2'/> So one times seven equals seven times one equals seven. "
        "One is the multiplicative identity.<bookmark mark='b3'/> But be "
        "careful: multiplying by zero gives zero, not the original number."
        "<bookmark mark='b4'/>"
    ),
    "scene8": (
        "Here is a daily-life example.<bookmark mark='b0'/> A milk vendor "
        "sells fifty six litres in the morning and forty four litres in the "
        "evening, at thirty rupees a litre.<bookmark mark='b1'/> His earnings "
        "are fifty six times thirty, plus forty four times thirty.<bookmark "
        "mark='b2'/> Both parts share the multiplier thirty, so we take it "
        "out: fifty six plus forty four, in a bracket, times thirty.<bookmark "
        "mark='b3'/> That is one hundred times thirty, which is three thousand "
        "rupees.<bookmark mark='b4'/>"
    ),
    "scene9_setup": (
        "Your turn!<bookmark mark='b0'/> Use the distributive property for "
        "five times, seven plus eight, in a bracket.<bookmark mark='b1'/> "
        "Multiply five by each term inside the bracket.<bookmark mark='b2'/> "
        "Pause the video and try it.<bookmark mark='b3'/>"
    ),
    "scene9_reveal": (
        "Let's check.<bookmark mark='b0'/> Five times seven is thirty five, "
        "and five times eight is forty.<bookmark mark='b1'/> Thirty five plus "
        "forty is seventy five.<bookmark mark='b2'/> And a quick identity "
        "check: nine plus zero is nine, and nine times one is also nine."
        "<bookmark mark='b3'/>"
    ),
    "scene10": (
        "Let's recap.<bookmark mark='b0'/> The distributive property: a times, "
        "b plus c, equals a b plus a c.<bookmark mark='b1'/> The additive "
        "identity is zero: a plus zero equals a.<bookmark mark='b2'/> The "
        "multiplicative identity is one: a times one equals a.<bookmark "
        "mark='b3'/> Distribute to simplify, and remember that the identities "
        "keep a number unchanged.<bookmark mark='b4'/> Thank you for watching!"
        "<bookmark mark='b5'/>"
    ),
}


class DistributivePropertyStory(VoiceoverScene):
    """Story-mode chalkboard lesson: distributive property + identities."""

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
        out_dir = _HERE / "media" / "videos" / "distributive_property_story"
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
        self.beat1_split()
        self.beat2_total()
        self.beat3_both()
        self.beat4_rule()
        self.beat5_example()
        self.beat6_zero()
        self.beat7_one()
        self.beat8_milk()
        self.beat9_challenge()
        self.beat10_summary()

        self._write_real_srt()

    # ================================================================ beats ==

    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Distributive Property", 38, CHALK_WHITE,
                               "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 1.6, 0]))
            self.play(Write(title), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            sub = board_text("and the identity elements 0 and 1", 20,
                             CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 0.9, 0]))
            grid = dot_grid(5, 4, spacing=0.34, r=0.06)
            grid.move_to(np.array([-1.9, -0.55, 0]))
            eq = MathTex(r"5\times4=20", font_size=34, color=CHALK_WHITE
                         ).move_to(np.array([2.3, -0.55, 0]))
            self.play(Write(sub), run_time=rt(
                tracker.time_until_bookmark("b1")))
            # the puzzle itself is the next window: "Let's begin with a
            # multiplication puzzle!"
            self.play(FadeIn(grid, shift=DOWN * 0.1), Write(eq),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.6))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(Indicate(eq, color=CHALK_YELLOW, scale_factor=1.05),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: can we split a multiplication? -----------------------------
    def beat1_split(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("A Multiplication Puzzle", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            grid = dot_grid(5, 4, spacing=0.52, r=0.09)
            grid.move_to(np.array([BOARD_CX - 0.9, 0.25, 0]))
            total = MathTex(r"5\times4=20", font_size=34, color=CHALK_WHITE
                            ).move_to(np.array([3.4, 0.25, 0]))

            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))
            self.play(FadeIn(grid, shift=DOWN * 0.12), Write(total),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(*[Indicate(row_of(grid, i), color=CHALK_YELLOW,
                                 scale_factor=1.12) for i in range(5)],
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            divider = DashedLine(grid.get_left() + LEFT * 0.25,
                                 grid.get_right() + RIGHT * 0.25,
                                 color=SPLIT_COLOR, stroke_width=2.6)
            divider.move_to(row_of(grid, 1).get_center() + DOWN * 0.26)
            self.play(Create(divider), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            bottom = VGroup(*[d for i in range(2, 5) for d in row_of(grid, i)])
            ask = board_text("Can two smaller groups give the same total?", 18,
                             CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX, -2.35, 0]))
            self.play(bottom.animate.shift(DOWN * 0.42), FadeIn(ask, shift=UP * 0.1),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: the total does not change ----------------------------------
    def beat2_total(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("Split the Group. Keep the Total.", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            top = dot_grid(2, 4, spacing=0.52, r=0.09)
            top.move_to(np.array([BOARD_CX - 0.9, 1.25, 0]))
            bottom = dot_grid(3, 4, spacing=0.52, r=0.09)
            bottom.move_to(np.array([BOARD_CX - 0.9, -0.35, 0]))

            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.35))
            self.play(FadeIn(top, shift=DOWN * 0.1), FadeIn(bottom, shift=UP * 0.1),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            eq8 = MathTex(r"2\times4=8", font_size=30, color=DOT_COLOR).move_to(
                np.array([3.3, 1.25, 0]))
            self.play(Indicate(top, color=CHALK_YELLOW, scale_factor=1.1),
                      Write(eq8), run_time=rt(
                          tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            eq12 = MathTex(r"3\times4=12", font_size=30, color=DOT_COLOR
                           ).move_to(np.array([3.3, -0.35, 0]))
            self.play(Indicate(bottom, color=CHALK_YELLOW, scale_factor=1.1),
                      Write(eq12), run_time=rt(
                          tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            sum_eq = MathTex("8+12=20", font_size=32, color=RESULT_COLOR
                             ).move_to(np.array([3.3, -1.4, 0]))
            self.play(Write(sum_eq), Flash(sum_eq, color=RESULT_COLOR,
                                           flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)

            rule = MathTex(r"5\times4=(2\times4)+(3\times4)", font_size=30,
                           color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, -2.15, 0]))
            boxed = MathTex(r"(2+3)\times4=2\times4+3\times4", font_size=30,
                            color=SPLIT_COLOR).move_to(
                np.array([BOARD_CX, -2.62, 0]))
            self.play(TransformMatchingTex(eq8, rule), FadeOut(eq12),
                      FadeOut(sum_eq),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.5))
            self.play(Write(boxed), Flash(boxed, color=SPLIT_COLOR,
                                          flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: multiply both parts ----------------------------------------
    def beat3_both(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()

            heading = board_text("Multiply Both Terms", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            expr = MathTex("(", "2", "+", "3", ")", r"\times", "4",
                           font_size=48).move_to(np.array([BOARD_CX, -0.2, 0]))
            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))
            self.play(Write(expr), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            br = SurroundingRectangle(expr[6], color=CHALK_YELLOW, buff=0.12,
                                      corner_radius=0.1, stroke_width=2.4)
            self.play(Create(br), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            a1 = dist_arrow(expr[6], expr[1], DIST_COLOR)
            p1 = MathTex(r"2\times4", font_size=30, color=DIST_COLOR).move_to(
                np.array([-1.6, -1.6, 0]))
            self.play(Create(a1), FadeIn(p1), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            a2 = dist_arrow(expr[6], expr[3], DIST_COLOR)
            p2 = MathTex(r"3\times4", font_size=30, color=DIST_COLOR).move_to(
                np.array([1.9, -1.6, 0]))
            self.play(Create(a2), FadeIn(p2), run_time=rt(
                tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            full = MathTex(r"(2+3)\times4=(2\times4)+(3\times4)", font_size=30,
                           color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, -2.35, 0]))
            done = MathTex("8+12=20", font_size=30, color=RESULT_COLOR
                           ).move_to(np.array([BOARD_CX, 1.9, 0]))
            self.play(FadeOut(p1), FadeOut(p2), FadeOut(a1), FadeOut(a2),
                      FadeOut(br), Write(full), Write(done),
                      Flash(done, color=RESULT_COLOR, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: the distributive rule --------------------------------------
    def beat4_rule(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()

            heading = board_text("DISTRIBUTIVE PROPERTY", 24, DIST_COLOR,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            expr = MathTex("a", "(", "b", "+", "c", ")", font_size=52).move_to(
                np.array([BOARD_CX, 0.7, 0]))
            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))
            self.play(Write(expr), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.play(Indicate(expr[0], color=DIST_COLOR, scale_factor=1.2),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            a1 = dist_arrow(expr[0], expr[2], DIST_COLOR)
            p1 = MathTex("ab", font_size=34, color=DIST_COLOR).move_to(
                np.array([-1.4, -0.9, 0]))
            self.play(Create(a1), FadeIn(p1), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            a2 = dist_arrow(expr[0], expr[4], DIST_COLOR)
            p2 = MathTex("ac", font_size=34, color=DIST_COLOR).move_to(
                np.array([2.0, -0.9, 0]))
            self.play(Create(a2), FadeIn(p2), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            rule = MathTex("a(b+c)=ab+ac", font_size=40, color=CHALK_WHITE
                           ).move_to(np.array([BOARD_CX, -1.85, 0]))
            rbox = SurroundingRectangle(rule, color=DIST_COLOR, buff=0.16,
                                        corner_radius=0.1, stroke_width=3)
            other = MathTex("(b+c)a=ba+ca", font_size=30, color=CHALK_CYAN
                            ).move_to(np.array([BOARD_CX, -2.55, 0]))
            self.play(FadeOut(p1), FadeOut(p2), FadeOut(a1), FadeOut(a2),
                      Write(rule), Create(rbox), FadeIn(other),
                      Flash(rule, color=DIST_COLOR, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: 12 x 75 ----------------------------------------------------
    def beat5_example(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            self.reset_board()

            heading = board_text("Break Big Numbers into Easy Parts", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            start = MathTex(r"12\times75", font_size=44, color=CHALK_WHITE
                            ).move_to(np.array([BOARD_CX, 0.9, 0]))
            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))
            self.play(Write(start), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            split = MathTex("75=70+5", font_size=36, color=SPLIT_COLOR).move_to(
                np.array([BOARD_CX, 0.0, 0]))
            self.play(Indicate(start, color=CHALK_YELLOW, scale_factor=1.05),
                      Write(split), run_time=rt(
                          tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            sub = MathTex("12(70+5)", font_size=42, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, 0.9, 0]))
            self.play(TransformMatchingTex(start, sub), FadeOut(split),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            step = MathTex(r"(12\times70)+(12\times5)", font_size=30,
                           color=DIST_COLOR).move_to(
                np.array([BOARD_CX, -0.9, 0]))
            self.play(Write(step), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            val = MathTex("840+60", font_size=36, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, -1.7, 0]))
            self.play(TransformMatchingTex(step, val), run_time=rt(
                tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            ans = MathTex("900", font_size=48, color=RESULT_COLOR).move_to(
                np.array([BOARD_CX, -2.45, 0]))
            abox = SurroundingRectangle(ans, color=RESULT_COLOR, buff=0.18,
                                        corner_radius=0.1, stroke_width=3)
            hint = board_text("75 = 80 − 5 also works", 16, CHALK_CYAN).move_to(
                np.array([3.6, -2.45, 0]))
            self.play(FadeOut(sub), FadeOut(val), Write(ans), Create(abox),
                      FadeIn(hint), Flash(ans, color=RESULT_COLOR,
                                          flash_radius=0.8),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: zero, the additive identity --------------------------------
    def beat6_zero(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("Adding Zero Changes Nothing", 23, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            seven = counter_group(7, DOT_COLOR, cols=4)
            seven.move_to(np.array([-2.1, 0.55, 0]))
            empty = counter_group(0, CHALK_CYAN)
            empty.move_to(np.array([1.3, 0.55, 0]))
            zero = MathTex("0", font_size=44, color=CHALK_CYAN).move_to(
                empty.outline.get_center())
            sumsign = MathTex("+", font_size=34, color=CHALK_WHITE).move_to(
                np.array([-0.35, 0.55, 0]))

            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))
            self.play(FadeIn(seven), run_time=rt(
                tracker.time_until_bookmark("b0")))
            count7 = MathTex("7", font_size=34, color=DOT_COLOR).next_to(
                seven, DOWN, buff=0.2)
            self.play(FadeIn(count7), FadeIn(empty), FadeIn(zero),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(Indicate(empty, color=CHALK_CYAN, scale_factor=1.15),
                      Indicate(zero, color=CHALK_CYAN, scale_factor=1.3),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(sumsign),
                      empty.animate.move_to(np.array([0.6, 0.55, 0])),
                      zero.animate.move_to(np.array([0.6, 0.55, 0])),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            eq = MathTex("7+0=7", font_size=36, color=RESULT_COLOR).move_to(
                np.array([BOARD_CX, -1.4, 0]))
            rule = MathTex("a+0=0+a=a", font_size=34, color=CHALK_WHITE
                           ).move_to(np.array([BOARD_CX, -2.15, 0]))
            rbox = SurroundingRectangle(rule, color=CHALK_CYAN, buff=0.14,
                                        corner_radius=0.1, stroke_width=3)
            lbl = board_text("ADDITIVE IDENTITY = 0", 18, CHALK_CYAN, "BOLD"
                             ).move_to(np.array([BOARD_CX, 1.7, 0]))
            self.play(Write(eq), Flash(eq, color=RESULT_COLOR, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.2))
            self.play(Write(rule), Create(rbox), FadeIn(lbl),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: one, the multiplicative identity ---------------------------
    def beat7_one(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("Multiplying by One Changes Nothing", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            group = counter_group(7, DOT_COLOR, cols=4)
            group.move_to(np.array([-2.2, 0.75, 0]))
            one_lbl = MathTex("1", font_size=34, color=CHALK_CYAN).next_to(
                group, LEFT, buff=0.25)
            times = MathTex(r"\times", font_size=32, color=CHALK_WHITE)
            eq1 = MathTex(r"1\times7=7", font_size=32, color=CHALK_WHITE
                          ).move_to(np.array([2.4, 0.75, 0]))

            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))
            self.play(FadeIn(group), FadeIn(one_lbl), FadeIn(times.next_to(
                one_lbl, RIGHT, buff=0.15)), Write(eq1),
                run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            solo_txt = board_text("1 group of 7", 18, CHALK_CYAN, "BOLD"
                                  ).move_to(np.array([-2.2, -0.15, 0]))
            self.play(FadeIn(solo_txt, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # the same seven counters regroup into seven groups of one
            singles = VGroup(*[counter_group(1, CHALK_PINK, r=0.09,
                                             pad=0.1) for _ in range(7)]
                             ).arrange(RIGHT, buff=0.12).move_to(
                np.array([BOARD_CX, -1.1, 0]))
            targets = [g.outline.get_center() for g in singles]
            self.play(FadeIn(singles), run_time=rt(
                tracker.time_until_bookmark("b2") * 0.4))
            self.play(*[d.animate.move_to(np.array([t[0], t[1], 0.0]))
                        for d, t in zip(group.dots, targets)],
                      FadeOut(group.outline), FadeOut(solo_txt),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            eq2 = MathTex(r"7\times1=7", font_size=32, color=CHALK_WHITE
                          ).move_to(np.array([2.4, -1.1, 0]))
            rule = MathTex(r"a\times1=1\times a=a", font_size=32,
                           color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, -2.1, 0]))
            rbox = SurroundingRectangle(rule, color=CHALK_PINK, buff=0.14,
                                        corner_radius=0.1, stroke_width=3)
            lbl = board_text("MULTIPLICATIVE IDENTITY = 1", 18, CHALK_PINK,
                             "BOLD").move_to(np.array([BOARD_CX, 1.7, 0]))
            self.play(TransformMatchingTex(eq1, eq2),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.55))
            self.play(Write(rule), Create(rbox), FadeIn(lbl),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)

            warn = board_text("7 × 0 = 0 — multiplying by zero is different!", 16,
                              CHALK_RED, "BOLD").move_to(
                np.array([BOARD_CX, -2.6, 0]))
            self.play(FadeIn(warn), run_time=rt(
                tracker.get_remaining_duration()))
            self.add_sound(self.sfx["ding"], gain=-13)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the milk vendor -------------------------------------------
    def beat8_milk(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("Distributivity in Daily Life", 23, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            morning = milk_can("56 L", CHALK_CYAN).move_to(
                np.array([-2.9, 0.85, 0]))
            evening = milk_can("44 L", CHALK_PINK).move_to(
                np.array([-0.9, 0.85, 0]))
            price = board_text("Rs 30 per litre", 19, CHALK_YELLOW, "BOLD").move_to(
                np.array([2.7, 0.85, 0]))
            pbox = SurroundingRectangle(price, color=CHALK_YELLOW, buff=0.16,
                                        corner_radius=0.1, stroke_width=2.4)

            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))
            self.play(FadeIn(morning, shift=UP * 0.1),
                      FadeIn(evening, shift=UP * 0.1),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.6))
            self.play(FadeIn(price), Create(pbox), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            e1 = MathTex(r"(56\times30)+(44\times30)", font_size=30,
                         color=DIST_COLOR).move_to(
                np.array([BOARD_CX, -0.65, 0]))
            self.play(Indicate(morning), Indicate(evening),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.play(Write(e1), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            e2 = MathTex(r"(56+44)\times30", font_size=34, color=SPLIT_COLOR
                         ).move_to(np.array([BOARD_CX, -1.45, 0]))
            tag = board_text("common multiplier 30", 16, SPLIT_COLOR, "BOLD"
                             ).move_to(np.array([3.7, -1.45, 0]))
            self.play(TransformMatchingTex(e1, e2), FadeIn(tag),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            e3 = MathTex(r"100\times30", font_size=34, color=CHALK_WHITE
                         ).move_to(np.array([BOARD_CX, -2.1, 0]))
            self.play(TransformMatchingTex(e2, e3), FadeOut(tag),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.5))
            ans = board_text("Rs 3000", 36, RESULT_COLOR, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))
            abox = SurroundingRectangle(ans, color=RESULT_COLOR, buff=0.16,
                                        corner_radius=0.1, stroke_width=3)
            self.play(FadeOut(e3), Write(ans), Create(abox),
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
            expr = MathTex("5", "(", "7", "+", "8", ")", "=?", font_size=46,
                           color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, 1.2, 0]))
            hint = board_text("Multiply 5 by each term inside the bracket.", 18,
                              CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, 0.25, 0]))
            pause = board_text("Pause and try it.", 18, CHALK_WHITE, "BOLD"
                               ).move_to(np.array([BOARD_CX, -1.9, 0]))

            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.play(Write(expr), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(FadeIn(hint, shift=RIGHT * 0.12), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(pause, shift=UP * 0.1), run_time=rt(
                tracker.get_remaining_duration()))

            self.challenge = {"expr": expr, "hint": hint, "pause": pause}
            self._capture_srt(tracker)

        play_challenge_countdown(self, seconds=4, sfx=self.sfx)

        with self.voiceover(text=NARRATION["scene9_reveal"]) as tracker:
            ch = self.challenge
            expr = ch["expr"]
            self.play(FadeOut(ch["pause"]), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.3))

            a1 = dist_arrow(expr[0], expr[2], DIST_COLOR)
            a2 = dist_arrow(expr[0], expr[4], DIST_COLOR)
            step = MathTex(r"(5\times7)+(5\times8)", font_size=32,
                           color=DIST_COLOR).move_to(
                np.array([BOARD_CX, -0.4, 0]))
            self.play(Create(a1), Create(a2), FadeOut(ch["hint"]), Write(step),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            val = MathTex("35+40=75", font_size=34, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, -1.1, 0]))
            self.play(TransformMatchingTex(step, val), run_time=rt(
                tracker.time_until_bookmark("b2") * 0.5))
            self.add_sound(self.sfx["ding"], gain=-13)

            ans = MathTex("75", font_size=44, color=RESULT_COLOR).move_to(
                np.array([BOARD_CX, -1.95, 0]))
            abox = SurroundingRectangle(ans, color=RESULT_COLOR, buff=0.18,
                                        corner_radius=0.1, stroke_width=3)
            self.play(Write(ans), Create(abox),
                      Flash(ans, color=RESULT_COLOR, flash_radius=0.8),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.play(FadeOut(expr), FadeOut(val), FadeOut(a1), FadeOut(a2),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.25))
            self.add_sound(self.sfx["success"], gain=-11)

            q1 = MathTex("9+0=?", font_size=32, color=CHALK_CYAN).move_to(
                np.array([-1.7, 1.2, 0]))
            q2 = MathTex(r"9\times1=?", font_size=32, color=CHALK_PINK).move_to(
                np.array([2.6, 1.2, 0]))
            a1t = MathTex("9+0=9", font_size=30, color=CHALK_CYAN).move_to(q1)
            a2t = MathTex(r"9\times1=9", font_size=30, color=CHALK_PINK).move_to(
                q2)
            self.play(FadeIn(q1), FadeIn(q2), run_time=rt(
                tracker.time_until_bookmark("b3") * 0.25))
            self.play(TransformMatchingTex(q1, a1t),
                      TransformMatchingTex(q2, a2t),
                      Flash(a1t, color=CHALK_CYAN, flash_radius=0.5),
                      run_time=rt(tracker.get_remaining_duration()))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 10: summary + thanks -----------------------------------------
    def beat10_summary(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("Distributive Property & Identities", 23,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y - 0.05, 0]))
            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))

            grid = dot_grid(2, 4, spacing=0.3, r=0.055)
            grid2 = dot_grid(3, 4, spacing=0.3, r=0.055)
            grid.move_to(np.array([-3.3, 1.15, 0]))
            grid2.move_to(np.array([-3.3, 0.5, 0]))
            dist_card = VGroup(
                board_text("DISTRIBUTIVE", 15, DIST_COLOR, "BOLD"),
                board_text("split the group", 13, CHALK_WHITE),
                MathTex("a(b+c)=ab+ac", font_size=22, color=DIST_COLOR),
            ).arrange(DOWN, buff=0.14).move_to(np.array([-0.6, 1.0, 0]))

            seven = counter_group(7, DOT_COLOR, cols=4, r=0.07, pad=0.12)
            seven.move_to(np.array([2.2, 1.15, 0]))
            empty = counter_group(0, CHALK_CYAN, pad=0.12).move_to(
                np.array([3.3, 1.15, 0]))
            add_card = VGroup(
                board_text("ADDITIVE IDENTITY", 15, CHALK_CYAN, "BOLD"),
                board_text("+ 0 keeps the number", 13, CHALK_WHITE),
                MathTex("a+0=a", font_size=22, color=CHALK_CYAN),
            ).arrange(DOWN, buff=0.14).move_to(np.array([3.6, -0.5, 0]))

            one_lbl = MathTex("1", font_size=34, color=CHALK_PINK).move_to(
                np.array([-3.3, -0.75, 0]))
            seven2 = counter_group(7, DOT_COLOR, cols=4, r=0.07, pad=0.12)
            seven2.move_to(np.array([-1.6, -0.75, 0]))
            mul_card = VGroup(
                board_text("MULTIPLICATIVE IDENTITY", 15, CHALK_PINK, "BOLD"),
                board_text("× 1 keeps the number", 13, CHALK_WHITE),
                MathTex(r"a\times1=a", font_size=22, color=CHALK_PINK),
            ).arrange(DOWN, buff=0.14).move_to(np.array([1.6, -1.75, 0]))

            self.play(FadeIn(dist_card, shift=RIGHT * 0.15), FadeIn(grid),
                      FadeIn(grid2),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(FadeIn(seven), FadeIn(empty),
                      FadeIn(add_card, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(FadeIn(one_lbl), FadeIn(seven2),
                      FadeIn(mul_card, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["pop"], gain=-13)

            take = board_text("Distribute to simplify. The identities keep a "
                              "number unchanged.", 18, CHALK_YELLOW, "BOLD"
                              ).move_to(np.array([BOARD_CX, -2.45, 0]))
            rows = VGroup(
                summary_row(1, "Distribute over addition:", "a(b+c)=ab+ac",
                            DIST_COLOR),
                summary_row(2, "Additive identity:", "a+0=a", CHALK_CYAN),
                summary_row(3, "Multiplicative identity:", r"a\times1=a",
                            CHALK_PINK),
            ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX, 0.15, 0]))
            rows.shift(RIGHT * (BOARD_CX - rows.get_center()[0]))
            self.play(FadeIn(take), Flash(take, color=CHALK_YELLOW,
                                          flash_radius=0.9),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.5))
            self.play(FadeOut(VGroup(dist_card, grid, grid2, seven, empty,
                                     add_card, one_lbl, seven2, mul_card)),
                      FadeIn(rows),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)

            summary = VGroup(heading, rows, take)
            self.play(FadeOut(summary), run_time=rt(
                tracker.time_until_bookmark("b5") * 0.5))

            thanks = board_text("Thank You for Watching!", 40, CHALK_WHITE,
                                "BOLD")
            thanks2 = board_text("See you in the next lesson :)", 25, CHALK_CYAN)
            thanks_group = VGroup(thanks, thanks2).arrange(DOWN, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY, 0]))
            self.play(Write(thanks), run_time=rt(
                tracker.time_until_bookmark("b5") * 0.5))
            self.add_sound(self.sfx["ding"], gain=-11)
            self.play(FadeIn(thanks2, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b5")))
            self.play(Circumscribe(thanks_group, color=CHALK_AMBER,
                                   stroke_width=3, time_width=0.5), run_time=0.3)
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(END_HOLD)


if __name__ == "__main__":
    pass

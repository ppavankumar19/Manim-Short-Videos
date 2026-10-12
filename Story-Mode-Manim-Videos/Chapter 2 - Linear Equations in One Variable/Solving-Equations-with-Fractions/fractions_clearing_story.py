"""
Solving Equations with Fractions — Clear the Denominators
Story-mode chalkboard lesson (Telangana Class 8 Maths, Chapter 2:
Linear Equations in One Variable, reducing equations with fractions).

Core idea: denominators are barriers, not magic. Multiplying BOTH sides by a
denominator removes it, and the cancellation is shown happening. Once the
fractions are gone the equation is an ordinary linear equation. When the
equation is one fraction equal to another, the same two multiplications give
the cross-multiplication shortcut A*D = B*C -- which the video uses only AFTER
deriving it.

Production pipeline (mirrors the rest of the Story-Mode series):
  - shared assets/background2.png chalkboard + student/teacher cutouts +
    dhimantAI (top-left) and Mathematics (top-right) corner badges.
  - VoiceoverScene + speech service; narration written as natural prose.
  - synced_voice.install_synced_voiceover() re-times every word against the
    real audio.
  - real per-line SRT export (carry-safe timestamps).
  - sound effects from sound_effects.py, chalk-styled Text/MathTex.
  - story_common.play_challenge_countdown() for the "YOUR TURN" clock.

Title + 10 beats:
  0. Title card.
  1. The Fraction Barrier -- the equation assembled from its parts.
  2. Why Clearing Works -- xB then xD, cancellation, A*D = B*C.
  3. Where Cross-Multiplication Comes From -- Example 19 derivation.
  4. Solve Normally -- x = 2.
  5. Cross-Multiply -- Example 20.
  6. Finish It -- x = -3 and the check.
  7. Discount -- (76/100)x = 380 -> Rs 500.
  8. Which Method? -- LCM or cross-multiply.
  9. Student Challenge -- x/3 - x/5 = 4 -> x = 30.
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
    ImageMobject, MathTex, VGroup, VMobject, Line, DashedLine, Circle,
    Rectangle, RoundedRectangle, Polygon, Triangle, Arrow, DoubleArrow, Text,
    Write, FadeIn, FadeOut, Create, ReplacementTransform, TransformMatchingTex,
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

NUM_COLOR = CHALK_CYAN       # numerators keep one colour
DEN_COLOR = CHALK_AMBER      # denominators keep another
BAR_COLOR = CHALK_WHITE
MULT_COLOR = CHALK_YELLOW    # the travelling multiplier

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

EQ_Y = 1.3
HEAD_Y = BOARD_TOP - 0.45


def rt(seconds: float, floor: float = MIN_RT) -> float:
    return max(floor, float(seconds))


def board_text(s: str, size: int = 34, color: str = CHALK_WHITE,
               weight: str = "NORMAL") -> Text:
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def chalk_math(s: str, size: int = 34, color: str = MATH_COLOR) -> MathTex:
    return MathTex(s, font_size=size, color=color)


def centre_on(mob, cx: float = BOARD_CX, cy: float = EQ_Y):
    """Centre any mobject (equation or group) on the board."""
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


# ------------------------------------------------------ fraction machinery --
def frac(num: str, den: str, size: int = 34,
         num_color: str = NUM_COLOR, den_color: str = DEN_COLOR,
         bar_color: str = BAR_COLOR) -> VGroup:
    """A fraction built from separate parts, so the bar, the numerator and the
    denominator can each be animated (pulsed, slashed, cancelled) on their own."""
    n = MathTex(num, font_size=size, color=num_color)
    d = MathTex(den, font_size=size, color=den_color)
    width = max(n.width, d.width) + 0.16
    bar = Line(np.array([-width / 2, 0, 0]), np.array([width / 2, 0, 0]),
               stroke_color=bar_color, stroke_width=2.8)
    grp = VGroup(n, bar, d).arrange(DOWN, buff=0.12)
    grp.num, grp.bar, grp.den = n, bar, d
    return grp


def frac_eq(f1: VGroup, f2: VGroup, size: int = 40) -> VGroup:
    """`f1 = f2`, with the equals sign its own mobject so it never moves."""
    eq = MathTex("=", font_size=size, color=CHALK_WHITE)
    grp = VGroup(f1, eq, f2).arrange(RIGHT, buff=0.34)
    grp.eq, grp.f1, grp.f2 = eq, f1, f2
    return grp


def cross_arrows(left: VGroup, right: VGroup, color: str = CHALK_GREEN,
                 bow: float = 0.28) -> VGroup:
    """The two diagonal cross-multiplication arrows between two fractions."""
    from manim import CurvedArrow
    a = CurvedArrow(left.num.get_right() + RIGHT * 0.04,
                    right.den.get_left() + LEFT * 0.04, angle=-bow,
                    color=color, stroke_width=2.6, tip_length=0.16)
    b = CurvedArrow(left.den.get_right() + RIGHT * 0.04,
                    right.num.get_left() + LEFT * 0.04, angle=bow,
                    color=color, stroke_width=2.6, tip_length=0.16)
    return VGroup(a, b)


def percent_bar(width: float = 6.4, height: float = 0.55,
                taken: float = 0.24, pos=np.array([BOARD_CX, 1.35, 0])) -> VGroup:
    """A 100-part bar: the discounted part is shaded, the paid part is left."""
    frame = RoundedRectangle(corner_radius=0.04, width=width, height=height,
                             stroke_color=CHALK_WHITE, stroke_width=2,
                             fill_color="#16202B", fill_opacity=0.85)
    cut = taken * width
    paid = Rectangle(width=width - cut, height=height - 0.06, stroke_width=0,
                     fill_color="#1E3B22", fill_opacity=0.9).move_to(
        frame.get_center() + RIGHT * (cut / 2))
    lost = Rectangle(width=cut, height=height - 0.06, stroke_width=0,
                     fill_color=CHALK_PINK, fill_opacity=0.45).move_to(
        frame.get_center() - RIGHT * ((width - cut) / 2))
    ticks = VGroup(*[
        Line(frame.get_top() + DOWN * height * 0.18 + RIGHT * (x - width / 2),
             frame.get_bottom() + UP * height * 0.18 + RIGHT * (x - width / 2),
             stroke_color=CHALK_WHITE, stroke_width=1, stroke_opacity=0.35)
        for x in np.linspace(0, width, 11)[1:-1]
    ])
    grp = VGroup(frame, lost, paid, ticks).move_to(pos)
    grp.frame, grp.lost, grp.paid = frame, lost, paid
    return grp


def summary_row(n: int, label: str, math_tex: str, color: str) -> VGroup:
    badge = Circle(radius=0.19, stroke_color=color, stroke_width=2,
                   fill_color=color, fill_opacity=0.18)
    num = board_text(str(n), 17, color, "BOLD").move_to(badge.get_center())
    return VGroup(VGroup(badge, num),
                  board_text(label, 18, CHALK_WHITE),
                  MathTex(math_tex, font_size=22)).arrange(RIGHT, buff=0.28)


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "Today we clear the fractions out of equations.<bookmark mark='b0'/> "
        "Fractions make an equation look harder than it really is, and there is "
        "a safe way to remove them.<bookmark mark='b1'/> Let's see how!"
        "<bookmark mark='b2'/>"
    ),
    "scene1": (
        "Here is an equation with fractions on both sides.<bookmark mark='b0'/> "
        "The left side is five x plus two, over two x plus three.<bookmark "
        "mark='b1'/> The right side is twelve over seven.<bookmark mark='b2'/> "
        "The numerators are ordinary expressions, and the fraction bars are "
        "just barriers.<bookmark mark='b3'/> So can we remove the denominators, "
        "without changing the equality?<bookmark mark='b4'/>"
    ),
    "scene2": (
        "Let's see what removing a denominator really means.<bookmark "
        "mark='b0'/> Start with A over B, equals C over D.<bookmark mark='b1'/> "
        "Multiply both sides by B.<bookmark mark='b2'/> On the left, the B "
        "cancels with the denominator, and on the right we keep B times C over "
        "D.<bookmark mark='b3'/> Now multiply both sides by D.<bookmark "
        "mark='b4'/> The D cancels on the right, and what is left is A times D, "
        "equals B times C.<bookmark mark='b5'/> The fractions are gone, and the "
        "equality is still true.<bookmark mark='b6'/>"
    ),
    "scene3": (
        "Now let's do exactly that with our equation.<bookmark mark='b0'/> "
        "First, multiply both sides by two x plus three.<bookmark mark='b1'/> "
        "The denominator on the left cancels.<bookmark mark='b2'/> Next, "
        "multiply both sides by seven.<bookmark mark='b3'/> Now the denominator "
        "on the right cancels too.<bookmark mark='b4'/> What is left is seven "
        "times, five x plus two, equals twelve times, two x plus three."
        "<bookmark mark='b5'/> Look at the pattern: each numerator is multiplied "
        "by the denominator on the opposite side.<bookmark mark='b6'/> That "
        "shortcut is called cross multiplication.<bookmark mark='b7'/>"
    ),
    "scene4": (
        "The fractions are gone, so now we solve normally.<bookmark mark='b0'/> "
        "Expanding both sides gives thirty five x plus fourteen, equals twenty "
        "four x plus thirty six.<bookmark mark='b1'/> Collecting the x terms on "
        "the left and the numbers on the right gives eleven x equals twenty two."
        "<bookmark mark='b2'/> So x equals two.<bookmark mark='b3'/>"
    ),
    "scene5": (
        "Let's use the shortcut on another equation.<bookmark mark='b0'/> Seven "
        "over, three x plus sixteen, equals four over, x plus seven.<bookmark "
        "mark='b1'/> This is one fraction equal to another, so we can cross "
        "multiply.<bookmark mark='b2'/> Seven multiplies x plus seven, and four "
        "multiplies three x plus sixteen.<bookmark mark='b3'/> That gives seven "
        "times, x plus seven, equals four times, three x plus sixteen."
        "<bookmark mark='b4'/>"
    ),
    "scene6": (
        "Now we finish it.<bookmark mark='b0'/> Expanding gives seven x plus "
        "forty nine, equals twelve x plus sixty four.<bookmark mark='b1'/> "
        "Collecting the terms gives minus five x equals fifteen.<bookmark "
        "mark='b2'/> So x equals minus three.<bookmark mark='b3'/> Let's check: "
        "seven over, three times minus three plus sixteen, is seven over seven, "
        "which is one; and four over, minus three plus seven, is four over four, "
        "which is also one.<bookmark mark='b4'/>"
    ),
    "scene7": (
        "Fractions also appear in everyday problems.<bookmark mark='b0'/> Rehana "
        "buys a dress with a twenty four percent discount, and she pays three "
        "hundred and eighty rupees.<bookmark mark='b1'/> Let the marked price be "
        "x.<bookmark mark='b2'/> The discount is twenty four hundredths of x, so "
        "she pays seventy six hundredths of x.<bookmark mark='b3'/> That equals "
        "three hundred and eighty.<bookmark mark='b4'/> Multiplying both sides by "
        "one hundred, and dividing by seventy six, gives x equals five hundred."
        "<bookmark mark='b5'/> So the marked price was five hundred rupees."
        "<bookmark mark='b6'/>"
    ),
    "scene8": (
        "So which method should you use?<bookmark mark='b0'/> If there are "
        "several fractional terms, find the LCM of the denominators, and "
        "multiply every term by it.<bookmark mark='b1'/> If the equation is one "
        "fraction equal to another, cross multiplication is quicker.<bookmark "
        "mark='b2'/> Either way, the goal is the same: remove the denominators, "
        "and then solve the linear equation.<bookmark mark='b3'/>"
    ),
    "scene9_setup": (
        "Your turn!<bookmark mark='b0'/> The third part of a number exceeds its "
        "fifth part by four.<bookmark mark='b1'/> Let the number be x, so we get "
        "x over three, minus x over five, equals four.<bookmark mark='b2'/> What "
        "should we multiply every term by?<bookmark mark='b3'/> Pause the video, "
        "and try it yourself.<bookmark mark='b4'/>"
    ),
    "scene9_reveal": (
        "The denominators are three and five, so the LCM is fifteen.<bookmark "
        "mark='b0'/> Multiply every term by fifteen: fifteen times x over three, "
        "minus fifteen times x over five, equals fifteen times four.<bookmark "
        "mark='b1'/> The denominators cancel, leaving five x minus three x "
        "equals sixty.<bookmark mark='b2'/> So two x equals sixty, and x equals "
        "thirty.<bookmark mark='b3'/> Let's check: the third part of thirty is "
        "ten, the fifth part is six, and ten minus six is four.<bookmark "
        "mark='b4'/> Well done!<bookmark mark='b5'/>"
    ),
    "scene10": (
        "Let's summarise.<bookmark mark='b0'/> When an equation has several "
        "fractional terms, find the LCM of the denominators, and multiply every "
        "term by it.<bookmark mark='b1'/> When it is one fraction equal to "
        "another, cross multiply: A times D, equals B times C.<bookmark "
        "mark='b2'/> Both methods do the same job: they clear the denominators."
        "<bookmark mark='b3'/> After that the equation is linear, and we solve "
        "it normally, and check the answer.<bookmark mark='b4'/> Clear first, "
        "solve second. Thank you so much for watching, and I will see you in the "
        "next lesson!<bookmark mark='b5'/>"
    ),
}


class FractionsClearingStory(VoiceoverScene):
    """Story-mode chalkboard lesson: fractional linear equations."""

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
        out_dir = _HERE / "media" / "videos" / "fractions_clearing_story"
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
        self.beat1_barrier()
        self.beat2_why()
        self.beat3_derive()
        self.beat4_solve()
        self.beat5_apply()
        self.beat6_finish()
        self.beat7_discount()
        self.beat8_methods()
        self.beat9_challenge()
        self.beat10_summary()

        self._write_real_srt()

    # ================================================================ beats ==

    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Solving Equations with Fractions", 36,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 1.6, 0]))
            self.play(Write(title), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            sub = board_text("Clear the denominators", 21, CHALK_YELLOW,
                             "BOLD").move_to(np.array([BOARD_CX, BOARD_CY + 0.9, 0]))
            self.play(Write(sub), run_time=rt(tracker.time_until_bookmark("b1") * 0.4))

            f1 = frac("A", "B", size=40)
            f2 = frac("C", "D", size=40)
            eq = frac_eq(f1, f2, size=44).move_to(np.array([BOARD_CX, -0.75, 0]))
            tag = board_text("Do the same operation to both sides.", 18,
                             CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX, -2.05, 0]))
            self.play(FadeIn(eq, shift=DOWN * 0.1), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.6))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(FadeIn(tag), Flash(tag, color=CHALK_CYAN, flash_radius=0.8),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 1: the fraction barrier ---------------------------------------
    def beat1_barrier(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("The Fraction Barrier", 25, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            f1 = frac("5x+2", "2x+3", size=46)
            f2 = frac("12", "7", size=46)
            eq = frac_eq(f1, f2, size=48)
            centre_on(eq, BOARD_CX, 0.85)

            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))
            # numerators first, then the bars, then the denominators
            self.play(FadeIn(f1.num), FadeIn(f2.num), FadeIn(eq.eq),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(Create(f1.bar), Create(f2.bar),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(FadeIn(f1.den), FadeIn(f2.den),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            hit = board_text("Same equation — just extra layers.", 18,
                             CHALK_WHITE).move_to(np.array([BOARD_CX, -1.15, 0]))
            self.play(FadeIn(hit), run_time=rt(tracker.time_until_bookmark("b3") * 0.6))
            self.play(Circumscribe(VGroup(f1.den, f2.den),
                                   color=DEN_COLOR, stroke_width=3),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            question = board_text("Can we remove the denominators?", 19,
                                  CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, -2.1, 0]))
            self.play(FadeIn(question), Flash(question, color=CHALK_PINK,
                                              flash_radius=0.8),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["swipe"], gain=-15)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 2: why clearing works -----------------------------------------
    def beat2_why(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("Why Clearing Works", 25, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            eq = MathTex(r"\frac{A}{B}", "=", r"\frac{C}{D}", font_size=46)
            centre_on(eq, BOARD_CX, 1.15)
            self.play(Write(heading), FadeIn(eq), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.6))
            self.play(Indicate(eq[0], color=DEN_COLOR, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # b1: the starting equation, on its own
            self.play(Indicate(eq, color=CHALK_WHITE, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b1")))

            # b2: multiply both sides by B  (plain MathTex, transformed)
            e2 = MathTex("B\\times", r"\frac{A}{B}", "=", "B\\times",
                         r"\frac{C}{D}", font_size=44)
            centre_on(e2, BOARD_CX, 1.15)
            e2_left = VGroup(e2[0], e2[1])
            e2_right = VGroup(e2[3], e2[4])
            den_l = np.array([e2[1].get_center()[0],
                              e2[1].get_bottom()[1] + 0.16, 0])
            self.play(TransformMatchingTex(eq, e2), run_time=rt(
                tracker.time_until_bookmark("b2") * 0.5))
            self.play(Indicate(e2_left, color=MULT_COLOR, scale_factor=1.0),
                      Indicate(e2_right, color=MULT_COLOR, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            # b3: the left denominator cancels away
            e3 = MathTex("A", "=", "B\\times", r"\frac{C}{D}", font_size=44)
            centre_on(e3, BOARD_CX, 1.15)
            e3_right = VGroup(e3[2], e3[3])
            self.play(TransformMatchingTex(e2, e3),
                      Flash(den_l, color=CHALK_RED, flash_radius=0.45),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.play(Indicate(e3_right, color=MULT_COLOR, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            # b4: ... then the same with D
            e4 = MathTex("D\\times", "A", "=", "B\\times", r"\frac{C}{D}",
                         "\\times D", font_size=44)
            centre_on(e4, BOARD_CX, 1.15)
            e4_left = VGroup(e4[0], e4[1])
            e4_right = VGroup(e4[3], e4[4], e4[5])
            den_r = np.array([e4[4].get_center()[0],
                              e4[4].get_bottom()[1] + 0.16, 0])
            self.play(TransformMatchingTex(e3, e4), run_time=rt(
                tracker.time_until_bookmark("b4") * 0.5))
            self.play(Indicate(e4_left, color=MULT_COLOR, scale_factor=1.0),
                      Indicate(e4_right, color=MULT_COLOR, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            final = MathTex("A\\times D", "=", "B\\times C", font_size=48,
                            color=CHALK_GREEN)
            centre_on(final, BOARD_CX, 1.15)
            fbox = SurroundingRectangle(final, color=CHALK_GREEN, buff=0.2,
                                        corner_radius=0.1, stroke_width=3)
            note = board_text("The fractions are gone — the equality stayed true.",
                              18, CHALK_WHITE).move_to(
                np.array([BOARD_CX, -0.15, 0]))
            self.play(TransformMatchingTex(e4, final), Create(fbox),
                      Flash(den_r, color=CHALK_RED, flash_radius=0.45),
                      run_time=rt(tracker.time_until_bookmark("b5") * 0.6))
            self.play(FadeIn(note), Flash(final, color=CHALK_GREEN, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["success"], gain=-11)

            rule = board_text("Do the same operation to both sides.", 18,
                              CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.2, 0]))
            self.play(FadeOut(note), FadeIn(rule),
                      run_time=rt(tracker.time_until_bookmark("b6") * 0.6))
            self.add_sound(self.sfx["ding"], gain=-12)
            self.play(Indicate(final, color=CHALK_GREEN, scale_factor=1.03),
                      run_time=rt(tracker.get_remaining_duration()))
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 3: where cross-multiplication comes from ----------------------
    def beat3_derive(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()

            heading = board_text("Where the Shortcut Comes From", 23,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            f1 = frac("5x+2", "2x+3", size=40)
            f2 = frac("12", "7", size=40)
            eq = frac_eq(f1, f2, size=44)
            centre_on(eq, BOARD_CX, 1.2)
            self.play(Write(heading), FadeIn(eq), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.5))
            self.play(Indicate(f1.den, color=DEN_COLOR, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            m1 = MathTex("(2x+3)\\times", font_size=36, color=MULT_COLOR)
            self.play(FadeIn(m1.next_to(f1, LEFT, buff=0.1)),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.6))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            # the denominator cancels away (it fades out of the fraction)
            self.play(f1.den.animate.set_opacity(0.12),
                      Flash(f1.den.get_center(), color=CHALK_RED, flash_radius=0.45),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            m2 = MathTex("\\times 7", font_size=36, color=MULT_COLOR)
            self.play(FadeIn(m2.next_to(f2, RIGHT, buff=0.1)),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.6))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(f2.den.animate.set_opacity(0.12),
                      Flash(f2.den.get_center(), color=CHALK_RED, flash_radius=0.45),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["click"], gain=-15)

            clean = MathTex("7(5x+2)", "=", "12(2x+3)", font_size=44)
            centre_on(clean, BOARD_CX, 0.6)
            cbox = SurroundingRectangle(clean, color=CHALK_GREEN, buff=0.2,
                                        corner_radius=0.1, stroke_width=3)
            self.play(FadeOut(VGroup(eq, m1, m2)),
                      Write(clean), Create(cbox),
                      run_time=rt(tracker.time_until_bookmark("b5") * 0.6))
            self.add_sound(self.sfx["pop"], gain=-13)

            # now, and only now, the diagonal shortcut
            f3 = frac("5x+2", "2x+3", size=34)
            f4 = frac("12", "7", size=34)
            small = frac_eq(f3, f4, size=38).move_to(np.array([BOARD_CX, -0.85, 0]))
            ars = cross_arrows(f3, f4, color=CHALK_GREEN)
            self.play(FadeIn(small), run_time=rt(
                tracker.time_until_bookmark("b6") * 0.5))
            self.play(Create(ars), run_time=rt(
                tracker.time_until_bookmark("b6")))
            self.add_sound(self.sfx["click"], gain=-15)

            lbl = board_text("CROSS MULTIPLICATION", 19, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -1.85, 0]))
            note = board_text("Shortcut discovered — not memorised.", 16,
                              CHALK_YELLOW).move_to(np.array([BOARD_CX, -2.4, 0]))
            self.play(FadeIn(lbl), Flash(lbl, color=CHALK_GREEN, flash_radius=0.8),
                      run_time=rt(tracker.time_until_bookmark("b7") * 0.6))
            self.play(FadeIn(note), run_time=rt(
                tracker.time_until_bookmark("b7")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 4: solve normally ---------------------------------------------
    def beat4_solve(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()

            heading = board_text("Now Solve Normally", 25, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            chain = [
                ("7(5x+2)", "=", "12(2x+3)", "b0"),
                ("35x+14", "=", "24x+36", "b0"),
                ("35x-24x", "=", "36-14", "b1"),
                ("11x", "=", "22", "b2"),
            ]
            cur = None
            for lhs, mid, rhs, mark in chain:
                nxt = MathTex(lhs, r"\;=\;", rhs, font_size=40)
                centre_on(nxt, BOARD_CX, 1.2)
                if cur is None:
                    self.play(Write(nxt), run_time=rt(
                        tracker.time_until_bookmark(mark) * 0.4))
                else:
                    self.play(TransformMatchingTex(cur, nxt),
                              run_time=rt(tracker.time_until_bookmark(mark)))
                    self.add_sound(self.sfx["click"], gain=-15)
                cur = nxt

            final = MathTex("x", r"\;=\;", "2", font_size=48, color=CHALK_GREEN)
            centre_on(final, BOARD_CX, 1.2)
            self.play(TransformMatchingTex(cur, final),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.6))
            ans = MathTex("x", "=", "2", font_size=44, color=CHALK_GREEN).move_to(
                np.array([BOARD_CX, 0.0, 0]))
            abox = SurroundingRectangle(ans, color=CHALK_GREEN, buff=0.22,
                                        corner_radius=0.1, stroke_width=3)
            note = board_text("Fractions gone — familiar algebra.", 18,
                              CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.15, 0]))
            self.play(FadeOut(final), run_time=0.2)
            self.play(FadeIn(ans), Create(abox), FadeIn(note),
                      Flash(ans, color=CHALK_GREEN, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 5: apply cross-multiplication ---------------------------------
    def beat5_apply(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            self.reset_board()

            heading = board_text("One Fraction Equals One Fraction", 23,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            f1 = frac("7", "3x+16", size=40)
            f2 = frac("4", "x+7", size=40)
            eq = frac_eq(f1, f2, size=44)
            centre_on(eq, BOARD_CX, 1.15)
            self.play(Write(heading), FadeIn(eq), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.5))
            self.add_sound(self.sfx["pop"], gain=-13)

            structure = board_text("one fraction  =  one fraction", 17,
                                   CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX, 0.15, 0]))
            self.play(FadeIn(structure), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            ar1 = ArcBetweenPoints(f1.num.get_right() + RIGHT * 0.04,
                                   f2.den.get_left() + LEFT * 0.04, angle=-0.28
                                   ).set_stroke(color=CHALK_GREEN, width=2.6
                                                ).add_tip(tip_length=0.14,
                                                          tip_width=0.14)
            self.play(Create(ar1), run_time=rt(
                tracker.time_until_bookmark("b2") * 0.5))
            ar2 = ArcBetweenPoints(f1.den.get_right() + RIGHT * 0.04,
                                   f2.num.get_left() + LEFT * 0.04, angle=0.28
                                   ).set_stroke(color=CHALK_GREEN, width=2.6
                                                ).add_tip(tip_length=0.14,
                                                          tip_width=0.14)
            self.play(Create(ar2), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            prod = MathTex("7(x+7)", "=", "4(3x+16)", font_size=44)
            centre_on(prod, BOARD_CX, -0.75)
            pbox = SurroundingRectangle(prod, color=CHALK_GREEN, buff=0.2,
                                       corner_radius=0.1, stroke_width=3)
            self.play(TransformFromCopy(VGroup(f1.num, f2.den), prod[0]),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            self.play(TransformFromCopy(VGroup(f1.den, f2.num), prod[2]),
                      FadeIn(prod[1]), Create(pbox),
                      Flash(prod, color=CHALK_GREEN, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)

            note = board_text("Cross the numerator with the opposite denominator.",
                              16, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.7, 0]))
            self.play(FadeOut(structure), FadeIn(note), run_time=rt(
                tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-12)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 6: finish the example -----------------------------------------
    def beat6_finish(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("Clear, Expand, Group, Solve", 23, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            chain = [
                ("7(x+7)", "=", "4(3x+16)", "b0"),
                ("7x+49", "=", "12x+64", "b0"),
                ("7x-12x", "=", "64-49", "b1"),
                ("-5x", "=", "15", "b2"),
            ]
            cur = None
            for lhs, mid, rhs, mark in chain:
                nxt = MathTex(lhs, r"\;=\;", rhs, font_size=40)
                centre_on(nxt, BOARD_CX, 1.25)
                if cur is None:
                    self.play(Write(nxt), run_time=rt(
                        tracker.time_until_bookmark(mark) * 0.4))
                else:
                    self.play(TransformMatchingTex(cur, nxt),
                              run_time=rt(tracker.time_until_bookmark(mark)))
                    self.add_sound(self.sfx["click"], gain=-15)
                cur = nxt

            final = MathTex("x", r"\;=\;", "-3", font_size=48, color=CHALK_GREEN)
            centre_on(final, BOARD_CX, 1.25)
            self.play(TransformMatchingTex(cur, final),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.6))

            chk = MathTex(r"\frac{7}{7}", "=", "1", r"\quad", r"\frac{4}{4}", "=",
                          "1", font_size=34, color=CHALK_GREEN).move_to(
                np.array([BOARD_CX, 0.2, 0]))
            ck = tick_beside(chk, CHALK_GREEN, 0.32, 0.3)
            note = board_text("Both sides are 1 — the answer checks.", 17,
                              CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -0.75, 0]))
            self.play(FadeOut(final), run_time=0.2)
            self.play(Write(chk), run_time=rt(
                tracker.time_until_bookmark("b3") * 0.4))
            self.play(Create(ck), Flash(chk, color=CHALK_GREEN, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)

            ans = MathTex("x", "=", "-3", font_size=44, color=CHALK_GREEN).move_to(
                np.array([BOARD_CX, -1.6, 0]))
            abox = SurroundingRectangle(ans, color=CHALK_GREEN, buff=0.2,
                                        corner_radius=0.1, stroke_width=3)
            self.play(FadeIn(note), FadeIn(ans), Create(abox),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-12)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 7: the discount ------------------------------------------------
    def beat7_discount(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("Real Life: A Discount", 25, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            bar = percent_bar(width=6.6, height=0.6, taken=0.24,
                              pos=np.array([BOARD_CX, 1.5, 0]))
            price = MathTex(r"\text{marked price } x", font_size=28, color=NUM_COLOR
                            ).next_to(bar, UP, buff=0.16)
            self.play(FadeIn(bar), FadeIn(price), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.7))
            self.add_sound(self.sfx["pop"], gain=-13)

            disc = board_text("24% discount", 16, CHALK_PINK, "BOLD").next_to(
                bar.lost, UP, buff=0.1)
            self.play(FadeIn(disc), Indicate(bar.lost, color=CHALK_PINK,
                                             scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            left = board_text("76% is paid", 16, CHALK_GREEN, "BOLD").next_to(
                bar.paid, DOWN, buff=0.12)
            paid_amt = board_text("= 380 rupees", 16, CHALK_GREEN, "BOLD").next_to(
                left, RIGHT, buff=0.3)
            self.play(FadeIn(left), FadeIn(paid_amt), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            fact = MathTex(r"\frac{76}{100}x", "=", "380", font_size=38)
            centre_on(fact, BOARD_CX, -0.5)
            self.play(FadeIn(fact), run_time=rt(
                tracker.time_until_bookmark("b3") * 0.6))
            self.play(Indicate(fact[0], color=DEN_COLOR, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            step = MathTex("x", "=", r"\frac{380\times 100}{76}", font_size=36)
            centre_on(step, BOARD_CX, -0.5)
            self.play(TransformMatchingTex(fact, step), run_time=rt(
                tracker.time_until_bookmark("b4") * 0.5))
            final = MathTex(r"\text{Rs }500", font_size=44, color=CHALK_GREEN)
            centre_on(final, BOARD_CX, -0.5)
            fbox = SurroundingRectangle(final, color=CHALK_GREEN, buff=0.22,
                                        corner_radius=0.1, stroke_width=3)
            self.play(TransformMatchingTex(step, final), Create(fbox),
                      Flash(final, color=CHALK_GREEN, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)

            note = board_text("Marked price = Rs 500", 18, CHALK_YELLOW,
                              "BOLD").move_to(np.array([BOARD_CX, -2.4, 0]))
            self.play(FadeIn(note), run_time=rt(
                tracker.time_until_bookmark("b5") * 0.6))
            self.play(Indicate(final, color=CHALK_GREEN, scale_factor=1.05),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["ding"], gain=-12)
            self.play(FadeOut(note), run_time=rt(
                tracker.time_until_bookmark("b6") * 0.5))
            self.play(Circumscribe(fbox, color=CHALK_AMBER, stroke_width=3),
                      run_time=rt(tracker.time_until_bookmark("b6")))
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 8: which method? ----------------------------------------------
    def beat8_methods(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("Which Method?", 26, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            card1 = VGroup(
                RoundedRectangle(corner_radius=0.1, width=4.3, height=2.5,
                                 stroke_color=CHALK_CYAN, stroke_width=2,
                                 fill_color="#16202B", fill_opacity=0.9),
                board_text("Several fractional terms", 15, CHALK_CYAN, "BOLD"),
                MathTex(r"\frac{x}{3}-\frac{x}{5}=4", font_size=30),
                board_text("Multiply every term by the LCM", 13, CHALK_WHITE),
            )
            card1[1].move_to(card1[0].get_top() + DOWN * 0.32)
            card1[2].move_to(card1[0].get_center() + UP * 0.12)
            card1[3].move_to(card1[0].get_center() + DOWN * 0.62)
            card2 = VGroup(
                RoundedRectangle(corner_radius=0.1, width=4.3, height=2.5,
                                 stroke_color=CHALK_GREEN, stroke_width=2,
                                 fill_color="#16202B", fill_opacity=0.9),
                board_text("One fraction = one fraction", 15, CHALK_GREEN, "BOLD"),
                MathTex(r"\frac{A}{B}=\frac{C}{D}", font_size=30),
                board_text("Cross multiply", 13, CHALK_WHITE),
            )
            card2[1].move_to(card2[0].get_top() + DOWN * 0.32)
            card2[2].move_to(card2[0].get_center() + UP * 0.12)
            card2[3].move_to(card2[0].get_center() + DOWN * 0.62)
            cards = VGroup(card1, card2).arrange(RIGHT, buff=0.5).move_to(
                np.array([BOARD_CX, 0.55, 0]))
            cards.shift(RIGHT * (BOARD_CX - cards.get_center()[0]))

            self.play(FadeIn(card1, shift=DOWN * 0.15), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(Indicate(card1[2], color=CHALK_CYAN, scale_factor=1.03),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(card2, shift=DOWN * 0.15), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            goal = board_text("Same goal: remove every denominator.", 18,
                              CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.35, 0]))
            self.play(FadeIn(goal), Circumscribe(goal, color=CHALK_YELLOW,
                                                 stroke_width=3),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 9: student challenge -----------------------------------------
    def beat9_challenge(self) -> None:
        with self.voiceover(text=NARRATION["scene9_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", 30, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y - 0.05, 0]))
            problem = board_text("The third part of a number exceeds its fifth "
                                 "part by 4.", 18, CHALK_WHITE).move_to(
                np.array([BOARD_CX, 2.1, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.play(FadeIn(problem), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            f1 = frac("x", "3", size=38)
            f2 = frac("x", "5", size=38)
            eq = VGroup(f1, MathTex("-", font_size=38), f2,
                        MathTex("=", font_size=38),
                        MathTex("4", font_size=38)).arrange(RIGHT, buff=0.26)
            centre_on(eq, BOARD_CX, 0.75)
            self.play(FadeIn(eq), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["pop"], gain=-13)

            ask = board_text("What should we multiply every term by?", 17,
                             CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX, -0.35, 0]))
            pause = board_text("Pause and try it", 19, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.05, 0]))
            self.play(FadeIn(ask), run_time=rt(
                tracker.time_until_bookmark("b3") * 0.5))
            self.play(FadeIn(pause), run_time=rt(
                tracker.time_until_bookmark("b3") * 0.85))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(Indicate(eq, color=CHALK_YELLOW, scale_factor=1.03),
                      run_time=rt(tracker.get_remaining_duration() * 0.9))
            self.challenge = VGroup(heading, problem, eq, ask, pause)
            self._capture_srt(tracker)

        play_challenge_countdown(self, seconds=6, sfx=self.sfx)

        with self.voiceover(text=NARRATION["scene9_reveal"]) as tracker:
            eq = self.challenge[2]
            self.play(FadeOut(self.challenge[4]), FadeOut(self.challenge[3]),
                      run_time=0.3)

            lcm = MathTex("\\text{LCM}(3,5)=15", font_size=34, color=MULT_COLOR
                          ).move_to(np.array([BOARD_CX, -0.3, 0]))
            self.play(Write(lcm), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.6))
            self.add_sound(self.sfx["ding"], gain=-13)

            cleared = MathTex("15\\left(\\frac{x}{3}\\right)",
                              "-", "15\\left(\\frac{x}{5}\\right)", "=", "15(4)",
                              font_size=34).move_to(np.array([BOARD_CX, 0.85, 0]))
            self.play(FadeOut(eq), FadeIn(cleared), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.5))
            self.play(Indicate(cleared[0], color=MULT_COLOR, scale_factor=1.0),
                      Indicate(cleared[2], color=MULT_COLOR, scale_factor=1.0),
                      Indicate(cleared[4], color=MULT_COLOR, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            simple = MathTex("5x-3x", "=", "60", font_size=38)
            centre_on(simple, BOARD_CX, 0.85)
            self.play(TransformMatchingTex(cleared, simple), run_time=rt(
                tracker.time_until_bookmark("b2") * 0.5))
            two = MathTex("2x", "=", "60", font_size=38)
            centre_on(two, BOARD_CX, 0.85)
            self.play(TransformMatchingTex(simple, two), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            ans = MathTex("x", "=", "30", font_size=46, color=CHALK_GREEN).move_to(
                np.array([BOARD_CX, 0.85, 0]))
            self.play(ReplacementTransform(two, ans), run_time=rt(
                tracker.time_until_bookmark("b3") * 0.6))
            abox = SurroundingRectangle(ans, color=CHALK_GREEN, buff=0.22,
                                        corner_radius=0.1, stroke_width=3)
            chk = MathTex(r"\frac{30}{3}-\frac{30}{5}", "=", "10-6", "=", "4",
                          font_size=30, color=CHALK_GREEN).move_to(
                np.array([BOARD_CX, -0.55, 0]))
            ck = tick_beside(chk, CHALK_GREEN, 0.3, 0.28)
            self.play(FadeOut(lcm), Create(abox), Flash(ans, color=CHALK_GREEN,
                                                         flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)

            self.play(Write(chk), run_time=rt(
                tracker.time_until_bookmark("b4") * 0.5))
            self.play(Create(ck), run_time=rt(
                tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-12)

            well = board_text("Well done! The LCM cleared every term.", 17,
                              CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.6, 0]))
            self.play(FadeIn(well), Flash(well, color=CHALK_YELLOW, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 10: summary ---------------------------------------------------
    def beat10_summary(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("Summary", 31, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y - 0.05, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.4))

            chain = MathTex(r"\frac{A}{B}=\frac{C}{D} \;\Rightarrow\; A\cdot D = B\cdot C",
                            font_size=26, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, 2.20, 0]))
            self.play(Write(chain), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            r1 = summary_row(1, "Several fractions:", r"\text{LCM, every term}",
                             CHALK_CYAN)
            r2 = summary_row(2, "One fraction = one fraction:", r"A\cdot D=B\cdot C",
                             CHALK_GREEN)
            r3 = summary_row(3, "Then the equation is linear:", r"11x=22", CHALK_AMBER)
            r4 = summary_row(4, "Solve and check:", r"x=2,\; x=-3,\; x=30",
                             CHALK_YELLOW)
            rows = VGroup(r1, r2, r3, r4).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
            rows.move_to(np.array([BOARD_CX, 0.50, 0]))
            rows.shift(RIGHT * (BOARD_CX - rows.get_center()[0]))

            self.play(FadeIn(r1, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(r2, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(r3, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(r4, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            take = board_text("Clear first. Solve second.", 24, CHALK_YELLOW,
                              "BOLD").move_to(np.array([BOARD_CX, -1.45, 0]))
            take2 = board_text("LCM for several fractions — cross multiply for "
                               "fraction = fraction.", 15, CHALK_CYAN).move_to(
                np.array([BOARD_CX, -2.0, 0]))
            self.play(FadeIn(take), Flash(take, color=CHALK_YELLOW, flash_radius=0.9),
                      FadeIn(take2),
                      run_time=rt(tracker.time_until_bookmark("b5") * 0.3))
            self.add_sound(self.sfx["success"], gain=-11)

            summary = VGroup(heading, chain, rows, take, take2)
            self.play(FadeOut(summary),
                      run_time=rt(tracker.time_until_bookmark("b5") * 0.3))

            thanks = board_text("Thank You for Watching!", 40, CHALK_WHITE, "BOLD")
            thanks2 = board_text("See you in the next lesson :)", 25, CHALK_CYAN)
            thanks_group = VGroup(thanks, thanks2).arrange(DOWN, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY, 0]))
            self.play(Write(thanks),
                      run_time=rt(tracker.time_until_bookmark("b5") * 0.4))
            self.add_sound(self.sfx["ding"], gain=-11)
            self.play(FadeIn(thanks2, shift=UP * 0.1),
                      run_time=rt(tracker.get_remaining_duration()))
            self.play(Circumscribe(thanks_group, color=CHALK_AMBER, stroke_width=3,
                                   time_width=0.5), run_time=0.3)
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(END_HOLD)


if __name__ == "__main__":
    pass

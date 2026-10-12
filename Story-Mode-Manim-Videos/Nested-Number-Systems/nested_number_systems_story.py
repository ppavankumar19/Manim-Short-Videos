"""
Nested Number Systems -- From Natural to Rational Numbers
Story-mode chalkboard lesson (Classes 6-12 Maths, Chapter 1 -- Rational
Numbers).

Production pipeline (mirrors the rest of the Story-Mode series):
  - assets/background2.png chalkboard backdrop, student + teacher cutouts,
    corner badges.
  - VoiceoverScene + EdgeSpeechService (en-IN-PrabhatNeural).
  - Real per-word sync via <bookmark> tags + tracker timing.
  - Ground-truth SRT from edge-tts word boundaries.
  - Shared story_common.play_challenge_countdown() for the "YOUR TURN"
    round THINK badge (board-centre, dims the whole board except itself).

Topic: N subset W subset Z subset Q -- every step keeps the previous
numbers and adds exactly what was missing (0, then negatives, then
fractions). The "growing container" (beats 2-4) is built with
ReplacementTransform from one pre-arranged row to the next specifically so
the old numbers are never erased, only carried forward -- the storyboard's
explicit production rule.

Title + 7 beats + closing summary:
  0. Title card -- text only, N->W->Z->Q preview chain.
  1. Start With Natural Numbers.
  2. Natural -> Whole (0 joins).
  3. Whole -> Integers (negatives join).
  4. Integers -> Rational (5=5/1 etc.; fractions fill gaps).
  5. Why Are They Nested? -- concentric-circle diagram.
  6. Challenge -- classify 3, 0, -1/2 (round THINK badge, whole-board dim,
     full-space bottom box).
  7. Summary -- flow recap + boxed relation + Thank You card.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from manim import (
    ORIGIN, UP, DOWN, LEFT, RIGHT, UL, UR, DL, DR, PI, BLACK,
    ImageMobject, MathTex, VGroup, Group, Line, DashedLine, Dot, Circle,
    Rectangle, RoundedRectangle, Arrow, Text, Write, FadeIn, FadeOut,
    Create, Transform, ReplacementTransform, GrowFromCenter, GrowArrow,
    LaggedStart, AnimationGroup, DrawBorderThenFill, Indicate, config, Brace, Circumscribe,
)
from manim_voiceover import VoiceoverScene
from manim_voiceover.tracker import AUDIO_OFFSET_RESOLUTION

from speech_service import get_speech_service
from sound_effects import load_all as load_sfx
from story_common import play_challenge_countdown

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


def rt(seconds: float, floor: float = MIN_RT) -> float:
    return max(floor, float(seconds))


BOARD_LEFT = -4.6
BOARD_RIGHT = 5.6
BOARD_TOP = 3.3
BOARD_BOTTOM = -2.9
BOARD_CX = (BOARD_LEFT + BOARD_RIGHT) / 2
BOARD_CY = (BOARD_TOP + BOARD_BOTTOM) / 2


def board_text(s: str, size: int = 34, color: str = CHALK_WHITE, weight: str = "NORMAL") -> Text:
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def chalk_math(s: str, size: int = 34, color: str = MATH_COLOR) -> MathTex:
    return MathTex(s, font_size=size, color=color)


def drop_shadow(mobj, dx: float = 0.05, dy: float = -0.06, opacity: float = 0.3):
    shadow = mobj.copy()
    shadow.set_fill(BLACK, opacity=opacity)
    shadow.set_stroke(width=0)
    shadow.shift(np.array([dx, dy, 0]))
    return VGroup(shadow, mobj)


class NestedNumberSystemsStory(VoiceoverScene):
    """8-beat Manim lesson on N subset W subset Z subset Q."""

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

        # Both corner badges share the same chalk-stamped ribbon style and
        # are rendered at font_size=12 then scaled up -- manim/Pango
        # introduces visible per-glyph spacing artifacts in this font at
        # small integer font sizes above 12, but scaling the finished
        # badge (before the margin snap in _corner_badge) is artifact-free.
        # The same scale factor keeps "Mathematics" and "dhimantAI" the
        # same visual size (matches the rest of the Story-Mode series).
        # This replaces the old topic-label "Nested Sets" left badge with
        # the dhimantAI brand badge used across the rest of the series.
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
            # compensate for the background art's perspective -- at equal
            # 0.08 margins the right badge renders with a visibly larger
            # gap to the board frame than the left badge, so it's nudged
            # right to match dhimantAI's spacing (same fix as the rest of
            # the Story-Mode series).
            badge.shift(RIGHT * (BOARD_RIGHT - 0.013 - badge.get_right()[0]))
        # Snap the TOP edge to the same 0.08 margin used horizontally, so
        # both badges sit with equal spacing from the board's edges
        # regardless of font scaling.
        badge.shift(UP * ((BOARD_TOP - 0.08) - badge.get_top()[1]))
        return badge

    def reset_board(self) -> None:
        self.clear()
        self.add(self.bg, self.student, self.teacher, self.badge, self.badge_l)

    def construct(self):
        self.sfx = load_sfx()
        self.set_speech_service(get_speech_service(), create_subcaption=False)

        self.add_background()

        self.beat0_title()
        self.beat2_natural()
        self.beat3_whole()
        self.beat4_integers()
        self.beat5_rational()
        self.beat6_nested()
        self.beat7_challenge()
        self.beat8_summary()

        self._write_real_srt()

    # ================================================================ beats ==

    def beat0_title(self):
        """Title card -- a small nesting-circles teaser plays during the
        opening line instead of leaving the board blank, then the title
        text lands. (The teaser also previews beat6's concentric-circle
        diagram, so the opening seconds aren't just dead air.)"""
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            teaser_pos = np.array([BOARD_CX, BOARD_CY + 0.9, 0])
            tiny = Circle(radius=0.35, color=CHALK_PINK, stroke_width=2.5).move_to(teaser_pos)
            bigger = Circle(radius=0.75, color=CHALK_AMBER, stroke_width=2.5).move_to(teaser_pos)
            biggest = Circle(radius=1.15, color=CHALK_CYAN, stroke_width=2.5).move_to(teaser_pos)
            # "Numbers grow, one system inside another." -- three rings
            # nest outward in time with the sentence.
            self.play(Create(tiny), run_time=rt(tracker.time_until_bookmark("b0") * 0.35))
            self.play(Create(bigger), run_time=rt(tracker.time_until_bookmark("b0") * 0.35))
            self.play(Create(biggest), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))
            self.add_sound(self.sfx["swipe"], gain=-16)

            title = board_text("Nested Number Systems", size=38, weight="BOLD").move_to(teaser_pos)
            self.play(FadeOut(VGroup(tiny, bigger, biggest)), Write(title),
                     run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            subtitle = board_text("From Natural Numbers to Rational Numbers", size=22,
                                  color=CHALK_CYAN).move_to(np.array([BOARD_CX, BOARD_CY + 0.3, 0]))
            self.play(Write(subtitle), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            chain = chalk_math(r"\mathbb{N} \rightarrow \mathbb{W} \rightarrow \mathbb{Z} \rightarrow \mathbb{Q}",
                               size=40, color=CHALK_YELLOW).move_to(np.array([BOARD_CX, BOARD_CY - 0.6, 0]))
            self.play(Write(chain), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            question = board_text("How does one number system grow into another?", size=20,
                                  color=CHALK_PINK).move_to(np.array([BOARD_CX, BOARD_CY - 1.5, 0]))
            self.play(FadeIn(question), run_time=rt(tracker.time_until_bookmark("b4")))
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat2_natural(self):
        """Beat: start with natural numbers 1,2,3,4,5,... inside a labeled
        container; a lone 0 appears outside, unanswered."""
        with self.voiceover(text=NARRATION["natural"]) as tracker:
            self.reset_board()

            self.heading = board_text("Start With Natural Numbers", size=26, weight="BOLD",
                                      color=CHALK_PINK).move_to(np.array([BOARD_CX, BOARD_TOP - 0.55, 0]))
            self.play(Write(self.heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            self.box = RoundedRectangle(width=8.8, height=2.0, corner_radius=0.15,
                                        stroke_color=CHALK_PINK, stroke_width=2.5,
                                        fill_color="#1E1A2A", fill_opacity=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.6, 0]))
            self.label = chalk_math(r"\mathbb{N}", size=40, color=CHALK_PINK).next_to(
                self.box, LEFT, buff=0.3)
            self.play(Create(self.box), Write(self.label), run_time=rt(MIN_RT))

            chips = [chalk_math(n, size=32, color=CHALK_WHITE) for n in ["1", "2", "3", "4", "5"]]
            chips.append(board_text("...", size=28, color=CHALK_WHITE))
            self.row = VGroup(*chips).arrange(RIGHT, buff=0.5).move_to(self.box.get_center())
            self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in self.row], lag_ratio=0.15),
                     run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-14)

            self.formula = chalk_math(r"\mathbb{N}=\{1,2,3,\ldots\}", size=24, color=CHALK_PINK).move_to(
                np.array([BOARD_CX, BOARD_CY - 1.1, 0]))
            self.play(Write(self.formula), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.zero_outside = chalk_math("0", size=40, color=CHALK_YELLOW).move_to(
                np.array([BOARD_CX, BOARD_CY - 1.9, 0]))
            self.zero_q = board_text("But where does 0 belong?", size=20, color=CHALK_CYAN).next_to(
                self.zero_outside, DOWN, buff=0.25)
            self.play(FadeIn(self.zero_outside, scale=0.5), FadeIn(self.zero_q),
                     run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["pop"], gain=-14)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat3_whole(self):
        """Beat: 0 joins the set -- N subset W."""
        with self.voiceover(text=NARRATION["whole"]) as tracker:
            new_heading = board_text("Whole Numbers = Natural + 0", size=24, weight="BOLD",
                                     color=CHALK_AMBER).move_to(self.heading.get_center())
            self.play(FadeOut(self.zero_q), ReplacementTransform(self.heading, new_heading),
                     run_time=rt(tracker.time_until_bookmark("b0")))
            self.heading = new_heading
            self.add_sound(self.sfx["whoosh"], gain=-15)

            self.play(FadeOut(self.zero_outside), run_time=rt(MIN_RT))

            new_chips = [chalk_math(n, size=32, color=CHALK_WHITE) for n in ["0", "1", "2", "3", "4", "5"]]
            new_chips.append(board_text("...", size=28, color=CHALK_WHITE))
            new_row = VGroup(*new_chips).arrange(RIGHT, buff=0.5).move_to(self.box.get_center())
            self.play(ReplacementTransform(self.row, new_row), self.box.animate.set_stroke(color=CHALK_AMBER),
                     run_time=rt(tracker.time_until_bookmark("b1")))
            self.row = new_row
            self.add_sound(self.sfx["pop"], gain=-14)

            new_label = chalk_math(r"\mathbb{W}", size=40, color=CHALK_AMBER).move_to(self.label.get_center())
            new_formula = chalk_math(r"\mathbb{W}=\{0,1,2,3,\ldots\}", size=24, color=CHALK_AMBER).move_to(
                self.formula.get_center())
            self.play(ReplacementTransform(self.label, new_label),
                     ReplacementTransform(self.formula, new_formula),
                     run_time=rt(tracker.time_until_bookmark("b2")))
            self.label = new_label
            self.formula = new_formula
            self.add_sound(self.sfx["ding"], gain=-13)

            self.subset_prev = chalk_math(r"\mathbb{N}\subset\mathbb{W}", size=26, color=CHALK_GREEN).move_to(
                np.array([BOARD_CX, BOARD_CY - 1.6, 0]))
            self.play(Write(self.subset_prev), Indicate(self.subset_prev, color=CHALK_GREEN),
                     run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)

            self.negs_outside = chalk_math(r"\ldots,-3,-2,-1", size=28, color=CHALK_RED).move_to(
                np.array([BOARD_CX, BOARD_CY - 2.1, 0]))
            self.play(FadeIn(self.negs_outside, shift=RIGHT * 0.2), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["pop"], gain=-14)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat4_integers(self):
        """Beat: negative numbers join -- W subset Z."""
        with self.voiceover(text=NARRATION["integers"]) as tracker:
            new_heading = board_text("Whole Numbers Expand to Integers", size=22, weight="BOLD",
                                     color=CHALK_CYAN).move_to(self.heading.get_center())
            self.play(FadeOut(self.subset_prev), ReplacementTransform(self.heading, new_heading),
                     run_time=rt(tracker.time_until_bookmark("b0")))
            self.heading = new_heading
            self.add_sound(self.sfx["whoosh"], gain=-15)

            self.play(FadeOut(self.negs_outside), run_time=rt(MIN_RT))

            new_vals = ["...", "-3", "-2", "-1", "0", "1", "2", "3", "4", "5", "..."]
            new_chips = [board_text(v, 24, CHALK_WHITE) if v == "..." else chalk_math(v, size=26, color=CHALK_WHITE)
                        for v in new_vals]
            new_row = VGroup(*new_chips).arrange(RIGHT, buff=0.24).move_to(self.box.get_center())
            self.play(ReplacementTransform(self.row, new_row), self.box.animate.set_stroke(color=CHALK_CYAN),
                     run_time=rt(tracker.time_until_bookmark("b1")))
            self.row = new_row
            self.add_sound(self.sfx["pop"], gain=-14)

            new_label = chalk_math(r"\mathbb{Z}", size=40, color=CHALK_CYAN).move_to(self.label.get_center())
            new_formula = board_text("...,-3,-2,-1,0,1,2,3,...", size=18, color=CHALK_CYAN).move_to(
                self.formula.get_center())
            self.play(ReplacementTransform(self.label, new_label),
                     ReplacementTransform(self.formula, new_formula),
                     run_time=rt(tracker.time_until_bookmark("b2")))
            self.label = new_label
            self.formula = new_formula
            self.add_sound(self.sfx["ding"], gain=-13)

            self.subset_prev = chalk_math(r"\mathbb{W}\subset\mathbb{Z}", size=26, color=CHALK_GREEN).move_to(
                np.array([BOARD_CX, BOARD_CY - 1.6, 0]))
            self.play(Write(self.subset_prev), Indicate(self.subset_prev, color=CHALK_GREEN),
                     run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)

            self.fracs_outside = chalk_math(r"\frac12,\ -\frac34,\ \frac53", size=28, color=CHALK_PINK).move_to(
                np.array([BOARD_CX, BOARD_CY - 2.1, 0]))
            self.play(FadeIn(self.fracs_outside, shift=RIGHT * 0.2), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["pop"], gain=-14)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat5_rational(self):
        """Beat: integers expand to rationals -- 5=5/1 etc.; fractions fill
        the gaps between integers; Z subset Q."""
        with self.voiceover(text=NARRATION["rational"]) as tracker:
            self.play(FadeOut(VGroup(self.heading, self.box, self.row, self.label, self.formula,
                                      self.subset_prev, self.fracs_outside)),
                     run_time=rt(tracker.time_until_bookmark("b0") * 0.4))

            heading = board_text("Integers Expand to Rational Numbers", size=22, weight="BOLD",
                                 color=CHALK_GREEN).move_to(np.array([BOARD_CX, BOARD_TOP - 0.55, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            row1 = VGroup(chalk_math("5", size=38, color=CHALK_WHITE),
                         chalk_math(r"=\frac51", size=38, color=CHALK_YELLOW)).arrange(RIGHT, buff=0.3)
            row2 = VGroup(chalk_math("-3", size=38, color=CHALK_WHITE),
                         chalk_math(r"=\frac{-3}{1}", size=38, color=CHALK_YELLOW)).arrange(RIGHT, buff=0.3)
            row3 = VGroup(chalk_math("0", size=38, color=CHALK_WHITE),
                         chalk_math(r"=\frac01", size=38, color=CHALK_YELLOW)).arrange(RIGHT, buff=0.3)
            examples = VGroup(row1, row2, row3).arrange(RIGHT, buff=0.9).move_to(
                np.array([BOARD_CX, BOARD_CY + 1.1, 0]))
            self.play(Write(row1), run_time=rt(tracker.time_until_bookmark("b1") * 0.4))
            self.play(Write(row2), run_time=rt(tracker.time_until_bookmark("b1") * 0.7))
            self.play(Write(row3), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            nl_y = BOARD_CY - 0.7
            nl_left = np.array([BOARD_CX - 4.0, nl_y, 0])
            nl_right = np.array([BOARD_CX + 4.0, nl_y, 0])
            nl_body = Line(nl_left, nl_right, stroke_color=CHALK_WHITE, stroke_width=3)
            # Small arrows extending OUTWARD past each endpoint (rather
            # than a flat stop) since a real number line continues
            # infinitely in both directions.
            nl_right_tip = Arrow(nl_right, nl_right + RIGHT * 0.22, color=CHALK_WHITE,
                                  stroke_width=3, buff=0, tip_length=0.16,
                                  max_tip_length_to_length_ratio=1.0)
            nl_left_tip = Arrow(nl_left, nl_left + LEFT * 0.22, color=CHALK_WHITE,
                                 stroke_width=3, buff=0, tip_length=0.16,
                                 max_tip_length_to_length_ratio=1.0)
            nl_line = VGroup(nl_body, nl_left_tip, nl_right_tip)

            def nl_x(v: float) -> float:
                return BOARD_CX + v * 4.0

            ticks = VGroup(*[Line(np.array([nl_x(v), nl_y - 0.12, 0]), np.array([nl_x(v), nl_y + 0.12, 0]),
                                  stroke_color=CHALK_WHITE, stroke_width=2.5) for v in (-1, 0, 1)])
            tick_lbls = VGroup(*[board_text(s, 22, CHALK_WHITE).move_to(
                np.array([nl_x(v), nl_y - 0.4, 0])) for v, s in ((-1, "-1"), (0, "0"), (1, "1"))])
            frac_dot1 = Dot(np.array([nl_x(0.5), nl_y, 0]), radius=0.09, color=CHALK_PINK)
            frac_lbl1 = chalk_math(r"\frac12", size=24, color=CHALK_PINK).next_to(frac_dot1, UP, buff=0.2)
            frac_dot2 = Dot(np.array([nl_x(-0.75), nl_y, 0]), radius=0.09, color=CHALK_CYAN)
            frac_lbl2 = chalk_math(r"-\frac34", size=24, color=CHALK_CYAN).next_to(frac_dot2, UP, buff=0.2)
            self.play(Create(nl_line), Create(ticks), FadeIn(tick_lbls),
                     run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            self.play(FadeIn(frac_dot1, scale=0.5), Write(frac_lbl1),
                     FadeIn(frac_dot2, scale=0.5), Write(frac_lbl2),
                     run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["pop"], gain=-14)

            caption = board_text("Rational Numbers include integers AND fractions.", size=18,
                                 color=CHALK_WHITE).move_to(np.array([BOARD_CX, BOARD_CY - 1.6, 0]))
            self.play(FadeIn(caption), run_time=rt(tracker.time_until_bookmark("b3")))

            subset3 = chalk_math(r"\mathbb{Z}\subset\mathbb{Q}", size=28, color=CHALK_GREEN).move_to(
                np.array([BOARD_CX, BOARD_CY - 2.15, 0]))
            self.play(Write(subset3), Indicate(subset3, color=CHALK_GREEN),
                     run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)

            self.rational_group = VGroup(heading, examples, nl_line, ticks, tick_lbls, frac_dot1, frac_lbl1,
                                         frac_dot2, frac_lbl2, caption, subset3)
            self._capture_srt(tracker)

        self.play(FadeOut(self.rational_group))

    def beat6_nested(self):
        """Beat: the concentric-circle picture -- N subset W subset Z subset Q."""
        with self.voiceover(text=NARRATION["nested"]) as tracker:
            self.reset_board()

            heading = board_text("Why Are They Nested?", size=28, weight="BOLD",
                                 color=CHALK_AMBER).move_to(np.array([BOARD_CX, BOARD_TOP - 0.55, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            center = np.array([BOARD_CX, BOARD_CY, 0])
            n_circle = Circle(radius=0.55, color=CHALK_PINK, stroke_width=2.5).move_to(center)
            w_circle = Circle(radius=1.05, color=CHALK_AMBER, stroke_width=2.5).move_to(center)
            z_circle = Circle(radius=1.55, color=CHALK_CYAN, stroke_width=2.5).move_to(center)
            q_circle = Circle(radius=2.1, color=CHALK_WHITE, stroke_width=2.5).move_to(center)

            n_lbl = chalk_math(r"\mathbb{N}", size=22, color=CHALK_PINK).move_to(center)
            w_lbl = chalk_math(r"\mathbb{W}", size=22, color=CHALK_AMBER).move_to(center + UP * 0.8)
            z_lbl = chalk_math(r"\mathbb{Z}", size=22, color=CHALK_CYAN).move_to(center + UP * 1.3)
            q_lbl = chalk_math(r"\mathbb{Q}", size=22, color=CHALK_WHITE).move_to(center + UP * 1.85)

            self.play(Create(n_circle), Write(n_lbl), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-14)
            self.play(Create(w_circle), Write(w_lbl), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["pop"], gain=-14)
            self.play(Create(z_circle), Write(z_lbl), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["pop"], gain=-14)
            self.play(Create(q_circle), Write(q_lbl), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["pop"], gain=-14)

            relation = chalk_math(r"\mathbb{N}\subset\mathbb{W}\subset\mathbb{Z}\subset\mathbb{Q}", size=26,
                                  color=CHALK_GREEN).move_to(np.array([BOARD_CX, BOARD_BOTTOM + 0.8, 0]))
            callout = board_text("Every smaller system fits inside the next.", size=18,
                                 color=CHALK_WHITE).move_to(np.array([BOARD_CX, BOARD_BOTTOM + 0.35, 0]))
            self.play(Write(relation), FadeIn(callout), Indicate(relation, color=CHALK_GREEN),
                     run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["success"], gain=-11)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat7_challenge(self):
        """YOUR TURN -- classify 3, 0, and -1/2 across N/W/Z/Q. Follows the
        series pattern: full-space bordered box, round THINK badge at
        board centre, whole-board dim while it counts down."""
        box_y = BOARD_CY - 0.3
        with self.voiceover(text=NARRATION["challenge_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", size=32, weight="BOLD",
                                 color=CHALK_PINK).move_to(np.array([BOARD_CX, BOARD_TOP - 0.55, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            # Sized to snugly fit the widest row (number + value + reveal
            # answer) instead of a wide box with a huge empty gap between
            # the left-anchored number and the board-centre value/question.
            box = RoundedRectangle(width=5.6, height=4.4, corner_radius=0.16,
                                   stroke_color=CHALK_CYAN, stroke_width=2,
                                   fill_color="#1E2A1E", fill_opacity=0.3).move_to(
                np.array([BOARD_CX, box_y, 0]))
            num_x = box.get_left()[0] + 0.4
            row_gap = 1.25

            n1 = board_text("1.", size=22, weight="BOLD", color=CHALK_AMBER).move_to(
                np.array([num_x, box_y + row_gap, 0]))
            t1 = chalk_math("3", size=42, color=CHALK_WHITE).next_to(n1, RIGHT, buff=0.35)
            q1 = board_text("Which sets contain it?", size=17, color=CHALK_CYAN).next_to(
                t1, RIGHT, buff=0.35)
            self.play(Create(box), FadeIn(n1), Write(t1), FadeIn(q1),
                     run_time=rt(tracker.time_until_bookmark("b1")))

            n2 = board_text("2.", size=22, weight="BOLD", color=CHALK_AMBER).move_to(
                np.array([num_x, box_y, 0]))
            t2 = chalk_math("0", size=42, color=CHALK_WHITE).next_to(n2, RIGHT, buff=0.35)
            q2 = board_text("Which sets contain it?", size=17, color=CHALK_CYAN).next_to(
                t2, RIGHT, buff=0.35)
            self.play(FadeIn(n2), Write(t2), FadeIn(q2), run_time=rt(tracker.time_until_bookmark("b2")))

            n3 = board_text("3.", size=22, weight="BOLD", color=CHALK_AMBER).move_to(
                np.array([num_x, box_y - row_gap, 0]))
            t3 = chalk_math(r"-\frac12", size=38, color=CHALK_WHITE).next_to(n3, RIGHT, buff=0.35)
            q3 = board_text("Which sets contain it?", size=17, color=CHALK_CYAN).next_to(
                t3, RIGHT, buff=0.35)
            self.play(FadeIn(n3), Write(t3), FadeIn(q3), run_time=rt(tracker.time_until_bookmark("b3")))

            pause_lbl = board_text("Pause and try it!", size=20, color=CHALK_PINK).move_to(
                np.array([BOARD_CX, box_y - 1.95, 0]))
            self.play(FadeIn(pause_lbl), run_time=rt(tracker.time_until_bookmark("b4")))

            self._capture_srt(tracker)

        # Consistent 10-second challenge clock (whole series): a round
        # THINK badge at board centre dims the WHOLE board (question box
        # included) except itself while students think.
        play_challenge_countdown(self, seconds=10, sfx=self.sfx)

        with self.voiceover(text=NARRATION["challenge_reveal"]) as tracker:
            self.play(FadeOut(pause_lbl), FadeOut(q1), FadeOut(q2), FadeOut(q3),
                     run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            a1 = board_text("N, W, Z, Q -- all four!", size=17, weight="BOLD",
                            color=CHALK_GREEN).next_to(t1, RIGHT, buff=0.35)
            self.play(Write(a1), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["success"], gain=-11)

            a2 = board_text("W, Z, Q -- not N", size=17, weight="BOLD",
                            color=CHALK_AMBER).next_to(t2, RIGHT, buff=0.35)
            self.play(Write(a2), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            a3 = board_text("Q only", size=17, weight="BOLD",
                            color=CHALK_PINK).next_to(t3, RIGHT, buff=0.35)
            self.play(Write(a3), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            self.challenge_group = VGroup(heading, box, n1, t1, n2, t2, n3, t3, a1, a2, a3)
            self._capture_srt(tracker)

        self.play(FadeOut(self.challenge_group))

    def bullet_row(self, n: int, lines: list[str], *, color: str = CHALK_CYAN) -> VGroup:
        badge = Circle(radius=0.19, stroke_color=color, stroke_width=2,
                        fill_color=color, fill_opacity=0.18)
        num = board_text(str(n), 18, color, "BOLD").move_to(badge.get_center())
        text_block = VGroup(*[board_text(t, 22, CHALK_WHITE) for t in lines]).arrange(
            DOWN, buff=0.06, aligned_edge=LEFT)
        row = VGroup(VGroup(badge, num), text_block).arrange(RIGHT, buff=0.3)
        VGroup(badge, num).move_to(np.array([row[0].get_x(), text_block.get_y(), 0]))
        return row

    def beat8_summary(self) -> None:
        with self.voiceover(text=NARRATION["summary"]) as tracker:
            self.reset_board()

            heading = board_text("Summary", 34, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.4, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            # A horizontal flow (mirroring the title card's N->W->Z->Q
            # chain) instead of 7 lines of text stacked tightly on top of
            # each other -- that vertical stack read as a congested wall
            # of text using almost none of the board's width.
            labels = ["NATURAL", "WHOLE", "INTEGER", "RATIONAL"]
            colors = [CHALK_PINK, CHALK_AMBER, CHALK_CYAN, CHALK_GREEN]
            additions = ["+ 0", "+ negatives", "+ fractions"]

            words = VGroup(*[board_text(lbl, 22, c, "BOLD") for lbl, c in zip(labels, colors)])
            words.arrange(RIGHT, buff=1.15).move_to(np.array([BOARD_CX, BOARD_CY + 0.8, 0]))

            arrows = VGroup(*[
                Arrow(words[i].get_right(), words[i + 1].get_left(), buff=0.12,
                      stroke_width=2.5, color=CHALK_WHITE)
                for i in range(3)
            ])
            add_labels = VGroup(*[
                board_text(additions[i], 16, CHALK_WHITE).next_to(arrows[i], DOWN, buff=0.15)
                for i in range(3)
            ])

            self.play(FadeIn(words[0]), run_time=rt(tracker.time_until_bookmark("b2") * 0.3))
            self.play(
                LaggedStart(*[
                    AnimationGroup(GrowArrow(arrows[i]), FadeIn(words[i + 1]), FadeIn(add_labels[i]))
                    for i in range(3)
                ], lag_ratio=0.35),
                run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            relation = chalk_math(r"\mathbb{N}\subset\mathbb{W}\subset\mathbb{Z}\subset\mathbb{Q}", size=30,
                                  color=CHALK_YELLOW).move_to(np.array([BOARD_CX, BOARD_CY - 0.9, 0]))
            self.play(Write(relation), Indicate(relation, color=CHALK_YELLOW),
                     run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)

            summary_group = VGroup(heading, words, arrows, add_labels, relation)
            self.play(FadeOut(summary_group), run_time=rt(tracker.get_remaining_duration() * 0.25))

            thanks = board_text("Thank You for Watching!", 42, CHALK_WHITE, "BOLD")
            thanks2 = board_text("See you in the next lesson :)", 26, CHALK_CYAN)
            thanks_group = VGroup(thanks, thanks2).arrange(DOWN, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY, 0]))
            self.play(Write(thanks), run_time=rt(tracker.get_remaining_duration() * 0.6))
            self.add_sound(self.sfx["ding"], gain=-11)
            self.play(FadeIn(thanks2, shift=UP * 0.1), run_time=rt(tracker.get_remaining_duration()))
            self.play(Circumscribe(thanks_group, color=CHALK_AMBER, stroke_width=3,
                                    time_width=0.6), run_time=0.6)
            self.add_sound(self.sfx["success"], gain=-11)

            self._capture_srt(tracker)

        self.wait(END_HOLD)

    # ============================================================= helpers ==

    def _capture_srt(self, tracker, words_per_line: int = 9) -> None:
        wbs = [
            wb for wb in tracker.data.get("word_boundaries", [])
            if wb.get("text", "").strip()
        ]
        if not wbs:
            return
        starts = [tracker.start_t + wb["audio_offset"] / AUDIO_OFFSET_RESOLUTION for wb in wbs]
        for i in range(0, len(wbs), words_per_line):
            chunk = wbs[i:i + words_per_line]
            chunk_starts = starts[i:i + words_per_line]
            end = starts[i + words_per_line] if i + words_per_line < len(starts) else tracker.end_t
            text = " ".join(wb["text"] for wb in chunk)
            self._srt_entries.append((chunk_starts[0], end, text))

    def _write_real_srt(self) -> None:
        out_dir = _HERE / "media" / "videos" / "nested_number_systems_story"
        out_dir.mkdir(parents=True, exist_ok=True)
        srt_path = out_dir / f"{self.__class__.__name__}.real.srt"

        def fmt(t: float) -> str:
            # round to whole milliseconds FIRST, then split: rounding the
            # fraction on its own can give ms = 1000, which writes a
            # four-digit millisecond field -- invalid SRT that strict
            # parsers drop.  See fix_srt_timestamps.py.
            total = int(round(max(float(t), 0.0) * 1000))
            h = total // 3_600_000
            m = (total // 60_000) % 60
            s = (total // 1000) % 60
            ms = total % 1000
            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
        lines = []
        for idx, (start, end, text) in enumerate(self._srt_entries, 1):
            lines.append(str(idx))
            lines.append(f"{fmt(start)} --> {fmt(max(end, start + 0.3))}")
            lines.append(text)
            lines.append("")
        srt_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"[real SRT written] {srt_path}")


# ------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "Numbers grow, one system inside another.<bookmark mark='b0'/> "
        "Nested Number Systems.<bookmark mark='b1'/> From Natural Numbers "
        "to Rational Numbers.<bookmark mark='b2'/> Natural, Whole, "
        "Integer, Rational.<bookmark mark='b3'/> How does one number "
        "system grow into another?<bookmark mark='b4'/>"
    ),
    "natural": (
        "Let's start with the simplest numbers — the natural numbers."
        "<bookmark mark='b0'/> One, two, three, four, five, and on it "
        "goes.<bookmark mark='b1'/> These make up the set of Natural "
        "Numbers.<bookmark mark='b2'/> But where does zero belong?"
        "<bookmark mark='b3'/>"
    ),
    "whole": (
        "All natural numbers are whole numbers — but whole numbers add "
        "one more.<bookmark mark='b0'/> Watch zero join the family."
        "<bookmark mark='b1'/> Now we have zero, one, two, three, and on."
        "<bookmark mark='b2'/> Natural numbers are completely inside "
        "whole numbers.<bookmark mark='b3'/> But numbers below zero are "
        "still missing.<bookmark mark='b4'/>"
    ),
    "integers": (
        "Whole numbers grow again — this time into negative territory."
        "<bookmark mark='b0'/> Watch the negative numbers join: minus "
        "three, minus two, minus one.<bookmark mark='b1'/> Integers add "
        "the negative numbers.<bookmark mark='b2'/> Whole numbers are "
        "completely inside integers.<bookmark mark='b3'/> But fractions "
        "are still missing.<bookmark mark='b4'/>"
    ),
    "rational": (
        "Now integers expand into rational numbers.<bookmark mark='b0'/> "
        "Watch: five becomes five over one, minus three becomes minus "
        "three over one, and zero becomes zero over one.<bookmark "
        "mark='b1'/> Rational numbers also fill in fractions between the "
        "integers — like one half, and minus three quarters.<bookmark "
        "mark='b2'/> Rational Numbers include integers AND fractions."
        "<bookmark mark='b3'/> Integers are completely inside the "
        "rational numbers.<bookmark mark='b4'/>"
    ),
    "nested": (
        "Let's see the whole picture together.<bookmark mark='b0'/> "
        "Natural numbers form the smallest circle.<bookmark mark='b1'/> "
        "Whole numbers wrap around them.<bookmark mark='b2'/> Integers "
        "wrap around whole numbers.<bookmark mark='b3'/> And rational "
        "numbers contain them all.<bookmark mark='b4'/> Every smaller "
        "system fits perfectly inside the next.<bookmark mark='b5'/>"
    ),
    "challenge_setup": (
        "Now it's your turn — where does each number belong?"
        "<bookmark mark='b0'/> Number one: three.<bookmark mark='b1'/> "
        "Number two: zero.<bookmark mark='b2'/> Number three: minus one "
        "half.<bookmark mark='b3'/> Pause and figure out which sets "
        "contain each one!<bookmark mark='b4'/>"
    ),
    "challenge_reveal": (
        "Three is natural, so it's whole, integer, and rational too."
        "<bookmark mark='b0'/> Zero is not natural, but it is whole, "
        "integer, and rational.<bookmark mark='b1'/> Minus one half is "
        "only rational — not whole or integer.<bookmark mark='b2'/>"
    ),
    "summary": (
        "Let's lock in the big picture.<bookmark mark='b1'/> Watch the "
        "whole chain build.<bookmark mark='b2'/> Natural is a subset of "
        "Whole, is a subset of Integer, is a subset of Rational."
        "<bookmark mark='b3'/> Thank you so much for watching, and I "
        "will see you in the next lesson!"
    ),
}


if __name__ == "__main__":
    pass

"""
Commutative Property: The "Swap Test"
Story-mode chalkboard lesson (Classes 6-12 Maths, Chapter 1 -- Rational
Numbers).

Production pipeline (mirrors the rest of the Story-Mode series):
  - assets/background2.png chalkboard backdrop.
  - VoiceoverScene + EdgeSpeechService (en-IN-PrabhatNeural).
  - Real per-word sync via <bookmark> tags + tracker timing.
  - Ground-truth SRT from edge-tts word boundaries.

Topic: swapping the order of two operands in addition or multiplication
never changes the result (commutative), but swapping in subtraction or
division does (NOT commutative). All four operations are tested -- an
earlier cut only covered +/-, which left the wrong impression that
addition was "the" commutative operation. One consistent "swap test"
mechanism, with numbers PHYSICALLY moving positions (not instantly
replaced) for every swap. Title + 9 beats + closing summary:
  0. Title card.
  1. The swap idea -- two number cards swap places.
  2. Formal definition: a*b -> b*a.
  3. Addition test: 2+3 vs 3+2.
  4. Rational-number addition: -5/2+3/4 vs 3/4+(-5/2).
  5. Subtraction test: 5-2 vs 2-5.
  6. Rational-number subtraction: 2/3-7/8 vs 7/8-2/3.
  7. Multiplication (3x4 vs 4x3, commutative) & division (10/2 vs
     2/10, NOT commutative).
  8. Challenge: 3/5+2/7 vs 2/7+3/5 (with a real pause).
  9. Recap: all four operations, side by side.
  10. Summary -- bullet recap + Thank You card.
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
    Rectangle, RoundedRectangle, Arrow, CurvedArrow, Text, Write, FadeIn, FadeOut,
    Create, Transform, ReplacementTransform, GrowFromCenter, GrowArrow,
    LaggedStart, DrawBorderThenFill, Indicate, config, Brace, Circumscribe,
    SurroundingRectangle,
)
from manim_voiceover import VoiceoverScene
from manim_voiceover.tracker import AUDIO_OFFSET_RESOLUTION

from speech_service import get_speech_service
from sound_effects import load_all as load_sfx
from story_common import play_challenge_countdown

# --------------------------------------------------------------- theme -----
CHALK_WHITE = "#F5F2E9"
CHALK_YELLOW = "#FFE066"
CHALK_PINK = "#FF8FA3"
CHALK_CYAN = "#7FE7DC"
CHALK_AMBER = "#E8B769"
CHALK_GREEN = "#9BE38A"
CHALK_RED = "#FF6B6B"
CHALK_BLUE = "#4ECDC4"
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


class CommutativePropertyStory(VoiceoverScene):
    """9-beat Manim lesson on the commutative property and the swap test."""

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
        self.badge = self._corner_badge("Mathematics", corner="right",
                                         y=BOARD_TOP - 0.16, font_size=12)
        self.badge_l = self._corner_badge("Commutative Property", corner="left",
                                           y=BOARD_TOP - 0.16, font_size=12)

        self.add(self.bg, self.student, self.teacher, self.badge, self.badge_l)

    def _corner_badge(self, text: str, *, corner: str, y: float | None = None,
                       font_size: int = 13) -> VGroup:
        label = board_text(text, font_size, CHALK_WHITE, "BOLD")
        frame = RoundedRectangle(
            corner_radius=0.04, width=label.width + 0.24, height=label.height + 0.16,
            stroke_color=CHALK_AMBER, stroke_width=1.5,
            fill_color="#2A1D10", fill_opacity=0.45,
        )
        label.move_to(frame.get_center())
        badge = VGroup(frame, label)

        yy = BOARD_TOP - 0.32 if y is None else y
        if corner == "left":
            badge.move_to(np.array([BOARD_LEFT + 0.55, yy, 0]))
            badge.shift(LEFT * (badge.get_left()[0] - (BOARD_LEFT + 0.08)))
        else:
            badge.move_to(np.array([BOARD_RIGHT - 0.6, yy, 0]))
            badge.shift(RIGHT * (BOARD_RIGHT - 0.08 - badge.get_right()[0]))
        return badge

    def reset_board(self) -> None:
        self.clear()
        self.add(self.bg, self.student, self.teacher, self.badge, self.badge_l)

    def construct(self):
        self.sfx = load_sfx()
        self.set_speech_service(get_speech_service(), create_subcaption=False)

        self.add_background()

        self.beat0_title()
        self.beat1_swap_idea()
        self.beat2_definition()
        self.beat3_addition_test()
        self.beat4_rational_addition()
        self.beat5_subtraction_test()
        self.beat6_rational_subtraction()
        self.beat7_mult_div()
        self.beat8_challenge()
        self.beat9_recap()
        self.beat10_summary()

        self._write_real_srt()

    # ================================================================ beats ==

    def _swap(self, left, right, run_time: float):
        """Physically swap two mobjects' positions -- movement itself is
        the mental model for commutativity, not an instant replace."""
        lp, rp = left.get_center().copy(), right.get_center().copy()
        self.play(left.animate.move_to(rp), right.animate.move_to(lp),
                 run_time=run_time)

    def beat0_title(self):
        """Title card -- two dots swap places inside a small frame,
        teasing the "does order matter" question, before the title text."""
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            frame = RoundedRectangle(width=2.2, height=1.0, corner_radius=0.1,
                                      stroke_color=CHALK_CYAN, stroke_width=2.5,
                                      fill_color="#1E2A1A", fill_opacity=0.3).move_to(
                np.array([BOARD_CX, BOARD_TOP - 1.3, 0]))
            dot_a = Dot(frame.get_center() + LEFT * 0.6, radius=0.09, color=CHALK_GREEN)
            dot_b = Dot(frame.get_center() + RIGHT * 0.6, radius=0.09, color=CHALK_PINK)
            self.play(Create(frame), FadeIn(dot_a), FadeIn(dot_b),
                     run_time=rt(tracker.time_until_bookmark("b0") * 0.4))
            self._swap(dot_a, dot_b, rt(tracker.time_until_bookmark("b0") * 0.35))
            self.add_sound(self.sfx["pop"], gain=-15)
            self.play(FadeOut(frame), FadeOut(dot_a), FadeOut(dot_b),
                     run_time=rt(tracker.time_until_bookmark("b0")))

            title = board_text("Commutative Property", size=38, weight="BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 0.4, 0]))
            self.play(Write(title), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            subtitle = board_text("The Swap Test", size=30, color=CHALK_PINK).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.4, 0]))
            self.play(Write(subtitle), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat1_swap_idea(self):
        """Beat 1: Two number cards, 2 and 3, physically swap places."""
        with self.voiceover(text=NARRATION["beat1"]) as tracker:
            self.reset_board()

            heading = board_text("The Swap Test", size=28, weight="BOLD",
                                 color=CHALK_AMBER).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.6, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.4))

            card2 = chalk_math("2", size=56, color=CHALK_GREEN).move_to(
                np.array([BOARD_CX - 1.6, BOARD_CY + 0.5, 0]))
            card3 = chalk_math("3", size=56, color=CHALK_PINK).move_to(
                np.array([BOARD_CX + 1.6, BOARD_CY + 0.5, 0]))
            self.play(FadeIn(card2), FadeIn(card3),
                     run_time=rt(tracker.time_until_bookmark("b0")))

            swap_arrow = CurvedArrow(card2.get_top() + UP * 0.1, card3.get_top() + UP * 0.1,
                                     color=CHALK_CYAN, stroke_width=3)
            swap_lbl = board_text("SWAP", size=20, color=CHALK_CYAN, weight="BOLD").next_to(
                swap_arrow, UP, buff=0.1)
            self.play(Create(swap_arrow), FadeIn(swap_lbl),
                     run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["swipe"], gain=-14)

            self._swap(card2, card3, rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            question = board_text("Does the answer change when we swap?", size=22,
                                  color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.6, 0]))
            self.play(FadeOut(swap_arrow), FadeOut(swap_lbl), Write(question),
                     run_time=rt(tracker.time_until_bookmark("b3")))

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat2_definition(self):
        """Beat 2: Formal definition -- a*b -> b*a."""
        with self.voiceover(text=NARRATION["beat2"]) as tracker:
            self.reset_board()

            heading = board_text("Commutative Property", size=26, weight="BOLD",
                                 color=CHALK_AMBER).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.6, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))

            a1 = chalk_math("a", size=52, color=CHALK_GREEN).move_to(
                np.array([BOARD_CX - 1.6, BOARD_CY + 0.7, 0]))
            star1 = chalk_math(r"\star", size=44, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.7, 0]))
            b1 = chalk_math("b", size=52, color=CHALK_PINK).move_to(
                np.array([BOARD_CX + 1.6, BOARD_CY + 0.7, 0]))
            self.play(FadeIn(a1), FadeIn(star1), FadeIn(b1),
                     run_time=rt(tracker.time_until_bookmark("b1")))

            self._swap(a1, b1, rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["swipe"], gain=-14)

            equation = chalk_math(r"a\star b=b\star a", size=40, color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.7, 0]))
            self.play(Write(equation), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)

            caption = board_text("Order can change — result does not", size=22,
                                 weight="BOLD", color=CHALK_AMBER).next_to(
                equation, DOWN, buff=0.4)
            self.play(FadeIn(caption), Circumscribe(equation, color=CHALK_AMBER),
                     run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat3_addition_test(self):
        """Beat 3: 2+3 vs 3+2 -- addition passes the swap test."""
        with self.voiceover(text=NARRATION["beat3"]) as tracker:
            self.reset_board()

            heading = board_text("Addition", size=26, weight="BOLD", color=CHALK_GREEN).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.6, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            # eq+result are pre-arranged as one centered pair BEFORE
            # either is revealed, so the whole "expression = answer" sits
            # centered on the board instead of the expression alone being
            # centered and the answer trailing off to one side.
            eq1 = chalk_math("2+3", size=48, color=CHALK_WHITE)
            result1 = chalk_math("=5", size=48, color=CHALK_YELLOW)
            VGroup(eq1, result1).arrange(RIGHT, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.9, 0]))
            self.play(Write(eq1), run_time=rt(tracker.time_until_bookmark("b0")))
            self.play(Write(result1), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            eq2 = chalk_math("3+2", size=48, color=CHALK_CYAN)
            result2 = chalk_math("=5", size=48, color=CHALK_YELLOW)
            VGroup(eq2, result2).arrange(RIGHT, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.4, 0]))
            self.play(Write(eq2), run_time=rt(tracker.time_until_bookmark("b2") * 0.6))
            self.play(Write(result2), run_time=rt(tracker.time_until_bookmark("b2")))

            same_box = SurroundingRectangle(VGroup(result1, result2), color=CHALK_GREEN,
                                             buff=0.15, corner_radius=0.1)
            self.play(Create(same_box), Indicate(VGroup(result1, result2), color=CHALK_GREEN,
                                                  scale_factor=1.1),
                     run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)

            tag = board_text("Same answer — Addition is commutative!", size=20,
                             weight="BOLD", color=CHALK_GREEN).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.5, 0]))
            self.play(FadeIn(tag), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat4_rational_addition(self):
        """Beat 4: -5/2 + 3/4 vs 3/4 + (-5/2) -- rational addition."""
        with self.voiceover(text=NARRATION["beat4"]) as tracker:
            self.reset_board()

            heading = board_text("Rational Numbers", size=24, weight="BOLD",
                                 color=CHALK_GREEN).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.6, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))

            eq1 = chalk_math(r"-\frac52+\frac34", size=40, color=CHALK_WHITE)
            result1 = chalk_math(r"=-\frac74", size=40, color=CHALK_YELLOW)
            VGroup(eq1, result1).arrange(RIGHT, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.9, 0]))
            self.play(Write(eq1), run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.play(Write(result1), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            eq2 = chalk_math(r"\frac34+\left(-\frac52\right)", size=40, color=CHALK_CYAN)
            result2 = chalk_math(r"=-\frac74", size=40, color=CHALK_YELLOW)
            VGroup(eq2, result2).arrange(RIGHT, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.5, 0]))
            self.play(Write(eq2), run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            self.play(Write(result2), run_time=rt(tracker.time_until_bookmark("b2")))

            same_box = SurroundingRectangle(VGroup(result1, result2), color=CHALK_GREEN,
                                             buff=0.15, corner_radius=0.1)
            self.play(Create(same_box), Indicate(VGroup(result1, result2), color=CHALK_GREEN,
                                                  scale_factor=1.08),
                     run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)

            tag = board_text("Swap -> Same Result:  a + b = b + a", size=20,
                             weight="BOLD", color=CHALK_AMBER).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.5, 0]))
            self.play(FadeIn(tag), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat5_subtraction_test(self):
        """Beat 5: 5-2 vs 2-5 -- subtraction fails the swap test."""
        with self.voiceover(text=NARRATION["beat5"]) as tracker:
            self.reset_board()

            heading = board_text("Subtraction", size=26, weight="BOLD",
                                 color=CHALK_RED).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.6, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            eq1 = chalk_math("5-2", size=48, color=CHALK_WHITE)
            result1 = chalk_math("=3", size=48, color=CHALK_GREEN)
            VGroup(eq1, result1).arrange(RIGHT, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.9, 0]))
            self.play(Write(eq1), run_time=rt(tracker.time_until_bookmark("b0")))
            self.play(Write(result1), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            eq2 = chalk_math("2-5", size=48, color=CHALK_CYAN)
            result2 = chalk_math("=-3", size=48, color=CHALK_RED)
            VGroup(eq2, result2).arrange(RIGHT, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.4, 0]))
            self.play(Write(eq2), run_time=rt(tracker.time_until_bookmark("b2") * 0.6))
            self.play(Write(result2), run_time=rt(tracker.time_until_bookmark("b2")))

            neq = chalk_math(r"3\neq-3", size=32, color=CHALK_RED).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 1.1, 0]))
            self.play(FadeIn(neq), Indicate(VGroup(result1, result2), color=CHALK_RED,
                                             scale_factor=1.1),
                     run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            tag = board_text("Different answer — NOT commutative!", size=20,
                             weight="BOLD", color=CHALK_RED).next_to(neq, DOWN, buff=0.25)
            self.play(FadeIn(tag), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["click"], gain=-15)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat6_rational_subtraction(self):
        """Beat 6: 2/3-7/8 vs 7/8-2/3 -- rational subtraction fails too."""
        with self.voiceover(text=NARRATION["beat6"]) as tracker:
            self.reset_board()

            heading = board_text("Rational Numbers", size=24, weight="BOLD",
                                 color=CHALK_RED).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.6, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))

            eq1 = chalk_math(r"\frac23-\frac78", size=40, color=CHALK_WHITE)
            result1 = chalk_math(r"=-\frac{5}{24}", size=40, color=CHALK_GREEN)
            VGroup(eq1, result1).arrange(RIGHT, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.9, 0]))
            self.play(Write(eq1), run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.play(Write(result1), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            eq2 = chalk_math(r"\frac78-\frac23", size=40, color=CHALK_CYAN)
            result2 = chalk_math(r"=\frac{5}{24}", size=40, color=CHALK_RED)
            VGroup(eq2, result2).arrange(RIGHT, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.5, 0]))
            self.play(Write(eq2), run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            self.play(Write(result2), run_time=rt(tracker.time_until_bookmark("b2")))

            tag = board_text("Different results — subtraction is NOT commutative!",
                             size=18, weight="BOLD", color=CHALK_RED).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.6, 0]))
            self.play(FadeIn(tag), Indicate(VGroup(result1, result2), color=CHALK_RED,
                                             scale_factor=1.08),
                     run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat7_mult_div(self):
        """Beat 7: multiplication passes the swap test too (3x4 vs 4x3);
        division does not (10/2 vs 2/10) -- closes the gap where only
        addition/subtraction were tested."""
        with self.voiceover(text=NARRATION["beat_mult_div"]) as tracker:
            self.reset_board()

            heading = board_text("Multiplication & Division", size=24, weight="BOLD",
                                 color=CHALK_GREEN).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.6, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))

            eq1 = chalk_math(r"3\times4", size=44, color=CHALK_WHITE)
            result1 = chalk_math("=12", size=44, color=CHALK_YELLOW)
            VGroup(eq1, result1).arrange(RIGHT, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY + 1.2, 0]))
            self.play(Write(eq1), run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.play(Write(result1), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            eq2 = chalk_math(r"4\times3", size=44, color=CHALK_CYAN)
            result2 = chalk_math("=12", size=44, color=CHALK_YELLOW)
            VGroup(eq2, result2).arrange(RIGHT, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.3, 0]))
            self.play(Write(eq2), run_time=rt(tracker.time_until_bookmark("b2") * 0.6))
            self.play(Write(result2), run_time=rt(tracker.time_until_bookmark("b2")))

            same_box = SurroundingRectangle(VGroup(result1, result2), color=CHALK_GREEN,
                                             buff=0.15, corner_radius=0.1)
            self.play(Create(same_box), Indicate(VGroup(result1, result2), color=CHALK_GREEN,
                                                  scale_factor=1.08),
                     run_time=rt(MIN_RT))

            tag = board_text("Multiplication is commutative too!", size=20, weight="BOLD",
                             color=CHALK_GREEN).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.6, 0]))
            self.play(FadeIn(tag), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)

            div_q = board_text("What about division?", size=20, color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_CY - 1.3, 0]))
            self.play(FadeIn(div_q), run_time=rt(tracker.time_until_bookmark("b4")))

            division_eq = chalk_math(r"10\div2=5,\quad 2\div10=\frac15", size=26,
                                     color=CHALK_RED).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 1.0, 0]))
            division_tag = board_text("Division is NOT commutative!", size=18, weight="BOLD",
                                      color=CHALK_RED).next_to(division_eq, DOWN, buff=0.25)
            self.play(FadeOut(div_q), Write(division_eq), FadeIn(division_tag),
                     run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["click"], gain=-15)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat8_challenge(self):
        """Beat 8: YOUR TURN -- 3/5+2/7 vs 2/7+3/5, with a real pause."""
        with self.voiceover(text=NARRATION["beat8_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", size=32, weight="BOLD",
                                 color=CHALK_PINK).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.6, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            # testA/resultA (and testB/resultB) are pre-arranged as one
            # centered pair now, even though the result stays unrevealed
            # (never added to the scene) until the reveal half below --
            # so the finished "expression = answer" row is centered on
            # the board, not just the expression alone.
            testA = chalk_math(r"\frac35+\frac27", size=40, color=CHALK_WHITE)
            resultA = chalk_math(r"=\frac{31}{35}", size=36, color=CHALK_GREEN)
            VGroup(testA, resultA).arrange(RIGHT, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.9, 0]))

            testB = chalk_math(r"\frac27+\frac35", size=40, color=CHALK_WHITE)
            resultB = chalk_math(r"=\frac{31}{35}", size=36, color=CHALK_GREEN)
            VGroup(testB, resultB).arrange(RIGHT, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.1, 0]))

            self.play(FadeIn(testA), FadeIn(testB),
                     run_time=rt(tracker.time_until_bookmark("b1")))

            pause_lbl = board_text("Same result or different? Think first!", size=20,
                                   color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.6, 0]))
            self.play(FadeIn(pause_lbl), run_time=rt(tracker.time_until_bookmark("b2")))

            self._capture_srt(tracker)

        # Consistent 10-second challenge clock (whole series): the
        # background dims while the countdown runs, question stays bright.
        play_challenge_countdown(self, seconds=10, sfx=self.sfx)

        with self.voiceover(text=NARRATION["beat8_reveal"]) as tracker:
            self.play(FadeOut(pause_lbl), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            self.play(Write(resultA), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(Write(resultB), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["success"], gain=-11)

            final = board_text("Same result — Addition passes again!", size=22,
                               weight="BOLD", color=CHALK_GREEN).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.5, 0]))
            self.play(FadeIn(final), Indicate(VGroup(resultA, resultB), color=CHALK_GREEN,
                                               scale_factor=1.08),
                     run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat9_recap(self):
        """Beat 9: Split-screen recap -- ALL FOUR operations, not just
        addition/subtraction, so the video doesn't leave the impression
        that addition is "the" commutative operation."""
        with self.voiceover(text=NARRATION["beat9"]) as tracker:
            self.reset_board()

            heading = board_text("The Swap Test", size=26, weight="BOLD",
                                 color=CHALK_AMBER).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.5, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))

            divider = Line(np.array([BOARD_CX, BOARD_TOP - 0.9, 0]),
                          np.array([BOARD_CX, BOARD_BOTTOM + 0.9, 0]),
                          stroke_color=CHALK_WHITE, stroke_width=1.5)
            self.play(Create(divider), run_time=rt(MIN_RT))

            commute_col = VGroup(
                board_text("COMMUTATIVE", size=20, weight="BOLD", color=CHALK_GREEN),
                chalk_math("a + b = b + a", size=26, color=CHALK_WHITE),
                chalk_math(r"a \times b = b \times a", size=26, color=CHALK_WHITE),
                board_text("(OK) Addition, Multiplication", size=15, weight="BOLD",
                          color=CHALK_GREEN),
            ).arrange(DOWN, buff=0.22).move_to(
                np.array([BOARD_CX - 2.4, BOARD_CY + 0.1, 0]))
            self.play(FadeIn(commute_col, shift=LEFT * 0.15),
                     run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            not_col = VGroup(
                board_text("NOT COMMUTATIVE", size=20, weight="BOLD", color=CHALK_RED),
                chalk_math(r"a - b \neq b - a", size=26, color=CHALK_WHITE),
                chalk_math(r"a \div b \neq b \div a", size=26, color=CHALK_WHITE),
                board_text("(X) Subtraction, Division", size=15, weight="BOLD",
                          color=CHALK_RED),
            ).arrange(DOWN, buff=0.22).move_to(
                np.array([BOARD_CX + 2.4, BOARD_CY + 0.1, 0]))
            self.play(FadeIn(not_col, shift=RIGHT * 0.15),
                     run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            takeaway = board_text("Swap the numbers -> check the result!", size=20,
                                  weight="BOLD", color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.5, 0]))
            self.play(FadeIn(takeaway), Circumscribe(VGroup(commute_col, not_col),
                                                       color=CHALK_AMBER, stroke_width=2),
                     run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def bullet_row(self, n: int, lines: list[str], *, color: str = CHALK_CYAN) -> VGroup:
        """A numbered recap line -- matches the closing-summary layout
        used across the whole Story-Mode series."""
        badge = Circle(radius=0.19, stroke_color=color, stroke_width=2,
                        fill_color=color, fill_opacity=0.18)
        num = board_text(str(n), 18, color, "BOLD").move_to(badge.get_center())
        text_block = VGroup(*[board_text(t, 22, CHALK_WHITE) for t in lines]).arrange(
            DOWN, buff=0.06, aligned_edge=LEFT)
        row = VGroup(VGroup(badge, num), text_block).arrange(RIGHT, buff=0.3)
        VGroup(badge, num).move_to(np.array([row[0].get_x(), text_block.get_y(), 0]))
        return row

    def beat10_summary(self) -> None:
        """Closing screen -- same "Thank You for Watching!" template used
        across the whole Story-Mode series. Bullets now cover all four
        operations (not just addition/subtraction)."""
        with self.voiceover(text=NARRATION["summary"]) as tracker:
            self.reset_board()

            heading = board_text("Summary", 34, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.4, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            bullets = VGroup(
                self.bullet_row(1, ["Addition & multiplication: a+b=b+a,",
                                     "a×b=b×a — commutative."], color=CHALK_GREEN),
                self.bullet_row(2, ["Subtraction & division: a-b ≠ b-a,",
                                     "a÷b ≠ b÷a — NOT commutative."], color=CHALK_RED),
                self.bullet_row(3, ["Swap the two numbers, then check",
                                     "if the result stays the same."], color=CHALK_CYAN),
            )
            bullets.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
            bullets.move_to(np.array([BOARD_CX, BOARD_CY + 0.15, 0]))

            self.play(FadeIn(bullets[0], shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(bullets[1], shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(bullets[2], shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            summary_group = VGroup(heading, bullets)
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
        out_dir = _HERE / "media" / "videos" / "commutative_property_story"
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
        "Does the order of numbers really matter?<bookmark mark='b0'/> "
        "Let's find out with the Commutative Property<bookmark mark='b1'/> "
        "and the Swap Test!<bookmark mark='b2'/>"
    ),
    "beat1": (
        "Here are two numbers: two and three.<bookmark mark='b0'/> Now, "
        "let's swap them.<bookmark mark='b1'/> Two and three become three "
        "and two.<bookmark mark='b2'/> Does the answer change when we "
        "swap the order?<bookmark mark='b3'/>"
    ),
    "beat2": (
        "This is called the Commutative Property.<bookmark mark='b0'/> "
        "Start with a star b.<bookmark mark='b1'/> Now swap the operands: "
        "b star a.<bookmark mark='b2'/> If the operation is commutative, "
        "both sides are equal.<bookmark mark='b3'/> Order can change — "
        "the result does not.<bookmark mark='b4'/>"
    ),
    "beat3": (
        "Let's test addition.<bookmark mark='b0'/> Two plus three equals "
        "five.<bookmark mark='b1'/> Now swap: three plus two.<bookmark mark='b2'/> "
        "That also equals five!<bookmark mark='b3'/> Same answer — "
        "addition passes the swap test.<bookmark mark='b4'/>"
    ),
    "beat4": (
        "Does this work for rational numbers too?<bookmark mark='b0'/> "
        "Minus five-halves plus three-fourths equals minus seven-fourths."
        "<bookmark mark='b1'/> Now swap: three-fourths plus negative "
        "five-halves.<bookmark mark='b2'/> That also equals minus "
        "seven-fourths!<bookmark mark='b3'/> Swap, same result — addition "
        "is commutative for rational numbers.<bookmark mark='b4'/>"
    ),
    "beat5": (
        "Now let's try subtraction.<bookmark mark='b0'/> Five minus two "
        "equals three.<bookmark mark='b1'/> Swap it: two minus five."
        "<bookmark mark='b2'/> That equals minus three!<bookmark mark='b3'/> "
        "Three is not equal to minus three — subtraction fails the swap "
        "test.<bookmark mark='b4'/>"
    ),
    "beat6": (
        "Let's confirm this with rational numbers.<bookmark mark='b0'/> "
        "Two-thirds minus seven-eighths equals minus five twenty-fourths."
        "<bookmark mark='b1'/> Now swap: seven-eighths minus two-thirds."
        "<bookmark mark='b2'/> That equals plus five twenty-fourths this "
        "time!<bookmark mark='b3'/>"
    ),
    "beat_mult_div": (
        "Does multiplication pass the swap test?<bookmark mark='b0'/> "
        "Three times four equals twelve.<bookmark mark='b1'/> Swap it: "
        "four times three also equals twelve!<bookmark mark='b2'/> "
        "Multiplication is commutative too.<bookmark mark='b3'/> What "
        "about division?<bookmark mark='b4'/> Ten divided by two is "
        "five, but two divided by ten is one-fifth — division is NOT "
        "commutative.<bookmark mark='b5'/>"
    ),
    "beat8_setup": (
        "Now it's your turn.<bookmark mark='b0'/> Three-fifths plus "
        "two-sevenths — does swapping give the same result?"
        "<bookmark mark='b1'/> Think about it before we reveal the "
        "answer.<bookmark mark='b2'/>"
    ),
    "beat8_reveal": (
        "Three-fifths plus two-sevenths equals thirty-one over "
        "thirty-five.<bookmark mark='b0'/> And two-sevenths plus "
        "three-fifths also equals thirty-one over thirty-five!"
        "<bookmark mark='b1'/> Same result — addition passes again!"
        "<bookmark mark='b2'/>"
    ),
    "beat9": (
        "Let's put all four operations side by side.<bookmark mark='b0'/> "
        "Addition and multiplication pass the swap test — they're "
        "commutative!<bookmark mark='b1'/> Subtraction and division "
        "fail — they're not commutative!<bookmark mark='b2'/> Swap the "
        "numbers, then check the result.<bookmark mark='b3'/>"
    ),
    "summary": (
        "Let's lock in what we learned today.<bookmark mark='b1'/> "
        "Addition and multiplication always give the same result when "
        "swapped — both are commutative.<bookmark mark='b2'/> But "
        "swapping in subtraction or division changes the answer — "
        "neither is commutative.<bookmark mark='b3'/> Just remember: "
        "swap the numbers, then check if the result stays the same."
        "<bookmark mark='b4'/> Thank you so much for watching, and I "
        "will see you in the next lesson!"
    ),
}


if __name__ == "__main__":
    pass

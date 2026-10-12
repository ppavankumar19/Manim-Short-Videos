"""
Decimal Forms -- From Fractions to Terminating & Recurring Decimals
Story-mode chalkboard lesson (Classes 6-12 Maths, Chapter 1 -- Rational
Numbers).

Production pipeline (mirrors the rest of the Story-Mode series):
  - assets/background2.png chalkboard backdrop, student + teacher cutouts,
    corner badges.
  - VoiceoverScene + EdgeSpeechService (en-IN-PrabhatNeural) -- NOTE: this
    project's .env may route TTS through Gemini instead (GOOGLE_TTS_VOICE
    contains "zephyr"); Gemini has been observed to fail on narration that
    reads like an enumerated list ("Number one: ... Number two: ...") by
    generating text instead of audio, so narration below is written as
    natural continuous prose and avoids that pattern.
  - Real per-word sync via <bookmark> tags + tracker timing.
  - Ground-truth SRT from edge-tts word boundaries.
  - Shared story_common.play_challenge_countdown() for the "YOUR TURN"
    round THINK badge (board-centre, dims the whole board except itself).

Topic: p/q = p div q; the decimal terminates when the remainder hits 0,
and recurs when a remainder repeats (forcing the same digits to repeat).
Production rule: animate the division progressively -- digit by digit,
with the remainder shown at each step -- never reveal the final decimal
all at once.

Title + 7 beats + closing summary:
  0. Title card -- 5/8, 3/7 preview, p/q -> ?
  1. A Fraction Is a Division -- p/q = p div q.
  2. Terminating Decimal -- 5 div 8 = 0.625, remainders 2,4,0, STOP.
  3. Recurring Decimal -- 3 div 7 = 0.428571 repeating, remainder cycle
     back to 3, LOOP.
  4. Why Do Digits Repeat? -- remainder cycle diagram.
  5. Side-by-Side Comparison -- STOP vs LOOP.
  6. Challenge -- predict 3/4 (terminating) and 2/7 (recurring).
  7. Summary -- Divide -> watch the remainder -> STOP or LOOP.
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
    LaggedStart, DrawBorderThenFill, Indicate, config, Brace, Circumscribe,
    CurvedArrow,
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


class DecimalFormsStory(VoiceoverScene):
    """8-beat Manim lesson on terminating and recurring decimal forms of
    rational numbers."""

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
        self.badge_l = self._corner_badge("Decimal Forms", corner="left",
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
        self.beat1_fraction_is_division()
        self.beat2_terminating()
        self.beat3_recurring()
        self.beat4_why_repeat()
        self.beat5_comparison()
        self.beat6_challenge()
        self.beat7_summary()

        self._write_real_srt()

    # ================================================================ beats ==

    def beat0_title(self):
        """Title card -- 5/8 and 3/7 preview, p/q -> ? question."""
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()
            self.wait(rt(tracker.time_until_bookmark("b0")))

            title = board_text("Decimal Forms", size=40, weight="BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 1.1, 0]))
            self.play(Write(title), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            fracs = chalk_math(r"\frac58 \qquad \frac37", size=44, color=CHALK_YELLOW).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.2, 0]))
            self.play(Write(fracs), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["pop"], gain=-14)

            arrow_eq = chalk_math(r"\frac pq \ \longrightarrow\ ?", size=36, color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.8, 0]))
            self.play(Write(arrow_eq), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            question = board_text("What decimal does a fraction become?", size=20,
                                  color=CHALK_PINK).move_to(np.array([BOARD_CX, BOARD_CY - 1.7, 0]))
            self.play(FadeIn(question), run_time=rt(tracker.time_until_bookmark("b4")))

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat1_fraction_is_division(self):
        """Beat: p/q = p div q, worked with 5/8 -> 5 div 8."""
        with self.voiceover(text=NARRATION["fraction_division"]) as tracker:
            self.reset_board()

            heading = board_text("A Fraction Is a Division", size=28, weight="BOLD",
                                 color=CHALK_CYAN).move_to(np.array([BOARD_CX, BOARD_TOP - 0.55, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            formula = chalk_math(r"\frac pq = p\div q", size=40, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_CY + 1.0, 0]))
            self.play(Write(formula), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            ex = chalk_math(r"\frac58", size=44, color=CHALK_YELLOW)
            arrow = chalk_math(r"\longrightarrow", size=36, color=CHALK_WHITE)
            ex2 = chalk_math(r"5\div8", size=44, color=CHALK_GREEN)
            row = VGroup(ex, arrow, ex2).arrange(RIGHT, buff=0.4).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.2, 0]))
            self.play(Write(ex), run_time=rt(tracker.time_until_bookmark("b2") * 0.4))
            self.play(Write(arrow), Write(ex2), Indicate(ex2, color=CHALK_GREEN),
                     run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            note = board_text("Divide numerator by denominator.", size=20, color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_CY - 1.5, 0]))
            self.play(FadeIn(note), run_time=rt(tracker.time_until_bookmark("b3")))

            cond = chalk_math(r"q\ne0", size=22, color=CHALK_RED).next_to(note, DOWN, buff=0.3)
            self.play(FadeIn(cond), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["click"], gain=-15)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat2_terminating(self):
        """Beat: 5 div 8 = 0.625, progressive digits + remainders, STOP."""
        with self.voiceover(text=NARRATION["terminating"]) as tracker:
            self.reset_board()

            heading = board_text("Terminating Decimal: The Division Ends", size=22, weight="BOLD",
                                 color=CHALK_GREEN).move_to(np.array([BOARD_CX, BOARD_TOP - 0.55, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            expr = chalk_math(r"5\div8", size=40, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_CY + 1.2, 0]))
            self.play(Write(expr), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            digits = chalk_math("0.6", size=40, color=CHALK_YELLOW).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.3, 0]))
            rem = board_text("remainder: 2", size=18, color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.35, 0]))
            self.play(Write(digits), FadeIn(rem), run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            self.add_sound(self.sfx["click"], gain=-15)

            digits2 = chalk_math("0.62", size=40, color=CHALK_YELLOW).move_to(digits.get_center())
            rem2 = board_text("remainder: 4", size=18, color=CHALK_CYAN).move_to(rem.get_center())
            self.play(ReplacementTransform(digits, digits2), ReplacementTransform(rem, rem2),
                     run_time=rt(tracker.time_until_bookmark("b2") * 0.8))
            self.add_sound(self.sfx["click"], gain=-15)

            digits3 = chalk_math("0.625", size=40, color=CHALK_GREEN).move_to(digits2.get_center())
            rem3 = board_text("remainder: 0", size=18, weight="BOLD", color=CHALK_GREEN).move_to(rem2.get_center())
            self.play(ReplacementTransform(digits2, digits3), ReplacementTransform(rem2, rem3),
                     Indicate(digits3, color=CHALK_GREEN, scale_factor=1.15),
                     run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            stop = board_text("Remainder = 0  ->  the decimal STOPS.", size=19, weight="BOLD",
                              color=CHALK_GREEN).move_to(np.array([BOARD_CX, BOARD_CY - 1.2, 0]))
            self.play(FadeIn(stop), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            final = chalk_math(r"\frac58=0.625 \quad \text{(Terminating)}", size=24,
                               color=CHALK_WHITE).move_to(np.array([BOARD_CX, BOARD_CY - 2.0, 0]))
            self.play(Write(final), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat3_recurring(self):
        """Beat: 3 div 7 = 0.428571 repeating, progressive digits + LOOP."""
        with self.voiceover(text=NARRATION["recurring"]) as tracker:
            self.reset_board()

            heading = board_text("Recurring Decimal: The Division Loops", size=22, weight="BOLD",
                                 color=CHALK_PINK).move_to(np.array([BOARD_CX, BOARD_TOP - 0.55, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            expr = chalk_math(r"3\div7", size=38, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_CY + 1.35, 0]))
            self.play(Write(expr), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            stages = ["0.4", "0.42", "0.428", "0.4285", "0.42857", "0.428571"]
            rems = [2, 6, 4, 5, 1, 3]
            digits = chalk_math(stages[0], size=34, color=CHALK_YELLOW).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.55, 0]))
            rem = board_text(f"remainder: {rems[0]}", size=17, color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.05, 0]))
            self.play(Write(digits), FadeIn(rem), run_time=rt(tracker.time_until_bookmark("b2") * 0.3))
            self.add_sound(self.sfx["click"], gain=-15)

            per_step = rt(tracker.time_until_bookmark("b2") * 1.0 / len(stages))
            for stage, r in zip(stages[1:], rems[1:]):
                new_digits = chalk_math(stage, size=34, color=CHALK_YELLOW).move_to(digits.get_center())
                new_rem = board_text(f"remainder: {r}", size=17, color=CHALK_CYAN).move_to(rem.get_center())
                self.play(ReplacementTransform(digits, new_digits), ReplacementTransform(rem, new_rem),
                         run_time=rt(per_step))
                self.add_sound(self.sfx["click"], gain=-15)
                digits, rem = new_digits, new_rem

            back = board_text("Remainder 3 is back where we started!", size=18, weight="BOLD",
                              color=CHALK_PINK).move_to(np.array([BOARD_CX, BOARD_CY - 0.75, 0]))
            self.play(FadeIn(back), Indicate(rem, color=CHALK_PINK, scale_factor=1.2),
                     run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            final = chalk_math(r"\frac37=0.\overline{428571}", size=30, color=CHALK_PINK).move_to(
                np.array([BOARD_CX, BOARD_CY - 1.6, 0]))
            self.play(FadeOut(back), Write(final), Indicate(final, color=CHALK_PINK, scale_factor=1.1),
                     run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)

            loop = board_text("The digits repeat forever -- Recurring Decimal.", size=17, weight="BOLD",
                              color=CHALK_PINK).move_to(np.array([BOARD_CX, BOARD_CY - 2.15, 0]))
            self.play(FadeIn(loop), run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat4_why_repeat(self):
        """Beat: remainder cycle diagram -- why digits repeat."""
        with self.voiceover(text=NARRATION["why_repeat"]) as tracker:
            self.reset_board()

            heading = board_text("The Secret Is the Remainder", size=26, weight="BOLD",
                                 color=CHALK_AMBER).move_to(np.array([BOARD_CX, BOARD_TOP - 0.55, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            vals = [3, 2, 6, 4, 5, 1]
            xs = np.linspace(BOARD_CX - 3.6, BOARD_CX + 3.6, len(vals))
            y = BOARD_CY + 0.7
            nodes = VGroup(*[
                VGroup(
                    Circle(radius=0.32, stroke_color=CHALK_CYAN, stroke_width=2,
                           fill_color="#1E2A2A", fill_opacity=0.4),
                    board_text(str(v), size=20, weight="BOLD", color=CHALK_CYAN),
                ) for v in vals
            ])
            for node, x in zip(nodes, xs):
                node.move_to(np.array([x, y, 0]))
                node[1].move_to(node[0].get_center())

            arrows = VGroup(*[
                Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), buff=0.05,
                     stroke_width=2.5, color=CHALK_WHITE) for i in range(len(vals) - 1)
            ])
            self.play(LaggedStart(*[FadeIn(n, scale=0.6) for n in nodes], lag_ratio=0.15),
                     run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-14)
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15),
                     run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            # A gentle arc OVER the top of the row (not a deep dip below
            # it) -- the natural way to draw a "wraps back around" return
            # path in a cycle diagram. Bulging upward means the arc sits
            # entirely above every node's height, so only the two end
            # circles it actually touches need checking (verified
            # numerically), and it stays clear of the heading above.
            loop_arrow = CurvedArrow(nodes[-1].get_top() + UP * 0.2, nodes[0].get_top() + UP * 0.2,
                                     color=CHALK_PINK, stroke_width=2.5, angle=PI * 0.3)
            self.play(Create(loop_arrow), Indicate(nodes[0], color=CHALK_PINK, scale_factor=1.3),
                     run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)

            note = board_text("Same remainder -> same division steps -> repeating digits.", size=17,
                              weight="BOLD", color=CHALK_AMBER).move_to(np.array([BOARD_CX, BOARD_CY - 1.0, 0]))
            self.play(FadeIn(note), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            contrast = chalk_math(r"\text{Terminating: remainder}\to0 \qquad "
                                  r"\text{Recurring: a remainder repeats}", size=17,
                                  color=CHALK_WHITE).move_to(np.array([BOARD_CX, BOARD_CY - 1.9, 0]))
            self.play(FadeIn(contrast), run_time=rt(tracker.time_until_bookmark("b5")))

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat5_comparison(self):
        """Beat: side-by-side terminating vs recurring."""
        with self.voiceover(text=NARRATION["comparison"]) as tracker:
            self.reset_board()

            heading = board_text("Terminating vs Recurring", size=28, weight="BOLD",
                                 color=CHALK_WHITE).move_to(np.array([BOARD_CX, BOARD_TOP - 0.55, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            left = VGroup(
                chalk_math(r"\frac58=0.625", size=26, color=CHALK_GREEN),
                board_text("remainder -> 0", size=18, color=CHALK_GREEN),
                board_text("STOPS", size=24, weight="BOLD", color=CHALK_GREEN),
            ).arrange(DOWN, buff=0.3).move_to(np.array([BOARD_CX - 2.3, BOARD_CY + 0.2, 0]))
            self.play(Write(left[0]), run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.play(FadeIn(left[1]), FadeIn(left[2]), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["success"], gain=-11)

            right = VGroup(
                chalk_math(r"\frac37=0.\overline{428571}", size=26, color=CHALK_PINK),
                board_text("a remainder repeats", size=18, color=CHALK_PINK),
                board_text("LOOPS", size=24, weight="BOLD", color=CHALK_PINK),
            ).arrange(DOWN, buff=0.3).move_to(np.array([BOARD_CX + 2.3, BOARD_CY + 0.2, 0]))
            self.play(Write(right[0]), run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            self.play(FadeIn(right[1]), FadeIn(right[2]), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            divider = Line(np.array([BOARD_CX, BOARD_CY + 1.3, 0]), np.array([BOARD_CX, BOARD_CY - 1.1, 0]),
                          stroke_color=CHALK_AMBER, stroke_width=2)
            self.play(Create(divider), run_time=rt(MIN_RT))

            cue = board_text("STOP -> Terminating.   LOOP -> Recurring.", size=19, weight="BOLD",
                             color=CHALK_YELLOW).move_to(np.array([BOARD_CX, BOARD_CY - 1.9, 0]))
            self.play(FadeIn(cue), Circumscribe(cue, color=CHALK_YELLOW, stroke_width=2),
                     run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat6_challenge(self):
        """YOUR TURN -- predict 3/4 (terminating) and 2/7 (recurring).
        Follows the series pattern: full-space bordered box, round THINK
        badge at board centre, whole-board dim while it counts down."""
        box_y = BOARD_CY - 0.3
        with self.voiceover(text=NARRATION["challenge_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN: Predict the Type", size=28, weight="BOLD",
                                 color=CHALK_PINK).move_to(np.array([BOARD_CX, BOARD_TOP - 0.55, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            # Sized to fit the reveal answer tags (the widest content)
            # snugly. The number now sits right next to its fraction
            # (which stays centred, so the tag below it stays symmetric)
            # instead of stranded at the box's left edge with a big empty
            # gap before the board-centre fraction.
            box = RoundedRectangle(width=5.2, height=4.6, corner_radius=0.16,
                                   stroke_color=CHALK_CYAN, stroke_width=2,
                                   fill_color="#1E2A1E", fill_opacity=0.3).move_to(
                np.array([BOARD_CX, box_y, 0]))

            t1 = chalk_math(r"\frac34", size=48, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, box_y + 1.3, 0]))
            n1 = board_text("1.", size=24, weight="BOLD", color=CHALK_AMBER).next_to(
                t1, LEFT, buff=0.4)
            self.play(Create(box), FadeIn(n1), Write(t1), run_time=rt(tracker.time_until_bookmark("b1")))

            t2 = chalk_math(r"\frac27", size=48, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, box_y - 0.6, 0]))
            n2 = board_text("2.", size=24, weight="BOLD", color=CHALK_AMBER).next_to(
                t2, LEFT, buff=0.4)
            self.play(FadeIn(n2), Write(t2), run_time=rt(tracker.time_until_bookmark("b2")))

            rule = board_text("Watch the remainder!", size=20, weight="BOLD", color=CHALK_YELLOW).move_to(
                np.array([BOARD_CX, box_y - 1.75, 0]))
            self.play(FadeIn(rule), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["pop"], gain=-14)

            self._capture_srt(tracker)

        # Consistent 10-second challenge clock (whole series): a round
        # THINK badge at board centre dims the WHOLE board (question box
        # included) except itself while students think.
        play_challenge_countdown(self, seconds=10, sfx=self.sfx)

        with self.voiceover(text=NARRATION["challenge_reveal"]) as tracker:
            self.play(FadeOut(rule), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            a1 = board_text("0.75  ->  Terminating!", size=19, weight="BOLD",
                            color=CHALK_GREEN).next_to(t1, DOWN, buff=0.35)
            self.play(Write(a1), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["success"], gain=-11)

            a2 = board_text("0.285714...  ->  Recurring!", size=19, weight="BOLD",
                            color=CHALK_PINK).next_to(t2, DOWN, buff=0.35)
            self.play(Write(a2), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["success"], gain=-11)

            self.challenge_group = VGroup(heading, box, n1, t1, n2, t2, a1, a2)
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

    def beat7_summary(self) -> None:
        with self.voiceover(text=NARRATION["summary"]) as tracker:
            self.reset_board()

            heading = board_text("Summary", 34, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.4, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            bullets = VGroup(
                self.bullet_row(1, ["Every fraction p/q becomes a decimal", "by dividing p by q."],
                                 color=CHALK_CYAN),
                self.bullet_row(2, ["Remainder reaches 0 -> Terminating.",
                                     "Example: 5/8 = 0.625"], color=CHALK_GREEN),
                self.bullet_row(3, ["A remainder repeats -> Recurring.",
                                     "Example: 3/7 = 0.428571..."], color=CHALK_PINK),
            )
            bullets.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
            bullets.move_to(np.array([BOARD_CX, BOARD_CY + 0.2, 0]))

            self.play(FadeIn(bullets[0], shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.4))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(bullets[1], shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(bullets[2], shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            cue = board_text("Divide -> Watch the remainder -> STOP or LOOP.", size=17,
                             weight="BOLD", color=CHALK_YELLOW).next_to(bullets, DOWN, buff=0.4)
            self.play(FadeIn(cue, shift=UP * 0.1), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)

            summary_group = VGroup(heading, bullets, cue)
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
        out_dir = _HERE / "media" / "videos" / "decimal_forms_story"
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
        "Where does a fraction go when we write it as a decimal?"
        "<bookmark mark='b0'/> Decimal Forms.<bookmark mark='b1'/> Take "
        "five-eighths, and three-sevenths.<bookmark mark='b2'/> A "
        "fraction can always become a decimal.<bookmark mark='b3'/> What "
        "decimal does a fraction become?<bookmark mark='b4'/>"
    ),
    "fraction_division": (
        "Here's the key idea: a fraction is really just a division."
        "<bookmark mark='b0'/> P over Q simply means P divided by Q."
        "<bookmark mark='b1'/> Take five-eighths — that becomes five "
        "divided by eight.<bookmark mark='b2'/> To get the decimal form, "
        "divide the numerator by the denominator.<bookmark mark='b3'/> "
        "Of course, Q can never be zero.<bookmark mark='b4'/>"
    ),
    "terminating": (
        "Let's actually do the division for five divided by eight."
        "<bookmark mark='b0'/> Set it up and start dividing."
        "<bookmark mark='b1'/> The first digit is six, leaving a "
        "remainder of two. Keep going: the next digit is two, leaving a "
        "remainder of four. One more step gives five, and now the "
        "remainder becomes zero!<bookmark mark='b2'/> When the remainder "
        "hits zero, the decimal simply stops.<bookmark mark='b3'/> So "
        "five-eighths equals zero point six two five — a terminating "
        "decimal.<bookmark mark='b4'/>"
    ),
    "recurring": (
        "Now let's try three divided by seven.<bookmark mark='b0'/> "
        "Setting up the division.<bookmark mark='b1'/> Watch the digits "
        "appear one by one, while we track the remainder at every step."
        "<bookmark mark='b2'/> After six steps, look closely — the "
        "remainder three shows up again!<bookmark mark='b3'/> Since the "
        "remainder repeats, the digits must repeat too: three-sevenths "
        "equals zero point four two eight five seven one, repeating "
        "forever.<bookmark mark='b4'/> The digits repeat forever — this "
        "is a recurring decimal.<bookmark mark='b5'/>"
    ),
    "why_repeat": (
        "So why do the digits repeat? The secret is the remainder."
        "<bookmark mark='b0'/> Follow the chain of remainders from our "
        "division: three, two, six, four, five, one.<bookmark mark='b1'/> "
        "Each remainder leads to the next through the same division "
        "steps.<bookmark mark='b2'/> And eventually, the very first "
        "remainder shows up again, closing the loop.<bookmark mark='b3'/> "
        "The same remainder always produces the same division steps, "
        "and therefore the same repeating digits.<bookmark mark='b4'/> "
        "For terminating decimals, the remainder reaches zero — for "
        "recurring decimals, a remainder repeats.<bookmark mark='b5'/>"
    ),
    "comparison": (
        "Let's place both side by side.<bookmark mark='b0'/> On the "
        "left, five-eighths equals zero point six two five — the "
        "remainder reached zero, so the division stops.<bookmark mark='b1'/> "
        "On the right, three-sevenths equals zero point four two eight "
        "five seven one repeating — a remainder repeated, so the "
        "division loops forever.<bookmark mark='b2'/> Remember it simply: "
        "stop means terminating, loop means recurring.<bookmark mark='b3'/>"
    ),
    "challenge_setup": (
        "Time to predict the decimal type for two fractions."
        "<bookmark mark='b0'/> The first fraction is three-fourths."
        "<bookmark mark='b1'/> The second fraction is two-sevenths."
        "<bookmark mark='b2'/> Take a moment here, and watch the "
        "remainder carefully.<bookmark mark='b3'/>"
    ),
    "challenge_reveal": (
        "Three divided by four gives zero point seven five, and the "
        "remainder becomes zero — so that one is terminating."
        "<bookmark mark='b0'/> Two divided by seven gives zero point two "
        "eight five seven one four, and the remainder keeps repeating — "
        "so that one is recurring.<bookmark mark='b1'/>"
    ),
    "summary": (
        "Let's lock in the big idea.<bookmark mark='b1'/> Every fraction "
        "becomes a decimal through division.<bookmark mark='b2'/> If the "
        "remainder reaches zero, the decimal terminates — like "
        "five-eighths, which equals zero point six two five. If a "
        "remainder repeats, the decimal recurs — like three-sevenths, "
        "which equals zero point four two eight five seven one, "
        "repeating forever.<bookmark mark='b3'/> Divide, watch the "
        "remainder, and you'll always know: stop, or loop."
        "<bookmark mark='b4'/> Thank you so much for watching, and I "
        "will see you in the next lesson!"
    ),
}


if __name__ == "__main__":
    pass

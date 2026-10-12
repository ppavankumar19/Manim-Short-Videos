"""
Closure Property & the "Division by Zero" Trap
Story-mode chalkboard lesson (Classes 6-12 Maths, Closure Property of
Rational Numbers).

Production pipeline (mirrors the rest of the Story-Mode series):
  - assets/background2.png chalkboard backdrop.
  - VoiceoverScene + EdgeSpeechService (en-IN-PrabhatNeural).
  - Real per-word sync via <bookmark> tags + tracker timing.
  - Ground-truth SRT from edge-tts word boundaries.

Topic: an operation is "closed" on a set only when its result always
stays inside that set. Rational numbers are closed under addition,
subtraction, and multiplication -- but NOT division, because 5/0 is
undefined. Title + 9 beats + closing summary:
  0. Title card.
  1. Hook -- a "closed" Q box, does 2/3 ÷ 7/8 stay inside?
  2. Core idea -- a simple operation machine (2+3=5).
  3. Formal definition, built from whole numbers.
  4. Rational numbers pass addition, subtraction, multiplication.
  5. Division looks closed too (2/3 ÷ 7/8 = 16/21).
  6. The trap: 5 ÷ 0 is undefined.
  7. Why it fails: 0 × x can never equal 5.
  8. Challenge -- is division closed? (with a real pause).
  9. Recap -- closure table + golden rule.
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
    Rectangle, RoundedRectangle, Arrow, Text, Write, FadeIn, FadeOut,
    Create, Transform, ReplacementTransform, GrowFromCenter, GrowArrow,
    LaggedStart, DrawBorderThenFill, Indicate, config, Brace, Circumscribe,
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


class ClosurePropertyStory(VoiceoverScene):
    """9-beat Manim lesson on the closure property and division by zero."""

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
        self.badge_l = self._corner_badge("Closure Property", corner="left",
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
        self.beat1_hook()
        self.beat2_core_idea()
        self.beat3_definition()
        self.beat4_three_operations()
        self.beat5_division_seems_closed()
        self.beat6_division_by_zero()
        self.beat7_why_it_fails()
        self.beat8_challenge()
        self.beat9_recap()
        self.beat10_summary()

        self._write_real_srt()

    # ================================================================ beats ==

    def beat0_title(self):
        """Title card -- text only, no diagram: just the title and
        subtitle appearing on the plain chalkboard."""
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            self.wait(rt(tracker.time_until_bookmark("b0")))

            title = board_text("Closure Property", size=42, weight="BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 0.4, 0]))
            self.play(Write(title), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            subtitle = board_text("The 'Division by Zero' Trap", size=28,
                                  color=CHALK_PINK).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.4, 0]))
            self.play(Write(subtitle), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def _q_box(self, width: float = 3.2, height: float = 1.8) -> VGroup:
        box = RoundedRectangle(width=width, height=height, corner_radius=0.12,
                                stroke_color=CHALK_CYAN, stroke_width=2.5,
                                fill_color="#1E2A1A", fill_opacity=0.3)
        lbl = chalk_math(r"\mathbb{Q}", size=44, color=CHALK_CYAN).move_to(
            box.get_top() + DOWN * 0.4)
        return VGroup(box, lbl)

    def beat1_hook(self):
        """Beat 1: A "closed" Q box -- does 2/3 ÷ 7/8 stay inside?"""
        with self.voiceover(text=NARRATION["beat1"]) as tracker:
            self.reset_board()

            question0 = board_text("What does 'closed' mean?", size=26,
                                   color=CHALK_AMBER, weight="BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.8, 0]))
            self.play(Write(question0), run_time=rt(tracker.time_until_bookmark("b0")))

            qbox = self._q_box(width=3.4, height=1.9).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.6, 0]))
            self.play(Create(qbox[0]), Write(qbox[1]),
                     run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            num1 = chalk_math(r"\frac23", size=40, color=CHALK_GREEN).move_to(
                np.array([BOARD_CX - 2.6, BOARD_CY - 1.4, 0]))
            op = chalk_math(r"\div", size=40, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_CY - 1.4, 0]))
            num2 = chalk_math(r"\frac78", size=40, color=CHALK_PINK).move_to(
                np.array([BOARD_CX + 2.6, BOARD_CY - 1.4, 0]))
            self.play(FadeIn(num1), FadeIn(op), FadeIn(num2),
                     run_time=rt(tracker.time_until_bookmark("b2")))

            arrow1 = Arrow(num1.get_top(), qbox.get_bottom() + LEFT * 0.5,
                          color=CHALK_GREEN, stroke_width=2.5, buff=0.1)
            arrow2 = Arrow(num2.get_top(), qbox.get_bottom() + RIGHT * 0.5,
                          color=CHALK_PINK, stroke_width=2.5, buff=0.1)
            question = board_text("Does the result stay inside?", size=24,
                                  color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.5, 0]))
            self.play(GrowArrow(arrow1), GrowArrow(arrow2), Write(question),
                     run_time=rt(tracker.time_until_bookmark("b3")))

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat2_core_idea(self):
        """Beat 2: A simple operation machine -- 2 + 3 = 5."""
        with self.voiceover(text=NARRATION["beat2"]) as tracker:
            self.reset_board()

            # Everything shifted up from the old layout (machine center was
            # BOARD_CY+0.3) and the two-line caption merged into one, so the
            # final caption stays comfortably above BOARD_BOTTOM instead of
            # spilling off the bottom of the board.
            machine_y = BOARD_CY + 0.9
            machine = RoundedRectangle(width=2.0, height=1.6, corner_radius=0.15,
                                        stroke_color=CHALK_WHITE, stroke_width=2.5,
                                        fill_color="#3A2A15", fill_opacity=0.4).move_to(
                np.array([BOARD_CX, machine_y, 0]))
            self.play(Create(drop_shadow(machine, dx=0.06, dy=-0.07, opacity=0.3)),
                     run_time=rt(tracker.time_until_bookmark("b0")))

            a = chalk_math("2", size=48, color=CHALK_GREEN).move_to(
                np.array([BOARD_LEFT + 1.4, machine_y + 0.6, 0]))
            b = chalk_math("3", size=48, color=CHALK_PINK).move_to(
                np.array([BOARD_LEFT + 1.4, machine_y - 0.6, 0]))
            op_lbl = chalk_math("+", size=40, color=CHALK_AMBER).move_to(machine.get_center())
            arrow_a = Arrow(a.get_right(), machine.get_left() + UP * 0.3, buff=0.15,
                            stroke_width=2, color=CHALK_GREEN)
            arrow_b = Arrow(b.get_right(), machine.get_left() + DOWN * 0.3, buff=0.15,
                            stroke_width=2, color=CHALK_PINK)
            result = chalk_math("?", size=44, color=CHALK_WHITE).move_to(
                np.array([BOARD_RIGHT - 1.3, machine_y, 0]))
            arrow_out = Arrow(machine.get_right(), result.get_left(), buff=0.15,
                              stroke_width=2.5, color=CHALK_WHITE)
            self.play(FadeIn(a), FadeIn(b), Write(op_lbl),
                      GrowArrow(arrow_a), GrowArrow(arrow_b),
                      GrowArrow(arrow_out), FadeIn(result),
                     run_time=rt(tracker.time_until_bookmark("b1")))

            result5 = chalk_math("5", size=48, color=CHALK_YELLOW).move_to(result.get_center())
            self.play(ReplacementTransform(result, result5),
                      Indicate(machine, color=CHALK_AMBER, scale_factor=1.06),
                     run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            setbox = RoundedRectangle(width=6.6, height=1.15, corner_radius=0.1,
                                       stroke_color=CHALK_CYAN, stroke_width=2,
                                       fill_color="#1E2A1A", fill_opacity=0.25).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.9, 0]))
            members = VGroup(
                chalk_math("2", 32, CHALK_GREEN), chalk_math("3", 32, CHALK_PINK),
                chalk_math("5", 32, CHALK_YELLOW),
            ).arrange(RIGHT, buff=1.0).move_to(setbox.get_center())
            set_brace = Brace(members, DOWN, buff=0.1, color=CHALK_CYAN)
            self.play(Create(setbox), FadeIn(members), GrowFromCenter(set_brace),
                     run_time=rt(tracker.time_until_bookmark("b3")))

            caption = board_text("Closure = the result stays in the same set!", size=20,
                                 color=CHALK_CYAN, weight="BOLD").next_to(
                set_brace, DOWN, buff=0.3)
            self.play(FadeIn(caption), Indicate(setbox, color=CHALK_GREEN, scale_factor=1.04),
                     run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat3_definition(self):
        """Beat 3: Build the formal definition, from whole numbers."""
        with self.voiceover(text=NARRATION["beat3"]) as tracker:
            self.reset_board()

            eq = chalk_math("2+3=5", size=48, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_TOP - 1.0, 0]))
            self.play(Write(eq), run_time=rt(tracker.time_until_bookmark("b0")))

            wbox = RoundedRectangle(width=3.2, height=1.6, corner_radius=0.12,
                                     stroke_color=CHALK_CYAN, stroke_width=2.5,
                                     fill_color="#1E2A1A", fill_opacity=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.2, 0]))
            wlabel = chalk_math("W", size=40, color=CHALK_CYAN).move_to(
                wbox.get_top() + DOWN * 0.35)
            members = chalk_math("2,\\ 3,\\ 5", size=30, color=CHALK_YELLOW).move_to(
                wbox.get_center() + DOWN * 0.15)
            self.play(Create(wbox), Write(wlabel), FadeIn(members),
                     run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            general = chalk_math(r"a,b\in S\ \Rightarrow\ a\star b\in S", size=32,
                                 color=CHALK_GREEN).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 1.9, 0]))
            self.play(Write(general), run_time=rt(tracker.time_until_bookmark("b2")))

            closed_lbl = board_text("Closed under that operation", size=22,
                                    color=CHALK_CYAN, weight="BOLD").next_to(
                general, DOWN, buff=0.25)
            self.play(FadeIn(closed_lbl), run_time=rt(tracker.time_until_bookmark("b3")))

            # Two conditions, not one -- this is the piece the review
            # flagged as missing: closure requires the operation to be
            # DEFINED for every pair, as well as landing back in the set.
            # Without this, "5 / 0 is the counterexample" doesn't follow
            # from the rule as originally stated.
            rule = VGroup(
                board_text("1) The operation must give an answer", size=17,
                          weight="BOLD", color=CHALK_AMBER),
                board_text("2) That answer must stay in the set", size=17,
                          weight="BOLD", color=CHALK_AMBER),
            ).arrange(DOWN, buff=0.12).move_to(closed_lbl.get_center())
            self.play(ReplacementTransform(closed_lbl, rule),
                      Circumscribe(general, color=CHALK_AMBER),
                     run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)

            final_tag = board_text("Both must hold -- that's closure!", size=18,
                                   weight="BOLD", color=CHALK_GREEN).next_to(
                rule, DOWN, buff=0.25)
            self.play(FadeIn(final_tag), run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def _op_test(self, label: str, expr: str, result_tex: str, color: str) -> VGroup:
        lbl = board_text(label, size=22, color=color, weight="BOLD")
        eq = chalk_math(expr + "=" + result_tex, size=36, color=CHALK_WHITE)
        row = VGroup(lbl, eq).arrange(DOWN, buff=0.25).move_to(
            np.array([BOARD_CX, BOARD_CY + 0.2, 0]))
        return row

    def beat4_three_operations(self):
        """Beat 4: Addition, subtraction, multiplication all stay rational."""
        with self.voiceover(text=NARRATION["beat4"]) as tracker:
            self.reset_board()

            qbox = self._q_box(width=8.6, height=3.2).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.1, 0]))
            # Anchor the Q label to the box's own top-right corner (not an
            # absolute board position) so it reads as this box's label
            # instead of floating disconnected above it.
            qbox[1].move_to(qbox[0].get_corner(UR) + DOWN * 0.45 + LEFT * 0.5)
            self.play(Create(qbox[0]), Write(qbox[1]),
                     run_time=rt(tracker.time_until_bookmark("b0")))

            add_test = self._op_test("Addition", r"\frac27+\frac58", r"\frac{51}{56}", CHALK_GREEN)
            check1 = board_text("(rational)", 18, CHALK_GREEN).next_to(add_test, DOWN, buff=0.15)
            self.play(FadeIn(add_test), run_time=rt(tracker.time_until_bookmark("b1") * 0.7))
            self.play(FadeIn(check1), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            sub_test = self._op_test("Subtraction", r"\frac59-\frac34", r"-\frac{7}{36}", CHALK_PINK)
            check2 = board_text("(rational)", 18, CHALK_PINK).next_to(sub_test, DOWN, buff=0.15)
            self.play(FadeOut(add_test), FadeOut(check1), FadeIn(sub_test),
                     run_time=rt(tracker.time_until_bookmark("b2") * 0.7))
            self.play(FadeIn(check2), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            mul_test = self._op_test("Multiplication", r"\frac12\times\frac36", r"\frac14", CHALK_YELLOW)
            check3 = board_text("(rational)", 18, CHALK_YELLOW).next_to(mul_test, DOWN, buff=0.15)
            self.play(FadeOut(sub_test), FadeOut(check2), FadeIn(mul_test),
                     run_time=rt(tracker.time_until_bookmark("b3") * 0.7))
            self.play(FadeIn(check3), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            summary = VGroup(
                board_text("Addition (OK)", 22, CHALK_GREEN, "BOLD"),
                board_text("Subtraction (OK)", 22, CHALK_PINK, "BOLD"),
                board_text("Multiplication (OK)", 22, CHALK_YELLOW, "BOLD"),
            ).arrange(DOWN, buff=0.18).move_to(np.array([BOARD_CX, BOARD_CY, 0]))
            self.play(FadeOut(mul_test), FadeOut(check3), FadeIn(summary),
                     run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat5_division_seems_closed(self):
        """Beat 5: 2/3 ÷ 7/8 = 16/21 -- division seems closed too."""
        with self.voiceover(text=NARRATION["beat5"]) as tracker:
            self.reset_board()

            div_lbl = board_text("Division", size=24, color=CHALK_CYAN, weight="BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.7, 0]))
            self.play(Write(div_lbl), run_time=rt(tracker.time_until_bookmark("b0")))

            step1 = chalk_math(r"\frac23\div\frac78", size=44, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.6, 0]))
            self.play(Write(step1), run_time=rt(tracker.time_until_bookmark("b1") * 0.4))
            step2 = chalk_math(r"\frac23\times\frac87", size=44, color=CHALK_CYAN).move_to(
                step1.get_center())
            self.play(ReplacementTransform(step1, step2),
                     run_time=rt(tracker.time_until_bookmark("b1")))

            step3 = chalk_math(r"=\ \frac{16}{21}", size=44, color=CHALK_YELLOW).next_to(
                step2, DOWN, buff=0.4)
            self.play(Write(step3), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            qtag = board_text("still rational!", size=22, color=CHALK_GREEN,
                              weight="BOLD").next_to(step3, DOWN, buff=0.3)
            self.play(FadeIn(qtag), run_time=rt(tracker.time_until_bookmark("b3")))

            trap = chalk_math(r"5\div0", size=52, color=CHALK_RED).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.9, 0]))
            self.play(FadeOut(qtag), Write(trap),
                     run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["click"], gain=-15)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat6_division_by_zero(self):
        """Beat 6: 5 ÷ 0 is undefined -- the trap."""
        with self.voiceover(text=NARRATION["beat6"]) as tracker:
            self.reset_board()

            prob = chalk_math(r"5\div0", size=56, color=CHALK_RED).move_to(
                np.array([BOARD_CX, BOARD_TOP - 1.0, 0]))
            self.play(Write(prob), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["click"], gain=-15)

            frac = chalk_math(r"\frac50", size=48, color=CHALK_RED).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.4, 0]))
            self.play(ReplacementTransform(prob.copy(), frac), FadeOut(prob),
                     run_time=rt(tracker.time_until_bookmark("b1")))

            cross = board_text("(X)", size=40, weight="BOLD", color=CHALK_RED).next_to(
                frac, RIGHT, buff=0.4)
            self.play(FadeIn(cross), Indicate(frac, color=CHALK_RED, scale_factor=1.1),
                     run_time=rt(tracker.time_until_bookmark("b2")))

            # A small flow arrow -- "the attempt stops here" -- connecting
            # the failed 5/0 to why it fails, echoing the storyboard's
            # 5÷0 -> X -> not defined pipeline visual.
            fail_arrow = Arrow(frac.get_bottom() + DOWN * 0.1, frac.get_bottom() + DOWN * 0.7,
                               color=CHALK_RED, stroke_width=2.5, buff=0)
            note1 = board_text("Zero cannot be the divisor.", size=24, color=CHALK_AMBER,
                               weight="BOLD").move_to(np.array([BOARD_CX, BOARD_CY - 1.1, 0]))
            self.play(GrowArrow(fail_arrow), FadeIn(note1),
                     run_time=rt(tracker.time_until_bookmark("b3")))

            note2 = board_text("Undefined -- no quotient.", size=22, color=CHALK_PINK).next_to(
                note1, DOWN, buff=0.3)
            self.play(FadeIn(note2), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["click"], gain=-15)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat7_why_it_fails(self):
        """Beat 7: 5 ÷ 0 = ? means 0 × ? = 5 -- and 0 × x is always 0."""
        with self.voiceover(text=NARRATION["beat7"]) as tracker:
            self.reset_board()

            q1 = chalk_math(r"5\div0=\ ?", size=44, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.9, 0]))
            self.play(Write(q1), run_time=rt(tracker.time_until_bookmark("b0")))

            q2 = chalk_math(r"0\times\ ?\ =5", size=44, color=CHALK_CYAN).move_to(q1.get_center())
            self.play(ReplacementTransform(q1, q2),
                     run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["swipe"], gain=-14)

            general = chalk_math(r"0\times x=0", size=36, color=CHALK_AMBER).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.5, 0]))
            self.play(Write(general), run_time=rt(tracker.time_until_bookmark("b2")))

            tries = VGroup(
                chalk_math(r"0\times1=0", size=28, color=CHALK_WHITE),
                chalk_math(r"0\times5=0", size=28, color=CHALK_WHITE),
                chalk_math(r"0\times100=0", size=28, color=CHALK_WHITE),
            ).arrange(DOWN, buff=0.22).next_to(general, DOWN, buff=0.4)
            self.play(LaggedStart(*[FadeIn(t) for t in tries], lag_ratio=0.3),
                     run_time=rt(tracker.time_until_bookmark("b3")))

            never = chalk_math(r"0\times x\neq5", size=34, color=CHALK_RED).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.5, 0]))
            self.play(Write(never), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["click"], gain=-15)

            aha = board_text("There is no quotient.", size=24, weight="BOLD",
                             color=CHALK_PINK).move_to(never.get_center())
            self.play(ReplacementTransform(never, aha),
                     run_time=rt(tracker.time_until_bookmark("b5")))

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat8_challenge(self):
        """Beat 8: YOUR TURN -- is division closed? The test expressions
        and question live in a bordered box near the bottom of the
        board, clear of the round THINK badge which now sits at board
        centre and dims everything else while it counts down."""
        with self.voiceover(text=NARRATION["beat8_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", size=32, weight="BOLD",
                                 color=CHALK_PINK).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.6, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            box_y = BOARD_BOTTOM + 1.0
            box = RoundedRectangle(width=8.6, height=1.3, corner_radius=0.12,
                                    stroke_color=CHALK_CYAN, stroke_width=2,
                                    fill_color="#1E2A1A", fill_opacity=0.3).move_to(
                np.array([BOARD_CX, box_y, 0]))
            testA = chalk_math(r"\frac34\div\frac25", size=32, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX - 2.0, box_y + 0.35, 0]))
            testB = chalk_math(r"5\div0", size=32, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX + 2.0, box_y + 0.35, 0]))
            self.play(Create(box), FadeIn(testA), FadeIn(testB),
                     run_time=rt(tracker.time_until_bookmark("b1")))

            question = board_text("Is division closed for rational numbers?", size=17,
                                  color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, box_y - 0.35, 0]))
            self.play(FadeIn(question), run_time=rt(tracker.time_until_bookmark("b2")))

            self._capture_srt(tracker)

        # Consistent 10-second challenge clock (whole series): a round
        # THINK badge at board centre dims the WHOLE board (question box
        # included) except itself while students think.
        play_challenge_countdown(self, seconds=10, sfx=self.sfx)

        with self.voiceover(text=NARRATION["beat8_reveal"]) as tracker:
            # The setup content has served its purpose -- clear it so the
            # reveal rows have the whole box to themselves.
            self.play(FadeOut(VGroup(testA, testB, question)),
                     run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            rowA_math = chalk_math(r"\frac34\div\frac25=\frac{15}{8}", size=26,
                                   color=CHALK_GREEN)
            rowA_tag = board_text("(OK)", size=18, weight="BOLD", color=CHALK_GREEN)
            rowA = VGroup(rowA_math, rowA_tag).arrange(RIGHT, buff=0.25).move_to(
                np.array([BOARD_CX, box_y + 0.32, 0]))
            self.play(Write(rowA), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["success"], gain=-11)

            rowB_math = chalk_math(r"5\div0", size=26, color=CHALK_WHITE)
            rowB_word = board_text("= undefined", size=22, weight="BOLD", color=CHALK_RED)
            rowB_tag = board_text("(X)", size=18, weight="BOLD", color=CHALK_RED)
            rowB = VGroup(rowB_math, rowB_word, rowB_tag).arrange(RIGHT, buff=0.2).move_to(
                np.array([BOARD_CX, box_y - 0.32, 0]))
            self.play(Write(rowB), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            final = board_text("Not closed!", size=30, weight="BOLD", color=CHALK_PINK).move_to(
                heading.get_center())
            self.play(ReplacementTransform(heading, final),
                      Indicate(rowB, color=CHALK_RED, scale_factor=1.06),
                     run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat9_recap(self):
        """Beat 9: Closes the loop -- revisits the opening "machine"
        metaphor to explain what "undefined" concretely means (the
        machine jams, nothing comes out), and confirms the video's own
        opening example (2/3 / 7/8) stayed inside the set. Deliberately
        NOT a repeat of the closing summary's recap sentences -- review
        flagged the two beats as near-verbatim duplicates."""
        with self.voiceover(text=NARRATION["beat9"]) as tracker:
            self.reset_board()

            heading = board_text("Closure Under the Four Operations", size=22,
                                 color=CHALK_AMBER, weight="BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.5, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))

            rows = VGroup(
                board_text("Addition          (OK)", 24, CHALK_GREEN),
                board_text("Subtraction       (OK)", 24, CHALK_PINK),
                board_text("Multiplication    (OK)", 24, CHALK_YELLOW),
                board_text("Division          (X)", 24, CHALK_RED),
            ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.5, 0]))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.25),
                     run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            # b1->b2: "Addition, subtraction, and multiplication all
            # stayed inside the set -- just like two-thirds divided by
            # seven-eighths did, right at the start." -- closes the loop
            # on the video's OWN opening example instead of restating
            # the upcoming summary's conclusion.
            self.play(Indicate(VGroup(rows[0], rows[1], rows[2]), color=CHALK_GREEN,
                                scale_factor=1.05),
                     run_time=rt(tracker.time_until_bookmark("b2")))

            # b2->b3: "Division is the one exception -- it only jams when
            # the divisor is zero."
            self.play(Indicate(rows[3], color=CHALK_RED, scale_factor=1.08),
                     run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            # b3->b4: "Undefined means the machine jams: no answer comes
            # out at all." -- the S1 fix: ties "undefined" back to the
            # opening operation-machine metaphor instead of leaving it
            # as an abstract word.
            golden = board_text("Undefined = the machine jams, no answer at all", size=17,
                                weight="BOLD", color=CHALK_AMBER).next_to(
                rows, DOWN, buff=0.4)
            self.play(FadeIn(golden), Circumscribe(rows, color=CHALK_AMBER, stroke_width=2.5),
                     run_time=rt(tracker.time_until_bookmark("b4")))
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
        across the whole Story-Mode series."""
        with self.voiceover(text=NARRATION["summary"]) as tracker:
            self.reset_board()

            heading = board_text("Summary", 34, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.4, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            bullets = VGroup(
                self.bullet_row(1, ["Addition, subtraction and multiplication:",
                                     "all stay rational."], color=CHALK_GREEN),
                self.bullet_row(2, ["Division breaks it: 5 ÷ 0 is undefined."],
                                 color=CHALK_RED),
                self.bullet_row(3, ["Q is closed under +, −, ×",
                                     "but NOT under ÷."], color=CHALK_PINK),
            )
            bullets.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
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
        out_dir = _HERE / "media" / "videos" / "closure_property_story"
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
        "Every operation makes a promise: keep the result inside the set."
        "<bookmark mark='b0'/> Welcome to the Closure Property,"
        "<bookmark mark='b1'/> and the sneaky 'Division by Zero' trap!"
        "<bookmark mark='b2'/>"
    ),
    "beat1": (
        "What does it mean for something to be 'closed'?<bookmark mark='b0'/> "
        "Here's the set of rational numbers, Q.<bookmark mark='b1'/> Take two "
        "numbers — two-thirds and seven-eighths — with a division between "
        "them.<bookmark mark='b2'/> Does the result stay inside the set?"
        "<bookmark mark='b3'/>"
    ),
    "beat2": (
        "Think of it like a simple machine.<bookmark mark='b0'/> Two numbers "
        "go in, an operation happens, and a result comes out.<bookmark mark='b1'/> "
        "Two plus three equals five.<bookmark mark='b2'/> All three numbers "
        "belong to the same set.<bookmark mark='b3'/> That's closure: the "
        "result stays in the same set.<bookmark mark='b4'/>"
    ),
    "beat3": (
        "Let's build the formal idea, starting with whole numbers."
        "<bookmark mark='b0'/> Two plus three equals five — and two, "
        "three and five are all whole numbers.<bookmark mark='b1'/> In "
        "general: if a and b belong to a set S, and a star b also "
        "belongs to S,<bookmark mark='b2'/> then the set is closed under "
        "that operation.<bookmark mark='b3'/> But that's only half the "
        "story: the operation must always give an answer, and that "
        "answer must stay in the set.<bookmark mark='b4'/> Both "
        "together — that's real closure!<bookmark mark='b5'/>"
    ),
    "beat4": (
        "Now let's test rational numbers.<bookmark mark='b0'/> Addition: "
        "two-sevenths plus five-eighths equals fifty-one over fifty-six — "
        "still rational.<bookmark mark='b1'/> Subtraction: five-ninths "
        "minus three-fourths equals minus seven over thirty-six — still "
        "rational.<bookmark mark='b2'/> Multiplication: one-half times "
        "three-sixths equals one-fourth — still rational.<bookmark mark='b3'/> "
        "Addition, subtraction, and multiplication all pass!<bookmark mark='b4'/>"
    ),
    "beat5": (
        "What about division?<bookmark mark='b0'/> Two-thirds divided by "
        "seven-eighths means two-thirds times eight-sevenths,"
        "<bookmark mark='b1'/> which equals sixteen over twenty-one — still "
        "rational!<bookmark mark='b2'/> Division seems closed too — but "
        "watch what happens with this:<bookmark mark='b3'/> five "
        "divided by zero.<bookmark mark='b4'/>"
    ),
    "beat6": (
        "Let's try five divided by zero.<bookmark mark='b0'/> That's the "
        "same as five over zero.<bookmark mark='b1'/> But division by zero "
        "is simply not allowed.<bookmark mark='b2'/> Zero cannot be the "
        "divisor.<bookmark mark='b3'/> So the result is undefined — "
        "there is no quotient at all.<bookmark mark='b4'/>"
    ),
    "beat7": (
        "Why exactly does this fail?<bookmark mark='b0'/> Five divided by "
        "zero really means: zero times what equals five?<bookmark mark='b1'/> "
        "But zero times any number always gives zero.<bookmark mark='b2'/> "
        "Zero times one is zero, zero times five is zero, zero times one "
        "hundred is zero.<bookmark mark='b3'/> There's no number that makes "
        "zero times x equal five.<bookmark mark='b4'/> There is simply no "
        "quotient.<bookmark mark='b5'/>"
    ),
    "beat8_setup": (
        "Now it's your turn.<bookmark mark='b0'/> Test these: three-fourths "
        "divided by two-fifths, and five divided by zero.<bookmark mark='b1'/> "
        "Pause and decide — is division closed for rational numbers?"
        "<bookmark mark='b2'/>"
    ),
    "beat8_reveal": (
        "Three-fourths divided by two-fifths equals fifteen over eight — "
        "that works.<bookmark mark='b0'/> But five divided by zero is "
        "undefined — that breaks it.<bookmark mark='b1'/> Just one "
        "counterexample is enough: division is not closed.<bookmark mark='b2'/>"
    ),
    "beat9": (
        "Remember our operation machine?<bookmark mark='b0'/> Here are "
        "all four operations we tested.<bookmark mark='b1'/> Addition, "
        "subtraction, and multiplication all stayed inside the set — "
        "just like two-thirds divided by seven-eighths did, right at "
        "the start.<bookmark mark='b2'/> Division is the one exception "
        "— it only jams when the divisor is zero.<bookmark mark='b3'/> "
        "Undefined means the machine jams: no answer comes out at all."
        "<bookmark mark='b4'/>"
    ),
    "summary": (
        "Let's lock in what we learned today.<bookmark mark='b1'/> "
        "Addition, subtraction, and multiplication of rational numbers "
        "all stay rational.<bookmark mark='b2'/> But division breaks the "
        "rule, because five divided by zero is simply undefined."
        "<bookmark mark='b3'/> So rational numbers are closed under "
        "addition, subtraction, and multiplication — but not under "
        "division.<bookmark mark='b4'/> Thank you so much for watching, "
        "and I will see you in the next lesson!"
    ),
}


if __name__ == "__main__":
    pass

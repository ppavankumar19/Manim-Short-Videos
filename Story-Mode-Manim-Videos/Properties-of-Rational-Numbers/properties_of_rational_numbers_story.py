"""
Properties of Rational Numbers -- Closure, Commutative, Associative
Story-mode chalkboard lesson (Classes 6-12 Maths, Chapter 1 -- Rational
Numbers).

Production pipeline (mirrors the rest of the Story-Mode series):
  - assets/background2.png chalkboard backdrop.
  - VoiceoverScene + EdgeSpeechService (en-IN-PrabhatNeural).
  - Real per-word sync via <bookmark> tags + tracker timing.
  - Ground-truth SRT from edge-tts word boundaries.
  - Shared story_common.play_challenge_countdown() for the "YOUR TURN"
    round THINK badge (board-centre, dims the whole board except itself).

Topic: three separate lenses on the same four operations --
  - Closure: does the RESULT stay inside Q?
  - Commutative: does SWAPPING the numbers change the result?
  - Associative: does REGROUPING (moving brackets) change the result?
Production rule kept visually distinct throughout: Commutative moves the
NUMBERS; Associative keeps numbers in place and moves only the GROUPING
highlight; Closure moves the RESULT into/outside the Q container.

Title + 8 beats + closing summary:
  0. Title card (text only, no diagram).
  1. Intro -- three property cards (Closure/Commutative/Associative).
  2. What do properties tell us? -- a+b+c and the three guiding questions.
  3. Closure: 2/7+5/8=51/56 stays in Q; contrast 5/0 undefined.
  4. Commutative: 2+3=3+2=5 (physical swap); 3/5+2/7=2/7+3/5=31/35;
     contrast 5-2=3 != 2-5=-3.
  5. Associative: (3+2)+5=3+(2+5)=10 (moving grouping highlight);
     (1/2+1/3)+1/6 = 1/2+(1/3+1/6) = 1; contrast (5-3)-1=1 != 5-(3-1)=3.
  6. One-glance comparison table.
  7. Challenge -- identify the property for 3 quick tests (round THINK
     badge, whole-board dim, questions in a bottom box).
  8. Summary -- bullet recap + Thank You card.
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
    SurroundingRectangle,
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
BOARD_Y_SHIFT = 0.3  # whole board nudged up a bit; kept content-side so it
                     # stays aligned with the shifted backdrop in add_background()
BOARD_TOP = 3.3 + BOARD_Y_SHIFT
BOARD_BOTTOM = -2.9 + BOARD_Y_SHIFT
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


class PropertiesOfRationalNumbersStory(VoiceoverScene):
    """9-beat Manim lesson on Closure, Commutative, and Associative
    properties of rational numbers."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._srt_entries: list[tuple[float, float, str]] = []

    # -- backdrop (mirrors every Story-Mode video) -------------------------
    def add_background(self) -> None:
        assets_dir = Path(_ROOT) / "Story-Mode-Manim-Videos" / "assets"

        bg = ImageMobject(str(assets_dir / "background2.png"))
        bg.stretch_to_fit_width(config.frame_width)
        # Extra height gives slack so the whole board can shift up without
        # opening a gap at the bottom of frame (see BOARD_Y_SHIFT above).
        bg.stretch_to_fit_height(config.frame_height + 2 * BOARD_Y_SHIFT)
        bg.move_to(ORIGIN)
        bg.shift(UP * BOARD_Y_SHIFT)
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
        # same visual size. This replaces the old image-based
        # "dhimantAI logo.png" badge with a text badge matching the
        # right-corner subject badge's style.
        self.bg = bg
        self.student = student
        self.teacher = teacher
        self.badge = self._corner_badge("Mathematics", corner="right",
                                         y=BOARD_TOP - 0.16, font_size=12,
                                         scale=16 / 12)
        self.logo = self._corner_badge("dhimantAI", corner="left",
                                        y=BOARD_TOP - 0.16, font_size=12,
                                        scale=16 / 12, text_color=BRAND_WHITE)

        self.add(self.bg, self.student, self.teacher, self.logo, self.badge)

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
            badge.shift(LEFT * (badge.get_left()[0] - (BOARD_LEFT + 0.08)))
        else:
            badge.move_to(np.array([BOARD_RIGHT - 0.6, yy, 0]))
            # Right margin is smaller than the left corner's 0.08 to
            # compensate for the background art's perspective -- at equal
            # 0.08 margins the right badge renders with a visibly larger
            # gap to the board frame than the left badge, so it's nudged
            # right to match dhimantAI's spacing (same fix as the
            # Distributive-Property-Smart-Simplification project).
            badge.shift(RIGHT * (BOARD_RIGHT - 0.013 - badge.get_right()[0]))
        # Snap the TOP edge to the same 0.08 margin used horizontally, so
        # both badges sit with equal spacing from the board's edges
        # regardless of font scaling.
        badge.shift(UP * ((BOARD_TOP - 0.08) - badge.get_top()[1]))
        return badge

    def reset_board(self) -> None:
        self.clear()
        self.add(self.bg, self.student, self.teacher, self.logo, self.badge)

    def construct(self):
        self.sfx = load_sfx()
        self.set_speech_service(get_speech_service(), create_subcaption=False)

        self.add_background()

        self.beat0_title()
        self.beat1_intro_cards()
        self.beat2_context()
        self.beat3_closure()
        self.beat4_commutative()
        self.beat5_associative()
        self.beat6_comparison()
        self.beat7_challenge()
        self.beat8_summary()

        self._write_real_srt()

    # ================================================================ beats ==

    def _swap(self, left, right, run_time: float):
        """Physically swap two mobjects' positions -- the movement
        itself is the mental model for commutativity."""
        lp, rp = left.get_center().copy(), right.get_center().copy()
        self.play(left.animate.move_to(rp), right.animate.move_to(lp),
                 run_time=run_time)

    def beat0_title(self):
        """Title card -- text only, no diagram."""
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            # Title now draws DURING the opening line instead of sitting
            # on a silent empty board until b0 -- removes the dead-air
            # delay before anything appears on screen.
            title = board_text("Properties of Rational Numbers", size=32,
                               weight="BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 0.4, 0]))
            self.play(Write(title), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(rt(tracker.time_until_bookmark("b1") * 0.3))

            subtitle = board_text("Closure  •  Commutative  •  Associative",
                                  size=24, color=CHALK_PINK).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.4, 0]))
            self.play(Write(subtitle), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat1_intro_cards(self):
        """Beat 1: three property cards, each with a tiny symbol."""
        with self.voiceover(text=NARRATION["beat1"]) as tracker:
            self.reset_board()

            tagline = board_text("Three properties. Three simple tips.", size=22,
                                 color=CHALK_AMBER, weight="BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.6, 0]))
            self.play(Write(tagline), run_time=rt(tracker.time_until_bookmark("b0")))

            card_w, card_h = 2.6, 2.0

            c1 = RoundedRectangle(width=card_w, height=card_h, corner_radius=0.12,
                                   stroke_color=CHALK_CYAN, stroke_width=2.5,
                                   fill_color="#1E2A1A", fill_opacity=0.3).move_to(
                np.array([BOARD_CX - 3.0, BOARD_CY - 0.3, 0]))
            c1_icon = RoundedRectangle(width=0.5, height=0.4, corner_radius=0.05,
                                        stroke_color=CHALK_CYAN, stroke_width=2).move_to(
                c1.get_center() + UP * 0.35)
            c1_dot = Dot(c1_icon.get_center(), radius=0.06, color=CHALK_YELLOW)
            c1_lbl = board_text("CLOSURE", size=18, weight="BOLD",
                                color=CHALK_CYAN).move_to(c1.get_center() + DOWN * 0.5)
            self.play(Create(c1), FadeIn(c1_icon), FadeIn(c1_dot), Write(c1_lbl),
                     run_time=rt(tracker.time_until_bookmark("b1")))

            c2 = RoundedRectangle(width=card_w, height=card_h, corner_radius=0.12,
                                   stroke_color=CHALK_PINK, stroke_width=2.5,
                                   fill_color="#1E2A1A", fill_opacity=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.3, 0]))
            c2_a1 = Arrow(LEFT * 0.32, RIGHT * 0.32, color=CHALK_PINK, stroke_width=2.5,
                         buff=0).move_to(c2.get_center() + UP * 0.45)
            c2_a2 = Arrow(RIGHT * 0.32, LEFT * 0.32, color=CHALK_PINK, stroke_width=2.5,
                         buff=0).move_to(c2.get_center() + UP * 0.22)
            c2_lbl = board_text("COMMUTATIVE", size=15, weight="BOLD",
                                color=CHALK_PINK).move_to(c2.get_center() + DOWN * 0.5)
            self.play(Create(c2), FadeIn(c2_a1), FadeIn(c2_a2), Write(c2_lbl),
                     run_time=rt(tracker.time_until_bookmark("b2")))

            c3 = RoundedRectangle(width=card_w, height=card_h, corner_radius=0.12,
                                   stroke_color=CHALK_AMBER, stroke_width=2.5,
                                   fill_color="#1E2A1A", fill_opacity=0.3).move_to(
                np.array([BOARD_CX + 3.0, BOARD_CY - 0.3, 0]))
            c3_icon = chalk_math(r"(\ \cdot\ )", size=32, color=CHALK_AMBER).move_to(
                c3.get_center() + UP * 0.35)
            c3_lbl = board_text("ASSOCIATIVE", size=15, weight="BOLD",
                                color=CHALK_AMBER).move_to(c3.get_center() + DOWN * 0.5)
            self.play(Create(c3), FadeIn(c3_icon), Write(c3_lbl),
                     run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat2_context(self):
        """Beat 2: a+b+c and the three guiding questions."""
        with self.voiceover(text=NARRATION["beat2"]) as tracker:
            self.reset_board()

            heading = board_text("What Do Properties Tell Us?", size=24, weight="BOLD",
                                 color=CHALK_AMBER).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.6, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))

            expr = chalk_math("a+b+c", size=44, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_CY + 1.1, 0]))
            self.play(Write(expr), run_time=rt(tracker.time_until_bookmark("b1")))

            q1 = board_text("Closure: stays inside the set", size=20,
                            color=CHALK_CYAN).move_to(np.array([BOARD_CX, BOARD_CY + 0.15, 0]))
            self.play(FadeIn(q1), run_time=rt(tracker.time_until_bookmark("b2")))

            q2 = board_text("Commutative: can we change the order?", size=20,
                            color=CHALK_PINK).next_to(q1, DOWN, buff=0.3)
            self.play(FadeIn(q2), run_time=rt(tracker.time_until_bookmark("b3")))

            q3 = board_text("Associative: can we change the grouping?", size=20,
                            color=CHALK_AMBER).next_to(q2, DOWN, buff=0.3)
            self.play(FadeIn(q3), run_time=rt(tracker.time_until_bookmark("b4")))

            self.play(Circumscribe(VGroup(q1, q2, q3), color=CHALK_YELLOW, stroke_width=2),
                     run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat3_closure(self):
        """Beat 3: 3+4=7 stays inside the set; contrast 5-6=-1, which
        doesn't -- whole-number examples, not fractions."""
        with self.voiceover(text=NARRATION["beat3"]) as tracker:
            self.reset_board()

            heading = board_text("Closure Property", size=28, weight="BOLD",
                                 color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.6, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))

            formula = chalk_math(r"a \; + \; b \;\in\; \text{Set} \qquad\qquad "
                                  r"a \; \times \; b \;\in\; \text{Set}",
                                  size=26, color=CHALK_AMBER).move_to(
                np.array([BOARD_CX, BOARD_CY + 1.3, 0]))
            self.play(Write(formula), run_time=rt(MIN_RT))

            qbox = RoundedRectangle(width=6.4, height=2.0, corner_radius=0.12,
                                     stroke_color=CHALK_CYAN, stroke_width=2.5,
                                     fill_color="#1E2A1A", fill_opacity=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.15, 0]))
            qlbl = board_text("Whole Numbers", size=16, color=CHALK_CYAN).move_to(
                qbox.get_corner(UR) + DOWN * 0.3 + LEFT * 0.85)
            self.play(Create(qbox), Write(qlbl), run_time=rt(MIN_RT))

            eq = chalk_math(r"3 \; + \; 4 \; = \; 7", size=36, color=CHALK_WHITE).move_to(
                qbox.get_center())
            self.play(Write(eq), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            tag = board_text("Still a whole number!", size=20, weight="BOLD",
                             color=CHALK_GREEN).next_to(qbox, DOWN, buff=0.3)
            self.play(FadeIn(tag), Indicate(eq, color=CHALK_GREEN, scale_factor=1.1),
                     run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            trap = chalk_math(r"5 \; - \; 6 \; = \; -1", size=28, color=CHALK_RED).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.8, 0]))
            self.play(Write(trap), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            note = board_text("Not a whole number -- subtraction is NOT closed!", size=15,
                              weight="BOLD", color=CHALK_RED).next_to(trap, DOWN, buff=0.15)
            self.play(FadeIn(note), run_time=rt(tracker.time_until_bookmark("b4")))

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat4_commutative(self):
        """Beat 4: 2+3=3+2=5 (physical swap); rational check;
        contrast subtraction."""
        with self.voiceover(text=NARRATION["beat4"]) as tracker:
            self.reset_board()

            heading = board_text("Commutative", size=28, weight="BOLD",
                                 color=CHALK_PINK).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.6, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))

            card2 = chalk_math("5", size=44, color=CHALK_GREEN).move_to(
                np.array([BOARD_CX - 1.3, BOARD_CY + 1.15, 0]))
            plus = chalk_math("+", size=44, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_CY + 1.15, 0]))
            card3 = chalk_math("3", size=44, color=CHALK_PINK).move_to(
                np.array([BOARD_CX + 1.3, BOARD_CY + 1.15, 0]))
            eq5 = chalk_math("=\\ 8", size=44, color=CHALK_YELLOW).next_to(
                card3, RIGHT, buff=0.3)
            self.play(FadeIn(card2), FadeIn(plus), FadeIn(card3), Write(eq5),
                     run_time=rt(tracker.time_until_bookmark("b1")))

            self._swap(card2, card3, rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["swipe"], gain=-14)

            tag = board_text("Order doesn't matter!", size=18, weight="BOLD",
                             color=CHALK_GREEN).move_to(np.array([BOARD_CX, BOARD_CY + 0.55, 0]))
            self.play(FadeIn(tag), Indicate(VGroup(card2, plus, card3, eq5),
                                             color=CHALK_GREEN, scale_factor=1.05),
                     run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)

            formula_add = chalk_math(r"a \; + \; b \; = \; b \; + \; a",
                                     size=26, color=CHALK_CYAN)
            formula_mul = chalk_math(r"a \; \times \; b \; = \; b \; \times \; a",
                                     size=26, color=CHALK_CYAN)
            VGroup(formula_add, formula_mul).arrange(DOWN, buff=0.2).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.25, 0]))
            self.play(Write(formula_add), run_time=rt(tracker.time_until_bookmark("b4") * 0.5))
            self.play(Write(formula_mul), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            sub1 = chalk_math(r"5 \; - \; 3 \; = \; 2", size=28, color=CHALK_WHITE)
            sub2 = chalk_math(r"3 \; - \; 5 \; = \; -2", size=28, color=CHALK_RED)
            VGroup(sub1, sub2).arrange(RIGHT, buff=0.6).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.95, 0]))
            self.play(Write(sub1), run_time=rt(tracker.time_until_bookmark("b5") * 0.5))
            self.play(Write(sub2), run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["click"], gain=-15)

            subtag = board_text("Subtraction is NOT commutative!", size=16, weight="BOLD",
                                color=CHALK_RED).next_to(VGroup(sub1, sub2), DOWN, buff=0.18)
            self.play(FadeIn(subtag), run_time=rt(tracker.time_until_bookmark("b6")))

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat5_associative(self):
        """Beat 5: (3+2)+5=3+(2+5)=10 -- only the grouping highlight
        moves, numbers stay in place; rational check; contrast subtraction."""
        with self.voiceover(text=NARRATION["beat5"]) as tracker:
            self.reset_board()

            heading = board_text("Associative", size=28, weight="BOLD",
                                 color=CHALK_AMBER).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.6, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))

            n3 = chalk_math("2", size=40, color=CHALK_GREEN).move_to(
                np.array([BOARD_CX - 1.6, BOARD_CY + 1.15, 0]))
            p1 = chalk_math("+", size=40, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX - 0.8, BOARD_CY + 1.15, 0]))
            n2 = chalk_math("3", size=40, color=CHALK_PINK).move_to(
                np.array([BOARD_CX, BOARD_CY + 1.15, 0]))
            p2 = chalk_math("+", size=40, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX + 0.8, BOARD_CY + 1.15, 0]))
            n5 = chalk_math("4", size=40, color=CHALK_AMBER).move_to(
                np.array([BOARD_CX + 1.6, BOARD_CY + 1.15, 0]))
            self.play(Write(VGroup(n3, p1, n2, p2, n5)),
                     run_time=rt(tracker.time_until_bookmark("b1")))

            group_hl = SurroundingRectangle(VGroup(n3, p1, n2), color=CHALK_CYAN,
                                             buff=0.1, corner_radius=0.08)
            result1 = chalk_math("=\\ 9", size=40, color=CHALK_YELLOW).next_to(
                n5, RIGHT, buff=0.3)
            self.play(Create(group_hl), run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            self.play(Write(result1), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            group_hl2 = SurroundingRectangle(VGroup(n2, p2, n5), color=CHALK_CYAN,
                                              buff=0.1, corner_radius=0.08)
            self.play(Transform(group_hl, group_hl2), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["swipe"], gain=-14)

            tag = board_text("Grouping doesn't matter!", size=18, weight="BOLD",
                             color=CHALK_GREEN).move_to(np.array([BOARD_CX, BOARD_CY + 0.55, 0]))
            self.play(FadeIn(tag), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)

            formula_add = chalk_math(r"(a \; + \; b) \; + \; c \; = \; a \; + \; (b \; + \; c)",
                                     size=22, color=CHALK_CYAN)
            formula_mul = chalk_math(r"(a \; \times \; b) \; \times \; c \; = \; "
                                      r"a \; \times \; (b \; \times \; c)",
                                     size=22, color=CHALK_CYAN)
            VGroup(formula_add, formula_mul).arrange(DOWN, buff=0.2).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.35, 0]))
            self.play(Write(formula_add), run_time=rt(tracker.time_until_bookmark("b5") * 0.5))
            self.play(Write(formula_mul), run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["ding"], gain=-13)

            subA = chalk_math(r"(5 \; - \; 3) \; - \; 1 \; = \; 1", size=24, color=CHALK_WHITE)
            subB = chalk_math(r"5 \; - \; (3 \; - \; 1) \; = \; 3", size=24, color=CHALK_RED)
            VGroup(subA, subB).arrange(RIGHT, buff=0.6).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.95, 0]))
            self.play(Write(subA), run_time=rt(tracker.time_until_bookmark("b6") * 0.5))
            self.play(Write(subB), run_time=rt(tracker.time_until_bookmark("b6")))
            self.add_sound(self.sfx["click"], gain=-15)

            subtag = board_text("Subtraction is NOT associative!", size=16, weight="BOLD",
                                color=CHALK_RED).next_to(VGroup(subA, subB), DOWN, buff=0.18)
            self.play(FadeIn(subtag), run_time=rt(tracker.time_until_bookmark("b7")))

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat6_comparison(self):
        """Beat 6: one-glance comparison of what each property checks."""
        with self.voiceover(text=NARRATION["beat6"]) as tracker:
            self.reset_board()

            heading = board_text("One-Glance Comparison", size=24, weight="BOLD",
                                 color=CHALK_AMBER).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.5, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))

            row1 = VGroup(
                board_text("CLOSURE", 22, CHALK_CYAN, "BOLD"),
                board_text("-> Stay inside the set?", 20, CHALK_WHITE),
            ).arrange(RIGHT, buff=0.3)
            row2 = VGroup(
                board_text("COMMUTATIVE", 22, CHALK_PINK, "BOLD"),
                board_text("-> Change the order?", 20, CHALK_WHITE),
            ).arrange(RIGHT, buff=0.3)
            row3 = VGroup(
                board_text("ASSOCIATIVE", 22, CHALK_AMBER, "BOLD"),
                board_text("-> Move the brackets?", 20, CHALK_WHITE),
            ).arrange(RIGHT, buff=0.3)
            rows = VGroup(row1, row2, row3).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX, BOARD_CY, 0]))

            self.play(FadeIn(row1, shift=RIGHT * 0.15), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(row2, shift=RIGHT * 0.15), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(row3, shift=RIGHT * 0.15), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            tag = board_text("Three different questions, three different tests!",
                             size=16, weight="BOLD", color=CHALK_GREEN).next_to(
                rows, DOWN, buff=0.4)
            self.play(FadeIn(tag), Circumscribe(rows, color=CHALK_AMBER, stroke_width=2),
                     run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat7_challenge(self):
        """Beat 7: YOUR TURN -- identify the property for 3 quick tests.
        Follows the series pattern: questions in a bottom box, round
        THINK badge at board centre dims the whole board except itself."""
        with self.voiceover(text=NARRATION["beat7_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", size=30, weight="BOLD",
                                 color=CHALK_PINK).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.6, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            box_y = BOARD_CY - 0.3
            # Sized to snugly fit the widest row (number + equation, or the
            # widest reveal tag) instead of a wide box with a huge empty
            # gap between the left-anchored number and the board-centre
            # equation.
            box = RoundedRectangle(width=5.6, height=4.6, corner_radius=0.16,
                                    stroke_color=CHALK_CYAN, stroke_width=2,
                                    fill_color="#1E2A1A", fill_opacity=0.3).move_to(
                np.array([BOARD_CX, box_y, 0]))
            num_x = box.get_left()[0] + 0.4
            row_gap = 1.5

            n1 = board_text("1.", size=22, weight="BOLD", color=CHALK_AMBER).move_to(
                np.array([num_x, box_y + row_gap, 0]))
            t1 = chalk_math(r"5 \; + \; 3 \; = \; 3 \; + \; 5", size=28,
                            color=CHALK_WHITE).next_to(n1, RIGHT, buff=0.35)
            self.play(Create(box), FadeIn(n1), FadeIn(t1), run_time=rt(tracker.time_until_bookmark("b1")))

            n2 = board_text("2.", size=22, weight="BOLD", color=CHALK_AMBER).move_to(
                np.array([num_x, box_y, 0]))
            t2 = chalk_math(r"(2 \; + \; 3) \; + \; 4 \; = \; 2 \; + \; (3 \; + \; 4)", size=22,
                            color=CHALK_WHITE).next_to(n2, RIGHT, buff=0.35)
            self.play(FadeIn(n2), FadeIn(t2), run_time=rt(tracker.time_until_bookmark("b2")))

            n3 = board_text("3.", size=22, weight="BOLD", color=CHALK_AMBER).move_to(
                np.array([num_x, box_y - row_gap, 0]))
            t3 = chalk_math(r"3 \; + \; 4 \; = \; 7", size=28,
                            color=CHALK_WHITE).next_to(n3, RIGHT, buff=0.35)
            self.play(FadeIn(n3), FadeIn(t3), run_time=rt(tracker.time_until_bookmark("b3")))

            self.play(Indicate(box, color=CHALK_AMBER, scale_factor=1.02),
                     run_time=rt(tracker.time_until_bookmark("b4")))

            self._capture_srt(tracker)

        # Consistent 10-second challenge clock (whole series): a round
        # THINK badge at board centre dims the WHOLE board (question box
        # included) except itself while students think.
        play_challenge_countdown(self, seconds=10, sfx=self.sfx)

        with self.voiceover(text=NARRATION["beat7_reveal"]) as tracker:
            # The three tests stay on screen (the box already fills the
            # board) -- each gets an answer tag written just below it so
            # the reveal keeps using the same space instead of emptying it.
            tag_gap = 0.5
            ans1 = board_text("-> Commutative! (changed the order)", size=17,
                              weight="BOLD", color=CHALK_PINK).move_to(
                np.array([BOARD_CX + 0.2, box_y + row_gap - tag_gap, 0]))
            self.play(Write(ans1), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            ans2 = board_text("-> Associative! (changed grouping)", size=17,
                              weight="BOLD", color=CHALK_AMBER).move_to(
                np.array([BOARD_CX + 0.2, box_y - tag_gap, 0]))
            self.play(Write(ans2), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            ans3 = board_text("-> Closure! (stayed in the set)", size=17,
                              weight="BOLD", color=CHALK_CYAN).move_to(
                np.array([BOARD_CX + 0.2, box_y - row_gap - tag_gap, 0]))
            self.play(Write(ans3), run_time=rt(tracker.time_until_bookmark("b2")))
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

    def beat8_summary(self) -> None:
        """Closing screen -- same "Thank You for Watching!" template used
        across the whole Story-Mode series."""
        with self.voiceover(text=NARRATION["summary"]) as tracker:
            self.reset_board()

            heading = board_text("Summary", 34, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.4, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            bullets = VGroup(
                self.bullet_row(1, ["Closure: a + b, a x b stay",
                                     "in the same set"], color=CHALK_CYAN),
                self.bullet_row(2, ["Commutative: a + b = b + a",
                                     "a x b = b x a"], color=CHALK_PINK),
                self.bullet_row(3, ["Associative: (a+b)+c = a+(b+c)",
                                     "(axb)xc = ax(bxc)"], color=CHALK_AMBER),
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

            recap = board_text("Stay  •  Swap  •  Regroup", size=24, weight="BOLD",
                               color=CHALK_YELLOW).next_to(bullets, DOWN, buff=0.4)
            self.play(FadeIn(recap, shift=UP * 0.1), run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["ding"], gain=-13)

            summary_group = VGroup(heading, bullets, recap)
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
        out_dir = _HERE / "media" / "videos" / "properties_of_rational_numbers_story"
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
        "What rules do numbers follow when we add, subtract, multiply, "
        "or divide them?<bookmark mark='b0'/> Let's explore the "
        "Properties of Rational Numbers<bookmark mark='b1'/> — Closure, "
        "Commutative, and Associative!<bookmark mark='b2'/>"
    ),
    "beat1": (
        "Three properties. Three simple tips.<bookmark mark='b0'/> "
        "Closure stays inside the set.<bookmark mark='b1'/> "
        "Commutative asks: can we change the order?<bookmark mark='b2'/> "
        "Associative asks: can we change the grouping?<bookmark mark='b3'/>"
    ),
    "beat2": (
        "Every property describes how numbers behave under an operation."
        "<bookmark mark='b0'/> Take a, b, and c, with an operation like "
        "addition.<bookmark mark='b1'/> Closure: does the result stay "
        "inside the set?<bookmark mark='b2'/> Commutative: can we "
        "change the order?<bookmark mark='b3'/> Associative: can we "
        "change the grouping?<bookmark mark='b4'/> These three "
        "questions guide everything that follows.<bookmark mark='b5'/>"
    ),
    "beat3": (
        "Let's test Closure first.<bookmark mark='b0'/> Adding two "
        "whole numbers, like 3 plus 4, gives 7 — still a whole number."
        "<bookmark mark='b1'/> The result stays right inside the set!"
        "<bookmark mark='b2'/> But watch: 5 minus 6 gives negative 1"
        "<bookmark mark='b3'/> — and that's NOT a whole number. "
        "Closure depends on the operation.<bookmark mark='b4'/>"
    ),
    "beat4": (
        "Now, Commutative: does changing the order change the result?"
        "<bookmark mark='b0'/> Five plus three equals eight."
        "<bookmark mark='b1'/> Swap it: three plus five also equals "
        "eight!<bookmark mark='b2'/> Order doesn't matter for addition."
        "<bookmark mark='b3'/> The same rule holds for multiplication: "
        "a plus b equals b plus a, and a times b equals b times a."
        "<bookmark mark='b4'/> But try subtraction: five minus three is "
        "two, while three minus five is negative two.<bookmark mark='b5'/> "
        "Subtraction is NOT commutative!<bookmark mark='b6'/>"
    ),
    "beat5": (
        "Finally, Associative: does regrouping change the result?"
        "<bookmark mark='b0'/> Take two plus three, plus four."
        "<bookmark mark='b1'/> Group the first two: that's five, plus "
        "four, which is nine.<bookmark mark='b2'/> Now move the "
        "brackets: two, plus three plus four, still nine!"
        "<bookmark mark='b3'/> Grouping doesn't matter for addition."
        "<bookmark mark='b4'/> The same rule holds for multiplication: "
        "open bracket a times b close bracket times c equals a times "
        "open bracket b times c close bracket.<bookmark mark='b5'/> "
        "But subtraction fails again: five minus three, minus one, is "
        "one, while five minus the quantity three minus one, is three."
        "<bookmark mark='b6'/> Subtraction is NOT associative!"
        "<bookmark mark='b7'/>"
    ),
    "beat6": (
        "Let's put all three side by side.<bookmark mark='b0'/> "
        "Closure checks the result: does it stay inside the set?"
        "<bookmark mark='b1'/> Commutative checks the order: can we "
        "change it?<bookmark mark='b2'/> Associative checks the "
        "grouping: can we regroup?<bookmark mark='b3'/> Three "
        "different questions, three different tests.<bookmark mark='b4'/>"
    ),
    "beat7_setup": (
        "Now it's your turn — identify the property!<bookmark mark='b0'/> "
        "Test one: 5 plus 3 equals 3 plus 5.<bookmark mark='b1'/> Test "
        "two: open bracket 2 plus 3 close bracket, plus 4, equals 2, "
        "plus open bracket 3 plus 4 close bracket.<bookmark mark='b2'/> "
        "Test three: 3 plus 4 equals 7.<bookmark mark='b3'/> Which "
        "property does each one test?<bookmark mark='b4'/>"
    ),
    "beat7_reveal": (
        "Test one changed the order — that's Commutative!"
        "<bookmark mark='b0'/> Test two changed the grouping — that's "
        "Associative!<bookmark mark='b1'/> Test three checked if the "
        "result stays inside the set — that's Closure!<bookmark mark='b2'/>"
    ),
    "summary": (
        "Let's lock in the three tests, with their formulas."
        "<bookmark mark='b1'/> Closure: a plus b, and a times b, stay "
        "in the same set.<bookmark mark='b2'/> Commutative: a plus b "
        "equals b plus a, and a times b equals b times a."
        "<bookmark mark='b3'/> Associative: open bracket a plus b "
        "close bracket plus c, equals a plus open bracket b plus c "
        "close bracket — and the same for multiplication."
        "<bookmark mark='b4'/> Remember: Stay, Swap, Regroup."
        "<bookmark mark='b5'/> Thank you so much for watching, and I "
        "will see you in the next lesson!"
    ),
}


if __name__ == "__main__":
    pass

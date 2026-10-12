"""
Identities & Inverses -- "What Brings You Back?"
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

Topic: Identity = changes nothing (Addition -> 0, Multiplication -> 1).
Inverse = brings a pair together into that special result. Production
rule: for identities the second number visually disappears without
changing the original; for inverses the two numbers physically move
together and collapse into 0 or 1.

Title + 7 beats + closing summary:
  0. Title card -- IDENTITY vs INVERSE cards.
  1. Additive Identity -- 3/5+0=3/5 via an operation-machine diagram.
  2. Multiplicative Identity -- 3/7x1=3/7.
  3. Identity Comparison -- side by side, "Add 0. Multiply by 1."
  4. Additive Inverse -- 3+(-3)=0, 2/3+(-2/3)=0.
  5. Multiplicative Inverse -- 2/7x7/2=1.
  6. The Zero Trap -- 0 has no multiplicative inverse.
  7. Challenge -- classify 4 statements (round THINK badge, whole-board
     dim, full-space bottom box).
  8. Summary -- four boxed rules + Thank You card.
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
    Rectangle, RoundedRectangle, Polygon, Arrow, Text, Write, FadeIn, FadeOut,
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


def operation_machine(symbol: str = "+", color: str = CHALK_AMBER) -> VGroup:
    """A small "machine" built from real shapes -- a funnel intake, a
    boxy body with a gear-dial and the operation symbol on its front
    panel, and a chute outlet -- instead of a plain box labelled
    "machine". Positioned around its own local origin so callers can
    `.move_to(...)` the whole assembly; `.get_top()` / `.get_bottom()`
    land on the funnel mouth / chute mouth for arrow hookups."""
    body_w, body_h = 3.0, 1.5
    body = RoundedRectangle(width=body_w, height=body_h, corner_radius=0.16,
                             stroke_color=color, stroke_width=2.5,
                             fill_color="#2A1E10", fill_opacity=0.4)

    funnel = Polygon(
        np.array([-body_w * 0.28, body_h / 2, 0]),
        np.array([body_w * 0.28, body_h / 2, 0]),
        np.array([body_w * 0.1, body_h / 2 + 0.3, 0]),
        np.array([-body_w * 0.1, body_h / 2 + 0.3, 0]),
        stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.15,
    )
    chute = Polygon(
        np.array([-body_w * 0.1, -body_h / 2, 0]),
        np.array([body_w * 0.1, -body_h / 2, 0]),
        np.array([body_w * 0.22, -body_h / 2 - 0.28, 0]),
        np.array([-body_w * 0.22, -body_h / 2 - 0.28, 0]),
        stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.15,
    )

    # A dial/gear face on the left of the panel -- a ring with tick
    # marks and a needle, like a control gauge.
    dial_center = LEFT * 0.85
    dial = Circle(radius=0.26, stroke_color=color, stroke_width=2.2,
                  fill_color="#1A140A", fill_opacity=0.6).move_to(dial_center)
    dial_ticks = VGroup(*[
        Line(dial_center + 0.18 * np.array([np.cos(a), np.sin(a), 0]),
             dial_center + 0.26 * np.array([np.cos(a), np.sin(a), 0]),
             stroke_color=color, stroke_width=1.5)
        for a in np.linspace(0, 2 * np.pi, 8, endpoint=False)
    ])
    needle = Line(dial_center, dial_center + 0.19 * np.array([np.cos(1.0), np.sin(1.0), 0]),
                  stroke_color=CHALK_YELLOW, stroke_width=2)

    lights = VGroup(
        Dot(radius=0.05, color=CHALK_GREEN).move_to(RIGHT * 0.35 + UP * 0.4),
        Dot(radius=0.05, color=CHALK_RED).move_to(RIGHT * 0.6 + UP * 0.4),
    )
    op_panel = RoundedRectangle(width=0.6, height=0.5, corner_radius=0.06,
                                 stroke_color=color, stroke_width=1.5,
                                 fill_color="#1A140A", fill_opacity=0.6).move_to(RIGHT * 0.75 + DOWN * 0.15)
    op_lbl = MathTex(symbol, font_size=30, color=CHALK_WHITE).move_to(op_panel.get_center())

    return VGroup(chute, body, funnel, dial, dial_ticks, needle, lights, op_panel, op_lbl)


class IdentitiesInversesStory(VoiceoverScene):
    """9-beat Manim lesson on additive/multiplicative identities and
    inverses of rational numbers."""

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
        # This replaces the old topic-label "Identity/Inverse" left badge
        # with the dhimantAI brand badge used across the rest of the series.
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
        self.beat1_additive_identity()
        self.beat2_multiplicative_identity()
        self.beat3_comparison()
        self.beat4_additive_inverse()
        self.beat5_multiplicative_inverse()
        self.beat6_zero_trap()
        self.beat7_challenge()
        self.beat8_summary()

        self._write_real_srt()

    # ================================================================ beats ==

    def beat0_title(self):
        """Title card -- the title writes immediately as narration starts
        (no blank-board wait), then IDENTITY vs INVERSE preview cards."""
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Identities & Inverses", size=36, weight="BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.6, 0]))
            self.play(Write(title), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            subtitle = board_text("What Brings You Back?", size=22, color=CHALK_CYAN).next_to(
                title, DOWN, buff=0.25)
            self.play(Write(subtitle), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            card_w, card_h = 3.2, 1.9
            id_card = RoundedRectangle(width=card_w, height=card_h, corner_radius=0.14,
                                       stroke_color=CHALK_CYAN, stroke_width=2.5,
                                       fill_color="#1E2A2A", fill_opacity=0.3).move_to(
                np.array([BOARD_CX - 2.1, BOARD_CY - 0.4, 0]))
            id_lbl = board_text("IDENTITY", size=24, weight="BOLD", color=CHALK_CYAN).move_to(
                id_card.get_center() + UP * 0.5)
            id_sub = board_text("Changes nothing", size=17, color=CHALK_WHITE).move_to(
                id_card.get_center() + DOWN * 0.35)
            id_group = VGroup(id_card, id_lbl, id_sub)
            self.play(Create(id_card), Write(id_lbl), FadeIn(id_sub),
                     run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["pop"], gain=-14)

            inv_card = RoundedRectangle(width=card_w, height=card_h, corner_radius=0.14,
                                        stroke_color=CHALK_PINK, stroke_width=2.5,
                                        fill_color="#2A1E2A", fill_opacity=0.3).move_to(
                np.array([BOARD_CX + 2.1, BOARD_CY - 0.4, 0]))
            inv_lbl = board_text("INVERSE", size=24, weight="BOLD", color=CHALK_PINK).move_to(
                inv_card.get_center() + UP * 0.5)
            inv_sub = board_text("Brings you back", size=17, color=CHALK_WHITE).move_to(
                inv_card.get_center() + DOWN * 0.35)
            self.play(Create(inv_card), Write(inv_lbl), FadeIn(inv_sub),
                     run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["pop"], gain=-14)

            ops = chalk_math(r"+ \quad \text{and} \quad \times", size=30, color=CHALK_YELLOW).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.6, 0]))
            self.play(FadeIn(ops, shift=UP * 0.15), run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat1_additive_identity(self):
        """Beat: 3/5+0=3/5 via an operation-machine diagram."""
        with self.voiceover(text=NARRATION["additive_identity"]) as tracker:
            self.reset_board()

            # size=20, not 22 -- at 22 this heading's right edge crosses
            # into the "Mathematics" corner badge (it's the widest heading
            # in the lesson); 20 clears it with the same margin the other
            # near-boundary headings in this file use.
            heading = board_text("Additive Identity: The Do-Nothing Number", size=20, weight="BOLD",
                                 color=CHALK_CYAN).move_to(np.array([BOARD_CX, BOARD_TOP - 0.55, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            expr = chalk_math(r"\frac35+0", size=44, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_CY + 1.5, 0]))
            self.play(Write(expr), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            machine = operation_machine("+").move_to(np.array([BOARD_CX, BOARD_CY - 0.1, 0]))
            arrow_in = Arrow(expr.get_bottom() + DOWN * 0.05, machine.get_top(),
                             color=CHALK_AMBER, stroke_width=3, buff=0.05)
            self.play(Create(machine), GrowArrow(arrow_in),
                     run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            result = chalk_math(r"\frac35", size=44, color=CHALK_GREEN).move_to(
                np.array([BOARD_CX, BOARD_CY - 1.7, 0]))
            arrow_out = Arrow(machine.get_bottom(), result.get_top() + UP * 0.05,
                              color=CHALK_AMBER, stroke_width=3, buff=0.05)
            self.play(GrowArrow(arrow_out), Write(result), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self.play(Indicate(result, color=CHALK_GREEN, scale_factor=1.1), run_time=rt(MIN_RT))

            note = board_text("Adding 0 changes nothing.", size=18, color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_CY - 2.5, 0]))
            formula = chalk_math(r"a+0=a", size=22, color=CHALK_YELLOW).next_to(note, RIGHT, buff=0.5)
            self.play(FadeIn(note), Write(formula), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat2_multiplicative_identity(self):
        """Beat: 3/7x1=3/7."""
        with self.voiceover(text=NARRATION["multiplicative_identity"]) as tracker:
            self.reset_board()

            heading = board_text("Multiplicative Identity", size=26, weight="BOLD",
                                 color=CHALK_AMBER).move_to(np.array([BOARD_CX, BOARD_TOP - 0.55, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            expr = chalk_math(r"\frac37\times1", size=44, color=CHALK_WHITE)
            result = chalk_math(r"=\frac37", size=44, color=CHALK_GREEN)
            VGroup(expr, result).arrange(RIGHT, buff=0.4).move_to(np.array([BOARD_CX, BOARD_CY + 0.6, 0]))
            self.play(Write(expr), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.play(Write(result), Indicate(result, color=CHALK_GREEN, scale_factor=1.1),
                     run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            note = board_text("Multiplying by 1 changes nothing.", size=19, color=CHALK_AMBER).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.6, 0]))
            self.play(FadeIn(note), run_time=rt(tracker.time_until_bookmark("b3")))

            formula = chalk_math(r"a\times1=a", size=26, color=CHALK_YELLOW).move_to(
                np.array([BOARD_CX, BOARD_CY - 1.4, 0]))
            label = board_text("1 = Multiplicative Identity", size=18, weight="BOLD",
                               color=CHALK_AMBER).move_to(np.array([BOARD_CX, BOARD_CY - 2.15, 0]))
            self.play(Write(formula), FadeIn(label), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat3_comparison(self):
        """Beat: identity side-by-side comparison."""
        with self.voiceover(text=NARRATION["comparison"]) as tracker:
            self.reset_board()

            heading = board_text("Two \"Do-Nothing\" Numbers", size=26, weight="BOLD",
                                 color=CHALK_WHITE).move_to(np.array([BOARD_CX, BOARD_TOP - 0.55, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            left_eq = chalk_math(r"a+0=a", size=32, color=CHALK_CYAN).move_to(
                np.array([BOARD_CX - 2.3, BOARD_CY + 0.8, 0]))
            left_lbl = board_text("Identity = 0", size=20, weight="BOLD", color=CHALK_CYAN).next_to(
                left_eq, DOWN, buff=0.4)
            self.play(Write(left_eq), FadeIn(left_lbl), Indicate(left_eq, color=CHALK_CYAN),
                     run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-14)

            right_eq = chalk_math(r"a\times1=a", size=32, color=CHALK_AMBER).move_to(
                np.array([BOARD_CX + 2.3, BOARD_CY + 0.8, 0]))
            right_lbl = board_text("Identity = 1", size=20, weight="BOLD", color=CHALK_AMBER).next_to(
                right_eq, DOWN, buff=0.4)
            self.play(Write(right_eq), FadeIn(right_lbl), Indicate(right_eq, color=CHALK_AMBER),
                     run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["pop"], gain=-14)

            cue = board_text("Add 0. Multiply by 1.", size=22, weight="BOLD", color=CHALK_YELLOW).move_to(
                np.array([BOARD_CX, BOARD_CY - 1.2, 0]))
            self.play(FadeIn(cue), Circumscribe(cue, color=CHALK_YELLOW, stroke_width=2),
                     run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat4_additive_inverse(self):
        """Beat: 3+(-3)=0 and 2/3+(-2/3)=0 -- pairs physically collapse
        together into 0."""
        with self.voiceover(text=NARRATION["additive_inverse"]) as tracker:
            self.reset_board()

            heading = board_text("Additive Inverse: Cancel to Zero", size=24, weight="BOLD",
                                 color=CHALK_PINK).move_to(np.array([BOARD_CX, BOARD_TOP - 0.55, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            n3 = chalk_math("3", size=44, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX - 2.0, BOARD_CY + 1.1, 0]))
            neg3 = chalk_math("-3", size=44, color=CHALK_RED).move_to(
                np.array([BOARD_CX + 2.0, BOARD_CY + 1.1, 0]))
            self.play(FadeIn(n3), FadeIn(neg3), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-14)

            zero1 = chalk_math("0", size=44, color=CHALK_GREEN).move_to(np.array([BOARD_CX, BOARD_CY + 1.1, 0]))
            self.play(n3.animate.move_to(zero1.get_center() + LEFT * 0.01),
                     neg3.animate.move_to(zero1.get_center() + RIGHT * 0.01),
                     run_time=rt(tracker.time_until_bookmark("b2")))
            self.play(FadeOut(n3), FadeOut(neg3), FadeIn(zero1, scale=1.4),
                     Indicate(zero1, color=CHALK_GREEN), run_time=rt(MIN_RT))
            self.add_sound(self.sfx["success"], gain=-11)

            eqA = chalk_math(r"\frac23", size=34, color=CHALK_WHITE)
            plus = chalk_math("+", size=34, color=CHALK_WHITE)
            eqB = chalk_math(r"\left(-\frac23\right)", size=34, color=CHALK_RED)
            eqC = chalk_math("=0", size=34, color=CHALK_GREEN)
            row = VGroup(eqA, plus, eqB, eqC).arrange(RIGHT, buff=0.25).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.4, 0]))
            self.play(Write(eqA), Write(plus), Write(eqB), run_time=rt(tracker.time_until_bookmark("b3")))
            self.play(Write(eqC), Indicate(eqC, color=CHALK_GREEN), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)

            formula = chalk_math(r"a+(-a)=0", size=26, color=CHALK_YELLOW).move_to(
                np.array([BOARD_CX, BOARD_CY - 1.5, 0]))
            label = board_text("-a = Additive Inverse of a", size=17, weight="BOLD",
                               color=CHALK_PINK).move_to(np.array([BOARD_CX, BOARD_CY - 2.15, 0]))
            self.play(Write(formula), FadeIn(label), run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat5_multiplicative_inverse(self):
        """Beat: 2/7x7/2=1 -- reciprocal pairs collapse into 1."""
        with self.voiceover(text=NARRATION["multiplicative_inverse"]) as tracker:
            self.reset_board()

            heading = board_text("Multiplicative Inverse: Multiply to One", size=21, weight="BOLD",
                                 color=CHALK_CYAN).move_to(np.array([BOARD_CX, BOARD_TOP - 0.55, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            q = chalk_math(r"\frac27\times\ ?\ =1", size=36, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_CY + 1.2, 0]))
            self.play(Write(q), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            eqA = chalk_math(r"\frac27", size=40, color=CHALK_WHITE)
            times = chalk_math(r"\times", size=40, color=CHALK_WHITE)
            eqB = chalk_math(r"\frac72", size=40, color=CHALK_CYAN)
            eqC = chalk_math("=1", size=40, color=CHALK_GREEN)
            row = VGroup(eqA, times, eqB, eqC).arrange(RIGHT, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.1, 0]))
            self.play(FadeOut(q), FadeIn(VGroup(eqA, times, eqB)),
                     run_time=rt(tracker.time_until_bookmark("b2")))
            self.play(Write(eqC), Indicate(eqC, color=CHALK_GREEN, scale_factor=1.15),
                     run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)

            note = board_text("Reciprocals multiply to 1.", size=19, color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.9, 0]))
            formula = chalk_math(r"\frac ab\times\frac ba=1", size=24, color=CHALK_YELLOW).next_to(
                note, DOWN, buff=0.3)
            self.play(FadeIn(note), Write(formula), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat6_zero_trap(self):
        """Beat: 0 has no multiplicative inverse."""
        with self.voiceover(text=NARRATION["zero_trap"]) as tracker:
            self.reset_board()

            heading = board_text("The Zero Trap", size=30, weight="BOLD", color=CHALK_RED).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.55, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            question = chalk_math(r"0\times\ ?\ =1", size=40, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_CY + 1.2, 0]))
            self.play(Write(question), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            try1 = chalk_math(r"0\times2=0", size=28, color=CHALK_WHITE)
            try2 = chalk_math(r"0\times100=0", size=28, color=CHALK_WHITE)
            tries = VGroup(try1, try2).arrange(RIGHT, buff=0.8).move_to(np.array([BOARD_CX, BOARD_CY + 0.3, 0]))
            self.play(Write(try1), run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            self.play(Write(try2), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            always = chalk_math(r"0\times x=0", size=30, color=CHALK_RED).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.5, 0]))
            self.play(Write(always), Indicate(always, color=CHALK_RED), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            conclusion = board_text("0 has no reciprocal.", size=22, weight="BOLD", color=CHALK_RED).move_to(
                np.array([BOARD_CX, BOARD_CY - 1.4, 0]))
            undefined = chalk_math(r"\frac10\ \text{is undefined}", size=22, color=CHALK_RED).move_to(
                np.array([BOARD_CX, BOARD_CY - 2.1, 0]))
            self.play(FadeIn(conclusion), Write(undefined), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat7_challenge(self):
        """YOUR TURN -- classify 4 statements as identity or inverse.
        Follows the series pattern: full-space bordered box, round THINK
        badge at board centre, whole-board dim while it counts down."""
        box_y = BOARD_CY - 0.3
        # 4 rows + the pause label spread evenly across the box's height
        # (rather than clustered in the upper two-thirds, leaving a dead
        # empty gap at the bottom before the label).
        row_ys = [1.56, 0.78, 0.0, -0.78]
        pause_y = -1.56
        with self.voiceover(text=NARRATION["challenge_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN: Identity or Inverse?", size=26, weight="BOLD",
                                 color=CHALK_PINK).move_to(np.array([BOARD_CX, BOARD_TOP - 0.55, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            # Sized to snugly fit the widest row (number + equation +
            # reveal answer tag) instead of the old 8.8-wide box, which
            # left a large empty area to the right once the equations
            # were moved to sit right next to their numbers.
            box = RoundedRectangle(width=5.8, height=4.6, corner_radius=0.16,
                                   stroke_color=CHALK_CYAN, stroke_width=2,
                                   fill_color="#1E2A1E", fill_opacity=0.3).move_to(
                np.array([BOARD_CX, box_y, 0]))
            num_x = box.get_left()[0] + 0.4

            items = [
                (r"\frac45+0=\frac45", "1."),
                (r"\frac45+\left(-\frac45\right)=0", "2."),
                (r"\frac56\times\frac65=1", "3."),
                (r"\frac56\times1=\frac56", "4."),
            ]
            self.q_nums = []
            self.q_eqs = []
            for i, ((tex, num), y) in enumerate(zip(items, row_ys)):
                n = board_text(num, size=20, weight="BOLD", color=CHALK_AMBER).move_to(
                    np.array([num_x, box_y + y, 0]))
                # Sits right next to its number instead of near board-centre
                # -- at a fixed centre x every equation left a big empty
                # gap after the number, regardless of the number's width.
                eq = chalk_math(tex, size=26, color=CHALK_WHITE).next_to(n, RIGHT, buff=0.35)
                self.q_nums.append(n)
                self.q_eqs.append(eq)

            self.play(Create(box), run_time=rt(MIN_RT))
            for i in range(4):
                self.play(FadeIn(self.q_nums[i]), Write(self.q_eqs[i]),
                         run_time=rt(tracker.time_until_bookmark(f"b{i + 1}")))

            pause_lbl = board_text("Pause and try it!", size=17, color=CHALK_YELLOW).move_to(
                np.array([BOARD_CX, box_y + pause_y, 0]))
            self.play(FadeIn(pause_lbl), run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["pop"], gain=-14)

            self._capture_srt(tracker)

        # Consistent 10-second challenge clock (whole series): a round
        # THINK badge at board centre dims the WHOLE board (question box
        # included) except itself while students think.
        play_challenge_countdown(self, seconds=10, sfx=self.sfx)

        with self.voiceover(text=NARRATION["challenge_reveal"]) as tracker:
            self.play(FadeOut(pause_lbl), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            answers = ["Additive Identity", "Additive Inverse", "Multiplicative Inverse",
                      "Multiplicative Identity"]
            colors = [CHALK_CYAN, CHALK_PINK, CHALK_GREEN, CHALK_AMBER]
            self.a_tags = []
            for i, (ans, col, y) in enumerate(zip(answers, colors, row_ys)):
                tag = board_text(f"-> {ans}", size=17, weight="BOLD", color=col).next_to(
                    self.q_eqs[i], RIGHT, buff=0.3)
                self.a_tags.append(tag)
                self.play(Write(tag), run_time=rt(tracker.time_until_bookmark(f"b{i}")))
                self.add_sound(self.sfx["ding"] if i % 2 == 0 else self.sfx["success"], gain=-12)

            self.challenge_group = VGroup(heading, box, *self.q_nums, *self.q_eqs, *self.a_tags)
            self._capture_srt(tracker)

        self.play(FadeOut(self.challenge_group))

    def bullet_row(self, n: int, lines: list[str], *, color: str = CHALK_CYAN) -> VGroup:
        badge = Circle(radius=0.19, stroke_color=color, stroke_width=2,
                        fill_color=color, fill_opacity=0.18)
        num = board_text(str(n), 18, color, "BOLD").move_to(badge.get_center())
        text_block = VGroup(*[board_text(t, 20, CHALK_WHITE) for t in lines]).arrange(
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

            bullets = VGroup(
                self.bullet_row(1, ["Additive Identity: a + 0 = a"], color=CHALK_CYAN),
                self.bullet_row(2, ["Multiplicative Identity: a x 1 = a"], color=CHALK_AMBER),
                self.bullet_row(3, ["Additive Inverse: a + (-a) = 0"], color=CHALK_PINK),
                self.bullet_row(4, ["Multiplicative Inverse: a x 1/a = 1"], color=CHALK_GREEN),
            )
            bullets.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
            bullets.move_to(np.array([BOARD_CX, BOARD_CY + 0.3, 0]))

            self.play(FadeIn(bullets[0], shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.4))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(bullets[1], shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(bullets[2], shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(bullets[3], shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            cue = board_text("Identity: changes nothing.  Inverse: brings you back.", size=17,
                             weight="BOLD", color=CHALK_YELLOW).next_to(bullets, DOWN, buff=0.4)
            self.play(FadeIn(cue, shift=UP * 0.1), run_time=rt(tracker.time_until_bookmark("b5")))
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
        out_dir = _HERE / "media" / "videos" / "identities_inverses_story"
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
        "What brings a number back to where it started?<bookmark mark='b0'/> "
        "Identities & Inverses.<bookmark mark='b1'/> What Brings You Back?"
        "<bookmark mark='b2'/> Identity means it changes nothing."
        "<bookmark mark='b3'/> Inverse means it brings you back to a "
        "special result.<bookmark mark='b4'/> We'll explore this through "
        "addition and multiplication.<bookmark mark='b5'/>"
    ),
    "additive_identity": (
        "Let's build the idea of identity, starting simple.<bookmark mark='b0'/> "
        "Take three-fifths, plus zero.<bookmark mark='b1'/> Send it "
        "through the addition machine.<bookmark mark='b2'/> Out comes "
        "three-fifths again — completely unchanged!<bookmark mark='b3'/> "
        "Adding zero changes nothing — that's why zero is the additive "
        "identity.<bookmark mark='b4'/>"
    ),
    "multiplicative_identity": (
        "Multiplication has its own do-nothing number too.<bookmark mark='b0'/> "
        "Three-sevenths, times one.<bookmark mark='b1'/> The result is "
        "still three-sevenths!<bookmark mark='b2'/> Multiplying by one "
        "changes nothing.<bookmark mark='b3'/> That's why one is the "
        "multiplicative identity.<bookmark mark='b4'/>"
    ),
    "comparison": (
        "Let's compare the two, so we never mix them up.<bookmark mark='b0'/> "
        "For addition, the identity is zero.<bookmark mark='b1'/> For "
        "multiplication, the identity is one.<bookmark mark='b2'/> "
        "Remember it simply: add zero, multiply by one.<bookmark mark='b3'/>"
    ),
    "additive_inverse": (
        "Now, something different — the additive inverse.<bookmark mark='b0'/> "
        "Take three, and minus three.<bookmark mark='b1'/> Watch them "
        "come together and cancel out completely to zero!<bookmark mark='b2'/> "
        "It works for fractions too: two-thirds, plus minus two-thirds,"
        "<bookmark mark='b3'/> collapses straight to zero.<bookmark mark='b4'/> "
        "Any number plus its opposite always gives zero — that's the "
        "additive inverse.<bookmark mark='b5'/>"
    ),
    "multiplicative_inverse": (
        "Multiplication has its own kind of inverse too — the reciprocal."
        "<bookmark mark='b0'/> What number can multiply with two-sevenths "
        "to make one?<bookmark mark='b1'/> Try seven-halves.<bookmark mark='b2'/> "
        "Multiply them together, and you get exactly one!<bookmark mark='b3'/> "
        "Reciprocals always multiply to one — that's the multiplicative "
        "inverse.<bookmark mark='b4'/>"
    ),
    "zero_trap": (
        "But there's one crucial exception — the zero trap.<bookmark mark='b0'/> "
        "Can zero, times something, ever equal one?<bookmark mark='b1'/> "
        "Try zero times two — that's zero. Try zero times a hundred — "
        "still zero.<bookmark mark='b2'/> No matter what you multiply "
        "zero by, you always get zero.<bookmark mark='b3'/> So zero has "
        "no multiplicative inverse — one over zero is simply undefined."
        "<bookmark mark='b4'/>"
    ),
    "challenge_setup": (
        "Now it's your turn — figure out identity or inverse in each one."
        "<bookmark mark='b0'/> First, four-fifths plus zero equals "
        "four-fifths.<bookmark mark='b1'/> Second, four-fifths plus "
        "minus four-fifths equals zero.<bookmark mark='b2'/> Third, "
        "five-sixths times six-fifths equals one.<bookmark mark='b3'/> "
        "Fourth, five-sixths times one equals five-sixths."
        "<bookmark mark='b4'/> Pause the video and classify each one."
        "<bookmark mark='b5'/>"
    ),
    "challenge_reveal": (
        "The first one added zero and stayed the same — that's the "
        "Additive Identity.<bookmark mark='b0'/> The second one "
        "cancelled to zero — that's the Additive Inverse."
        "<bookmark mark='b1'/> The third one multiplied to one — that's "
        "the Multiplicative Inverse.<bookmark mark='b2'/> The fourth one "
        "multiplied by one and stayed the same — that's the "
        "Multiplicative Identity.<bookmark mark='b3'/>"
    ),
    "summary": (
        "Let's lock in the four rules.<bookmark mark='b1'/> Additive "
        "identity: a plus zero equals a. Multiplicative identity: a "
        "times one equals a.<bookmark mark='b2'/> Additive inverse: a "
        "plus minus a equals zero.<bookmark mark='b3'/> Multiplicative "
        "inverse: a times one over a equals one.<bookmark mark='b4'/> "
        "Remember: identity changes nothing, inverse brings you back."
        "<bookmark mark='b5'/> Thank you so much for watching, and I "
        "will see you in the next lesson!"
    ),
}


if __name__ == "__main__":
    pass

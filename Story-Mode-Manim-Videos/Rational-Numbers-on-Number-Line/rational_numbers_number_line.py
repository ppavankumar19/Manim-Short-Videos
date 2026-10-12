"""
Where Do Fractions Live? — Rational Numbers on a Number Line
Story-mode chalkboard lesson (Classes 6-12 Maths, primary focus Class 8).

Production pipeline (mirrors Distributive-Property-Smart-Simplification):
  - assets/background2.png chalkboard backdrop.
  - VoiceoverScene + EdgeSpeechService (en-IN-PrabhatNeural).
  - Real per-word sync via <bookmark> tags + tracker timing.
  - Ground-truth SRT from edge-tts word boundaries.
  - Hand-built chalk-style number lines (not manim's default NumberLine
    look) for visual consistency with the rest of the series.

Topic: Representation of Rational Numbers on a Number Line.
Core idea repeated throughout: denominator = equal parts, numerator =
parts counted, sign = direction. Beats:
  1. Title.
  2. Hook — measuring a length that isn't a whole number.
  3. Placement — integers and fractions share the same number line.
  4. Rule + worked example — divide 0-1 into 7 parts, count 3 (3/7).
  5. Negative example — divide -1-0 into 4 parts, count 3 left (-3/4).
  6. Real-world — a ruler, 3/4 metre.
  7. Challenge — locate -4/5 (with a real silent pause).
  8. Recap — three rules + p/q formula.
  9. Summary/outro.
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


# Board-safe rectangle (same as every Story-Mode video)
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
    """Pseudo-3D depth via a soft dark silhouette behind mobject."""
    shadow = mobj.copy()
    shadow.set_fill(BLACK, opacity=opacity)
    shadow.set_stroke(width=0)
    shadow.shift(np.array([dx, dy, 0]))
    return VGroup(shadow, mobj)


class ChalkNumberLine:
    """A bare, hand-built chalk number line over [x_min, x_max], mapped
    onto a fixed on-screen width — deliberately NOT manim's default
    NumberLine mobject, to match this series' hand-drawn look (plain
    Line + small tick marks) instead of a graphing-calculator style axis.

    By default the line gets small arrowheads at both ends -- a real
    number line extends infinitely in both directions, so an abrupt flat
    stop at the shown range reads as wrong/incomplete. Pass arrows=False
    for a bounded physical object (e.g. a 1-metre ruler) that should NOT
    imply it continues past its ends.
    """

    def __init__(self, x_min: float, x_max: float, y: float, width: float = 8.4,
                 color: str = CHALK_WHITE, stroke_width: float = 3.0,
                 arrows: bool = True):
        self.x_min = x_min
        self.x_max = x_max
        self.y = y
        self.left_pt = np.array([BOARD_CX - width / 2, y, 0])
        self.right_pt = np.array([BOARD_CX + width / 2, y, 0])
        body = Line(self.left_pt, self.right_pt, stroke_color=color,
                    stroke_width=stroke_width)
        if arrows:
            # Separate short arrows extending OUTWARD past each endpoint
            # (rather than manim's add_tip(), which retracts into the
            # line) so the tips never overlap the "parts counted"
            # highlight segments that start exactly at x_min/x_max.
            tip_len = 0.22
            right_tip = Arrow(self.right_pt, self.right_pt + RIGHT * tip_len,
                               color=color, stroke_width=stroke_width, buff=0,
                               tip_length=0.16, max_tip_length_to_length_ratio=1.0)
            left_tip = Arrow(self.left_pt, self.left_pt + LEFT * tip_len,
                              color=color, stroke_width=stroke_width, buff=0,
                              tip_length=0.16, max_tip_length_to_length_ratio=1.0)
            self.line = VGroup(body, left_tip, right_tip)
        else:
            self.line = body

    def n2p(self, x: float) -> np.ndarray:
        frac = (x - self.x_min) / (self.x_max - self.x_min)
        return self.left_pt + (self.right_pt - self.left_pt) * frac

    def tick(self, x: float, height: float = 0.14, color: str = CHALK_WHITE,
              stroke_width: float = 2.5) -> Line:
        p = self.n2p(x)
        return Line(p + UP * height, p + DOWN * height, stroke_color=color,
                    stroke_width=stroke_width)

    def subdivisions(self, denom: int, color: str = CHALK_CYAN) -> VGroup:
        """Small tick marks at every 1/denom step across the FULL range
        (excluding the two endpoints, which get their own bigger ticks)."""
        ticks = VGroup()
        for k in range(1, denom):
            x = self.x_min + k * (self.x_max - self.x_min) / denom
            ticks.add(self.tick(x, height=0.09, color=color, stroke_width=2.0))
        return ticks

    def segment(self, x_from: float, x_to: float, color: str,
                stroke_width: float = 7.0) -> Line:
        return Line(self.n2p(x_from), self.n2p(x_to), stroke_color=color,
                    stroke_width=stroke_width)


class RationalNumbersStory(VoiceoverScene):
    """9-beat Manim lesson on representing rational numbers on a number line."""

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
        self.add(self.bg, self.student, self.teacher, self.logo, self.badge)

    def construct(self):
        self.sfx = load_sfx()
        self.set_speech_service(get_speech_service(), create_subcaption=False)

        self.add_background()

        self.beat_title()
        self.beat_scene1_hook()
        self.beat_scene2_placement()
        self.beat_scene3_4_rule_and_worked()
        self.beat_scene5_negative()
        self.beat_scene6_realworld()
        self.beat_scene7_challenge()
        self.beat_scene8_recap()
        self.beat_summary()

        self._write_real_srt()

    # ================================================================ beats ==

    def beat_title(self):
        """Title card — a tiny number line with a dot sliding to a
        fractional point, teasing the whole lesson before the text."""
        with self.voiceover(text=NARRATION["title"]) as tracker:
            mini_line = Line(LEFT * 1.6, RIGHT * 1.6, stroke_color=CHALK_WHITE,
                              stroke_width=2.5).move_to(
                np.array([BOARD_CX, BOARD_TOP - 1.15, 0]))
            mini_zero = board_text("0", 20).next_to(mini_line, DOWN, buff=0.1).align_to(
                mini_line, LEFT)
            mini_one = board_text("1", 20).next_to(mini_line, DOWN, buff=0.1).align_to(
                mini_line, RIGHT)
            mini_dot = Dot(mini_line.get_left(), radius=0.08, color=CHALK_YELLOW)

            self.play(Create(mini_line), FadeIn(mini_zero), FadeIn(mini_one),
                     run_time=rt(tracker.time_until_bookmark("b0") * 0.3))
            self.play(FadeIn(mini_dot), run_time=rt(tracker.time_until_bookmark("b0") * 0.15))
            self.play(mini_dot.animate.move_to(mini_line.get_center()),
                     run_time=rt(tracker.time_until_bookmark("b0") * 0.25))
            self.add_sound(self.sfx["pop"], gain=-15)

            title = board_text("Where Do Fractions Live?", size=42, weight="BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 0.5, 0]))
            self.play(FadeOut(VGroup(mini_line, mini_zero, mini_one, mini_dot)),
                      Write(title), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            subtitle = board_text("Rational Numbers on a Number Line", size=30,
                                  color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.3, 0]))
            self.play(Write(subtitle), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat_scene1_hook(self):
        """Scene 1: A length between 0 and 1 that whole numbers can't
        describe — motivating the need for fractions."""
        with self.voiceover(text=NARRATION["scene1_hook"]) as tracker:
            self.reset_board()

            heading = board_text("MEASURING A LENGTH", size=22, color=CHALK_AMBER,
                                 weight="BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.5, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.4))

            strip_w = 8.6
            strip = RoundedRectangle(width=strip_w, height=0.9, corner_radius=0.1,
                                      stroke_color=CHALK_WHITE, stroke_width=2.5,
                                      fill_color=CHALK_AMBER, fill_opacity=0.15).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.9, 0]))
            # Small perpendicular tick marks turn the plain box into a
            # measuring tape being stretched out -- matching the "rope"
            # narration instead of reading as an empty rectangle, and
            # foreshadowing the ruler ticks used later in the lesson.
            strip_y = BOARD_CY + 0.9
            strip_ticks = VGroup(*[
                Line(np.array([BOARD_CX - strip_w / 2 + k * strip_w / 8, strip_y - 0.3, 0]),
                     np.array([BOARD_CX - strip_w / 2 + k * strip_w / 8, strip_y + 0.3, 0]),
                     stroke_color=CHALK_WHITE, stroke_width=1.5, stroke_opacity=0.55)
                for k in range(1, 8)
            ])
            self.play(Create(strip),
                      LaggedStart(*[Create(t) for t in strip_ticks], lag_ratio=0.08),
                     run_time=rt(tracker.time_until_bookmark("b0")))

            nl = ChalkNumberLine(0, 1, BOARD_CY - 0.3, width=strip_w)
            lbl0 = board_text("0", 28).next_to(nl.n2p(0), DOWN, buff=0.2)
            lbl1 = board_text("1", 28).next_to(nl.n2p(1), DOWN, buff=0.2)
            tick0 = nl.tick(0, height=0.18)
            tick1 = nl.tick(1, height=0.18)
            self.play(Create(nl.line), Create(tick0), Create(tick1),
                      FadeIn(lbl0), FadeIn(lbl1),
                     run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["swipe"], gain=-14)

            point = Dot(nl.n2p(0.62), radius=0.1, color=CHALK_PINK)
            arrow = Arrow(point.get_center() + UP * 0.7, point.get_center() + UP * 0.08,
                          color=CHALK_PINK, stroke_width=3, buff=0)
            question = board_text("What about the numbers in between?", size=24,
                                  color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.6, 0]))
            self.play(FadeIn(point), GrowArrow(arrow), Write(question),
                     run_time=rt(tracker.time_until_bookmark("b2")))

            half = chalk_math(r"\frac12", size=36, color=CHALK_YELLOW).next_to(
                nl.n2p(0.5), UP, buff=0.3)
            three_q = chalk_math(r"\frac34", size=36, color=CHALK_GREEN).next_to(
                nl.n2p(0.75), UP, buff=0.3)
            self.play(FadeIn(half), FadeIn(three_q),
                     run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat_scene2_placement(self):
        """Scene 2: A number line from -2 to 2 — integers first, then
        fractional positions (-1/2, 1/2, 3/2) settle into their places."""
        with self.voiceover(text=NARRATION["scene2_placement"]) as tracker:
            self.reset_board()

            nl = ChalkNumberLine(-2, 2, BOARD_CY, width=9.0)
            self.play(Create(nl.line), run_time=rt(tracker.time_until_bookmark("b0")))

            int_labels = VGroup()
            int_ticks = VGroup()
            for v in [-2, -1, 0, 1, 2]:
                t = nl.tick(v, height=0.16)
                lbl = board_text(str(v), 28).next_to(nl.n2p(v), DOWN, buff=0.2)
                int_ticks.add(t)
                int_labels.add(lbl)
            self.play(LaggedStart(*[Create(t) for t in int_ticks], lag_ratio=0.15),
                      LaggedStart(*[FadeIn(l) for l in int_labels], lag_ratio=0.15),
                     run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["swipe"], gain=-14)

            dot_half = Dot(nl.n2p(0.5), radius=0.11, color=CHALK_YELLOW)
            lbl_half = chalk_math(r"\frac12", size=34, color=CHALK_YELLOW).next_to(
                dot_half, UP, buff=0.2)
            self.play(FadeIn(dot_half), Write(lbl_half),
                     run_time=rt(tracker.time_until_bookmark("b2")))

            dot_neg_half = Dot(nl.n2p(-0.5), radius=0.11, color=CHALK_PINK)
            lbl_neg_half = chalk_math(r"-\frac12", size=34, color=CHALK_PINK).next_to(
                dot_neg_half, UP, buff=0.2)
            self.play(FadeIn(dot_neg_half), Write(lbl_neg_half),
                     run_time=rt(tracker.time_until_bookmark("b3")))

            dot_three_halves = Dot(nl.n2p(1.5), radius=0.11, color=CHALK_GREEN)
            lbl_three_halves = chalk_math(r"\frac32", size=34, color=CHALK_GREEN).next_to(
                dot_three_halves, UP, buff=0.2)
            self.play(FadeIn(dot_three_halves), Write(lbl_three_halves),
                     run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            caption = board_text("Every rational number has a place.", size=24,
                                 color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.5, 0]))
            self.play(Write(caption),
                      Indicate(VGroup(dot_half, dot_neg_half, dot_three_halves),
                               color=CHALK_AMBER, scale_factor=1.3),
                     run_time=rt(tracker.time_until_bookmark("b5")))

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat_scene3_4_rule_and_worked(self):
        """Scenes 3+4 combined (kept as ONE continuous diagram, per the
        storyboard's continuity note): introduce denominator/numerator on
        3/7, then immediately walk through locating it step-by-step on
        the SAME 0-1 line, so nothing is rebuilt from scratch."""
        with self.voiceover(text=NARRATION["scene3_rule"]) as tracker:
            self.reset_board()

            # Built as indexed tex parts (not a single chalk_math string) so
            # the numerator and denominator can each be highlighted on
            # their own via frac_num / frac_denom, instead of a fragile
            # get_part_by_tex lookup.
            frac = MathTex(r"\frac{", "3", "}{", "7", "}", font_size=56,
                            color=MATH_COLOR).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.9, 0]))
            frac_num, frac_denom = frac[1], frac[3]
            self.play(Write(frac), run_time=rt(tracker.time_until_bookmark("b0")))

            nl = ChalkNumberLine(0, 1, BOARD_CY - 0.5, width=8.8)
            lbl0 = board_text("0", 28).next_to(nl.n2p(0), DOWN, buff=0.2)
            lbl1 = board_text("1", 28).next_to(nl.n2p(1), DOWN, buff=0.2)
            tick0 = nl.tick(0, height=0.18)
            tick1 = nl.tick(1, height=0.18)
            self.play(Create(nl.line), Create(tick0), Create(tick1),
                      FadeIn(lbl0), FadeIn(lbl1),
                     run_time=rt(tracker.time_until_bookmark("b1") * 0.4))

            # b1->b2: "The denominator, seven, tells us how many equal
            # parts..." — divide into 7 parts, highlighting the denominator.
            subticks = nl.subdivisions(7, color=CHALK_CYAN)
            self.play(frac_denom.animate.set_color(CHALK_CYAN),
                      LaggedStart(*[Create(t) for t in subticks], lag_ratio=0.12),
                     run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["swipe"], gain=-14)
            parts_lbl = board_text("7 equal parts", size=22, color=CHALK_CYAN).next_to(
                nl.line, DOWN, buff=0.85)
            self.play(FadeIn(parts_lbl), run_time=rt(MIN_RT))

            # b2->b3: "The numerator, three, tells us how many of those
            # parts to count from zero." — highlight the numerator + first
            # three segments.
            segs = VGroup(*[nl.segment(k / 7, (k + 1) / 7, CHALK_GREEN)
                            for k in range(3)])
            self.play(frac_num.animate.set_color(CHALK_GREEN),
                      LaggedStart(*[Create(s) for s in segs], lag_ratio=0.3),
                     run_time=rt(tracker.time_until_bookmark("b3")))
            count_lbl = board_text("3 parts counted", size=22, color=CHALK_GREEN).next_to(
                parts_lbl, DOWN, buff=0.25)
            self.play(FadeIn(count_lbl), run_time=rt(MIN_RT))

            dot = Dot(nl.n2p(3 / 7), radius=0.11, color=CHALK_YELLOW)
            self.play(FadeIn(dot, scale=0.5), run_time=rt(MIN_RT))

            # b3->b4: "Denominator: equal parts. Numerator: parts
            # counted. That's the whole secret!" — settle on the summary.
            summary = VGroup(
                board_text("Denominator → equal parts", size=20, color=CHALK_CYAN),
                board_text("Numerator → parts counted", size=20, color=CHALK_GREEN),
            ).arrange(DOWN, buff=0.12).move_to(np.array([BOARD_CX, BOARD_BOTTOM + 0.5, 0]))
            self.play(FadeOut(parts_lbl), FadeOut(count_lbl), Write(summary),
                      Indicate(dot, color=CHALK_YELLOW, scale_factor=1.4),
                     run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

        # ---- continues on the SAME diagram: the step-by-step walk-through
        with self.voiceover(text=NARRATION["scene4_worked"]) as tracker:
            problem = board_text("Locate 3/7 on the number line", size=24,
                                 weight="BOLD", color=CHALK_AMBER).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.5, 0]))
            self.play(ReplacementTransform(frac, problem), FadeOut(summary),
                     run_time=rt(tracker.time_until_bookmark("b0")))

            self.play(Indicate(subticks, color=CHALK_CYAN, scale_factor=1.3),
                     run_time=rt(tracker.time_until_bookmark("b1")))
            parts_lbl2 = board_text("7 equal parts", size=22, color=CHALK_CYAN).next_to(
                nl.line, DOWN, buff=0.85)
            self.play(FadeIn(parts_lbl2), run_time=rt(MIN_RT))

            # "One... two... three." — walk a fresh marker across the
            # already-highlighted segments, one step per beat.
            walker = Dot(nl.n2p(0), radius=0.1, color=CHALK_PINK)
            self.play(FadeIn(walker), run_time=rt(tracker.time_until_bookmark("b2") * 0.3))
            for k in (1, 2, 3):
                self.play(walker.animate.move_to(nl.n2p(k / 7)),
                         run_time=rt(tracker.time_until_bookmark("b3") / 3))
                self.add_sound(self.sfx["click"], gain=-16)

            result = chalk_math(r"\frac37", size=40, color=CHALK_YELLOW).next_to(
                dot, UP, buff=0.25)
            self.play(FadeOut(walker), Write(result),
                     run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat_scene5_negative(self):
        """Scene 5: The same rule, but negative — divide -1 to 0 into 4
        parts, count 3, moving LEFT instead of right."""
        with self.voiceover(text=NARRATION["scene5_negative"]) as tracker:
            self.reset_board()

            frac = chalk_math(r"-\frac34", size=52).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.9, 0]))
            self.play(Write(frac), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            nl = ChalkNumberLine(-1, 0, BOARD_CY - 0.5, width=8.8)
            lbl_neg1 = board_text("-1", 28).next_to(nl.n2p(-1), DOWN, buff=0.2)
            lbl0 = board_text("0", 28).next_to(nl.n2p(0), DOWN, buff=0.2)
            tick_neg1 = nl.tick(-1, height=0.18)
            tick0 = nl.tick(0, height=0.18)
            self.play(Create(nl.line), Create(tick_neg1), Create(tick0),
                      FadeIn(lbl_neg1), FadeIn(lbl0),
                     run_time=rt(tracker.time_until_bookmark("b1")))

            subticks = nl.subdivisions(4, color=CHALK_CYAN)
            self.play(LaggedStart(*[Create(t) for t in subticks], lag_ratio=0.15),
                     run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["swipe"], gain=-14)
            parts_lbl = board_text("4 equal parts", size=22, color=CHALK_CYAN).next_to(
                nl.line, DOWN, buff=0.85)
            self.play(FadeIn(parts_lbl), run_time=rt(MIN_RT))

            segs = VGroup(*[nl.segment(-k / 4, -(k + 1) / 4, CHALK_PINK)
                            for k in range(3)])
            arrow = Arrow(nl.n2p(0) + UP * 0.55, nl.n2p(-0.35) + UP * 0.55,
                          color=CHALK_PINK, stroke_width=3, buff=0)
            self.play(LaggedStart(*[Create(s) for s in segs], lag_ratio=0.3),
                      GrowArrow(arrow),
                     run_time=rt(tracker.time_until_bookmark("b3")))

            dot = Dot(nl.n2p(-0.75), radius=0.11, color=CHALK_YELLOW)
            result = chalk_math(r"-\frac34", size=36, color=CHALK_YELLOW).next_to(
                dot, DOWN, buff=0.35)
            self.play(FadeIn(dot, scale=0.5), Write(result),
                     run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat_scene6_realworld(self):
        """Scene 6: A measuring ruler — locating 3/4 of a metre, the
        same division rule applied to a real measurement."""
        with self.voiceover(text=NARRATION["scene6_realworld"]) as tracker:
            self.reset_board()

            heading = board_text("MEASURING A LENGTH", size=22, color=CHALK_AMBER,
                                 weight="BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.5, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))

            ruler = RoundedRectangle(width=8.2, height=0.75, corner_radius=0.08,
                                      stroke_color=CHALK_WHITE, stroke_width=2.5,
                                      fill_color="#3A2A15", fill_opacity=0.4).move_to(
                np.array([BOARD_CX, BOARD_CY, 0]))
            self.play(Create(drop_shadow(ruler, dx=0.06, dy=-0.07, opacity=0.3)),
                     run_time=rt(tracker.time_until_bookmark("b1")))

            nl = ChalkNumberLine(0, 1, BOARD_CY, width=8.0, arrows=False)
            lbl0 = board_text("0 m", 22).next_to(nl.n2p(0), DOWN, buff=0.55)
            lbl1 = board_text("1 m", 22).next_to(nl.n2p(1), DOWN, buff=0.55)
            self.play(FadeIn(lbl0), FadeIn(lbl1),
                     run_time=rt(tracker.time_until_bookmark("b2") * 0.3))

            subticks = nl.subdivisions(4, color=CHALK_CYAN)
            self.play(LaggedStart(*[Create(t) for t in subticks], lag_ratio=0.2),
                     run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["swipe"], gain=-14)

            segs = VGroup(*[nl.segment(k / 4, (k + 1) / 4, CHALK_GREEN)
                            for k in range(3)])
            self.play(LaggedStart(*[Create(s) for s in segs], lag_ratio=0.3),
                     run_time=rt(tracker.time_until_bookmark("b3")))

            dot = Dot(nl.n2p(0.75), radius=0.1, color=CHALK_YELLOW)
            label = board_text("3/4 metre", size=26, color=CHALK_YELLOW).next_to(
                dot, UP, buff=0.35)
            self.play(FadeIn(dot, scale=0.5), Write(label),
                     run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat_scene7_challenge(self):
        """Scene 7: YOUR TURN — locate -4/5, with a genuine silent pause
        (a separate voiceover-free self.wait) before the reveal, so the
        "pause the video" instruction is honest rather than decorative.
        A wide bordered box + a full-width number line fill the board
        instead of leaving large empty margins on either side."""
        box_w, box_h = 8.8, 4.7
        box_cy = -0.15
        with self.voiceover(text=NARRATION["scene7_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", size=32, weight="BOLD",
                                 color=CHALK_PINK).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.6, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            box = RoundedRectangle(width=box_w, height=box_h, corner_radius=0.16,
                                    stroke_color=CHALK_CYAN, stroke_width=2,
                                    fill_color="#1E2A1A", fill_opacity=0.3).move_to(
                np.array([BOARD_CX, box_cy, 0]))
            challenge = chalk_math(r"-\frac45", size=64).move_to(
                np.array([BOARD_CX, box_cy + 1.55, 0]))
            self.play(Create(box), Write(challenge), run_time=rt(tracker.time_until_bookmark("b1")))

            nl = ChalkNumberLine(-1, 0, box_cy - 0.55, width=8.2)
            lbl_neg1 = board_text("-1", 26).next_to(nl.n2p(-1), DOWN, buff=0.22)
            lbl0 = board_text("0", 26).next_to(nl.n2p(0), DOWN, buff=0.22)
            tick_neg1 = nl.tick(-1, height=0.18)
            tick0 = nl.tick(0, height=0.18)
            pause_lbl = board_text("Pause and try it!", size=24, color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, box_cy - 1.9, 0]))
            self.play(Create(nl.line), Create(tick_neg1), Create(tick0),
                      FadeIn(lbl_neg1), FadeIn(lbl0), FadeIn(pause_lbl),
                     run_time=rt(tracker.time_until_bookmark("b2")))

            self._capture_srt(tracker)

        # Consistent 10-second challenge clock (whole series): the
        # background dims while the countdown runs, question stays bright.
        play_challenge_countdown(self, seconds=10, sfx=self.sfx)

        with self.voiceover(text=NARRATION["scene7_reveal"]) as tracker:
            self.play(FadeOut(pause_lbl), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            subticks = nl.subdivisions(5, color=CHALK_CYAN)
            self.play(LaggedStart(*[Create(t) for t in subticks], lag_ratio=0.15),
                     run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["swipe"], gain=-14)
            parts_lbl = board_text("5 equal parts", size=22, color=CHALK_CYAN).next_to(
                nl.line, DOWN, buff=0.85)
            self.play(FadeIn(parts_lbl), run_time=rt(MIN_RT))

            segs = VGroup(*[nl.segment(-k / 5, -(k + 1) / 5, CHALK_PINK)
                            for k in range(4)])
            self.play(LaggedStart(*[Create(s) for s in segs], lag_ratio=0.25),
                     run_time=rt(tracker.time_until_bookmark("b2")))

            dot = Dot(nl.n2p(-0.8), radius=0.13, color=CHALK_YELLOW)
            answer = chalk_math(r"-\frac45", size=50, color=CHALK_YELLOW).next_to(
                dot, UP, buff=0.3)
            self.play(FadeIn(dot, scale=0.5), Write(answer),
                     run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat_scene8_recap(self):
        """Scene 8: Three-rule recap plus the general p/q formula."""
        with self.voiceover(text=NARRATION["scene8_recap"]) as tracker:
            self.reset_board()

            heading = board_text("REPRESENTING RATIONAL NUMBERS", size=22,
                                 color=CHALK_AMBER, weight="BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.5, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))

            rules = VGroup(
                board_text("Denominator → equal parts", size=26, color=CHALK_CYAN),
                board_text("Numerator → parts counted", size=26, color=CHALK_GREEN),
                board_text("Sign → direction", size=26, color=CHALK_PINK),
            ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.4, 0]))

            self.play(FadeIn(rules[0], shift=RIGHT * 0.15),
                     run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(rules[1], shift=RIGHT * 0.15),
                     run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(rules[2], shift=RIGHT * 0.15),
                     run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            formula = chalk_math(r"\frac{p}{q},\ \ q\neq0", size=44,
                                 color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.6, 0]))
            self.play(Write(formula), Indicate(rules, color=CHALK_AMBER, scale_factor=1.02),
                     run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def bullet_row(self, n: int, lines: list[str], *, color: str = CHALK_CYAN) -> VGroup:
        badge = Circle(radius=0.19, stroke_color=color, stroke_width=2,
                        fill_color=color, fill_opacity=0.18)
        num = board_text(str(n), 18, color, "BOLD").move_to(badge.get_center())
        text_block = VGroup(*[board_text(t, 22, CHALK_WHITE) for t in lines]).arrange(
            DOWN, buff=0.06, aligned_edge=LEFT)
        row = VGroup(VGroup(badge, num), text_block).arrange(RIGHT, buff=0.3)
        VGroup(badge, num).move_to(np.array([row[0].get_x(), text_block.get_y(), 0]))
        return row

    def beat_summary(self) -> None:
        """Closing screen — same "Thank You for Watching!" template used
        across the whole Story-Mode series."""
        with self.voiceover(text=NARRATION["summary"]) as tracker:
            self.reset_board()

            heading = board_text("Summary", 34, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.4, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            bullets = VGroup(
                self.bullet_row(1, ["Denominator = equal parts of the unit"],
                                 color=CHALK_CYAN),
                self.bullet_row(2, ["Numerator = how many parts to count"],
                                 color=CHALK_GREEN),
                self.bullet_row(3, ["Positive = right, Negative = left"],
                                 color=CHALK_PINK),
                self.bullet_row(4, ["Used for 3/7, -3/4, a real ruler, and -4/5"],
                                 color=CHALK_YELLOW),
            )
            bullets.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
            bullets.move_to(np.array([BOARD_CX, BOARD_CY + 0.15, 0]))

            self.play(FadeIn(bullets[0], shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
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
        out_dir = _HERE / "media" / "videos" / "rational_numbers_number_line"
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
        "Where do fractions live on the number line?<bookmark mark='b0'/> "
        "Today we're learning how to represent rational numbers — numbers "
        "like p over q — as exact points on a number line.<bookmark mark='b1'/>"
    ),
    "scene1_hook": (
        "Imagine measuring a length with a rope.<bookmark mark='b0'/> Here's "
        "zero, and here's one whole unit.<bookmark mark='b1'/> But what if "
        "the length falls somewhere in between?<bookmark mark='b2'/> We need "
        "numbers like one-half and three-fourths to describe exactly where "
        "it lands.<bookmark mark='b3'/>"
    ),
    "scene2_placement": (
        "Every rational number has an exact place on the number line."
        "<bookmark mark='b0'/> Here are the integers: minus two, minus one, "
        "zero, one, and two.<bookmark mark='b1'/> Halfway between zero and "
        "one is one-half.<bookmark mark='b2'/> Halfway between minus one and "
        "zero is minus one-half.<bookmark mark='b3'/> And beyond one, we "
        "find three-halves.<bookmark mark='b4'/> Fractions aren't floating "
        "symbols — they live at exact points.<bookmark mark='b5'/>"
    ),
    "scene3_rule": (
        "Let's zoom into the interval from zero to one.<bookmark mark='b0'/> "
        "Look at this fraction: three-sevenths.<bookmark mark='b1'/> The "
        "denominator, seven, tells us how many equal parts to divide this "
        "unit into.<bookmark mark='b2'/> The numerator, three, tells us how "
        "many of those parts to count from zero.<bookmark mark='b3'/> "
        "Denominator: equal parts. Numerator: parts counted. That's the "
        "whole secret!<bookmark mark='b4'/>"
    ),
    "scene4_worked": (
        "Let's locate three-sevenths, step by step.<bookmark mark='b0'/> "
        "First, divide zero to one into seven equal parts.<bookmark mark='b1'/> "
        "Now, count three parts from zero.<bookmark mark='b2'/> One... "
        "two... three.<bookmark mark='b3'/> That's exactly where "
        "three-sevenths lives.<bookmark mark='b4'/>"
    ),
    "scene5_negative": (
        "What changes for a negative rational number, like minus "
        "three-fourths?<bookmark mark='b0'/> The rule is exactly the same "
        "— divide the unit into equal parts.<bookmark mark='b1'/> Here, the "
        "denominator four means four equal parts, from minus one to zero."
        "<bookmark mark='b2'/> The numerator three tells us to count three "
        "parts. But now the negative sign means we move left from zero, not "
        "right.<bookmark mark='b3'/> Same rule, opposite direction."
        "<bookmark mark='b4'/>"
    ),
    "scene6_realworld": (
        "This isn't just abstract — it's how we measure real things."
        "<bookmark mark='b0'/> Say a length measures three-fourths of a "
        "metre.<bookmark mark='b1'/> Divide the one-metre ruler into four "
        "equal parts,<bookmark mark='b2'/> and count three of them."
        "<bookmark mark='b3'/> That's exactly three-fourths of a metre — the "
        "same idea as our number line!<bookmark mark='b4'/>"
    ),
    "scene7_setup": (
        "Now it's your turn.<bookmark mark='b0'/> Try to locate minus "
        "four-fifths on the number line.<bookmark mark='b1'/> Pause the "
        "video and work it out for yourself.<bookmark mark='b2'/>"
    ),
    "scene7_reveal": (
        "Let's check your answer.<bookmark mark='b0'/> The denominator five "
        "means five equal parts, from minus one to zero.<bookmark mark='b1'/> "
        "Now count four parts, moving left because of the negative sign."
        "<bookmark mark='b2'/> One, two, three, four — there it is: minus "
        "four-fifths!<bookmark mark='b3'/>"
    ),
    "scene8_recap": (
        "Let's lock in the method with three simple rules.<bookmark mark='b0'/> "
        "Denominator tells you the number of equal parts.<bookmark mark='b1'/> "
        "Numerator tells you how many parts to count.<bookmark mark='b2'/> "
        "And the sign tells you which direction to move.<bookmark mark='b3'/> "
        "Any rational number p over q, with q not equal to zero, can be "
        "located this way.<bookmark mark='b4'/>"
    ),
    "summary": (
        "Let's recap what we learned today.<bookmark mark='b1'/> The "
        "denominator divides the unit into equal parts, and the numerator "
        "counts how many of them to take.<bookmark mark='b2'/> A positive "
        "sign moves right, a negative sign moves left.<bookmark mark='b3'/> "
        "We used this to locate three-sevenths, minus three-fourths, a real "
        "measurement, and even solved minus four-fifths together."
        "<bookmark mark='b4'/> Thank you so much for watching, and I will "
        "see you in the next lesson!"
    ),
}


if __name__ == "__main__":
    pass

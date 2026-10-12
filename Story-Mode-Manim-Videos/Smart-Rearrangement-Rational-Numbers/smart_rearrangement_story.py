"""
Smart Rearrangement — Story-mode chalkboard lesson
(Telangana Class 8 Maths, Chapter 1 — Rational Numbers).

Production pipeline (mirrors Distributive-Property-Smart-Simplification):
  - assets/background2.png chalkboard backdrop.
  - VoiceoverScene + speech service (Gemini/edge, via speech_service.py).
  - Real per-word sync via <bookmark> tags + tracker timing.
  - Ground-truth SRT from TTS word boundaries.

Topic: Using the commutative and associative properties of addition to
reorder and regroup rational numbers before calculating, so that terms
sharing a denominator land together and the arithmetic gets easier:
  0. Title — "Smart Rearrangement".
  1. History/Hook — a measurement ledger getting messy.
  2. The Long Route — plain left-to-right calculation, denominator 35
     every step.
  3. Friendly Pairs — spotting the matching denominators before
     calculating.
  4. Commutative Property — a+b=b+a, cards swap order.
  5. Associative Property — a+(b+c)=(a+b)+c, brackets slide.
  6. Apply — rearrange + group the worked example.
  7. Finish — complete the calculation, compare effort with Scene 2.
  8. Real World — net temperature change from four signed readings.
  9. Challenge — YOUR TURN, narrated setup + reveal.
  10. Recap — both properties + final answer, "Thank You" card.
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
    Create, Transform, ReplacementTransform, TransformMatchingTex,
    GrowFromCenter, GrowArrow, LaggedStart, DrawBorderThenFill, Indicate,
    config, Brace, Circumscribe, Arc, ArcBetweenPoints,
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

# Storyboard's color system: denominator-5 family -> blue, denominator-7
# family -> amber. Negative terms are additionally drawn in red text so
# a flipped sign always reads as a warning color.
DEN5_COLOR = CHALK_BLUE
DEN7_COLOR = CHALK_AMBER

END_HOLD = 2.0
TRANSITION_HOLD = 0.35
MIN_RT = 0.12


def rt(seconds: float, floor: float = MIN_RT) -> float:
    return max(floor, float(seconds))


# Board-safe rectangle (same as the rest of the series)
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


def fraction_card(latex: str, border_color: str, *, size: int = 40,
                   text_color: str = CHALK_WHITE) -> VGroup:
    """A movable "number card" -- a fraction in a rounded, colored-border
    box, per the storyboard's core visual metaphor. Border color marks
    the denominator family (blue=5, amber=7, ...); text color marks sign
    (red for negative terms)."""
    tex = chalk_math(latex, size=size, color=text_color)
    box = RoundedRectangle(width=tex.width + 0.5, height=tex.height + 0.42,
                            corner_radius=0.1, stroke_color=border_color,
                            stroke_width=2.5, fill_color=border_color,
                            fill_opacity=0.08)
    box.move_to(tex.get_center())
    card = VGroup(box, tex)
    card.box = box
    card.tex = tex
    return card


# --------------------------------------------------------- narration dict --
NARRATION = {
    "title": (
        "Smart Rearrangement.<bookmark mark='b0'/> Same numbers, a "
        "smarter order.<bookmark mark='b1'/> Let's make rational number "
        "addition easier.<bookmark mark='b2'/>"
    ),
    "scene1_ledger": (
        "Long before calculators, people combined fractional quantities "
        "by hand — in trade, measurement, and record-keeping."
        "<bookmark mark='b0'/> Here is a simple ledger of measurements."
        "<bookmark mark='b1'/> As entries pile up, the calculation "
        "starts to look messy.<bookmark mark='b2'/> Can we calculate "
        "this more cleverly?<bookmark mark='b3'/>"
    ),
    "scene2_long_route": (
        "Here is our expression.<bookmark mark='b0'/> Two fifths, plus "
        "three sevenths, minus six fifths, minus thirteen sevenths."
        "<bookmark mark='b1'/> The usual way is to work left to right, "
        "converting every pair to a common denominator of thirty five."
        "<bookmark mark='b2'/> Two fifths plus three sevenths becomes "
        "twenty nine over thirty five.<bookmark mark='b3'/> Bring in "
        "minus six fifths, and we get minus thirteen over thirty five."
        "<bookmark mark='b4'/> Finally, minus thirteen sevenths gives "
        "minus seventy eight over thirty five.<bookmark mark='b5'/> "
        "Correct — but that is a lot of repeated work.<bookmark mark='b6'/>"
    ),
    "scene3_pairs": (
        "Let's look again, before calculating.<bookmark mark='b0'/> Two "
        "of these fractions already share the same denominator — five."
        "<bookmark mark='b1'/> And two of them already share the same "
        "denominator — seven.<bookmark mark='b2'/> If we group the "
        "friendly pairs together first, the work becomes much simpler."
        "<bookmark mark='b3'/>"
    ),
    "scene4_commutative": (
        "This works because addition lets us change the order of the "
        "terms.<bookmark mark='b0'/> A plus B equals B plus A — the "
        "commutative property.<bookmark mark='b1'/> Watch two of our "
        "terms swap places without changing the total.<bookmark mark='b2'/>"
    ),
    "scene5_associative": (
        "Addition also lets us change the grouping.<bookmark mark='b0'/> "
        "Open bracket A plus B close bracket, plus C, equals A, plus "
        "open bracket B plus C close bracket — the associative property."
        "<bookmark mark='b1'/> Together, reordering and regrouping are "
        "the two moves behind smart rearrangement.<bookmark mark='b2'/>"
    ),
    "scene6_apply": (
        "Let's apply both moves to our example.<bookmark mark='b0'/> "
        "Two fifths, three sevenths, minus six fifths, minus thirteen "
        "sevenths.<bookmark mark='b1'/> Move minus six fifths next to "
        "two fifths, and minus thirteen sevenths next to three sevenths."
        "<bookmark mark='b2'/> Now group each friendly pair inside "
        "brackets.<bookmark mark='b3'/>"
    ),
    "scene7_finish": (
        "Two fifths minus six fifths gives minus four fifths, and three "
        "sevenths minus thirteen sevenths gives minus ten sevenths."
        "<bookmark mark='b0'/> There's still one common denominator "
        "step left: minus twenty eight over thirty five, minus fifty "
        "over thirty five.<bookmark mark='b1'/> That gives minus "
        "seventy eight over thirty five — the same answer, with far "
        "less work.<bookmark mark='b2'/>"
    ),
    "scene8_realworld": (
        "Here's why this matters outside the textbook.<bookmark mark='b0'/> "
        "A weather station records four temperature changes: plus one "
        "and a half, minus half, plus one and three quarters, minus "
        "three quarters degrees.<bookmark mark='b1'/> To find the net "
        "change, we can group compatible fractions regardless of the "
        "order they happened in.<bookmark mark='b2'/> One and a half "
        "minus half gives one, and one and three quarters minus three "
        "quarters gives one as well.<bookmark mark='b3'/> Together, "
        "that's a net change of two degrees Celsius.<bookmark mark='b4'/>"
    ),
    "challenge_setup": (
        "Now it's your turn.<bookmark mark='b0'/> Five eighths, minus "
        "one third, minus one eighth, plus two thirds.<bookmark mark='b1'/> "
        "Look for the friendly pairs, and try grouping them yourself."
        "<bookmark mark='b2'/>"
    ),
    "challenge_reveal": (
        "First, pair the eighths: five eighths minus one eighth gives "
        "four eighths, which simplifies to one half.<bookmark mark='b0'/> "
        "Then pair the thirds: minus one third plus two thirds gives "
        "one third.<bookmark mark='b1'/> Add those together, and one "
        "half plus one third gives five sixths.<bookmark mark='b2'/>"
    ),
    "recap": (
        "Let's remember the two moves.<bookmark mark='b0'/> A plus B "
        "equals B plus A — reorder.<bookmark mark='b1'/> A, plus open "
        "bracket B plus C close bracket, equals open bracket A plus B "
        "close bracket, plus C — regroup.<bookmark mark='b2'/> Same "
        "sum, smarter route.<bookmark mark='b3'/> Thank you so much for "
        "watching, and I will see you in the next lesson!"
    ),
}


class SmartRearrangementStory(VoiceoverScene):
    """11-beat Manim lesson on smart rearrangement of rational numbers."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._srt_entries: list[tuple[float, float, str]] = []

    # -- backdrop -----------------------------------------------------------
    def add_background(self) -> None:
        """Load the chalkboard + student/teacher art once and keep them
        alive as instance attrs, so every later `self.clear()` between
        scenes can re-add the *same* mobjects instead of reloading from
        disk."""
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
        # same visual size. This replaces the old image-based
        # "dhimantAI logo.png" badge with a text badge matching the
        # right-corner subject badge's style (rest of the series).
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
        """Wipe the previous scene's chalk content while keeping the
        background, student/teacher art, logo, and corner badge on
        screen."""
        self.clear()
        self.add(self.bg, self.student, self.teacher, self.logo, self.badge)

    def construct(self):
        self.sfx = load_sfx()
        self.set_speech_service(get_speech_service(), create_subcaption=False)

        self.add_background()

        self.beat_title()
        self.beat_scene1_ledger()
        self.beat_scene2_long_route()
        self.beat_scene3_pairs()
        self.beat_scene4_commutative()
        self.beat_scene5_associative()
        self.beat_scene6_apply()
        self.beat_scene7_finish()
        self.beat_scene8_realworld()
        self.beat_scene9_challenge()
        self.beat_recap()

        self._write_real_srt()

    # ================================================================ beats ==

    def beat_title(self):
        """Scene 0: Title card — two number cards swap places behind the
        title text as a quick visual teaser of the whole lesson."""
        with self.voiceover(text=NARRATION["title"]) as tracker:
            card_a = fraction_card("a", DEN5_COLOR, size=34)
            card_b = fraction_card("b", DEN7_COLOR, size=34)
            card_a.move_to(np.array([BOARD_CX - 0.9, BOARD_TOP - 1.15, 0]))
            card_b.move_to(np.array([BOARD_CX + 0.9, BOARD_TOP - 1.15, 0]))

            self.play(FadeIn(card_a), FadeIn(card_b),
                     run_time=rt(tracker.time_until_bookmark("b0") * 0.4))
            self.add_sound(self.sfx["pop"], gain=-15)
            self.play(
                card_a.animate.move_to(np.array([BOARD_CX + 0.9, BOARD_TOP - 1.15, 0])),
                card_b.animate.move_to(np.array([BOARD_CX - 0.9, BOARD_TOP - 1.15, 0])),
                run_time=rt(tracker.time_until_bookmark("b0") * 0.6))

            title = board_text("Smart Rearrangement", size=42, weight="BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 0.2, 0]))
            self.play(FadeOut(card_a), FadeOut(card_b), Write(title),
                     run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            tagline = board_text("Same numbers, a smarter order.",
                                 size=22, color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.7, 0]))
            self.play(FadeIn(tagline), run_time=rt(tracker.time_until_bookmark("b1")))

            self.play(Indicate(VGroup(title, tagline), color=CHALK_YELLOW,
                                scale_factor=1.03),
                     run_time=rt(tracker.time_until_bookmark("b2")))

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat_scene1_ledger(self):
        """Scene 1: A measurement ledger getting crowded with fractional
        entries -- the historical/practical hook."""
        with self.voiceover(text=NARRATION["scene1_ledger"]) as tracker:
            self.reset_board()

            heading = board_text("A calculation problem", size=24,
                                 color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.5, 0]))
            self.play(FadeIn(heading), run_time=rt(tracker.time_until_bookmark("b0")))

            # Sized to use most of the available board height between the
            # heading and the closing question, rather than a small box
            # floating in a mostly-empty board.
            ledger_w, ledger_h = 4.8, 4.0
            ledger = RoundedRectangle(width=ledger_w, height=ledger_h, corner_radius=0.1,
                                       stroke_width=2.5, stroke_color=CHALK_WHITE,
                                       fill_color="#1E2A1A", fill_opacity=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY, 0]))
            # 3 divider lines split the ledger into 4 equal ROW BANDS
            # (rather than 4 lines an entry could sit on top of) so each
            # fraction entry has clear space above and below it. Both
            # lists hold ABSOLUTE y-coordinates (BOARD_CY-based), matching
            # how the entries below are positioned.
            band_h = ledger_h / 4
            row_ys = [BOARD_CY + ledger_h / 2 - band_h * (i + 0.5) for i in range(4)]
            divider_ys = [BOARD_CY + ledger_h / 2 - band_h * i for i in range(1, 4)]
            rows = VGroup(*[
                Line(np.array([ledger.get_left()[0] + 0.25, y, 0]),
                     np.array([ledger.get_right()[0] - 0.25, y, 0]),
                     stroke_color=CHALK_WHITE, stroke_width=1, stroke_opacity=0.4)
                for y in divider_ys
            ])
            self.play(Create(drop_shadow(ledger, dx=0.07, dy=-0.08, opacity=0.3)),
                      Create(rows), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            entries_latex = [r"+\frac{2}{5}", r"+\frac{3}{7}", r"-\frac{6}{5}", r"-\frac{13}{7}"]
            entries = VGroup(*[
                chalk_math(latex, size=34, color=(CHALK_RED if latex.startswith("-") else CHALK_WHITE))
                for latex in entries_latex
            ])
            for entry, y in zip(entries, row_ys):
                entry.move_to(np.array([BOARD_CX, y, 0]))
            self.play(LaggedStart(*[FadeIn(e, shift=RIGHT * 0.15) for e in entries],
                                   lag_ratio=0.35),
                     run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            question = board_text("Can we calculate this more cleverly?",
                                  size=22, weight="BOLD", color=CHALK_AMBER).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.4, 0]))
            self.play(FadeIn(question), run_time=rt(tracker.time_until_bookmark("b3")))

            self._capture_srt(tracker)
            self.ledger_group = VGroup(heading, ledger, rows, entries, question)

        self.wait(TRANSITION_HOLD)

    def beat_scene2_long_route(self):
        """Scene 2: Plain left-to-right calculation -- denominator 35
        appears at every single step."""
        with self.voiceover(text=NARRATION["scene2_long_route"]) as tracker:
            self.reset_board()

            heading = board_text("The usual route", size=24, color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.5, 0]))
            self.play(FadeIn(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.4))

            expr = chalk_math(
                r"\frac{2}{5}+\frac{3}{7}-\frac{6}{5}-\frac{13}{7}",
                size=38, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_TOP - 1.2, 0]))
            self.play(Write(expr), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            note = board_text("Common denominator: 35", size=18,
                              color=CHALK_AMBER).move_to(
                np.array([BOARD_CX, BOARD_CY + 1.2, 0]))
            self.play(FadeIn(note), run_time=rt(tracker.time_until_bookmark("b2")))

            # Pre-arrange all three steps as one column (buff computed from
            # their real rendered heights) so consecutive stacked-fraction
            # equations never overlap, then place each one only when its
            # narration beat reaches it.
            step1 = chalk_math(r"\frac{2}{5}+\frac{3}{7}=\frac{29}{35}",
                               size=30, color=CHALK_WHITE)
            step2 = chalk_math(r"\frac{29}{35}-\frac{6}{5}=-\frac{13}{35}",
                               size=30, color=CHALK_WHITE)
            step3 = chalk_math(r"-\frac{13}{35}-\frac{13}{7}=-\frac{78}{35}",
                               size=30, color=CHALK_YELLOW)
            VGroup(step1, step2, step3).arrange(DOWN, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.45, 0]))

            self.play(Write(step1), run_time=rt(tracker.time_until_bookmark("b3")))

            self.play(ReplacementTransform(step1.copy(), step2),
                     run_time=rt(tracker.time_until_bookmark("b4")))

            self.play(ReplacementTransform(step2.copy(), step3),
                     run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["success"], gain=-11)

            tag = board_text("Correct... but a lot of work.", size=20,
                             weight="BOLD", color=CHALK_PINK).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.35, 0]))
            self.play(FadeIn(tag), Indicate(VGroup(step1, step2, step3), color=CHALK_PINK,
                                             scale_factor=1.02),
                     run_time=rt(tracker.time_until_bookmark("b6")))

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat_scene3_pairs(self):
        """Scene 3: The four original terms as cards; matching
        denominators are discovered and physically pulled together."""
        with self.voiceover(text=NARRATION["scene3_pairs"]) as tracker:
            self.reset_board()

            c1 = fraction_card(r"\frac{2}{5}", DEN5_COLOR, size=46)
            c2 = fraction_card(r"\frac{3}{7}", DEN7_COLOR, size=46)
            c3 = fraction_card(r"-\frac{6}{5}", DEN5_COLOR, size=46, text_color=CHALK_RED)
            c4 = fraction_card(r"-\frac{13}{7}", DEN7_COLOR, size=46, text_color=CHALK_RED)
            cards = VGroup(c1, c2, c3, c4).arrange(RIGHT, buff=0.6).move_to(
                np.array([BOARD_CX, BOARD_CY + 1.1, 0]))

            self.play(LaggedStart(*[FadeIn(c, scale=0.85) for c in cards], lag_ratio=0.15),
                     run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-15)

            # b0->b1: "Two of these fractions already share denominator 5."
            arc5 = ArcBetweenPoints(c1.get_top(), c3.get_top(), angle=-PI / 3,
                                     color=DEN5_COLOR, stroke_width=3)
            self.play(Indicate(c1, color=DEN5_COLOR, scale_factor=1.08),
                      Indicate(c3, color=DEN5_COLOR, scale_factor=1.08),
                      Create(arc5),
                     run_time=rt(tracker.time_until_bookmark("b1")))

            # b1->b2: "...share denominator 7."
            arc7 = ArcBetweenPoints(c2.get_top(), c4.get_top(), angle=-PI / 3,
                                     color=DEN7_COLOR, stroke_width=3)
            self.play(Indicate(c2, color=DEN7_COLOR, scale_factor=1.08),
                      Indicate(c4, color=DEN7_COLOR, scale_factor=1.08),
                      Create(arc7),
                     run_time=rt(tracker.time_until_bookmark("b2")))

            # b2->b3: cards physically slide into paired groups, spread
            # across the lower half of the board rather than clustering
            # near the vertical center. Pair spacing is derived from each
            # card's real width (like scene 6's grouping) so the larger
            # font size here can never make adjacent cards touch.
            pair_y = BOARD_CY - 1.0
            target_c1 = np.array([BOARD_CX - 2.9, pair_y, 0])
            target_c3 = target_c1 + RIGHT * (c1.width / 2 + c3.width / 2 + 0.3)
            target_c4 = np.array([BOARD_CX + 2.9, pair_y, 0])
            target_c2 = target_c4 - RIGHT * (c4.width / 2 + c2.width / 2 + 0.3)
            label = board_text("Friendly pairs", size=28, weight="BOLD",
                               color=CHALK_AMBER).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.5, 0]))
            self.play(
                FadeOut(arc5), FadeOut(arc7),
                c1.animate.move_to(target_c1),
                c3.animate.move_to(target_c3),
                c2.animate.move_to(target_c2),
                c4.animate.move_to(target_c4),
                FadeIn(label),
                run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["swipe"], gain=-14)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat_scene4_commutative(self):
        """Scene 4: Two generic cards (a, b) physically swap places to
        introduce the commutative property, then the same swap is shown
        with two real terms from the example."""
        with self.voiceover(text=NARRATION["scene4_commutative"]) as tracker:
            self.reset_board()

            heading = board_text("COMMUTATIVE PROPERTY", size=26, weight="BOLD",
                                 color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.6, 0]))
            self.play(FadeIn(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            card_a = fraction_card("a", CHALK_CYAN, size=52)
            card_b = fraction_card("b", CHALK_GREEN, size=52)
            plus = chalk_math("+", size=52, color=CHALK_WHITE)
            row = VGroup(card_a, plus, card_b).arrange(RIGHT, buff=0.4).move_to(
                np.array([BOARD_CX, BOARD_CY + 1.3, 0]))
            self.play(FadeIn(row), run_time=rt(tracker.time_until_bookmark("b0")))

            formula = chalk_math("a+b=b+a", size=48, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.2, 0]))

            left_x, right_x = card_a.get_x(), card_b.get_x()
            self.play(
                card_a.animate.move_to(np.array([right_x, card_a.get_y(), 0])),
                card_b.animate.move_to(np.array([left_x, card_b.get_y(), 0])),
                run_time=rt(tracker.time_until_bookmark("b1") * 0.6))
            self.add_sound(self.sfx["swipe"], gain=-14)
            self.play(Write(formula), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # b1->b2: swap two real terms from the worked example.
            c37 = fraction_card(r"\frac{3}{7}", DEN7_COLOR, size=44)
            c65 = fraction_card(r"-\frac{6}{5}", DEN5_COLOR, size=44, text_color=CHALK_RED)
            real_plus = chalk_math("+", size=44, color=CHALK_WHITE)
            real_row = VGroup(c37, real_plus, c65).arrange(RIGHT, buff=0.4).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.9, 0]))
            self.play(FadeOut(row), FadeOut(formula), FadeIn(real_row),
                     run_time=rt(tracker.time_until_bookmark("b2") * 0.4))
            lx, rx = c37.get_x(), c65.get_x()
            self.play(
                c37.animate.move_to(np.array([rx, c37.get_y(), 0])),
                c65.animate.move_to(np.array([lx, c65.get_y(), 0])),
                run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["swipe"], gain=-14)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat_scene5_associative(self):
        """Scene 5: Three generic cards (a, b, c) with parentheses
        sliding from one pair to the other -- the associative property."""
        with self.voiceover(text=NARRATION["scene5_associative"]) as tracker:
            self.reset_board()

            heading = board_text("ASSOCIATIVE PROPERTY", size=26, weight="BOLD",
                                 color=CHALK_PINK).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.6, 0]))
            self.play(FadeIn(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.25))

            left_expr = chalk_math("(a+b)+c", size=56, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.9, 0]))
            self.play(Write(left_expr), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            right_expr = chalk_math("a+(b+c)", size=56, color=CHALK_WHITE).move_to(
                left_expr.get_center())
            self.play(TransformMatchingTex(left_expr, right_expr),
                     run_time=rt(tracker.time_until_bookmark("b1") * 0.7))

            formula = chalk_math("(a+b)+c=a+(b+c)", size=40, color=CHALK_YELLOW).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.6, 0]))
            self.play(Write(formula), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            tags = board_text("Reorder  +  Regroup", size=26, weight="BOLD",
                              color=CHALK_AMBER).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.6, 0]))
            self.play(FadeIn(tags), Indicate(VGroup(right_expr, formula), color=CHALK_AMBER,
                                              scale_factor=1.03),
                     run_time=rt(tracker.time_until_bookmark("b2")))

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat_scene6_apply(self):
        """Scene 6: Apply both properties to the worked example -- terms
        physically reorder, then brackets grow around each friendly
        pair."""
        with self.voiceover(text=NARRATION["scene6_apply"]) as tracker:
            self.reset_board()

            tag = board_text("Reorder + Regroup", size=18, color=CHALK_AMBER).move_to(
                np.array([BOARD_RIGHT - 1.2, BOARD_TOP - 0.75, 0]))
            heading = board_text("Apply it to our example", size=26,
                                 color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.55, 0]))
            self.play(FadeIn(tag), FadeIn(heading),
                     run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            c1 = fraction_card(r"\frac{2}{5}", DEN5_COLOR, size=42)
            c2 = fraction_card(r"\frac{3}{7}", DEN7_COLOR, size=42)
            c3 = fraction_card(r"-\frac{6}{5}", DEN5_COLOR, size=42, text_color=CHALK_RED)
            c4 = fraction_card(r"-\frac{13}{7}", DEN7_COLOR, size=42, text_color=CHALK_RED)
            cards = VGroup(c1, c2, c3, c4).arrange(RIGHT, buff=0.5).move_to(
                np.array([BOARD_CX, BOARD_CY + 1.3, 0]))
            self.play(FadeIn(cards), run_time=rt(tracker.time_until_bookmark("b0")))

            # b0->b1: nothing new, hold the row while it's being named.
            self.play(Indicate(cards, color=CHALK_WHITE, scale_factor=1.02),
                     run_time=rt(tracker.time_until_bookmark("b1")))

            # b1->b2: physically move -6/5 beside 2/5, -13/7 beside 3/7.
            # Groups are pulled closer than the original card row so a "+"
            # sign fits legibly between the two bracket boxes -- without it
            # the pairs float as two disconnected chunks with no visible
            # link between them.
            gap = 0.4
            target_c1 = np.array([BOARD_CX - 1.9, BOARD_CY - 1.1, 0])
            target_c3 = target_c1 + RIGHT * (c1.width / 2 + c3.width / 2 + gap)
            target_c2 = np.array([BOARD_CX + 1.9, BOARD_CY - 1.1, 0])
            target_c4 = target_c2 + RIGHT * (c2.width / 2 + c4.width / 2 + gap)
            self.play(
                c1.animate.move_to(target_c1),
                c3.animate.move_to(target_c3),
                c2.animate.move_to(target_c2),
                c4.animate.move_to(target_c4),
                run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["swipe"], gain=-14)

            # b2->b3: grow brackets around each pair, with a "+" between
            # them so the two boxes read as one continuous expression.
            pair1_box = RoundedRectangle(
                width=(c1.width + c3.width + gap + 0.3), height=c1.height + 0.3,
                corner_radius=0.1, stroke_color=CHALK_YELLOW, stroke_width=2.5,
            ).move_to(VGroup(c1, c3).get_center())
            pair2_box = RoundedRectangle(
                width=(c2.width + c4.width + gap + 0.3), height=c2.height + 0.3,
                corner_radius=0.1, stroke_color=CHALK_YELLOW, stroke_width=2.5,
            ).move_to(VGroup(c2, c4).get_center())
            mid_plus = chalk_math("+", size=36, color=CHALK_WHITE).move_to(
                np.array([(pair1_box.get_right()[0] + pair2_box.get_left()[0]) / 2,
                          BOARD_CY - 0.3, 0]))
            self.play(Create(pair1_box), Create(pair2_box), Write(mid_plus),
                     run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self._capture_srt(tracker)
            self.pairs_state = VGroup(heading, tag, c1, c2, c3, c4, pair1_box, pair2_box,
                                       mid_plus)

        self.wait(TRANSITION_HOLD)

    def beat_scene7_finish(self):
        """Scene 7: Finish the calculation -- each pair collapses to one
        fraction, then a single common-denominator step at the end."""
        with self.voiceover(text=NARRATION["scene7_finish"]) as tracker:
            self.reset_board()

            expr = chalk_math(
                r"\left(\frac{2}{5}-\frac{6}{5}\right)+\left(\frac{3}{7}-\frac{13}{7}\right)",
                size=34, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_TOP - 1.1, 0]))
            self.play(Write(expr), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            step1 = chalk_math(r"-\frac{4}{5}", size=40, color=CHALK_CYAN).move_to(
                np.array([BOARD_CX - 1.2, BOARD_CY + 0.5, 0]))
            step2 = chalk_math(r"-\frac{10}{7}", size=40, color=CHALK_CYAN).move_to(
                np.array([BOARD_CX + 1.2, BOARD_CY + 0.5, 0]))
            self.play(FadeIn(step1), run_time=rt(tracker.time_until_bookmark("b0") * 0.5))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.play(FadeIn(step2), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            combined = chalk_math(r"-\frac{4}{5}-\frac{10}{7}=-\frac{28}{35}-\frac{50}{35}",
                                  size=34, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.5, 0]))
            self.play(ReplacementTransform(VGroup(step1, step2).copy(), combined),
                     run_time=rt(tracker.time_until_bookmark("b1")))

            final = chalk_math(r"=-\frac{78}{35}", size=48, color=CHALK_YELLOW).move_to(
                np.array([BOARD_CX, BOARD_CY - 1.5, 0]))
            self.play(FadeIn(final), run_time=rt(tracker.time_until_bookmark("b2") * 0.6))
            self.add_sound(self.sfx["success"], gain=-11)

            tag = board_text("Same value. Easier path.", size=22, weight="BOLD",
                             color=CHALK_GREEN).next_to(final, DOWN, buff=0.35)
            self.play(FadeIn(tag), Circumscribe(final, color=CHALK_YELLOW,
                                                 stroke_width=3, time_width=0.6),
                     run_time=rt(tracker.time_until_bookmark("b2")))

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat_scene8_realworld(self):
        """Scene 8: Real-world application -- four signed temperature
        readings, net change found by regrouping compatible fractions."""
        with self.voiceover(text=NARRATION["scene8_realworld"]) as tracker:
            self.reset_board()

            heading = board_text("Net Temperature Change", size=26,
                                 color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.55, 0]))
            self.play(FadeIn(heading), run_time=rt(tracker.time_until_bookmark("b0")))

            # A noticeably larger, more realistic thermometer anchors the
            # left side of the board: a tinted "glass" tube (not a flat
            # dark fill) with graduation ticks like a real instrument, a
            # bulb wide enough to read as glass-blown rather than a plain
            # dot, a rounded mercury meniscus instead of a flat-topped
            # rectangle, and a thin highlight streak for a subtle 3D sheen.
            thermo_center = np.array([BOARD_LEFT + 1.5, BOARD_CY - 0.1, 0])
            thermo_tube = RoundedRectangle(width=0.5, height=3.6, corner_radius=0.25,
                                            stroke_color=CHALK_WHITE, stroke_width=2.5,
                                            fill_color=CHALK_WHITE, fill_opacity=0.1).move_to(
                thermo_center)
            thermo_bulb = Circle(radius=0.42, stroke_color=CHALK_WHITE, stroke_width=2.5,
                                  fill_color=CHALK_RED, fill_opacity=0.85).move_to(
                thermo_tube.get_bottom())
            # Graduation ticks along the outside edge of the tube, like a
            # real calibrated thermometer -- alternating long/short marks.
            tube_right_x = thermo_center[0] + 0.25
            thermo_ticks = VGroup(*[
                Line(np.array([tube_right_x, thermo_center[1] + ty, 0]),
                     np.array([tube_right_x + (0.16 if i % 2 == 0 else 0.09),
                               thermo_center[1] + ty, 0]),
                     stroke_color=CHALK_WHITE, stroke_width=1.5, stroke_opacity=0.6)
                for i, ty in enumerate(np.linspace(-1.5, 1.5, 9))
            ])
            thermo_highlight = Line(
                thermo_tube.get_top() + LEFT * 0.12 + DOWN * 0.2,
                thermo_bulb.get_center() + UP * 0.15 + LEFT * 0.1,
                stroke_color=CHALK_WHITE, stroke_width=2, stroke_opacity=0.35,
            )
            mercury = RoundedRectangle(width=0.28, height=1.3, corner_radius=0.09,
                                        stroke_width=0, fill_color=CHALK_RED,
                                        fill_opacity=0.9).move_to(
                thermo_tube.get_bottom() + UP * 0.8)
            thermo = VGroup(thermo_tube, thermo_ticks, thermo_bulb, mercury, thermo_highlight)

            readings = VGroup(*[
                chalk_math(latex, size=30, color=(CHALK_GREEN if latex.startswith("+") else CHALK_RED))
                for latex in [r"+\frac{3}{2}", r"-\frac{1}{2}", r"+\frac{7}{4}", r"-\frac{3}{4}"]
            ]).arrange(RIGHT, buff=0.55).move_to(np.array([BOARD_CX + 1.0, BOARD_CY + 1.3, 0]))
            self.play(FadeIn(thermo), LaggedStart(*[FadeIn(r) for r in readings], lag_ratio=0.2),
                     run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            regroup = chalk_math(
                r"\left(\frac{3}{2}-\frac{1}{2}\right)+\left(\frac{7}{4}-\frac{3}{4}\right)",
                size=34, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX + 1.0, BOARD_CY + 0.3, 0]))
            self.play(Write(regroup), run_time=rt(tracker.time_until_bookmark("b2")))

            calc = chalk_math("1+1", size=42, color=CHALK_CYAN).move_to(
                np.array([BOARD_CX + 0.5, BOARD_CY - 0.8, 0]))
            self.play(ReplacementTransform(regroup.copy(), calc),
                     run_time=rt(tracker.time_until_bookmark("b3")))

            result = chalk_math(r"=2^{\circ}C", size=50, color=CHALK_YELLOW).next_to(
                calc, RIGHT, buff=0.35)
            self.play(FadeIn(result), mercury.animate.stretch_to_fit_height(2.6, about_edge=DOWN),
                     run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat_scene9_challenge(self):
        """Scene 9: YOUR TURN -- a fresh expression the student solves by
        grouping eighths and thirds. Setup and reveal are narrated; only
        the countdown itself is silent (series convention)."""
        with self.voiceover(text=NARRATION["challenge_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", size=32, weight="BOLD",
                                 color=CHALK_PINK).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.6, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            prob = chalk_math(r"\frac{5}{8}-\frac{1}{3}-\frac{1}{8}+\frac{2}{3}",
                              size=48, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_CY + 1.1, 0]))
            self.play(Write(prob), run_time=rt(tracker.time_until_bookmark("b1")))

            hint = board_text("Which terms should you group?", size=24,
                              color=CHALK_CYAN).next_to(prob, DOWN, buff=0.5)
            self.play(FadeIn(hint), run_time=rt(tracker.time_until_bookmark("b2")))

            self._capture_srt(tracker)

        play_challenge_countdown(self, seconds=8, sfx=self.sfx)

        with self.voiceover(text=NARRATION["challenge_reveal"]) as tracker:
            self.play(FadeOut(hint), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            step1 = chalk_math(r"\left(\frac{5}{8}-\frac{1}{8}\right)=\frac{1}{2}",
                               size=38, color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_CY, 0]))
            self.play(ReplacementTransform(prob.copy(), step1),
                     run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            step2 = chalk_math(r"\left(-\frac{1}{3}+\frac{2}{3}\right)=\frac{1}{3}",
                               size=38, color=CHALK_GREEN).next_to(step1, DOWN, buff=0.4)
            self.play(FadeIn(step2), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            final = chalk_math(r"\frac{1}{2}+\frac{1}{3}=\frac{5}{6}",
                               size=46, color=CHALK_YELLOW).next_to(step2, DOWN, buff=0.45)
            self.play(FadeIn(final), Circumscribe(final, color=CHALK_YELLOW,
                                                   stroke_width=3, time_width=0.6),
                     run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

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

    def beat_recap(self) -> None:
        """Closing screen -- both properties recapped, then the
        "Thank You" template shared by the rest of the series."""
        with self.voiceover(text=NARRATION["recap"]) as tracker:
            self.reset_board()

            heading = board_text("Smart Rearrangement", 32, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.4, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.5))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            bullets = VGroup(
                self.bullet_row(1, ["a + b = b + a  (reorder)"], color=CHALK_CYAN),
                self.bullet_row(2, ["a+(b+c) = (a+b)+c  (regroup)"], color=CHALK_PINK),
            )
            bullets.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
            bullets.move_to(np.array([BOARD_CX, BOARD_CY + 0.5, 0]))

            self.play(FadeIn(bullets[0], shift=RIGHT * 0.15),
                     run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(bullets[1], shift=RIGHT * 0.15),
                     run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            tagline = board_text("Same sum. Smarter route.", size=26,
                                 weight="BOLD", color=CHALK_AMBER).next_to(
                bullets, DOWN, buff=0.4)
            self.play(FadeIn(tagline, shift=UP * 0.1),
                      Indicate(bullets, color=CHALK_AMBER, scale_factor=1.02),
                     run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            summary_group = VGroup(heading, bullets, tagline)
            self.play(FadeOut(summary_group), run_time=rt(tracker.time_until_bookmark("b3") * 0.5))

            thanks = board_text("Thank You for Watching!", 42, CHALK_WHITE, "BOLD")
            thanks2 = board_text("See you in the next lesson :)", 26, CHALK_CYAN)
            thanks_group = VGroup(thanks, thanks2).arrange(DOWN, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY, 0]))
            self.play(Write(thanks), run_time=rt(tracker.time_until_bookmark("b3")))
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
        out_dir = _HERE / "media" / "videos" / "smart_rearrangement_story"
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


if __name__ == "__main__":
    pass

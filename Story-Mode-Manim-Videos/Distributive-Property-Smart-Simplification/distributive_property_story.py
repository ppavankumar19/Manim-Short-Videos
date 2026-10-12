"""
Distributive Property — Story-mode chalkboard lesson
(Telangana Classes 6–12 Maths, Chapter 1 — Rational Numbers).

Production pipeline (mirrors Simple-vs-Compound-Interest):
  - assets/background2.png chalkboard backdrop.
  - VoiceoverScene + EdgeSpeechService (en-IN-PrabhatNeural).
  - Real per-word sync via <bookmark> tags + tracker timing.
  - Ground-truth SRT from edge-tts word boundaries.
  - Realistic Manim diagrams with careful positioning to avoid overlaps.

Topic: Distributive Property of Multiplication over Addition AND
Subtraction (a(b+c)=ab+ac and a(b-c)=ab-ac), scoped for an 8th-grade
audience with concrete, relatable examples rather than heavier algebra:
  0. Title — "Distributive Property".
  1. History/Hook — Land surveyors (rectangle split visual).
  2. Intuitive — Whole = sum of parts (duplicate/split animation).
  3. Formula — a(b+c) = ab+ac and a(b-c) = ab-ac, with Brace labels.
  4. Worked Example (Addition) — 4 x 23 = 4(20+3) = 80+12 = 92.
     Worked Example (Subtraction) — 6 x 98 = 6(100-2) = 600-12 = 588.
  4b. Common Mistake — only distributing to the first term.
  5. Real-World — 5 friends buying notebooks + pens, Rs.115 total.
  6. Challenge — YOUR TURN, narrated setup + reveal + countdown.
  7. Finale — Recap the formula, then the closing "Thank You" card.
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
    Arc, Polygon,
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
TRANSITION_HOLD = 0.35  # short beat-to-beat breath, not a 2s dead-air gap
MIN_RT = 0.12


def rt(seconds: float, floor: float = MIN_RT) -> float:
    return max(floor, float(seconds))


# Board-safe rectangle (same as Simple-vs-Compound-Interest)
BOARD_LEFT = -4.6
BOARD_RIGHT = 5.6
BOARD_TOP = 3.3
BOARD_BOTTOM = -2.9
BOARD_CX = (BOARD_LEFT + BOARD_RIGHT) / 2
BOARD_CY = (BOARD_TOP + BOARD_BOTTOM) / 2

LEFT_CX = (BOARD_LEFT + BOARD_CX) / 2 - 0.3
RIGHT_CX = (BOARD_CX + BOARD_RIGHT) / 2 + 0.3


def board_text(s: str, size: int = 34, color: str = CHALK_WHITE, weight: str = "NORMAL",
               font: str = FONT) -> Text:
    return Text(s, font=font, font_size=size, color=color, weight=weight)


def chalk_math(s: str, size: int = 34, color: str = MATH_COLOR) -> MathTex:
    return MathTex(s, font_size=size, color=color)


def drop_shadow(mobj, dx: float = 0.05, dy: float = -0.06, opacity: float = 0.3):
    """Pseudo-3D depth via a soft dark silhouette behind mobject."""
    shadow = mobj.copy()
    shadow.set_fill(BLACK, opacity=opacity)
    shadow.set_stroke(width=0)
    shadow.shift(np.array([dx, dy, 0]))
    return VGroup(shadow, mobj)


def wheat_stalk(pos: np.ndarray, color: str = CHALK_YELLOW, height: float = 0.34) -> VGroup:
    """A tiny chalk-drawn wheat stalk: a stem with a row of angled ears,
    used to texture a field plot instead of a flat color wash."""
    stem = Line(ORIGIN, UP * height, stroke_color=color, stroke_width=1.6)
    ears = VGroup(*[
        Line(np.array([0, y, 0]),
             np.array([0, y, 0]) + 0.09 * np.array([np.cos(ang), np.sin(ang), 0]),
             stroke_color=color, stroke_width=1.4)
        for y in np.linspace(height * 0.35, height, 3)
        for ang in (PI * 0.2, PI * 0.8)
    ])
    # Center-anchored (not bottom-anchored) so wheat lines up with corn_cob
    # on the same grid point — previously wheat sat higher than corn within
    # each cell since only wheat was anchored by its bottom edge.
    return VGroup(stem, ears).move_to(pos)


def corn_cob(pos: np.ndarray, color: str = CHALK_GREEN, height: float = 0.3) -> VGroup:
    """A tiny chalk-drawn corn cob: an oval outline with kernel dots,
    used to texture a field plot instead of a flat color wash."""
    body = Circle(radius=height * 0.4, stroke_color=color, stroke_width=1.4,
                   fill_color=color, fill_opacity=0.12).stretch(1.7, 1)
    kernels = VGroup(*[
        Dot(np.array([0, y, 0]), radius=0.02, color=color)
        for y in np.linspace(-height * 0.28, height * 0.28, 3)
    ])
    return VGroup(body, kernels).move_to(pos)


def field_texture(rect: Rectangle, kind: str, color: str, margin: float = 0.2) -> VGroup:
    """Tile a small field-plot Rectangle with wheat stalks or corn cobs so
    it reads as an actual crop field rather than a flat color fill."""
    cx, cy = rect.get_center()[0], rect.get_center()[1]
    half_w = rect.width / 2 - margin
    half_h = rect.height / 2 - margin
    cols = max(2, int(rect.width / 0.55))
    rows = max(2, int(rect.height / 0.55))
    marks = VGroup()
    for c in np.linspace(cx - half_w, cx + half_w, cols):
        for r in np.linspace(cy - half_h, cy + half_h, rows):
            pos = np.array([c, r, 0])
            marks.add(wheat_stalk(pos, color) if kind == "wheat" else corn_cob(pos, color))
    return marks


# --------------------------------------------------------- narration dict --
NARRATION = {
    "title": (
        "Distributive Property.<bookmark mark='b0'/> One multiplier — "
        "every term inside gets it.<bookmark mark='b1'/> It's one of the "
        "most useful tricks in all of mathematics.<bookmark mark='b2'/>"
    ),
    "scene1_hook": (
        "Imagine you're an ancient land surveyor.<bookmark mark='b0'/> You have "
        "a large field divided into two sections: wheat on one side, corn on "
        "the other.<bookmark mark='b1'/> You need to know the total area. "
        "Do you measure the entire field? Or measure each section and add them? "
        "<bookmark mark='b2'/> Both give the same answer — that's our story today."
        "<bookmark mark='b3'/>"
    ),
    "scene2_intuitive": (
        "Watch this carefully.<bookmark mark='b0'/> Here's the whole field. "
        "Now let me split it into two pieces.<bookmark mark='b1'/> The yellow "
        "piece and the green piece.<bookmark mark='b2'/> If I add them back "
        "together, do I get the same total? Yes! The whole equals the sum of "
        "the parts.<bookmark mark='b3'/>"
    ),
    "scene3_formula": (
        "Let me show you this idea with letters.<bookmark mark='b0'/> Let's "
        "call the height of our rectangle 'a'.<bookmark mark='b1'/> The width "
        "of the yellow part is 'b', and the width of the green part is 'c'."
        "<bookmark mark='b2'/> The area of the whole rectangle is a times "
        "(b plus c).<bookmark mark='b3'/> The area of the yellow part is a "
        "times b, and the green part is a times c.<bookmark mark='b4'/> "
        "So: a(b+c) equals ab plus ac. That's the distributive property "
        "over addition.<bookmark mark='b5'/> The same idea also works over "
        "subtraction: a times (b minus c) equals a b minus a c."
        "<bookmark mark='b6'/>"
    ),
    "scene4_worked": (
        "Let's try this with real numbers.<bookmark mark='b0'/> What is "
        "4 times 23?<bookmark mark='b1'/> Instead of multiplying directly,"
        "<bookmark mark='b2'/> break 23 into 20 and 3.<bookmark mark='b2b'/> "
        "So we have 4 times "
        "(20 plus 3).<bookmark mark='b3'/> Distribute the 4: 4 times 20 "
        "equals 80, and 4 times 3 equals 12.<bookmark mark='b4'/> Add them: "
        "80 plus 12 equals 92.<bookmark mark='b5'/> That's the distributive "
        "property over addition.<bookmark mark='b6'/> Now let's try one "
        "over subtraction.<bookmark mark='b7'/> What is 6 times 98?"
        "<bookmark mark='b8'/> Think of 98 as 100 minus 2."
        "<bookmark mark='b8b'/> So we have 6 times (100 minus 2)."
        "<bookmark mark='b9'/> Distribute the 6: 6 times 100 equals 600, "
        "and 6 times 2 equals 12.<bookmark mark='b10'/> Subtract them: "
        "600 minus 12 equals 588.<bookmark mark='b11'/> Same trick, "
        "works either way!<bookmark mark='b12'/>"
    ),
    "scene4b_mistake": (
        "Here's a mistake many students make.<bookmark mark='b0'/> When "
        "solving 4 times (20 plus 3), some multiply only the first term."
        "<bookmark mark='b1'/> They write 4 times 20, plus 3 — forgetting "
        "to multiply the second term!<bookmark mark='b2'/> That gives 80 "
        "plus 3, which is 83 — and that's wrong.<bookmark mark='b3'/> "
        "Remember: the 4 must multiply every term inside the brackets."
        "<bookmark mark='b4'/> The correct way is 4 times 20, plus 4 times "
        "3, which gives 92.<bookmark mark='b5'/> Always distribute to "
        "every single term!<bookmark mark='b6'/>"
    ),
    "scene4c_mistake": (
        "Subtraction has its own tricky mistake.<bookmark mark='b0'/> "
        "When solving 6 times the quantity 100 minus 2, some students "
        "flip the sign.<bookmark mark='b1'/> They write 6 times 100, "
        "plus 6 times 2 — turning the minus into a plus!"
        "<bookmark mark='b2'/> That gives 600 plus 12, which is 612 — "
        "and that's wrong.<bookmark mark='b3'/> Remember: the minus "
        "sign must stay between the two distributed products."
        "<bookmark mark='b4'/> The correct way is 6 times 100, minus 6 "
        "times 2, which gives 588.<bookmark mark='b5'/> Keep the "
        "operation exactly as it was inside the brackets!"
        "<bookmark mark='b6'/>"
    ),
    "scene5_realworld": (
        "Here's a real-world example.<bookmark mark='b0'/> 5 friends each buy "
        "a notebook for 20 rupees and a pen for 3 rupees.<bookmark mark='b1'/> "
        "What's the total cost?<bookmark mark='b2'/> We can think of it as "
        "5 times (20 plus 3).<bookmark mark='b3'/> Or, buy all 5 notebooks "
        "first: 100 rupees. Then all 5 pens: 15 rupees.<bookmark mark='b4'/> "
        "Total: 115 rupees. Distribution happens naturally in everyday life!"
        "<bookmark mark='b5'/>"
    ),
    "challenge_setup": (
        "Time to try one yourself: seven times nineteen."
        "<bookmark mark='b0'/> Here's a hint — nineteen equals twenty "
        "minus one.<bookmark mark='b1'/> Take a moment here and work it "
        "out using the distributive property.<bookmark mark='b2'/>"
    ),
    "challenge_reveal": (
        "Seven times nineteen becomes seven times the quantity twenty "
        "minus one, which splits into one hundred forty minus seven, "
        "giving one hundred thirty three.<bookmark mark='b0'/> Quick "
        "mental math, all thanks to distributing.<bookmark mark='b1'/>"
    ),
    "scene7_finale": (
        "Remember: the distributive property is just breaking things apart."
        "<bookmark mark='b0'/> Wherever you see a(b+c), you can distribute — "
        "split the parts, multiply each, then add them back.<bookmark mark='b1'/> "
        "Use it for mental math, and for real-life shopping. "
        "Break it down to make it simple.<bookmark mark='b2'/>"
    ),
    "summary": (
        "Let's recap the power of breaking it apart.<bookmark mark='b1'/> "
        "Over addition: a times open bracket b plus c close bracket "
        "equals a b plus a c.<bookmark mark='b2'/> Over subtraction: a "
        "times open bracket b minus c close bracket equals a b minus a c."
        "<bookmark mark='b2b'/> We used it for quick mental math, and for "
        "splitting a real shopping bill.<bookmark mark='b3'/> Whenever a number multiplies "
        "a sum or a difference, you can distribute it across every term — "
        "break it down to make it simple.<bookmark mark='b4'/> Thank you "
        "so much for watching, and I will see you in the next lesson!"
    ),
}


class DistributivePropertyStory(VoiceoverScene):
    """7-scene Manim lesson on the distributive property."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._srt_entries: list[tuple[float, float, str]] = []

    # -- backdrop (mirrors Simple-vs-Compound-Interest) -------------------
    def add_background(self) -> None:
        """Load the chalkboard + student/teacher art once and keep them
        alive as instance attrs, so every later `self.clear()` between
        scenes can re-add the *same* mobjects instead of reloading from
        disk — and, crucially, so they never silently disappear after the
        first clear()."""
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
        # Both corner badges share the same chalk-stamped ribbon style and
        # are rendered at font_size=12 then scaled up -- manim/Pango
        # introduces visible per-glyph spacing artifacts in this font at
        # small integer font sizes above 12, but scaling the finished
        # badge (before the margin snap in _corner_badge) is artifact-free.
        # The same scale factor keeps "Mathematics" and "dhimantAI" the
        # same visual size.
        self.badge = self._corner_badge("Mathematics", corner="right",
                                         y=BOARD_TOP - 0.16, font_size=12,
                                         scale=16 / 12)
        self.logo = self._corner_badge("dhimantAI", corner="left",
                                        y=BOARD_TOP - 0.16, font_size=12,
                                        scale=16 / 12, text_color=BRAND_WHITE)

        self.add(self.bg, self.student, self.teacher, self.logo, self.badge)

    def _corner_badge(self, text: str, *, corner: str, y: float | None = None,
                       font_size: int = 13, font: str = FONT,
                       scale: float = 1.0, text_color: str = CHALK_WHITE) -> VGroup:
        """Small chalk-stamped ribbon tucked in a top corner of the board,
        staying on screen for the whole video."""
        label = board_text(text, font_size, text_color, "BOLD", font=font)
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
            # Snap the LEFT edge to the same 0.08 margin the right-corner
            # badge uses off BOARD_RIGHT, so the two badges mirror each
            # other exactly regardless of label width.
            badge.shift(RIGHT * (BOARD_LEFT + 0.08 - badge.get_left()[0]))
        else:
            badge.move_to(np.array([BOARD_RIGHT - 0.6, yy, 0]))
            # Right margin is smaller than the left corner's 0.08 to
            # compensate for the background art's perspective -- at equal
            # 0.08 margins the right badge renders with a visibly larger
            # gap to the board frame than the left badge, so it's nudged
            # right to match dhimantAI's spacing.
            badge.shift(RIGHT * (BOARD_RIGHT - 0.013 - badge.get_right()[0]))
        # Snap the TOP edge to the same 0.08 margin used horizontally, so
        # both badges sit with equal spacing from the board's edges
        # regardless of font scaling.
        badge.shift(UP * ((BOARD_TOP - 0.08) - badge.get_top()[1]))
        return badge

    def reset_board(self) -> None:
        """Wipe the previous scene's chalk content while keeping the
        background, student/teacher art, logo, and corner badge on screen."""
        self.clear()
        self.add(self.bg, self.student, self.teacher, self.logo, self.badge)

    def construct(self):
        self.sfx = load_sfx()
        self.set_speech_service(get_speech_service(), create_subcaption=False)

        self.add_background()

        # Beat sequence
        self.beat_title()
        self.beat_scene1_hook()
        self.beat_scene2_intuitive()
        self.beat_scene3_formula()
        self.beat_scene4_worked()
        self.beat_scene4b_mistake()
        self.beat_scene4c_mistake_subtraction()
        self.beat_scene5_realworld()
        self.beat_scene6b_challenge()
        self.beat_scene7_finale()
        self.beat_summary()

        # Write real SRT from captured word boundaries
        self._write_real_srt()

    # ================================================================ beats ==

    def beat_title(self):
        """Scene 0: Title card — simple and direct: just "Distributive
        Property". Opens on a tiny animated area-model icon (split-
        rectangle preview) before the text, so the video doesn't open on
        a static title screen."""
        with self.voiceover(text=NARRATION["title"]) as tracker:
            # Mini animated preview: a rectangle splitting into two colored
            # halves and sliding apart — a quick visual teaser of the whole
            # lesson before any text appears.
            mini_rect = RoundedRectangle(width=2.6, height=1.3, corner_radius=0.05,
                                          stroke_color=CHALK_WHITE, stroke_width=2).move_to(
                np.array([BOARD_CX, BOARD_TOP - 1.1, 0]))
            mini_l = Rectangle(width=1.3, height=1.3, stroke_width=0,
                                fill_color=CHALK_YELLOW, fill_opacity=0.45).move_to(
                mini_rect.get_center() + LEFT * 0.65)
            mini_r = Rectangle(width=1.3, height=1.3, stroke_width=0,
                                fill_color=CHALK_GREEN, fill_opacity=0.45).move_to(
                mini_rect.get_center() + RIGHT * 0.65)
            icon = VGroup(mini_rect, mini_l, mini_r)

            # b0 covers "Distributive Property." — icon teaser, then the
            # title itself, both inside this one short window.
            self.play(Create(mini_rect), FadeIn(mini_l), FadeIn(mini_r),
                     run_time=rt(tracker.time_until_bookmark("b0") * 0.3))
            self.add_sound(self.sfx["pop"], gain=-15)
            self.play(mini_l.animate.shift(LEFT * 0.25), mini_r.animate.shift(RIGHT * 0.25),
                     run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            title = board_text("Distributive Property", size=46, weight="BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 0.2, 0]))
            self.play(FadeOut(icon), Write(title),
                     run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # b1: "One multiplier — every term inside gets it." — the
            # core teaching idea, right when it's spoken.
            tagline = board_text("One multiplier — every term inside gets it.",
                                 size=22, color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.7, 0]))
            self.play(FadeIn(tagline), run_time=rt(tracker.time_until_bookmark("b1")))

            # b2: "It's one of the most useful tricks in all of
            # mathematics." — a closing highlight, not a frozen board.
            self.play(Indicate(VGroup(title, tagline), color=CHALK_YELLOW,
                                scale_factor=1.03),
                     run_time=rt(tracker.time_until_bookmark("b2")))

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat_scene1_hook(self):
        """Scene 1: Land surveyor problem — a large, textured crop field
        using most of the board, with measurement brackets on the left and
        bottom edges (storyboard scene 1), not a small flat-fill rectangle."""
        with self.voiceover(text=NARRATION["scene1_hook"]) as tracker:
            self.reset_board()

            # Large field plot, enlarged to use most of the board width
            rect_full = RoundedRectangle(width=6.4, height=3.4, corner_radius=0.08,
                                          stroke_width=3, stroke_color=CHALK_WHITE,
                                          fill_color="#1E2A1A", fill_opacity=0.35).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.3, 0]))
            field = drop_shadow(rect_full, dx=0.08, dy=-0.08, opacity=0.35)

            self.play(Create(field), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            divider = DashedLine(
                np.array([BOARD_CX, BOARD_CY + 2.0, 0]),
                np.array([BOARD_CX, BOARD_CY - 1.4, 0]),
                stroke_color=CHALK_WHITE, stroke_width=2.5, dash_length=0.2
            )
            # b1 covers "...divided into two sections: wheat on one side,
            # corn on the other." — so the divider, the wheat crop, and the
            # corn crop must all land INSIDE this one window, in that same
            # spoken order, not later during an unrelated sentence.
            self.play(Create(divider), run_time=rt(tracker.time_until_bookmark("b1") * 0.2))

            # Leave headroom at the top of each plot for the Wheat/Corn
            # labels, so the crop texture never sits behind the text.
            left_plot = Rectangle(width=2.9, height=2.3, stroke_width=0).move_to(
                np.array([BOARD_CX - 1.6, BOARD_CY + 0.15, 0]))
            right_plot = Rectangle(width=2.9, height=2.3, stroke_width=0).move_to(
                np.array([BOARD_CX + 1.6, BOARD_CY + 0.15, 0]))
            wheat_rows = field_texture(left_plot, "wheat", CHALK_YELLOW, margin=0.3)
            corn_rows = field_texture(right_plot, "corn", CHALK_GREEN, margin=0.3)
            label_wheat = board_text("Wheat", size=22, color=CHALK_YELLOW).move_to(
                np.array([BOARD_CX - 1.6, BOARD_CY + 1.6, 0]))
            label_corn = board_text("Corn", size=22, color=CHALK_GREEN).move_to(
                np.array([BOARD_CX + 1.6, BOARD_CY + 1.6, 0]))

            # Wheat grows in first ("wheat on one side"...)
            self.play(LaggedStart(*[GrowFromCenter(m) for m in wheat_rows], lag_ratio=0.03),
                      FadeIn(label_wheat),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.55))
            self.add_sound(self.sfx["swipe"], gain=-14)
            # ...then corn grows in second ("...corn on the other"),
            # getting whatever's left of the b1 window.
            self.play(LaggedStart(*[GrowFromCenter(m) for m in corn_rows], lag_ratio=0.03),
                      FadeIn(label_corn),
                      run_time=rt(tracker.time_until_bookmark("b1")))

            # b2 covers "You need to know the total area. Do you measure
            # the entire field, or measure each section and add them?" —
            # so the measurement brackets and the question text belong here.
            label_q = board_text("How much land total?", size=22, color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.35, 0]))
            width_brace = Brace(rect_full, DOWN, buff=0.15, color=CHALK_WHITE)
            width_label = board_text("Total Width", size=18, color=CHALK_WHITE).next_to(
                width_brace, DOWN, buff=0.1)
            height_brace = Brace(rect_full, LEFT, buff=0.15, color=CHALK_WHITE)
            height_label = board_text("Length", size=18, color=CHALK_WHITE).next_to(
                height_brace, LEFT, buff=0.1)
            self.play(FadeIn(label_q),
                     GrowFromCenter(width_brace), FadeIn(width_label),
                     GrowFromCenter(height_brace), FadeIn(height_label),
                     run_time=rt(tracker.time_until_bookmark("b2")))

            # b3: "Both give the same answer — that's our story today." —
            # a settling highlight on the whole field, not a frozen board.
            self.play(Indicate(rect_full, color=CHALK_CYAN, scale_factor=1.03),
                     run_time=rt(tracker.time_until_bookmark("b3")))

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat_scene2_intuitive(self):
        """Scene 2: Whole = sum of parts — enlarged rectangles using more
        of the board width/height."""
        with self.voiceover(text=NARRATION["scene2_intuitive"]) as tracker:
            self.reset_board()

            # First rectangle (top) — soft pseudo-3D depth via drop_shadow
            rect1 = RoundedRectangle(width=3.6, height=2.0, corner_radius=0.06,
                            stroke_width=2.5, stroke_color=CHALK_WHITE).move_to(
                np.array([BOARD_CX - 1.3, BOARD_CY + 1.3, 0]))
            rect1_shadowed = drop_shadow(rect1, dx=0.07, dy=-0.08, opacity=0.3)
            fill1_l = Rectangle(width=1.8, height=2.0, stroke_width=0,
                              fill_color=CHALK_YELLOW, fill_opacity=0.3).move_to(
                np.array([BOARD_CX - 2.2, BOARD_CY + 1.3, 0]))
            fill1_r = Rectangle(width=1.8, height=2.0, stroke_width=0,
                              fill_color=CHALK_GREEN, fill_opacity=0.3).move_to(
                np.array([BOARD_CX - 0.4, BOARD_CY + 1.3, 0]))

            self.play(Create(rect1_shadowed), FadeIn(fill1_l), FadeIn(fill1_r),
                     run_time=rt(tracker.time_until_bookmark("b0")))

            # Second rectangle (bottom, will split) — pulled in from the
            # board edge so the split pieces below have room to slide
            # apart without crossing BOARD_RIGHT or the teacher art.
            rect2 = RoundedRectangle(width=3.6, height=2.0, corner_radius=0.06,
                            stroke_width=2.5, stroke_color=CHALK_WHITE).move_to(
                np.array([BOARD_CX + 1.0, BOARD_CY - 1.1, 0]))
            rect2_shadowed = drop_shadow(rect2, dx=0.07, dy=-0.08, opacity=0.3)
            fill2_l = Rectangle(width=1.8, height=2.0, stroke_width=0,
                              fill_color=CHALK_YELLOW, fill_opacity=0.3).move_to(
                np.array([BOARD_CX + 0.1, BOARD_CY - 1.1, 0]))
            fill2_r = Rectangle(width=1.8, height=2.0, stroke_width=0,
                              fill_color=CHALK_GREEN, fill_opacity=0.3).move_to(
                np.array([BOARD_CX + 1.9, BOARD_CY - 1.1, 0]))

            self.play(Create(rect2_shadowed), FadeIn(fill2_l), FadeIn(fill2_r),
                     run_time=rt(tracker.time_until_bookmark("b1")))

            # Split the bottom rectangle — shift reduced from the original
            # 1.4 so the pieces stay inside BOARD_RIGHT (5.6) instead of
            # sliding off the board into the teacher illustration.
            self.play(
                fill2_l.animate.shift(LEFT * 1.0),
                fill2_r.animate.shift(RIGHT * 1.0),
                rect2.animate.scale(0.8),
                run_time=rt(tracker.time_until_bookmark("b2"))
            )
            self.add_sound(self.sfx["swipe"], gain=-14)

            # Text: "Whole = Sum of Parts"
            eq_text = board_text("Whole  =  Sum of Parts", size=28, color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.5, 0]))
            self.play(Write(eq_text), run_time=rt(tracker.time_until_bookmark("b3")))

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat_scene3_formula(self):
        """Scene 3: Formula a(b+c) = ab+ac — enlarged rectangle with real
        Brace labels (storyboard: braces for a, b, c) instead of floating
        letters, so the labelling reads clearly against the diagram."""
        with self.voiceover(text=NARRATION["scene3_formula"]) as tracker:
            # Clear previous elements
            self.reset_board()

            # Rectangle with labeled dimensions — enlarged, soft pseudo-3D depth
            rect = RoundedRectangle(width=5.4, height=2.8, corner_radius=0.06,
                           stroke_width=3, stroke_color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.5, 0]))
            rect_shadowed = drop_shadow(rect, dx=0.08, dy=-0.09, opacity=0.32)

            fill_l = Rectangle(width=2.7, height=2.8, stroke_width=0,
                             fill_color=CHALK_YELLOW, fill_opacity=0.25).move_to(
                np.array([BOARD_CX - 1.35, BOARD_CY + 0.5, 0]))
            fill_r = Rectangle(width=2.7, height=2.8, stroke_width=0,
                             fill_color=CHALK_GREEN, fill_opacity=0.25).move_to(
                np.array([BOARD_CX + 1.35, BOARD_CY + 0.5, 0]))

            self.play(Create(rect_shadowed), FadeIn(fill_l), FadeIn(fill_r),
                     run_time=rt(tracker.time_until_bookmark("b0")))

            # Brace + label 'a' (height)
            brace_a = Brace(rect, LEFT, buff=0.15, color=CHALK_RED)
            label_a = chalk_math("a", size=40, color=CHALK_RED).next_to(brace_a, LEFT, buff=0.1)
            self.play(GrowFromCenter(brace_a), FadeIn(label_a),
                     run_time=rt(tracker.time_until_bookmark("b1")))

            # Braces + labels 'b' and 'c' (widths) under each half
            brace_b = Brace(fill_l, DOWN, buff=0.15, color=CHALK_BLUE)
            label_b = chalk_math("b", size=40, color=CHALK_BLUE).next_to(brace_b, DOWN, buff=0.1)
            brace_c = Brace(fill_r, DOWN, buff=0.15, color=CHALK_GREEN)
            label_c = chalk_math("c", size=40, color=CHALK_GREEN).next_to(brace_c, DOWN, buff=0.1)
            self.play(GrowFromCenter(brace_b), FadeIn(label_b),
                      GrowFromCenter(brace_c), FadeIn(label_c),
                     run_time=rt(tracker.time_until_bookmark("b2")))

            # b2->b3: "The area of the whole rectangle is a times (b plus
            # c)." — still talking about the WHOLE rectangle here, so just
            # highlight it; the "ab"/"ac" area labels don't get named until
            # the *next* sentence, so they must not appear yet.
            self.play(Indicate(VGroup(rect, brace_a, label_a, brace_b, label_b,
                                       brace_c, label_c),
                                color=CHALK_WHITE, scale_factor=1.03),
                     run_time=rt(tracker.time_until_bookmark("b3")))

            # Area labels inside rectangles
            area_b = chalk_math("ab", size=36, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX - 1.35, BOARD_CY + 0.5, 0]))
            area_c = chalk_math("ac", size=36, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX + 1.35, BOARD_CY + 0.5, 0]))
            # b3->b4 covers "The area of the yellow part is a times b, and
            # the green part is a times c." — reveal 'ab' on the first half
            # (yellow), then 'ac' on the second half (green), in that order.
            self.play(FadeIn(area_b), run_time=rt(tracker.time_until_bookmark("b4") * 0.5))
            self.play(FadeIn(area_c), run_time=rt(tracker.time_until_bookmark("b4")))

            # b4->b5: "So: a(b+c) equals ab plus ac. That's the
            # distributive property over addition." — the addition form,
            # labeled so it can sit alongside the subtraction form below.
            add_label = board_text("Over Addition:", size=18, color=CHALK_CYAN)
            add_eq = chalk_math("a(b+c) = ab+ac", size=32, color=CHALK_WHITE)
            add_row = VGroup(add_label, add_eq).arrange(RIGHT, buff=0.25).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.95, 0]))
            self.play(Write(add_row), run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # b5->b6: "The same idea also works over subtraction: a times
            # (b minus c) equals a b minus a c." — the subtraction form,
            # right below, so both are visible together as the takeaway.
            sub_label = board_text("Over Subtraction:", size=18, color=CHALK_PINK)
            sub_eq = chalk_math("a(b-c) = ab-ac", size=32, color=CHALK_WHITE)
            sub_row = VGroup(sub_label, sub_eq).arrange(RIGHT, buff=0.25).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.35, 0]))
            self.play(Write(sub_row), run_time=rt(tracker.time_until_bookmark("b6")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat_scene4_worked(self):
        """Scene 4: Worked example 4 × 23 — the classic Class 8 mental-math
        trick, with real Brace labels for height/width."""
        with self.voiceover(text=NARRATION["scene4_worked"]) as tracker:
            self.reset_board()

            prob = chalk_math("4 \\times 23", size=52).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.8, 0]))
            self.play(Write(prob), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # Diagram: rectangle 4 x 23 — enlarged to use the board, with a
            # real Brace + label for the height.
            rect = RoundedRectangle(width=5.6, height=2.2, corner_radius=0.06,
                           stroke_width=2.5, stroke_color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.4, 0]))
            height_brace = Brace(rect, LEFT, buff=0.15, color=CHALK_WHITE)
            height_label = chalk_math("4", size=36, color=CHALK_RED).next_to(
                height_brace, LEFT, buff=0.1)
            self.play(Create(drop_shadow(rect, dx=0.07, dy=-0.08, opacity=0.3)),
                     GrowFromCenter(height_brace), FadeIn(height_label),
                     run_time=rt(tracker.time_until_bookmark("b1")))

            # Fast divider draw at the true 20/23 split point
            split_x = rect.get_left()[0] + rect.width * (20 / 23)
            divider = DashedLine(
                np.array([split_x, rect.get_bottom()[1], 0]),
                np.array([split_x, rect.get_top()[1], 0]),
                stroke_color=CHALK_WHITE, stroke_width=2
            )
            self.play(Create(divider), run_time=rt(tracker.time_until_bookmark("b2") * 0.35))

            # Width labels as real Braces under each piece (own bookmark,
            # so it isn't starved by the divider's animation above)
            left_ref = Rectangle(width=split_x - rect.get_left()[0], height=0.01).move_to(
                np.array([(rect.get_left()[0] + split_x) / 2, rect.get_bottom()[1], 0]))
            right_ref = Rectangle(width=rect.get_right()[0] - split_x, height=0.01).move_to(
                np.array([(split_x + rect.get_right()[0]) / 2, rect.get_bottom()[1], 0]))
            brace_20 = Brace(left_ref, DOWN, buff=0.12, color=CHALK_BLUE)
            lbl_20 = chalk_math("20", size=34, color=CHALK_BLUE).next_to(brace_20, DOWN, buff=0.1)
            brace_3 = Brace(right_ref, DOWN, buff=0.12, color=CHALK_GREEN)
            lbl_3 = chalk_math("3", size=34, color=CHALK_GREEN).next_to(brace_3, DOWN, buff=0.1)
            self.play(GrowFromCenter(brace_20), FadeIn(lbl_20),
                      GrowFromCenter(brace_3), FadeIn(lbl_3),
                     run_time=rt(tracker.time_until_bookmark("b2b")))

            # Step 1: 4(20+3)
            step1 = chalk_math("4(20+3)", size=44, color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.8, 0]))
            self.play(ReplacementTransform(prob, step1),
                     run_time=rt(tracker.time_until_bookmark("b3")))

            # Step 2: 80 + 12 — pre-arranged with the result BEFORE either
            # is shown, so "80 + 12 = 92" ends up centred on the board as
            # one unit instead of "80 + 12" alone being centred and "= 92"
            # trailing off to the right of true centre.
            step2 = chalk_math("80 + 12", size=44, color=CHALK_CYAN)
            result = chalk_math("= 92", size=44, color=CHALK_YELLOW)
            VGroup(step2, result).arrange(RIGHT, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.8, 0]))
            self.play(ReplacementTransform(step1, step2),
                     run_time=rt(tracker.time_until_bookmark("b4")))

            # Result: = 92 (already positioned as part of the pre-centered
            # pair above)
            self.play(FadeIn(result), run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["success"], gain=-11)

            # "That's the distributive property over addition." (b6) —
            # keeps the board moving through the tail of the narration
            # instead of freezing.
            self.play(Indicate(VGroup(step2, result), color=CHALK_YELLOW, scale_factor=1.08),
                     run_time=rt(tracker.time_until_bookmark("b6")))

            # b6->b7: "Now let's try one over subtraction." — clear the
            # addition diagram to make room for the 6x98 example.
            addition_group = VGroup(step2, result, rect, height_brace, height_label,
                                     divider, brace_20, lbl_20, brace_3, lbl_3)
            self.play(FadeOut(addition_group), run_time=rt(tracker.time_until_bookmark("b7")))

            # b7->b8: "What is 6 times 98?" — a new problem + rectangle
            # diagram, echoing the addition example's structure exactly.
            prob2 = chalk_math("6 \\times 98", size=52).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.8, 0]))
            rect2 = RoundedRectangle(width=5.6, height=2.2, corner_radius=0.06,
                           stroke_width=2.5, stroke_color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.4, 0]))
            height_brace2 = Brace(rect2, LEFT, buff=0.15, color=CHALK_WHITE)
            height_label2 = chalk_math("6", size=36, color=CHALK_RED).next_to(
                height_brace2, LEFT, buff=0.1)
            self.play(Write(prob2),
                      Create(drop_shadow(rect2, dx=0.07, dy=-0.08, opacity=0.3)),
                      GrowFromCenter(height_brace2), FadeIn(height_label2),
                     run_time=rt(tracker.time_until_bookmark("b8")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # b8->b8b: "Think of 98 as 100 minus 2." — a big "100" piece
            # plus a small pink "taken away" sliver on the right (widened
            # here for legibility — not drawn to the true 2/100 scale).
            split_x2 = rect2.get_left()[0] + rect2.width * 0.82
            divider2 = DashedLine(
                np.array([split_x2, rect2.get_bottom()[1], 0]),
                np.array([split_x2, rect2.get_top()[1], 0]),
                stroke_color=CHALK_WHITE, stroke_width=2
            )
            removed = Rectangle(
                width=rect2.get_right()[0] - split_x2, height=rect2.height,
                stroke_width=0, fill_color=CHALK_PINK, fill_opacity=0.35,
            ).move_to(np.array([(split_x2 + rect2.get_right()[0]) / 2,
                                 rect2.get_center()[1], 0]))
            self.play(Create(divider2), FadeIn(removed),
                     run_time=rt(tracker.time_until_bookmark("b8b") * 0.4))

            left_ref2 = Rectangle(width=split_x2 - rect2.get_left()[0], height=0.01).move_to(
                np.array([(rect2.get_left()[0] + split_x2) / 2, rect2.get_bottom()[1], 0]))
            right_ref2 = Rectangle(width=rect2.get_right()[0] - split_x2, height=0.01).move_to(
                np.array([(split_x2 + rect2.get_right()[0]) / 2, rect2.get_bottom()[1], 0]))
            brace_100 = Brace(left_ref2, DOWN, buff=0.12, color=CHALK_BLUE)
            lbl_100 = chalk_math("100", size=32, color=CHALK_BLUE).next_to(
                brace_100, DOWN, buff=0.1)
            brace_2 = Brace(right_ref2, DOWN, buff=0.12, color=CHALK_PINK)
            lbl_2 = chalk_math("-2", size=30, color=CHALK_PINK).next_to(
                brace_2, DOWN, buff=0.1)
            self.play(GrowFromCenter(brace_100), FadeIn(lbl_100),
                      GrowFromCenter(brace_2), FadeIn(lbl_2),
                     run_time=rt(tracker.time_until_bookmark("b8b")))

            # Step 1: 6(100-2) — b8b->b9: "So we have 6 times (100 minus 2)."
            step1b = chalk_math("6(100-2)", size=44, color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.8, 0]))
            self.play(ReplacementTransform(prob2, step1b),
                     run_time=rt(tracker.time_until_bookmark("b9")))

            # Step 2: 600 - 12 — pre-arranged with the result BEFORE either
            # is shown (same fix as the addition example above), so
            # "600 - 12 = 588" ends up centred on the board as one unit.
            # b9->b10: "Distribute the 6: 6 times 100 equals 600, and 6
            # times 2 equals 12."
            step2b = chalk_math("600 - 12", size=44, color=CHALK_CYAN)
            resultb = chalk_math("= 588", size=44, color=CHALK_YELLOW)
            VGroup(step2b, resultb).arrange(RIGHT, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.8, 0]))
            self.play(ReplacementTransform(step1b, step2b),
                     run_time=rt(tracker.time_until_bookmark("b10")))

            # Result: = 588 (already positioned as part of the pre-centered
            # pair above) — b10->b11: "Subtract them: 600 minus 12 equals
            # 588."
            self.play(FadeIn(resultb), run_time=rt(tracker.time_until_bookmark("b11")))
            self.add_sound(self.sfx["success"], gain=-11)

            # "Same trick, works either way!" (b12)
            self.play(Indicate(VGroup(step2b, resultb), color=CHALK_YELLOW, scale_factor=1.08),
                     run_time=rt(tracker.time_until_bookmark("b12")))

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat_scene4b_mistake(self):
        """Bonus scene: the #1 student mistake on this topic — forgetting
        to distribute to the second term — contrasted with the correct
        method, reusing the same 4x23 numbers for continuity."""
        with self.voiceover(text=NARRATION["scene4b_mistake"]) as tracker:
            self.reset_board()

            heading = board_text("A Common Mistake!", size=32, weight="BOLD",
                                color=CHALK_PINK).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.8, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))

            # Pre-arrange the WHOLE row (label + equation + result + tag)
            # as one centered VGroup before anything is shown, so revealing
            # the result/tag later doesn't leave the row looking shifted
            # left of true board centre.
            wrong_label = board_text("WRONG:", size=24, weight="BOLD", color=CHALK_RED)
            wrong_eq = chalk_math("4\\times 20+3", size=38, color=CHALK_RED)
            wrong_result = chalk_math("=\\ 83", size=38, color=CHALK_RED)
            cross = board_text("(X)", size=26, weight="BOLD", color=CHALK_RED)
            VGroup(wrong_label, wrong_eq, wrong_result, cross).arrange(
                RIGHT, buff=0.3).move_to(np.array([BOARD_CX, BOARD_CY + 1.1, 0]))
            wrong_row = VGroup(wrong_label, wrong_eq)
            self.play(FadeIn(wrong_row), run_time=rt(tracker.time_until_bookmark("b1")))

            # b1->b2: "They write 4 times 20, plus 3 — forgetting to
            # multiply the second term!" — the number 83 isn't spoken until
            # the *next* sentence, so just highlight the (incomplete)
            # wrong equation here rather than revealing its answer early.
            self.play(Indicate(wrong_eq, color=CHALK_RED, scale_factor=1.05),
                     run_time=rt(tracker.time_until_bookmark("b2")))

            # b2->b3: "That gives 80 plus 3, which is 83 — and that's
            # wrong." — reveal the wrong answer exactly when it's named
            # (already positioned as part of the pre-centered row above).
            self.play(Write(wrong_result), FadeIn(cross),
                     run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            note = board_text("The 4 must multiply BOTH terms!", size=20,
                              color=CHALK_AMBER).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.1, 0]))
            self.play(FadeIn(note), run_time=rt(tracker.time_until_bookmark("b4")))

            correct_label = board_text("CORRECT:", size=24, weight="BOLD", color=CHALK_GREEN)
            correct_eq = chalk_math("4\\times 20+4\\times 3=92", size=34, color=CHALK_GREEN)
            check = board_text("(OK)", size=26, weight="BOLD", color=CHALK_GREEN)
            VGroup(correct_label, correct_eq, check).arrange(RIGHT, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY - 1.4, 0]))
            correct_row = VGroup(correct_label, correct_eq)
            self.play(FadeIn(correct_row), FadeIn(check),
                     run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["success"], gain=-11)

            tip = board_text("Always distribute to every single term!", size=20,
                             color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.4, 0]))
            self.play(FadeIn(tip), Indicate(correct_eq, color=CHALK_GREEN),
                     run_time=rt(tracker.time_until_bookmark("b6")))

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def _notebook_icon(self, width: float = 0.34, height: float = 0.44,
                        color: str = CHALK_BLUE) -> VGroup:
        """A chalk-vector spiral notebook: soft-cornered cover with pseudo-
        3D depth (drop_shadow, matching every other diagram in this file),
        a red margin rule, ruled page lines, and circular spiral-ring
        binding along the top edge — built the same way as wheat_stalk/
        corn_cob, from primitive shapes rather than a flat colored square."""
        cover = RoundedRectangle(width=width, height=height, corner_radius=0.02,
                                  stroke_color=color, stroke_width=1.6,
                                  fill_color=color, fill_opacity=0.22)
        margin = Line(cover.get_corner(UL) + DOWN * height * 0.08 + RIGHT * width * 0.2,
                      cover.get_corner(DL) + UP * height * 0.06 + RIGHT * width * 0.2,
                      stroke_color=CHALK_RED, stroke_width=0.9, stroke_opacity=0.65)
        pages = VGroup(*[
            Line(RIGHT * width * 0.1, RIGHT * width * 0.34,
                 stroke_color=CHALK_WHITE, stroke_width=0.9, stroke_opacity=0.55)
            .move_to(cover.get_center() + DOWN * y)
            for y in np.linspace(-height * 0.16, height * 0.28, 3)
        ])
        body = drop_shadow(VGroup(cover, margin, pages), dx=0.02, dy=-0.025, opacity=0.25)
        rings = VGroup(*[
            Circle(radius=width * 0.045, stroke_color=CHALK_WHITE, stroke_width=1.1,
                   fill_color="#1E2A1A", fill_opacity=0.85).move_to(
                cover.get_top() + RIGHT * x)
            for x in np.linspace(-width * 0.32, width * 0.32, 4)
        ])
        return VGroup(body, rings)

    def _pen_icon(self, length: float = 0.64, color: str = CHALK_GREEN) -> VGroup:
        """A chalk-vector ballpoint pen with a distinct two-tone cap,
        pocket clip, tapered barrel and a metal-tone tip — assembled from
        Rectangle/Polygon primitives (same technique as wheat_stalk/
        corn_cob) instead of a flat circle, so it reads as an actual pen."""
        w = length * 0.16
        cap_h, barrel_h, taper_h, tip_h = length * 0.26, length * 0.32, length * 0.1, length * 0.08

        y0 = 0.0
        y1 = y0 - cap_h
        y2 = y1 - barrel_h
        y3 = y2 - taper_h
        y4 = y3 - tip_h

        cap = RoundedRectangle(width=w * 1.05, height=cap_h, corner_radius=w * 0.3,
                                stroke_color=color, stroke_width=1.4,
                                fill_color=color, fill_opacity=0.4).move_to(
            np.array([0, (y0 + y1) / 2, 0]))
        clip = Rectangle(width=w * 0.2, height=cap_h * 0.65, stroke_color=color,
                          stroke_width=1.0, fill_color=color, fill_opacity=0.55).move_to(
            np.array([w * 0.58, (y0 + y1) / 2 + cap_h * 0.05, 0]))
        seam = Rectangle(width=w * 1.05, height=length * 0.02, stroke_width=0,
                          fill_color=CHALK_WHITE, fill_opacity=0.6).move_to(
            np.array([0, y1, 0]))
        barrel = Rectangle(width=w, height=barrel_h, stroke_color=color,
                            stroke_width=1.4, fill_color=color, fill_opacity=0.22).move_to(
            np.array([0, (y1 + y2) / 2, 0]))
        taper = Polygon(
            np.array([-w / 2, y2, 0]), np.array([w / 2, y2, 0]),
            np.array([w * 0.18, y3, 0]), np.array([-w * 0.18, y3, 0]),
            stroke_color=color, stroke_width=1.2, fill_color=color, fill_opacity=0.3,
        )
        tip = Polygon(
            np.array([-w * 0.18, y3, 0]), np.array([w * 0.18, y3, 0]), np.array([0, y4, 0]),
            stroke_color="#D8D8D8", stroke_width=1.0,
            fill_color="#D8D8D8", fill_opacity=0.9,
        )
        pen = VGroup(barrel, taper, tip, cap, seam, clip)
        pen.rotate(-PI / 9)
        return pen

    def _bag_icon(self) -> VGroup:
        """A shopping bag holding a real notebook and pen diagram (not a
        flat square/circle) — a realistic pair for the everyday-life
        example."""
        bag = RoundedRectangle(width=0.95, height=1.15, corner_radius=0.12,
                                stroke_color=CHALK_AMBER, stroke_width=2,
                                fill_color="#3A2A15", fill_opacity=0.45)
        book = self._notebook_icon().move_to(bag.get_center() + UP * 0.2 + LEFT * 0.06)
        pen = self._pen_icon().move_to(bag.get_center() + DOWN * 0.24 + RIGHT * 0.22)
        return VGroup(bag, book, pen)

    def beat_scene4c_mistake_subtraction(self):
        """Bonus scene: the sign mistake unique to subtraction -- flipping
        the minus into a plus when distributing (a(b-c) must NOT become
        ab+ac). Mirrors beat_scene4b_mistake's layout for visual
        consistency, reusing the 6x98 numbers from the subtraction
        worked example."""
        with self.voiceover(text=NARRATION["scene4c_mistake"]) as tracker:
            self.reset_board()

            heading = board_text("The Subtraction Trap!", size=32, weight="BOLD",
                                color=CHALK_PINK).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.8, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))

            # Pre-arrange the WHOLE row (label + equation + result + tag)
            # as one centered VGroup before anything is shown, so revealing
            # the result/tag later doesn't leave the row looking shifted
            # left of true board centre.
            wrong_label = board_text("WRONG:", size=24, weight="BOLD", color=CHALK_RED)
            wrong_eq = chalk_math("6\\times100+6\\times2", size=32, color=CHALK_RED)
            wrong_result = chalk_math("=\\ 612", size=38, color=CHALK_RED)
            cross = board_text("(X)", size=26, weight="BOLD", color=CHALK_RED)
            VGroup(wrong_label, wrong_eq, wrong_result, cross).arrange(
                RIGHT, buff=0.3).move_to(np.array([BOARD_CX, BOARD_CY + 1.1, 0]))
            wrong_row = VGroup(wrong_label, wrong_eq)
            self.play(FadeIn(wrong_row), run_time=rt(tracker.time_until_bookmark("b1")))

            # b1->b2: "They write 6 times 100, plus 6 times 2 — turning
            # the minus into a plus!" — highlight the (incomplete) wrong
            # equation; its numeric answer isn't named until the next
            # sentence.
            self.play(Indicate(wrong_eq, color=CHALK_RED, scale_factor=1.05),
                     run_time=rt(tracker.time_until_bookmark("b2")))

            # b2->b3: "That gives 600 plus 12, which is 612 — and that's
            # wrong." — reveal the wrong answer exactly when it's named
            # (already positioned as part of the pre-centered row above).
            self.play(Write(wrong_result), FadeIn(cross),
                     run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            note = board_text("The minus sign must stay!", size=20,
                              color=CHALK_AMBER).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.1, 0]))
            self.play(FadeIn(note), run_time=rt(tracker.time_until_bookmark("b4")))

            correct_label = board_text("CORRECT:", size=24, weight="BOLD", color=CHALK_GREEN)
            correct_eq = chalk_math("6\\times100-6\\times2=588", size=30, color=CHALK_GREEN)
            check = board_text("(OK)", size=26, weight="BOLD", color=CHALK_GREEN)
            VGroup(correct_label, correct_eq, check).arrange(RIGHT, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY - 1.4, 0]))
            correct_row = VGroup(correct_label, correct_eq)
            self.play(FadeIn(correct_row), FadeIn(check),
                     run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["success"], gain=-11)

            tip = board_text("Keep the operation exactly as it was inside!", size=18,
                             color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.4, 0]))
            self.play(FadeIn(tip), Indicate(correct_eq, color=CHALK_GREEN),
                     run_time=rt(tracker.time_until_bookmark("b6")))

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat_scene5_realworld(self):
        """Scene 5: Real-world — 5 friends, each buying a notebook and a
        pen, shown as real bag icons and enlarged, not equations alone."""
        with self.voiceover(text=NARRATION["scene5_realworld"]) as tracker:
            self.reset_board()

            title = board_text("5 Friends: Notebooks & Pens", size=27,
                              color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.9, 0]))
            bags = VGroup(*[self._bag_icon() for _ in range(5)]).arrange(
                RIGHT, buff=0.4).move_to(np.array([BOARD_CX, BOARD_CY + 1.1, 0]))

            self.play(Write(title),
                      LaggedStart(*[GrowFromCenter(b) for b in bags], lag_ratio=0.15),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-15)

            # b0->b1: "5 friends each buy a notebook for 20 rupees and a pen
            # for 3 rupees." — the prices are being named here, before any
            # equation exists yet, so just tag the bags with the prices.
            price_tags = board_text("Notebooks Each Rs 20 and Pens Each Rs 3",
                                    size=18, color=CHALK_AMBER).next_to(
                bags, DOWN, buff=0.3)
            self.play(FadeIn(price_tags), run_time=rt(tracker.time_until_bookmark("b1")))

            # b1->b2: "What's the total cost?" — the question that motivates
            # writing the expression down.
            prob = chalk_math("5(20+3)", size=44).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.6, 0]))
            self.play(FadeOut(price_tags), Write(prob),
                     run_time=rt(tracker.time_until_bookmark("b2")))

            # b2->b3: "We can think of it as 5 times (20 plus 3)." — this is
            # literally `prob`, so just settle on it rather than moving on.
            self.play(Indicate(prob, color=CHALK_CYAN, scale_factor=1.05),
                     run_time=rt(tracker.time_until_bookmark("b3")))

            # b3->b4: "Or, buy all 5 notebooks first: 100 rupees. Then all 5
            # pens: 15 rupees." — distribute, then compute each piece, in
            # that spoken order, both inside this one window.
            dist = chalk_math("5(20) + 5(3)", size=44, color=CHALK_CYAN).move_to(
                prob.get_center())
            self.play(ReplacementTransform(prob, dist),
                     run_time=rt(tracker.time_until_bookmark("b4") * 0.45))
            calc = chalk_math("100 + 15", size=44, color=CHALK_GREEN).move_to(
                dist.get_center())
            self.play(ReplacementTransform(dist, calc),
                     run_time=rt(tracker.time_until_bookmark("b4")))

            # b4->b5: "Total: 115 rupees. Distribution happens naturally in
            # everyday life!" — reveal the total, then the recap detail line.
            total = chalk_math("= 115", size=44, color=CHALK_YELLOW).next_to(
                calc, RIGHT, buff=0.3)
            self.play(FadeIn(total), run_time=rt(tracker.time_until_bookmark("b5") * 0.4))
            self.add_sound(self.sfx["success"], gain=-11)

            detail = board_text("(5 notebooks @ Rs.20 + 5 pens @ Rs.3)", size=16,
                              color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_CY - 1.5, 0]))
            self.play(FadeIn(detail), run_time=rt(tracker.time_until_bookmark("b5")))

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat_scene6b_challenge(self):
        """YOUR TURN -- 7 x 19, a fresh problem the student hasn't already
        seen solved (the earlier worked examples covered 4x23 and 6x98,
        so reusing either here would just replay an answer rather than
        test anything). Series' consistent 10-second countdown clock;
        setup and reveal are narrated, only the countdown itself is silent."""
        with self.voiceover(text=NARRATION["challenge_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", size=32, weight="BOLD",
                                 color=CHALK_PINK).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.6, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            prob = chalk_math(r"7\times 19", size=52, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.9, 0]))
            hint = board_text("Hint: 19 = 20 - 1", size=22, color=CHALK_CYAN).next_to(
                prob, DOWN, buff=0.4)
            self.play(Write(prob), FadeIn(hint), run_time=rt(tracker.time_until_bookmark("b1")))

            pause_lbl = board_text("Pause and try it!", size=22, color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.5, 0]))
            self.play(FadeIn(pause_lbl), run_time=rt(tracker.time_until_bookmark("b2")))

            self._capture_srt(tracker)

        # Consistent 10-second challenge clock (whole series): the
        # background dims while the countdown runs, question stays bright.
        play_challenge_countdown(self, seconds=10, sfx=self.sfx)

        # Reveal -- 7x19 = 7(20-1) = 140-7 = 133.
        with self.voiceover(text=NARRATION["challenge_reveal"]) as tracker:
            self.play(FadeOut(pause_lbl), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))
            steps = VGroup(
                chalk_math(r"7\times 19 = 7\times(20-1)", size=30, color=CHALK_WHITE),
                chalk_math(r"= 7\times 20 - 7\times 1", size=30, color=CHALK_CYAN),
                chalk_math(r"= 140 - 7 = 133", size=30, color=CHALK_GREEN),
            ).arrange(DOWN, buff=0.35).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.5, 0]))
            self.play(FadeOut(prob), FadeOut(hint), FadeIn(steps),
                     run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["success"], gain=-11)

            tag = board_text("Quick mental math -- distribute!", size=22,
                             weight="BOLD", color=CHALK_AMBER).next_to(
                steps, DOWN, buff=0.4)
            self.play(FadeIn(tag), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def beat_scene7_finale(self):
        """Scene 7: Recap and conclusion — the splitting rectangle from
        Scene 2 and the formula from Scene 3, per the storyboard, enlarged."""
        with self.voiceover(text=NARRATION["scene7_finale"]) as tracker:
            self.reset_board()

            # b0's narration is "Remember: the distributive property is
            # just breaking things apart." — the closing punchline "Break
            # it down to make it simple." isn't spoken until the very end
            # of this scene (b2), so it must not appear here; a different
            # takeaway line replaces it near the formula reveal below.
            # size/y tuned so this stays clear of the top-left logo (height
            # 0.7, centred at BOARD_TOP-0.4) even though it's a wide string.
            takeaway = board_text("It's All About Breaking Things Apart!",
                                 size=27, weight="BOLD", color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, BOARD_TOP - 1.05, 0]))
            self.play(Write(takeaway), run_time=rt(tracker.time_until_bookmark("b0")))

            # The splitting/rejoining rectangle from Scene 2, recapped
            whole = RoundedRectangle(width=4.4, height=2.2, corner_radius=0.06,
                            stroke_width=2.5, stroke_color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.6, 0]))
            half_l = Rectangle(width=2.2, height=2.2, stroke_width=0,
                              fill_color=CHALK_YELLOW, fill_opacity=0.3).move_to(
                np.array([BOARD_CX - 1.1, BOARD_CY + 0.6, 0]))
            half_r = Rectangle(width=2.2, height=2.2, stroke_width=0,
                              fill_color=CHALK_GREEN, fill_opacity=0.3).move_to(
                np.array([BOARD_CX + 1.1, BOARD_CY + 0.6, 0]))
            # Both steps stay inside the b1 bookmark budget (first call
            # only spends 60% of it) instead of adding untracked fixed
            # run_times after it, which would push the formula reveal below
            # late relative to the narration.
            self.play(Create(drop_shadow(whole, dx=0.08, dy=-0.09, opacity=0.3)),
                      FadeIn(half_l), FadeIn(half_r),
                     run_time=rt(tracker.time_until_bookmark("b1") * 0.6))
            self.add_sound(self.sfx["ding"], gain=-13)

            # Split apart, echoing Scene 2's proof
            self.play(half_l.animate.shift(LEFT * 0.5), half_r.animate.shift(RIGHT * 0.5),
                      run_time=rt(tracker.time_until_bookmark("b1")))

            # Both stay inside the b2 budget (Write takes 70%, Circumscribe
            # gets the correctly-reduced remainder) — narration ends right
            # at b2 now, so nothing is left unconsumed after this. b2's
            # narration ends on "...Break it down to make it simple." so
            # that punchline replaces the opening heading right here,
            # landing exactly when it's spoken instead of at scene open.
            formula = chalk_math("a(b+c) = ab + ac", size=44, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.9, 0]))
            punchline = board_text("Break it down to make it simple.",
                                   size=32, weight="BOLD", color=CHALK_AMBER).move_to(
                takeaway.get_center())
            self.play(Write(formula), ReplacementTransform(takeaway, punchline),
                     run_time=rt(tracker.time_until_bookmark("b2") * 0.7))
            self.play(Circumscribe(formula, color=CHALK_AMBER, stroke_width=3, time_width=0.6),
                     run_time=rt(tracker.time_until_bookmark("b2")))

            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    def bullet_row(self, n: int, lines: list[str], *, color: str = CHALK_CYAN) -> VGroup:
        """A numbered recap line — mirrors Simple-vs-Compound-Interest's
        closing summary layout."""
        badge = Circle(radius=0.19, stroke_color=color, stroke_width=2,
                        fill_color=color, fill_opacity=0.18)
        num = board_text(str(n), 18, color, "BOLD").move_to(badge.get_center())
        text_block = VGroup(*[board_text(t, 22, CHALK_WHITE) for t in lines]).arrange(
            DOWN, buff=0.06, aligned_edge=LEFT)
        row = VGroup(VGroup(badge, num), text_block).arrange(RIGHT, buff=0.3)
        VGroup(badge, num).move_to(np.array([row[0].get_x(), text_block.get_y(), 0]))
        return row

    def beat_summary(self) -> None:
        """Closing screen — same "Thank You for Watching!" template as
        Simple-vs-Compound-Interest's beat_summary."""
        with self.voiceover(text=NARRATION["summary"]) as tracker:
            self.reset_board()

            heading = board_text("Summary", 34, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.4, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            bullets = VGroup(
                self.bullet_row(1, ["a(b+c) = ab+ac — over addition"], color=CHALK_CYAN),
                self.bullet_row(2, ["a(b-c) = ab-ac — over subtraction"], color=CHALK_PINK),
                self.bullet_row(3, ["Mental math & a Rs. 115 shopping bill"], color=CHALK_GREEN),
            )
            bullets.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
            bullets.move_to(np.array([BOARD_CX, BOARD_CY + 0.55, 0]))

            # b1->b2: "Over addition: a times (b plus c) equals a b plus a c."
            self.play(FadeIn(bullets[0], shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            # b2->b2b: "Over subtraction: a times (b minus c) equals a b
            # minus a c."
            self.play(FadeIn(bullets[1], shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b2b")))
            self.add_sound(self.sfx["click"], gain=-15)

            # b2b->b3 covers "We used it for quick mental math, and for
            # splitting a real shopping bill." — the one remaining bullet.
            self.play(FadeIn(bullets[2], shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            # b3->b4: "Whenever a number multiplies a sum or a difference,
            # you can distribute it across every term — break it down to
            # make it simple." — highlight the recap and reveal the
            # closing tagline right when it's spoken.
            tagline = board_text("Break it down to make it simple.", size=24,
                                 weight="BOLD", color=CHALK_AMBER).next_to(
                bullets, DOWN, buff=0.35)
            self.play(Indicate(bullets, color=CHALK_AMBER, scale_factor=1.02),
                      FadeIn(tagline, shift=UP * 0.1),
                     run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            summary_group = VGroup(heading, bullets, tagline)
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
        """Capture word boundaries from tracker and build SRT entries."""
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
        """Write real SRT file from captured word boundaries."""
        out_dir = _HERE / "media" / "videos" / "distributive_property_story"
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

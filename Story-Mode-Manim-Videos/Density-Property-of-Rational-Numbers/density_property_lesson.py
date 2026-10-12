"""
Density Property of Rational Numbers — Chalkboard Lesson (v2)
Uses assets/background2.png (an empty classroom chalkboard, no characters),
so the whole board is available: intuition, a short history beat, and two
worked numeric examples, all synced to voiceover narration.

Sync strategy: EdgeSpeechService (edge_speech_service.py) captures real
per-word timing from edge-tts's WordBoundary events. Every narration string
below carries `<bookmark mark='...'/>` tags at the exact word a visual must
land on, and every `self.play(...)` run_time is computed from
`tracker.time_until_bookmark(...)` instead of a guessed fraction of the
total duration — so an animation finishes exactly when the matching word is
spoken, no matter how edge-tts happens to pace that particular sentence.

Beats:
  0. Title
  1. Hook / The Canyon — successive integers 0 and 1 have nothing between them.
  2. History — fractions are ancient; the density property was made rigorous
     when 19th-century mathematicians (Dedekind) built the real numbers.
  3. The Halfway Bridge — the mean (a+b)/2 always lands a new rational
     number exactly in the middle. Flag dropped at 1/2.
  4. Quarters — repeat the trick: 1/4 and 3/4 appear.
  5. Eighths — repeat again, microscopic scale: 1/8, 3/8, 5/8, 7/8.
  6. Example 1 — a rational strictly between 1/4 and 1/2 (worked numerically).
  7. Example 2 — a rational strictly between 0.3 and 0.32 (decimals; shows the
     trick still works even when the numbers are already very close).
  8. Endless Universe — the formal density-property statement + glowing
     highway of numbers (equivalent fractions as evidence of infinity).
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
    ORIGIN, UP, DOWN, LEFT, RIGHT, UL, UR, DL, DR, PI,
    ImageMobject, MathTex, VGroup, Group, Line, DashedLine, Dot, Circle,
    Polygon, Rectangle, RoundedRectangle, Triangle, Arrow, Sector, Annulus,
    Text, Write, FadeIn, FadeOut, Create, Uncreate, Transform,
    ReplacementTransform, FadeTransform, GrowFromCenter, GrowFromPoint,
    GrowArrow, Indicate, Flash, Circumscribe, Wiggle, DrawBorderThenFill,
    LaggedStart, LaggedStartMap, Succession, SpinInFromNothing,
    ShrinkToCenter, ApplyWave, rate_functions, config,
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
FONT = "Segoe Print"
MATH_COLOR = CHALK_WHITE

END_HOLD = 2.2
MIN_RT = 0.12  # floor for any run_time computed from bookmark timing


def rt(seconds: float, floor: float = MIN_RT) -> float:
    """Clamp a bookmark-derived duration to a sane minimum run_time so a
    mistimed or very close pair of bookmarks never yields a ~0s play()."""
    return max(floor, float(seconds))


# Safe drawing rectangle inside the chalkboard (measured against
# assets/background2.png — an empty board, so this is nearly the full
# green area, just clearing the wooden frame, the chalk ledge at the
# bottom, and the world map / bookshelf decor on the right).
BOARD_LEFT = -4.6
BOARD_RIGHT = 5.6
BOARD_TOP = 3.3
BOARD_BOTTOM = -2.9
BOARD_CX = (BOARD_LEFT + BOARD_RIGHT) / 2
BOARD_CY = (BOARD_TOP + BOARD_BOTTOM) / 2

LINE_X0 = BOARD_LEFT + 0.6
LINE_X1 = BOARD_RIGHT - 0.6
LINE_Y = BOARD_CY + 0.4


def board_text(s: str, size: int = 34, color: str = CHALK_WHITE, weight: str = "NORMAL") -> Text:
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def chalk_math(s: str, size: int = 34, color: str = MATH_COLOR) -> MathTex:
    return MathTex(s, font_size=size, color=color)


def vx(vmin: float, vmax: float, x0: float, x1: float, v: float) -> float:
    return x0 + (v - vmin) / (vmax - vmin) * (x1 - x0)


def _frac_label(v: float) -> str:
    if float(v).is_integer():
        return str(int(v))
    from fractions import Fraction
    f = Fraction(v).limit_denominator(1000)
    return f"{f.numerator}/{f.denominator}"


def make_number_line(vmin: float, vmax: float, majors: list[float], *,
                      y: float = LINE_Y, x0: float = LINE_X0, x1: float = LINE_X1,
                      color: str = CHALK_WHITE, label_fn=_frac_label) -> VGroup:
    """A horizontal chalk line spanning value range [vmin, vmax] with big
    ticks + labels at every value in `majors`. Carries a `.to_x(v)` helper
    so callers can place more marks on the same scale later.

    The line gets small arrowheads at both ends -- a real number line
    (even a deliberately zoomed-in slice of it, as most beats here are)
    extends infinitely, so a flat stop misrepresents it. Arrows extend
    OUTWARD past x0/x1 (rather than retracting into them) so they never
    collide with ticks/dots placed exactly at the endpoints.
    """
    body = Line(np.array([x0, y, 0]), np.array([x1, y, 0]),
                stroke_color=color, stroke_width=5)
    tip_len = 0.22
    right_tip = Arrow(np.array([x1, y, 0]), np.array([x1 + tip_len, y, 0]),
                       color=color, stroke_width=5, buff=0, tip_length=0.18,
                       max_tip_length_to_length_ratio=1.0)
    left_tip = Arrow(np.array([x0, y, 0]), np.array([x0 - tip_len, y, 0]),
                      color=color, stroke_width=5, buff=0, tip_length=0.18,
                      max_tip_length_to_length_ratio=1.0)
    line = VGroup(body, left_tip, right_tip)
    ticks = VGroup()
    for v in majors:
        px = vx(vmin, vmax, x0, x1, v)
        tick = Line(np.array([px, y - 0.14, 0]), np.array([px, y + 0.14, 0]),
                    stroke_color=color, stroke_width=5)
        dot = Dot(np.array([px, y, 0]), radius=0.09, color=CHALK_YELLOW)
        label = board_text(label_fn(v), 30, CHALK_YELLOW).next_to(
            np.array([px, y, 0]), DOWN, buff=0.32)
        ticks.add(VGroup(tick, dot, label))
    g = VGroup(line, ticks)
    g.to_x = lambda v, _x0=x0, _x1=x1, _vmin=vmin, _vmax=vmax: vx(_vmin, _vmax, _x0, _x1, v)
    g.y = y
    return g


def drop_flag(pos: np.ndarray, color: str = CHALK_PINK, height: float = 0.55) -> VGroup:
    pole = Line(pos, pos + UP * height, stroke_color=CHALK_WHITE, stroke_width=3)
    pennant = Polygon(
        pos + UP * height,
        pos + UP * (height - 0.22) + RIGHT * 0.34,
        pos + UP * (height - 0.44),
        stroke_width=0, fill_color=color, fill_opacity=0.95,
    )
    return VGroup(pole, pennant)


def small_dot_label(pos: np.ndarray, label: str, color: str = CHALK_CYAN,
                     dot_color: str = CHALK_CYAN) -> VGroup:
    dot = Dot(pos, radius=0.07, color=dot_color)
    lbl = board_text(label, 24, color).next_to(pos, DOWN, buff=0.24)
    return VGroup(dot, lbl)


def timeline_node(pos: np.ndarray, color: str = CHALK_CYAN) -> VGroup:
    ring = Circle(radius=0.11, stroke_color=color, stroke_width=3,
                   fill_color=color, fill_opacity=0.25).move_to(pos)
    return ring


# ---------------------------------------------------------------- narration --
# `<bookmark mark='...'/>` tags are stripped before speech synthesis (see
# edge_speech_service.py) but are used by manim_voiceover's tracker to map
# real per-word audio timing back onto the scene, via tracker.time_until_bookmark.
NARRATION = {
    "intro_real": (
        "Think about everyday life for a second.<bookmark mark='b1'/> "
        "When you slice a pizza into equal pieces,<bookmark mark='b2'/> "
        "measure a plank of wood down to the last half "
        "centimetre,<bookmark mark='b3'/> or split a dinner bill three "
        "ways,<bookmark mark='b4'/> you are using rational numbers all the "
        "time. So let's dig into one of their most surprising secrets."
    ),
    "title": (
        "Come sit down. Today we are going on a tiny expedition, right here "
        "on our number line, to find something that feels almost like magic: "
        "<bookmark mark='b1'/>the density property "
        "<bookmark mark='b2'/>of rational numbers<bookmark mark='b3'/>."
    ),
    "canyon": (
        "Look at zero and one.<bookmark mark='b1'/> They are neighbours. "
        "Successive integers.<bookmark mark='b2'/> If I ask you for a whole "
        "number strictly between them, you would search and search and find "
        "nothing.<bookmark mark='b3'/> It is a canyon with no integer bridge "
        "across it.<bookmark mark='b4'/> But rational numbers, fractions, "
        "are far more adventurous than whole numbers. Let's see what they "
        "can do."
    ),
    "history": (
        "Fractions themselves are ancient.<bookmark mark='b1'/> Egyptian and "
        "Babylonian traders were splitting bread and land into pieces like "
        "one half and two thirds, thousands of years ago.<bookmark mark='b2'/> "
        "Later, the Greeks turned fractions into ratios and "
        "proportions.<bookmark mark='b3'/> But the deeper question, exactly "
        "how many rational numbers are hiding between two others, was only "
        "answered rigorously in the eighteen seventies, when the "
        "mathematician Richard Dedekind<bookmark mark='b4'/> was building a "
        "precise theory of numbers. He proved what we are about to discover "
        "ourselves: the gap is never truly empty."
    ),
    "bridge": (
        "Here is our first trick.<bookmark mark='b1'/> Take the two numbers "
        "at the edges of the canyon, zero and one,<bookmark mark='b2'/> and "
        "average them. Add them, and divide by two.<bookmark mark='b3'/> "
        "Zero plus one over two gives us one half.<bookmark mark='b4'/> "
        "Watch our explorer zoom in twice, and plant a flag exactly in the "
        "middle.<bookmark mark='b5'/> One half is a brand new rational "
        "number, sitting right inside the canyon."
    ),
    "quarters": (
        "But why stop there? We can repeat the very same trick.<bookmark "
        "mark='b1'/> Average zero and one half, and we land on one "
        "quarter.<bookmark mark='b2'/> Average one half and one, and we "
        "land on three quarters.<bookmark mark='b3'/> Zooming in four times "
        "reveals two more numbers hiding inside the same tiny canyon, and "
        "neither of them existed for whole numbers at all."
    ),
    "eighths": (
        "Now zoom in even further, to a microscopic scale.<bookmark "
        "mark='b1'/> Bisect each of those little gaps again, and one "
        "eighth,<bookmark mark='b2'/> three eighths,<bookmark mark='b3'/> "
        "five eighths,<bookmark mark='b4'/> and seven eighths<bookmark "
        "mark='b5'/> all appear, one after another. Every single time we "
        "take an average, a brand new rational number is born, and there is "
        "nothing stopping us from doing this again, and again, forever."
    ),
    "example1": (
        "Let's use this trick for real. Suppose someone asks: find a "
        "rational number between one quarter and one half.<bookmark "
        "mark='b1'/> We do exactly what we practised. Average them: one "
        "quarter plus one half, over two, gives three eighths.<bookmark "
        "mark='b2'/> Check it on the line, three eighths sits neatly "
        "between one quarter and one half.<bookmark mark='b3'/> Problem "
        "solved."
    ),
    "example2": (
        "Here is a trickier one. Find a rational number between zero point "
        "three and zero point three two.<bookmark mark='b1'/> These two are "
        "already very close together, but the trick never fails us. "
        "Average them, and we get zero point three one.<bookmark "
        "mark='b2'/> It slots in perfectly.<bookmark mark='b3'/> No matter "
        "how close two rational numbers already are, their average always "
        "finds room in between."
    ),
    "endless": (
        "That is the density property. For any two rational numbers a and "
        "b, their average lies strictly between them, and it is rational "
        "too.<bookmark mark='b1'/> Repeat this forever, and the canyon is "
        "not empty at all. It becomes an endless, glowing highway of "
        "numbers,<bookmark mark='b2'/> fifty one over one "
        "hundred,<bookmark mark='b3'/> five hundred and two over one "
        "thousand,<bookmark mark='b4'/> eight hundred and ninety nine over "
        "one thousand.<bookmark mark='b5'/> Between any two rational "
        "numbers, there live infinitely many more."
    ),
    "challenge_setup": (
        "Now it's your turn!<bookmark mark='b0'/> Find one rational number "
        "that lies strictly between one-fourth and one-half."
        "<bookmark mark='b1'/> Use the halfway trick you just learned."
        "<bookmark mark='b2'/> Pause the video and work it out!"
        "<bookmark mark='b3'/>"
    ),
    "challenge_reveal": (
        "Add them up: one-fourth plus one-half, divided by two."
        "<bookmark mark='b0'/> That gives us three-eighths!"
        "<bookmark mark='b1'/> And three-eighths sits perfectly between "
        "one-fourth and one-half.<bookmark mark='b2'/>"
    ),
    "summary": (
        "Let's quickly recap what we discovered today.<bookmark mark='b1'/> "
        "First, the average of any two rational numbers always gives us a "
        "brand new rational number, sitting exactly in between "
        "them.<bookmark mark='b2'/> Second, we can repeat this trick "
        "forever, zooming in again and again, from halves, to quarters, to "
        "eighths, and beyond.<bookmark mark='b3'/> Third, it works just as "
        "well for decimals, even when two numbers are already very close "
        "together.<bookmark mark='b4'/> And that, together, is exactly what "
        "mathematicians call the density property of rational "
        "numbers.<bookmark mark='b5'/> Thank you so much for watching, and "
        "I will see you in the next lesson!"
    ),
}


class DensityPropertyLesson(VoiceoverScene):
    """Chalkboard lesson on the density property, with history and examples."""

    def construct(self) -> None:
        # create_subcaption=False: manim_voiceover's built-in subcaption
        # writer splits text by *character count* over the whole clip
        # duration, which is only a rough approximation. We build our own
        # SRT below directly from edge-tts's real per-word timestamps
        # (the same data that drives every animation's run_time), so the
        # exported .srt is ground truth for checking sync, not a guess.
        self.set_speech_service(get_speech_service(), create_subcaption=False)
        self.sfx = load_sfx()
        self._srt_entries: list[tuple[float, float, str]] = []

        self.add_background()
        self.beat_intro_real()
        self.beat_title()
        self.beat_canyon()
        self.beat_history()
        self.beat_bridge()
        self.beat_quarters()
        self.beat_eighths()
        self.beat_example1()
        self.beat_example2()
        self.beat_endless()
        self.beat_challenge()
        self.beat_summary()

        self._write_real_srt()

    # -- real (word-boundary-accurate) SRT export -------------------------
    def _capture_srt(self, tracker, words_per_line: int = 9) -> None:
        """Record caption lines for this beat using edge-tts's real
        per-word audio offsets (not a linear character-count guess), so the
        exported .srt reflects exactly when each word is actually spoken."""
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
        out_dir = Path(__file__).resolve().parent / "media" / "videos" / "density_property_lesson"
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

    # -- backdrop (mirrors every Story-Mode video) ------------------------
    def add_background(self) -> None:
        assets_dir = _ROOT / "Story-Mode-Manim-Videos" / "assets"

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
        # This replaces the old topic-label "Density of Q" left badge with
        # the dhimantAI brand badge used across the rest of the series.
        badge = self._corner_badge("Mathematics", corner="right",
                                    y=BOARD_TOP - 0.16, font_size=12,
                                    scale=16 / 12)
        badge_l = self._corner_badge("dhimantAI", corner="left",
                                      y=BOARD_TOP - 0.16, font_size=12,
                                      scale=16 / 12, text_color=BRAND_WHITE)

        # These stay on screen for the whole video -- no beat ever calls
        # self.clear(), so a single add() here is enough (unlike the sibling
        # videos, which re-add them per beat via reset_board()).
        self.add(bg, student, teacher, badge, badge_l)

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

    # -- Beat -1: Real-world hook (pizza / ruler / bill split) -----------------
    def beat_intro_real(self) -> None:
        with self.voiceover(text=NARRATION["intro_real"]) as tracker:
            pizza = self._pizza_icon()
            ruler = self._ruler_icon()
            bill = self._bill_icon()
            icons = VGroup(pizza, ruler, bill).arrange(RIGHT, buff=1.1)
            icons.move_to(np.array([BOARD_CX, BOARD_CY + 0.1, 0]))

            heading = board_text("Fractions are everywhere...", 30, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.45, 0]))
            # "Think about everyday life for a second."
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            # "...slice a pizza into equal pieces,"
            self.play(FadeIn(pizza, scale=0.6), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["pop"], gain=-14)
            # "...measure a plank of wood down to the last half centimetre,"
            self.play(FadeIn(ruler, scale=0.6), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["pop"], gain=-14)
            # "...split a dinner bill three ways,"
            self.play(FadeIn(bill, scale=0.6), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["pop"], gain=-14)
            self.play(LaggedStart(*[Indicate(i, scale_factor=1.15) for i in icons],
                                   lag_ratio=0.25),
                      run_time=rt(tracker.get_remaining_duration() * 0.7))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.intro_group = VGroup(heading, icons)
            self._capture_srt(tracker)

        self.play(FadeOut(self.intro_group))

    def _pizza_icon(self) -> VGroup:
        n = 8
        slices = VGroup(*[
            Sector(radius=0.7, angle=2 * np.pi / n,
                   start_angle=i * 2 * np.pi / n,
                   stroke_color=CHALK_AMBER, stroke_width=2,
                   fill_color=CHALK_AMBER if i < 3 else "#2A3B2A",
                   fill_opacity=0.55 if i < 3 else 0.15)
            for i in range(n)
        ])
        label = board_text("3/8 of a pizza", 20, CHALK_AMBER).next_to(slices, DOWN, buff=0.25)
        return VGroup(slices, label)

    def _ruler_icon(self) -> VGroup:
        body = Rectangle(width=2.4, height=0.5, stroke_color=CHALK_CYAN,
                          stroke_width=2, fill_color="#2A3B3B", fill_opacity=0.3)
        ticks = VGroup(*[
            Line(np.array([x, -0.25, 0]), np.array([x, -0.25 + (0.18 if i % 2 == 0 else 0.1), 0]),
                 stroke_color=CHALK_CYAN, stroke_width=1.5)
            for i, x in enumerate(np.linspace(-1.15, 1.15, 13))
        ])
        label = board_text("12.5 cm", 20, CHALK_CYAN).next_to(body, DOWN, buff=0.25)
        return VGroup(body, ticks, label)

    def _bill_icon(self) -> VGroup:
        receipt = RoundedRectangle(corner_radius=0.08, width=1.3, height=1.5,
                                    stroke_color=CHALK_PINK, stroke_width=2,
                                    fill_color="#3B2A33", fill_opacity=0.3)
        lines = VGroup(*[
            Line(np.array([-0.45, y, 0]), np.array([0.45, y, 0]),
                 stroke_color=CHALK_PINK, stroke_width=1.5, stroke_opacity=0.6)
            for y in np.linspace(0.5, -0.2, 4)
        ])
        label = board_text("1/3 each", 20, CHALK_PINK).next_to(receipt, DOWN, buff=0.25)
        return VGroup(receipt, lines, label)

    # -- Beat 0: Title -----------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            title = board_text("Density Property of", 40, CHALK_WHITE, "BOLD")
            title2 = board_text("Rational Numbers", 44, CHALK_YELLOW, "BOLD")
            group = VGroup(title, title2).arrange(DOWN, buff=0.25)
            group.move_to(np.array([BOARD_CX, BOARD_CY, 0]))

            # Nothing on screen while the narrator sets up the sentence;
            # the title itself appears exactly as "the density property" is said.
            self.wait(rt(tracker.time_until_bookmark("b1"), 0.0))
            self.play(Write(title), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(Write(title2), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-12)
            self.play(Circumscribe(title2, color=CHALK_CYAN, stroke_width=3),
                      run_time=rt(tracker.get_remaining_duration() * 0.7))
            self.title_group = group
            self._capture_srt(tracker)

        self.play(FadeOut(self.title_group))

    # -- Beat 1: The Canyon --------------------------------------------------
    def beat_canyon(self) -> None:
        with self.voiceover(text=NARRATION["canyon"]) as tracker:
            line = make_number_line(-1, 2, [-1, 0, 1, 2])
            self.line = line
            self.vmin, self.vmax = -1.0, 2.0

            # "Look at zero and one." — the bare line appears.
            self.play(Create(line[0]), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["swipe"], gain=-16)
            # "They are neighbours. Successive integers." — ticks land.
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in line[1]],
                                   lag_ratio=0.25),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-16)

            x0 = line.to_x(0)
            x1 = line.to_x(1)
            canyon = self._canyon_shape(x0, x1, LINE_Y)
            qmark = board_text("?", 40, CHALK_AMBER, "BOLD").move_to(
                np.array([(x0 + x1) / 2, LINE_Y - 0.85, 0]))
            # "...search and search and find nothing." — the canyon opens up,
            # then the question mark lands right as the bookmark is reached.
            self.play(FadeIn(canyon), run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            self.play(Write(qmark), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["pop"], gain=-14)

            label = board_text("no integers here!", 24, CHALK_PINK).next_to(
                canyon, DOWN, buff=0.3)
            # "...canyon with no integer bridge across it." — the label appears.
            self.play(FadeIn(label, shift=UP * 0.1), run_time=rt(tracker.time_until_bookmark("b4")))

            self.canyon_group = VGroup(canyon, qmark, label)
            self._capture_srt(tracker)

        self.play(FadeOut(self.canyon_group), FadeOut(self.line))

    def _canyon_shape(self, x0: float, x1: float, y: float) -> VGroup:
        n = 7
        top_pts = []
        for i in range(n + 1):
            xx = x0 + (x1 - x0) * i / n
            depth = 0.5 if i % 2 else 0.0
            top_pts.append(np.array([xx, y - 0.18 - depth, 0]))
        bottom_pts = [np.array([x1, y - 1.5, 0]), np.array([x0, y - 1.5, 0])]
        poly = Polygon(*top_pts, *bottom_pts, stroke_color=CHALK_AMBER,
                        stroke_width=2, fill_color=CHALK_AMBER, fill_opacity=0.12)
        return VGroup(poly)

    # -- Beat 2: History -------------------------------------------------------
    def beat_history(self) -> None:
        with self.voiceover(text=NARRATION["history"]) as tracker:
            heading = board_text("A Little History", 34, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.45, 0]))
            # "Fractions themselves are ancient." — heading appears.
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            tl_y = BOARD_CY + 0.9
            tl = Line(np.array([BOARD_LEFT + 0.6, tl_y, 0]),
                      np.array([BOARD_RIGHT - 0.6, tl_y, 0]),
                      stroke_color=CHALK_WHITE, stroke_width=3)

            events = [
                (0.12, "~3000 BCE", "Egypt & Babylon:", "fractions for trade"),
                (0.5, "Ancient Greece", "ratios &", "proportions"),
                (0.92, "1872", "Dedekind formalises", "the real numbers"),
            ]
            nodes = VGroup()
            for frac, top_line, l1, l2 in events:
                px = BOARD_LEFT + 0.6 + frac * ((BOARD_RIGHT - 0.6) - (BOARD_LEFT + 0.6))
                pos = np.array([px, tl_y, 0])
                node = timeline_node(pos, CHALK_CYAN)
                yr = board_text(top_line, 20, CHALK_YELLOW, "BOLD").next_to(pos, UP, buff=0.22)
                cap = VGroup(
                    board_text(l1, 18, CHALK_WHITE),
                    board_text(l2, 18, CHALK_WHITE),
                ).arrange(DOWN, buff=0.06).next_to(pos, DOWN, buff=0.3)
                nodes.add(VGroup(node, yr, cap))

            # "Egyptian and Babylonian traders..." — timeline + first node.
            self.play(Create(tl), GrowFromCenter(nodes[0]),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)
            # "Later, the Greeks turned fractions into ratios and proportions."
            self.play(GrowFromCenter(nodes[1]), run_time=rt(tracker.time_until_bookmark("b3")))
            # "...Richard Dedekind..." — third node lands.
            self.play(GrowFromCenter(nodes[2]), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.play(Indicate(nodes[2], scale_factor=1.25, color=CHALK_PINK),
                      run_time=rt(tracker.get_remaining_duration() * 0.6))

            self.history_group = VGroup(heading, tl, nodes)
            self._capture_srt(tracker)

        self.play(FadeOut(self.history_group))

    # -- Beat 3: The Halfway Bridge -------------------------------------------
    def beat_bridge(self) -> None:
        with self.voiceover(text=NARRATION["bridge"]) as tracker:
            old = self.line

            zoom_rect = Rectangle(
                width=old.to_x(1) - old.to_x(0) + 0.3, height=1.0,
                stroke_color=CHALK_CYAN, stroke_width=3,
            ).move_to(np.array([(old.to_x(0) + old.to_x(1)) / 2, LINE_Y, 0]))
            # "Here is our first trick." — highlight the zoom target.
            self.play(Create(zoom_rect), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-16)

            new_line = make_number_line(0, 1, [0, 1])
            # "...zero and one," — zoom into [0, 1].
            self.play(FadeOut(old), FadeOut(zoom_rect), FadeIn(new_line),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-16)
            self.line = new_line
            self.vmin, self.vmax = 0.0, 1.0

            mid_x = new_line.to_x(0.5)
            eq = chalk_math(r"\frac{0+1}{2}=\frac{1}{2}", 34, CHALK_WHITE).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.55, 0]))
            # "...gives us one half." — equation finishes writing on that word.
            self.play(Write(eq), run_time=rt(tracker.time_until_bookmark("b4")))

            flag = drop_flag(np.array([mid_x, LINE_Y, 0]), color=CHALK_PINK)
            half_label = board_text("1/2", 28, CHALK_PINK).next_to(
                np.array([mid_x, LINE_Y, 0]), DOWN, buff=0.32)
            # "...plant a flag exactly in the middle." — flag drops.
            self.play(GrowFromPoint(flag, np.array([mid_x, LINE_Y + 1.2, 0])),
                      FadeIn(half_label), run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["pop"], gain=-14)
            self.play(Flash(np.array([mid_x, LINE_Y, 0]), color=CHALK_PINK,
                             flash_radius=0.5), run_time=rt(tracker.get_remaining_duration() * 0.6))
            self.add_sound(self.sfx["ding"], gain=-12)

            self.mid_flag = VGroup(flag, half_label)
            self.eq_card = eq
            self._capture_srt(tracker)

        self.play(FadeOut(self.eq_card))

    # -- Beat 4: Quarters ------------------------------------------------------
    def beat_quarters(self) -> None:
        with self.voiceover(text=NARRATION["quarters"]) as tracker:
            line = self.line

            eq1 = chalk_math(r"\frac{0+\frac12}{2}=\frac14", 28, CHALK_CYAN)
            eq2 = chalk_math(r"\frac{\frac12+1}{2}=\frac34", 28, CHALK_CYAN)
            eqs = VGroup(eq1, eq2).arrange(RIGHT, buff=1.0).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.5, 0]))

            marks = VGroup()
            for v, col in ((0.25, CHALK_GREEN), (0.75, CHALK_GREEN)):
                px = line.to_x(v)
                pos = np.array([px, LINE_Y, 0])
                tick = Line(pos + UP * 0.11, pos + DOWN * 0.11,
                            stroke_color=col, stroke_width=4)
                mark = small_dot_label(pos, _frac_label(v), col, col)
                marks.add(VGroup(tick, mark))

            # "...we land on one quarter." — first equation + 1/4 mark together.
            self.play(Write(eq1), GrowFromCenter(marks[0]),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            # "...we land on three quarters." — second equation + 3/4 mark.
            self.play(Write(eq2), GrowFromCenter(marks[1]),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-12)
            self.play(LaggedStart(*[Indicate(m, scale_factor=1.3) for m in marks],
                                   lag_ratio=0.35),
                      run_time=rt(tracker.get_remaining_duration() * 0.7))

            self.quarter_marks = marks
            self.quarter_eqs = eqs
            self._capture_srt(tracker)

        self.play(FadeOut(self.quarter_eqs))

    # -- Beat 5: Eighths (microscopic) -----------------------------------------
    def beat_eighths(self) -> None:
        with self.voiceover(text=NARRATION["eighths"]) as tracker:
            line = self.line

            # Lower and further from the corner than before -- at
            # (BOARD_RIGHT-0.9, BOARD_TOP-0.6) the lens overlapped the
            # "Mathematics" corner badge.
            mag = self._magnifier().move_to(
                np.array([BOARD_RIGHT - 1.3, BOARD_TOP - 1.1, 0]))
            # "...to a microscopic scale." — magnifier appears and wiggles.
            self.play(FadeIn(mag, scale=0.6), run_time=rt(tracker.time_until_bookmark("b1") * 0.6))
            self.play(Wiggle(mag), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-16)

            eighths = [0.125, 0.375, 0.625, 0.875]
            marks = VGroup()
            for v in eighths:
                px = line.to_x(v)
                pos = np.array([px, LINE_Y, 0])
                tick = Line(pos + UP * 0.08, pos + DOWN * 0.08,
                            stroke_color=CHALK_PINK, stroke_width=3)
                dot = Dot(pos, radius=0.05, color=CHALK_PINK)
                lbl = board_text(_frac_label(v), 20, CHALK_PINK).next_to(
                    pos, UP, buff=0.22)
                marks.add(VGroup(tick, dot, lbl))

            # Each eighth appears exactly as its own word is spoken.
            self.play(FadeIn(marks[0], scale=0.4), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-14)
            self.play(FadeIn(marks[1], scale=0.4), run_time=rt(tracker.time_until_bookmark("b3")))
            self.play(FadeIn(marks[2], scale=0.4), run_time=rt(tracker.time_until_bookmark("b4")))
            self.play(FadeIn(marks[3], scale=0.4), run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["click"], gain=-14)
            self.play(LaggedStart(*[Flash(m[1].get_center(), color=CHALK_PINK,
                                           flash_radius=0.3) for m in marks],
                                   lag_ratio=0.22),
                      run_time=rt(tracker.get_remaining_duration() * 0.8))

            self.eighth_marks = marks
            self.mag = mag
            self._capture_srt(tracker)

        self.play(
            FadeOut(self.mag), FadeOut(self.eighth_marks),
            FadeOut(self.quarter_marks), FadeOut(self.mid_flag),
            FadeOut(self.line),
        )

    def _magnifier(self) -> VGroup:
        """A magnifying glass with a wooden-toned handle and a glass
        highlight on the lens, instead of a bare circle-plus-line."""
        lens = Circle(radius=0.32, stroke_color=CHALK_CYAN, stroke_width=4,
                       fill_color=CHALK_CYAN, fill_opacity=0.1)
        lens_highlight = Circle(radius=0.1, stroke_width=0, fill_color=CHALK_WHITE,
                                 fill_opacity=0.3).move_to(
            lens.get_center() + np.array([-0.1, 0.1, 0]))
        handle = Line(lens.get_center() + np.array([0.22, -0.22, 0]),
                      lens.get_center() + np.array([0.55, -0.55, 0]),
                      stroke_color="#8B5A2B", stroke_width=6)
        grip = Circle(radius=0.05, stroke_width=0, fill_color="#8B5A2B",
                      fill_opacity=1).move_to(handle.get_end())
        return VGroup(handle, grip, lens, lens_highlight)

    # -- Beat 6: Example 1 — between 1/4 and 1/2 --------------------------------
    def beat_example1(self) -> None:
        with self.voiceover(text=NARRATION["example1"]) as tracker:
            heading = board_text("Example 1", 32, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.4, 0]))
            prompt = board_text("Find a rational number between 1/4 and 1/2",
                                 26, CHALK_WHITE).next_to(heading, DOWN, buff=0.28)
            # "...find a rational number between one quarter and one half."
            self.play(Write(heading), FadeIn(prompt, shift=UP * 0.1),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            line = make_number_line(0.15, 0.6, [0.25, 0.5])
            self.line = line
            # A quick beat to draw the reference line before the working starts.
            self.play(Create(line[0]), LaggedStart(*[FadeIn(t) for t in line[1]],
                                                     lag_ratio=0.3),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.35))
            self.add_sound(self.sfx["click"], gain=-16)

            eq = chalk_math(r"\frac{\frac14+\frac12}{2}=\frac38", 32, CHALK_CYAN).next_to(
                prompt, DOWN, buff=0.35)
            # "...gives three eighths." — equation lands.
            self.play(Write(eq), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            mid_x = line.to_x(0.375)
            mark = small_dot_label(np.array([mid_x, LINE_Y, 0]), "3/8", CHALK_PINK, CHALK_PINK)
            # "...three eighths sits neatly between..." — mark drops on the line.
            self.play(GrowFromCenter(mark), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(Flash(np.array([mid_x, LINE_Y, 0]), color=CHALK_PINK, flash_radius=0.4),
                       run_time=rt(tracker.get_remaining_duration() * 0.7))
            self.add_sound(self.sfx["success"], gain=-12)

            self.ex1_group = VGroup(heading, prompt, eq, line, mark)
            self._capture_srt(tracker)

        self.play(FadeOut(self.ex1_group))

    # -- Beat 7: Example 2 — between 0.3 and 0.32 (decimals) ---------------------
    def beat_example2(self) -> None:
        with self.voiceover(text=NARRATION["example2"]) as tracker:
            heading = board_text("Example 2", 32, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.4, 0]))
            prompt = board_text("Find a rational number between 0.30 and 0.32",
                                 26, CHALK_WHITE).next_to(heading, DOWN, buff=0.28)
            # "...between zero point three and zero point three two."
            self.play(Write(heading), FadeIn(prompt, shift=UP * 0.1),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            decimal_label = lambda v: f"{v:.2f}"
            line = make_number_line(0.28, 0.34, [0.30, 0.32], label_fn=decimal_label)
            self.line = line
            self.play(Create(line[0]), LaggedStart(*[FadeIn(t) for t in line[1]],
                                                     lag_ratio=0.3),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.35))
            self.add_sound(self.sfx["click"], gain=-16)

            eq = chalk_math(r"\frac{0.30+0.32}{2}=0.31", 32, CHALK_CYAN).next_to(
                prompt, DOWN, buff=0.35)
            # "...we get zero point three one." — equation lands.
            self.play(Write(eq), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            mid_x = line.to_x(0.31)
            mark = small_dot_label(np.array([mid_x, LINE_Y, 0]), "0.31", CHALK_PINK, CHALK_PINK)
            # "It slots in perfectly." — mark drops on the line.
            self.play(GrowFromCenter(mark), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(Flash(np.array([mid_x, LINE_Y, 0]), color=CHALK_PINK, flash_radius=0.4),
                       run_time=rt(tracker.get_remaining_duration() * 0.4))
            self.add_sound(self.sfx["success"], gain=-12)

            close_note = board_text("still room in between — always!", 22,
                                     CHALK_GREEN).next_to(line, DOWN, buff=0.5)
            self.play(FadeIn(close_note, shift=UP * 0.1),
                      run_time=rt(tracker.get_remaining_duration() * 0.8))

            self.ex2_group = VGroup(heading, prompt, eq, line, mark, close_note)
            self._capture_srt(tracker)

        self.play(FadeOut(self.ex2_group))

    # -- Beat 8: Endless Universe / formal statement -----------------------------
    def beat_endless(self) -> None:
        with self.voiceover(text=NARRATION["endless"]) as tracker:
            statement = chalk_math(
                r"a<b \implies a<\frac{a+b}{2}<b", 34, CHALK_WHITE
            ).move_to(np.array([BOARD_CX, BOARD_TOP - 0.55, 0]))
            # "...their average lies strictly between them, and it is rational too."
            self.play(Write(statement), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            line = make_number_line(0, 1, [0, 1])
            self.line = line
            glow = VGroup(*[
                Line(np.array([LINE_X0, LINE_Y, 0]), np.array([LINE_X1, LINE_Y, 0]),
                     stroke_color=CHALK_CYAN, stroke_width=w, stroke_opacity=op)
                for w, op in ((14, 0.06), (9, 0.10), (5, 0.18))
            ])
            rng = np.random.default_rng(7)
            sparkle_vals = sorted(rng.uniform(0.02, 0.98, 26))
            sparkles = VGroup(*[
                Dot(np.array([line.to_x(v), LINE_Y, 0]), radius=0.035,
                    color=CHALK_YELLOW, fill_opacity=0.85)
                for v in sparkle_vals
            ])
            # "...glowing highway of numbers," — line, glow, and sparkles bloom.
            self.play(FadeIn(line), FadeIn(glow),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.4))
            self.add_sound(self.sfx["whoosh"], gain=-13)
            self.play(LaggedStart(*[GrowFromCenter(s) for s in sparkles], lag_ratio=0.05),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-14)

            # Card anchor x-positions are spread evenly across the board so
            # that two values close together on the line (0.51 and 0.502)
            # never produce overlapping cards; each card still points down
            # to its true position on the line via a connector line.
            fracs = [(0.51, "51/100"), (0.502, "502/1000"), (0.899, "899/1000")]
            anchor_xs = np.linspace(LINE_X0 + 0.9, LINE_X1 - 0.9, len(fracs))
            frac_cards = []
            for anchor_x, (v, s) in zip(anchor_xs, fracs):
                px = line.to_x(v)
                card = self._pop_card(s).move_to(np.array([anchor_x, LINE_Y + 1.0, 0]))
                arrow = Line(np.array([px, LINE_Y + 0.15, 0]), card.get_bottom(),
                             stroke_color=CHALK_AMBER, stroke_width=2)
                frac_cards.append(VGroup(arrow, card))

            # "fifty one over one hundred," — first card.
            self.play(FadeIn(frac_cards[0], shift=UP * 0.2),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["pop"], gain=-14)
            # "five hundred and two over one thousand," — second card.
            self.play(FadeIn(frac_cards[1], shift=UP * 0.2),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            # "eight hundred and ninety nine over one thousand." — third card.
            self.play(FadeIn(frac_cards[2], shift=UP * 0.2),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["pop"], gain=-14)

            frac_cards_group = VGroup(*frac_cards)
            self.play(FadeOut(statement), FadeOut(frac_cards_group), run_time=0.15)

            takeaway = board_text("Infinitely many rational numbers", 30,
                                   CHALK_WHITE, "BOLD")
            takeaway2 = board_text("live between any two numbers!", 30,
                                    CHALK_YELLOW, "BOLD")
            # Sits lower/more centred on the board, clear of the top edge.
            take_group = VGroup(takeaway, takeaway2).arrange(DOWN, buff=0.2).move_to(
                np.array([BOARD_CX, BOARD_CY + 1.5, 0]))
            # "Between any two rational numbers, there live infinitely many more."
            self.play(Write(take_group), run_time=rt(tracker.get_remaining_duration() * 0.6))
            self.add_sound(self.sfx["success"], gain=-11)
            self.play(Circumscribe(take_group, color=CHALK_CYAN, stroke_width=3,
                                    time_width=0.6),
                      run_time=rt(tracker.get_remaining_duration()))

            self.final_group = VGroup(line, glow, sparkles, take_group)
            self._capture_srt(tracker)

        self.play(FadeOut(self.final_group))

    def bullet_row(self, n: int, lines: list[str], *, color: str = CHALK_CYAN) -> VGroup:
        """One numbered summary point. `lines` may be 1-2 strings so a point
        that needs to wrap still carries a single badge/number, not one
        badge per visual line."""
        badge = Circle(radius=0.19, stroke_color=color, stroke_width=2,
                        fill_color=color, fill_opacity=0.18)
        num = board_text(str(n), 18, color, "BOLD").move_to(badge.get_center())
        text_block = VGroup(*[board_text(t, 24, CHALK_WHITE) for t in lines]).arrange(
            DOWN, buff=0.06, aligned_edge=LEFT)
        row = VGroup(VGroup(badge, num), text_block).arrange(RIGHT, buff=0.3)
        # Keep the badge vertically centred on the whole text block, not just
        # its first line, when a point wraps to two lines.
        VGroup(badge, num).move_to(np.array([row[0].get_x(), text_block.get_y(), 0]))
        return row

    # -- Beat 8.5: YOUR TURN -------------------------------------------------
    def beat_challenge(self) -> None:
        """YOUR TURN -- find a rational number between 1/4 and 1/2, using
        the halfway trick. Follows the series pattern established across
        the other Story-Mode videos: a bordered box that fills the board,
        round THINK countdown badge, whole-board dim while it counts down."""
        box_y = BOARD_CY - 0.2
        with self.voiceover(text=NARRATION["challenge_setup"]) as tracker:
            heading = board_text("YOUR TURN", size=34, weight="BOLD",
                                 color=CHALK_PINK).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.55, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            box = RoundedRectangle(width=8.8, height=4.6, corner_radius=0.16,
                                    stroke_color=CHALK_CYAN, stroke_width=2,
                                    fill_color="#1E2A1E", fill_opacity=0.3).move_to(
                np.array([BOARD_CX, box_y, 0]))
            question = board_text("Find a rational number between:", size=24,
                                  color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, box_y + 1.85, 0]))
            nums = chalk_math(r"\frac14 \quad \text{and} \quad \frac12", size=48,
                              color=CHALK_YELLOW).move_to(np.array([BOARD_CX, box_y + 0.9, 0]))
            self.play(Create(box), Write(question), Write(nums),
                     run_time=rt(tracker.time_until_bookmark("b1")))

            hint = board_text("Hint: try the halfway trick!", size=22,
                              color=CHALK_CYAN).move_to(np.array([BOARD_CX, box_y - 0.3, 0]))
            self.play(FadeIn(hint), run_time=rt(tracker.time_until_bookmark("b2")))

            pause_lbl = board_text("Pause and try it!", size=22, color=CHALK_AMBER).move_to(
                np.array([BOARD_CX, box_y - 1.1, 0]))
            self.play(FadeIn(pause_lbl), run_time=rt(tracker.time_until_bookmark("b3")))

            self._capture_srt(tracker)

        # Consistent 10-second challenge clock (whole series): a round
        # THINK badge at board centre dims the WHOLE board (question box
        # included) except itself while students think.
        play_challenge_countdown(self, seconds=10, sfx=self.sfx)

        with self.voiceover(text=NARRATION["challenge_reveal"]) as tracker:
            self.play(FadeOut(hint), FadeOut(pause_lbl),
                     run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            work = chalk_math(r"\frac{\frac14+\frac12}{2}", size=38, color=CHALK_WHITE)
            result = chalk_math(r"=\frac38", size=42, color=CHALK_YELLOW)
            VGroup(work, result).arrange(RIGHT, buff=0.4).move_to(
                np.array([BOARD_CX, box_y - 0.5, 0]))
            self.play(Write(work), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.play(Write(result), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["success"], gain=-11)

            confirm = chalk_math(r"\frac14<\frac38<\frac12", size=34,
                                 color=CHALK_GREEN).move_to(np.array([BOARD_CX, box_y - 1.6, 0]))
            self.play(Write(confirm), Indicate(confirm, color=CHALK_GREEN, scale_factor=1.05),
                     run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            self.challenge_group = VGroup(heading, box, question, nums, work, result, confirm)
            self._capture_srt(tracker)

        self.play(FadeOut(self.challenge_group))

    # -- Beat 9: Summary + Thank You ---------------------------------------------
    def beat_summary(self) -> None:
        with self.voiceover(text=NARRATION["summary"]) as tracker:
            heading = board_text("Summary", 36, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.5, 0]))
            # "Let's quickly recap what we discovered today."
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            bullets = VGroup(
                self.bullet_row(1, ["The average of two rational numbers is always",
                                     "a new rational number, sitting between them."]),
                self.bullet_row(2, ["Repeat the trick forever: halves, quarters,",
                                     "eighths, and beyond — it never runs out."]),
                self.bullet_row(3, ["It works for decimals too, no matter how close",
                                     "two numbers already are."]),
            )
            bullets.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            bullets.move_to(np.array([BOARD_CX, BOARD_CY + 0.15, 0]))

            # "...sitting exactly in between them." — point 1.
            self.play(FadeIn(bullets[0], shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)
            # "...from halves, to quarters, to eighths, and beyond." — point 2.
            self.play(FadeIn(bullets[1], shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)
            # "...even when two numbers are already very close together." — point 3.
            self.play(FadeIn(bullets[2], shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            tag = board_text("— the Density Property of Rational Numbers",
                              24, CHALK_YELLOW, "BOLD").next_to(bullets, DOWN, buff=0.35)
            # "...density property of rational numbers." — the name lands.
            self.play(FadeIn(tag, shift=UP * 0.1), run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["success"], gain=-12)

            summary_group = VGroup(heading, bullets, tag)
            self.play(FadeOut(summary_group), run_time=rt(tracker.get_remaining_duration() * 0.25))

            thanks = board_text("Thank You for Watching!", 42, CHALK_WHITE, "BOLD")
            thanks2 = board_text("See you in the next lesson :)", 26, CHALK_CYAN)
            thanks_group = VGroup(thanks, thanks2).arrange(DOWN, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY, 0]))
            # "Thank you so much for watching, and I will see you in the next lesson!"
            self.play(Write(thanks), run_time=rt(tracker.get_remaining_duration() * 0.6))
            self.add_sound(self.sfx["ding"], gain=-11)
            self.play(FadeIn(thanks2, shift=UP * 0.1),
                      run_time=rt(tracker.get_remaining_duration()))
            self.play(Circumscribe(thanks_group, color=CHALK_AMBER, stroke_width=3,
                                    time_width=0.6), run_time=0.6)
            self.add_sound(self.sfx["success"], gain=-11)

            self.thanks_group = thanks_group
            self._capture_srt(tracker)

        self.wait(END_HOLD)

    def _pop_card(self, s: str) -> VGroup:
        lbl = board_text(s, 24, CHALK_AMBER, "BOLD")
        frame = RoundedRectangle(
            corner_radius=0.1, width=lbl.width + 0.4, height=lbl.height + 0.3,
            stroke_color=CHALK_AMBER, stroke_width=2,
            fill_color="#1E2A1E", fill_opacity=0.55,
        )
        lbl.move_to(frame.get_center())
        return VGroup(frame, lbl)

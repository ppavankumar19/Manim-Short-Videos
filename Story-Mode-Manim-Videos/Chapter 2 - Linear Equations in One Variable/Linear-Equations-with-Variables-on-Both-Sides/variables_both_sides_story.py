"""
Linear Equations with Variables on Both Sides — Bring Like Terms Together
Story-mode chalkboard lesson (Telangana Class 8 Maths, Chapter 2:
Linear Equations in One Variable, Section 2.4).

Core idea: when the unknown appears on BOTH sides, collect the variable terms
together on one side and the number terms together on the other, combine the
like terms, then isolate the variable -- and check the answer on both sides.
Brackets are shown as packages that must be opened (distributed) first.

Production pipeline (mirrors the rest of the Story-Mode series):
  - shared assets/background2.png chalkboard + student/teacher cutouts +
    dhimantAI (top-left) and Mathematics (top-right) corner badges.
  - VoiceoverScene + speech service; narration written as natural prose.
  - synced_voice.install_synced_voiceover() re-times every word against the
    real audio (keeps the same voice, fixes the timeline).
  - real per-word SRT export (carry-safe timestamps).
  - sound effects from sound_effects.py, chalk-styled Text/MathTex.
  - story_common.play_challenge_countdown() for the "YOUR TURN" clock.

Title + 10 beats:
  0. Title card.
  1. X on Both Sides       -- 5x-12 = 2x-6 with x-tiles on both sides.
  2. Gather the Variables  -- the 2x tiles cross over and cancel: 3x-12 = -6.
  3. Gather the Constants  -- -12 crosses as +12: 3x = -6+12 = 6.
  4. Isolate x             -- 3 x x = 6 -> x = 6/3 -> x = 2.
  5. Check Both Sides      -- 5(2)-12 = 2(2)-6 -> -2 = -2.
  6. Brackets First        -- 3(x-3) = 5(2x-1) -> x = -4/7.
  7. The Complete Strategy -- Simplify / Group / Solve / Check.
  8. Ages Application      -- Karthik & Ananya: 49x+70 = 45x+90 -> 35 and 25.
  9. Student Challenge     -- 7x - 5 = 2x with the 10 s THINK clock -> x = 1.
 10. Summary + outtro.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
_ROOT = next(p for p in _HERE.parents
        if (p / "speech_service.py").exists())
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from manim import (
    ORIGIN, UP, DOWN, LEFT, RIGHT, PI, TAU, BLACK,
    ImageMobject, MathTex, VGroup, Line, Circle, Rectangle, RoundedRectangle,
    Arrow, Text, Write, FadeIn, FadeOut, Create, ReplacementTransform,
    TransformMatchingTex, TransformFromCopy, GrowArrow, Indicate, Flash,
    Circumscribe, SurroundingRectangle, config,
)
from manim_voiceover import VoiceoverScene
from manim_voiceover.tracker import AUDIO_OFFSET_RESOLUTION

from speech_service import get_speech_service
from sound_effects import load_all as load_sfx
from story_common import play_challenge_countdown
from synced_voice import install_synced_voiceover

# --------------------------------------------------------------- theme -----
CHALK_WHITE = "#F5F2E9"
BRAND_WHITE = "#FFFFFF"
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

BOARD_LEFT = -4.6
BOARD_RIGHT = 5.6
BOARD_TOP = 3.3
BOARD_BOTTOM = -2.9
BOARD_CX = (BOARD_LEFT + BOARD_RIGHT) / 2  # 0.5
BOARD_CY = (BOARD_TOP + BOARD_BOTTOM) / 2  # 0.2

EQ_Y = 0.45        # main equation line
TILE_Y = 1.45      # x-tile rows sit above the equation


def rt(seconds: float, floor: float = MIN_RT) -> float:
    return max(floor, float(seconds))


def board_text(s: str, size: int = 34, color: str = CHALK_WHITE,
               weight: str = "NORMAL") -> Text:
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def chalk_math(s: str, size: int = 34, color: str = MATH_COLOR) -> MathTex:
    return MathTex(s, font_size=size, color=color)


def align_equals(eq: MathTex, cx: float = BOARD_CX, cy: float = EQ_Y) -> MathTex:
    """Centre the whole equation line on the board."""
    eq.move_to(np.array([cx, cy, 0.0]))
    return eq


def check_mark(color: str = CHALK_GREEN, size: float = 0.4,
               width: float = 5) -> VGroup:
    a = np.array([-0.52, 0.16, 0.0]) * size
    b = np.array([-0.16, -0.30, 0.0]) * size
    c = np.array([0.52, 0.40, 0.0]) * size
    return VGroup(Line(a, b, color=color, stroke_width=width),
                  Line(b, c, color=color, stroke_width=width))


def tick_beside(target, color: str = CHALK_GREEN, size: float = 0.4,
                buff: float = 0.3) -> VGroup:
    mark = check_mark(color, size)
    mark.next_to(target, RIGHT, buff=buff)
    mark.shift(UP * (target.get_center()[1] - mark.get_center()[1]))
    return mark


# ------------------------------------------------------------- algebra tiles --
def x_tile(color: str = CHALK_CYAN, size: float = 0.4) -> VGroup:
    """One x-tile: the visible unit of the unknown."""
    box = RoundedRectangle(corner_radius=0.06, width=size, height=size,
                           stroke_color=color, stroke_width=1.8,
                           fill_color="#123333", fill_opacity=0.8)
    lbl = MathTex("x", font_size=20, color=color).move_to(box.get_center())
    return VGroup(box, lbl)


def num_tile(label: str, color: str = CHALK_PINK, size: float = 0.4) -> VGroup:
    """One number tile (a constant)."""
    box = RoundedRectangle(corner_radius=0.06, width=size, height=size,
                           stroke_color=color, stroke_width=1.8,
                           fill_color="#2E1020", fill_opacity=0.8)
    lbl = MathTex(label, font_size=18, color=color).move_to(box.get_center())
    return VGroup(box, lbl)


def tile_row(n: int, color: str = CHALK_CYAN, size: float = 0.4,
             buff: float = 0.07) -> VGroup:
    return VGroup(*[x_tile(color, size) for _ in range(n)]).arrange(RIGHT, buff=buff)


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "Today we solve a new kind of equation — one where the unknown appears "
        "on both sides.<bookmark mark='b0'/> We will bring the variable terms "
        "together, and the number terms together.<bookmark mark='b1'/> Let's "
        "start with the example!<bookmark mark='b2'/>"
    ),
    "scene1": (
        "Five x minus twelve equals two x minus six.<bookmark mark='b0'/> Look "
        "closely: the same unknown, x, is on both sides.<bookmark mark='b1'/> "
        "There are five x tiles on the left, and two x tiles on the right."
        "<bookmark mark='b2'/> Earlier the unknown stayed on one side, so now "
        "we must collect it together.<bookmark mark='b3'/> How do we isolate x "
        "this time?<bookmark mark='b4'/>"
    ),
    "scene2": (
        "First, bring the variable terms together.<bookmark mark='b0'/> The two "
        "x on the right must cross the equals sign — and there they become "
        "minus two x.<bookmark mark='b1'/> Five x minus two x leaves three x."
        "<bookmark mark='b2'/> So the equation becomes three x minus twelve "
        "equals minus six.<bookmark mark='b3'/>"
    ),
    "scene3": (
        "Now bring the numbers together.<bookmark mark='b0'/> Minus twelve must "
        "cross to the other side, and there it becomes plus twelve."
        "<bookmark mark='b1'/> Three x equals minus six plus twelve."
        "<bookmark mark='b2'/> Minus six plus twelve is six, so three x equals "
        "six.<bookmark mark='b3'/>"
    ),
    "scene4": (
        "Now isolate x.<bookmark mark='b0'/> Three x means three times x, so we "
        "undo it with division.<bookmark mark='b1'/> Divide both sides by "
        "three: x equals six divided by three.<bookmark mark='b2'/> Six divided "
        "by three is two.<bookmark mark='b3'/> x equals two — that is the "
        "solution.<bookmark mark='b4'/>"
    ),
    "scene5": (
        "A solution must work on both sides, so let's check it."
        "<bookmark mark='b0'/> Put two in place of x: five times two minus "
        "twelve, and two times two minus six.<bookmark mark='b1'/> On the left, "
        "ten minus twelve is minus two. On the right, four minus six is also "
        "minus two.<bookmark mark='b2'/> Both sides are equal: minus two equals "
        "minus two.<bookmark mark='b3'/> The solution is verified."
        "<bookmark mark='b4'/>"
    ),
    "scene6": (
        "What if both sides have brackets?<bookmark mark='b0'/> Open the "
        "brackets first: the three multiplies both terms inside, giving three x "
        "minus nine, and the five multiplies both terms, giving ten x minus "
        "five.<bookmark mark='b1'/> Now it is the pattern we know: bring the "
        "variable terms together. Three x minus ten x equals minus five plus "
        "nine.<bookmark mark='b2'/> That gives minus seven x equals four, so x "
        "equals minus four over seven.<bookmark mark='b3'/>"
    ),
    "scene7": (
        "Here is the complete strategy.<bookmark mark='b0'/> Simplify any "
        "brackets first.<bookmark mark='b1'/> Then bring the variable terms "
        "together.<bookmark mark='b2'/> Bring the number terms together, and "
        "solve.<bookmark mark='b3'/> Finally, check your answer on both sides."
        "<bookmark mark='b4'/>"
    ),
    "scene8": (
        "Let's use this on a real problem.<bookmark mark='b0'/> Karthik and "
        "Ananya's ages are in the ratio seven to five, so let Karthik be seven x "
        "and Ananya be five x.<bookmark mark='b1'/> Ten years later their ages "
        "are seven x plus ten and five x plus ten, and the ratio becomes nine "
        "to seven.<bookmark mark='b2'/> Multiplying across gives forty nine x "
        "plus seventy equals forty five x plus ninety.<bookmark mark='b3'/> "
        "Bring the variable terms together: forty nine x minus forty five x "
        "equals ninety minus seventy, so four x equals twenty, and x equals "
        "five.<bookmark mark='b4'/> That makes Karthik thirty five years old, and "
        "Ananya twenty five.<bookmark mark='b5'/>"
    ),
    "scene9_setup": (
        "Your turn!<bookmark mark='b0'/> Solve seven x minus five equals two x."
        "<bookmark mark='b1'/> Where should the x terms meet?"
        "<bookmark mark='b2'/> Pause the video, and try it yourself."
        "<bookmark mark='b3'/>"
    ),
    "scene9_reveal": (
        "Bring the two x to the left: seven x minus two x equals five."
        "<bookmark mark='b0'/> That is five x equals five, so x equals one."
        "<bookmark mark='b1'/> Well done!<bookmark mark='b2'/>"
    ),
    "scene10": (
        "Let's summarise.<bookmark mark='b0'/> When the variable is on both "
        "sides, bring the variable terms together, and the number terms "
        "together.<bookmark mark='b1'/> Then combine the like terms."
        "<bookmark mark='b2'/> Simplify any brackets before you group."
        "<bookmark mark='b3'/> And always check by substituting into both "
        "sides.<bookmark mark='b4'/> Variables together, numbers together, and "
        "check. Thank you so much for watching, and I will see you in the next "
        "lesson!<bookmark mark='b5'/>"
    ),
}


class VariablesBothSidesStory(VoiceoverScene):
    """Story-mode chalkboard lesson: variables on both sides."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._srt_entries: list[tuple[float, float, str]] = []

    # -- backdrop ----------------------------------------------------------
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
            -config.frame_height / 2 + student.height / 2 - 0.1, 0]))

        teacher = ImageMobject(str(assets_dir / "teacher.png"))
        teacher.set_z_index(-5)
        teacher.height = 3.3
        teacher.move_to(np.array([
            config.frame_width / 2 - teacher.width / 2 + 0.45,
            -config.frame_height / 2 + teacher.height / 2 - 0.1, 0]))

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
            corner_radius=0.04, width=label.width + 0.24,
            height=label.height + 0.16,
            stroke_color=CHALK_AMBER, stroke_width=1.5,
            fill_color="#2A1D10", fill_opacity=0.45)
        label.move_to(frame.get_center())
        badge = VGroup(frame, label).scale(scale)
        yy = BOARD_TOP - 0.32 if y is None else y
        if corner == "left":
            badge.move_to(np.array([BOARD_LEFT + 0.55, yy, 0]))
            badge.shift(RIGHT * (BOARD_LEFT + 0.08 - badge.get_left()[0]))
        else:
            badge.move_to(np.array([BOARD_RIGHT - 0.6, yy, 0]))
            badge.shift(RIGHT * (BOARD_RIGHT - 0.013 - badge.get_right()[0]))
        badge.shift(UP * ((BOARD_TOP - 0.08) - badge.get_top()[1]))
        return badge

    def reset_board(self) -> None:
        self.clear()
        self.add(self.bg, self.student, self.teacher, self.badge, self.badge_l)

    # -- real SRT export ---------------------------------------------------
    def _capture_srt(self, tracker, words_per_line: int = 9) -> None:
        wbs = [wb for wb in tracker.data.get("word_boundaries", [])
               if wb.get("text", "").strip()]
        if not wbs:
            return
        starts = [tracker.start_t + wb["audio_offset"] / AUDIO_OFFSET_RESOLUTION
                  for wb in wbs]
        for i in range(0, len(wbs), words_per_line):
            chunk = wbs[i:i + words_per_line]
            end = starts[i + words_per_line] if i + words_per_line < len(starts) \
                else tracker.end_t
            text = " ".join(wb["text"] for wb in chunk)
            self._srt_entries.append((starts[i], end, text))

    def _write_real_srt(self) -> None:
        out_dir = _HERE / "media" / "videos" / "variables_both_sides_story"
        out_dir.mkdir(parents=True, exist_ok=True)

        def fmt(t: float) -> str:
            total_ms = int(round(max(t, 0.0) * 1000))
            h, rem = divmod(total_ms, 3_600_000)
            m, rem = divmod(rem, 60_000)
            s, ms = divmod(rem, 1000)
            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

        lines = []
        for idx, (start, end, text) in enumerate(self._srt_entries, 1):
            lines.append(str(idx))
            lines.append(f"{fmt(start)} --> {fmt(max(end, start + 0.3))}")
            lines.append(text)
            lines.append("")
        content = "\n".join(lines)
        (out_dir / f"{self.__class__.__name__}.real.srt").write_text(
            content, encoding="utf-8")
        print(f"[real SRT written] {out_dir}")
        (out_dir / "real.srt").write_text(content, encoding="utf-8")
        try:
            if (hasattr(self, "renderer") and hasattr(self.renderer, "file_writer")
                    and self.renderer.file_writer.movie_file_path):
                movie_dir = Path(self.renderer.file_writer.movie_file_path).parent
                (movie_dir / "real.srt").write_text(content, encoding="utf-8")
                (movie_dir / f"{self.__class__.__name__}.real.srt").write_text(
                    content, encoding="utf-8")
        except Exception:
            pass

    def construct(self):
        self.sfx = load_sfx()
        self.set_speech_service(get_speech_service(), create_subcaption=False)
        install_synced_voiceover(self)
        self.add_background()

        self.beat0_title()
        self.beat1_both_sides()
        self.beat2_gather_variables()
        self.beat3_gather_constants()
        self.beat4_isolate()
        self.beat5_check()
        self.beat6_brackets()
        self.beat7_strategy()
        self.beat8_ages()
        self.beat9_challenge()
        self.beat10_summary()

        self._write_real_srt()

    # ================================================================ beats ==

    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Linear Equations with Variables on Both Sides", 28, CHALK_WHITE,
                               "BOLD").move_to(np.array([BOARD_CX, BOARD_CY + 1.5, 0]))
            self.play(Write(title), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            sub = board_text("Bring like terms together", 22, CHALK_YELLOW,
                             "BOLD").move_to(np.array([BOARD_CX, BOARD_CY + 0.8, 0]))
            eq = MathTex("5x-12", r"\;=\;", "2x-6", font_size=44)
            align_equals(eq, BOARD_CX, BOARD_CY - 0.7)
            eq[0][1].set_color(CHALK_CYAN)
            eq[2][1].set_color(CHALK_CYAN)
            self.play(Write(sub), Write(eq),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)

            question = board_text("x is on both sides!", 20, CHALK_PINK,
                                  "BOLD").move_to(np.array([BOARD_CX, -1.75, 0]))
            self.play(FadeIn(question), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["swipe"], gain=-15)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 1: x on both sides -------------------------------------------
    def beat1_both_sides(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("x is on BOTH sides!", 24, CHALK_PINK,
                                 "BOLD").move_to(np.array([BOARD_CX, BOARD_TOP - 0.45, 0]))
            eq = MathTex("5x-12", r"\;=\;", "2x-6", font_size=46)
            align_equals(eq, BOARD_CX, EQ_Y)
            eq[0][1].set_color(CHALK_CYAN)
            eq[2][1].set_color(CHALK_CYAN)

            left_tiles = tile_row(5).move_to(np.array(
                [eq[0][0:2].get_center()[0], TILE_Y, 0]))
            right_tiles = tile_row(2, CHALK_GREEN).move_to(np.array(
                [eq[2][0:2].get_center()[0], TILE_Y, 0]))
            l_lbl = board_text("5 x", 14, CHALK_CYAN, "BOLD").next_to(
                left_tiles, RIGHT, buff=0.15)
            r_lbl = board_text("2 x", 14, CHALK_GREEN, "BOLD").next_to(
                right_tiles, RIGHT, buff=0.15)

            question = board_text("How do we isolate x now?", 19, CHALK_YELLOW,
                                  "BOLD").move_to(np.array([BOARD_CX, -1.15, 0]))

            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.4))
            self.play(Write(eq), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(Indicate(eq[0][1], color=CHALK_CYAN, scale_factor=1.6),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.play(Indicate(eq[2][1], color=CHALK_GREEN, scale_factor=1.6),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(left_tiles, shift=UP * 0.15),
                      FadeIn(right_tiles, shift=UP * 0.15),
                      FadeIn(l_lbl), FadeIn(r_lbl),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            self.play(Indicate(left_tiles, color=CHALK_CYAN, scale_factor=1.06),
                      Indicate(right_tiles, color=CHALK_GREEN, scale_factor=1.06),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(FadeIn(question),
                      run_time=rt(tracker.time_until_bookmark("b3")))

            both = board_text("Bring them together!", 20, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, -1.85, 0]))
            self.play(FadeIn(both), Flash(both, color=CHALK_AMBER, flash_radius=0.8),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.eq = eq
            self.left_tiles = left_tiles
            self.right_tiles = right_tiles
            self.beat1_extras = VGroup(heading, l_lbl, r_lbl, question, both)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 2: gather the variables --------------------------------------
    def beat2_gather_variables(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            eq = self.eq
            heading = board_text("Bring Variables Together", 24, CHALK_CYAN,
                                 "BOLD").move_to(np.array([BOARD_CX, BOARD_TOP - 0.45, 0]))
            self.play(FadeOut(self.beat1_extras), FadeIn(heading),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.4))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(Indicate(eq[2][0:2], color=CHALK_GREEN, scale_factor=1.3),
                      Indicate(self.right_tiles, color=CHALK_GREEN, scale_factor=1.1),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["click"], gain=-15)

            # the two x-tiles cross the '=' and turn into -2x
            apex = np.array([BOARD_CX, 2.45, 0.0])
            landing = np.array([self.left_tiles.get_right()[0] + 0.5, TILE_Y, 0.0])
            mover = self.right_tiles.copy()
            minus2x = num_tile("-2x", CHALK_GREEN, 0.62).move_to(apex)
            self.play(mover.animate.move_to(apex),
                      FadeOut(self.right_tiles),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.45))
            self.play(ReplacementTransform(mover, minus2x),
                      Flash(apex, color=CHALK_YELLOW, flash_radius=0.5),
                      run_time=0.3)
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(minus2x.animate.move_to(landing),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.45))

            e2 = MathTex("5x-2x-12", r"\;=\;", "-6", font_size=44)
            align_equals(e2, BOARD_CX, EQ_Y)
            e2[0][0].set_color(CHALK_CYAN)
            e2[0][1].set_color(CHALK_CYAN)
            self.play(TransformMatchingTex(eq, e2), FadeOut(minus2x),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            # five x-tiles minus two leaves three
            self.play(FadeOut(self.left_tiles[3:5]),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            e3 = MathTex("3x-12", r"\;=\;", "-6", font_size=44)
            align_equals(e3, BOARD_CX, EQ_Y)
            e3[0][1].set_color(CHALK_CYAN)
            self.play(TransformMatchingTex(e2, e3),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-12)

            self.eq = e3
            self.tiles3 = VGroup(*self.left_tiles[0:3])
            self.beat2_extras = VGroup(heading)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 3: gather the constants --------------------------------------
    def beat3_gather_constants(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            eq = self.eq
            heading = board_text("Bring Numbers Together", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, BOARD_TOP - 0.45, 0]))
            self.play(FadeOut(self.beat2_extras), FadeIn(heading),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.4))

            box12 = SurroundingRectangle(eq[0][2:5], color=CHALK_AMBER, buff=0.1,
                                         corner_radius=0.08, stroke_width=3)
            self.play(Create(box12),
                      run_time=rt(tracker.time_until_bookmark("b0")))

            e4 = MathTex("3x", r"\;=\;", "-6+12", font_size=44)
            align_equals(e4, BOARD_CX, EQ_Y)
            e4[0][1].set_color(CHALK_CYAN)
            landing = np.array([e4[2].get_center()[0] - 0.55, EQ_Y, 0.0])
            apex = np.array([BOARD_CX, 2.45, 0.0])
            start = eq[0][2:5].get_center()
            mover = MathTex("-12", font_size=28, color=CHALK_AMBER).move_to(start)
            self.play(mover.animate.move_to(apex),
                      eq[0][2:5].animate.set_opacity(0.25),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.45))
            mover_p = MathTex("+12", font_size=28, color=CHALK_GREEN).move_to(apex)
            self.play(ReplacementTransform(mover, mover_p),
                      Flash(apex, color=CHALK_YELLOW, flash_radius=0.45),
                      run_time=0.3)
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(mover_p.animate.move_to(landing),
                      TransformMatchingTex(eq, e4), FadeOut(mover_p),
                      FadeOut(box12),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            e5 = MathTex("3x", r"\;=\;", "6", font_size=46)
            align_equals(e5, BOARD_CX, EQ_Y)
            e5[0][1].set_color(CHALK_CYAN)
            var_lbl = board_text("VARIABLE TERM", 13, CHALK_CYAN, "BOLD").move_to(
                np.array([e5[0].get_center()[0], -0.55, 0]))
            num_lbl = board_text("CONSTANT", 13, CHALK_AMBER, "BOLD").move_to(
                np.array([e5[2].get_center()[0], -0.55, 0]))
            self.play(TransformMatchingTex(e4, e5), FadeIn(var_lbl), FadeIn(num_lbl),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-12)

            self.eq = e5
            self.beat3_extras = VGroup(heading, var_lbl, num_lbl)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 4: isolate x -------------------------------------------------
    def beat4_isolate(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            eq = self.eq
            heading = board_text("Now Isolate x", 24, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.45, 0]))
            self.play(FadeOut(self.beat3_extras), FadeIn(heading),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            e6 = MathTex(r"3\times x", r"\;=\;", "6", font_size=44)
            align_equals(e6, BOARD_CX, EQ_Y)
            e6[0][2].set_color(CHALK_CYAN)
            self.play(TransformMatchingTex(eq, e6),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.play(Circumscribe(e6[0][0:1], color=CHALK_YELLOW, stroke_width=3),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.4))

            e7 = MathTex("x", r"\;=\;", r"\frac{6}{3}", font_size=44)
            align_equals(e7, BOARD_CX, EQ_Y)
            e7[0].set_color(CHALK_CYAN)
            landing = e7[2][-1].get_center()
            apex = np.array([BOARD_CX, 2.45, 0.0])
            start = e6[0][0].get_center()
            mover = MathTex("3", font_size=28, color=CHALK_YELLOW).move_to(start)
            self.play(mover.animate.move_to(apex),
                      e6[0][0].animate.set_opacity(0.25),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.3))
            self.play(mover.animate.move_to(landing),
                      TransformMatchingTex(e6, e7), FadeOut(mover),
                      FadeOut(self.tiles3),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["success"], gain=-11)

            e8 = MathTex("x", r"\;=\;", "2", font_size=52, color=CHALK_GREEN)
            align_equals(e8, BOARD_CX, EQ_Y)
            one_tile = num_tile("2", CHALK_GREEN, 0.5)
            one_tile.move_to(np.array([eq[0].get_center()[0], TILE_Y, 0]))
            self.play(TransformMatchingTex(e7, e8), FadeIn(one_tile, scale=0.6),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-12)

            ans_box = SurroundingRectangle(e8, color=CHALK_GREEN, buff=0.2,
                                           corner_radius=0.1, stroke_width=3)
            done = board_text("x is isolated!", 18, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -0.6, 0]))
            self.play(Create(ans_box),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            self.play(FadeIn(done), Flash(e8, color=CHALK_GREEN, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self.play(Indicate(one_tile, color=CHALK_GREEN, scale_factor=1.1),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 5: check both sides ------------------------------------------
    def beat5_check(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            self.reset_board()

            heading = board_text("Check Both Sides", 24, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.45, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            sol = MathTex("x", r"\;=\;", "2", font_size=28, color=CHALK_GREEN).move_to(
                np.array([BOARD_CX, 1.9, 0]))
            eq_orig = MathTex("5x-12", r"\;=\;", "2x-6", font_size=40)
            align_equals(eq_orig, BOARD_CX, 0.95)
            eq_orig[0][1].set_color(CHALK_CYAN)
            eq_orig[2][1].set_color(CHALK_CYAN)
            self.play(FadeIn(sol), Write(eq_orig),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            sub = MathTex("5(2)-12", r"\;=\;", "2(2)-6", font_size=40)
            align_equals(sub, BOARD_CX, 0.95)
            self.play(TransformMatchingTex(eq_orig, sub),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.4))
            self.play(Indicate(sub[0], color=CHALK_CYAN, scale_factor=1.1),
                      Indicate(sub[2], color=CHALK_GREEN, scale_factor=1.1),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            step2 = MathTex("10-12", r"\;=\;", "4-6", font_size=40)
            align_equals(step2, BOARD_CX, 0.95)
            self.play(TransformMatchingTex(sub, step2),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            final = MathTex("-2", r"\;=\;", "-2", font_size=46)
            align_equals(final, BOARD_CX, 0.95)
            self.play(TransformMatchingTex(step2, final),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-12)

            ck = tick_beside(final, CHALK_GREEN, 0.44, 0.4)
            ok = board_text("LHS = RHS", 20, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -0.45, 0]))
            self.play(Create(ck), FadeIn(ok),
                      Flash(final, color=CHALK_GREEN, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            verified = board_text("Both sides are equal — the solution works!",
                                  17, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, -1.25, 0]))
            self.play(FadeIn(verified), run_time=rt(tracker.time_until_bookmark("b4")))
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 6: brackets first --------------------------------------------
    def beat6_brackets(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("Brackets? Open Them First", 24, CHALK_PINK,
                                 "BOLD").move_to(np.array([BOARD_CX, BOARD_TOP - 0.45, 0]))
            eq = MathTex(r"3(x-3)", r"\;=\;", r"5(2x-1)", font_size=44)
            align_equals(eq, BOARD_CX, EQ_Y)
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.4))
            self.play(Write(eq), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # the two brackets drawn as "packages"
            part_l = eq[0]
            part_r = eq[2]
            pack_l = SurroundingRectangle(part_l[1:6], color=CHALK_PINK, buff=0.1,
                                          corner_radius=0.12, stroke_width=2.5)
            pack_r = SurroundingRectangle(part_r[1:7], color=CHALK_AMBER, buff=0.1,
                                          corner_radius=0.12, stroke_width=2.5)
            self.play(Create(pack_l), Create(pack_r),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.25))

            # distribution: one short arrow up into each term inside the bracket
            up_y = -0.85
            def dist_arrow(term, color: str) -> Arrow:
                return Arrow(np.array([term.get_center()[0], up_y, 0.0]),
                             term.get_bottom() + DOWN * 0.10,
                             buff=0.02, color=color, stroke_width=2.4,
                             max_tip_length_to_length_ratio=0.2, tip_length=0.14)

            a1 = dist_arrow(part_l[2], CHALK_PINK)   # 3 -> x
            a2 = dist_arrow(part_l[4], CHALK_PINK)   # 3 -> 3
            a3 = dist_arrow(part_r[3], CHALK_AMBER)  # 5 -> x (of 2x)
            a4 = dist_arrow(part_r[5], CHALK_AMBER)  # 5 -> 1
            f3 = MathTex(r"\times 3", font_size=22, color=CHALK_PINK).move_to(
                np.array([(part_l[2].get_center()[0] + part_l[4].get_center()[0]) / 2,
                          up_y - 0.42, 0]))
            f5 = MathTex(r"\times 5", font_size=22, color=CHALK_AMBER).move_to(
                np.array([(part_r[3].get_center()[0] + part_r[5].get_center()[0]) / 2,
                          up_y - 0.42, 0]))
            how = board_text("multiply every term inside", 16, CHALK_WHITE).move_to(
                np.array([BOARD_CX, up_y - 0.95, 0]))
            self.play(GrowArrow(a1), GrowArrow(a2), GrowArrow(a3), GrowArrow(a4),
                      FadeIn(f3), FadeIn(f5),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.4))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(FadeIn(how), Circumscribe(pack_l, color=CHALK_PINK,
                                                stroke_width=2.5),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.3))

            e2 = MathTex("3x-9", r"\;=\;", "10x-5", font_size=44)
            align_equals(e2, BOARD_CX, EQ_Y)
            self.play(TransformMatchingTex(eq, e2),
                      FadeOut(pack_l), FadeOut(pack_r), FadeOut(a1), FadeOut(a2),
                      FadeOut(a3), FadeOut(a4), FadeOut(f3), FadeOut(f5),
                      FadeOut(how),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["success"], gain=-11)

            e3 = MathTex("3x-10x", r"\;=\;", "-5+9", font_size=40)
            align_equals(e3, BOARD_CX, EQ_Y)
            self.play(TransformMatchingTex(e2, e3),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            e4 = MathTex("-7x", r"\;=\;", "4", font_size=42)
            align_equals(e4, BOARD_CX, EQ_Y)
            self.play(TransformMatchingTex(e3, e4),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            e5 = MathTex("x", r"\;=\;", r"-\frac{4}{7}", font_size=44,
                         color=CHALK_GREEN)
            align_equals(e5, BOARD_CX, EQ_Y)
            self.play(TransformMatchingTex(e4, e5),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 7: the complete strategy -------------------------------------
    def strategy_card(self, n: int, title: str, math_tex: str, color: str) -> VGroup:
        card = RoundedRectangle(corner_radius=0.1, width=2.1, height=1.5,
                                stroke_color=color, stroke_width=2,
                                fill_color="#16202B", fill_opacity=0.9)
        num = board_text(str(n), 18, color, "BOLD").move_to(
            card.get_top() + DOWN * 0.25)
        lbl = board_text(title, 15, CHALK_WHITE, "BOLD").move_to(
            card.get_center() + UP * 0.22)
        tex = MathTex(math_tex, font_size=20).move_to(
            card.get_center() + DOWN * 0.3)
        return VGroup(card, num, lbl, tex)

    def beat7_strategy(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("The Complete Strategy", 26, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, BOARD_TOP - 0.45, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.4))

            c1 = self.strategy_card(1, "SIMPLIFY", r"2(x+3)\to 2x+6", CHALK_PINK)
            c2 = self.strategy_card(2, "GROUP x", r"5x-2x", CHALK_CYAN)
            c3 = self.strategy_card(3, "GROUP NUMBERS", r"-6+12", CHALK_AMBER)
            c4 = self.strategy_card(4, "SOLVE", r"3x=6 \to x=2", CHALK_GREEN)
            cards = VGroup(c1, c2, c3, c4).arrange(RIGHT, buff=0.16).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.35, 0]))

            self.play(FadeIn(c1, shift=DOWN * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(c2, shift=DOWN * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(c3, shift=DOWN * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(c4, shift=DOWN * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            check = board_text("Then CHECK: put your answer back into both sides.",
                               18, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.35, 0]))
            self.play(FadeIn(check), Circumscribe(check, color=CHALK_YELLOW,
                                                  stroke_width=3),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 8: ages application ------------------------------------------
    def beat8_ages(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("Real Problem: Two Ages", 23,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.45, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            # ---- today's ages (left half) ----
            today = board_text("Today", 16, CHALK_AMBER, "BOLD").move_to(
                np.array([-2.75, 2.35, 0]))
            rafi = board_text("Karthik", 19, CHALK_CYAN, "BOLD").move_to(
                np.array([-3.35, 1.75, 0]))
            fathi = board_text("Ananya", 19, CHALK_PINK, "BOLD").move_to(
                np.array([-3.35, 1.15, 0]))
            r_age = MathTex("7x", font_size=28, color=CHALK_CYAN).move_to(
                np.array([-2.35, 1.75, 0]))
            f_age = MathTex("5x", font_size=28, color=CHALK_PINK).move_to(
                np.array([-2.35, 1.15, 0]))
            ratio = board_text("ratio 7 : 5", 15, CHALK_WHITE).move_to(
                np.array([-2.75, 0.6, 0]))
            self.play(FadeIn(today), FadeIn(rafi), FadeIn(fathi), FadeIn(r_age),
                      FadeIn(f_age), FadeIn(ratio),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            # ---- ten years later (right half) ----
            arrow = Arrow(np.array([-1.55, 1.45, 0]), np.array([-0.35, 1.45, 0]),
                          buff=0.05, color=CHALK_YELLOW, stroke_width=2.5)
            t10 = board_text("+10 years", 15, CHALK_YELLOW, "BOLD").move_to(
                np.array([-0.95, 1.95, 0]))
            later = board_text("10 years later", 16, CHALK_GREEN, "BOLD").move_to(
                np.array([1.45, 2.35, 0]))
            rafi2 = board_text("Karthik", 19, CHALK_CYAN, "BOLD").move_to(
                np.array([0.45, 1.75, 0]))
            fathi2 = board_text("Ananya", 19, CHALK_PINK, "BOLD").move_to(
                np.array([0.45, 1.15, 0]))
            future_r = MathTex("7x+10", font_size=26, color=CHALK_CYAN).move_to(
                np.array([1.85, 1.75, 0]))
            future_f = MathTex("5x+10", font_size=26, color=CHALK_PINK).move_to(
                np.array([1.85, 1.15, 0]))
            ratio2 = board_text("ratio 9 : 7", 15, CHALK_WHITE).move_to(
                np.array([1.45, 0.6, 0]))
            self.play(GrowArrow(arrow), FadeIn(t10), FadeIn(later), FadeIn(rafi2),
                      FadeIn(fathi2), FadeIn(future_r), FadeIn(future_f),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.6))
            self.play(FadeIn(ratio2),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            e1 = MathTex("49x+70", r"\;=\;", "45x+90", font_size=32).move_to(
                np.array([BOARD_CX, -0.35, 0]))
            e1[0][2].set_color(CHALK_CYAN)
            e1[2][2].set_color(CHALK_CYAN)
            hint = board_text("multiply across the ratios", 14, CHALK_WHITE).move_to(
                np.array([BOARD_CX, -1.95, 0]))
            self.play(Write(e1), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            e2 = MathTex("49x-45x", r"\;=\;", "90-70", font_size=32).move_to(
                np.array([BOARD_CX, -0.35, 0]))
            self.play(TransformMatchingTex(e1, e2),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            e3 = MathTex("4x", r"\;=\;", "20", font_size=32).move_to(
                np.array([BOARD_CX, -0.35, 0]))
            self.play(TransformMatchingTex(e2, e3),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            e4 = MathTex("x", r"\;=\;", "5", font_size=36, color=CHALK_GREEN).move_to(
                np.array([BOARD_CX, -0.35, 0]))
            self.play(TransformMatchingTex(e3, e4),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.5))
            box = SurroundingRectangle(e4, color=CHALK_GREEN, buff=0.18,
                                       corner_radius=0.1, stroke_width=2.5)
            self.play(Create(box), Flash(e4, color=CHALK_GREEN, flash_radius=0.5),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)

            ages = VGroup(
                board_text("Karthik = 35", 20, CHALK_CYAN, "BOLD"),
                board_text("Ananya = 25", 20, CHALK_PINK, "BOLD"),
            ).arrange(RIGHT, buff=0.7).move_to(np.array([BOARD_CX, -1.35, 0]))
            self.play(FadeIn(ages, shift=UP * 0.15), FadeOut(hint),
                      Flash(ages, color=CHALK_AMBER, flash_radius=0.8),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["ding"], gain=-12)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 9: student challenge -----------------------------------------
    def beat9_challenge(self) -> None:
        with self.voiceover(text=NARRATION["scene9_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", 30, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.5, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            eq_c = MathTex("7x-5", r"\;=\;", "2x", font_size=52)
            align_equals(eq_c, BOARD_CX, 0.8)
            eq_c[0][1].set_color(CHALK_CYAN)
            eq_c[2][1].set_color(CHALK_CYAN)
            self.play(Write(eq_c), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            find = board_text("Isolate x", 22, CHALK_WHITE).move_to(
                np.array([BOARD_CX, -0.15, 0]))
            self.play(FadeIn(find), run_time=rt(tracker.time_until_bookmark("b2") * 0.4))
            where = board_text("Where should the x terms meet?", 18, CHALK_YELLOW,
                               "BOLD").move_to(np.array([BOARD_CX, -0.85, 0]))
            self.play(FadeIn(where), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            pause = board_text("Pause and try it", 20, CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX, -1.55, 0]))
            self.play(FadeIn(pause), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.challenge_q = VGroup(heading, eq_c, find, where, pause)
            self._capture_srt(tracker)

        play_challenge_countdown(self, seconds=10, sfx=self.sfx)

        with self.voiceover(text=NARRATION["scene9_reveal"]) as tracker:
            eq_c = self.challenge_q[1]
            self.play(FadeOut(self.challenge_q[3]), FadeOut(self.challenge_q[4]),
                      run_time=0.3)

            box2x = SurroundingRectangle(eq_c[2], color=CHALK_GREEN, buff=0.1,
                                         corner_radius=0.08, stroke_width=3)
            strip = board_text("2x crosses over and becomes -2x", 14, CHALK_GREEN,
                               "BOLD").move_to(np.array([BOARD_CX, 2.2, 0]))
            self.play(Create(box2x), FadeIn(strip),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.4))

            e2 = MathTex("7x-2x", r"\;=\;", "5", font_size=50)
            align_equals(e2, BOARD_CX, 0.8)
            e2[0][0].set_color(CHALK_CYAN)
            e2[0][1].set_color(CHALK_CYAN)
            self.play(TransformMatchingTex(eq_c, e2), FadeOut(box2x),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["success"], gain=-11)

            e3 = MathTex("5x", r"\;=\;", "5", font_size=50)
            align_equals(e3, BOARD_CX, 0.8)
            e3[0][1].set_color(CHALK_CYAN)
            self.play(TransformMatchingTex(e2, e3),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.45))
            e4 = MathTex("x", r"\;=\;", "1", font_size=54, color=CHALK_GREEN)
            align_equals(e4, BOARD_CX, 0.8)
            self.play(TransformMatchingTex(e3, e4),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["success"], gain=-11)

            ans_box = SurroundingRectangle(e4, color=CHALK_GREEN, buff=0.22,
                                           corner_radius=0.1, stroke_width=3)
            ck = tick_beside(e4, CHALK_GREEN, 0.42, 0.45)
            well = board_text("Well done!", 20, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -0.85, 0]))
            self.play(Create(ans_box), Create(ck), FadeIn(well),
                      Flash(e4, color=CHALK_GREEN, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-12)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 10: summary + outtro -----------------------------------------
    def summary_row(self, n: int, label: str, math_tex: str, color: str) -> VGroup:
        badge = Circle(radius=0.2, stroke_color=color, stroke_width=2,
                       fill_color=color, fill_opacity=0.18)
        num = board_text(str(n), 18, color, "BOLD").move_to(badge.get_center())
        return VGroup(VGroup(badge, num), board_text(label, 19, CHALK_WHITE),
                      MathTex(math_tex, font_size=22)).arrange(RIGHT, buff=0.3)

    def beat10_summary(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("Summary", 32, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.5, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.5))

            chain = MathTex(
                r"5x-12=2x-6 \;\rightarrow\; 3x=6 \;\rightarrow\; x=2",
                font_size=26, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, 2.32, 0]))
            self.play(Write(chain), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            r1 = self.summary_row(1, "Variables together:",
                                  r"5x-2x = 3x", CHALK_CYAN)
            r2 = self.summary_row(2, "Numbers together:",
                                  r"-6+12 = 6", CHALK_GREEN)
            r3 = self.summary_row(3, "Brackets first:",
                                  r"3(x-3) \to 3x-9", CHALK_PINK)
            r4 = self.summary_row(4, "Check both sides:",
                                  r"-2 = -2", CHALK_YELLOW)
            rows = VGroup(r1, r2, r3, r4).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            rows.move_to(np.array([BOARD_CX, 0.45, 0]))
            rows.shift(RIGHT * (BOARD_CX - rows.get_center()[0]))

            self.play(FadeIn(r1, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(r2, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(r3, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(r4, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # the takeaway is the closing line OF the summary ...
            takeaway = board_text("Variables together. Numbers together.",
                                  22, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.45, 0]))
            second = board_text("Brackets? Simplify them first.", 17,
                                CHALK_CYAN).move_to(
                np.array([BOARD_CX, -1.95, 0]))
            self.play(FadeIn(takeaway), Flash(takeaway, color=CHALK_YELLOW,
                                              flash_radius=0.9),
                      FadeIn(second),
                      run_time=rt(tracker.time_until_bookmark("b5") * 0.3))
            self.add_sound(self.sfx["success"], gain=-11)

            summary = VGroup(heading, chain, rows, takeaway, second)
            self.play(FadeOut(summary),
                      run_time=rt(tracker.time_until_bookmark("b5") * 0.3))

            # ... so after the summary only the Thank-You template is left.
            thanks = board_text("Thank You for Watching!", 40, CHALK_WHITE, "BOLD")
            thanks2 = board_text("See you in the next lesson :)", 25, CHALK_CYAN)
            thanks_group = VGroup(thanks, thanks2).arrange(DOWN, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY, 0]))
            self.play(Write(thanks), run_time=rt(tracker.time_until_bookmark("b5") * 0.4))
            self.add_sound(self.sfx["ding"], gain=-11)
            self.play(FadeIn(thanks2, shift=UP * 0.1),
                      run_time=rt(tracker.get_remaining_duration()))
            self.play(Circumscribe(thanks_group, color=CHALK_AMBER, stroke_width=3,
                                   time_width=0.5), run_time=0.3)
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(END_HOLD)


if __name__ == "__main__":
    pass

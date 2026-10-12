"""
The Wall Builders & The Race Against Time — Time and Work (Inverse Proportion)
Story-mode chalkboard lesson (Telangana Class 8 Maths, Ch. 10, Direct & Inverse
Proportions).

Follows the same production pipeline as interest_growth_story.py:
  - assets/background2.png (empty chalkboard) as a fixed backdrop; every
    drawing stays inside the measured board-safe rectangle.
  - assets/students.png / teacher.png (deglazed, clean-edged cutouts) in the
    bottom corners, "CLASS 09" / "Mathematics" badges stacked top-right.
  - VoiceoverScene + EdgeSpeechService (en-IN-PrabhatNeural).
  - Every animation's run_time is computed from real edge-tts per-word
    timestamps via `<bookmark mark='...'/>` tags + tracker.time_until_bookmark.
  - A ground-truth .srt is exported from the same real word-boundary data.
  - Sound effects from sound_effects.py, chalk-styled Text/MathTex.

Storyboard (4 scenes, ~90s target):
  1. The Lonely Wall — Raju alone takes 6 hours; rate = 1/6 wall/hour.
  2. Teamwork & Triple Speed — 3 workers, combined rate 1/2 wall/hour, 2 hours.
  3. The Inverse Proportion Seesaw — workers up x3, time down /3; x*y=k.
  4. The Takeaway & Summary Table — 1->6h, 2->3h, 3->2h, 6->1h; x1y1=x2y2.
Plus a short Summary + Thank You closing beat (studio's usual outro).
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
    Polygon, Rectangle, RoundedRectangle, Triangle, Arrow, Sector, Arc,
    Text, Write, FadeIn, FadeOut, Create, Uncreate, Transform,
    ReplacementTransform, FadeTransform, GrowFromCenter, GrowFromPoint,
    GrowArrow, Indicate, Flash, Circumscribe, Wiggle, DrawBorderThenFill,
    LaggedStart, LaggedStartMap, Succession, SpinInFromNothing,
    ShrinkToCenter, ApplyWave, rate_functions, config, MoveAlongPath,
)
from manim_voiceover import VoiceoverScene
from manim_voiceover.tracker import AUDIO_OFFSET_RESOLUTION

from speech_service import get_speech_service
from sound_effects import load_all as load_sfx

# --------------------------------------------------------------- theme -----
CHALK_WHITE = "#F5F2E9"
CHALK_YELLOW = "#FFE066"
CHALK_PINK = "#FF8FA3"
CHALK_CYAN = "#7FE7DC"
CHALK_AMBER = "#E8B769"
CHALK_GREEN = "#9BE38A"
CHALK_ORANGE = "#F2A65A"
CHALK_BLUE = "#7FB3E8"
FONT = "Segoe Print"
MATH_COLOR = CHALK_WHITE

END_HOLD = 2.2
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


def drop_shadow(mobj: VGroup, dx: float = 0.05, dy: float = -0.06,
                 opacity: float = 0.3) -> VGroup:
    shadow = mobj.copy()
    shadow.set_fill(BLACK, opacity=opacity)
    shadow.set_stroke(width=0)
    shadow.shift(np.array([dx, dy, 0]))
    return VGroup(shadow, mobj)


def worker_icon(color: str = CHALK_AMBER, skin: str = "#F0C9A0") -> VGroup:
    """A small mason figure: hardhat + head + shirt + trowel."""
    body = RoundedRectangle(corner_radius=0.05, width=0.36, height=0.5,
                             stroke_color=color, stroke_width=2)
    body.set_fill(color=[CHALK_WHITE, color, "#5A3A1E"], opacity=0.85)
    body.move_to(np.array([0, -0.15, 0]))

    legs = VGroup(*[
        Rectangle(width=0.1, height=0.22, stroke_color="#2A3B55", stroke_width=1.5,
                  fill_color="#2A3B55", fill_opacity=0.9).move_to(np.array([dx, -0.5, 0]))
        for dx in (-0.09, 0.09)
    ])

    head = Circle(radius=0.16, stroke_color="#7A5230", stroke_width=1.5,
                   fill_color=skin, fill_opacity=0.95).move_to(np.array([0, 0.28, 0]))

    hardhat = Sector(radius=0.19, angle=PI, start_angle=0,
                      stroke_color=color, stroke_width=2, fill_color=color,
                      fill_opacity=0.95)
    hardhat.stretch(0.55, dim=1)
    hardhat.move_to(np.array([0, 0.34, 0]), aligned_edge=DOWN)
    hat_brim = Line(np.array([-0.2, 0.34, 0]), np.array([0.2, 0.34, 0]),
                     stroke_color=color, stroke_width=2)

    trowel = Polygon(
        np.array([0.2, -0.02, 0]), np.array([0.4, 0.1, 0]), np.array([0.3, 0.2, 0]),
        stroke_width=1, stroke_color="#7A5230",
        fill_color="#C9C9C9", fill_opacity=0.9,
    )
    handle = Line(np.array([0.2, -0.02, 0]), np.array([0.1, -0.14, 0]),
                  stroke_color="#7A5230", stroke_width=2)

    figure = VGroup(legs, body, head, hardhat, hat_brim, handle, trowel)
    return drop_shadow(figure, dx=0.03, dy=-0.04, opacity=0.2)


def brick_wall(cols: int = 6, rows: int = 3, brick_w: float = 0.5,
               brick_h: float = 0.3, color: str = CHALK_AMBER) -> VGroup:
    """A running-bond brick grid, each brick a separate mobject so it can be
    revealed one-by-one to show construction progress."""
    bricks = VGroup()
    total_w = cols * brick_w
    for r in range(rows):
        offset = brick_w / 2 if r % 2 == 1 else 0
        n = cols if offset == 0 else cols - 1
        for c in range(n):
            x = -total_w / 2 + offset + c * brick_w + brick_w / 2
            y = r * brick_h
            brick = Rectangle(width=brick_w - 0.05, height=brick_h - 0.05,
                               stroke_color=color, stroke_width=1.2)
            brick.set_fill(color=[CHALK_WHITE, color, "#7A4A22"], opacity=0.8)
            brick.move_to(np.array([x, y, 0]))
            bricks.add(brick)
    bricks.move_to(ORIGIN)
    return bricks


def digital_timer(label: str) -> VGroup:
    box = RoundedRectangle(corner_radius=0.08, width=1.5, height=0.55,
                            stroke_color=CHALK_GREEN, stroke_width=2,
                            fill_color="#0A1A12", fill_opacity=0.7)
    txt = board_text(label, 26, CHALK_GREEN, "BOLD").move_to(box.get_center())
    return VGroup(box, txt)


def _corner_badge(text: str, *, corner: str, y: float, font_size: int = 11,
                   filled: bool = True) -> VGroup:
    label = board_text(text, font_size, CHALK_WHITE, "BOLD")
    if filled:
        frame = RoundedRectangle(
            corner_radius=0.04, width=label.width + 0.24, height=label.height + 0.16,
            stroke_color=CHALK_AMBER, stroke_width=1.5,
            fill_color="#2A1D10", fill_opacity=0.45,
        )
        label.move_to(frame.get_center())
        badge = VGroup(frame, label)
    else:
        badge = VGroup(label)

    if corner == "left":
        badge.move_to(np.array([BOARD_LEFT + 0.55, y, 0]))
    else:
        badge.move_to(np.array([BOARD_RIGHT - 0.6, y, 0]))
        badge.shift(RIGHT * (BOARD_RIGHT - 0.08 - badge.get_right()[0]))
    return badge


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "Today's topic: time and work, and inverse "
        "proportion.<bookmark mark='b1'/> Get ready for the wall builders' "
        "race against time!<bookmark mark='b2'/>"
    ),
    "scene1": (
        "Meet Raju, a hardworking mason.<bookmark mark='b1'/> Working all "
        "alone, Raju takes six hours to build one complete brick "
        "wall.<bookmark mark='b2'/> That means every hour, he finishes "
        "exactly one sixth of the work.<bookmark mark='b3'/> Phew! Six "
        "hours for one worker — Raju definitely needs some "
        "backup!<bookmark mark='b4'/>"
    ),
    "scene2": (
        "Now watch what happens when two identical clones join "
        "Raju.<bookmark mark='b1'/> Three workers are laying bricks at the "
        "exact same rate.<bookmark mark='b2'/> One sixth, plus one sixth, "
        "plus one sixth, equals three sixths, or one half a wall per "
        "hour.<bookmark mark='b3'/> Together, they complete half the wall "
        "in just one hour.<bookmark mark='b4'/> And in just two hours — "
        "bam — the wall is fully built!<bookmark mark='b5'/>"
    ),
    "scene3": (
        "Notice the pattern?<bookmark mark='b1'/> As the number of workers "
        "triples, from one to three,<bookmark mark='b2'/> the time taken "
        "drops to one third, from six hours to two.<bookmark mark='b3'/> "
        "This is called inverse proportion. When one quantity increases, "
        "the other decreases at exactly the same rate.<bookmark "
        "mark='b4'/> The product always stays constant: one times six, "
        "equals three times two, equals six.<bookmark mark='b5'/>"
    ),
    "scene4": (
        "Let's see the full pattern, for every number of "
        "workers.<bookmark mark='b1'/> One worker takes six hours. Two "
        "workers take three hours. Three workers take two hours. And six "
        "workers take just one hour.<bookmark mark='b2'/> Every single "
        "time, the product of workers and hours stays exactly "
        "six.<bookmark mark='b3'/> For any inverse proportion problem, the "
        "rule is the same: x one, y one, equals x two, y "
        "two.<bookmark mark='b4'/>"
    ),
    "summary": (
        "Let's recap the big idea.<bookmark mark='b1'/> Number of workers "
        "and time taken vary inversely — more hands mean less "
        "time.<bookmark mark='b2'/> Doubling the workers halves the time. "
        "Tripling the workers cuts the time to one third.<bookmark "
        "mark='b3'/> And the product of workers and time always stays the "
        "same constant.<bookmark mark='b4'/> Thank you so much for "
        "watching, and I will see you in the next lesson!"
    ),
}


class TimeAndWorkStory(VoiceoverScene):
    """Story-mode chalkboard lesson: Time and Work (Inverse Proportion)."""

    def construct(self) -> None:
        self.set_speech_service(get_speech_service(), create_subcaption=False)
        self.sfx = load_sfx()
        self._srt_entries: list[tuple[float, float, str]] = []

        self.add_background()
        self.beat_title()
        self.beat_scene1_lonely_wall()
        self.beat_scene2_teamwork()
        self.beat_scene3_seesaw()
        self.beat_scene4_table()
        self.beat_summary()

        self._write_real_srt()

    # -- backdrop --------------------------------------------------------
    def add_background(self) -> None:
        bg = ImageMobject(str(_HERE / "assets" / "background2.png"))
        bg.stretch_to_fit_width(config.frame_width)
        bg.stretch_to_fit_height(config.frame_height)
        bg.set_z_index(-10)
        self.add(bg)

        student = ImageMobject(str(_HERE / "assets" / "students.png"))
        student.set_z_index(-5)
        student.height = 3.3
        student.move_to(np.array([
            -config.frame_width / 2 + student.width / 2 - 0.15,
            -config.frame_height / 2 + student.height / 2 - 0.1,
            0,
        ]))
        self.add(student)

        teacher = ImageMobject(str(_HERE / "assets" / "teacher.png"))
        teacher.set_z_index(-5)
        teacher.height = 3.3
        teacher.move_to(np.array([
            config.frame_width / 2 - teacher.width / 2 + 0.45,
            -config.frame_height / 2 + teacher.height / 2 - 0.1,
            0,
        ]))
        self.add(teacher)

        self.add(_corner_badge("CLASS 8", corner="right", y=BOARD_TOP - 0.16, font_size=11))
        self.add(_corner_badge("Mathematics", corner="right", y=BOARD_TOP - 0.62,
                                font_size=12, filled=True))

    # -- real (word-boundary-accurate) SRT export -------------------------
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
        out_dir = _HERE / "media" / "videos" / "time_and_work_story"
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

    # -- Beat 0: Title -----------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            title = board_text("Time and Work", 40, CHALK_WHITE, "BOLD")
            title2 = board_text("Inverse Proportion", 30, CHALK_YELLOW, "BOLD")
            sub = board_text("The Wall Builders' Race Against Time", 22, CHALK_CYAN)
            group = VGroup(title, title2, sub).arrange(DOWN, buff=0.28).move_to(
                np.array([BOARD_CX, BOARD_CY, 0]))

            self.play(Write(title), Write(title2),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(FadeIn(sub, shift=UP * 0.15), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-12)

            self.title_group = group
            self._capture_srt(tracker)

        self.play(FadeOut(self.title_group))

    # -- Beat 1: Scene 1 — The Lonely Wall ----------------------------------
    def beat_scene1_lonely_wall(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            heading = board_text("Raju builds alone", 26, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.4, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b1") * 0.6))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            wall_x = BOARD_CX - 0.7
            wall_y = BOARD_CY - 0.3
            outline = Rectangle(width=3.1, height=1.05, stroke_color=CHALK_WHITE,
                                 stroke_width=2, stroke_opacity=0.6).move_to(
                np.array([wall_x, wall_y, 0]))
            target_lbl = board_text("Target: 1 Whole Wall", 18, CHALK_WHITE).next_to(
                outline, UP, buff=0.18)
            worker = worker_icon(CHALK_CYAN).scale(1.3).next_to(outline, RIGHT, buff=0.5)
            name = board_text("Raju", 20, CHALK_CYAN, "BOLD").next_to(worker, DOWN, buff=0.15)
            timer = digital_timer("0:00").move_to(np.array([BOARD_CX, BOARD_TOP - 0.85, 0]))

            self.play(Create(outline), FadeIn(target_lbl), FadeIn(timer),
                      FadeIn(worker, shift=UP * 0.2), FadeIn(name),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)

            rate_box = board_text("Rate = 1/6 wall per hour", 18, CHALK_YELLOW, "BOLD").next_to(
                worker, UP, buff=0.35)
            self.play(FadeIn(rate_box, shift=UP * 0.1),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.4))
            self.add_sound(self.sfx["click"], gain=-14)

            wall = brick_wall(cols=6, rows=3).move_to(np.array([wall_x, wall_y, 0]))
            hours = ["1:00", "2:00", "3:00", "4:00", "5:00", "6:00"]
            n = len(wall)
            step = max(1, n // len(hours))
            reveal_time = rt(tracker.time_until_bookmark("b2"))
            self.play(LaggedStart(*[FadeIn(b, scale=0.6) for b in wall[:step]], lag_ratio=0.2),
                      run_time=reveal_time / len(hours))
            for i, hlabel in enumerate(hours[1:], start=1):
                new_timer = digital_timer(hlabel).move_to(timer.get_center())
                lo, hi = i * step, min((i + 1) * step, n)
                anims = [ReplacementTransform(timer, new_timer)]
                if lo < n:
                    anims.append(LaggedStart(*[FadeIn(b, scale=0.6) for b in wall[lo:hi]],
                                              lag_ratio=0.2))
                self.play(*anims, run_time=reveal_time / len(hours))
                timer = new_timer
            self.add_sound(self.sfx["success"], gain=-12)

            bubble = board_text('"Phew! I need some backup!"', 20, CHALK_CYAN).next_to(
                outline, DOWN, buff=0.6)
            self.play(FadeIn(bubble, shift=UP * 0.1),
                      run_time=rt(tracker.get_remaining_duration() * 0.8))
            self.add_sound(self.sfx["ding"], gain=-12)

            self.scene1_group = VGroup(heading, outline, target_lbl, worker, name,
                                        rate_box, wall, timer, bubble)
            self._capture_srt(tracker)

        self.play(FadeOut(self.scene1_group))

    # -- Beat 2: Scene 2 — Teamwork & Triple Speed --------------------------
    def beat_scene2_teamwork(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            heading = board_text("Three workers join forces", 26, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.4, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b1") * 0.4))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            wall_x = BOARD_CX - 0.7
            wall_y = BOARD_CY - 0.3
            outline = Rectangle(width=3.1, height=1.05, stroke_color=CHALK_WHITE,
                                 stroke_width=2, stroke_opacity=0.6).move_to(
                np.array([wall_x, wall_y, 0]))
            timer = digital_timer("0:00").move_to(np.array([BOARD_CX, BOARD_TOP - 0.85, 0]))

            # Side by side (not stacked) — each figure is taller than 0.5
            # units once scaled, so stacking them vertically with a small
            # offset made them overlap into a single blob.
            raju = worker_icon(CHALK_CYAN).scale(1.1).next_to(outline, RIGHT, buff=0.3)
            clone1 = worker_icon(CHALK_PINK).scale(1.1).next_to(raju, RIGHT, buff=0.12)
            clone2 = worker_icon(CHALK_GREEN).scale(1.1).next_to(clone1, RIGHT, buff=0.12)

            self.play(Create(outline), FadeIn(timer), FadeIn(raju, shift=UP * 0.2),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.play(LaggedStart(
                FadeIn(clone1, shift=RIGHT * 0.6), FadeIn(clone2, shift=RIGHT * 0.6),
                lag_ratio=0.35), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["swipe"], gain=-13)

            eq = chalk_math(r"\frac16+\frac16+\frac16=\frac36=\frac12",
                             26, CHALK_YELLOW).next_to(
                VGroup(raju, clone1, clone2), UP, buff=0.3)
            self.play(Write(eq), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-14)

            wall = brick_wall(cols=6, rows=3).move_to(np.array([wall_x, wall_y, 0]))
            half = len(wall) // 2
            self.play(LaggedStart(*[FadeIn(b, scale=0.6) for b in wall[:half]], lag_ratio=0.08),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.6))
            new_timer = digital_timer("1:00").move_to(timer.get_center())
            self.play(ReplacementTransform(timer, new_timer),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.4))
            timer = new_timer
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(LaggedStart(*[FadeIn(b, scale=0.6) for b in wall[half:]], lag_ratio=0.08),
                      run_time=rt(tracker.time_until_bookmark("b5") * 0.6))
            new_timer2 = digital_timer("2:00").move_to(timer.get_center())
            self.play(ReplacementTransform(timer, new_timer2),
                      Flash(outline.get_center(), color=CHALK_YELLOW, flash_radius=1.2),
                      run_time=rt(tracker.time_until_bookmark("b5") * 0.4))
            timer = new_timer2
            self.add_sound(self.sfx["success"], gain=-11)

            self.scene2_group = VGroup(heading, outline, timer, raju, clone1, clone2,
                                        eq, wall)
            self._capture_srt(tracker)

        self.play(FadeOut(self.scene2_group))

    # -- Beat 3: Scene 3 — The Inverse Proportion Seesaw ---------------------
    def beat_scene3_seesaw(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            heading = board_text("The Inverse Proportion Seesaw", 28, CHALK_AMBER,
                                  "BOLD").move_to(np.array([BOARD_CX, BOARD_TOP - 0.4, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            pivot_y = BOARD_CY + 0.2
            fulcrum = Triangle(stroke_color=CHALK_WHITE, stroke_width=2,
                                fill_color="#5A3A1E", fill_opacity=0.8)
            fulcrum.scale(0.35).move_to(np.array([BOARD_CX, pivot_y - 0.35, 0]))
            bar = Line(np.array([BOARD_CX - 2.4, pivot_y, 0]),
                       np.array([BOARD_CX + 2.4, pivot_y, 0]),
                       stroke_color=CHALK_WHITE, stroke_width=4)
            self.play(FadeIn(fulcrum), Create(bar), run_time=rt(0.5))

            left_pt = bar.get_left()
            right_pt = bar.get_right()
            workers_dot = Circle(radius=0.28, stroke_color=CHALK_BLUE, stroke_width=2,
                                  fill_color=CHALK_BLUE, fill_opacity=0.6).move_to(
                left_pt + DOWN * 0.3)
            workers_lbl = board_text("Workers (x)", 18, CHALK_BLUE, "BOLD").next_to(
                workers_dot, DOWN, buff=0.15)
            workers_val = board_text("1", 24, CHALK_WHITE, "BOLD").move_to(workers_dot.get_center())

            time_dot = Circle(radius=0.28, stroke_color=CHALK_ORANGE, stroke_width=2,
                               fill_color=CHALK_ORANGE, fill_opacity=0.6).move_to(
                right_pt + DOWN * 0.3)
            time_lbl = board_text("Time (y)", 18, CHALK_ORANGE, "BOLD").next_to(
                time_dot, DOWN, buff=0.15)
            time_val = board_text("6", 24, CHALK_WHITE, "BOLD").move_to(time_dot.get_center())

            self.play(FadeIn(workers_dot), FadeIn(workers_val), FadeIn(workers_lbl),
                      FadeIn(time_dot), FadeIn(time_val), FadeIn(time_lbl),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            self.add_sound(self.sfx["pop"], gain=-13)

            # Workers side rises (x1), time side drops (/3), bar tilts to match.
            new_workers_val = board_text("3", 24, CHALK_WHITE, "BOLD")
            new_time_val = board_text("2", 24, CHALK_WHITE, "BOLD")
            tilt = 0.35
            self.play(
                bar.animate.rotate(tilt, about_point=np.array([BOARD_CX, pivot_y, 0])),
                workers_dot.animate.shift(UP * 0.45),
                workers_val.animate.shift(UP * 0.45),
                workers_lbl.animate.shift(UP * 0.45),
                time_dot.animate.shift(DOWN * 0.45),
                time_val.animate.shift(DOWN * 0.45),
                time_lbl.animate.shift(DOWN * 0.45),
                run_time=rt(tracker.time_until_bookmark("b3")),
            )
            new_workers_val.move_to(workers_val.get_center())
            new_time_val.move_to(time_val.get_center())
            self.play(ReplacementTransform(workers_val, new_workers_val),
                      ReplacementTransform(time_val, new_time_val), run_time=0.3)
            workers_val, time_val = new_workers_val, new_time_val
            self.add_sound(self.sfx["ding"], gain=-12)

            inverse_lbl = board_text("Inverse Proportion", 24, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 1.6, 0]))
            self.play(FadeIn(inverse_lbl, shift=UP * 0.1),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-12)

            k_box_bg = RoundedRectangle(corner_radius=0.1, width=4.2, height=0.7,
                                         stroke_color=CHALK_GREEN, stroke_width=2,
                                         fill_color="#0A1A12", fill_opacity=0.6).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.7, 0]))
            k_eq = chalk_math(r"x \cdot y = k \;\Rightarrow\; 1\times6=3\times2=6",
                               24, CHALK_GREEN).move_to(k_box_bg.get_center())
            self.play(FadeIn(k_box_bg), Write(k_eq),
                      run_time=rt(tracker.get_remaining_duration() * 0.85))
            self.add_sound(self.sfx["success"], gain=-11)

            self.scene3_group = VGroup(heading, fulcrum, bar, workers_dot, workers_val,
                                        workers_lbl, time_dot, time_val, time_lbl,
                                        inverse_lbl, k_box_bg, k_eq)
            self._capture_srt(tracker)

        self.play(FadeOut(self.scene3_group))

    # -- Beat 4: Scene 4 — The Takeaway & Summary Table ----------------------
    def beat_scene4_table(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            heading = board_text("Summary Table", 30, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.4, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b1") * 0.3))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            rows_data = [("1", "6", "1 x 6 = 6"), ("2", "3", "2 x 3 = 6"),
                         ("3", "2", "3 x 2 = 6"), ("6", "1", "6 x 1 = 6")]
            header = VGroup(
                board_text("Workers", 20, CHALK_CYAN, "BOLD"),
                board_text("Hours", 20, CHALK_ORANGE, "BOLD"),
                board_text("Product", 20, CHALK_GREEN, "BOLD"),
            )
            col_x = [BOARD_CX - 2.3, BOARD_CX - 0.3, BOARD_CX + 1.9]
            for cell, x in zip(header, col_x):
                cell.move_to(np.array([x, BOARD_CY + 1.3, 0]))

            self.play(LaggedStart(*[FadeIn(c) for c in header], lag_ratio=0.2),
                      run_time=rt(tracker.time_until_bookmark("b1")))

            table_rows = VGroup()
            for i, (w, h, p) in enumerate(rows_data):
                y = BOARD_CY + 0.8 - i * 0.55
                row = VGroup(
                    board_text(w, 22, CHALK_CYAN, "BOLD").move_to(np.array([col_x[0], y, 0])),
                    board_text(h, 22, CHALK_ORANGE, "BOLD").move_to(np.array([col_x[1], y, 0])),
                    board_text(p, 20, CHALK_GREEN).move_to(np.array([col_x[2], y, 0])),
                )
                table_rows.add(row)

            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in table_rows],
                                   lag_ratio=0.3), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-14)

            divider = Line(np.array([BOARD_CX - 3.0, BOARD_CY + 1.0, 0]),
                            np.array([BOARD_CX + 3.0, BOARD_CY + 1.0, 0]),
                            stroke_color=CHALK_WHITE, stroke_width=1.5, stroke_opacity=0.4)
            self.play(Create(divider), run_time=rt(tracker.time_until_bookmark("b3") * 0.4))
            self.add_sound(self.sfx["success"], gain=-12)

            raju = worker_icon(CHALK_CYAN).scale(1.0).move_to(
                np.array([BOARD_CX, BOARD_BOTTOM + 0.75, 0]))
            formula = chalk_math(r"x_1 y_1 = x_2 y_2", 30, CHALK_YELLOW).next_to(
                raju, RIGHT, buff=0.5)
            self.play(FadeIn(raju, shift=UP * 0.15), Write(formula),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.play(Flash(formula.get_center(), color=CHALK_YELLOW, flash_radius=1.0),
                      run_time=rt(tracker.get_remaining_duration() * 0.7))
            self.add_sound(self.sfx["success"], gain=-11)

            self.scene4_group = VGroup(heading, header, table_rows, divider, raju, formula)
            self._capture_srt(tracker)

        self.play(FadeOut(self.scene4_group))

    # -- Beat 5: Summary + Thank You ---------------------------------------
    def bullet_row(self, n: int, lines: list[str], *, color: str = CHALK_CYAN) -> VGroup:
        badge = Circle(radius=0.19, stroke_color=color, stroke_width=2,
                        fill_color=color, fill_opacity=0.18)
        num = board_text(str(n), 18, color, "BOLD").move_to(badge.get_center())
        text_block = VGroup(*[board_text(t, 24, CHALK_WHITE) for t in lines]).arrange(
            DOWN, buff=0.06, aligned_edge=LEFT)
        row = VGroup(VGroup(badge, num), text_block).arrange(RIGHT, buff=0.3)
        VGroup(badge, num).move_to(np.array([row[0].get_x(), text_block.get_y(), 0]))
        return row

    def beat_summary(self) -> None:
        with self.voiceover(text=NARRATION["summary"]) as tracker:
            heading = board_text("Summary", 36, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.5, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            bullets = VGroup(
                self.bullet_row(1, ["Workers and time vary inversely —",
                                     "more hands mean less time."], color=CHALK_CYAN),
                self.bullet_row(2, ["Double the workers, halve the time.",
                                     "Triple the workers, cut time to a third."],
                                 color=CHALK_PINK),
                self.bullet_row(3, ["The product of workers and time",
                                     "always stays the same constant."], color=CHALK_YELLOW),
            )
            bullets.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
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

            self.thanks_group = thanks_group
            self._capture_srt(tracker)

        self.wait(END_HOLD)

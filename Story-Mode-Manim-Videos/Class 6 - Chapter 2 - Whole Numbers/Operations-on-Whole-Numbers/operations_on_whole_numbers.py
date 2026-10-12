"""
Operations on Whole Numbers — Moving, Jumping and Landing
Story-mode chalkboard lesson (Telangana Class 6 Maths, Chapter 2: Whole
Numbers, Section 2.3 — whole numbers on the number line).

Core idea: the number line is a stage.  Adding means moving right, subtracting
means moving left, and multiplying means making equal-sized jumps.  The unit
spacing of the line NEVER changes; only the marker, the jump arcs and the
highlighted landing position move.

Production pipeline (mirrors the rest of the Story-Mode series):
  - shared assets/background2.png chalkboard + student/teacher cutouts +
    dhimantAI (top-left) and Mathematics (top-right) corner badges.
  - VoiceoverScene + speech service; narration written as natural prose.
  - synced_voice.install_synced_voiceover() re-times every word against the
    real audio.
  - real per-line SRT export (carry-safe timestamps).
  - sound effects from sound_effects.py, chalk-styled Text/MathTex.
  - story_common.play_challenge_countdown() for the "YOUR TURN" clock.

Title + 10 scenes:
  0. Title card.
  1. Math Can Be Movement -- floor tiles, marker on 2, three steps to 5.
  2. Recall the Whole-Number Line -- 0 .. 10 with equal steps.
  3. Addition Means Moving Right -- 2 + 3 = 5.
  4. Subtraction Means Moving Left -- 6 - 2 = 4.
  5. Multiplication Means Equal Jumps -- 4 x 2 = 8.
  6. Three Operations, Three Patterns -- the three replays stacked.
  7. The Number-Line Game -- Gayatri's 3 + 8 + 5 = 16 journey.
  8. A Simple Routine -- START / OPERATE / MOVE / RESULT.
  9. Student Challenge -- 5 x 3 = 15 with the THINK clock.
 10. Summary + the Thank-You template.
"""

from __future__ import annotations

import sys
from math import atan
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
_ROOT = next(p for p in _HERE.parents
             if (p / "speech_service.py").exists())
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from manim import (
    ORIGIN, UP, DOWN, LEFT, RIGHT, PI, TAU, DEGREES, BLACK,
    ImageMobject, MathTex, VGroup, Line, DashedLine, Circle, Dot, Triangle,
    Rectangle, RoundedRectangle, Polygon, Arrow, DoubleArrow, Text,
    Write, FadeIn, FadeOut, Create, ReplacementTransform, TransformMatchingTex,
    TransformFromCopy, GrowArrow, Indicate, Flash, Circumscribe, CurvedArrow,
    SurroundingRectangle, MoveAlongPath, ArcBetweenPoints, config,
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

LINE_COLOR = CHALK_CYAN       # the number line itself
MARK_COLOR = CHALK_AMBER      # the traveller (start / current position)
RIGHT_COLOR = CHALK_GREEN     # addition: move right
LEFT_COLOR = CHALK_PINK       # subtraction: move left
MULT_COLOR = CHALK_YELLOW     # multiplication: equal jumps
RESULT_COLOR = CHALK_GREEN    # the landing position

END_HOLD = 2.0
TRANSITION_HOLD = 0.35
MIN_RT = 0.12

# measured chalkboard safe bounds (shared across the series)
BOARD_LEFT = -4.6
BOARD_RIGHT = 5.6
BOARD_TOP = 3.3
BOARD_BOTTOM = -2.9
BOARD_CX = (BOARD_LEFT + BOARD_RIGHT) / 2   # 0.5
BOARD_CY = (BOARD_TOP + BOARD_BOTTOM) / 2   # 0.2

HEAD_Y = BOARD_TOP - 0.45


def rt(seconds: float, floor: float = MIN_RT) -> float:
    return max(floor, float(seconds))


def board_text(s: str, size: int = 34, color: str = CHALK_WHITE,
               weight: str = "NORMAL") -> Text:
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def chalk_math(s: str, size: int = 34, color: str = MATH_COLOR) -> MathTex:
    return MathTex(s, font_size=size, color=color)


def centre_on(mob, cx: float = BOARD_CX, cy: float = 0.0):
    mob.move_to(np.array([cx, cy, 0.0]))
    return mob


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


def drop_shadow(mobj: VGroup, dx: float = 0.045, dy: float = -0.05,
                opacity: float = 0.3) -> VGroup:
    shadow = mobj.copy()
    shadow.set_fill(BLACK, opacity=opacity)
    shadow.set_stroke(width=0)
    shadow.shift(np.array([dx, dy, 0]))
    return VGroup(shadow, mobj)


# --------------------------------------------------- the number-line kit ---
def bow_for(span: float, height: float = 0.45) -> float:
    """Arc angle that lifts a jump arc about `height` units off the line.  The
    lift is computed from the span, so short and long jumps look consistent."""
    span = max(abs(span), 0.35)
    return min(PI / 1.6, 4 * atan(2 * height / span))


def num_line(values, *, x0: float = -3.9, step: float = 0.78, y: float = -0.6,
             color: str = LINE_COLOR, dot_color: str = LINE_COLOR,
             size: int = 24, pad: float = 0.5, arrow: bool = True,
             label_every: int = 1, centre: bool = True) -> VGroup:
    """A number line whose unit spacing never changes.

    The line is centred on the board by default: the whole group is shifted so
    that the midpoint of the numbered dots sits on `BOARD_CX`, and `grp.x` is
    shifted with it so that markers and jump arcs placed from `grp.x` stay on
    the dots."""
    xs = [x0 + i * step for i in range(len(values))]
    end = np.array([xs[-1] + pad, y, 0.0])
    start = np.array([x0 - pad, y, 0.0])
    if arrow:
        axis = Arrow(start, end, buff=0, color=color, stroke_width=2.6,
                     tip_length=0.17)
    else:
        axis = Line(start, end, color=color, stroke_width=2.6)
    grp = VGroup(axis)
    dots, labels = {}, {}
    for i, (v, x) in enumerate(zip(values, xs)):
        d = Dot(np.array([x, y, 0.0]), radius=0.052, color=dot_color)
        grp.add(d)
        dots[v] = d
        if i % label_every == 0:
            lab = MathTex(str(v), font_size=size, color=CHALK_WHITE).next_to(
                d, DOWN, buff=0.13)
            grp.add(lab)
            labels[v] = lab
    dx = 0.0
    if centre:
        dx = BOARD_CX - (xs[0] + xs[-1]) / 2.0
        grp.shift(RIGHT * dx)
    grp.dots, grp.labels = dots, labels
    grp.x = {v: x + dx for v, x in zip(values, xs)}
    grp.y = y
    return grp


def hop_arc(x_from: float, x_to: float, y: float, color: str,
            label: str | None = None, label_size: int = 20,
            label_height: float = 0.6, height: float = 0.45) -> VGroup:
    """One jump above the line, drawn as an arc with an arrow head."""
    arc = CurvedArrow(np.array([x_from, y, 0.0]), np.array([x_to, y, 0.0]),
                      angle=-bow_for(x_to - x_from, height), color=color,
                      stroke_width=2.6, tip_length=0.15)
    grp = VGroup(arc)
    if label is not None:
        lab = MathTex(label, font_size=label_size, color=color).move_to(
            np.array([(x_from + x_to) / 2, y + label_height, 0.0]))
        grp.add(lab)
        grp.label = lab
    grp.arc = arc
    return grp


def tile_row(values, *, size: float = 0.92, buff: float = 0.12, y: float = -0.25,
             color: str = CHALK_WHITE, font: int = 26) -> VGroup:
    """Classroom floor tiles, one number each (Scene 1)."""
    tiles = VGroup()
    for v in values:
        sq = RoundedRectangle(corner_radius=0.05, width=size, height=size,
                              stroke_color=color, stroke_width=1.8,
                              fill_color="#16202B", fill_opacity=0.72)
        lab = MathTex(str(v), font_size=font, color=color).move_to(sq.get_center())
        tile = VGroup(sq, lab)
        tile.sq, tile.lab = sq, lab
        tiles.add(tile)
    tiles.arrange(RIGHT, buff=buff).move_to(np.array([BOARD_CX, y, 0]))
    tiles.x = {v: t.get_center()[0] for v, t in zip(values, tiles)}
    tiles.y = y
    return tiles


def marker(x: float, y: float, color: str = MARK_COLOR,
           label: str | None = None, label_side: str = "up") -> VGroup:
    dot = Dot(np.array([x, y, 0.0]), radius=0.11, color=color)
    grp = VGroup(dot)
    if label is not None:
        tag = board_text(label, 15, color, "BOLD")
        if label_side == "right":
            # above the dot but nudged to the right: sitting BESIDE the dot put
            # the label straight on top of the number line
            tag.next_to(dot, UP, buff=0.16).shift(RIGHT * 0.42)
        else:
            tag.next_to(dot, UP, buff=0.16)
        grp.add(tag)
    grp.dot = dot
    return grp


def routine_card(title: str, caption: str, color: str,
                 width: float = 1.9, height: float = 0.95) -> VGroup:
    box = RoundedRectangle(corner_radius=0.07, width=width, height=height,
                           stroke_color=color, stroke_width=2,
                           fill_color="#16202B", fill_opacity=0.8)
    name = board_text(title, 15, color, "BOLD").move_to(box.get_center())
    cap = board_text(caption, 12, CHALK_WHITE).next_to(box, DOWN, buff=0.14)
    grp = VGroup(box, name, cap)
    grp.box, grp.name = box, name
    return grp


def summary_row(n: int, label: str, math_tex: str, color: str) -> VGroup:
    badge = Circle(radius=0.19, stroke_color=color, stroke_width=2,
                   fill_color=color, fill_opacity=0.18)
    num = board_text(str(n), 17, color, "BOLD").move_to(badge.get_center())
    return VGroup(VGroup(badge, num),
                  board_text(label, 17, CHALK_WHITE),
                  MathTex(math_tex, font_size=21)).arrange(RIGHT, buff=0.26)


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "Today we use the number line to do operations.<bookmark mark='b0'/> "
        "Adding moves us to the right, subtracting moves us to the left, and "
        "multiplying makes equal jumps.<bookmark mark='b1'/> Let's play a "
        "number game!<bookmark mark='b2'/>"
    ),
    "scene1": (
        "Imagine a floor marked with numbers.<bookmark mark='b0'/> A student "
        "stands on two. The teacher says: move three steps forward.<bookmark "
        "mark='b1'/> One, two, three; she lands on five.<bookmark mark='b2'/> "
        "So what did she just do? She added. Two plus three equals five."
        "<bookmark mark='b3'/>"
    ),
    "scene2": (
        "Let's remember our number line.<bookmark mark='b0'/> Zero is the "
        "starting point.<bookmark mark='b1'/> Then come one, two, three, four, "
        "five, and we keep going: six, seven, eight, nine, ten.<bookmark "
        "mark='b2'/> The arrow shows that the whole numbers never end."
        "<bookmark mark='b3'/> And every step has the same size; that is what "
        "makes a number line useful.<bookmark mark='b4'/>"
    ),
    "scene3": (
        "Now let's add on the number line. Two plus three.<bookmark mark='b0'/> "
        "We start at two.<bookmark mark='b1'/> We make three jumps to the "
        "right: one, two, three.<bookmark mark='b2'/> We land on five."
        "<bookmark mark='b3'/> So two plus three equals five. Addition means "
        "moving right.<bookmark mark='b4'/>"
    ),
    "scene4": (
        "Subtraction is the opposite. Six minus two.<bookmark mark='b0'/> We "
        "start at six.<bookmark mark='b1'/> We make two jumps to the left: "
        "one, two.<bookmark mark='b2'/> We land on four, so six minus two "
        "equals four.<bookmark mark='b3'/> Subtraction means moving left."
        "<bookmark mark='b4'/>"
    ),
    "scene5": (
        "Multiplication is repeated addition. Four times two.<bookmark "
        "mark='b0'/> We start at zero and make four jumps, each of two units."
        "<bookmark mark='b1'/> Two, four, six, eight.<bookmark mark='b2'/> "
        "Four times two is two plus two plus two plus two, which is eight."
        "<bookmark mark='b3'/> Multiplication means equal jumps.<bookmark "
        "mark='b4'/>"
    ),
    "scene6": (
        "Let's compare the three operations.<bookmark mark='b0'/> Addition "
        "moves right: two plus three lands on five.<bookmark mark='b1'/> "
        "Subtraction moves left: six minus two lands on four.<bookmark "
        "mark='b2'/> Multiplication repeats equal jumps: four times two lands "
        "on eight.<bookmark mark='b3'/>"
    ),
    "scene7": (
        "Now a game from the textbook. Raju asks Gayatri: start at zero and "
        "jump three, then eight, then five. Where will you land?<bookmark "
        "mark='b0'/> First jump: zero plus three is three.<bookmark mark='b1'/> "
        "Second jump: three plus eight is eleven.<bookmark mark='b2'/> Third "
        "jump: eleven plus five is sixteen.<bookmark mark='b3'/> So three plus "
        "eight plus five equals sixteen.<bookmark mark='b4'/>"
    ),
    "scene8": (
        "Here is a simple routine for every number-line question.<bookmark "
        "mark='b0'/> First, find the starting number.<bookmark mark='b1'/> Then "
        "read the operation.<bookmark mark='b2'/> Then decide how to move: "
        "right, left, or equal jumps.<bookmark mark='b3'/> And finally, write "
        "down where you landed.<bookmark mark='b4'/>"
    ),
    "scene9_setup": (
        "Your turn!<bookmark mark='b0'/> Here is the question: five times "
        "three.<bookmark mark='b1'/> How many jumps should we make, and how "
        "big is each jump?<bookmark mark='b2'/> Start from zero, and pause the "
        "video to try it.<bookmark mark='b3'/>"
    ),
    "scene9_reveal": (
        "Let's check.<bookmark mark='b0'/> Five jumps of three units each."
        "<bookmark mark='b1'/> Three, six, nine, twelve, fifteen.<bookmark "
        "mark='b2'/> So five times three equals fifteen: five jumps, and the "
        "landing position is fifteen.<bookmark mark='b3'/>"
    ),
    "scene10": (
        "Let's recall.<bookmark mark='b0'/> Addition moves right: two plus "
        "three equals five.<bookmark mark='b1'/> Subtraction moves left: six "
        "minus two equals four.<bookmark mark='b2'/> Multiplication makes equal "
        "jumps: four times two equals eight.<bookmark mark='b3'/> And five "
        "times three equals fifteen.<bookmark mark='b4'/> A number line makes "
        "operations visible.<bookmark mark='b5'/> Thank you for watching!"
        "<bookmark mark='b6'/>"
    ),
}


class OperationsOnWholeNumbersStory(VoiceoverScene):
    """Story-mode chalkboard lesson: Operations on Whole Numbers (Class 6)."""

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
        out_dir = _HERE / "media" / "videos" / "operations_on_whole_numbers"
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
        self.beat1_floor()
        self.beat2_recall()
        self.beat3_addition()
        self.beat4_subtraction()
        self.beat5_multiplication()
        self.beat6_patterns()
        self.beat7_game()
        self.beat8_routine()
        self.beat9_challenge()
        self.beat10_summary()

        self._write_real_srt()

    # ================================================================ beats ==

    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Operations on Whole Numbers", 38, CHALK_WHITE,
                               "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 1.6, 0]))
            self.play(Write(title), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            sub = board_text("Move right, move left, jump equally", 21,
                             CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 0.9, 0]))
            self.play(Write(sub), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.4))

            line = num_line([0, 1, 2, 3, 4, 5], x0=-1.75, step=0.9, y=-0.75,
                            size=26)
            mk = marker(line.x[2], line.y)
            self.play(FadeIn(line, shift=DOWN * 0.1), FadeIn(mk),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.6))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(Indicate(mk.dot, color=MARK_COLOR, scale_factor=1.6),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: math can be movement --------------------------------------
    def beat1_floor(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("Let's Play a Number Game", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            tiles = tile_row([0, 1, 2, 3, 4, 5], size=0.92, buff=0.12, y=-0.25)
            mk = marker(tiles.x[2], tiles.y)

            # the floor tiles are the preamble; the marker appears only when
            # "A student stands on two" is spoken
            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))
            self.play(FadeIn(tiles, shift=UP * 0.1),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            steps = board_text("Move 3 steps forward.", 20, CHALK_CYAN, "BOLD"
                               ).move_to(np.array([BOARD_CX, 1.65, 0]))
            self.play(FadeIn(steps, shift=RIGHT * 0.12), FadeIn(mk),
                      Indicate(tiles[2].sq, color=MARK_COLOR, scale_factor=1.1),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            hops = [hop_arc(tiles.x[i], tiles.x[i + 1], tiles.y, RIGHT_COLOR,
                            label=str(i - 1), height=0.38)
                    for i in (2, 3, 4)]
            self.play(Create(hops[0].arc), FadeIn(hops[0].label),
                      mk.animate.move_to(tiles[3].get_center()),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.34))
            self.play(Create(hops[1].arc), FadeIn(hops[1].label),
                      mk.animate.move_to(tiles[4].get_center()),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            self.play(Create(hops[2].arc), FadeIn(hops[2].label),
                      mk.animate.move_to(tiles[5].get_center()),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            eq = MathTex("2+3=5", font_size=36, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, -1.7, 0]))
            ebox = SurroundingRectangle(eq, color=RESULT_COLOR, buff=0.16,
                                        corner_radius=0.1, stroke_width=3)
            tag = board_text("Math can be movement!", 19, CHALK_YELLOW, "BOLD"
                             ).move_to(np.array([BOARD_CX, -2.45, 0]))
            self.play(FadeOut(steps),
                      Indicate(tiles[5].lab, color=RESULT_COLOR,
                               scale_factor=1.6),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            self.play(Write(eq), Create(ebox), FadeIn(tag),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: recall the whole-number line -------------------------------
    def beat2_recall(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("The Whole Number Line", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            line = num_line(list(range(11)), x0=-2.9, step=0.62, y=-0.6, size=26)
            whole = MathTex(r"W=\{0,1,2,3,\ldots\}", font_size=30,
                            color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, 1.55, 0]))

            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))
            # the axis and zero appear on "Zero is the starting point.", the
            # dots 1-5 on the first half of the counting line and 6-10 on the
            # second half, so the numbers arrive as they are counted
            self.play(Create(line[0]), FadeIn(line.dots[0]),
                      FadeIn(line.labels[0]),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(FadeIn(VGroup(*[line.dots[v] for v in range(1, 6)],
                                    *[line.labels[v] for v in range(1, 6)]),
                             shift=UP * 0.1),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(VGroup(*[line.dots[v] for v in range(6, 11)],
                                    *[line.labels[v] for v in range(6, 11)]),
                             shift=UP * 0.1),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            # "the whole numbers never end": the set notation belongs here, and
            # the stray marker on 2 has been removed (it belongs to scene 3)
            self.play(Indicate(line.dots[10], color=LINE_COLOR, scale_factor=2.0),
                      Write(whole),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            same = board_text("Every step has equal distance.", 20, CHALK_GREEN,
                              "BOLD").move_to(np.array([BOARD_CX, -2.0, 0]))
            self.play(FadeIn(same, shift=UP * 0.1),
                      Flash(same, color=CHALK_GREEN, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- shared builder for the three operation beats ------------------------
    def _operation_beat(self, tracker, *, heading: str, question: str,
                        start: int, jumps: int, jump_size: int, color: str,
                        move_label: str, answer_eq: str,
                        direction: int = 1):
        """Add / subtract / multiply on the same 0..10 line."""
        head = board_text(heading, 24, CHALK_AMBER, "BOLD").move_to(
            np.array([BOARD_CX, HEAD_Y, 0]))
        line = num_line(list(range(11)), x0=-2.9, step=0.62, y=-0.75, size=24)
        q = MathTex(question, font_size=34, color=color).move_to(
            np.array([BOARD_CX, 1.5, 0]))
        mk = marker(line.x[start], line.y)
        start_lbl = board_text(f"Start at {start}.", 19, MARK_COLOR, "BOLD"
                               ).move_to(np.array([BOARD_CX, 0.8, 0]))

        self.play(Write(head), run_time=rt(
            tracker.time_until_bookmark("b0") * 0.35))
        self.play(Create(line[0]),
                  *[FadeIn(line.dots[v]) for v in range(11)],
                  *[FadeIn(line.labels[v]) for v in range(11)],
                  Write(q), FadeIn(mk),
                  run_time=rt(tracker.time_until_bookmark("b0")))
        self.add_sound(self.sfx["pop"], gain=-13)

        self.play(FadeIn(start_lbl, shift=RIGHT * 0.12),
                  Indicate(mk.dot, color=MARK_COLOR, scale_factor=1.7),
                  run_time=rt(tracker.time_until_bookmark("b1")))
        self.add_sound(self.sfx["ding"], gain=-13)

        # the jumps: equal, one per unit step, spread across the b2 interval
        for k in range(jumps):
            frac = 1.0 / (jumps - k)
            run_time = rt(tracker.time_until_bookmark("b2") * frac)
            a = start + direction * k * jump_size
            b = start + direction * (k + 1) * jump_size
            hop = hop_arc(line.x[a], line.x[b], line.y, color,
                          label=("1" if jump_size == 1 else f"+{jump_size}"))
            self.play(Create(hop.arc), FadeIn(hop.label),
                      mk.animate.move_to(np.array([line.x[b], line.y, 0.0])),
                      run_time=run_time)
            self.add_sound(self.sfx["click"], gain=-15)

        land = start + direction * jumps * jump_size
        ans = MathTex(answer_eq, font_size=34, color=color).move_to(
            np.array([BOARD_CX, -1.9, 0]))
        abox = SurroundingRectangle(ans, color=color, buff=0.16,
                                    corner_radius=0.1, stroke_width=3)
        self.play(Flash(line.dots[land], color=RESULT_COLOR, flash_radius=0.5),
                  Indicate(line.dots[land], color=RESULT_COLOR,
                           scale_factor=2.0),
                  run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
        self.play(Write(ans), Create(abox),
                  run_time=rt(tracker.time_until_bookmark("b3")))
        self.add_sound(self.sfx["ding"], gain=-13)

        # the move label sits clear below the boxed answer: at -2.5 the box's
        # lower edge ran straight through the words
        note = board_text(move_label, 20, color, "BOLD").move_to(
            np.array([BOARD_CX, -2.6, 0]))
        self.play(FadeOut(start_lbl), FadeIn(note),
                  Flash(note, color=color, flash_radius=0.7),
                  run_time=rt(tracker.time_until_bookmark("b4")))
        self.add_sound(self.sfx["success"], gain=-11)
        self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    def beat3_addition(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()
            self._operation_beat(
                tracker, heading="Addition = Move Right", question="2+3=?",
                start=2, jumps=3, jump_size=1, color=RIGHT_COLOR,
                move_label="ADDITION → MOVE RIGHT", answer_eq="2+3=5")

    def beat4_subtraction(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()
            self._operation_beat(
                tracker, heading="Subtraction = Move Left", question="6-2=?",
                start=6, jumps=2, jump_size=1, color=LEFT_COLOR,
                move_label="SUBTRACTION → MOVE LEFT", answer_eq="6-2=4",
                direction=-1)

    def beat5_multiplication(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            self.reset_board()
            self._operation_beat(
                tracker, heading="Multiplication = Equal Jumps",
                question=r"4\times2=?", start=0, jumps=4, jump_size=2,
                color=MULT_COLOR, move_label="MULTIPLICATION → EQUAL JUMPS",
                answer_eq=r"4\times2=2+2+2+2=8")

    # -- Scene 6: three patterns stacked -------------------------------------
    def beat6_patterns(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("Three Operations, Three Patterns", 23,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.3))

            specs = [
                ("Addition", RIGHT_COLOR, 2, 3, 1, "2+3=5"),
                ("Subtraction", LEFT_COLOR, 6, 2, 1, "6-2=4"),
                ("Multiplication", MULT_COLOR, 0, 4, 2, r"4\times2=8"),
            ]
            ys = [1.5, 0.35, -0.9]
            rows = []
            for (name, color, start, jumps, size, eq), y in zip(specs, ys):
                lbl = board_text(name, 17, color, "BOLD").move_to(
                    np.array([BOARD_LEFT + 1.05, y, 0]))
                line = num_line(list(range(11)), x0=-1.95, step=0.44,
                                y=y - 0.4, size=17, pad=0.32, label_every=2)
                eqm = MathTex(eq, font_size=24, color=color).move_to(
                    np.array([BOARD_RIGHT - 1.15, y, 0]))
                rows.append({"lbl": lbl, "line": line, "eqm": eqm,
                             "color": color, "start": start, "jumps": jumps,
                             "size": size})

            # all three little lines are laid out first, then replayed one by one
            self.play(FadeIn(VGroup(*[r["line"] for r in rows])),
                      FadeIn(VGroup(*[r["lbl"] for r in rows])),
                      FadeIn(VGroup(*[r["eqm"] for r in rows])),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            for i, (row, mark) in enumerate(zip(rows, ("b1", "b2", "b3"))):
                line, color = row["line"], row["color"]
                mk = marker(line.x[row["start"]], line.y, color=color)
                step = row["size"]
                direction = -1 if row["lbl"].text == "Subtraction" else 1
                # the marker of this row appears on this row's own sentence:
                # the hops then share the rest of that window equally
                self.play(FadeIn(mk), run_time=rt(
                    tracker.time_until_bookmark(mark) * 0.15))
                for k in range(row["jumps"]):
                    a = row["start"] + direction * k * step
                    b = row["start"] + direction * (k + 1) * step
                    hop = hop_arc(line.x[a], line.x[b], line.y, color,
                                  height=0.3)
                    frac = 1.0 / (row["jumps"] - k)
                    # the very last hop keeps a slice of its window for the
                    # closing table, which otherwise gets a zero-length play
                    if i == len(rows) - 1 and k == row["jumps"] - 1:
                        frac *= 0.75
                    self.play(Create(hop.arc),
                              mk.animate.move_to(np.array([line.x[b], line.y, 0.0])),
                              run_time=rt(tracker.time_until_bookmark(mark)
                                          * frac))
                self.add_sound(self.sfx["click"], gain=-15)

            table = board_text("Right    |    Left    |    Equal jumps", 17,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.1, 0]))
            self.play(FadeIn(table, shift=UP * 0.1),
                      Flash(table, color=CHALK_WHITE, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: Gayatri's journey ------------------------------------------
    def beat7_game(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("The Number-Line Game", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            line = num_line(list(range(17)), x0=-3.9, step=0.48, y=-0.5,
                            size=18)
            mk = marker(line.x[0], line.y, label="Gayatri", label_side="right")
            self.play(Write(heading), Create(line[0]),
                      *[FadeIn(line.dots[v]) for v in range(17)],
                      *[FadeIn(line.labels[v]) for v in range(17)],
                      FadeIn(mk),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.5))
            ask = board_text("Where will Gayatri reach?", 19, CHALK_CYAN,
                             "BOLD").move_to(np.array([BOARD_CX, 1.85, 0]))
            self.play(FadeIn(ask, shift=RIGHT * 0.12),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            leaps = [(0, 3, "0+3=3", "b1"), (3, 11, "3+8=11", "b2"),
                     (11, 16, "11+5=16", "b3")]
            for i, (a, b, eq, mark) in enumerate(leaps):
                hop = hop_arc(line.x[a], line.x[b], line.y, RIGHT_COLOR,
                              label=f"+{b - a}", label_height=0.56)
                eqm = MathTex(eq, font_size=26, color=RIGHT_COLOR).move_to(
                    np.array([BOARD_RIGHT - 1.25, 1.15 - i * 0.42, 0]))
                self.play(Create(hop.arc), FadeIn(hop.label), Write(eqm),
                          mk.animate.move_to(np.array([line.x[b], line.y, 0.0])),
                          run_time=rt(tracker.time_until_bookmark(mark)))
                self.add_sound(self.sfx["click"], gain=-15)

            final = MathTex("3+8+5=16", font_size=34, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, -2.0, 0]))
            fbox = SurroundingRectangle(final, color=RESULT_COLOR, buff=0.16,
                                        corner_radius=0.1, stroke_width=3)
            self.play(FadeOut(ask), Write(final), Create(fbox),
                      Flash(line.dots[16], color=RESULT_COLOR, flash_radius=0.6),
                      Indicate(line.dots[16], color=RESULT_COLOR,
                               scale_factor=2.2),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the routine ------------------------------------------------
    def beat8_routine(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("A Simple Routine", 24, CHALK_AMBER, "BOLD"
                                 ).move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            cards = VGroup(
                routine_card("START", "where do I begin?", MARK_COLOR),
                routine_card("OPERATE", "what is asked?", CHALK_WHITE),
                routine_card("MOVE", "right, left or jumps?", CHALK_CYAN),
                routine_card("RESULT", "where did I land?", RESULT_COLOR),
            ).arrange(RIGHT, buff=0.45).move_to(np.array([BOARD_CX, 0.7, 0]))
            arrows = VGroup(*[
                Arrow(cards[i].get_right() + RIGHT * 0.04,
                      cards[i + 1].get_left() + LEFT * 0.04,
                      buff=0.02, color=CHALK_YELLOW, stroke_width=2.4,
                      tip_length=0.14)
                for i in range(3)
            ])
            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.35))
            self.play(FadeIn(cards, shift=DOWN * 0.12),
                      *[GrowArrow(a) for a in arrows],
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            # all four cards are highlighted on their own step, including the
            # RESULT card on "finally, write down where you landed"; the process
            # strip then fills the rest of that window
            for k, mark in enumerate(("b1", "b2", "b3", "b4")):
                frac = 0.5 if k == 3 else 1.0
                self.play(Indicate(cards[k], color=cards[k].name.get_color(),
                                   scale_factor=1.06),
                          run_time=rt(tracker.time_until_bookmark(mark) * frac))
                self.add_sound(self.sfx["click"], gain=-15)

            process = board_text("Start → Understand → Move → Answer", 19,
                                 CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.6, 0]))
            self.play(FadeIn(process, shift=UP * 0.1),
                      Flash(process, color=CHALK_YELLOW, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 9: student challenge -----------------------------------------
    def beat9_challenge(self) -> None:
        with self.voiceover(text=NARRATION["scene9_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", 30, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y - 0.05, 0]))
            q = MathTex(r"5\times3=?", font_size=36, color=MULT_COLOR).move_to(
                np.array([BOARD_CX, 1.75, 0]))
            line = num_line(list(range(16)), x0=-3.6, step=0.5, y=-0.35, size=20)
            ask1 = board_text("How many jumps?", 19, CHALK_WHITE, "BOLD"
                              ).move_to(np.array([BOARD_CX, 0.85, 0]))
            ask2 = board_text("What is the size of each jump?", 19, CHALK_WHITE,
                              "BOLD").move_to(np.array([BOARD_CX, 0.35, 0]))
            hint = board_text("Start from zero — pause and try it.", 18,
                              CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.6, 0]))

            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.play(Create(line[0]),
                      *[FadeIn(line.dots[v]) for v in range(16)],
                      *[FadeIn(line.labels[v]) for v in range(16)],
                      Write(q),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(FadeIn(ask1, shift=RIGHT * 0.12), run_time=rt(
                tracker.time_until_bookmark("b2") * 0.5))
            self.play(FadeIn(ask2, shift=RIGHT * 0.12), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(hint, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b3")))

            self.challenge = {"line": line, "q": q, "ask1": ask1,
                              "ask2": ask2, "hint": hint}
            self._capture_srt(tracker)

        play_challenge_countdown(self, seconds=4, sfx=self.sfx)

        with self.voiceover(text=NARRATION["scene9_reveal"]) as tracker:
            line, q = self.challenge["line"], self.challenge["q"]
            mk = marker(line.x[0], line.y, color=MULT_COLOR)
            # b0: "Let's check." -- clear the questions, drop the marker on 0
            self.play(FadeOut(self.challenge["ask1"]),
                      FadeOut(self.challenge["ask2"]),
                      FadeOut(self.challenge["hint"]),
                      FadeIn(mk),
                      run_time=rt(tracker.time_until_bookmark("b0")))

            # b0 -> b1 "Five jumps of three units each:" -- the first three
            # jumps; b1 -> b2 "Three, six, nine, twelve, fifteen." -- the last
            # two jumps and the running sum
            for k in range(5):
                a, b = 3 * k, 3 * (k + 1)
                hop = hop_arc(line.x[a], line.x[b], line.y, MULT_COLOR,
                              label="+3", label_height=0.45, label_size=18,
                              height=0.32)
                if k < 3:
                    when, frac = "b1", 1.0 / (3 - k)
                else:
                    when, frac = "b2", 0.5 / (5 - k)
                self.play(Create(hop.arc), FadeIn(hop.label),
                          mk.animate.move_to(np.array([line.x[b], line.y, 0.0])),
                          run_time=rt(tracker.time_until_bookmark(when) * frac))
                self.add_sound(self.sfx["click"], gain=-15)

            sum_eq = MathTex("3+3+3+3+3=15", font_size=30, color=MULT_COLOR
                             ).move_to(np.array([BOARD_CX, -1.5, 0]))
            self.play(Write(sum_eq), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            ans = MathTex(r"5\times3=15", font_size=38, color=CHALK_WHITE
                          ).move_to(np.array([BOARD_CX, -2.25, 0]))
            abox = SurroundingRectangle(ans, color=RESULT_COLOR, buff=0.16,
                                        corner_radius=0.1, stroke_width=3)
            note = board_text("5 jumps · lands on 15", 17, RESULT_COLOR, "BOLD"
                              ).move_to(np.array([BOARD_CX, 1.75, 0]))
            self.play(Write(ans), Create(abox), FadeOut(q),
                      Flash(line.dots[15], color=RESULT_COLOR, flash_radius=0.6),
                      Indicate(line.dots[15], color=RESULT_COLOR,
                               scale_factor=2.2),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            self.play(FadeIn(note, shift=RIGHT * 0.12),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 10: summary + thanks -----------------------------------------
    def beat10_summary(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("Summary", 30, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y - 0.05, 0]))
            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0")))

            rows = VGroup(
                summary_row(1, "Addition moves right:", "2+3=5", RIGHT_COLOR),
                summary_row(2, "Subtraction moves left:", "6-2=4", LEFT_COLOR),
                summary_row(3, "Multiplication — equal jumps:",
                            r"4\times2=8", MULT_COLOR),
                summary_row(4, "Five jumps of three:", r"5\times3=15",
                            CHALK_WHITE),
            ).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
            rows.move_to(np.array([BOARD_CX, 0.95, 0]))
            rows.shift(RIGHT * (BOARD_CX - rows.get_center()[0]))

            # each row appears on its own recap line: row 1 on "Addition moves
            # right ...", row 4 on "And five times three equals fifteen."
            for k, mark in enumerate(("b1", "b2", "b3", "b4")):
                self.play(FadeIn(rows[k], shift=RIGHT * 0.12),
                          run_time=rt(tracker.time_until_bookmark(mark)))
                self.add_sound(self.sfx["click"], gain=-15)

            take = board_text("A Number Line Makes Operations Visible!", 21,
                              CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.5, 0]))
            support = board_text("Addition → Right      Subtraction → Left      "
                                 "Multiplication → Equal Jumps", 15, CHALK_CYAN
                                 ).move_to(np.array([BOARD_CX, -2.05, 0]))
            rule = board_text("Choose the operation, follow the movement, "
                              "read the landing number.", 17, CHALK_WHITE
                              ).move_to(np.array([BOARD_CX, -2.5, 0]))
            self.play(FadeIn(take), FadeIn(support), FadeIn(rule),
                      Flash(take, color=CHALK_YELLOW, flash_radius=0.9),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["success"], gain=-11)

            summary = VGroup(heading, rows, take, support, rule)
            self.play(FadeOut(summary), run_time=rt(
                tracker.time_until_bookmark("b6") * 0.35))

            thanks = board_text("Thank You for Watching!", 40, CHALK_WHITE,
                                "BOLD")
            thanks2 = board_text("See you in the next lesson :)", 25, CHALK_CYAN)
            thanks_group = VGroup(thanks, thanks2).arrange(DOWN, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY, 0]))
            self.play(Write(thanks), run_time=rt(
                tracker.time_until_bookmark("b6") * 0.4))
            self.add_sound(self.sfx["ding"], gain=-11)
            self.play(FadeIn(thanks2, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b6")))
            self.play(Circumscribe(thanks_group, color=CHALK_AMBER,
                                   stroke_width=3, time_width=0.5), run_time=0.3)
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(END_HOLD)


if __name__ == "__main__":
    pass

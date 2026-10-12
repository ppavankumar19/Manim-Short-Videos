"""
Solving Simple Equations — Undo to Find the Unknown
Story-mode chalkboard lesson (Telangana Class 8 Maths, Chapter 2:
Linear Equations in One Variable, Section 2.3).

Core idea: an equation is an operation machine. To solve it, run the machine
BACKWARD -- undo, in reverse order, whatever was done to the variable, until
the unknown stands alone. Then check the answer by substitution.

Production pipeline (mirrors the rest of the Story-Mode series):
  - shared assets/background2.png chalkboard + student/teacher cutouts +
    dhimantAI (top-left) and Mathematics (top-right) corner badges.
  - VoiceoverScene + speech service; narration written as natural prose.
  - synced_voice.install_synced_voiceover() re-times every word against the
    real audio (the service's own word timings drift by seconds).
  - real per-word SRT export (carry-safe timestamps).
  - sound effects from sound_effects.py, chalk-styled Text/MathTex.
  - story_common.play_challenge_countdown() for the "YOUR TURN" clock.

Title + 10 beats:
  0. Title card.
  1. The Number Machine -- ? -> x3 -> +1 -> 16, compressed to 3x+1=16.
  2. Run the Machine Backward -- 16 -1-> 15 -/3-> 5.
  3. What Does "Solve" Mean? -- isolate x; the x3 and +1 layers around x.
  4. Undo the Addition -- +1 crosses the '=' and becomes -1; 3x = 15.
  5. Undo the Multiplication -- 3 crosses to the denominator; x = 5.
  6. Check the Solution -- 3(5)+1 = 16, so 16 = 16.
  7. The Solving Routine -- identify, undo, isolate, check.
  8. Application -- "four times a number reduced by 5 equals 19" -> x = 6.
  9. Student Challenge -- 7x - 9 = 26 with the 10 s THINK clock -> x = 5.
 10. Recap -- forward and reverse machines collapse into the solution.
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
    ORIGIN, UP, DOWN, LEFT, RIGHT, UL, UR, DL, DR, PI, TAU, BLACK,
    ImageMobject, MathTex, VGroup, Line, Circle, Rectangle, RoundedRectangle,
    Square, Polygon, Dot, Arrow, Text, Write, FadeIn, FadeOut, Create,
    ReplacementTransform, TransformMatchingTex, GrowArrow, Indicate, Flash,
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

# Measured chalkboard safe bounds (shared across the series)
BOARD_LEFT = -4.6
BOARD_RIGHT = 5.6
BOARD_TOP = 3.3
BOARD_BOTTOM = -2.9
BOARD_CX = (BOARD_LEFT + BOARD_RIGHT) / 2  # 0.5
BOARD_CY = (BOARD_TOP + BOARD_BOTTOM) / 2  # 0.2

EQ_Y = 0.7          # the main equation line
ROW_Y = 0.95        # the operation-machine row
ROW2_Y = -1.85      # the reverse machine row

# Scene 8 is a two-column composition: the word phrase on the left, the
# equation working on the right, balanced symmetrically about the board centre.
WORDS_CX = BOARD_CX - 2.2
EQ_COL_CX = BOARD_CX + 2.2


def rt(seconds: float, floor: float = MIN_RT) -> float:
    return max(floor, float(seconds))


def board_text(s: str, size: int = 34, color: str = CHALK_WHITE,
               weight: str = "NORMAL") -> Text:
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def chalk_math(s: str, size: int = 34, color: str = MATH_COLOR) -> MathTex:
    return MathTex(s, font_size=size, color=color)


def align_equals(eq: MathTex, cx: float = BOARD_CX, cy: float = EQ_Y) -> MathTex:
    """Centre the whole equation line on the board (bbox centring)."""
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


# ----------------------------------------------------- machine vocabulary ---
def value_ring(label: str, color: str = CHALK_GREEN, r: float = 0.45) -> VGroup:
    """A circled result value, e.g. the machine's output 16."""
    ring = Circle(radius=r, stroke_color=color, stroke_width=2.5,
                  fill_color="#12240F", fill_opacity=0.6)
    txt = MathTex(label, font_size=30, color=color).move_to(ring.get_center())
    return VGroup(ring, txt)


def mystery_box(label: str = "?", size: float = 0.95,
                color: str = CHALK_AMBER) -> VGroup:
    """The hidden input of the machine."""
    box = RoundedRectangle(corner_radius=0.1, width=size, height=size,
                           stroke_color=color, stroke_width=2.5,
                           fill_color="#2A1D10", fill_opacity=0.6)
    lbl = MathTex(label, font_size=30, color=CHALK_CYAN).move_to(box.get_center())
    grp = VGroup(box, lbl)
    grp.lbl = lbl
    grp.shell = box
    return grp


def machine_row(stations: list, y: float, buff: float = 0.85):
    """Lay a row of stations out centred on the board, with arrows between."""
    row = VGroup(*stations).arrange(RIGHT, buff=buff)
    row.move_to(np.array([BOARD_CX, y, 0]))
    arrows = VGroup(*[
        Arrow(stations[i].get_right(), stations[i + 1].get_left(), buff=0.12,
              color=CHALK_WHITE, stroke_width=2.5)
        for i in range(len(stations) - 1)
    ])
    return row, arrows


# ------------------------------------------------- realistic machine icons ---
# Ported from the series' own icon vocabulary (Transposition-Balancing-Scales
# and Identities-and-Inverses) so the machine looks like a machine instead of
# a plain labelled box.

def drop_shadow(mobj: VGroup, dx: float = 0.05, dy: float = -0.06,
                opacity: float = 0.3) -> VGroup:
    shadow = mobj.copy()
    shadow.set_fill(BLACK, opacity=opacity)
    shadow.set_stroke(width=0)
    shadow.shift(np.array([dx, dy, 0]))
    return VGroup(shadow, mobj)


def detective_hat(color: str = "#5A3B1E", width: float = 0.8) -> VGroup:
    """A jaunty detective fedora: curved brim, creased crown, ribbon."""
    brim = RoundedRectangle(corner_radius=0.06, width=width, height=0.12,
                            stroke_color=CHALK_AMBER, stroke_width=1.8,
                            fill_color=color, fill_opacity=0.95)
    crown_w = width * 0.62
    crown = RoundedRectangle(corner_radius=0.08, width=crown_w, height=0.32,
                             stroke_color=CHALK_AMBER, stroke_width=1.8,
                             fill_color=color, fill_opacity=0.95).next_to(
        brim, UP, buff=-0.02)
    ribbon = RoundedRectangle(corner_radius=0.02, width=crown_w, height=0.07,
                              stroke_width=0, fill_color=CHALK_YELLOW,
                              fill_opacity=0.9).move_to(crown.get_bottom() + UP * 0.04)
    hat = VGroup(brim, crown, ribbon)
    hat.rotate(np.radians(-6))
    return hat


def mystery_crate(width: float = 1.0, height: float = 0.95) -> VGroup:
    """A wooden mystery crate with a detective hat and an empty cyan medallion
    (the '?' / 'x' label is drawn by the caller so it can morph)."""
    body = RoundedRectangle(corner_radius=0.06, width=width, height=height,
                            stroke_color=CHALK_AMBER, stroke_width=2.5)
    body.set_fill(color=["#2B1A0E", "#4A2E18", "#6B4424"], opacity=0.9)
    planks = VGroup(*[
        Line(body.get_left() + UP * y, body.get_right() + UP * y,
             stroke_color="#1F130A", stroke_width=1.2, stroke_opacity=0.6)
        for y in np.linspace(-height * 0.28, height * 0.28, 3)
    ])
    brackets = VGroup(*[
        Square(side_length=0.14, stroke_color=CHALK_AMBER, stroke_width=1.2,
               fill_color="#1F130A", fill_opacity=0.7).move_to(body.get_corner(c))
        for c in (UL, UR, DL, DR)
    ])
    badge = Circle(radius=0.24, stroke_color=CHALK_CYAN, stroke_width=2,
                   fill_color="#1B3333", fill_opacity=0.85).move_to(body.get_center())
    lid = RoundedRectangle(corner_radius=0.04, width=width * 1.06, height=0.14,
                           stroke_color=CHALK_AMBER, stroke_width=2.2,
                           fill_color=["#6B4424", "#4A2E18"],
                           fill_opacity=0.95).next_to(body, UP, buff=-0.04)
    hat = detective_hat(width=width * 0.82).next_to(lid, UP, buff=-0.06)
    crate = VGroup(body, planks, brackets, badge, lid, hat)
    wrapped = drop_shadow(crate, dx=0.05, dy=-0.06, opacity=0.25)
    wrapped.badge = badge
    return wrapped


def machine_icon(symbol: str, color: str, scale: float = 0.42,
                 op_size: int = 40) -> VGroup:
    """An operation machine: funnel intake, dial gauge, a big operation panel
    and a chute outlet -- so the operation on x is clearly readable."""
    body_w, body_h = 3.0, 1.5
    body = RoundedRectangle(width=body_w, height=body_h, corner_radius=0.16,
                            stroke_color=color, stroke_width=2.5,
                            fill_color="#2A1E10", fill_opacity=0.5)
    funnel = Polygon(
        np.array([-body_w * 0.28, body_h / 2, 0]),
        np.array([body_w * 0.28, body_h / 2, 0]),
        np.array([body_w * 0.1, body_h / 2 + 0.3, 0]),
        np.array([-body_w * 0.1, body_h / 2 + 0.3, 0]),
        stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.15)
    chute = Polygon(
        np.array([-body_w * 0.1, -body_h / 2, 0]),
        np.array([body_w * 0.1, -body_h / 2, 0]),
        np.array([body_w * 0.22, -body_h / 2 - 0.28, 0]),
        np.array([-body_w * 0.22, -body_h / 2 - 0.28, 0]),
        stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.15)
    dial_center = LEFT * 0.85
    dial = Circle(radius=0.24, stroke_color=color, stroke_width=2.2,
                  fill_color="#1A140A", fill_opacity=0.6).move_to(dial_center)
    dial_ticks = VGroup(*[
        Line(dial_center + 0.16 * np.array([np.cos(a), np.sin(a), 0]),
             dial_center + 0.24 * np.array([np.cos(a), np.sin(a), 0]),
             stroke_color=color, stroke_width=1.4)
        for a in np.linspace(0, 2 * np.pi, 8, endpoint=False)
    ])
    lights = VGroup(
        Dot(radius=0.05, color=CHALK_GREEN).move_to(LEFT * 0.85 + UP * 0.52),
        Dot(radius=0.05, color=CHALK_RED).move_to(LEFT * 0.55 + UP * 0.52),
    )
    # big central panel so the operation reads at 360p
    op_panel = RoundedRectangle(width=1.25, height=0.75, corner_radius=0.08,
                                stroke_color=color, stroke_width=1.6,
                                fill_color="#1A140A", fill_opacity=0.75).move_to(
        RIGHT * 0.45)
    op_lbl = MathTex(symbol, font_size=op_size, color=CHALK_WHITE).move_to(
        op_panel.get_center())
    machine = VGroup(chute, body, funnel, dial, dial_ticks, lights, op_panel,
                     op_lbl).scale(scale)
    return drop_shadow(machine, dx=0.04, dy=-0.05, opacity=0.25)


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "Today we learn to solve simple linear equations.<bookmark mark='b0'/> "
        "We will undo the operations around the unknown, one at a time."
        "<bookmark mark='b1'/> Let's start with a number machine!"
        "<bookmark mark='b2'/>"
    ),
    "scene1": (
        "A number goes into the machine.<bookmark mark='b0'/> First it is "
        "multiplied by three,<bookmark mark='b1'/> and then one is added."
        "<bookmark mark='b2'/> Out comes sixteen.<bookmark mark='b3'/> What "
        "number went in? We know the operations, and we know the result — but "
        "not the starting number.<bookmark mark='b4'/> That is exactly the "
        "kind of problem a simple equation solves: three x plus one equals "
        "sixteen.<bookmark mark='b5'/>"
    ),
    "scene2": (
        "To find the input, we run the machine backward.<bookmark mark='b0'/> "
        "Adding one was the last operation, so we undo it first with minus "
        "one: sixteen minus one is fifteen.<bookmark mark='b1'/> Then we undo "
        "multiplying by three with dividing by three: fifteen divided by "
        "three is five.<bookmark mark='b2'/> So the number that went in was "
        "five.<bookmark mark='b3'/>"
    ),
    "scene3": (
        "Now let's write it as an equation: three x plus one equals sixteen."
        "<bookmark mark='b0'/> Solving an equation is not about moving numbers "
        "at random.<bookmark mark='b1'/> The goal is to isolate x — to strip "
        "away the operations around it until x stands alone."
        "<bookmark mark='b2'/> Two operations are attached to x: it is "
        "multiplied by three, and then one is added.<bookmark mark='b3'/>"
    ),
    "scene4": (
        "Addition is the outer operation, so we undo it first."
        "<bookmark mark='b0'/> One is added to x, so we subtract one — and as "
        "the one crosses the equals sign, plus becomes minus."
        "<bookmark mark='b1'/> Three x equals sixteen minus one."
        "<bookmark mark='b2'/> Sixteen minus one is fifteen, so three x "
        "equals fifteen.<bookmark mark='b3'/> Only the multiplication by "
        "three is left.<bookmark mark='b4'/>"
    ),
    "scene5": (
        "Three x means three times x, so we undo it with division."
        "<bookmark mark='b0'/> The three crosses the equals sign and becomes "
        "a divisor.<bookmark mark='b1'/> x equals fifteen divided by three."
        "<bookmark mark='b2'/> Fifteen divided by three is five."
        "<bookmark mark='b3'/> x equals five — the unknown is isolated, and "
        "the equation is solved.<bookmark mark='b4'/>"
    ),
    "scene6": (
        "But is five really correct? We check by putting five back into the "
        "original equation, in place of x.<bookmark mark='b0'/> Three times "
        "five is fifteen, plus one is sixteen.<bookmark mark='b1'/> Both "
        "sides give sixteen: sixteen equals sixteen.<bookmark mark='b2'/> "
        "The answer is verified.<bookmark mark='b3'/>"
    ),
    "scene7": (
        "Let's collect the method.<bookmark mark='b0'/> First, identify what "
        "is attached to x — here, times three, and plus one."
        "<bookmark mark='b1'/> Next, undo in reverse order: plus one is undone "
        "by minus one, and times three is undone by dividing by three. Then x "
        "stands alone: x equals five.<bookmark mark='b2'/> Finally, check by "
        "substituting the value back into the original equation."
        "<bookmark mark='b3'/> Identify, undo, isolate, check."
        "<bookmark mark='b4'/>"
    ),
    "scene8": (
        "Equations also solve word problems.<bookmark mark='b0'/> Four times a "
        "number, reduced by five, equals nineteen — so let the number be x."
        "<bookmark mark='b1'/> Four times x, minus five, equals nineteen."
        "<bookmark mark='b2'/> Undo the minus five: four x equals nineteen "
        "plus five, which is twenty four.<bookmark mark='b3'/> Divide by "
        "four: x equals six. The number is six.<bookmark mark='b4'/>"
    ),
    "scene9_setup": (
        "Your turn!<bookmark mark='b0'/> Solve seven x minus nine equals "
        "twenty six.<bookmark mark='b1'/> What should you undo first?"
        "<bookmark mark='b2'/> Pause the video, and try it yourself."
        "<bookmark mark='b3'/>"
    ),
    "scene9_reveal": (
        "First undo the minus nine: seven x equals twenty six plus nine, "
        "which is thirty five.<bookmark mark='b0'/> Then undo the times "
        "seven: x equals thirty five divided by seven.<bookmark mark='b1'/> "
        "That gives x equals five!<bookmark mark='b2'/> Well done — you used "
        "the same two steps.<bookmark mark='b3'/>"
    ),
    "scene10": (
        "Let's summarise the whole method.<bookmark mark='b0'/> Identify what "
        "is done to the unknown — here, multiplied by three, then one is "
        "added.<bookmark mark='b1'/> Undo those operations in reverse order: "
        "undo the addition, then undo the multiplication."
        "<bookmark mark='b2'/> Keep undoing until x stands alone — that gives "
        "the solution, x equals five.<bookmark mark='b3'/> And always check by "
        "putting your answer back into the original equation."
        "<bookmark mark='b4'/> Undo in reverse, isolate the unknown, and "
        "check. Thank you so much for watching, and I will see you in the "
        "next lesson!<bookmark mark='b5'/>"
    ),
}


class EquationSolvingStory(VoiceoverScene):
    """Story-mode chalkboard lesson: solving simple linear equations by
    undoing operations in reverse order."""

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
        out_dir = _HERE / "media" / "videos" / "equation_solving_story"
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
        # also drop a copy next to the rendered movie (caption burn-in)
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
        self.beat1_machine()
        self.beat2_backward()
        self.beat3_isolate()
        self.beat4_undo_addition()
        self.beat5_undo_multiplication()
        self.beat6_check()
        self.beat7_routine()
        self.beat8_application()
        self.beat9_challenge()
        self.beat10_recap()

        self._write_real_srt()

    # ================================================================ beats ==

    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Solving Simple Equations", 40,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 1.55, 0]))
            self.play(Write(title), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            sub = board_text("Undo to find the unknown", 22, CHALK_YELLOW,
                             "BOLD").move_to(np.array([BOARD_CX, BOARD_CY + 0.85, 0]))
            x_in = mystery_crate(width=0.8, height=0.78).move_to(
                np.array([-2.25, -0.55, 0]))
            c1 = machine_icon(r"\times 3", CHALK_CYAN, scale=0.32).move_to(
                np.array([-0.9, -0.55, 0]))
            c2 = machine_icon("+1", CHALK_PINK, scale=0.32).move_to(
                np.array([0.55, -0.55, 0]))
            out = value_ring("16", r=0.4).move_to(np.array([2.0, -0.55, 0]))
            mini_q = MathTex("?", font_size=24, color=CHALK_CYAN).move_to(
                x_in.badge.get_center())
            a1 = Arrow(x_in.get_right(), c1.get_left(), buff=0.1,
                       color=CHALK_WHITE, stroke_width=2.5)
            a2 = Arrow(c1.get_right(), c2.get_left(), buff=0.1,
                       color=CHALK_WHITE, stroke_width=2.5)
            a3 = Arrow(c2.get_right(), out.get_left(), buff=0.1,
                       color=CHALK_WHITE, stroke_width=2.5)
            preview = VGroup(x_in, mini_q, c1, c2, out, a1, a2, a3)
            # the mini machine must sit on the board's centre line
            preview.shift(RIGHT * (BOARD_CX - preview.get_center()[0]))
            self.play(Write(sub), FadeIn(preview, shift=DOWN * 0.1),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)

            question = board_text("What number went in?", 20, CHALK_PINK,
                                  "BOLD").move_to(np.array([BOARD_CX, -1.7, 0]))
            self.play(FadeIn(question), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["swipe"], gain=-15)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 1: The Number Machine ----------------------------------------
    def beat1_machine(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            top = board_text("A number goes into the machine...", 19,
                             CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.5, 0]))

            box = mystery_crate(width=0.95, height=0.9)
            mul = machine_icon(r"\times 3", CHALK_CYAN, scale=0.4)
            add = machine_icon("+1", CHALK_PINK, scale=0.4)
            out = value_ring("16")
            row, arrows = machine_row([box, mul, add, out], ROW_Y, buff=0.8)
            q_lbl = MathTex("?", font_size=30, color=CHALK_CYAN).move_to(
                box.badge.get_center())

            question = board_text("What number went in?", 19, CHALK_PINK,
                                  "BOLD").move_to(np.array([BOARD_CX, -1.15, 0]))

            self.play(FadeIn(top), run_time=rt(tracker.time_until_bookmark("b0") * 0.4))
            self.play(FadeIn(box, scale=0.8), FadeIn(q_lbl, scale=0.8),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(GrowArrow(arrows[0]), FadeIn(mul),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(GrowArrow(arrows[1]), FadeIn(add),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(GrowArrow(arrows[2]), FadeIn(out),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-12)

            self.play(FadeIn(question),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.4))
            x_lbl = MathTex("x", font_size=30, color=CHALK_CYAN).move_to(
                q_lbl.get_center())
            self.play(ReplacementTransform(q_lbl, x_lbl),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["click"], gain=-15)

            chain = MathTex(r"x \rightarrow 3x \rightarrow 3x+1 \rightarrow 16",
                            font_size=28).move_to(np.array([BOARD_CX, EQ_Y, 0]))
            eq = MathTex("3x+1", r"\;=\;", "16", font_size=50)
            align_equals(eq, BOARD_CX, EQ_Y)
            eq[0][1].set_color(CHALK_CYAN)
            eq_box = SurroundingRectangle(eq, color=CHALK_GREEN, buff=0.22,
                                          corner_radius=0.1, stroke_width=2)
            self.play(FadeIn(chain), FadeOut(top), FadeOut(box),
                      FadeOut(x_lbl), FadeOut(mul), FadeOut(add), FadeOut(out),
                      FadeOut(arrows), FadeOut(question),
                      run_time=rt(tracker.time_until_bookmark("b5") * 0.4))
            self.play(TransformMatchingTex(chain, eq), Create(eq_box),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["success"], gain=-11)

            self.eq = eq
            self.eq_box = eq_box
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 2: Run the machine backward ----------------------------------
    def beat2_backward(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("Undo in Reverse Order", 24, CHALK_CYAN,
                                 "BOLD").move_to(np.array([BOARD_CX, BOARD_TOP - 0.45, 0]))
            fwd_label = board_text("Forward", 15, CHALK_AMBER, "BOLD").move_to(
                np.array([-3.9, 1.75, 0]))
            back_label = board_text("Backward", 15, CHALK_GREEN, "BOLD").move_to(
                np.array([-3.9, 0.05, 0]))

            x_in = mystery_crate(width=0.78, height=0.76)
            f_mul = machine_icon(r"\times 3", CHALK_CYAN, scale=0.34)
            f_add = machine_icon("+1", CHALK_PINK, scale=0.34)
            f_out = value_ring("16", r=0.42)
            frow, farrows = machine_row([x_in, f_mul, f_add, f_out], 1.75, buff=0.8)
            f_q = MathTex("x", font_size=26, color=CHALK_CYAN).move_to(
                x_in.badge.get_center())
            frow = VGroup(frow, f_q)

            hidden = mystery_box("?", size=0.8, color=CHALK_GREEN)
            r_div = machine_icon(r"\div 3", CHALK_YELLOW, scale=0.34)
            r_sub = machine_icon("-1", CHALK_GREEN, scale=0.34)
            r_out = value_ring("16", r=0.42)
            rrow = VGroup(hidden, r_div, r_sub, r_out).arrange(RIGHT, buff=0.8)
            rrow.move_to(np.array([BOARD_CX, 0.05, 0]))
            rarrows = VGroup(*[
                Arrow(rrow[i + 1].get_left(), rrow[i].get_right(), buff=0.14,
                      color=CHALK_GREEN, stroke_width=2.5)
                for i in range(3)
            ])

            self.play(Write(heading), FadeIn(fwd_label), FadeIn(back_label),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.4))
            self.play(FadeIn(frow), FadeIn(farrows),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.4))
            self.play(FadeIn(rrow), FadeIn(rarrows),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            work1 = chalk_math(r"16 - 1 \;=\; 15", size=30, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, -1.1, 0]))
            self.play(Circumscribe(f_add, color=CHALK_PINK, stroke_width=3),
                      Circumscribe(r_sub, color=CHALK_GREEN, stroke_width=3),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.play(FadeIn(work1), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            work2 = chalk_math(r"15 \div 3 \;=\; 5", size=30, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, -1.85, 0]))
            self.play(Circumscribe(f_mul, color=CHALK_CYAN, stroke_width=3),
                      Circumscribe(r_div, color=CHALK_YELLOW, stroke_width=3),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            self.play(FadeIn(work2), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            answer = MathTex("x", r"\;=\;", "5", font_size=34, color=CHALK_GREEN)
            answer.move_to(hidden.get_center())
            self.play(ReplacementTransform(hidden, answer),
                      Flash(answer.get_center(), color=CHALK_GREEN, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 3: What does "solve" mean? -----------------------------------
    def beat3_isolate(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()

            heading = board_text("Solve = Isolate the Variable", 24, CHALK_CYAN,
                                 "BOLD").move_to(np.array([BOARD_CX, BOARD_TOP - 0.45, 0]))
            eq = MathTex("3x+1", r"\;=\;", "16", font_size=50)
            align_equals(eq, BOARD_CX, EQ_Y)
            eq[0][1].set_color(CHALK_CYAN)
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.4))
            self.play(Write(eq), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            goal = board_text("Goal: isolate x", 20, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -1.5, 0]))
            goal_arrow = Arrow(goal.get_top(), eq[0][1].get_bottom() + DOWN * 0.28,
                               buff=0.08, color=CHALK_GREEN, stroke_width=2.5)
            self.play(FadeIn(goal), GrowArrow(goal_arrow),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            shell_mul = SurroundingRectangle(eq[0][0:2], color=CHALK_CYAN, buff=0.14,
                                             corner_radius=0.1, stroke_width=2.5)
            lbl_mul = board_text("multiplied by 3", 14, CHALK_CYAN, "BOLD").move_to(
                np.array([eq[0][0:2].get_center()[0] - 0.1, 1.85, 0]))
            self.play(Create(shell_mul), FadeIn(lbl_mul),
                      Indicate(eq[0][1], color=CHALK_CYAN, scale_factor=1.4),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            shell_add = SurroundingRectangle(eq[0][2:4], color=CHALK_PINK, buff=0.14,
                                             corner_radius=0.1, stroke_width=2.5)
            lbl_add = board_text("then add 1", 14, CHALK_PINK, "BOLD").move_to(
                np.array([eq[0][2:4].get_center()[0] + 0.45, 1.85, 0]))
            self.play(Create(shell_add), FadeIn(lbl_add),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.6))
            self.play(Indicate(shell_add, color=CHALK_PINK, scale_factor=1.08),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-12)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 4: Undo the addition -----------------------------------------
    def beat4_undo_addition(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()

            heading = board_text("Step 1: Undo the +1", 22, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.45, 0]))
            rule = chalk_math(r"+\;\longleftrightarrow\;-", size=24,
                              color=CHALK_GREEN).move_to(np.array([BOARD_CX, 1.85, 0]))
            eq = MathTex("3x+1", r"\;=\;", "16", font_size=50)
            align_equals(eq, BOARD_CX, EQ_Y)
            eq[0][1].set_color(CHALK_CYAN)
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.4))
            self.play(Write(eq), FadeIn(rule),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-12)

            box1 = SurroundingRectangle(eq[0][2:4], color=CHALK_AMBER, buff=0.1,
                                        corner_radius=0.08, stroke_width=3)
            self.play(Create(box1), run_time=rt(tracker.time_until_bookmark("b1") * 0.3))

            new_eq = MathTex("3x", r"\;=\;", "16-1", font_size=48)
            align_equals(new_eq, BOARD_CX, EQ_Y)
            new_eq[0][1].set_color(CHALK_CYAN)
            landing = new_eq[2][2:4].get_center()
            apex = np.array([BOARD_CX, 2.35, 0.0])
            start = eq[0][2:4].get_center()
            mover = MathTex("+1", font_size=30, color=CHALK_PINK).move_to(start)
            self.play(mover.animate.move_to(apex),
                      eq[0][2:4].animate.set_opacity(0.25),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.35))
            mover_m = MathTex("-1", font_size=30, color=CHALK_GREEN).move_to(apex)
            self.play(ReplacementTransform(mover, mover_m),
                      Flash(apex, color=CHALK_YELLOW, flash_radius=0.45),
                      run_time=0.3)
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(mover_m.animate.move_to(landing),
                      TransformMatchingTex(eq, new_eq), FadeOut(mover_m),
                      FadeOut(box1),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            box16 = SurroundingRectangle(new_eq[2], color=CHALK_AMBER, buff=0.1,
                                         corner_radius=0.08, stroke_width=3)
            self.play(Create(box16),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.4))
            eq15 = MathTex("3x", r"\;=\;", "15", font_size=48)
            align_equals(eq15, BOARD_CX, EQ_Y)
            eq15[0][1].set_color(CHALK_CYAN)
            self.play(TransformMatchingTex(new_eq, eq15), FadeOut(box16),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            lbl_left = board_text("only the x3 is left", 16, CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX, -0.55, 0]))
            self.play(FadeIn(lbl_left),
                      Circumscribe(eq15[0][0:2], color=CHALK_CYAN, stroke_width=3),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-12)
            self.eq = eq15
            self.scene4_extras = VGroup(heading, rule, lbl_left)
            self._capture_srt(tracker)

        self.play(FadeOut(self.scene4_extras), run_time=0.4)
        self.wait(TRANSITION_HOLD)

    # -- Beat 5: Undo the multiplication -----------------------------------
    def beat5_undo_multiplication(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            eq = self.eq  # 3x = 15

            heading = board_text("Step 2: Undo the x3", 22, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.45, 0]))
            strip = chalk_math(r"\times \;\longleftrightarrow\; \div", size=24,
                               color=CHALK_YELLOW).move_to(
                np.array([BOARD_CX, 1.85, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.4))

            eq_times = MathTex(r"3\times x", r"\;=\;", "15", font_size=48)
            align_equals(eq_times, BOARD_CX, EQ_Y)
            eq_times[0][2].set_color(CHALK_CYAN)
            self.play(TransformMatchingTex(eq, eq_times), FadeIn(strip),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.6))
            self.play(Circumscribe(eq_times[0][0:1], color=CHALK_YELLOW, stroke_width=3),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-12)

            # the 3 crosses and lands below the fraction bar
            frac_eq = MathTex("x", r"\;=\;", r"\frac{15}{3}", font_size=48)
            align_equals(frac_eq, BOARD_CX, EQ_Y)
            frac_eq[0].set_color(CHALK_CYAN)
            landing = frac_eq[2][-1].get_center()
            apex = np.array([BOARD_CX, 2.35, 0.0])
            start = eq_times[0][0].get_center()
            mover = MathTex("3", font_size=30, color=CHALK_YELLOW).move_to(start)
            self.play(mover.animate.move_to(apex),
                      eq_times[0][0].animate.set_opacity(0.25),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.play(mover.animate.move_to(landing),
                      TransformMatchingTex(eq_times, frac_eq), FadeOut(mover),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["success"], gain=-11)

            self.play(Indicate(frac_eq[2], color=CHALK_WHITE, scale_factor=1.15),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            eq5 = MathTex("x", r"\;=\;", "5", font_size=52, color=CHALK_GREEN)
            align_equals(eq5, BOARD_CX, EQ_Y)
            self.play(TransformMatchingTex(frac_eq, eq5),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-11)

            ans_box = SurroundingRectangle(eq5, color=CHALK_GREEN, buff=0.2,
                                           corner_radius=0.1, stroke_width=3)
            done = board_text("x is isolated!", 18, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -0.6, 0]))
            self.play(Create(ans_box), FadeIn(done),
                      Flash(eq5, color=CHALK_GREEN, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self.scene5_extras = VGroup(heading, strip, ans_box, done)
            self._capture_srt(tracker)

        self.play(FadeOut(self.scene5_extras), run_time=0.4)
        self.wait(TRANSITION_HOLD)

    # -- Beat 6: Check the solution ----------------------------------------
    def beat6_check(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("Check the Solution", 24, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.45, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.4))

            eq_orig = MathTex("3x+1", r"\;=\;", "16", font_size=44)
            align_equals(eq_orig, BOARD_CX, 0.6)
            eq_orig[0][1].set_color(CHALK_CYAN)
            sol = MathTex("x", r"\;=\;", "5", font_size=30, color=CHALK_GREEN)
            sol.move_to(np.array([eq_orig[0][1].get_center()[0], 1.9, 0]))
            down_arrow = Arrow(sol.get_bottom(), eq_orig[0][1].get_top(), buff=0.1,
                               color=CHALK_GREEN, stroke_width=3)
            self.play(FadeIn(sol), Write(eq_orig), GrowArrow(down_arrow),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            sub1 = MathTex("3(5)+1", r"\;=\;", "16", font_size=44)
            align_equals(sub1, BOARD_CX, 0.6)
            tgt = np.array([sub1[0][2].get_center()[0], 1.30, 0.0])
            mover5 = MathTex("5", font_size=30, color=CHALK_GREEN).move_to(
                sol[2].get_center())
            self.play(mover5.animate.move_to(tgt), FadeOut(down_arrow),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.play(TransformMatchingTex(eq_orig, sub1), FadeOut(mover5),
                      Flash(sub1[0], color=CHALK_GREEN, flash_radius=0.5),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["success"], gain=-11)

            sub2 = MathTex("15+1", r"\;=\;", "16", font_size=44)
            align_equals(sub2, BOARD_CX, 0.6)
            self.play(TransformMatchingTex(sub1, sub2),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            sub3 = MathTex("16", r"\;=\;", "16", font_size=48)
            align_equals(sub3, BOARD_CX, 0.6)
            self.play(TransformMatchingTex(sub2, sub3),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-12)

            ck = tick_beside(sub3, CHALK_GREEN, 0.44, 0.4)
            ok = board_text("LHS = RHS", 20, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -0.7, 0]))
            self.play(Create(ck), FadeIn(ok),
                      Flash(sub3, color=CHALK_GREEN, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 7: The solving routine ---------------------------------------
    def bullet_row(self, n: int, items: list, color: str) -> VGroup:
        badge = Circle(radius=0.2, stroke_color=color, stroke_width=2,
                       fill_color=color, fill_opacity=0.18)
        num = board_text(str(n), 18, color, "BOLD").move_to(badge.get_center())
        blocks = [board_text(it, 20, CHALK_WHITE) if isinstance(it, str) else it
                  for it in items]
        text_block = VGroup(*blocks).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        return VGroup(VGroup(badge, num), text_block).arrange(RIGHT, buff=0.3)

    def beat7_routine(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("The Solving Routine", 28, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, BOARD_TOP - 0.5, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            r1 = self.bullet_row(1, [
                "Identify what is attached to x:",
                MathTex(r"3x+1=16 \quad\Rightarrow\quad \times 3,\; +1", font_size=24),
            ], CHALK_CYAN)
            r2 = self.bullet_row(2, [
                "Undo in reverse order:",
                MathTex(r"+1 \rightarrow -1 \qquad \times 3 \rightarrow \div 3",
                        font_size=24),
            ], CHALK_GREEN)
            r3 = self.bullet_row(3, [
                "Isolate:", MathTex(r"x = 5", font_size=26, color=CHALK_GREEN),
            ], CHALK_YELLOW)
            r4 = self.bullet_row(4, [
                "Check:", MathTex(r"3(5)+1 = 16", font_size=24),
            ], CHALK_PINK)
            rows = VGroup(r1, r2, r3, r4).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
            rows.move_to(np.array([BOARD_CX, BOARD_CY + 0.1, 0]))
            rows.shift(RIGHT * (BOARD_CX - rows.get_center()[0]))

            self.play(FadeIn(r1, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(r2, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            self.play(FadeIn(r3, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(r4, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            strip = board_text("Identify  ->  Undo  ->  Isolate  ->  Check",
                               20, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -2.1, 0]))
            self.play(FadeIn(strip), Circumscribe(strip, color=CHALK_YELLOW,
                                                  stroke_width=3),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 8: Application: words -> equation ----------------------------
    def beat8_application(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("From Words to an Equation", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, BOARD_TOP - 0.45, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.4))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            words = VGroup(
                board_text("Four times a number,", 19, CHALK_WHITE),
                board_text("reduced by five,", 19, CHALK_WHITE),
                board_text("equals nineteen.", 19, CHALK_WHITE),
            ).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
            words.move_to(np.array([WORDS_CX, 0.2, 0]))
            self.play(FadeIn(words, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.35))

            e1 = MathTex("4x-5", r"\;=\;", "19", font_size=38).move_to(
                np.array([EQ_COL_CX, 0.55, 0]))
            e1[0][1].set_color(CHALK_CYAN)
            self.play(Write(e1), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            e2 = MathTex("4x", r"\;=\;", "19+5", font_size=38).move_to(
                np.array([EQ_COL_CX, -0.35, 0]))
            e2[0][1].set_color(CHALK_CYAN)
            self.play(Indicate(words[1], color=CHALK_PINK, scale_factor=1.15),
                      TransformMatchingTex(e1, e2),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            e3 = MathTex("4x", r"\;=\;", "24", font_size=38).move_to(
                np.array([EQ_COL_CX, -0.35, 0]))
            e3[0][1].set_color(CHALK_CYAN)
            self.play(TransformMatchingTex(e2, e3),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            e4 = MathTex("x", r"\;=\;", r"\frac{24}{4}", font_size=38).move_to(
                np.array([EQ_COL_CX, -1.25, 0]))
            e4[0].set_color(CHALK_CYAN)
            self.play(TransformMatchingTex(e3, e4),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            e5 = MathTex("x", r"\;=\;", "6", font_size=42, color=CHALK_GREEN).move_to(
                np.array([EQ_COL_CX, -1.25, 0]))
            self.play(TransformMatchingTex(e4, e5),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.5))
            ans_box = SurroundingRectangle(e5, color=CHALK_GREEN, buff=0.18,
                                           corner_radius=0.1, stroke_width=2.5)
            result = board_text("The number is 6.", 18, CHALK_GREEN, "BOLD").move_to(
                np.array([WORDS_CX, -1.35, 0]))
            self.play(Create(ans_box), FadeIn(result),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 9: Student challenge -----------------------------------------
    def beat9_challenge(self) -> None:
        box_y = 0.8
        with self.voiceover(text=NARRATION["scene9_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", 30, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.5, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            eq_c = MathTex("7x-9", r"\;=\;", "26", font_size=52)
            align_equals(eq_c, BOARD_CX, box_y)
            eq_c[0][1].set_color(CHALK_CYAN)
            self.play(Write(eq_c), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            undo = board_text("Isolate x", 22, CHALK_WHITE).move_to(
                np.array([BOARD_CX, -0.1, 0]))
            self.play(FadeIn(undo), run_time=rt(tracker.time_until_bookmark("b2") * 0.4))
            first = board_text("What should you undo first?", 18, CHALK_YELLOW,
                               "BOLD").move_to(np.array([BOARD_CX, -0.8, 0]))
            self.play(FadeIn(first), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            pause = board_text("Pause and try it", 20, CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX, -1.5, 0]))
            self.play(FadeIn(pause), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.challenge_q = VGroup(heading, eq_c, undo, first, pause)
            self._capture_srt(tracker)

        play_challenge_countdown(self, seconds=10, sfx=self.sfx)

        with self.voiceover(text=NARRATION["scene9_reveal"]) as tracker:
            eq_c = self.challenge_q[1]
            self.play(FadeOut(self.challenge_q[3]), FadeOut(self.challenge_q[4]),
                      run_time=0.3)

            box9 = SurroundingRectangle(eq_c[0][2:4], color=CHALK_AMBER, buff=0.1,
                                        corner_radius=0.08, stroke_width=3)
            strip1 = board_text("Across '=': - becomes +", 14, CHALK_YELLOW,
                                "BOLD").move_to(np.array([BOARD_CX, 2.15, 0]))
            self.play(Create(box9), FadeIn(strip1),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.5))
            eq_c2 = MathTex("7x", r"\;=\;", "26+9", font_size=52)
            align_equals(eq_c2, BOARD_CX, box_y)
            eq_c2[0][1].set_color(CHALK_CYAN)
            self.play(TransformMatchingTex(eq_c, eq_c2), FadeOut(box9),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["click"], gain=-15)

            eq_c3 = MathTex("7x", r"\;=\;", "35", font_size=52)
            align_equals(eq_c3, BOARD_CX, box_y)
            eq_c3[0][1].set_color(CHALK_CYAN)
            self.play(TransformMatchingTex(eq_c2, eq_c3),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.35))
            box7 = SurroundingRectangle(eq_c3[0], color=CHALK_AMBER, buff=0.1,
                                        corner_radius=0.08, stroke_width=3)
            eq_c4 = MathTex("x", r"\;=\;", r"\frac{35}{7}", font_size=52)
            align_equals(eq_c4, BOARD_CX, box_y)
            eq_c4[0].set_color(CHALK_CYAN)
            self.play(Create(box7), run_time=rt(tracker.time_until_bookmark("b1") * 0.3))
            self.play(TransformMatchingTex(eq_c3, eq_c4), FadeOut(box7),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            eq_c5 = MathTex("x", r"\;=\;", "5", font_size=56, color=CHALK_GREEN)
            align_equals(eq_c5, BOARD_CX, box_y)
            self.play(TransformMatchingTex(eq_c4, eq_c5),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            ans_box = SurroundingRectangle(eq_c5, color=CHALK_GREEN, buff=0.22,
                                           corner_radius=0.1, stroke_width=3)
            ck = tick_beside(eq_c5, CHALK_GREEN, 0.42, 0.45)
            well = board_text("Well done!", 20, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -0.85, 0]))
            self.play(Create(ans_box), Create(ck), FadeIn(well),
                      Flash(eq_c5, color=CHALK_GREEN, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-12)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 10: SUMMARY --------------------------------------------------
    def summary_row(self, n: int, label: str, math_tex: str, color: str) -> VGroup:
        badge = Circle(radius=0.2, stroke_color=color, stroke_width=2,
                       fill_color=color, fill_opacity=0.18)
        num = board_text(str(n), 18, color, "BOLD").move_to(badge.get_center())
        return VGroup(VGroup(badge, num),
                      board_text(label, 19, CHALK_WHITE),
                      MathTex(math_tex, font_size=23)).arrange(RIGHT, buff=0.3)

    def beat10_recap(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("Summary", 32, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.5, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.4))

            # the whole journey in two compact rows: forward, then backward
            fwd = VGroup(
                board_text("x", 20, CHALK_CYAN, "BOLD"),
                MathTex(r"\times 3", font_size=22, color=CHALK_CYAN),
                MathTex("+1", font_size=22, color=CHALK_PINK),
                MathTex("16", font_size=22, color=CHALK_GREEN),
            ).arrange(RIGHT, buff=0.45).move_to(np.array([BOARD_CX, 2.05, 0]))
            fwd_arrows = VGroup(*[
                Arrow(fwd[i].get_right(), fwd[i + 1].get_left(), buff=0.1,
                      color=CHALK_WHITE, stroke_width=2.2) for i in range(3)])
            back = VGroup(
                MathTex("16", font_size=22, color=CHALK_GREEN),
                MathTex("-1", font_size=22, color=CHALK_GREEN),
                MathTex(r"\div 3", font_size=22, color=CHALK_YELLOW),
                MathTex("5", font_size=22, color=CHALK_GREEN),
            ).arrange(RIGHT, buff=0.45).move_to(np.array([BOARD_CX, 1.4, 0]))
            back_arrows = VGroup(*[
                Arrow(back[i + 1].get_left(), back[i].get_right(), buff=0.1,
                      color=CHALK_GREEN, stroke_width=2.2) for i in range(3)])
            self.play(FadeIn(fwd), FadeIn(fwd_arrows), FadeIn(back),
                      FadeIn(back_arrows),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            r1 = self.summary_row(1, "Identify what is done to x:",
                                  r"\times 3,\; +1", CHALK_CYAN)
            r2 = self.summary_row(2, "Undo in reverse order:",
                                  r"+1 \rightarrow -1, \quad \times 3 \rightarrow \div 3",
                                  CHALK_GREEN)
            r3 = self.summary_row(3, "Isolate, then check:",
                                  r"x = 5, \quad 3(5)+1 = 16", CHALK_PINK)
            rows = VGroup(r1, r2, r3).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
            rows.move_to(np.array([BOARD_CX, 0.15, 0]))
            rows.shift(RIGHT * (BOARD_CX - rows.get_center()[0]))

            self.play(FadeIn(r1, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(r2, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(r3, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.play(Indicate(r3, color=CHALK_PINK, scale_factor=1.05),
                      run_time=rt(tracker.time_until_bookmark("b4")))

            # the takeaway is the last line OF the summary ...
            takeaway = board_text("Undo in reverse. Isolate the unknown.",
                                  22, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.75, 0]))
            self.play(FadeIn(takeaway, shift=UP * 0.1),
                      Flash(takeaway, color=CHALK_YELLOW, flash_radius=0.9),
                      run_time=rt(tracker.time_until_bookmark("b5") * 0.25))
            self.add_sound(self.sfx["success"], gain=-11)

            summary = VGroup(heading, fwd, fwd_arrows, back, back_arrows, rows,
                             takeaway)
            self.play(FadeOut(summary),
                      run_time=rt(tracker.time_until_bookmark("b5") * 0.3))

            # ... so after the summary only the Thank-You template is left.
            thanks = board_text("Thank You for Watching!", 42, CHALK_WHITE, "BOLD")
            thanks2 = board_text("See you in the next lesson :)", 26, CHALK_CYAN)
            thanks_group = VGroup(thanks, thanks2).arrange(DOWN, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.2, 0]))
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

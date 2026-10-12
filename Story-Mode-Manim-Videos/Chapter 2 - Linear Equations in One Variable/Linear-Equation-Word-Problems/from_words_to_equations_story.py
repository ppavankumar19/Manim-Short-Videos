"""
Linear Equation Word Problems — Turn the Story into Algebra
Story-mode chalkboard lesson (Telangana Class 8 Maths, Chapter 2:
Linear Equations in One Variable, word problems).

Core idea: a real problem arrives as WORDS. Before anything can be solved, the
information has to be translated -- choose the unknown, express the other
quantities with it, turn the given condition into one equation, solve it, and
finally answer the original question. Sentence fragments physically become
algebra on screen; no equation ever appears ready-made.

Production pipeline (mirrors the rest of the Story-Mode series):
  - shared assets/background2.png chalkboard + student/teacher cutouts +
    dhimantAI (top-left) and Mathematics (top-right) corner badges.
  - VoiceoverScene + speech service; narration written as natural prose.
  - synced_voice.install_synced_voiceover() re-times every word against the
    real audio.
  - real per-line SRT export (carry-safe timestamps).
  - sound effects from sound_effects.py, chalk-styled Text/MathTex.
  - story_common.play_challenge_countdown() for the "YOUR TURN" clock.

Title + 10 beats:
  0. Title card -- the pipeline in miniature.
  1. Where Is the Equation? -- park + two sentence fragments, no equation yet.
  2. The Word-Problem Machine -- UNKNOWN -> EXPRESS -> RELATION -> EQUATION ->
     ANSWER, then the memory strip.
  3. Translate the Relationship -- five phrases becoming algebra.
  4. Build the Equation -- two number cards assembled into x+(x+5)=29.
  5. Solve, Then Return to the Story -- x=12, then 12 and 17, checked.
  6. Age Problems -- bars, +6 years, (x+6)+(4x+6)=62 -> 10 and 40.
  7. Real-World: The Park -- 2[(x+17)+x]=178 -> breadth 36 m, length 53 m.
  8. The Word-Problem Routine -- choose, express, relate, solve, answer.
  9. Student Challenge -- consecutive odd numbers, 56 -> 27 and 29.
 10. Summary + the Thank-You template.
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
    ImageMobject, MathTex, VGroup, Line, Circle, Ellipse, Rectangle,
    RoundedRectangle, Triangle, Arrow, DoubleArrow, Text, Write, FadeIn,
    FadeOut, Create, ReplacementTransform, TransformMatchingTex,
    TransformFromCopy, GrowArrow, Indicate, Flash, Circumscribe,
    SurroundingRectangle, DashedLine, config,
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

# measured chalkboard safe bounds (shared across the series)
BOARD_LEFT = -4.6
BOARD_RIGHT = 5.6
BOARD_TOP = 3.3
BOARD_BOTTOM = -2.9
BOARD_CX = (BOARD_LEFT + BOARD_RIGHT) / 2   # 0.5
BOARD_CY = (BOARD_TOP + BOARD_BOTTOM) / 2   # 0.2

EQ_Y = 0.55        # main equation line
HEAD_Y = BOARD_TOP - 0.45
WORDS_CX = BOARD_CX - 2.35   # the word column of the two-column layout
ALG_CX = BOARD_CX + 2.35     # the algebra column


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


def drop_shadow(mobj: VGroup, dx: float = 0.045, dy: float = -0.05,
                opacity: float = 0.3) -> VGroup:
    shadow = mobj.copy()
    shadow.set_fill(BLACK, opacity=opacity)
    shadow.set_stroke(width=0)
    shadow.shift(np.array([dx, dy, 0]))
    return VGroup(shadow, mobj)


# ------------------------------------------------------- card / chip kit ----
def card_box(width: float, height: float, color: str,
             fill: str = "#16202B", radius: float = 0.1) -> RoundedRectangle:
    return RoundedRectangle(corner_radius=radius, width=width, height=height,
                            stroke_color=color, stroke_width=2,
                            fill_color=fill, fill_opacity=0.9)


def text_chip(s: str, color: str, size: int = 17, pad_w: float = 0.34,
              pad_h: float = 0.22, fill: str = "#16202B") -> VGroup:
    """A small rounded label chip around a piece of text."""
    lbl = board_text(s, size, color, "BOLD")
    box = RoundedRectangle(corner_radius=0.08,
                           width=lbl.width + pad_w, height=lbl.height + pad_h,
                           stroke_color=color, stroke_width=1.8,
                           fill_color=fill, fill_opacity=0.85)
    lbl.move_to(box.get_center())
    return VGroup(box, lbl)


def math_chip(tex: str, color: str, size: int = 24, pad_w: float = 0.36,
              pad_h: float = 0.26, fill: str = "#16202B") -> VGroup:
    lbl = MathTex(tex, font_size=size, color=color)
    box = RoundedRectangle(corner_radius=0.08,
                           width=lbl.width + pad_w, height=lbl.height + pad_h,
                           stroke_color=color, stroke_width=1.8,
                           fill_color=fill, fill_opacity=0.85)
    lbl.move_to(box.get_center())
    return VGroup(box, lbl)


def step_card(n: int, title: str, example, color: str, width: float = 1.7,
              height: float = 1.8) -> VGroup:
    """One stage of the word-problem pipeline."""
    box = card_box(width, height, color)
    num = board_text(str(n), 16, color, "BOLD").move_to(
        box.get_top() + DOWN * 0.24)
    lbl = board_text(title, 14, CHALK_WHITE, "BOLD").move_to(
        box.get_center() + UP * 0.14)
    ex = (board_text(example, 12, color) if isinstance(example, str)
          else example)
    ex.move_to(box.get_center() + DOWN * 0.38)
    return VGroup(box, num, lbl, ex)


def phrase_row(phrase: str, expr: str, color: str, y: float) -> VGroup:
    """WORDS on the left -> ALGEBRA on the right, joined by an arrow."""
    lbl = board_text(phrase, 18, CHALK_WHITE)
    lbl.align_to(np.array([-0.75, 0, 0]), RIGHT).shift(UP * (y - lbl.get_center()[1]))
    ar = Arrow(np.array([-0.42, y, 0]), np.array([0.52, y, 0]), buff=0.02,
               color=color, stroke_width=2.4,
               max_tip_length_to_length_ratio=0.22, tip_length=0.15)
    ex = MathTex(expr, font_size=30, color=color)
    ex.align_to(np.array([0.75, 0, 0]), LEFT).shift(UP * (y - ex.get_center()[1]))
    return VGroup(lbl, ar, ex)


def summary_row(n: int, label: str, math_tex: str, color: str) -> VGroup:
    badge = Circle(radius=0.19, stroke_color=color, stroke_width=2,
                   fill_color=color, fill_opacity=0.18)
    num = board_text(str(n), 17, color, "BOLD").move_to(badge.get_center())
    return VGroup(VGroup(badge, num),
                  board_text(label, 18, CHALK_WHITE),
                  MathTex(math_tex, font_size=22)).arrange(RIGHT, buff=0.28)


# --------------------------------------------------------- park diagram -----
# Icon vocabulary shared with the rest of the series (the Anatomy video's
# park puzzle): proper little trees with layered foliage, a rippled pond and
# a scattered lawn, so the drawing reads as a real plot of land.
def tree_icon(pos: np.ndarray, scale: float = 1.0) -> VGroup:
    """A chalk tree anchored at its base: trunk + three-tone foliage."""
    trunk = Rectangle(width=0.09, height=0.34, fill_color="#5A3B1E",
                      fill_opacity=1, stroke_width=0).move_to(UP * 0.17)
    fol_low = Circle(0.24, fill_color="#2E7D46", fill_opacity=0.95,
                     stroke_color=CHALK_GREEN, stroke_width=1.5).move_to(UP * 0.46)
    fol_mid = Circle(0.18, fill_color="#3B9A5B", fill_opacity=0.95,
                     stroke_color=CHALK_GREEN, stroke_width=1.2).move_to(
        UP * 0.52 + RIGHT * 0.14)
    fol_top = Circle(0.12, fill_color="#4FB06C", fill_opacity=0.95,
                     stroke_color=CHALK_GREEN, stroke_width=1.0).move_to(
        UP * 0.62 + LEFT * 0.08)
    tree = VGroup(trunk, fol_low, fol_mid, fol_top)
    tree.scale(scale).move_to(np.array([pos[0], pos[1] + 0.34 * scale / 2, 0]))
    return tree


def grass_tuft(pos: np.ndarray, color: str = CHALK_GREEN,
               height: float = 0.13) -> VGroup:
    """A small chalk grass tuft: three short blades fanning from one point."""
    blades = VGroup(*[
        Line(ORIGIN, height * np.array([np.sin(a), np.cos(a), 0]),
             stroke_color=color, stroke_width=1.2)
        for a in (-0.5, 0.0, 0.5)
    ])
    return blades.move_to(pos)


def sparse_lawn(rect: Rectangle, blockers: tuple = (),
                 color: str = CHALK_GREEN, margin: float = 0.26,
                 spacing: float = 0.6) -> VGroup:
    """Grass texture scattered over the plot, avoiding the pond and trees."""
    cx, cy = rect.get_center()[0], rect.get_center()[1]
    half_w = rect.width / 2 - margin
    half_h = rect.height / 2 - margin
    cols = max(2, int(rect.width / spacing))
    rows = max(2, int(rect.height / spacing))
    tufts = VGroup()
    for c in np.linspace(cx - half_w, cx + half_w, cols):
        for r in np.linspace(cy - half_h, cy + half_h, rows):
            p = np.array([c, r, 0])
            if any(np.linalg.norm(p - b) < rad for b, rad in blockers):
                continue
            tufts.add(grass_tuft(p, color))
    return tufts


def pond_icon(pos: np.ndarray, scale: float = 1.0) -> VGroup:
    """A small chalk pond: water ellipse with a lighter inner ripple."""
    outer = Ellipse(width=0.62, height=0.38, stroke_color=CHALK_CYAN,
                    stroke_width=1.8, fill_color="#1E4F63",
                    fill_opacity=0.9).move_to(ORIGIN)
    inner = Ellipse(width=0.34, height=0.17, stroke_color=CHALK_CYAN,
                    stroke_width=1.1, fill_color="#2E82A0",
                    fill_opacity=0.7).move_to(ORIGIN)
    return VGroup(outer, inner).scale(scale).move_to(pos)


def park_diagram(width: float = 3.0, height: float = 1.85,
                 cx: float = 0.0, cy: float = 0.0) -> VGroup:
    """A real-looking park plot: bordered lawn, two trees, a pond, grass.

    The returned group carries `.plot` (the boundary rectangle) so callers can
    hang dimension arrows off it.
    """
    plot = Rectangle(width=width, height=height, stroke_color=CHALK_CYAN,
                     stroke_width=2.5, fill_color="#1E3B22", fill_opacity=0.62)
    plot.move_to(np.array([cx, cy, 0]))
    # a fenced border just outside the plot -- reads as a real park boundary
    fence = RoundedRectangle(corner_radius=0.05, width=width + 0.18,
                             height=height + 0.18, stroke_color=CHALK_GREEN,
                             stroke_width=1.6).move_to(plot.get_center())

    top = plot.get_top()[1] - 0.22
    tree1 = tree_icon(np.array([cx - width * 0.33, top, 0]), scale=0.8)
    tree2 = tree_icon(np.array([cx + width * 0.3, top, 0]), scale=0.72)
    pond_pos = np.array([cx - width * 0.1, cy - height * 0.2, 0])
    pond = pond_icon(pond_pos, scale=0.95)
    lawn = sparse_lawn(plot, blockers=(
        (pond_pos, 0.55),
        (np.array([cx - width * 0.33, top, 0]), 0.42),
        (np.array([cx + width * 0.3, top, 0]), 0.38),
    ))

    park = VGroup(plot, fence, lawn, pond, tree1, tree2)
    park.plot = plot
    return park


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "Today we turn stories into equations.<bookmark mark='b0'/> Real problems "
        "arrive as words, and our job is to build the mathematics hidden inside "
        "them.<bookmark mark='b1'/> Let's start with a real problem!"
        "<bookmark mark='b2'/>"
    ),
    "scene1": (
        "Here is a real problem.<bookmark mark='b0'/> The length of a rectangular "
        "park is seventeen metres more than its breadth, and its perimeter is one "
        "hundred and seventy eight metres.<bookmark mark='b1'/> Look at what we "
        "have: words, and not a single equation.<bookmark mark='b2'/> The "
        "relationship is hidden inside the sentence.<bookmark mark='b3'/> Where is "
        "the equation hiding?<bookmark mark='b4'/>"
    ),
    "scene2": (
        "So how do we pull an equation out of a story?<bookmark mark='b0'/> First "
        "we ask what we do not know, and we give that unknown a name, x."
        "<bookmark mark='b1'/> Next, we express every other quantity using x."
        "<bookmark mark='b2'/> Then we translate the given relationship into one "
        "equation.<bookmark mark='b3'/> After that we solve it, and finally we "
        "return to the story with the answer.<bookmark mark='b4'/> That is the "
        "whole method: choose, express, relate, solve, and answer."
        "<bookmark mark='b5'/>"
    ),
    "scene3": (
        "Let's practise the translation itself.<bookmark mark='b0'/> Five more than "
        "x becomes x plus five.<bookmark mark='b1'/> Four times x becomes four x."
        "<bookmark mark='b2'/> Six years later turns x into x plus six."
        "<bookmark mark='b3'/> The next odd number after x is x plus two."
        "<bookmark mark='b4'/> And the phrase their sum is twenty nine becomes "
        "equals twenty nine.<bookmark mark='b5'/> Read the relationship, not just "
        "the numbers.<bookmark mark='b6'/>"
    ),
    "scene4": (
        "Now let's build one equation together.<bookmark mark='b0'/> The sum of two "
        "numbers is twenty nine, and one number exceeds the other by five."
        "<bookmark mark='b1'/> Which quantity should be x?<bookmark mark='b2'/> Let "
        "the smaller number be x, so the bigger number must be x plus five."
        "<bookmark mark='b3'/> Their sum is twenty nine, so x plus x plus five "
        "equals twenty nine.<bookmark mark='b4'/> The story has now become algebra."
        "<bookmark mark='b5'/>"
    ),
    "scene5": (
        "Solving it is quick now.<bookmark mark='b0'/> x plus x plus five is two x "
        "plus five, so two x equals twenty four.<bookmark mark='b1'/> Dividing both "
        "sides by two gives x equals twelve.<bookmark mark='b2'/> But the question "
        "asked for two numbers, not just x.<bookmark mark='b3'/> The smaller number "
        "is twelve, and the bigger number is twelve plus five, which is seventeen."
        "<bookmark mark='b4'/> Let's check: twelve plus seventeen is twenty nine, "
        "exactly as the story said.<bookmark mark='b5'/> So the two numbers are "
        "twelve and seventeen.<bookmark mark='b6'/>"
    ),
    "scene6": (
        "The same translation works for ages.<bookmark mark='b0'/> Let Vijaya's "
        "present age be x.<bookmark mark='b1'/> Her mother is four times as old, so "
        "her age is four x.<bookmark mark='b2'/> After six years, both ages grow by "
        "six: x plus six, and four x plus six.<bookmark mark='b3'/> Their sum is "
        "then sixty two, so x plus six plus four x plus six equals sixty two."
        "<bookmark mark='b4'/> That simplifies to five x plus twelve equals sixty "
        "two, so x equals ten.<bookmark mark='b5'/> Vijaya is ten years old, and "
        "her mother is forty.<bookmark mark='b6'/>"
    ),
    "scene7": (
        "Back to the park.<bookmark mark='b0'/> We do not know the breadth, so let "
        "the breadth be x.<bookmark mark='b1'/> The length is seventeen metres more, "
        "so the length is x plus seventeen.<bookmark mark='b2'/> The perimeter "
        "formula says that twice the sum of the length and the breadth is the "
        "perimeter.<bookmark mark='b3'/> Substituting the story into the formula "
        "gives two times, x plus seventeen plus x, equals one hundred and seventy "
        "eight.<bookmark mark='b4'/> That becomes four x plus thirty four equals one "
        "hundred and seventy eight, so four x equals one hundred and forty four, and "
        "x equals thirty six.<bookmark mark='b5'/> The breadth is thirty six metres, "
        "and the length is fifty three metres.<bookmark mark='b6'/> Let's check the "
        "perimeter: two times thirty six plus fifty three is one hundred and seventy "
        "eight metres exactly.<bookmark mark='b7'/>"
    ),
    "scene8": (
        "Every word problem follows the same routine.<bookmark mark='b0'/> First, "
        "choose the unknown.<bookmark mark='b1'/> Then express the other quantities "
        "in terms of it.<bookmark mark='b2'/> Next, relate them with the given "
        "condition, and write one equation.<bookmark mark='b3'/> Solve that "
        "equation.<bookmark mark='b4'/> And finally, interpret the answer back in "
        "the story.<bookmark mark='b5'/> Choose, express, relate, solve, and answer."
        "<bookmark mark='b6'/>"
    ),
    "scene9_setup": (
        "Your turn!<bookmark mark='b0'/> The sum of two consecutive odd numbers is "
        "fifty six.<bookmark mark='b1'/> If the first odd number is x, what is the "
        "next odd number?<bookmark mark='b2'/> Pause the video, and try it yourself."
        "<bookmark mark='b3'/>"
    ),
    "scene9_reveal": (
        "Consecutive odd numbers differ by two, so the next one is x plus two."
        "<bookmark mark='b0'/> Their sum is fifty six, so x plus x plus two equals "
        "fifty six, which gives two x equals fifty four.<bookmark mark='b1'/> So x "
        "equals twenty seven, and the numbers are twenty seven and twenty nine."
        "<bookmark mark='b2'/> Well done — you translated the story before solving "
        "it.<bookmark mark='b3'/>"
    ),
    "scene10": (
        "Let's summarise.<bookmark mark='b0'/> Read the story, and find what is "
        "unknown, then name it x.<bookmark mark='b1'/> Express every other quantity "
        "using x.<bookmark mark='b2'/> Translate the given condition into one "
        "equation.<bookmark mark='b3'/> Solve it, and then return to the story, to "
        "answer the actual question and check it.<bookmark mark='b4'/> Do not solve "
        "the words — translate them first. Translate first, solve second. Thank you "
        "so much for watching, and I will see you in the next lesson!"
        "<bookmark mark='b5'/>"
    ),
}


class FromWordsToEquationsStory(VoiceoverScene):
    """Story-mode chalkboard lesson: word problems into equations."""

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
        out_dir = _HERE / "media" / "videos" / "from_words_to_equations_story"
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
        self.beat1_where()
        self.beat2_machine()
        self.beat3_translate()
        self.beat4_build()
        self.beat5_solve()
        self.beat6_ages()
        self.beat7_park()
        self.beat8_routine()
        self.beat9_challenge()
        self.beat10_summary()

        self._write_real_srt()

    # ================================================================ beats ==

    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Linear Equation Word Problems", 36, CHALK_WHITE,
                               "BOLD").move_to(np.array([BOARD_CX, BOARD_CY + 1.6, 0]))
            self.play(Write(title), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            sub = board_text("Turn the story into algebra", 21, CHALK_YELLOW,
                             "BOLD").move_to(np.array([BOARD_CX, BOARD_CY + 0.9, 0]))
            self.play(Write(sub), run_time=rt(tracker.time_until_bookmark("b1") * 0.4))

            chips = VGroup(
                text_chip("WORDS", CHALK_WHITE, 15),
                text_chip("CHOOSE x", CHALK_CYAN, 15),
                text_chip("EXPRESS", CHALK_GREEN, 15),
                text_chip("EQUATION", CHALK_AMBER, 15),
                text_chip("ANSWER", CHALK_PINK, 15),
            ).arrange(RIGHT, buff=0.18).move_to(np.array([BOARD_CX, -0.55, 0]))
            arrows = VGroup(*[
                Arrow(chips[i].get_right(), chips[i + 1].get_left(), buff=0.02,
                      color=CHALK_WHITE, stroke_width=2.2,
                      max_tip_length_to_length_ratio=0.3, tip_length=0.1)
                for i in range(4)
            ])
            question = board_text("Where is the equation hiding?", 20,
                                  CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, -1.85, 0]))
            self.play(FadeIn(chips, shift=DOWN * 0.1), FadeIn(arrows),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(FadeIn(question), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["swipe"], gain=-15)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 1: where is the equation? ------------------------------------
    def beat1_where(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("A Real Problem", 24, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))

            park = park_diagram(width=2.6, height=1.75, cx=-3.05, cy=0.6)
            # both dimension arrows sit just outside the plot, and each label
            # sits outside its own arrow -- nothing crosses the arrow line
            b_arrow = DoubleArrow(park.plot.get_left(), park.plot.get_right(),
                                  buff=0, color=CHALK_CYAN, stroke_width=2.2,
                                  max_tip_length_to_length_ratio=0.12,
                                  tip_length=0.12).next_to(park.plot, DOWN, buff=0.12)
            b_lbl = VGroup(MathTex("?", font_size=24, color=CHALK_CYAN),
                           board_text("breadth", 14, CHALK_CYAN)
                           ).arrange(DOWN, buff=0.04).next_to(b_arrow, DOWN, buff=0.1)
            l_arrow = DoubleArrow(park.plot.get_bottom(), park.plot.get_top(),
                                  buff=0, color=CHALK_GREEN, stroke_width=2.2,
                                  max_tip_length_to_length_ratio=0.12,
                                  tip_length=0.12).next_to(park.plot, RIGHT, buff=0.12)
            l_lbl = board_text("length", 14, CHALK_GREEN).next_to(
                l_arrow, RIGHT, buff=0.12)

            f1 = VGroup(board_text("The length is", 15),
                        board_text("17 m more", 15, CHALK_YELLOW, "BOLD"),
                        board_text("than the breadth.", 15)).arrange(RIGHT, buff=0.16)
            f2 = VGroup(board_text("The perimeter is", 15),
                        board_text("178 m", 15, CHALK_YELLOW, "BOLD")
                        ).arrange(RIGHT, buff=0.16)
            frags = VGroup(f1, f2).arrange(DOWN, buff=0.42, aligned_edge=LEFT)
            frags.move_to(np.array([ALG_CX - 0.1, 0.85, 0]))

            tag = board_text("Real problems come as words.", 18, CHALK_WHITE)
            tag.move_to(np.array([BOARD_CX, -1.5, 0]))
            question = board_text("Where is the equation hiding?", 21,
                                  CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, -2.15, 0]))

            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))
            self.play(Create(park), GrowArrow(b_arrow), GrowArrow(l_arrow),
                      FadeIn(b_lbl), FadeIn(l_lbl),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(FadeIn(f1, shift=LEFT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.play(FadeIn(f2, shift=LEFT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(tag), run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            # a scale-Indicate would push the highlighted phrase into its
            # neighbours, so the key words only flash in place
            self.play(Indicate(f1[1], color=CHALK_YELLOW, scale_factor=1.0),
                      Flash(f1[1], color=CHALK_YELLOW, flash_radius=0.45),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            self.play(Indicate(f2[1], color=CHALK_YELLOW, scale_factor=1.0),
                      Flash(f2[1], color=CHALK_YELLOW, flash_radius=0.45),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(question), Flash(question, color=CHALK_PINK,
                                              flash_radius=0.8),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["swipe"], gain=-15)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 2: the word-problem machine ----------------------------------
    def beat2_machine(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("Story to Algebra", 26, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            c1 = step_card(1, "UNKNOWN", "let it be x", CHALK_CYAN)
            c2 = step_card(2, "EXPRESS", "x+5,  4x", CHALK_GREEN)
            c3 = step_card(3, "RELATION", "sum, perimeter", CHALK_AMBER)
            c4 = step_card(4, "EQUATION", "write ONE", CHALK_PINK)
            c5 = step_card(5, "ANSWER", "back to the story", CHALK_YELLOW)
            cards = VGroup(c1, c2, c3, c4, c5).arrange(RIGHT, buff=0.3).move_to(
                np.array([BOARD_CX, 0.45, 0]))
            cards.shift(RIGHT * (BOARD_CX - cards.get_center()[0]))
            arrows = VGroup(*[
                Arrow(cards[i].get_right(), cards[i + 1].get_left(), buff=0.02,
                      color=CHALK_WHITE, stroke_width=2.2,
                      max_tip_length_to_length_ratio=0.3, tip_length=0.11)
                for i in range(4)
            ])

            self.play(FadeIn(c1, shift=DOWN * 0.12),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["click"], gain=-15)
            for k, (card, mark) in enumerate(
                    [(c2, "b1"), (c3, "b2"), (c4, "b3"), (c5, "b4")], start=1):
                self.play(GrowArrow(arrows[k - 1]), FadeIn(card, shift=DOWN * 0.12),
                          run_time=rt(tracker.time_until_bookmark(mark)))
                self.add_sound(self.sfx["click"], gain=-15)

            strip = board_text("Choose  ->  Express  ->  Relate  ->  Solve  ->  Answer",
                               21, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.5, 0]))
            self.play(FadeIn(strip), Circumscribe(strip, color=CHALK_YELLOW,
                                                  stroke_width=3),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 3: translate the relationship --------------------------------
    def beat3_translate(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()

            heading = board_text("Translate the Relationship", 26, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            specs = [
                ("five more than x", "x+5", CHALK_CYAN, 1.35),
                ("four times x", "4x", CHALK_GREEN, 0.65),
                ("six years later", "x+6", CHALK_YELLOW, -0.05),
                ("the next odd number", "x+2", CHALK_AMBER, -0.75),
                ("their sum is 29", "=29", CHALK_PINK, -1.45),
            ]
            rows = VGroup(*[phrase_row(p, e, c, y) for p, e, c, y in specs])
            # WORDS + ALGEBRA together form one centred block on the board
            rows.shift(RIGHT * (BOARD_CX - rows.get_center()[0]))
            words_lbl = board_text("WORDS", 15, CHALK_WHITE, "BOLD").move_to(
                rows[0][0].get_center() + UP * 0.8)
            alg_lbl = board_text("ALGEBRA", 15, CHALK_CYAN, "BOLD").move_to(
                rows[0][2].get_center() + UP * 0.8)
            self.play(FadeIn(words_lbl), FadeIn(alg_lbl),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            marks = ["b1", "b2", "b3", "b4", "b5"]
            for row, mark in zip(rows, marks):
                self.play(FadeIn(row[0], shift=RIGHT * 0.1),
                          run_time=rt(tracker.time_until_bookmark(mark) * 0.35))
                self.play(GrowArrow(row[1]),
                          run_time=rt(tracker.time_until_bookmark(mark) * 0.25))
                self.play(TransformFromCopy(row[0], row[2]),
                          run_time=rt(tracker.time_until_bookmark(mark)))
                self.add_sound(self.sfx["click"], gain=-15)

            note = board_text("Read the relationship, not just the numbers.", 18,
                              CHALK_WHITE).move_to(np.array([BOARD_CX, -2.1, 0]))
            self.play(FadeIn(note), run_time=rt(tracker.time_until_bookmark("b6")))
            self.add_sound(self.sfx["ding"], gain=-13)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 4: build the equation ----------------------------------------
    def beat4_build(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()

            heading = board_text("Build the Equation", 26, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            story1 = VGroup(board_text("The sum of two numbers is ", 16),
                            board_text("29", 16, CHALK_YELLOW, "BOLD"),
                            board_text(".", 16)).arrange(RIGHT, buff=0.05)
            story2 = VGroup(board_text("One number exceeds the other by ", 16),
                            board_text("5", 16, CHALK_YELLOW, "BOLD"),
                            board_text(".", 16)).arrange(RIGHT, buff=0.05)
            story = VGroup(story1, story2).arrange(DOWN, buff=0.3,
                                                   aligned_edge=LEFT).move_to(
                np.array([BOARD_CX, 2.15, 0]))

            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.25))
            self.play(FadeIn(story, shift=DOWN * 0.1),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            small = VGroup(card_box(1.85, 1.15, CHALK_CYAN),
                           board_text("smaller number", 13, CHALK_CYAN, "BOLD"))
            small[1].move_to(small[0].get_top() + DOWN * 0.24)
            small.move_to(np.array([BOARD_CX - 2.05, 0.75, 0]))
            big = VGroup(card_box(1.85, 1.15, CHALK_GREEN),
                         board_text("bigger number", 13, CHALK_GREEN, "BOLD"))
            big[1].move_to(big[0].get_top() + DOWN * 0.24)
            big.move_to(np.array([BOARD_CX + 2.05, 0.75, 0]))
            q = board_text("Which quantity should be x?", 18, CHALK_PINK,
                           "BOLD").move_to(np.array([BOARD_CX, 1.55, 0]))

            self.play(FadeIn(small), FadeIn(big), FadeIn(q),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.4))
            x_in_small = MathTex("x", font_size=32, color=CHALK_CYAN).move_to(
                small[0].get_center() + DOWN * 0.22)
            self.play(FadeIn(x_in_small, scale=0.7),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(FadeOut(q), run_time=0.3)
            x_plus = MathTex("x+5", font_size=32, color=CHALK_GREEN).move_to(
                big[0].get_center() + DOWN * 0.22)
            self.play(FadeIn(x_plus, scale=0.7),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["pop"], gain=-13)

            eq_part = MathTex("x+(x+5)", font_size=42).move_to(
                np.array([BOARD_CX - 0.5, -0.75, 0]))
            self.play(TransformFromCopy(x_in_small, eq_part[0][0:1]),
                      TransformFromCopy(x_plus, eq_part[0][2:7]),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            sum_lbl = board_text("their sum", 15, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -0.2, 0]))
            self.play(FadeIn(sum_lbl), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            full = MathTex("x+(x+5)", r"\;=\;", "29", font_size=42)
            align_equals(full, BOARD_CX, -0.75)
            box = SurroundingRectangle(full, color=CHALK_GREEN, buff=0.2,
                                       corner_radius=0.1, stroke_width=3)
            self.play(TransformMatchingTex(eq_part, full),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.play(Create(box), Flash(full, color=CHALK_GREEN, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.4))
            self.add_sound(self.sfx["success"], gain=-11)

            done = board_text("The story has become algebra.", 19, CHALK_GREEN,
                              "BOLD").move_to(np.array([BOARD_CX, -1.85, 0]))
            self.play(FadeIn(done), run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["ding"], gain=-12)

            self.eq = full
            self.beat4_extras = VGroup(heading, story, small, big, x_in_small,
                                       x_plus, sum_lbl, box, done)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 5: solve, then return to the story ---------------------------
    def beat5_solve(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            self.reset_board()

            heading = board_text("Solve, Then Return to the Story", 24,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            eq1 = MathTex("x+(x+5)", r"\;=\;", "29", font_size=42)
            align_equals(eq1, BOARD_CX, 1.15)
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))
            self.play(Write(eq1), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            eq2 = MathTex("2x+5", r"\;=\;", "29", font_size=42)
            align_equals(eq2, BOARD_CX, 1.15)
            self.play(TransformMatchingTex(eq1, eq2),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            eq3 = MathTex("2x", r"\;=\;", "24", font_size=42)
            align_equals(eq3, BOARD_CX, 1.15)
            self.play(TransformMatchingTex(eq2, eq3),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            eq4 = MathTex("x", r"\;=\;", "12", font_size=46, color=CHALK_GREEN)
            align_equals(eq4, BOARD_CX, 1.15)
            self.play(TransformMatchingTex(eq3, eq4),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            ask = board_text("The question asked for two numbers, not just x.",
                             18, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, 0.25, 0]))
            self.play(FadeIn(ask), run_time=rt(tracker.time_until_bookmark("b3") * 0.4))

            small = math_chip("x = 12", CHALK_CYAN, 24)
            big = math_chip("x+5 = 17", CHALK_GREEN, 24)
            cards = VGroup(small, big).arrange(RIGHT, buff=0.6).move_to(
                np.array([BOARD_CX, -0.55, 0]))
            lbl_s = board_text("smaller", 14, CHALK_CYAN, "BOLD").next_to(
                small, UP, buff=0.1)
            lbl_b = board_text("bigger", 14, CHALK_GREEN, "BOLD").next_to(
                big, UP, buff=0.1)
            self.play(FadeIn(small, shift=UP * 0.1), FadeIn(big, shift=UP * 0.1),
                      FadeIn(lbl_s), FadeIn(lbl_b),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["pop"], gain=-13)

            chk = MathTex("12+17", r"\;=\;", "29", font_size=34)
            align_equals(chk, BOARD_CX - 0.35, -1.35)
            ck = tick_beside(chk, CHALK_GREEN, 0.34, 0.3)
            self.play(Write(chk), run_time=rt(tracker.time_until_bookmark("b4") * 0.5))
            self.play(Create(ck), Flash(chk, color=CHALK_GREEN, flash_radius=0.5),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)

            answer = MathTex("12", r"\text{ and }", "17", font_size=40,
                             color=CHALK_GREEN).move_to(np.array([BOARD_CX, -2.05, 0]))
            abox = SurroundingRectangle(answer, color=CHALK_GREEN, buff=0.16,
                                        corner_radius=0.1, stroke_width=3)
            self.play(FadeOut(ask), run_time=0.25)
            self.play(FadeIn(answer), Create(abox),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["ding"], gain=-12)
            self.play(Indicate(answer, color=CHALK_GREEN, scale_factor=1.08),
                      run_time=rt(tracker.time_until_bookmark("b6")))
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 6: age problems ----------------------------------------------
    def age_bar(self, label: str, expr: str, length: float, color: str,
                y: float, x0: float = -3.3) -> VGroup:
        lbl = board_text(label, 17, color, "BOLD")
        lbl.align_to(np.array([x0 - 0.25, 0, 0]), RIGHT).shift(
            UP * (y - lbl.get_center()[1]))
        bar = RoundedRectangle(corner_radius=0.06, width=length, height=0.42,
                               stroke_color=color, stroke_width=2,
                               fill_color=color, fill_opacity=0.22)
        bar.move_to(np.array([x0 + length / 2, y, 0]))
        ex = MathTex(expr, font_size=26, color=color)
        ex.next_to(bar, RIGHT, buff=0.22)
        return VGroup(lbl, bar, ex)

    def beat6_ages(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("Age Problems: Time Changes Every Age", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            vij = self.age_bar("Vijaya", "x", 0.95, CHALK_CYAN, 1.5)
            mot = self.age_bar("Mother", "4x", 2.6, CHALK_GREEN, 0.85)
            wait_lbl = board_text("present ages", 14, CHALK_WHITE).move_to(
                np.array([-3.55, 2.05, 0]))
            future_lbl = board_text("after 6 years", 14, CHALK_GREEN).move_to(
                np.array([2.6, 2.05, 0]))
            arrow = Arrow(np.array([0.35, 1.18, 0]), np.array([1.75, 1.18, 0]),
                          buff=0.04, color=CHALK_YELLOW, stroke_width=2.6)
            t6 = board_text("+6 years", 15, CHALK_YELLOW, "BOLD").move_to(
                np.array([1.05, 1.62, 0]))
            fut_v = MathTex("x+6", font_size=26, color=CHALK_CYAN).move_to(
                np.array([2.35, 1.5, 0]))
            fut_m = MathTex("4x+6", font_size=26, color=CHALK_GREEN).move_to(
                np.array([2.55, 0.85, 0]))
            # bars + timeline + future ages form one composition, centred
            ages_grp = VGroup(vij, mot, wait_lbl, future_lbl, arrow, t6, fut_v,
                              fut_m)
            ages_grp.shift(RIGHT * (BOARD_CX - ages_grp.get_center()[0]))

            self.play(FadeIn(vij, shift=RIGHT * 0.12),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.play(FadeIn(mot, shift=RIGHT * 0.12),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(FadeIn(wait_lbl), FadeIn(future_lbl), GrowArrow(arrow),
                      FadeIn(t6),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(FadeIn(fut_v, scale=0.8),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            self.play(FadeIn(fut_m, scale=0.8),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            cond = MathTex("(x+6)+(4x+6)", r"\;=\;", "62", font_size=36)
            align_equals(cond, BOARD_CX, -0.3)
            self.play(Write(cond), run_time=rt(tracker.time_until_bookmark("b4") * 0.6))
            cond2 = MathTex("5x+12", r"\;=\;", "62", font_size=36)
            align_equals(cond2, BOARD_CX, -0.3)
            self.play(TransformMatchingTex(cond, cond2),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["click"], gain=-15)

            solved = MathTex("x", r"\;=\;", "10", font_size=40, color=CHALK_GREEN)
            align_equals(solved, BOARD_CX, -0.3)
            self.play(TransformMatchingTex(cond2, solved),
                      run_time=rt(tracker.time_until_bookmark("b5") * 0.5))
            ages = VGroup(board_text("Vijaya = 10 years", 19, CHALK_CYAN, "BOLD"),
                          board_text("Mother = 40 years", 19, CHALK_GREEN, "BOLD")
                          ).arrange(RIGHT, buff=0.7).move_to(
                np.array([BOARD_CX, -1.3, 0]))
            self.play(FadeIn(ages, shift=UP * 0.1), Flash(ages, color=CHALK_AMBER,
                                                          flash_radius=0.8),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["success"], gain=-11)

            note = board_text("After 6 years: add 6 to BOTH ages", 16, CHALK_YELLOW,
                              "BOLD").move_to(np.array([BOARD_CX, -2.05, 0]))
            self.play(FadeIn(note), run_time=rt(tracker.time_until_bookmark("b6")))
            self.add_sound(self.sfx["ding"], gain=-12)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 7: the park ---------------------------------------------------
    def beat7_park(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("Real-World: The Park", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            park = park_diagram(width=2.9, height=1.75, cx=-2.6, cy=0.5)
            # arrows and their labels stay outside the plot and outside each
            # other; the final lengths replace the labels in place, so no chip
            # ever lands on top of a dimension arrow
            b_arrow = DoubleArrow(park.plot.get_left(), park.plot.get_right(),
                                  buff=0, color=CHALK_CYAN, stroke_width=2.2,
                                  max_tip_length_to_length_ratio=0.12,
                                  tip_length=0.12).next_to(park.plot, DOWN, buff=0.12)
            l_arrow = DoubleArrow(park.plot.get_bottom(), park.plot.get_top(),
                                  buff=0, color=CHALK_GREEN, stroke_width=2.2,
                                  max_tip_length_to_length_ratio=0.12,
                                  tip_length=0.12).next_to(park.plot, RIGHT, buff=0.12)
            lbl_b = VGroup(MathTex("x", font_size=26, color=CHALK_CYAN),
                           board_text("breadth", 14, CHALK_CYAN)
                           ).arrange(DOWN, buff=0.04).next_to(b_arrow, DOWN, buff=0.1)
            lbl_l = VGroup(MathTex("x+17", font_size=24, color=CHALK_GREEN),
                           board_text("length", 14, CHALK_GREEN)
                           ).arrange(DOWN, buff=0.04).next_to(l_arrow, RIGHT, buff=0.14)
            trace = SurroundingRectangle(park.plot, color=CHALK_YELLOW, buff=0.05,
                                         corner_radius=0.02, stroke_width=3)

            self.play(Create(park), run_time=rt(tracker.time_until_bookmark("b0")))
            self.play(GrowArrow(b_arrow), FadeIn(lbl_b),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.play(GrowArrow(l_arrow), FadeIn(lbl_l), Flash(lbl_l[0],
                                                              color=CHALK_GREEN,
                                                              flash_radius=0.4),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)

            formula = MathTex("P", r"\;=\;", r"2(l+b)", font_size=30).move_to(
                np.array([ALG_CX, 1.5, 0]))
            self.play(Create(trace), Write(formula),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            e1 = MathTex("2[(x+17)+x]", r"\;=\;", "178", font_size=28).move_to(
                np.array([ALG_CX, 0.8, 0]))
            self.play(Write(e1), run_time=rt(tracker.time_until_bookmark("b3") * 0.6))
            e2 = MathTex("4x+34", r"\;=\;", "178", font_size=28).move_to(
                np.array([ALG_CX, 0.8, 0]))
            self.play(TransformMatchingTex(e1, e2),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            e3 = MathTex("4x", r"\;=\;", "144", font_size=28).move_to(
                np.array([ALG_CX, 0.12, 0]))
            e4 = MathTex("x", r"\;=\;", "36", font_size=32,
                         color=CHALK_GREEN).move_to(np.array([ALG_CX, -0.56, 0]))
            self.play(FadeOut(formula), TransformMatchingTex(e2, e3),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.5))
            self.play(TransformMatchingTex(e3, e4),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.play(Indicate(trace, color=CHALK_YELLOW, scale_factor=1.02),
                      run_time=0.4)
            self.add_sound(self.sfx["success"], gain=-11)

            # the drawing now carries the real dimensions in the same places
            val_b = MathTex(r"36\,\text{m}", font_size=26, color=CHALK_CYAN).move_to(
                lbl_b[0])
            val_l = MathTex(r"53\,\text{m}", font_size=24, color=CHALK_GREEN).move_to(
                lbl_l[0])
            chk = MathTex("2(36+53)", r"\;=\;", "178", font_size=26).move_to(
                np.array([ALG_CX, -1.35, 0]))
            tick = tick_beside(chk, CHALK_GREEN, 0.3, 0.26)
            self.play(FadeOut(e4), FadeIn(chk), Create(tick),
                      Flash(chk, color=CHALK_GREEN, flash_radius=0.5),
                      run_time=rt(tracker.time_until_bookmark("b5") * 0.5))
            self.play(ReplacementTransform(lbl_b[0], val_b),
                      ReplacementTransform(lbl_l[0], val_l),
                      Flash(val_b, color=CHALK_CYAN, flash_radius=0.5),
                      Flash(val_l, color=CHALK_GREEN, flash_radius=0.5),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["ding"], gain=-12)

            note = board_text("Relationship + formula = equation", 17,
                              CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -2.3, 0]))
            self.play(FadeIn(note), run_time=rt(tracker.time_until_bookmark("b6") * 0.5))
            self.play(Indicate(lbl_l[1], color=CHALK_GREEN, scale_factor=1.0),
                      Indicate(lbl_b[1], color=CHALK_CYAN, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b6")))
            self.add_sound(self.sfx["ding"], gain=-12)

            # the perimeter check, then the dimensions confirmed on the drawing
            self.play(Indicate(chk, color=CHALK_GREEN, scale_factor=1.1),
                      Indicate(trace, color=CHALK_YELLOW, scale_factor=1.02),
                      run_time=rt(tracker.time_until_bookmark("b7") * 0.5))
            self.play(Circumscribe(lbl_b, color=CHALK_AMBER, stroke_width=3),
                      Circumscribe(lbl_l, color=CHALK_AMBER, stroke_width=3),
                      run_time=rt(tracker.time_until_bookmark("b7")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 8: the routine ------------------------------------------------
    def beat8_routine(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("The Word-Problem Routine", 26, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            cards = VGroup(
                step_card(1, "UNKNOWN", "name it x", CHALK_CYAN,
                          width=1.85, height=1.7),
                step_card(2, "EXPRESS", "x+5,  4x", CHALK_GREEN,
                          width=1.85, height=1.7),
                step_card(3, "RELATION", "sum = 29", CHALK_AMBER,
                          width=1.85, height=1.7),
                step_card(4, "SOLVE", "x = 12", CHALK_PINK,
                          width=1.85, height=1.7),
                step_card(5, "INTERPRET", "12 and 17", CHALK_YELLOW,
                          width=1.85, height=1.7),
            ).arrange(RIGHT, buff=0.14).move_to(np.array([BOARD_CX, 0.5, 0]))
            cards.shift(RIGHT * (BOARD_CX - cards.get_center()[0]))

            marks = ["b0", "b1", "b2", "b3", "b4"]
            for card, mark in zip(cards, marks):
                self.play(FadeIn(card, shift=DOWN * 0.12),
                          run_time=rt(tracker.time_until_bookmark(mark)))
                self.add_sound(self.sfx["click"], gain=-15)

            strip = board_text("Choose  ->  Express  ->  Relate  ->  Solve  ->  Answer",
                               20, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.45, 0]))
            self.play(FadeIn(strip), Circumscribe(strip, color=CHALK_YELLOW,
                                                  stroke_width=3),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["ding"], gain=-12)
            self.play(Indicate(cards[4], color=CHALK_YELLOW, scale_factor=1.04),
                      run_time=rt(tracker.time_until_bookmark("b6")))
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 9: student challenge -----------------------------------------
    def beat9_challenge(self) -> None:
        with self.voiceover(text=NARRATION["scene9_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", 30, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y - 0.05, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            problem = board_text("The sum of two consecutive odd numbers is 56.",
                                 20, CHALK_WHITE).move_to(
                np.array([BOARD_CX, 1.55, 0]))
            self.play(FadeIn(problem), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            c1 = VGroup(card_box(1.9, 1.0, CHALK_CYAN),
                        board_text("first odd number", 13, CHALK_CYAN, "BOLD"))
            c1[1].move_to(c1[0].get_top() + DOWN * 0.22)
            c1.move_to(np.array([BOARD_CX - 1.75, 0.5, 0]))
            c2 = VGroup(card_box(1.9, 1.0, CHALK_GREEN),
                        board_text("next odd number", 13, CHALK_GREEN, "BOLD"))
            c2[1].move_to(c2[0].get_top() + DOWN * 0.22)
            c2.move_to(np.array([BOARD_CX + 1.75, 0.5, 0]))
            c1_val = MathTex("x", font_size=30, color=CHALK_CYAN).move_to(
                c1[0].get_center() + DOWN * 0.2)
            c2_q = MathTex("?", font_size=30, color=CHALK_GREEN).move_to(
                c2[0].get_center() + DOWN * 0.2)
            self.play(FadeIn(c1), FadeIn(c2), FadeIn(c1_val), FadeIn(c2_q),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["pop"], gain=-13)

            pause = board_text("Pause and try it", 19, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -0.75, 0]))
            self.play(FadeIn(pause), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            self.challenge = VGroup(heading, problem, c1, c2, c1_val, c2_q, pause)
            self._capture_srt(tracker)

        play_challenge_countdown(self, seconds=6, sfx=self.sfx)

        with self.voiceover(text=NARRATION["scene9_reveal"]) as tracker:
            c2_q = self.challenge[5]
            c2 = self.challenge[3]
            reveal = MathTex("x+2", font_size=30, color=CHALK_GREEN).move_to(
                c2[0].get_center() + DOWN * 0.2)
            self.play(FadeOut(self.challenge[6]), ReplacementTransform(c2_q, reveal),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.5))
            hint = board_text("odd numbers differ by 2", 15, CHALK_GREEN,
                              "BOLD").move_to(np.array([BOARD_CX, -0.75, 0]))
            self.play(FadeIn(hint), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["click"], gain=-15)

            e1 = MathTex("x+(x+2)", r"\;=\;", "56", font_size=40).move_to(
                np.array([BOARD_CX, -1.4, 0]))
            e2 = MathTex("2x+2", r"\;=\;", "56", font_size=40).move_to(
                np.array([BOARD_CX, -1.4, 0]))
            e3 = MathTex("2x", r"\;=\;", "54", font_size=40).move_to(
                np.array([BOARD_CX, -1.4, 0]))
            self.play(Write(e1), run_time=rt(tracker.time_until_bookmark("b1") * 0.4))
            self.play(TransformMatchingTex(e1, e2),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.3))
            self.play(TransformMatchingTex(e2, e3),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            e4 = MathTex("x", r"\;=\;", "27", font_size=42, color=CHALK_GREEN).move_to(
                np.array([BOARD_CX, -1.4, 0]))
            self.play(TransformMatchingTex(e3, e4),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            ans = MathTex("27", r"\text{ and }", "29", font_size=36,
                          color=CHALK_GREEN).move_to(np.array([BOARD_CX, -2.05, 0]))
            abox = SurroundingRectangle(ans, color=CHALK_GREEN, buff=0.14,
                                        corner_radius=0.1, stroke_width=3)
            ck = tick_beside(ans, CHALK_GREEN, 0.32, 0.34)
            self.play(FadeOut(hint), FadeOut(e4), FadeIn(ans), Create(abox),
                      Create(ck), Flash(ans, color=CHALK_GREEN, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            well = board_text("Well done!", 19, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -0.75, 0]))
            self.play(FadeIn(well), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-12)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 10: summary ---------------------------------------------------
    def beat10_summary(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("Summary", 32, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y - 0.05, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.4))

            chain = MathTex(
                r"x \;\to\; x+5 \;\to\; x+(x+5)=29 \;\to\; 12,\;17",
                font_size=25, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, 2.3, 0]))
            self.play(Write(chain), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            r1 = summary_row(1, "Choose the unknown:", r"\text{let the smaller be } x",
                             CHALK_CYAN)
            r2 = summary_row(2, "Express the rest:", r"\text{bigger } = x+5",
                             CHALK_GREEN)
            r3 = summary_row(3, "Use the condition:", r"x+(x+5) = 29", CHALK_AMBER)
            r4 = summary_row(4, "Solve and return:", r"x = 12 \;\to\; 12,\;17",
                             CHALK_PINK)
            rows = VGroup(r1, r2, r3, r4).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            rows.move_to(np.array([BOARD_CX, 0.55, 0]))
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

            # the takeaway closes the summary ...
            take = board_text("Translate first. Solve second.", 24, CHALK_YELLOW,
                              "BOLD").move_to(np.array([BOARD_CX, -1.5, 0]))
            sub = board_text("Choose -> Express -> Relate -> Solve -> Answer", 17,
                             CHALK_CYAN).move_to(np.array([BOARD_CX, -2.05, 0]))
            self.play(FadeIn(take), Flash(take, color=CHALK_YELLOW, flash_radius=0.9),
                      FadeIn(sub),
                      run_time=rt(tracker.time_until_bookmark("b5") * 0.3))
            self.add_sound(self.sfx["success"], gain=-11)

            summary = VGroup(heading, chain, rows, take, sub)
            self.play(FadeOut(summary),
                      run_time=rt(tracker.time_until_bookmark("b5") * 0.3))

            # ... so after the summary only the Thank-You template is left.
            thanks = board_text("Thank You for Watching!", 40, CHALK_WHITE, "BOLD")
            thanks2 = board_text("See you in the next lesson :)", 25, CHALK_CYAN)
            thanks_group = VGroup(thanks, thanks2).arrange(DOWN, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY, 0]))
            self.play(Write(thanks),
                      run_time=rt(tracker.time_until_bookmark("b5") * 0.4))
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

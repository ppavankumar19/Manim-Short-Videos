"""
Whole Numbers — From Counting to Zero
Story-mode chalkboard lesson (Telangana Class 6 Maths, Chapter 2: Whole
Numbers, Sections 2.1-2.3).

Core idea: natural numbers are the counting numbers 1, 2, 3, ...; an empty
pencil box needs a number of its own, so zero joins the collection and we get
the whole numbers 0, 1, 2, 3, ....  On the number line the successor is one
step right and the predecessor one step left -- where it exists in the chosen
collection.  Zero has no predecessor in the whole numbers.

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
  1. When Counting Reaches Nothing -- 3 -> 2 -> 1 -> 0 pencil box.
  2. Natural Numbers Become Whole Numbers -- zero joins the collection.
  3. Spot the Difference -- the two collections aligned, N subset of W.
  4. Whole Numbers on the Number Line -- 0, 1, 2, ... with the arrow.
  5. Predecessor and Successor -- around 9: 8 <- 9 -> 10.
  6. The Special Case of Zero and One -- 1 - 1 = 0, and zero's boundary.
  7. Find the Neighbouring Numbers -- 12 | 13 | 14 and 998 | 999 | 1000.
  8. Real-World Application -- four pencils, one added, one removed.
  9. Student Challenge -- successor of 11 and predecessor of 5.
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
    ORIGIN, UP, DOWN, LEFT, RIGHT, PI, TAU, DEGREES, BLACK,
    ImageMobject, MathTex, VGroup, Line, DashedLine, Circle, Dot, Triangle,
    Rectangle, RoundedRectangle, Polygon, Arrow, DoubleArrow, Text,
    Write, FadeIn, FadeOut, Create, ReplacementTransform, TransformMatchingTex,
    TransformFromCopy, GrowArrow, Indicate, Flash, Circumscribe,
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

NAT_COLOR = CHALK_CYAN        # the natural-number collection
WHOLE_COLOR = CHALK_GREEN     # the whole-number collection
ZERO_COLOR = CHALK_YELLOW     # zero always stands out
LINE_COLOR = CHALK_CYAN       # the number line
SUCC_COLOR = CHALK_GREEN      # successor
PRED_COLOR = CHALK_PINK       # predecessor

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


# ------------------------------------------------------- story furniture ----
def pencil(color: str = CHALK_AMBER, scale: float = 1.0) -> VGroup:
    """One upright pencil: painted body, wooden tip, graphite point, metal
    ferrule and a rubber end.  Built from explicit polygons so the parts line
    up exactly (a scaled Triangle drifts when the body size changes)."""
    body = Rectangle(width=0.13, height=0.5, stroke_color=color,
                     stroke_width=1.2, fill_color=color, fill_opacity=0.32)
    shade = Rectangle(width=0.045, height=0.5, stroke_width=0,
                      fill_color=BLACK, fill_opacity=0.22)
    shade.align_to(body, LEFT)
    tip = Polygon(np.array([-0.065, 0.0, 0.0]), np.array([0.065, 0.0, 0.0]),
                  np.array([0.0, 0.13, 0.0]), stroke_color=CHALK_WHITE,
                  stroke_width=1.0, fill_color="#E8DCC0", fill_opacity=0.9)
    tip.next_to(body, UP, buff=0)
    point = Polygon(np.array([-0.021, 0.0, 0.0]), np.array([0.021, 0.0, 0.0]),
                    np.array([0.0, 0.055, 0.0]), stroke_width=0,
                    fill_color="#3A3A3A", fill_opacity=0.95)
    point.next_to(tip, UP, buff=-0.025)
    ferrule = Rectangle(width=0.13, height=0.055, stroke_width=0,
                        fill_color="#C9C9C9", fill_opacity=0.9)
    ferrule.next_to(body, DOWN, buff=0)
    eraser = RoundedRectangle(corner_radius=0.02, width=0.13, height=0.075,
                              stroke_width=0, fill_color=CHALK_PINK,
                              fill_opacity=0.9)
    eraser.next_to(ferrule, DOWN, buff=0)
    return VGroup(eraser, ferrule, body, shade, tip, point).scale(scale)


def pencil_box(n: int = 3, width: float = 2.1, height: float = 1.15,
               slots: int = 5, pos=np.array([BOARD_CX, 0.35, 0])) -> VGroup:
    """An open pencil box holding exactly `n` pencils, centred in the tray.

    A box of three pencils must *look* like a box of three, so the pencils on
    show are always spread evenly about the centre of the tray; `slots` extra
    pencils are pre-built for a later "add one", and `grp.centres(k)` returns the
    centred positions for `k` pencils so the remaining ones can slide across when
    one is taken away."""
    tray = RoundedRectangle(corner_radius=0.09, width=width, height=height,
                            stroke_color=CHALK_WHITE, stroke_width=2.4,
                            fill_color="#101820", fill_opacity=0.85)
    tray.move_to(pos)
    inner = RoundedRectangle(corner_radius=0.07, width=width - 0.24,
                             height=height - 0.36, stroke_color=CHALK_WHITE,
                             stroke_width=1.0, stroke_opacity=0.35,
                             fill_color="#1B2733", fill_opacity=0.6)
    inner.move_to(tray.get_center() + UP * 0.02)
    rim = Line(tray.get_corner(np.array([-1, 1, 0])) + RIGHT * 0.04 + DOWN * 0.16,
               tray.get_corner(np.array([1, 1, 0])) + LEFT * 0.04 + DOWN * 0.16,
               stroke_color=CHALK_WHITE, stroke_width=1.0, stroke_opacity=0.25)

    all_pencils = VGroup(*[pencil() for _ in range(slots)])

    def centres(k: int) -> list:
        """The k evenly spaced, tray-centred resting places for k pencils."""
        gap = 0.13 + 0.16
        span = (k - 1) * gap / 2.0
        base = inner.get_center() + UP * 0.04
        return [base + RIGHT * (i * gap - span) for i in range(k)]

    def place(k: int) -> list:
        """Move the first k pencils to those positions and return them."""
        spots = centres(k)
        for p, spot in zip(all_pencils[:k], spots):
            p.move_to(spot)
        return spots

    grp = VGroup(tray, inner, rim, all_pencils)
    grp.box = tray
    grp.inner = inner
    grp.rim = rim
    grp.pencils_all = list(all_pencils)
    grp.pencils = list(all_pencils)[:n]        # visible from the start
    grp.hidden = list(all_pencils)[n:]         # kept back for "add one"
    grp.centres = centres
    grp.place = place
    place(n)
    return grp


def number_card(value, color: str = CHALK_WHITE, size: float = 0.62,
                font: int = 26) -> VGroup:
    box = RoundedRectangle(corner_radius=0.06, width=size, height=size,
                           stroke_color=color, stroke_width=1.8,
                           fill_color="#16202B", fill_opacity=0.8)
    num = MathTex(str(value), font_size=font, color=color).move_to(box.get_center())
    grp = VGroup(box, num)
    grp.label = num
    return grp


def card_row(values, color: str = CHALK_WHITE, size: float = 0.62,
             buff: float = 0.18, font: int = 26) -> VGroup:
    return VGroup(*[number_card(v, color, size, font) for v in values]
                  ).arrange(RIGHT, buff=buff)


def num_line(values, *, x0: float = -3.9, step: float = 0.78, y: float = -0.5,
             color: str = LINE_COLOR, dot_color: str = LINE_COLOR,
             size: int = 24, pad: float = 0.5, arrow: bool = True) -> VGroup:
    """A number line with a dot and a label under every value given."""
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
    for v, x in zip(values, xs):
        d = Dot(np.array([x, y, 0.0]), radius=0.055, color=dot_color)
        lab = MathTex(str(v), font_size=size, color=CHALK_WHITE).next_to(
            d, DOWN, buff=0.13)
        dots[v], labels[v] = d, lab
        grp.add(d, lab)
    grp.dots, grp.labels = dots, labels
    grp.x = {v: x for v, x in zip(values, xs)}
    grp.y = y
    return grp


def step_arrow(x_from: float, x_to: float, y: float, color: str,
               lift: float = 0.42) -> Arrow:
    """A straight arrow above the line, from one number to its neighbour."""
    return Arrow(np.array([x_from, y + lift, 0.0]),
                 np.array([x_to, y + lift, 0.0]),
                 buff=0, color=color, stroke_width=2.6,
                 tip_length=0.16)


def summary_row(n: int, label: str, math_tex: str, color: str) -> VGroup:
    badge = Circle(radius=0.19, stroke_color=color, stroke_width=2,
                   fill_color=color, fill_opacity=0.18)
    num = board_text(str(n), 17, color, "BOLD").move_to(badge.get_center())
    return VGroup(VGroup(badge, num),
                  board_text(label, 17, CHALK_WHITE),
                  MathTex(math_tex, font_size=21)).arrange(RIGHT, buff=0.26)


def three_cards(pre, num, succ, y: float = 0.35, size: float = 1.5,
                buff: float = 0.45) -> VGroup:
    """[predecessor] [number] [successor] -- the reusable neighbour table."""
    def slot(value, color):
        box = RoundedRectangle(corner_radius=0.08, width=size, height=0.95,
                               stroke_color=color, stroke_width=2,
                               fill_color="#16202B", fill_opacity=0.8)
        txt = MathTex(str(value), font_size=32, color=color
                      ).move_to(box.get_center())
        grp = VGroup(box, txt)
        grp.txt = txt
        grp.box = box
        return grp

    left = slot(pre, PRED_COLOR)
    mid = slot(num, CHALK_WHITE)
    right = slot(succ, SUCC_COLOR)
    grp = VGroup(left, mid, right).arrange(RIGHT, buff=buff).move_to(
        np.array([BOARD_CX, y, 0]))
    grp.left, grp.mid, grp.right = left, mid, right
    return grp


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "Today we meet the whole numbers.<bookmark mark='b0'/> We will count "
        "objects, discover what zero really means, and learn about the "
        "predecessor and successor of a number.<bookmark mark='b1'/> Let's "
        "begin with a pencil box!<bookmark mark='b2'/>"
    ),
    "scene1": (
        "Look at this pencil box.<bookmark mark='b0'/> It has three pencils."
        "<bookmark mark='b1'/> One pencil is taken out, so two remain. Another "
        "pencil goes, and just one is left.<bookmark mark='b2'/> Now the last "
        "pencil is taken away, and the box is empty.<bookmark mark='b3'/> So "
        "what number tells us how many pencils are in the box now? Zero!"
        "<bookmark mark='b4'/>"
    ),
    "scene2": (
        "How do we count things? We say one, two, three, four, and we never "
        "stop.<bookmark mark='b0'/> These counting numbers have a name: they "
        "are the natural numbers.<bookmark mark='b1'/> We write them as the "
        "set one, two, three, four and so on.<bookmark mark='b2'/> But our "
        "empty box needed a number of its own.<bookmark mark='b3'/> So zero "
        "joins the collection, and we get zero, one, two, three, four and so "
        "on.<bookmark mark='b4'/> This larger family is called the whole "
        "numbers.<bookmark mark='b5'/> Whole numbers are the natural numbers "
        "together with zero.<bookmark mark='b6'/>"
    ),
    "scene3": (
        "Now let us place the two collections one above the other and compare "
        "them.<bookmark mark='b0'/> The numbers one, two, three, four and five "
        "match exactly.<bookmark mark='b1'/> There is only one new member, and "
        "that is zero.<bookmark mark='b2'/> So the smallest natural number is "
        "one, and the smallest whole number is zero.<bookmark mark='b3'/> And "
        "every natural number is also a whole number: N is a subset of W."
        "<bookmark mark='b4'/>"
    ),
    "scene4": (
        "Now let us put the whole numbers on a line.<bookmark mark='b0'/> This "
        "is the whole number line, and zero is its starting point.<bookmark "
        "mark='b1'/> Then come one, two, three, four, and we keep going: five, "
        "six, seven, eight, nine, ten, and on.<bookmark mark='b2'/> The arrow "
        "shows that the whole numbers never end. Every step to the right is "
        "one more, so the number on the right is always greater.<bookmark "
        "mark='b3'/> Remember, zero is the starting point of the whole number "
        "line.<bookmark mark='b4'/>"
    ),
    "scene5": (
        "Let us look closely at one number.<bookmark mark='b0'/> Take nine."
        "<bookmark mark='b1'/> One step to the right is ten, so ten is the "
        "successor of nine.<bookmark mark='b2'/> One step to the left is "
        "eight, so eight is the predecessor of nine.<bookmark mark='b3'/> The "
        "successor is the next number, and the predecessor is the previous "
        "number.<bookmark mark='b4'/> In general, the successor of a number n "
        "is n plus one, and its predecessor is n minus one.<bookmark mark='b5'/>"
    ),
    "scene6": (
        "Now a very important question. What comes before one?<bookmark "
        "mark='b0'/> In the whole numbers, one minus one is zero.<bookmark "
        "mark='b1'/> But remember, zero is not a natural number, it is a whole "
        "number.<bookmark mark='b2'/> So among the natural numbers, one has no "
        "predecessor. In the whole numbers, the predecessor of one is zero."
        "<bookmark mark='b3'/> And what is the predecessor of zero? There is "
        "no whole number before zero, so zero has no predecessor in the whole "
        "numbers.<bookmark mark='b4'/> But zero does have a successor: zero "
        "plus one is one.<bookmark mark='b5'/>"
    ),
    "scene7": (
        "Let us practise with bigger numbers.<bookmark mark='b0'/> Take "
        "thirteen. One less is twelve, and one more is fourteen.<bookmark "
        "mark='b1'/> Now take nine hundred and ninety nine.<bookmark "
        "mark='b2'/> One less is nine hundred and ninety eight, and one more "
        "is one thousand.<bookmark mark='b3'/> The rule works even when the "
        "number of digits changes.<bookmark mark='b4'/>"
    ),
    "scene8": (
        "Numbers describe real things.<bookmark mark='b0'/> Our box has four "
        "pencils. Add one pencil and we have five, so five is the successor of "
        "four.<bookmark mark='b1'/> Take the last pencil out of a box that has "
        "one, and we are left with zero.<bookmark mark='b2'/> Adding one gives "
        "the successor; removing one gives the predecessor, when it exists in "
        "our collection.<bookmark mark='b3'/>"
    ),
    "scene9_setup": (
        "Your turn!<bookmark mark='b0'/> Look at the number line.<bookmark "
        "mark='b1'/> What is the successor of eleven?<bookmark mark='b2'/> And "
        "what is the predecessor of five?<bookmark mark='b3'/> Pause the video "
        "and try both.<bookmark mark='b4'/>"
    ),
    "scene9_reveal": (
        "Let us check.<bookmark mark='b0'/> Eleven plus one is twelve, so the "
        "successor of eleven is twelve.<bookmark mark='b1'/> Five minus one is "
        "four, so the predecessor of five is four.<bookmark mark='b2'/> And "
        "one last question: does zero have a predecessor in the whole numbers? "
        "No, because the whole number line begins at zero.<bookmark mark='b3'/>"
    ),
    "scene10": (
        "Let us recap.<bookmark mark='b0'/> The counting numbers, one, two, "
        "three and so on, are the natural numbers.<bookmark mark='b1'/> When "
        "zero joins them we get the whole numbers: zero, one, two, three and "
        "so on.<bookmark mark='b2'/> The successor of a number is one more, "
        "and the predecessor is one less, where it exists.<bookmark mark='b3'/> "
        "And zero is the smallest whole number, with no predecessor.<bookmark "
        "mark='b4'/> Whole numbers are natural numbers plus zero.<bookmark "
        "mark='b5'/> Thank you for watching!<bookmark mark='b6'/>"
    ),
}


class WholeNumbersStory(VoiceoverScene):
    """Story-mode chalkboard lesson: Whole Numbers (Class 6, Chapter 2)."""

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
        out_dir = _HERE / "media" / "videos" / "whole_numbers_story"
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
        self.beat1_counting()
        self.beat2_whole()
        self.beat3_compare()
        self.beat4_line()
        self.beat5_neighbours()
        self.beat6_zero_case()
        self.beat7_practise()
        self.beat8_real()
        self.beat9_challenge()
        self.beat10_summary()

        self._write_real_srt()

    # ================================================================ beats ==

    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Whole Numbers", 42, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 1.65, 0]))
            self.play(Write(title),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            sub = board_text("From Counting to Zero", 22, CHALK_YELLOW,
                             "BOLD").move_to(np.array([BOARD_CX, BOARD_CY + 0.95, 0]))
            self.play(Write(sub),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.4))

            line = num_line([0, 1, 2, 3, 4, 5], x0=-1.75, step=0.9, y=-0.65,
                            size=26)
            tag = board_text("Numbers that count, and the number for nothing.",
                             17, CHALK_CYAN).move_to(
                np.array([BOARD_CX, -2.05, 0]))
            # the line and tag take the rest of the b0 -> b1 window (no
            # fraction: a *0.6 second play would only consume 76% of it and
            # drag the zero highlight 1.9 s early, onto the wrong sentence)
            self.play(FadeIn(line, shift=DOWN * 0.1), FadeIn(tag),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(Indicate(line.dots[0], color=ZERO_COLOR, scale_factor=2.2),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: counting down to nothing ----------------------------------
    def beat1_counting(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("Let's Count!", 26, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            box = pencil_box(3, pos=np.array([BOARD_CX - 1.0, 0.35, 0]))
            count = MathTex("3", font_size=64, color=CHALK_YELLOW).move_to(
                np.array([BOARD_CX + 1.15, 0.35, 0]))
            # the box starts with EXACTLY three pencils, and each removal takes
            # one away, so the number on the right always matches the box
            self.play(Write(heading), FadeIn(box.box), FadeIn(box.inner),
                      FadeIn(box.rim),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(*[FadeIn(p, shift=UP * 0.1) for p in box.pencils],
                      Write(count),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            two = MathTex("2", font_size=64, color=CHALK_YELLOW).move_to(count)
            one = MathTex("1", font_size=64, color=CHALK_YELLOW).move_to(count)
            # each removal slides the remaining pencils back to the centre, so
            # the box never looks like it is missing pencils at one end
            self.play(FadeOut(box.pencils[2], shift=DOWN * 0.4),
                      *[p.animate.move_to(spot) for p, spot in
                        zip(box.pencils[:2], box.centres(2))],
                      TransformMatchingTex(count, two),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeOut(box.pencils[1], shift=DOWN * 0.4),
                      box.pencils[0].animate.move_to(box.centres(1)[0]),
                      TransformMatchingTex(two, one),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            question = MathTex("?", font_size=56, color=CHALK_PINK).move_to(count)
            self.play(FadeOut(box.pencils[0], shift=DOWN * 0.4),
                      TransformMatchingTex(one, question),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            zero = MathTex("0", font_size=72, color=ZERO_COLOR).move_to(
                np.array([BOARD_CX - 1.0, 0.35, 0]))
            zbox = SurroundingRectangle(zero, color=ZERO_COLOR, buff=0.24,
                                        corner_radius=0.1, stroke_width=3)
            note = board_text("What number represents nothing?", 20, CHALK_WHITE,
                              "BOLD").move_to(np.array([BOARD_CX, -1.5, 0]))
            self.play(FadeOut(question), Write(zero), Create(zbox),
                      FadeIn(note, shift=UP * 0.1),
                      Flash(zero, color=ZERO_COLOR, flash_radius=0.8),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: natural numbers become whole numbers ----------------------
    def beat2_whole(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("From Counting to Whole Numbers", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            nat_label = board_text("NATURAL NUMBERS", 20, NAT_COLOR, "BOLD").move_to(
                np.array([BOARD_CX, 1.95, 0]))
            nat_row = card_row([1, 2, 3, 4, 5], NAT_COLOR, 0.56, 0.16, 24).move_to(
                np.array([BOARD_CX - 0.35, 1.2, 0]))
            dots = MathTex(r"\ldots", font_size=34, color=NAT_COLOR).next_to(
                nat_row, RIGHT, buff=0.22)
            nat_set = MathTex(r"N=\{1,2,3,4,\ldots\}", font_size=32,
                              color=NAT_COLOR).move_to(
                np.array([BOARD_CX, 0.45, 0]))
            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))
            self.play(FadeIn(nat_row, shift=DOWN * 0.12), FadeIn(dots),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)
            # the label owns "they are the natural numbers" (b0 -> b1); the
            # set notation owns "we write them as the set ..." (b1 -> b2)
            self.play(FadeIn(nat_label), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.play(Write(nat_set), run_time=rt(
                tracker.time_until_bookmark("b2") * 0.7))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.play(Indicate(nat_set, color=NAT_COLOR, scale_factor=1.04),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            # zero travels in from the left
            zero_chip = number_card(0, ZERO_COLOR, 0.56, 24).move_to(
                np.array([BOARD_LEFT + 0.9, 1.2, 0]))
            self.play(FadeIn(zero_chip, shift=RIGHT * 0.3), run_time=rt(
                tracker.time_until_bookmark("b3") * 0.5))
            self.play(zero_chip.animate.next_to(nat_row, LEFT, buff=0.16),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            whole_row = card_row([0, 1, 2, 3, 4, 5], WHOLE_COLOR, 0.56, 0.16, 24,
                                 ).move_to(np.array([BOARD_CX - 0.35, -0.75, 0]))
            whole_label = board_text("WHOLE NUMBERS", 20, WHOLE_COLOR, "BOLD"
                                     ).move_to(np.array([BOARD_CX, -0.15, 0]))
            # the rows merge on "zero joins the collection", and the zero card
            # flashes right after the word "zero", not on "three, four and so on"
            self.play(ReplacementTransform(VGroup(nat_row, dots, zero_chip),
                                           whole_row),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.25))
            self.play(Flash(whole_row[0], color=ZERO_COLOR, flash_radius=0.5),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(FadeOut(nat_label), FadeIn(whole_label),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            whole_set = MathTex(r"W=\{0,1,2,3,4,\ldots\}", font_size=32,
                                color=WHOLE_COLOR).move_to(
                np.array([BOARD_CX, -1.55, 0]))
            # "Whole numbers are the natural numbers together with zero."
            self.play(Write(whole_set), run_time=rt(
                tracker.time_until_bookmark("b6") * 0.55))
            self.add_sound(self.sfx["ding"], gain=-13)

            rule = MathTex(r"W = N \cup \{0\}", font_size=34, color=ZERO_COLOR)
            centre_on(rule, BOARD_CX, -2.35)
            rbox = SurroundingRectangle(rule, color=ZERO_COLOR, buff=0.16,
                                        corner_radius=0.1, stroke_width=3)
            self.play(Write(rule), Create(rbox),
                      Flash(rule, color=ZERO_COLOR, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b6")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: spot the difference ---------------------------------------
    def beat3_compare(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()

            heading = board_text("Spot the Difference", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            nat_lab = board_text("Natural", 18, NAT_COLOR, "BOLD")
            who_lab = board_text("Whole", 18, WHOLE_COLOR, "BOLD")
            nat_row = card_row([1, 2, 3, 4, 5], NAT_COLOR, 0.6, 0.2, 26).move_to(
                np.array([BOARD_CX + 0.35, 1.45, 0]))
            who_row = card_row([0, 1, 2, 3, 4, 5], WHOLE_COLOR, 0.6, 0.2, 26
                               ).move_to(np.array([BOARD_CX + 0.35, 0.35, 0]))
            # 1..5 must sit directly above the matching whole numbers, so the
            # dashed "they match" links are vertical, not slanted (shift in x
            # only -- shifting by the full centre would drop the row a level)
            nat_row.shift(RIGHT * (who_row[1].get_center()[0]
                                   - nat_row[0].get_center()[0]))
            nat_dots = MathTex(r"\ldots", font_size=32, color=NAT_COLOR).next_to(
                nat_row, RIGHT, buff=0.2)
            who_dots = MathTex(r"\ldots", font_size=32, color=WHOLE_COLOR
                               ).next_to(who_row, RIGHT, buff=0.2)
            # labels sit in one column just left of the rows they name
            who_lab.next_to(who_row, LEFT, buff=0.3)
            nat_lab.move_to(np.array([who_lab.get_center()[0],
                                      nat_row.get_center()[1], 0]))

            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))
            self.play(FadeIn(nat_lab), FadeIn(nat_row, shift=DOWN * 0.1),
                      FadeIn(nat_dots),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.6))
            self.play(FadeIn(who_lab), FadeIn(who_row, shift=DOWN * 0.1),
                      FadeIn(who_dots),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            # the matching numbers line up
            links = VGroup(*[
                DashedLine(nat_row[i].get_bottom(),
                           who_row[i + 1].get_top(),
                           color=CHALK_WHITE, stroke_width=1.4,
                           stroke_opacity=0.5)
                for i in range(5)
            ])
            self.play(Create(links), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            only = board_text("Only zero is the new addition.", 19, ZERO_COLOR,
                              "BOLD").move_to(np.array([BOARD_CX, -0.65, 0]))
            self.play(Indicate(who_row[0], color=ZERO_COLOR, scale_factor=1.25),
                      FadeIn(only), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            small_nat = board_text("Smallest natural number = 1", 18, NAT_COLOR,
                                   "BOLD").move_to(np.array([BOARD_CX, -1.25, 0]))
            small_who = board_text("Smallest whole number = 0", 18, WHOLE_COLOR,
                                   "BOLD").move_to(np.array([BOARD_CX, -1.72, 0]))
            self.play(FadeIn(small_nat, shift=RIGHT * 0.12),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            self.play(FadeIn(small_who, shift=RIGHT * 0.12),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            sub = MathTex(r"N \subset W", font_size=36, color=CHALK_YELLOW)
            centre_on(sub, BOARD_CX, -2.2)
            sbox = SurroundingRectangle(sub, color=CHALK_YELLOW, buff=0.2,
                                        corner_radius=0.1, stroke_width=3)
            self.play(Write(sub), Create(sbox), FadeOut(links),
                      Flash(sub, color=CHALK_YELLOW, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: the whole-number line --------------------------------------
    def beat4_line(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()

            heading = board_text("The Whole Number Line", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            line = num_line([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], x0=-2.9,
                            step=0.70, y=-0.55, size=24, pad=0.45)
            zero_lab = board_text("starting point", 16, ZERO_COLOR, "BOLD")

            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))
            self.play(Create(line[0]), FadeIn(line.dots[0]), FadeIn(line.labels[0]),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            zero_lab.next_to(line.dots[0], UP, buff=0.55)
            self.play(FadeIn(zero_lab, shift=DOWN * 0.1),
                      Indicate(line.dots[0], color=ZERO_COLOR, scale_factor=1.8),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            early = VGroup(*[line.dots[v] for v in (1, 2, 3)],
                           *[line.labels[v] for v in (1, 2, 3)])
            late = VGroup(*[line.dots[v] for v in range(4, 11)],
                          *[line.labels[v] for v in range(4, 11)])
            # dots 1-3 own "one, two, three", dots 4-10 the rest of the count
            self.play(FadeIn(early, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b2") * 0.18))
            self.play(FadeIn(late, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            marker = Dot(radius=0.11, color=CHALK_GREEN).move_to(line.dots[3])
            self.play(FadeIn(marker), run_time=rt(
                tracker.time_until_bookmark("b3") * 0.25))
            self.play(marker.animate.move_to(line.dots[4]), run_time=rt(
                tracker.time_until_bookmark("b3") * 0.35))
            greater = board_text("The number on the right is greater.", 19,
                                 CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, 1.15, 0]))
            self.play(FadeIn(greater), Flash(marker, color=CHALK_GREEN,
                                             flash_radius=0.5),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            tag = board_text("Zero is the starting point of the whole-number line.",
                             18, CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX, -2.1, 0]))
            self.play(FadeOut(zero_lab), FadeOut(marker), FadeIn(tag),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: predecessor and successor ----------------------------------
    def beat5_neighbours(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            self.reset_board()

            heading = board_text("Predecessor and Successor", 23, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            line = num_line([7, 8, 9, 10, 11], x0=-2.2, step=1.35, y=-0.95,
                            size=28)
            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))
            self.play(Create(line[0]),
                      *[FadeIn(line.dots[v]) for v in (7, 8, 9, 10, 11)],
                      *[FadeIn(line.labels[v]) for v in (7, 8, 9, 10, 11)],
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            ours = board_text("Our number = 9", 19, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, 1.75, 0]))
            self.play(FadeIn(ours), Indicate(line.dots[9], color=CHALK_WHITE,
                                             scale_factor=2.0),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # the two arrows sit at different heights so they never read as one
            # double-headed arrow; each label sits above its own arrow and each
            # equation is parked to the side, level with its arrow
            succ = step_arrow(line.x[9], line.x[10], line.y, SUCC_COLOR,
                              lift=0.45)
            succ_lbl = board_text("SUCCESSOR", 18, SUCC_COLOR, "BOLD").move_to(
                np.array([(line.x[9] + line.x[10]) / 2, line.y + 0.82, 0]))
            succ_eq = MathTex("9+1=10", font_size=30, color=SUCC_COLOR).move_to(
                np.array([4.0, line.y + 0.45, 0]))
            self.play(GrowArrow(succ), FadeIn(succ_lbl), Write(succ_eq),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            pred = step_arrow(line.x[9], line.x[8], line.y, PRED_COLOR,
                              lift=1.0)
            pred_lbl = board_text("PREDECESSOR", 18, PRED_COLOR, "BOLD").move_to(
                np.array([(line.x[9] + line.x[8]) / 2, line.y + 1.37, 0]))
            pred_eq = MathTex("9-1=8", font_size=30, color=PRED_COLOR).move_to(
                np.array([-3.0, line.y + 1.0, 0]))
            self.play(GrowArrow(pred), FadeIn(pred_lbl), Write(pred_eq),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            both = VGroup(
                board_text("Successor", 17, SUCC_COLOR, "BOLD"),
                board_text("→ next number", 17, CHALK_WHITE),
                board_text("Predecessor", 17, PRED_COLOR, "BOLD"),
                board_text("→ previous number", 17, CHALK_WHITE),
            ).arrange(RIGHT, buff=0.28).move_to(np.array([BOARD_CX, -1.95, 0]))
            self.play(FadeIn(both, shift=UP * 0.1),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            rule = MathTex(r"\text{Successor}=n+1", r"\quad", r"\text{Predecessor}=n-1",
                           font_size=28, color=CHALK_YELLOW).move_to(
                np.array([BOARD_CX, -2.55, 0]))
            self.play(Write(rule), Flash(rule, color=CHALK_YELLOW,
                                         flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: the special case of zero and one ---------------------------
    def beat6_zero_case(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("What Comes Before 1?", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            line = num_line([0, 1, 2, 3, 4], x0=-2.4, step=1.45, y=-0.95,
                            size=28)
            self.play(Write(heading), Create(line[0]),
                      *[FadeIn(line.dots[v]) for v in (0, 1, 2, 3, 4)],
                      *[FadeIn(line.labels[v]) for v in (0, 1, 2, 3, 4)],
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.5))
            ask = board_text("What comes before 1?", 19, CHALK_PINK, "BOLD"
                             ).move_to(np.array([BOARD_CX, 1.15, 0]))
            self.play(FadeIn(ask), Indicate(line.dots[1], color=CHALK_WHITE,
                                            scale_factor=2.0),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            arrow = step_arrow(line.x[1], line.x[0], line.y, PRED_COLOR)
            eq1 = MathTex("1-1=0", font_size=32, color=PRED_COLOR).move_to(
                np.array([BOARD_CX, 0.4, 0]))
            self.play(GrowArrow(arrow), Write(eq1),
                      Flash(line.dots[0], color=ZERO_COLOR, flash_radius=0.5),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            not_nat = board_text("0 is not a natural number.", 18, CHALK_PINK,
                                 "BOLD").move_to(
                np.array([BOARD_CX, -1.85, 0]))
            is_whole = board_text("0 is a whole number.", 18, WHOLE_COLOR,
                                  "BOLD").move_to(
                np.array([BOARD_CX, -2.35, 0]))
            self.play(FadeIn(not_nat, shift=RIGHT * 0.12),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            self.play(FadeIn(is_whole, shift=RIGHT * 0.12),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            nat_case = board_text("In N, 1 has no predecessor.", 18, NAT_COLOR,
                                  "BOLD").move_to(
                np.array([BOARD_CX, 0.4, 0]))
            who_case = board_text("In W, the predecessor of 1 is 0.", 18,
                                  WHOLE_COLOR, "BOLD").move_to(
                np.array([BOARD_CX, -0.1, 0]))
            self.play(FadeOut(eq1), FadeIn(nat_case, shift=RIGHT * 0.12),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.4))
            self.play(FadeIn(who_case, shift=RIGHT * 0.12),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            # the dashed "nothing to the left" mark stops just above the axis so
            # it never runs through the "0" label below the dot
            boundary = DashedLine(line.dots[0].get_center() + DOWN * 0.02,
                                  line.dots[0].get_center() + UP * 0.44,
                                  color=ZERO_COLOR, stroke_width=3)
            none = board_text("No predecessor within Whole Numbers", 18,
                              ZERO_COLOR, "BOLD").move_to(
                np.array([BOARD_CX, 1.15, 0]))
            # clear the earlier question first: a long cross-fade in the same
            # spot would leave both sentences unreadable on top of each other
            self.play(FadeOut(ask), run_time=rt(
                tracker.time_until_bookmark("b4") * 0.25))
            self.play(Create(boundary), FadeIn(none),
                      Indicate(line.dots[0], color=ZERO_COLOR, scale_factor=2.0),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            # "0 + 1 = 1": the successor arrow sits higher and the predecessor
            # arrow is cleared away, so the two never merge into one
            # double-headed arrow
            succ = step_arrow(line.x[0], line.x[1], line.y, SUCC_COLOR,
                              lift=0.78)
            eq2 = MathTex("0+1=1", font_size=32, color=SUCC_COLOR).move_to(
                np.array([BOARD_CX, 0.4, 0]))
            self.play(FadeOut(nat_case), FadeOut(who_case), FadeOut(boundary),
                      FadeOut(arrow), GrowArrow(succ), Write(eq2),
                      Flash(line.dots[1], color=SUCC_COLOR, flash_radius=0.5),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: find the neighbouring numbers ------------------------------
    def beat7_practise(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("Find the Neighbours", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))

            cap_l, cap_m, cap_r = (
                board_text("Predecessor", 17, PRED_COLOR, "BOLD"),
                board_text("Number", 17, CHALK_WHITE, "BOLD"),
                board_text("Successor", 17, SUCC_COLOR, "BOLD"),
            )
            cards = three_cards(0, 13, 0, y=0.3)
            # each caption is centred on the card it names, not on a fixed gap
            cap_l.move_to(np.array([cards.left.box.get_center()[0], 1.3, 0]))
            cap_m.move_to(np.array([cards.mid.box.get_center()[0], 1.3, 0]))
            cap_r.move_to(np.array([cards.right.box.get_center()[0], 1.3, 0]))
            caps = VGroup(cap_l, cap_m, cap_r)
            # start with only the middle number filled in
            blank_l = MathTex("?", font_size=32, color=PRED_COLOR).move_to(
                cards.left.txt)
            blank_r = MathTex("?", font_size=32, color=SUCC_COLOR).move_to(
                cards.right.txt)
            # the empty table is the preamble (b0); "Take thirteen." fills it
            self.play(FadeIn(cards.left.box), FadeIn(cards.mid.box),
                      FadeIn(cards.right.box), FadeIn(caps),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(Write(cards.mid.txt), FadeIn(blank_l), FadeIn(blank_r),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.25))

            twelve = MathTex("12", font_size=32, color=PRED_COLOR).move_to(
                cards.left.txt)
            fourteen = MathTex("14", font_size=32, color=SUCC_COLOR).move_to(
                cards.right.txt)
            self.play(TransformMatchingTex(blank_l, twelve),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.4))
            self.play(TransformMatchingTex(blank_r, fourteen),
                      Flash(cards.right.box, color=SUCC_COLOR, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(Indicate(cards.mid.txt, color=CHALK_YELLOW, scale_factor=1.2),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            # the number changes, so its neighbours must not stay behind:
            # 13 -> 999 blanks 12 and 14 until the new pair is written
            nine99 = MathTex("999", font_size=32, color=CHALK_YELLOW).move_to(
                cards.mid.txt)
            q_l = MathTex("?", font_size=32, color=PRED_COLOR).move_to(twelve)
            q_r = MathTex("?", font_size=32, color=SUCC_COLOR).move_to(fourteen)
            self.play(TransformMatchingTex(cards.mid.txt, nine99),
                      FadeOut(twelve), FadeOut(fourteen),
                      FadeIn(q_l), FadeIn(q_r),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            nine98 = MathTex("998", font_size=32, color=PRED_COLOR).move_to(q_l)
            thousand = MathTex("1000", font_size=32, color=SUCC_COLOR).move_to(q_r)
            self.play(TransformMatchingTex(q_l, nine98),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.4))
            self.play(TransformMatchingTex(q_r, thousand),
                      Flash(cards.right.box, color=SUCC_COLOR, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)

            tag = board_text("One less ← Number → One more", 19, CHALK_YELLOW,
                             "BOLD").move_to(np.array([BOARD_CX, -1.35, 0]))
            # one term under each card, on the cards' own pitch
            r_l = MathTex("n-1", font_size=30, color=PRED_COLOR).move_to(
                np.array([cards.left.box.get_center()[0], -2.05, 0]))
            r_m = MathTex("n", font_size=30, color=CHALK_WHITE).move_to(
                np.array([cards.mid.box.get_center()[0], -2.05, 0]))
            r_r = MathTex("n+1", font_size=30, color=SUCC_COLOR).move_to(
                np.array([cards.right.box.get_center()[0], -2.05, 0]))
            self.play(FadeIn(tag), Write(r_l), Write(r_m), Write(r_r),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: real-world application -------------------------------------
    def beat8_real(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("Adding and Removing One", 23, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            box = pencil_box(4, width=2.1, height=1.15,
                             pos=np.array([-2.0, 0.2, 0]))
            count = MathTex("4", font_size=54, color=CHALK_YELLOW).move_to(
                np.array([-0.15, 0.2, 0]))
            self.play(Write(heading), FadeIn(box.box), FadeIn(box.inner),
                      FadeIn(box.rim), Write(count),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.5))
            self.play(*[FadeIn(p, shift=UP * 0.1) for p in box.pencils],
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            five = MathTex("5", font_size=54, color=CHALK_YELLOW).move_to(count)
            add_eq = MathTex("4+1=5", font_size=32, color=SUCC_COLOR).move_to(
                np.array([2.6, 0.75, 0]))
            succ_lbl = board_text("Successor of 4 = 5", 18, SUCC_COLOR, "BOLD"
                                  ).move_to(np.array([2.6, 0.15, 0]))
            # the fifth pencil fades in at its own centred place while the other
            # four slide outwards to make an evenly spread row of five
            box.hidden[0].move_to(box.centres(5)[4])
            self.play(FadeIn(box.hidden[0], shift=UP * 0.1),
                      *[p.animate.move_to(spot) for p, spot in
                        zip(box.pencils_all[:4], box.centres(5)[:4])],
                      TransformMatchingTex(count, five), Write(add_eq),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.play(FadeIn(succ_lbl, shift=RIGHT * 0.12),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # one pencil, then none
            solo = VGroup(box.box.copy(), box.inner.copy(), box.rim.copy(),
                          box.pencils[0].copy()).move_to(
                np.array([-2.0, -1.45, 0]))
            solo[3].move_to(solo[1].get_center() + UP * 0.04)
            solo_count = MathTex("1", font_size=44, color=CHALK_YELLOW).move_to(
                np.array([-0.15, -1.45, 0]))
            zero_eq = MathTex("1-1=0", font_size=32, color=PRED_COLOR).move_to(
                np.array([2.6, -1.45, 0]))
            # the box and its "1" fill the first part of the window; the last
            # pencil is taken out when the voice reaches "out of a box that has
            # one ... left with zero"
            self.play(FadeIn(solo), Write(solo_count),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.75))
            zero_count = MathTex("0", font_size=44, color=ZERO_COLOR).move_to(
                solo_count)
            zero_word = board_text("Zero pencils", 18, ZERO_COLOR, "BOLD"
                                   ).move_to(np.array([-2.0, -2.25, 0]))
            # the pencil is solo[3]; fading solo[1] would have removed the tray
            self.play(FadeOut(solo[3], shift=DOWN * 0.3),
                      TransformMatchingTex(solo_count, zero_count), Write(zero_eq),
                      FadeIn(zero_word, shift=UP * 0.1),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            add_line = board_text("+1 gives the successor", 17,
                                  SUCC_COLOR, "BOLD").move_to(
                np.array([2.5, -0.45, 0]))
            rem_line = board_text("−1 gives the predecessor", 17, PRED_COLOR,
                                  "BOLD").move_to(
                np.array([2.5, -1.05, 0]))
            self.play(FadeIn(add_line, shift=RIGHT * 0.12),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            self.play(FadeIn(rem_line, shift=RIGHT * 0.12),
                      Flash(add_line, color=SUCC_COLOR, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 9: student challenge -----------------------------------------
    def beat9_challenge(self) -> None:
        with self.voiceover(text=NARRATION["scene9_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", 30, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y - 0.05, 0]))
            line = num_line(list(range(13)), x0=-3.2, step=0.62, y=-0.35,
                            size=22)
            q1 = board_text("What is the successor of 11?", 19, SUCC_COLOR,
                            "BOLD").move_to(np.array([BOARD_CX, 1.75, 0]))
            q2 = board_text("What is the predecessor of 5?", 19, PRED_COLOR,
                            "BOLD").move_to(np.array([BOARD_CX, 1.15, 0]))
            pause = board_text("Pause and try both.", 19, CHALK_YELLOW, "BOLD"
                               ).move_to(np.array([BOARD_CX, -1.5, 0]))

            self.play(Write(heading), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.play(Create(line[0]),
                      *[FadeIn(line.dots[v]) for v in range(13)],
                      *[FadeIn(line.labels[v]) for v in range(13)],
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)
            # each question owns its own bookmark window: successor (b1 -> b2),
            # predecessor (b2 -> b3), pause prompt (b3 -> b4)
            self.play(FadeIn(q1, shift=RIGHT * 0.12), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(q2, shift=RIGHT * 0.12), run_time=rt(
                tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(pause, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b4")))

            self.challenge = {"line": line, "q1": q1, "q2": q2, "pause": pause}
            self._capture_srt(tracker)

        # the clock sits past the right end of the line, where it hides neither
        # the dots and labels of the 0-12 line nor either question
        play_challenge_countdown(self, seconds=4, sfx=self.sfx,
                                 position=np.array([4.15, 0.85, 0]))

        with self.voiceover(text=NARRATION["scene9_reveal"]) as tracker:
            line, q1, q2 = (self.challenge["line"], self.challenge["q1"],
                            self.challenge["q2"])
            self.play(FadeOut(self.challenge["pause"]),
                      run_time=rt(tracker.time_until_bookmark("b0")))

            # b0 -> b1: "Eleven plus one is twelve, so the successor of eleven
            # is twelve."
            a1 = MathTex("11+1=12", font_size=30, color=SUCC_COLOR).move_to(
                np.array([BOARD_CX - 1.9, -1.5, 0]))
            ans1 = MathTex("12", font_size=40, color=SUCC_COLOR).move_to(
                np.array([BOARD_CX - 1.9, -2.15, 0]))
            abox1 = SurroundingRectangle(ans1, color=SUCC_COLOR, buff=0.14,
                                         corner_radius=0.1, stroke_width=3)
            arrow_r = step_arrow(line.x[11], line.x[12], line.y, SUCC_COLOR,
                                 lift=0.36)
            self.play(GrowArrow(arrow_r), Write(a1), Write(ans1), Create(abox1),
                      Flash(line.dots[12], color=SUCC_COLOR, flash_radius=0.5),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            # b1 -> b2: "Five minus one is four, so the predecessor of five is
            # four."
            a2 = MathTex("5-1=4", font_size=30, color=PRED_COLOR).move_to(
                np.array([BOARD_CX + 1.9, -1.5, 0]))
            ans2 = MathTex("4", font_size=40, color=PRED_COLOR).move_to(
                np.array([BOARD_CX + 1.9, -2.15, 0]))
            abox2 = SurroundingRectangle(ans2, color=PRED_COLOR, buff=0.14,
                                         corner_radius=0.1, stroke_width=3)
            arrow_l = step_arrow(line.x[5], line.x[4], line.y, PRED_COLOR,
                                 lift=0.36)
            self.play(GrowArrow(arrow_l), Write(a2), Write(ans2), Create(abox2),
                      Flash(line.dots[4], color=PRED_COLOR, flash_radius=0.5),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            ask = board_text("Does zero have a predecessor in W?", 19,
                             CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, 2.15, 0]))
            no = board_text("No.", 22, ZERO_COLOR, "BOLD").next_to(ask, RIGHT,
                                                                   buff=0.25)
            # clear the two questions first, so the new line is not crammed
            # against them, then ask it and answer
            self.play(FadeOut(q1), FadeOut(q2), run_time=rt(
                tracker.time_until_bookmark("b3") * 0.2))
            self.play(FadeIn(ask), run_time=rt(
                tracker.time_until_bookmark("b3") * 0.45))
            self.play(FadeIn(no, shift=RIGHT * 0.12),
                      Flash(no, color=ZERO_COLOR, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)
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

            # b0 -> b1: "The counting numbers, one, two, three and so on, are
            # the natural numbers."
            nat = MathTex(r"N=\{1,2,3,\ldots\}", font_size=30, color=NAT_COLOR
                          ).move_to(np.array([BOARD_CX, 2.1, 0]))
            rows = VGroup(
                summary_row(1, "Natural numbers are the counting numbers:",
                            r"1,2,3,\ldots", NAT_COLOR),
                summary_row(2, "Whole numbers add zero:",
                            r"0,1,2,3,\ldots", WHOLE_COLOR),
                summary_row(3, "Successor = one more:",
                            r"n+1", SUCC_COLOR),
                summary_row(4, "Predecessor = one less:",
                            r"n-1", PRED_COLOR),
            ).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
            rows.move_to(np.array([BOARD_CX, 0.55, 0]))
            rows.shift(RIGHT * (BOARD_CX - rows.get_center()[0]))
            self.play(Write(nat), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.45))
            self.play(FadeIn(rows[0], shift=RIGHT * 0.12), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)

            # b1 -> b2: "When zero joins them we get the whole numbers ..."
            whole = MathTex(r"W=N\cup\{0\}=\{0,1,2,3,\ldots\}", font_size=30,
                            color=WHOLE_COLOR).move_to(
                np.array([BOARD_CX, 2.1, 0]))
            self.play(TransformMatchingTex(nat, whole),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.45))
            self.play(FadeIn(rows[1], shift=RIGHT * 0.12), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # b2 -> b3: "The successor of a number is one more, and the
            # predecessor is one less, where it exists."
            self.play(FadeIn(rows[2], shift=RIGHT * 0.12),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            self.play(FadeIn(rows[3], shift=RIGHT * 0.12),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            note = board_text("Zero is the smallest whole number — "
                              "and it has no predecessor.", 17, ZERO_COLOR,
                              "BOLD").move_to(np.array([BOARD_CX, -1.35, 0]))
            self.play(FadeIn(note, shift=UP * 0.1),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            take = board_text("Whole Numbers = Natural Numbers + Zero", 22,
                              CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.95, 0]))
            take2 = board_text("Successor → +1     Predecessor → −1", 16,
                               CHALK_CYAN).move_to(
                np.array([BOARD_CX, -2.45, 0]))
            self.play(FadeIn(take), FadeIn(take2),
                      Flash(take, color=CHALK_YELLOW, flash_radius=0.9),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["success"], gain=-11)

            summary = VGroup(heading, whole, rows, note, take, take2)
            # the takeaway has had its whole line; clear it as the thank-you
            # card comes in, a fraction of the next line
            self.play(FadeOut(summary),
                      run_time=rt(tracker.time_until_bookmark("b6") * 0.35))

            thanks = board_text("Thank You for Watching!", 40, CHALK_WHITE,
                                "BOLD")
            thanks2 = board_text("See you in the next lesson :)", 25, CHALK_CYAN)
            thanks_group = VGroup(thanks, thanks2).arrange(DOWN, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY, 0]))
            self.play(Write(thanks),
                      run_time=rt(tracker.time_until_bookmark("b6") * 0.4))
            self.add_sound(self.sfx["ding"], gain=-11)
            self.play(FadeIn(thanks2, shift=UP * 0.1),
                      run_time=rt(tracker.time_until_bookmark("b6")))
            self.play(Circumscribe(thanks_group, color=CHALK_AMBER, stroke_width=3,
                                   time_width=0.5), run_time=0.3)
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(END_HOLD)


if __name__ == "__main__":
    pass

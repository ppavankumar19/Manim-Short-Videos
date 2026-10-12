"""
Two-Digit Number Riddles — Cracking Digit Reversal
Story-mode chalkboard lesson (Telangana Class 8 Maths, Chapter 2:
Linear Equations in One Variable, digit puzzles).

Core idea: a two-digit number is NOT two loose digits -- it is tens plus ones,
i.e. 10t + u. Reversing the digits swaps their place values, giving 10u + t.
Two place-value boxes stay fixed on the board while the same digit objects
physically cross between them, so every reversal puzzle becomes an equation.

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
  0. Title card -- 35 -> 53 in miniature.
  1. Same Digits, New Number -- the flip display reverses.
  2. Place Value -- Tens/Ones boxes, 35 = 30 + 5 = 10*3 + 5.
  3. What Reversal Means -- the digits cross boxes, 53 = 10*5 + 3.
  4. General Form -- 10t + u and the mirrored 10u + t.
  5. Choose the Unknown -- digits sum 8, ones = x, tens = 8-x.
  6. Form and Solve -- (80-9x)+18 = 9x+8 -> x = 5 -> 35.
  7. Check -- 35 + 18 = 53 and 3 + 5 = 8.
  8. Real-World Place Value -- 30+5 against 50+3 on two displays.
  9. Student Challenge -- sum 9, minus 27 -> 63.
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
    ImageMobject, MathTex, VGroup, Line, DashedLine, Circle, Rectangle,
    RoundedRectangle, Arrow, ArcBetweenPoints, MoveAlongPath, DoubleArrow, Text,
    Write, FadeIn, FadeOut, Create, ReplacementTransform, TransformMatchingTex,
    TransformFromCopy, GrowArrow, Indicate, Flash, Circumscribe,
    SurroundingRectangle, config,
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

TENS_COLOR = CHALK_CYAN      # the tens digit keeps one colour everywhere
ONES_COLOR = CHALK_PINK      # the ones digit keeps another

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

EQU_Y = 0.55        # the main equation line
HEAD_Y = BOARD_TOP - 0.45
BOX_Y = 0.7         # place-value box row
BOX_DX = 1.2        # half-distance between the two boxes


def rt(seconds: float, floor: float = MIN_RT) -> float:
    return max(floor, float(seconds))


def board_text(s: str, size: int = 34, color: str = CHALK_WHITE,
               weight: str = "NORMAL") -> Text:
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def chalk_math(s: str, size: int = 34, color: str = MATH_COLOR) -> MathTex:
    return MathTex(s, font_size=size, color=color)


def align_equals(eq: MathTex, cx: float = BOARD_CX, cy: float = EQU_Y) -> MathTex:
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


# --------------------------------------------------- place-value machinery --
def digit_card(d: str, color: str = CHALK_WHITE, size: float = 1.15) -> VGroup:
    """One flip-display digit card: a dark tile with the digit on it."""
    card = RoundedRectangle(corner_radius=0.08, width=size * 0.78, height=size,
                            stroke_color=CHALK_AMBER, stroke_width=2,
                            fill_color="#1B2430", fill_opacity=0.95)
    lbl = MathTex(d, font_size=int(size * 46), color=color).move_to(card.get_center())
    return VGroup(card, lbl)


def flip_display(d1: str, d2: str,
                 c1: str = CHALK_WHITE, c2: str = CHALK_WHITE,
                 size: float = 1.15, buff: float = 0.1) -> VGroup:
    """A chalk flip-style two-digit display: frame, hinge line, two cards."""
    cards = VGroup(digit_card(d1, c1, size), digit_card(d2, c2, size)
                   ).arrange(RIGHT, buff=buff)
    frame = RoundedRectangle(corner_radius=0.12,
                             width=cards.width + 0.3, height=size + 0.28,
                             stroke_color=CHALK_AMBER, stroke_width=2.6,
                             fill_color="#101820", fill_opacity=0.85)
    frame.move_to(cards.get_center())
    hinge = Line(frame.get_top() + DOWN * 0.16, frame.get_bottom() + UP * 0.16,
                 stroke_color=CHALK_AMBER, stroke_width=1.2, stroke_opacity=0.5)
    grp = VGroup(frame, hinge, cards)
    grp.cards = cards
    return grp


def place_box(label: str, content, color: str, width: float = 1.2,
              height: float = 1.2, font_size: int = 38) -> VGroup:
    """A labelled place-value box holding a digit (or an expression)."""
    box = RoundedRectangle(corner_radius=0.1, width=width, height=height,
                           stroke_color=color, stroke_width=2.4,
                           fill_color="#16202B", fill_opacity=0.88)
    lbl = board_text(label, 15, color, "BOLD").next_to(box, UP, buff=0.1)
    val = MathTex(str(content), font_size=font_size, color=CHALK_WHITE)
    val.move_to(box.get_center())
    grp = VGroup(box, lbl, val)
    grp.box, grp.lbl, grp.val = box, lbl, val
    return grp


def box_pair(tens, ones, cy: float = BOX_Y,
             cx: float = BOARD_CX) -> VGroup:
    """The two place-value boxes, centred on the board."""
    pair = VGroup(tens, ones).arrange(RIGHT, buff=0.5)
    pair.move_to(np.array([cx, cy, 0]))
    return pair


def summary_row(n: int, label: str, math_tex: str, color: str) -> VGroup:
    badge = Circle(radius=0.19, stroke_color=color, stroke_width=2,
                   fill_color=color, fill_opacity=0.18)
    num = board_text(str(n), 17, color, "BOLD").move_to(badge.get_center())
    return VGroup(VGroup(badge, num),
                  board_text(label, 18, CHALK_WHITE),
                  MathTex(math_tex, font_size=22)).arrange(RIGHT, buff=0.28)


def swap_digits(a, b, arc: float = PI / 2.1):
    """Move two digit mobjects into each other's place along crossing arcs."""
    a_start, a_end = a.get_center(), b.get_center()
    b_start, b_end = b.get_center(), a.get_center()
    path_a = ArcBetweenPoints(a_start, a_end, angle=arc)
    path_b = ArcBetweenPoints(b_start, b_end, angle=-arc)
    return (MoveAlongPath(a, path_a), MoveAlongPath(b, path_b))


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "Today we crack a two-digit number puzzle.<bookmark mark='b0'/> The "
        "digits stay exactly the same, but their places change — and that "
        "changes everything.<bookmark mark='b1'/> Let's begin with a flip "
        "display!<bookmark mark='b2'/>"
    ),
    "scene1": (
        "Look at this display: thirty five.<bookmark mark='b0'/> Now watch the "
        "digit cards change places.<bookmark mark='b1'/> The display reads "
        "fifty three.<bookmark mark='b2'/> The digits are exactly the same, but "
        "the number is not.<bookmark mark='b3'/> How did the same digits make a "
        "new number?<bookmark mark='b4'/> It is all about place value."
        "<bookmark mark='b5'/>"
    ),
    "scene2": (
        "Every two-digit number is built from tens and ones.<bookmark mark='b0'/> "
        "In thirty five, the three sits in the tens place, so it counts three "
        "tens, which is thirty.<bookmark mark='b1'/> The five sits in the ones "
        "place, so it counts five ones, which is five.<bookmark mark='b2'/> Put "
        "together, thirty five is thirty plus five.<bookmark mark='b3'/> And "
        "thirty is ten times three, so thirty five is ten times three, plus "
        "five.<bookmark mark='b4'/>"
    ),
    "scene3": (
        "Now let's reverse the digits.<bookmark mark='b0'/> The three and the "
        "five lift out of their boxes and swap places.<bookmark mark='b1'/> Now "
        "the five is in the tens place, and the three is in the ones place."
        "<bookmark mark='b2'/> The new number is fifty three: ten times five, "
        "plus three.<bookmark mark='b3'/> Reversing the digits is simply "
        "swapping their place values.<bookmark mark='b4'/>"
    ),
    "scene4": (
        "Let's write this with symbols, so that it works for any number."
        "<bookmark mark='b0'/> Let the tens digit be t, and the ones digit be u."
        "<bookmark mark='b1'/> Then the original number is ten t plus u."
        "<bookmark mark='b2'/> When the digits are reversed, the tens digit "
        "becomes u and the ones digit becomes t, so the reversed number is ten u "
        "plus t.<bookmark mark='b3'/> Those two expressions are the key to every "
        "digit puzzle.<bookmark mark='b4'/>"
    ),
    "scene5": (
        "Here is our puzzle.<bookmark mark='b0'/> A two-digit number has digits "
        "whose sum is eight, and if eighteen is added to the number, its digits "
        "are reversed.<bookmark mark='b1'/> Let's choose the ones digit to be x."
        "<bookmark mark='b2'/> Since the digits add to eight, the tens digit must "
        "be eight minus x.<bookmark mark='b3'/> So the original number is ten "
        "times, eight minus x, plus x, which simplifies to eighty minus nine x."
        "<bookmark mark='b4'/> Now reverse the digits: the reversed number is ten "
        "x plus, eight minus x, which is nine x plus eight.<bookmark mark='b5'/>"
    ),
    "scene6": (
        "The condition says that the original number plus eighteen equals the "
        "reversed number.<bookmark mark='b0'/> Substituting our expressions gives "
        "eighty minus nine x, plus eighteen, equals nine x plus eight."
        "<bookmark mark='b1'/> That simplifies to ninety eight minus nine x "
        "equals nine x plus eight.<bookmark mark='b2'/> Collecting the x terms "
        "and the numbers gives ninety equals eighteen x.<bookmark mark='b3'/> So "
        "x equals five.<bookmark mark='b4'/> The ones digit is five, so the tens "
        "digit is three, and the number is thirty five.<bookmark mark='b5'/>"
    ),
    "scene7": (
        "Let's check the answer in the story.<bookmark mark='b0'/> The digits of "
        "thirty five add to eight: three plus five is eight.<bookmark mark='b1'/> "
        "And thirty five plus eighteen is fifty three, which is thirty five with "
        "its digits reversed.<bookmark mark='b2'/> Both conditions are satisfied, "
        "so the number is thirty five.<bookmark mark='b3'/>"
    ),
    "scene8": (
        "This is why reversal puzzles work at all.<bookmark mark='b0'/> On a real "
        "display, thirty five shows three tens and five ones, while fifty three "
        "shows five tens and three ones.<bookmark mark='b1'/> The same two "
        "digits, in a different place, are worth something completely different."
        "<bookmark mark='b2'/> Place value decides the value.<bookmark mark='b3'/>"
    ),
    "scene9_setup": (
        "Your turn!<bookmark mark='b0'/> A two-digit number has digits whose sum "
        "is nine, and if twenty seven is subtracted from the number, its digits "
        "are reversed.<bookmark mark='b1'/> Let the ones digit be x."
        "<bookmark mark='b2'/> Pause the video, and try it yourself."
        "<bookmark mark='b3'/>"
    ),
    "scene9_reveal": (
        "Since the digits add to nine, the tens digit is nine minus x."
        "<bookmark mark='b0'/> So the original number is ninety minus nine x, and "
        "the reversed number is nine x plus nine.<bookmark mark='b1'/> The "
        "condition gives ninety minus nine x, minus twenty seven, equals nine x "
        "plus nine.<bookmark mark='b2'/> That becomes sixty three minus nine x "
        "equals nine x plus nine, so fifty four equals eighteen x, and x equals "
        "three.<bookmark mark='b3'/> The tens digit is six, so the number is "
        "sixty three.<bookmark mark='b4'/> Excellent — you used place value to "
        "build the equation.<bookmark mark='b5'/>"
    ),
    "scene10": (
        "Let's summarise.<bookmark mark='b0'/> Write the tens digit and the ones "
        "digit, and remember that a two-digit number is ten times the tens digit, "
        "plus the ones digit.<bookmark mark='b1'/> Then the reversed number is "
        "ten times the ones digit, plus the tens digit.<bookmark mark='b2'/> Use "
        "the given condition to form one equation, and solve it.<bookmark "
        "mark='b3'/> Finally, put the digits back into the number, and check both "
        "conditions.<bookmark mark='b4'/> Use place value to build the equation. "
        "Thank you so much for watching, and I will see you in the next lesson!"
        "<bookmark mark='b5'/>"
    ),
}


class TwoDigitPuzzlesStory(VoiceoverScene):
    """Story-mode chalkboard lesson: two-digit reversal puzzles."""

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
        out_dir = _HERE / "media" / "videos" / "two_digit_puzzles_story"
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
        self.beat1_flip()
        self.beat2_place_value()
        self.beat3_reversal()
        self.beat4_general()
        self.beat5_setup()
        self.beat6_solve()
        self.beat7_check()
        self.beat8_realworld()
        self.beat9_challenge()
        self.beat10_summary()

        self._write_real_srt()

    # ================================================================ beats ==

    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Two-Digit Number Riddles", 38, CHALK_WHITE,
                               "BOLD").move_to(np.array([BOARD_CX, BOARD_CY + 1.6, 0]))
            self.play(Write(title), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            sub = board_text("Cracking digit reversal", 21, CHALK_YELLOW,
                             "BOLD").move_to(np.array([BOARD_CX, BOARD_CY + 0.9, 0]))
            self.play(Write(sub), run_time=rt(tracker.time_until_bookmark("b1") * 0.4))

            d35 = flip_display("3", "5", TENS_COLOR, ONES_COLOR, size=1.0)
            d35.move_to(np.array([BOARD_CX - 1.5, -0.75, 0]))
            d53 = flip_display("5", "3", ONES_COLOR, TENS_COLOR, size=1.0)
            d53.move_to(np.array([BOARD_CX + 1.5, -0.75, 0]))
            ar = Arrow(d35.get_right(), d53.get_left(), buff=0.12,
                       color=CHALK_YELLOW, stroke_width=2.6)
            self.play(FadeIn(d35, shift=DOWN * 0.1), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.6))
            self.play(GrowArrow(ar), FadeIn(d53, shift=DOWN * 0.1),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)

            question = board_text("Same digits — a different number!",
                                  19, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, -2.0, 0]))
            self.play(FadeIn(question), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["swipe"], gain=-15)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 1: same digits, new number -----------------------------------
    def beat1_flip(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("A Number Puzzle", 25, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            disp = flip_display("3", "5", TENS_COLOR, ONES_COLOR)
            disp.move_to(np.array([BOARD_CX, 0.95, 0]))
            self.play(FadeIn(disp, scale=0.85), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            # the two digit cards physically swap places
            cards = disp.cards
            a, b = cards[0], cards[1]
            self.play(*swap_digits(a, b), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            shown = None   # (the plain readout is not needed on screen)
            tag = board_text("Same digits, new number!", 19, CHALK_CYAN, "BOLD")
            tag.move_to(np.array([BOARD_CX, -0.9, 0]))
            self.play(FadeIn(tag), run_time=rt(tracker.time_until_bookmark("b2") * 0.5))

            # both numbers side by side: 35 -> 53
            d35 = flip_display("3", "5", TENS_COLOR, ONES_COLOR)
            d53 = flip_display("5", "3", ONES_COLOR, TENS_COLOR)
            pair = VGroup(d35, d53).arrange(RIGHT, buff=1.15).move_to(
                np.array([BOARD_CX, 0.95, 0]))
            ar = Arrow(pair[0].get_right(), pair[1].get_left(), buff=0.1,
                       color=CHALK_YELLOW, stroke_width=2.6)
            self.play(FadeOut(disp), FadeIn(d35), run_time=0.3)
            self.play(FadeIn(d53, shift=RIGHT * 0.2), GrowArrow(ar),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            question = board_text("How did the same digits make a new number?",
                                  20, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, -1.7, 0]))
            self.play(FadeOut(tag), FadeIn(question), run_time=rt(
                tracker.time_until_bookmark("b3")))

            place = board_text("It is all about place value.", 19, CHALK_YELLOW,
                               "BOLD").move_to(np.array([BOARD_CX, -2.25, 0]))
            self.play(FadeIn(place), run_time=rt(tracker.time_until_bookmark("b4") * 0.5))
            self.play(Indicate(pair[0].cards[0], color=TENS_COLOR, scale_factor=1.0),
                      Indicate(pair[1].cards[0], color=ONES_COLOR, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self.play(Flash(question, color=CHALK_PINK, flash_radius=0.8),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self.play(Indicate(pair[1].cards[0], color=ONES_COLOR, scale_factor=1.06),
                      run_time=rt(tracker.get_remaining_duration()))
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 2: place value ------------------------------------------------
    def beat2_place_value(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("Place Value", 26, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            tens = place_box("Tens", "3", TENS_COLOR)
            ones = place_box("Ones", "5", ONES_COLOR)
            pair = box_pair(tens, ones, cy=BOX_Y)
            self.play(FadeIn(pair, scale=0.9), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            t_lbl = MathTex("3\\text{ tens}", r"\;=\;", "30", font_size=26,
                            color=TENS_COLOR).move_to(np.array([-1.6, -0.75, 0]))
            self.play(Circumscribe(tens.box, color=TENS_COLOR, stroke_width=3),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.6))
            self.play(FadeIn(t_lbl), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            o_lbl = MathTex("5\\text{ ones}", r"\;=\;", "5", font_size=26,
                            color=ONES_COLOR).move_to(np.array([2.2, -0.75, 0]))
            self.play(Circumscribe(ones.box, color=ONES_COLOR, stroke_width=3),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.6))
            self.play(FadeIn(o_lbl), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            e1 = MathTex("35", r"\;=\;", "30+5", font_size=36)
            align_equals(e1, BOARD_CX, -1.55)
            self.play(FadeOut(t_lbl), FadeOut(o_lbl), Write(e1),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            e2 = MathTex("35", r"\;=\;", r"10\times 3+5", font_size=36)
            align_equals(e2, BOARD_CX, -1.55)
            self.play(TransformMatchingTex(e1, e2),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.6))
            note = board_text("place value matters", 17, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -2.3, 0]))
            self.play(FadeIn(note), Flash(e2, color=CHALK_GREEN, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 3: what reversal means ---------------------------------------
    def beat3_reversal(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()

            heading = board_text("Reverse the Digits", 25, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            tens = place_box("Tens", "3", TENS_COLOR)
            ones = place_box("Ones", "5", ONES_COLOR)
            pair = box_pair(tens, ones, cy=0.95)
            self.play(FadeIn(pair, scale=0.9), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(*swap_digits(tens.val, ones.val), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            swapped = board_text("5 is now in the tens place!", 17, CHALK_GREEN,
                                 "BOLD").move_to(np.array([BOARD_CX, -0.05, 0]))
            self.play(FadeIn(swapped), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            e1 = MathTex("53", r"\;=\;", "50+3", font_size=36)
            align_equals(e1, BOARD_CX, -0.95)
            self.play(Write(e1), run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            e2 = MathTex("53", r"\;=\;", r"10\times 5+3", font_size=36)
            align_equals(e2, BOARD_CX, -0.95)
            self.play(TransformMatchingTex(e1, e2),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            note = board_text("Reversing swaps the place values.", 18,
                              CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.9, 0]))
            self.play(FadeOut(swapped), FadeIn(note), Flash(e2, color=CHALK_GREEN,
                                                            flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 4: general form ----------------------------------------------
    def beat4_general(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()

            heading = board_text("Build the Number Algebraically", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            t_box = place_box("Tens", "t", TENS_COLOR, width=1.0, height=1.0,
                              font_size=34)
            u_box = place_box("Ones", "u", ONES_COLOR, width=1.0, height=1.0,
                              font_size=34)
            orig = VGroup(t_box, u_box).arrange(RIGHT, buff=0.4).move_to(
                np.array([-2.55, 1.05, 0]))
            self.play(FadeIn(orig, scale=0.9), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.6))
            self.add_sound(self.sfx["pop"], gain=-13)

            orig_eq = MathTex(r"\text{Original}", "=", "10t+u", font_size=28).move_to(
                np.array([-2.55, 0.05, 0]))
            self.play(Write(orig_eq), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # the mirrored pair: the digits have swapped boxes
            u_box2 = place_box("Tens", "u", ONES_COLOR, width=1.0, height=1.0,
                               font_size=34)
            t_box2 = place_box("Ones", "t", TENS_COLOR, width=1.0, height=1.0,
                               font_size=34)
            rev = VGroup(u_box2, t_box2).arrange(RIGHT, buff=0.4).move_to(
                np.array([2.55, 1.05, 0]))
            rev_eq = MathTex(r"\text{Reversed}", "=", "10u+t", font_size=28).move_to(
                np.array([2.55, 0.05, 0]))
            self.play(FadeIn(rev, scale=0.9), run_time=rt(
                tracker.time_until_bookmark("b2") * 0.5))
            self.play(Write(rev_eq), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            mid = Arrow(np.array([-0.85, 1.05, 0]), np.array([0.85, 1.05, 0]),
                        buff=0.06, color=CHALK_YELLOW, stroke_width=2.6)
            swap_lbl = board_text("swap", 15, CHALK_YELLOW, "BOLD").next_to(
                mid, UP, buff=0.1)
            self.play(GrowArrow(mid), FadeIn(swap_lbl),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            self.play(Indicate(orig_eq, color=CHALK_CYAN, scale_factor=1.0),
                      Indicate(rev_eq, color=CHALK_PINK, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            note = board_text("These two expressions unlock every digit puzzle.",
                              17, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.15, 0]))
            self.play(FadeIn(note), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 5: choose the unknown ----------------------------------------
    def beat5_setup(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            self.reset_board()

            heading = board_text("Choose the Unknown", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            p1 = VGroup(board_text("A two-digit number: digits sum to ", 16),
                        board_text("8", 16, CHALK_YELLOW, "BOLD"),
                        board_text(".", 16)).arrange(RIGHT, buff=0.05)
            p2 = VGroup(board_text("Add ", 16),
                        board_text("18", 16, CHALK_YELLOW, "BOLD"),
                        board_text(" — the digits reverse.", 16)).arrange(
                RIGHT, buff=0.05)
            puzzle = VGroup(p1, p2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX, 2.2, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))
            self.play(FadeIn(puzzle, shift=DOWN * 0.1), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.7))
            self.play(Indicate(p1[1], color=CHALK_YELLOW, scale_factor=1.0),
                      Indicate(p2[1], color=CHALK_YELLOW, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            tens = place_box("Tens (10s)", "?", TENS_COLOR)
            ones = place_box("Ones", "x", ONES_COLOR)
            pair = box_pair(tens, ones, cy=BOX_Y)
            x_note = board_text("let the ones digit be x", 15, ONES_COLOR,
                                "BOLD").next_to(pair, DOWN, buff=0.18)
            self.play(FadeIn(pair, scale=0.9), FadeIn(x_note),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["pop"], gain=-13)

            new_tens = place_box("Tens (10s)", "8-x", TENS_COLOR, font_size=32)
            new_pair = box_pair(new_tens, ones, cy=BOX_Y)
            self.play(Circumscribe(ones.box, color=ONES_COLOR, stroke_width=3),
                      FadeOut(x_note),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.4))
            self.play(ReplacementTransform(pair, new_pair),
                      Flash(new_tens.box, color=TENS_COLOR, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            o_eq = MathTex(r"\text{Original}", "=", "10(8-x)+x", "=", "80-9x",
                           font_size=27).move_to(np.array([BOARD_CX, -0.85, 0]))
            r_eq = MathTex(r"\text{Reversed}", "=", "10x+(8-x)", "=", "9x+8",
                           font_size=27).move_to(np.array([BOARD_CX, -1.75, 0]))
            self.play(Write(o_eq), run_time=rt(tracker.time_until_bookmark("b4") * 0.6))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.play(Write(r_eq), run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 6: form the equation and solve --------------------------------
    def beat6_solve(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("Form the Equation", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            cond = MathTex(r"\text{Original}", "+18", "=", r"\text{Reversed}",
                           font_size=28).move_to(np.array([BOARD_CX, 1.85, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))
            self.play(Write(cond), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            e1 = MathTex("(80-9x)+18", r"\;=\;", "9x+8", font_size=34)
            align_equals(e1, BOARD_CX, 1.0)
            self.play(Write(e1), run_time=rt(tracker.time_until_bookmark("b1") * 0.6))
            e2 = MathTex("98-9x", r"\;=\;", "9x+8", font_size=34)
            align_equals(e2, BOARD_CX, 1.0)
            self.play(TransformMatchingTex(e1, e2),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            e3 = MathTex("90", r"\;=\;", "18x", font_size=34)
            align_equals(e3, BOARD_CX, 1.0)
            self.play(TransformMatchingTex(e2, e3),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            e4 = MathTex("x", r"\;=\;", "5", font_size=38, color=CHALK_GREEN)
            align_equals(e4, BOARD_CX, 1.0)
            self.play(TransformMatchingTex(e3, e4),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            read = VGroup(board_text("ones digit = 5", 17, ONES_COLOR, "BOLD"),
                          board_text("tens digit = 3", 17, TENS_COLOR, "BOLD")
                          ).arrange(RIGHT, buff=0.7).move_to(
                np.array([BOARD_CX, 0.05, 0]))
            self.play(FadeIn(read, shift=UP * 0.1),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.6))
            self.play(Indicate(read, color=CHALK_YELLOW, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.5))
            self.add_sound(self.sfx["click"], gain=-15)

            back = MathTex("10(8-5)+5", r"\;=\;", "35", font_size=34)
            align_equals(back, BOARD_CX, -0.95)
            self.play(Write(back), run_time=rt(tracker.time_until_bookmark("b4") * 0.5))
            box = SurroundingRectangle(back, color=CHALK_GREEN, buff=0.18,
                                       corner_radius=0.1, stroke_width=3)
            self.play(FadeOut(cond), FadeOut(read), Create(box),
                      Flash(back, color=CHALK_GREEN, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 7: check ------------------------------------------------------
    def beat7_check(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("Check the Solution", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            d35 = flip_display("3", "5", TENS_COLOR, ONES_COLOR, size=1.0)
            d53 = flip_display("5", "3", ONES_COLOR, TENS_COLOR, size=1.0)
            pair = VGroup(d35, d53).arrange(RIGHT, buff=1.5).move_to(
                np.array([BOARD_CX, 1.15, 0]))
            ar = Arrow(pair[0].get_right(), pair[1].get_left(), buff=0.1,
                       color=CHALK_YELLOW, stroke_width=2.6)
            plus = board_text("+18", 17, CHALK_YELLOW, "BOLD").next_to(ar, UP, buff=0.08)
            self.play(FadeIn(d35), GrowArrow(ar), FadeIn(plus),
                      FadeIn(d53, shift=RIGHT * 0.2),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            sum_eq = MathTex("3+5", r"\;=\;", "8", font_size=34)
            align_equals(sum_eq, BOARD_CX, -0.15)
            ck1 = tick_beside(sum_eq, CHALK_GREEN, 0.32, 0.3)
            self.play(Write(sum_eq), run_time=rt(tracker.time_until_bookmark("b1") * 0.6))
            self.play(Create(ck1), Flash(sum_eq, color=CHALK_GREEN, flash_radius=0.5),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            plus_eq = MathTex("35+18", r"\;=\;", "53", font_size=34)
            align_equals(plus_eq, BOARD_CX, -1.25)
            ck2 = tick_beside(plus_eq, CHALK_GREEN, 0.32, 0.3)
            self.play(Write(plus_eq), run_time=rt(tracker.time_until_bookmark("b2") * 0.6))
            self.play(Create(ck2), Flash(plus_eq, color=CHALK_GREEN, flash_radius=0.5),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            done = board_text("Both conditions hold: the number is 35.", 18,
                              CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -2.05, 0]))
            self.play(FadeIn(done), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-12)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 8: real-world place value -------------------------------------
    def beat8_realworld(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("Digits Changing Place Changes Value", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            d35 = flip_display("3", "5", TENS_COLOR, ONES_COLOR).move_to(
                np.array([-2.6, 1.15, 0]))
            d53 = flip_display("5", "3", ONES_COLOR, TENS_COLOR).move_to(
                np.array([2.6, 1.15, 0]))
            price1 = board_text("price tag", 14, CHALK_WHITE).next_to(d35, UP, buff=0.12)
            price2 = board_text("digit cards reversed", 14, CHALK_WHITE).next_to(
                d53, UP, buff=0.12)
            self.play(FadeIn(d35), FadeIn(price1),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.6))
            self.play(FadeIn(d53), FadeIn(price2), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            exp1 = MathTex("30+5", font_size=32, color=TENS_COLOR).move_to(
                np.array([-2.6, 0.05, 0]))
            self.play(Write(exp1), run_time=rt(tracker.time_until_bookmark("b1") * 0.6))
            exp2 = MathTex("50+3", font_size=32, color=ONES_COLOR).move_to(
                np.array([2.6, 0.05, 0]))
            self.play(Write(exp2), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            neq = MathTex("35", r"\;\neq\;", "53", font_size=38,
                          color=CHALK_YELLOW).move_to(np.array([BOARD_CX, -0.9, 0]))
            self.play(Write(neq), run_time=rt(tracker.time_until_bookmark("b2") * 0.6))
            self.play(Indicate(exp1, color=TENS_COLOR, scale_factor=1.0),
                      Indicate(exp2, color=ONES_COLOR, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            note = board_text("Same digits. Different value.", 19, CHALK_YELLOW,
                              "BOLD").move_to(np.array([BOARD_CX, -1.85, 0]))
            self.play(FadeIn(note), Flash(note, color=CHALK_YELLOW, flash_radius=0.8),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self.play(Circumscribe(note, color=CHALK_YELLOW, stroke_width=3),
                      run_time=rt(tracker.get_remaining_duration()))
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 9: student challenge -----------------------------------------
    def beat9_challenge(self) -> None:
        with self.voiceover(text=NARRATION["scene9_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", 30, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y - 0.05, 0]))
            p1 = VGroup(board_text("A two-digit number: digits sum to ", 16),
                        board_text("9", 16, CHALK_YELLOW, "BOLD"),
                        board_text(".", 16)).arrange(RIGHT, buff=0.05)
            p2 = VGroup(board_text("Subtract ", 16),
                        board_text("27", 16, CHALK_YELLOW, "BOLD"),
                        board_text(" — the digits reverse.", 16)).arrange(
                RIGHT, buff=0.05)
            puzzle = VGroup(p1, p2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX, 2.2, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.play(FadeIn(puzzle, shift=DOWN * 0.1), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            tens = place_box("Tens (10s)", "?", TENS_COLOR)
            ones = place_box("Ones", "x", ONES_COLOR)
            pair = box_pair(tens, ones, cy=BOX_Y)
            ask = board_text("Let the ones digit be x.", 17, ONES_COLOR, "BOLD").move_to(
                np.array([BOARD_CX, -0.35, 0]))
            pause = board_text("Pause and try it", 19, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.15, 0]))
            self.play(FadeIn(pair, scale=0.9), FadeIn(ask),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            self.play(FadeIn(pause), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(Indicate(pair, color=CHALK_YELLOW, scale_factor=1.03),
                      run_time=rt(tracker.get_remaining_duration()))
            self.challenge = VGroup(heading, puzzle, pair, ask, pause)
            self._capture_srt(tracker)

        play_challenge_countdown(self, seconds=6, sfx=self.sfx)

        with self.voiceover(text=NARRATION["scene9_reveal"]) as tracker:
            pair = self.challenge[2]
            ask = self.challenge[3]
            self.play(FadeOut(self.challenge[4]), FadeOut(ask), run_time=0.3)

            tens_val = MathTex("9-x", font_size=32, color=TENS_COLOR).move_to(
                pair[0].box.get_center())
            rev_eq = MathTex(r"\text{Original}=90-9x", r"\quad", r"\text{Reversed}=9x+9",
                             font_size=25).move_to(np.array([BOARD_CX, -0.35, 0]))
            self.play(ReplacementTransform(pair[0].val, tens_val),
                      FadeIn(rev_eq),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            e1 = MathTex("(90-9x)-27", r"\;=\;", "9x+9", font_size=32)
            align_equals(e1, BOARD_CX, -1.05)
            e2 = MathTex("63-9x", r"\;=\;", "9x+9", font_size=32)
            align_equals(e2, BOARD_CX, -1.05)
            e3 = MathTex("54", r"\;=\;", "18x", font_size=32)
            align_equals(e3, BOARD_CX, -1.05)
            self.play(Write(e1), run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.play(TransformMatchingTex(e1, e2),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(TransformMatchingTex(e2, e3),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            e4 = MathTex("x", r"\;=\;", "3", font_size=36, color=CHALK_GREEN)
            align_equals(e4, BOARD_CX, -1.05)
            self.play(TransformMatchingTex(e3, e4),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            ans = MathTex("63", font_size=44, color=CHALK_GREEN).move_to(
                np.array([BOARD_CX, -1.95, 0]))
            abox = SurroundingRectangle(ans, color=CHALK_GREEN, buff=0.2,
                                        corner_radius=0.1, stroke_width=3)
            label = board_text("the number is", 16, CHALK_GREEN, "BOLD").next_to(
                abox, LEFT, buff=0.25)
            self.play(FadeOut(e4),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.4))
            self.play(FadeIn(ans), Create(abox), FadeIn(label),
                      Flash(ans, color=CHALK_GREEN, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-12)

            well = board_text("Well done — place value built the equation!", 17,
                              CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -2.6, 0]))
            self.play(FadeOut(rev_eq), FadeIn(well),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.6))
            self.play(Flash(well, color=CHALK_YELLOW, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self.play(Indicate(ans, color=CHALK_GREEN, scale_factor=1.08),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 10: summary ---------------------------------------------------
    def beat10_summary(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("Summary", 31, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y - 0.05, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.4))

            chain = MathTex(r"10t+u \;\to\; 10u+t \;\to\; \text{equation} \;\to\; 35",
                            font_size=26, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, 2.35, 0]))
            self.play(Write(chain), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            r1 = summary_row(1, "Tens digit t, ones digit u:", r"10t+u", CHALK_CYAN)
            r2 = summary_row(2, "Reversed number:", r"10u+t", CHALK_PINK)
            r3 = summary_row(3, "Use the digit sum:", r"t+u = S", CHALK_AMBER)
            r4 = summary_row(4, "Solve, then check:", r"35 \to 53", CHALK_GREEN)
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
            take = board_text("Use place value to build the equation.", 22,
                              CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.5, 0]))
            sub = board_text("Original = 10t + u     Reversed = 10u + t", 17,
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

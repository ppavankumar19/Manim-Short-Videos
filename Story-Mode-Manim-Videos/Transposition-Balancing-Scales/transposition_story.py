"""
The Balancing Scales of Transposition — Solving 3x + 5 = 20
Story-mode chalkboard lesson (Telangana Class 8 Maths, Chapter 2: Linear Equations in One Variable).

Production Pipeline:
  - assets/background2.png as a fixed backdrop; all drawings inside board-safe rectangle.
  - assets/students.png / teacher.png in bottom corners, 'CLASS 08' / 'Mathematics' top-right.
  - VoiceoverScene + EdgeSpeechService (en-IN-PrabhatNeural).
  - Computed run_times from real edge-tts per-word bookmarks.
  - Word-boundary accurate SRT export (_write_real_srt()).
  - Sound effects from sound_effects.py, chalk-styled Text/MathTex (font='Segoe Print').
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
    ORIGIN, UP, DOWN, LEFT, RIGHT, UL, UR, DL, DR, PI, TAU, BLACK,
    ImageMobject, MathTex, VGroup, Group, Line, DashedLine, Dot, Circle,
    Polygon, Rectangle, RoundedRectangle, Triangle, Arrow, Sector, Arc,
    Text, Write, FadeIn, FadeOut, Create, Uncreate, Transform,
    ReplacementTransform, FadeTransform, GrowFromCenter, GrowFromPoint,
    GrowArrow, Indicate, Flash, Circumscribe, Wiggle, DrawBorderThenFill,
    LaggedStart, LaggedStartMap, Succession, SpinInFromNothing,
    ShrinkToCenter, ApplyWave, rate_functions, config, MoveAlongPath,
    Square, Ellipse,
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


# Measured chalkboard safe bounds
BOARD_LEFT = -4.6
BOARD_RIGHT = 5.6
BOARD_TOP = 3.3
BOARD_BOTTOM = -2.9
BOARD_CX = (BOARD_LEFT + BOARD_RIGHT) / 2  # 0.5
BOARD_CY = (BOARD_TOP + BOARD_BOTTOM) / 2  # 0.2


def board_text(s: str, size: int = 34, color: str = CHALK_WHITE, weight: str = "NORMAL") -> Text:
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def chalk_math(s: str, size: int = 34, color: str = MATH_COLOR) -> MathTex:
    return MathTex(s, font_size=size, color=color)


def drop_shadow(mobj: VGroup, dx: float = 0.05, dy: float = -0.06, opacity: float = 0.3) -> VGroup:
    shadow = mobj.copy()
    shadow.set_fill(BLACK, opacity=opacity)
    shadow.set_stroke(width=0)
    shadow.shift(np.array([dx, dy, 0]))
    return VGroup(shadow, mobj)


# ----------------------------------------------------------- Characters & Icons -----

def detective_hat(color: str = "#5A3B1E", width: float = 0.8) -> VGroup:
    """A jaunty detective fedora hat with a curved brim, creased crown, and ribbon."""
    brim = RoundedRectangle(corner_radius=0.06, width=width, height=0.12,
                            stroke_color=CHALK_AMBER, stroke_width=1.8,
                            fill_color=color, fill_opacity=0.95)
    crown_w = width * 0.62
    crown_h = 0.32
    crown = RoundedRectangle(corner_radius=0.08, width=crown_w, height=crown_h,
                             stroke_color=CHALK_AMBER, stroke_width=1.8,
                             fill_color=color, fill_opacity=0.95).next_to(brim, UP, buff=-0.02)
    ribbon = RoundedRectangle(corner_radius=0.02, width=crown_w, height=0.07,
                              stroke_width=0, fill_color=CHALK_YELLOW, fill_opacity=0.9).move_to(
        crown.get_bottom() + UP * 0.04)
    # Magnifying glass pin on ribbon
    pin_ring = Circle(radius=0.04, stroke_color=CHALK_WHITE, stroke_width=1.5, fill_opacity=0).move_to(
        ribbon.get_right() + LEFT * 0.08 + UP * 0.02)
    pin_handle = Line(pin_ring.get_center(), pin_ring.get_center() + DR * 0.045,
                      stroke_color=CHALK_WHITE, stroke_width=1.5)
    pin = VGroup(pin_ring, pin_handle)
    hat = VGroup(brim, crown, ribbon, pin)
    hat.rotate(np.radians(-6))
    return hat


def mystery_box_crate(label: str = "x", width: float = 1.05, height: float = 0.95) -> VGroup:
    """Detective Mystery Box x: wooden crate texture + detective hat + chalk x medallion."""
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
    x_lbl = board_text(label, 26, CHALK_CYAN, "BOLD").move_to(badge.get_center())
    medallion = VGroup(badge, x_lbl)

    lid = RoundedRectangle(corner_radius=0.04, width=width * 1.06, height=0.14,
                           stroke_color=CHALK_AMBER, stroke_width=2.2,
                           fill_color=["#6B4424", "#4A2E18"], fill_opacity=0.95).next_to(
        body, UP, buff=-0.04)

    hat = detective_hat(width=width * 0.82).next_to(lid, UP, buff=-0.06)
    lid_hat = VGroup(lid, hat)
    box = VGroup(body, planks, brackets, medallion, lid_hat)
    shadowed = drop_shadow(box, dx=0.05, dy=-0.06, opacity=0.25)
    shadowed.lid_hat = lid_hat
    shadowed.body = body
    return shadowed


def multiplier_badge(label: str = "x3", radius: float = 0.28) -> VGroup:
    """A bright emblem representing x 3 multiplier."""
    bg = Circle(radius=radius, stroke_color=CHALK_YELLOW, stroke_width=2.5,
                fill_color="#3B2A08", fill_opacity=0.9)
    txt = board_text(label, 20, CHALK_YELLOW, "BOLD").move_to(bg.get_center())
    badge = VGroup(bg, txt)
    return drop_shadow(badge, dx=0.03, dy=-0.04, opacity=0.2)


def weight_kettlebell(label: str = "+5", width: float = 0.85, height: float = 0.8) -> VGroup:
    """A solid cast-iron weight labeled +5."""
    body_h = height * 0.72
    body = Polygon(
        np.array([-width * 0.35, -height / 2, 0]),
        np.array([width * 0.35, -height / 2, 0]),
        np.array([width * 0.26, -height / 2 + body_h, 0]),
        np.array([-width * 0.26, -height / 2 + body_h, 0]),
        stroke_color=CHALK_GREEN, stroke_width=2.5,
        fill_color=["#1E293B", "#334155", "#1E293B"], fill_opacity=0.95,
    )
    handle = Arc(radius=width * 0.24, start_angle=0, angle=PI,
                 stroke_color=CHALK_GREEN, stroke_width=3).move_to(
        np.array([0, -height / 2 + body_h + 0.1, 0]))
    lbl = board_text(label, 22, CHALK_WHITE, "BOLD").move_to(body.get_center() + UP * 0.02)
    wt = VGroup(body, handle, lbl)
    return drop_shadow(wt, dx=0.04, dy=-0.05, opacity=0.25)


def balloon_icon(label: str = "-5", radius: float = 0.42) -> VGroup:
    """A floating helium balloon labeled -5 with string."""
    balloon = Circle(radius=radius, stroke_color=CHALK_PINK, stroke_width=2.5)
    balloon.set_fill(color=[CHALK_WHITE, CHALK_PINK, "#9B2C4D"], opacity=0.9)
    knot = Triangle(stroke_color=CHALK_PINK, stroke_width=2,
                    fill_color=CHALK_PINK, fill_opacity=0.9).scale(0.08).next_to(
        balloon, DOWN, buff=-0.03)
    pts = [knot.get_bottom() + DOWN * (i * 0.12) + RIGHT * (0.04 * ((-1)**i)) for i in range(5)]
    string = VGroup(*[
        Line(pts[i], pts[i+1], stroke_color=CHALK_WHITE, stroke_width=1.4, stroke_opacity=0.7)
        for i in range(4)
    ])
    lbl = board_text(label, 22, CHALK_WHITE, "BOLD").move_to(balloon.get_center())
    balloon_grp = VGroup(balloon, knot, string, lbl)
    return drop_shadow(balloon_grp, dx=0.04, dy=-0.05, opacity=0.2)


def coin_stack_pile(count_label: str = "20", width: float = 1.1, height: float = 0.9) -> VGroup:
    """A neat golden coin stack with count label badge."""
    base = RoundedRectangle(corner_radius=0.08, width=width, height=height,
                            stroke_color=CHALK_AMBER, stroke_width=2)
    base.set_fill(color=["#5C4308", "#A87B11", "#D4A017"], opacity=0.9)
    lines = VGroup(*[
        Line(base.get_left() + UP * y + RIGHT * 0.05, base.get_right() + UP * y + LEFT * 0.05,
             stroke_color="#FFF099", stroke_width=1.5, stroke_opacity=0.75)
        for y in np.linspace(-height * 0.35, height * 0.35, 5)
    ])
    badge = RoundedRectangle(corner_radius=0.04, width=0.6, height=0.32,
                            stroke_color=CHALK_WHITE, stroke_width=1.5,
                            fill_color="#2B1E05", fill_opacity=0.85).move_to(base.get_center())
    lbl = board_text(count_label, 20, CHALK_YELLOW, "BOLD").move_to(badge.get_center())
    top_coin = Ellipse(width=width * 0.95, height=0.18, stroke_color=CHALK_WHITE, stroke_width=1.5,
                       fill_color=CHALK_YELLOW, fill_opacity=0.9).next_to(base, UP, buff=-0.08)
    stack = VGroup(base, lines, badge, lbl, top_coin)
    return drop_shadow(stack, dx=0.04, dy=-0.05, opacity=0.25)


def seesaw_scale(beam_w: float = 6.4, pivot_x: float = BOARD_CX, pivot_y: float = -0.7) -> VGroup:
    """Seesaw scale: fulcrum triangle + glowing '=' pivot + balanced beam + trays."""
    base_tri = Triangle(stroke_color=CHALK_AMBER, stroke_width=3,
                        fill_color=["#2B1A0E", "#4A2E18"], fill_opacity=0.95).scale(0.48)
    base_tri.move_to(np.array([pivot_x, pivot_y - 0.38, 0]))

    beam = RoundedRectangle(corner_radius=0.03, width=beam_w, height=0.14,
                            stroke_color=CHALK_AMBER, stroke_width=2.5,
                            fill_color=["#6B4424", "#8A5830"], fill_opacity=0.95).move_to(
        np.array([pivot_x, pivot_y, 0]))

    tray_w = 2.1
    left_tray = RoundedRectangle(corner_radius=0.02, width=tray_w, height=0.08,
                                 stroke_color=CHALK_CYAN, stroke_width=2,
                                 fill_color="#1F3333", fill_opacity=0.9).move_to(
        np.array([pivot_x - beam_w * 0.38, pivot_y + 0.08, 0]))
    right_tray = RoundedRectangle(corner_radius=0.02, width=tray_w, height=0.08,
                                  stroke_color=CHALK_PINK, stroke_width=2,
                                  fill_color="#331F28", fill_opacity=0.9).move_to(
        np.array([pivot_x + beam_w * 0.38, pivot_y + 0.08, 0]))

    pivot_glow = Circle(radius=0.34, stroke_color=CHALK_YELLOW, stroke_width=3,
                        fill_color="#2B1E05", fill_opacity=0.95).move_to(
        np.array([pivot_x, pivot_y, 0]))
    pivot_eq = board_text("=", 34, CHALK_YELLOW, "BOLD").move_to(pivot_glow.get_center())
    pivot = VGroup(pivot_glow, pivot_eq)

    lbl_lhs = board_text("LHS", 16, CHALK_CYAN, "BOLD").next_to(left_tray, DOWN, buff=0.25)
    lbl_rhs = board_text("RHS", 16, CHALK_PINK, "BOLD").next_to(right_tray, DOWN, buff=0.25)

    assembly = VGroup(base_tri, beam, left_tray, right_tray, pivot, lbl_lhs, lbl_rhs)
    return assembly


# ---------------------------------------------------------------- Narration -----
NARRATION = {
    "title": (
        "Today's topic: the balancing scales of transposition!<bookmark mark='b1'/> "
        "We'll discover how moving terms across the equal sign solves linear equations,<bookmark mark='b2'/> "
        "through the power of balanced operations!"
    ),
    "scene1": (
        "An equation is just like a balanced seesaw!<bookmark mark='b1'/> "
        "Whatever sits on the Left-Hand Side equals whatever sits on the Right-Hand Side.<bookmark mark='b2'/> "
        "Here, three mystery boxes, three x, plus a five weight, balance twenty coins.<bookmark mark='b3'/> "
        "Mystery box x says: help me get isolated so I can reveal my true value!<bookmark mark='b4'/>"
    ),
    "scene2": (
        "Rule Number One: when a term crosses the equal sign pivot, it flips its sign!<bookmark mark='b1'/> "
        "Watch the plus five weight slide toward the pivot.<bookmark mark='b2'/> "
        "As it crosses, sparks fly, and it turns into a floating minus five balloon on the right!<bookmark mark='b3'/> "
        "Twenty minus five leaves fifteen.<bookmark mark='b4'/> "
        "Now three x equals fifteen, and the seesaw stays perfectly balanced!"
    ),
    "scene3": (
        "Rule Number Two: a multiplier on one side drops below the line to become a divisor on the other side!<bookmark mark='b1'/> "
        "Mystery box x gently nudges the times three badge across the pivot.<bookmark mark='b2'/> "
        "It drops straight below the fraction line, under fifteen, becoming divided by three.<bookmark mark='b3'/> "
        "Fifteen divided by three gives us five!<bookmark mark='b4'/> "
        "Leaving x all alone on the left!"
    ),
    "scene4": (
        "Now the mystery box pops open!<bookmark mark='b1'/> "
        "Inside is the secret number: five!<bookmark mark='b2'/> "
        "Let's verify: three times five plus five equals fifteen plus five, which is twenty.<bookmark mark='b3'/> "
        "The seesaw balances perfectly: twenty equals twenty!"
    ),
    "scene5": (
        "Remember: transposition is simply reversing operations across the equal sign!<bookmark mark='b1'/> "
        "Addition switches with subtraction,<bookmark mark='b2'/> "
        "and multiplication switches with division.<bookmark mark='b3'/> "
        "Master the pivot, and you can solve any linear equation!<bookmark mark='b4'/> "
        "Thank you so much for watching, and see you in the next lesson!"
    ),
}


class TranspositionStory(VoiceoverScene):
    """Story-mode chalkboard lesson: The Balancing Scales of Transposition."""

    def construct(self) -> None:
        self.set_speech_service(get_speech_service(), create_subcaption=False)
        self.sfx = load_sfx()
        self._srt_entries: list[tuple[float, float, str]] = []

        self.add_background()
        self.beat_title()
        self.beat_scene1_seesaw()
        self.beat_scene2_addition()
        self.beat_scene3_multiplication()
        self.beat_scene4_verification()
        self.beat_scene5_summary()

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

        # Badges top right
        self.add(self._corner_badge("CLASS 08", angle_deg=0, corner="right",
                                     y=BOARD_TOP - 0.16, font_size=11))
        self.add(self._corner_badge("Mathematics", angle_deg=0, corner="right",
                                     y=BOARD_TOP - 0.62, font_size=12, filled=True))

    def _corner_badge(self, text: str, *, angle_deg: float, corner: str,
                       y: float | None = None, font_size: int = 13,
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
        badge.rotate(np.radians(angle_deg))

        yy = BOARD_TOP - 0.32 if y is None else y
        if corner == "left":
            badge.move_to(np.array([BOARD_LEFT + 0.55, yy, 0]))
        else:
            badge.move_to(np.array([BOARD_RIGHT - 0.6, yy, 0]))
            badge.shift(RIGHT * (BOARD_RIGHT - 0.08 - badge.get_right()[0]))
        return badge

    # -- real SRT export -------------------------------------------------
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
        out_dir = _HERE / "media" / "videos" / "transposition_story"
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
        srt_content = "\n".join(lines)
        srt_path.write_text(srt_content, encoding="utf-8")
        print(f"[real SRT written] {srt_path}")
        (out_dir / "real.srt").write_text(srt_content, encoding="utf-8")
        try:
            if hasattr(self, "renderer") and hasattr(self.renderer, "file_writer") and self.renderer.file_writer.movie_file_path:
                movie_dir = Path(self.renderer.file_writer.movie_file_path).parent
                (movie_dir / "real.srt").write_text(srt_content, encoding="utf-8")
                (movie_dir / f"{self.__class__.__name__}.real.srt").write_text(srt_content, encoding="utf-8")
        except Exception:
            pass

    # -- Beat 0: Title -----------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            title = board_text("The Balancing Scales of Transposition", 32, CHALK_WHITE, "BOLD")
            sub = board_text("Solving 3x + 5 = 20", 26, CHALK_YELLOW, "BOLD")
            group = VGroup(title, sub).arrange(DOWN, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY + 0.3, 0]))

            mini_seesaw = seesaw_scale(beam_w=4.2, pivot_x=BOARD_CX, pivot_y=BOARD_CY - 1.1).scale(0.8)

            self.play(Write(title), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(Write(sub), FadeIn(mini_seesaw, shift=UP * 0.2),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-12)

            self.title_group = VGroup(group, mini_seesaw)
            self._capture_srt(tracker)

        self.play(FadeOut(self.title_group))

    # -- Beat 1: Scene 1 — The Balanced Seesaw -----------------------------
    def beat_scene1_seesaw(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            # Header equation
            eq_title = board_text("Linear Equation", 20, CHALK_AMBER, "BOLD")
            eq_math = chalk_math(r"3x + 5 = 20", 36, CHALK_WHITE)
            header = VGroup(eq_title, eq_math).arrange(RIGHT, buff=0.35).move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.5, 0]))

            # Seesaw assembly
            seesaw = seesaw_scale(beam_w=6.4, pivot_x=BOARD_CX, pivot_y=-0.7)

            # Left tray items: Mystery box x + multiplier badge *3 + weight +5
            tray_l_x = BOARD_CX - 6.4 * 0.38  # ~ -1.93
            box_x = mystery_box_crate("x", width=0.95, height=0.88).move_to(
                np.array([tray_l_x - 0.45, -0.05, 0]))
            badge_3 = multiplier_badge("x3", radius=0.25).move_to(
                np.array([tray_l_x + 0.18, 0.25, 0]))
            wt_5 = weight_kettlebell("+5", width=0.75, height=0.72).move_to(
                np.array([tray_l_x + 0.45, -0.22, 0]))

            # Right tray items: 20 coin stack
            tray_r_x = BOARD_CX + 6.4 * 0.38  # ~ 2.93
            coins_20 = coin_stack_pile("20", width=1.1, height=0.85).move_to(
                np.array([tray_r_x, -0.16, 0]))

            # "An equation is just like a balanced seesaw!"
            self.play(Create(seesaw[0]), Create(seesaw[1]), FadeIn(seesaw[2]), FadeIn(seesaw[3]),
                      FadeIn(seesaw[4]), FadeIn(seesaw[5]), FadeIn(seesaw[6]),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            # "Whatever sits on Left equals Right" — equation header appears
            self.play(Write(header), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            # Items drop onto trays
            self.play(
                LaggedStart(
                    FadeIn(box_x, shift=DOWN * 0.3),
                    FadeIn(badge_3, scale=0.5),
                    FadeIn(wt_5, shift=DOWN * 0.3),
                    FadeIn(coins_20, shift=DOWN * 0.3),
                    lag_ratio=0.25,
                ),
                run_time=rt(tracker.time_until_bookmark("b3")),
            )
            self.add_sound(self.sfx["pop"], gain=-13)

            # Detective x dialogue bubble
            bubble = board_text('"Isolate me to find my value!"', 18, CHALK_CYAN).next_to(
                box_x, UP, buff=0.25)
            bubble.shift(RIGHT * min(0, BOARD_CX - 0.2 - bubble.get_right()[0]))
            self.play(FadeIn(bubble, shift=UP * 0.1), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-12)

            self.header = header
            self.eq_math = eq_math
            self.seesaw = seesaw
            self.box_x = box_x
            self.badge_3 = badge_3
            self.wt_5 = wt_5
            self.coins_20 = coins_20
            self.bubble = bubble
            self._capture_srt(tracker)

        self.play(FadeOut(self.bubble))

    # -- Beat 2: Scene 2 — Crossing the Pivot (+ to -) --------------------
    def beat_scene2_addition(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            # Rule 1 Banner
            rule_badge = RoundedRectangle(
                corner_radius=0.04, width=5.2, height=0.42,
                stroke_color=CHALK_GREEN, stroke_width=1.5,
                fill_color="#132B1A", fill_opacity=0.85,
            ).move_to(np.array([BOARD_CX, BOARD_TOP - 1.05, 0]))
            rule_txt = board_text("Rule 1: Addition flips to Subtraction (+a -> -a)", 18, CHALK_GREEN, "BOLD").move_to(
                rule_badge.get_center())
            rule_group = VGroup(rule_badge, rule_txt)

            # "Rule Number One: when a term crosses the equal sign..."
            self.play(FadeIn(rule_group, shift=DOWN * 0.1), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            # "Watch the plus five weight slide toward the pivot."
            pivot_pos = self.seesaw[4].get_center()
            self.play(self.wt_5.animate.move_to(pivot_pos + LEFT * 0.45 + UP * 0.2),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            # "As it crosses, sparks fly, and it turns into a floating minus five balloon on the right!"
            tray_r_x = BOARD_CX + 6.4 * 0.38
            balloon = balloon_icon("-5", radius=0.38).move_to(np.array([tray_r_x + 0.65, 0.45, 0]))

            self.play(
                Flash(pivot_pos, color=CHALK_YELLOW, flash_radius=0.55),
                ReplacementTransform(self.wt_5, balloon),
                run_time=rt(tracker.time_until_bookmark("b3")),
            )
            self.add_sound(self.sfx["ding"], gain=-11)

            # Updated equation: 3x = 20 - 5
            new_eq1 = chalk_math(r"3x = 20 - 5", 36, CHALK_WHITE).move_to(self.eq_math.get_center())
            self.play(ReplacementTransform(self.eq_math, new_eq1), run_time=0.4)
            self.eq_math = new_eq1

            # "Twenty minus five leaves fifteen."
            coins_15 = coin_stack_pile("15", width=1.0, height=0.76).move_to(
                np.array([tray_r_x, -0.19, 0]))

            self.play(
                FadeOut(balloon, shift=DOWN * 0.2),
                ReplacementTransform(self.coins_20, coins_15),
                run_time=rt(tracker.time_until_bookmark("b4")),
            )
            self.add_sound(self.sfx["success"], gain=-12)

            # Updated equation: 3x = 15
            new_eq2 = chalk_math(r"3x = 15", 36, CHALK_CYAN).move_to(self.eq_math.get_center())
            self.play(ReplacementTransform(self.eq_math, new_eq2), run_time=0.35)
            self.eq_math = new_eq2

            # Seesaw re-centers slightly
            self.play(Wiggle(self.seesaw[1], scale_value=1.02, rotation_angle=0.015 * TAU), run_time=0.5)

            self.rule_group = rule_group
            self.coins_15 = coins_15
            self._capture_srt(tracker)

        self.play(FadeOut(self.rule_group))

    # -- Beat 3: Scene 3 — Crossing the Line (* to /) ----------------------
    def beat_scene3_multiplication(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            rule_badge2 = RoundedRectangle(
                corner_radius=0.04, width=5.5, height=0.42,
                stroke_color=CHALK_YELLOW, stroke_width=1.5,
                fill_color="#2B2508", fill_opacity=0.85,
            ).move_to(np.array([BOARD_CX, BOARD_TOP - 1.05, 0]))
            rule_txt2 = board_text("Rule 2: Multiplier drops as Divisor (*a -> /a)", 18, CHALK_YELLOW, "BOLD").move_to(
                rule_badge2.get_center())
            rule_group2 = VGroup(rule_badge2, rule_txt2)

            # "Rule Number Two: a multiplier on one side drops below the line..."
            self.play(FadeIn(rule_group2, shift=DOWN * 0.1), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            # "Mystery box x gently nudges the times three badge across the pivot."
            pivot_pos = self.seesaw[4].get_center()
            self.play(
                self.box_x.animate.shift(LEFT * 0.1),
                self.badge_3.animate.move_to(pivot_pos + UP * 0.3),
                run_time=rt(tracker.time_until_bookmark("b2")),
            )
            self.add_sound(self.sfx["whoosh"], gain=-14)

            # "It drops straight below the fraction line, under fifteen, becoming divided by three."
            tray_r_x = BOARD_CX + 6.4 * 0.38
            frac_line = Line(np.array([tray_r_x - 0.7, -0.42, 0]),
                             np.array([tray_r_x + 0.7, -0.42, 0]),
                             stroke_color=CHALK_WHITE, stroke_width=2.5)
            denom_3 = board_text("3", 24, CHALK_YELLOW, "BOLD").next_to(frac_line, DOWN, buff=0.12)

            # Updated equation: x = 15 / 3
            new_eq = chalk_math(r"x = \frac{15}{3}", 38, CHALK_WHITE).move_to(self.eq_math.get_center())

            self.play(
                Flash(pivot_pos, color=CHALK_YELLOW, flash_radius=0.4),
                Create(frac_line),
                ReplacementTransform(self.badge_3, denom_3),
                ReplacementTransform(self.eq_math, new_eq),
                run_time=rt(tracker.time_until_bookmark("b3")),
            )
            self.add_sound(self.sfx["ding"], gain=-12)
            self.eq_math = new_eq

            # "Fifteen divided by three gives us five!"
            coins_5 = coin_stack_pile("5", width=0.85, height=0.62).move_to(
                np.array([tray_r_x, -0.22, 0]))
            sol_eq = chalk_math(r"x = 5", 40, CHALK_GREEN).move_to(self.eq_math.get_center())

            self.play(
                FadeOut(frac_line),
                FadeOut(denom_3),
                ReplacementTransform(self.coins_15, coins_5),
                ReplacementTransform(self.eq_math, sol_eq),
                run_time=rt(tracker.time_until_bookmark("b4")),
            )
            self.add_sound(self.sfx["success"], gain=-11)
            self.eq_math = sol_eq

            # Box x is now centered on LHS tray
            self.play(self.box_x.animate.move_to(np.array([BOARD_CX - 6.4 * 0.38, -0.05, 0])),
                      run_time=0.4)

            self.rule_group2 = rule_group2
            self.coins_5 = coins_5
            self._capture_srt(tracker)

        self.play(FadeOut(self.rule_group2))

    # -- Beat 4: Scene 4 — Verification & Mystery Unveiled -----------------
    def beat_scene4_verification(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            # "Now the mystery box pops open!"
            self.play(
                self.box_x.lid_hat.animate.shift(UP * 0.42 + LEFT * 0.1).rotate(np.radians(14)),
                run_time=rt(tracker.time_until_bookmark("b1")),
            )
            self.add_sound(self.sfx["pop"], gain=-12)

            # "Inside is the secret number: five!"
            rev_5 = board_text("5", 34, CHALK_YELLOW, "BOLD").move_to(
                self.box_x.body.get_center() + UP * 0.1)

            # Confetti burst
            confetti_pts = [
                self.box_x.body.get_center() + np.array([
                    0.6 * np.cos(a), 0.6 * np.sin(a) + 0.3, 0
                ])
                for a in np.linspace(0, PI, 8)
            ]
            confetti = VGroup(*[
                Dot(p, radius=0.035, color=[CHALK_YELLOW, CHALK_PINK, CHALK_CYAN, CHALK_GREEN][i % 4])
                for i, p in enumerate(confetti_pts)
            ])

            self.play(
                GrowFromCenter(rev_5),
                LaggedStart(*[GrowFromPoint(c, self.box_x.body.get_top()) for c in confetti], lag_ratio=0.1),
                run_time=rt(tracker.time_until_bookmark("b2")),
            )
            self.add_sound(self.sfx["ding"], gain=-10)

            # Verification banner
            verif_card = RoundedRectangle(
                corner_radius=0.06, width=5.6, height=1.1,
                stroke_color=CHALK_GREEN, stroke_width=2,
                fill_color="#112918", fill_opacity=0.92,
            ).move_to(np.array([BOARD_CX, BOARD_TOP - 1.25, 0]))
            verif_title = board_text("Check: Substitute x = 5", 18, CHALK_WHITE, "BOLD").next_to(
                verif_card.get_top(), DOWN, buff=0.12)
            verif_math = chalk_math(r"3(5) + 5 = 15 + 5 = 20", 28, CHALK_YELLOW).next_to(
                verif_title, DOWN, buff=0.1)
            check_mark = board_text("[Balanced!]", 18, CHALK_GREEN, "BOLD").next_to(
                verif_math, RIGHT, buff=0.25)
            verif_group = VGroup(verif_card, verif_title, verif_math, check_mark)

            self.play(
                FadeOut(confetti),
                FadeIn(verif_group, shift=DOWN * 0.15),
                run_time=rt(tracker.time_until_bookmark("b3")),
            )
            self.add_sound(self.sfx["success"], gain=-11)

            # Seesaw balances with a tiny celebratory bounce
            self.play(
                Wiggle(self.seesaw[1], scale_value=1.02, rotation_angle=0.012 * TAU),
                Circumscribe(self.seesaw[4], color=CHALK_YELLOW, stroke_width=3),
                run_time=rt(tracker.get_remaining_duration() * 0.8),
            )

            self.verif_group = verif_group
            self.rev_5 = rev_5
            self._capture_srt(tracker)

        # Clean stage for summary
        self.play(
            FadeOut(self.header),
            FadeOut(self.seesaw),
            FadeOut(self.box_x),
            FadeOut(self.coins_5),
            FadeOut(self.rev_5),
            FadeOut(self.verif_group),
            run_time=0.45,
        )

    # -- Beat 5: Scene 5 — Reversal Rules Summary & Outro ------------------
    def row_rule(self, op1: str, arrow: str, op2: str, label: str, color: str) -> VGroup:
        card = RoundedRectangle(corner_radius=0.05, width=7.0, height=0.55,
                                stroke_color=color, stroke_width=1.5,
                                fill_color="#182333", fill_opacity=0.9)
        sym_group = VGroup(
            chalk_math(op1, 24, color),
            chalk_math(arrow, 20, CHALK_WHITE),
            chalk_math(op2, 24, color),
        ).arrange(RIGHT, buff=0.18)
        sym_group.move_to(card.get_left() + RIGHT * 1.3)

        divider = Line(UP * 0.18, DOWN * 0.18, stroke_color=color, stroke_width=1.2, stroke_opacity=0.5).move_to(
            card.get_left() + RIGHT * 2.35)

        desc = board_text(label, 16, CHALK_WHITE).next_to(divider, RIGHT, buff=0.25)
        return VGroup(card, sym_group, divider, desc)

    def beat_scene5_summary(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            heading = board_text("Transposition: Reversing Operations", 26, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX - 0.4, BOARD_TOP - 0.5, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            # Table of 4 reversal rules
            r1 = self.row_rule(r"+", r"\longleftrightarrow", r"-", "Addition switches with Subtraction", CHALK_GREEN)
            r2 = self.row_rule(r"\times", r"\longleftrightarrow", r"\div", "Multiplication switches with Division", CHALK_YELLOW)
            r3 = self.row_rule(r"LHS", r"\longleftrightarrow", r"RHS", "Pivot fulcrum maintains balance (=)", CHALK_CYAN)

            rows = VGroup(r1, r2, r3).arrange(DOWN, buff=0.22).move_to(
                np.array([BOARD_CX - 0.4, BOARD_CY + 0.1, 0]))

            self.play(FadeIn(r1, shift=RIGHT * 0.15), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(r2, shift=RIGHT * 0.15), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(r3, shift=RIGHT * 0.15), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-12)

            summary_group = VGroup(heading, rows)
            self.play(FadeOut(summary_group), run_time=rt(tracker.get_remaining_duration() * 0.25))

            # Outro
            thanks = board_text("Thank You for Watching!", 42, CHALK_WHITE, "BOLD")
            thanks2 = board_text("See you in the next lesson :)", 26, CHALK_CYAN)
            thanks_group = VGroup(thanks, thanks2).arrange(DOWN, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY, 0]))

            self.play(Write(thanks), run_time=rt(tracker.get_remaining_duration() * 0.6))
            self.add_sound(self.sfx["ding"], gain=-11)
            self.play(FadeIn(thanks2, shift=UP * 0.1), run_time=rt(tracker.get_remaining_duration()))
            self.play(Circumscribe(thanks_group, color=CHALK_AMBER, stroke_width=3, time_width=0.6), run_time=0.6)
            self.add_sound(self.sfx["success"], gain=-11)

            self._capture_srt(tracker)

        self.wait(END_HOLD)

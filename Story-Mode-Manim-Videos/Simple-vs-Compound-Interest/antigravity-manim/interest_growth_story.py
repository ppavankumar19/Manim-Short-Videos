"""
The Tale of Two Coin Piles — Simple Interest vs Compound Interest
Story-mode chalkboard lesson (Telangana Class 8 Maths, Ch. 5, Sections 5.7 & 5.8).

Follows the same production pipeline as density_property_lesson.py:
  - assets/background2.png (empty chalkboard) as a fixed backdrop; every
    drawing stays inside the measured board-safe rectangle.
  - VoiceoverScene + EdgeSpeechService (en-IN-PrabhatNeural), one voice
    reading both narrator lines and the two characters' dialogue.
  - Every animation's run_time is computed from real edge-tts per-word
    timestamps via `<bookmark mark='...'/>` tags + tracker.time_until_bookmark,
    not a guessed fraction of the clip duration.
  - A ground-truth .srt is exported from the same real word-boundary data
    (not manim_voiceover's naive character-count splitter).
  - Sound effects from sound_effects.py, chalk-styled Text/MathTex.

Storyboard (5 scenes, ~120s target):
  1. Initial Deposit — Ramesh & Sreenu both start with P=Rs100 at R=10%.
  2. Year 1 — Twin earnings: both earn Rs10. Ramesh jars it, Sreenu mixes it in.
  3. Year 2 — Interest on interest: Ramesh +Rs10 (jar), Sreenu +Rs11 (10% of 110).
  4. Year 3 — Linear vs exponential: Ramesh Rs130 (straight line), Sreenu Rs133.10 (curve).
  5. Ending takeaway — side-by-side SI line vs CI curve graph.
Plus a short Summary + Thank You closing beat (matches the studio's usual outro).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent.parent.parent
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
FONT = "Segoe Print"
MATH_COLOR = CHALK_WHITE

END_HOLD = 2.2
MIN_RT = 0.12


def rt(seconds: float, floor: float = MIN_RT) -> float:
    return max(floor, float(seconds))


def fmt_money(v: float) -> str:
    if abs(v - round(v)) < 1e-9:
        return f"Rs {int(round(v))}"
    return f"Rs {v:.2f}"


# Safe drawing rectangle inside the chalkboard (same measurement as
# density_property_lesson.py against assets/background2.png).
BOARD_LEFT = -4.6
BOARD_RIGHT = 5.6
BOARD_TOP = 3.3
BOARD_BOTTOM = -2.9
BOARD_CX = (BOARD_LEFT + BOARD_RIGHT) / 2
BOARD_CY = (BOARD_TOP + BOARD_BOTTOM) / 2

LEFT_CX = (BOARD_LEFT + BOARD_CX) / 2 - 0.3
RIGHT_CX = (BOARD_CX + BOARD_RIGHT) / 2 + 0.3
CHEST_Y = BOARD_CY - 0.3


def board_text(s: str, size: int = 34, color: str = CHALK_WHITE, weight: str = "NORMAL") -> Text:
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def chalk_math(s: str, size: int = 34, color: str = MATH_COLOR) -> MathTex:
    return MathTex(s, font_size=size, color=color)


def drop_shadow(mobj: VGroup, dx: float = 0.05, dy: float = -0.06,
                 opacity: float = 0.3) -> VGroup:
    """A soft dark silhouette offset behind `mobj`, giving flat chalk-vector
    icons a sense of depth/weight instead of looking pasted flat on the
    board. Cheap: just the same geometry recoloured solid black."""
    shadow = mobj.copy()
    shadow.set_fill(BLACK, opacity=opacity)
    shadow.set_stroke(width=0)
    shadow.shift(np.array([dx, dy, 0]))
    return VGroup(shadow, mobj)


def coin(pos: np.ndarray, color: str = CHALK_YELLOW, radius: float = 0.13) -> VGroup:
    """A small gold coin: gradient-filled disc (light-struck top edge to a
    darker rim), an inner embossed ring, and a shine streak — reads as an
    actual minted coin instead of a flat dot."""
    disc = Circle(radius=radius, stroke_color="#B8860B", stroke_width=1.5)
    disc.set_fill(color=[CHALK_WHITE, color, "#B8860B"], opacity=1)
    rim = Circle(radius=radius * 0.7, stroke_color="#B8860B", stroke_width=1,
                 stroke_opacity=0.8, fill_opacity=0)
    shine = Line(np.array([-radius * 0.35, radius * 0.25, 0]),
                 np.array([radius * 0.05, radius * 0.55, 0]),
                 stroke_color=CHALK_WHITE, stroke_width=1.4, stroke_opacity=0.85)
    body = VGroup(disc, rim, shine).move_to(pos)
    return drop_shadow(body, dx=0.02, dy=-0.025, opacity=0.22)


def coin_cluster(center: np.ndarray, n: int, color: str = CHALK_YELLOW) -> VGroup:
    n = max(1, min(n, 6))
    pts = []
    for i in range(n):
        ang = 2 * np.pi * i / n
        pts.append(center + np.array([0.16 * np.cos(ang), 0.16 * np.sin(ang), 0]))
    return VGroup(*[coin(p, color) for p in pts])


def chest_icon(color: str = CHALK_AMBER, width: float = 1.5, height: float = 1.0) -> VGroup:
    """A small treasure chest: domed lid + banded body + corner studs + a
    keyhole, instead of a bare rounded rectangle. Wood-grain gradients and a
    drop shadow give it weight instead of a flat cartoon outline."""
    body_h = height * 0.68
    body = RoundedRectangle(corner_radius=0.07, width=width, height=body_h,
                             stroke_color=color, stroke_width=3)
    body.set_fill(color=["#2E1F10", "#5A3B1E", "#7A5330"], opacity=0.85)
    body.move_to(np.array([0, -height / 2 + body_h / 2, 0]))
    # Faint wood-plank streaks across the body.
    grain = VGroup(*[
        Line(body.get_left() + RIGHT * 0.05 + UP * gy, body.get_right() + LEFT * 0.05 + UP * gy,
             stroke_color="#2A1B0E", stroke_width=1, stroke_opacity=0.25)
        for gy in np.linspace(-body_h * 0.32, body_h * 0.32, 3)
    ])

    # A squashed half-disc reads as a shallow domed lid rather than a tall
    # half-circle, keeping the whole chest's footprint close to `height`.
    lid = Sector(radius=width / 2, angle=PI, start_angle=0, stroke_color=color, stroke_width=3)
    lid.set_fill(color=["#8A6238", "#5A3B1E", "#3A2510"], opacity=0.9)
    lid.stretch(0.4, dim=1)
    lid.move_to(np.array([0, body.get_top()[1], 0]), aligned_edge=DOWN)
    # Glossy highlight streak along the top of the dome.
    lid_shine = Line(lid.get_center() + LEFT * width * 0.22 + UP * lid.height * 0.15,
                      lid.get_center() + RIGHT * width * 0.05 + UP * lid.height * 0.35,
                      stroke_color=CHALK_WHITE, stroke_width=2, stroke_opacity=0.35)

    band_top = Line(body.get_corner(UL), body.get_corner(UR),
                     stroke_color=color, stroke_width=2, stroke_opacity=0.8)
    band_top.shift(DOWN * body_h * 0.32)
    band_left = Line(body.get_top() + LEFT * width * 0.28,
                      body.get_bottom() + LEFT * width * 0.28,
                      stroke_color=color, stroke_width=1.5, stroke_opacity=0.6)
    band_right = Line(body.get_top() + RIGHT * width * 0.28,
                       body.get_bottom() + RIGHT * width * 0.28,
                       stroke_color=color, stroke_width=1.5, stroke_opacity=0.6)

    studs = VGroup(*[
        Dot(body.get_corner(c), radius=0.028, color=color, fill_opacity=0.9)
        for c in (UL, UR, DL, DR)
    ])

    keyhole_top = Circle(radius=0.055, stroke_width=0, fill_color=color,
                          fill_opacity=0.85).move_to(np.array([0, body_h * 0.06, 0]))
    keyhole_body = Polygon(
        np.array([-0.035, body_h * 0.02, 0]), np.array([0.035, body_h * 0.02, 0]),
        np.array([0.05, -body_h * 0.16, 0]), np.array([-0.05, -body_h * 0.16, 0]),
        stroke_width=0, fill_color=color, fill_opacity=0.85,
    )
    plate = RoundedRectangle(corner_radius=0.05, width=0.22, height=0.24,
                              stroke_color=color, stroke_width=1.5,
                              fill_color="#2A1D10", fill_opacity=0.7).move_to(
        np.array([0, -body_h * 0.05, 0]))
    keyhole = VGroup(plate, keyhole_top, keyhole_body)

    chest = VGroup(body, grain, lid, lid_shine, band_top, band_left, band_right,
                    studs, keyhole)
    return drop_shadow(chest, dx=0.06, dy=-0.08, opacity=0.25)


def jar_icon(color: str = CHALK_CYAN, width: float = 0.7, height: float = 0.8) -> VGroup:
    """A small glass jar: tapered shoulders, a metal lid, and glass-
    reflection streaks, instead of a bare rectangle. A left-to-right
    gradient plus a drop shadow sell the glassy, three-dimensional look."""
    body = RoundedRectangle(corner_radius=0.1, width=width, height=height * 0.78,
                             stroke_color=color, stroke_width=2.5)
    body.set_fill(color=["#0F2626", "#1B3B3B", "#2A5555"], opacity=0.45)
    body.move_to(np.array([0, -height * 0.11, 0]))

    neck_w = width * 0.5
    shoulder = Polygon(
        body.get_corner(UL), body.get_corner(UR),
        body.get_top() + RIGHT * neck_w / 2, body.get_top() + LEFT * neck_w / 2,
        stroke_color=color, stroke_width=2.5,
        fill_color="#1B3B3B", fill_opacity=0.4,
    )
    lid = RoundedRectangle(corner_radius=0.04, width=neck_w * 1.12, height=0.14,
                            stroke_color=color, stroke_width=2.5)
    lid.set_fill(color=[CHALK_WHITE, color], opacity=0.65)
    lid.move_to(shoulder.get_top() + UP * 0.05)

    gloss = VGroup(*[
        Line(body.get_left() + RIGHT * 0.08 + UP * dy,
             body.get_left() + RIGHT * 0.08 + UP * (dy - 0.14),
             stroke_color=CHALK_WHITE, stroke_width=1, stroke_opacity=0.4)
        for dy in (0.12, -0.06)
    ])
    jar = VGroup(body, shoulder, lid, gloss)
    return drop_shadow(jar, dx=0.035, dy=-0.05, opacity=0.22)


def clock_icon(year_label: str, color: str = CHALK_WHITE) -> VGroup:
    """A small wall clock face with 12/3/6/9 ticks and hour dots, instead of
    a bare circle with two bare hands. A radial gradient + rim highlight +
    drop shadow read as a glass-covered dial rather than a flat outline."""
    face = Circle(radius=0.42, stroke_color=color, stroke_width=3)
    face.set_fill(color=["#3A3A3A", "#1A1A1A", "#000000"], opacity=0.55)
    center = face.get_center()
    # A short bright arc top-left suggests glass catching the light.
    rim_shine = Arc(radius=0.39, start_angle=PI * 0.55, angle=PI * 0.35,
                     stroke_color=CHALK_WHITE, stroke_width=2, stroke_opacity=0.3)
    rim_shine.move_arc_center_to(center)

    major_ticks = VGroup(*[
        Line(center + 0.34 * np.array([np.cos(a), np.sin(a), 0]),
             center + 0.40 * np.array([np.cos(a), np.sin(a), 0]),
             stroke_color=color, stroke_width=2.5)
        for a in (PI / 2, 0, -PI / 2, PI)
    ])
    hour_dots = VGroup(*[
        Dot(center + 0.37 * np.array([np.cos(a), np.sin(a), 0]), radius=0.02,
            color=color, fill_opacity=0.6)
        for a in np.linspace(0, 2 * PI, 12, endpoint=False)
        if not any(abs(a - m) < 0.01 for m in (0, PI / 2, PI, 3 * PI / 2))
    ])
    pin = Dot(center, radius=0.035, color=CHALK_AMBER, fill_opacity=1)
    hour = Line(center, center + 0.19 * np.array([np.cos(PI / 3), np.sin(PI / 3), 0]),
                stroke_color=color, stroke_width=3)
    minute = Line(center, center + 0.30 * np.array([np.cos(-PI / 6), np.sin(-PI / 6), 0]),
                  stroke_color=color, stroke_width=2)
    dial = VGroup(face, rim_shine, major_ticks, hour_dots, hour, minute, pin)
    dial = drop_shadow(dial, dx=0.035, dy=-0.045, opacity=0.25)
    label = board_text(year_label, 20, CHALK_YELLOW, "BOLD").next_to(face, DOWN, buff=0.15)
    return VGroup(dial, label)


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "Today's topic: simple interest versus compound "
        "interest.<bookmark mark='b1'/> We'll learn it through a fun story "
        "about two friends and their two coin chests — the tale of two "
        "coin piles.<bookmark mark='b2'/>"
    ),
    "scene1": (
        "Meet Ramesh and Sreenu!<bookmark mark='b1'/> Both start with a "
        "principal of one hundred rupees<bookmark mark='b2'/> at ten "
        "percent annual interest.<bookmark mark='b3'/> But they have two "
        "completely different ways of growing their money over three "
        "years.<bookmark mark='b4'/> Let's see who builds a bigger "
        "treasure!"
    ),
    "scene2": (
        "At the end of Year One,<bookmark mark='b1'/> both earn ten "
        "percent of one hundred rupees, which is ten "
        "rupees!<bookmark mark='b2'/> Ramesh keeps his interest in a side "
        "jar,<bookmark mark='b3'/> while Sreenu mixes his ten rupees into "
        "his main chest.<bookmark mark='b4'/> Both have one hundred and "
        "ten rupees right now — but watch what happens next!"
    ),
    "scene3": (
        "Year Two arrives.<bookmark mark='b1'/> The bank calculates "
        "Ramesh's interest only on his original one hundred rupees — ten "
        "more coins fall into his jar, taking him to one hundred and "
        "twenty rupees.<bookmark mark='b2'/> But Sreenu's chest now holds "
        "one hundred and ten rupees, so the bank calculates ten percent on "
        "the full one hundred and ten — showering eleven coins in, taking "
        "him to one hundred and twenty one rupees!<bookmark mark='b3'/> "
        "Ramesh asks: why did you get eleven coins when I only got "
        "ten?<bookmark mark='b4'/> Sreenu replies: because my second "
        "year's interest was calculated on my entire one hundred and ten "
        "rupee balance! That one extra rupee is interest earned on my "
        "previous year's interest!"
    ),
    "scene4": (
        "Year Three.<bookmark mark='b1'/> Ramesh receives another flat "
        "batch of ten coins — one hundred, plus ten, plus ten, plus ten, "
        "equals one hundred and thirty rupees. His total builds a "
        "straight, linear bar.<bookmark mark='b2'/> But the bank "
        "calculates ten percent on Sreenu's accumulated one hundred and "
        "twenty one rupees — twelve rupees and ten paise pours in, "
        "pushing his chest to one hundred thirty three rupees and ten "
        "paise!<bookmark mark='b3'/> Sreenu's growth curve bends upward, "
        "exponentially."
    ),
    "formulas": (
        "Let's write down exactly what happened, using your textbook "
        "formulas.<bookmark mark='b1'/> Simple interest: Amount equals "
        "Principal, plus P times T times R, over one "
        "hundred.<bookmark mark='b2'/> For Ramesh: one hundred plus "
        "thirty equals one hundred and thirty rupees.<bookmark "
        "mark='b3'/> Compound interest: Amount equals Principal, times "
        "one plus R over one hundred, raised to the power "
        "n.<bookmark mark='b4'/> For Sreenu: one hundred times one "
        "point one, cubed, equals one hundred thirty three rupees and "
        "ten paise."
    ),
    "scene5": (
        "By Year Three, Ramesh's money grows in a straight "
        "line,<bookmark mark='b1'/> reaching one hundred and thirty "
        "rupees. But Sreenu's money accelerates upward to one hundred "
        "thirty three rupees and ten paise!<bookmark mark='b2'/> That "
        "extra three rupees and ten paise came entirely from letting "
        "interest compound itself over time.<bookmark mark='b3'/> Simple "
        "interest stays constant because the principal never changes. "
        "Compound interest multiplies your wealth because yesterday's "
        "interest becomes today's principal — that is the power of "
        "compounding!"
    ),
    "summary": (
        "Let's recap our tale of two coin piles.<bookmark mark='b1'/> "
        "Ramesh's simple interest adds the same flat amount every single "
        "year, so his wealth climbs in a straight line.<bookmark "
        "mark='b2'/> Sreenu's compound interest adds interest on top of "
        "interest, so his wealth curves upward faster and "
        "faster.<bookmark mark='b3'/> Over a longer time, that difference "
        "only grows bigger and bigger.<bookmark mark='b4'/> Thank you so "
        "much for watching, and I will see you in the next lesson!"
    ),
}


class InterestGrowthStory(VoiceoverScene):
    """Story-mode chalkboard lesson: Simple Interest vs Compound Interest."""

    def construct(self) -> None:
        self.set_speech_service(get_speech_service(), create_subcaption=False)
        self.sfx = load_sfx()
        self._srt_entries: list[tuple[float, float, str]] = []

        self.add_background()
        self.beat_title()
        self.beat_scene1_deposit()
        self.beat_scene2_year1()
        self.beat_scene3_year2()
        self.beat_scene4_year3()
        self.beat_formulas()
        self.beat_scene5_takeaway()
        self.beat_summary()

        self._write_real_srt()

    # -- backdrop --------------------------------------------------------
    def add_background(self) -> None:
        bg = ImageMobject(str(_HERE / "assets" / "background2.png"))
        bg.stretch_to_fit_width(config.frame_width)
        bg.stretch_to_fit_height(config.frame_height)
        bg.set_z_index(-10)
        self.add(bg)

        # Students sitting at their desk in the bottom-left corner of the
        # frame, outside the chalkboard's left edge (board starts at
        # BOARD_LEFT=-4.6), so they never cover any chalk content.
        student = ImageMobject(str(_HERE / "assets" / "students.png"))
        student.set_z_index(-5)
        student.height = 3.3
        student.move_to(np.array([
            -config.frame_width / 2 + student.width / 2 - 0.15,
            -config.frame_height / 2 + student.height / 2 - 0.1,
            0,
        ]))
        self.add(student)

        # Teacher mirrored into the bottom-right corner of the frame,
        # outside the chalkboard's right edge (board ends at
        # BOARD_RIGHT=5.6), so she never covers any chalk content either.
        teacher = ImageMobject(str(_HERE / "assets" / "teacher.png"))
        teacher.set_z_index(-5)
        teacher.height = 3.3
        teacher.move_to(np.array([
            config.frame_width / 2 - teacher.width / 2 + 0.45,
            -config.frame_height / 2 + teacher.height / 2 - 0.1,
            0,
        ]))
        self.add(teacher)

        # Both labels stacked tight in the very top-right corner, just a
        # slight gap from the wooden frame — nothing in the top-left corner.
        self.add(self._corner_badge("CLASS 09", angle_deg=0, corner="right",
                                     y=BOARD_TOP - 0.16, font_size=11))
        self.add(self._corner_badge("Mathematics", angle_deg=0, corner="right",
                                     y=BOARD_TOP - 0.62, font_size=12, filled=True))

    def _corner_badge(self, text: str, *, angle_deg: float, corner: str,
                       y: float | None = None, font_size: int = 13,
                       filled: bool = True) -> VGroup:
        """A small chalk-stamped ribbon tucked in a top corner of the board,
        tilted diagonally like a hand-drawn label. Stays on screen for the
        whole video, clear of the Ramesh/Sreenu name row below it. Right-
        corner badges are right-aligned to a fixed inset so a longer word
        (e.g. "Mathematics") still can't run past the board edge."""
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
        out_dir = _HERE / "media" / "videos" / "interest_growth_story"
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
            # Simple, direct title first (what the lesson actually is),
            # with the story framing as a smaller tagline underneath.
            title = board_text("Simple Interest vs Compound Interest", 34, CHALK_WHITE, "BOLD")
            sub = board_text("The Tale of Two Coin Piles", 24, CHALK_YELLOW, "BOLD")
            group = VGroup(title, sub).arrange(DOWN, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY, 0]))
            coins = coin_cluster(np.array([BOARD_CX, BOARD_CY - 1.4, 0]), 6)

            self.play(Write(title), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(Write(sub), FadeIn(coins, shift=UP * 0.2),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-12)

            self.title_group = VGroup(group, coins)
            self._capture_srt(tracker)

        self.play(FadeOut(self.title_group))

    # -- Beat 1: Scene 1 — Initial Deposit ----------------------------------
    def beat_scene1_deposit(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            names = VGroup(
                board_text("Ramesh", 28, CHALK_CYAN, "BOLD").move_to(
                    np.array([LEFT_CX, BOARD_TOP - 0.4, 0])),
                board_text("Sreenu", 28, CHALK_PINK, "BOLD").move_to(
                    np.array([RIGHT_CX, BOARD_TOP - 0.4, 0])),
            )
            # "Meet Ramesh and Sreenu!" — names appear.
            self.play(LaggedStart(*[Write(n) for n in names], lag_ratio=0.4),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-14)

            divider = Line(np.array([BOARD_CX, BOARD_TOP - 0.7, 0]),
                            np.array([BOARD_CX, BOARD_BOTTOM + 0.3, 0]),
                            stroke_color=CHALK_WHITE, stroke_width=1.5, stroke_opacity=0.35)

            r_chest = chest_icon(CHALK_CYAN).move_to(np.array([LEFT_CX, CHEST_Y, 0]))
            s_chest = chest_icon(CHALK_PINK).move_to(np.array([RIGHT_CX, CHEST_Y, 0]))
            r_amt = board_text("Rs 100", 30, CHALK_CYAN, "BOLD").next_to(r_chest, DOWN, buff=0.25)
            s_amt = board_text("Rs 100", 30, CHALK_PINK, "BOLD").next_to(s_chest, DOWN, buff=0.25)
            r_label = board_text("Principal", 18, CHALK_WHITE).next_to(r_amt, DOWN, buff=0.1)
            s_label = board_text("Principal", 18, CHALK_WHITE).next_to(s_amt, DOWN, buff=0.1)

            # "...principal of one hundred rupees..." — both chests appear.
            self.play(Create(divider),
                      DrawBorderThenFill(r_chest), DrawBorderThenFill(s_chest),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(Write(r_amt), Write(s_amt), FadeIn(r_label), FadeIn(s_label),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.6 + 0.3))

            # Clock's top (face radius 0.42 + tick length) previously reached
            # y=3.37, just past BOARD_TOP=3.3, clipping the wooden frame.
            # Lowered so its top clears the board with margin.
            clock = clock_icon("Year 0").move_to(np.array([BOARD_CX, BOARD_TOP - 0.62, 0]))
            rate = board_text("Rate: 10% per annum", 22, CHALK_AMBER, "BOLD").next_to(
                clock, DOWN, buff=0.55)
            # "...at ten percent annual interest." — clock + rate sign.
            self.play(FadeIn(clock, scale=0.6), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(rate, shift=UP * 0.1), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.ramesh_total = 100.0
            self.ramesh_jar = 0.0
            self.sreenu_total = 100.0
            self.divider = divider
            self.r_chest, self.s_chest = r_chest, s_chest
            self.r_amt, self.s_amt = r_amt, s_amt
            self.names, self.clock, self.rate = names, clock, rate
            self.scene_group = VGroup(r_label, s_label)
            self._capture_srt(tracker)

        self.play(FadeOut(self.scene_group), FadeOut(self.rate))

    # -- Beat 2: Scene 2 — Year 1, twin earnings ----------------------------
    def beat_scene2_year1(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            new_clock = clock_icon("Year 1")
            new_clock.move_to(self.clock.get_center())
            # "At the end of Year One," — clock advances.
            self.play(ReplacementTransform(self.clock, new_clock),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.clock = new_clock
            self.add_sound(self.sfx["click"], gain=-15)

            r_coins = coin_cluster(np.array([LEFT_CX, CHEST_Y + 1.1, 0]), 3, CHALK_YELLOW)
            s_coins = coin_cluster(np.array([RIGHT_CX, CHEST_Y + 1.1, 0]), 3, CHALK_YELLOW)
            # "...both earn ten percent of one hundred rupees, which is ten rupees!"
            self.play(LaggedStart(FadeIn(r_coins, shift=DOWN * 0.3),
                                   FadeIn(s_coins, shift=DOWN * 0.3), lag_ratio=0.3),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["pop"], gain=-14)

            r_jar = jar_icon(CHALK_CYAN).next_to(self.r_chest, RIGHT, buff=0.4)
            # "Ramesh keeps his interest in a side jar," — jar appears, coins drop in.
            self.play(FadeIn(r_jar, shift=UP * 0.2),
                      r_coins.animate.move_to(r_jar.get_center()),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.ramesh_jar = 10.0
            jar_lbl = board_text("Rs 10", 18, CHALK_CYAN).next_to(r_jar, DOWN, buff=0.12)
            self.play(FadeOut(r_coins), FadeIn(jar_lbl), run_time=0.3)

            # "...Sreenu mixes his ten rupees into his main chest." — coins absorbed.
            self.play(s_coins.animate.move_to(self.s_chest.get_center()).scale(0.3),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(FadeOut(s_coins), run_time=0.2)
            self.add_sound(self.sfx["success"], gain=-12)

            self.ramesh_total = 110.0
            self.sreenu_total = 110.0
            new_r_amt = board_text("Rs 110", 30, CHALK_CYAN, "BOLD").move_to(self.r_amt.get_center())
            new_s_amt = board_text("Rs 110", 30, CHALK_PINK, "BOLD").move_to(self.s_amt.get_center())
            self.play(ReplacementTransform(self.r_amt, new_r_amt),
                      ReplacementTransform(self.s_amt, new_s_amt))
            self.r_amt, self.s_amt = new_r_amt, new_s_amt

            self.r_jar, self.jar_lbl = r_jar, jar_lbl
            self._capture_srt(tracker)

    # -- Beat 3: Scene 3 — Year 2, interest on interest ---------------------
    def beat_scene3_year2(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            new_clock = clock_icon("Year 2")
            new_clock.move_to(self.clock.get_center())
            self.play(ReplacementTransform(self.clock, new_clock), run_time=rt(0.5))
            self.clock = new_clock
            self.add_sound(self.sfx["click"], gain=-15)

            r_coins = coin_cluster(np.array([LEFT_CX, CHEST_Y + 1.1, 0]), 3, CHALK_YELLOW)
            # "...ten more coins fall into his jar, taking him to Rs 120."
            self.play(FadeIn(r_coins, shift=DOWN * 0.3),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.4))
            self.play(r_coins.animate.move_to(self.r_jar.get_center()).scale(0.3),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(FadeOut(r_coins), run_time=0.2)
            self.ramesh_jar = 20.0
            self.ramesh_total = 120.0
            new_jar_lbl = board_text("Rs 20", 18, CHALK_CYAN).move_to(self.jar_lbl.get_center())
            new_r_amt = board_text("Rs 120", 30, CHALK_CYAN, "BOLD").move_to(self.r_amt.get_center())
            self.play(ReplacementTransform(self.jar_lbl, new_jar_lbl),
                      ReplacementTransform(self.r_amt, new_r_amt))
            self.jar_lbl, self.r_amt = new_jar_lbl, new_r_amt

            s_coins = coin_cluster(np.array([RIGHT_CX, CHEST_Y + 1.2, 0]), 4, CHALK_AMBER)
            crown_dot = coin(np.array([RIGHT_CX + 0.35, CHEST_Y + 1.2, 0]), CHALK_PINK, 0.09)
            crown_lbl = board_text("interest on interest!", 16, CHALK_PINK, "BOLD").next_to(
                crown_dot, UP, buff=0.12)
            # "...showering eleven coins in, taking him to Rs 121!"
            # [1] reaches past the chest's drop-shadow silhouette (index 0)
            # to the actual chest artwork, so the glow doesn't tint the shadow.
            self.play(self.s_chest[1].animate.set_stroke(color=CHALK_PINK, width=5),
                      FadeIn(s_coins, shift=DOWN * 0.3), FadeIn(crown_dot), FadeIn(crown_lbl),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-12)
            self.play(s_coins.animate.move_to(self.s_chest.get_center()).scale(0.25),
                      crown_dot.animate.move_to(self.s_chest.get_center()),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            self.play(FadeOut(s_coins), FadeOut(crown_dot), FadeOut(crown_lbl),
                      self.s_chest[1].animate.set_stroke(color=CHALK_PINK, width=3),
                      run_time=0.3)
            self.add_sound(self.sfx["success"], gain=-12)
            self.sreenu_total = 121.0
            new_s_amt = board_text("Rs 121", 30, CHALK_PINK, "BOLD").move_to(self.s_amt.get_center())
            self.play(ReplacementTransform(self.s_amt, new_s_amt),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.s_amt = new_s_amt

            # Dialogue: Ramesh asks, Sreenu replies.
            bubble_r = board_text('"Why 11 coins when I got 10?"', 20, CHALK_CYAN).next_to(
                self.r_chest, UP, buff=0.35)
            self.play(FadeIn(bubble_r, shift=UP * 0.1), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["pop"], gain=-13)

            bubble_s = board_text('"Interest earned on my interest!"', 20, CHALK_PINK).next_to(
                self.s_chest, UP, buff=0.35).shift(LEFT * 0.4)
            # Right-aligned inset so this long line never touches the frame,
            # and never crosses left of the middle divider either.
            bubble_s.shift(RIGHT * min(0, BOARD_RIGHT - 0.3 - bubble_s.get_right()[0]))
            bubble_s.shift(RIGHT * max(0, BOARD_CX + 0.3 - bubble_s.get_left()[0]))
            self.play(FadeOut(bubble_r), FadeIn(bubble_s, shift=UP * 0.1),
                      run_time=rt(tracker.get_remaining_duration() * 0.85))
            self.add_sound(self.sfx["ding"], gain=-12)

            self.bubble_s = bubble_s
            self._capture_srt(tracker)

        self.play(FadeOut(self.bubble_s))

    # -- Beat 4: Scene 4 — Year 3, linear vs exponential ---------------------
    def beat_scene4_year3(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            new_clock = clock_icon("Year 3")
            new_clock.move_to(self.clock.get_center())
            self.play(ReplacementTransform(self.clock, new_clock), run_time=rt(0.5))
            self.clock = new_clock
            self.add_sound(self.sfx["click"], gain=-15)

            r_coins = coin_cluster(np.array([LEFT_CX, CHEST_Y + 1.1, 0]), 3, CHALK_YELLOW)
            self.play(FadeIn(r_coins, shift=DOWN * 0.3),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.35))
            self.play(r_coins.animate.move_to(self.r_jar.get_center()).scale(0.3),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.play(FadeOut(r_coins), run_time=0.2)
            self.ramesh_jar = 30.0
            self.ramesh_total = 130.0
            new_jar_lbl = board_text("Rs 30", 18, CHALK_CYAN).move_to(self.jar_lbl.get_center())
            new_r_amt = board_text("Rs 130", 30, CHALK_CYAN, "BOLD").move_to(self.r_amt.get_center())
            # "...equals Rs 130. His total builds a straight, linear bar."
            # Anchored to a fixed baseline (not next_to the chest) so a
            # taller bar (Sreenu's) grows upward and never pushes past the
            # bottom of the board. Heights kept short of the "Rs 130" /
            # "Rs 133.10" amount labels above (around y=-1.03) so the bar
            # top never touches the text.
            bar_base_y = BOARD_BOTTOM + 0.35
            bar_r = Rectangle(width=0.5, height=0.9, stroke_color=CHALK_CYAN, stroke_width=2)
            bar_r.set_fill(color=[CHALK_WHITE, CHALK_CYAN, "#1B7A6E"], opacity=0.75)
            bar_r.move_to(np.array([LEFT_CX, bar_base_y + bar_r.height / 2, 0]))
            self.play(ReplacementTransform(self.jar_lbl, new_jar_lbl),
                      ReplacementTransform(self.r_amt, new_r_amt),
                      GrowFromPoint(bar_r, bar_r.get_bottom()),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.jar_lbl, self.r_amt = new_jar_lbl, new_r_amt
            self.add_sound(self.sfx["success"], gain=-12)

            s_coins = coin_cluster(np.array([RIGHT_CX, CHEST_Y + 1.2, 0]), 5, CHALK_AMBER)
            self.play(FadeIn(s_coins, shift=DOWN * 0.3),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.3))
            self.play(s_coins.animate.move_to(self.s_chest.get_center()).scale(0.25),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.4))
            self.play(FadeOut(s_coins), run_time=0.2)
            self.add_sound(self.sfx["ding"], gain=-12)
            self.sreenu_total = 133.10
            new_s_amt = board_text("Rs 133.10", 30, CHALK_PINK, "BOLD").move_to(self.s_amt.get_center())
            bar_s = Rectangle(width=0.5, height=1.15, stroke_color=CHALK_PINK, stroke_width=2)
            bar_s.set_fill(color=[CHALK_WHITE, CHALK_PINK, "#B03A5A"], opacity=0.75)
            bar_s.move_to(np.array([RIGHT_CX, bar_base_y + bar_s.height / 2, 0]))
            # "...pushing his chest to Rs 133.10! Sreenu's growth curve bends upward, exponentially."
            self.play(ReplacementTransform(self.s_amt, new_s_amt),
                      GrowFromPoint(bar_s, bar_s.get_bottom()),
                      run_time=rt(tracker.get_remaining_duration() * 0.85))
            self.s_amt = new_s_amt
            self.add_sound(self.sfx["success"], gain=-11)

            self.bar_r, self.bar_s = bar_r, bar_s
            self._capture_srt(tracker)

    # -- Beat 4.5: The Formulas -------------------------------------------------
    def beat_formulas(self) -> None:
        with self.voiceover(text=NARRATION["formulas"]) as tracker:
            fade_targets = VGroup(
                self.names, self.clock, self.r_chest, self.s_chest,
                self.r_amt, self.s_amt, self.divider, self.r_jar, self.jar_lbl,
                self.bar_r, self.bar_s,
            )
            self.play(FadeOut(fade_targets), run_time=0.4)

            heading = board_text("The Formulas", 34, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.5, 0]))
            # "Let's write down exactly what happened, using your textbook formulas."
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            divider = Line(np.array([BOARD_CX, BOARD_TOP - 0.9, 0]),
                            np.array([BOARD_CX, BOARD_BOTTOM + 0.3, 0]),
                            stroke_color=CHALK_WHITE, stroke_width=1.5, stroke_opacity=0.3)
            self.play(Create(divider), run_time=0.25)

            si_label = board_text("Simple Interest", 22, CHALK_CYAN, "BOLD")
            si_formula = chalk_math(r"A = P + \frac{PTR}{100}", 26, CHALK_CYAN)
            si_group = VGroup(si_label, si_formula).arrange(DOWN, buff=0.35).move_to(
                np.array([LEFT_CX, BOARD_CY + 0.6, 0]))
            # "Simple interest: Amount equals Principal, plus P T R over one hundred."
            self.play(Write(si_group), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-14)

            si_plug = chalk_math(r"100+30=130", 24, CHALK_CYAN).next_to(si_formula, DOWN, buff=0.4)
            # "For Ramesh: one hundred plus thirty equals one hundred and thirty rupees."
            self.play(Write(si_plug), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-12)

            ci_label = board_text("Compound Interest", 22, CHALK_PINK, "BOLD")
            ci_formula = chalk_math(r"A = P\left(1+\frac{R}{100}\right)^n", 24, CHALK_PINK)
            ci_group = VGroup(ci_label, ci_formula).arrange(DOWN, buff=0.35).move_to(
                np.array([RIGHT_CX, BOARD_CY + 0.6, 0]))
            # "Compound interest: Amount equals Principal times, one plus R over
            # one hundred, raised to the power n."
            self.play(Write(ci_group), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["click"], gain=-14)

            ci_plug = chalk_math(r"100(1.1)^3=133.10", 22, CHALK_PINK).next_to(
                ci_formula, DOWN, buff=0.4)
            # "For Sreenu: one hundred times one point one cubed equals
            # one hundred thirty three rupees and ten paise."
            self.play(Write(ci_plug), run_time=rt(tracker.get_remaining_duration() * 0.85))
            self.add_sound(self.sfx["success"], gain=-11)

            self.formulas_group = VGroup(heading, divider, si_group, si_plug, ci_group, ci_plug)
            self._capture_srt(tracker)

        self.play(FadeOut(self.formulas_group))

    # -- Beat 5: Scene 5 — Ending takeaway (graph comparison) ----------------
    def beat_scene5_takeaway(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            # Graph plot area stops well short of the board's right edge so
            # the "Simple/Compound Interest" tags at the line ends have
            # room to sit fully inside the board without clipping.
            gx0, gx1 = BOARD_LEFT + 1.7, BOARD_RIGHT - 2.6
            gy0, gy1 = BOARD_BOTTOM + 0.6, BOARD_TOP - 0.9
            # Arrows (not bare lines) so both axes carry a proper arrowhead.
            axis_x = Arrow(np.array([gx0, gy0, 0]), np.array([gx1 + 0.3, gy0, 0]),
                           buff=0, color=CHALK_WHITE, stroke_width=3,
                           max_tip_length_to_length_ratio=0.06)
            axis_y = Arrow(np.array([gx0, gy0, 0]), np.array([gx0, gy1 + 0.3, 0]),
                           buff=0, color=CHALK_WHITE, stroke_width=3,
                           max_tip_length_to_length_ratio=0.06)

            def gx(year): return gx0 + (gx1 - gx0) * year / 3.0
            def gy(amount): return gy0 + (gy1 - gy0) * (amount - 100) / 40.0

            # Tick values on both axes, so the graph reads as real data, not
            # just a bare pair of crossing lines.
            x_ticks = VGroup()
            for yv in range(4):
                px = gx(yv)
                tick = Line(np.array([px, gy0 - 0.08, 0]), np.array([px, gy0 + 0.08, 0]),
                            stroke_color=CHALK_WHITE, stroke_width=2)
                lbl = board_text(str(yv), 16, CHALK_WHITE).next_to(
                    np.array([px, gy0, 0]), DOWN, buff=0.2)
                x_ticks.add(tick, lbl)

            y_ticks = VGroup()
            for amt in range(100, 141, 10):
                py = gy(amt)
                tick = Line(np.array([gx0 - 0.08, py, 0]), np.array([gx0 + 0.08, py, 0]),
                            stroke_color=CHALK_WHITE, stroke_width=2)
                lbl = board_text(str(amt), 14, CHALK_WHITE).next_to(
                    np.array([gx0, py, 0]), LEFT, buff=0.15)
                y_ticks.add(tick, lbl)

            x_lbl = board_text("Years", 20, CHALK_WHITE).next_to(x_ticks, DOWN, buff=0.2)
            # Rotated first, *then* next_to'd against the tick labels (not
            # the bare axis) so it clears the numeric y-axis values and
            # lines up with "Years" the same way, at an equal offset.
            y_lbl = board_text("Amount (Rs)", 18, CHALK_WHITE)
            y_lbl.rotate(np.pi / 2)
            y_lbl.next_to(y_ticks, LEFT, buff=0.2)

            si_pts = [np.array([gx(y), gy(100 + 10 * y), 0]) for y in range(4)]
            si_line = VGroup(*[
                Line(si_pts[i], si_pts[i + 1], stroke_color=CHALK_CYAN, stroke_width=4)
                for i in range(3)
            ])
            si_tag = board_text("Simple Interest", 17, CHALK_CYAN, "BOLD")
            si_tag.move_to(si_pts[-1] + RIGHT * 0.15 + DOWN * 0.18, aligned_edge=LEFT)
            # Right-aligned to a fixed inset so the longer "Compound
            # Interest" label below can never run past the board edge,
            # regardless of exactly where the line ends.
            si_tag.shift(RIGHT * min(0, BOARD_RIGHT - 0.15 - si_tag.get_right()[0]))

            ci_vals = [100, 110, 121, 133.10]
            ci_pts = [np.array([gx(y), gy(ci_vals[y]), 0]) for y in range(4)]
            ci_line = VGroup(*[
                Line(ci_pts[i], ci_pts[i + 1], stroke_color=CHALK_PINK, stroke_width=4)
                for i in range(3)
            ])
            ci_tag = board_text("Compound Interest", 17, CHALK_PINK, "BOLD")
            ci_tag.move_to(ci_pts[-1] + RIGHT * 0.15 + UP * 0.18, aligned_edge=LEFT)
            ci_tag.shift(RIGHT * min(0, BOARD_RIGHT - 0.15 - ci_tag.get_right()[0]))

            # "By Year Three, Ramesh's money grows in a straight line," — axes + SI line.
            self.play(GrowArrow(axis_x), GrowArrow(axis_y), FadeIn(x_lbl), FadeIn(y_lbl),
                      FadeIn(x_ticks), FadeIn(y_ticks),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.4))
            self.play(LaggedStart(*[Create(seg) for seg in si_line], lag_ratio=0.3),
                      Write(si_tag), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["swipe"], gain=-15)

            # "...Sreenu's money accelerates upward to Rs 133.10!" — CI curve.
            self.play(LaggedStart(*[Create(seg) for seg in ci_line], lag_ratio=0.3),
                      Write(ci_tag), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-13)
            self.play(Flash(ci_pts[-1], color=CHALK_PINK, flash_radius=0.4),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.4))
            self.add_sound(self.sfx["ding"], gain=-12)

            takeaway = board_text("That's the power of compounding!", 26,
                                   CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.4, 0]))
            self.play(Write(takeaway), run_time=rt(tracker.get_remaining_duration() * 0.7))
            self.add_sound(self.sfx["success"], gain=-11)

            self.graph_group = VGroup(axis_x, axis_y, x_lbl, y_lbl, x_ticks, y_ticks,
                                       si_line, si_tag, ci_line, ci_tag, takeaway)
            self._capture_srt(tracker)

        self.play(FadeOut(self.graph_group))

    # -- Beat 6: Summary + Thank You ---------------------------------------
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
                self.bullet_row(1, ["Ramesh's simple interest adds the same flat amount",
                                     "every year, so his wealth climbs in a straight line."],
                                 color=CHALK_CYAN),
                self.bullet_row(2, ["Sreenu's compound interest adds interest on top of",
                                     "interest, so his wealth curves upward faster and faster."],
                                 color=CHALK_PINK),
                self.bullet_row(3, ["Over a longer time, that gap only grows",
                                     "bigger and bigger."], color=CHALK_YELLOW),
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

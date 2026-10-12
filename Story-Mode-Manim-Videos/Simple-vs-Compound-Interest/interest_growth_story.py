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

All money figures are computed once from PRINCIPAL/RATE below (not typed
as literal strings scattered through the scene code), so changing those
two constants updates every diagram, dialogue amount, and formula plug-in
consistently.

Storyboard (5 scenes, ~120s target):
  1. Initial Deposit — Ramesh & Srinu both start with P=Rs500 at R=20%.
  2. Year 1 — Twin earnings: both earn the same interest. Ramesh jars it,
     Srinu mixes it into his chest.
  3. Year 2 — Interest on interest: Ramesh's jar grows by a flat amount;
     Srinu's chest earns interest on his larger balance.
  4. Year 3 — Linear vs exponential: a shared mini line-graph (not bars)
     shows the two trends diverging.
  5. Ending takeaway — the same two curves stretched out to 20 years, to
     show how dramatically compounding pulls ahead over the long run.
Plus a short Summary + Thank You closing beat (matches the studio's usual outro).
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
FONT = "Segoe Print"
MATH_COLOR = CHALK_WHITE

END_HOLD = 2.2
MIN_RT = 0.12


def rt(seconds: float, floor: float = MIN_RT) -> float:
    return max(floor, float(seconds))


# ------------------------------------------------------------- the numbers --
# Change these two and every diagram/dialogue/formula below recomputes.
PRINCIPAL = 500.0
RATE = 20.0  # percent per annum


def si_amount(years: float) -> float:
    """Simple interest amount after `years`: A = P + PTR/100."""
    return PRINCIPAL + PRINCIPAL * years * RATE / 100


def ci_amount(years: float) -> float:
    """Compound interest amount after `years`: A = P(1+R/100)^n."""
    return PRINCIPAL * (1 + RATE / 100) ** years


def jar_amount(years: float) -> float:
    """Ramesh's side-jar total after `years` (just the flat interest)."""
    return PRINCIPAL * RATE / 100 * years


def fmt_money(v: float) -> str:
    if abs(v - round(v)) < 1e-6:
        return f"Rs {int(round(v)):,}"
    return f"Rs {v:,.2f}"


def fmt_int(v: float) -> str:
    return f"{int(round(v)):,}"


SI1, SI2, SI3 = si_amount(1), si_amount(2), si_amount(3)
CI1, CI2, CI3 = ci_amount(1), ci_amount(2), ci_amount(3)
JAR1, JAR2, JAR3 = jar_amount(1), jar_amount(2), jar_amount(3)
YEAR2_INTEREST = CI2 - CI1  # actual rupees credited to Srinu in year 2
YEAR3_INTEREST = CI3 - CI2  # actual rupees credited to Srinu in year 3
BONUS_YEAR2 = CI2 - SI2     # "interest on interest" bonus, year 2

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
CHEST_Y = BOARD_CY - 0.1


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


def trend_icon(kind: str, color: str, label: str) -> VGroup:
    """A tiny "at a glance" mini-graph — a straight trend for `kind="linear"`
    or an accelerating curve for `kind="curve"` — used as a quick visual
    preview at the very start of the video, before the title itself."""
    box = RoundedRectangle(corner_radius=0.08, width=1.5, height=1.15,
                            stroke_color=color, stroke_width=2,
                            fill_color="#10241c", fill_opacity=0.55)
    origin = box.get_corner(DL) + RIGHT * 0.2 + UP * 0.18
    x_end = box.get_corner(DR) + LEFT * 0.15 + UP * 0.18
    y_end = box.get_corner(UL) + RIGHT * 0.2 + DOWN * 0.15
    axis_x = Line(origin, x_end, stroke_color=CHALK_WHITE, stroke_width=1.5)
    axis_y = Line(origin, y_end, stroke_color=CHALK_WHITE, stroke_width=1.5)

    n = 6
    if kind == "linear":
        pts = [origin + (x_end - origin) * (i / n) + (y_end - origin) * 0.75 * (i / n)
               for i in range(n + 1)]
    else:
        pts = [origin + (x_end - origin) * (i / n) + (y_end - origin) * 0.9 * (i / n) ** 2.2
               for i in range(n + 1)]
    trend = VGroup(*[
        Line(pts[i], pts[i + 1], stroke_color=color, stroke_width=3)
        for i in range(n)
    ])

    lbl = board_text(label, 18, color, "BOLD").next_to(box, DOWN, buff=0.12)
    return VGroup(box, axis_x, axis_y, trend, lbl)


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "Take a quick look at these two lines.<bookmark mark='b0'/> One "
        "grows steadily in a straight line, while the other curves upward, "
        "faster and faster, the longer it grows.<bookmark mark='b0b'/> "
        "This is today's topic: simple interest, versus compound "
        "interest.<bookmark mark='b1'/> We'll learn it through a fun story "
        "about two friends and their two coin chests — the tale of two "
        "coin piles.<bookmark mark='b2'/>"
    ),
    "scene1": (
        "Meet Ramesh and Srinu!<bookmark mark='b1'/> Both start with a "
        f"principal of<bookmark mark='b1b'/> {fmt_int(PRINCIPAL)} "
        "rupees<bookmark mark='b2'/> at<bookmark mark='b2b'/> "
        f"{fmt_int(RATE)} percent annual interest.<bookmark mark='b3'/> But "
        "they have two completely different ways of growing their money "
        "over three years.<bookmark mark='b4'/> Let's see who builds a "
        "bigger treasure!"
    ),
    "scene2": (
        "At the end of Year One,<bookmark mark='b1'/> both earn "
        f"{fmt_int(RATE)} percent of {fmt_int(PRINCIPAL)} rupees, which is "
        f"{fmt_int(JAR1)} rupees!<bookmark mark='b2'/> Ramesh keeps his "
        "interest in a side jar,<bookmark mark='b3'/> while Srinu mixes "
        f"his {fmt_int(JAR1)} rupees into his main chest.<bookmark "
        f"mark='b4'/> Both have {fmt_int(SI1)} rupees right now — but "
        "watch what happens next!"
    ),
    "scene3": (
        "Year Two arrives.<bookmark mark='b1'/> The bank calculates "
        f"Ramesh's interest only on his original {fmt_int(PRINCIPAL)} "
        f"rupees — another {fmt_int(JAR2 - JAR1)} rupees falls into his "
        f"jar, taking him to {fmt_int(SI2)} rupees.<bookmark mark='b2'/> "
        f"But Srinu's chest now holds {fmt_int(SI1)} rupees, so the bank "
        f"calculates {fmt_int(RATE)} percent on the full {fmt_int(CI1)} — "
        f"showering {fmt_int(YEAR2_INTEREST)} rupees in, taking him to "
        f"{fmt_int(CI2)} rupees!<bookmark mark='b3'/> Ramesh asks: why did "
        f"you get {fmt_int(YEAR2_INTEREST)} rupees when I only got "
        f"{fmt_int(JAR2 - JAR1)}?<bookmark mark='b4'/> Srinu replies: "
        "because my second year's interest was calculated on my entire "
        f"{fmt_int(CI1)} rupee balance! Those extra {fmt_int(BONUS_YEAR2)} "
        "rupees are interest earned on my previous year's interest!"
    ),
    "scene4": (
        "Year Three.<bookmark mark='b1'/> Ramesh receives another flat "
        f"{fmt_int(JAR2 - JAR1)} rupees — {fmt_int(PRINCIPAL)}, plus "
        f"{fmt_int(JAR1)}, plus {fmt_int(JAR1)}, plus {fmt_int(JAR1)}, "
        f"equals {fmt_int(SI3)} rupees. His total builds a straight, "
        "linear line.<bookmark mark='b2'/> But the bank calculates "
        f"{fmt_int(RATE)} percent on Srinu's accumulated {fmt_int(CI2)} "
        f"rupees — {fmt_int(YEAR3_INTEREST)} rupees pours in, pushing his "
        f"chest to {fmt_int(CI3)} rupees!<bookmark mark='b3'/> Srinu's "
        "growth curve bends upward, exponentially."
    ),
    "formulas": (
        "Let's write down exactly what happened, using your textbook "
        "formulas.<bookmark mark='b1'/> Here, A stands for Amount, the "
        "final total you end up with. P stands for Principal, the money "
        "you start with. T and n both stand for Time, in years. And R "
        "stands for Rate, the percent interest charged per "
        "year.<bookmark mark='b2'/> "
        "Simple interest: Amount equals Principal, plus P times T times "
        "R, over one hundred.<bookmark mark='b3'/> For Ramesh, that's "
        f"{fmt_int(PRINCIPAL)} plus {fmt_int(PRINCIPAL * 3 * RATE / 100)}, "
        f"equals {fmt_int(SI3)} rupees.<bookmark mark='b4'/> Compound "
        "interest: Amount equals Principal, times one plus R over one "
        "hundred, raised to the power n.<bookmark mark='b5'/> For Srinu, "
        f"that's {fmt_int(PRINCIPAL)} times {1 + RATE / 100:.1f}, cubed, "
        f"equals {fmt_int(CI3)} rupees."
    ),
    "scene5": (
        "Now let's zoom out, to twenty years, to see the real power of "
        "compounding.<bookmark mark='b1'/> Over twenty years, Ramesh's "
        "simple interest crawls up in a straight line, reaching only "
        f"{fmt_int(si_amount(20))} rupees.<bookmark mark='b2'/> But "
        "Srinu's compound interest rockets upward, reaching nearly "
        f"{fmt_int(ci_amount(20))} rupees!<bookmark mark='b3'/> Look at "
        "that massive gap — that difference came entirely from letting "
        "interest compound itself, year after year.<bookmark mark='b4'/> "
        "Simple interest stays constant because the principal never "
        "changes. Compound interest multiplies your wealth because "
        "yesterday's interest becomes today's principal — that is the "
        "power of compounding!"
    ),
    "summary": (
        "Let's recap our tale of two coin piles.<bookmark mark='b1'/> "
        "Ramesh's simple interest adds the same flat amount every single "
        "year, so his wealth climbs in a straight line.<bookmark "
        "mark='b2'/> Srinu's compound interest adds interest on top of "
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

        # Only the subject label, tucked in the very top-right corner, just
        # a slight gap from the wooden frame — no class badge, nothing in
        # the top-left corner.
        self.add(self._corner_badge("Mathematics", angle_deg=0, corner="right",
                                     y=BOARD_TOP - 0.16, font_size=12, filled=True))

    def _corner_badge(self, text: str, *, angle_deg: float, corner: str,
                       y: float | None = None, font_size: int = 13,
                       filled: bool = True) -> VGroup:
        """A small chalk-stamped ribbon tucked in a top corner of the board,
        tilted diagonally like a hand-drawn label. Stays on screen for the
        whole video, clear of the Ramesh/Srinu name row below it. Right-
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
        srt_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"[real SRT written] {srt_path}")

    # -- Beat 0: Title -----------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            # A quick "at a glance" preview of the two trend shapes — shown
            # and explained *before* the title itself, so the video doesn't
            # open on an empty board while the narrator sets the scene.
            si_icon = trend_icon("linear", CHALK_CYAN, "Simple Interest")
            ci_icon = trend_icon("curve", CHALK_PINK, "Compound Interest")
            icons = VGroup(si_icon, ci_icon).arrange(RIGHT, buff=0.9).move_to(
                np.array([BOARD_CX, BOARD_CY, 0]))

            # "Take a quick look:" — icons appear.
            self.play(LaggedStart(FadeIn(si_icon, shift=UP * 0.15),
                                   FadeIn(ci_icon, shift=UP * 0.15), lag_ratio=0.3),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            # "...one grows in a straight line, the other curves upward
            # faster and faster." — the two trend strokes draw themselves.
            self.play(LaggedStart(*[Create(seg) for seg in si_icon[3]], lag_ratio=0.15),
                      LaggedStart(*[Create(seg) for seg in ci_icon[3]], lag_ratio=0.15),
                      run_time=rt(tracker.time_until_bookmark("b0b")))
            self.add_sound(self.sfx["swipe"], gain=-14)

            self.icons_group = icons

            # Simple, direct title next (what the lesson actually is), with
            # the story framing as a smaller tagline underneath.
            title = board_text("Simple Interest vs Compound Interest", 34, CHALK_WHITE, "BOLD")
            sub = board_text("The Tale of Two Coin Piles", 24, CHALK_YELLOW, "BOLD")
            group = VGroup(title, sub).arrange(DOWN, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY, 0]))
            coins = coin_cluster(np.array([BOARD_CX, BOARD_CY - 1.4, 0]), 6)

            # "Today's topic: simple interest versus compound interest." —
            # icons swapped out for the actual title text.
            self.play(FadeOut(icons), Write(title), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-12)
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
                board_text("Srinu", 28, CHALK_PINK, "BOLD").move_to(
                    np.array([RIGHT_CX, BOARD_TOP - 0.4, 0])),
            )
            # "Meet Ramesh and Srinu!" — names appear.
            self.play(LaggedStart(*[Write(n) for n in names], lag_ratio=0.4),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-14)

            divider = Line(np.array([BOARD_CX, BOARD_TOP - 0.7, 0]),
                            np.array([BOARD_CX, BOARD_BOTTOM + 0.3, 0]),
                            stroke_color=CHALK_WHITE, stroke_width=1.5, stroke_opacity=0.35)

            r_chest = chest_icon(CHALK_CYAN).move_to(np.array([LEFT_CX, CHEST_Y, 0]))
            s_chest = chest_icon(CHALK_PINK).move_to(np.array([RIGHT_CX, CHEST_Y, 0]))
            r_amt = board_text(fmt_money(PRINCIPAL), 30, CHALK_CYAN, "BOLD").next_to(
                r_chest, DOWN, buff=0.25)
            s_amt = board_text(fmt_money(PRINCIPAL), 30, CHALK_PINK, "BOLD").next_to(
                s_chest, DOWN, buff=0.25)
            r_label = board_text("Principal", 18, CHALK_WHITE).next_to(r_amt, DOWN, buff=0.1)
            s_label = board_text("Principal", 18, CHALK_WHITE).next_to(s_amt, DOWN, buff=0.1)

            # "...principal of..." — empty chests appear first, drawn while
            # the narrator sets up the sentence, finishing right as "of" is
            # said — *before* the number itself is spoken.
            self.play(Create(divider),
                      DrawBorderThenFill(r_chest), DrawBorderThenFill(s_chest),
                      run_time=rt(tracker.time_until_bookmark("b1b")))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            # "...500 rupees..." — the amount now writes in over the real
            # span it takes to say "500 rupees" (was previously squeezed
            # into a near-zero leftover sliver from the reused bookmark,
            # so the number used to just snap in instead of animating in
            # sync with the narration).
            self.play(Write(r_amt), Write(s_amt), FadeIn(r_label), FadeIn(s_label),
                      run_time=rt(tracker.time_until_bookmark("b2")))

            # Clock's top (face radius 0.42 + tick length) previously reached
            # y=3.37, just past BOARD_TOP=3.3, clipping the wooden frame.
            # Lowered so its top clears the board with margin.
            clock = clock_icon("Year 0").move_to(np.array([BOARD_CX, BOARD_TOP - 0.62, 0]))
            rate = board_text(f"Rate: {fmt_int(RATE)}% per annum", 22, CHALK_AMBER,
                               "BOLD").next_to(clock, DOWN, buff=0.55)
            # "at" — clock appears first (brief).
            self.play(FadeIn(clock, scale=0.6), run_time=rt(tracker.time_until_bookmark("b2b")))
            self.add_sound(self.sfx["click"], gain=-15)
            # "...20 percent annual interest." — the rate sign now lands
            # exactly on this phrase (previously it was keyed to the next,
            # unrelated sentence, so it only finished appearing well after
            # "20 percent" had already been said).
            self.play(FadeIn(rate, shift=UP * 0.1), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.ramesh_total = PRINCIPAL
            self.ramesh_jar = 0.0
            self.sreenu_total = PRINCIPAL
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
            # "...both earn 20 percent of 500 rupees, which is 100 rupees!"
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
            self.ramesh_jar = JAR1
            jar_lbl = board_text(fmt_money(JAR1), 18, CHALK_CYAN).next_to(r_jar, DOWN, buff=0.12)
            self.play(FadeOut(r_coins), FadeIn(jar_lbl), run_time=0.3)

            # "...Srinu mixes his 100 rupees into his main chest." — coins absorbed.
            self.play(s_coins.animate.move_to(self.s_chest.get_center()).scale(0.3),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(FadeOut(s_coins), run_time=0.2)
            self.add_sound(self.sfx["success"], gain=-12)

            self.ramesh_total = SI1
            self.sreenu_total = CI1
            # Ramesh's CHEST amount stays "Rs 500" forever — the principal
            # never changes for simple interest, that's the whole point of
            # keeping the interest in a *separate* jar. Only Srinu's chest
            # (which mixes interest back in) updates. A new "Total" line
            # below the jar shows the combined figure the narration speaks.
            new_s_amt = board_text(fmt_money(CI1), 30, CHALK_PINK, "BOLD").move_to(
                self.s_amt.get_center())
            total_lbl = board_text(f"Total: {fmt_money(SI1)}", 16, CHALK_CYAN, "BOLD")
            total_lbl.next_to(VGroup(self.r_amt, jar_lbl), DOWN, buff=0.15)
            self.play(FadeIn(total_lbl, shift=UP * 0.1),
                      ReplacementTransform(self.s_amt, new_s_amt))
            self.s_amt = new_s_amt

            self.r_jar, self.jar_lbl, self.total_lbl = r_jar, jar_lbl, total_lbl
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
            # "...another 100 rupees falls into his jar, taking him to 700."
            self.play(FadeIn(r_coins, shift=DOWN * 0.3),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.4))
            self.play(r_coins.animate.move_to(self.r_jar.get_center()).scale(0.3),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(FadeOut(r_coins), run_time=0.2)
            self.ramesh_jar = JAR2
            self.ramesh_total = SI2
            # Chest stays "Rs 500" — only the jar and the separate "Total"
            # line change.
            new_jar_lbl = board_text(fmt_money(JAR2), 18, CHALK_CYAN).move_to(
                self.jar_lbl.get_center())
            new_total_lbl = board_text(f"Total: {fmt_money(SI2)}", 16, CHALK_CYAN,
                                        "BOLD").move_to(self.total_lbl.get_center())
            self.play(ReplacementTransform(self.jar_lbl, new_jar_lbl),
                      ReplacementTransform(self.total_lbl, new_total_lbl))
            self.jar_lbl, self.total_lbl = new_jar_lbl, new_total_lbl

            s_coins = coin_cluster(np.array([RIGHT_CX, CHEST_Y + 1.2, 0]), 4, CHALK_AMBER)
            # Raised clear of the coin cluster above (was buff=0.12 right on
            # top of the coins) so the label never overlaps them.
            crown_dot = coin(np.array([RIGHT_CX + 0.35, CHEST_Y + 1.55, 0]), CHALK_PINK, 0.09)
            crown_lbl = board_text("interest on interest!", 16, CHALK_PINK, "BOLD").next_to(
                crown_dot, UP, buff=0.15)
            # "...showering 120 rupees in, taking him to 720!"
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
            self.sreenu_total = CI2
            new_s_amt = board_text(fmt_money(CI2), 30, CHALK_PINK, "BOLD").move_to(
                self.s_amt.get_center())
            self.play(ReplacementTransform(self.s_amt, new_s_amt),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.s_amt = new_s_amt

            # Dialogue: Ramesh asks, Srinu replies.
            bubble_r = board_text(
                f'"Why {fmt_int(YEAR2_INTEREST)} when I got {fmt_int(JAR2 - JAR1)}?"',
                20, CHALK_CYAN).next_to(self.r_chest, UP, buff=0.35)
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
            self.ramesh_jar = JAR3
            self.ramesh_total = SI3
            # Chest still frozen at "Rs 500" — the whole point of the jar.
            new_jar_lbl = board_text(fmt_money(JAR3), 18, CHALK_CYAN).move_to(
                self.jar_lbl.get_center())
            new_total_lbl = board_text(f"Total: {fmt_money(SI3)}", 16, CHALK_CYAN,
                                        "BOLD").move_to(self.total_lbl.get_center())
            self.play(ReplacementTransform(self.jar_lbl, new_jar_lbl),
                      ReplacementTransform(self.total_lbl, new_total_lbl),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.jar_lbl, self.total_lbl = new_jar_lbl, new_total_lbl
            self.add_sound(self.sfx["success"], gain=-12)

            s_coins = coin_cluster(np.array([RIGHT_CX, CHEST_Y + 1.2, 0]), 5, CHALK_AMBER)
            self.play(FadeIn(s_coins, shift=DOWN * 0.3),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.3))
            self.play(s_coins.animate.move_to(self.s_chest.get_center()).scale(0.25),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.4))
            self.play(FadeOut(s_coins), run_time=0.2)
            self.add_sound(self.sfx["ding"], gain=-12)
            self.sreenu_total = CI3
            new_s_amt = board_text(fmt_money(CI3), 30, CHALK_PINK, "BOLD").move_to(
                self.s_amt.get_center())
            self.play(ReplacementTransform(self.s_amt, new_s_amt),
                      run_time=rt(tracker.get_remaining_duration() * 0.45))
            self.s_amt = new_s_amt
            self.add_sound(self.sfx["success"], gain=-11)

            # Two separate small graphs (not one shared/overlapping plot) —
            # one under Ramesh, one under Srinu — each with real numeric
            # tick values on both axes, on the same Rs scale so their
            # steepness is directly comparable.
            y_max = (int(CI3 // 100) + 2) * 100  # round ceiling above CI3
            r_graph, r_pts = self._mini_graph(
                LEFT_CX, [PRINCIPAL, SI1, SI2, SI3], CHALK_CYAN, y_max,
                y_shift=-0.08)
            s_graph, s_pts = self._mini_graph(
                RIGHT_CX, [PRINCIPAL, CI1, CI2, CI3], CHALK_PINK, y_max)

            # Sequential, not simultaneous — Ramesh's graph appears and
            # draws itself completely first, then Srinu's does the same.
            # By this point in the beat almost all of the narration's
            # bookmarked content has already played, so `get_remaining_
            # duration()` is tiny and squeezed both graphs in almost
            # instantly — fixed, generous durations instead, so each one
            # is actually visible on its own before the next starts.
            self.play(FadeIn(r_graph[0]), run_time=0.5)
            self.play(LaggedStart(*[Create(s) for s in r_graph[1]], lag_ratio=0.3),
                      run_time=1.1)
            self.add_sound(self.sfx["swipe"], gain=-14)
            self.wait(0.4)

            self.play(FadeIn(s_graph[0]), run_time=0.5)
            self.play(LaggedStart(*[Create(s) for s in s_graph[1]], lag_ratio=0.3),
                      run_time=1.1)
            self.add_sound(self.sfx["swipe"], gain=-14)

            self.mini_graph = VGroup(r_graph, s_graph)
            self._capture_srt(tracker)

        # A beat to actually look at the finished graphs before the next
        # scene's fade-out sweeps them away — previously the formulas beat
        # started fading these out the instant its own narration began,
        # so the graphs were barely visible before vanishing.
        self.wait(1.3)

    def _mini_graph(self, cx: float, values: list[float], color: str,
                     y_max: float, y_shift: float = 0.0
                     ) -> tuple[VGroup, list[np.ndarray]]:
        """A small years-0-to-3 line graph centred at x=cx, with numeric
        tick values on both axes. Returns (axes+ticks+labels, line-segments)
        as two separate VGroups so the axes can appear before the line
        animates in, plus the raw data points. `y_shift` nudges this one
        graph up/down independently of the other (e.g. Ramesh's sits
        slightly lower than Srinu's, per user request)."""
        gx0, gx1 = cx - 1.15, cx + 1.15
        gy0, gy1 = (BOARD_BOTTOM + 0.65 + y_shift, BOARD_BOTTOM + 1.75 + y_shift)

        axis_x = Arrow(np.array([gx0, gy0, 0]), np.array([gx1 + 0.2, gy0, 0]),
                       buff=0, color=CHALK_WHITE, stroke_width=2,
                       max_tip_length_to_length_ratio=0.06)
        axis_y = Arrow(np.array([gx0, gy0, 0]), np.array([gx0, gy1 + 0.2, 0]),
                       buff=0, color=CHALK_WHITE, stroke_width=2,
                       max_tip_length_to_length_ratio=0.06)

        def gx(t: float) -> float:
            return gx0 + (gx1 - gx0) * t / 3.0

        def gy(v: float) -> float:
            return gy0 + (gy1 - gy0) * v / y_max

        x_ticks = VGroup()
        for t in range(4):
            px = gx(t)
            tick = Line(np.array([px, gy0 - 0.05, 0]), np.array([px, gy0 + 0.05, 0]),
                        stroke_color=CHALK_WHITE, stroke_width=1.5)
            lbl = board_text(str(t), 11, CHALK_WHITE).next_to(np.array([px, gy0, 0]), DOWN, buff=0.1)
            x_ticks.add(tick, lbl)

        y_ticks = VGroup()
        step = y_max / 4
        for i in range(5):
            amt = i * step
            py = gy(amt)
            tick = Line(np.array([gx0 - 0.05, py, 0]), np.array([gx0 + 0.05, py, 0]),
                        stroke_color=CHALK_WHITE, stroke_width=1.5)
            lbl = board_text(fmt_int(amt), 10, CHALK_WHITE).next_to(
                np.array([gx0, py, 0]), LEFT, buff=0.08)
            y_ticks.add(tick, lbl)

        x_lbl = board_text("Years", 12, CHALK_WHITE).next_to(x_ticks, DOWN, buff=0.08)
        y_lbl = board_text("Rs", 12, CHALK_WHITE).next_to(y_ticks, LEFT, buff=0.08)

        pts = [np.array([gx(t), gy(values[t]), 0]) for t in range(4)]
        segments = VGroup(*[
            Line(pts[i], pts[i + 1], stroke_color=color, stroke_width=3)
            for i in range(3)
        ])
        # A small dot at every year (0, 1, 2, 3) marking the actual data
        # point on the line, not just a bare trend stroke.
        dots = VGroup(*[Dot(p, radius=0.045, color=color) for p in pts])
        line = VGroup(segments, dots)

        axes = VGroup(axis_x, axis_y, x_ticks, y_ticks, x_lbl, y_lbl)
        return VGroup(axes, line), pts

    # -- Beat 4.5: The Formulas -------------------------------------------------
    def beat_formulas(self) -> None:
        with self.voiceover(text=NARRATION["formulas"]) as tracker:
            fade_targets = VGroup(
                self.names, self.clock, self.r_chest, self.s_chest,
                self.r_amt, self.s_amt, self.total_lbl, self.divider, self.r_jar,
                self.jar_lbl, self.mini_graph,
            )
            self.play(FadeOut(fade_targets), run_time=0.4)

            heading = board_text("The Formulas", 32, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.35, 0]))
            # "Let's write down exactly what happened, using your textbook formulas."
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            # "A stands for Amount... P stands for Principal... T stands for
            # Time... R stands for Rate... and n stands for the number of
            # years." — every symbol that appears in either formula, explained.
            # Well clear of the heading above it (heading's own bottom edge
            # sits around y=2.6, so the legend starts a full 0.5 below that).
            legend = VGroup(
                board_text("A = Amount (final total)    P = Principal (money you start with)",
                           17, CHALK_WHITE),
                board_text("T, n = Time (in years)    R = Rate of interest (% per annum)",
                           17, CHALK_WHITE),
            ).arrange(DOWN, buff=0.14).move_to(np.array([BOARD_CX, BOARD_TOP - 1.25, 0]))
            self.play(FadeIn(legend, shift=UP * 0.1), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-13)

            si_label = board_text("Simple Interest", 22, CHALK_CYAN, "BOLD")
            si_formula = chalk_math(r"A = P + \frac{PTR}{100}", 26, CHALK_CYAN)
            si_group = VGroup(si_label, si_formula).arrange(DOWN, buff=0.35).move_to(
                np.array([LEFT_CX, BOARD_CY + 0.05, 0]))
            # "Simple interest: Amount equals Principal, plus P T R over one hundred."
            self.play(Write(si_group), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-14)

            si_plug = chalk_math(
                f"{fmt_int(PRINCIPAL)}+{fmt_int(PRINCIPAL * 3 * RATE / 100)}={fmt_int(SI3)}",
                22, CHALK_CYAN).next_to(si_formula, DOWN, buff=0.4)
            # "For Ramesh, that's 500 plus 300, equals 800 rupees."
            self.play(Write(si_plug), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-12)

            ci_label = board_text("Compound Interest", 22, CHALK_PINK, "BOLD")
            ci_formula = chalk_math(r"A = P\left(1+\frac{R}{100}\right)^n", 24, CHALK_PINK)
            ci_group = VGroup(ci_label, ci_formula).arrange(DOWN, buff=0.35).move_to(
                np.array([RIGHT_CX, BOARD_CY + 0.05, 0]))
            # "Compound interest: Amount equals Principal times, one plus R over
            # one hundred, raised to the power n."
            self.play(Write(ci_group), run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["click"], gain=-14)

            ci_plug = chalk_math(
                f"{fmt_int(PRINCIPAL)}({1 + RATE / 100:.1f})^3={fmt_int(CI3)}",
                20, CHALK_PINK).next_to(ci_formula, DOWN, buff=0.4)
            # "For Srinu, that's 500 times 1.2 cubed, equals 864 rupees."
            self.play(Write(ci_plug), run_time=rt(tracker.get_remaining_duration() * 0.85))
            self.add_sound(self.sfx["success"], gain=-11)

            self.formulas_group = VGroup(heading, legend, si_group, si_plug,
                                          ci_group, ci_plug)
            self._capture_srt(tracker)

        self.play(FadeOut(self.formulas_group))

    # -- Beat 5: Scene 5 — Ending takeaway (20-year graph comparison) --------
    def beat_scene5_takeaway(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            # Graph plot area stops well short of the board's right edge so
            # the "Simple/Compound Interest" tags at the line ends have
            # room to sit fully inside the board without clipping.
            gx0, gx1 = BOARD_LEFT + 1.7, BOARD_RIGHT - 2.6
            gy0, gy1 = BOARD_BOTTOM + 1.05, BOARD_TOP - 0.9
            # Arrows (not bare lines) so both axes carry a proper arrowhead —
            # the y-axis tip is longer and its head bigger than the x-axis's,
            # so it reads clearly as pointing further upward.
            axis_x = Arrow(np.array([gx0, gy0, 0]), np.array([gx1 + 0.3, gy0, 0]),
                           buff=0, color=CHALK_WHITE, stroke_width=3,
                           max_tip_length_to_length_ratio=0.06)
            axis_y = Arrow(np.array([gx0, gy0, 0]), np.array([gx0, gy1 + 0.55, 0]),
                           buff=0, color=CHALK_WHITE, stroke_width=3,
                           max_tip_length_to_length_ratio=0.09)

            # Stretched from 3 to 20 years — at 3 years the two curves are
            # still close together; by 20 the gap is dramatic and easy to
            # see, which is the whole point of this closing beat.
            Y_MAX = 20
            AMT_MAX = 20000.0  # round ceiling just above ci_amount(20)

            def gx(year: float) -> float:
                return gx0 + (gx1 - gx0) * year / Y_MAX

            def gy(amount: float) -> float:
                return gy0 + (gy1 - gy0) * amount / AMT_MAX

            # Tick values on both axes, so the graph reads as real data, not
            # just a bare pair of crossing lines.
            x_ticks = VGroup()
            for yv in range(0, Y_MAX + 1, 5):
                px = gx(yv)
                tick = Line(np.array([px, gy0 - 0.08, 0]), np.array([px, gy0 + 0.08, 0]),
                            stroke_color=CHALK_WHITE, stroke_width=2)
                lbl = board_text(str(yv), 16, CHALK_WHITE).next_to(
                    np.array([px, gy0, 0]), DOWN, buff=0.2)
                x_ticks.add(tick, lbl)

            y_ticks = VGroup()
            for amt in range(0, int(AMT_MAX) + 1, 5000):
                py = gy(amt)
                tick = Line(np.array([gx0 - 0.08, py, 0]), np.array([gx0 + 0.08, py, 0]),
                            stroke_color=CHALK_WHITE, stroke_width=2)
                lbl = board_text(f"{amt:,}", 13, CHALK_WHITE).next_to(
                    np.array([gx0, py, 0]), LEFT, buff=0.15)
                y_ticks.add(tick, lbl)

            x_lbl = board_text("Years", 20, CHALK_WHITE).next_to(x_ticks, DOWN, buff=0.2)
            # Rotated first, *then* next_to'd against the tick labels (not
            # the bare axis) so it clears the numeric y-axis values and
            # lines up with "Years" the same way, at an equal offset.
            y_lbl = board_text("Amount (Rs)", 18, CHALK_WHITE)
            y_lbl.rotate(np.pi / 2)
            y_lbl.next_to(y_ticks, LEFT, buff=0.2)

            years = list(range(0, Y_MAX + 1))
            si_pts = [np.array([gx(t), gy(si_amount(t)), 0]) for t in years]
            ci_pts = [np.array([gx(t), gy(ci_amount(t)), 0]) for t in years]
            si_line = VGroup(*[
                Line(si_pts[i], si_pts[i + 1], stroke_color=CHALK_CYAN, stroke_width=4)
                for i in range(Y_MAX)
            ])
            ci_line = VGroup(*[
                Line(ci_pts[i], ci_pts[i + 1], stroke_color=CHALK_PINK, stroke_width=4)
                for i in range(Y_MAX)
            ])
            # A dot at every 5-year mark (matching the x-axis ticks) on
            # each curve, so specific data points are readable — not just
            # a bare trend stroke.
            marked_years = list(range(0, Y_MAX + 1, 5))
            si_dots = VGroup(*[Dot(si_pts[t], radius=0.05, color=CHALK_CYAN) for t in marked_years])
            ci_dots = VGroup(*[Dot(ci_pts[t], radius=0.05, color=CHALK_PINK) for t in marked_years])

            si_tag = board_text("Simple Interest", 17, CHALK_CYAN, "BOLD")
            si_tag.move_to(si_pts[-1] + RIGHT * 0.15 + DOWN * 0.15, aligned_edge=LEFT)
            # Right-aligned to a fixed inset so the longer "Compound
            # Interest" label below can never run past the board edge,
            # regardless of exactly where the line ends.
            si_tag.shift(RIGHT * min(0, BOARD_RIGHT - 0.15 - si_tag.get_right()[0]))

            ci_tag = board_text("Compound Interest", 17, CHALK_PINK, "BOLD")
            ci_tag.move_to(ci_pts[-1] + RIGHT * 0.15 + UP * 0.05, aligned_edge=LEFT)
            ci_tag.shift(RIGHT * min(0, BOARD_RIGHT - 0.15 - ci_tag.get_right()[0]))

            # "Over twenty years, Ramesh's simple interest crawls up..." — axes + SI line.
            self.play(GrowArrow(axis_x), GrowArrow(axis_y), FadeIn(x_lbl), FadeIn(y_lbl),
                      FadeIn(x_ticks), FadeIn(y_ticks),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.4))
            self.play(LaggedStart(*[Create(seg) for seg in si_line], lag_ratio=0.05),
                      Write(si_tag), run_time=rt(tracker.time_until_bookmark("b1")))
            self.play(LaggedStart(*[GrowFromCenter(d) for d in si_dots], lag_ratio=0.2),
                      run_time=rt(tracker.get_remaining_duration() * 0.3))
            self.add_sound(self.sfx["swipe"], gain=-15)

            # "...Srinu's compound interest rockets upward..." — CI curve.
            self.play(LaggedStart(*[Create(seg) for seg in ci_line], lag_ratio=0.05),
                      Write(ci_tag), run_time=rt(tracker.time_until_bookmark("b2")))
            self.play(LaggedStart(*[GrowFromCenter(d) for d in ci_dots], lag_ratio=0.2),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.3))
            self.add_sound(self.sfx["whoosh"], gain=-13)
            self.play(Flash(ci_pts[-1], color=CHALK_PINK, flash_radius=0.4),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.4))
            self.add_sound(self.sfx["ding"], gain=-12)

            gap_lbl = board_text(
                f"Gap after 20 years = {fmt_money(ci_amount(Y_MAX) - si_amount(Y_MAX))}",
                20, CHALK_YELLOW, "BOLD").move_to(np.array([BOARD_CX, BOARD_TOP - 0.4, 0]))
            self.play(Write(gap_lbl), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)

            takeaway = board_text("That's the power of compounding!", 17,
                                   CHALK_YELLOW, "BOLD").next_to(gap_lbl, DOWN, buff=0.15)
            self.play(Write(takeaway), run_time=rt(tracker.get_remaining_duration() * 0.7))
            self.add_sound(self.sfx["success"], gain=-11)

            self.graph_group = VGroup(axis_x, axis_y, x_lbl, y_lbl, x_ticks, y_ticks,
                                       si_line, si_dots, si_tag, ci_line, ci_dots, ci_tag,
                                       gap_lbl, takeaway)
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
                self.bullet_row(2, ["Srinu's compound interest adds interest on top of",
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

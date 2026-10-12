"""
Linear Equations — LHS, RHS & Transposition
Story-mode chalkboard lesson (Telangana Class 8 Maths, Chapter 2: Linear
Equations in One Variable).

Production pipeline (mirrors the rest of the Story-Mode series):
  - Shared assets/background2.png chalkboard backdrop + student/teacher
    cutouts + corner badges: dhimantAI brand badge top-left (no topic
    label) and Mathematics top-right (assets folder of
    Story-Mode-Manim-Videos).
  - VoiceoverScene + speech service (edge-tts en-IN-PrabhatNeural, or the
    project's Gemini Zephyr routing via .env). Narration is written as
    natural continuous prose (no enumerated-list phrasing, which Gemini
    TTS has been observed to reject by generating text instead of audio).
  - Real per-word sync via <bookmark> tags + tracker timing.
  - Ground-truth SRT export from the service's word boundaries.
  - Sound effects from sound_effects.py; chalk-styled Text (Segoe Print)
    and MathTex.
  - Shared story_common.play_challenge_countdown() for the "YOUR TURN"
    10-second THINK badge (board-centre, dims the whole board).

Visual identity (kept for the whole video):
  - x (variable) is always chalk cyan; LHS container cyan, RHS pink.
  - The '=' stays centred and stable; the term being transposed is
    highlighted, then travels across the '=' and flips its operation
    DURING the crossing (never before).
  - One equation transformation at a time; bottom 15-20% kept clear for
    subtitles.

Title + 10 scenes:
  0. Title card.
  1. The Mystery Number -- ? -> x2 -> -7 -> 35 compresses into 2x-7=35.
  2. Anatomy -- equality sign, LHS, RHS, variable, constants.
  3. What '=' Really Says -- same value; guesses 10, 15, 21; 21 wins.
  4. Transposing Addition/Subtraction -- -7 crosses, becomes +7; 2x=42.
  5. Transposing Multiplication/Division -- 2 crosses to denominator;
     x = 21.
  6. Check the Solution -- substitute 21; 35 = 35 verified.
  7. The Four Transposition Rules -- +<->- and x<->/ around '='.
  8. Real-World Park -- 2[(x+17)+x]=178 -> x=36 (park 36 m x 53 m).
  9. Your Turn -- 3x+1=16 with 10 s countdown -> x=5.
 10. Recap -- LHS=RHS + rules + 2x-7=35 -> x=21 + Thank You.
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
    Square, Polygon, Ellipse, Dot, Arrow, DoubleArrow, Text, Write, FadeIn,
    FadeOut, Create, ReplacementTransform, TransformMatchingTex, GrowArrow,
    TransformFromCopy,
    Indicate, Flash, Circumscribe, SurroundingRectangle, config,
)
from manim_voiceover import VoiceoverScene
from manim_voiceover.tracker import AUDIO_OFFSET_RESOLUTION

from speech_service import get_speech_service
from sound_effects import load_all as load_sfx
from story_common import play_challenge_countdown
from synced_voice import install_synced_voiceover

# --------------------------------------------------------------- theme -----
CHALK_WHITE = "#F5F2E9"
BRAND_WHITE = "#FFFFFF"  # pure white for the dhimantAI badge -- higher contrast than CHALK_WHITE
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

# The main equation line lives here for scenes 1-6 so the '=' never moves.
EQ_Y = 0.7


def rt(seconds: float, floor: float = MIN_RT) -> float:
    return max(floor, float(seconds))


def board_text(s: str, size: int = 34, color: str = CHALK_WHITE,
               weight: str = "NORMAL") -> Text:
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def chalk_math(s: str, size: int = 34, color: str = MATH_COLOR) -> MathTex:
    return MathTex(s, font_size=size, color=color)


# ---------------------------------------------------------------- helpers ----

def check_mark(color: str = CHALK_GREEN, size: float = 0.4,
               width: float = 5) -> VGroup:
    """A proper chalk tick: down-left start, valley, long up-right stroke."""
    a = np.array([-0.52, 0.16, 0.0]) * size
    b = np.array([-0.16, -0.30, 0.0]) * size
    c = np.array([0.52, 0.40, 0.0]) * size
    return VGroup(
        Line(a, b, color=color, stroke_width=width),
        Line(b, c, color=color, stroke_width=width),
    )


def cross_mark(color: str = CHALK_RED, size: float = 0.34,
               width: float = 5) -> VGroup:
    """A proper chalk cross (two crossed strokes)."""
    return VGroup(
        Line(np.array([-0.5, 0.5, 0.0]) * size, np.array([0.5, -0.5, 0.0]) * size,
             color=color, stroke_width=width),
        Line(np.array([0.5, 0.5, 0.0]) * size, np.array([-0.5, -0.5, 0.0]) * size,
             color=color, stroke_width=width),
    )


def tick_beside(target, color: str = CHALK_GREEN, size: float = 0.4,
                buff: float = 0.3) -> VGroup:
    """Tick placed to the right of `target`, vertically centred on it."""
    mark = check_mark(color, size)
    mark.next_to(target, RIGHT, buff=buff)
    mark.shift(UP * (target.get_center()[1] - mark.get_center()[1]))
    return mark


def align_equals(eq: MathTex, anchor_x: float = BOARD_CX,
                 anchor_y: float = EQ_Y) -> MathTex:
    """Centre the WHOLE equation line on the board.

    (Aligning only the '=' left the wider LHS lines sitting to the left of
    the board's centre line; centring the full bounding box keeps every
    equation visually centred on the green board.)"""
    eq.move_to(np.array([anchor_x, anchor_y, 0.0]))
    return eq


def panel_around(mobj, color: str, buff: float = 0.14,
                 opacity: float = 0.14) -> SurroundingRectangle:
    return SurroundingRectangle(
        mobj, color=color, buff=buff, corner_radius=0.08,
        fill_color=color, fill_opacity=opacity, stroke_width=2,
    )


def side_panel(part, eq, color: str, pad: float = 0.16,
               opacity: float = 0.14) -> SurroundingRectangle:
    """A rounded panel hugging one side of the equation.

    The equation typesets its '=' with wide spacing (`\\;=\\;`), so a panel
    that hugs its own part always clears both that part's glyphs and the
    equality sign. (The earlier version pinned the panel's inner edge a
    fixed distance from the '=', which pushed it over its own text.)
    """
    return SurroundingRectangle(
        part, color=color, buff=pad, corner_radius=0.12,
        fill_color=color, fill_opacity=opacity, stroke_width=2.5,
    )


# --------------------------------------------------------- realistic icons ----
# Ported from the series' own icon vocabulary (Transposition-Balancing-Scales
# and Identities-and-Inverses) so the diagrams match the rest of the videos.

def drop_shadow(mobj: VGroup, dx: float = 0.05, dy: float = -0.06,
                opacity: float = 0.3) -> VGroup:
    shadow = mobj.copy()
    shadow.set_fill(BLACK, opacity=opacity)
    shadow.set_stroke(width=0)
    shadow.shift(np.array([dx, dy, 0]))
    return VGroup(shadow, mobj)


def detective_hat(color: str = "#5A3B1E", width: float = 0.8) -> VGroup:
    """A jaunty detective fedora with curved brim, creased crown, ribbon."""
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
    """Wooden mystery crate with a detective hat and an empty cyan medallion
    (the '?' / 'x' label is drawn separately by the caller so it can morph)."""
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


def machine_icon(symbol: str, color: str, scale: float = 0.42) -> VGroup:
    """A small operation machine (funnel intake, dial gauge, op panel, chute
    outlet) -- ported from the Identities-and-Inverses operation_machine."""
    body_w, body_h = 3.0, 1.5
    body = RoundedRectangle(width=body_w, height=body_h, corner_radius=0.16,
                            stroke_color=color, stroke_width=2.5,
                            fill_color="#2A1E10", fill_opacity=0.5)
    funnel = Polygon(
        np.array([-body_w * 0.28, body_h / 2, 0]),
        np.array([body_w * 0.28, body_h / 2, 0]),
        np.array([body_w * 0.1, body_h / 2 + 0.3, 0]),
        np.array([-body_w * 0.1, body_h / 2 + 0.3, 0]),
        stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.15,
    )
    chute = Polygon(
        np.array([-body_w * 0.1, -body_h / 2, 0]),
        np.array([body_w * 0.1, -body_h / 2, 0]),
        np.array([body_w * 0.22, -body_h / 2 - 0.28, 0]),
        np.array([-body_w * 0.22, -body_h / 2 - 0.28, 0]),
        stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.15,
    )
    dial_center = LEFT * 0.85
    dial = Circle(radius=0.26, stroke_color=color, stroke_width=2.2,
                  fill_color="#1A140A", fill_opacity=0.6).move_to(dial_center)
    dial_ticks = VGroup(*[
        Line(dial_center + 0.18 * np.array([np.cos(a), np.sin(a), 0]),
             dial_center + 0.26 * np.array([np.cos(a), np.sin(a), 0]),
             stroke_color=color, stroke_width=1.5)
        for a in np.linspace(0, 2 * np.pi, 8, endpoint=False)
    ])
    needle = Line(dial_center,
                  dial_center + 0.19 * np.array([np.cos(1.0), np.sin(1.0), 0]),
                  stroke_color=CHALK_YELLOW, stroke_width=2)
    lights = VGroup(
        Dot(radius=0.05, color=CHALK_GREEN).move_to(RIGHT * 0.35 + UP * 0.4),
        Dot(radius=0.05, color=CHALK_RED).move_to(RIGHT * 0.6 + UP * 0.4),
    )
    op_panel = RoundedRectangle(width=0.6, height=0.5, corner_radius=0.06,
                                stroke_color=color, stroke_width=1.5,
                                fill_color="#1A140A", fill_opacity=0.6).move_to(
        RIGHT * 0.75 + DOWN * 0.15)
    op_lbl = MathTex(symbol, font_size=28, color=CHALK_WHITE).move_to(op_panel.get_center())
    machine = VGroup(chute, body, funnel, dial, dial_ticks, needle, lights,
                     op_panel, op_lbl).scale(scale)
    return drop_shadow(machine, dx=0.04, dy=-0.05, opacity=0.25)


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
    # anchored at the base so the trunk always meets the ground
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


def sparse_lawn(rect: Rectangle, blockers: tuple = (), color: str = CHALK_GREEN,
                 margin: float = 0.3, spacing: float = 0.72) -> VGroup:
    """A light scattering of grass tufts: enough texture to read as a lawn,
    but far fewer marks than a full grid (nothing grows under the pond or
    the trees)."""
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
    inner = Ellipse(width=0.36, height=0.18, stroke_color=CHALK_CYAN,
                    stroke_width=1.1, fill_color="#2E82A0",
                    fill_opacity=0.7).move_to(ORIGIN)
    return VGroup(outer, inner).scale(scale).move_to(pos)


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "Today, linear equations!<bookmark mark='b0'/> "
        "The left hand side, the right hand side, and the transposition "
        "rules that reveal the unknown.<bookmark mark='b1'/> "
        "Let's begin with a mystery!<bookmark mark='b2'/>"
    ),
    "scene1": (
        "A number is hidden inside this box.<bookmark mark='b0'/> "
        "We double it, and then take away seven.<bookmark mark='b1'/> "
        "The final result is thirty five.<bookmark mark='b2'/> "
        "What was the number? Instead of guessing, let's name the unknown "
        "x.<bookmark mark='b3'/> The whole puzzle now squeezes into one "
        "neat sentence: two x minus seven equals thirty five."
        "<bookmark mark='b4'/> An equation stores every piece of the "
        "puzzle in a single mathematical statement.<bookmark mark='b5'/>"
    ),
    "scene2": (
        "An equation is built from three main parts.<bookmark mark='b0'/> "
        "The equality sign is the heart: it declares that both sides are "
        "tied together.<bookmark mark='b1'/> On the left of the equals "
        "sign lives the expression two x minus seven — the L H S, the "
        "left hand side.<bookmark mark='b2'/> On the right lives thirty "
        "five — the R H S, the right hand side.<bookmark mark='b3'/> "
        "The x is the variable, the unknown we must find."
        "<bookmark mark='b4'/> And two, seven, and thirty five are "
        "constants — fixed numbers that never change.<bookmark mark='b5'/>"
    ),
    "scene3": (
        "The equals sign makes one simple promise: both sides hold the "
        "same value.<bookmark mark='b0'/> L H S equals R H S — the same "
        "value on both sides.<bookmark mark='b1'/> So which value of x "
        "keeps the promise? Try ten: two times ten minus seven is "
        "thirteen — not thirty five.<bookmark mark='b2'/> Try fifteen: "
        "that gives twenty three — still not right.<bookmark mark='b3'/> "
        "Try twenty one: two times twenty one minus seven is exactly "
        "thirty five!<bookmark mark='b4'/> Twenty one is the solution — "
        "the value that makes both sides equal.<bookmark mark='b5'/>"
    ),
    "scene4": (
        "Now let's solve it step by step, keeping equality true the "
        "whole time.<bookmark mark='b0'/> The minus seven hides the x, "
        "so we undo that subtraction by adding seven.<bookmark mark='b1'/> "
        "Watch the seven cross the equals sign — and the instant it "
        "crosses, minus flips into plus!<bookmark mark='b2'/> Two x "
        "equals thirty five plus seven.<bookmark mark='b3'/> Thirty five "
        "plus seven is forty two.<bookmark mark='b4'/> Rule one: minus "
        "becomes plus when it crosses the equals sign.<bookmark mark='b5'/>"
    ),
    "scene5": (
        "Two x really means two times x.<bookmark mark='b0'/> The two is "
        "multiplied onto the variable.<bookmark mark='b1'/> So we undo "
        "it with the opposite operation: division.<bookmark mark='b2'/> "
        "The two crosses the equals sign, and lands below forty two as a "
        "divisor.<bookmark mark='b3'/> Forty two divided by two is "
        "twenty one.<bookmark mark='b4'/> Rule two: multiplication "
        "becomes division when it crosses. And now x stands all alone — "
        "x equals twenty one!<bookmark mark='b5'/>"
    ),
    "scene6": (
        "How do we know twenty one is truly correct? We check!"
        "<bookmark mark='b0'/> Substitute twenty one back into the "
        "original equation, in place of x.<bookmark mark='b1'/> Two "
        "times twenty one minus seven — that is forty two minus seven."
        "<bookmark mark='b2'/> Forty two minus seven gives thirty five."
        "<bookmark mark='b3'/> Both sides are thirty five: thirty five "
        "equals thirty five. The solution is verified!"
        "<bookmark mark='b4'/>"
    ),
    "scene7": (
        "Let's collect all four transposition rules.<bookmark mark='b0'/> "
        "Addition crosses the equals sign and becomes subtraction,"
        "<bookmark mark='b1'/> and subtraction crosses back to become "
        "addition.<bookmark mark='b2'/> Multiplication crosses over to "
        "become division,<bookmark mark='b3'/> and division crosses back "
        "to become multiplication.<bookmark mark='b4'/> One golden idea: "
        "across the equals sign, every operation flips to its inverse."
        "<bookmark mark='b5'/>"
    ),
    "cross": (
        "When both sides of an equation are fractions, transposition "
        "becomes cross multiplication.<bookmark mark='b0'/> A over b equals "
        "c over d gives a times d equals b times c.<bookmark mark='b1'/> "
        "Let's solve x over four equals three over two."
        "<bookmark mark='b2'/> Cross multiply: x times two equals four "
        "times three.<bookmark mark='b3'/> So two x equals twelve, and x "
        "equals six.<bookmark mark='b4'/> Check it: six over four is the "
        "same as three over two, so x equals six is correct."
        "<bookmark mark='b5'/>"
    ),
    "scene8": (
        "Equations solve real problems — like this rectangular park."
        "<bookmark mark='b0'/> Its breadth is x metres, and its length "
        "is x plus seventeen metres. The perimeter is one hundred and "
        "seventy eight metres.<bookmark mark='b1'/> The perimeter "
        "formula adds all four sides: two times, x plus seventeen plus "
        "x, equals one seventy eight.<bookmark mark='b2'/> That "
        "simplifies to four x plus thirty four equals one seventy "
        "eight.<bookmark mark='b3'/> Transpose the thirty four: four x "
        "equals one forty four.<bookmark mark='b4'/> Divide both sides "
        "by four, and x equals thirty six.<bookmark mark='b5'/> So the "
        "park is thirty six metres wide and fifty three metres long. "
        "Unknown, equation, solution!<bookmark mark='b6'/>"
    ),
    "scene9_setup": (
        "Your turn!<bookmark mark='b0'/> Solve three x plus one equals "
        "sixteen.<bookmark mark='b1'/> Which term moves first?"
        "<bookmark mark='b2'/> Pause the video, and try it yourself."
        "<bookmark mark='b3'/>"
    ),
    "scene9_reveal": (
        "First, plus one crosses the equals sign and becomes minus one: "
        "three x equals fifteen.<bookmark mark='b0'/> Then the "
        "multiplier three crosses and becomes a divisor: x equals "
        "fifteen divided by three.<bookmark mark='b1'/> That gives x "
        "equals five!<bookmark mark='b2'/> Wonderful — you solved it "
        "with transposition!<bookmark mark='b3'/>"
    ),
    "scene10": (
        "Let's lock in the whole journey.<bookmark mark='b0'/> An "
        "equation has two sides — the left hand side and the right hand "
        "side — joined by the equality sign.<bookmark mark='b1'/> The "
        "unknown is the variable, and transposition flips every "
        "operation as it crosses: minus becomes plus, multiplication "
        "becomes division.<bookmark mark='b2'/> Two x minus seven "
        "equals thirty five became two x equals forty two, and finally "
        "x equals twenty one.<bookmark mark='b3'/> Keep the equality "
        "true, isolate the unknown, and always check your answer!"
        "<bookmark mark='b4'/> Thank you so much for watching, and I "
        "will see you in the next lesson!<bookmark mark='b5'/>"
    ),
}


class EquationAnatomyStory(VoiceoverScene):
    """Story-mode chalkboard lesson: Anatomy of an Equation (LHS, RHS &
    Transposition)."""

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
            -config.frame_height / 2 + student.height / 2 - 0.1,
            0,
        ]))

        teacher = ImageMobject(str(assets_dir / "teacher.png"))
        teacher.set_z_index(-5)
        teacher.height = 3.3
        teacher.move_to(np.array([
            config.frame_width / 2 - teacher.width / 2 + 0.45,
            -config.frame_height / 2 + teacher.height / 2 - 0.1,
            0,
        ]))

        self.bg = bg
        self.student = student
        self.teacher = teacher

        # Both corner badges share the same chalk-stamped ribbon style and
        # are rendered at font_size=12 then scaled up (manim/Pango shows
        # per-glyph spacing artifacts in this font at small sizes above 12;
        # scaling the finished badge is artifact-free). Left = dhimantAI
        # brand badge (no topic label), right = Mathematics -- matches the
        # rest of the Story-Mode series.
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
            corner_radius=0.04, width=label.width + 0.24, height=label.height + 0.16,
            stroke_color=CHALK_AMBER, stroke_width=1.5,
            fill_color="#2A1D10", fill_opacity=0.45,
        )
        label.move_to(frame.get_center())
        badge = VGroup(frame, label)
        badge.scale(scale)

        yy = BOARD_TOP - 0.32 if y is None else y
        if corner == "left":
            badge.move_to(np.array([BOARD_LEFT + 0.55, yy, 0]))
            badge.shift(RIGHT * (BOARD_LEFT + 0.08 - badge.get_left()[0]))
        else:
            badge.move_to(np.array([BOARD_RIGHT - 0.6, yy, 0]))
            # Right margin is smaller than the left corner's 0.08 to
            # compensate for the background art's perspective (same fix as
            # the rest of the Story-Mode series).
            badge.shift(RIGHT * (BOARD_RIGHT - 0.013 - badge.get_right()[0]))
        # Snap the TOP edge to the same 0.08 margin used horizontally, so
        # both badges sit with equal spacing from the board's edges.
        badge.shift(UP * ((BOARD_TOP - 0.08) - badge.get_top()[1]))
        return badge

    def reset_board(self) -> None:
        self.clear()
        self.add(self.bg, self.student, self.teacher, self.badge, self.badge_l)

    # -- real SRT export ---------------------------------------------------
    def _capture_srt(self, tracker, words_per_line: int = 9) -> None:
        wbs = [
            wb for wb in tracker.data.get("word_boundaries", [])
            if wb.get("text", "").strip()
        ]
        if not wbs:
            return
        starts = [tracker.start_t + wb["audio_offset"] / AUDIO_OFFSET_RESOLUTION
                  for wb in wbs]
        for i in range(0, len(wbs), words_per_line):
            chunk = wbs[i:i + words_per_line]
            chunk_starts = starts[i:i + words_per_line]
            end = starts[i + words_per_line] if i + words_per_line < len(starts) \
                else tracker.end_t
            text = " ".join(wb["text"] for wb in chunk)
            self._srt_entries.append((chunk_starts[0], end, text))

    def _write_real_srt(self) -> None:
        out_dir = _HERE / "media" / "videos" / "equation_anatomy_story"
        out_dir.mkdir(parents=True, exist_ok=True)
        srt_path = out_dir / f"{self.__class__.__name__}.real.srt"

        def fmt(t: float) -> str:
            # carry-safe: rounding must never produce ",1000" (4-digit ms),
            # which is an invalid SRT timestamp that caption parsers drop.
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
        srt_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"[real SRT written] {srt_path}")
        (out_dir / "real.srt").write_text("\n".join(lines), encoding="utf-8")
        try:
            if (hasattr(self, "renderer") and hasattr(self.renderer, "file_writer")
                    and self.renderer.file_writer.movie_file_path):
                movie_dir = Path(self.renderer.file_writer.movie_file_path).parent
                (movie_dir / "real.srt").write_text("\n".join(lines), encoding="utf-8")
                (movie_dir / f"{self.__class__.__name__}.real.srt").write_text(
                    "\n".join(lines), encoding="utf-8")
        except Exception:
            pass

    def construct(self):
        self.sfx = load_sfx()
        self.set_speech_service(get_speech_service(), create_subcaption=False)
        # The Gemini service times words by character count, which drifts
        # seconds away from the real speech. Re-time every narration clip
        # against the audio it will actually play (same voice, real timeline).
        install_synced_voiceover(self)

        self.add_background()

        self.beat0_title()
        self.beat1_mystery()
        self.beat2_anatomy()
        self.beat3_equality()
        self.beat4_transpose_add()
        self.beat5_transpose_mult()
        self.beat6_verify()
        self.beat7_rules()
        self.beat7b_cross_multiply()
        self.beat8_park()
        self.beat9_challenge()
        self.beat10_recap()

        self._write_real_srt()

    # ================================================================ beats ==

    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Linear Equations", 42, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 1.6, 0]))
            self.play(Write(title), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            sub = board_text("LHS, RHS & Transposition", 22, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 0.95, 0]))
            mini = MathTex("2x-7", r"\;=\;", "35", font_size=50).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.15, 0]))
            mini[0][1].set_color(CHALK_CYAN)
            ml = SurroundingRectangle(mini[0], color=CHALK_CYAN, buff=0.14,
                                      corner_radius=0.08, stroke_width=2.5,
                                      fill_color=CHALK_CYAN, fill_opacity=0.12)
            mr = SurroundingRectangle(mini[2], color=CHALK_PINK, buff=0.14,
                                      corner_radius=0.08, stroke_width=2.5,
                                      fill_color=CHALK_PINK, fill_opacity=0.12)
            mini_lhs = board_text("LHS", 15, CHALK_CYAN, "BOLD").next_to(ml, UP, buff=0.12)
            mini_rhs = board_text("RHS", 15, CHALK_PINK, "BOLD").next_to(mr, UP, buff=0.12)
            self.play(Write(sub), FadeIn(mini), Create(ml), Create(mr),
                      FadeIn(mini_lhs), FadeIn(mini_rhs),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)

            rules_prev = MathTex(r"-\leftrightarrow+\qquad\times\leftrightarrow\div",
                                 font_size=30, color=CHALK_GREEN).move_to(
                np.array([BOARD_CX, -1.25, 0]))
            question = board_text("What was the hidden number?", 20, CHALK_PINK,
                                  "BOLD").move_to(np.array([BOARD_CX, -2.05, 0]))
            self.play(FadeIn(rules_prev, shift=UP * 0.1), FadeIn(question),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["swipe"], gain=-15)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 1: Scene 1 — The Mystery Number --------------------------------
    def beat1_mystery(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            top = board_text("A number is hidden.", 18, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.55, 0]))

            # Realistic machine row, CENTRED on the board: detective crate ->
            # "x2" machine -> "-7" machine -> green 35 output.
            crate = mystery_crate(width=1.0, height=0.95)
            mul = machine_icon(r"\times 2", CHALK_CYAN, scale=0.42)
            sub = machine_icon("-7", CHALK_PINK, scale=0.42)
            ring = Circle(0.45, stroke_color=CHALK_GREEN, stroke_width=2.5,
                          fill_color="#12240F", fill_opacity=0.6)
            out35 = MathTex("35", font_size=30, color=CHALK_GREEN).move_to(
                ring.get_center())
            out = VGroup(ring, out35)

            stations = VGroup(crate, mul, sub, out).arrange(RIGHT, buff=1.05)
            stations.move_to(np.array([BOARD_CX, 0.95, 0]))
            q = MathTex("?", font_size=30, color=CHALK_CYAN).move_to(
                crate.badge.get_center())

            a1 = Arrow(crate.get_right(), mul.get_left(), buff=0.08,
                       color=CHALK_WHITE, stroke_width=3)
            a2 = Arrow(mul.get_right(), sub.get_left(), buff=0.08,
                       color=CHALK_WHITE, stroke_width=3)
            a3 = Arrow(sub.get_right(), out.get_left(), buff=0.08,
                       color=CHALK_WHITE, stroke_width=3)

            self.play(FadeIn(top), run_time=rt(tracker.time_until_bookmark("b0") * 0.4))
            self.play(FadeIn(crate, scale=0.8), FadeIn(q, scale=0.8),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            # "We double it, and then take away seven." -- BOTH machines
            # appear during this sentence, in the order they are spoken.
            self.play(GrowArrow(a1), FadeIn(mul),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.55))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(GrowArrow(a2), FadeIn(sub),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.45))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            # "The final result is thirty five." -- the output lands now.
            self.play(GrowArrow(a3), FadeIn(out),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-12)

            # "What was the number? ... let's name the unknown x." --
            # the question appears first, then the "?" becomes x.
            question = board_text("What was the number?", 18, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, -0.3, 0]))
            self.play(FadeIn(question),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.4))
            x_lbl = MathTex("x", font_size=30, color=CHALK_CYAN).move_to(
                q.get_center())
            self.play(ReplacementTransform(q, x_lbl),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            # "The whole puzzle now squeezes into one neat sentence: two x
            # minus seven equals thirty five." -- the machine visibly
            # compresses into the chain (it fades out in the same play, so
            # nothing ever overlaps on the board).
            chain = MathTex(r"x \rightarrow 2x \rightarrow 2x-7 \rightarrow 35",
                            font_size=28).move_to(np.array([BOARD_CX, EQ_Y, 0]))
            self.play(FadeIn(chain), FadeOut(crate), FadeOut(x_lbl),
                      FadeOut(mul), FadeOut(sub), FadeOut(out), FadeOut(a1),
                      FadeOut(a2), FadeOut(a3),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-12)

            # "An equation stores every piece ... one mathematical statement."
            eq = MathTex("2x-7", r"\;=\;", "35", font_size=50)
            align_equals(eq, BOARD_CX, EQ_Y)
            eq[0][1].set_color(CHALK_CYAN)
            eq_box = SurroundingRectangle(eq, color=CHALK_GREEN, buff=0.22,
                                          corner_radius=0.1, stroke_width=2)
            self.play(FadeOut(top), FadeOut(question),
                      run_time=rt(tracker.time_until_bookmark("b5") * 0.45))
            self.play(TransformMatchingTex(chain, eq), Create(eq_box),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["success"], gain=-11)

            self.eq = eq
            self.eq_box = eq_box
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 2: Scene 2 — Anatomy of an Equation -----------------------------
    def beat2_anatomy(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            eq = self.eq

            heading = board_text("Anatomy of an Equation", 26, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.4, 0]))
            self.play(Write(heading), FadeOut(self.eq_box),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            # "EQUALITY SIGN" is parked directly above the '=' (which is no
            # longer at the board centre now that the whole line is centred).
            eq_label = board_text("EQUALITY SIGN", 16, CHALK_YELLOW, "BOLD").move_to(
                np.array([eq[1].get_center()[0], 2.15, 0]))
            pointer = Arrow(eq_label.get_bottom() + DOWN * 0.16,
                            eq[1].get_top() + UP * 0.12, buff=0,
                            color=CHALK_YELLOW, stroke_width=2.2,
                            max_tip_length_to_length_ratio=0.16, tip_length=0.13)
            self.play(Indicate(eq[1], color=CHALK_YELLOW, scale_factor=1.5),
                      FadeIn(eq_label), GrowArrow(pointer),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # Panels hold a fixed gap from the '=' (nothing touches the sign)
            # and the two-line labels sit well above them, spread wide so the
            # arrow passes cleanly between them.
            lhs_box = side_panel(eq[0], eq, CHALK_CYAN, pad=0.18)
            lhs_lbl = VGroup(
                board_text("LHS", 24, CHALK_CYAN, "BOLD"),
                board_text("Left Hand Side", 14, CHALK_CYAN),
            ).arrange(DOWN, buff=0.06).move_to(
                np.array([eq[0].get_center()[0] - 0.3, 1.45, 0]))
            self.play(Create(lhs_box), FadeIn(lhs_lbl),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            rhs_box = side_panel(eq[2], eq, CHALK_PINK, pad=0.18)
            rhs_lbl = VGroup(
                board_text("RHS", 24, CHALK_PINK, "BOLD"),
                board_text("Right Hand Side", 14, CHALK_PINK),
            ).arrange(DOWN, buff=0.06).move_to(
                np.array([eq[2].get_center()[0] + 0.35, 1.45, 0]))
            self.play(Create(rhs_box), FadeIn(rhs_lbl),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            # Variable / constants live in the free lower half of the board.
            x_pt = eq[0][1].get_center()
            var_lbl = board_text("Variable", 20, CHALK_CYAN, "BOLD").move_to(
                np.array([x_pt[0] - 0.35, -0.95, 0]))
            var_arrow = Arrow(var_lbl.get_top(), x_pt + DOWN * 0.3, buff=0.05,
                              color=CHALK_CYAN, stroke_width=2.5)
            self.play(FadeIn(var_lbl), GrowArrow(var_arrow),
                      Indicate(eq[0][1], color=CHALK_CYAN, scale_factor=1.5),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-13)

            const_lbl = board_text("Constants / numbers", 18, CHALK_AMBER,
                                   "BOLD").move_to(
                np.array([BOARD_CX, -1.85, 0]))
            self.play(FadeIn(const_lbl),
                      Indicate(eq[0][0], color=CHALK_AMBER, scale_factor=1.5),
                      Indicate(eq[0][3], color=CHALK_AMBER, scale_factor=1.5),
                      Indicate(eq[2], color=CHALK_AMBER, scale_factor=1.3),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["click"], gain=-15)

            self.lhs_box = lhs_box
            self.rhs_box = rhs_box
            self.eq_labels = VGroup(heading, eq_label, pointer, lhs_lbl, rhs_lbl,
                                    var_lbl, var_arrow, const_lbl)
            self._capture_srt(tracker)

        self.play(FadeOut(self.eq_labels), run_time=0.4)
        self.wait(TRANSITION_HOLD)

    # -- Beat 3: Scene 3 — What '=' Really Says -------------------------------
    def beat3_equality(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            eq = self.eq

            self.play(Indicate(self.lhs_box, color=CHALK_CYAN, scale_factor=1.08),
                      run_time=rt(tracker.time_until_bookmark("b0")))

            same_lbl = board_text("Same value", 18, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, 2.0, 0]))
            self.play(Indicate(self.rhs_box, color=CHALK_PINK, scale_factor=1.08),
                      Flash(eq[1], color=CHALK_YELLOW, flash_radius=0.5),
                      FadeIn(same_lbl),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            def guess(v: int, ok: bool) -> VGroup:
                val = 2 * v - 7
                chip = VGroup(
                    MathTex(f"x={v}", font_size=26),
                    MathTex(r"\to", font_size=20, color=CHALK_WHITE),
                    MathTex(str(val), font_size=24,
                            color=CHALK_GREEN if ok else CHALK_RED),
                ).arrange(RIGHT, buff=0.14)
                mark = (tick_beside(chip, CHALK_GREEN, 0.34, 0.16) if ok
                        else cross_mark(CHALK_RED, 0.26))
                if not ok:
                    mark.next_to(chip, RIGHT, buff=0.16)
                    mark.shift(UP * (chip.get_center()[1] - mark.get_center()[1]))
                return VGroup(chip, mark)

            g10 = guess(10, False)
            g15 = guess(15, False)
            g21 = guess(21, True)

            # The row stays centred on the board as each guess appears
            # (chips are re-arranged after every addition).
            def placed(visible):
                grp = VGroup(*visible).arrange(RIGHT, buff=0.75)
                grp.move_to(np.array([BOARD_CX, -0.55, 0]))
                return [m.get_center().copy() for m in grp]

            p1 = placed([g10])
            p2 = placed([g10, g15])
            p3 = placed([g10, g15, g21])

            g10.move_to(p1[0])
            self.play(FadeIn(g10, scale=0.7),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            g15.move_to(p2[1])
            self.play(g10.animate.move_to(p2[0]), FadeIn(g15, scale=0.7),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            g21.move_to(p3[2])
            self.play(g10.animate.move_to(p3[0]), g15.animate.move_to(p3[1]),
                      FadeIn(g21, scale=0.7),
                      Flash(g21, color=CHALK_GREEN, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)

            sol_lbl = board_text("21 is the solution!", 20, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -1.4, 0]))
            self.play(FadeIn(sol_lbl),
                      Circumscribe(g21, color=CHALK_GREEN, stroke_width=3, time_width=0.6),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["ding"], gain=-12)

            self.guess_group = VGroup(same_lbl, g10, g15, g21, sol_lbl)
            self._capture_srt(tracker)

        self.play(FadeOut(self.guess_group), run_time=0.4)
        self.wait(TRANSITION_HOLD)

    # -- Beat 4: Scene 4 — Transposing Addition / Subtraction -----------------
    def beat4_transpose_add(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            eq = self.eq

            self.play(FadeOut(self.lhs_box), FadeOut(self.rhs_box),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.35))

            heading = board_text("Transpose the -7", 22, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.45, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            box7 = SurroundingRectangle(eq[0][2:4], color=CHALK_AMBER, buff=0.08,
                                        corner_radius=0.06, stroke_width=3)
            # Parked on the LEFT so the flying "-7" (apex above the '=') never
            # crosses this label.
            note = board_text("Remove -7 from the LHS", 16, CHALK_PINK, "BOLD").move_to(
                np.array([-2.05, 2.0, 0]))
            self.play(Create(box7), FadeIn(note),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            # The 7 travels an arch over the '='; the sign flips at the top.
            t2 = rt(tracker.time_until_bookmark("b2"))
            start = eq[0][2:4].get_center()
            new_eq = MathTex("2x", r"\;=\;", "35+7", font_size=48)
            align_equals(new_eq, BOARD_CX, EQ_Y)
            new_eq[0][1].set_color(CHALK_CYAN)
            landing = new_eq[2][2:4].get_center()
            apex = np.array([BOARD_CX, 2.15, 0.0])

            mover = MathTex("-7", font_size=30).move_to(start)
            self.play(mover.animate.move_to(apex),
                      eq[0][2:4].animate.set_opacity(0.25), run_time=t2 * 0.45)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            mover_p = MathTex("+7", font_size=30, color=CHALK_GREEN).move_to(apex)
            self.play(ReplacementTransform(mover, mover_p),
                      Flash(apex, color=CHALK_YELLOW, flash_radius=0.45), run_time=0.3)
            self.add_sound(self.sfx["ding"], gain=-11)

            # The 7 finishes its crossing WHILE the equation updates, so the
            # chip is never parked on top of the old "35" for a static beat.
            self.play(mover_p.animate.move_to(landing),
                      TransformMatchingTex(eq, new_eq), FadeOut(mover_p),
                      FadeOut(box7), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self.eq = new_eq

            box357 = SurroundingRectangle(new_eq[2], color=CHALK_AMBER, buff=0.08,
                                          corner_radius=0.06, stroke_width=3)
            lbl357 = board_text("35 + 7 = 42", 16, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, -0.5, 0]))
            self.play(Create(box357), FadeIn(lbl357),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.4))

            eq42 = MathTex("2x", r"\;=\;", "42", font_size=48)
            align_equals(eq42, BOARD_CX, EQ_Y)
            eq42[0][1].set_color(CHALK_CYAN)
            self.play(TransformMatchingTex(new_eq, eq42), FadeOut(box357),
                      FadeOut(lbl357), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.eq = eq42

            rule = self.rule_card(r"-\ \longleftrightarrow\ +",
                                  "Across '=': minus becomes plus", CHALK_GREEN)
            rule.move_to(np.array([BOARD_CX, BOARD_TOP - 1.05, 0]))
            self.play(FadeIn(rule, shift=DOWN * 0.1), FadeOut(note),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["ding"], gain=-12)

            self.scene4_extras = VGroup(heading, rule)
            self._capture_srt(tracker)

        self.play(FadeOut(self.scene4_extras), run_time=0.4)
        self.wait(TRANSITION_HOLD)

    # -- Beat 5: Scene 5 — Transposing Multiplication / Division --------------
    def beat5_transpose_mult(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            eq = self.eq  # 2x = 42

            heading = board_text("Transpose the 2", 22, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.45, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.4))

            eq_times = MathTex(r"2\times x", r"\;=\;", "42", font_size=48)
            align_equals(eq_times, BOARD_CX, EQ_Y)
            eq_times[0][2].set_color(CHALK_CYAN)
            self.play(TransformMatchingTex(eq, eq_times),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-12)
            self.eq = eq_times

            box2 = SurroundingRectangle(eq_times[0], color=CHALK_AMBER, buff=0.08,
                                        corner_radius=0.06, stroke_width=3)
            # Parked above the multiplication (left side, clear of the flying
            # "2"'s arc over the '=').
            lbl2 = board_text("multiplied by 2", 15, CHALK_AMBER, "BOLD").move_to(
                np.array([eq_times[0].get_center()[0] - 0.6, 2.0, 0]))
            self.play(Create(box2), FadeIn(lbl2),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            strip = chalk_math(r"\text{Across '=': }\times \text{ becomes } \div",
                               size=15, color=CHALK_YELLOW).move_to(
                np.array([BOARD_CX, 1.55, 0]))
            self.play(FadeIn(strip), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            # The 2 crosses the '=' and lands below the fraction bar.
            t3 = rt(tracker.time_until_bookmark("b3"))
            start = eq_times[0][0].get_center()
            new_eq = MathTex("x", r"\;=\;", r"\frac{42}{2}", font_size=44)
            align_equals(new_eq, BOARD_CX, EQ_Y)
            new_eq[0].set_color(CHALK_CYAN)
            landing = new_eq[2][-1].get_center()
            apex = np.array([BOARD_CX, 2.15, 0.0])

            mover = MathTex("2", font_size=30).move_to(start)
            self.play(mover.animate.move_to(apex),
                      eq_times[0][0].animate.set_opacity(0.25), run_time=t3 * 0.45)
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(Flash(apex, color=CHALK_YELLOW, flash_radius=0.4), run_time=0.25)
            self.play(mover.animate.move_to(landing), run_time=t3 * 0.45)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(TransformMatchingTex(eq_times, new_eq), FadeOut(mover),
                      FadeOut(box2), run_time=rt(tracker.time_until_bookmark("b4") * 0.5))
            eq21 = MathTex("x", r"\;=\;", "21", font_size=50, color=CHALK_GREEN)
            align_equals(eq21, BOARD_CX, EQ_Y)
            self.play(TransformMatchingTex(new_eq, eq21),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self.eq = eq21

            ans_box = SurroundingRectangle(eq21, color=CHALK_GREEN, buff=0.2,
                                           corner_radius=0.1, stroke_width=3)
            ans_lbl = board_text("x = 21", 20, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -0.6, 0]))
            self.play(Create(ans_box), FadeIn(ans_lbl),
                      Flash(eq21, color=CHALK_GREEN, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["ding"], gain=-11)

            self.scene5_extras = VGroup(heading, lbl2, strip, ans_box, ans_lbl)
            self._capture_srt(tracker)

        self.play(FadeOut(self.scene5_extras), run_time=0.4)
        self.wait(TRANSITION_HOLD)

    # -- Beat 6: Scene 6 — How Do We Know the Answer Is Correct? --------------
    def beat6_verify(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("CHECK THE SOLUTION", 24, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.45, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            eq_orig = MathTex("2x-7", r"\;=\;", "35", font_size=40)
            align_equals(eq_orig, BOARD_CX, 0.85)
            eq_orig[0][1].set_color(CHALK_CYAN)
            # the solution chip sits directly above the x it replaces, so the
            # substitution arrow drops straight down
            sol = MathTex("x", r"\;=\;", "21", font_size=28, color=CHALK_GREEN).move_to(
                np.array([eq_orig[0][1].get_center()[0], 2.05, 0]))
            down_arrow = Arrow(sol.get_bottom(), eq_orig[0][1].get_top(), buff=0.1,
                               color=CHALK_GREEN, stroke_width=3)

            self.play(FadeIn(sol), Write(eq_orig), GrowArrow(down_arrow),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.55))

            sub1 = MathTex("2(", "21", ")-7", r"\;=\;", "35", font_size=40)
            align_equals(sub1, BOARD_CX, 0.85)
            # The solution chip stays ABOVE the equation: it pulses while the
            # equation itself shows the substitution.  (Sliding the chip down
            # onto the x parked a green "21" on top of "2x-7 = 35".)
            self.play(Indicate(sol[2], color=CHALK_GREEN, scale_factor=1.12),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.45))
            self.play(TransformMatchingTex(eq_orig, sub1),
                      FadeOut(sol), FadeOut(down_arrow),
                      Flash(sub1[1], color=CHALK_GREEN, flash_radius=0.4),
                      run_time=0.35)
            self.add_sound(self.sfx["click"], gain=-15)

            sub2 = MathTex("42-7", r"\;=\;", "35", font_size=40)
            align_equals(sub2, BOARD_CX, 0.85)
            self.play(TransformMatchingTex(sub1, sub2),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            sub3 = MathTex("35", r"\;=\;", "35", font_size=44)
            align_equals(sub3, BOARD_CX, 0.85)
            self.play(TransformMatchingTex(sub2, sub3),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-12)

            ck = tick_beside(sub3, CHALK_GREEN, 0.44, 0.4)
            ok_lbl = board_text("LHS = RHS", 20, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -0.5, 0]))
            self.play(Create(ck), FadeIn(ok_lbl),
                      Flash(sub3, color=CHALK_GREEN, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 7: Scene 7 — The Transposition Rules -----------------------------
    def rule_card(self, syms: str, desc: str, color: str) -> VGroup:
        card = RoundedRectangle(corner_radius=0.06, width=5.4, height=0.62,
                                stroke_color=color, stroke_width=1.8,
                                fill_color="#15202B", fill_opacity=0.92)
        s = MathTex(syms, font_size=24, color=color).move_to(card.get_left() + RIGHT * 1.45)
        d = board_text(desc, 12, CHALK_WHITE).move_to(card.get_left() + RIGHT * 3.45)
        return VGroup(card, s, d)

    def beat7_rules(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("TRANSPOSITION RULES", 26, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.4, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.4))

            big_eq = MathTex("=", font_size=64, color=CHALK_YELLOW).move_to(
                np.array([BOARD_CX, 0.5, 0]))
            self.play(FadeIn(big_eq, scale=1.5),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-12)

            row1 = self.rule_card(r"+\ \longleftrightarrow\ -",
                                  "Addition  <->  Subtraction", CHALK_GREEN)
            row2 = self.rule_card(r"\times\ \longleftrightarrow\ \div",
                                  "Multiplication  <->  Division", CHALK_YELLOW)
            row1.move_to(np.array([BOARD_CX, 2.15, 0]))
            row2.move_to(np.array([BOARD_CX, -0.95, 0]))

            # "+" crosses the '=' and becomes "-" (all four sub-steps split
            # one bookmark's budget so the motion never outruns the voice).
            self.play(FadeIn(row1, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.25))
            m1 = MathTex("+", font_size=30, color=CHALK_GREEN).move_to(
                np.array([-1.7, 0.5, 0]))
            self.play(m1.animate.move_to(np.array([BOARD_CX, 1.45, 0])),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.25))
            m1m = MathTex("-", font_size=30, color=CHALK_GREEN).move_to(m1.get_center())
            self.play(ReplacementTransform(m1, m1m),
                      Flash(m1m.get_center(), color=CHALK_YELLOW, flash_radius=0.4),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.25))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(m1m.animate.move_to(np.array([2.7, 0.5, 0])),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.25))

            # "-" crosses back and becomes "+".
            self.play(FadeOut(m1m), run_time=rt(MIN_RT))
            m2 = MathTex("-", font_size=30, color=CHALK_GREEN).move_to(
                np.array([2.7, 0.5, 0]))
            self.play(m2.animate.move_to(np.array([BOARD_CX, 1.45, 0])),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.35))
            m2p = MathTex("+", font_size=30, color=CHALK_GREEN).move_to(m2.get_center())
            self.play(ReplacementTransform(m2, m2p),
                      Flash(m2p.get_center(), color=CHALK_YELLOW, flash_radius=0.4),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.3))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(m2p.animate.move_to(np.array([-1.7, 0.5, 0])),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.35))

            # "x" crosses and becomes "/".
            self.play(FadeOut(m2p), FadeIn(row2, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.25))
            m3 = MathTex(r"\times", font_size=30, color=CHALK_YELLOW).move_to(
                np.array([-1.7, 0.5, 0]))
            self.play(m3.animate.move_to(np.array([BOARD_CX, 1.45, 0])),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.25))
            m3d = MathTex(r"\div", font_size=30, color=CHALK_YELLOW).move_to(m3.get_center())
            self.play(ReplacementTransform(m3, m3d),
                      Flash(m3d.get_center(), color=CHALK_YELLOW, flash_radius=0.4),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.25))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(m3d.animate.move_to(np.array([2.7, 0.5, 0])),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.25))

            # "/" crosses back and becomes "x".
            self.play(FadeOut(m3d), run_time=rt(MIN_RT))
            m4 = MathTex(r"\div", font_size=30, color=CHALK_YELLOW).move_to(
                np.array([2.7, 0.5, 0]))
            self.play(m4.animate.move_to(np.array([BOARD_CX, 1.45, 0])),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.35))
            m4t = MathTex(r"\times", font_size=30, color=CHALK_YELLOW).move_to(m4.get_center())
            self.play(ReplacementTransform(m4, m4t),
                      Flash(m4t.get_center(), color=CHALK_YELLOW, flash_radius=0.4),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.3))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(m4t.animate.move_to(np.array([-1.7, 0.5, 0])),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.35))
            self.play(FadeOut(m4t), run_time=rt(MIN_RT))

            golden = board_text("Across '=': every operation flips to its inverse.",
                                16, CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX, -1.75, 0]))
            self.play(FadeIn(golden), run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 7b: Cross Multiplication (fraction = fraction) -------------------
    def beat7b_cross_multiply(self) -> None:
        """When both sides are fractions, transposition becomes cross
        multiplication: a/b = c/d  ->  a*d = b*c, worked on x/4 = 3/2."""
        with self.voiceover(text=NARRATION["cross"]) as tracker:
            self.reset_board()

            heading = board_text("Cross Multiplication", 26, CHALK_AMBER,
                                 "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.45, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            rule = chalk_math(r"\frac{a}{b} = \frac{c}{d} \;\Longrightarrow\; "
                              r"a \times d = b \times c", size=34,
                              color=CHALK_CYAN).move_to(np.array([BOARD_CX, 1.7, 0]))
            self.play(Write(rule), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            ex = MathTex(r"\frac{x}{4}", r"\;=\;", r"\frac{3}{2}", font_size=46)
            align_equals(ex, BOARD_CX, 0.7)
            self.play(Write(ex), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # The two diagonals are shown by WHERE EACH NUMBER TRAVELS
            # (flying copies) instead of arrows drawn across the equation --
            # the letters stay completely clear.
            step = MathTex("x", r"\times", "2", r"\;=\;", "4", r"\times", "3",
                           font_size=40).move_to(np.array([BOARD_CX, -0.5, 0]))
            step[0].set_color(CHALK_CYAN)
            step[2].set_color(CHALK_CYAN)
            step[4].set_color(CHALK_PINK)
            step[6].set_color(CHALK_PINK)
            src_x = MathTex("x", font_size=34, color=CHALK_CYAN).move_to(
                ex[0].get_top() + UP * 0.02)
            src_2 = MathTex("2", font_size=34, color=CHALK_CYAN).move_to(
                ex[2].get_bottom() + DOWN * 0.02)
            src_4 = MathTex("4", font_size=34, color=CHALK_PINK).move_to(
                ex[0].get_bottom() + DOWN * 0.02)
            src_3 = MathTex("3", font_size=34, color=CHALK_PINK).move_to(
                ex[2].get_top() + UP * 0.02)

            self.play(TransformFromCopy(src_x, step[0]),
                      TransformFromCopy(src_2, step[2]), Write(step[1]),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            self.play(TransformFromCopy(src_4, step[4]),
                      TransformFromCopy(src_3, step[6]),
                      Write(step[3]), Write(step[5]),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            two_x = MathTex("2x", r"\;=\;", "12", font_size=40)
            align_equals(two_x, BOARD_CX, -0.5)
            self.play(TransformMatchingTex(step, two_x),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.45))
            six = MathTex("x", r"\;=\;", "6", font_size=46, color=CHALK_GREEN)
            align_equals(six, BOARD_CX, -1.45)
            self.play(TransformMatchingTex(two_x, six),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            ans_box = SurroundingRectangle(six, color=CHALK_GREEN, buff=0.2,
                                           corner_radius=0.1, stroke_width=2.5)
            self.play(Create(ans_box), run_time=0.25)
            self.add_sound(self.sfx["success"], gain=-11)

            check = chalk_math(r"\frac{6}{4} \;=\; \frac{3}{2}", size=30,
                               color=CHALK_GREEN).move_to(np.array([BOARD_CX, -2.15, 0]))
            ck = tick_beside(check, CHALK_GREEN, 0.34, 0.3)
            self.play(FadeIn(check), Create(ck),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["ding"], gain=-12)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 8: Scene 8 — Real-World Application: The Park --------------------
    def beat8_park(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("Real-World: The Park Puzzle", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, BOARD_TOP - 0.42, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            # ---- the park (left side): a simple but real-looking plot --
            # grass texture, two trees planted at the top corners, a small
            # pond -- with only the TWO dimension arrows the problem uses:
            # breadth (x) along the bottom, length (x+17) up the side.
            park = Rectangle(width=3.5, height=2.3, stroke_color=CHALK_CYAN,
                             stroke_width=2.5).move_to(np.array([-1.85, 0.55, 0]))
            park.set_fill("#1E3B22", opacity=0.6)
            tree1 = tree_icon(np.array([-3.15, 1.35, 0]), scale=0.85)
            tree2 = tree_icon(np.array([-0.7, 1.35, 0]), scale=0.85)
            pond = pond_icon(np.array([-2.65, 0.1, 0]), scale=0.95)
            lawn = sparse_lawn(park,
                               blockers=((np.array([-2.65, 0.1, 0]), 0.6),
                                         (np.array([-3.15, 1.2, 0]), 0.45),
                                         (np.array([-0.7, 1.2, 0]), 0.45)),
                               color=CHALK_GREEN)

            ar_bot = DoubleArrow(park.get_left(), park.get_right(), buff=0,
                                 color=CHALK_GREEN, stroke_width=2.2).next_to(
                park, DOWN, buff=0.1)
            ar_r = DoubleArrow(park.get_bottom(), park.get_top(), buff=0,
                               color=CHALK_GREEN, stroke_width=2.2).next_to(
                park, RIGHT, buff=0.1)
            # dimension labels sit outside their own arrow (no overlaps)
            lbl_x_grp = VGroup(
                MathTex("x", font_size=30, color=CHALK_CYAN),
                board_text("breadth", 14, CHALK_CYAN),
            ).arrange(DOWN, buff=0.06).next_to(ar_bot, DOWN, buff=0.1)
            lbl_l_grp = VGroup(
                MathTex("x+17", font_size=28, color=CHALK_PINK),
                board_text("length", 14, CHALK_PINK),
            ).arrange(DOWN, buff=0.06).next_to(ar_r, RIGHT, buff=0.14)

            self.play(Create(park), FadeIn(tree1), FadeIn(tree2), FadeIn(pond),
                      FadeIn(lawn), Create(ar_bot), Create(ar_r),
                      FadeIn(lbl_x_grp), FadeIn(lbl_l_grp),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            # ---- worked solution column (right half) ----
            col_x = 3.15
            perim = board_text("Perimeter = 178 m", 18, CHALK_YELLOW, "BOLD").move_to(
                np.array([col_x, 2.05, 0]))
            self.play(FadeIn(perim), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            e1 = MathTex(r"2[(x+17)+x]", "=", "178", font_size=30).move_to(
                np.array([col_x, 1.25, 0]))
            # "The perimeter formula adds all four sides..." -- the park
            # outline pulses instead of four separate arrows tracing it.
            self.play(Write(e1), Indicate(park, color=CHALK_GREEN, scale_factor=1.03),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-12)

            # Each step is KEPT on the board, building a full worked
            # solution down the right column (fills the board and shows
            # the whole progression instead of only the last line).
            e2 = MathTex("4x+34", "=", "178", font_size=30).move_to(
                np.array([col_x, 0.3, 0]))
            e2[0][1].set_color(CHALK_CYAN)
            self.play(Write(e2), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            e3 = MathTex("4x", "=", "178-34", font_size=30).move_to(
                np.array([col_x, -0.6, 0]))
            e3[0][1].set_color(CHALK_CYAN)
            self.play(Write(e3), run_time=rt(tracker.time_until_bookmark("b4") * 0.5))
            e4 = MathTex("4x", "=", "144", font_size=30).move_to(e3.get_center())
            e4[0][1].set_color(CHALK_CYAN)
            self.play(TransformMatchingTex(e3, e4),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.5))
            self.add_sound(self.sfx["click"], gain=-15)

            e5 = MathTex("x", "=", "36", font_size=34, color=CHALK_GREEN).move_to(
                np.array([col_x, -1.45, 0]))
            self.play(Write(e5), run_time=rt(tracker.time_until_bookmark("b5") * 0.6))
            ans_box = SurroundingRectangle(e5, color=CHALK_GREEN, buff=0.18,
                                           corner_radius=0.1, stroke_width=2.5)
            self.play(Create(ans_box), run_time=rt(tracker.time_until_bookmark("b5") * 0.4))
            self.add_sound(self.sfx["success"], gain=-11)

            # ---- final dimensions on the park itself ----
            final_b = board_text("Breadth = 36 m", 16, CHALK_GREEN, "BOLD").next_to(
                ar_bot, DOWN, buff=0.1)
            final_l = board_text("Length = 53 m", 16, CHALK_GREEN, "BOLD").next_to(
                ar_r, RIGHT, buff=0.12)
            strip = chalk_math(r"\text{Unknown} \rightarrow \text{Equation} "
                               r"\rightarrow \text{Solution}", size=20,
                               color=CHALK_CYAN).move_to(np.array([BOARD_CX, -2.25, 0]))
            self.play(ReplacementTransform(lbl_x_grp, final_b),
                      ReplacementTransform(lbl_l_grp, final_l),
                      FadeIn(strip),
                      run_time=rt(tracker.time_until_bookmark("b6")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 9: Scene 9 — Student Challenge -----------------------------------
    def beat9_challenge(self) -> None:
        with self.voiceover(text=NARRATION["scene9_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", 30, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.5, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            eq_c = MathTex("3x+1", r"\;=\;", "16", font_size=48)
            align_equals(eq_c, BOARD_CX, 0.8)
            eq_c[0][1].set_color(CHALK_CYAN)
            self.play(Write(eq_c), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            find_lbl = board_text("Find x.", 22, CHALK_WHITE).move_to(
                np.array([BOARD_CX, -0.1, 0]))
            self.play(FadeIn(find_lbl), run_time=rt(tracker.time_until_bookmark("b2") * 0.4))
            which_lbl = board_text("Which term moves first?", 18, CHALK_YELLOW,
                                   "BOLD").move_to(np.array([BOARD_CX, -0.8, 0]))
            self.play(FadeIn(which_lbl), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            pause_lbl = board_text("Pause and try it", 20, CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX, -1.5, 0]))
            self.play(FadeIn(pause_lbl), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.challenge_q = VGroup(heading, eq_c, find_lbl, which_lbl, pause_lbl)
            self._capture_srt(tracker)

        # Series-standard 10-second THINK clock (dims the whole board except
        # the badge while students pause and try).
        play_challenge_countdown(self, seconds=10, sfx=self.sfx)

        with self.voiceover(text=NARRATION["scene9_reveal"]) as tracker:
            eq_c = self.challenge_q[1]
            self.play(FadeOut(self.challenge_q[3]), FadeOut(self.challenge_q[4]),
                      run_time=0.3)

            box1 = SurroundingRectangle(eq_c[0][2:4], color=CHALK_AMBER, buff=0.08,
                                        corner_radius=0.06, stroke_width=3)
            strip1 = board_text("Across '=': + becomes -", 14, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, 2.35, 0]))
            self.play(Create(box1), FadeIn(strip1),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.5))

            eq_c2 = MathTex("3x", r"\;=\;", "16-1", font_size=48)
            align_equals(eq_c2, BOARD_CX, 0.8)
            eq_c2[0][1].set_color(CHALK_CYAN)
            self.play(TransformMatchingTex(eq_c, eq_c2), FadeOut(box1),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["click"], gain=-15)

            eq_c3 = MathTex("3x", r"\;=\;", "15", font_size=48)
            align_equals(eq_c3, BOARD_CX, 0.8)
            eq_c3[0][1].set_color(CHALK_CYAN)
            self.play(TransformMatchingTex(eq_c2, eq_c3),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.35))
            self.add_sound(self.sfx["click"], gain=-15)

            box3 = SurroundingRectangle(eq_c3[0], color=CHALK_AMBER, buff=0.08,
                                        corner_radius=0.06, stroke_width=3)
            eq_c4 = MathTex("x", r"\;=\;", r"\frac{15}{3}", font_size=48)
            align_equals(eq_c4, BOARD_CX, 0.8)
            eq_c4[0].set_color(CHALK_CYAN)
            self.play(Create(box3), run_time=rt(tracker.time_until_bookmark("b1") * 0.25))
            self.play(TransformMatchingTex(eq_c3, eq_c4), FadeOut(box3),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            eq_c5 = MathTex("x", r"\;=\;", "5", font_size=52, color=CHALK_GREEN)
            align_equals(eq_c5, BOARD_CX, 0.8)
            self.play(TransformMatchingTex(eq_c4, eq_c5),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            ans_box = SurroundingRectangle(eq_c5, color=CHALK_GREEN, buff=0.22,
                                           corner_radius=0.1, stroke_width=3)
            ck = tick_beside(eq_c5, CHALK_GREEN, 0.42, 0.45)
            well = board_text("Excellent! x = 5", 20, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -0.85, 0]))
            self.play(Create(ans_box), Create(ck), FadeIn(well),
                      Flash(eq_c5, color=CHALK_GREEN, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-12)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 10: Scene 10 — Finalization / Recap ------------------------------
    def bullet_row(self, n: int, items: list, color: str) -> VGroup:
        """A numbered summary bullet row (series summary style)."""
        badge = Circle(radius=0.2, stroke_color=color, stroke_width=2,
                       fill_color=color, fill_opacity=0.18)
        num = board_text(str(n), 18, color, "BOLD").move_to(badge.get_center())
        block_items = [
            board_text(it, 20, CHALK_WHITE) if isinstance(it, str) else it
            for it in items
        ]
        text_block = VGroup(*block_items).arrange(DOWN, buff=0.07, aligned_edge=LEFT)
        row = VGroup(VGroup(badge, num), text_block).arrange(RIGHT, buff=0.3)
        return row

    def beat10_recap(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("Summary", 34, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_TOP - 0.5, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-15)

            b1 = self.bullet_row(1, [
                "An equation has two sides — the LHS and the RHS —",
                "joined by the equality sign. They hold the same value.",
            ], CHALK_CYAN)
            b2 = self.bullet_row(2, [
                "x is the variable. Transposition flips each operation",
                "as it crosses '=':  minus becomes plus, times becomes divide.",
            ], CHALK_GREEN)
            b3 = self.bullet_row(3, [
                MathTex(r"2x-7=35 \rightarrow 2x=42 \rightarrow x=21", font_size=22),
                "Substituting back checks it: 35 = 35.",
            ], CHALK_PINK)
            bullets = VGroup(b1, b2, b3).arrange(DOWN, buff=0.34, aligned_edge=LEFT)
            bullets.move_to(np.array([BOARD_CX, BOARD_CY + 0.25, 0]))
            bullets.shift(LEFT * (bullets.get_left()[0] + 4.0))

            self.play(FadeIn(b1, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(b2, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(b3, shift=RIGHT * 0.15),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            takeaway = board_text("Keep the equality true. Isolate the unknown.",
                                  21, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.75, 0]))
            self.play(FadeIn(takeaway, shift=UP * 0.1),
                      Flash(takeaway, color=CHALK_YELLOW, flash_radius=0.9),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.7))
            self.add_sound(self.sfx["ding"], gain=-12)
            self.play(Circumscribe(takeaway, color=CHALK_YELLOW, stroke_width=3,
                                   time_width=0.6), run_time=0.5)

            summary_group = VGroup(heading, bullets, takeaway)
            self.play(FadeOut(summary_group),
                      run_time=rt(tracker.time_until_bookmark("b5") * 0.3))

            thanks = board_text("Thank You for Watching!", 42, CHALK_WHITE, "BOLD")
            thanks2 = board_text("See you in the next lesson :)", 26, CHALK_CYAN)
            thanks_group = VGroup(thanks, thanks2).arrange(DOWN, buff=0.3).move_to(
                np.array([BOARD_CX, BOARD_CY, 0]))
            self.play(Write(thanks), run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["ding"], gain=-11)
            self.play(FadeIn(thanks2, shift=UP * 0.1),
                      run_time=rt(tracker.get_remaining_duration()))
            self.play(Circumscribe(thanks_group, color=CHALK_AMBER, stroke_width=3,
                                   time_width=0.5), run_time=0.5)
            self.add_sound(self.sfx["success"], gain=-11)

            self._capture_srt(tracker)

        self.wait(END_HOLD)


if __name__ == "__main__":
    pass

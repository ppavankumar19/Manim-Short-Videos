"""
The Pythagorean Theorem: History + ADEPT Method
Chalkboard Story-Mode Lesson for Telangana Class 8 Mathematics.

Visual Standards:
  - Top-Right Corner: Elegant persistent 'Mathematics' badge (no Class 08).
  - Scene 1 Intro: Realistic ancient land plot diagram with survey pegs, river/marsh obstacle,
    measured boundary sides a & b, and diagonal distance '?' across the obstacle.
  - Zero overlaps across all 15 scenes:
    - Scene 2: 12-knot rope card has wide clearance from Side = 5 hypotenuse.
    - Scene 3: Equation card 9 + 16 = 25 separated with 1.5+ unit margin from orange square.
    - Scene 5: '25 Empty Slots' label positioned above the grid (no cell occlusion).
    - Scene 6: Result card well separated from hypotenuse square; all 25 tiles fade out cleanly.
    - Scene 12: Native vector checkmark and cross icons (no font missing glyphs).
    - Scene 13: Ladder label positioned clear of ladder line; clean unit text rendering.
    - Scene 14: Timer bar completely fades out after countdown (zero leftover slivers).
    - Scene 15: Checklist header fades out for outro card ('Thank You for Watching!').
  - Color convention: a = Blue (#60A5FA), b = Green (#4ADE80), c = Orange (#FB923C).
  - c is always the hypotenuse, strictly opposite the 90-degree right angle.
  - Voiceover via Gemini Zephyr generative voice + real word-boundary SRT export.
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
    Square, CubicBezier,
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
CHALK_GREEN = "#4ADE80"  # b = green
CHALK_BLUE = "#60A5FA"   # a = blue
CHALK_ORANGE = "#FB923C" # c = orange
FONT = "Segoe Print"

END_HOLD = 2.0
MIN_RT = 0.12


def rt(seconds: float, floor: float = MIN_RT) -> float:
    return max(floor, float(seconds))


def board_text(
    text: str,
    font_size: int = 24,
    color: str = CHALK_WHITE,
    weight: str = "NORMAL",
) -> Text:
    return Text(text, font=FONT, font_size=font_size, color=color, weight=weight)


# ------------------------------------------------------------- scripts -----
SCRIPTS: dict[str, str] = {
    "scene1": (
        "Thousands of years ago, people needed to measure land,<bookmark mark='b1'/> "
        "construct buildings, and create accurate right angles.<bookmark mark='b2'/> "
        "But how could they find a distance that was difficult to measure directly?"
    ),
    "scene2": (
        "Ancient builders and surveyors discovered useful patterns.<bookmark mark='b1'/> "
        "A triangle with sides three, four, and five creates a perfect right angle.<bookmark mark='b2'/> "
        "Twelve equally spaced knots formed this sacred surveying triangle."
    ),
    "scene3": (
        "Mathematicians realized that this was not just a useful trick.<bookmark mark='b1'/> "
        "There was a deeper geometric relationship between the sides of any right triangle.<bookmark mark='b2'/>"
    ),
    "scene4": (
        "The relationship was known across ancient civilizations,<bookmark mark='b1'/> "
        "but became famous through Pythagoras and the Greek tradition of proof:<bookmark mark='b2'/> "
        "a squared plus b squared equals c squared!"
    ),
    "scene5": (
        "Imagine these squares as floor tiles.<bookmark mark='b1'/> "
        "The first square has nine tiles, and the second has sixteen tiles.<bookmark mark='b2'/> "
        "Together, they total exactly twenty-five tiles."
    ),
    "scene6": (
        "Watch closely:<bookmark mark='b1'/> "
        "when we combine the nine and sixteen tiles,<bookmark mark='b2'/> "
        "they perfectly tile the twenty-five square on the longest side!<bookmark mark='b3'/> "
        "Nine plus sixteen equals twenty-five."
    ),
    "scene7": (
        "In a right triangle,<bookmark mark='b1'/> "
        "the two shorter sides that meet at ninety degrees are called legs: a and b.<bookmark mark='b2'/> "
        "The longest side, directly opposite the right angle, is the hypotenuse, c."
    ),
    "scene8": (
        "Each square's area represents the side length squared.<bookmark mark='b1'/> "
        "The area of square a, plus the area of square b,<bookmark mark='b2'/> "
        "equals the area of square c!<bookmark mark='b3'/> "
        "Thus: a squared plus b squared equals c squared."
    ),
    "scene9": (
        "Let's test our three-four-five triangle!<bookmark mark='b1'/> "
        "Three squared plus four squared equals c squared.<bookmark mark='b2'/> "
        "Nine plus sixteen gives twenty-five.<bookmark mark='b3'/> "
        "Taking the square root, c equals five!"
    ),
    "scene10": (
        "In plain English:<bookmark mark='b1'/> "
        "small square plus medium square equals large square!<bookmark mark='b2'/> "
        "Geometry and algebra expressing the exact same truth."
    ),
    "scene11": (
        "The formal theorem states:<bookmark mark='b1'/> "
        "In any right-angled triangle,<bookmark mark='b2'/> "
        "the square of the hypotenuse equals the sum of the squares of the other two sides."
    ),
    "scene12": (
        "Beware of this critical rule!<bookmark mark='b1'/> "
        "The Pythagorean theorem works only for right triangles.<bookmark mark='b2'/> "
        "If there is no ninety-degree angle, this formula cannot be used!"
    ),
    "scene13": (
        "In the real world:<bookmark mark='b1'/> "
        "if a ladder reaches eight meters up a wall, and sits six meters from the base,<bookmark mark='b2'/> "
        "six squared plus eight squared equals one hundred.<bookmark mark='b3'/> "
        "The ladder is exactly ten meters long!"
    ),
    "scene14": (
        "Now, it's your turn!<bookmark mark='b1'/> "
        "A right triangle has legs five and twelve.<bookmark mark='b2'/> "
        "What is the hypotenuse?<bookmark mark='b3'/> "
        "Five squared plus twelve squared is one hundred sixty-nine.<bookmark mark='b4'/> "
        "The hypotenuse is thirteen!"
    ),
    "scene15": (
        "To recap:<bookmark mark='b1'/> "
        "confirm the right angle, identify the hypotenuse c,<bookmark mark='b2'/> "
        "square the two legs, add them, and take the square root!<bookmark mark='b3'/> "
        "Thank you for watching, and see you next time!"
    ),
}


class PythagoreanStory(VoiceoverScene):
    """Story-mode chalkboard lesson: The Pythagorean Theorem (ADEPT Method)."""

    def construct(self) -> None:
        self.set_speech_service(get_speech_service(), create_subcaption=False)
        self.sfx = load_sfx()
        self._srt_entries: list[tuple[float, float, str]] = []

        self.add_background()
        
        # 15 Scenes
        self.beat_scene1_original_problem()
        self.beat_scene2_ancient_pattern()
        self.beat_scene3_from_pattern_to_math()
        self.beat_scene4_historical_naming()
        self.beat_scene5_analogy_tile_setup()
        self.beat_scene6_analogy_visual_payoff()
        self.beat_scene7_diagram_anatomy()
        self.beat_scene8_diagram_becomes_equation()
        self.beat_scene9_worked_example()
        self.beat_scene10_plain_english()
        self.beat_scene11_technical_definition()
        self.beat_scene12_misconception_check()
        self.beat_scene13_real_world_application()
        self.beat_scene14_student_challenge()
        self.beat_scene15_final_recap()

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
        teacher.height = 3.4
        teacher.move_to(np.array([
            config.frame_width / 2 - teacher.width / 2 + 0.45,
            -config.frame_height / 2 + teacher.height / 2 - 0.1,
            0,
        ]))
        self.add(teacher)

        # Persistent 'Mathematics' badge at top-most right corner (No Class 08)
        math_badge = self._pill_badge("Mathematics", CHALK_YELLOW, font_size=16)
        math_badge.move_to(np.array([4.4, 3.15, 0]))
        math_badge.set_z_index(5)
        self.add(math_badge)

    # -- pill badge helper -----------------------------------------------
    def _pill_badge(self, text: str, color: str, font_size: int = 18) -> VGroup:
        t = board_text(text, font_size, color, "BOLD")
        box = RoundedRectangle(
            corner_radius=0.08,
            width=t.width + 0.30,
            height=t.height + 0.16,
            stroke_color=color,
            stroke_width=1.5,
            fill_color="#141414",
            fill_opacity=0.85,
        )
        t.move_to(box.get_center())
        return VGroup(box, t)

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
        srt_dir = _HERE / "media" / "videos" / "pythagorean_story"
        srt_dir.mkdir(parents=True, exist_ok=True)
        srt_path = srt_dir / "PythagoreanStory.real.srt"

        def fmt_tc(s: float) -> str:
            # round to whole milliseconds FIRST, then split: rounding the
            # fraction on its own can give ms = 1000, which writes a
            # four-digit millisecond field -- invalid SRT that strict
            # parsers drop.  See fix_srt_timestamps.py.
            total = int(round(max(float(s), 0.0) * 1000))
            hh = total // 3_600_000
            mm = (total // 60_000) % 60
            ss = (total // 1000) % 60
            ms = total % 1000
            return f"{hh:02d}:{mm:02d}:{ss:02d},{ms:03d}"
        with open(srt_path, "w", encoding="utf-8") as f:
            for idx, (t0, t1, line) in enumerate(self._srt_entries, 1):
                f.write(f"{idx}\n{fmt_tc(t0)} --> {fmt_tc(t1)}\n{line}\n\n")
        print(f"[real SRT written] {srt_path}")

    # =========================================================================
    # SCENE 1: The Original Problem (Realistic Land Plot & Surveyor Obstacle)
    # =========================================================================
    def beat_scene1_original_problem(self) -> None:
        with self.voiceover(text=SCRIPTS["scene1"]) as tracker:
            title = board_text("Ancient Land Measurement", 28, CHALK_YELLOW, "BOLD").move_to(np.array([0, 2.45, 0]))
            self.play(FadeIn(title, shift=DOWN * 0.15), run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.add_sound(self.sfx["pop"], gain=-12)

            # Realistic Ancient Field Plot with boundary pegs and natural obstacle
            field_w, field_h = 4.4, 2.5
            center_plot = np.array([0.15, -0.05, 0])
            p_dl = center_plot + np.array([-field_w / 2, -field_h / 2, 0])
            p_dr = center_plot + np.array([field_w / 2, -field_h / 2, 0])
            p_ur = center_plot + np.array([field_w / 2, field_h / 2, 0])
            p_ul = center_plot + np.array([-field_w / 2, field_h / 2, 0])

            # Perimeter plot outline
            field_rect = Polygon(p_dl, p_dr, p_ur, p_ul, stroke_color=CHALK_WHITE, stroke_width=2.5, fill_color="#182A24", fill_opacity=0.45)

            # Realistic subtle crop furrows / grid lines
            furrows = VGroup()
            for k in range(1, 4):
                y_pos = p_dl[1] + k * (field_h / 4.0)
                furrows.add(Line(np.array([p_dl[0], y_pos, 0]), np.array([p_dr[0], y_pos, 0]), color="#2C4A3E", stroke_width=1.0))

            # Realistic River / Marsh obstacle in middle making direct measurement impossible
            # Placed lower and narrower so diagonal passes cleanly above its label
            river_pts = [
                center_plot + np.array([-0.6, 0.4, 0]),
                center_plot + np.array([0.0, -0.1, 0]),
                center_plot + np.array([0.5, -0.7, 0]),
                center_plot + np.array([0.9, -1.0, 0]),
                center_plot + np.array([1.2, -1.0, 0]),
                center_plot + np.array([0.8, -0.5, 0]),
                center_plot + np.array([0.3, 0.1, 0]),
                center_plot + np.array([-0.3, 0.6, 0]),
            ]
            river_marsh = Polygon(*river_pts, stroke_color=CHALK_CYAN, stroke_width=1.5, fill_color="#10383C", fill_opacity=0.65)
            # Label placed below the marsh, safely clear of the diagonal line
            lbl_marsh = board_text("Marsh Obstacle", 13, CHALK_CYAN).move_to(center_plot + np.array([0.65, -0.65, 0]))

            # Stone boundary pegs at the 4 corners
            corner_markers = VGroup()
            for pt in [p_dl, p_dr, p_ur, p_ul]:
                ring = Circle(radius=0.12, stroke_color=CHALK_YELLOW, stroke_width=2.0).move_to(pt)
                core = Dot(pt, radius=0.06, color=CHALK_YELLOW)
                corner_markers.add(VGroup(ring, core))

            # Measured boundary sides
            side_a = Line(p_dl, p_dr, color=CHALK_BLUE, stroke_width=5.0)
            side_b = Line(p_dl, p_ul, color=CHALK_GREEN, stroke_width=5.0)
            
            lbl_a = board_text("Width = a (Measured)", 17, CHALK_BLUE, "BOLD").next_to(side_a, DOWN, buff=0.15)
            lbl_b = board_text("Length = b (Measured)", 16, CHALK_GREEN, "BOLD").next_to(side_b, RIGHT, buff=0.15).shift(UP * 0.4)

            # Surveyor 90° angle mark
            sq_corner = Square(side_length=0.25, stroke_color=CHALK_YELLOW, stroke_width=2.0).move_to(p_dl + np.array([0.125, 0.125, 0]))
            deg_lbl = board_text("90°", 13, CHALK_YELLOW).next_to(sq_corner, UR, buff=0.05)

            self.play(
                Create(field_rect),
                Create(furrows),
                DrawBorderThenFill(river_marsh), FadeIn(lbl_marsh),
                FadeIn(corner_markers),
                Create(side_a), Create(side_b),
                FadeIn(lbl_a), FadeIn(lbl_b),
                Create(sq_corner), FadeIn(deg_lbl),
                run_time=rt(tracker.time_until_bookmark("b2")),
            )
            self.add_sound(self.sfx["whoosh"], gain=-13)

            # Unknown diagonal distance across the obstacle
            diag = DashedLine(p_dl, p_ur, color=CHALK_ORANGE, stroke_width=4.0, dash_length=0.12)
            card_q = RoundedRectangle(corner_radius=0.1, width=3.4, height=0.6, stroke_color=CHALK_ORANGE, stroke_width=2.0, fill_color="#20140A", fill_opacity=0.9).move_to(center_plot + np.array([-0.25, 0.85, 0]))
            lbl_q = board_text("Diagonal Distance = ?", 18, CHALK_ORANGE, "BOLD").move_to(card_q.get_center())
            q_badge = VGroup(card_q, lbl_q)

            self.play(Create(diag), FadeIn(q_badge, shift=DOWN * 0.1), run_time=rt(tracker.get_remaining_duration()))
            self.play(Indicate(q_badge, color=CHALK_YELLOW), run_time=0.6)
            self.add_sound(self.sfx["ding"], gain=-12)

            self._capture_srt(tracker)

        self.play(
            FadeOut(VGroup(
                title, field_rect, furrows, river_marsh, lbl_marsh, corner_markers,
                side_a, side_b, lbl_a, lbl_b, sq_corner, deg_lbl, diag, q_badge
            )),
            run_time=0.4,
        )

    # =========================================================================
    # SCENE 2: Ancient 3-4-5 Pattern (Rope knots & right angle, zero overlap)
    # =========================================================================
    def beat_scene2_ancient_pattern(self) -> None:
        with self.voiceover(text=SCRIPTS["scene2"]) as tracker:
            title = board_text("The Ancient 3-4-5 Rope Triangle", 28, CHALK_CYAN, "BOLD").move_to(np.array([0, 2.45, 0]))
            self.play(FadeIn(title, shift=DOWN * 0.15), run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.add_sound(self.sfx["pop"], gain=-12)

            # Triangle shifted left to guarantee zero overlap with rope info card
            s = 0.50
            p_right = np.array([-2.4, -0.9, 0])
            p_a = p_right + np.array([3 * s, 0, 0])
            p_b = p_right + np.array([0, 4 * s, 0])

            tri = Polygon(p_right, p_a, p_b, stroke_color=CHALK_WHITE, stroke_width=3.0, fill_color="#2A241C", fill_opacity=0.45)
            
            line_a = Line(p_right, p_a, color=CHALK_BLUE, stroke_width=4.5)
            line_b = Line(p_right, p_b, color=CHALK_GREEN, stroke_width=4.5)
            line_c = Line(p_b, p_a, color=CHALK_ORANGE, stroke_width=4.5)

            lbl_a = board_text("Side = 3", 19, CHALK_BLUE, "BOLD").next_to(line_a, DOWN, buff=0.16)
            lbl_b = board_text("Side = 4", 19, CHALK_GREEN, "BOLD").next_to(line_b, LEFT, buff=0.16)
            lbl_c = board_text("Side = 5", 19, CHALK_ORANGE, "BOLD").move_to(line_c.get_center() + np.array([0.45, 0.25, 0]))

            sq_corner = Square(side_length=0.24, stroke_color=CHALK_YELLOW, stroke_width=2.0)
            sq_corner.move_to(p_right + np.array([0.12, 0.12, 0]))
            deg_lbl = board_text("90°", 14, CHALK_YELLOW).next_to(sq_corner, UR, buff=0.06)

            self.play(
                Create(tri),
                Create(line_a), Create(line_b), Create(line_c),
                Write(lbl_a), Write(lbl_b), Write(lbl_c),
                Create(sq_corner), FadeIn(deg_lbl),
                run_time=rt(tracker.time_until_bookmark("b2")),
            )
            self.add_sound(self.sfx["click"], gain=-12)

            knots = VGroup()
            for i in range(4):
                knots.add(Dot(p_right + (p_a - p_right) * (i / 3.0), radius=0.06, color=CHALK_YELLOW))
            for i in range(1, 5):
                knots.add(Dot(p_right + (p_b - p_right) * (i / 4.0), radius=0.06, color=CHALK_YELLOW))
            for i in range(1, 5):
                knots.add(Dot(p_b + (p_a - p_b) * (i / 5.0), radius=0.06, color=CHALK_YELLOW))

            # Rope card moved right to x = 2.2 for abundant clearance from Side = 5
            rope_box = RoundedRectangle(corner_radius=0.12, width=3.6, height=1.3, stroke_color=CHALK_AMBER, stroke_width=2, fill_color="#22180E", fill_opacity=0.85).move_to(np.array([2.2, 0.4, 0]))
            r1 = board_text("12 Equal Rope Knots", 20, CHALK_YELLOW, "BOLD").move_to(rope_box.get_center() + np.array([0, 0.25, 0]))
            r2 = board_text("Ratio: 3 + 4 + 5 = 12", 18, CHALK_WHITE).move_to(rope_box.get_center() + np.array([0, -0.25, 0]))
            rope_card = VGroup(rope_box, r1, r2)

            self.play(LaggedStartMap(FadeIn, knots, lag_ratio=0.08), FadeIn(rope_card), run_time=rt(tracker.get_remaining_duration()))
            self.play(Circumscribe(rope_box, color=CHALK_YELLOW, time_width=0.6), run_time=0.6)
            self.add_sound(self.sfx["ding"], gain=-12)

            self._capture_srt(tracker)

        self.play(FadeOut(VGroup(title, tri, line_a, line_b, line_c, lbl_a, lbl_b, lbl_c, sq_corner, deg_lbl, knots, rope_card)), run_time=0.4)

    # =========================================================================
    # SCENE 3: From Pattern to Mathematics (Squares on sides, zero overlap)
    # =========================================================================
    def beat_scene3_from_pattern_to_math(self) -> None:
        with self.voiceover(text=SCRIPTS["scene3"]) as tracker:
            title = board_text("Squares on Each Side", 28, CHALK_YELLOW, "BOLD").move_to(np.array([0, 2.45, 0]))
            self.play(FadeIn(title, shift=DOWN * 0.15), run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.add_sound(self.sfx["pop"], gain=-12)

            # Shift triangle left to (-1.8, -0.7, 0)
            s = 0.35
            p_right = np.array([-1.8, -0.7, 0])
            p_a = p_right + np.array([3 * s, 0, 0])
            p_b = p_right + np.array([0, 4 * s, 0])

            tri = Polygon(p_right, p_a, p_b, stroke_color=CHALK_WHITE, stroke_width=2.5, fill_color="#241E18", fill_opacity=0.5)

            sq_a = Polygon(p_right, p_a, p_a + np.array([0, -3 * s, 0]), p_right + np.array([0, -3 * s, 0]),
                           stroke_color=CHALK_BLUE, stroke_width=2.5, fill_color=CHALK_BLUE, fill_opacity=0.35)
            lbl_sq_a = board_text("Area = 9", 18, CHALK_BLUE, "BOLD").move_to(sq_a.get_center())

            sq_b = Polygon(p_right, p_b, p_b + np.array([-4 * s, 0, 0]), p_right + np.array([-4 * s, 0, 0]),
                           stroke_color=CHALK_GREEN, stroke_width=2.5, fill_color=CHALK_GREEN, fill_opacity=0.35)
            lbl_sq_b = board_text("Area = 16", 18, CHALK_GREEN, "BOLD").move_to(sq_b.get_center())

            norm_c = np.array([4.0, 3.0, 0.0]) / 5.0 * (5 * s)
            sq_c = Polygon(p_b, p_a, p_a + norm_c, p_b + norm_c,
                           stroke_color=CHALK_ORANGE, stroke_width=2.5, fill_color=CHALK_ORANGE, fill_opacity=0.35)
            lbl_sq_c = board_text("Area = 25", 20, CHALK_ORANGE, "BOLD").move_to(sq_c.get_center())

            # Equation card placed safely at x = 2.4, y = 0.2 (no collision with orange square)
            eq_box = RoundedRectangle(corner_radius=0.1, width=3.2, height=0.75, stroke_color=CHALK_AMBER, stroke_width=2, fill_color="#18120B", fill_opacity=0.85).move_to(np.array([2.4, 0.2, 0]))
            eq_tex = MathTex("9 + 16 = 25", color=CHALK_YELLOW, font_size=32).move_to(eq_box.get_center())

            self.play(
                Create(tri),
                DrawBorderThenFill(sq_a), Write(lbl_sq_a),
                DrawBorderThenFill(sq_b), Write(lbl_sq_b),
                DrawBorderThenFill(sq_c), Write(lbl_sq_c),
                run_time=rt(tracker.time_until_bookmark("b2")),
            )
            self.add_sound(self.sfx["whoosh"], gain=-13)

            self.play(FadeIn(eq_box), Write(eq_tex), run_time=rt(tracker.get_remaining_duration()))
            self.play(Indicate(eq_tex, color=CHALK_WHITE), run_time=0.6)
            self.add_sound(self.sfx["success"], gain=-12)

            self._capture_srt(tracker)

        self.play(FadeOut(VGroup(title, tri, sq_a, lbl_sq_a, sq_b, lbl_sq_b, sq_c, lbl_sq_c, eq_box, eq_tex)), run_time=0.4)

    # =========================================================================
    # SCENE 4: Historical Naming (Pythagorean Theorem)
    # =========================================================================
    def beat_scene4_historical_naming(self) -> None:
        with self.voiceover(text=SCRIPTS["scene4"]) as tracker:
            banner = RoundedRectangle(corner_radius=0.15, width=5.6, height=0.9, stroke_color=CHALK_AMBER, stroke_width=2.5, fill_color="#241B10", fill_opacity=0.85).move_to(np.array([0, 1.35, 0]))
            t_hist = board_text("The Pythagorean Theorem", 30, CHALK_YELLOW, "BOLD").move_to(banner.get_center())

            self.play(DrawBorderThenFill(banner), Write(t_hist), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-11)

            desc = board_text("Formalized in ancient Greek geometry by Pythagoras", 20, CHALK_WHITE).move_to(np.array([0, 0.35, 0]))
            formula_card = RoundedRectangle(corner_radius=0.12, width=4.2, height=1.0, stroke_color=CHALK_CYAN, stroke_width=2.5, fill_color="#0F2422", fill_opacity=0.85).move_to(np.array([0, -0.70, 0]))
            formula = MathTex("a^2 + b^2 = c^2", color=CHALK_CYAN, font_size=44).move_to(formula_card.get_center())

            self.play(FadeIn(desc, shift=UP * 0.15), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-13)

            self.play(FadeIn(formula_card), Write(formula), run_time=rt(tracker.get_remaining_duration()))
            self.play(Circumscribe(formula_card, color=CHALK_AMBER, stroke_width=3, time_width=0.7), run_time=0.7)
            self.add_sound(self.sfx["ding"], gain=-11)

            self._capture_srt(tracker)

        self.play(FadeOut(VGroup(banner, t_hist, desc, formula_card, formula)), run_time=0.4)

    # =========================================================================
    # SCENE 5: A - Analogy (Tile Setup: 9 blue + 16 green + empty 25 grid, zero overlap)
    # =========================================================================
    def beat_scene5_analogy_tile_setup(self) -> None:
        with self.voiceover(text=SCRIPTS["scene5"]) as tracker:
            title = board_text("A — Analogy: The Tile Puzzle", 28, CHALK_CYAN, "BOLD").move_to(np.array([0, 2.45, 0]))
            self.play(FadeIn(title, shift=DOWN * 0.15), run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.add_sound(self.sfx["pop"], gain=-12)

            # Triangle shifted left to (-1.8, -0.65, 0)
            s = 0.33
            p_right = np.array([-1.8, -0.65, 0])
            p_a = p_right + np.array([3 * s, 0, 0])
            p_b = p_right + np.array([0, 4 * s, 0])

            tri = Polygon(p_right, p_a, p_b, stroke_color=CHALK_WHITE, stroke_width=2.5, fill_color="#2A241C", fill_opacity=0.4)

            tiles_a = VGroup()
            for r in range(3):
                for c in range(3):
                    sq = Square(side_length=s - 0.03, stroke_color=CHALK_BLUE, stroke_width=1.5, fill_color=CHALK_BLUE, fill_opacity=0.65)
                    sq.move_to(p_right + np.array([(c + 0.5) * s, -(r + 0.5) * s, 0]))
                    tiles_a.add(sq)

            tiles_b = VGroup()
            for r in range(4):
                for c in range(4):
                    sq = Square(side_length=s - 0.03, stroke_color=CHALK_GREEN, stroke_width=1.5, fill_color=CHALK_GREEN, fill_opacity=0.65)
                    sq.move_to(p_right + np.array([-(c + 0.5) * s, (r + 0.5) * s, 0]))
                    tiles_b.add(sq)

            norm_c = np.array([4.0, 3.0, 0.0]) / 5.0 * s
            tang_c = (p_a - p_b) / 5.0
            grid_c = VGroup()
            for r in range(5):
                for c in range(5):
                    center = p_b + tang_c * (c + 0.5) + norm_c * (r + 0.5)
                    cell = Square(side_length=s - 0.03, stroke_color=CHALK_ORANGE, stroke_width=1.2, fill_opacity=0.1)
                    cell.rotate(np.arctan2(tang_c[1], tang_c[0]))
                    cell.move_to(center)
                    grid_c.add(cell)

            lbl_a = board_text("9 Blue Tiles", 16, CHALK_BLUE, "BOLD").next_to(tiles_a, DOWN, buff=0.12)
            lbl_b = board_text("16 Green Tiles", 16, CHALK_GREEN, "BOLD").next_to(tiles_b, LEFT, buff=0.12)
            # Label placed cleanly above grid (no cell obstruction)
            lbl_c = board_text("25 Empty Slots", 16, CHALK_ORANGE, "BOLD").move_to(np.array([0.65, 1.45, 0]))

            self.play(
                Create(tri),
                LaggedStartMap(FadeIn, tiles_a, lag_ratio=0.03), Write(lbl_a),
                LaggedStartMap(FadeIn, tiles_b, lag_ratio=0.02), Write(lbl_b),
                run_time=rt(tracker.time_until_bookmark("b2")),
            )
            self.add_sound(self.sfx["whoosh"], gain=-13)

            self.play(Create(grid_c), Write(lbl_c), run_time=rt(tracker.get_remaining_duration()))
            self.play(Indicate(lbl_c, color=CHALK_YELLOW), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-12)

            self._capture_srt(tracker)

            self._s5_data = (title, tri, tiles_a, lbl_a, tiles_b, lbl_b, grid_c, lbl_c)

    # =========================================================================
    # SCENE 6: Analogy Visual Payoff (Slide, zero overlap, 100% clean fadeout)
    # =========================================================================
    def beat_scene6_analogy_visual_payoff(self) -> None:
        title, tri, tiles_a, lbl_a, tiles_b, lbl_b, grid_c, lbl_c = self._s5_data

        with self.voiceover(text=SCRIPTS["scene6"]) as tracker:
            t_payoff = board_text("Combining Tiles: 9 + 16 = 25", 28, CHALK_YELLOW, "BOLD").move_to(np.array([0, 2.45, 0]))
            self.play(Transform(title, t_payoff), FadeOut(lbl_c), run_time=rt(tracker.time_until_bookmark("b1")))

            filled_targets = VGroup()
            anims = []
            for i in range(9):
                target = grid_c[i].copy().set_fill(CHALK_BLUE, opacity=0.85).set_stroke(CHALK_BLUE, width=1.5)
                filled_targets.add(target)
                anims.append(ReplacementTransform(tiles_a[i], target))
            
            for j in range(16):
                target = grid_c[9 + j].copy().set_fill(CHALK_GREEN, opacity=0.85).set_stroke(CHALK_GREEN, width=1.5)
                filled_targets.add(target)
                anims.append(ReplacementTransform(tiles_b[j], target))

            self.play(
                FadeOut(lbl_a), FadeOut(lbl_b),
                *anims,
                run_time=rt(tracker.time_until_bookmark("b2")),
            )
            self.add_sound(self.sfx["whoosh"], gain=-11)

            # Result card placed at x = 2.2, y = -0.2 (plenty of room away from grid and teacher)
            result_card = RoundedRectangle(corner_radius=0.1, width=3.2, height=0.75, stroke_color=CHALK_YELLOW, stroke_width=2.5, fill_color="#241B0F", fill_opacity=0.9).move_to(np.array([2.2, -0.2, 0]))
            res_tex = MathTex("9 + 16 = 25", color=CHALK_YELLOW, font_size=32).move_to(result_card.get_center())

            self.play(FadeIn(result_card), Write(res_tex), run_time=rt(tracker.time_until_bookmark("b3")))
            self.play(Indicate(res_tex, color=CHALK_WHITE), run_time=rt(tracker.get_remaining_duration()))
            self.add_sound(self.sfx["success"], gain=-11)

            self._capture_srt(tracker)

        # FADE OUT EVERYTHING INCLUDING filled_targets! ZERO GHOST MOBJECTS!
        self.play(FadeOut(VGroup(title, tri, grid_c, filled_targets, result_card, res_tex)), run_time=0.4)

    # =========================================================================
    # SCENE 7: D - Diagram: Anatomy of a Right Triangle
    # =========================================================================
    def beat_scene7_diagram_anatomy(self) -> None:
        with self.voiceover(text=SCRIPTS["scene7"]) as tracker:
            title = board_text("D — Diagram: Triangle Anatomy", 28, CHALK_CYAN, "BOLD").move_to(np.array([0, 2.45, 0]))
            self.play(FadeIn(title, shift=DOWN * 0.15), run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.add_sound(self.sfx["pop"], gain=-12)

            s = 0.50
            p_right = np.array([-1.4, -0.8, 0])
            p_a = p_right + np.array([3 * s, 0, 0])
            p_b = p_right + np.array([0, 4 * s, 0])

            tri = Polygon(p_right, p_a, p_b, stroke_color=CHALK_WHITE, stroke_width=3.0, fill_color="#1F2826", fill_opacity=0.45)
            
            line_a = Line(p_right, p_a, color=CHALK_BLUE, stroke_width=5.0)
            line_b = Line(p_right, p_b, color=CHALK_GREEN, stroke_width=5.0)
            line_c = Line(p_b, p_a, color=CHALK_ORANGE, stroke_width=5.5)

            lbl_a = board_text("Leg a (Blue)", 18, CHALK_BLUE, "BOLD").next_to(line_a, DOWN, buff=0.16)
            lbl_b = board_text("Leg b (Green)", 18, CHALK_GREEN, "BOLD").next_to(line_b, LEFT, buff=0.16)
            lbl_c = board_text("Hypotenuse c (Orange)", 19, CHALK_ORANGE, "BOLD").move_to(line_c.get_center() + np.array([0.65, 0.4, 0]))

            corner = Square(side_length=0.26, stroke_color=CHALK_YELLOW, stroke_width=2.0).move_to(p_right + np.array([0.13, 0.13, 0]))
            lbl_90 = board_text("90°", 14, CHALK_YELLOW).next_to(corner, UR, buff=0.06)

            arrow_opp = Arrow(p_right + np.array([0.25, 0.25, 0]), line_c.get_center() + np.array([-0.1, -0.1, 0]), color=CHALK_YELLOW, stroke_width=2.5, buff=0.1)
            lbl_opp = board_text("Strictly Opposite 90°", 16, CHALK_YELLOW).next_to(arrow_opp, UP, buff=0.08)

            self.play(
                Create(tri),
                Create(line_a), Write(lbl_a),
                Create(line_b), Write(lbl_b),
                Create(corner), FadeIn(lbl_90),
                run_time=rt(tracker.time_until_bookmark("b2")),
            )
            self.add_sound(self.sfx["click"], gain=-12)

            self.play(
                Create(line_c), Write(lbl_c),
                GrowArrow(arrow_opp), FadeIn(lbl_opp),
                run_time=rt(tracker.get_remaining_duration()),
            )
            self.play(Indicate(lbl_c, color=CHALK_WHITE), run_time=0.6)
            self.add_sound(self.sfx["ding"], gain=-11)

            self._capture_srt(tracker)

        self.play(FadeOut(VGroup(title, tri, line_a, line_b, line_c, lbl_a, lbl_b, lbl_c, corner, lbl_90, arrow_opp, lbl_opp)), run_time=0.4)

    # =========================================================================
    # SCENE 8: Diagram Becomes Equation (Visual to Symbolic)
    # =========================================================================
    def beat_scene8_diagram_becomes_equation(self) -> None:
        with self.voiceover(text=SCRIPTS["scene8"]) as tracker:
            title = board_text("From Diagram to Equation", 28, CHALK_YELLOW, "BOLD").move_to(np.array([0, 2.45, 0]))
            self.play(FadeIn(title, shift=DOWN * 0.15), run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.add_sound(self.sfx["pop"], gain=-12)

            card_a = RoundedRectangle(corner_radius=0.1, width=1.9, height=0.9, stroke_color=CHALK_BLUE, stroke_width=2, fill_color="#0F2027", fill_opacity=0.85).move_to(np.array([-2.2, 0.6, 0]))
            tex_a = MathTex("a^2", color=CHALK_BLUE, font_size=34).move_to(card_a.get_center())
            sub_a = board_text("Area of Side a", 13, CHALK_BLUE).next_to(card_a, DOWN, buff=0.1)

            plus = MathTex("+", color=CHALK_WHITE, font_size=36).move_to(np.array([-1.1, 0.6, 0]))

            card_b = RoundedRectangle(corner_radius=0.1, width=1.9, height=0.9, stroke_color=CHALK_GREEN, stroke_width=2, fill_color="#0D261A", fill_opacity=0.85).move_to(np.array([0.0, 0.6, 0]))
            tex_b = MathTex("b^2", color=CHALK_GREEN, font_size=34).move_to(card_b.get_center())
            sub_b = board_text("Area of Side b", 13, CHALK_GREEN).next_to(card_b, DOWN, buff=0.1)

            equals = MathTex("=", color=CHALK_WHITE, font_size=36).move_to(np.array([1.1, 0.6, 0]))

            card_c = RoundedRectangle(corner_radius=0.1, width=1.9, height=0.9, stroke_color=CHALK_ORANGE, stroke_width=2, fill_color="#261A0D", fill_opacity=0.85).move_to(np.array([2.2, 0.6, 0]))
            tex_c = MathTex("c^2", color=CHALK_ORANGE, font_size=34).move_to(card_c.get_center())
            sub_c = board_text("Area of Hypotenuse", 13, CHALK_ORANGE).next_to(card_c, DOWN, buff=0.1)

            self.play(
                FadeIn(card_a), Write(tex_a), FadeIn(sub_a),
                Write(plus),
                FadeIn(card_b), Write(tex_b), FadeIn(sub_b),
                run_time=rt(tracker.time_until_bookmark("b2")),
            )
            self.add_sound(self.sfx["click"], gain=-13)

            self.play(
                Write(equals),
                FadeIn(card_c), Write(tex_c), FadeIn(sub_c),
                run_time=rt(tracker.time_until_bookmark("b3")),
            )
            self.add_sound(self.sfx["click"], gain=-13)

            final_tex = MathTex("a^2 + b^2 = c^2", color=CHALK_YELLOW, font_size=42).move_to(np.array([0, -0.95, 0]))
            self.play(Write(final_tex), run_time=rt(tracker.get_remaining_duration()))
            self.play(Circumscribe(final_tex, color=CHALK_AMBER, stroke_width=3, time_width=0.6), run_time=0.6)
            self.add_sound(self.sfx["success"], gain=-11)

            self._capture_srt(tracker)

        self.play(FadeOut(VGroup(title, card_a, tex_a, sub_a, plus, card_b, tex_b, sub_b, equals, card_c, tex_c, sub_c, final_tex)), run_time=0.4)

    # =========================================================================
    # SCENE 9: E - Example (Solving 3, 4, ?)
    # =========================================================================
    def beat_scene9_worked_example(self) -> None:
        with self.voiceover(text=SCRIPTS["scene9"]) as tracker:
            title = board_text("E — Example: Triangle 3, 4, c", 28, CHALK_CYAN, "BOLD").move_to(np.array([0, 2.45, 0]))
            self.play(FadeIn(title, shift=DOWN * 0.15), run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.add_sound(self.sfx["pop"], gain=-12)

            s = 0.40
            p_right = np.array([-3.0, -0.7, 0])
            p_a = p_right + np.array([3 * s, 0, 0])
            p_b = p_right + np.array([0, 4 * s, 0])
            tri = Polygon(p_right, p_a, p_b, stroke_color=CHALK_WHITE, stroke_width=2.5, fill_color="#241E18", fill_opacity=0.45)
            corner = Square(side_length=0.20, stroke_color=CHALK_YELLOW, stroke_width=1.5).move_to(p_right + np.array([0.1, 0.1, 0]))
            lbl_a = board_text("a = 3", 18, CHALK_BLUE).next_to(Line(p_right, p_a), DOWN, buff=0.1)
            lbl_b = board_text("b = 4", 18, CHALK_GREEN).next_to(Line(p_right, p_b), LEFT, buff=0.1)
            lbl_c = board_text("c = ?", 20, CHALK_ORANGE, "BOLD").move_to(Line(p_b, p_a).get_center() + np.array([0.45, 0.25, 0]))

            tri_group = VGroup(tri, corner, lbl_a, lbl_b, lbl_c)

            eq1 = MathTex("3^2 + 4^2 = c^2", color=CHALK_WHITE, font_size=30).move_to(np.array([1.2, 0.9, 0]))
            eq2 = MathTex("9 + 16 = c^2", color=CHALK_YELLOW, font_size=30).move_to(np.array([1.2, 0.3, 0]))
            eq3 = MathTex("25 = c^2", color=CHALK_AMBER, font_size=32).move_to(np.array([1.2, -0.3, 0]))
            eq4 = MathTex("c = \\sqrt{25} = 5", color=CHALK_GREEN, font_size=36).move_to(np.array([1.2, -0.9, 0]))

            self.play(FadeIn(tri_group), Write(eq1), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-13)

            self.play(Write(eq2), Write(eq3), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-13)

            lbl_c_done = board_text("c = 5", 20, CHALK_GREEN, "BOLD").move_to(lbl_c.get_center())
            self.play(
                Write(eq4),
                Transform(lbl_c, lbl_c_done),
                run_time=rt(tracker.get_remaining_duration()),
            )
            self.play(Circumscribe(eq4, color=CHALK_GREEN, stroke_width=3, time_width=0.6), run_time=0.6)
            self.add_sound(self.sfx["success"], gain=-11)

            self._capture_srt(tracker)

        self.play(FadeOut(VGroup(title, tri_group, eq1, eq2, eq3, eq4)), run_time=0.4)

    # =========================================================================
    # SCENE 10: P - Plain English
    # =========================================================================
    def beat_scene10_plain_english(self) -> None:
        with self.voiceover(text=SCRIPTS["scene10"]) as tracker:
            title = board_text("P — Plain English Intuition", 28, CHALK_YELLOW, "BOLD").move_to(np.array([0, 2.45, 0]))
            self.play(FadeIn(title, shift=DOWN * 0.15), run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.add_sound(self.sfx["pop"], gain=-12)

            box_rule = RoundedRectangle(corner_radius=0.15, width=7.0, height=1.3, stroke_color=CHALK_CYAN, stroke_width=2.5, fill_color="#122524", fill_opacity=0.85).move_to(np.array([0, 0.65, 0]))
            t1 = board_text("Small Square  +  Medium Square", 20, CHALK_CYAN, "BOLD").move_to(box_rule.get_center() + np.array([0, 0.22, 0]))
            t2 = board_text("=  Large Square", 22, CHALK_YELLOW, "BOLD").move_to(box_rule.get_center() + np.array([0, -0.25, 0]))

            sub_plain = board_text("Combined areas of shorter sides equal area of longest side!", 16, CHALK_WHITE).move_to(np.array([0, -0.35, 0]))
            formula_morph = MathTex("a^2 + b^2 = c^2", color=CHALK_YELLOW, font_size=40).move_to(np.array([0, -1.05, 0]))

            self.play(
                DrawBorderThenFill(box_rule), Write(t1), Write(t2),
                run_time=rt(tracker.time_until_bookmark("b2")),
            )
            self.add_sound(self.sfx["whoosh"], gain=-13)

            self.play(
                FadeIn(sub_plain), Write(formula_morph),
                run_time=rt(tracker.get_remaining_duration()),
            )
            self.play(Indicate(formula_morph, color=CHALK_WHITE), run_time=0.6)
            self.add_sound(self.sfx["ding"], gain=-11)

            self._capture_srt(tracker)

        self.play(FadeOut(VGroup(title, box_rule, t1, t2, sub_plain, formula_morph)), run_time=0.4)

    # =========================================================================
    # SCENE 11: T - Technical Definition
    # =========================================================================
    def beat_scene11_technical_definition(self) -> None:
        with self.voiceover(text=SCRIPTS["scene11"]) as tracker:
            title = board_text("T — Technical Definition", 28, CHALK_CYAN, "BOLD").move_to(np.array([0, 2.45, 0]))
            self.play(FadeIn(title, shift=DOWN * 0.15), run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.add_sound(self.sfx["pop"], gain=-12)

            def_card = RoundedRectangle(corner_radius=0.15, width=7.2, height=1.5, stroke_color=CHALK_AMBER, stroke_width=2.5, fill_color="#241B10", fill_opacity=0.85).move_to(np.array([0, 0.85, 0]))
            line1 = board_text("In a right-angled triangle,", 20, CHALK_WHITE, "BOLD").move_to(def_card.get_center() + np.array([0, 0.35, 0]))
            line2 = board_text("the square of the hypotenuse is equal to", 18, CHALK_WHITE).move_to(def_card.get_center())
            line3 = board_text("the sum of the squares of the other two sides.", 18, CHALK_YELLOW, "BOLD").move_to(def_card.get_center() + np.array([0, -0.35, 0]))

            def_group = VGroup(def_card, line1, line2, line3)

            b_leg1 = self._pill_badge("a = Leg 1", CHALK_BLUE, 16).move_to(np.array([-2.2, -0.45, 0]))
            b_leg2 = self._pill_badge("b = Leg 2", CHALK_GREEN, 16).move_to(np.array([0.0, -0.45, 0]))
            b_hyp = self._pill_badge("c = Hypotenuse (Opposite 90°)", CHALK_ORANGE, 16).move_to(np.array([0.0, -1.05, 0]))

            self.play(DrawBorderThenFill(def_card), Write(line1), Write(line2), Write(line3), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-13)

            self.play(FadeIn(b_leg1), FadeIn(b_leg2), FadeIn(b_hyp), run_time=rt(tracker.get_remaining_duration()))
            self.play(Circumscribe(b_hyp, color=CHALK_YELLOW, stroke_width=2.5, time_width=0.6), run_time=0.6)
            self.add_sound(self.sfx["success"], gain=-11)

            self._capture_srt(tracker)

        self.play(FadeOut(VGroup(title, def_group, b_leg1, b_leg2, b_hyp)), run_time=0.4)

    # =========================================================================
    # SCENE 12: Misconception Check (Native vector icons - NO missing glyphs)
    # =========================================================================
    def beat_scene12_misconception_check(self) -> None:
        with self.voiceover(text=SCRIPTS["scene12"]) as tracker:
            title = board_text("Misconception Alert!", 28, CHALK_PINK, "BOLD").move_to(np.array([0, 2.45, 0]))
            self.play(FadeIn(title, shift=DOWN * 0.15), run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.add_sound(self.sfx["pop"], gain=-12)

            p1 = np.array([-3.2, -0.6, 0])
            p2 = np.array([-1.4, -0.6, 0])
            p3 = np.array([-3.2, 0.7, 0])
            tri_right = Polygon(p1, p2, p3, stroke_color=CHALK_WHITE, stroke_width=2.5, fill_color="#1A3326", fill_opacity=0.4)
            sq_c = Square(side_length=0.22, stroke_color=CHALK_YELLOW, stroke_width=1.5).move_to(p1 + np.array([0.11, 0.11, 0]))
            
            chk1 = Line(np.array([-2.7, -0.95, 0]), np.array([-2.5, -1.15, 0]), color=CHALK_GREEN, stroke_width=4.0)
            chk2 = Line(np.array([-2.5, -1.15, 0]), np.array([-2.1, -0.80, 0]), color=CHALK_GREEN, stroke_width=4.0)
            check_icon = VGroup(chk1, chk2)
            lbl_valid = board_text("Valid (90° Right Angle)", 16, CHALK_GREEN, "BOLD").move_to(np.array([-2.3, -1.35, 0]))
            f_valid = MathTex("a^2 + b^2 = c^2", color=CHALK_GREEN, font_size=28).move_to(np.array([-2.3, -1.75, 0]))

            left_group = VGroup(tri_right, sq_c, check_icon, lbl_valid, f_valid)

            q1 = np.array([1.2, -0.6, 0])
            q2 = np.array([3.4, -0.6, 0])
            q3 = np.array([2.0, 0.8, 0])
            tri_non = Polygon(q1, q2, q3, stroke_color=CHALK_WHITE, stroke_width=2.5, fill_color="#331A1A", fill_opacity=0.4)
            
            cr1 = Line(np.array([2.0, -1.15, 0]), np.array([2.4, -0.85, 0]), color=CHALK_PINK, stroke_width=4.0)
            cr2 = Line(np.array([2.0, -0.85, 0]), np.array([2.4, -1.15, 0]), color=CHALK_PINK, stroke_width=4.0)
            cross_icon = VGroup(cr1, cr2)
            lbl_invalid = board_text("Invalid (No 90° Angle)", 16, CHALK_PINK, "BOLD").move_to(np.array([2.3, -1.35, 0]))
            f_invalid = MathTex("a^2 + b^2 \\neq c^2", color=CHALK_PINK, font_size=28).move_to(np.array([2.3, -1.75, 0]))

            right_group = VGroup(tri_non, cross_icon, lbl_invalid, f_invalid)

            self.play(FadeIn(left_group), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-12)

            self.play(FadeIn(right_group), run_time=rt(tracker.get_remaining_duration()))
            self.play(Wiggle(cross_icon), run_time=0.6)
            self.add_sound(self.sfx["ding"], gain=-11)

            self._capture_srt(tracker)

        self.play(FadeOut(VGroup(title, left_group, right_group)), run_time=0.4)

    # =========================================================================
    # SCENE 13: Real-World Application (Leaning Ladder, zero line collision)
    # =========================================================================
    def beat_scene13_real_world_application(self) -> None:
        with self.voiceover(text=SCRIPTS["scene13"]) as tracker:
            title = board_text("Real-World: The Leaning Ladder", 28, CHALK_CYAN, "BOLD").move_to(np.array([0, 2.45, 0]))
            self.play(FadeIn(title, shift=DOWN * 0.15), run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.add_sound(self.sfx["pop"], gain=-12)

            ground = Line(np.array([-3.5, -0.9, 0]), np.array([-0.6, -0.9, 0]), color="#8D6E63", stroke_width=5)
            wall = Line(np.array([-3.2, -0.9, 0]), np.array([-3.2, 1.5, 0]), color="#B0BEC5", stroke_width=6)

            p_base = np.array([-1.4, -0.9, 0])
            p_top = np.array([-3.2, 1.3, 0])
            ladder = Line(p_base, p_top, color=CHALK_ORANGE, stroke_width=6)

            rungs = VGroup()
            for i in range(1, 7):
                pos = p_base + (p_top - p_base) * (i / 7.0)
                r = Line(pos + np.array([-0.08, 0.06, 0]), pos + np.array([0.08, -0.06, 0]), color=CHALK_YELLOW, stroke_width=3)
                rungs.add(r)

            lbl_ground = board_text("Base = 6 m", 16, CHALK_BLUE).next_to(ground, DOWN, buff=0.12).shift(RIGHT * 0.5)
            lbl_wall = board_text("Wall = 8 m", 16, CHALK_GREEN).next_to(wall, LEFT, buff=0.12)
            # Label safely placed in the clear zone between ladder and calculation card
            lbl_ladder = board_text("Ladder = ?", 18, CHALK_ORANGE, "BOLD").move_to(np.array([-1.2, 0.45, 0]))

            diagram = VGroup(ground, wall, ladder, rungs, lbl_ground, lbl_wall, lbl_ladder)

            m_card = RoundedRectangle(corner_radius=0.12, width=3.6, height=2.2, stroke_color=CHALK_AMBER, stroke_width=2, fill_color="#18130B", fill_opacity=0.85).move_to(np.array([2.0, 0.1, 0]))
            t1 = MathTex("6^2 + 8^2 = c^2", color=CHALK_WHITE, font_size=28).move_to(m_card.get_center() + np.array([0, 0.6, 0]))
            t2 = MathTex("36 + 64 = 100", color=CHALK_YELLOW, font_size=28).move_to(m_card.get_center() + np.array([0, 0.05, 0]))
            
            # Cleanly rendered formula and units (avoiding missing font glyphs)
            t3_math = MathTex("c = \\sqrt{100} = 10", color=CHALK_GREEN, font_size=32)
            t3_unit = board_text(" m", 20, CHALK_GREEN, "BOLD").next_to(t3_math, RIGHT, buff=0.08)
            t3 = VGroup(t3_math, t3_unit).move_to(m_card.get_center() + np.array([0, -0.55, 0]))

            self.play(Create(diagram), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-13)

            self.play(FadeIn(m_card), Write(t1), Write(t2), run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-12)

            lbl_ladder_done = board_text("Ladder = 10 m", 18, CHALK_GREEN, "BOLD").move_to(np.array([-1.2, 0.45, 0]))
            self.play(
                Write(t3),
                Transform(lbl_ladder, lbl_ladder_done),
                run_time=rt(tracker.get_remaining_duration()),
            )
            self.play(Indicate(t3, color=CHALK_WHITE), run_time=0.6)
            self.add_sound(self.sfx["success"], gain=-11)

            self._capture_srt(tracker)

        self.play(FadeOut(VGroup(title, diagram, m_card, t1, t2, t3)), run_time=0.4)

    # =========================================================================
    # SCENE 14: Student Challenge (5, 12, ?, clean timer fade)
    # =========================================================================
    def beat_scene14_student_challenge(self) -> None:
        with self.voiceover(text=SCRIPTS["scene14"]) as tracker:
            title = board_text("Your Turn: Solve for c!", 28, CHALK_YELLOW, "BOLD").move_to(np.array([0, 2.45, 0]))
            self.play(FadeIn(title, shift=DOWN * 0.15), run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.add_sound(self.sfx["pop"], gain=-12)

            p_right = np.array([-3.0, -0.8, 0])
            p_a = p_right + np.array([2.4, 0, 0])  # base = 12
            p_b = p_right + np.array([0, 1.0, 0])   # height = 5

            tri = Polygon(p_right, p_a, p_b, stroke_color=CHALK_WHITE, stroke_width=2.5, fill_color="#241E18", fill_opacity=0.45)
            corner = Square(side_length=0.2, stroke_color=CHALK_YELLOW, stroke_width=1.5).move_to(p_right + np.array([0.1, 0.1, 0]))
            lbl_a = board_text("Side = 12", 16, CHALK_GREEN).next_to(Line(p_right, p_a), DOWN, buff=0.1)
            lbl_b = board_text("Side = 5", 16, CHALK_BLUE).next_to(Line(p_right, p_b), LEFT, buff=0.1)
            lbl_c = board_text("c = ?", 20, CHALK_ORANGE, "BOLD").move_to(Line(p_b, p_a).get_center() + np.array([0.35, 0.25, 0]))

            tri_grp = VGroup(tri, corner, lbl_a, lbl_b, lbl_c)

            badge = self._pill_badge("Can you find c?", CHALK_CYAN, 18).move_to(np.array([1.8, 1.0, 0]))
            t_bar = Rectangle(width=3.2, height=0.14, stroke_color=CHALK_YELLOW, fill_color=CHALK_YELLOW, fill_opacity=1.0).move_to(np.array([1.8, 0.45, 0]))

            self.play(FadeIn(tri_grp), FadeIn(badge), Create(t_bar), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-13)

            # Timer bar shrinks and fades completely (zero leftover slivers)
            self.play(
                t_bar.animate.stretch_to_fit_width(0.01).shift(RIGHT * 1.6),
                run_time=rt(tracker.time_until_bookmark("b3")),
            )
            self.remove(t_bar)
            self.add_sound(self.sfx["ding"], gain=-12)

            sol1 = MathTex("5^2 + 12^2 = 25 + 144 = 169", color=CHALK_YELLOW, font_size=26).move_to(np.array([1.8, -0.1, 0]))
            sol2 = MathTex("c = \\sqrt{169} = 13", color=CHALK_GREEN, font_size=34).move_to(np.array([1.8, -0.7, 0]))
            lbl_c_done = board_text("c = 13", 20, CHALK_GREEN, "BOLD").move_to(lbl_c.get_center())

            self.play(Write(sol1), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["click"], gain=-13)

            self.play(
                Write(sol2),
                Transform(lbl_c, lbl_c_done),
                run_time=rt(tracker.get_remaining_duration()),
            )
            self.play(Circumscribe(sol2, color=CHALK_GREEN, stroke_width=2.5, time_width=0.6), run_time=0.6)
            self.add_sound(self.sfx["success"], gain=-11)

            self._capture_srt(tracker)

        self.play(FadeOut(VGroup(title, tri_grp, badge, sol1, sol2)), run_time=0.4)

    # =========================================================================
    # SCENE 15: Final Recap & Outro (Clean transition to Outro Card)
    # =========================================================================
    def beat_scene15_final_recap(self) -> None:
        with self.voiceover(text=SCRIPTS["scene15"]) as tracker:
            title = board_text("The 5-Step Master Checklist", 28, CHALK_YELLOW, "BOLD").move_to(np.array([0, 2.45, 0]))
            self.play(FadeIn(title, shift=DOWN * 0.15), run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.add_sound(self.sfx["pop"], gain=-12)

            s1 = self._pill_badge("1. Confirm 90° Right Angle", CHALK_YELLOW, 16)
            s2 = self._pill_badge("2. Spot Hypotenuse c (Opposite 90°)", CHALK_ORANGE, 16)
            s3 = self._pill_badge("3. Square Legs (a², b²)", CHALK_BLUE, 16)
            s4 = self._pill_badge("4. Add Areas (a² + b²)", CHALK_GREEN, 16)
            s5 = self._pill_badge("5. Take Square Root √", CHALK_CYAN, 16)

            flow = VGroup(s1, s2, s3, s4, s5).arrange(DOWN, buff=0.12).move_to(np.array([0, 0.4, 0]))

            self.play(LaggedStartMap(FadeIn, flow, lag_ratio=0.15), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-12)

            thanks = board_text("Thank You for Watching!", 32, CHALK_WHITE, "BOLD")
            formula_end = MathTex("a^2 + b^2 = c^2", color=CHALK_AMBER, font_size=44)
            thanks2 = board_text("See you in the next lesson :)", 22, CHALK_CYAN)
            thanks_group = VGroup(thanks, formula_end, thanks2).arrange(DOWN, buff=0.25).move_to(np.array([0, 0.35, 0]))

            # Fade out both the checklist AND the title so Outro takes center stage cleanly
            self.play(FadeOut(flow), FadeOut(title), run_time=0.3)
            self.play(Write(thanks), FadeIn(formula_end), FadeIn(thanks2, shift=UP * 0.1), run_time=rt(tracker.get_remaining_duration()))
            self.play(Circumscribe(thanks_group, color=CHALK_AMBER, stroke_width=3, time_width=0.6), run_time=0.6)
            self.add_sound(self.sfx["success"], gain=-11)

            self._capture_srt(tracker)

        self.wait(END_HOLD)

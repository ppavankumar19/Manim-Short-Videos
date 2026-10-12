"""
Area of a Circle — TG Board Class 8 Mathematics
Chapter: Area of Plane Figures (chapter map: 9.6 Area of circle)

Extended 4-minute conceptual lesson with history, prerequisites,
intuition, multiple examples, and rich animations.

Animation techniques used (from https://docs.manim.community):
  LaggedStart, SpiralIn, MoveAlongPath, ApplyWave, FocusOn,
  ShowPassingFlash, Rotate, GrowFromEdge, ShrinkToCenter, Succession,
  TracedPath, Broadcast, Circumscribe, TransformFromCopy,
  DrawBorderThenFill, SpinInFromNothing, FadeTransform, plus standard
  Create/Write/FadeIn/FadeOut/Flash/Indicate/Wiggle/GrowFromCenter.
"""

from __future__ import annotations

import numpy as np
from manim import (
    ORIGIN, UP, DOWN, LEFT, RIGHT, DL, UL, UR, DR,
    PI, TAU,
    MathTex, VGroup, Circle, Sector, Rectangle, Line, Brace, Arc,
    Dot, DashedLine, Arrow, Polygon, Square, Ellipse,
    SurroundingRectangle, RoundedRectangle,
    FadeIn, FadeOut, Write, Create, Indicate, DrawBorderThenFill,
    ReplacementTransform, GrowFromCenter, GrowFromEdge, TransformFromCopy,
    GrowArrow, Flash, Wiggle, SpinInFromNothing, ShrinkToCenter,
    FadeTransform, Circumscribe, FocusOn, ApplyWave,
    ShowPassingFlash, MoveAlongPath, Rotate,
    LaggedStart, LaggedStartMap, Succession, SpiralIn, Uncreate,
    TracedPath, AnimatedBoundary,
    Text, rate_functions, config,
)
from manim_voiceover import VoiceoverScene

from lesson_kit import (
    BG, INK, MUTED, ACCENT, SUCCESS, AMBER, ROSE, VIOLET, PANEL,
    txt, heading, card, given_panel, rule_line,
    END_HOLD, FONT,
)
from speech_service import get_speech_service
from sound_effects import load_all as load_sfx


LESSON_META = {
    "board": "TG",
    "subject": "Mathematics",
    "grade": 8,
    "chapter": "Area of Plane Figures",
    "concept": "Area of a circle",
    "title": "Area of a Circle",
    "scene": "CircleAreaLesson",
    "chapter_map": ["9.6 Area of circle"],
    "source_example": "Example 12 — circumference 22 cm, find the area",
}

# ~570 words for ~4 minutes at +9% rate
NARRATION = {
    "title": (
        "Let us discuss the area of a circle. Where does pi r squared "
        "truly come from?"
    ),
    "hook": (
        "Think about this. Every area formula you have learned so far, "
        "rectangles, triangles, parallelograms, they all come down to "
        "length times breadth. But a chapati, a coin, a wheel, "
        "these have no straight edges at all. So how can we "
        "measure the space inside a circle?"
    ),
    "history": (
        "Over two thousand years ago, the Greek mathematician Archimedes "
        "had a brilliant idea. What if he could straighten the curved edge? "
        "He imagined cutting a circle into thin slices, like pieces of cake. "
        "Then he rearranged them into a shape with straight sides. "
        "The more slices he used, the closer it came to a perfect rectangle. "
        "This was one of the earliest ideas behind calculus, centuries "
        "before calculus was invented."
    ),
    "fundamentals": (
        "Before we build the formula, let us be clear about three measurements. "
        "The radius is the distance from the centre to any point on the edge. "
        "The diameter is twice the radius, stretching across the full circle. "
        "And the circumference is the total distance around the circle, "
        "which equals two pi r. These three are the only tools we need."
    ),
    "build": (
        "Now watch carefully. Take the circle and slice it into equal sectors. "
        "Colour half of them blue and the other half red. "
        "Now separate the sectors and lay them alternately, one pointing up, "
        "one pointing down, interlocking like the teeth of a zipper. "
        "The bumpy edges begin to look almost straight. If we slice thinner "
        "and thinner, the bumps flatten out completely, and we get a perfect "
        "rectangle."
    ),
    "formal": (
        "Look at this rectangle. Its height is the radius r. "
        "Its width is exactly half the circumference, which is pi r. "
        "So the area of the rectangle is pi r times r, "
        "which gives us pi r squared. "
        "And since we built this rectangle from the circle without adding "
        "or removing anything, the area of the circle is also pi r squared."
    ),
    "why": (
        "But why is the width only half the circumference? "
        "Think about the interlocked sectors. Half of the curved edges "
        "point upward along the top, and the other half point downward "
        "along the bottom. So each long side of the rectangle carries "
        "exactly half the total circumference. "
        "That is why the width is pi r and not two pi r."
    ),
    "working": (
        "Let us put this formula to work. A circle has a circumference of "
        "twenty two centimetres. We need to find its area. "
        "First, find the radius. We know two pi r equals twenty two. "
        "Using pi as twenty two over seven, the radius comes out to "
        "three point five centimetres."
    ),
    "example": (
        "Now apply the formula. Area equals pi r squared. "
        "That is twenty two over seven times three point five squared. "
        "Three point five squared is twelve point two five. "
        "Multiply, and the area is thirty eight point five square centimetres."
    ),
    "example2": (
        "Here is another example. A circular garden has a radius of "
        "seven metres. Find the area. "
        "Area equals pi r squared. That is twenty two over seven times "
        "seven squared. Seven squared is forty nine. Multiply, and the area "
        "is one hundred and fifty four square metres."
    ),
    "summary": (
        "Let us bring it all together. A circle is simply a rectangle "
        "in disguise, with height r and width pi r. "
        "The area is always pi r squared. "
        "From Archimedes to your classroom, the same beautiful idea."
    ),
}

EXAMPLE_CHECKS = [
    ("2 * (22/7) * 3.5", 22.0),
    ("(22/7) * 3.5 ** 2", 38.5),
    ("3.5 ** 2", 12.25),
    ("22 / (2 * (22/7))", 3.5),
    ("(22/7) * 7 ** 2", 154.0),
    ("7 ** 2", 49),
]

_R = 1.5
_N = 14       # number of sectors in the fan
_N2 = 24      # finer slicing for the second demonstration

# Extra palette for variety
TEAL = "#2DD4BF"
SKY = "#38BDF8"
LIME = "#A3E635"
ORANGE = "#FB923C"


def wedge(i: int, n: int, color: str, radius: float = _R) -> Sector:
    step = TAU / n
    return Sector(
        radius=radius, start_angle=i * step, angle=step,
        color=color, fill_opacity=0.35, stroke_width=1.5,
    )


def sliced_circle(n: int = _N, radius: float = _R) -> VGroup:
    return VGroup(*[
        wedge(i, n, ACCENT if i % 2 == 0 else ROSE, radius) for i in range(n)
    ])


def interlocked(n: int = _N, radius: float = _R) -> VGroup:
    """Sectors laid alternately up/down, approximating a rectangle."""
    step = TAU / n
    half_angle = step / 2
    dx = radius * np.sin(half_angle)

    row = VGroup()
    for i in range(n):
        up = i % 2 == 0
        tri = Sector(
            radius=radius, start_angle=PI / 2 - half_angle, angle=step,
            color=ACCENT if up else ROSE,
            fill_opacity=0.35, stroke_width=1.5,
        )
        if not up:
            tri.rotate(PI, about_point=np.array([0.0, radius / 2, 0.0]))
        tri.shift(RIGHT * i * dx)
        row.add(tri)
    row.move_to(ORIGIN)
    return row


class CircleAreaLesson(VoiceoverScene):
    """Extended conceptual lesson on the area of a circle (~4 min)."""

    def construct(self) -> None:
        self.set_speech_service(get_speech_service(), create_subcaption=True)
        self.sfx = load_sfx()

        self.beat_title()
        self.beat_hook()
        self.beat_history()
        self.beat_fundamentals()
        self.beat_build()
        self.beat_formal()
        self.beat_why()
        self.beat_working()
        self.beat_example()
        self.beat_example2()
        self.beat_summary()

    # -- Beat 1: Title --------------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            d = tracker.duration

            # Animated pulsing concentric rings using LaggedStart
            rings = VGroup(*[
                Circle(radius=r, color=ACCENT, stroke_width=2,
                       stroke_opacity=0.12 + 0.1 * i)
                for i, r in enumerate([1.0, 1.8, 2.6, 3.4])
            ]).move_to(ORIGIN)

            title = txt("Area of a Circle", 48, ACCENT, "BOLD")
            formula = MathTex(r"\pi r^2", font_size=64, color=SUCCESS)
            group = VGroup(title, formula).arrange(DOWN, buff=0.5).move_to(ORIGIN)

            # Orbiting dot that traces a path
            orbit = Circle(radius=3.4, color=AMBER, stroke_width=0).move_to(ORIGIN)
            tracer_dot = Dot(color=AMBER, radius=0.09)
            tracer_dot.move_to(orbit.point_from_proportion(0))

            self.play(
                LaggedStart(*[Create(r) for r in rings], lag_ratio=0.25),
                run_time=0.18 * d,
            )
            self.play(
                Write(title),
                MoveAlongPath(tracer_dot, orbit),
                run_time=0.28 * d,
            )
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(
                SpinInFromNothing(formula),
                FadeOut(tracer_dot),
                run_time=0.22 * d,
            )
            self.add_sound(self.sfx["ding"], gain=-12)
            self.play(
                Flash(formula.get_center(), color=AMBER, flash_radius=1.0,
                      num_lines=16, line_length=0.4),
                run_time=0.20 * d,
            )
            self.add_sound(self.sfx["swipe"], gain=-16)
            self.play(
                LaggedStart(*[ShrinkToCenter(r) for r in rings], lag_ratio=0.1),
                FadeOut(group),
                run_time=0.12 * d,
            )

    # -- Beat 2: Hook ---------------------------------------------------------
    def beat_hook(self) -> None:
        with self.voiceover(text=NARRATION["hook"]) as tracker:
            d = tracker.duration

            # Rectangle with l x b — the familiar formula
            rect = Rectangle(
                width=2.6, height=1.4, fill_color=VIOLET,
                fill_opacity=0.18, stroke_color=VIOLET, stroke_width=3,
            ).move_to(LEFT * 3.5 + UP * 1.0)
            r_lbl = MathTex(r"l \times b", font_size=32, color=VIOLET)
            r_lbl.next_to(rect, DOWN, buff=0.22)
            rect_title = txt("Every formula so far", 22, MUTED)
            rect_title.next_to(rect, UP, buff=0.22)

            # Triangle
            tri = Polygon(
                LEFT * 1.3 + DOWN * 0.7, RIGHT * 1.3 + DOWN * 0.7, UP * 0.7,
                fill_color=TEAL, fill_opacity=0.18,
                stroke_color=TEAL, stroke_width=2.5,
            ).scale(0.55).move_to(LEFT * 0.5 + UP * 1.0)

            # Parallelogram
            para = Polygon(
                LEFT * 1.2 + DOWN * 0.5, RIGHT * 0.6 + DOWN * 0.5,
                RIGHT * 1.2 + UP * 0.5, LEFT * 0.6 + UP * 0.5,
                fill_color=SKY, fill_opacity=0.18,
                stroke_color=SKY, stroke_width=2.5,
            ).scale(0.55).move_to(LEFT * 0.5 + DOWN * 0.5)

            # Circular objects — three different colours
            chapati = Circle(
                radius=0.6, color=AMBER, fill_opacity=0.25, stroke_width=3,
            ).move_to(RIGHT * 2.5 + UP * 1.2)
            chap_lbl = txt("chapati", 18, AMBER)
            chap_lbl.next_to(chapati, DOWN, buff=0.18)

            coin = Circle(
                radius=0.38, color=LIME, fill_opacity=0.3, stroke_width=3,
            ).move_to(RIGHT * 4.2 + UP * 1.2)
            coin_lbl = txt("coin", 18, LIME)
            coin_lbl.next_to(coin, DOWN, buff=0.18)

            wheel = Circle(
                radius=0.72, color=ROSE, fill_opacity=0.2, stroke_width=3,
            ).move_to(RIGHT * 5.6 + UP * 0.5)
            wheel_lbl = txt("wheel", 18, ROSE)
            wheel_lbl.next_to(wheel, DOWN, buff=0.18)
            # Spokes inside the wheel
            spokes = VGroup(*[
                Line(wheel.get_center(),
                     wheel.get_center() + np.array([
                         0.72 * np.cos(a), 0.72 * np.sin(a), 0]),
                     stroke_color=ROSE, stroke_width=1.5)
                for a in np.linspace(0, TAU, 8, endpoint=False)
            ])

            ask = txt("No straight edges at all!", 28, ACCENT, "BOLD")
            ask.move_to(DOWN * 1.4)

            question = txt("So how can we measure the space?", 28, SUCCESS, "BOLD")
            question.move_to(DOWN * 2.4)

            # Build with LaggedStart for staggered entry
            self.add_sound(self.sfx["click"], gain=-16)
            self.play(
                LaggedStart(
                    Create(rect), FadeIn(rect_title), Write(r_lbl),
                    lag_ratio=0.3,
                ),
                run_time=0.14 * d,
            )
            self.play(
                DrawBorderThenFill(tri),
                DrawBorderThenFill(para),
                run_time=0.10 * d,
            )
            self.add_sound(self.sfx["pop"], gain=-14)
            self.play(
                LaggedStart(
                    GrowFromCenter(chapati), FadeIn(chap_lbl),
                    GrowFromCenter(coin), FadeIn(coin_lbl),
                    GrowFromCenter(wheel), FadeIn(wheel_lbl),
                    Create(spokes),
                    lag_ratio=0.15,
                ),
                run_time=0.20 * d,
            )
            self.add_sound(self.sfx["whoosh"], gain=-16)
            self.play(
                FadeIn(ask, shift=UP * 0.3),
                Wiggle(chapati), Wiggle(coin),
                Rotate(wheel, angle=PI / 4),
                run_time=0.18 * d,
            )
            self.play(
                ApplyWave(question, amplitude=0.15),
                FadeIn(question),
                run_time=0.18 * d,
            )
            self.play(
                FocusOn(question.get_center(), color=SUCCESS, opacity=0.15),
                run_time=0.08 * d,
            )
            self.play(
                FadeOut(VGroup(
                    rect, r_lbl, rect_title, tri, para,
                    chapati, chap_lbl, coin, coin_lbl,
                    wheel, wheel_lbl, spokes, ask, question,
                )),
                run_time=0.12 * d,
            )

    # -- Beat 3: History (Archimedes) -----------------------------------------
    def beat_history(self) -> None:
        with self.voiceover(text=NARRATION["history"]) as tracker:
            d = tracker.duration

            head = heading("Archimedes' brilliant idea")

            # Circle on the left
            circ = Circle(
                radius=1.5, color=ACCENT, stroke_width=3, fill_opacity=0.15,
            ).move_to(LEFT * 4.0 + DOWN * 0.2)

            # Archimedes label with SpiralIn
            arch_label = txt("Archimedes", 26, AMBER, "BOLD")
            arch_label.next_to(circ, DOWN, buff=0.4)
            year_label = txt("~250 BC", 18, MUTED)
            year_label.next_to(arch_label, DOWN, buff=0.1)
            year_label.set_x(arch_label.get_center()[0])

            # Animated slice lines appearing one by one (LaggedStart)
            slice_lines = VGroup(*[
                Line(circ.get_center(),
                     circ.get_center() + np.array([
                         1.5 * np.cos(i * TAU / 12),
                         1.5 * np.sin(i * TAU / 12), 0]),
                     stroke_color=MUTED, stroke_width=1.5)
                for i in range(12)
            ])

            # Arrow — centered between circle and interlocked rows
            arrow = Arrow(
                LEFT * 1.8, RIGHT * 0.2,
                color=AMBER, stroke_width=3,
            ).move_to(ORIGIN + DOWN * 0.2)
            arrow_lbl = txt("rearrange", 18, AMBER)
            arrow_lbl.next_to(arrow, UP, buff=0.18)

            # Interlocked coarse
            row_coarse = interlocked(12, 1.5).scale(0.38)
            row_coarse.move_to(RIGHT * 3.5 + UP * 0.6)
            coarse_lbl = txt("12 slices", 18, MUTED)
            coarse_lbl.next_to(row_coarse, DOWN, buff=0.2)

            # Interlocked finer
            row_fine = interlocked(24, 1.5).scale(0.38)
            row_fine.move_to(RIGHT * 3.5 + DOWN * 1.2)
            fine_lbl = txt("24 slices — almost flat!", 18, SUCCESS)
            fine_lbl.next_to(row_fine, DOWN, buff=0.2)

            # Rectangle hint around fine version
            rect_ghost = RoundedRectangle(
                width=row_fine.width + 0.2, height=row_fine.height + 0.15,
                corner_radius=0.05, stroke_color=AMBER, stroke_width=2,
                fill_opacity=0,
            ).move_to(row_fine.get_center())

            note = txt("An early glimpse of calculus!", 22, VIOLET, "BOLD")
            note.move_to(DOWN * 3.1)

            self.play(FadeIn(head), Create(circ), run_time=0.08 * d)
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(
                SpiralIn(arch_label, scale_factor=0.1),
                FadeIn(year_label),
                run_time=0.10 * d,
            )
            self.add_sound(self.sfx["click"], gain=-18)
            self.play(
                LaggedStart(*[Create(sl) for sl in slice_lines], lag_ratio=0.08),
                run_time=0.14 * d,
            )
            self.play(GrowArrow(arrow), FadeIn(arrow_lbl), run_time=0.08 * d)
            self.add_sound(self.sfx["pop"], gain=-16)
            self.play(Create(row_coarse), FadeIn(coarse_lbl), run_time=0.14 * d)
            self.play(
                Create(row_fine), FadeIn(fine_lbl),
                run_time=0.14 * d,
            )
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(
                Create(rect_ghost),
                ShowPassingFlash(
                    rect_ghost.copy().set_stroke(SUCCESS, 4),
                    time_width=0.5,
                ),
                run_time=0.12 * d,
            )
            self.play(
                FadeIn(note, shift=UP * 0.15),
                Flash(circ.get_center(), color=ACCENT, flash_radius=1.2,
                      num_lines=10, line_length=0.3),
                run_time=0.12 * d,
            )
            self.play(
                FadeOut(VGroup(
                    head, circ, slice_lines, arch_label, year_label,
                    arrow, arrow_lbl, row_coarse, coarse_lbl,
                    row_fine, fine_lbl, rect_ghost, note,
                )),
                run_time=0.08 * d,
            )

    # -- Beat 4: Fundamentals --------------------------------------------------
    def beat_fundamentals(self) -> None:
        with self.voiceover(text=NARRATION["fundamentals"]) as tracker:
            d = tracker.duration

            head = heading("Three measurements you need")

            circ = Circle(radius=_R, color=ACCENT, stroke_width=3)
            circ.move_to(LEFT * 3.5 + DOWN * 0.3)

            # Centre dot
            centre = Dot(circ.get_center(), color=AMBER, radius=0.07)
            c_lbl = txt("O", 20, AMBER)
            c_lbl.next_to(centre, DL, buff=0.1)

            # --- Radius ---
            r_line = Line(
                circ.get_center(), circ.get_center() + RIGHT * _R,
                stroke_color=SUCCESS, stroke_width=3,
            )
            r_lbl = MathTex(r"r", font_size=36, color=SUCCESS)
            r_lbl.next_to(r_line, UP, buff=0.15)

            # Info cards on the right — stacked with consistent left alignment
            card_left_x = 1.6  # common left-edge x position

            r_card = VGroup(
                txt("Radius", 24, SUCCESS, "BOLD"),
                txt("centre to edge", 18, MUTED),
            ).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            r_card.move_to(RIGHT * 3.2 + UP * 2.0)
            r_card.set_x(card_left_x, direction=LEFT)

            # --- Diameter ---
            d_line = DashedLine(
                circ.get_center() + LEFT * _R,
                circ.get_center() + RIGHT * _R,
                stroke_color=ROSE, stroke_width=2.5, dash_length=0.12,
            )
            d_lbl = MathTex(r"d = 2r", font_size=30, color=ROSE)
            d_lbl.next_to(circ, DOWN, buff=0.5)

            d_card = VGroup(
                txt("Diameter", 24, ROSE, "BOLD"),
                txt("full width across", 18, MUTED),
            ).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            d_card.move_to(RIGHT * 3.2 + UP * 0.7)
            d_card.set_x(card_left_x, direction=LEFT)

            # --- Circumference ---
            circ_trace = Circle(
                radius=_R, color=AMBER, stroke_width=5,
            ).move_to(circ.get_center())

            c_eq = MathTex(r"C = 2\pi r", font_size=42, color=AMBER)
            c_card = VGroup(
                txt("Circumference", 24, AMBER, "BOLD"),
                txt("all the way round", 18, MUTED),
                c_eq,
            ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            c_card.move_to(RIGHT * 3.2 + DOWN * 0.9)
            c_card.set_x(card_left_x, direction=LEFT)

            # Travelling dot along circumference using MoveAlongPath
            trace_dot = Dot(color=AMBER, radius=0.08)
            trace_dot.move_to(circ_trace.point_from_proportion(0))

            # Depth shadow behind the circle
            circ_shadow = Circle(
                radius=_R + 0.04, color="#000000", stroke_width=0,
                fill_opacity=0.15,
            ).move_to(circ.get_center() + RIGHT * 0.06 + DOWN * 0.06)

            self.play(
                FadeIn(head), FadeIn(circ_shadow),
                Create(circ), FadeIn(centre), FadeIn(c_lbl),
                run_time=0.10 * d,
            )
            self.add_sound(self.sfx["click"], gain=-16)
            self.play(
                Create(r_line), FadeIn(r_lbl),
                GrowFromEdge(r_card, LEFT),
                run_time=0.16 * d,
            )
            self.add_sound(self.sfx["click"], gain=-16)
            self.play(
                Create(d_line), FadeIn(d_lbl),
                GrowFromEdge(d_card, LEFT),
                run_time=0.16 * d,
            )
            self.add_sound(self.sfx["whoosh"], gain=-16)
            self.play(
                MoveAlongPath(trace_dot, circ_trace),
                Create(circ_trace),
                run_time=0.22 * d,
            )
            self.add_sound(self.sfx["click"], gain=-16)
            self.play(
                GrowFromEdge(c_card, LEFT),
                FadeOut(trace_dot),
                run_time=0.12 * d,
            )
            self.add_sound(self.sfx["ding"], gain=-16)
            self.play(
                ShowPassingFlash(
                    circ_trace.copy().set_stroke(SUCCESS, 6),
                    time_width=0.4,
                ),
                run_time=0.12 * d,
            )
            self.play(
                FadeOut(VGroup(
                    head, circ, circ_shadow, centre, c_lbl,
                    r_line, r_lbl, r_card,
                    d_line, d_lbl, d_card,
                    circ_trace, c_card,
                )),
                run_time=0.12 * d,
            )

    # -- Beat 5: Build ---------------------------------------------------------
    def beat_build(self) -> None:
        with self.voiceover(text=NARRATION["build"]) as tracker:
            d = tracker.duration
            # Narration sentences (for sync reference):
            # S1: "Now watch carefully."                              ~3w
            # S2: "Take the circle and slice it into equal sectors."  ~9w
            # S3: "Colour half of them blue and the other half red."  ~10w
            # S4: "Now separate the sectors and lay them alternately,
            #      one pointing up, one pointing down, interlocking
            #      like the teeth of a zipper."                       ~21w
            # S5: "The bumpy edges begin to look almost straight.
            #      If we slice thinner and thinner, the bumps flatten
            #      out completely,"                                   ~19w
            # S6: "and we get a perfect rectangle."                   ~6w
            # Total ~68 words

            head = heading("Slice it into sectors")

            # Full circle — left side
            circ = Circle(
                radius=1.4, color=ACCENT, stroke_width=3, fill_opacity=0.12,
            ).move_to(LEFT * 4.5)

            # Sliced circle
            fan = sliced_circle(_N, 1.4).move_to(LEFT * 4.5)

            # Colour legend — beside the circle
            legend = VGroup(
                VGroup(Dot(color=ACCENT, radius=0.06),
                       txt("blue", 18, ACCENT)).arrange(RIGHT, buff=0.12),
                VGroup(Dot(color=ROSE, radius=0.06),
                       txt("red", 18, ROSE)).arrange(RIGHT, buff=0.12),
            ).arrange(RIGHT, buff=0.5)
            legend.move_to(LEFT * 4.5 + DOWN * 2.0)

            # Interlocked coarse — full width, generous vertical space
            row1 = interlocked(_N, 1.4).scale(0.45)
            row1.move_to(RIGHT * 1.8 + UP * 1.2)
            row1_lbl = txt("Interlock like a zipper", 20, INK)
            row1_lbl.next_to(row1, DOWN, buff=0.2)

            # Interlocked fine — placed well below row1
            row2 = interlocked(_N2, 1.4).scale(0.45)
            row2.move_to(RIGHT * 1.8 + DOWN * 0.8)
            row2_lbl = txt("Thinner slices, straighter edges", 18, SUCCESS)
            row2_lbl.next_to(row2, DOWN, buff=0.15)

            # Rectangle outline around fine version
            rect_hint = RoundedRectangle(
                width=row2.width + 0.3, height=row2.height + 0.2,
                corner_radius=0.05,
                stroke_color=AMBER, stroke_width=2.5, fill_opacity=0,
            ).move_to(row2.get_center())

            # "A perfect rectangle!" placed below row2_lbl with extra spacing
            perfect_lbl = txt("A perfect rectangle!", 24, AMBER, "BOLD")
            perfect_lbl.next_to(row2_lbl, DOWN, buff=0.35)

            # --- Animations synced to narration sentences ---

            # S1: "Now watch carefully." + S2 start: head + circle appear
            self.play(
                FadeIn(head), DrawBorderThenFill(circ),
                run_time=0.06 * d,
            )
            # S2: "Take the circle and slice it into equal sectors."
            self.play(
                ReplacementTransform(circ, fan),
                run_time=0.12 * d,
            )
            # S3: "Colour half of them blue and the other half red."
            self.play(FadeIn(legend), run_time=0.10 * d)
            # S4: "Now separate the sectors and lay them alternately,
            #      one pointing up, one pointing down, interlocking
            #      like the teeth of a zipper."
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(
                LaggedStart(*[GrowFromCenter(s) for s in row1], lag_ratio=0.04),
                run_time=0.18 * d,
            )
            self.play(FadeIn(row1_lbl), run_time=0.08 * d)
            # S5: "The bumpy edges begin to look almost straight.
            #      If we slice thinner and thinner..."
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(
                LaggedStart(*[GrowFromCenter(s) for s in row2], lag_ratio=0.02),
                FadeIn(row2_lbl),
                run_time=0.18 * d,
            )
            # S6: "and we get a perfect rectangle."
            self.add_sound(self.sfx["ding"], gain=-12)
            self.play(
                Create(rect_hint),
                FadeIn(perfect_lbl, shift=UP * 0.15),
                Flash(row2.get_center(), color=AMBER, flash_radius=0.5),
                run_time=0.12 * d,
            )
            self.play(
                ShowPassingFlash(
                    rect_hint.copy().set_stroke(SUCCESS, 5),
                    time_width=0.4,
                ),
                run_time=0.08 * d,
            )
            self.play(
                FadeOut(VGroup(
                    head, fan, legend,
                    row1, row1_lbl, row2, row2_lbl, rect_hint, perfect_lbl,
                )),
                run_time=0.08 * d,
            )

    # -- Beat 6: Formal --------------------------------------------------------
    def beat_formal(self) -> None:
        with self.voiceover(text=NARRATION["formal"]) as tracker:
            d = tracker.duration

            head = heading("It is a rectangle!")

            # The equivalent rectangle
            rect = Rectangle(
                width=5.0, height=1.5,
                fill_color=ACCENT, fill_opacity=0.10,
                stroke_color=ACCENT, stroke_width=3,
            ).move_to(UP * 0.7)

            # Height brace (left)
            h_brace = Brace(rect, LEFT, color=AMBER)
            h_lbl = MathTex(r"r", font_size=38, color=AMBER)
            h_lbl.next_to(h_brace, LEFT, buff=0.18)

            # Width brace (bottom) — VIOLET for variety
            w_brace = Brace(rect, DOWN, color=VIOLET)
            w_lbl = MathTex(r"\pi r", font_size=38, color=VIOLET)
            w_lbl.next_to(w_brace, DOWN, buff=0.18)

            w_note = txt("= half the circumference", 18, MUTED)
            w_note.next_to(w_lbl, RIGHT, buff=0.2)

            # Formula build-up with coloured parts
            f1 = MathTex(
                r"\text{Area}", r"=", r"\pi r", r"\times", r"r",
                font_size=42, color=INK,
            ).move_to(DOWN * 1.6)
            f1[2].set_color(VIOLET)
            f1[4].set_color(AMBER)

            f2 = MathTex(
                r"\text{Area}", r"=", r"\pi r^2",
                font_size=50, color=SUCCESS,
            ).move_to(DOWN * 1.6)

            box = SurroundingRectangle(f2, color=AMBER, buff=0.2, corner_radius=0.12)

            same_note = txt("Circle reshaped, area preserved", 20, MUTED)
            same_note.move_to(DOWN * 2.9)

            # Depth shadow behind the rectangle for 3D feel
            rect_shadow = Rectangle(
                width=5.0, height=1.5,
                fill_color="#000000", fill_opacity=0.12,
                stroke_width=0,
            ).move_to(rect.get_center() + RIGHT * 0.08 + DOWN * 0.08)

            self.play(
                FadeIn(head), FadeIn(rect_shadow),
                DrawBorderThenFill(rect),
                run_time=0.08 * d,
            )
            self.add_sound(self.sfx["pop"], gain=-16)
            self.play(
                GrowFromCenter(h_brace),
                SpinInFromNothing(h_lbl),
                run_time=0.12 * d,
            )
            self.add_sound(self.sfx["pop"], gain=-16)
            self.play(
                GrowFromCenter(w_brace),
                SpinInFromNothing(w_lbl),
                FadeIn(w_note),
                run_time=0.14 * d,
            )
            # TransformFromCopy: copy the labels into the formula
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(
                TransformFromCopy(w_lbl, f1[2]),
                TransformFromCopy(h_lbl, f1[4]),
                Write(VGroup(f1[0], f1[1], f1[3])),
                run_time=0.18 * d,
            )
            self.play(
                ReplacementTransform(f1, f2),
                run_time=0.14 * d,
            )
            self.add_sound(self.sfx["success"], gain=-12)
            self.play(
                Create(box),
                Flash(f2.get_center(), color=SUCCESS, flash_radius=0.6,
                      num_lines=12),
                run_time=0.12 * d,
            )
            self.play(
                FadeIn(same_note, shift=UP * 0.1),
                run_time=0.12 * d,
            )
            self.play(
                FadeOut(VGroup(
                    head, rect, rect_shadow, h_brace, h_lbl,
                    w_brace, w_lbl, w_note, f2, box, same_note,
                )),
                run_time=0.10 * d,
            )

    # -- Beat 7: Why -----------------------------------------------------------
    def beat_why(self) -> None:
        with self.voiceover(text=NARRATION["why"]) as tracker:
            d = tracker.duration
            # Narration (60 words):
            # S1: "But why is the width only half the circumference?"
            # S2: "Think about the interlocked sectors."
            # S3: "Half of the curved edges point upward along the top,"
            # S4: "and the other half point downward along the bottom."
            # S5: "So each long side of the rectangle carries exactly
            #      half the total circumference."
            # S6: "That is why the width is pi r and not two pi r."

            head = heading("Why only half?")

            # Interlocked shape — moderate scale, centered in upper area
            row = interlocked(_N, 1.4).scale(0.75)
            row.move_to(UP * 0.4)

            # Use actual bounding box edges so lines sit OUTSIDE the figure
            row_top_y = row.get_top()[1]
            row_bot_y = row.get_bottom()[1]
            row_left_x = row.get_left()[0]
            row_right_x = row.get_right()[0]

            # Top edge highlight — just above the actual top of the shape
            top_line = Line(
                np.array([row_left_x, row_top_y + 0.1, 0]),
                np.array([row_right_x, row_top_y + 0.1, 0]),
                stroke_color=ACCENT, stroke_width=5,
            )
            top_lbl = MathTex(r"\pi r", font_size=36, color=ACCENT)
            top_lbl.next_to(top_line, UP, buff=0.12)
            top_note = txt("half the arcs point up", 20, ACCENT)
            top_note.next_to(top_lbl, RIGHT, buff=0.35)

            # Bottom edge highlight — just below the actual bottom
            bot_line = Line(
                np.array([row_left_x, row_bot_y - 0.1, 0]),
                np.array([row_right_x, row_bot_y - 0.1, 0]),
                stroke_color=ROSE, stroke_width=5,
            )
            bot_lbl = MathTex(r"\pi r", font_size=36, color=ROSE)
            bot_lbl.next_to(bot_line, DOWN, buff=0.12)
            bot_note = txt("half the arcs point down", 20, ROSE)
            bot_note.next_to(bot_lbl, RIGHT, buff=0.35)

            # Total circumference — well below the figure
            total = VGroup(
                txt("Total circumference", 22, MUTED),
                MathTex(r"= 2\pi r", font_size=34, color=MUTED),
            ).arrange(RIGHT, buff=0.25)
            total.move_to(DOWN * 2.5)

            # Conclusion with math symbols
            conclusion = VGroup(
                txt("Width is", 24, VIOLET, "BOLD"),
                MathTex(r"\pi r", font_size=38, color=VIOLET),
                txt(", not", 24, VIOLET, "BOLD"),
                MathTex(r"2\pi r", font_size=38, color=VIOLET),
            ).arrange(RIGHT, buff=0.18)
            conclusion.move_to(DOWN * 3.3)

            # --- Animations synced to narration ---

            # S1: "But why is the width only half the circumference?"
            self.play(FadeIn(head), run_time=0.10 * d)

            # S2: "Think about the interlocked sectors."
            self.play(
                LaggedStart(*[GrowFromCenter(s) for s in row], lag_ratio=0.03),
                run_time=0.10 * d,
            )

            # S3: "Half of the curved edges point upward along the top,"
            self.play(
                Create(top_line),
                FadeIn(top_lbl), FadeIn(top_note),
                ShowPassingFlash(
                    top_line.copy().set_stroke(SUCCESS, 8),
                    time_width=0.3,
                ),
                run_time=0.18 * d,
            )

            # S4: "and the other half point downward along the bottom."
            self.play(
                Create(bot_line),
                FadeIn(bot_lbl), FadeIn(bot_note),
                ShowPassingFlash(
                    bot_line.copy().set_stroke(ORANGE, 8),
                    time_width=0.3,
                ),
                run_time=0.18 * d,
            )

            # S5: "So each long side...exactly half the total circumference."
            self.play(
                FadeIn(total, shift=UP * 0.15),
                Indicate(top_lbl, color=SUCCESS),
                Indicate(bot_lbl, color=SUCCESS),
                run_time=0.18 * d,
            )

            # S6: "That is why the width is pi r and not two pi r."
            self.add_sound(self.sfx["ding"], gain=-12)
            self.play(
                FadeIn(conclusion, shift=UP * 0.15),
                FocusOn(conclusion.get_center(), color=VIOLET, opacity=0.12),
                run_time=0.16 * d,
            )

            self.play(
                FadeOut(VGroup(
                    head, row, top_line, top_lbl, top_note,
                    bot_line, bot_lbl, bot_note, total, conclusion,
                )),
                run_time=0.10 * d,
            )

    # -- Beat 8: Working -------------------------------------------------------
    def beat_working(self) -> None:
        with self.voiceover(text=NARRATION["working"]) as tracker:
            d = tracker.duration

            head = heading("Find the radius first")

            # Given panel
            panel = given_panel([
                "Circumference = 22 cm",
                "Find the area",
            ], width=5.5)
            panel.move_to(LEFT * 4.0 + UP * 0.5)

            # Steps on the right — each step enters with a different animation
            s1 = MathTex(r"2\pi r = 22", font_size=38, color=ACCENT)
            s2 = MathTex(r"\pi = \frac{22}{7}", font_size=32, color=MUTED)
            s3 = MathTex(r"r = \frac{22}{2 \times \frac{22}{7}}", font_size=32, color=INK)
            s4 = MathTex(r"r = 3.5\ \text{cm}", font_size=38, color=SUCCESS)

            work = VGroup(s1, s2, s3, s4).arrange(DOWN, buff=0.4)
            work.move_to(RIGHT * 2.5 + UP * 0.3)

            r_box = SurroundingRectangle(s4, color=AMBER, buff=0.15, corner_radius=0.08)

            # Small decorative circle on the left
            mini = Circle(radius=0.6, color=ACCENT, stroke_width=2,
                          fill_opacity=0.06).move_to(LEFT * 4.0 + DOWN * 2.0)
            c_trace = Arc(radius=0.6, start_angle=0, angle=TAU,
                          color=AMBER, stroke_width=3).move_to(mini.get_center())
            c_val = txt("C = 22", 16, AMBER)
            c_val.next_to(mini, DOWN, buff=0.15)

            self.play(
                FadeIn(head),
                FadeIn(panel, shift=RIGHT * 0.2),
                Create(mini), FadeIn(c_val),
                run_time=0.10 * d,
            )
            self.play(
                Create(c_trace),
                Write(s1),
                run_time=0.18 * d,
            )
            self.play(FadeIn(s2, shift=DOWN * 0.1), run_time=0.12 * d)
            self.play(Write(s3), run_time=0.20 * d)
            self.add_sound(self.sfx["success"], gain=-12)
            self.play(
                Write(s4), Create(r_box),
                Flash(s4.get_center(), color=SUCCESS, flash_radius=0.4),
                run_time=0.22 * d,
            )
            self.play(
                FadeOut(VGroup(head, panel, work, r_box, mini, c_trace, c_val)),
                run_time=0.18 * d,
            )

    # -- Beat 9: Example -------------------------------------------------------
    def beat_example(self) -> None:
        with self.voiceover(text=NARRATION["example"]) as tracker:
            d = tracker.duration

            head = heading("Apply the formula")

            # Circle diagram on the left with animated fill
            mini_circ = Circle(
                radius=0.85, color=ACCENT, stroke_width=2.5, fill_opacity=0.08,
            ).move_to(LEFT * 4.5 + UP * 0.5)
            mini_r = Line(
                mini_circ.get_center(),
                mini_circ.get_center() + RIGHT * 0.85,
                stroke_color=AMBER, stroke_width=2.5,
            )
            mini_r_lbl = MathTex(r"3.5", font_size=22, color=AMBER)
            mini_r_lbl.next_to(mini_r, UP, buff=0.08)

            # Fill the circle gradually to show "area"
            filled = Circle(
                radius=0.85, color=SUCCESS, fill_opacity=0.3,
                stroke_width=0,
            ).move_to(mini_circ.get_center())

            # Working steps
            l1 = MathTex(r"\text{Area} = \pi r^2", font_size=38, color=ACCENT)
            l2 = MathTex(
                r"= \frac{22}{7} \times (3.5)^2",
                font_size=36, color=INK,
            )
            l3 = MathTex(
                r"= \frac{22}{7} \times 12.25",
                font_size=36, color=INK,
            )
            l4 = MathTex(
                r"= 38.5\ \text{cm}^2",
                font_size=42, color=SUCCESS,
            )

            steps = VGroup(l1, l2, l3, l4).arrange(DOWN, buff=0.38)
            steps.move_to(RIGHT * 1.0 + DOWN * 0.1)

            ans_box = SurroundingRectangle(l4, color=AMBER, buff=0.18, corner_radius=0.1)

            self.play(
                FadeIn(head),
                Create(mini_circ), Create(mini_r), FadeIn(mini_r_lbl),
                run_time=0.10 * d,
            )
            self.play(Write(l1), run_time=0.16 * d)
            self.add_sound(self.sfx["click"], gain=-18)
            self.play(Write(l2), run_time=0.18 * d)
            self.add_sound(self.sfx["click"], gain=-18)
            self.play(
                Write(l3),
                FadeIn(filled),
                run_time=0.18 * d,
            )
            self.add_sound(self.sfx["success"], gain=-12)
            self.play(
                Write(l4), Create(ans_box),
                Flash(l4.get_center(), color=AMBER, flash_radius=0.4),
                run_time=0.18 * d,
            )
            self.play(
                FadeOut(VGroup(head, mini_circ, mini_r, mini_r_lbl,
                               filled, steps, ans_box)),
                run_time=0.20 * d,
            )

    # -- Beat 10: Second Example -----------------------------------------------
    def beat_example2(self) -> None:
        with self.voiceover(text=NARRATION["example2"]) as tracker:
            d = tracker.duration

            head = heading("One more example")

            # Garden circle with decorative ring
            garden = Circle(
                radius=1.0, color=SUCCESS, fill_opacity=0.15, stroke_width=3,
            ).move_to(LEFT * 4.2 + UP * 0.3)
            # Decorative inner ring
            inner = Circle(
                radius=0.5, color=SUCCESS, stroke_width=1.5, fill_opacity=0.08,
            ).move_to(garden.get_center())
            garden_lbl = txt("circular garden", 18, SUCCESS)
            garden_lbl.next_to(garden, DOWN, buff=0.25)

            r_line = Line(
                garden.get_center(), garden.get_center() + RIGHT * 1.0,
                stroke_color=AMBER, stroke_width=3,
            )
            r_val = MathTex(r"r = 7\ \text{m}", font_size=26, color=AMBER)
            r_val.next_to(r_line, UP, buff=0.12)

            # Working
            e1 = MathTex(r"\text{Area} = \pi r^2", font_size=36, color=ACCENT)
            e2 = MathTex(r"= \frac{22}{7} \times 7^2", font_size=34, color=INK)
            e3 = MathTex(r"= \frac{22}{7} \times 49", font_size=34, color=INK)
            e4 = MathTex(r"= 154\ \text{m}^2", font_size=40, color=SUCCESS)
            work = VGroup(e1, e2, e3, e4).arrange(DOWN, buff=0.38)
            work.move_to(RIGHT * 2.0 + UP * 0.2)

            ans_box = SurroundingRectangle(e4, color=AMBER, buff=0.15, corner_radius=0.1)

            # Garden filling animation
            garden_fill = Circle(
                radius=1.0, color=LIME, fill_opacity=0.25,
                stroke_width=0,
            ).move_to(garden.get_center())

            self.play(
                FadeIn(head),
                DrawBorderThenFill(garden), FadeIn(inner),
                FadeIn(garden_lbl),
                Create(r_line), FadeIn(r_val),
                run_time=0.12 * d,
            )
            self.add_sound(self.sfx["whoosh"], gain=-15)
            self.play(Write(e1), run_time=0.12 * d)
            self.add_sound(self.sfx["click"], gain=-18)
            self.play(Write(e2), run_time=0.14 * d)
            self.add_sound(self.sfx["click"], gain=-18)
            self.play(
                Write(e3),
                FadeIn(garden_fill),
                run_time=0.14 * d,
            )
            self.add_sound(self.sfx["success"], gain=-12)
            self.play(
                Write(e4), Create(ans_box),
                Flash(e4.get_center(), color=SUCCESS, flash_radius=0.4),
                run_time=0.18 * d,
            )
            self.play(
                LaggedStart(
                    ShrinkToCenter(garden), ShrinkToCenter(inner),
                    ShrinkToCenter(garden_fill),
                    FadeOut(VGroup(head, garden_lbl, r_line, r_val, work, ans_box)),
                    lag_ratio=0.1,
                ),
                run_time=0.30 * d,
            )

    # -- Beat 11: Summary -----------------------------------------------------
    def beat_summary(self) -> None:
        with self.voiceover(text=NARRATION["summary"]) as tracker:
            d = tracker.duration

            # Grand finale card
            frame = card(10.5, 5.0, ACCENT)
            frame.move_to(ORIGIN)

            line1 = txt("A circle is a rectangle in disguise", 26, INK, "BOLD")

            # Height/width labels — use MathTex throughout for consistent baseline
            line2 = VGroup(
                MathTex(r"\text{height} = r", font_size=32, color=AMBER),
                MathTex(r",", font_size=32, color=MUTED),
                MathTex(r"\text{width} = \pi r", font_size=32, color=VIOLET),
            ).arrange(RIGHT, buff=0.2)

            bar = rule_line(4.0)

            formula = MathTex(
                r"\text{Area} = \pi r^2",
                font_size=52, color=SUCCESS,
            )
            formula_box = SurroundingRectangle(
                formula, color=SUCCESS, buff=0.22, corner_radius=0.12,
            )

            archimedes_note = txt(
                "From Archimedes to your classroom", 20, VIOLET,
            )

            body = VGroup(
                line1, line2, bar, VGroup(formula, formula_box), archimedes_note,
            ).arrange(DOWN, buff=0.35).move_to(frame.get_center())

            # Orbiting decoration on the card
            orbit_ring = Circle(radius=4.0, color=ACCENT, stroke_width=0)
            orbit_dots = VGroup(*[
                Dot(orbit_ring.point_from_proportion(i / 6),
                    color=[ACCENT, SUCCESS, AMBER, ROSE, VIOLET, TEAL][i],
                    radius=0.05)
                for i in range(6)
            ])

            self.add_sound(self.sfx["whoosh"], gain=-15)
            self.play(
                FadeIn(frame),
                LaggedStart(*[SpiralIn(dot, scale_factor=0.1)
                              for dot in orbit_dots], lag_ratio=0.1),
                run_time=0.14 * d,
            )
            self.play(
                FadeIn(line1, shift=UP * 0.2),
                run_time=0.12 * d,
            )
            self.add_sound(self.sfx["click"], gain=-18)
            self.play(FadeIn(line2), run_time=0.10 * d)
            self.play(Create(bar), run_time=0.06 * d)
            self.add_sound(self.sfx["ding"], gain=-12)
            self.play(
                SpinInFromNothing(formula),
                Create(formula_box),
                run_time=0.20 * d,
            )
            self.play(
                FadeIn(archimedes_note, shift=UP * 0.1),
                run_time=0.08 * d,
            )
            self.add_sound(self.sfx["success"], gain=-10)
            self.play(
                Flash(formula.get_center(), color=AMBER, flash_radius=0.8,
                      num_lines=18, line_length=0.35),
                run_time=0.14 * d,
            )
            self.play(
                *[Rotate(dot, angle=PI / 3, about_point=ORIGIN)
                  for dot in orbit_dots],
                run_time=0.10 * d,
            )
            self.play(FadeOut(orbit_dots), run_time=0.06 * d)

        self.wait(END_HOLD)

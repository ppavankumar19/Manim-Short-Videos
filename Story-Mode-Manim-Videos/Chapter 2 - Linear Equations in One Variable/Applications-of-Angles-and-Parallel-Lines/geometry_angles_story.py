"""
Applications of Angles and Parallel Lines — Finding Unknown Angles
Story-mode chalkboard lesson (Telangana Class 8 Maths, Chapter 2:
Linear Equations in One Variable, geometric applications).

Core idea: the DIAGRAM decides the relationship, and the relationship decides
the equation. Two parallel lines cut by a transversal give either
  - same-side interior angles:  A + B = 180 degrees, or
  - corresponding angles:       A = B.
The two angle sectors physically leave the diagram and become the terms of the
equation, so nothing ever appears magically. After solving, x returns to the
diagram and the angles are read off (x is NOT the angle).

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
  0. Title card -- Geometry gives the rule. Algebra finds x.
  1. The Diagram -- parallel lines l, m, transversal p, two marked angles.
  2. Same-Side Interior -- the sectors combine into a straight 180 degrees.
  3. Geometry -> Equation -- (3x+20) + (5x-8) = 180.
  4. Solve -- x = 21.
  5. Return to the Diagram -- 83 degrees and 97 degrees, checked.
  6. Corresponding Angles -- 5x = 2x + 24.
  7. Solve -- x = 8, both angles 40 degrees.
  8. The Routine -- identify, relate, form, solve, interpret.
  9. Student Challenge -- supplementary angles differing by 34 -> 73 and 107.
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
    ImageMobject, MathTex, VGroup, VMobject, Line, DashedLine, Circle,
    Rectangle, RoundedRectangle, Polygon, Triangle, Arc, Sector, Arrow,
    DoubleArrow, Text, Write, FadeIn, FadeOut, Create, ReplacementTransform,
    TransformMatchingTex, TransformFromCopy, GrowArrow, Indicate, Flash,
    Circumscribe, SurroundingRectangle, Rotate, config,
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

LINE_COLOR = CHALK_CYAN        # the parallel lines
TRANS_COLOR = CHALK_AMBER      # the transversal
ANGLE_A_COLOR = CHALK_GREEN    # angle A (and its expression)
ANGLE_B_COLOR = CHALK_PINK     # angle B
RADIUS = 0.5                   # angle arc radius

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

EQ_Y = -1.75        # equation line under the diagram
HEAD_Y = BOARD_TOP - 0.45

# the fixed geometry of the diagram (parallel lines + transversal)
L_Y = 1.25          # upper parallel line
M_Y = -0.45         # lower parallel line
X0, X1 = -3.5, 4.5  # the extent of both parallel lines
P_TOP = np.array([-0.45, 2.15, 0.0])     # transversal, upper end
P_BOT = np.array([1.45, -1.35, 0.0])     # transversal, lower end


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


# ------------------------------------------------------- angle machinery ----
def unit(v) -> np.ndarray:
    v = np.array(v, dtype=float)
    v[2] = 0.0
    n = np.linalg.norm(v)
    return v / n if n > 1e-9 else np.array([1.0, 0.0, 0.0])


def angle_wedge(vertex, d1, d2, radius: float = RADIUS, color: str = ANGLE_A_COLOR,
                fill: float = 0.3, label: str | None = None,
                label_size: int = 26, push: float = 0.34) -> VGroup:
    """A translucent angle sector between two rays from `vertex`.

    The smaller of the two possible wedges is always used, so the caller only
    has to give the two ray directions. A Manim `Sector` is built with its apex
    at the local origin, so it is SHIFTED (never `move_to`, which would centre
    its bounding box and slide the wedge to the wrong side of the vertex).
    """
    a1 = float(np.arctan2(d1[1], d1[0]))
    a2 = float(np.arctan2(d2[1], d2[0]))
    diff = (a2 - a1) % TAU
    if diff > PI:
        a1, a2 = a2, a1
        diff = TAU - diff
    sec = Sector(radius=radius, start_angle=a1, angle=diff,
                 stroke_color=color, stroke_width=2.2,
                 fill_color=color, fill_opacity=fill)
    vertex = np.array(vertex, dtype=float)
    vertex[2] = 0.0
    sec.shift(vertex)
    grp = VGroup(sec)
    if label is not None:
        mid = a1 + diff / 2
        pos = vertex + (radius + push) * np.array([np.cos(mid), np.sin(mid), 0.0])
        lbl = MathTex(label, font_size=label_size, color=color).move_to(pos)
        grp.add(lbl)
        grp.lbl = lbl
    grp.sector = sec
    return grp


def parallel_pair(l_y: float = L_Y, m_y: float = M_Y,
                  x0: float = X0, x1: float = X1) -> VGroup:
    """Two parallel lines with chalk chevron marks and their letters."""
    lines = VGroup()
    for y, name in ((l_y, "l"), (m_y, "m")):
        ln = Line(np.array([x0, y, 0]), np.array([x1, y, 0]),
                  stroke_color=LINE_COLOR, stroke_width=2.6)
        chev = VGroup(*[
            VGroup(Line(np.array([0, -0.09, 0]), np.array([0.11, 0, 0]),
                        stroke_color=LINE_COLOR, stroke_width=2),
                   Line(np.array([0, 0.09, 0]), np.array([0.11, 0, 0]),
                        stroke_color=LINE_COLOR, stroke_width=2))
            .move_to(np.array([x, y, 0]))
            for x in (x1 - 0.5, x1 - 0.78)
        ])
        lbl = MathTex(name, font_size=30, color=LINE_COLOR).move_to(
            np.array([x0 - 0.3, y + 0.02, 0]))
        lines.add(VGroup(ln, chev, lbl))
    return lines


def transversal() -> VGroup:
    ln = Line(P_TOP, P_BOT, stroke_color=TRANS_COLOR, stroke_width=2.6)
    lbl = MathTex("p", font_size=30, color=TRANS_COLOR).move_to(
        P_TOP + np.array([0.28, 0.12, 0]))
    return VGroup(ln, lbl)


def intersections(l_y: float = L_Y, m_y: float = M_Y) -> tuple[np.ndarray, np.ndarray]:
    """Where the transversal meets the two parallel lines."""
    d = P_BOT - P_TOP
    e_t = (l_y - P_TOP[1]) / d[1]
    f_t = (m_y - P_TOP[1]) / d[1]
    return P_TOP + e_t * d, P_TOP + f_t * d


def down_dir() -> np.ndarray:
    return unit(P_BOT - P_TOP)


def up_dir() -> np.ndarray:
    return unit(P_TOP - P_BOT)


def wedge_span(d1, d2) -> tuple[float, float]:
    """Start angle and span of the smaller wedge between two ray directions."""
    a1 = float(np.arctan2(d1[1], d1[0]))
    a2 = float(np.arctan2(d2[1], d2[0]))
    diff = (a2 - a1) % TAU
    if diff > PI:
        a1, a2 = a2, a1
        diff = TAU - diff
    return a1, diff


def diagram() -> dict:
    """The complete parallel-lines diagram with the two same-side interior
    wedges, all from one set of coordinates so nothing can drift apart."""
    lines = parallel_pair()
    trans = transversal()
    e, f = intersections()
    w_a = angle_wedge(e, LEFT, down_dir(), color=ANGLE_A_COLOR, fill=0.32)
    w_b = angle_wedge(f, LEFT, up_dir(), color=ANGLE_B_COLOR, fill=0.32)
    span_a, span_b = wedge_span(LEFT, down_dir())[1], wedge_span(LEFT, up_dir())[1]
    return {"lines": lines, "trans": trans, "e": e, "f": f,
            "w_a": w_a, "w_b": w_b, "span_a": span_a, "span_b": span_b}


def label_at(vertex, direction, tex: str, color: str, size: int = 24,
             push: float = 0.95) -> MathTex:
    """An angle label sitting outward along the wedge's bisector."""
    a = float(np.arctan2(direction[1], direction[0]))
    return MathTex(tex, font_size=size, color=color).move_to(
        np.array(vertex, dtype=float) + push * np.array([np.cos(a), np.sin(a), 0.0]))


def mid_dir(d1, d2) -> np.ndarray:
    a1, diff = wedge_span(d1, d2)
    mid = a1 + diff / 2
    return np.array([np.cos(mid), np.sin(mid), 0.0])


def attached_label(pos, target, tex: str, color: str,
                   size: int = 24) -> VGroup:
    """An angle expression placed clear of the lines, tied to its arc by a
    dashed leader so it is never detached from the angle it belongs to."""
    lbl = MathTex(tex, font_size=size, color=color).move_to(np.array(pos, dtype=float))
    d = unit(np.array(target, dtype=float) - lbl.get_center())
    start = lbl.get_center() + d * (lbl.width / 2 + 0.1)
    leader = DashedLine(start, np.array(target, dtype=float), dash_length=0.06,
                        stroke_color=color, stroke_width=1.2, stroke_opacity=0.8)
    grp = VGroup(leader, lbl)
    grp.lbl, grp.leader = lbl, leader
    return grp


def summary_row(n: int, label: str, math_tex: str, color: str) -> VGroup:
    badge = Circle(radius=0.19, stroke_color=color, stroke_width=2,
                   fill_color=color, fill_opacity=0.18)
    num = board_text(str(n), 17, color, "BOLD").move_to(badge.get_center())
    return VGroup(VGroup(badge, num),
                  board_text(label, 18, CHALK_WHITE),
                  MathTex(math_tex, font_size=22)).arrange(RIGHT, buff=0.28)


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "Today we let geometry find the algebra.<bookmark mark='b0'/> A diagram "
        "can tell us how two angles are related, and that relationship becomes "
        "our equation.<bookmark mark='b1'/> Let's look at a diagram!"
        "<bookmark mark='b2'/>"
    ),
    "scene1": (
        "Here are two parallel lines, l and m, cut by a transversal, p."
        "<bookmark mark='b0'/> The chevrons tell us that the two lines are "
        "parallel.<bookmark mark='b1'/> Two angles are marked, and they carry "
        "algebraic expressions.<bookmark mark='b2'/> But before we solve for x, "
        "we must read the geometry.<bookmark mark='b3'/> What relationship "
        "connects these two angles?<bookmark mark='b4'/>"
    ),
    "scene2": (
        "Look carefully at where these two angles sit.<bookmark mark='b0'/> Both "
        "of them are inside the parallel lines, between l and m.<bookmark "
        "mark='b1'/> And both of them are on the same side of the transversal."
        "<bookmark mark='b2'/> Angles like these are called same-side interior "
        "angles, and for parallel lines their sum is one hundred and eighty "
        "degrees.<bookmark mark='b3'/> Watch this: if we slide the two sectors "
        "together, they exactly fill a straight line.<bookmark mark='b4'/> So A "
        "plus B equals one hundred and eighty degrees.<bookmark mark='b5'/>"
    ),
    "scene3": (
        "Now the geometry can give us the equation.<bookmark mark='b0'/> The "
        "first angle is three x plus twenty degrees.<bookmark mark='b1'/> The "
        "second angle is five x minus eight degrees.<bookmark mark='b2'/> "
        "Because they are same-side interior angles, they add up to one hundred "
        "and eighty.<bookmark mark='b3'/> So three x plus twenty, plus five x "
        "minus eight, equals one hundred and eighty.<bookmark mark='b4'/> Every "
        "term of this equation has a geometric reason.<bookmark mark='b5'/>"
    ),
    "scene4": (
        "Now the geometry is done, and we solve the equation.<bookmark mark='b0'/> "
        "Removing the brackets gives three x plus twenty, plus five x minus eight, "
        "equals one hundred and eighty.<bookmark mark='b1'/> Combining like terms "
        "gives eight x plus twelve equals one hundred and eighty.<bookmark "
        "mark='b2'/> So eight x equals one hundred and sixty eight, and x is one "
        "hundred and sixty eight divided by eight.<bookmark mark='b3'/> x equals "
        "twenty one.<bookmark mark='b4'/>"
    ),
    "scene5": (
        "But remember, x is not the angle.<bookmark mark='b0'/> Let's put twenty "
        "one back into the diagram.<bookmark mark='b1'/> The first angle is three "
        "times twenty one, plus twenty, which is eighty three degrees.<bookmark "
        "mark='b2'/> The second angle is five times twenty one, minus eight, "
        "which is ninety seven degrees.<bookmark mark='b3'/> And eighty three "
        "plus ninety seven is one hundred and eighty, exactly as the geometry "
        "promised.<bookmark mark='b4'/>"
    ),
    "scene6": (
        "Now let's meet a different relationship.<bookmark mark='b0'/> Here are "
        "the same parallel lines with a transversal.<bookmark mark='b1'/> These "
        "two angles sit in matching positions at the two intersections, so they "
        "are corresponding angles.<bookmark mark='b2'/> For parallel lines, "
        "corresponding angles are equal.<bookmark mark='b3'/> One of them is five "
        "x degrees, and the other is two x plus twenty four degrees, so five x "
        "equals two x plus twenty four.<bookmark mark='b4'/>"
    ),
    "scene7": (
        "The geometry has changed, but the algebra is exactly the same."
        "<bookmark mark='b0'/> Subtracting two x from both sides gives three x "
        "equals twenty four.<bookmark mark='b1'/> So x equals eight.<bookmark "
        "mark='b2'/> Both angles are forty degrees: five times eight, and two "
        "times eight plus twenty four.<bookmark mark='b3'/> Equal angles, equal "
        "expressions.<bookmark mark='b4'/>"
    ),
    "scene8": (
        "Here is the routine for every angle problem.<bookmark mark='b0'/> First, "
        "identify which angles the question is about.<bookmark mark='b1'/> Then "
        "relate them, using the geometry: are they equal, or do they add to one "
        "hundred and eighty?<bookmark mark='b2'/> Next, replace the angles with "
        "their algebraic expressions, to form the equation.<bookmark mark='b3'/> "
        "Solve it, and finally return to the diagram, and check the angles."
        "<bookmark mark='b4'/>"
    ),
    "scene9_setup": (
        "Your turn!<bookmark mark='b0'/> Two supplementary angles differ by "
        "thirty four degrees.<bookmark mark='b1'/> Let the smaller angle be x, so "
        "the larger angle is x plus thirty four.<bookmark mark='b2'/> Pause the "
        "video, and try it yourself.<bookmark mark='b3'/>"
    ),
    "scene9_reveal": (
        "Supplementary angles add to one hundred and eighty, so x plus, x plus "
        "thirty four, equals one hundred and eighty.<bookmark mark='b0'/> That "
        "gives two x plus thirty four equals one hundred and eighty, so two x "
        "equals one hundred and forty six, and x equals seventy three."
        "<bookmark mark='b1'/> The smaller angle is seventy three degrees, and "
        "the larger is seventy three plus thirty four, which is one hundred and "
        "seven degrees.<bookmark mark='b2'/> Let's check: seventy three plus one "
        "hundred and seven is one hundred and eighty. Well done!"
        "<bookmark mark='b3'/>"
    ),
    "scene10": (
        "Let's summarise.<bookmark mark='b0'/> Read the diagram first, and "
        "identify the angles.<bookmark mark='b1'/> Then use the geometry: "
        "corresponding angles are equal, and same-side interior angles add to one "
        "hundred and eighty.<bookmark mark='b2'/> Replace the angles with their "
        "expressions, and solve the equation.<bookmark mark='b3'/> Finally, "
        "return to the diagram, and check that the angles agree.<bookmark "
        "mark='b4'/> Geometry gives the rule, and algebra finds x. Thank you so "
        "much for watching, and I will see you in the next lesson!"
        "<bookmark mark='b5'/>"
    ),
}


class GeometryAnglesStory(VoiceoverScene):
    """Story-mode chalkboard lesson: angles and linear equations."""

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
        out_dir = _HERE / "media" / "videos" / "geometry_angles_story"
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
        self.beat1_diagram()
        self.beat2_rule()
        self.beat3_equation()
        self.beat4_solve()
        self.beat5_return()
        self.beat6_corresponding()
        self.beat7_solve_second()
        self.beat8_routine()
        self.beat9_challenge()
        self.beat10_summary()

        self._write_real_srt()

    # ================================================================ beats ==

    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Applications of Angles and Parallel Lines", 30, CHALK_WHITE,
                               "BOLD").move_to(np.array([BOARD_CX, BOARD_CY + 1.6, 0]))
            self.play(Write(title), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            sub = board_text("Finding unknown angles", 21, CHALK_YELLOW,
                             "BOLD").move_to(np.array([BOARD_CX, BOARD_CY + 0.95, 0]))
            self.play(Write(sub), run_time=rt(tracker.time_until_bookmark("b1") * 0.4))

            d = diagram()
            preview = VGroup(d["lines"], d["trans"], d["w_a"], d["w_b"])
            preview.scale(0.66, about_point=ORIGIN).move_to(
                np.array([BOARD_CX, -0.45, 0]))
            tag = board_text("Geometry gives the rule. Algebra finds x.", 19,
                             CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX, -2.05, 0]))

            self.play(FadeIn(preview, shift=DOWN * 0.1),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.6))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(FadeIn(tag), Flash(tag, color=CHALK_CYAN, flash_radius=0.8),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 1: the diagram ------------------------------------------------
    def beat1_diagram(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("Read the Diagram First", 25, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            d = diagram()
            e, f = d["e"], d["f"]
            w_a, w_b = d["w_a"], d["w_b"]
            lbl_a = attached_label(np.array([-2.35, 1.85, 0]),
                                   e + 0.55 * mid_dir(LEFT, down_dir()),
                                   "(3x+20)^\\circ", ANGLE_A_COLOR)
            lbl_b = attached_label(np.array([-1.6, -1.45, 0]),
                                   f + 0.55 * mid_dir(LEFT, up_dir()),
                                   "(5x-8)^\\circ", ANGLE_B_COLOR)

            self.play(Write(heading), Create(d["lines"]), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.5))
            self.play(Indicate(d["lines"], color=LINE_COLOR, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(Create(d["trans"]), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.6))
            self.play(Indicate(d["trans"], color=TRANS_COLOR, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(FadeIn(w_a.sector), FadeIn(w_b.sector),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(FadeIn(lbl_a), FadeIn(lbl_b),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.6))

            question = board_text("What relationship connects these angles?", 19,
                                  CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, -2.0, 0]))
            self.play(FadeIn(question),
                      Indicate(w_a.sector, color=ANGLE_A_COLOR, scale_factor=1.0),
                      Indicate(w_b.sector, color=ANGLE_B_COLOR, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["click"], gain=-15)

            tag = board_text("Before solving x, read the geometry.", 18,
                             CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -2.6, 0]))
            self.play(FadeIn(tag), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-12)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 2: same-side interior -> 180 ----------------------------------
    def beat2_rule(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("Same-Side Interior Angles", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            d = diagram()
            w_a, w_b = d["w_a"], d["w_b"]
            span_a, span_b = d["span_a"], d["span_b"]

            self.play(Write(heading), FadeIn(d["lines"]), FadeIn(d["trans"]),
                      FadeIn(w_a.sector), FadeIn(w_b.sector),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.5))

            # the interior band between the parallel lines
            band = Rectangle(width=(X1 - X0), height=(L_Y - M_Y),
                             stroke_color=CHALK_WHITE, stroke_width=1.2,
                             fill_color=CHALK_WHITE, fill_opacity=0.07)
            band.move_to(np.array([(X0 + X1) / 2, (L_Y + M_Y) / 2, 0]))
            lbl_int = board_text("interior", 15, CHALK_WHITE, "BOLD").move_to(
                np.array([-2.6, 0.95, 0]))
            self.play(FadeIn(band), FadeIn(lbl_int),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            lbl_side = board_text("same side", 15, CHALK_YELLOW, "BOLD").move_to(
                np.array([-2.6, 0.6, 0]))
            self.play(FadeIn(lbl_side),
                      Indicate(w_a.sector, color=ANGLE_A_COLOR, scale_factor=1.0),
                      Indicate(w_b.sector, color=ANGLE_B_COLOR, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b1") * 2))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(Flash(VGroup(lbl_int, lbl_side), color=CHALK_YELLOW,
                            flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # the two sectors slide out and exactly fill a straight line
            base = np.array([-2.5, -1.95, 0])
            flat_a = Sector(radius=0.42, start_angle=0, angle=span_a,
                            stroke_color=ANGLE_A_COLOR, stroke_width=2.2,
                            fill_color=ANGLE_A_COLOR, fill_opacity=0.35).shift(base)
            flat_b = Sector(radius=0.42, start_angle=span_a, angle=span_b,
                            stroke_color=ANGLE_B_COLOR, stroke_width=2.2,
                            fill_color=ANGLE_B_COLOR, fill_opacity=0.35).shift(base)
            straight = Line(base + np.array([-0.55, 0, 0]),
                            base + np.array([0.55, 0, 0]),
                            stroke_color=CHALK_WHITE, stroke_width=2.6)
            lab_180 = MathTex("180^\\circ", font_size=28, color=CHALK_YELLOW
                              ).next_to(straight, RIGHT, buff=0.5)
            self.play(TransformFromCopy(w_a.sector, flat_a),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            self.play(TransformFromCopy(w_b.sector, flat_b),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(Create(straight), FadeIn(lab_180),
                      run_time=rt(tracker.time_until_bookmark("b4")))

            rule = MathTex("A", "+", "B", "=", "180^\\circ", font_size=40,
                           color=CHALK_GREEN).move_to(np.array([2.9, -1.85, 0]))
            rbox = SurroundingRectangle(rule, color=CHALK_GREEN, buff=0.2,
                                        corner_radius=0.1, stroke_width=3)
            note = board_text("Same-side interior angles are supplementary.", 17,
                              CHALK_WHITE).move_to(np.array([BOARD_CX, -2.6, 0]))
            self.play(Write(rule), Create(rbox), FadeIn(note),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 3: geometry -> equation ---------------------------------------
    def beat3_equation(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()

            heading = board_text("Geometry to Equation", 25, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            d = diagram()
            e, f = d["e"], d["f"]
            w_a, w_b = d["w_a"], d["w_b"]
            lbl_a = attached_label(np.array([-2.35, 1.85, 0]),
                                   e + 0.55 * mid_dir(LEFT, down_dir()),
                                   "(3x+20)^\\circ", ANGLE_A_COLOR)
            lbl_b = attached_label(np.array([-1.6, -1.45, 0]),
                                   f + 0.55 * mid_dir(LEFT, up_dir()),
                                   "(5x-8)^\\circ", ANGLE_B_COLOR)

            self.play(Write(heading), FadeIn(d["lines"]), FadeIn(d["trans"]),
                      FadeIn(w_a.sector), FadeIn(w_b.sector),
                      FadeIn(lbl_a), FadeIn(lbl_b),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.4))
            self.play(Indicate(lbl_a.lbl, color=ANGLE_A_COLOR, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(Indicate(lbl_b.lbl, color=ANGLE_B_COLOR, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            rule = board_text("same-side interior  ->  add to 180", 17,
                              CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))
            self.play(FadeIn(rule), run_time=rt(
                tracker.time_until_bookmark("b2") * 0.6))

            eq = MathTex("(3x+20)", "+", "(5x-8)", r"\;=\;", "180", font_size=36)
            align_equals(eq, BOARD_CX, -2.0)
            eq_box = SurroundingRectangle(eq, color=ANGLE_A_COLOR, buff=0.2,
                                          corner_radius=0.1, stroke_width=3)
            self.play(TransformFromCopy(lbl_a.lbl, eq[0]), FadeIn(eq[1]),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.play(TransformFromCopy(lbl_b.lbl, eq[2]), FadeIn(eq[3]), FadeIn(eq[4]),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.play(Create(eq_box), Flash(eq, color=ANGLE_A_COLOR,
                                            flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.5))
            self.add_sound(self.sfx["success"], gain=-11)

            note = board_text("Every term has a geometric reason.", 17,
                              CHALK_WHITE).move_to(np.array([BOARD_CX, -2.55, 0]))
            self.play(FadeOut(rule), FadeIn(note),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.play(Indicate(eq, color=CHALK_WHITE, scale_factor=1.03),
                      run_time=rt(tracker.time_until_bookmark("b5")))
            self.add_sound(self.sfx["ding"], gain=-12)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 4: solve ------------------------------------------------------
    def beat4_solve(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()

            heading = board_text("Now Solve the Equation", 25, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            e1 = MathTex("(3x+20)+(5x-8)", r"\;=\;", "180", font_size=38)
            align_equals(e1, BOARD_CX, 1.45)
            self.play(Write(e1), run_time=rt(tracker.time_until_bookmark("b0") * 0.5))
            e2 = MathTex("3x+20+5x-8", r"\;=\;", "180", font_size=38)
            align_equals(e2, BOARD_CX, 1.45)
            self.play(TransformMatchingTex(e1, e2),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["click"], gain=-15)

            e3 = MathTex("8x+12", r"\;=\;", "180", font_size=38)
            align_equals(e3, BOARD_CX, 1.45)
            self.play(TransformMatchingTex(e2, e3),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["ding"], gain=-13)

            e4 = MathTex("8x", r"\;=\;", "168", font_size=38)
            align_equals(e4, BOARD_CX, 1.45)
            self.play(TransformMatchingTex(e3, e4),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            e5 = MathTex("x", r"\;=\;", r"\frac{168}{8}", font_size=38)
            align_equals(e5, BOARD_CX, 1.45)
            self.play(TransformMatchingTex(e4, e5),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            e6 = MathTex("x", r"\;=\;", "21", font_size=44, color=CHALK_GREEN)
            align_equals(e6, BOARD_CX, 1.45)
            self.play(TransformMatchingTex(e5, e6),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.6))

            ans = MathTex("x", "=", "21", font_size=48, color=CHALK_GREEN).move_to(
                np.array([BOARD_CX, 0.05, 0]))
            abox = SurroundingRectangle(ans, color=CHALK_GREEN, buff=0.22,
                                        corner_radius=0.1, stroke_width=3)
            note = board_text("the value of x — not an angle yet", 17,
                              CHALK_YELLOW, "BOLD").next_to(abox, DOWN, buff=0.18)
            self.play(FadeOut(e6), run_time=0.3)
            self.play(FadeIn(ans), Create(abox), FadeIn(note),
                      Flash(ans, color=CHALK_GREEN, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self.play(Indicate(VGroup(ans, abox), color=CHALK_GREEN, scale_factor=1.02),
                      run_time=rt(tracker.get_remaining_duration()))
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 5: return to the diagram --------------------------------------
    def beat5_return(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            self.reset_board()

            heading = board_text("Return to the Diagram", 25, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            d = diagram()
            e, f = d["e"], d["f"]
            w_a, w_b = d["w_a"], d["w_b"]
            self.play(Write(heading), FadeIn(d["lines"]), FadeIn(d["trans"]),
                      FadeIn(w_a.sector), FadeIn(w_b.sector),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.4))

            x_val = MathTex("x", "=", "21", font_size=34, color=CHALK_GREEN
                            ).move_to(np.array([3.4, 1.95, 0]))
            self.play(FadeIn(x_val), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.6))
            self.play(Indicate(w_a.sector, color=ANGLE_A_COLOR, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            calc_a = MathTex("3(21)+20", "=", "83^\\circ", font_size=28,
                             color=ANGLE_A_COLOR).move_to(
                np.array([-1.85, -1.7, 0]))
            self.play(Write(calc_a), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            calc_b = MathTex("5(21)-8", "=", "97^\\circ", font_size=28,
                             color=ANGLE_B_COLOR).move_to(
                np.array([2.55, -1.7, 0]))
            self.play(Write(calc_b), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            # the values replace the expressions on the arcs
            val_a = attached_label(np.array([-2.35, 1.85, 0]),
                                   e + 0.55 * mid_dir(LEFT, down_dir()),
                                   "83^\\circ", ANGLE_A_COLOR)
            val_b = attached_label(np.array([-1.35, -1.15, 0]),
                                   f + 0.55 * mid_dir(LEFT, up_dir()),
                                   "97^\\circ", ANGLE_B_COLOR)
            self.play(FadeIn(val_a), FadeIn(val_b),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.5))

            chk = MathTex("83^\\circ", "+", "97^\\circ", "=", "180^\\circ",
                          font_size=32, color=CHALK_GREEN).move_to(
                np.array([BOARD_CX, -2.5, 0]))
            ck = tick_beside(chk, CHALK_GREEN, 0.32, 0.3)
            self.play(Write(chk), run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            self.play(Create(ck), Flash(chk, color=CHALK_GREEN, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)

            note = board_text("x = 21, but the angles are 83 and 97 degrees.",
                              17, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -2.5, 0]))
            self.play(FadeOut(chk), FadeOut(ck), FadeIn(note),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["ding"], gain=-12)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 6: corresponding angles ---------------------------------------
    def beat6_corresponding(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("Corresponding Angles", 25, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            d = diagram()
            e, f = d["e"], d["f"]
            # the two matching-position angles: upper-right at each intersection
            w_e = angle_wedge(e, RIGHT, up_dir(), color=CHALK_GREEN, fill=0.35)
            w_f = angle_wedge(f, RIGHT, up_dir(), color=CHALK_GREEN, fill=0.35)
            lbl_e = attached_label(np.array([1.65, 2.25, 0]),
                                   e + 0.55 * mid_dir(RIGHT, up_dir()),
                                   "5x^\\circ", CHALK_GREEN)
            lbl_f = attached_label(np.array([2.25, 0.5, 0]),
                                   f + 0.55 * mid_dir(RIGHT, up_dir()),
                                   "(2x+24)^\\circ", CHALK_GREEN)

            self.play(Write(heading), FadeIn(d["lines"]), FadeIn(d["trans"]),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.5))
            self.play(FadeIn(w_e.sector), FadeIn(w_f.sector),
                      FadeIn(lbl_e), FadeIn(lbl_f),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(Indicate(w_e.sector, color=CHALK_GREEN, scale_factor=1.0),
                      Indicate(w_f.sector, color=CHALK_GREEN, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.6))
            same = board_text("matching positions", 16, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.38, 0]))
            self.play(FadeIn(same), run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            rule = board_text("parallel lines  \u2192  corresponding angles are equal",
                              17, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.70, 0]))
            self.play(FadeIn(rule), Flash(rule, color=CHALK_YELLOW, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            eq = MathTex("5x", r"\;=\;", "2x+24", font_size=38)
            align_equals(eq, BOARD_CX, -2.38)
            eq_box = SurroundingRectangle(eq, color=CHALK_GREEN, buff=0.18,
                                          corner_radius=0.1, stroke_width=3)
            self.play(FadeOut(same), run_time=rt(
                tracker.time_until_bookmark("b4") * 0.2))
            self.play(TransformFromCopy(lbl_e.lbl, eq[0]),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.4))
            self.play(TransformFromCopy(lbl_f.lbl, eq[2]), FadeIn(eq[1]),
                      Create(eq_box), Flash(eq, color=CHALK_GREEN, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 7: solve the corresponding case -------------------------------
    def beat7_solve_second(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("Same Algebra, New Rule", 25, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            e1 = MathTex("5x", r"\;=\;", "2x+24", font_size=38)
            align_equals(e1, BOARD_CX, 1.5)
            self.play(Write(e1), run_time=rt(tracker.time_until_bookmark("b0") * 0.6))
            e2 = MathTex("5x-2x", r"\;=\;", "24", font_size=38)
            align_equals(e2, BOARD_CX, 1.5)
            self.play(TransformMatchingTex(e1, e2),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["click"], gain=-15)

            e3 = MathTex("3x", r"\;=\;", "24", font_size=38)
            align_equals(e3, BOARD_CX, 1.5)
            self.play(TransformMatchingTex(e2, e3),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            e4 = MathTex("x", r"\;=\;", "8", font_size=44, color=CHALK_GREEN)
            align_equals(e4, BOARD_CX, 1.5)
            self.play(TransformMatchingTex(e3, e4),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.6))
            self.add_sound(self.sfx["ding"], gain=-13)

            a1 = MathTex("5(8)", "=", "40^\\circ", font_size=32, color=CHALK_GREEN
                         ).move_to(np.array([-1.7, 0.15, 0]))
            a2 = MathTex("2(8)+24", "=", "40^\\circ", font_size=32,
                         color=CHALK_GREEN).move_to(np.array([2.5, 0.15, 0]))
            t1 = tick_beside(a1, CHALK_GREEN, 0.3, 0.28)
            t2 = tick_beside(a2, CHALK_GREEN, 0.3, 0.28)
            self.play(Write(a1), Write(a2), run_time=rt(
                tracker.time_until_bookmark("b2") * 0.4))
            self.play(Create(t1), Create(t2), Flash(a1, color=CHALK_GREEN,
                                                    flash_radius=0.5),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            equal = MathTex("40^\\circ", r"\;=\;", "40^\\circ", font_size=38,
                            color=CHALK_GREEN).move_to(np.array([BOARD_CX, -0.85, 0]))
            ebox = SurroundingRectangle(equal, color=CHALK_GREEN, buff=0.18,
                                        corner_radius=0.1, stroke_width=3)
            self.play(FadeOut(e4), Write(equal), Create(ebox),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-12)

            note = board_text("Equal angles  ->  equal expressions.", 18,
                              CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.85, 0]))
            self.play(FadeIn(note), run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 8: the routine ------------------------------------------------
    def beat8_routine(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("The Routine for Angle Problems", 23,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.3))

            def card(n, title, sub, color, math: bool = False):
                box = RoundedRectangle(corner_radius=0.1, width=2.3, height=1.7,
                                       stroke_color=color, stroke_width=2,
                                       fill_color="#16202B", fill_opacity=0.9)
                num = board_text(str(n), 15, color, "BOLD").move_to(
                    box.get_top() + DOWN * 0.25)
                lbl = board_text(title, 14, CHALK_WHITE, "BOLD").move_to(
                    box.get_center() + UP * 0.16)
                # math cards MUST be MathTex: a card sub-line that holds LaTeX
                # but is handed to Text() renders the source literally
                sm = (MathTex(sub, font_size=19, color=color) if math
                      else board_text(sub, 12, color))
                sm.move_to(box.get_center() + DOWN * 0.3)
                return VGroup(box, num, lbl, sm)

            c1 = card(1, "IDENTIFY", "which angles?", CHALK_CYAN)
            c2 = card(2, "RELATE", r"A=B \;\text{or}\; A+B=180", ANGLE_B_COLOR,
                      math=True)
            c3 = card(3, "FORM", r"\text{one equation}", ANGLE_A_COLOR,
                      math=True)
            c4 = card(4, "SOLVE", r"\text{find } x", CHALK_YELLOW, math=True)
            cards = VGroup(c1, c2, c3, c4).arrange(RIGHT, buff=0.2).move_to(
                np.array([BOARD_CX, 0.55, 0]))
            cards.shift(RIGHT * (BOARD_CX - cards.get_center()[0]))

            marks = ["b0", "b1", "b2", "b3"]
            for c, m in zip(cards, marks):
                self.play(FadeIn(c, shift=DOWN * 0.12),
                          run_time=rt(tracker.time_until_bookmark(m)))
                self.add_sound(self.sfx["click"], gain=-15)

            strip = board_text("Identify \u2192 Relate \u2192 Form \u2192 Solve "
                               "\u2192 Interpret",
                               19, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.4, 0]))
            self.play(FadeIn(strip), Circumscribe(strip, color=CHALK_YELLOW,
                                                  stroke_width=3),
                      run_time=rt(tracker.time_until_bookmark("b4") * 0.6))
            self.play(Indicate(cards[0], color=CHALK_CYAN, scale_factor=1.05),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 9: student challenge -----------------------------------------
    def beat9_challenge(self) -> None:
        with self.voiceover(text=NARRATION["scene9_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", 30, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y - 0.05, 0]))
            problem = board_text("Two supplementary angles differ by 34 degrees.",
                                 19, CHALK_WHITE).move_to(
                np.array([BOARD_CX, 2.15, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0")))
            self.play(FadeIn(problem), run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            # a straight line with two supplementary sectors
            base = np.array([BOARD_CX, 0.9, 0])
            flat = Line(base + np.array([-2.4, 0, 0]), base + np.array([2.4, 0, 0]),
                        stroke_color=CHALK_WHITE, stroke_width=2.6)
            sec_a = Sector(radius=0.62, start_angle=0, angle=73 * DEGREES,
                           stroke_color=CHALK_CYAN, stroke_width=2.4,
                           fill_color=CHALK_CYAN, fill_opacity=0.3).shift(base)
            sec_b = Sector(radius=0.62, start_angle=73 * DEGREES,
                           angle=107 * DEGREES, stroke_color=CHALK_PINK,
                           stroke_width=2.4, fill_color=CHALK_PINK,
                           fill_opacity=0.3).shift(base)
            lbl_a = MathTex("x^\\circ", font_size=28, color=CHALK_CYAN).move_to(
                base + 0.9 * np.array([np.cos(36 * DEGREES),
                                       np.sin(36 * DEGREES), 0]))
            lbl_b = MathTex("(x+34)^\\circ", font_size=28, color=CHALK_PINK
                            ).move_to(base + 0.95 * np.array(
                                [np.cos(126 * DEGREES), np.sin(126 * DEGREES), 0]))
            self.play(Create(flat), FadeIn(sec_a), FadeIn(lbl_a),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.6))
            self.play(FadeIn(sec_b), FadeIn(lbl_b),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["pop"], gain=-13)

            ask = board_text("Let the smaller angle be x.", 17, CHALK_CYAN,
                             "BOLD").move_to(np.array([BOARD_CX, -0.35, 0]))
            pause = board_text("Pause and try it", 19, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.05, 0]))
            self.play(FadeIn(ask), run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            self.play(FadeIn(pause), run_time=rt(
                tracker.time_until_bookmark("b3") * 0.85))
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(Indicate(VGroup(sec_a, sec_b), color=CHALK_YELLOW,
                               scale_factor=1.03),
                      run_time=rt(tracker.get_remaining_duration() * 0.9))
            self.challenge = VGroup(heading, problem, flat, sec_a, sec_b, lbl_a,
                                    lbl_b, ask, pause)
            self._capture_srt(tracker)

        play_challenge_countdown(self, seconds=6, sfx=self.sfx)

        with self.voiceover(text=NARRATION["scene9_reveal"]) as tracker:
            sec_a, sec_b = self.challenge[3], self.challenge[4]
            self.play(FadeOut(self.challenge[8]), FadeOut(self.challenge[7]),
                      run_time=0.3)

            e1 = MathTex("x+(x+34)", r"\;=\;", "180", font_size=36)
            align_equals(e1, BOARD_CX, -0.4)
            self.play(Write(e1), run_time=rt(tracker.time_until_bookmark("b0") * 0.6))
            e2 = MathTex("2x+34", r"\;=\;", "180", font_size=36)
            align_equals(e2, BOARD_CX, -0.4)
            self.play(TransformMatchingTex(e1, e2),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["click"], gain=-15)

            e3 = MathTex("2x", r"\;=\;", "146", font_size=36)
            align_equals(e3, BOARD_CX, -0.4)
            self.play(TransformMatchingTex(e2, e3),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            e4 = MathTex("x", r"\;=\;", "73", font_size=40, color=CHALK_GREEN)
            align_equals(e4, BOARD_CX, -0.4)
            self.play(TransformMatchingTex(e3, e4),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["success"], gain=-11)

            val_a = MathTex("73^\\circ", font_size=28, color=CHALK_CYAN
                            ).move_to(self.challenge[5])
            val_b = MathTex("107^\\circ", font_size=28, color=CHALK_PINK
                            ).move_to(self.challenge[6])
            self.play(ReplacementTransform(self.challenge[5], val_a),
                      ReplacementTransform(self.challenge[6], val_b),
                      Flash(val_a, color=CHALK_CYAN, flash_radius=0.5),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-12)

            chk = MathTex("73^\\circ", "+", "107^\\circ", "=", "180^\\circ",
                          font_size=32, color=CHALK_GREEN).move_to(
                np.array([BOARD_CX, -1.25, 0]))
            ck = tick_beside(chk, CHALK_GREEN, 0.32, 0.3)
            well = board_text("Well done! Supplementary means 180 degrees.", 17,
                              CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -2.15, 0]))
            self.play(FadeOut(e4), Write(chk), Create(ck),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.play(FadeIn(well), Flash(chk, color=CHALK_GREEN, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.3))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Beat 10: summary ---------------------------------------------------
    def beat10_summary(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("Summary", 31, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, HEAD_Y - 0.05, 0]))
            self.play(Write(heading), run_time=rt(tracker.time_until_bookmark("b0") * 0.4))

            chain = MathTex(r"A=B \quad\text{or}\quad A+B=180^\circ", font_size=28,
                            color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, 2.35, 0]))
            self.play(Write(chain), run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            r1 = summary_row(1, "Corresponding angles:", r"A = B", CHALK_GREEN)
            r2 = summary_row(2, "Same-side interior angles:", r"A+B = 180^\circ",
                             ANGLE_B_COLOR)
            r3 = summary_row(3, "Replace with expressions:", r"ax+b,\; cx+d",
                             CHALK_CYAN)
            r4 = summary_row(4, "Return and check:", r"x=21 \to 83^\circ, 97^\circ",
                             CHALK_YELLOW)
            rows = VGroup(r1, r2, r3, r4).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            rows.move_to(np.array([BOARD_CX, 0.6, 0]))
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
            take = board_text("Geometry gives the rule.", 22, CHALK_YELLOW,
                              "BOLD").move_to(np.array([BOARD_CX, -1.45, 0]))
            take2 = board_text("Algebra finds x.", 22, CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX, -2.0, 0]))
            self.play(FadeIn(take), Flash(take, color=CHALK_YELLOW, flash_radius=0.9),
                      FadeIn(take2),
                      run_time=rt(tracker.time_until_bookmark("b5") * 0.3))
            self.add_sound(self.sfx["success"], gain=-11)

            summary = VGroup(heading, chain, rows, take, take2)
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

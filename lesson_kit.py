"""
Shared studio kit for TG Board conceptual lessons.

Holds only theme constants and pure construction helpers. Every lesson keeps its
own nine `self.voiceover(...)` beats, its own FadeOut stage-clearing, and its own
`run_time` fractions in the lesson file, because that is what
`validate_lessons.py` inspects.

Palette matches agent/manim/theme.py so new lessons sit alongside the existing
catalog.
"""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Arrow,
    Circle,
    Dot,
    Line,
    Polygon,
    RoundedRectangle,
    Square,
    Text,
    VGroup,
    config,
)

# ------------------------------------------------------------------ theme ---
BG = "#0F172A"
INK = "#F1F5F9"
MUTED = "#94A3B8"
ACCENT = "#38BDF8"
SUCCESS = "#34D399"
AMBER = "#FBBF24"
ROSE = "#FB7185"
VIOLET = "#C084FC"
PANEL = "#1E293B"
# Calibri — clean, modern, available on Windows 10/11.
FONT = "Calibri"

config.background_color = BG

# Frame is 14.222 x 8.0; keep 0.25 of edge margin (plan.md Section 21).
FRAME_W = 14.222
FRAME_H = 8.0
SAFE_W = FRAME_W - 0.5
SAFE_H = FRAME_H - 0.5

# Seconds the closing card stays on screen after narration ends, so the last
# line is still readable when the video stops (validate_lessons.py enforces it).
END_HOLD = 2.5


# ------------------------------------------------------------------- type ---
def txt(s: str, size: int = 32, color: str = INK, weight: str = "NORMAL") -> Text:
    """Prose. Never put prose in MathTex (plan.md Section 20)."""
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def heading(s: str, color: str = AMBER) -> Text:
    """Section heading pinned to the top edge. One per beat; fade it with the beat."""
    return txt(s, 34, color, "BOLD").to_edge(UP, buff=0.4)


def hook_line(s: str, color: str = SUCCESS) -> Text:
    return txt(s, 34, color, "BOLD")


def punch(s: str, color: str = SUCCESS) -> Text:
    """The one-line takeaway that lands the beat."""
    return txt(s, 34, color, "BOLD")


# ------------------------------------------------------------------ cards ---
def card(width: float, height: float, color: str = ACCENT) -> RoundedRectangle:
    return RoundedRectangle(
        corner_radius=0.18,
        width=width,
        height=height,
        fill_color=PANEL,
        fill_opacity=0.92,
        stroke_color=color,
        stroke_width=2,
    )


def given_panel(rows: list[str], *, title: str = "Given", width: float = 5.3,
                max_width: float = 6.6) -> VGroup:
    """Panel of given information only — never the answer (plan.md Section 16).

    Sizes itself to its longest row instead of trusting the caller's width,
    which let a long line spill out of the card; and never grows past
    `max_width`, since these panels sit in one column of a two-column beat and
    a wider card runs off the frame edge.
    """
    body = VGroup(txt(title, 26, AMBER, "BOLD"), *[txt(r, 25, INK) for r in rows])
    body.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    if body.width + 0.9 > max_width:
        body.scale((max_width - 0.9) / body.width)
    frame = card(min(max(width, body.width + 0.9), max_width),
                 body.height + 0.9, MUTED)
    body.move_to(frame.get_center())
    return VGroup(frame, body)


def idea_card(lines: list[Text], *, width: float = 9.6, height: float = 3.0,
              color: str = ACCENT) -> VGroup:
    frame = card(width, height, color)
    body = VGroup(*lines).arrange(DOWN, buff=0.4).move_to(frame.get_center())
    return VGroup(frame, body)


# ------------------------------------------------------------------ parts ---
def unit_squares(n: int, color: str, side: float = 0.42) -> VGroup:
    g = VGroup(*[
        Square(side_length=side, fill_color=color, fill_opacity=0.55,
               stroke_color=color, stroke_width=2)
        for _ in range(n)
    ])
    g.arrange(RIGHT, buff=0.14)
    return g


def right_triangle(a: float, b: float, color: str = ACCENT, *, unit: float = 0.42,
                   label_sides: bool = True, mark_right_angle: bool = True) -> VGroup:
    """A right triangle with legs `a` (up) and `b` (across), drawn to scale.

    Sides are drawn in the ratio the lesson names them, so a triangle captioned
    "3, 4, 5" is actually a 3-4-5 right triangle rather than a generic wedge.
    Returned group is ``(polygon, marker, labels)``; the right angle sits at the
    bottom-left so several triangles can share a baseline.
    """
    p0 = np.array([0.0, 0.0, 0.0])
    p1 = np.array([b * unit, 0.0, 0.0])
    p2 = np.array([0.0, a * unit, 0.0])
    poly = Polygon(p0, p1, p2, stroke_color=color, stroke_width=3,
                   fill_color=color, fill_opacity=0.22)

    marker = VGroup()
    if mark_right_angle:
        s = min(0.22, 0.35 * unit * min(a, b))
        marker.add(Line(p0 + RIGHT * s, p0 + RIGHT * s + UP * s,
                        stroke_color=color, stroke_width=2),
                   Line(p0 + UP * s, p0 + RIGHT * s + UP * s,
                        stroke_color=color, stroke_width=2))

    labels = VGroup()
    if label_sides:
        c = (a ** 2 + b ** 2) ** 0.5
        # Push the hypotenuse label along the outward normal, so it clears the
        # sloping side instead of landing on it as the triangle grows.
        normal = np.array([a, b, 0.0])
        normal = normal / np.linalg.norm(normal)
        mid = (p1 + p2) / 2
        hyp_lbl = txt(_num(c), 20, color)
        # Clear the sloping side by the label's own reach along that normal,
        # otherwise a longer number still lands on the line as the triangle grows.
        reach = (abs(normal[0]) * hyp_lbl.width + abs(normal[1]) * hyp_lbl.height) / 2
        hyp_lbl.move_to(mid + normal * (reach + 0.16))
        labels.add(
            txt(_num(b), 20, color).next_to(Line(p0, p1), DOWN, buff=0.18),
            txt(_num(a), 20, color).next_to(Line(p0, p2), LEFT, buff=0.18),
            hyp_lbl,
        )

    g = VGroup(poly, marker, labels)
    g.move_to(ORIGIN)
    return g


def rule_line(half_width: float = 5.0, color: str = MUTED, width: float = 2) -> Line:
    return Line(LEFT * half_width, RIGHT * half_width,
                stroke_color=color, stroke_width=width)


# ------------------------------------------------------------------- axes ---
def axes2d(
    *,
    x_max: float,
    y_max: float,
    x_ticks: tuple[float, ...] = (),
    y_ticks: tuple[float, ...] = (),
    width: float = 6.0,
    height: float = 3.6,
    x_label: str = "",
    y_label: str = "",
    tick_font: int = 18,
) -> VGroup:
    """Arrowed axes carrying real tick values, built in data units.

    A graph a student cannot read numbers off is only a picture of a graph, so
    both axes get an arrowhead, ticks at the given data values, and a unit
    label. Data is placed with :func:`plot_xy`, which reuses the same scale.

    Returned group is ``(x_axis, y_axis, x_label, y_label, ticks)`` and carries
    ``.sx`` / ``.sy`` so callers never re-derive the scale by hand.
    """
    sx = width / x_max
    sy = height / y_max

    x = Arrow(ORIGIN, RIGHT * (width + 0.4), buff=0, color=MUTED,
              stroke_width=4, max_tip_length_to_length_ratio=0.055,
              max_stroke_width_to_length_ratio=12)
    y = Arrow(ORIGIN, UP * (height + 0.4), buff=0, color=MUTED,
              stroke_width=4, max_tip_length_to_length_ratio=0.055,
              max_stroke_width_to_length_ratio=12)

    ticks = VGroup()
    for v in x_ticks:
        px = v * sx
        mark = Line(RIGHT * px + DOWN * 0.09, RIGHT * px + UP * 0.09,
                    stroke_color=MUTED, stroke_width=3)
        ticks.add(mark, txt(_num(v), tick_font, MUTED).next_to(mark, DOWN, buff=0.14))
    for v in y_ticks:
        py = v * sy
        mark = Line(UP * py + LEFT * 0.09, UP * py + RIGHT * 0.09,
                    stroke_color=MUTED, stroke_width=3)
        ticks.add(mark, txt(_num(v), tick_font, MUTED).next_to(mark, LEFT, buff=0.14))

    xl = txt(x_label, 22, MUTED).next_to(x, DOWN, buff=0.58) if x_label else VGroup()
    yl = VGroup()
    if y_label:
        yl = txt(y_label, 22, MUTED).rotate(np.pi / 2)
        # Clear the widest tick label rather than the bare axis line.
        left = min([t.get_left()[0] for t in ticks] or [0.0])
        yl.next_to(y, LEFT, buff=0.0).set_x(left - 0.42, direction=RIGHT)

    # Invisible anchors at the data origin and at one unit-span along each
    # axis. They are part of the group, so they follow any later scale() or
    # shift() and let plot_xy/at_xy stay correct after the group is moved —
    # a stored scale factor would go stale the moment a caller resizes it.
    anchors = VGroup(
        Dot(ORIGIN, radius=0.001),
        Dot(RIGHT * width, radius=0.001),
        Dot(UP * height, radius=0.001),
    ).set_opacity(0)

    g = VGroup(x, y, xl, yl, ticks, anchors)
    g.x_max, g.y_max = x_max, y_max
    g.sx, g.sy = sx, sy
    return g


def _num(v: float) -> str:
    return str(int(v)) if float(v).is_integer() else str(v)


def at_xy(ax: VGroup, x: float, y: float):
    """The scene point for one data coordinate on an :func:`axes2d` grid.

    Reads the axes' current anchors, so it stays right after scale()/shift().
    """
    anchors = ax[5]
    origin = anchors[0].get_center()
    span_x = anchors[1].get_center() - origin
    span_y = anchors[2].get_center() - origin
    return origin + span_x * (x / ax.x_max) + span_y * (y / ax.y_max)


def plot_xy(ax: VGroup, pts, color: str = SUCCESS, radius: float = 0.075) -> VGroup:
    """Dots at data coordinates on an :func:`axes2d` grid."""
    return VGroup(*[
        Dot(at_xy(ax, px, py), color=color, radius=radius) for px, py in pts
    ])


def label_row(label: str, body, *, buff: float = 0.5, size: int = 25) -> VGroup:
    return VGroup(txt(label, size, MUTED), body).arrange(RIGHT, buff=buff)


def table_rows(labels: list[str], rows: list[list], *, col_buff: float = 1.4,
               row_buff: float = 0.7, label_x: float = -5.0,
               body_x: float = 0.9) -> VGroup:
    """Left-labelled rows of equal-width columns, arranged as one block."""
    out = VGroup()
    for label, row in zip(labels, rows):
        cells = VGroup(*row).arrange(RIGHT, buff=col_buff).move_to(RIGHT * body_x)
        lbl = txt(label, 25, MUTED).move_to(RIGHT * label_x)
        out.add(VGroup(lbl, cells))
    out.arrange(DOWN, buff=row_buff, aligned_edge=LEFT)
    return out


def overview_panel(items: list[str], *, title: str = "Key Takeaways",
                    color: str = SUCCESS, width: float = 10.6) -> VGroup:
    """Numbered recap card — the closing "overview" beat.

    Distinct from :func:`punch` (one punchy takeaway line): this lists
    every key point from the lesson as a numbered checklist inside a
    bordered card, for a beat that recaps rather than lands a single idea.
    """
    head = txt(title, 30, AMBER, "BOLD")

    rows = VGroup()
    for i, item in enumerate(items, 1):
        badge = Circle(radius=0.22, stroke_color=color, stroke_width=2,
                        fill_color=color, fill_opacity=0.15)
        num = txt(str(i), 18, color, "BOLD").move_to(badge.get_center())
        row_txt = txt(item, 24, INK)
        row = VGroup(VGroup(badge, num), row_txt).arrange(RIGHT, buff=0.35)
        rows.add(row)
    rows.arrange(DOWN, buff=0.35, aligned_edge=LEFT)

    if rows.width + 1.0 > width:
        rows.scale((width - 1.0) / rows.width)

    body = VGroup(head, rows).arrange(DOWN, buff=0.5)
    frame = card(max(width, body.width + 1.0), body.height + 1.0, AMBER)
    body.move_to(frame.get_center())
    return VGroup(frame, body)


def fits(mob, max_width: float = SAFE_W) -> bool:
    """Measured width check — plan.md Section 21 says measure, do not guess."""
    return mob.width <= max_width


# --------------------------------------------------------------- backdrop ---
def blueprint_grid(spacing: float = 1.0, color: str = ACCENT,
                    opacity: float = 0.07) -> VGroup:
    """Faint full-frame graph-paper grid — a technical-drafting backdrop
    for construction/diagram-heavy lessons. Static (no animation needed);
    add it once at the start of a scene with `self.add(...)`.
    """
    lines = VGroup()
    x = -FRAME_W / 2
    while x <= FRAME_W / 2 + 1e-6:
        lines.add(Line(np.array([x, -FRAME_H / 2, 0]), np.array([x, FRAME_H / 2, 0]),
                        stroke_color=color, stroke_width=1, stroke_opacity=opacity))
        x += spacing
    y = -FRAME_H / 2
    while y <= FRAME_H / 2 + 1e-6:
        lines.add(Line(np.array([-FRAME_W / 2, y, 0]), np.array([FRAME_W / 2, y, 0]),
                        stroke_color=color, stroke_width=1, stroke_opacity=opacity))
        y += spacing
    return lines

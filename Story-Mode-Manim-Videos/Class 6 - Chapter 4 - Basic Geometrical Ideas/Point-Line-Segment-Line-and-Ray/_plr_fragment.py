"""Board furniture and narration for Storyboard 01 -- Point, Line Segment, Line
& Ray, Class 6 Mathematics, Chapter 4 (Basic Geometrical Ideas).

This file is *spliced*, never imported: assemble_point_line_ray.py grafts it into
the proven video-03 head of the Chapter 3 quadrilaterals set, so the theme names
(CHALK_*, FONT, BOARD_*), `board_text`, `chalk_math`, `appear` and the pacing
helpers (`rt`, `quick`, `leftover`) are already defined above it.

The furniture is this video's "build one object at a time" kit:

  * `dot_point`   -- one labelled point (a chalk dot plus its capital letter),
  * `straight`    -- a plain straight chalk line between two x positions,
  * `ray_line`    -- a straight line with a single arrowhead (a ray),
  * `both_way_line` -- a straight line with arrowheads at both ends (a line),
  * `end_tick`    -- the short cross-stroke that marks an endpoint,
  * `ruler`       -- the measuring ruler that belongs to the segment only,
  * `chip`        -- a small labelled chip ("2 ENDPOINTS"),
  * `card`        -- a titled card (the naming rules, the middle column),
  * `pictogram`   -- a self-contained mini diagram of one linear object,
  * `object_icon` -- a tiny chalk drawing of an everyday object (book, screen,
                     rangoli, star) for the opening scene,
  * `torch_icon`  -- the torch whose light becomes the ray.

The file has two splice markers, a board-layout section (constants plus the
furniture helpers) and the narration table; assemble_point_line_ray.py cuts
between them.
"""
from __future__ import annotations

import numpy as np

from manim import (
    Arrow, Circle, Dot, DoubleArrow, DOWN, LEFT, Line, MathTex,
    RoundedRectangle, UP, VGroup,
)

# ------------------------------------------------------------ board layout --
# (this section is spliced into a head whose own imports omit ArcBetweenPoints,
#  Brace and Ellipse)
from manim import ArcBetweenPoints, Brace, Ellipse  # noqa: E402,F401

# Board layout shared by every scene of this video.
ROW_Y = 2.72             # every scene heading sits on this line
SUB_Y = 2.16             # the one-line sub-heading under it
BANNER_Y = -1.15         # the closing banner, above the strip
# The burned-in caption grows up from the bottom of the frame: a one-line cue
# starts at y = -3.38 and a wrapped two-line cue reaches y = -2.93 (measured on
# the burned 360p cuts), so every closing strip sits at -1.80 and nothing at all
# sits below CAPTION_SAFE_Y = -2.00 -- audited by the IN-CAPTION-BAND check.
STRIP_Y = -1.80
CAPTION_SAFE_Y = -2.00

PANEL_FILL = "#16202B"
LINE_W = 3.6             # chalk stroke width for the geometry itself
TICK_HALF = 0.17         # half-length of an endpoint tick
DOT_R = 0.072            # radius of a chalk point
MARK_SIZE = 18           # ONE size for every point letter in the video
LABEL_DY = 0.34          # ONE offset: every letter sits this far below its dot
                         # (A, B, C / O / P, Q / R / S, T all use it, so the
                         # naming looks the same in every scene and no letter
                         # ever lands on a line, a dot or another label)


# ---------------------------------------------------------------- furniture --
def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


def row_centres(half_widths, gap, cx=BOARD_CX):
    """x centres for a row of figures whose ink is `gap` apart.

    The row's combined ink is centred on `cx` (the green board's centre line)
    and the figures of a row are not all equally wide, so equal centre spacing
    is NOT equal spacing on the board: this returns the centres that leave
    exactly `gap` units of clear air between neighbours.
    """
    total = 2.0 * sum(half_widths) + gap * (len(half_widths) - 1)
    x = cx - total / 2.0
    centres = []
    for half in half_widths:
        centres.append(x + half)
        x += 2.0 * half + gap
    return tuple(centres)


def straight(x1, x2, y, color=CHALK_WHITE, width=LINE_W):
    """A plain straight chalk line between two x positions."""
    return Line(np.array([x1, y, 0.0]), np.array([x2, y, 0.0]),
                stroke_color=color, stroke_width=width)


def ray_line(x1, x2, y, color=CHALK_WHITE, width=LINE_W, tip=0.26):
    """A ray: a straight line with one arrowhead at (x2, y)."""
    return Arrow(np.array([x1, y, 0.0]), np.array([x2, y, 0.0]), buff=0.0,
                 color=color, stroke_color=color, stroke_width=width,
                 tip_length=tip, max_tip_length_to_length_ratio=0.30)


def both_way_line(x1, x2, y, color=CHALK_WHITE, width=LINE_W, tip=0.24):
    """A line: a straight line with an arrowhead at each end."""
    return DoubleArrow(np.array([x1, y, 0.0]), np.array([x2, y, 0.0]), buff=0.0,
                       color=color, stroke_color=color, stroke_width=width,
                       tip_length=tip, max_tip_length_to_length_ratio=0.30)


def end_tick(x, y, color=CHALK_AMBER, half=TICK_HALF, width=3.0):
    """The short cross-stroke that marks an endpoint (or a definite length)."""
    return Line(np.array([x, y - half, 0.0]), np.array([x, y + half, 0.0]),
                stroke_color=color, stroke_width=width)


def dot_point(name=None, x=0.0, y=0.0, color=CHALK_CYAN, size=MARK_SIZE,
              label_dy=LABEL_DY, r=DOT_R):
    """One chalk point with its capital-letter name under it."""
    dot = Dot(radius=r, color=color, fill_opacity=1.0)
    dot.move_to(np.array([float(x), float(y), 0.0]))
    grp = VGroup(dot)
    if name:
        lab = board_text(name, size, color, "BOLD")
        lab.move_to(np.array([float(x), float(y) - label_dy, 0.0]))
        grp.add(lab)
        grp.label = lab
    grp.dot = dot
    return grp


def pair_dots(x1, x2, y, names=("A", "B"), color=CHALK_CYAN, size=MARK_SIZE,
              label_dy=LABEL_DY):
    """Two labelled points on one horizontal line."""
    return VGroup(dot_point(names[0], x1, y, color, size=size,
                            label_dy=label_dy),
                  dot_point(names[1], x2, y, color, size=size,
                            label_dy=label_dy))


def chip(text, color=CHALK_CYAN, size=15, width=None, height=0.50):
    """A small labelled chip."""
    lab = board_text(text, size, color, "BOLD")
    box = RoundedRectangle(corner_radius=0.09,
                           width=width or (lab.width + 0.40), height=height,
                           stroke_color=color, stroke_width=1.7,
                           fill_color=PANEL_FILL, fill_opacity=0.7)
    lab.move_to(box.get_center())
    return VGroup(box, lab)


def card(title, lines, color=CHALK_WHITE, width=3.9, height=1.30,
         title_size=19, line_size=15):
    """A rounded card with a heading and one or two body lines."""
    head = board_text(title, title_size, color, "BOLD")
    body = VGroup(*[board_text(line, line_size, CHALK_WHITE, "BOLD")
                    for line in lines]).arrange(DOWN, buff=0.22)
    box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                           stroke_color=color, stroke_width=2.0,
                           fill_color=PANEL_FILL, fill_opacity=0.55)
    head.move_to(box.get_center() + UP * (height / 2 - 0.24))
    body.move_to(box.get_center() - DOWN * (0.20 if len(lines) > 1 else 0.14))
    return VGroup(box, head, body)


def ruler(length=3.40, height=0.30, color=CHALK_AMBER, ticks=8):
    """The measuring ruler, drawn only where a length is definite."""
    box = RoundedRectangle(corner_radius=0.04, width=length, height=height,
                           stroke_color=color, stroke_width=1.6,
                           fill_color=PANEL_FILL, fill_opacity=0.55)
    marks = VGroup()
    for i in range(ticks + 1):
        x = -length / 2 + length * i / ticks
        drop = 0.15 if i % 2 else 0.10
        marks.add(Line(np.array([x, height / 2, 0.0]),
                       np.array([x, height / 2 - drop, 0.0]),
                       stroke_color=color, stroke_width=1.2))
    return VGroup(box, marks)


def curve_path(x1, x2, y, angle=1.0, color=CHALK_WHITE, width=2.0):
    """One curved route between two points (the paths that are not straight)."""
    return ArcBetweenPoints(np.array([x1, y, 0.0]), np.array([x2, y, 0.0]),
                            angle=angle, stroke_color=color,
                            stroke_width=width)


def torch_icon(color=CHALK_AMBER, scale=1.0):
    """A real torch, lying on its side and pointing right.

    Built from Manim primitives, not a bare rectangle: a tapered barrel with a
    highlight stripe and three grip rings, a switch, a flaring head, and a
    bright lens disc inside a two-step glow.  The barrel's mouth (the lens) is
    where the light -- and therefore the ray -- comes out; `place_torch` pins
    the icon by that lens, and `light_cone` draws the beam itself.
    """
    barrel = Polygon(np.array([-1.02, -0.16, 0.0]),
                     np.array([-0.34, -0.20, 0.0]),
                     np.array([-0.34, 0.20, 0.0]),
                     np.array([-1.02, 0.16, 0.0]),
                     stroke_color=color, stroke_width=1.8,
                     fill_color=color, fill_opacity=0.22)
    shine = Polygon(np.array([-0.98, 0.04, 0.0]),
                    np.array([-0.40, 0.07, 0.0]),
                    np.array([-0.40, 0.13, 0.0]),
                    np.array([-0.98, 0.10, 0.0]),
                    stroke_width=0, fill_color=CHALK_WHITE,
                    fill_opacity=0.22)
    grip = VGroup(*[Line(np.array([x, -0.175, 0.0]),
                         np.array([x, 0.175, 0.0]),
                         stroke_color=color, stroke_width=1.1,
                         stroke_opacity=0.85)
                    for x in (-0.94, -0.82, -0.70)])
    head = Polygon(np.array([-0.36, -0.21, 0.0]),
                   np.array([-0.10, -0.31, 0.0]),
                   np.array([-0.10, 0.31, 0.0]),
                   np.array([-0.36, 0.21, 0.0]),
                   stroke_color=CHALK_YELLOW, stroke_width=1.8,
                   fill_color=CHALK_YELLOW, fill_opacity=0.45)
    switch = Dot(radius=0.030, color=CHALK_PINK, fill_opacity=1.0)
    switch.move_to(np.array([-0.86, -0.07, 0.0]))
    glow = VGroup(*[Circle(radius=r, stroke_width=0,
                           fill_color=CHALK_YELLOW, fill_opacity=op)
                    for r, op in ((0.30, 0.10), (0.21, 0.18))])
    for g in glow:
        g.move_to(np.array([-0.06, 0.0, 0.0]))
    lens = Circle(radius=0.115, stroke_color=CHALK_YELLOW, stroke_width=1.5,
                  fill_color=CHALK_WHITE, fill_opacity=0.95)
    lens.move_to(np.array([-0.06, 0.0, 0.0]))
    grp = VGroup(barrel, shine, grip, head, switch, glow, lens).scale(scale)
    grp.lens = lens
    return grp


def place_torch(torch, lens_x, lens_y):
    """Pin a torch so that its lens sits exactly on (lens_x, lens_y)."""
    c = torch.lens.get_center()
    return torch.shift(np.array([float(lens_x) - c[0], float(lens_y) - c[1],
                                 0.0]))


def light_cone(x0, x1, y, half0=0.11, half1=0.62, color=CHALK_YELLOW,
               opacity=0.15):
    """The beam the ray travels in: a translucent cone widening from the lens."""
    return Polygon(np.array([x0, y - half0, 0.0]),
                   np.array([x0, y + half0, 0.0]),
                   np.array([x1, y + half1, 0.0]),
                   np.array([x1, y - half1, 0.0]),
                   stroke_width=0, fill_color=color, fill_opacity=opacity)


def object_icon(kind, color=CHALK_CYAN, size=0.62):
    """A small chalk drawing of one everyday object, centred on the origin.

    Each one is built from filled, shaded primitives so it reads as the real
    thing and not as an outline: a closed book (cream page block, shaded cover,
    spine, ruled lines, ribbon), a screen (dark bezel, lit glass with a sheen,
    trapezoid stand and base), a rangoli (shaded disc, a ring of eight petals,
    two rings and a petalled centre) and a five-pointed star with a halo.
    """
    s = float(size)
    if kind == "book":
        pages = RoundedRectangle(corner_radius=0.03, width=s * 0.72,
                                 height=s * 0.92, stroke_color=CHALK_WHITE,
                                 stroke_width=1.1, fill_color=CHALK_WHITE,
                                 fill_opacity=0.88)
        pages.shift(RIGHT * s * 0.07)
        cover = RoundedRectangle(corner_radius=0.04, width=s * 0.70,
                                 height=s * 0.98, stroke_color=color,
                                 stroke_width=1.9, fill_color=color,
                                 fill_opacity=0.30)
        cover.shift(LEFT * s * 0.05)
        spine = RoundedRectangle(corner_radius=0.02, width=s * 0.14,
                                 height=s * 0.98, stroke_color=color,
                                 stroke_width=1.3, fill_color=color,
                                 fill_opacity=0.80)
        spine.align_to(cover, LEFT).shift(RIGHT * s * 0.07)
        rules = VGroup(*[
            Line(np.array([-s * 0.10, s * (0.26 - 0.17 * k), 0.0]),
                 np.array([s * 0.27, s * (0.26 - 0.17 * k), 0.0]),
                 stroke_color=CHALK_WHITE, stroke_width=1.3,
                 stroke_opacity=0.85) for k in range(3)])
        ribbon = Polygon(np.array([s * 0.16, s * 0.49, 0.0]),
                         np.array([s * 0.25, s * 0.49, 0.0]),
                         np.array([s * 0.25, s * 0.30, 0.0]),
                         np.array([s * 0.205, s * 0.36, 0.0]),
                         np.array([s * 0.16, s * 0.30, 0.0]),
                         stroke_width=0, fill_color=CHALK_PINK,
                         fill_opacity=0.85)
        return VGroup(pages, cover, spine, rules, ribbon)
    if kind == "screen":
        bezel = RoundedRectangle(corner_radius=0.06, width=s * 1.34,
                                 height=s * 0.92, stroke_color=color,
                                 stroke_width=2.2, fill_color=BLACK,
                                 fill_opacity=0.55)
        bezel.shift(UP * s * 0.12)
        glass = RoundedRectangle(corner_radius=0.04, width=s * 1.16,
                                 height=s * 0.74, stroke_color=color,
                                 stroke_width=1.0, fill_color=CHALK_CYAN,
                                 fill_opacity=0.30)
        glass.move_to(bezel.get_center())
        lit = RoundedRectangle(corner_radius=0.04, width=s * 0.86,
                               height=s * 0.50, stroke_width=0,
                               fill_color=CHALK_CYAN, fill_opacity=0.45)
        lit.move_to(bezel.get_center())
        sheen = Polygon(bezel.get_center() + np.array([-s * 0.56, s * 0.34, 0]),
                        bezel.get_center() + np.array([-s * 0.20, s * 0.34, 0]),
                        bezel.get_center() + np.array([-s * 0.48, -s * 0.34, 0]),
                        bezel.get_center() + np.array([-s * 0.58, -s * 0.34, 0]),
                        stroke_width=0, fill_color=CHALK_WHITE,
                        fill_opacity=0.14)
        neck = Polygon(bezel.get_bottom() + np.array([-s * 0.14, 0.0, 0]),
                       bezel.get_bottom() + np.array([s * 0.14, 0.0, 0]),
                       bezel.get_bottom() + np.array([s * 0.20, -s * 0.14, 0]),
                       bezel.get_bottom() + np.array([-s * 0.20, -s * 0.14, 0]),
                       stroke_color=color, stroke_width=1.4,
                       fill_color=color, fill_opacity=0.30)
        base = RoundedRectangle(corner_radius=0.03, width=s * 0.72,
                                height=s * 0.10, stroke_color=color,
                                stroke_width=1.4, fill_color=color,
                                fill_opacity=0.55)
        base.next_to(neck, DOWN, buff=0.0)
        led = Dot(radius=s * 0.035, color=CHALK_GREEN, fill_opacity=1.0)
        led.move_to(bezel.get_corner(DL) + np.array([s * 0.11, s * 0.08, 0]))
        return VGroup(bezel, glass, lit, sheen, neck, base, led)
    if kind == "rangoli":
        disc = Circle(radius=s * 0.58, stroke_color=color, stroke_width=1.7,
                      fill_color=CHALK_PINK, fill_opacity=0.14)
        petals = VGroup()
        for k in range(8):
            ang = TAU * k / 8.0
            petal = Ellipse(width=s * 0.24, height=s * 0.40,
                            stroke_color=color, stroke_width=1.1,
                            fill_color=(CHALK_PINK if k % 2 else CHALK_YELLOW),
                            fill_opacity=0.45)
            petal.move_to(np.array([np.cos(ang) * s * 0.30,
                                    np.sin(ang) * s * 0.30, 0.0]))
            petal.rotate(ang - PI / 2.0)
            petals.add(petal)
        rings = VGroup(Circle(radius=s * 0.46, stroke_color=CHALK_YELLOW,
                              stroke_width=1.2),
                       Circle(radius=s * 0.18, stroke_color=color,
                              stroke_width=1.2))
        core = Dot(radius=s * 0.075, color=CHALK_YELLOW, fill_opacity=1.0)
        dots = VGroup(*[Dot(radius=s * 0.030, color=CHALK_WHITE,
                            fill_opacity=0.9).move_to(
                                np.array([np.cos(TAU * (k + 0.5) / 8.0) * s * 0.41,
                                          np.sin(TAU * (k + 0.5) / 8.0) * s * 0.41,
                                          0.0])) for k in range(8)])
        return VGroup(disc, petals, rings, dots, core)
    if kind == "star":
        pts, halo_pts = [], []
        for k in range(10):
            ang = PI / 2.0 + k * PI / 5.0
            r = s * 0.60 if k % 2 == 0 else s * 0.24
            pts.append(np.array([np.cos(ang) * r, np.sin(ang) * r, 0.0]))
            halo_pts.append(np.array([np.cos(ang) * r * 1.22,
                                      np.sin(ang) * r * 1.22, 0.0]))
        halo = Polygon(*halo_pts, stroke_width=0, fill_color=CHALK_YELLOW,
                       fill_opacity=0.12)
        star = Polygon(*pts, stroke_color=CHALK_YELLOW, stroke_width=1.7,
                       fill_color=CHALK_YELLOW, fill_opacity=0.38)
        inner = Polygon(*[p * 0.52 for p in pts], stroke_width=0,
                        fill_color=CHALK_WHITE, fill_opacity=0.20)
        sparks = VGroup(*[
            Line(np.array([np.cos(a) * s * 0.72, np.sin(a) * s * 0.72, 0.0]),
                 np.array([np.cos(a) * s * 0.88, np.sin(a) * s * 0.88, 0.0]),
                 stroke_color=CHALK_YELLOW, stroke_width=1.3,
                 stroke_opacity=0.8)
            for a in (PI / 4.0, 3 * PI / 4.0, 5 * PI / 4.0, 7 * PI / 4.0)])
        return VGroup(halo, star, inner, sparks)
    raise ValueError(f"unknown object icon: {kind!r}")


def pictogram(kind, width=2.20, color=CHALK_WHITE, names=(), label_size=MARK_SIZE,
              label_dy=LABEL_DY, marks=True, dot_color=CHALK_CYAN):
    """A small self-contained diagram of one linear object, centred on the
    origin so `at()` can place it exactly.

    `kind` is "point" / "segment" / "ray" / "line"; `names` are the capital
    letters drawn under the dots (P, Q for a segment, R for a ray, S and T for
    the two points inside a line).
    """
    half = float(width) / 2.0
    parts: list = []
    if kind == "point":
        parts.append(Dot(radius=DOT_R, color=dot_color, fill_opacity=1.0))
    elif kind == "segment":
        parts.append(straight(-half, half, 0.0, color))
        parts.append(Dot(radius=DOT_R, color=dot_color, fill_opacity=1.0)
                     .move_to(np.array([-half, 0.0, 0.0])))
        parts.append(Dot(radius=DOT_R, color=dot_color, fill_opacity=1.0)
                     .move_to(np.array([half, 0.0, 0.0])))
        if marks:
            parts.append(end_tick(-half, 0.0, half=TICK_HALF * 0.9))
            parts.append(end_tick(half, 0.0, half=TICK_HALF * 0.9))
    elif kind == "ray":
        parts.append(Arrow(np.array([-half, 0.0, 0.0]),
                           np.array([half, 0.0, 0.0]), buff=0.0, color=color,
                           stroke_color=color, stroke_width=LINE_W,
                           tip_length=0.22,
                           max_tip_length_to_length_ratio=0.30))
        parts.append(Dot(radius=DOT_R, color=dot_color, fill_opacity=1.0)
                     .move_to(np.array([-half, 0.0, 0.0])))
        if marks:
            parts.append(end_tick(-half, 0.0, half=TICK_HALF * 0.9))
    elif kind == "line":
        parts.append(DoubleArrow(np.array([-half, 0.0, 0.0]),
                                 np.array([half, 0.0, 0.0]), buff=0.0,
                                 color=color, stroke_color=color,
                                 stroke_width=LINE_W, tip_length=0.20,
                                 max_tip_length_to_length_ratio=0.30))
        if names:
            for name, x in zip(names, (-half * 0.55, half * 0.55)):
                parts.append(Dot(radius=DOT_R, color=dot_color,
                                 fill_opacity=1.0)
                             .move_to(np.array([x, 0.0, 0.0])))
    else:
        raise ValueError(f"unknown pictogram: {kind!r}")

    grp = VGroup(*parts)
    if names:
        xs = {"point": [0.0],
              "segment": [-half, half],
              "ray": [-half, 0.0],
              "line": [-half * 0.55, half * 0.55]}[kind]
        for x, name in zip(xs, names):
            lab = board_text(name, label_size, color, "BOLD")
            lab.move_to(np.array([x, -label_dy, 0.0]))
            grp.add(lab)
    return grp


def place_line(pict, x, y):
    """Pin a pictogram so that its own straight drawing sits exactly on (x, y).

    The capital letters under the dots are part of the group, so centring the
    group would push the drawing off its row; this keeps the *drawing* -- not
    the bounding box -- on the row, which is what makes two pictograms line up.
    """
    centre = pict.get_center()
    pict.shift(np.array([float(x) - centre[0], float(y) - centre[1], 0.0]))
    return pict


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "Geometry begins with the simplest things: <bookmark mark='b0'/>a point, a "
        "line segment, a line, and a ray. <bookmark mark='b1'/>Let us build all "
        "four of them from one point, one step at a time."
    ),
    "s1": (
        "Geometry is all around us: the straight edge of a book, the frame of a "
        "television screen, the lines of a rangoli, the shape of a building. "
        "<bookmark mark='b0'/>But every one of those shapes is built from simpler "
        "ideas. <bookmark mark='b1'/>A rectangle is made of straight pieces, a "
        "rangoli is made of lines and points, and a star in the sky is simply a "
        "point very far away. <bookmark mark='b2'/>So what is the simplest thing we "
        "can draw in geometry?"
    ),
    "s2": (
        "Start with a point. <bookmark mark='b0'/>A pencil pressed on paper leaves a "
        "dot. Sharpen the pencil and the dot becomes smaller; sharpen it again and "
        "again, and the dot becomes smaller and smaller. <bookmark mark='b1'/>In "
        "geometry we keep the idea and not the ink: a point marks a location, and it "
        "has no size at all. <bookmark mark='b2'/>We name a point with a capital "
        "letter, like A, or B, or C."
    ),
    "s3": (
        "Now add a second point, B. <bookmark mark='b0'/>Join A to B. Many curved "
        "paths are possible, but only one of them is straight, and that straight "
        "path is the shortest. <bookmark mark='b1'/>This is a line segment. It has "
        "two endpoints, A and B, and it has a definite length, so a ruler can "
        "measure it. <bookmark mark='b2'/>We write it as segment AB."
    ),
    "s4": (
        "Now extend the segment beyond A and beyond B, without stopping. <bookmark "
        "mark='b0'/>It goes on and on in both directions, so we draw arrowheads at "
        "both ends. <bookmark mark='b1'/>A and B are not endpoints any more; they "
        "are simply points lying on the line. <bookmark mark='b2'/>So a line has no "
        "endpoints at all, and we may also name it with a small letter, like l."
    ),
    "s5": (
        "A torch gives us the next idea. <bookmark mark='b0'/>Its light starts at "
        "one point and spreads in one direction, and it never stops. <bookmark "
        "mark='b1'/>In geometry that is a ray: it has exactly one endpoint, called "
        "the initial point, and it goes on endlessly in one direction. <bookmark "
        "mark='b2'/>We write it as ray AB, and the rays of the sun and the rays of a "
        "light are everyday examples."
    ),
    "s6": (
        "How do we tell these three apart? <bookmark mark='b0'/>Count the endpoints. "
        "A line segment has two. <bookmark mark='b1'/>A ray has one. <bookmark "
        "mark='b2'/>A line has none. <bookmark mark='b3'/>And remember: only the "
        "line segment has a definite length, because the ray and the line go on "
        "forever."
    ),
    "s7": (
        "Now put three points on one straight line: C, A and B. <bookmark "
        "mark='b0'/>A lies between C and B, and all three points lie on the same "
        "line. <bookmark mark='b1'/>From A we can draw a ray towards B, and another "
        "ray towards C. <bookmark mark='b2'/>Both rays start at A, and they travel "
        "in opposite directions."
    ),
    "s8": (
        "There is one more rule about naming a ray. <bookmark mark='b0'/>Look at ray "
        "OA: it starts at O and it passes through A and B. <bookmark mark='b1'/>Ray "
        "OB starts at the same point and travels in the same direction, so ray OA "
        "and ray OB are the same ray. <bookmark mark='b2'/>But ray AO starts at A, "
        "so ray AO is a different ray. The first letter always names the starting "
        "point."
    ),
    "s9q": (
        "Your turn. Four quick checks. <bookmark mark='b0'/>For each diagram, say "
        "whether it is a point, a line segment, a line, or a ray. <bookmark "
        "mark='b1'/>Two endpoints joined. <bookmark mark='b2'/>One endpoint with an "
        "arrow. <bookmark mark='b3'/>Arrows at both ends. <bookmark mark='b4'/>And "
        "last of all: can ray OA also be named ray OB?"
    ),
    "s9a": (
        "<bookmark mark='b0'/>The first diagram has two endpoints, so it is the line "
        "segment PQ. <bookmark mark='b1'/>The second has one endpoint and one arrow, "
        "so it is a ray. <bookmark mark='b2'/>The third has arrows at both ends, so "
        "it is a line. <bookmark mark='b3'/>And yes, ray OA can also be named ray "
        "OB, because both start at O and travel in the same direction through the "
        "same straight path."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>A point marks a location. <bookmark "
        "mark='b1'/>Join two points and you have a line segment, with two endpoints "
        "and a definite length. <bookmark mark='b2'/>Extend it one way and it "
        "becomes a ray, with one endpoint; extend it both ways and it becomes a "
        "line, with no endpoints. <bookmark mark='b3'/>From a point, geometry "
        "begins. <bookmark mark='b4'/>Thank you for watching, <bookmark "
        "mark='b5'/>and see you in the next lesson."
    ),
}

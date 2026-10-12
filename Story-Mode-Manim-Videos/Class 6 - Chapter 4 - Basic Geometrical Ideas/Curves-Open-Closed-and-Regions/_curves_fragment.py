"""Board furniture and narration for Storyboard 02 -- Understanding Curves &
Regions: Open, Closed, Interior, Exterior & Boundary, Class 6 Mathematics,
Chapter 4 (Basic Geometrical Ideas).

This file is *spliced*, never imported: assemble_curves.py grafts it into the
proven video-03 head of the Chapter 3 quadrilaterals set, so the theme names
(CHALK_*, FONT, BOARD_*), `board_text`, `chalk_math`, `appear` and the pacing
helpers (`rt`, `quick`, `leftover`) are already defined above it.

The furniture is this video's "one pencil, three questions" kit:

  * `open_wave`    -- an open wavy path (two free ends, no crossing),
  * `oval`         -- a smooth closed loop (the closed, simple curve),
  * `figure_eight` -- a closed self-crossing curve (the lemniscate),
  * `interior_fill`-- the shaded interior of a closed figure,
  * `dot_point`    -- a labelled chalk point,
  * `chip` / `card`-- the labelled chips and cards used for the answers.

The file has two splice markers, a board-layout section and the narration table;
assemble_curves.py cuts between them.
"""
from __future__ import annotations

import numpy as np

# ------------------------------------------------------------ board layout --
# (this section is spliced into a head whose own imports omit Ellipse and
#  VMobject; everything else -- Dot, RoundedRectangle, VGroup, PI, np -- is
#  already imported by the head)
from manim import Ellipse, VMobject  # noqa: E402,F401

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
STROKE_W = 3.4           # chalk stroke width for the curves themselves
DOT_R = 0.072            # radius of a chalk point
LOOP_SPEED = 2.4         # rad/s of the title card's travelling trace point
                         # (a full lap of the closed loop every ~2.6 s)


# ---------------------------------------------------------------- furniture --
def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


def row_centres(half_widths, gap, cx=BOARD_CX):
    """x centres for a row of figures whose ink is `gap` apart.

    The row's combined ink is centred on `cx` (the green board's centre line)
    and the four figures of "one pencil, many curves" are not equally wide, so
    equal centre spacing is NOT equal spacing on the board: this returns the
    centres that leave exactly `gap` units of clear air between neighbours.
    """
    total = 2.0 * sum(half_widths) + gap * (len(half_widths) - 1)
    x = cx - total / 2.0
    centres = []
    for half in half_widths:
        centres.append(x + half)
        x += 2.0 * half + gap
    return tuple(centres)


def loop_point(cx, cy, w, h, phase):
    """A point on a closed oval loop at `phase` radians (0 = right vertex).

    The title card's trace point is driven by this instead of by Rotate: a
    rotation about the centre would trace a circle and leave the oval, while
    the parametric point stays on the drawn loop at every angle.
    """
    return np.array([float(cx) + (w / 2.0) * np.cos(phase),
                     float(cy) + (h / 2.0) * np.sin(phase), 0.0])


def straight_line(x1, x2, y, color=CHALK_WHITE, width=STROKE_W):
    """A plain straight chalk line between two x positions."""
    from manim import Line  # noqa: E402  (already imported by the head)
    return Line(np.array([x1, y, 0.0]), np.array([x2, y, 0.0]),
                stroke_color=color, stroke_width=width)


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


def dot_point(name=None, x=0.0, y=0.0, color=CHALK_CYAN, size=20,
              label_dy=0.34, r=DOT_R):
    """One chalk point with its capital-letter name under (or over) it."""
    dot = Dot(radius=r, color=color, fill_opacity=1.0)
    dot.move_to(np.array([float(x), float(y), 0.0]))
    grp = VGroup(dot)
    if name:
        lab = board_text(name, size, color, "BOLD")
        lab.move_to(np.array([float(x), float(y) + label_dy, 0.0]))
        grp.add(lab)
        grp.label = lab
    grp.dot = dot
    return grp


def open_wave(color=CHALK_CYAN, width=2.70, amp=0.52, cycles=1.5, n=60,
              stroke=STROKE_W):
    """An open wavy path: two free ends, no self-crossing."""
    xs = np.linspace(-width / 2.0, width / 2.0, n)
    ys = amp * np.sin(2.0 * PI * cycles * xs / width)
    pts = np.stack([xs, ys, np.zeros_like(xs)], axis=1)
    vm = VMobject().set_points_smoothly(pts)
    vm.set_stroke(color, stroke)
    return vm


def oval(color=CHALK_GREEN, w=2.50, h=1.70, stroke=STROKE_W):
    """A smooth closed loop (the simple closed curve)."""
    return Ellipse(width=w, height=h, stroke_color=color, stroke_width=stroke)


def figure_eight(color=CHALK_PINK, a=0.95, n=120, stroke=STROKE_W):
    """A closed self-crossing curve: the lemniscate (a figure eight)."""
    t = np.linspace(0.0, 2.0 * PI, n, endpoint=False)
    denom = 1.0 + np.sin(t) ** 2
    x = a * np.cos(t) / denom
    y = a * np.sin(t) * np.cos(t) / denom
    pts = np.stack([x, y, np.zeros_like(x)], axis=1)
    vm = VMobject().set_points_smoothly(pts)
    vm.set_stroke(color, stroke)
    return vm


def interior_fill(w=2.50, h=1.70, color=CHALK_CYAN, opacity=0.22):
    """The shaded interior of a closed figure (drawn behind its boundary)."""
    return Ellipse(width=w, height=h, stroke_width=0, fill_color=color,
                   fill_opacity=opacity)


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "A curve is one of the first ideas in geometry. <bookmark mark='b0'/>It "
        "is a drawing made without lifting the pencil from the paper. <bookmark "
        "mark='b1'/>Some curves close up, and some stay open; and a closed curve "
        "separates the plane into an inside and an outside. Let us learn how to "
        "tell them apart."
    ),
    "s1": (
        "Imagine drawing with a pencil, and never lifting it from the paper. "
        "<bookmark mark='b0'/>You might draw a wavy path, or a loop, or a path "
        "that crosses itself. <bookmark mark='b1'/>And here is a surprise: in "
        "geometry, even a straight line is a curve. <bookmark mark='b2'/>So a "
        "curve is any figure drawn in one continuous stroke, without lifting the "
        "pencil."
    ),
    "s2": (
        "Now ask the first question: does the path close? <bookmark mark='b0'/>"
        "Look at this wavy path. Its two ends stay apart, so it is an open "
        "curve. <bookmark mark='b1'/>Now look at this loop. The pencil comes all "
        "the way back to its starting point, so the path closes. <bookmark "
        "mark='b2'/>That is a closed curve."
    ),
    "s3": (
        "The second question is: does the path cross itself? <bookmark "
        "mark='b0'/>This loop never crosses itself, so it is a simple curve. "
        "<bookmark mark='b1'/>But this figure crosses itself, right here, where "
        "the two parts meet. <bookmark mark='b2'/>So it is not simple. A simple "
        "curve is simply one that does not cross itself."
    ),
    "s4": (
        "These are two different questions. <bookmark mark='b0'/>This wavy path "
        "is open, because its ends stay apart, and simple, because it never "
        "crosses itself. <bookmark mark='b1'/>This oval is closed, and it is "
        "simple too. <bookmark mark='b2'/>But this figure is closed and it "
        "crosses itself, so it is not simple. Open or closed, and simple or not "
        "simple, are two separate questions."
    ),
    "s5": (
        "Now watch what a closed curve does. <bookmark mark='b0'/>It is like the "
        "boundary wall of a park. <bookmark mark='b1'/>The wall splits the plane "
        "into three parts: the inside, which we call the interior; the wall "
        "itself, the boundary; and the outside, the exterior. <bookmark "
        "mark='b2'/>To get from outside the park to inside, you must cross the "
        "boundary."
    ),
    "s6": (
        "So when you see a closed figure, ask: where is each point? <bookmark "
        "mark='b0'/>A point inside is in the interior. <bookmark mark='b1'/>A "
        "point exactly on the edge is on the boundary. <bookmark mark='b2'/>And "
        "a point outside is in the exterior."
    ),
    "s7": (
        "Now we can say what a region is. <bookmark mark='b0'/>The region is the "
        "interior and the boundary taken together. <bookmark mark='b1'/>The "
        "interior alone is not the whole region; the edge is part of the region "
        "too. <bookmark mark='b2'/>Region equals interior plus boundary."
    ),
    "s8": (
        "One more step connects curves to the shapes we study next. <bookmark "
        "mark='b0'/>If a simple closed curve is made of straight line segments, "
        "<bookmark mark='b1'/>it is called a polygon. <bookmark mark='b2'/>So a "
        "polygon is a special kind of simple closed figure, and we will meet it "
        "very soon."
    ),
    "s9q": (
        "Your turn. Four quick checks. <bookmark mark='b0'/>For each diagram, say "
        "whether the curve is open or closed, and simple or not simple. <bookmark "
        "mark='b1'/>A wavy path with two free ends. <bookmark mark='b2'/>A closed "
        "oval. <bookmark mark='b3'/>A path that crosses itself. <bookmark "
        "mark='b4'/>And last of all: in this closed figure, point P is inside, "
        "point Q is on the edge, and point R is outside. Classify P, Q and R."
    ),
    "s9a": (
        "<bookmark mark='b0'/>The first is open, because its ends do not meet, "
        "and simple, because it never crosses itself. <bookmark mark='b1'/>The "
        "second is closed and simple: a smooth oval. <bookmark mark='b2'/>The "
        "third crosses itself, so it is not simple. <bookmark mark='b3'/>And in "
        "the last figure, P is in the interior, Q is on the boundary, and R is in "
        "the exterior."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>A curve is drawn without lifting the "
        "pencil. <bookmark mark='b1'/>If the ends stay apart, it is open; if they "
        "join, it is closed. <bookmark mark='b2'/>And if it never crosses itself, "
        "it is simple. <bookmark mark='b3'/>A closed curve gives us interior, "
        "boundary and exterior, and the region is the interior plus the "
        "boundary. <bookmark mark='b4'/>Draw, classify, locate. <bookmark "
        "mark='b5'/>Thank you for watching, <bookmark mark='b6'/>and see you in "
        "the next lesson."
    ),
}

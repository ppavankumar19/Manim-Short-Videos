"""Board furniture and narration for Storyboard 06 -- Exploring Quadrilaterals:
Sides, Angles, Diagonals, and Opposite vs. Adjacent Elements, Class 6
Mathematics, Chapter 4 (Basic Geometrical Ideas).

This file is *spliced*, never imported: assemble_quads.py grafts it into the
proven video-03 head of the Chapter 3 quadrilaterals set, so the theme names
(CHALK_*, FONT, BOARD_*), `board_text`, `chalk_math`, `appear` and the pacing
helpers (`rt`, `quick`, `leftover`) are already defined above it.

The furniture is this video's "one quadrilateral, six layers" kit:

  * `quad_pts`   -- the quadrilateral's four vertices, scaled about its
                    centroid, so every scene can place the very same figure,
  * `quad_fill`  -- the soft interior tint of the figure,
  * `quad_side`  -- one thick chalk side (one of the four line segments),
  * `corner_arc` -- the angle mark drawn in a corner of the quadrilateral,
  * `diag`       -- a dashed diagonal, the convention for a line across the
                    inside of a figure,
  * `dot_point`  -- a labelled point (vertex, or a point in a region),
  * `chip`       -- a small labelled chip.

Diagrams are drawn realistically: the sides are thick chalk strokes, the four
vertices carry solid dots with their letters offset outward, the interior is
tinted so the figure reads as a region, and the two diagonals are dashed so they
are never confused with the boundary.
"""
from __future__ import annotations

import numpy as np

# ------------------------------------------------------------ board layout --
# (this section is spliced into a head whose own imports omit Arc and Sector;
#  Dot, Line, DashedLine, Arrow, Circle, Polygon, VGroup and np are there)
from manim import Arc, Sector  # noqa: E402,F401

# Board layout shared by every scene of this video.
ROW_Y = 2.72             # every scene heading sits on this line
SUB_Y = 2.16             # the one-line sub-heading under it
BANNER_Y = -1.15         # the closing banner, above the strip
# The burned-in caption grows up from the bottom of the frame: a one-line cue
# starts at y = -3.38 and a wrapped two-line cue reaches y = -2.93 (measured on
# the burned caps), so every closing strip sits at -1.80 and nothing at all sits
# below CAPTION_SAFE_Y = -2.00 -- audited by the IN-CAPTION-BAND check.
STRIP_Y = -1.80
CAPTION_SAFE_Y = -2.00

PANEL_FILL = "#16202B"
SIDE_W = 4.4             # stroke width of a chalk side
DIAG_W = 3.2             # stroke width of a diagonal
DOT_R = 0.084            # radius of a point dot
CORNER_R = 0.42          # radius of a corner's angle mark
MARK_SIZE = 18           # ONE letter size for every corner letter
LABEL_R = 0.40           # every corner letter sits this far out along the
                         # bisector of its own corner, in every scene
SIDE_LAB_R = 0.30        # every side name sits this far off its own line

# The persistent quadrilateral A-B-C-D, in order round the boundary.  It is a
# general convex quadrilateral -- deliberately NOT a special one (no pair of
# sides parallel, no two angles equal), because this section is about the
# general structure -- but it is drawn clean and well proportioned: a 3.05 x
# 1.77 figure whose ink is centred on the board axis.
#   A top-left, B top-right, C bottom-right, D bottom-left
QUAD_CEN = (BOARD_CX, 0.51)          # the ink's bounding-box centre
QUAD_LOCAL = ((-1.525, 0.885), (1.325, 0.615),
              (1.525, -0.855), (-1.175, -0.885))

# The right-hand column carries the labels of whatever the scene is naming.
# The figure is the diagram block and keeps the board's centre line; the column
# is its deliberate side label column, left-aligned just right of the figure's
# rightmost corner letter (2.41) so every label starts on the same vertical
# line and none of them can reach the board's edge or run across the figure.
COL_L = 2.70
COL_W = 2.70             # the widest a column item may be
COL_ROWS = (1.20, 0.50, -0.20)
COL_NOTE_Y = -0.95


# ---------------------------------------------------------------- furniture --
def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


def at_left(mob, x, y):
    """Pin a mobject by its LEFT edge (and vertical centre).

    The right-hand column's labels are left-aligned on `COL_L`, so however wide
    a chip is, every one of them starts on the same vertical line -- and none of
    them can drift across the figure or off the green board.
    """
    mob.move_to(np.array([float(x) + mob.width / 2.0, float(y), 0.0]))
    return mob


def quad_pts(scale=1.0, cx=QUAD_CEN[0], cy=QUAD_CEN[1]):
    """The quadrilateral's four vertices, scaled and moved as one figure.

    `QUAD_LOCAL` is already centred on its own bounding box, so passing
    `cx=BOARD_CX` centres the figure's ink on the board axis -- which is what
    every scene does, so the same quadrilateral is centred in every frame.
    """
    return [(cx + p[0] * scale, cy + p[1] * scale) for p in QUAD_LOCAL]


def quad_centroid(pts):
    """The average of the four vertices (used to keep normals outward)."""
    return tuple(np.mean(np.array([[*p, 0.0] for p in pts], dtype=float),
                         axis=0)[:2])


def corner_label_dx(pts, i, r=LABEL_R):
    """The offset that puts corner `i`'s letter just outside its own corner.

    The letter goes `r` units along the bisector of the corner's interior
    angle, away from the figure -- the textbook place for a corner letter.
    Using the same rule at every corner and in every scene is what makes the
    four letters look alike (the old offsets were four hand-picked pairs of
    different direction, so A, B, C and D each sat a different way).
    """
    p = np.array(pts[i], dtype=float)
    q = np.array(pts[(i + 1) % 4], dtype=float)
    o = np.array(pts[(i - 1) % 4], dtype=float)
    u = (q - p) / np.linalg.norm(q - p)
    w = (o - p) / np.linalg.norm(o - p)
    b = u + w
    b = b / np.linalg.norm(b)
    return (-b[0] * r, -b[1] * r)


def side_label_pos(pts, i, r=SIDE_LAB_R):
    """Where side `i` (corner i -> corner i+1) has its name written.

    `r` units off the middle of the side, on the outside: so a side name can
    never land on its side, and every side name is the same distance out.
    """
    p = np.array(pts[i], dtype=float)
    q = np.array(pts[(i + 1) % 4], dtype=float)
    mid = (p + q) / 2.0
    d = (q - p) / np.linalg.norm(q - p)
    n = np.array([-d[1], d[0]])
    cen = np.array(quad_centroid(pts))
    if np.dot(n, cen - mid) > 0.0:
        n = -n
    out = mid + n * r
    return (float(out[0]), float(out[1]))


def quad_fill(pts, opacity=0.14, color=CHALK_CYAN):
    """The soft interior tint of the quadrilateral."""
    return Polygon(*[np.array([p[0], p[1], 0.0]) for p in pts],
                   stroke_width=0, fill_color=color, fill_opacity=opacity)


def quad_side(p1, p2, color=CHALK_GREEN, width=SIDE_W):
    """One thick chalk side -- one of the four line segments."""
    return Line(np.array([float(p1[0]), float(p1[1]), 0.0]),
                np.array([float(p2[0]), float(p2[1]), 0.0]),
                stroke_color=color, stroke_width=width)


def diag(p1, p2, color=CHALK_YELLOW, width=DIAG_W, dash=0.16):
    """One dashed diagonal: the convention for a segment across the inside."""
    return DashedLine(np.array([float(p1[0]), float(p1[1]), 0.0]),
                      np.array([float(p2[0]), float(p2[1]), 0.0]),
                      color=color, stroke_color=color, stroke_width=width,
                      dash_length=dash)


def corner_arc(vertex, p, q, radius=CORNER_R, color=CHALK_AMBER, width=2.8):
    """The angle mark in the corner at `vertex`, drawn between the two sides
    that run from it towards `p` and `q` (the shorter way round)."""
    v = np.array([float(vertex[0]), float(vertex[1]), 0.0])
    a1 = np.arctan2(p[1] - vertex[1], p[0] - vertex[0])
    a2 = np.arctan2(q[1] - vertex[1], q[0] - vertex[0])
    sweep = (a2 - a1 + np.pi) % (2.0 * np.pi) - np.pi
    return Arc(radius=radius, start_angle=a1, angle=sweep, arc_center=v,
               stroke_color=color, stroke_width=width)


def dot_point(name=None, x=0.0, y=0.0, color=CHALK_CYAN, size=MARK_SIZE,
              label_dx=(0.0, 0.0), r=DOT_R):
    """One chalk point with its letter beside it."""
    dot = Dot(radius=r, color=color, fill_opacity=1.0)
    dot.move_to(np.array([float(x), float(y), 0.0]))
    grp = VGroup(dot)
    if name:
        lab = board_text(name, size, color, "BOLD")
        lab.move_to(np.array([float(x) + label_dx[0], float(y) + label_dx[1],
                              0.0]))
        grp.add(lab)
        grp.label = lab
    grp.dot = dot
    return grp


def chip(text, color=CHALK_CYAN, size=15, width=None, height=0.46):
    """A small labelled chip."""
    lab = board_text(text, size, color, "BOLD")
    box = RoundedRectangle(corner_radius=0.09,
                           width=width or (lab.width + 0.40), height=height,
                           stroke_color=color, stroke_width=1.7,
                           fill_color=PANEL_FILL, fill_opacity=0.7)
    lab.move_to(box.get_center())
    return VGroup(box, lab)


def mark_yes(p, color=CHALK_GREEN, s=0.17):
    """A drawn tick (Segoe Print has no tick glyph)."""
    a = np.array([p[0] - s * 0.60, p[1] + s * 0.05, 0.0])
    b = np.array([p[0] - s * 0.05, p[1] - s * 0.55, 0.0])
    c = np.array([p[0] + s * 0.65, p[1] + s * 0.75, 0.0])
    return VGroup(Line(a, b, stroke_color=color, stroke_width=3.4),
                  Line(b, c, stroke_color=color, stroke_width=3.4))


def mark_no(p, color=CHALK_RED, s=0.17):
    """A drawn cross."""
    return VGroup(
        Line(np.array([p[0] - s * 0.6, p[1] - s * 0.6, 0.0]),
             np.array([p[0] + s * 0.6, p[1] + s * 0.6, 0.0]),
             stroke_color=color, stroke_width=3.4),
        Line(np.array([p[0] - s * 0.6, p[1] + s * 0.6, 0.0]),
             np.array([p[0] + s * 0.6, p[1] - s * 0.6, 0.0]),
             stroke_color=color, stroke_width=3.4))


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "A quadrilateral is a simple closed polygon with four sides. <bookmark "
        "mark='b0'/>It has four vertices and four angles, <bookmark "
        "mark='b1'/>and it also has two diagonals."
    ),
    "s1": (
        "In the last lesson we closed a figure with three line segments: a "
        "triangle. <bookmark mark='b0'/>What happens if we add one more corner? "
        "<bookmark mark='b1'/>Watch the side CA. It opens out into two new "
        "sides, CD and DA, and the figure closes again. <bookmark mark='b2'/>Now "
        "the figure has four sides, so it is a quadrilateral."
    ),
    "s2": (
        "Let us build it segment by segment. <bookmark mark='b0'/>Here is side "
        "AB. <bookmark mark='b1'/>Attach side BC. <bookmark mark='b2'/>Attach "
        "side CD: the figure is still open. <bookmark mark='b3'/>Attach side DA, "
        "and the ends meet. The figure closes. <bookmark mark='b4'/>Simple, "
        "because the sides do not cross; closed, because the ends join up; and "
        "four sides. That is a quadrilateral, and like every closed figure it "
        "has an interior, a boundary and an exterior."
    ),
    "s3": (
        "The four line segments are the sides: side AB, <bookmark mark='b0'/>"
        "side BC, <bookmark mark='b1'/>side CD, <bookmark mark='b2'/>and side "
        "DA, which brings us back to A. <bookmark mark='b3'/>The four points A, "
        "B, C and D are its vertices. <bookmark mark='b4'/>So the sides form the "
        "boundary, <bookmark mark='b5'/>and the vertices are the corners where "
        "two sides meet."
    ),
    "s4": (
        "At every vertex, the two sides form an angle. <bookmark mark='b0'/>At "
        "corner A we have angle A, <bookmark mark='b1'/>at corner B angle B, "
        "<bookmark mark='b2'/>at corner C angle C, <bookmark mark='b3'/>and at "
        "corner D angle D. <bookmark mark='b4'/>So four vertices give four "
        "angles."
    ),
    "s5": (
        "Now compare the sides. <bookmark mark='b0'/>Side AB and side BC meet at "
        "the vertex B, so they are adjacent. <bookmark mark='b1'/>Side AB and "
        "side DA meet at the vertex A, so they are adjacent as well. <bookmark "
        "mark='b2'/>Adjacent sides always share a vertex."
    ),
    "s6": (
        "Some elements are across from each other instead. <bookmark "
        "mark='b0'/>Side AB and side CD do not meet at all, so they are opposite "
        "sides. <bookmark mark='b1'/>Side BC and side DA are the other pair of "
        "opposite sides. <bookmark mark='b2'/>Angles have opposites too: angle A "
        "is opposite angle C, and angle B is opposite angle D. <bookmark "
        "mark='b3'/>So adjacent means next to, and opposite means across."
    ),
    "s7": (
        "Now join the opposite vertices. <bookmark mark='b0'/>The vertices A and "
        "C are opposite, and joining them gives the segment AC. <bookmark "
        "mark='b1'/>The vertices B and D are opposite, and joining them gives the "
        "segment BD. <bookmark mark='b2'/>These two segments are the diagonals "
        "of the quadrilateral: a diagonal joins two opposite vertices."
    ),
    "s8": (
        "Let us put the whole relationship map together. <bookmark "
        "mark='b0'/>Adjacent elements share a corner: AB and BC share the vertex "
        "B. <bookmark mark='b1'/>Opposite elements lie across the shape: AB and "
        "CD share no vertex. <bookmark mark='b2'/>And a diagonal connects the "
        "opposite corners: AC joins A and C. <bookmark mark='b3'/>So ask "
        "yourself: are they next to each other, across from each other, or "
        "joined across?"
    ),
    "s9q": (
        "Your turn. Four quick checks on quadrilateral PQRS. <bookmark "
        "mark='b0'/>First: which side is opposite QR? <bookmark mark='b1'/>"
        "Second: which angle is opposite angle P? <bookmark mark='b2'/>Third: "
        "which sides are adjacent to PQ? <bookmark mark='b3'/>And last of all: "
        "join the opposite vertices, and name the two diagonals."
    ),
    "s9a": (
        "<bookmark mark='b0'/>The side opposite QR is PS. <bookmark "
        "mark='b1'/>The angle opposite angle P is angle R. <bookmark "
        "mark='b2'/>The sides adjacent to PQ are PS and QR, because each of them "
        "shares a vertex with PQ. <bookmark mark='b3'/>And the two diagonals are "
        "PR and QS: they join the opposite vertices P with R, and Q with S."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>A quadrilateral is a simple closed "
        "polygon with four sides, <bookmark mark='b1'/>four vertices and four "
        "angles. <bookmark mark='b2'/>Adjacent elements are next to each other, "
        "and opposite elements are across the shape. <bookmark mark='b3'/>And "
        "its two diagonals join the opposite vertices. <bookmark mark='b4'/>"
        "Build it, compare its parts, and connect the corners. <bookmark "
        "mark='b5'/>Thank you for watching, <bookmark mark='b6'/>and see you in "
        "the next lesson."
    ),
}

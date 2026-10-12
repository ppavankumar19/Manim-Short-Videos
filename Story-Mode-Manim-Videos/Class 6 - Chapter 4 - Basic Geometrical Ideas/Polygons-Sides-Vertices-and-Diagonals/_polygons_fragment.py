"""Board furniture and narration for Storyboard 03 -- Polygons Explained: Sides,
Vertices, Adjacent Elements & Diagonals, Class 6 Mathematics, Chapter 4 (Basic
Geometrical Ideas).

This file is *spliced*, never imported: assemble_polygons.py grafts it into the
proven video-03 head of the Chapter 3 quadrilaterals set, so the theme names
(CHALK_*, FONT, BOARD_*), `board_text`, `chalk_math`, `appear` and the pacing
helpers (`rt`, `quick`, `leftover`) are already defined above it.

The furniture is this video's "build the polygon, then reveal its anatomy" kit:

  * `side_seg`   -- one thick boundary side (a straight line segment),
  * `diag`       -- a dashed diagonal (the textbook convention),
  * `vertex`     -- a solid corner dot with its capital-letter name,
  * `poly_outline` -- a filled polygon outline (soft interior tint),
  * `open_chain` -- an open zig-zag of three segments (not yet a polygon).

The diagrams are drawn realistically: solid vertex dots, thick chalk sides, a
subtle interior tint, and dashed diagonals -- the same conventions a textbook
figure uses.
"""
from __future__ import annotations

import numpy as np

# ------------------------------------------------------------ board layout --
# (this section is spliced into a head whose own imports omit DashedLine,
#  Ellipse and Polygon; Dot, RoundedRectangle, VGroup, PI and np are already
#  imported by the head)
from manim import DashedLine, Ellipse, Polygon  # noqa: E402,F401

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
SIDE_W = 4.6             # stroke width of a boundary side
DOT_R = 0.078            # radius of a vertex dot
MARK_SIZE = 18           # ONE letter size for every labelled figure
LABEL_DX = 0.30          # every corner letter sits this far out sideways ...
LABEL_DY = 0.34          # ... and this far out vertically, in every scene, so
                         # no letter ever lands on a side or on another label

# The persistent quadrilateral ABCD: a clean, symmetric convex trapezium whose
# ink is centred on the board axis.  AB is the long bottom side, DC the shorter
# top side centred over it -- a well-proportioned textbook quadrilateral whose
# two diagonals cross exactly on the board's centre line (0.5, 0.47).
#   A bottom-left, B bottom-right, C top-right, D top-left (anti-clockwise)
QUAD_PTS = {"A": (BOARD_CX - 1.85, -0.34), "B": (BOARD_CX + 1.85, -0.34),
            "C": (BOARD_CX + 1.05, 1.28), "D": (BOARD_CX - 1.05, 1.28)}
QUAD_CENTRE = (BOARD_CX, 0.47)      # the ink's own centre
QUAD_LABEL_DX = {"A": (-LABEL_DX, -LABEL_DY), "B": (LABEL_DX, -LABEL_DY),
                 "C": (LABEL_DX, LABEL_DY), "D": (-LABEL_DX, LABEL_DY)}

# The triangle ABC used by the first three scenes, centred on the same axis.
TRI_PTS = {"A": (BOARD_CX - 1.60, -0.34), "B": (BOARD_CX + 1.60, -0.34),
           "C": (BOARD_CX, 1.28)}
TRI_LABEL_DX = {"A": (-LABEL_DX, -LABEL_DY), "B": (LABEL_DX, -LABEL_DY),
                "C": (0.0, LABEL_DY)}


# ---------------------------------------------------------------- furniture --
def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


def row_centres(half_widths, gap, cx=BOARD_CX):
    """x centres for a row of elements whose ink is `gap` apart.

    The row's combined ink is centred on `cx` (the green board's centre line)
    and the elements of a row are not equally wide, so equal centre spacing is
    NOT equal spacing on the board: this returns the centres that leave exactly
    `gap` units of clear air between neighbours.
    """
    total = 2.0 * sum(half_widths) + gap * (len(half_widths) - 1)
    x = cx - total / 2.0
    centres = []
    for half in half_widths:
        centres.append(x + half)
        x += 2.0 * half + gap
    return tuple(centres)


def chip(text, color=CHALK_CYAN, size=15, width=None, height=0.50):
    """A small labelled chip."""
    lab = board_text(text, size, color, "BOLD")
    box = RoundedRectangle(corner_radius=0.09,
                           width=width or (lab.width + 0.40), height=height,
                           stroke_color=color, stroke_width=1.7,
                           fill_color=PANEL_FILL, fill_opacity=0.7)
    lab.move_to(box.get_center())
    return VGroup(box, lab)


def card(title, lines, color=CHALK_WHITE, width=4.0, height=1.30,
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


def side_seg(p1, p2, color=CHALK_GREEN, width=SIDE_W):
    """One thick boundary side."""
    return Line(np.array([*p1, 0.0]), np.array([*p2, 0.0]),
                stroke_color=color, stroke_width=width)


def diag(p1, p2, color=CHALK_AMBER, width=3.2):
    """A diagonal: dashed, the textbook convention."""
    return DashedLine(np.array([*p1, 0.0]), np.array([*p2, 0.0]),
                      dash_length=0.15, stroke_color=color, stroke_width=width)


def vertex(name, pt, color=CHALK_CYAN, size=MARK_SIZE, label_dx=(0.0, 0.0)):
    """A solid corner dot with its capital-letter name beside it."""
    dot = Dot(radius=DOT_R, color=color, fill_opacity=1.0).move_to(
        np.array([pt[0], pt[1], 0.0]))
    lab = board_text(name, size, color, "BOLD").move_to(
        np.array([pt[0] + label_dx[0], pt[1] + label_dx[1], 0.0]))
    grp = VGroup(dot, lab)
    grp.dot = dot
    grp.label = lab
    return grp


def poly_outline(points, color=CHALK_GREEN, width=SIDE_W, fill=CHALK_CYAN,
                 opacity=0.12):
    """A filled polygon outline (soft interior tint, thick chalk sides)."""
    return Polygon(*[np.array([*p, 0.0]) for p in points],
                   stroke_color=color, stroke_width=width,
                   fill_color=fill, fill_opacity=opacity)


def quad_vertices():
    """The four labelled corner dots of quadrilateral ABCD."""
    return quad_verts(QUAD_PTS)


def quad_points(scale=1.0, dx=0.0, dy=0.0):
    """The four corners of ABCD, shrunk about the figure's own centre.

    `scale` lets the same clean quadrilateral appear full size in the teaching
    scenes and smaller in the curve -> polygon comparison; the letters keep the
    one outward offset, so they look the same in both.
    """
    cx, cy = QUAD_CENTRE
    return {n: (cx + scale * (p[0] - cx) + dx,
                cy + scale * (p[1] - cy) + dy) for n, p in QUAD_PTS.items()}


def quad_shape(points, color=CHALK_GREEN, width=4.0):
    """The quadrilateral outline through `points` (A, B, C, D in order)."""
    return poly_outline([points[n] for n in "ABCD"], color, width)


def quad_verts(points, color=CHALK_CYAN, size=MARK_SIZE):
    """Its four solid corner dots, each with its letter just outside."""
    return VGroup(*[vertex(n, points[n], color, size, label_dx=QUAD_LABEL_DX[n])
                    for n in "ABCD"])


def tri_shape(color=CHALK_GREEN, width=4.0):
    """The triangle ABC outline."""
    return poly_outline([TRI_PTS[n] for n in "ABC"], color, width)


def tri_verts(color=CHALK_CYAN, size=MARK_SIZE):
    """Its three solid corner dots, each with its letter just outside."""
    return VGroup(*[vertex(n, TRI_PTS[n], color, size, label_dx=TRI_LABEL_DX[n])
                    for n in "ABC"])


def qpoint(name):
    """One corner of the persistent quadrilateral ABCD."""
    return QUAD_PTS[name]


def qvert(name, color=CHALK_CYAN, size=MARK_SIZE):
    """One labelled corner of the persistent quadrilateral."""
    return vertex(name, QUAD_PTS[name], color, size,
                  label_dx=QUAD_LABEL_DX[name])


def tpoint(name):
    """One corner of triangle ABC."""
    return TRI_PTS[name]


def tvert(name, color=CHALK_CYAN, size=MARK_SIZE):
    """One labelled corner of triangle ABC."""
    return vertex(name, TRI_PTS[name], color, size,
                  label_dx=TRI_LABEL_DX[name])


def open_chain(color=CHALK_WHITE, width=SIDE_W):
    """Three segments arranged as an open zig-zag (not yet a polygon).

    Symmetric about the origin, so `at(chain, BOARD_CX, y)` centres it.
    """
    a = (-1.55, 0.45)
    b = (-0.50, -0.35)
    c = (0.50, 0.45)
    d = (1.55, -0.15)
    segs = VGroup(side_seg(a, b, color, width),
                  side_seg(b, c, color, width),
                  side_seg(c, d, color, width))
    return segs


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "A polygon is the next idea in geometry. <bookmark mark='b0'/>It is a "
        "simple closed figure made from a definite number of straight line "
        "segments. <bookmark mark='b1'/>Inside every polygon we find sides, "
        "vertices, and diagonals. Let us learn their names."
    ),
    "s1": (
        "We already know a simple closed curve. <bookmark mark='b0'/>But a "
        "smooth curve like this is not a polygon. <bookmark mark='b1'/>When its "
        "boundary becomes straight line segments, <bookmark mark='b2'/>the "
        "figure is called a polygon."
    ),
    "s2": (
        "What must a polygon have? <bookmark mark='b0'/>It must be made of line "
        "segments, it must be closed, and it must not cross itself. <bookmark "
        "mark='b1'/>Here are three segments, open, so it is not a polygon yet. "
        "<bookmark mark='b2'/>Join the ends and it closes into a triangle. "
        "<bookmark mark='b3'/>Three sides is the smallest number that can close."
    ),
    "s3": (
        "Look at triangle ABC. <bookmark mark='b0'/>Its three line segments are "
        "its sides. <bookmark mark='b1'/>Its three corner points, A, B and C, "
        "are its vertices. <bookmark mark='b2'/>Each vertex is the place where "
        "two sides meet."
    ),
    "s4": (
        "Now add a fourth vertex and build quadrilateral ABCD. <bookmark "
        "mark='b0'/>Its four sides are AB, BC, CD, and DA. <bookmark "
        "mark='b1'/>It has four vertices: A, B, C and D."
    ),
    "s5": (
        "Some parts are next to each other. <bookmark mark='b0'/>Side AB shares "
        "vertex B with side BC, and shares vertex A with side DA. <bookmark "
        "mark='b1'/>So AB is adjacent to BC, and adjacent to DA. <bookmark "
        "mark='b2'/>Adjacent means next to, sharing a corner."
    ),
    "s6": (
        "Now look across the quadrilateral. <bookmark mark='b0'/>Side CD does "
        "not touch side AB, so CD is the side opposite AB. <bookmark "
        "mark='b1'/>Vertex A and vertex C are opposite vertices, <bookmark "
        "mark='b2'/>and so are B and D."
    ),
    "s7": (
        "Join the opposite vertices. <bookmark mark='b0'/>The segment from A to "
        "C is a diagonal. <bookmark mark='b1'/>The segment from B to D is the "
        "second diagonal. <bookmark mark='b2'/>So quadrilateral ABCD has two "
        "diagonals: AC and BD."
    ),
    "s8": (
        "Do not mix up a side and a diagonal. <bookmark mark='b0'/>A side is "
        "part of the boundary, like AB. <bookmark mark='b1'/>A diagonal joins "
        "opposite vertices across the inside, like AC. <bookmark mark='b2'/>BC "
        "and DA are sides, while BD is a diagonal."
    ),
    "s9q": (
        "Your turn. Four quick checks on quadrilateral PQRS. <bookmark "
        "mark='b0'/>First, name the four sides. <bookmark mark='b1'/>Second, "
        "name the sides adjacent to PQ. <bookmark mark='b2'/>Third, name the "
        "two diagonals. <bookmark mark='b3'/>And last of all: is this open "
        "chain a polygon?"
    ),
    "s9a": (
        "<bookmark mark='b0'/>The four sides are PQ, QR, RS, and SP. <bookmark "
        "mark='b1'/>The sides adjacent to PQ are QR and PS, because they share "
        "an endpoint with PQ. <bookmark mark='b2'/>The diagonals are PR and QS. "
        "<bookmark mark='b3'/>And no, the open chain is not a polygon, because "
        "it is not closed."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>A polygon is a simple closed figure "
        "made of line segments. <bookmark mark='b1'/>Its boundary segments are "
        "its sides, and its corner points are its vertices. <bookmark "
        "mark='b2'/>Sides that share a vertex are adjacent. <bookmark "
        "mark='b3'/>And line segments that join opposite vertices are diagonals. "
        "<bookmark mark='b4'/>Know the parts, and you understand the polygon. "
        "<bookmark mark='b5'/>Thank you for watching, <bookmark mark='b6'/>and "
        "see you in the next lesson."
    ),
}

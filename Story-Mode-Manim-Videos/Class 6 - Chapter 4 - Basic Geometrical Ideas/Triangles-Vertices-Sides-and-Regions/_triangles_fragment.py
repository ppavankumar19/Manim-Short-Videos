"""Board furniture and narration for Storyboard 05 -- Triangles Uncovered:
Vertices, Sides, Angles, and Triangular Regions, Class 6 Mathematics, Chapter 4
(Basic Geometrical Ideas).

This file is *spliced*, never imported: assemble_triangles.py grafts it into the
proven video-03 head of the Chapter 3 quadrilaterals set, so the theme names
(CHALK_*, FONT, BOARD_*), `board_text`, `chalk_math`, `appear` and the pacing
helpers (`rt`, `quick`, `leftover`) are already defined above it.

The furniture is this video's "three sticks become a triangle" kit:

  * `tri_pts`     -- the triangle's three vertices, scaled about its centroid,
                     so every scene can place the very same figure,
  * `tri_fill`    -- the soft interior tint of the figure,
  * `tri_side`    -- one thick chalk side (one of the three line segments),
  * `match_stick` -- the same segment as a matchstick, with its head,
  * `corner_arc`  -- the angle mark drawn in a corner of the triangle,
  * `dot_point`   -- a labelled point (vertex, or a point in a region),
  * `chip`        -- a small labelled chip,
  * `mark_yes` / `mark_no` -- a drawn tick and cross (Segoe Print has neither).

Diagrams are drawn realistically: the sides are thick chalk strokes, the three
vertices carry solid dots with their letters offset clear of the sides, the
interior is tinted so the figure reads as a region, and every letter of a region
point is placed so no letter ever sits on a side.
"""
from __future__ import annotations

import numpy as np

# ------------------------------------------------------------ board layout --
# (this section is spliced into a head whose own imports omit Arc, Sector and
#  Rotate; Dot, Line, Arrow, Circle, Polygon, VGroup and np are already there)
from manim import Arc, Rotate, Sector  # noqa: E402,F401

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
STICK_W = 7.0            # stroke width of a matchstick
DOT_R = 0.082            # radius of a point dot
CORNER_R = 0.46          # radius of a corner's angle mark
MARK_SIZE = 18           # ONE letter size for every corner letter
LABEL_R = 0.40           # every corner letter sits this far out along the
                         # bisector of its own corner, in every scene
SIDE_LAB_R = 0.26        # every side name sits this far off its own line

# The persistent triangle A-B-C: a clean, well-proportioned SCALENE triangle
# (no two sides equal and no two angles equal -- the general case this lesson
# is about) whose ink is centred on the board axis:
#   base BC 3.00 wide on y = -0.45, apex A at (0.15, 1.30), height 1.75,
#   sides 2.09 / 2.65 / 3.00, angles 57 / 43 / 80 degrees.
#   A apex, B bottom-left, C bottom-right
TRI_A = (0.15, 1.30)
TRI_B = (-1.00, -0.45)
TRI_C = (2.00, -0.45)
TRI_CEN = (BOARD_CX, 0.425)          # the ink's bounding-box centre

# The right-hand column carries the labels of whatever the scene is naming.
# The figure is the diagram block and keeps the board's centre line; the column
# is its deliberate side label column, left-aligned just right of the figure's
# rightmost label (2.45) so every label starts on the same vertical line and
# none of them can reach the board's edge or run across the figure.
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


def tri_pts(scale=1.0, cx=TRI_CEN[0], cy=TRI_CEN[1]):
    """The triangle's three vertices, scaled about the ink's own centre and
    moved so that centre sits at (cx, cy) -- so `cx=BOARD_CX` centres the figure
    on the board in every scene, at any size."""
    return [(cx + (p[0] - TRI_CEN[0]) * scale,
             cy + (p[1] - TRI_CEN[1]) * scale) for p in (TRI_A, TRI_B, TRI_C)]


def tri_centroid(pts):
    """The average of the three vertices (used to keep normals outward)."""
    return tuple(np.mean(np.array([[*p, 0.0] for p in pts], dtype=float),
                         axis=0)[:2])


def corner_label_dx(pts, i, r=LABEL_R):
    """The offset that puts corner `i`'s letter just outside its own corner.

    The letter goes `r` units along the bisector of the corner's interior
    angle, away from the figure -- the textbook place for a corner letter, and
    the same rule at every corner and in every scene, so A, B and C always look
    alike and none of them can sit on a side.
    """
    p = np.array(pts[i], dtype=float)
    q = np.array(pts[(i + 1) % 3], dtype=float)
    o = np.array(pts[(i - 1) % 3], dtype=float)
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
    q = np.array(pts[(i + 1) % 3], dtype=float)
    mid = (p + q) / 2.0
    d = (q - p) / np.linalg.norm(q - p)
    n = np.array([-d[1], d[0]])
    cen = np.array(tri_centroid(pts))
    if np.dot(n, cen - mid) > 0.0:
        n = -n
    out = mid + n * r
    return (float(out[0]), float(out[1]))


def tri_fill(pts, opacity=0.16, color=CHALK_CYAN):
    """The soft interior tint of the triangle."""
    return Polygon(np.array([pts[0][0], pts[0][1], 0.0]),
                   np.array([pts[1][0], pts[1][1], 0.0]),
                   np.array([pts[2][0], pts[2][1], 0.0]),
                   stroke_width=0, fill_color=color, fill_opacity=opacity)


def tri_side(p1, p2, color=CHALK_GREEN, width=SIDE_W):
    """One thick chalk side -- one of the three line segments."""
    return Line(np.array([float(p1[0]), float(p1[1]), 0.0]),
                np.array([float(p2[0]), float(p2[1]), 0.0]),
                stroke_color=color, stroke_width=width)


def match_stick(p1, p2, color=CHALK_AMBER, width=STICK_W):
    """The same segment as a matchstick: the stick plus its head."""
    line = tri_side(p1, p2, color, width)
    head = Dot(radius=0.085, color=CHALK_RED, fill_opacity=1.0)
    head.move_to(np.array([float(p2[0]), float(p2[1]), 0.0]))
    grp = VGroup(line, head)
    grp.line = line
    grp.head = head
    return grp


def corner_arc(vertex, p, q, radius=CORNER_R, color=CHALK_AMBER, width=2.8):
    """The angle mark in the corner at `vertex`, drawn between the two sides
    that run from it towards `p` and `q` (the shorter way round)."""
    v = np.array([float(vertex[0]), float(vertex[1]), 0.0])
    a1 = np.arctan2(p[1] - vertex[1], p[0] - vertex[0])
    a2 = np.arctan2(q[1] - vertex[1], q[0] - vertex[0])
    sweep = (a2 - a1 + np.pi) % (2.0 * np.pi) - np.pi
    return Arc(radius=radius, start_angle=a1, angle=sweep, arc_center=v,
               stroke_color=color, stroke_width=width)


def corner_wedge(vertex, p, q, radius=CORNER_R, color=CHALK_AMBER,
                 opacity=0.20):
    """The light fill of one corner's angle mark."""
    v = np.array([float(vertex[0]), float(vertex[1]), 0.0])
    a1 = np.arctan2(p[1] - vertex[1], p[0] - vertex[0])
    a2 = np.arctan2(q[1] - vertex[1], q[0] - vertex[0])
    sweep = (a2 - a1 + np.pi) % (2.0 * np.pi) - np.pi
    return Sector(radius=radius, start_angle=a1, angle=sweep, stroke_width=0,
                  fill_color=color, fill_opacity=opacity, arc_center=v)


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
        "A triangle has three sides, three vertices and three angles. <bookmark "
        "mark='b0'/>The three sides are line segments, and together they close "
        "the figure. <bookmark mark='b1'/>A triangle also separates the plane "
        "around it into an interior, a boundary and an exterior."
    ),
    "s1": (
        "How many sticks do we need to close a figure? <bookmark mark='b0'/>One "
        "stick cannot close anything: its two ends are far apart. <bookmark "
        "mark='b1'/>Two sticks make a V, and the two free ends are still open. "
        "<bookmark mark='b2'/>Add a third stick, and the ends meet. The figure "
        "closes. <bookmark mark='b3'/>So three is the least number of line "
        "segments needed to make a closed figure."
    ),
    "s2": (
        "The textbook calls this a triangle. <bookmark mark='b0'/>A triangle is "
        "a simple closed figure formed by three line segments. Simple, because "
        "the sides do not cross each other. <bookmark mark='b1'/>Closed, because "
        "the ends join up. <bookmark mark='b2'/>And exactly three line segments: "
        "no more, and no fewer."
    ),
    "s3": (
        "Now let us name the parts. <bookmark mark='b0'/>The three line segments "
        "are the sides of the triangle: side AB, <bookmark mark='b1'/>side BC, "
        "<bookmark mark='b2'/>and side CA. <bookmark mark='b3'/>The three sides "
        "together form the boundary of the triangle."
    ),
    "s4": (
        "The three points where the sides meet are the vertices. <bookmark "
        "mark='b0'/>Point A is one vertex, <bookmark mark='b1'/>point B is the "
        "second, <bookmark mark='b2'/>and point C is the third. <bookmark "
        "mark='b3'/>So a vertex is a corner of the triangle, and it is not the "
        "same as a side."
    ),
    "s5": (
        "At every vertex, the two sides of the triangle form an angle. <bookmark "
        "mark='b0'/>At vertex A we have angle BAC, <bookmark mark='b1'/>at "
        "vertex B we have angle ABC, <bookmark mark='b2'/>and at vertex C we "
        "have angle ACB. <bookmark mark='b3'/>So the three vertices give three "
        "angles."
    ),
    "s6": (
        "How do we name a triangle? <bookmark mark='b0'/>We use its three "
        "vertices. <bookmark mark='b1'/>Going around the figure in order, A then "
        "B then C, gives the name triangle ABC. <bookmark mark='b2'/>The same "
        "triangle can also be read as triangle BCA or triangle CAB."
    ),
    "s7": (
        "A triangle divides the plane around it into three parts. <bookmark "
        "mark='b0'/>Point P lies inside the triangle, so it is in the interior. "
        "<bookmark mark='b1'/>Point Q lies on one of the sides, so it is on the "
        "boundary. <bookmark mark='b2'/>Point R lies outside the triangle, so it "
        "is in the exterior."
    ),
    "s8": (
        "Now we can name the whole figure. <bookmark mark='b0'/>The boundary of "
        "the triangle together with its interior is called the triangular region. "
        "<bookmark mark='b1'/>So the region is not only the shaded inside: "
        "<bookmark mark='b2'/>it also includes the three sides themselves."
    ),
    "s9q": (
        "Your turn. Four quick checks. <bookmark mark='b0'/>First: name the three "
        "sides of triangle PQR. <bookmark mark='b1'/>Second: name its three "
        "vertices. <bookmark mark='b2'/>Third: name the angle at Q. <bookmark "
        "mark='b3'/>And last of all: point X, point Y and point Z. Which of them "
        "is in the interior, which is on the boundary, and which is in the "
        "exterior?"
    ),
    "s9a": (
        "<bookmark mark='b0'/>The three sides of triangle PQR are PQ, QR and RP. "
        "<bookmark mark='b1'/>Its three vertices are P, Q and R. <bookmark "
        "mark='b2'/>The angle at Q is angle PQR, because the vertex Q stays in "
        "the middle. <bookmark mark='b3'/>And point X is in the interior, point Y "
        "is on the boundary, and point Z is in the exterior."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>A triangle is a simple closed figure "
        "made from three line segments. <bookmark mark='b1'/>It has three sides, "
        "three vertices and three angles. <bookmark mark='b2'/>And its boundary "
        "together with its interior is the triangular region. <bookmark "
        "mark='b3'/>Build the triangle, identify its parts, <bookmark "
        "mark='b4'/>and locate the points. <bookmark mark='b5'/>Thank you for "
        "watching, <bookmark mark='b6'/>and see you in the next lesson."
    ),
}

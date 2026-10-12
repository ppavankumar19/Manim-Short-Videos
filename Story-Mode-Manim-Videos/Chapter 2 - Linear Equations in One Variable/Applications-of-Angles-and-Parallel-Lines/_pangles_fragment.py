"""Board furniture and narration for the Class 8, Chapter 2 topic
"Applications of Angles and Parallel Lines".

This file is *spliced*, never imported: assemble_pangles.py grafts it into the
proven video-03 head of the Chapter 3 quadrilaterals set, so the theme names
(CHALK_*, FONT, BOARD_*), `board_text`, `chalk_math`, `appear` and the pacing
helpers (`rt`, `quick`, `leftover`) are already defined above it.

The furniture is this video's "one transversal, eight angles, six rules" kit:

  * `par_pair`      -- the two parallel lines, each carrying the same chevron
                       arrow mark (the textbook's parallel sign),
  * `transversal`   -- the third line that cuts across them,
  * `ANGLE_SPEC`    -- where the eight angles sit: which crossing, and the two
                       directions that bound the wedge,
  * `sector_at` / `arc_at` -- the translucent wedge and its arc mark,
  * `angle_pos`     -- where the number of an angle is written (inside its own
                       wedge, clear of both lines that bound it),
  * `band`          -- the translucent strip between the parallel lines, so the
                       interior angles have a visible home,
  * `dot_point`, `chip`, `chevron`.

Diagrams are drawn realistically: the parallel lines carry the same arrow mark,
the transversal is long enough to stick out past both lines, every one of the
eight angles is a real translucent wedge with its own arc, and the numbers sit
inside their wedges, never on a line.
"""
from __future__ import annotations

import numpy as np

# ------------------------------------------------------------ board layout --
# (this section is spliced into a head whose own imports omit Arc and Sector;
#  Dot, Line, Arrow, Circle, Polygon, VGroup and np are already there)
from manim import Arc, Sector  # noqa: E402,F401

# Board layout shared by every scene of this video.
ROW_Y = 2.72             # every scene heading sits on this line
SUB_Y = 2.16             # the one-line sub-heading under it
BANNER_Y = -1.15         # the closing banner, above the strip
# The burned-in caption grows up from the bottom of the frame: a one-line cue
# starts at y = -3.38 and a wrapped two-line cue reaches y = -2.93, so every
# closing strip sits at -1.80 and nothing at all sits below
# CAPTION_SAFE_Y = -2.00 -- audited by the IN-CAPTION-BAND check.
STRIP_Y = -1.80
CAPTION_SAFE_Y = -2.00
PANEL_FILL = "#16202B"

# The figure: two horizontal parallel lines cut by one steep transversal.
# The lines sit high enough that the lowest wedges and arcs stay clear of the
# closing banner at BANNER_Y, and the transversal stops well above it too.
PAR_Y1 = 1.35            # the upper parallel line
PAR_Y2 = -0.25           # the lower parallel line
PAR_X0 = -3.30
PAR_X1 = 1.30
TRA_TOP = (0.596, 1.85)
TRA_BOT = (-0.360, -0.72)
U_CROSS = (0.410, 1.35)  # where the transversal meets the upper line
L_CROSS = (-0.186, -0.25)  # where it meets the lower line
TRA_ANG = 69.6           # the transversal's "up" direction, in degrees
SECT_R = 0.62            # radius of every angle wedge
LINE_W = 4.0

# The eight angles.  At each crossing the four wedges are, counter-clockwise:
# top-left, top-right, bottom-left, bottom-right.  Numbering (the textbook
# convention): 1-4 at the upper crossing, 5-8 at the lower one, so that
#   1 2 7 8 are exterior, 3 4 5 6 are interior,
#   1=5, 2=6, 3=7, 4=8 correspond, and 3+5, 4+6 are same-side interior.
ANGLE_SPEC = {
    1: (U_CROSS, TRA_ANG, 180.0),
    2: (U_CROSS, 0.0, TRA_ANG),
    3: (U_CROSS, 180.0, TRA_ANG + 180.0),
    4: (U_CROSS, TRA_ANG + 180.0, 360.0),
    5: (L_CROSS, TRA_ANG, 180.0),
    6: (L_CROSS, 0.0, TRA_ANG),
    7: (L_CROSS, 180.0, TRA_ANG + 180.0),
    8: (L_CROSS, TRA_ANG + 180.0, 360.0),
}
INTERIOR = (3, 4, 5, 6)
EXTERIOR = (1, 2, 7, 8)
CORRESPONDING = ((1, 5), (2, 6), (3, 7), (4, 8))
ALT_INTERIOR = ((4, 5), (3, 6))
SAME_SIDE_INTERIOR = ((3, 5), (4, 6))
ALT_EXTERIOR = ((2, 7), (1, 8))
SAME_SIDE_EXTERIOR = ((1, 7), (2, 8))
VERTICAL = ((1, 4), (2, 3), (5, 8), (6, 7))

# The six relationships, in the order this video teaches them.
CHALK_VIOLET = "#B58CF0"
RULE_COLOR = {
    "vertical": CHALK_VIOLET,
    "corresponding": CHALK_PINK,
    "alt_interior": CHALK_RED,
    "same_side_interior": CHALK_GREEN,
    "alt_exterior": CHALK_CYAN,
    "same_side_exterior": CHALK_YELLOW,
}

# The right-hand column: the labels of whatever the scene is naming.
COL_X = 3.60


# ---------------------------------------------------------------- furniture --
def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


def pt(p):
    """A board coordinate as a 3-D point."""
    return np.array([float(p[0]), float(p[1]), 0.0])


def par_pair(color=CHALK_WHITE, width=LINE_W):
    """The two parallel lines, each with the same chevron arrow mark at its
    right-hand end -- the sign that says "these two are parallel"."""
    l1 = Line(pt((PAR_X0, PAR_Y1)), pt((PAR_X1, PAR_Y1)), stroke_color=color,
              stroke_width=width)
    l2 = Line(pt((PAR_X0, PAR_Y2)), pt((PAR_X1, PAR_Y2)), stroke_color=color,
              stroke_width=width)
    m1 = chevron(PAR_X1 - 0.30, PAR_Y1, color)
    m2 = chevron(PAR_X1 - 0.30, PAR_Y2, color)
    grp = VGroup(l1, l2)
    grp.marks = VGroup(m1, m2)
    grp.l1 = l1
    grp.l2 = l2
    return grp


def chevron(x, y, color=CHALK_WHITE, s=0.17):
    """A small ">" arrowhead on a line: the parallel mark."""
    a = np.array([float(x), float(y) + s, 0.0])
    b = np.array([float(x) + s * 0.85, float(y), 0.0])
    c = np.array([float(x), float(y) - s, 0.0])
    return VGroup(Line(a, b, stroke_color=color, stroke_width=3.0),
                  Line(b, c, stroke_color=color, stroke_width=3.0))


def transversal(color=CHALK_AMBER, width=LINE_W):
    """The third line, long enough to stick out past both parallel lines."""
    return Line(pt(TRA_BOT), pt(TRA_TOP), stroke_color=color,
                stroke_width=width)


def sector_at(vertex, a1, a2, radius=SECT_R, color=CHALK_CYAN, opacity=0.22):
    """The translucent wedge of one angle."""
    return Sector(radius=radius, start_angle=np.radians(a1),
                  angle=np.radians(a2 - a1), stroke_width=0,
                  fill_color=color, fill_opacity=opacity, arc_center=pt(vertex))


def arc_at(vertex, a1, a2, radius=SECT_R, color=CHALK_AMBER, width=2.8):
    """The arc that marks one angle."""
    return Arc(radius=radius, start_angle=np.radians(a1),
               angle=np.radians(a2 - a1), arc_center=pt(vertex),
               stroke_color=color, stroke_width=width)


def angle_sector(n, radius=SECT_R, color=CHALK_CYAN, opacity=0.22):
    v, a1, a2 = ANGLE_SPEC[n]
    return sector_at(v, a1, a2, radius, color, opacity)


def angle_arc(n, radius=SECT_R, color=CHALK_AMBER, width=2.8):
    v, a1, a2 = ANGLE_SPEC[n]
    return arc_at(v, a1, a2, radius, color, width)


def angle_pos(n, dist=0.42):
    """Where the number of angle `n` is written: inside its own wedge, on the
    bisector, far enough from both bounding lines that the digits never touch
    a line."""
    (vx, vy), a1, a2 = ANGLE_SPEC[n]
    mid = np.radians((a1 + a2) / 2.0)
    return (vx + dist * np.cos(mid), vy + dist * np.sin(mid))


def band(color=CHALK_CYAN, opacity=0.10):
    """The translucent strip between the parallel lines: the interior."""
    poly = Polygon(pt((PAR_X0, PAR_Y2)), pt((PAR_X1, PAR_Y2)),
                   pt((PAR_X1, PAR_Y1)), pt((PAR_X0, PAR_Y1)),
                   stroke_width=0, fill_color=color, fill_opacity=opacity)
    return poly


def dot_point(name=None, x=0.0, y=0.0, color=CHALK_CYAN, size=20,
              label_dx=(0.0, 0.0), r=0.08):
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


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "A transversal cutting two parallel lines makes eight angles. <bookmark "
        "mark='b0'/>Those eight angles are linked by six relationships, "
        "<bookmark mark='b1'/>and those relationships turn a diagram into an "
        "equation."
    ),
    "s1": (
        "Two lines in the same plane that never meet are called parallel lines. "
        "<bookmark mark='b0'/>Here they are, with the same arrow mark on each. "
        "<bookmark mark='b1'/>A line that cuts across them is called a "
        "transversal. <bookmark mark='b2'/>It crosses both parallel lines and "
        "makes eight angles, four at each crossing. <bookmark mark='b3'/>The "
        "whole lesson lives in that one figure."
    ),
    "s2": (
        "At each crossing there are four angles, so the figure has eight angles "
        "in all. <bookmark mark='b0'/>We number them from one to eight, going "
        "around each crossing. <bookmark mark='b1'/>Angles three, four, five and "
        "six lie between the two parallel lines: these are the interior angles. "
        "<bookmark mark='b2'/>Angles one, two, seven and eight lie outside the "
        "lines: these are the exterior angles."
    ),
    "s3": (
        "Start at the upper crossing. <bookmark mark='b0'/>Angles one and four "
        "are vertically opposite, so they are equal. <bookmark mark='b1'/>Angles "
        "one and two lie side by side on the straight line, so they form a "
        "linear pair and add up to one hundred and eighty degrees. <bookmark "
        "mark='b2'/>The same is true at the lower crossing."
    ),
    "s4": (
        "Corresponding angles sit in the same position at the two crossings. "
        "<bookmark mark='b0'/>Angle one and angle five are both at the top left, "
        "so they correspond, and they are equal. <bookmark mark='b1'/>Angle two "
        "and angle six are both at the top right, so they are equal as well. "
        "<bookmark mark='b2'/>In the same way, angle three equals angle seven, "
        "and angle four equals angle eight."
    ),
    "s5": (
        "Now look between the parallel lines. <bookmark mark='b0'/>Angles four "
        "and five are on opposite sides of the transversal, so they are "
        "alternate interior angles, and they are equal. <bookmark mark='b1'/>"
        "Angles three and six are the other alternate interior pair, and they "
        "are equal too. <bookmark mark='b2'/>Alternate interior angles are "
        "always equal when the lines are parallel."
    ),
    "s6": (
        "One pair of interior angles behaves differently. <bookmark "
        "mark='b0'/>Angles three and five are on the same side of the "
        "transversal, between the parallel lines. <bookmark mark='b1'/>Because "
        "the lines are parallel, these same-side interior angles add up to one "
        "hundred and eighty degrees. <bookmark mark='b2'/>Angles four and six "
        "are the other such pair, and they also add up to one hundred and eighty "
        "degrees."
    ),
    "s7": (
        "The exterior angles have their own two rules. <bookmark mark='b0'/>"
        "Angles two and seven are on opposite sides of the transversal, outside "
        "the parallel lines: they are alternate exterior angles, and they are "
        "equal. <bookmark mark='b1'/>Angles one and eight are the other "
        "alternate exterior pair, and they are equal too. <bookmark "
        "mark='b2'/>Angles one and seven are on the same side, so they are "
        "same-side exterior angles, and they add up to one hundred and eighty "
        "degrees. <bookmark mark='b3'/>Angles two and eight do the same, so both "
        "exterior rules are now in place."
    ),
    "s8": (
        "This is why the rules matter: every one of them turns a diagram into an "
        "equation. <bookmark mark='b0'/>Step one: identify the pair. Angles three "
        "and five are same-side interior angles, so they add up to one hundred "
        "and eighty degrees. <bookmark mark='b1'/>Step two: read the measures off "
        "the diagram: three x plus twenty, and five x minus eight. <bookmark "
        "mark='b2'/>Step three: form the equation. Eight x plus twelve equals one "
        "hundred and eighty, so eight x is one hundred and sixty-eight. <bookmark "
        "mark='b3'/>Step four: solve, and x is twenty-one. <bookmark mark='b4'/>"
        "Step five: interpret. The angles are eighty-three degrees and "
        "ninety-seven degrees, and they do add up to one hundred and eighty."
    ),
    "s9": (
        "Let us use a second pair. <bookmark mark='b0'/>These two angles are in "
        "the same position at the two crossings, so they are corresponding "
        "angles, and corresponding angles are equal. <bookmark mark='b1'/>The "
        "diagram gives them as five x, and two x plus twenty-four. <bookmark "
        "mark='b2'/>Equal angles give an equation: five x equals two x plus "
        "twenty-four. Subtracting two x from both sides leaves three x equals "
        "twenty-four. <bookmark mark='b3'/>So x is eight. <bookmark mark='b4'/>"
        "Both angles are forty degrees, which is exactly what equal angles should "
        "be."
    ),
    "s9q": (
        "Your turn. Four quick checks. <bookmark mark='b0'/>First: this pair sit "
        "in the same position at the two crossings. Are they equal, or do they "
        "add up to one hundred and eighty? <bookmark mark='b1'/>Second: this "
        "pair lie between the parallel lines, on opposite sides of the "
        "transversal. <bookmark mark='b2'/>Third: this pair lie between the "
        "lines, on the same side. <bookmark mark='b3'/>And last of all: two "
        "corresponding angles are two x plus ten and three x minus thirty. Find "
        "x."
    ),
    "s9a": (
        "<bookmark mark='b0'/>The first pair are corresponding angles, so they "
        "are equal. <bookmark mark='b1'/>The second pair are alternate interior "
        "angles, so they are equal as well. <bookmark mark='b2'/>The third pair "
        "are same-side interior angles, so they add up to one hundred and eighty "
        "degrees. <bookmark mark='b3'/>And for the last one: two x plus ten "
        "equals three x minus thirty, so x is forty, and each angle is ninety "
        "degrees."
    ),
    "s10": (
        "One last look at all six relationships. <bookmark mark='b0'/>"
        "Corresponding angles are equal, <bookmark mark='b1'/>alternate interior "
        "angles are equal, and so are alternate exterior angles. <bookmark "
        "mark='b2'/>Vertically opposite angles are equal too. <bookmark "
        "mark='b3'/>Same-side interior angles add up to one hundred and eighty "
        "degrees, and same-side exterior angles do the same. <bookmark "
        "mark='b4'/>Geometry gives the rule, and the equation finds x. <bookmark "
        "mark='b5'/>Thank you for watching, <bookmark mark='b6'/>and see you in "
        "the next lesson."
    ),
}

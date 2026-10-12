"""Board furniture and narration for Storyboard 04 -- Understanding Angles:
Vertex, Arms, and Angle Regions, Class 6 Mathematics, Chapter 4 (Basic
Geometrical Ideas).

This file is *spliced*, never imported: assemble_angles.py grafts it into the
proven video-03 head of the Chapter 3 quadrilaterals set, so the theme names
(CHALK_*, FONT, BOARD_*), `board_text`, `chalk_math`, `appear` and the pacing
helpers (`rt`, `quick`, `leftover`) are already defined above it.

The furniture is this video's "open the door, build the angle" kit:

  * `ray_from`   -- one thick ray: a straight line with an arrowhead,
  * `arc_at`     -- the arc mark that shows the opening between the two rays,
  * `wedge_at`   -- the light fill of the angle marker between the arms,
  * `dot_point`  -- a labelled point (vertex, or a point in a region),
  * `mark_yes` / `mark_no` -- a drawn tick and cross (Segoe Print has neither),
  * `door_icon` / `clock_icon` -- the two everyday openings of scene 1.

Diagrams are drawn realistically: thick arrowed rays, a solid vertex dot with
its letter offset clear of the arms, a filled angle marker with its arc, and the
letters of region points placed so no letter ever sits on a ray.
"""
from __future__ import annotations

import numpy as np

# ------------------------------------------------------------ board layout --
# (this section is spliced into a head whose own imports omit Arc, Rotate and
#  Sector; Dot, Line, Arrow, Circle, Polygon, VGroup and np are already there)
from manim import Arc, Rotate, Sector  # noqa: E402,F401

# Board layout shared by every scene of this video.
ROW_Y = 2.72             # every scene heading sits on this line
SUB_Y = 2.16             # the one-line sub-heading under it
BANNER_Y = -1.34         # the closing banner, above the strip
# The angle scenes sit a little lower on the board than the heading grid alone
# would put them, so the figure, its banner and its strip read as one block.
FIG_DROP = 0.12
# The burned-in caption grows up from the bottom of the frame: a one-line cue
# starts at y = -3.38 and a wrapped two-line cue reaches y = -2.93 (measured on
# the burned caps), so every closing strip sits at -1.80 and nothing at all sits
# below CAPTION_SAFE_Y = -2.00 -- audited by the IN-CAPTION-BAND check.
STRIP_Y = -1.86
CAPTION_SAFE_Y = -2.00

PANEL_FILL = "#16202B"
RAY_W = 4.2              # stroke width of an arm (ray)
DOT_R = 0.078            # radius of a point dot

# The persistent angle O-A-B: one arm along the x axis, the other at 40 degrees,
# fixed so every scene draws the same opening.
O_PT = (-2.30, -0.97)
ANG_A = 40.0
ANG_B = 0.0
RAY_A_LEN = 3.30
RAY_B_LEN = 4.10
A_PT = (O_PT[0] + RAY_A_LEN * np.cos(np.radians(ANG_A)),
        O_PT[1] + RAY_A_LEN * np.sin(np.radians(ANG_A)))
B_PT = (O_PT[0] + RAY_B_LEN, O_PT[1])
A_LABEL = (A_PT[0] + 0.26, A_PT[1] + 0.20)
B_LABEL = (B_PT[0] + 0.24, B_PT[1] - 0.02)

MARK_R = 0.88            # radius of the angle marker (arc + light fill)

# Scene 1's two everyday openings, placed symmetrically about BOARD_CX (0.50),
# and the two columns of the challenge cards, so both are centred on the board.
DOOR_X = -2.20
CLOCK_X = 3.20
CARD_L = -2.75
CARD_R = 3.75


# ---------------------------------------------------------------- furniture --
def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


def chip(text, color=CHALK_CYAN, size=15, width=None, height=0.50):
    """A small labelled chip."""
    lab = board_text(text, size, color, "BOLD")
    box = RoundedRectangle(corner_radius=0.09,
                           width=width or (lab.width + 0.40), height=height,
                           stroke_color=color, stroke_width=1.7,
                           fill_color=PANEL_FILL, fill_opacity=0.7)
    lab.move_to(box.get_center())
    return VGroup(box, lab)


def card(title, lines, color=CHALK_WHITE, width=4.0, height=1.20,
         title_size=18, line_size=15):
    """A rounded card with a heading and one or two body lines."""
    head = board_text(title, title_size, color, "BOLD")
    body = VGroup(*[board_text(line, line_size, CHALK_WHITE, "BOLD")
                    for line in lines]).arrange(DOWN, buff=0.20)
    box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                           stroke_color=color, stroke_width=2.0,
                           fill_color=PANEL_FILL, fill_opacity=0.55)
    head.move_to(box.get_center() + UP * (height / 2 - 0.24))
    body.move_to(box.get_center() - DOWN * (0.18 if len(lines) > 1 else 0.12))
    return VGroup(box, head, body)


def dot_point(name=None, x=0.0, y=0.0, color=CHALK_CYAN, size=20,
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


def ray_from(start, degrees, length, color=CHALK_WHITE, width=RAY_W,
             tip=0.24):
    """One thick ray: a straight line from `start` with an arrowhead."""
    start = np.array([float(start[0]), float(start[1]), 0.0])
    end = start + np.array([np.cos(np.radians(degrees)),
                            np.sin(np.radians(degrees)), 0.0]) * float(length)
    return Arrow(start, end, buff=0.0, color=color, stroke_color=color,
                 stroke_width=width, tip_length=tip,
                 max_tip_length_to_length_ratio=0.30)


def arc_at(start, a1, a2, radius=MARK_R, color=CHALK_AMBER, width=2.8):
    """The arc that marks the opening between two ray directions."""
    arc = Arc(radius=radius, start_angle=np.radians(a1),
              angle=np.radians(a2 - a1), stroke_color=color,
              stroke_width=width)
    arc.shift(np.array([float(start[0]), float(start[1]), 0.0]))
    return arc


def wedge_at(start, a1, a2, radius=MARK_R, color=CHALK_CYAN, opacity=0.22):
    """The light fill of the angle marker between the arms."""
    sec = Sector(radius=radius, start_angle=np.radians(a1),
                 angle=np.radians(a2 - a1), stroke_width=0,
                 fill_color=color, fill_opacity=opacity)
    return sec.shift(np.array([float(start[0]), float(start[1]), 0.0]))


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


def door_icon(color=CHALK_AMBER, w=1.06, h=1.52):
    """A real door, ajar, drawn with Manim's own primitives.

    It has everything a door has: the frame it hangs in (two jambs and a
    lintel), the leaf itself standing in perspective -- the hinge edge full
    height, the free edge nearer the viewer and so shorter -- with its two
    raised panels, its knob and its hinges, the floor line under it, and the
    arc the leaf sweeps as it opens.  The angle between the leaf and the
    threshold is exactly the angle this scene is about.

    The leaf and its panels are Polygons (not Rectangles) so that the layout
    audit never reads a door part as a card with chalk drawn behind it."""
    hinge = np.array([0.0, 0.0, 0.0])
    left = Line(hinge + DOWN * 0.10 + LEFT * 0.06,
                hinge + UP * (h + 0.08) + LEFT * 0.06,
                stroke_color=color, stroke_width=5.0)
    right = Line(hinge + RIGHT * w + DOWN * 0.10,
                 hinge + RIGHT * w + UP * (h + 0.04),
                 stroke_color=color, stroke_width=5.0)
    lintel = Line(hinge + LEFT * 0.06 + UP * (h + 0.08),
                  hinge + RIGHT * w + UP * (h + 0.04),
                  stroke_color=color, stroke_width=5.0)
    frame = VGroup(left, right, lintel)
    threshold = Line(hinge, hinge + RIGHT * w, stroke_color=CHALK_WHITE,
                     stroke_width=1.8, stroke_opacity=0.45)
    p00 = hinge + DOWN * 0.06
    p01 = hinge + UP * (h - 0.02)
    p10 = hinge + RIGHT * (w * 0.60) + DOWN * 0.16
    p11 = hinge + RIGHT * (w * 0.60) + UP * (h - 0.26)
    panel = Polygon(p00, p10, p11, p01, stroke_color=CHALK_WHITE,
                    stroke_width=2.8, fill_color=color, fill_opacity=0.26)

    def inside(u, v):
        """Bilinear point inside the leaf, so its panels stay glued to it."""
        return (p00 * (1 - u) * (1 - v) + p10 * u * (1 - v)
                + p11 * u * v + p01 * (1 - u) * v)

    def panel_rect(u0, u1, v0, v1):
        return Polygon(inside(u0, v0), inside(u1, v0), inside(u1, v1),
                       inside(u0, v1), stroke_color=CHALK_WHITE,
                       stroke_width=1.4, stroke_opacity=0.70,
                       fill_color=CHALK_WHITE, fill_opacity=0.04)

    panels = VGroup(panel_rect(0.16, 0.84, 0.56, 0.86),
                    panel_rect(0.16, 0.84, 0.14, 0.44))
    knob = VGroup(
        Circle(radius=0.080, stroke_color=CHALK_WHITE, stroke_width=2.2,
               fill_color=PANEL_FILL, fill_opacity=0.90),
        Circle(radius=0.032, stroke_color=CHALK_WHITE, stroke_width=1.2,
               fill_color=CHALK_WHITE, fill_opacity=0.95))
    knob.move_to(inside(0.78, 0.50))
    hinges = VGroup()
    for v in (0.24, 0.76):
        hinge_tab = Rectangle(width=0.055, height=0.15, stroke_color=color,
                              stroke_width=1.6, fill_color=color,
                              fill_opacity=0.75)
        hinge_tab.move_to(inside(0.03, v))
        hinges.add(hinge_tab)
    leaf = VGroup(panel, panels, knob, hinges)
    floor = Line(hinge + LEFT * 0.34 + DOWN * 0.11,
                 hinge + RIGHT * (w + 0.34) + DOWN * 0.11,
                 stroke_color=CHALK_WHITE, stroke_width=1.5,
                 stroke_opacity=0.35)
    sweep = Arc(radius=w * 0.66, start_angle=-0.15, angle=np.radians(50.0),
                arc_center=hinge, stroke_color=color, stroke_width=2.2)
    # The angle itself: a translucent wedge between the leaf and the threshold
    # with its arc drawn on top, so the opening the door makes is unmistakable.
    wedge = Sector(radius=w * 0.42, start_angle=0.0, angle=np.radians(44.0),
                   stroke_width=0, fill_color=CHALK_CYAN, fill_opacity=0.32,
                   arc_center=hinge)
    opening = Arc(radius=w * 0.42, start_angle=0.0, angle=np.radians(44.0),
                  arc_center=hinge, stroke_color=CHALK_YELLOW,
                  stroke_width=3.0)
    swing = VGroup(sweep, wedge, opening)
    grp = VGroup(frame, floor, threshold, swing, leaf)
    grp.frame = frame
    grp.threshold = threshold
    grp.swing = swing
    grp.leaf = leaf
    grp.hinge = hinge
    return grp


def clock_icon(color=CHALK_CYAN, r=0.66):
    """A real clock face: the rim, twelve hour marks, the two hands and the
    centre pin -- the textbook's second everyday angle."""
    rim = Circle(radius=r, stroke_color=color, stroke_width=3.0)
    face = Circle(radius=r * 0.90, stroke_color=color, stroke_width=1.0,
                  fill_color=PANEL_FILL, fill_opacity=0.55)
    marks = VGroup()
    for i in range(12):
        ang = np.radians(90.0 - i * 30.0)
        d = np.array([np.cos(ang), np.sin(ang), 0.0])
        marks.add(Line(d * (r * 0.78), d * (r * 0.90),
                       stroke_color=CHALK_WHITE,
                       stroke_width=2.6 if i % 3 == 0 else 1.3))
    pin = Dot(radius=0.038, color=CHALK_WHITE, fill_opacity=1.0)
    hand1 = Line(ORIGIN, UP * r * 0.52, stroke_color=CHALK_WHITE,
                 stroke_width=3.6)
    hand2 = Line(ORIGIN, RIGHT * r * 0.76, stroke_color=CHALK_YELLOW,
                 stroke_width=3.0)
    grp = VGroup(rim, face, marks, hand1, hand2, pin)
    grp.face = VGroup(rim, face, marks)
    grp.hand1 = hand1
    grp.hand2 = hand2
    return grp


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "An angle is made by two rays that start at the same point. <bookmark "
        "mark='b0'/>The common point is the vertex, and the two rays are the "
        "arms of the angle. <bookmark mark='b1'/>An angle also separates the "
        "plane into an interior, a boundary and an exterior."
    ),
    "s1": (
        "We see angles everywhere. <bookmark mark='b0'/>Think of a door: as it "
        "opens, the space between the door and the frame grows wider. <bookmark "
        "mark='b1'/>Now think of the hands of a clock: as they move apart, they "
        "also make an angle. <bookmark mark='b2'/>If we keep only the two "
        "directions, we are left with two rays starting at one point."
    ),
    "s2": (
        "Let us build that angle. <bookmark mark='b0'/>Start with a point O, and "
        "draw one ray from it, ray OB. <bookmark mark='b1'/>Now draw a second "
        "ray from the same point O: ray OA. <bookmark mark='b2'/>The opening "
        "between them is the angle, and we write it as angle AOB. Two rays with "
        "a common endpoint make an angle."
    ),
    "s3": (
        "Every angle has two named parts. <bookmark mark='b0'/>The common "
        "endpoint is the vertex, so here the vertex is O. <bookmark "
        "mark='b1'/>The two rays are the arms: ray OA is one arm, <bookmark "
        "mark='b2'/>and ray OB is the other. The arms are also called the sides "
        "of the angle."
    ),
    "s4": (
        "Now the naming rule. <bookmark mark='b0'/>With three letters, the "
        "vertex must be the middle letter: angle AOB is correct. <bookmark "
        "mark='b1'/>Angle BOA is also correct, because O is still in the "
        "middle. <bookmark mark='b2'/>But angle OAB has A in the middle, and "
        "angle ABO has B in the middle. <bookmark mark='b3'/>Those are not "
        "names of this angle, because the vertex O is not in the middle."
    ),
    "s5": (
        "Notice that angle AOB and angle BOA name the same angle. <bookmark "
        "mark='b0'/>Reading the arms in the other order does not change the "
        "opening. <bookmark mark='b1'/>And when there is only one angle at O, we "
        "may name it simply as angle O."
    ),
    "s6": (
        "An angle divides the plane around it. <bookmark mark='b0'/>The region "
        "between the two arms is called the interior of the angle. <bookmark "
        "mark='b1'/>A point X that lies between the arms is in the interior. "
        "<bookmark mark='b2'/>The interior follows the arms outward, however far "
        "they are extended."
    ),
    "s7": (
        "What about the arms themselves? <bookmark mark='b0'/>A point S on one "
        "of the arms lies on the angle itself; the arms are its boundary. "
        "<bookmark mark='b1'/>A point Z outside the opening is in the exterior. "
        "<bookmark mark='b2'/>So an angle separates the plane into three parts: "
        "interior, boundary and exterior."
    ),
    "s8": (
        "Let us sort three points on one angle. <bookmark mark='b0'/>Here is "
        "angle PQR, with its vertex at Q. <bookmark mark='b1'/>Point N lies on "
        "an arm, so it is on the boundary. <bookmark mark='b2'/>Point M is "
        "between the arms, so it is in the interior, and point T is outside, in "
        "the exterior."
    ),
    "s9q": (
        "Your turn. Four quick checks. <bookmark mark='b0'/>First: in angle COD, "
        "name the vertex and the two arms. <bookmark mark='b1'/>Second: this "
        "angle has vertex Q. Give two valid three-letter names. <bookmark "
        "mark='b2'/>Third: point M, point N and point T. <bookmark mark='b3'/>"
        "And last of all: which of these names is wrong?"
    ),
    "s9a": (
        "<bookmark mark='b0'/>In angle COD the vertex is O, and the arms are OC "
        "and OD. <bookmark mark='b1'/>For the second: angle AQB and angle BQA, "
        "because the vertex Q stays in the middle. <bookmark mark='b2'/>And "
        "point M is in the interior, point N is on the boundary, and point T is "
        "in the exterior. <bookmark mark='b3'/>The wrong name is angle ABO, "
        "because its middle letter is B and not the vertex O."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>Two rays with a common endpoint make "
        "an angle. <bookmark mark='b1'/>That common endpoint is the vertex, and "
        "the two rays are the arms. <bookmark mark='b2'/>When you name an angle "
        "with three letters, the vertex goes in the middle. <bookmark "
        "mark='b3'/>And the angle separates the plane into its interior, its "
        "boundary and its exterior. <bookmark mark='b4'/>Build, name, locate. "
        "<bookmark mark='b5'/>Thank you for watching, <bookmark mark='b6'/>and "
        "see you in the next lesson."
    ),
}

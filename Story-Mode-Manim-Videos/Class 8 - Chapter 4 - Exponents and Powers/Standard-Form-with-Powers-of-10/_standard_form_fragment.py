"""Board furniture and narration for Storyboard 05 -- Standard Form with Powers
of 10: Writing Very Large and Very Small Numbers (Class 8 Mathematics,
Chapter 4: Exponents and Powers, the closing video of the five-part sequence).

This file is *spliced*, never imported: assemble_standard_form.py grafts it into
the proven video-03 head of the Chapter 3 quadrilaterals set, so the theme names
(CHALK_*, FONT, BOARD_*), `board_text`, `chalk_math` and the pacing helpers
(`rt`, `quick`, `leftover`) are already defined above it.

The visual identity is the DECIMAL-POINT ELEVATOR: a numeral laid out slot by
slot on a place-value track, with a bright decimal marker that travels one slot
at a time while a counter ticks off the places -- so the exponent is *counted*,
never announced.

Furniture:

  * `decimal_slots` -- a numeral laid out on a fixed pitch, so the marker has
                       somewhere to travel to; the "." in the string marks where
                       the marker starts,
  * `deci_marker`   -- the travelling decimal point,
  * `card`          -- a rounded chalk card wrapped snugly around one expression,
  * `law_card`      -- a card holding one expression plus its one-line rule,
  * `chip`          -- a small labelled chip,
  * `scale_marks`   -- the powers-of-ten scale ruler of scene 2,
  * `q_card`        -- one challenge question card,
  * `answer_row`    -- one revealed challenge answer.

The file has two splice markers, a board-layout section (constants plus the
furniture helpers) and the narration table; assemble_standard_form.py cuts
between them.
"""
from __future__ import annotations

import numpy as np

from manim import (
    DOWN, LEFT, RIGHT, UP, Dot, Line, RoundedRectangle, VGroup,
)

# ------------------------------------------------------------ board layout --
from manim import Ellipse  # noqa: E402  (the base head does not import it)

# Board layout shared by every scene of this video.
ROW_Y = 2.72             # every scene heading sits on this line
BANNER_Y = -1.30         # the closing banner, above the strip
# The burned-in caption grows up from the bottom of the frame: a one-line cue
# starts at y = -3.38 and a wrapped two-line cue reaches y = -2.93 (measured on
# the series' own burned 360p cuts), so every closing strip sits at -1.80 and
# nothing at all sits below y = -2.00 -- audited by the IN-CAPTION-BAND check.
STRIP_Y = -1.80

PANEL_FILL = "#16202B"
TRACK_PITCH = 0.46       # one place on the decimal elevator
TRACK_Y = 0.95           # where the numeral itself is laid out
COUNT_Y = 1.78           # where the place counter sits, above the numeral


# ---------------------------------------------------------------- furniture --
def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


def decimal_slots(digits, point_pos, y=0.95, pitch=TRACK_PITCH, size=34,
                  color=CHALK_WHITE, cx=None):
    """Lay a numeral out digit by digit along a place-value track.

    `point_pos` is how many digits sit LEFT of the decimal point to begin with
    (9 for 300000000, 1 for 0.000003).  The point itself is not a glyph -- it is
    the travelling marker -- so the marker has somewhere honest to walk to:
    `positions[p]` is the x of the point when p digits are in front of it.
    """
    cx = BOARD_CX if cx is None else cx
    n = len(digits)
    xs = [cx - (n - 1) * pitch / 2.0 + i * pitch for i in range(n)]
    glyphs = VGroup(*[chalk_math(ch, size=size, color=color).move_to(
        np.array([x, y, 0.0])) for ch, x in zip(digits, xs)])
    grp = VGroup(glyphs)
    grp.xs = xs
    grp.glyphs = list(glyphs)
    grp.positions = ([xs[0] - pitch / 2.0]
                     + [xs[i] + pitch / 2.0 for i in range(n)])
    grp.point_pos = point_pos
    return grp


def deci_marker(x, y, color=CHALK_RED, radius=0.065):
    """The travelling decimal point."""
    return Dot(radius=radius, color=color).move_to(np.array([x, y, 0.0]))


def card(mob, color=CHALK_WHITE, pad_x=0.54, pad_y=0.36, fill=0.55,
         stroke=1.9):
    """A rounded chalk card wrapped snugly around one expression."""
    box = RoundedRectangle(corner_radius=0.10, width=mob.width + pad_x,
                           height=mob.height + pad_y, stroke_color=color,
                           stroke_width=stroke, fill_color=PANEL_FILL,
                           fill_opacity=fill)
    mob.move_to(box.get_center())
    grp = VGroup(box, mob)
    grp.body = mob
    return grp


def law_card(maths, note, color=CHALK_CYAN, width=4.2, height=1.35,
             note_size=14, math_up=0.30, note_down=0.34):
    """One dashboard cell: an expression, with its one-line rule underneath."""
    box = RoundedRectangle(corner_radius=0.12, width=width, height=height,
                           stroke_color=color, stroke_width=2.0,
                           fill_color=PANEL_FILL, fill_opacity=0.55)
    maths.move_to(box.get_center() + UP * math_up)
    note_mob = board_text(note, note_size, color, "BOLD")
    note_mob.move_to(box.get_center() + DOWN * note_down)
    return VGroup(box, maths, note_mob)


def chip(text, color=CHALK_CYAN, size=15, width=None, height=0.50):
    """A small labelled chip."""
    lab = board_text(text, size, color, "BOLD")
    box = RoundedRectangle(corner_radius=0.09,
                           width=width or (lab.width + 0.42), height=height,
                           stroke_color=color, stroke_width=1.7,
                           fill_color=PANEL_FILL, fill_opacity=0.7)
    lab.move_to(box.get_center())
    return VGroup(box, lab)


def sun(radius=0.30, body=CHALK_AMBER, ray=CHALK_YELLOW):
    """The Sun: a chalk disc with eight rays (300,000,000 m across)."""
    disc = Circle(radius=radius, stroke_color=ray, stroke_width=2.2,
                  fill_color=body, fill_opacity=0.9)
    rays = VGroup()
    for k in range(8):
        ang = k * np.pi / 4.0
        start = np.array([np.cos(ang), np.sin(ang), 0.0]) * (radius + 0.05)
        end = np.array([np.cos(ang), np.sin(ang), 0.0]) * (radius + 0.17)
        rays.add(Line(start, end, stroke_color=ray, stroke_width=2.8))
    return VGroup(rays, disc)


def chip_icon(size=0.60, body="#33424E", trace=CHALK_CYAN):
    """A computer chip: a body with legs and one highlighted wire across it
    (the wire that is 0.000003 m across).  (The labelled `chip` helper above is
    a different thing -- a small caption box.)"""
    box = RoundedRectangle(corner_radius=0.07, width=size, height=size,
                           stroke_color=CHALK_WHITE, stroke_width=2.0,
                           fill_color=body, fill_opacity=0.9)
    legs = VGroup()
    for i in range(3):
        off = (i - 1) * size / 3.0
        legs.add(Line(np.array([-size / 2 - 0.13, off, 0.0]),
                      np.array([-size / 2, off, 0.0]),
                      stroke_color=CHALK_WHITE, stroke_width=2.0))
        legs.add(Line(np.array([size / 2, off, 0.0]),
                      np.array([size / 2 + 0.13, off, 0.0]),
                      stroke_color=CHALK_WHITE, stroke_width=2.0))
    wire = Line(np.array([-size / 2, -size / 6.0, 0.0]),
                np.array([size / 2, -size / 6.0, 0.0]), color=trace,
                stroke_width=3.6)
    return VGroup(box, legs, wire)


def plant_cell(w=0.98, h=0.74, wall=CHALK_GREEN, fill="#17301F"):
    """A plant cell: wall, nucleus, vacuole and a few organelles
    (0.00001275 m across)."""
    outer = RoundedRectangle(corner_radius=0.15, width=w, height=h,
                             stroke_color=wall, stroke_width=2.6,
                             fill_color=fill, fill_opacity=0.9)
    inner = RoundedRectangle(corner_radius=0.13, width=w - 0.10,
                             height=h - 0.10, stroke_color=wall,
                             stroke_width=1.3)
    nucleus = Circle(radius=0.105, stroke_color=CHALK_PINK, stroke_width=1.8,
                     fill_color=CHALK_PINK, fill_opacity=0.55
                     ).move_to(np.array([-0.17, 0.09, 0.0]))
    vacuole = Ellipse(width=0.34, height=0.24, stroke_color=CHALK_CYAN,
                      stroke_width=1.5, fill_color=CHALK_CYAN,
                      fill_opacity=0.25).move_to(np.array([0.17, -0.08, 0.0]))
    dots = VGroup(*[Dot(radius=0.026, color=CHALK_YELLOW).move_to(p)
                    for p in ((0.24, 0.17, 0.0), (-0.29, -0.15, 0.0),
                              (0.02, -0.24, 0.0))])
    return VGroup(outer, inner, nucleus, vacuole, dots)


def scale_marks(ks, y=0.90, dy=0.45, step=1.35, size=22, value_size=16,
                small=CHALK_PINK, large=CHALK_GREEN):
    """The powers-of-ten scale ruler: one tick per exponent, value beneath."""
    axis = Line(np.array([BOARD_CX - 3 * step - 0.70, y, 0.0]),
                np.array([BOARD_CX + 3 * step + 0.70, y, 0.0]),
                color=CHALK_WHITE, stroke_width=2.2)
    ticks, labels = VGroup(), VGroup()
    for i, k in enumerate(ks):
        x = BOARD_CX + k * step
        ticks.add(Line(np.array([x, y - 0.13, 0.0]),
                       np.array([x, y + 0.13, 0.0]), color=CHALK_WHITE,
                       stroke_width=2.4))
        col = large if k > 0 else (CHALK_WHITE if k == 0 else small)
        labels.add(chalk_math(f"10^{{{k}}}", size=size, color=col).move_to(
            np.array([x, y + dy, 0.0])))
        val = {0: "1", 1: "10", 2: "100", 3: "1000", -1: "1/10",
               -2: "1/100", -3: "1/1000"}[k]
        labels.add(chalk_math(val, size=value_size, color=CHALK_WHITE).move_to(
            np.array([x, y - dy, 0.0])))
    grp = VGroup(axis, ticks, labels)
    grp.axis = axis
    grp.ticks = ticks
    grp.labels = labels
    return grp


def q_card(title, body, color=CHALK_CYAN, width=3.7, height=0.92,
           head_up=0.28, body_down=0.22):
    """One 'your turn' question card: the prompt over the expression."""
    head = board_text(title, 13, color, "BOLD")
    box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                           stroke_color=color, stroke_width=1.9,
                           fill_color=PANEL_FILL, fill_opacity=0.55)
    head.move_to(box.get_center() + UP * head_up)
    body.move_to(box.get_center() + DOWN * body_down)
    return VGroup(box, head, body)


def answer_row(tag, maths, note, color, width=8.0, height=0.70):
    """One revealed answer: its letter, the expression and a short note."""
    lab = board_text(tag, 17, color, "BOLD")
    txt = board_text(note, 16, CHALK_WHITE, "BOLD")
    row = VGroup(lab, maths, txt).arrange(RIGHT, buff=0.40)
    box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                           stroke_color=color, stroke_width=1.8,
                           fill_color=PANEL_FILL, fill_opacity=0.6)
    row.move_to(box.get_center())
    return VGroup(box, row)


# ---------------------------------------------------------------- narration --
# About four minutes of speech at the series' rate (roughly 2.6 words a second),
# plus the ten-second challenge clock, the ten transition holds and the closing
# hold.
NARRATION = {
    "title": (
        "Standard form with powers of ten. <bookmark mark='b0'/>Among all the "
        "exponent laws, this one is the most useful in science: it writes very "
        "large and very small numbers compactly. <bookmark mark='b1'/>Move the "
        "decimal point, count the places, and write the power of ten."
    ),
    "s1": (
        "Standard form begins with two extremes. <bookmark mark='b0'/>The Sun "
        "is about three hundred million metres away. <bookmark mark='b1'/>A "
        "wire inside a computer chip is about zero point zero zero zero zero "
        "zero three metres across. <bookmark mark='b2'/>Powers of ten write "
        "both: three times ten to the power eight, and three times ten to the "
        "power minus six."
    ),
    "s2": (
        "Powers of ten are really a scale. <bookmark mark='b0'/>Ten to the "
        "power zero is one, in the middle. <bookmark mark='b1'/>To the right "
        "the numbers grow: ten, one hundred, one thousand. <bookmark "
        "mark='b2'/>To the left they shrink below one: one tenth, one "
        "hundredth, one thousandth. <bookmark mark='b3'/>So a positive "
        "exponent means a large scale, and a negative exponent means a small "
        "scale."
    ),
    "s3": (
        "Now convert a large number: three hundred million. <bookmark "
        "mark='b0'/>The decimal point sits at the right-hand end. <bookmark "
        "mark='b1'/>Move it left, one place at a time, until a single non-zero "
        "digit stands in front of it: that is eight places. <bookmark "
        "mark='b2'/>So three hundred million is three times ten to the power "
        "eight."
    ),
    "s4": (
        "Here is a second large number: six thousand and twenty million. "
        "<bookmark mark='b0'/>Again the decimal point begins at the right-hand "
        "end. <bookmark mark='b1'/>Move it left until only one non-zero digit "
        "stands in front: <bookmark mark='b2'/>one, <bookmark mark='b3'/>two, "
        "<bookmark mark='b4'/>three, <bookmark mark='b5'/>four, <bookmark "
        "mark='b6'/>five, <bookmark mark='b7'/>six, <bookmark mark='b8'/>seven, "
        "<bookmark mark='b9'/>eight, <bookmark mark='b10'/>nine places. "
        "<bookmark mark='b11'/>The digits we keep are six, zero, two. "
        "<bookmark mark='b12'/>So the number is six point zero two times ten "
        "to the power nine."
    ),
    "s5": (
        "Now a very small number: the wire inside a chip is zero point zero "
        "zero zero zero zero three metres across. <bookmark mark='b0'/>This "
        "time the decimal point starts at the left. <bookmark mark='b1'/>Move "
        "it right until only one non-zero digit stands in front: that is six "
        "places, and the digit is three. <bookmark mark='b2'/>Because we moved "
        "right, into a number that was smaller than one, the exponent is "
        "negative: three times ten to the power minus six."
    ),
    "s6": (
        "A plant cell is even more interesting: it is zero point zero zero "
        "zero zero one two seven five metres across. <bookmark mark='b0'/>The "
        "significant digits are one, two, seven and five, and they do not "
        "change. <bookmark mark='b1'/>Move the decimal point right: <bookmark "
        "mark='b2'/>one, <bookmark mark='b3'/>two, <bookmark mark='b4'/>three, "
        "<bookmark mark='b5'/>four, <bookmark mark='b6'/>five places. "
        "<bookmark mark='b7'/>So the standard form is one point two seven five "
        "times ten to the power minus five. The quantity is the same; only the "
        "way we write it has changed."
    ),
    "s7": (
        "Now the other direction: from standard form back to usual form. "
        "<bookmark mark='b0'/>Four point six seven times ten to the power "
        "four: the exponent is positive, so the decimal point moves right four "
        "places, giving forty six thousand seven hundred. <bookmark "
        "mark='b1'/>Three point zero two times ten to the power minus six: the "
        "exponent is negative, so the decimal point moves left six places, "
        "giving zero point zero zero zero zero zero three zero two. <bookmark "
        "mark='b2'/>These directions are for going back to usual form; making "
        "standard form moves the decimal the other way."
    ),
    "s8": (
        "Here is the complete map. <bookmark mark='b0'/>A large number in "
        "usual form moves its decimal point left and takes a positive "
        "exponent. <bookmark mark='b1'/>A small number moves its decimal point "
        "right and takes a negative exponent. <bookmark mark='b2'/>Coming back "
        "from standard form the movements reverse: a positive exponent moves "
        "the decimal right, and a negative exponent moves it left. Always ask "
        "which direction you are converting."
    ),
    "s9q": (
        "Your turn. <bookmark mark='b0'/>Three conversions. Write zero point zero "
        "zero zero zero four five six in standard form. Write six thousand and twenty "
        "million in standard form. And write five point eight times ten to the power "
        "seven in usual form."
    ),
    "s9a": (
        "<bookmark mark='b0'/>For the first, the decimal moves right five places, so "
        "it is four point five six times ten to the power minus five. <bookmark "
        "mark='b1'/>For the second, the decimal moves left nine places: six point "
        "zero two times ten to the power nine. <bookmark mark='b2'/>And for the third "
        "the exponent is positive seven, so the decimal moves right seven places: "
        "fifty eight million."
    ),
    "s10": (
        "One last look at the whole idea. <bookmark mark='b0'/>Move the decimal "
        "point, count the places, choose the sign, and write times ten to the power: "
        "three hundred million is three times ten to the power eight. <bookmark "
        "mark='b1'/>And zero point zero zero zero zero zero three is three times ten "
        "to the power minus six. <bookmark mark='b2'/>Powers of ten let us write the "
        "very large and the very small compactly. <bookmark mark='b3'/>Thank you for "
        "watching the chapter, <bookmark mark='b4'/>and see you in the next lesson."
    ),
}





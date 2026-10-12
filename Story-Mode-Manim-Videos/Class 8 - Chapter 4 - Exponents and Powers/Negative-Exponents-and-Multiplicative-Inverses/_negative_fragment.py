"""Board furniture and narration for Storyboard 02 -- Understanding Negative
Exponents: Reciprocal Rules and Multiplicative Inverses (Class 8 Mathematics,
Chapter 4: Exponents and Powers).

This file is *spliced*, never imported: assemble_negative.py grafts it into the
proven video-03 head of the Chapter 3 quadrilaterals set, so the theme names
(CHALK_*, FONT, BOARD_*), `board_text`, `chalk_math` and the pacing helpers
(`rt`, `quick`, `leftover`) are already defined above it.

The furniture is this video's two persistent visuals:

  * `staircase`   -- the Exponent Staircase: one row per power, indented as it
                     descends, so a step down is visible as a step,
  * `card`        -- a rounded chalk card wrapped snugly around one expression
                     (the staircase steps, the rule, the mirror halves),
  * `divider_box` -- the "÷10 each step" / "÷2 each step" note beside the
                     staircase (the base changes with the staircase, safeguard G),
  * `mirror`      -- the Reciprocal Mirror: a dashed vertical axis with a label,
  * `q_card`      -- one challenge question card,
  * `answer_row`  -- one revealed challenge answer,
  * `sun`         -- the stylised Sun recalled from storymode 01,
  * `number_line` -- the "below 1" line of the opening scene.

The file has two splice markers, a board-layout section (constants plus the
furniture helpers) and the narration table; assemble_negative.py cuts between
them.
"""
from __future__ import annotations

import numpy as np

from manim import (
    DOWN, LEFT, RIGHT, UP, Circle, DashedLine, Line, MathTex,
    RoundedRectangle, VGroup,
)

# ------------------------------------------------------------ board layout --
# Board layout shared by every scene of this video.
ROW_Y = 2.72             # every scene heading sits on this line
SUB_Y = 2.20             # the one-line sub-heading under it
BANNER_Y = -1.25         # the closing banner, above the strip
# The burned-in caption grows up from the bottom of the frame: a one-line cue
# starts at y = -3.38 and a wrapped two-line cue reaches y = -2.93 (measured on
# the series' own burned 360p cuts), so every closing strip sits at -1.80 and
# nothing at all sits below y = -2.00 -- audited by the IN-CAPTION-BAND check.
STRIP_Y = -1.80

PANEL_FILL = "#16202B"


# ---------------------------------------------------------------- furniture --
def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


def card(mob, color=CHALK_WHITE, pad_x=0.52, pad_y=0.36, fill=0.55,
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


def chip(text, color=CHALK_CYAN, size=15, width=None, height=0.52):
    """A small labelled chip."""
    lab = board_text(text, size, color, "BOLD")
    box = RoundedRectangle(corner_radius=0.09,
                           width=width or (lab.width + 0.42), height=height,
                           stroke_color=color, stroke_width=1.7,
                           fill_color=PANEL_FILL, fill_opacity=0.7)
    lab.move_to(box.get_center())
    return VGroup(box, lab)


def staircase(rows, x0=1.35, y0=1.60, dy=0.58, dx=-0.42, size=26,
              color=CHALK_WHITE):
    """The Exponent Staircase: one row per power, indented as it descends."""
    mobs = [chalk_math(r, size=size, color=color) for r in rows]
    for i, m in enumerate(mobs):
        m.move_to(np.array([x0 + i * dx, y0 - i * dy, 0.0]))
    grp = VGroup(*mobs)
    grp.rows = mobs
    return grp


def divider_box(lines, color=CHALK_YELLOW, width=1.35, height=1.05,
                size=15):
    """The 'one step down' note beside a staircase (base-aware: 10 or 2)."""
    body = VGroup(*[board_text(l, size, color, "BOLD")
                    for l in lines]).arrange(DOWN, buff=0.24)
    box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                           stroke_color=color, stroke_width=1.8,
                           fill_color=PANEL_FILL, fill_opacity=0.7)
    body.move_to(box.get_center())
    return VGroup(box, body)


def down_arrow(x, y_top, y_bottom, color=CHALK_CYAN, width=3.0):
    """A tall thin arrow showing which way the staircase descends."""
    from manim import Arrow
    return Arrow(np.array([x, y_top, 0.0]), np.array([x, y_bottom, 0.0]),
                 buff=0, stroke_width=width, color=color,
                 max_tip_length_to_length_ratio=0.10)


def mirror(x, y_top, y_bottom, color=CHALK_CYAN):
    """The Reciprocal Mirror axis, with its label pinned above it."""
    axis = DashedLine(np.array([x, y_top, 0.0]), np.array([x, y_bottom, 0.0]),
                      color=color, stroke_width=2.6, dash_length=0.13)
    label = board_text("RECIPROCAL MIRROR", 15, color, "BOLD")
    label.next_to(axis, UP, buff=0.12)
    return VGroup(axis, label)


def q_card(title, body, color=CHALK_CYAN, width=3.7, height=0.92):
    """One 'your turn' question card: the prompt over the expression."""
    head = board_text(title, 14, color, "BOLD")
    box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                           stroke_color=color, stroke_width=1.9,
                           fill_color=PANEL_FILL, fill_opacity=0.55)
    head.move_to(box.get_center() + UP * 0.24)
    body.move_to(box.get_center() + DOWN * 0.22)
    return VGroup(box, head, body)


def answer_row(tag, maths, note, color, width=7.6, height=0.70):
    """One revealed answer: its letter, the expression and a short note."""
    lab = board_text(tag, 17, color, "BOLD")
    txt = board_text(note, 16, CHALK_WHITE, "BOLD")
    row = VGroup(lab, maths, txt).arrange(RIGHT, buff=0.40)
    box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                           stroke_color=color, stroke_width=1.8,
                           fill_color=PANEL_FILL, fill_opacity=0.6)
    row.move_to(box.get_center())
    return VGroup(box, row)


def sun(radius=0.50, body=CHALK_AMBER, ray=CHALK_YELLOW):
    """The stylised Sun recalled from storymode 01."""
    disc = Circle(radius=radius, stroke_color=ray, stroke_width=2.2,
                  fill_color=body, fill_opacity=0.9)
    rays = VGroup()
    for k in range(8):
        ang = k * np.pi / 4.0
        start = np.array([np.cos(ang), np.sin(ang), 0.0]) * (radius + 0.08)
        end = np.array([np.cos(ang), np.sin(ang), 0.0]) * (radius + 0.24)
        rays.add(Line(start, end, stroke_color=ray, stroke_width=2.6))
    return VGroup(rays, disc)


def number_line(y, x_left=-2.60, x_right=3.60, tick_x=0.50):
    """The 'below 1' line: a tick at 1, bigger to the right, smaller left."""
    axis = Line(np.array([x_left, y, 0.0]), np.array([x_right, y, 0.0]),
                color=CHALK_WHITE, stroke_width=2.2)
    tick = Line(np.array([tick_x, y - 0.14, 0.0]),
                np.array([tick_x, y + 0.14, 0.0]), color=CHALK_WHITE,
                stroke_width=2.4)
    one = board_text("1", 17, CHALK_WHITE, "BOLD")
    one.next_to(tick, UP, buff=0.10)
    big = board_text("bigger  \u2192", 15, CHALK_GREEN, "BOLD")
    big.next_to(axis, RIGHT, buff=0.16)
    small = board_text("\u2190  smaller", 15, CHALK_PINK, "BOLD")
    small.next_to(axis, LEFT, buff=0.16)
    return VGroup(axis, tick, one, big, small)


# ---------------------------------------------------------------- narration --
# About three and a half minutes of speech at the series' rate (roughly 2.6 words
# a second), plus the ten-second challenge clock, the ten transition holds and
# the closing hold.
NARRATION = {
    "title": (
        "Negative exponents. <bookmark mark='b0'/>A negative power is not a "
        "negative number: it is a reciprocal. <bookmark mark='b1'/>Let us see "
        "where the minus sign really goes."
    ),
    "s1": (
        "Last time, exponents wrote the Sun's width as one point four times "
        "ten to the power nine. <bookmark mark='b0'/>Now look at something "
        "tiny: a human hair is about zero point zero zero zero zero zero five "
        "metres thick. <bookmark mark='b1'/>Can exponents take us below one? "
        "<bookmark mark='b2'/>We need a new kind of power."
    ),
    "s2": (
        "Start with the powers you already know. <bookmark mark='b0'/>Ten "
        "cubed is one thousand. Divide by ten and the exponent drops to two: "
        "one hundred. <bookmark mark='b1'/>Divide by ten again: ten to the "
        "power one is ten. And ten to the power zero is one. <bookmark "
        "mark='b2'/>Every step down divides the value by ten."
    ),
    "s3": (
        "But the staircase does not stop at one. <bookmark mark='b0'/>Keep the "
        "same rule: one divided by ten is one tenth, so ten to the power minus "
        "one. <bookmark mark='b1'/>One tenth divided by ten is one hundredth: "
        "ten to the power minus two. <bookmark mark='b2'/>And one thousandth "
        "is ten to the power minus three. <bookmark mark='b3'/>The minus sign "
        "moves the power under one."
    ),
    "s4": (
        "The pattern is not special to ten. <bookmark mark='b0'/>Try the base "
        "two: eight, four, two, one. <bookmark mark='b1'/>Each step divides by "
        "two. <bookmark mark='b2'/>So one divided by two is one half: two to "
        "the power minus one. And one quarter is two to the power minus two."
    ),
    "s5": (
        "Now we can write the rule for any base a that is not zero. <bookmark "
        "mark='b0'/>A raised to the power minus m equals one over a to the "
        "power m. <bookmark mark='b1'/>The exponent becomes positive in the "
        "denominator, and the minus sign disappears. <bookmark mark='b2'/>Read "
        "it the other way too: one over a to the power m equals a to the power "
        "minus m."
    ),
    "s6": (
        "Here is the mistake to avoid. <bookmark mark='b0'/>Two to the power "
        "minus three is one over two cubed, which is one eighth, a positive "
        "fraction. <bookmark mark='b1'/>But minus two cubed means minus eight. "
        "They are not equal. <bookmark mark='b2'/>The minus sign belongs to "
        "the exponent, so it takes the reciprocal."
    ),
    "s7": (
        "Now look in a mirror. <bookmark mark='b0'/>On the left, two cubed is "
        "eight. On the right, two to the power minus three is one eighth. "
        "<bookmark mark='b1'/>Multiply them: eight times one eighth is one. "
        "<bookmark mark='b2'/>In general, a to the power m times a to the "
        "power minus m is a to the power zero, which is one. <bookmark "
        "mark='b3'/>So each is the multiplicative inverse of the other."
    ),
    "s8": (
        "Finding an inverse is quick. <bookmark mark='b0'/>Three to the power "
        "minus five pairs with three to the power five, because their product "
        "is one. <bookmark mark='b1'/>Four to the power minus three pairs with "
        "four cubed. <bookmark mark='b2'/>And x to the power minus n pairs "
        "with x to the power n. <bookmark mark='b3'/>The inverse of any power "
        "simply flips the sign of its exponent."
    ),
    "s9q": (
        "Your turn. <bookmark mark='b0'/>Three questions. Write ten to the power "
        "minus four with a positive exponent. Find the value of five to the power "
        "minus two. Write the multiplicative inverse of seven to the power minus "
        "three."
    ),
    "s9a": (
        "<bookmark mark='b0'/>Ten to the power minus four is one over ten to the "
        "power four: one over ten thousand. <bookmark mark='b1'/> Five to the power "
        "minus two is one over five squared: one twenty fifth. <bookmark "
        "mark='b2'/>And the inverse of seven to the power minus three is seven cubed."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>When the exponent goes down by one, the "
        "value is divided by the base. <bookmark mark='b1'/>A negative exponent means "
        "the reciprocal: a to the power minus m is one over a to the power m. "
        "<bookmark mark='b2'/>And that reciprocal is the multiplicative inverse, "
        "because their product is always one. <bookmark mark='b3'/>Thank you for "
        "watching, <bookmark mark='b4'/>and see you in the next lesson."
    ),
}


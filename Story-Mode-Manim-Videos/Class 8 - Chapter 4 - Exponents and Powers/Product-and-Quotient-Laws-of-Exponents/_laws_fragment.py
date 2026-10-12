"""Board furniture and narration for Storyboard 03 -- Product & Quotient Laws of
Exponents: Multiplying and Dividing Powers with the Same Base (Class 8
Mathematics, Chapter 4: Exponents and Powers).

This file is *spliced*, never imported: assemble_laws.py grafts it into the
proven video-03 head of the Chapter 3 quadrilaterals set, so the theme names
(CHALK_*, FONT, BOARD_*), `board_text`, `chalk_math` and the pacing helpers
(`rt`, `quick`, `leftover`) are already defined above it.

The defining visual is the FACTOR BLOCK: every copy of the base is one identical
tile, and the same tiles are carried through the whole scene --

  * multiplication: the two groups physically slide together into one chain
    (JOIN -> ADD),
  * division: matching tiles above and below the fraction bar are slashed and
    removed in pairs (CANCEL -> SUBTRACT).

Furniture:

  * `tile`       -- one copy of the base as a labelled tile,
  * `tile_run`   -- n tiles in a row, returned with the individual tiles,
  * `cancel_mark`-- the red slash that removes a matched tile,
  * `frac_bar`   -- the quotient's fraction bar,
  * `card`       -- a rounded chalk card wrapped snugly around one expression,
  * `chip`       -- a small labelled chip,
  * `zone_card`  -- a titled panel holding a few stacked lines,
  * `q_card`     -- one challenge question card,
  * `answer_row` -- one revealed challenge answer.

The file has two splice markers, a board-layout section (constants plus the
furniture helpers) and the narration table; assemble_laws.py cuts between them.
"""
from __future__ import annotations

import numpy as np

from manim import (
    DOWN, LEFT, RIGHT, UP, Line, RoundedRectangle, VGroup,
)

# ------------------------------------------------------------ board layout --
# Board layout shared by every scene of this video.
ROW_Y = 2.72             # every scene heading sits on this line
SUB_Y = 2.20             # the one-line sub-heading under it
BANNER_Y = -1.30         # the closing banner, above the strip
# The burned-in caption grows up from the bottom of the frame: a one-line cue
# starts at y = -3.38 and a wrapped two-line cue reaches y = -2.93 (measured on
# the series' own burned 360p cuts), so every closing strip sits at -1.80 and
# nothing at all sits below y = -2.00 -- audited by the IN-CAPTION-BAND check.
STRIP_Y = -1.80

TILE_W = 0.42            # one factor block
TILE_H = 0.52
TILE_BUFF = 0.09
PANEL_FILL = "#16202B"


# ---------------------------------------------------------------- furniture --
def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


def tile(label, color=CHALK_WHITE, size=22, w=TILE_W, h=TILE_H, fill=0.55):
    """One copy of the base as a factor block."""
    lab = chalk_math(label, size=size, color=color)
    box = RoundedRectangle(corner_radius=0.06, width=w, height=h,
                           stroke_color=color, stroke_width=1.8,
                           fill_color=PANEL_FILL, fill_opacity=fill)
    lab.move_to(box.get_center())
    grp = VGroup(box, lab)
    grp.label = lab
    return grp


def tile_run(n, label="2", color=CHALK_WHITE, size=22, buff=TILE_BUFF):
    """`n` factor blocks in a row: returns (group, [tiles])."""
    tiles = [tile(label, color, size=size) for _ in range(n)]
    grp = VGroup(*tiles).arrange(RIGHT, buff=buff)
    grp.tiles = list(grp)
    return grp, list(grp)


def cancel_mark(target, color=CHALK_RED, width=3.4, pad=0.04):
    """The red slash that cancels one factor block."""
    a, b = target.get_corner(np.array([-1.0, -1.0, 0.0])), \
        target.get_corner(np.array([1.0, 1.0, 0.0]))
    a = a + np.array([-pad, -pad, 0.0])
    b = b + np.array([pad, pad, 0.0])
    return Line(a, b, color=color, stroke_width=width)


def frac_bar(x_left, x_right, y, color=CHALK_WHITE, width=2.6):
    """The fraction bar of a quotient."""
    return Line(np.array([x_left, y, 0.0]), np.array([x_right, y, 0.0]),
                color=color, stroke_width=width)


def mark_no(size=1.0, color=CHALK_RED):
    """A drawn chalk cross (the board font has no cross glyph)."""
    cross = VGroup(
        Line(np.array([-0.10, -0.10, 0.0]), np.array([0.10, 0.10, 0.0])),
        Line(np.array([-0.10, 0.10, 0.0]), np.array([0.10, -0.10, 0.0])),
    ).set_stroke(color=color, width=4.2)
    cross.scale(size)
    return cross


def card(mob, color=CHALK_WHITE, pad_x=0.54, pad_y=0.38, fill=0.55,
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


def chip(text, color=CHALK_CYAN, size=15, width=None, height=0.50):
    """A small labelled chip."""
    lab = board_text(text, size, color, "BOLD")
    box = RoundedRectangle(corner_radius=0.09,
                           width=width or (lab.width + 0.42), height=height,
                           stroke_color=color, stroke_width=1.7,
                           fill_color=PANEL_FILL, fill_opacity=0.7)
    lab.move_to(box.get_center())
    return VGroup(box, lab)


def zone_card(title, lines, color=CHALK_WHITE, width=4.2, height=2.60,
              title_size=18, line_size=30, note_size=16, note=None):
    """A titled panel holding the power, the arrow note and the result."""
    head = board_text(title, title_size, color, "BOLD")
    body = VGroup(*lines).arrange(DOWN, buff=0.26)
    box = RoundedRectangle(corner_radius=0.12, width=width, height=height,
                           stroke_color=color, stroke_width=2.0,
                           fill_color=PANEL_FILL, fill_opacity=0.55)
    head.move_to(box.get_center() + UP * (height / 2 - 0.30))
    if note is None:
        body.move_to(box.get_center() + DOWN * 0.20)
    else:
        note_mob = board_text(note, note_size, CHALK_YELLOW, "BOLD")
        stack = VGroup(body, note_mob).arrange(DOWN, buff=0.28)
        stack.move_to(box.get_center() + DOWN * 0.30)
        body = stack
    grp = VGroup(box, head, body)
    grp.body = body
    return grp


def q_card(title, body, color=CHALK_CYAN, width=3.7, height=0.92,
           head_up=0.24, body_down=0.22):
    """One 'your turn' question card: the prompt over the expression.

    `head_up` / `body_down` are opened up for a card whose expression is a
    fraction, so the taller math keeps its clearance from the card edge."""
    head = board_text(title, 14, color, "BOLD")
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
# About three and a half minutes of speech at the series' rate (roughly 2.6 words
# a second), plus the ten-second challenge clock, the ten transition holds and
# the closing hold.
NARRATION = {
    "title": (
        "The product and quotient laws of exponents. <bookmark mark='b0'/>When "
        "powers with the same base are multiplied, the exponents are added. "
        "<bookmark mark='b1'/>When they are divided, the exponents are "
        "subtracted."
    ),
    "s1": (
        "Suppose we want two to the power four, times two to the power three. "
        "<bookmark mark='b0'/>We could expand both: four twos, and then three "
        "more twos. <bookmark mark='b1'/>That is seven twos multiplied "
        "together, which is two to the power seven. <bookmark mark='b2'/>"
        "Expanding everything every time is slow. There must be a shortcut."
    ),
    "s2": (
        "Let us watch the factors instead. <bookmark mark='b0'/>Two to the "
        "power four is four tiles, and two to the power three is three tiles. "
        "<bookmark mark='b1'/>Multiply, and the two groups join into one chain "
        "of seven. <bookmark mark='b2'/>So four plus three gives the new "
        "exponent, seven. <bookmark mark='b3'/>For any base: a to the power m "
        "times a to the power n is a to the power m plus n."
    ),
    "s3": (
        "Does the same rule work when an exponent is negative? <bookmark "
        "mark='b0'/>Look at three squared times three to the power minus four. "
        "<bookmark mark='b1'/>The base is the same, so add the exponents: two "
        "plus minus four. <bookmark mark='b2'/>That is minus two, so the "
        "answer is three to the power minus two. <bookmark mark='b3'/>And from "
        "the last lesson, that is one over three squared, or one ninth."
    ),
    "s4": (
        "Now division. <bookmark mark='b0'/>Take a to the power seven over a "
        "to the power three: seven factors on top, three below. <bookmark "
        "mark='b1'/>Every factor below can cancel one on top. Three pairs "
        "cancel, leaving four factors. <bookmark mark='b2'/>So the exponent is "
        "seven minus three, which is four. <bookmark mark='b3'/>In general, a "
        "to the power m over a to the power n is a to the power m minus n."
    ),
    "s5": (
        "Let us use the textbook's example: four to the power seven over four "
        "to the power four. <bookmark mark='b0'/>The bases are the same. "
        "<bookmark mark='b1'/>Subtract the exponents, top minus bottom: seven "
        "minus four. <bookmark mark='b2'/>That is three, so the answer is four "
        "cubed. <bookmark mark='b3'/>And four cubed is sixty four."
    ),
    "s6": (
        "What if the bottom exponent is bigger? <bookmark mark='b0'/>Look at "
        "five squared over five to the power five. <bookmark mark='b1'/>The "
        "base is the same, so subtract: two minus five. <bookmark mark='b2'/>"
        "That is minus three, so the answer is five to the power minus three. "
        "<bookmark mark='b3'/>A negative exponent is a perfectly good answer: "
        "it is one over five cubed, which is one over one hundred and twenty "
        "five."
    ),
    "s7": (
        "Now put the two laws side by side. <bookmark mark='b0'/>For a "
        "product, the factor groups join, so the exponents are added: a to the "
        "power m times a to the power n is a to the power m plus n. <bookmark "
        "mark='b1'/>For a quotient, matching factors cancel, so the exponents "
        "are subtracted: a to the power m over a to the power n is a to the "
        "power m minus n. <bookmark mark='b2'/>In both laws the base stays "
        "exactly the same."
    ),
    "s8": (
        "Here are three mistakes to avoid. <bookmark mark='b0'/>First: x to "
        "the power minus three times x to the power minus two is x to the "
        "power minus five, not minus six. <bookmark mark='b1'/>Second: two "
        "cubed times three to the fourth has different bases, so the exponents "
        "cannot be added. <bookmark mark='b2'/>Third: a squared over a to the "
        "power five is a to the power minus three, not a cubed. <bookmark "
        "mark='b3'/>Read the operation carefully."
    ),
    "s9q": (
        "Your turn. <bookmark mark='b0'/>Three questions. Simplify two to the power "
        "minus three times two to the power minus two. Simplify seven to the power "
        "minus two times seven to the power five. And simplify four to the power "
        "seven over four to the power four."
    ),
    "s9a": (
        "<bookmark mark='b0'/>For the first, the exponents add: minus three plus "
        "minus two is minus five, so two to the power minus five. <bookmark "
        "mark='b1'/>For the second, minus two plus five is three, so seven cubed. "
        "<bookmark mark='b2'/>And for the third, seven minus four is three, so four "
        "cubed, which is sixty four."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>When powers with the same base are "
        "multiplied, the factor groups join, so the exponents are added. <bookmark "
        "mark='b1'/>When they are divided, matching factors cancel, so the exponents "
        "are subtracted. <bookmark mark='b2'/>Keep the base, and remember: "
        "multiplication adds, division subtracts. <bookmark mark='b3'/>Thank you for "
        "watching, <bookmark mark='b4'/>and see you in the next lesson."
    ),
}



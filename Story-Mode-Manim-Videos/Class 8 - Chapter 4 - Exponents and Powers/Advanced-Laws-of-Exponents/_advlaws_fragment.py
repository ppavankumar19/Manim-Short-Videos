"""Board furniture and narration for Storyboard 04 -- Advanced Laws of
Exponents: Power of a Power, Product & Fraction Rules, and Zero Exponent
(Class 8 Mathematics, Chapter 4: Exponents and Powers).

This file is *spliced*, never imported: assemble_advanced_laws.py grafts it into
the proven video-03 head of the Chapter 3 quadrilaterals set, so the theme names
(CHALK_*, FONT, BOARD_*), `board_text`, `chalk_math` and the pacing helpers
(`rt`, `quick`, `leftover`) are already defined above it.

The visual identity is "the exponent knows what is inside the brackets":

  * power of a power -- the outer exponent duplicates the WHOLE group, and the
    group count times the factors per group gives `mn`;
  * power of a product -- the exponent splits horizontally onto both factors;
  * power of a fraction -- the exponent splits vertically, top and bottom;
  * zero exponent -- the same factor blocks that cancelled in storymode 03
    cancel again, leaving `1`.

Furniture:

  * `tile` / `tile_run` -- one factor block / a row of them,
  * `cancel_mark`       -- the red slash that removes a matched factor,
  * `frac_bar`          -- a quotient's fraction bar,
  * `card`              -- a rounded chalk card wrapped snugly around one
                           expression,
  * `law_card`          -- a card holding one law plus its one-line rule,
  * `chip`              -- a small labelled chip,
  * `q_card`            -- one challenge question card,
  * `answer_row`        -- one revealed challenge answer,
  * `mark_no`           -- a drawn chalk cross (the font has no cross glyph).

The file has two splice markers, a board-layout section (constants plus the
furniture helpers) and the narration table; assemble_advanced_laws.py cuts
between them.
"""
from __future__ import annotations

import numpy as np

from manim import (
    DOWN, LEFT, RIGHT, UP, Line, RoundedRectangle, VGroup,
)

# ------------------------------------------------------------ board layout --
# Board layout shared by every scene of this video.
ROW_Y = 2.72             # every scene heading sits on this line
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

GRID_DX = 2.85           # the two columns of every four-cell dashboard
GRID_X = (0.5 - GRID_DX, 0.5 + GRID_DX)
GRID_DY = 1.60           # the two rows of it
GRID_Y = (1.25, -0.35)


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
    a = target.get_corner(np.array([-1.0, -1.0, 0.0])) + np.array([-pad, -pad, 0])
    b = target.get_corner(np.array([1.0, 1.0, 0.0])) + np.array([pad, pad, 0])
    return Line(a, b, color=color, stroke_width=width)


def frac_bar(x_left, x_right, y, color=CHALK_WHITE, width=2.6):
    """A quotient's fraction bar."""
    return Line(np.array([x_left, y, 0.0]), np.array([x_right, y, 0.0]),
                color=color, stroke_width=width)


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


def law_card(maths, note, color=CHALK_CYAN, width=4.2, height=1.35,
             note_size=14, math_up=0.30, note_down=0.34):
    """One dashboard cell: the law, with its one-line rule underneath.

    `math_up` / `note_down` are tightened for a card that has to stay clear of
    the caption band below it."""
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


def q_card(title, body, color=CHALK_CYAN, width=3.7, height=0.78,
           head_up=0.20, body_down=0.16):
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


def mark_no(size=1.0, color=CHALK_RED):
    """A drawn chalk cross (the board font has no cross glyph)."""
    cross = VGroup(
        Line(np.array([-0.10, -0.10, 0.0]), np.array([0.10, 0.10, 0.0])),
        Line(np.array([-0.10, 0.10, 0.0]), np.array([0.10, -0.10, 0.0])),
    ).set_stroke(color=color, width=4.2)
    cross.scale(size)
    return cross


# ---------------------------------------------------------------- narration --
# About four minutes of speech at the series' rate (roughly 2.6 words a second),
# plus the ten-second challenge clock, the ten transition holds and the closing
# hold.
NARRATION = {
    "title": (
        "Advanced laws of exponents. <bookmark mark='b0'/>Power of a power, "
        "power of a product, power of a fraction, and the zero exponent. "
        "<bookmark mark='b1'/>First recognise the structure, then choose the "
        "law."
    ),
    "s1": (
        "In the last video we multiplied powers with the same base and added "
        "the exponents. <bookmark mark='b0'/>But look at this: a to the power "
        "m, all raised to the power n. <bookmark mark='b1'/>Should we add the "
        "exponents again? <bookmark mark='b2'/>The structure is different, so "
        "the rule is different. First recognise the structure."
    ),
    "s2": (
        "Take a small example: two cubed, all squared. <bookmark mark='b0'/>"
        "The inner power is three factors of two: one group. <bookmark "
        "mark='b1'/>The outer exponent two makes two copies of that whole "
        "group. <bookmark mark='b2'/>So there are two groups with three "
        "factors each: six factors altogether. That is two to the power six, "
        "because three times two is six. <bookmark mark='b3'/>So a power "
        "raised to another power multiplies the exponents."
    ),
    "s3": (
        "Now with letters. <bookmark mark='b0'/>A to the power m, all raised "
        "to the power n, means n copies of a to the power m. <bookmark "
        "mark='b1'/>That is m plus m plus m, n times over, which is m times n "
        "factors of a. <bookmark mark='b2'/>So the exponents multiply: a to "
        "the power m, all raised to the power n, is a to the power m n."
    ),
    "s4": (
        "Next, a product inside the brackets: two times three, all to the "
        "power four. <bookmark mark='b0'/>The outer exponent four makes four "
        "copies of the bracket. <bookmark mark='b1'/>Now regroup: all the twos "
        "together, and all the threes together. <bookmark mark='b2'/>That "
        "gives two to the power four times three to the power four. <bookmark "
        "mark='b3'/>In general, a b all to the power m is a to the power m "
        "times b to the power m: the exponent reaches every factor."
    ),
    "s5": (
        "Fractions work the same way: two fifths, all cubed. <bookmark "
        "mark='b0'/>That is two fifths, times two fifths, times two fifths. "
        "<bookmark mark='b1'/>The numerators group: two times two times two, "
        "which is two cubed. The denominators group: five times five times "
        "five, which is five cubed. <bookmark mark='b2'/>A fraction inside "
        "brackets is powered on the top and on the bottom."
    ),
    "s6": (
        "Why is any non-zero number to the power zero equal to one? <bookmark "
        "mark='b0'/>Start with a to the power four over a to the power four. "
        "<bookmark mark='b1'/>By ordinary division, anything divided by itself "
        "is one. <bookmark mark='b2'/>But by the quotient law the exponents "
        "subtract: four minus four is zero, so it is also a to the power zero. "
        "<bookmark mark='b3'/>Both answers describe the same quantity, so a to "
        "the power zero is one, for any non-zero a."
    ),
    "s7": (
        "Now look at the four shapes together. <bookmark mark='b0'/>A power "
        "raised to another power: multiply the exponents. <bookmark "
        "mark='b1'/>A product inside brackets: distribute the power to both "
        "factors. <bookmark mark='b2'/>A fraction inside brackets: power the "
        "top and the bottom. And an exponent of zero: the answer is simply one."
    ),
    "s8": (
        "Four mistakes to avoid. <bookmark mark='b0'/>First: x squared, all "
        "cubed, is x to the power six, not x to the power five, because the "
        "exponents multiply. <bookmark mark='b1'/>Second: a b all cubed is a "
        "cubed b cubed, not a cubed b. <bookmark mark='b2'/>Third: a over b, "
        "all squared, is a squared over b squared. <bookmark mark='b3'/>And "
        "fourth: seven to the power zero is one, not zero."
    ),
    "s9q": (
        "Your turn. <bookmark mark='b0'/>Four questions, one for each law. Simplify "
        "three to the power four, all squared. Simplify five x, all cubed. Simplify "
        "three sevenths, all squared. And work out minus six, all to the power zero."
    ),
    "s9a": (
        "<bookmark mark='b0'/>Three to the power four, all squared, multiplies the "
        "exponents: three to the power eight. <bookmark mark='b1'/>Five x, all cubed, "
        "is five cubed x cubed: one hundred and twenty five x cubed. <bookmark "
        "mark='b2'/>Three sevenths squared is three squared over seven squared, that "
        "is nine over forty nine. And minus six to the power zero is one."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>A power of a power multiplies the "
        "exponents. A power of a product distributes to every factor. <bookmark "
        "mark='b1'/>A power of a fraction powers the top and the bottom. And any "
        "non-zero base to the power zero is one. <bookmark mark='b2'/>See the "
        "structure, then choose the law. <bookmark mark='b3'/>Thank you for watching, "
        "<bookmark mark='b4'/>and see you in the next lesson."
    ),
}


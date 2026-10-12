"""Board furniture and narration for Storyboard 01 -- Introduction to
Exponents & Powers, Class 8 Mathematics, Chapter 4 (Exponents and Powers).

This file is *spliced*, never imported: assemble_exponents.py grafts it into the
proven video-03 head of the Chapter 3 quadrilaterals set, so the theme names
(CHALK_*, FONT, BOARD_*), `board_text`, `chalk_math` and the pacing helpers
(`rt`, `quick`, `leftover`) are already defined above it.

The furniture is this video's "Power Compressor" kit:

  * `tile`        -- one repeated factor as its own chalk tile,
  * `cross_sign`  -- the multiplication sign between two tiles,
  * `count_badge` -- the counter that visits each factor (1, 2, 3 ...),
  * `brace_note`  -- a brace under a chain with its "n factors" label,
  * `panel`       -- a titled card (BASE / EXPONENT / the long Sun number),
  * `machine`     -- the compressor box the factors enter,
  * `chip`        -- a small labelled chip (the "other large numbers" row),
  * `sun`         -- the stylised Sun of the large-number scene,
  * `chessboard`  -- the doubling board of the growth scene,
  * `mark_yes`    -- a drawn tick (Segoe Print has no tick glyph).

The file has two splice markers, a board-layout section (constants plus the
furniture helpers) and the narration table; assemble_exponents.py cuts between
them.
"""
from __future__ import annotations

import numpy as np

from manim import (
    DOWN, LEFT, RIGHT, UP, Circle, Line, MathTex, RoundedRectangle, Square,
    VGroup, Brace,
)

# ------------------------------------------------------------ board layout --
from manim import Brace  # noqa: E402  (this section is spliced into a head
#                                         whose own imports omit Brace)

# Board layout shared by every scene of this video.
COLUMN_X = 3.05          # the series' right-hand note column
LEFT_X = -2.40           # left half of a two-column comparison
RIGHT_X = 3.40           # right half of a two-column comparison
ROW_Y = 2.72             # every scene heading sits on this line
SUB_Y = 2.20             # the one-line sub-heading under it
BANNER_Y = -1.15         # the closing banner, above the strip
# The burned-in caption grows up from the bottom of the frame: a one-line cue
# starts at y = -3.38 and a wrapped two-line cue reaches y = -2.93 (measured on
# the burned 360p cuts), so every closing strip sits at -1.80 and nothing at all
# sits below CAPTION_SAFE_Y = -2.00 -- audited by the IN-CAPTION-BAND check.
STRIP_Y = -1.80
CAPTION_SAFE_Y = -2.00

TILE_W = 0.60            # one factor tile
TILE_H = 0.72
PANEL_FILL = "#16202B"

# The factor chains and the three-question challenge are laid out from these,
# so every scene keeps the same rhythm.
CHAIN_BUFF = 0.18
CHAIN_Y = 1.02


# ---------------------------------------------------------------- furniture --
def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


def tile(label, color=CHALK_WHITE, size=26, w=TILE_W, h=TILE_H, fill=0.55):
    """One repeated factor as a chalk tile: a rounded box around its digit."""
    lab = chalk_math(label, size=size, color=color)
    box = RoundedRectangle(corner_radius=0.07, width=w, height=h,
                           stroke_color=color, stroke_width=1.9,
                           fill_color=PANEL_FILL, fill_opacity=fill)
    lab.move_to(box.get_center())
    grp = VGroup(box, lab)
    grp.label = lab
    return grp


def cross_sign(color=CHALK_WHITE, size=24):
    """The multiplication sign between two factor tiles."""
    return board_text("\u00d7", size, color, "BOLD")


def chain_of(n, label="3", color=CHALK_WHITE, size=26, buff=CHAIN_BUFF):
    """`n` factor tiles with multiplication signs between them."""
    parts = []
    for i in range(n):
        if i:
            parts.append(cross_sign(size=int(size * 0.85)))
        parts.append(tile(label, color, size=size))
    grp = VGroup(*parts).arrange(RIGHT, buff=buff)
    grp.tiles = [parts[i] for i in range(0, len(parts), 2)]
    grp.crosses = [parts[i] for i in range(1, len(parts), 2)]
    return grp


def count_badge(value, color=CHALK_CYAN, size=15, radius=0.18):
    """The counter that visits each factor in turn."""
    lab = board_text(str(value), size, color, "BOLD")
    ring = Circle(radius=radius, stroke_color=color, stroke_width=1.6,
                  fill_color=PANEL_FILL, fill_opacity=0.7)
    ring.move_to(lab.get_center())
    return VGroup(ring, lab)


def brace_note(group, text, color=CHALK_CYAN, size=15, buff=0.10):
    """A brace under `group` carrying a small label."""
    brace = Brace(group, DOWN, buff=buff, color=color)
    note = board_text(text, size, color, "BOLD")
    note.next_to(brace, DOWN, buff=0.08)
    return VGroup(brace, note)


def panel(title, lines, color=CHALK_WHITE, width=4.0, height=1.40,
          title_size=20, line_size=15):
    """A rounded card with a heading and one or two body lines.

    The offsets are measured so the heading, the body lines and the box edge all
    keep at least 0.24 units between their ink, which is the series' clearance
    standard."""
    head = board_text(title, title_size, color, "BOLD")
    body = VGroup(*[board_text(l, line_size, CHALK_WHITE, "BOLD")
                    for l in lines]).arrange(DOWN, buff=0.24)
    box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                           stroke_color=color, stroke_width=2.0,
                           fill_color=PANEL_FILL, fill_opacity=0.55)
    head.move_to(box.get_center() + UP * (height / 2 - 0.21))
    body.move_to(box.get_center() + DOWN * (0.30 if len(lines) > 1 else 0.22))
    return VGroup(box, head, body)


def machine(title, subtitle="", color=CHALK_CYAN, width=2.30, height=1.55,
            size=16):
    """The Power Compressor: the box the factors travel through."""
    head = board_text(title, size, color, "BOLD")
    box = RoundedRectangle(corner_radius=0.12, width=width, height=height,
                           stroke_color=color, stroke_width=2.4,
                           fill_color=PANEL_FILL, fill_opacity=0.7)
    head.move_to(box.get_center() + UP * (0.20 if subtitle else 0.0))
    grp = VGroup(box, head)
    if subtitle:
        sub = board_text(subtitle, size - 3, CHALK_YELLOW, "BOLD")
        sub.move_to(box.get_center() + DOWN * 0.28)
        grp.add(sub)
        grp.sub = sub
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


def sun(radius=0.72, body=CHALK_AMBER, ray=CHALK_YELLOW):
    """The stylised Sun of the large-number scene (body plus eight rays)."""
    disc = Circle(radius=radius, stroke_color=ray, stroke_width=2.4,
                  fill_color=body, fill_opacity=0.9)
    rays = VGroup()
    for k in range(8):
        ang = k * np.pi / 4.0
        start = np.array([np.cos(ang), np.sin(ang), 0.0]) * (radius + 0.10)
        end = np.array([np.cos(ang), np.sin(ang), 0.0]) * (radius + 0.30)
        rays.add(Line(start, end, stroke_color=ray, stroke_width=3.0))
    return VGroup(rays, disc)


def chessboard(rows=2, cols=6, sq=0.62, light="#D9CDB4", dark="#5C6B57"):
    """A stretch of chessboard: alternating squares, top row first."""
    squares = VGroup()
    for r in range(rows):
        for c in range(cols):
            fill = light if (r + c) % 2 == 0 else dark
            squares.add(Square(side_length=sq, stroke_color=CHALK_WHITE,
                               stroke_width=1.2, fill_color=fill,
                               fill_opacity=0.85))
    grid = VGroup()
    for r in range(rows):
        row = VGroup(*squares[r * cols:(r + 1) * cols]).arrange(RIGHT, buff=0)
        grid.add(row)
    grid.arrange(DOWN, buff=0)
    grid.squares = squares
    return grid


def mark_yes(size=1.0, color=CHALK_GREEN):
    """A drawn chalk tick (the board font has no tick glyph)."""
    tick = VGroup(
        Line(ORIGIN, np.array([0.09, -0.11, 0.0])),
        Line(np.array([0.09, -0.11, 0.0]), np.array([0.28, 0.17, 0.0])),
    ).set_stroke(color=color, width=4.2)
    tick.scale(size)
    return tick


# ---------------------------------------------------------------- narration --
# About three and a half minutes of speech at the series' rate (roughly 2.6 words
# a second), plus the ten-second challenge clock, the ten transition holds and
# the closing hold.
NARRATION = {
    "title": (
        "Exponents and powers. <bookmark mark='b0'/>A short way to write "
        "repeated multiplication: base, exponent and power. <bookmark "
        "mark='b1'/>Let us see why we need it."
    ),
    "s1": (
        "Start with a simple product: three times three times three. <bookmark "
        "mark='b0'/>Now keep going, up to six factors of three. <bookmark "
        "mark='b1'/>Every single three has to be written out. <bookmark "
        "mark='b2'/>Do we really need to write three six times? There must be "
        "a shorter way."
    ),
    "s2": (
        "Let us count them. <bookmark mark='b0'/>Three times three times "
        "three times three times three times three: six equal factors. "
        "<bookmark mark='b1'/>That small raised number tells us how many times "
        "the base is used as a factor. <bookmark mark='b2'/>So three to the "
        "power six means six threes multiplied together."
    ),
    "s3": (
        "Look closely at three to the power six. <bookmark mark='b0'/>The "
        "large number at the bottom is the base: three, the number that is "
        "multiplied again and again. <bookmark mark='b1'/>The small raised "
        "number is the exponent: six, the number of factors. <bookmark "
        "mark='b2'/>The whole expression is called a power. We read it as "
        "three raised to the power six."
    ),
    "s4": (
        "Now send five factors of four through the power compressor. <bookmark "
        "mark='b0'/>In they go: four times four times four times four times "
        "four. <bookmark mark='b1'/>The machine counts five factors and writes "
        "four to the power five. <bookmark mark='b2'/>Send it back the other "
        "way, and four to the power five expands into five fours multiplied."
    ),
    "s5": (
        "Here is a mistake to avoid. <bookmark mark='b0'/>Four to the power "
        "five is not four times five. <bookmark mark='b1'/>Four to the power "
        "five means five fours multiplied, which is one thousand and twenty "
        "four. <bookmark mark='b2'/>Four times five is only twenty. The "
        "exponent counts factors, not how many times to multiply."
    ),
    "s6": (
        "Powers of ten are the most useful of all. <bookmark mark='b0'/>Ten to "
        "the power one is ten, and ten squared is ten times ten: one hundred. "
        "<bookmark mark='b1'/>Ten cubed is one thousand. Every new factor of "
        "ten adds another zero. <bookmark mark='b2'/>Ten to the power nine is "
        "a one followed by nine zeros: one thousand million."
    ),
    "s7": (
        "Now the reason we need all this. <bookmark mark='b0'/>The Sun is "
        "about fourteen crore metres across: a one and a four, followed by "
        "eight zeros. <bookmark mark='b1'/>In exponential form that is one "
        "point four times ten to the power nine. <bookmark mark='b2'/>The same "
        "short line writes the distance to the Sun, or the age of the universe."
    ),
    "s8": (
        "Numbers can also grow very fast. <bookmark mark='b0'/>One grain on "
        "the first square of a chessboard, two on the next, four on the next, "
        "then eight, sixteen, thirty two. <bookmark mark='b1'/>Every square "
        "doubles the one before it. <bookmark mark='b2'/>By the last square "
        "the number is enormous, and only exponents can write it comfortably."
    ),
    "s9q": (
        "Your turn. <bookmark mark='b0'/>Three questions. Write seven times seven "
        "times seven times seven in exponential form. Expand two to the power five. "
        "Name the base and the exponent in ten to the power six."
    ),
    "s9a": (
        "<bookmark mark='b0'/>Seven is repeated four times, so that is seven to the "
        "power four. <bookmark mark='b1'/>Two to the power five is five twos "
        "multiplied together. <bookmark mark='b2'/>And in ten to the power six, ten "
        "is the base and six is the exponent."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>The base is the number that repeats. The "
        "exponent counts how many times it is used as a factor. <bookmark "
        "mark='b1'/>The power is the compact expression that writes it in one place. "
        "<bookmark mark='b2'/>Remember: exponents make repeated multiplication short. "
        "<bookmark mark='b3'/>Thank you for watching, <bookmark mark='b4'/>and see you "
        "in the next lesson."
    ),
}

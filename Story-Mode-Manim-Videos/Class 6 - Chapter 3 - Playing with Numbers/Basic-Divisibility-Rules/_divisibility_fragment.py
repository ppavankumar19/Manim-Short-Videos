"""Layout furniture and narration for Storyboard 01 -- Basic Divisibility
Rules for 2, 3, 5, 6, 9 and 10 (Class 6 Maths, Chapter 3: Playing with Numbers).

This file is *spliced*, never imported: assemble_divisibility.py grafts it into
the video-03 head of the Chapter 3 quadrilaterals set, so the theme names
(CHALK_*, FONT, BOARD_*), `board_text`, `chalk_math` and the pacing helpers
(`rt`, `quick`, `leftover`) are already defined above it, exactly as the series'
other topics do it.

What the head already provides and this topic reuses unchanged:
the chalkboard backdrop with the student, the teacher and both corner badges,
`reset_board`, `appear`, `_capture_srt`/`_write_real_srt`, the card helpers
(`measure_card`, `check_row`, `summary_row`, `combo_card`, `choice_row`) and the
shared THINK clock from story_common.

What this file adds: number cards, digit tiles, chocolate groups, verdict marks,
zone panels and the narration table.

    # ---------------------------------------------------------- furniture --
    # ---------------------------------------------------------- narration --
"""
from __future__ import annotations

import numpy as np

from manim import (
    DOWN, LEFT, RIGHT, UP, Dot, Line, MathTex, RoundedRectangle, VGroup,
)

# ------------------------------------------------------------ board layout --
# Board layout shared by every scene of this video.
COLUMN_X = 3.05          # the series' right-hand note column
LEFT_X = -2.40           # left half of a two-column comparison
RIGHT_X = 3.40           # right half of a two-column comparison
ROW_Y = 2.72             # every scene heading sits on this line
# The burned-in captions grow upward from the bottom of the frame: a one-line
# cue starts at y = -3.33 and a two-line cue reaches y = -2.33.  Every closing
# strip therefore sits at -1.95, with nothing below -2.15 (audited by the
# IN-CAPTION-BAND check).
STRIP_Y = -1.95

TILE_W = 0.40            # one digit tile
TILE_H = 0.54
PANEL_FILL = "#16202B"


# ---------------------------------------------------------------- furniture --
def number_card(value, color=CHALK_WHITE, size=26, stroke=CHALK_AMBER):
    """A number on its own small chalk card."""
    tex = chalk_math(str(value), size=size, color=color)
    box = RoundedRectangle(corner_radius=0.08, width=tex.width + 0.44,
                           height=tex.height + 0.30, stroke_color=stroke,
                           stroke_width=1.8, fill_color=PANEL_FILL,
                           fill_opacity=0.8)
    tex.move_to(box.get_center())
    grp = VGroup(box, tex)
    grp.tex = tex
    return grp


def badge_card(label, color=CHALK_WHITE, size=26, width=None, height=0.62,
               text_size=None):
    """A single number or symbol in a rounded badge (a divisor chip)."""
    tex = board_text(label, text_size or int(size * 0.72), color, "BOLD")
    box = RoundedRectangle(corner_radius=0.10,
                           width=width or max(tex.width + 0.44, height),
                           height=height, stroke_color=color, stroke_width=2.0,
                           fill_color=PANEL_FILL, fill_opacity=0.75)
    tex.move_to(box.get_center())
    grp = VGroup(box, tex)
    grp.tex = tex
    return grp


def digit_tiles(number, size=26, color=CHALK_WHITE, buff=0.10):
    """Each digit of `number` as its own tile: returns (group, [tiles])."""
    tiles = []
    for ch in str(number):
        lab = chalk_math(ch, size=size, color=color)
        box = RoundedRectangle(corner_radius=0.06, width=TILE_W, height=TILE_H,
                               stroke_color=CHALK_WHITE, stroke_width=1.5,
                               fill_color=PANEL_FILL, fill_opacity=0.5)
        lab.move_to(box.get_center())
        tiles.append(VGroup(box, lab))
    grp = VGroup(*tiles).arrange(RIGHT, buff=buff)
    for i, tile in enumerate(grp):
        tile.index = i
    return grp, list(grp)


def tile_ring(tile, color=CHALK_YELLOW, buff=0.07):
    """The magnifying ring that picks one digit out of a number."""
    return RoundedRectangle(corner_radius=0.08, width=TILE_W + 2 * buff + 0.08,
                            height=TILE_H + 2 * buff + 0.08, stroke_color=color,
                            stroke_width=3.0).move_to(tile.get_center())


def mark_yes(size=1.0, color=CHALK_GREEN):
    """A chalk tick (the same stroke used by check_row)."""
    tick = VGroup(
        Line(ORIGIN, np.array([0.09, -0.11, 0.0])),
        Line(np.array([0.09, -0.11, 0.0]), np.array([0.28, 0.17, 0.0])),
    ).set_stroke(color=color, width=4.2)
    tick.scale(size)
    return tick


def mark_no(size=1.0, color=CHALK_RED):
    """A chalk cross."""
    cross = VGroup(
        Line(np.array([-0.10, -0.10, 0.0]), np.array([0.10, 0.10, 0.0])),
        Line(np.array([-0.10, 0.10, 0.0]), np.array([0.10, -0.10, 0.0])),
    ).set_stroke(color=color, width=4.2)
    cross.scale(size)
    return cross


def verdict(ok, text, color=None, size=15, buff=0.20):
    """A tick or a cross beside the reason it is there."""
    m = mark_yes(size=0.95) if ok else mark_no(size=0.95)
    t = board_text(text, size, color or (CHALK_GREEN if ok else CHALK_PINK),
                   "BOLD")
    return VGroup(m, t).arrange(RIGHT, buff=buff)


def chocolate_groups(n_groups, per_group=4, cols=3, r=0.05, buff=0.05,
                     pad=0.10, color=CHALK_YELLOW):
    """`n_groups` little share-boxes, each holding `per_group` chocolates."""
    boxes = []
    for _ in range(n_groups):
        dots = VGroup(*[Dot(radius=r, color=color) for _ in range(per_group)])
        dots.arrange_in_grid(rows=2, cols=2, buff=buff)
        box = RoundedRectangle(corner_radius=0.05, width=dots.width + 2 * pad,
                               height=dots.height + 2 * pad,
                               stroke_color=CHALK_WHITE, stroke_width=1.3,
                               stroke_opacity=0.75)
        dots.move_to(box.get_center())
        boxes.append(VGroup(box, dots))
    rows = (n_groups + cols - 1) // cols
    return VGroup(*boxes).arrange_in_grid(rows=rows, cols=cols, buff=0.16)


def rule_line(label, detail, color=CHALK_WHITE, width=None, size=17):
    """One divisibility rule as a card: the divisor badge and its test."""
    badge = board_text(label, size, color, "BOLD")
    body = board_text(detail, size - 2, CHALK_WHITE, "BOLD")
    box = RoundedRectangle(corner_radius=0.09,
                           width=width or max(badge.width + body.width + 0.90,
                                              2.4),
                           height=0.60, stroke_color=color, stroke_width=1.7,
                           fill_color=PANEL_FILL, fill_opacity=0.7)
    badge.move_to(box.get_center() + LEFT * (box.width / 2 - badge.width / 2
                                             - 0.16))
    body.next_to(badge, RIGHT, buff=0.24)
    grp = VGroup(box, badge, body)
    grp.badge, grp.body = badge, body
    return grp


def zone_panel(title, lines, color=CHALK_WHITE, width=3.0, height=2.35,
               size=16, line_size=14):
    """One of the three 'families of rules' panels of the dashboard scene."""
    head = board_text(title, size, color, "BOLD")
    body = VGroup(*[board_text(l, line_size, CHALK_WHITE, "BOLD")
                    for l in lines]).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                           stroke_color=color, stroke_width=2.0,
                           fill_color=PANEL_FILL, fill_opacity=0.55)
    head.move_to(box.get_center() + UP * (height / 2 - 0.34))
    body.move_to(box.get_center() + DOWN * 0.22)
    return VGroup(box, head, body)


def column_card(mob, y, x=COLUMN_X):
    return mob.move_to(np.array([x, y, 0]))


def column_note(text, y, x=COLUMN_X, size=15, color=CHALK_WHITE):
    return board_text(text, size, color, "BOLD").move_to(np.array([x, y, 0]))


def gate(label, detail, color=CHALK_WHITE, width=2.7, height=1.05):
    """A scanner gate: the test it runs, over the evidence for it."""
    head = board_text(label, 17, color, "BOLD")
    body = board_text(detail, 14, CHALK_WHITE, "BOLD")
    box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                           stroke_color=color, stroke_width=2.0,
                           fill_color=PANEL_FILL, fill_opacity=0.6)
    head.move_to(box.get_center() + UP * 0.24)
    body.move_to(box.get_center() + DOWN * 0.20)
    return VGroup(box, head, body)


# ---------------------------------------------------------------- narration --
# Cut to the production target: 11 pieces, about 3 minutes of speech at the
# series' rate (2.6 words a second), keeping the seven-stage structure --
# hook (scene 1), meaning (2), the rules (3-7), real-world use (8), practice
# (9) and recap (10).
NARRATION = {
    "title": (
        "Every number carries a clue about its divisors. <bookmark "
        "mark='b0'/>Here are the quick tests for six divisors, with no long "
        "division at all. <bookmark mark='b1'/>Look, add, combine."
    ),
    "scene1": (
        "Hasini has one hundred and twenty five chocolates to share. <bookmark "
        "mark='b0'/>Traders shared grain this way for centuries. <bookmark "
        "mark='b1'/>Five at a time gives twenty five groups; <bookmark "
        "mark='b2'/>six leaves five over. <bookmark mark='b3'/>Every guess "
        "costs a division. <bookmark mark='b4'/>So can we tell without "
        "dividing? <bookmark mark='b5'/>Yes, with a divisibility rule."
    ),
    "scene2": (
        "What does divisible mean? <bookmark mark='b0'/>Twenty four divided by "
        "four is six equal groups, <bookmark mark='b1'/>remainder zero. "
        "<bookmark mark='b2'/>Twenty nine leaves <bookmark mark='b3'/>one over. "
        "<bookmark mark='b4'/>Remainder zero: that is the test. <bookmark "
        "mark='b5'/>Now inspect the digits."
    ),
    "scene3": (
        "Divisibility by two. <bookmark mark='b0'/>Take nine hundred fifty "
        "three <bookmark mark='b1'/>and nine thousand five hundred thirty four. "
        "<bookmark mark='b2'/>Only the ones digit matters. <bookmark "
        "mark='b3'/>Even endings: zero, two, four, six, eight. <bookmark "
        "mark='b4'/>The second passes; <bookmark mark='b5'/>the first does not. "
        "<bookmark mark='b6'/>Ignore every other digit."
    ),
    "scene4": (
        "Divisibility by five and ten. <bookmark mark='b0'/>Five thousand "
        "seven hundred eighty five ends in five: <bookmark mark='b1'/>five "
        "divides it. <bookmark mark='b2'/>One thousand two hundred fifty ends "
        "in zero: <bookmark mark='b3'/>five and ten divide it. <bookmark "
        "mark='b4'/>Two needs even; five needs zero or five; ten needs zero. "
        "<bookmark mark='b5'/>Three rules, one glance."
    ),
    "scene5": (
        "Divisibility by three is different. <bookmark mark='b0'/>Twenty seven "
        "and thirty seven both end in seven, <bookmark mark='b1'/>yet only "
        "twenty seven divides by three. <bookmark mark='b2'/>Add the digits of "
        "thirty six thousand one hundred twenty nine. <bookmark mark='b3'/>"
        "Three, six, one, two, nine: twenty one, which three divides. <bookmark "
        "mark='b4'/>So the number does too."
    ),
    "scene6": (
        "Divisibility by nine: the same digits, a stronger question. "
        "<bookmark mark='b0'/>Nine thousand eight hundred forty six. <bookmark "
        "mark='b1'/>Nine, eight, four, six: twenty seven, which is nine times "
        "three. <bookmark mark='b2'/>So nine divides it. <bookmark "
        "mark='b3'/>Same digits, stronger question."
    ),
    "scene7": (
        "Divisibility by six needs two tests. <bookmark mark='b0'/>Seven "
        "thousand two hundred twenty four ends in four, an even digit. "
        "<bookmark mark='b1'/>Seven, two, two, four: fifteen, and three "
        "divides fifteen. <bookmark mark='b2'/>Both pass, so six divides it. "
        "<bookmark mark='b3'/>Remember the word both."
    ),
    "scene8": (
        "Now use it. <bookmark mark='b0'/>Three hundred seventy two runners "
        "want equal teams of six. <bookmark mark='b1'/>Test two: the number "
        "ends in two. <bookmark mark='b2'/>Test three: three, seven, two, "
        "twelve. <bookmark mark='b3'/>Both pass: sixty two teams, nobody out."
    ),
    "scene9": (
        "Which of two, three, five, six, nine and ten divide twelve thousand "
        "three hundred forty five? <bookmark mark='b0'/>Pause and decide. "
        "<bookmark mark='b1'/>The last digit is five, which is odd: two fails, "
        "and six too. <bookmark mark='b2'/>Five passes, and ten fails. "
        "<bookmark mark='b3'/>The digits add to fifteen: three passes, nine "
        "fails. <bookmark mark='b4'/>Divisible by three and five."
    ),
    "scene10": (
        "All six rules, in three ideas. <bookmark mark='b0'/>Last digit: two "
        "needs even; five needs zero or five; ten needs zero. <bookmark "
        "mark='b1'/>Add the digits: three needs a sum divisible by three; nine "
        "by nine. <bookmark mark='b2'/>Combine: six needs two and three "
        "together. <bookmark mark='b3'/>Look, add, combine. <bookmark "
        "mark='b4'/>Thank you for watching. See you next lesson."
    ),
}

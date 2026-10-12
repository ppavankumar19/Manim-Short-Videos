"""Layout furniture and narration for Storyboard 02 -- Advanced Divisibility
Rules for 4, 8 and 11 (Class 6 Maths, Chapter 3: Playing with Numbers).

This file is *spliced*, never imported: assemble_advanced.py grafts it into the
video-03 head of the Chapter 3 quadrilaterals set, so the theme names
(CHALK_*, FONT, BOARD_*), `board_text`, `chalk_math` and the pacing helpers
(`rt`, `quick`, `leftover`) are already defined above it.

The furniture is the same "divisibility scanner" kit the previous video in this
chapter uses (number cards, digit tiles, badges, gates, rule lines, zone
panels, ticks and crosses) plus what these three rules need:

  * a *lens* -- a rounded window over the last two or three digit tiles, with
    the digits outside it dimmed (the visual that makes 4 and 8 memorable);
  * *place tags* and two *baskets* for the alternating-position test for 11.

The file has two splice markers, a board-layout section (constants plus the
furniture helpers) and the narration table, and assemble_advanced.py cuts
between them.
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
# The burned-in caption grows up from the bottom of the frame: a one-line cue
# starts at y = -3.38 and a wrapped two-line cue reaches y = -2.93 (measured on
# the burned 360p cut).  The production audit still asked for the closing
# banners to move clear of the subtitle zone, so the strip was lifted 0.15 --
# roughly 15% of the banner band it lives in -- from -1.95 to -1.80, and the row
# above it was lifted with it.  The lowest ink on the board is now the strip's
# own baseline at -1.93 and nothing at all sits below CAPTION_SAFE_Y = -2.00 --
# audited by the IN-CAPTION-BAND check in audit_sync_overlap.py.
STRIP_Y = -1.80

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


def digit_tiles(number, size=26, color=CHALK_WHITE, buff=0.10,
                tile_w=TILE_W, tile_h=TILE_H):
    """Each digit of `number` as its own tile: returns (group, [tiles])."""
    tiles = []
    for ch in str(number):
        lab = chalk_math(ch, size=size, color=color)
        box = RoundedRectangle(corner_radius=0.06, width=tile_w, height=tile_h,
                               stroke_color=CHALK_WHITE, stroke_width=1.5,
                               fill_color=PANEL_FILL, fill_opacity=0.5)
        lab.move_to(box.get_center())
        tiles.append(VGroup(box, lab))
    grp = VGroup(*tiles).arrange(RIGHT, buff=buff)
    return grp, list(grp)


def tile_ring(tile, color=CHALK_YELLOW, buff=0.07):
    """A ring around a single digit."""
    return RoundedRectangle(corner_radius=0.08, width=TILE_W + 2 * buff + 0.08,
                            height=TILE_H + 2 * buff + 0.08, stroke_color=color,
                            stroke_width=3.0).move_to(tile.get_center())


def digit_lens(tiles, k, color=CHALK_YELLOW, buff=0.10, width_pad=0.32):
    """The scanner lens: a window over the last `k` tiles of a number."""
    last = tiles[-k:]
    left, right = last[0].get_left()[0], last[-1].get_right()[0]
    top, bottom = last[0].get_top()[1], last[0].get_bottom()[1]
    box = RoundedRectangle(corner_radius=0.10,
                           width=(right - left) + width_pad,
                           height=(top - bottom) + 2 * buff + 0.08,
                           stroke_color=color, stroke_width=3.2)
    box.move_to(np.array([(left + right) / 2.0, (top + bottom) / 2.0, 0]))
    return box


def dim_outside(tiles, k):
    """The original tiles outside the lens, so they can be faded in place.

    Fading a *copy* over the original would draw every digit twice (and the
    audits rightly report the two glyphs as text-in-text)."""
    return VGroup(*[tile for i, tile in enumerate(tiles)
                    if i < len(tiles) - k])


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


def rule_line(label, detail, color=CHALK_WHITE, width=None, size=17):
    """One rule as a card: the divisor badge and its test."""
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


def zone_panel(title, lines, color=CHALK_WHITE, width=3.0, height=2.30,
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


def basket(label, terms, total, color=CHALK_WHITE, width=3.4, height=1.45,
           size=16):
    """One alternating-position basket for the 11 test: label, sum, total."""
    head = board_text(label, size, color, "BOLD")
    body = chalk_math(terms, size=26, color=CHALK_YELLOW)
    box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                           stroke_color=color, stroke_width=2.0,
                           fill_color=PANEL_FILL, fill_opacity=0.6)
    head.move_to(box.get_center() + UP * 0.42)
    body.move_to(box.get_center() + DOWN * 0.16)
    grp = VGroup(box, head, body)
    grp.head, grp.body, grp.total = head, body, total
    return grp


def place_tags(tiles, letters=("odd", "even"), color=CHALK_CYAN, size=11,
               y_shift=-0.42):
    """Label each digit with the parity of its place, counting from the right."""
    tags = VGroup()
    for i, tile in enumerate(reversed(tiles)):        # right to left
        word = letters[i % 2]
        tags.add(board_text(word, size, color, "BOLD").move_to(
            tile.get_center() + DOWN * abs(y_shift)))
    return tags


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
# Speech runs at the series' rate (about 2.6 words a second).  The cold-open
# hook and the stadium application add ~26 s of speech, which takes the finished
# video (with the centred THINK clock, the transitions and the closing hold to
# about 3 min 45 s -- still inside the storyboard's estimate for this story.
NARRATION = {
    # Cold open: the production audit asked for a real-world hook before the
    # title card, so the video no longer opens on "three more divisibility
    # tests" with no reason to care.
    "hook": (
        "These tests are not only for the classroom. <bookmark mark='b0'/>A "
        "leap year arrives every four years. <bookmark mark='b1'/>A tiler "
        "checks whether eight tiles fit the wall. <bookmark mark='b2'/>A bank "
        "reads eleven on long account numbers."
    ),
    "title": (
        "Three more divisibility tests. <bookmark mark='b0'/>Four, eight and "
        "eleven need more than the last digit, and more than the digit sum. "
        "<bookmark mark='b1'/>Zoom in, zoom deeper, and alternate."
    ),
    "scene1": (
        "The scanner knows six rules: two, three, five, six, nine and ten. "
        "<bookmark mark='b0'/>Three new numbers join them: four, eight and "
        "eleven. <bookmark mark='b1'/>One digit is not enough for these. "
        "<bookmark mark='b2'/>Four and eight look deeper; eleven needs a new "
        "idea."
    ),
    "scene2": (
        "Divisibility by four. <bookmark mark='b0'/>Seventy six thousand five "
        "hundred thirty two is seventy six thousand five hundred, plus thirty "
        "two. <bookmark mark='b1'/>The first part is a multiple of one hundred, "
        "which divides by four. <bookmark mark='b2'/>So it is already divisible "
        "by four. <bookmark mark='b3'/>Only thirty two is left, and it divides "
        "by four."
    ),
    "scene3": (
        "Now use it on fifty six thousand four hundred ninety six. <bookmark "
        "mark='b0'/>The lens closes on ninety six. <bookmark mark='b1'/>Ninety "
        "six is four times twenty four, so it passes. <bookmark mark='b2'/>So "
        "the whole number divides by four. <bookmark mark='b3'/>The test works "
        "above one hundred."
    ),
    "scene4": (
        "Divisibility by eight. <bookmark mark='b0'/>One hundred fails, but "
        "one thousand works: eight times one hundred twenty five. <bookmark "
        "mark='b1'/>Break ninety three thousand six hundred twenty four into "
        "two parts: ninety three thousand, plus six hundred twenty four. "
        "<bookmark mark='b2'/>That part is a multiple of one thousand, so eight "
        "already divides it. <bookmark mark='b3'/>And six hundred twenty four "
        "divides by eight exactly."
    ),
    "scene5": (
        "Do not mix the two. Take two thousand one hundred four. <bookmark "
        "mark='b0'/>For four, the last two digits are zero four: four itself. "
        "<bookmark mark='b1'/>For eight, the last three: one hundred four, "
        "eight times thirteen. <bookmark mark='b2'/>Four looks at two digits, "
        "eight at three."
    ),
    "scene6": (
        "Divisibility by eleven. <bookmark mark='b0'/>Count the places from the "
        "right: odd, even, odd, even. <bookmark mark='b1'/>Odd places: one plus "
        "two is three. <bookmark mark='b2'/>Even places: two plus one is three. "
        "<bookmark mark='b3'/>Compare: three minus three is zero. <bookmark "
        "mark='b4'/>Zero: eleven divides it."
    ),
    "scene7": (
        "Now a number that fails. <bookmark mark='b0'/>Six thousand five "
        "hundred thirty five. <bookmark mark='b1'/>Odd places: five plus five, "
        "ten. Even places: three plus six, nine. <bookmark mark='b2'/>Ten minus "
        "nine is one. <bookmark mark='b3'/>One is not zero and not a multiple "
        "of eleven."
    ),
    "scene8": (
        "Three advanced rules, three clues. <bookmark mark='b0'/>For four, zoom "
        "into the last two digits. <bookmark mark='b1'/>For eight, zoom into "
        "the last three. <bookmark mark='b2'/>For eleven, split the digits into "
        "two alternating groups and compare their sums."
    ),
    # The second audit addition: one 10-15 s real-world application between the
    # dashboard and "Your Turn", using the textbook's own 56496.
    "apply": (
        "Fifty six thousand four hundred ninety six seats go into four-seat "
        "boxes. <bookmark mark='b0'/>Does anything stay empty? <bookmark "
        "mark='b1'/>The last two digits, ninety six, divide by four. <bookmark "
        "mark='b2'/>So the whole number does. <bookmark mark='b3'/>No seat is "
        "left over."
    ),
    "scene9": (
        "Your turn. <bookmark mark='b0'/>First, seven hundred twenty six "
        "thousand three hundred fifty two. <bookmark mark='b1'/>Pause and "
        "decide. <bookmark mark='b2'/>Last two digits, fifty two: four divides "
        "it. Last three digits, three hundred fifty two: eight divides it too. "
        "<bookmark mark='b3'/>So that number passes both tests. <bookmark "
        "mark='b4'/>Now a second number: ten thousand eight hundred twenty "
        "four. <bookmark mark='b5'/>Odd places thirteen, even places two. "
        "<bookmark mark='b6'/>Thirteen minus two is eleven, so eleven divides "
        "it."
    ),
    "scene10": (
        "One last look. <bookmark mark='b0'/>Four: the last two digits. "
        "<bookmark mark='b1'/>Eight: the last three digits. <bookmark "
        "mark='b2'/>Eleven: alternate the places, add each group, compare. "
        "<bookmark mark='b3'/>Zoom, zoom more, alternate. <bookmark "
        "mark='b4'/>Thank you for watching, and see you in the next lesson."
    ),
}

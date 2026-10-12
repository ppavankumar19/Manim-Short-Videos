"""Board furniture and narration for Storyboard 01 -- Compound Ratio & Inverse
Ratio: Applications in Business Profit Sharing, Class 8 Mathematics, Chapter 5
(Comparing Quantities using Proportion).

This file is *spliced*, never imported: assemble_compound_ratio.py grafts it into
the proven head of the Chapter 3 quadrilaterals set, so the theme names
(CHALK_*, FONT, BOARD_*), `board_text`, `chalk_math`, `appear` and the pacing
helpers (`rt`, `quick`, `leftover`) are already defined above it.

The furniture is this video's "two partners share a profit" business kit:

  * `person_icon`   -- a small filled figure (head over shoulders),
  * `partner_card`  -- a named card carrying one partner's money and time,
  * `ratio_card`    -- a ratio in a box (the object that slides and flips),
  * `money_bag`     -- the profit bag, drawn as filled shaded shapes,
  * `coin_stack`    -- a stack of coins (filled discs, not an outline),
  * `profit_blocks` -- the equal parts of the profit, drawn as solid blocks,
  * `machine`       -- the compound-ratio machine the two ratio cards enter,
  * `cross_out` / `tick` -- the drawn cross and tick (Segoe Print has neither).

Everything is drawn as filled, shaded geometry -- a bag with a tied neck, coins
with thickness, solid blocks -- never as a bare outline.
"""
from __future__ import annotations

import numpy as np

# ------------------------------------------------------------ board layout --
# (this section is spliced into a head whose own imports omit Ellipse, Arc,
#  Sector and Rotate; Dot, Circle, Line, Polygon, RoundedRectangle, VGroup,
#  DEGREES and np are already imported by the head)
from manim import Arc, Ellipse, Rotate, Sector  # noqa: E402,F401

# Board layout shared by every scene of this video.
ROW_Y = 2.72             # every scene heading sits on this line
SUB_Y = 2.16             # the one-line sub-heading under it
BANNER_Y = -1.15         # the closing banner, above the strip
# The burned-in caption grows up from the bottom of the frame: a one-line cue
# starts at y = -3.38 and a wrapped two-line cue reaches y = -2.93 (measured on
# the series' own burned 360p cuts), so every closing strip sits at -1.80 and
# nothing at all sits below CAPTION_SAFE_Y = -2.00 -- audited by the
# IN-CAPTION-BAND check.
STRIP_Y = -1.80
CAPTION_SAFE_Y = -2.00

# The two content bands.  Cards are 0.94 tall, so their TEXT boxes stay at least
# 0.25 units apart vertically at these centres -- the audits measure text.
BAND_A = 0.70            # the upper band (partner cards, input cards)
BAND_B = -0.50           # the lower band (the result of the upper band)

PANEL_FILL = "#16202B"
CARD_W = 3.30            # the standard card width
CARD_H = 0.94            # the standard card height
CHIP_H = 0.50
MARK_SIZE = 18           # ONE letter size for every labelled figure
DOT_R = 0.075
COIN_R = 0.17

# The example figures this video works with.  Both the profit total and the
# challenge amounts are marked on screen as examples, never as textbook facts.
RAMAYYA = ("Ramayya", "Rs 2,000", "for 12 months", CHALK_GREEN)
GOPALAM = ("Gopalam", "Rs 3,000", "for 9 months", CHALK_PINK)
CAP_RATIO = (2, 3)
TIME_RATIO = (4, 3)
COMPOUND = (8, 9)
PROFIT_TOTAL = 17000
PART_VALUE = 1000


# ---------------------------------------------------------------- furniture --
def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


def row_centres(half_widths, gap, cx=BOARD_CX):
    """x centres for a row of elements whose ink is `gap` apart.

    The row's combined ink is centred on `cx` (the green board's centre line) and
    the elements of a row are not equally wide, so equal centre spacing is NOT
    equal spacing on the board: this returns the centres that leave exactly `gap`
    units of clear air between neighbours.
    """
    total = 2.0 * sum(half_widths) + gap * (len(half_widths) - 1)
    x = cx - total / 2.0
    centres = []
    for half in half_widths:
        centres.append(x + half)
        x += 2.0 * half + gap
    return tuple(centres)


def panel(width, height, color=CHALK_WHITE, opacity=0.6, radius=0.10,
          stroke=1.9):
    """A rounded panel: the box every card and chip is drawn on."""
    return RoundedRectangle(corner_radius=radius, width=width, height=height,
                            stroke_color=color, stroke_width=stroke,
                            fill_color=PANEL_FILL, fill_opacity=opacity)


def chip(text, color=CHALK_CYAN, size=15, width=None, height=CHIP_H,
         fill=PANEL_FILL):
    """A small labelled chip."""
    lab = board_text(text, size, color, "BOLD")
    box = RoundedRectangle(corner_radius=0.09,
                           width=width or (lab.width + 0.40), height=height,
                           stroke_color=color, stroke_width=1.7,
                           fill_color=fill, fill_opacity=0.7)
    lab.move_to(box.get_center())
    grp = VGroup(box, lab)
    grp.box, grp.label = box, lab
    return grp


def person_icon(cx, cy, color=CHALK_CYAN, scale=1.0):
    """A small filled figure: a round head over a pair of shoulders."""
    head = Circle(radius=0.105 * scale, stroke_width=0,
                  fill_color=color, fill_opacity=0.9)
    head.move_to(np.array([cx, cy + 0.15 * scale, 0.0]))
    body = Ellipse(width=0.40 * scale, height=0.28 * scale, stroke_width=0,
                   fill_color=color, fill_opacity=0.5)
    body.move_to(np.array([cx, cy - 0.10 * scale, 0.0]))
    return VGroup(body, head)


def partner_card(name, money, months, color=CHALK_GREEN, width=CARD_W,
                 height=CARD_H, name_size=17, line_size=13):
    """One partner's card: their name, their money and their time.

    The figure (a filled head over shoulders) sits in the card's left margin, so
    the two partners read as two people and not just two rows of numbers.  The
    card's own two lines are spaced 0.22 apart -- the tightest the clearance
    audit allows two texts to come.
    """
    box = panel(width, height, color)
    icon = person_icon(-width / 2 + 0.42, 0.0, color)
    head = board_text(name, name_size, color, "BOLD")
    line = board_text(f"{money} · {months}", line_size, CHALK_WHITE, "BOLD")
    txt = VGroup(head, line).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
    txt.move_to(np.array([-width / 2 + 0.95 + txt.width / 2.0, 0.0, 0.0]))
    grp = VGroup(box, icon, txt)
    grp.box, grp.icon, grp.line, grp.name = box, icon, line, head
    return grp


def ratio_card(a, b, color=CHALK_AMBER, width=1.62, height=0.72, size=26):
    """A ratio written in a box -- the object that slides and flips."""
    tex = chalk_math(f"{a} : {b}", size=size, color=color)
    box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                           stroke_color=color, stroke_width=2.0,
                           fill_color=PANEL_FILL, fill_opacity=0.6)
    tex.move_to(box.get_center())
    grp = VGroup(box, tex)
    grp.box, grp.tex = box, tex
    return grp


def money_bag(cx, cy, scale=1.0, color=CHALK_AMBER, text="PROFIT",
              size=16, coins=True):
    """The profit bag: a filled, shaded bag with a tied neck (and coins)."""
    body = Ellipse(width=0.94 * scale, height=0.78 * scale, stroke_color=color,
                   stroke_width=2.6, fill_color=color, fill_opacity=0.24)
    body.move_to(np.array([cx, cy - 0.12 * scale, 0.0]))
    neck = Polygon(np.array([cx - 0.19 * scale, cy + 0.16 * scale, 0.0]),
                   np.array([cx + 0.19 * scale, cy + 0.16 * scale, 0.0]),
                   np.array([cx + 0.30 * scale, cy - 0.04 * scale, 0.0]),
                   np.array([cx - 0.30 * scale, cy - 0.04 * scale, 0.0]),
                   stroke_color=color, stroke_width=2.2,
                   fill_color=color, fill_opacity=0.24)
    tie = Line(np.array([cx - 0.30 * scale, cy + 0.15 * scale, 0.0]),
               np.array([cx + 0.30 * scale, cy + 0.15 * scale, 0.0]),
               stroke_color=CHALK_RED, stroke_width=3.4)
    # the label sits clear of the bag's own neck, so the audit's polygon
    # clearance check stays green
    lab = board_text(text, size, CHALK_WHITE, "BOLD")
    lab.move_to(np.array([cx, cy - 0.30 * scale, 0.0]))
    grp = VGroup(body, neck, tie, lab)
    grp.label = lab
    if coins:
        grp.add(coin_stack(cx - 0.60 * scale, cy - 0.44 * scale, 3, scale))
        grp.add(coin_stack(cx + 0.60 * scale, cy - 0.44 * scale, 3, scale))
    return grp


def coin_stack(cx, cy, n=3, scale=1.0, color=CHALK_YELLOW):
    """A stack of coins: filled discs with thickness, drawn bottom-up."""
    discs = VGroup()
    for i in range(n):
        e = Ellipse(width=0.46 * scale, height=0.16 * scale,
                    stroke_color=color, stroke_width=1.5,
                    fill_color=color, fill_opacity=0.38)
        e.move_to(np.array([cx, cy + 0.075 * i * scale, 0.0]))
        discs.add(e)
    return discs


def profit_blocks(count, color=CHALK_GREEN, side=0.24, gap=0.08, rows=1):
    """`count` equal solid blocks -- one block for one equal part of a profit.

    With `rows` > 1 the blocks are laid out in that many rows (bottom row
    first) and the whole block area is centred on the origin, so `at()` places
    it anywhere on the board.
    """
    per_row = int(np.ceil(count / rows))
    blocks = VGroup()
    for i in range(count):
        r, c = divmod(i, per_row)
        b = Square(side_length=side, stroke_color=color, stroke_width=1.6,
                   fill_color=color, fill_opacity=0.42)
        b.move_to(np.array([(c - (per_row - 1) / 2.0) * (side + gap),
                            (r - (rows - 1) / 2.0) * (side + gap), 0.0]))
        blocks.add(b)
    return blocks


def machine(width=4.60, height=1.50, title="COMPOUND RATIO MACHINE",
            color=CHALK_CYAN, formula=None, size=15):
    """The share machine: a filled box that two ratio cards go into.

    Its own heading and its own output formula live inside the one box, so the
    whole machine is a single board object.
    """
    box = RoundedRectangle(corner_radius=0.12, width=width, height=height,
                           stroke_color=color, stroke_width=2.4,
                           fill_color=PANEL_FILL, fill_opacity=0.62)
    head = board_text(title, size, color, "BOLD")
    head.move_to(box.get_top() + DOWN * 0.27)
    parts = [box, head]
    if formula is not None:
        parts.append(formula)
    grp = VGroup(*parts)
    grp.box, grp.head = box, head
    return grp


def funnel(cx, cy, width=0.80, height=0.46, color=CHALK_AMBER):
    """A small filled funnel: what goes into the machine on its left."""
    top = Line(np.array([cx - width / 2, cy + height / 2, 0.0]),
               np.array([cx + width / 2, cy + height / 2, 0.0]),
               stroke_color=color, stroke_width=2.4)
    left = Line(np.array([cx - width / 2, cy + height / 2, 0.0]),
                np.array([cx, cy - height / 2, 0.0]),
                stroke_color=color, stroke_width=2.4)
    right = Line(np.array([cx + width / 2, cy + height / 2, 0.0]),
                 np.array([cx, cy - height / 2, 0.0]),
                 stroke_color=color, stroke_width=2.4)
    body = Polygon(np.array([cx - width / 2, cy + height / 2, 0.0]),
                   np.array([cx + width / 2, cy + height / 2, 0.0]),
                   np.array([cx, cy - height / 2, 0.0]),
                   stroke_width=0, fill_color=color, fill_opacity=0.20)
    return VGroup(body, top, left, right)


def cross_out(mob, color=CHALK_RED, pad=0.10):
    """A drawn cross over a mobject (Segoe Print has no cross glyph).

    The cross is returned as part of a VGroup with its target by the caller, so
    the two are one board object and the audit never reads the strokes as a
    line running through somebody else's card.
    """
    x0, y0 = mob.get_left()[0] - pad, mob.get_bottom()[1] - pad
    x1, y1 = mob.get_right()[0] + pad, mob.get_top()[1] + pad
    return VGroup(
        Line(np.array([x0, y0, 0.0]), np.array([x1, y1, 0.0]),
             stroke_color=color, stroke_width=4.2),
        Line(np.array([x0, y1, 0.0]), np.array([x1, y0, 0.0]),
             stroke_color=color, stroke_width=4.2))


def wrong_card(text, color=CHALK_RED, width=2.60, height=1.05, size=15):
    """A card holding a WRONG statement, with a drawn cross over it.

    The cross occupies the card's top half and the statement its bottom half, so
    the strike-through is unmistakable yet never comes within the 0.04 units the
    audit allows between a stroke and the lettering.  The whole card is ONE
    board object, so the strokes are never read as a line running into a box.
    """
    box = panel(width, height, color, opacity=0.7)
    cross = VGroup(
        Line(np.array([-width / 2 + 0.55, 0.14, 0.0]),
             np.array([-width / 2 + 1.05, 0.50, 0.0]),
             stroke_color=color, stroke_width=4.2),
        Line(np.array([-width / 2 + 0.55, 0.50, 0.0]),
             np.array([-width / 2 + 1.05, 0.14, 0.0]),
             stroke_color=color, stroke_width=4.2),
    )
    cross.move_to(box.get_center() + UP * (height / 2 - 0.24))
    cross.shift(RIGHT * 0.10)
    lab = board_text(text, size, color, "BOLD")
    lab.move_to(box.get_center() + DOWN * (height / 2 - 0.22))
    grp = VGroup(box, cross, lab)
    grp.box, grp.cross, grp.label = box, cross, lab
    return grp


def tick(p, color=CHALK_GREEN, s=0.16):
    """A drawn tick (Segoe Print has no tick glyph)."""
    a = np.array([p[0] - s * 0.60, p[1] + s * 0.05, 0.0])
    b = np.array([p[0] - s * 0.05, p[1] - s * 0.55, 0.0])
    c = np.array([p[0] + s * 0.65, p[1] + s * 0.75, 0.0])
    return VGroup(Line(a, b, stroke_color=color, stroke_width=3.4),
                  Line(b, c, stroke_color=color, stroke_width=3.4))


def arrow_between(p1, p2, color=CHALK_YELLOW, width=3.0, tip=0.20):
    """A short arrow from one board point to another."""
    return Arrow(np.array([p1[0], p1[1], 0.0]), np.array([p2[0], p2[1], 0.0]),
                 buff=0.0, stroke_color=color, stroke_width=width,
                 tip_length=tip, max_tip_length_to_length_ratio=0.35)


def note_card(head, lines, color=CHALK_CYAN, width=3.40, height=1.05,
              head_size=15, line_size=13):
    """A card with a bold head line and one or two body lines under it.

    The head and the body are held 0.275 units apart, so the pair passes the
    clearance audit (which flags any two texts closer than 0.22).
    """
    box = panel(width, height, color)
    h = board_text(head, head_size, color, "BOLD")
    body = VGroup(*[board_text(line, line_size, CHALK_WHITE, "BOLD")
                    for line in lines]).arrange(DOWN, buff=0.24)
    h.move_to(box.get_center() + UP * 0.26)
    body.move_to(box.get_center() + DOWN * 0.26)
    grp = VGroup(box, h, body)
    grp.box, grp.head, grp.body = box, h, body
    return grp


def ratio_math(a, b, color=CHALK_AMBER, size=26):
    """A ratio as board maths."""
    return chalk_math(f"{a} : {b}", size=size, color=color)


def rupe(text, color=CHALK_WHITE, size=15):
    """A rupee amount as board text (the word 'Rs', which always renders)."""
    return board_text(text, size, color, "BOLD")


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "Meet two partners. <bookmark mark='b0'/>Ramayya invests two thousand "
        "rupees, and keeps that money in the business for twelve months. "
        "<bookmark mark='b1'/>Gopalam invests three thousand rupees for nine "
        "months. <bookmark mark='b2'/>At the end of the year the business earns "
        "a profit. <bookmark mark='b3'/>Should the two partners share that "
        "profit equally? <bookmark mark='b4'/>No. Profit in a partnership is "
        "shared in the ratio of what each partner contributed."
    ),
    "s1": (
        "A ratio is an ordered comparison. <bookmark mark='b0'/>Three to two is "
        "not the same as two to three. <bookmark mark='b1'/>The order of the "
        "two terms matters. <bookmark mark='b2'/>If we swap the two terms of a "
        "ratio, we get its inverse ratio: a to b becomes b to a. <bookmark "
        "mark='b3'/>So the inverse of four to five is five to four. <bookmark "
        "mark='b4'/>Inverse means swap the terms. It never means add them, and "
        "it never means change their signs."
    ),
    "s2": (
        "Now suppose both partners keep their money in for the same time. "
        "<bookmark mark='b0'/>Ramayya invests two thousand rupees for twelve "
        "months. <bookmark mark='b1'/>Gopalam also invests for twelve months, "
        "but he puts in three thousand rupees. <bookmark mark='b2'/>The time is "
        "the same for both, so the time factor cancels. <bookmark mark='b3'/>The "
        "capitals are in the ratio two thousand to three thousand, which "
        "simplifies to two to three. <bookmark mark='b4'/>So the profit is "
        "divided in the ratio two to three."
    ),
    "s3": (
        "Now suppose both partners invest the same capital. <bookmark "
        "mark='b0'/>Each of them invests five thousand rupees. <bookmark "
        "mark='b1'/>But Ramayya keeps his money in for twelve months, while "
        "Gopalam keeps his in for only nine months. <bookmark mark='b2'/>The "
        "capital is the same for both, so the capital factor cancels. <bookmark "
        "mark='b3'/>The times are in the ratio twelve to nine, and that "
        "simplifies to four to three. <bookmark mark='b4'/>So here the profit "
        "follows the time ratio, four to three."
    ),
    "s4": (
        "But in our business, both the money and the time are different. "
        "<bookmark mark='b0'/>Ramayya gives two thousand rupees for twelve "
        "months. <bookmark mark='b1'/>Gopalam gives three thousand rupees for "
        "nine months. <bookmark mark='b2'/>The capital ratio is two to three. "
        "<bookmark mark='b3'/>The time ratio is twelve to nine, that is four to "
        "three. <bookmark mark='b4'/>Neither ratio alone can decide the profit, "
        "so the two ratios must be combined."
    ),
    "s5": (
        "To combine two ratios we use the compound ratio. <bookmark "
        "mark='b0'/>For the ratios a to b and c to d, multiply the first terms "
        "together, <bookmark mark='b1'/>and multiply the second terms together. "
        "<bookmark mark='b2'/>The compound ratio is a times c to b times d. "
        "<bookmark mark='b3'/>A common mistake is to add the terms instead, and "
        "write a plus c to b plus d. <bookmark mark='b4'/>That is wrong. A "
        "compound ratio multiplies corresponding terms; it never adds them."
    ),
    "s6": (
        "Let us apply the rule. <bookmark mark='b0'/>We multiply the capital "
        "ratio two to three <bookmark mark='b1'/>by the time ratio four to "
        "three. <bookmark mark='b2'/>Two times four is eight, and three times "
        "three is nine, so the compound ratio is eight to nine. <bookmark "
        "mark='b3'/>Let us cross-check with money multiplied by time. Two "
        "thousand times twelve is twenty four thousand, and three thousand times "
        "nine is twenty seven thousand. <bookmark mark='b4'/>Twenty four "
        "thousand to twenty seven thousand simplifies to eight to nine, so the "
        "compound ratio is correct."
    ),
    "s7": (
        "Now let us turn that ratio into rupees. <bookmark mark='b0'/>Suppose "
        "the profit for the year is seventeen thousand rupees. This total is an "
        "example, not a textbook figure. <bookmark mark='b1'/>The ratio is eight "
        "to nine, so the profit is divided into eight plus nine, that is "
        "seventeen, equal parts. <bookmark mark='b2'/>Seventeen thousand divided "
        "by seventeen gives one thousand rupees for each part. <bookmark "
        "mark='b3'/>Ramayya takes eight parts, that is eight thousand rupees. "
        "<bookmark mark='b4'/>Gopalam takes nine parts, that is nine thousand "
        "rupees, and eight thousand plus nine thousand is seventeen thousand. "
        "The whole profit is shared."
    ),
    "s8": (
        "Here is the decision rule to remember. <bookmark mark='b0'/>If the "
        "time is the same, share the profit in the ratio of the capitals. "
        "<bookmark mark='b1'/>If the capital is the same, share it in the ratio "
        "of the times. <bookmark mark='b2'/>If both the capital and the time are "
        "different, share it in the compound ratio of capital and time. "
        "<bookmark mark='b3'/>So the share of the profit follows capital "
        "multiplied by time."
    ),
    "s9q": (
        "Your turn. Four quick checks. <bookmark mark='b0'/>First: write the "
        "inverse of the ratio seven to five. <bookmark mark='b1'/>Second: find "
        "the compound ratio of three to four and two to three. <bookmark "
        "mark='b2'/>Third: compound three to four with the inverse of four to "
        "five. <bookmark mark='b3'/>And last: partner P invests four thousand "
        "rupees for six months, and partner Q invests three thousand rupees for "
        "eight months. In what ratio should they share the profit?"
    ),
    "s9a": (
        "<bookmark mark='b0'/>The inverse of seven to five is five to seven, "
        "because the inverse swaps the two terms. <bookmark mark='b1'/>The "
        "compound ratio of three to four and two to three is six to twelve, "
        "which simplifies to one to two. <bookmark mark='b2'/>Three to four, "
        "compounded with the inverse of four to five, is three times five to "
        "four times four, that is fifteen to sixteen. <bookmark mark='b3'/>And "
        "for P and Q, four thousand times six is twenty four thousand, and three "
        "thousand times eight is also twenty four thousand. So the ratio is one "
        "to one, and the two partners share the profit equally."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>The inverse ratio swaps the two "
        "terms: a to b becomes b to a. <bookmark mark='b1'/>The compound ratio "
        "multiplies corresponding terms: a to b and c to d give a times c to b "
        "times d. <bookmark mark='b2'/>In a partnership, a partner's share "
        "follows capital multiplied by time. <bookmark mark='b3'/>And when the "
        "profit is known, divide it into equal parts using the ratio. <bookmark "
        "mark='b4'/>Money and time together decide the share. <bookmark "
        "mark='b5'/>Thank you for watching, <bookmark mark='b6'/>and see you in "
        "the next lesson."
    ),
}

"""Board furniture and the spoken script for Storyboard 02 -- Simple Interest
vs. Compound Interest: Deriving the Compound Interest Formula, Class 8
Mathematics, Chapter 5 (Comparing Quantities using Proportion).

This file is *spliced*, never imported: assemble_sicompound.py grafts it into
the proven head of the Chapter 3 quadrilaterals set, so the theme names
(CHALK_*, FONT, BOARD_*), `board_text`, `chalk_math` and the pacing helpers
(`rt`, `quick`, `leftover`) are already defined above it.

The furniture is this video's "two money ladders" interest kit:

  * `method_card`  -- an account card naming a method and its first result,
  * `block_row`    -- one solid block of a money ladder (principal / interest
                      / amount), optionally carrying a drawn padlock,
  * `padlock`      -- the drawn padlock that LOCKS a simple-interest principal
                      (Segoe Print has no lock glyph),
  * `ladder`       -- a column of those blocks, bottom row first,
  * `factor_card`  -- the boxed one-period growth factor (1 + R/100),
  * `coin_stack` / `rupee_note` -- the drawn money: filled discs with thickness
                      and a filled note with its own band,
  * `chip` / `note_card` / `panel` -- the boxed labels and cards,
  * `wrong_card` / `cross_out` / `tick` -- the drawn marks (Segoe Print has
                      neither a cross nor a tick).

Everything is drawn as filled, shaded geometry -- coins with thickness, notes
with a band, solid blocks -- never as a bare outline.
"""
from __future__ import annotations

import numpy as np

# ------------------------------------------------------------ board layout --
# (this section is spliced into a head whose own imports omit Arc and Ellipse;
#  Dot, Circle, Line, Polygon, RoundedRectangle, VGroup, DEGREES and np are
#  already imported by the head)
from manim import Arc, Ellipse  # noqa: E402,F401

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

# The two content bands.  The band centre is where a row of cards is pinned.
BAND_A = 0.72            # the upper band (ladders, formula rows)
BAND_B = -0.45           # the lower band (results, secondary rows)

PANEL_FILL = "#16202B"
CARD_W = 3.60            # the account card width
CARD_H = 1.36            # the account card height (three stacked lines)
CHIP_H = 0.50            # every small label box
LADDER_W = 2.30          # a big ladder block
LADDER_H = 0.62
ROW_STEP = 0.72
SMALL_W = 1.86           # a small ladder block (the side-by-side comparison)
SMALL_H = 0.42
SMALL_STEP = 0.55
MARK_SIZE = 18
COIN_R = 0.17

# The figures this video works with.  The textbook example is the Rs 2,500 one
# for simple interest; the compound-interest figures are the video's own, and
# the challenge amounts are marked on screen as exercises.
PRINCIPAL = 100
RATE = 10
SI_EXAMPLE = (2500, 12, 3, 900, 3400)      # P, R, T, SI, amount
CI_EXAMPLE = (5000, 8, 2, 5832, 832)       # P, R, n, amount, CI
CHECK_A = (2000, 5, 3, 300, 2300)          # P, R, T, SI, amount
CHECK_B = (5000, 10, 2, 6050, 1050)        # P, R, n, amount, CI


# ---------------------------------------------------------------- furniture --
def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


def row_centres(half_widths, gap, cx=BOARD_CX):
    """x centres for a row of elements whose ink is `gap` apart.

    The row's combined ink is centred on `cx` (the green board's centre line)
    and the elements of a row are not equally wide, so equal centre spacing is
    NOT equal spacing on the board: this returns the centres that leave exactly
    `gap` units of clear air between neighbours.
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


def coin_stack(cx, cy, n=3, scale=1.0, color=CHALK_YELLOW):
    """A stack of rupee coins: filled discs with thickness, drawn bottom-up."""
    discs = VGroup()
    for i in range(n):
        e = Ellipse(width=0.40 * scale, height=0.14 * scale,
                    stroke_color=color, stroke_width=1.4,
                    fill_color=color, fill_opacity=0.38)
        e.move_to(np.array([cx, cy + 0.065 * i * scale, 0.0]))
        discs.add(e)
    return discs


def rupee_note(cx, cy, scale=1.0, color=CHALK_YELLOW):
    """A drawn rupee note: a filled note with its own printed band."""
    body = RoundedRectangle(corner_radius=0.05, width=0.62 * scale,
                            height=0.36 * scale, stroke_color=color,
                            stroke_width=1.6, fill_color=color,
                            fill_opacity=0.30)
    body.move_to(np.array([cx, cy, 0.0]))
    band = Circle(radius=0.09 * scale, stroke_color=color, stroke_width=1.2,
                  fill_color=color, fill_opacity=0.30)
    band.move_to(np.array([cx, cy, 0.0]))
    return VGroup(body, band)


def method_card(name, method, result, color=CHALK_GREEN, kind="coins",
                width=CARD_W, height=CARD_H, name_size=15, line_size=14,
                result_size=14, buff=0.26):
    """One friend's method card: who, which interest, and the money it makes.

    The money (filled coins or a filled note) sits in the card's left margin, so
    the two friends read as two money handlers and not just two rows of words.
    The card's three lines are held `buff` apart -- 0.26, the tightest the
    clearance audit allows two texts to come is 0.22.
    """
    box = panel(width, height, color)
    icon = (coin_stack(-width / 2 + 0.40, -0.14, 3, 0.95, color)
            if kind == "coins"
            else rupee_note(-width / 2 + 0.40, -0.02, 1.05, color))
    head = board_text(name, name_size, color, "BOLD")
    line = board_text(method, line_size, CHALK_WHITE, "BOLD")
    res = board_text(result, result_size, CHALK_YELLOW, "BOLD")
    txt = VGroup(head, line, res).arrange(DOWN, buff=buff, aligned_edge=LEFT)
    txt.move_to(np.array([-width / 2 + 0.92 + txt.width / 2.0, 0.0, 0.0]))
    grp = VGroup(box, icon, txt)
    grp.box, grp.head, grp.line, grp.result, grp.icon = box, head, line, res, icon
    return grp


def padlock(cx, cy, scale=1.0, color=CHALK_RED):
    """The drawn padlock that fixes a simple-interest principal.

    A filled body, a shackle arc over it and a keyhole dot.  It is always
    returned inside the same VGroup as the block it locks, so the audit never
    reads its strokes as a line running into a card.
    """
    body = RoundedRectangle(corner_radius=0.05, width=0.40 * scale,
                            height=0.30 * scale, stroke_color=color,
                            stroke_width=2.0, fill_color=PANEL_FILL,
                            fill_opacity=0.92)
    body.move_to(np.array([cx, cy - 0.05 * scale, 0.0]))
    shackle = Arc(radius=0.12 * scale, start_angle=0.0, angle=PI,
                  stroke_color=color, stroke_width=2.0)
    shackle.move_to(np.array([cx, cy + 0.10 * scale, 0.0]))
    key = Dot(radius=0.03 * scale, color=color).move_to(
        np.array([cx, cy - 0.05 * scale, 0.0]))
    return VGroup(body, shackle, key)


def block_row(label, color=CHALK_GREEN, width=LADDER_W, height=LADDER_H,
              size=13, opacity=0.42, lock_dx=None, text_color=CHALK_WHITE):
    """One solid block of a money ladder, carrying its own amount.

    `lock_dx` is the padlock's x offset from the block's centre (None = no
    padlock).  A lock inside the block's left margin shifts the amount to the
    right; a lock placed outside the block leaves the amount centred.  The
    label is sized so that no word ever touches its own block's edge, and the
    padlock is a member of this block's own VGroup.
    """
    box = RoundedRectangle(corner_radius=0.08, width=width, height=height,
                           stroke_color=color, stroke_width=1.9,
                           fill_color=color, fill_opacity=opacity)
    lab = board_text(label, size, text_color, "BOLD")
    parts = [box]
    inside = lock_dx is not None and lock_dx > -width / 2.0 + 0.06
    if lock_dx is not None:
        parts.append(padlock(lock_dx, 0.0,
                             0.86 * (0.6 + 0.4 * height / LADDER_H)))
    if inside:
        lab.move_to(box.get_center() + RIGHT * 0.28)
    else:
        lab.move_to(box.get_center())
    parts.append(lab)
    grp = VGroup(*parts)
    grp.box, grp.label = box, lab
    return grp


def ladder(x, rows, width=LADDER_W, height=LADDER_H, step=ROW_STEP, size=13,
           y0=-0.42):
    """A column of money blocks, bottom row first.

    `rows` is a list of (label, colour, lock_dx or None).  The blocks are
    returned separately (not as one group) so a single block can be animated --
    merged, slid down, or indicated -- on its own.
    """
    out = []
    for i, row in enumerate(rows):
        label, color = row[0], row[1]
        lock_dx = row[2] if len(row) > 2 else None
        h = row[3] if len(row) > 3 else height
        w = row[4] if len(row) > 4 else width
        out.append(at(block_row(label, color, w, h, size, lock_dx=lock_dx),
                      x, y0 + i * step))
    return out


def factor_card(color=CHALK_AMBER, width=2.30, height=0.78, size=24):
    """The one-period growth factor, boxed: the object that multiplies."""
    box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                           stroke_color=color, stroke_width=2.1,
                           fill_color=PANEL_FILL, fill_opacity=0.55)
    tex = chalk_math(r"\left(1+\frac{R}{100}\right)", size=size, color=color)
    tex.move_to(box.get_center())
    grp = VGroup(box, tex)
    grp.box, grp.tex = box, tex
    return grp


def note_card(head, lines, color=CHALK_CYAN, width=3.40, height=1.05,
              head_size=15, line_size=13, buff=0.28):
    """A card with a bold head line and one or two body lines under it.

    The head and the body are laid out as ONE stack, so the gap between the head
    and the first body line is the full 0.28 the clearance audit asks for.
    """
    box = panel(width, height, color)
    parts = [board_text(head, head_size, color, "BOLD")]
    parts += [board_text(line, line_size, CHALK_WHITE, "BOLD")
              for line in lines]
    txt = VGroup(*parts).arrange(DOWN, buff=buff)
    txt.move_to(box.get_center())
    grp = VGroup(box, txt)
    grp.box, grp.head, grp.body = box, parts[0], VGroup(*parts[1:])
    return grp


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


def wrong_card(text, color=CHALK_RED, width=3.10, height=1.05, size=15):
    """A card holding a WRONG statement, with a drawn cross over it.

    The cross occupies the card's top half and the statement its bottom half, so
    the strike-through is unmistakable yet never comes within the 0.04 units the
    audit allows between a stroke and the lettering.  The whole card is ONE
    board object, so the strokes are never read as a line running into a box.
    """
    box = panel(width, height, color, opacity=0.7)
    cross = VGroup(
        Line(np.array([-width / 2 + 0.60, 0.14, 0.0]),
             np.array([-width / 2 + 1.10, 0.50, 0.0]),
             stroke_color=color, stroke_width=4.2),
        Line(np.array([-width / 2 + 0.60, 0.50, 0.0]),
             np.array([-width / 2 + 1.10, 0.14, 0.0]),
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


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "Ramesh and Sreenu lent the same money to two different borrowers. "
        "<bookmark mark='b0'/>Ramesh lent one hundred rupees at ten percent for "
        "two years, and got back one hundred and twenty rupees. <bookmark "
        "mark='b1'/>Sreenu lent one hundred rupees at the same ten percent, for "
        "the same two years, and got back one hundred and twenty one rupees. "
        "<bookmark mark='b2'/>Same principal, same rate, same time, and yet one "
        "rupee more. <bookmark mark='b3'/>Where did that extra rupee come from? "
        "<bookmark mark='b4'/>The two friends used two different methods. "
        "<bookmark mark='b5'/>Ramesh's method is simple interest, and Sreenu's "
        "method is compound interest."
    ),
    "s1": (
        "Ramesh uses simple interest. <bookmark mark='b0'/>The interest is "
        "always calculated on the original principal, so the base never "
        "changes. <bookmark mark='b1'/>One hundred rupees at ten percent gives "
        "ten rupees of interest every year. <bookmark mark='b2'/>Year one pays "
        "ten rupees, and year two pays ten rupees again, because the base is "
        "still the original one hundred. <bookmark mark='b3'/>Ten plus ten is "
        "twenty, so the amount is one hundred plus twenty, that is one hundred "
        "and twenty rupees. <bookmark mark='b4'/>Simple interest is P times T "
        "times R, divided by one hundred. <bookmark mark='b5'/>For example, two "
        "thousand five hundred rupees at twelve percent for three years gives "
        "nine hundred rupees of interest, <bookmark mark='b6'/>and the amount is "
        "three thousand four hundred rupees."
    ),
    "s2": (
        "Sreenu uses compound interest. <bookmark mark='b0'/>Here each new "
        "amount becomes the next principal, so the base itself grows. "
        "<bookmark mark='b1'/>In year one, ten percent of one hundred is ten "
        "rupees, so the amount is one hundred and ten rupees. <bookmark "
        "mark='b2'/>That one hundred and ten rupees is now the principal for "
        "year two. <bookmark mark='b3'/>In year two, ten percent of one hundred "
        "and ten is eleven rupees, so the amount becomes one hundred and twenty "
        "one rupees. <bookmark mark='b4'/>The second interest is eleven rupees, "
        "one rupee more than the first. <bookmark mark='b5'/>That extra rupee "
        "is ten percent of the first year's ten rupees of interest: <bookmark "
        "mark='b6'/>the interest itself earned interest."
    ),
    "s3": (
        "Watch one period only. <bookmark mark='b0'/>In one period the amount "
        "is the principal plus the interest on it: A one equals P plus P R over "
        "one hundred. <bookmark mark='b1'/>Take P outside the bracket, and the "
        "same amount is P times one plus R over one hundred. <bookmark "
        "mark='b2'/>The bracket, one plus R over one hundred, is the one period "
        "growth factor. <bookmark mark='b3'/>Whatever the principal is, "
        "<bookmark mark='b4'/>one period multiplies it by that same factor."
    ),
    "s4": (
        "Now the second year. <bookmark mark='b0'/>The amount from year one "
        "becomes the principal for year two. <bookmark mark='b1'/>So the same "
        "growth factor multiplies again. <bookmark mark='b2'/>A two equals P "
        "times one plus R over one hundred, times one plus R over one hundred "
        "once more. <bookmark mark='b3'/>Which is P into the square of one plus "
        "R over one hundred. <bookmark mark='b4'/>Two years means two factors, "
        "and two factors compress into one single power. <bookmark "
        "mark='b5'/>That power is the square, and every extra year adds one "
        "more."
    ),
    "s5": (
        "One factor for every year. <bookmark mark='b0'/>Year one multiplies by "
        "the growth factor, year two multiplies again, year three multiplies "
        "again, and so on up to year n. <bookmark mark='b1'/>Repeated "
        "multiplication by the same number compresses into a power. <bookmark "
        "mark='b2'/>So the amount after n years is A equals P times one plus R "
        "over one hundred, raised to the power n. <bookmark mark='b3'/>The "
        "exponent n is not a decoration. <bookmark mark='b4'/>It is the number "
        "of growth periods."
    ),
    "s6": (
        "Careful: this formula gives the amount. <bookmark mark='b0'/>The amount "
        "is the principal plus the interest, so it is not the interest itself. "
        "<bookmark mark='b1'/>The compound interest is the amount minus the "
        "principal. <bookmark mark='b2'/>So C I equals A minus P, which is P "
        "times one plus R over one hundred to the power n, minus P. <bookmark "
        "mark='b3'/>For one hundred rupees at ten percent for two years, the "
        "amount is one hundred and twenty one rupees, <bookmark mark='b4'/>and "
        "the interest is twenty one rupees."
    ),
    "s7": (
        "Let us use it with real numbers. Take P equals five thousand rupees, R "
        "equals eight percent, and n equals two years. <bookmark mark='b0'/>One "
        "plus eight over one hundred is one point zero eight, so the amount is "
        "five thousand times one point zero eight squared. <bookmark "
        "mark='b1'/>That is five thousand eight hundred and thirty two rupees. "
        "<bookmark mark='b2'/>The compound interest is the amount minus the "
        "principal. <bookmark mark='b3'/>Five thousand eight hundred and thirty "
        "two minus five thousand is eight hundred and thirty two rupees. "
        "<bookmark mark='b4'/>So the compound interest is eight hundred and "
        "thirty two rupees, <bookmark mark='b5'/>and not five thousand eight "
        "hundred and thirty two."
    ),
    "s8": (
        "Put the two ladders side by side. <bookmark mark='b0'/>On the simple "
        "interest ladder the principal stays locked at one hundred, so both "
        "years add the same ten rupees, and the amount is one hundred and "
        "twenty. <bookmark mark='b1'/>On the compound ladder the first year "
        "makes one hundred and ten, and that becomes the base, so the second "
        "year adds eleven rupees, and the amount is one hundred and twenty one. "
        "<bookmark mark='b2'/>Now look at the first year: both ladders add the "
        "same ten rupees, because both started from the original principal. "
        "<bookmark mark='b3'/>After that, simple interest keeps adding the same "
        "block, <bookmark mark='b4'/>while compound interest adds a bigger "
        "block, because its base grows."
    ),
    "s9q": (
        "Your turn. Four quick checks. <bookmark mark='b0'/>A: simple interest "
        "on two thousand rupees at five percent for three years. <bookmark "
        "mark='b1'/>B: compound interest on five thousand rupees at ten percent "
        "for two years. <bookmark mark='b2'/>C: every year the interest is "
        "calculated on five thousand rupees. <bookmark mark='b3'/>And next "
        "year's interest is calculated on the previous year's amount. <bookmark "
        "mark='b4'/>D: after the first year, are simple and compound interest "
        "different?"
    ),
    "s9a": (
        "Let us check the four answers. <bookmark mark='b0'/>A: two thousand "
        "times three times five, divided by one hundred, is three hundred "
        "rupees, so the amount is two thousand three hundred. <bookmark "
        "mark='b1'/>B: five thousand times one point one squared is six thousand "
        "and fifty, so the compound interest is one thousand and fifty. "
        "<bookmark mark='b2'/>C: interest on five thousand rupees every year is "
        "simple interest, and interest on the previous year's amount is compound "
        "interest. <bookmark mark='b3'/>D: no, after the first period they are "
        "the same, because both used the original principal."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>Simple interest keeps the original "
        "principal as the base, so every year adds the same interest. <bookmark "
        "mark='b1'/>Compound interest lets each new amount become the next base, "
        "so the interest itself grows. <bookmark mark='b2'/>We derived it: A "
        "one, then A two, then A equals P times one plus R over one hundred, to "
        "the power n. <bookmark mark='b3'/>And the formula gives the amount, so "
        "the compound interest is A minus P. <bookmark mark='b4'/>Simple stays "
        "on the original base; compound grows on the new base. <bookmark "
        "mark='b5'/>Thank you for watching, <bookmark mark='b6'/>and see you in "
        "the next lesson."
    ),
}

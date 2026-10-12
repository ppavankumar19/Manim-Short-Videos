"""Board furniture and narration for Storyboard 02 -- Percentage Increases,
Decreases & Quick Estimation Rules on Bills, Class 8 Mathematics, Chapter 5
(Comparing Quantities using Proportion).

This file is *spliced*, never imported: assemble_percentage.py grafts it into
the proven head of the Chapter 3 quadrilaterals set, so the theme names
(CHALK_*, FONT, BOARD_*), `board_text`, `chalk_math`, `appear` and the pacing
helpers (`rt`, `quick`, `leftover`) are already defined above it.

The furniture is this video's "percentage on a bill" kit:

  * `mode_panel`    -- the persistent percentage control panel: the three modes
                       CONVERT / CHANGE / ESTIMATE with the live one lit,
  * `percent_grid`  -- the hundred-cell percentage square that fills cell by
                       cell (Group A lights 75 cells, Group B lights 80),
  * `pct_bar` / `pct_block` -- the 100% original and the block that ATTACHES
                       for an increase,
  * `decade_row`    -- ten ten-percent blocks: the last one can detach and
                       LEAVE, which is how a decrease is drawn,
  * `split_block`   -- one ten-percent block that splits in half into two 5%,
  * `money_note`, `coin_stack`, `money_bag` -- drawn money (filled, shaded),
  * `price_tag`     -- a shop tag with a punched hole and a string,
  * `receipt`       -- a filled bill with ruled lines,
  * `number_ruler`  -- the ruler the bill snaps along from 477.80 to 480,
  * `wrong_card` / `cross_out` / `tick` -- the drawn cross and tick (Segoe
                       Print has neither glyph).

Everything is drawn as filled, shaded geometry -- notes with a printed inner
frame, coins with thickness, a bag with a tied neck, solid blocks -- never as a
bare outline.
"""
from __future__ import annotations

import numpy as np

# ------------------------------------------------------------ board layout --
# (this section is spliced into a head whose own imports omit Ellipse and Arc;
#  Dot, Circle, Line, DashedLine, Polygon, Rectangle, RoundedRectangle, Square,
#  VGroup, DEGREES and np are already imported by the head)
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

# The three content lines.  PANEL_Y carries the percentage control panel, which
# stays on the board in every teaching scene; ROW_A holds the diagram, ROW_B the
# numbers under it and ROW_C the rule chip above the banner.  The rows are set
# so that no two texts come within the 0.22 units the clearance audit asks for,
# including the banner text sitting at -1.15.
PANEL_Y = 1.52
ROW_A = 0.88
ROW_B = 0.02
ROW_C = -0.60

PANEL_FILL = "#16202B"
MODE_W = 1.58            # one control-panel mode chip
MODE_H = 0.44
CHIP_H = 0.50
CARD_W = 3.30
CARD_H = 0.94
MARK_SIZE = 18
DOT_R = 0.075
COIN_R = 0.17

# The figures this video works with.  The bill is the series' own estimation
# example: it rounds to a number that is easier without changing much.
GROUP_A = ("Group A", 225, 300, CHALK_GREEN)
GROUP_B = ("Group B", 200, 250, CHALK_CYAN)
SALES = "Rs 98,700"
BILL = 477.80
ROUNDED_BILL = 480.0

# The miniature number line the bill snaps along (470 ... 490).
NL_LO, NL_HI = 470.0, 490.0
NL_W = 4.60
NL_Y = 0.95
MODES = (("CONVERT", CHALK_GREEN), ("CHANGE", CHALK_AMBER),
         ("ESTIMATE", CHALK_CYAN))


# ---------------------------------------------------------------- furniture --
def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


def write_board_file(path, text: str) -> None:
    """Write a board artefact (the ground-truth SRT), surviving Windows' limit.

    This topic's media folder is 211 characters deep and `<Class>.real.srt`
    pushes the full name to exactly 260 -- one over what a plain open accepts on
    a machine whose long-path support is off (measured here:
    LongPathsEnabled = 0).  The write therefore falls back to the `\\\\?\\` form,
    which the OS always accepts.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        path.write_text(text, encoding="utf-8")
    except OSError:
        with open("\\\\?\\" + str(path.resolve()), "w",
                  encoding="utf-8") as handle:
            handle.write(text)


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


def mode_panel(active="CONVERT"):
    """The percentage control panel: three modes, the live one lit.

    It sits on the same line of the board in every teaching scene, so the
    viewer always knows which of the three moves the board is on.  The inactive
    modes stay visible but dimmed -- they are furniture, never a surprise.
    """
    row = VGroup()
    for name, color in MODES:
        lit = active in (name, "ALL")
        c = chip(name, color if lit else CHALK_WHITE, size=13, width=MODE_W,
                 height=MODE_H)
        if not lit:
            c.set_opacity(0.40)
        row.add(c)
    row.arrange(RIGHT, buff=0.26)
    return at(row, BOARD_CX, PANEL_Y)


def percent_grid(fill_n, color=CHALK_GREEN, cell=0.100, gap=0.012,
                 rows=10, cols=10):
    """The hundred-cell percentage square: `fill_n` cells lit, the rest waiting.

    The cells are lit one at a time (the caller runs a LaggedStart over
    `grp.lit`), so "75 out of 100" is something the viewer watches happen rather
    than a number that is simply asserted.
    """
    step = cell + gap
    cells, lit = VGroup(), VGroup()
    for i in range(rows * cols):
        r, c = divmod(i, cols)
        sq = Square(side_length=cell, stroke_color=CHALK_WHITE,
                    stroke_width=0.8, fill_color=color, fill_opacity=0.06)
        sq.set_stroke(opacity=0.40)
        sq.move_to(np.array([(c - (cols - 1) / 2.0) * step,
                             ((rows - 1) / 2.0 - r) * step, 0.0]))
        cells.add(sq)
        if i < fill_n:
            lit.add(sq)
    grp = VGroup(cells)
    grp.cells, grp.lit = cells, lit
    return grp


def pct_bar(width=2.20, height=0.50, color=CHALK_GREEN,
            label="100% ORIGINAL", size=14):
    """The whole, drawn as one bar: every change is measured from this."""
    box = RoundedRectangle(corner_radius=0.05, width=width, height=height,
                           stroke_color=color, stroke_width=2.0,
                           fill_color=color, fill_opacity=0.22)
    grp = VGroup(box)
    grp.box = box
    if label:
        lab = board_text(label, size, CHALK_WHITE, "BOLD")
        lab.move_to(box.get_center())
        grp.add(lab)
        grp.label = lab
    return grp


def pct_block(width, height=0.50, color=CHALK_AMBER, label=None, size=13):
    """One coloured block: the piece that attaches (or leaves) the 100% bar."""
    box = Rectangle(width=width, height=height, stroke_color=color,
                    stroke_width=2.2, fill_color=color, fill_opacity=0.34)
    grp = VGroup(box)
    grp.box = box
    if label:
        lab = board_text(label, size, CHALK_WHITE, "BOLD")
        lab.move_to(box.get_center())
        grp.add(lab)
        grp.label = lab
    return grp


def decade_row(n=10, cell=0.26, gap=0.03, color=CHALK_CYAN, height=0.52):
    """Ten equal blocks: one block is one tenth, so the row is the whole 100%.

    A decrease is drawn by letting the last block detach and leave, which is
    visibly the opposite of the block that attaches for an increase.
    """
    row = VGroup()
    for _ in range(n):
        row.add(Rectangle(width=cell, height=height, stroke_color=color,
                          stroke_width=1.6, fill_color=color,
                          fill_opacity=0.30))
    row.arrange(RIGHT, buff=gap)
    row.cell_w = cell
    return row


def split_block(width=1.20, height=0.54, color=CHALK_AMBER):
    """One ten-percent block that halves into two five-percent blocks.

    Both halves, their labels and the divider live in ONE VGroup, so the halves
    can slide apart without their wording being left behind.
    """
    half = (width - 0.06) / 2.0
    boxes = VGroup(
        Rectangle(width=half, height=height, stroke_color=color,
                  stroke_width=2.0, fill_color=color, fill_opacity=0.32),
        Rectangle(width=half, height=height, stroke_color=color,
                  stroke_width=2.0, fill_color=color, fill_opacity=0.32),
    ).arrange(RIGHT, buff=0.06)
    left = VGroup(boxes[0],
                  board_text("5%", 13, CHALK_WHITE, "BOLD"
                             ).move_to(boxes[0].get_center()))
    right = VGroup(boxes[1],
                   board_text("5%", 13, CHALK_WHITE, "BOLD"
                              ).move_to(boxes[1].get_center()))
    grp = VGroup(left, right)
    grp.half_l, grp.half_r = left, right
    return grp


def money_note(width=1.70, height=0.80, color=CHALK_GREEN,
               text="Rs 34,545", size=13):
    """A drawn rupee note: a filled, shaded rectangle with a printed frame."""
    body = RoundedRectangle(corner_radius=0.06, width=width, height=height,
                            stroke_color=color, stroke_width=2.2,
                            fill_color=color, fill_opacity=0.24)
    inner = RoundedRectangle(corner_radius=0.04, width=width - 0.22,
                             height=height - 0.22, stroke_color=color,
                             stroke_width=1.1, fill_color=color,
                             fill_opacity=0.10)
    inner.set_stroke(opacity=0.6)
    inner.move_to(body.get_center())
    lab = board_text(text, size, CHALK_WHITE, "BOLD").move_to(body.get_center())
    grp = VGroup(body, inner, lab)
    grp.box, grp.label = body, lab
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


def money_bag(cx, cy, scale=1.0, color=CHALK_AMBER, text="SALES",
              size=15, coins=True):
    """The money bag: a filled, shaded bag with a tied neck (and coins)."""
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


def price_tag(width=2.30, height=0.86, color=CHALK_PINK, text="Rs 550",
              size=15):
    """A shop price tag: a filled tag shape, a punched hole and a string."""
    tip = height * 0.5
    body = Polygon(
        np.array([-width / 2, height / 2, 0.0]),
        np.array([width / 2 - tip, height / 2, 0.0]),
        np.array([width / 2, 0.0, 0.0]),
        np.array([width / 2 - tip, -height / 2, 0.0]),
        np.array([-width / 2, -height / 2, 0.0]),
        stroke_color=color, stroke_width=2.4, fill_color=color,
        fill_opacity=0.24)
    hole = Circle(radius=0.072, stroke_color=color, stroke_width=1.6,
                  fill_color=PANEL_FILL, fill_opacity=0.9)
    hole.move_to(np.array([-width / 2 + 0.20, 0.0, 0.0]))
    loop = Arc(radius=0.16, start_angle=150 * DEGREES, angle=120 * DEGREES,
               arc_center=np.array([-width / 2 + 0.02, 0.22, 0.0]),
               stroke_color=CHALK_WHITE, stroke_width=1.8)
    lab = board_text(text, size, CHALK_WHITE, "BOLD")
    lab.move_to(np.array([-width / 2 + 0.34 + (width - tip - 0.40) / 2.0,
                          0.0, 0.0]))
    grp = VGroup(body, hole, loop, lab)
    grp.body, grp.label = body, lab
    return grp


def receipt(width=1.70, height=1.00, color=CHALK_CYAN, head="BILL",
            value="Rs 477.80"):
    """The bill itself: a filled slip with a heading and the amount on it.

    The ruled lines are thin filled bars rather than strokes, so no line ever
    runs through the lettering.
    """
    body = RoundedRectangle(corner_radius=0.06, width=width, height=height,
                            stroke_color=color, stroke_width=2.2,
                            fill_color=color, fill_opacity=0.18)
    h = board_text(head, 13, color, "BOLD")
    h.move_to(body.get_center() + UP * 0.30)
    v = board_text(value, 13, CHALK_WHITE, "BOLD")
    v.move_to(body.get_center() + DOWN * 0.26)
    bars = VGroup()
    for yy in (0.10, 0.02):
        b = Rectangle(width=width - 0.46, height=0.035, stroke_width=0,
                      fill_color=CHALK_WHITE, fill_opacity=0.35)
        b.move_to(body.get_center() + UP * yy)
        bars.add(b)
    grp = VGroup(body, bars, h, v)
    grp.box, grp.head, grp.value = body, h, v
    return grp


def nl_x(value):
    """The board x of a number on the ruler."""
    mid = (NL_LO + NL_HI) / 2.0
    return BOARD_CX + (float(value) - mid) / (NL_HI - NL_LO) * NL_W


def number_ruler(lo=NL_LO, hi=NL_HI, y=NL_Y, width=NL_W, step=5,
                 color=CHALK_WHITE, size=13):
    """The ruler the bill snaps along: a bar with a tick and a label each step."""
    axis = Line(np.array([BOARD_CX - width / 2, y, 0.0]),
                np.array([BOARD_CX + width / 2, y, 0.0]),
                stroke_color=color, stroke_width=2.2)
    ticks, labels = VGroup(), VGroup()
    v = lo
    while v <= hi + 1e-6:
        x = nl_x(v)
        ticks.add(Line(np.array([x, y, 0.0]), np.array([x, y - 0.14, 0.0]),
                       stroke_color=color, stroke_width=1.8))
        lab = board_text(f"{int(v)}", size, color, "BOLD")
        lab.move_to(np.array([x, y - 0.34, 0.0]))
        labels.add(lab)
        v += step
    grp = VGroup(axis, ticks, labels)
    grp.axis, grp.ticks, grp.labels = axis, ticks, labels
    return grp


def note_card(head, lines, color=CHALK_CYAN, width=3.40, height=1.05,
              head_size=15, line_size=13):
    """A card with a bold head line and one or two body lines under it.

    The head and the body are held 0.26 units apart, so the pair passes the
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


def cross_out(mob, color=CHALK_RED, pad=0.10):
    """A drawn cross over a mobject (Segoe Print has no cross glyph)."""
    x0, y0 = mob.get_left()[0] - pad, mob.get_bottom()[1] - pad
    x1, y1 = mob.get_right()[0] + pad, mob.get_top()[1] + pad
    return VGroup(
        Line(np.array([x0, y0, 0.0]), np.array([x1, y1, 0.0]),
             stroke_color=color, stroke_width=4.2),
        Line(np.array([x0, y1, 0.0]), np.array([x1, y0, 0.0]),
             stroke_color=color, stroke_width=4.2))


def wrong_card(text, color=CHALK_RED, width=2.30, height=0.85, size=13):
    """A card holding a WRONG statement, with a drawn cross over it.

    The cross occupies the card's top half and the statement its bottom half, so
    the strike-through is unmistakable yet never comes within the 0.04 units the
    audit allows between a stroke and the lettering.  The whole card is ONE
    board object, so the strokes are never read as a line running into a box.
    """
    box = panel(width, height, color, opacity=0.7)
    cross = VGroup(
        Line(np.array([-width / 2 + 0.45, 0.10, 0.0]),
             np.array([-width / 2 + 0.90, 0.38, 0.0]),
             stroke_color=color, stroke_width=4.2),
        Line(np.array([-width / 2 + 0.45, 0.38, 0.0]),
             np.array([-width / 2 + 0.90, 0.10, 0.0]),
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
        "Suppose two school groups are selling tickets for the annual function. "
        "<bookmark mark='b0'/>Group A sold 225 tickets out of 300. <bookmark "
        "mark='b1'/>Group B sold 200 tickets out of 250. <bookmark mark='b2'/>"
        "The two totals are different, so the numbers 225 and 200 cannot be "
        "compared directly. <bookmark mark='b3'/>Who actually did better? "
        "<bookmark mark='b4'/>A percentage puts different totals onto one "
        "common scale, and that scale is always out of one hundred."
    ),
    "s1": (
        "Now let us convert both groups to one common scale. <bookmark "
        "mark='b0'/>Both 225 out of 300 and 200 out of 250 can be written as "
        "fractions. 225 out of 300 is 3 over 4, which is 75 out of 100, so that "
        "is 75 percent. <bookmark mark='b1'/>200 out of 250 is 4 over 5, which "
        "is 80 out of 100, so that is 80 percent. <bookmark mark='b2'/>So group "
        "B is closer to the target. <bookmark mark='b3'/>The rule is: "
        "percentage equals part divided by whole, multiplied by one hundred. "
        "<bookmark mark='b4'/>And always name the whole, because the percentage "
        "is measured from that reference."
    ),
    "s2": (
        "Now think about a change. <bookmark mark='b0'/>Suppose a value grows "
        "by 35 percent. Start with the original value drawn as a full bar of "
        "one hundred percent. <bookmark mark='b1'/>A 35 percent increase "
        "attaches one more block to that bar. <bookmark mark='b2'/>The original "
        "hundred percent and the new thirty five percent together make one "
        "hundred and thirty five percent. <bookmark mark='b3'/>So a 35 percent "
        "increase means the new value is 135 percent of the original. <bookmark "
        "mark='b4'/>The increase is always measured from the original, never "
        "from the new value."
    ),
    "s3": (
        "Let us apply that to money. <bookmark mark='b0'/>Last month the sales "
        "were Rs 98,700. <bookmark mark='b1'/>This month they are up by 35 "
        "percent. <bookmark mark='b2'/>First find the increase: 35 over 100 "
        "times 98,700 is Rs 34,545. <bookmark mark='b3'/>Then add it to the "
        "original: 98,700 plus 34,545 gives Rs 1,33,245. <bookmark mark='b4'/>"
        "Here is the shortcut: 135 percent of 98,700 is the same Rs 1,33,245, "
        "because the new value is 135 percent of the old one."
    ),
    "s4": (
        "Now the other direction. <bookmark mark='b0'/>A price tag shows "
        "Rs 550, and the shop offers 10 percent off. <bookmark mark='b1'/>Ten "
        "percent of 550 is Rs 55. <bookmark mark='b2'/>Take it away: 550 minus "
        "55 is Rs 495, and that is what you pay. <bookmark mark='b3'/>Now "
        "compare the two changes on one panel. An increase of p percent gives "
        "100 percent plus p percent. <bookmark mark='b4'/>A decrease of p "
        "percent gives 100 percent minus p percent, so 10 percent off leaves 90 "
        "percent."
    ),
    "s5": (
        "Here is the mental toolkit. <bookmark mark='b0'/>Ten percent is one "
        "tenth, so move the decimal point one place. <bookmark mark='b1'/>Five "
        "percent is half of ten percent. <bookmark mark='b2'/>Fifteen percent "
        "is ten percent plus five percent, and twenty percent is simply two "
        "tens. <bookmark mark='b3'/>A common mistake is to say that five percent "
        "is half of twenty percent; the cross shows that this is wrong. "
        "<bookmark mark='b4'/>Now use 480: ten percent is 48, five percent is "
        "24, so fifteen percent is 72. Build hard percentages out of ten "
        "percent."
    ),
    "s6": (
        "Now use that on a bill. <bookmark mark='b0'/>The bill is Rs 477.80, "
        "which is awkward, so round it to Rs 480. <bookmark mark='b1'/>Ten "
        "percent of 480 is 48. <bookmark mark='b2'/>Five percent is half of "
        "that, so 24, and fifteen percent is 48 plus 24, that is 72. <bookmark "
        "mark='b3'/>Subtract that from the rounded bill: 480 minus 72 is 408. "
        "<bookmark mark='b4'/>So you pay about Rs 410, and the approximation "
        "sign stays on the board, because this is an estimate."
    ),
    "s7": (
        "Let us put the two lanes side by side. <bookmark mark='b0'/>The exact "
        "lane works with the real bill: fifteen percent of 477.80 is Rs 71.67, "
        "and 477.80 minus 71.67 is 406.13. <bookmark mark='b1'/>The mental lane "
        "rounded the bill to 480 and used 72, which gave about 408, or about "
        "410. <bookmark mark='b2'/>The two answers are close, so the estimate "
        "is sensible. <bookmark mark='b3'/>Remember: an estimate is a "
        "reasonableness check, not exact arithmetic. <bookmark mark='b4'/>The "
        "exact lane is only there to show that the quick answer is believable."
    ),
    "s8": (
        "So here is the decision map. <bookmark mark='b0'/>To convert, divide "
        "the part by the whole and multiply by one hundred. <bookmark "
        "mark='b1'/>To handle an increase, add the percentage to one hundred. "
        "<bookmark mark='b2'/>To handle a decrease, subtract it from one "
        "hundred. <bookmark mark='b3'/>To estimate, round the number first, and "
        "then build the percentage from ten percent. <bookmark mark='b4'/>Four "
        "moves: convert, change, estimate, and check."
    ),
    "s9q": (
        "Your turn. Four quick checks. <bookmark mark='b0'/>A: convert 18 out "
        "of 24 into a percentage. <bookmark mark='b1'/>B: find the price of an "
        "item marked Rs 800 with 10 percent off. <bookmark mark='b2'/>C: "
        "estimate 20 percent of Rs 357.30 by first rounding it to 360. "
        "<bookmark mark='b3'/>D: increase Rs 900 by 35 percent. Now pause the "
        "video, work all four out on paper, and then we will check every "
        "answer."
    ),
    "s9a": (
        "Let us check every answer. <bookmark mark='b0'/>A: 18 out of 24 is "
        "three quarters, so it is 75 percent. <bookmark mark='b1'/>B: ten "
        "percent of 800 is 80, so 800 minus 80 is Rs 720. <bookmark "
        "mark='b2'/>C: twenty percent of 360 is two tens of 36, which is 36 "
        "plus 36, so it is about Rs 72. <bookmark mark='b3'/>D: 135 percent of "
        "900 is Rs 1,215, because 900 plus 315 gives 1,215. Every answer used "
        "the whole as its base."
    ),
    "s10": (
        "Let us put it together. <bookmark mark='b0'/>One: compare, because a "
        "percentage is always out of one hundred. <bookmark mark='b1'/>Two: "
        "change, where an increase adds to one hundred percent and a decrease "
        "subtracts from it. <bookmark mark='b2'/>Three: estimate, by rounding "
        "first and then building the percentage from ten percent. <bookmark "
        "mark='b3'/>Four: check, because an estimate is a reasonableness check "
        "and not exact arithmetic. <bookmark mark='b4'/>Compare, change, "
        "estimate, check. <bookmark mark='b5'/>Thank you for watching, "
        "<bookmark mark='b6'/>and see you in the next lesson."
    ),
}

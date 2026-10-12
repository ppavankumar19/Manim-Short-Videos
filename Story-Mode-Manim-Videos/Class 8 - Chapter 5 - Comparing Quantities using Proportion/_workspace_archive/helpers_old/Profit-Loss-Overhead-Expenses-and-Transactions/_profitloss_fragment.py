"""Board furniture and narration for Storyboard 02 -- Profit, Loss & Overhead
Expenses: Solving Single and Double Transaction Problems, Class 8 Mathematics,
Chapter 5 (Comparing Quantities using Proportion).

This file is *spliced*, never imported: assemble_profitloss.py grafts it into
the proven head of the Chapter 3 quadrilaterals set, so the theme names
(CHALK_*, FONT, BOARD_*), `board_text`, `chalk_math`, `appear` and the pacing
helpers (`rt`, `quick`, `leftover`) are already defined above it.

The furniture is this video's shopkeeper's kit -- everything is drawn as filled,
shaded geometry, never as a bare outline:

  * `ledger_frame`  -- the persistent two-column TRANSACTION LEDGER
                       (MONEY OUT | MONEY IN) with its own column rule,
  * `two_col_row`   -- one line of that ledger: label left, amount right, in
                       fixed columns so every row's figures line up,
  * `total_box`     -- the shaded TOTAL COST PRICE box the expenses flow into,
  * `balance_rig`   -- the two-pan balance that compares money out with money
                       in (the side carrying more money rises): the money-in
                       side rising is a profit, the money-out side rising is a
                       loss,
  * `mini_ledger`   -- a small one-item ledger; two of them merge into the
                       single total ledger,
  * `formula_card` / `math_card` -- cards whose body IS one piece of board maths,
  * `refrigerator`, `flat_icon`, `table_icon`, `bicycle_icon`, `tv_icon`,
    `banana_bunch`, `truck_icon`, `wrench_icon` -- the drawn, filled items and
    the expense-tag icons,
  * `cross_out` / `wrong_card` -- the drawn cross and the struck-through card
    (Segoe Print has neither a cross nor a tick glyph).

`.venv/Scripts/python.exe` only ever imports the assembled module, never this
file.
"""
from __future__ import annotations

import numpy as np

# ------------------------------------------------------------ board layout --
# (this section is spliced into a head whose own imports omit Arc, Ellipse,
#  Rotate and Sector; Dot, Circle, Line, Polygon, Square, RoundedRectangle,
#  Arrow, VGroup, DEGREES, PI and np are already imported by the head)
from manim import Arc, Ellipse, Rotate, Sector  # noqa: E402,F401

# Board grid shared by every scene of this video.
ROW_Y = 2.72             # every scene heading sits on this line
SUB_Y = 2.16             # the one-line sub-heading under it
BANNER_Y = -1.15         # the banner line (kept clear: the ledgers reach it)
# The burned-in caption grows up from the bottom of the frame: a one-line cue
# starts at y = -3.38 and a wrapped two-line cue reaches y = -2.93 (measured on
# the series' own burned 360p cuts), so every closing strip sits at -1.80 and
# nothing at all sits below CAPTION_SAFE_Y = -2.00 -- audited by the
# IN-CAPTION-BAND check.
STRIP_Y = -1.80
CAPTION_SAFE_Y = -2.00

BAND_A = 0.75            # the upper content band
BAND_B = -0.65           # the lower content band

PANEL_FILL = "#16202B"
CARD_W = 3.30            # the standard card width
CARD_H = 0.94            # the standard card height
CHIP_H = 0.50
MARK_SIZE = 15           # ONE letter size for every row tag

# -- the transaction ledger -------------------------------------------------
# Absolute board coordinates: the ledger is centred on the board's own centre
# line, so every scene's ledger is the same object in the same place.
LEDGER_W = 9.00          # wider than 8.00 on purpose: a full-width panel must
LEDGER_H = 2.94          # never read as a card the clearance audit measures
LEDGER_CY = 0.16         # the frame spans y [-1.31 .. 1.63]
LEDGER_SPLIT = 5.20      # divider at x = BOARD_CX - LEDGER_W/2 + LEDGER_SPLIT
LED_TITLE_Y = 1.36
LED_COL_Y = 0.90
LED_ROW_Y = (0.44, -0.04, -0.52)     # three stacked item rows, 0.48 apart
LED_TOTAL_Y = -1.00
LED_OUT_L, LED_OUT_R = -3.80, 0.85   # the money-out column
LED_IN_L, LED_IN_R = 1.60, 4.80      # the money-in column
LED_OUT_CX = (LED_OUT_L + LED_OUT_R) / 2.0   # -1.475
LED_IN_CX = (LED_IN_L + LED_IN_R) / 2.0      # 3.20

# The example figures this video works with: examples on the board, never
# textbook facts.
FRIDGE_BUY, FRIDGE_MOVE, FRIDGE_FIX, FRIDGE_SELL = 5000, 100, 500, 7000
FLAT_BUY, FLAT_FIX, FLAT_SELL = 450000, 10000, 425500
TABLE_SP, PLUS_PC, MINUS_PC = 3000, 20, 20
BANANA_BUY, BANANA_MOVE, BANANA_SELL = 1250, 250, 1575
CYCLE_BUY, CYCLE_MOVE, CYCLE_FIX, CYCLE_SELL = 4000, 200, 300, 5400
TV_SP = 9900


# --------------------------------------------------------------- furniture --
def write_text_long(path, text: str) -> None:
    """Write a text file, through the extended-length path when needed.

    This topic's media paths -- `...\\media\\videos\\
    profit_loss_overhead_expenses_and_transactions\\360p30\\<Class>.real.srt` --
    run past the 260-character MAX_PATH limit, which is why the chapter pipeline
    renders into the short `D:\\m3` media dir and copies the result back here.
    The copy-back and this ground-truth SRT write therefore fall back to the
    ``\\\\?\\`` extended form when the plain path is too long for the OS.
    """
    try:
        Path(path).write_text(text, encoding="utf-8")
    except OSError:
        with open("\\\\?\\" + str(Path(path).resolve()), "w",
                  encoding="utf-8") as fh:
            fh.write(text)


def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


def panel(width, height, color=CHALK_WHITE, opacity=0.6, radius=0.10,
          stroke=1.9):
    """A rounded panel: the box every card, chip and ledger is drawn on."""
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


def two_col_row(lab, val, span, color=CHALK_WHITE, size=13):
    """One ledger line: its label flush left, its amount flush right.

    The row is built at the origin with a FIXED width `span`, so `at()` puts
    the label column and the amount column on the same two vertical lines in
    every row of every ledger of this video.  Fixed columns, not centring: a
    centred row puts each label at a different x.
    """
    a = board_text(lab, size, color, "BOLD")
    b = board_text(val, size, CHALK_WHITE, "BOLD")
    a.move_to(np.array([-span / 2.0 + a.width / 2.0, 0.0, 0.0]))
    b.move_to(np.array([span / 2.0 - b.width / 2.0, 0.0, 0.0]))
    grp = VGroup(a, b)
    grp.label, grp.value = a, b
    return grp


def ledger_line(lab, val, y, color=CHALK_WHITE, size=13,
                x_left=LED_OUT_L, x_right=LED_OUT_R):
    """One ledger line already pinned to its row of the money-out column."""
    return at(two_col_row(lab, val, x_right - x_left, color, size),
              (x_left + x_right) / 2.0, y)


def ledger_frame(width=LEDGER_W, height=LEDGER_H, cx=BOARD_CX, cy=LEDGER_CY,
                 split=LEDGER_SPLIT, title="TRANSACTION LEDGER",
                 left_head="MONEY OUT", right_head="MONEY IN",
                 color=CHALK_AMBER, rule_bot=None):
    """The two-column TRANSACTION LEDGER: one panel, one column rule.

    The rule and the panel are ONE mobject, so the clearance audit never reads
    the rule as a line running into a *foreign* box.  It is still a chalk
    stroke, though, so it must never cross any lettering either: the ledger's
    own title therefore sits over the money-out column, clear of the rule's
    x, and a scene whose lower rows straddle the rule (the merged total ledger)
    passes a `rule_bot` that stops the rule above them.
    """
    box = panel(width, height, color, opacity=0.56, radius=0.14, stroke=2.2)
    box.move_to(np.array([cx, cy, 0.0]))
    rx = cx - width / 2.0 + split
    y0 = box.get_bottom()[1] + 0.16 if rule_bot is None else float(rule_bot)
    rule = Line(np.array([rx, y0, 0.0]),
                np.array([rx, box.get_top()[1] - 0.16, 0.0]),
                stroke_color=color, stroke_width=1.6, stroke_opacity=0.7)
    head = board_text(title, 15, color, "BOLD")
    head.move_to(np.array([cx - 1.10, box.get_top()[1] - 0.28, 0.0]))
    lh = board_text(left_head, 12, CHALK_CYAN, "BOLD")
    lh.move_to(np.array([(box.get_left()[0] + rx) / 2.0,
                         box.get_top()[1] - 0.74, 0.0]))
    rh = board_text(right_head, 12, CHALK_PINK, "BOLD")
    rh.move_to(np.array([(rx + box.get_right()[0]) / 2.0,
                         box.get_top()[1] - 0.74, 0.0]))
    grp = VGroup(box, rule, head, lh, rh)
    grp.box, grp.rule, grp.head = box, rule, head
    grp.left_head, grp.right_head = lh, rh
    return grp


def total_box(text, cx=LED_OUT_CX, cy=LED_TOTAL_Y, color=CHALK_GREEN,
              width=4.55, height=0.50, size=13):
    """The shaded TOTAL COST PRICE box every expense of the column flows into."""
    box = RoundedRectangle(corner_radius=0.08, width=width, height=height,
                           stroke_color=color, stroke_width=1.9,
                           fill_color=color, fill_opacity=0.20)
    box.move_to(np.array([cx, cy, 0.0]))
    lab = board_text(text, size, CHALK_WHITE, "BOLD")
    lab.move_to(box.get_center())
    grp = VGroup(box, lab)
    grp.box, grp.label = box, lab
    return grp


def result_box(text, cx=BOARD_CX, cy=-0.60, color=CHALK_RED,
               width=5.40, height=0.54, size=15):
    """A shaded result strip under the ledger: the overall profit or loss."""
    box = RoundedRectangle(corner_radius=0.08, width=width, height=height,
                           stroke_color=color, stroke_width=1.9,
                           fill_color=color, fill_opacity=0.20)
    box.move_to(np.array([cx, cy, 0.0]))
    lab = board_text(text, size, color, "BOLD")
    lab.move_to(box.get_center())
    grp = VGroup(box, lab)
    grp.box, grp.label = box, lab
    return grp


def math_card(tex, color=CHALK_GREEN, width=3.20, height=1.00, size=22):
    """A card whose whole content is one piece of board maths.

    Nothing else lives in the card, so no two texts can come too close.
    """
    box = panel(width, height, color)
    m = chalk_math(tex, size=size, color=CHALK_WHITE)
    m.move_to(box.get_center())
    grp = VGroup(box, m)
    grp.box, grp.math = box, m
    return grp


def formula_card(head, tex, color=CHALK_GREEN, width=3.20, height=1.52,
                 head_size=15, tex_size=24):
    """A card whose head names a formula and whose body IS that formula."""
    box = panel(width, height, color)
    h = board_text(head, head_size, color, "BOLD")
    m = chalk_math(tex, size=tex_size, color=CHALK_WHITE)
    h.move_to(box.get_center() + np.array([0.0, 0.52, 0.0]))
    m.move_to(box.get_center() + np.array([0.0, -0.30, 0.0]))
    grp = VGroup(box, h, m)
    grp.box, grp.head, grp.math = box, h, m
    return grp


def mini_ledger(head, rows, color=CHALK_GREEN, width=4.10, head_size=13,
                size=12):
    """One item's own small ledger: its head over its label/amount rows."""
    h = board_text(head, head_size, color, "BOLD")
    body = VGroup(*[two_col_row(lab, val, width - 0.70, CHALK_WHITE, size)
                    for lab, val in rows]).arrange(DOWN, buff=0.28)
    content = VGroup(h, body).arrange(DOWN, buff=0.30)
    box = panel(width, content.height + 0.34, color, opacity=0.55)
    content.move_to(box.get_center())
    grp = VGroup(box, content)
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


def wrong_card(text, color=CHALK_RED, width=2.60, height=1.05, size=15):
    """A card holding a WRONG statement, with a drawn cross over it.

    The cross occupies the card's top half and the statement its bottom half, so
    the strike-through is unmistakable yet never comes within the 0.04 units the
    clearance audit allows between a stroke and the lettering.  The whole card is
    ONE board object, so the strokes are never read as a line running into a
    box.  The caller reveals the cross by animating `.cross` to full stroke.
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
    cross.move_to(box.get_center() + np.array([0.10, height / 2 - 0.24, 0.0]))
    lab = board_text(text, size, color, "BOLD")
    lab.move_to(box.get_center() + np.array([0.0, -(height / 2 - 0.22), 0.0]))
    grp = VGroup(box, cross, lab)
    grp.box, grp.cross, grp.label = box, cross, lab
    return grp


def arrow_between(p1, p2, color=CHALK_YELLOW, width=3.0, tip=0.20):
    """A short arrow from one board point to another."""
    return Arrow(np.array([p1[0], p1[1], 0.0]), np.array([p2[0], p2[1], 0.0]),
                 buff=0.0, stroke_color=color, stroke_width=width,
                 tip_length=tip, max_tip_length_to_length_ratio=0.35)


# -- the drawn items --------------------------------------------------------
def refrigerator(cx, cy, scale=1.0, color=CHALK_CYAN):
    """A filled, shaded refrigerator: body, freezer seam, handles, feet."""
    w, h = 0.60 * scale, 0.90 * scale
    body = RoundedRectangle(corner_radius=0.07 * scale, width=w, height=h,
                            stroke_color=color, stroke_width=2.0,
                            fill_color=color, fill_opacity=0.22)
    body.move_to(np.array([cx, cy, 0.0]))
    sy = cy + h * 0.16
    seam = Line(np.array([cx - w / 2 + 0.04, sy, 0.0]),
                np.array([cx + w / 2 - 0.04, sy, 0.0]),
                stroke_color=color, stroke_width=1.6)
    handles = VGroup(
        Line(np.array([cx + w / 2 - 0.09, sy + 0.07, 0.0]),
             np.array([cx + w / 2 - 0.09, sy + 0.22 * scale, 0.0]),
             stroke_color=CHALK_AMBER, stroke_width=2.6),
        Line(np.array([cx + w / 2 - 0.09, sy - 0.24 * scale, 0.0]),
             np.array([cx + w / 2 - 0.09, sy - 0.07, 0.0]),
             stroke_color=CHALK_AMBER, stroke_width=2.6))
    feet = VGroup(*[
        Rectangle(width=0.10 * scale, height=0.06 * scale, stroke_width=0,
                  fill_color=color, fill_opacity=0.7).move_to(
            np.array([cx + dx * w / 3.0, cy - h / 2 - 0.03 * scale, 0.0]))
        for dx in (-1.0, 1.0)])
    return VGroup(body, seam, handles, feet)


def flat_icon(cx, cy, scale=1.0, color=CHALK_AMBER):
    """A filled block of flats: body, lit windows, a door and a roof slab."""
    w, h = 0.86 * scale, 0.74 * scale
    body = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.0,
                     fill_color=color, fill_opacity=0.18)
    body.move_to(np.array([cx, cy, 0.0]))
    roof = Line(np.array([cx - w / 2 - 0.06 * scale, cy + h / 2, 0.0]),
                np.array([cx + w / 2 + 0.06 * scale, cy + h / 2, 0.0]),
                stroke_color=color, stroke_width=4.0)
    windows = VGroup()
    for r in range(2):
        for c in range(3):
            win = Rectangle(width=0.16 * scale, height=0.14 * scale,
                            stroke_width=0, fill_color=CHALK_YELLOW,
                            fill_opacity=0.55)
            win.move_to(np.array([cx + (c - 1) * 0.26 * scale,
                                  cy + 0.17 * scale - r * 0.30 * scale, 0.0]))
            windows.add(win)
    door = Rectangle(width=0.16 * scale, height=0.20 * scale, stroke_width=0,
                     fill_color=color, fill_opacity=0.6)
    door.move_to(np.array([cx, cy - h / 2 + 0.10 * scale, 0.0]))
    return VGroup(body, windows, door, roof)


def table_icon(cx, cy, scale=1.0, color=CHALK_AMBER):
    """A filled table: a solid top over two legs and a rail."""
    w, h = 0.80 * scale, 0.50 * scale
    top = Rectangle(width=w, height=0.13 * scale, stroke_color=color,
                    stroke_width=1.8, fill_color=color, fill_opacity=0.55)
    top.move_to(np.array([cx, cy + h / 2 - 0.065 * scale, 0.0]))
    legs = VGroup(*[
        Rectangle(width=0.09 * scale, height=h - 0.16 * scale, stroke_width=0,
                  fill_color=color, fill_opacity=0.40).move_to(
            np.array([cx + sx * (w / 2 - 0.08 * scale),
                      cy - 0.08 * scale, 0.0]))
        for sx in (-1.0, 1.0)])
    rail = Rectangle(width=w * 0.66, height=0.07 * scale, stroke_width=0,
                     fill_color=color, fill_opacity=0.35)
    rail.move_to(np.array([cx, cy - h / 2 + 0.14 * scale, 0.0]))
    return VGroup(top, legs, rail)


def bicycle_icon(cx, cy, scale=1.0, color=CHALK_CYAN):
    """A filled bicycle: two solid-tyred wheels, a frame, a seat and bars."""
    r = 0.20 * scale

    def wheel(dx):
        c = np.array([cx + dx, cy - 0.10 * scale, 0.0])
        return VGroup(
            Circle(radius=r, stroke_color=color, stroke_width=3.0,
                   fill_color=color, fill_opacity=0.12).move_to(c),
            Circle(radius=r * 0.24, stroke_width=0, fill_color=color,
                   fill_opacity=0.9).move_to(c))

    p0 = np.array([cx - 0.30 * scale, cy - 0.10 * scale, 0.0])
    p1 = np.array([cx - 0.02 * scale, cy + 0.22 * scale, 0.0])
    p2 = np.array([cx + 0.10 * scale, cy - 0.10 * scale, 0.0])
    p3 = np.array([cx + 0.30 * scale, cy - 0.10 * scale, 0.0])
    frame = VGroup(
        Line(p0, p1, stroke_color=color, stroke_width=3.0),
        Line(p1, p2, stroke_color=color, stroke_width=3.0),
        Line(p2, p3, stroke_color=color, stroke_width=3.0),
        Line(p0, p2, stroke_color=color, stroke_width=3.0))
    seat = Rectangle(width=0.17 * scale, height=0.06 * scale, stroke_width=0,
                     fill_color=CHALK_AMBER, fill_opacity=0.9)
    seat.move_to(np.array([cx - 0.06 * scale, cy + 0.26 * scale, 0.0]))
    bars = Line(np.array([cx + 0.10 * scale, cy + 0.20 * scale, 0.0]),
                np.array([cx + 0.24 * scale, cy + 0.30 * scale, 0.0]),
                stroke_color=CHALK_AMBER, stroke_width=3.0)
    return VGroup(wheel(-0.30 * scale), wheel(0.30 * scale), frame, seat, bars)


def tv_icon(cx, cy, scale=1.0, color=CHALK_PINK):
    """A filled television: a lit screen in a case, on a stand, with aerials."""
    w, h = 0.72 * scale, 0.50 * scale
    body = RoundedRectangle(corner_radius=0.05 * scale, width=w, height=h,
                            stroke_color=color, stroke_width=2.0,
                            fill_color=color, fill_opacity=0.22)
    body.move_to(np.array([cx, cy, 0.0]))
    screen = Rectangle(width=w - 0.14 * scale, height=h - 0.14 * scale,
                       stroke_width=0, fill_color=CHALK_CYAN,
                       fill_opacity=0.30)
    screen.move_to(np.array([cx, cy, 0.0]))
    stand = Polygon(np.array([cx - 0.14 * scale, cy - h / 2, 0.0]),
                    np.array([cx + 0.14 * scale, cy - h / 2, 0.0]),
                    np.array([cx + 0.06 * scale, cy - h / 2 - 0.09 * scale, 0.0]),
                    np.array([cx - 0.06 * scale, cy - h / 2 - 0.09 * scale, 0.0]),
                    stroke_width=0, fill_color=color, fill_opacity=0.55)
    aerials = VGroup(
        Line(np.array([cx - 0.02 * scale, cy + h / 2, 0.0]),
             np.array([cx - 0.17 * scale, cy + h / 2 + 0.17 * scale, 0.0]),
             stroke_color=color, stroke_width=2.0),
        Line(np.array([cx + 0.02 * scale, cy + h / 2, 0.0]),
             np.array([cx + 0.17 * scale, cy + h / 2 + 0.17 * scale, 0.0]),
             stroke_color=color, stroke_width=2.0))
    return VGroup(body, screen, stand, aerials)


def banana_bunch(cx, cy, scale=1.0, color=CHALK_YELLOW):
    """A bunch of bananas: three thick filled crescents over a stalk.

    The crescents are drawn as fat chalk arcs (a filled band, not a hairline),
    each with a chalk highlight down its back, so the bunch reads as solid
    fruit and not as three bare outlines.
    """
    fruit = VGroup()
    for dx in (-0.17, 0.0, 0.17):
        c = np.array([cx + dx * scale, cy + 0.06 * scale, 0.0])
        fruit.add(Arc(radius=0.30 * scale, start_angle=200 * DEGREES,
                      angle=140 * DEGREES, arc_center=c,
                      stroke_color=color, stroke_width=12.0 * scale))
        fruit.add(Arc(radius=0.30 * scale, start_angle=205 * DEGREES,
                      angle=130 * DEGREES, arc_center=c,
                      stroke_color=CHALK_WHITE, stroke_width=3.0 * scale,
                      stroke_opacity=0.35))
    stalk = Rectangle(width=0.10 * scale, height=0.16 * scale, stroke_width=0,
                      fill_color="#8A6B2A", fill_opacity=0.9)
    stalk.move_to(np.array([cx, cy - 0.14 * scale, 0.0]))
    return VGroup(stalk, fruit)


def truck_icon(cx, cy, scale=1.0, color=CHALK_CYAN):
    """A filled delivery truck: cargo box, cab and two wheels."""
    box = Rectangle(width=0.50 * scale, height=0.30 * scale,
                    stroke_color=color, stroke_width=1.8,
                    fill_color=color, fill_opacity=0.30)
    box.move_to(np.array([cx - 0.09 * scale, cy + 0.06 * scale, 0.0]))
    cab = Polygon(np.array([cx + 0.17 * scale, cy - 0.09 * scale, 0.0]),
                  np.array([cx + 0.38 * scale, cy - 0.09 * scale, 0.0]),
                  np.array([cx + 0.38 * scale, cy + 0.04 * scale, 0.0]),
                  np.array([cx + 0.25 * scale, cy + 0.15 * scale, 0.0]),
                  np.array([cx + 0.17 * scale, cy + 0.15 * scale, 0.0]),
                  stroke_color=color, stroke_width=1.8,
                  fill_color=color, fill_opacity=0.30)
    wheels = VGroup(*[
        Circle(radius=0.075 * scale, stroke_width=0, fill_color=CHALK_WHITE,
               fill_opacity=0.75).move_to(
            np.array([cx + dx * scale, cy - 0.16 * scale, 0.0]))
        for dx in (-0.20, 0.28)])
    return VGroup(box, cab, wheels)


def wrench_icon(cx, cy, scale=1.0, color=CHALK_AMBER):
    """A filled spanner: a thick handle under an open two-jaw head."""
    handle = Line(np.array([cx - 0.05 * scale, cy - 0.20 * scale, 0.0]),
                  np.array([cx + 0.04 * scale, cy + 0.10 * scale, 0.0]),
                  stroke_color=color, stroke_width=7.0 * scale)
    jaws = VGroup(
        Polygon(np.array([cx + 0.01 * scale, cy + 0.09 * scale, 0.0]),
                np.array([cx + 0.17 * scale, cy + 0.15 * scale, 0.0]),
                np.array([cx + 0.15 * scale, cy + 0.30 * scale, 0.0]),
                np.array([cx + 0.03 * scale, cy + 0.24 * scale, 0.0]),
                stroke_width=0, fill_color=color, fill_opacity=0.85),
        Polygon(np.array([cx - 0.04 * scale, cy + 0.09 * scale, 0.0]),
                np.array([cx + 0.09 * scale, cy + 0.02 * scale, 0.0]),
                np.array([cx + 0.19 * scale, cy + 0.04 * scale, 0.0]),
                np.array([cx + 0.06 * scale, cy + 0.14 * scale, 0.0]),
                stroke_width=0, fill_color=color, fill_opacity=0.85))
    return VGroup(handle, jaws)


def balance_rig(cx, cy, scale=1.0, arm_color=CHALK_AMBER):
    """The two-pan balance that compares money out with money in.

    Returns `(stand, tracker, moving)`.  `stand` is the fixed post and base;
    `moving` is an `always_redraw` beam, ropes and pair of pans driven by
    `tracker`, so `tracker.animate.set_value(v)` is the whole comparison:

        v > 0  the money-in pan rises  -> a profit,
        v < 0  the money-out pan rises -> a loss.

    The pans are shallow filled dishes (never bare outlines), and `moving` is
    added straight to the scene -- the same pattern the series' own compasses
    use -- so the audit sees the real pose of every stroke.
    """
    pivot = np.array([cx, cy + 0.66 * scale, 0.0])
    arm = 1.24 * scale
    stand = VGroup(
        Polygon(np.array([cx - 0.30 * scale, cy - 0.66 * scale, 0.0]),
                np.array([cx + 0.30 * scale, cy - 0.66 * scale, 0.0]),
                np.array([cx + 0.13 * scale, pivot[1], 0.0]),
                np.array([cx - 0.13 * scale, pivot[1], 0.0]),
                stroke_color=arm_color, stroke_width=1.8,
                fill_color=arm_color, fill_opacity=0.22),
        RoundedRectangle(corner_radius=0.04, width=1.30 * scale,
                         height=0.14 * scale, stroke_color=arm_color,
                         stroke_width=1.8, fill_color=arm_color,
                         fill_opacity=0.30).move_to(
            np.array([cx, cy - 0.66 * scale - 0.07 * scale, 0.0])))
    tracker = ValueTracker(0.0)

    def build():
        ang = float(tracker.get_value()) * 12 * DEGREES
        d = np.array([np.cos(ang), np.sin(ang), 0.0])
        left, right = pivot - d * arm, pivot + d * arm
        grp = VGroup(Line(left, right, stroke_color=arm_color,
                          stroke_width=7.0))
        for end in (left, right):
            pan_y = end[1] - 0.46 * scale
            grp.add(Line(end, np.array([end[0] - 0.26 * scale, pan_y, 0.0]),
                         stroke_color=arm_color, stroke_width=1.6),
                    Line(end, np.array([end[0] + 0.26 * scale, pan_y, 0.0]),
                         stroke_color=arm_color, stroke_width=1.6),
                    Polygon(np.array([end[0] - 0.34 * scale, pan_y, 0.0]),
                            np.array([end[0] + 0.34 * scale, pan_y, 0.0]),
                            np.array([end[0] + 0.24 * scale,
                                      pan_y - 0.13 * scale, 0.0]),
                            np.array([end[0] - 0.24 * scale,
                                      pan_y - 0.13 * scale, 0.0]),
                            stroke_color=CHALK_YELLOW, stroke_width=1.6,
                            fill_color=CHALK_YELLOW, fill_opacity=0.24))
        return grp

    return stand, tracker, always_redraw(build)


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "The purchase price is not always the real cost. <bookmark mark='b0'/> "
        "A second-hand refrigerator is bought for five thousand rupees. "
        "<bookmark mark='b1'/> Then one hundred rupees go on transport, "
        "<bookmark mark='b2'/> and five hundred rupees on repairs. <bookmark "
        "mark='b3'/> So the money actually spent is five thousand plus one "
        "hundred plus five hundred, that is five thousand six hundred rupees. "
        "<bookmark mark='b4'/> Sold for seven thousand rupees, the real profit "
        "is seven thousand minus five thousand six hundred, which is one "
        "thousand four hundred rupees. <bookmark mark='b5'/> Not two thousand."
    ),
    "s1": (
        "First, decide whether a deal is a profit, a loss, or neither. "
        "<bookmark mark='b0'/> Cost price five hundred rupees, selling price "
        "six hundred and fifty: the selling price is bigger, so this is a "
        "profit of six hundred fifty minus five hundred, that is one hundred "
        "and fifty rupees. <bookmark mark='b1'/> Now change the selling price "
        "to four hundred and fifty: this time the cost price is bigger, so it "
        "is a loss of five hundred minus four hundred fifty, that is fifty "
        "rupees. <bookmark mark='b2'/> And when the selling "
        "price equals the cost price, there is neither a profit nor a loss. "
        "<bookmark mark='b3'/> So there are two formulas: profit is selling "
        "price minus cost price, and loss is cost price minus selling price. "
        "<bookmark mark='b4'/> Always ask which one is bigger before you "
        "subtract."
    ),
    "s2": (
        "Now the percentage. <bookmark mark='b0'/> A profit of one hundred "
        "fifty rupees on a cost price of five hundred rupees is a profit of "
        "thirty percent. <bookmark mark='b1'/> The difference is always "
        "measured against the cost price: profit percent is profit divided by "
        "cost price, times one hundred. <bookmark mark='b2'/> And loss percent "
        "is loss divided by cost price, times one hundred. <bookmark "
        "mark='b3'/> The cost price is the base. <bookmark mark='b4'/> A very "
        "common error is to divide by the selling price instead. That is "
        "wrong, and we cross it out."
    ),
    "s3": (
        "Let us keep a proper ledger for the refrigerator. <bookmark "
        "mark='b0'/> Purchase price five thousand rupees. <bookmark "
        "mark='b1'/> Add transport, one hundred rupees, <bookmark mark='b2'/> "
        "and repairs, five hundred rupees. <bookmark mark='b3'/> So the total "
        "cost price is five thousand six hundred rupees. <bookmark mark='b4'/> "
        "The selling price is seven thousand rupees, so the profit is one "
        "thousand four hundred rupees. <bookmark mark='b5'/> And the profit "
        "percent is one thousand four hundred divided by five thousand six "
        "hundred, times one hundred. That is twenty five percent."
    ),
    "s4": (
        "Here is the same idea with a loss. <bookmark mark='b0'/> A flat is "
        "bought for four lakh fifty thousand rupees. <bookmark mark='b1'/> Ten "
        "thousand rupees are spent on repairs and painting, <bookmark "
        "mark='b2'/> so the total cost price is four lakh sixty thousand "
        "rupees. <bookmark mark='b3'/> It is sold for four lakh twenty five "
        "thousand five hundred rupees, so the selling price is smaller. "
        "<bookmark mark='b4'/> The loss is four lakh sixty thousand minus four "
        "lakh twenty five thousand five hundred, that is thirty four thousand "
        "five hundred rupees. <bookmark mark='b5'/> And the loss percent is "
        "thirty four thousand five hundred divided by four lakh sixty "
        "thousand, times one hundred, which is seven point five percent."
    ),
    "s5": (
        "Now a trap. <bookmark mark='b0'/> Two tables are each sold for three "
        "thousand rupees. <bookmark mark='b1'/> One gives a gain of twenty "
        "percent, <bookmark mark='b2'/> and the other gives a loss of twenty "
        "percent. <bookmark mark='b3'/> Do the plus twenty and the minus "
        "twenty cancel? It is tempting to say zero percent. <bookmark "
        "mark='b4'/> But the percentages act on different cost prices. On the "
        "first table, three thousand rupees is one hundred and twenty percent "
        "of the cost price, so the cost price is three thousand divided by one "
        "point two, that is two thousand five hundred rupees. <bookmark "
        "mark='b5'/> On the second table, three thousand rupees is eighty "
        "percent of the cost price, so the cost price is three thousand "
        "divided by zero point eight, that is three thousand seven hundred and "
        "fifty rupees. The two bases are different."
    ),
    "s6": (
        "Now solve the whole transaction. <bookmark mark='b0'/> The total cost "
        "price is two thousand five hundred plus three thousand seven hundred "
        "fifty, that is six thousand two hundred and fifty rupees. <bookmark "
        "mark='b1'/> The total selling price is three thousand plus three "
        "thousand, that is six thousand rupees. <bookmark mark='b2'/> The "
        "selling price is smaller, so overall there is a loss of two hundred "
        "and fifty rupees. <bookmark mark='b3'/> And the loss percent is two "
        "hundred and fifty divided by six thousand two hundred fifty, times "
        "one hundred, which is four percent. <bookmark mark='b4'/> So plus "
        "twenty percent and minus twenty percent did not give zero percent "
        "here."
    ),
    "s7": (
        "Here is the decision process, in five steps. <bookmark mark='b0'/> "
        "Step one: find the purchase price. <bookmark mark='b1'/> Step two: "
        "add every overhead expense to get the total cost price. <bookmark "
        "mark='b2'/> Step three: find the total selling price. <bookmark "
        "mark='b3'/> Step four: compare the two. If the selling price is "
        "bigger there is a profit, and if it is smaller there is a loss. "
        "<bookmark mark='b4'/> Step five: divide by the cost price and "
        "multiply by one hundred for the percentage. <bookmark mark='b5'/> And "
        "when there are several items, compare the sum of the cost prices with "
        "the sum of the selling prices."
    ),
    "s8": (
        "One more reminder. <bookmark mark='b0'/> Overheads still count when "
        "part of the stock cannot be sold. <bookmark mark='b1'/> Bananas are "
        "bought for one thousand two hundred and fifty rupees, and two hundred "
        "and fifty rupees go on transport, so the total cost price is one "
        "thousand five hundred rupees. <bookmark mark='b2'/> Only some dozens "
        "are good enough to sell, and they bring in one thousand five hundred "
        "and seventy five rupees. <bookmark mark='b3'/> The spoiled bananas do "
        "not vanish from the cost: the money spent on them is still part of "
        "the cost price. <bookmark mark='b4'/> And the profit is one thousand "
        "five hundred seventy five minus one thousand five hundred, that is "
        "seventy five rupees, which is five percent."
    ),
    "s9q": (
        "Your turn. <bookmark mark='b0'/> First: a bicycle is bought for four "
        "thousand rupees, <bookmark mark='b1'/> with two hundred rupees for "
        "transport and three hundred rupees for repair. It is sold for five "
        "thousand four hundred rupees. Find the total cost price, the profit, "
        "and the profit percent. <bookmark mark='b2'/> Second: two television "
        "sets are each sold for nine thousand nine hundred rupees. <bookmark "
        "mark='b3'/> One gives a profit of ten percent, and the other gives a "
        "loss of ten percent. Did the plus ten and the minus ten cancel?"
    ),
    "s9a": (
        "Let us check. <bookmark mark='b0'/> For the bicycle, the overheads are "
        "two hundred plus three hundred, so the total cost price is four "
        "thousand five hundred rupees. <bookmark mark='b1'/> The profit is five "
        "thousand four hundred minus four thousand five hundred, that is nine "
        "hundred rupees, and the profit percent is nine hundred divided by four "
        "thousand five hundred, times one hundred, which is twenty percent. "
        "<bookmark mark='b2'/> For the television sets, the first cost price is "
        "nine thousand nine hundred divided by one point one, that is nine "
        "thousand rupees. <bookmark mark='b3'/> The second cost price is nine "
        "thousand nine hundred divided by zero point nine, that is eleven "
        "thousand rupees. The total cost price is twenty thousand rupees and "
        "the total selling price is nineteen thousand eight hundred, so there "
        "is a loss of two hundred rupees, which is one percent. The plus ten "
        "and the minus ten did not cancel."
    ),
    "s10": (
        "Let us put it together. <bookmark mark='b0'/> First add the overheads "
        "to the purchase price. <bookmark mark='b1'/> Then compare the total "
        "cost price with the selling price. <bookmark mark='b2'/> Take the "
        "percentage on the cost price, never on the selling price. <bookmark "
        "mark='b3'/> And for several items, compare the total cost with the "
        "total selling price. <bookmark mark='b4'/> The purchase price alone "
        "is never the real cost. <bookmark mark='b5'/> Thank you for watching, "
        "<bookmark mark='b6'/> and see you in the next lesson."
    ),
}

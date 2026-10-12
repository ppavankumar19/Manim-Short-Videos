"""Board furniture and narration for Storyboard 03 -- Sales Tax, VAT & GST
Calculations: Determining Original Prices and Total Bills, Class 8 Mathematics,
Chapter 5 (Comparing Quantities using Proportion).

This file is *spliced*, never imported: assemble_salestax.py grafts it into the
proven head of the Chapter 3 quadrilaterals set, so the theme names
(CHALK_*, FONT, BOARD_*), `board_text`, `chalk_math`, `appear` and the pacing
helpers (`rt`, `quick`, `leftover`) are already defined above it.

The furniture is this video's "tax on a bill" kit:

  * `bill_bar`     -- the persistent bill bar: one filled bar IS 100% of the
                      base price, and every later change is measured from it,
  * `tax_layer`    -- the translucent tax layer that descends from above the
                      bar, attaches flush against its right end and then merges
                      into the (100 + r)% total,
  * `rate_bar`     -- the (100 + r)% bar with its tax portion marked: the
                      reverse direction, before the bar shrinks back to 100%,
  * `tax_split`    -- one tax block that physically halves into two labelled
                      blocks (the textbook's CGST / SGST case),
  * `receipt`      -- a drawn bill slip that GROWS as the tax layer joins,
  * `med_receipt`  -- the medical-shop receipt (a filled slip with a drawn
                      medical cross),
  * `price_tag`    -- the shop tag with a punched hole and a string,
  * `shoe_pair`    -- the pair of shoes, drawn as filled shaded shapes,
  * `goods_icon` / `service_icon` -- the goods-and-services pair,
  * `money_note`, `coin_stack` -- drawn money (filled, shaded),
  * `lane_card`    -- one lane of the forward/backward decision board,
  * `wrong_card` / `cross_out` / `tick` -- the drawn cross and tick (Segoe
                      Print has neither glyph).

Everything is drawn as filled, shaded geometry -- bars with painted bodies,
shoes with soles and uppers, notes with a printed inner frame, coins with
thickness -- never as a bare outline.
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

# The three content lines.  ROW_A carries the diagram (the bill bar and the
# drawn items), ROW_B the numbers worked under it and ROW_C the rule chip above
# the banner.  The rows are set so that no two texts come within the 0.22 units
# the clearance audit asks for, including the banner text sitting at -1.15.
ROW_A = 0.90
ROW_B = 0.04
ROW_C = -0.62

PANEL_FILL = "#16202B"
CHIP_H = 0.50
CARD_W = 3.30
CARD_H = 0.94
MARK_SIZE = 18
DOT_R = 0.075
COIN_R = 0.17

# The example figures this video works with.  They are held as data so the board
# and the narration can never drift apart, and every rate here is a textbook or
# historical example -- never current tax advice.
SHOE_PRICE = 450
SHOE_RATE = 6
SHOE_TAX = 27
SHOE_BILL = 477
VAT_BASE = "Rs 354.45"
VAT_TAX = "Rs 17.72"
VAT_BILL = "Rs 372.18"
GST_BASE = 1000
GST_RATE = 5
GST_TAX = 50
GST_BILL = 1050
REV_BILL = 2360
REV_RATE = 18
REV_BASE = 2000
REV_TAX = 360


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


def bill_bar(width=2.40, height=0.54, color=CHALK_GREEN,
             label="BASE PRICE = 100%", size=13):
    """The persistent bill bar: one filled bar IS the whole 100% base price.

    The same bar -- same colour, same height, same label position -- is the
    anchor of every teaching scene, so "the base price" always looks the same
    and the tax layer is always seen attaching to that one object.
    """
    box = RoundedRectangle(corner_radius=0.05, width=width, height=height,
                           stroke_color=color, stroke_width=2.2,
                           fill_color=color, fill_opacity=0.22)
    grp = VGroup(box)
    grp.box = box
    if label:
        lab = board_text(label, size, CHALK_WHITE, "BOLD")
        lab.move_to(box.get_center())
        grp.add(lab)
        grp.label = lab
    return grp


def tax_layer(width=0.62, height=0.54, color=CHALK_AMBER, label="TAX",
              size=12):
    """The translucent tax layer that attaches above the 100% bar.

    It is deliberately see-through: the viewer must read it as a layer ADDED on
    top of the base price, never as a second base price.
    """
    box = RoundedRectangle(corner_radius=0.05, width=width, height=height,
                           stroke_color=color, stroke_width=2.2,
                           fill_color=color, fill_opacity=0.20)
    grp = VGroup(box)
    grp.box = box
    if label:
        lab = board_text(label, size, color, "BOLD")
        lab.move_to(box.get_center())
        grp.add(lab)
        grp.label = lab
    return grp


def rate_bar(base_w=2.60, rate=18, height=0.58, base_color=CHALK_GREEN,
             tax_color=CHALK_AMBER, base_label="100% = BASE PRICE",
             tax_label=None, size=13, tax_size=11):
    """The (100 + r)% bar: the base portion and the marked tax portion.

    The two portions sit flush against each other in ONE group, so the bar can
    be shrunk back to its 100% portion by taking the tax portion away.  The tax
    portion is proportional (r% of the base width), which is what makes it
    visibly the smaller part.
    """
    tax_w = max(base_w * rate / 100.0, 0.34)
    base = RoundedRectangle(corner_radius=0.04, width=base_w, height=height,
                            stroke_color=base_color, stroke_width=2.2,
                            fill_color=base_color, fill_opacity=0.22)
    tax = RoundedRectangle(corner_radius=0.04, width=tax_w, height=height,
                           stroke_color=tax_color, stroke_width=2.2,
                           fill_color=tax_color, fill_opacity=0.34)
    bar = VGroup(base, tax).arrange(RIGHT, buff=0.0)
    grp = VGroup(bar)
    grp.base, grp.tax = base, tax
    lab = board_text(base_label, size, CHALK_WHITE, "BOLD")
    lab.move_to(base.get_center())
    grp.add(lab)
    grp.label = lab
    if tax_label:
        # the tax label sits ABOVE its own thin portion: the portion is only a
        # sliver, so a label inside it could not be read
        tl = board_text(tax_label, tax_size, tax_color, "BOLD")
        tl.move_to(np.array([tax.get_center()[0],
                             tax.get_top()[1] + 0.19, 0.0]))
        grp.add(tl)
        grp.tax_label = tl
    return grp


def tax_split(width=3.60, height=0.66, color=CHALK_AMBER, left="CGST Rs 180",
              right="SGST Rs 180", size=12):
    """One tax block that physically halves into two labelled blocks.

    Both halves, their wording and the gap between them live in ONE group, so
    the block can be split apart without the labels being left behind.  Pass
    `left=None` / `right=None` to get the two bare halves and label them one
    bookmark at a time.
    """
    half = (width - 0.10) / 2.0
    boxes = VGroup(
        RoundedRectangle(corner_radius=0.05, width=half, height=height,
                         stroke_color=color, stroke_width=2.0,
                         fill_color=color, fill_opacity=0.32),
        RoundedRectangle(corner_radius=0.05, width=half, height=height,
                         stroke_color=color, stroke_width=2.0,
                         fill_color=color, fill_opacity=0.32),
    ).arrange(RIGHT, buff=0.10)
    halves = []
    for box, lab in zip(boxes, (left, right)):
        if lab is None:
            halves.append(VGroup(box))
        else:
            halves.append(VGroup(box, board_text(lab, size, CHALK_WHITE,
                                                 "BOLD"
                                                 ).move_to(box.get_center())))
    grp = VGroup(*halves)
    grp.half_l, grp.half_r = halves[0], halves[1]
    grp.boxes = boxes
    return grp


def whole_tax_block(width=3.60, height=0.66, color=CHALK_AMBER,
                    label="GST = Rs 360", size=13):
    """The undivided tax block the split is made from."""
    box = RoundedRectangle(corner_radius=0.05, width=width, height=height,
                           stroke_color=color, stroke_width=2.0,
                           fill_color=color, fill_opacity=0.32)
    lab = board_text(label, size, CHALK_WHITE, "BOLD")
    lab.move_to(box.get_center())
    grp = VGroup(box, lab)
    grp.box, grp.label = box, lab
    return grp


def receipt(width=1.80, height=1.10, color=CHALK_CYAN, head="BILL",
            value="Rs 477", size=12):
    """The bill itself: a filled slip with a heading and the amount on it.

    The ruled lines are thin filled bars rather than strokes, so no line ever
    runs through the lettering.
    """
    body = RoundedRectangle(corner_radius=0.06, width=width, height=height,
                            stroke_color=color, stroke_width=2.2,
                            fill_color=color, fill_opacity=0.18)
    h = board_text(head, size, color, "BOLD")
    h.move_to(body.get_center() + UP * 0.34)
    v = board_text(value, size, CHALK_WHITE, "BOLD")
    v.move_to(body.get_center() + DOWN * 0.32)
    bars = VGroup()
    for yy in (0.12, 0.04):
        b = Rectangle(width=width - 0.48, height=0.035, stroke_width=0,
                      fill_color=CHALK_WHITE, fill_opacity=0.35)
        b.move_to(body.get_center() + UP * yy)
        bars.add(b)
    grp = VGroup(body, bars, h, v)
    grp.box, grp.head, grp.value = body, h, v
    return grp


def med_receipt(width=1.95, height=1.30, color=CHALK_CYAN, head="MEDICAL",
                value="Rs 372.18", size=12):
    """The medical-shop receipt: a filled slip with a drawn medical cross.

    The cross is two filled bars (no outline glyph, no bare stroke), so it
    reads as printed ink on the slip.
    """
    body = RoundedRectangle(corner_radius=0.06, width=width, height=height,
                            stroke_color=color, stroke_width=2.2,
                            fill_color=color, fill_opacity=0.18)
    cross = VGroup(
        Rectangle(width=0.10, height=0.34, stroke_width=0,
                  fill_color=CHALK_WHITE, fill_opacity=0.55),
        Rectangle(width=0.34, height=0.10, stroke_width=0,
                  fill_color=CHALK_WHITE, fill_opacity=0.55),
    )
    cross.move_to(body.get_center())
    h = board_text(head, size, color, "BOLD")
    h.move_to(body.get_center() + UP * 0.46)
    v = board_text(value, size, CHALK_WHITE, "BOLD")
    v.move_to(body.get_center() + DOWN * 0.46)
    bars = VGroup()
    for yy in (-0.20, -0.28):
        b = Rectangle(width=width - 0.48, height=0.035, stroke_width=0,
                      fill_color=CHALK_WHITE, fill_opacity=0.35)
        b.move_to(body.get_center() + UP * yy)
        bars.add(b)
    grp = VGroup(body, cross, bars, h, v)
    grp.box, grp.head, grp.value = body, h, v
    return grp


def price_tag(width=2.00, height=0.82, color=CHALK_PINK, text="Rs 450",
              size=14):
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


def shoe_pair(cx, cy, scale=1.0, color=CHALK_PINK):
    """A pair of shoes: two filled, shaded shoes (sole, upper and a lace)."""
    shoes = VGroup()
    for dx in (-0.34 * scale, 0.34 * scale):
        sole = Polygon(
            np.array([cx + dx - 0.32 * scale, cy - 0.13 * scale, 0.0]),
            np.array([cx + dx + 0.27 * scale, cy - 0.13 * scale, 0.0]),
            np.array([cx + dx + 0.33 * scale, cy - 0.03 * scale, 0.0]),
            np.array([cx + dx - 0.36 * scale, cy - 0.03 * scale, 0.0]),
            stroke_color=color, stroke_width=1.9,
            fill_color=color, fill_opacity=0.34)
        upper = Polygon(
            np.array([cx + dx - 0.28 * scale, cy - 0.02 * scale, 0.0]),
            np.array([cx + dx + 0.05 * scale, cy - 0.02 * scale, 0.0]),
            np.array([cx + dx + 0.00 * scale, cy + 0.25 * scale, 0.0]),
            np.array([cx + dx - 0.22 * scale, cy + 0.23 * scale, 0.0]),
            stroke_color=color, stroke_width=1.9,
            fill_color=color, fill_opacity=0.26)
        lace = Line(np.array([cx + dx - 0.19 * scale, cy + 0.09 * scale, 0.0]),
                    np.array([cx + dx - 0.01 * scale, cy + 0.12 * scale, 0.0]),
                    stroke_color=CHALK_WHITE, stroke_width=1.6)
        shoes.add(sole, upper, lace)
    return shoes


def goods_icon(cx, cy, scale=1.0, color=CHALK_GREEN):
    """Goods: a filled parcel with a printed band and tape."""
    body = Rectangle(width=0.64 * scale, height=0.56 * scale,
                     stroke_color=color, stroke_width=2.0,
                     fill_color=color, fill_opacity=0.26)
    body.move_to(np.array([cx, cy, 0.0]))
    band = Rectangle(width=0.10 * scale, height=0.56 * scale, stroke_width=0,
                     fill_color=CHALK_WHITE, fill_opacity=0.45)
    band.move_to(body.get_center())
    tape = Rectangle(width=0.64 * scale, height=0.10 * scale, stroke_width=0,
                     fill_color=CHALK_WHITE, fill_opacity=0.45)
    tape.move_to(body.get_center())
    return VGroup(body, band, tape)


def service_icon(cx, cy, scale=1.0, color=CHALK_CYAN):
    """Services: a filled badge holding a drawn spanner."""
    disc = Circle(radius=0.32 * scale, stroke_color=color, stroke_width=2.0,
                  fill_color=color, fill_opacity=0.26)
    disc.move_to(np.array([cx, cy, 0.0]))
    handle = Rectangle(width=0.42 * scale, height=0.09 * scale,
                       stroke_color=CHALK_WHITE, stroke_width=0.0,
                       fill_color=CHALK_WHITE, fill_opacity=0.55)
    handle.move_to(np.array([cx, cy - 0.10 * scale, 0.0]))
    handle.rotate(-35 * DEGREES)
    jaw = Circle(radius=0.11 * scale, stroke_color=CHALK_WHITE,
                 stroke_width=2.0, fill_color=PANEL_FILL, fill_opacity=0.85)
    jaw.move_to(handle.get_end())
    return VGroup(disc, handle, jaw)


def money_note(width=1.54, height=0.74, color=CHALK_GREEN, text="Rs 27",
               size=13):
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


def name_card(head, sub, color=CHALK_CYAN, width=2.40, head_size=12,
              sub_size=10, gap=0.24, pad=0.16):
    """A small two-line card: the name of a quantity and its one-line gloss.

    Used for the three quantities of the title card.  The two lines are held
    0.24 apart and the box is sized to them, so the gloss can never be squeezed
    against the name.
    """
    h = board_text(head, head_size, color, "BOLD")
    s = board_text(sub, sub_size, CHALK_WHITE, "BOLD")
    inner = VGroup(h, s).arrange(DOWN, buff=gap)
    box = panel(width, inner.height + 2 * pad, color, radius=0.09)
    inner.move_to(box.get_center())
    grp = VGroup(box, h, s)
    grp.box, grp.head, grp.sub = box, h, s
    return grp


def lane_card(head, lines, color=CHALK_CYAN, width=4.20, head_size=15,
              line_size=12, gap=0.30, buff=0.26, pad=0.26):
    """One lane of the forward/backward decision board.

    The head and the body are separated by `gap` (0.30) and the body's own lines
    by `buff` (0.26), so the card passes the clearance audit (which flags any
    two texts closer than 0.22).  The box is sized to the text it carries, so
    the wording can never stick out of its own panel.
    """
    h = board_text(head, head_size, color, "BOLD")
    body = VGroup(*[board_text(line, line_size, CHALK_WHITE, "BOLD")
                    for line in lines]).arrange(DOWN, buff=buff)
    inner = VGroup(h, body).arrange(DOWN, buff=gap)
    box = panel(width, inner.height + 2 * pad, color)
    inner.move_to(box.get_center())
    grp = VGroup(box, h, body)
    grp.box, grp.head, grp.body = box, h, body
    return grp


def note_card(head, lines, color=CHALK_CYAN, width=3.40, height=1.05,
              head_size=15, line_size=13):
    """A card with a bold head line and ONE body line under it.

    A second body line would leave less than the 0.22 units the clearance audit
    asks for between the head and the body, so this card carries one line; the
    two-line board is `lane_card`.
    """
    box = panel(width, height, color)
    h = board_text(head, head_size, color, "BOLD")
    body = VGroup(*[board_text(line, line_size, CHALK_WHITE, "BOLD")
                    for line in lines]).arrange(DOWN, buff=0.24)
    h.move_to(box.get_center() + UP * 0.27)
    body.move_to(box.get_center() + DOWN * 0.27)
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


def wrong_card(text, color=CHALK_RED, width=2.60, height=1.00, size=13):
    """A card holding a WRONG statement, with a drawn cross over it.

    The cross occupies the card's top half and the statement its bottom half, so
    the strike-through is unmistakable yet never comes within the 0.04 units the
    audit allows between a stroke and the lettering.  The whole card is ONE
    board object, so the strokes are never read as a line running into a box.
    """
    box = panel(width, height, color, opacity=0.7)
    cross = VGroup(
        Line(np.array([-width / 2 + 0.50, 0.12, 0.0]),
             np.array([-width / 2 + 0.98, 0.42, 0.0]),
             stroke_color=color, stroke_width=4.2),
        Line(np.array([-width / 2 + 0.50, 0.42, 0.0]),
             np.array([-width / 2 + 0.98, 0.12, 0.0]),
             stroke_color=color, stroke_width=4.2),
    )
    cross.move_to(box.get_center() + UP * (height / 2.0 - 0.24))
    cross.shift(RIGHT * 0.10)
    lab = board_text(text, size, color, "BOLD")
    lab.move_to(box.get_center() + DOWN * (height / 2.0 - 0.24))
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
        "Meet the price tag, then meet the bill. <bookmark mark='b0'/>A pair of "
        "shoes is marked at four hundred and fifty rupees. <bookmark "
        "mark='b1'/>At the counter, a sales tax of six percent is added. "
        "<bookmark mark='b2'/>Three quantities are involved: the base price, "
        "the price before any tax; <bookmark mark='b3'/>the tax amount, the "
        "percentage that is added; <bookmark mark='b4'/>and the final bill, the "
        "base price plus the tax. So the tag and the bill show two different "
        "numbers."
    ),
    "s1": (
        "A tax is just a percentage increase. <bookmark mark='b0'/>The original "
        "price is taken as one hundred percent. <bookmark mark='b1'/>Adding a "
        "tax of r percent gives one hundred plus r percent. <bookmark "
        "mark='b2'/>With six percent, the total becomes one hundred and six "
        "percent. <bookmark mark='b3'/>So the final bill is one hundred plus r, "
        "divided by one hundred, times the base price. <bookmark mark='b4'/>This "
        "is exactly the percentage increase we met in the earlier lesson."
    ),
    "s2": (
        "Now the same shoes, with the numbers filled in. <bookmark "
        "mark='b0'/>The base price is four hundred and fifty rupees. <bookmark "
        "mark='b1'/>Sales tax is six percent, so the tax is six over one hundred "
        "times four hundred and fifty, which is twenty seven rupees. <bookmark "
        "mark='b2'/>Add it to the base price: four hundred and fifty plus twenty "
        "seven is four hundred and seventy seven rupees. <bookmark mark='b3'/>"
        "Here is the shortcut: one hundred and six percent of four hundred and "
        "fifty. <bookmark mark='b4'/>That is one point zero six times four "
        "hundred and fifty, which is again four hundred and seventy seven "
        "rupees."
    ),
    "s3": (
        "A tax can also be written on the bill. <bookmark mark='b0'/>Here is a "
        "medical bill: the amount before value added tax is three hundred and "
        "fifty four rupees and forty five paise. <bookmark mark='b1'/>The value "
        "added tax is five percent, which is seventeen rupees and seventy two "
        "paise. <bookmark mark='b2'/>The total is three hundred and seventy two "
        "rupees and eighteen paise, so the base plus the tax gives the bill. "
        "<bookmark mark='b3'/>Value added tax works exactly like the sales tax "
        "we just used: both are the same percentage idea. <bookmark "
        "mark='b4'/>And remember, these older rates are textbook and historical "
        "examples, not advice about the taxes of today."
    ),
    "s4": (
        "Goods and services tax uses the same structure. <bookmark "
        "mark='b0'/>GST is an indirect tax on goods and services, and it is "
        "charged on the base price. <bookmark mark='b1'/>Take a base price of "
        "one thousand rupees, with GST at five percent. <bookmark mark='b2'/>"
        "Five percent of one thousand is fifty rupees, so the tax amount is "
        "fifty rupees. <bookmark mark='b3'/>Add it to the base: one thousand "
        "plus fifty is one thousand and fifty rupees. <bookmark mark='b4'/>The "
        "shortcut is unchanged: one hundred and five percent of one thousand is "
        "also one thousand and fifty."
    ),
    "s5": (
        "Now the other direction. <bookmark mark='b0'/>A bill of two thousand "
        "three hundred and sixty rupees already includes GST at eighteen "
        "percent. <bookmark mark='b1'/>So this bill is not one hundred percent: "
        "it is one hundred and eighteen percent of the base price. <bookmark "
        "mark='b2'/>To recover the base price we divide: two thousand three "
        "hundred and sixty times one hundred, over one hundred and eighteen. "
        "<bookmark mark='b3'/>That gives a base price of two thousand rupees, "
        "and the tax is the rest, three hundred and sixty rupees. <bookmark "
        "mark='b4'/>Never take eighteen percent of two thousand three hundred "
        "and sixty and subtract it: the rate was charged on the base, not on the "
        "bill."
    ),
    "s6": (
        "Here is a worked example from the textbook. <bookmark mark='b0'/>The "
        "total GST on that purchase is three hundred and sixty rupees. <bookmark "
        "mark='b1'/>In this worked example the tax is divided into two equal "
        "parts. <bookmark mark='b2'/>One half is central GST, one hundred and "
        "eighty rupees. <bookmark mark='b3'/>The other half is state GST, "
        "another one hundred and eighty rupees. <bookmark mark='b4'/>So one "
        "block of three hundred and sixty splits into one hundred and eighty and "
        "one hundred and eighty. That equal split belongs to this worked "
        "example, not to every bill."
    ),
    "s7": (
        "Now a two lane decision board. <bookmark mark='b0'/>If the base price "
        "is given, go forward: find the tax, then add it, or use the bill equals "
        "the base times one hundred plus r, over one hundred. <bookmark "
        "mark='b1'/>If the tax-inclusive bill is given, go backward: recover the "
        "base with base equals bill times one hundred, over one hundred plus r. "
        "<bookmark mark='b2'/>Which lane you use depends only on what you were "
        "given. <bookmark mark='b3'/>And keep tax separate from discount: a "
        "discount is taken away from the price, while a tax is added to the "
        "base. <bookmark mark='b4'/>Tax adds, discount removes."
    ),
    "s8": (
        "Here is the classic error. <bookmark mark='b0'/>Take a base price of "
        "one thousand rupees, with GST at eighteen percent. <bookmark "
        "mark='b1'/>The tax is eighteen percent of one thousand, which is one "
        "hundred and eighty rupees, so the bill is one thousand one hundred and "
        "eighty. <bookmark mark='b2'/>The mistake is to apply the rate to the "
        "bill: eighteen percent of one thousand one hundred and eighty is not "
        "the tax for this purchase. <bookmark mark='b3'/>The same mistake is to "
        "subtract the rate straight off a tax-inclusive bill. <bookmark "
        "mark='b4'/>The rate is always applied to the base, and a tax-inclusive "
        "bill is worked backward with one hundred over one hundred plus r."
    ),
    "s9q": (
        "Your turn. Four quick checks. <bookmark mark='b0'/>A: an item costs "
        "eight hundred rupees, and the tax is five percent. What is the tax, and "
        "what is the bill? <bookmark mark='b1'/>B: a bill of one thousand one "
        "hundred and eighty rupees includes GST at eighteen percent. What is the "
        "base price, and what is the tax? <bookmark mark='b2'/>C: a total GST of "
        "one hundred and eighty rupees is split equally into central GST and "
        "state GST. How much is each part? <bookmark mark='b3'/>D: here is the "
        "error to spot. Eighteen percent of one thousand rupees is one hundred "
        "and eighty rupees, so is eighteen percent of one thousand one hundred "
        "and eighty the right tax for the same purchase? Pause the video, work "
        "all four out, and then we will check every answer."
    ),
    "s9a": (
        "Let us check every answer. <bookmark mark='b0'/>A: five percent of "
        "eight hundred is forty rupees, so the tax is forty rupees and the bill "
        "is eight hundred and forty rupees. <bookmark mark='b1'/>B: the bill is "
        "one hundred and eighteen percent, so the base is one thousand one "
        "hundred and eighty times one hundred over one hundred and eighteen, "
        "which is one thousand rupees, and the tax is one hundred and eighty "
        "rupees. <bookmark mark='b2'/>C: one hundred and eighty split equally is "
        "ninety and ninety, so central GST is ninety rupees and state GST is "
        "ninety rupees. <bookmark mark='b3'/>D: no. Eighteen percent of one "
        "thousand one hundred and eighty is not the tax for this purchase. The "
        "rate belongs on the base of one thousand rupees."
    ),
    "s10": (
        "One last look. <bookmark mark='b0'/>Start at one hundred percent, the "
        "base price. <bookmark mark='b1'/>Add the tax to reach one hundred plus "
        "r percent. <bookmark mark='b2'/>Work backward with one hundred divided "
        "by one hundred plus r when the tax-inclusive total is given. <bookmark "
        "mark='b3'/>And keep the tax separate from a discount: a tax adds to the "
        "base, a discount takes off the price. <bookmark mark='b4'/>So start at "
        "one hundred percent, add the tax, and work backward with one hundred "
        "divided by one hundred plus r. <bookmark mark='b5'/>Thank you for "
        "watching, <bookmark mark='b6'/>and see you in the next lesson."
    ),
}

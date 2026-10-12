"""Board furniture and narration for Storyboard 02 -- Discounts, Marked Price
and Rebate, Class 8 Mathematics, Chapter 5 (Comparing Quantities using
Proportion).

This file is *spliced*, never imported: assemble_discounts.py grafts it into the
proven head of the Chapter 3 quadrilaterals set, so the theme names
(CHALK_*, FONT, BOARD_*), `board_text`, `chalk_math` and the pacing helpers
(`rt`, `quick`, `leftover`) are already defined above it.

The furniture is this video's shop-counter kit:

  * `price_tag`      -- the tagged price of an article (a filled tag with a
                        punched hole, a gloss streak and the rupees on it),
  * `price_sticker`  -- the glossy percent badge stuck on the tag,
  * `book_icon` / `cycle_icon` / `fan_icon` -- the three drawn articles
                        (filled, shaded shapes, each carrying its own price),
  * `split_bar`      -- the 100% = marked-price bar with the discount portion
                        physically cut off it, leaving the selling price,
  * `list_card`      -- a named part card (marked price / discount / SP),
  * `mistake_card`   -- a wrong statement with a drawn cross in the card's top
                        half and its correction in the bottom half,
  * `coin_stack` / `note_stack` -- drawn coins and currency notes,
  * `cross_mark` / `tick` -- the drawn cross and tick (Segoe Print has neither).

Everything is drawn as filled, shaded geometry -- a tag with a punched hole, a
book with a page block, wheels with hubs, a fan with solid blades -- never as a
bare outline.
"""
from __future__ import annotations

import numpy as np

# ------------------------------------------------------------ board layout --
# (this section is spliced into a head whose own imports omit Ellipse, Arc and
#  Sector; Dot, Circle, Line, DashedLine, Rectangle, RoundedRectangle, Polygon,
#  DoubleArrow, VGroup, DEGREES, PI, TAU and np are already imported by the head)
from manim import Arc, Ellipse, Sector  # noqa: E402,F401

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

# The content bands.  Cards are about a unit tall, so their TEXT boxes keep the
# 0.22 units of air the clearance audit asks for at these centres.
BAND_A = 1.05            # the upper band (the part cards, the decision cards)
BAND_B = -0.45           # the lower band (the one-line rule under them)

PANEL_FILL = "#16202B"
CARD_W = 3.00            # the standard card width
CARD_H = 1.10            # the standard card height
CHIP_H = 0.50
BAR_W = 4.20             # the price bar: 100% = the marked price
BAR_H = 0.46

# The example figures this video works with.  Every one is an on-screen example,
# never a textbook fact.
TITLE_MP = 1600
BOOK = (80, 15)          # a book: Rs 80 marked, 15% off
CYCLE = (3600, 3312)     # a cycle: Rs 3600 marked, sold for Rs 3312
FAN = (1600, 6)          # a fan: Rs 1600 marked, 6% off
QUIZ = ((450, 7), (1000, 900), (250, 5))


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


def cross_mark(point, size=0.21, color=CHALK_RED, width=4.2):
    """A drawn cross (Segoe Print has no cross glyph).

    Kept just under 0.45 units across so it can never be read as a figure a
    chalk line runs into; it is always placed inside the same VGroup as what it
    strikes through.
    """
    x, y = float(point[0]), float(point[1])
    return VGroup(
        Line(np.array([x - size, y - size, 0.0]),
             np.array([x + size, y + size, 0.0]),
             stroke_color=color, stroke_width=width),
        Line(np.array([x - size, y + size, 0.0]),
             np.array([x + size, y - size, 0.0]),
             stroke_color=color, stroke_width=width))


def tick(point, color=CHALK_GREEN, s=0.16):
    """A drawn tick (Segoe Print has no tick glyph)."""
    a = np.array([point[0] - s * 0.60, point[1] + s * 0.05, 0.0])
    b = np.array([point[0] - s * 0.05, point[1] - s * 0.55, 0.0])
    c = np.array([point[0] + s * 0.65, point[1] + s * 0.75, 0.0])
    return VGroup(Line(a, b, stroke_color=color, stroke_width=3.4),
                  Line(b, c, stroke_color=color, stroke_width=3.4))


def price_panel(cx, cy, price, color=CHALK_AMBER, size=14):
    """The little price plate a drawn article carries.

    The plate is sized from its own text, so the rupees always sit inside it
    with air to spare.
    """
    lab = board_text(price, size, CHALK_WHITE, "BOLD")
    tag = RoundedRectangle(corner_radius=0.05, width=lab.width + 0.34,
                           height=lab.height + 0.22, stroke_color=color,
                           stroke_width=1.6, fill_color="#2A1D10",
                           fill_opacity=0.75)
    tag.move_to(np.array([float(cx), float(cy), 0.0]))
    lab.move_to(tag.get_center())
    grp = VGroup(tag, lab)
    grp.tag, grp.label = tag, lab
    return grp


def price_tag(price="Rs 1600", cx=BOARD_CX, cy=0.0, color=CHALK_AMBER,
              width=2.50, height=1.24, size=24):
    """The tagged price of an article: a filled tag with a punched hole.

    This is the one object that stays on the board of every scene, so the
    tagged price is never lost when the discount is cut away from it.
    """
    x0, x1 = cx - width / 2.0, cx + width / 2.0
    y0, y1 = cy - height / 2.0, cy + height / 2.0
    body = Polygon(np.array([x0, cy, 0.0]),
                   np.array([x0 + 0.34, y1, 0.0]),
                   np.array([x1, y1, 0.0]),
                   np.array([x1, y0, 0.0]),
                   np.array([x0 + 0.34, y0, 0.0]),
                   stroke_color=color, stroke_width=2.4,
                   fill_color=color, fill_opacity=0.26)
    hole = Circle(radius=0.085, stroke_color=color, stroke_width=1.4,
                  fill_color="#0E1620", fill_opacity=0.95)
    hole.move_to(np.array([x0 + 0.52, cy + height * 0.30, 0.0]))
    gloss = Polygon(np.array([x0 + 0.42, y1 - 0.11, 0.0]),
                    np.array([x1 - 0.10, y1 - 0.11, 0.0]),
                    np.array([x1 - 0.22, y1 - 0.03, 0.0]),
                    np.array([x0 + 0.48, y1 - 0.03, 0.0]),
                    stroke_width=0, fill_color=CHALK_WHITE, fill_opacity=0.16)
    lab = board_text(price, size, CHALK_WHITE, "BOLD")
    lab.move_to(np.array([cx + 0.10, cy - 0.02, 0.0]))
    grp = VGroup(body, hole, gloss, lab)
    grp.body, grp.label = body, lab
    return grp


def price_sticker(text="6% OFF", cx=BOARD_CX, cy=0.0, r=0.50,
                  color=CHALK_PINK, size=15):
    """The glossy percent badge that is stuck over the tag.

    The gloss is a filled slanted slip (never an arc stroke): a stroke would be
    read as a chalk line running through the badge's own lettering.
    """
    cx, cy = float(cx), float(cy)
    disc = Circle(radius=r, stroke_color=color, stroke_width=2.2,
                  fill_color=color, fill_opacity=0.32)
    disc.move_to(np.array([cx, cy, 0.0]))
    gloss = Polygon(np.array([cx - 0.60 * r, cy + 0.44 * r, 0.0]),
                    np.array([cx + 0.06 * r, cy + 0.66 * r, 0.0]),
                    np.array([cx + 0.20 * r, cy + 0.54 * r, 0.0]),
                    np.array([cx - 0.46 * r, cy + 0.34 * r, 0.0]),
                    stroke_width=0, fill_color=CHALK_WHITE, fill_opacity=0.22)
    lab = board_text(text, size, CHALK_WHITE, "BOLD")
    lab.move_to(disc.get_center())
    grp = VGroup(disc, gloss, lab)
    grp.disc, grp.label = disc, lab
    return grp


def coin_stack(cx, cy, n=3, scale=1.0, color=CHALK_YELLOW):
    """A stack of coins: filled discs with thickness, drawn bottom-up."""
    discs = VGroup()
    for i in range(n):
        e = Ellipse(width=0.46 * scale, height=0.16 * scale,
                    stroke_color=color, stroke_width=1.5,
                    fill_color=color, fill_opacity=0.40)
        e.move_to(np.array([cx, cy + 0.075 * i * scale, 0.0]))
        discs.add(e)
    return discs


def note_stack(cx, cy, n=3, scale=1.0, color=CHALK_GREEN):
    """Drawn currency notes: filled slips with a band across each one."""
    notes = VGroup()
    for i in range(n):
        body = RoundedRectangle(corner_radius=0.03, width=0.94 * scale,
                                height=0.34 * scale, stroke_color=color,
                                stroke_width=1.5, fill_color=color,
                                fill_opacity=0.26)
        band = Rectangle(width=0.94 * scale, height=0.05 * scale,
                         stroke_width=0, fill_color=color, fill_opacity=0.55)
        band.move_to(body.get_center())
        slip = VGroup(body, band)
        slip.move_to(np.array([cx + 0.05 * i * scale,
                               cy + 0.10 * i * scale, 0.0]))
        notes.add(slip)
    return notes


def book_icon(cx, cy, price="Rs 80", color=CHALK_CYAN, scale=1.0):
    """A closed book with a page block, a spine and its price plate."""
    w, h = 1.30 * scale, 1.02 * scale
    cover = RoundedRectangle(corner_radius=0.06, width=w, height=h,
                             stroke_color=color, stroke_width=2.2,
                             fill_color=color, fill_opacity=0.28)
    cover.move_to(np.array([float(cx), float(cy), 0.0]))
    pages = Rectangle(width=w * 0.78, height=h * 0.80, stroke_width=0,
                      fill_color=CHALK_WHITE, fill_opacity=0.16)
    pages.align_to(cover, RIGHT).shift(LEFT * 0.07)
    spine = Rectangle(width=0.13 * scale, height=h * 0.90, stroke_width=0,
                      fill_color=color, fill_opacity=0.55)
    spine.move_to(np.array([cx - w / 2 + 0.09 * scale, cy, 0.0]))
    plate = price_panel(cx + 0.14 * scale, cy - h * 0.27, price, color, size=14)
    return VGroup(cover, pages, spine, plate)


def cycle_icon(cx, cy, price="Rs 3600", color=CHALK_AMBER, scale=1.0):
    """A bicycle: two spoked wheels with solid hubs and a filled frame."""
    r = 0.32 * scale
    wheels = VGroup()
    for wx in (cx - 0.54 * scale, cx + 0.54 * scale):
        tyre = Circle(radius=r, stroke_width=0,
                      fill_color=color, fill_opacity=0.55)
        rim = Circle(radius=r * 0.60, stroke_width=0,
                     fill_color=PANEL_FILL, fill_opacity=0.95)
        hub = Circle(radius=r * 0.16, stroke_width=0,
                     fill_color=CHALK_WHITE, fill_opacity=0.85)
        spoked = VGroup(tyre, rim, hub)
        spoked.move_to(np.array([wx, cy - 0.34 * scale, 0.0]))
        for k in range(4):
            ang = k * PI / 4.0
            a = spoked.get_center() + np.array([np.cos(ang), np.sin(ang), 0.0]) \
                * r * 0.55
            b = spoked.get_center() + np.array([-np.cos(ang), -np.sin(ang), 0.0]) \
                * r * 0.55
            spoked.add(Line(a, b, stroke_color=color, stroke_width=1.1))
        wheels.add(spoked)
    frame = Polygon(np.array([cx - 0.54 * scale, cy - 0.34 * scale, 0.0]),
                    np.array([cx + 0.02 * scale, cy + 0.22 * scale, 0.0]),
                    np.array([cx + 0.36 * scale, cy - 0.34 * scale, 0.0]),
                    stroke_color=color, stroke_width=2.4,
                    fill_color=color, fill_opacity=0.18)
    seat = Ellipse(width=0.30 * scale, height=0.13 * scale, stroke_width=0,
                   fill_color=CHALK_WHITE, fill_opacity=0.35)
    seat.move_to(np.array([cx - 0.30 * scale, cy + 0.32 * scale, 0.0]))
    handle = Line(np.array([cx + 0.02 * scale, cy + 0.22 * scale, 0.0]),
                  np.array([cx + 0.30 * scale, cy + 0.44 * scale, 0.0]),
                  stroke_color=color, stroke_width=2.6)
    plate = price_panel(cx + 0.44 * scale, cy + 0.66 * scale, price, color,
                        size=13)
    return VGroup(wheels, frame, seat, handle, plate)


def fan_icon(cx, cy, price="Rs 1600", color=CHALK_CYAN, scale=1.0):
    """A ceiling fan: three solid blades on a hub, on a short down-rod."""
    blades = VGroup()
    for k in range(3):
        blade = RoundedRectangle(corner_radius=0.06, width=0.72 * scale,
                                 height=0.20 * scale, stroke_color=color,
                                 stroke_width=1.6, fill_color=color,
                                 fill_opacity=0.32)
        blade.move_to(np.array([cx + 0.44 * scale, cy, 0.0]))
        blade.rotate(k * TAU / 3.0, about_point=np.array([cx, cy, 0.0]))
        blades.add(blade)
    hub = Circle(radius=0.15 * scale, stroke_color=color, stroke_width=1.8,
                 fill_color=color, fill_opacity=0.65)
    hub.move_to(np.array([float(cx), float(cy), 0.0]))
    rod = Rectangle(width=0.09 * scale, height=0.34 * scale, stroke_width=0,
                    fill_color=color, fill_opacity=0.5)
    rod.move_to(np.array([cx, cy + 0.40 * scale, 0.0]))
    canopy = Ellipse(width=0.34 * scale, height=0.14 * scale,
                     stroke_color=color, stroke_width=1.6,
                     fill_color=color, fill_opacity=0.26)
    canopy.move_to(np.array([cx, cy + 0.60 * scale, 0.0]))
    plate = price_panel(cx, cy - 0.60 * scale, price, color, size=13)
    return VGroup(blades, hub, rod, canopy, plate)


def list_card(head, lines, color=CHALK_CYAN, width=2.90, head_size=15,
              line_size=13, gap=0.26, pad=0.16, height=None):
    """A named part card: a bold head over one or two body lines.

    The card's height is computed from the real text heights, so the head and
    the body keep exactly `gap` (>= the 0.22 the clearance audit asks for) even
    though different lines have different ascenders and descenders.  Pass
    `height` to force a row of cards to one common height.
    """
    body = VGroup(*[board_text(t, line_size, CHALK_WHITE, "BOLD")
                    for t in lines]).arrange(DOWN, buff=gap)
    head_t = board_text(head, head_size, color, "BOLD")
    content = head_t.height + gap + body.height
    box = panel(width, height if height is not None else content + 2 * pad,
                color)
    head_t.move_to(box.get_center() + UP * (content / 2.0 - head_t.height / 2.0))
    body.move_to(head_t.get_center()
                 + DOWN * (head_t.height / 2.0 + gap + body.height / 2.0))
    grp = VGroup(box, head_t, body)
    grp.box, grp.head, grp.body = box, head_t, body
    return grp


def mistake_card(wrong, fix, color=CHALK_RED, width=4.05, height=1.10,
                 wrong_size=15, fix_size=12, fix_color=CHALK_GREEN):
    """A wrong statement struck through by a drawn cross, with its correction.

    The cross occupies the card's top half beside the wrong wording and the fix
    sits in the bottom half, so the strike-through is unmistakable yet never
    comes within the 0.04 units the audit allows between a stroke and a letter.
    The whole card is ONE board object.
    """
    box = panel(width, height, color, opacity=0.62)
    cross = cross_mark(np.array([0.0, 0.0, 0.0]), size=0.20, color=color)
    wrong_t = board_text(wrong, wrong_size, color, "BOLD")
    top = VGroup(cross, wrong_t).arrange(RIGHT, buff=0.30)
    top.move_to(box.get_center() + UP * 0.26)
    fix_t = board_text(fix, fix_size, fix_color, "BOLD")
    fix_t.move_to(box.get_center() + DOWN * 0.26)
    grp = VGroup(box, top, fix_t)
    grp.box, grp.cross, grp.wrong, grp.fix = box, cross, wrong_t, fix_t
    return grp


def split_bar(cx, cy, width=BAR_W, height=BAR_H, cut=0.15, sp_text="",
              sp_size=14, slide=1.10, mp_note="", mp_size=14,
              color_sp=CHALK_GREEN, color_disc=CHALK_PINK, slot_side="right"):
    """The 100% = marked-price bar with the discount portion cut off it.

    The bar is drawn as the whole marked price: the selling-price part stays and
    the discount part is physically cut away and slides aside, which is exactly
    the relation on the board -- marked price minus discount equals selling
    price.  Everything (both parts, their labels, the cut line) is ONE board
    object, so none of its own labels can ever be read as sitting inside
    somebody else's box.

    Attributes:
        .sp        the selling-price part that stays behind
        .disc      the discount part that is cut away
        .delta     the shift that separates the discount part from the bar
        .slot_x    where the (left-aligned) discount label starts
        .slot_y    the line that label is written on
        .cut_x     the x of the cut
    """
    disc_w = width * cut
    sp_w = width - disc_w
    x_left = cx - width / 2.0
    sp = Rectangle(width=sp_w, height=height, stroke_color=color_sp,
                   stroke_width=1.8, fill_color=color_sp, fill_opacity=0.32)
    sp.move_to(np.array([x_left + sp_w / 2.0, cy, 0.0]))
    disc = Rectangle(width=disc_w, height=height, stroke_color=color_disc,
                     stroke_width=1.8, fill_color=color_disc, fill_opacity=0.44)
    disc.move_to(np.array([x_left + sp_w + disc_w / 2.0, cy, 0.0]))
    cut_mark = DashedLine(
        np.array([x_left + sp_w, cy - height / 2.0 - 0.10, 0.0]),
        np.array([x_left + sp_w, cy + height / 2.0 + 0.10, 0.0]),
        stroke_color=CHALK_RED, stroke_width=2.0, dash_length=0.07)
    cut_mark.set_stroke(opacity=0)
    parts = [sp, disc, cut_mark]
    if sp_text:
        lab = board_text(sp_text, sp_size, color_sp, "BOLD")
        lab.move_to(sp.get_center())
        parts.append(lab)
        grp_lab = lab
    else:
        grp_lab = None
    if mp_note:
        note = board_text(mp_note, mp_size, CHALK_WHITE, "BOLD")
        note.move_to(np.array([cx, cy + height / 2.0 + 0.30, 0.0]))
        parts.append(note)
    grp = VGroup(*parts)
    grp.sp, grp.disc, grp.cut_mark, grp.sp_label = sp, disc, cut_mark, grp_lab
    grp.delta = np.array([float(slide), 0.0, 0.0])
    if slot_side == "left":
        # the label sits in the air the cut part leaves behind, between the
        # selling-price bar and the block that was cut off
        grp.slot_x = x_left + sp_w + 0.28
    else:
        grp.slot_x = x_left + sp_w + disc_w / 2.0 + slide + disc_w / 2.0 + 0.28
    grp.slot_y = cy
    grp.cut_x = x_left + sp_w
    return grp


def bar_arrow(cx, cy, width=BAR_W, color=CHALK_WHITE):
    """The full-width arrow under the bar: this whole bar is 100% = MP."""
    return DoubleArrow(np.array([cx - width / 2.0, cy, 0.0]),
                       np.array([cx + width / 2.0, cy, 0.0]),
                       buff=0.0, stroke_color=color, stroke_width=2.0,
                       tip_length=0.14, max_tip_length_to_length_ratio=0.2)


def price_pair(cx, cy, width, mp_text="", sp_text="", frac=0.94, height=BAR_H,
               color_mp=CHALK_AMBER, color_sp=CHALK_GREEN, size=15):
    """Two bars end to end: the marked price and the smaller selling price.

    Both are left-aligned, so the rupees the discount took off are visible as
    the gap at the right-hand end.  The pair is one board object.
    """
    x_left = cx - width / 2.0
    mp = Rectangle(width=width, height=height, stroke_color=color_mp,
                   stroke_width=1.8, fill_color=color_mp, fill_opacity=0.28)
    mp.move_to(np.array([x_left + width / 2.0, cy, 0.0]))
    sp = Rectangle(width=width * frac, height=height, stroke_color=color_sp,
                   stroke_width=1.8, fill_color=color_sp, fill_opacity=0.32)
    sp.move_to(np.array([x_left + width * frac / 2.0, cy - 0.55, 0.0]))
    gap = Rectangle(width=width * (1.0 - frac), height=height,
                    stroke_color=CHALK_PINK, stroke_width=1.8,
                    fill_color=CHALK_PINK, fill_opacity=0.46)
    gap.move_to(np.array([x_left + width * frac + width * (1.0 - frac) / 2.0,
                          cy, 0.0]))
    parts = [mp, sp, gap]
    if mp_text:
        lab = board_text(mp_text, size, CHALK_WHITE, "BOLD")
        lab.move_to(mp.get_center())
        parts.append(lab)
    if sp_text:
        lab = board_text(sp_text, size, CHALK_WHITE, "BOLD")
        lab.move_to(sp.get_center())
        parts.append(lab)
    grp = VGroup(*parts)
    grp.mp, grp.sp, grp.gap = mp, sp, gap
    grp.gap_delta = np.array([-0.30, 0.55, 0.0])
    grp.gap_slot = np.array([gap.get_center()[0], gap.get_center()[1], 0.0])
    return grp


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "Look at this price tag. The price written on it is one thousand six "
        "hundred rupees. <bookmark mark='b0'/> But that sticker says six "
        "percent off, <bookmark mark='b1'/> so the price you pay is not the "
        "price on the tag. Three quantities are at work here. The first is the "
        "marked price: the price written on the article, also called the list "
        "price. <bookmark mark='b2'/> The second is the discount: the amount "
        "reduced, and the same idea is also called a rebate. <bookmark "
        "mark='b3'/> The third is the selling price: what is actually paid. "
        "<bookmark mark='b4'/> One relation ties all three together: marked "
        "price minus discount equals selling price. <bookmark mark='b5'/> And "
        "the tagged price never disappears, because the discount is always "
        "calculated from it, <bookmark mark='b6'/> and never from the selling "
        "price."
    ),
    "s1": (
        "The price tag has three parts, and each part has a name. <bookmark "
        "mark='b0'/> The marked price is the price written on the article; it "
        "is also called the list price, or the catalogue price. <bookmark "
        "mark='b1'/> The discount is the amount that is reduced from that "
        "price, and the same idea is also called a rebate. <bookmark "
        "mark='b2'/> The selling price is what is actually paid at the "
        "counter. <bookmark mark='b3'/> One relation ties the three together: "
        "marked price minus discount equals selling price. <bookmark "
        "mark='b4'/> The tagged price never disappears, because the discount "
        "is always calculated from the marked price. <bookmark mark='b5'/> So "
        "keep the marked price on the board: the discount is only a part of "
        "it."
    ),
    "s2": (
        "A book is marked eighty rupees, and the shop gives fifteen percent "
        "off. <bookmark mark='b0'/> The marked price is the whole bar: one "
        "hundred percent, that is eighty rupees. <bookmark mark='b1'/> Step "
        "one is to find the discount, which is fifteen percent of the marked "
        "price: fifteen over one hundred times eighty is twelve rupees. "
        "<bookmark mark='b2'/> Step two is the selling price: remove that "
        "discount from the marked price, so eighty minus twelve is sixty eight "
        "rupees. <bookmark mark='b3'/> You can see the fifteen percent block "
        "cut away from the bar, and the selling price is what remains. "
        "<bookmark mark='b4'/> So marked price minus discount equals selling "
        "price. <bookmark mark='b5'/> And the discount is always calculated on "
        "the marked price, never on the selling price, <bookmark mark='b6'/> "
        "because the marked price is the base for every discount."
    ),
    "s3": (
        "Now let us find a discount percentage. <bookmark mark='b0'/> A "
        "bicycle is marked three thousand six hundred rupees, and it is sold "
        "for three thousand three hundred and twelve rupees. <bookmark "
        "mark='b1'/> The difference between the two prices is two hundred and "
        "eighty eight rupees, and you can see that gap at the end of the bars. "
        "<bookmark mark='b2'/> Now the discount percentage: its base is the "
        "marked price, never the selling price. <bookmark mark='b3'/> The gap "
        "is measured against the whole bar, so the percentage is two hundred "
        "and eighty eight divided by three thousand six hundred, times one "
        "hundred. <bookmark mark='b4'/> That is eight percent. <bookmark "
        "mark='b5'/> Always divide by the marked price, and never by the "
        "selling price."
    ),
    "s4": (
        "Now the other direction: the discount percentage is given, and we "
        "must find the selling price. <bookmark mark='b0'/> A ceiling fan is "
        "marked one thousand six hundred rupees, with six percent off. The "
        "discount is six percent of the marked price: six over one hundred "
        "times one thousand six hundred is ninety six rupees. <bookmark "
        "mark='b1'/> The selling price is the marked price minus the discount, "
        "so one thousand six hundred minus ninety six is one thousand five "
        "hundred and four rupees. <bookmark mark='b2'/> Notice that the "
        "discount amount is ninety six rupees, while the discount rate is six "
        "percent. <bookmark mark='b3'/> One is money, the other is a "
        "percentage of the marked price, <bookmark mark='b4'/> so keep the "
        "amount in rupees and the rate in percent, and never mix the two up."
    ),
    "s5": (
        "There is a shortcut, and it comes from one simple idea. <bookmark "
        "mark='b0'/> If six percent is taken off the marked price, then ninety "
        "four percent is still payable. <bookmark mark='b1'/> Route one: find "
        "the discount first, ninety six rupees, and subtract it from one "
        "thousand six hundred. <bookmark mark='b2'/> Route two: find the "
        "remaining percent first, ninety four percent, and multiply it by one "
        "thousand six hundred. <bookmark mark='b3'/> Both routes give one "
        "thousand five hundred and four rupees. <bookmark mark='b4'/> So the "
        "shortcut is: selling price equals one hundred minus d, over one "
        "hundred, times the marked price. <bookmark mark='b5'/> Use whichever "
        "route you like, but check that the two routes agree. <bookmark "
        "mark='b6'/> Two different routes are a free check on your answer."
    ),
    "s6": (
        "There are three questions you can be asked, and each one has its own "
        "route. <bookmark mark='b0'/> If the marked price and the discount "
        "percentage are given, find the discount first, and then subtract it "
        "from the marked price. <bookmark mark='b1'/> If the marked price and "
        "the selling price are given, find the discount by subtraction, and "
        "then divide that discount by the marked price, times one hundred. "
        "<bookmark mark='b2'/> If the marked price and the discount amount are "
        "given, the selling price is simply marked price minus discount. "
        "<bookmark mark='b3'/> In every case the first move is the same: find "
        "the discount, or find the marked price. <bookmark mark='b4'/> And in "
        "every case the base for a percentage is the marked price. <bookmark "
        "mark='b5'/> Read the question twice, and pick the route that fits the "
        "quantities you were given."
    ),
    "s7": (
        "Now the mistakes that cost marks, and the fix for each one. <bookmark "
        "mark='b0'/> The first mistake is calculating the discount percentage "
        "on the selling price instead of the marked price. <bookmark "
        "mark='b1'/> The second is adding the discount to the marked price, "
        "instead of subtracting it. <bookmark mark='b2'/> The third is "
        "confusing the discount amount, ninety six rupees, with the discount "
        "rate, six percent. <bookmark mark='b3'/> The fourth is reading "
        "fifteen percent off as if you pay fifteen percent, when eighty five "
        "percent is still payable. <bookmark mark='b4'/> So check three things "
        "every time: the base is the marked price, the discount is subtracted, "
        "and the rate is a percentage while the amount is in rupees. <bookmark "
        "mark='b5'/> Fix those four habits, and the marks stop leaking away."
    ),
    "s8": (
        "Before you write the answer, check that it makes sense. <bookmark "
        "mark='b0'/> A discount always makes the selling price smaller than "
        "the marked price, so the selling price must be less than the marked "
        "price. <bookmark mark='b1'/> And if d percent is taken off, then one "
        "hundred minus d percent is still payable. <bookmark mark='b2'/> Here "
        "the marked price is one thousand six hundred rupees, and the selling "
        "price is one thousand five hundred and four rupees, which is smaller. "
        "<bookmark mark='b3'/> Six percent off leaves ninety four percent "
        "payable, and six plus ninety four is one hundred. <bookmark "
        "mark='b4'/> So two checks every time: the selling price must be "
        "smaller than the marked price, and the two percentages must add up to "
        "one hundred. Write those two lines on your rough sheet before you "
        "answer."
    ),
    "s9q": (
        "Your turn. Four quick checks. <bookmark mark='b0'/> First: a shirt is "
        "marked four hundred and fifty rupees with seven percent off. Find the "
        "discount, and then the selling price. <bookmark mark='b1'/> Second: "
        "an article is marked one thousand rupees and sold for nine hundred "
        "rupees. Find the discount, and then the discount percentage. "
        "<bookmark mark='b2'/> Third: a table is marked two hundred and fifty "
        "rupees with five percent off. Find the selling price directly, using "
        "the percent that remains. <bookmark mark='b3'/> And last: check that "
        "every selling price you write is smaller than its marked price. Take "
        "your time, and pause the video if you need to."
    ),
    "s9a": (
        "Let us check. <bookmark mark='b0'/> For the shirt: seven percent of "
        "four hundred and fifty is thirty one rupees fifty, so the selling "
        "price is four hundred and fifty minus thirty one fifty, which is four "
        "hundred and eighteen rupees fifty. <bookmark mark='b1'/> For the "
        "article: the discount is one thousand minus nine hundred, that is one "
        "hundred rupees, and one hundred divided by one thousand, times one "
        "hundred, is ten percent. <bookmark mark='b2'/> For the table: five "
        "percent off leaves ninety five percent, and ninety five over one "
        "hundred times two hundred and fifty is two hundred and thirty seven "
        "rupees fifty. <bookmark mark='b3'/> And in all three the selling "
        "price is smaller than the marked price, and the base was the marked "
        "price. Check both of those every time, and your answers will be right."
    ),
    "s10": (
        "The whole chapter in four lines. <bookmark mark='b0'/> One: the "
        "marked price is the price written on the article, and the discount, "
        "or rebate, is calculated from it. <bookmark mark='b1'/> Two: the "
        "selling price is what is actually paid, and selling price equals "
        "marked price minus discount. <bookmark mark='b2'/> Three: the "
        "discount percentage is the discount divided by the marked price, "
        "times one hundred. <bookmark mark='b3'/> Four: the price flow is tag, "
        "reduce, pay, compare. <bookmark mark='b4'/> So keep the marked price "
        "visible, subtract the discount, and check the answer against the tag. "
        "<bookmark mark='b5'/> Thank you for watching, <bookmark mark='b6'/> "
        "and see you in the next lesson."
    ),
}

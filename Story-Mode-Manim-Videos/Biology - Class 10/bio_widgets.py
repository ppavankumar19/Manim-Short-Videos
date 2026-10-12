"""Card / label helpers shared by the Biology videos."""
from __future__ import annotations

import numpy as np

from bio_kit import *  # noqa: F401,F403
from bio_art import *  # noqa: F401,F403
from bio_water_art import *  # noqa: F401,F403

# ------------------------------------------------------------ helpers -------
def fm(tex, color=CHALK_WHITE, size=40, w=None, h=None, pad=0.30):
    """A boxed chemical formula."""
    m = M(tex, size, color)
    box = panel(w or m.width + 2 * pad, h or m.height + 0.30, color,
                radius=0.14, stroke=2.4)
    m.move_to(box)
    g = VGroup(box, m)
    g.box = box
    return g


def icard(icon, head, sub, color, w=3.0, h=1.5, icon_w=1.0, head_size=26,
          sub_size=22):
    """Icon on the left, name + one line on the right, in a tight card."""
    ic = fit(icon, icon_w, h - 0.3)
    txt = VGroup(T(head, head_size, color)).arrange(DOWN, aligned_edge=LEFT)
    if sub:
        txt.add(T(sub, sub_size, CHALK_WHITE))
        txt.arrange(DOWN, buff=0.08, aligned_edge=LEFT)
    fit(txt, w - ic.width - 0.65, h - 0.3)
    row = VGroup(ic, txt).arrange(RIGHT, buff=0.25)
    box = panel(row.width + 0.5, max(row.height + 0.3, 0.7), color)
    row.move_to(box)
    g = VGroup(box, row)
    g.box = box
    return g


def stack_card(icon, head, lines_, color, w=3.1, h=2.7, icon_h=1.1,
               head_size=28, line_size=22):
    """Picture on top, bold head, short lines under it."""
    ic = fit(icon, w - 0.5, icon_h)
    parts = [ic, T(head, head_size, color, max_w=w - 0.3)]
    parts += [T(s, line_size, CHALK_WHITE, max_w=w - 0.3) for s in lines_]
    col = VGroup(*parts).arrange(DOWN, buff=0.12)
    box = panel(max(w, 0.1), max(h, col.height + 0.30), color)
    col.move_to(box)
    g = VGroup(box, col)
    g.box = box
    g._tight = True          # fixed size: neighbours stay the same height
    return g


def pic_card(pic, caption, color, w=4.2, h=2.7, pic_w=3.5, pic_h=1.75,
             cap_size=22):
    """A fixed-size card: the picture sits in the upper part and the caption
    in its own strip underneath, so text can never touch the drawing."""
    box = panel(w, h, color)
    pic = fit(pic, pic_w, pic_h)
    cap = T(caption, cap_size, color, max_w=w - 0.4)
    strip_h = cap.height + 0.12
    top_room = h - strip_h - 0.45
    pic.move_to(box.get_top() + DOWN * (0.20 + top_room / 2))
    cap.move_to(box.get_bottom() + UP * (0.17 + cap.height / 2))
    g = VGroup(box, pic, cap)
    g.box = box
    g._tight = True
    return g


def big_plant(ground_y, h=2.5, soil_w=3.2, cx=None):
    pl = plant(h, soil_w=soil_w)
    pl.move_to([CX if cx is None else cx, ground_y, 0])
    # .move_to centres the whole group; re-seat so the ground line is exact
    pl.shift(UP * (ground_y - pl.soil.get_top()[1]))
    return pl


def crown_of(pl):
    return pl.leaves[-1].get_center()




XYL_C = "#42A5F5"          # the blue water pathway
VAP_C = "#B3E5FC"
PUSH_C = "#FFB74D"         # root pressure (small push)
PULL_C = "#F06292"         # transpiration pull (main pull)


def qa_row(letter, question, answer, color, w=9.4, h=0.62, size=22):
    """One challenge row: letter badge, question text, '?' / answer slot at
    the right.  Fixed size so a stack of rows aligns."""
    box = panel(w, h, color, radius=0.14, stroke=2.4)
    badge = num_badge(letter, color, r=0.23, size=22)
    badge.move_to(box.get_left() + RIGHT * 0.30)
    q = T(question, size, CHALK_WHITE, max_w=w - 3.9)
    q.next_to(badge, RIGHT, buff=0.22)
    slot = T(answer, size + 2, color, max_w=3.3)
    slot.move_to(box.get_right() + LEFT * (0.25 + slot.width / 2))
    g = VGroup(box, badge, q, slot)
    g.box, g.slot = box, slot
    g._tight = True
    return g



def chain(labels, colors, size=22, gap=0.10, arrow_len=0.34):
    """Chips joined by arrows:  A -> B -> C."""
    parts = []
    for k, (lb, col) in enumerate(zip(labels, colors)):
        parts.append(chip(lb, col, size))
        if k < len(labels) - 1:
            parts.append(arrow([0, 0, 0], [arrow_len, 0, 0], CHALK_WHITE, 6, 0.16))
    return VGroup(*parts).arrange(RIGHT, buff=gap)

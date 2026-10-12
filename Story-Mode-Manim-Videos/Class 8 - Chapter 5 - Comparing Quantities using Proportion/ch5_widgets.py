"""Card / row widgets shared by the Chapter 5 topic scripts."""
from __future__ import annotations

from ch5_kit import *  # noqa: F401,F403
from ch5_art import *  # noqa: F401,F403


def part_card(icon, head, body, color, w=3.1, h=3.0, icon_h=0.90,
              head_size=28, body_size=24):
    """An illustrated card: picture on top, bold name, short lines."""
    ic = fit(icon, w - 0.7, icon_h)
    head_t = T(head, head_size, color, max_w=w - 0.3)
    body_t = lines(body, body_size, CHALK_WHITE, buff=0.08, max_w=w - 0.3)
    content = VGroup(ic, head_t, body_t).arrange(DOWN, buff=0.14)
    box = panel(w, h, color)
    content.move_to(box.get_center())
    g = VGroup(box, content)
    g.box = box
    return g


def route_row(tag, given, todo, color, w=9.6, h=0.82, size=26, tsize=24):
    """tag, GIVEN  ->  what to do."""
    box = panel(w, h, color, radius=0.14, stroke=2.4)
    badge = num_badge(tag, color, r=0.26)
    badge.move_to(box.get_left() + RIGHT * (0.24 + badge.width / 2))
    g_ = T(given, size, color)
    arr = Arrow(ORIGIN, RIGHT * 0.7, buff=0, stroke_width=5, tip_length=0.2,
                color=CHALK_WHITE)
    td = T(todo, tsize, CHALK_WHITE)
    txt = VGroup(g_, arr, td).arrange(RIGHT, buff=0.28)
    fit(txt, w - badge.width - 0.8, h - 0.16)
    txt.next_to(badge, RIGHT, buff=0.30)
    g = VGroup(box, badge, txt)
    g.box = box
    return g


def mistake_card(wrong, fix, w=4.8, h=1.45, size=26):
    """A wrong statement struck by a drawn cross, with its correction."""
    box = panel(w, h, CHALK_RED, opacity=0.78)
    cross = cross_mark(ORIGIN, size=0.2, color=CHALK_RED, width=6)
    wr = T(wrong, size, CHALK_RED)
    top = VGroup(cross, wr).arrange(RIGHT, buff=0.45)
    fit(top, w - 0.5, 0.5)
    fx = T(fix, size - 2, CHALK_GREEN, max_w=w - 0.5)
    both = VGroup(top, fx).arrange(DOWN, buff=0.26)
    both.move_to(box.get_center())
    g = VGroup(box, both)
    g.box = box
    return g


def q_card(icon, head, body, color, w=4.85, h=1.95):
    """A 'your turn' prompt: picture on the left, name + lines on the right."""
    box = panel(w, h, color)
    ic = fit(icon, 1.35, h - 0.4)
    ic.move_to(box.get_left() + RIGHT * (0.2 + ic.width / 2 + 0.05))
    txt = VGroup(T(head, 28, color),
                 *[T(s, 24, CHALK_WHITE) for s in body]).arrange(
        DOWN, buff=0.1, aligned_edge=LEFT)
    fit(txt, w - 1.95, h - 0.3)
    txt.next_to(ic, RIGHT, buff=0.22)
    g = VGroup(box, ic, txt)
    g.box = box
    return g


def icon_chip(icon, text, color, w=4.6, h=1.0, size=26, icon_w=1.0):
    """A chip with a small picture on its left."""
    box = panel(w, h, color)
    ic = fit(icon, icon_w, h - 0.22)
    ic.move_to(box.get_left() + RIGHT * (0.2 + ic.width / 2))
    t = T(text, size, color) if isinstance(text, str) else text
    fit(t, w - ic.width - 0.6, h - 0.2)
    t.next_to(ic, RIGHT, buff=0.22)
    g = VGroup(box, ic, t)
    g.box = box
    return g


def table_icon(w=1.5):
    top = RoundedRectangle(corner_radius=0.05, width=w, height=w * 0.14)
    top.set_fill("#C98B4A", 1).set_stroke(OUTLINE, 3)
    top.set_sheen(0.3, UL)
    legs = VGroup(*[Rectangle(width=w * 0.09, height=w * 0.62).set_fill(
        "#A56F36", 1).set_stroke(OUTLINE, 3) for _ in range(2)])
    legs[0].next_to(top, DOWN, buff=0).align_to(top, LEFT).shift(RIGHT * w * 0.08)
    legs[1].next_to(top, DOWN, buff=0).align_to(top, RIGHT).shift(LEFT * w * 0.08)
    return VGroup(top, legs)


def ticket(w=2.0, color="#FFB347", label="TICKET", size=22):
    """A raffle ticket with two punched notches and a star."""
    h = w * 0.5
    body = RoundedRectangle(corner_radius=0.08, width=w, height=h)
    paint(body, color, op=1, lw=2.8, sheen=0.25)
    notches = VGroup(*[Circle(radius=h * 0.13, stroke_color=OUTLINE,
                              stroke_width=2.4, fill_color="#16202B",
                              fill_opacity=1).move_to(
        [sx * w / 2, 0, 0]) for sx in (-1, 1)])
    perf = DashedLine([w * 0.22, h / 2 - 0.06, 0], [w * 0.22, -h / 2 + 0.06, 0],
                      stroke_color=OUTLINE, stroke_width=2, dash_length=0.07)
    star = Star(n=5, outer_radius=h * 0.26, inner_radius=h * 0.11,
                fill_color="#FFF3C4", fill_opacity=1, stroke_color=OUTLINE,
                stroke_width=1.6).move_to([-w * 0.30, 0, 0])
    t = T(label, size, "#4A2A06")
    fit(t, w * 0.34, h * 0.5)
    t.move_to([w * 0.02, 0, 0])
    return VGroup(body, notches, perf, star, t)


def pie(frac, r=0.8, color=CHALK_CYAN, rest="#25384A"):
    """A percent pie: filled sector for `frac` of the circle."""
    base = Circle(radius=r, stroke_color=OUTLINE, stroke_width=3,
                  fill_color=rest, fill_opacity=1)
    sec = Sector(radius=r, angle=TAU * frac, start_angle=PI / 2,
                 fill_color=color, fill_opacity=1, stroke_color=OUTLINE,
                 stroke_width=3)
    sec.set_sheen(0.25, UL)
    return VGroup(base, sec)

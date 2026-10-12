"""Drawn-from-geometry illustrations for the Chapter 5 videos.

Every function returns a VGroup centred on ORIGIN (move it with P()/move_to).
The look is a shaded cartoon: a dark outline, a pastel body, a soft sheen and a
ground shadow -- so each object reads as a thing, not as a doodle.  Only core
Manim mobjects are used (Polygon, Arc, Ellipse, Star, Sector, BarChart, Axes,
NumberLine, Brace ...), the same toolbox shown in Manim-Mobjects-and-Animations
and manimce-public-animations.
"""
from __future__ import annotations

import numpy as np

from ch5_kit import *  # noqa: F401,F403
from ch5_kit import (CHALK_AMBER, CHALK_CYAN, CHALK_GREEN, CHALK_PINK,
                     CHALK_RED, CHALK_WHITE, CHALK_YELLOW, CHALK_BLUE,
                     CHALK_PURPLE, PANEL_FILL, T, M, fit, panel, P)
from manim import (VGroup, Polygon, Circle, Ellipse, Rectangle,
                   RoundedRectangle, Line, Arc, Star, Sector, AnnularSector,
                   Dot, DashedLine, CubicBezier, VMobject, UP, DOWN, LEFT,
                   RIGHT, UL, UR, DL, DR, ORIGIN, PI, TAU, DEGREES, ArcBetweenPoints,
                   Square, BarChart, Axes, NumberLine, Brace, Text)

OUTLINE = "#0E141B"


# ---------------------------------------------------------------- paint -----
def paint(m, fill, op=0.96, line=OUTLINE, lw=3.0, sheen=0.30, sdir=UL):
    """Fill + dark outline + soft sheen (the shaded-cartoon look)."""
    m.set_fill(fill, op)
    m.set_stroke(line, lw)
    if sheen:
        m.set_sheen(sheen, sdir)
    return m


def shadow(w, h=None, y=0.0, op=0.38):
    e = Ellipse(width=w, height=h or w * 0.16, fill_color="#000000",
                fill_opacity=op, stroke_width=0)
    e.move_to([0, y, 0])
    return e


def _pts(seq, sc=1.0):
    return [np.array([x * sc, y * sc, 0.0]) for x, y in seq]


def poly(seq, fill, sc=1.0, round_r=0.0, **kw):
    p = Polygon(*_pts(seq, sc))
    if round_r:
        p.round_corners(round_r)
    return paint(p, fill, **kw)


# ---------------------------------------------------------- price things ----
def shop_tag(price="Rs 1600", w=3.4, h=1.55, color=CHALK_AMBER, size=44,
             price_color="#2B1A08"):
    """A hanging price tag: chamfered card, punched eyelet, string, price."""
    cham = h * 0.42
    outline = [(-w / 2, 0), (-w / 2 + cham, h / 2), (w / 2, h / 2),
               (w / 2, -h / 2), (-w / 2 + cham, -h / 2)]
    sh = Polygon(*_pts(outline)).round_corners(0.12)
    sh.set_fill("#000000", 0.34).set_stroke(width=0).shift(
        np.array([0.07, -0.09, 0]))
    body = poly(outline, "#F6E3B4", round_r=0.12, lw=3.4, sheen=0.28)
    rim = Polygon(*_pts([(-w / 2 + cham + 0.05, h / 2 - 0.10),
                         (w / 2 - 0.10, h / 2 - 0.10),
                         (w / 2 - 0.10, -h / 2 + 0.10),
                         (-w / 2 + cham + 0.05, -h / 2 + 0.10),
                         (-w / 2 + 0.22, 0)]))
    rim.set_fill(opacity=0).set_stroke(color, 2.4, opacity=0.9)
    eye_c = np.array([-w / 2 + cham * 0.62, 0, 0])
    ring = Circle(radius=0.17, stroke_color=color, stroke_width=4,
                  fill_color="#10161C", fill_opacity=1).move_to(eye_c)
    hole = Circle(radius=0.075, stroke_width=0, fill_color="#0A0F14",
                  fill_opacity=1).move_to(eye_c)
    string = CubicBezier(eye_c + np.array([-0.05, 0.02, 0]),
                         eye_c + np.array([-0.55, 0.55, 0]),
                         eye_c + np.array([-0.15, 0.95, 0]),
                         eye_c + np.array([-0.55, 1.15, 0]))
    string.set_stroke(CHALK_WHITE, 3.2, opacity=0.9)
    lab = T(price, size, price_color)
    fit(lab, w - cham - 0.95, h - 0.45)
    lab.move_to([cham * 0.30 + 0.10, 0, 0])
    g = VGroup(sh, string, body, rim, ring, hole, lab)
    g.body, g.label = body, lab
    return g


def sticker(top="6%", bottom="OFF", r=0.78, color=CHALK_PINK, size=34):
    """The glossy starburst percent sticker."""
    star = Star(n=16, outer_radius=r, inner_radius=r * 0.84,
                fill_color=color, fill_opacity=1, stroke_color="#7A1E36",
                stroke_width=3)
    star.set_sheen(0.35, UL)
    ring = Circle(radius=r * 0.72, stroke_color="#7A1E36", stroke_width=2.2,
                  stroke_opacity=0.7, fill_opacity=0)
    t1 = T(top, size, "#5A0F26")
    t2 = T(bottom, int(size * 0.72), "#5A0F26")
    fit(t1, r * 1.25)
    fit(t2, r * 1.1)
    VGroup(t1, t2).arrange(DOWN, buff=0.03).move_to(star.get_center())
    g = VGroup(star, ring, t1, t2)
    g.star, g.t1, g.t2 = star, t1, t2
    return g


def rupee_note(w=2.0, color="#8FD3A0", label="Rs 100", size=22):
    h = w * 0.48
    body = RoundedRectangle(corner_radius=0.07, width=w, height=h)
    paint(body, color, op=1, lw=2.6, sheen=0.18)
    inner = RoundedRectangle(corner_radius=0.05, width=w * 0.90, height=h * 0.78)
    inner.set_fill(opacity=0).set_stroke("#FFFFFF", 1.6, opacity=0.8)
    medal = Circle(radius=h * 0.26, stroke_color="#FFFFFF", stroke_width=2,
                   fill_color="#FFFFFF", fill_opacity=0.28)
    medal.move_to([-w * 0.20, 0, 0])
    t = T(label, size, "#143A23")
    fit(t, w * 0.48, h * 0.5)
    t.move_to([w * 0.20, 0, 0])
    dots = VGroup(*[Dot(radius=0.025, color="#FFFFFF").move_to(p) for p in
                    [[-w * 0.41, h * 0.30, 0], [w * 0.41, h * 0.30, 0],
                     [-w * 0.41, -h * 0.30, 0], [w * 0.41, -h * 0.30, 0]]])
    return VGroup(body, inner, medal, t, dots)


def note_stack(n=3, w=2.0, color="#8FD3A0", label="Rs 100", size=22):
    g = VGroup()
    for i in range(n):
        note = rupee_note(w, color, label, size)
        note.shift(np.array([0.10 * i, 0.13 * i, 0]))
        g.add(note)
    return g


def coin(r=0.32, color="#F4C542", label="Rs"):
    c = Circle(radius=r, stroke_color="#7A5A08", stroke_width=3,
               fill_color=color, fill_opacity=1)
    c.set_sheen(0.4, UL)
    ring = Circle(radius=r * 0.74, stroke_color="#8A6A12", stroke_width=2,
                  fill_opacity=0)
    t = T(label, int(r * 56), "#5A4004")
    t.move_to(c.get_center())
    return VGroup(c, ring, t)


def coin_stack(n=4, r=0.42, color="#F4C542"):
    """A pile of coins seen from slightly above: side wall + top ellipse."""
    g = VGroup()
    th = 0.15
    for i in range(n):
        y = i * th
        side = Rectangle(width=2 * r, height=th, stroke_width=0,
                         fill_color="#C9961B", fill_opacity=1).move_to([0, y, 0])
        under = Ellipse(width=2 * r, height=r * 0.7, stroke_width=0,
                        fill_color="#C9961B", fill_opacity=1).move_to(
            [0, y - th / 2, 0])
        top = Ellipse(width=2 * r, height=r * 0.7, stroke_color="#7A5A08",
                      stroke_width=2, fill_color=color, fill_opacity=1)
        top.set_sheen(0.35, UL).move_to([0, y + th / 2, 0])
        g.add(under, side, top)
    return g


def calculator(display="1504", w=1.9, accent=CHALK_AMBER):
    h = w * 1.42
    body = RoundedRectangle(corner_radius=0.16, width=w, height=h)
    paint(body, "#46566A", lw=3.2, sheen=0.22)
    scr_h = h * 0.22
    screen = RoundedRectangle(corner_radius=0.06, width=w * 0.82, height=scr_h)
    paint(screen, "#14352B", op=1, line="#08140F", lw=2, sheen=0)
    screen.move_to([0, h / 2 - 0.16 - scr_h / 2, 0])
    txt = T(display, 30, CHALK_GREEN)
    fit(txt, w * 0.74, scr_h * 0.7)
    txt.move_to(screen.get_center())
    txt.align_to(screen, RIGHT).shift(LEFT * 0.12)
    keys = VGroup()
    gx = w * 0.82 / 4
    top_y = screen.get_bottom()[1] - 0.20
    avail = top_y - (-h / 2 + 0.16)
    gy = avail / 4
    for r_ in range(4):
        for c_ in range(4):
            col = accent if c_ == 3 else "#C9D3DD"
            k = RoundedRectangle(corner_radius=0.05, width=gx * 0.78,
                                 height=gy * 0.70)
            paint(k, col, lw=1.6, sheen=0.3)
            k.move_to([-w * 0.41 + gx * (c_ + 0.5), top_y - gy * (r_ + 0.5), 0])
            keys.add(k)
    return VGroup(body, screen, txt, keys)


def receipt(w=2.2, h=3.2, rows=("ITEM", "TAX", "TOTAL"), size=22,
            colors=None):
    """A till receipt with a zig-zag torn edge."""
    teeth = 9
    pts = [(-w / 2, h / 2), (w / 2, h / 2)]
    for i in range(teeth + 1):
        x = w / 2 - i * w / teeth
        pts.append((x, -h / 2 + (0.12 if i % 2 else 0.0)))
    body = Polygon(*_pts(pts))
    paint(body, "#F7F1DE", op=1, lw=2.4, sheen=0.15)
    g = VGroup(shadow(w * 0.9, 0.16, -h / 2 - 0.02), body)
    ys = np.linspace(h / 2 - 0.55, -h / 2 + 0.65, len(rows))
    for i, (r_, y) in enumerate(zip(rows, ys)):
        col = (colors[i] if colors else "#2A2A2A")
        t = T(r_, size, col)
        fit(t, w - 0.4)
        t.move_to([0, y, 0])
        g.add(t)
        if i < len(rows) - 1:
            d = DashedLine([-w / 2 + 0.2, y - 0.33, 0], [w / 2 - 0.2, y - 0.33, 0],
                           stroke_color="#8B8B8B", stroke_width=1.8,
                           dash_length=0.08)
            g.add(d)
    return g


# -------------------------------------------------------------- articles ----
def shirt(w=2.0, color="#6FA8FF"):
    sc = w
    body = poly([(-0.16, 0.50), (-0.40, 0.42), (-0.64, 0.14), (-0.52, 0.00),
                 (-0.35, 0.12), (-0.35, -0.50), (0.35, -0.50), (0.35, 0.12),
                 (0.52, 0.00), (0.64, 0.14), (0.40, 0.42), (0.16, 0.50),
                 (0.0, 0.40)], color, sc=sc, round_r=0.05 * sc / 2,
                lw=3.2)
    collar = poly([(-0.16, 0.50), (0.0, 0.26), (0.16, 0.50), (0.0, 0.40)],
                  "#EAF2FF", sc=sc, lw=2.4, sheen=0)
    placket = Line(np.array([0, 0.26 * sc, 0]), np.array([0, -0.50 * sc, 0]),
                   stroke_color=OUTLINE, stroke_width=2.0, stroke_opacity=0.7)
    buttons = VGroup(*[Dot(radius=0.028 * sc, color="#F5F2E9").move_to(
        [0, y * sc, 0]) for y in (0.12, -0.06, -0.24, -0.40)])
    pocket = poly([(0.10, 0.02), (0.28, 0.02), (0.28, -0.16), (0.10, -0.16)],
                  color, sc=sc, lw=1.8, sheen=0)
    return VGroup(shadow(0.8 * sc, 0.1 * sc, -0.52 * sc), body, collar,
                  placket, buttons, pocket)


def book(w=1.8, color="#59B4E6"):
    h = w * 1.28
    pages = RoundedRectangle(corner_radius=0.03, width=w * 0.94, height=h * 0.96)
    paint(pages, "#F6F1E3", op=1, lw=2.0, sheen=0)
    pages.move_to([0.07 * w, -0.03 * h, 0])
    cover = RoundedRectangle(corner_radius=0.05, width=w * 0.94, height=h * 0.96)
    paint(cover, color, lw=3.2, sheen=0.28)
    spine = Rectangle(width=w * 0.14, height=h * 0.96, stroke_width=0,
                      fill_color="#2F86B8", fill_opacity=1)
    spine.align_to(cover, LEFT).align_to(cover, DOWN)
    label = RoundedRectangle(corner_radius=0.04, width=w * 0.52, height=h * 0.22)
    paint(label, "#FDF6DA", op=1, lw=1.8, sheen=0)
    label.move_to(cover.get_center() + np.array([w * 0.08, h * 0.17, 0]))
    ln = VGroup(*[Line([-w * 0.20, y, 0], [w * 0.20, y, 0],
                       stroke_color="#2A2A2A", stroke_width=3.0)
                  for y in (h * 0.04, -h * 0.04)])
    ln.move_to(label.get_center())
    star = Star(n=5, outer_radius=w * 0.13, inner_radius=w * 0.055,
                fill_color=CHALK_YELLOW, fill_opacity=1, stroke_width=0)
    star.move_to(cover.get_center() + np.array([w * 0.08, -h * 0.20, 0]))
    ribbon = poly([(0, 0), (0.07, 0), (0.07, -0.20), (0.035, -0.15), (0, -0.20)],
                  CHALK_RED, sc=w, lw=1.4, sheen=0)
    ribbon.move_to([w * 0.28, -h * 0.5 - 0.02, 0])
    return VGroup(shadow(w * 1.0, w * 0.14, -h * 0.52), pages, cover, spine,
                  label, ln, star, ribbon)


def bicycle(w=3.0, color="#F0A23C"):
    r = w * 0.2
    ax_r, ax_f = np.array([-1.15 * r, 0, 0]), np.array([1.15 * r, 0, 0])
    bb = np.array([-0.15 * r, 0, 0])
    seat = np.array([-0.55 * r, 0.98 * r, 0])
    ht = np.array([0.72 * r, 1.04 * r, 0])
    hb = np.array([0.80 * r, 0.80 * r, 0])
    g = VGroup(shadow(w * 0.95, w * 0.07, -r))
    for ax in (ax_r, ax_f):
        tyre = Circle(radius=r, stroke_color="#1A1F26", stroke_width=9,
                      fill_opacity=0).move_to(ax)
        rim = Circle(radius=r * 0.90, stroke_color="#C9D3DD", stroke_width=3,
                     fill_opacity=0).move_to(ax)
        spokes = VGroup(*[
            Line(ax, ax + r * 0.9 * np.array([np.cos(a), np.sin(a), 0]),
                 stroke_color="#C9D3DD", stroke_width=1.2, stroke_opacity=0.9)
            for a in np.linspace(0, TAU, 17)[:-1]])
        hub = Dot(radius=0.06, color="#E9EEF3").move_to(ax)
        g.add(tyre, rim, spokes, hub)
    def bar(a, b, wd=6.5, col=color):
        return Line(a, b, stroke_color=col, stroke_width=wd)
    frame = VGroup(bar(ax_r, bb), bar(ax_r, seat), bar(bb, seat),
                   bar(seat, ht), bar(bb, hb), bar(hb, ht),
                   bar(hb, ax_f, 5.5, "#C9D3DD"))
    stem = bar(ht, ht + np.array([-0.08 * r, 0.22 * r, 0]), 4.5, "#C9D3DD")
    hbar = bar(ht + np.array([-0.08 * r, 0.22 * r, 0]),
               ht + np.array([0.20 * r, 0.26 * r, 0]), 5.5, "#1A1F26")
    saddle = bar(seat + np.array([-0.30 * r, 0.10 * r, 0]),
                 seat + np.array([0.12 * r, 0.12 * r, 0]), 9, "#1A1F26")
    chainring = Circle(radius=0.20 * r, stroke_color="#C9D3DD", stroke_width=3,
                       fill_opacity=0).move_to(bb)
    crank = bar(bb, bb + np.array([0.12 * r, -0.30 * r, 0]), 3.5, "#C9D3DD")
    pedal = bar(bb + np.array([0.04 * r, -0.30 * r, 0]),
                bb + np.array([0.26 * r, -0.30 * r, 0]), 5, "#1A1F26")
    g.add(frame, stem, hbar, saddle, chainring, crank, pedal)
    return g


def ceiling_fan(w=3.0, color="#7FB8E8"):
    """A three-blade ceiling fan seen from below: paddles on arms around a
    motor hub with a lit dome, and a faint ring for the spin."""
    R = w / 2.0
    g = VGroup()
    spin = Circle(radius=R * 0.99, stroke_color=CHALK_WHITE, stroke_width=2,
                  stroke_opacity=0.28, fill_opacity=0)
    g.add(spin)
    for k in range(3):
        ang = 90 + k * 120
        arm = poly([(0.14, 0.05), (0.40, 0.05), (0.40, -0.05), (0.14, -0.05)],
                   "#5E6E80", sc=R, lw=2.0, sheen=0.1)
        blade = poly([(0.34, 0.15), (0.90, 0.21), (0.99, 0.0), (0.90, -0.21),
                      (0.34, -0.15)], color, sc=R, round_r=0.06 * R, lw=3.0,
                     sheen=0.40)
        edge = Line(np.array([0.46 * R, 0.0, 0.0]), np.array([0.88 * R, 0.0, 0.0]),
                    stroke_color="#FFFFFF", stroke_width=3, stroke_opacity=0.45)
        grp = VGroup(arm, blade, edge)
        grp.rotate(ang * DEGREES, about_point=ORIGIN)
        g.add(grp)
    hub = Circle(radius=0.24 * R)
    paint(hub, "#4C6A8A", lw=3.0, sheen=0.35)
    ring = Circle(radius=0.17 * R, stroke_color="#C9D3DD", stroke_width=2.2,
                  fill_color="#2F4A66", fill_opacity=1)
    dome = Circle(radius=0.10 * R, stroke_width=0, fill_color="#FFE8A8",
                  fill_opacity=1)
    g.add(hub, ring, dome)
    return g


# ------------------------------------------------------------ bar models ----
def segbar(w, parts, h=0.78, size=26, gap=0.0, outline=True):
    """Bar model: `parts` = [(fraction, colour, label), ...] left to right.

    Returns a VGroup with .segs (each a VGroup(rect, label)), .left_x and
    .right_x.  Fractions are of the full width `w`.
    """
    segs = VGroup()
    x = -w / 2
    for frac, col, label in parts:
        sw = w * frac
        rect = Rectangle(width=max(sw - gap, 0.02), height=h,
                         stroke_color=col, stroke_width=3,
                         fill_color=col, fill_opacity=0.40)
        rect.set_sheen(0.15, UL)
        rect.move_to([x + sw / 2, 0, 0])
        parts_ = [rect]
        if label:
            lab = T(label, size, CHALK_WHITE)
            fit(lab, sw - 0.14, h - 0.14)
            lab.move_to(rect.get_center())
            parts_.append(lab)
        seg = VGroup(*parts_)
        seg.rect = rect
        segs.add(seg)
        x += sw
    g = VGroup(segs)
    g.segs = segs
    g.left_x, g.right_x = -w / 2, w / 2
    return g


def brace_label(mob, text, direction=UP, size=26, color=CHALK_WHITE, buff=0.12,
                max_w=None):
    b = Brace(mob, direction=direction, color=color, buff=buff,
              stroke_width=1.2)
    t = T(text, size, color, max_w=max_w)
    t.next_to(b, direction, buff=0.10)
    g = VGroup(b, t)
    g.brace, g.label = b, t
    return g


def hundred_grid(side=0.27, gap=0.04, color=CHALK_CYAN, empty="#25384A"):
    """10x10 percent square, cells ordered row by row from the bottom-left."""
    cells = VGroup()
    step = side + gap
    for r_ in range(10):
        for c_ in range(10):
            sq = Square(side_length=side, stroke_width=1.2,
                        stroke_color="#0E141B", fill_color=empty,
                        fill_opacity=1)
            sq.move_to([(c_ - 4.5) * step, (r_ - 4.5) * step, 0])
            cells.add(sq)
    cells.fill_color_on = color
    return cells


# ------------------------------------------------------------ more articles --
def fridge(h=2.4, color="#D6E4EE"):
    w = h * 0.55
    body = RoundedRectangle(corner_radius=0.10, width=w, height=h)
    paint(body, color, lw=3.2, sheen=0.30)
    seam = Line([-w / 2, h * 0.16, 0], [w / 2, h * 0.16, 0],
                stroke_color=OUTLINE, stroke_width=3)
    hand1 = RoundedRectangle(corner_radius=0.03, width=0.06, height=h * 0.16)
    paint(hand1, "#7C8B99", lw=1.6, sheen=0)
    hand1.move_to([w / 2 - 0.16, h * 0.30, 0])
    hand2 = hand1.copy().move_to([w / 2 - 0.16, -h * 0.02, 0])
    feet = VGroup(*[Rectangle(width=0.14, height=0.07, stroke_width=0,
                              fill_color=OUTLINE, fill_opacity=1).move_to(
        [sx * w * 0.36, -h / 2 - 0.035, 0]) for sx in (-1, 1)])
    magnet = Circle(radius=0.07, fill_color=CHALK_RED, fill_opacity=1,
                    stroke_width=0).move_to([-w * 0.25, h * 0.36, 0])
    return VGroup(shadow(w * 1.3, 0.12, -h / 2 - 0.07), feet, body, seam, hand1,
                  hand2, magnet)


def truck(w=2.6, color="#F0A23C"):
    s = w / 2.6
    cargo = RoundedRectangle(corner_radius=0.06, width=1.65 * s, height=1.0 * s)
    paint(cargo, color, lw=3.0, sheen=0.28).move_to([-0.35 * s, 0.1 * s, 0])
    cab = poly([(0.50, -0.40), (0.50, 0.50), (0.90, 0.50), (1.20, 0.10),
                (1.20, -0.40)], "#6FA8FF", sc=s, round_r=0.05 * s, lw=3.0)
    win = poly([(0.58, 0.40), (0.58, 0.10), (0.96, 0.10), (1.10, 0.40 - 0.30)],
               "#EAF4FF", sc=s, lw=2.0, sheen=0)
    chassis = Rectangle(width=2.55 * s, height=0.10 * s, stroke_width=0,
                        fill_color=OUTLINE, fill_opacity=1).move_to(
        [0.0, -0.42 * s, 0])
    wheels = VGroup()
    for wx in (-0.85, 0.20, 0.88):
        tyre = Circle(radius=0.23 * s, stroke_color="#0A0F14", stroke_width=3,
                      fill_color="#1A1F26", fill_opacity=1)
        hub = Circle(radius=0.09 * s, stroke_width=0, fill_color="#C9D3DD",
                     fill_opacity=1)
        wheels.add(VGroup(tyre, hub).move_to([wx * s, -0.48 * s, 0]))
    return VGroup(shadow(2.4 * s, 0.14 * s, -0.74 * s), chassis, cargo, cab, win,
                  wheels)


def wrench(w=2.2, color="#C9D3DD"):
    from manim import Difference
    h = w * 0.13
    handle = RoundedRectangle(corner_radius=h / 2, width=w * 0.8, height=h)
    paint(handle, color, lw=2.6, sheen=0.4)
    r = w * 0.15
    heads = VGroup()
    for sx in (-1, 1):
        ring = Circle(radius=r)
        notch = Rectangle(width=r * 1.2, height=r * 0.9)
        notch.move_to([sx * r * 0.9, 0, 0])
        jaw = Difference(ring, notch, fill_opacity=1, stroke_width=3)
        paint(jaw, color, lw=2.6, sheen=0.4)
        jaw.move_to([sx * w * 0.42, 0, 0])
        heads.add(jaw)
    g = VGroup(handle, heads)
    g.rotate(35 * DEGREES)
    return g


def building(w=1.9, color="#8FA9C7"):
    h = w * 1.25
    body = Rectangle(width=w, height=h)
    paint(body, color, lw=3.0, sheen=0.25)
    roof = Rectangle(width=w * 1.08, height=h * 0.07)
    paint(roof, "#5E6E80", lw=2.4, sheen=0).move_to([0, h / 2 + h * 0.035, 0])
    wins = VGroup()
    for r_ in range(3):
        for c_ in range(3):
            win = Rectangle(width=w * 0.2, height=h * 0.14)
            paint(win, "#FFE8A8" if (r_ + c_) % 2 == 0 else "#BFD9F2", lw=1.6,
                  sheen=0)
            win.move_to([(c_ - 1) * w * 0.29, h * 0.30 - r_ * h * 0.24, 0])
            wins.add(win)
    door = Rectangle(width=w * 0.22, height=h * 0.2)
    paint(door, "#6B4A2B", lw=1.8, sheen=0).move_to([0, -h / 2 + h * 0.10, 0])
    return VGroup(shadow(w * 1.2, 0.12, -h / 2), body, roof, wins, door)


def _crescent(p0, p1, a_out, a_in, fill="#FFE066"):
    from manim import ArcBetweenPoints
    arc1 = ArcBetweenPoints(np.array(p0), np.array(p1), angle=a_out)
    arc2 = ArcBetweenPoints(np.array(p1), np.array(p0), angle=a_in)
    c = VMobject()
    c.set_points(arc1.points)
    c.append_points(arc2.points)
    return paint(c, fill, lw=2.6, sheen=0.3)


def bananas(w=2.2):
    g = VGroup()
    for k, dy in enumerate((0.0, 0.34, 0.68)):
        c = _crescent([-0.55 * w, 0.15 * w + dy * w * 0.5, 0],
                      [0.55 * w, 0.30 * w + dy * w * 0.5, 0],
                      -1.25, 0.32)
        g.add(c)
        tip = Dot(radius=0.03 * w, color="#5B3A12").move_to(
            [0.55 * w, 0.30 * w + dy * w * 0.5, 0])
        g.add(tip)
    g.move_to(ORIGIN)
    return g


def tv(w=2.2):
    h = w * 0.62
    body = RoundedRectangle(corner_radius=0.08, width=w, height=h)
    paint(body, "#2A3340", lw=3.2, sheen=0.2)
    screen = RoundedRectangle(corner_radius=0.05, width=w * 0.9, height=h * 0.82)
    paint(screen, "#5FA8E8", lw=1.6, sheen=0.45)
    play = Polygon([-0.08 * w, 0.10 * w, 0], [-0.08 * w, -0.10 * w, 0],
                   [0.12 * w, 0, 0])
    play.set_fill("#FFFFFF", 0.9).set_stroke(width=0)
    stand = VGroup(Rectangle(width=w * 0.12, height=h * 0.14),
                   Rectangle(width=w * 0.40, height=h * 0.06))
    stand.set_fill("#2A3340", 1).set_stroke(OUTLINE, 2)
    stand[0].move_to([0, -h / 2 - h * 0.07, 0])
    stand[1].move_to([0, -h / 2 - h * 0.17, 0])
    return VGroup(body, screen, play, stand)


def balance(tilt=0.0, left="", right="", w=4.4, lcol=CHALK_AMBER,
            rcol=CHALK_GREEN, size=24):
    """Two-pan balance.  tilt > 0 drops the RIGHT pan (right side heavier).
    The structure is identical for every tilt so Transform morphs the swing."""
    L = w * 0.42
    piv = np.array([0.0, 0.95, 0.0])
    a = tilt * DEGREES
    el = piv + L * np.array([-np.cos(a), np.sin(a), 0])
    er = piv + L * np.array([np.cos(a), -np.sin(a), 0])
    S = 1.05
    pw = w * 0.30
    base = poly([(-0.95, -1.15), (0.95, -1.15), (0.62, -0.92), (-0.62, -0.92)],
                "#6B4A2B", lw=3.0)
    pole = Rectangle(width=0.14, height=piv[1] + 0.95)
    paint(pole, "#8A6A45", lw=2.4, sheen=0.3)
    pole.move_to([0, (piv[1] - 0.95) / 2, 0])
    beam = Line(el, er, stroke_color="#E0B070", stroke_width=11)
    beam_o = Line(el, er, stroke_color=OUTLINE, stroke_width=15)
    pivot = Circle(radius=0.12, stroke_color=OUTLINE, stroke_width=2.5,
                   fill_color="#F4C542", fill_opacity=1).move_to(piv)
    parts = [base, pole, beam_o, beam, pivot]
    for end, txt, col in ((el, left, lcol), (er, right, rcol)):
        pc = end + np.array([0, -S, 0])
        pan = Polygon(pc + np.array([-pw / 2, 0, 0]),
                      pc + np.array([pw / 2, 0, 0]),
                      pc + np.array([pw * 0.36, -0.20, 0]),
                      pc + np.array([-pw * 0.36, -0.20, 0]))
        paint(pan, "#B9C4CF", lw=2.6, sheen=0.4)
        s1 = Line(end, pc + np.array([-pw / 2, 0, 0]), stroke_color="#E9EEF3",
                  stroke_width=2.2)
        s2 = Line(end, pc + np.array([pw / 2, 0, 0]), stroke_color="#E9EEF3",
                  stroke_width=2.2)
        lab = T(txt, size, col) if txt else T(" ", size, col)
        blk = panel(max(lab.width + 0.3, 0.6), 0.52, col, radius=0.10,
                    stroke=2.4)
        lab.move_to(blk.get_center())
        grp = VGroup(blk, lab)
        grp.move_to(pc + np.array([0, 0.40, 0]))
        parts += [s1, s2, pan, grp]
    return VGroup(*parts)


# ------------------------------------------------------------ shop things ----
def sneaker(w=3.0, color="#FF8F70"):
    """A side-on trainer: rounded upper, white sole, laces and a heel tab."""
    s = w
    upper = poly([(-0.50, -0.20), (-0.50, 0.12), (-0.40, 0.27), (-0.18, 0.29),
                  (-0.06, 0.40), (0.06, 0.22), (0.30, 0.10), (0.50, 0.00),
                  (0.58, -0.10), (0.56, -0.20)], color, sc=s,
                 round_r=0.06 * s, lw=3.2, sheen=0.35)
    sole = RoundedRectangle(corner_radius=0.05 * s, width=1.16 * s,
                            height=0.12 * s)
    paint(sole, "#F5F2E9", op=1, lw=2.8, sheen=0.2).move_to([0.04 * s, -0.25 * s, 0])
    swoosh = poly([(-0.34, -0.06), (-0.05, 0.10), (0.20, 0.02), (-0.02, -0.02),
                   (-0.30, -0.14)], "#FFFFFF", sc=s, round_r=0.03 * s, lw=1.4,
                  sheen=0)
    laces = VGroup(*[Line([(0.00 + 0.07 * i) * s, (0.20 - 0.032 * i) * s, 0],
                          [(0.07 + 0.07 * i) * s, (0.27 - 0.032 * i) * s, 0],
                          stroke_color="#FFFFFF", stroke_width=3.6)
                     for i in range(4)])
    tab = poly([(-0.52, 0.10), (-0.47, 0.30), (-0.40, 0.27), (-0.43, 0.10)],
               "#C94E30", sc=s, lw=1.6, sheen=0)
    return VGroup(shadow(1.15 * s, 0.07 * s, -0.33 * s), upper, sole, swoosh,
                  laces, tab)


def shoe_pair(w=3.0):
    return sneaker(w)


def pharmacy(w=2.8):
    s = w
    body = Rectangle(width=0.92 * s, height=0.62 * s)
    paint(body, "#F2EBDD", lw=3.0, sheen=0.15).move_to([0, -0.05 * s, 0])
    awn = VGroup()
    n = 6
    aw = 1.0 * s / n
    for i in range(n):
        x0 = -0.5 * s + i * aw
        st = Polygon([x0, 0.30 * s, 0], [x0 + aw, 0.30 * s, 0],
                     [x0 + aw * 1.08, 0.16 * s, 0], [x0 - aw * 0.08, 0.16 * s, 0])
        paint(st, "#E5484D" if i % 2 == 0 else "#FFFFFF", op=1, lw=2.2,
              sheen=0.25)
        awn.add(st)
    sign = RoundedRectangle(corner_radius=0.04 * s, width=0.42 * s,
                            height=0.22 * s)
    paint(sign, "#FFFFFF", op=1, lw=2.4, sheen=0).move_to([0, 0.43 * s, 0])
    cross = VGroup(Rectangle(width=0.14 * s, height=0.045 * s),
                   Rectangle(width=0.045 * s, height=0.14 * s))
    cross.set_fill("#2EAA5A", 1).set_stroke(width=0)
    cross.move_to(sign.get_center())
    door = Rectangle(width=0.20 * s, height=0.34 * s)
    paint(door, "#8FC4E8", lw=2.4, sheen=0.3).move_to([0.22 * s, -0.19 * s, 0])
    win = Rectangle(width=0.34 * s, height=0.24 * s)
    paint(win, "#BFE3F7", lw=2.4, sheen=0.3).move_to([-0.22 * s, -0.12 * s, 0])
    return VGroup(shadow(1.0 * s, 0.07 * s, -0.37 * s), body, sign, cross, awn,
                  door, win)


def shopping_bag(w=1.6, color="#FFB347"):
    h = w * 1.1
    body = poly([(-0.5, -0.5), (0.5, -0.5), (0.42, 0.36), (-0.42, 0.36)], color,
                sc=w, round_r=0.03 * w, lw=3.0)
    h1 = Arc(radius=0.17 * w, start_angle=0, angle=PI, stroke_color=OUTLINE,
             stroke_width=4).move_to([-0.15 * w, 0.40 * w, 0])
    h2 = h1.copy().move_to([0.15 * w, 0.40 * w, 0])
    badge = Circle(radius=0.15 * w, stroke_color=OUTLINE, stroke_width=2.4,
                   fill_color="#FFF3C4", fill_opacity=1).move_to([0, -0.05 * w, 0])
    pct = T("%", int(w * 22), "#B02030")
    pct.move_to(badge)
    return VGroup(shadow(1.0 * w, 0.1 * w, -0.52 * w), h1, h2, body, badge, pct)


def padlock(w=0.9, color="#F4C542"):
    body = RoundedRectangle(corner_radius=0.08 * w, width=w, height=w * 0.78)
    paint(body, color, lw=3.0, sheen=0.35).move_to([0, -w * 0.12, 0])
    sh = Arc(radius=w * 0.30, start_angle=0, angle=PI, stroke_color="#C9D3DD",
             stroke_width=7).move_to([0, w * 0.40, 0])
    sh_o = Arc(radius=w * 0.30, start_angle=0, angle=PI, stroke_color=OUTLINE,
               stroke_width=11).move_to([0, w * 0.40, 0])
    hole = Circle(radius=w * 0.09, stroke_width=0, fill_color=OUTLINE,
                  fill_opacity=1).move_to([0, -w * 0.07, 0])
    slot = Rectangle(width=w * 0.07, height=w * 0.2, stroke_width=0,
                     fill_color=OUTLINE, fill_opacity=1).move_to(
        [0, -w * 0.20, 0])
    return VGroup(sh_o, sh, body, hole, slot)


def person(base=ORIGIN, height=1.9, facing=RIGHT, shirt="#4F8EF7"):
    from human_figure import Man
    return Man(base=base, height=height, facing=facing, shirt=shirt)


def block(w, h, color, text="", size=26, op=0.55):
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=3,
                  fill_color=color, fill_opacity=op)
    r.set_sheen(0.2, UL)
    g = VGroup(r)
    if text:
        t = T(text, size, CHALK_WHITE)
        fit(t, w - 0.1, h - 0.1)
        t.move_to(r)
        g.add(t)
    g.rect = r
    return g


def money_bag(w=1.3, color="#D9B26F", label="Rs"):
    body = Ellipse(width=w, height=w * 0.92)
    paint(body, color, lw=3.0, sheen=0.35).move_to([0, -w * 0.08, 0])
    neck = poly([(-0.18, 0.0), (0.18, 0.0), (0.30, 0.20), (-0.30, 0.20)], color,
                sc=w, lw=3.0, sheen=0.2).move_to([0, w * 0.38, 0])
    tie = RoundedRectangle(corner_radius=0.03 * w, width=w * 0.5, height=w * 0.09)
    paint(tie, "#B02030", lw=1.8, sheen=0).move_to([0, w * 0.29, 0])
    t = T(label, int(w * 30), "#5A3A06")
    t.move_to([0, -w * 0.10, 0])
    return VGroup(shadow(w * 0.9, w * 0.12, -w * 0.52), body, neck, tie, t)


def tiles(a, b, side=0.30, ca=CHALK_CYAN, cb=CHALK_AMBER, gap=0.06):
    """Two rows of square tiles: `a` of the first colour above `b` of the
    second -- a ratio you can count."""
    ra = VGroup(*[Square(side_length=side, stroke_color=OUTLINE, stroke_width=2,
                         fill_color=ca, fill_opacity=0.95)
                  for _ in range(a)]).arrange(RIGHT, buff=gap)
    rb = VGroup(*[Square(side_length=side, stroke_color=OUTLINE, stroke_width=2,
                         fill_color=cb, fill_opacity=0.95)
                  for _ in range(b)]).arrange(RIGHT, buff=gap)
    g = VGroup(ra, rb).arrange(DOWN, buff=gap, aligned_edge=LEFT)
    return g


def dial(n, r=1.0, labels=None, size=24,
         colors=(CHALK_CYAN, CHALK_AMBER, CHALK_GREEN, CHALK_PINK)):
    """A one-year clock face cut into `n` equal conversion periods."""
    span = TAU / n
    gap = 0.07 if n > 1 else 0.0
    g = VGroup()
    for k in range(n):
        a0 = PI / 2 - (k + 1) * span + gap / 2
        sec = Sector(radius=r, angle=span - gap, start_angle=a0,
                     fill_color=colors[k % len(colors)], fill_opacity=0.80,
                     stroke_color=OUTLINE, stroke_width=3)
        sec.set_sheen(0.25, UL)
        g.add(sec)
        if labels:
            mid = PI / 2 - (k + 0.5) * span
            pos = 0.60 * r * np.array([np.cos(mid), np.sin(mid), 0])
            if n == 1:
                pos = np.array([0, 0.30 * r, 0])
            lab = T(labels[k], size, "#0E141B")
            fit(lab, r * 0.8 if n > 1 else r * 1.2, r * 0.45)
            lab.move_to(pos)
            g.add(lab)
    hub = Circle(radius=0.10 * r, stroke_color=OUTLINE, stroke_width=2,
                 fill_color="#F5F2E9", fill_opacity=1)
    g.add(hub)
    return g


def house(w=1.0, color="#E8B769"):
    body = Rectangle(width=w, height=w * 0.62)
    paint(body, color, lw=2.8, sheen=0.25).move_to([0, 0, 0])
    roof = Polygon([-w * 0.62, w * 0.31, 0], [w * 0.62, w * 0.31, 0],
                   [0, w * 0.78, 0])
    paint(roof, "#C0504D", lw=2.8, sheen=0.25)
    door = Rectangle(width=w * 0.2, height=w * 0.36)
    paint(door, "#6B4A2B", lw=1.8, sheen=0).move_to([0, -w * 0.13, 0])
    win = Square(side_length=w * 0.2)
    paint(win, "#BFE3F7", lw=1.8, sheen=0.3).move_to([w * 0.28, w * 0.06, 0])
    return VGroup(shadow(w * 1.2, w * 0.12, -w * 0.31), body, roof, door, win)

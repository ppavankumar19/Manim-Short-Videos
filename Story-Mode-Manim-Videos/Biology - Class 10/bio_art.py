"""Realistic, shaded illustrations for the Class 10 Biology videos.

Everything is built from Manim primitives (Polygon, Ellipse, Circle, Arc,
ParametricFunction, Line, Sector ...) with gradients, sheens, highlights, soft
glows and ground shadows -- so a leaf has veins and a lit surface, atoms are
shaded spheres, the Sun glows, roots branch, a plant cell has a wall, a
vacuole, a nucleus and chloroplasts with grana.

Every function returns a VGroup centred on ORIGIN unless noted.
"""
from __future__ import annotations

import numpy as np

from bio_kit import *  # noqa: F401,F403
from bio_kit import (CHALK_AMBER, CHALK_CYAN, CHALK_GREEN, CHALK_PINK,
                     CHALK_RED, CHALK_WHITE, CHALK_YELLOW, CHALK_PURPLE,
                     PANEL_FILL, T, M, fit, panel, P)
from manim import (VGroup, Polygon, Circle, Ellipse, Rectangle,
                   RoundedRectangle, Line, Arc, Dot, DashedLine, VMobject,
                   ParametricFunction, Sector, AnnularSector, CubicBezier,
                   UP, DOWN, LEFT, RIGHT, UL, UR, DL, DR, ORIGIN, PI, TAU,
                   DEGREES, Text, Square, Arrow, ManimColor)

OUTLINE = "#0B1410"


# ------------------------------------------------------------------ paint ---
def paint(m, fill, op=1.0, line=OUTLINE, lw=2.4, sheen=0.28, sdir=UL):
    m.set_fill(fill, op)
    m.set_stroke(line, lw)
    if sheen:
        m.set_sheen(sheen, sdir)
    return m


def shadow(w, h=None, y=0.0, op=0.35):
    e = Ellipse(width=w, height=h or w * 0.16, fill_color="#000000",
                fill_opacity=op, stroke_width=0)
    e.move_to([0, y, 0])
    return e


def _smooth(points, closed=True):
    m = VMobject()
    pts = [np.array(p, dtype=float) for p in points]
    if closed:
        pts = pts + [pts[0]]
    m.set_points_smoothly(pts)
    return m


def glow(r, color, layers=7, peak=0.55):
    """A soft radial glow: stacked translucent discs."""
    g = VGroup()
    for i in range(layers):
        k = (layers - i) / layers
        c = Circle(radius=r * (0.35 + 0.65 * k), stroke_width=0,
                   fill_color=color, fill_opacity=peak * (1 - k) ** 1.2 + 0.03)
        g.add(c)
    return g


# -------------------------------------------------------------- the Sun ------
def sun(r=0.8, rays=14, halo=True):
    g = VGroup()
    if halo:
        g.add(glow(r * 2.3, "#FFD54A", layers=8, peak=0.28))
    for k in range(rays):
        a = k * TAU / rays
        long = k % 2 == 0
        L = r * (0.95 if long else 0.65)
        w = 0.22 * r
        tri = Polygon([r * 1.12, -w / 2, 0], [r * 1.12 + L, 0, 0],
                      [r * 1.12, w / 2, 0])
        tri.set_fill("#FFC107", 0.95).set_stroke("#B26A00", 1.4)
        tri.rotate(a, about_point=ORIGIN)
        g.add(tri)
    disc = Circle(radius=r)
    paint(disc, ["#FFF59D", "#FFB300"], lw=3, sheen=0.55, line="#B26A00")
    core = Circle(radius=r * 0.62, stroke_width=0, fill_color="#FFFDE7",
                  fill_opacity=0.5).shift(UL * r * 0.12)
    g.add(disc, core)
    return g


# --------------------------------------------------------------- leaves ------
def leaf(L=2.0, W=0.9, curve=0.10, color_a="#2E7D32", color_b="#7CB342",
         veins=6, tip=True):
    """A lit leaf pointing along +x with its base at the origin."""
    n = 40
    ts = np.linspace(0, 1, n)
    prof = lambda t: (np.sin(np.pi * t ** 0.85)) ** 0.9
    top = [[L * t, W / 2 * prof(t) + curve * L * np.sin(np.pi * t) * 0.5, 0]
           for t in ts]
    bot = [[L * t, -W / 2 * prof(t) + curve * L * np.sin(np.pi * t) * 0.5, 0]
           for t in ts[::-1]]
    body = _smooth(top + bot[1:-1], closed=True)
    paint(body, [color_a, color_b, color_a], lw=2.6, sheen=0.22,
          line="#1B3D1F")
    mid_pts = [[L * t, curve * L * np.sin(np.pi * t) * 0.5, 0]
               for t in np.linspace(0.02, 0.96, 18)]
    mid = _smooth(mid_pts, closed=False)
    mid.set_fill(opacity=0).set_stroke("#DCEDC8", 3.2, opacity=0.9)
    vs = VGroup()
    for k in range(veins):
        t0 = 0.14 + 0.72 * k / max(veins - 1, 1)
        for sgn in (1, -1):
            y0 = curve * L * np.sin(np.pi * t0) * 0.5
            x1 = L * min(t0 + 0.14, 0.97)
            y1 = y0 + sgn * W / 2 * prof(min(t0 + 0.14, 0.97)) * 0.78
            vs.add(Line([L * t0, y0, 0], [x1, y1, 0], stroke_color="#C5E1A5",
                        stroke_width=1.6, stroke_opacity=0.75))
    return VGroup(body, vs, mid)


def droplet(h=0.5, color="#4FC3F7"):
    a = h / 2
    ts = np.linspace(0, TAU, 60, endpoint=False)
    pts = [[a * np.sin(t) * np.sin(t / 2) * 0.95, a * np.cos(t), 0] for t in ts]
    d = _smooth(pts)
    paint(d, [color, "#0277BD"], lw=2.2, sheen=0.4, line="#01579B")
    hi = Ellipse(width=a * 0.28, height=a * 0.55, stroke_width=0,
                 fill_color="#FFFFFF", fill_opacity=0.65)
    hi.rotate(20 * DEGREES).move_to([-a * 0.28, -a * 0.18, 0])
    return VGroup(d, hi)


# --------------------------------------------------------------- atoms -------
ATOM = {"C": ("#9E9E9E", "#424242"), "O": ("#EF5350", "#B71C1C"),
        "H": ("#FAFAFA", "#B0BEC5")}


def atom(sym, r):
    c1, c2 = ATOM[sym]
    s = Circle(radius=r)
    paint(s, [c1, c2], lw=2.0, sheen=0.55, sdir=UL, line="#1A1A1A")
    hi = Circle(radius=r * 0.28, stroke_width=0, fill_color="#FFFFFF",
                fill_opacity=0.6).move_to([-r * 0.35, r * 0.35, 0])
    return VGroup(s, hi)


def _bond(a, b, n=1, w=5):
    v = np.array(b) - np.array(a)
    n_ = np.array([-v[1], v[0], 0.0])
    n_ = n_ / (np.linalg.norm(n_) + 1e-9)
    g = VGroup()
    offs = [0.0] if n == 1 else [-0.045, 0.045]
    for o in offs:
        g.add(Line(np.array(a) + n_ * o, np.array(b) + n_ * o,
                   stroke_color="#CFD8DC", stroke_width=w))
    return g


def co2(s=1.0):
    """O=C=O, linear, shaded balls."""
    r_c, r_o, d = 0.15 * s, 0.17 * s, 0.38 * s
    pos = [(-d, 0, 0), (0, 0, 0), (d, 0, 0)]
    g = VGroup(_bond(pos[0], pos[1], 2, 4), _bond(pos[1], pos[2], 2, 4))
    g.add(atom("O", r_o).move_to(pos[0]), atom("C", r_c).move_to(pos[1]),
          atom("O", r_o).move_to(pos[2]))
    return g


def h2o(s=1.0):
    r_o, r_h, d = 0.17 * s, 0.10 * s, 0.30 * s
    a = 52 * DEGREES
    h1 = np.array([-d * np.sin(a), -d * np.cos(a), 0])
    h2 = np.array([d * np.sin(a), -d * np.cos(a), 0])
    g = VGroup(_bond(ORIGIN, h1, 1, 4), _bond(ORIGIN, h2, 1, 4))
    g.add(atom("H", r_h).move_to(h1), atom("H", r_h).move_to(h2),
          atom("O", r_o))
    return g


def o2(s=1.0):
    r, d = 0.17 * s, 0.20 * s
    g = VGroup(_bond([-d, 0, 0], [d, 0, 0], 2, 4))
    g.add(atom("O", r).move_to([-d, 0, 0]), atom("O", r).move_to([d, 0, 0]))
    return g


def glucose_ring(r=0.55, labels=True, color="#FFB74D"):
    """Beta-D-glucose (pyranose): six-membered ring, ring oxygen at the top,
    four OH groups and a CH2OH -- a skeletal structure drawn by vertex."""
    angs = [90, 150, 210, 270, 330, 30]            # V0 = ring O
    V = [np.array([r * np.cos(a * DEGREES), r * np.sin(a * DEGREES), 0])
         for a in angs]
    g = VGroup()
    fill = Polygon(*V)
    fill.set_fill(color, 0.28).set_stroke(width=0)
    g.add(fill)
    for k in range(6):
        g.add(Line(V[k], V[(k + 1) % 6], stroke_color=CHALK_WHITE,
                   stroke_width=4.2))
    subs = [(1, "OH", CHALK_RED), (2, "OH", CHALK_RED), (3, "OH", CHALK_RED),
            (4, "OH", CHALK_RED), (5, "CH2OH", CHALK_CYAN)]
    for k, lab, col in subs:
        d = np.array([np.cos(angs[k] * DEGREES), np.sin(angs[k] * DEGREES), 0])
        p1 = V[k] + d * r * 0.50
        g.add(Line(V[k], p1, stroke_color=CHALK_WHITE, stroke_width=3.2))
        if labels:
            t = T(lab, 16, col)
            half = np.array([abs(d[0]) * t.width / 2 + 0.03,
                             abs(d[1]) * t.height / 2 + 0.03, 0])
            t.move_to(p1 + d * np.linalg.norm(half) * 1.0)
            g.add(t)
    ob = Circle(radius=r * 0.2, stroke_width=0, fill_color=PANEL_FILL,
                fill_opacity=1).move_to(V[0])
    ot = T("O", 18, CHALK_RED).move_to(V[0])
    g.add(ob, ot)
    return g


def glucose_hex(r=0.3, color="#FFB74D"):
    """A simplified glucose badge (a ring) used inside chains."""
    hexa = Polygon(*[[r * np.cos((90 + 60 * k) * DEGREES),
                      r * np.sin((90 + 60 * k) * DEGREES), 0]
                     for k in range(6)])
    paint(hexa, color, op=0.9, lw=2.4, sheen=0.4, line="#6D4C0F")
    o = Dot(radius=r * 0.12, color="#B71C1C").move_to(hexa.get_vertices()[0])
    return VGroup(hexa, o)


# ---------------------------------------------------- plant, soil, roots -----
def soil_block(w=3.4, h=1.1):
    base = Rectangle(width=w, height=h)
    paint(base, ["#8D6E63", "#4E342E"], lw=2.2, sheen=0.1, line="#2B1B14")
    grass = Rectangle(width=w, height=0.14)
    grass.set_fill("#558B2F", 1).set_stroke("#33691E", 2)
    grass.move_to([0, h / 2 - 0.07, 0])
    dots = VGroup()
    rng = np.random.RandomState(5)
    for _ in range(26):
        x = rng.uniform(-w / 2 + 0.1, w / 2 - 0.1)
        y = rng.uniform(-h / 2 + 0.08, h / 2 - 0.25)
        dots.add(Dot([x, y, 0], radius=rng.uniform(0.012, 0.032),
                     color=rng.choice(["#A1887F", "#3E2723", "#BCAAA4"])))
    return VGroup(base, grass, dots)


def roots(depth=0.95, spread=0.9):
    g = VGroup()

    def branch(p0, p1, p2, w):
        c = CubicBezier(np.array(p0), np.array(p0) + (np.array(p1) -
                                                     np.array(p0)) * 0.5,
                        np.array(p1), np.array(p2))
        c.set_stroke("#E8D5B0", w)
        return c
    main = branch([0, 0, 0], [0.02, -depth * 0.5, 0], [0, -depth, 0], 5)
    g.add(main)
    for sgn, d, ln in ((-1, 0.25, 0.8), (1, 0.30, 0.9), (-1, 0.55, 0.6),
                       (1, 0.62, 0.65)):
        p0 = [0, -depth * d, 0]
        p1 = [sgn * spread * ln * 0.55, -depth * d - 0.10, 0]
        p2 = [sgn * spread * ln, -depth * d - 0.34, 0]
        g.add(branch(p0, p1, p2, 3.2))
        # root hairs
        for k in range(3):
            tpos = np.array(p0) + (np.array(p2) - np.array(p0)) * (0.35 +
                                                                  0.2 * k)
            g.add(Line(tpos, tpos + [0.08 * sgn, -0.10, 0],
                       stroke_color="#F5E6C8", stroke_width=1.4))
    return g


def plant(h=3.2, leaves_n=5, with_soil=True, soil_w=3.2):
    """A whole plant, ground line at y = 0, roots in a soil cut-away.
    Returns a VGroup with .soil, .stem, .leaves, .top (the leaf crown centre)
    and .ground_y."""
    stem_pts_l, stem_pts_r = [], []
    for t in np.linspace(0, 1, 18):
        x = 0.07 * np.sin(t * 3.2)
        w = 0.085 * (1 - 0.55 * t)
        y = t * h * 0.78
        stem_pts_l.append([x - w, y, 0])
        stem_pts_r.append([x + w, y, 0])
    stem = Polygon(*(stem_pts_l + stem_pts_r[::-1]))
    paint(stem, ["#2E7D32", "#7CB342"], lw=2.0, sheen=0.3, line="#1B3D1F")
    ls = VGroup()
    specs = [(0.30, 1, 28, 1.25), (0.40, -1, 152, 1.25), (0.57, 1, 38, 1.15),
             (0.66, -1, 142, 1.15), (0.80, 1, 55, 0.95), (0.88, -1, 125, 0.95)]
    for (t, sgn, ang, sc) in specs[:leaves_n + 1]:
        lf = leaf(L=1.15 * sc, W=0.55 * sc, curve=0.12)
        if sgn < 0:
            lf.flip(UP, about_point=ORIGIN)
            lf.rotate((ang - 180) * DEGREES, about_point=ORIGIN)
        else:
            lf.rotate(ang * DEGREES, about_point=ORIGIN)
        lf.shift([0.07 * np.sin(t * 1.0 * 3.2), t * h * 0.78, 0])
        ls.add(lf)
    # crown leaf at the very top
    crown = leaf(L=1.0, W=0.5, curve=0.15).rotate(80 * DEGREES,
                                                  about_point=ORIGIN)
    crown.shift([0.07 * np.sin(3.2), h * 0.78, 0])
    ls.add(crown)
    g = VGroup()
    if with_soil:
        soil = soil_block(soil_w, 1.15).move_to([0, -0.575, 0])
        rt = roots(0.95, 0.9).move_to([0, -0.55 - 0.0, 0], aligned_edge=UP)
        rt.align_to(np.array([0, -0.02, 0]), UP)
        g.add(soil, rt)
        g.soil = soil
        g.roots = rt
    g.add(stem, ls)
    g.stem, g.leaves = stem, ls
    g.ground_y = 0.0
    g.crown = np.array([0.07 * np.sin(3.2), h * 0.78, 0])
    return g


# --------------------------------------------------------- waves & arrows ----
def wavy(p0, p1, amp=0.07, waves=6, color="#FFE082", w=4, tip=True):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    v = p1 - p0
    L = np.linalg.norm(v)
    u = v / L
    nrm = np.array([-u[1], u[0], 0])
    f = lambda t: p0 + u * (L * t) + nrm * (amp * np.sin(waves * TAU * t) *
                                           min(1, 6 * t, 6 * (1 - t)))
    pf = ParametricFunction(f, t_range=[0, 1], stroke_color=color,
                            stroke_width=w)
    g = VGroup(pf)
    if tip:
        h = Polygon(p1, p1 - u * 0.2 + nrm * 0.09, p1 - u * 0.2 - nrm * 0.09)
        h.set_fill(color, 1).set_stroke(color, 1)
        g.add(h)
    return g


def arrow(p0, p1, color=CHALK_WHITE, w=6, tip=0.22):
    return Arrow(np.array(p0, float), np.array(p1, float), buff=0,
                 stroke_width=w, tip_length=tip, color=color,
                 max_tip_length_to_length_ratio=0.35)


# ---------------------------------------------------------- cell + organelles
def chloroplast(w=1.5, grana=4):
    """Double membrane, stroma, and stacks of thylakoid discs (grana)."""
    h = w * 0.55
    outer = Ellipse(width=w, height=h)
    paint(outer, "#2E7D32", lw=3.0, sheen=0.25, line="#0F3D12")
    inner = Ellipse(width=w * 0.92, height=h * 0.84)
    paint(inner, "#66BB6A", op=0.95, lw=1.6, sheen=0.3, line="#1B5E20")
    g = VGroup(outer, inner)
    xs = np.linspace(-w * 0.30, w * 0.30, grana)
    for k, x in enumerate(xs):
        y0 = (0.05 if k % 2 else -0.04) * h
        stack = VGroup()
        for j in range(4):
            d = RoundedRectangle(corner_radius=h * 0.03, width=w * 0.15,
                                 height=h * 0.07)
            paint(d, ["#1B5E20", "#43A047"], lw=1.2, sheen=0.3,
                  line="#0A2E0C")
            d.move_to([x, y0 + (j - 1.5) * h * 0.085, 0])
            stack.add(d)
        g.add(stack)
    for a, b in zip(xs[:-1], xs[1:]):
        g.add(Line([a + w * 0.07, 0.0, 0], [b - w * 0.07, 0.0, 0],
                   stroke_color="#1B5E20", stroke_width=1.6,
                   stroke_opacity=0.8))
    return g


def plant_cell(w=3.6, h=2.4, chloros=7, labels=False):
    """A mesophyll cell: cellulose wall, membrane, vacuole, nucleus,
    chloroplasts around the edge."""
    wall = RoundedRectangle(corner_radius=0.30, width=w, height=h)
    paint(wall, "#C5E1A5", op=0.35, lw=7, sheen=0.1, line="#8BC34A")
    mem = RoundedRectangle(corner_radius=0.26, width=w - 0.16, height=h - 0.16)
    mem.set_fill("#A5D6A7", 0.35).set_stroke("#558B2F", 2.2)
    vac = RoundedRectangle(corner_radius=0.35, width=w * 0.42, height=h * 0.46)
    paint(vac, ["#B3E5FC", "#4FC3F7"], op=0.55, lw=2.0, sheen=0.3,
          line="#0288D1")
    vac.move_to([w * 0.05, 0.0, 0])
    nuc = Circle(radius=h * 0.12)
    paint(nuc, ["#B39DDB", "#5E35B1"], lw=2.2, sheen=0.5, line="#311B92")
    nuc.move_to([-w * 0.27, -h * 0.10, 0])
    nl = Circle(radius=h * 0.045, stroke_width=0, fill_color="#311B92",
                fill_opacity=0.9).move_to(nuc.get_center() + UR * 0.03)
    g = VGroup(wall, mem, vac, nuc, nl)
    spots = [(-0.32, 0.30), (-0.05, 0.36), (0.30, 0.32), (0.38, -0.02),
             (0.28, -0.34), (-0.02, -0.36), (-0.34, -0.34)]
    rots = [20, -8, 10, 90, -12, 6, 25]
    cl = VGroup()
    for (sx, sy), rt_ in list(zip(spots, rots))[:chloros]:
        c = chloroplast(w * 0.20, 3)
        c.rotate(rt_ * DEGREES)
        c.move_to([sx * w, sy * h, 0])
        cl.add(c)
    g.add(cl)
    g.chloros = cl
    return g


def person_eating(h=1.9):
    from human_figure import Man
    man = Man(base=[0, -h * 0.5, 0], height=h, facing=RIGHT,
              pose={"r_shoulder": 0.9, "r_elbow": 1.3, "l_shoulder": 0.25,
                    "l_elbow": 0.4, "look": 0.0})
    return man


def plate(w=1.2):
    pl = Ellipse(width=w, height=w * 0.30)
    paint(pl, "#F5F5F5", lw=2.4, sheen=0.3, line="#90A4AE")
    rim = Ellipse(width=w * 0.72, height=w * 0.20)
    rim.set_fill(opacity=0).set_stroke("#CFD8DC", 1.8)
    rice = Ellipse(width=w * 0.32, height=w * 0.18)
    paint(rice, "#FFF8E1", lw=1.4, sheen=0.3, line="#D7CCC8")
    rice.move_to([-w * 0.12, w * 0.07, 0])
    tom = Circle(radius=w * 0.075)
    paint(tom, "#E53935", lw=1.4, sheen=0.5, line="#7F0000")
    tom.move_to([w * 0.14, w * 0.06, 0])
    grn = Ellipse(width=w * 0.2, height=w * 0.09)
    paint(grn, "#7CB342", lw=1.2, sheen=0.3, line="#33691E")
    grn.move_to([w * 0.05, -0.0, 0])
    return VGroup(pl, rim, rice, tom, grn)


def tag_label(text, color=CHALK_WHITE, size=24):
    """A small label pill."""
    t = T(text, size, color)
    box = RoundedRectangle(corner_radius=0.12, width=t.width + 0.34,
                           height=t.height + 0.20, stroke_color=color,
                           stroke_width=2.2, fill_color=PANEL_FILL,
                           fill_opacity=0.85)
    t.move_to(box)
    g = VGroup(box, t)
    g.box = box
    return g


def starch_granule(r=0.30):
    g = VGroup()
    for k in range(5):
        e = Ellipse(width=2 * r * (1 - k * 0.17), height=1.5 * r * (1 - k * 0.17))
        e.set_fill("#FFF3E0" if k % 2 == 0 else "#FFE0B2", 1)
        e.set_stroke("#BCAAA4", 1.4)
        g.add(e)
    g.rotate(-15 * DEGREES)
    return g


def cellulose_wall(w=1.5, h=0.55):
    box = Rectangle(width=w, height=h)
    paint(box, "#C5E1A5", op=0.7, lw=2.4, sheen=0.2, line="#558B2F")
    fibres = VGroup(*[Line([-w / 2 + 0.06, -h / 2 + (k + 0.5) * h / 5, 0],
                           [w / 2 - 0.06, -h / 2 + (k + 0.5) * h / 5 + 0.04, 0],
                           stroke_color="#33691E", stroke_width=2.4)
                      for k in range(5)])
    return VGroup(box, fibres)

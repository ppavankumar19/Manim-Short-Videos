"""Water-transport art for the Class 10 Biology 'water up a tree' video.

Realistic, shaded diagrams built from Manim primitives (same look as
bio_art.py): a eucalyptus, magnified soil with root hairs, a xylem vessel with
a column of linked water molecules, a leaf cross-section with stomata, a cut
stem with a glass tube, a glass with a straw.
"""
from __future__ import annotations

import numpy as np

from bio_art import *  # noqa: F401,F403
from bio_art import paint, shadow, soil_block, glow, OUTLINE
from bio_kit import *  # noqa: F401,F403
from bio_kit import (CHALK_WHITE, CHALK_YELLOW, T, fit, panel)
from manim import (VGroup, Polygon, Circle, Ellipse, Rectangle,
                   RoundedRectangle, Line, Arc, Dot, VMobject, UP, DOWN, LEFT,
                   RIGHT, UL, ORIGIN, PI, TAU, DEGREES)

WATER_BLUE = "#4FC3F7"


# ---------------------------------------------------------------- tree ------
def _lance(L, W, color_a, color_b, ang):
    """A drooping lanceolate leaf hanging from the origin."""
    n = 14
    ts = np.linspace(0, 1, n)
    top = [[L * t, W / 2 * np.sin(np.pi * t ** 0.8) ** 0.9, 0] for t in ts]
    bot = [[L * t, -W / 2 * np.sin(np.pi * t ** 0.8) ** 0.9, 0] for t in ts[::-1]]
    m = VMobject()
    pts = [np.array(p, dtype=float) for p in top + bot[1:-1]]
    m.set_points_smoothly(pts + [pts[0]])
    paint(m, [color_a, color_b], op=0.97, lw=1.0, sheen=0.3, line="#1B5E20")
    m.rotate(ang, about_point=ORIGIN)
    return m


def eucalyptus(h=4.0, soil=False):
    """A tall eucalyptus: slim, swaying trunk with peeling bark, a few limbs and
    a broad crown made of many drooping lance-shaped leaves in clusters.
    Ground line y = 0.  Attributes: .trunk, .crown, .top (point), .H."""
    s = h / 4.0
    H = h * 0.76
    L, R = [], []
    for t in np.linspace(0, 1, 30):
        sway = 0.10 * s * np.sin(t * 3.4)
        flare = 0.05 * s * np.exp(-t * 14)
        w = (0.115 - 0.065 * t) * s + flare
        L.append([sway - w, t * H, 0])
        R.append([sway + w, t * H, 0])
    trunk = Polygon(*(L + R[::-1]))
    paint(trunk, ["#9C8579", "#6D4C41"], lw=2.2, sheen=0.35, line="#3E2723")
    bark = VGroup()
    rng = np.random.RandomState(3)
    for k in range(14):
        t0 = rng.uniform(0.03, 0.9)
        x0 = 0.10 * s * np.sin(t0 * 3.4) + rng.uniform(-0.05, 0.05) * s
        bark.add(Line([x0, t0 * H, 0], [x0 + rng.uniform(-0.01, 0.02),
                                        t0 * H + rng.uniform(0.15, 0.35) * s, 0],
                      stroke_color=rng.choice(["#D7CCC8", "#BCAAA4", "#5D4037"]),
                      stroke_width=1.6, stroke_opacity=0.75))
    top = np.array([0.10 * s * np.sin(3.4), H, 0.0])
    limbs = VGroup()
    tips = []
    for k, (dx, dy) in enumerate(((-0.80, 0.30), (0.78, 0.34), (-0.40, 0.62),
                                  (0.42, 0.66), (0.0, 0.80), (-0.95, 0.05),
                                  (0.95, 0.08))):
        base0 = top + np.array([0, -0.05 * s * (k % 3) - 0.12 * s, 0])
        tip = top + np.array([dx * s * 1.1, dy * s * 1.1, 0])
        limbs.add(Line(base0, tip, stroke_color="#5D4037",
                       stroke_width=3.2 - 0.2 * k))
        tips.append(tip)
    crown = VGroup()
    greens = [("#2E7D32", "#66BB6A"), ("#388E3C", "#81C784"),
              ("#1B5E20", "#4CAF50"), ("#558B2F", "#9CCC65")]
    for k, tp in enumerate(tips):
        for m_ in range(18):
            ang = -PI / 2 + rng.uniform(-1.15, 1.15)
            lf = _lance(rng.uniform(0.34, 0.52) * s, 0.10 * s,
                        *greens[(k + m_) % 4], ang)
            lf.shift(tp + np.array([rng.uniform(-0.26, 0.26) * s,
                                    rng.uniform(-0.04, 0.16) * s, 0]))
            crown.add(lf)
    g = VGroup(limbs, trunk, bark, crown)
    g.trunk, g.crown, g.top, g.H = trunk, crown, top, H
    return g


# ---------------------------------------------------------------- soil ------
def soil_grains(w, h, n=26, seed=2, r=(0.07, 0.15)):
    rng = np.random.RandomState(seed)
    g = VGroup()
    cols = ["#8D6E63", "#795548", "#A1887F", "#6D4C41"]
    for _ in range(n):
        rr = rng.uniform(*r)
        k = rng.randint(5, 8)
        ang = np.sort(rng.uniform(0, TAU, k))
        pts = [[rr * rng.uniform(0.7, 1.15) * np.cos(a),
                rr * rng.uniform(0.7, 1.15) * np.sin(a), 0] for a in ang]
        poly_ = Polygon(*pts)
        poly_.round_corners(rr * 0.45)
        paint(poly_, cols[rng.randint(4)], lw=1.2, sheen=0.12, line="#2B1B14")
        film = poly_.copy().set_fill(opacity=0).set_stroke("#4FC3F7", 2.6,
                                                         opacity=0.55)
        film.scale(1.16)
        poly_ = VGroup(film, poly_)
        poly_.move_to([rng.uniform(-w / 2 + rr, w / 2 - rr),
                       rng.uniform(-h / 2 + rr, h / 2 - rr), 0])
        g.add(poly_)
    return g


def small_drop(r=0.10, color=WATER_BLUE):
    d = Circle(radius=r)
    paint(d, [color, "#0288D1"], lw=1.6, sheen=0.5, line="#01579B")
    hi = Circle(radius=r * 0.28, stroke_width=0, fill_color="#FFFFFF",
                fill_opacity=0.7).move_to([-r * 0.3, r * 0.3, 0])
    return VGroup(d, hi)


def root_hair_view(w=5.2, h=3.0):
    """Magnified soil, root surface at the left (epidermal cells) with root
    hairs reaching between soil grains; water droplets between the grains.
    Attributes: .hairs (each has .tip), .drops, .cells, .bg."""
    g = VGroup()
    bg = RoundedRectangle(corner_radius=0.10, width=w, height=h)
    paint(bg, ["#5D4037", "#3E2723"], op=1, lw=2.2, sheen=0.0, line="#2B1B14")
    g.add(bg)
    grains = soil_grains(w - 1.6, h - 0.3, n=30, seed=4, r=(0.10, 0.22))
    grains.move_to(bg.get_center() + RIGHT * 0.75)
    g.add(grains)
    x0 = -w / 2 + 0.05
    cells = VGroup()
    nrow = 6
    ch = (h - 0.1) / nrow
    for k in range(nrow):
        c = RoundedRectangle(corner_radius=0.06, width=0.95, height=ch - 0.04)
        paint(c, ["#F5E6C8", "#E8D5B0"], lw=2.0, sheen=0.3, line="#8D6E63")
        c.move_to([x0 + 0.475, -h / 2 + 0.05 + (k + 0.5) * ch, 0])
        nuc = Circle(radius=0.07, stroke_width=0, fill_color="#8E24AA",
                     fill_opacity=0.85).move_to(c.get_center() + LEFT * 0.12)
        cells.add(VGroup(c, nuc))
    g.add(cells)
    hairs = []
    lens = [1.55, 1.05, 1.9, 1.25, 1.65, 1.1]
    for k in range(nrow):
        y = -h / 2 + 0.05 + (k + 0.5) * ch
        Ln = lens[k]
        base = np.array([x0 + 0.95, y, 0.0])
        wob = 0.10 * (1 if k % 2 else -1)
        ts = np.linspace(0, 1, 22)
        pts = [base + np.array([Ln * t, wob * np.sin(t * 5.0) +
                                0.03 * t * t * (1 if k % 3 else -1), 0])
               for t in ts]
        up = [p + np.array([0, 0.055 * (1 - 0.5 * t), 0]) for p, t in zip(pts, ts)]
        dn = [p - np.array([0, 0.055 * (1 - 0.5 * t), 0]) for p, t in zip(pts, ts)]
        tube = Polygon(*(up + dn[::-1]))
        paint(tube, ["#FFF3E0", "#FFE0B2"], lw=1.8, sheen=0.3, line="#8D6E63")
        tip = Circle(radius=0.058, stroke_width=1.6, stroke_color="#8D6E63",
                     fill_color="#FFE0B2", fill_opacity=1).move_to(pts[-1])
        hair = VGroup(tube, tip)
        hair.tip = pts[-1]
        hair.root = base
        hairs.append(hair)
        g.add(hair)
    drops = VGroup()
    rng = np.random.RandomState(9)
    for k in range(10):
        p = np.array([rng.uniform(x0 + 1.5, w / 2 - 0.3),
                      rng.uniform(-h / 2 + 0.3, h / 2 - 0.3), 0])
        d = small_drop(0.075)
        d.move_to(p)
        drops.add(d)
    g.add(drops)
    g.hairs, g.drops, g.cells, g.bg = hairs, drops, cells, bg
    return g


# ------------------------------------------------------------- xylem --------
def xylem_tube(h=3.0, w=0.46, rings=True):
    wall = Rectangle(width=w, height=h)
    paint(wall, ["#E3F2FD", "#BBDEFB"], op=0.35, lw=3.2, sheen=0.0,
          line="#1565C0")
    g = VGroup(wall)
    if rings:
        n = int(h / 0.22)
        for k in range(n):
            y = -h / 2 + (k + 0.5) * h / n
            g.add(Line([-w / 2, y, 0], [w / 2, y, 0], stroke_color="#1565C0",
                       stroke_width=2.4, stroke_opacity=0.65))
    g.wall = wall
    return g


def water_column(h=3.0, n=12, linked=True, r=0.085):
    """Continuous column of water molecules joined by links; .mols bottom to
    top."""
    g = VGroup()
    ys = np.linspace(-h / 2 + r * 1.3, h / 2 - r * 1.3, n)
    mols = []
    for y in ys:
        m = Circle(radius=r)
        paint(m, ["#81D4FA", "#0288D1"], lw=1.6, sheen=0.5, line="#01579B")
        m.move_to([0, y, 0])
        mols.append(m)
    links = VGroup()
    if linked:
        for a, b in zip(mols[:-1], mols[1:]):
            links.add(Line(a.get_center(), b.get_center(),
                           stroke_color="#E1F5FE", stroke_width=3.2,
                           stroke_opacity=0.9))
    g.add(links, *mols)
    g.mols, g.links = mols, links
    return g


# -------------------------------------------------------------- leaf --------
def mesophyll_cell(w=0.42, h=0.38, seed=0):
    rng = np.random.RandomState(seed)
    c = Ellipse(width=w, height=h)
    paint(c, ["#A5D6A7", "#43A047"], lw=1.8, sheen=0.3, line="#1B5E20")
    g = VGroup(c)
    for k in range(3):
        a = rng.uniform(0, TAU)
        d = Ellipse(width=w * 0.14, height=h * 0.10, stroke_width=0,
                    fill_color="#1B5E20", fill_opacity=0.9)
        d.move_to([np.cos(a) * w * 0.26, np.sin(a) * h * 0.24, 0])
        g.add(d)
    return g


def leaf_section(w=5.4, h=2.8):
    """Leaf cross-section with generous spacing so nothing overlaps: upper
    epidermis, a palisade row, two loose rows of spongy mesophyll cells with
    air spaces between them, a vein (xylem + phloem) in its own space at the
    left, and a lower epidermis with one stoma.
    Attributes: .xyl, .stoma, .air (points), .cells, .vein, .palisade."""
    g = VGroup()
    bg = Rectangle(width=w, height=h)
    bg.set_fill("#B2DFDB", 0.26).set_stroke(width=0)
    g.add(bg)
    up = Rectangle(width=w, height=0.18)
    paint(up, ["#C5E1A5", "#AED581"], lw=1.8, sheen=0.1, line="#558B2F")
    up.move_to([0, h / 2 - 0.09, 0])
    lo = Rectangle(width=w, height=0.18)
    paint(lo, ["#C5E1A5", "#AED581"], lw=1.8, sheen=0.1, line="#558B2F")
    lo.move_to([0, -h / 2 + 0.09, 0])
    g.add(up)
    # palisade row (elongated cells, chloroplasts along the walls)
    pal = VGroup()
    n = 10
    cw = (w - 0.2) / n
    top_y = h / 2 - 0.18 - 0.04
    for k in range(n):
        c = RoundedRectangle(corner_radius=0.07, width=cw * 0.80, height=0.62)
        paint(c, ["#81C784", "#2E7D32"], lw=1.6, sheen=0.3, line="#1B5E20")
        cx0 = -w / 2 + 0.10 + (k + 0.5) * cw
        c.move_to([cx0, top_y - 0.31, 0])
        pal.add(c)
        for j2, (ox, oy) in enumerate(((-0.07, 0.15), (0.07, 0.02),
                                       (-0.07, -0.12))):
            d = Ellipse(width=0.06, height=0.04, stroke_width=0,
                        fill_color="#0B3D0B", fill_opacity=0.9)
            d.move_to([cx0 + ox, top_y - 0.31 + oy, 0])
            pal.add(d)
    g.add(pal)
    # spongy mesophyll: two loose rows, clear gaps = air spaces
    sp = VGroup()
    cells = []
    row_y = (top_y - 0.62 - 0.30, top_y - 0.62 - 0.88)
    x_start, x_end = -w / 2 + 1.55, w / 2 - 0.45
    for r_, y in enumerate(row_y):
        nn = 6
        for k in range(nn):
            x = x_start + (x_end - x_start) * (k + (0.5 if r_ else 0.0)) / (nn - 0.5)
            c = mesophyll_cell(0.46, 0.40, k + 7 * r_)
            c.move_to([x, y, 0])
            sp.add(c)
            cells.append(c)
    g.add(sp)
    g.add(lo)
    # vein in its own space at the left
    vp = np.array([-w / 2 + 0.78, (row_y[0] + row_y[1]) / 2, 0.0])
    vein = Circle(radius=0.36)
    paint(vein, ["#FFF9C4", "#FFE082"], op=0.92, lw=2.4, sheen=0.2,
          line="#8D6E00")
    vein.move_to(vp)
    xy = Circle(radius=0.17)
    paint(xy, ["#90CAF9", "#1E88E5"], op=1, lw=2.2, sheen=0.4, line="#0D47A1")
    xy.move_to(vp + np.array([-0.07, 0.05, 0]))
    ph = Circle(radius=0.09)
    paint(ph, ["#FFCC80", "#FB8C00"], op=1, lw=1.6, sheen=0.3, line="#E65100")
    ph.move_to(vp + np.array([0.16, -0.13, 0]))
    g.add(vein, xy, ph)
    # stoma
    sx, sy = 0.95, -h / 2 + 0.09
    gcs = VGroup()
    for sgn in (-1, 1):
        e = Ellipse(width=0.26, height=0.18)
        paint(e, ["#66BB6A", "#2E7D32"], lw=1.8, sheen=0.3, line="#1B5E20")
        e.move_to([sx + sgn * 0.14, sy, 0])
        gcs.add(e)
    gap = Rectangle(width=0.06, height=0.20, stroke_width=0,
                    fill_color="#B2DFDB", fill_opacity=1).move_to([sx, sy, 0])
    g.add(gcs, gap)
    ym = (row_y[0] + row_y[1]) / 2
    g.xyl = vp + np.array([-0.07, 0.05, 0])
    g.stoma = np.array([sx, sy, 0.0])
    g.air = [np.array([x_start + 0.45, ym, 0.0]),
             np.array([x_start + 1.55, ym, 0.0]),
             np.array([sx - 0.15, (ym + sy) / 2 - 0.05, 0.0]),
             np.array([sx, sy + 0.25, 0.0])]
    g.cells = cells
    g.vein = vein
    g.palisade = pal
    return g


# ------------------------------------------------------ apparatus ----------
def glass_tube_setup(h=2.2):
    """Cut stem with a vertical glass tube.  .lvl1 / .lvl2 are the water
    column at M1 and M2; markers are drawn."""
    g = VGroup()
    base = RoundedRectangle(corner_radius=0.04, width=0.52, height=0.62)
    paint(base, ["#A1887F", "#6D4C41"], lw=2.4, sheen=0.3, line="#3E2723")
    base.move_to([0, -h / 2 + 0.31, 0])
    cut = Ellipse(width=0.52, height=0.14)
    paint(cut, ["#D7CCC8", "#BCAAA4"], lw=1.6, sheen=0.2, line="#3E2723")
    cut.move_to([0, -h / 2 + 0.62, 0])
    tube = Rectangle(width=0.22, height=h - 0.62)
    tube.set_fill("#E3F2FD", 0.25).set_stroke("#90A4AE", 3)
    tube.move_to([0, -h / 2 + 0.62 + (h - 0.62) / 2, 0])
    y0 = -h / 2 + 0.62
    m1y, m2y = y0 + 0.45, y0 + 1.15
    lvl1 = Rectangle(width=0.16, height=m1y - y0)
    lvl1.set_fill("#29B6F6", 0.9).set_stroke(width=0)
    lvl1.move_to([0, (m1y + y0) / 2, 0])
    lvl2 = Rectangle(width=0.16, height=m2y - y0)
    lvl2.set_fill("#29B6F6", 0.9).set_stroke(width=0)
    lvl2.move_to([0, (m2y + y0) / 2, 0])
    mk = VGroup()
    for y, lab in ((m1y, "M1"), (m2y, "M2")):
        mk.add(Line([0.16, y, 0], [0.40, y, 0], stroke_color=CHALK_YELLOW,
                    stroke_width=3))
        t = T(lab, 22, CHALK_YELLOW)
        t.move_to([0.46 + t.width / 2, y, 0])
        mk.add(t)
    g.add(tube, lvl1, base, cut, mk)
    g.lvl1, g.lvl2, g.m1y, g.m2y, g.y0 = lvl1, lvl2, m1y, m2y, y0
    return g


def straw_glass(h=2.1):
    g = VGroup()
    top_w, bot_w = 1.0, 0.8
    glass = Polygon([-top_w / 2, h / 2 - 0.9, 0], [top_w / 2, h / 2 - 0.9, 0],
                    [bot_w / 2, -h / 2, 0], [-bot_w / 2, -h / 2, 0])
    glass.set_fill("#E1F5FE", 0.18).set_stroke("#B0BEC5", 3.0)
    water = Polygon([-top_w / 2 + 0.05, h / 2 - 1.15, 0],
                    [top_w / 2 - 0.05, h / 2 - 1.15, 0],
                    [bot_w / 2 - 0.03, -h / 2 + 0.03, 0],
                    [-bot_w / 2 + 0.03, -h / 2 + 0.03, 0])
    paint(water, ["#4FC3F7", "#0288D1"], op=0.75, lw=0, sheen=0.3,
          line="#0288D1")
    p0 = [-0.12, -h / 2 + 0.2, 0]
    p1 = [0.30, h / 2 + 0.25, 0]
    straw = Line(p0, p1)
    straw.set_stroke("#EF5350", 11)
    hi = Line(p0, p1)
    hi.set_stroke("#FFCDD2", 4, opacity=0.7)
    fill = Line(p0, p1)
    fill.set_stroke("#29B6F6", 6)
    g.add(water, glass, straw, hi, fill)
    g.straw_top = np.array(p1)
    return g


def vapour_dot(r=0.055):
    d = Circle(radius=r)
    d.set_fill("#E1F5FE", 0.95).set_stroke("#81D4FA", 1.8)
    return d


def soil_with_roots(w=3.0, h=0.9):
    """A soil cut-away with a branching root system, top edge at y = 0."""
    sb = soil_block(w, h).move_to([0, -h / 2, 0])
    rt = roots(h * 0.85, w * 0.33)
    rt.move_to([0, -h * 0.05, 0], aligned_edge=UP)
    g = VGroup(sb, rt)
    g.soil = sb
    return g


def root_cell(w=1.1, h=1.1, seed=0):
    """A root cortex cell: thick wall, membrane, nucleus and a vacuole."""
    wall = RoundedRectangle(corner_radius=0.16, width=w, height=h)
    paint(wall, ["#F5E6C8", "#E8D5B0"], lw=3.4, sheen=0.25, line="#8D6E63")
    mem = RoundedRectangle(corner_radius=0.12, width=w - 0.14, height=h - 0.14)
    mem.set_fill("#FFF8E1", 0.5).set_stroke("#BCAAA4", 1.4)
    vac = RoundedRectangle(corner_radius=0.12, width=w * 0.45, height=h * 0.34)
    paint(vac, ["#E1F5FE", "#81D4FA"], op=0.8, lw=1.4, sheen=0.3,
          line="#0288D1")
    vac.move_to([w * 0.1, -h * 0.12, 0])
    nuc = Circle(radius=h * 0.10)
    paint(nuc, ["#CE93D8", "#7B1FA2"], lw=1.6, sheen=0.5, line="#4A148C")
    nuc.move_to([-w * 0.20, h * 0.22, 0])
    return VGroup(wall, mem, vac, nuc)


# ---------------------------------------------------------------------------
def root_side_view(h=2.5):
    """A root seen from the side: tapering root with a cap, cortex cells, a
    central xylem vessel, and root hairs on both flanks.  Origin at the centre.
    Attributes: .xyl_pos (x), .hair_tips (list of (pos, dir)), .tube."""
    g = VGroup()
    wtop, wbot = 1.0, 0.48
    L, R = [], []
    for t in np.linspace(0, 1, 24):
        y = h / 2 - t * h
        w = (wtop + (wbot - wtop) * t ** 1.3) / 2
        if t > 0.9:
            w *= np.sqrt(max(0.0, 1 - ((t - 0.9) / 0.1) ** 2)) * 0.9 + 0.1
        L.append([-w, y, 0])
        R.append([w, y, 0])
    body = Polygon(*(L + R[::-1]))
    paint(body, ["#F1DDB8", "#D9BE8E"], lw=2.6, sheen=0.3, line="#8D6E63")
    g.add(body)
    # cortex cells
    rng = np.random.RandomState(4)
    cells = VGroup()
    for k in range(9):
        y = h / 2 - 0.22 - k * (h - 0.6) / 8
        wk = (wtop + (wbot - wtop) * ((h / 2 - y) / h) ** 1.3)
        for sx in (-1, 1):
            c = RoundedRectangle(corner_radius=0.05, width=0.2, height=0.2)
            c.set_fill("#FFF8E1", 0.6).set_stroke("#BCAAA4", 1.2)
            c.move_to([sx * (wk / 2 - 0.17), y, 0])
            cells.add(c)
    g.add(cells)
    tube = xylem_tube(h - 0.45, 0.30)
    tube.move_to([0, 0.06, 0])
    g.add(tube)
    # root hairs on both flanks
    tips = []
    hairs = VGroup()
    for k in range(10):
        t = 0.10 + k * 0.075
        y = h / 2 - t * h
        wk = (wtop + (wbot - wtop) * t ** 1.3) / 2
        for sx in (-1, 1):
            ln = 0.50 + 0.22 * rng.rand()
            pts = [np.array([sx * (wk - 0.02 + ln * u),
                             y + 0.10 * np.sin(u * 3) + 0.05 * u * u * (k % 3 - 1),
                             0.0]) for u in np.linspace(0, 1, 10)]
            hm = VMobject()
            hm.set_points_smoothly(pts)
            hm.set_stroke("#FFF3E0", 3.0).set_fill(opacity=0)
            hairs.add(hm)
            tips.append((pts[-1], np.array([-sx, 0.0, 0.0])))
    g.add(hairs)
    g.tube, g.hair_tips, g.body = tube, tips, body
    return g


def pot_apparatus(h=2.6):
    """A potted plant cut off just above the soil, joined by a rubber tube to
    an upright glass tube: the water level rises from M1 to M2.  Attributes:
    .lvl1 (water at M1), .y0 (tube bottom), .m1y, .m2y."""
    g = VGroup()
    pot = Polygon([-0.55, -0.55, 0], [0.55, -0.55, 0], [0.38, -1.30, 0],
                  [-0.38, -1.30, 0])
    paint(pot, ["#D8805A", "#A8512F"], lw=2.6, sheen=0.3, line="#5D2A12")
    rim = RoundedRectangle(corner_radius=0.05, width=1.22, height=0.16)
    paint(rim, ["#E08F68", "#B45C38"], lw=2.4, sheen=0.3, line="#5D2A12")
    rim.move_to([0, -0.50, 0])
    soil = Ellipse(width=1.06, height=0.20)
    paint(soil, ["#6D4C41", "#3E2723"], lw=1.8, sheen=0.1, line="#2B1B14")
    soil.move_to([0, -0.46, 0])
    stem = Rectangle(width=0.15, height=0.62)
    paint(stem, ["#7CB342", "#33691E"], lw=2.0, sheen=0.3, line="#1B3D1F")
    stem.move_to([0, -0.15, 0])
    cut = Ellipse(width=0.15, height=0.06)
    paint(cut, ["#E6EE9C", "#C0CA33"], lw=1.2, sheen=0.1, line="#33691E")
    cut.move_to([0, 0.16, 0])
    rub = RoundedRectangle(corner_radius=0.03, width=0.24, height=0.36)
    paint(rub, ["#78909C", "#37474F"], lw=2.0, sheen=0.3, line="#1C262B")
    rub.move_to([0, 0.28, 0])
    y0 = 0.46
    gl = Rectangle(width=0.20, height=1.30)
    gl.set_fill("#E3F2FD", 0.22).set_stroke("#B0BEC5", 3.0)
    gl.move_to([0, y0 + 0.65, 0])
    m1y, m2y = y0 + 0.42, y0 + 1.04
    lvl1 = Rectangle(width=0.14, height=m1y - y0)
    lvl1.set_fill("#29B6F6", 0.92).set_stroke(width=0)
    lvl1.move_to([0, (m1y + y0) / 2, 0])
    mk = VGroup()
    for yy, lab in ((m1y, "M1"), (m2y, "M2")):
        mk.add(Line([0.13, yy, 0], [0.38, yy, 0], stroke_color=CHALK_YELLOW,
                    stroke_width=3))
        t = T(lab, 22, CHALK_YELLOW)
        t.move_to([0.44 + t.width / 2, yy, 0])
        mk.add(t)
    g.add(pot, soil, rim, stem, cut, rub, gl, lvl1, mk)
    g.lvl1, g.y0, g.m1y, g.m2y = lvl1, y0, m1y, m2y
    return g

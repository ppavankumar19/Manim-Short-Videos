"""Circulation art for the Class 10 Biology red-blood-cell video.

A four-chamber heart (muscle wall, shaded chambers, valve leaflets), the great
vessels as shaded tubes, lungs, an upper-body icon and a body band -- laid out
as ONE fixed circulation map that every scene reuses, so the viewer always
knows where they are.  Plus a persistent red blood cell that changes colour
with its oxygen state, and the two capillary insets (lungs, body tissue).

Colour code (used everywhere): blue = deoxygenated, red = oxygenated.
Heart orientation: patient's right side is on the VIEWER'S LEFT.
"""
from __future__ import annotations

import numpy as np

from bio_art import *  # noqa: F401,F403
from bio_art import paint, shadow, glow, o2, OUTLINE
from bio_kit import *  # noqa: F401,F403
from bio_kit import (CHALK_WHITE, CHALK_YELLOW, CHALK_CYAN, CHALK_PINK, T, fit,
                     panel)
from manim import (VGroup, Polygon, Circle, Ellipse, Rectangle, RoundedRectangle,
                   Line, Arc, Dot, VMobject, UP, DOWN, LEFT, RIGHT, ORIGIN, PI,
                   TAU, DEGREES, UL, MoveAlongPath)

DEOX = "#4A78D0"          # deoxygenated blue
DEOX_L = "#8FB0F0"
OXY = "#E04848"           # oxygenated red
OXY_L = "#F59A9A"
MUSCLE = "#B65A5A"
RBC_DEOX = "#6A55C4"
RBC_OXY = "#E53935"

# ------------------------------------------------------------- the map ------
# Board coordinates of the fixed circulation map.
CH = {                                   # chamber centres and sizes (w, h)
    "RA": ((0.03, -0.07), (0.82, 0.80)),
    "RV": ((0.18, -0.92), (0.92, 1.05)),
    "LA": ((1.08, -0.05), (0.78, 0.76)),
    "LV": ((0.95, -0.95), (0.95, 1.15)),
}
LUNGS_C = np.array([1.05, 1.68, 0.0])
BODY_Y = -2.35
UPPER_C = np.array([-3.05, 1.55, 0.0])

PATHS = {                                # RBC / vessel centre lines
    "SVC": [(-2.75, 1.50), (-1.9, 1.55), (-1.1, 1.25), (-0.70, 0.75),
            (-0.30, 0.22)],
    "IVC": [(-2.15, -2.18), (-1.45, -2.05), (-0.95, -1.35), (-0.78, -0.60),
            (-0.42, -0.18), (-0.20, -0.12)],
    "PA": [(0.56, -0.62), (0.56, 0.05), (0.56, 0.78), (0.35, 1.12),
           (0.28, 1.34)],
    "PV": [(1.85, 1.34), (1.85, 0.78), (1.50, 0.40)],
    "AORTA": [(1.36, -0.88), (1.92, -0.88), (2.20, -1.20), (2.22, -1.70),
              (2.22, -2.18)],
}


def A(pt):
    return np.array([pt[0], pt[1], 0.0])


def path_vm(points):
    """An invisible smooth path through board points (for MoveAlongPath)."""
    m = VMobject()
    m.set_points_smoothly([A(p) for p in points])
    m.set_stroke(opacity=0).set_fill(opacity=0)
    return m


def tube(points, color, w=12, light=None):
    """A shaded vessel: dark outline, body colour, soft highlight."""
    outline = path_vm(points).set_stroke(OUTLINE, w + 6, opacity=1)
    body = path_vm(points).set_stroke(color, w, opacity=1)
    hi = path_vm(points).set_stroke(light or "#FFFFFF", max(w * 0.22, 2),
                                    opacity=0.35)
    g = VGroup(outline, body, hi)
    g.body = body
    return g


def chevrons(points, color="#FFFFFF", n=3, size=0.075):
    """Little arrow tips along a path, showing the direction of flow."""
    pm = path_vm(points)
    g = VGroup()
    for k in range(n):
        a = (k + 0.5) / n
        p = pm.point_from_proportion(a)
        q = pm.point_from_proportion(min(a + 0.02, 1.0))
        d = q - p
        d = d / (np.linalg.norm(d) + 1e-9)
        nrm = np.array([-d[1], d[0], 0.0])
        tip = p + d * size
        t = Polygon(tip, p - d * size + nrm * size * 0.9,
                    p - d * size - nrm * size * 0.9)
        t.set_fill(color, 0.95).set_stroke(width=0)
        g.add(t)
    return g


# --------------------------------------------------------------- heart ------
def _blob(points, fill_a, fill_b, thick):
    m = VMobject()
    pts = [A(p) for p in points]
    m.set_points_smoothly(pts + [pts[0]])
    paint(m, [fill_a, fill_b], op=1, lw=3.4 if thick else 2.4, sheen=0.35,
          line="#4A1010" if thick else "#5A2020")
    return m


def _atrium(key, fill_a, fill_b):
    (cx, cy), (w, h) = CH[key]
    c = RoundedRectangle(corner_radius=min(w, h) * 0.38, width=w, height=h)
    paint(c, [fill_a, fill_b], op=1, lw=2.4, sheen=0.35, line="#5A2020")
    c.move_to([cx, cy, 0])
    return c


RV_PTS = [(-0.28, -0.52), (0.18, -0.40), (0.62, -0.50), (0.66, -1.05),
          (0.42, -1.45), (0.02, -1.35), (-0.28, -0.98)]
LV_PTS = [(0.50, -0.50), (0.95, -0.38), (1.42, -0.52), (1.47, -1.05),
          (1.20, -1.52), (0.92, -1.70), (0.64, -1.25)]


def heart_body():
    """Muscle wall + the four chambers + septum + coronary vessels + valves
    (closed).  Attributes: .ch (dict of chambers), .tri, .mit, .muscle."""
    pts = [(-0.52, 0.02), (-0.42, 0.52), (-0.05, 0.62), (0.30, 0.55),
           (0.56, 0.50), (0.86, 0.55), (1.28, 0.46), (1.60, 0.12),
           (1.70, -0.52), (1.56, -1.15), (1.28, -1.62), (0.98, -1.84),
           (0.60, -1.68), (0.05, -1.46), (-0.38, -1.08), (-0.54, -0.55)]
    m = VMobject()
    m.set_points_smoothly([A(p) for p in pts] + [A(pts[0])])
    paint(m, [MUSCLE, "#8E3C3C"], op=1, lw=3.0, sheen=0.30, line="#3A0C0C")
    g = VGroup(m)
    ch = {
        "RA": _atrium("RA", DEOX_L, DEOX),
        "RV": _blob(RV_PTS, DEOX_L, DEOX, True),
        "LA": _atrium("LA", OXY_L, OXY),
        "LV": _blob(LV_PTS, OXY_L, OXY, True),
    }
    for k in ("RV", "LV", "RA", "LA"):
        g.add(ch[k])
    sept = Line(A((0.56, -0.45)), A((0.56, -1.55)), stroke_color="#4A1010",
                stroke_width=7)
    g.add(sept)
    # coronary vessels on the surface
    for pts_c, col in (([(-0.44, -0.55), (-0.40, -0.95), (-0.18, -1.38)], "#4060C0"),
                       ([(1.52, -0.60), (1.50, -1.00), (1.28, -1.50)], "#D84040"),
                       ([(0.58, 0.46), (0.95, -0.2), (1.20, -0.35)], "#D84040")):
        v = path_vm(pts_c).set_stroke(col, 3.2, opacity=0.9)
        g.add(v)
    tri = valve((0.03, -0.465), 0.62, opened=False)
    mit = valve((1.08, -0.435), 0.58, opened=False)
    g.add(tri, mit)
    g.ch, g.tri, g.mit, g.muscle = ch, tri, mit, m
    return g


def valve(pos, width, opened=False):
    """Two valve leaflets: closed = they meet; open = they swing apart."""
    x, y = pos
    hw = width / 2
    if opened:
        l = Line(A((x - hw, y + 0.02)), A((x - hw * 0.55, y - 0.30)))
        r = Line(A((x + hw, y + 0.02)), A((x + hw * 0.55, y - 0.30)))
    else:
        l = Line(A((x - hw, y + 0.02)), A((x - 0.02, y - 0.12)))
        r = Line(A((x + hw, y + 0.02)), A((x + 0.02, y - 0.12)))
    for ln in (l, r):
        ln.set_stroke("#FFF3E0", 6)
    g = VGroup(l, r)
    g.pos, g.width = (x, y), width
    return g


def map_vessels(show_flow=True):
    """All great vessels (blue = deoxygenated, red = oxygenated)."""
    g = VGroup()
    parts = {}
    for k, col, light in (("SVC", DEOX, DEOX_L), ("IVC", DEOX, DEOX_L),
                          ("PA", DEOX, DEOX_L), ("PV", OXY, OXY_L),
                          ("AORTA", OXY, OXY_L)):
        t = tube(PATHS[k], col, 12, light)
        parts[k] = t
        g.add(t)
        if show_flow:
            g.add(chevrons(PATHS[k], "#FFFFFF", 3))
    g.parts = parts
    return g


# -------------------------------------------------------------- lungs -------
def _lung_shape(pts, sx, sy, shift):
    m = VMobject()
    P_ = [np.array([x * sx + shift[0], y * sy + shift[1], 0.0]) for x, y in pts]
    m.set_points_smoothly(P_ + [P_[0]])
    paint(m, ["#F7B6C6", "#E0829E"], lw=2.8, sheen=0.4, line="#7A2840")
    return m


def lung_pair(w=3.0, h=0.95):
    """Both lungs (the viewer-left one has three lobes, the other two and a
    notch for the heart), a trachea and branching bronchi, fine alveoli."""
    g = VGroup()
    sx, sy = w / 3.0, h / 0.95
    # viewer-left lung (patient's right): three lobes
    left_pts = [(-1.42, 0.0), (-1.28, 0.38), (-0.85, 0.48), (-0.40, 0.42),
                (-0.14, 0.18), (-0.12, -0.12), (-0.30, -0.38), (-0.80, -0.48),
                (-1.22, -0.36)]
    # viewer-right lung (patient's left): two lobes + cardiac notch
    right_pts = [(0.14, 0.18), (0.40, 0.42), (0.85, 0.48), (1.28, 0.38),
                 (1.42, 0.0), (1.22, -0.36), (0.80, -0.48), (0.36, -0.40),
                 (0.20, -0.18), (0.12, -0.02)]
    lu = _lung_shape(left_pts, sx, sy, (0, 0))
    ru = _lung_shape(right_pts, sx, sy, (0, 0))
    g.add(lu, ru)
    fis = VGroup()
    for (a, b) in (((-1.25, 0.12), (-0.28, 0.02)), ((-0.95, -0.40), (-0.28, -0.12)),
                   ((1.30, 0.10), (0.30, 0.02))):
        fis.add(Line([a[0] * sx, a[1] * sy, 0], [b[0] * sx, b[1] * sy, 0],
                     stroke_color="#A04060", stroke_width=2.2, stroke_opacity=0.7))
    g.add(fis)
    br = VGroup()
    tr0 = [0.0, h / 2 + 0.06, 0.0]
    br.add(Line(tr0, [0.0, 0.10 * sy, 0], stroke_color="#FFF3E0", stroke_width=7))
    for sgn in (-1, 1):
        main = [sgn * 0.62 * sx, -0.10 * sy, 0]
        br.add(Line([0, 0.10 * sy, 0], main, stroke_color="#FFF3E0",
                    stroke_width=5))
        for dx, dy, ex, ey in ((0.40, 0.0, 0.85, 0.30), (0.45, -0.05, 0.95, -0.12),
                               (0.35, 0.0, 0.70, -0.32), (0.85, 0.30, 1.15, 0.38),
                               (0.95, -0.12, 1.25, -0.20)):
            x0 = sgn * (0.62 if dx < 0.5 else dx) * sx
            br.add(Line([sgn * dx * sx + (0 if dx > 0.5 else 0.0), dy * sy, 0],
                        [sgn * ex * sx, ey * sy, 0], stroke_color="#FFF3E0",
                        stroke_width=2.6, stroke_opacity=0.85))
    g.add(br)
    rng = np.random.RandomState(5)
    for _ in range(18):
        sgn = rng.choice([-1, 1])
        d = Dot(radius=0.022, color="#FFFFFF")
        d.set_opacity(0.5)
        d.move_to([sgn * rng.uniform(0.35, 1.2) * sx, rng.uniform(-0.3, 0.3) * sy, 0])
        g.add(d)
    return g


def upper_body_icon(h=0.9):
    """Head, neck and shoulders (the upper body)."""
    g = VGroup()
    sh = RoundedRectangle(corner_radius=0.25, width=h * 1.35, height=h * 0.62)
    paint(sh, ["#6FA8FF", "#3466C4"], lw=2.4, sheen=0.3, line="#12306A")
    sh.move_to([0, -h * 0.26, 0])
    nk = Rectangle(width=h * 0.18, height=h * 0.16)
    paint(nk, ["#F1C9A5", "#D9A87F"], lw=1.6, sheen=0.2, line="#6B4A2B")
    nk.move_to([0, h * 0.06, 0])
    hd = Circle(radius=h * 0.30)
    paint(hd, ["#F6D3B3", "#E0AE86"], lw=2.2, sheen=0.4, line="#6B4A2B")
    hd.move_to([0, h * 0.30, 0])
    hr = Arc(radius=h * 0.30, start_angle=0.2, angle=PI - 0.4,
             stroke_color="#2B1B10", stroke_width=9).move_to(
        [0, h * 0.42, 0])
    g.add(sh, nk, hd, hr)
    return g


def body_band(w=5.3, h=0.46):
    b = RoundedRectangle(corner_radius=0.14, width=w, height=h)
    paint(b, ["#8D6A7E", "#5E3F52"], lw=2.6, sheen=0.3, line="#2E1A28")
    g = VGroup(b)
    rng = np.random.RandomState(8)
    for _ in range(18):
        d = Dot(radius=0.03, color="#E8C8D8")
        d.set_opacity(0.5)
        d.move_to(b.get_center() + np.array([rng.uniform(-w / 2 + 0.2, w / 2 - 0.2),
                                             rng.uniform(-h / 2 + 0.08,
                                                         h / 2 - 0.08), 0]))
        g.add(d)
    g.b = b
    return g


# ---------------------------------------------------------------- RBC -------
def rbc(r=0.13, oxy=False, glow_ring=True):
    """A red blood cell: a biconcave disc -- dark thick rim, a lighter ring,
    a darker central dimple and a soft highlight.  Same construction in both
    states so Transform keeps it the same traveller."""
    rim_c = "#9E1F28" if oxy else "#3E3590"
    mid_c = "#E53935" if oxy else "#6A55C4"
    lit_c = "#FF8A80" if oxy else "#A99BEA"
    dip_c = "#7A1218" if oxy else "#2A2468"
    g = VGroup()
    if glow_ring:
        ring = Circle(radius=r * 1.55, stroke_color=CHALK_YELLOW,
                      stroke_width=3.2, stroke_opacity=0.95,
                      fill_color=CHALK_YELLOW, fill_opacity=0.14)
        g.add(ring)
    d = Ellipse(width=r * 2.0, height=r * 1.7)
    paint(d, [lit_c, mid_c], lw=2.0, sheen=0.5, line="#1E0710")
    d.set_fill(rim_c, 1.0)
    d.set_sheen(0.55, UL)
    band = Ellipse(width=r * 1.55, height=r * 1.30)
    band.set_fill(mid_c, 1.0).set_stroke(width=0)
    band.set_sheen(0.45, UL)
    dim = Ellipse(width=r * 0.90, height=r * 0.62)
    dim.set_fill(dip_c, 0.80).set_stroke(width=0)
    hi = Ellipse(width=r * 0.52, height=r * 0.20, stroke_width=0,
                 fill_color="#FFFFFF", fill_opacity=0.55)
    hi.move_to([-r * 0.42, r * 0.46, 0]).rotate(0.35)
    g.add(d, band, dim, hi)
    return g


def plain_rbc(r=0.12, oxy=False):
    return rbc(r, oxy, glow_ring=False)


# -------------------------------------------------------- capillary insets --
def _cap_tube(points, c1, c2, w=14):
    """A capillary whose colour runs from c1 (start) to c2 (end)."""
    n = len(points)
    half = max(2, n // 2)
    a = tube(points[:half + 1], c1, w)
    b = tube(points[half:], c2, w)
    return VGroup(a, b)


def lung_inset(w=3.6, h=2.3):
    """An alveolus (thin air sac) wrapped by a capillary: deoxygenated blood
    arrives (blue end), oxygenated blood leaves (red end).  Attributes:
    .cap_pts (path points), .air (point inside the sac)."""
    g = VGroup()
    sac = Circle(radius=min(w, h) * 0.30)
    paint(sac, ["#FFF1F5", "#F8BBD0"], op=0.92, lw=3.0, sheen=0.3,
          line="#C2185B")
    sac.move_to([0, 0.0, 0])
    g.add(sac)
    for k in range(5):
        a = k * TAU / 5 + 0.3
        bub = Circle(radius=0.20)
        paint(bub, ["#FFF1F5", "#F8BBD0"], op=0.85, lw=2.0, sheen=0.3,
              line="#C2185B")
        bub.move_to(np.array([np.cos(a), np.sin(a), 0]) * (min(w, h) * 0.30 + 0.12))
        g.add(bub)
    R = min(w, h) * 0.30 + 0.22
    pts = [(-w / 2 + 0.10, h * 0.30), (-w * 0.30, h * 0.04), (-R * 0.9, -R * 0.75),
           (0.0, -R - 0.10), (R * 0.9, -R * 0.75), (w * 0.30, h * 0.04),
           (w / 2 - 0.10, h * 0.30)]
    cap = _cap_tube(pts, DEOX, OXY, 15)
    g.add(cap)
    g.cap_pts, g.air = pts, np.array([0.0, 0.0, 0.0])
    g.sac = sac
    g.add(T("ALVEOLUS (AIR SAC)", 18, "#F8BBD0").move_to([0, R + 0.28, 0]))
    return g


def tissue_inset(w=3.6, h=2.3):
    """Body cells around a capillary: oxygenated blood arrives (red end),
    deoxygenated blood leaves (blue end).  .cap_pts, .cells."""
    g = VGroup()
    rng = np.random.RandomState(2)
    cells = []
    for (x, y) in ((-1.1, 0.75), (0.0, 0.85), (1.1, 0.75), (-1.1, -0.85),
                   (0.0, -0.9), (1.1, -0.85)):
        c = RoundedRectangle(corner_radius=0.20, width=0.9, height=0.55)
        paint(c, ["#FFD7B5", "#F4A877"], lw=2.2, sheen=0.35, line="#8D4A1F")
        c.move_to([x, y, 0])
        nuc = Circle(radius=0.08)
        paint(nuc, ["#CE93D8", "#7B1FA2"], lw=1.4, sheen=0.4, line="#4A148C")
        nuc.move_to([x + 0.12, y + 0.04, 0])
        g.add(c, nuc)
        cells.append(c)
    pts = [(-w / 2 + 0.10, 0.0), (-w * 0.30, 0.05), (-0.55, 0.0), (0.0, -0.02),
           (0.55, 0.0), (w * 0.30, 0.05), (w / 2 - 0.10, 0.0)]
    cap = _cap_tube(pts, OXY, DEOX, 15)
    g.add(cap)
    g.cap_pts, g.cells = pts, cells
    g.add(T("BODY TISSUE CELLS", 18, "#F4A877").move_to([0, -h / 2 - 0.02, 0]))
    return g

"""Realistic thorax map for the red-blood-cell video.

Sources (outside the project, see D:\\Manim-Short-Videos\\manim-resources\\biology\\):
  man_shadow_anatomy.svg  (Mikael Haggstrom, public domain) -- its embedded
      Gray's-Anatomy organ plates were extracted to
      man_shadow_anatomy_parts/part_14_image7849.png  (lungs + heart + great
      vessels, transparent background)
  male_front_3d_shaded.svg (Goran_tek-en, CC BY-SA 4.0) -- the human figure,
      cropped to head and shoulders, shirt added, shading re-created
      (Manim does not render SVG gradients).

Everything is data: the SVG is only parsed, the PNG only displayed.
"""
from __future__ import annotations

import numpy as np

from bio_art import paint, OUTLINE
from bio_kit import *  # noqa: F401,F403
from bio_real_art import RES, SRC, _fill_hex
from manim import (VGroup, VMobject, ImageMobject, SVGMobject, Rectangle,
                   Intersection, Difference, Ellipse, Circle, Line, Dot,
                   Polygon, ManimColor, UP, DOWN, LEFT, RIGHT, ORIGIN)

PLATE = RES / "man_shadow_anatomy_parts" / "part_14_image7849.png"
HEART_PLATE = RES / "man_shadow_anatomy_parts" / "part_16_image3855.png"
ATTR_BODY = "Body: Goran_tek-en, CC BY-SA 4.0"

DEOX = "#3F78E0"
OXY = "#E8333A"

# ---- the plate's anatomy, in the plate's own frame (height 7.6, centre 0,0) --
# (read off a grid overlay of the plate)
PLATE_H = 7.6
PTS = {
    "SVC_TOP": (-1.00, 2.20), "SVC_MID": (-1.05, 1.00), "RA": (-0.95, -0.30),
    "IVC_JOIN": (-1.00, -1.25), "IVC_LOW": (-1.00, -2.55),
    "RV": (0.05, -1.00), "TRUNK": (0.45, 0.30),
    "LA": (1.05, 0.00), "LV": (0.95, -1.25),
    "AO_ROOT": (0.35, 0.45), "AO_ARCH": (0.60, 2.30), "AO_TOP": (0.45, 3.35),
    "LUNG_L": (-2.20, 0.40), "LUNG_R": (2.35, 0.20),
}
PA_PATH = [(0.45, 0.30), (0.70, 0.95), (1.20, 1.35), (1.95, 1.30)]
PV_PATH = [(2.10, 0.55), (1.60, 0.30), (1.05, 0.00)]
SVC_IN = [(-1.00, 2.20), (-1.05, 1.00), (-1.10, 0.05), (-0.95, -0.30)]
IVC_IN = [(-1.00, -2.55), (-1.05, -1.40), (-1.00, -0.60), (-0.95, -0.30)]
RA_RV = [(-0.95, -0.30), (-0.55, -0.75), (0.05, -1.00)]
RV_TRUNK = [(0.05, -1.00), (0.30, -0.35), (0.45, 0.30)]
LA_LV = [(1.05, 0.00), (1.00, -0.60), (0.95, -1.25)]
LV_AORTA = [(0.95, -1.25), (0.70, -0.35), (0.35, 0.45), (0.50, 1.60),
            (0.55, 2.40), (0.45, 3.35)]


class Thorax:
    """Geometry + layers of the map.  `b(p)` converts plate coords -> board."""

    def __init__(self, cx=-0.15, cy=-0.30, height=3.4):
        self.cx, self.cy, self.k = cx, cy, height / PLATE_H
        self.height = height

    def b(self, p):
        return np.array([self.cx + self.k * p[0], self.cy + self.k * p[1], 0.0])

    def bl(self, pts):
        return [self.b(p) for p in pts]

    def plate(self):
        im = ImageMobject(str(PLATE)).set(height=self.height)
        # the bitmap's alpha box is slightly off-centre; centre on (cx, cy)
        im.move_to([self.cx, self.cy, 0.0])
        return im


def path_vm(points):
    m = VMobject()
    m.set_points_smoothly([np.array(p, dtype=float) for p in points])
    m.set_stroke(opacity=0).set_fill(opacity=0)
    return m


def flow(points, color, w=9, op=0.80, outline=True):
    """A translucent vessel drawn over the anatomy plate."""
    g = VGroup()
    if outline:
        g.add(path_vm(points).set_stroke(OUTLINE, w + 4, opacity=0.55))
    g.add(path_vm(points).set_stroke(color, w, opacity=op))
    g.add(path_vm(points).set_stroke("#FFFFFF", max(w * 0.2, 1.6), opacity=0.35))
    return g


def chevrons(points, color="#FFFFFF", n=3, size=0.07):
    pm = path_vm(points)
    g = VGroup()
    for k in range(n):
        a = (k + 0.5) / n
        p = pm.point_from_proportion(a)
        q = pm.point_from_proportion(min(a + 0.02, 1.0))
        d = q - p
        d = d / (np.linalg.norm(d) + 1e-9)
        nr = np.array([-d[1], d[0], 0.0])
        tip = p + d * size
        t = Polygon(tip, p - d * size + nr * size * 0.9,
                    p - d * size - nr * size * 0.9)
        t.set_fill(color, 0.95).set_stroke(width=0)
        g.add(t)
    return g


def upper_body_real(height=1.6, shirt="#3C6EC8"):
    """Head, neck and shoulders of the shaded male figure, in a shirt."""
    m = SVGMobject(str(SRC / "male_front_3d_shaded.svg"))
    m.set(height=8)
    base = max(m.submobjects, key=lambda s: s.width * s.height)
    cut, top = 1.90, 4.05
    keep = []
    for s in m.submobjects:
        if s is base or s.get_fill_opacity() < 0.05:
            continue
        if s.get_bottom()[1] < cut + 0.05:
            continue
        try:
            blk = _fill_hex(s) == "#000000"
        except Exception:
            blk = False
        if blk:
            s.set_fill("#7A4A2E", 0.05).set_stroke(width=0)
        keep.append(s)
    rect = Rectangle(width=6, height=top - cut).move_to(
        [0, (top + cut) / 2, 0]).set_stroke(width=0)
    skin = Intersection(base, rect, fill_color="#DDAA82", fill_opacity=1,
                        stroke_width=0)
    srect = Rectangle(width=6, height=2.62 - cut).move_to(
        [0, (2.62 + cut) / 2, 0]).set_stroke(width=0)
    sh = Intersection(base, srect, fill_color=shirt, fill_opacity=1,
                      stroke_width=0)
    neck = Ellipse(width=1.05, height=0.62).move_to([0, 2.62, 0])
    shirt_m = Difference(sh, neck, fill_color=shirt, fill_opacity=1,
                         stroke_color="#1E3D78", stroke_width=2)
    seam = Line([0, 2.45, 0], [0, cut, 0], stroke_color="#1E3D78",
                stroke_width=2, stroke_opacity=0.6)
    # ---- face: hair, eyes, brows, nose, mouth (head spans x +-0.40, y 2.95-4.0)
    hair_pts = [(-0.43, 3.45), (-0.45, 3.78), (-0.30, 4.04), (0.0, 4.12),
                (0.30, 4.04), (0.45, 3.78), (0.43, 3.45), (0.40, 3.70),
                (0.22, 3.88), (0.0, 3.93), (-0.22, 3.88), (-0.40, 3.70)]
    hair = VMobject()
    hair.set_points_smoothly([np.array([x, y, 0.0]) for x, y in hair_pts]
                             + [np.array([hair_pts[0][0], hair_pts[0][1], 0.0])])
    hair.set_fill("#2A1A10", 1).set_stroke("#120A06", 2)
    hair.set_sheen(0.25, UL)
    face = VGroup()
    for sx in (-1, 1):
        white = Ellipse(width=0.17, height=0.085)
        white.set_fill("#FFFFFF", 1).set_stroke("#4A3020", 1.2)
        white.move_to([sx * 0.14, 3.57, 0])
        iris = Circle(radius=0.036)
        iris.set_fill("#3B2412", 1).set_stroke("#120A06", 1)
        iris.move_to([sx * 0.14, 3.57, 0])
        pup = Dot([sx * 0.14, 3.57, 0], radius=0.014, color="#000000")
        glint = Dot([sx * 0.14 + 0.012, 3.585, 0], radius=0.007, color="#FFFFFF")
        brow = VMobject()
        brow.set_points_smoothly([np.array([sx * 0.07, 3.69, 0]),
                                  np.array([sx * 0.15, 3.725, 0]),
                                  np.array([sx * 0.23, 3.70, 0])])
        brow.set_stroke("#2A1A10", 4).set_fill(opacity=0)
        face.add(white, iris, pup, glint, brow)
    nose = VMobject()
    nose.set_points_smoothly([np.array([0.0, 3.52, 0]), np.array([-0.012, 3.40, 0]),
                              np.array([-0.045, 3.32, 0])])
    nose.set_stroke("#9A6A48", 2.6).set_fill(opacity=0)
    nostrils = VGroup(*[Dot([sx * 0.045, 3.30, 0], radius=0.012, color="#7A4A2E")
                        for sx in (-1, 1)])
    nbase = VMobject()
    nbase.set_points_smoothly([np.array([-0.07, 3.31, 0]),
                               np.array([0.0, 3.285, 0]),
                               np.array([0.07, 3.31, 0])])
    nbase.set_stroke("#9A6A48", 2.2).set_fill(opacity=0)
    mouth = VMobject()
    mouth.set_points_smoothly([np.array([-0.10, 3.17, 0]),
                               np.array([0.0, 3.135, 0]),
                               np.array([0.10, 3.17, 0])])
    mouth.set_stroke("#9A3A32", 3.4).set_fill(opacity=0)
    lip = Line([-0.085, 3.172, 0], [0.085, 3.172, 0], stroke_color="#7A2A24",
               stroke_width=1.6)
    face.add(nose, nostrils, nbase, mouth, lip)
    g = VGroup(skin, shirt_m, seam, face, hair)
    g.set(height=height)
    return g

"""Shared kit for the Class 10 Physics story-mode videos.

It re-uses the series' chalkboard engine (bio_kit: narration bookmarks, sync
log, strict layout audit, tight boxes, burned-caption pipeline) with the plain
full-width board (assets/background.png, no students / teacher), a "Physics"
corner badge, and the optical drawings used in the ray-optics lessons:

  concave_mirror()  silvered, shaded spherical mirror with its hatched back
  candle()          a lit candle (wax, wick, flame, glow) -- the object / image
  ray()             a light ray with direction chevrons
  screen()          a white screen on which a real image is caught
"""
from __future__ import annotations

import math
import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_BIO = _HERE.parent / "Biology - Class 10"
if str(_BIO) not in sys.path:
    sys.path.insert(0, str(_BIO))

# the plain board must be chosen before bio_kit is first imported
os.environ["BIO_BOARD"] = "plain"

from bio_kit import *  # noqa: F401,F403,E402
from bio_art import paint, OUTLINE, arrow  # noqa: F401,E402
from bio_widgets import qa_row  # noqa: F401,E402

assert BOARD_NAME == "plain", "bio_kit was imported before BIO_BOARD was set"

import numpy as np  # noqa: E402
from manim import (VGroup, VMobject, Arc, Line, DashedLine, Polygon, Circle,
                   Ellipse, Rectangle, RoundedRectangle, Dot, PI, UP, DOWN,
                   LEFT, RIGHT, RIGHT as _R)  # noqa: E402


class PhysScene(BioScene):
    """Physics base scene: plain board, 'Physics' badge, medium-large type."""
    BADGE_TEXT = "Physics"
    TEXT_SCALE = 0.92
    TIGHT_BOXES = True
    STRICT_BOXES = True
    AVOID_ART = True


# ------------------------------------------------------- multi-line labels ---
def mlines(txt, col, size):
    """Text (one or several lines, split at newlines), every line centred."""
    parts = txt.split("\n")
    return lines(parts, size, col, buff=0.03) if len(parts) > 1 else \
        T(txt, size, col)


def pchip(txt, col, size, h=None, w=3.5):
    """A panel chip of fixed width `w`; newlines make centred extra lines."""
    lab = mlines(txt, col, size)
    fit(lab, w - 0.3)
    box = panel(w, h or lab.height + 0.34, col, radius=0.14, stroke=2.4)
    lab.move_to(box.get_center())
    c = VGroup(box, lab)
    c.box, c.label = box, lab
    c._tight = True
    return c


def pcard(head, body, col, size=22, head_size=26, w=3.5, pad=0.15, gap=0.06):
    """A panel card of fixed width `w` (never shrunk to its text)."""
    c = tcard(head, body, col, w=w, head_size=head_size, body_size=size,
              pad=pad, gap=gap)
    c._tight = True
    return c


def stack(items, top=2.45, gap=0.18, x=4.69, max_h=5.2):
    """Lay panel items out top-down with a real gap, centred on x."""
    g = VGroup(*items).arrange(DOWN, buff=gap)
    if g.height > max_h:
        g.scale(max_h / g.height)
    g.move_to([x, top - g.height / 2, 0])
    return g


# ------------------------------------------------------------- optics art ---
def concave_mirror(px, ay, R=6.0, half=1.75, s=1):
    """A concave mirror with its pole at (px, ay).  s=1: opens to the right
    (centre of curvature to the right of the pole); s=-1: opens to the left.
    Silvered face, dark edge, glint and hatched back."""
    a = math.asin(half / R)
    cx = px + s * R
    base = PI if s == 1 else 0.0
    kw = dict(radius=R, start_angle=base - a, angle=2 * a,
              arc_center=np.array([cx, ay, 0.0]))
    back = Arc(**kw).set_stroke("#1B1F25", 17)
    back.shift(np.array([-s * 0.075, 0, 0]))
    mid = Arc(**kw).set_stroke("#8FA1B0", 10)
    face = Arc(**kw).set_stroke("#E6EEF4", 4.5)
    gl = dict(kw)
    gl.update(start_angle=base + 0.35 * a * (1 if s == 1 else -1) - 0.08,
              angle=0.16)
    glint = Arc(**gl).set_stroke("#FFFFFF", 3).shift(
        np.array([s * 0.015, 0, 0]))
    hatch = VGroup()
    for t in np.linspace(-0.93 * a, 0.93 * a, 15):
        th = base + t
        p = np.array([cx + R * math.cos(th), ay + R * math.sin(th), 0.0])
        u = np.array([math.cos(th), math.sin(th), 0.0])
        tg = np.array([-math.sin(th), math.cos(th), 0.0])
        q0 = p + u * 0.10
        q1 = q0 + u * 0.17 + tg * 0.13
        hatch.add(Line(q0, q1, stroke_color="#8E99A3", stroke_width=2))
    g = VGroup(hatch, back, mid, face, glint)
    g.R, g.cx = R, cx
    return g


def sag(dy, R=6.0):
    """How far the arc is from its pole plane at height dy."""
    return R - math.sqrt(max(R * R - dy * dy, 0.0))


def candle(h=0.8, op=1.0):
    """A lit candle standing on y=0 (centre x=0), total height ~h."""
    bw, bh = h * 0.30, h * 0.62
    body = RoundedRectangle(corner_radius=bw * 0.16, width=bw, height=bh)
    paint(body, ["#FFF3C4", "#DDBB6A"], op=op, lw=1.6, sheen=0.4,
          line="#7A5A22")
    body.move_to([0, bh / 2, 0])
    wick = Line([0, bh, 0], [0, bh + h * 0.07, 0], stroke_color="#2A1A10",
                stroke_width=2.4)
    y0, hf, w = bh + h * 0.06, h * 0.32, h * 0.26

    def drop(sc, col_a, col_b):
        pts = [(0, y0), (w * 0.52 * sc, y0 + hf * 0.28 * sc),
               (w * 0.30 * sc, y0 + hf * 0.70 * sc), (0, y0 + hf * sc),
               (-w * 0.30 * sc, y0 + hf * 0.70 * sc),
               (-w * 0.52 * sc, y0 + hf * 0.28 * sc), (0, y0)]
        m = VMobject()
        m.set_points_smoothly([np.array([x, y, 0.0]) for x, y in pts])
        m.set_fill(col_a, op).set_stroke(col_b, 1.2, opacity=op)
        m.set_sheen(0.4, UP)
        return m
    outer = drop(1.0, "#FFA726", "#E65100")
    inner = drop(0.55, "#FFF6B8", "#FFE082")
    glow = Circle(radius=h * 0.42, fill_color="#FFC857", fill_opacity=0.22 * op,
                  stroke_width=0).move_to([0, y0 + hf * 0.5, 0])
    return VGroup(glow, body, wick, outer, inner)


def screen(x, y_mid, h=2.1):
    """A white screen (thin board on a foot) standing at x."""
    board = Rectangle(width=0.10, height=h)
    paint(board, ["#FFFFFF", "#DDE3E8"], lw=1.6, sheen=0.2, line="#6C7782")
    board.move_to([x, y_mid, 0])
    foot = Rectangle(width=0.5, height=0.07)
    paint(foot, "#5A6470", lw=1.2, sheen=0, line="#2B3138")
    foot.move_to([x, y_mid - h / 2 - 0.035, 0])
    return VGroup(board, foot)


def ray(points, col, w=3.2, chev=1):
    """A light ray through `points`, with a direction chevron on each leg."""
    pts = [np.array([p[0], p[1], 0.0]) for p in points]
    m = VMobject()
    m.set_points_as_corners(pts)
    m.set_stroke(col, w)
    g = VGroup(m)
    for a, b in zip(pts[:-1], pts[1:]):
        d = b - a
        L = np.linalg.norm(d)
        if L < 0.6:
            continue
        d = d / L
        n = np.array([-d[1], d[0], 0.0])
        for k in range(chev):
            c = a + d * L * (k + 0.5) / chev
            tri = Polygon(c + d * 0.11, c - d * 0.07 + n * 0.08,
                          c - d * 0.07 - n * 0.08)
            tri.set_fill(col, 1).set_stroke(width=0)
            g.add(tri)
    return g


# ---------------------------------------------------- solar-cooker art -------
def parabolic_dish(xp, ay, f, half, theta=0.0):
    """A concave dish (paraboloid, so parallel rays meet exactly at F).  Vertex
    at (xp, ay); it opens to the LEFT (towards the Sun); focal length f.
    `theta` turns the whole dish about its vertex (anticlockwise, radians)."""
    from manim import ParametricFunction
    kw = dict(t_range=[-half, half, 0.02])

    def curve(dx=0.0):
        return ParametricFunction(
            lambda t: np.array([xp + dx - t * t / (4 * f), ay + t, 0.0]), **kw)
    back = curve(0.075).set_stroke("#1B1F25", 17)
    mid = curve(0.0).set_stroke("#8FA1B0", 10)
    face = curve(-0.005).set_stroke("#E6EEF4", 4.5)
    hatch = VGroup()
    for t in np.linspace(-0.93 * half, 0.93 * half, 17):
        p = np.array([xp - t * t / (4 * f), ay + t, 0.0])
        tg = np.array([-t / (2 * f), 1.0, 0.0])
        tg /= np.linalg.norm(tg)
        nrm = np.array([tg[1], -tg[0], 0.0])           # points outwards (right)
        if nrm[0] < 0:
            nrm = -nrm
        q0 = p + nrm * 0.11
        q1 = q0 + nrm * 0.17 + tg * 0.13
        hatch.add(Line(q0, q1, stroke_color="#8E99A3", stroke_width=2))
    g = VGroup(hatch, back, mid, face)
    if theta:
        g.rotate(theta, about_point=np.array([xp, ay, 0.0]))
    return g


def pot(w=0.8, h=0.55):
    """A cooking pot (side view), centred on the origin."""
    body = RoundedRectangle(corner_radius=h * 0.2, width=w, height=h)
    paint(body, ["#7A8591", "#2B3037"], lw=2, sheen=0.45, line="#0F1316")
    rim = Ellipse(width=w * 1.05, height=h * 0.24)
    paint(rim, ["#C3CBD3", "#8E99A3"], lw=1.6, sheen=0.3, line="#0F1316")
    rim.move_to([0, h / 2, 0])
    ins = Ellipse(width=w * 0.92, height=h * 0.16)
    ins.set_fill("#12161A", 1).set_stroke(width=0)
    ins.move_to([0, h / 2, 0])
    hl = VGroup(*[Arc(radius=h * 0.16, start_angle=PI / 2 * (1 if s < 0 else -1) - 0.0,
                      angle=-PI * (1 if s < 0 else -1), stroke_color="#0F1316",
                      stroke_width=5).move_to([s * (w / 2 + 0.04), h * 0.12, 0])
                  for s in (-1, 1)])
    shine = Line([-w * 0.28, -h * 0.30, 0], [-w * 0.28, h * 0.20, 0],
                 stroke_color="#FFFFFF", stroke_width=3, stroke_opacity=0.25)
    return VGroup(hl, body, rim, ins, shine)


def steam(w=0.8, n=3):
    """Soft steam wisps rising above a pot (centred at the pot's top)."""
    g = VGroup()
    for k in range(n):
        x = (k - (n - 1) / 2) * w * 0.28
        m = VMobject()
        m.set_points_smoothly([np.array([x, 0.0, 0.0]),
                               np.array([x + 0.07, 0.14, 0.0]),
                               np.array([x - 0.05, 0.30, 0.0]),
                               np.array([x + 0.06, 0.46, 0.0])])
        m.set_stroke("#FFFFFF", 3, opacity=0.55)
        g.add(m)
    return g


def sun_icon(r=0.42):
    core = Circle(radius=r, fill_color="#FFD54F", fill_opacity=1,
                  stroke_color="#FF9800", stroke_width=3)
    core.set_sheen(0.4, UP)
    halo = Circle(radius=r * 1.7, fill_color="#FFE082", fill_opacity=0.18,
                  stroke_width=0)
    g = VGroup(halo, core)
    for k in range(12):
        a = k * PI / 6
        d = np.array([math.cos(a), math.sin(a), 0.0])
        g.add(Line(d * r * 1.25, d * r * 1.65, stroke_color="#FFD54F",
                   stroke_width=3.5))
    return g


def heat_meter(level, w=3.6, h=0.34, x=0.0, y=0.0):
    """A horizontal heat meter; `level` in 0..1.  Same structure for every
    level so Transform animates the fill."""
    lv = max(0.02, min(level, 1.0))
    col = "#FFD54F" if lv < 0.34 else ("#FF9800" if lv < 0.67 else "#F44336")
    frame = RoundedRectangle(corner_radius=h / 2, width=w, height=h,
                             stroke_color=CHALK_WHITE, stroke_width=2.4,
                             fill_color="#10181F", fill_opacity=0.9)
    fill = RoundedRectangle(corner_radius=h / 2 * 0.8, width=max(w * lv - 0.1, 0.05),
                            height=h - 0.1, stroke_width=0, fill_color=col,
                            fill_opacity=1)
    fill.align_to(frame, LEFT).shift(RIGHT * 0.05)
    g = VGroup(frame, fill)
    g.move_to([x, y, 0])
    return g


def reflect(d, n):
    n = n / np.linalg.norm(n)
    return d - 2 * np.dot(d, n) * n

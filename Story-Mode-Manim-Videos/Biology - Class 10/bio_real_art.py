"""Realistic anatomy from freely licensed SVGs, loaded through Manim.

The SVG files live OUTSIDE the project, in
    D:\\Manim-Short-Videos\\manim-resources\\biology\\
with their sources and licences in that folder's README / sources.json.  They
are untrusted downloads: they were scanned for scripts / handlers / remote
links before use, and Manim only PARSES them (SVGMobject); nothing in them is
ever executed.

  heart_diagram_en.svg   ZooFari, CC BY-SA 3.0   (anatomical heart cut-away)
  alveolus_diagram.svg   LadyofHats, public domain (alveoli + capillary net)

The heart SVG ships with text labels and leader lines baked in; both are
removed here, the black cavities are recoloured (blue = deoxygenated right
side, red = oxygenated left side), and anatomy anchors are exposed so the
red blood cell can be placed in the right chamber.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

from bio_art import paint, OUTLINE
from bio_kit import *  # noqa: F401,F403
from manim import (VGroup, VMobject, SVGMobject, Circle, Line, Dot, ManimColor,
                   UP, DOWN, LEFT, RIGHT, ORIGIN, PI)

RES = Path(r"D:\Manim-Short-Videos\manim-resources\biology")
SRC = RES / "_downloads"

ATTRIBUTION = {
    "heart": "Heart: ZooFari, CC BY-SA 3.0 (Wikimedia Commons)",
    "alveolus": "Alveolus: LadyofHats, public domain (Wikimedia Commons)",
}

# anchors in the SVG's own frame (after set(height=8)); see _anchor_check
ANCHORS = {
    "RA": (-1.15, -0.45), "RV": (0.15, -2.05),
    "LA": (1.80, 0.10), "LV": (2.05, -1.75),
    "TRI": (-0.45, -1.30), "MIT": (2.05, -0.55),
    "SVC_TOP": (-1.00, 2.30), "IVC_BOT": (-0.90, -3.30),
    "AORTA_TOP": (0.55, 3.25), "PA_TIP": (3.00, 1.40),
}


def _fill_hex(m):
    try:
        c = m.get_fill_color()
        return ManimColor(c).to_hex().upper()
    except Exception:
        return "#000000"


def _is_blackish(m):
    if m.get_fill_opacity() < 0.05:
        return False
    h = _fill_hex(m)
    r, g, b = int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)
    return max(r, g, b) < 40


def real_heart(height=3.0):
    """The anatomical heart, cleaned.  Returns a VGroup centred on ORIGIN with
    .anchor(name) -> board point (relative to the group's current position),
    .raw (the unfiltered scale factor) and .scale_k."""
    m = SVGMobject(str(SRC / "heart_diagram_en.svg"))
    m.set(height=8)
    col = [s for s in m.submobjects if s.get_fill_opacity() > 0.05
           and not _is_blackish(s) and s.width * s.height > 0.05]
    x0 = min(s.get_left()[0] for s in col)
    x1 = max(s.get_right()[0] for s in col)
    y0 = min(s.get_bottom()[1] for s in col)
    y1 = max(s.get_top()[1] for s in col)
    keep = []
    for s in m.submobjects:
        cx, cy = s.get_center()[0], s.get_center()[1]
        if not (x0 - 0.10 <= cx <= x1 + 0.10 and y0 - 0.10 <= cy <= y1 + 0.10):
            continue                                  # label text in the margin
        if s.get_fill_opacity() < 0.05:               # leader lines (stroke only)
            continue
        keep.append(s)
    for s in keep:
        if _is_blackish(s):
            cx, cy = s.get_center()[0], s.get_center()[1]
            if cy > 0.75 and cx > 0.5:
                col = "#2F6DC4"                       # pulmonary artery: blue
            elif cx < 0.5:
                col = "#243E85"                       # right heart / venae cavae
            else:
                col = "#9B1C1C"                       # left heart cavity
            s.set_fill(col, 1.0)
    g = VGroup(*keep)
    # invisible anchor markers ride along with every later move / scale
    marks = {}
    for name, (ax, ay) in ANCHORS.items():
        d = Dot([ax, ay, 0.0], radius=0.01)
        d.set_opacity(0)
        marks[name] = d
        g.add(d)
    k = height / (y1 - y0)
    g.shift(-np.array([(x0 + x1) / 2, (y0 + y1) / 2, 0.0]))
    g.scale(k, about_point=ORIGIN)
    g.marks = marks
    g.at = lambda name: marks[name].get_center()
    return g


def alveolus_view(width=4.2):
    """Realistic alveoli with their capillary network (the lung gas-exchange
    picture); the grey backdrop and the leader lines are removed."""
    m = SVGMobject(str(SRC / "alveolus_diagram.svg"))
    keep = []
    for s in m.submobjects:
        if s.get_fill_opacity() < 0.05:
            continue                                  # leader lines / outlines only
        if _fill_hex(s) == "#DBDBDB" and s.width * s.height > 0.4 * m.width * m.height:
            continue                                  # the grey plate
        keep.append(s)
    g = VGroup(*keep)
    g.set(width=width)
    return g

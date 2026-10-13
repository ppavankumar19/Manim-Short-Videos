"""Hand-built art for the two beats the reference clip fills with photography.

The reference cuts to satellite imagery of the Oresund and then to an engraving
of Uraniborg.  Neither is in this repo, so both are drawn here from primitives:
a stylised strait with Ven sitting in it, and a line-art observatory in the
manner of a period engraving.  They read as the same two shots without
pretending to be the same two pictures.
"""

from __future__ import annotations

import numpy as np
from manim import (
    ORIGIN, UP, DOWN, LEFT, RIGHT, PI,
    Arc, Circle, Line, Polygon, Rectangle, VGroup,
)

SEA = "#12305C"
SEA_DEEP = "#0B1F3D"
LAND = "#2E4A2C"
LAND_HI = "#3E5F36"
LAND_DARK = "#22391F"
LAND_DRY = "#5A6B3A"
SHALLOW = "#1D4A7A"
COAST = "#7B8C6A"
ENGRAVE = "#E8E8E8"


def _rough(points, *, seed: int, jitter: float = 0.16, splits: int = 3):
    """Turn a coarse outline into a ragged coastline.

    Each pass inserts a midpoint on every edge and pushes it sideways, so the
    result keeps the shape it was given but stops reading as a polygon --
    which is all a stylised coast has to do here.
    """
    rng = np.random.default_rng(seed)
    # Outlines are written as flat (x, y) pairs for readability; manim wants
    # 3-vectors, so lift them here rather than at every call site.
    pts = [np.array([p[0], p[1], p[2] if len(p) > 2 else 0.0], float)
           for p in points]
    for level in range(splits):
        amp = jitter / (2 ** level)
        out = []
        for i, a in enumerate(pts):
            b = pts[(i + 1) % len(pts)]
            out.append(a)
            mid = (a + b) / 2
            edge = b - a
            normal = np.array([-edge[1], edge[0], 0.0])
            n = np.linalg.norm(normal)
            if n > 1e-9:
                mid = mid + normal / n * rng.uniform(-amp, amp) * np.linalg.norm(edge)
            out.append(mid)
        pts = out
    return pts


def _landmass(outline, *, seed: int, jitter: float = 0.16,
              tints: int = 5) -> VGroup:
    """A coast, a shallow shelf outside it, and mottled ground inside.

    The tints are re-roughened copies of the same outline, each shrunk and
    nudged, so they stay inside the coast by construction -- scattering
    free-floating blobs over the landmass would spill them into the water.
    """
    rng = np.random.default_rng(seed + 500)
    pts = _rough(outline, seed=seed, jitter=jitter)

    shelf = Polygon(*pts, fill_color=SHALLOW, fill_opacity=1.0, stroke_width=0)
    body = Polygon(*pts, fill_color=LAND, fill_opacity=1.0,
                   stroke_color=COAST, stroke_width=1.2, stroke_opacity=0.45)
    shelf.scale(1.035, about_point=body.get_center())

    ground = VGroup()
    for k in range(tints):
        patch = Polygon(*_rough(outline, seed=seed + 11 * (k + 1),
                                jitter=jitter * 1.4),
                        fill_color=rng.choice([LAND_HI, LAND_DARK, LAND_DRY]),
                        fill_opacity=float(rng.uniform(0.30, 0.60)),
                        stroke_width=0)
        f = float(rng.uniform(0.34, 0.78))
        patch.scale(f, about_point=body.get_center())
        # Only drift by the room the shrink just made, so a patch cannot
        # wander off the land it is meant to be texturing.
        room = (1.0 - f) * np.array([body.width, body.height, 0.0]) / 2
        patch.shift(np.array([rng.uniform(-1, 1) * room[0] * 0.8,
                              rng.uniform(-1, 1) * room[1] * 0.8, 0.0]))
        ground.add(patch)

    return VGroup(shelf, body, ground)


def oresund(width: float = 20.0) -> tuple[VGroup, np.ndarray]:
    """The strait, with Ven in the middle of it.

    Returned as ``(art, ven_centre)`` so the beat can push the camera in on
    the island without hunting for it inside the group.
    """
    sea = Rectangle(width=width * 1.6, height=width * 1.2,
                    fill_color=SEA, fill_opacity=1.0, stroke_width=0)
    deep = Rectangle(width=width * 0.30, height=width * 1.2,
                     fill_color=SEA_DEEP, fill_opacity=0.55, stroke_width=0)

    s = width / 20.0
    # Ven is about a quarter the width of the water it sits in, so the coasts
    # are kept close enough that the island is still an island when the shot
    # lands on it -- and ragged enough that the shot reads as a coastline
    # rather than as two rectangles with a gap.
    west = _landmass([(-1.6, 9.0), (-1.4, 5.2), (-2.1, 2.4), (-1.5, -0.8),
                      (-2.4, -4.0), (-1.8, -7.4), (-2.6, -9.5),
                      (-12.0, -9.5), (-12.0, 9.0)], seed=4, jitter=0.30)
    east = _landmass([(1.5, 9.0), (12.0, 9.0), (12.0, -9.5), (2.9, -9.5),
                      (2.0, -6.2), (2.8, -2.8), (1.7, 0.6), (2.3, 4.4)],
                     seed=9, jitter=0.30)
    inlet = _landmass([(-5.4, 3.2), (-3.6, 2.6), (-3.2, 0.4), (-5.0, -0.6),
                       (-6.4, 1.2)], seed=33, jitter=0.22)
    # Same builder, read as water: the shelf and ground go, the body fills
    # with sea, so an inland fjord gets the coastline treatment for free.
    inlet[0].set_fill(SHALLOW, opacity=1.0)
    inlet[1].set_fill(SEA, opacity=1.0).set_stroke(COAST, opacity=0.35)
    inlet[2].set_opacity(0.0)

    islets = VGroup(*[
        Polygon(*_rough(pts, seed=sd, jitter=0.22, splits=2),
                fill_color=LAND, fill_opacity=1.0, stroke_color=COAST,
                stroke_width=1.0)
        for pts, sd in (
            ([(-0.9, 6.4), (-0.4, 6.7), (-0.2, 6.1), (-0.8, 5.9)], 41),
            ([(0.9, -5.6), (1.4, -5.2), (1.6, -6.0), (1.0, -6.2)], 47),
        )
    ])

    ven_pts = _rough([(0.22, 0.48), (0.48, 0.22), (0.42, -0.26),
                      (0.0, -0.52), (-0.42, -0.22), (-0.45, 0.26)],
                     seed=21, jitter=0.14, splits=3)
    ven = Polygon(*ven_pts, fill_color=LAND, fill_opacity=1.0,
                  stroke_color=COAST, stroke_width=1.2)

    art = VGroup(sea, deep, west, east, inlet, islets, ven)
    art.scale(s, about_point=ORIGIN)
    return art, ven.get_center()


# ------------------------------------------------------------- observatory --
def _hatch(shape, *, n: int, angle: float = -PI / 3,
           color: str = ENGRAVE, opacity: float = 0.35,
           width: float = 1.0) -> VGroup:
    """Parallel rule lines clipped to a box -- the engraver's shading."""
    left, right = shape.get_left()[0], shape.get_right()[0]
    bottom, top = shape.get_bottom()[1], shape.get_top()[1]
    lines = VGroup()
    for k in range(n):
        y = bottom + (top - bottom) * (k + 0.5) / n
        lines.add(Line(np.array([left, y, 0.0]), np.array([right, y, 0.0]),
                       stroke_color=color, stroke_width=width,
                       stroke_opacity=opacity))
    return lines


def _block(cx, cy, w, h, *, hatch: int = 6) -> VGroup:
    body = Rectangle(width=w, height=h, stroke_color=ENGRAVE, stroke_width=1.6,
                     fill_opacity=0.0).move_to(np.array([cx, cy, 0.0]))
    return VGroup(body, _hatch(body, n=hatch, opacity=0.22))


def _windows(cx, cy, w, h, cols, rows) -> VGroup:
    out = VGroup()
    for r in range(rows):
        for c in range(cols):
            x = cx + (c - (cols - 1) / 2) * (w / max(cols, 1))
            y = cy + (r - (rows - 1) / 2) * (h / max(rows, 1))
            pane = Rectangle(width=w * 0.30 / cols * 2, height=h * 0.34 / rows * 2,
                             stroke_color=ENGRAVE, stroke_width=1.2,
                             fill_opacity=0.0).move_to(np.array([x, y, 0.0]))
            out.add(pane, Line(pane.get_top(), pane.get_bottom(),
                               stroke_color=ENGRAVE, stroke_width=0.8,
                               stroke_opacity=0.5))
    return out


def uraniborg() -> VGroup:
    """A line-art observatory: central domed tower over two arched wings.

    Uraniborg's silhouette is the shot, not its detail -- a tall lantern on a
    dome, a square keep under it, and lower wings either side -- so it is drawn
    at that level and shaded with rule hatching to sit in the same register as
    the engraving the reference clip cuts to.
    """
    art = VGroup()

    # wings
    art.add(_block(-3.05, -1.55, 2.5, 2.2, hatch=8))
    art.add(_block(3.05, -1.55, 2.5, 2.2, hatch=8))
    art.add(_windows(-3.05, -1.55, 1.7, 1.5, 2, 2))
    art.add(_windows(3.05, -1.55, 1.7, 1.5, 2, 2))

    # arched roofs over the wings
    for cx in (-3.05, 3.05):
        arch = Arc(radius=1.30, start_angle=0, angle=PI,
                   stroke_color=ENGRAVE, stroke_width=1.6)
        arch.move_to(np.array([cx, -0.45 + 0.0, 0.0]), aligned_edge=DOWN)
        art.add(arch)
        art.add(*[Line(np.array([cx, -0.45, 0.0]),
                       arch.point_from_proportion(t),
                       stroke_color=ENGRAVE, stroke_width=0.8,
                       stroke_opacity=0.30)
                  for t in np.linspace(0.06, 0.94, 9)])

    # the keep
    art.add(_block(0.0, -1.35, 3.4, 2.6, hatch=9))
    art.add(_windows(0.0, -1.35, 2.4, 1.8, 3, 2))
    door = Rectangle(width=0.62, height=1.05, stroke_color=ENGRAVE,
                     stroke_width=1.5, fill_opacity=0.0)
    door.move_to(np.array([0.0, -2.12, 0.0]))
    art.add(door)

    # the tower
    art.add(_block(0.0, 0.85, 1.9, 1.8, hatch=7))
    art.add(_windows(0.0, 0.95, 1.2, 1.0, 2, 1))

    dome = Arc(radius=0.98, start_angle=0, angle=PI, stroke_color=ENGRAVE,
               stroke_width=1.8)
    dome.move_to(np.array([0.0, 1.75, 0.0]), aligned_edge=DOWN)
    art.add(dome)
    art.add(*[Line(np.array([0.0, 1.75, 0.0]), dome.point_from_proportion(t),
                   stroke_color=ENGRAVE, stroke_width=0.9, stroke_opacity=0.38)
              for t in np.linspace(0.04, 0.96, 11)])

    # lantern and finial
    art.add(_block(0.0, 3.02, 0.52, 0.72, hatch=3))
    art.add(Arc(radius=0.30, start_angle=0, angle=PI, stroke_color=ENGRAVE,
                stroke_width=1.4).move_to(np.array([0.0, 3.38, 0.0]),
                                          aligned_edge=DOWN))
    art.add(Line(np.array([0.0, 3.62, 0.0]), np.array([0.0, 4.05, 0.0]),
                 stroke_color=ENGRAVE, stroke_width=1.4))
    art.add(Circle(radius=0.10, stroke_color=ENGRAVE, stroke_width=1.2,
                   fill_opacity=0.0).move_to(np.array([0.0, 4.15, 0.0])))

    # ground line
    art.add(Line(np.array([-5.4, -2.66, 0.0]), np.array([5.4, -2.66, 0.0]),
                 stroke_color=ENGRAVE, stroke_width=1.2, stroke_opacity=0.45))
    return art


# ------------------------------------------------------------------- arrow --
def marker_arrow(start, end, *, bow: float = 2.2, thick: float = 0.30,
                 color: str = "#FFFFFF") -> VGroup:
    """A fat hand-drawn arrow, the outro's "look down here" gesture.

    Built as a filled outline rather than a stroked path so the shaft can
    taper the way a marker stroke does; a uniform-width stroke reads as a
    diagram, not as something somebody drew on top of the frame.
    """
    p0 = np.asarray(start, float)
    p2 = np.asarray(end, float)
    mid = (p0 + p2) / 2
    edge = p2 - p0
    normal = np.array([-edge[1], edge[0], 0.0])
    normal = normal / max(np.linalg.norm(normal), 1e-9)
    p1 = mid + normal * bow

    t = np.linspace(0.0, 1.0, 60)[:, None]
    curve = (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2
    tangent = np.gradient(curve, axis=0)
    tangent /= np.maximum(np.linalg.norm(tangent, axis=1, keepdims=True), 1e-9)
    norms = np.stack([-tangent[:, 1], tangent[:, 0],
                      np.zeros(len(tangent))], axis=1)

    # Fat at the top, tapering into the head, like a felt-tip pulled downward.
    half = thick * (1.0 - 0.55 * t[:, 0]) / 2
    left = curve + norms * half[:, None]
    right = curve - norms * half[:, None]
    shaft = Polygon(*np.vstack([left, right[::-1]]), fill_color=color,
                    fill_opacity=1.0, stroke_width=0)

    # A plain wedge, skewed a little off the shaft's axis: a hand-drawn head
    # is lopsided, but a many-cornered one just reads as a mistake.
    tip = curve[-1] + tangent[-1] * 0.22
    back = tangent[-1]
    side = norms[-1]
    head = Polygon(
        tip,
        tip - back * 1.15 + side * 0.66,
        tip - back * 1.32 - side * 0.58,
        fill_color=color, fill_opacity=1.0, stroke_width=0,
    )
    return VGroup(shaft, head)

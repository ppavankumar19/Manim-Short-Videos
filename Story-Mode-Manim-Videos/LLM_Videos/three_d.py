"""3D rigs for the "high-level 3D diagram" shots.

Why these are built from plain polygons instead of ``Surface``/``Sphere``:
Manim CE's ``ThreeDCamera.get_mobjects_to_display`` sends every mobject whose
``shade_in_3d`` is set into a *depth-sorted group drawn first*, and everything
else into a *z-index group drawn last*.  A ``Surface`` would therefore render
behind the fixed backdrop.  Ordinary ``Rectangle``/``Line``/``Polygon``
mobjects are still perspective-projected by the camera -- they just keep
their ``z_index`` ordering -- so the rigs below are made of those, and depth
ordering is done explicitly by :func:`apply_depth`.

The first version of these rigs was flat: plates and bare rectangles.  This
version is a small production kit instead:

  * ``box3d``   -- a box with six faces, each shaded by a fixed key light,
                   so every object reads as having real thickness;
  * ``glow``    -- layered translucent stroke copies behind a shape;
  * ``floor_reflection`` -- a faded mirror of a rig under the panel line,
                   which is the cheapest high-end depth cue there is;
  * ``apply_depth`` -- z_index from z, so nearer geometry draws last.
"""
from __future__ import annotations

import numpy as np

from manim import (
    DEGREES, DOWN, LEFT, ORIGIN, RIGHT, UP,
    Circle, Dot, Line, Polygon, Rectangle, RoundedRectangle, Text, VGroup,
)

from theme import (
    AMBER, GREEN, INK, MUTED, NEON_BLUE, NEON_CYAN, NEON_MAGENTA,
    NEON_VIOLET, PANEL, PANEL_EDGE, ROSE, mono, pg, token_color,
)

# Key light direction for the fixed shading model (upper-left-front).
_LIGHT = np.array([0.35, 0.55, 0.80])
_LIGHT = _LIGHT / np.linalg.norm(_LIGHT)


# --------------------------------------------------------------- ordering ---
def apply_depth(group: VGroup, *, base: float = -6.0, scale: float = 1.0) -> VGroup:
    """Give every leaf mobject a z_index from its own z position.

    Nearer (larger z) must draw last.  Because all of these mobjects are
    non-``shade_in_3d``, the camera draws them in z_index order -- so this is
    the only depth cue the renderer needs.  ``base`` keeps the whole rig
    below ordinary 2D content at z_index 0 and above the backdrop at -100.
    """
    for m in group.get_family():
        if not m.submobjects:
            m.set_z_index(base + m.get_center()[2] * scale)
    return group


# ------------------------------------------------------------------ kit ----
def glow(mob, *, color: str | None = None, layers: int = 3,
         base_opacity: float = 0.22) -> VGroup:
    """Layered translucent stroke copies of `mob` -- a cheap neon halo.

    Add the returned group to the scene *before* `mob`, and call
    :func:`apply_depth` on the pair so the halo sits behind by z_index.
    """
    c = color or mob.get_stroke_color() or NEON_CYAN
    g = VGroup()
    for k in range(1, layers + 1):
        copy = mob.copy()
        copy.set_stroke(c, width=1.5 + k * 2.4,
                        opacity=base_opacity / (k * 0.75 + 0.25))
        copy.set_fill(opacity=0)
        g.add(copy)
    return g


def _face_brightness(normal: np.ndarray) -> float:
    return float(0.30 + 0.50 * max(0.0, float(np.dot(normal, _LIGHT))))


def box3d(width: float, height: float, depth: float, *,
          color: str = NEON_CYAN, fill_opacity: float = 0.16,
          stroke_width: float = 2.0, corner_radius: float = 0.0) -> VGroup:
    """A six-faced box with per-face shading from the fixed key light.

    The brightest face is always the one pointing at the light, so the box
    reads as a solid even though every face is flat.  Rounded corners are
    only applied to the front face (the only one seen head-on).
    """
    hz = depth / 2.0
    x = width / 2.0
    y = height / 2.0

    def face(pts, normal, *, closed_front=False):
        poly = Polygon(
            *pts, fill_color=color, fill_opacity=fill_opacity * 1.0,
            stroke_color=color, stroke_width=stroke_width,
        )
        bright = _face_brightness(normal)
        poly.set_fill(color, opacity=fill_opacity * (0.35 + 1.55 * bright))
        return poly

    f_pts = [np.array([-x, -y, hz]), np.array([x, -y, hz]),
             np.array([x, y, hz]), np.array([-x, y, hz])]
    b_pts = [np.array([-x, -y, -hz]), np.array([x, -y, -hz]),
             np.array([x, y, -hz]), np.array([-x, y, -hz])]
    front = face(f_pts, np.array([0, 0, 1]))
    back = face([b_pts[3], b_pts[2], b_pts[1], b_pts[0]], np.array([0, 0, -1]))
    top = face([f_pts[3], f_pts[2], b_pts[2], b_pts[3]], np.array([0, 1, 0]))
    bottom = face([f_pts[0], f_pts[1], b_pts[1], b_pts[0]], np.array([0, -1, 0]))
    left = face([f_pts[3], f_pts[0], b_pts[0], b_pts[3]], np.array([-1, 0, 0]))
    right = face([f_pts[1], f_pts[2], b_pts[2], b_pts[1]], np.array([1, 0, 0]))
    g = VGroup(front, back, top, bottom, left, right)
    apply_depth(g, base=-6.0)
    return g


def floor_reflection(mob, *, floor_y: float = -1.72, fade: float = 0.10,
                     z_shift: float = 0.0) -> VGroup:
    """A faded, vertically flipped copy of `mob` below the panel line."""
    r = mob.copy()
    r.stretch(-1, 1, about_point=np.array([0.0, floor_y, 0.0]))
    r.set_opacity(fade)
    if z_shift:
        r.shift(np.array([0.0, 0.0, z_shift]))
    return r


def grid_floor(width: float = 12.0, depth: float = 22.0, *,
               lines: int = 9, color: str = NEON_BLUE,
               opacity: float = 0.28, y: float = -2.3) -> VGroup:
    """A receding floor grid -- the strongest cheap depth cue there is."""
    g = VGroup()
    for i in range(lines + 1):
        x = -width / 2 + width * i / lines
        g.add(Line(np.array([x, y, 0.0]), np.array([x, y, -depth]),
                   stroke_color=color, stroke_width=1.0, stroke_opacity=opacity))
    for j in range(lines + 1):
        z = -depth * j / lines
        g.add(Line(np.array([-width / 2, y, z]), np.array([width / 2, y, z]),
                   stroke_color=color, stroke_width=1.0, stroke_opacity=opacity))
    return g


# ---------------------------------------------------- rig 1: input runway ---
def input_grid_floor(rows: int = 4, cols: int = 6, *, pitch_x: float = 1.55,
                     pitch_z: float = 1.55, y: float = -2.0,
                     color: str = NEON_CYAN, start: int = 0,
                     title: str = "input positions") -> VGroup:
    """The model's real input: a runway of numbered positions receding in depth.

    Scene 01's payoff -- the machine does not want the sentence, it wants
    *positions*.  The cells lie flat in the X-Z plane, so a camera looking
    down at ~35-40 degrees reads them as a runway, and the digits stay
    legible.  Converging side rails turn the array into a runway with a
    vanishing point instead of a floating table of squares.
    """
    g = VGroup()
    z0 = 0.8
    cell_w, cell_h = pitch_x * 0.84, pitch_z * 0.84
    first_row_z = z0
    last_row_z = z0 - (rows - 1) * pitch_z
    half_w = (cols - 1) / 2.0 * pitch_x

    # side rails converging toward the far row -- the runway cue
    for side in (-1, 1):
        g.add(Line(
            np.array([side * (half_w + cell_w * 0.55), y, first_row_z]),
            np.array([side * (half_w * 0.72 + cell_w * 0.55), y, last_row_z]),
            stroke_color=color, stroke_width=1.4, stroke_opacity=0.5,
        ))

    for r in range(rows):
        for c in range(cols):
            x = (c - (cols - 1) / 2.0) * pitch_x
            z = z0 - r * pitch_z
            cell = Rectangle(
                width=cell_w, height=cell_h,
                stroke_color=color, stroke_width=1.3,
                fill_color=color, fill_opacity=0.07,
            ).rotate(90 * DEGREES, axis=RIGHT)
            cell.move_to(np.array([x, y, z]))
            num = mono(str(start + r * cols + c), 22, color)
            num.rotate(90 * DEGREES, axis=RIGHT)
            num.move_to(np.array([x, y, z]))
            # Fade with distance so the runway has a far end.  Note: set
            # fill/stroke separately -- Mobject.set_opacity() would force the
            # fill to fully opaque and the digits would vanish under it.
            fade = 1.0 + 0.62 * (-r / max(rows - 1, 1))
            cell.set_fill(color, opacity=0.07 * fade)
            cell.set_stroke(color, width=1.3, opacity=0.85 * fade)
            num.set_opacity(max(1.0 + 0.60 * (-r / max(rows - 1, 1)), 0.35))
            g.add(cell, num)
    caption = pg(title, 18, MUTED)
    caption.rotate(90 * DEGREES, axis=RIGHT)
    caption.move_to(np.array([0.0, y, z0 + pitch_z * 0.95]))
    g.add(caption)
    apply_depth(g)
    return g


# ------------------------------------------------------- rig 2: console -----
def console_dial(label: str, value: str, *, color: str = NEON_CYAN,
                 radius: float = 0.62, ticks: int = 10,
                 needle_deg: float = -35.0, with_text: bool = True) -> VGroup:
    """One physical control: a ring, tick marks, a needle and a readout.

    ``with_text=False`` drops the in-rig caption.  Three captions this wide,
    projected and overlapping each other in the middle of the plate, is
    illegible; the scene supplies pinned HUD labels instead.
    """
    ring = Circle(radius=radius, stroke_color=color, stroke_width=2.4,
                  fill_color=color, fill_opacity=0.10)
    marks = VGroup()
    for i in range(ticks + 1):
        a = np.pi * (0.15 + 0.70 * i / ticks)
        inner = np.array([np.cos(a), np.sin(a), 0.0]) * (radius * 0.76)
        outer = np.array([np.cos(a), np.sin(a), 0.0]) * (radius * 0.94)
        marks.add(Line(inner, outer, stroke_color=color, stroke_width=1.0,
                       stroke_opacity=0.55))
    a = np.radians(needle_deg)
    needle = Line(ORIGIN, np.array([np.cos(a), np.sin(a), 0.0]) * radius * 0.66,
                  stroke_color=AMBER, stroke_width=3.0)
    hub = Dot(ORIGIN, radius=0.05, color=AMBER)
    g = VGroup(ring, marks, needle, hub)
    if with_text:
        name = pg(label, 17, INK, "BOLD").move_to(
            np.array([0.0, -radius - 0.34, 0.0]))
        read = mono(value, 16, color).move_to(
            np.array([0.0, -radius - 0.62, 0.0]))
        g.add(name, read)
        g.needle, g.readout, g.label = needle, read, name
    return g


def control_console(factors, *, color: str = NEON_BLUE) -> VGroup:
    """The three-stage configuration room from Scene 06.

    A thick tilted plate with three glowing dials, a light strip along the
    top edge, and its own reflection in the floor of the panel.
    """
    plate = box3d(9.2, 2.5, 0.55, color=color, fill_opacity=0.10,
                  stroke_width=2.0)
    strip = Line(np.array([-4.1, 1.05, 0.29]), np.array([4.1, 1.05, 0.29]),
                 stroke_color=NEON_CYAN, stroke_width=2.4)
    strip.set_z_index(-5.7)
    dials = VGroup()
    for i, (name, value) in enumerate(factors):
        dial = console_dial(name, value, with_text=False,
                            color=[NEON_CYAN, NEON_VIOLET, AMBER][i % 3],
                            radius=0.66, needle_deg=[-40, 10, 55][i % 3])
        dial.move_to(np.array([-3.0 + i * 3.0, 0.05, 0.30]))
        halo = glow(dial, layers=2, base_opacity=0.30)
        halo.set_z_index(-6.0)
        dials.add(VGroup(halo, dial))
        dials.add(halo, dial)
    console = VGroup(plate, strip, dials)
    console.rotate(-14 * DEGREES, axis=UP)
    apply_depth(console)
    console.dials = dials
    return console


# ------------------------------------------------------ rig 3: vault wall ---
def vault_drawer(width: float, height: float, depth: float, *,
                 color: str = NEON_CYAN, label: str = "", ident: str = "") -> VGroup:
    """One vocabulary drawer: a shaded box with its token on the front."""
    box = box3d(width, height, depth, color=color, fill_opacity=0.14,
                stroke_width=1.6)
    front_z = depth / 2.0 + 0.01
    tok = mono(label, 20, INK)
    tok.move_to(np.array([-width / 2 + 1.1, 0.0, front_z]))
    idt = mono(ident, 19, NEON_CYAN)
    idt.move_to(np.array([width / 2 - 1.2, 0.0, front_z]))
    g = VGroup(box, tok, idt)
    apply_depth(g)
    return g


def vault_wall(entries, *, rows_visible: int = 7, spacing: float = 0.78,
               width: float = 6.6, color: str = NEON_CYAN) -> VGroup:
    """The searchable vocabulary as a receding wall of solid drawers."""
    g = VGroup()
    for i in range(rows_visible):
        z = -0.6 - i * spacing
        tok, ident = entries[i] if i < len(entries) else ("", "")
        ident_s = str(ident) if ident is not None else "\u2014"
        d = vault_drawer(width, spacing * 0.72, 0.34, color=color,
                         label=tok, ident=ident_s)
        d.move_to(np.array([0.0, 0.0, z]))
        g.add(d)
    apply_depth(g)
    return g


# ------------------------------------------------------- rig 4: lab bench ---
def bench_machine(label: str, method: str, year: str, *,
                  width: float = 3.0, height: float = 1.5,
                  color: str = NEON_CYAN) -> VGroup:
    """One tokenizer machine: a lit box with a name slot and a status light."""
    body = box3d(width, height, 1.0, color=color, fill_opacity=0.13,
                 stroke_width=2.2)
    hz = 0.51
    name = pg(label, 19, INK, "BOLD")
    name.move_to(np.array([0.0, 0.24, hz]))
    sub = pg(f"{method}  {year}", 13, MUTED)
    sub.move_to(np.array([0.0, -0.04, hz]))
    slot = Rectangle(width=width - 0.6, height=height * 0.40,
                     stroke_color=color, stroke_width=1.4,
                     fill_color=color, fill_opacity=0.10)
    slot.move_to(np.array([0.0, -0.55, hz]))
    light = Dot(np.array([width / 2 - 0.22, height / 2 - 0.22, hz]),
                radius=0.06, color=GREEN)
    halo = glow(light, color=GREEN, layers=2, base_opacity=0.5)
    halo.set_z_index(-5.0)
    g = VGroup(body, name, sub, slot, halo, light)
    apply_depth(g, base=-6.0)
    return g


def lab_bench(machines, *, spacing: float = 3.3, width: float = 3.0,
              height: float = 1.5) -> VGroup:
    """Four tokenizer machines standing on a thick, reflecting bench."""
    bench = box3d(spacing * len(machines) + 0.9, 0.24, 2.4,
                  color=NEON_BLUE, fill_opacity=0.16)
    # kept shallow and high: at these camera angles the base is the lowest
    # part of the rig, and a deeper slab projected past the panel's rim
    bench.move_to(np.array([0.0, -0.85, -1.2]))
    bench.rig = "bench"
    rig = VGroup(bench)
    machines_g = VGroup()
    for i, (label, method, year, color) in enumerate(machines):
        x = -spacing * (len(machines) - 1) / 2 + i * spacing
        m = bench_machine(label, method, year, width=width, height=height,
                          color=color)
        m.move_to(np.array([x, -0.2, 0.0]))
        m.rig = "bench"
        rig.add(m)
        machines_g.add(m)
    apply_depth(rig)
    rig.machines = machines_g
    return rig


# ---------------------------------------------------- rig 5: embed slab -----
def embedding_slab(rows: int = 7, cols: int = 8, *, cell: float = 0.30,
                   color: str = NEON_VIOLET) -> VGroup:
    """The embedding table as a thick physical slab of learned rows."""
    cells = VGroup()
    for r in range(rows):
        row = VGroup()
        for c in range(cols):
            row.add(Rectangle(
                width=cell, height=cell,
                fill_color=color, fill_opacity=0.30,
                stroke_color=color, stroke_width=0.8,
            ))
        row.arrange(RIGHT, buff=0.035)
        cells.add(row)
    cells.arrange(DOWN, buff=0.035)
    cells.move_to(ORIGIN)
    slab = box3d(cells.width + 0.26, cells.height + 0.26, 0.5,
                 color=color, fill_opacity=0.08, stroke_width=1.8)
    front_z = 0.26
    cells.shift(np.array([0.0, 0.0, front_z]))
    rig = VGroup(slab, cells)
    apply_depth(rig)
    return rig


def vector_beam(cols: int = 8, *, spread: float = 3.0, max_h: float = 1.15,
                color: str = NEON_VIOLET, seed: int = 0,
                z: float = 0.0) -> VGroup:
    """One vocabulary row pulled forward into a learned vector.

    Bars, not digits.  This is a *learned parameter*: the scene must never
    suggest the integer ID itself carries meaning, so the vector is drawn as
    a shape whose heights are arbitrary learned values.  A faint base line
    ties the bars to their row.
    """
    rng = np.random.default_rng(seed)
    vals = rng.uniform(0.22, 1.0, cols)
    g = VGroup()
    pitch = spread / max(cols - 1, 1)
    base = Line(np.array([-spread / 2, -0.06, z]),
                np.array([spread / 2, -0.06, z]),
                stroke_color=color, stroke_width=1.2, stroke_opacity=0.5)
    g.add(base)
    for c, v in enumerate(vals):
        h = max_h * float(v)
        x = -spread / 2 + pitch * c
        bar = Rectangle(width=pitch * 0.52, height=h,
                        fill_color=color, fill_opacity=0.85, stroke_width=0)
        bar.move_to(np.array([x, h / 2 - 0.06, z]))
        g.add(bar)
    g.vals = vals
    apply_depth(g, base=-4.0)
    return g


def token_tunnel(n: int = 6, *, spacing: float = 2.8,
                 size: tuple[float, float] = (3.6, 1.9),
                 color: str = NEON_CYAN, start_z: float = -0.5) -> VGroup:
    """A corridor of numbered input slots receding into the machine.

    Kept for completeness; Scene 01 now uses :func:`input_grid_floor`.
    """
    frames, rails = VGroup(), VGroup()
    corners = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    chans = []
    for i in range(n):
        z = start_z - i * spacing
        rect = Rectangle(
            width=size[0], height=size[1], stroke_color=color,
            stroke_width=2.2, stroke_opacity=max(0.95 - 0.11 * i, 0.28),
        )
        rect.move_to(np.array([0.0, 0.0, z]))
        frames.add(rect)
        chans.append([np.array([cx * size[0] / 2, cy * size[1] / 2, z])
                      for cx, cy in corners])
    for c in range(4):
        for a, b in zip([row[c] for row in chans], [row[c] for row in chans][1:]):
            rails.add(Line(a, b, stroke_color=color, stroke_width=1.0,
                           stroke_opacity=0.30))
    g = VGroup(frames, rails)
    apply_depth(g)
    return g

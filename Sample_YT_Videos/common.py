"""Shared theme, geometry, narration and captions for the Kepler short.

A landscape (1920x1080, 60 fps) re-creation of the portrait reference clip
`When being beautifully wrong leads to discovery.mp4`, rebuilt entirely in
Manim CE with the project's own voice (en-IN-PrabhatNeural via
`speech_service.get_speech_service`).

Two things drive every scene in this folder:

  * `SPHERE_R` -- Kepler's Mysterium Cosmographicum nesting, at its true
    proportions.  A sphere sits inside an octahedron, a sphere around that,
    an icosahedron around that, and so on out to the cube.  Each solid's
    inradius is the sphere below it and its circumradius is the sphere above,
    so the six sphere radii fall out of the solids' own geometry rather than
    being placed by eye.

  * `Captions` -- the reference clip's karaoke subtitles: two short lines at
    a time, the spoken one amber and the other white.  The switch times come
    from the edge-tts word boundaries of *our* narration, so the captions stay
    in sync even though our voice is not the reference clip's voice.
"""

from __future__ import annotations

import os
import sys

import numpy as np
from manim import (
    ORIGIN, UP, DOWN, LEFT, RIGHT, IN, OUT, UR, UL, DR, DL, PI, TAU, DEGREES,
    Arc, ArcBetweenPoints, Circle, Dot, Line, VGroup, VMobject, Text,
    ImageMobject, Polygon, Annulus, CubicBezier, Rectangle, Ellipse, Square,
    FadeIn, FadeOut, Create, Write, GrowFromCenter, Indicate, Flash,
    LaggedStart, AnimationGroup, Succession, Rotate, Transform,
    ReplacementTransform, MoveAlongPath,
    rate_functions, config, BLACK, WHITE, Group,
)
from manim_voiceover import VoiceoverScene

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from speech_service import get_speech_service  # noqa: E402

# ------------------------------------------------------------------ output --
# Landscape 1080p at 60 fps, as requested -- the reference clip is 720x1280@30.
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60
config.background_color = BLACK

FRAME_W = config.frame_width      # 14.222...
FRAME_H = config.frame_height     # 8.0

HERE = os.path.dirname(os.path.abspath(__file__))
VOICEOVER_CACHE_DIR = os.path.join(HERE, "media", "voiceovers")
KEPLER_IMAGE = os.path.join(HERE, "images.jfif")

# ------------------------------------------------------------------- theme --
INK = "#FFFFFF"
AMBER = "#F5C518"          # the karaoke highlight in the reference clip
DIM = "#8A8A8A"
SHELL = "#B8BDC6"          # the translucent nesting spheres
SOLID_INK = "#F2F4F7"      # platonic-solid wireframe

# Six orbits, innermost first.  Sampled off the reference clip's frames.
PLANETS = [
    ("Mercury", "#C9C6BE"),
    ("Venus", "#5FC7E8"),
    ("Earth", "#3FD3A8"),
    ("Mars", "#F2705B"),
    ("Jupiter", "#F5872E"),
    ("Saturn", "#C4A484"),
]

CAPTION_FONT = "Segoe UI"       # heavy geometric sans, all-caps, like the clip
SERIF_FONT = "Times New Roman"  # the "Kepler" / "Tycho Brahe" plates

CAPTION_SIZE = 40
CAPTION_LINE_BUFF = 0.16
CAPTION_BOTTOM = 0.62           # buff from the bottom edge

END_HOLD = 1.0


# ---------------------------------------------------------------- narration --
# Each beat is a list of caption lines.  The narration handed to edge-tts is
# exactly " ".join(lines), which is what lets `Captions` locate every line's
# character offset and therefore its spoken time.
LINES: dict[str, list[str]] = {
    "kepler": [
        "Kepler wanted to", "prove the most",
        "elegant theory", "in astronomy.",
    ],
    "nesting": [
        "The idea was if you", "imagine a sphere",
        "inscribed in an", "octahedron, and",
        "then you fit the", "smallest possible",
        "sphere around that,", "and then fit the",
        "smallest possible", "icosahedron",
        "around that, then", "layer on another",
        "sphere, and then", "a dodecahedron,",
        "one more sphere,", "then a tetrahedron,",
        "one more sphere,", "a cube, and then",
        "one final sphere.",
    ],
    "ratios": [
        "You get these six", "spheres, and the",
        "ratios between", "the sizes of those",
        "spheres, Kepler", "believed, would",
        "match the ratios of", "the orbits for the",
        "six known planets.",
        "Since these are the", "Platonic solids,",
        "it somehow feels", "like a very natural",
        "or universal", "set of ratios.",
    ],
    "ven": [
        "Eventually, he", "was able to get",
        "his hands on some", "orbital data to",
        "try to confirm", "his theory.",
    ],
    "tycho": [
        "And the way he did", "it was completely",
        "heroic, by the", "way, but that's",
        "beside the point.",
    ],
    "misfit": [
        "And he couldn't get", "the theory to fit.",
        "It was always off", "by a few percent.",
    ],
    "laws": [
        "But, even though", "he started with the",
        "wrong premise, this", "is what led him to",
        "be the first person", "to understand how",
        "planets actually", "move around",
        "the sun, and to", "develop his famous",
        "eponymous laws.",
    ],
}

NARRATION = {beat: " ".join(lines) for beat, lines in LINES.items()}

# edge-tts rate per beat.  The reference clip runs about 3.4 words a second,
# which PrabhatNeural can only match by gabbling, so these sit near the voice's
# natural pace instead.  Every run time in every beat is derived from the
# resulting word boundaries, so slowing the voice slows the animation with it.
BEAT_RATE = {
    "kepler": "+2%", "nesting": "+6%", "ratios": "+6%", "ven": "+4%",
    "tycho": "+4%", "misfit": "+2%", "laws": "+6%",
}


def scene_speech_service(beat: str):
    return get_speech_service(cache_dir=VOICEOVER_CACHE_DIR, rate=BEAT_RATE[beat])


# ----------------------------------------------------------------- captions --
def _pair_up(lines: list[str]) -> list[list[int]]:
    """Group caption lines into the on-screen pairs the reference clip uses.

    Two lines share the screen, but a line that ends a sentence closes its
    group -- which is why "six known planets." and "beside the point." stand
    alone in the clip instead of being carried over into the next sentence.
    """
    groups: list[list[int]] = []
    current: list[int] = []
    for i, line in enumerate(lines):
        current.append(i)
        if len(current) == 2 or line.rstrip().endswith((".", "!", "?")):
            groups.append(current)
            current = []
    if current:
        groups.append(current)
    return groups


class Captions:
    """Two-line karaoke subtitles pinned to the bottom of the frame.

    Every (group, highlighted line) state is built once up front and left in
    the scene at zero opacity; an updater then shows exactly one of them.  That
    keeps the captions running on wall-clock time *alongside* whatever the beat
    is animating, instead of forcing the beat to stop and wait at each line.
    """

    def __init__(self, scene, beat: str):
        self.lines = LINES[beat]
        self.groups = _pair_up(self.lines)
        self.states: list[VGroup] = []
        self.line_of_state: list[int] = []

        for group in self.groups:
            for hot in group:
                block = VGroup(*[
                    Text(self.lines[i].upper(), font=CAPTION_FONT,
                         font_size=CAPTION_SIZE, weight="HEAVY",
                         color=AMBER if i == hot else INK)
                    for i in group
                ])
                block.arrange(DOWN, buff=CAPTION_LINE_BUFF)
                block.to_edge(DOWN, buff=CAPTION_BOTTOM)
                block.set_opacity(0.0)
                self.states.append(block)
                self.line_of_state.append(hot)

        self.holder = VGroup(*self.states)
        self.times: list[float] = []
        self._t = 0.0
        # Pinning to the frame only means anything under a 3D camera; the flat
        # beats (the plates, the outro) are plain scenes and just add them.
        pin = getattr(scene, "add_fixed_in_frame_mobjects", scene.add)
        pin(self.holder)

    def start(self, tracker) -> None:
        """Latch this beat's line-start times off the TTS word boundaries."""
        self.times = _line_times(tracker, self.lines)
        self._t = 0.0
        self.holder.add_updater(self._tick)

    def stop(self) -> None:
        self.holder.remove_updater(self._tick)
        self.holder.set_opacity(0.0)

    def _tick(self, _mob, dt: float) -> None:
        self._t += dt
        active = -1
        for k, line in enumerate(self.line_of_state):
            if self._t >= self.times[line] - 0.03:
                active = k
        for k, state in enumerate(self.states):
            state.set_opacity(1.0 if k == active else 0.0)


def _line_times(tracker, lines: list[str]) -> list[float]:
    """Spoken start time, in seconds, of each caption line.

    edge-tts hands back one boundary per word carrying its offset into the
    narration string and its offset into the audio, so a line's start time is
    the audio offset of the first word at or after that line's character
    position.  Lines are located by scanning forward, never by searching the
    whole string, so a line repeated later in the beat ("one more sphere,")
    still resolves to its own occurrence.
    """
    text = tracker.data["input_text"]
    boundaries = tracker.data.get("word_boundaries") or []

    offsets: list[int] = []
    cursor = 0
    for line in lines:
        idx = text.find(line, cursor)
        if idx == -1:
            idx = cursor
        offsets.append(idx)
        cursor = idx + len(line)

    times: list[float] = []
    for off in offsets:
        chosen = None
        for wb in boundaries:
            if wb["text_offset"] >= off:
                chosen = wb["audio_offset"] / 1e7
                break
        if chosen is None:
            chosen = boundaries[-1]["audio_offset"] / 1e7 if boundaries else 0.0
        times.append(chosen)

    # Word boundaries are per-word, so two lines can land on the same word when
    # a line is a single short word.  Keep the sequence strictly increasing so
    # no caption state is unreachable.
    for i in range(1, len(times)):
        times[i] = max(times[i], times[i - 1] + 0.12)
    return times


# --------------------------------------------------------------- platonics --
PHI = (1.0 + 5.0 ** 0.5) / 2.0


def _cyclic(a, b, c):
    return [np.array([a, b, c], float), np.array([c, a, b], float),
            np.array([b, c, a], float)]


def _tetra_v():
    return [np.array(p, float) for p in
            ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))]


def _cube_v():
    return [np.array((x, y, z), float)
            for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]


def _octa_v():
    return [np.array(p, float) for p in
            ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))]


def _icosa_v():
    out = []
    for s1 in (1, -1):
        for s2 in (1, -1):
            out += _cyclic(0.0, s1 * 1.0, s2 * PHI)
    return out


def _dodeca_v():
    out = _cube_v()
    for s1 in (1, -1):
        for s2 in (1, -1):
            out += _cyclic(0.0, s1 / PHI, s2 * PHI)
    return out


def _normalise(verts):
    """Scale a vertex set to circumradius 1 and list its edges.

    Every platonic solid's edges are exactly its closest vertex pairs, so the
    edge list falls out of the minimum pairwise distance -- no hand-typed
    index tables to get wrong.
    """
    scale = float(np.linalg.norm(verts[0]))
    verts = [v / scale for v in verts]
    n = len(verts)
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    lengths = {p: float(np.linalg.norm(verts[p[0]] - verts[p[1]])) for p in pairs}
    shortest = min(lengths.values())
    edges = [p for p in pairs if lengths[p] - shortest < 1e-6]
    return verts, edges


# circumradius / inradius for each solid -- the factor by which the sphere
# above it is bigger than the sphere below it.
R_OVER_r = {
    "tetrahedron": 3.0,
    "cube": 3.0 ** 0.5,
    "octahedron": 3.0 ** 0.5,
    "dodecahedron": 1.2584085723648188,
    "icosahedron": 1.2584085723648188,
}

PLATONIC = {
    "tetrahedron": _normalise(_tetra_v()),
    "cube": _normalise(_cube_v()),
    "octahedron": _normalise(_octa_v()),
    "dodecahedron": _normalise(_dodeca_v()),
    "icosahedron": _normalise(_icosa_v()),
}

# The nesting, inside out, exactly as the narration walks it.
NEST_ORDER = ["octahedron", "icosahedron", "dodecahedron", "tetrahedron", "cube"]

# Sphere radii in model units, Mercury's sphere at 1.  Each solid's inradius is
# the sphere below it, so the sphere above is R_OVER_r times bigger.
SPHERE_R: list[float] = [1.0]
for _name in NEST_ORDER:
    SPHERE_R.append(SPHERE_R[-1] * R_OVER_r[_name])

# Circumradius of each solid in the nest: it circumscribes the sphere below it.
SOLID_R = {name: SPHERE_R[i + 1] for i, name in enumerate(NEST_ORDER)}

# Resting orientation of each solid, chosen so it reads as a solid rather than
# as a flat outline from the shallow camera angle the clip uses.
SOLID_TILT = {
    "octahedron": (0.0, 0.0),
    "icosahedron": (0.30, 0.55),
    "dodecahedron": (0.42, 0.30),
    "tetrahedron": (0.0, PI / 4),
    "cube": (0.0, 0.22),
}


def wire_solid(name: str, radius: float | None = None, *, color: str = SOLID_INK,
               width: float = 2.0, opacity: float = 1.0) -> VGroup:
    """A platonic solid as crisp 3D line segments, at its nesting circumradius.

    Drawn from `Line`s rather than a `Polyhedron` because cairo shades a
    Surface-backed solid into soft banded quads; flat lines with
    `set_shade_in_3d` project as real vectors and stay razor sharp at any
    camera angle, which is what the reference clip's wireframes look like.
    """
    radius = SOLID_R[name] if radius is None else radius
    verts, edges = PLATONIC[name]
    pts = [v * radius for v in verts]
    group = VGroup(*[
        Line(pts[i], pts[j], stroke_color=color, stroke_width=width,
             stroke_opacity=opacity)
        for i, j in edges
    ])
    group.set_shade_in_3d(True)
    tilt_x, tilt_z = SOLID_TILT.get(name, (0.0, 0.0))
    if tilt_x:
        group.rotate(tilt_x, axis=RIGHT, about_point=ORIGIN)
    if tilt_z:
        group.rotate(tilt_z, axis=OUT, about_point=ORIGIN)
    return group


def solid_icon(name: str, size: float = 0.62, *, color: str = SOLID_INK,
               width: float = 1.6, tilt=(0.42, 0.72, 0.18)) -> VGroup:
    """A flat orthographic wireframe badge of a solid, for the on-deck queue.

    The queue in the reference clip rides along the top of the frame while the
    camera zooms across two orders of magnitude, so these are drawn as real 2D
    mobjects -- the vertices are rotated in space and then flattened here, once
    -- and pinned with `add_fixed_in_frame_mobjects`.  A live 3D solid parked
    up there would shrink to a speck the moment the camera pulled back.
    """
    verts, edges = PLATONIC[name]
    rx, ry, rz = tilt
    cx, sx = np.cos(rx), np.sin(rx)
    cy, sy = np.cos(ry), np.sin(ry)
    cz, sz = np.cos(rz), np.sin(rz)
    mx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]], float)
    my = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]], float)
    mz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]], float)
    rot = mz @ my @ mx

    pts = [rot @ v * size for v in verts]
    flat = [np.array([p[0], p[2], 0.0]) for p in pts]   # orthographic, depth dropped
    return VGroup(*[
        Line(flat[i], flat[j], stroke_color=color, stroke_width=width)
        for i, j in edges
    ])


def queue_rail(solids: list[str], *, y: float = 2.68, size: float = 0.55,
               gap: float = 1.9, x0: float = -4.9) -> tuple[VGroup, VGroup]:
    """The on-deck solids and the amber rail they ride, both fixed in frame.

    Returned as ``(rail, badges)`` so a beat can retire one badge at a time as
    its solid drops into the nest.
    """
    rail = ArcBetweenPoints(
        np.array([-FRAME_W / 2 - 0.4, y - 0.62, 0.0]),
        np.array([FRAME_W / 2 + 0.4, y - 0.40, 0.0]),
        angle=-0.30, color="#F5872E", stroke_width=2.0, fill_opacity=0.0,
    )
    rail.set_fill(opacity=0.0)
    badges = VGroup(*[solid_icon(name, size) for name in solids])
    for k, badge in enumerate(badges):
        badge.move_to(np.array([x0 + k * gap, y, 0.0]))
    return rail, badges


def cue_times(tracker, beat: str, marks: list[int]) -> tuple[float, list[float]]:
    """Turn caption-line indices into a lead-in plus one run_time per step.

    The animation is cut to the words rather than to guessed fractions: step
    *i* runs from the moment line ``marks[i]`` is spoken until line
    ``marks[i+1]`` is, and the last step runs out the remaining audio.  Because
    the times come from the TTS word boundaries, the choreography re-syncs
    itself if the narration or the voice rate ever changes.
    """
    times = _line_times(tracker, LINES[beat])
    starts = [times[m] for m in marks]
    tail = max(float(tracker.duration), starts[-1] + 0.4)
    ends = starts[1:] + [tail]
    return starts[0], [max(0.12, e - s) for s, e in zip(starts, ends)]


SHELL_PEAK = 0.34      # alpha through the middle of one ball
SHELL_RECEDE = 0.45    # how far every ball dims when a bigger one closes over it
SHELL_RIM = 0.20       # stroke opacity of a ball's limb

# The reference clip's camera is all but orthographic.  Manim's default focal
# distance of 20 is shorter than the cube's own circumradius, which bends it
# into a frustum -- a long focal distance flattens that back out and lets a
# cube read as a cube however far the nest has grown.
FOCAL = 220.0
SHELL_BANDS = 30


def shell_sphere(radius: float, *, peak: float = SHELL_PEAK,
                 bands: int = SHELL_BANDS) -> VGroup:
    """One of the six nesting spheres, as a soft translucent ball.

    A sphere's silhouette from any viewpoint is a circle about the line of
    sight, and every shell here is centred on the origin the camera is aimed
    at -- so a stack of flat discs facing the camera projects identically to a
    real sphere, for a fraction of the cost, and without cairo's shaded-quad
    banding.  `Scene.add_fixed_orientation_mobjects` keeps them square to the
    camera as it moves.

    The discs share one small alpha, so the number of them covering a point is
    what sets its density.  Spacing them evenly would make the ball a bright
    core with a nearly clear edge; a real sphere is much flatter, because the
    line of sight at radius fraction ``b`` passes through ``sqrt(1 - b^2)`` of
    its diameter.  Placing the j-th disc at ``sqrt(1 - ((j+1)/bands)^2)`` makes
    the disc count follow exactly that, so the stack composes to
    ``1 - (1 - a)^(bands * sqrt(1 - b^2))`` -- the real profile, with `peak`
    through the middle whatever `bands` is set to.
    """
    alpha = 1.0 - (1.0 - peak) ** (1.0 / bands)
    body = VGroup()
    # Every disc carries the same alpha -- the profile is made by how many of
    # them overlap -- so the whole ball can be dimmed later with one
    # `set_fill(opacity=band_alpha * f)` without disturbing its shape.
    body.band_alpha = alpha
    for j in range(bands):
        f = float(np.sqrt(max(0.0, 1.0 - ((j + 1) / bands) ** 2)))
        if f <= 0.0:
            continue
        body.add(Circle(radius=radius * f, color=SHELL, stroke_width=0,
                        stroke_opacity=0.0, fill_color=SHELL,
                        fill_opacity=alpha))
    # The rim: a sphere's limb is the one place it reads as a surface.
    body.add(Circle(radius=radius, color=SHELL, stroke_color=SHELL,
                    stroke_width=2.0, stroke_opacity=SHELL_RIM, fill_opacity=0.0))
    body.model_radius = radius
    return body


def recede_shell(shell, depth: int):
    """Animation target for a ball pushed behind `depth` bigger ones.

    Every disc in a ball shares one alpha -- the sphere profile comes from how
    many of them overlap -- so scaling that alpha dims the whole ball without
    disturbing its shape.  The limb dims with it, otherwise the buried balls
    survive as a stack of hard concentric rings.
    """
    f = SHELL_RECEDE ** depth
    # `suspend_mobject_updating=False` or the ball stops being resized for the
    # length of the animation and snaps back to its model radius -- see
    # `pin_shell`, and `fade_shell` for the same reason.
    return shell.animate(suspend_mobject_updating=False).set_fill(
        opacity=shell.band_alpha * f).set_stroke(opacity=SHELL_RIM * f)


def fade_shell(shell, *, out: bool = False):
    """Fade a ball in or out without freezing its size.

    Manim suspends a mobject's updaters for the length of an animation, so a
    plain `FadeIn(shell)` leaves `pin_shell`'s resize dormant and the ball
    renders at its raw model radius -- which for Saturn's shell is 14.25 frame
    units, covering the whole frame.
    """
    anim = FadeOut if out else FadeIn
    return anim(shell, suspend_mobject_updating=False)


def settle_shell(shell, depth: int) -> None:
    """`recede_shell` applied at once, for a beat that opens mid-nest."""
    f = SHELL_RECEDE ** depth
    shell.set_fill(opacity=shell.band_alpha * f)
    shell.set_stroke(opacity=SHELL_RIM * f)


def pin_shell(scene, shell) -> None:
    """Draw a ball flat in frame at whatever size the camera implies.

    A sphere centred on the point the camera is aimed at always projects to a
    circle centred on the middle of the screen, so these are drawn in frame
    coordinates and resized to ``radius * zoom`` every frame.

    Manim's own `add_fixed_orientation_mobjects` cannot do this job: for a
    fixed-orientation mobject it returns ``points + (new_center - center)``,
    translating the mobject to the projected centre without ever projecting or
    scaling the points themselves.  That is right for a label, which should
    keep its size, and wrong for a ball -- the cube's sphere has a model radius
    of 14.25, so it covered the entire frame no matter how far the camera
    pulled back.
    """
    radius = shell.model_radius
    parts = shell.family_members_with_points()
    unit = [part.points.copy() / radius for part in parts]

    def _fit(_mob, _dt=0.0):
        size = radius * scene.renderer.camera.get_zoom()
        for part, base in zip(parts, unit):
            part.points = base * size

    scene.add_fixed_in_frame_mobjects(shell)
    shell.add_updater(_fit)
    _fit(shell)
    # An animation would otherwise suspend this updater; `fade_shell` and
    # `recede_shell` opt out of that.
    shell.resume_updating()


# ------------------------------------------------------------------ orbits --
def orbit(radius: float, color: str, *, head: float = 0.0,
          span: float = 1.25 * PI, width: float = 2.4) -> VGroup:
    """One planet's orbit: a faint full ring plus a bright fading trail.

    The reference clip draws each orbit as a comet trail rather than a closed
    curve, so the ring carries the geometry and the trail carries the motion.
    Returned group is ``(ring, trail, planet)``.
    """
    ring = Circle(radius=radius, stroke_color=color, stroke_width=1.1,
                  stroke_opacity=0.20, fill_opacity=0.0)
    trail = Arc(radius=radius, start_angle=head - span, angle=span,
                stroke_color=color, stroke_width=width)
    trail.set_stroke(color=[BLACK, color])
    planet = Dot(radius * np.array([np.cos(head), np.sin(head), 0.0]),
                 color=color, radius=0.045)
    group = VGroup(ring, trail, planet)
    group.set_shade_in_3d(True)
    return group


ORBIT_HEADS = [0.55, 2.10, 3.55, 4.90, 1.35, 5.75]

# Angular speed of each planet, in radians per second of screen time.  Scaled
# off the real orbital periods so the inner planets visibly race the outer
# ones, then floored so Saturn is not simply frozen for the whole minute.
ORBIT_RATE = [0.85, 0.52, 0.42, 0.31, 0.14, 0.09]


def solar_system(count: int = 6, *, radii: list[float] | None = None) -> VGroup:
    """The innermost `count` orbits, at the nesting spheres' radii."""
    radii = SPHERE_R if radii is None else radii
    return VGroup(*[
        orbit(radii[i], PLANETS[i][1], head=ORBIT_HEADS[i],
              width=2.4 if i >= 3 else 2.0)
        for i in range(count)
    ])


def spin_orbits(orbits: VGroup, seconds: float) -> AnimationGroup:
    """Turn every orbit about the sun for `seconds` of screen time."""
    return AnimationGroup(*[
        Rotate(o, ORBIT_RATE[i] * seconds, axis=OUT, about_point=ORIGIN,
               run_time=seconds, rate_func=rate_functions.linear)
        for i, o in enumerate(orbits)
    ])


Z_STARS, Z_SHELL, Z_ORBIT, Z_SOLID, Z_SUN = -20, 0, 5, 10, 30

# How far back a solid drops once a sphere has closed over it.  In the
# reference clip only the outermost solid is drawn at full strength; the ones
# inside survive as a faint web at the centre of the ball, which is what keeps
# a five-deep nest from reading as a tangle of white lines.
BURIED = 0.12


def framing_zoom(radius: float, *, target: float = 2.15) -> float:
    """Camera zoom that puts something of `radius` at a constant screen size.

    The nest spans a factor of fourteen from Mercury's sphere to the cube, so
    a fixed camera would either crop the start or lose the end.  Framing the
    newest thing instead keeps every step of the build the same size on screen
    -- the reason the reference clip stays legible while it pulls back.
    """
    return target / radius


def full_nest(*, newest: str = "cube"):
    """The completed model: six shells, six orbits, five solids.

    Beats 3, 6 and 7 all open on the finished nest, so they rebuild it from
    here rather than each carrying its own copy of the construction.  Solids
    come back already graded -- `newest` at full strength, the rest buried --
    so a beat that opens mid-nest looks like the beat that built it.
    Returns ``(shells, orbits, solids)`` with the solids keyed by name.
    """
    shells = [shell_sphere(r).set_z_index(Z_SHELL) for r in SPHERE_R]
    # Each ball has receded once for every bigger ball that closed over it, so
    # the outermost dominates and the rest survive as a faint core.
    for depth, shell in enumerate(reversed(shells)):
        if depth:
            settle_shell(shell, depth)
    orbits = solar_system().set_z_index(Z_ORBIT)
    solids = {}
    for name in NEST_ORDER:
        solid = wire_solid(name).set_z_index(Z_SOLID)
        if name != newest:
            solid.set_stroke(opacity=BURIED)
        solids[name] = solid
    return shells, orbits, solids


def sun_glow(scale: float = 1.0) -> VGroup:
    """The sun as a screen-space point of light.

    Kept flat and fixed in frame: the camera always looks at the origin, so
    the sun always projects to the centre of the screen, and a real 3D sphere
    here would balloon as the camera zooms in on Mercury's orbit instead of
    staying the pinpoint the clip shows.
    """
    glow = VGroup()
    for r, op, col in ((0.44, 0.05, "#F5B301"), (0.28, 0.09, "#F5B301"),
                       (0.17, 0.18, "#FFD24A"), (0.085, 0.55, "#FFE082"),
                       (0.038, 1.00, "#FFF6D0")):
        glow.add(Circle(radius=r * scale, stroke_width=0,
                        fill_color=col, fill_opacity=op))
    return glow.set_z_index(Z_SUN)


def star_field(n: int = 130, seed: int = 11) -> VGroup:
    """A fixed-in-frame scatter of stars, so the void never reads as flat black."""
    rng = np.random.default_rng(seed)
    stars = VGroup()
    for _ in range(n):
        x = rng.uniform(-FRAME_W / 2, FRAME_W / 2)
        y = rng.uniform(-FRAME_H / 2, FRAME_H / 2)
        stars.add(Dot(np.array([x, y, 0.0]), color=WHITE,
                      radius=float(rng.uniform(0.008, 0.026)))
                  .set_opacity(float(rng.uniform(0.20, 0.95))))
    # The balls are drawn in frame too, so the stars need an explicit z-index
    # to stay behind them rather than relying on insertion order.
    return stars.set_z_index(Z_STARS)


# --------------------------------------------------------------- typography --
def plate(label: str, size: int = 62, color: str = INK) -> Text:
    """A serif name plate -- the clip's "Kepler" and "Tycho Brahe" cards."""
    return Text(label, font=SERIF_FONT, font_size=size, color=color)


def kicker(label: str, size: int = 54, color: str = AMBER) -> Text:
    return Text(label.upper(), font=CAPTION_FONT, font_size=size,
                weight="HEAVY", color=color)

"""A genuinely interactive 3D quadrilateral explorer, built in Manim itself.

WHAT THIS IS, AND WHAT IT IS NOT
--------------------------------
An .mp4 is a strip of frames.  Nothing inside it can respond to a mouse, so
the rendered lesson video (`render_all.py`) can never be dragged, spun or
re-parameterised by the student -- that is a property of the file format, not
of Manim.

But Manim is not only an .mp4 factory.  Its OpenGL renderer can open a live
window instead of writing a file, and that window *does* take mouse and
keyboard events: `Scene.on_mouse_drag`, `Scene.on_mouse_scroll` and
`Scene.set_key_function` are part of the public API.  So the interaction
lives here, in a scene run with `--renderer=opengl`, driven by the exact same
`common.py` geometry the recorded lesson uses.  One source of truth, two
outputs: a video to watch, and a window to play in.

RUN IT
------
    .venv\\Scripts\\manim.exe render --renderer=opengl -p --force_window ^
        --dry_run -qm quadrilateral_scenes\\interactive_quads.py QuadExplorer

`--dry_run` is what stops Manim writing an .mp4; `--force_window` is what
makes it open the live window instead.  Nothing is saved: this scene is the
window, not a file.

CONTROLS
--------
    left-drag        orbit the camera around the shape
    middle-drag      pan
    scroll           zoom
    1 . . 6          square, rectangle, parallelogram, rhombus, trapezium, kite
    n                next shape in the family
    m                show / hide the equal-side and parallel marks
    x                show / hide the two diagonals
    f                fold the shape out of its own plane, one step at a time
    r                reset the camera
    q                quit

Set QUAD_EXPLORER_AUTOQUIT=<seconds> to have the window close itself; that is
for testing the scene, not for using it.

`f` is the point of the whole thing: four bars with fixed lengths do not
determine a shape, and here the student can push it out of the plane and
watch that happen, instead of being told it.
"""
from __future__ import annotations

import numpy as np
from manim import Scene, VGroup, DEGREES, OUT, DOWN

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import (  # noqa: E402  (path juggling has to come first)
    FAMILY_PTS, FAMILY_COLOR, FAMILY_NAME, FAMILY_RULE, FAMILY_ORDER,
    INK, MUTED, ACCENT, AMBER,
    plate, plate_top, ticks, chevrons, corner_mark, diagonals, table_top,
    placard, mtx, txt,
)

LIFT = OUT * 0.02
FOLD_STEPS = [0.0, 0.30, 0.60, 0.95, 0.60, 0.30]     # radians, cycled by `f`


def marks_for(name: str, pts) -> VGroup:
    """The schoolbook notation for whichever shape is on screen.

    Same rules as the recorded lesson: ticks mean equal, chevrons mean
    parallel, a small square means a right angle.
    """
    p = pts
    if name == "square":
        return VGroup(
            *[ticks(p[i], p[(i + 1) % 4], 1, INK) for i in range(4)],
            *[corner_mark(p[i], p[(i - 1) % 4], p[(i + 1) % 4], 0.26, INK)
              for i in range(4)],
        )
    if name == "rectangle":
        return VGroup(
            ticks(p[0], p[1], 1, INK), ticks(p[2], p[3], 1, INK),
            ticks(p[1], p[2], 2, INK), ticks(p[3], p[0], 2, INK),
            *[corner_mark(p[i], p[(i - 1) % 4], p[(i + 1) % 4], 0.26, INK)
              for i in range(4)],
        )
    if name == "parallelogram":
        return VGroup(
            chevrons(p[0], p[1], 1, INK), chevrons(p[3], p[2], 1, INK),
            chevrons(p[1], p[2], 2, INK), chevrons(p[0], p[3], 2, INK),
        )
    if name == "rhombus":
        return VGroup(*[ticks(p[i], p[(i + 1) % 4], 1, INK) for i in range(4)])
    if name == "trapezium":
        return VGroup(chevrons(p[0], p[1], 1, INK), chevrons(p[3], p[2], 1, INK))
    # kite
    return VGroup(
        ticks(p[0], p[1], 1, INK), ticks(p[3], p[0], 1, INK),
        ticks(p[1], p[2], 2, INK), ticks(p[2], p[3], 2, INK),
    )


def folded(pts, angle: float) -> list:
    """Hinge the fourth vertex about the p0-p2 diagonal, lengths preserved.

    Exactly the fold `scene_02_rigid.py` uses, and for the same reason: the
    four side lengths are untouched, so anything that changes is proof that
    four lengths do not fix a quadrilateral.
    """
    p = [np.asarray(q, dtype=float) for q in pts]
    if not angle:
        return p
    axis = p[2] - p[0]
    u = axis / max(float(np.linalg.norm(axis)), 1e-9)
    v = p[3] - p[0]
    v_par = float(np.dot(v, u)) * u
    v_perp = v - v_par
    w = np.cross(u, v_perp)
    p[3] = p[0] + v_par + v_perp * np.cos(angle) + w * np.sin(angle)
    return p


class QuadExplorer(Scene):
    """Six quadrilaterals, one live window, and a mouse that actually works."""

    def construct(self) -> None:
        self.index = 0
        self.fold_step = 0
        self.show_marks = True
        self.show_diagonals = False
        self.quit_interaction = False

        self.add(table_top(20.0, 14.0))
        self.figure = VGroup()
        self.hud = VGroup()
        self.add(self.figure, self.hud)

        self._orient_camera()
        self._rebuild()

        for i, name in enumerate(FAMILY_ORDER):
            self.set_key_function(str(i + 1), self._selector(i))
        self.set_key_function("n", self._next_shape)
        self.set_key_function("m", self._toggle_marks)
        self.set_key_function("x", self._toggle_diagonals)
        self.set_key_function("f", self._fold)

        # Keep the window alive and dispatching events.  Every `wait` swaps
        # the buffer, which is where pyglet pumps mouse and key events, so the
        # camera keeps responding for as long as this loop runs.
        #
        # QUAD_EXPLORER_AUTOQUIT=<seconds> closes the window on its own, which
        # is the only way to smoke-test an interactive scene without a person
        # sitting in front of it.
        budget = float(os.environ.get("QUAD_EXPLORER_AUTOQUIT", 0) or 0)
        waited = 0.0
        while not self.quit_interaction:
            if getattr(self.renderer, "window", None) is not None:
                if self.renderer.window.is_closing:
                    break
            self.wait(0.2)
            waited += 0.2
            if budget and waited >= budget:
                break

    # ------------------------------------------------------------ camera --
    def _orient_camera(self) -> None:
        """A three-quarter view to start from; the mouse takes it from here."""
        camera = getattr(self.renderer, "camera", None)
        if camera is not None and hasattr(camera, "set_phi"):
            camera.set_phi(58 * DEGREES)
            camera.set_theta(-90 * DEGREES)

    # ------------------------------------------------------------- build --
    @property
    def shape(self) -> str:
        return FAMILY_ORDER[self.index]

    def _rebuild(self) -> None:
        """Redraw the figure and the heads-up display from current state."""
        name = self.shape
        color = FAMILY_COLOR[name]
        angle = FOLD_STEPS[self.fold_step]
        pts = folded(FAMILY_PTS[name], angle)

        body = plate(pts, color)
        top = [p + LIFT for p in plate_top(pts)]

        parts = VGroup(body)
        if self.show_marks and not angle:
            # Once the shape leaves its plane the marks would be claiming
            # things about a figure that is no longer flat, so they go away.
            parts.add(marks_for(name, top))
        if self.show_diagonals:
            parts.add(diagonals(top, MUTED, 3.0))

        # The panel stands upright on the table beside the shape rather than
        # being pinned to the frame: in an orbiting window there is no fixed
        # frame to pin it to, and a placard that turns with the scene reads
        # as part of the model instead of fighting it.
        panel = VGroup(
            txt(FAMILY_NAME[name], 34, color, "BOLD"),
            mtx(FAMILY_RULE[name], 32, color),
            txt(f"fold {angle:.2f} rad" if angle else "flat", 26,
                AMBER if angle else MUTED),
        ).arrange(DOWN, buff=0.28)
        placard(panel, np.array([0.0, -2.75, 0.0]), lift=0.85)

        self.remove(self.figure, self.hud)
        self.figure, self.hud = parts, panel
        self.add(self.figure, self.hud)

    # ------------------------------------------------------------- input --
    def _selector(self, i: int):
        def choose() -> None:
            self.index = i
            self.fold_step = 0
            self._rebuild()
        return choose

    def _next_shape(self) -> None:
        self.index = (self.index + 1) % len(FAMILY_ORDER)
        self.fold_step = 0
        self._rebuild()

    def _toggle_marks(self) -> None:
        self.show_marks = not self.show_marks
        self._rebuild()

    def _toggle_diagonals(self) -> None:
        self.show_diagonals = not self.show_diagonals
        self._rebuild()

    def _fold(self) -> None:
        self.fold_step = (self.fold_step + 1) % len(FOLD_STEPS)
        self._rebuild()

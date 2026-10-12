"""Composition lab: render single stills to tune 3D rigs cheaply.

Each class renders one frame with ``-s``, so iterating on a camera angle or a
rig's proportions costs about a second instead of a full scene render.

    python -m manim render -s --resolution 640,360 --media_dir D:\\m3 \
        --disable_caching _shot_lab.py ShotTunnelA ShotTunnelB ...
"""
from __future__ import annotations

import numpy as np

from manim import DEGREES, DOWN, LEFT, ORIGIN, RIGHT, UP, Rectangle, VGroup

from theme import NEON_CYAN, NEON_BLUE, INK, LLMScene, mono, pg
from three_d import apply_depth, box3d, grid_floor, lab_bench, token_tunnel


class _Rig(LLMScene):
    module_stem = "_shot_lab"

    def setup(self) -> None:
        pass

    def construct(self) -> None:
        self.setup_episode()
        self.add_backdrop()
        self.build()


class ShotTunnelA(_Rig):
    """front frame large, spacing wide, low oblique camera."""

    def build(self) -> None:
        self.set_camera_orientation(phi=66 * DEGREES, theta=-60 * DEGREES,
                                    zoom=1.22)
        t = token_tunnel(n=6, spacing=2.8, size=(3.8, 2.0), start_z=-0.5)
        t.move_to(np.array([0.0, 0.2, 0.0]))
        self.add(t)


class ShotTunnelB(_Rig):
    """tighter spacing and a floor grid: corridor should read as depth."""

    def build(self) -> None:
        self.set_camera_orientation(phi=70 * DEGREES, theta=-58 * DEGREES,
                                    zoom=1.0)
        floor = grid_floor(width=11.0, depth=16.0, lines=7, y=-1.9)
        t = token_tunnel(n=7, spacing=1.9, size=(3.6, 1.8), start_z=-0.6)
        t.move_to(np.array([0.0, -0.1, 0.0]))
        self.add(floor, t)


class ShotTunnelC(_Rig):
    """steeper look-down, corridor fills the panel."""

    def build(self) -> None:
        self.set_camera_orientation(phi=78 * DEGREES, theta=-62 * DEGREES,
                                    zoom=1.05)
        floor = grid_floor(width=12.0, depth=18.0, lines=8, y=-2.0)
        t = token_tunnel(n=8, spacing=1.7, size=(4.0, 2.0), start_z=-0.4)
        t.move_to(np.array([0.0, 0.1, 0.0]))
        self.add(floor, t)


class ShotFonts(_Rig):
    """The drawable emoji substitutes: vector note, CJK glyph, sample line."""

    def build(self) -> None:
        from components import book_sample_line, music_note
        from theme import GREEN, INK, cjk
        line = book_sample_line(size=15)
        line.move_to(np.array([0.0, 1.55, 0.0]))
        row = VGroup(
            music_note(height=1.6, color=INK),
            cjk("\u9E1F", 58),
            music_note(height=1.05, color=GREEN),
            music_note(height=0.62, color="#FBBF24"),
        ).arrange(RIGHT, buff=0.9).move_to(np.array([0.0, -0.35, 0.0]))
        self.add(line, row)


class ShotGridA(_Rig):
    """numbered input floor, high look-down."""

    def build(self) -> None:
        from three_d import input_grid_floor
        self.set_camera_orientation(phi=38 * DEGREES, theta=-70 * DEGREES,
                                    zoom=1.0)
        self.add(grid_floor(width=12.0, depth=18.0, lines=8, y=-2.0),
                 input_grid_floor(rows=4, cols=6))


class ShotGridB(_Rig):
    """numbered input floor, slightly lower and closer."""

    def build(self) -> None:
        from three_d import input_grid_floor
        self.set_camera_orientation(phi=48 * DEGREES, theta=-72 * DEGREES,
                                    zoom=1.05)
        g = input_grid_floor(rows=4, cols=6, pitch_x=1.7, pitch_z=1.7)
        g.move_to(np.array([0.0, 0.0, -1.2]))
        self.add(grid_floor(width=12.0, depth=20.0, lines=8, y=-2.0), g)


class ShotGridC(_Rig):
    """numbered input floor with the prompt pinned as legible HUD text."""

    def build(self) -> None:
        from three_d import input_grid_floor
        from theme import panel
        self.set_camera_orientation(phi=40 * DEGREES, theta=-70 * DEGREES,
                                    zoom=1.02)
        self.add(grid_floor(width=10.5, depth=16.0, lines=7, y=-2.0),
                 input_grid_floor(rows=3, cols=6, pitch_x=1.42, pitch_z=1.5))
        box = panel(6.2, 0.9, color=NEON_CYAN, fill_opacity=0.18)
        box.move_to(np.array([0.0, 2.15, 0.0]))
        lbl = mono("What is the capital of India?", 25, INK)
        lbl.move_to(box.get_center())
        group = VGroup(box, lbl)
        self.hud(group)
        self.add(group)


class ShotBench(_Rig):
    """the four-tokenizer laboratory bench, angled."""

    def build(self) -> None:
        self.set_camera_orientation(phi=68 * DEGREES, theta=-64 * DEGREES,
                                    zoom=1.0)
        b = lab_bench([
            ("BERT uncased", "WordPiece", "2018", NEON_CYAN),
            ("GPT-2", "BPE", "2019", NEON_BLUE),
            ("FLAN-T5", "SentencePiece", "2022", "#A6D854"),
            ("GPT-4", "BPE", "2023", "#E78AC3"),
        ])
        b.move_to(np.array([0.0, 0.4, 0.0]))
        self.add(b)


class ShotConsole(_Rig):
    """the three-control tokenizer console."""

    def build(self) -> None:
        from data_traces import THREE_FACTORS
        from three_d import control_console
        self.set_camera_orientation(phi=64 * DEGREES, theta=-58 * DEGREES,
                                    zoom=1.0)
        c = control_console(THREE_FACTORS)
        c.move_to(np.array([0.0, 0.3, 0.0]))
        self.add(c)


class ShotVault(_Rig):
    """the vocabulary vault wall."""

    def build(self) -> None:
        from three_d import vault_wall
        self.set_camera_orientation(phi=62 * DEGREES, theta=-62 * DEGREES,
                                    zoom=1.0)
        v = vault_wall([("apolog", 27746), ("izing", 5281), ("play", 4021),
                        ("##ization", 7712), ("token", 3301), ("Subject", 3323),
                        ("ject", 622)],
                       rows_visible=6)
        v.move_to(np.array([0.0, 0.3, 0.0]))
        self.add(v)


class ShotSlab(_Rig):
    """the embedding slab with two extruded vectors."""

    def build(self) -> None:
        from three_d import embedding_slab, vector_beam
        self.set_camera_orientation(phi=68 * DEGREES, theta=-60 * DEGREES,
                                    zoom=1.0)
        s = embedding_slab()
        s.move_to(np.array([-0.6, 0.2, 0.0]))
        beams = VGroup(vector_beam(seed=1, spread=2.4),
                       vector_beam(seed=4, spread=2.4, z=-0.9))
        beams.move_to(np.array([2.4, -0.6, 0.0]))
        self.add(s, beams)

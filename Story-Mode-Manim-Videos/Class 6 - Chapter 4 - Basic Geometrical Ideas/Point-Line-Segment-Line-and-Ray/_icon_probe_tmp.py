"""Draw just the new artwork on a board-coloured background and save one frame.

A 30-second check that the reshaped icons actually read as a book, a screen, a
rangoli, a five-pointed star and a torch before a five-minute render is spent.

    python -m manim render --resolution 640,360 -s --media_dir D:\\m3 \
        _icon_probe_tmp.py IconProbe
"""
from __future__ import annotations

from manim import DOWN, RIGHT, UP, Rectangle, Scene, VGroup, config

config.renderer = "cairo"
config.disable_caching = True

from fundamental_geometric_building_blocks_point_line_ray import (  # noqa: E402
    Dot, CHALK_GREEN, CHALK_WHITE, object_icon, torch_icon,
)


class IconProbe(Scene):
    def construct(self) -> None:
        board = Rectangle(width=config.frame_width,
                          height=config.frame_height,
                          fill_color="#2E4A32", fill_opacity=1.0,
                          stroke_width=0)
        icons = VGroup(*[object_icon(k, size=1.35)
                         for k in ("book", "screen", "rangoli", "star")])
        icons.arrange(RIGHT, buff=1.0).shift(UP * 1.25)
        torch = torch_icon(scale=1.7).shift(DOWN * 1.15 + RIGHT * 0.3)
        switch = Dot(radius=0.05, color=CHALK_WHITE).next_to(icons, DOWN,
                                                             buff=0.35)
        self.add(board, icons, torch, switch)

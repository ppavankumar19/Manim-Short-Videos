"""Phase 0 proof clip.

Not part of the episode: this exists to prove four things at 360p before any
real scene is written.

  1. The supplied backdrop sits *behind* geometry that the 3D camera
     perspective-projects (the layering trap in ThreeDCamera).
  2. The safe-area constants actually land inside the artwork's glass panel.
  3. Zephyr narration plays, and the real per-word timings drive the reveals.
  4. The ground-truth SRT is written where the house pipeline expects it.

Render:
    python -m manim render --resolution 640,360 --fps 30 _proof_scene.py ProofClip
"""
from __future__ import annotations

import numpy as np

from manim import (
    DEGREES, DOWN, LEFT, ORIGIN, RIGHT, UP,
    Create, FadeIn, FadeOut, LaggedStart, Rectangle, RoundedRectangle,
    Text, VGroup, Write,
)

from data_traces import BOOK, CHAPTER
from theme import (
    AMBER, INK, MONO, MUTED, NEON_CYAN, NEON_VIOLET, PANEL, ROSE, SAFE_B,
    SAFE_L, SAFE_R, SAFE_T, TITLE_Y, LLMScene, mono, panel, pg, rt,
    source_chip, title_bar, token_color,
)


class ProofClip(LLMScene):
    module_stem = "_proof_scene"

    def construct(self) -> None:
        self.setup_episode()
        self.add_backdrop()
        self._beat_proof()
        self.write_real_srt()

    # ------------------------------------------------------------------
    def _beat_proof(self) -> None:
        text = (
            "Before a language model can read a single word, something has to "
            "turn that word into numbers.<bookmark mark='tunnel'/> "
            "This is the token machine."
        )
        with self.voiceover(text=text) as tracker:
            title = self.hud(title_bar("Proof clip - layering, framing, timing"))
            self.play(FadeIn(title), run_time=0.5)
            self.keep.add(title)

            prompt = panel(4.6, 0.86, color=NEON_CYAN)
            prompt.set_z_index(5)
            label = mono("Hello!", 30, INK).move_to(prompt.get_center())
            label.set_z_index(6)
            group = VGroup(prompt, label).move_to(np.array([0.0, 1.4, 0.0]))

            self.play(FadeIn(group, shift=DOWN * 0.15),
                      run_time=rt(tracker.time_until_bookmark("tunnel") * 0.40))

            # A receding corridor of frames.  These are ordinary Rectangles at
            # real z: ThreeDCamera perspective-projects them, and because they
            # are not shade_in_3d they still respect z_index against the
            # fixed-in-frame backdrop.
            corridor = VGroup()
            for i in range(4):
                z = -2.2 - i * 2.6
                frame = Rectangle(
                    width=3.0, height=0.95,
                    stroke_color=token_color(i), stroke_width=2.4,
                    fill_color=token_color(i), fill_opacity=0.14,
                )
                frame.move_to(np.array([0.0, 0.4, z]))
                chip = mono(f"id {42 + i}", 20, token_color(i))
                chip.move_to(np.array([0.0, -0.55, z]))
                corridor.add(VGroup(frame, chip))
            corridor.set_z_index(2)

            self.play(
                LaggedStart(*[Create(f) for f in corridor], lag_ratio=0.22),
                run_time=rt(tracker.time_until_bookmark("tunnel") * 0.60),
            )
            self.keep.add(corridor)

            self.view_3d(phi=66, theta=-60, zoom=1.05, run_time=1.5)

            foot = self.hud(pg("backdrop fixed in frame | corridor is real 3D",
                               20, AMBER, "BOLD").move_to(
                np.array([0.0, -2.35, 0.0])))
            self.play(Write(foot),
                      run_time=rt(tracker.get_remaining_duration() - 0.6))
            chip = self.hud(source_chip("illus"))
            self.play(FadeIn(chip), run_time=0.4)
            self.keep.add(foot, chip)
            self.capture_srt(tracker)

        self.clear_stage()
        self.view_2d(run_time=0.6)

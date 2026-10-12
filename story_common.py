"""Shared helpers for the Story-Mode-Manim-Videos series.

This module is the single home for the series' consistent 10-second
"YOUR TURN" challenge clock, so every story video shows the exact same
timer look and behaviour:

  - a round chalk-styled badge with "THINK" and the countdown (10s -> 0s)
    stacked in its centre,
  - a soft click on every tick,
  - and, while the clock runs, the WHOLE board dims -- a dark veil at
    z_index 20, above every chalk mobject (default z 0) and above the
    backdrop images (z -10/-5), but below the badge itself (z 30) so
    only the badge stays at full brightness while everything else,
    challenge question included, dims behind it.
"""
from __future__ import annotations

import numpy as np

from manim import (
    BLACK, Circle, FadeIn, FadeOut, Rectangle, ReplacementTransform,
    Scene, Text, VGroup, config,
)

FONT = "Segoe Print"
CHALK_YELLOW = "#FFE066"
CHALK_AMBER = "#E8B769"

# Dead centre of the chalkboard itself (matches BOARD_CX/BOARD_CY, shared
# across every Story-Mode video's own board layout constants) -- the big
# round badge becomes the visual focus of the "think" pause instead of a
# small strip at the bottom.
CLOCK_POS = np.array([0.5, 0.2, 0.0])


def install_sfx_safe_sounds() -> None:
    """Keep every sound effect in the mix on a cached re-render.

    ``CairoRenderer.play()`` sets ``skip_animations = True`` whenever an
    animation is served from Manim's partial-movie cache (so a re-render of an
    unchanged beat is fast), and ``Scene.add_sound()`` returns early while that
    flag is set.  Every sound effect in these stories is added right after a
    ``play()``, so on any re-render that reuses cached animations the pop, the
    ding and -- the one that matters most -- each tick of the THINK clock were
    silently dropped from the audio track.  manim-voiceover works around the
    same trap for the narration clips; this does it for the sound effects by
    restoring the flag before handing over to the real ``add_sound``.

    Imported (and therefore installed) with ``story_common``, so every story
    module gets it without a code change of its own.
    """
    if getattr(Scene, "_sfx_safe_add_sound", False):
        return
    original = Scene.add_sound

    def add_sound(self, sound_file, *args, **kwargs):
        renderer = getattr(self, "renderer", None)
        if renderer is not None:
            renderer.skip_animations = renderer._original_skipping_status
        return original(self, sound_file, *args, **kwargs)

    Scene.add_sound = add_sound
    Scene._sfx_safe_add_sound = True


install_sfx_safe_sounds()


def play_compact_countdown(scene, seconds: int = 10, *,
                           sfx: dict | None = None,
                           position: np.ndarray) -> None:
    """The same THINK clock, small, parked at `position` near the top of the
    board.  The board is NOT dimmed: the question stays fully visible."""
    r = 0.46
    ring = Circle(radius=r, stroke_color=CHALK_AMBER, stroke_width=3.5,
                  fill_color="#0A1A12", fill_opacity=0.95).move_to(position)
    think_lbl = Text("THINK", font=FONT, font_size=14, color=CHALK_AMBER,
                     weight="BOLD").move_to(position + np.array([0.0, 0.17, 0.0]))

    def dg(n, at=None):
        t = Text(f"{n}s", font=FONT, font_size=24, color=CHALK_YELLOW,
                 weight="BOLD")
        t.move_to(position + np.array([0.0, -0.13, 0.0]) if at is None else at)
        t.set_z_index(30)
        return t
    digits = dg(seconds)
    clock = VGroup(ring, think_lbl, digits).set_z_index(30)
    scene.play(FadeIn(clock), run_time=0.4)
    for remaining in range(seconds - 1, -1, -1):
        new_digits = dg(remaining, digits.get_center())
        scene.play(ReplacementTransform(digits, new_digits), run_time=1.0)
        if sfx:
            scene.add_sound(sfx["click"], gain=-16)
        digits = new_digits
    scene.play(FadeOut(VGroup(ring, think_lbl, digits)), run_time=0.4)


def play_challenge_countdown(scene, seconds: int = 10, *,
                             sfx: dict | None = None,
                             position: np.ndarray = CLOCK_POS) -> None:
    """Run the series' consistent challenge countdown clock: a round
    badge with "THINK" above the seconds count, both centred inside it.

    `scene` is the VoiceoverScene instance; `sfx` the scene's loaded
    sound-effect dict (optional). The whole countdown runs
    0.4s (fade in) + `seconds` (clock) + 0.4s (fade out).
    """
    # 1) Dim veil over the WHOLE board -- see module docstring for the
    # z_index ordering that keeps only the badge undimmed.
    dim = Rectangle(
        width=config.frame_width + 0.6,
        height=config.frame_height + 0.6,
        fill_color=BLACK,
        fill_opacity=0.72,
        stroke_width=0,
    ).move_to(np.array([0.0, 0.0, 0.0]))
    dim.set_z_index(20)

    # 2) Round badge: "THINK" and the countdown, both centred inside it.
    #    Bigger now that it sits at board centre (was a small bottom strip).
    ring = Circle(
        radius=0.9, stroke_color=CHALK_AMBER, stroke_width=4,
        fill_color="#0A1A12", fill_opacity=0.95,
    ).move_to(position)
    think_lbl = Text("THINK", font=FONT, font_size=22, color=CHALK_AMBER,
                     weight="BOLD").move_to(position + np.array([0.0, 0.34, 0.0]))
    digits = Text(f"{seconds}s", font=FONT, font_size=46, color=CHALK_YELLOW,
                  weight="BOLD").move_to(position + np.array([0.0, -0.2, 0.0]))
    clock = VGroup(ring, think_lbl, digits).set_z_index(30)

    scene.play(FadeIn(dim), FadeIn(clock), run_time=0.4)

    # 3) Count down one second at a time.
    for remaining in range(seconds - 1, -1, -1):
        new_digits = Text(f"{remaining}s", font=FONT, font_size=46,
                          color=CHALK_YELLOW, weight="BOLD").move_to(
            digits.get_center())
        # Each replacement Text is a fresh mobject -- it must be re-pinned
        # to the badge's z_index (30) or it falls behind the z=20 dim veil
        # from the second tick onward and silently disappears.
        new_digits.set_z_index(30)
        scene.play(ReplacementTransform(digits, new_digits), run_time=1.0)
        if sfx:
            scene.add_sound(sfx["click"], gain=-16)
        digits = new_digits

    # 4) Restore the board.
    scene.play(FadeOut(dim), FadeOut(clock), run_time=0.4)

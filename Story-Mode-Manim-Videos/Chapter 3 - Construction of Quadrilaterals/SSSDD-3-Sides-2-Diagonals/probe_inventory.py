"""List every mobject on the board when each beat ends.

    .venv/Scripts/python.exe probe_inventory.py [beat]

Used to identify stray geometry (the dashed strokes seen around the triangle in
scene 5 of the first 1080p cut).
"""
from __future__ import annotations

import collections
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "speech_service.py").exists())
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))

from manim import config  # noqa: E402

config.renderer = "cairo"
config.disable_caching = True

from manim import Line, Text, VGroup  # noqa: E402
from manim.animation.animation import prepare_animation  # noqa: E402

from construct_quadrilateral_3sides_2diagonals import (  # noqa: E402
    ConstructQuadrilateral3Sides2DiagonalsStory,
)

STOP = sys.argv[1] if len(sys.argv) > 1 else "beat5_triangle"


class Tracker:
    data = {"word_boundaries": []}

    def time_until_bookmark(self, mark: str) -> float:
        return 3.0

    def get_remaining_duration(self) -> float:
        return 3.0


class Harness:
    def __init__(self, scene):
        self.scene = scene
        self.clock = 0.0

    def tracker(self):
        return Tracker()

    def play(self, *args, run_time: float = 1.0, **kwargs):
        anims = [prepare_animation(a) for a in args]
        self.scene.add_mobjects_from_animations(anims)
        for a in anims:
            a._setup_scene(self.scene)
            a.begin()
        for a in anims:
            a.interpolate(1)
            a.clean_up_from_scene(self.scene)
        self.clock += float(run_time)

    def wait(self, duration: float = 1.0, **kwargs):
        self.clock += max(0.0, float(duration))


class Ctx:
    def __init__(self, h):
        self.h = h

    def __enter__(self):
        return self.h.tracker()

    def __exit__(self, *exc):
        return False


def dump(scene, name):
    print(f"\n=== {name} : {len(scene.mobjects)} top-level mobjects ===")
    for m in scene.mobjects:
        fam = m.get_family()
        c = m.get_center()
        kind = type(m).__name__
        if any(isinstance(x, Text) for x in fam):
            txt = next(x.text for x in fam if isinstance(x, Text))
            print(f"  {kind:24s} fam={len(fam):4d} @({c[0]:+.2f},{c[1]:+.2f}) "
                  f"text={txt[:24]!r}")
            continue
        lines = [x for x in fam if isinstance(x, Line)]
        if lines and len(lines) == 1:
            ln = lines[0]
            print(f"  {kind:24s} fam={len(fam):4d} @({c[0]:+.2f},{c[1]:+.2f}) "
                  f"line {np.round(ln.get_start()[:2], 2)} -> "
                  f"{np.round(ln.get_end()[:2], 2)} pts={len(ln.points)}")
            continue
        print(f"  {kind:24s} fam={len(fam):4d} @({c[0]:+.2f},{c[1]:+.2f}) "
              f"lines={len(lines)}")


def main() -> None:
    scene = ConstructQuadrilateral3Sides2DiagonalsStory()
    scene._clock = 0.0
    scene.sfx = collections.defaultdict(lambda: None)
    h = Harness(scene)

    scene.voiceover = lambda text=None, **kw: Ctx(h)
    scene.play = h.play
    scene.wait = h.wait
    scene.add_sound = lambda *a, **k: None
    scene.set_speech_service = lambda *a, **k: None
    scene._capture_srt = lambda *a, **k: None
    scene._write_real_srt = lambda: None
    scene.add_background = lambda: None
    scene.reset_board = lambda: scene.clear()

    order = ["beat0_title", "beat1_data", "beat2_choose", "beat3_plan",
             "beat4_diagonal", "beat5_triangle", "beat6_locate_d",
             "beat7_complete", "beat8_method", "beat9_challenge",
             "beat10_recap"]
    for name in order:
        getattr(scene, name)()
        dump(scene, name)
        if name == STOP:
            break


if __name__ == "__main__":
    main()

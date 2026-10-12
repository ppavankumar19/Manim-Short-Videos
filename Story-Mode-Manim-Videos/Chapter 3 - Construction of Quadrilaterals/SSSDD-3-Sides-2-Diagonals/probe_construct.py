"""Replay the scene with a fake voiceover so construct-time errors surface
before a render is spent on them.

Run from the topic folder:
    .venv/Scripts/python.exe probe_construct.py

The fake tracker hands every bookmark the same plausible offset, which is
enough to exercise every play (positions, geometry helpers, transforms); it is
NOT a sync check -- the real timings come from the rendered audio.
"""
from __future__ import annotations

import re
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "speech_service.py").exists())
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))

from manim import config  # noqa: E402

config.renderer = "cairo"
config.disable_caching = True

from construct_quadrilateral_3sides_2diagonals import (  # noqa: E402
    ConstructQuadrilateral3Sides2DiagonalsStory,
)

STEP = 4.0          # seconds the fake tracker allows per bookmark


class FakeTracker:
    data = {"word_boundaries": []}

    def __init__(self, clock, marks):
        self.clock = clock
        self.marks = marks
        self.asked: set[str] = set()

    def time_until_bookmark(self, mark: str) -> float:
        # the real tracker raises when a beat asks for a mark its narration
        # does not define -- reproduce that here so the mistake costs a probe
        # run instead of a whole render
        if mark not in self.marks:
            raise Exception(f"There is no <bookmark mark='{mark}' />")
        self.asked.add(mark)
        try:
            n = int(re.search(r"\d+", mark).group())
        except AttributeError:
            n = 0
        return max(0.0, (n + 1) * STEP - self.clock)

    def get_remaining_duration(self) -> float:
        return max(0.0, 6 * STEP - self.clock)


class Ctx:
    def __init__(self, scene, text):
        self.scene = scene
        self.marks = set(re.findall(r"<bookmark mark='([^']+)'/>", text or ""))
        self.tracker = None

    def __enter__(self):
        self.tracker = FakeTracker(self.scene._clock, self.marks)
        self.scene._trackers.append(self.tracker)
        return self.tracker

    def __exit__(self, *exc):
        self.scene._clock += 8 * STEP
        self.scene._clock = 0.0
        return False


def main() -> None:
    scene = ConstructQuadrilateral3Sides2DiagonalsStory()
    scene._clock = 0.0
    scene._trackers = []
    scene.voiceover = lambda text=None, **kw: Ctx(scene, text)
    scene.play = lambda *a, run_time=1.0, **kw: None
    scene.wait = lambda *a, **kw: None
    scene.add_sound = lambda *a, **k: None
    scene.set_speech_service = lambda *a, **k: None
    scene.install_synced_voiceover = lambda *a, **k: None
    scene._capture_srt = lambda *a, **k: None
    scene._write_real_srt = lambda: None
    scene.add_background = lambda: None
    scene.reset_board = lambda: None
    try:
        scene.construct()
        print("construct completed")
        unused = [t.marks - t.asked for t in scene._trackers]
        for k, u in enumerate(unused):
            if u:
                print(f"  note: piece {k} never used {sorted(u)}")
    except Exception:
        traceback.print_exc()
        raise SystemExit(1)


if __name__ == "__main__":
    main()

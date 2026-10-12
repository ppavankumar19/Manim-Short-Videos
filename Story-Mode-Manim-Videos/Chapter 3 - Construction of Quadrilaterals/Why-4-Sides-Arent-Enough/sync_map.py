"""Sync map: for every play() in the scene, show the narration words it
actually plays over (real audio timings), so visual-vs-voice mismatches are
visible at a glance.

Run from the topic folder:
    .venv/Scripts/python.exe sync_map.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
_ROOT = next(p for p in _HERE.parents
        if (p / "speech_service.py").exists())
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from manim import config  # noqa: E402
config.renderer = "cairo"
config.disable_caching = True

from manim.animation.animation import prepare_animation  # noqa: E402
from manim_voiceover.helper import remove_bookmarks  # noqa: E402

from quadrilateral_uniqueness_and_five_measurements import NARRATION, QuadrilateralUniquenessStory  # noqa: E402

NO_BM = re.compile(r"<bookmark mark='([^']+)'/>")


class Mapper:
    def __init__(self):
        self.piece = "?"
        self.rows: list[tuple] = []
        self.pending: list[str] = []
        self.seg_text = ""
        self.clock = 0.0
        self.mark_times: dict[str, float] = {}
        self.piece_start = 0.0

    # -- fake voiceover -----------------------------------------------------
    def _enter(self, text: str) -> None:
        for piece, narr in NARRATION.items():
            if narr == text:
                self.piece = piece
                break
        self.piece_start = self.clock
        self.pending = []
        # absolute time of each bookmark, from character position, using the
        # real per-beat duration only as a scale (order is what matters here)
        cleaned = remove_bookmarks(text)
        total = max(len(cleaned), 1)
        marks = {}
        consumed = 0
        for m in NO_BM.finditer(text):
            pos = m.start() - consumed
            consumed += len(m.group(0))
            marks[m.group(1)] = pos / total
        self.mark_fracs = marks

    def _exit(self) -> None:
        self.piece = "?"
        self.pending = []

    def tracker(self):
        h = self

        class T:
            data = {"word_boundaries": []}

            def time_until_bookmark(tself, mark):
                h.pending.append(mark)
                return 0.3

            def get_remaining_duration(tself):
                h.pending.append("<remaining>")
                return 0.3

        return T()

    def voiceover(self, text=None, **kw):
        h = self

        class CM:
            def __enter__(cm):
                h._enter(text)
                return h.tracker()

            def __exit__(cm, *exc):
                h._exit()

        return CM()

    # -- fake play ----------------------------------------------------------
    def play(self, *args, run_time: float = 1.0, **kwargs):
        anims = []
        for a in args:
            try:
                prepared = prepare_animation(a)
            except Exception:
                continue
            name = type(prepared).__name__
            tgt = getattr(prepared, "mobject", None)
            label = self._describe(tgt)
            anims.append(f"{name}{label}")
        seg = self._segment_text(self.pending)
        self.rows.append((self.piece, "; ".join(self.pending) or "-",
                          round(float(run_time), 2), seg, " | ".join(anims)[:150]))
        self.pending = []
        self.clock += float(run_time)

    def wait(self, duration=1.0, **kw):
        self.clock += float(duration)

    @staticmethod
    def _describe(mobj):
        if mobj is None:
            return ""
        for m in mobj.get_family():
            t = getattr(m, "tex_string", None) or getattr(m, "text", None)
            if t:
                return f"({t[:28]!r})"
        return ""

    def _segment_text(self, marks: list[str]) -> str:
        narr = NARRATION.get(self.piece, "")
        cleaned = remove_bookmarks(narr)
        # locate bookmark char offsets in the cleaned text
        offsets, consumed = {}, 0
        for m in NO_BM.finditer(narr):
            offsets[m.group(1)] = m.start() - consumed
            consumed += len(m.group(0))
        used = [m for m in marks if m in offsets]
        if not used:
            return "(no bookmark)"
        last = max(used, key=lambda m: offsets[m])
        start = 0
        for mark, off in sorted(offsets.items(), key=lambda kv: kv[1]):
            if off < offsets[last]:
                start = off
        seg = cleaned[start:offsets[last]].strip()
        return (seg[:88] + "...") if len(seg) > 88 else seg


def main() -> None:
    scene = QuadrilateralUniquenessStory()
    m = Mapper()
    scene.voiceover = lambda text=None, **kw: m.voiceover(text, **kw)
    scene.play = m.play
    scene.wait = m.wait
    scene.add_sound = lambda *a, **k: None
    scene.set_speech_service = lambda *a, **k: None
    scene._capture_srt = lambda *a, **k: None
    scene._write_real_srt = lambda: None
    try:
        scene.construct()
    except Exception as exc:  # layout errors are irrelevant for the map
        print(f"(construct stopped early: {exc})")

    current = None
    for piece, marks, rt_, seg, anims in m.rows:
        if piece != current:
            print(f"\n===== {piece} =====")
            current = piece
        print(f"  [{marks:>16s}] rt={rt_:>5.2f}  words: {seg}")
        print(f"  {'':>16s}        anim: {anims}")


if __name__ == "__main__":
    main()

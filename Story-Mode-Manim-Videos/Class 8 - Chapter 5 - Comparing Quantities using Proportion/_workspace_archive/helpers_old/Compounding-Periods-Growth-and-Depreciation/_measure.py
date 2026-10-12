"""Measure the clear space around the four exponent-carrying formulas.

The revision pass asked for the powers to have room: each formula's FULL
bounding box (the raised exponent included) must keep about 0.25 units of clear
air above it.  This probe replays the cut exactly as `audit_sync_overlap.py`
does -- same harness, same draft SRT, same fake play/wait -- and at every play
boundary records, for each of the four formulas, its own bbox (and its
exponent's top), the nearest TEXT above it and the nearest FRAME above it.

    python _measure.py

It prints one row per formula; nothing is written and nothing is rendered.
"""
from __future__ import annotations

import importlib
import re
import sys
from pathlib import Path

from manim import config

config.renderer = "cairo"
config.disable_caching = True

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

audit = importlib.import_module("audit_sync_overlap")          # noqa: E402
mod = importlib.import_module(                                   # noqa: E402
    "compounding_periods_half_yearly_quarterly_depreciation")

# The four powers the revision named, by the LaTeX that draws them.
TARGETS = {
    r"P\left(1 + \frac{R}{200}\right)^{2n}": "s2  half-yearly  P(1+R/200)^2n",
    r"P\left(1 + \frac{R}{400}\right)^{4n}": "s4  quarterly   P(1+R/400)^4n",
    r"A = P\left(1 + \frac{R}{100}\right)^{n}": "s10 growth      A=P(1+R/100)^n",
    r"V = P\left(1 - \frac{R}{100}\right)^{n}": "s10/s6 decline  V=P(1-R/100)^n",
}


def norm(s: str) -> str:
    return re.sub(r"\s+", "", s or "")


WANT = {norm(k): v for k, v in TARGETS.items()}


class MeasureHarness(audit.Harness):
    """The sync audit's harness, plus a measurement of the formulas."""

    def __init__(self, scene):
        super().__init__(scene)
        self.rows: list[dict] = []

    def play(self, *args, run_time: float = 1.0, **kwargs):
        super().play(*args, run_time=run_time, **kwargs)
        texts, frames = [], []
        for m in self.scene.mobjects:
            for leaf in audit.content_leaves(m):
                if audit.is_texty(leaf):
                    texts.append(leaf)
                elif audit.frame_kind(leaf) is not None:
                    frames.append(leaf)
        for leaf in texts:
            key = norm(getattr(leaf, "tex_string", "") or "")
            hit = next((lab for tgt, lab in WANT.items() if tgt in key), None)
            if hit is None:
                continue
            x0, y0, x1, y1 = self.bbox(leaf)
            label = hit
            best = None
            for other in texts:
                if other is leaf:
                    continue
                ox0, oy0, ox1, oy1 = self.bbox(other)
                if ox1 < x0 + 0.05 or ox0 > x1 - 0.05:
                    continue                      # no horizontal overlap
                if oy1 < y0 - 0.01:
                    continue                      # not above the formula
                gap = oy0 - y1
                if best is None or gap < best[0]:
                    best = (gap, other)
            bestf = None
            for fr in frames:
                fx0, fy0, fx1, fy1 = self.bbox(fr)
                if fx1 < x0 + 0.05 or fx0 > x1 - 0.05:
                    continue
                if fy1 < y0 - 0.01:
                    continue
                gap = fy0 - y1
                if bestf is None or gap < bestf[0]:
                    bestf = (gap, fr)
            self.rows.append({
                "label": label,
                "piece": self.piece, "w": x1 - x0, "h": y1 - y0,
                "top": y1, "bot": y0,
                "text_gap": None if best is None else best[0],
                "text": None if best is None else audit.describe(best[1]),
                "frame_gap": None if bestf is None else bestf[0],
                "frame": None if bestf is None else audit.describe(bestf[1]),
            })


def main() -> None:
    scene = mod.CompoundingPeriodsHalfYearlyQuarterlyDepreciationStory()
    h = MeasureHarness(scene)
    scene.voiceover = lambda text=None, **kw: h.voiceover_cm(text)
    scene.play = h.play
    scene.wait = h.wait
    scene.add_sound = lambda *a, **k: None
    scene.set_speech_service = lambda *a, **k: None
    scene._capture_srt = lambda *a, **k: None
    scene._write_real_srt = lambda: None

    scene.construct()

    print("\n===== EXPONENT CLEARANCE (formula bbox top vs the nearest "
          "thing above) =====")
    print(f"{'formula':30s} {'piece':6s} {'w':>5s} {'h':>5s} {'top':>6s} "
          f"{'text gap':>9s} {'frame gap':>10s}  nearest above")
    for r in h.rows:
        tg = "n/a" if r["text_gap"] is None else f"{r['text_gap']:.2f}"
        fg = "n/a" if r["frame_gap"] is None else f"{r['frame_gap']:.2f}"
        near = r["text"] or r["frame"] or "-"
        print(f"{r['label']:30s} {r['piece']:6s} {r['w']:5.2f} {r['h']:5.2f} "
              f"{r['top']:6.2f} {tg:>9s} {fg:>10s}  {near}")


if __name__ == "__main__":
    main()

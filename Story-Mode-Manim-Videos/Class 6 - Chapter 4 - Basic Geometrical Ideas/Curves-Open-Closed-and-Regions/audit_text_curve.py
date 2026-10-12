"""Text-against-curve clearance probe for curves_open_closed_and_regions.py.

Neither shipped audit can see a label that lies on a *smooth* curve.  Both
classify a leaf with `frame_kind`, which only knows Line/Arrow/DoubleArrow/Dot/
Arc as "line" and Rectangle/RoundedRectangle/Circle/Ellipse/Polygon/Sector as
"area" -- so this topic's open wave and figure eight (bare `VMobject`s) fall
through both, and an Ellipse or a Polygon is treated as a frame that text is
*meant* to sit inside.  The user's review found exactly that class of defect
(OPEN printed across the wave, "the path joins back" across the oval).

This probe replays the scene with audit_sync_overlap's own harness and then
measures the real geometry: every text leaf's bounding box against every
sampled point of every drawn curve -- any leaf with points that is not text,
not a card panel and not a point marker.  It also prints, per piece, the union
box of the curves so a figure block's centring on BOARD_CX can be checked.

    python audit_text_curve.py [min_gap]
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from manim import ImageMobject

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import audit_sync_overlap as audit  # noqa: E402
from curves_open_closed_and_regions import (  # noqa: E402
    BOARD_CX, CurvesOpenClosedRegionsStory,
)

PANELS = (audit.Rectangle, audit.RoundedRectangle, audit.SurroundingRectangle)


def curve_parts(mob) -> list:
    """Every drawn stroke under `mob`: text, card panels and point markers out.

    A `Text`'s family is made of `VMobjectFromSVGPath` glyph outlines, which
    carry points just like a drawn curve does -- without the `glyph` set below
    every label "collides" with its own letters (gap 0.00).  So the outlines of
    every Text in the family are excluded while the diagram a card also holds
    (a wave inside a question card) is kept."""
    fam = mob.get_family()
    glyph = set()
    for x in fam:
        if isinstance(x, audit.Text):
            for d in x.get_family():
                glyph.add(id(d))
    out = []
    for x in fam:
        if id(x) in glyph:
            continue
        if isinstance(x, (audit.Text, ImageMobject, audit.Dot,
                          audit.ValueTracker)):
            continue
        if isinstance(x, PANELS):
            continue
        if audit.is_decor(x):
            continue
        if len(getattr(x, "points", ())) >= 2:
            out.append(x)
    return out


def text_leaves(mob) -> list:
    return [x for x in mob.get_family() if isinstance(x, audit.Text)]


class Probe(audit.Harness):
    def __init__(self, scene, min_gap: float = 0.10):
        super().__init__(scene)
        self.min_gap = min_gap
        self.curve_hits: list[str] = []
        self.seen_hits: set[str] = set()
        self.blocks: list[str] = []
        self.seen_blocks: set[str] = set()

    def check_overlaps(self) -> None:
        scene = self.scene
        skip = {id(getattr(scene, n, None)) for n in
                ("bg", "student", "teacher", "badge", "badge_l")}
        texts, curves = [], []
        for m in scene.mobjects:
            if id(m) in skip or audit.is_think_badge(m) \
                    or isinstance(m, audit.ValueTracker):
                continue
            texts.extend(text_leaves(m))
            curves.extend(curve_parts(m))
        # --- text against the real curve geometry -------------------------
        for t in texts:
            tx0, ty0, tx1, ty1 = self.bbox(t)
            if (tx1 - tx0) * (ty1 - ty0) < 1e-4:
                continue
            for c in curves:
                cx0, cy0, cx1, cy1 = self.bbox(c)
                # A bounding box is never farther than the curve it wraps, so a
                # box gap wider than the threshold rules the pair out without
                # sampling a single point -- the difference between a ~2 min
                # sweep and an hours-long one.
                if (max(tx0 - cx1, cx0 - tx1) > self.min_gap
                        or max(ty0 - cy1, cy0 - ty1) > self.min_gap):
                    continue
                best = 9.9
                parts = [p for p in c.get_family()
                         if len(getattr(p, "points", ()))]
                for part in parts:
                    for s in np.linspace(0.0, 1.0, 90):
                        p = part.point_from_proportion(s)
                        dx = max(tx0 - p[0], 0.0, p[0] - tx1)
                        dy = max(ty0 - p[1], 0.0, p[1] - ty1)
                        best = min(best, float(np.hypot(dx, dy)))
                        if best < 0.02:
                            break
                    if best < 0.02:
                        break
                if best < self.min_gap:
                    key = f"{self.piece}|{audit.describe(t)}|" \
                          f"{audit.describe(c)}"
                    if key in self.seen_hits:
                        continue
                    self.seen_hits.add(key)
                    self.curve_hits.append(
                        f"[{self.piece:12s} step {self.step:3d}] "
                        f"TEXT-ON-CURVE gap {best:.2f}  {audit.describe(t)}"
                        f"   <->   {audit.describe(c)}")
        # --- where the curves of this piece sit ---------------------------
        if curves:
            xs0 = min(self.bbox(c)[0] for c in curves)
            xs1 = max(self.bbox(c)[2] for c in curves)
            key = f"{self.piece}|{xs0:.2f}|{xs1:.2f}"
            if key not in self.seen_blocks:
                self.seen_blocks.add(key)
                self.blocks.append(
                    f"[{self.piece:12s}] curves span [{xs0:+.2f}..{xs1:+.2f}] "
                    f"centre {(xs0 + xs1) / 2:+.2f}  (board axis {BOARD_CX:+.2f})")


def main() -> None:
    min_gap = float(sys.argv[1]) if len(sys.argv) > 1 else 0.10
    scene = CurvesOpenClosedRegionsStory()
    h = Probe(scene, min_gap)
    scene.voiceover = lambda text=None, **kw: h.voiceover_cm(text)
    scene.play = h.play
    scene.wait = h.wait
    scene.add_sound = lambda *a, **k: None
    scene.set_speech_service = lambda *a, **k: None
    scene._capture_srt = lambda *a, **k: None
    scene._write_real_srt = lambda: None
    scene.construct()

    print(f"\n===== TEXT CLOSER THAN {min_gap} TO A DRAWN CURVE =====")
    if not h.curve_hits:
        print("(none)")
    for line in h.curve_hits:
        print(line)
    print(f"\n{len(h.curve_hits)} text/curve collision(s)")

    print("\n===== CURVE BLOCK POSITION PER PIECE =====")
    for line in h.blocks:
        print(line)


if __name__ == "__main__":
    main()

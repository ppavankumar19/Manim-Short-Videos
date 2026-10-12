"""Is the title card's trace point really travelling round the closed loop?

The user's review asked for the marker that draws the closed curve to keep
moving for the whole hold instead of sitting still, so the claim has to be
checkable.  The trace is a solid CHALK_YELLOW (#FFE066) dot and nothing else on
the title card is that colour, but video compression smears every edge a little
and the board art carries a few warm pixels, so the dot is taken as the densest
8x8 cluster of yellowish pixels inside the loop's own band -- a single dot wins
that vote by a wide margin and the scattered art pixels do not.

A frozen marker reports the same (x, y) in every frame; a travelling one walks
around the loop.  `LOOP_SPEED` is 2.4 rad/s, so the samples below are a little
under a quarter of a lap apart.

    python audit_trace_motion.py <dir-of-pngs>
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

YELLOW = np.array([0xFF, 0xE0, 0x66], dtype=float)
TOL = 60.0          # compressed edges drift: keep a generous colour radius
WINDOW = 8          # px: the densest window of that size holds the dot
# the band the closed loop itself lives in: above it sit the labels, below it
# the captions; a dull chalk-dust patch on the board art (board y ~ -1.8, the
# old, tighter band caught it) is outside this window as well
TOP, BOTTOM, LEFT, RIGHT = 162, 230, 290, 420


def main() -> None:
    d = Path(sys.argv[1])
    for png in sorted(d.glob("*.png")):
        a = np.asarray(Image.open(png).convert("RGB"), dtype=float)
        dist = np.linalg.norm(a - YELLOW, axis=2)
        mask = dist < TOL
        mask[:TOP, :] = mask[BOTTOM:, :] = False
        mask[:, :LEFT] = mask[:, RIGHT:] = False
        ys, xs = np.where(mask)
        if len(xs) == 0:
            print(f"{png.name:22s} no trace pixel found")
            continue
        # vote for the densest WINDOW x WINDOW cell: that is the dot
        ux, uy = np.unique(xs // WINDOW), np.unique(ys // WINDOW)
        counts = {(int(cx), int(cy)):
                  int(((xs // WINDOW == cx) & (ys // WINDOW == cy)).sum())
                  for cx in ux for cy in uy}
        (bx, by), best = max(counts.items(), key=lambda kv: kv[1])
        near = ((xs // WINDOW == bx) & (ys // WINDOW == by))
        cx, cy = xs[near].mean(), ys[near].mean()
        print(f"{png.name:22s} dot @ x={cx:6.1f} y={cy:6.1f}  "
              f"({best} px in its {WINDOW}x{WINDOW} cell, "
              f"{len(xs)} yellowish px on the whole band)")


if __name__ == "__main__":
    main()

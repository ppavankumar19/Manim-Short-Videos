"""Measure the rendered heading's right edge against the corner badge.

The heading sits on the board's heading line (board y = 2.72 -> pixel row 58 at
360p) and the badge's left edge is at board x = 3.79 -> pixel column 490, so the
bright ink in the heading band left of column 490 is the heading, and anything
in that band right of 490 is the badge itself.

    python _badge_px_tmp.py <frame.png> ...
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

BAND_TOP, BAND_BOT = 44, 70          # the heading's own row band
BADGE_LEFT = 490                     # the right badge's left edge, in pixels


def main() -> None:
    for arg in sys.argv[1:]:
        p = Path(arg)
        a = np.asarray(Image.open(p).convert("L"), dtype=float)
        band = a[BAND_TOP:BAND_BOT, 140:BADGE_LEFT]
        ys, xs = np.where(band > 150)
        if len(xs) == 0:
            print(f"{p.name:26s} no heading ink found")
            continue
        right = 140 + int(xs.max())
        badge = a[BAND_TOP:BAND_BOT, BADGE_LEFT:560]
        bxs = np.where((badge > 120).any(axis=0))[0]
        bl = BADGE_LEFT + int(bxs.min()) if len(bxs) else None
        gap_px = (bl - right) if bl is not None else None
        print(f"{p.name:26s} heading right edge x={right:3d}  "
              f"badge left x={bl}  gap={gap_px} px "
              f"= {gap_px / 45.0:.2f} board units" if gap_px is not None else
              f"{p.name:26s} heading right edge x={right:3d}  no badge ink")


if __name__ == "__main__":
    main()

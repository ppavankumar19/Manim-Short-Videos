"""Do the answer/recap rows really share one tag column?

Reads a still of the answers or recap board and, for each row, measures the x of
the row's tag (the letter/digit, drawn in the row's own colour), the sentence
that follows it (same colour, a clear gap away) and the note (the only white ink
in that band).  Fixed columns mean every row reports the same tag x and the same
tag->sentence gap.

    python audit_row_columns.py <still.png> <tag> <tag> ...
        tag = y_pixel_band:colour_hex, e.g. 100:120:7FE7DC
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

GAP_X = 10          # px: wider than any intra-sentence word gap
TOL = 70.0
# the answer boxes span board x -3.80..+4.30 -> pixel 149..514; the room around
# the board is full of warm/green art, so only the box interior is searched
X_LO, X_HI = 158, 500


def main() -> None:
    a = np.asarray(Image.open(Path(sys.argv[1])).convert("RGB"), dtype=float)
    a[:, :X_LO] = 0.0
    a[:, X_HI:] = 0.0
    print(f"{Path(sys.argv[1]).name}")
    print(f"  {'band':>12}  {'tag x0..x1':>14}  {'sentence x0':>11}  "
          f"{'note x0':>8}  gap tag->sentence")
    for spec in sys.argv[2:]:
        y0, y1, hexcol = spec.split(":")
        y0, y1 = int(y0), int(y1)
        col = np.array([int(hexcol[i:i + 2], 16) for i in (0, 2, 4)], dtype=float)
        band = a[y0:y1]
        dist = np.linalg.norm(band - col, axis=2)
        ys, xs = np.where(dist < TOL)
        if len(xs) == 0:
            print(f"  {y0:5d}..{y1:<5d}  no ink")
            continue
        order = np.argsort(xs)
        xs_s = xs[order]
        clusters, start = [], xs_s[0]
        for prev, cur in zip(xs_s, xs_s[1:]):
            if cur - prev > GAP_X:
                clusters.append((start, prev))
                start = cur
        clusters.append((start, xs_s[-1]))
        white = np.where(np.linalg.norm(band - 245.0, axis=2) < 90.0)[1]
        note_x = int(white.min()) if len(white) else -1
        sentence = clusters[1][0] if len(clusters) > 1 else -1
        print(f"  {y0:5d}..{y1:<5d}  {clusters[0][0]:6d}..{clusters[0][1]:<6d}  "
              f"{sentence:>11d}  {note_x:>8d}  "
              f"{'' if sentence < 0 else sentence - clusters[0][1]}")


if __name__ == "__main__":
    main()

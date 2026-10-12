"""When does each closing-scene reveal actually hit the screen?

The strip is the only white text in its band (board y = -1.80 -> pixel row
~261), so counting bright pixels in that narrow band per video frame gives the
exact moment the strip arrives; the thank-you card is the only text in the
board's middle band, and the board rows are the only bright ink in the row band.
This settles whether a reveal lands on its own bookmark in the rendered cut
(rather than merely in the audit's replay).

    python audit_reveal_times.py <movie> <t0> <t1> <step>
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

# pixel bands (640x360): board y -> pixel row = 180 - 45 * y
BANDS = {
    "strip(-1.80)": (256, 268, 240, 420),
    "rows(1.45..-0.35)": (110, 215, 140, 500),
    "banner(-1.15)": (228, 242, 240, 420),
    "thanks(0.62)": (140, 175, 220, 430),
    "bye(-0.32)": (185, 205, 240, 420),
}


def main() -> None:
    movie = Path(sys.argv[1])
    t0, t1, step = float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
    tmp = movie.parent / "_reveal_probe.png"
    t = t0
    print(f"{'t':>7}  " + "  ".join(f"{k:>18}" for k in BANDS))
    while t <= t1 + 1e-9:
        # output seeking: frame-accurate, unlike -ss before -i
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(movie),
                        "-ss", f"{t:.3f}", "-frames:v", "1", str(tmp)],
                       check=True)
        a = np.asarray(Image.open(tmp).convert("L"), dtype=float)
        counts = []
        for y0, y1, x0, x1 in BANDS.values():
            counts.append(int((a[y0:y1, x0:x1] > 150).sum()))
        print(f"{t:7.2f}  " + "  ".join(f"{c:>18d}" for c in counts))
        t += step
    tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    main()

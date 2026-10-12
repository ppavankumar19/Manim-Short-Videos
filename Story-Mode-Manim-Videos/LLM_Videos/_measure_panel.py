"""Locate the neon rim precisely, by profiling the actual pixel columns.

The first attempt scanned for "bright, saturated" pixels, but the backdrop's
circuitry, corner cubes and floor reflections are all bright and saturated,
so the extremes were meaningless.  The rim itself is the brightest thing on
each scan line near the panel, so this prints the luminance profile and picks
the peaks instead.
"""
from __future__ import annotations

import numpy as np
from PIL import Image
from pathlib import Path

HERE = Path(__file__).resolve().parent
BG = HERE / "assets" / "background.png"
FRAME_W, FRAME_H = 14.222, 8.0


def main() -> int:
    a = np.asarray(Image.open(BG).convert("RGB")).astype(np.float32)
    h, w, _ = a.shape
    lum = a.max(axis=2) / 255.0

    def fx(px):
        return (px / w) * FRAME_W - FRAME_W / 2

    def fy(py):
        return FRAME_H / 2 - (py / h) * FRAME_H

    # Average luminance over a band, so a single noisy pixel cannot win.
    def row_profile(y0, y1):
        return lum[y0:y1].mean(axis=0)

    def col_profile(x0, x1):
        return lum[:, x0:x1].mean(axis=1)

    print("row profile (averaged over y=380..560, the panel's clear middle):")
    prof = row_profile(380, 560)
    # left half peaks, right half peaks
    lh = prof[: w // 2]
    rh = prof[w // 2:]
    lpeak = int(np.argmax(lh))
    rpeak = int(w // 2 + np.argmax(rh))
    print(f"   left rim core  x={lpeak}  lum={prof[lpeak]:.3f}   -> frame x {fx(lpeak):+.3f}")
    print(f"   right rim core x={rpeak}  lum={prof[rpeak]:.3f}   -> frame x {fx(rpeak):+.3f}")

    print("\ncol profile (averaged over x=740..930, the panel's clear middle):")
    cprof = col_profile(740, 930)
    th = cprof[: h // 2]
    bh = cprof[h // 2:]
    tpeak = int(np.argmax(th))
    bpeak = int(h // 2 + np.argmax(bh))
    print(f"   top rim core   y={tpeak}  lum={cprof[tpeak]:.3f}   -> frame y {fy(tpeak):+.3f}")
    print(f"   bottom rim core y={bpeak}  lum={cprof[bpeak]:.3f}   -> frame y {fy(bpeak):+.3f}")

    # The rim has thickness; the usable interior is just inside it.
    print("\n  rim cores in frame coords:")
    print(f"    left  {fx(lpeak):+.2f}   right  {fx(rpeak):+.2f}")
    print(f"    top   {fy(tpeak):+.2f}   bottom {fy(bpeak):+.2f}")

    # Walk inward until luminance drops below the rim's half-peak, then a bit
    # further to clear the glow and the inner bevel.
    def inward(prof, peak, step):
        half = prof[peak] * 0.5
        i = peak
        while 0 <= i < len(prof) and prof[i] > half:
            i += step
        return i

    li = inward(prof, lpeak, +1)
    ri = inward(prof, rpeak, -1)
    ti = inward(cprof, tpeak, +1)
    bi = inward(cprof, bpeak, -1)
    print("\n  rim inner edge (half-peak):")
    print(f"    left {fx(li):+.2f}  right {fx(ri):+.2f}  top {fy(ti):+.2f}  bottom {fy(bi):+.2f}")

    print("\n  SAFE box = 0.30 inside that, for the rounded corners:")
    print(f"    SAFE_L = {fx(li) + 0.30:+.2f}")
    print(f"    SAFE_R = {fx(ri) - 0.30:+.2f}")
    print(f"    SAFE_T = {fy(ti) - 0.30:+.2f}")
    print(f"    SAFE_B = {fy(bi) + 0.30:+.2f}")
    print(f"    width  = {(fx(ri) - fx(li)) - 0.60:.2f}")
    print(f"    height = {(fy(ti) - fy(bi)) - 0.60:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Check the fixed corresponding-angles layout on the rendered 1080p master.

Measures, straight from the pixels:
  * the bottom of the green equation box vs the board's bottom edge (-2.9),
  * the horizontal centre of the amber transversal vs the board centre (0.5).
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
VIDEO = (HERE / "media" / "videos" / "geometry_angles_story" / "1080p60"
         / "GeometryAnglesStory_captioned.mp4")
TMP = HERE / "frames"
PX = 1080 / 8.0
BOARD_BOTTOM_PX = (4.0 + 2.9) * PX        # 931.5
BOARD_CX_PX = (0.5 + 14.2222 / 2) * PX    # 1027.5


def grab(t: float, name: str) -> np.ndarray:
    out = TMP / name
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t),
                    "-i", str(VIDEO), "-frames:v", "1", str(out)], check=True)
    return np.asarray(Image.open(out).convert("RGB"), dtype=np.int16)


def near(img, rgb, tol):
    return np.abs(img - np.array(rgb)).sum(axis=2) < tol


def bright_green(img):
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    return (g >= 160) & (g - r >= 45) & (g - b >= 45)


def main() -> None:
    img = grab(152.0, "chk152.png")
    green = bright_green(img)
    sub = green[650:960, 600:1500]
    ys, xs = np.nonzero(sub)
    if len(ys) == 0:
        print("no bright green pixels found in the bottom band")
    else:
        low = ys.max() + 650
        print(f"lowest green box pixel  y = {low} px   "
              f"board bottom y = {BOARD_BOTTOM_PX:.1f} px   margin = "
              f"{BOARD_BOTTOM_PX - low:.0f} px "
              f"({(BOARD_BOTTOM_PX - low) / PX:.2f} manim units)")
        print(f"box stroke pixels in the band: {len(ys)}   "
              f"x span {xs.min() + 600}..{xs.max() + 600}")
    amber = near(img, (232, 183, 105), 70)
    ays, axs = np.nonzero(amber)
    keep = (ays > 200) & (ays < 900) & (axs > 700) & (axs < 1400)
    axs = axs[keep]
    if len(axs):
        print(f"transversal x span {axs.min()} .. {axs.max()}  centre "
              f"{(axs.min() + axs.max()) / 2:.1f} px vs board centre "
              f"{BOARD_CX_PX:.1f} px")


if __name__ == "__main__":
    main()

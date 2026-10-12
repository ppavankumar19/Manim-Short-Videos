"""Locate the THINK countdown inside a rendered story video.

The countdown dims the whole board (a 72% black veil), so the countdown
window is simply the darkest stretch of frames in the second half of the
video.  Printing it means the visual check can be aimed exactly at the
paused clock instead of guessing a timestamp.

    python find_timer.py <video.mp4>
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

W, H = 32, 18


def main() -> None:
    path = Path(sys.argv[1])
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vf",
         f"fps=1,scale={W}:{H},format=gray", "-f", "rawvideo", "-"],
        capture_output=True).stdout
    n = len(raw) // (W * H)
    luma = [sum(raw[i * W * H:(i + 1) * W * H]) / (W * H)
            for i in range(n)]
    base = sorted(luma)[len(luma) // 2]
    dark = [i for i, v in enumerate(luma) if v < base - 12]
    runs, cur = [], []
    for i in dark:
        if cur and i == cur[-1] + 1:
            cur.append(i)
        else:
            if len(cur) >= 2:
                runs.append(cur)
            cur = [i]
    if len(cur) >= 2:
        runs.append(cur)
    print(f"{path.name}: {n} frames, median luma {base:.0f}")
    for r in runs:
        print(f"  dark (countdown) {r[0]:5d}s -> {r[-1]:5d}s  "
              f"({len(r)}s)  mid={r[len(r) // 2]}s")
    if not runs:
        print("  no darkened window found")


if __name__ == "__main__":
    main()

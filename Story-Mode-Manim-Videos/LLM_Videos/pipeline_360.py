"""Render one act of Chapter 2 Episode 1 to the house 360p deliverable.

Follows the established convention of the Chapter 2 maths topics exactly
(``Chapter 2 - Linear Equations in One Variable/pipeline_360.py``):

  1. render 640x360 @ 30 fps into the short media dir ``D:\\m3`` (the topic
     paths are long enough to hit Windows' MAX_PATH),
  2. copy the movie and its ground-truth ``*.real.srt`` back into this
     folder's ``media/videos/<stem>/360p30/``,
  3. ``verify_sync.py``       -- captions sit inside speech; every speech
     block is captioned; the SRT belongs to this render,
  4. ``verify_captions.py``   -- the SRT reproduces the narration word for word,
  5. burn the captions in with ffmpeg, keeping the audio (``-c:a copy``),
  6. publish the captioned movie plus its ``.srt`` into ``final_videos/``.

Usage:
    python pipeline_360.py act1_scenes Chapter2Act1
    python pipeline_360.py act1_scenes Chapter2Act1 act2_scenes Chapter2Act2
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"D:\Manim-Short-Videos")
PY = ROOT / ".venv" / "Scripts" / "python.exe"
M3 = Path(r"D:\m3")
HERE = Path(__file__).resolve().parent
FINALS = HERE / "final_videos"

# The series' single caption style.  libass scales it with the video height,
# so the same string serves the 360p cut and any later 1080p master.
FORCE_STYLE = (
    "FontSize=9.5,Bold=1,PrimaryColour=&HFFFFFF&,"
    "OutlineColour=&H80000000&,BackColour=&H80000000&,BorderStyle=3,"
    "Outline=1.6,Shadow=0,MarginV=10,MarginL=43,MarginR=10"
)


def run(cmd: list, cwd: Path, tag: str) -> int:
    print(f"\n>>> [{tag}] {' '.join(str(c) for c in cmd)}", flush=True)
    p = subprocess.run(cmd, cwd=str(cwd))
    print(f"<<< [{tag}] exit {p.returncode}", flush=True)
    return p.returncode


def one(module: str, cls: str) -> int:
    # `manim render` needs a file path; `verify_captions.py` needs an import
    # name.  Accept either spelling on the command line and derive both.
    module_file = module if module.endswith(".py") else f"{module}.py"
    stem = Path(module_file).stem
    print(f"\n{'=' * 72}\n{cls}   ({module_file})\n{'=' * 72}", flush=True)

    if run([PY, "-m", "manim", "render", "--resolution", "640,360",
            "--fps", "30", "--media_dir", str(M3), "--disable_caching",
            module_file, cls], HERE, "render") != 0:
        return 1

    out = M3 / "videos" / stem / "360p30"
    movie, srt_src = out / f"{cls}.mp4", out / f"{cls}.real.srt"
    for p in (movie, srt_src):
        if not p.exists():
            print(f"MISSING after render: {p}")
            return 1

    dest = HERE / "media" / "videos" / stem / "360p30"
    dest.mkdir(parents=True, exist_ok=True)
    srt = dest / f"{cls}.real.srt"
    shutil.copy2(movie, dest / movie.name)
    shutil.copy2(srt_src, srt)
    shutil.copy2(srt_src, dest / "real.srt")
    # the voice cache must not be mistaken for a second source of truth
    print(f"copied back to {dest}")

    rc_sync = run([PY, ROOT / "verify_sync.py", dest / movie.name, srt],
                  HERE, "verify_sync")
    rc_caps = run([PY, ROOT / "verify_captions.py", HERE / module_file, stem,
                   "NARRATION", srt], HERE, "verify_captions")

    captioned = dest / f"{cls}_captioned.mp4"
    if run(["ffmpeg", "-y", "-i", movie.name, "-vf",
            f"subtitles={srt.name}:force_style='{FORCE_STYLE}'",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-c:a", "copy", captioned.name],
           dest, "burn") != 0:
        return 1

    FINALS.mkdir(exist_ok=True)
    shutil.copy2(captioned, FINALS / captioned.name)
    stale = FINALS / f"{cls}.srt"
    if stale.exists():
        stale.unlink()
    shutil.copy2(srt, FINALS / f"{cls}_captioned.srt")
    print(f"final_videos <- {captioned.name} + {cls}_captioned.srt")

    print(f"\nRESULT {cls}: verify_sync={rc_sync} verify_captions={rc_caps} "
          f"captioned={captioned.name}")
    return 0 if (rc_sync == 0 and rc_caps == 0) else 1


def main() -> int:
    args = sys.argv[1:]
    if not args or len(args) % 2:
        print(__doc__)
        return 2
    worst = 0
    order = list(zip(args[0::2], args[1::2]))
    for module, cls in order:
        worst = max(worst, one(module, cls))
    print(f"\n{pipeline_report(order, worst)}")
    return worst


def pipeline_report(order, worst: int) -> str:
    lines = ["=" * 72, "PIPELINE SUMMARY", "=" * 72]
    for module, cls in order:
        stem = Path(module).stem
        p = HERE / "final_videos" / f"{cls}_captioned.mp4"
        state = "ok" if p.exists() else "MISSING"
        size = f"{p.stat().st_size / 1e6:.1f} MB" if p.exists() else "-"
        lines.append(f"  {cls:<16} {state:<8} {size:>10}   ({stem})")
    lines.append(f"\noverall: {'PASS' if worst == 0 else 'REVIEW'}")
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())

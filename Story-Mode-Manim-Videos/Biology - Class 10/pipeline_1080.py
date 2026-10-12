"""Render one topic's 1080p60 master of this chapter.

This chapter's `final_videos\\` holds the 360p cut of each story; the 1080p60
master is the version the series delivers at full resolution, so it is written
to `final_videos\\1080p\\` and never clobbers the 360p files.

Steps, all logged (the same sequence as the Chapter 3 quadrilaterals master):

  1. render at 1920x1080 / 60 fps into the short media dir D:\\m3 (MAX_PATH
     safety -- the topic paths are long),
  2. copy the movie + its ground-truth SRT into the topic's media dir,
  3. verify_sync.py and verify_captions.py on the fresh cut,
  4. burn the captions in with ffmpeg -> *_captioned.mp4,
  5. copy the captioned master + .srt into
     "Class 6 - Chapter 3 - Playing with Numbers\\final_videos\\1080p\\".

Usage (from this chapter folder):
    python pipeline_1080.py <topic-folder> <module.py> <Class>
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
FINALS = HERE / "final_videos" / "1080p"

# libass scales the style with the video height, so the series' single caption
# style is used for the 360p cut and the 1080p master alike -- the same string
# as Chapter 3's pipeline_360.py / pipeline_1080.py.
FORCE_STYLE = (
    "FontSize=9.5,Bold=1,PrimaryColour=&HFFFFFF&,"
    "OutlineColour=&H80000000&,BackColour=&H80000000&,BorderStyle=3,"
    "Outline=1.6,Shadow=0,MarginV=10,MarginL=43,MarginR=10"
)


def run(cmd: list[str], cwd: Path, tag: str) -> int:
    print(f"\n>>> [{tag}] {' '.join(str(c) for c in cmd)}", flush=True)
    p = subprocess.run(cmd, cwd=str(cwd))
    print(f"<<< [{tag}] exit {p.returncode}", flush=True)
    return p.returncode


def main() -> int:
    topic = (HERE / sys.argv[1]).resolve()
    module = sys.argv[2]
    cls = sys.argv[3]
    stem = Path(module).stem

    # 1) render the master
    if run([PY, "-m", "manim", "render", "--resolution", "1920,1080",
            "--fps", "60", "--media_dir", str(M3), module, cls],
           topic, "render") != 0:
        return 1

    out = M3 / "videos" / stem / "1080p60"
    movie = out / f"{cls}.mp4"
    srt_src = out / f"{cls}.real.srt"
    for p in (movie, srt_src):
        if not p.exists():
            print(f"MISSING after render: {p}")
            return 1

    # 2) copy back into the topic's media dir
    dest = topic / "media" / "videos" / stem / "1080p60"
    dest.mkdir(parents=True, exist_ok=True)
    srt = dest / f"{cls}.real.srt"
    shutil.copy2(movie, dest / movie.name)
    shutil.copy2(srt_src, srt)
    shutil.copy2(srt_src, dest / "real.srt")
    print(f"copied back to {dest}")

    # 3) verifiers
    rc_sync = run([PY, ROOT / "verify_sync.py", dest / movie.name, srt],
                  topic, "verify_sync")
    rc_caps = run([PY, ROOT / "verify_captions.py", topic / module, stem,
                   "NARRATION", srt], topic, "verify_captions")

    # 4) burn the captions (libass scales them to the 1080p height)
    captioned = dest / f"{cls}_captioned.mp4"
    if run(["ffmpeg", "-y", "-i", movie.name, "-vf",
            f"subtitles={srt.name}:force_style='{FORCE_STYLE}'",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-c:a", "copy", captioned.name],
           dest, "burn") != 0:
        return 1

    # 5) the chapter's 1080p masters folder
    FINALS.mkdir(parents=True, exist_ok=True)
    shutil.copy2(captioned, FINALS / captioned.name)
    stale = FINALS / f"{cls}.srt"
    if stale.exists():
        stale.unlink()
    shutil.copy2(srt, FINALS / f"{cls}_captioned.srt")
    print(f"final_videos\\1080p <- {captioned.name} + {cls}_captioned.srt")

    print(f"\nRESULT {topic.name}: verify_sync={rc_sync} "
          f"verify_captions={rc_caps} master={captioned.name}")
    return 0 if (rc_sync == 0 and rc_caps == 0) else 1


if __name__ == "__main__":
    sys.exit(main())

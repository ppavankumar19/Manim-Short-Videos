"""Re-cut one topic's 360p deliverable after an on-screen change.

Steps, all logged:

  1. render at 360p30 into the short media dir D:\\m3 (MAX_PATH safety),
  2. copy the movie + its ground-truth SRT back into the topic's media dir
     (the audit and the frame sweeps read them from there),
  3. verify_sync.py  -- captions sit inside speech, every speech block is
     captioned, the SRT belongs to this render,
  4. verify_captions.py -- the SRT reproduces the narration word for word,
  5. burn the captions in with ffmpeg -> *_captioned.mp4,
  6. copy the captioned movie and its .srt into finals_360\\.

Usage:
    python pipeline_360.py <topic-folder> <module.py> <Class>
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
FINALS = HERE / "finals_360"

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

    # 1) render
    if run([PY, "-m", "manim", "render", "--resolution", "640,360",
            "--fps", "30", "--media_dir", str(M3), module, cls],
           topic, "render") != 0:
        return 1

    out = M3 / "videos" / stem / "360p30"
    movie = out / f"{cls}.mp4"
    srt_src = out / f"{cls}.real.srt"
    for p in (movie, srt_src):
        if not p.exists():
            print(f"MISSING after render: {p}")
            return 1

    # 2) copy back into the topic's media dir
    dest = topic / "media" / "videos" / stem / "360p30"
    dest.mkdir(parents=True, exist_ok=True)
    srt = dest / f"{cls}.real.srt"
    try:
        shutil.copy2(movie, dest / movie.name)
        shutil.copy2(srt_src, srt)
        shutil.copy2(srt_src, dest / "real.srt")
    except OSError:                       # long path: use the \\?\ form
        src = f"\\\\?\\{movie}"
        shutil.copyfile(src, f"\\\\?\\{dest / movie.name}")
        shutil.copyfile(f"\\\\?\\{srt_src}", f"\\\\?\\{srt}")
    print(f"copied back to {dest}")

    # 3) + 4) verifiers
    rc_sync = run([PY, ROOT / "verify_sync.py", dest / movie.name, srt],
                  topic, "verify_sync")
    rc_caps = run([PY, ROOT / "verify_captions.py", topic / module, stem,
                   "NARRATION", srt], topic, "verify_captions")

    # 5) burn the captions
    captioned = dest / f"{cls}_captioned.mp4"
    if run(["ffmpeg", "-y", "-i", movie.name, "-vf",
            f"subtitles={srt.name}:force_style='{FORCE_STYLE}'",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-c:a", "copy", captioned.name],
           dest, "burn") != 0:
        return 1

    # 6) finals -- the SRT keeps the captioned file's name, and any copy from
    #    an earlier cut is removed so a stale caption file can never linger
    #    next to the new movie
    FINALS.mkdir(exist_ok=True)
    shutil.copy2(captioned, FINALS / captioned.name)
    stale = FINALS / f"{cls}.srt"
    if stale.exists():
        stale.unlink()
    shutil.copy2(srt, FINALS / f"{cls}_captioned.srt")
    print(f"finals <- {captioned.name} + {cls}_captioned.srt")

    print(f"\nRESULT {topic.name}: verify_sync={rc_sync} "
          f"verify_captions={rc_caps} captioned={captioned.name}")
    return 0 if (rc_sync == 0 and rc_caps == 0) else 1


if __name__ == "__main__":
    sys.exit(main())

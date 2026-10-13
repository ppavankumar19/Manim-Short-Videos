"""Render every beat of the Kepler short and stitch them into one file.

    ..\.venv\Scripts\python.exe render_all.py            # render, then join
    ..\.venv\Scripts\python.exe render_all.py --only 02  # one beat
    ..\.venv\Scripts\python.exe render_all.py --join     # join what is there

Output: `kepler_short.mp4`, 1920x1080 at 60 fps, in this folder.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PYTHON = sys.executable
OUT = os.path.join(HERE, "kepler_short.mp4")

BEATS = [
    ("scene_01_kepler.py", "Scene01Kepler"),
    ("scene_02_nesting.py", "Scene02Nesting"),
    ("scene_03_ratios.py", "Scene03Ratios"),
    ("scene_04_ven.py", "Scene04Ven"),
    ("scene_05_tycho.py", "Scene05Tycho"),
    ("scene_06_misfit.py", "Scene06Misfit"),
    ("scene_07_laws.py", "Scene07Laws"),
    ("scene_08_outro.py", "Scene08Outro"),
]


def rendered_path(module: str, scene: str) -> str:
    return os.path.join(HERE, "media", "videos", module[:-3], "1080p60",
                        f"{scene}.mp4")


def render(module: str, scene: str, *, attempts: int = 3) -> None:
    """Render one beat, retrying a failed edge-tts fetch.

    Narration is synthesised over the network on the first render of a beat,
    and that call drops often enough to break an unattended eight-beat run.
    A successful synthesis is cached, so a retry costs only the beat that
    failed.
    """
    print(f"--- {scene}", flush=True)
    for attempt in range(1, attempts + 1):
        done = subprocess.run(
            [PYTHON, "-m", "manim", "render", "-qh", module, scene], cwd=HERE,
        )
        if done.returncode == 0:
            return
        print(f"    {scene} failed (attempt {attempt}/{attempts})", flush=True)
    raise SystemExit(f"{scene} would not render")


def has_audio(path: str) -> bool:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a",
         "-show_entries", "stream=codec_type", "-of", "csv=p=0", path],
        capture_output=True, text=True,
    )
    return "audio" in out.stdout


def with_silence(path: str) -> str:
    """A copy of a silent beat that carries an empty audio track.

    The outro has no narration, so manim writes it video-only -- and the
    concat demuxer will not line up a set of inputs whose stream layouts
    differ.  Giving it silence of its own keeps every beat the same shape.
    """
    padded = path.replace(".mp4", "_silent.mp4")
    subprocess.run(
        ["ffmpeg", "-y", "-i", path, "-f", "lavfi",
         "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
         "-shortest", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", padded],
        check=True, capture_output=True,
    )
    return padded


def join(paths: list[str]) -> None:
    """Concatenate the beats.

    Re-encoded rather than stream-copied: the beats carry per-scene audio at
    whatever length edge-tts produced, and a concat demuxer copy leaves the
    audio and video timestamps drifting apart across eight joins.
    """
    paths = [p if has_audio(p) else with_silence(p) for p in paths]

    listing = os.path.join(HERE, "media", "_beats.txt")
    with open(listing, "w", encoding="utf-8") as fh:
        for p in paths:
            fh.write(f"file '{p.replace(chr(92), '/')}'\n")

    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listing,
         "-r", "60", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", OUT],
        cwd=HERE, check=True,
    )
    print(f"\nWrote {OUT}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="render just the beat with this number, e.g. 02")
    ap.add_argument("--join", action="store_true",
                    help="skip rendering and only stitch what is on disk")
    args = ap.parse_args()

    beats = BEATS
    if args.only:
        beats = [b for b in BEATS if f"scene_{args.only}_" in b[0]]
        if not beats:
            raise SystemExit(f"no beat matches {args.only!r}")

    if not args.join:
        for module, scene in beats:
            render(module, scene)

    paths = [rendered_path(m, s) for m, s in BEATS]
    missing = [p for p in paths if not os.path.exists(p)]
    if missing:
        print("not joining, these beats are not rendered yet:")
        for p in missing:
            print("  ", os.path.basename(p))
        return
    join(paths)


if __name__ == "__main__":
    main()

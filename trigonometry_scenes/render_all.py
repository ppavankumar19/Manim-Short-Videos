"""Render all 10 scenes individually and combine into one final video."""
from __future__ import annotations

import os
import subprocess
import sys
import json

SCENES_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCENES_DIR)
MANIM_EXE = os.path.join(PROJECT_DIR, ".venv", "Scripts", "manim.exe")
MIKTEX_BIN = r"D:\MiKTeX\miktex\bin\x64"
OUTPUT_DIR = os.path.join(SCENES_DIR, "renders")
TIMESTAMPS_FILE = os.path.join(SCENES_DIR, "timestamps.txt")

SCENES = [
    ("scene_00_intro.py", "Scene00Intro"),
    ("scene_01_title.py", "Scene01Title"),
    ("scene_02_hook.py", "Scene02Hook"),
    ("scene_03_triangle.py", "Scene03Triangle"),
    ("scene_04_space.py", "Scene04Space"),
    ("scene_05_ratio.py", "Scene05Ratio"),
    ("scene_06_similar.py", "Scene06Similar"),
    ("scene_07_formal.py", "Scene07Formal"),
    ("scene_08_working.py", "Scene08Working"),
    ("scene_09_example.py", "Scene09Example"),
    ("scene_10_summary.py", "Scene10Summary"),
    ("scene_11_overview.py", "Scene11Overview"),
]

BEAT_NAMES = [
    "Intro (Why)", "Title", "Hook", "Triangle", "In Space", "Ratio",
    "Similarity", "Formal", "Working", "Example", "Summary", "Overview",
]


def get_duration(video_path: str) -> float:
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json",
             "-show_format", video_path],
            capture_output=True, text=True,
        )
        info = json.loads(result.stdout)
        return float(info["format"]["duration"])
    except Exception:
        return 0.0


def fmt_time(seconds: float) -> str:
    m, s = divmod(seconds, 60)
    return f"{int(m)}:{s:05.2f}"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    env = os.environ.copy()
    env["PATH"] = MIKTEX_BIN + ";" + env.get("PATH", "")

    video_files = []
    durations = []

    print("=" * 60)
    print("  Heights and Distances — Scene Renderer")
    print("=" * 60)

    for i, (scene_file, scene_class) in enumerate(SCENES, 1):
        scene_path = os.path.join(SCENES_DIR, scene_file)
        print(f"\n[{i:2d}/{len(SCENES)}] Rendering {scene_class}...")

        result = subprocess.run(
            [MANIM_EXE, "render", "-qh", "--fps", "60", scene_path, scene_class],
            env=env, cwd=SCENES_DIR, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
        )

        if result.returncode != 0:
            print(f"  ERROR rendering {scene_file}:")
            print(result.stderr[-500:] if result.stderr else "No error output")
            sys.exit(1)

        media_dir = os.path.join(
            SCENES_DIR, "media", "videos", scene_file.replace(".py", ""), "1080p60",
        )
        video_path = os.path.join(media_dir, f"{scene_class}.mp4")

        if not os.path.exists(video_path):
            for root, dirs, files in os.walk(os.path.join(SCENES_DIR, "media")):
                for f in files:
                    if f == f"{scene_class}.mp4":
                        video_path = os.path.join(root, f)
                        break

        if not os.path.exists(video_path):
            print(f"  ERROR: Output video not found for {scene_class}")
            sys.exit(1)

        dur = get_duration(video_path)
        durations.append(dur)
        video_files.append(video_path)
        print(f"  Done: {dur:.2f}s — {video_path}")

    print(f"\n{'=' * 60}")
    print("  Writing timestamps...")

    cumulative = 0.0
    with open(TIMESTAMPS_FILE, "w", encoding="utf-8") as f:
        f.write("Heights and Distances — Scene Timestamps\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"{'Beat':<6} {'Name':<16} {'Start':>8} {'End':>8} {'Duration':>10}\n")
        f.write("-" * 70 + "\n")
        for i, (name, dur) in enumerate(zip(BEAT_NAMES, durations), 1):
            start = cumulative
            cumulative += dur
            f.write(f"{i:<6d} {name:<16s} {fmt_time(start):>8s} "
                    f"{fmt_time(cumulative):>8s} {dur:>8.2f}s\n")
        f.write("-" * 70 + "\n")
        f.write(f"\nTotal duration: {fmt_time(cumulative)} ({cumulative:.2f}s)\n")
        f.write(f"Total scenes: {len(durations)}\n")
        f.write(f"\nIndividual scene MP4s in: {OUTPUT_DIR}\n")

    print(f"  Saved: {TIMESTAMPS_FILE}")

    import shutil
    for i, (vf, (_, scene_class)) in enumerate(zip(video_files, SCENES), 1):
        dest = os.path.join(OUTPUT_DIR, f"{i:02d}_{scene_class}.mp4")
        if os.path.abspath(vf) != os.path.abspath(dest):
            shutil.copy2(vf, dest)

    concat_file = os.path.join(OUTPUT_DIR, "concat_list.txt")
    with open(concat_file, "w", encoding="utf-8") as f:
        for i, (_, scene_class) in enumerate(SCENES, 1):
            f.write(f"file '{i:02d}_{scene_class}.mp4'\n")

    final_output = os.path.join(OUTPUT_DIR, "HeightsAndDistances_FULL.mp4")
    print("\n  Concatenating into final video...")

    result = subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
         "-i", concat_file, "-c", "copy", final_output],
        capture_output=True, text=True,
    )

    if result.returncode == 0:
        final_dur = get_duration(final_output)
        print(f"  Final video: {final_output}")
        print(f"  Duration: {fmt_time(final_dur)}")
    else:
        print(f"  ffmpeg concat failed — individual scenes are still in {OUTPUT_DIR}")
        if result.stderr:
            print(result.stderr[-300:])

    print(f"\n{'=' * 60}")
    print(f"  All done! {len(video_files)} scenes rendered.")
    print(f"  Timestamps: {TIMESTAMPS_FILE}")
    print(f"  Renders: {OUTPUT_DIR}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()

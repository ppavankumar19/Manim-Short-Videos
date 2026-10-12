"""Burn the series caption style into the eight 1080p60 Chapter-2 masters.

Run from the Story-Mode-Manim-Videos folder:
    python ../.venv/Scripts/python.exe burn_1080_all.py
"""
from __future__ import annotations

import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAPTER = "Chapter 2 - Linear Equations in One Variable"

STYLE = ("subtitles={srt}:force_style='FontSize=9.5,Bold=1,"
         "PrimaryColour=&HFFFFFF&,OutlineColour=&H80000000&,"
         "BackColour=&H80000000&,BorderStyle=3,Outline=1.6,Shadow=0,"
         "MarginV=10,MarginL=43,MarginR=10'")

TOPICS = [
    ("Linear-Equations", "equation_anatomy_story",
     "EquationAnatomyStory"),
    ("Solving-Simple-Equations", "equation_solving_story",
     "EquationSolvingStory"),
    ("Linear-Equation-Word-Problems", "from_words_to_equations_story",
     "FromWordsToEquationsStory"),
    ("Linear-Equations-with-Variables-on-Both-Sides", "variables_both_sides_story",
     "VariablesBothSidesStory"),
    ("Two-Digit-Number-Riddles", "two_digit_puzzles_story",
     "TwoDigitPuzzlesStory"),
    ("Boats-and-Streams-Problems", "upstream_downstream_story",
     "UpstreamDownstreamStory"),
    ("Applications-of-Angles-and-Parallel-Lines", "geometry_angles_story", "GeometryAnglesStory"),
    ("Solving-Equations-with-Fractions", "fractions_clearing_story",
     "FractionsClearingStory"),
]


def main() -> None:
    for folder, module, cls in TOPICS:
        d = HERE / CHAPTER / folder / "media" / "videos" / module / "1080p60"
        src = d / f"{cls}.mp4"
        srt = d / f"{cls}.real.srt"
        out = d / f"{cls}_captioned.mp4"
        if not src.exists() or not srt.exists():
            print(f"!! missing inputs for {folder}")
            continue
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
               "-vf", STYLE.format(srt=srt.name),
               "-c:v", "libx264", "-preset", "fast", "-crf", "18",
               "-pix_fmt", "yuv420p", "-c:a", "copy", str(out)]
        p = subprocess.run(cmd, cwd=d)
        size = out.stat().st_size / 1e6 if out.exists() else 0
        print(f"{'ok ' if p.returncode == 0 else '!! '}{folder:46s} "
              f"{size:6.1f} MB")


if __name__ == "__main__":
    main()

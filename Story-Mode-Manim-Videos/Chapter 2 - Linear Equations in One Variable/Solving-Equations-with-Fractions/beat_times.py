"""Print the wall-clock span of every narration piece from the real SRT."""
from __future__ import annotations

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRT = (HERE / "media" / "videos" / "fractions_clearing_story" / "360p30"
       / "FractionsClearingStory.real.srt")

ANCHORS = [
    ("title", "today we clear the fractions"),
    ("scene1", "here is an equation with fractions"),
    ("scene2", "let's see what removing"),
    ("scene3", "now let's do exactly that"),
    ("scene4", "the fractions are gone so now"),
    ("scene5", "let's use the shortcut"),
    ("scene6", "now we finish it"),
    ("scene7", "fractions also appear"),
    ("scene8", "so which method should you use"),
    ("scene9_setup", "your turn the third part"),
    ("scene9_reveal", "the denominators are three and five"),
    ("scene10", "let's summarise"),
]


def norm(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def parse_srt(path: Path):
    cues = []
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8").strip()):
        lines = [ln for ln in block.splitlines() if ln.strip()]
        if len(lines) < 3:
            continue
        m = re.match(r"(\d+):(\d+):(\d+),(\d+)", lines[1])
        if not m:
            continue
        h, mi, s, ms = (int(x) for x in m.groups())
        start = h * 3600 + mi * 60 + s + ms / 1000
        cues.append((start, " ".join(lines[2:])))
    return cues


def main() -> None:
    cues = parse_srt(SRT)
    marks = []
    for name, anchor in ANCHORS:
        a = norm(anchor)
        found = None
        for start, text in cues:
            if a in norm(text):
                found = start
                break
        marks.append((name, found))
    for i, (name, start) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) and marks[i + 1][1] else cues[-1][0]
        print(f"{name:14s} {start:8.2f} -> {end:8.2f}   ({end - start:6.2f}s)")


if __name__ == "__main__":
    main()

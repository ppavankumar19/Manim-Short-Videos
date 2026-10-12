"""Join the four captioned acts into the single episode deliverable.

The acts render separately (so a five-minute act can be reviewed and
re-rendered without touching twenty minutes of footage).  This concatenates
them, with the chapter title card still to come, and reports the total
runtime.

Usage:
    python concat_acts.py            # build the episode file
    python concat_acts.py --check    # just report what is present
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FINALS = HERE / "final_videos"
OUT = FINALS / "Chapter2_Ep1_The_Secret_Language_of_LLMs.mp4"

ACTS = [
    ("Chapter2Act1", "01-05  why tokenisation exists"),
    ("Chapter2Act2", "06-08  inside the tokenizer"),
    ("Chapter2Act3", "09-12  the tokenizer experiment"),
    ("Chapter2Act4", "13-15  the token budget and the bridge"),
]


def duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        capture_output=True, text=True).stdout.strip()
    try:
        return float(out)
    except ValueError:
        return 0.0


def main() -> int:
    if "--check" in sys.argv:
        total = 0.0
        print(f"{'act':<14} {'state':<9} {'duration':>9}  content")
        for cls, desc in ACTS:
            p = FINALS / f"{cls}_captioned.mp4"
            if p.exists():
                d = duration(p)
                total += d
                print(f"{cls:<14} {'ok':<9} {d:8.1f}s  {desc}")
            else:
                print(f"{cls:<14} {'MISSING':<9} {'-':>9}  {desc}")
        print(f"\ntotal {total:.1f}s  ({total / 60:.1f} min)")
        return 0 if total > 0 else 1

    missing = [c for c, _ in ACTS if not (FINALS / f"{c}_captioned.mp4").exists()]
    if missing:
        print("cannot concatenate - missing: " + ", ".join(missing))
        return 1

    listing = FINALS / "_concat_list.txt"
    listing.write_text(
        "\n".join(f"file '{c}_captioned.mp4'" for c, _ in ACTS) + "\n",
        encoding="utf-8")
    rc = subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
         "-i", listing.name, "-c", "copy", OUT.name],
        cwd=str(FINALS)).returncode
    listing.unlink(missing_ok=True)
    if rc != 0:
        print("ffmpeg concat failed")
        return rc

    d = duration(OUT)
    print(f"episode <- {OUT.name}")
    print(f"runtime {d:.1f}s  ({d / 60:.1f} min)  "
          f"{OUT.stat().st_size / 1e6:.1f} MB")
    merge_srt()
    return 0


# ------------------------------------------------------ episode subtitles ---
CUE = re.compile(
    r"(\d\d):(\d\d):(\d\d),(\d\d\d) --> (\d\d):(\d\d):(\d\d),(\d\d\d)\s*\n"
    r"(.*?)(?=\n\s*\n|\Z)", re.S)


def _secs(groups) -> float:
    h, m, s, ms = (int(x) for x in groups)
    return h * 3600 + m * 60 + s + ms / 1000.0


def _stamp(t: float) -> str:
    total = int(round(max(t, 0.0) * 1000))
    return (f"{total // 3_600_000:02d}:{(total // 60_000) % 60:02d}:"
            f"{(total // 1000) % 60:02d},{total % 1000:03d}")


def merge_srt() -> None:
    """Write one episode-level .srt, offsetting each act by its own runtime.

    The burned-in captions are already correct; this exists for the upload
    copy (soft subtitles, chapter-accurate timings).
    """
    out_lines: list[str] = []
    offset = 0.0
    n = 0
    for cls, _ in ACTS:
        srt = FINALS / f"{cls}_captioned.srt"
        movie = FINALS / f"{cls}_captioned.mp4"
        if not srt.exists() or not movie.exists():
            continue
        text = srt.read_text(encoding="utf-8")
        for m in CUE.finditer(text):
            start = _secs(m.groups()[:4]) + offset
            end = _secs(m.groups()[4:8]) + offset
            body = " ".join(m.group(9).split())
            n += 1
            out_lines += [str(n), f"{_stamp(start)} --> {_stamp(end)}", body, ""]
        offset += duration(movie)
    target = FINALS / "Chapter2_Ep1_The_Secret_Language_of_LLMs.srt"
    target.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"subtitles <- {target.name}  ({n} cues over {offset:.1f}s)")


if __name__ == "__main__":
    sys.exit(main())

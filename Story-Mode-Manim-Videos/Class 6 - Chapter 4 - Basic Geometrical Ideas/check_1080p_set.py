"""Inventory + integrity check of this chapter's 1080p caption-burned masters.

For every `final_videos\\1080p\\<Class>_captioned.mp4` this prints the delivered
facts (resolution, fps, duration, caption count) and checks that the file is a
byte-for-byte copy of the topic's own `media/videos/<stem>/1080p60/` master, so a
stale or half-copied file cannot pass unnoticed.

    python check_1080p_set.py
"""
from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
FINALS = HERE / "final_videos" / "1080p"

CUE = re.compile(r"^\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d",
                 re.M)


def probe(path: Path) -> str:
    return subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,r_frame_rate",
         "-show_entries", "format=duration,size",
         "-of", "default=nw=1:nk=1", str(path)],
        capture_output=True, text=True).stdout.split()


def md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    movies = sorted(FINALS.glob("*_captioned.mp4"))
    print(f"{len(movies)} 1080p master(s) in {FINALS}\n")
    ok = True
    for movie in movies:
        cls = movie.name.removesuffix("_captioned.mp4")
        srt = FINALS / f"{cls}_captioned.srt"
        vals = probe(movie)
        w, h, fps, dur, size = (vals[0], vals[1], vals[2], vals[3], vals[4])
        cues = len(CUE.findall(srt.read_text(encoding="utf-8"))) if srt.exists() \
            else 0
        print(f"{cls}")
        print(f"   {w}x{h} @ {fps}  {float(dur):7.2f}s  "
              f"{int(size) / 1048576:5.2f} MB  {cues} captions  "
              f"{srt.name if srt.exists() else 'NO SRT'}")
        topic_dirs = [d for d in HERE.iterdir()
                      if d.is_dir() and d.name != "final_videos"
                      and (d / "media" / "videos").exists()]
        twin = next((p for d in topic_dirs
                     for p in (d / "media" / "videos").glob(
                         f"*/1080p60/{cls}_captioned.mp4")), None)
        if twin is None:
            print("   media master: not found (only the deliverable exists)")
            ok = False
        else:
            same = md5(movie) == md5(twin)
            print(f"   media master: media/videos/{twin.parent.parent.name}/"
                  f"1080p60  identical={same}")
            ok = ok and same
    print(f"\nRESULT: {'PASS - every master is present and verified' if ok else 'REVIEW - see the lines above'}")


if __name__ == "__main__":
    main()

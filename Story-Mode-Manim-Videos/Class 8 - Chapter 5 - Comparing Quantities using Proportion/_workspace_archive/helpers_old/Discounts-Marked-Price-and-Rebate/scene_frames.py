"""Extract one full-resolution frame per scene, at the moment the scene holds.

The scene boundaries are recovered from the rendered SRT: the SRT reproduces
the narration word for word (verify_captions guarantees it), so walking the
narration keys in order assigns every cue to its scene, and the last cue of a
scene lands inside that scene's hold -- the moment the finished layout is on
the board for the viewer to read.  That is the frame to inspect for alignment,
diagram position and overlaps.

    python scene_frames.py <module.py> <Class> <srt> <out_dir> [bias]

`bias` is added to the last cue's start (default 0.6 s).
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

CUE = re.compile(
    r"(\d\d):(\d\d):(\d\d),(\d\d\d) --> (\d\d):(\d\d):(\d\d),(\d\d\d)\s*\n"
    r"(.*?)(?=\n\s*\n|\Z)", re.S)


def norm(word: str) -> str:
    return re.sub(r"[^a-z0-9]", "", word.lower())


def narration(module: Path) -> list[tuple[str, list[str]]]:
    """[(scene key, narration words)] in source order."""
    text = module.read_text(encoding="utf-8")
    body = text.split("NARRATION = {", 1)[1]
    body = body.split("\n}", 1)[0]
    out = []
    key_re = r'"(\w+)"\s*:\s*(.*?)(?=\n\s*"\w+"\s*:|\Z)'
    for m in re.finditer(key_re, body, re.S):
        key, value = m.group(1), m.group(2)
        prose = " ".join(re.findall(r'"([^"]*)"', value))
        prose = re.sub(r"<bookmark mark='[^']*'/>", " ", prose)
        words = [norm(w) for w in prose.split() if norm(w)]
        if words:
            out.append((key, words))
    return out


def cues(srt: Path):
    out = []
    for m in CUE.finditer(read_text_long(srt)):
        h, mi, s, ms = (int(m.group(1)), int(m.group(2)), int(m.group(3)),
                        int(m.group(4)))
        start = h * 3600 + mi * 60 + s + ms / 1000.0
        body = " ".join(m.group(9).split())
        out.append((start, [norm(w) for w in body.split()]))
    return out


def read_text_long(path):
    """Read a text file through the extended-length form past MAX_PATH."""
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        ext = chr(92) * 2 + "?" + chr(92)
        return Path(ext + str(path.resolve())).read_text(encoding="utf-8")


def main() -> None:
    module = Path(sys.argv[1]).resolve()
    cls = sys.argv[2]
    srt = Path(sys.argv[3]).resolve()
    out_dir = Path(sys.argv[4]).resolve()
    bias = float(sys.argv[5]) if len(sys.argv) > 5 else 0.6
    movie = srt.parent / f"{cls}.mp4"
    if not movie.exists():
        movie = srt.parent / f"{cls}_captioned.mp4"
    duration = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(movie)],
        capture_output=True, text=True).stdout.strip())

    scenes = narration(module)
    stream = cues(srt)
    flat = [w for _, words in stream for w in words]
    flat_times = [t for t, words in stream for _ in words]

    out_dir.mkdir(parents=True, exist_ok=True)
    pos = 0
    starts: list[tuple[str, float, int]] = []
    print(f"{module.stem}: {len(scenes)} scenes, {len(stream)} cues, "
          f"movie {movie.name}")
    for key, words in scenes:
        # resynchronise on the scene's opening words so a mismatch in one
        # scene cannot shift every scene after it
        probe = words[:5]
        idx = next((i for i in range(pos, len(flat) - len(probe) + 1)
                    if flat[i:i + len(probe)] == probe), pos)
        starts.append((key, flat_times[idx], idx))
        pos = idx + len(words)
    for n, (key, start, idx) in enumerate(starts):
        nxt = starts[n + 1][1] if n + 1 < len(starts) else None
        end = (nxt - bias) if nxt is not None else (duration - 1.0)
        png = out_dir / f"{n + 1:02d}_{key}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{end:.2f}",
                        "-i", str(movie), "-frames:v", "1", str(png)],
                       check=True)
        print(f"  {n + 1:02d} {key:14s} voice {start:7.2f}s -> "
              f"{'end' if nxt is None else f'{nxt:7.2f}s'}   "
              f"frame @ {end:7.2f}s  {png.name}")


if __name__ == "__main__":
    main()

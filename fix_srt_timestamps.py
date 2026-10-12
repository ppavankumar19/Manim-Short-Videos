"""Repair SRT files whose timestamps round a millisecond up to 1000.

The story-mode SRT writer formats a cue time as

    h = int(t // 3600); m = ...; s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

When a cue boundary lands within half a millisecond below a whole second the
fraction rounds to 1000 and the file gets a four-digit millisecond field, e.g.

    00:01:31,1000 --> 00:01:36,559

That is not a valid SRT timestamp.  libass still renders it when the captions are
burned in, but strict parsers -- YouTube's, and this repo's `verify_sync.py` --
drop the whole cue, so the line is reported as uncaptioned.

The repair is exact rather than a guess: the field is *milliseconds*, so ",1000"
simply carries into the next second (00:01:31,1000 -> 00:01:32,000).

    python fix_srt_timestamps.py <path> [<path> ...]        # files or folders
    python fix_srt_timestamps.py --dry <path> [...]         # report only

Folders are searched recursively for *.srt.  Files without the defect are left
untouched, so the command is safe to re-run.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

TIME = re.compile(
    r"(\d+):(\d\d):(\d\d),(\d+)\s+-->\s+(\d+):(\d\d):(\d\d),(\d+)")


def repair_line(line: str) -> tuple[str, bool]:
    """Return (line, changed) with any over-long millisecond field carried."""
    m = TIME.search(line)
    if not m:
        return line, False
    parts = [int(g) for g in m.groups()]
    if len(m.group(4)) <= 3 and len(m.group(8)) <= 3:
        return line, False

    def fmt(h: int, mi: int, s: int, ms: int) -> str:
        total = ((h * 60 + mi) * 60 + s) * 1000 + ms      # ms may exceed 999
        hh, rem = divmod(total, 3_600_000)
        mm, rem = divmod(rem, 60_000)
        ss, msec = divmod(rem, 1000)
        return f"{hh:02d}:{mm:02d}:{ss:02d},{msec:03d}"

    start = fmt(*parts[0:4])
    end = fmt(*parts[4:8])
    return (line[:m.start()] + f"{start} --> {end}" + line[m.end():], True)


def targets(args: list[str]) -> list[Path]:
    out: list[Path] = []
    for a in args:
        p = Path(a)
        if p.is_dir():
            out.extend(sorted(p.rglob("*.srt")))
        elif p.exists():
            out.append(p)
        else:
            print(f"  (no such path: {a})")
    return out


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--dry"]
    dry = "--dry" in sys.argv
    if not args:
        print(__doc__)
        return 2

    files = targets(args)
    fixed = 0
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        changed = 0
        for i, line in enumerate(lines):
            new, hit = repair_line(line)
            if hit:
                print(f"  {path.name}: {line.strip()}  ->  {new.strip()}")
                lines[i] = new
                changed += 1
        if changed and not dry:
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        fixed += 1 if changed else 0

    verb = "would repair" if dry else "repaired"
    print(f"\n{verb} {fixed} of {len(files)} SRT file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

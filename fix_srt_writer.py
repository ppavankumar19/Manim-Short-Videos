"""Make every story module's SRT writer carry a millisecond round-up correctly.

`_write_real_srt` in each story module formats cue times with

    h = int(t // 3600); m = int((t % 3600) // 60); s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

Rounding the fraction on its own can produce ``ms = 1000`` for a boundary within
half a millisecond below a whole second, and the file then carries a four-digit
millisecond field -- invalid SRT, which strict parsers drop (see
`fix_srt_timestamps.py`, which repairs the files already written).

This rewrites that formatter to round to whole milliseconds FIRST and then split,
so the carry is automatic.  The replacement keeps whatever variable names the
module used (h/m/s or hh/mm/ss) and whatever the function's parameter is called.

    python fix_srt_writer.py <path> [<path> ...]     # files or folders
    python fix_srt_writer.py --dry <path> [...]

Folders are searched recursively for *.py.  Modules whose formatter is already
carry-safe (or absent) are untouched, so the command is safe to re-run.  Each
rewritten module is compile-checked before it is written back.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DEF_FMT = re.compile(r"^(?P<ind>[ \t]*)def fmt\w*\((?P<arg>\w+)[^)]*\)[^:]*:")
RETURN = re.compile(
    r"return f\"\{(\w+):02d\}:\{(\w+):02d\}:\{(\w+):02d\},\{(\w+):03d\}\"")
BUGGY = re.compile(r"int\(round\(\(\s*(\w+)\s*-\s*int\(\s*\1\s*\)\s*\)\s*\*\s*1000"
                   r"\s*\)\)")


def patch_block(lines: list[str], start: int) -> tuple[list[str], int]:
    """Patch the `def fmt` block beginning at `start`; return (lines, changed)."""
    m = DEF_FMT.match(lines[start])
    if not m:
        return lines, 0
    ind, arg = m.group("ind"), m.group("arg")
    end = start + 1
    while end < len(lines):
        line = lines[end]
        if line.strip() and not line.startswith(ind + " "):
            break
        end += 1
    block = "\n".join(lines[start:end])
    if not BUGGY.search(block):
        return lines, 0
    names = RETURN.search(block)
    if not names:
        return lines, 0
    hh, mm, ss, ms = names.groups()

    pad = ind + "    "
    body = [
        f"{pad}# round to whole milliseconds FIRST, then split: rounding the",
        f"{pad}# fraction on its own can give ms = 1000, which writes a",
        f"{pad}# four-digit millisecond field -- invalid SRT that strict",
        f"{pad}# parsers drop.  See fix_srt_timestamps.py.",
        f"{pad}total = int(round(max(float({arg}), 0.0) * 1000))",
        f"{pad}{hh} = total // 3_600_000",
        f"{pad}{mm} = (total // 60_000) % 60",
        f"{pad}{ss} = (total // 1000) % 60",
        f"{pad}{ms} = total % 1000",
        f"{pad}return f\"{{{hh}:02d}}:{{{mm}:02d}}:{{{ss}:02d}}"
        f",{{{ms}:03d}}\"",
    ]
    return lines[:start] + [lines[start]] + body + lines[end:], 1


def patch_text(text: str) -> tuple[str, int]:
    lines = text.splitlines()
    changed = 0
    i = 0
    while i < len(lines):
        if DEF_FMT.match(lines[i]):
            lines, n = patch_block(lines, i)
            changed += n
            i += 11 if n else 1
        else:
            i += 1
    return "\n".join(lines) + ("\n" if text.endswith("\n") else ""), changed


def targets(args: list[str]) -> list[Path]:
    out: list[Path] = []
    for a in args:
        p = Path(a)
        if p.is_dir():
            out.extend(sorted(p.rglob("*.py")))
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

    files = 0
    for path in targets(args):
        if any(part in {".venv", "__pycache__", "site-packages"}
               for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if "def fmt" not in text:
            continue
        new, n = patch_text(text)
        if not n:
            continue
        if not dry:
            try:
                compile(new, str(path), "exec")
            except SyntaxError as exc:            # never write a broken module
                print(f"  !! skipped {path}: {exc}")
                continue
            path.write_text(new, encoding="utf-8")
        files += 1
        print(f"  {'would patch' if dry else 'patched'} {path}")

    verb = "would patch" if dry else "patched"
    print(f"\n{verb} {files} module(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

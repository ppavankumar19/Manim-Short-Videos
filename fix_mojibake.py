"""Repair text files that were round-tripped through the ANSI code page.

Reading a UTF-8 file with a non-UTF-8 default encoding and writing it back as
UTF-8 turns every multi-byte character into its mojibake form ("->" becomes
"a†'").  The transformation is byte-for-byte reversible: encode the mojibake
back to the code page it was decoded from, then decode those bytes as UTF-8.

    python fix_mojibake.py <path> [<path> ...]      # files or folders
    python fix_mojibake.py --dry <path> [...]
"""
from __future__ import annotations

import sys
from pathlib import Path

SUFFIXES = {".md", ".py", ".txt", ".srt"}
MARKERS = ("â€", "â†", "Ã—", "Ã¢", "Â·", "âˆ", "â‰", "Ã·", "â€”")


def repair(text: str) -> str | None:
    """Undo a UTF-8 -> ANSI -> UTF-8 round trip (the writer added a BOM)."""
    body = text.lstrip("\ufeff")
    for enc in ("cp1252", "latin-1"):
        try:
            return body.encode(enc).decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
    return None


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--dry"]
    dry = "--dry" in sys.argv
    if not args:
        print(__doc__)
        return 2
    targets: list[Path] = []
    for a in args:
        p = Path(a)
        if p.is_dir():
            targets.extend(sorted(q for q in p.rglob("*")
                                  if q.suffix in SUFFIXES))
        elif p.exists():
            targets.append(p)

    fixed = 0
    for path in targets:
        if any(part in {".venv", "__pycache__"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if not any(m in text for m in MARKERS):
            continue
        new = repair(text)
        if new is None:
            print(f"  cannot repair {path}")
            continue
        if not dry:
            path.write_text(new, encoding="utf-8")
        fixed += 1
        print(f"  {'would repair' if dry else 'repaired'} {path}")
    print(f"\n{fixed} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

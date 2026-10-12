"""Patch every generated scene_frames.py with the extended-length SRT read.

Chapter 5's topic paths are past Windows' 260-character MAX_PATH, and
scene_frames.py already failed once on the percentage topic's real SRT.  The
patch is idempotent: it inserts a `read_text_long` helper (which builds the
extended prefix without any backslash literal, so the patch itself never has to
escape one) and routes the SRT read through it.

    python _fix_scene_frames_longpath.py
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(r"D:\Manim-Short-Videos\Story-Mode-Manim-Videos")

HELPER = '''def read_text_long(path):
    """Read a text file through the extended-length form past MAX_PATH."""
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        ext = chr(92) * 2 + "?" + chr(92)
        return Path(ext + str(path.resolve())).read_text(encoding="utf-8")


'''

OLD = 'srt.read_text(encoding="utf-8")'


def main() -> None:
    for path in sorted(ROOT.rglob("scene_frames.py")):
        text = path.read_text(encoding="utf-8")
        if "read_text_long" in text:
            print(f"already patched: {path.parent.name}")
            continue
        if OLD not in text:
            print(f"no SRT read found: {path.parent.name}")
            continue
        text = text.replace(OLD, "read_text_long(srt)")
        text = text.replace("def main() -> None:", HELPER + "def main() -> None:",
                            1)
        path.write_text(text, encoding="utf-8")
        print(f"patched: {path.parent.name}")


if __name__ == "__main__":
    main()

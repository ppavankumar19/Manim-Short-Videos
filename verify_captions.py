"""Does the delivered SRT carry exactly the narration that was voiced?

Every cue in the rendered SRT must reproduce, word for word and in order, the
narration dictionary in the topic's script (bookmarks removed). This catches
caption-export bugs (dropped words, duplicated lines, a stale SRT burned in).

Usage:
    python verify_captions.py <topic_script.py> <module_name> <NarrationDict> <srt>
"""
from __future__ import annotations

import importlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(r"D:\Manim-Short-Videos")))


def norm(words):
    return [re.sub(r"[^a-z0-9]", "", w.lower()) for w in words if w.strip()]


def read_text_long(path: Path) -> str:
    """Read a text file, going through the \\\\?\\ extended form if the path is
    past the old 260-character MAX_PATH limit (the Chapter 5 topic paths are)."""
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return Path("\\\\?\\" + str(path.resolve())).read_text(encoding="utf-8")


def srt_words(path: Path) -> list[str]:
    txt = read_text_long(path)
    out = []
    for body in re.findall(r"\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d\s*\n(.*?)(?=\n\s*\n|\Z)",
                           txt, re.S):
        out += body.split()
    return out


def main() -> int:
    script_dir = Path(sys.argv[1]).resolve().parent
    module = sys.argv[2]
    narration_attr = sys.argv[3] if len(sys.argv) > 3 else "NARRATION"
    srt = Path(sys.argv[4]).resolve()

    sys.path.insert(0, str(script_dir))
    mod = importlib.import_module(module)
    narration = getattr(mod, narration_attr)

    expected = []
    for key, text in narration.items():
        cleaned = re.sub(r"<bookmark mark='[^']+'/>", " ", text)
        expected += cleaned.split()

    exp_n, got_n = norm(expected), norm(srt_words(srt))
    print(f"\n=== {module} :: {srt.name}")
    print(f"    narration words {len(exp_n)}   srt words {len(got_n)}")
    if exp_n == got_n:
        print("    RESULT: PASS - captions carry the narration word for word")
        return 0

    first = next((i for i, (a, b) in enumerate(zip(exp_n, got_n)) if a != b),
                 min(len(exp_n), len(got_n)))
    lo = max(0, first - 6)
    print(f"    MISMATCH at word {first}")
    print(f"      narration: {' '.join(exp_n[lo:first + 8])}")
    print(f"      srt      : {' '.join(got_n[lo:first + 8])}")
    extra = [w for w in got_n if w not in exp_n][:12]
    missing = [w for w in exp_n if w not in got_n][:12]
    if extra:
        print(f"      not in narration: {extra}")
    if missing:
        print(f"      missing from srt: {missing}")
    print("    RESULT: REVIEW")
    return 1


if __name__ == "__main__":
    sys.exit(main())

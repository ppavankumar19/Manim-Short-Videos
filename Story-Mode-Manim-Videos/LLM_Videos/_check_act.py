"""Count the narration budget for one act, and check bookmark sanity.

Every ``<bookmark mark='x'/>`` must be unique inside its own beat (the
tracker keys bookmarks by name, so a duplicate silently overwrites the
first) and every ``time_until_bookmark`` in the scene must reference a mark
that actually exists in that beat -- otherwise the render raises part-way
through, 20 minutes in.

Usage:  python _check_act.py act1_scenes
"""
from __future__ import annotations

import importlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

WORDS_PER_SECOND = 2.5      # measured Zephyr pace in this project


def main() -> int:
    module_name = sys.argv[1] if len(sys.argv) > 1 else "act1_scenes"
    mod = importlib.import_module(module_name)
    narration = mod.NARRATION

    total_words = 0
    total_marks = 0
    problems: list[str] = []
    print(f"=== {module_name} :: {len(narration)} beats")
    for key, text in narration.items():
        clean = re.sub(r"<bookmark\s+mark='[^']+'\s*/>", " ", text)
        words = len(clean.split())
        marks = re.findall(r"<bookmark\s+mark='([^']+)'\s*/>", text)
        dupes = {m for m in marks if marks.count(m) > 1}
        total_words += words
        total_marks += len(marks)
        flag = ""
        if dupes:
            flag = f"  DUPLICATE MARKS {sorted(dupes)}"
            problems.append(f"{key}: duplicate marks {sorted(dupes)}")
        if not marks:
            flag += "  (no bookmarks)"
        print(f"  {key:8} {words:>4} words  {len(marks)} marks{flag}")

    print(f"\ntotal words {total_words}   marks {total_marks}")
    print(f"estimated speech {total_words / WORDS_PER_SECOND:.0f}s "
          f"({total_words / WORDS_PER_SECOND / 60:.1f} min)")

    # every mark referenced in code must exist in its own beat
    src = (HERE / f"{module_name}.py").read_text(encoding="utf-8")
    beats = re.split(r"with self\.beat\(", src)
    for chunk in beats[1:]:
        m = re.match(r"""["']([^"']+)["']""", chunk)
        if m is None:
            continue
        beat_key = m.group(1)
        body = chunk.split("with self.beat(")[0]
        used = set(re.findall(r'time_until_bookmark\("([^"]+)"', body))
        declared = set(re.findall(
            r"<bookmark\s+mark='([^']+)'\s*/>", narration.get(beat_key, "")))
        missing = used - declared
        if missing:
            problems.append(f"{beat_key}: uses undeclared marks {sorted(missing)}")
            print(f"  !! {beat_key} uses {sorted(missing)} not in its narration")
        if beat_key not in narration:
            problems.append(f"{beat_key}: no narration entry")
            print(f"  !! {beat_key} has no narration entry")

    # every narration entry must actually be used by a beat
    used_keys = set(re.findall(r'with self\.beat\("([^"]+)"\)', src))
    unused = set(narration) - used_keys
    if unused:
        problems.append(f"narration entries never used: {sorted(unused)}")
        print(f"  !! narration written but never played: {sorted(unused)}")

    if problems:
        print("\nPROBLEMS:")
        for p in problems:
            print("  -", p)
        return 1
    print("\nRESULT: PASS - unique marks, every referenced mark declared")
    return 0


if __name__ == "__main__":
    sys.exit(main())

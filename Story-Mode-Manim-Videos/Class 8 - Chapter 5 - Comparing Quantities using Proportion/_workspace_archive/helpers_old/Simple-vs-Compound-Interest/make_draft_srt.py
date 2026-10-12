"""Write a draft SRT from the narration so the layout audits can run before the
first render.

The audits replay the scene against the rendered SRT (its word timings give the
per-bookmark windows).  Their *geometry* checks do not depend on the real audio:
they snapshot the visible mobjects after every play.  So a synthetic SRT, built
by laying the narration words out at a realistic speaking rate, lets a bad
layout be caught before a render is spent on it.  The real render overwrites
this file with the ground-truth SRT.

    python make_draft_srt.py
"""
from __future__ import annotations

import importlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

MODULE = "simple_vs_compound_interest_formula"
CLASS = "SimpleVsCompoundInterestFormulaStory"
WORD_SECONDS = 0.36        # the series' speech runs at roughly 2.8 words/s
LEAD_IN = 0.30
WORDS_PER_CUE = 9
BOOKMARK = re.compile(r"<bookmark[^>]*/>")

narration = importlib.import_module(MODULE).NARRATION


def fmt(t: float) -> str:
    total_ms = int(round(max(t, 0.0) * 1000))
    h, rem = divmod(total_ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main() -> None:
    # bookmarks are tags, not speech: the service never voices them
    pieces = [(key, " ".join(BOOKMARK.sub(" ", text).split()))
              for key, text in narration.items()]
    total_words = sum(len(text.split()) for _, text in pieces)

    entries: list[tuple[float, float, str]] = []
    t = LEAD_IN
    for _, text in pieces:
        chunk_words = text.split()
        for i in range(0, len(chunk_words), WORDS_PER_CUE):
            chunk = chunk_words[i:i + WORDS_PER_CUE]
            dur = max(WORD_SECONDS * len(chunk), 0.4)
            entries.append((t, t + dur, " ".join(chunk)))
            t += dur
        t += 0.35                                # the scene transition hold

    lines: list[str] = []
    for idx, (start, end, text) in enumerate(entries, 1):
        lines += [str(idx), f"{fmt(start)} --> {fmt(end)}", text, ""]

    out = (HERE / "media" / "videos" / MODULE / "360p30"
           / f"{CLASS}.real.srt")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    (out.parent / "real.srt").write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(entries)} draft cues, {total_words} words, "
          f"{t:.1f}s -> {out}")


if __name__ == "__main__":
    main()

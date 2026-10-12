"""Print the real bookmark windows of every narration piece in a story module.

The voiceover cache (``media/voiceovers/cache.json``) stores the word boundaries
returned by the TTS *service*; ``audio_offset`` is in 100 ns units.  At render
time ``synced_voice.install_synced_voiceover()`` REPLACES those boundaries with
word times re-derived from the real WAV, so the cache's times drift from what the
delivered video actually uses (observed up to ~2.8 s on one mark).  This tool
therefore retimes each piece the same way the render does -- ``speech_blocks`` +
``align_words`` on the cached WAV -- and falls back to the service times only when
the WAV is missing.  The columns printed are the times the render uses.

A ``<bookmark mark='bN'/>`` sits between two words, so its time is the start of
the word that follows it.  Printing those windows next to the words spoken inside
them makes it possible to check that each animation in a scene happens while its
phrase is actually being spoken -- a class of error the sync/overlap audit cannot
see (it only measures per-beat run-time totals).

Usage, from a topic folder:

    python <repo>/bookmark_times.py <story_module> [piece ...]

Example:

    python ../../../bookmark_times.py dot_patterns_story scene4 scene10
"""
from __future__ import annotations

import importlib
import json
import re
import sys
from pathlib import Path

MARK = re.compile(r"<bookmark mark='(b\d+)'/>")
RES = 1e7  # audio_offset units per second

_HERE = Path(__file__).resolve().parent
_ROOT = next((p for p in _HERE.parents if (p / "synced_voice.py").exists()),
             None)
if _ROOT is not None and str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
try:  # the render-time retiming helper; optional, the tool still works without
    import synced_voice  # type: ignore
except Exception:  # pragma: no cover
    synced_voice = None


def boundaries(entry: dict, cache_dir: Path) -> tuple[list[dict], str]:
    """The word boundaries the render uses: retimed from the WAV when possible,
    otherwise the service times as cached."""
    wav_name = entry.get("final_audio") or entry.get("original_audio")
    if synced_voice is not None and wav_name:
        wav = cache_dir / wav_name
        if wav.exists():
            try:
                blocks, dur = synced_voice.speech_blocks(wav)
                aligned = synced_voice.align_words(entry["input_text"], blocks,
                                                   dur)
                if aligned:
                    return aligned, "retimed(wav)"
            except Exception:
                pass
    return entry["word_boundaries"], "service(cache)"


def pieces(module_name: str) -> dict:
    sys.path.insert(0, str(Path.cwd()))
    mod = importlib.import_module(module_name)
    return getattr(mod, "NARRATION")


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        raise SystemExit(2)
    module_name, wanted = sys.argv[1], sys.argv[2:]
    cache = Path("media") / "voiceovers" / "cache.json"
    if not cache.exists():
        raise SystemExit(f"no voiceover cache at {cache.resolve()}")
    cache_dir = cache.parent
    entries = {e["input_text"]: e for e in json.loads(
        cache.read_text(encoding="utf-8"))}
    for key, text in pieces(module_name).items():
        if wanted and key not in wanted:
            continue
        entry = entries.get(text)
        if entry is None:
            print(f"{key:>14}: (no cache entry)")
            continue
        bounds, source = boundaries(entry, cache_dir)
        # The boundaries index the transcript with the tags stripped out.
        marks, stripped, consumed = [], 0, 0
        for m in MARK.finditer(text):
            stripped += m.start() - consumed
            after = [b for b in bounds if b["text_offset"] >= stripped]
            marks.append((m.group(1),
                          after[0]["audio_offset"] / RES if after else
                          bounds[-1]["audio_offset"] / RES))
            consumed = m.end()
        end = bounds[-1]["audio_offset"] / RES
        edges = [0.0] + [t for _, t in marks] + [end]
        print("=" * 72)
        print(f"{key}  (spoken {end:.2f}s, {source})")
        for i, (name, t) in enumerate(marks):
            nxt = edges[i + 2]
            words = " ".join(b["text"] for b in bounds
                             if t * RES <= b["audio_offset"] < nxt * RES)
            print(f"  {name:>4} @ {t:6.2f}s  ({nxt - t:5.2f}s)  {words}")


if __name__ == "__main__":
    main()

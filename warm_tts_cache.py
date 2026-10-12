"""Warm the *render* voiceover cache for every Chapter 4 narration piece.

A render launched with ``--media_dir D:\\m3`` resolves its voiceover cache to
``D:\\m3\\voiceovers\\cache.json``, while ``tts_precheck.py`` (run by hand, with
no media dir) writes into ``<topic>/media/voiceovers``.  Pieces that are not in
the render's own cache are re-synthesised during the render, and the Gemini
endpoint occasionally answers with a payload that has no ``content`` key
(``KeyError: 'content'``), which kills the whole render.

This script asks the service for every piece of every topic *with the render's
cache dir* and a retry loop, so a render then runs entirely from cache.

    python warm_tts_cache.py                     # the five chapter-4 topics
    python warm_tts_cache.py 2                   # just the second of those
    python warm_tts_cache.py <topic-folder> <module>   # any other topic

The two-argument form takes the topic folder and the story module name, both as
seen from the chapter folder that contains it.
"""
from __future__ import annotations

import importlib
import sys
import time
from pathlib import Path

ROOT = Path(r"D:\Manim-Short-Videos")
CHAPTER = (ROOT / "Story-Mode-Manim-Videos"
           / "Class 8 - Chapter 4 - Exponents and Powers")
CACHE = Path(r"D:\m3\voiceovers")

sys.path.insert(0, str(ROOT))

from speech_service import get_speech_service  # noqa: E402

TOPICS = [
    ("Introduction-to-Exponents-and-Powers",
     "exponents_and_base_concept_introduction"),
    ("Negative-Exponents-and-Multiplicative-Inverses",
     "negative_exponents_and_multiplicative_inverse"),
    ("Product-and-Quotient-Laws-of-Exponents",
     "laws_of_exponents_product_and_quotient"),
    ("Advanced-Laws-of-Exponents",
     "laws_of_exponents_power_product_quotient_zero"),
    ("Standard-Form-with-Powers-of-10",
     "scientific_notation_large_and_small_numbers"),
]


def custom_args(argv: list[str]) -> tuple[list[str], tuple[Path, list[tuple[str, str]]]]:
    """Return (wanted indices, (chapter-ish root, topics)) for the CLI form."""
    if len(argv) == 2:
        folder = Path(argv[0]).resolve()
        module = argv[1]
        if module.endswith(".py"):
            module = module[:-3]
        return [], (folder.parent, [(folder.name, module)])
    return [int(a) for a in argv], (CHAPTER, TOPICS)


def main() -> int:
    wanted, (root, topics) = custom_args(sys.argv[1:])
    if not wanted:
        wanted = list(range(1, len(topics) + 1))
    service = get_speech_service(cache_dir=str(CACHE))
    print(f"cache dir: {service.cache_dir}")
    bad = []
    for idx, (folder, module) in enumerate(topics, 1):
        if idx not in wanted:
            continue
        sys.path.insert(0, str(root / folder))
        narration = importlib.import_module(module).NARRATION
        print(f"=== {folder}")
        for key, text in narration.items():
            for attempt in range(1, 6):
                try:
                    data = service._wrap_generate_from_text(text)
                    words = len(data.get("word_boundaries") or [])
                    print(f"   ok {key:>6}  {words:3d} boundaries  "
                          f"{data['final_audio']}")
                    break
                except Exception as exc:            # noqa: BLE001
                    print(f"   .. {key:>6}  attempt {attempt}: "
                          f"{type(exc).__name__}: {exc}")
                    time.sleep(2 * attempt)
            else:
                bad.append((folder, key))
                print(f"   !! {key:>6}  GAVE UP")
        sys.path.pop(0)
    print("ALL CACHED" if not bad else f"FAILED: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())

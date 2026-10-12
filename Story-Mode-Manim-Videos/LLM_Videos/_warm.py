"""Pre-synthesise and time one act's narration.

Locks the Zephyr takes in before a render (Gemini TTS is stochastic), and
measures each clip so a bad key/offline machine shows up in seconds instead
of twenty minutes into a render.

Usage:  python _warm.py act1_scenes [act2_scenes ...]
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from audio import warm_narration  # noqa: E402


def main() -> int:
    names = sys.argv[1:] or ["act1_scenes"]
    for name in names:
        mod = importlib.import_module(name)
        texts = list(mod.NARRATION.values())
        print(f"\n### {name}: {len(texts)} beats")
        warm_narration(texts)
    return 0


if __name__ == "__main__":
    sys.exit(main())

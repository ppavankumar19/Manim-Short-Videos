"""Tune edge-tts rate per beat so narration matches the authored animation.

TARGETS are the summed `run_time`s in each scene file (video-first): the
animation timing is decided first, then the voice is fitted to it.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tts_tune import tune_rate
from common import NARRATION

TARGETS = {
    "greeting": 14.0,
    "word": 25.4,
    "rigid": 35.0,
    "cannot": 24.0,
    "trick": 36.01,
    "names": 21.8,
    "ratio": 31.99,
    "used": 25.31,
    "summary": 21.0,
    "thanks": 11.05,
}

if __name__ == "__main__":
    print("BEAT_RATE = {")
    for beat, target in TARGETS.items():
        rate, dur = tune_rate(NARRATION[beat], target)
        flag = "" if abs(rate - 9) <= 25 else "   # <-- far from +9%, reword"
        print(f'    "{beat}": "{rate:+d}%",  # {target:.1f}s -> {dur:.2f}s{flag}')
    print("}")

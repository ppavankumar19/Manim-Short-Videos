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
    "greeting": 11.45,
    "intro": 24.39,
    "title": 6.94,
    "hard": 28.53,
    "words": 22.0,
    "idea": 16.23,
    "rings": 28.17,
    "unroll": 31.92,
    "formula": 23.41,
    "pizza": 19.5,
    "working": 24.05,
    "example1": 18.0,
    "example2": 23.69,
    "summary": 15.0,
    "thanks": 14.42,
}

if __name__ == "__main__":
    print("BEAT_RATE = {")
    for beat, target in TARGETS.items():
        rate, dur = tune_rate(NARRATION[beat], target)
        flag = "" if abs(rate - 9) <= 25 else "   # <-- far from +9%, reword"
        print(f'    "{beat}": "{rate:+d}%",  # {target:.1f}s -> {dur:.2f}s{flag}')
    print("}")

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
    "intro": 25.0,
    "title": 5.0,
    "hook": 20.0,
    "triangle": 22.0,
    "space": 25.0,
    "ratio": 26.0,
    "similar": 21.0,
    "formal": 20.0,
    "working": 19.0,
    "example": 25.0,
    "summary": 8.0,
    "overview": 18.0,
}

if __name__ == "__main__":
    print("BEAT_RATE = {")
    for beat, target in TARGETS.items():
        rate, dur = tune_rate(NARRATION[beat], target)
        flag = "" if abs(rate - 9) <= 25 else "   # <-- far from +9%, reword"
        print(f'    "{beat}": "{rate:+d}%",  # {target:.1f}s -> {dur:.2f}s{flag}')
    print("}")

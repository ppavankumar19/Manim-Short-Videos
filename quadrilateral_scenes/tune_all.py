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
    "intro": 22.0,
    "title": 5.0,
    "family": 37.0,
    "typesa": 29.5,
    "typesb": 25.4,
    "tree": 31.4,
    "rigid": 26.0,
    "data": 19.0,
    "count": 22.5,
    "choose": 24.0,
    "sss": 21.0,
    "construct": 22.0,
    "locate": 20.0,
    "verify": 21.0,
    "summary": 8.4,
    "overview": 19.5,
}

if __name__ == "__main__":
    print("BEAT_RATE = {")
    for beat, target in TARGETS.items():
        rate, dur = tune_rate(NARRATION[beat], target)
        flag = "" if abs(rate - 9) <= 25 else "   # <-- far from +9%, reword"
        print(f'    "{beat}": "{rate:+d}%",  # {target:.1f}s -> {dur:.2f}s{flag}')
    print("}")

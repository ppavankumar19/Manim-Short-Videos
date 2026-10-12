"""Generate simple synthesised sound-effect WAVs for lesson videos."""
from __future__ import annotations

import os
import wave
import numpy as np

_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media", "sounds")


def _wav(name: str, signal: np.ndarray, sr: int = 44100) -> str:
    os.makedirs(_DIR, exist_ok=True)
    path = os.path.join(_DIR, name)
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return path
    s = (np.clip(signal, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(s.tobytes())
    return path


def _t(dur: float, sr: int = 44100):
    return np.linspace(0, dur, int(sr * dur), endpoint=False)


def pop() -> str:
    t = _t(0.1)
    return _wav("pop.wav", np.sin(2 * np.pi * 880 * t) * np.exp(-t * 35) * 0.7)


def whoosh() -> str:
    t = _t(0.25)
    freq = 300 + 500 * t / 0.25
    sig = np.sin(2 * np.pi * freq * t) * np.exp(-t * 6) * 0.4
    sig += np.random.default_rng(42).standard_normal(len(t)) * 0.03 * np.exp(-t * 10)
    return _wav("whoosh.wav", sig)


def ding() -> str:
    t = _t(0.35)
    sig = (np.sin(2 * np.pi * 1047 * t) + 0.5 * np.sin(2 * np.pi * 1568 * t))
    return _wav("ding.wav", sig * np.exp(-t * 7) * 0.5)


def success() -> str:
    t = _t(0.45)
    mid = len(t) // 2
    sig = np.zeros_like(t)
    sig[:mid] = np.sin(2 * np.pi * 523 * t[:mid]) * np.exp(-t[:mid] * 5) * 0.4
    sig[mid:] = np.sin(2 * np.pi * 784 * t[mid:]) * np.exp(-(t[mid:] - t[mid]) * 5) * 0.4
    return _wav("success.wav", sig)


def click() -> str:
    t = _t(0.04)
    return _wav("click.wav", np.sin(2 * np.pi * 2500 * t) * np.exp(-t * 90) * 0.5)


def swipe() -> str:
    t = _t(0.18)
    freq = 600 - 400 * t / 0.18
    return _wav("swipe.wav", np.sin(2 * np.pi * freq * t) * np.exp(-t * 12) * 0.5)


SFX: dict[str, str] = {}


def load_all() -> dict[str, str]:
    global SFX
    SFX = {
        "pop": pop(),
        "whoosh": whoosh(),
        "ding": ding(),
        "success": success(),
        "click": click(),
        "swipe": swipe(),
    }
    return SFX

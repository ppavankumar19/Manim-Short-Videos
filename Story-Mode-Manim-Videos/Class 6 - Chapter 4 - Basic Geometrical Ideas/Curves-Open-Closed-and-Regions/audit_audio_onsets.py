"""Where are the words, acoustically, in the rendered cut's closing paragraph?

The SRT's word times come from the TTS word boundaries.  This measures the same
region from the *audio itself* (short-time RMS on a mono 16 kHz decode), so a
reported reveal time can be compared with the moment the phrase is actually
spoken rather than with the caption clock.

    python audit_audio_onsets.py <movie> <t0> <t1>
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

SR = 16000
HOP = int(SR * 0.02)          # 20 ms resolution
FLOOR_DB = -42.0              # speech/no-speech gate


def main() -> None:
    movie, t0, t1 = Path(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
    with tempfile.TemporaryDirectory() as td:
        wav = Path(td) / "a.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}",
                        "-to", f"{t1:.3f}", "-i", str(movie), "-ac", "1",
                        "-ar", str(SR), "-f", "wav", str(wav)], check=True)
        raw = wav.read_bytes()
    x = np.frombuffer(raw[raw.index(b"data") + 8:], dtype=np.int16).astype(float)
    n = len(x) // HOP
    rms = np.sqrt((x[:n * HOP].reshape(n, HOP) ** 2).mean(axis=1)) / 32768.0
    db = 20 * np.log10(np.maximum(rms, 1e-9))
    voiced = db > FLOOR_DB
    print(f"threshold {FLOOR_DB} dB   window {HOP / SR * 1000:.0f} ms")
    print("\n-- speech runs (start .. end, seconds into the cut) --")
    i = 0
    while i < n:
        if voiced[i]:
            j = i
            while j < n and voiced[j]:
                j += 1
            if (j - i) * HOP / SR >= 0.04:
                print(f"  {t0 + i * HOP / SR:8.2f} .. {t0 + j * HOP / SR:8.2f}"
                      f"   ({(j - i) * HOP / SR:5.2f}s)"
                      f"   peak {db[i:j].max():6.1f} dB")
            i = j
        else:
            i += 1


if __name__ == "__main__":
    main()

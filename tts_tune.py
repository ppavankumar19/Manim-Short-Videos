"""Rate-tune edge-tts narration so its spoken duration matches a target.

Video-first workflow: each scene authors its animation timing as fixed
seconds first (a target duration per beat). This script generates the
narration for that beat, measures how long it actually runs, and searches
for an edge-tts `rate` percentage that lands the audio close to the target
— so when the scene later calls `self.voiceover(text=...)`, the resulting
`tracker.duration` (and therefore every `run_time=fraction*d` in the scene)
is already close to the intended pacing instead of whatever length the TTS
happened to produce by default.

Usage (importable):
    from tts_tune import tune_rate
    rate_pct, actual_seconds = tune_rate("Some narration text.", target_seconds=6.0)

Usage (CLI, for one-off checks):
    .venv/Scripts/python.exe tts_tune.py "Some narration text." 6.0
"""
from __future__ import annotations

import asyncio
import subprocess
import sys
import tempfile
from pathlib import Path

import edge_tts

VOICE = "en-IN-PrabhatNeural"
PITCH = "+0Hz"


def _rate_str(pct: int) -> str:
    return f"{pct:+d}%"


async def _synthesize(text: str, rate_pct: int, out_path: Path) -> None:
    communicate = edge_tts.Communicate(
        text, VOICE, rate=_rate_str(rate_pct), pitch=PITCH,
    )
    with open(out_path, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])


def _measure(text: str, rate_pct: int) -> float:
    with tempfile.TemporaryDirectory() as td:
        out_path = Path(td) / "probe.mp3"
        asyncio.run(_synthesize(text, rate_pct, out_path))
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(out_path)],
            capture_output=True, text=True,
        )
        return float(result.stdout.strip())


def tune_rate(
    text: str, target_seconds: float, *, base_rate: int = 9,
    tolerance: float = 0.03, max_iterations: int = 3,
) -> tuple[int, float]:
    """Search for an edge-tts rate percentage close to `target_seconds`.

    Speech duration is roughly inversely proportional to `(1 + rate/100)`,
    so each measurement gives a near-exact correction; two or three
    iterations reliably lands within `tolerance` of the target.
    """
    rate = base_rate
    duration = _measure(text, rate)

    for _ in range(max_iterations):
        if abs(duration - target_seconds) / target_seconds <= tolerance:
            break
        factor = (1 + rate / 100) * duration / target_seconds
        rate = round((factor - 1) * 100)
        duration = _measure(text, rate)

    return rate, duration


if __name__ == "__main__":
    text_arg = sys.argv[1]
    target_arg = float(sys.argv[2])
    rate_result, duration_result = tune_rate(text_arg, target_arg)
    print(f"rate={rate_result:+d}%  duration={duration_result:.2f}s  "
          f"target={target_arg:.2f}s")

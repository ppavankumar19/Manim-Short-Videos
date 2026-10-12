"""Generate individual audio files for each beat's narration using Edge TTS."""
from __future__ import annotations

import asyncio
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audios")
TIMESTAMPS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "timestamps.txt")

VOICE = "en-IN-PrabhatNeural"
RATE = "+9%"

BEAT_ORDER = [
    "intro", "title", "hook", "history", "fundamentals", "build",
    "formal", "why", "working", "example", "example2", "summary",
]


async def generate_audio(text: str, output_path: str) -> float:
    """Generate a single audio file and return its duration in seconds."""
    import edge_tts

    communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
    await communicate.save(output_path)

    # Get duration using wave module for wav, or mutagen/ffprobe for mp3
    # edge_tts saves as mp3, so we use a simple ffprobe approach
    try:
        import subprocess
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json",
             "-show_format", output_path],
            capture_output=True, text=True,
        )
        info = json.loads(result.stdout)
        return float(info["format"]["duration"])
    except Exception:
        # Fallback: estimate from file size (~16kbps for edge-tts mp3)
        size = os.path.getsize(output_path)
        return size / 2000.0


async def main():
    from common import NARRATION

    os.makedirs(AUDIO_DIR, exist_ok=True)

    timestamps = []
    cumulative = 0.0

    print(f"Generating {len(BEAT_ORDER)} audio files...\n")

    for i, beat_name in enumerate(BEAT_ORDER, 1):
        filename = f"{i:02d}_{beat_name}.mp3"
        output_path = os.path.join(AUDIO_DIR, filename)
        text = NARRATION[beat_name]

        print(f"  [{i:2d}/11] {beat_name:15s} → {filename}")
        duration = await generate_audio(text, output_path)

        start_time = cumulative
        cumulative += duration

        timestamps.append({
            "beat": i,
            "name": beat_name,
            "file": filename,
            "start": start_time,
            "end": cumulative,
            "duration": duration,
        })

        print(f"           Duration: {duration:.2f}s  |  "
              f"Timeline: {_fmt(start_time)} → {_fmt(cumulative)}")

    # Write timestamps file
    with open(TIMESTAMPS_FILE, "w", encoding="utf-8") as f:
        f.write("Area of a Circle — Scene Timestamps\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"{'Beat':<6} {'Name':<16} {'Start':>8} {'End':>8} "
                f"{'Duration':>10}  {'Audio File'}\n")
        f.write("-" * 80 + "\n")

        for t in timestamps:
            f.write(
                f"{t['beat']:<6d} {t['name']:<16s} {_fmt(t['start']):>8s} "
                f"{_fmt(t['end']):>8s} {t['duration']:>8.2f}s  {t['file']}\n"
            )

        f.write("-" * 80 + "\n")
        f.write(f"\nTotal duration: {_fmt(cumulative)} ({cumulative:.2f}s)\n")
        f.write(f"Total beats: {len(timestamps)}\n")

    print(f"\nTimestamps saved to: {TIMESTAMPS_FILE}")
    print(f"Total duration: {_fmt(cumulative)}")


def _fmt(seconds: float) -> str:
    m, s = divmod(seconds, 60)
    return f"{int(m)}:{s:05.2f}"


if __name__ == "__main__":
    asyncio.run(main())

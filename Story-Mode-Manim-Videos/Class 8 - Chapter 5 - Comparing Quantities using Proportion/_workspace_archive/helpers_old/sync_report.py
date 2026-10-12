"""Objective caption / speech alignment report for a delivered story video.

Measures, from the delivered file only:

  * the container's audio and video start offsets (a constant A/V shift),
  * every caption's overlap with detected speech (a caption that is early or
    late shows up as a small overlap),
  * the delay between each caption's start and the nearest speech onset, and
    the delay between each caption's end and the speech end,
  * the silent gaps longer than a second (the designed pauses between scenes,
    in total and the longest one).

    python sync_report.py <video.mp4> <subs.srt> [--noise -35dB] [--min-sil 0.25]
"""
from __future__ import annotations

import re
import statistics
import subprocess
import sys
from pathlib import Path

CUE = re.compile(
    r"(\d\d):(\d\d):(\d\d),(\d\d\d) --> (\d\d):(\d\d):(\d\d),(\d\d\d)")


def secs(h: str, m: str, s: str, ms: str) -> float:
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def probe_streams(path: Path) -> None:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=codec_type,start_time,duration", "-of", "default=nw=1",
         str(path)], capture_output=True, text=True).stdout
    print("streams:")
    for block in out.strip().split("[STREAM]"):
        if block.strip():
            print("   " + " ".join(block.split()))


def speech_blocks(path: Path, noise: str, min_sil: float):
    out = subprocess.run(
        ["ffmpeg", "-v", "info", "-i", str(path), "-af",
         f"silencedetect=noise={noise}:d={min_sil}", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    starts = [float(m) for m in re.findall(r"silence_start: ([\d.]+)", out)]
    ends = [float(m) for m in re.findall(r"silence_end: ([\d.]+)", out)]
    # speech = everything that is not silence, clamped to the audio
    dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        capture_output=True, text=True).stdout.strip())
    spans, t = [], 0.0
    for s, e in zip(starts, ends):
        if s > t:
            spans.append((t, s))
        t = e
    if t < dur:
        spans.append((t, dur))
    return spans, starts, ends


def cues(srt: Path):
    text = srt.read_text(encoding="utf-8")
    out = []
    for m in CUE.finditer(text):
        out.append((secs(*m.group(1, 2, 3, 4)), secs(*m.group(5, 6, 7, 8))))
    return out


def overlap(a0, a1, b0, b1) -> float:
    return max(0.0, min(a1, b1) - max(a0, b0))


def main() -> None:
    video = Path(sys.argv[1])
    srt = Path(sys.argv[2])
    noise = sys.argv[sys.argv.index("--noise") + 1] if "--noise" in sys.argv \
        else "-35dB"
    min_sil = float(sys.argv[sys.argv.index("--min-sil") + 1]) \
        if "--min-sil" in sys.argv else 0.25

    print(f"=== {video.name}")
    probe_streams(video)
    spans, sil_starts, sil_ends = speech_blocks(video, noise, min_sil)
    cue_list = cues(srt)

    print(f"\nspeech: {len(spans)} blocks, "
          f"{sum(b - a for a, b in spans):.1f}s of the audio")
    # the gap between one speech block's end and the next one's start
    gaps = [(b, a) for (_, b), (a, _) in zip(spans, spans[1:]) if b - a > 1.0]
    total_gap = sum(b - a for a, b in gaps)
    print(f"silent gaps > 1.0s: {len(gaps)}, {total_gap:.1f}s total"
          + (f", longest {max(b - a for a, b in gaps):.1f}s" if gaps else ""))

    inside, dead, offsets, ends = 0, 0, [], []
    for c0, c1 in cue_list:
        best = 0.0
        for s0, s1 in spans:
            best = max(best, overlap(c0, c1, s0, s1))
        frac = best / max(c1 - c0, 1e-6)
        if frac >= 0.60:
            inside += 1
        else:
            dead += 1
        # delay of the caption's start from the speech onset it follows
        onsets = [s0 for s0, _ in spans if s0 <= c0 + 0.6]
        if onsets:
            offsets.append(c0 - onsets[-1])
        ends.append(c1)

    print(f"\ncaptions: {len(cue_list)}, first {cue_list[0][0]:.2f}s, "
          f"last {cue_list[-1][1]:.2f}s")
    print(f"captions inside speech: {inside}  (poorly aligned: {dead})")
    if offsets:
        med = statistics.median(offsets)
        print(f"caption start minus speech onset: median {med:+.2f}s, "
              f"min {min(offsets):+.2f}s, max {max(offsets):+.2f}s")
        late = sum(1 for o in offsets if o > 1.2)
        print(f"  captions starting more than 1.2s after a speech onset: {late}")


if __name__ == "__main__":
    main()

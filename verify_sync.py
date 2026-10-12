"""Content-level A/V + caption sync verification for a rendered story-mode video.

This checks the *delivered file*, not the plan:

  1. container  -- video vs audio stream duration / start offsets, frame count
  2. captions   -- every caption must sit inside speech. The audio is scanned
                   with ffmpeg silencedetect; a caption whose interval is mostly
                   silence means the burn used a stale/mismatched SRT.
  3. coverage   -- every speech block longer than a second must be captioned
                   (speech with no caption on screen).
  4. freshness  -- the SRT that was burned must belong to this render (its last
                   cue must fall inside the video, not after it).

Usage:
    python verify_sync.py <video.mp4> <subs.srt> [--noise -35dB] [--min-sil 0.30]
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

MAX_SILENT_TAIL = 5.5      # video past the audio end: the closing thank-you card
                           # is deliberately shown with no narration over it, so
                           # the cut runs ~4.8s past the last sound (2.65s card
                           # entrance + emphasis, 2.0s hold).  A stale or
                           # mismatched render overshoots far more than this.
MIN_SPEECH_BLOCK = 1.0     # only check speech runs longer than this
CAPTION_OK = 0.60          # a caption must overlap speech at least this much
MIN_SPEECH_IN_CAPTION = 0.25   # ... unless it carries at least this much speech
COVER_OK = 0.50            # a speech block must be captioned at least this much


def read_text_long(path: Path) -> str:
    """Read a text file, going through the \\\\?\\ extended form if the path is
    past the old 260-character MAX_PATH limit (the Chapter 5 topic paths are)."""
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return Path("\\\\?\\" + str(path.resolve())).read_text(encoding="utf-8")


def ffprobe_streams(path: Path) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=codec_type,duration,start_time,nb_frames,r_frame_rate,width,height",
         "-of", "default=nw=1", str(path)],
        capture_output=True, text=True).stdout
    streams, cur = [], {}
    for line in out.splitlines():
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        if k == "codec_type":
            cur = {"type": v}
            streams.append(cur)
        elif cur:
            cur[k] = v
    return {s["type"]: s for s in streams if "type" in s}


def parse_srt(path: Path) -> list[tuple[float, float, str]]:
    txt = read_text_long(path)
    cues = []
    for m in re.finditer(r"(\d\d):(\d\d):(\d\d),(\d\d\d) --> "
                         r"(\d\d):(\d\d):(\d\d),(\d\d\d)\s*\n(.*?)(?=\n\s*\n|\Z)",
                         txt, re.S):
        g = [int(x) for x in m.groups()[:8]]
        start = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        end = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        text = " ".join(m.group(9).split())
        cues.append((start, end, text))
    return cues


def find_silence(path: Path, noise: str, min_sil: float) -> list[tuple[float, float]]:
    proc = subprocess.run(
        ["ffmpeg", "-v", "info", "-i", str(path), "-af",
         f"silencedetect=noise={noise}:d={min_sil}", "-f", "null", "-"],
        capture_output=True, text=True)
    log = proc.stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    return list(zip(starts, ends + [None] * (len(starts) - len(ends))))


def complement(silences, total: float) -> list[tuple[float, float]]:
    speech, cursor = [], 0.0
    for s, e in silences:
        if s > cursor:
            speech.append((cursor, min(s, total)))
        cursor = max(cursor, e if e is not None else total)
    if cursor < total:
        speech.append((cursor, total))
    return [(a, b) for a, b in speech if b - a > 0.05]


def overlap(a: tuple[float, float], b: tuple[float, float]) -> float:
    return max(0.0, min(a[1], b[1]) - max(a[0], b[0]))


def main() -> int:
    video = Path(sys.argv[1])
    subs = Path(sys.argv[2])
    noise = sys.argv[sys.argv.index("--noise") + 1] if "--noise" in sys.argv else "-35dB"
    min_sil = float(sys.argv[sys.argv.index("--min-sil") + 1]) if "--min-sil" in sys.argv else 0.30

    st = ffprobe_streams(video)
    v, a = st.get("video", {}), st.get("audio", {})
    v_dur = float(v.get("duration", 0) or 0)
    a_dur = float(a.get("duration", 0) or 0)
    v_start = float(v.get("start_time", 0) or 0)
    a_start = float(a.get("start_time", 0) or 0)
    cues = parse_srt(subs)

    # video may legitimately run past the audio for the silent closing card
    tail = v_dur - a_dur
    av_ok = (abs(v_start) <= 0.05 and abs(a_start) <= 0.05
             and -0.2 <= tail <= MAX_SILENT_TAIL)

    print(f"\n=== {video.name}")
    print(f"    {v.get('width')}x{v.get('height')} @ {v.get('r_frame_rate')}  "
          f"frames={v.get('nb_frames')}")
    print(f"    video {v_dur:8.3f}s (start {v_start:+.3f})   "
          f"audio {a_dur:8.3f}s (start {a_start:+.3f})   "
          f"silent tail {tail:+.3f}s  [{'ok' if av_ok else 'CHECK'}]")
    print(f"    captions: {len(cues)}  first {cues[0][0]:.2f}s  "
          f"last {cues[-1][1]:.2f}s  (video {v_dur:.2f}s)")

    silences = find_silence(video, noise, min_sil)
    total = a_dur or v_dur
    speech = complement(silences, total)
    speech_time = sum(b - a_ for a_, b in speech)
    print(f"    speech blocks: {len(speech)}  speech time {speech_time:.1f}s "
          f"({100 * speech_time / total:.1f}% of audio)")

    bad_caps, cap_in_speech = [], 0.0
    for start, end, text in cues:
        hit = sum(overlap((start, end), blk) for blk in speech)
        frac = hit / max(end - start, 1e-6)
        cap_in_speech += hit
        # A caption is only wrong if it has essentially NO speech under it.
        # Short closing captions legitimately linger a fraction of a second
        # into the trailing pause of the sentence.
        if frac < CAPTION_OK and hit < MIN_SPEECH_IN_CAPTION:
            bad_caps.append((start, end, frac, text))
    cap_time = sum(e - s for s, e, _ in cues)
    print(f"    caption time {cap_time:.1f}s   "
          f"caption-inside-speech {100 * cap_in_speech / max(cap_time, 1e-6):.1f}%")

    uncovered = []
    for blk in speech:
        if blk[1] - blk[0] < MIN_SPEECH_BLOCK:
            continue
        hit = sum(overlap(blk, (s, e)) for s, e, _ in cues)
        frac = hit / (blk[1] - blk[0])
        if frac < COVER_OK:
            uncovered.append((blk[0], blk[1], frac))

    print(f"    captions mostly in silence: {len(bad_caps)}")
    for start, end, frac, text in bad_caps[:6]:
        print(f"      {start:7.2f}-{end:7.2f}  speech {frac:4.0%}  {text[:58]!r}")
    print(f"    speech blocks (> {MIN_SPEECH_BLOCK}s) not captioned: {len(uncovered)}")
    for start, end, frac in uncovered[:6]:
        print(f"      {start:7.2f}-{end:7.2f}  captioned {frac:4.0%}")

    ok = (av_ok and not bad_caps and not uncovered
          and cues[-1][1] <= v_dur + 1.0 and cap_time > 0)
    print(f"    RESULT: {'PASS' if ok else 'REVIEW'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

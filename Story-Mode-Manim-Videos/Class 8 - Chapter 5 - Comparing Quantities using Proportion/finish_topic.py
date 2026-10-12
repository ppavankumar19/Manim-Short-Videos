"""Finish one Chapter 5 topic: warm the TTS cache, render + burn the 360p cut,
audit the rendered cut, and sweep the frames — one command per topic.

    python finish_topic.py <topic-folder> <module.py> <Class>

Steps (all logged to <topic>/finish.log):
  1. warm_tts_cache.py <topic> <module>        (render cache, D:\\m3\\voiceovers)
  2. pipeline_360.py <topic> <module> <Class>  (render -> verify -> burn -> finals)
  3. audit_sync_overlap.py                     (real cut: sync stretch + flags)
  4. audit_clearance.py <topic> <module> <Class>
  5. audit_badge_clearance.py
  6. scene_frames.py + find_timer.py           (frame sweep + THINK clock window)

It then prints a compact report (the numbers the delivery report needs) and a
per-topic summary line, so the caller does not have to read the full logs.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"D:\Manim-Short-Videos")
PY = ROOT / ".venv" / "Scripts" / "python.exe"
HERE = Path(__file__).resolve().parent
FINALS = HERE / "final_videos"

CATEGORIES = ("TEXT-IN-TEXT", "PARTIAL", "TEXT-ON-ARROW", "TEXT-ON-SIDE",
              "TEXT-OUTSIDE-BOX", "OUT-OF-BOARD", "IN-CAPTION-BAND",
              "NEAR-BADGE", "LATEX-AS-TEXT", "EMPTY-TEXT", "OFF-CENTRE")


def run(cmd: list, cwd: Path, log) -> int:
    print(f"\n>>> {' '.join(str(c) for c in cmd)}", flush=True)
    p = subprocess.run([str(c) for c in cmd], cwd=str(cwd), capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    log.write(f"\n===== {' '.join(str(c) for c in cmd)}\n")
    log.write(p.stdout or "")
    log.write(p.stderr or "")
    print(f"<<< exit {p.returncode}", flush=True)
    return p.returncode


def probe(movie: Path) -> tuple[float, int]:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "format=duration,size", "-of", "default=nw=1:nk=1",
                          str(movie)], capture_output=True, text=True).stdout
    vals = [v for v in out.split() if v]
    return (float(vals[0]) if vals else 0.0,
            int(vals[1]) if len(vals) > 1 else 0)


def counts(text: str) -> dict[str, int]:
    out = {}
    for cat in CATEGORIES:
        n = len(re.findall(rf"\]\s+{re.escape(cat)}\s", text))
        if n:
            out[cat] = n
    return out


def main() -> int:
    topic_name, module, cls = sys.argv[1], sys.argv[2], sys.argv[3]
    topic = HERE / topic_name
    stem = Path(module).stem
    log_path = topic / "finish.log"
    with log_path.open("w", encoding="utf-8") as log:
        run([PY, ROOT / "warm_tts_cache.py", topic, module], HERE, log)
        rc = run([PY, HERE / "pipeline_360.py", topic_name, module, cls], HERE, log)
        run([PY, "audit_sync_overlap.py"], topic, log)
        run([PY, "audit_clearance.py", topic_name, module, cls], topic, log)
        run([PY, "audit_badge_clearance.py"], topic, log)
        srt = (topic / "media" / "videos" / stem / "360p30"
               / f"{cls}.real.srt")
        run([PY, "scene_frames.py", topic / f"{module}", cls, srt,
             topic / "frames360" / "chk"], topic, log)
        run([PY, "find_timer.py",
             topic / "media" / "videos" / stem / "360p30" / f"{cls}.mp4"],
            topic, log)

    text = log_path.read_text(encoding="utf-8")
    print("\n================ REPORT", topic_name)
    print(f"pipeline rc = {rc}")
    for line in text.splitlines():
        if ("RESULT" in line or "captions:" in line or "silent tail" in line
                or "speech blocks" in line or "captions mostly in silence" in line
                or "not captioned" in line or "dark (countdown)" in line):
            print("   " + line.strip())
    final = FINALS / f"{cls}_captioned.mp4"
    if final.exists():
        dur, size = probe(final)
        caps = len(re.findall(r"^\d+$", (FINALS / f"{cls}_captioned.srt")
                              .read_text(encoding="utf-8"), re.M))
        print(f"   DELIVERABLE {final.name}: {dur:.2f}s  {size} B  "
              f"{size / 1048576:.2f} MB  {caps} captions")
    else:
        print("   DELIVERABLE MISSING")
    sync = re.findall(r"^(\w+)\s+audio=\s*([\d.]+)s anim=\s*([\d.]+)s "
                      r"stretch=\s*([\d.]+)s", text, re.M)
    print("   SYNC " + " | ".join(f"{p} {a}/{n} stretch {s}" for p, a, n, s in sync))
    print("   FLAGS(sync_overlap) " + str(counts(text)))
    tight = re.search(r"(\d+) pair\(s\) closer than", text)
    online = re.search(r"(\d+) text/line collision", text)
    foreign = re.search(r"(\d+) foreign-box collision", text)
    print(f"   CLEARANCE tight={tight.group(1) if tight else '?'} "
          f"online={online.group(1) if online else '?'} "
          f"foreign={foreign.group(1) if foreign else '?'}")
    bad = [ln for ln in text.splitlines()
           if "TOO CLOSE" in ln]
    print(f"   BADGE {'all ok' if not bad else bad}")
    return rc


if __name__ == "__main__":
    sys.exit(main())

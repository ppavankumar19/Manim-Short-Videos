"""Chapter 2 (Linear Equations in One Variable) — full delivery confirmation.

For each of the eight Class-8 Chapter-2 storyboard topics it checks, from the
files on disk:

  * storyboard.md exists and names the chapter,
  * the scene script / class exist,
  * the captioned masters exist at 1080p60 and 360p30 (duration + resolution),
  * verify_sync.py  -> captions-in-silence and uncaptioned-speech counts,
  * verify_captions.py -> narration words vs SRT words,
  * the topic's own audit_sync_overlap.py -> collision / latex / bounds flags.

Run from the Story-Mode-Manim-Videos folder:
    python ../../.venv/Scripts/python.exe confirm_chapter2.py
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAPTER = "Chapter 2 - Linear Equations in One Variable"
REPO = HERE.parent
PY = REPO / ".venv" / "Scripts" / "python.exe"
VERIFY_SYNC = REPO / "verify_sync.py"
VERIFY_CAPTIONS = REPO / "verify_captions.py"

TOPICS = [
    ("1. Linear Equations",
     "Linear-Equations"),
    ("2. Solving Simple Equations",
     "Solving-Simple-Equations"),
    ("3. Linear Equation Word Problems",
     "Linear-Equation-Word-Problems"),
    ("4. Linear Equations with Variables on Both Sides",
     "Linear-Equations-with-Variables-on-Both-Sides"),
    ("5. Two-Digit Number Riddles",
     "Two-Digit-Number-Riddles"),
    ("6. Boats and Streams Problems",
     "Boats-and-Streams-Problems"),
    ("7. Applications of Angles and Parallel Lines",
     "Applications-of-Angles-and-Parallel-Lines"),
    ("8. Solving Equations with Fractions",
     "Solving-Equations-with-Fractions"),
]

ENV = dict(os.environ, PYTHONIOENCODING="utf-8")


def run(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True,
                       errors="replace")
    return (p.stdout or "") + (p.stderr or "")


def probe(path: Path) -> str:
    out = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
               "-show_entries", "stream=width,height,r_frame_rate",
               "-show_entries", "format=duration", "-of", "csv=p=0", str(path)])
    vals = ",".join(v for v in out.strip().splitlines() if v)
    return vals


def chapter_ok(folder: Path) -> str:
    sb = folder / "storyboard.md"
    if not sb.exists():
        return "missing"
    m = re.search(r"\*\*CHAPTER:\*\*\s*(.+)", sb.read_text(encoding="utf-8",
                                                          errors="replace"))
    return m.group(1).strip() if m else "untagged"


def main() -> None:
    lines = ["# Chapter 2 — Linear Equations in One Variable: confirmation",
             "",
             "| # | Topic | Storyboard | Script / class | 1080p60 | 360p30 | sync | captions | audit |",
             "|---|---|---|---|---|---|---|---|---|"]
    all_ok = True
    for label, folder_name in TOPICS:
        folder = HERE / CHAPTER / folder_name
        sb = chapter_ok(folder)
        script = next(folder.glob("*_story.py"), None) or next(
            (p for p in folder.glob("*.py")
             if p.name not in {"audit_sync_overlap.py", "sync_map.py"}
             and "probe" not in p.name and "confirm" not in p.name), None)
        cls = ""
        if script:
            m = re.search(r"^class (\w+)", script.read_text(
                encoding="utf-8", errors="replace"), re.M)
            cls = m.group(1) if m else "?"
        caps = sorted(folder.glob("media/videos/**/*_captioned.mp4"))
        by_res = {}
        for c in caps:
            res = next((part for part in c.parts if re.fullmatch(r"\d+p\d+",
                                                                 part)), "other")
            by_res.setdefault(res, c)
        hi = by_res.get("1080p60")
        lo = by_res.get("360p30")
        if not hi or not lo:
            all_ok = False

        sync_txt = ""
        cap_txt = "n/a"
        for tag, path in (("1080p60", hi), ("360p30", lo)):
            if not path:
                continue
            srt = path.with_name(path.name.replace("_captioned.mp4", ".real.srt"))
            if not srt.exists():
                srt = next(path.parent.glob("*.real.srt"), None)
            if srt and VERIFY_SYNC.exists():
                out = run([str(PY), str(VERIFY_SYNC), str(path), str(srt)])
                ok = "PASS" if "RESULT: PASS" in out else "FAIL"
                sil = re.search(r"captions mostly in silence:\s*(\d+)", out)
                unc = re.search(r"not captioned:\s*(\d+)", out)
                sync_txt += (f"{tag} {ok} (silence {sil.group(1) if sil else '?'}, "
                             f"uncaptioned {unc.group(1) if unc else '?'})<br>")
                if ok != "PASS":
                    all_ok = False
            if srt and VERIFY_CAPTIONS.exists() and script:
                out = run([str(PY), str(VERIFY_CAPTIONS), str(script),
                           script.stem, "NARRATION", str(srt)])
                m = re.search(r"narration words (\d+)\s+srt words (\d+)", out)
                ok = "PASS" if "RESULT: PASS" in out else "FAIL"
                cap_txt = (f"{ok} ({m.group(1)}={m.group(2)} words)" if m
                           else ok)
                if ok != "PASS":
                    all_ok = False

        audit_txt = "n/a"
        audit = folder / "audit_sync_overlap.py"
        if audit.exists():
            out = run([str(PY), str(audit)], cwd=folder)
            counts = {}
            for line in out.splitlines():
                m = re.match(r"\[\S+\s+step\s+\d+\]\s+([A-Z][A-Z0-9\-]*)", line)
                if m:
                    key = m.group(1)
                    counts[key] = counts.get(key, 0) + 1
            bad = {k: v for k, v in counts.items() if k != "OFF-CENTRE"}
            audit_txt = ("clean (0 collisions)" if not bad
                         else ", ".join(f"{k}:{v}" for k, v in bad.items()))
            if bad:
                all_ok = False

        lines.append(
            f"| {label} | `{folder_name}` | {sb} | `{script.name if script else '?'}` / "
            f"`{cls}` | {probe(hi) if hi else 'MISSING'} | "
            f"{probe(lo) if lo else 'MISSING'} | {sync_txt} | {cap_txt} | {audit_txt} |")
        print(f"[done] {folder_name}")

    lines += ["", f"**Overall: {'ALL 8 CONFIRMED' if all_ok else 'ISSUES FOUND'}**", ""]
    (HERE / "CHAPTER2_CONFIRMATION.md").write_text("\n".join(lines),
                                                  encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

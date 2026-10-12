"""Run the full audit suite across the Class 6 Chapter 2 story videos.

For every topic folder this runs, in order:

  1. the topic's own ``audit_sync_overlap.py``  (per-beat sync stretch + layout
     collision flags, measured against the real SRT),
  2. ``verify_sync.py``       on the delivered 360p30 captioned master
     (captions in silence / uncaptioned speech),
  3. ``verify_captions.py``   (caption text vs the narration, word for word).

Everything is sequential on purpose: two manim processes sharing one TeX cache
corrupt each other's ``media/texts`` files.

Usage (from this folder):

    .venv/Scripts/python.exe class6_audit.py [--json out.json]
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "verify_sync.py").exists())
PY = Path(sys.executable)
SKIP = {"audit_sync_overlap.py", "sync_map.py", "probe_construct.py",
        "bookmark_times.py", "segment_map.py", "class6_audit.py"}

STRICT = re.compile(
    r"TEXT-IN-TEXT|PARTIAL \d|OUT-OF-BOARD|TEXT-ON-ARROW|NEAR-BADGE"
    r"|LATEX-AS-TEXT|EMPTY-TEXT|TEXT-OUTSIDE-BOX")
BEAT = re.compile(r"^(\S+)\s+audio=\s*([\d.]+)s\s+anim=\s*([\d.]+)s\s+"
                  r"stretch=\s*([\d.]+)s")
TOTAL = re.compile(r"^TOTAL\s+audio=\s*([\d.]+)s\s+anim=\s*([\d.]+)s\s+"
                   r"stretch=\s*([\d.]+)s")
CAPS = re.compile(r"captions:\s*(\d+)\s+first\s*([\d.]+)s\s+last\s*([\d.]+)s")
VID = re.compile(r"video\s+([\d.]+)s.*audio\s+([\d.]+)s")
RESULT = re.compile(r"RESULT:\s*(PASS|FAIL)")
WORDS = re.compile(r"narration words\s*(\d+)\s+srt words\s*(\d+)")


def run(cmd: list[str], cwd: Path) -> str:
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=1800)
    return (proc.stdout or "") + (proc.stderr or "")


def story_script(folder: Path) -> Path | None:
    for p in sorted(folder.glob("*.py")):
        if p.name in SKIP:
            continue
        if "NARRATION" in p.read_text(encoding="utf-8", errors="replace"):
            return p
    return None


def main() -> None:
    topics = sorted(d for d in HERE.iterdir()
                    if d.is_dir() and (d / "media").is_dir())
    report = []
    for folder in topics:
        script = story_script(folder)
        if script is None:
            print(f"!! {folder.name}: no story script found")
            continue
        module = script.stem
        # audit the delivered master: prefer the 1080p60 render, keep the
        # 360p30 review copy listed alongside it
        masters = sorted(folder.glob("media/videos/*/*/*_captioned.mp4"),
                         key=lambda p: ("1080p60" not in str(p), str(p)))
        mp4 = masters[0] if masters else None
        if mp4 is None:
            print(f"!! {folder.name}: missing master")
            continue
        srt = mp4.parent / mp4.name.replace("_captioned.mp4", ".real.srt")
        if not srt.exists():
            print(f"!! {folder.name}: missing SRT next to the master")
            continue

        print(f"\n########## {folder.name} ##########")
        entry = {"topic": folder.name, "script": script.name,
                 "module": module, "video": str(mp4.relative_to(HERE)),
                 "also": [str(p.relative_to(HERE)) for p in masters[1:]]}

        # 1. sync + layout audit
        out = run([str(PY), "audit_sync_overlap.py"], folder)
        beats, total = [], None
        for line in out.splitlines():
            m = BEAT.match(line.strip())
            if m:
                beats.append({"name": m.group(1), "audio": float(m.group(2)),
                              "anim": float(m.group(3)),
                              "stretch": float(m.group(4))})
            t = TOTAL.match(line.strip())
            if t:
                total = {"audio": float(t.group(1)), "anim": float(t.group(2)),
                         "stretch": float(t.group(3))}
        strict = STRICT.findall(out)
        offc = len(re.findall(r"OFF-CENTRE", out))
        entry.update({"beats": beats, "total": total,
                      "strict_flags": strict, "strict_count": len(strict),
                      "off_centre": offc,
                      "max_stretch": max((b["stretch"] for b in beats),
                                         default=0.0)})
        print(f"  beats={len(beats)} max_stretch={entry['max_stretch']:.2f}s "
              f"collisions={len(strict)} off-centre={offc}")
        for f in sorted(set(strict)):
            print(f"    FLAG {f}")

        # 2. sync verification on the delivered file
        out = run([str(PY), str(ROOT / "verify_sync.py"), str(mp4), str(srt)],
                  folder)
        vid = VID.search(out)
        caps = CAPS.search(out)
        res = RESULT.search(out)
        entry["verify_sync"] = {
            "video_s": float(vid.group(1)) if vid else None,
            "audio_s": float(vid.group(2)) if vid else None,
            "captions": int(caps.group(1)) if caps else None,
            "result": res.group(1) if res else "UNKNOWN",
            "silence": "captions mostly in silence: 0" in out,
            "uncaptioned": "not captioned: 0" in out,
        }
        print(f"  verify_sync: {entry['verify_sync']['result']} "
              f"captions={entry['verify_sync']['captions']} "
              f"video={entry['verify_sync']['video_s']}s")

        # 3. caption wording
        out = run([str(PY), str(ROOT / "verify_captions.py"), script.name,
                   module, "NARRATION", str(srt)], folder)
        words = WORDS.search(out)
        res = RESULT.search(out)
        entry["verify_captions"] = {
            "narration_words": int(words.group(1)) if words else None,
            "srt_words": int(words.group(2)) if words else None,
            "result": res.group(1) if res else "UNKNOWN",
        }
        print(f"  verify_captions: {entry['verify_captions']['result']} "
              f"{entry['verify_captions']['narration_words']}="
              f"{entry['verify_captions']['srt_words']} words")
        report.append(entry)

    print("\n\n########## SUMMARY ##########")
    print(f"{'topic':<40} {'video':>8} {'beats':>6} {'stretch':>8} "
          f"{'collide':>8} {'sync':>5} {'words':>12}")
    for e in report:
        w = e["verify_captions"]
        print(f"{e['topic']:<40} {e['verify_sync']['video_s'] or 0:>8.2f} "
              f"{len(e['beats']):>6} {e['max_stretch']:>8.2f} "
              f"{e['strict_count']:>8} {e['verify_sync']['result']:>5} "
              f"{str(w['narration_words']) + '=' + str(w['srt_words']):>12}")

    if "--json" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--json") + 1])
        out.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"\nwrote {out}")


if __name__ == "__main__":
    main()

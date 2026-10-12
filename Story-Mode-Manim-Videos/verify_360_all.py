"""Verify the eight retitled Chapter-2 videos at 360p30.

Checks, per topic, on the freshly rendered 360p30 captioned master:
  * storyboard title / script title card (the new names),
  * verify_sync.py  -> captions in silence / uncaptioned speech,
  * verify_captions.py -> narration words == SRT words,
  * the topic's audit_sync_overlap.py -> collision / latex / bounds flags.

Run from the Story-Mode-Manim-Videos folder.
"""
from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PY = REPO / ".venv" / "Scripts" / "python.exe"
VS = REPO / "verify_sync.py"
VC = REPO / "verify_captions.py"
CHAPTER = "Chapter 2 - Linear Equations in One Variable"
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")

TOPICS = [
    ("1. Linear Equations", "Linear-Equations",
     "equation_anatomy_story.py", "EquationAnatomyStory", "equation_anatomy_story"),
    ("2. Solving Simple Equations", "Solving-Simple-Equations",
     "equation_solving_story.py", "EquationSolvingStory", "equation_solving_story"),
    ("3. Linear Equation Word Problems", "Linear-Equation-Word-Problems",
     "from_words_to_equations_story.py", "FromWordsToEquationsStory",
     "from_words_to_equations_story"),
    ("4. Linear Equations with Variables on Both Sides", "Linear-Equations-with-Variables-on-Both-Sides",
     "variables_both_sides_story.py", "VariablesBothSidesStory",
     "variables_both_sides_story"),
    ("5. Two-Digit Number Riddles", "Two-Digit-Number-Riddles",
     "two_digit_puzzles_story.py", "TwoDigitPuzzlesStory", "two_digit_puzzles_story"),
    ("6. Boats and Streams Problems", "Boats-and-Streams-Problems",
     "upstream_downstream_story.py", "UpstreamDownstreamStory",
     "upstream_downstream_story"),
    ("7. Applications of Angles and Parallel Lines", "Applications-of-Angles-and-Parallel-Lines",
     "geometry_angles_story.py", "GeometryAnglesStory", "geometry_angles_story"),
    ("8. Solving Equations with Fractions", "Solving-Equations-with-Fractions",
     "fractions_clearing_story.py", "FractionsClearingStory",
     "fractions_clearing_story"),
]


def run(cmd, cwd=None):
    p = subprocess.run([str(c) for c in cmd], cwd=cwd, env=ENV,
                       capture_output=True, text=True, errors="replace")
    return (p.stdout or "") + (p.stderr or "")


def main() -> None:
    rows = []
    all_ok = True
    for label, folder, script, cls, module in TOPICS:
        d = HERE / CHAPTER / folder
        vid = d / "media/videos" / module / "360p30" / f"{cls}_captioned.mp4"
        srt = vid.with_name(f"{cls}.real.srt")
        card = ""
        card_re = re.compile(r'board_text\("([^"]+)",\s*(\d+),\s*CHALK_WHITE,\s*"BOLD"\)'
                             r'|board_text\("([^"]+)",\s*(\d+),')
        m = card_re.search((d / script).read_text(encoding="utf-8"))
        if m:
            card = m.group(1) or m.group(3)
        sb = ""
        sbm = re.search(r"\*\*VIDEO TITLE:\*\*\s*(.+)",
                        (d / "storyboard.md").read_text(encoding="utf-8"))
        if sbm:
            sb = sbm.group(1).strip()

        sync = cap = audit = "n/a"
        if vid.exists():
            out = run([PY, VS, vid, srt])
            ok = "PASS" if "RESULT: PASS" in out else "FAIL"
            sil = re.search(r"captions mostly in silence:\s*(\d+)", out)
            unc = re.search(r"not captioned:\s*(\d+)", out)
            sync = (f"{ok} (silence {sil.group(1) if sil else '?'}, "
                    f"uncaptioned {unc.group(1) if unc else '?'})")
            if ok != "PASS":
                all_ok = False
            out = run([PY, VC, d / script, Path(script).stem, "NARRATION", srt])
            w = re.search(r"narration words (\d+)\s+srt words (\d+)", out)
            ok = "PASS" if "RESULT: PASS" in out else "FAIL"
            cap = f"{ok} ({w.group(1)}={w.group(2)})" if w else ok
            if ok != "PASS":
                all_ok = False
        else:
            sync = "MISSING VIDEO"
            all_ok = False
        if (d / "audit_sync_overlap.py").exists():
            out = run([PY, d / "audit_sync_overlap.py"], cwd=d)
            counts = {}
            for line in out.splitlines():
                mm = re.match(r"\[\S+\s+step\s+\d+\]\s+([A-Z][A-Z0-9\-]*)", line)
                if mm:
                    counts[mm.group(1)] = counts.get(mm.group(1), 0) + 1
            bad = {k: v for k, v in counts.items() if k != "OFF-CENTRE"}
            audit = "clean" if not bad else ", ".join(f"{k}:{v}"
                                                      for k, v in bad.items())
            if bad:
                all_ok = False
        rows.append((label, card, sb, sync, cap, audit))
        print(f"[done] {label}")

    lines = ["# Chapter 2 — retitled videos, 360p30 check", "",
             "| # | New title | On-screen card | Storyboard | sync | captions | audit |",
             "|---|---|---|---|---|---|---|"]
    for label, card, sb, sync, cap, audit in rows:
        lines.append(f"| {label} | `{card}` | {sb} | {sync} | {cap} | {audit} |")
    lines += ["", f"**Overall: {'ALL 8 OK' if all_ok else 'ISSUES FOUND'}**", ""]
    (HERE / "CHAPTER2_360_CHECK.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

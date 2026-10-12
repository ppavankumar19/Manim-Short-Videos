"""Append the alignment / overlap revision note to each storyboard.

Idempotent: running it twice changes nothing.

    python add_alignment_notes.py
"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent

HEAD = """
---

## Revision 2 — alignment, diagram positioning and overlap pass

The three videos were re-checked scene by scene at the moment each scene holds
(`scene_frames.py`, stills under `frames360/crosscheck/`), and with two
automated passes: the hard-overlap audit (`audit_sync_overlap.py`) and a new
clearance audit (`audit_clearance.py`) that measures every pair of chalk texts
closer than 0.22 units **and** every text a chalk line actually runs through —
the case a bounding-box test cannot see, because a straight line's box is
degenerate.

What it found and what was fixed:

{fixes}

After the fixes: `audit_clearance.py` → **0 text/line collisions** in this
video (the pairs still under 0.22 units are the designed two-line card stacks,
which sit 0.05-0.10 apart by construction), and `audit_sync_overlap.py` → **0
flags**. Nothing was re-timed: the narration, the bookmarks and every `run_time`
are untouched, so `verify_sync.py` → PASS ({caps} captions, 0 in silence, 0
uncaptioned, {dur} s) and `verify_captions.py` → PASS ({words} = {words} words)
on the re-rendered master.

Delivered this round: the **1080p60 master** with the captions burned in
(`final_videos/{cls}_captioned.mp4`), alongside the refreshed 360p review cut
(`finals_360/`).
"""

NOTES = {
    "SASAA-2-Sides-3-Angles": dict(
        cls="ConstructQuadrilateral2Sides3AnglesStory", caps=69, dur="224.4",
        words=598,
        fixes="""- **The 100° label at `Q` sat on the dashed `P R` guide line**
  (measured clearance 0.02 units). The label is placed along the angle
  bisector; it now sits at 1.04 instead of 1.30 from `Q`, i.e. well inside the
  angle and clear of the guide.
- **The "90°" of the `75° = (60° + 90°)/2` inset sat on the tip of the
  vertical 90° arm** (clearance 0.00). The inset is unchanged; the label is
  lifted clear of the arm's tip."""),
    "SASAS-3-Sides-2-Angles": dict(
        cls="ConstructQuadrilateral3Sides2AnglesStory", caps=72, dur="247.1",
        words=631,
        fixes="""- **The `D` label lay on the 6 cm compass arc that locates `D`**
  (clearance 0.00): the arc is centred on `C` with radius `C D`, so the label
  is now placed radially outward from `C`, 0.34 beyond the vertex, instead of
  a fixed offset that the arc ran through."""),
    "Special-Quads": dict(
        cls="ConstructSpecialQuadrilateralsRhombusParallelogramStory", caps=94,
        dur="315.5", words=815,
        fixes="""- **`O` lay on the horizontal diagonal** in the read-the-diagonals
  scene (on `A C`), in the rhombus construction (on `A C`) and in the square
  construction (on `J U`) — clearance 0.00-0.02 in all three. It now sits in a
  free quadrant beside the crossing: lower-left in the read-off, upper-left
  (above the line, clear of the compass leg) in the two construction scenes.
- **`O` also sat inside the right-angle mark** at the crossing in the
  read-the-diagonals scene (it overlapped the mark's corner), with `90°` only
  0.04 from it. `O` is out of the mark and `90°` is moved further out, so the
  mark reads cleanly on its own.
- **`B` and `D` lay on the perpendicular bisector**: that dashed line is drawn
  1.22x past the vertices, so it ran through both letters. Both labels now sit
  0.34 to the right of their vertex, which also clears the 3 cm compass arc
  (centred on `O` with radius `O B`) that they had started to touch.
- **The morph drew the square's equal diagonal through the rhombus's `A` and
  `C` labels**: those names are retired as the morph starts, so no line crosses
  a letter during the transition."""),
}


def main() -> None:
    for folder, kw in NOTES.items():
        path = HERE / folder / "storyboard.md"
        text = path.read_text(encoding="utf-8")
        if "alignment, diagram positioning and overlap pass" in text:
            print(f"{folder}: already noted, skipped")
            continue
        path.write_text(text.rstrip("\n") + "\n" + HEAD.format(**kw),
                        encoding="utf-8")
        print(f"{folder}: storyboard.md -> {path.stat().st_size} bytes")


if __name__ == "__main__":
    main()

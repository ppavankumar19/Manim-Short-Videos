"""Alignment / overlap fixes for videos 05, 06 and 07.

Found by cross-checking every scene at its hold moment (scene_frames.py) and by
the two audits: audit_sync_overlap.py (hard overlaps) and audit_clearance.py
(pairs of text closer than 0.22 units, and text a chalk line runs through --
the case a bounding-box test cannot see, because a straight line's box is
degenerate).

Every fix is a label offset, asserted so a silent mis-patch is impossible:

  05  the 60/90 inset's "90°" sat on the tip of the vertical 90 arm;
      the 100° label at Q sat on the dashed P R guide line.
  06  the "D" label sat on the compass arc that locates D.
  07  the "O" label sat on the horizontal diagonal in all three rhombus/square
      scenes and inside the right-angle mark in the read-the-diagonals scene;
      the "B" and "D" labels sat on the perpendicular bisector, which runs
      1.22x past the vertices; the rhombus's A/C labels were still on the board
      when the morph drew the square's equal diagonal through them.

Run from this folder, then render:

    python fix_alignment.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

FIXES: dict[str, list[tuple[str, str, int]]] = {
    "SASAA-2-Sides-3-Angles": [
        # the "90°" label of the 75 = (60+90)/2 inset: lift it clear of the
        # 90 arm, whose tip was inside the label's box
        ("            v + np.array([-0.05, 0.98, 0])",
         "            v + np.array([-0.05, 1.16, 0])", 1),
        # the 100° label at Q: the dashed P R guide runs through it at 1.30
        # along the bisector, so bring it in towards the vertex
        ('            ang_lab = board_text("100°", 15, CHALK_AMBER, "BOLD")'
         '.move_to(\n'
         '                np.array(Q, dtype=float) + 1.30 * unit(\n'
         '                    (d["qp_deg"] + d["qr_deg"]) / 2.0))',
         '            ang_lab = board_text("100°", 15, CHALK_AMBER, "BOLD")'
         '.move_to(\n'
         '                np.array(Q, dtype=float) + 1.04 * unit(\n'
         '                    (d["qp_deg"] + d["qr_deg"]) / 2.0))', 1),
    ],
    "SASAS-3-Sides-2-Angles": [
        # the "D" label: push it radially out of the 6 cm arc that finds D
        ("                D + np.array([-0.10, 0.30, 0])",
         "                D + 0.34 * unit(dir_deg(C, D))", 1),
        # the four method cards overlapped the figure -- its C vertex and the
        # C D / C B edges ran underneath cards 1-3 (found by the LINE-IN-BOX
        # check).  Shift the column right: still inside the board, and the
        # figure keeps its own space.
        ("                np.array([2.85, 0.55, 0]))",
         "                np.array([3.40, 0.55, 0]))", 1),
        # the recap rows (1), (2), (3) started 0.09 from the figure's C label;
        # a little further right gives it room
        ("                np.array([BOARD_CX + 1.5, 1.15, 0]))",
         "                np.array([BOARD_CX + 1.85, 1.15, 0]))", 1),
    ],
    "Special-Quads": [
        # read-the-diagonals: "O" out of the right-angle mark, into the free
        # lower-left quadrant; "90°" a little further off the mark's corner
        ("                O + np.array([0.22, 0.16, 0])",
         "                O + np.array([-0.36, -0.34, 0])", 1),
        ("                O + np.array([0.42, 0.34, 0])",
         "                O + np.array([0.50, 0.44, 0])", 1),
        # rhombus + square constructions: "O" was sitting on the horizontal
        # diagonal (A C / J U) in both scenes
        ("O + np.array([0.20, -0.02, 0])",
         "O + np.array([-0.32, 0.30, 0])", 1),
        ("O2 + np.array([0.20, -0.02, 0])",
         "O2 + np.array([-0.32, 0.30, 0])", 1),
        # the perpendicular bisector runs past the vertices, through "B"
        # and "D": move both labels off it, and far enough out to clear the
        # 3 cm compass arc as well (it is centred on O with radius O B)
        ("                B + np.array([0.06, 0.26, 0])",
         "                B + np.array([0.34, 0.26, 0])", 1),
        ("                B + np.array([0.34, 0.06, 0])",
         "                B + np.array([0.34, 0.26, 0])", 1),
        ("                D + np.array([0.06, -0.34, 0])",
         "                D + np.array([0.34, -0.34, 0])", 1),
        ("                D + np.array([0.34, -0.12, 0])",
         "                D + np.array([0.34, -0.34, 0])", 1),
        # the morph drew the square's equal diagonal through the rhombus's
        # A / C labels: retire those names as the morph starts
        ("            self.play(Transform(rh, sq_group), run_time=min(",
         "            self.play(Transform(rh, sq_group), FadeOut(names),\n"
         "                      run_time=min(", 1),
        ("            self.play(FadeOut(rh), FadeOut(names), FadeOut(ask), "
         "FadeOut(note_sq),",
         "            self.play(FadeOut(rh), FadeOut(ask), FadeOut(note_sq),",
         1),
    ],
}

ASSEMBLER = {
    "SASAA-2-Sides-3-Angles": "assemble_sasaa.py",
    "SASAS-3-Sides-2-Angles": "assemble_sasas.py",
    "Special-Quads": "assemble_specialq.py",
}


def main() -> int:
    for topic, fixes in FIXES.items():
        folder = HERE / topic
        beats = next(p for p in folder.glob("_*_beats.py"))
        text = beats.read_text(encoding="utf-8")
        print(f"\n=== {topic}  ({beats.name})")
        for old, new, want in fixes:
            got = text.count(old)
            if got == 0:
                # already patched by an earlier run (the audits re-verify)
                print(f"  --  not needed / already applied: "
                      f"{old.strip()[:52]}")
                continue
            if got != want:
                print(f"  !! expected {want} of {old!r}, found {got}")
                return 1
            text = text.replace(old, new)
            print(f"  ok  x{want}  {new.strip().splitlines()[-1][:64]}")
        beats.write_text(text, encoding="utf-8")

        p = subprocess.run([sys.executable, ASSEMBLER[topic]], cwd=str(folder),
                           capture_output=True, text=True)
        line = (p.stdout.strip().splitlines() or ["(no output)"])[0]
        print(f"  {line}")
        if p.returncode != 0:
            print(p.stderr[-2000:])
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

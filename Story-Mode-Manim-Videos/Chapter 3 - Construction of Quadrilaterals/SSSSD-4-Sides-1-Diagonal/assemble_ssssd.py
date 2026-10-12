"""Build storyboard 03's module from storyboard 02's proven scaffolding.

Video 02 already carries the series theme, the backdrop/badges, the SRT export,
the CRISP-TEXT pacing helpers (rt/quick/leftover/appear), the compass tool and
the construction helpers.  For video 03 we keep that head verbatim, and replace
only what is topic-specific:

  * the module docstring,
  * the two geometry frames (example_frame / practice_frame),
  * the narration table,
  * the class name and the output path,
  * every scene beat.

Run from the topic folder:
    python assemble_ssssd.py
"""
from __future__ import annotations

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAPTER = HERE.parent
SRC = CHAPTER / "SSSSA-4-Sides-1-Angle" / "construct_quadrilateral_4sides_1angle.py"
OUT = HERE / "construct_quadrilateral_4sides_1diagonal.py"
FRAG = HERE / "_ssssd_fragment.py"
BEATS = HERE / "_ssssd_beats.py"

DOCSTRING = '''"""
How to Construct a Quadrilateral Given 4 Sides and 1 Diagonal
Story-mode chalkboard lesson (Telangana Class 8 Maths, Chapter 3:
Construction of Quadrilaterals, Storymode 03).

LLM KEY / FUNCTION NAME: construct_quadrilateral_4sides_1diagonal

Production pipeline (mirrors the rest of the Story-Mode series):
  - Shared assets/background2.png chalkboard backdrop + student/teacher
    cutouts + corner badges (dhimantAI top-left, Mathematics top-right).
  - VoiceoverScene + speech service; narration written as continuous prose.
  - Real per-word sync via <bookmark> tags + tracker timing, and a
    ground-truth SRT export from the service word boundaries.
  - Sound effects from sound_effects.py; chalk-styled Text (Segoe Print) and
    MathTex; shared story_common.play_challenge_countdown() for the THINK clock.
  - Text appears crisply and the board then HOLDS: a fade spread over a long
    narration window reads as truncated lettering.  Diagram work is paced
    across its window, words are not.

The defining visual: the diagonal is the shared side of two triangles.  With
A C = 5 cm given, triangle A B C is fixed by its three sides (S.S.S) and the
two remaining sides then locate D on the other side of the diagonal.

Title + 10 scenes:
  0. Title card.
  1. The five given measurements (Example 3 data).
  2. The diagonal splits the quadrilateral into two triangles.
  3. Which three measurements to use first (three sides, no angle).
  4. Draw the diagonal and set the compasses to A B = 4.
  5. The second arc fixes B -- triangle A B C complete.
  6. The remaining two sides locate D.
  7. Complete A B C D and verify all five measurements.
  8. The reusable method.
  9. Your turn: a practice set -- plan the construction.
 10. Recap and thank-you.
"""'''


def section(text: str, start: str, end: str) -> tuple[int, int]:
    """Character offsets of the region from `start` up to (not including) `end`."""
    i = text.index(start)
    j = text.index(end, i)
    return i, j


def main() -> None:
    src = SRC.read_text(encoding="utf-8")
    frag = FRAG.read_text(encoding="utf-8")
    beats = BEATS.read_text(encoding="utf-8")
    # the beats fragment carries a leading note for the reader; only the
    # indented class body belongs inside the module
    beats = beats[beats.index("    # ================================================================ beats =="):]

    # 1. docstring
    i, j = section(src, '"""', 'from __future__ import annotations')
    out = DOCSTRING + "\n" + src[j:]

    # 2. geometry frames: keep everything after `def vertex_label(`
    frame_part = frag.split("# ---------------------------------------------------------------- narration --")[0]
    frames = frame_part.split("# ------------------------------------------------- construction furniture ----")[1]
    i, j = section(out, "def example_frame(", "def vertex_label(")
    # `frames` carries the topic's own SCALE/AC_Y constants and both frames,
    # so it replaces the two frames of video 02 wholesale
    out = out[:i] + frames.strip() + "\n\n\n" + out[j:]

    # 3. narration table
    narr_part = frag.split("# ---------------------------------------------------------------- narration --")[1]
    narration = ("# ---------------------------------------------------------------- narration --"
                 + narr_part.split("NARRATION = {", 1)[1])
    narration = "NARRATION = {" + narration
    i, j = section(out, "# ---------------------------------------------------------------- narration --",
                   "class ConstructQuadrilateral4Sides1AngleStory")
    out = out[:i] + narration.rstrip() + "\n\n\n" + out[j:]

    # 4. class name + output paths
    out = out.replace("class ConstructQuadrilateral4Sides1AngleStory",
                      "class ConstructQuadrilateral4Sides1DiagonalStory")
    out = out.replace('construct_quadrilateral_4sides_1angle"',
                      'construct_quadrilateral_4sides_1diagonal"')

    # 5. scene beats
    i = out.index("    # ================================================================ beats ==")
    out = out[:i] + beats

    # 6. construct() dispatch -- the new beat names
    out = out.replace("        self.beat2_sketch()\n", "        self.beat2_split()\n")
    out = out.replace("        self.beat4_side_angle()\n", "        self.beat4_diagonal()\n")
    out = out.replace("        self.beat6_locate_s()\n", "        self.beat6_locate_d()\n")

    OUT.write_text(out, encoding="utf-8")
    print(f"wrote {OUT}  ({len(out.splitlines())} lines)")
    for token in ("beat2_split", "beat4_diagonal", "beat6_locate_d",
                  "practice_frame", "triangle_apex",
                  "ConstructQuadrilateral4Sides1DiagonalStory",
                  "construct_quadrilateral_4sides_1diagonal"):
        print(f"  {token}: {out.count(token)}")


if __name__ == "__main__":
    main()

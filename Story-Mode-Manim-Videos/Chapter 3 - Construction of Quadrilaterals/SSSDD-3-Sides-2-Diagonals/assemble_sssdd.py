"""Build storyboard 04's module from storyboard 03's proven scaffolding.

Video 03 already carries the series theme, the backdrop/badges, the SRT export,
the crisp-text pacing helpers, the compass tool and `diamond_names()` (which puts
each vertex letter in the corner that is actually free).  For video 04 we keep
that head verbatim and replace only what is topic-specific:

  * the module docstring,
  * the geometry frames (example_frame / practice_frame),
  * the narration table,
  * the class name and the output path,
  * every scene beat.

Run from the topic folder:
    python assemble_sssdd.py
"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAPTER = HERE.parent
SRC = CHAPTER / "SSSSD-4-Sides-1-Diagonal" / "construct_quadrilateral_4sides_1diagonal.py"
OUT = HERE / "construct_quadrilateral_3sides_2diagonals.py"
FRAG = HERE / "_sssdd_fragment.py"
BEATS = HERE / "_sssdd_beats.py"

DOCSTRING = '''"""
How to Construct a Quadrilateral Given 3 Sides and 2 Diagonals
Story-mode chalkboard lesson (Telangana Class 8 Maths, Chapter 3:
Construction of Quadrilaterals, Storymode 04).

LLM KEY / FUNCTION NAME: construct_quadrilateral_3sides_2diagonals

Production pipeline (mirrors the rest of the Story-Mode series):
  - Shared assets/background2.png chalkboard backdrop + student/teacher
    cutouts + corner badges (dhimantAI top-left, Mathematics top-right).
  - VoiceoverScene + speech service; narration written as continuous prose.
  - Real per-word sync via <bookmark> tags + tracker timing, and a
    ground-truth SRT export from the service word boundaries.
  - Sound effects from sound_effects.py; chalk-styled Text (Segoe Print) and
    MathTex; shared story_common.play_challenge_countdown() for the THINK clock.
  - Text appears crisply and the board then HOLDS; diagram work is paced across
    its window, words are not.
  - Every construction arc is drawn by a pair of compasses (hinge, legs,
    needle, pencil) -- both arcs of each pair, never one.

The defining visual: the five measurements are sorted 3 + 2.  Two sides and the
diagonal A C (all three known) build triangle A B C by S.S.S; the remaining
side C D and the other diagonal B D then locate D on the far side of A C.  The
fifth side, A D, is never given -- the construction fixes it.

Title + 10 scenes:
  0. Title card.
  1. The five given measurements sorted into 3 sides and 2 diagonals.
  2. Rough sketch: find the triangle whose three lengths are known.
  3. The 3 + 2 plan: "3 build, 2 locate".
  4. Draw the diagonal A C and set the compasses to A B = 4.5.
  5. The second arc fixes B -- triangle A B C complete.
  6. The side C D and the diagonal B D locate D on the far side of A C.
  7. Complete A B C D and verify all five measurements.
  8. The reusable method (and why A B D cannot be built first).
  9. Your turn: Exercise 3.3(a) -- quadrilateral G O L D.
 10. Recap and thank-you.
"""'''


def section(text: str, start: str, end: str) -> tuple[int, int]:
    i = text.index(start)
    j = text.index(end, i)
    return i, j


def main() -> None:
    src = SRC.read_text(encoding="utf-8")
    frag = FRAG.read_text(encoding="utf-8")
    beats = BEATS.read_text(encoding="utf-8")
    beats = beats[beats.index("    # ================================================================ beats =="):]

    # 1. docstring
    i, j = section(src, '"""', 'from __future__ import annotations')
    out = DOCSTRING + "\n" + src[j:]

    # 2. geometry frames (the fragment carries SCALE/AC_Y and both frames);
    #    `diamond_names()` lives inside the replaced span, so keep it verbatim
    dn_i, dn_j = section(src, "def diamond_names(", "def vertex_label(")
    keep_diamond = src[dn_i:dn_j].rstrip()
    frame_part = frag.split("# ---------------------------------------------------------------- narration --")[0]
    frames = frame_part.split("# ------------------------------------------------- construction furniture ----")[1]
    i, j = section(out, "SCALE = 0.56", "def vertex_label(")
    out = out[:i] + frames.strip() + "\n\n\n" + keep_diamond + "\n\n\n" + out[j:]

    # 3. narration table
    narr_part = frag.split("# ---------------------------------------------------------------- narration --")[1]
    narration = "NARRATION = {" + narr_part.split("NARRATION = {", 1)[1]
    i, j = section(out, "NARRATION = {",
                   "class ConstructQuadrilateral4Sides1DiagonalStory")
    out = out[:i] + narration.rstrip() + "\n\n\n" + out[j:]

    # 4. class name + output paths
    out = out.replace("class ConstructQuadrilateral4Sides1DiagonalStory",
                      "class ConstructQuadrilateral3Sides2DiagonalsStory")
    out = out.replace('construct_quadrilateral_4sides_1diagonal"',
                      'construct_quadrilateral_3sides_2diagonals"')

    # 5. scene beats
    out = out.replace("self.beat2_split()", "self.beat2_choose()")
    out = out.replace("self.beat3_choose()", "self.beat3_plan()")
    i = out.index("    # ================================================================ beats ==")
    out = out[:i] + beats

    OUT.write_text(out, encoding="utf-8")
    print(f"wrote {OUT}  ({len(out.splitlines())} lines)")
    for token in ("ConstructQuadrilateral3Sides2DiagonalsStory",
                  "construct_quadrilateral_3sides_2diagonals",
                  "practice_frame", "diamond_names", "compass_on"):
        print(f"  {token}: {out.count(token)}")


if __name__ == "__main__":
    main()

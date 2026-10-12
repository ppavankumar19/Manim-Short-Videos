"""Build storyboard 07's module from storyboard 03's proven scaffolding.

Storyboard 03's module is the untouched head of the series: the theme, the
backdrop/badges, the SRT export, the crisp-text pacing helpers, the pair of
compasses, `angle_mark()`, `protractor()`, `diamond_names()` and the card
helpers.  For storyboard 07 (special quadrilaterals) we keep that head verbatim
and replace only what is topic-specific:

  * the module docstring,
  * the geometry frames (parallelogram_frame, rhombus_frame, square_frame) and
    the vector helpers,
  * the narration table,
  * the class name and the output path,
  * every scene beat.

Run from the topic folder:
    python assemble_specialq.py
"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAPTER = HERE.parent
SRC = CHAPTER / "SSSSD-4-Sides-1-Diagonal" / "construct_quadrilateral_4sides_1diagonal.py"
OUT = HERE / "construct_special_quadrilaterals_rhombus_parallelogram.py"
FRAG = HERE / "_specialq_fragment.py"
BEATS = HERE / "_specialq_beats.py"

DOCSTRING = '''"""
Constructing Special Quadrilaterals: Rhombus, Parallelogram and Square
Story-mode chalkboard lesson (Telangana Class 8 Maths, Chapter 3:
Construction of Quadrilaterals, Storymode 07).

LLM KEY / FUNCTION NAME: construct_special_quadrilaterals_rhombus_parallelogram

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

The defining idea: a special quadrilateral is named information.  The
parallelogram is given two sides and one angle, and its angle properties supply
the other three angles; the rhombus is given its two diagonals, and the
perpendicular-bisecting property places all four vertices; the square is the
rhombus construction with the extra condition that the diagonals are equal.
Every figure is built from the given numbers with vectors, never by hand.

Title + 10 scenes:
  0. Title card.
  1. Three short lists of measurements -- and why they are enough.
  2. Parallelogram B E L T: derive the missing angles from the properties.
  3. Construct B E L T: S.A.S triangle, then two 135 degree rays meet at T.
  4. Rhombus A B C D: read the two diagonal properties.
  5. Construct the rhombus: A C, its perpendicular bisector, B and D at 3 cm.
  6. From rhombus to square: equal diagonals, then square J U M P.
  7. Three shapes, three property strategies.
  8. The reusable method: analyse before you draw.
  9. Your turn: a parallelogram's angles and a rhombus's half-diagonals.
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

    # 2. geometry frames (the fragment carries the three frames);
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
                      "class ConstructSpecialQuadrilateralsRhombusParallelogramStory")
    out = out.replace('construct_quadrilateral_4sides_1diagonal"',
                      'construct_special_quadrilaterals_rhombus_parallelogram"')

    # 5. scene beats
    for old, new in (("self.beat1_data()", "self.beat1_special()"),
                     ("self.beat2_split()", "self.beat2_parallelogram()"),
                     ("self.beat3_choose()", "self.beat3_construct_belt()"),
                     ("self.beat4_diagonal()", "self.beat4_rhombus_props()"),
                     ("self.beat5_triangle()", "self.beat5_construct_rhombus()"),
                     ("self.beat6_locate_d()", "self.beat6_square()"),
                     ("self.beat7_complete()", "self.beat7_compare()")):
        out = out.replace(old, new)
    i = out.index("    # ================================================================ beats ==")
    out = out[:i] + beats

    OUT.write_text(out, encoding="utf-8")
    print(f"wrote {OUT}  ({len(out.splitlines())} lines)")
    for token in ("ConstructSpecialQuadrilateralsRhombusParallelogramStory",
                  "construct_special_quadrilaterals_rhombus_parallelogram",
                  "parallelogram_frame", "rhombus_frame", "square_frame",
                  "diamond_names"):
        print(f"  {token}: {out.count(token)}")


if __name__ == "__main__":
    main()

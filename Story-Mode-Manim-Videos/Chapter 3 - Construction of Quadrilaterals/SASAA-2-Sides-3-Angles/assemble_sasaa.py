"""Build storyboard 05's module from storyboard 03's proven scaffolding.

Storyboard 03's module is the untouched head of the series: the theme, the
backdrop/badges, the SRT export, the crisp-text pacing helpers, the pair of
compasses, `angle_mark()`, `protractor()`, `diamond_names()` and the card
helpers.  For storyboard 05 (two adjacent sides + three angles) we keep that
head verbatim and replace only what is topic-specific:

  * the module docstring,
  * the geometry frames (example_frame / practice_frame) and the ray helpers,
  * the narration table,
  * the class name and the output path,
  * every scene beat.

Run from the topic folder:
    python assemble_sasaa.py
"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAPTER = HERE.parent
SRC = CHAPTER / "SSSSD-4-Sides-1-Diagonal" / "construct_quadrilateral_4sides_1diagonal.py"
OUT = HERE / "construct_quadrilateral_2sides_3angles.py"
FRAG = HERE / "_sasaa_fragment.py"
BEATS = HERE / "_sasaa_beats.py"

DOCSTRING = '''"""
How to Construct a Quadrilateral Given 2 Adjacent Sides and 3 Angles
Story-mode chalkboard lesson (Telangana Class 8 Maths, Chapter 3:
Construction of Quadrilaterals, Storymode 05).

LLM KEY / FUNCTION NAME: construct_quadrilateral_2sides_3angles

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
  - Angles are set out the way the textbook sets them out: a protractor for the
    100 degree angle, a bisected 60/90 pair for the 75 degree angle, and the
    pair of compasses for the standard 120 degree angle.

The defining visual: the five measurements sort 3 + 2.  The two adjacent sides
P Q and Q R with the angle between them, angle Q, build triangle P Q R by
S.A.S; the remaining two angles, at P and at R, are two RAYS whose crossing is
the fourth vertex.  Where the earlier videos of this chapter located the last
vertex with two compass arcs, here it is located by two intersecting rays.

Title + 10 scenes:
  0. Title card.
  1. The five given measurements: 2 adjacent sides and 3 angles.
  2. Find the S.A.S triangle: P Q, angle Q, Q R.
  3. The 3 + 2 plan: "3 build, 2 locate".
  4. Draw P Q and set out the 100 degree angle at Q with the protractor.
  5. Measure Q R = 4.8 along that ray: triangle P Q R is fixed.
  6. The 75 degree angle at P gives the first ray -- one direction for S.
  7. The 120 degree angle at R gives the second ray: they cross at S.
  8. Complete and verify P Q R S, then the reusable method.
  9. Your turn: quadrilateral A B C D.
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

    # 2. geometry frames (the fragment carries SCALE and both frames);
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
                      "class ConstructQuadrilateral2Sides3AnglesStory")
    out = out.replace('construct_quadrilateral_4sides_1diagonal"',
                      'construct_quadrilateral_2sides_3angles"')

    # 5. scene beats
    for old, new in (("self.beat2_split()", "self.beat2_choose()"),
                     ("self.beat3_choose()", "self.beat3_plan()"),
                     ("self.beat4_diagonal()", "self.beat4_build()"),
                     ("self.beat6_locate_d()", "self.beat6_first_ray()"),
                     ("self.beat7_complete()", "self.beat7_second_ray()"),
                     ("self.beat8_method()", "self.beat8_complete()")):
        out = out.replace(old, new)
    i = out.index("    # ================================================================ beats ==")
    out = out[:i] + beats

    OUT.write_text(out, encoding="utf-8")
    print(f"wrote {OUT}  ({len(out.splitlines())} lines)")
    for token in ("ConstructQuadrilateral2Sides3AnglesStory",
                  "construct_quadrilateral_2sides_3angles",
                  "practice_frame", "diamond_names", "ray_intersection",
                  "demonstration"):
        print(f"  {token}: {out.count(token)}")


if __name__ == "__main__":
    main()

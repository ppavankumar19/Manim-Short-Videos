"""Build storyboard 06's module from storyboard 03's proven scaffolding.

Storyboard 03's module is the untouched head of the series: the theme, the
backdrop/badges, the SRT export, the crisp-text pacing helpers, the pair of
compasses, `angle_mark()`, `protractor()`, `diamond_names()` and the card
helpers.  For storyboard 06 (three sides + two included angles) we keep that
head verbatim and replace only what is topic-specific:

  * the module docstring,
  * the geometry frames (example_construction / practice_construction) and the
    ray helpers,
  * the narration table,
  * the class name and the output path,
  * every scene beat.

Run from the topic folder:
    python assemble_sasas.py
"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAPTER = HERE.parent
SRC = CHAPTER / "SSSSD-4-Sides-1-Diagonal" / "construct_quadrilateral_4sides_1diagonal.py"
OUT = HERE / "construct_quadrilateral_3sides_2angles.py"
FRAG = HERE / "_sasas_fragment.py"
BEATS = HERE / "_sasas_beats.py"

DOCSTRING = '''"""
How to Construct a Quadrilateral Given 3 Sides and 2 Included Angles
Story-mode chalkboard lesson (Telangana Class 8 Maths, Chapter 3:
Construction of Quadrilaterals, Storymode 06).

LLM KEY / FUNCTION NAME: construct_quadrilateral_3sides_2angles

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
  - The angles are set out the way the textbook sets them out: a protractor for
    the 100 degree angle at B, a bisected 60/90 pair for the 75 degree angle at
    C, and the pair of compasses for the final 6 cm arc.

The defining visual: the five measurements are READ AS A CHAIN --
side, angle, side, angle, side.  The first three (A B, angle B, B C) build
triangle A B C by S.A.S; the second angle (at C) then gives a DIRECTION and the
last side (C D) gives a DISTANCE along it, so the fourth vertex is located by
one ray and one arc.  That is what separates this case from the previous one,
where two rays located the last vertex.

Title + 10 scenes:
  0. Title card.
  1. The five measurements as a connected chain.
  2. What "included angle" means.
  3. The 3 + 2 plan: "3 build, 2 finish".
  4. Draw A B and set out the 100 degree angle at B with the protractor.
  5. Measure B C = 4.5 along that ray: triangle A B C is fixed.
  6. The 75 degree angle at C gives the direction of C D.
  7. The 6 cm arc about C cuts that ray at D -- direction plus distance.
  8. Complete and verify A B C D, then the reusable method.
  9. Your turn: Exercise 3.5(a), quadrilateral P Q R S.
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
                      "class ConstructQuadrilateral3Sides2AnglesStory")
    out = out.replace('construct_quadrilateral_4sides_1diagonal"',
                      'construct_quadrilateral_3sides_2angles"')

    # 5. scene beats
    for old, new in (("self.beat1_data()", "self.beat1_chain()"),
                     ("self.beat2_split()", "self.beat2_included()"),
                     ("self.beat3_choose()", "self.beat3_plan()"),
                     ("self.beat4_diagonal()", "self.beat4_build()"),
                     ("self.beat6_locate_d()", "self.beat6_second_angle()"),
                     ("self.beat7_complete()", "self.beat7_locate_d()"),
                     ("self.beat8_method()", "self.beat8_complete()")):
        out = out.replace(old, new)
    i = out.index("    # ================================================================ beats ==")
    out = out[:i] + beats

    OUT.write_text(out, encoding="utf-8")
    print(f"wrote {OUT}  ({len(out.splitlines())} lines)")
    for token in ("ConstructQuadrilateral3Sides2AnglesStory",
                  "construct_quadrilateral_3sides_2angles",
                  "practice_construction", "diamond_names",
                  "quadrilateral_from_chain", "_convex"):
        print(f"  {token}: {out.count(token)}")


if __name__ == "__main__":
    main()


"""Assemble the SSSSA story script from the series scaffolding.

The chapter's first video carries the shared scaffolding (theme, chalk helpers,
Class-8 geometry helpers, the VoiceoverScene plumbing that produces the SRT).
This builds the second script out of it plus the topic's own narration, helpers
and beats, so every video in the chapter stays identical in structure.
"""
from __future__ import annotations

import pathlib
import re

CHAP = pathlib.Path(__file__).resolve().parent
BASE = (CHAP / "Why-4-Sides-Arent-Enough"
        / "quadrilateral_uniqueness_and_five_measurements.py")
FRAG = CHAP / "_ssssa_fragment.py"
OUT_DIR = CHAP / "SSSSA-4-Sides-1-Angle"
OUT = OUT_DIR / "construct_quadrilateral_4sides_1angle.py"

NEW_DOC = '''"""
How to Construct a Quadrilateral Given 4 Sides and 1 Angle -- the S.S.S.S.A Method
Story-mode chalkboard lesson (Telangana Class 8 Maths, Chapter 3:
Construction of Quadrilaterals, Storymode 02).

LLM KEY / FUNCTION NAME: construct_quadrilateral_4sides_1angle

Production pipeline (mirrors the rest of the Story-Mode series):
  - Shared assets/background2.png chalkboard backdrop + student/teacher
    cutouts + corner badges (dhimantAI top-left, Mathematics top-right).
  - VoiceoverScene + speech service; narration written as continuous prose.
  - Real per-word sync via <bookmark> tags + tracker timing, and a
    ground-truth SRT export from the service word boundaries.
  - Sound effects from sound_effects.py; chalk-styled Text (Segoe Print) and
    MathTex; shared story_common.play_challenge_countdown() for the THINK clock.

The defining visual: the five given measurements split into 3 + 2 -- two sides
and the included angle build triangle PQR, and the remaining two side lengths
become the radii of two compass arcs whose intersection is the fourth vertex.

Title + 10 scenes:
  0. Title card.
  1. The five given measurements (Example 1 data).
  2. Rough sketch, every measurement marked.
  3. Which three measurements to use first (S.A.S).
  4. Draw PQ and set out the 120 degree angle at Q.
  5. Compass arc of 5.2 cm about Q fixes R.
  6. Two arcs (4 cm about P, 5.5 cm about R) locate S.
  7. Join PS and SR, then verify all five measurements.
  8. The reusable S.S.S.S.A method.
  9. Your turn: Exercise 3.1(a) -- plan the construction.
 10. Recap and thank-you.
"""
'''


def main() -> None:
    src = BASE.read_text(encoding="utf-8")
    i_narr = src.index("# ------------------------------------------------"
                       "---------------- narration --")
    i_class = src.index("class QuadrilateralUniquenessStory")
    i_construct = src.index("    def construct(self):")
    head, plumb = src[:i_narr], src[i_class:i_construct]

    head = re.sub(r'^""".*?"""', NEW_DOC.strip(), head, count=1, flags=re.S)
    head = head.replace(
        "    Indicate, Flash, Circumscribe, SurroundingRectangle, config,",
        "    Indicate, Flash, Circumscribe, SurroundingRectangle, LaggedStart,\n"
        "    config,")
    plumb = (plumb.replace("QuadrilateralUniquenessStory",
                           "ConstructQuadrilateral4Sides1AngleStory")
             .replace("quadrilateral_uniqueness_and_five_measurements",
                      "construct_quadrilateral_4sides_1angle"))

    frag = FRAG.read_text(encoding="utf-8")
    middle, beats = frag.split("# @@PLUMBING@@")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(head + middle + plumb + beats, encoding="utf-8")
    print(f"wrote {OUT} ({len(OUT.read_text(encoding='utf-8').splitlines())} lines)")


if __name__ == "__main__":
    main()

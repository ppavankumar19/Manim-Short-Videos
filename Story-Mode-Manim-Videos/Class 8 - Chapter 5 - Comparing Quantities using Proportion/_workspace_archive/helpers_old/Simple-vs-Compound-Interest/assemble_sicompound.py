"""Build this topic's module from the proven head of the Chapter 3
quadrilaterals set.

That module is the untouched head of the series: the theme and board constants,
the chalkboard backdrop with the student, the teacher and both corner badges,
`reset_board`, `appear`, the crisp-text pacing helpers and the ground-truth SRT
export.  None of that is topic-specific, so it is kept verbatim and only the
topic-specific parts are replaced:

  * the module docstring,
  * the narration table and this topic's money-ladder furniture,
  * the class name and the output path,
  * `_capture_srt` (the series version folds a one-or-two-word tail chunk into
    the caption before it, so no caption lands mostly in silence),
  * every scene beat.

Run from this folder:
    python assemble_sicompound.py
"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAPTER = next(p for p in HERE.parents
               if (p / "Chapter 3 - Construction of Quadrilaterals").exists())
SRC = (CHAPTER / "Chapter 3 - Construction of Quadrilaterals"
       / "SSSSD-4-Sides-1-Diagonal"
       / "construct_quadrilateral_4sides_1diagonal.py")
OUT = HERE / "simple_vs_compound_interest_formula.py"
FRAG = HERE / "_sicompound_fragment.py"
BEATS = HERE / "_sicompound_beats.py"

CLASS = "SimpleVsCompoundInterestFormulaStory"
MODULE_KEY = "simple_vs_compound_interest_formula"

DOCSTRING = '''"""
Simple Interest vs. Compound Interest: Deriving the Compound Interest Formula
Story-mode chalkboard lesson (Class 8 Maths, Chapter 5: Comparing Quantities
using Proportion, Storymode 02).

LLM KEY / FUNCTION NAME: simple_vs_compound_interest_formula

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
  - Nothing on the board sits below y = -2.00: the burned-in caption grows up
    from the bottom of the frame.
  - All money is written "Rs" (the rupee glyph is not in the board font).

The defining visual is TWO MONEY LADDERS: on Ramesh's simple-interest ladder a
drawn padlock fixes the principal block while identical interest blocks stack
beside it; on Sreenu's compound ladder the principal and its interest merge into
one block that slides down to become the next year's principal, from which a
larger interest block is cut.  The ladders then give way to algebra, transformed
with TransformMatchingTex so P and the growth factor stay continuous through
P + PR/100 -> P(1 + R/100) -> P(1 + R/100)^2 -> P(1 + R/100)^n.

Title + 10 scenes:
  0. Title: the same Rs 100 at the same 10% for the same 2 years gives Rs 120 by
     one method and Rs 121 by the other -- where did the extra Re 1 come from?
  1. Simple interest: the interest is always on the ORIGINAL principal, so it is
     Rs 10 every year; SI = PTR/100, and Rs 2,500 at 12% for 3 years gives
     Rs 900.
  2. Compound interest: each new amount becomes the next principal, so year two
     earns Rs 11 and the amount is Rs 121 -- the extra rupee is interest on the
     first year's interest.
  3. The one-period growth factor: A1 = P + PR/100 = P(1 + R/100).
  4. Year two: the same factor multiplies again, giving A2 = P(1 + R/100)^2.
  5. n years: one factor per year compresses into a power, A = P(1 + R/100)^n --
     and the exponent counts the growth periods.
  6. The formula gives the AMOUNT, so CI = A - P = P(1 + R/100)^n - P.
  7. Apply it: Rs 5,000 at 8% for 2 years gives Rs 5,832, so CI is Rs 832.
  8. The two ladders side by side, and why SI and CI agree after one period.
  9. Your turn: three exercises and the quick check, after the series' centred
     ten-second THINK clock.
 10. Recap of the derivation, and the spoken thank-you card.
"""'''

# The series' SRT export, with the two-word tail folded into the caption before
# it (a stand-alone last word otherwise lands mostly in silence).
SRT_OLD = '''    def _capture_srt(self, tracker, words_per_line: int = 9) -> None:
        wbs = [
            wb for wb in tracker.data.get("word_boundaries", [])
            if wb.get("text", "").strip()
        ]
        if not wbs:
            return
        starts = [tracker.start_t + wb["audio_offset"] / AUDIO_OFFSET_RESOLUTION
                  for wb in wbs]
        for i in range(0, len(wbs), words_per_line):
            chunk = wbs[i:i + words_per_line]
            chunk_starts = starts[i:i + words_per_line]
            end = starts[i + words_per_line] if i + words_per_line < len(starts) \\
                else tracker.end_t
            text = " ".join(wb["text"] for wb in chunk)
            self._srt_entries.append((chunk_starts[0], end, text))'''

SRT_NEW = '''    def _capture_srt(self, tracker, words_per_line: int = 9) -> None:
        """Ground-truth export, with one change: a final chunk of one or two
        words is folded into the caption before it.  A stand-alone last word
        keeps its own half-second caption, which lands mostly in silence at the
        end of the piece and reads badly."""
        wbs = [wb for wb in tracker.data.get("word_boundaries", [])
               if wb.get("text", "").strip()]
        if not wbs:
            return
        starts = [tracker.start_t + wb["audio_offset"] / AUDIO_OFFSET_RESOLUTION
                  for wb in wbs]
        chunks = []
        for i in range(0, len(wbs), words_per_line):
            chunk = wbs[i:i + words_per_line]
            end = starts[i + words_per_line] if i + words_per_line < len(starts) \\
                else tracker.end_t
            chunks.append([starts[i], end, list(chunk)])
        if len(chunks) > 1 and len(chunks[-1][2]) <= 2:
            tail = chunks.pop()
            chunks[-1][1] = tail[1]
            chunks[-1][2].extend(tail[2])
        for start, end, chunk in chunks:
            text = " ".join(wb["text"] for wb in chunk)
            self._srt_entries.append((start, end, text))'''

CONSTRUCT_OLD = """        self.beat0_title()
        self.beat1_data()
        self.beat2_split()
        self.beat3_choose()
        self.beat4_diagonal()
        self.beat5_triangle()
        self.beat6_locate_d()
        self.beat7_complete()
        self.beat8_method()
        self.beat9_challenge()
        self.beat10_recap()"""

CONSTRUCT_NEW = """        self.beat_title()
        self.beat_s1()
        self.beat_s2()
        self.beat_s3()
        self.beat_s4()
        self.beat_s5()
        self.beat_s6()
        self.beat_s7()
        self.beat_s8()
        self.beat_s9()
        self.beat_s10()"""


def section(text: str, start: str, end: str) -> tuple[int, int]:
    i = text.index(start)
    j = text.index(end, i)
    return i, j


def main() -> None:
    src = SRC.read_text(encoding="utf-8")
    frag = FRAG.read_text(encoding="utf-8")
    beats = BEATS.read_text(encoding="utf-8")
    beats = beats[beats.index(
        "    # ================================================================ "
        "beats =="):]

    i, j = section(src, '"""', 'from __future__ import annotations')
    out = DOCSTRING + "\n" + src[j:]

    frag_body = frag[frag.index("board layout --"):frag.index("narration --")]
    furniture = frag_body.split("\n", 1)[1].strip()
    narration = "NARRATION = {" + frag.split("NARRATION = {", 1)[1]
    i, j = section(out, "NARRATION = {",
                   "class ConstructQuadrilateral4Sides1DiagonalStory")
    out = out[:i] + furniture + "\n\n\n" + narration.rstrip() + "\n\n\n" + out[j:]

    out = out.replace("class ConstructQuadrilateral4Sides1DiagonalStory",
                      f"class {CLASS}")
    src_key = '"construct_quadrilateral_4sides_1diagonal"'
    assert out.count(src_key) == 1, out.count(src_key)
    out = out.replace(src_key, f'"{MODULE_KEY}"')

    assert out.count(CONSTRUCT_OLD) == 1
    out = out.replace(CONSTRUCT_OLD, CONSTRUCT_NEW)
    assert out.count(SRT_OLD) == 1, out.count(SRT_OLD)
    out = out.replace(SRT_OLD, SRT_NEW)

    i = out.index("    # =========================================================="
                  "====== beats ==")
    out = out[:i] + beats

    OUT.write_text(out, encoding="utf-8")
    print(f"wrote {OUT}  ({len(out.splitlines())} lines)")
    for token in (CLASS, MODULE_KEY, "beat_title", "beat_s1", "beat_s10",
                  "method_card", "block_row", "padlock", "ladder",
                  "factor_card", "wrong_card", "play_challenge_countdown",
                  "folded into the caption"):
        print(f"  {token}: {out.count(token)}")


if __name__ == "__main__":
    main()

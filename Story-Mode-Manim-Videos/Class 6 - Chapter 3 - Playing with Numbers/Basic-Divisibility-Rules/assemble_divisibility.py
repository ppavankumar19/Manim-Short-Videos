"""Build this topic's module from the proven video-03 head of the Chapter 3
quadrilaterals set.

That module is the untouched head of the series: the theme and board constants,
the chalkboard backdrop with the student, the teacher and both corner badges,
`reset_board`, `appear`, the crisp-text pacing helpers, the card helpers
(`measure_card`, `check_row`, `summary_row`, `combo_card`, `choice_row`) and the
ground-truth SRT export.  None of that is topic-specific, so it is kept verbatim
and only the topic-specific parts are replaced:

  * the module docstring,
  * the narration table and this topic's layout furniture,
  * the class name and the output path,
  * `_capture_srt` (the series version folds a one-or-two-word tail chunk into
    the caption before it, so no caption lands mostly in silence),
  * every scene beat.

Run from this folder:
    python assemble_divisibility.py
"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAPTER = next(p for p in HERE.parents
               if (p / "Chapter 3 - Construction of Quadrilaterals").exists())
SRC = (CHAPTER / "Chapter 3 - Construction of Quadrilaterals"
       / "SSSSD-4-Sides-1-Diagonal"
       / "construct_quadrilateral_4sides_1diagonal.py")
OUT = HERE / "divisibility_rules_basic_2_3_5_6_9_10.py"
FRAG = HERE / "_divisibility_fragment.py"
BEATS = HERE / "_divisibility_beats.py"

CLASS = "DivisibilityRulesBasicStory"
MODULE_KEY = "divisibility_rules_basic_2_3_5_6_9_10"

DOCSTRING = '''"""
Mastering Basic Divisibility Rules: Quick Tests for 2, 3, 5, 6, 9 and 10
Story-mode chalkboard lesson (Telangana Class 6 Maths, Chapter 3:
Playing with Numbers, Storymode 01).

LLM KEY / FUNCTION NAME: divisibility_rules_basic_2_3_5_6_9_10

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

The defining visual is the Divisibility Scanner: six rules collapse into three
ways of looking at a number --

  * 2, 5, 10  ->  inspect the ones digit only,
  * 3, 9      ->  add all the digits and test that sum,
  * 6         ->  pass the test for 2 AND the test for 3.

Title + 10 scenes:
  0. Title card.
  1. Hasini's 125 chocolates: guessing by dividing is slow.
  2. What "divisible" means: remainder 0 (24 / 4) versus remainder 1 (29 / 4).
  3. Divisibility by 2: the ones digit 0, 2, 4, 6, 8.
  4. Divisibility by 5 and 10, and the last-digit family.
  5. Divisibility by 3: 27 versus 37, then the digit sum of 36129.
  6. Divisibility by 9: the same digit sum, a stronger test (9846).
  7. Divisibility by 6: the test for 2 and the test for 3 together (7224).
  8. One dashboard: last digit / digit sum / combine both.
  9. Your turn: which of 2, 3, 5, 6, 9, 10 divide 12345 exactly?
 10. Recap and thank-you.
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

CONSTRUCT_NEW = """        self.beat0_title()
        self.beat1_chocolate()
        self.beat2_divisible()
        self.beat3_rule2()
        self.beat4_rule5_10()
        self.beat5_rule3()
        self.beat6_rule9()
        self.beat7_rule6()
        self.beat8_application()
        self.beat9_challenge()
        self.beat10_recap()"""


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

    # 1. docstring
    i, j = section(src, '"""', 'from __future__ import annotations')
    out = DOCSTRING + "\n" + src[j:]

    # 2. this topic's board layout, furniture and narration (the head's own
    #    furniture stays: the compass helpers, the card helpers, the frames)
    furniture = frag.split(
        "# ------------------------------------------------------------ "
        "board layout --")[1].split(
        "# ---------------------------------------------------------------- "
        "narration --")[0].strip()
    narration = "NARRATION = {" + frag.split("NARRATION = {", 1)[1]
    i, j = section(out, "NARRATION = {",
                   "class ConstructQuadrilateral4Sides1DiagonalStory")
    out = out[:i] + furniture + "\n\n\n" + narration.rstrip() + "\n\n\n" + out[j:]

    # 3. class name and output path
    out = out.replace("class ConstructQuadrilateral4Sides1DiagonalStory",
                      f"class {CLASS}")
    src_key = '"construct_quadrilateral_4sides_1diagonal"'
    assert out.count(src_key) == 1, out.count(src_key)
    out = out.replace(src_key, f'"{MODULE_KEY}"')

    # 4. the beat calls, and the SRT export with the folded tail
    assert out.count(CONSTRUCT_OLD) == 1
    out = out.replace(CONSTRUCT_OLD, CONSTRUCT_NEW)
    assert out.count(SRT_OLD) == 1, out.count(SRT_OLD)
    out = out.replace(SRT_OLD, SRT_NEW)

    # 5. every scene beat
    i = out.index("    # =========================================================="
                  "====== beats ==")
    out = out[:i] + beats

    OUT.write_text(out, encoding="utf-8")
    print(f"wrote {OUT}  ({len(out.splitlines())} lines)")
    for token in (CLASS, MODULE_KEY, "beat1_chocolate", "beat10_recap",
                  "zone_panel", "digit_tiles", "play_challenge_countdown",
                  "final SRT", "folded into the caption"):
        print(f"  {token}: {out.count(token)}")


if __name__ == "__main__":
    main()


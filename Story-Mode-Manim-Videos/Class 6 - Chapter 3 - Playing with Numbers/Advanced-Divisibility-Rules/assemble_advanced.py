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
    python assemble_advanced.py
"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAPTER = next(p for p in HERE.parents
               if (p / "Chapter 3 - Construction of Quadrilaterals").exists())
SRC = (CHAPTER / "Chapter 3 - Construction of Quadrilaterals"
       / "SSSSD-4-Sides-1-Diagonal"
       / "construct_quadrilateral_4sides_1diagonal.py")
OUT = HERE / "divisibility_rules_advanced_4_8_11.py"
FRAG = HERE / "_advanced_fragment.py"
BEATS = HERE / "_advanced_beats.py"

CLASS = "DivisibilityRulesAdvancedStory"
MODULE_KEY = "divisibility_rules_advanced_4_8_11"

DOCSTRING = '''"""
Advanced Divisibility Tests: How to Instantly Test Divisibility by 4, 8 and 11
Story-mode chalkboard lesson (Telangana Class 6 Maths, Chapter 3:
Playing with Numbers, Storymode 02).

LLM KEY / FUNCTION NAME: divisibility_rules_advanced_4_8_11

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
  - Nothing on the board sits below CAPTION_SAFE_Y (-2.00): the burned-in
    caption grows up from the bottom of the frame.

The defining visual is the scanner from the previous video, upgraded with three
new modes:

  * 4  ->  a TWO-digit lens over the end of the number, because 100 divides by 4,
  * 8  ->  a THREE-digit lens, because 1000 divides by 8,
  * 11 ->  an alternating-position sorter: digits jump into odd/even baskets,
           the two sums are compared, and the difference must be 0 or a
           multiple of 11.

Cold open + title + 11 scenes:
  C. Why these tests? -- the calendar, a tiler and a bank (real-world hook).
  0. Title card.
  1. The scanner gains three modes: 4, 8 and 11.
  2. Why 4 needs only two digits (76532 = 76500 + 32, and 100 = 4 x 25).
  3. Apply it to the textbook's 56496 (last two digits 96 = 4 x 24).
  4. Why 8 needs three digits (1000 = 8 x 125, 93624 = 93000 + 624).
  5. Two lenses on one number (2104): 4 looks at two, 8 looks at three.
  6. Divisibility by 11: 1221 -> (1+2) and (2+1), difference 0.
  7. The same test failing: 6535 -> 10 - 9 = 1, so not divisible by 11.
  8. Three rules, three clues: last 2 / last 3 / alternating sums.
  9. A real stadium: 56496 seats into four-seat boxes, nothing left over.
 10. Your turn, staged: 726352 by 4 and 8 on the left, cleared, then 10824 by
    11 centred in larger type.
 11. Recap and thank-you.
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

CONSTRUCT_NEW = """        self.beat_cold_open()
        self.beat0_title()
        self.beat1_hook()
        self.beat2_why4()
        self.beat3_apply4()
        self.beat4_why8()
        self.beat5_two_lenses()
        self.beat6_rule11()
        self.beat7_11_fails()
        self.beat8_dashboard()
        self.beat_apply()
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
    for token in (CLASS, MODULE_KEY, "beat1_hook", "beat6_rule11",
                  "beat10_recap", "digit_lens", "basket", "place_tags",
                  "play_challenge_countdown", "folded into the caption"):
        print(f"  {token}: {out.count(token)}")


if __name__ == "__main__":
    main()

"""Build this topic's module from the proven head of the Chapter 3
quadrilaterals set.

That module is the untouched head of the series: the theme and board constants,
the chalkboard backdrop with the student, the teacher and both corner badges,
`reset_board`, `appear`, the crisp-text pacing helpers and the ground-truth SRT
export.  None of that is topic-specific, so it is kept verbatim and only the
topic-specific parts are replaced:

  * the module docstring,
  * the narration table and this topic's percentage furniture,
  * the class name and the output path,
  * `_capture_srt` (the series version folds a one-or-two-word tail chunk into
    the caption before it, so no caption lands mostly in silence),
  * every scene beat.

Run from this folder:
    python assemble_percentage.py
"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAPTER = next(p for p in HERE.parents
               if (p / "Chapter 3 - Construction of Quadrilaterals").exists())
SRC = (CHAPTER / "Chapter 3 - Construction of Quadrilaterals"
       / "SSSSD-4-Sides-1-Diagonal"
       / "construct_quadrilateral_4sides_1diagonal.py")
OUT = HERE / "percentage_applications_and_estimation.py"
FRAG = HERE / "_percentage_fragment.py"
BEATS = HERE / "_percentage_beats.py"

CLASS = "PercentageApplicationsAndEstimationStory"
MODULE_KEY = "percentage_applications_and_estimation"

DOCSTRING = '''"""
Percentage Increases, Decreases & Quick Estimation Rules on Bills
Story-mode chalkboard lesson (Class 8 Maths, Chapter 5: Comparing Quantities
using Proportion, Storymode 02).

LLM KEY / FUNCTION NAME: percentage_applications_and_estimation

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

The defining visual is the PERCENTAGE CONTROL PANEL: three modes (CONVERT,
CHANGE, ESTIMATE) stay on the board while every scene lights the one it needs.
Under it the lesson draws hundred-cell percentage squares that fill cell by
cell, the 100% original bar with a block that visibly ATTACHES for an increase
and a block that visibly LEAVES for a decrease, rupee notes and coins, a price
tag, a bill on a ruler that snaps from 477.80 to 480, and a ten-percent block
that splits in half to make five percent.

Title + 10 scenes:
  0. Title card: 225 of 300 against 200 of 250 -- who did better?
  1. Converting to one scale: 3/4 = 75% and 4/5 = 80%, and the rule
     percentage = part / whole x 100%.
  2. A 35% increase: the original is a full 100% bar and a 35% block attaches
     to it, so the new value is 135% of the original.
  3. Applying it: sales of Rs 98,700 up 35% -- the increase is Rs 34,545 and
     the new figure is Rs 1,33,245, the same as 135% of 98,700.
  4. A 10% decrease: a Rs 550 tag with 10% off pays Rs 495; the comparison
     panel sets increase p% -> 100% + p% and decrease p% -> 100% - p%.
  5. The mental toolkit: 10% = one tenth, 5% = half of 10%, 15% = 10% + 5%,
     20% = two tens -- demonstrated on 480 to give 72.
  6. Estimation on a bill: Rs 477.80 rounds to 480, 15% of that is 72, so the
     payment is about Rs 408, that is about Rs 410.
  7. Exact versus estimate: 15% of 477.80 is 71.67 and the exact answer is
     406.13 -- close enough to show that the estimate is sensible, and that an
     estimate is a reasonableness check, not exact arithmetic.
  8. The decision map: convert, increase, decrease, estimate.
  9. Your turn: four checks (18 of 24, 10% off Rs 800, 20% of 357.30, and a
     35% rise on Rs 900) after the series' centred ten-second THINK clock.
 10. Recap: compare, change, estimate, check -- and the spoken thank-you card.
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

# The head writes its ground-truth SRT under `media/videos/<module>/360p30/`:
# this topic's folder name pushes `<Class>.real.srt` to exactly 260 characters,
# one over the limit a plain open accepts while Windows' long-path support is
# off.  The head's four writes therefore go through the fragment's
# long-path-safe `write_board_file` helper.
SRT_WRITE_OLD = '''        srt_path.write_text("\\n".join(lines), encoding="utf-8")
        print(f"[real SRT written] {srt_path}")
        (out_dir / "real.srt").write_text("\\n".join(lines), encoding="utf-8")'''

SRT_WRITE_NEW = '''        write_board_file(srt_path, "\\n".join(lines))
        print(f"[real SRT written] {srt_path}")
        write_board_file(out_dir / "real.srt", "\\n".join(lines))'''

SRT_TREE_OLD = '''                (movie_dir / "real.srt").write_text("\\n".join(lines), encoding="utf-8")
                (movie_dir / f"{self.__class__.__name__}.real.srt").write_text(
                    "\\n".join(lines), encoding="utf-8")'''

SRT_TREE_NEW = '''                write_board_file(movie_dir / "real.srt", "\\n".join(lines))
                write_board_file(
                    movie_dir / f"{self.__class__.__name__}.real.srt",
                    "\\n".join(lines))'''

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

    assert out.count(SRT_WRITE_OLD) == 1, out.count(SRT_WRITE_OLD)
    out = out.replace(SRT_WRITE_OLD, SRT_WRITE_NEW)
    assert out.count(SRT_TREE_OLD) == 1, out.count(SRT_TREE_OLD)
    out = out.replace(SRT_TREE_OLD, SRT_TREE_NEW)

    i = out.index("    # =========================================================="
                  "====== beats ==")
    out = out[:i] + beats

    OUT.write_text(out, encoding="utf-8")
    print(f"wrote {OUT}  ({len(out.splitlines())} lines)")
    for token in (CLASS, MODULE_KEY, "beat_title", "beat_s1", "beat_s10",
                  "mode_panel", "percent_grid", "pct_bar", "pct_block",
                  "money_note", "money_bag", "price_tag", "receipt",
                  "number_ruler", "split_block", "play_challenge_countdown",
                  "folded into the caption"):
        print(f"  {token}: {out.count(token)}")


if __name__ == "__main__":
    main()

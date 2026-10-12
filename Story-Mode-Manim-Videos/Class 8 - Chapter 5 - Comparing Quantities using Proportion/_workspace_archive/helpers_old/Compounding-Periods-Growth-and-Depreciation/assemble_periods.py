"""Build this topic's module from the proven head of the Chapter 3
quadrilaterals set.

That module is the untouched head of the series: the theme and board constants,
the chalkboard backdrop with the student, the teacher and both corner badges,
`reset_board`, `appear`, the crisp-text pacing helpers and the ground-truth SRT
export.  None of that is topic-specific, so it is kept verbatim and only the
topic-specific parts are replaced:

  * the module docstring,
  * the narration table and this topic's compounding-clock furniture,
  * the class name and the output path,
  * `_capture_srt` (the series version folds a one-or-two-word tail chunk into
    the caption before it, so no caption lands mostly in silence),
  * every scene beat.

Run from this folder:
    python assemble_periods.py
"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAPTER = next(p for p in HERE.parents
               if (p / "Chapter 3 - Construction of Quadrilaterals").exists())
SRC = (CHAPTER / "Chapter 3 - Construction of Quadrilaterals"
       / "SSSSD-4-Sides-1-Diagonal"
       / "construct_quadrilateral_4sides_1diagonal.py")
OUT = HERE / "compounding_periods_half_yearly_quarterly_depreciation.py"
FRAG = HERE / "_periods_fragment.py"
BEATS = HERE / "_periods_beats.py"

CLASS = "CompoundingPeriodsHalfYearlyQuarterlyDepreciationStory"
MODULE_KEY = "compounding_periods_half_yearly_quarterly_depreciation"

DOCSTRING = '''"""
Compounding Half-Yearly, Quarterly & Applications to Population Growth and
Depreciation
Story-mode chalkboard lesson (Class 8 Maths, Chapter 5: Comparing Quantities
using Proportion, Storymode 04).

LLM KEY / FUNCTION NAME: compounding_periods_half_yearly_quarterly_depreciation

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

The defining visual is the COMPOUNDING CLOCK: one one-year dial that physically
splits into two six-month sectors and then into four quarter sectors, while the
rate card splits with it (R -> R/2 -> R/4) and the period counter moves
(n -> 2n -> 4n).  The same P(1 + r)^n structure then drives a rising village and
a shrinking value bar with a ball that loses height at every bounce.

Title + 11 scenes (thirteen pieces):
  0. Title card: the lesson's four parts, chalked on a bare board.
  1. The conversion period: the interval after which interest is added.
  2. The half-yearly rule: the rate halves AND the periods double together.
  3. The worked example: 1000(1.05)^2 = Rs 1,102.50, CI = Rs 102.50.
  4. Quarterly: R/4 and 4n, the same rule extended to four periods.
  5. Population growth: the new total is the next period's base.
  6. Depreciation: (100 - R)% is kept, and the bouncing ball.
  7. One structure, three uses: growth up, depreciation down.
  8. The five-step decision map.
  9. Your turn: half-yearly, quarterly, depreciation and the quick check after
     the series' centred ten-second THINK clock.
 10. The summary: the three conversion periods, the two mixed formulas and the
     five steps gathered on one board.
 11. Recap: period, rate, factor, repeat -- and the spoken thank-you card.
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
        self.beat_s10()
        self.beat_s11()"""

# This topic's class name pushes the media path past the 260-character MAX_PATH
# limit, so the ground-truth SRT is written through the extended-length form
# (the chapter pipeline renders into the short D:\m3 media dir and copies back).
SRT_WRITE_OLD = '''        srt_path.write_text("\\n".join(lines), encoding="utf-8")
        print(f"[real SRT written] {srt_path}")
        (out_dir / "real.srt").write_text("\\n".join(lines), encoding="utf-8")'''

SRT_WRITE_NEW = '''        write_text_long(srt_path, "\\n".join(lines))
        print(f"[real SRT written] {srt_path}")
        write_text_long(out_dir / "real.srt", "\\n".join(lines))'''


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

    i = out.index("    # =========================================================="
                  "====== beats ==")
    out = out[:i] + beats

    OUT.write_text(out, encoding="utf-8")
    print(f"wrote {OUT}  ({len(out.splitlines())} lines)")
    for token in (CLASS, MODULE_KEY, "beat_title", "beat_s1", "beat_s11",
                  "clock_face", "clock_sectors", "village", "value_bar",
                  "bounce_track", "car_icon", "note_stack", "wrong_card",
                  "play_challenge_countdown", "folded into the caption"):
        print(f"  {token}: {out.count(token)}")


if __name__ == "__main__":
    main()

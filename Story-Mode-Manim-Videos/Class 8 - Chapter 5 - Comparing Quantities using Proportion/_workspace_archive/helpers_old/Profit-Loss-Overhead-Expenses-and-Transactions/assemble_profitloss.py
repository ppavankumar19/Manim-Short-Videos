"""Build this topic's module from the proven head of the Chapter 3
quadrilaterals set.

That module is the untouched head of the series: the theme and board constants,
the chalkboard backdrop with the student, the teacher and both corner badges,
`reset_board`, `appear`, the crisp-text pacing helpers and the ground-truth SRT
export.  None of that is topic-specific, so it is kept verbatim and only the
topic-specific parts are replaced:

  * the module docstring,
  * the narration table and this topic's ledger furniture,
  * the class name and the output path,
  * `_capture_srt` (the series version folds a one-or-two-word tail chunk into
    the caption before it, so no caption lands mostly in silence),
  * every scene beat.

Run from this folder:
    python assemble_profitloss.py
"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAPTER = next(p for p in HERE.parents
               if (p / "Chapter 3 - Construction of Quadrilaterals").exists())
SRC = (CHAPTER / "Chapter 3 - Construction of Quadrilaterals"
       / "SSSSD-4-Sides-1-Diagonal"
       / "construct_quadrilateral_4sides_1diagonal.py")
OUT = HERE / "profit_loss_overhead_expenses_and_transactions.py"
FRAG = HERE / "_profitloss_fragment.py"
BEATS = HERE / "_profitloss_beats.py"

CLASS = "ProfitLossOverheadExpensesAndTransactionsStory"
MODULE_KEY = "profit_loss_overhead_expenses_and_transactions"

DOCSTRING = '''"""
Profit, Loss & Overhead Expenses: Solving Single and Double Transaction
Problems
Story-mode chalkboard lesson (Class 8 Maths, Chapter 5: Comparing Quantities
using Proportion, Storymode 02).

LLM KEY / FUNCTION NAME: profit_loss_overhead_expenses_and_transactions

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

The defining visual is the TRANSACTION LEDGER: a two-column book (MONEY OUT
against MONEY IN) that every scene keeps on the board.  The purchase price sits
at the head of the money-out column, the expense tags -- truck for transport,
spanner for repairs -- dock under it, and all of them flow into one shaded
TOTAL COST PRICE box.  A two-pan balance compares money out with money in (the
money-in side rising is a profit, the money-out side rising is a loss), two
item ledgers physically merge into one total ledger, and the tempting
"+20% and -20% give 0%" is stopped, pulled apart and replaced by the two real
cost prices it was hiding.

Title + 10 scenes:
  0. Title: the purchase price is not the real cost -- Rs 5,600, not Rs 5,000.
  1. Profit, loss, or neither: compare first, then subtract -- with the balance.
  2. The percentage: profit and loss percent are both taken on the cost price,
     and the tempting profit/SP x 100 is struck through.
  3. The refrigerator ledger: Rs 5,000 + Rs 100 + Rs 500 = Rs 5,600 cost,
     Rs 7,000 sold, Rs 1,400 profit, 25%.
  4. The same ledger with a loss: the flat, Rs 4,60,000 cost, Rs 4,25,500 sold,
     Rs 34,500 lost, 7.5%.
  5. The two-item trap: +20% and -20% do NOT cancel -- the two cost prices are
     recovered from their different bases.
  6. The whole transaction: Rs 6,250 cost against Rs 6,000 selling price, a
     loss of Rs 250, that is 4%.
  7. The decision process: five steps, and the totals for several items.
  8. Spoiled stock still costs: the bananas, and the overheads that stay.
  9. Your turn: two problems after the series' centred ten-second THINK clock.
 10. Recap: overheads, comparison, percentage base, totals -- and the spoken
     thank-you card.
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


# This topic's media path is longer than the 260-character MAX_PATH limit, so
# the ground-truth SRT write goes through the extended-length form when the
# operating system refuses the plain path (the render itself is done into the
# short D:\m3 media dir by the chapter pipeline).
WRSRT_OLD = '''        srt_path.write_text("\\n".join(lines), encoding="utf-8")
        print(f"[real SRT written] {srt_path}")
        (out_dir / "real.srt").write_text("\\n".join(lines), encoding="utf-8")'''

WRSRT_NEW = '''        write_text_long(srt_path, "\\n".join(lines))
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
    assert out.count(WRSRT_OLD) == 1, out.count(WRSRT_OLD)
    out = out.replace(WRSRT_OLD, WRSRT_NEW)

    i = out.index("    # =========================================================="
                  "====== beats ==")
    out = out[:i] + beats

    OUT.write_text(out, encoding="utf-8")
    print(f"wrote {OUT}  ({len(out.splitlines())} lines)")
    for token in (CLASS, MODULE_KEY, "beat_title", "beat_s1", "beat_s10",
                  "ledger_frame", "total_box", "balance_rig", "mini_ledger",
                  "two_col_row", "wrong_card", "banana_bunch",
                  "write_text_long", "play_challenge_countdown",
                  "folded into the caption"):
        print(f"  {token}: {out.count(token)}")


if __name__ == "__main__":
    main()

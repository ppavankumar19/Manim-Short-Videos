"""Build this topic's module from the proven video-03 head of the Chapter 3
quadrilaterals set.

That module is the untouched head of the series: the theme and board constants,
the chalkboard backdrop with the student, the teacher and both corner badges,
`reset_board`, `appear`, the crisp-text pacing helpers, the card helpers and the
ground-truth SRT export.  None of that is topic-specific, so it is kept verbatim
and only the topic-specific parts are replaced:

  * the module docstring,
  * the narration table and this topic's parallel-lines furniture,
  * the class name and the output path,
  * `_capture_srt` (the series version folds a one-or-two-word tail chunk into
    the caption before it, so no caption lands mostly in silence),
  * every scene beat.

Run from this folder:
    python assemble_pangles.py
"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAPTER = next(p for p in HERE.parents
               if (p / "Chapter 3 - Construction of Quadrilaterals").exists())
SRC = (CHAPTER / "Chapter 3 - Construction of Quadrilaterals"
       / "SSSSD-4-Sides-1-Diagonal"
       / "construct_quadrilateral_4sides_1diagonal.py")
OUT = HERE / "parallel_lines_and_angles.py"
FRAG = HERE / "_pangles_fragment.py"
BEATS = HERE / "_pangles_beats.py"

CLASS = "ParallelLinesAndAnglesStory"
MODULE_KEY = "parallel_lines_and_angles"

DOCSTRING = '''"""
Angles and Parallel Lines: the Six Relationships, and the Equation They Give
Story-mode chalkboard lesson (Class 8 Mathematics, Chapter 2: Linear Equations
in One Variable -- Applications of Angles and Parallel Lines).

LLM KEY / FUNCTION NAME: parallel_lines_and_angles

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

The defining visual is ONE FIGURE: two parallel lines, each carrying the same
chevron arrow mark, cut by a single transversal, making eight angles.  Every
relationship is then revealed by changing only the emphasis -- the pair of
wedges is lit in its own colour while the other six stay pale -- and the video
ends by turning one of those rules into a linear equation and solving it.

Title + 10 scenes:
  0. Title card: eight angles, six relationships, one equation.
  1. Parallel lines and the transversal: what the words mean.
  2. Eight angles at two crossings, and the interior/exterior regions.
  3. Vertically opposite angles are equal; a linear pair adds to 180.
  4. Corresponding angles are equal (1=5, 2=6, 3=7, 4=8).
  5. Alternate interior angles are equal (4=5, 3=6).
  6. Same-side interior angles add to 180 (3+5, 4+6).
  7. The two exterior rules: alternate exterior equal, same-side exterior 180.
  8. The application: same-side interior -> (3x+20)+(5x-8)=180 -> x=21,
     and the angles 83 and 97 degrees.
  9. Your turn: name each relationship, then find x -- after the series'
     centred ten-second THINK clock.
 10. The six relationships in one list, and the spoken thank-you card.
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
        self.beat_s9q()
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
                  "par_pair", "transversal", "angle_sector", "angle_arc",
                  "angle_pos", "band", "chevron", "play_challenge_countdown",
                  "folded into the caption"):
        print(f"  {token}: {out.count(token)}")


if __name__ == "__main__":
    main()

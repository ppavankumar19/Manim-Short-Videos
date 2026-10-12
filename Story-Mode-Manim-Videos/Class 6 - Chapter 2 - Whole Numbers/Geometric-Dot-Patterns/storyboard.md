# Production-Ready Storyboard

**VIDEO TITLE:** Geometric Dot Patterns
**TOPIC:** Patterns with Dots — Lines, Rectangles, Squares and Triangles, and
Using Them to Calculate Faster
**CLASS / CHAPTER:** Class 6 Mathematics — Chapter 2 — Whole Numbers
**STORYMODE:** 05 (fifth video of the Class 6 Chapter 2 set)
**DURATION (measured):** 4 min 24 s (264.03 s), 360p30 master (1080p60 to follow)
**TEXTBOOK REFERENCE:** Telangana SCERT, Class VI Mathematics (English Medium),
2025–26 edition, Chapter 2 — Whole Numbers: the patterns section that builds
lines, rectangles, squares and triangles from dots.

---

## Learning Objective

By the end of this video, students should be able to:

- See that the same number of dots can be arranged in different shapes.
- Read a rectangle as a multiplication (`2 × 3 = 6`) and a line as repeated
  addition (`1 + 2 = 3`).
- Recognise square numbers (`4, 9, 16, …`) as equal rows and columns.
- Recognise triangular numbers (`3, 6, 10, …`) as growing rows.
- Use a nearby round number to calculate faster (`296 ± 9`, `296 ± 99`).
- Apply the same idea inside a bracket (`65 × 99 = 65(100 − 1) = 6435`).
- Solve a two-part challenge independently.

**Primary takeaway:** A dot pattern shows *why* a calculation works, and a
pattern lets you replace a hard calculation with an easy one.

## Historical / Why-Needed Hook

A puzzle rather than history — six dots, one arrangement at a time:

```
. . .        . .        .
. . .        . .       . .
             . .      . . .
```

All three arrangements use six dots, and six can therefore be read three ways:
`6 = 2 × 3 = 1 + 2 + 3`. Opening question: **"Can six dots make different
shapes without adding or removing a single dot?"**

## Core Visual Metaphor

Four connected dot patterns, one idea each:

- **Visual A — the line.** Two dots, then three, then four, then five: each step
  adds exactly one dot, so the pattern is `2, 3, 4, 5, …`.
- **Visual B — the rectangle.** Six dots as two rows of three: the rows are read
  as addition (`3 + 3 = 6`) and then as multiplication (`2 × 3 = 6`).
- **Visual C — the square.** `2 × 2` grows to `3 × 3` and then `4 × 4`, keeping
  every earlier dot on the board: the square numbers are `4, 9, 16, …`.
- **Visual D — the triangle.** Rows of one, two, three and four dots: the
  triangular numbers are `3, 6, 10, …`, and the tenth dot is the fourth row.

## Mathematical Content

| Concept | Pattern | Example |
|---|---|---|
| One number, many shapes | `6 = 2 × 3 = 1 + 2 + 3` | six dots as a rectangle and as a triangle |
| Line pattern | `2, 3, 4, 5, …` (one more each time) | `2` dots, then `3`, `4`, `5` |
| Rectangle → product | rows × columns | `2 × 3 = 6`, `3 + 3 = 6` |
| Square numbers | equal rows and columns | `2×2=4`, `3×3=9`, `4×4=16` |
| Triangular numbers | growing rows | `1+2=3`, `1+2+3=6`, `1+2+3+4=10` |
| Round-number shortcut | `9 = 10 − 1`, `99 = 100 − 1` | `296+9=296+10−1=305` |
| Subtraction case | take away ten, add one back | `296−9=296−10+1=287` |
| Both round numbers | add/subtract one hundred | `296+99=395`, `296−99=197` |
| Bracket, then distribute | `65 × 99 = 65(100−1)` | `6500 − 65 = 6435` |
| Real-life application | split `25` into `20 + 5` | `46 × 25 = 1150` stickers |
| Challenge | both ideas at once | `1+2+3+4=10`, `65 × 999 = 64935` |

## Scene Overview (measured times)

| Scene | Time | Learning goal | Visual | Key on-screen text | Math |
|---|---|---|---|---|---|
| Title | 00:00–00:11 | Frame the topic | Title + dot motifs | Geometric Dot Patterns | `2×3=6` |
| 1 | 00:11–00:33 | One number, many shapes | Six scattered dots → line → 2×3 → triangle | A Dot Puzzle | `6=2×3`, `6=1+2+3` |
| 2 | 00:33–00:50 | Grow a line | Dots added one at a time | Line Pattern | `2,3,4,5,…` |
| 3 | 00:50–01:07 | Rows become a product | Six dots as 2×3, rows counted | 3+3=6 → 2×3=6 | `2×3=6` |
| 4 | 01:08–01:23 | Square numbers | 2×2 → 3×3 → 4×4, old dots kept | SQUARE NUMBERS | `4,9,16,…` |
| 5 | 01:24–01:47 | Triangular numbers | Rows 1,2,3,4 + running sums | Triangle = Growing Rows | `1+2+3+4=10` |
| 6 | 01:47–02:20 | Round-number shortcut | `296+9` → `296+10−1` → `305` | Use Round Numbers! | `296±9`, `296±99` |
| 7 | 02:21–02:45 | The shortcut in a bracket | `65×99 → 65(100−1)`, two arrows | Multiply by 100, Subtract Once | `6500−65=6435` |
| 8 | 02:45–03:11 | Real-life application | Packets of stickers, `25=20+5` | Break Numbers Into Easy Parts | `46×25=1150` |
| 9 | 03:11–03:57 | Student challenge | Triangle + `65×999=?`, THINK clock, reveal | YOUR TURN | `1+2+3+4=10`, `64935` |
| 10 | 03:58–04:24 | Recap | Four shapes, both sequences, recap rows | See the Pattern. Simplify the Calculation. | three rules |

## Scene Notes (Manim implementation)

- **Scene 1:** six `Dot`s start scattered and are *moved* — never re-created —
  into a line, then into a `dot_grid(2, 3)`, then into `triangle_rows(3)`; the
  counter `6` stays in place while the equations `6=2×3` and `6=1+2+3` appear.
- **Scene 2:** a two-dot line grows to five dots, each step a separate
  `FadeIn` of one new `Dot`, with the count above the line transforming each
  time; the sequence `2, 3, 4, 5, …` and the note close the scene.
- **Scene 3:** `dot_grid(2, 3)`; each row gets its own label, `3+3=6` is written,
  then `TransformMatchingTex` turns it into `2×3=6` inside a highlight box.
- **Scene 4:** the 2×2 grid grows to 3×3 and 4×4 by moving every existing dot to
  its new slot and fading the new dots in from above, so all sixteen dots are
  visible at the end; the equation transforms `2×2=4 → 3×3=9 → 4×4=16`, and the
  sequence `4, 9, 16, …` closes the scene.
- **Scene 5:** `triangle_rows(4)` with a label on each row; the running sum
  transforms `1+2=3 → 1+2+3=6 → 1+2+3+4=10`, a question text appears before the
  fourth row, and the scene closes on `3, 6, 10, …` boxed.
- **Scene 6:** `296+9` with the `9 is almost 10` tag, `9=10−1`, then
  `296+10−1` by `TransformMatchingTex`; four results are written in turn
  (`305`, `287`, `395`, `197`) and the scene closes on the combined rule
  `9 = 10 − 1        99 = 100 − 1`.
- **Scene 7:** `65×99` with the `99=100−1` note, then the bracket
  `65(100−1)` built from separate `MathTex` parts with **two** `dist_arrow`s
  running from `65` to `100` and to `1`, then
  `(65×100)−(65×1) → 6500−65 → 6435` boxed.
- **Scene 8:** three `packet_icon`s with the labels `25 stickers per packet` and
  `46 packets`; `46×25 → 46(20+5) → (46×20)+(46×5) → 920+230` and the boxed
  `1150 stickers`.
- **Scene 9:** the triangle of six dots with the question, and `65×999=?`;
  after the four-second THINK clock the reveal adds the fourth row, writes
  `1+2+3+4=10`, and transforms `999=1000−1 → 65(1000−1) → 65000−65 → 64935`.
- **Scene 10:** the four shapes with their labels, both sequences, the two
  round-number rules, then the three recap rows with the takeaway line, and
  finally the **Thank-You template only**.

## Key Pedagogical Safeguards

1. **Dots are moved, never re-created.** In Scene 1 the same six dots become the
   line, the rectangle and the triangle, which is what makes
   `6 = 2 × 3 = 1 + 2 + 3` believable.
2. **The rectangle is read twice.** Addition first (`3 + 3 = 6`, the rows),
   multiplication second (`2 × 3 = 6`, rows × columns) — the multiplication is a
   *shortcut for* the addition, not a replacement for it.
3. **Square numbers keep their history.** Growing 2×2 → 3×3 → 4×4 never clears
   the board, so `1, 4, 9, 16` are visibly nested.
4. **Round numbers are shown as a rule, not a trick.** `9 = 10 − 1` and
   `99 = 100 − 1` are written before any shortcut is used, and both the addition
   and the subtraction case are worked (`+9`, `−9`, `+99`, `−99`).
5. **Two arrows again.** Inside `65(100−1)` a separate arrow runs to each term,
   matching the distributive property taught in the previous video.
6. **The challenge is mirrored by the reveal:** the same triangle and the same
   `65 × 999` question return, and both answers are worked in full.

## Final Production Check

Delivered as `dot_patterns_story.py` (`DotPatternsStory`):

- **Masters:** `media/videos/dot_patterns_story/1080p60/DotPatternsStory_captioned.mp4`
  (1920×1080, 60 fps, 266.4 s) — the delivered master — and the 360p30 review
  copy, both with the series caption style burned in.
- **Layout pass (final):** four corrections after the first 1080p60 render —
  the six dots in scene 1 line up *centred on the board* (the line used to sit
  half a unit left of the rectangle and triangle it is compared with); the count
  `6` moved from the far right edge down to sit level with the shape area; the
  closing question in scene 1 now fades out on its own before `6=2×3` and
  `6=1+2+3` are written (a single cross-fading play left the question and the
  equations on top of each other); the `25` on each sticker packet in scene 8
  clears the sticker circle (it used to be drawn across the circle's lower edge);
  and the four recap shapes in scene 10 sit on a common baseline with all four
  labels on one line, in four columns evenly spaced about the board centre.
- **Closing narration:** the last line is now spoken as well as written — the
  audio says "Thank you for watching! See you in the next lesson!", with the
  card's second line fading in on that sentence (the TTS was pre-checked before
  the render; the piece grew from 22.6 s to 24.6 s and the caption count from 80
  to 81).
- **Second phrase-level sync pass:** re-checking every window against the real
  (WAV-retimed) word boundaries found one defect and twelve leads still present.
  The `3+3=6` sum in scene 3 started a sentence early and pushed the `2×3=6` rule
  and its tag a beat late; the other twelve were windows whose last play
  multiplied the mark by a fraction, leaving 24–30 % of the window unconsumed so
  the next window's visual appeared during the previous sentence. All are now
  pinned to their own marks.
- **Sync audit** (`audit_sync_overlap.py`) against the real SRT — every beat
  matches its narration exactly:

  | Beat | audio | animation | stretch |
  |---|---|---|---|
  | title | 10.83 s | 10.83 s | 0.00 s |
  | scene1 | 21.76 s | 21.76 s | 0.00 s |
  | scene2 | 16.52 s | 16.52 s | 0.00 s |
  | scene3 | 17.09 s | 17.09 s | 0.00 s |
  | scene4 | 15.65 s | 15.65 s | 0.00 s |
  | scene5 | 23.34 s | 23.34 s | 0.00 s |
  | scene6 | 33.19 s | 33.19 s | 0.00 s |
  | scene7 | 24.23 s | 24.23 s | 0.00 s |
  | scene8 | 25.33 s | 25.33 s | 0.00 s |
  | scene9_setup | 19.79 s | 19.79 s | 0.00 s |
  | scene9_reveal | 22.49 s | 22.49 s | 0.00 s |
  | scene10 | 22.59 s | 22.88 s | 0.30 s |

  The single 0.30 s stretch is the closing flourish on the Thank-You card.
- **Phrase-level sync check:** the per-beat audit only measures run-time totals,
  so each scene's animation windows were additionally checked against the real
  TTS word boundaries (new series tool
  `Story-Mode-Manim-Videos/bookmark_times.py`). This found and fixed four
  windows that were a phrase early: the whole recap in Scene 10 (the takeaway
  and the recap rows used to appear one bookmark early and vanished exactly as
  their words were spoken), the 3×3/4×4 growth in Scene 4, the first three steps
  in Scene 5, and the reveal steps in Scene 9. Each animation now happens while
  its own phrase is being spoken.
- **Layout audit:** **0** text-in-text, partial-overlap, out-of-board,
  out-of-board-low, text-on-arrow, near-badge, LaTeX-as-text or empty-TeX
  flags. The 102 `OFF-CENTRE` reports are the dot patterns, the row labels
  beside their own rows and the side-by-side card rows, all of which sit where
  they are being demonstrated. Two earlier defects were fixed here: the
  takeaway line collided with the first recap row, and the recap rows ran below
  the bottom of the board.
- **Content verification on the delivered file:** `verify_sync.py` → **PASS**
  (80 captions, **0 captions in silence**, **0 speech blocks uncaptioned**,
  caption time 250.8 s), and `verify_captions.py` → **PASS** with caption text
  **676 words = narration 676 words**. Every value was checked against the
  textbook: `6=2×3=1+2+3`, `2,3,4,5,…`, `3+3=6`, `2×3=6`, `2×2=4`, `3×3=9`,
  `4×4=16`, `4,9,16,…`, `1+2=3`, `1+2+3=6`, `1+2+3+4=10`, `3,6,10,…`,
  `9=10−1`, `99=100−1`, `296+9=305`, `296−9=287`, `296+99=395`, `296−99=197`,
  `65×99=65(100−1)=6500−65=6435`, `46×25=46(20+5)=920+230=1150`,
  `65×999=65000−65=64935`.
- **Visual proof:** `proof_sync_scene4.png` (the 4×4 grid and `4×4=16` on
  screen while the voice says "four give sixteen dots") and
  `proof_sync_scene10.png` (the takeaway line and the three recap rows on screen
  during "See the pattern, and simplify the calculation").
- **Narration note:** all twelve lines were pre-checked against the TTS before
  rendering (the service occasionally returns an empty response for certain
  phrasings); all twelve passed.

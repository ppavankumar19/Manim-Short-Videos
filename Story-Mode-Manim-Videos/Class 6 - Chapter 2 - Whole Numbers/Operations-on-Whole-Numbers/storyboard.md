# Production-Ready Storyboard

**VIDEO TITLE:** Operations on Whole Numbers
**TOPIC:** Whole Numbers & Operations on the Number Line
**CLASS / CHAPTER:** Class 6 Mathematics — Chapter 2 — Whole Numbers
**STORYMODE:** 02 (second video of the Class 6 Chapter 2 set)
**DURATION (measured):** 3 min 28 s (208.0 s), 360p30 master (1080p60 to follow)
**TEXTBOOK REFERENCE:** Telangana SCERT, Class VI Mathematics (English Medium),
2025–26 edition, Chapter 2, Section 2.3 — Representation of Whole Numbers on
Number Line (printed pages 17–18)

---

## Learning Objective

By the end of this video, students should be able to:

- Recognise and locate whole numbers on a number line.
- Perform addition by moving towards the right.
- Perform subtraction by moving towards the left.
- Understand multiplication as repeated, equal-sized jumps.
- Differentiate between the starting number, the jump size and the number of
  jumps.
- Solve simple whole-number operations visually.

**Primary takeaway:** A number line turns mathematical operations into
movements we can see.

## Historical / Why-Needed Hook

A classroom floor marked with numbers. A student stands on **2**; the teacher
says *"move three steps forward"*. She lands on **5**. Only then does the
equation appear:

```
2 + 3 = 5          forward = add
                   backward = subtract
                   repeating equal jumps = multiply
```

## Core Visual Metaphor

**A character travelling along one continuous number line.**

| Visual element | Meaning |
|---|---|
| Amber marker | starting / current position |
| Green arc | rightward movement (addition) |
| Pink arc | leftward movement (subtraction) |
| Yellow arcs, all the same size | equal jumps (multiplication) |
| Flashing dot | the result / landing position |
| Fixed number line | whole-number positions |

**Continuity rule:** the number line never changes its unit spacing. Only the
marker, the jump arcs and the highlighted landing position move. The jump lift
is computed from the span (`bow_for`), so equal jumps always *look* equal.

## Mathematical Content

| Operation | Movement | Textbook example |
|---|---|---|
| Addition | start at the number, move right | `2 + 3 = 5` |
| Subtraction | start at the number, move left | `6 − 2 = 4` |
| Multiplication | start at 0, make equal jumps | `4 × 2 = 2+2+2+2 = 8` |
| Combined journey | consecutive jumps | `3 + 8 + 5 = 16` |

## Scene Overview

| Scene | Time | Learning goal | Visual | Key on-screen text | Math |
|---|---|---|---|---|---|
| Title | 00:00–00:12 | Frame the topic | Title card + marker on a short line | Operations on Whole Numbers | `0…5` |
| 1 | 00:12–00:28 | Movement is mathematics | Floor tiles 0–5, marker on 2, three steps right | Math can be movement! | `2+3=5` |
| 2 | 00:28–00:50 | Recall the whole-number line | Line 0…10, equal steps | Every step has equal distance. | `W={0,1,2,…}` |
| 3 | 00:50–01:08 | Addition | Line 0…10, three right jumps from 2 | ADDITION → MOVE RIGHT | `2+3=5` |
| 4 | 01:08–01:24 | Subtraction | Same line, two left jumps from 6 | SUBTRACTION → MOVE LEFT | `6-2=4` |
| 5 | 01:24–01:44 | Multiplication | Four equal jumps of 2 from 0 | MULTIPLICATION → EQUAL JUMPS | `4×2=2+2+2+2=8` |
| 6 | 01:44–02:00 | Compare the three | Three stacked mini lines | Right \| Left \| Equal jumps | `+ , − , ×` |
| 7 | 02:00–02:20 | Apply consecutively | Line 0…16, Gayatri's journey | Where will Gayatri reach? | `3+8+5=16` |
| 8 | 02:20–02:32 | Reusable routine | START → OPERATE → MOVE → RESULT cards | Start → Understand → Move → Answer | — |
| 9 | 02:33–03:07 | Student challenge | Line 0…15, THINK clock (4 s), five jumps of 3 | YOUR TURN | `5×3=15` |
| 10 | 03:07–03:28 | Recap | Four summary rows + takeaway | A Number Line Makes Operations Visible! | `2+3`, `6-2`, `4×2`, `5×3` |

## Scene Notes (Manim implementation)

- **Scene 1:** `RoundedRectangle` floor tiles with numbers inside; the amber
  `Dot` marker travels tile to tile while three `CurvedArrow` jumps grow above
  them; the landing tile flashes and `2+3=5` is boxed.
- **Scene 2:** the line is created from the axis, then `0`, then `1–5`, then
  `6–10`; the marker lands on 2 and `W = {0,1,2,…}` appears with the
  "every step has equal distance" rule.
- **Scenes 3/4/5:** one shared builder puts the same `0…10` line on the board
  and replays the operation: heading, the question `2+3=?` / `6-2=?` /
  `4×2=?`, "Start at n.", one arc per jump (each labelled), the landing dot
  flashing, the boxed answer and the movement rule
  (`ADDITION → MOVE RIGHT`, `SUBTRACTION → MOVE LEFT`,
  `MULTIPLICATION → EQUAL JUMPS`). Subtraction passes `direction=-1`, so it
  genuinely starts at 6 and walks left to 4.
- **Scene 6:** three mini number lines stacked (labels every second number);
  the three movements are replayed on their own line, then the comparison
  "Right | Left | Equal jumps" appears.
- **Scene 7:** the textbook game — a 0…16 line with a marker tagged *Gayatri*;
  the three leaps `+3`, `+8`, `+5` are drawn and the running equations
  `0+3=3`, `3+8=11`, `11+5=16` collect in the right column; landing on 16
  flashes and `3+8+5=16` is boxed.
- **Scene 8:** four routine cards with captions, arrows between them, each card
  illuminating in turn, then the strip `Start → Understand → Move → Answer`.
- **Scene 9:** the challenge line 0…15 with every label, the question
  `5×3=?`, the two prompts, the series THINK clock (4 s), then five equal `+3`
  arcs, `3+3+3+3+3=15` and the boxed `5×3=15` with "5 jumps · lands on 15".
- **Scene 10:** four summary rows (addition, subtraction, multiplication and
  `5×3=15`), the takeaway **A Number Line Makes Operations Visible!**, the
  supporting line and the closing sentence; after the summary only the
  **Thank-You template** remains.

## Key Pedagogical Safeguards

1. **Starting position ≠ number of steps.** For `2+3` the marker starts at 2
   and makes three separate one-unit jumps — it never counts five positions
   from zero.
2. **Subtraction moves left, and only whole-number results are shown.**
   `6−2=4` is on the line; `2−5` is never drawn and the line is never extended
   into negative numbers.
3. **Multiplication uses equal jumps.** All four arcs for `4×2` are drawn with
   the same computed lift, so they look identical.
4. **Equal spacing is preserved.** The gap 0→1 always equals the gap 7→8; the
   line is never stretched as the marker advances.
5. **The endpoint is the result, not the jump count.** For `5×3=15` the video
   says "five jumps" and shows the landing position as *fifteen*, with the note
   "5 jumps · lands on 15".

## Final Production Check

Delivered as `operations_on_whole_numbers.py`
(`OperationsOnWholeNumbersStory`):

- **Masters:** `media/videos/operations_on_whole_numbers/360p30/OperationsOnWholeNumbersStory_captioned.mp4`
  (640×360, 30 fps, 207.8 s) — the 1080p60 master follows the review pass.
- **Number-line centring:** `num_line()` used to lay the axis out from a fixed
  left-hand `x0`, which left every line up to 0.56 board units off centre (the
  0–10 line in scenes 3–5 sat 0.3 units left, so the right margin looked wider
  than the left). The helper now shifts the whole group so the numbered dots are
  centred on `BOARD_CX`, and shifts its `grp.x` lookup with it, so markers, jump
  arcs and labels stay on their dots. Every line in the video (title, the 0–10
  game line, the three comparison rows, the 0…16 journey and the 0…15 challenge)
  is now centred on the board.
- **Move-label overlap:** the "ADDITION → MOVE RIGHT" / "SUBTRACTION → MOVE
  LEFT" / "MULTIPLICATION → EQUAL JUMPS" note sat at y = −2.5 while the boxed
  answer sat at y = −2.0, so the box's lower edge ran straight through the words.
  The answer box is now at −1.9 and the note at −2.6, with clear space between.
- **Phrase-level sync pass:** every beat's animation windows were checked
  against the real (WAV-retimed) TTS word boundaries with `bookmark_times.py`,
  which found and fixed ten placements where a visual was attached to the wrong
  sentence. The worst was the whole recap in scene 10: each of the four summary
  rows appeared one sentence early (the subtraction row while the voice said
  "Addition moves right …"), and the takeaway line appeared while the voice said
  "And five times three equals fifteen." Scene 2 showed the dots 1–5 a sentence
  before the counting started and put the `W = {0,1,2,3,…}` set and a stray
  marker on the wrong lines. Scene 9's revealed jumps began during "Let's
  check." and the answer arrived a second early. Scene 1 placed the student's
  marker before she stood on the tile, scene 6's row markers drifted into the
  previous sentence, and scene 8 never highlighted its RESULT card.
- **Sync audit** (`audit_sync_overlap.py`) against the real SRT: **0.00 s**
  animation-vs-audio stretch on every beat (only the closing flourish of the
  summary runs 0.30 s).
- **Layout audit:** no text/text, text/arrow, out-of-board, out-of-board-low,
  badge, LaTeX-as-text, empty-TeX or text-outside-box flags. The remaining
  `OFF-CENTRE` items are the intended layouts — the number lines themselves,
  the jump arcs over their own span and the marker sitting on its position.
- **Content verification on the delivered file:** 55 captions,
  **0 captions in silence**, **0 speech blocks uncaptioned**, caption text
  453 words = narration 453 words, and every operation checked against the
  textbook (`2+3=5` as three right jumps from 2, `6-2=4` as two left jumps from
  6, `4×2=2+2+2+2=8` as four equal jumps from 0, `3+8+5=16` for the Raju /
  Gayatri journey, and `5×3=15` with the note "5 jumps · lands on 15").
- **Caption timing:** the SRT is generated from the same retimed word boundaries
  the animation uses, so the burned captions follow the voice; verified cue by
  cue against the rendered audio (55 cues, first at 0.28 s, last at 205.5 s of a
  207.8 s video).

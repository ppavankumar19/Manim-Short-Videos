# Production-Ready Storyboard

**VIDEO TITLE:** Whole Numbers
**TOPIC:** From Counting to Zero — Natural Numbers, Whole Numbers,
Predecessor & Successor
**CLASS / CHAPTER:** Class 6 Mathematics — Chapter 2 — Whole Numbers
**STORYMODE:** 01 (first video of the Class 6 Chapter 2 set)
**DURATION (measured):** 4 min 36 s (276.2 s), 1080p60 and 360p30 masters
**TEXTBOOK REFERENCE:** Telangana SCERT, Class VI Mathematics (English Medium),
2025–26 edition, Chapter 2, Sections 2.1–2.3 (printed pages 16–17)

---

## Learning Objective

By the end of this video, students should be able to:

- Understand the difference between natural numbers and whole numbers.
- Explain why zero is included in whole numbers.
- Identify the smallest natural and whole numbers.
- Find the predecessor and successor of a number.
- Understand why zero has no predecessor within whole numbers.
- Represent and identify neighbouring whole numbers on a number line.

**Primary takeaway:** Natural numbers help us count. Whole numbers include those
counting numbers **and zero**.

## Historical / Why-Needed Hook

No unrelated historical fact: the video opens with a **pencil box**. Three
pencils are taken out one by one — three, two, one — and then the last pencil
goes, leaving an empty box. That empty box is the reason zero is needed, and the
reason the collection has to grow:

```
3  →  2  →  1  →  0        What number represents nothing?
```

## Core Visual Metaphor

**A counting collection that grows to include zero.**

- **Visual A — the counting collection.** The natural numbers are shown as
  number cards `1, 2, 3, 4, 5, …`; nothing is replaced, a single new card `0`
  travels in and the same collection becomes `0, 1, 2, 3, 4, 5, …`. This makes
  "every natural number is also a whole number" visible.
- **Visual B — the number-line journey.** One step right gives the successor,
  one step left gives the predecessor — where it exists in the collection being
  discussed. Zero is the left end of the whole-number line, so it has no
  predecessor there.

The three recurring assets — **pencil box, number cards, number line** — are
reused across the video instead of being cleared and rebuilt.

## Mathematical Content

| Concept | Representation |
|---|---|
| Natural numbers | `N = {1, 2, 3, 4, …}` |
| Whole numbers | `W = {0, 1, 2, 3, 4, …}` |
| Relationship | `W = N ∪ {0}` , `N ⊂ W` |
| Successor | `n + 1` |
| Predecessor | `n − 1`, when the result belongs to the chosen collection |
| Smallest natural number | `1` |
| Smallest whole number | `0` |

**Boundary conditions that the video states explicitly:**

- In natural numbers, `1` has no predecessor.
- In whole numbers, the predecessor of `1` is `0`.
- Within whole numbers, `0` has no predecessor.
- Every natural and every whole number has a successor; neither collection has
  a greatest number.

## Scene Overview (measured times from the rendered master)

| Scene | Time | Learning goal | Visual | Key on-screen text | Math |
|---|---|---|---|---|---|
| Title | 00:00–00:12 | Frame the topic | Title card + first whole-number line | Whole Numbers / From Counting to Zero | `0,1,2,3,4,5` |
| 1 | 00:12–00:32 | Why zero is needed | Pencil box emptied one pencil at a time | What number represents nothing? | `3→2→1→0` |
| 2 | 00:32–01:04 | Natural → whole numbers | Zero card joins the counting collection | Natural Numbers + Zero = Whole Numbers | `N={1,2,…}`, `W={0,1,…}`, `W=N∪{0}` |
| 3 | 01:04–01:27 | Compare the sets | Two aligned rows of number cards | Only zero is the new addition | `N ⊂ W` |
| 4 | 01:27–01:56 | The whole-number line | Line starting at zero, arrow right | Zero is the starting point | `0,1,2,…,10` |
| 5 | 01:56–02:21 | Predecessor / successor | Line around 9, one-step arrows | Before = Predecessor, After = Successor | `8 ← 9 → 10`, `n±1` |
| 6 | 02:21–02:53 | Boundary cases | Zero and one highlighted | No predecessor within Whole Numbers | `1−1=0`, `0+1=1` |
| 7 | 02:53–03:13 | Apply the rules | Predecessor–Number–Successor cards | One less ← Number → One more | `12,13,14`; `998,999,1000` |
| 8 | 03:13–03:32 | Real-world quantity | Pencil box: add one, remove one | +1 gives the successor | `4+1=5`, `1−1=0` |
| 9 | 03:32–04:07 | Student challenge | Number line 0…12 + THINK clock | YOUR TURN | `11+1=12`, `5−1=4` |
| 10 | 04:07–04:34 | Final recap | Equations + four summary rows | Whole Numbers = Natural Numbers + Zero | `W={0,1,2,…}` |

## Scene Notes (Manim implementation)

- **Title:** title, subtitle and a first whole-number line; zero pulses.
- **Scene 1:** `RoundedRectangle` pencil tray (with an inner panel and a rim)
  holding exactly three pencils; the pencils are faded out one at a time, the
  count `3 → 2 → 1 → ?` transformed with `TransformMatchingTex`, then the boxed
  `0` appears inside the empty box.
- **Scene 2:** the natural row is built from number cards; a `0` card travels in
  from the left and the row *becomes* the whole row (`ReplacementTransform`), so
  no number is ever replaced. Labels swap Natural → Whole, and `W = N ∪ {0}` is
  boxed.
- **Scene 3:** both rows stay on the board; dashed links show the matching
  numbers, zero enlarges, and the two "smallest number" facts plus `N ⊂ W`
  appear.
- **Scene 4:** the line is created from the axis, then `0`, then `1–3`, then
  `4–10`; a green marker walks from 3 to 4 to show "right is greater".
- **Scene 5:** the line centres on 9; a green arrow steps right to 10
  (SUCCESSOR) and a pink arrow steps left to 8 (PREDECESSOR); the general rule
  `Successor = n+1`, `Predecessor = n−1` closes the beat.
- **Scene 6:** `1 − 1 = 0`, then the two membership facts, then a dashed
  boundary at zero with "No predecessor within Whole Numbers", and finally
  `0 + 1 = 1`. **Negative numbers are never mentioned.**
- **Scene 7:** the reusable three-card component; `13` gives `12 | 13 | 14`, and
  when the middle card becomes `999` the neighbours blank to `?` before
  `998 | 999 | 1000` is filled in (no stale neighbours are ever shown).
- **Scene 8:** the pencil box returns; adding a pencil gives `4 + 1 = 5`, and
  removing the last pencil gives `1 − 1 = 0` with "Zero pencils".
- **Scene 9:** the challenge line carries **every number 0…12**; the two
  questions appear, the series THINK clock runs (4 s), then the reveal steps
  `11 → 12` and `5 → 4` with the answers boxed and the closing question
  "Does zero have a predecessor in W?" answered "No."
- **Scene 10:** `N`, `W` and the four summary rows, the takeaway and the
  supporting lines; after the summary only the **Thank-You template** remains.

## Key Pedagogical Safeguards

1. **Zero is never called a natural number.** `N = {1,2,3,…}` and
   `W = {0,1,2,3,…}` are used consistently.
2. **Show why zero is included** — the empty pencil box comes first, the
   definition second.
3. **Distinguish the predecessors of 1 and 0:** in `N`, `1` has no predecessor;
   in `W`, the predecessor of `1` is `0`; within `W`, `0` has no predecessor.
   The video never says zero's predecessor does not exist in mathematics.
4. **Keep number-line distances consistent:** every neighbouring whole number is
   one equal step apart; successor = one step right, predecessor = one step left.

## Final Production Check

Delivered as `whole_numbers_story.py` (`WholeNumbersStory`):

- **Masters:** `media/videos/whole_numbers_story/1080p60/WholeNumbersStory_captioned.mp4`
  (1920×1080, 60 fps, 275.9 s) — the delivered master — and
  `media/videos/whole_numbers_story/360p30/WholeNumbersStory_captioned.mp4`
  (640×360, 30 fps) as the review copy. Both carry the series caption style
  burned in.
- **Pencil-box correction (Scenes 1 and 8):** the box is built with its pencils
  **centred in the tray** — a box of three looks like a box of three, not a box
  of five with two missing. Each removal slides the remaining pencils back to the
  centre, and adding the fifth pencil in Scene 8 pushes the other four apart into
  an evenly spread row of five. The counter always matches what is in the box.
  The pencils themselves are drawn with an explicit body, wooden tip, graphite
  point, metal ferrule and rubber end, inside a tray + inner panel + rim.
- **"Remove the last pencil" bug (Scene 8):** the removal used to fade
  `solo[1]`, the copied *inner tray*, so the box stayed visually occupied while
  the counter read `0`, the equation read `1 − 1 = 0` and "Zero pencils" was
  written underneath. It now fades `solo[3]`, the pencil itself.
- **Phrase-level sync pass:** every beat's animation windows were checked
  against the real TTS word boundaries (`bookmark_times.py`), which found and
  fixed twelve places where a visual was attached to the wrong sentence or the
  wrong part of one — most importantly the two challenge questions
  ("…successor of 11?" appeared during the *predecessor* line, and "Pause and
  try both." faded in across the whole preceding question), the
  successor/predecessor answers in the reveal, the `N`/`W` recap rows in Scene
  10, "Zero pencils" in Scene 8, and the natural / whole set notation in Scene 2.
  The second pass (after the tool was corrected — see below) added four more:
  the title's zero highlight ran 1.9 s early because a `× 0.6` play only consumed
  76% of its window, Scene 4's dots 4–10 arrived a beat late, Scene 2's zero
  flash landed on "three, four and so on" instead of on the word "zero", and
  Scene 8's last-pencil removal started before "a box that has one".
  **Tooling note:** `bookmark_times.py` originally read the TTS *service* word
  times from the voiceover cache, but the render replaces those with times
  re-derived from the real WAV (`synced_voice`), so the cache times drift by up
  to ~2.8 s from what the delivered video uses. The tool now retimes each piece
  from the cached WAV exactly as the render does, so its windows are the ones
  the video actually follows.
- **Layout corrections:** the natural and whole card rows are now aligned so the
  dashed "they match" links are vertical; the `N ⊂ W` box was loosened and its
  block lifted off the bottom rail; the "Natural"/"Whole" labels sit next to the
  rows they name; the successor and predecessor arrows in Scene 5 are at
  different heights with their equations parked to the side (they used to merge
  into one double-headed arrow); the dashed "no predecessor" mark no longer runs
  through the `0` label and the stale predecessor arrow is cleared before the
  successor arrow is drawn in Scene 6; the Scene 7 captions and the `n−1 n n+1`
  terms are centred on the card pitch; and the four-second **THINK clock now
  sits clear of the number line and both questions** instead of covering the
  `5` it asks about.
- **Sync audit** (`audit_sync_overlap.py`) against the real SRT: **0.00 s**
  animation-vs-audio stretch on every beat (only the closing flourish of the
  summary runs 0.30 s).
- **Layout audit:** no text/text, text/arrow, out-of-board, out-of-board-low,
  badge, LaTeX-as-text, empty-TeX or text-outside-box flags. The remaining
  `OFF-CENTRE` items are the intended layouts (number lines, the card rows and
  the labels that sit beside their own dot).
- **Content verification on the delivered 1080p60 master:** 84 captions,
  **0 captions in silence**, **0 speech blocks uncaptioned**, caption text
  706 words = narration 706 words, and every step checked against the textbook
  (`3→2→1→0`, `W = N ∪ {0}`, `N ⊂ W`, `8 ← 9 → 10`, `1−1=0` with no
  predecessor for `0`, `12|13|14`, `998|999|1000`, `4+1=5`, `1−1=0`,
  `11+1=12`, `5−1=4`).

# Production-Ready Storyboard

**VIDEO TITLE:** Distributive Property of Whole Numbers
**TOPIC:** Distributive Property & Identity Elements (0 and 1)
**CLASS / CHAPTER:** Class 6 Mathematics — Chapter 2 — Whole Numbers
**STORYMODE:** 04 (fourth video of the Class 6 Chapter 2 set)
**DURATION (measured):** 4 min 03 s (243.2 s), 360p30 master (1080p60 to follow)
**TEXTBOOK REFERENCE:** Telangana SCERT, Class VI Mathematics (English Medium),
2025–26 edition, Chapter 2, Section 2.4 — Properties of Whole Numbers
(page 24) with an application from Exercise 2.2 (page 25)

---

## Learning Objective

By the end of this video, students should be able to:

- Understand the distributive property through a visual grouping of objects.
- Recognise that multiplication can be distributed across addition.
- Apply the distributive property to simplify calculations.
- Understand the role of zero as the additive identity.
- Understand the role of one as the multiplicative identity.
- Distinguish between distributivity and identity properties.
- Apply these concepts in simple real-world situations.

**Primary takeaway:** Multiplication can be distributed across grouped
quantities, and adding zero or multiplying by one leaves a whole number
unchanged.

## Historical / Why-Needed Hook

A practical puzzle rather than history — twenty dots in five rows of four:

```
5 × 4 = 20      ->      (2 × 4) + (3 × 4) = 8 + 12 = 20
```

Splitting the rectangle changes nothing. Opening question: **"Can we split a
multiplication problem into smaller calculations without changing the answer?"**

## Core Visual Metaphor

Three connected representations:

- **Visual A — the rectangle that splits.** A 5 × 4 dot rectangle divides into
  a 2 × 4 and a 3 × 4 rectangle. *All twenty dots stay on the board; none is
  added or removed.*
- **Visual B — multiplication reaches every term.** Two separate curved arrows
  run from the multiplier to each term inside the bracket
  (`(2+3)×4 → 2×4 + 3×4`). The property is never shown as a single arrow.
- **Visual C — the unchanged number.** Seven counters stay physically
  unchanged: adding an empty container gives `7 + 0 = 7`, and the same seven
  counters regrouped as seven groups of one give `7 × 1 = 7`.

## Mathematical Content

| Concept | General rule | Example |
|---|---|---|
| Distributive over addition | `a(b+c) = ab + ac` | `(2+3)×4 = 2×4 + 3×4` |
| Distributive over subtraction | `a(b−c) = ab − ac` | `12(80−5) = 12×80 − 12×5` |
| Additive identity | `a + 0 = 0 + a = a` | `7 + 0 = 7` |
| Multiplicative identity | `a × 1 = 1 × a = a` | `7 × 1 = 7` |

Worked example: `12 × 75 = 12(70+5) = 840 + 60 = 900` (with `75 = 80 − 5` as a
hint). Real-life: `(56+44) × 30 = 3000`. Challenge: `5(7+8) = 35 + 40 = 75`.

## Scene Overview (measured times)

| Scene | Time | Learning goal | Visual | Key on-screen text | Math |
|---|---|---|---|---|---|
| Title | 00:00–00:10 | Frame the topic | Title + 5×4 grid | Distributive Property | `5×4=20` |
| 1 | 00:10–00:28 | Why split a product | 5×4 grid, dashed divider, rows move apart | Can two smaller groups give the same total? | `5×4=20` |
| 2 | 00:28–00:52 | The total does not change | 2×4 and 3×4 rectangles | Split the Group. Keep the Total. | `8+12=20`, `(2+3)×4=2×4+3×4` |
| 3 | 00:52–01:11 | How distribution works | Bracket highlighted + two arrows | Multiply Both Terms | `(2+3)×4=2×4+3×4` |
| 4 | 01:11–01:32 | The general rule | `a(b+c)` with two arrows | DISTRIBUTIVE PROPERTY | `a(b+c)=ab+ac` |
| 5 | 01:32–01:58 | Simplify a product | `12×75 → 12(70+5) → 840+60` | Break Big Numbers into Easy Parts | `12×75=900` |
| 6 | 01:58–02:19 | Additive identity | Seven counters + empty container | Adding Zero Changes Nothing | `7+0=7`, `a+0=a` |
| 7 | 02:19–02:42 | Multiplicative identity | Same seven counters regrouped | Multiplying by One Changes Nothing | `1×7=7×1=7`, `a×1=a` |
| 8 | 02:42–03:03 | Real-world application | Two milk cans + price tag | Distributivity in Daily Life | `(56+44)×30=3000` |
| 9 | 03:03–03:39 | Student challenge | `5(7+8)` + THINK clock + identity check | YOUR TURN | `5(7+8)=75`; `9+0=9`; `9×1=9` |
| 10 | 03:39–04:03 | Recap | Concept cards + summary rows | Distribute to simplify | three rules |

## Scene Notes (Manim implementation)

- **Scene 1:** one `dot_grid(5, 4)` of twenty `Dot`s; a dashed `Line` is drawn
  after the second row and the bottom three rows **shift down** — the dots
  themselves never change, which is the pedagogical point.
- **Scene 2:** two grids (2×4 and 3×4) with their products, `8 + 12 = 20`, then
  the relation `5×4 = (2×4) + (3×4)` and the boxed
  `(2+3)×4 = 2×4 + 3×4`.
- **Scene 3:** the expression is built from separate `MathTex` parts
  (`("(", "2", "+", "3", ")", r"\times", "4")`) so the bracket can be
  highlighted, and **two** `dist_arrow`s run from the multiplier to `2` and to
  `3` (never one arrow), with the products appearing under each arrow.
- **Scene 4:** the same two-arrow treatment on `a(b+c)`, then
  `a(b+c)=ab+ac` boxed and the equivalent orientation `(b+c)a = ba+ca`.
- **Scene 5:** `12 × 75` transforms into `12(70+5)`, then
  `(12×70) + (12×5)`, then `840 + 60`, and `900` is boxed — with the small
  hint `75 = 80 − 5`.
- **Scene 6:** seven counters (`counter_group(7)`) with an empty container
  (`counter_group(0)`) holding `0`; the container slides next to the counters
  while the counter group is untouched, then `7 + 0 = 7` and the boxed
  `a+0=0+a=a` with the ADDITIVE IDENTITY = 0 label.
- **Scene 7:** the *same* seven counters regroup into seven single-counter
  outlines (`1×7=7` → `7×1=7`), the boxed `a×1=1×a=a`, the
  MULTIPLICATIVE IDENTITY = 1 label, and a red note `7 × 0 = 0 — multiplying by
  zero is different!` so the two identities are never confused.
- **Scene 8:** two `milk_can` graphics (56 L, 44 L) with the `Rs 30 per litre`
  tag; `(56×30)+(44×30)` transforms into `(56+44)×30` (the common multiplier is
  labelled), then `100×30` and the boxed **Rs 3000**.
- **Scene 9:** the challenge `5(7+8)` with the two distribution arrows after the
  4-second THINK clock, the boxed `75`, and then the quick identity check
  `9+0=9` / `9×1=9`.
- **Scene 10:** the dot grids and the three concept cards, then the three
  summary rows, the takeaway and finally the **Thank-You template only**.

## Key Pedagogical Safeguards

1. **The rectangle splits BEFORE the formula appears.** Students see
   `5×4 = (2×4)+(3×4)` first; only then is `a(b+c)=ab+ac` written.
2. **Two arrows, always.** The common mistake `a(b+c) = ab + c` is prevented by
   showing a separate arrow (and a separate product) for each term.
3. **The two identities stay distinct:** zero is the additive identity,
   one is the multiplicative identity, and the video explicitly warns that
   `7 × 0 = 0`, not `7`.
4. **Object continuity:** when the 5×4 grid separates, all twenty dots remain;
   the identity animations use the same seven counters before and after.
5. **The real-world example never loses the common multiplier:** the video shows
   `56×30 + 44×30` becoming `(56+44)×30`, naming the shared `30`.

## Final Production Check

Delivered as `distributive_property_story.py` (`DistributivePropertyStory`):

- **Masters:** `media/videos/distributive_property_story/1080p60/DistributivePropertyStory_captioned.mp4`
  (1920×1080, 60 fps, 243.2 s) — the delivered master — and the 360p30 review
  copy, both with the series caption style burned in.
- **Phrase-level sync pass:** every beat's windows were checked against the real
  (WAV-retimed) TTS word boundaries with `bookmark_times.py`. Fifteen placements
  were corrected. Scene 8 ran a whole narration window early in four places (the
  earnings equation, the "common multiplier 30" tag, `100×30` and the `Rs 3000`
  answer), the scene-9 reveal chain was one window early (the `(5×7)+(5×8)` step
  and the `35+40=75` result), and the scene-3 highlight box marked the bracket
  instead of the multiplier `4` it was describing. The rest were windows whose
  trailing fraction left a quarter to a third of themselves unconsumed.
- **Sync audit** (`audit_sync_overlap.py`) against the real SRT: **every beat
  matches its narration exactly (0.00 s)**; only the summary's closing flourish
  runs 0.30 s long. (Four beats originally finished up to 1.7 s early because
  their last bookmark was not the end of the spoken line — fixed by letting the
  closing play of those beats consume `get_remaining_duration()`.)
- **Layout audit:** no text/text, text/arrow, out-of-board, out-of-board-low,
  badge, LaTeX-as-text or empty-TeX flags. The three `TEXT-OUTSIDE-BOX` reports
  in Scene 3 are the intended highlight: a yellow box marks the `(2+3)` group
  *inside* the longer expression, so the expression naturally extends beyond the
  box. The `OFF-CENTRE` reports are the dot grids and counter groups that must
  sit where they are being demonstrated.
- **Content verification on the delivered file:** 74 captions,
  **0 captions in silence**, **0 speech blocks uncaptioned**, caption text
  618 words = narration 618 words, and every step checked against the textbook
  (`5×4=(2×4)+(3×4)=20`, `(2+3)×4=2×4+3×4`, `a(b+c)=ab+ac`,
  `(b+c)a=ba+ca`, `12×75=12(70+5)=840+60=900`, `7+0=7`, `a+0=0+a=a`,
  `1×7=7×1=7`, `a×1=1×a=a`, `(56+44)×30=3000`, `5(7+8)=35+40=75`,
  `9+0=9`, `9×1=9`).
- **Narration note:** every line was pre-checked against the TTS before
  rendering (the service occasionally returns an empty response for certain
  phrasings); all twelve passed. The rupee sign is rendered as `Rs`, matching
  the rest of the series, because `₹` is not available inside LaTeX maths.

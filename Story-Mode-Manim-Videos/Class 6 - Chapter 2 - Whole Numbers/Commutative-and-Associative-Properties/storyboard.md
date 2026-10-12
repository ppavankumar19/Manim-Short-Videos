# Production-Ready Storyboard

**VIDEO TITLE:** Commutative & Associative Properties of Whole Numbers
**TOPIC:** Order and Grouping — properties of whole numbers
**CLASS / CHAPTER:** Class 6 Mathematics — Chapter 2 — Whole Numbers
**STORYMODE:** 03 (third video of the Class 6 Chapter 2 set)
**DURATION (measured):** 3 min 57 s (237.0 s), 360p30 master (1080p60 to follow)
**TEXTBOOK REFERENCE:** Telangana SCERT, Class VI Mathematics (English Medium),
2025–26 edition, Chapter 2, Section 2.4 — Properties of Whole Numbers
(printed pages 21–23)

---

## Learning Objective

By the end of this video, students should be able to:

- Understand the meaning of the commutative property.
- Recognise that changing the order of numbers does not change the result of
  addition or multiplication.
- Understand the meaning of the associative property.
- Recognise that changing the grouping of numbers does not change the result of
  addition or multiplication.
- Visually distinguish rearranging numbers from regrouping them.
- Apply both properties to simplify calculations.

**Primary takeaway:** Commutative means changing the **order**. Associative
means changing the **grouping**. Both work for addition and multiplication of
whole numbers.

## Historical / Why-Needed Hook

A mental-maths challenge instead of history:

```
196 + 57 + 4 = ?          ->  196 + 4 = 200   ->   200 + 57
```

Students usually work left to right; the video shows that *rearranging* and
*regrouping* makes the sum easy — then asks: **"Can changing the order or
grouping make mathematics easier without changing the answer?"**

## Core Visual Metaphor

Number tiles, counting dots and movable grouping brackets, with **two visibly
different animations**:

- **Commutative → the tiles physically swap places** (`3 + 4 → 4 + 3`).
- **Associative → the tiles keep their order and only the grouping bracket
  moves** (`(3+4)+5 → 3+(4+5)`).

That contrast — swap versus bracket — is the central teaching device, and it is
repeated in the summary cards at the end.

## Mathematical Content

| Property | Addition | Multiplication |
|---|---|---|
| Commutative (order) | `a + b = b + a` | `a × b = b × a` |
| Associative (grouping) | `(a + b) + c = a + (b + c)` | `(a × b) × c = a × (b × c)` |

Worked examples: `3 + 4 = 4 + 3 = 7` · `4 × 3 = 3 × 4 = 12` ·
`(3+4)+5 = 3+(4+5) = 12` · `(5×6)×2 = 5×(6×2) = 60` ·
`196 + 57 + 4 = (196+4) + 57 = 200 + 57 = 257` ·
`238 + 695 + 162 = (238+162) + 695 = 400 + 695 = 1095`.

## Scene Overview

| Scene | Learning goal | Visual | Key on-screen text | Math |
|---|---|---|---|---|
| Title | Frame the topic | Title + two tiles and a rule | Commutative & Associative Properties | `3+4=4+3` |
| 1 | Why properties help | Tiles 196, 57, 4 — the 4 moves next to 196 | Can we change the order and grouping? | `196+4+57`, `(196+4)+57` |
| 2 | Commutative in addition | 3-counter and 4-counter groups swap | COMMUTATIVE PROPERTY | `3+4=4+3=7` |
| 3 | Commutative in multiplication | 4×3 dot grid becomes 3×4 | The order changed. The product stayed the same. | `4×3=3×4=12` |
| 4 | The general rule | Tiles `a` and `b` swap | COMMUTATIVE — Change the Order | `a+b=b+a`, `a×b=b×a` |
| 5 | Associative in addition | Three counter groups, bracket moves | ASSOCIATIVE PROPERTY | `(3+4)+5=3+(4+5)=12` |
| 6 | Associative in multiplication | 5 rows × 6 capsules, then one row bracketed | ASSOCIATIVE — Multiplication | `(5×6)×2=5×(6×2)=60` |
| 7 | Distinguish the two | Split screen: swap vs bracket | Order vs Grouping | Commutative / Associative |
| 8 | Apply both | Notebook stacks 196, 57, 4 and the chain | Rearrange. Regroup. Simplify. | `196+57+4 → 257` |
| 9 | Student challenge | Tiles 238, 695, 162 + THINK clock | YOUR TURN | `238+695+162=1095` |
| 10 | Recap | Two property cards + four formulae | Both work for addition and multiplication | four rules |

## Scene Notes (Manim implementation)

- **Scene 1:** three independent `num_tile` objects; the `4` tile animates next
  to the `196` tile (a real movement, no re-creation), a `bracket_around` the
  pair appears and `196+4=200` flashes. The calculation is deliberately *not*
  finished here.
- **Scene 2:** two `counter_group`s with their own number labels; the groups and
  their labels swap positions while the counters themselves stay visible, then
  `3+4=7` transforms into `4+3=7` and the boxed `3+4=4+3` plus the
  COMMUTATIVE PROPERTY label appear.
- **Scene 3:** twelve `Dot`s in a 4×3 grid; the *same* dots animate to the
  transposed 3×4 arrangement (`grid_targets`), so the identity of the twelve
  counters is never lost.
- **Scene 4:** tiles `a` and `b`, then the addition rule; at the multiplication
  step **both rules stay on the board** — the earlier version transformed one
  into the other, which left the first rule's box around an empty space.
- **Scene 5:** three counter groups in a fixed left-to-right order; the bracket
  `Transform`s from the first pair to the second pair. The numbers never move —
  only the outline — and each grouping is evaluated step by step
  (`7+5=12`, `3+9=12`).
- **Scene 6:** 30 capsules (each holding two dots) in 5 rows of 6; the dots are
  revealed inside the capsules, one row is bracketed, and a **single** running
  equation is shown at a time (`5×6=30` → `30×2=60` → `5×12=60`) so the bottom
  of the board never crowds.
- **Scene 7:** a dashed vertical divider splits the board; the left column swaps
  two tiles, the right column keeps three tiles fixed and moves only the
  bracket; the closing line is `Order is not grouping.`
- **Scene 8:** three `notebook_stack` icons labelled 196, 57 and 4; the main
  equation transforms through `196+57+4 → 196+(57+4) → 196+(4+57) →
  (196+4)+57 → 200+57`, with small labels naming the property used at each
  step, then the boxed answer `257`.
- **Scene 9:** three tiles `238`, `695`, `162`; the question, the prompt "Which
  two numbers can make a round hundred?", the series THINK clock (4 s), then the
  swap of 162 next to 238, the bracket, `400+695` and the boxed `1095`.
- **Scene 10:** two property cards (order / grouping) with the four general
  formulae, the takeaway lines, and then the **Thank-You template only**.

## Key Pedagogical Safeguards

1. **The two properties never look alike.** Commutativity visibly swaps numbers;
   associativity keeps the order and moves only the grouping bracket.
2. **Grouping is shown before evaluating.** `(3+4)+5` first combines 3 and 4
   visibly, then adds 5; the same for `3+(4+5)`, so 12 = 12 is demonstrated, not
   asserted.
3. **The properties are only claimed for addition and multiplication.** Nothing
   in the video suggests they hold for subtraction or division, and the number
   line is never extended into negatives.
4. **Object continuity is preserved:** the same twelve dots are rearranged, the
   same three counter groups stay in order, and 196, 57 and 4 keep their
   identities while they move and regroup.

## Final Production Check

Delivered as `commutative_associative_story.py`
(`CommutativeAssociativeStory`):

- **Masters:** `media/videos/commutative_associative_story/1080p60/CommutativeAssociativeStory_captioned.mp4`
  (1920×1080, 60 fps, 236.7 s) — the delivered master — and the 360p30 review
  copy, both with the series caption style burned in.
- **Phrase-level sync pass:** every beat's windows were checked against the real
  (WAV-retimed) TTS word boundaries with `bookmark_times.py`. Nine placements
  were corrected: the ASSOCIATIVE card and the closing "Both work for addition
  and multiplication…" banner each appeared a whole sentence early, and seven
  windows left 24–30 % of themselves unconsumed because their last play
  multiplied the mark by a fraction — which dragged the following window's
  visual into the previous sentence (the title's equation pulse, scene 1's
  "196+4=200" pair, scene 3's grid, scene 6's capsules, the scene-9 reveal
  bracket, and the scene-10 cards and board clear). All nine now end exactly on
  their own mark.
- **Sync audit** (`audit_sync_overlap.py`) against the real SRT: **0.00 s**
  animation-vs-audio stretch on every beat (only the closing flourish of the
  summary runs 0.30 s).
- **Layout audit:** no text/text, text/arrow, out-of-board, out-of-board-low,
  badge, LaTeX-as-text, empty-TeX or text-outside-box flags. The remaining
  `OFF-CENTRE` reports are the intended layouts (the tiles, the counter groups
  and the brackets that must sit where they are being demonstrated).
- **Content verification on the delivered file:** 70 captions,
  **0 captions in silence**, **0 speech blocks uncaptioned**, caption text
  586 words = narration 586 words, and every step checked against the textbook
  (`3+4=4+3=7`, `4×3=3×4=12`, `a+b=b+a`, `a×b=b×a`, `(3+4)+5=3+(4+5)=12`,
  `(5×6)×2=5×(6×2)=60`, `196+57+4 → (196+4)+57 → 257`, `238+695+162=1095`).
- **Two defects found by the frame sweep and fixed before delivery:** the
  multiplication rule in Scene 4 used to consume the addition rule (leaving an
  empty box), and Scene 6 stacked three equations at the bottom (now one line at
  a time).
- **Note on narration:** one line of Scene 9 was reworded after the TTS service
  rejected the original phrasing (a long numeric clause); the meaning and all
  four bookmarks are unchanged.

# Production-Ready Storyboard

**VIDEO TITLE:** Two-Digit Number Riddles
**TOPIC:** Two-Digit Number & Digit Reversal Puzzles
**CHAPTER:** Chapter 2 — Linear Equations in One Variable
**TARGET CLASS LEVEL:** Class 8 primary; understandable for Classes 6–12
**ESTIMATED DURATION:** 4 minutes 27 seconds (10 teaching scenes + 6 s thinking clock)

**LEARNING OBJECTIVE:** Students should be able to convert a two-digit number
puzzle into algebra using **place value** — represent the number from its tens
and ones digits, form the reversed number, build a linear equation from the
given condition, solve it and verify the answer.

---

## HISTORICAL / WHY-NEEDED HOOK

The textbook gives no historical origin here, so the video invents none. It
opens on the practical surprise that motivates the whole topic:

> **When the digits swap places, the number changes — because place value
> changes.**

## CORE VISUAL METAPHOR — the two place-value boxes

```
[Tens] [Ones]
```

`35 = 3 tens + 5 ones = 30 + 5`

If the digits are reversed: `53 = 5 tens + 3 ones = 50 + 3`

> A reversed number is not the same digits doing nothing — it is the digits
> **changing place value**.

---

## FORMULAS

With tens digit `t` and ones digit `u`:

```
Original  = 10t + u          Reversed = 10u + t
t + u = S   (the given digit sum)
```

These are introduced **visually through the place-value boxes**, never as
rules to memorise first.

## WORKED EXAMPLE (chapter's two-digit reversal puzzle)

> A two-digit number has digits whose sum is 8. If 18 is added to the number,
> its digits are reversed. Find the number.

ones `= x`, tens `= 8 - x`
original `= 10(8-x) + x = 80 - 9x`, reversed `= 10x + (8-x) = 9x + 8`
`(80-9x) + 18 = 9x + 8 → 98 - 9x = 9x + 8 → 90 = 18x → x = 5`
so the number is `10(8-5) + 5 = 35`, checked by `35 + 18 = 53` and `3 + 5 = 8`.

## REAL-WORLD APPLICATION

A flip-style display / price tag / route board: `35` becomes `53` when the
digit cards are reversed. The same two digits are worth `30 + 5` in one place
and `50 + 3` in the other — reversal puzzles are **place-value puzzles** turned
into equations.

## STUDENT CHALLENGE

> A two-digit number has digits whose sum is 9. If 27 is subtracted from the
> number, its digits are reversed. Find the number.

ones `= x`, tens `= 9 - x`, original `= 90 - 9x`, reversed `= 9x + 9`
`(90-9x) - 27 = 9x + 9 → 63 - 9x = 9x + 9 → 54 = 18x → x = 3` → **63**.

---

# Visual Identity

- **Tens digit** and **ones digit** each keep one colour throughout.
- The **place-value boxes** never change shape or position, so the swap reads.
- When digits reverse, the **same digit objects** physically cross boxes
  (`MoveAlongPath` on crossing arcs).
- `×10` is shown as “moving into the tens box”.
- Original and reversed numbers are always visually distinguishable.
- Large `MathTex`, one equation at a time, bottom 15–20 % clear for captions.

```text
Original:   [8 - x] [x]
Reversed:   [x] [8 - x]
```

---

# Storyboard Overview

| Scene | Time | Learning Goal | Visual | Key On-Screen Text | Math |
|---|---|---|---|---|---|
| 1 | 00:12–00:30 | Introduce the puzzle | Flip display 35 → 53 | Same digits, new number! | `35 → 53` |
| 2 | 00:30–00:53 | Build place-value intuition | Tens/ones boxes, expanding | Place value matters | `35 = 30+5 = 10·3+5` |
| 3 | 00:53–01:12 | Understand reversal | Digits lift and swap boxes | Reversing means swapping place values | `53 = 10·5+3` |
| 4 | 01:12–01:35 | Generalise the rule | Boxes labelled `t`, `u`, mirrored | Build the number algebraically | `10t+u`, `10u+t` |
| 5 | 01:35–02:04 | Set up the worked example | Puzzle text + boxes with `x`, `8-x` | Choose the unknown | `80-9x`, `9x+8` |
| 6 | 02:04–02:32 | Form and solve the equation | Centred equation chain | Form the equation | `(80-9x)+18=9x+8 → x=5` |
| 7 | 02:32–02:48 | Verify and interpret | 35 and 53 displays | Check the solution | `35+18=53`, `3+5=8` |
| 8 | 02:48–03:05 | Real-world place value | Two displays + expansions | Digits changing place changes value | `35 ≠ 53` |
| 9 | 03:05–03:56 | Student challenge | New puzzle + boxes, clock | Your Turn | `(90-9x)-27=9x+9` |
| 10 | 03:56–04:27 | Final recap | Boxes + formulas + takeaway, then Thanks | Place value → Equation → Answer | `10t+u`, `10u+t` |

---

# Scene Notes (Manim Implementation)

- **Scene 1:** a chalk flip display (frame + two hinged digit cards) shows `35`;
  the two digit cards physically swap along crossing arcs, giving `53`; a second
  display holding `35` slides in so both numbers sit side by side, and the
  question *"How did the same digits make a new number?"* appears.
- **Scene 2:** labelled `Tens` / `Ones` boxes hold `3` and `5`; each box is
  highlighted in turn with `3 tens = 30` and `5 ones = 5`, then the two collapse
  into `35 = 30 + 5` and finally `35 = 10·3 + 5`.
- **Scene 3:** the same boxes, the digits lift and cross into each other's box,
  and the reversed number is expanded: `53 = 50 + 3 = 10·5 + 3`.
- **Scene 4:** the boxes are relabelled with `t` and `u`; the original
  `10t + u` and the mirrored reversed `10u + t` are built side by side and stay
  visible together.
- **Scene 5:** the puzzle arrives as two short lines; the ones digit is chosen
  as `x` and dropped into the boxes, the tens digit becomes `8 - x` from the
  digit sum, then the original simplifies to `80 - 9x` and the reversed to
  `9x + 8`.
- **Scene 6:** the condition becomes one equation, transformed step by step
  (`(80-9x)+18=9x+8 → 98-9x=9x+8 → 90=18x → x=5`), the digits are read back
  (`5` and `3`), and `10(8-5)+5 = 35` is boxed.
- **Scene 7:** two displays `35` and `53` with `35 + 18 = 53` ticked, plus the
  digit-sum check `3 + 5 = 8` ticked.
- **Scene 8:** the same two displays sit under their place-value expansions
  `30 + 5` and `50 + 3` with `Same digits. Different value.`
- **Scene 9:** the challenge uses the series thinking clock
  (`story_common.play_challenge_countdown`); before the pause only the modelling
  prompt appears, after it the whole chain
  `(90-9x)-27=9x+9 → 63-9x=9x+9 → 54=18x → x=3` and the boxed **63**.
- **Scene 10:** the recap chain, four numbered rows and the closing line
  `Use place value to build the equation.` make up the **Summary**. After the
  summary the board is cleared and **only the Thank-You template** remains.

## Key Pedagogical Safeguard

The classic mistake is treating a two-digit number as two loose digits:
`35 → 3 + 5`. Every scene shows `35 = 30 + 5 = 10·3 + 5` instead. The second
mistake is writing the reversed number as `u + t`; the boxes make it visible
that reversing means `10u + t` — the digit that moves into the tens box is
multiplied by ten.

## Final Production Check

Delivered as `two_digit_puzzles_story.py` (`TwoDigitPuzzlesStory`):

- **Masters:** `media/videos/two_digit_puzzles_story/1080p60/TwoDigitPuzzlesStory_captioned.mp4`
  (1920×1080, 60 fps, 4:27) and `.../360p30/…_captioned.mp4` (640×360, 30 fps),
  both with the series caption style (`BorderStyle=3` white-on-dark box) burned in.
- **Sync audit** (`audit_sync_overlap.py`) against the real SRT: **0.00 s**
  animation-vs-audio stretch on every beat (only the closing flourish runs
  0.30 s long) — every beat's visuals consume its narration exactly.
- **Layout audit:** no text/text, text/arrow, out-of-board or badge collisions;
  every equation line centred on the board, the two displays and the box pairs
  centred as blocks.
- **Content verification on the delivered files:** 87 captions, **0 captions in
  silence**, **0 speech blocks uncaptioned**, caption text 723 words = narration
  723 words (word for word).

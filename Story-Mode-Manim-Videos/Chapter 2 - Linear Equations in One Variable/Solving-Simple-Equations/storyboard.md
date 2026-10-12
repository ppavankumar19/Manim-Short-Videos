# Production-Ready Storyboard

**VIDEO TITLE:** Solving Simple Equations
**TOPIC:** Solving Simple Linear Equations (Variable on One Side)
**CHAPTER:** Chapter 2 — Linear Equations in One Variable
**TARGET CLASS LEVEL:** Class 8
**ESTIMATED DURATION:** ~4 minutes 10 seconds (10 teaching scenes + 10 s challenge clock)

**LEARNING OBJECTIVE:** Students should understand how to solve a simple linear
equation with the variable on one side by **isolating the unknown
step-by-step**, using inverse operations/transposition, and finally checking
the answer.

The textbook defines a simple linear equation in one variable in forms such as
`ax + b = 0` or `ax = b`, with `a ≠ 0`, and then specifically introduces solving
equations where the variable is on one side.

**HISTORICAL / WHY-NEEDED HOOK:** No specific historical development is given
in this section, so instead of inventing history, the video opens with the
chapter's practical idea: **we know the result, but not the number that
produced it.** Equations give us a systematic way to work backward and recover
that unknown.

**CORE VISUAL METAPHOR / IDEA — The Operation Machine → Undo Machine**

Forward:  `x --×3--> 3x --+1--> 3x + 1 = 16`

To solve, move backward using opposite operations:
`16 --−1--> 15 --÷3--> 5`, therefore `x = 5`.

> **Solve an equation by undoing what was done to the variable — in reverse
> order.**

---

## FORMULA / RULE

For a simple equation `ax + b = c`, isolate x by undoing the constant first:
`ax = c − b`, then undo the multiplication: `x = (c − b) / a`.

The video does **not** introduce this as a formula to memorise. Students first
see the operation machine and understand the reversal visually.

**Transposition connection:** `+ ↔ −` and `× ↔ ÷`. The textbook solves its first
Section 2.3 example by transposing 39 and then 3, and verifies the answer by
substituting it into the LHS.

---

## WORKED EXAMPLE (appears in Exercise 2.1)

`3x + 1 = 16` → `3x = 16 − 1` → `3x = 15` → `x = 15/3` → **x = 5**

## REAL-WORLD APPLICATION

"Four times a number reduced by 5 equals 19. Find the number."
`4x − 5 = 19` → `4x = 24` → **x = 6** (checked: 4(6) − 5 = 19).

## STUDENT CHALLENGE

`7x − 9 = 26` → `7x = 35` → **x = 5** (same two-step idea: undo subtraction,
then undo multiplication — no new concept).

---

# Visual Identity

- **x** → same highlight throughout.
- **Operations acting on x** → shown as operation blocks/cards.
- **Forward operations** → arrows moving right.
- **Undo operations** → arrows moving left.
- **Equality sign** → always visually stable.
- **Current operation being undone** → highlighted.
- Final isolated x → boxed.
- Bottom 15–20% remains clear for subtitles.

The main animation principle:

```
[x] -> [×3] -> [+1] -> [16]        then reverse:
[16] -> [−1] -> [÷3] -> [x = 5]
```

---

# Storyboard Overview

| Scene | Time | Learning Goal | Visual Composition | Animation / Movement | Key On-Screen Text | Math / Formula |
|---|---|---|---|---|---|---|
| 1 | 00:10–00:32 | Establish the mystery-number problem | Hidden x enters operation machine | x → ×3 → +1 → 16 | What number went in? | `3x+1=16` |
| 2 | 00:32–00:51 | Build intuition for solving | Forward machine above, reverse path below | Arrows reverse; +1 becomes −1, ×3 becomes ÷3 | Undo in reverse order | `16→15→5` |
| 3 | 00:51–01:11 | Identify what solving means | Equation centered; x trapped by ×3 and +1 | Operation layers appear around x | Goal: Isolate x | `3x+1=16` |
| 4 | 01:11–01:32 | Undo addition/subtraction | +1 crosses equality | +1 → −1 | Undo +1 first | `3x=16−1=15` |
| 5 | 01:32–01:53 | Undo multiplication/division | 3 becomes denominator | 3×x → x = 15/3 | Undo ×3 with ÷3 | `x=5` |
| 6 | 01:53–02:09 | Verify the solution | Substitute 5 into original equation | 3(5)+1 → 16 | Check your answer | `16=16` |
| 7 | 02:09–02:37 | Generalize the process | Generic operation ladder / routine | Steps appear sequentially | Identify → Undo → Isolate → Check | `ax+b=c` |
| 8 | 02:37–02:58 | Apply to a simple real situation | Mystery-number statement + equation | Words transform into 4x−5=19, then solution | Turn words into an equation | `x=6` |
| 9 | 02:58–03:36 | Student challenge | 7x−9=26 large centre | 10-s countdown, then animated solution | Your Turn | `x=5` |
| 10 | 03:36–04:12 | Final recap | Summary rows + takeaway, then Thanks | Summary shown once, then the Thank-You template | Undo in reverse. Isolate x. | `3x+1=16 → x=5` |

---

# Scene Notes (Manim Implementation)

- **Scene 1:** mystery box → `×3` card → `+1` card → `16`, connected by arrows;
  `?` becomes `x`; the machine compresses into `3x+1=16`.
- **Scene 2:** forward row stays at the top; the reverse row is built
  underneath with left-pointing arrows and inverse-operation cards; `16−1=15`
  and `15÷3=5` appear as working lines; `x=5` is revealed.
- **Scene 3:** equation centred; a cyan shell around `3x` (the ×3 operation) and
  a pink shell around `+1` (the outer operation); the outer `+1` pulses at the
  end to set up scene 4.
- **Scene 4:** the `1` travels an arch over the `=` and flips to `−1` at the
  crossing point (never before), `3x = 16 − 1` → `3x = 15`.
- **Scene 5:** `3x` is exposed as `3 × x`; the `3` crosses the `=` and lands
  below the fraction bar → `x = 15/3` → boxed `x = 5`.
- **Scene 6:** substitution chain `3(5)+1 → 15+1 → 16 → 16 = 16` with a drawn
  checkmark and the label `LHS = RHS`.
- **Scene 7:** four numbered routine rows (identify, undo, isolate, check) plus
  the strategy strip `Identify → Undo → Isolate → Check`.
- **Scene 8:** word chunks on the left turn into the equation column on the
  right; `4x − 5 = 19 → 4x = 19 + 5 → 4x = 24 → x = 24/4 → x = 6`.
- **Scene 8 → 9:** the challenge uses the series-standard 10-second THINK
  countdown (`story_common.play_challenge_countdown`).
- **Scene 10:** forward and reverse machine rows, the three routine rows and the
  closing line `Undo in reverse. Isolate the unknown.` make up the **Summary**.
  After the summary has been shown, the board is cleared and **only the
  Thank-You template** (`Thank You for Watching!` / `See you in the next
  lesson :)`) remains — the video ends there.

## Key Pedagogical Safeguard

Avoid making transposition feel like "move a number across `=`, then magically
change its sign". The animation shows the **inverse-operation idea first**
(`+1` is undone by `−1`, `×3` is undone by `÷3`) and only then connects it to
the textbook word *transposition*, so students get both the school method and
the reason it works.

## Final Production Check

Delivered as `equation_solving_story.py` (`EquationSolvingStory`):

- **Masters:** `media/videos/equation_solving_story/1080p60/EquationSolvingStory_captioned.mp4`
  (1920×1080, 60 fps, 4:11) and `.../360p30/EquationSolvingStory_captioned.mp4`
  (640×360, 30 fps) — both with the real SRT captions burned in.
- **Concept cross-check:** every equation in the video is worked out correctly —
  `3x+1=16 → 3x=15 → x=5` (checked `3(5)+1=16`), `4x−5=19 → 4x=24 → x=6`,
  challenge `7x−9=26 → 7x=35 → x=5`, and the reverse machine
  `16−1=15, 15÷3=5` matches the forward machine `x→×3→+1→16`.
- **Sync audit** (`audit_sync_overlap.py` replays the scene against the real
  `EquationSolvingStory.real.srt`): **0.00 s** animation-vs-audio stretch on
  every beat (only the closing flourish runs 0.30 s long).
- **Layout audit:** no text/text, text/arrow, out-of-board or badge collisions;
  the board's centrepiece is centred on `BOARD_CX` (the mini machine on the
  title card, the two machine rows, every equation line), the routine and
  summary lists are centred as blocks, and scene 8's word/equation columns sit
  symmetrically at ±2.2 around the board centre.
- **Ending rule:** the Summary (journey rows + routine rows + the closing line
  `Undo in reverse. Isolate the unknown.`) is shown, then the board is cleared
  and **only the Thank-You template** remains — nothing else follows it.

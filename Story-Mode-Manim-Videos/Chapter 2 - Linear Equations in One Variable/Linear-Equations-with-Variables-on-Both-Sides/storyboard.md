# Production-Ready Storyboard

**VIDEO TITLE:** Linear Equations with Variables on Both Sides
**TOPIC:** Solving Linear Equations with Variables on Both Sides
**CHAPTER:** Chapter 2 — Linear Equations in One Variable
**TARGET CLASS LEVEL:** Class 8
**ESTIMATED DURATION:** ~2 minutes 50 seconds

**LEARNING OBJECTIVE:** Students should understand how to solve equations where
the variable appears on **both sides** by simplifying brackets when needed,
bringing variable terms to one side, bringing constants to the other side,
combining like terms, and isolating the variable.

The textbook introduces this section by pointing out that the RHS need not be
only a number; both sides of an equation may contain algebraic expressions.

**HISTORICAL / WHY-NEEDED HOOK:** The textbook gives no historical origin for
this technique, so the opening uses the practical mathematical need: earlier
equations kept the unknown mainly on one side, but real relationships can place
the **same unknown on both sides**. We therefore need a method for collecting
all instances of the unknown together.

**CORE VISUAL METAPHOR / IDEA:** the equation as a balanced two-sided
workspace. `5x − 12 = 2x − 6` — the left holds **five x-tiles**, the right holds
**two x-tiles**. Instead of solving two separate mysteries, move the x-terms
together: `5x − 2x = −6 + 12` → `3x = 6` → `x = 2`.

> **Variables together. Numbers together. Then isolate the variable.**

Brackets are shown as a **closed package** that must be opened using
multiplication: `3(x − 3) → 3x − 9`. Only after brackets are opened should like
terms be collected.

---

## SOLVING ROUTINE

For `ax + b = cx + d`: `ax − cx = d − b` → `(a−c)x = d − b` → `x = (d−b)/(a−c)`.
The video does **not** present this as a formula to memorise — it builds:

```
Simplify → Variables together → Constants together → Solve → Check
```

The textbook demonstrates this structure with `49x + 70 = 45x + 90` becoming
`49x − 45x = 90 − 70`, then `4x = 20`, `x = 5`.

---

## WORKED EXAMPLE (Exercise 2.3)

`5x − 12 = 2x − 6` → `5x − 2x = −6 + 12` → `3x = 6` → **x = 2**

## BRACKET EXTENSION (Exercise 2.3)

`3(x − 3) = 5(2x − 1)` → `3x − 9 = 10x − 5` → `3x − 10x = −5 + 9` →
`−7x = 4` → **x = −4/7**

## REAL-WORLD APPLICATION (chapter's age problem)

Karthik : Ananya = 7 : 5 now, and 9 : 7 ten years later.
`Karthik = 7x`, `Ananya = 5x` → `(7x+10)/(5x+10) = 9/7` → `49x + 70 = 45x + 90`
→ `49x − 45x = 90 − 70` → `4x = 20` → `x = 5` → **Karthik 35, Ananya 25**.

## STUDENT CHALLENGE (Exercise 2.3, Q1)

`7x − 5 = 2x` → `7x − 2x = 5` → `5x = 5` → **x = 1**

---

# Visual Identity

- All **x-terms** → same visual treatment (cyan x-tiles).
- **Constants** → second treatment (number blocks / amber).
- `=` → fixed at screen centre, always visually stable.
- Terms moving across `=` → visibly transform operation/sign **during** the
  crossing.
- **Brackets** → drawn as literal containers (packages) around terms.
- **Distribution arrows** → from the outside coefficient into every term inside.
- **Like terms** → physically gather before any arithmetic happens.
- Final `x` → isolated at centre and boxed.
- Bottom 15–20 % stays clear for subtitles.

Recurring visual rule: `VARIABLES ← = → CONSTANTS` (a consistent strategy, not a
mathematical law).

---

# Storyboard Overview

| Scene | Time | Learning Goal | Visual Composition | Key Text | Math |
|---|---|---|---|---|---|
| 1 | 00:00–00:15 | Introduce the new problem | `5x−12=2x−6` with x-tiles on both sides | x is on BOTH sides! | `5x-12=2x-6` |
| 2 | 00:15–00:32 | Build grouping intuition | five x-tiles left, two move right→left | Bring variables together | `5x-2x=-6+12` |
| 3 | 00:32–00:48 | Group constants | `−12` crosses and becomes `+12` | Bring numbers together | `3x=6` |
| 4 | 00:48–01:04 | Isolate variable | `3x=6`, three tiles compress to one | Now isolate x | `x=2` |
| 5 | 01:04–01:20 | Verify solution | substitute on both sides | Check: LHS = RHS | `-2=-2` |
| 6 | 01:20–01:42 | What to do with brackets | bracket packages open by distribution | Open brackets first | `3x-9=10x-5` |
| 7 | 01:42–01:58 | Generalize the strategy | four-step flow | Simplify → Group → Solve → Check | `ax+b=cx+d` |
| 8 | 01:58–02:20 | Real-world application | Karthik/Ananya age bars | Same unknown on both sides | `49x+70=45x+90` |
| 9 | 02:20–02:39 | Student practice | `7x-5=2x` with a thinking pause | Your Turn | `x=1` |
| 10 | 02:39–02:52 | Summary / recap | variables and constants regroup | Variables together. Numbers together. | `5x-12=2x-6 → x=2` |

---

# Scene Notes (Manim Implementation)

- **Scene 1:** equation centred (`\;=\;` spacing); rows of **x-tiles** above the
  `5x` and `2x` groups; `5x` and `2x` highlighted in turn, then both pulse;
  `x is on BOTH sides!` and the question `How do we isolate x now?`.
- **Scene 2:** the two right-hand x-tiles travel an arch over the `=`, turning
  into `−2x`; two of the five left tiles then cancel, leaving three; equation
  goes `5x − 12 = 2x − 6 → 5x − 2x − 12 = −6 → 3x − 12 = −6`.
- **Scene 3:** `−12` crosses and becomes `+12` → `3x = −6 + 12 → 3x = 6`; brief
  labels `VARIABLE TERM` (left) and `CONSTANT` (right).
- **Scene 4:** `3x = 6 → 3 × x = 6 → x = 6/3 → x = 2` (boxed); the three x-tiles
  compress into a single green tile showing **2**.
- **Scene 5:** `x = 2` at the top; substitution on **both** sides
  `5(2) − 12 = 2(2) − 6 → 10 − 12 = 4 − 6 → −2 = −2`, then a tick and
  `LHS = RHS`.
- **Scene 6:** brackets drawn as packages; distribution arrows from `3` into
  `x` and `−3`, and from `5` into `2x` and `−1`; result `3x − 9 = 10x − 5`,
  then `3x − 10x = −5 + 9 → −7x = 4 → x = −4/7`.
- **Scene 7:** four strategy cards (`Simplify`, `Group variables`,
  `Group numbers`, `Solve`) plus a `Check` chip, each with a mini example.
- **Scene 8:** two age bars (`Karthik 7x`, `Ananya 5x`), a `+10 years` arrow, the
  ratio `9 : 7`, then the equation column `49x+70=45x+90 → 4x=20 → x=5` and the
  final ages `35` and `25`.
- **Scene 9:** challenge `7x − 5 = 2x` with the series-standard 10-second THINK
  countdown, then `7x − 2x = 5 → 5x = 5 → x = 1`.
- **Scene 10:** **Summary** — the forward story in one line, numbered bullets
  (variables together / numbers together / isolate / check), the takeaway
  `Variables together. Numbers together.` with `Brackets? Simplify them first.`
  as the summary's closing lines. After the summary has been shown, the board is
  cleared and **only the Thank-You template** remains — the video ends there.

## Key Pedagogical Safeguard

Do not teach the chant "move x left, numbers right". Make the reason visible:
the equation contains **like variable terms on opposite sides**, and we collect
them precisely so they can be combined (`5x − 2x`), just as the constants are
collected so they can be simplified (`−6 + 12`). For brackets, make the order
unmistakable: **open brackets first**, then combine like terms.

## Final Production Check

Rendered and verified as `variables_both_sides_story.py`
(`VariablesBothSidesStory`):

- **Master:** `media/videos/variables_both_sides_story/360p30/VariablesBothSidesStory_captioned.mp4`
  — 640×360, 30 fps, 3:57, real SRT captions burned in.
- **Sync audit** (`audit_sync_overlap.py`, replays the scene against the real
  `VariablesBothSidesStory.real.srt`): 0.00 s animation-vs-audio stretch on
  every beat (only the closing flourish runs 0.30 s long) — captions, voice and
  chalk marks change together.
- **Layout audit:** no text/text, text/arrow, out-of-board or badge collisions;
  every equation line is centred on the board (`BOARD_CX`) and nothing enters
  the caption band.
- **Realistic diagrams kept simple:** equal-sized x-tiles that visibly cross the
  equals sign and cancel, the `−12 → +12` chip that flies over, brackets drawn
  as packages with distribution arrows, the two-age bar comparison, and the
  complete-strategy cards (Simplify → Group → Solve → Check).

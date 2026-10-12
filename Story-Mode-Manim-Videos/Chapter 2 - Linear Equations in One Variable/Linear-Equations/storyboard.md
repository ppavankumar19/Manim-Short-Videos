# Production-Ready Visual Storyboard

**VIDEO TITLE:** Linear Equations
**TOPIC:** Anatomy of an Equation & The Transposition Rules
**CHAPTER:** Chapter 2 — Linear Equations in One Variable
**TARGET CLASS LEVEL:** Class 8 primary; understandable for Classes 6–12
**ESTIMATED DURATION:** ~2 minutes 45 seconds

**LEARNING OBJECTIVE:** By the end of the video, students should be able to
identify the **variable, constants, LHS, RHS, and equality sign** in a simple
equation, understand that an equation represents two equal expressions, and
solve a simple equation by transposing terms correctly.

**HISTORICAL / NEED HOOK:** The textbook opens with an unknown-number puzzle:
double a number, subtract 7, and the result is 35. This storyboard uses that
source-based puzzle to answer the more useful question: **Why do we need
equations? — to represent and uncover unknown quantities.**

**CORE VISUAL METAPHOR / IDEA:** An equation is shown as a **balanced
two-sided structure**:

```
\boxed{LHS} = \boxed{RHS}
```

The equality sign is the center divider. Transposition is visualized as
**undoing an operation while preserving equality**, rather than making a
symbol magically change sign.

**CORE ANATOMY:** `2x - 7 = 35`

- `x` → variable
- `2, -7, 35` → numerical quantities/constants
- `2x - 7` → LHS
- `35` → RHS
- `=` → equality sign

**TRANSPOSITION RULES FROM THE CHAPTER:**

```
+  <->  -
×  <->  ÷
```

**WORKED EXAMPLE:** `2x - 7 = 35` → `2x = 35 + 7` → `2x = 42` →
`x = 42/2` → **x = 21**

**REAL-WORLD APPLICATION:** A rectangular park has breadth `x`, length
`x + 17`, and perimeter `178` m. Build `2[(x+17)+x] = 178` and use
equation-solving/transposition to obtain `x = 36`, so the park is
`36 m × 53 m`.

**STUDENT CHALLENGE:** `3x + 1 = 16` → `3x = 16 - 1` → `3x = 15` →
`x = 15/3` → **x = 5**

---

# Visual Identity for the Entire Video

Maintain the same identity from beginning to end:

- **Variable x:** one consistent highlight (chalk cyan).
- **LHS:** subtle left-side container (chalk cyan).
- **RHS:** contrasting right-side container (chalk pink).
- **Equality sign:** always centered and visually stable (chalk yellow).
- **Term being transposed:** briefly highlighted before movement.
- **Operation change:** animate during the crossing, never before it.
- Keep the `=` fixed wherever possible so students feel that **equality must
  remain true**.
- Reserve the bottom 15–20% for subtitles.
- Use large `MathTex`.
- Never show more than one main equation transformation at once.

A useful persistent screen metaphor is:

```text
            EQUATION

      LHS       =       RHS
     2x - 7             35
```

---

# Storyboard Overview

| Scene | Time | Learning Goal | Visual Composition | Animation / Movement | Key On-Screen Text | Math / Formula |
|---|---|---|---|---|---|---|
| 1 | 00:00–00:15 | Understand why equations are needed | Mystery-number machine | Number hidden as `x`; ×2 then −7 gives 35 | What was the number? | `2x-7=35` |
| 2 | 00:15–00:34 | Learn equation anatomy | Equation split around fixed `=` | LHS/RHS regions appear; variable and constants highlight | Anatomy of an Equation | `2x-7=35` |
| 3 | 00:34–00:49 | Understand equality | LHS and RHS shown as equally valued sides | Both sides glow together | LHS = RHS | `2x-7=35` |
| 4 | 00:49–01:08 | Understand +/− transposition | `-7` moves across `=` | It becomes `+7` on RHS | − becomes + | `2x=35+7` → `2x=42` |
| 5 | 01:08–01:26 | Understand ×/÷ transposition | `2 × x` emphasized | 2 crosses and becomes division | × becomes ÷ | `x=42/2` → `x=21` |
| 6 | 01:26–01:43 | Verify the solution | `x=21` travels back into original equation | LHS calculates to 35 and matches RHS | Check: LHS = RHS | `2(21)-7=35` |
| 7 | 01:43–01:56 | Consolidate all four rules | Four operation cards around `=` | Each crosses and morphs to inverse operation | Transposition Rules | `+<->-`, `×<->÷` |
| 8 | 01:56–02:16 | Apply equations to a real situation | Rectangular park diagram | Measurements become equation; key transposition shown | Unknown → Equation → Solution | `4x+34=178` → `x=36` |
| 9 | 02:16–02:36 | Student independently applies rules | Large `3x+1=16` | 10-s countdown pause, then solution transforms | Your Turn | `x=5` |
| 10 | 02:36–02:48 | Final visual recap | LHS = RHS with rules beneath | Earlier equation rebuilds and simplifies | Keep the equality true | `2x-7=35` → `x=21` |

---

# Scene Notes (Manim Implementation)

- **Scene 1:** `Square()`/`RoundedRectangle()` mystery box, `MathTex()`,
  `Arrow()`, `TransformMatchingTex()`, `ReplacementTransform()`. Machine
  compresses into the boxed equation, which stays fixed for Scene 2.
- **Scene 2:** `MathTex()`, `SurroundingRectangle()`, `Indicate()`; labels
  anchored **above** to preserve subtitle space; one component at a time.
- **Scene 3:** two panels + synchronized glow + `Indicate()`; guess chips
  `x=10, x=15, x=21` with a checkmark only on 21; check/cross drawn with
  simple geometry (no font glyph dependency).
- **Scene 4:** `-7` travels a curved path across `=`; the sign flips to `+7`
  **at the crossing point** (`ReplacementTransform` + `Flash`), then
  `TransformMatchingTex` produces `2x = 35+7` and `2x = 42`.
- **Scene 5:** `2x` exposed as `2 × x`; the `2` crosses and lands below the
  fraction bar (`TransformMatchingTex` so the 2 visibly becomes the
  denominator); resolves to boxed `x = 21`.
- **Scene 6:** `TransformFromCopy`/`TransformMatchingTex` substitution chain
  `2(21)-7 → 42-7 → 35 → 35=35` with a drawn checkmark and `LHS = RHS`.
- **Scene 7:** four operation cards; one operation pair crosses the central
  `=` at a time and morphs to its inverse.
- **Scene 8:** `Rectangle()`, `DoubleArrow()` perimeter trace; equation
  column on the right runs `2[(x+17)+x]=178 → 4x+34=178 → 4x=178-34 →
  4x=144 → x=36`; labels update to `Breadth = 36 m`, `Length = 53 m`.
- **Scene 9:** series-standard 10-second THINK countdown
  (`story_common.play_challenge_countdown`), then reveal
  `3x=16-1 → 3x=15 → x=15/3 → x=5`.
- **Scene 10:** LHS/RHS panels + rules + solution chain
  `2x-7=35 → 2x=42 → x=21`; final takeaway: **Keep the equality true.
  Isolate the unknown.**

## Important Mathematical / Animation Safeguard

The phrase "when a term crosses the equals sign, its sign changes" must not
look like magic. The animation communicates `-7 is being undone` and then
shows `2x = 35 + 7`; likewise `2x = 42` visually exposes `2 × x = 42` before
becoming `x = 42/2`. This keeps the textbook's transposition rules while
showing that equality is preserved on both sides.

## Final Production Check

This storyboard uses the chapter's own opening mystery-number example,
preserves the terminology of **LHS, RHS, equality sign, solution, and
transposition**, and uses the `2x-7=35 → x=21` progression as the central
continuous visual story. Equality is established before the four
transposition rules are summarized, the worked example is verified by
substitution, a chapter-based park application demonstrates practical use,
and the final challenge requires only the operations already taught. All
proposed visuals are realistic with standard Manim objects and
`TransformMatchingTex()`.

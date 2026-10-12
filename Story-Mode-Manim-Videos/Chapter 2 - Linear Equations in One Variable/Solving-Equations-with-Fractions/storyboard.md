# Production-Ready Storyboard

**VIDEO TITLE:** Solving Equations with Fractions
**TOPIC:** Fractional Linear Equations and Cross-Multiplication
**CHAPTER:** Chapter 2 — Linear Equations in One Variable
**TARGET CLASS LEVEL:** Class 8
**DURATION (measured):** 4 min 48 s (288.0 s) — 10 teaching scenes + 6 s thinking
clock (both masters, 1080p60 and 360p30)

**LEARNING OBJECTIVE:** Students should learn to simplify linear equations
containing fractions by **removing the denominators**, and understand why the
**cross-multiplication method** works when one fraction equals another.

---

## HISTORICAL / WHY-NEEDED HOOK

No historical origin is given in the textbook, so the video invents none. It
opens on the practical problem

```
(5x+2)/(2x+3) = 12/7
```

Students already solve `5x+2 = 12`; the denominators are what make the equation
*look* harder. The guiding question:

> **Can we remove the denominators without changing the equality?**

## CORE VISUAL METAPHOR

The equation is two sides joined by a fixed `=`. The denominators are
**barriers**; instead of "sending them across", the video multiplies **both
sides** by them, and the cancellation is shown happening:

```
 A     C
─── = ───        ×B        ×D
 B     D    ───────────▶   A·D = B·C
```

> **Cross-multiplication is a shortcut for clearing denominators.**

## THE TWO METHODS

| Situation | Method | Example |
|---|---|---|
| Several fractional terms | multiply **every term** by the LCM | `x/3 - x/5 = 4` → ×15 |
| One fraction = one fraction | **cross-multiply** `AD = BC` | `(5x+2)/(2x+3) = 12/7` |

## EXAMPLES

**Example 19.** `(5x+2)/(2x+3) = 12/7` → `7(5x+2) = 12(2x+3)` →
`35x+14 = 24x+36` → `35x-24x = 36-14` → `11x = 22` → **x = 2**

**Example 20.** `7/(3x+16) = 4/(x+7)` → `7(x+7) = 4(3x+16)` →
`7x+49 = 12x+64` → `7x-12x = 64-49` → `-5x = 15` → **x = -3**
(check: `7/7 = 1` and `4/4 = 1`)

**Example 21.** 24 % discount, paid ₹380 → `(76/100)x = 380` →
`x = 380×100/76` → **₹500**

**Exercise 2.5.** `x/3 - x/5 = 4` → ×15 → `5x-3x = 60` → `2x = 60` → **x = 30**
(check: `10 - 6 = 4`)

---

# Visual Identity

- Fraction bars stay clearly visible until the denominators are removed.
- **Denominators** have one visual treatment, **numerators** another; the
  equality sign never moves.
- When multiplying both sides, the **same multiplier is written on both sides at
  once**, and the cancellation is **shown on screen** (the cancelled denominator
  fades out with a red flash), never implied.
- **Cross-multiplication arrows appear only after** the derivation has been
  shown.
- `x` keeps the same identity throughout; bottom 15–20 % stays clear for captions.

**The defining animation rule: never make a denominator jump across the equals
sign magically — show the equal operation first.**

---

# Storyboard Overview

| Scene | Time | Learning Goal | Visual | Key On-Screen Text | Math |
|---|---|---|---|---|---|
| 1 | 00:11–00:30 | Introduce denominator difficulty | Fraction equation, bars and denominators | Fractions make it look harder | `(5x+2)/(2x+3)=12/7` |
| 2 | 00:30–00:58 | Why clearing works | Generic fractions, ×B then ×D, cancellation | Do the same operation to both sides | `AD = BC` |
| 3 | 00:58–01:27 | Derive cross-multiplication | Example 19 with both multiplications | Cross multiplication | `7(5x+2)=12(2x+3)` |
| 4 | 01:27–01:44 | Solve Example 19 | Centred chain | Now solve normally | `x=2` |
| 5 | 01:44–02:11 | Apply the shortcut | Example 20, diagonals | One fraction = one fraction | `7(x+7)=4(3x+16)` |
| 6 | 02:11–02:37 | Finish Example 20 | Chain + check | Clear → Expand → Group → Solve | `x=-3` |
| 7 | 02:37–03:05 | Real-world discount | Price tag + 100-part bar | Percent means “out of 100” | `(76/100)x=380 → ₹500` |
| 8 | 03:05–03:24 | Choose the right tool | Two method cards | Same goal: remove the denominators | LCM / cross-multiply |
| 9 | 03:24–04:16 | Student challenge | `x/3 - x/5 = 4`, clock | Your Turn | `5x-3x=60 → x=30` |
| 10 | 04:16–04:45 | Final recap | Two branches → linear equation → solve | Clear first. Solve second. | `AD = BC` |

---

# Scene Notes (Manim Implementation)

- **Scene 1:** the fraction equation is **assembled part by part** —
  numerators first, then the fraction bars, then the denominators — and the two
  denominators pulse as the "barriers".
- **Scene 2:** `A/B = C/D` with the `×B` written on both sides at once, the
  left cancellation shown by the denominator fading out with a red flash; then
  the same with `×D`, leaving `A·D = B·C` boxed.
- **Scene 3:** the same two multiplications on Example 19, the denominator
  cancelling visibly each time; then the two **diagonal arrows** appear with the
  label `CROSS MULTIPLICATION` — after the reason, never before.
- **Scene 4:** `7(5x+2)=12(2x+3) → 35x+14=24x+36 → 35x-24x=36-14 → 11x=22 → x=2`.
- **Scene 5:** `7/(3x+16) = 4/(x+7)` with the diagonals producing
  `7(x+7) = 4(3x+16)`.
- **Scene 6:** the chain to `x = -3` plus the check that both sides become `1`.
- **Scene 7:** a price tag `₹x` and a 100-part bar; 24 parts are shaded as the
  discount, 76 remain → `(76/100)x = 380 → x = 500`.
- **Scene 8:** two cards — *several fractional terms → LCM* and
  *one fraction = one fraction → cross-multiply* — with the shared goal stated.
- **Scene 9:** the challenge uses the series thinking clock; the `15` visibly
  multiplies **every** term, then `5x-3x=60 → 2x=60 → x=30`.
- **Scene 10:** both branches merge into a linear equation and the takeaway
  `Clear first. Solve second.`; after the summary only the **Thank-You**
  template remains.

## Key Pedagogical Safeguards

1. Cross-multiplication is never magic: the derivation is shown first, the
   shortcut second.
2. When clearing denominators, multiply **every term** — including the constant
   on the right — not only the fractions.
3. Cross-multiplication is for *one fraction = one fraction*; several fractional
   terms call for the LCM.

## Final Production Check

Delivered as `fractions_clearing_story.py` (`FractionsClearingStory`):

- **Masters:** `media/videos/fractions_clearing_story/1080p60/FractionsClearingStory_captioned.mp4`
  (1920×1080, 60 fps, 287.8 s) and
  `.../360p30/FractionsClearingStory_captioned.mp4` (640×360, 30 fps, 288.0 s),
  both with the series caption style burned in.
- **Sync audit** against the real SRT: 0.00 s animation-vs-audio stretch in every
  beat (only the closing flourish of the summary runs 0.30 s long).
- **Layout audit:** no text/text, text/arrow, out-of-board or badge collisions.
  The remaining reported items are the intended layouts — the two method cards
  (±2.40 units, symmetric about the board centre), the left-aligned summary rows
  and the two halves of a centred equation.
- **Content verification on the delivered files:** 0 captions in silence,
  0 speech blocks uncaptioned, captions word for word (729 narration words =
  729 SRT words), and every step checked (`x=2`, `x=-3`, `₹500`, `x=30`).
  Frame spot-checks (contact sheets of every beat, plus full-res crops of the
  cancellation flashes and the two-card scene) show no overlaps and no
  clipped text.

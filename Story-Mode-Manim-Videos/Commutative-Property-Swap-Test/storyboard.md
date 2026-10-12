# Storyboard — Commutative Property: The "Swap Test"

**Topic:** Commutative Property (Chapter 1 — Rational Numbers)
**Core comparison:** a+b=b+a vs a−b≠b−a
**Target duration:** 1:45–2:00
**Core visual idea:** Swap the numbers. If the result stays the same → commutative. If it changes → not commutative.

The textbook defines the commutative property as changing the order of two numbers in a binary operation without changing the result. Addition is commutative; subtraction is not — established for rational numbers.

## Overall Story Flow

| Scene | Time | Learning Goal | Visual Focus | Key Takeaway |
| --- | ---: | --- | --- | --- |
| 1 | 0:00–0:12 | Introduce the swap idea | Two numbers swapping places | Does order matter? |
| 2 | 0:12–0:25 | Define commutative property | a⋆b → b⋆a | Same result after swapping |
| 3 | 0:25–0:42 | Addition test | 2+3 vs 3+2 | Addition passes ✓ |
| 4 | 0:42–1:00 | Rational-number addition | Fraction swap | a+b=b+a |
| 5 | 1:00–1:18 | Subtraction test | 5−2 vs 2−5 | Subtraction fails ✕ |
| 6 | 1:18–1:32 | Rational-number subtraction | 2/3−7/8 vs reverse | a−b≠b−a |
| 7 | 1:32–1:47 | Student challenge | Swap-test question | Think before reveal |
| 8 | 1:47–2:00 | Recap | Addition ✓ / Subtraction ✕ | Swap test |

## Scene 1 — "What Happens If We Swap Them?"
Two number cards (2, 3) with a swap arrow. Swap → 3, 2. "Does the answer change?"

## Scene 2 — What Is the Commutative Property?
a⋆b → swap → b⋆a → a⋆b=b⋆a. "Commutative = order can change, result does not."

## Scene 3 — Addition Passes the Swap Test
2+3=5, swap → 3+2=5. Same answer merges. "Addition is commutative."

## Scene 4 — Addition Works for Rational Numbers Too
−5/2 + 3/4 = −7/4. Swap (still addition): 3/4 + (−5/2) = −7/4. a+b=b+a confirmed.

## Scene 5 — Now Try Subtraction
5−2=3. Swap → 2−5=−3. 3≠−3. "Subtraction is NOT commutative."

## Scene 6 — Rational Numbers Confirm the Pattern
2/3−7/8 = 16/24−21/24 = −5/24. Swap → 7/8−2/3 = 21/24−16/24 = 5/24. −5/24 ≠ 5/24.

## Scene 7 — Your Turn: Apply the Swap Test
3/5+2/7 ? 2/7+3/5. Pause, then reveal: both = 31/35. "Addition passes!"

## Scene 8 — Final Recap: The Swap Test
Split: Addition a+b=b+a ✓ COMMUTATIVE. Subtraction a−b≠b−a ✕ NOT COMMUTATIVE.
Takeaway: SWAP THE NUMBERS → CHECK THE RESULT. Same → Commutative ✓. Different → Not Commutative ✕.

## Visual Continuity Plan
One consistent "Swap Test" mechanism throughout: 2+3→3+2→same; 5−2→2−5→different; then rational versions of each. The operation, not the numbers, determines whether swapping works.

## Manim Implementation Ideas
MathTex, Text, VGroup, Arrow, SurroundingRectangle, Transform/ReplacementTransform, TransformMatchingTex, Indicate, Circumscribe, FadeIn/FadeOut, Create, `.animate.move_to()`.

**Important animation principle:** actually move the numbers when demonstrating the swap (animate positions crossing), not an instant replace — the movement itself is the mental model.

## Mathematical Accuracy Checklist
- Addition: a+b=b+a (commutative) — verified for whole numbers and rationals.
- Subtraction: a−b≠b−a (not commutative) — verified for whole numbers and rationals.
- Core definition: changing the order does not change the result (for commutative operations).

**Final "aha":** SWAP → SAME = COMMUTATIVE. SWAP → DIFFERENT = NOT COMMUTATIVE.

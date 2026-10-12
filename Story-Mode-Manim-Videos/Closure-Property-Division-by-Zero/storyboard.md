# Storyboard — Closure Property & the "Division by Zero" Trap

**Concept:** Closure Property under Division for Rational Numbers
**Core "Aha":** An operation is **closed** only when the result stays inside the same set. Division looks closed for rational numbers—until **zero becomes the divisor**.

Grounded in the textbook's treatment of Closure Property: defines closure using whole numbers, then shows rational numbers are closed under addition, subtraction, and multiplication, but **not division** because \(5 \div 0\) is undefined. Excluding zero from the rational-number set makes division closed.

**Target duration:** ≤ 1:59
**Structure:** 9 beats
**One central intuition:** **"The result must stay inside the set."**

---

## Overall Story Flow

| Beat | Time | Purpose | Visual Focus | Key Takeaway |
| --- | ---: | --- | --- | --- |
| 1 | 0:00–0:10 | Hook | A "closed" mathematical box | What does closed mean? |
| 2 | 0:10–0:22 | Intuition | Numbers enter → operation → result | Result must remain in the set |
| 3 | 0:22–0:36 | Fundamentals | Simple whole-number example | Build closure from zero |
| 4 | 0:36–0:49 | Apply to rational numbers | +, −, × | These stay rational |
| 5 | 0:49–1:02 | Introduce division | Rational ÷ rational | Division seems closed |
| 6 | 1:02–1:18 | The trap | 5÷0 | Zero cannot be the divisor |
| 7 | 1:18–1:34 | Why it fails | Multiplication-back check | No number satisfies 0×?=5 |
| 8 | 1:34–1:49 | Student challenge | Decide closed/not closed | Test the divisor |
| 9 | 1:49–1:59 | Recap | Closure summary | Rational numbers are not closed under division |

---

## Beat 1 — The Mathematical "Closed Door" (0:00–0:10)
Q container; 2/3 and 7/8 outside with ÷ between them. "What does 'closed' mean?" → "Does the result stay inside the set?"

## Beat 2 — The Core Idea of Closure (0:10–0:22)
Operation machine: 2 and 3 in, + happens, 5 out. Place 2,3,5 in the same set — check mark if inside, X if outside. "Closure = the result stays in the same set."

## Beat 3 — Build the Definition From Zero (0:22–0:36)
2+3=5 with 2,3,5 ∈ W (whole numbers). Generalize: a,b ∈ S ⇒ a⋆b ∈ S ⇒ closed. "Result must remain in the set."

## Beat 4 — Rational Numbers: Three Operations Pass (0:36–0:49)
- Addition: 2/7 + 5/8 = 51/56 ✓
- Subtraction: 5/9 − 3/4 = −7/36 ✓
- Multiplication: 1/2 × 3/6 = 1/4 ✓

## Beat 5 — Division Looks Like It Works (0:49–1:02)
2/3 ÷ 7/8 = 2/3 × 8/7 = 16/21 (rational). "Division seems closed…" then introduce 5÷0.

## Beat 6 — The "Division by Zero" Trap (1:02–1:18)
5÷0 = 5/0, not defined. "Zero cannot be the divisor." → "So the result is not a rational number."

## Beat 7 — Why Does 5÷0 Fail? (1:18–1:34)
5÷0=? means 0×?=5. But 0×x=0 always (0×1=0, 0×5=0, 0×100=0). No number makes 0×x=5. "There is no quotient."

## Beat 8 — Your Turn: Is Division Closed? (1:34–1:49)
Test A: 3/4 ÷ 2/5. Test B: 5÷0. Pause for a thinking interval, no immediate answer.
Reveal: 3/4÷2/5 = 15/8 ✓, but 5÷0 undefined ✕. One valid counterexample is enough to break closure. **Not closed.**

## Beat 9 — Final Recap (1:49–1:59)
Addition ✓, Subtraction ✓, Multiplication ✓, Division ✕ (5÷0 undefined).
**Q is not closed under division** — because 0∈Q and division by 0 is undefined.
Excluding zero from Q makes the resulting collection closed under division.
Final takeaway: **Closure means the result stays in the set.**

---

## Visual Continuity Plan
One persistent Q container throughout:
Set → Closure idea → Q → {+,−,×} → ÷ → 5÷0 → undefined → not closed

## Manim Object Strategy
MathTex, Text, Rectangle, VGroup/Group, Arrow, Line, Circumscribe/Indicate, TransformMatchingTex, FadeIn/FadeOut, Create, `.animate.move_to()`. Beat 8 needs an actual thinking pause (no narration/animation) before the reveal.

## Mathematical Accuracy Checklist
- Closure = result of an operation remains in the same set.
- Rational numbers are closed under addition, subtraction, multiplication.
- Division of rationals is rational when the divisor is non-zero.
- 5÷0 is undefined.
- Therefore Q is **not** closed under division.
- Excluding zero from Q makes the resulting collection closed under division.

**Single "aha" for the entire video:**
> Closure means: after the operation, the result must still belong to the set.

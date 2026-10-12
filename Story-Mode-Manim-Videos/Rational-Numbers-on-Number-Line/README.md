# Where Do Fractions Live? — Rational Numbers on a Number Line
## Topic Status & Build Information

**Topic Folder:** `Rational-Numbers-on-Number-Line/`

**Video Title:** "Where Do Fractions Live? — Rational Numbers on a Number Line"

**Status:** ✅ Storyboard received and ready for build (Stage 4 of process.md)

---

## Storyboard Content

See `storyboard.md` — a complete 8-scene breakdown with:
- Visual composition and animation sequences for each scene
- Exact mathematical elements and formulas ($p/q,\ q\neq0$)
- Manim implementation hints for each scene
- Pedagogical goals and narration intents
- Worked example: $\frac{3}{7}$ (positive) and $-\frac{3}{4}$ (negative)
- Real-world application: measuring $\frac{3}{4}$ metre on a ruler/tape
- Student challenge: $-\frac{4}{5}$ with a 5-second pause before reveal

---

## Key Characteristics

| Aspect | Value |
| --- | --- |
| **Duration (target)** | ~2 minutes 35 seconds |
| **Target Class Level** | Classes 6–12, primary focus Class 8 |
| **Core Concept** | Denominator = equal parts, Numerator = count, Sign = direction |
| **Main Formula** | $p/q,\ q\neq0$ |
| **Worked Example** | $\frac{3}{7}$ — divide 0→1 into 7 equal parts, count 3 |
| **Negative Example** | $-\frac{3}{4}$ — divide −1→0 into 4 equal parts, count 3 left |
| **Real-World Hook** | Measuring ruler/tape — locating $\frac{3}{4}$ metre |
| **Student Challenge** | $-\frac{4}{5}$, with a 5-second pause before the answer reveals |
| **Visual Style** | Persistent, reusable number-line object — reused/transformed across scenes rather than rebuilt each time |

---

## Next Steps

### For Claude Code (Build Stage)

When ready to generate the Manim script, provide this build prompt:

> Create a new story-mode video Manim project in `Rational-Numbers-on-Number-Line/`
>
> **Topic:** Representation of Rational Numbers on a Number Line
>
> **Storyboard:** 8 scenes (see `storyboard.md`)
>
> **Concrete Numbers:**
> - Worked example (positive): $\frac{3}{7}$ — divide 0→1 into 7 parts, count 3
> - Negative example: $-\frac{3}{4}$ — divide −1→0 into 4 parts, count 3 left
> - Real-world: $\frac{3}{4}$ metre on a ruler
> - Student challenge: $-\frac{4}{5}$ — divide −1→0 into 5 parts, count 4 left
>
> **Visual Style:**
> - Reuse established chalkboard background and chalk-vector aesthetic
> - A single, reusable number-line structure transformed/rescaled across scenes (per denominator/example) rather than rebuilt from scratch each time
> - VoiceoverScene + edge-tts (en-IN-PrabhatNeural) with bookmark-based sync
> - Real per-word SRT captions via edge-tts word boundaries
> - Sound effects (ding, swipe, etc.) at key moments
>
> **Teaching Constraints:**
> - Explain denominator = equal parts and numerator = count clearly, before applying to any specific example
> - Show positive AND negative rational numbers using the identical division method
> - Include a real-world (ruler/measurement) anchor
> - Include a "YOUR TURN" student challenge with an actual pause (no narration/animation) before revealing the answer
> - End with a compact 3-rule recap: Denominator → parts, Numerator → count, Sign → direction
>
> **Production Pipeline:**
> - Render at 360p/30fps first for fast iteration
> - Generate real SRT from edge-tts per-word timestamps
> - Burn captions into preview with established ffmpeg style
> - Verify sync frame-by-frame against SRT before approving scenes
> - Final render at 1080p/60fps with captions

### For Content Verification

Before starting the build:
1. Verify the storyboard against the state textbook (ensure formulas and terminology match)
2. Check the Manim reference repos for reusable number-line/ruler animation patterns
3. Confirm the audio timing estimates (each scene duration) align with typical narration pacing

---

## Files in This Folder

- **`storyboard.md`** — Complete 8-scene breakdown with visual/animation/math details
- **`README.md`** (this file) — Status and build information

---

## Process Reference

This topic follows the stages outlined in `Story-Mode-Manim-Videos/process.md`:
- ✅ Stage 1 — Source the topic from textbook
- ✅ Stage 2 — Draft storyboard with clear visual and pedagogical goals
- ⏳ Stage 3 — Verify content (accuracy, grade level, explained terms, payoff)
- ⏳ Stage 3.5 — Check local Manim repos for reusable patterns
- ⏳ Stage 4 — Build prompt for Claude Code (ready to go)

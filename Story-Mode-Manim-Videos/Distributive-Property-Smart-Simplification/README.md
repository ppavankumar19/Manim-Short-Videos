# Distributive Property & Smart Simplification
## Topic Status & Build Information

**Topic Folder:** `Distributive-Property-Smart-Simplification/`

**Video Title:** "The Power of Breaking It Apart"

**Status:** ✅ Storyboard verified and ready for build prompt (Stage 4 of process.md)

---

## Storyboard Content

See `storyboard.md` — a complete 7-scene breakdown with:
- Visual composition and animation sequences for each scene
- Exact mathematical elements and formulas ($a(b + c) = ab + ac$)
- Manim implementation hints for each scene
- Pedagogical goals and narration intents
- Worked examples: $4 \times 23$ and $6 \times 98$ with student challenge
- Real-world application: bulk purchase cost calculation

---

## Key Characteristics

| Aspect | Value |
| --- | --- |
| **Duration (target)** | 2–3 minutes |
| **Target Class Level** | Classes 6–12 |
| **Core Concept** | Area Model (rectangle splitting to show distribution) |
| **Main Formula** | $a(b + c) = ab + ac$ |
| **Worked Example 1** | $4 \times 23 = 4(20 + 3) = 80 + 12 = 92$ |
| **Worked Example 2 (Challenge)** | $6 \times 98 = 6(100 - 2) = 600 - 12 = 588$ |
| **Real-World Hook** | Ancient land surveyors calculating divided land areas |
| **Practical App** | Calculating bulk purchase costs (5 kits, each with 2 items) |
| **Visual Style** | Chalkboard, chalk-vector rectangles, color-coded variables (red, blue, green) |

---

## Next Steps

### For Claude Code (Build Stage)

When ready to generate the Manim script, provide this build prompt:

> Create a new story-mode video Manim project in `Distributive-Property-Smart-Simplification/`
> 
> **Topic:** Distributive Property & Smart Simplification ("The Power of Breaking It Apart")
> 
> **Storyboard:** 7 scenes (see `storyboard.md`)
> 
> **Characters/Scenario:** Ancient land surveyors (hook), then abstract mathematics
> 
> **Concrete Numbers:**
> - Main formula: $a(b + c) = ab + ac$
> - Worked example 1: $4 \times 23 = 80 + 12 = 92$
> - Worked example 2 (challenge): $6 \times 98 = 600 - 12 = 588$
> - Real-world: 5 kits, each $20 + $3 items, total $115
> 
> **Visual Style:**
> - Reuse established chalkboard background and chalk-vector aesthetic
> - Rectangle area model with yellow/green split (wheat/corn for hook, then abstract)
> - Color-coded variables: red for $a$, blue for $b$, green for $c$
> - VoiceoverScene + edge-tts (en-IN-PrabhatNeural) with bookmark-based sync
> - Real per-word SRT captions via edge-tts word boundaries
> - Sound effects (ding, swipe, etc.) at key moments
> 
> **Teaching Constraints:**
> - Explain every formula variable ($a$, $b$, $c$) in the narration
> - Show the area model visually before introducing variables
> - Demonstrate that distribution works with subtraction (Scene 6 challenge)
> - Provide a tangible real-world anchor (bulk purchase scenario)
> - Include a student pause/challenge moment with a hint and solution reveal
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
2. Check the Manim reference repos for reusable rectangle animation patterns
3. Confirm the audio timing estimates (each scene duration) align with typical narration pacing

---

## Files in This Folder

- **`storyboard.md`** — Complete 7-scene breakdown with visual/animation/math details
- **`README.md`** (this file) — Status and build information

---

## Process Reference

This topic follows the stages outlined in `Story-Mode-Manim-Videos/process.md`:
- ✅ Stage 1 — Source the topic from textbook
- ✅ Stage 2 — Draft storyboard with clear visual and pedagogical goals
- ✅ Stage 3 — Verify content (accuracy, grade level, explained terms, payoff)
- ✅ Stage 3.5 — Check local Manim repos for reusable patterns
- ⏳ Stage 4 — Build prompt for Claude Code (ready to go)

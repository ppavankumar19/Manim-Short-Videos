# Production-Ready Storyboard — as built

## Simple Interest vs. Compound Interest: Deriving the Compound Interest Formula

CLASS 8 MATHS · CHAPTER 5 (COMPARING QUANTITIES USING PROPORTION) · STORYMODE 06

**LLM KEY / FUNCTION NAME:** `simple_vs_compound_interest_formula`
**CHAPTER:** Class 8 · Chapter 5 — Comparing Quantities using Proportion
**TEXTBOOK THREAD:** Ramesh's and Sreenu's methods for the same Rs 100 at 10% for
two years (Rs 120 and Rs 121), simple interest on the original principal, and the
derivation `A₁ → A₂ → A = P(1 + R/100)ⁿ`.

## Learning objective

By the end of the video a student can: compute simple interest with
`SI = PTR/100` and explain that its base never changes; explain why compound
interest grows (each new amount becomes the next principal); **derive**
`A = P(1 + R/100)ⁿ` as one growth factor per period; keep the **amount** and the
**compound interest** apart (`CI = A − P`); and state that SI and CI agree after
the first period.

**Primary takeaway:**
`A = P(1 + R/100)ⁿ` (amount) · `CI = A − P` · one period: SI = CI

## Core visual metaphor — two money ladders

Two **money ladders** stand side by side. On the **simple-interest** ladder a
drawn **padlock** fixes the principal block while identical interest blocks stack
linearly beside it (`+Rs 10`, `+Rs 10`). On the **compound** ladder the `P + I₁`
blocks **merge into one A₁ block that slides down into the next year's principal
slot**, and from it a visibly **larger I₂ block is cut** — the extra Re 1 is
literally the interest on the previous year's interest. The ladders then hand
over to the algebra through `TransformMatchingTex`, so `P` and the growth factor
stay visually continuous from `P + PR/100` to `P(1 + R/100)ⁿ`.

## Realistic diagrams (production direction)

- the ladders are **filled blocks** (principal, interest, amount), not outlines;
- a drawn **padlock** (shackle + body + keyhole) locks the SI principal;
- **filled coin stacks and a rupee-note icon** sit on the two account cards;
- the block algebra hands over to the symbols with `TransformMatchingTex`;
- fixed-column answer/recap rows, so A/B/C/D and 1/2/3/4 share one vertical line.

## Scene plan (timings are the delivered cut's own)

| # | in | Scene | Key on-screen text | Focus |
|---|---|---|---|---|
| 0 | 0:00 | The mystery: Rs 120 vs Rs 121 | Ramesh's method · Sreenu's method | where the extra Re 1 comes from |
| 1 | 0:31 | Simple interest | Rs 10 + Rs 10 = Rs 20 → Rs 120 · SI = PTR/100 | the base never changes |
| 2 | 1:11 | Compound interest | 100 → 110 → **Rs 11** → 121 | the amount becomes the next principal |
| 3 | 1:47 | The one-period growth factor | A₁ = P + PR/100 = P(1 + R/100) | name the bracket |
| 4 | 2:13 | Year 2 | A₂ = P(1 + R/100)(1 + R/100) = P(1 + R/100)² | the same factor again |
| 5 | 2:43 | n years | one factor per year → A = P(1 + R/100)ⁿ | n = number of periods |
| 6 | 3:10 | Amount is not the interest | CI = A − P = P(1 + R/100)ⁿ − P | keep them apart |
| 7 | 3:39 | Apply it | 5000(108/100)² = Rs 5,832 · CI = Rs 832 | the formula at work |
| 8 | 4:13 | SI vs CI | same first period, then CI pulls ahead | the two ladders |
| 9 | 4:47 | YOUR TURN — questions read, then the silent clock | four checks | all concepts |
| 10 | 5:28 | The answers | A SI 300/amount 2300 · B A 6050/CI 1050 | all concepts |
| 11 | 6:04 | Recap, then the spoken thank-you card | A₁ → A₂ → A = P(1+R/100)ⁿ · CI = A − P | all concepts |

**Delivered file**

    final_videos/SimpleVsCompoundInterestFormulaStory_captioned.mp4
    640×360, 30 fps, 395.30 s (6 min 35 s), 120 captions, 14.90 MB (15,619,442 B)
    final_videos/SimpleVsCompoundInterestFormulaStory_captioned.srt

The raw render and its ground-truth SRT sit in
`media/videos/simple_vs_compound_interest_formula/360p30/`.

## The production instructions

1. **No overlaps, and proper alignment/positioning.**
   `audit_sync_overlap.py` on the rendered cut → **0 defect flags**; only the
   deliberate **OFF-CENTRE review entries (237)** — chiefly the two ladders and
   the left-hand account cards. `audit_clearance.py` → **0 tight pairs, 0
   text/line collisions, 0 foreign-box collisions**. `audit_badge_clearance.py`
   → all headings/sub-headings **ok**, tightest `s4.sub` at **0.52 units**
   (requirement 0.30); nothing below `CAPTION_SAFE_Y = -2.00`.

2. **The YOUR TURN clock: centred, ten seconds, silent** —
   `play_challenge_countdown(self, seconds=10, position=(BOARD_CX, BOARD_CY))`
   with the four question cards in the four corners; `find_timer.py` locates the
   window at **313 s → 323 s** (mid 318 s).

3. **Realistic diagrams** — see the production direction above.

## Voice sync

Every reveal waits for its bookmark (`self.wait(leftover(tracker, "bN"))` before
the play) and `closing()` consumes each window's tail.

**All twelve pieces at 0.00 s stretch:**

| piece | audio (s) | anim (s) | stretch |
|---|---|---|---|
| title | 30.38 | 30.38 | 0.00 |
| s1 | 38.80 | 38.80 | 0.00 |
| s2 | 34.16 | 34.16 | 0.00 |
| s3 | 25.00 | 25.00 | 0.00 |
| s4 | 29.58 | 29.58 | 0.00 |
| s5 | 26.38 | 26.38 | 0.00 |
| s6 | 27.49 | 27.49 | 0.00 |
| s7 | 32.79 | 32.79 | 0.00 |
| s8 | 33.64 | 33.64 | 0.00 |
| s9q | 24.96 | 16.98 | 0.00 |
| s9a | 35.86 | 35.86 | 0.00 |
| s10 | 31.83 | 31.35 | 0.00 |
| **TOTAL** | **370.87** | **362.41** | **0.00** |

`verify_sync.py`: video 395.291 s, audio 393.344 s, silent tail +1.947 s [ok],
**120 captions**, first 0.14 s, last 393.31 s, 107 speech blocks (328.8 s),
**0 captions in silence, 0 speech blocks (> 1.0 s) uncaptioned** → PASS.
`verify_captions.py`: narration **1064 words = SRT 1064 words** → PASS.

Delivered voice windows: title 0.14–31.59 · s1 31.59–71.55 · s2 71.55–106.97 ·
s3 106.97–132.97 · s4 132.97–163.40 · s5 163.40–190.69 · s6 190.69–219.09 ·
s7 219.09–253.27 · s8 253.27–287.89 · s9q 287.89–328.15 (clock 313–323) ·
s9a 328.15–364.25 · s10 364.25–395.30.

The closing scene is fixed by bookmarks only: the recap rows come on one per
bookmark, the strip on its own bookmark on the sentence that says it, the board
is cleared and the thank-you card revealed only in front of "Thank you for
watching,", and the goodbye lands on its own bookmark before "see you in the next
lesson".

## Pedagogical safeguards honoured

- **The formula is derived, never opened with.** Scenes 3–5 take `A₁`, then
  `A₂`, then the n-year power; the formula only appears after the repeated
  multiplication has been shown.
- **The SI principal stays locked.** A drawn padlock holds the principal block
  while identical interest blocks stack beside it — `P + I` never becomes the
  next SI principal (which would accidentally draw compound interest).
- **The CI amount genuinely re-bases.** The `P + I₁` blocks merge into `A₁` and
  slide into the next year's principal slot; the larger `I₂` is cut from it.
- **Amount and interest are kept apart**: the formula gives the **amount**, and
  `CI = A − P` is written separately.
- **The exponent is explained**: one factor per year, `n` = the number of growth
  periods.
- **Annual compounding only** — no half-yearly compounding is mixed in (that is a
  separate topic in this chapter).
- **SI and CI agree after the first period**, stated explicitly in scene 8.

## Tools in this folder

`assemble_sicompound.py` (splices `_sicompound_fragment.py` +
`_sicompound_beats.py` into the proven head), `setup_tools.py`,
`make_draft_srt.py`, `tts_precheck.py`, `audit_sync_overlap.py`,
`audit_clearance.py`, `audit_badge_clearance.py`, `scene_frames.py`,
`find_timer.py`, and the chapter's `pipeline_360.py`.

**Frame sweep:** `frames360/chk/` holds one still per scene (`01_title` …
`12_s10`) plus the centred THINK clock at mid-countdown.

**Money glyph:** every amount is written **Rs** (the brief's allowed fallback).

**Note:** this topic is built fresh for Chapter 5; the older, differently-built
`Story-Mode-Manim-Videos\Simple-vs-Compound-Interest` folder was not touched.

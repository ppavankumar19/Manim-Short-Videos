# Production-Ready Storyboard — as built

## Finding Discounts & Marked Price: Calculating SP and Discount Percentages

CLASS 8 MATHS · CHAPTER 5 (COMPARING QUANTITIES USING PROPORTION) · STORYMODE 03

**LLM KEY / FUNCTION NAME:** `discounts_marked_price_and_rebate`
**CHAPTER:** Class 8 · Chapter 5 — Comparing Quantities using Proportion
**TEXTBOOK THREAD:** marked price (list/catalogue price), discount (rebate),
selling price, `MP − Discount = SP`, the discount percentage measured on the
marked price, and the `(100 − d)%` shortcut.

## Learning objective

By the end of the video a student can: name the marked price, the discount
(rebate) and the selling price and write `MP − Discount = SP`; find the discount
and the SP when MP and the discount % are given; recover the discount % from MP
and SP, using **MP as the base**; use the shortcut `SP = (100 − d)/100 × MP`;
and check the answer with `SP < MP`.

**Primary takeaway:**
`MP − Discount = SP` · `d% = D/MP × 100` · `SP = (100 − d)/100 × MP`

## Core visual metaphor — the price bar you cut

A persistent shop **price tag** carries the marked price; the price bar **is**
100% = MP, and the discount portion is physically **cut off** the bar (a cutter
motion) leaving the SP portion behind, with `MP − Discount = SP` written
underneath. In the reverse case two bars (Rs 3,600 and Rs 3,312) reveal the
**Rs 288 gap** between them, and that gap then travels up above the full bar to
give `288/3600 × 100 = 8%`.

## Realistic diagrams (production direction)

- a **glossy price sticker**, a **tag with a punched hole**, a **percent badge**;
- drawn, filled items: a **book** (page block), a **bicycle** (wheel hubs and
  frame), a **ceiling fan** (solid blades);
- the **split bars**: the discount slice leaves the MP bar and slides aside;
- **filled notes and coin stacks** where money is shown;
- mistake cards carry a **drawn cross** (in the card's own VGroup, in its top
  half, clear of the lettering) with the correction in the bottom half;
- fixed-column answer/recap rows, so A/B/C and 1/2/3/4 share one vertical line.

## Scene plan (timings are the delivered cut's own)

| # | in | Scene | Key on-screen text | Focus |
|---|---|---|---|---|
| 0 | 0:00 | The tag says Rs 1600, the sticker says 6% OFF | MP · DISCOUNT/REBATE · SP | the three quantities |
| 1 | 0:45 | The three parts and their relation | MP − DISCOUNT = SP | the tagged price stays |
| 2 | 1:21 | A book Rs 80 with 15% off | D = Rs 12 → SP = Rs 68 | find D, then SP |
| 3 | 2:02 | A cycle Rs 3600 sold for Rs 3312 | gap Rs 288 → 288/3600 × 100 = 8% | the base is MP |
| 4 | 2:38 | A fan Rs 1600 with 6% off | D = Rs 96 → SP = Rs 1504 | amount ≠ rate |
| 5 | 3:17 | The shortcut | 6% off leaves 94% → Rs 1504 | both routes agree |
| 6 | 3:59 | Which formula? | MP+% · MP+SP · MP+Rs decision board | pick the route |
| 7 | 4:35 | Common mistakes, each crossed | wrong base · MP + D · amount vs rate · 15% = paying 15% | corrections |
| 8 | 5:01 | Reasonableness | a discount means SP < MP | check every answer |
| 9 | 5:41 | YOUR TURN — questions read, then the silent clock | four prompts | all concepts |
| 10 | 6:26 | The answers | A Rs 31.50/Rs 418.50 · B 10% · C Rs 237.50 | all concepts |
| 11 | 7:07 | Recap, then the spoken thank-you card | TAG → REDUCE → PAY → COMPARE | all concepts |

**Delivered file**

    final_videos/DiscountsMarkedPriceAndRebateStory_captioned.mp4
    640×360, 30 fps, 455.53 s (7 min 36 s), 156 captions, 16.74 MB (17,548,965 B)
    final_videos/DiscountsMarkedPriceAndRebateStory_captioned.srt

The raw render and its ground-truth SRT sit in
`media/videos/discounts_marked_price_and_rebate/360p30/`.

## The production instructions

1. **No overlaps, and proper alignment/positioning.**
   `audit_sync_overlap.py` against the rendered audio → **0 defect flags** (no
   text-in-text, partial, text-on-arrow, text-on-side, text-outside-box,
   out-of-board, in-caption-band, near-badge, empty-text, LaTeX-as-text); only
   the deliberate **OFF-CENTRE review entries (224)**.
   `audit_clearance.py` → **0 pairs closer than 0.22, 0 text/line collisions, 0
   foreign-box collisions**.
   `audit_badge_clearance.py` → every heading/sub-heading **ok**; tightest
   `s8.sub` at **0.55 units** (requirement 0.30). Nothing below
   `CAPTION_SAFE_Y = -2.00`.

2. **The YOUR TURN clock: centred, ten seconds, silent** —
   `play_challenge_countdown(self, seconds=10, position=(BOARD_CX, BOARD_CY))`
   with the four prompt cards in the four corners; `find_timer.py` finds the
   darkened window at **367 s → 377 s** (mid 372 s).

3. **Realistic diagrams** — see the production direction above.

## Voice sync

Every reveal waits for its narration bookmark (`self.wait(leftover(tracker,
"bN"))` *before* the play) and `closing()` consumes each window's tail.

**All twelve pieces at 0.00 s stretch:**

| piece | audio (s) | anim (s) | stretch |
|---|---|---|---|
| title | 43.92 | 43.92 | 0.00 |
| s1 | 33.02 | 33.02 | 0.00 |
| s2 | 39.03 | 39.03 | 0.00 |
| s3 | 34.58 | 34.58 | 0.00 |
| s4 | 38.99 | 38.99 | 0.00 |
| s5 | 39.17 | 39.17 | 0.00 |
| s6 | 37.36 | 37.36 | 0.00 |
| s7 | 19.24 | 19.24 | 0.00 |
| s8 | 38.84 | 38.84 | 0.00 |
| s9q | 33.20 | 33.20 | 0.00 |
| s9a | 40.20 | 40.20 | 0.00 |
| s10 | 33.72 | 33.23 | 0.00 |
| **TOTAL** | **431.27** | **430.78** | **0.00** |

`verify_sync.py`: video 455.519 s, audio 453.589 s, silent tail +1.930 s [ok],
**156 captions**, first 0.30 s, last 453.56 s, 134 speech blocks (375.5 s),
**0 captions in silence, 0 speech blocks (> 1.0 s) uncaptioned** → PASS.
`verify_captions.py`: narration **1387 words = SRT 1387 words** → PASS.

Delivered voice windows: title 0.30–45.17 · s1 45.17–81.43 · s2 81.43–122.55 ·
s3 122.55–158.71 · s4 158.71–197.13 · s5 197.13–239.61 · s6 239.61–275.54 ·
s7 275.54–301.25 · s8 301.25–341.66 · s9q 341.66–386.34 (clock at 367–377) ·
s9a 386.34–427.40 · s10 427.40–455.53.

The closing scene is fixed by bookmarks only: recap rows one per bookmark, the
strip on its own bookmark on the sentence that says it, the board cleared and
the thank-you card revealed only in front of "Thank you for watching,", and the
goodbye on its own bookmark before "see you in the next lesson"
(`closing(run_time = 0.90)`).

## Pedagogical safeguards honoured

- **MP is the base and stays visible.** Scene 3 states it in words and on a chip:
  the discount percentage is `288/3600 × 100`, measured on the **marked price**,
  never on the selling price; the tag never leaves the board.
- **Discount and rebate are one idea** — the same card carries both names, and no
  second formula is introduced.
- **Amount and rate are kept apart** — scene 4 shows the discount **amount**
  (Rs 96) and the discount **rate** (6%) as two different chips.
- **A discount reduces.** Scene 8 checks `SP < MP` and that `d%` off leaves
  `(100 − d)%` payable, and the relation is always written `MP − D = SP`, never
  `MP + D`.
- **"15% off" is not "pay 15%"** — scene 5 shows 6% off leaving 94% payable.
- **No successive discounts** anywhere.

## Tools in this folder

`assemble_discounts.py` (splices `_discounts_fragment.py` +
`_discounts_beats.py` into the proven head), `setup_tools.py`,
`make_draft_srt.py`, `tts_precheck.py`, `audit_sync_overlap.py`,
`audit_clearance.py`, `audit_badge_clearance.py`, `scene_frames.py`,
`find_timer.py`, and the chapter's `pipeline_360.py`.

**Frame sweep:** `frames360/chk/` holds one still per scene (`01_title` …
`12_s10`) plus the centred THINK clock at mid-countdown.

**Money glyph:** every amount is written **Rs** (the brief's allowed fallback).

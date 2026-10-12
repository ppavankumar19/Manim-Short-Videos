# Production-Ready Storyboard — as built

## Profit, Loss & Overhead Expenses: Solving Single and Double Transaction Problems

CLASS 8 MATHS · CHAPTER 5 (COMPARING QUANTITIES USING PROPORTION) · STORYMODE 04

**LLM KEY / FUNCTION NAME:** `profit_loss_overhead_expenses_and_transactions`
**CHAPTER:** Class 8 · Chapter 5 — Comparing Quantities using Proportion
**TEXTBOOK THREAD:** profit and loss, the cost price as the percentage base,
overhead expenses, and the two-item transaction where equal gain and loss
percentages do **not** cancel.

## Learning objective

By the end of the video a student can: build the **total cost price** as purchase
price **+ overheads** (transport, repairs, labour, maintenance, commission,
storage); decide profit/loss by comparing SP with CP *before* subtracting; take
the percentage on the **cost price**; and solve a two-item problem by comparing
**total CP with total SP** rather than cancelling a gain against a loss.

**Primary takeaway:**
`total CP = purchase + overheads` · `profit % = profit/CP × 100` ·
`+x%` and `−x%` do **not** cancel (the bases differ)

## Core visual metaphor — the transaction ledger

Every scene is built on one **ledger** with two columns: **MONEY OUT** (the
purchase, then the transport, repair and other overhead tags that **attach** to
it and merge into a shaded **TOTAL COST PRICE** box) and **MONEY IN** (the
selling price). A two-pan **balance** tilts with the money-in side for profit and
with the money-out side for loss, and in the two-item problem two **mini-ledgers
physically merge** into the one total ledger.

## Realistic diagrams (production direction)

- drawn, filled items: a **refrigerator, a flat, a table, a bicycle, a TV set and
  a bunch of bananas**, plus a **truck** and a **wrench** on the overhead tags;
- the **ledger** columns are filled shaded boxes, and the overhead tags visibly
  **travel into** the TOTAL COST PRICE box;
- the **balance** is a real two-pan beam that tilts;
- the misconception is stopped on screen: the tempting `+20% −20% → 0%` chip is
  **crossed out**, pulled apart, and replaced by the recovered cost prices
  (Rs 2,500 and Rs 3,750) before the totals merge;
- a **drawn cross** always sits in the same object as the card it strikes, in the
  card's top half, clear of the lettering;
- fixed-column answer/recap rows, so A/B/C/D and 1/2/3/4 share one vertical line.

## Scene plan (timings are the delivered cut's own)

| # | in | Scene | Key on-screen text | Focus |
|---|---|---|---|---|
| 0 | 0:00 | The fridge: Rs 5000 + Rs 100 + Rs 500 | real profit Rs 1,400, **not** Rs 2,000 | the purchase price is not the cost |
| 1 | 0:31 | Profit, loss, or neither | SP 650 → profit Rs 150 · SP 450 → loss Rs 50 | compare first |
| 2 | 1:13 | The percentage base | profit/CP × 100 (the SP version crossed) | the base is CP |
| 3 | 1:39 | The refrigerator ledger | 5000 + 100 + 500 = 5600 · profit 1400 = **25%** | overheads count |
| 4 | 2:07 | An overhead loss | 4,50,000 + 10,000 = 4,60,000 · loss 34,500 = **7.5%** | overhead loss |
| 5 | 2:44 | The two-item trap | "+20% −20% → 0%" **stopped**; CP 2500 and 3750 | the bases differ |
| 6 | 3:18 | The whole transaction | total CP 6250 vs total SP 6000 → loss 250 = 4% | compare the totals |
| 7 | 3:52 | The decision process | five steps | the method |
| 8 | 4:25 | Overheads and spoilage | bananas: CP 1500, SP 1575 → 5% | spoiled money is still cost |
| 9 | 5:03 | YOUR TURN — questions read, then the silent clock | four checks | all concepts |
| 10 | 5:40 | The answers | A CP 4500, profit 900 = 20% · B loss 200 = 1% | the two-item check |
| 11 | 6:26 | Recap, then the spoken thank-you card | ADD · COMPARE · PERCENT · TOTALS | all concepts |

**Delivered file**

    final_videos/ProfitLossOverheadExpensesAndTransactionsStory_captioned.mp4
    640×360, 30 fps, 404.67 s (6 min 45 s), 132 captions, 15.04 MB (15,772,062 B)
    final_videos/ProfitLossOverheadExpensesAndTransactionsStory_captioned.srt

The raw render and its ground-truth SRT sit in
`media/videos/profit_loss_overhead_expenses_and_transactions/360p30/`.

## The production instructions

1. **No overlaps, and proper alignment/positioning.**
   `audit_sync_overlap.py` on the rendered cut → **0 defect flags**; only the
   deliberate **OFF-CENTRE review entries (243)**. `audit_clearance.py` → **0
   tight pairs, 0 text/line collisions, 0 foreign-box collisions**.
   `audit_badge_clearance.py` → all headings/sub-headings **ok**, tightest
   `s10.head` at **0.68 units** (requirement 0.30); nothing below
   `CAPTION_SAFE_Y = -2.00`.

2. **The YOUR TURN clock: centred, ten seconds, silent** —
   `play_challenge_countdown(self, seconds=10, position=(BOARD_CX, BOARD_CY))`
   with the four question cards in the four corners; `find_timer.py` locates the
   window at **326 s → 335 s** (mid 331 s).

3. **Realistic diagrams** — see the production direction above.

## Voice sync

Every reveal waits for its bookmark (`self.wait(leftover(tracker, "bN"))` before
the play) and `closing()` consumes each window's tail.

**All twelve pieces at 0.00 s stretch:**

| piece | audio (s) | anim (s) | stretch |
|---|---|---|---|
| title | 29.70 | 29.70 | 0.00 |
| s1 | 40.86 | 40.86 | 0.00 |
| s2 | 25.01 | 25.01 | 0.00 |
| s3 | 27.09 | 27.09 | 0.00 |
| s4 | 34.83 | 34.83 | 0.00 |
| s5 | 31.35 | 31.35 | 0.00 |
| s6 | 33.17 | 33.17 | 0.00 |
| s7 | 31.37 | 31.37 | 0.00 |
| s8 | 33.21 | 33.21 | 0.00 |
| s9q | 29.12 | 21.57 | 0.00 |
| s9a | 43.38 | 43.38 | 0.00 |
| s10 | 21.65 | 21.64 | 0.00 |
| **TOTAL** | **380.74** | **373.18** | **0.00** |

The first cut of this topic came back with **s10 at 0.79 s stretch** (the closing
sentence's own audio ran faster than the draft SRT assumed). It was fixed by
trimming the s10 reveals (board clear 0.55 → 0.35 s, card 0.50 → 0.35 s, goodbye
0.45 → 0.30 s, `closing(run_time=0.60)`); the audit was re-run against the real
SRT (0.00 s) before the cut was re-rendered.

`verify_sync.py`: video 404.653 s, audio 402.539 s, silent tail +2.114 s [ok],
**132 captions**, first 0.30 s, last 402.50 s, 119 speech blocks (333.3 s),
**0 captions in silence, 0 speech blocks (> 1.0 s) uncaptioned** → PASS.
`verify_captions.py`: narration **1186 words = SRT 1186 words** → PASS.

Delivered voice windows: title 0.30–31.19 · s1 31.19–73.22 · s2 73.22–99.11 ·
s3 99.11–127.49 · s4 127.49–164.57 · s5 164.57–198.45 · s6 198.45–232.94 ·
s7 232.94–265.52 · s8 265.52–303.16 · s9q 303.16–340.14 (clock 326–335) ·
s9a 340.14–386.07 · s10 386.07–404.67.

The closing scene is fixed by bookmarks only: the four recap rows come on one per
bookmark, the strip on its own bookmark on the sentence that says it, the board
is cleared and the thank-you card revealed only in front of "Thank you for
watching,", and the goodbye lands on its own bookmark before "see you in the next
lesson".

## Pedagogical safeguards honoured

- **Overheads belong to the cost.** The very first scene contrasts the naive
  Rs 7,000 − Rs 5,000 = Rs 2,000 with the real Rs 7,000 − Rs 5,600 = Rs 1,400,
  and every later ledger adds transport and repairs *before* any profit is
  computed.
- **The percentage base is CP.** Scene 2 writes `profit/CP × 100` and shows the
  common `profit/SP × 100` **crossed out**.
- **Comparison before subtraction.** Scene 1 asks which is bigger, then writes
  `profit = SP − CP` or `loss = CP − SP`.
- **Equal gain and loss percentages do not cancel.** Scene 5 lets the tempting
  "0%" appear, stops it with a drawn cross, and recovers the two cost prices
  (Rs 3,000 = 120% of CP₁ → CP₁ = Rs 2,500; Rs 3,000 = 80% of CP₂ → CP₂ =
  Rs 3,750) before scene 6 compares the totals — and no memorised shortcut is
  introduced.
- **Overheads still count when goods spoil** (scene 8: bananas, CP Rs 1,500 with
  transport, SP Rs 1,575 → 5%).
- **Multiple items use the totals**: total CP against total SP, never one item's
  percentage against another's.

## Tools in this folder

`assemble_profitloss.py` (splices `_profitloss_fragment.py` +
`_profitloss_beats.py` into the proven head), `setup_tools.py`,
`make_draft_srt.py`, `tts_precheck.py`, `audit_sync_overlap.py`,
`audit_clearance.py`, `audit_badge_clearance.py`, `scene_frames.py`,
`find_timer.py`, and the chapter's `pipeline_360.py`.

**Frame sweep:** `frames360/chk/` holds one still per scene (`01_title` …
`12_s10`) plus the centred THINK clock at mid-countdown.

**Money glyph:** every amount is written **Rs** (the brief's allowed fallback).

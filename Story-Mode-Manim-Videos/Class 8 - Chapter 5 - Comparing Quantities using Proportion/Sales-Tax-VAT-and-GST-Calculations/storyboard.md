# Production-Ready Storyboard — as built

## Sales Tax, VAT & GST Calculations: Determining Original Prices and Total Bills

CLASS 8 MATHS · CHAPTER 5 (COMPARING QUANTITIES USING PROPORTION) · STORYMODE 05

**LLM KEY / FUNCTION NAME:** `sales_tax_vat_and_gst_calculations`
**CHAPTER:** Class 8 · Chapter 5 — Comparing Quantities using Proportion
**TEXTBOOK THREAD:** sales tax as a percentage increase, the VAT-inclusive bill,
GST on goods and services, recovering the base price from a tax-inclusive total,
and the textbook's CGST/SGST split.

## Learning objective

By the end of the video a student can: name the base price, the tax amount and
the final bill; read a tax of `r%` as `(100 + r)%` of the base and compute
`Bill = (100 + r)/100 × P`; recover the base from a tax-inclusive bill with
`P = B × 100/(100 + r)`; split a GST into CGST and SGST in the textbook's worked
case; and keep a **tax (which adds)** apart from a **discount (which removes)**.

**Primary takeaway:**
`tax = r/100 × base` · `bill = base + tax = (100+r)/100 × base` ·
`base = bill × 100/(100+r)`

## Core visual metaphor — the bill bar and the tax layer

A persistent **bill bar** is 100% = the base price. A translucent **tax layer
descends from above, lands flush on the bar and merges into it**, while a drawn
**receipt grows** as the layer joins. For the reverse problem the bar is shown as
**118%** with the 18% portion marked, that portion **leaves** (the bar shrinks
back to the 100% base) and only then does `BASE = BILL × 100/(100+r)` appear.
The GST is one block that **physically halves** into CGST and SGST.

## Realistic diagrams (production direction)

- the bar and the tax layer are **filled, shaded** shapes that merge;
- a drawn **receipt** that grows as the tax joins, plus **filled items** (a pair
  of shoes, a medical-shop receipt) rather than bare outlines;
- the two-lane decision board separates the forward lane (base → tax → bill) from
  the backward lane (bill → base);
- the classic errors each sit on a **wrong_card** whose drawn cross lives in the
  same object, in the card's top half, clear of the lettering, with the ticked
  correction beside it;
- fixed-column answer/recap rows, so A/B/C/D and 1/2/3/4 share one vertical line.

## Scene plan (timings are the delivered cut's own)

| # | in | Scene | Key on-screen text | Focus |
|---|---|---|---|---|
| 0 | 0:00 | The tag says Rs 450, the tax is 6% | BASE PRICE · TAX · FINAL BILL | the three quantities |
| 1 | 0:23 | Tax is a percentage increase | 100% + 6% = 106% · layer attaches | the same increase idea |
| 2 | 0:45 | Sales-tax example | 6% of 450 = Rs 27 → Rs 477 · 106% shortcut | tax, then bill |
| 3 | 1:14 | Reading a VAT-inclusive bill | 354.45 + 17.72 = 372.18 · historical rates | base + VAT = bill |
| 4 | 1:50 | GST has the same structure | 5% of 1000 = 50 → Rs 1050 · 105% | one arithmetic model |
| 5 | 2:22 | Reverse: find the original price | bill Rs 2360 = **118%** → Rs 2000 | never 18% of 2360 |
| 6 | 3:04 | The CGST/SGST split | Rs 360 halves into Rs 180 + Rs 180 | the textbook's worked case |
| 7 | 3:33 | Forward or backward? | base given → add; bill given → `×100/(100+r)` | two lanes |
| 8 | 4:08 | The classic error | 18% of Rs 1180 is wrong; 18% of Rs 1000 is right | crossed and corrected |
| 9 | 4:44 | YOUR TURN — questions read, then the silent clock | four checks | all concepts |
| 10 | 5:38 | The answers | A Rs 840 · B base Rs 1000, tax Rs 180 · C Rs 90 + Rs 90 | all concepts |
| 11 | 6:18 | Recap, then the spoken thank-you card | 100% → (100+r)% → ×100/(100+r) | all concepts |

**Delivered file**

    final_videos/SalesTaxVatAndGstCalculationsStory_captioned.mp4
    640×360, 30 fps, 407.53 s (6 min 48 s), 132 captions, 15.22 MB (15,962,467 B)
    final_videos/SalesTaxVatAndGstCalculationsStory_captioned.srt

The raw render and its ground-truth SRT sit in
`media/videos/sales_tax_vat_and_gst_calculations/360p30/`.

## The production instructions

1. **No overlaps, and proper alignment/positioning.**
   `audit_sync_overlap.py` on the rendered cut → **0 defect flags**; only the
   deliberate **OFF-CENTRE review entries (203)** (the left-hand bar/layer groups
   and the corner question cards). `audit_clearance.py` → **0 tight pairs, 0
   text/line collisions, 0 foreign-box collisions**. `audit_badge_clearance.py`
   → all 33 headings/sub-headings **ok**, tightest `s1.sub`/`s8.sub` at
   **0.89 units** (requirement 0.30); nothing below `CAPTION_SAFE_Y = -2.00`.

2. **The YOUR TURN clock: centred, ten seconds, silent** —
   `play_challenge_countdown(self, seconds=10, position=(BOARD_CX, BOARD_CY))`
   with the four question cards in the four corners; `find_timer.py` locates the
   window at **324 s → 334 s** (mid 329 s).

3. **Realistic diagrams** — see the production direction above.

## Voice sync

Every reveal waits for its bookmark (`self.wait(leftover(tracker, "bN"))` before
the play) and `closing()` consumes each window's tail.

**All twelve pieces at 0.00 s stretch:**

| piece | audio (s) | anim (s) | stretch |
|---|---|---|---|
| title | 22.59 | 22.59 | 0.00 |
| s1 | 20.80 | 20.80 | 0.00 |
| s2 | 27.71 | 27.71 | 0.00 |
| s3 | 34.55 | 34.55 | 0.00 |
| s4 | 31.22 | 31.22 | 0.00 |
| s5 | 38.09 | 38.09 | 0.00 |
| s6 | 28.09 | 28.09 | 0.00 |
| s7 | 33.64 | 33.64 | 0.00 |
| s8 | 34.54 | 34.54 | 0.00 |
| s9q | 42.92 | 25.57 | 0.00 |
| s9a | 39.58 | 39.58 | 0.00 |
| s10 | 29.43 | 29.38 | 0.00 |
| **TOTAL** | **383.16** | **365.76** | **0.00** |

`verify_sync.py`: video 407.523 s, audio 405.483 s, silent tail +2.040 s [ok],
**132 captions**, first 0.14 s, last 405.44 s, 126 speech blocks (332.1 s),
**0 captions in silence, 0 speech blocks (> 1.0 s) uncaptioned** → PASS.
`verify_captions.py`: narration **1151 words = SRT 1151 words** → PASS.

Delivered voice windows: title 0.14–23.73 · s1 23.73–45.45 · s2 45.45–74.21 ·
s3 74.21–110.08 · s4 110.08–142.40 · s5 142.40–184.39 · s6 184.39–213.78 ·
s7 213.78–248.52 · s8 248.52–284.74 · s9q 284.74–338.65 (clock 324–334) ·
s9a 338.65–378.21 · s10 378.21–407.53.

The closing scene is fixed by bookmarks only: the recap rows come on one per
bookmark, the strip on its own bookmark on the sentence that says it, the board
is cleared and the thank-you card revealed only in front of "Thank you for
watching,", and the goodbye lands on its own bookmark before "see you in the next
lesson".

## Pedagogical safeguards honoured

- **Base and bill are visually separate.** The bar is always the 100% base, the
  tax layer is a distinct shaded band, and the bill is the merged result — the
  rate is never applied to the tax-added total (scene 8 shows "18% of Rs 1180"
  struck through against the correct "18% of Rs 1000").
- **Tax is an increase**, so `18% GST = 118% of the base`, written on screen.
- **Never subtract the rate off a tax-inclusive bill** — the reverse lane uses
  `× 100/(100 + r)`, and the 18% portion visibly leaves the bar before the formula
  appears.
- **One arithmetic model for sales tax, VAT and GST** (base + percentage tax =
  bill), stated in scene 3/4.
- **Historical/textbook framing.** The VAT and sales-tax rates carry an on-screen
  "HISTORICAL RATES, NOT TODAY'S TAX ADVICE" chip with matching narration, and
  the CGST/SGST equal split is framed as the textbook's worked case, not a
  universal rule or a memorisation target.
- **Tax adds, discount removes** — kept side by side in scene 7.

## Tools in this folder

`assemble_salestax.py` (splices `_salestax_fragment.py` + `_salestax_beats.py`
into the proven head), `setup_tools.py`, `make_draft_srt.py`, `tts_precheck.py`,
`audit_sync_overlap.py`, `audit_clearance.py`, `audit_badge_clearance.py`,
`scene_frames.py`, `find_timer.py`, and the chapter's `pipeline_360.py`.

**Frame sweep:** `frames360/chk/` holds one still per scene (`01_title` …
`12_s10`) plus the centred THINK clock at mid-countdown.

**Money glyph:** every amount is written **Rs** (the brief's allowed fallback).

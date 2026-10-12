# Production-Ready Storyboard — as built

## Percentage Increases, Decreases & Quick Estimation Rules on Bills

CLASS 8 MATHS · CHAPTER 5 (COMPARING QUANTITIES USING PROPORTION) · STORYMODE 02

**LLM KEY / FUNCTION NAME:** `percentage_applications_and_estimation`
**CHAPTER:** Class 8 · Chapter 5 — Comparing Quantities using Proportion
**TEXTBOOK THREAD:** percentage as the common scale, percentage increase and
decrease, the quick mental percentages (10%, 5%, 15%, 20%) and estimation on a
bill.

## Learning objective

By the end of the video a student can: convert a part/whole comparison into a
percentage and say which quantity is the **whole/reference**; read a percentage
increase as `100% + p%` and a decrease as `100% − p%`; compute an increase or a
decrease from the original; and estimate a bill by rounding and building the
percentage out of 10% (5% = half of 10%, 15% = 10% + 5%, 20% = two 10%s).

**Primary takeaway:**
**compare → change → estimate → check**
`Percentage = part/whole × 100` · increase = `100% + p%` · decrease = `100% − p%`

## Core visual metaphor — one percentage control panel and one 100% bar

A persistent three-mode **control panel** (CONVERT / CHANGE / ESTIMATE) sits on
every teaching scene with the mode in use lit, so the learner always knows which
of the three uses of percentage is on the board. The 100-cell grid bars fill
**cell by cell** (Group A 75, Group B 80), and a persistent 100% original bar
carries a coloured block that **attaches** for an increase (+35%) and a decade
row whose last block **detaches and leaves** for a decrease (−10%).

## Realistic diagrams (production direction)

Everything is drawn as filled, shaded geometry — never a bare outline:

- the **100-cell bars** are real filled cells that light one by one, so 75% and
  80% are literally filled areas;
- the **increase** block physically **attaches** to the 100% bar and the
  **decrease** decade block **detaches and leaves**, so "add" and "take away"
  look different;
- money is a **filled note, a money bag and coin stacks**; the shop scene has a
  **price tag**, and the bill scene a **receipt** with a **number line** the bill
  snaps along (477.80 → 480);
- the **10% block splits in half** into two 5% blocks on screen;
- a mistake is shown on a `wrong_card` whose **drawn cross** lives in the same
  VGroup, in the card's top half, clear of the lettering;
- answer/recap rows sit in **fixed columns**, so A/B/C/D and 1/2/3/4 share one
  vertical line.

## Scene plan (timings are the delivered cut's own)

| # | in | Scene | Key on-screen text | Focus |
|---|---|---|---|---|
| 0 | 0:00 | Why one scale? Group A 225/300, Group B 200/250 | WHO DID BETTER? | the need for % |
| 1 | 0:27 | Convert to a common scale | 225 : 300 = 3 : 4 · 200 : 250 = 4 : 5 → 75% / 80% | part/whole × 100 |
| 2 | 1:05 | A 35% increase | 100% + 35% = 135% · the block ATTACHES | increase = the original + the increase |
| 3 | 1:36 | Apply it to sales | 35/100 × 98,700 = Rs 34,545 → Rs 1,33,245 · 135% shortcut | the two routes agree |
| 4 | 2:16 | A 10% decrease | 10% of 550 = Rs 55 → Rs 495 · the block LEAVES | decrease = 100% − p% |
| 5 | 2:46 | The mental toolkit | 10% = 48, 5% = 24, 15% = 72 (on 480) | build from 10% |
| 6 | 3:19 | Estimation on a bill | Rs 477.80 → Rs 480 → 10% 48, 5% 24, 15% 72 → about Rs 410 | round, then build |
| 7 | 3:50 | Exact vs estimate | 15% of 477.80 vs the rounded route | estimate = reasonableness check |
| 8 | 4:27 | The decision map | CONVERT · CHANGE · ESTIMATE | the four rules |
| 9 | 4:50 | YOUR TURN — questions read, then the silent clock | four checks | all concepts |
| 10 | 5:31 | The four answers | A 75% · B Rs 720 · C about Rs 72 | all concepts |
| 11 | 6:03 | Recap, then the spoken thank-you card | COMPARE · CHANGE · ESTIMATE · CHECK | all concepts |

**Delivered file**

    final_videos/PercentageApplicationsAndEstimationStory_captioned.mp4
    640×360, 30 fps, 394.93 s (6 min 35 s), 101 captions, 14.71 MB (15,427,840 B)
    final_videos/PercentageApplicationsAndEstimationStory_captioned.srt

The raw render and its ground-truth SRT sit in
`media/videos/percentage_applications_and_estimation/360p30/`.

## The production instructions

1. **No overlaps, and proper alignment/positioning.**
   `audit_sync_overlap.py` against the rendered audio → **0 defect flags**: no
   text-in-text, partial, text-on-arrow, text-on-side, text-outside-box,
   out-of-board, in-caption-band, near-badge, empty-text or LaTeX-as-text. The
   only lines it prints are the deliberate **OFF-CENTRE review entries (227)** —
   the side-by-side cards, the left-hand bars and the four corner question cards
   that the narration needs off the centre line.
   `audit_clearance.py` → **0 pairs closer than 0.22, 0 text/line collisions, 0
   foreign-box collisions**.
   `audit_badge_clearance.py` → all 33 headings/sub-headings/banners **ok**; the
   tightest is `s4.sub` at **0.66 units** (requirement 0.30).
   Nothing on the board reaches `CAPTION_SAFE_Y = -2.00`.

2. **The YOUR TURN clock: centred on the board, ten seconds, and silent.**
   `story_common.play_challenge_countdown(self, seconds=10, position=(BOARD_CX,
   BOARD_CY))` with the four question cards in the four corners.
   `find_timer.py` locates the darkened window at **320 s → 330 s** (mid 325 s)
   inside a 394.93 s cut.

3. **Realistic diagrams** — see the production direction above.

## Voice sync

Every reveal waits for the narration bookmark that ends the phrase describing it
and only then plays (`self.wait(leftover(tracker, "bN"))` *before* the play), so
the board can never run ahead of the voice; `closing()` consumes each window's
tail.

`audit_sync_overlap.py` against the rendered audio: **all twelve pieces at
0.00 s stretch** —

| piece | audio (s) | anim (s) | stretch |
|---|---|---|---|
| title | 26.25 | 26.25 | 0.00 |
| s1 | 37.20 | 37.20 | 0.00 |
| s2 | 29.65 | 29.65 | 0.00 |
| s3 | 39.44 | 39.44 | 0.00 |
| s4 | 28.32 | 28.32 | 0.00 |
| s5 | 32.07 | 32.07 | 0.00 |
| s6 | 29.78 | 29.78 | 0.00 |
| s7 | 36.79 | 36.79 | 0.00 |
| s8 | 22.03 | 22.03 | 0.00 |
| s9q | 28.77 | 19.20 | 0.00 |
| s9a | 31.53 | 31.53 | 0.00 |
| s10 | 28.96 | 28.90 | 0.00 |
| **TOTAL** | **370.79** | **361.16** | **0.00** |

`verify_sync.py`: video 394.915 s, audio 392.939 s, silent tail +1.976 s [ok],
**101 captions**, first 0.14 s, last 392.90 s, 129 speech blocks (321.6 s of
speech), **0 captions in silence, 0 speech blocks (> 1.0 s) uncaptioned** →
PASS.
`verify_captions.py`: narration **900 words = SRT 900 words** → PASS (word for
word).

Delivered voice windows (`scene_frames.py`, one hold frame per scene):
title 0.14–27.33 · s1 27.33–65.63 · s2 65.63–96.23 · s3 96.23–136.78 ·
s4 136.78–166.15 · s5 166.15–199.14 · s6 199.14–230.06 · s7 230.06–267.83 ·
s8 267.83–290.96 · s9q 290.96–331.17 (questions read, then the clock) ·
s9a 331.17–363.71 · s10 363.71–394.93.

The closing scene is fixed by bookmarks only: recap rows one per bookmark, the
closing strip on its own bookmark on the sentence that says it, the board
cleared and the thank-you card revealed only on the bookmark in front of "Thank
you for watching,", and the goodbye line on its own bookmark before "see you in
the next lesson" (`closing(run_time = 0.90)`), then a 1.98 s hold on the card.

## Pedagogical safeguards honoured

- **A percentage always has a stated base.** Scene 1 names the whole (300 and
  250) before it converts, and the narration insists on saying which quantity is
  the reference.
- **Change is measured from the original.** Scene 2 builds 100% → 135% on the
  original bar, and scene 4 takes 10% off the original price (Rs 550), so
  "35% increase = 135% of the original" and "10% decrease = 90%" are shown, not
  asserted.
- **Increase and decrease look different.** The +35% block visibly **attaches**
  to the 100% bar; the −10% decade block visibly **detaches and leaves**.
- **Estimation is not exact arithmetic.** Scene 7 keeps the approximation sign
  and the word "about" on screen, presents the exact lane only as a comparison,
  and explains why "about Rs 410" is sensible.
- **Rounding is chosen to make the number easier** (477.80 → 480; 357.30 → 360),
  and hard percentages are built from 10% (5% = half of 10%, 15% = 10% + 5%,
  20% = two 10%s).
- **No successive discounts** anywhere in the video or the narration.

## Tools in this folder

`assemble_percentage.py` (splices `_percentage_fragment.py` +
`_percentage_beats.py` into the proven head), `setup_tools.py`,
`make_draft_srt.py`, `tts_precheck.py`, `audit_sync_overlap.py`,
`audit_clearance.py`, `audit_badge_clearance.py`, `scene_frames.py`,
`find_timer.py`, and the chapter's `pipeline_360.py`
(render → verify_sync → verify_captions → burn captions → `final_videos/`).

**Frame sweep:** `frames360/chk/` holds one still per scene (`01_title` …
`12_s10`), the centred THINK clock at mid-countdown (`zz_timer_mid.png`) and the
closing card (`zz_close_card.png`).

**Money glyph:** every amount is written **Rs** (the fallback the brief allows),
so no frame can show a missing-glyph box.

**Note on this topic's paths:** this media path is at the old 260-character
MAX_PATH limit, so the module's `_write_real_srt`, `make_draft_srt.py`, the
generated `audit_sync_overlap.py`/`scene_frames.py` readers and the chapter's
`pipeline_360.py` copies all go through the `\\?\` extended-length form. The
verifiers (`verify_sync.py`, `verify_captions.py`) were given the same
`read_text_long()` fallback, and both PASS on this cut.

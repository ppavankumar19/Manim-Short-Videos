# Production-Ready Storyboard — as built

## Compound Ratio & Inverse Ratio: Applications in Business Profit Sharing

CLASS 8 MATHS · CHAPTER 5 (COMPARING QUANTITIES USING PROPORTION) · STORYMODE 01

**LLM KEY / FUNCTION NAME:** `compound_ratio_and_business_proportions`
**CHAPTER:** Class 8 · Chapter 5 — Comparing Quantities using Proportion
**TEXTBOOK THREAD:** inverse ratio, the compound ratio of two ratios, and the way
a partnership profit is shared — the chapter's own business application of
proportion.

## Learning objective

By the end of the video a student can: say what an inverse (reciprocal) ratio is
and swap the terms of a ratio; state the compound-ratio rule `a:b` and `c:d`
give `ac:bd`; explain why the wrong `(a+c):(b+d)` is not a compound ratio; decide
which ratio settles a partnership profit (same time → capital ratio, same
capital → time ratio, both different → compound ratio); and divide a given
profit into the partners' shares in that ratio.

**Primary takeaway:**
**inverse = swap the terms** · **compound = multiply corresponding terms** ·
**a partner's share follows capital × time**

## Core visual metaphor — two partners and one profit bag

Ramayya's card (Rs 2,000 · 12 months) and Gopalam's card (Rs 3,000 · 9 months)
persist on the board, with the profit bag between them. The video then walks the
learner through the reasoning: the ordered ratio and its inverse, the two "one
factor cancels" cases, the case where both the money and the time differ, the
compound-ratio machine the two ratio cards slide into, the money × time
cross-check, and finally the profit split into seventeen equal blocks which
physically move to the two partners.

## Realistic diagrams (production direction)

Everything is drawn as filled, shaded geometry — never a bare outline:

- the partners are **named cards with a filled figure** (a round head over a
  pair of shoulders) in the card's left margin;
- the profit is a **money bag with a tied neck** plus two **coin stacks** (filled
  discs with thickness);
- ratios live in **cards** (`ratio_card`) which are the objects that slide into
  the machine and *turn over* (`Rotate(swap, PI, axis=UP)`) to become the
  inverse;
- the rule is a **compound-ratio machine**: a filled box with its own heading and
  its output formula, with the two ratio cards **sliding in** from the left and a
  drawn **funnel** marking the entry;
- the profit is **seventeen equal solid blocks** — eight green and nine pink —
  which **physically move** (`block.animate.move_to`) into two clusters under
  the partners' share cards;
- mistakes are marked with a **drawn cross** (`wrong_card`: the cross fills the
  card's top half and the wrong wording sits under it, so a stroke never touches
  lettering);
- every card is a **single board object**, so a row is one centred mobject.

## Scene plan (timings are the delivered cut's own)

| # | in | Scene | Key on-screen text | Focus |
|---|---|---|---|---|
| 0 | 0:00 | Title card: two partners, one profit | SHOULD THEY SHARE IT EQUALLY? | the question |
| 1 | 0:22 | A ratio is an ordered comparison | 3 : 2 ≠ 2 : 3 · INVERSE | inverse ratio |
| 2 | 0:47 | Same time for both partners | SAME TIME · TIME CANCELS · 2000 : 3000 = 2 : 3 | the time cancels |
| 3 | 1:13 | Same capital, different time | SAME CAPITAL · CAPITAL CANCELS · 12 : 9 = 4 : 3 | the capital cancels |
| 4 | 1:38 | Both capital and time differ | CAPITAL 2 : 3 · COMBINE BOTH · TIME 4 : 3 | both must combine |
| 5 | 2:00 | The compound ratio rule | COMPOUND RATIO MACHINE · (a+c):(b+d) crossed out | ac : bd |
| 6 | 2:26 | Applying the compound ratio | 2 : 3 × 4 : 3 → 8 : 9 · Rs 2000 × 12 · Rs 3000 × 9 | apply + cross-check |
| 7 | 2:57 | From ratio to rupees | 17 equal parts of Rs 1,000 → Rs 8,000 + Rs 9,000 | the shares |
| 8 | 3:31 | Which ratio decides the share? | SAME TIME / SAME CAPITAL / BOTH DIFFERENT | the decision map |
| 9 | 3:51 | YOUR TURN — questions read, then the silent clock | four checks | all concepts |
| 10 | 4:31 | The four answers | A 5 : 7 · B 1 : 2 · C 15 : 16 · D 1 : 1 | all concepts |
| 11 | 5:03 | Recap, then the spoken thank-you card | INVERSE · COMPOUND · PARTNERSHIP | all concepts |

**Delivered file**

    final_videos/CompoundRatioAndBusinessProportionsStory_captioned.mp4
    640×360, 30 fps, 331.65 s (5 min 32 s), 101 captions, 13.06 MB (13,695,362 B)
    final_videos/CompoundRatioAndBusinessProportionsStory_captioned.srt

The raw render and its ground-truth SRT sit in
`media/videos/compound_ratio_and_business_proportions/360p30/`.

## The production instructions

1. **No overlaps, and proper alignment/positioning.**
   `audit_sync_overlap.py` against the rendered audio → **0 defect flags**: no
   text-in-text, partial, text-on-arrow, text-on-side, text-outside-box,
   out-of-board, in-caption-band, near-badge, empty-text or LaTeX-as-text. The
   only lines it prints are the deliberate **OFF-CENTRE review entries** (174):
   the rows of two partner cards / several chips that must sit side by side, the
   same structural entries every topic in this series reports.
   `audit_clearance.py` → **0 pairs closer than 0.22, 0 text/line collisions, 0
   foreign-box collisions**.
   `audit_badge_clearance.py` → every heading, sub-heading and banner clears
   both corner badges; the tightest is `s6.sub` at **0.57 units** (requirement
   0.30).
   The rows are centred on `BOARD_CX = 0.50`; cards space their own lines by 0.28
   units (the clearance rule is 0.22); the cross-of-the-mistake lives in the same
   object as the card it strikes; nothing on the board reaches
   `CAPTION_SAFE_Y = -2.00`.

2. **The YOUR TURN clock: centred on the board, ten seconds, and silent.**
   `story_common.play_challenge_countdown(self, seconds=10, position=(BOARD_CX,
   BOARD_CY))` — the series' shared badge, dead centre of the green board, with
   the four question cards in the four corners. `find_timer.py` locates the
   darkened window at **259 s → 269 s** (mid 264 s) inside a 331.65 s cut.

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
| title | 20.86 | 20.86 | 0.00 |
| s1 | 24.50 | 24.50 | 0.00 |
| s2 | 24.65 | 24.65 | 0.00 |
| s3 | 24.29 | 24.29 | 0.00 |
| s4 | 20.93 | 20.93 | 0.00 |
| s5 | 24.79 | 24.79 | 0.00 |
| s6 | 30.32 | 30.32 | 0.00 |
| s7 | 32.78 | 32.78 | 0.00 |
| s8 | 19.60 | 19.60 | 0.00 |
| s9q | 26.83 | 17.07 | 0.00 |
| s9a | 29.95 | 29.95 | 0.00 |
| s10 | 28.61 | 27.64 | 0.00 |
| **TOTAL** | **308.11** | **297.38** | **0.00** |

`verify_sync.py`: video 331.652 s, audio 329.707 s, silent tail +1.945 s [ok],
**101 captions**, first 0.18 s, last 329.68 s, 102 speech blocks (268.7 s of
speech), caption time 312.5 s, **0 captions in silence, 0 speech blocks
(> 1.0 s) uncaptioned** → PASS.
`verify_captions.py`: narration **900 words = SRT 900 words** → PASS (word for
word).

Delivered voice windows (`scene_frames.py`, one hold frame per scene):
title 0.18–22.03 · s1 22.03–47.51 · s2 47.51–73.12 · s3 73.12–98.35 ·
s4 98.35–120.35 · s5 120.35–146.21 · s6 146.21–177.46 · s7 177.46–211.28 ·
s8 211.28–231.74 · s9q 231.74–271.20 (questions read, then the clock) ·
s9a 271.20–303.35 · s10 303.35–331.65.

The closing scene is fixed by bookmarks only: **b0–b3** reveal recap rows 1–4,
**b4** reveals the closing strip on the sentence that says it ("Money and time
together decide the share."), **b5** — the bookmark in front of "Thank you for
watching," — clears the board and brings in the thank-you card, and **b6** lands
"See you in the next lesson :)" with the spoken goodbye (`closing(run_time =
0.90)`), then the cut holds the card for 1.95 s.

## Pedagogical safeguards honoured

- **A ratio is ordered.** Scene 1 writes `3 : 2 ≠ 2 : 3` before it says what the
  inverse is, and the inverse is always *swapping the terms* — never adding or
  negating: "Inverse means swap the two terms, never add them."
- **The compound ratio multiplies.** Scene 5 states the rule, shows the machine's
  `a:b × c:d → ac:bd`, and then shows the wrong `(a + c) : (b + d)` struck through
  with a drawn cross — the screen says a compound ratio "multiplies corresponding
  terms; it never adds them".
- **Profit is not always shared by capital alone.** Scenes 2, 3 and 4 take the
  three cases in order (same time → capital ratio; same capital → time ratio;
  both different → combine), and only then is the compound ratio used.
- **Money × time is shown before 8 : 9.** Scene 6 computes Rs 2000 × 12 =
  Rs 24,000 and Rs 3000 × 9 = Rs 27,000 and simplifies `24,000 : 27,000` to
  `8 : 9` — the compound ratio is never asserted without the cross-check.
- **Ratios stay separate from rupee amounts.** Ratio chips are written as `8 : 9`
  and the money chips always carry `Rs`.
- **Model-created numbers are marked as examples.** Scene 7 labels the total
  "PROFIT (EXAMPLE) = Rs 17,000", and the narration says "This total is an
  example, not a textbook figure."; the challenge's Rs 4,000/Rs 3,000 pair is a
  question, not a claim about the textbook.

## Tools in this folder

`assemble_compound_ratio.py` (splices `_compound_ratio_fragment.py` +
`_compound_ratio_beats.py` into the proven head), `setup_tools.py`,
`make_draft_srt.py`, `tts_precheck.py`, `audit_sync_overlap.py`,
`audit_clearance.py`, `audit_badge_clearance.py`, `scene_frames.py`,
`find_timer.py`, and the chapter's `pipeline_360.py`
(render → verify_sync → verify_captions → burn captions → `final_videos/`, with
the `\\?\` extended-path copy for these long topic paths).

**Frame sweep:** `frames360/chk/` holds one still per scene (`01_title` …
`12_s10`) plus `zz_timer_mid.png` (the centred THINK clock at mid-countdown).
The delivered cut was rendered with the TTS cache warmed first
(`warm_tts_cache.py <topic> <module>`), so the render ran entirely from cache.

**Money glyph:** every amount uses the word **Rs** — the fallback the brief
allows if the rupee sign does not render cleanly in the board font (Segoe
Print has no guaranteed rupee glyph, and the whole series writes `Rs`), so no
frame can ever show a missing-glyph box.

**Closing-transition check (read on the rendered cut):** at 5:24.5 s the four
recap rows *and* the closing strip are still on the board while the burned
caption reads "Money and time together decide the share. Thank you" — the frame
never runs ahead of the voice — and at 5:27 s the board is cleared with the
thank-you card up and the goodbye line under it ("for watching, and see you in
the next lesson.").

# Production-Ready Storyboard

## Advanced Divisibility Tests: How to Instantly Test Divisibility by 4, 8, and 11

CLASS 6 MATHEMATICS · CHAPTER 3 · STORYMODE 02

**LLM KEY / FUNCTION NAME:** `divisibility_rules_advanced_4_8_11`
**DIRECT TOPIC:** Advanced Divisibility Rules for 4, 8, and 11
**CHAPTER:** Chapter 3 — Playing with Numbers
**TARGET CLASS LEVEL:** Class 6
**TEXTBOOK:** Telangana SCERT, Class 6 Mathematics (English Medium), 2025–26,
Chapter 3 — Playing with Numbers. The chapter develops these rules after
revising divisibility by 2, 3, 5, 6, 9 and 10, and uses the examples
**56496** (for 4), **93624** (for 8) and **6535**, **1221** (for 11).

---

## Learning Objective

By the end of the video, students should be able to:

- Test divisibility by **4** using the last two digits.
- Explain *why* the last two digits are enough (100 and its multiples divide by 4).
- Test divisibility by **8** using the last three digits (1000 and its multiples).
- Identify the alternating digit positions **from the right** for divisibility by 11.
- Compare the two alternating sums and accept a difference of 0 **or a multiple of 11**.
- Decide divisibility quickly, without dividing the whole number.
- Recognise the three tests in real situations: leap years, tiling a wall,
  checking an account number, and packing seats into boxes of four.

**Primary takeaway:** **4 → last 2 digits · 8 → last 3 digits · 11 → alternating sums.**

## Core Visual Metaphor — "Zoom Into the Important Digits"

The scanner from the previous video gains three modes:

| divisor | what the scanner does |
|---|---|
| 4 | a **two-digit lens** at the end of the number; the leading digits dim |
| 8 | a **three-digit lens**; the leading digits dim |
| 11 | an **alternating-position sorter**: digits drop into odd/even baskets, the two sums are compared |

## Core Mathematical Rules

| Divisor | Textbook test | Worked example |
|---|---|---|
| 4 | Check the number formed by the last two digits | 56496 → 96 = 4 × 24 |
| 8 | For four or more digits, check the last three digits | 93624 → 624 = 8 × 78 |
| 11 | Difference between the sums of alternating positions (from the right) must be 0 or a multiple of 11 | 1221 → (1+2) − (2+1) = 0; 6535 → 10 − 9 = 1 → no |

## Scene Plan

| Scene | Learning goal | Visual | Key on-screen text | Maths |
|---|---|---|---|---|
| Hook (cold open) | Give a reason to care *before* the title | Three real-world rows, each with its divisor badge | Why These Tests? | leap year → 4, tiling → 8, account numbers → 11 |
| 1 | Introduce the advanced tests | The six known rules, then 4, 8, 11 arrive | New Numbers, New Patterns | 2,3,5,6,9,10 → 4,8,11 |
| 2 | Derive the rule for 4 | 76532 split into 76500 + 32; the front block fades | Why 4 Needs Only Two Digits | 100 = 4 × 25, 32 = 4 × 8 |
| 3 | Apply the rule for 4 | The lens closes on 96; leading digits dim | Last 2 Digits | 56496 → 96 = 4 × 24 |
| 4 | Derive the rule for 8 | 100 fails, 1000 works; 93624 = 93000 + 624 | Why 8 Needs Three Digits | 1000 = 8 × 125, 624 = 8 × 78 |
| 5 | Keep 4 and 8 apart | One number, two lenses | Don't Mix the Two | 2104: 04 and 104 |
| 6 | Explain the rule for 11 | 1221 digits tagged odd/even from the right, into two baskets | Divisibility by 11 | (1+2) − (2+1) = 0 |
| 7 | Show the test failing | 6535 into the same baskets | When the Test Fails | 10 − 9 = 1 |
| 8 | Organise all three | Three panels, one clue each | Three Advanced Rules, Three Clues | 4 / 8 / 11 summary |
| 9 | Let the rule do real work | 56496 seats, four-seat boxes, the lens on 96, a drawn tick | Real Seats, Real Boxes | 96 ÷ 4 = 24, nothing left over |
| 10 | Student challenge, staged | 726352 with the 4 and 8 checks on the left, cleared away, then 10824 checked by 11 centred in larger type, with the THINK clock | YOUR TURN | 52, 352, and 13 − 2 = 11 |
| 11 | Final recap | Three rules and the quick examples | ZOOM. ZOOM MORE. ALTERNATE. | 96÷4, 624÷8, 1221→0 |

## Key Pedagogical Safeguards

1. **Explain why 4 uses two digits.** Scene 2 physically separates
   76532 = 76500 + 32 and shows 100 = 4 × 25, so the leading block is already
   divisible by 4 — the rule is derived, not asserted.
2. **Explain why 8 uses three digits.** Scene 4 does the same with 1000 = 8 × 125
   and 93624 = 93000 + 624.
3. **Preserve the textbook's scope.** The on-screen note keeps the source's
   framing for 4 (*"works for numbers greater than 100"*); the narration says the
   test is for larger numbers.
4. **Count positions from the right.** Scene 6 shows a "start from the right"
   arrow before the digits are tagged odd/even.
5. **Difference 0 *or a multiple of 11*.** Scene 7 shows a difference of 1
   failing, and the rule card reads "0 or a multiple of 11".
6. **Subtract the smaller from the larger** so Class 6 students never meet a
   negative difference (10 − 9, 13 − 2, 3 − 3).

---

# Final Production Check

**Module:** `divisibility_rules_advanced_4_8_11.py`
(`DivisibilityRulesAdvancedStory`), assembled by `assemble_advanced.py` from the
series' proven video-03 head (theme, chalkboard backdrop with the student, the
teacher and both corner badges, `reset_board`, `appear`, the card helpers, the
ground-truth SRT export) plus this topic's fragment (`_advanced_fragment.py`:
board layout, the lens/basket furniture, the narration) and beats
(`_advanced_beats.py`).

**Delivered files** (the same performance, cut at two resolutions):

The 360p cut:

    final_videos/DivisibilityRulesAdvancedStory_captioned.mp4
    640×360, 30 fps, 227.73 s (3 min 48 s), 10.4 MB, 61 captions
    final_videos/DivisibilityRulesAdvancedStory_captioned.srt

The 1080p60 master, re-rendered from the same module (no re-timing, so the
audio, the reveal timing and the SRT are the same performance):

    final_videos/1080p/DivisibilityRulesAdvancedStory_captioned.mp4
    1920×1080, 60 fps, 227.68 s, 13 661 frames, 43.1 MB, 61 captions
    final_videos/1080p/DivisibilityRulesAdvancedStory_captioned.srt

    verify_sync.py      video 227.683 s, 61 captions, first 0.24 s, last
                        225.68 s, 0 in silence, 0 uncaptioned  -> PASS
    verify_captions.py  narration 527 words = SRT 527 words       -> PASS

`pipeline_1080.py` in this chapter folder produced the master
(render 1920×1080/60 → verify → burn → `final_videos/1080p/`); libass scales the
one caption style with the video height, so the 1080p burn is the 360p burn
three times the size and the banner clearance is identical.

The raw renders and their ground-truth SRTs also sit in
`media/videos/divisibility_rules_advanced_4_8_11/360p30/` and `…/1080p60/`.

**Voice sync** (`audit_sync_overlap.py`): **every one of the 13 narration pieces
matches its audio to 0.00 s** — no stretch anywhere; total speech 225.6 s. Each
reveal waits for the bookmark that ends the phrase describing it and only then
plays (`self.wait(leftover(tracker, "bN"))` *before* the `FadeIn`), so the board
never runs ahead of the voice.

**Real captions** (`verify_sync.py`): 61 captions, first at 0.24 s, last at
225.51 s of a 227.72 s video, **0 captions in silence**, **0 speech blocks
uncaptioned** → **PASS**. `verify_captions.py`: narration 527 words = SRT 527
words → **PASS (word for word)**.

**Layout audits** (run on a synthetic draft SRT before the render, then again
against the real one):

- `audit_sync_overlap.py` → **0** out-of-board, text-in-text, text-on-line,
  text-outside-box, near-badge, LaTeX-as-text, empty-TeX and **IN-CAPTION-BAND**
  flags (nothing sits below y = −2.00, the caption's reach). The 75 `OFF-CENTRE`
  notes are the deliberate two-column layouts (the 11 baskets, the three
  dashboard panels, the left-hand 726352 column) and are down from 94 before the
  challenge was staged.
- `audit_clearance.py` → **0** text/line collisions, **0** foreign-box
  collisions and **0** `GLYPH-AS-TEXT` hits; the 9 pairs under 0.22 units are
  the designed stacks inside single panels (the odd/even place tags, the
  dashboard panel lines) — the same list as before, one pair shorter.

## Production-audit round 2 (all five notes closed)

| Audit note | What was done |
|---|---|
| The video "opens abruptly with *three more divisibility tests*": add a real-world/historical hook (~10 s) | New cold-open scene **Why These Tests?** — a leap year every four years, a tiler checking eight tiles, a bank reading eleven on account numbers — runs before the title card (12.3 s) |
| Add a 10–15 s real-world application before *Your Turn* | New scene **Real Seats, Real Boxes** (12.2 s): the textbook's 56496 seats into four-seat boxes, 96 ÷ 4 = 24, a drawn tick and "no seat is left over" |
| The bottom banners sit in the subtitle collision zone (00:03, 00:57, 01:33) | The closing strip was lifted **0.15 units** (≈15 % of the banner band plus its row) from `STRIP_Y = -1.95` to **-1.80**; the promise/answer rows went to −1.20/−1.18, the ÷4 rule card to −1.14, the ÷11 result boxes to −1.16 with a tighter frame, and scene 2's last division and its verdict now share **one** row instead of two. The caption band was re-measured on this video's own burned cut (one line starts at y = −3.38, a wrapped two-line cue at −2.93), and `CAPTION_SAFE_Y` is now the stricter **-2.00** — the lowest ink on the board is the strip baseline at −1.93 |
| The *Your Turn* slide is too cramped (two six-digit numbers, five checks, two verdicts at once) | The challenge is **staged sequentially**: 726352 with the 4 and 8 checks on the left and the centred THINK clock, then the whole group fades out, then 10824 moves to the **centre in larger type** (32 pt tiles, 20 pt sums, a 30 pt difference) with its boxed verdict |
| Check the voice/audio/SRT sync | Every beat is wait-then-reveal; the sync audit reports 0.00 s stretch on all 13 pieces and the caption verifiers pass word-for-word (527 = 527) |

**Three real defects were caught and fixed before delivery:**

1. the leading digits in scene 3 were faded by drawing a translucent *copy* over
   them, which doubles every glyph (the audit reported text-in-text) — they are
   now faded in place;
2. the ÷11 panel title touched its panel border (text-on-side, gap 0.02) — the
   panel headings are a size smaller;
3. the tick glyphs in the 11-test strip, the dashboard panels, the challenge
   lines and the recap examples rendered as **empty boxes**, because Segoe Print
   has no ✓/✗ glyph — every tick is now a drawn stroke (`mark_yes`/`mark_no`),
   and `audit_clearance.py` gained a `GLYPH-AS-TEXT` check so a literal tick,
   cross or ballot box can never reach the board again.

**TTS pre-check** (`tts_precheck.py`): all thirteen pieces generated audio with
word boundaries — including the two new scenes and the rewritten challenge (33,
36 and 66 boundaries). The check earned its keep earlier in the build: the
service rejected two sentences in scene 4 (`KeyError: 'content'`), which were
rewritten and re-verified before the render.

**Timer:** the THINK clock is centred on the board
(`story_common.play_challenge_countdown`, `position=(BOARD_CX, BOARD_CY)`) for
the four-second pause in the challenge; `find_timer.py` locates the countdown
window at 185–189 s, i.e. inside the challenge beat.

**Frame sweep:** the cold open, the title, all eleven scenes and the closing card
inspected as stills in `frames360/01_hook.png` … `13_scene10.png`, plus the
staged-challenge and countdown stills in `frames360/chk/` and the 1080p master
stills in `frames1080/`.

**Tools in this folder:** `assemble_advanced.py`, `setup_tools.py`,
`make_draft_srt.py`, `tts_precheck.py`, `audit_sync_overlap.py`,
`audit_clearance.py`, `scene_frames.py`, `find_timer.py`, and the chapter's
`pipeline_360.py` (render → verify → burn → `final_videos/`) and
`pipeline_1080.py` (render → verify → burn → `final_videos/1080p/`).

# Production-Ready Storyboard — as built

## Product & Quotient Laws of Exponents: Multiplying and Dividing Powers with the Same Base

CLASS 8 MATHEMATICS · CHAPTER 4 (EXPONENTS AND POWERS) · STORYMODE 03

**LLM KEY / FUNCTION NAME:** `laws_of_exponents_product_and_quotient`
**CLASS LEVEL:** Class 8 · **TEXTBOOK:** Telangana SCERT, 8 Maths EM 2025-26,
Chapter 4, Section 4.2. The section recalls `a^m × a^n = a^(m+n)`, asks whether it
survives negative exponents (verified with `3^2 × 3^-4 = 3^-2`), concludes it holds
for integer exponents on a non-zero base, and then gives the quotient law
`a^m / a^n = a^(m-n)`.

## Learning objective

Spot when two powers share a base; know *why* multiplication adds the exponents
and division subtracts them; apply both laws with positive, zero and negative
exponents; simplify to a single power; and avoid the classic errors (multiplying
the exponents, adding across different bases, reversing the subtraction).

**Primary takeaway:** **same base? keep the base** — × adds, ÷ subtracts.

## The defining visual — factor blocks

Every copy of the base is one identical tile, and the *same tiles* are carried
through each scene (no clear-and-redraw):

- **product:** the two groups physically slide together into one chain — the four
  cyan tiles and three pink tiles become the single chain of seven, and the
  counters above change from "4 factors / 3 factors" to `4 + 3 = 7` → **JOIN → ADD**;
- **quotient:** seven tiles over the fraction bar, three below, the matched pairs
  slashed and removed — the four survivors then slide into one chain beside
  `7 - 3 = 4` → **CANCEL → SUBTRACT**.

## Scene plan (timings are the delivered cut's own)

| # | in | Scene | On-screen text | Maths |
|---|---|---|---|---|
| 0 | 0:00 | Title card | Product & Quotient Laws | `a^m × a^n = a^(m+n)`, `a^m/a^n = a^(m-n)` |
| 1 | 0:11 | There Must Be a Faster Way | There must be a shortcut | `2^4 × 2^3` → seven 2s → `2^7` |
| 2 | 0:29 | Multiplication Joins Factors | KEEP THE BASE — ADD THE EXPONENTS | tiles join: `2^(4+3) = 2^7`, the law card |
| 3 | 0:53 | Keep the Base, Add the Exponents | The law holds for integer exponents | `3^2 × 3^-4`, `2 + (-4) = -2`, `3^-2 = 1/3^2 = 1/9` |
| 4 | 1:14 | Division Cancels Matching Factors | DIVISION CANCELS MATCHING FACTORS | `a^7/a^3`: three pairs cancel, `7 - 3 = 4` |
| 5 | 1:40 | Top Exponent Minus Bottom Exponent | Numerator exponent minus denominator exponent | `4^7/4^4 = 4^(7-4) = 4^3 = 64` |
| 6 | 1:58 | A Negative Answer Is Fine | A negative exponent is a valid answer | `5^2/5^5 = 5^-3 = 1/5^3 = 1/125` |
| 7 | 2:21 | Same Base Is the Key | SAME BASE | PRODUCT: join → add · QUOTIENT: cancel → subtract |
| 8 | 2:50 | Three Mistakes to Avoid | Read the operation carefully | `x^-3x^-2 = x^-5` (not `x^-6`), `2^3·3^4`, `a^2/a^5 = a^-3` |
| 9 | 3:17 | YOUR TURN — questions read, then the silent clock | KEEP THE BASE → ADD OR SUBTRACT | `2^-3·2^-2`, `7^-2·7^5`, `4^7/4^4` |
| 10 | 4:02 | Recap, then the spoken thank-you card | JOIN → ADD · CANCEL → SUBTRACT | both laws, `a ≠ 0` |

**Delivered files**

    final_videos/ProductQuotientLawsStory_captioned.mp4
    640×360, 30 fps, 265.49 s (4 min 25 s), 10.3 MB, 76 captions
    final_videos/ProductQuotientLawsStory_captioned.srt
    final_videos/1080p/ProductQuotientLawsStory_captioned.mp4
    1920×1080, 60 fps, master with the same burned captions
    final_videos/1080p/ProductQuotientLawsStory_captioned.srt

The raw render and its ground-truth SRT also sit in
`media/videos/laws_of_exponents_product_and_quotient/360p30/` (and the 1080p60 raw
cut in the sibling `1080p60/`).

*The brief estimated ~3 min 40 s; the cut runs 4 min 25 s because the storyboard's
own content is large — the title card plus ten scenes, the three error cases of scene 8
and three challenge questions with the series' ten-second thinking clock. No
scene was padded and none was dropped.*

## The production checks

**No overlaps, proper alignment/positioning.** `audit_sync_overlap.py` → **0**
out-of-board, text-in-text, text-on-line, text-on-a-figure-side, text-inside-a-
foreign-card, near-badge, LaTeX-as-text, empty-TeX and **IN-CAPTION-BAND** flags.
`audit_clearance.py` → **0 pairs closer than 0.22 units, 0 text/line collisions,
0 foreign-box collisions, 0 glyph-as-text hits**. The 79 `OFF-CENTRE` notes are
the deliberate diagram geometry (the tile chains, the two law panels, the
challenge cards waiting on the left); every heading, banner, strip, card and
answer row is centred on the board.

Two real defects were caught by the draft pass and fixed before rendering:

1. the cancellation slashes ran **through the tile glyphs** (the audit reported
   text-on-line at gap 0.00) — the matched factors now fade label-first, so each
   slash crosses an empty block;
2. the `4^7/4^4` question card was too short for a fraction, which came within
   0.01 of the card edge — that card is now taller with its own head/body
   offsets.

**The YOUR TURN clock: centred on the board, ten seconds, and silent.**
`story_common.play_challenge_countdown(self, seconds=10, position=(BOARD_CX,
BOARD_CY))`. `find_timer.py` locates the countdown window at **214–224 s**, and
`frames360/chk2/t219.png` shows it dead centre with the three question cards on
the left, none covered. The challenge runs as three movements — questions read
first (3:17.0–3:33.7), then the clock with **no narration under it**, then the
answers (3:45.4 onward): the caption gap between the last question (3:33.63) and
the first answer (3:45.43) is 11.80 s of measured silence. The only sound inside
that window is the badge's own tick (measured at −25 dB against −5 dB for the
narration around it), so the pause is silent of *narration* while still reading
as a running timer.

**Voice sync.** Every reveal waits for its narration bookmark *before* playing.
Against the rendered audio: **all twelve pieces at 0.00 s stretch** (title 9.73 s,
s1 17.34, s2 22.30, s3 20.61, s4 24.31, s5 17.91, s6 21.83, s7 27.28, s8 26.29,
s9q 16.65, s9a 16.39, s10 20.30; total speech 240.94 s in a 265.49 s video, the
rest being the silent clock and the holds).
`verify_sync.py`: 76 captions, first 0.28 s, last 263.47 s, **0 captions in
silence, 0 speech blocks uncaptioned** → PASS. `verify_captions.py`: narration
**671 words = SRT 671 words** → PASS (word for word).

### The silent clock and the narrated closing card (re-rendered)

* **Questions first, then the timer.** `play_challenge_countdown` no longer sits
  inside the questions voiceover: the ticks are the only sound in the clock
  window, and the answers begin after the clock.
* **The closing card is narrated.** The recap clears as the voice says "Thank
  you for watching," and "See you in the next lesson :)" lands as the voice says
  "and see you in the next lesson."; the piece holds the card for the 2.0 s
  `END_HOLD` (last caption 263.47 s in a 265.49 s cut).
* **A note on the tick (a real sound-effect bug, fixed here).**
  `CairoRenderer.play()` sets `skip_animations = True` whenever an animation is
  served from Manim's partial-movie cache, and `Scene.add_sound()` returns early
  while that flag is set. Every sound effect in these stories is added right
  after a `play()`, so a *cached* re-render silently dropped the pop, the ding
  and every tick of the clock from the audio track.
  `story_common.install_sfx_safe_sounds()` now restores the flag before handing
  over to `add_sound`; this cut — re-rendered after that fix — carries every one
  of them, the clock's own tick included.

## Pedagogical safeguards honoured

- **"Same base" is stated, never assumed.** Scenes 3, 5 and 6 carry an explicit
  "the same base" note; scene 8's second error is `2^3 × 3^4`, where the bases
  differ and the exponents therefore cannot be added.
- **The base is kept unchanged.** One persistent base object runs through each
  transformation; the bases are never multiplied into each other.
- **Product adds, it does not multiply.** Scene 8 shows `x^-3 · x^-2 = x^-5` and
  explicitly rejects `x^-6`.
- **The subtraction has a direction.** Scene 5's heading is "Top Exponent Minus
  Bottom Exponent" and the working reads `7 - 4 = 3`, so `n - m` cannot creep in.
- **A negative result is expected, not reversed.** Scene 6 computes `2 - 5 = -3`
  and then `5^-3 = 1/5^3 = 1/125`, tying straight back to storymode 02.
- **The non-zero base is always shown** (`a ≠ 0` on the recap's rule card, and
  "a is not zero, and the exponents are integers" on scene 7's strip).
- **The other laws are left out** — power-of-a-power and same-exponent products
  are not introduced, as the brief requires.

## Tools in this folder

`assemble_laws.py` (splices `_laws_fragment.py` + `_laws_beats.py` into the proven
video-03 head), `setup_tools.py`, `make_draft_srt.py`, `tts_precheck.py` (all 12
pieces generated audio with word boundaries before the render),
`audit_sync_overlap.py`, `audit_clearance.py`, `scene_frames.py`, `find_timer.py`,
and the chapter's `pipeline_360.py` / `pipeline_1080.py` (render → verify_sync →
verify_captions → burn captions → `final_videos/` and `final_videos/1080p/`).

**Frame sweep:** the title, all ten scenes and the closing card are in
`frames360/01_title.png … 11_s10.png`, with the cancellation moment and the
centred clock in `frames360/chk/`; the questions board, the silent clock, the
answers board and the closing card of this cut are in `frames360/chk2/`.

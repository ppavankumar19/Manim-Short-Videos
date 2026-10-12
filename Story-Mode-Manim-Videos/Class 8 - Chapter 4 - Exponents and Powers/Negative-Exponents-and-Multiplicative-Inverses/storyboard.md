# Production-Ready Storyboard — as built

## Understanding Negative Exponents: Reciprocal Rules and Multiplicative Inverses

CLASS 8 MATHEMATICS · CHAPTER 4 (EXPONENTS AND POWERS) · STORYMODE 02

**LLM KEY / FUNCTION NAME:** `negative_exponents_and_multiplicative_inverse`
**CLASS LEVEL:** Class 8 · **TEXTBOOK:** Telangana SCERT, 8 Maths EM 2025-26,
Chapter 4. The chapter motivates negative exponents from very small quantities
(a hair, `0.000005 m`), extends `10^3, 10^2, 10^1, 10^0` to
`10^-1, 10^-2, 10^-3` — each step one tenth of the one above — and then states
`a^-m = 1/a^m` for non-zero `a`, which makes `a^-m` the multiplicative inverse
of `a^m`.

## Learning objective

Extend the exponent pattern through `a^0` to negative exponents; understand that
a negative exponent does **not** make the value negative; read and use
`a^-m = 1/a^m`; rewrite negative powers with positive exponents; identify
multiplicative inverses of exponential expressions; verify `a^m · a^-m = 1`; and
connect negative powers of ten with `1/10, 1/100, 1/1000`.

**Primary takeaway:** **a negative exponent means "take the reciprocal"** —
`a^-m = 1/a^m`, `a ≠ 0`.

## The two persistent visuals

- **The Exponent Staircase** — one row per power, indented as it descends, with
  a "one step down" box beside it that divides by the staircase's **own base**
  (÷10 in the tens scenes, **÷2** in the powers-of-two scene, so the note is
  never left behind — safeguard G). The critical moment is
  `10^0 = 1` stepping down to the ringed `10^-1 = 1/10`, shown large in its own
  card, and only afterwards the general rule.
- **The Reciprocal Mirror** — a dashed vertical axis with `2^3 = 8` on the left
  and `2^-3 = 1/8` on the right, their product collapsing to `1`, then
  `a^m × a^-m = a^(m+(-m)) = a^0 = 1`.

## Scene plan (timings are the delivered cut's own)

| # | in | Scene | On-screen text | Maths |
|---|---|---|---|---|
| 0 | 0:00 | Title card | Negative Exponents | `2^-3 = 1/2^3 = 1/8` |
| 1 | 0:10 | From Huge Numbers to Tiny Numbers | We need a new kind of power | `1.4 × 10^9 m` → `0.000005 m` |
| 2 | 0:29 | Follow the Pattern | Every step down divides by ten | `10^3 … 10^0`, ÷10 between steps, `10^-1 = ?` |
| 3 | 0:47 | Crossing Zero | The minus sign moves the power under one | `10^-1 = 1/10`, `10^-2`, `10^-3` |
| 4 | 1:06 | Any Base Works | One step down divides by the base | `2^3 … 2^-2` with ÷2 |
| 5 | 1:24 | The Negative Exponent Rule | Negative exponent → reciprocal | `a^-m = 1/a^m`, `1/a^m = a^-m`, `a ≠ 0` |
| 6 | 1:47 | Not a Negative Number | The minus sign is part of the exponent | `2^-3 = 1/8 ≠ -2^3 = -8` |
| 7 | 2:05 | Multiplicative Inverses | Each is the inverse of the other | `8 × 1/8 = 1`, `a^m × a^-m = 1` |
| 8 | 2:29 | Flip the Sign | The inverse reverses the exponent sign | `3^-5↔3^5`, `4^-3↔4^3`, `x^-n↔x^n` |
| 9 | 2:49 | YOUR TURN — questions read, then the silent clock | Rewrite → Evaluate → Find the inverse | `10^-4`, `5^-2`, inverse of `7^-3` |
| 10 | 3:31 | Recap, then the spoken thank-you card | Negative exponent → reciprocal → inverse | staircase + mirror + rule |

**Delivered files**

    final_videos/NegativeExponentsInverseStory_captioned.mp4
    640×360, 30 fps, 233.29 s (3 min 53 s), 9.3 MB, 69 captions
    final_videos/NegativeExponentsInverseStory_captioned.srt
    final_videos/1080p/NegativeExponentsInverseStory_captioned.mp4
    1920×1080, 60 fps, master with the same burned captions
    final_videos/1080p/NegativeExponentsInverseStory_captioned.srt

The raw render and its ground-truth SRT also sit in
`media/videos/negative_exponents_and_multiplicative_inverse/360p30/` (and the
1080p60 raw cut in the sibling `1080p60/`).

## The production checks

**No overlaps, proper alignment/positioning.** `audit_sync_overlap.py` → **0**
out-of-board, text-in-text, text-on-line, text-inside-a-foreign-card, near-badge,
LaTeX-as-text, empty-TeX and **IN-CAPTION-BAND** flags. `audit_clearance.py` →
**0 pairs closer than 0.22 units, 0 text/line collisions, 0 foreign-box
collisions, 0 glyph-as-text hits**. The 98 `OFF-CENTRE` notes are the deliberate
diagram geometry — the staircase's descent indent, the ÷-note beside it, the
mirror's two halves and the challenge cards waiting on the left — and every
heading, banner, strip, rule card and answer row is centred on the board.

The draft pass caught, and the build fixed before rendering: the opening number
line drifting onto the question (it is positioned by its own y, not re-centred),
its end labels leaving the board, the third ÷10 chip touching the `10^-1 = ?`
card, the ÷-note's two lines sitting 0.14 apart, the last staircase row closing
on the strip, the reverse-rule card crowding its side note, and the mirror axis
running through the product lines.

**The YOUR TURN clock: centred on the board, ten seconds, and silent.**
`story_common.play_challenge_countdown(self, seconds=10, position=(BOARD_CX,
BOARD_CY))`. `find_timer.py` locates the countdown window at **184–193 s**, and
it is verified centred (with the three question cards waiting on the left, so the
badge covers nothing) in `frames360/chk2/t189.png`. The challenge is split into
three movements: the questions are read first (2:49.6–3:03.6), the clock then
ticks with **no narration under it**, and the answers follow (3:14.7 onward) —
the caption gap between the last question (3:03.58) and the first answer
(3:14.70) is 11.12 s of measured silence. The only sound inside that window is
the badge's own tick (measured at −25 dB against −5 dB for the narration around
it), so the pause is silent of *narration* while still reading as a running
timer.

**Voice sync.** Every reveal waits for its narration bookmark *before* playing.
Against the rendered audio: **all twelve pieces at 0.00 s stretch** (title 9.05 s,
s1 17.93, s2 16.84, s3 18.01, s4 17.06, s5 21.94, s6 17.68, s7 22.72, s8 19.12,
s9q 13.53, s9a 15.26, s10 20.27; total speech 209.41 s inside a 233.29 s video,
the rest being the silent clock and the holds).
`verify_sync.py`: 69 captions, first 0.22 s, last 231.38 s, **0 captions in
silence, 0 speech blocks uncaptioned** → PASS. `verify_captions.py`: narration
**598 words = SRT 598 words** → PASS (word for word).

### The silent clock and the narrated closing card (re-rendered)

* **Questions first, then the timer.** The clock used to run inside the
  questions voiceover, so its ticks competed with the voice. It now sits *after*
  the questions block: question → silence → clock → answers, with the tick the
  only sound in the clock window.
* **The closing card is narrated.** The recap clears as the voice says "Thank
  you for watching," so the "Thank You for Watching!" card appears *with* the
  words, and "See you in the next lesson :)" lands as the voice says "and see
  you in the next lesson."; the piece then holds the card for the 1.9 s
  `END_HOLD` (last caption 231.38 s in a 233.29 s cut).
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

- **The pattern comes first.** Scenes 2 and 3 build `10^3 → 10^0 → 10^-3` with
  visible `÷10` steps before the formula appears in scene 5.
- **A negative exponent is not a negative number.** Scene 6 sets
  `2^-3 = 1/2^3 = 1/8` against `-2^3 = -8` with a large `≠`, and the banner reads
  "the minus sign is part of the exponent".
- **The non-zero condition is always shown.** `a ≠ 0` sits beside every statement
  of the rule (scenes 5 and 10).
- **Reciprocal, not a sign trick.** The transformation shown is
  `a^-m → 1/a^m` (a card that literally moves the power under one), not merely
  `-m → m`.
- **The inverse is verified by its product.** Scene 7 shows `8 × 1/8 = 1` and
  `a^m × a^-m = a^(m+(-m)) = a^0 = 1`; scene 8 verifies each pair the same way.
- **Decimal expansion is left out**, as the brief asks — the video stays on
  negative exponents, reciprocals and inverses.
- **Object identity** is preserved throughout: the staircase rows stay the same
  mobjects as they are ringed and highlighted, and the mirror halves are the same
  cards that then multiply together.

## Tools in this folder

`assemble_negative.py` (splices `_negative_fragment.py` + `_negative_beats.py`
into the proven video-03 head), `setup_tools.py`, `make_draft_srt.py`,
`tts_precheck.py` (all 12 pieces generated audio with word boundaries before the
render), `audit_sync_overlap.py`, `audit_clearance.py`, `scene_frames.py`,
`find_timer.py`, and the chapter's `pipeline_360.py` / `pipeline_1080.py`
(render → verify_sync → verify_captions → burn captions → `final_videos/`
and `final_videos/1080p/`).

**Frame sweep:** the title, all ten scenes and the closing card are in
`frames360/01_title.png … 11_s10.png`, with the challenge and the centred clock
in `frames360/chk/`; the questions board, the silent clock, the answers board and
the closing card of this cut are in `frames360/chk2/`.

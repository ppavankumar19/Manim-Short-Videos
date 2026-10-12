# Production-Ready Storyboard — as built

## Advanced Laws of Exponents: Power of a Power, Product & Fraction Rules, and Zero Exponent

CLASS 8 MATHEMATICS · CHAPTER 4 (EXPONENTS AND POWERS) · STORYMODE 04

**LLM KEY / FUNCTION NAME:** `laws_of_exponents_power_product_quotient_zero`
**CLASS LEVEL:** Class 8 · **TEXTBOOK:** Telangana SCERT, 8 Maths EM 2025-26,
Chapter 4. The chapter's law summary is the spine of this video:

    (a^m)^n = a^(mn)        a^m b^m = (ab)^m
    (a/b)^m = a^m / b^m     a^0 = 1

## Learning objective

Simplify a power raised to another power; see why the exponents **multiply**;
distribute a common exponent over a product and over a fraction; derive `a^0 = 1`;
tell these four laws apart from storymode 03's product and quotient laws; and
recognise the classic errors, including `(x^2)^3 ≠ x^8`.

**Primary takeaway:** **look at the structure before choosing the law.**

## The visual identity — "the exponent knows what is inside the brackets"

- **power of a power:** the outer exponent duplicates the *whole* inner group —
  `(2^3)^2` becomes two groups of three tiles (the same tiles, coloured by group),
  they merge into one chain, and `2 groups × 3 factors = 6` gives `2^6`;
- **power of a product:** `(2×3)^4` becomes four copies of the bracket, the twos
  and the threes regroup into `2^4` and `3^4` — the exponent reaches every factor;
- **power of a fraction:** `(2/5)^3` becomes three copies of the fraction; the
  numerators group to `2^3` and the denominators to `5^3`;
- **zero exponent:** the same bookkeeping as storymode 03 — `a^4/a^4 = 1` by
  division, `= a^(4-4) = a^0` by the quotient law, therefore `a^0 = 1`.

## Scene plan (timings are the delivered cut's own)

| # | in | Scene | On-screen text | Maths |
|---|---|---|---|---|
| 0 | 0:00 | Title card | Advanced Laws of Exponents | the four laws |
| 1 | 0:13 | Same Exponents, Different Structures | First recognise the structure | `a^m×a^n` vs `(a^m)^n`, `(ab)^m`, `(a/b)^m` |
| 2 | 0:31 | Groups × Factors in Each Group | POWER OF A POWER — MULTIPLY THE EXPONENTS | `(2^3)^2 = 2^(3×2) = 2^6` |
| 3 | 0:57 | Multiply the Exponents | NEVER ADD THE EXPONENTS HERE | `m + m + … + m = mn`, `(a^m)^n = a^(mn)` |
| 4 | 1:21 | The Exponent Reaches Every Factor | THE OUTER EXPONENT APPLIES TO BOTH | `(2×3)^4 → 2^4·3^4`, `(ab)^m = a^m b^m` |
| 5 | 1:50 | Power the Top and the Bottom | POWER THE NUMERATOR AND THE DENOMINATOR | `(2/5)^3 = 2^3/5^3`, `(a/b)^m = a^m/b^m` |
| 6 | 2:14 | Zero Exponent Does Not Mean Zero | for any non-zero a | `a^4/a^4 = 1 = a^0 → a^0 = 1` |
| 7 | 2:42 | Structure Chooses the Law | RECOGNISE FIRST, THEN APPLY | the four lanes |
| 8 | 3:02 | Don't Mix the Rules | LOOK AT THE WHOLE EXPRESSION | `(x^2)^3`, `(ab)^3`, `(a/b)^2`, `7^0`, each corrected |
| 9 | 3:31 | YOUR TURN — questions read, then the silent clock | RECOGNISE FIRST, SIMPLIFY SECOND | `(3^4)^2`, `(5x)^3`, `(3/7)^2`, `(-6)^0` |
| 10 | 4:21 | Recap, then the spoken thank-you card | SEE THE STRUCTURE, THEN CHOOSE THE LAW | all four laws |

**Delivered files**

    final_videos/AdvancedExponentLawsStory_captioned.mp4
    640×360, 30 fps, 283.39 s (4 min 43 s), 10.7 MB, 74 captions
    final_videos/AdvancedExponentLawsStory_captioned.srt
    final_videos/1080p/AdvancedExponentLawsStory_captioned.mp4
    1920×1080, 60 fps, master with the same burned captions
    final_videos/1080p/AdvancedExponentLawsStory_captioned.srt

The raw render and its ground-truth SRT also sit in
`media/videos/laws_of_exponents_power_product_quotient_zero/360p30/` (and the
1080p60 raw cut in the sibling `1080p60/`).

*The brief estimated ~4 minutes; the cut runs 4 min 43 s. The storyboard's own
content drives that — the title card plus ten scenes, an expansion plus a generalisation
for each of the three power rules, four error cases and four challenge questions
with the series' ten-second clock. Nothing was padded, nothing was dropped.*

## The production checks

**No overlaps, proper alignment/positioning.** `audit_sync_overlap.py` → **0**
out-of-board, text-in-text, text-on-line, text-on-a-figure-side, text-inside-a-
foreign-card, near-badge, LaTeX-as-text, empty-TeX and **IN-CAPTION-BAND** flags.
`audit_clearance.py` → **0 pairs closer than 0.22 units, 0 text/line collisions,
0 foreign-box collisions, 0 glyph-as-text hits**. The 116 `OFF-CENTRE` notes are
the deliberate geometry — the two-column law dashboards (`GRID_X`), the tile
groups and the challenge cards — and every heading, banner, strip, law card and
answer row is centred on the board.

Two real defects were caught by the draft pass and fixed before rendering:

1. the zero-exponent law card sat on top of that scene's strip (the strip's text
   landed *inside* the card's border — reported as text-on-side and
   text-outside-box) — the strip was dropped there and the card given its own
   internal offsets;
2. the four challenge cards were stacked so tightly that each prompt sat 0.13
   from its expression — they now sit in a 2 × 2 grid **around** the centred
   clock, each tall enough for a 0.28 clearance.

**One tooling fix:** the audit anchor for scene 6 originally read
"why is any non-zero number". `norm_word` strips the hyphen from the SRT's words
but the anchor is compared raw, so the audit could never match it; the anchor is
now "why is any".

**The YOUR TURN clock: centred on the board, ten seconds, and silent.**
`story_common.play_challenge_countdown(self, seconds=10, position=(BOARD_CX,
BOARD_CY))`. `find_timer.py` locates the countdown window at **228–237 s**, and
`frames360/chk2/t233.png` shows it dead centre with the four question cards
waiting around it, none covered. The challenge runs as three movements —
questions read first (3:31.4–3:46.9), then the clock with **no narration under
it**, then the answers (3:58.5 onward): the caption gap between the last question
(3:46.85) and the first answer (3:58.54) is 11.69 s of measured silence. The only
sound inside that window is the badge's own tick (measured at −25 dB against
−5 dB for the narration around it), so the pause is silent of *narration* while
still reading as a running timer.

**Voice sync.** Every reveal waits for its narration bookmark *before* playing.
Against the rendered audio: **all twelve pieces at 0.00 s stretch** (title 11.88 s,
s1 16.68, s2 24.57, s3 23.50, s4 27.62, s5 23.68, s6 26.93, s7 19.18, s8 27.91,
s9q 15.47, s9a 22.36, s10 19.33; total speech 259.11 s inside a 283.39 s video,
the rest being the silent clock and the holds).
`verify_sync.py`: 74 captions, first 0.26 s, last 281.40 s, **0 captions in
silence, 0 speech blocks uncaptioned** → PASS. `verify_captions.py`: narration
**666 words = SRT 666 words** → PASS (word for word).

### The silent clock and the narrated closing card (re-rendered)

* **Questions first, then the timer.** `play_challenge_countdown` no longer sits
  inside the questions voiceover: the four prompts are read, then the clock ticks
  with no narration under it, and the four answers follow the clock.
* **The closing card is narrated.** The recap clears as the voice says "Thank
  you for watching," and "See you in the next lesson :)" lands as the voice says
  "and see you in the next lesson."; the piece holds the card for the 2.0 s
  `END_HOLD` (last caption 281.40 s in a 283.39 s cut).
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

- **Multiply, never add, in a power of a power.** Scene 3's strip reads "NEVER ADD
  THE EXPONENTS HERE", scene 8 opens with `(x^2)^3 = x^(2+3) = x^5` crossed out
  and corrected to `x^6`, and scene 1 places `a^m×a^n` beside `(a^m)^n` so the
  two structures are compared directly.
- **The exponent applies to the whole bracket.** Scene 8 crosses out `(ab)^3 =
  a^3b` and `(a/b)^2 = a^2/b`, correcting both.
- **Zero exponent ≠ zero.** `7^0 = 0` is crossed out and corrected to `1`; the
  derivation comes from `a^4/a^4`, not from assertion.
- **The non-zero condition is shown** beside the zero-exponent law
  ("for any non-zero a").
- **"Fraction rule" is never called a fractional exponent** — the base is a
  fraction, `(3/7)^2`, and the exponent is a plain integer.
- **The earlier laws are used only where needed** (the quotient law in scene 6);
  the learning load stays on the four new patterns.

## Tools in this folder

`assemble_advanced_laws.py` (splices `_advlaws_fragment.py` +
`_advlaws_beats.py` into the proven video-03 head), `setup_tools.py`,
`make_draft_srt.py`, `tts_precheck.py` (all 12 pieces generated audio with word
boundaries before the render), `audit_sync_overlap.py`, `audit_clearance.py`,
`scene_frames.py`, `find_timer.py`, and the chapter's `pipeline_360.py` /
`pipeline_1080.py` (render → verify_sync → verify_captions → burn captions →
`final_videos/` and `final_videos/1080p/`).

**Frame sweep:** the title, all ten scenes and the closing card are in
`frames360/01_title.png … 11_s10.png`, with the centred clock and the
phrase-level sync checks in `frames360/chk/`; the questions board, the silent
clock, the answers board and the closing card of this cut are in
`frames360/chk2/`.

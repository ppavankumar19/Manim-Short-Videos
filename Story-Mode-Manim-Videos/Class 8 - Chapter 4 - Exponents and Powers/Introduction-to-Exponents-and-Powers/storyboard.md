# Production-Ready Storyboard — as built

## Introduction to Exponents & Powers: Understanding Base, Exponent, Power and Exponential Notation

CLASS 8 MATHEMATICS · CHAPTER 4 (EXPONENTS AND POWERS) · STORYMODE 01

**LLM KEY / FUNCTION NAME:** `exponents_and_base_concept_introduction`
**CLASS LEVEL:** Class 8 · **TEXTBOOK:** Telangana SCERT, 8 Maths EM 2025-26,
Chapter 4. The chapter opens by recalling
`3 × 3 × 3 × 3 × 3 × 3 = 3^6`, generalises it to `3^m`, and motivates exponent
notation with very large quantities — the Sun's diameter `1,40,00,00,000 m`,
the Sun–Earth distance, the age of the universe — and the chessboard doubling
problem. Positive exponents only in this introduction.

## Learning objective

By the end of the video a student can: recognise repeated multiplication;
rewrite it in exponential notation; name the **base** and the **exponent** in
`3^6`; say what the exponent counts; tell the base, the exponent and the
resulting **power** apart; expand a power back into a product; and read `10^9`
as "10 raised to the power 9".

**Primary takeaway:** **exponent notation is a shortcut for repeated
multiplication** — `a × a × … × a` (n times) `= a^n`.

## Core visual metaphor — the Power Compressor

One repeated factor survives as the **base**, the rest of the chain collapses,
and the **count of factors** rides up into the exponent position, so the
exponent is *seen* to come from counting. The same `4` object stays on screen
through `4 × 4 × 4 × 4 × 4 → 4^5` (safeguard G), and the same idea is replayed at
scale: `10 × … × 10 → 10^9` and `1,40,00,00,000 → 1.4 × 10^9`.

## Scene plan (timings are the delivered cut's own)

| # | in | Scene | On-screen text | Maths |
|---|---|---|---|---|
| 0 | 0:00 | Title card | Introduction to Exponents & Powers | `3^6 = 3 × 3 × 3 × 3 × 3 × 3` |
| 1 | 0:10 | There Must Be a Shorter Way | Six factors, counted 1–6, then compressed | `3 × 3 × 3 × 3 × 3 × 3 → 3^6` |
| 2 | 0:26 | What Does the Exponent Count? | EXPONENT = NUMBER OF TIMES THE BASE IS USED AS A FACTOR | braced chain, `= 3^6` |
| 3 | 0:45 | Base, Exponent and Power | BASE · EXPONENT · POWER | `3^6`, read as "three raised to the power six" |
| 4 | 1:05 | The Power Compressor | COMPRESS ↔ EXPAND | `4 × 4 × 4 × 4 × 4 ↔ 4^5` |
| 5 | 1:26 | A Very Important Difference | THE EXPONENT COUNTS FACTORS | `4^5 = 1024 ≠ 4 × 5 = 20` |
| 6 | 1:45 | Powers of Ten | nine zeros after the one | `10^1, 10^2, 10^3, 10^9` |
| 7 | 2:04 | Why Exponents Are Useful | 10 raised to the power 9 | `1,40,00,00,000 m → 1.4 × 10^9 m` |
| 8 | 2:23 | When Numbers Grow Fast | Doubling again and again | chessboard `1, 2, 4, 8, 16, 32` |
| 9 | 2:43 | YOUR TURN — questions read, then the silent clock | Write → Expand → Identify | `7×7×7×7`, `2^5`, `10^6` |
| 10 | 3:24 | Recap, then the spoken thank-you card | BASE · EXPONENT · POWER | `a^n` |

**Delivered files**

    final_videos/ExponentsAndBaseConceptStory_captioned.mp4
    640×360, 30 fps, 225.62 s (3 min 46 s), 9.2 MB, 64 captions
    final_videos/ExponentsAndBaseConceptStory_captioned.srt
    final_videos/1080p/ExponentsAndBaseConceptStory_captioned.mp4
    1920×1080, 60 fps, master with the same burned captions
    final_videos/1080p/ExponentsAndBaseConceptStory_captioned.srt

The raw render and its ground-truth SRT also sit in
`media/videos/exponents_and_base_concept_introduction/360p30/` (and the 1080p60
raw cut in the sibling `1080p60/`).

## The two production instructions

1. **No overlaps, and proper alignment/positioning.**
   `audit_sync_overlap.py` → **0** out-of-board, text-in-text, text-on-line,
   text-inside-a-foreign-card, near-badge, LaTeX-as-text, empty-TeX and
   **IN-CAPTION-BAND** flags. `audit_clearance.py` → **0 pairs closer than 0.22
   units, 0 text/line collisions, 0 foreign-box collisions, 0 glyph-as-text
   hits** — the tightest layout of the series so far (the earlier videos carry 9
   to 10 accepted pairs inside single panels; here every one was measured out).
   The 81 `OFF-CENTRE` notes are the deliberate two-column and left-column
   diagrams (the Sun beside its number, the `4^5` against `4 × 5`, the compressor
   in/out, and the three question cards waiting on the left), all of which the
   audit reports for review rather than as defects; every heading, banner, strip
   and answer row is centred on the board.
   Eight tight pairs were found in the draft pass and fixed before the render
   (panel heading/body spacing, the chessboard grain labels, the elapsed
   question cards); the chessboard square was widened from 0.62 to 0.66 to give
   "16" and "32" their clearance.

2. **The YOUR TURN clock: centred on the board, ten seconds, and silent.**
   `story_common.play_challenge_countdown(self, seconds=10, position=(BOARD_CX,
   BOARD_CY))` — the series' shared badge, dead centre of the green board.
   The whole challenge is now deliberately split into three movements:
   the **questions are read first** (2:43.3–2:57.7, the three cards on the
   left), the clock then runs with **no narration at all** — only its own
   tick — and the **answers** follow it (3:08.9 onward). The clock no longer
   overlaps a single spoken word.
   `find_timer.py` locates the countdown window at **178–188 s (11 s** of
   screen time = 0.4 fade-in + 10 counted seconds + 0.4 fade-out), and it is
   verified centred in `frames360/chk2/t183.png`; the caption gap between the
   last question (2:57.99) and the first answer (3:08.94) is 10.95 s of
   measured silence. The only sound inside that window is the badge's own tick
   (measured at −25 dB against −5 dB for the narration around it), so the pause
   is silent of *narration* while still reading as a running timer. The three
   question cards were placed on the left half so the badge never covers them;
   the answers fade in after the clock, centred.

## Voice sync (the third instruction)

Every reveal waits for the bookmark that ends the phrase describing it and only
then plays (`self.wait(leftover(tracker, "bN"))` *before* the `FadeIn`), so the
board can never run ahead of the voice; `closing()` consumes each window's tail.

`audit_sync_overlap.py` against the rendered audio: **all twelve pieces at
0.00 s stretch** (title 8.73 s, s1 15.52, s2 17.43, s3 19.61, s4 19.47, s5 17.64,
s6 18.48, s7 18.19, s8 18.64, s9q 14.44, s9a 13.92, s10 19.04; total speech
201.11 s over a 225.62 s video, the rest being the silent clock and the
`TRANSITION_HOLD`/`END_HOLD` beats).

`verify_sync.py`: 64 captions, first at 0.12 s, last at 223.31 s, **0 captions in
silence, 0 speech blocks uncaptioned** → PASS.
`verify_captions.py`: narration **542 words = SRT 542 words** → PASS (word for
word).

### The silent clock and the narrated closing card (re-rendered)

Two production notes were folded into this cut:

* **Questions first, then the timer.** The ten-second clock used to run inside
  the questions voiceover, so its ticks competed with the voice reading the
  questions. `play_challenge_countdown` now sits *after* the questions
  voiceover block, so the board reads *question → silence → clock → answers*:
  the last question lands at 2:57.99, the clock ticks from 178 s to 188 s with
  no narration under it, and the answers start at 3:08.94.
* **The closing card is narrated.** The recap clears as the voice says "Thank
  you for watching," so the "Thank You for Watching!" card appears *with* the
  words, and "See you in the next lesson :)" lands as the voice says "and see
  you in the next lesson."; the piece then holds the card for the 2.3 s
  `END_HOLD` (last caption 223.31 s in a 225.62 s cut).
* **A note on the tick (a real sound-effect bug, fixed here).**
  `CairoRenderer.play()` sets `skip_animations = True` whenever an animation is
  served from Manim's partial-movie cache, and `Scene.add_sound()` returns early
  while that flag is set. Every sound effect in these stories is added right
  after a `play()`, so a *cached* re-render silently dropped the pop, the ding
  and every tick of the clock from the audio track.
  `story_common.install_sfx_safe_sounds()` now restores the flag before handing
  over to `add_sound`; this cut — re-rendered after that fix — carries every one
  of them, the clock's own tick included.

Spot-checked on frames: at 3:17 the caption reads "*is five twos multiplied
together. And in ten to*" with answers A and B on the board; at 3:43.5 the
closing card is on the centred board with the caption
"*see you in the next lesson.*"; at 2:32.5 "*Every square doubles the one before
it*" lands with the chessboard note.

### Sync correction — the factor counters (re-rendered)

Scene 2's counter badges used to pop in over one second while the voice spent
about four seconds naming the factors ("three times three times three times three
times three times three: six equal factors"), so the counter was finished long
before the sentence was. The visit now spreads across whatever is left of that
phrase's narration window (`time_until_bookmark("b1")`, capped at 3.2 s), so the
badges appear one by one as the factors are named. Verified on the re-rendered
cut: at 0:29.5 the six factor tiles are up with no badges yet; by 0:31 the badges
have reached 4 and the fifth is fading in. The narration text is unchanged; the
`.srt` was regenerated by the re-render and re-verified (64 cues, 542 words).

## Pedagogical safeguards honoured

- **The exponent counts factors.** Scene 1 builds six separate 3s with a counter
  visiting each; scene 2 braces them as "6 factors" before writing `3^6`.
  Nothing on screen ever suggests `3^6 = 3 × 6`.
- **Base and exponent stay attached.** `3^6` is set as one MathTex object, and
  the compressor's superscript is pinned to the surviving base tile's corner.
- **Expression, expansion and value are kept distinct.** Scene 5 shows
  `4^5 = 4 × 4 × 4 × 4 × 4 = 1024` beside `4 × 5 = 20`, separated by a large ≠.
- **Consistent vocabulary.** BASE / EXPONENT / POWER appear with the same colours
  (cyan / pink / green) in scenes 3, 5 and 10.
- **Smaller from larger.** The subtraction and comparison always read left to
  right from the larger quantity; no negatives anywhere.
- **No negative exponents, no standard-form rules.** `1.4 × 10^9` is used purely
  as motivation, as the textbook's introduction does.
- **Object identity.** `VGroup` identity is preserved through the compressor
  (`base.animate.move_to`, `Transform(out, expanded)`) rather than clearing and
  redrawing.

## Tools in this folder

`assemble_exponents.py` (splices `_exponents_fragment.py` + `_exponents_beats.py`
into the proven video-03 head), `setup_tools.py`, `make_draft_srt.py`,
`tts_precheck.py` (all 12 pieces generated audio with word boundaries before the
render), `audit_sync_overlap.py`, `audit_clearance.py`, `scene_frames.py`,
`find_timer.py`, and the chapter's `pipeline_360.py` / `pipeline_1080.py`
(render → verify_sync → verify_captions → burn captions → `final_videos/`
and `final_videos/1080p/`).

**Frame sweep:** the title, all ten scenes and the closing card are in
`frames360/01_title.png … 11_s10.png`, with the challenge, the centred clock and
the phrase-level sync checks in `frames360/chk/`; the questions board, the silent
clock, the answers board and the closing card of this cut are in
`frames360/chk2/`.


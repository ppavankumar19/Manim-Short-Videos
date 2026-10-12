# Production-Ready Storyboard — as built

## Standard Form with Powers of 10: Writing Very Large and Very Small Numbers

CLASS 8 MATHEMATICS · CHAPTER 4 (EXPONENTS AND POWERS) · STORYMODE 05
*(the closing video of the five-part sequence)*

**LLM KEY / FUNCTION NAME:** `scientific_notation_large_and_small_numbers`
**CLASS LEVEL:** Class 8 · **TEXTBOOK:** Telangana SCERT, 8 Maths EM 2025-26,
Chapter 4. The section recalls `300,000,000 m = 3 × 10^8 m`, extends the same
idea to very small numbers (`0.000003 m = 3 × 10^-6 m`, the wire in a computer
chip), gives the plant cell `0.00001275 m = 1.275 × 10^-5 m`, and asks students
to convert back to usual form (`3.02 × 10^-6 = 0.00000302`).

## Learning objective

See why powers of ten handle both extremes; convert large numbers and decimals
below 1 into standard form; read the exponent's sign as the scale (positive →
large place value, negative → small); convert back to usual form; and connect
the decimal point's movement with the power of ten.

**Primary takeaway:** **move the decimal point, count the places, write the
power of ten** — and always ask which direction you are converting.

## The visual identity — the Decimal-Point Elevator

The numeral is laid out digit by digit on a place-value track, and a bright
decimal **marker walks it one place at a time** while a counter ticks above it,
so the exponent is *counted*, never announced:

- `300000000` → the point starts at the right-hand end, walks **left 8 places**
  to sit after the 3, and gives `3 × 10^8`;
- `6020000000` → **left 9 places**, the kept digits 602 ringed, giving
  `6.02 × 10^9`;
- `0000003` (i.e. `0.000003`) → the point starts at the left, walks **right 6
  places**, and the exponent takes the **minus** sign: `3 × 10^-6`;
- `0.00001275` → **right 5 places**, with the significant digits 1275 ringed and
  unchanged, giving `1.275 × 10^-5`.

### The example diagrams

Each measured example is drawn beside its number, so the scale is visible and not
just asserted:

| drawing | where | what it is |
|---|---|---|
| the **Sun** — a chalk disc with eight rays | scene 1, left | `300,000,000 m`, the Sun's distance |
| the **chip** — a body with six legs and one highlighted wire across it | scenes 1 and 5 | `0.000003 m`, the wire inside a computer chip |
| the **plant cell** — wall, nucleus, vacuole and organelles | scene 6 | `0.00001275 m`, a plant cell |

Scene 1 sets them opposite each other with the question "Can one notation handle
both?" and a double arrow labelled *same notation* between them; scenes 5 and 6
carry their drawing beside the elevator while it walks. All three are drawn with
Manim primitives (circles, lines, rounded rectangles, an ellipse and dots) — no
image files — so they stay crisp at any resolution.

## Scene plan (timings are the delivered cut's own)

| # | in | Scene | On-screen text | Maths |
|---|---|---|---|---|
| 0 | 0:00 | Title card | Standard Form with Powers of 10 | `300,000,000 = 3×10^8`, `0.000003 = 3×10^-6` |
| 1 | 0:15 | One Notation for Both Extremes | The exponent tells the scale | the Sun **drawn** beside `300,000,000 m`, the **chip with its wire** beside `0.000003 m` |
| 2 | 0:35 | The Exponent Tells the Scale | POWERS OF TEN ARE A SCALE | `10^-3 … 10^3` on a ruler |
| 3 | 0:57 | Large → Positive Exponent | MOVE LEFT, COUNT, EXPONENT IS POSITIVE | `300,000,000 → 3×10^8` (8 moves) |
| 4 | 1:15 | Count the Moves | LARGE NUMBER → POSITIVE EXPONENT | `6020000000 → 6.02×10^9` (9 moves) |
| 5 | 1:41 | Small → Negative Exponent | SMALL NUMBER → NEGATIVE EXPONENT | `0.000003 → 3×10^-6` (6 moves), the chip drawn beside the track |
| 6 | 2:11 | Keep the Digits — Change the Scale | the significant digits do not change | `0.00001275 → 1.275×10^-5` (5 moves), the plant cell drawn beside the track |
| 7 | 2:38 | Standard Form → Usual Form | POSITIVE → RIGHT; NEGATIVE → LEFT | `4.67×10^4 = 46700`, `3.02×10^-6 = 0.00000302` |
| 8 | 3:12 | Which Direction Am I Converting? | FIRST ASK WHICH WAY YOU ARE CONVERTING | the four conversion routes |
| 9 | 3:37 | YOUR TURN — questions read, then the silent clock | MOVE, COUNT, CHOOSE THE SIGN, WRITE | `0.0000456`, `6020000000`, `5.8×10^7` |
| 10 | 4:25 | Recap, then the spoken thank-you card | POWERS OF 10 WRITE THE VERY LARGE AND THE VERY SMALL | both extremes |

**Delivered files**

    final_videos/StandardFormStory_captioned.mp4
    640×360, 30 fps, 292.16 s (4 min 52 s), 11.1 MB, 86 captions
    final_videos/StandardFormStory_captioned.srt
    final_videos/1080p/StandardFormStory_captioned.mp4
    1920×1080, 60 fps, master with the same burned captions
    final_videos/1080p/StandardFormStory_captioned.srt

The raw render and its ground-truth SRT also sit in
`media/videos/scientific_notation_large_and_small_numbers/360p30/` (and the
1080p60 raw cut in the sibling `1080p60/`).

*The brief estimated ~4 minutes; the cut runs 4 min 52 s. The storyboard's own
content drives it — the title card plus ten scenes, four full elevator walks (8, 9, 6 and
5 counted places), both conversion directions and three challenge questions with
the ten-second clock. Nothing was padded, nothing was dropped.*

## The production checks

**No overlaps, proper alignment/positioning.** `audit_sync_overlap.py` → **0**
out-of-board, text-in-text, text-on-line, text-on-a-figure-side, text-inside-a-
foreign-card, near-badge, LaTeX-as-text, empty-TeX and **IN-CAPTION-BAND** flags.
`audit_clearance.py` → **0 pairs closer than 0.22 units, 0 text/line collisions,
0 foreign-box collisions, 0 glyph-as-text hits** — including the elevator's
digit-by-digit tracks, whose glyphs sit on a 0.44 pitch. The 129 `OFF-CENTRE`
notes are the deliberate geometry (the two-column comparison, the scale ruler,
the conversion rows, the challenge cards); every heading, banner, strip, card and
answer row is centred on the board.

**One build defect was caught before any render** (by the audit harness): the
elevator's track and counter heights had been declared only as class attributes
and were referenced as bare names inside a method, which raised `NameError`; they
are now module-level constants alongside the other layout constants.

**The YOUR TURN clock: centred on the board, ten seconds, and silent.**
`story_common.play_challenge_countdown(self, seconds=10, position=(BOARD_CX,
BOARD_CY))`. `find_timer.py` locates the countdown window at **233–242 s**, and
`frames360/chk2/t238.png` shows it dead centre with the three question cards
around it, none covered. The challenge runs as three movements — questions read
first (3:37.2–3:52.5), then the clock with **no narration under it**, then the
answers (4:03.9 onward): the caption gap between the last question (3:52.48) and
the first answer (4:03.96) is 11.48 s of measured silence. The only sound inside
that window is the badge's own tick (measured at −25 dB against −5 dB for the
narration around it), so the pause is silent of *narration* while still reading
as a running timer.

**Voice sync.** Every reveal waits for its narration bookmark *before* playing.
Against the rendered audio: **all twelve pieces at 0.00 s stretch** (title 14.09 s,
s1 18.71, s2 21.00, s3 17.54, s4 24.71, s5 29.13, s6 25.62, s7 32.66, s8 24.16,
s9q 15.31, s9a 20.51, s10 24.56; 268.00 s of speech inside a 292.16 s video, the
rest being the silent clock and the holds).
`verify_sync.py`: 86 captions, first 0.40 s, last 290.43 s, **0 captions in
silence, 0 speech blocks uncaptioned** → PASS. `verify_captions.py`: narration
**750 words = SRT 750 words** → PASS (word for word).

### The silent clock and the narrated closing card (re-rendered)

* **Questions first, then the timer.** `play_challenge_countdown` no longer sits
  inside the questions voiceover, so the three conversions are read, the clock
  then ticks with no narration under it, and the three answers follow the clock.
* **The closing card is narrated.** The recap clears as the voice says "Thank
  you for watching the chapter," and "See you in the next lesson :)" lands as the
  voice says "and see you in the next lesson."; the piece holds the card for
  the 1.7 s `END_HOLD` (last caption 290.43 s in a 292.16 s cut).
* **A note on the tick (a real sound-effect bug, fixed here).**
  `CairoRenderer.play()` sets `skip_animations = True` whenever an animation is
  served from Manim's partial-movie cache, and `Scene.add_sound()` returns early
  while that flag is set. Every sound effect in these stories is added right
  after a `play()`, so a *cached* re-render silently dropped the pop, the ding
  and every tick of the clock from the audio track.
  `story_common.install_sfx_safe_sounds()` now restores the flag before handing
  over to `add_sound`; this cut — re-rendered after that fix — carries every one
  of them, the clock's own tick included.

### Sync correction — the elevator walk (re-rendered)

An on-screen check of the delivered cut found the walk itself out of step with
the voice. The marker moved at a fixed 0.22 s per place, so all nine places of
`6020000000` were done in about two seconds while the narration spent seven
seconds speaking them: at 1:26 the caption read "Move it left until only one
non-zero" with the counter already at **7**, and at 1:30, while the voice said
"*one, two, three, four, five*", the counter already read **9**.

The words were already right, so the narration text is unchanged; what changed is
when each place happens:

- **where the voice counts aloud** — scene 4 (one…nine) and scene 6 (one…five) —
  every number now carries its own bookmark, and the marker advances one place
  **on that spoken number**, so the counter shows the number being said;
- **where the voice does not count** — scenes 3 (eight places) and 5 (six
  places) — the walk is spread across the whole narration window
  (`time_until_bookmark(next) / places`, capped at 0.90 s) instead of running at
  a fixed rate, so it cannot finish early.

Verified on the re-rendered cut at the same timestamps: 1:26 → counter **0** with
the marker at the right-hand end (the walk is just beginning); 1:32 → counter
**8** while the voice says "six, seven, eight, nine places"; 2:20 → counter **0**
before "Move the decimal point right: one, …" begins. The `.srt` was regenerated
by the re-render and re-verified (86 cues, 750 words).

## Pedagogical safeguards honoured

- **Standard form vs usual form** are named consistently, and scene 7 states
  explicitly that its decimal directions belong to the *reverse* conversion, so
  the two sets of directions cannot be confused.
- **"Count the zeros" is never taught.** Every conversion counts *decimal
  moves*, which is why the multi-digit case (`0.00001275`, five moves) works the
  same way as the single-digit one.
- **The two directions are separated:** scene 8 is a four-route map — usual →
  standard (left/positive, right/negative) and standard → usual (right for a
  positive exponent, left for a negative one).
- **A negative exponent is not a negative quantity.** `3 × 10^-6` is built from
  a positive 3; the minus belongs to the power, tying back to storymode 02.
- **The significant digits are preserved.** The `1275` in scene 6 is ringed and
  never changes — "same quantity, different representation".
- **No comparison lesson.** The Sun/Earth comparison is deliberately left out;
  the video stays on conversion between usual and standard form.
- **Source contexts** carry the motivation: the Sun's distance, the wire inside a
  computer chip and a plant cell.

## Tools in this folder

`assemble_standard_form.py` (splices `_standard_form_fragment.py` +
`_standard_form_beats.py` into the proven video-03 head), `setup_tools.py`,
`make_draft_srt.py`, `tts_precheck.py` (all 12 pieces generated audio with word
boundaries before the render), `audit_sync_overlap.py`, `audit_clearance.py`,
`scene_frames.py`, `find_timer.py`, and the chapter's `pipeline_360.py` /
`pipeline_1080.py` (render → verify_sync → verify_captions → burn captions →
`final_videos/` and `final_videos/1080p/`).

**Frame sweep:** the title, all ten scenes and the closing card are in
`frames360/01_title.png … 11_s10.png`, with the countdown in `frames360/chk/`; the
questions board, the silent clock, the answers board and the closing card
of this cut are in `frames360/chk2/`.

---

## The chapter, complete

| # | video | deliverable | length |
|---|---|---|---|
| 01 | Introduction to Exponents & Powers | `ExponentsAndBaseConceptStory_captioned.mp4` | 3:46 |
| 02 | Negative Exponents and Multiplicative Inverses | `NegativeExponentsInverseStory_captioned.mp4` | 3:53 |
| 03 | Product & Quotient Laws of Exponents | `ProductQuotientLawsStory_captioned.mp4` | 4:25 |
| 04 | Advanced Laws: Power, Product, Fraction, Zero | `AdvancedExponentLawsStory_captioned.mp4` | 4:43 |
| 05 | Standard Form with Powers of 10 | `StandardFormStory_captioned.mp4` | 4:52 |

All five sit in `Class 8 - Chapter 4 - Exponents and Powers/final_videos/`, each
with its ground-truth `.srt`, each 360p with the captions burned in, and each
audited with 0 overlap, 0 clearance and 0 caption-band flags and 0.00 s sync
stretch on every narration piece. The same five are in the folder's `1080p/`
sub-folder as 1920×1080 / 60 fps masters with the identical caption burn.
Every cut ends the same way: the challenge questions are read first, the
ten-second THINK clock then ticks with no narration under it, the answers follow,
and the closing thank-you card is spoken — "Thank you for watching… see you in the
next lesson" plays over the card itself.


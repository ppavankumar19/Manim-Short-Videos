# Production-Ready Storyboard — as built

## Understanding Curves & Regions: Open, Closed, Interior, Exterior & Boundary

CLASS 6 MATHEMATICS · CHAPTER 4 (BASIC GEOMETRICAL IDEAS) · STORYMODE 02

**LLM KEY / FUNCTION NAME:** `curves_open_closed_and_regions`
**CLASS LEVEL:** Class 6 · **TEXTBOOK:** Telangana SCERT, 6 Maths EM 2025-26,
Chapter 4. The chapter introduces curves through drawings, contrasts open and
closed curves, defines a **simple curve** as one that does not cross itself, and
explains that a closed figure separates the plane into **interior, boundary and
exterior**, with **region = interior + boundary**.

## Learning objective

By the end of the video a student can: describe a **curve** as a figure drawn
without lifting the pencil (even a straight line counts); tell an **open** curve
from a **closed** one; identify a **simple** curve as one that never crosses
itself; keep "open/closed" and "simple/not-simple" as two separate questions;
and classify a point as lying in the **interior**, on the **boundary**, or in the
**exterior** of a closed figure, with **region = interior + boundary**.

**Primary takeaway:**

**Open/Closed = does the path close?** · **Simple = does it cross itself?** ·
**A closed figure gives Interior, Boundary and Exterior.**

## Core visual metaphor — one pencil, three questions

A persistent pencil path is drawn, joined, bent and un-bent: an open wave, a
closed loop, a self-crossing figure eight, and finally the closed loop that
becomes the park boundary with its shaded interior and outside. The three
question cards — *does it close?*, *does it cross itself?*, *where is the
point?* — generate the whole lesson.

## Scene plan (timings are the delivered cut's own)

| # | in | Scene | Key on-screen text | Concept |
|---|---|---|---|---|
| 0 | 0:00 | Title card | open · closed · not simple | curve |
| 1 | 0:17 | One pencil, many curves | even a straight line is a curve | curve |
| 2 | 0:38 | Open or closed? | OPEN CURVE · CLOSED CURVE | open vs closed |
| 3 | 0:53 | Simple or self-crossing? | SIMPLE · NOT SIMPLE | self-crossing |
| 4 | 1:12 | Two different questions | OPEN + SIMPLE · CLOSED + SIMPLE · CLOSED, NOT SIMPLE | two axes |
| 5 | 1:35 | A closed curve separates the plane | BOUNDARY · INTERIOR · EXTERIOR | park wall |
| 6 | 1:55 | Where is the point? | A interior · B boundary · C exterior | point location |
| 7 | 2:08 | What is a region? | REGION = INTERIOR + BOUNDARY | region |
| 8 | 2:23 | From a closed curve to a polygon | polygon = line segments | bridge |
| 9 | 2:38 | YOUR TURN — questions, the silent clock, answers | open/closed, simple, locate P·Q·R | all concepts |
| 10 | 3:36 | Recap, then the spoken thank-you card | draw → classify → locate | all concepts |

**Delivered files**

The 360p cut:

    final_videos/CurvesOpenClosedRegionsStory_captioned.mp4
    640×360, 30 fps, 241.50 s (4 min 01 s), 72 captions
    final_videos/CurvesOpenClosedRegionsStory_captioned.srt

The 1080p60 master, re-rendered from the same module (the pipeline re-synthesises
the narration, so the cut re-times by a few hundredths of a second; the boarding,
the layout and the word-for-word captions are identical):

    final_videos/1080p/CurvesOpenClosedRegionsStory_captioned.mp4
    1920×1080, 60 fps, 241.50 s, 14 490 frames, 42.86 MB, 72 captions
    final_videos/1080p/CurvesOpenClosedRegionsStory_captioned.srt

    verify_sync.py      video 241.500 s, 72 captions, first 0.48 s, last
                        239.51 s, 0 in silence, 0 uncaptioned  -> PASS
    verify_captions.py  narration 623 words = SRT 623 words       -> PASS

`pipeline_1080.py` in this chapter folder produced the master
(render 1920×1080/60 → verify → burn → `final_videos/1080p/`); libass scales the
one caption style with the video height, so the 1080p burn is the 360p burn
three times the size.

The raw renders and their ground-truth SRTs sit in
`media/videos/curves_open_closed_and_regions/360p30/` and `…/1080p60/`.

## Layout revision (second cut)

The first cut was re-cut after a review of four frames. Every fix keeps a label
clear of the curve it names, and every figure row is centred on `BOARD_CX`:

- **Title card** — `OPEN` / `CLOSED` / `NOT SIMPLE` moved off the drawn curves
  (labels 0.60 → 0.52, figures -0.25 → -0.38, captions -1.10 → -1.20), which
  also opens the sub-heading/label gap from 0.215 to 0.32.
- **Title card** — the closed loop's marker is now a `ValueTracker`-driven
  parametric point (`loop_point`, `LOOP_SPEED = 2.4 rad/s`), so it laps the loop
  every ~2.6 s for the whole hold instead of sitting still; it is chalk-yellow so
  it stays visible on the green loop. Audit: `audit_trace_motion.py` reads the
  dot's pixel centroid out of seven frames of the hold and finds it advancing
  ~94° every 0.7 s (2.35 rad/s) on the ellipse.
- **One Pencil, Many Curves** — `row_centres()` places the four figures so their
  ink has exactly 0.75 of air between neighbours and the row's union is centred
  on +0.50 (`[-3.77..+4.77]`).
- **Open or Closed?** — "the path comes back and closes" moved from inside the
  oval to `y = 0.26`, below the oval and above the chips.
- **Simple or Self-Crossing?** — "never crosses itself" and "it crosses itself
  here" moved to `y = 0.30`, clear below the oval and the figure-eight.
- **Your Turn** — the P/Q/R card keeps 0.30 between its prompt and the mini
  figure (0.20 left `Q`'s letter touching the prompt).

`audit_text_curve.py` was added for this review: neither shipped audit can see a
label lying on a *smooth* curve, because a bare `VMobject` wave or figure-eight
is not a frame kind to them and an `Ellipse` counts as a frame text may sit in.
It measures every text leaf against every sampled curve point and also prints
each piece's curve-block centre.

## Revision (third cut): answer columns and the closing sync

- **A/B/C/D and 1/2/3 on one vertical line.** `answer_row()` no longer centres
  each row inside its box (which put the letter at a different x in every row).
  The row is laid out in fixed columns anchored at `box left + 0.34`, with a
  constant 0.36 between tag, sentence and note, so the tag column and the
  sentence column are one vertical line in both the answers scene and the recap.
  The box still centres on `BOARD_CX`; the widest row (D) is 7.08 wide against
  7.92 of room, so nothing overflows the box.
- **The closing scene waits for the voice.** `NARRATION["s10"]` gained a bookmark
  before "Thank you for watching," and the goodbye mark was renumbered:

      b0 "A curve is drawn…"      -> row 1
      b1 "If the ends stay apart…"-> row 2
      b2 "And if it never…"       -> row 3
      b3 "A closed curve gives…"  -> REGION = INTERIOR + BOUNDARY (stays up)
      b4 "Draw, classify, locate."-> the closing strip, on its own mark
      b5 "Thank you for watching,"-> clear the board, fade in the thank-you card
      b6 "and see you in the next…"-> fade in the goodbye line

  The old cut cleared the board on b4 — one phrase early, so the frame jumped
  ahead of the voice. No narration word changed. Measured on the rendered cut
  (`audit_reveal_times.py`, bright-ink counts per pixel band): the three rows and
  the rule line are still up at 235.10 s, the strip arrives at ~234.0 s with
  "Draw, classify, locate." (spoken 234.5–235.5), the board starts clearing at
  235.50 s exactly as "Thank you" is spoken (235.65) and the card is up by
  236.5 s, inside "Thank you for watching,". `audit_audio_onsets.py` confirms the
  SRT word times match the acoustic onsets to within 0.1 s; the residual
  0.2–0.8 s lead between a reveal and its word is the voiceover tracker's
  piecewise-linear bookmark interpolation and applies to every reveal in the
  series (the same lead is in the earlier cuts).

## The two production instructions

1. **No overlaps, and proper alignment/positioning.**
   `audit_sync_overlap.py` → **0** out-of-board, text-in-text, text-on-line,
   text-inside-a-foreign-card, near-badge, LaTeX-as-text, empty-TeX and
   **IN-CAPTION-BAND** flags. `audit_clearance.py` → **0 pairs closer than 0.22
   units, 0 text/line collisions, 0 foreign-box collisions**. Every heading sits
   on the board's heading line, every curve is pinned with `at` so two diagrams
   on one row line up, and the whole board stays above `CAPTION_SAFE_Y = -2.00`.

2. **The YOUR TURN clock: centred on the board, ten seconds, and silent.**
   `story_common.play_challenge_countdown(self, seconds=10, position=(BOARD_CX,
   BOARD_CY))` — the series' shared badge, dead centre of the green board. The
   challenge runs as three movements: the four questions are **read first**
   (2:38.3–3:03.3), the clock then ticks for ten seconds with **no narration
   under it** (only its own tick, measured at −25 dB against −4.5 dB for the
   narration around it), and the four answers follow (3:14.7 onward). The four
   question cards sit in the four corners so the badge never covers one.
   `find_timer.py` locates the countdown window at **184–193 s (10 s** of screen
   time) and it is verified centred in `frames360/chk/s9_clock.png`.

## Voice sync (the third instruction)

Every reveal waits for the narration bookmark that ends the phrase describing it
and only then plays (`self.wait(leftover(tracker, "bN"))` *before* the play), so
the board can never run ahead of the voice; `closing()` consumes each window's
tail.

`audit_sync_overlap.py` against the rendered audio: **all twelve pieces at
0.00 s stretch** (title 15.55 s, s1 19.36, s2 14.62, s3 17.89, s4 21.28, s5 18.85,
s6 12.85, s7 13.61, s8 13.92, s9q 25.02, s9a 20.20, s10 23.35; total speech
216.50 s inside a 241.40 s video, the rest being the silent clock, the transition
holds and the closing hold).

`verify_sync.py`: 72 captions, first at 0.48 s, last at 239.57 s, **0 captions in
silence, 0 speech blocks uncaptioned** → PASS.
`verify_captions.py`: narration **623 words = SRT 623 words** → PASS (word for
word).

The closing card is **narrated**: the recap clears as the voice says "Thank you
for watching," so the "Thank You for Watching!" card appears *with* the words,
and "See you in the next lesson :)" lands as the voice says "and see you in the
next lesson."; the cut then holds the card for 1.93 s.

## Pedagogical safeguards honoured

- **"Simple" means "does not cross itself", not "easy".** Scenes 3 and 4 state
  this with the textbook wording, and the crossing point is shown pulsing.
- **Open/closed and simple/not-simple are two separate questions.** Scene 4
  shows three representative cases (open + simple, closed + simple, closed +
  not simple) rather than treating the words as three competing labels.
- **A curve need not look bent.** Scene 1 draws a straight line and labels it a
  curve, matching the textbook's note.
- **Interior is not the region.** Scene 7 keeps the boundary highlighted and
  writes **region = interior + boundary**.
- **A boundary is its own category**, neither inside nor outside — scene 6 gives
  three points, one in each place.
- **Interior/exterior appear only after a closed figure** (never for the open
  wave), following the textbook.
- **Polygons are a bridge, not the topic.** Scene 8 connects a closed curve to a
  polygon and defers the details to later shapes.
- **Object identity.** The same open wave, oval and figure eight recur across
  scenes, so the classification is visibly about the same drawings.

## Tools in this folder

`assemble_curves.py` (splices `_curves_fragment.py` + `_curves_beats.py` into the
proven video-03 head), `setup_tools.py`, `make_draft_srt.py`, `tts_precheck.py`,
`audit_sync_overlap.py`, `audit_clearance.py`, `audit_text_curve.py` (text against
real curve geometry), `audit_trace_motion.py` (is the title marker still
moving?), `audit_reveal_times.py` (when does each reveal actually hit the
screen?) and `audit_audio_onsets.py` (where are the words, acoustically?),
`scene_frames.py`, `find_timer.py`, and the chapter's `pipeline_360.py`
(render → verify_sync → verify_captions → burn captions → `final_videos/`).

**Frame sweep:** the title, each concept scene, the centred clock, the answers
board, the recap and the closing card are in `frames360/chk/` (the numbered
`01_…`-`12_…` stills from `scene_frames.py`, the named sweep above them, and
`title_check/` — seven stills across the title hold for the marker's motion).

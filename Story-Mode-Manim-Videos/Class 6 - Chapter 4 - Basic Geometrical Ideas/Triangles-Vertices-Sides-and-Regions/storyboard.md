# Production-Ready Storyboard — as built

## Triangles Uncovered: Vertices, Sides, Angles, and Triangular Regions

CLASS 6 MATHEMATICS · CHAPTER 4 (BASIC GEOMETRICAL IDEAS) · STORYMODE 05

**LLM KEY / FUNCTION NAME:** `triangles_vertices_sides_and_triangular_region`
**CLASS LEVEL:** Class 6 · **TEXTBOOK:** Telangana SCERT, 6 Maths EM 2025-26,
Chapter 4. The chapter reaches a triangle through the **matchstick activity**:
three is the **least number of sticks needed to form a closed figure**. It then
defines a **triangle** as a **simple closed figure formed by three line
segments**, names the segments `AB, BC, CA` as its **sides**, the points
`A, B, C` as its **vertices**, identifies the three **angles** at those
vertices, and states that a triangle separates the plane into **interior,
boundary and exterior**, where the **boundary together with the interior is the
triangular region**.

## Learning objective

By the end of the video a student can: recognise a triangle as a **simple closed
figure made from three line segments**; explain why one stick or two sticks
cannot close a figure; name the three **sides** and the three **vertices** of
`ABC`; identify the **three angles** `∠BAC, ∠ABC, ∠ACB` and say which vertex
each belongs to; name a triangle by its vertices (`△ABC`, `△BCA`, `△CAB`); and
sort any point of the plane as **interior, on the boundary, or exterior** —
where the **triangular region = interior + boundary**.

**Primary takeaway:**

**3 sides** · **3 vertices** · **3 angles** ·
**Boundary + interior = triangular region**

## Core visual metaphor — three sticks become a triangle

One set of three segments is built in front of the learner and never replaced.
First stick: still open. Second stick: a V, and the two free ends are still
apart. Third stick: the ends meet and the figure closes. That **same triangle**
is then taken apart in layers — each side traced and named, each meeting point
pulsed as a vertex, an arc drawn at every corner for the angle, the boundary
traced once more for the name `△ABC`, points dropped inside, on and outside the
figure, and finally the interior and the boundary merged into the triangular
region. Nothing is introduced on a separate static slide.

## Realistic diagrams (production direction)

The figure is drawn with the conventions a textbook illustration uses, using
Manim's own geometry primitives — no image files:

- the three segments are **thick chalk strokes** (`SIDE_W = 4.4`); in the
  opening scene the very same segments are **matchsticks**, each with its head
  (`match_stick`);
- the **interior carries a soft tint** (`Polygon`, `fill_opacity` 0.10–0.22) so
  the figure reads as a region and not just an outline, and the tint is what
  grows when the third stick closes the shape;
- **solid vertex dots** sit exactly on the three corners, each with its capital
  letter offset outward by the one rule (`corner_label_dx`: 0.40 units out along
  that corner's own outward bisector — so A, B and C look alike and none of them
  can sit on a side), and every side name sits 0.26 units off its own line;
- the **angle at a corner is marked with a real arc** (`corner_arc`, radius
  0.46) drawn between the two sides that meet there, in its own colour per
  vertex;
- the **boundary is lit** as a separate object (`INTERIOR` tint overlaid with a
  thicker yellow boundary) when the triangular region is defined;
- the figure is built with `Create`, picked out with `Indicate`, and paced
  across its narration window.

## Scene plan (timings are the delivered cut's own)

| # | in | Scene | Key on-screen text | Geometry focus |
|---|---|---|---|---|
| 0 | 0:00 | Title card | 3 SIDES · 3 VERTICES · 3 ANGLES | the three parts |
| 1 | 0:15 | How many sticks close a figure? | 3 IS THE LEAST NUMBER OF SEGMENTS | 1 stick → 2 → 3 closes |
| 2 | 0:35 | What is a triangle? | 3 LINE SEGMENTS = TRIANGLE | simple + closed + 3 segments |
| 3 | 0:52 | The three sides | SIDE 1 · AB, SIDE 2 · BC, SIDE 3 · CA | `AB, BC, CA` |
| 4 | 1:05 | The three vertices | VERTEX A · B · C | corners, not sides |
| 5 | 1:18 | Three vertices, three angles | at A `∠BAC`, at B `∠ABC`, at C `∠ACB` | the angle at each corner |
| 6 | 1:34 | Naming the triangle | `△ABC` · BCA and CAB | the name from the vertices |
| 7 | 1:50 | Interior, boundary, exterior | P · INTERIOR, Q · BOUNDARY, R · EXTERIOR | the three parts of the plane |
| 8 | 2:07 | The triangular region | INTERIOR + BOUNDARY = TRIANGULAR REGION | the boundary is included |
| 9 | 2:20 | YOUR TURN — questions read, then the silent clock | four checks on `PQR` | all concepts |
| 10 | 2:52 | The four answers | A sides · B vertices · C angle at Q · D X, Y, Z | all concepts |
| 11 | 3:14 | Recap, then the spoken thank-you card | BUILD · IDENTIFY · LOCATE | all concepts |

**Delivered files**

The 360p cut:

    final_videos/TrianglesVerticesSidesAndTriangularRegionStory_captioned.mp4
    640×360, 30 fps, 216.16 s (3 min 36 s), 63 captions, 9.22 MB
    final_videos/TrianglesVerticesSidesAndTriangularRegionStory_captioned.srt

The 1080p60 master, re-rendered from the same module (the pipeline re-synthesises
the narration, so the cut re-times by a few hundredths of a second; the boarding,
the layout and the word-for-word captions are identical):

    final_videos/1080p/TrianglesVerticesSidesAndTriangularRegionStory_captioned.mp4
    1920×1080, 60 fps, 216.32 s, 12 979 frames, 38.93 MB, 63 captions
    final_videos/1080p/TrianglesVerticesSidesAndTriangularRegionStory_captioned.srt

    verify_sync.py      video 216.317 s, 63 captions, first 0.52 s, last
                        214.33 s, 0 in silence, 0 uncaptioned  -> PASS
    verify_captions.py  narration 547 words = SRT 547 words       -> PASS

`pipeline_1080.py` in this chapter folder produced the master
(render 1920×1080/60 → verify → burn → `final_videos/1080p/`); libass scales the
one caption style with the video height, so the 1080p burn is the 360p burn
three times the size.

The raw renders and their ground-truth SRTs sit in
`media/videos/triangles_vertices_sides_and_triangular_region/360p30/` and
`…/1080p60/`.

*The brief estimated ~3 min 40 s; the delivered cut runs 3 min 36 s. Every
scene from the storyboard is present with its full content and no padding, so
the tighter narration simply reads a little faster — nothing was dropped.*

## The three production instructions

1. **No overlaps, and proper alignment/positioning.**
   `audit_sync_overlap.py` against the rendered audio → **0** out-of-board,
   text-in-text, text-on-side, text-on-line, text-inside-a-foreign-card,
   near-badge, empty-TeX, LaTeX-as-text and **IN-CAPTION-BAND** flags.
   `audit_clearance.py` → **0 pairs closer than 0.22 units, 0 text/line
   collisions, 0 foreign-box collisions**.
   `audit_badge_clearance.py` (measures each heading's own bounding box against
   the two real corner badges) → the tightest heading in the video is the s7
   sub-heading at **0.71 units** of clear air, i.e. every heading clears both
   badges by more than twice the 0.30 units the user asked for.
   The triangle is built from fixed, audited coordinates (`TRI_A (0.15, 1.30)`,
   `TRI_B (-1.00, -0.45)`, `TRI_C (2.00, -0.45)`, ink centre
   `TRI_CEN (0.50, 0.425)`) so every scene draws the same figure, it is the
   diagram block and is **centred on `BOARD_CX = 0.50`** in every scene, and the
   right-hand column is its deliberate side label column: every chip and card is
   **left-aligned on `COL_L = 2.70` and capped at `COL_W = 2.70`**, so the column
   reads down one vertical line, never crosses the figure and never reaches the
   board's edge (its own right edge ≤ 5.40 against a limit of 5.48). The three
   answer rows and the four recap rows are laid out in **fixed columns**
   (`answer_row(pad=0.34, buff=0.36)`) so the tag and the text start on the same
   x in every row, the two-line column cards separate their keyword and note by
   0.52 units, and nothing on the board reaches `CAPTION_SAFE_Y = -2.00`.

2. **The YOUR TURN clock: centred on the board, ten seconds, and silent.**
   `story_common.play_challenge_countdown(self, seconds=10, position=(BOARD_CX,
   BOARD_CY))` — the series' shared badge, dead centre of the green board
   (board centre `(0.5, 0.20)` → pixel ≈ (342, 171) of 640×360), with the four
   question cards in the four corners of the board so the badge covers none of
   them. The challenge runs as three movements: the four questions are **read
   first** (2:20.9–2:40.9, 19.99 s of narration), the clock then ticks for ten
   seconds with **no narration under it** (2:40.9–2:50.9), and the four answers
   follow (2:51.5 onward). Per-second `volumedetect`: **−25.1 dB** (the tick
   alone) for every whole second `162 … 171`, against **−7.3 dB** for the
   question narration before and **−4.2 dB** for the answers after.
   `find_timer.py` locates the countdown window at **161 s → 171 s (10 s** of
   screen time) and it is centred in `frames360/chk/zz_timer_mid.png`
   (showing `THINK 5S` at the middle of the board).

3. **Realistic diagrams** — see the production direction above: thick chalk
   sides, matchsticks with heads in the opening scene, a tinted interior, solid
   vertex dots with offset letters, real corner arcs and a lit boundary.

## Voice sync (the fourth instruction)

Every reveal waits for the narration bookmark that ends the phrase describing it
and only then plays (`self.wait(leftover(tracker, "bN"))` *before* the play), so
the board can never run ahead of the voice; `closing()` consumes each window's
tail.

`audit_sync_overlap.py` against the rendered audio: **all twelve pieces at
0.00 s stretch** (title 14.26 s, s1 18.77, s2 15.52, s3 11.98, s4 12.54,
s5 15.36, s6 14.86, s7 15.60, s8 12.38, s9q 19.99 [10.49 s of it the silent
clock window], s9a 21.11, s10 19.70; total speech **192.07 s inside a 216.16 s
video**, the rest being the 10 s silent clock, the transition holds and the
closing hold), and **0 overlap / clearance flags against the real cut**.

`verify_sync.py`: video 216.161 s, audio 214.229 s, silent tail +1.931 s [ok],
**63 captions**, first at 0.52 s, last at 214.20 s, speech blocks 57 (173.1 s of
speech), caption time 196.6 s, **0 captions in silence, 0 speech blocks
(> 1.0 s) uncaptioned** → PASS.
`verify_captions.py`: narration **547 words = SRT 547 words** → PASS (word for
word).

Delivered voice windows (`scene_frames.py`, one hold frame per scene):
title 0.52–15.81 · s1 15.81–35.54 · s2 35.54–52.07 · s3 52.07–65.04 ·
s4 65.04–78.43 · s5 78.43–94.83 · s6 94.83–110.80 · s7 110.80–127.50 ·
s8 127.50–140.95 · s9q 140.95–172.19 (questions read, then the clock) ·
s9a 172.19–194.19 · s10 194.19–216.16.

The closing scene is fixed by bookmarks only, and the last piece now carries one
bookmark per movement: **b3** reveals the fourth recap row, **b4** reveals the
strip as the voice says "and locate the points." (so the whole recap list is
still on the board through the closing sentence), **b5** — the bookmark in front
of "Thank you for watching," — clears the board and brings in the "Thank You for
Watching!" card, and **b6** lands "See you in the next lesson :)" with the
spoken goodbye; the cut then holds the card for 1.93 s (captions 62–63, ending
3:34.20). Frames at 3:29.0 s (list + strip, voice still on "and locate the
points.") and 3:31.5 s (board cleared, card up) confirm the frame is never ahead
of the voice.

## Pedagogical safeguards honoured

- **A triangle must be closed, and three is the least number of segments.** Scene
  1 shows one stick and then two sticks failing to close the figure before the
  third closes it, and states the conclusion in the banner.
- **Sides are not vertices.** Scene 3 names the three *line segments*; scene 4
  names the three *points* where they meet, and adds "a corner, not a side".
- **Every angle belongs to a vertex.** Scene 5 marks the angle at each corner and
  names it with the **vertex in the middle** (`∠BAC`, `∠ABC`, `∠ACB`), which is
  exactly the naming rule the previous Storymode established for angles.
- **No triangle classification.** Equilateral, isosceles, scalene and acute /
  right / obtuse are deliberately absent: this section of the chapter deals with
  the triangle's anatomy and its region only.
- **No measures, and no angle sum.** Degree measures and "the angles of a
  triangle add to 180°" are not part of this subsection and are not used here.
- **The triangular region is more than the inside.** Scene 8 tints the interior,
  then lights the boundary, and states that the region is the interior **together
  with the boundary** — the region includes the sides.
- **Object continuity.** The same three segments are used throughout: first as
  matchsticks, then as the triangle's sides, then as the arms of the angles at
  the corners, and finally as the boundary of the triangular region.

## Tools in this folder

`assemble_triangles.py` (splices `_triangles_fragment.py` + `_triangles_beats.py`
into the proven video-03 head), `setup_tools.py`, `make_draft_srt.py`,
`tts_precheck.py`, `audit_sync_overlap.py`, `audit_clearance.py`,
`audit_badge_clearance.py`, `scene_frames.py`, `find_timer.py`, and the
chapter's `pipeline_360.py` (render → verify_sync → verify_captions → burn
captions → `final_videos/`).

**Frame sweep:** `frames360/chk/` holds the title, the matchstick scene, each
concept scene (`03_s2` … `09_s8`), the four challenge cards (`10_s9q`, plus
`zz_card_qa/qb/qd` crops), the centred clock at mid-countdown
(`zz_timer_mid.png`, `zz_captioned_timer.png`), the answers board (`11_s9a`),
the closing card (`12_s10`), the closing transition against the voice
(`zz_close_209/210` = list + strip under "and locate the points.", `zz_close_211/212`
= board cleared, card up under "Thank you for watching,") and the burn-in check
(`zz_captioned_210.png`: the caption sits below the strip, no collision).

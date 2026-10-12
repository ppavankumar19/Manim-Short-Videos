# Production-Ready Storyboard — as built

## Exploring Quadrilaterals: Sides, Angles, Diagonals, and Opposite vs. Adjacent Elements

CLASS 6 MATHEMATICS · CHAPTER 4 (BASIC GEOMETRICAL IDEAS) · STORYMODE 06

**LLM KEY / FUNCTION NAME:** `quadrilaterals_sides_angles_and_diagonals`
**CLASS LEVEL:** Class 6 · **TEXTBOOK:** Telangana SCERT, 6 Maths EM 2025-26,
Chapter 4. The chapter defines a **quadrilateral** as a **simple closed polygon
with four sides**; for `ABCD` it names the four **sides** `AB, BC, CD, DA`, the
four **angles** `∠A, ∠B, ∠C, ∠D`, and the two **diagonals** `AC, BD` that join
**opposite vertices** — and it then works through **opposite sides, adjacent
sides, opposite angles and adjacent angles**, which is the conceptual centre of
this lesson.

## Learning objective

By the end of the video a student can: recognise a quadrilateral as a **simple
closed polygon with four sides**; name its four **sides**, four **vertices** and
four **angles**; tell **adjacent** (next to — they share a vertex) from
**opposite** (across — they never meet), for both sides and angles; identify the
two **diagonals** as the segments that join opposite vertices; and apply all of
this to a fresh quadrilateral `PQRS`.

**Primary takeaway:**

**4 sides** · **4 vertices** · **4 angles** · **2 diagonals** ·
**Adjacent = next to** · **Opposite = across** ·
**Diagonal = opposite vertices joined**

## Core visual metaphor — one quadrilateral as a relationship map

A single quadrilateral `ABCD` is built once and never replaced. First the
third side of the previous lesson's triangle **opens out into two sides** to make
the fourth corner; then the boundary is laid segment by segment; then each idea
is revealed by changing only the emphasis — the four sides traced and named, the
four corners pulsed, an arc drawn at every corner, two **adjacent** sides
brought together on their **shared vertex**, two **opposite** sides lit across
the shape, opposite angles lit in pairs, and finally the two opposite vertices
joined by the **dashed diagonals**. Nothing is introduced on a separate static
slide.

## Realistic diagrams (production direction)

The figure is drawn with the conventions a textbook illustration uses, using
Manim's own geometry primitives — no image files:

- the four sides are **thick chalk strokes** (`SIDE_W = 4.4`), and a highlighted
  side is overlaid in its own colour at double weight so the emphasis reads at
  360p;
- the **interior carries a soft tint** (`Polygon`, `fill_opacity` 0.11–0.22) so
  the figure reads as a region and not just an outline;
- **solid vertex dots** sit exactly on the four corners, each with its capital
  letter offset outward, and every side name is placed 0.5 units off its line, so
  no letter ever sits on a side;
- the **diagonals are dashed** (`DashedLine`) — the standard convention for a
  segment that crosses the inside of a figure, and never confused with the
  boundary;
- the **angle at a corner is marked with a real arc** (`corner_arc`, radius
  0.42) drawn between the two sides that meet there, colour-coded per corner;
- the figure is built with `Create`, picked out with `Indicate`, and paced across
  its narration window.

## Scene plan (timings are the delivered cut's own)

| # | in | Scene | Key on-screen text | Geometry focus |
|---|---|---|---|---|
| 0 | 0:00 | Title card | 4 SIDES · 4 VERTICES · 4 ANGLES · 2 DIAGONALS | the anatomy |
| 1 | 0:10 | Adding a Fourth Corner | THE THIRD SIDE OPENS IN TWO | triangle `ABC` → `ABCD` |
| 2 | 0:30 | What makes it a quadrilateral | 4 SEGMENTS = QUADRILATERAL | built segment by segment |
| 3 | 0:57 | The four sides and four vertices | SIDE 1 · AB … 4 SIDES · THE BOUNDARY | `AB, BC, CD, DA`; `A, B, C, D` |
| 4 | 1:16 | Four corners, four angles | at A `∠A` … at D `∠D` | the angle at each corner |
| 5 | 1:30 | Adjacent means next to | ADJACENT SIDES SHARE A CORNER | `AB` with `BC` (share `B`), `AB` with `DA` (share `A`) |
| 6 | 1:46 | Opposite means across | NEXT TO OR ACROSS? | `AB`↔`CD`, `BC`↔`DA`, `∠A`↔`∠C`, `∠B`↔`∠D` |
| 7 | 2:12 | Diagonals | OPPOSITE VERTICES = DIAGONAL | the dashed `AC` and `BD` |
| 8 | 2:32 | The relationship map | ADJACENT · OPPOSITE · DIAGONAL | the three modes together |
| 9 | 2:56 | YOUR TURN — questions read, then the silent clock | four checks on `PQRS` | all concepts |
| 10 | 3:25 | The four answers | A `PS` · B `∠R` · C `PS, QR` · D `PR, QS` | all concepts |
| 11 | 3:46 | Recap, then the spoken thank-you card | BUILD · COMPARE · CONNECT | all concepts |

**Delivered files**

The 360p cut:

    final_videos/QuadrilateralsSidesAnglesAndDiagonalsStory_captioned.mp4
    640×360, 30 fps, 247.30 s (4 min 07 s), 70 captions, 10.83 MB
    final_videos/QuadrilateralsSidesAnglesAndDiagonalsStory_captioned.srt

The 1080p60 master, re-rendered from the same module (the pipeline re-synthesises
the narration, so the cut re-times by a few hundredths of a second; the boarding,
the layout and the word-for-word captions are identical):

    final_videos/1080p/QuadrilateralsSidesAnglesAndDiagonalsStory_captioned.mp4
    1920×1080, 60 fps, 247.40 s, 14 844 frames, 43.69 MB, 70 captions
    final_videos/1080p/QuadrilateralsSidesAnglesAndDiagonalsStory_captioned.srt

    verify_sync.py      video 247.400 s, 70 captions, first 0.58 s, last
                        245.20 s, 0 in silence, 0 uncaptioned  -> PASS
    verify_captions.py  narration 590 words = SRT 590 words       -> PASS

`pipeline_1080.py` in this chapter folder produced the master
(render 1920×1080/60 → verify → burn → `final_videos/1080p/`); libass scales the
one caption style with the video height, so the 1080p burn is the 360p burn
three times the size.

The raw renders and their ground-truth SRTs sit in
`media/videos/quadrilaterals_sides_angles_and_diagonals/360p30/` and
`…/1080p60/`.

## Revision (second cut): one centred figure, one marker rule, a capped column

The first cut was re-cut after the user's review, then swept for the same
classes of defect in every scene.

- **The quadrilateral is redrawn and centred.** It used to run
  `A(-2.90,1.00) B(-0.35,1.42) C(0.95,-0.65) D(-2.25,-0.95)` with its ink centred
  on x ≈ -0.98 and its `D` letter down at y = -1.15 (inside the banner's band,
  avoided only by writing a short banner). It is now a clean, well-proportioned
  general convex quadrilateral -- deliberately *not* a special one, since this
  section is about the general structure -- whose ink is centred on the board
  axis:

      A(-1.02, 1.40)   B(+1.82, +1.12)      ink bbox centre (+0.500, +0.510)
      C(+2.02, -0.34)  D(-0.68, -0.38)      3.05 wide x 1.77 tall

  No pair of sides is parallel and no two angles are equal (AB slopes -0.098,
  DC +0.015; BC -5.9, DA -3.6), and the interior is tinted.
- **One marker rule.** `MARK_SIZE = 18` and `LABEL_R = 0.40`: every corner
  letter sits the same distance out along the bisector of its own corner, in
  every scene (the old offsets were four hand-picked pairs -- `C` was labelled
  sideways at `(+0.35, +0.05)`), so A, B, C and D look alike and none can touch
  a side. The four letters now measure A y[+1.57..+1.76], B y[+1.32..+1.51],
  C y[-0.71..-0.51], D y[-0.78..-0.59]: 0.26 clear of the sub-heading, 0.25
  clear of the banner. Side names use the same idea (`SIDE_LAB_R = 0.30` off
  the middle of their own side, computed from the geometry), so none of them
  needs a hand-placed coordinate either.
- **The right-hand column is capped and left-aligned.** `COL_L = 2.70` is the
  column's left edge -- just right of the figure's rightmost letter (2.41) --
  and every item is left-aligned there and at most `COL_W = 2.70` wide, so no
  label can drift across the figure or off the board (the old column sat centred
  at 3.60 with items up to 3.57 wide, reaching x = 5.39). Four chip texts were
  shortened to fit the cap without losing meaning ("4 SIDES · BOUNDARY",
  "4 VERTICES · CORNERS", "AB opposite CD", "BC opposite DA"; "angles A with C ·
  B with D" became "A opposite C · B opposite D") and the longest sit at size 12.
- **The diagonals read apart**: AC is dashed yellow and BD dashed pink, and each
  chip matches its diagonal's colour (they were both yellow).
- **`answer_row()` now uses fixed columns** (tag, name and note each on their
  own vertical line, box still centred on `BOARD_CX`), in the answers scene and
  in the recap list.
- **Sync**: the last piece gained a bookmark before "Thank you for watching,"
  (and the goodbye mark was renumbered), so the recap list stays on the board
  through the whole closing sentence, the strip is written on its own bookmark
  as the voice says "Build it, compare its parts, and connect the corners.", and
  only the bookmark in front of "Thank you for watching," clears the board and
  brings in the card. The closing `Indicate` was trimmed to 0.90 s, which takes
  the last piece from 0.19 s stretch to **0.00 s** like every other.

## Revision (third cut): the scene-1 heading vs the corner badge

The shipped `NEAR-BADGE` check looks only at a coarse corner strip, so it passed
a heading that the user could plainly see running into the top-right
"Mathematics" badge. Measured properly — the real badges are built by the
scene's own `_corner_badge`, right badge `x [+3.79..+5.59] y [+2.82..+3.22]`,
left `x [-4.52..-3.01]` — the scene-1 heading was `6.68` wide with its right edge
at `+3.84`: the two boxes **overlapped** (`-0.05` in x and `-0.06` in y).

- **Scene 1 heading: "What Happens When We Add a Fourth Corner?" →
  "Adding a Fourth Corner"** (on-screen text only; the narration is untouched,
  and it keeps the same heading line, size 20, amber colour and weight). Its
  right edge moved from `+3.84` to `+2.20`: clearance to the right badge
  **-0.05 → 1.58** board units, measured **1.60** on the rendered frame (72 px).
- **Every other heading, sub-heading and banner was then measured the same way.**
  None needed changing; the tightest is scene 3's "The Four Sides and the Four
  Vertices" (5.21 wide, right edge `+3.10`) at **0.68** to the right badge
  (0.71 = 32 px on the rendered frame), then scene 7's "Diagonals Join Opposite
  Vertices" at 0.99 (1.00 on the frame). The sub-headings sit at y = 2.16, below
  the badges' bottom edge (2.81), and the banners/strips are 3.8+ away.
  Two tools were added for this: `audit_badge_clearance.py` (exact mobject
  geometry for every heading, sub-heading and banner) and `audit_badge_pixels.py`
  (the same gap measured on a rendered frame).

*The brief estimated ~3 min 50 s; the delivered cut runs 4 min 07 s. Every scene
from the storyboard is present with its full content and no padding.*

## The three production instructions

1. **No overlaps, and proper alignment/positioning.**
   `audit_sync_overlap.py` against the rendered audio → **0** out-of-board,
   text-in-text, text-on-side, text-on-line, text-inside-a-foreign-card,
   near-badge, empty-TeX, LaTeX-as-text and **IN-CAPTION-BAND** flags.
   `audit_clearance.py` → **0 pairs closer than 0.22 units, 0 text/line
   collisions, 0 foreign-box collisions**. The quadrilateral is defined once
   (`QUAD_LOCAL` + `QUAD_CEN`, centred on `BOARD_CX`, with `corner_label_dx`
   placing every letter by the one rule) so every scene draws the same centred
   figure; the figure keeps the board's centre line while the right-hand column
   (`COL_L = 2.70`, items at most `COL_W = 2.70` wide) carries whatever that
   scene is naming, so nothing is ever written across the boundary, and nothing
   on the board reaches `CAPTION_SAFE_Y = -2.00`.

2. **The YOUR TURN clock: centred on the board, ten seconds, and silent.**
   `story_common.play_challenge_countdown(self, seconds=10, position=(BOARD_CX,
   BOARD_CY))` — the series' shared badge, dead centre of the green board
   (board centre `(0.5, 0.20)` → pixel ≈ (342, 171) of 640×360), with the four
   question cards in the four corners of the board so the badge covers none of
   them. The challenge runs as three movements: the four questions are **read
   first** (2:56.8–3:14.2, 17.41 s of narration), the clock then ticks for ten
   seconds with **no narration under it** (3:14.2–3:24.2), and the four answers
   follow (3:25.4 onward). Per-second `volumedetect`: **−25.1 dB** (the tick
   alone) for every whole second `195 … 204`, against **−12.1 dB** for the fading
   question narration before and **−6.6 dB** for the answers after.
   `find_timer.py` locates the countdown window at **195 s → 204 s (10 s** of
   screen time) and it is centred in `frames360/chk/zz_timer_mid.png`
   (showing `THINK 5S` at the middle of the board).

3. **Realistic diagrams** — see the production direction above: thick chalk
   sides, a tinted interior, solid vertex dots with offset letters, real
   colour-coded corner arcs, and the two diagonals drawn as dashed lines across
   the inside.

## Voice sync (the fourth instruction)

Every reveal waits for the narration bookmark that ends the phrase describing it
and only then plays (`self.wait(leftover(tracker, "bN"))` *before* the play), so
the board can never run ahead of the voice; `closing()` consumes each window's
tail.

`audit_sync_overlap.py` against the rendered audio: **all twelve pieces at
0.00 s stretch** (title 8.77 s, s1 18.99, s2 25.95, s3 18.01, s4 12.52,
s5 15.71, s6 24.80, s7 19.03, s8 23.00, s9q 17.41, s9a 20.31, s10 18.24; total
speech **222.74 s inside a 247.30 s video**, the rest being the 10 s silent
clock, the transition holds and the closing hold), and **0 overlap / clearance
flags against the real cut**.

`verify_sync.py`: video 247.191 s, audio 245.163 s, silent tail +2.029 s [ok],
**70 captions**, first at 0.58 s, last at 245.12 s, speech blocks 78 (196.7 s of
speech), caption time 227.5 s, **0 captions in silence, 0 speech blocks
(> 1.0 s) uncaptioned** → PASS.
`verify_captions.py`: narration **590 words = SRT 590 words** → PASS (word for
word).

Delivered voice windows (the piece's own first cue, from the real SRT):
title 0.58 · s1 10.39 · s2 30.41 · s3 57.30 · s4 76.59 · s5 90.08 · s6 106.79 ·
s7 132.65 · s8 152.92 · s9q 176.77 (questions read, then the clock) ·
s9a 205.44 · s10 226.65 — the cut ends at 247.20 s.

The closing card is **narrated**: the recap clears as the voice says "Build it,
compare its parts, and connect the corners. Thank you for watching," so the
"Thank You for Watching!" card appears *with* the words, and "See you in the next
lesson :)" lands as the voice says "and see you in the next lesson."; the cut
then holds the card for 2.03 s (captions 69–70, ending 4:05.06).

## Pedagogical safeguards honoured

- **A quadrilateral must be simple and closed.** Scene 2 lays `AB`, `BC` and
  `CD` as an open chain and only the fourth segment closes the figure; scene 1
  shows the fourth corner arriving before the shape is called a quadrilateral.
- **Sides, vertices and angles stay distinct.** Scene 3 names the four *line
  segments* and the four *points*; scene 4 turns each corner into its angle, and
  the words "side" and "vertex" are never used of the wrong object.
- **Adjacent means sharing a vertex.** Scene 5 lights `AB` with `BC` on the
  shared vertex `B`, then `AB` with `DA` on the shared vertex `A`, and states the
  rule; `AB` and `CD` are never called adjacent.
- **Opposite means no shared vertex.** Scene 6 pairs `AB`↔`CD` and `BC`↔`DA`,
  then the angles `∠A`↔`∠C` and `∠B`↔`∠D`, exactly the relationships the textbook
  gives, with the phrase "across the shape".
- **A diagonal joins opposite vertices.** Scene 7 joins `A` with `C` and `B`
  with `D`, marks both as diagonals, and the boundary segments are never called
  diagonals.
- **No special quadrilaterals yet.** Square, rectangle, parallelogram, rhombus
  and trapezium are deliberately absent: this section is about the general
  structure of a quadrilateral.
- **Continuity with the previous lessons.** Scene 1 starts from the triangle of
  Storymode 05 and *grows* the fourth corner, and scene 4 reuses the
  angle-naming idea of Storymode 04 (`∠A` is the angle at `A`).
- **The plane-region idea is only a quick connection.** The interior, boundary
  and exterior were taught in Storymodes 02 and 05, so here they appear only in
  one closing line of scene 2 rather than as another full segment.

## Tools in this folder

`assemble_quads.py` (splices `_quads_fragment.py` + `_quads_beats.py` into the
proven video-03 head), `setup_tools.py`, `make_draft_srt.py`, `tts_precheck.py`,
`audit_sync_overlap.py`, `audit_clearance.py`, `audit_row_columns.py` (are the
answers rows' letters really on one vertical line?), `scene_frames.py`,
`find_timer.py`, and the chapter's `pipeline_360.py` (render → verify_sync →
verify_captions → burn captions → `final_videos/`).

**Frame sweep:** `frames360/chk/` holds the numbered stills (`01_title` …
`12_s10`), the named sweep (`title.png`, `s1_fourth_corner.png`, `s2_build.png`,
`s3_sides.png`, `s4_angles.png`, `s5_adjacent.png`, `s6_opposite.png`,
`s7_diagonals.png`, `s8_map.png`, `s9_answers.png`, `s10_recap.png`,
`s10_card.png`), the centred clock at mid-countdown (`zz_timer_mid.png`, 200 s)
and the closing card (`13_s10_close.png`), plus `final_check/` with three stills
across the closing sequence (list + strip still up at 241.5 s, board cleared at
243.3 s, card + goodbye at 244.5 s).

# Production-Ready Storyboard — as built

## Polygons Explained: Sides, Vertices, Adjacent Elements & Diagonals

CLASS 6 MATHEMATICS · CHAPTER 4 (BASIC GEOMETRICAL IDEAS) · STORYMODE 03

**LLM KEY / FUNCTION NAME:** `polygons_sides_vertices_and_diagonals`
**CLASS LEVEL:** Class 6 · **TEXTBOOK:** Telangana SCERT, 6 Maths EM 2025-26,
Chapter 4. A **polygon** is a simple closed figure made from a definite number
of line segments; the chapter then develops **sides** and **vertices** through a
triangle, and **sides, adjacent sides, opposite sides** and **diagonals**
through quadrilateral `ABCD`.

## Learning objective

By the end of the video a student can: define a polygon as a **simple closed
figure made from line segments**; say why an open chain is not a polygon;
recognise that three sides is the smallest number that can close; name the
**sides** and **vertices** of a polygon; identify **adjacent sides** as sides
sharing a vertex; name the **opposite side** and the **opposite vertices** of a
quadrilateral; and draw/naming the two **diagonals** `AC` and `BD`, which join
opposite vertices.

**Primary takeaway:**

**Polygon = simple + closed + line segments** · **Sides form the boundary** ·
**Vertices are the corners** · **Adjacent = sharing a corner** ·
**Diagonals join opposite vertices**

## Core visual metaphor — build the polygon, then reveal its anatomy

One persistent quadrilateral `ABCD` is constructed in front of the learner: the
four straight sides are drawn in order, the boundary is traced, the corner dots
pulse, adjacent parts are highlighted in colour, the opposite parts are shown
across the figure, and finally the two **dashed diagonals** are drawn through
the same shape. Nothing is introduced on a separate static slide.

## Realistic diagrams (production direction)

The figures are drawn with the conventions a textbook illustration uses, using
Manim's own geometry primitives — no image files:

- every polygon carries a **soft interior tint** (`Polygon` fill) so the enclosed
  region reads as a surface, not just an outline;
- **solid vertex dots** sit exactly on the corners, with each capital letter
  offset outward so it never touches a side;
- boundary **sides are thick chalk strokes**; a highlighted side is overlaid in
  its own colour;
- **diagonals are dashed** (`DashedLine`), the standard convention for a line
  that crosses the interior;
- vertices pulse (`Indicate`), the boundary is drawn with `Create`, and the
  construction is paced across its narration window.

## Scene plan (timings are the delivered cut's own)

| # | in | Scene | Key on-screen text | Geometry focus |
|---|---|---|---|---|
| 0 | 0:00 | Title card | side · vertex · diagonal | the three parts |
| 1 | 0:14 | From a closed curve to a polygon | POLYGON = SIMPLE + CLOSED + LINE SEGMENTS | curve → straight boundary |
| 2 | 0:25 | What must a polygon have? | SIMPLE + CLOSED + LINE SEGMENTS | open chain vs triangle |
| 3 | 0:44 | Sides and vertices | SIDES MEET AT VERTICES | triangle ABC |
| 4 | 0:57 | Building quadrilateral ABCD | 4 SIDES · 4 VERTICES | `AB, BC, CD, DA` |
| 5 | 1:10 | Adjacent = next to | ADJACENT = SHARING A CORNER | AB with BC and DA |
| 6 | 1:26 | Across, not next to | OPPOSITE VERTICES: A and C · B and D | CD opposite AB |
| 7 | 1:41 | Diagonals cut across | DIAGONAL = JOIN OPPOSITE VERTICES | dashed `AC`, `BD` |
| 8 | 1:56 | Side or diagonal? | BOUNDARY = SIDE · OPPOSITE VERTICES = DIAGONAL | AB vs AC |
| 9 | 2:12 | YOUR TURN — questions read, then the silent clock | four checks on PQRS | all concepts |
| 10 | 2:58 | Recap, then the spoken thank-you card | KNOW THE PARTS | all concepts |

**Delivered files**

The 360p cut:

    final_videos/PolygonsSidesVerticesDiagonalsStory_captioned.mp4
    640×360, 30 fps, 202.87 s (3 min 23 s), 54 captions
    final_videos/PolygonsSidesVerticesDiagonalsStory_captioned.srt

The 1080p60 master, re-rendered from the same module (the pipeline re-synthesises
the narration, so the cut re-times by a few hundredths of a second; the boarding,
the layout and the word-for-word captions are identical):

    final_videos/1080p/PolygonsSidesVerticesDiagonalsStory_captioned.mp4
    1920×1080, 60 fps, 202.97 s, 12 178 frames, 36.68 MB, 54 captions
    final_videos/1080p/PolygonsSidesVerticesDiagonalsStory_captioned.srt

    verify_sync.py      video 202.967 s, 54 captions, first 0.34 s, last
                        200.97 s, 0 in silence, 0 uncaptioned  -> PASS
    verify_captions.py  narration 461 words = SRT 461 words       -> PASS

`pipeline_1080.py` in this chapter folder produced the master
(render 1920×1080/60 → verify → burn → `final_videos/1080p/`); libass scales the
one caption style with the video height, so the 1080p burn is the 360p burn
three times the size.

The raw renders and their ground-truth SRTs sit in
`media/videos/polygons_sides_vertices_and_diagonals/360p30/` and `…/1080p60/`.

## Revision (second cut): a proper polygon, centred, with one marker style

The first cut was re-cut after a review of two frames, then swept for the same
classes of defect everywhere.

- **The quadrilateral is redrawn from scratch.** It used to be a lopsided figure
  (`A(-1.66,-0.39) B(1.44,-0.39) C(1.73,1.19) D(-1.51,1.19)`, ink centred on
  x ≈ 0.04, top side shifted right over the bottom). It is now a clean,
  symmetric convex trapezium centred on the board axis, larger than before:

      A(-1.35, -0.34)   B(+2.35, -0.34)      bottom side AB = 3.70 wide
      C(+1.55, +1.28)   D(-0.55, +1.28)      top side DC = 2.10, centred over AB

  ink `[-1.35..+2.35]` → **centre +0.500**, height 1.62; the interior is tinted
  (Polygon fill), and the two diagonals cross exactly on the board's centre line
  (midpoints (0.10,0.47) and (0.90,0.47)). The triangle is the same treatment:
  `A(-1.10,-0.34) B(+2.10,-0.34) C(+0.50,+1.28)`, ink centre **+0.500**.
- **One marker style.** `MARK_SIZE = 18`, `LABEL_DX = 0.30`, `LABEL_DY = 0.34`:
  every corner letter sits the same distance outward along its own corner
  diagonal, in every scene (the old offsets ranged 0.26–0.32 across the four
  corners and the letter size was 20). Measured letter boxes: A x[-1.75..-1.55]
  y[-0.77..-0.59], B x[+2.57..+2.73] y[-0.78..-0.58] — 0.25 clear of side AB —
  and C/D 0.30 below the sub-heading. The challenge thumbnails keep the same
  four-marker pattern at a card-sized scale (letters at ±0.20/±0.24, size 13).
- **Curve → polygon** is now one centred row: an 0.85-scale copy of the SAME
  quadrilateral on the right, the oval on the left, and the arrow centred in the
  gap (0.45 of air on each side). Block ink `[-3.52..+4.52]` → **centre +0.497**;
  it used to run `-3.85..+4.80` with the arrow butted against the polygon's
  corner. Both figures keep their own caption ("a smooth closed curve",
  "polygon").
- **Blocks centred everywhere**: the title's three part-columns moved from
  `-2.20, 0, +2.20` (centre 0.0) to `-1.61, +0.43, +2.54` (equal 0.55 air, row
  centre +0.50); the open chain is now symmetric about the origin and placed on
  `BOARD_CX`; the challenge/answers rows use fixed columns (`answer_row`).
- **The parts read**: sides are thick chalk strokes overlaid in their own
  colours (AB cyan, BC yellow, CD pink, DA white), vertex dots are solid, and
  the two diagonals are dashed in their own colours — **AC amber, BD pink** —
  each with its own chip on its own side (the single left-hand "DIAGONAL" chip is
  gone), so the pair is unmistakable and the chips' row is symmetric about the
  board axis.
- **Sync**: the title card's parts are drawn on b0 and *named* on b1, the line
  that names them. The last piece gained a bookmark before "Thank you for
  watching," (and the goodbye mark was renumbered), so the recap list stays on
  the board through the whole closing sentence, the strip is written on its own
  bookmark as the voice says "Know the parts, and you understand the polygon.",
  and only the bookmark in front of "Thank you for watching," clears the board
  and brings in the card. Measured on the rendered cut: the full list plus the
  strip are still up at 196.0 s (the voice is at "you understand the polygon."),
  the board starts clearing at 197.4 s as "Thank you" is spoken (197.46), and the
  card is up by 198.5 s with the goodbye line following at 199.5 s.

*The brief estimated ~3 min 45 s; the delivered cut runs 3 min 23 s. Every
scene from the storyboard is present with its full content and no padding, so
the tighter narration simply reads faster — nothing was dropped.*

## The three production instructions

1. **No overlaps, and proper alignment/positioning.**
   `audit_sync_overlap.py` → **0** out-of-board, text-in-text, text-on-line,
   text-inside-a-foreign-card, near-badge, LaTeX-as-text, empty-TeX and
   **IN-CAPTION-BAND** flags. `audit_clearance.py` → **0 pairs closer than 0.22
   units, 0 text/line collisions, 0 foreign-box collisions**. The quadrilateral
   and triangle are defined once (`QUAD_PTS` / `TRI_PTS`, centred on `BOARD_CX`
   with the one outward label offset) so their corner letters clear both the
   sub-heading above and the banner below, and nothing on the board reaches
   `CAPTION_SAFE_Y = -2.00`.

2. **The YOUR TURN clock: centred on the board, ten seconds, and silent.**
   `story_common.play_challenge_countdown(self, seconds=10, position=(BOARD_CX,
   BOARD_CY))` — the series' shared badge, dead centre of the green board. The
   challenge runs as three movements: the four questions are **read first**
   (2:12.3–2:26.3), the clock then ticks for ten seconds with **no narration
   under it** (only its own tick: measured at −25 dB for every second of the
   window against −6 dB for the answers narration that follows), and the four
   answers follow (2:38.0 onward). The four question cards sit in the four
   corners so the badge never covers one. `find_timer.py` locates the countdown
   window at **147–156 s (10 s** of screen time) and it is centred in
   `frames360/chk/s9_clock.png`.

3. **Realistic diagrams** — see the production direction above: filled polygons,
   solid vertex dots with offset labels, thick chalk sides and dashed diagonals.

## Voice sync (the fourth instruction)

Every reveal waits for the narration bookmark that ends the phrase describing it
and only then plays (`self.wait(leftover(tracker, "bN"))` *before* the play), so
the board can never run ahead of the voice; `closing()` consumes each window's
tail.

`audit_sync_overlap.py` against the rendered audio: **all twelve pieces at
0.00 s stretch** (title 12.55 s, s1 9.94, s2 18.54, s3 11.66, s4 11.57, s5 15.19,
s6 14.25, s7 13.57, s8 15.53, s9q 14.02, s9a 18.62, s10 22.86; total speech
178.30 s inside a 202.86 s video, the rest being the silent clock, the transition
holds and the closing hold), and **0 overlap / clearance flags against the real
cut**.

`verify_sync.py`: 54 captions, first at 0.34 s, last at 200.88 s, **0 captions in
silence, 0 speech blocks uncaptioned** → PASS.
`verify_captions.py`: narration **461 words = SRT 461 words** → PASS (word for
word).

The closing card is **narrated**: the recap clears as the voice says "Thank you
for watching," so the "Thank You for Watching!" card appears *with* the words,
and "See you in the next lesson :)" lands as the voice says "and see you in the
next lesson."; the cut then holds the card for 1.94 s.

## Pedagogical safeguards honoured

- **A polygon must be closed.** Scene 2 shows an open chain of three segments and
  states it is not a polygon yet; only when the ends join does it become one.
- **The boundary must be line segments.** Scene 1 links back to Storymode 02: a
  smooth closed curve becomes a polygon only when its boundary straightens.
- **Sides and vertices are different objects.** Scene 3 separates the three
  line segments (sides) from the three points (vertices) of triangle `ABC`.
- **Adjacent sides must share a vertex.** Scene 5 highlights `AB` with `BC` and
  `AD`; `AB` and `CD` are never called adjacent.
- **"Adjacent vertices" is a vocabulary extension.** Scene 5's strip says
  neighbouring vertices are joined by a side; the video does not attribute that
  wording to the textbook, which defines only adjacent sides here.
- **A diagonal joins opposite vertices**, not any interior segment (scene 7), and
  a diagonal is never part of the boundary (scene 8).
- **No diagonal-count formula.** The `n(n−3)/2` formula is beyond this chapter
  and is deliberately absent.

## Tools in this folder

`assemble_polygons.py` (splices `_polygons_fragment.py` + `_polygons_beats.py`
into the proven video-03 head), `setup_tools.py`, `make_draft_srt.py`,
`tts_precheck.py`, `audit_sync_overlap.py`, `audit_clearance.py`,
`audit_row_columns.py` (are the answers rows' numbers really on one vertical
line?), `scene_frames.py`, `find_timer.py`, and the chapter's `pipeline_360.py`
(render → verify_sync → verify_captions → burn captions → `final_videos/`).

**Frame sweep:** the title, each concept scene, the centred clock, the answers
board, the recap and the closing card are in `frames360/chk/` (the numbered
`01_…`-`12_…` stills from `scene_frames.py` plus the named sweep, including
`s1_polygon.png`, `s7_diagonals.png` and `s10_recap.png`).

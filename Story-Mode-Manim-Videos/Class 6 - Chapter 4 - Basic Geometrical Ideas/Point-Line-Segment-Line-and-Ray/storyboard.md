# Production-Ready Storyboard — as built

## Point, Line Segment, Line & Ray: The Fundamental Building Blocks of Geometry

CLASS 6 MATHEMATICS · CHAPTER 4 (BASIC GEOMETRICAL IDEAS) · STORYMODE 01

**LLM KEY / FUNCTION NAME:** `fundamental_geometric_building_blocks_point_line_ray`
**CLASS LEVEL:** Class 6 · **TEXTBOOK:** Telangana SCERT, 6 Maths EM 2025-26,
Chapter 4. The chapter opens with everyday shapes, then builds the idea of a
point (a location), a line segment (two endpoints, definite length), a line
(endless in both directions) and a ray (one initial point, one endless
direction), and names them with capital letters.

## Learning objective

By the end of the video a student can: say that a **point** marks a location and
is named with a capital letter; name the **two endpoints** of a line segment and
its definite length; describe a **line** as extending endlessly in both
directions (no endpoints); describe a **ray** as starting at an **initial point**
and extending endlessly in one direction (one endpoint); count the endpoints
**2 / 1 / 0** for segment / ray / line; explain why the **first letter names the
starting point** of a ray; and recognise points that lie on the same straight
line.

**Primary takeaway:**

**Point → Location** · **Segment → 2 Endpoints** · **Ray → 1 Endpoint** ·
**Line → 0 Endpoints**

## Core visual metaphor — one object, built step by step

A single point `A` stays alive for the whole video. A second point `B` joins it
(segment, two endpoints); one end is released and drawn on forever (ray, one
endpoint); the other end is released too (line, no endpoints). The endpoint
counter rides from **2 → 1 → 0** beside the same drawing, so the three linear
objects are seen as one evolving idea rather than three separate definitions.

## Scene plan (timings are the delivered cut's own)

| # | in | Scene | On-screen text | Geometry focus |
|---|---|---|---|---|
| 0 | 0:00 | Title card | The four objects + endpoint counts | point · segment · ray · line |
| 1 | 0:12 | Geometry is all around us | Every shape starts with simple ideas | book → screen → rangoli → star → dot/edge/arrow |
| 2 | 0:38 | A point marks a location | POINT = A LOCATION | the pencil dot sharpened smaller and smaller |
| 3 | 1:01 | Join two points: the line segment | 2 ENDPOINTS · definite length | `AB`, the ruler, the shortest path |
| 4 | 1:21 | Extend both ways: the line | NO ENDPOINTS | `AB` endless, A and B as points on the line, `l` |
| 5 | 1:42 | One starting point: the ray | 1 ENDPOINT + 1 DIRECTION | torch → ray `AB`, initial point |
| 6 | 2:05 | The endpoint test | 2 → SEGMENT · 1 → RAY · 0 → LINE | three aligned diagrams, the counters |
| 7 | 2:20 | Points on the same line | SAME STRAIGHT LINE | C–A–B, the two opposite rays from A |
| 8 | 2:41 | Why the order of letters matters | THE FIRST LETTER NAMES THE STARTING POINT | ray OA = ray OB, ray AO ≠ ray OA |
| 9 | 3:06 | YOUR TURN — questions read, then the silent clock | name each diagram, then ray OA vs OB | 4 questions → 10 s THINK → answers |
| 10 | 3:57 | Recap, then the spoken thank-you card | FROM A POINT, GEOMETRY BEGINS | point → segment → ray → line |

**Delivered files**

The 360p cut:

    final_videos/FundamentalGeometricBuildingBlocksStory_captioned.mp4
    640×360, 30 fps, 262.13 s (4 min 22 s), 81 captions
    final_videos/FundamentalGeometricBuildingBlocksStory_captioned.srt

The 1080p60 master, re-rendered from the same module (the pipeline re-synthesises
the narration, so the cut re-times by a few hundredths of a second; the boarding,
the layout and the word-for-word captions are identical):

    final_videos/1080p/FundamentalGeometricBuildingBlocksStory_captioned.mp4
    1920×1080, 60 fps, 262.27 s, 15 736 frames, 46.69 MB, 81 captions
    final_videos/1080p/FundamentalGeometricBuildingBlocksStory_captioned.srt

    verify_sync.py      video 262.267 s, 81 captions, first 0.26 s, last
                        260.27 s, 0 in silence, 0 uncaptioned  -> PASS
    verify_captions.py  narration 699 words = SRT 699 words       -> PASS

`pipeline_1080.py` in this chapter folder produced the master
(render 1920×1080/60 → verify → burn → `final_videos/1080p/`); libass scales the
one caption style with the video height, so the 1080p burn is the 360p burn
three times the size.

The raw renders and their ground-truth SRTs sit in
`media/videos/fundamental_geometric_building_blocks_point_line_ray/360p30/` and
`…/1080p60/`.

## Revision (second cut): centred blocks, real icons, one marker style

The first cut was re-cut after a review of four frames, then swept for the same
classes of defect everywhere. Every diagram row is now centred on `BOARD_CX` and
every point letter uses one size and one offset (`MARK_SIZE = 18`,
`LABEL_DY = 0.34`, always *below* its point):

- **Title card** — the four columns moved from `-3.45 + i·2.30` (row centre 0.0)
  to `row_centres((0.80,·), 0.70)`, i.e. centres **-2.95, -0.65, 1.65, 3.95**:
  the row's ink `[-3.75..+4.75]` is centred on +0.50 with equal 0.70 gaps.
- **Every Shape Starts with Simple Ideas** — both rows re-placed the same way:
  icons at centres **-2.85 … +3.65** (equal 1.30 gaps, footprint-measured because
  the four icons differ in width) at `y = 1.28` with their names at 0.52, and the
  three reductions below centred with equal 1.25 gaps (the point column measured
  by its caption, since its ink is one dot).
- **The icons are real objects now**, built from filled, shaded primitives
  rather than bare outlines: a closed **book** (cream page block, shaded cover,
  spine, three ruled lines, ribbon), a **screen** (dark bezel, lit glass with a
  white sheen, trapezoid neck, base, LED), a **rangoli** (shaded disc, a ring of
  eight alternating petals, two rings, eight dots, a petalled centre) and a
  five-pointed **star** (halo, filled body, inner highlight, four sparkles).
- **One Starting Point: the Ray** — the torch was a bare two-rectangle glyph
  whose beam pointed *up* while the ray went right. It is now a real torch lying
  on its side and pointing right: tapered barrel with a highlight stripe and
  three grip rings, a switch, a flaring head, and a bright lens disc inside a
  two-step glow; `place_torch()` pins it by that lens at the ray's initial point
  and `light_cone()` draws the translucent beam the ray travels in.
- **One Idea, Four Objects** — the four columns moved from `-3.45 + i·2.30` to
  **-2.95 … +3.95** (row centred on +0.50), the picture letters from
  `label_dy = 0.26` to the series' 0.34, and the third text row is no longer one
  centred sentence: it is four entries — *POINT = LOCATION · SEGMENT = 2 ·
  RAY = 1 · LINE = 0* — each sitting under its own column at size 13.
- **Whole-video sweep** — the segment scene (segment, ruler and the "definite
  length" caption all to centre +0.50; the old drawing sat at -0.80 with the
  caption at +2.35), the line scene (A/B centred at -0.80/+1.80, the endless line
  `[-4.30..+5.30]`, the endpoint chip moved from -3.20 to the centre), the
  endpoint test (label | diagram | counter row moved from centre -0.57 to +0.50
  with equal 0.75 air), points-on-one-line (line, points and both rays symmetric
  about A = +0.30, ray names under the ray tips) and the ray-naming scene (the
  three points centred at -2.10/+0.80/+2.80). The point scene's dot-vs-idea
  comparison is centred as a block, its notes dropped to 0.42 and its A/B/C row
  raised to -0.35 so nothing comes within 0.22 of the banner. `answer_row()`
  now lays its tag/name/note in fixed columns (measured: every one of A, B, C, D
  starts at 165 px = board -3.44 with an 18 px gap to its name).
- The light beam's cone is sized (0.13 → 0.90 half-height) so its edges clear
  every caption and the sub-heading; the closing Indicate was trimmed to 1.10 s
  so the last piece reports **0.00 s stretch** (it was 0.04).

## The two production instructions

1. **No overlaps, and proper alignment/positioning.**
   `audit_sync_overlap.py` → **0** out-of-board, text-in-text, text-on-line,
   text-inside-a-foreign-card, near-badge, LaTeX-as-text, empty-TeX and
   **IN-CAPTION-BAND** flags. `audit_clearance.py` → **0 pairs closer than 0.22
   units, 0 text/line collisions, 0 foreign-box collisions**. Every heading sits
   on the board's heading line, every diagram is pinned with `place_line`/`at`
   so two pictograms on one row line up exactly, and the whole board stays above
   `CAPTION_SAFE_Y = -2.00` (nothing reaches the burned caption band).

2. **The YOUR TURN clock: centred on the board, ten seconds, and silent.**
   `story_common.play_challenge_countdown(self, seconds=10, position=(BOARD_CX,
   BOARD_CY))` — the series' shared badge, dead centre of the green board. The
   challenge runs as three movements: the four questions are **read first**
   (3:05.7–3:24.3), the clock then ticks for ten seconds with **no narration
   under it** (only its own tick, measured at −25 dB against −5 dB for the
   narration around it), and the four answers follow (3:35.6 onward). The four
   question cards sit in the four corners so the badge never covers one.
   `find_timer.py` locates the countdown window at **205–214 s (10 s** of screen
   time) and it is verified centred in `frames360/chk/s9_clock.png`.

## Voice sync (the third instruction)

Every reveal waits for the narration bookmark that ends the phrase describing it
and only then plays (`self.wait(leftover(tracker, "bN"))` *before* the play), so
the board can never run ahead of the voice; `closing()` consumes each window's
tail.

`audit_sync_overlap.py` against the rendered audio: **all twelve pieces at
0.00 s stretch** (title 10.66 s, s1 25.28, s2 21.96, s3 19.59, s4 20.04, s5 21.18,
s6 14.41, s7 19.94, s8 23.77, s9q 18.56, s9a 20.64, s10 22.70; total speech
238.73 s inside a 262.12 s video, the rest being the silent clock, the transition
holds and the closing hold).

`verify_sync.py`: 81 captions, first at 0.26 s, last at 260.15 s, **0 captions in
silence, 0 speech blocks uncaptioned** → PASS.
`verify_captions.py`: narration **699 words = SRT 699 words** → PASS (word for
word).

The closing card is **narrated**: the recap clears as the voice says "Thank you
for watching," so the "Thank You for Watching!" card appears *with* the words,
and "See you in the next lesson :)" lands as the voice says "and see you in the
next lesson."; the cut then holds the card for 1.94 s.

## Pedagogical safeguards honoured

- **A point is not a tiny circle with size.** The pencil dot is shown shrinking
  smaller and smaller, and the narration says "we keep the idea, not the ink —
  a point marks a location and has no size at all."
- **A and B are not endpoints of a line.** Scene 4 extends the segment beyond
  both points and states that A and B become points lying *on* the line; only
  the segment's ends are called endpoints.
- **Only the line segment has a definite length.** The ruler appears once, in
  scene 3, on the segment; the ray and the line "go on forever".
- **Ray direction matters.** Scene 8 shows ray OA = ray OB (same start, same
  direction) but ray AO ≠ ray OA (the first letter names the starting point).
- **"Points on the same line", not "collinear".** The textbook section does not
  define the term *collinear*, so the on-screen wording stays source-faithful.
- **Intersecting and parallel lines are out of scope.** They are introduced in
  Chapter 5 (Measures of Lines and Angles), so this Chapter 4 video does not
  teach them.
- **Object identity.** One persistent point A is reused across every scene, so
  the segment, the ray and the line are visibly built from the same objects.

## Tools in this folder

`assemble_point_line_ray.py` (splices `_plr_fragment.py` + `_plr_beats.py` into
the proven video-03 head), `setup_tools.py`, `make_draft_srt.py`,
`tts_precheck.py`, `audit_sync_overlap.py`, `audit_clearance.py`,
`audit_row_columns.py` (are the answer rows' letters really on one vertical
line?), `scene_frames.py`, `find_timer.py`, and the chapter's `pipeline_360.py`
(render → verify_sync → verify_captions → burn captions → `final_videos/`).

**Frame sweep:** the title, each concept scene, the centred clock, the answers
board, the recap and the closing card are in `frames360/chk/` (the numbered
`01_…`-`12_…` stills from `scene_frames.py` plus the named sweep).

# Production-Ready Storyboard — as built

## 2.7 Geometric Applications: Angles & Parallel Lines
### The Six Relationships, and the Equations They Give

**LLM KEY / FUNCTION NAME:** `parallel_lines_and_angles`
**MODULE:** `parallel_lines_and_angles.py` · **CLASS:** `ParallelLinesAndAnglesStory`
**CHAPTER:** Chapter 2 — Linear Equations in One Variable · **CLASS LEVEL:** Class 8
**TEXTBOOK SECTION:** 2.7 Geometric Applications: Angles & Parallel Lines
**DELIVERED:** 5 min 13 s (312.76 s), 640×360, 30 fps, 96 captions — **one video**

*Restructured: this is now a single lesson. The old two-part arrangement (an
earlier `geometry_angles_story` cut followed by the six-relationship cut) has
been rebuilt into one continuous video with one title, one thread and one
closing card, and **all of the earlier renders have been removed**.*

## Learning objective

By the end of the video a student can: say what a **transversal** does to two
**parallel lines**; point to the **eight angles** it makes and name the four
**interior** and four **exterior** angles; state and use **all six
relationships**; and run the section's routine — **identify the pair → write the
rule → form the equation → solve → put the value back into the diagram** — on a
same-side interior pair (`x = 21`, 83° and 97°) and on a corresponding pair
(`x = 8`, 40° and 40°).

**Primary takeaway**

| Relationship | Angles | Rule | Colour |
|---|---|---|---|
| Corresponding | 1 = 5, 2 = 6, 3 = 7, 4 = 8 | **equal** | pink |
| Alternate interior | 4 = 5, 3 = 6 | **equal** | red |
| Alternate exterior | 2 = 7, 1 = 8 | **equal** | cyan |
| Vertically opposite | 1 = 4, 2 = 3, 5 = 8, 6 = 7 | **equal** | violet |
| Same-side interior | 3 + 5, 4 + 6 | **add to 180°** | green |
| Same-side exterior | 1 + 7, 2 + 8 | **add to 180°** | yellow |

*A **linear pair** — two angles side by side on a straight line — always adds to
180°, and that is what makes the two same-side rules true.*

## Core visual metaphor — one figure, six lights, one routine

Two parallel lines, each carrying the same chevron arrow mark, are cut by one
transversal; that single figure is never redrawn. Each relationship is revealed
by **changing only the emphasis**: the pair of wedges is lit in its own rule
colour while the other six arcs stay pale, and the rule is written in the
right-hand column. The eight numbers stay in place the whole time, so the learner
always knows which angles are being discussed. The last two teaching scenes then
walk the same figure through the section's routine twice — once where the rule
gives a **sum** equal to 180, once where it gives an **equality** — so the
student sees that the geometry decides the equation.

## Realistic diagrams (production direction)

The figure is drawn with the conventions a textbook illustration uses, using
Manim's own geometry primitives — no image files:

- the two parallel lines carry the **same chevron arrow mark**, the standard sign
  for "these are parallel";
- the transversal is long enough to **stick out past both lines** on each side;
- **every angle is a real wedge**: a translucent `Sector` with its own arc, so
  "the angle between these two lines" is a visible region, not an abstract
  corner — the pair being discussed is filled at 0.38 opacity in its rule colour;
- the **interior gets a translucent band** between the two lines (a `Polygon`, so
  the parallel lines are never "inside a box");
- the **eight numbers** sit on the bisector of their own wedge, clear of both
  lines that bound it and clear of the arc;
- the construction is drawn with `Create`, pairs are picked out with a colour
  fill, and the work is paced across its narration window.

## Scene plan (timings are the delivered cut's own)

| # | in | Scene | On-screen rule / text | Content |
|---|---|---|---|---|
| 0 | 0:00 | Title card | 8 angles · 6 relationships · 1 equation | the promise |
| 1 | 0:10 | Parallel lines and a transversal | ONE LINE CROSSES TWO PARALLEL LINES | the words and the marks |
| 2 | 0:29 | Eight angles, two regions | INTERIOR 3,4,5,6 · EXTERIOR 1,2,7,8 | the eight numbers |
| 3 | 0:52 | Vertically opposite and linear pairs | VERTICALLY OPPOSITE ANGLES ARE EQUAL | 1 = 4, and 1 + 2 = 180 |
| 4 | 1:09 | Corresponding angles | CORRESPONDING ANGLES ARE EQUAL | 1=5, 2=6, 3=7, 4=8 |
| 5 | 1:29 | Alternate interior angles | ALTERNATE INTERIOR ANGLES ARE EQUAL | 4=5, 3=6 |
| 6 | 1:50 | Same-side interior angles | SAME-SIDE INTERIOR ANGLES ADD TO 180 | 3+5, 4+6 |
| 7 | 2:11 | The two exterior rules | EXTERIOR PAIRS: EQUAL OR 180 | 2=7, 1=8; 1+7, 2+8 = 180 |
| 8 | 2:42 | The routine, on a same-side interior pair | (3x+20)+(5x−8)=180 → x = 21 | 83° and 97°, with the eight angles numbered on the figure |
| 9 | 3:20 | The same routine, on a corresponding pair | 5x = 2x+24 → x = 8 | 40° and 40° |
| 10 | 3:48 | YOUR TURN — questions read, then the silent clock | four checks | name the pair, then find x |
| 11 | 4:23 | The four answers | A corresponding · B alternate interior · C same-side interior · D x = 40 | all six rules |
| 12 | 4:45 | The six relationships, then the spoken thank-you | six rows, each with its own picture | recap |

**Delivered file**

    final_videos/ParallelLinesAndAnglesStory_captioned.mp4
    640×360, 30 fps, 312.76 s (5 min 13 s), 96 captions, 12.22 MB
    final_videos/ParallelLinesAndAnglesStory_captioned.srt

The raw render and its ground-truth SRT sit in
`media/videos/parallel_lines_and_angles/360p30/`. The earlier cuts — the
`geometry_angles_story` renders (360p and 1080p) and the merged two-part file —
have been **deleted**; nothing stale is left in the topic.

## The three production instructions

1. **No overlaps, and proper alignment/positioning.**
   `audit_sync_overlap.py` against the rendered audio → **0** out-of-board,
   text-in-text, text-on-arc, text-on-line, text-inside-a-foreign-card,
   near-badge, empty-TeX, LaTeX-as-text and **IN-CAPTION-BAND** flags.
   `audit_clearance.py` → **0 pairs closer than 0.22 units, 0 text/line
   collisions, 0 foreign-box collisions**. The figure is built from fixed,
   audited coordinates (`PAR_Y1`, `PAR_Y2`, `TRA_TOP`, `TRA_BOT`) so every scene
   draws the same lines; the lines sit high enough, and the transversal stops
   early enough, that no closing banner is ever crossed by a chalk line; the
   eight numbers sit inside their own wedges, clear of both bounding lines and of
   the arc; every rule lives in the right-hand column (`COL_X = 3.60`), so
   nothing is written across the figure; nothing on the board reaches
   `CAPTION_SAFE_Y = -2.00`. (Both audits were run on the draft *and* on the
   rendered cut: 0 flags each time.)
2. **The YOUR TURN clock: centred on the board, ten seconds, and silent.**
   `story_common.play_challenge_countdown(self, seconds=10, position=(BOARD_CX,
   BOARD_CY))` — the series' shared badge, dead centre of the green board, with
   the four question cards in the four corners. The challenge runs as three
   movements: the four questions are **read first** (3:48.6–4:12.5, 23.83 s of
   narration), the clock then ticks for ten seconds with **no narration under
   it** (4:13.0–4:23.0), and the four answers follow (4:23.7 onward).
   Per-second `volumedetect`: **−25.1 / −25.2 dB** (the tick alone) for every
   whole second `254 … 262`, with digital silence (−91 dB) at 253 and the answers
   narration at **−6.6 dB** just after. `find_timer.py` locates the countdown
   window at **253 s → 262 s (10 s** of screen time) and it is centred in
   `frames360/chk/zz_timer_mid.png` (showing `THINK 6S` at the middle of the
   board).
3. **Realistic diagrams** — see the production direction above: chevron-marked
   parallel lines, a transversal that overshoots both, eight real translucent
   wedges with arcs, the interior band, and colour fills that light only the pair
   under discussion.

## Voice sync (the fourth instruction)

Every reveal waits for the narration bookmark that ends the phrase describing it
and only then plays (`self.wait(leftover(tracker, "bN"))` *before* the play), so
the board can never run ahead of the voice; `closing()` consumes each window's
tail.

`audit_sync_overlap.py` against the rendered audio: **all thirteen pieces at
0.00 s stretch** (title 9.41 s, s1 17.75, s2 22.02, s3 15.23, s4 19.04, s5 20.13,
s6 20.13, s7 30.71, s8 37.25, s9 26.85, s9q 23.83, s9a 20.48, s10 25.24; total
speech **288.07 s inside a 312.66 s video**, the rest being the 10 s silent
clock, the transition holds and the closing hold), and **0 overlap / clearance
flags against the real cut**.

`verify_sync.py`: video 312.757 s, audio 310.635 s, silent tail +2.122 s [ok],
**96 captions**, first at 0.36 s, last at 310.61 s, **0 captions in silence,
0 speech blocks (> 1.0 s) uncaptioned** → PASS.
`verify_captions.py`: narration **840 words = SRT 840 words** → PASS (word for
word).

Delivered voice windows: title 0.36 · s1 10.90 · s2 29.86 · s3 52.91 · s4 69.03 ·
s5 89.06 · s6 110.18 · s7 131.29 · s8 162.71 · s9 200.84 · s9q 228.63 (questions
read, then the clock) · s9a 263.69 · s10 285.06 — the cut ends at 312.66 s.

The last scene is cut to the voice in three separate windows, so nothing runs
early: the strip "Geometry gives the rule, and the equation finds x." appears on
its own bookmark (5:04.3, with the six rows still on the board), the thank-you
card replaces the recap exactly as the voice says **"Thank you for watching,"**
(5:07.5), and "See you in the next lesson :)" fades in with **"and see you in
the next lesson."** (5:09.4, caption 96 ending 5:10.61). The voice then stops and
the cut holds the finished card for **2.12 s** of silence.

## Pedagogical safeguards honoured

- **Naming first.** Scene 1 defines *parallel* (never meet, marked with the same
  arrow) and *transversal* (cuts across) before any relationship is named.
- **Interior and exterior are fixed by the picture, not by the rule.** Scene 2
  numbers the eight angles and tints the band between the lines, so 3, 4, 5, 6
  are the interior angles and 1, 2, 7, 8 the exterior ones — every later rule
  refers back to those same numbers.
- **Equal and "add to 180" are never confused.** The four equal rules are drawn
  in one family of colours, the two supplementary rules in another, and the words
  on the banner always say which is which. A linear pair is taught first, because
  it is what makes the same-side rules true.
- **A relationship is never asserted without the parallel condition.** The
  transversal alone does not make corresponding angles equal; every rule on the
  board is stated as "because the two lines are parallel".
- **The equation is never written before the rule.** In scene 8 the pair is
  identified, the rule is stated, and only then is the equation formed; in scene
  9 the equality of corresponding angles produces `5x = 2x + 24`. The same
  five-step routine is spoken in both scenes, so the method — not the answer — is
  what the student takes away.
- **`x` is not the angle.** Each worked example puts the value back into the
  diagram and reports the angles (`83°` and `97°`, adding to 180; `40°` and
  `40°`, equal), and checks the rule.
- **The challenge checks recognition, not memory of numbers.** The three picture
  cards require the student to recognise the *position* of a pair, and the last
  card is a genuine equation to solve (`x = 40`, both angles 90°).

## Tools in this folder

`assemble_pangles.py` (splices `_pangles_fragment.py` + `_pangles_beats.py` into
the proven video-03 head), `setup_tools.py`, `make_draft_srt.py`,
`tts_precheck.py`, `audit_sync_overlap.py`, `audit_clearance.py`,
`scene_frames.py`, `find_timer.py`, and the chapter's `pipeline_360.py`
(render → verify_sync → verify_captions → burn captions → `final_videos/`).
The first version of this topic survives only as source
(`geometry_angles_story.py`, `storyboard-legacy.md`); its renders are gone.

**Frame sweep:** `frames360/chk/` holds the title, the two definition scenes, the
five rule scenes (`04_s3` … `08_s7`), both routine scenes (`09_s8`, `10_s9`), the
centred clock at mid-countdown (`zz_timer_mid.png`), the challenge board
(`11_s9q`), the answers board (`12_s9a`) and the six-rule recap (`13_s10`).

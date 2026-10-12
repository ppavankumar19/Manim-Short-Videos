# Production-Ready Storyboard

> **Revision (this cut).** Four review changes were applied and re-rendered:
> (1) scene 1 now shows a **real door** (wall, jamb, a panel with its knob,
> the threshold and its swing + angle arcs) and a **real clock** (rim, twelve
> hour marks, two hands, centre pin), placed symmetrically about the board's
> centre line; (2) the title card's *vertex* and *arms* labels sit close to
> the figure they name; (3) the four **YOUR TURN diagrams are larger**, on
> equal, symmetric rows; (4) the closing scene is cut to the voice in three
> windows -- the recap stays on the board through the whole "interior,
> boundary, exterior" sentence, the closing strip joins it on "Build, name,
> locate.", and only on **"Thank you for watching,"** does the thank-you
> card replace the recap, with the goodbye line landing on "and see you in
> the next lesson." No earlier sentence is cut off any more.

> **Second review pass.** (5) The door is now drawn as a real door in
> perspective -- frame (jambs + lintel), the leaf with two raised panels, a knob,
> two hinges, the floor line and its sweep + angle arcs (the leaf is a Polygon,
> so the layout audit never reads a door part as a card); (6) the angle scenes
> sit 0.12 lower on the board, with the banner and the strip moved down to match,
> so figure + banner + strip read as one block; (7) every revealed row -- the
> four YOUR TURN answers and the four recap rows -- now uses one fixed-column
> layout (letter, sentence, note), all starting at the same x with identical
> spacing.
 — as built

## Angles Explained: Vertex, Arms and Angle Regions

CLASS 6 MATHEMATICS · CHAPTER 4 (BASIC GEOMETRICAL IDEAS) · STORYMODE 04

**LLM KEY / FUNCTION NAME:** `angles_vertex_arms_and_regions`
**CLASS LEVEL:** Class 6 · **TEXTBOOK:** Telangana SCERT, 6 Maths EM 2025-26,
Chapter 4. An **angle** is made by **two rays with a common endpoint**; the
chapter then names its parts — the **vertex** (the common endpoint) and the
**arms** (the two rays, also called the sides) — shows how an angle is **named
with three letters, the vertex in the middle**, and that an angle **separates
the plane into interior, boundary and exterior**.

## Learning objective

By the end of the video a student can: say that an **angle is two rays from one
common endpoint**; point out the real angles in a door opening and in a clock's
hands; name the **vertex** and the **two arms** of an angle; **name an angle with
three letters putting the vertex in the middle** (`∠AOB = ∠BOA`, never `∠OAB`);
read the **interior** of an angle as the region between the arms; and place any
point of the plane as **interior, on the boundary, or exterior**.

**Primary takeaway:**

**2 rays + 1 common endpoint = angle** · **Vertex = the common endpoint** ·
**Arms = the two rays** · **Three-letter name: vertex in the middle** ·
**Interior · boundary · exterior**

## Core visual metaphor — one angle, taken apart

A single angle `AOB` is built in front of the learner and never replaced: the
vertex dot is placed, the two **arrowed chalk rays** are drawn from it, the
amber **mark arc** appears in the opening, and then every new idea works on that
same figure — the parts are labelled, the naming rule is written beside the same
angle, the **interior is tinted** (`Sector` wedge), the arms light up as the
**boundary**, and points `M`, `N`, `T` are dropped into the three regions.
Nothing is introduced on a separate static slide.

## Realistic diagrams (production direction)

The figures are drawn with the conventions a textbook illustration uses, using
Manim's own geometry primitives — no image files:

- the **rays are real arrows** (`Arrow`, thick chalk strokes, `RAY_W = 4.2`) so
  "ray" reads as "goes on for ever in one direction";
- a **soft amber interior tint** (`Sector`, `fill_opacity` ≈ 0.15) fills the
  opening between the arms, so the angle reads as a region, not just two lines;
- the **mark arc** (`Arc`, `MARK_R = 0.88`) sits in the opening exactly where a
  textbook puts the angle mark, and is kept small so it never runs under a
  letter;
- **solid vertex dots** (`Dot`, `DOT_R = 0.078`) sit exactly on the vertex and on
  every labelled point, with each capital letter offset outward so it never
  touches a ray;
- the `A`/`B`/`O` letters are drawn just outside the ray heads, and every angle
  name is typeset in chalk maths (`chalk_math(r"\angle AOB")`), not as a text
  glyph;
- the tick ✓ and cross ✗ of the naming table are **drawn strokes**
  (`mark_yes` / `mark_no`), not font characters;
- concepts are animated in place: `Create` for the rays, `Rotate` for the door
  and the clock hands, `Indicate` on the figures that are being picked out, and
  the whole construction is paced across its narration window.

## Scene plan (timings are the delivered cut's own)

| # | in | Scene | Key on-screen text | Geometry focus |
|---|---|---|---|---|
| 0 | 0:00 | Title card | Vertex · Arms · Angle Regions | the three parts |
| 1 | 0:14 | What makes an angle? | AN ANGLE APPEARS | door, clock → two rays |
| 2 | 0:32 | Two rays form an angle | 2 RAYS + 1 ENDPOINT = ANGLE | `∠AOB` on the figure |
| 3 | 0:52 | Vertex and arms | VERTEX · ARM 1 · OA · ARM 2 · OB | the named parts |
| 4 | 1:08 | The middle letter | `∠AOB ✓ ∠BOA ✓ ∠OAB ✗ ∠ABO ✗` | the naming rule |
| 5 | 1:31 | Same angle, two names | `∠AOB = ∠BOA` · "angle O" | reversing the arms |
| 6 | 1:45 | The interior | INTERIOR = BETWEEN THE ARMS | tinted opening, point X |
| 7 | 2:01 | Boundary and exterior | INTERIOR · BOUNDARY · EXTERIOR | `S` on an arm, `Z` outside |
| 8 | 2:18 | Where does each point belong? | M · INTERIOR, N · BOUNDARY, T · EXTERIOR | angle `PQR`, three regions |
| 9 | 2:36 | YOUR TURN — questions read, then the silent clock | four checks | all concepts |
| 10 | 3:06 | The four answers | A vertex `O` · arms `OC`,`OD` … | all concepts |
| 11 | 3:34 | Recap, then the spoken thank-you card | BUILD · NAME · LOCATE | all concepts |

**Delivered files**

The 360p cut:

    final_videos/AnglesVertexArmsRegionsStory_captioned.mp4
    640×360, 30 fps, 241.47 s (4 min 01 s), 71 captions
    final_videos/AnglesVertexArmsRegionsStory_captioned.srt

The 1080p60 master, re-rendered from the same module (the pipeline re-synthesises
the narration, so the cut re-times by a few hundredths of a second; the boarding,
the layout and the word-for-word captions are identical):

    final_videos/1080p/AnglesVertexArmsRegionsStory_captioned.mp4
    1920×1080, 60 fps, 241.27 s, 14 476 frames, 43.38 MB, 71 captions
    final_videos/1080p/AnglesVertexArmsRegionsStory_captioned.srt

    verify_sync.py      video 241.267 s, 71 captions, first 0.18 s, last
                        239.34 s, 0 in silence, 0 uncaptioned  -> PASS
    verify_captions.py  narration 615 words = SRT 615 words       -> PASS

`pipeline_1080.py` in this chapter folder produced the master
(render 1920×1080/60 → verify → burn → `final_videos/1080p/`); libass scales the
one caption style with the video height, so the 1080p burn is the 360p burn
three times the size.

The raw renders and their ground-truth SRTs sit in
`media/videos/angles_vertex_arms_and_regions/360p30/` and `…/1080p60/`.

## The three production instructions

1. **No overlaps, and proper alignment/positioning.**
   `audit_sync_overlap.py` → **0** out-of-board, text-in-text, text-on-line,
   text-inside-a-foreign-card, near-badge, LaTeX-as-text, empty-TeX and
   **IN-CAPTION-BAND** flags. `audit_clearance.py` → **0 pairs closer than 0.22
   units, 0 text/line collisions, 0 foreign-box collisions**. The angle is built
   from fixed, audited coordinates (`O_PT`, `A_PT`, `B_PT`, `MARK_R`) so the
   letter `A` clears the sub-heading above and `B` clears the banner below; the
   four challenge cards were re-sized (`q_card(pad=0.14, buff=0.26)`,
   `ask_card(line_size=12)`, `mini_angle` arms 0.72/0.64) so the 2×2 grid fits
   inside the board with the centre free for the clock, and nothing on the board
   reaches `CAPTION_SAFE_Y = -2.00`.

2. **The YOUR TURN clock: centred on the board, ten seconds, and silent.**
   `story_common.play_challenge_countdown(self, seconds=10, position=(BOARD_CX,
   BOARD_CY))` — the series' shared badge, dead centre of the green board
   (board centre `(0.5, 0.20)` → pixel ≈ (342, 171) of 640×360), with the four
   question cards in the four corners of the board so the badge covers none of
   them. The challenge runs as three movements: the four questions are **read
   first** (2:36.5–2:55.0, 18.49 s of narration), the clock then ticks for ten
   seconds with **no narration under it** (2:55.0–3:05.0), and the four answers
   follow (3:05.1 onward). Per-second `volumedetect`: **−25.2 dB** (the tick
   alone) for every whole second `176 … 185`, against **−8.1 dB** for the
   answers narration either side, and digital silence (−91 dB) 0.5 s before the
   first tick. `find_timer.py` locates the countdown window at
   **175 s → 185 s (10 s** of screen time) and it is centred in
   `frames360/chk/zz_timer_mid.png`.

3. **Realistic diagrams** — see the production direction above: arrowed chalk
   rays, a tinted interior wedge, a textbook mark arc, solid vertex dots with
   offset letters, drawn ✓/✗ marks and in-place `Create`/`Rotate`/`Indicate`
   animation.

## Voice sync (the fourth instruction)

Every reveal waits for the narration bookmark that ends the phrase describing it
and only then plays (`self.wait(leftover(tracker, "bN"))` *before* the play), so
the board can never run ahead of the voice; `closing()` consumes each window's
tail.

`audit_sync_overlap.py` against the rendered audio: **all twelve pieces at
0.00 s stretch** (title 13.37 s, s1 17.34, s2 18.54, s3 15.39, s4 21.96,
s5 13.09, s6 14.23, s7 16.49, s8 16.73, s9q 18.49, s9a 27.09, s10 24.64; total
speech **217.36 s inside a 241.26 s video**, the rest being the 10 s silent
clock, the transition holds and the closing hold), and **0 overlap / clearance
flags against the real cut**.

`verify_sync.py`: video 241.260 s, audio 239.296 s, silent tail +1.964 s [ok],
**71 captions**, first at 0.18 s, last at 239.27 s, speech blocks 80 (187.3 s of
speech), **0 captions in silence, 0 speech blocks (> 1.0 s) uncaptioned** →
PASS.
`verify_captions.py`: narration **615 words = SRT 615 words** → PASS (word for
word).

Delivered voice windows (`scene_frames.py`, one hold frame per scene):
title 0.18–14.63 · s1 14.63–32.79 · s2 32.79–52.51 · s3 52.51–68.98 ·
s4 68.98–91.94 · s5 91.94–105.84 · s6 105.84–121.13 · s7 121.13–138.69 ·
s8 138.69–156.47 · s9q 156.47–186.25 (questions read, then the clock) ·
s9a 186.25–214.36 · s10 214.36–241.26.

The closing card is **narrated**: the recap clears as the voice says "Build,
name, locate. Thank you for watching," so the "Thank You for Watching!" card
appears *with* the words, and "See you in the next lesson :)" lands as the voice
says "and see you in the next lesson."; the cut then holds the card for 1.96 s
(captions 70–71, ending 3:59.27).

## Pedagogical safeguards honoured

- **An angle is rays, not segments.** Scenes 1–2 keep the two directions and
  show them as **arrowed rays from one point**; the door and the clock hands are
  only used to *motivate* the opening, then removed so the figure on the board is
  the mathematical object.
- **The vertex is one point, the arms are two rays.** Scene 3 labels the three
  objects separately (`VERTEX` at `O`, `ARM 1 · OA`, `ARM 2 · OB`) and notes that
  the arms are "also called sides".
- **Naming rule is mechanical, and checked both ways.** Scene 4 accepts `∠AOB`
  and `∠BOA` (same angle) and rejects `∠OAB` and `∠ABO`, because in both the
  middle letter is not the vertex; scene 5 adds the shortcut name "angle O" and
  states it is safe **only when there is a single angle at that vertex**.
- **Interior is a region, not a line.** Scene 6 tints the opening between the
  arms and lets the point `X` sit *between* the arms; scene 7 then separates
  **interior / boundary / exterior** (point `S` on an arm is on the boundary,
  point `Z` outside the opening is exterior) and states the three-part split of
  the plane.
- **Measure and classification are out of scope here.** Degrees, and acute /
  right / obtuse, belong to Chapter 5 and are deliberately absent; so are
  intersecting and parallel lines.
- **The three regions are exhaustive.** Scene 8 closes the idea with "every other
  point lies in one of the three regions", and the challenge's third answer
  repeats it as `M interior · N boundary · T exterior`.

## Tools in this folder

`assemble_angles.py` (splices `_angles_fragment.py` + `_angles_beats.py` into
the proven video-03 head), `setup_tools.py`, `make_draft_srt.py`,
`tts_precheck.py`, `audit_sync_overlap.py`, `audit_clearance.py`,
`scene_frames.py`, `find_timer.py`, and the chapter's `pipeline_360.py`
(render → verify_sync → verify_captions → burn captions → `final_videos/`).

**Frame sweep:** `frames360/chk/` holds the title, each concept scene
(`01_title` … `09_s8`), the centred clock at mid-countdown (`zz_timer_mid.png`,
showing `THINK 5S` dead centre), the answers board (`11_s9a`) and the closing
card (`12_s10`).

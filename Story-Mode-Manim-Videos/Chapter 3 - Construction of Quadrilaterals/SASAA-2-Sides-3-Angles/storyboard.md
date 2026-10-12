# Production-Ready Storyboard

**VIDEO TITLE:** How to Construct a Quadrilateral Given 2 Adjacent Sides and
3 Angles (S.A.S.A.A Method)
**TOPIC:** Construction of a Quadrilateral from Two Adjacent Sides and Three
Angles
**CLASS / CHAPTER:** Class 8 Mathematics — Chapter 3 — Construction of
Quadrilaterals
**STORYMODE:** 05 (fifth video of the Class 8 Chapter 3 set)
**LLM KEY / FUNCTION NAME:** `construct_quadrilateral_2sides_3angles`
**DURATION (measured):** 3 min 44 s (224.3 s) — 360p30 delivered with captions
burned in, 69 captions / 598 words
**TEXTBOOK REFERENCE:** Telangana SCERT, Class VIII Mathematics (English
Medium), 2025–26 edition, Chapter 3 — Construction of Quadrilaterals:
"Construction: when the lengths of two adjacent sides and three angles are
known (S.A.S.A.A)", **Example 6** (`P Q = 4`, `Q R = 4.8`, `∠P = 75°`,
`∠Q = 100°`, `∠R = 120°`), with a model-created practice quadrilateral
(`A B = 5`, `B C = 4`, `∠A = 70°`, `∠B = 110°`, `∠C = 120°`) as the student
challenge.

---

## Learning Objective

By the end of this video, students should be able to:

- Recognise the data pattern: **two adjacent sides and three angles**.
- See that the two sides must be **adjacent**, and identify the angle
  **between** them (`∠Q`).
- Build the first triangle by **S.A.S** — two sides and the included angle.
- Use the remaining two angles to draw **two rays**, one from each end of the
  known side.
- Locate the fourth vertex at the **crossing of those rays** and complete the
  quadrilateral.
- Verify all five given measurements, and understand that `P S` and `R S` were
  never given — the construction produced them.
- Apply the same strategy to a new set of labels and measurements.

**Primary takeaway:** side–angle–side builds the first triangle; the other two
angles are two directions whose crossing is the fourth vertex. *3 build,
2 locate.*

## Why Angles Locate Differently from Distances

Videos 2–4 of this chapter all located the last vertex with **two compass
arcs**, because the data were distances. Here two of the five measurements are
**angles**, and an angle carries no length — only a direction:

```
        S                          triangle PQR:  PQ = 4, angle Q = 100, QR = 4.8
       / \                         built first, by S.A.S
      /   \                        then:  ray from P at 75 degrees to P Q
     /     \                             ray from R at 120 degrees to R Q
    P-------Q   R                  their crossing is S
```

So the video's second stage changes its visual language:

| data | what locates the last vertex |
|---|---|
| distances (videos 2–4) | two compass **arcs** crossing |
| angles (this video) | two **rays** crossing |

## The figure is constructed, not sketched

`example_construction()` and `practice_construction()` build both figures the
way the construction builds them — the S.A.S triangle first, then the crossing
of the two rays — so each drawing satisfies its data exactly:

| figure | given | how the point is found | measured off the render |
|---|---|---|---|
| Example 6 | `P Q = 4` | the base, drawn level | 4.000 |
| Example 6 | `∠Q = 100°`, `Q R = 4.8` | `R` on the ray set out from `Q P` | 100.00°, 4.800 |
| Example 6 | `∠P = 75°`, `∠R = 120°` | the two rays `P → S` and `R → S` cross at `S` | 75.00°, 120.00° |
| Example 6 | `P S`, `R S`, `∠S` | never given — produced by the construction | 7.424, 3.802, 65.00° |
| practice | `A B = 5`, `B C = 4` | base and the ray at `∠B` | 5.000, 4.000 |
| practice | `∠A = 70°`, `∠C = 120°` | their rays cross at `D` | 70.00°, 120.00° |
| practice | `∠D` | produced by the construction | 60.00° |

`probe_layout.py` re-measures every one of those values from the constructed
vertices before a render is spent, checks the board bounds of the figure and its
letters, and confirms the 60° compass steps: both chords come back exactly equal
to the compass opening.

## Mathematical Content

| Concept | Statement | Shown as |
|---|---|---|
| The data pattern | 2 adjacent sides + 3 angles | two side cards, three angle cards, boxed `S.A.S.A.A` |
| Which three to use | `P Q`, `∠Q`, `Q R` | the two sides and the included angle highlighted, the other two angles moved to a "USE LATER" panel |
| The plan | 3 measurements build, 2 locate | BUILD / LOCATE columns, "3 Build. 2 Locate." |
| Setting out `100°` at `Q` | a protractor on `Q P` | the protractor is laid on the base and the graduation marked |
| Fixing `R` | `Q R = 4.8` along that ray | compasses carry the length from the card to the ray |
| Setting out `75°` at `P` | the first direction for `S` | an arm swings from `P Q` to `75°`, the arc growing under it |
| The `75°` shortcut | half way between `60°` and `90°` | a compact inset showing both standard angles and the bisector |
| Setting out `120°` at `R` | the standard construction | arc about `R`, then the same opening stepped round twice |
| Locating `S` | two directions agree | the two rays cross, pulsing dot and letter |
| Verification | all five values re-read | five green tick rows |

## Scene Overview (measured times)

| Scene | Time | Learning goal | Visual | Key on-screen text |
|---|---|---|---|---|
| Title | 00:00–00:11 | Frame the problem | faint `P Q R S` with the S.A.S triangle lit and both rays dashed | Construct a Quadrilateral / Two Sides and Three Angles |
| 1 | 00:11–00:30 | The five given measurements | `2 adjacent sides` row, `3 angles` row, boxed strip, question | Two Sides and Three Angles · S.A.S.A.A · Side – Angle – Side – Angle – Angle · Where do we begin? |
| 2 | 00:30–00:50 | Find the S.A.S triangle | `△PQR` tinted, the two sides and `∠Q` lit, the other two angles boxed as "USE LATER" | Find the Side – Angle – Side Triangle · Side – Angle – Side · S.A.S · The included angle tells us the first triangle |
| 3 | 00:50–01:05 | The 3 + 2 plan | BUILD column (3 cards) + triangle, LOCATE column (2 cards) + two rays meeting | 3 Build. 2 Locate. · 3 measurements → triangle, 2 angles → rays |
| 4 | 01:05–01:21 | Draw `P Q`, set out `100°` at `Q` | `P Q` with its length, protractor on the base, graduation marked, ray drawn | STEP 2 — Build Triangle PQR by S.A.S · 4 cm · 100° · R must lie somewhere on this ray |
| 5 | 01:21–01:38 | Fix `R`, complete the triangle | compasses carry `4.8` to the ray, `R` marked, `Q R` joined, triangle filled | STEP 2 — Complete the Triangle · Triangle P Q R is fixed by S.A.S |
| 6 | 01:38–02:00 | The `75°` angle gives one ray | arm swings to `75°` with the arc growing, ray extended, a dot walking the ray, the 60/90 inset | STEP 3 — Set Out the Angle at P · 75° · S could be somewhere on this ray |
| 7 | 02:00–02:18 | The `120°` angle finds `S` | base arc about `R`, two chord steps, the second ray, the crossing marked `S` | STEP 4 — The Angle at R Finds S · ∠R = 120° · The two rays cross at exactly one point · Two directions agree at one point. |
| 8 | 02:18–02:44 | Complete, verify, generalise | `P S`, `R S` joined, five tick rows, then four method cards | Required Quadrilateral PQRS · Sketch → SAS → Rays → Intersection |
| 9 | 02:44–03:24 | Student challenge | YOUR TURN, `A B C D` with five cards, 4 s THINK clock, reveal of `△ABC`, the two rays and `D` | YOUR TURN · Which three measurements should you use first? · What is their included angle? · First triangle: A B C · built by S.A.S · S.A.S builds. Two angles locate. |
| 10 | 03:24–03:44 | Recap | recap figure + three recap rows + Thank-You card | Two Sides and Three Angles · S.A.S.A.A · Side–Angle–Side builds the triangle. · Angle–Angle locates the fourth vertex. |

## Scene Notes (Manim implementation)

- **The instruments match the textbook's note.** The textbook says standard
  angles can be handled with ruler and compasses and other angles with a
  protractor; the video shows exactly that split. `100°` is **read off a
  protractor** laid on `P Q` (the 80° graduation of the semicircle is marked and
  the ray drawn through it); `75°` is **set out by a swinging arm** with the arc
  growing under it, and the inset shows why it is available — it is the bisector
  of `60°` and `90°`; `120°` is **constructed with the pair of compasses**: an
  arc about `R` cutting `R Q`, then the same opening stepped round twice, since
  the chord of a 60° step is exactly the compass opening. `probe_layout.py`
  confirms both chords come back equal to the opening.
- **Both rays are drawn, kept, and then trimmed.** The ray from `P` is set out
  in scene 6 and stays on the board through scenes 7–8; the ray from `R` is set
  out in scene 7 and crosses it at `S`. Both stop just past `S` so the crossing
  is visible without the lines running off the figure.
- **Exact geometry.** Every vertex is a circle-circle intersection or a
  ray-ray intersection: `R` comes from the 4.8 cm circle about `Q`, and `S` from
  the crossing of the two rays at 75° and 120°. `probe_layout.py` re-measures
  4.000 / 4.800 / 75.00° / 100.00° / 120.00° / 65.00° for Example 6 and
  5.000 / 4.000 / 70.00° / 110.00° / 120.00° / 60.00° for the practice figure.
- **This figure is long and narrow** (`P S = 7.42 cm` against `P Q = 4 cm`), so
  it is drawn at 0.55 board units per centimetre, centred left of the board with
  the step column on the right, and the base at `y = +0.05` so the vertex
  letters clear both the heading and the notes.
- **Scene 7's construction has its own narration windows.** The narration marks
  the construction, the ray and the crossing separately, so the base arc sweeps
  over ~1.7 s and each chord step gets ~0.75 s instead of every sweep running at
  the 0.4 s floor.
- **The caption splitter folds a one-word tail into the previous caption.** A
  stand-alone last word ("D.") keeps a half-second caption that lands mostly in
  silence; merging it fixed the only caption that `verify_sync` queried.
- **A cache trap, fixed in the shared sync layer.** The speech cache is keyed on
  the words alone — bookmarks are stripped before hashing — so a cached clip
  carries the `input_text` of the *first* synthesis. Editing a bookmark layout
  afterwards asked the tracker for a mark its stored text did not contain, and
  manim-voiceover raised. `synced_voice.install_synced_voiceover` now hands the
  tracker the text the scene is actually speaking.
- **Text appears crisply, then the board holds.** Headings, cards and labels
  fade in over ≤0.5 s and the window's remaining time is a hold. Diagram work is
  paced across its window; words are not.

## Key Pedagogical Safeguards

1. **The two sides are adjacent, and the included angle is named.** Scene 2
   highlights `P Q`, then `∠Q`, then `Q R`, and says that the 100° angle is the
   one *between* them — that is what makes the first triangle an S.A.S
   construction.
2. **The three angles are not used at once.** Two of them are moved into a
   "USE LATER" panel in scene 2: the triangle comes first.
3. **Directions are contrasted with distances.** Scene 6 says it in the
   narration ("an angle gives a direction, not a distance") and shows a dot that
   could sit anywhere on the ray.
4. **The angles are set out on the correct side.** Each angle is drawn on the
   interior of the figure, and the ray from `R` is measured from `R Q`, not from
   `R P`.
5. **`P S` and `R S` are not invented.** They are never labelled with numbers;
   the video says they are what the construction produced.
6. **The construction marks stay.** The arcs, the chord points and both rays
   remain until the verification, so the crossing at `S` is still visible when
   the quadrilateral is finished.

## Final Production Check

Delivered as `construct_quadrilateral_2sides_3angles.py`
(`ConstructQuadrilateral2Sides3AnglesStory`):

- **Delivered file:** `media/videos/construct_quadrilateral_2sides_3angles/360p30/ConstructQuadrilateral2Sides3AnglesStory_captioned.mp4`
  (640×360, 30 fps, 224.3 s) with the series caption style burned in. Only the
  360p cut was rendered for this one, as requested; the same module renders the
  1080p60 master with the usual `--resolution 1920,1080 --fps 60` command.
- **Voice sync** (`audit_sync_overlap.py`): **11 of the 12 narration beats match
  their audio to 0.00 s** (scene 3 overruns by 0.12 s); the closing flourish on
  the Thank-You card adds the usual 0.37 s.
- **Layout/collision audit:** **no** out-of-board, text-in-text, text-on-line,
  text-outside-box, near-badge, LaTeX-as-text or empty-TeX flags. The flags in
  the first cut found four real problems — the title card's rays running through
  the sub-title, the `Q` and `B` letters sitting on the bottom notes, the
  "4 cm" and "100°" labels landing on the protractor, and the `R` letter under
  the chord-step compasses — and, through the last of those, a genuine geometry
  bug: the 120° construction's intermediate points were not 60° apart, so the
  chord of each step did not equal the compass opening and the "steps" would not
  have met on the base arc. All fixed and re-verified.
- **Real captions:** `verify_sync` — 69 captions, first at 0.32 s, last at
  221.90 s of a 224.30 s video, **0 captions in silence**, **0 speech blocks
  uncaptioned** → **PASS**. `verify_captions` — narration 598 words = SRT 598
  words → **PASS (word for word)**.
- **TTS pre-check:** all twelve narration pieces were generated and checked
  before the render; every line came back with audio and word boundaries.
- **Frame sweep:** title, all ten scenes and the closing card inspected as
  stills, plus zoomed checks of the protractor reading at `Q`, the swinging arm
  and the 60/90 inset at `P`, the compass construction at `R`, and the crossing
  at `S`.
- **Proof frames:** `frames360/tileA.png`, `tileB.png`, `tileC.png`,
  `tile_s7.png`, `f_row.png`, `zoom_protractor.png`, `zoom_R2.png`,
  `thanks_crop.png`.

---

## Revision — on-board `cm` unit, centred THINK clock (re-cut 360p)

Two on-screen fixes were asked for and applied, then the 360p cut was re-rendered
with the captions burned in:

1. **Every length on the board now shows its unit.** The measurement cards read `P Q = 4 cm`, `Q R = 4.8 cm`, and the two practice cards read
   `A B = 5 cm`, `B C = 4 cm`; the verification rows repeat them with the unit — 12 places
   in all, including the "USE LATER" and check panels. The narration
   already said "centimetres"; the board now agrees with it. Angles are
   untouched (`∠P = 75°`, `∠Q = 100°`, `∠R = 120°` carry no unit).
2. **The THINK countdown is centred on the board.** It is parked at
   `(BOARD_CX, BOARD_CY)` — the series default `story_common.CLOCK_POS` — so the
   paused clock is the centre of the frame instead of sitting in the right-hand gap.

Re-verified after the change: `audit_sync_overlap.py` → 0 real flags (only the
deliberate 0.37 s closing flourish, logged in `audit_after_cm.log`);
`verify_sync.py` → PASS, 69 captions, 0 captions in silence, 0 speech blocks
uncaptioned, 224.37 s; `verify_captions.py` → PASS, 598 = 598 words.
Unchanged timing (224.4 s) confirms the change is cosmetic only.
Visual proof: `frames360/after_cm/05_cards.png` (the `cm` cards) and
`frames360/after_cm/05_timer.png` (the centred clock)`.

---

## Revision 2 — alignment, diagram positioning and overlap pass

The three videos were re-checked scene by scene at the moment each scene holds
(`scene_frames.py`, stills under `frames360/crosscheck/`), and with two
automated passes: the hard-overlap audit (`audit_sync_overlap.py`) and a new
clearance audit (`audit_clearance.py`) that measures every pair of chalk texts
closer than 0.22 units **and** every text a chalk line actually runs through —
the case a bounding-box test cannot see, because a straight line's box is
degenerate.

What it found and what was fixed:

- **The 100° label at `Q` sat on the dashed `P R` guide line**
  (measured clearance 0.02 units). The label is placed along the angle
  bisector; it now sits at 1.04 instead of 1.30 from `Q`, i.e. well inside the
  angle and clear of the guide.
- **The "90°" of the `75° = (60° + 90°)/2` inset sat on the tip of the
  vertical 90° arm** (clearance 0.00). The inset is unchanged; the label is
  lifted clear of the arm's tip.

After the fixes: `audit_clearance.py` → **0 text/line collisions** in this
video (the pairs still under 0.22 units are the designed two-line card stacks,
which sit 0.05-0.10 apart by construction), and `audit_sync_overlap.py` → **0
flags**. Nothing was re-timed: the narration, the bookmarks and every `run_time`
are untouched, so `verify_sync.py` → PASS (69 captions, 0 in silence, 0
uncaptioned, 224.4 s) and `verify_captions.py` → PASS (598 = 598 words)
on the re-rendered master.

Delivered this round: the **1080p60 master** with the captions burned in
(`final_videos/ConstructQuadrilateral2Sides3AnglesStory_captioned.mp4`), alongside the refreshed 360p review cut
(`finals_360/`).

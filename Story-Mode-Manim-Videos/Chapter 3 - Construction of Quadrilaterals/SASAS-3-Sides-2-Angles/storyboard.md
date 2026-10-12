# Production-Ready Storyboard

**VIDEO TITLE:** How to Construct a Quadrilateral Given 3 Sides and 2 Included
Angles (S.A.S.A.S Method)
**TOPIC:** Construction of a Quadrilateral from Three Sides and Two Included
Angles
**CLASS / CHAPTER:** Class 8 Mathematics — Chapter 3 — Construction of
Quadrilaterals
**STORYMODE:** 06 (sixth video of the Class 8 Chapter 3 set)
**LLM KEY / FUNCTION NAME:** `construct_quadrilateral_3sides_2angles`
**DURATION (measured):** 4 min 07 s (247.1 s) — 360p30 delivered with captions
burned in, 72 captions / 631 words
**TEXTBOOK REFERENCE:** Telangana SCERT, Class VIII Mathematics (English
Medium), 2025–26 edition, Chapter 3 — Construction of Quadrilaterals:
"construction when three sides and two included angles are given (S.A.S.A.S)",
**Example 8** (`A B = 5`, `B C = 4.5`, `C D = 6`, `∠B = 100°`, `∠C = 75°`),
with **Exercise 3.5(a)** (`P Q = 3.6`, `Q R = 4.5`, `R S = 5.6`,
`∠Q = 135°`, `∠R = 60°`) as the student challenge.

---

## Learning Objective

By the end of this video, students should be able to:

- Read the five measurements as a **chain**: side, angle, side, angle, side.
- Check that each angle is an **included** angle — it must lie between the two
  sides that are given next to it.
- Build the first triangle by **S.A.S** (here `△ABC`: `A B`, `∠B`, `B C`).
- Use the second included angle to draw a **ray** from the third vertex.
- Mark the last side's length on that ray with the compasses, locating the
  fourth vertex.
- Complete the quadrilateral — and note that the fourth side was never given.
- Apply the same chain to a new set of labels (Exercise 3.5(a)).

**Primary takeaway:** S.A.S builds the first triangle; the next angle gives a
**direction**, the last side gives a **distance**, and direction plus distance
locate the fourth vertex. *3 build, 2 finish.*

## Why the Last Step is One Ray and One Arc

The previous video (S.A.S.A.A) ended with **two** unused angles, so its last
vertex was found at the crossing of two rays. This case ends with an angle and
a length:

```
        D                                  chain:  AB - ∠B - BC - ∠C - CD
       / \                                 first three  ->  triangle ABC by S.A.S
      /   \                                next angle   ->  ray from C
  A--/-----\--B   C                        last side    ->  6 cm arc about C
      \     /                              ray ∩ arc    ->  D
       \   /
        (D on ray C Y)
```

| method | what locates the last vertex |
|---|---|
| S.S.S.S.D / S.S.S.D.D (videos 3–4) | two compass **arcs** |
| S.A.S.A.A (video 5) | two **rays** |
| **S.A.S.A.S (this video)** | **one ray and one arc** |

## The figures are constructed, not sketched

`quadrilateral_from_chain()` builds both figures the way the construction
builds them — the S.A.S triangle first, then the ray, then the distance along
it — so each drawing satisfies its data exactly. The second angle's turn is
taken on the side that keeps the figure convex.

| figure | given | how the point is found | measured off the render |
|---|---|---|---|
| Example 8 | `A B = 5` | the base, drawn level | 5.000 |
| Example 8 | `∠B = 100°`, `B C = 4.5` | `C` on the ray set out from `B A` | 100.00°, 4.500 |
| Example 8 | `∠C = 75°`, `C D = 6` | the ray from `C`, and `D` at 6 cm along it | 75.00°, 6.000 |
| Example 8 | `A D`, `∠A`, `∠D` | never given — produced by the construction | 3.914, 92.87°, 92.13° |
| Ex 3.5(a) | `P Q = 3.6`, `∠Q = 135°`, `Q R = 4.5` | the S.A.S triangle | 3.600, 135.00°, 4.500 |
| Ex 3.5(a) | `∠R = 60°`, `R S = 5.6` | ray from `R`, distance along it | 60.00°, 5.600 |
| Ex 3.5(a) | `P S`, `∠P`, `∠S` | produced by the construction | 4.831, 73.49°, 91.51° |

`probe_layout.py` re-measures every one of those values off the constructed
vertices, confirms both figures come out **convex**, and checks the board
bounds of the figures, their letters, both rays and the five-card chain row.

## Mathematical Content

| Concept | Statement | Shown as |
|---|---|---|
| The measurement chain | `AB – ∠B – BC – ∠C – CD` | five connected cards with `S A S A S` beneath them |
| Included angle | the angle between the two sides given next to it | each angle highlighted with its two arms, in the sides' colours |
| Which three build | `A B`, `∠B`, `B C` | BUILD column + triangle sketch |
| Which two finish | `∠C`, `C D` | FINISH column + a mini ray-and-arc sketch |
| Setting out `100°` at `B` | a protractor on `B A` | the protractor laid on the base, graduation marked, ray drawn |
| Fixing `C` | `B C = 4.5` along that ray | compasses carry the length from the card to the ray |
| The direction for `D` | `∠C = 75°` from `C B` | an arm swings from `C B`, the arc growing under it, then the ray |
| The distance to `D` | `C D = 6` on that ray | the compasses sweep a 6 cm arc about `C`; it cuts the ray at `D` |
| Verification | all five values re-read | five green tick rows |
| The reusable method | sketch → SAS → ray → length | four method cards + the flow line |

## Scene Overview (measured times)

| Scene | Time | Learning goal | Visual | Key on-screen text |
|---|---|---|---|---|
| Title | 00:00–00:11 | Frame the problem | faint `ABCD` with `A B`, `B C`, `C D` lit and both included angles marked | Construct a Quadrilateral / Three Sides + Two Included Angles |
| 1 | 00:11–00:37 | The measurement chain | five empty cards linked by arrows, then each measurement drops in with its `S`/`A` letter | Three Sides + Two Included Angles · Follow the measurement chain · S.A.S.A.S · Side – Angle – Side – Angle – Side |
| 2 | 00:37–00:57 | What "included" means | `A B`+`B C` light up with `∠B`, then `B C`+`C D` with `∠C` | What Does Included Mean? · 100° is between A B and B C · 75° is between B C and C D · Included = between two given sides · `AB – ∠B – BC – ∠C – CD` |
| 3 | 00:57–01:14 | The 3 + 2 plan | BUILD column (3 cards) + triangle; FINISH column (2 cards) + mini ray-and-arc | 3 Build. 2 Finish. · 3 measurements → triangle, 2 → ray + distance |
| 4 | 01:14–01:32 | Draw `A B`, set out `100°` at `B` | `A B = 5 cm`, protractor on the base, graduation marked, ray drawn | STEP 2 — Start with SAS · 5 cm · 100° · C must lie somewhere on this ray |
| 5 | 01:32–01:56 | Fix `C`, complete `△ABC` | compasses carry `4.5` to the ray, `C` marked, `B C` and the internal `A C` drawn, triangle filled | STEP 2 — Complete the Triangle · Triangle A B C is fixed by S.A.S · A C was not given — the construction made it |
| 6 | 01:56–02:15 | The `75°` angle gives a direction | arm swings from `C B` to `75°`, ray extended, a dot slides along it | STEP 3 — The Angle at C · 75° · D could lie anywhere on this ray · …but we still need the distance from C |
| 7 | 02:15–02:37 | The last side fixes `D` | 6 cm compass arc about `C` cutting the ray at `D`, then `A D` joins | STEP 4 — Locate D · Angle + Side = exact vertex · Direction + Distance → D |
| 8 | 02:37–03:04 | Complete, verify, generalise | five tick rows, then four method cards | Required Quadrilateral ABCD · A D was never given · Sketch → SAS → Ray → Length |
| 9 | 03:04–03:47 | Student challenge (Ex 3.5(a)) | YOUR TURN, `P Q R S` with five cards, 4 s THINK clock, reveal of `△PQR`, the 60° ray, the 5.6 arc and `S` | YOUR TURN · Which three measurements construct the first triangle? · Find the first Side–Angle–Side group · First triangle: P Q R · built by S.A.S · S.A.S builds. A.S finishes. |
| 10 | 03:47–04:07 | Recap | completed `A B C D` + three recap rows + Thank-You card | Three Sides + Two Included Angles · S.A.S.A.S · S.A.S builds the first triangle. · Angle gives direction. Side gives distance. |

## Scene Notes (Manim implementation)

- **The chain is the video's identity.** Scene 1 lays out five *empty* cards
  linked by arrows, then drops each measurement into its box with its `S` or
  `A` letter beneath, and only then reveals the boxed `S.A.S.A.S` and the
  spelled-out name. The five cards are colour-coded — cyan for sides, amber and
  pink for angles — and those colours are reused everywhere the measurement
  appears.
- **The instruments match the textbook's note.** `100°` is read off a
  **protractor** laid on `B A`; `75°` is set out by a **swinging arm** with the
  arc growing under it; the final `6 cm` is a **compass arc** about `C` — so all
  three construction marks the textbook asks students to keep are on the board
  through scene 8.
- **Exact geometry.** `quadrilateral_from_chain()` builds `C` from the 4.5 cm
  circle about `B`, then takes the second angle's turn on the side that makes
  the quadrilateral convex, and places `D` at 6 cm along that ray.
  `probe_layout.py` re-measures 5.000 / 4.500 / 6.000 / 100.00° / 75.00° for
  Example 8 and 3.600 / 4.500 / 5.600 / 135.00° / 60.00° for Exercise 3.5(a),
  and confirms both figures are convex.
- **The C letter moves radially clear.** The compass arc that fixes `C` passes
  through the vertex itself, so the letter is offset along the radius
  (`C + (-0.26, 0.37)`) rather than to the usual up-right corner.
- **The 75° label sits in the free part of the wedge.** The interior diagonal
  `A C` lies inside the `∠C` wedge, so the label is placed between `C B` and
  `C A` (a third of the way round from `C B`) with a small arc, not on the
  bisector where the diagonal runs.
- **`A C` is drawn only while the triangle is being explained.** It is the
  construction's own third side, so it appears as a dashed internal segment in
  scenes 5 and 8 and is dropped from scenes 6–7, where it would otherwise cross
  the angle label.
- **A cache trap, fixed in the shared sync layer (video 5).** The speech cache
  is keyed on the words alone, so a cached clip carries the `input_text` of the
  first synthesis; `synced_voice.install_synced_voiceover` now hands the tracker
  the text the scene is actually speaking, so a later bookmark edit cannot ask
  for a mark the stored text does not contain.
- **The caption splitter folds a short tail into the previous caption**, so no
  stand-alone one-word caption lands mostly in silence at the end of a piece.
- **Text appears crisply, then the board holds.** Headings, cards and labels
  fade in over ≤0.5 s and the window's remaining time is a hold. Diagram work is
  paced across its window; words are not.

## Key Pedagogical Safeguards

1. **"Included" is the point of the video.** Scene 2 is devoted to it: each
   angle is shown with the two sides it lies between, in those sides' colours,
   and the boxed line "Included = between two given sides" closes the scene.
2. **All three angles are not used at once.** Only `∠B` belongs to the first
   triangle; `∠C` is the direction for the last side.
3. **This case is not S.A.S.A.A.** The narration says the angle alone does not
   fix a point — "D could be anywhere on this ray" — and the last side's arc is
   what settles it.
4. **The angles stay on the correct side.** `∠B` is set out from `B A` and
   `∠C` from `C B`; the second turn is chosen so the quadrilateral closes
   convexly.
5. **`A D` is never invented.** It is not labelled with a length; the video says
   the construction produced it.
6. **Construction marks are kept.** The `100°` angle, the `75°` angle, the ray
   `C Y` and the final 6 cm arc are still on the board when the verification
   rows appear.

## Final Production Check

Delivered as `construct_quadrilateral_3sides_2angles.py`
(`ConstructQuadrilateral3Sides2AnglesStory`):

- **Delivered file:** `media/videos/construct_quadrilateral_3sides_2angles/360p30/ConstructQuadrilateral3Sides2AnglesStory_captioned.mp4`
  (640×360, 30 fps, 247.1 s) with the series caption style burned in. Only the
  360p cut was rendered for this one; the same module renders the 1080p60 master
  with `--resolution 1920,1080 --fps 60`.
- **Voice sync** (`audit_sync_overlap.py`): **11 of the 12 narration beats match
  their audio to 0.00 s** (scene 3 overruns by 0.12 s); the closing flourish on
  the Thank-You card adds the usual 0.37 s.
- **Layout/collision audit:** **no** out-of-board, text-in-text, text-on-line,
  text-outside-box, near-badge, LaTeX-as-text or empty-TeX flags. The first cut
  found eight real problems — the chain's acronym strip drawn after its window
  had run out (a 0.8 s overrun), the boxed "Included" line on the `C` letter,
  the `C` letter on the arc that fixes it, the `4.5 cm` label inside the step
  column, the dashed `A C` through the `75°` label, the `75°` label on the
  triangle's `A C` edge in scenes 6, 7 and 10, the step cards reaching back over
  `B C`, and the challenge cards running into the exercise tag. All fixed and
  re-verified.
- **Real captions:** `verify_sync` — 72 captions, first at 0.26 s, last at
  244.66 s of a 247.06 s video, **0 captions in silence**, **0 speech blocks
  uncaptioned** → **PASS**. `verify_captions` — narration 631 words = SRT 631
  words → **PASS (word for word)**.
- **TTS pre-check:** all twelve narration pieces were generated and checked
  before the render; every line came back with audio and word boundaries.
- **Frame sweep:** title, all ten scenes and the closing card inspected as
  stills, plus zoomed checks of the chain row, the protractor reading at `B`,
  the swinging arm at `C`, the 6 cm arc and the crossing at `D`.
- **Proof frames:** `frames360/tileA.png`, `tileB.png`, `tileC.png`,
  `frames360/end.png`.

---

## Revision — on-board `cm` unit, centred THINK clock (re-cut 360p)

Two on-screen fixes were asked for and applied, then the 360p cut was re-rendered
with the captions burned in:

1. **Every length on the board now shows its unit.** The measurement cards read `A B = 5 cm`, `B C = 4.5 cm`, `C D = 6 cm` — in the
   measurement chain, the build panels, the verification rows and the practice column
   (`P Q = 3.6 cm`, `Q R = 4.5 cm`, `R S = 5.6 cm`) — 15 places in all. The narration
   already said "centimetres"; the board now agrees with it. Angles are
   untouched (`∠B = 100°`, `∠C = 75°`, `∠Q = 135°`, `∠R = 60°`).
2. **The THINK countdown is centred on the board.** It is parked at
   `(BOARD_CX, BOARD_CY)` — the series default `story_common.CLOCK_POS` — so the
   paused clock is the centre of the frame instead of sitting in the right-hand gap.

Re-verified after the change: `audit_sync_overlap.py` → 0 real flags (only the
deliberate 0.37 s closing flourish, logged in `audit_after_cm.log`);
`verify_sync.py` → PASS, 72 captions, 0 captions in silence, 0 speech blocks
uncaptioned, 247.07 s; `verify_captions.py` → PASS, 631 = 631 words.
Unchanged timing (247.1 s) confirms the change is cosmetic only.
Visual proof: `frames360/after_cm/06_cards.png` and `06_cards_full.png` (the `cm` chain
cards) and `frames360/after_cm/06_timer.png` (the centred clock)`.

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

- **The `D` label lay on the 6 cm compass arc that locates `D`**
  (clearance 0.00): the arc is centred on `C` with radius `C D`, so the label
  is now placed radially outward from `C`, 0.34 beyond the vertex, instead of
  a fixed offset that the arc ran through.

After the fixes: `audit_clearance.py` → **0 text/line collisions** in this
video (the pairs still under 0.22 units are the designed two-line card stacks,
which sit 0.05-0.10 apart by construction), and `audit_sync_overlap.py` → **0
flags**. Nothing was re-timed: the narration, the bookmarks and every `run_time`
are untouched, so `verify_sync.py` → PASS (72 captions, 0 in silence, 0
uncaptioned, 247.1 s) and `verify_captions.py` → PASS (631 = 631 words)
on the re-rendered master.

Delivered this round: the **1080p60 master** with the captions burned in
(`final_videos/ConstructQuadrilateral3Sides2AnglesStory_captioned.mp4`), alongside the refreshed 360p review cut
(`finals_360/`).

## Revision 2b — the method cards no longer sit on the figure

Two more problems were reported from the rendered master and are fixed:

- **The four method cards overlapped the figure.** In "Required Quadrilateral
  ABCD" the column of cards (`1. SKETCH … 4. FINAL SIDE`) started at x = +1.48
  while the figure's `C` vertex and the `C D` and `C B` edges reach x = +1.65 —
  so the cards were drawn *over* the figure's corner and its `C` label
  (a LINE-IN-BOX hit: a figure edge running inside a card). The column now
  starts at +2.03, a 0.38 gap, and still ends at +4.77, well inside the
  board's +5.60 edge.
- **The recap rows (1), (2), (3) crowded the figure's `C` label** (0.09 gap).
  The rows moved 0.35 to the right: the gap is now 0.44 and the rows end at
  +4.44.

Both were caught by a new check in `audit_clearance.py` that reports chalk from
one part of a scene lying inside another part's card (`TEXT-IN-BOX`,
`LINE-IN-BOX`) — the overlap class a text-against-text audit cannot see, since
the figure's edges are not text. All three videos in this batch now report
**0 foreign-box collisions**; this one also reports 0 text/line collisions and
0 hard-overlap flags.

Re-rendered after the fix: the 360p review cut (`finals_360/`) and the 1080p60
master (`final_videos/`), both verified — `verify_sync` PASS (72 captions, 0 in
silence, 0 uncaptioned) and `verify_captions` PASS (631 = 631 words). The
narration and every `run_time` are untouched, so the timing is unchanged.

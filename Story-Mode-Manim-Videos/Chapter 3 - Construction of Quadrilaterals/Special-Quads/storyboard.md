# Production-Ready Storyboard

**VIDEO TITLE:** Constructing Special Quadrilaterals: Rhombus, Parallelogram &
Square
**TOPIC:** Construction of Special Quadrilaterals (Rhombus, Parallelogram,
Square) Using Diagonal and Angle Properties
**CLASS / CHAPTER:** Class 8 Mathematics — Chapter 3 — Construction of
Quadrilaterals
**STORYMODE:** 07 (seventh video of the Class 8 Chapter 3 set)
**LLM KEY / FUNCTION NAME:** `construct_special_quadrilaterals_rhombus_parallelogram`
**DURATION (measured):** 5 min 15 s (315.4 s) — 360p30 delivered with captions
burned in, 94 captions / 815 words
**TEXTBOOK REFERENCE:** Telangana SCERT, Class VIII Mathematics (English
Medium), 2025–26 edition, Chapter 3 — Construction of Quadrilaterals:
the parallelogram **Example 7** (`B E = 4.2`, `E L = 5`, `∠T = 45°`), the
rhombus **Example 9** (diagonals `A C = 4.5`, `B D = 6`), and Exercise 3.6
(square `J U M P` with diagonal `4.2 cm`). The page's own question — what
figure results when a rhombus's two diagonals become equal — is answered in
scene 6, and the full square construction is presented as the textbook-grounded
extension it is, not as a worked textbook example.

---

## Learning Objective

By the end of this video, students should be able to:

- Explain why a **special** quadrilateral can be constructed from fewer
  explicitly given measurements.
- Use a parallelogram's **angle properties** (opposite angles equal,
  consecutive angles supplementary) to derive the missing angles.
- Construct a parallelogram from two adjacent sides and one angle.
- Use the rhombus's **perpendicular-bisecting diagonals** to place all four
  vertices from the two diagonals alone.
- See the square as the same construction with the extra condition that the
  diagonals are equal.
- Decide **which property is the key** before reaching for the ruler.

**Primary takeaway:** for a special quadrilateral, use its properties to
generate the construction information that was never given.

## Why Special Shapes Are Different

The earlier videos in this chapter always supplied five independent
measurements. A named shape carries information of its own:

| shape | given | property used | what it supplies |
|---|---|---|---|
| parallelogram `B E L T` | 2 sides + 1 angle | opposite angles equal; consecutive angles sum to 180° | the other three angles |
| rhombus `A B C D` | 2 diagonals | diagonals bisect each other at right angles | every vertex, from half-diagonal distances |
| square `J U M P` | 1 diagonal | the rhombus rule **and** equal diagonals | the second diagonal, and every vertex |

## The figures are constructed, not sketched

Every vertex is generated from the given numbers with vectors:

| figure | given | how the points are found | measured off the render |
|---|---|---|---|
| `B E L T` | `B E = 4.2` | the base, drawn level | 4.200 |
| `B E L T` | `∠T = 45°` → `∠E = 45°` | `L` on the ray from `E`, `E L = 5` | 45.00°, 5.000 |
| `B E L T` | `L T = B E`, `T B = E L` | `T = B + (L − E)` — where the two 135° rays meet | 4.200, 5.000 |
| `B E L T` | the angles | re-measured at all four corners | 45°, 135°, 45°, 135° |
| `A B C D` | `A C = 4.5`, `B D = 6` | half each either side of `O`, at right angles | 4.500, 6.000; halves 2.25/2.25, 3/3 |
| `A B C D` | the sides | all four re-measured (they should be equal) | 3.750 each; `A C · B D = 0` |
| `J U M P` | diagonal `4.2` | no length given twice: equal perpendicular-bisecting diagonals | both diagonals 4.200; halves 2.100; sides 2.970 |

`probe_layout.py` re-measures all of that off the constructed vertices, checks
that both pairs of opposite sides of `B E L T` really are parallel (cross
products 0.0000), that the rhombus's and square's diagonals are perpendicular
(dot products 0.0000), and that the figures and their letters stay on the board.

## Mathematical Content

| Concept | Statement | Shown as |
|---|---|---|
| Special shape = extra information | the name itself tells us something | three cards whose "?" becomes a property |
| Opposite angles | `∠E = ∠T = 45°` | the two angles marked in the same colour |
| Consecutive angles | `180° − 45° = 135°` | the arithmetic card, then `∠L = ∠B = 135°` |
| The construction | S.A.S triangle `B E L`, then two 135° rays | arms swinging to 45° at `E`, then 135° at `B` and at `L`, meeting at `T` |
| Rhombus diagonals | perpendicular, bisecting | the right-angle mark at `O` and the bisection ticks |
| Half-diagonals | `O B = O D = 6 ÷ 2 = 3` | the value card, then the compasses carrying 3 cm each way |
| Rhombus from diagonals | no side lengths needed | `A C`, its perpendicular bisector, `B` and `D` at 3 cm |
| Rhombus → square | equal diagonals | the shorter diagonal grows until they match |
| Square from one diagonal | the other diagonal is equal | `4.2 ÷ 2 = 2.1` each way from `O` |
| The method | shape → property → derived measurement → construction | four cards + the flow line |
| The challenge | `∠A = 65°` → `65°, 115°, 115°`; diagonals 8 and 6 → 4, 4, 3, 3 | answers appear under each figure |

## Scene Overview (measured times)

| Scene | Time | Learning goal | Visual | Key on-screen text |
|---|---|---|---|---|
| Title | 00:00–00:10 | Frame the problem | three small figures with their names | Special Quadrilaterals · Parallelogram · Rhombus · Square · Property → Missing Information → Construction |
| 1 | 00:10–00:31 | Three short lists of measurements | three cards: the given data, a "?", then the property that unlocks it | Special Shape = Extra Information · Only 3 measurements? · Only 2 measurements? · Can this be enough? |
| 2 | 00:31–01:06 | Derive the parallelogram's angles | `∠T` and `∠E` marked 45°, then the arithmetic, then `∠L` and `∠B` at 135° | Use the Properties First · Opposite angles are equal · Consecutive angles add to 180° · 180° − 45° = 135° · 45°, 135°, 45°, 135° |
| 3 | 01:06–01:35 | Construct `B E L T` | `B E`, the 45° arm at `E`, `E L = 5`, then two 135° arms meeting at `T` | STEP 2 — Build Triangle BEL · Triangle B E L is fixed by S.A.S · PARALLELOGRAM COMPLETE |
| 4 | 01:35–02:02 | Read the rhombus's diagonal properties | the two diagonals crossing at `O`, right angle, bisection ticks | RHOMBUS ABCD — Read the Diagonals · Diagonals are perpendicular · Diagonals bisect each other · OB = OD = 6/2 = 3 · BISECT + PERPENDICULAR |
| 5 | 02:02–02:38 | Construct the rhombus | `A C = 4.5`, its perpendicular bisector, compasses at 3 cm each way | STEP 2 — Draw A C and Its Bisector · The perpendicular through O · 6/2 = 3 · RHOMBUS COMPLETE |
| 6 | 02:38–03:17 | Extend to the square | the rhombus's shorter diagonal grows; then `J U M P` from one diagonal | From Rhombus to Square · What if both diagonals are equal? · Equal diagonals, bisecting at right angles: a square · 4.2 ÷ 2 = 2.1 · SQUARE COMPLETE |
| 7 | 03:17–03:41 | Compare the three strategies | three columns: shape, property, effect | Which Property Unlocks the Construction? · So which property gives the missing information? |
| 8 | 03:41–03:58 | The reusable method | four method cards + a small rhombus reminder | Analyse Before You Draw · 1 IDENTIFY / 2 RECALL / 3 DERIVE / 4 CONSTRUCT · Shape → Property → Derived Measurement → Construction |
| 9 | 03:58–04:57 | Student challenge | a parallelogram with `∠A = 65°` and a rhombus with diagonals 8 and 6, 4 s THINK clock, then the answers | YOUR TURN · Property first — construction second · What are the other three angles? · How far is each vertex from O? |
| 10 | 04:57–05:15 | Recap | the three figures with their properties, then the boxed chain | Know the Shape. Use Its Properties. · Special properties → missing measurements → construction · Know the Shape. Use Its Properties. Construct It. |

## Scene Notes (Manim implementation)

- **The three cards unlock rather than appear.** Scene 1 lays out three cards
  with the shape name, the given data and a "?"; at the last window the "?"
  fades and the property takes its place — the video's visual identity
  (given + property → enough information) in one move.
- **The parallelogram's angles are propagated, not asserted.** `∠T = 45°`
  appears first, then `∠E` in the same colour with the note "opposite angles are
  equal", then the arithmetic card `180° − 45° = 135°` before `∠L` and `∠B`
  appear. Nothing is labelled with a number the video has not derived.
- **The angle at `T` is drawn between the right arms.** An early cut drew it
  between `T E` and `T B` — `T E` is the diagonal, not a side — which showed a
  ~20° wedge instead of the given 45°. The audit's collision at that label led
  to the mistake; the arms are now `T L` and `T B`.
- **The rhombus construction is the textbook's.** `A C` is drawn, its
  perpendicular bisector through the midpoint `O` is added, and the compasses
  carry `6 ÷ 2 = 3` cm to both sides of the perpendicular — which is exactly
  where `B` and `D` must be.
- **The square is presented as an extension, as the textbook frames it.** Scene 6
  first answers the page's own question by animating the rhombus's shorter
  diagonal until both are equal (the figure becomes a square), and only then
  builds `J U M P` from its 4.2 cm diagonal with the same method.
- **Everything is derived from the numbers.** `parallelogram_frame()`,
  `rhombus_frame()` and `square_frame()` generate the vertices with vectors;
  the parallelogram's `T` is literally `B + (L − E)`, which is where the two
  135° rays meet.
- **Text appears crisply, then the board holds.** Headings, cards and labels
  fade in over ≤0.5 s and the window's remaining time is a hold.
- **The caption splitter folds a short tail into the previous caption**, and
  `synced_voice` hands the tracker the text the scene is actually speaking, so
  a later bookmark edit can never ask for a mark the cached clip does not carry.

## Key Pedagogical Safeguards

1. **Only special quadrilaterals can be treated this way.** The narration says
   the shape's *name* is the extra information, and every derived value is tied
   to the property that produced it.
2. **The derivation is shown before the construction.** Scene 2 ends with all
   four angles on the board; only then does scene 3 start drawing.
3. **The rhombus's crossing is exact.** Perpendicularity is marked at `O`, both
   diagonals carry bisection ticks, and the video states `O B = O D = 6 ÷ 2 = 3`.
4. **The square is flagged as the extension it is** — "the same construction,
   with one extra condition" — never as a separate textbook worked example.
5. **The fourth side is never invented.** `A D` is not given a length; it appears
   when `A` is joined to `D`.
6. **Properties before tools.** Every scene states the property first and picks
   up the compasses second, which is the habit the chapter is trying to build.

## Final Production Check

Delivered as `construct_special_quadrilaterals_rhombus_parallelogram.py`
(`ConstructSpecialQuadrilateralsRhombusParallelogramStory`):

- **Delivered file:** `media/videos/construct_special_quadrilaterals_rhombus_parallelogram/360p30/ConstructSpecialQuadrilateralsRhombusParallelogramStory_captioned.mp4`
  (640×360, 30 fps, 315.4 s) with the series caption style burned in; copied
  into the chapter's `finals_360/`. Only the 360p cut was rendered; the same
  module renders the 1080p60 master with `--resolution 1920,1080 --fps 60`.
- **Voice sync** (`audit_sync_overlap.py`): **11 of the 12 narration beats match
  their audio to 0.00 s**; the closing flourish on the Thank-You card adds the
  usual 0.37 s.
- **Layout/collision audit:** **no** out-of-board, text-in-text, text-on-line,
  text-outside-box, near-badge, LaTeX-as-text or empty-TeX flags. The first two
  cuts found fifteen real problems, including an empty `Text("")` behind the
  scene-1 "given" lines, the three card questions falling outside their cards,
  the dashed `T E` link and both 45° labels on top of each other, the half-diagonal
  labels sitting on the compass legs, the comparison columns overflowing the
  board, the setup's 65° mark surviving into the reveal (so it was drawn twice),
  a 1.1 s overrun in the recap's closing order — and the wrong-arms angle at `T`
  described above. All fixed and re-verified.
- **Real captions:** `verify_sync` — 94 captions, first at 0.14 s, last at
  313.00 s of a 315.39 s video, **0 captions in silence**, **0 speech blocks
  uncaptioned** → **PASS**. `verify_captions` — narration 815 words = SRT 815
  words → **PASS (word for word)**.
- **TTS pre-check:** all twelve narration pieces were generated and checked
  before the render.
- **Frame sweep:** title, all ten scenes and the closing card inspected as
  stills, plus zooms of the three cards unlocking, the propagated angles, the
  135° rays meeting at `T`, the perpendicular bisector with the 3 cm marks, the
  rhombus-to-square morph and the `J U M P` construction.
- **Proof frames:** `frames360/tileA.png`, `tileB.png`, `tileC.png`.

---

## Revision — on-board `cm` unit, centred THINK clock (re-cut 360p)

Two on-screen fixes were asked for and applied, then the 360p cut was re-rendered
with the captions burned in:

1. **Every length on the board now shows its unit.** The cards read `B E = 4.2 cm`, `E L = 5 cm`, `A C = 4.5 cm`, `B D = 6 cm`, and the
   derived values read `O B = O D = 6/2 = 3 cm` and `4.2 ÷ 2 = 2.1 cm` — 10 places in all, belt and
   rhombus, given and derived. The narration
   already said "centimetres"; the board now agrees with it. Angles are
   untouched (`∠T = 45°`, `∠E = 45°`, `∠A = 65°`).
2. **The THINK countdown is centred on the board.** It is parked at
   `(BOARD_CX, BOARD_CY)` — the series default `story_common.CLOCK_POS` — so the
   paused clock is the centre of the frame instead of below the figure.

Re-verified after the change: `audit_sync_overlap.py` → 0 real flags (only the
deliberate 0.37 s closing flourish, logged in `audit_after_cm.log`);
`verify_sync.py` → PASS, 94 captions, 0 captions in silence, 0 speech blocks
uncaptioned, 315.53 s; `verify_captions.py` → PASS, 815 = 815 words.
Unchanged timing (315.5 s) confirms the change is cosmetic only.
Visual proof: `frames360/after_cm/07_cards.png` and `frames360/after_cm/07_timer.png`
(the centred clock, with `8 cm` / `6 cm` on the challenge text)`.

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

- **`O` lay on the horizontal diagonal** in the read-the-diagonals
  scene (on `A C`), in the rhombus construction (on `A C`) and in the square
  construction (on `J U`) — clearance 0.00-0.02 in all three. It now sits in a
  free quadrant beside the crossing: lower-left in the read-off, upper-left
  (above the line, clear of the compass leg) in the two construction scenes.
- **`O` also sat inside the right-angle mark** at the crossing in the
  read-the-diagonals scene (it overlapped the mark's corner), with `90°` only
  0.04 from it. `O` is out of the mark and `90°` is moved further out, so the
  mark reads cleanly on its own.
- **`B` and `D` lay on the perpendicular bisector**: that dashed line is drawn
  1.22x past the vertices, so it ran through both letters. Both labels now sit
  0.34 to the right of their vertex, which also clears the 3 cm compass arc
  (centred on `O` with radius `O B`) that they had started to touch.
- **The morph drew the square's equal diagonal through the rhombus's `A` and
  `C` labels**: those names are retired as the morph starts, so no line crosses
  a letter during the transition.

After the fixes: `audit_clearance.py` → **0 text/line collisions** in this
video (the pairs still under 0.22 units are the designed two-line card stacks,
which sit 0.05-0.10 apart by construction), and `audit_sync_overlap.py` → **0
flags**. Nothing was re-timed: the narration, the bookmarks and every `run_time`
are untouched, so `verify_sync.py` → PASS (94 captions, 0 in silence, 0
uncaptioned, 315.5 s) and `verify_captions.py` → PASS (815 = 815 words)
on the re-rendered master.

Delivered this round: the **1080p60 master** with the captions burned in
(`final_videos/ConstructSpecialQuadrilateralsRhombusParallelogramStory_captioned.mp4`), alongside the refreshed 360p review cut
(`finals_360/`).

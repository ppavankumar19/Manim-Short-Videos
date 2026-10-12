# Production-Ready Storyboard

**VIDEO TITLE:** Why 4 Sides Aren't Enough: Understanding the 5-Measurement Rule
for Drawing Unique Quadrilaterals
**TOPIC:** Uniqueness of Quadrilaterals & Why 5 Independent Measurements Are Required
**CLASS / CHAPTER:** Class 8 Mathematics — Chapter 3 — Construction of Quadrilaterals
**STORYMODE:** 01 (first video of the Class 8 Chapter 3 set)
**LLM KEY / FUNCTION NAME:** `quadrilateral_uniqueness_and_five_measurements`
**DURATION (measured):** 3 min 34 s (214.1 s), 1080p60 master with captions burned
**TEXTBOOK REFERENCE:** Telangana SCERT, Class VIII Mathematics (English Medium),
2025–26 edition, Chapter 3 — Construction of Quadrilaterals: the Kamal and Joseph
introductory activity (pages 62–63), the four-stick and fifth-stick activity
(page 68) and the chapter summary (page 83).

---

## Learning Objective

By the end of this video, students should be able to:

- Say what it means for a quadrilateral to be *unique* (all constructions from
  the same data are congruent).
- Explain why four side lengths alone do not fix a quadrilateral.
- Show that a quadrilateral can change shape while its four sides stay fixed.
- Explain why a *suitable fifth independent* measurement is needed.
- Recognise that a diagonal fixes the shape because it creates two triangles.
- Name the measurement combinations used later in the chapter.

**Primary takeaway:** four sides can bend into many shapes; a suitable fifth
independent measurement removes the last freedom and makes the shape unique.

## Historical / Why-Needed Hook

The textbook opens with Kamal and Joseph, both asked to draw a frame 8 cm long
and 6 cm wide. Their drawings do not match, although every corresponding side is
correct. The video opens on exactly that mystery: **"If the measurements match,
why don't the shapes?"**

## Core Visual Metaphor — the flexible four-stick frame

A quadrilateral built from four *rigid* sticks (8 cm, 6 cm, 8 cm, 6 cm) joined by
pivots, driven by a parametric shear:

- **Scene 3** sweeps the interior angle from 90° → 56° → 124° while a live angle
  arc counts the degrees and the four side lengths never change. The corner
  positions come from `quad_points()`, so the shear is exact — nothing is
  stretched.
- **Scene 5** adds the fifth stick along diagonal `BD`; the frame is pushed with
  the same force and no longer moves.
- **Scene 8** repeats the idea on a window frame, which becomes rigid with one
  diagonal brace.

## Mathematical Content

| Concept | Statement | Shown as |
|---|---|---|
| Four sides are not enough | `AB = CD = 8`, `BC = DA = 6` fixes no angles | three different shapes from the same sticks |
| Uniqueness = congruence | same data ⇒ congruent figures | shape 2 slid onto shape 1: the tops diverge |
| Fifth measurement | `AB, BC, CD, DA, BD` | the diagonal brace |
| Why it works | `△ABD` and `△BCD` each fixed by SSS | the two triangles part and rejoin |
| The general rule | 4 sides + 1 suitable independent measurement | boxed rule + the five combinations |
| Independence | repeating a side, or the perimeter `28`, adds nothing | the challenge's options A and C |

Construction combinations previewed (Section 3.2): `SSSSD`, `SSSSA`, `SSSDD`,
`SASAA`, `SASAS` — with `SSSSD` highlighted as the one just demonstrated.

## Scene Overview (measured times)

| Scene | Time | Learning goal | Visual | Key on-screen text | Math |
|---|---|---|---|---|---|
| Title | 00:00–00:09 | Frame the question | leaning frame + brace | Why 4 Sides Aren't Enough | 4 sides + 1 = 1 shape |
| 1 | 00:09–00:25 | The Kamal/Joseph mystery | two pinned sheets, rectangle vs slanted frame | Same Four Sides. Different Shapes! | 8, 6, 8, 6 |
| 2 | 00:25–00:39 | What four sticks give you | two 8 cm and two 6 cm sticks assemble, joints pin them | Four Sticks, One Rectangle | `AB=CD=8`, `BC=DA=6` |
| 3 | 00:39–00:57 | Non-uniqueness | live shear with degree arc; three ghost outlines | The Angles Changed. The Lengths Didn't! | same 8, 6, 8, 6 |
| 4 | 00:57–01:13 | What "unique" means | three shapes, then shape 2 slid onto shape 1 | Not Congruent | four sides are not enough |
| 5 | 01:13–01:31 | The fifth measurement | dashed BD → rigid green stick; push has no effect | The Fifth Measurement | `AB, BC, CD, DA, BD` |
| 6 | 01:31–01:57 | Why the diagonal works | two triangles part along BD and rejoin | Two Fixed Triangles | `△ABD`, `△BCD`, SSS |
| 7 | 01:57–02:14 | The general rule | quad with 4 sides + diagonal, five combo cards | 5 INDEPENDENT MEASUREMENTS | `SSSSD` … `SASAS` |
| 8 | 02:14–02:24 | Real-world use | window frame shears, then takes a brace | Make the Frame Rigid | sides + fixed diagonal |
| 9 | 02:24–03:04 | Student challenge | YOUR TURN, options A/B/C, THINK clock, reveal | Which extra measurement? | `8+6+8+6=28` is not new |
| 10 | 03:04–03:34 | Recap | frame bends, then locks with BD | Five Independent Measurements | boxed `AB…BD` |

## Scene Notes (Manim implementation)

- **Sticks and joints.** `stick()` draws a painted body with a highlight down its
  middle; `joint()` puts a metal pin at every corner, so the frame reads as
  physical material rather than thin lines. `frame_at(theta)` builds the whole
  frame from `quad_points()`, which keeps `AB = CD = a` and `BC = DA = b` exactly
  for every interior angle.
- **Scene 3** drives everything from one `ValueTracker` through `always_redraw`,
  including the side labels and a live angle arc whose degree label updates each
  frame (`other_angle` is switched once the frame leans past 90°).
- **Scene 5** grows the diagonal from a dashed line into a rigid green stick, then
  pushes the frame: it quivers 2° and returns, and the diagonal's length is shown
  to be the thing that is now fixed.
- **Scene 6** fills `△ABD` and `△BCD` with different colours, separates them along
  the diagonal and closes them again, with the SSS reminder in between.
- **Scene 8** uses `window_frame()` — outer frame, two mullions and a glass tint —
  redrawn from *two* trackers (angle and brace) so the brace appears without
  transforming a redrawn mobject.
- **Scene 9** runs the shared `story_common.play_challenge_countdown()` THINK
  clock, then dims options A and C with their reasons and locks the frame by
  drawing `BD`.

## Key Pedagogical Safeguards

1. **The four side lengths never change during the shear.** The corner positions
   are computed from the angle, so the demonstration is honest: an animation that
   dragged a vertex would quietly stretch the sides.
2. **Uniqueness is congruence, not screen position.** The video says explicitly
   that turning, sliding or flipping is allowed; scene 4 shows two shapes that are
   *not* congruent by sliding one onto the other side-by-side.
3. **The fifth measurement must be independent.** Scene 9 makes the point with
   three options: repeating an 8 cm side and quoting the perimeter (`28`, already
   implied) both add nothing, while fixing `BD` adds a new constraint.
4. **Five is the general rule, not a demand for five numbers in every special
   case.** The video presents the combinations as a preview and stresses
   "independent, suitable and consistent".
5. **No compass construction yet.** This is the uniqueness video; the actual
   ruler-and-compass procedures belong to the later Chapter 3 topics.

## Final Production Check

Delivered as `quadrilateral_uniqueness_and_five_measurements.py`
(`QuadrilateralUniquenessStory`):

- **Masters:** `media/videos/quadrilateral_uniqueness_and_five_measurements/1080p60/QuadrilateralUniquenessStory_captioned.mp4`
  (1920×1080, 60 fps, 214.2 s) — the delivered master — and the 360p30 review
  copy, both with the series caption style burned in.
- **Label clearance (the "broken tick marks").** The length labels were placed a
  fixed 0.26 units out from their side, but a "6 cm" label is over a unit wide, so
  on a *vertical* side the line ran straight through the text — the fragments of
  the side visible between the glyphs looked like stray tick marks, and both
  sheets in scene 1 had a label overlapping an edge. `side_label()` now pushes
  each label out along the outward normal by its own half-extent plus a gap, so a
  label can never touch the side it names; the scene-1 figures were also made
  smaller inside slightly larger sheets so drawing, labels and border all fit.
- **Correct angle marking.** At the rectangle the corner at `A` carries the
  **square (reversed-L) symbol**; once the frame is sheared the arc sweeps
  **inside** the figure between the two sides. The earlier `other_angle` switch
  drew the reflex arc *outside* the corner for obtuse angles while the label read
  e.g. 121 — wrong on both counts.
- **Scene 3 reads as three shapes, not a smear.** The three configurations are now
  three separate small quadrilaterals side by side, each labelled with its
  interior angle (90°, 56°, 124°), and the live frame is faded out *before* they
  appear (cross-fading left the old side labels sitting on the new shapes).
- **Overlap fixes.** The scene-7 heading was wide enough to run into the
  "Mathematics" badge (now 21 pt); the scene-9 options are spaced further apart so
  each reason note sits clear of the option above it.
- **Recap uses the series' summary rows.** Scene 10 now carries three numbered
  rows naming the measurement each sentence refers to — "Four sides alone:
  `4 sides`", "Add one suitable measurement: `+1 measurement`", "Five independent
  measurements: `AB, BC, CD, DA, BD`" — plus the boxed formula and the closing
  line, matching the recap style of the other Story-Mode videos.
- **Text clarity pass (headings never look truncated).** Every title, subtitle,
  heading and long formula **fades in whole** — a capped `Write()` used to draw
  them letter by letter for up to three seconds, so mid-render frames showed
  "A Geome…", "Four Sticks, One", "The Fifth Measureme", "Two Fixed Triangl",
  "5 INDEPENDENT MEASURE", "Make the Fra", "Five Independent Meas". Text writes
  are capped by `quick()` (0.85 s) and the window's remaining time goes to the
  diagram the narration is describing. The title/subtitle gap was opened (title
  +1.85, subtitle +0.95) so the descender of "Enough" cannot touch the line below.
- **More physical diagram.** Each stick is now a dark outline, a painted body and
  a highlight down its middle, with metal joint pins at every corner.
- **Sync audit** (`audit_sync_overlap.py`, against the real SRT): **every one of
  the 12 narration beats matches its audio exactly (0.00 s)**; only the closing
  flourish on the Thank-You card adds 0.37 s. (A regression introduced while
  capping text writes — scene 2 lost 4 s — was caught by this audit and fixed, so
  the beat totals are exact again.)
- **Layout audit:** no text-in-text, partial-overlap, out-of-board, near-badge,
  LaTeX-as-text or empty-TeX flags. What remains is the `TEXT-ON-ARROW` report for
  the two `BD` labels: the audit compares bounding boxes, and a full-length
  diagonal's box covers the whole figure, so any label inside the figure is
  reported — the labels are visually clear of the line (checked frame by frame).
- **Content verification on the delivered file:** 64 captions, **0 captions in
  silence**, **0 speech blocks uncaptioned**, caption text 534 words = narration
  534 words.
- **TTS pre-check:** all twelve narration lines were generated and checked before
  the render; every line came back with audio and word boundaries.
- **Vertex letters on the challenge figure.** The YOUR TURN frame in scene 9 had
  no `A, B, C, D`, so the diagonal `BD` named in the options and drawn in the
  reveal had nothing to refer to. The four corners are now labelled like every
  other figure in the video (`A` bottom-left, `B` bottom-right, `C` top-right,
  `D` top-left), and when the diagonal is drawn in the reveal the `B` and `D`
  labels pulse green so the "diagonal BD" is visibly the stick joining them.
- **Independent frame sweep (187 images).** A separate pass over the delivered
  360p30 file (one frame every ~4 s plus targeted crops) found two blockers and
  ten cosmetic items; all are fixed in this master:
  1. scene 5 cross-faded "What if we add one more measurement?" into "The diagonal
     holds it in place." at the same y, printing both on top of each other — the
     first line now leaves before the second arrives;
  2. the THINK clock sat on board centre and hid the B and C option badges in
     scene 9 — it now sits in the gap between the figure and the options (the
     figure and the options moved apart to open that gap);
  3. the live angle readout now carries its degree sign ("85°", "122°") to match
     the static 90°/56°/124° labels;
  4. the highlighted `SSSSD` card is ringed (`Circumscribe`) instead of recoloured,
     so its sub-line stays legible;
  5. the combination cards and the boxed rule above them share one column and no
     longer touch;
  6. the scene-7 heading reads "FIVE INDEPENDENT MEASUREMENTS" (the chalk-script
     "5" was ambiguous with "S" at 360p) and is clear of the badge;
  7. the two lowest board lines were raised 0.1 units off the bottom frame;
  8. recap row ③ no longer repeats the boxed list — it reads "5 measurements";
  9. a new diagonal is built without the dark outline, so it is green from its
     first frame instead of flashing navy on the dark board;
  10. the two triangles now part along the diagonal *with* their vertex letters,
      so no letter is left floating away from the shape it names.
  The sweep also confirmed CLEAN: no truncated or half-drawn text anywhere (all 14
  headings, both rules, the perimeter sum and the boxed list fade in whole), no
  label sitting on a line, the 90° square symbol and inside-sweeping arcs, the
  three labelled configurations, the recap rows, and the left/right margins.
- **Known cosmetic note:** manim finishes this render with a `FileNotFoundError`
  in its *post-combine* housekeeping (it tries to touch one cached partial movie
  file that was already consolidated). The delivered movie is complete — the final
  frame shows the full Thank-You card, the last caption ends at 211.8 s of a
  214.2 s video, and both verifications pass.
- **Proof frames:** `proof_heading_complete.png`, `proof_scene2_rule.png`,
  `proof_title_spacing.png`, `proof_recap_spacing.png`, `proof_shear.png`,
  `proof_diagonal.png`, `proof_combinations.png`, `proof_challenge.png`.

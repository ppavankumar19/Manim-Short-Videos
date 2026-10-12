# Production-Ready Storyboard

**VIDEO TITLE:** How to Construct a Quadrilateral Given 4 Sides and 1 Angle
**TOPIC:** Construction of a Quadrilateral from Four Sides and One Angle
**CLASS / CHAPTER:** Class 8 Mathematics — Chapter 3 — Construction of
Quadrilaterals
**STORYMODE:** 02 (second video of the Class 8 Chapter 3 set)
**LLM KEY / FUNCTION NAME:** `construct_quadrilateral_4sides_1angle`
**DURATION (measured):** 4 min 15.5 s (255.5 s) for the delivered 1080p60 master
with captions burned (the 360p30 review copy runs 255.1 s), 78 captions /
657 words
**TEXTBOOK REFERENCE:** Telangana SCERT, Class VIII Mathematics (English
Medium), 2025–26 edition, Chapter 3 — Construction of Quadrilaterals: the
"four sides and one angle" construction, **Example 1**
(`PQ = 4.5`, `QR = 5.2`, `RS = 5.5`, `PS = 4`, `∠RQP = 120°`) and
**Exercise 3.1(a)** (`AB = 5.5`, `BC = 3.5`, `CD = 4`, `AD = 5`, `∠A = 45°`).

---

## Learning Objective

By the end of this video, students should be able to:

- Recognise the data pattern: **four sides and one angle**.
- Choose the **first triangle** correctly — two sides and the *included* angle
  (S.A.S.) — instead of starting with the angle on its own.
- Draw `PQ` with a ruler and set out the 120° angle at `Q` with a protractor.
- **Set a pair of compasses** to a given length and draw the arc that fixes the
  third vertex `R`.
- Locate the fourth vertex `S` as the **intersection of two arcs** whose radii
  are the two remaining sides.
- Join the last two sides and **verify all five measurements** on the finished
  figure.
- Apply the same four-step plan to a fresh exercise (Exercise 3.1(a)).

**Primary takeaway:** three measurements (two sides + the included angle) build
the first triangle; the two remaining sides become the radii of two arcs, and
where those arcs cross is the fourth vertex.

## Why-Needed Hook

The previous video showed that four sides alone can bend into infinitely many
shapes. So the natural question — and the one the title card asks — is:
**"if the measurements match, why don't the shapes?"** … and then, *how do you
actually draw the one shape the five measurements describe?* This video answers
it with ruler, protractor and compass, exactly as the textbook does.

## Core Visual Metaphor — five measurements split 3 + 2

Every scene is built on the same split of the five given numbers:

```
 PQ = 4.5  QR = 5.2  RS = 5.5   PS = 4   ∠RQP = 120°
 └────── 3 measurements ──────┘ └──── 2 measurements ────┘
        build triangle PQR          radii of two arcs
                                     → the fourth vertex S
```

- **Scene 1** lays the five measurements out as a **centred** stack of cards and
  boxes the words **"4 Sides + 1 Angle"** underneath them.
- **Scenes 4–5** build triangle `PQR`: the ruler draws `PQ`, the protractor sets
  out the 120° ray at `Q`, and a pair of **compasses set to 5.2 cm** draws the
  arc that cuts that ray — the crossing point *is* `R`.
- **Scene 6** draws the 4 cm arc about `P` (again with the compasses in view)
  and the 5.5 cm arc about `R`; both arcs pass **through** `S`, so their
  crossing visibly *is* the fourth vertex.
- **Scene 7** joins `PS` and `SR` and ticks off all five measurements.

## The figure is constructed, not sketched

`example_frame()` builds the quadrilateral the way the construction does it, so
the drawing satisfies the given data exactly:

| given | how the point is found | measured off the render |
|---|---|---|
| `PQ = 4.5` | `Q = P + (4.5·s, 0)` on the base | 4.50 |
| `∠RQP = 120°` | the **interior** angle at `Q`, between `QP` (pointing back left) and `QR` — so `QR` leaves `Q` at 60° above the base | 120.0° |
| `QR = 5.2` | `R = Q + 5.2·s ∠60°` | 5.20 |
| `PS = 4`, `RS = 5.5` | `S` = intersection of the 4 cm circle about `P` and the 5.5 cm circle about `R` | 4.00, 5.50 |

`proof_construct.png` draws both figures from these helpers and prints the side
lengths and the angle **re-measured from the computed vertices**.

Layout: `P` bottom-left, `Q` bottom-right, `R` top-right, `S` top-left — the
120° corner at `Q` opens upward into the figure, which is how the textbook draws
it.

## Mathematical Content

| Concept | Statement | Shown as |
|---|---|---|
| The data pattern | `PQ, QR, RS, PS` + `∠RQP` | five measurement cards + boxed "4 Sides + 1 Angle" |
| Which three first | `PQ`, `QR` and the angle *between* them | `△PQR` highlighted, "S.A.S" card |
| The angle alone fixes direction | the 120° ray says *where* `R` lies, not how far | dashed ray from `Q` through `R` |
| The second side fixes the distance | compasses set to 5.2 cm, needle at `Q`, pencil cuts the ray at `R` | compass + arc + yellow dot at `R` |
| The fourth vertex | `S` is 4 cm from `P` **and** 5.5 cm from `R` | two arcs crossing at `S` |
| Verification | all five numbers re-read off the finished figure | five green tick rows |
| The reusable plan | Sketch → Triangle → Arcs → Join → Verify | four numbered method cards |
| Same plan, new data | `AB=5.5, BC=3.5, CD=4, AD=5, ∠A=45°` | YOUR TURN + reveal of `△BAD` |

## Scene Overview (measured times)

| Scene | Time | Learning goal | Visual | Key on-screen text | Math |
|---|---|---|---|---|---|
| Title | 00:00–00:11 | Frame the problem | leaning `PQRS` outline + step tag | Construct a Quadrilateral | Four Sides and One Angle |
| 1 | 00:11–00:34 | The five given measurements | centred card stack; boxed "4 Sides + 1 Angle"; "Where should we start?" | Four Sides and One Angle | `PQ=4.5 … ∠RQP=120°` |
| 2 | 00:35–00:53 | Sketch first | deliberately *not*-to-scale `PQRS`, every label, 120° at `Q` | STEP 1 — Rough Sketch | not to scale |
| 3 | 00:54–01:10 | Choose the first triangle | `△PQR` fills in; S.A.S cards in the free right column | Use 3 of the 5 Measurements First | `Side+Angle+Side` |
| 4 | 01:11–01:30 | Draw `PQ`, set the angle | ruler line + protractor at `Q` + 120° ray | STEP 2 — PQ and the 120° Angle | `R` lies *on* the ray |
| 5 | 01:31–01:43 | Fix `R` with the compasses | **compasses set to 5.2 cm**, needle at `Q`, pencil draws the arc that cuts the ray | Triangle PQR is Fixed | `QR = 5.2 cm` |
| 6 | 01:44–02:07 | Locate `S` | compasses draw the 4 cm arc about `P`; the 5.5 cm arc about `R` joins it — they cross at `S` | STEP 3 — Locate S | `PS = 4`, `RS = 5.5` |
| 7 | 02:08–02:32 | Complete + verify | white `PQ`,`QR` + green `PS`,`SR`; five tick rows | Required Quadrilateral PQRS | all five used |
| 8 | 02:33–02:54 | The reusable method | four numbered cards + mini construction beside them | The Four-Step Method | Sketch→Triangle→Arcs→Join |
| 9 | 02:55–03:47 | Student challenge | YOUR TURN, `ABCD` + centred cards, 4 s **THINK** clock, reveal of `△BAD` + two arcs → `C` | First triangle: BAD | `∠A=45°`, arcs 3.5 / 4 |
| 10 | 03:48–04:15 | Recap | recap rows + small construction with both arcs through `S` + Thank-You card | Four Sides and One Angle | 3 measurements + 2 radii |

## Scene Notes (Manim implementation)

- **Exact geometry, not a drawing.** `probe_construct.py` replays the whole
  scene before a render is spent, and `proof_construct.png` prints the
  re-measured values.
- **The arcs are drawn with a pair of compasses.** `compass_tool()` builds the
  instrument — two outlined steel legs, a knurled hinge, a needle standing on
  the centre and a wooden pencil whose graphite tip sits exactly on the arc —
  and `compass_arc_drawer()` drives it with a `ValueTracker`: the pencil sweeps,
  the arc grows behind it, then the compasses are laid down. Scene 5 (the 5.2 cm
  arc that fixes `R`) and scene 6 (the 4 cm arc about `P`) are drawn this way.
  The hinge is placed on the far side of the needle-pencil line, and the leg
  length is chosen so the whole instrument stays on the board and clear of the
  figure's labels.
- **The arc of an angle is the interior one.** manim's `Angle` sweeps
  **counter-clockwise** from the first line unless told otherwise, and for this
  figure that sweep is the *reflex* angle (240°): the corner at `Q` was drawn as
  a circular arc looping outside the figure while its label read 120°. The
  helper `angle_mark()` now picks the sweep from the interior bisector, so the
  arc always lies between the two sides (verified: the drawn arc runs
  180° → 120° → 60°, i.e. exactly the 120° corner, and 0° → 22.5° → 45° at `A`).
- **Arcs pass through the vertex they locate.** `locating_arc(centre, target,
  radius, spread)` centres the arc's sector on the direction of the target, used
  for the 5.2 cm arc at `R` (scenes 5, 8), the arcs that cross at `S` (scenes 6,
  8, 10) and the arcs that cross at `C` (scene 9).
- **Text appears crisply, then the board holds.** `appear()` fades a heading,
  card or label in over ~0.45 s and spends the *rest* of the narration window
  holding it. Spreading a fade across a long window leaves text
  half-transparent for seconds, which reads as truncated lettering (a heading
  missing its last letters) or as an empty box (a measurement card whose label
  has not arrived yet) — both were reported on the first 360p cut and are fixed.
  Diagram work is still paced across its window; words are not.
- **The 120° card is introduced by its own sentence.** A bookmark (`b0b`) sits
  at the start of "And angle R Q P is one hundred and twenty degrees", so the
  angle card enters exactly when the narration reaches it instead of crawling in
  for seven seconds.
- **Labels are placed clear of their own lines.** `side_label()` and
  `radius_line()` push a label out along the outward normal by the label's own
  half-extent along that normal plus a gap, so a 1.5-unit-wide label can never
  be clipped by the line it names however steep the line is.
- **Scene 9** runs the shared `story_common.play_challenge_countdown()` THINK
  clock for 4 s (parked in the empty left column so the vertices stay visible),
  then reveals `△BAD`, pulses the 45° arc and grows the two arcs that cross at
  `C`.
- **Scene 10** repeats the whole construction small (lower-left of the board)
  beside the three numbered recap rows.

## Key Pedagogical Safeguards

1. **The included angle is the point.** The video never lets the 120° stand
   alone: it says explicitly that the angle fixes the *direction* of `QR` but
   not its length, which is why the compasses still have to be set to 5.2 cm.
2. **The arcs are real arcs, drawn by a real compass.** The instrument is on
   screen while the arc appears, and the arc is drawn *through* the point it is
   supposed to locate, so "those two arcs meet at exactly one point on this
   side" is visible rather than asserted.
3. **The sketch is honest about being a sketch.** Scene 2 says "not to scale" on
   the board — but its `Q` corner is still drawn opening to 120°, so the angle
   marked on it is the angle that is actually drawn.
4. **Verification is part of the method.** Scene 7 re-reads all five given
   measurements off the finished figure.
5. **Student work is planned, not just watched.** Scene 9 asks which triangle to
   build first, gives 4 s of thinking time, and only then reveals `△BAD` and the
   two arcs that find `C`.
6. **The naming is the student's own phrase.** Nothing on the board uses an
   acronym: the pattern is always written out as **4 sides + 1 angle**, in the
   title card, the boxed strip, the method card heading and the recap — and the
   narration says the same words.

## Final Production Check

Delivered as `construct_quadrilateral_4sides_1angle.py`
(`ConstructQuadrilateral4Sides1AngleStory`):

- **Delivered master:** `media/videos/construct_quadrilateral_4sides_1angle/1080p60/ConstructQuadrilateral4Sides1AngleStory_captioned.mp4`
  (1920×1080, 60 fps, 255.5 s, 42.6 MB) with the series caption style burned in,
  copied into the chapter's `final_videos/` (SHA-256 verified against the source).
- **Review copy:** `media/videos/construct_quadrilateral_4sides_1angle/360p30/ConstructQuadrilateral4Sides1AngleStory.mp4`
  (640×360, 30 fps, 255.1 s) with the matching ground-truth `.real.srt`.
- **Voice sync** (`audit_sync_overlap.py`): **11 of the 12 narration beats match
  their audio to 0.00 s**; scene 6 overruns by 0.12 s and the closing flourish
  on the Thank-You card adds the usual 0.37 s. The audit now counts *holds* as
  well as animations towards a beat's time, since a beat can be kept in step by
  holding the board just as much as by animating.
- **Real captions:** `verify_sync` — 78 captions, first at 0.18 s, last at
  253.14 s of a 255.50 s video, **0 captions in silence**, **0 speech blocks
  uncaptioned** → **PASS**. `verify_captions` — narration 657 words = SRT 657
  words → **PASS (word for word)**.
- **Layout/collision audit:** **no** out-of-board, text-in-text,
  text-on-line, text-on-side, text-outside-box, near-badge or empty-TeX flags.
  `TEXT-ON-ARROW` is confirmed by sampling the line and measuring the *real* gap
  to the text's box, so bounding-box false positives no longer hide genuine hits
  (the invisible `ValueTracker` that drives the compasses is excluded from the
  scan), and a matching `TEXT-ON-SIDE` check samples each **polygon's outline**
  — a label lying on a figure's *side* is the same defect as a label on a line,
  but a polygon is an area frame, so it needed its own check (it is what hid the
  `AD = 5` label sitting on the `AD` side).
- **Second review round (this build):**
  1. **The opening now matches the chapter's other title cards.** The title card
     was rebuilt the way storyboard 03's is: `Construct a Quadrilateral` with
     `Four Sides and One Angle`, a small quadrilateral centred under it, **this
     video's defining measurement drawn and flashed** (the 120° angle at `Q`,
     since the given angle is what distinguishes this case), and the same
     arrow-style step line — now `Angle → Triangle → Arcs → Join`.
  2. **`QR = 5.2 cm` overlapped a side.** Inside the triangle the label is wider
     than the triangle itself, so its end ran into the `P–R` side; just outside
     the `Q–R` side the compass arc grazed it. It now sits to the right of the
     figure, below the corner at `R`, clear of both (measured gaps: 0.53 to the
     arc, 0.27 to the sides).
  3. **`AD = 5` was printed across the `A–D` side** in the scene-9 reveal — a
     fixed offset had put it back on the line it names. It is now placed by
     `side_label()` outward from the triangle's own centroid.
  4. **"Which triangle comes first?" is centred** on the board's centre line
     under the figure (it was pushed to the left).
- **This revision (from the reviewer's notes):**
  1. **Headings looked truncated.** They were not clipped — they were caught
     mid-fade, so at a scene boundary the right-hand letters were faint enough
     to read as missing. All headings/cards/labels now arrive in ≤0.45 s and the
     board then holds (the beat still ends exactly on its bookmark).
  2. **A stray empty box appeared below "PS = 4".** It was the 120° card fading
     in across a 7 s window: the card's dark box arrived long before its label
     was legible. The card now enters crisply on its own sentence.
  3. **Title card** now reads **"Construct a Quadrilateral"** with the subtitle
     **"Four Sides and One Angle"** (no acronym).
  4. **Scene 1 is centred on the board's centre line** — heading, card stack
     (centre-aligned, so the boxes line up) and the boxed strip **"4 Sides + 1
     Angle"**, with "Where should we start?" under it.
  5. **"Side + Angle + Side"** was crowding the board's frame and the corner
     badge: both S.A.S cards now sit in the free right-hand column at
     `y = -0.55 / -1.15`, and the `QR = 5.2` label is placed outward from the
     figure's centroid.
  6. **"R must lie somewhere on this ray."** was pushed into the ray's corner;
     it is now centred under the figure at `y = -1.85`.
  7. **The measurement-box stack in scene 9 was ragged** (left-aligned cards of
     different widths): the stack is centre-aligned with a roomier 0.20 gap and
     sits clear of the frame.
  8. **"First triangle: BAD" overlapped the vertex `C` and the crossing arcs**:
     it now sits below the card stack, well clear of both.
  9. **The arcs are now drawn by a pair of compasses** (legs, hinge, needle and
     pencil) rather than appearing by `Create()`.
  10. **No "S.S.S.S.A" anywhere** — board text and narration both say
      "four sides and one angle".
  11. **Every entrance animates.** A first pass bounded some diagram entrances
     by the bookmark they had just passed, which clamped them to a single frame
     (the four side cards, the rough sketch, the triangle outline and the 45°
     arc popped instead of animating); each window now plays its animation and
     then holds to its bookmark.
- **Frame sweep (360p stills):** title, scenes 1–10 at the moments the changed
  elements appear (including a zoomed check of the compasses at work), plus the
  closing card — no truncated text, no label on a line, no overlap, both
  locating arcs visibly crossing at `S`, all four vertex letters visible during
  the THINK countdown, and the closing "Thank You for Watching!" card complete.
- **Proof frames:** `proof_construct.png`, `frames360/rev2_A.png`,
  `frames360/rev2_B.png`, `frames360/rev2_C.png`.

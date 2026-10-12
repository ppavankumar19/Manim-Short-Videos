# Production-Ready Storyboard

**VIDEO TITLE:** How to Construct a Quadrilateral Given 4 Sides and 1 Diagonal
**TOPIC:** Construction of a Quadrilateral from Four Sides and One Diagonal
**CLASS / CHAPTER:** Class 8 Mathematics — Chapter 3 — Construction of
Quadrilaterals
**STORYMODE:** 03 (third video of the Class 8 Chapter 3 set)
**LLM KEY / FUNCTION NAME:** `construct_quadrilateral_4sides_1diagonal`
**DURATION (measured):** 4 min 40 s (280.5 s) for the 1080p60 master with
captions burned (the 360p30 review copy runs the same length), 84 captions /
703 words
**TEXTBOOK REFERENCE:** Telangana SCERT, Class VIII Mathematics (English
Medium), 2025–26 edition, Chapter 3 — Construction of Quadrilaterals: the
"four sides and one diagonal" construction, **Example 3**
(`AB = 4`, `BC = 3.6`, `CD = 4.2`, `AD = 4.8`, diagonal `AC = 5`), with a
practice set of the same shape used for the student challenge
(`PQ = 4`, `QR = 3`, `RS = 5`, `PS = 4.5`, diagonal `PR = 5.5`).

---

## Learning Objective

By the end of this video, students should be able to:

- Recognise the data pattern: **four sides and one diagonal**.
- Explain what the diagonal does: it joins two opposite corners and turns one
  quadrilateral into **two triangles**.
- Pick the triangle whose **three sides** are all known and construct it by
  **S.S.S** — with no angle needed.
- Set a pair of compasses to each of the two remaining sides and use the two
  arcs to locate the fourth vertex.
- Keep the fourth vertex on the correct side of the diagonal.
- Join the last two sides and **verify all five measurements**.
- Apply the same strategy to a new four-sides-plus-diagonal problem.

**Primary takeaway:** use the diagonal to build one triangle first; then use the
remaining two sides to locate the fourth vertex.

## Why the Diagonal Helps

Video 1 established that four side lengths alone do not fix a general
quadrilateral. Here one more measurement is given — the diagonal `AC = 5 cm` —
and it is the *shared side of two triangles*:

```
            B                     triangle ABC:  AB = 4,  BC = 3.6,  AC = 5
           / \                    triangle ACD:  AD = 4.8, CD = 4.2,  AC = 5
          /   \
     A --/-----\-- C              the diagonal is in BOTH triangles
          \   /
           \ /
            D
```

Because `AB`, `BC` and `AC` are all known, `△ABC` is fixed by its three sides;
the two remaining lengths are then just two radii whose crossing is `D`.

## The figure is constructed, not sketched

`example_frame()` builds the quadrilateral the way the construction does it, so
the drawing satisfies the given data exactly:

| given | how the point is found | measured off the render |
|---|---|---|
| `AB = 4`, `BC = 3.6` | `B` = intersection of the 4 cm circle about `A` and the 3.6 cm circle about `C`, **above** the diagonal | 4.00, 3.60 |
| `AC = 5` | the diagonal, drawn level | 5.00 |
| `AD = 4.8`, `CD = 4.2` | `D` = intersection of the 4.8 cm circle about `A` and the 4.2 cm circle about `C`, **below** the diagonal (the textbook places the fourth vertex on the other side) | 4.80, 4.20 |

`probe_layout.py` re-measures all five values from the constructed vertices
before a render is spent, and the render's own audit checks that no letter sits
on an edge or an arc.

## Mathematical Content

| Concept | Statement | Shown as |
|---|---|---|
| The data pattern | four sides + one diagonal | five measurement cards, the diagonal card in amber |
| What the diagonal does | `ABCD = △ABC + △ACD` | the diagonal splitting the figure into two tinted triangles |
| Which triangle first | `AB`, `BC`, `AC` — three sides | the three sides highlighted, "Side + Side + Side" card |
| The diagonal is shared | it belongs to both triangles | the diagonal stays bright through the whole construction |
| Locating `B` | arc about `A` (4 cm) × arc about `C` (3.6 cm) | compasses set and swept, crossing marked, `AB`/`BC` joined |
| Locating `D` | arc about `A` (4.8 cm) × arc about `C` (4.2 cm), other side | compasses drawn below the diagonal, crossing marked `D` |
| Verification | all five values re-read | five green tick rows |
| The reusable plan | sketch → triangle → arcs → join → verify | four method cards + mini construction |

## Scene Overview (measured times)

| Scene | Time | Learning goal | Visual | Key on-screen text |
|---|---|---|---|---|
| Title | 00:00–00:11 | Frame the problem | faint `ABCD` with the diagonal lit | Construct a Quadrilateral / Four Sides and One Diagonal |
| 1 | 00:11–00:35 | The five given measurements | centred card stack; boxed strip; question | Four Sides and One Diagonal · 4 Sides + 1 Diagonal |
| 2 | 00:35–00:55 | The diagonal makes two triangles | tinted `△ABC` / `△ACD`, the two triangles part and rejoin | One Diagonal, Two Triangles · `ABCD = △ABC + △ACD` |
| 3 | 00:55–01:15 | Pick the S.S.S triangle | `AB`, `BC`, `AC` highlighted, rest dimmed | Use 3 of the 5 Measurements · Side + Side + Side · No angle is needed here |
| 4 | 01:15–01:40 | Draw the diagonal, set the compasses | `AC` drawn; compasses at `A`, pencil drawing the 4 cm arc | STEP 1 — Draw the Diagonal · This diagonal belongs to both triangles · B is 4 cm from A |
| 5 | 01:41–02:03 | Fix `B` and complete the triangle | second arc about `C`; crossing = `B`; `AB`, `BC` joined, triangle filled | STEP 2 — Complete the Triangle · Three sides fix this triangle |
| 6 | 02:04–02:28 | The remaining sides locate `D` | compasses about `A` (4.8) below the diagonal, arc about `C` (4.2), crossing `D` | STEP 3 — Locate D · D satisfies both distances |
| 7 | 02:29–02:50 | Complete and verify | `AD`, `DC` joined; five tick rows | Required Quadrilateral ABCD · All five measurements used |
| 8 | 02:51–03:15 | The reusable method | four method cards + mini construction | Diagonal First · Diagonal → Triangle → Arcs → Join → Verify |
| 9 | 03:15–04:14 | Student challenge | YOUR TURN, practice set, 4 s THINK clock, reveal of `△PQR` and the arcs to `S` | Practice set — made for this video · First triangle: PQR |
| 10 | 04:15–04:40 | Recap | mini construction + three recap rows + Thank-You card | Four Sides and One Diagonal · Diagonal → Triangle → Arcs → Join |

## Scene Notes (Manim implementation)

- **Exact geometry.** `example_frame()` and `practice_frame()` build both figures
  from the numbers with `triangle_apex()` (a circle-circle intersection), never
  by hand-placement: `probe_layout.py` re-measures 4.00 / 3.60 / 4.20 / 4.80 /
  5.00 and 4.00 / 3.00 / 5.00 / 4.50 / 5.50 and confirms `B` is above and `D`
  below the diagonal.
- **The arcs are drawn with real compasses.** `compass_tool()` draws the
  instrument (two outlined steel legs, a knurled hinge, a needle standing on the
  centre, a wooden pencil whose graphite tip sits exactly on the arc) and
  `compass_on()` / `sweep_compass()` park it and sweep it with a `ValueTracker`,
  so the pencil visibly draws each arc. Used for the 4 cm arc about `A`, the
  3.6 cm arc about `C` (the crossing that fixes `B`) and the 4.8 cm arc about
  `A` below the diagonal. Each tool is laid down inside its own narration
  window, and every tool pose was measured to stay on the board and clear of
  every label (clearances 0.13–1.4).
- **Vertex letters are placed for this figure.** `diamond_names()` puts each
  letter in the corner that is actually free: the left vertex up-left, the top
  vertex up-right, the right vertex up-right (above the diagonal, clear of the
  `AC` label) and the bottom vertex out to the down-right — that last one is
  where the two locating arcs cross, and the series' default corner would put
  the letter on them.
- **Text appears crisply, then the board holds.** Headings, cards and labels
  fade in over ≤0.5 s and the window's remaining time is a hold. Diagram work is
  paced across its window; words are not.
- **The diagonal is introduced on cue.** A bookmark sits at the start of "And
  the diagonal A C is five centimetres", so the amber diagonal card enters with
  its own sentence.
- **Scene 2 shows the split physically.** `△ABC` and `△ACD` tint in one after
  the other, part slightly and close again, and the equation
  `ABCD = △ABC + △ACD` is drawn with the diagonal ringed.
- **Scene 9** runs the shared `story_common.play_challenge_countdown()` THINK
  clock for 4 s, parked in the gap between the figure and the card stack so all
  four vertex letters stay visible, then reveals `△PQR` (green) and the two arcs
  that cross at `S`.

## Key Pedagogical Safeguards

1. **The diagonal is not just another side.** Every scene keeps it visible and
   bright: it is the shared side of the two triangles, which is exactly why the
   construction works.
2. **No angle is constructed.** The video says so on the board — with three
   known sides the triangle needs no angle, which is the difference from the
   previous video's S.S.S.S.A case.
3. **Both arc crossings are explained, not asserted.** One arc is "every point
   that is 4 cm from A", the other "every point that is 3.6 cm from C"; their
   common point satisfies both. The same sentence structure is reused for `D`.
4. **`D` stays on the far side.** The video states it and the arcs are drawn
   below the diagonal, matching the textbook.
5. **The construction marks stay.** Compass arcs are not erased when the
   intersection is found; they fade only in the final verification.
6. **The naming is the student's own phrase.** Nothing on the board uses an
   acronym: the pattern is always written out as **4 sides + 1 diagonal**, in
   the title, the boxed strip, the method heading and the recap — and the
   narration says the same words.

## Final Production Check

Delivered as `construct_quadrilateral_4sides_1diagonal.py`
(`ConstructQuadrilateral4Sides1DiagonalStory`):

- **Delivered master:** `media/videos/construct_quadrilateral_4sides_1diagonal/1080p60/ConstructQuadrilateral4Sides1DiagonalStory_captioned.mp4`
  (1920×1080, 60 fps, 280.5 s) with the series caption style burned in, copied
  into the chapter's `final_videos/` with a SHA-256 check against the source.
- **Review copy:** the matching 640×360 30 fps file and `.real.srt` in the same
  topic's `360p30/` folder.
- **Voice sync** (`audit_sync_overlap.py`): **11 of the 12 narration beats match
  their audio to 0.00 s**; scene 4 overruns by 0.07 s, scene 8 by 0.02 s and the
  closing flourish on the Thank-You card adds the usual 0.37 s.
- **Layout/collision audit:** **no** out-of-board, text-in-text, text-on-line,
  text-outside-box, near-badge or empty-TeX flags. `TEXT-ON-ARROW` is confirmed
  by sampling the line and measuring the real gap to the text's box, so
  bounding-box false positives cannot hide genuine hits — it found five genuine
  ones in the first cut (the top vertex's letter on the `BC` side, the bottom
  vertex's letter on the locating arcs in scenes 6/8/9/10, and the `AC` label
  crowding the `C` letter and the compass body), all fixed and re-verified.
- **Real captions:** `verify_sync` — 84 captions, first at 0.18 s, last at
  278.00 s of a 280.49 s video, **0 captions in silence**, **0 speech blocks
  uncaptioned** → **PASS**. `verify_captions` — narration 703 words = SRT 703
  words → **PASS (word for word)**.
- **TTS pre-check:** all twelve narration pieces were generated and checked
  before the render; every line came back with audio and word boundaries.
- **Frame sweep:** title, all ten scenes and the closing card inspected as
  stills, plus zoomed checks of the compasses at work, the two arcs crossing
  exactly at `B`, the crossing at `D` in the mini figure, and the `AC` label
  clear of both the vertex letters and the compass body.
- **Proof frames:** `frames360/gA.png`, `frames360/gB.png`, `frames360/gC.png`,
  `frames360/zoom_ac3.png`, `frames360/zoom_final.png`,
  `frames360/clock2.png`.

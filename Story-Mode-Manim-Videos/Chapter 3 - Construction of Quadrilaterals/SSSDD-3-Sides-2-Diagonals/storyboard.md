# Production-Ready Storyboard

**VIDEO TITLE:** How to Construct a Quadrilateral Given 3 Sides and 2 Diagonals
**TOPIC:** Construction of a Quadrilateral from Three Sides and Two Diagonals
**CLASS / CHAPTER:** Class 8 Mathematics — Chapter 3 — Construction of
Quadrilaterals
**STORYMODE:** 04 (fourth video of the Class 8 Chapter 3 set)
**LLM KEY / FUNCTION NAME:** `construct_quadrilateral_3sides_2diagonals`
**DURATION (measured):** 4 min 39 s (278.6 s) for the 1080p60 master with
captions burned (the 360p30 review copy runs the same length), 87 captions /
719 words
**TEXTBOOK REFERENCE:** Telangana SCERT, Class VIII Mathematics (English
Medium), 2025–26 edition, Chapter 3 — Construction of Quadrilaterals: the
"three sides and two diagonals" construction, **Example 5**
(`AB = 4.5`, `BC = 5.2`, `CD = 4.8`, diagonals `AC = 5`, `BD = 5.4`), with
**Exercise 3.3(a)** — quadrilateral `GOLD` (`GL = 6`, `LD = 5`, `DG = 5.5`,
`OL = 7.5`, diagonal `OD = 10`) — as the student challenge.

---

## Learning Objective

By the end of this video, students should be able to:

- Recognise the data pattern: **three sides and two diagonals**.
- Sort the five measurements and find the triangle whose **three lengths are
  all known**.
- See that one diagonal turns two of the given sides into a **complete
  triangle** (here `△ABC`: `AB = 4.5`, `BC = 5.2`, `AC = 5`).
- Construct that triangle by **S.S.S** — with no angle needed.
- Use the remaining **side and diagonal as two radii** and intersect the arcs
  to locate the fourth vertex.
- Keep the fourth vertex on the correct side of the diagonal.
- Join the last sides and **verify all five measurements**, noting that the
  fifth side was never given — the construction fixed it.
- Apply the same strategy to Exercise 3.3(a).

**Primary takeaway:** three measurements build a triangle; the last side and
diagonal locate the fourth vertex. *3 build, 2 locate.*

## Why Two Diagonals Help

The previous video used the diagonal as the shared side of two triangles. Here
there are **two** diagonals and only three sides, and the pair still reduces to
one triangle plus one located vertex:

```
        B                          triangle ABC:  AB = 4.5,  BC = 5.2,  AC = 5
       / \                         the diagonal AC is the shared side, and all
      /   \                        three of its lengths are given  ->  S.S.S
 A --/-----\-- C                   B is fixed;  D is then the crossing of
      \   /                        "5.4 from B" (the diagonal BD) and
       \ /                         "4.8 from C" (the side CD), on the far side
        D                          of AC.  AD is never given.
```

Sorting the data is the whole lesson: `AB`, `BC`, `AC` build; `CD` and `BD`
locate. Nothing else is needed.

## The figure is constructed, not sketched

`example_frame()` and `practice_frame()` build both figures the way the
construction does it, so each drawing satisfies the given data exactly:

| figure | given | how the point is found | measured off the render |
|---|---|---|---|
| Example 5 | `AC = 5` | the diagonal, drawn level (the shared side) | 5.00 |
| Example 5 | `AB = 4.5`, `BC = 5.2` | `B` = crossing of the 4.5 cm circle about `A` and the 5.2 cm circle about `C`, **above** the diagonal | 4.50, 5.20 |
| Example 5 | `BD = 5.4`, `CD = 4.8` | `D` = crossing of the 5.4 cm circle about `B` and the 4.8 cm circle about `C`, **below** the diagonal | 5.40, 4.80 |
| Example 5 | `AD` | never given — fixed by the construction | 1.12 (not a given) |
| Ex 3.3(a) | `GL = 6` | the diagonal, drawn level | 6.00 |
| Ex 3.3(a) | `LD = 5`, `DG = 5.5` | `D` = crossing of the 5 cm circle about `L` and the 5.5 cm circle about `G`, above | 5.00, 5.50 |
| Ex 3.3(a) | `OL = 7.5`, `OD = 10` | `O` = crossing of the 7.5 cm circle about `L` and the 10 cm circle about `D`, below | 7.50, 10.00 |

`probe_layout.py` re-measures every value from the constructed vertices before
a render is spent (all nine values come back exact), `probe_arcs.py` checks that
each compass arc still passes through the vertex it locates and stays on the
board, and the render's own audit checks that no letter sits on an edge or an
arc.

## Mathematical Content

| Concept | Statement | Shown as |
|---|---|---|
| The data pattern | three sides + two diagonals | five measurement cards sorted 3 + 2 |
| Which three to use | `AB`, `BC`, `AC` — all known | the triangle highlighted, "Side + Side + Side" card |
| The plan | 3 measurements build, 2 locate | BUILD / LOCATE columns, "3 Build. 2 Locate." |
| Locating `B` | arc about `A` (4.5) × arc about `C` (5.2) | compasses set and swept, crossing marked, `AB`/`BC` joined |
| Locating `D` | arc about `B` (5.4) × arc about `C` (4.8), far side | compasses drawn below the diagonal, crossing marked `D` |
| Verification | all five values re-read | five green tick rows |
| The fifth side | `AD` was never given | the `AD` side ringed, "AD was never given" |
| The reusable plan | sketch → triangle → arcs → join | four method cards + mini construction |
| Why not `△ABD` | `AD` is unknown, so it has only two known sides | the note in scene 8 |

## Scene Overview (measured times)

| Scene | Time | Learning goal | Visual | Key on-screen text |
|---|---|---|---|---|
| Title | 00:00–00:13 | Frame the problem | faint `ABCD` with **both** diagonals lit | Construct a Quadrilateral / Three Sides and Two Diagonals |
| 1 | 00:13–00:36 | The five given measurements | `3 sides` row, `2 diagonals` row, boxed strip, question | Three Sides and Two Diagonals · 3 Sides + 2 Diagonals · Which three should we use first? |
| 2 | 00:36–00:59 | Find the complete triangle | `△ABC` tinted, its three lengths highlighted, one diagonal dashed dim | Find a Complete Triangle · Side + Side + Side · One diagonal turns two sides into a triangle |
| 3 | 00:59–01:15 | The 3 + 2 plan | BUILD column (3 cards) / LOCATE column (2 cards), triangle + `D` dot | 3 Build. 2 Locate. · 3 measurements → triangle → 2 measurements → D |
| 4 | 01:15–01:36 | Draw the diagonal, set the compasses | `AC` drawn; compasses at `A`, pencil drawing the 4.5 cm arc | STEP 1 — Draw the Diagonal AC · AC = 5 cm · Every point on this arc is 4.5 cm from A |
| 5 | 01:36–01:53 | Fix `B`, complete the triangle | second arc about `C`; crossing = `B`; `AB`, `BC` joined, triangle filled | STEP 2 — Complete the Triangle · Three sides fix this triangle |
| 6 | 01:53–02:23 | The side and diagonal locate `D` | both radii dashed, cards for `BD`/`CD`, compass about `B`, compass about `C`, crossing `D` | STEP 3 — Locate D · diagonal BD · side CD · One diagonal and one side have located D |
| 7 | 02:23–02:52 | Complete and verify | `CD`, `BD`, `AD` joined; five tick rows | Required Quadrilateral ABCD · AD was never given: the construction fixed it |
| 8 | 02:52–03:22 | The reusable method | four method cards + mini construction | Analyse First · 1 SKETCH / 2 FIND THE TRIANGLE / 3 TWO ARCS / 4 JOIN |
| 9 | 03:22–04:20 | Student challenge (Ex 3.3(a)) | YOUR TURN, `GOLD` with both diagonals, five cards, 4 s THINK clock, reveal of `△GLD` and the arcs to `O` | Exercise 3.3(a) — quadrilateral GOLD · Which triangle comes first? · First triangle: GLD |
| 10 | 04:20–04:38 | Recap | recap figure + three recap rows + Thank-You card | Three Sides and Two Diagonals · 3 build, 2 locate. |

## Scene Notes (Manim implementation)

- **Exact geometry.** `example_frame()` and `practice_frame()` build both figures
  from the numbers with `circle_intersection()`, never by hand-placement:
  `probe_layout.py` re-measures 4.50 / 5.20 / 4.80 / 5.00 / 5.40 and
  6.00 / 5.00 / 5.50 / 7.50 / 10.00 and confirms `B` is above and `D` below the
  diagonal in Example 5 (`△ABC` and `△ACD`), and `O` on the far side of `GL`
  from `D` in Exercise 3.3(a).
- **This quadrilateral is tall.** `AB = 4.5` and `BC = 5.2` put the apex `B`
  about 2.3 board units above the diagonal, so the example is drawn with its
  base at `AC_Y = -0.40` (storyboard 03 sits at `+0.30`); at the storyboard-03
  height the letter `B` collided with the scene heading and the arc about `C`
  reached into the top badge strip.
- **Two-column scenes are balanced, not hugged to the margin.** The challenge
  figure sits at `BOARD_CX - 2.3` and the recap figure at `BOARD_CX - 3.35`, so
  each reads as centred in the left half instead of pushed against the left
  edge with a wide empty band before the right-hand column; the challenge's
  question line moves with it (`BOARD_CX + 0.30`) and the 4 s THINK clock parks
  in the gap (`BOARD_CX + 1.35`). The question and its "Pause and decide"
  prompt both fade out when the reveal starts, which leaves the bottom of the
  board free for the arc about `L` whose pencil sweeps down to `y = -2.44`.
- **Scene 1's two rows are separated by equal gaps.** `3 sides` sits 0.20 above
  its three cards, the `2 diagonals` caption 0.22 below them and 0.20 above its
  own two cards (measured with `probe_sizes.py`); before the fix the caption was
  0.03 below the card row above it and read as part of that row.
- **The arcs are drawn with real compasses.** `compass_tool()` draws the
  instrument (two outlined steel legs, a knurled hinge, a needle standing on the
  centre, a wooden pencil whose graphite tip sits exactly on the arc) and
  `compass_on()` / `sweep_compass()` park it and sweep it with a `ValueTracker`,
  so the pencil visibly draws each arc. Every one of the seven arcs in the video
  is drawn this way: 4.5 about `A`, 5.2 about `C`, 5.4 about `B`, 4.8 about `C`,
  and 7.5 about `L`, 10 about `D` in the challenge.
- **The compasses are actually laid down.** `put_down_tool()` fades a *static
  copy* of the tool and drops the live `always_redraw` object. The tool's updater
  rebuilds it at full opacity every frame, so a plain `FadeOut` never showed and
  the compasses stood on the board over the finished drawing — found in the frame
  sweep, fixed, and re-checked.
- **Arc sectors are biased, not blindly symmetric.** `compass_on(..., bias=)`
  rotates a sector so a tail cannot stray over the figure: the arc about `C` that
  locates `D` sweeps 8° further down (its symmetric tail poked back above the
  diagonal, near `A`), and both challenge arcs sweep 4° further away from the
  quadrilateral. `probe_arcs.py` reports each sector's board bounds and its
  distance to the vertex it must pass through.
- **Labels are placed clear of their own side.** `side_label()` (overridden in
  this module) pushes a length label along the **true outward normal**; the
  earlier centroid-to-midpoint direction is not perpendicular, so a 66° side like
  `AB` ran through its own label. The `BD` radius label also landed on the `AB`
  side, so the two locating distances are shown on cards on the right instead.
- **Text appears crisply, then the board holds.** Headings, cards and labels
  fade in over ≤0.5 s and the window's remaining time is a hold. Diagram work is
  paced across its window; words are not.
- **The challenge clock** runs the shared `story_common.play_challenge_countdown()`
  for 4 s between the figure and the card stack, so all four letters of `GOLD`
  stay visible.
- **No acronyms on the board.** The pattern is always written out — **3 Sides +
  2 Diagonals** — in the title, the boxed strip, the method and the recap, and
  the narration says the same words.

## Key Pedagogical Safeguards

1. **Sorting comes first.** Scene 1 shows the five measurements grouped as
   `3 sides` / `2 diagonals` and asks the question before anything is drawn; the
   answer (the triangle) is earned in scene 2.
2. **The "3 build, 2 locate" split is stated, then used.** Scene 3 names the
   plan; scenes 4–6 execute exactly that split.
3. **Both arcs of every pair are explained, not asserted.** Scene 6 shows the
   two radii first ("5.4 from B" and "4.8 from C"), then draws each arc from its
   own centre with the compasses.
4. **`D` stays on the far side.** The video states it and the arcs are drawn
   below the diagonal, matching the textbook.
5. **The fifth side is called out.** Scene 7 rings `AD` and says it was never
   given — the construction decided it. This is the difference from the
   four-sides case of storyboard 03.
6. **The trap is named.** Scene 8 asks why `△ABD` cannot be built first and
   answers it: `AD` is unknown, so that triangle has only two known sides.
7. **The construction marks stay.** Compass arcs are not erased when the
   intersection is found.

## Final Production Check

Delivered as `construct_quadrilateral_3sides_2diagonals.py`
(`ConstructQuadrilateral3Sides2DiagonalsStory`):

- **Delivered master:** `media/videos/construct_quadrilateral_3sides_2diagonals/1080p60/ConstructQuadrilateral3Sides2DiagonalsStory_captioned.mp4`
  (1920×1080, 60 fps, 278.6 s, 16 716 frames) with the series caption style
  burned in, copied into the chapter's `final_videos/` with a SHA-256 check
  against the source (`096B7343…C42ADDA9`, identical).
- **Review copy:** the matching 640×360 30 fps file and `.real.srt` in the same
  topic's `360p30/` folder.
- **Voice sync** (`audit_sync_overlap.py`): **11 of the 12 narration beats match
  their audio to 0.00 s** (scene 4 overruns by 0.07 s); the closing flourish on
  the Thank-You card adds the usual 0.37 s.
- **Layout/collision audit:** **no** out-of-board, text-in-text, text-on-line,
  text-outside-box, near-badge, LaTeX-as-text or empty-TeX flags. Six genuine
  hits in the first two cuts were fixed and re-verified: the plan's flow line
  touching the triangle; the `AB` label on its own side; the `BD` radius label
  on the `AB` side; the `GL` label on the `O`–`D` diagonal; the letter `B` on
  the two arcs that cross at it; and the challenge compass sweeping across the
  `L` letter and the `GL` label.
- **The audit now runs the per-frame updaters.** `Scene.update_mobjects(0.0)` is
  called after every faked play, so `always_redraw` mobjects are checked at the
  pose they really hold. Without it the pair of compasses stayed frozen at its
  initial pose and the last two hits above were invisible to the audit — they
  were caught by the full-resolution frame sweep instead.
- **Real captions:** `verify_sync` (on the captioned master) — 87 captions,
  first at 0.14 s, last at 276.22 s of a 278.60 s video, **0 captions in
  silence**, **0 speech blocks uncaptioned** → **PASS**. `verify_captions` —
  narration 719 words = SRT 719 words → **PASS (word for word)**.
- **TTS pre-check:** all twelve narration pieces were generated and checked
  before the render; every line came back with audio and word boundaries.
- **Frame sweep:** title, all ten scenes and the closing card inspected as
  stills, plus zoomed checks of the two arcs crossing exactly at `B`, the
  crossings at `D` and `O`, the compasses being laid down, and both bottom notes.
- **Proof frames:** `frames360/gA.png` (the arc pair crossing at `B`),
  `frames360/gB.png` (the crossing at `D` with both arcs),
  `frames360/gC.png` (the challenge arcs meeting at `O`), plus the review tiles
  `frames360/tileA.png`–`tileG.png` and the zooms `zoom_cross.png`,
  `zoom_d.png`, `zoom_note6.png`, `zoom_note7.png`, `zoom_end.png`,
  `zoom_thanks.png`.

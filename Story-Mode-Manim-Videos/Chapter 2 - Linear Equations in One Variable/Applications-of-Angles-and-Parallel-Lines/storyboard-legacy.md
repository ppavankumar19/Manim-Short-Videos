# Production-Ready Storyboard

**VIDEO TITLE:** Applications of Angles and Parallel Lines
**TOPIC:** Linear Equations in Geometry: Angles and Parallel Lines
**CHAPTER:** Chapter 2 — Linear Equations in One Variable
**TARGET CLASS LEVEL:** Class 8
**ESTIMATED DURATION:** 4 minutes 32 seconds (10 teaching scenes + 6 s thinking clock)

**LEARNING OBJECTIVE:** Students should learn to read a geometric diagram,
identify the correct angle relationship, translate that relationship into a
linear equation, solve for `x`, and then return to the diagram to interpret the
angle.

---

## HISTORICAL / WHY-NEEDED HOOK

The textbook gives no historical background here, so the video invents none. It
opens on the mathematical need:

> A diagram shows `(3x+20)°` and `(5x-8)°` — but **geometry** tells us how those
> two angles are related, and that relationship becomes the equation.

## CORE VISUAL METAPHOR — Diagram → Rule → Equation → Solve

```
DIAGRAM -> ANGLE RULE -> EQUATION -> SOLVE        then   x -> back into the diagram
```

The equation must never appear magically: the two angle sectors **physically
leave the diagram and become the terms of the equation**.

## THE TWO RELATIONSHIPS

| Relationship | Rule | Example |
|---|---|---|
| Interior angles on the same side of the transversal | `A + B = 180°` | `(3x+20)+(5x-8)=180` |
| Corresponding angles | `A = B` | `5x = 2x+24` |

## WORKED EXAMPLE (textbook Example 3)

`(3x+20)+(5x-8)=180 → 3x+20+5x-8=180 → 8x+12=180 → 8x=168 → x=168/8 → x=21`
The angles are `3(21)+20 = 83°` and `5(21)-8 = 97°`, and `83+97 = 180` ✓.

## SECOND APPLICATION (corresponding angles)

`5x = 2x+24 → 3x = 24 → x = 8`, so both angles are `5(8) = 2(8)+24 = 40°`.

## STUDENT CHALLENGE (supplementary angles)

Two supplementary angles differ by `34°`: smaller `x`, larger `x+34`
`x+(x+34)=180 → 2x+34=180 → 2x=146 → x=73` → **73° and 107°**.

---

# Visual Identity

- Parallel lines `l` and `m` stay **fixed**, marked with chevrons; the
  transversal `p` has its own colour.
- Angle **arcs + translucent sectors** large enough to read on a phone.
- Angles in the **same relationship share one colour**; equality → matching
  markers (ticks); supplementary → sectors that **combine into a straight line**.
- An angle expression is never detached from its arc without a connecting
  motion (`TransformFromCopy`).
- Bottom 15–20 % stays clear for the caption band.

---

# Storyboard Overview

| Scene | Time | Learning Goal | Visual | Key On-Screen Text | Math |
|---|---|---|---|---|---|
| 1 | 00:11–00:31 | Introduce the idea | Parallel lines + transversal, two arcs | The diagram already contains a clue | — |
| 2 | 00:31–01:00 | Same-side interior angles | Interior band, sectors combine to a straight line | Same-side interior → 180° | `A+B=180°` |
| 3 | 01:00–01:24 | Form the equation | Expressions copy from arcs into the equation | Geometry → Equation | `(3x+20)+(5x-8)=180` |
| 4 | 01:24–01:46 | Solve | Centred chain | Solve for x | `x=21` |
| 5 | 01:46–02:09 | Interpret and check | Values replace expressions on the arcs | Return to the diagram | `83°+97°=180°` |
| 6 | 02:09–02:33 | Corresponding angles | Matching-position arcs pulse together | Corresponding angles are equal | `5x=2x+24` |
| 7 | 02:33–02:52 | Solve the second case | Chain, then 40° on both arcs | Equal angles → equal expressions | `x=8` |
| 8 | 02:52–03:13 | Generalise | Four cards + strip | Identify → Relate → Form → Solve | — |
| 9 | 03:13–03:59 | Student challenge | Supplementary sectors on a straight line | Your Turn | `x+(x+34)=180` |
| 10 | 03:59–04:32 | Final recap | Rule table + takeaway, then Thanks | Geometry gives the rule. Algebra finds x. | `A=B` or `A+B=180°` |

---

# Scene Notes (Manim Implementation)

- **Scene 1:** `l` and `m` are drawn with chalk chevron markers and the
  transversal `p` sweeps in; two translucent angle sectors appear at the two
  intersections and the question *"What relationship connects these angles?"* is
  asked. No algebra yet.
- **Scene 2:** a translucent band marks the region **between** the parallel
  lines; both sectors pulse, labelled `interior` / `same side`; the two sectors
  are then **copied, rotated and laid side by side** along a straight line with
  a `180°` label, and the rule `A + B = 180°` is boxed.
- **Scene 3:** the angle labels `(3x+20)°` and `(5x-8)°` attach to their arcs,
  are highlighted, and `TransformFromCopy` carries them into a centred
  equation, with `= 180` supplied by the rule — so every term has a reason.
- **Scene 4:** the equation is solved in place
  (`3x+20+5x-8=180 → 8x+12=180 → 8x=168 → x=168/8 → x=21`).
- **Scene 5:** `21` returns to the arcs, which now read `83°` and `97°`, and the
  check `83+97=180` is ticked — the distinction between `x` and the angle.
- **Scene 6:** the diagram is redrawn with a matching-position (corresponding)
  pair, the arcs pulse together, and the equality `5x = 2x+24` is formed. The
  rule line `parallel lines → corresponding angles are equal` sits at
  `y = -1.70` and the boxed equation **below** it at `y = -2.38`, so the box
  clears the board's bottom frame by 0.18 units.
- **Scene 7:** `5x-2x=24 → 3x=24 → x=8`, and both arcs update to `40°` with
  matching ticks.
- **Scene 8:** four cards `IDENTIFY / RELATE / FORM / SOLVE` plus the strip
  `Identify → Relate → Form → Solve → Interpret`.
- **Scene 9:** two supplementary sectors on a straight line, `x°` and
  `(x+34)°`, with the series thinking clock; the reveal runs
  `x+(x+34)=180 → 2x+34=180 → 2x=146 → x=73` and the angles become
  **73° and 107°**.
- **Scene 10:** the rule table, the four routine rows and the closing line
  `Geometry gives the rule. Algebra finds x.` make up the **Summary**. After the
  summary the board is cleared and **only the Thank-You template** remains.

## Key Pedagogical Safeguards

Students must not write an equation straight from two expressions. The video
always runs **diagram → relationship → equation**, and the video never shows the
forward direction `diagram → equation` skipping the rule. The symbol between two
angle expressions depends on the geometry: corresponding ⇒ `=`, same-side
interior ⇒ `+` and `180°`. And `x = 21` is **not** the angle — the angles are
`83°` and `97°`.

## Final Production Check

Delivered as `geometry_angles_story.py` (`GeometryAnglesStory`):

- **Masters:** `media/videos/geometry_angles_story/1080p60/GeometryAnglesStory_captioned.mp4`
  (1920×1080, 60 fps, 4:32) and `.../360p30/…_captioned.mp4` (640×360, 30 fps),
  both with the series caption style (`BorderStyle=3` white-on-dark box) burned in.
- **Sync audit** (`audit_sync_overlap.py`) against the real SRT: **0.00 s**
  animation-vs-audio stretch on every beat.
- **Layout audit:** no text/text, text/arrow, out-of-board (top **or bottom**),
  out-of-board-low or badge collisions; equations centred on the board and paired
  compositions centred as blocks.
- **Bottom-bound fix (Scene 7):** the boxed equation used to sit at `y = -2.7`,
  so its box ran to `y0 = -3.03` — past the board's bottom edge (`-2.9`) and into
  the wooden frame. The rule line moved to `y = -1.70` and the boxed equation to
  `y = -2.38`; the rendered 1080p frame now leaves **24 px (0.18 units)** of
  clearance above the frame. The transversal was also re-centred on the board
  (`P_TOP/P_BOT` shifted +0.5 in x), so the whole diagram is symmetric about
  `BOARD_CX` instead of sitting 0.5 units to the left.
- **LaTeX-leak fix (Scene 8):** the card helper chose between `MathTex` and
  `Text` by sniffing the string (`sub.startswith("\\")`), so the `RELATE`
  sub-line `A=B \;\text{or}\; A+B=180` — which starts with `A` — was handed to
  `Text()` and rendered **as raw LaTeX source**. The helper now takes an explicit
  `math=True` flag and the three math sub-lines are real `MathTex` at font 19
  (`A = B or A + B = 180`, `one equation`, `find x`); the routine strip uses
  proper `→` glyphs. A repo-wide sweep of all 44 scene scripts found no other
  place where LaTeX is passed to `Text()`.
- **Geometry checked numerically and by eye:** the two wedges span **118.5° and
  61.5°** (sum exactly **180°**), the corresponding pair both span **118.5°**, and
  each sector's **apex sits exactly on its intersection** (a Manim `Sector` is
  built with its apex at the local origin, so it must be *shifted* into place —
  `move_to` would centre its bounding box and slide the wedge to the wrong side
  of the line).
- **Content verification on the delivered files:** 85 captions, **0 captions in
  silence**, **0 speech blocks uncaptioned**, caption text 701 words = narration
  701 words, and every algebraic step checked (`x=21 → 83°,97°`;
  `x=8 → 40°,40°`; `x=73 → 73°,107°`).

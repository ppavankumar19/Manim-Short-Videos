# Production-Ready Storyboard

**VIDEO TITLE:** Boats and Streams Problems
**TOPIC:** Upstream and Downstream Boat Problems
**CHAPTER:** Chapter 2 — Linear Equations in One Variable
**TARGET CLASS LEVEL:** Class 8
**ESTIMATED DURATION:** 4 minutes 5 seconds (10 teaching scenes + 6 s thinking clock)

**LEARNING OBJECTIVE:** Students should understand how a river current changes a
boat's **effective speed**, how to write the downstream and upstream speeds
algebraically, and how the **same fixed distance** creates the linear equation.

---

## HISTORICAL / WHY-NEEDED HOOK

The textbook gives no historical origin, so the video invents none. It opens on
the physical question:

> **How can the same boat be faster in one direction and slower in the other?**

The river current. With the current the speeds combine; against the current the
current reduces the boat's speed.

## CORE VISUAL METAPHOR — one river, a current that never turns

```
A  ~~~~~~~~~~~~~~~~→~~~~~~~~~~~~~~~  B
                 current
```

Boat speed in still water `x`, stream speed `s`:

```
Downstream  (boat and current together)   x + s
Upstream    (boat against the current)    x - s
```

Two velocity arrows are the recurring visual: stacked tip-to-tail downstream
(they add), opposed upstream (the current visibly eats part of the boat arrow).

## GENERAL RULE

```
v_downstream = b + s        v_upstream = b - s
Distance = Speed x Time
```

## WORKED EXAMPLE (textbook Example 16)

Boat `x` km/h, stream `2` km/h, downstream `5 h`, upstream `6 h`:

```
v_d = x+2   v_u = x-2
5(x+2) = 6(x-2)      (same A-B distance)
5x+10 = 6x-12 -> 5x-6x = -12-10 -> -x = -22 -> x = 22
```

**Boat speed in still water = 22 km/h**, checked by
`(22+2) x 5 = 120` and `(22-2) x 6 = 120`.

## STUDENT CHALLENGE (built from the same textbook model)

Stream `3` km/h, downstream `4 h`, upstream `6 h`:

```
4(x+3) = 6(x-3) -> 4x+12 = 6x-18 -> 30 = 2x -> x = 15
```

**15 km/h**.

---

# Visual Identity

- **Boat's own speed `x`** → one colour; **river current** → another, and the
  current arrows **never change direction** while the boat turns around.
- **Downstream** → boat and current arrows point the same way.
- **Upstream** → they oppose, and the resultant arrow is visibly shorter.
- The **same boat object** is reused; towns A and B never move; the A–B
  distance never changes.
- Clocks carry the times (`5 h`, `6 h`) next to their journeys.
- Large `MathTex`, equations transform rather than reappear, bottom 15–20 %
  clear for the caption band.

**Realistic scenery, drawn from Manim primitives** (the series' own icon
vocabulary): the river is layered water with a `set_points_smoothly` wave for the
surface, a soft deep/shallow boundary wave, sine ripples, `ArcBetweenPoints` flow
arrows with triangular heads, and grassy banks topped with tufts; each village is
**anchored to the bank line** (`town_marker(letter, x, base_y, scale)` builds it
with its base at the origin) so houses, signpost, tree and jetty stand on land
and only the jetty dips into the water; the boat is a six-point hull polygon with
a deck line, a cabin and porthole, a mast, a smoothed belly-sail and a flag, and
it leaves two `Arc` ripples as a wake.

---

# Storyboard Overview

| Scene | Time | Learning Goal | Visual | Key On-Screen Text | Math |
|---|---|---|---|---|---|
| 1 | 00:12–00:36 | Create the physical mystery | River A→B, boat out and back, clocks | The river is moving too | — |
| 2 | 00:36–00:55 | Downstream speed | Boat + current arrows, tip-to-tail | With the current → ADD | `x+2` |
| 3 | 00:55–01:13 | Upstream speed | Boat arrow opposed by the current | Against the current → SUBTRACT | `x-2` |
| 4 | 01:13–01:30 | Connect speed, time, distance | Two lanes with clocks | Distance = Speed × Time | `5(x+2)`, `6(x-2)` |
| 5 | 01:30–01:48 | Discover the key equation | One A–B route, both distances | Same distance! | `5(x+2)=6(x-2)` |
| 6 | 01:48–02:08 | Solve the equation | Centred chain | Solve for the boat's speed | `x=22` |
| 7 | 02:08–02:31 | Verify meaning | Both journeys computed | Check both journeys | `120=120` |
| 8 | 02:31–02:51 | Generalise strategy | Four cards + strip | Direction → Speed → Distance → Equation | `b+s`, `b-s` |
| 9 | 02:51–03:39 | Student challenge | New river, 4 h / 6 h, clock | Your Turn | `4(x+3)=6(x-3)` |
| 10 | 03:39–04:05 | Final recap | River + formulas + takeaway, then Thanks | With → Add. Against → Subtract. | `t_d(b+s)=t_u(b-s)` |

---

# Scene Notes (Manim Implementation)

- **Scene 1:** a realistic chalk river — layered water with a **smooth wavy
  surface** and ripples, curved flowing current arrows, and **grassy banks with
  tufts** — with a **village standing on each bank** (house with roof, windows,
  door and chimney, a signpost carrying the letter, a tree, and a jetty that is
  the only part dipping into the water), and the **same boat** travelling A→B
  (fast) then B→A (slow) with a wake behind it, staying clear of the villages in
  the water below them. `5 h` and `6 h` clock badges appear beside the two
  journeys; no algebra yet.
- **Scene 2:** the boat arrow and the current arrow are laid **tip-to-tail**
  above the river, and the resultant arrow underneath is visibly longer:
  `x + 2`, labelled `Downstream — with the current, add`.
- **Scene 3:** the boat turns around while the current arrows keep flowing the
  same way; the boat arrow points left, the current arrow right, and the
  resultant upstream arrow is **shorter**: `x - 2`, labelled
  `Against the current, subtract`.
- **Scene 4:** two lanes — downstream with the `5 h` clock and `x+2`, upstream
  with the `6 h` clock and `x-2` — feed `Distance = Speed x Time` and produce
  `5(x+2)` and `6(x-2)`.
- **Scene 5:** a single A–B route carries both distances; the two spans lock
  into one and the equality appears: `5(x+2) = 6(x-2)` — the same distance is
  what creates the equation.
- **Scene 6:** the equation is solved in place
  (`5x+10=6x-12 → 5x-6x=-12-10 → -x=-22 → x=22`) and `22 km/h` is boxed.
- **Scene 7:** the check on both journeys: `22+2=24`, `24x5=120`; `22-2=20`,
  `20x6=120`; `120 = 120` with a tick.
- **Scene 8:** three strategy cards (direction, speed, distance) plus the strip
  `Same distance → equate them`.
- **Scene 9:** the challenge uses the series thinking clock
  (`story_common.play_challenge_countdown`); before the pause only the setup is
  shown, after it `4(x+3)=6(x-3) → 4x+12=6x-18 → 30=2x → x=15` and boxed
  **15 km/h**.
- **Scene 10:** the recap chain, four numbered rows and the closing line
  `Current changes the speed. Same distance creates the equation.` make up the
  **Summary**. After the summary the board is cleared and **only the Thank-You
  template** remains.

## Key Pedagogical Safeguards

Students must not memorise “`x+2` downstream, `x-2` upstream” — the **arrows
come first**, so the direction is the reason. Nor should they memorise “multiply
5 here and 6 there”: `5(x+2)` is the A→B distance and `6(x-2)` is the B→A
distance, and the A–B distance is fixed, which is exactly why the two
expressions are equal.

## Final Production Check

Delivered as `upstream_downstream_story.py` (`UpstreamDownstreamStory`):

- **Masters:** `media/videos/upstream_downstream_story/1080p60/UpstreamDownstreamStory_captioned.mp4`
  (1920×1080, 60 fps, 4:05) and `.../360p30/…_captioned.mp4` (640×360, 30 fps),
  both with the series caption style (`BorderStyle=3` white-on-dark box) burned in.
- **Sync audit** (`audit_sync_overlap.py`) against the real SRT: **0.00 s**
  animation-vs-audio stretch on every beat (only the closing flourish runs
  0.30 s long).
- **Layout audit:** no text/text, text/arrow, out-of-board or badge collisions;
  equations centred on the board, the arrow diagrams, lane rows, card row and
  summary list centred as blocks.
- **Content verification on the delivered files:** 77 captions, **0 captions in
  silence**, **0 speech blocks uncaptioned**, caption text 650 words = narration
  650 words (word for word). All arithmetic checked: `5(x+2)=6(x-2) → x=22`,
  `(22+2)×5 = (22-2)×6 = 120`, and `4(x+3)=6(x-3) → x=15`.

# Production-Ready Storyboard

**VIDEO TITLE:** Linear Equation Word Problems
**TOPIC:** Formulating & Solving Word Problems
**CHAPTER:** Chapter 2 — Linear Equations in One Variable
**TARGET CLASS LEVEL:** Class 8
**ESTIMATED DURATION:** 4 minutes 42 seconds (10 teaching scenes + 6 s thinking clock)

**LEARNING OBJECTIVE:** Students should learn how to convert a word problem into a
linear equation by **choosing an unknown**, expressing related quantities in
terms of that unknown, translating the given condition into an equation, solving
it, and finally **interpreting the answer in the original situation**.

---

## HISTORICAL / WHY-NEEDED HOOK

The textbook gives no historical origin for this section, so the video invents
none. It opens on the practical need:

> **Real problems arrive as words, not ready-made equations.**

A park does not announce `4x + 34 = 178`. It says *"the length is 17 m more than
the breadth, and the perimeter is 178 m."* The student's job is to build the
mathematics hidden inside the sentence.

---

## CORE VISUAL METAPHOR — Story → Model → Equation → Answer

```
WORDS  →  CHOOSE x  →  EXPRESS  →  EQUATION  →  SOLVE  →  ANSWER IN CONTEXT
```

The heart of the video is **before** the solving starts: sentence fragments
physically transform into algebraic expressions.

```
"5 more than x"   →   x + 5
"four times x"    →   4x
"after 6 years"   →   x + 6
"next odd number" →   x + 2
"sum is 29"       →   = 29
```

> **Do not solve the words. First translate them.**

---

## GENERAL METHOD — the five steps

1. **Choose the unknown** — name the quantity you do not know.
2. **Express everything else** using that unknown.
3. **Use the given condition** to write ONE equation.
4. **Solve** the equation.
5. **Answer the original question** and check it.

---

## WORKED EXAMPLE (chapter's number puzzle)

> The sum of two numbers is 29 and one number exceeds the other by 5.

smaller `= x`, bigger `= x + 5`,
`x + (x + 5) = 29 → 2x + 5 = 29 → 2x = 24 → x = 12`,
so the numbers are **12 and 17** (check `12 + 17 = 29`).

## AGE-PROBLEM PATTERN

Vijaya `= x`, Mother `= 4x`; after 6 years `x + 6` and `4x + 6`:
`(x + 6) + (4x + 6) = 62 → 5x + 12 = 62 → x = 10`, present ages **10** and **40**.
Only the *translation* is taught in detail here.

## REAL-WORLD APPLICATION (chapter's Example 6 — the park)

Breadth `= x`, length `= x + 17`, with `P = 2(l + b)`:
`2[(x + 17) + x] = 178 → 4x + 34 = 178 → 4x = 144 → x = 36`,
so **breadth = 36 m, length = 53 m** (check `2(36 + 53) = 178`).

## STUDENT CHALLENGE (Exercise 2.2)

The sum of two consecutive odd numbers is 56.
`x` and `x + 2` → `x + (x + 2) = 56 → 2x = 54 → x = 27` → **27 and 29**.

---

# Visual Identity

- **x** → one consistent cyan highlight throughout.
- **Relationship words** (“more than”, “four times”, “after”) → highlighted as
  they turn into symbols.
- **The given condition** (sum, perimeter) → its own accent colour.
- **Words stay on the left, algebra forms on the right**; arrows connect phrase
  to algebra.
- Equations are **assembled from sentence fragments** — never written whole.
- Bottom 15–20 % of the board stays clear for the caption band.
- Large text, never a paragraph on screen.

Persistent layout:

```text
WORDS                        ALGEBRA
smaller number        →        x
5 more                →      x + 5
their sum is 29       →  x + (x + 5) = 29
```

---

# Storyboard Overview

| Scene | Time | Learning Goal | Visual | Key On-Screen Text | Math |
|---|---|---|---|---|---|
| 1 | 00:12–00:30 | Why translation is needed | Park rectangle + two sentence fragments | Where is the equation hiding? | — |
| 2 | 00:30–00:56 | The word→algebra process | Five-stage pipeline, one stage lit at a time | Story to Algebra | `x`, `x+5` |
| 3 | 00:56–01:14 | Recognise language patterns | Phrase → expression rows | Translate the Relationship | `x+5, 4x, x+6, x+2, =29` |
| 4 | 01:14–01:37 | Formulate the worked example | Two number cards assembled into one equation | Build the Equation | `x+(x+5)=29` |
| 5 | 01:37–02:04 | Solve, then return to the story | Equation chain → number cards → check | Answer the question, not just x | `x=12`, `12, 17` |
| 6 | 02:04–02:33 | Age translation | Two age bars + `+6 years` timeline | Time changes every age | `(x+6)+(4x+6)=62` |
| 7 | 02:33–03:15 | Modelling in geometry | Park rectangle, perimeter traced | Relationship + formula = equation | `2[(x+17)+x]=178` |
| 8 | 03:15–03:36 | Generalise the method | Five routine cards | Choose → Express → Relate → Solve → Answer | — |
| 9 | 03:36–04:15 | Student formulates alone | Two odd-number cards, thinking clock | Your Turn | `x+(x+2)=56` |
| 10 | 04:15–04:42 | Final recap | Recap chain + routine rows + takeaway, then Thanks | Translate first. Solve second. | `x → x+5 → x+(x+5)=29 → 12, 17` |

---

# Scene Notes (Manim Implementation)

- **Scene 1:** a real-looking chalk park — bordered lawn with scattered grass
  tufts, two trees with layered canopies, a rippled pond — with the breadth and
  length dimension arrows *outside* the plot and each label outside its own
  arrow (`?` / breadth below, length beside). Two sentence fragments appear on
  the right with the relationship words `17 m more` / `178 m` highlighted. No
  equation is shown.
- **Scene 2:** five rounded cards `UNKNOWN → EXPRESS → RELATION → EQUATION →
  ANSWER` light up in turn with a tiny illustration inside each, then condense
  into the strip `Choose → Express → Relate → Solve → Answer`.
- **Scene 3:** five phrase rows — `five more than x`, `four times x`, `six years
  later`, `the next odd number`, `their sum is 29` — each transforming into its
  algebra on the right; only `x` and `x+5` survive at the end.
- **Scene 4:** question `Which quantity should be x?`; the smaller-number card
  becomes `x`, the larger becomes `x+5`, `TransformFromCopy` carries both into
  one line, and `= 29` is added last, so the equation is visibly *assembled*.
- **Scene 5:** `x+(x+5)=29 → 2x+5=29 → 2x=24 → x=12`, then the two number cards
  come back as `12` and `x+5 = 17`, the check `12+17=29` appears with a tick, and
  the boxed answer `12 and 17` closes the scene.
- **Scene 6:** two horizontal age bars (`x`, `4x`), a `+6 years` arrow that
  shifts both, the future ages `x+6`, `4x+6`, then the condition line
  `(x+6)+(4x+6)=62 → 5x+12=62 → x=10` and the present ages 10 and 40.
- **Scene 7:** the same park kit (trees, pond, grass, fenced border) with
  breadth `x` and length `x+17` labelled outside their own dimension arrows, the
  boundary traced in yellow, `P = 2(l+b)`, then the full construction
  `2[(x+17)+x]=178 → 4x+34=178 → 4x=144 → x=36`; when 36 is found the two
  dimension labels are **replaced in place** by `36 m` and `53 m` (no extra
  chips are dropped on top of the arrows), and the check `2(36+53)=178` closes
  the scene.
- **Scene 8:** five routine cards (`UNKNOWN`, `EXPRESS`, `RELATION`, `SOLVE`,
  `INTERPRET`) each carrying the example from the video, then the memory strip.
- **Scene 9:** the challenge uses the series-standard thinking clock
  (`story_common.play_challenge_countdown`); the pause asks only *“what is the
  next odd number?”* — the equation is revealed afterwards: `x+(x+2)=56 →
  2x+2=56 → 2x=54 → x=27` → boxed `27 and 29`.
- **Scene 10:** the recap chain, four numbered routine rows and the closing line
  `Translate first. Solve second.` form the **Summary**. After the summary the
  board is cleared and **only the Thank-You template** remains — the video ends
  there.

## Key Pedagogical Safeguard

The mistake this video exists to prevent:

> **Seeing numbers in the question and immediately doing arithmetic on them.**

In *“sum of two numbers is 29 and one exceeds the other by 5”*, the numbers 29
and 5 alone do not say what to compute — the **relationships** do
(`smaller = x`, `bigger = x + 5`, `their sum = 29`, and only then
`x + (x + 5) = 29`). Every scene keeps that distinction visible, and every
answer is taken back to the original question — `x = 12` is only the smaller
number; the required answer is **12 and 17**.

## Final Production Check

Delivered as `from_words_to_equations_story.py` (`FromWordsToEquationsStory`):

- **Masters:** `media/videos/from_words_to_equations_story/1080p60/FromWordsToEquationsStory_captioned.mp4`
  (1920×1080, 60 fps, 4:42) and `.../360p30/..._captioned.mp4` (640×360, 30 fps),
  both with the series caption style (`BorderStyle=3` white-on-dark box) burned in.
- **Sync audit** against the real SRT: **0.00 s** animation-vs-audio stretch on
  every beat (only the closing flourish runs 0.30 s long).
- **Layout audit:** no text/text, text/arrow, out-of-board or badge collisions;
  every equation line centred on `BOARD_CX`; the phrase/algebra block, the
  pipeline row, the two number cards and the ages composition are all centred
  as blocks (the routine and summary lists are centred lists with left-aligned
  rows).
- **Content verification on the delivered files:** 90 captions, **0 captions in
  silence**, **0 speech blocks uncaptioned**, caption text 764 words = narration
  764 words (word for word).

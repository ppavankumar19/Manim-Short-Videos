# Process — Going From a New Topic to a Finished Story-Mode Video

This is the reusable playbook for starting a **brand-new** topic in this
series (Telangana Class 8 Maths). It covers everything *before* the Manim
script exists — content sourcing, drafting, and verification — and hands off
to `implementation.md`-style engineering (render/sync/caption loop) once a
concrete video prompt is ready. Treat this as the template to follow each
time a new chapter/topic is picked.

---

## Stage 1 — Source the topic from the textbook

- Start from the actual state textbook (e.g.
  `8 Maths EM 2025-26 Final 08.11.24.pdf` at the repo root), not from
  general knowledge — the video must match what the student is actually
  taught, in the order and notation the textbook uses.
- Identify the exact chapter/section and the one core idea the video should
  teach (one idea per video — e.g. "simple vs compound interest," "density
  of rational numbers," "Pythagorean theorem"). Note any specific numbers,
  formulas, or worked examples the textbook itself uses, since the video
  should stay consistent with them unless there's a good reason to change
  the numbers for clarity.

## Stage 2 — Draft a storyboard with an LLM (NotebookLM)

- Load the relevant chapter (PDF pages, or a trimmed excerpt) into
  **NotebookLM** as a source.
- Ask it to produce a **scene-by-scene storyboard**, not prose — for each
  scene: a short title, and one sentence stating the pedagogical goal of
  that scene ("The Goal: ..."). This mirrors the format already used for
  the Density Property topic (see
  `Story-Mode-Manim-Videos/Density Property of Rational Numbers Story Mode.txt`):
  a numbered list of scenes, each with a concrete visual idea and the
  concept it's proving.
- Push for a storyboard that has a **narrative hook** (characters, a
  concrete scenario, a "twist" moment) rather than a dry list of
  definitions — the story-mode format in this repo always teaches through
  a small story (two friends and their coin chests, an explorer zooming
  into a number line, etc.), not a lecture.
- Save the raw storyboard output as a `.txt`/`.md` file next to the topic
  folder, so it's kept as a record of the source content decisions (as
  already done for Density Property).

## Stage 3 — Verify the content before writing any code

This step matters as much as the render/sync loop that comes later — a
perfectly synced video that teaches something wrong is worse than a rough
one that's correct. Check the drafted storyboard against the textbook for:

- **Mathematical correctness** — formulas, definitions, and worked numbers
  must be exactly right (no rounding slips, no off-by-one in
  years/terms/etc.).
- **Grade-level appropriateness** — no notation or concepts beyond what a
  Class 8 student has seen; if the textbook defines a term a certain way
  (e.g. what `n` means in the compound interest formula), the video must
  use that same definition, not a more general/advanced one.
- **No unexplained jumps** — every formula term that appears on screen
  should be explained in the narration (this was an explicit requirement
  in earlier videos — "explain every term in the formula").
- **A genuine "aha" moment** — the storyboard should build to one clear
  payoff (e.g. the SI/CI graphs diverging dramatically over 20 years), not
  just a list of facts.

Only once the storyboard survives this check does it turn into an actual
build prompt.

## Stage 3.5 — Check the local Manim reference repos before inventing anything new

Before writing new animation code, check whether a technique, font style, or
diagram type needed for this topic's storyboard already has a working
example somewhere in the repo, rather than reinventing it from scratch:

- **`manim/`** — the actual Manim Community source. Useful for looking up
  exact mobject/animation signatures (e.g. `Arrow`, `Sector`,
  `LaggedStart`, `ReplacementTransform` parameters) and confirming
  capabilities before assuming something isn't possible.
- **`manimce-public-animations/`** and **`Manim-Mobjects-and-Animations/`**
  — collections of worked example scenes. Good for pulling concrete
  animation patterns (graph reveals, transforms, camera moves, text
  styling) and fonts/text treatments that already render well, instead of
  guessing at parameters.
- **`awesome-manim/`** — a curated list of community creators and
  resources, not a library itself. Use it to find inspiration or a
  creator's public repo to look at for a specific effect, not to import
  from directly.
- Prefer **matching this project's existing style** first (chalkboard
  background, chalk-vector icon look, Lato font, established palette) —
  only reach into these reference repos for a *technique* (how to animate
  something) or to confirm a *capability* exists, not to copy a different
  project's visual style wholesale.

## Stage 4 — Turn the verified storyboard into a build prompt

The verified storyboard gets rewritten as a **direct instruction to Claude
Code** to build the Manim project. A good prompt at this stage specifies:

- The **topic folder name** to create (matching the repo's per-topic
  folder convention, e.g. `Story-Mode-Manim-Videos/<Topic-Name>/`).
- The **characters/scenario** to use for the story framing, if any.
- The **concrete numbers** to use in worked examples (principal, rate,
  measurements, etc.) — pulled straight from the verified storyboard so
  they don't drift from the textbook.
- The **visual style** to reuse (chalkboard background, chalk-vector icon
  style, VoiceoverScene + edge-tts sync, real per-word SRT captions, sound
  effects) — this repo's established pipeline, referenced rather than
  re-specified from scratch every time.
- The **beat structure** expected (title → hook/story setup → worked
  example(s) → formula breakdown → generalization/zoom-out → recap), based
  on the storyboard's scene list from Stage 2.
- Any **explicit teaching constraints** carried over from Stage 3 (e.g.
  "explain every formula term," "keep principal and interest visually
  separate," "the graph must show a dramatic difference by the end").

This prompt is the handoff point: once it's given, the process continues
exactly as documented in `Simple-vs-Compound-Interest/implementation.md` —
script scaffolding with dynamic constants and bookmarked narration, low-res
render/caption/verify loop, user feedback rounds, then the final 1080p60
captioned render.

---

## Summary of the full pipeline (content → finished video)

```
Textbook chapter (source PDF)
   → NotebookLM storyboard draft (scene list + pedagogical goal per scene)
   → content verification (accuracy, grade level, explained terms, payoff)
   → check local Manim reference repos for reusable animation/diagram/font
     techniques (manim/, manimce-public-animations/,
     Manim-Mobjects-and-Animations/, awesome-manim/)
   → build prompt for Claude Code (topic, characters, numbers, beats,
     style, constraints)
   → Manim project scaffolding (see implementation.md):
       narration + bookmarks → voiceover render → real SRT capture
       → low-res render + caption burn-in → frame-level sync verification
       → feedback/fix rounds → final 1080p60 captioned render
```

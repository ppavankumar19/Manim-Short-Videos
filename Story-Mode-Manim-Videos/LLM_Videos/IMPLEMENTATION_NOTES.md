# Implementation Notes — Chapter 2, Episode 1
### "The Secret Language of LLMs" — tokenisation, in Manim

This records what was actually built, what broke, and how each break was
found. It follows the same purpose as
`Simple-vs-Compound-Interest/implementation.md`: a reusable account of the
engineering, not a restatement of the plan (that is in
`CHAPTER2_EP1_AUDIT_AND_PLAN.md`).

---

## 1. Layout

```
Story-Mode-Manim-Videos/LLM_Videos/
  assets/background.png          supplied neon panel — the whole visual language
  CHAPTER2_BOOK_TEXT_EXTRACT.txt verbatim Chapter 2 text (pp. 37-57), for re-verification
  CHAPTER2_EP1_AUDIT_AND_PLAN.md pre-build audit + plan
  IMPLEMENTATION_NOTES.md        this file

  audio.py        Zephyr voice + real word timings (see §3)
  theme.py        palette, safe area, backdrop, LLMScene base, stage management
  data_traces.py  every value that appears on screen, tagged book/illus
  components.py   the nine reusable families the storyboard asks for
  three_d.py      3D rigs (input grid, console, vault, bench, embedding slab)
  act1_scenes.py  Scenes 01-05   Chapter2Act1
  act2_scenes.py  Scenes 06-08   Chapter2Act2
  act3_scenes.py  Scenes 09-12   Chapter2Act3
  act4_scenes.py  Scenes 13-15   Chapter2Act4

  pipeline_360.py  render -> verify -> burn -> publish, per act
  concat_acts.py   join the four captioned acts into the episode
  _warm.py         pre-synthesise and time one act's narration
  _check_act.py    narration budget + bookmark integrity check
  _inspect_takes.py per-take duration/ratio audit
  _shot_lab.py     single-frame composition lab for 3D rigs
```

Acts render separately so a five-minute act can be reviewed and re-rendered
without touching the other fifteen minutes.

---

## 2. Base class, and the layering trap

`LLMScene(ThreeDScene, VoiceoverScene)` — the MRO was smoke-tested before any
scene was written, because "3D diagrams *with* narration" was the one
requirement that could have been impossible.

The trap: **`ThreeDCamera.get_mobjects_to_display` sends every
`shade_in_3d` mobject (`Surface`, `Sphere`, `Polyhedron`) into a depth-sorted
group that is drawn *first*, and everything else into a z-index group drawn
*last*.** A `Surface` would therefore render *behind* the backdrop.

So every 3D rig here is built from ordinary `Rectangle` / `Line` / `Polygon`
mobjects at real `z` coordinates. They are still perspective-projected by the
camera; they just keep their `z_index` ordering. Depth ordering is then
explicit, via `three_d.apply_depth`.

Second half of the same trap: a *normal* mobject is projected, so the
backdrop swung away with the camera on the first proof render (the panel
tilted into a plane). The backdrop is therefore marked **fixed in frame** —
which skips projection but still participates in z-index ordering, so it
stays behind. `theme.hud()` marks anything that belongs to the frame rather
than the world: titles, provenance chips, footers, and any text that must
stay readable during a camera move.

**Design consequence:** all critical *text* in 3D shots is HUD. Only geometry
is 3D. The first bench render put machine names on the 3D boxes and they were
illegible; pinned labels fixed it with no geometry change.

---

## 3. Narration: Zephyr's voice, the audio's own clock

The brief was "use Zephyr sound", knowing that Gemini's TTS returns **audio
only, no timestamps**, so `gemini_speech_service._calculate_word_boundaries()`
*invents* them by spreading each clip's duration across words by character
count. Measured against real audio that estimate was off by 0.03–0.79 s per
clip, worst on numerals and token IDs — precisely this episode's material.

`audio.HybridZephyrSpeechService` keeps the voice and fixes the clock:

1. synthesise with `GeminiZephyrSpeechService` (sharing the repo's voice cache),
2. measure the clip with `ffprobe` + `ffmpeg silencedetect`: total duration,
   leading silence, trailing silence, and every internal pause,
3. get **real** per-word offsets for the same text from edge-tts (this voice's
   audio is discarded — only its clock is used),
4. resample that timing *shape* onto the Zephyr clip's own measured speech
   span, so both ends are anchored by measurement, not assumption,
5. snap any word that lands inside a measured pause forward to the moment
   speech resumes — a word cannot start during silence.

Everything is cached on disk, so re-renders never re-synthesise or re-measure.

### Two API failure modes, both fixed by retrying

* **Empty response.** The endpoint periodically returns HTTP 200 with
  `finishReason: OTHER` and no audio at all — measured at roughly one call in
  three on the *same* input. The upstream service only retries non-200
  responses, so without a retry the render dies with a bare
  `KeyError: 'content'`.
* **Truncated take.** Worse, because it looks like success: one Act I line
  came back as 32 words in 4.41 s — 7.3 words/second against the voice's
  normal 2.1–3.1. Nothing in the response says "truncated". `take_is_plausible`
  catches it by comparing the clip against how long the same text takes to
  say, plus an independent words-per-second band (2.07–3.10 measured across
  this episode). A bad take is evicted from the voice cache and re-synthesised.

That second check needs the edge reference to be *available*, so `edge_curve`
also retries — a transient edge-tts failure would otherwise silently disable
the truncation test. (It did, once: a take at 2.33× the expected duration got
through, which is why the independent band exists as well.)

### Verified take quality

All 60 beats across the four acts: duration/expected-duration ratio
**0.84–1.43**, words/second **1.73–3.10**. No take is truncated.

---

## 4. Stage management — the bug that cost the most

Three things happen to on-screen objects: they are per-beat, per-scene, or
permanent. Getting that wrong is invisible until the next scene.

The first Act I render leaked its "LANGUAGE MODEL" machine into Scene 02, and
Scene 02's title was drawn straight over Scene 01's. Three distinct causes:

1. **Registering a parent `VGroup` after fading in its children.** The
   terminal was built as `VGroup(term, caret, typed)`, but only the children
   were added to the scene. `FadeOut(parent)` then animates nothing, because
   the parent was never staged.
2. **`VGroup[:1]` slices the *family*, not the top-level members.** Using a
   slice to say "keep the title" would have faded exactly one glyph.
3. **Bookkeeping inversion.** Clearing originally meant "fade everything I
   registered". Miss one registration and the object is orphaned — on stage,
   tracked by nothing, immortal. That is exactly what happened.

The fix inverts it: `_unprotected()` returns *everything on stage that is not
explicitly protected*, so an unregistered object cannot survive a cut.
`dissolve` protects `chrome` + `stage`; `clear_stage` protects only `keep`
and the backdrop, so the title dies at the scene boundary where it should.

### A camera bug with the same shape

`view_3d()` leaves the camera in a perspective orientation. Forgetting
`view_2d()` after a 3D beat means every *later* beat in that scene draws
tilted. Act II Scene 06 hit this; the fix is a `release_stage()` +
`view_2d()` pair after any 3D shot.

### Captions are unconditional now

The first Act I render shipped with captions for **9 of its 19 beats**: only
the beats that happened to end with a provenance chip called `capture_srt`.
Rather than remember, `LLMScene.beat(key)` is a context manager that wraps
`voiceover()` and always captures. The SRT went from 35 cues to 78.

---

## 5. Layout, measured not guessed

The supplied backdrop's glass panel occupies roughly x ∈ [-5.9, 5.9],
y ∈ [-2.1, 3.25]; the reflective floor below is left clear for burned-in
subtitles. `theme.SAFE_*` encodes that, and `fit()` shrinks anything that
overruns it.

Two collisions were found by looking at extracted frames, not by reading code:

* Scene 01's "EXPECTED: NUMERIC INPUT" panel sat on top of the machine's
  "LANGUAGE MODEL" label. Fixed by moving the label *inside* the machine and
  giving the wide machine a wide interior for the numbered slots.
* Scene 02's title overprinted Scene 01's (see §4).

A third: `Mobject.set_opacity()` forces **both** fill and stroke opacity, so
using it to fade distant grid cells turned them solid and hid the digits.
Fade fill and stroke separately.

---

## 6. 3D rigs, chosen by looking

`_shot_lab.py` renders single frames (`manim render -s`) so a camera angle or
rig proportion costs about a second instead of a full scene render. Two rigs
were rejected on the evidence:

* **A corridor of upright frames** (the original "token tunnel") read as a
  stack of plates: with the camera at a low oblique angle, a corridor along
  −z sits almost perpendicular to the view axis. Replaced by
  `input_grid_floor` — numbered input positions lying flat in the X–Z plane,
  read from a ~40° look-down as a runway going away from the viewer. This
  also matches the storyboard's actual wording ("a grid of numbered input
  positions") better than a tunnel did.
* **The laboratory bench** had its labels on the 3D boxes and they were
  illegible. Names and methods moved to pinned HUD labels below the bench.

Rigs that survived as built: `control_console` (tilted plate, three dials),
`vault_wall` (receding row stack for vocabulary lookup), `embedding_slab`
plus `vector_beam`.

---

## 7. Accuracy guards carried into the code

`data_traces.py` holds every on-screen value, tagged `book` or `illus`, and a
provenance chip appears on screen for each. Beyond the audit fixes:

* **No invented token IDs, ever.** The book prints IDs for the musical note
  (8582 / 236 / 113) but none for the Chinese character, so the Chinese
  character is shown as byte-derived pieces with a visible note that no IDs
  are given.
* **Markers rendered as printed**: `[UNK]` for BERT, `<unk>` for FLAN-T5.
  Flattening them would erase a real difference.
* **GPT-2 is labelled "BPE (byte fallback)"**, not "byte-level BPE" — the
  book explicitly says these tokenizers are *not* tokenization-free
  byte-level encoders.
* **The four tokenizer machines are stamped a subset** of the eight the book
  compares.
* **Whitespace rendered visibly.** Four literal spaces render as nothing in
  Pango; the four-space token carries the visible `␣` marker, and a note says
  the marker is a rendering, not a character.

---

## 8. Verification

Two gates, both from the repo's existing toolkit, run per act by
`pipeline_360.py`:

* `verify_sync.py` — container A/V durations, every caption overlapping
  silence-detected speech, every speech block over a second captioned, and
  SRT freshness.
* `verify_captions.py` — the SRT reproduces the narration dictionary word for
  word.

Plus `_check_act.py`, which validates narration budget and, more usefully,
that every `time_until_bookmark("x")` references a mark declared in that
beat's own narration — the failure mode otherwise being a render that dies
twenty minutes in.

Results are recorded in §9.

---

## 9. Render log

All four acts render at 640×360 @ 30 fps with burned-in captions and audio
kept, and both house verifiers pass on every act.

| Act | Scenes | 360p30 duration | verify_sync | verify_captions | narration words |
| --- | --- | --- | --- | --- | --- |
| Chapter2Act1 | 01–05 | 249.8 s | PASS | PASS | 621 |
| Chapter2Act2 | 06–08 | 151.5 s | PASS | PASS | 377 |
| Chapter2Act3 | 09–12 | 249.3 s | PASS | PASS | 625 |
| Chapter2Act4 | 13–15 | 144.7 s | PASS | PASS | 375 |

**Episode:** `final_videos/Chapter2_Ep1_The_Secret_Language_of_LLMs.mp4` —
**796.5 s (13.3 min)**, 640×360, 30 fps, h264 + AAC stereo.

Episode-level check (`verify_sync.py` against the merged SRT):

```
video 796.500s   audio 795.959s   silent tail +0.541s   [ok]
captions: 252   first 0.15s   last 795.92s   (video 796.50s)
speech blocks: 280   speech time 650.9s (81.8% of audio)
captions mostly in silence: 0
speech blocks (> 1.0s) not captioned: 0
RESULT: PASS
```

---

## 9b. Revision: series font, and everything inside the panel

Three problems were reported after the first cut: the typeface did not match
the rest of the channel, elements overlapped, and content sat outside the
backdrop's border.  All three are fixed, and the fixes are now enforced by a
tool rather than by eye.

### The font

**All 25 existing Story-Mode videos use Segoe Print** (measured, not assumed:
`grep '^FONT ='` across every `*_story.py` returns one value, 25 times).  This
episode now uses it for prose *and* for token strings, IDs and code, so the
channel reads as one voice.  Two consequences had to be handled:

* **Segoe Print is wider than Consolas** (4.35 vs 5.06 units for the same
  string at size 18), so several rows that fitted before no longer did.
  `fit()` and explicit scaling were applied where the audit flagged overflow.
* **U+2423 OPEN BOX, the space marker, is not in any installed font.**  Its
  advance width measured 0.04 units at size 26 in Segoe Print, Calibri *and*
  Consolas — i.e. it renders as nothing.  Whitespace is now a *drawn*
  rectangle (`theme.space_marker`), which cannot silently disappear.

### The panel is measured, not eyeballed

`_measure_panel.py` profiles the backdrop's pixels and finds the neon rim's
core at x = −6.04 / +6.03 and y = +3.25 / −2.14 in frame coordinates.  The
safe box is that rim inset by 0.45:

```
SAFE_L, SAFE_R = -5.58, 5.58
SAFE_B, SAFE_T = -1.82, 2.90
```

Every element is now confined to it.  The reflective floor below the rim
carries no content — it belongs to the burned-in subtitles.

### The layout auditor

Eyeballing extracted frames found the two collisions in Act I.  Two is not a
survey, so `LLMScene` grew an audit mode:

```powershell
$env:LLM_LAYOUT_AUDIT = "1"     # "2" also prints box coordinates
manim render --dry_run --resolution 640,360 --fps 30 actN_scenes.py Chapter2ActN
```

It runs after every `play()`, projects each mobject through the camera, and
reports anything that escapes the safe box or collides with something else.
`--dry_run` means no frames are written, so a full four-act survey takes
seconds.  Reports land in `media/layout_audit/<Class>.txt`.

Two subtleties had to be right for the output to be worth reading:

* **Boxes must be the union of *leaf* boxes, not the group's own box.**
  `fixed_in_frame` is recorded per mobject, and a wrapper `VGroup(a, b)` made
  at a call site and handed straight to `play` is *not* in that set even
  though its children are.  Asking such a wrapper for its projection
  projected it as 3D geometry and reported the scene title at the wrong
  height — which showed up as a title/label clash in every 3D shot.
* **Containment is not a collision.**  A label inside its panel, or a
  highlight box drawn around one item of a list, is intentional.  Leaf-level
  comparison was tried and is far too noisy: Segoe Print is a handwriting
  face, so neighbouring glyph boxes inside one word already overlap.  The rule
  that works is group-level comparison, skipping any pair where a group's
  leaves are *all* inside the other's box.

### What it found, and the result

| Act | before | after |
| --- | --- | --- |
| Chapter2Act1 | 38 outside, 17 overlaps | **0, 0** |
| Chapter2Act2 | 31 outside, 16 overlaps | 0, 3 (all intentional highlights) |
| Chapter2Act3 | 17 outside, 13 overlaps | 0, 12 (code-indent + bench bbox) |
| Chapter2Act4 | 14 outside, 12 overlaps | 3, 4 (answer-box highlight) |

The remaining entries are all cases the audit cannot classify on its own:
a highlight box around one item of a list, and the padded bounding box of a
perspective-projected rig (the visible geometry sits well inside it).  Each
was checked against an extracted frame at that timestamp.

Real defects it caught that reading the code had not:

* the scene-01 prompt panel overprinting the title;
* the "no match" label landing on top of the search box;
* the input grid projecting past the rim and onto the provenance chip;
* the console's three in-rig captions overlapping each other — now removed,
  with the pinned HUD labels doing that job;
* the laboratory bench, whose base plate projected below the panel;
* option 3 of the retrieval check overflowing the right edge once Segoe Print
  widened it.

**Syncing was untouched throughout**: no narration text changed, so the voice
cache and every measured word timing stayed valid.  The SRTs regenerate
identically, and both verifiers still pass on all four acts and on the
finished episode.

---

## 9c. Revision: audio-measured sync, and a real 3D kit

Two further complaints after the second cut: the sync still did not match,
and the 3D diagrams did not hold up.

### Sync: the timing now comes from the rendered audio itself

The previous method resampled the edge-tts word curve onto the Zephyr clip.
That is correct only if two different voices pace a sentence identically;
they do not.  Measured across the episode's 61 lines, the estimated word
onsets were off by **255 ms on average and up to 2.9 s** -- which is what
"not matched at all" was.

The replacement is genuine forced alignment, with no new dependencies
(numpy + scipy + PyAV only):

1. synthesise the line with Zephyr (the take that actually renders),
2. synthesise the same line with edge-tts and keep its *recording* --
   its per-word onsets are known exactly from its WordBoundary events,
3. trim both clips to their speech spans (silence at the heads would
   otherwise absorb alignment),
4. dynamic-time-warp the two recordings against each other on log-mel
   spectra, and map every edge word onset onto the Zephyr take,
5. keep the pause-snapping and the measured end anchors as guards.

The result: every word onset is measured from the audio that ships in the
video.  Validation on all 61 lines: **0 word onsets inside a measured pause**,
and only 3% of word windows near the noise floor (quiet function words).
The same boundaries drive the captions and the animations, so both land on
the spoken word.

Three bugs in the first DTW draft are worth recording, because each one
looked correct in isolation:

* the vectorised row update dropped the horizontal move, so the reachable
  region collapsed to one column per row and `d[n,m]` went to infinity;
  the prefix-min identity
  ``d[i,j] = C[j+1] + min_k<=j ( t[k] - C[k+1] )`` restores it,
* the backtrack could wander into uncomputed cells, where ``inf == inf``
  ties on the diagonal branch and pushes indices negative -- Python's
  negative indexing then read an unrelated row and poisoned the path,
* untrimmed leading silence let DTW absorb a clip's opening stretch for
  free.

``_probe_sync.py`` and ``_probe_one.py`` turn this into a repeatable audit:
they compare the old estimate against the alignment and check every onset
against the real energy envelope.

### 3D: a shading/glow kit instead of flat plates

The rigs were rebuilt on a small production kit in `three_d.py`:

* ``box3d`` -- six faces with per-face shading from a fixed key light, so
  every object reads as having real thickness;
* ``glow`` -- layered translucent stroke copies (neon halo);
* ``floor_reflection`` -- kept in the kit but not used in shots: the user
  requires everything inside the panel rim, and a reflection lives below
  it.

Scenes 06-09 and 15 now use shaded boxes, glowing dials, a status light per
machine, and a vault whose matched drawer slides out of the wall.  Motion is
object-level rather than camera-level: camera orbits repeatedly pushed the
projected rigs past the rim (the layout auditor caught each attempt), while
drawer slides, rising machines and growing vector bars stay inside by
construction.

The auditor gained three rules so its output stays meaningful for rigs:
camera ``ValueTracker``s are machinery and are skipped; parts of one rig
(carried via a ``rig`` tag) overlap each other by construction; and a hollow
box around one list item is a highlight, not a collision.

**Final audit state: all four acts report 0 objects outside the panel and
0 collisions.**  Sync is unchanged from §9's checks otherwise: narration
text untouched, so the voice cache, verifiers and SRT word-for-word checks
all hold.

---

## 10. Rebuilding


```powershell
cd Story-Mode-Manim-Videos\LLM_Videos

# narration is cached; this is only needed after editing NARRATION
python _warm.py act1_scenes act2_scenes act3_scenes act4_scenes

# edit act3_scenes.py, then re-render just that act
python pipeline_360.py act3_scenes Chapter2Act3

# rejoin the episode
python concat_acts.py
```

Two developer tools worth keeping:

* `_check_act.py actN_scenes` — narration budget, unique bookmarks, and every
  referenced mark declared. Run it before any render; it catches the class of
  error that otherwise surfaces twenty minutes into one.
* `_shot_lab.py` — `manim render -s` on any class in it gives one frame in
  about a second, which is how the camera angles and rig proportions were
  settled.

**Clear `media/voiceovers/` whenever a bookmark moves but the spoken words do
not** — the cache key is the spoken text, so an unchanged sentence silently
reuses audio that does not know about the new bookmark.


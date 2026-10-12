# Class 6 — Chapter 2 (Whole Numbers) — Audit Report

**Scope:** all five Class 6 story-mode videos, delivered as **1080p60 masters with
burned series-style captions** (360p30 review copies kept alongside them).
**Method:** each topic's own `audit_sync_overlap.py` (per-beat animation time vs
the real audio duration, plus a layout collision sweep), a phrase-level check of
every narration window against the render-truth WAV-retimed word boundaries
(`bookmark_times.py`), then `verify_sync.py` and `verify_captions.py` on the
delivered captioned file.
Audits run sequentially — two manim processes sharing one TeX cache corrupt each
other's `media/texts` files.
**Reproduce:** from this folder, `.venv/Scripts/python.exe class6_audit.py`
(optionally `--json class6_audit.json`).

---

## 1. Deliverables (1080p60, captions burned)

| Video | 1080p60 master | Duration | Beats exact | Max stretch | Layout flags | Captions | Wording |
|---|---|---|---|---|---|---|---|
| 01 Whole Numbers | `whole_numbers_story/1080p60/WholeNumbersStory_captioned.mp4` | 275.9 s | 11/12 | 0.30 s | clean | 84 cues, silence 0, uncaptioned 0 | 706 = 706 |
| 02 Operations on Whole Numbers | `operations_on_whole_numbers/1080p60/OperationsOnWholeNumbersStory_captioned.mp4` | 207.9 s | 11/12 | 0.30 s | clean | 55 cues, silence 0, uncaptioned 0 | 453 = 453 |
| 03 Commutative & Associative | `commutative_associative_story/1080p60/CommutativeAssociativeStory_captioned.mp4` | 236.7 s | 11/12 | 0.30 s | clean | 70 cues, silence 0, uncaptioned 0 | 586 = 586 |
| 04 Distributive Property & Identities | `distributive_property_story/1080p60/DistributivePropertyStory_captioned.mp4` | 243.2 s | 11/12 | 0.32 s | clean | 74 cues, silence 0, uncaptioned 0 | 618 = 618 |
| 05 Geometric Dot Patterns | `dot_patterns_story/1080p60/DotPatternsStory_captioned.mp4` | 266.4 s | 11/12 | 0.37 s | clean | 81 cues, silence 0, uncaptioned 0 | 682 = 682 |

All five are 1920×1080 at 60 fps; every one is **PASS** on `verify_sync.py` (no
captions in silence, no uncaptioned speech) and **PASS** on `verify_captions.py`
(caption text word-for-word identical to the narration). Chapter total: 3 039
narration words, 363 caption cues. The single non-zero stretch in each video is
the closing highlight ring on the Thank-You card.

## 2. What the review pass changed

Every video was re-checked phrase by phrase — which animation happens while which
sentence is being spoken — because the per-beat audit compares only *totals* and
cannot see a beat whose visuals are attached to the wrong line. That pass found
**one defect or lead in almost every scene**; all were corrected before the final
renders.

- **01 Whole Numbers** — pencils are centred in the tray and stay centred as they
  are removed or added; a "remove the last pencil" bug that faded the tray instead
  of the pencil; 12 phrase-level sync errors (the two challenge questions, the
  reveal answers, the `N`/`W` recap rows, "Zero pencils", the set notation, plus
  the title's zero highlight which ran 1.9 s early because a `× 0.6` play
  consumed only 76 % of its window).
- **02 Operations on Whole Numbers** — every number line centred on the board
  (`num_line()` used to lay out from a fixed left-hand `x0`, leaving lines up to
  0.56 units off centre); the "ADDITION → MOVE RIGHT" note no longer collides
  with the boxed answer; 10 phrase-level sync errors (all four recap rows played
  a sentence early, the reveal jumps and scene-2 dots ran early, scene 8 never
  highlighted its RESULT card).
- **03 Commutative & Associative** — 9 fixes: the ASSOCIATIVE card and the
  closing banner in scene 10 each appeared a whole sentence early, plus seven
  windows whose trailing fraction left 24–30 % of the window unconsumed (so the
  next window's visual started during the previous sentence).
- **04 Distributive Property & Identities** — 15 fixes: scene 8 ran a whole
  narration window early in four places (the earnings equation, the common
  multiplier, `100×30` and the `Rs 3000` answer), the scene-9 reveal chain was one
  window early, and the scene-3 highlight box marked the bracket instead of the
  multiplier it was talking about.
- **05 Geometric Dot Patterns** — 13 fixes: the `3+3=6` sum in scene 3 started a
  sentence early and pushed the `2×3=6` rule late; twelve windows were
  under-consumed by their trailing fractions.

**Tooling note:** `bookmark_times.py` originally read the TTS *service* word
times from the voiceover cache, but at render time `synced_voice` replaces those
with times re-derived from the real WAV, so the two drift by up to ~2.8 s on a
mark. The tool now retimes every piece from the cached WAV exactly as the render
does, so the windows it prints are the ones the delivered videos actually follow.

Every caption check is **PASS** (`verify_sync.py`) with **0 captions in
silence** and **0 speech blocks uncaptioned**, and every wording check is
**PASS** (`verify_captions.py`) with the caption text carrying the narration
word for word. Total across the chapter: 3 039 narration words, 363 caption
cues.

## 2. Per-beat sync (measured on the delivered 1080p60 files)

Every video has 12 narration beats. In all five, **11 of the 12 match their audio
exactly (0.00 s)**; the single non-zero entry is the closing flourish of the
recap scene — the highlight ring drawn around the Thank-You card, deliberately
allowed to finish just after the last spoken word, as in the rest of the series:

| Video | Closing beat | audio | animation | stretch |
|---|---|---|---|---|
| 01 Whole Numbers | scene10 | 25.74 s | 26.04 s | +0.30 s |
| 02 Operations on Whole Numbers | scene10 | 20.73 s | 21.03 s | +0.30 s |
| 03 Commutative & Associative | scene10 | 25.71 s | 26.01 s | +0.30 s |
| 04 Distributive Property & Identities | scene10 | 20.68 s | 21.00 s | +0.32 s |
| 05 Geometric Dot Patterns | scene10 | 22.59 s | 22.88 s | +0.30 s |

No beat under-runs either: a window that ends early would push the next scene's
audio on top of the previous one, so every window is now consumed to its own
mark (this is what the phrase-level pass was for). The `TOTAL` row printed by the
audit sums the beats and is not a beat of its own.

## 3. Layout sweep (0 flags)

| Video | Collision / bounds flags | `OFF-CENTRE` (intended) |
|---|---|---|
| 01 Whole Numbers | 0 | 113 |
| 02 Operations on Whole Numbers | 0 | 23 |
| 03 Commutative & Associative | 0 | 89 |
| 04 Distributive Property & Identities | 0 | 63 |
| 05 Geometric Dot Patterns | 0 | 101 |

Zero `TEXT-IN-TEXT`, `PARTIAL`, `TEXT-ON-ARROW`, `NEAR-BADGE`, `OUT-OF-BOARD`,
`OUT-OF-BOARD-LOW`, `LATEX-AS-TEXT`, `EMPTY-TEXT` and `TEXT-OUTSIDE-BOX` flags
across the whole chapter. (The three `TEXT-OUTSIDE-BOX` reports that used to
appear in the Distributive video are gone: the highlight box in scene 3 now wraps
the multiplier `4` it is describing instead of the bracket `(2+3)`.)

The `OFF-CENTRE` reports are the deliberate layouts where a group is demonstrated
rather than centred — number lines, dot patterns, row labels sitting beside their
own row, and side-by-side card rows. None is a collision; the audit flags them
only because they are not centred on the board axis.

## 4. What was fixed in this pass

- **05 Geometric Dot Patterns** — the `3+3=6` sum in scene 3 started a sentence
  early and pushed the `2×3=6` rule and its tag a beat late; twelve further
  windows were under-consumed by their trailing fractions so their visuals
  appeared during the previous sentence. Scene 10's recap (takeaway + three rows)
  used to appear one bookmark early and vanish exactly as its own words were
  spoken; the takeaway also collided with the first recap row and the rows ran
  below the bottom of the board (takeaway moved to −1.25, rows to −2.20); and the
  scene-9 question text ran 0.2 board units past the left edge.
  A final layout pass on this video then fixed, by eye: the scene-1 line is
  centred on the board like the shapes it is compared with, the count `6` sits
  level with the shape area instead of at the right edge, the scene-1 question
  fades out before the two equations are written (the cross-fade had left them on
  top of each other), the `25` on each sticker packet clears the sticker circle,
  and the four recap shapes share a baseline with their labels on one line. Its
  closing narration also now speaks "See you in the next lesson!", so the video
  is 266.4 s with 81 caption cues (682 words).
- **04 Distributive Property & Identities** — scene 8 ran a whole narration
  window early in four places (the earnings equation, the "common multiplier 30"
  tag, `100×30` and the `Rs 3000` answer); the scene-9 reveal chain was one window
  early; the scene-3 highlight box marked the bracket instead of the multiplier
  `4`; and eight further windows were under-consumed.
- **03 Commutative & Associative** — the ASSOCIATIVE card and the closing "Both
  work for addition and multiplication…" banner each appeared a whole sentence
  early; seven windows were under-consumed (title pulse, scene 1's `196+4=200`,
  scene 3's grid, scene 6's capsules, the scene-9 bracket, the scene-10 cards and
  the board clear).
- **02 Operations on Whole Numbers** — every number line is now centred on the
  board (`num_line()` laid out from a fixed left-hand `x0`, leaving lines up to
  0.56 units off centre); the "ADDITION → MOVE RIGHT" note no longer collides with
  the boxed answer; ten phrase-level placements were wrong, including all four
  recap rows playing a sentence early and scene 8 never highlighting its RESULT
  card.
- **01 Whole Numbers** — the pencil box: the visible pencils are centred in the
  tray and stay centred as they are removed or added, and the "remove the last
  pencil" step now fades the pencil instead of the tray (it used to leave a pencil
  drawn while the counter read `0`); twelve phrase-level placements were wrong,
  including the title's zero highlight which ran 1.9 s early.

## 5. Verification gap worth knowing about

The per-beat audit compares **total** animation time with **total** audio time,
so a beat can be perfectly "in sync" while its animations are attached to the
wrong line. That is why every video was additionally checked window by window
against the real word boundaries with `bookmark_times.py`, which can be pointed
at any topic:

```powershell
.venv/Scripts/python.exe ..\..\bookmark_times.py dot_patterns_story scene4 scene10
```

The tool retimes each piece from the cached WAV exactly as the render does (the
cache's own times are the TTS *service* times and drift from what the video
plays), and prints each bookmark's time next to the words spoken inside that
window. All 60 narration windows across the chapter are now pinned to their own
marks.

## 6. Delivered artefacts

| Video | 1080p60 master (delivered) | 360p30 review copy |
|---|---|---|
| 01 Whole Numbers | `whole_numbers_story/1080p60/WholeNumbersStory_captioned.mp4` | same folder tree, `360p30/` |
| 02 Operations | `operations_on_whole_numbers/1080p60/OperationsOnWholeNumbersStory_captioned.mp4` | `360p30/` |
| 03 Commutative & Associative | `commutative_associative_story/1080p60/CommutativeAssociativeStory_captioned.mp4` | `360p30/` |
| 04 Distributive | `distributive_property_story/1080p60/DistributivePropertyStory_captioned.mp4` | `360p30/` |
| 05 Geometric Dot Patterns | `dot_patterns_story/1080p60/DotPatternsStory_captioned.mp4` | `360p30/` |

Each topic folder also holds its `storyboard.md` (with the measured timings and
the production-check section), its `audit_sync_overlap.py` and `sync_map.py`, and
proof frames of the areas that were corrected.

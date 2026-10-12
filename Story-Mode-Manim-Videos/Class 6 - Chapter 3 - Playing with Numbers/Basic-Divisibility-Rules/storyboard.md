# Production-Ready Storyboard

## Mastering Basic Divisibility Rules: Quick Tests for 2, 3, 5, 6, 9, and 10

CLASS 6 MATHEMATICS · CHAPTER 3 · STORYMODE 01

**LLM KEY / FUNCTION NAME:** `divisibility_rules_basic_2_3_5_6_9_10`
**DIRECT TOPIC:** Basic Divisibility Rules for 2, 3, 5, 6, 9, and 10
**CHAPTER:** Chapter 3 — Playing with Numbers
**TARGET CLASS LEVEL:** Class 6
**TEXTBOOK:** Telangana SCERT, Class 6 Mathematics (English Medium), 2025–26,
Chapter 3 — Playing with Numbers; the chapter opens with Hasini's 125 chocolates
to be shared among 25 students, defines a divisibility rule as a way of checking
divisibility **without actual division**, and reviews the rules for
2, 3, 6, 9, 5 and 10 (Exercise 3.1, Question 5).

---

## Learning Objective

By the end of this video, students should be able to:

- Understand what "divisible" means (remainder zero).
- Check divisibility without performing long division.
- Apply the divisibility tests for 2, 3, 5, 6, 9 and 10.
- Recognise that some rules examine only the **ones digit** (2, 5, 10).
- Recognise that some rules use the **sum of all digits** (3, 9).
- Understand that divisibility by 6 requires **two tests together**.
- Apply several divisibility tests to the same number.

**Primary takeaway:** *Don't divide the whole number — inspect the right clue.*

## Core Visual Metaphor — "The Divisibility Scanner"

Six rules collapse into three ways of looking at a number, and that grouping is
the signature visual of the video:

    boxed{2, 5, 10}  ->  LOOK AT THE LAST DIGIT
    boxed{3, 9}      ->  ADD ALL THE DIGITS
    boxed{6}         ->  PASS TWO TESTS (2 AND 3)

## Core Divisibility Rules

| Divisor | Quick Test |
|---|---|
| 2 | Ones digit is 0, 2, 4, 6 or 8 |
| 3 | Sum of digits is divisible by 3 |
| 5 | Ones digit is 0 or 5 |
| 6 | Number is divisible by both 2 and 3 |
| 9 | Sum of digits is divisible by 9 |
| 10 | Ones digit is 0 |

## Scene Plan

| Scene | Learning goal | Visual | Key on-screen text | Maths |
|---|---|---|---|---|
| 1 | Motivate divisibility | Hasini's 125 chocolates, attempts leaving remainders | Can we tell without dividing? | 125 ÷ 5, ÷ 6, ÷ 4 |
| 2 | Define divisibility | Two columns of share-boxes | Remainder 0 → exactly divisible | 24 ÷ 4, 29 ÷ 4 |
| 3 | Rule for 2 | Four numbers, last digit ringed | Divisible by 2 → ones digit 0,2,4,6,8 | 953, 9534, 900, 452 |
| 4 | Rules for 5 and 10 | Two examples, three rule cards | LAST-DIGIT RULES | 5785, 1250 |
| 5 | Rule for 3 | 27 vs 37, then a digit sum | 3+6+1+2+9 = 21 | 36129 |
| 6 | Rule for 9 | Same digit sum, stronger test | 3 and 9 → ADD THE DIGITS | 9846 → 27 = 9×3 |
| 7 | Rule for 6 | Two gates merging into one badge | Divisible by 6 = BOTH 2 and 3 | 7224 |
| 8 | Compare all rules | Three zone panels | LOOK → ADD → COMBINE | summary |
| 9 | Student challenge | Six divisor buttons, THINK clock | YOUR TURN | 12345 against 2,3,5,6,9,10 |
| 10 | Final recap | Three families, quick examples | LOOK. ADD. COMBINE. | 452, 5785, 9846, 7224 |

## Key Pedagogical Safeguards

1. **Divisibility means zero remainder.** Scene 2 establishes remainder 0 versus
   remainder 1 before any shortcut appears.
2. **For 2, 5 and 10 only the ones digit is used** — the other digits are simply
   not examined, and the video says so.
3. **The last digit is not used for 3 or 9.** Scene 5 deliberately contrasts 27
   and 37: same last digit, different answer.
4. **Divisibility by 6 needs both conditions.** Scene 7 shows two independent
   gates and stresses the word *both*; one test alone is never enough.
5. **3 and 9 differ only in the question asked of the digit sum** — scene 6
   states this explicitly.
6. **Four, eight and eleven are deliberately left out**; the textbook develops
   those later.

---

# Final Production Check

**Module:** `divisibility_rules_basic_2_3_5_6_9_10.py`
(`DivisibilityRulesBasicStory`), assembled by `assemble_divisibility.py` from the
series' proven video-03 head (theme, chalkboard backdrop with the student, the
teacher and both corner badges, `reset_board`, `appear`, the card helpers, the
ground-truth SRT export) plus this topic's fragment (`_divisibility_fragment.py`:
board layout, number cards, digit tiles, chocolate groups, verdict marks, zone
panels, gates, narration) and beats (`_divisibility_beats.py`).

**Delivered files** (the same performance, cut at two resolutions):

The 360p cut:

    final_videos/DivisibilityRulesBasicStory_captioned.mp4
    640×360, 30 fps, 192.37 s (3 min 12 s), 9.2 MB, 50 captions
    final_videos/DivisibilityRulesBasicStory_captioned.srt

The 1080p60 master, re-rendered from the same module (no re-timing, so the
audio, the reveal timing and the SRT are the same performance):

    final_videos/1080p/DivisibilityRulesBasicStory_captioned.mp4
    1920×1080, 60 fps, 192.28 s, 11 537 frames, 37.1 MB, 50 captions
    final_videos/1080p/DivisibilityRulesBasicStory_captioned.srt

    verify_sync.py      video 192.283 s, 50 captions, first 0.14 s, last
                        190.27 s, 0 in silence, 0 uncaptioned  -> PASS
    verify_captions.py  narration 435 words = SRT 435 words       -> PASS

`pipeline_1080.py` in this chapter folder produced the master
(render 1920×1080/60 → verify → burn → `final_videos/1080p/`). libass scales the
one caption style with the video height, so the 1080p burn is the 360p burn
three times the size.

The raw renders and their ground-truth SRTs also sit in
`media/videos/divisibility_rules_basic_2_3_5_6_9_10/360p30/` and `…/1080p60/`.

**Voice sync** (`audit_sync_overlap.py`): **every one of the 11 narration
pieces matches its audio to 0.00 s** — no stretch anywhere; the closing card's
2 s hold is the only deliberate extra. Total audio 242.5 s.

**Real captions** (`verify_sync.py`): 73 captions, first at 0.52 s, last at
253.40 s of a 255.40 s video, **0 captions in silence**, **0 speech blocks
uncaptioned** → **PASS**. `verify_captions.py`: narration 632 words = SRT 632
words → **PASS (word for word)**.

**Layout audits** (both run twice: on a synthetic draft SRT before the render,
then again against the real one):

- `audit_sync_overlap.py` → **0** out-of-board, text-in-text, text-on-line,
  text-outside-box, near-badge, LaTeX-as-text or empty-TeX flags.
- `audit_clearance.py` → **0** text/line collisions and **0** foreign-box
  collisions; the 10 pairs still under 0.22 units are the designed two-line
  stacks inside one card (0.14–0.18 apart).

The draft pass earned its keep: it caught the "125 chocolates" card touching
the first attempt row, the four recap rows reaching into the corner-badge strip,
and both scene-7 ticks sitting outside their gate groups. All three were fixed
before a render was spent.

**Timer:** the THINK clock is centred on the board
(`story_common.play_challenge_countdown`, `position=(BOARD_CX, BOARD_CY)`), the
series default, for the four-second pause in scene 9.

**TTS pre-check** (`tts_precheck.py`): all eleven pieces generated audio with
word boundaries before the render (54–70 boundaries each).

**Frame sweep:** title, all ten scenes, the centred countdown and the closing
card inspected as stills in `frames360/01_title.png` … `11_scene10.png`, plus
`10b_countdown.png` for the clock.

**Tools in this folder:** `assemble_divisibility.py`, `setup_tools.py` (builds
the audits from the quadrilaterals set), `make_draft_srt.py`,
`tts_precheck.py`, `audit_sync_overlap.py`, `audit_clearance.py`,
`scene_frames.py`, `find_timer.py`, and the chapter's `pipeline_360.py`
(render → verify → burn → `final_videos/`) and `pipeline_1080.py`
(render → verify → burn → `final_videos/1080p/`).

---

# Revision — production audit fixes

Every point of the production audit was fixed and re-verified. The delivered
file was re-rendered from scratch (360p30, captions burned in).

## Runtime: 04:14 -> 03:12 (speech 02:59, inside the 2:30-3:00 target)

| Piece | before | after |
|---|---:|---:|
| title | 19 s | 9 s |
| scene 1 hook + chocolates | 20 s | 16 s |
| scene 2 meaning | 18 s | 13 s |
| scene 3 rule for 2 | 28 s | 18 s |
| scene 4 rules for 5 and 10 | 23 s | 19 s |
| scene 5 rule for 3 | 21 s | 19 s |
| scene 6 rule for 9 | 20 s | 16 s |
| scene 7 rule for 6 | 23 s | 17 s |
| **scene 8 real-world application (new)** | -- | 15 s |
| scene 9 student challenge | 23 s | 21 s |
| scene 10 recap (absorbed the old dashboard) | 26 s | 20 s |

The separate "Don't Memorise Six Separate Tricks" dashboard was merged into the
final recap, exactly as the audit asked, so the video has one summary segment
instead of two. The remaining 13 seconds beyond the speech are the designed
pauses: the centred 4.8 s THINK clock, eleven scene transitions and the closing
hold.

## Pedagogical structure

- **Stage 1 (hook) added** in scene 1: *"Traders shared grain this way for
  centuries."* — on the board as a cyan line under the 125-chocolate card, so
  the textbook situation is tied to why the idea exists at all.
- **Stage 5 (real-world application) added as its own scene 8**: *372 runners
  into equal relay teams of six*. The two gates (ends in 2 -> passes 2;
  3+7+2 = 12 -> passes 3) merge into the 6 badge and the answer *"62 teams,
  nobody out"*, with the closing line *"6 x 62 = 372, and no long division."*

## Mathematical / audio-visual alignment

- **`1250` now shows both checks** the narration speaks: `ones digit 0 -> /5`
  and `ones digit 0 -> /10`, beside `5785 -> ones digit 5 -> /5`.
- **Rule pill made symmetric**: `10 -> must be 0` became `10 -> 0`, matching
  `2 -> 0, 2, 4, 6, 8` and `5 -> 0 or 5`.

## Layout: subtitle collision and mobile readability

- **Caption safe zone enforced.** The burned-in caption grows upward from the
  bottom of the frame -- a one-line cue starts at y = -3.33 and a **two-line cue
  reaches y = -2.33**, which is what covered the closing strips. Every bottom
  strip moved from y = -2.58 to **y = -1.95**, and nothing in the video now sits
  below **y = -2.15**.
- **A new audit check locks it in.** `audit_sync_overlap.py` gained
  `IN-CAPTION-BAND`: any board content below `CAPTION_SAFE_Y = -2.15` is
  reported. All eleven scenes report zero.
- **Bigger type where it was dense.** The challenge solution dropped its two
  cramped paragraphs for two large lines (`1+2+3+4+5 = 15 -> divisible by 3`,
  `ends in 5 -> divisible by 5`, 22 pt) with the tick/cross marks on the divisor
  boxes carrying the failures; the recap rows went from 15 to 19 pt and
  "LOOK. ADD. COMBINE." from 22 to 24 pt; scene 3 shows **two** large number
  tiles instead of four small ones, and scene 1 **two** attempts instead of
  three.

## Verification of the delivered file

    final_videos/DivisibilityRulesBasicStory_captioned.mp4
    640x360, 30 fps, 192.4 s (3 min 12 s), 8.6 MB
    final_videos/DivisibilityRulesBasicStory_captioned.srt

- **Voice sync** (`audit_sync_overlap.py`): every one of the 11 pieces matches
  its audio to **0.00 s**; total speech 178.7 s.
- **Captions** (`verify_sync.py`): 50 captions, first 0.14 s, last 190.22 s of a
  192.40 s video, **0 captions in silence**, **0 speech blocks uncaptioned** ->
  **PASS**. `verify_captions.py`: 435 = 435 words -> **PASS (word for word)**.
- **Layout** (`audit_sync_overlap.py` + `audit_clearance.py`): **0**
  out-of-board, text-in-text, text-on-line, text-outside-box, near-badge,
  LaTeX-as-text, empty-TeX, **IN-CAPTION-BAND**, text/line-collision or
  foreign-box flags; the 4 pairs under 0.22 units are the designed two-line
  stacks inside single cards.
- The pipeline that produced it (`pipeline_360.py`) now also deletes any
  previous cut's caption file before copying the new one, so a stale `.srt` can
  never sit beside a fresh movie again -- that bug briefly mis-reported the
  first re-cut.

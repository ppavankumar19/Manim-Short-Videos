# Implementation Notes — "The Tale of Two Coin Piles"
### Simple Interest vs Compound Interest (Telangana Class 8 story-mode video)

This document records the actual process followed to go from a plain-language
request to the finished, captioned, voice-synced Manim video. It's written as
a reusable playbook for the next story-mode video in this series.

---

## 1. Starting point — what already existed

This project reuses a shared pipeline built for earlier lessons in the repo,
so nothing here started from zero:

- **`manim` (Community Edition)** for all animation/rendering.
- **`manim_voiceover`**'s `VoiceoverScene`, paired with a custom
  `EdgeSpeechService` (in `speech_service.py` / `edge_speech_service.py` at
  the repo root) that calls Microsoft Edge's neural TTS
  (`en-IN-PrabhatNeural`, Indian-accented English) instead of a paid API.
- A **chalkboard visual style**: `background2.png` + hand-drawn "chalk vector"
  icons (chests, jars, clocks, coins) built from Manim primitives
  (`RoundedRectangle`, `Sector`, `Arc`) with gradient fills and a
  `drop_shadow()` helper for pseudo-3D depth.
- A **sound-effects module** (`sound_effects.py`) for click/ding/swipe/success
  stings layered under the animation.

## 2. Turning the request into a script

The user describes the lesson in plain language (topic, characters, the
concr�ete numbers to use, what misconception to correct). That gets turned
into:

1. **Module-level constants** (`PRINCIPAL`, `RATE`) and pure functions
   (`si_amount()`, `ci_amount()`, `jar_amount()`, `fmt_money()`, `fmt_int()`)
   so every on-screen number and every spoken number is *computed*, never
   hard-coded twice. Changing `PRINCIPAL`/`RATE` once (e.g. 100→500,
   10%→20%) automatically ripples through every diagram, label, and
   sentence of narration — the numbers used in the story come directly
   from the request.
2. A **narration dictionary** (`NARRATION = {...}`), one string per "beat"
   of the story (title, scene1, scene2 …). Each string is the literal text
   handed to the TTS engine, written the way a teacher would actually speak
   it — short sentences, natural pauses, explicit numbers.
3. **`<bookmark mark='xyz'/>` tags** inserted directly into the narration
   text at the exact words an animation must land on (e.g. right after "20
   percent annual interest" is spoken). These tags are stripped before the
   text is sent to the TTS engine, but their position in the string is used
   afterwards to know *when* that point in the audio occurs.

## 3. Building the scene

For each beat, a `beat_xxx()` method does three things together inside a
`with self.voiceover(text=NARRATION["xxx"]) as tracker:` block:

- Builds/animates the Manim mobjects for that beat (chests, coins, graphs,
  formulas…).
- Times every `self.play(..., run_time=...)` off the **real audio**, using
  `tracker.time_until_bookmark("xyz")` or `tracker.get_remaining_duration()`
  — never a guessed constant — so the animation always lands exactly where
  the matching word is spoken, regardless of how TTS happens to pace that
  sentence.
- Fires a matching sound effect (`self.add_sound(self.sfx["ding"], ...)`) at
  the same beat.

Two extra pieces of care that came up repeatedly in this project:

- **Reusing a bookmark for two sequential `self.play()` calls breaks the
  second one** — `time_until_bookmark()` returns the time *remaining* from
  "now", so once the first animation consumes it, the second call to the
  same bookmark returns ~0 and snaps in instantly. Fix: give every
  animation step its own bookmark, or split one bookmark's budget with a
  fraction (`* 0.4`) for the first step and let the second step use the
  (now correctly reduced) remainder.
- **Fixed durations near the end of a beat** — once nearly all of a beat's
  bookmarked narration has already played, `get_remaining_duration()` is
  tiny, so anything timed off it (like two sequential graphs revealing one
  after another) can end up looking simultaneous even though the code is
  structured correctly. For "just let the viewer see this" moments after
  the narration's content is essentially done, plain fixed `run_time=`
  values work better than fractions of a shrinking budget.

## 4. Getting a *real* subtitle file (not an approximation)

`manim_voiceover`'s built-in subcaption feature estimates caption timing by
character count, which drifts from the actual audio. Instead, this project:

- Sets `create_subcaption=False`.
- Reads `tracker.data["word_boundaries"]` (edge-tts's actual per-word audio
  timestamps) plus `AUDIO_OFFSET_RESOLUTION` from `manim_voiceover.tracker`.
- Custom methods `_capture_srt()` / `_write_real_srt()` turn those word
  boundaries into a proper `.srt` file — `InterestGrowthStory.real.srt` —
  with correct start/end times for every line, called once per beat so the
  offsets stay in sync with which beat is currently playing.

This real SRT is the source of truth used both for burning captions into the
preview *and* for verifying sync (see step 6).

## 5. The render/iterate loop

Every change — even a small layout nudge — goes through the same low-cost
loop before being considered "done":

1. If any **bookmark text changed** (new tag, moved tag) but the underlying
   spoken words didn't change, the voice cache is stale — clear it:
   `rm -rf media/voiceovers`. (The cache key is spoken text + voice params,
   with bookmarks stripped, so an unchanged sentence with a newly-added
   bookmark silently reuses old cached audio that doesn't know the new
   bookmark exists, and raises `Exception: There is no <bookmark .../>`.)
2. Render fast, not final:
   ```
   manim --resolution 640,360 --fps 30 --disable_caching \
         interest_growth_story.py InterestGrowthStory
   ```
   (360p/30fps renders in a couple of minutes instead of 15–20.)
3. Copy the freshly-written real SRT next to the render:
   ```
   cp InterestGrowthStory.real.srt media/videos/interest_growth_story/360p30/real.srt
   ```
4. Burn it into a captioned preview with ffmpeg, using a fixed style that's
   been tuned once and reused everywhere (font size/margins are
   resolution-independent under libass, so this string is never rescaled
   for higher-res renders):
   ```
   ffmpeg -y -i InterestGrowthStory.mp4 -vf "subtitles=real.srt:force_style='FontSize=9.5,Bold=1,PrimaryColour=&HFFFFFF&,OutlineColour=&H80000000&,BackColour=&H80000000&,BorderStyle=3,Outline=1.6,Shadow=0,MarginV=10,MarginL=43,MarginR=10'" InterestGrowthStory_captioned.mp4
   ```

## 6. Verifying sync — never trust a claim, check the frame

This was the standard applied to every fix in this project, per the rule
"once check the srt timestamp and video based synching":

1. `grep` the real SRT for the phrase in question, to get its exact
   start/end timestamp.
2. Extract a single frame at that timestamp (and a few nearby, to see
   before/during/after):
   ```
   ffmpeg -y -ss <t> -i InterestGrowthStory_captioned.mp4 -frames:v 1 out.png
   ```
3. Visually inspect the extracted frame — does the caption on screen match
   what's drawn (correct number, correct sign, graph fully drawn vs. still
   animating, etc.)?
4. Only after seeing this evidence is a fix reported back as done.

This is how, for example, the "rate of interest sign appears late" bug and
the "graphs look simultaneous" bug were actually found and confirmed fixed
— both were invisible from reading the code alone.

## 7. Feedback → fix cycle

Every round followed the same shape:

1. User watches the captioned low-res preview and reports what's visually
   or pedagogically wrong ("main chest should stay 500", "graphs feel
   simultaneous", "years label overlaps").
2. Root cause is found in the beat method responsible (a bookmark
   pointing at the wrong sentence, a mobject not being frozen when it
   should be, a fixed offset colliding with a board edge, etc.).
3. Minimal, targeted fix — no unrelated refactors.
4. Re-run the full loop in steps 5–6 above, only then reply with confirmed
   evidence (specific timestamp/frame) or a screenshot description.

## 8. Final high-resolution render

Only after the low-res preview is fully approved:

```
manim -qh --resolution 1920,1080 --fps 60 --disable_caching \
      interest_growth_story.py InterestGrowthStory
```

(`-qh` = Manim's "high quality" preset, 1080p/60fps — deliberately *not*
`-qk`, which targets 4K.) Then the same caption burn-in step is repeated
against the 1080p60 output to produce the final deliverable:

```
cp .../InterestGrowthStory.real.srt .../1080p60/real.srt
ffmpeg -y -i InterestGrowthStory.mp4 -vf "subtitles=real.srt:force_style='...'" InterestGrowthStory_captioned.mp4
```

Final output: `media/videos/interest_growth_story/1080p60/InterestGrowthStory_captioned.mp4`.

---

## Summary of the pipeline, end to end

```
Plain-language request
   → narration text + bookmarks + dynamic constants (in the .py script)
   → Manim VoiceoverScene render (edge-tts synthesizes real audio per beat)
   → real per-word SRT captured from edge-tts word boundaries
   → low-res (360p/30fps) render + SRT burned in via ffmpeg
   → frame-level visual verification against SRT timestamps
   → user feedback → targeted fix → repeat verification loop
   → final 1080p/60fps render + captions burned in
```

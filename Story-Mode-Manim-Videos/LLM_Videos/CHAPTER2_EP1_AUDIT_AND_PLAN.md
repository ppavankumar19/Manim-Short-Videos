# Chapter 2 · Episode 1 — "The Secret Language of LLMs"
## Production Audit + Implementation Plan (pre-build)

**Target folder:** `Story-Mode-Manim-Videos/LLM_Videos/`
**Backdrop asset:** `LLM_Videos/assets/background.png` (1672×941, neon-blue tech panel — already present)
**Sources audited:** `Hands-On Large Language Models.pdf` (Alammar & Grootendorst, O'Reilly 2024),
Chapter 2, book pp. 37–57 (= PDF pp. 39–59); `Hands_On_LLMs_Book_Storyboard_Master_Prompt.txt`;
the supplied Chapter 2 Episode 1 storyboard.
**Status of the shared ChatGPT link:** `https://chatgpt.com/share/6ac87a6b-…` is a JS-rendered
share page. It returns HTTP 200 but **no recoverable text** for a fetcher. The storyboard pasted
in the request is therefore treated as the authoritative brief.

A verbatim extract of the book's Chapter 2 tokenization half is kept next to this file as
`CHAPTER2_BOOK_TEXT_EXTRACT.txt` so every on-screen value can be re-verified without reopening the PDF.

---

# PART A — AUDIT

## A1. Environment capability audit

| Item | Finding | Verdict |
| --- | --- | --- |
| Manim | **CE 0.21.0** in `D:\Manim-Short-Videos\.venv` | ✅ |
| `manim_voiceover` | 0.4.0 | ✅ |
| TTS | `edge-tts` 7.2.8 + `edge_speech_service.EdgeSpeechService` (repo root) | ✅ |
| ffmpeg | 8.0.1-full_build on PATH (caption burn-in + concat) | ✅ |
| Fonts | Calibri, Cambria, Consolas, Segoe UI, Segoe Print present | ✅ |
| `tokenizers` 0.23.2 | Installed | ⚠️ see A6 |
| SoX | **Not installed** | ⚠️ Manim warning only; harmless here |
| `ThreeDScene` + `VoiceoverScene` | **Smoke-tested in this session** → MRO resolves, `camera = ThreeDCamera`, `set_speech_service` present | ✅ **3D + narration is viable** |
| Background asset | `LLM_Videos/assets/background.png` is 16:9 (1.777 vs frame 1.778) | ✅ scales to frame cleanly |
| `background.png` free space | The bright glass panel occupies roughly x∈[-12%…+12%] of centre → generous native safe area | ✅ |

**Consequence:** the "high-level 3D diagrams" requirement is not a risk. `class LLMScene(ThreeDScene, VoiceoverScene)`
is the base class for this episode.

## A2. Pipeline audit (repo convention)

The repo already has a proven, documented playbook — `Story-Mode-Manim-Videos/process.md` and
`Simple-vs-Compound-Interest/implementation.md`. Audit finding: **this episode should reuse it
rather than invent anything.**

| Established stage | Reuse decision |
| --- | --- |
| Constants + pure functions so numbers are computed, never hard-coded twice | ✅ keep |
| `NARRATION = {beat: text}` with `<bookmark mark='x'/>` tags at animation landings | ✅ keep |
| `with self.voiceover(text=...) as tracker:` + `tracker.time_until_bookmark()` | ✅ keep |
| Real per-word SRT from `tracker.data["word_boundaries"]` (not char-count estimates) | ✅ keep |
| Low-res 360p/30 preview → frame-level SRT verification → final 1080p60 | ✅ keep |
| `rm -rf media/voiceovers` whenever bookmark text (not spoken text) changes | ✅ keep — bookmark trap applies here |
| Chalkboard + `story_common.play_challenge_countdown` timer | ❌ **not reused.** Wrong visual language (this is a neon tech series, not Class 8 maths), and the storyboard's Scene 14 uses a 5s *predict* pause, not the 10s THINK clock |
| `background2.png` chalkboard | ❌ replaced by the supplied neon `background.png` |

**Audit finding — new palette needed.** `lesson_kit.py` and `story_common.py` are written for a
dark-slate/chalk aesthetic (`BG #0F172A`, `SUCCESS #34D399`, Segoe Print). The supplied backdrop is
cyan→violet neon. Forcing the maths palette onto it will look wrong. A new `theme.py` is required,
sampled from the backdrop art.

## A3. Storyboard factual audit — every verifiable claim against the book

I checked each numeric/factual claim in the storyboard against the extracted book text.

### ✅ VERIFIED CORRECT

| Storyboard claim | Book evidence | Status |
| --- | --- | --- |
| Book page map: 38–42, 43, 44–45, 46–54, 55–56 | Section headings land exactly on those book pages | ✅ exact |
| `apologizing` → `apolog` (27746) + `izing` (5281) | p.40–41: tensor `[…, 27746, 5281, …]` ↔ decode list `<s>, Write, an, email, apolog, izing, to, …` — index 4/5 match | ✅ exact |
| `3323` = `Sub`, `622` = `ject`, joined = `Subject` | p.42: "token 3323, 'Sub', followed by token 622, 'ject'" | ✅ exact |
| GPT-2 `🎵` = IDs **8582, 236, 113**, `decode([8582,236,113])` → `🎵` | p.49 verbatim | ✅ exact |
| BERT uncased → lowercase, `capital` + `##ization` (2 pieces) | p.47–48 tokenized text + bullet | ✅ exact |
| GPT-2 → `CAP ITAL IZ ATION` (4 pieces) | p.49 | ✅ exact |
| FLAN-T5 → `CA PI TAL IZ ATION` (5 pieces) | p.50 | ✅ exact |
| GPT-4 → `CAPITAL IZATION` (2 pieces) | p.50, and p.51 "two tokens versus four" | ✅ exact |
| BERT uncased / FLAN-T5 turn `🎵鸟` into unknown markers | p.48 `[UNK] [UNK]`; p.50 `<unk> <unk>` | ✅ exact |
| `elif` is a single token in GPT-4 | p.51 | ✅ exact |
| Four spaces = one token in GPT-4 | p.51 (+ "every sequence of whitespaces up to … 83") | ✅ exact |
| `##` = WordPiece continuation marker | p.48 | ✅ exact |
| Three determiners: method, parameters, training data | p.43 + p.55 | ✅ exact |
| Subword ≈ 3 chars/token ⇒ ~3× text per 1,024 context | p.45 | ✅ exact |
| Word-level pain: `apology/apologize/apologetic/apologist` + unseen words | p.44 | ✅ exact |
| WordPiece = BERT, BPE = GPT, SentencePiece implements BPE/unigram (a *framework*, not an algorithm) | p.43, p.47, p.50 | ✅ exact — storyboard's distinction is correct and worth keeping |
| Years 2018 / 2019 / 2022 / 2023 | p.47, p.49, p.50, p.50 | ✅ exact |

### ⚠️ MUST-FIX (accuracy defects)

| # | Defect | Why it matters | Fix |
| --- | --- | --- | --- |
| **F1** | Scene 9 labels GPT-2 as **"Byte-level BPE"** | The book explicitly says GPT-2/RoBERTa *include bytes in the vocabulary as a fallback* and that **"this doesn't make them tokenization-free byte-level tokenizers."** The storyboard's own Scene 11 caption is right, but the Scene 9 machine label contradicts the book. | Relabel → **"BPE (byte fallback)"** |
| **F2** | Scene 12 uses invented code `def greet(name): / print(name)` | Book's recorded code example is **`def add_numbers(a, b): / ...."""Add the two numbers…""" / ....return a + b`** with the literal `....` rendering of the four indentation spaces. Using a different program silently swaps a book example for an invented one. | Use the book's `add_numbers` program verbatim |
| **F3** | Scenes 3, 4(counter) and 5 use `play/player/playing/playfulness` and `p-l-a-y` as if they were book examples | Book's word-level example is `apology/apologize/apologetic/apologist`; its subword payload is **`apolog` + suffix tokens `-y, -ize, -etic, -ist`**; its "play" reference is only the *character-vs-subword* illustration. | Keep the `play` family (good pedagogy) but stamp it **"Illustrative example (created for explanation)"**, and **add** the book's `apolog` family as the second, book-grounded pass in Scene 5 |
| **F4** | Scene 9 title "One Prompt, **Four** Tokenizers", 4 machines | The book compares **eight** trained tokenizers (BERT uncased, BERT cased, GPT-2, FLAN-T5, GPT-4, StarCoder2, Galactica, Phi-3). Showing four is a legitimate simplification but must not be presented as *the* book comparison. | Retitle → "Four of the Book's Tokenizers"; on-screen stamp **"subset of the book's comparison (pp. 46–54)"** |
| **F5** | Scene 11 implies the whole `🎵鸟` pair is reconstructed by GPT-2 with given IDs | The book gives IDs **only for `🎵`** (8582/236/113). It says 鸟 is also "represented by multiple tokens each" but publishes **no IDs**. Inventing them would violate the master prompt. | Animate `🎵` with the three real IDs; show 鸟 as byte-derived pieces **without invented IDs**, and say the ID values are not shown in the source |
| **F6** | Scene 11 says "BERT **and FLAN-T5** routes replace the two symbols" — but the machine row for FLAN-T5 is not visually distinguished as `<unk>` (it uses `[UNK]` too) | Book uses **different markers per tokenizer family**: `[UNK]` (BERT) vs `<unk>` (FLAN-T5). Flattening them loses a real distinction. | Render the two markers exactly as the book prints them |
| **F7** | Master-prompt rule: original fictional samples must be labelled. Only Scene 2 and Scene 13 carry caveats | Scenes 1, 3, 4, 5, 6, 12 each contain invented values (`What is the capital of India?`, `playfulness`, `p-l-a-y-f-u-l`, dial positions, `add_numbers` if kept). | Add a persistent, low-key corner chip: **`illustrative`** / **`book-recorded`** on every scene — this is also excellent pedagogy |

### 🔍 GAP AUDIT — book material the storyboard omits (recommended additions)

These are all *book-recorded*, high-value, and cheap to animate. Ranked by value/cost:

| # | Gap | Book anchor | Where it fits | Recommendation |
| --- | --- | --- | --- | --- |
| **G1** | **BERT *cased* → `CAPITALIZATION` = 8 tokens** (`CA ##PI ##TA ##L ##I ##Z ##AT ##ION`) | p.48 | Scene 10 row 2 | **ADD.** This is the single sharpest "same word, wildly different split" datapoint in the whole book, and it costs one extra row |
| **G2** | **Vocabulary sizes are all published**: BERT 30,522 · BERT-cased 28,996 · GPT-2 50,257 · FLAN-T5 32,100 · GPT-4 "a little over 100,000" · StarCoder2 49,152 · Galactica 50,000 · Phi-3 32,000 | pp.47–54 | Scene 06 | **ADD a real comparative bar chart.** Scene 06 currently animates a vague "vocabulary capacity" control; real numbers are strictly better and directly book-sourced |
| **G3** | **BERT uncased destroys newline breaks** — "makes the model blind to information encoded in newlines (e.g., a chat log)" | p.48 | Scene 10 or 12 | **ADD as a one-line consequence card.** Concrete, memorable, and it motivates the code scene |
| **G4** | **StarCoder2 (2024)**: one token per digit (`600` → `6 0 0`), whitespace runs as single tokens, `<filename>/<reponame>/<gh_stars>` | p.52 | Scene 12 | **ADD.** Scene 12 is the code scene and currently has no code-specialist tokenizer in it — a real hole in the "domain of training data" argument |
| **G5** | **Special-token inventories**: `[UNK] [SEP] [PAD] [CLS] [MASK]` / `<|endoftext|>` / `<unk> <pad>` / GPT-4 FIM trio / Phi-3 chat trio `<|user|> <|assistant|> <|system|>` | pp.47–54, 55 | Scene 06 | **ADD a compact "special-token shelf" beat.** Scene 06 says the words "special tokens" but never shows one |
| **G6** | **"A pretrained language model is linked with its tokenizer and can't use a different tokenizer without training."** | p.57 | Scene 15 | **ADD as the closing line.** It is the *reason the entire 18 minutes matters* — currently Scene 15 ends on a weaker note |
| **G7** | **Figures 2-1 and 2-2** are never cited (storyboard cites 2-3…2-6) | pp.37–38 | Scenes 01–02 | Minor: cite 2-1/2-2 in Scene 01/02 source strip |
| **G8** | Phi-3 = Llama-2 tokenizer + added chat tokens; vocab 32,000 | p.53 | Scene 07 | Minor: one caption line adds real context to the `apolog` example |

### ❌ NOT DEFECTS (things that look wrong but are correct)

- Scene 1's "machine rejects text" is a sanctioned metaphor — the storyboard already labels it.
- Scene 2's `[42, 91]` toy IDs — correctly labelled as invented, and they deliberately do not
  collide with any book ID.
- Scene 13's "12 slots / 11 vs 6" — correctly labelled as invented. Must stay labelled.
- The storyboard's claim that WordPiece/BPE are *algorithms* while SentencePiece is a *framework
  implementing* BPE/unigram is **exactly right** (p.50) and should survive to the final script.

### Timing audit

Every scene boundary is continuous with no gaps and the 15 scenes sum to exactly **18:00**. ✅
Two scenes are heavy: Scene 10 (90 s, 4–5 segmentation rows) and Scene 12 (90 s, book code +
whitespace + StarCoder2 + GPT-4). If G1/G2/G4 are accepted the runtime grows by roughly **+90 s**;
the honest options are (a) accept **≈19:30**, or (b) trim Scene 04 and Scene 13 by ~45 s each.
**Do not** compress by shrinking type — the master prompt forbids it. The plan below assumes
**(a) accept the growth**.

## A4. Risk audit

| Risk | Severity | Mitigation |
| --- | --- | --- |
| 18–20 min @ 1080p60 ≈ 65k–70k frames | **High** — likely 4–10 h of render | Render **per act** (4 independent renders) → review between acts; concat at the end. Fall back to 1080p30 if the schedule binds |
| Bookmark reuse silently breaks the 2nd animation (`time_until_bookmark` returns *remaining* time) | Medium | One bookmark per animation step; the repo already documents this trap |
| Voice-cache staleness when a bookmark moves but words don't change | Medium | Clear `media/voiceovers/` on every bookmark edit |
| Dense token rows become illegible | Medium | The storyboard's own rule: never show dozens of tiny blocks — zoom into one phrase |
| Byte-derived tokens cannot render as glyphs (`\ufffd` in the book) | High for Scene 11 | Use the book's own approach: show the raw byte value as a **hex/ID chip**, then animate the **joined decode** producing the visible `🎵` |
| `media/` collisions across 4 act renders | Low | One output dir per act; ffmpeg concat |
| SoX missing | Low | Only affects Manim's audio-merge warning; narration is muxed by voiceover |

## A5. Deliverable audit — what "done" means

Per the master prompt, a *storyboard* is the deliverable and it explicitly forbids emitting code.
**This request supersedes that**: the user asked for the actual Manim scripts and a video. Audit
finding: the storyboard is complete and verified, so the master prompt's "storyboard phase"
requirement is satisfied and we may now move to implementation. Narration **must** now be written
(the storyboard deliberately deferred it).

## A6. Component audit vs. storyboard's required 9

| Required component | Plan |
| --- | --- |
| `TokenBlock` | ✅ shared, colour-by-token-index using the book's own 6-colour cycle (p.46) |
| `RawTextTrack` | ✅ |
| `VocabularyTable` | ✅ |
| `TokenizerMachine` | ✅ |
| `SegmentationAnimator` | ✅ |
| `UnknownTokenIndicator` | ✅ |
| `ByteSequenceView` | ✅ |
| `ContextSlotMeter` | ✅ |
| `EmbeddingMatrixPreview` | ✅ 3D slab — this is where the 3D requirement pays off |

---

## A7. Deep pipeline audit (requested: "go through the complete folder")

### A7.1 Render / caption / audio convention — verified empirically

The house convention is **360p30**, and captions + audio are always present. I traced it in
`Chapter 2 - Linear Equations in One Variable/pipeline_360.py` and confirmed it against a real
deliverable.

| Step | Exact house convention |
| --- | --- |
| Render | `python -m manim render --resolution 640,360 --fps 30 --media_dir D:\m3 <module.py> <Class>` |
| Why `D:\m3` | short media root, avoids Windows MAX_PATH on the long topic paths |
| Ground-truth SRT | `<Class>.real.srt` written by the scene's own `_write_real_srt()`, copied as `real.srt` |
| Gate 1 | `python verify_sync.py <Class>.mp4 <Class>.real.srt` |
| Gate 2 | `python verify_captions.py <module.py> <stem> NARRATION <Class>.real.srt` |
| Burn | `ffmpeg -y -i <Class>.mp4 -vf "subtitles=<Class>.real.srt:force_style='FontSize=9.5,Bold=1,PrimaryColour=&HFFFFFF&,OutlineColour=&H80000000&,BackColour=&H80000000&,BorderStyle=3,Outline=1.6,Shadow=0,MarginV=10,MarginL=43,MarginR=10'" -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -c:a copy <Class>_captioned.mp4` |
| Audio | preserved through the burn by `-c:a copy` — narration always ships with the captions |
| Outputs | `<topic>/media/videos/<stem>/360p30/` and `<topic>/final_videos/` |

Verified on the real deliverable
`Chapter 2 - Linear Equations in One Variable/final_videos/ParallelLinesAndAnglesStory_captioned.mp4`:
**640×360, 30/1 fps, h264 + AAC stereo, 312.77 s video / 310.63 s audio.** ✅

**Conclusion:** the request "360 with captions burned and audio" is already the house standard. This
episode will follow `pipeline_360.py` verbatim rather than inventing a new render path.

### A7.2 Voice — ⚠️ the codebase does NOT currently use edge-tts

Every story module calls `self.set_speech_service(get_speech_service(), create_subcaption=False)`.
`speech_service.py` resolves in this order: macOS `say` → **Gemini Zephyr** → **edge-tts** → gTTS.

The Gemini branch fires when `GOOGLE_API_KEY` is set **and** (`TTS_PROVIDER` is gemini/google **or**
`"zephyr"` appears in `GOOGLE_TTS_VOICE`/`VOICE`). This workspace's `.env` has:

```
GOOGLE_API_KEY=<set>
GOOGLE_TTS_VOICE=en-IN-Chirp3-HD-Zephyr
```

I executed the resolver to be certain. It returns:

```
RESOLVED SERVICE: GeminiZephyrSpeechService
  voice = 'Zephyr'   model = 'gemini-2.5-flash-preview-tts'
```

Voice-cache evidence (`media/voiceovers/cache.json` → `input_data.service` / `.voice`):

| Topic | Service actually used |
| --- | --- |
| `Transposition-Balancing-Scales` | `edge` / `en-IN-PrabhatNeural` |
| `Pythagorean-Theorem-ADEPT` | `gemini-zephyr` / `Zephyr` |
| `Simple-vs-Compound-Interest` | `gemini-zephyr` / `Zephyr` |
| All 8 `Chapter 2 - Linear Equations` topics (322 clips) | `gemini-zephyr` / `Zephyr` |

**So the repo migrated from edge-tts to Gemini `en-IN-Chirp3-HD-Zephyr`, and the newest videos — the
ones this episode should match — are Zephyr.** The module docstrings and
`Simple-vs-Compound-Interest/implementation.md` still say "EdgeSpeechService (en-IN-PrabhatNeural)";
that documentation is **stale**, though the code path they describe still works.

### A7.3 ⚠️ Zephyr's word boundaries are *estimated*, not measured — this is a real sync defect

This is the most consequential finding of the audit.

- **edge-tts** returns genuine per-word `audio_offset` values emitted by the TTS engine.
- **Gemini's response contains only PCM audio** — no timestamps. So
  `gemini_speech_service._calculate_word_boundaries()` **invents** them: it spreads the clip's total
  duration across words *in proportion to character count*, adding +4 weight for `. ! ?` and +2 for
  `, ; :`. It never looks at the audio it just wrote.

Everything downstream inherits that estimate: the `.real.srt`, and every
`self.play(..., run_time=tracker.time_until_bookmark("x"))` reveal.

Measured on a real clip — `a-number-is-hidden-inside-this-box-we-double-it-51a9e40c.wav`
(23.211 s, "A number is hidden inside this box. We double it, and then take away seven. …"):

| Point | Claimed time | Real audio | Error |
| --- | --- | --- | --- |
| first word `A` | 0.000 s | speech starts 0.271 s | 0.27 s early |
| `box.` | 1.802 s | pause begins 2.180 s | 0.38 s early |
| `number?` | 8.073 s | pause begins 8.009 s | lands **inside** the pause |
| `five.` | 17.372 s | pause was 16.994–17.189 s | ~0.4 s late |
| `statement.` | 22.202 s | trailing pause begins 22.990 s | **0.79 s early** |

Errors in one 23-second clip span roughly **0.03 s to 0.79 s**. And the failure mode is worst exactly
where this episode lives: numerals, token IDs (`27746`, `5281`, `8582`), `CAPITALIZATION`, `🎵`, `##`
are all mis-weighted by a character-count heuristic that assumes every character takes equal time.

**Why this never got caught:** `verify_sync.py` checks only that each caption overlaps
*silence-detected speech* (`CAPTION_OK = 0.60`). An estimated SRT still passes that gate. So the
existing verifiers cannot detect word-level drift — they detect stale or missing captions, not
inaccurate ones.

**Impact on this episode:** the storyboard's entire pedagogy depends on a visual landing *on the
spoken word* ("show the unknown-token replacement before the byte-fallback explanation begins").
Sub-second drift is acceptable for a slow chalkboard lesson; it is much more visible when a token
block is supposed to appear exactly as the narrator says its ID.

### A7.4 Other pipeline findings

- `MAX_SILENT_TAIL = 5.5 s` in `verify_sync.py` is tuned for the maths series' silent "thank you"
  closing card. This episode's Scene 15 ends with narration, so the tail will be shorter — the gate
  still passes, no change needed.
- All 8 Chapter 2 Linear Equations topics share one `FORCE_STYLE` string with `pipeline_1080.py`,
  which is correct under libass (style scales with video height). The same string is reused here, so
  the 360p cut and any future 1080p master stay consistent.
- `sound_effects.load_all()` (pop/click/ding/whoosh/swipe/success) is already available and used by
  every beat; this episode will reuse it rather than adding assets.

---

# PART B — IMPLEMENTATION PLAN

## B1. Folder layout (all inside `Story-Mode-Manim-Videos/LLM_Videos/`)

```
LLM_Videos/
  CHAPTER2_EP1_AUDIT_AND_PLAN.md      ← this file
  CHAPTER2_BOOK_TEXT_EXTRACT.txt      ← verbatim book text, kept for re-verification
  assets/background.png               ← supplied backdrop
  theme.py            palette, type scale, safe area, backdrop loader, source chip
  data_traces.py      EVERY recorded value (IDs, segmentations, vocab sizes) — single source of truth
  components.py       the 9 reusable mobject families
  three_d.py          3D rigs: TokenTunnel, ControlConsole, VaultWall, EmbeddingSlab
  narration.py        NARRATION dict + bookmarks, one entry per beat
  act1_scenes.py      Scenes 01–05  (Chapter2Act1)
  act2_scenes.py      Scenes 06–08  (Chapter2Act2)
  act3_scenes.py      Scenes 09–12  (Chapter2Act3)
  act4_scenes.py      Scenes 13–15  (Chapter2Act4)
  pipeline_360.py     copied from the Chapter 2 Linear Equations convention: render 640x360@30
                      into D:\m3, copy the real SRT back, run both verifiers, burn captions
                      (-c:a copy), publish to final_videos/
  concat_acts.py      joins the four captioned act files into the single episode deliverable
  verify_frames.py    SRT timestamp -> extracted frame -> visual check helper
```

Base class in `theme.py`:

```python
class LLMScene(ThreeDScene, VoiceoverScene):   # smoke-tested ✅
```

## B2. Visual design bible (new, sampled from the backdrop)

| Role | Colour | Meaning on screen |
| --- | --- | --- |
| Raw text | `#E8F1FF` on `#0B1B33` | the human string |
| Token block | 6-colour cycle from the book p.46 (`#66C2A5 #FC8D62 #8DA0CB #E78AC3 #A6D854 #FFD92F`) | **the book's own palette** — deliberate continuity |
| Token ID | `#22D3EE` mono chips | discrete vocabulary identifier |
| Special token | `#F472B6` | `[CLS] <s> [UNK] <unk> …` |
| Unknown / loss | `#EF4444` | information destroyed |
| Byte / fallback | `#FBBF24` | byte-derived piece |
| Embedding vector | `#A78BFA` | learned parameter (never an ID) |
| Model boundary | `#38BDF8` glow | text stops here |

- Frame 16:9, backdrop at `z=-10`, content confined to the backdrop's glass panel
  (≈ 10% horizontal / 8% vertical safe inset), bottom **0.9** reserved for subtitles.
- Two persistent corner chips: `illustrative` (amber) / `book-recorded` (cyan) — satisfies F7.
- Recurring sample string, identical across Scenes 09–14, from the book p.46:
  `English and CAPITALIZATION\n\n🎵鸟\nshow_tokens False None elif == >= else: two tabs:"\t" Three tabs: "    "\n\n12.0*50=600`
  Stored once in `data_traces.py`; the camera shows sub-regions of it.

## B3. 3D plan (the "high-level 3D diagrams" requirement)

| Act | Shot | 3D treatment |
| --- | --- | --- |
| I | Scene 01 | **Token Tunnel** — camera flies through a receding 3D corridor of numbered input slots; the text prompt bounces off the model boundary |
| I | Scene 05 | **Vault Wall** — 3D lattice of vocabulary blocks; `play` stem + suffix tiles snap together |
| II | Scene 06 | **Control Console** — three physical 3D dials; `set_camera_orientation` orbits the console |
| II | Scene 07 | **Vocabulary Vault** — 3D receding row stack, `apolog`/`izing` rows extrude forward and morph into ID chips |
| III | Scene 09 | **Laboratory Bench** — four 3D machines in a row; camera tracks along the bench |
| IV | Scene 15 | **Embedding Slab** — 3D matrix slab; the two ID rows glow and extrude into vectors, then the camera pulls back to reveal the wider model stack |

All other scenes stay 2D on the backdrop for legibility (the storyboard's own "don't show dozens of
tiny blocks" rule). Roughly **6 of 15** scenes carry 3D — high-impact, not gratuitous.

## B4. Build order (each phase ends in something you can watch)

| Phase | Work | Output |
| --- | --- | --- |
| **0** | `theme.py` + `data_traces.py` + backdrop wiring; render one 5 s 3D+narrated proof | proof clip — confirms backdrop framing, palette, voice |
| **1** | `components.py` (9 families) + `three_d.py` | component test scene |
| **2** | Act I — Scenes 01–05 | `Act1_captioned.mp4` (~6 min) |
| **3** | Act II — Scenes 06–08 | `Act2_captioned.mp4` (~3 min) |
| **4** | Act III — Scenes 09–12 (the centrepiece) | `Act3_captioned.mp4` (~6 min) |
| **5** | Act IV — Scenes 13–15 | `Act4_captioned.mp4` (~3 min) |
| **6** | Final 1080p60 per act, caption burn, concat | single episode file |

The pipeline at every phase, exactly as the repo already does it:
`narration+bookmarks → edge-tts voiceover → real per-word SRT → 360p30 preview → burn captions →
extract frames at SRT timestamps and *look at them* → fix → repeat → 1080p60`.

## B5. Accuracy guards to carry into the code

1. Every number on screen comes from `data_traces.py`, tagged `book` or `illustrative`.
2. **No invented token IDs, ever** (F5). Where the book gives no IDs, show no IDs.
3. `##`/`<unk>`/`[UNK]`/`</s>`/`<s>` rendered exactly as the book prints them (F6).
4. Scene 9's four machines are explicitly stamped a subset of the book's eight (F4).
5. GPT-2 labelled "BPE (byte fallback)", not "byte-level" (F1).
6. The full ~200-char book sample string is stored in animation data even when the camera shows a
   sub-region — tokenisation depends on surrounding text, so we never compare a short string against
   outputs recorded for the long one.

## B6. Estimated effort / render budget

Following `pipeline_360.py` (640×360 @ 30 fps) makes the loop cheap enough to iterate properly.

| Item | Estimate |
| --- | --- |
| Script volume | ~4,500–6,000 lines across 8 modules |
| Single 360p act render | roughly 3–8 min wall-clock per ~5 min of animation |
| Preview iterations | 4 acts × ~4 rounds × ~5 min ≈ **80 min** of render |
| Audio | ~19.5 min of narration across ~200 beats; cached per beat, so re-renders reuse it |
| Caption burn + concat | ~1–2 min total at 360p |
| 1080p master (deferred) | a separate `pipeline_1080.py` run when the episode is locked |

---

# PART C — CONFIRMED DECISIONS

| # | Decision | Status |
| --- | --- | --- |
| 1 | **Content** | ✅ Apply audit fixes **F1–F7** and additions **G1–G6**. Episode grows to ≈19:30 |
| 2 | **Sequencing** | ✅ Act-by-act, with a review checkpoint after each act |
| 3 | **Render / captions / audio** | ✅ Follow `pipeline_360.py` exactly: **640×360 @ 30 fps**, real SRT, captions burned, audio kept (`-c:a copy`), deliverable into `final_videos/`. 1080p master deferred |
| 4 | **Voice** | ✅ **Option B chosen** — Zephyr's sound with edge-tts-derived real word timings |

### Decision 4 — resolved: Zephyr's voice, measured timing (Option B)

The house code no longer uses edge-tts (A7.2), and the newer voice's word timings are *estimated*
rather than measured (A7.3) — measured error 0.03–0.79 s per clip, worst on numerals and token IDs,
which is exactly this episode's material.

The chosen path keeps the voice and fixes the clock. `audio.HybridZephyrSpeechService` synthesises
with Zephyr, measures the clip's real duration and silence structure with ffmpeg, takes the per-word
offset curve from edge-tts for the same text, and resamples that shape onto the Zephyr clip's own
measured speech span — snapping any word that lands inside a measured pause forward to the moment
speech resumes. Both ends are anchored by measurement rather than assumption, so the result sounds
like the newest videos in the repo *and* every reveal lands on the word it belongs to.

Verified across all 60 beats of the episode: duration ratio **0.84–1.43** against the expected
speaking time, **1.73–3.10 words/second**. No take is truncated. See `IMPLEMENTATION_NOTES.md` §3.


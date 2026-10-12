# Class 6 — Final Videos (1080p60, captions burned in)

These are the finished masters for the Class 6 Chapter 2 set. Each file is a
byte-for-byte copy of the delivered master in its topic folder.

**Specification:** 1920×1080, 60 fps, H.264 (crf 18, yuv420p), audio copied from
the render, series caption style burned into the picture (white bold on a dark
box, bottom-left aligned).

| # | Video | File | Duration |
|---|---|---|---|
| 01 | Whole Numbers | `WholeNumbersStory_captioned.mp4` | 4:36 (275.9 s) |
| 02 | Operations on Whole Numbers | `OperationsOnWholeNumbersStory_captioned.mp4` | 3:28 (207.9 s) |
| 03 | Commutative and Associative Properties | `CommutativeAssociativeStory_captioned.mp4` | 3:57 (236.7 s) |
| 04 | Distributive Property and Identities | `DistributivePropertyStory_captioned.mp4` | 4:03 (243.2 s) |
| 05 | Geometric Dot Patterns | `DotPatternsStory_captioned.mp4` | 4:26 (266.4 s) |

## Verification (run on these exact files)

| # | Sync (`verify_sync.py`) | Captions (`verify_captions.py`) | Per-beat audit | Layout flags |
|---|---|---|---|---|
| 01 | PASS — 0 in silence, 0 uncaptioned | PASS — 706 = 706 words | 11/12 exact, closing ring +0.30 s | 0 |
| 02 | PASS — 0 in silence, 0 uncaptioned | PASS — 453 = 453 words | 11/12 exact, closing ring +0.30 s | 0 |
| 03 | PASS — 0 in silence, 0 uncaptioned | PASS — 586 = 586 words | 11/12 exact, closing ring +0.30 s | 0 |
| 04 | PASS — 0 in silence, 0 uncaptioned | PASS — 618 = 618 words | 11/12 exact, closing ring +0.32 s | 0 |
| 05 | PASS — 0 in silence, 0 uncaptioned | PASS — 682 = 682 words | 11/12 exact, closing ring +0.37 s | 0 |

Video 05 was re-rendered after a layout pass (the line in scene 1 centred on the
board, the floating count moved level with the shapes, the question no longer
cross-fades into the equations, the "25" on each sticker packet cleared of the
circle, and the four recap shapes put on a common baseline) and its closing
narration now speaks "See you in the next lesson!" as well — hence the longer
runtime and the extra caption cue.

The single non-zero per video is the highlight ring drawn around the Thank-You
card, deliberately allowed to finish just after the last spoken word. Full
report: `../CLASS6_CHAPTER2_AUDIT.md`.

## Where the sources live

For each video, in the chapter folder:

- master: `<Topic>/media/videos/<module>/1080p60/<File>` (the copy here)
- 360p30 review copy: `<Topic>/media/videos/<module>/360p30/…_captioned.mp4`
- sidecar subtitles (same text as the burned captions):
  `<Topic>/media/videos/<module>/1080p60/<Class>.real.srt`
- build script, sync/overlap audit and proof frames: in the topic folder itself

## Uploading

The captions are burned in, so the videos need no subtitle track. If a platform
also wants a sidecar file (for searchable captions or corrections), use the
`.real.srt` next to each master — it carries the identical text and timing.

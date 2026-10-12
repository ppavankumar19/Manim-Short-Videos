# Rational Numbers — 1080p60 subtitle files

The eight 1080p60 (1920×1080, 60 fps) ground-truth SRTs of the Rational Numbers
story-mode set, collected in one place. Each file is a byte-for-byte copy of the
`1080p60/real.srt` written by that topic's own render, so the timings are the
render's real word boundaries — not a transcription and not a re-timed draft.

| # | file | topic folder | render |
|---|---|---|---|
| 01 | `01 - Decimal Forms of Rational Numbers.srt` | `Decimal-Forms-of-Rational-Numbers` | `decimal_forms_story/1080p60` |
| 02 | `02 - Properties of Rational Numbers.srt` | `Properties-of-Rational-Numbers` | `properties_of_rational_numbers_story/1080p60` |
| 03 | `03 - Identities and Inverses.srt` | `Identities-and-Inverses` | `identities_inverses_story/1080p60` |
| 04 | `04 - The Distributive Property.srt` | `Distributive-Property-Smart-Simplification` | `distributive_property_story/1080p60` |
| 05 | `05 - Representing Rational Numbers on the Number Line.srt` | `Rational-Numbers-on-Number-Line` | `rational_numbers_number_line/1080p60` |
| 06 | `06 - Smart Rearrangement of Rational Numbers.srt` | `Smart-Rearrangement-Rational-Numbers` | `smart_rearrangement_story/1080p60` |
| 07 | `07 - Density of Rational Numbers.srt` | `Density-Property-of-Rational-Numbers` | `density_property_lesson/1080p60` |
| 08 | `08 - Nested Number Systems.srt` | `Nested-Number-Systems` | `nested_number_systems_story/1080p60` |

## Check (`verify_sync.py <1080p60 video> <srt>`)

Every file was checked against its own 1080p60 render: the SRT must cover the
video's speech, hold no caption in silence, and leave no speech block
(> 1.0 s) uncaptioned.

| file | video | cues | first cue | last cue | in silence | uncaptioned | result |
|---|---|---|---|---|---|---|---|
| 01 Decimal Forms | 214.67 s | 60 | 0.00 s | 212.05 s | 0 | 0 | **PASS** |
| 02 Properties | 224.17 s | 61 | 0.00 s | 221.55 s | 0 | 0 | **PASS** |
| 03 Identities and Inverses | 208.67 s | 53 | 0.00 s | 206.05 s | 0 | 0 | **PASS** |
| 04 The Distributive Property | 308.88 s | 87 | 0.00 s | 306.27 s | 0 | 0 | **PASS** |
| 05 Number Line | 203.73 s | 60 | 0.00 s | 201.12 s | 0 | 0 | **PASS** |
| 06 Smart Rearrangement | 223.70 s | 64 | 0.00 s | 221.09 s | 0 | 0 | **PASS** |
| 07 Density | 298.83 s | 88 | 0.00 s | 296.02 s | 0 | 0 | **PASS** |
| 08 Nested Number Systems | 165.72 s | 41 | 0.00 s | 163.11 s | 0 | 0 | **PASS** |

## A defect found in two files, and the fix

Files **01** and **02** arrived with one malformed timestamp each:

```
01:  00:01:57,1000 --> 00:02:01,051      (should be  00:01:58,000)
02:  00:01:31,1000 --> 00:01:36,559      (should be  00:01:32,000)
```

A four-digit millisecond field is not valid SRT. libass still rendered those
cues when the captions were burned in (checked frame by frame at 1:59 and 1:33),
but strict parsers — YouTube's subtitle reader and this repo's `verify_sync.py` —
drop the whole cue, which is why 02 first reported two uncaptioned speech blocks.

Cause: the SRT writer in every story module rounded the fractional part on its
own, `ms = int(round((t - int(t)) * 1000))`, which yields `1000` for a cue
boundary within half a millisecond below a whole second.

Repaired, so this folder is clean:

1. **The files** — `D:\Manim-Short-Videos\fix_srt_timestamps.py` carries an
   over-long field into the next second (`,1000` → `+1 s,000`). It repaired 13
   SRT files across the repo (including the two here); the copy in this folder is
   taken from the repaired source, so source and collection agree.
2. **The generator** — `D:\Manim-Short-Videos\fix_srt_writer.py` rewrote the
   formatter in all 15 story modules that still had the buggy rounding, so no
   future render can write `,1000` again (the other 24 modules were already
   carry-safe). Both tools are idempotent; re-running them reports 0 changes.

The burned-in captioned videos were **not** re-encoded: the affected cues were
verified visible in the delivered files, and the SRT files themselves are what
needed to be valid for separate-subtitle use.

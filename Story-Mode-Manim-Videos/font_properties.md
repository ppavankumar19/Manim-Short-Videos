# Font properties — Story-Mode chalkboard videos

Applies to the Red Blood Cell video and the three Physics videos (plain board,
`TEXT_SCALE` 0.92). Older videos use the same fonts with `TEXT_SCALE` 0.72 or 1.0.

Frame: 14.222 × 8 units. 360p = 45 px/unit, 1080p = 135 px/unit.

## 1. Board text

| Property | Value |
|---|---|
| Font | **Segoe Print** (Windows `segoeprb.ttf`, bold) — `FONT` in `bio_kit.py` |
| Weight | Bold for everything |
| Size rule | written size × `TEXT_SCALE` (0.92), never below **14 pt** |
| Too-wide text | shrunk to fit its box (a few labels end up a little smaller) |
| Colours | amber `#E8B769` headings · white body · yellow `#FFE066` · cyan `#7FE7DC` · green `#9BE38A` · red `#FF6B6B` · pink / blue / purple accents |
| Card fill | `#16202B` (dark) |

Measured height = line height of the text (ascenders to descenders).

| Use | Written | Actual size | 360p | 1080p |
|---|---|---|---|---|
| Title card, main line | 58–60 | 53–55 pt | 35–36 px | 106–109 px |
| Title card, sub-lines | 38 / 34 / 30 | 35 / 31 / 28 pt | 23 / 21 / 18 px | 69 / 62 / 55 px |
| "Thank You for Watching" | 60 | 55 pt | 36 px | 109 px |
| "See you in the next lesson" | 44 | 40.5 pt | 27 px | 80 px |
| Closing slogans | 42 | 38.6 pt | 26 px | 77 px |
| Scene heading | 36 | 33 pt | 22 px | 66 px |
| Subtitle line (e.g. "YOUR TURN" line) | 28 | 26 pt | 17 px | 51 px |
| Card body text | 22 | 20 pt | 13 px | 40 px |
| Chips and labels | 20 | 18 pt | 12 px | 36 px |
| Smallest text (credit, notes) | 14 | 14 pt | 9 px | 28 px |
| Corner badge ("Physics", "dhimantAI") | 12 × 1.33 | 16 pt | 11 px | 33 px |

A capital letter in a scene heading is 0.36 units tall: 16 px at 360p, 49 px at 1080p.

## 2. Maths (LaTeX `MathTex`, Computer Modern)

Scaled by the same 0.92. The height includes the fraction bar and both lines,
so one fraction is far taller than a line of text.

| Written | Actual size | 360p | 1080p |
|---|---|---|---|
| 66 | 61 pt | 63 px | 190 px |
| 54 | 50 pt | 52 px | 156 px |
| 40 | 37 pt | 38 px | 115 px |
| 34 | 31 pt | 33 px | 98 px |

## 3. Burned-in captions

Made with ffmpeg's `subtitles` filter (libass); no font name is set, so it falls
back to **Arial** (confirmed: `fontselect: Arial → ArialMT`).

| Property | Value |
|---|---|
| Font | Arial (default), **bold** |
| Size | `FontSize=9.5` in libass units (a 384×288 grid), ≈ 11.9 px em at 360p, ≈ 35.6 px at 1080p |
| Text colour | white `&HFFFFFF&` |
| Box | `BorderStyle=3` (opaque box), colour `&H80000000&` (black, 50 % transparent), `Outline=1.6`, `Shadow=0` |
| Alignment | bottom centre (libass default) |
| Margins (360p, current) | `MarginV=4`, `MarginL=10`, `MarginR=10` (env `BIO_SUB_MARGINV` / `BIO_SUB_MARGINL`) |
| Margins (1080p script) | `MarginV=10`, `MarginL=43`, `MarginR=10` (not changed) |
| Words per line | about 9 per caption chunk, taken from the narration |

Measured on a test frame with a typical caption line:

| | Text height (ascender to descender) | Box height | Box bottom to frame bottom |
|---|---|---|---|
| 360p (MarginV 4) | 9 px (2.5 % of frame height) | 17 px | 2 px |
| 1080p (MarginV 10) | 29 px (2.7 % of frame height) | 49 px | 31 px |

Caption text is therefore about as tall as the 14 pt minimum board text (9 px at
360p) and a little smaller than a chip label (12 px).

## 4. Where it is set

- Board font, scale, minimum size, colours: `Biology - Class 10\bio_kit.py` (`FONT`, `TEXT_SCALE`, `T()`, `M()`).
- Physics reuses it through `Physics - Class 10\phys_kit.py`.
- Caption style: `pipeline_360.py` and `pipeline_1080.py` (`FORCE_STYLE`) in the Biology and Physics folders.

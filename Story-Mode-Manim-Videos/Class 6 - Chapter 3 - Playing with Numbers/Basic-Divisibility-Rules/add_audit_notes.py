"""Append the production-audit fix record to this video's storyboard.

    python add_audit_notes.py
"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE / "storyboard.md"

NOTE = """
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
"""


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    if "production audit fixes" in text:
        print("already noted, skipped")
        return
    TARGET.write_text(text.rstrip("\n") + "\n" + NOTE, encoding="utf-8")
    print(f"{TARGET.name} -> {TARGET.stat().st_size} bytes")


if __name__ == "__main__":
    main()

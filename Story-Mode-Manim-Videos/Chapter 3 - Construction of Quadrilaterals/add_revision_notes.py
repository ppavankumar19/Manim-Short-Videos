"""Append the revision note for the cm-unit / centred-THINK re-cut to each
storyboard.  Idempotent: running it twice adds nothing the second time.

    python add_revision_notes.py
"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent

HEAD = """
---

## Revision — on-board `cm` unit, centred THINK clock (re-cut 360p)

Two on-screen fixes were asked for and applied, then the 360p cut was re-rendered
with the captions burned in:

1. **Every length on the board now shows its unit.** {cards} The narration
   already said "centimetres"; the board now agrees with it. Angles are
   untouched ({angles}).
2. **The THINK countdown is centred on the board.** It is parked at
   `(BOARD_CX, BOARD_CY)` — the series default `story_common.CLOCK_POS` — so the
   paused clock is the centre of the frame instead of {where}.

Re-verified after the change: `audit_sync_overlap.py` → 0 real flags (only the
deliberate {stretch} closing flourish, logged in `audit_after_cm.log`);
`verify_sync.py` → PASS, {caps} captions, 0 captions in silence, 0 speech blocks
uncaptioned, {dur} s; `verify_captions.py` → PASS, {words} = {words} words.
Unchanged timing ({dur2} s) confirms the change is cosmetic only.
Visual proof: `frames360/after_cm/{frames}`.
"""

NOTES = {
    "SASAA-2-Sides-3-Angles": dict(
        cards=("The measurement cards read `P Q = 4 cm`, `Q R = 4.8 cm`, and the "
               "two practice cards read\n   `A B = 5 cm`, `B C = 4 cm`; the "
               "verification rows repeat them with the unit — 12 places\n   in "
               "all, including the \"USE LATER\" and check panels."),
        angles="`\u2220P = 75\u00b0`, `\u2220Q = 100\u00b0`, `\u2220R = 120\u00b0` carry no unit",
        where="sitting in the right-hand gap",
        stretch="0.37 s", caps=69, dur="224.37", dur2="224.4", words=598,
        frames=("05_cards.png` (the `cm` cards) and\n"
                "`frames360/after_cm/05_timer.png` (the centred clock)")),
    "SASAS-3-Sides-2-Angles": dict(
        cards=("The measurement cards read `A B = 5 cm`, `B C = 4.5 cm`, "
               "`C D = 6 cm` — in the\n   measurement chain, the build panels, "
               "the verification rows and the practice column\n   (`P Q = 3.6 cm`, "
               "`Q R = 4.5 cm`, `R S = 5.6 cm`) — 15 places in all."),
        angles="`\u2220B = 100\u00b0`, `\u2220C = 75\u00b0`, `\u2220Q = 135\u00b0`, `\u2220R = 60\u00b0`",
        where="sitting in the right-hand gap",
        stretch="0.37 s", caps=72, dur="247.07", dur2="247.1", words=631,
        frames=("06_cards.png` and `06_cards_full.png` (the `cm` chain\n"
                "cards) and `frames360/after_cm/06_timer.png` (the centred clock)")),
    "Special-Quads": dict(
        cards=("The cards read `B E = 4.2 cm`, `E L = 5 cm`, `A C = 4.5 cm`, "
               "`B D = 6 cm`, and the\n   derived values read "
               "`O B = O D = 6/2 = 3 cm` and `4.2 \u00f7 2 = 2.1 cm` — 10 places "
               "in all, belt and\n   rhombus, given and derived."),
        angles="`\u2220T = 45\u00b0`, `\u2220E = 45\u00b0`, `\u2220A = 65\u00b0`",
        where="below the figure",
        stretch="0.37 s", caps=94, dur="315.53", dur2="315.5", words=815,
        frames=("07_cards.png` and `frames360/after_cm/07_timer.png`\n"
                "(the centred clock, with `8 cm` / `6 cm` on the challenge text)")),
}


def main() -> None:
    for folder, kw in NOTES.items():
        path = HERE / folder / "storyboard.md"
        text = path.read_text(encoding="utf-8")
        if "centred THINK clock" in text:
            print(f"{folder}: already noted, skipped")
            continue
        note = HEAD.format(**kw)
        path.write_text(text.rstrip("\n") + "\n" + note, encoding="utf-8")
        print(f"{folder}: storyboard.md {len(text)} -> {path.stat().st_size} bytes")


if __name__ == "__main__":
    main()

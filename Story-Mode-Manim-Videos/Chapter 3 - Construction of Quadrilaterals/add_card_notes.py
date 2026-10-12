"""Append the addendum for the figure/card overlap fix to video 06's storyboard.

    python add_card_notes.py
"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE / "SASAS-3-Sides-2-Angles" / "storyboard.md"

NOTE = """
## Revision 2b — the method cards no longer sit on the figure

Two more problems were reported from the rendered master and are fixed:

- **The four method cards overlapped the figure.** In "Required Quadrilateral
  ABCD" the column of cards (`1. SKETCH … 4. FINAL SIDE`) started at x = +1.48
  while the figure's `C` vertex and the `C D` and `C B` edges reach x = +1.65 —
  so the cards were drawn *over* the figure's corner and its `C` label
  (a LINE-IN-BOX hit: a figure edge running inside a card). The column now
  starts at +2.03, a 0.38 gap, and still ends at +4.77, well inside the
  board's +5.60 edge.
- **The recap rows (1), (2), (3) crowded the figure's `C` label** (0.09 gap).
  The rows moved 0.35 to the right: the gap is now 0.44 and the rows end at
  +4.44.

Both were caught by a new check in `audit_clearance.py` that reports chalk from
one part of a scene lying inside another part's card (`TEXT-IN-BOX`,
`LINE-IN-BOX`) — the overlap class a text-against-text audit cannot see, since
the figure's edges are not text. All three videos in this batch now report
**0 foreign-box collisions**; this one also reports 0 text/line collisions and
0 hard-overlap flags.

Re-rendered after the fix: the 360p review cut (`finals_360/`) and the 1080p60
master (`final_videos/`), both verified — `verify_sync` PASS (72 captions, 0 in
silence, 0 uncaptioned) and `verify_captions` PASS (631 = 631 words). The
narration and every `run_time` are untouched, so the timing is unchanged.
"""


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    if "Revision 2b" in text:
        print("already noted, skipped")
        return
    TARGET.write_text(text.rstrip("\n") + "\n" + NOTE, encoding="utf-8")
    print(f"{TARGET.name} -> {TARGET.stat().st_size} bytes")


if __name__ == "__main__":
    main()

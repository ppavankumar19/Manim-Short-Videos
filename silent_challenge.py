"""Make each chapter-4 challenge a silent pause.

For every topic:

  * `beat_s9` becomes two narration pieces -- the questions, then (after the
    clock has run with nothing but its own ticks) the answers -- with the ten
    second THINK clock between them, outside any voiceover;
  * the closing card stops narrating over itself: the "thank you / see you in
    the next lesson" card is held in silence;
  * `setup_tools.py` learns the two new pieces (`s9q`, `s9a`) and their anchors.

    python silent_challenge.py [--dry]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(r"D:\Manim-Short-Videos\Story-Mode-Manim-Videos"
            r"\Class 8 - Chapter 4 - Exponents and Powers")
TOPICS = {
    "Introduction-to-Exponents-and-Powers": (
        "_exponents_beats.py", "seven is repeated four times"),
    "Negative-Exponents-and-Multiplicative-Inverses": (
        "_negative_beats.py", "is one over ten to the power four"),
    "Product-and-Quotient-Laws-of-Exponents": (
        "_laws_beats.py", "for the first the exponents add"),
    "Advanced-Laws-of-Exponents": (
        "_advlaws_beats.py", "three to the power four all squared multiplies"),
    "Standard-Form-with-Powers-of-10": (
        "_standard_form_beats.py",
        "for the first the decimal moves right five places"),
}
CLOCK_WAIT = '            self.wait(leftover(tracker, "b1"))\n'
CLOCK_NOTE = (
    "        # the ten-second THINK pause is deliberately SILENT: the questions\n"
    "        # have been read, and there is no narration to sync here -- only the\n"
    "        # clock and its tick\n")


def restructure_beats(text: str) -> str:
    i = text.index("    def beat_s9(self) -> None:")
    j = text.index("    # -- Scene 10", i)
    body = text[i:j]
    lines = body.splitlines(keepends=True)

    clock = next(n for n, ln in enumerate(lines)
                 if "play_challenge_countdown(" in ln)
    first = clock
    while first > 0 and lines[first - 1].lstrip().startswith("#"):
        first -= 1
    last = clock + 1                                   # the call's 2nd line
    while "position=np.array" not in lines[last]:
        last += 1
    wait = max(n for n in range(first)
               if lines[n] == CLOCK_WAIT)

    head = "".join(lines[:wait])
    clock_block = "".join("    " + ln[4:] if ln.startswith("    ") else ln
                          for ln in lines[first:last + 1])
    tail = "".join(lines[last + 1:])
    tail = tail.replace("        self.wait(TRANSITION_HOLD)", "\x00")
    tail, stop = tail.split("\x00", 1)
    tail = tail.rstrip("\n") + "\n"

    for k in (2, 3, 4, 5):                             # renumber the answers
        tail = tail.replace(f'"b{k}"', f'"bTMP{k - 2}"')
    for k in (0, 1, 2, 3):
        tail = tail.replace(f'"bTMP{k}"', f'"b{k}"')

    return (text[:i] + head
            + "            self._capture_srt(tracker)\n\n"
            + CLOCK_NOTE + clock_block + "\n"
            + '        with self.voiceover(text=NARRATION["s9a"]) as tracker:\n'
            + tail
            + "        self.wait(TRANSITION_HOLD)"
            + "\x00" + stop + text[j:]).replace("\x00", "")


def silence_closing(text: str) -> str:
    return text.replace(
        """            self.play(Indicate(thanks, color=CHALK_YELLOW, scale_factor=1.03),
                      run_time=rt(tracker.get_remaining_duration()))""",
        """            # the closing card is deliberately silent: the board says it,
            # and there is no narration left here to sync
            self.play(Indicate(thanks, color=CHALK_YELLOW, scale_factor=1.03),
                      run_time=1.2)""")


def update_tools(text: str, s9a_anchor: str) -> str:
    text = text.replace(
        'PIECE_ORDER = ["title"] + [f"s{i}" for i in range(1, 11)]',
        'PIECE_ORDER = (["title"] + [f"s{i}" for i in range(1, 9)]\n'
        '               + ["s9q", "s9a", "s10"])')
    text = text.replace('    "s9": "your turn",',
                        '    "s9q": "your turn",\n'
                        f'    "s9a": "{s9a_anchor}",')
    return text


def main() -> int:
    dry = "--dry" in sys.argv
    for topic, (beats_name, anchor) in TOPICS.items():
        bpath = ROOT / topic / beats_name
        spath = ROOT / topic / "setup_tools.py"
        beats = bpath.read_text(encoding="utf-8")
        tools = spath.read_text(encoding="utf-8")
        if 'NARRATION["s9a"]' in beats:
            print(f"  {topic}: already done")
            continue
        new_beats = silence_closing(restructure_beats(beats))
        new_tools = update_tools(tools, anchor)
        assert new_beats.count('NARRATION["s9a"]') == 1, topic
        assert 'run_time=1.2)' in new_beats, topic
        assert '"s9a":' in new_tools, topic
        if not dry:
            bpath.write_text(new_beats, encoding="utf-8")
            spath.write_text(new_tools, encoding="utf-8")
        print(f"  {'would update' if dry else 'updated'} {topic}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

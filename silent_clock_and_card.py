"""Make the THINK clock and the closing thank-you card truly SILENT.

Two structural fixes in every chapter-4 beats file:

1. ``play_challenge_countdown`` was still indented inside the ``s9q``
   voiceover block, so the ten-second clock ran *while the questions were
   being read*.  It must sit after the ``with`` block, so the questions are
   read first and the clock then ticks alone (only the tick SFX).

2. The closing thank-you card plays were still inside the ``s10`` voiceover
   block.  They move after it, so the recap stays on the board until the
   narration has finished and the card is then shown with no voice over it.

Both edits are pure indentation/ordering: no narration text changes, so the
cached TTS audio stays valid.
"""
from __future__ import annotations

import re
import textwrap
from pathlib import Path

HERE = (Path(__file__).parent / "Story-Mode-Manim-Videos"
        / "Class 8 - Chapter 4 - Exponents and Powers")
FILES = [
    "Introduction-to-Exponents-and-Powers/_exponents_beats.py",
    "Negative-Exponents-and-Multiplicative-Inverses/_negative_beats.py",
    "Product-and-Quotient-Laws-of-Exponents/_laws_beats.py",
    "Advanced-Laws-of-Exponents/_advlaws_beats.py",
    "Standard-Form-with-Powers-of-10/_standard_form_beats.py",
]
S10_MARK = "    # -- Scene 10: recap"

P1 = re.compile(
    r"(?P<cap> {12}self\._capture_srt\(tracker\)\n)"
    r"\n"
    r"(?:[^\S\n]*#[^\n]*\n)*?"          # stale comment lines, any indent
    r"[^\S\n]*play_challenge_countdown\(self, seconds=10, sfx=self\.sfx,\n"
    r"[^\S\n]*position=np\.array\(\[BOARD_CX, BOARD_CY, 0\]\)\)\n"
)

P1_NEW = (
    "{cap}"
    "\n"
    "        # The ten-second THINK pause is deliberately SILENT -- the\n"
    "        # questions have just been read, so the clock ticks alone, with\n"
    "        # no narration to sync against.\n"
    "        play_challenge_countdown(self, seconds=10, sfx=self.sfx,\n"
    "                                 position=np.array([BOARD_CX, BOARD_CY, 0]))\n"
)

P2 = re.compile(
    r"(?P<fade>^ {12}self\.play\(FadeOut\([^\n]*\n"
    r"(?:[^\S\n]*[^\n]*\n)*?)"
    r" {12}self\.play\(FadeIn\(thanks, shift=UP \* 0\.10\), run_time=0\.5\)\n"
    r" {12}self\.play\(FadeIn\(bye, shift=UP \* 0\.10\), run_time=0\.45\)\n"
    r"(?:[^\S\n]*#[^\n]*\n)+"
    r" {12}self\.play\(Indicate\(thanks, color=CHALK_YELLOW, scale_factor=1\.03\),\n"
    r"[^\S\n]*run_time=1\.2\)\n"
    r" {12}self\._capture_srt\(tracker\)\n"
    r"\n"
    r" {8}self\.wait\(END_HOLD\)",
    re.MULTILINE,
)


def dedent4(block: str) -> str:
    return "".join(line[4:] if line.startswith("    ") else line
                   for line in block.splitlines(keepends=True))


def p1_new(match: re.Match[str]) -> str:
    return P1_NEW.format(cap=match.group("cap"))


def p2_new(match: re.Match[str]) -> str:
    return (
        "            self._capture_srt(tracker)\n"
        "\n"
        "        # The closing card is deliberately SILENT: the recap clears\n"
        "        # once the narration has finished, and the thank-you card is\n"
        "        # then shown with no voice over it.\n"
        + dedent4(match.group("fade"))
        + "        self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.5)\n"
        + "        self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)\n"
        + "        self.play(Indicate(thanks, color=CHALK_YELLOW, "
          "scale_factor=1.03),\n"
        + "                  run_time=1.2)\n"
        + "\n"
        + "        self.wait(END_HOLD)"
    )


def main() -> int:
    rc = 0
    for rel in FILES:
        path = HERE / rel
        src = path.read_text(encoding="utf-8")
        if src.count(S10_MARK) != 1:
            print(f"!! {rel}: s10 marker count {src.count(S10_MARK)}")
            rc = 1
            continue
        # the clock lives in beat_s9, the card in beat_s10: keep the two
        # substitutions in their own halves so neither can span the file
        head, tail = src.split(S10_MARK, 1)
        tail = S10_MARK + tail
        m1 = list(P1.finditer(head))
        m2 = list(P2.finditer(tail))
        if len(m1) != 1 or len(m2) != 1:
            print(f"!! {rel}: clock matches={len(m1)} card matches={len(m2)}"
                  " (expected 1 and 1)")
            rc = 1
            continue
        n1, n2 = 1, 1
        a = m1[0]
        head = head[:a.start()] + p1_new(a) + head[a.end():]
        b = m2[0]
        tail = tail[:b.start()] + p2_new(b) + tail[b.end():]
        src2 = head + tail
        if n1 != 1 or n2 != 1:
            print(f"!! {rel}: clock={n1} card={n2} (expected 1 and 1)")
            rc = 1
            continue
        try:
            # the beats files are class-body fragments, so dedent first
            compile(textwrap.dedent(src2.lstrip("\ufeff")), str(path), "exec")
        except SyntaxError as exc:                      # pragma: no cover
            print(f"!! {rel}: syntax error after edit: {exc}")
            rc = 1
            continue
        path.write_text(src2, encoding="utf-8")
        print(f"ok {rel}: clock silent, closing card silent")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())

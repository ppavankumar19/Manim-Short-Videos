"""Split each chapter-4 challenge narration into "questions" and "answers"
pieces, with the ten-second pause removed from the narration, and drop the
spoken "thank you ... see you in the next lesson" from the closing piece.

The pause is no longer narrated: the questions are read first, then the clock
runs in silence (its ticks only), then the answers are read.

    python split_challenge_narration.py [--dry]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(r"D:\Manim-Short-Videos\Story-Mode-Manim-Videos"
            r"\Class 8 - Chapter 4 - Exponents and Powers")
FRAGMENTS = [
    "Introduction-to-Exponents-and-Powers/_exponents_fragment.py",
    "Negative-Exponents-and-Multiplicative-Inverses/_negative_fragment.py",
    "Product-and-Quotient-Laws-of-Exponents/_laws_fragment.py",
    "Advanced-Laws-of-Exponents/_advlaws_fragment.py",
    "Standard-Form-with-Powers-of-10/_standard_form_fragment.py",
]

PAUSE = re.compile(
    r"(?P<questions>.*?)\s*<bookmark mark='b1'/>\s*Take ten seconds.*?"
    r"<bookmark mark='b2'/>(?P<answers>.*)", re.S)
THANKS = re.compile(r"\s*Thank you for watching.*$", re.S)
QUOTED = re.compile(r'"([^"]*)"')


def prose(block: str) -> str:
    """The entry's text as one line, with the bookmark tags made whole again
    (a wrapped source line can leave "<bookmark  mark='b2'/>")."""
    joined = " ".join(QUOTED.findall(block))
    joined = re.sub(r"<bookmark\s+mark='(\w+)'\s*/>", r"<bookmark mark='\1'/>",
                    joined)
    return " ".join(joined.split())


def emit(key: str, text: str, width: int = 76) -> str:
    """Re-emit a narration entry as a wrapped, valid Python literal."""
    lines, cur = [], ""
    for word in text.split():
        if cur and len(cur) + 1 + len(word) > width:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    lines.append(cur)
    body = "\n".join(f'        "{line} "' for line in lines[:-1])
    body += f'\n        "{lines[-1]}"'
    return f'    "{key}": (\n{body}\n    ),'


def main() -> int:
    dry = "--dry" in sys.argv
    for rel in FRAGMENTS:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")

        if '"s9q": (' in text:                      # already split: normalise it
            keys = {}
            for key in ("s9q", "s9a", "s10"):
                m = re.search(rf'    "{key}": \((.*?)\n    \),', text, re.S)
                keys[key] = (m, prose(m.group(1)))
            out = text
            for key, (m, text_now) in keys.items():
                out = out.replace(m.group(0), emit(key, text_now))
            if not dry:
                path.write_text(out, encoding="utf-8")
            print(f"  {'would normalise' if dry else 'normalised'} {rel}"
                  f"  (s9q {len(keys['s9q'][1])} chars)")
            continue

        m9 = re.search(r'    "s9": \((.*?)\n    \),', text, re.S)
        m10 = re.search(r'    "s10": \((.*?)\n    \),', text, re.S)
        if not m9 or not m10:
            print(f"  !! entries not found in {rel}")
            continue
        p9, p10 = prose(m9.group(1)), prose(m10.group(1))
        parts = PAUSE.match(p9)
        if not parts:
            print(f"  !! pause sentence not found in {rel}")
            continue
        questions = parts.group("questions").strip()
        answers = parts.group("answers").strip()
        answers = "<bookmark mark='b0'/>" + re.sub(
            r"<bookmark mark='b(\d+)'/>",
            lambda mm: f"<bookmark mark='b{int(mm.group(1)) - 2}'/>",
            answers)
        closing = THANKS.sub("", p10).strip()
        assert "Thank you" not in closing, rel
        assert "Take ten seconds" not in answers, rel
        new = (emit("s9q", questions) + "\n" + emit("s9a", answers) + "\n"
               + emit("s10", closing))
        out = text[:m9.start()] + new + text[m10.end():]
        if not dry:
            path.write_text(out, encoding="utf-8")
        print(f"  {'would split' if dry else 'split'} {rel}")
        print(f"      s9q: {questions[:88]}…")
        print(f"      s9a: {answers[:88]}…")
        print(f"      s10 ends: …{closing[-58:]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

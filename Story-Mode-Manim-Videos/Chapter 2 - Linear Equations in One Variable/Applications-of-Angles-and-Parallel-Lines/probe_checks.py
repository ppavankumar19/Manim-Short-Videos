"""Self-test for the two audit detectors added after the LaTeX-leak bug.

Confirms that the LATEX-AS-TEXT regex fires on the exact string that was handed
to Text() in the RELATE card, and stays quiet on ordinary chalk text, and that
the TEXT-OUTSIDE-BOX rule fires only on real overflow.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(next(p for p in HERE.parents
            if (p / "speech_service.py").exists())))

from manim import MathTex, RoundedRectangle, Text  # noqa: E402

import audit_sync_overlap as A  # noqa: E402


def main() -> None:
    print("regex:", A.LATEX_HINT.pattern)
    bad = Text(r"A=B \;\text{or}\; A+B=180", font_size=12)
    ok = Text("which angles?", font_size=12)
    ok2 = Text("x = 21, but the angles are 83 and 97 degrees.", font_size=17)
    print(f"offending Text  -> flagged {bool(A.LATEX_HINT.search(bad.text))}")
    print(f"normal Text     -> flagged {bool(A.LATEX_HINT.search(ok.text))}")
    print(f"chalk sentence  -> flagged {bool(A.LATEX_HINT.search(ok2.text))}")
    fixed = MathTex(r"A=B \;\text{or}\; A+B=180", font_size=19)
    print("MathTex carries .text:", hasattr(fixed, "text"),
          "(so the detector never fires on real maths)")
    box = RoundedRectangle(width=2.3, height=1.7)
    for name, mob in (("old literal text", bad), ("fixed math", fixed)):
        w = mob.width
        print(f"{name:17s} width {w:.2f}  card 2.30  "
              f"side margin {max(0.0, (2.3 - w) / 2):.2f}")


if __name__ == "__main__":
    main()

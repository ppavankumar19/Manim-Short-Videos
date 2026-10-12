"""Add the cm unit to measurement cards and centre the THINK clock.

Run once per topic folder:

    python add_cm_centre_timer.py <folder> <beats-file> <assemble-script>

  * every `measure_card`, `check_row` and `value_card` whose label is a length
    (it has an "=" and is neither an angle nor already carries a unit) gets
    "\\text{ cm}" appended, so the unit is on the board and not only in the
    narration;
  * the challenge countdown is centred on the board: its `position` becomes
    (BOARD_CX, BOARD_CY) instead of being parked in a gap.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

FOLDER = Path(sys.argv[1]).resolve()
BEATS = FOLDER / sys.argv[2]
ASSEMBLE = sys.argv[3]

MAKERS = ("measure_card", "check_row", "value_card")
CALL = re.compile(
    r'(?P<fn>' + "|".join(MAKERS) + r')\((?P<prefix>\s*)r"(?P<label>[^"]*)"')
COUNTDOWN = re.compile(r"position=np\.array\(\[[^\]]*\]\)")


def wants_cm(label: str) -> bool:
    if "=" not in label:
        return False
    if "\\angle" in label or "circ" in label or "cm" in label:
        return False
    if "\\div" in label or "\\tfrac" in label or "\\frac" in label:
        return True
    return True


def main() -> None:
    s = BEATS.read_text(encoding="utf-8")
    n0 = len(s)
    added = []

    def repl(m: re.Match) -> str:
        label = m.group("label")
        if not wants_cm(label):
            return m.group(0)
        added.append(label)
        return f'{m.group("fn")}({m.group("prefix")}r"{label}\\text{{ cm}}"'

    s = CALL.sub(repl, s)
    s, n_timer = COUNTDOWN.subn("position=np.array([BOARD_CX, BOARD_CY, 0])", s)

    BEATS.write_text(s, encoding="utf-8")
    print(f"{FOLDER.name}: {len(added)} labels got cm, {n_timer} countdown "
          f"centred, {n0} -> {len(s)} chars")
    for label in added:
        print(f"    {label}  ->  {label}\\text{{ cm}}")
    if n_timer != 1:
        print(f"    WARNING: expected exactly one countdown position, "
              f"found {n_timer}")

    out = subprocess.run([sys.executable, ASSEMBLE], cwd=FOLDER,
                         capture_output=True, text=True)
    print("    " + (out.stdout.strip().splitlines() or ["assembler failed"])[0])
    if out.returncode != 0:
        print(out.stderr)


if __name__ == "__main__":
    main()

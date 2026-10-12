"""Fourth patch: bring the R letter back to scenes 5, 6 and 7.

An earlier `str.replace` of the vertex-letter block matched every scene that had
the same two lines after it, so scenes 5-7 lost the letter R along with scene 4
(where R genuinely does not exist yet).  This patch works by line number and
asserts what it is changing.
"""
from pathlib import Path

P = Path(__file__).resolve().parent / "_sasaa_beats.py"
lines = P.read_text(encoding="utf-8").splitlines()

WANT = ("                (P, Q), ((-0.28, -0.10), (0.12, -0.30)))")
NEW = ("                (P, Q, R), ((-0.28, -0.10), (0.12, -0.30), "
       "(0.50, -0.40)))")

# 1-based line numbers of the block's second line in scenes 5, 6 and 7
targets = [488, 554, 627]
for n in targets:
    assert lines[n - 1] == WANT, f"line {n} is {lines[n - 1]!r}"
assert lines[432] == WANT, "scene 4 must keep only P and Q"

for n in targets:
    lines[n - 1] = NEW

P.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("restored the R letter in scenes 5, 6 and 7")
for n in targets:
    print(f"  {n}: {lines[n - 2].strip()} / {lines[n - 1].strip()}")

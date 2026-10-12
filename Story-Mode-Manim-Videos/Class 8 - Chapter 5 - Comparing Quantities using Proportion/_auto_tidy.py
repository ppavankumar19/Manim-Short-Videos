"""Insert `tidy(..., same=True)` calls into a topic template.

For every narrated segment of every beat it finds the boxed items built there
(calc_row / step_row / route_row / tcard / part_card / mistake_card / q_card /
chip with an explicit w) and groups the ones that were given the same width,
so a stack of rows ends up one common (tight) width -- aligned, hugging the
text, with no dead air.  Rows built in a `rows = [...]` list are tidied
together.  Idempotent: lines it adds carry the marker  # auto-tidy.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

MAKERS = ("calc_row", "step_row", "route_row", "tcard", "part_card",
          "mistake_card", "q_card", "chip", "fmath", "fact_card",
          "partner_card")
DEFAULT_W = {"calc_row": "9.6", "step_row": "9.6", "route_row": "9.6",
             "tcard": "3.1", "part_card": "3.1", "mistake_card": "4.8",
             "q_card": "4.85", "chip": "-", "fmath": "-", "fact_card": "4.7",
             "partner_card": "4.7"}


def balanced(text, start):
    """text[start] == '(' -> index just past the matching ')'."""
    depth = 0
    i = start
    in_str = None
    while i < len(text):
        ch = text[i]
        if in_str:
            if ch == "\\":
                i += 1
            elif ch == in_str:
                in_str = None
        elif ch in "\"'":
            in_str = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return len(text)


def main(path):
    p = Path(path)
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"[ ]*[^\n]*# auto-tidy\n", "", s)          # idempotent
    beats = [m.start() for m in re.finditer(r"\n    def beat_", s)] + [len(s)]
    out = s[:beats[0]]
    for a, b in zip(beats, beats[1:]):
        body = s[a:b]
        segs = [m.start() for m in re.finditer(r"\n        with self\.narrate\(",
                                               body)] + [len(body)]
        new = body[:segs[0]]
        for c, d in zip(segs, segs[1:]):
            seg = body[c:d]
            groups = defaultdict(list)
            lists = []
            for m in re.finditer(r"\n            (\w+) = (?:P\(|hrow\()?(\w+)\(",
                                 seg):
                name, fn = m.group(1), m.group(2)
                if fn not in MAKERS:
                    continue
                st = m.end() - 1
                end = balanced(seg, st)
                call = seg[st:end]
                wm = re.search(r"\bw=([0-9.]+)", call)
                w = wm.group(1) if wm else DEFAULT_W[fn]
                if w == "-":
                    continue
                groups[(fn, w)].append(name)
            if re.search(r"\n            rows = \[", seg) and \
                    re.search(r"zip\(rows", seg):
                lists.append("rows")
            stmts = []
            for (fn, w), names in groups.items():
                if len(names) >= 2:
                    stmts.append(f"            tidy({', '.join(names)}, same=True)"
                                 f"  # auto-tidy\n")
            for st_ in list(stmts):
                if "tidy(qa, qb, qc, qd, same=True)" in st_:
                    stmts.append("            for q_ in (qa, qb, qc, qd):  # auto-tidy\n"
                                 "                q_.scale(0.90)  # auto-tidy\n")
            for nm in lists:
                stmts.append(f"            tidy(*{nm}, same=True)  # auto-tidy\n")
            k = seg.find("\n            self.cue(")
            kf = seg.find("\n            for k, r in enumerate(rows):")
            cand = [x for x in (k, kf) if x >= 0]
            if stmts and cand:
                pos = min(cand) + 1
                seg = seg[:pos] + "".join(stmts) + seg[pos:]
            new += seg
        out += new
    p.write_text(out, encoding="utf-8")
    print("tidied", p.name)


if __name__ == "__main__":
    for f in sys.argv[1:]:
        main(f)

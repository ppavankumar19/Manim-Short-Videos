import re
import sys

p = sys.argv[1]
keys = set(sys.argv[2:])
s = open(p, encoding="utf-8").read()
body = s.split("NARRATION = {", 1)[1].split("\n}", 1)[0]
for m in re.finditer(r'"(\w+)"\s*:\s*(.*?)(?=\n\s*"\w+"\s*:|\Z)', body, re.S):
    k = m.group(1)
    if keys and k not in keys:
        continue
    prose = " ".join(re.findall(r'"([^"]*)"', m.group(2)))
    prose = re.sub(r"<bookmark mark='[^']*'/>", " | ", prose)
    print("==", k, "==")
    print(" ".join(prose.split()))
    print()

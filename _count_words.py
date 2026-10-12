import re
import sys
from pathlib import Path

mod = Path(sys.argv[1])
srt = Path(sys.argv[2])
text = mod.read_text(encoding="utf-8")
body = text.split("NARRATION = {", 1)[1].split("\n}", 1)[0]
prose_all = []
for m in re.finditer(r'"(\w+)"\s*:\s*(.*?)(?=\n\s*"\w+"\s*:|\Z)', body, re.S):
    prose = " ".join(re.findall(r'"([^"]*)"', m.group(2)))
    prose = re.sub(r"<bookmark mark='[^']*'/>", " ", prose)
    prose_all.append(prose)
nar = " ".join(prose_all)
nw = len([w for w in nar.split() if w.strip()])
print("narration words:", nw)

CUE = re.compile(
    r"(\d\d):(\d\d):(\d\d),(\d\d\d) --> (\d\d):(\d\d):(\d\d),(\d\d\d)\s*\n"
    r"(.*?)(?=\n\s*\n|\Z)", re.S)
cues = list(CUE.finditer(srt.read_text(encoding="utf-8")))
sw = 0
for m in cues:
    sw += len(m.group(9).split())
print("captions:", len(cues), "srt words:", sw)
first = cues[0]
last = cues[-1]
print("first cue:", first.group(1), first.group(2), first.group(3), first.group(4))
print("last cue end:", last.group(5), last.group(6), last.group(7), last.group(8))

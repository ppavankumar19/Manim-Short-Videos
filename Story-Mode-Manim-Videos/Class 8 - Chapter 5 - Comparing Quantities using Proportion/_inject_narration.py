"""Build <topic>/<module>.py = template body + the ORIGINAL NARRATION dict.

    python _inject_narration.py <topic-dir> <module-stem>

The narration (and its bookmarks) is copied verbatim from
_original_scripts/<topic-dir>/<module>.py, so the cached TTS audio and the
caption word-for-word check stay valid.  The template lives next to the output
as <module>.tpl.py and must contain the line `NARRATION = {}  # __NARRATION__`.
"""
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
topic, stem = sys.argv[1], sys.argv[2]
orig = (here / "_original_scripts" / topic / f"{stem}.py").read_text(encoding="utf-8")
start = orig.index("NARRATION = {")
end = orig.index("\n}\n", start) + 3
block = orig[start:end].rstrip("\n")
tpl = (here / topic / f"{stem}.tpl.py").read_text(encoding="utf-8")
assert "NARRATION = {}  # __NARRATION__" in tpl
out = tpl.replace("NARRATION = {}  # __NARRATION__", block)
(here / topic / f"{stem}.py").write_text(out, encoding="utf-8")
print("wrote", here / topic / f"{stem}.py", len(out.splitlines()), "lines")

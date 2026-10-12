#!/bin/bash
# usage: ./_stills.sh <topic-dir> <module-stem> <Class> [beats,comma] [res]
# Renders every beat WITHOUT audio into stills_out/<module-stem>/ and prints the layout audit.
HERE="$(cd "$(dirname "$0")" && pwd)"
TOPIC="$1"; STEM="$2"; CLS="$3"; ONLY="${4:-}"; RES="${5:-1280,720}"
OUT="$HERE/stills_out/$STEM"
rm -f "$OUT"/*.png 2>/dev/null; mkdir -p "$OUT"
cd "$HERE/$TOPIC"
CH5_STILLS="$OUT" CH5_ONLY="$ONLY" /d/Manim-Short-Videos/.venv/Scripts/python.exe -m manim render -r $RES --fps 5 --media_dir "D:/m3s" "$STEM.py" "$CLS" 2>&1 | grep -E "AUDIT|SHRINK|ART-|STILLS DONE|Error|error|Traceback|File \"|line [0-9]+" | head -80
ls "$OUT" | wc -l

#!/bin/bash
# usage: ./_queue.sh "<topic> <module> <Class>" ...   -- renders 360p + burned subs sequentially
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE"
for job in "$@"; do
  set -- $job
  echo "=== $1" ; /d/Manim-Short-Videos/.venv/Scripts/python.exe pipeline_360.py "$1" "$2.py" "$3" > "render_$2.log" 2>&1
  tail -c 300 "render_$2.log" | tr -d '\0' | grep RESULT
done

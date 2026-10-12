#!/bin/bash
# audit one topic: prints the end-state audit lines only
HERE="$(cd "$(dirname "$0")" && pwd)"
"$HERE/_stills.sh" "$@" 2>&1 | grep -E "AUDIT|ART-STILL|Traceback|Error" | grep -o "AUDIT [a-z0-9]*/end\].*\|ART-STILL.*\|Error.*" | cut -c1-300

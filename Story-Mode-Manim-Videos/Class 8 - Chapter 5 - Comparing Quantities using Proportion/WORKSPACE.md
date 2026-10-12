# Class 8 - Chapter 5 workspace

Shared code (this folder): `ch5_kit.py` (board geometry, text/boxes, audits, sync log),
`ch5_art.py` (drawn articles), `ch5_widgets.py` (cards/rows), `_auto_tidy.py`.

Per topic folder: `<module>.tpl.py` (EDIT THIS) -> `python _inject_narration.py <topic> <module>`
writes `<module>.py` (what Manim renders; narration is copied verbatim from `_original_scripts/`).

Commands
- layout audit (silent frames): `./_stills.sh <topic> <module> <Class>`  -> `stills_out/`
- render 360 + burn captions:   `./_queue.sh "<topic> <module> <Class>"` -> `final_videos/`
- 1080p60 master:               `python pipeline_1080.py <topic> <module>.py <Class>`
- sync report:                  `python _sync_check.py`, `python _frame_sync.py`

Rules every video follows
1. A topic-name-only intro card (own narration) opens the video, then scene 1.
2. Everything inside the green board (SAFE_* in ch5_kit); nothing on teacher/students/badges (AVOID_ART).
3. Medium type (TEXT_SCALE 0.85), never below 14 pt; boxes hug their text (TIGHT_BOXES) and a
   stack of boxes shares one width AND height; boxes keep >= 0.10 gap (STRICT_BOXES audit).
4. Each picture appears at its narration bookmark (sync log: 0 late reveals).

Status: Compound-Ratio... FINALISED (360). The other six are on the older layout pass and still need
the intro card + this review, one by one.
`_workspace_archive/` holds old logs, drafts and the retired per-topic helper scripts.

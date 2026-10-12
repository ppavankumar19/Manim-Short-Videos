"""Create this topic's audit tooling from the Chapter 3 quadrilaterals set.

The quadrilaterals videos grew the audit tooling this series now uses; the
generic parts are copied verbatim and the topic-specific parts (module name,
class name, SRT path, narration anchors) are rewritten for this video.

    python setup_tools.py

Creates, in the topic folder:
    audit_sync_overlap.py   hard overlaps, per-piece sync stretch and the
                            IN-CAPTION-BAND safe-zone check
    audit_clearance.py      tight text pairs, text-on-line, chalk-in-foreign-box
    scene_frames.py         one still per scene at its hold moment
    find_timer.py           locates the THINK countdown window
    tts_precheck.py         asks the speech service for each narration piece
and, in this chapter folder:
    pipeline_360.py         render 360p30 -> verify -> burn captions -> finals
"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent            # the topic folder
CHAPTER = HERE.parent
REPO = next(p for p in HERE.parents if (p / "speech_service.py").exists())
QUADS = (REPO / "Story-Mode-Manim-Videos"
         / "Chapter 3 - Construction of Quadrilaterals")
DONOR_TOPIC = QUADS / "SASAA-2-Sides-3-Angles"

MODULE = "divisibility_rules_advanced_4_8_11"
CLASS = "DivisibilityRulesAdvancedStory"

PIECE_ORDER = ["hook", "title"] + [f"scene{i}" for i in range(1, 9)] + [
    "apply", "scene9", "scene10"]
PIECE_ANCHORS = {
    "hook": "these tests are not only for the classroom",
    "title": "three more divisibility tests",
    "scene1": "the scanner knows six rules",
    "scene2": "divisibility by four",
    "scene3": "now use it on",
    "scene4": "divisibility by eight",
    "scene5": "do not mix the two",
    "scene6": "divisibility by eleven",
    "scene7": "now a number that fails",
    "scene8": "three advanced rules three clues",
    "apply": "fifty six thousand four hundred ninety six seats",
    "scene9": "your turn",
    "scene10": "one last look",
}

VERBATIM = ("audit_clearance.py", "scene_frames.py", "find_timer.py")


def copy_verbatim() -> None:
    for name in VERBATIM:
        src = QUADS / name
        (HERE / name).write_text(src.read_text(encoding="utf-8"),
                                 encoding="utf-8")
        print(f"copied {name}")
    src = DONOR_TOPIC / "tts_precheck.py"
    (HERE / "tts_precheck.py").write_text(src.read_text(encoding="utf-8"),
                                          encoding="utf-8")
    print("copied tts_precheck.py")


def write_audit() -> None:
    text = (DONOR_TOPIC / "audit_sync_overlap.py").read_text(encoding="utf-8")

    text = text.replace(
        '"""Sync & overlap audit harness for '
        'construct_quadrilateral_2sides_3angles.py.',
        f'"""Sync & overlap audit harness for {MODULE}.py.')
    text = text.replace(
        "from construct_quadrilateral_2sides_3angles import (  # noqa: E402",
        f"from {MODULE} import (  # noqa: E402")
    text = text.replace(
        "    ConstructQuadrilateral2Sides3AnglesStory,\n)",
        f"    {CLASS},\n)")
    text = text.replace("ConstructQuadrilateral2Sides3AnglesStory", CLASS)

    old_srt = ('SRT = (_HERE / "media" / "videos" / '
               '"construct_quadrilateral_2sides_3angles" / "360p30"\n'
               f'       / "{CLASS}.real.srt")')
    new_srt = ('SRT = (_HERE / "media" / "videos" / '
               f'"{MODULE}" / "360p30"\n'
               f'       / "{CLASS}.real.srt")')
    assert old_srt in text, "SRT path anchor not found"
    text = text.replace(old_srt, new_srt)

    # The caption band was measured on this video's own burned 360p cut (a
    # one-line cue starts at y = -3.38, a wrapped two-line cue reaches -2.93),
    # and the production audit asked for more clearance, so the safe line for
    # this topic is -2.00 rather than the donor's -2.15.
    old_safe = ("# The burned-in captions occupy the bottom of the frame: a "
                "one-line cue starts\n"
                "# at y = -3.33 and a two-line cue reaches up to y = -2.33.  "
                "Nothing on the\n"
                "# board may sit below this line, or the subtitle covers it.\n"
                "CAPTION_SAFE_Y = -2.15")
    new_safe = ("# The burned-in captions occupy the bottom of the frame: a "
                "one-line cue starts\n"
                "# at y = -3.38 and a wrapped two-line cue reaches up to "
                "y = -2.93 (measured\n"
                "# on this video's own burned cut).  The closing banners were "
                "lifted 0.15 to\n"
                "# STRIP_Y = -1.80, so nothing sits below CAPTION_SAFE_Y and "
                "the subtitle can\n"
                "# never cover the board.\n"
                "CAPTION_SAFE_Y = -2.00")
    assert old_safe in text, "CAPTION_SAFE_Y block not found"
    text = text.replace(old_safe, new_safe)

    i = text.index("PIECE_ORDER = [")
    j = text.index("def norm_word")          # the next definition after them
    block = ("PIECE_ORDER = [\n"
             + "".join(f'    "{p}",\n' for p in PIECE_ORDER)
             + "]\nPIECE_ANCHORS = {\n"
             + "".join(f'    "{k}": "{v}",\n' for k, v in PIECE_ANCHORS.items())
             + "}\n\n\n")
    text = text[:i] + block + text[j:]
    (HERE / "audit_sync_overlap.py").write_text(text, encoding="utf-8")
    print("wrote audit_sync_overlap.py")


def write_pipeline() -> None:
    text = (QUADS / "pipeline_360.py").read_text(encoding="utf-8")
    text = text.replace("FINALS = HERE / \"finals_360\"",
                        "FINALS = HERE / \"final_videos\"")
    (CHAPTER / "pipeline_360.py").write_text(text, encoding="utf-8")
    print(f"wrote {CHAPTER / 'pipeline_360.py'}")


if __name__ == "__main__":
    copy_verbatim()
    write_audit()
    write_pipeline()

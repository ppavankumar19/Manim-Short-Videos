"""Create this topic's tooling from the Chapter 3 quadrilaterals set.

The quadrilaterals videos grew the audit tooling this series now uses; the
generic parts are copied verbatim and the topic-specific parts (module name,
class name, SRT path, narration anchors) are rewritten for this video.

    python setup_tools.py

Creates, in the topic folder:
    audit_sync_overlap.py   hard overlaps + per-piece sync stretch
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

MODULE = "divisibility_rules_basic_2_3_5_6_9_10"
CLASS = "DivisibilityRulesBasicStory"

PIECE_ORDER = ["title"] + [f"scene{i}" for i in range(1, 11)]
PIECE_ANCHORS = {
    "title": "every number carries a clue about its",
    "scene1": "hasini has one hundred and twenty five chocolates",
    "scene2": "what does divisible mean twenty four",
    "scene3": "divisibility by two take nine hundred",
    "scene4": "divisibility by five and ten",
    "scene5": "divisibility by three is different",
    "scene6": "divisibility by nine the same digits",
    "scene7": "divisibility by six needs two tests",
    "scene8": "now use it three hundred seventy two",
    "scene9": "which of two three five six",
    "scene10": "all six rules in three ideas",
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
        '"""Sync & overlap audit harness for construct_quadrilateral_2sides_3angles.py.',
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
    text = text.replace("copy the captioned movie and its .srt into finals_360\\.",
                        "copy the captioned movie and its .srt into the\\\n"
                        "     chapter's final_videos\\.")
    (CHAPTER / "pipeline_360.py").write_text(text, encoding="utf-8")
    print(f"wrote {CHAPTER / 'pipeline_360.py'}")


if __name__ == "__main__":
    copy_verbatim()
    write_audit()
    write_pipeline()


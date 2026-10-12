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

The chapter's `pipeline_360.py` (render -> verify -> burn -> final_videos) and
`pipeline_1080.py` already sit one folder up.
"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent            # the topic folder
CHAPTER = HERE.parent
REPO = next(p for p in HERE.parents if (p / "speech_service.py").exists())
QUADS = (REPO / "Story-Mode-Manim-Videos"
         / "Chapter 3 - Construction of Quadrilaterals")
DONOR_TOPIC = QUADS / "SASAA-2-Sides-3-Angles"

MODULE = "negative_exponents_and_multiplicative_inverse"
CLASS = "NegativeExponentsInverseStory"

PIECE_ORDER = (["title"] + [f"s{i}" for i in range(1, 9)]
               + ["s9q", "s9a", "s10"])
PIECE_ANCHORS = {
    "title": "negative exponents",
    "s1": "last time exponents wrote the sun's width",
    "s2": "start with the powers you already know",
    "s3": "but the staircase does not stop at one",
    "s4": "the pattern is not special to ten",
    "s5": "now we can write the rule for any base",
    "s6": "here is the mistake to avoid",
    "s7": "now look in a mirror",
    "s8": "finding an inverse is quick",
    "s9q": "your turn",
    "s9a": "ten to the power minus four is one over",
    "s10": "one last look",
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

    # The caption band was measured on the series' burned 360p cuts (a one-line
    # cue starts at y = -3.38, a wrapped two-line cue reaches -2.93), and the
    # production audit asked for the closing banners to stand well clear, so the
    # safe line for this topic is -2.00 rather than the donor's -2.15.
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
                "# on the series' own burned cut).  The closing strip sits at "
                "STRIP_Y = -1.80, so\n"
                "# nothing is below CAPTION_SAFE_Y and the subtitle can never "
                "cover the board.\n"
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


if __name__ == "__main__":
    copy_verbatim()
    write_audit()
    print(f"\nchapter pipeline: {CHAPTER / 'pipeline_360.py'}")



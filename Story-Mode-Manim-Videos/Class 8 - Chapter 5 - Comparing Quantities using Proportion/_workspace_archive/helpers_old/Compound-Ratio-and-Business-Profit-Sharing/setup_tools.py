"""Create this topic's audit tooling from the Class 6 Chapter 4 set.

Those videos grew the audit tooling this series now uses (the strict
`audit_badge_clearance.py`, the -2.00 caption band and the left-aligned column
checks), so the generic parts are copied verbatim and the topic-specific parts
(module name, class name, SRT path, narration anchors, heading list) are
rewritten for this video.

    python setup_tools.py

Creates, in the topic folder:
    audit_sync_overlap.py     hard overlaps, per-piece sync stretch and the
                              IN-CAPTION-BAND safe-zone check
    audit_clearance.py        tight text pairs, text-on-line, chalk-in-foreign-box
    audit_badge_clearance.py  every heading vs both corner badges (>= 0.30 units)
    scene_frames.py           one still per scene at its hold moment
    find_timer.py             locates the THINK countdown window
    tts_precheck.py           asks the speech service for each narration piece

The chapter's `pipeline_360.py` (render -> verify -> burn -> final_videos)
already sits one folder up.
"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent            # the topic folder
CHAPTER = HERE.parent
REPO = next(p for p in HERE.parents if (p / "speech_service.py").exists())
DONOR = (REPO / "Story-Mode-Manim-Videos"
         / "Class 6 - Chapter 4 - Basic Geometrical Ideas"
         / "Quadrilaterals-Sides-Angles-and-Diagonals")

MODULE = "compound_ratio_and_business_proportions"
CLASS = "CompoundRatioAndBusinessProportionsStory"

PIECE_ORDER = (["title"] + [f"s{i}" for i in range(1, 9)]
               + ["s9q", "s9a", "s10"])
# The first five words of each piece, exactly as voiced: the audit re-synchronises
# every piece on these, so one mismatch cannot shift the pieces after it.
PIECE_ANCHORS = {
    "title": "meet two partners",
    "s1": "a ratio is an ordered comparison",
    "s2": "now suppose both partners keep",
    "s3": "now suppose both partners invest",
    "s4": "but in our business both",
    "s5": "to combine two ratios we",
    "s6": "let us apply the rule",
    "s7": "now let us turn that",
    "s8": "here is the decision rule",
    "s9q": "your turn",
    "s9a": "the inverse of seven to",
    "s10": "one last look",
}

VERBATIM = ("audit_clearance.py", "scene_frames.py", "find_timer.py",
            "tts_precheck.py")


def copy_verbatim() -> None:
    for name in VERBATIM:
        (HERE / name).write_text((DONOR / name).read_text(encoding="utf-8"),
                                 encoding="utf-8")
        print(f"copied {name}")


def write_audit() -> None:
    text = (DONOR / "audit_sync_overlap.py").read_text(encoding="utf-8")

    text = text.replace(
        '"""Sync & overlap audit harness for '
        'quadrilaterals_sides_angles_and_diagonals.py.',
        f'"""Sync & overlap audit harness for {MODULE}.py.')
    text = text.replace(
        "from quadrilaterals_sides_angles_and_diagonals import (  # noqa: E402",
        f"from {MODULE} import (  # noqa: E402")
    text = text.replace(
        "    QuadrilateralsSidesAnglesAndDiagonalsStory,\n)",
        f"    {CLASS},\n)")
    text = text.replace("QuadrilateralsSidesAnglesAndDiagonalsStory", CLASS)
    text = text.replace("quadrilaterals_sides_angles_and_diagonals", MODULE)

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


def write_badge_audit() -> None:
    text = (DONOR / "audit_badge_clearance.py").read_text(encoding="utf-8")
    text = text.replace(
        "from quadrilaterals_sides_angles_and_diagonals import (  # noqa: E402",
        f"from {MODULE} import (  # noqa: E402")
    text = text.replace("QuadrilateralsSidesAnglesAndDiagonalsStory", CLASS)

    i = text.index("ITEMS = (")
    j = text.index("print(f\"\\n{'item':12s}")
    items = (
        ("title", "Two Partners, One Profit", 26, 1.98),
        ("title.sub", "Ramayya and Gopalam: money and time together.", 17, 1.42),
        ("s1.head", "A Ratio Is an Ordered Comparison", 20, "ROW_Y"),
        ("s2.head", "Same Time for Both Partners", 20, "ROW_Y"),
        ("s3.head", "Same Capital, Different Time", 20, "ROW_Y"),
        ("s4.head", "Both Capital and Time Differ", 20, "ROW_Y"),
        ("s5.head", "The Compound Ratio Rule", 20, "ROW_Y"),
        ("s6.head", "Applying the Compound Ratio", 20, "ROW_Y"),
        ("s7.head", "From Ratio to Rupees", 20, "ROW_Y"),
        ("s8.head", "Which Ratio Decides the Share?", 20, "ROW_Y"),
        ("s9.head", "YOUR TURN", 26, 2.78),
        ("s9.sub", "Four quick checks.", 16, 2.20),
        ("s10.head", "Inverse · Compound · Partnership", 22, "ROW_Y"),
        ("s1.sub", "Three to two is not two to three.", 17, "SUB_Y"),
        ("s2.sub", "The time factor cancels.", 17, "SUB_Y"),
        ("s3.sub", "The capital factor cancels.", 17, "SUB_Y"),
        ("s4.sub", "Neither ratio alone is enough.", 17, "SUB_Y"),
        ("s5.sub", "Multiply the corresponding terms.", 17, "SUB_Y"),
        ("s6.sub", "Two to three, compounded with four to three.",
         17, "SUB_Y"),
        ("s7.sub", "Divide the profit into equal parts.", 17, "SUB_Y"),
        ("s8.sub", "Time, capital, or both.", 17, "SUB_Y"),
        ("s10.sub", "Money and time together decide the share.", 17, "SUB_Y"),
    )
    body = "ITEMS = (\n"
    for tag, text_, size, y in items:
        yv = y if y == "ROW_Y" or y == "SUB_Y" else y
        body += (f'    ("{tag}", "{text_}", {size}, {yv}),\n')
    body += ")\n\n"
    text = text[:i] + body + text[j:]
    (HERE / "audit_badge_clearance.py").write_text(text, encoding="utf-8")
    print("wrote audit_badge_clearance.py")


if __name__ == "__main__":
    copy_verbatim()
    write_audit()
    write_badge_audit()
    print(f"\nchapter pipeline: {CHAPTER / 'pipeline_360.py'}")

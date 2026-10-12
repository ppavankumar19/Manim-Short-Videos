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

MODULE = "compounding_periods_half_yearly_quarterly_depreciation"
CLASS = "CompoundingPeriodsHalfYearlyQuarterlyDepreciationStory"

PIECE_ORDER = (["title"] + [f"s{i}" for i in range(1, 9)]
               + ["s9q", "s9a", "s10", "s11"])
# The first three-to-five words of each piece, exactly as voiced and already
# normalised (the audit strips punctuation and lowercases the spoken stream, so
# a hyphenated spoken word arrives here without its hyphen).  The audit
# re-synchronises every piece on these, so one mismatch cannot shift the pieces
# after it.
PIECE_ANCHORS = {
    "title": "one thousand rupees at",
    "s1": "first the conversion period",
    "s2": "now the halfyearly rule",
    "s3": "let us work it",
    "s4": "a year has four",
    "s5": "the same structure answers",
    "s6": "now depreciation the mirror",
    "s7": "one structure three uses",
    "s8": "here is the decision",
    "s9q": "your turn",
    "s9a": "let us check",
    "s10": "let us gather the",
    "s11": "one last look",
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

    # This topic's class name pushes the media path past the 260-character
    # MAX_PATH limit, so the rendered SRT is read through the extended-length
    # form (the chapter pipeline renders into the short D:\m3 media dir).
    old_read = '    lines = SRT.read_text(encoding="utf-8").splitlines()'
    new_read = "    lines = _read_srt().splitlines()"
    assert text.count(old_read) == 1, text.count(old_read)
    text = text.replace(old_read, new_read)
    helper = '''def _read_srt() -> str:
    """Read the rendered SRT.

    This topic's media path runs past the 260-character MAX_PATH limit (the
    render is done into the short D:\\\\m3 media dir and copied back here), so the
    extended-length form is used when the plain path is too long for the OS.
    """
    try:
        return SRT.read_text(encoding="utf-8")
    except OSError:
        return Path("\\\\\\\\?\\\\" + str(SRT.resolve())).read_text(encoding="utf-8")


'''
    anchor = "def parse_srt() -> list[tuple[str, float]]:"
    assert text.count(anchor) == 1, text.count(anchor)
    text = text.replace(anchor, helper + anchor)

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
        ("title", "Compounding Periods, Growth & Depreciation", 26, 2.06),
        ("title.sub", "Half-Yearly · Quarterly · Growth · Depreciation", 17,
         1.46),
        ("s1.head", "The Conversion Period", 20, "ROW_Y"),
        ("s2.head", "Half-Yearly: Two Changes at Once", 20, "ROW_Y"),
        ("s3.head", "Half-Yearly: Rs 1,000 at 10%", 20, "ROW_Y"),
        ("s4.head", "Quarterly: R/4 and 4n", 20, "ROW_Y"),
        ("s5.head", "Population Growth Is Compound", 20, "ROW_Y"),
        ("s6.head", "Depreciation: Keeping (100 - R)%", 20, "ROW_Y"),
        ("s7.head", "One Structure, Three Uses", 20, "ROW_Y"),
        ("s8.head", "Five Steps to Apply It", 20, "ROW_Y"),
        ("s9.head", "YOUR TURN", 26, 2.78),
        ("s9.sub", "Three questions and a quick check.", 16, 2.20),
        ("s10.head", "The Whole Lesson on One Board", 20, "ROW_Y"),
        ("s11.head", "Period · Rate · Factor · Repeat", 20, "ROW_Y"),
        ("s1.sub", "How often is the interest added?", 17, "SUB_Y"),
        ("s2.sub", "Halve the rate, double the periods.", 17, "SUB_Y"),
        ("s3.sub", "Rate 5% for each half-year, 2 periods.", 17, "SUB_Y"),
        ("s4.sub", "A year has four quarters.", 17, "SUB_Y"),
        ("s5.sub", "The new total becomes the next base.", 17, "SUB_Y"),
        ("s6.sub", "A reduction in value due to use and age.", 17, "SUB_Y"),
        ("s7.sub", "Growth multiplies up, depreciation down.", 17, "SUB_Y"),
        ("s8.sub", "Period, rate, factor, repeat.", 17, "SUB_Y"),
        ("s10.sub", "Period · Rate · Formula · Five Steps", 17, "SUB_Y"),
        # banners / strips (bottom rows, measured for completeness)
        ("s1.banner", "RATE AND PERIODS CHANGE TOGETHER", 18, "BANNER_Y"),
        ("s2.banner", "RATE AND PERIODS CHANGE TOGETHER", 18, "BANNER_Y"),
        ("s3.banner", "AMOUNT = Rs 1,102.50", 18, "BANNER_Y"),
        ("s5.banner", "6250 × (1.08)^2 = 7,290", 18, "BANNER_Y"),
        ("s6.banner", "25 × 0.9 × 0.9 = 20.25 m", 18, "BANNER_Y"),
        ("s8.banner", "PERIOD → RATE → FACTOR → REPEAT", 18, "BANNER_Y"),
        ("s10.banner", "PERIOD · RATE · FORMULA · FIVE STEPS", 18, "BANNER_Y"),
        ("s11.strip", "Period, rate, factor, repeat.", 16, "STRIP_Y"),
    )
    body = "ITEMS = (\n"
    for tag, text_, size, y in items:
        yv = y if y == "ROW_Y" or y == "SUB_Y" or y in ("BANNER_Y", "STRIP_Y") \
            else y
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

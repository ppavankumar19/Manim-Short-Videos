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

MODULE = "simple_vs_compound_interest_formula"
CLASS = "SimpleVsCompoundInterestFormulaStory"

PIECE_ORDER = (["title"] + [f"s{i}" for i in range(1, 9)]
               + ["s9q", "s9a", "s10"])
# The first three to five words of each piece, exactly as voiced: the audit
# re-synchronises every piece on these, so one mismatch cannot shift the pieces
# after it.
PIECE_ANCHORS = {
    "title": "ramesh and sreenu lent",
    "s1": "ramesh uses simple interest",
    "s2": "sreenu uses compound interest",
    "s3": "watch one period only",
    "s4": "now the second year",
    "s5": "one factor for every year",
    "s6": "careful this formula gives",
    "s7": "let us use it with",
    "s8": "put the two ladders side",
    "s9q": "your turn",
    "s9a": "let us check the four",
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
        ("title", "Same Money, Two Methods", 24, 2.06),
        ("title.sub", "Rs 100 for 2 years at 10%: Rs 120 or Rs 121?", 17, 1.40),
        ("s1.head", "Ramesh's Method: Simple Interest", 20, "ROW_Y"),
        ("s2.head", "Sreenu's Method: Compound Interest", 20, "ROW_Y"),
        ("s3.head", "The One-Period Growth Factor", 20, "ROW_Y"),
        ("s4.head", "The Same Factor Multiplies Again", 20, "ROW_Y"),
        ("s5.head", "One Factor for Every Year", 20, "ROW_Y"),
        ("s6.head", "The Formula Gives the Amount", 20, "ROW_Y"),
        ("s7.head", "Apply It: Rs 5,000 at 8% for 2 Years", 20, "ROW_Y"),
        ("s8.head", "Simple and Compound Side by Side", 20, "ROW_Y"),
        ("s9.head", "YOUR TURN", 26, 2.78),
        ("s9.sub", "Four quick checks.", 16, 2.20),
        ("s10.head", "Simple · Compound · Growth", 20, "ROW_Y"),
        ("s1.sub", "The interest stays on the original principal.", 17, "SUB_Y"),
        ("s2.sub", "Each new amount becomes the next principal.", 17, "SUB_Y"),
        ("s3.sub", "Amount equals principal plus the interest on it.",
         17, "SUB_Y"),
        ("s4.sub", "The year-one amount is the year-two principal.",
         17, "SUB_Y"),
        ("s5.sub", "Year one, year two, up to year n.", 17, "SUB_Y"),
        ("s6.sub", "The amount is principal plus interest.", 17, "SUB_Y"),
        ("s7.sub", "Principal Rs 5,000, rate 8%, two years.", 17, "SUB_Y"),
        ("s8.sub", "One base stays locked, the other grows.", 17, "SUB_Y"),
        # banners / strips (bottom rows, measured for completeness)
        ("s1.banner", "THE SAME INTEREST EVERY YEAR", 18, "BANNER_Y"),
        ("s2.banner", "THE INTEREST EARNED ALSO EARNS INTEREST", 18, "BANNER_Y"),
        ("s4.banner", "TWO YEARS, TWO FACTORS, ONE POWER", 18, "BANNER_Y"),
        ("s8.banner", "AFTER ONE YEAR SI AND CI ARE THE SAME", 18, "BANNER_Y"),
        ("s1.strip", "Simple interest always uses the original principal.",
         16, "STRIP_Y"),
        ("s6.strip", "The formula gives the amount, not the interest.",
         16, "STRIP_Y"),
        ("s8.strip", "The base changes only from the second year on.",
         16, "STRIP_Y"),
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

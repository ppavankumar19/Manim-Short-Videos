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

MODULE = "sales_tax_vat_and_gst_calculations"
CLASS = "SalesTaxVatAndGstCalculationsStory"

PIECE_ORDER = (["title"] + [f"s{i}" for i in range(1, 9)]
               + ["s9q", "s9a", "s10"])
# The first few words of each piece, exactly as voiced: the audit re-synchronises
# every piece on these, so one mismatch cannot shift the pieces after it.
PIECE_ANCHORS = {
    "title": "meet the price tag",
    "s1": "a tax is just",
    "s2": "now the same shoes",
    "s3": "a tax can also",
    "s4": "goods and services tax",
    "s5": "now the other direction",
    "s6": "here is a worked example",
    "s7": "now a two lane",
    "s8": "here is the classic",
    "s9q": "your turn four quick checks",
    "s9a": "let us check every answer",
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
        ("title", "The Tag Is Not the Bill", 26, 2.06),
        ("title.sub", "A pair of shoes, and a six percent tax.", 17, 1.44),
        ("s1.head", "A Tax Is a Percentage Increase", 20, "ROW_Y"),
        ("s2.head", "Sales Tax on a Pair of Shoes", 20, "ROW_Y"),
        ("s3.head", "Reading a VAT-Inclusive Bill", 20, "ROW_Y"),
        ("s4.head", "GST Uses the Same Structure", 20, "ROW_Y"),
        ("s5.head", "Finding the Price Before Tax", 20, "ROW_Y"),
        ("s6.head", "CGST and SGST in the Textbook", 20, "ROW_Y"),
        ("s7.head", "Forward or Backward?", 20, "ROW_Y"),
        ("s8.head", "The Classic Tax Error", 20, "ROW_Y"),
        ("s9.head", "YOUR TURN", 26, 2.78),
        ("s9.sub", "Four quick checks.", 16, 2.20),
        ("s10.head", "Base, Tax Rate, Bill", 22, "ROW_Y"),
        ("s1.sub", "The base price is the one hundred percent.", 17, "SUB_Y"),
        ("s2.sub", "Base Rs 450 and sales tax 6%.", 17, "SUB_Y"),
        ("s3.sub", "VAT is the same percentage idea.", 17, "SUB_Y"),
        ("s4.sub", "Base Rs 1,000 and GST at 5%.", 17, "SUB_Y"),
        ("s5.sub", "The bill is 118%, not 100%.", 17, "SUB_Y"),
        ("s6.sub", "A worked example, not a universal rule.", 17, "SUB_Y"),
        ("s7.sub", "What you were given decides the lane.", 17, "SUB_Y"),
        ("s8.sub", "Apply the rate to the base, never the bill.", 17, "SUB_Y"),
        ("s10.sub", "Four formulas to carry away.", 17, "SUB_Y"),
        # banners / strips (bottom rows, measured for completeness)
        ("title.banner", "BASE + TAX = THE FINAL BILL", 18, "BANNER_Y"),
        ("s1.banner", "A TAX IS A PERCENTAGE INCREASE", 18, "BANNER_Y"),
        ("s2.banner", "TAX Rs 27, FINAL BILL Rs 477", 18, "BANNER_Y"),
        ("s3.banner", "BASE Rs 354.45 + VAT Rs 17.72 = Rs 372.18", 16,
         "BANNER_Y"),
        ("s4.banner", "BASE + 5% GST = Rs 1,050", 18, "BANNER_Y"),
        ("s5.banner", "BASE = Rs 2,000, TAX = Rs 360", 18, "BANNER_Y"),
        ("s6.banner", "CGST Rs 180 + SGST Rs 180 = Rs 360", 17, "BANNER_Y"),
        ("s7.banner", "TAX ADDS, DISCOUNT REMOVES", 18, "BANNER_Y"),
        ("s8.banner", "NEVER APPLY THE RATE TO THE BILL", 18, "BANNER_Y"),
        ("title.strip", "The price on the tag is not always the bill you pay.",
         16, "STRIP_Y"),
        ("s8.strip", "The rate is charged on the base, never on the total.",
         15, "STRIP_Y"),
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

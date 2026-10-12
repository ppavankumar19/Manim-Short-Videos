"""Create this topic's audit tooling from the Class 6 Chapter 4 set.

Those videos grew the audit tooling this series now uses (the strict
`audit_badge_clearance.py`, the -2.00 caption band and the fixed-column checks),
so the generic parts are copied verbatim and the topic-specific parts (module
name, class name, SRT path, narration anchors, heading list) are rewritten for
this video.

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

MODULE = "discounts_marked_price_and_rebate"
CLASS = "DiscountsMarkedPriceAndRebateStory"

PIECE_ORDER = (["title"] + [f"s{i}" for i in range(1, 9)]
               + ["s9q", "s9a", "s10"])
# The first few words of each piece, exactly as voiced: the audit re-synchronises
# every piece on these, so one mismatch cannot shift the pieces after it.
PIECE_ANCHORS = {
    "title": "look at this price tag",
    "s1": "the price tag has three",
    "s2": "a book is marked eighty",
    "s3": "now let us find a",
    "s4": "now the other direction the",
    "s5": "there is a shortcut and",
    "s6": "there are three questions you",
    "s7": "now the mistakes that cost",
    "s8": "before you write the answer",
    "s9q": "your turn",
    "s9a": "let us check",
    "s10": "the whole chapter in four",
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
        ("title", "Discounts, Marked Price & Rebate", 20, "ROW_Y"),
        ("title.sub", "The tag price is not always the price you pay.",
         17, "SUB_Y"),
        ("s1.head", "The Three Parts of a Price", 20, "ROW_Y"),
        ("s1.sub", "Marked price, discount, selling price.", 17, "SUB_Y"),
        ("s2.head", "The Discount Comes First", 20, "ROW_Y"),
        ("s2.sub", "A book marked Rs 80 at 15% off.", 17, "SUB_Y"),
        ("s3.head", "Finding the Discount Percent", 20, "ROW_Y"),
        ("s3.sub", "A cycle marked Rs 3600, sold for Rs 3312.", 17, "SUB_Y"),
        ("s4.head", "Given the Discount, Find the SP", 20, "ROW_Y"),
        ("s4.sub", "A fan marked Rs 1600 with 6% off.", 17, "SUB_Y"),
        ("s5.head", "The Shortcut: What Remains", 20, "ROW_Y"),
        ("s5.sub", "If 6% is taken off, 94% remains.", 17, "SUB_Y"),
        ("s6.head", "Which Formula Do I Need?", 20, "ROW_Y"),
        ("s6.sub", "Look at what the question gives you.", 17, "SUB_Y"),
        ("s7.head", "Common Mistakes and Their Fixes", 20, "ROW_Y"),
        ("s7.sub", "Four wrong ideas, four corrections.", 17, "SUB_Y"),
        ("s8.head", "Does the Answer Make Sense?", 20, "ROW_Y"),
        ("s8.sub", "Check the selling price against the marked price.",
         17, "SUB_Y"),
        ("s9.head", "YOUR TURN", 26, 2.78),
        ("s9.sub", "Four quick checks.", 16, 2.20),
        ("s10.head", "Marked Price to Selling Price", 22, "ROW_Y"),
        # banners and strips (bottom rows, measured for completeness)
        ("s6.banner", "THE BASE IS ALWAYS THE MARKED PRICE", 18, "BANNER_Y"),
        ("s1.strip", "The discount is always calculated from the marked "
                     "price.", 16, "STRIP_Y"),
        ("s2.strip", "The discount is always calculated on the marked price.",
         16, "STRIP_Y"),
        ("s3.strip", "Always divide by the marked price, and never by the "
                     "selling price.", 16, "STRIP_Y"),
        ("s4.strip", "The amount is in rupees; the rate is a percentage of "
                     "the marked price.", 16, "STRIP_Y"),
        ("s5.strip", "Both routes land on the same selling price, Rs 1504.",
         16, "STRIP_Y"),
        ("s7.strip", "Check the base, the sign, and the units, every time.",
         16, "STRIP_Y"),
        ("s8.strip", "Check SP < MP, and check that d plus (100 - d) makes "
                     "100.", 16, "STRIP_Y"),
        ("s9a.strip", "The base is the marked price, and SP is always smaller "
                      "than MP.", 16, "STRIP_Y"),
        ("s10.strip", "Keep the marked price visible, subtract the discount, "
                      "check the answer.", 16, "STRIP_Y"),
    )
    body = "ITEMS = (\n"
    for tag, text_, size, y in items:
        yv = y if y == "ROW_Y" or y == "SUB_Y" or y == "BANNER_Y" \
            or y == "STRIP_Y" else y
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

"""Create this topic's audit tooling from the Class 6 Chapter 4 set.

Those videos grew the audit tooling this series now uses (the strict
`audit_badge_clearance.py`, the -2.00 caption band and the fixed-column checks),
so the generic parts are copied verbatim and the topic-specific parts
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

MODULE = "profit_loss_overhead_expenses_and_transactions"
CLASS = "ProfitLossOverheadExpensesAndTransactionsStory"

PIECE_ORDER = (["title"] + [f"s{i}" for i in range(1, 9)]
               + ["s9q", "s9a", "s10"])
# The first words of each piece, exactly as voiced: the audit re-synchronises
# every piece on these, so one mismatch cannot shift the pieces after it.
PIECE_ANCHORS = {
    "title": "the purchase price is not",
    "s1": "first decide whether a deal",
    "s2": "now the percentage",
    "s3": "let us keep a proper",
    "s4": "here is the same idea",
    "s5": "now a trap",
    "s6": "now solve the whole transaction",
    "s7": "here is the decision process",
    "s8": "one more reminder",
    "s9q": "your turn",
    "s9a": "let us check",
    "s10": "let us put it together",
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

    # This topic's media path (275 characters) runs past the 260-character
    # MAX_PATH limit, so the rendered SRT is read through the extended-length
    # form when the operating system refuses the plain path.
    old = "lines = SRT.read_text(encoding=\"utf-8\").splitlines()"
    assert text.count(old) == 1, text.count(old)
    text = text.replace(old, "lines = _read_srt().splitlines()")
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


def parse_srt()'''
    assert text.count("def parse_srt()") == 1
    text = text.replace("def parse_srt()", helper, 1)
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
        ("title", "The Real Cost of a Purchase", 24, "ROW_Y"),
        ("title.sub", "A second-hand refrigerator.", 16, "SUB_Y"),
        ("s1.head", "Profit, Loss, or Neither?", 20, "ROW_Y"),
        ("s2.head", "The Percentage Is Taken on CP", 20, "ROW_Y"),
        ("s3.head", "The Refrigerator Ledger", 20, "ROW_Y"),
        ("s4.head", "Overheads Can Bring a Loss", 20, "ROW_Y"),
        ("s5.head", "Two Tables, Twenty Percent Each", 20, "ROW_Y"),
        ("s6.head", "The Whole Transaction", 20, "ROW_Y"),
        ("s7.head", "The Decision Process", 20, "ROW_Y"),
        ("s8.head", "Spoiled Stock Still Costs", 20, "ROW_Y"),
        ("s9.head", "YOUR TURN", 26, 2.78),
        ("s9.sub", "Two problems.", 16, 2.20),
        ("s10.head", "Purchase · Overheads · Percentage", 22, "ROW_Y"),
        # sub-headings (same line in every scene)
        ("s1.sub", "Ask which one is bigger before subtracting.", 17, "SUB_Y"),
        ("s2.sub", "Measured against the cost price.", 17, "SUB_Y"),
        ("s3.sub", "Add every expense to the purchase price.", 16, "SUB_Y"),
        ("s4.sub", "A flat bought and then repaired.", 16, "SUB_Y"),
        ("s5.sub", "Do a gain and a loss cancel?", 17, "SUB_Y"),
        ("s6.sub", "Add the two costs and the two selling prices.", 16, "SUB_Y"),
        ("s7.sub", "Five steps, every time.", 17, "SUB_Y"),
        ("s8.sub", "Overheads count even for what is not sold.", 16, "SUB_Y"),
        ("s10.sub", "The purchase price alone is never the cost.", 16, "SUB_Y"),
        # closing strips (bottom line, measured for completeness)
        ("s1.strip", "Always compare before you subtract.", 16, "STRIP_Y"),
        ("s3.strip", "The purchase price plus the overheads is the real cost.",
         15, "STRIP_Y"),
        ("s6.strip", "Plus twenty and minus twenty did not give zero.", 16,
         "STRIP_Y"),
        ("s9.strip", "The bases were different every time.", 16, "STRIP_Y"),
    )
    body = "ITEMS = (\n"
    for tag, text_, size, y in items:
        body += f'    ("{tag}", "{text_}", {size}, {y}),\n'
    body += ")\n\n"
    text = text[:i] + body + text[j:]
    (HERE / "audit_badge_clearance.py").write_text(text, encoding="utf-8")
    print("wrote audit_badge_clearance.py")


if __name__ == "__main__":
    copy_verbatim()
    write_audit()
    write_badge_audit()
    print(f"\nchapter pipeline: {CHAPTER / 'pipeline_360.py'}")

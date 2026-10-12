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

MODULE = "percentage_applications_and_estimation"
CLASS = "PercentageApplicationsAndEstimationStory"

PIECE_ORDER = (["title"] + [f"s{i}" for i in range(1, 9)]
               + ["s9q", "s9a", "s10"])
# The first few words of each piece, exactly as voiced: the audit re-synchronises
# every piece on these, so one mismatch cannot shift the pieces after it.
PIECE_ANCHORS = {
    "title": "suppose two school groups",
    "s1": "now let us convert both",
    "s2": "now think about a change",
    "s3": "let us apply that to",
    "s4": "now the other direction",
    "s5": "here is the mental toolkit",
    "s6": "now use that on a",
    "s7": "let us put the two",
    "s8": "so here is the decision",
    "s9q": "your turn four quick checks",
    "s9a": "let us check every answer",
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

    # This topic's SRT path is exactly 260 characters long, one over the limit a
    # plain open accepts while Windows' long-path support is off (measured:
    # LongPathsEnabled = 0), so reading it falls back to the `\\?\` form.
    reader = ('def _srt_text() -> str:\n'
              '    """Read the ground-truth SRT past Windows\' path limit."""\n'
              '    try:\n'
              '        return SRT.read_text(encoding="utf-8")\n'
              '    except OSError:\n'
              '        with open("\\\\\\\\?\\\\" + str(SRT.resolve()),\n'
              '                  encoding="utf-8") as handle:\n'
              '            return handle.read()\n\n\n'
              'def parse_srt() -> list[tuple[str, float]]:')
    assert text.count("def parse_srt() -> list[tuple[str, float]]:") == 1
    text = text.replace("def parse_srt() -> list[tuple[str, float]]:", reader)
    assert text.count('    lines = SRT.read_text(encoding="utf-8").splitlines()') == 1
    text = text.replace('    lines = SRT.read_text(encoding="utf-8").splitlines()',
                        '    lines = _srt_text().splitlines()')

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
        ("title", "Who Did Better?", 26, 1.98),
        ("title.sub", "225 of 300, or 200 of 250?", 17, 1.42),
        ("s1.head", "One Scale for Every Total", 20, "ROW_Y"),
        ("s2.head", "A 35% Increase Attaches a Block", 20, "ROW_Y"),
        ("s3.head", "Applying the 35% Increase", 20, "ROW_Y"),
        ("s4.head", "A 10% Decrease on a Price Tag", 20, "ROW_Y"),
        ("s5.head", "The Mental Percentage Toolkit", 20, "ROW_Y"),
        ("s6.head", "Estimating 15% on a Bill", 20, "ROW_Y"),
        ("s7.head", "Exact Lane and Estimate Lane", 20, "ROW_Y"),
        ("s8.head", "The Four-Move Decision Map", 20, "ROW_Y"),
        ("s9.head", "YOUR TURN", 26, 2.78),
        ("s9.sub", "Four quick checks.", 16, 2.20),
        ("s10.head", "Compare, Change, Estimate, Check", 18, "ROW_Y"),
        ("s1.sub", "Part over whole, times one hundred.", 17, "SUB_Y"),
        ("s2.sub", "The increase is measured from the original.", 17, "SUB_Y"),
        ("s3.sub", "Add the increase to the original figure.", 17, "SUB_Y"),
        ("s4.sub", "A decrease is taken away from one hundred.", 17, "SUB_Y"),
        ("s5.sub", "Ten percent first, then half, then add.", 17, "SUB_Y"),
        ("s6.sub", "Round the bill, then build fifteen percent.", 17, "SUB_Y"),
        ("s7.sub", "An estimate is a check, not exact arithmetic.", 17,
         "SUB_Y"),
        ("s8.sub", "Convert, change, estimate, check.", 17, "SUB_Y"),
        ("s10.sub", "Four rules to carry away.", 17, "SUB_Y"),
        # banners / strips (bottom rows, measured for completeness)
        ("title.banner", "ONE SCALE: OUT OF 100", 18, "BANNER_Y"),
        ("s1.banner", "GROUP B DID BETTER: 80% > 75%", 18, "BANNER_Y"),
        ("s2.banner", "A 35% INCREASE GIVES 135% OF THE ORIGINAL", 16,
         "BANNER_Y"),
        ("s3.banner", "NEW SALES = Rs 1,33,245", 18, "BANNER_Y"),
        ("s4.banner", "10% OFF -> YOU PAY 90%", 18, "BANNER_Y"),
        ("s5.banner", "5% IS HALF OF 10%, NOT OF 20%", 16, "BANNER_Y"),
        ("s6.banner", "ROUND THE BILL, THEN PAY ABOUT Rs 410", 16, "BANNER_Y"),
        ("s7.banner", "EXACT 406.13, ESTIMATE ABOUT 410", 16, "BANNER_Y"),
        ("s8.banner", "FOUR MOVES: CONVERT, INCREASE, DECREASE, ESTIMATE",
         16, "BANNER_Y"),
        ("s5.strip", "Build hard percentages out of ten percent.", 16,
         "STRIP_Y"),
        ("s10.strip", "Compare, change, estimate, then check.", 16, "STRIP_Y"),
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

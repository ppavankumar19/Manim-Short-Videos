"""Throwaway geometry probe: exact chalk-text widths for this video's layout.

    python _measure.py

Every row of cards is placed by `row_centres`, whose result depends on the real
ink width of each label, so this prints those widths (and the resulting board
spans) before a render is spent on a layout that is 0.02 units too wide.
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import config

config.renderer = "cairo"
config.disable_caching = True

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from sales_tax_vat_and_gst_calculations import (  # noqa: E402
    SalesTaxVatAndGstCalculationsStory, board_text,
)

BOARD_LEFT, BOARD_RIGHT, BOARD_CX = -4.6, 5.6, 0.5

STRINGS = [
    # scene headings / sub-headings
    (20, "A Tax Is a Percentage Increase"),
    (17, "The base price is the one hundred percent."),
    # title row
    (12, "BASE PRICE"), (10, "before tax"),
    (12, "TAX AMOUNT"), (10, "the percentage added"),
    (12, "FINAL BILL"), (10, "base plus tax"),
    (18, "BASE + TAX = THE FINAL BILL"),
    (16, "The price on the tag is not always the bill you pay."),
    # s1
    (13, "FINAL BILL = (100 + r) / 100 x BASE PRICE"),
    (13, "SAME AS A PERCENTAGE INCREASE"),
    (13, "6% GIVES 106%"), (13, "BASE PRICE = 100%"),
    (13, "106% = THE BILL"), (12, "6%"),
    # s2
    (13, "TAX 6% OF 450 = Rs 27"), (13, "BILL = Rs 477"),
    (13, "6/100 x 450 = Rs 27"), (13, "450 + 27 = Rs 477"),
    (13, "SHORTCUT: 106% OF 450 = 1.06 x 450 = Rs 477"),
    (14, "Rs 450"),
    # s3
    (13, "PRE-VAT = Rs 354.45"), (13, "+ VAT 5% = Rs 17.72"),
    (13, "BASE + VAT = THE BILL"), (13, "354.45 + 17.72 = Rs 372.18"),
    (12, "VAT = THE SAME PERCENTAGE IDEA"),
    (12, "HISTORICAL RATES, NOT TODAY'S TAX ADVICE"),
    (16, "BASE Rs 354.45 + VAT Rs 17.72 = Rs 372.18"),
    # s4
    (12, "GST: AN INDIRECT TAX ON GOODS AND SERVICES"),
    (13, "BASE = Rs 1,000 · GST = 5%"),
    (13, "TAX = 5/100 x 1,000 = Rs 50"),
    (13, "BILL = 1,000 + 50 = Rs 1,050"),
    (13, "SHORTCUT: 105% OF 1,000 = Rs 1,050"),
    # s5
    (13, "118% = THE BILL"), (13, "100% = BASE PRICE"), (11, "18%"),
    (13, "BILL INCL. 18% GST = Rs 2,360"), (13, "2,360 x 100/118"),
    (13, "BASE = Rs 2,000"), (13, "TAX = Rs 360"),
    (13, "BASE = BILL x 100 / (100 + r)"),
    (18, "BASE = Rs 2,000, TAX = Rs 360"),
    (16, "NEVER SUBTRACT THE RATE OFF THE BILL"),
    # s6
    (13, "GST = Rs 360"), (12, "CGST Rs 180"), (12, "SGST Rs 180"),
    (13, "THE TEXTBOOK HALVES IT"), (13, "360 / 2 = Rs 180 EACH"),
    (13, "180 + 180 = Rs 360"),
    (12, "THIS IS THE WORKED CASE, NOT EVERY BILL"),
    # s7
    (14, "BASE PRICE GIVEN"), (12, "tax = r% of the base"),
    (12, "bill = base + tax"), (14, "TAX-INCLUSIVE BILL GIVEN"),
    (12, "base = bill x 100 / (100 + r)"), (12, "the tax is bill - base"),
    (13, "THE LANE FOLLOWS WHAT YOU WERE GIVEN"),
    (13, "TAX ADDS TO THE BASE"), (13, "DISCOUNT TAKES OFF THE PRICE"),
    # s8
    (13, "BASE = Rs 1,000 · GST = 18%"),
    (13, "18% OF Rs 1,000 = Rs 180"), (13, "BILL = Rs 1,180"),
    (13, "18% OF Rs 1,180"), (13, "1180 - 18% = ?"),
    (12, "18% OF Rs 1,000 = Rs 180"),
    (12, "Rs 1,180 x 100/118 = Rs 1,000"),
    (13, "RATE GOES ON THE BASE"),
    # s9
    (13, "A: tax and bill"), (13, "B: base and tax"),
    (13, "C: CGST and SGST"), (13, "D: spot the error"),
    (14, "Rs 800 + 5% tax = ?"), (13, "Rs 1,180 incl. 18% = ?"),
    (13, "GST Rs 180, split equally?"),
    (12, "18% of Rs 1,180:"), (12, "right for Rs 1,000?"),
    (17, "base Rs 1,000, tax Rs 180"), (15, "1,180 x 100/118 = Rs 1,000"),
    (17, "No: 18% of Rs 1,180 is wrong"), (15, "the rate belongs on Rs 1,000"),
    (17, "tax Rs 40, bill Rs 840"), (15, "5% of Rs 800 = Rs 40"),
    (17, "CGST Rs 90, SGST Rs 90"), (15, "180 split equally: 90 + 90"),
    # s10
    (15, "tax = r / 100 x base price"),
    (15, "bill = base + tax = (100 + r)/100 x base"),
    (15, "base = bill x 100 / (100 + r)"),
    (15, "tax adds to the base; discount removes"),
    (15, "Start at 100%, add the tax, work backward with 100/(100 + r)."),
]


def row(half_widths, gap, cx=BOARD_CX):
    total = 2.0 * sum(half_widths) + gap * (len(half_widths) - 1)
    return cx - total / 2.0, cx + total / 2.0


def main() -> None:
    print(f"{'size':>4s} {'w':>5s} {'h':>5s}  text")
    for size, s in STRINGS:
        t = board_text(s, size, "#FFFFFF", "BOLD")
        print(f"{size:4d} {t.width:5.2f} {t.height:5.2f}  {s}")

    print("\n--- composed rows (chip width = text + 0.40) ---")
    rows = {
        "title.three_name_cards": ([(12, "BASE PRICE"), (12, "TAX AMOUNT"),
                                    (12, "FINAL BILL")], 3 * [2.40 / 2], 0.45),
        "s2.rowB": ([(13, "6/100 x 450 = Rs 27"),
                     (13, "450 + 27 = Rs 477")], None, 0.50),
        "s3.rowA": ([(13, "PRE-VAT = Rs 354.45"),
                     (13, "+ VAT 5% = Rs 17.72")], None, 0.78),
        "s3.rowB": ([(13, "BASE + VAT = THE BILL"),
                     (13, "354.45 + 17.72 = Rs 372.18")], None, 0.50),
        "s4.rowA": ([(12, "GST: AN INDIRECT TAX ON GOODS AND SERVICES")],
                    None, 0.0),
        "s5.rowB": ([(13, "BASE = Rs 2,000"), (13, "TAX = Rs 360")],
                    None, 0.50),
        "s6.rowB": ([(13, "360 / 2 = Rs 180 EACH"),
                     (13, "180 + 180 = Rs 360")], None, 0.50),
        "s7.rowB": ([(13, "TAX ADDS TO THE BASE"),
                     (13, "DISCOUNT TAKES OFF THE PRICE")], None, 0.50),
        "s8.rowC": ([(12, "18% OF Rs 1,000 = Rs 180"),
                     (12, "Rs 1,180 x 100/118 = Rs 1,000")], None, 0.45),
        "s10.recap2": ([(17, "2"), (17, "BILL"),
                        (15, "bill = base + tax = (100 + r)/100 x base")],
                       None, 0.36),
        "s10.recap4": ([(17, "4"), (17, "TAX, NOT DISCOUNT"),
                        (15, "tax adds to the base; discount removes")],
                       None, 0.36),
    }
    for name, (items, halves, gap) in rows.items():
        if halves is None:
            halves = [(board_text(s, size, "#FFFFFF", "BOLD").width + 0.40)
                      / 2.0 for size, s in items]
        x0, x1 = row(halves, gap)
        flag = "" if x0 > BOARD_LEFT + 0.12 and x1 < BOARD_RIGHT - 0.12 \
            else "   <<< OUT"
        print(f"{name:24s} span[{x0:+.2f}..{x1:+.2f}] w={x1 - x0:5.2f}{flag}")

    print("\n--- answer rows (box is 8.60 wide, row starts pad 0.34 in) ---")
    scene = SalesTaxVatAndGstCalculationsStory()
    answers = [
        ("A", "tax Rs 40, bill Rs 840", "5% of Rs 800 = Rs 40"),
        ("B", "base Rs 1,000, tax Rs 180", "1,180 x 100/118 = Rs 1,000"),
        ("C", "CGST Rs 90, SGST Rs 90", "180 split equally: 90 + 90"),
        ("D", "No: 18% of Rs 1,180 is wrong",
         "the rate belongs on Rs 1,000"),
        ("1", "TAX", "tax = r / 100 x base price"),
        ("2", "BILL", "bill = base + tax = (100 + r)/100 x base"),
        ("3", "REVERSE", "base = bill x 100 / (100 + r)"),
        ("4", "TAX OR DISCOUNT", "tax adds to the base; discount removes"),
        ("4b", "TAX, NOT DISCOUNT", "a discount removes; a tax adds to the base"),
    ]
    for tag, head, note in answers:
        r = scene.answer_row(tag, head, note, "#FFFFFF")
        inner = r[1]
        over = inner.width + 0.34 - r[0].width
        flag = "" if over <= 0 else f"   <<< OVER by {over:.2f}"
        print(f"{tag:3s} {inner.width:5.2f} box {r[0].width:4.2f} "
              f"over={over:+.2f}{flag}")

    print("\n--- q_cards and lane_cards ---")
    pics = [
        ("A: tax and bill", board_text("Rs 800 + 5% tax = ?", 14)),
        ("B: base and tax", board_text("Rs 1,180 incl. 18% = ?", 13)),
        ("C: CGST and SGST", board_text("GST Rs 180, split equally?", 13)),
        ("D: spot the error", board_text("right for Rs 1,000?", 12)),
    ]
    for title, pict in pics:
        c = scene.q_card(title, pict)
        print(f"{title:20s} {c.width:5.2f} x {c.height:5.2f}")
    for head, lines in [
        ("BASE PRICE GIVEN", ["tax = r% of the base", "bill = base + tax"]),
        ("TAX-INCLUSIVE BILL GIVEN",
         ["base = bill x 100 / (100 + r)", "the tax is bill - base"]),
    ]:
        c = scene_lane(head, lines)
        print(f"{head:24s} {c.width:5.2f} x {c.height:5.2f}")


def scene_lane(head, lines):
    from sales_tax_vat_and_gst_calculations import lane_card
    return lane_card(head, lines, "#FFFFFF", width=4.20, head_size=14,
                     line_size=12)


if __name__ == "__main__":
    main()

"""Summarise visual-vs-voice timing for the rendered videos.

Reads <topic>/media/videos/<module>/360p30/<Class>.sync.csv written by ch5_kit
(one row per reveal: when the voice reaches the bookmark vs when the picture is
shown) and reports lag statistics plus the audio/video duration match of the
captioned deliverable.
"""
import csv
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
JOBS = [
    ("Discounts-Marked-Price-and-Rebate", "discounts_marked_price_and_rebate",
     "DiscountsMarkedPriceAndRebateStory"),
    ("Percentage-Increases-Decreases-and-Estimation",
     "percentage_applications_and_estimation",
     "PercentageApplicationsAndEstimationStory"),
    ("Profit-Loss-Overhead-Expenses-and-Transactions",
     "profit_loss_overhead_expenses_and_transactions",
     "ProfitLossOverheadExpensesAndTransactionsStory"),
    ("Sales-Tax-VAT-and-GST-Calculations", "sales_tax_vat_and_gst_calculations",
     "SalesTaxVatAndGstCalculationsStory"),
    ("Simple-vs-Compound-Interest", "simple_vs_compound_interest_formula",
     "SimpleVsCompoundInterestFormulaStory"),
    ("Compound-Ratio-and-Business-Profit-Sharing",
     "compound_ratio_and_business_proportions",
     "CompoundRatioAndBusinessProportionsStory"),
    ("Compounding-Periods-Growth-and-Depreciation",
     "compounding_periods_half_yearly_quarterly_depreciation",
     "CompoundingPeriodsHalfYearlyQuarterlyDepreciationStory"),
]


def probe(path, stream):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", stream,
                        "-show_entries", "stream=duration", "-of",
                        "default=nw=1:nk=1", str(path)],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.split()[0])
    except Exception:
        return float("nan")


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else ""
    for topic, mod, cls in JOBS:
        if only and only not in mod:
            continue
        d = Path(r"D:\m3") / "videos" / mod / "360p30"
        csvp = HERE / topic / "media" / "videos" / mod / "360p30" / f"{cls}.sync.csv"
        if not csvp.exists():
            csvp = d / f"{cls}.sync.csv"
        mp4 = HERE / "final_videos" / f"{cls}_captioned.mp4"
        print(f"\n=== {cls}")
        if mp4.exists():
            v, a = probe(mp4, "v:0"), probe(mp4, "a:0")
            print(f"  video {v:.2f}s  audio {a:.2f}s  diff {abs(v - a):.2f}s")
        if not csvp.exists():
            print("  (no sync.csv)")
            continue
        rows = list(csv.DictReader(open(csvp, encoding="utf-8")))
        lags = [float(r["lag_s"]) for r in rows]
        late = [r for r in rows if float(r["lag_s"]) > 0.35]
        print(f"  {len(rows)} reveals: max lag {max(lags):.2f}s, "
              f"mean {sum(lags) / len(lags):.2f}s, {len(late)} later than 0.35s")
        for r in late[:10]:
            print(f"   LATE {r['beat']}/{r['mark']} +{float(r['lag_s']):.2f}s "
                  f"voice='...{r['voice_before']}' shows='{r['shown']}'")


if __name__ == "__main__":
    main()

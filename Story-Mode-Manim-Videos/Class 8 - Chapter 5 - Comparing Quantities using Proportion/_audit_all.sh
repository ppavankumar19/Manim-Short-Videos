#!/bin/bash
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE"
while read -r t m c; do
  python _inject_narration.py "$t" "$m" >/dev/null
  echo "== $t"
  ./_stills_all.sh "$t" "$m" "$c"
done <<'LIST'
Discounts-Marked-Price-and-Rebate discounts_marked_price_and_rebate DiscountsMarkedPriceAndRebateStory
Percentage-Increases-Decreases-and-Estimation percentage_applications_and_estimation PercentageApplicationsAndEstimationStory
Profit-Loss-Overhead-Expenses-and-Transactions profit_loss_overhead_expenses_and_transactions ProfitLossOverheadExpensesAndTransactionsStory
Sales-Tax-VAT-and-GST-Calculations sales_tax_vat_and_gst_calculations SalesTaxVatAndGstCalculationsStory
Simple-vs-Compound-Interest simple_vs_compound_interest_formula SimpleVsCompoundInterestFormulaStory
Compound-Ratio-and-Business-Profit-Sharing compound_ratio_and_business_proportions CompoundRatioAndBusinessProportionsStory
Compounding-Periods-Growth-and-Depreciation compounding_periods_half_yearly_quarterly_depreciation CompoundingPeriodsHalfYearlyQuarterlyDepreciationStory
LIST
echo ALLDONE

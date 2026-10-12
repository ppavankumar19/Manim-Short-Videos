# Rebuild every Chapter 4 story module from its beats/fragment and re-run the
# draft sync/overlap audit.  Usage:
#     pwsh -File _rebuild_ch4.ps1 [-SkipTts]
param([switch]$SkipTts)

$ErrorActionPreference = "Continue"
$env:PYTHONIOENCODING = "utf-8"
$py = "D:\Manim-Short-Videos\.venv\Scripts\python.exe"
$base = "D:\Manim-Short-Videos\Story-Mode-Manim-Videos\Class 8 - Chapter 4 - Exponents and Powers"

$topics = @(
  @{ dir = "Introduction-to-Exponents-and-Powers";            asm = "assemble_exponents.py";      mod = "exponents_and_base_concept_introduction";           cls = "ExponentsAndBaseConceptStory" },
  @{ dir = "Negative-Exponents-and-Multiplicative-Inverses";  asm = "assemble_negative.py";       mod = "negative_exponents_and_multiplicative_inverse";      cls = "NegativeExponentsInverseStory" },
  @{ dir = "Product-and-Quotient-Laws-of-Exponents";          asm = "assemble_laws.py";           mod = "laws_of_exponents_product_and_quotient";             cls = "ProductQuotientLawsStory" },
  @{ dir = "Advanced-Laws-of-Exponents";                      asm = "assemble_advanced_laws.py";  mod = "laws_of_exponents_power_product_quotient_zero";      cls = "AdvancedExponentLawsStory" },
  @{ dir = "Standard-Form-with-Powers-of-10";                 asm = "assemble_standard_form.py";  mod = "scientific_notation_large_and_small_numbers";        cls = "StandardFormStory" }
)

foreach ($t in $topics) {
  Write-Output "=== $($t.dir)"
  Push-Location (Join-Path $base $t.dir)
  & $py $t.asm 2>&1 | Select-String -Pattern "wrote|Traceback|Error|error" | ForEach-Object { "   $_" }
  & $py setup_tools.py 2>&1 | Select-String -Pattern "wrote audit|Traceback|Error" | ForEach-Object { "   $_" }
  & $py make_draft_srt.py 2>&1 | Select-String -Pattern "draft cues|Traceback|Error" | ForEach-Object { "   $_" }
  if (-not $SkipTts) {
    & $py tts_precheck.py $t.mod s9q s9a s10 2>&1 |
      Select-String -Pattern "^!!|^ok |ALL OK|PROBLEMS|Traceback" |
      ForEach-Object { "   $_" }
  }
  & $py audit_sync_overlap.py > audit_draft.txt 2>&1
  Select-String -LiteralPath audit_draft.txt -Pattern "^TOTAL|^s9q |^s9a |^s10 " |
    ForEach-Object { "   " + $_.Line }
  $flags = Select-String -LiteralPath audit_draft.txt -Pattern "IN-CAPTION|TEXT-IN-TEXT|PARTIAL|TEXT-ON|OUT-OF-BOARD|NEAR-BADGE" |
    Measure-Object | Select-Object -ExpandProperty Count
  Write-Output "   flags: $flags (0 = only OFF-CENTRE)"
  Pop-Location
}
Write-Output "DONE"

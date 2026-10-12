# Render + verify + burn captions for all five Chapter 4 story videos.
# Usage: & "D:\Manim-Short-Videos\_render_ch4.ps1"
$env:PYTHONIOENCODING = "utf-8"
$py = "D:\Manim-Short-Videos\.venv\Scripts\python.exe"
$chapter = "D:\Manim-Short-Videos\Story-Mode-Manim-Videos\Class 8 - Chapter 4 - Exponents and Powers"

$topics = @(
  @{ dir = "Introduction-to-Exponents-and-Powers";           mod = "exponents_and_base_concept_introduction.py";      cls = "ExponentsAndBaseConceptStory" },
  @{ dir = "Negative-Exponents-and-Multiplicative-Inverses"; mod = "negative_exponents_and_multiplicative_inverse.py"; cls = "NegativeExponentsInverseStory" },
  @{ dir = "Product-and-Quotient-Laws-of-Exponents";         mod = "laws_of_exponents_product_and_quotient.py";        cls = "ProductQuotientLawsStory" },
  @{ dir = "Advanced-Laws-of-Exponents";                     mod = "laws_of_exponents_power_product_quotient_zero.py"; cls = "AdvancedExponentLawsStory" },
  @{ dir = "Standard-Form-with-Powers-of-10";                mod = "scientific_notation_large_and_small_numbers.py";   cls = "StandardFormStory" }
)

foreach ($t in $topics) {
  Write-Output "=== $($t.dir)"
  Push-Location $chapter
  & $py pipeline_360.py $t.dir $t.mod $t.cls 2>&1 |
    Select-String -Pattern "RESULT|MISSING|Traceback|Error|error:|FAIL|WARN|OUT OF SYNC|gap|MISMATCH" |
    ForEach-Object { "   $_" }
  Pop-Location
}
Write-Output "RENDERS DONE"

# Render + verify + burn captions for the five Chapter 4 masters at 1080p60.
# Output: "Class 8 - Chapter 4 - Exponents and Powers\final_videos\1080p\".
# Usage: & "D:\Manim-Short-Videos\_render1080_ch4.ps1"
$env:PYTHONIOENCODING = "utf-8"
$py = "D:\Manim-Short-Videos\.venv\Scripts\python.exe"
$chapter = "D:\Manim-Short-Videos\Story-Mode-Manim-Videos\Class 8 - Chapter 4 - Exponents and Powers"

$topics = @(
  @{ dir = "Introduction-to-Exponents-and-Powers";           mod = "exponents_and_base_concept_introduction.py";       cls = "ExponentsAndBaseConceptStory" },
  @{ dir = "Negative-Exponents-and-Multiplicative-Inverses"; mod = "negative_exponents_and_multiplicative_inverse.py"; cls = "NegativeExponentsInverseStory" },
  @{ dir = "Product-and-Quotient-Laws-of-Exponents";         mod = "laws_of_exponents_product_and_quotient.py";        cls = "ProductQuotientLawsStory" },
  @{ dir = "Advanced-Laws-of-Exponents";                     mod = "laws_of_exponents_power_product_quotient_zero.py"; cls = "AdvancedExponentLawsStory" },
  @{ dir = "Standard-Form-with-Powers-of-10";                mod = "scientific_notation_large_and_small_numbers.py";   cls = "StandardFormStory" }
)

foreach ($t in $topics) {
  Write-Output "=== 1080p $($t.dir)  $(Get-Date -Format 'HH:mm:ss')"
  Push-Location $chapter
  & $py pipeline_1080.py $t.dir $t.mod $t.cls 2>&1 |
    Select-String -Pattern "RESULT|MISSING|Traceback|KeyError|Error|error:|silent tail|captions:|mostly in silence|not captioned|final_videos" |
    ForEach-Object { "   $_" }
  Pop-Location
}
Write-Output "1080 RENDERS DONE  $(Get-Date -Format 'HH:mm:ss')"

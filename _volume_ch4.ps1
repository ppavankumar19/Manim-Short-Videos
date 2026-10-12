# Objective silence measurements on the delivered 360p cuts:
#   * mean/max volume inside the THINK clock window  (must be near-silent)
#   * the same for a narration window just before it (the reference level)
#   * mean/max volume over the last 3 s              (the silent closing card)
$env:PYTHONIOENCODING = "utf-8"
$py = "D:\Manim-Short-Videos\.venv\Scripts\python.exe"
$chapter = "D:\Manim-Short-Videos\Story-Mode-Manim-Videos\Class 8 - Chapter 4 - Exponents and Powers"

$topics = @(
  @{ dir = "Introduction-to-Exponents-and-Powers";           stem = "exponents_and_base_concept_introduction";      cls = "ExponentsAndBaseConceptStory";  mid = 183; dur = 225.12 },
  @{ dir = "Negative-Exponents-and-Multiplicative-Inverses"; stem = "negative_exponents_and_multiplicative_inverse"; cls = "NegativeExponentsInverseStory"; mid = 189; dur = 234.59 },
  @{ dir = "Product-and-Quotient-Laws-of-Exponents";         stem = "laws_of_exponents_product_and_quotient";        cls = "ProductQuotientLawsStory";      mid = 219; dur = 264.82 },
  @{ dir = "Advanced-Laws-of-Exponents";                     stem = "laws_of_exponents_power_product_quotient_zero"; cls = "AdvancedExponentLawsStory";     mid = 233; dur = 285.16 },
  @{ dir = "Standard-Form-with-Powers-of-10";                stem = "scientific_notation_large_and_small_numbers";   cls = "StandardFormStory";             mid = 238; dur = 292.69 }
)

foreach ($t in $topics) {
  Write-Output "=== $($t.dir)"
  Push-Location "$chapter\$($t.dir)\media\videos\$($t.stem)\360p30"
  $file = "$($t.cls).mp4"
  $a = $t.mid - 3
  Write-Output "   clock window      [${a}s +6s]"
  & ffmpeg -hide_banner -ss $a -t 6 -i $file -af volumedetect -f null - 2>&1 |
    Select-String -Pattern "mean_volume|max_volume" | ForEach-Object { "      " + $_.Line.Trim() }
  $n = $t.mid - 40
  Write-Output "   narration ref     [${n}s +6s]"
  & ffmpeg -hide_banner -ss $n -t 6 -i $file -af volumedetect -f null - 2>&1 |
    Select-String -Pattern "mean_volume|max_volume" | ForEach-Object { "      " + $_.Line.Trim() }
  $tail = [Math]::Round($t.dur - 3.0, 2)
  Write-Output "   closing card      [${tail}s +3s]"
  & ffmpeg -hide_banner -ss $tail -i $file -af volumedetect -f null - 2>&1 |
    Select-String -Pattern "mean_volume|max_volume" | ForEach-Object { "      " + $_.Line.Trim() }
  Pop-Location
}
Write-Output "VOLUME CHECK DONE"

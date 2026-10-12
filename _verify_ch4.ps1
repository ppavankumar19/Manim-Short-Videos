# Post-render verification for the five Chapter 4 story videos:
#   verify_sync + verify_captions, the real-audio overlap audit, the clearance
#   audit, ffprobe duration, the silent THINK clock window and its volume, the
#   volume of the silent closing card, and sync_report's gap table.
# Usage: & "D:\Manim-Short-Videos\_verify_ch4.ps1" [-Only <topic-dir>]
param([string]$Only = "")

$env:PYTHONIOENCODING = "utf-8"
$py = "D:\Manim-Short-Videos\.venv\Scripts\python.exe"
$root = "D:\Manim-Short-Videos"
$chapter = "$root\Story-Mode-Manim-Videos\Class 8 - Chapter 4 - Exponents and Powers"

$topics = @(
  @{ dir = "Introduction-to-Exponents-and-Powers";           mod = "exponents_and_base_concept_introduction.py";      cls = "ExponentsAndBaseConceptStory";  stem = "exponents_and_base_concept_introduction" },
  @{ dir = "Negative-Exponents-and-Multiplicative-Inverses"; mod = "negative_exponents_and_multiplicative_inverse.py"; cls = "NegativeExponentsInverseStory"; stem = "negative_exponents_and_multiplicative_inverse" },
  @{ dir = "Product-and-Quotient-Laws-of-Exponents";         mod = "laws_of_exponents_product_and_quotient.py";        cls = "ProductQuotientLawsStory";      stem = "laws_of_exponents_product_and_quotient" },
  @{ dir = "Advanced-Laws-of-Exponents";                     mod = "laws_of_exponents_power_product_quotient_zero.py"; cls = "AdvancedExponentLawsStory";     stem = "laws_of_exponents_power_product_quotient_zero" },
  @{ dir = "Standard-Form-with-Powers-of-10";                mod = "scientific_notation_large_and_small_numbers.py";   cls = "StandardFormStory";             stem = "scientific_notation_large_and_small_numbers" }
)

foreach ($t in $topics) {
  if ($Only -and $t.dir -ne $Only) { continue }
  Write-Output "=== $($t.dir)"
  $topic = Join-Path $chapter $t.dir
  $mediadir = Join-Path $topic "media\videos\$($t.stem)\360p30"
  $vid = Join-Path $mediadir "$($t.cls).mp4"
  $srt = Join-Path $mediadir "$($t.cls).real.srt"
  $cap = Join-Path $mediadir "$($t.cls)_captioned.mp4"
  $fin = Join-Path $chapter "final_videos\$($t.cls)_captioned.mp4"
  if (-not (Test-Path -LiteralPath $vid)) { Write-Output "   MISSING $vid"; continue }

  Push-Location $topic

  & $py "$root\verify_sync.py" $vid $srt 2>&1 |
    Select-String -Pattern "video |captions:|mostly in silence|not captioned|RESULT" |
    ForEach-Object { "   " + $_.Line.Trim() }

  & $py audit_sync_overlap.py > audit_real.txt 2>&1
  Select-String -LiteralPath audit_real.txt -Pattern "^TOTAL|^s9q |^s9a |^s10 " |
    ForEach-Object { "   " + $_.Line }
  $flags = (Select-String -LiteralPath audit_real.txt -Pattern "IN-CAPTION|TEXT-IN-TEXT|PARTIAL|TEXT-ON|OUT-OF-BOARD|NEAR-BADGE" |
    Measure-Object).Count
  Write-Output "   audit flags (0 = clean, OFF-CENTRE notes only): $flags"

  & $py audit_clearance.py $t.dir $t.mod $t.cls 0.22 > clearance_real.txt 2>&1
  Select-String -LiteralPath clearance_real.txt -Pattern "closer than|ON-LINE|FOREIGN|GLYPH|clean|pairs" |
    Select-Object -First 5 | ForEach-Object { "   " + $_.Line.Trim() }

  $dur = [double](& ffprobe -v error -show_entries format=duration -of csv=p=0 $vid)
  Write-Output ("   duration: {0:N2} s  ({1:N0}m {2:N0}s)" -f $dur, [Math]::Floor($dur / 60), ($dur % 60))

  # the silent THINK clock: its window, and how quiet it is
  $dark = (& $py "$topic\find_timer.py" $vid) | Select-String -Pattern "countdown"
  foreach ($d in $dark) { "   " + $d.Line.Trim() }
  $mid = 0
  if ($dark) {
    $m = [regex]::Match($dark[0].Line, "mid=(\d+)s")
    if ($m.Success) { $mid = [int]$m.Groups[1].Value }
  }
  if ($mid -gt 0) {
    $a = [Math]::Max(0, $mid - 3)
    $vol = & ffmpeg -v error -ss $a -t 6 -i $vid -af volumedetect -f null - 2>&1 |
      Select-String -Pattern "mean_volume|max_volume"
    foreach ($v in $vol) { "   clock window [${a}s..$($a+6)s] " + $v.Line.Trim() }
  }

  # the silent closing card: the last 3 s must carry no narration
  $tail = [Math]::Max(0, $dur - 3.0)
  $vol2 = & ffmpeg -v error -ss $tail -i $vid -af volumedetect -f null - 2>&1 |
    Select-String -Pattern "mean_volume|max_volume"
  foreach ($v in $vol2) { "   closing card [last 3 s] " + $v.Line.Trim() }

  & $py "$chapter\sync_report.py" $vid $srt 2>&1 |
    Select-String -Pattern "silent gaps|captions inside|caption start minus|more than 1.2s|captions:" |
    ForEach-Object { "   " + $_.Line.Trim() }

  if (Test-Path -LiteralPath $fin) {
    Write-Output ("   final: {0}  {1:N1} MB" -f (Split-Path $fin -Leaf),
                  ((Get-Item -LiteralPath $fin).Length / 1MB))
  } else { Write-Output "   MISSING FINAL $fin" }
  if (Test-Path -LiteralPath $cap) { } # captioned copy sits beside the render
  Pop-Location
}
Write-Output "VERIFY DONE"

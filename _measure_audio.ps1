# Print the max volume of each 1 s window of a video's audio track.
# Usage: & _measure_audio.ps1 <video> [start] [end]
param([string]$File, [double]$Start = 0, [double]$End = -1)
if ($End -lt 0) {
  $End = [int][double](& ffprobe -v error -show_entries format=duration -of csv=p=0 $File)
}
$t = $Start
while ($t -lt $End) {
  $v = (& ffmpeg -hide_banner -ss $t -t 1 -i $File -af volumedetect -f null - 2>&1 |
        Select-String "max_volume") -join ""
  "{0,7:N1}  {1}" -f $t, ($v -replace '.*\] ', '')
  $t += 1
}

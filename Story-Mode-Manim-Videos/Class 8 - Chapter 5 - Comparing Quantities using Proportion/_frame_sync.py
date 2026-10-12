"""Frame-level check: at each reveal's bookmark time the rendered picture must change."""
import csv, subprocess, sys
import numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _sync_check import JOBS, HERE
FPS = 15
for topic, mod, cls in JOBS[:6]:
    csvp = HERE/topic/"media"/"videos"/mod/"360p30"/f"{cls}.sync.csv"
    if not csvp.exists():
        csvp = Path(r"D:\m3")/"videos"/mod/"360p30"/f"{cls}.sync.csv"
    mp4 = HERE/"final_videos"/f"{cls}_captioned.mp4"
    rows = list(csv.DictReader(open(csvp, encoding="utf-8")))
    raw = subprocess.run(["ffmpeg","-v","error","-i",str(mp4),"-vf",
        f"fps={FPS},crop=440:224:100:20,format=gray","-f","rawvideo","-"],
        capture_output=True).stdout          # board area only, no captions
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 224, 440).astype(np.int16)
    d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))   # change per frame
    bad = []
    for r in rows:
        t = float(r["bookmark_s"]); k = int(round(t * FPS))
        win = d[max(k - 2, 0):k + 9]                     # -0.13s .. +0.6s
        if win.max() < 0.25:
            bad.append((r["beat"], r["mark"], round(t, 1), r["shown"][:30]))
        # where is the peak of change?
    print(f"{cls}: {len(rows)} reveals, {len(bad)} with NO visible change near the bookmark", bad[:6])

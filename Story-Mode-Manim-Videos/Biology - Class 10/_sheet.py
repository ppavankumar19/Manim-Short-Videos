"""Tile stills at the real 640x360 delivery size: python _sheet.py <dir> <out.png> [cols] [glob]"""
import sys, glob
from pathlib import Path
from PIL import Image
d, out = sys.argv[1], sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 2
pat = sys.argv[4] if len(sys.argv) > 4 else "*.png"
files = sorted(glob.glob(str(Path(d) / pat)))
W, H = 800, 450
rows = (len(files) + cols - 1) // cols
sheet = Image.new("RGB", (W * cols, H * rows), "black")
for i, f in enumerate(files):
    im = Image.open(f).convert("RGB").resize((W, H), Image.LANCZOS)
    sheet.paste(im, ((i % cols) * W, (i // cols) * H))
sheet.save(out)
print(len(files), "->", out, sheet.size)

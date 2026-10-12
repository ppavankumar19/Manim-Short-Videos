"""Measure the pieces the revised rows are built from, so the placement maths
uses real widths instead of guesses.

    python _plr_metrics_tmp.py
"""
from __future__ import annotations

import sys

from manim import config

config.renderer = "cairo"
config.disable_caching = True

sys.path.insert(0, ".")
from fundamental_geometric_building_blocks_point_line_ray import (  # noqa: E402
    BOARD_CX, CHALK_CYAN, CHALK_WHITE, board_text, object_icon, row_centres,
    torch_icon,
)

print(f"\nboard axis BOARD_CX = {BOARD_CX}")
print("\n=== everyday icons ===")
for kind in ("book", "screen", "rangoli", "star"):
    icon = object_icon(kind)
    print(f"  {kind:8s} w={icon.width:5.2f} h={icon.height:5.2f} "
          f"half={icon.width / 2:5.2f}")
print("\n=== icon names ===")
names = {}
for name in ("book", "screen", "rangoli", "star"):
    t = board_text(name, 15, CHALK_CYAN, "BOLD")
    names[name] = t.width
    print(f"  {name:8s} w={t.width:5.2f}")
half = [max(object_icon(k).width / 2, names[k] / 2)
        for k in ("book", "screen", "rangoli", "star")]
print(f"  footprints half={[round(h, 2) for h in half]}")
print(f"  equal-gap 0.75 centres: "
      f"{[round(x, 2) for x in row_centres(half, 0.75)]}")
print(f"  equal-centre 2.30 centres: "
      f"{[round(BOARD_CX - 3.45 + i * 2.30, 2) for i in range(4)]}")

print("\n=== lower row of the same frame ===")
for label, kind in (("a point", "point"), ("a straight piece", "segment"),
                    ("an arrowed path", "ray")):
    t = board_text(label, 15, CHALK_WHITE, "BOLD")
    print(f"  {label:18s} text w={t.width:5.2f}  (pictogram ink 1.80)")

print("\n=== torch ===")
torch = torch_icon()
print(f"  w={torch.width:5.2f} h={torch.height:5.2f} "
      f"lens={torch.lens.get_center()[:2]} bbox={torch.get_left()[0]:.2f}"
      f"..{torch.get_right()[0]:.2f}")

print("\n=== s10 per-column rule entries (size 13) ===")
rules = ("POINT = LOCATION", "SEGMENT = 2", "RAY = 1", "LINE = 0")
for r in rules:
    print(f"  {r:18s} w={board_text(r, 13, CHALK_WHITE, 'BOLD').width:5.2f}")

print("\n=== s10 / title labels and notes ===")
for s, size in (("POINT", 16), ("SEGMENT", 16), ("RAY", 16), ("LINE", 16),
                ("marks a location", 14), ("2 endpoints", 14),
                ("1 endpoint", 14), ("0 endpoints", 14),
                ("POINT", 14), ("SEGMENT", 14), ("RAY", 14), ("LINE", 14)):
    print(f"  {s:18s} size={size:2d} w={board_text(s, size, CHALK_WHITE, 'BOLD').width:5.2f}")

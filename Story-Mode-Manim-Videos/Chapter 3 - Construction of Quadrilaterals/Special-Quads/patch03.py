"""Patch 03: the last two audit hits, one of which is a real error.

  scene 2  the angle at T was drawn between T E and T B -- T E is the diagonal,
           not a side, so the arc showed about 20 degrees instead of the given
           45.  The correct arms at T are T L and T B.
  scene 3  the 135 degree label at B sat on the 4.2 cm label.
"""
from pathlib import Path

P = Path(__file__).resolve().parent / "_specialq_beats.py"
s = P.read_text(encoding="utf-8")
n0 = len(s)
reps = []

reps.append((
    """            ang_t = angle_mark(T, E, B, radius=0.46, color=CHALK_YELLOW,
                               label=None)
            ang_t_lab = board_text("45°", 15, CHALK_YELLOW, "BOLD").move_to(
                np.array(T, dtype=float) + 1.05 * unit(
                    (dir_deg(T, E) + dir_deg(T, B)) / 2.0))""",
    """            # the angle at T is between the sides T L and T B -- T E is the
            # diagonal and does not bound it
            ang_t = angle_mark(T, L, B, radius=0.46, color=CHALK_YELLOW,
                               label=None)
            ang_t_lab = board_text("45°", 15, CHALK_YELLOW, "BOLD").move_to(
                np.array(T, dtype=float) + 1.05 * unit(
                    (dir_deg(T, L) + dir_deg(T, B)) / 2.0))"""))

reps.append((
    """            lab_b = board_text("135°", 15, CHALK_PINK, "BOLD").move_to(
                np.array(B, dtype=float) + 1.10 * unit(-20.0))""",
    """            lab_b = board_text("135°", 15, CHALK_PINK, "BOLD").move_to(
                np.array(B, dtype=float) + 1.30 * unit(-35.0))"""))

for old, new in reps:
    assert old in s, f"not found: {old[:70]!r}"
    s = s.replace(old, new, 1)

P.write_text(s, encoding="utf-8")
print(f"beats: {n0} -> {len(s)} chars, {len(reps)} replacements")

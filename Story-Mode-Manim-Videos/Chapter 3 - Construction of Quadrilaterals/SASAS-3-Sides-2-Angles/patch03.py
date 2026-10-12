"""Patch 03: the last two audit hits.

  scene 6  the swinging arm's arc (radius 0.86) passed exactly through the
           75 degree label: the arc is drawn smaller (0.60) so the label sits
           outside it
  scene 7  the 75 degree label still had its old position (the previous patch
           replaced only the first of the two identical snippets)
"""
from pathlib import Path

P = Path(__file__).resolve().parent / "_sasas_beats.py"
s = P.read_text(encoding="utf-8")
n0 = len(s)
reps = []

reps.append((
    """            self.setout_arm(C, d["cb_deg"], d["cd_deg"], dist(C, D) * 0.55,
                            0.86, CHALK_PINK)""",
    """            self.setout_arm(C, d["cb_deg"], d["cd_deg"], dist(C, D) * 0.55,
                            0.60, CHALK_PINK)"""))

old = """            ang_c = board_text("75°", 15, CHALK_PINK, "BOLD").move_to(
                np.array(C, dtype=float) + 1.30 * unit(
                    (d["cb_deg"] + d["cd_deg"]) / 2.0))"""
new = """            # inside the angle but clear of the A C edge, which lies in the
            # same wedge
            ang_c = board_text("75°", 15, CHALK_PINK, "BOLD").move_to(
                np.array(C, dtype=float) + 0.85 * unit(
                    d["cb_deg"] + (d["cd_deg"] - d["cb_deg"]) / 3.0))"""
assert s.count(old) == 1, f"found {s.count(old)}"
reps.append((old, new))

for old_s, new_s in reps:
    assert old_s in s, f"not found: {old_s[:70]!r}"
    s = s.replace(old_s, new_s, 1)

P.write_text(s, encoding="utf-8")
print(f"beats: {n0} -> {len(s)} chars, {len(reps)} replacements")

"""Patch 02 of the S.A.S.A.S beats: the remaining audit hits.

  scene 6/7 the 75 degree label sat on the tinted triangle's A C edge -- the
            edge runs inside the angle's wedge, so the label moves to the free
            part of the wedge (between C B and C A)
  scene 8   same label problem with the automatic `angle_mark` label, plus the
            step cards' inner text reached back over the B C side, and the C
            letter had kept its old slot (the earlier patch only replaced the
            first of the two identical letter blocks)
"""
from pathlib import Path

P = Path(__file__).resolve().parent / "_sasas_beats.py"
s = P.read_text(encoding="utf-8")
n0 = len(s)
reps = []

# --- scene 6 and 7: place the 75 label in the free part of the wedge --------
reps.append((
    """            ang_c = board_text("75°", 15, CHALK_PINK, "BOLD").move_to(
                np.array(C, dtype=float) + 1.30 * unit(
                    (d["cb_deg"] + d["cd_deg"]) / 2.0))""",
    """            # inside the angle but clear of the A C edge, which lies in the
            # same wedge
            ang_c = board_text("75°", 15, CHALK_PINK, "BOLD").move_to(
                np.array(C, dtype=float) + 0.85 * unit(
                    d["cb_deg"] + (d["cd_deg"] - d["cb_deg"]) / 3.0))"""))

# --- scene 8: the C letter, the 75 label, the step column ------------------
reps.append((
    """                (A, B, C, D), ((-0.28, -0.10), (0.14, -0.30), (0.30, 0.02),
                               (-0.10, 0.30)))
            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=4.0)""",
    """                (A, B, C, D), ((-0.28, -0.10), (0.14, -0.30), (-0.26, 0.37),
                               (-0.10, 0.30)))
            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=4.0)"""))
reps.append((
    """            ang_c = angle_mark(C, B, D, radius=0.80, color=CHALK_PINK,
                               label="75°")""",
    """            ang_c = angle_mark(C, B, D, radius=0.80, color=CHALK_PINK,
                               label=None)
            ang_c_lab = board_text("75°", 15, CHALK_PINK, "BOLD").move_to(
                np.array(C, dtype=float) + 0.85 * unit(
                    d["cb_deg"] + (d["cd_deg"] - d["cb_deg"]) / 3.0))"""))
reps.append((
    """            self.play(FadeIn(ang_b), FadeIn(ang_c), run_time=min(
                leftover(tracker, "b0"), 0.6))""",
    """            self.play(FadeIn(ang_b), FadeIn(ang_c), FadeIn(ang_c_lab),
                      run_time=min(leftover(tracker, "b0"), 0.6))"""))
reps.append((
    """            self.play(FadeOut(checks), FadeOut(ac), FadeOut(ang_b),
                      FadeOut(ang_c), FadeOut(never), run_time=0.5)""",
    """            self.play(FadeOut(checks), FadeOut(ac), FadeOut(ang_b),
                      FadeOut(ang_c), FadeOut(ang_c_lab), FadeOut(never),
                      run_time=0.5)"""))
reps.append((
    """            ).arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to(
                np.array([2.55, 0.55, 0]))""",
    """            ).arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to(
                np.array([2.85, 0.55, 0]))"""))

for old, new in reps:
    assert old in s, f"not found: {old[:70]!r}"
    s = s.replace(old, new, 1)

P.write_text(s, encoding="utf-8")
print(f"beats: {n0} -> {len(s)} chars, {len(reps)} replacements")

"""Patch 01 of the S.A.S.A.S beats, from the first audit pass.

  scene 1   the chain's acronym strip was drawn *after* the last window had
            already run out, so the scene overran its narration by 0.8 s
  scene 2   the boxed "Included = ..." line sat on the C letter: it moves into
            the right-hand column
  scene 5   the C letter sat on the compass arc that fixes C, and the "4.5 cm"
            label ran into the column note: the letter moves radially clear and
            the label moves inside the triangle
  scene 6/7 the dashed A C ran through the 75 degree label (and is not needed
            once the triangle has been shown): it is dropped
  scene 9   the five cards ran into the exercise tag
  scene 10  the 75 degree label sat on the tinted triangle's A C edge
"""
from pathlib import Path

P = Path(__file__).resolve().parent / "_sasas_beats.py"
s = P.read_text(encoding="utf-8")
n0 = len(s)
reps = []

# --- scene 1: draw the strip inside the last window ------------------------
reps.append((
    """            self.play(FadeIn(row[4][1]), FadeIn(sas[4]), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b6"))

            self.play(FadeIn(strip, shift=UP * 0.1), Create(box),
                      FadeIn(spell), run_time=0.7)
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.wait(leftover(tracker, "b6"))""",
    """            self.play(FadeIn(row[4][1]), FadeIn(sas[4]), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(strip, shift=UP * 0.1), Create(box),
                      FadeIn(spell), run_time=0.7)
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.wait(leftover(tracker, "b6"))"""))

# --- scene 2: the boxed line goes into the column --------------------------
reps.append((
    """            included = board_text("Included = between two given sides", 17,
                                  CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, 2.22, 0]))""",
    """            included = board_text("Included = between\\ntwo given sides", 16,
                                  CHALK_GREEN, "BOLD").move_to(
                np.array([3.05, -1.25, 0]))"""))

# --- the C letter: radially clear of the arc that fixes C -------------------
for old, new in ((
    """            names = self.vertex_letters(
                (A, B, C), ((-0.28, -0.10), (0.14, -0.30), (0.30, 0.02)))
            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=4.2)""",
    """            names = self.vertex_letters(
                (A, B, C), ((-0.28, -0.10), (0.14, -0.30), (-0.26, 0.37)))
            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=4.2)"""),):
    assert s.count(old) == 3, f"C-letter block found {s.count(old)} times"
    s = s.replace(old, new)
reps.append((
    """                (A, B, C, D), ((-0.28, -0.10), (0.14, -0.30), (0.30, 0.02),
                               (-0.10, 0.30)))""",
    """                (A, B, C, D), ((-0.28, -0.10), (0.14, -0.30), (-0.26, 0.37),
                               (-0.10, 0.30)))"""))

# --- scene 5: the 4.5 cm label goes inside the triangle --------------------
reps.append((
    """            lab_bc = side_label(B, C, A, "4.5 cm", CHALK_YELLOW, 15, 0.20)""",
    """            # pushed towards the inside of the triangle: outward would run
            # into the step column
            lab_bc = side_label(B, C, B + C - A, "4.5 cm", CHALK_YELLOW, 15,
                                0.20)"""))

# --- scenes 6 and 7: drop the dashed A C -----------------------------------
reps.append((
    """            bc = Line(B, C, color=CHALK_YELLOW, stroke_width=4.2)
            ac = DashedLine(A, C, color=CHALK_WHITE, stroke_width=1.8,
                            dash_length=0.14)
            tri = Polygon(A, B, C, color=CHALK_CYAN, stroke_width=2.4,
                          fill_color=CHALK_CYAN, fill_opacity=0.14)
            ang_b = angle_mark(B, A, C, radius=0.62, color=CHALK_AMBER,
                               label="100°")
            card_c = self.column_card(degree_card(r"\\angle C = 75^\\circ",""",
    """            bc = Line(B, C, color=CHALK_YELLOW, stroke_width=4.2)
            tri = Polygon(A, B, C, color=CHALK_CYAN, stroke_width=2.4,
                          fill_color=CHALK_CYAN, fill_opacity=0.14)
            ang_b = angle_mark(B, A, C, radius=0.62, color=CHALK_AMBER,
                               label="100°")
            card_c = self.column_card(degree_card(r"\\angle C = 75^\\circ","""))
reps.append((
    """            self.play(FadeIn(tri), FadeIn(names), Create(ab), Create(bc),
                      Create(ac), FadeIn(ang_b), run_time=0.9)""",
    """            self.play(FadeIn(tri), FadeIn(names), Create(ab), Create(bc),
                      FadeIn(ang_b), run_time=0.9)"""))
reps.append((
    """            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=4.2)
            bc = Line(B, C, color=CHALK_YELLOW, stroke_width=4.2)
            ac = DashedLine(A, C, color=CHALK_WHITE, stroke_width=1.8,
                            dash_length=0.14)
            tri = Polygon(A, B, C, color=CHALK_CYAN, stroke_width=2.4,
                          fill_color=CHALK_CYAN, fill_opacity=0.14)
            ray_cd = self.ray_line(C, d["cd_deg"], dist(C, D) * 1.02,""",
    """            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=4.2)
            bc = Line(B, C, color=CHALK_YELLOW, stroke_width=4.2)
            tri = Polygon(A, B, C, color=CHALK_CYAN, stroke_width=2.4,
                          fill_color=CHALK_CYAN, fill_opacity=0.14)
            ray_cd = self.ray_line(C, d["cd_deg"], dist(C, D) * 1.02,"""))
reps.append((
    """            self.play(FadeIn(tri), FadeIn(names), Create(ab), Create(bc),
                      Create(ac), Create(ray_cd), FadeIn(ang_c), run_time=0.9)""",
    """            self.play(FadeIn(tri), FadeIn(names), Create(ab), Create(bc),
                      Create(ray_cd), FadeIn(ang_c), run_time=0.9)"""))

# --- scene 9: the card column drops clear of the tag ----------------------
reps.append((
    """            ).arrange(DOWN, buff=0.15).move_to(np.array([3.05, 0.85, 0]))""",
    """            ).arrange(DOWN, buff=0.15).move_to(np.array([3.05, 0.55, 0]))"""))

# --- scene 10: the 75 degree label off the triangle's A C edge -------------
reps.append((
    """            ang_c = angle_mark(C, B, D, radius=0.58, color=CHALK_PINK,
                               label="75°")""",
    """            ang_c = angle_mark(C, B, D, radius=0.58, color=CHALK_PINK,
                               label=None)
            ang_c_lab = board_text("75°", 15, CHALK_PINK, "BOLD").move_to(
                np.array(C, dtype=float) + 0.92 * unit(
                    d["cb_deg"] + 0.24 * (d["cd_deg"] - d["cb_deg"])))"""))
reps.append((
    """            self.play(Create(cd), FadeIn(ang_c), FadeIn(rows[1],
                                                        shift=RIGHT * 0.12),
                      run_time=min(leftover(tracker, "b2"), 0.9))""",
    """            self.play(Create(cd), FadeIn(ang_c), FadeIn(ang_c_lab),
                      FadeIn(rows[1], shift=RIGHT * 0.12),
                      run_time=min(leftover(tracker, "b2"), 0.9))"""))
reps.append((
    """            summary = VGroup(quad, names, tri, ab, bc, cd, ad, ang_b, ang_c,
                             rows, final, take, acr, acr_box)""",
    """            summary = VGroup(quad, names, tri, ab, bc, cd, ad, ang_b, ang_c,
                             ang_c_lab, rows, final, take, acr, acr_box)"""))

for old, new in reps:
    assert old in s, f"not found: {old[:70]!r}"
    s = s.replace(old, new, 1)

P.write_text(s, encoding="utf-8")
print(f"beats: {n0} -> {len(s)} chars, {len(reps)} replacements")

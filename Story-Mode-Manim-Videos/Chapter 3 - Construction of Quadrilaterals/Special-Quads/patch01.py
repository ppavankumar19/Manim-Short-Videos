"""Patch 01 of the special-quadrilaterals beats, from the first audit pass.

  scene 1   an empty String became an empty Text mobject, and the three
            questions fell just outside their cards: the cards are taller now
            and every line lives inside
  scene 2   the dashed T-E link ran through both 45 degree labels (the labels
            are also pushed clear of the sides)
  scene 3   the L letter sat on the arc that marks it; the two 135 degree
            labels move outside the figure; the "complete" strip moves off the
            E letter
  scene 4/5 the half-diagonal labels sat on the compass legs, which is what the
            boxed "OB = OD = 6/2 = 3" card already says
  scene 6   the 4.2 cm label and the perpendicular label sat on the tools; the
            ask line moves off the D letter
  scene 7   the comparison columns overflowed: no "given" line, shorter
            effects, figures lower
  scene 9   the setup's 65 degree mark was still on the board when the reveal
            added its own
  scene 10  the closing windows were out of order, so the scene overran its
            narration by 1.1 s
"""
from pathlib import Path

P = Path(__file__).resolve().parent / "_specialq_beats.py"
s = P.read_text(encoding="utf-8")
n0 = len(s)
reps = []

# ---------------------------------------------------------------- scene 1 ---
reps.append((
    """                box = RoundedRectangle(corner_radius=0.14, width=3.05,
                                       height=2.55, stroke_color=CHALK_WHITE,
                                       stroke_width=2.0, fill_color="#16202B",
                                       fill_opacity=0.45).move_to(
                    np.array([x, 0.35, 0]))
                head = board_text(name, 15, CHALK_YELLOW, "BOLD").move_to(
                    np.array([x, 1.38, 0]))
                give = VGroup(board_text(gv[0], 13, CHALK_WHITE, "BOLD"),
                              board_text(gv[1], 14, CHALK_CYAN, "BOLD"),
                              board_text(gv[2], 14, CHALK_CYAN, "BOLD")
                              ).arrange(DOWN, buff=0.10).move_to(
                    np.array([x, 0.72, 0]))
                qm = board_text("?", 30, CHALK_PINK, "BOLD").move_to(
                    np.array([x, -0.42, 0]))""",
    """                box = RoundedRectangle(corner_radius=0.14, width=3.05,
                                       height=2.90, stroke_color=CHALK_WHITE,
                                       stroke_width=2.0, fill_color="#16202B",
                                       fill_opacity=0.45).move_to(
                    np.array([x, 0.30, 0]))
                head = board_text(name, 15, CHALK_YELLOW, "BOLD").move_to(
                    np.array([x, 1.50, 0]))
                # empty entries would become empty Text mobjects
                give = VGroup(*[board_text(line, 14, colour, "BOLD")
                                for line, colour in zip(gv, (CHALK_WHITE,
                                                             CHALK_CYAN,
                                                             CHALK_CYAN))
                                if line]).arrange(DOWN, buff=0.10).move_to(
                    np.array([x, 0.80, 0]))
                qm = board_text("?", 30, CHALK_PINK, "BOLD").move_to(
                    np.array([x, -0.25, 0]))"""))
reps.append((
    """                prop = VGroup(*[board_text(line, 13, CHALK_GREEN, "BOLD")
                                for line in pk if line]
                              ).arrange(DOWN, buff=0.08).move_to(
                    np.array([x, -0.48, 0]))""",
    """                prop = VGroup(*[board_text(line, 13, CHALK_GREEN, "BOLD")
                                for line in pk if line]
                              ).arrange(DOWN, buff=0.08).move_to(
                    np.array([x, -0.35, 0]))"""))
reps.append((
    """            question = board_text(asks[0], 14, CHALK_WHITE, "BOLD").move_to(
                np.array([cols[0], -1.05, 0]))
            question2 = board_text(asks[1], 14, CHALK_WHITE, "BOLD").move_to(
                np.array([cols[1], -1.05, 0]))
            question3 = board_text(asks[2], 14, CHALK_WHITE, "BOLD").move_to(
                np.array([cols[2], -1.05, 0]))""",
    """            question = board_text(asks[0], 14, CHALK_WHITE, "BOLD").move_to(
                np.array([cols[0], -0.85, 0]))
            question2 = board_text(asks[1], 14, CHALK_WHITE, "BOLD").move_to(
                np.array([cols[1], -0.85, 0]))
            question3 = board_text(asks[2], 14, CHALK_WHITE, "BOLD").move_to(
                np.array([cols[2], -0.85, 0]))"""))

# ---------------------------------------------------------------- scene 2 ---
reps.append((
    """            ang_t = angle_mark(T, E, B, radius=0.46, color=CHALK_YELLOW,
                               label="45°")""",
    """            ang_t = angle_mark(T, E, B, radius=0.46, color=CHALK_YELLOW,
                               label=None)
            ang_t_lab = board_text("45°", 15, CHALK_YELLOW, "BOLD").move_to(
                np.array(T, dtype=float) + 1.05 * unit(
                    (dir_deg(T, E) + dir_deg(T, B)) / 2.0))"""))
reps.append((
    """            ang_e = angle_mark(E, B, L, radius=0.46, color=CHALK_YELLOW,
                               label="45°")
            link = DashedLine(np.array(T, dtype=float), np.array(E, dtype=float),
                              color=CHALK_YELLOW, stroke_width=2.2,
                              dash_length=0.14)""",
    """            ang_e = angle_mark(E, B, L, radius=0.46, color=CHALK_YELLOW,
                               label=None)
            ang_e_lab = board_text("45°", 15, CHALK_YELLOW, "BOLD").move_to(
                np.array(E, dtype=float) + 0.90 * unit(
                    (dir_deg(E, B) + dir_deg(E, L)) / 2.0))"""))
reps.append((
    """            self.play(FadeIn(ang_t), run_time=0.5)""",
    """            self.play(FadeIn(ang_t), FadeIn(ang_t_lab), run_time=0.5)"""))
reps.append((
    """            self.play(Create(link), FadeIn(note_opp), FadeIn(ang_e),
                      run_time=min(leftover(tracker, "b2"), 0.9))""",
    """            self.play(FadeIn(note_opp), FadeIn(ang_e), FadeIn(ang_e_lab),
                      run_time=min(leftover(tracker, "b2"), 0.9))"""))

# ---------------------------------------------------------------- scene 3 ---
reps.append((
    """            ray_el = self.ray_line(E, d["el_deg"], dist(E, L) * 1.05,
                                   CHALK_AMBER, 3.2)
            l_dot = Dot(radius=0.10, color=CHALK_YELLOW).move_to(L)
            l_name = board_text("L", 17, CHALK_WHITE, "BOLD").move_to(
                L + np.array([0.30, 0.10, 0]))""",
    """            ray_el = self.ray_line(E, d["el_deg"], dist(E, L),
                                   CHALK_AMBER, 3.2)
            l_dot = Dot(radius=0.10, color=CHALK_YELLOW).move_to(L)
            # radially clear of the arc that marks L
            l_name = board_text("L", 17, CHALK_WHITE, "BOLD").move_to(
                L + 0.42 * unit(d["el_deg"]))"""))
reps.append((
    """            lab_b = board_text("135°", 15, CHALK_PINK, "BOLD").move_to(
                np.array(B, dtype=float) + 0.86 * unit(
                    (d["be_deg"] + d["ebt_deg"]) / 2.0))
            lab_l = board_text("135°", 15, CHALK_PINK, "BOLD").move_to(
                np.array(L, dtype=float) + 0.86 * unit(
                    (d["le_deg"] + d["lt_deg"]) / 2.0))""",
    """            # outside the figure: the triangle's own diagonal runs through
            # the middle of both 135 degree corners
            lab_b = board_text("135°", 15, CHALK_PINK, "BOLD").move_to(
                np.array(B, dtype=float) + 1.10 * unit(-20.0))
            lab_l = board_text("135°", 15, CHALK_PINK, "BOLD").move_to(
                np.array(L, dtype=float) + 1.00 * unit(20.0))"""))
reps.append((
    """            done = board_text("PARALLELOGRAM COMPLETE", 16, CHALK_GREEN, "BOLD"
                              ).move_to(np.array([3.05, -1.35, 0]))""",
    """            done = board_text("PARALLELOGRAM COMPLETE", 16, CHALK_GREEN, "BOLD"
                              ).move_to(np.array([3.05, -1.85, 0]))"""))

# ---------------------------------------------------------------- scene 4 ---
reps.append((
    """            half_b = board_text("3 cm", 14, CHALK_PINK, "BOLD").move_to(
                mid(O, B) + np.array([0.45, 0.0, 0]))
            half_d = board_text("3 cm", 14, CHALK_PINK, "BOLD").move_to(
                mid(O, D) + np.array([0.45, 0.0, 0]))
""", ""))
reps.append((
    """            self.play(FadeIn(half_b, shift=UP * 0.06),
                      FadeIn(half_d, shift=DOWN * 0.06),
                      run_time=min(leftover(tracker, "b3"), 0.7))""",
    """            self.play(Indicate(mid_ticks, color=CHALK_WHITE,
                               scale_factor=1.15),
                      run_time=min(leftover(tracker, "b3"), 0.7))"""))

# ---------------------------------------------------------------- scene 5 ---
reps.append((
    """            lab_ac = board_text("4.5 cm", 15, CHALK_YELLOW, "BOLD").move_to(
                (A + C) / 2 + DOWN * 0.32)""",
    """            # left of the perpendicular, clear of the compasses' legs
            lab_ac = board_text("4.5 cm", 15, CHALK_YELLOW, "BOLD").move_to(
                (A + C) / 2 + np.array([-0.78, -0.28, 0]))"""))
reps.append((
    """            b_lab = board_text("3 cm", 14, CHALK_PINK, "BOLD").move_to(
                mid(O, B) + np.array([0.46, 0.0, 0]))
""", ""))
reps.append((
    """            d_lab = board_text("3 cm", 14, CHALK_PINK, "BOLD").move_to(
                mid(O, D) + np.array([0.46, 0.0, 0]))
""", ""))
reps.append((
    """            self.play(FadeIn(b_dot, scale=0.5), FadeIn(b_name), FadeIn(b_lab),
                      FadeIn(card_3), run_time=min(leftover(tracker, "b3"), 0.8))""",
    """            self.play(FadeIn(b_dot, scale=0.5), FadeIn(b_name),
                      FadeIn(card_3), run_time=min(
                          leftover(tracker, "b3"), 0.8))"""))
reps.append((
    """            self.play(FadeIn(d_dot, scale=0.5), FadeIn(d_name), FadeIn(d_lab),
                      run_time=min(leftover(tracker, "b4"), 0.8))""",
    """            self.play(FadeIn(d_dot, scale=0.5), FadeIn(d_name),
                      run_time=min(leftover(tracker, "b4"), 0.8))"""))

# ---------------------------------------------------------------- scene 6 ---
reps.append((
    """            ask = board_text("What if both diagonals are equal?", 17,
                             CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))""",
    """            ask = board_text("What if both diagonals are equal?", 17,
                             CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX + 0.85, -2.68, 0]))"""))
reps.append((
    """            perp = DashedLine(perp_a, perp_b, color=CHALK_WHITE,
                              stroke_width=2.2, dash_length=0.16)
            perp_lab = board_text("perpendicular\\nthrough O", 14, CHALK_WHITE,
                                  "BOLD").move_to(O2 + np.array([1.55, 0.95, 0]))""",
    """            perp = DashedLine(perp_a, perp_b, color=CHALK_WHITE,
                              stroke_width=2.2, dash_length=0.16)"""))
reps.append((
    """            perp_a, perp_b = perpendicular_ends(O2, s["ju_deg"],
                                                dist(O2, M2) * 1.25)""",
    """            perp_a, perp_b = perpendicular_ends(O2, s["ju_deg"],
                                                dist(O2, M2) * 1.05)"""))
reps.append((
    """            lab_ju = board_text("4.2 cm", 15, CHALK_YELLOW, "BOLD").move_to(
                (J2 + U2) / 2 + DOWN * 0.32)""",
    """            lab_ju = board_text("4.2 cm", 15, CHALK_YELLOW, "BOLD").move_to(
                (J2 + U2) / 2 + np.array([-0.62, -0.52, 0]))"""))
reps.append((
    """            half_m = board_text("2.1 cm", 14, CHALK_GREEN, "BOLD").move_to(
                mid(O2, M2) + np.array([0.52, 0.0, 0]))
            half_p = board_text("2.1 cm", 14, CHALK_GREEN, "BOLD").move_to(
                mid(O2, P2) + np.array([0.52, 0.0, 0]))
""", ""))
reps.append((
    """            self.play(Create(perp), FadeIn(perp_lab), run_time=min(
                leftover(tracker, "b3"), 0.8))""",
    """            self.play(Create(perp), run_time=min(
                leftover(tracker, "b3"), 0.8))"""))
reps.append((
    """            self.play(FadeIn(m_dot, scale=0.5), FadeIn(m_name), FadeIn(half_m),
                      run_time=min(leftover(tracker, "b4"), 0.7))""",
    """            self.play(FadeIn(m_dot, scale=0.5), FadeIn(m_name),
                      run_time=min(leftover(tracker, "b4"), 0.7))"""))
reps.append((
    """            self.play(FadeIn(p_dot, scale=0.5), FadeIn(p_name), FadeIn(half_p),
                      run_time=min(leftover(tracker, "b4"), 0.7))""",
    """            self.play(FadeIn(p_dot, scale=0.5), FadeIn(p_name),
                      run_time=min(leftover(tracker, "b4"), 0.7))"""))

for old, new in reps:
    assert old in s, f"not found: {old[:70]!r}"
    s = s.replace(old, new, 1)

P.write_text(s, encoding="utf-8")
print(f"beats: {n0} -> {len(s)} chars, {len(reps)} replacements")

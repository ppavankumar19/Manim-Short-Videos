"""One-off patch of _sasaa_beats.py after the first audit pass.

Every change here answers a flag in audit_report.txt from the first 360p cut:
the title card's rays ran through the sub-title, several vertex letters sat on
lines or on the bottom notes, the scene-2 "use later" panel overlapped its own
caption, the scene-3 column captions touched their cards, the "4 cm" and "100
degree" labels sat on the protractor, the scene-5/6 R and 75 labels sat on the
compass arc and the dashed P R, scene 7 drew the letter S twice, and the
challenge's reveal added a sixth card on top of the five.
"""
from pathlib import Path

P = Path(__file__).resolve().parent / "_sasaa_beats.py"
s = P.read_text(encoding="utf-8")
before = s

# 1. vertex letters: R moved off the arc, S moved off the rays
s = s.replace("""                (P, Q, R, S), ((-0.28, -0.10), (0.12, -0.30), (0.30, 0.02),
                               (-0.12, 0.30)))""",
              """                (P, Q, R, S), ((-0.28, -0.10), (0.12, -0.30), (0.40, -0.28),
                               (-0.14, 0.34)))""")
s = s.replace("""                (P, Q, R, S), ((-0.24, -0.09), (0.10, -0.26), (0.26, 0.02),
                               (-0.10, 0.26)), size=15)""",
              """                (P, Q, R, S), ((-0.24, -0.09), (0.10, -0.26), (0.34, -0.22),
                               (-0.14, 0.30)), size=15)""")
# scenes 4-7: S is not known yet, so only P Q R are lettered
s = s.replace("""                (P, Q, R, S), ((-0.28, -0.10), (0.12, -0.30), (0.40, -0.28),
                               (-0.14, 0.34)))
            pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=4.2)""",
              """                (P, Q, R), ((-0.28, -0.10), (0.12, -0.30), (0.40, -0.28)))
            pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=4.2)""")
s = s.replace("""            names = self.vertex_letters(
                (P, Q, R, S), ((-0.28, -0.10), (0.12, -0.30), (0.40, -0.28),
                               (-0.14, 0.34)))
            pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=4.0)""",
              """            names = self.vertex_letters(
                (P, Q, R, S), ((-0.28, -0.10), (0.12, -0.30), (0.40, -0.28),
                               (-0.14, 0.34)))
            pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=4.0)""")

# 2. the dashed P R belongs to scene 5 only
s = s.replace("""            ray_p = self.ray_line(P, d["ps_deg"], dist(P, S) * 1.06, CHALK_CYAN,
                                  3.2)
            ang_p = board_text("75°", 15, CHALK_YELLOW, "BOLD").move_to(
                np.array(P, dtype=float) + 1.06 * unit(
                    (d["pq_deg"] + d["ps_deg"]) / 2.0))
            card_r = self.column_card(degree_card(r"\\angle R = 120^\\circ", CHALK_PINK), 1.55)""",
              """            ray_p = self.ray_line(P, d["ps_deg"], dist(P, S) * 1.06, CHALK_CYAN,
                                  3.2)
            ang_p = board_text("75°", 15, CHALK_YELLOW, "BOLD").move_to(
                np.array(P, dtype=float) + 1.30 * unit(
                    (d["pq_deg"] + d["ps_deg"]) / 2.0))
            card_r = self.column_card(degree_card(r"\\angle R = 120^\\circ", CHALK_PINK), 1.55)""")
s = s.replace("""            pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=4.2)
            qr = Line(Q, R, color=CHALK_YELLOW, stroke_width=4.2)
            pr = DashedLine(P, R, color=CHALK_WHITE, stroke_width=2.0,
                            dash_length=0.14)
            tri = Polygon(P, Q, R, color=CHALK_CYAN, stroke_width=2.4,
                          fill_color=CHALK_CYAN, fill_opacity=0.14)
            ang_q = angle_mark(Q, P, R, radius=0.55, color=CHALK_AMBER)""",
              """            pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=4.2)
            qr = Line(Q, R, color=CHALK_YELLOW, stroke_width=4.2)
            tri = Polygon(P, Q, R, color=CHALK_CYAN, stroke_width=2.4,
                          fill_color=CHALK_CYAN, fill_opacity=0.14)
            ang_q = angle_mark(Q, P, R, radius=0.55, color=CHALK_AMBER)""")
s = s.replace("""            self.play(FadeIn(tri), FadeIn(names), Create(pq), Create(qr),
                      Create(pr), FadeIn(ang_q), FadeIn(ang_lab_q),
                      run_time=0.9)""",
              """            self.play(FadeIn(tri), FadeIn(names), Create(pq), Create(qr),
                      FadeIn(ang_q), FadeIn(ang_lab_q), run_time=0.9)""")
s = s.replace("""            self.play(FadeIn(tri), FadeIn(names), Create(pq), Create(qr),
                      Create(pr), Create(ray_p), FadeIn(ang_p), run_time=0.9)""",
              """            self.play(FadeIn(tri), FadeIn(names), Create(pq), Create(qr),
                      Create(ray_p), FadeIn(ang_p), run_time=0.9)""")
s = s.replace("""            pr = DashedLine(P, R, color=CHALK_WHITE, stroke_width=1.8,
                            dash_length=0.14)
            ps = Line(P, S, color=CHALK_GREEN, stroke_width=4.2)""",
              """            ps = Line(P, S, color=CHALK_GREEN, stroke_width=4.2)""")
s = s.replace("""            self.play(Create(ps), Create(rs), Create(pr), run_time=min(
                leftover(tracker, "b0"), 1.0))""",
              """            self.play(Create(ps), Create(rs), run_time=min(
                leftover(tracker, "b0"), 1.0))""")
s = s.replace("""            self.play(FadeOut(checks), FadeOut(check_lab), FadeOut(pr),
                      FadeOut(ang_p), FadeOut(ang_q), FadeOut(ang_r),
                      run_time=0.5)""",
              """            self.play(FadeOut(checks), FadeOut(check_lab),
                      FadeOut(ang_p), FadeOut(ang_q), FadeOut(ang_r),
                      run_time=0.5)""")

# 3. scene 2: the "use later" caption above its panel, cards down a little
s = s.replace("""            later_lab = board_text("USE LATER", 15, CHALK_PINK, "BOLD"
                                   ).move_to(np.array([3.05, -1.30, 0]))
            later = VGroup(
                degree_card(r"\\angle P = 75^\\circ", CHALK_CYAN, 15),
                degree_card(r"\\angle R = 120^\\circ", CHALK_PINK, 15),
            ).arrange(DOWN, buff=0.18).move_to(np.array([3.05, -1.95, 0]))""",
              """            later_lab = board_text("USE LATER", 15, CHALK_PINK, "BOLD"
                                   ).move_to(np.array([3.05, -1.15, 0]))
            later = VGroup(
                degree_card(r"\\angle P = 75^\\circ", CHALK_CYAN, 15),
                degree_card(r"\\angle R = 120^\\circ", CHALK_PINK, 15),
            ).arrange(DOWN, buff=0.18).move_to(np.array([3.05, -2.00, 0]))""")

# 4. scene 3: column captions clear of their cards, S off the rays
s = s.replace("""            lab_build = board_text("BUILD", 18, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX - 2.5, 1.95, 0]))""",
              """            lab_build = board_text("BUILD", 18, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX - 2.5, 2.18, 0]))""")
s = s.replace("""            ).arrange(DOWN, buff=0.22).move_to(
                np.array([BOARD_CX - 2.5, 0.95, 0]))""",
              """            ).arrange(DOWN, buff=0.22).move_to(
                np.array([BOARD_CX - 2.5, 1.05, 0]))""")
s = s.replace("""            lab_locate = board_text("LOCATE", 18, CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX + 2.6, 1.95, 0]))""",
              """            lab_locate = board_text("LOCATE", 18, CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX + 2.6, 2.18, 0]))""")
s = s.replace("""            ).arrange(DOWN, buff=0.22).move_to(
                np.array([BOARD_CX + 2.6, 1.05, 0]))""",
              """            ).arrange(DOWN, buff=0.22).move_to(
                np.array([BOARD_CX + 2.6, 1.32, 0]))""")
s = s.replace("""            m_s = board_text("S", 15, CHALK_WHITE, "BOLD").move_to(
                mv + np.array([0.34, 0.22, 0]))""",
              """            m_s = board_text("S", 15, CHALK_WHITE, "BOLD").move_to(
                mv + np.array([0.48, 0.32, 0]))""")

# 5. scene 4: the 4 cm label clear of the protractor, the reading outside it
s = s.replace("""            lab_pq = board_text("4 cm", 15, CHALK_YELLOW, "BOLD").move_to(
                (P + Q) / 2 + UP * 0.26)
            prot = protractor(Q, color=CHALK_AMBER, radius=0.95)""",
              """            lab_pq = board_text("4 cm", 15, CHALK_YELLOW, "BOLD").move_to(
                P + np.array([0.55, 0.26, 0]))
            prot = protractor(Q, color=CHALK_AMBER, radius=0.95)""")
s = s.replace("""            lab_pq = board_text("4 cm", 15, CHALK_YELLOW, "BOLD").move_to(
                (P + Q) / 2 + UP * 0.26)
            ray_qr = self.ray_line(Q, d["qr_deg"], dist(Q, R) * 1.10,""",
              """            lab_pq = board_text("4 cm", 15, CHALK_YELLOW, "BOLD").move_to(
                P + np.array([0.55, 0.26, 0]))
            ray_qr = self.ray_line(Q, d["qr_deg"], dist(Q, R) * 1.10,""")
s = s.replace("""            ang_lab = board_text("100°", 15, CHALK_AMBER, "BOLD").move_to(
                np.array(Q, dtype=float) + 0.92 * unit(
                    (d["qp_deg"] + tick_deg) / 2.0))""",
              """            ang_lab = board_text("100°", 15, CHALK_AMBER, "BOLD").move_to(
                np.array(Q, dtype=float) + 1.30 * unit(
                    (d["qp_deg"] + tick_deg) / 2.0))""")
s = s.replace("""            ang_lab = board_text("100°", 15, CHALK_AMBER, "BOLD").move_to(
                np.array(Q, dtype=float) + 0.92 * unit(
                    (d["qp_deg"] + d["qr_deg"]) / 2.0))""",
              """            ang_lab = board_text("100°", 15, CHALK_AMBER, "BOLD").move_to(
                np.array(Q, dtype=float) + 1.30 * unit(
                    (d["qp_deg"] + d["qr_deg"]) / 2.0))""")
s = s.replace("""                np.array(Q, dtype=float) + 0.92 * unit(
                    (d["qp_deg"] + d["qr_deg"]) / 2.0))
            card_p = self.column_card(""",
              """                np.array(Q, dtype=float) + 1.30 * unit(
                    (d["qp_deg"] + d["qr_deg"]) / 2.0))
            card_p = self.column_card(""")
s = s.replace("""                np.array(P, dtype=float) + 1.06 * unit(
                    (d["pq_deg"] + d["ps_deg"]) / 2.0))""",
              """                np.array(P, dtype=float) + 1.30 * unit(
                    (d["pq_deg"] + d["ps_deg"]) / 2.0))""")

# 6. scene 7: the R ray stops just past S; scene 8: no "check" caption
s = s.replace("""            ray_r = self.ray_line(R, d["rs_deg"], dist(R, S) * 1.26, CHALK_PINK,
                                  3.2)
            s_dot = Dot(radius=0.11, color=CHALK_YELLOW).move_to(S)""",
              """            ray_r = self.ray_line(R, d["rs_deg"], dist(R, S) * 1.06, CHALK_PINK,
                                  3.2)
            s_dot = Dot(radius=0.11, color=CHALK_YELLOW).move_to(S)""")
s = s.replace("""            check_lab = board_text("Every given measurement used", 15,
                                   CHALK_GREEN, "BOLD").move_to(
                np.array([3.05, 1.95, 0]))
""", "")
s = s.replace("""            self.play(FadeIn(check_lab), run_time=0.35)
            self.play(LaggedStart""", """            self.play(LaggedStart""")
s = s.replace("""            self.play(FadeOut(checks), FadeOut(check_lab),
                      FadeOut(ang_p)""", """            self.play(FadeOut(checks), FadeOut(ang_p)""")
s = s.replace("""            ).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to(
                np.array([2.55, 0.60, 0]))""",
              """            ).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to(
                np.array([2.62, 0.35, 0]))""")

# 7. challenge: no sixth card, the question clear of the B letter, D's letter
#    off the A ray, the A ray not overshooting into D's letter
s = s.replace("""            names = self.vertex_letters(
                (A, B, C, D), ((-0.28, -0.10), (0.12, -0.30), (0.30, 0.02),
                               (-0.10, 0.30)), letters="ABCD")""",
              """            names = self.vertex_letters(
                (A, B, C, D), ((-0.28, -0.10), (0.12, -0.30), (0.40, -0.28),
                               (-0.34, 0.06)), letters="ABCD")""")
s = s.replace("""            ask = board_text("Which three measurements come first?", 17,
                             CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX + 0.20, -2.45, 0]))""",
              """            ask = board_text("Which three measurements come first?", 17,
                             CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX + 0.75, -2.50, 0]))""")
s = s.replace("""            card_b = self.column_card(degree_card(r"\\angle B = 110^\\circ", CHALK_AMBER),
                                      0.60)
            badge = board_text("First triangle: A B C", 17, CHALK_GREEN, "BOLD"
                               ).move_to(np.array([3.05, -1.55, 0]))
            self.play(Create(tri), FadeIn(card_b),
                      Circumscribe(tri, color=CHALK_GREEN, stroke_width=2.6,
                                   time_width=0.6),
                      run_time=min(leftover(tracker, "b1"), 1.2))""",
              """            badge = board_text("First triangle: A B C", 17, CHALK_GREEN, "BOLD"
                               ).move_to(np.array([3.05, -1.55, 0]))
            self.play(Create(tri),
                      Indicate(ch["cards"][3], color=CHALK_AMBER,
                               scale_factor=1.12),
                      Circumscribe(tri, color=CHALK_GREEN, stroke_width=2.6,
                                   time_width=0.6),
                      run_time=min(leftover(tracker, "b1"), 1.2))""")
s = s.replace("""            ray_a = self.ray_line(A, d["ps_deg"], dist(A, D) * 1.06, CHALK_CYAN,
                                  3.0)
            ray_c = self.ray_line(C, d["rs_deg"], dist(C, D) * 1.30, CHALK_PINK,
                                  3.0)""",
              """            ray_a = self.ray_line(A, d["ps_deg"], dist(A, D) * 1.02, CHALK_CYAN,
                                  3.0)
            ray_c = self.ray_line(C, d["rs_deg"], dist(C, D) * 1.08, CHALK_PINK,
                                  3.0)""")

# 8. title card: the two rays are drawn relative to the small figure
s = s.replace("""            ray_p = self.ray_line(P, d["ps_deg"], 3.30, CHALK_CYAN, 2.6, True)
            ray_r = self.ray_line(R, d["rs_deg"], 2.40, CHALK_PINK, 2.6, True)""",
              """            ray_p = self.ray_line(P, d["ps_deg"], dist(P, S) * 1.05,
                                  CHALK_CYAN, 2.6, True)
            ray_r = self.ray_line(R, d["rs_deg"], dist(R, S) * 1.05,
                                  CHALK_PINK, 2.6, True)""")

# 9. recap: the R ray stops just past S
s = s.replace("""            ray_r = self.ray_line(R, d["rs_deg"], dist(R, S) * 1.26, CHALK_PINK,
                                  2.6)""",
              """            ray_r = self.ray_line(R, d["rs_deg"], dist(R, S) * 1.06, CHALK_PINK,
                                  2.6)""")

P.write_text(s, encoding="utf-8")
print(f"patched: {len(before.splitlines())} -> {len(s.splitlines())} lines")
for token in ("pr = DashedLine", "check_lab", "card_b", "0.92 * unit",
              "1.26, CHALK_PINK", "0.30, 0.02"):
    print(f"  {token!r}: {s.count(token)}")

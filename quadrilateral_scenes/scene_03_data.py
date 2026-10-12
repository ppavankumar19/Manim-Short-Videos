from common import *

# figure on the left, the five given numbers on the right
OFF = np.array([-3.05, 0.35, 0.0])
A3, B3, C3, D3 = [p + OFF for p in (A, B, C, D)]


class Scene03Data(VoiceoverScene):
    """What the question hands you: three sides, two diagonals, no more."""

    def construct(self):
        self.set_speech_service(scene_speech_service("data"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(paper_backdrop())

        quad = Polygon(A3, B3, C3, D3, stroke_color=INK, stroke_width=3,
                       stroke_opacity=0.35, fill_color=ACCENT,
                       fill_opacity=0.07)
        s_ab = Line(A3, B3, stroke_color=ACCENT, stroke_width=7)
        s_bc = Line(B3, C3, stroke_color=ACCENT, stroke_width=7)
        s_cd = Line(C3, D3, stroke_color=ACCENT, stroke_width=7)
        s_ad = DashedLine(A3, D3, stroke_color=ROSE, stroke_width=6,
                          dash_length=0.13)
        g_ac = Line(A3, C3, stroke_color=VIOLET, stroke_width=6)
        g_bd = Line(B3, D3, stroke_color=VIOLET, stroke_width=6)

        vA = vertex(A3, "A", DOWN + LEFT * 0.4)
        vB = vertex(B3, "B", DOWN + RIGHT * 0.4)
        vC = vertex(C3, "C", UP + RIGHT * 0.3)
        vD = vertex(D3, "D", LEFT + UP * 0.3)
        marks = VGroup(vA, vB, vC, vD)

        l_ab = side_label(A3, B3, "4.5", ACCENT, 26, out=DOWN, buff=0.34)
        l_bc = side_label(B3, C3, "5.2", ACCENT, 26, out=RIGHT, buff=0.34)
        l_cd = side_label(C3, D3, "4.8", ACCENT, 26, out=UP + LEFT, buff=0.34)
        l_ac = mtx("5", 26, VIOLET).move_to((A3 + C3) / 2 + np.array([0.40, -0.18, 0.0]))   # perpendicular to AC, clear of the stroke
        l_bd = mtx("5.4", 26, VIOLET).move_to((B3 + D3) / 2 + np.array([0.10, 0.34, 0.0]))
        l_ad = mtx("?", 30, ROSE).move_to((A3 + D3) / 2 + np.array([-0.36, -0.10, 0.0]))

        rows = VGroup(
            mtx(r"AB \;=\; 4.5", 36, ACCENT),
            mtx(r"BC \;=\; 5.2", 36, ACCENT),
            mtx(r"CD \;=\; 4.8", 36, ACCENT),
            mtx(r"AC \;=\; 5.0", 36, VIOLET),
            mtx(r"BD \;=\; 5.4", 36, VIOLET),
        ).arrange(DOWN, buff=0.44, aligned_edge=LEFT)
        rows.move_to(np.array([3.55, 0.85, 0.0]))
        frame = SurroundingRectangle(rows, color=MUTED, buff=0.50,
                                     corner_radius=0.16)
        missing = mtx(r"AD \;=\; ?", 36, ROSE)
        missing.next_to(frame, DOWN, buff=0.45)
        total = mtx(r"3 \;+\; 2 \;=\; 5", 40, AMBER)
        total.next_to(missing, DOWN, buff=0.50)

        with self.voiceover(text=NARRATION["data"]):
            self.play(FadeIn(quad), Create(frame),
                      LaggedStart(*[FadeIn(m, scale=0.6) for m in marks],
                                  lag_ratio=0.2),
                      run_time=6.23)
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(
                LaggedStart(
                    AnimationGroup(Create(s_ab), FadeIn(l_ab), FadeIn(rows[0])),
                    AnimationGroup(Create(s_bc), FadeIn(l_bc), FadeIn(rows[1])),
                    AnimationGroup(Create(s_cd), FadeIn(l_cd), FadeIn(rows[2])),
                    lag_ratio=0.42,
                ),
                run_time=3.48,
            )
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(
                LaggedStart(
                    AnimationGroup(Create(g_ac), FadeIn(l_ac), FadeIn(rows[3])),
                    AnimationGroup(Create(g_bd), FadeIn(l_bd), FadeIn(rows[4])),
                    lag_ratio=0.45,
                ),
                run_time=3.06,
            )
            self.add_sound(self.sfx["pop"], gain=-16)
            self.play(Create(s_ad), FadeIn(l_ad, scale=1.5),
                      FadeIn(missing, shift=UP * 0.15), run_time=4.22)
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(Write(total), Circumscribe(frame, color=AMBER, buff=0.10),
                      run_time=1.48)
            self.play(
                FadeOut(VGroup(quad, s_ab, s_bc, s_cd, s_ad, g_ac, g_bd, marks,
                               l_ab, l_bc, l_cd, l_ac, l_bd, l_ad, rows, frame,
                               missing, total)),
                run_time=0.53,
            )
        # beats sized to the sentences they illustrate
        # 6.23+3.48+3.06+4.22+1.48+0.53 = 19.0 s

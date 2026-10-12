from common import *


class Scene12Example2(VoiceoverScene):
    """Their turn: a real pause, a drawn cancellation, then the answer."""

    def construct(self):
        self.set_speech_service(scene_speech_service("example2"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(lesson_backdrop())

        head = txt("Your turn!", 42, AMBER).to_edge(UP, buff=0.50)

        C = np.array([-4.0, -0.10, 0.0])
        plot = garden(C, 1.55)
        r_line = Line(C, C + RIGHT * 1.55, stroke_color=AMBER, stroke_width=7)
        r_dot = Dot(C, radius=0.075, color=AMBER)
        r_lbl = chip(mtx(r"7\,\text{m}", 36, AMBER)
                     .next_to(r_line, UP, buff=0.18))
        g_cap = txt("a round garden", 28, MUTED).next_to(plot, DOWN, buff=0.34)

        pause = txt("PAUSE and try it!", 44, ROSE).move_to(np.array([2.9, 0.85, 0.0]))
        p_ring = SurroundingRectangle(pause, color=ROSE, buff=0.36,
                                      corner_radius=0.18)

        # Built from parts so the 7 underneath and a 7 in front can each be
        # struck through on their own.
        a_eq = mtx(r"A \;=", 44, INK)
        f = frac("22", "7", 40, INK)
        x1 = mtx(r"\times", 36, INK)
        s1 = mtx("7", 44, INK)
        x2 = mtx(r"\times", 36, INK)
        s2 = mtx("7", 44, INK)
        line1 = VGroup(a_eq, f, x1, s1, x2, s2).arrange(RIGHT, buff=0.18)
        line1.move_to(np.array([2.9, 0.95, 0.0]))

        s_den, s_seven, link = cancel_pair(f.den, s1, ROSE)

        mid = mtx(r"A \;=\; 22 \times 7", 46, INK)
        mid.move_to(np.array([2.9, 0.95, 0.0]))
        final = mtx(r"A \;=\; 154\,\text{m}^2", 56, SUCCESS)
        final.move_to(np.array([2.9, -1.05, 0.0]))
        box = SurroundingRectangle(final, color=SUCCESS, buff=0.26,
                                   corner_radius=0.14)

        with self.voiceover(text=NARRATION["example2"]):
            self.play(FadeIn(head, shift=DOWN * 0.2), run_time=3.64)
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(GrowFromCenter(plot), FadeIn(r_dot),
                      Create(r_line), FadeIn(r_lbl), FadeIn(g_cap),
                      run_time=4.09)
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(FadeIn(pause, scale=0.7), Create(p_ring), run_time=3.19)
            self.play(FadeOut(VGroup(pause, p_ring)), run_time=2.74)
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(Write(line1), run_time=3.64)

            # --- "the sevens cancel", drawn ------------------------------
            self.add_sound(self.sfx["swipe"], gain=-16)
            self.play(Create(link), run_time=0.45)
            self.play(Create(s_den), Create(s_seven), run_time=0.92)
            self.add_sound(self.sfx["pop"], gain=-16)
            self.play(
                FadeOut(VGroup(f, s1, x1, s_den, s_seven, link), scale=0.35),
                ReplacementTransform(VGroup(a_eq, x2, s2), mid),
                run_time=1.25,
            )
            self.add_sound(self.sfx["success"], gain=-13)
            self.play(FadeIn(final, shift=UP * 0.2), Create(box),
                      Flash(final.get_center(), color=SUCCESS,
                            flash_radius=1.4, num_lines=16),
                      run_time=3.77)
        # 3.64+4.09+3.19+2.74+3.64+0.45+0.92+1.25+3.77 = 23.69 s

        self.play(FadeOut(VGroup(head, plot, r_dot, r_line, r_lbl, g_cap,
                                 mid, final, box)), run_time=0.62)

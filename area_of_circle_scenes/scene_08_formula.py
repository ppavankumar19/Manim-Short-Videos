from common import *

T = np.array([0.0, -1.55, 0.0])          # triangle base midpoint
HALF = TAU * R_CIRC / 2


class Scene08Formula(VoiceoverScene):
    """Measure the triangle, cancel the halves, and pi r squared falls out."""

    def construct(self):
        self.set_speech_service(scene_speech_service("formula"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(lesson_backdrop())

        tri = Polygon(T + LEFT * HALF, T + RIGHT * HALF, T + UP * R_CIRC,
                      stroke_color=SUCCESS, stroke_width=6,
                      fill_color=AMBER, fill_opacity=0.18)

        base_br = BraceBetweenPoints(T + RIGHT * HALF, T + LEFT * HALF,
                                     direction=DOWN, color=AMBER)
        base_lbl = mtx(r"2 \pi r", 42, AMBER).next_to(base_br, DOWN, buff=0.18)
        h_line = DashedLine(T, T + UP * R_CIRC, stroke_color=SKY,
                            stroke_width=5, dash_length=0.11)
        h_br = BraceBetweenPoints(T + UP * R_CIRC + RIGHT * 0.06,
                                  T + RIGHT * 0.06, direction=RIGHT, color=SKY)
        h_lbl = mtx("r", 42, SKY).next_to(h_br, RIGHT, buff=0.16)

        rule = mtx(r"A \;=\; \tfrac{1}{2} \times b \times h", 46, INK)
        rule.move_to(np.array([0.0, 2.75, 0.0]))

        # Built from separate pieces so the 2 underneath and the 2 in front
        # can each be struck through on their own.
        a_eq = mtx(r"A \;=", 50, INK)
        half = frac("1", "2", 44, INK)
        x1 = mtx(r"\times", 40, INK)
        two = mtx("2", 50, INK)
        pir = mtx(r"\pi r", 50, INK)
        x2 = mtx(r"\times", 40, INK)
        rr = mtx("r", 50, INK)
        sub = VGroup(a_eq, half, x1, two, pir, x2, rr).arrange(RIGHT, buff=0.20)
        sub.move_to(np.array([0.0, 1.60, 0.0]))

        s_den, s_two, link = cancel_pair(half.den, two, ROSE)
        gone = txt("2 over 2 is just 1", 26, ROSE)
        gone.next_to(sub, DOWN, buff=0.34)

        answer = mtx(r"A \;=\; \pi r^2", 72, SUCCESS)
        answer.move_to(np.array([0.0, 1.60, 0.0]))
        box = SurroundingRectangle(answer, color=SUCCESS, buff=0.32,
                                   corner_radius=0.16)

        with self.voiceover(text=NARRATION["formula"]):
            self.play(FadeIn(tri), run_time=1.7)
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(Write(rule), run_time=2.98)
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(GrowFromCenter(base_br), FadeIn(base_lbl), run_time=3.83)
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(Create(h_line), GrowFromCenter(h_br), FadeIn(h_lbl),
                      run_time=2.55)
            self.play(TransformFromCopy(rule, sub), run_time=4.26)

            # --- the cancellation, drawn rather than described ------------
            self.add_sound(self.sfx["swipe"], gain=-16)
            self.play(Create(link), run_time=0.85)
            self.play(Create(s_den), Create(s_two), run_time=0.95)
            self.play(FadeIn(gone, shift=UP * 0.15),
                      Indicate(VGroup(s_den, s_two), color=ROSE,
                               scale_factor=1.15),
                      run_time=1.18)
            self.add_sound(self.sfx["ding"], gain=-13)
            # the struck terms shrink away, and what is left closes the gap
            self.play(
                FadeOut(VGroup(half, two, s_den, s_two, link, x1),
                        scale=0.35),
                run_time=1.30,
            )
            self.play(ReplacementTransform(VGroup(a_eq, pir, x2, rr), answer),
                      FadeOut(gone), run_time=2.11)
            self.add_sound(self.sfx["success"], gain=-13)
            self.play(Create(box),
                      Flash(answer.get_center(), color=SUCCESS,
                            flash_radius=1.5, num_lines=18),
                      run_time=1.7)
        # 1.7+2.98+3.83+2.55+4.26+0.85+0.95+1.18+1.3+2.11+1.7 = 23.41 s

        self.play(FadeOut(VGroup(tri, base_br, base_lbl, h_line, h_br, h_lbl,
                                 rule, answer, box)), run_time=0.53)

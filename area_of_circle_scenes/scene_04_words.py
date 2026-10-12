from common import *


class Scene04Words(VoiceoverScene):
    """Centre, radius, and the distance all the way around."""

    def construct(self):
        self.set_speech_service(scene_speech_service("words"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(lesson_backdrop())

        C = np.array([-3.4, 0.35, 0.0])
        R = 1.75
        circ = Circle(radius=R, stroke_color=ACCENT, stroke_width=7,
                      fill_color=ACCENT, fill_opacity=0.08).move_to(C)
        dot = Dot(C, color=AMBER, radius=0.10)
        l_centre = txt("centre", 30, AMBER).next_to(dot, DOWN, buff=0.22)

        edge = C + R * np.array([np.cos(38 * DEGREES), np.sin(38 * DEGREES), 0])
        radius = Line(C, edge, stroke_color=SUCCESS, stroke_width=7)
        l_radius = txt("radius", 30, SUCCESS).move_to(
            C + np.array([0.20, 1.30, 0.0]))
        r_sym = mtx("r", 46, SUCCESS).move_to(C + np.array([0.70, 0.28, 0.0]))

        # the string walks around the rim, then lies down straight
        string = Circle(radius=R, stroke_color=ROSE, stroke_width=8,
                        fill_opacity=0).move_to(C)
        straight = Line(np.array([-5.9, -2.85, 0.0]),
                        np.array([-5.9 + TAU * R * 0.62, -2.85, 0.0]),
                        stroke_color=ROSE, stroke_width=8)
        l_around = txt("circumference", 30, ROSE)
        l_around.next_to(straight, UP, buff=0.20).align_to(straight, LEFT)
        fact = mtx(r"2 \pi r", 64, ROSE).move_to(np.array([3.4, 0.55, 0.0]))
        box = SurroundingRectangle(fact, color=ROSE, buff=0.36,
                                   corner_radius=0.14)
        cap = txt("all the way around", 28, MUTED).next_to(box, UP, buff=0.30)

        with self.voiceover(text=NARRATION["words"]):
            self.play(Create(circ), run_time=1.8)
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(GrowFromCenter(dot), FadeIn(l_centre), run_time=2.9)
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(Create(radius), FadeIn(l_radius), run_time=4.33)
            self.play(FadeIn(r_sym, scale=0.6), run_time=1.44)
            self.add_sound(self.sfx["whoosh"], gain=-16)
            self.play(ReplacementTransform(string, straight),
                      FadeIn(l_around), run_time=6.85)
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(Write(fact), Create(box), FadeIn(cap), run_time=4.68)
        # 1.8+2.9+4.33+1.44+6.85+4.68+0.5 = 22.5 s

        self.play(FadeOut(VGroup(circ, dot, l_centre, radius, l_radius, r_sym,
                                 straight, l_around, fact, box, cap)),
                  run_time=0.5)

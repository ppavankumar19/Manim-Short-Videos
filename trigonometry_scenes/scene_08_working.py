from common import *

AF = np.array([-4.55, -2.25, 0.0])
DF = 1.95
BF = AF + RIGHT * DF
CF = AF + UP * (DF * np.sqrt(3.0))


class Scene08Working(VoiceoverScene):
    """Real numbers go into the same three symbols."""

    def construct(self):
        self.set_speech_service(scene_speech_service("working"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(blueprint_grid())

        tri = Polygon(AF, BF, CF, stroke_color=ACCENT, stroke_width=5,
                      fill_color=ACCENT, fill_opacity=0.12)
        rang = RightAngle(Line(AF, BF), Line(AF, CF), length=0.28, color=MUTED,
                          stroke_width=3)
        ang = Angle(Line(BF, AF), Line(BF, CF), radius=0.52, color=SUCCESS,
                    stroke_width=5, other_angle=True)
        th_lbl = mtx(r"60^\circ", 32, SUCCESS).move_to(BF + np.array([-0.98, 0.26, 0.0]))
        h_lbl = mtx(r"h", 40, ACCENT).move_to((AF + CF) / 2 + LEFT * 0.36)
        d_br = BraceBetweenPoints(BF, AF, direction=DOWN, color=VIOLET)
        d_lbl = mtx(r"15\,\text{m}", 32, VIOLET).next_to(d_br, DOWN, buff=0.14)
        man = Man(base=BF + RIGHT * 0.40, height=0.80, facing=LEFT,
                  pose=POINTING_UP)

        given = VGroup(
            mtx(r"d \;=\; 15\,\text{m}", 42, VIOLET),
            mtx(r"\theta \;=\; 60^\circ", 42, SUCCESS),
            mtx(r"h \;=\; ?", 42, AMBER),
        ).arrange(DOWN, buff=0.52, aligned_edge=LEFT).move_to(np.array([1.55, 1.35, 0.0]))
        given_box = SurroundingRectangle(given, color=MUTED, buff=0.42,
                                         corner_radius=0.14)

        eq = mtx(r"\tan 60^\circ \;=\; \frac{h}{15}", 56, INK)
        eq.move_to(np.array([2.05, -1.85, 0.0]))

        with self.voiceover(text=NARRATION["working"]):
            self.play(
                Create(tri), FadeIn(rang), Create(ang), FadeIn(th_lbl),
                FadeIn(h_lbl), GrowFromCenter(d_br), FadeIn(d_lbl), FadeIn(man),
                run_time=7.0,
            )
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(Create(given_box),
                      LaggedStart(*[FadeIn(g, shift=RIGHT * 0.2) for g in given],
                                  lag_ratio=0.3),
                      run_time=8.3)
            self.add_sound(self.sfx["ding"], gain=-15)
            self.play(Write(eq), run_time=2.7)
            self.play(
                FadeOut(VGroup(tri, rang, ang, th_lbl, h_lbl, d_br, d_lbl, man,
                               given, given_box, eq)),
                run_time=1.0,
            )
        # beats sized to the sentences they illustrate
        # 7.0+8.3+2.7+1.0 = 19.0 s

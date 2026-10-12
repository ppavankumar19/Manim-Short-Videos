from common import *

MAN_BASE = OBS + RIGHT * 0.46


class Scene03Triangle(VoiceoverScene):
    """The scene collapses into pure geometry: triangle ABC, h, d, theta."""

    def construct(self):
        self.set_speech_service(scene_speech_service("triangle"), create_subcaption=True)
        self.sfx = load_sfx()

        self.add(sky_ground_backdrop())
        self.add(star_field(18, y_min=1.2).set_opacity(0.4))

        tower = realistic_tower()
        man = Man(base=MAN_BASE, height=MAN_H, facing=LEFT, pose=POINTING_UP)
        sight = DashedLine(OBS, TOP, stroke_color=AMBER, stroke_width=4,
                           dash_length=0.14)

        side_h = Line(FOOT, TOP, stroke_color=ACCENT, stroke_width=7)
        side_d = Line(FOOT, OBS, stroke_color=VIOLET, stroke_width=7)
        side_s = Line(OBS, TOP, stroke_color=AMBER, stroke_width=6)

        h_lbl = mtx(r"h", 46, ACCENT).next_to(side_h, LEFT, buff=0.28)
        d_lbl = mtx(r"d", 46, VIOLET).next_to(side_d, DOWN, buff=0.30)

        rang = right_angle_at_foot(0.36)
        rang_lbl = mtx(r"90^\circ", 26, MUTED).move_to(
            FOOT + np.array([0.62, 0.30, 0.0]))

        ang = elevation_angle(SUCCESS, 0.66)
        th_lbl = mtx(r"\theta", 44, SUCCESS).move_to(
            OBS + np.array([-0.92, 0.30, 0.0]))

        vA = mtx(r"A", 34, INK).move_to(FOOT + np.array([-0.34, -0.30, 0.0]))
        vB = mtx(r"B", 34, INK).move_to(OBS + np.array([0.10, -0.36, 0.0]))
        vC = mtx(r"C", 34, INK).move_to(TOP + np.array([-0.36, 0.26, 0.0]))
        name = mtx(r"\triangle ABC", 44, INK).move_to(np.array([2.9, 1.9, 0.0]))

        legend = VGroup(
            mtx(r"h \;=\; AC", 34, ACCENT),
            mtx(r"d \;=\; AB", 34, VIOLET),
            mtx(r"\angle A = 90^\circ", 34, MUTED),
            mtx(r"\angle B = \theta", 34, SUCCESS),
        ).arrange(DOWN, buff=0.46, aligned_edge=LEFT).move_to(np.array([3.0, -0.5, 0.0]))

        with self.voiceover(text=NARRATION["triangle"]):
            self.play(FadeIn(tower), FadeIn(man), Create(sight), run_time=3.2)
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(
                tower.animate.set_opacity(0.25),
                Create(side_h), FadeIn(h_lbl, shift=RIGHT * 0.2),
                FadeIn(vA), FadeIn(vC), FadeIn(legend[0]),
                run_time=4.0,
            )
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(Create(side_d), FadeIn(d_lbl, shift=UP * 0.2),
                      FadeIn(vB), FadeIn(legend[1]), run_time=3.2)
            self.play(ReplacementTransform(sight, side_s), run_time=4.0)
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(Create(rang), FadeIn(rang_lbl), FadeIn(legend[2]),
                      run_time=4.0)
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(Create(ang), FadeIn(th_lbl, scale=0.6), FadeIn(legend[3]),
                      run_time=2.1)
            self.play(Write(name), Circumscribe(legend, color=INK, buff=0.30),
                      run_time=1.5)
        # beats sized to the sentences they illustrate
        # 3.2+4.0+3.2+4.0+4.0+2.1+1.5 = 22.0 s

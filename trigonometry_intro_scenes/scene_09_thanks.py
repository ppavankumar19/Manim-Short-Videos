from common import *


class Scene09Thanks(VoiceoverScene):
    """Sign off — no poster, just the closing card."""

    def construct(self):
        self.set_speech_service(scene_speech_service("thanks"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(lesson_backdrop())

        got = heading("Now you know!", SUCCESS, 54)
        word = txt("trigonometry  =  measuring triangles", 34, INK)

        shape, mark, verts = right_triangle(np.array([-1.25, -0.80, 0.0]),
                                            2.50, 1.85, ACCENT, 0.14, 7.0)
        corners = VGroup(*[Dot(p, color=AMBER, radius=0.10) for p in verts])
        badge = VGroup(shape, mark, corners)

        thanks = heading("Thanks for watching!", ACCENT, 46)

        block = VGroup(got, word, badge, thanks).arrange(DOWN, buff=0.50)
        block.move_to(ORIGIN)

        stars = VGroup(*[
            Star(n=5, outer_radius=0.17, color=AMBER, fill_opacity=0.9,
                 stroke_width=0).move_to(np.array([sx * x, y, 0.0]))
            for x, y in ((5.95, 2.55), (6.35, 0.15), (5.60, -2.55))
            for sx in (-1, 1)
        ])

        with self.voiceover(text=NARRATION["thanks"]):
            self.add_sound(self.sfx["success"], gain=-12)
            self.play(FadeIn(got, scale=0.75),
                      LaggedStart(*[SpinInFromNothing(s) for s in stars],
                                  lag_ratio=0.10),
                      run_time=2.21)
            self.play(FadeIn(word), DrawBorderThenFill(shape),
                      FadeIn(corners), run_time=3.13)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.play(FadeIn(thanks, shift=UP * 0.2), run_time=2.95)
            self.play(Circumscribe(badge, color=AMBER, buff=0.22),
                      run_time=2.76)
        # 2.21+3.13+2.95+2.76+0.74 = 11.79 s

        self.wait(END_HOLD)
        self.play(FadeOut(VGroup(block, stars)), run_time=0.74)

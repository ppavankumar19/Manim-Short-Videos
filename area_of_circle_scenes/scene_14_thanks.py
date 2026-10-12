from common import *


class Scene14Thanks(VoiceoverScene):
    """Sign off, then hand over to the closing poster."""

    def construct(self):
        self.set_speech_service(scene_speech_service("thanks"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(lesson_backdrop())

        done = heading("You did it!", SUCCESS, 56)
        solved = txt("a 2000-year-old puzzle, solved", 30, MUTED)

        # The ring is sized from the formula it holds, so the text can never
        # poke out of it however the font happens to render.
        formula = mtx(r"A \;=\; \pi r^2", 66, AMBER)
        ring = Circle(radius=max(formula.width, formula.height) / 2 + 0.62,
                      stroke_color=VIOLET, stroke_width=6,
                      stroke_opacity=0.55, fill_opacity=0)
        formula.move_to(ring.get_center())
        medal = VGroup(ring, formula)

        # one balanced column, centred in the frame
        block = VGroup(done, solved, medal).arrange(DOWN, buff=0.50)
        block.move_to(ORIGIN)

        # stars in mirrored pairs down both edges, clear of the column
        stars = VGroup(*[
            Star(n=5, outer_radius=0.17, color=AMBER, fill_opacity=0.9,
                 stroke_width=0).move_to(np.array([sx * x, y, 0.0]))
            for x, y in ((5.85, 2.60), (6.30, 0.20), (5.55, -2.60))
            for sx in (-1, 1)
        ])
        opening = VGroup(block, stars)

        # The closing card the lesson hands over to.  It already carries
        # "Thanks for watching", so nothing of ours is drawn on top of it.
        poster = ImageMobject(os.path.join(IMAGES_DIR, "area_of_circle.png"))
        poster.set(width=13.4)
        poster.move_to(ORIGIN)
        poster.set_opacity(0.0)

        with self.voiceover(text=NARRATION["thanks"]):
            self.add_sound(self.sfx["success"], gain=-12)
            self.play(FadeIn(done, scale=0.7),
                      LaggedStart(*[SpinInFromNothing(s) for s in stars],
                                  lag_ratio=0.10),
                      run_time=1.74)
            self.play(FadeIn(solved), Write(formula), Create(ring),
                      run_time=3.94)
            self.play(Circumscribe(formula, color=AMBER, buff=0.25),
                      run_time=2.19)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.add(poster)
            self.play(
                FadeOut(opening),
                poster.animate.set_opacity(1.0),
                run_time=3.93,
            )
            self.play(poster.animate.scale(1.035), run_time=2.62,
                      rate_func=rate_functions.ease_out_sine)
        # 1.74+3.94+2.19+3.93+2.62 = 14.42 s

        self.wait(END_HOLD)
        self.play(FadeOut(poster), run_time=0.96)

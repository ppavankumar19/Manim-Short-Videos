from common import *


class Scene00Intro(VoiceoverScene):
    """Why quadrilaterals: four of them from an ordinary room."""

    def construct(self):
        self.set_speech_service(scene_speech_service("intro"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(paper_backdrop())

        win = window_frame(np.array([-4.55, 1.25, 0.0]), 2.35, 2.85)
        kite = kite_shape(np.array([-1.30, 1.35, 0.0]), 1.95, 2.60)
        tiles = tile_floor(np.array([1.85, 1.30, 0.0]), 4, 3, 0.62)
        field = field_plot(np.array([4.85, 1.30, 0.0]), 2.70, 1.80)
        things = [win, kite, tiles, field]

        # the four-sided skeleton hiding inside each everyday object
        outlines = VGroup(
            Polygon(*[np.array([-4.55, 1.25, 0.0]) + np.array(v)
                      for v in ([-1.17, -1.42, 0], [1.17, -1.42, 0],
                                [1.17, 1.42, 0], [-1.17, 1.42, 0])],
                    stroke_color=AMBER, stroke_width=5, fill_opacity=0),
            Polygon(*[np.array([-1.30, 1.35, 0.0]) + np.array(v)
                      for v in ([0, 1.43, 0], [0.975, 0.31, 0],
                                [0, -1.17, 0], [-0.975, 0.31, 0])],
                    stroke_color=AMBER, stroke_width=5, fill_opacity=0),
            # one tile, traced from the tile itself so the outline lands
            # exactly on it
            tiles[0][5].copy().set_stroke(AMBER, 5).set_fill(opacity=0),
            field[0].copy().set_stroke(AMBER, 5).set_fill(opacity=0),
        )

        # symbols only: a quadrilateral is four labelled corners
        count = mtx(r"\square \;\equiv\; \{A,B,C,D\}", 44, AMBER)
        count.move_to(np.array([0.0, -1.60, 0.0]))

        question = mtx(r"\triangle \;\ne\; \square", 62, INK)
        question.move_to(np.array([0.0, -2.85, 0.0]))
        spark = mtx(r"\square \;\longrightarrow\; ?", 56, ROSE)
        spark.move_to(np.array([0.0, -2.85, 0.0]))

        with self.voiceover(text=NARRATION["intro"]):
            self.add_sound(self.sfx["whoosh"], gain=-16)
            self.play(
                LaggedStart(*[FadeIn(t, shift=DOWN * 0.35) for t in things],
                            lag_ratio=0.30),
                run_time=6.0,
            )
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(
                LaggedStart(*[Create(o) for o in outlines], lag_ratio=0.28),
                run_time=6.0,
            )
            self.add_sound(self.sfx["pop"], gain=-16)
            self.play(
                FadeIn(count, shift=UP * 0.25),
                LaggedStart(*[Indicate(o, color=AMBER, scale_factor=1.06)
                              for o in outlines], lag_ratio=0.18),
                run_time=4.0,
            )
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(Write(question), run_time=2.4)
            self.play(TransformMatchingTex(question, spark), run_time=1.8)
            self.play(
                FadeOut(VGroup(*things, outlines, count, spark)),
                run_time=1.8,
            )
        # beats sized to the sentences they illustrate
        # 6.0+6.0+4.0+2.4+1.8+1.8 = 22.0 s

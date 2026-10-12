from common import *

# A tiny stand-in quadrilateral, big enough to point at, small enough to sit
# beside the arithmetic.
Q = [np.array([-4.35, -1.60, 0.0]), np.array([-1.55, -1.85, 0.0]),
     np.array([-1.05, 1.05, 0.0]), np.array([-4.05, 1.55, 0.0])]


class Scene04Count(VoiceoverScene):
    """Why exactly five numbers: 4 x 2 - 3 = 5, counted on screen."""

    def construct(self):
        self.set_speech_service(scene_speech_service("count"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(paper_backdrop())

        quad = Polygon(*Q, stroke_color=ACCENT, stroke_width=5,
                       fill_color=ACCENT, fill_opacity=0.10)
        dots = VGroup(*[Dot(p, color=AMBER, radius=0.10) for p in Q])
        coords = VGroup(*[
            mtx(rf"(x_{i+1}, y_{i+1})", 24, MUTED).next_to(
                Dot(p), d, buff=0.20)
            for i, (p, d) in enumerate(zip(Q, (DL, DR, UR, UL)))
        ])

        # --- the count, line by line ----------------------------------------
        c1 = mtx(r"4 \times (x,y) \;=\; 8", 48, AMBER)
        c2 = mtx(r"-\,2 \quad \longleftrightarrow", 44, MUTED)
        c3 = mtx(r"-\,1 \quad \circlearrowleft", 44, MUTED)
        c4 = mtx(r"8 \;-\; 3 \;=\; \mathbf{5}", 56, SUCCESS)
        lines = VGroup(c1, c2, c3, c4).arrange(DOWN, buff=0.52,
                                               aligned_edge=LEFT)
        lines.move_to(np.array([2.85, 0.55, 0.0]))
        box = SurroundingRectangle(c4, color=SUCCESS, buff=0.26,
                                   corner_radius=0.12)
        verdict = mtx(r"5 \;\longleftrightarrow\; \square", 44, AMBER)
        verdict.move_to(np.array([2.85, -2.60, 0.0]))

        # the two motions that cost nothing
        shifted = Polygon(*[p + np.array([0.55, -0.30, 0.0]) for p in Q],
                          stroke_color=MUTED, stroke_width=3,
                          stroke_opacity=0.55, fill_opacity=0)
        turned = Polygon(*Q, stroke_color=MUTED, stroke_width=3,
                         stroke_opacity=0.55, fill_opacity=0)
        turned.rotate(28 * DEGREES, about_point=quad.get_center())

        with self.voiceover(text=NARRATION["count"]):
            self.play(Create(quad),
                      LaggedStart(*[GrowFromCenter(d) for d in dots],
                                  lag_ratio=0.18),
                      run_time=2.25)
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(
                LaggedStart(*[FadeIn(c, scale=0.7) for c in coords],
                            lag_ratio=0.22),
                Write(c1),
                run_time=3.6,
            )
            self.add_sound(self.sfx["whoosh"], gain=-18)
            self.play(FadeIn(shifted), FadeIn(c2, shift=RIGHT * 0.2),
                      run_time=4.29)
            self.play(FadeIn(turned), FadeIn(c3, shift=RIGHT * 0.2),
                      run_time=4.26)
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(
                FadeOut(VGroup(shifted, turned)),
                TransformFromCopy(VGroup(c1, c2, c3), c4),
                run_time=2.25,
            )
            self.play(Create(box), FadeIn(verdict, shift=UP * 0.15),
                      Flash(c4.get_center(), color=SUCCESS, flash_radius=1.3,
                            num_lines=14),
                      run_time=3.6)
            self.play(
                FadeOut(VGroup(quad, dots, coords, lines, box, verdict)),
                run_time=2.25,
            )
        # beats sized to the sentences they illustrate
        # 2.25+3.6+4.29+4.26+2.25+3.6+2.25 = 22.5 s

from common import *

# One vertex, two rays, two cuts: the classic similar-triangle picture that
# explains why h/d cannot depend on how far away you stand.
TH_S = 48 * DEGREES
B_S = np.array([3.85, -2.40, 0.0])
D1, D2S = 1.85, 3.15
A1 = B_S + LEFT * D1
A2 = B_S + LEFT * D2S
C1 = A1 + UP * (D1 * np.tan(TH_S))
C2 = A2 + UP * (D2S * np.tan(TH_S))


class Scene06Similar(VoiceoverScene):
    """Same theta, two sizes — the ratio refuses to change."""

    def construct(self):
        self.set_speech_service(scene_speech_service("similar"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(blueprint_grid())

        ground = Line(B_S + RIGHT * 0.5, A2 + LEFT * 0.9,
                      stroke_color=MUTED, stroke_width=4)
        ray = Line(B_S, C2 + (C2 - B_S) * 0.10, stroke_color=AMBER,
                   stroke_width=4)
        ang = Angle(Line(B_S, A2), Line(B_S, C2), radius=0.72, color=SUCCESS,
                    stroke_width=5, other_angle=True)
        th_lbl = mtx(r"\theta", 42, SUCCESS).move_to(B_S + np.array([-1.02, 0.30, 0.0]))
        b_lbl = mtx(r"B", 32, INK).move_to(B_S + np.array([0.28, -0.28, 0.0]))

        tri1 = Polygon(B_S, A1, C1, stroke_color=ACCENT, stroke_width=5,
                       fill_color=ACCENT, fill_opacity=0.15)
        h1 = Line(A1, C1, stroke_color=ACCENT, stroke_width=6)
        h1_lbl = mtx(r"h_1", 34, ACCENT).next_to(h1, LEFT, buff=0.16)
        d1_br = BraceBetweenPoints(B_S, A1, direction=DOWN, color=ACCENT)
        d1_lbl = mtx(r"d_1", 32, ACCENT).next_to(d1_br, DOWN, buff=0.12)

        tri2 = Polygon(B_S, A2, C2, stroke_color=VIOLET, stroke_width=5,
                       fill_color=VIOLET, fill_opacity=0.10)
        h2 = Line(A2, C2, stroke_color=VIOLET, stroke_width=6)
        h2_lbl = mtx(r"h_2", 34, VIOLET).next_to(h2, LEFT, buff=0.16)
        d2_br = BraceBetweenPoints(B_S, A2, direction=DOWN, color=VIOLET)
        d2_lbl = mtx(r"d_2", 32, VIOLET).next_to(d2_br, DOWN, buff=0.12)
        d2_br.shift(DOWN * 0.62)
        d2_lbl.shift(DOWN * 0.62)

        sim = mtx(r"\triangle BA_1C_1 \;\sim\; \triangle BA_2C_2", 40, INK)
        sim.move_to(np.array([-3.30, 2.85, 0.0]))
        ratio = mtx(r"\frac{h_1}{d_1} \;=\; \frac{h_2}{d_2} \;=\; \tan\theta",
                    48, AMBER).move_to(np.array([-3.30, 1.20, 0.0]))
        ratio_box = SurroundingRectangle(ratio, color=AMBER, buff=0.26,
                                         corner_radius=0.12)
        # theta decides tan(theta); d has no say — stated in symbols only
        only = mtx(r"\theta \;\mapsto\; \tan\theta \qquad d \;\not\mapsto\; \tan\theta",
                   32, SUCCESS).move_to(np.array([-3.30, -0.45, 0.0]))

        with self.voiceover(text=NARRATION["similar"]):
            self.play(Create(ground), Create(ray), Create(ang), FadeIn(th_lbl),
                      FadeIn(b_lbl), run_time=3.0)
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(FadeIn(tri1), Create(h1), FadeIn(h1_lbl),
                      GrowFromCenter(d1_br), FadeIn(d1_lbl), run_time=1.1)
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(FadeIn(tri2), Create(h2), FadeIn(h2_lbl),
                      GrowFromCenter(d2_br), FadeIn(d2_lbl), run_time=1.5)
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(
                Write(sim),
                Indicate(ang, color=SUCCESS, scale_factor=1.25),
                run_time=3.6,
            )
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(Write(ratio), Create(ratio_box), run_time=6.0)
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(FadeIn(only, shift=UP * 0.2), run_time=2.4)
            self.play(
                FadeOut(VGroup(ground, ray, ang, th_lbl, b_lbl, tri1, h1,
                               h1_lbl, d1_br, d1_lbl, tri2, h2, h2_lbl, d2_br,
                               d2_lbl, sim, ratio, ratio_box, only)),
                run_time=3.4,
            )
        # beats sized to the sentences they illustrate
        # 3.0+1.1+1.5+3.6+6.0+2.4+3.4 = 21.0 s

from common import *

# Left half carries the picture, right half the algebra, so the student can
# see *which* part of the triangle each rearrangement is talking about.
A7 = np.array([-5.05, -2.20, 0.0])
D7 = 2.20
B7 = A7 + RIGHT * D7
C7 = A7 + UP * (D7 * np.tan(58 * DEGREES))


class Scene07Formal(VoiceoverScene):
    """Two lines of algebra, tied at every step to the side they move."""

    def construct(self):
        self.set_speech_service(scene_speech_service("formal"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(blueprint_grid())

        # --- the picture: d and theta known, h still a question -------------
        base = Line(A7, B7, stroke_color=VIOLET, stroke_width=7)
        sight = Line(B7, C7, stroke_color=AMBER, stroke_width=5)
        rise = DashedLine(A7, C7, stroke_color=ACCENT, stroke_width=6,
                          dash_length=0.16)
        rise_solid = Line(A7, C7, stroke_color=ACCENT, stroke_width=8)
        face = Polygon(A7, B7, C7, stroke_width=0, fill_color=ACCENT,
                       fill_opacity=0.10)
        rang = RightAngle(Line(A7, B7), Line(A7, C7), length=0.30, color=MUTED,
                          stroke_width=3)
        ang = Angle(Line(B7, A7), Line(B7, C7), radius=0.58, color=SUCCESS,
                    stroke_width=5, other_angle=True)
        th_lbl = mtx(r"\theta", 38, SUCCESS).move_to(B7 + np.array([-0.92, 0.26, 0.0]))
        d_lbl = mtx(r"d", 38, VIOLET).move_to((A7 + B7) / 2 + DOWN * 0.42)
        h_q = mtx(r"h = \;?", 38, AMBER).move_to((A7 + C7) / 2 + LEFT * 0.72)
        h_ok = mtx(r"h", 44, ACCENT).move_to((A7 + C7) / 2 + LEFT * 0.52)
        picture = VGroup(face, base, sight, rise, rang, ang, th_lbl, d_lbl)

        # --- the algebra ----------------------------------------------------
        e1 = MathTex(r"\tan\theta", r"=", r"\frac{h}{d}",
                     font_size=60, color=INK).move_to(np.array([2.55, 1.85, 0.0]))
        e1[0].set_color(SUCCESS)
        e1[2].set_color(ACCENT)

        step = mtx(r"\big(\;\cdot\; d\;\big)", 34, MUTED)
        step.move_to(np.array([2.55, 0.62, 0.0]))
        step_arrow = Arrow(np.array([1.35, 0.62, 0.0]), np.array([1.35, -0.32, 0.0]),
                           color=MUTED, stroke_width=3, buff=0.05,
                           max_tip_length_to_length_ratio=0.28)

        e2 = MathTex(r"d\,\tan\theta", r"=", r"h",
                     font_size=60, color=INK).move_to(np.array([2.55, -0.75, 0.0]))
        e2[0].set_color(SUCCESS)
        e2[2].set_color(ACCENT)

        e3 = MathTex(r"h", r"=", r"d\,\tan\theta",
                     font_size=64, color=SUCCESS).move_to(np.array([2.55, -0.75, 0.0]))
        box = SurroundingRectangle(e3, color=AMBER, buff=0.30, corner_radius=0.14)

        known = mtx(r"d,\;\theta \;\Longrightarrow\; h", 40, AMBER)
        known.move_to(np.array([2.55, -2.55, 0.0]))

        with self.voiceover(text=NARRATION["formal"]):
            self.play(
                FadeIn(face), Create(base), Create(sight), Create(rang),
                Create(ang), FadeIn(th_lbl), FadeIn(d_lbl),
                Create(rise), FadeIn(h_q),
                run_time=2.9,
            )
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(Write(e1), Indicate(ang, color=SUCCESS, scale_factor=1.25),
                      run_time=4.9)
            self.play(
                FadeIn(step, shift=DOWN * 0.15), GrowArrow(step_arrow),
                TransformFromCopy(e1, e2),
                Indicate(base, color=VIOLET, scale_factor=1.06),
                run_time=4.1,
            )
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(TransformMatchingTex(e2, e3),
                      FadeOut(VGroup(step, step_arrow)),
                      ReplacementTransform(rise, rise_solid),
                      ReplacementTransform(h_q, h_ok),
                      run_time=4.0,
            )
            self.play(Create(box), FadeIn(known, shift=UP * 0.15),
                      Flash(e3.get_center(), color=AMBER, flash_radius=1.2,
                            num_lines=14),
                      run_time=3.0)
            self.play(
                FadeOut(VGroup(picture, rise_solid, h_ok, e1, e3, box, known)),
                run_time=1.1,
            )
        # beats sized to the sentences they illustrate
        # 2.9+4.9+4.1+4.0+3.0+1.1 = 20.0 s

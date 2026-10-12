from common import *

A2 = np.array([-4.90, -2.30, 0.0])      # right-angle corner
D2 = 2.55                                # d, held fixed all through
B2 = A2 + RIGHT * D2                     # the observer's corner


class Scene05Ratio(VoiceoverScene):
    """Open theta, watch h climb, and watch h/d settle on one number."""

    def construct(self):
        self.set_speech_service(scene_speech_service("ratio"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(blueprint_grid())

        th = ValueTracker(25 * DEGREES)

        def apex():
            return A2 + UP * (D2 * np.tan(th.get_value()))

        base = Line(A2, B2, stroke_color=VIOLET, stroke_width=7)
        d_brace = BraceBetweenPoints(B2, A2, direction=DOWN, color=MUTED)
        d_lbl = mtx(r"d", 40, VIOLET).next_to(d_brace, DOWN, buff=0.16)
        # "d never changes", said without a word of English
        d_fix = mtx(r"\Delta d = 0", 30, MUTED).next_to(d_lbl, DOWN, buff=0.22)

        rise = always_redraw(lambda: Line(A2, apex(), stroke_color=ACCENT,
                                          stroke_width=7))
        sight = always_redraw(lambda: Line(B2, apex(), stroke_color=AMBER,
                                           stroke_width=5))
        face = always_redraw(lambda: Polygon(A2, B2, apex(), stroke_width=0,
                                             fill_color=ACCENT, fill_opacity=0.12))
        apex_dot = always_redraw(lambda: Dot(apex(), color=ACCENT, radius=0.075))
        arc = always_redraw(lambda: Angle(Line(B2, A2), Line(B2, apex()),
                                          radius=0.60, color=SUCCESS,
                                          stroke_width=5, other_angle=True))
        h_lbl = always_redraw(
            lambda: mtx(r"h", 40, ACCENT).move_to(
                A2 + UP * (D2 * np.tan(th.get_value())) / 2 + LEFT * 0.36))
        rang = RightAngle(Line(A2, B2), Line(A2, A2 + UP), length=0.30,
                          color=MUTED, stroke_width=3)

        # --- live readout -------------------------------------------------
        th_eq = mtx(r"\theta \;=", 42, SUCCESS).move_to(np.array([1.55, 1.75, 0.0]))
        th_num = DecimalNumber(25.0, num_decimal_places=1, font_size=42,
                               color=SUCCESS)
        th_num.add_updater(lambda m: m.set_value(th.get_value() / DEGREES)
                           .next_to(th_eq, RIGHT, buff=0.24))
        th_deg = mtx(r"^\circ", 42, SUCCESS)
        th_deg.add_updater(lambda m: m.next_to(th_num, RIGHT, buff=0.04)
                           .align_to(th_num, UP))

        r_eq = mtx(r"\frac{h}{d} \;=", 44, ACCENT).move_to(np.array([1.55, 0.20, 0.0]))
        r_num = DecimalNumber(0.466, num_decimal_places=3, font_size=42,
                              color=ACCENT)
        r_num.add_updater(lambda m: m.set_value(np.tan(th.get_value()))
                          .next_to(r_eq, RIGHT, buff=0.26))

        law = mtx(r"\frac{h}{d} \;=\; \tan\theta", 52, AMBER)
        law.move_to(np.array([2.35, -1.65, 0.0]))
        law_box = SurroundingRectangle(law, color=AMBER, buff=0.28,
                                       corner_radius=0.12)
        at60 = mtx(r"\tan 60^\circ = \sqrt{3} \approx 1.732", 34, SUCCESS)
        at60.move_to(np.array([2.35, -2.85, 0.0]))

        with self.voiceover(text=NARRATION["ratio"]):
            self.play(Create(base), GrowFromCenter(d_brace), FadeIn(d_lbl),
                      FadeIn(d_fix), FadeIn(rang), run_time=3.35)
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(
                Create(rise), Create(sight), FadeIn(face), FadeIn(apex_dot),
                Create(arc), FadeIn(h_lbl),
                FadeIn(th_eq), FadeIn(th_num), FadeIn(th_deg),
                FadeIn(r_eq), FadeIn(r_num),
                run_time=2.0,
            )
            self.add_sound(self.sfx["whoosh"], gain=-17)
            self.play(th.animate.set_value(62 * DEGREES), run_time=4.3,
                      rate_func=rate_functions.ease_in_out_sine)
            self.play(th.animate.set_value(38 * DEGREES), run_time=4.2,
                      rate_func=rate_functions.ease_in_out_sine)
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(th.animate.set_value(60 * DEGREES), run_time=7.05,
                      rate_func=rate_functions.ease_in_out_sine)
            self.play(
                Write(law), Create(law_box), FadeIn(at60),
                # r_num rebuilds itself every frame, so flash its label instead
                Indicate(r_eq, color=AMBER, scale_factor=1.3),
                run_time=3.0,
            )
            self.play(
                FadeOut(VGroup(base, d_brace, d_lbl, d_fix, rise, sight, face,
                               apex_dot, arc, h_lbl, rang, th_eq, th_num,
                               th_deg, r_eq, r_num, law, law_box, at60)),
                run_time=2.1,
            )
        # beats sized to the sentences they illustrate
        # 3.35+2.0+4.3+4.2+7.05+3.0+2.1 = 26.0 s

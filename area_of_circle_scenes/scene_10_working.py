from common import *


class Scene10Working(VoiceoverScene):
    """Given the distance around, find r — and draw r while we find it."""

    def construct(self):
        self.set_speech_service(scene_speech_service("working"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(lesson_backdrop())

        C = np.array([-3.7, 0.35, 0.0])
        RAD = 1.55
        EDGE = C + RIGHT * RAD

        circ = Circle(radius=RAD, stroke_color=ACCENT, stroke_width=7,
                      fill_color=ACCENT, fill_opacity=0.10).move_to(C)
        centre = Dot(C, color=AMBER, radius=0.085)
        rim = Circle(radius=RAD, stroke_color=ROSE, stroke_width=9,
                     fill_opacity=0).move_to(C)
        given = mtx(r"22\,\text{cm}", 40, ROSE).next_to(circ, DOWN, buff=0.40)
        g_cap = txt("all the way around", 26, MUTED).next_to(given, DOWN, buff=0.18)
        want = mtx(r"A \;=\; ?", 44, AMBER).next_to(circ, UP, buff=0.45)

        # The radius is drawn while it is still unknown, then filled in with
        # its value the moment the arithmetic produces it.
        r_dash = DashedLine(C, EDGE, stroke_color=AMBER, stroke_width=7,
                            dash_length=0.13)
        r_tip = Dot(EDGE, color=AMBER, radius=0.075)
        r_q = chip(mtx(r"r \;=\; ?", 34, AMBER)
                   .next_to(Line(C, EDGE), UP, buff=0.34))
        r_solid = Line(C, EDGE, stroke_color=SUCCESS, stroke_width=9)
        r_val = chip(mtx(r"3.5\,\text{cm}", 34, SUCCESS)
                     .next_to(Line(C, EDGE), UP, buff=0.34))

        steps = VGroup(
            mtx(r"2 \pi r \;=\; 22", 44, INK),
            mtx(r"2 \times \tfrac{22}{7} \times r \;=\; 22", 44, INK),
            mtx(r"r \;=\; 3.5\,\text{cm}", 50, SUCCESS),
        ).arrange(DOWN, buff=0.70, aligned_edge=LEFT)
        steps.move_to(np.array([2.9, 0.30, 0.0]))
        box = SurroundingRectangle(steps[2], color=SUCCESS, buff=0.26,
                                   corner_radius=0.14)
        need = txt("first, find r", 32, AMBER).next_to(steps, UP, buff=0.55)

        with self.voiceover(text=NARRATION["working"]):
            self.play(FadeIn(circ), GrowFromCenter(centre), run_time=1.67)
            self.add_sound(self.sfx["whoosh"], gain=-17)
            self.play(Create(rim), FadeIn(given), FadeIn(g_cap), run_time=5.8)
            self.play(FadeIn(want, scale=0.7), run_time=2.09)
            # "first we need r" — so here is r, drawn but not yet known
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(Create(r_dash), FadeIn(r_tip), FadeIn(r_q),
                      FadeIn(need, shift=DOWN * 0.2), run_time=1.67)
            self.add_sound(self.sfx["click"], gain=-17)
            # 2 pi r ties the rim to the radius, so flash both together
            self.play(Write(steps[0]),
                      Indicate(rim, color=ROSE, scale_factor=1.04),
                      Indicate(r_dash, color=AMBER, scale_factor=1.08),
                      run_time=2.93)
            self.play(TransformFromCopy(steps[0], steps[1]), run_time=2.93)
            self.play(Indicate(steps[1], color=AMBER, scale_factor=1.06),
                      run_time=2.93)
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(FadeIn(steps[2], shift=UP * 0.2), run_time=1.26)
            self.add_sound(self.sfx["ding"], gain=-14)
            # the unknown radius becomes a measured one
            self.play(
                ReplacementTransform(r_dash, r_solid),
                ReplacementTransform(r_q, r_val),
                r_tip.animate.set_color(SUCCESS),
                Create(box),
                Flash(EDGE, color=SUCCESS, flash_radius=0.55, num_lines=12),
                run_time=2.77,
            )
        # 1.67+5.8+2.09+1.67+2.93+2.93+2.93+1.26+2.77 = 24.05 s

        self.play(FadeOut(VGroup(circ, centre, rim, given, g_cap, want,
                                 r_solid, r_tip, r_val, steps, box, need)),
                  run_time=0.52)

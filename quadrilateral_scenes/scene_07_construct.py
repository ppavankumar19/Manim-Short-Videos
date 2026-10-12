from common import *

# The real thing: ruler down, two arcs swung, C where they cross.
OFF = np.array([-1.35, -1.55, 0.0])
A7, B7, C7, D7 = [p + OFF for p in (A, B, C, D)]
R_A = AC * SCALE
R_B = BC * SCALE


class Scene07Construct(VoiceoverScene):
    """Ruler and compass, at the exact solved coordinates."""

    def construct(self):
        self.set_speech_service(scene_speech_service("construct"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(paper_backdrop())

        steps = VGroup(
            mtx(r"1)\;\; AB \;=\; 4.5", 32, ACCENT),
            mtx(r"2)\;\; \odot(A,\,5.0)", 32, VIOLET),
            mtx(r"3)\;\; \odot(B,\,5.2)", 32, AMBER),
            mtx(r"4)\;\; C \;=\; \odot \cap \odot", 32, SUCCESS),
        ).arrange(DOWN, buff=0.46, aligned_edge=LEFT)
        steps.move_to(np.array([4.05, 1.85, 0.0]))

        rule_bar = ruler(A7, B7)
        base = Line(A7, B7, stroke_color=ACCENT, stroke_width=7)
        l_ab = side_label(A7, B7, "4.5", ACCENT, 26, out=DOWN, buff=0.34)
        vA = vertex(A7, "A", DOWN + LEFT * 0.4)
        vB = vertex(B7, "B", DOWN + RIGHT * 0.4)

        # The compass is set to the arc's own radius and starts at the arc's
        # own start angle, so rotating it about the needle traces the arc.
        SWEEP = 62 * DEGREES
        ang_a = float(np.arctan2(*(C7 - A7)[1::-1])) - SWEEP / 2
        ang_b = float(np.arctan2(*(C7 - B7)[1::-1])) - SWEEP / 2
        arc_a = arc_from(A7, R_A, C7, SWEEP, VIOLET, 3.5)
        arc_b = arc_from(B7, R_B, C7, SWEEP, AMBER, 3.5)
        comp_a = compass(A7, R_A, ang_a, VIOLET, 0.9)
        comp_b = compass(B7, R_B, ang_b, AMBER, 0.9)

        vC = vertex(C7, "C", UP)
        s_ac = Line(A7, C7, stroke_color=VIOLET, stroke_width=6)
        s_bc = Line(B7, C7, stroke_color=AMBER, stroke_width=6)
        l_ac = mtx("5", 26, VIOLET).move_to((A7 + C7) / 2 + np.array([-0.38, 0.0, 0.0]))
        l_bc = mtx("5.2", 26, AMBER).move_to((B7 + C7) / 2 + np.array([0.44, 0.0, 0.0]))
        face = Polygon(A7, B7, C7, stroke_width=0, fill_color=SUCCESS,
                       fill_opacity=0.13)
        name = mtx(r"\triangle ABC \;\checkmark", 38, SUCCESS)
        name.move_to(np.array([4.05, -2.35, 0.0]))

        with self.voiceover(text=NARRATION["construct"]):
            self.add_sound(self.sfx["swipe"], gain=-17)
            self.play(FadeIn(rule_bar, shift=DOWN * 0.4), FadeIn(steps[0]),
                      run_time=2.36)
            self.play(Create(base), FadeIn(vA), FadeIn(vB), FadeIn(l_ab),
                      rule_bar.animate.shift(DOWN * 1.30).set_opacity(0.0),
                      run_time=3.93)
            self.add_sound(self.sfx["whoosh"], gain=-17)
            self.play(FadeIn(comp_a), FadeIn(steps[1]), run_time=1.5)
            self.play(Create(arc_a), Rotate(comp_a, SWEEP, about_point=A7),
                      run_time=4.39)
            self.add_sound(self.sfx["whoosh"], gain=-17)
            self.play(FadeOut(comp_a), FadeIn(comp_b), FadeIn(steps[2]),
                      run_time=1.4)
            self.play(Create(arc_b), Rotate(comp_b, SWEEP, about_point=B7),
                      run_time=3.31)
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(FadeOut(comp_b), FadeIn(vC, scale=0.5),
                      FadeIn(steps[3]),
                      Flash(C7, color=SUCCESS, flash_radius=0.65,
                            num_lines=14),
                      run_time=2.0)
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(Create(s_ac), Create(s_bc), FadeIn(l_ac), FadeIn(l_bc),
                      FadeIn(face), FadeIn(name), run_time=2.3)
            self.play(FadeOut(VGroup(arc_a, arc_b)), run_time=0.81)
        # beats sized to the sentences they illustrate
        # 2.36+3.93+1.5+4.39+1.4+3.31+2.0+2.3+0.81 = 22.0 s

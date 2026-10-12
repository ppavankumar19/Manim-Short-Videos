from common import *

# Continues straight on from scene 07: same offset, same triangle, so the
# cut is invisible and the construction simply carries on.
OFF = np.array([-1.35, -1.55, 0.0])
A8, B8, C8, D8 = [p + OFF for p in (A, B, C, D)]
R_B = BD * SCALE
R_C = CD * SCALE


class Scene08Locate(VoiceoverScene):
    """The last corner, from the two measurements nobody has used yet."""

    def construct(self):
        self.set_speech_service(scene_speech_service("locate"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(paper_backdrop())

        # --- carried over from the previous beat -----------------------------
        base = Line(A8, B8, stroke_color=ACCENT, stroke_width=7)
        s_ac = Line(A8, C8, stroke_color=VIOLET, stroke_width=6)
        s_bc = Line(B8, C8, stroke_color=AMBER, stroke_width=6)
        face = Polygon(A8, B8, C8, stroke_width=0, fill_color=SUCCESS,
                       fill_opacity=0.13)
        vA = vertex(A8, "A", DOWN + LEFT * 0.4)
        vB = vertex(B8, "B", DOWN + RIGHT * 0.4)
        vC = vertex(C8, "C", UP)
        carried = VGroup(face, base, s_ac, s_bc, vA, vB, vC)
        self.add(carried)

        left = VGroup(
            mtx(r"5)\;\; \odot(B,\,5.4)", 32, AMBER),
            mtx(r"6)\;\; \odot(C,\,4.8)", 32, ROSE),
            mtx(r"7)\;\; D \;=\; \odot \cap \odot", 32, SUCCESS),
        ).arrange(DOWN, buff=0.46, aligned_edge=LEFT)
        left.move_to(np.array([4.05, 1.85, 0.0]))

        SW_B, SW_C = 46 * DEGREES, 54 * DEGREES
        ang_b = float(np.arctan2(*(D8 - B8)[1::-1])) - SW_B / 2
        ang_c = float(np.arctan2(*(D8 - C8)[1::-1])) - SW_C / 2
        arc_b = arc_from(B8, R_B, D8, SW_B, AMBER, 3.5)
        arc_c = arc_from(C8, R_C, D8, SW_C, ROSE, 3.5)
        comp_b = compass(B8, R_B, ang_b, AMBER, 0.9)
        comp_c = compass(C8, R_C, ang_c, ROSE, 0.9)

        vD = vertex(D8, "D", LEFT + UP * 0.25)
        s_bd = Line(B8, D8, stroke_color=AMBER, stroke_width=5)
        s_cd = Line(C8, D8, stroke_color=ROSE, stroke_width=6)
        s_ad = Line(A8, D8, stroke_color=ACCENT, stroke_width=6)
        l_bd = mtx("5.4", 24, AMBER).move_to((B8 + D8) / 2 + np.array([0.05, 0.34, 0.0]))
        l_cd = mtx("4.8", 24, ROSE).move_to((C8 + D8) / 2 + np.array([-0.42, 0.06, 0.0]))
        quad = Polygon(A8, B8, C8, D8, stroke_width=0, fill_color=ACCENT,
                       fill_opacity=0.14)
        done = mtx(r"\square ABCD \;\checkmark", 40, SUCCESS)
        done.move_to(np.array([4.05, -2.35, 0.0]))

        with self.voiceover(text=NARRATION["locate"]):
            self.add_sound(self.sfx["whoosh"], gain=-17)
            self.play(FadeIn(comp_b), FadeIn(left[0]), FadeIn(left[1]),
                      run_time=5.71)
            self.play(Create(arc_b), Rotate(comp_b, SW_B, about_point=B8),
                      run_time=2.45)
            self.add_sound(self.sfx["whoosh"], gain=-17)
            self.play(FadeOut(comp_b), FadeIn(comp_c), run_time=0.8)
            self.play(Create(arc_c), Rotate(comp_c, SW_C, about_point=C8),
                      run_time=2.06)
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(FadeOut(comp_c), FadeIn(vD, scale=0.5), FadeIn(left[2]),
                      Flash(D8, color=SUCCESS, flash_radius=0.65,
                            num_lines=14),
                      run_time=2.2)
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(Create(s_bd), Create(s_cd), FadeIn(l_bd), FadeIn(l_cd),
                      run_time=3.51)
            self.add_sound(self.sfx["success"], gain=-13)
            self.play(
                Create(s_ad), FadeIn(quad),
                FadeOut(VGroup(arc_b, arc_c)),
                FadeIn(done, shift=UP * 0.15),
                run_time=2.27,
            )
            self.play(
                FadeOut(VGroup(carried, s_bd, s_cd, s_ad, l_bd, l_cd, quad,
                               vD, left, done)),
                run_time=1.0,
            )
        # beats sized to the sentences they illustrate
        # 5.71+2.45+0.8+2.06+2.2+3.51+2.27+1.0 = 20.0 s

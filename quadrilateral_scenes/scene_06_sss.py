from common import *

# S.S.S. shown as what it really is: two circles meeting in two points.
# This beat uses its own smaller scale so that BOTH intersection points and
# both whole circles stay inside the frame.
S6 = 0.62
A6 = np.array([-1.75, -0.15, 0.0])
B6 = A6 + RIGHT * (AB * S6)
C6 = A6 + np.array([2.023 * S6, 4.572 * S6, 0.0])
C6_MIRROR = np.array([C6[0], 2 * A6[1] - C6[1], 0.0])
R_A = AC * S6
R_B = BC * S6


class Scene06Sss(VoiceoverScene):
    """Three lengths fix a triangle because two circles meet twice."""

    def construct(self):
        self.set_speech_service(scene_speech_service("sss"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(paper_backdrop())

        base = Line(A6, B6, stroke_color=ACCENT, stroke_width=7)
        vA = vertex(A6, "A", DOWN + LEFT * 0.4)
        vB = vertex(B6, "B", DOWN + RIGHT * 0.4)
        l_ab = side_label(A6, B6, "4.5", ACCENT, 26, out=DOWN, buff=0.32)

        cir_a = full_circle(A6, R_A, VIOLET, 3.0, 0.85)
        cir_b = full_circle(B6, R_B, AMBER, 3.0, 0.85)
        cond_a = mtx(r"|PA| \;=\; 5", 32, VIOLET)
        cond_a.move_to(np.array([-5.35, 3.15, 0.0]))
        cond_b = mtx(r"|PB| \;=\; 5.2", 32, AMBER)
        cond_b.move_to(np.array([-5.35, 2.40, 0.0]))

        hit1 = Dot(C6, color=SUCCESS, radius=0.11)
        hit2 = Dot(C6_MIRROR, color=MUTED, radius=0.11)
        lbl1 = mtx(r"C", 34, SUCCESS).next_to(hit1, UP, buff=0.18)
        lbl2 = mtx(r"C'", 30, MUTED).next_to(hit2, DOWN, buff=0.18)
        mirror = DashedLine(A6 + LEFT * 0.9, B6 + RIGHT * 0.9,
                            stroke_color=MUTED, stroke_width=2,
                            dash_length=0.10, stroke_opacity=0.7)

        tri = Polygon(A6, B6, C6, stroke_color=SUCCESS, stroke_width=6,
                      fill_color=SUCCESS, fill_opacity=0.15)

        law = mtx(r"S\!\cdot\!S\!\cdot\!S \;\Longrightarrow\; "
                  r"\exists!\,\triangle", 40, SUCCESS)
        law.to_edge(DOWN, buff=0.50)

        with self.voiceover(text=NARRATION["sss"]):
            self.play(Create(base), FadeIn(vA), FadeIn(vB), FadeIn(l_ab),
                      run_time=4.33)
            self.add_sound(self.sfx["whoosh"], gain=-17)
            self.play(Create(cir_a), FadeIn(cond_a, shift=RIGHT * 0.2),
                      run_time=5.0)
            self.add_sound(self.sfx["whoosh"], gain=-17)
            self.play(Create(cir_b), FadeIn(cond_b, shift=RIGHT * 0.2),
                      run_time=5.0)
            self.add_sound(self.sfx["pop"], gain=-16)
            self.play(
                GrowFromCenter(hit1), GrowFromCenter(hit2),
                FadeIn(lbl1), FadeIn(lbl2), Create(mirror),
                run_time=3.0,
            )
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(
                DrawBorderThenFill(tri),
                FadeOut(VGroup(cir_a, cir_b, hit2, lbl2, mirror)),
                run_time=2.4,
            )
            self.play(Write(law), run_time=0.8)
            self.play(
                FadeOut(VGroup(base, vA, vB, l_ab, cond_a, cond_b, hit1, lbl1,
                               tri, law)),
                run_time=0.47,
            )
        # beats sized to the sentences they illustrate
        # 4.33+5.0+5.0+3.0+2.4+0.8+0.47 = 21.0 s

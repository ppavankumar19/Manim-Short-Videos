from common import *

# Two candidate starting triangles, side by side, scored against the data.
LOFF = np.array([-3.55, 0.05, 0.0])
ROFF = np.array([3.15, 0.05, 0.0])
AL, BL, CL, DL_ = [p + LOFF for p in (A, B, C, D)]
AR, BR, CR, DR_ = [p + ROFF for p in (A, B, C, D)]


def faint_quad(a, b, c, d):
    return Polygon(a, b, c, d, stroke_color=MUTED, stroke_width=2,
                   stroke_opacity=0.40, fill_opacity=0)


class Scene05Choose(VoiceoverScene):
    """Only one of the two triangles has all three of its lengths."""

    def construct(self):
        self.set_speech_service(scene_speech_service("choose"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(paper_backdrop())

        rule = mtx(r"\triangle \;\Longleftarrow\; \{\ell_1, \ell_2, \ell_3\}", 40, AMBER)
        rule.to_edge(UP, buff=0.45)

        # ---------------------------------------------------------- left: ABC
        gl = faint_quad(AL, BL, CL, DL_)
        tri_l = Polygon(AL, BL, CL, stroke_color=SUCCESS, stroke_width=6,
                        fill_color=SUCCESS, fill_opacity=0.14)
        marks_l = VGroup(vertex(AL, "A", DOWN + LEFT * 0.4, size=28),
                         vertex(BL, "B", DOWN + RIGHT * 0.4, size=28),
                         vertex(CL, "C", UP, size=28),
                         vertex(DL_, "D", LEFT, MUTED, 28))
        name_l = mtx(r"\triangle ABC", 40, SUCCESS)
        name_l.move_to(LOFF + np.array([0.0, 2.85, 0.0]))
        score_l = VGroup(
            mtx(r"AB \;=\; 4.5 \;\; \checkmark", 30, SUCCESS),
            mtx(r"BC \;=\; 5.2 \;\; \checkmark", 30, SUCCESS),
            mtx(r"AC \;=\; 5.0 \;\; \checkmark", 30, SUCCESS),
        ).arrange(DOWN, buff=0.34, aligned_edge=LEFT)
        score_l.move_to(LOFF + np.array([0.05, -3.05, 0.0]))

        # --------------------------------------------------------- right: ABD
        gr = faint_quad(AR, BR, CR, DR_)
        tri_r = Polygon(AR, BR, DR_, stroke_color=ROSE, stroke_width=6,
                        fill_color=ROSE, fill_opacity=0.12)
        marks_r = VGroup(vertex(AR, "A", DOWN + LEFT * 0.4, size=28),
                         vertex(BR, "B", DOWN + RIGHT * 0.4, size=28),
                         vertex(CR, "C", UP, MUTED, 28),
                         vertex(DR_, "D", LEFT, size=28))
        name_r = mtx(r"\triangle ABD", 40, ROSE)
        name_r.move_to(ROFF + np.array([0.0, 2.85, 0.0]))
        score_r = VGroup(
            mtx(r"AB \;=\; 4.5 \;\; \checkmark", 30, SUCCESS),
            mtx(r"BD \;=\; 5.4 \;\; \checkmark", 30, SUCCESS),
            mtx(r"AD \;=\; ? \;\;\; \times", 30, ROSE),
        ).arrange(DOWN, buff=0.34, aligned_edge=LEFT)
        score_r.move_to(ROFF + np.array([0.05, -3.05, 0.0]))

        # the missing side, flashing red
        gap = DashedLine(AR, DR_, stroke_color=ROSE, stroke_width=6,
                         dash_length=0.12)

        with self.voiceover(text=NARRATION["choose"]):
            self.play(FadeIn(rule, shift=DOWN * 0.2),
                      FadeIn(gl), FadeIn(gr),
                      FadeIn(marks_l), FadeIn(marks_r),
                      run_time=7.65)
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(DrawBorderThenFill(tri_l), Write(name_l), run_time=1.74)
            self.play(
                LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in score_l],
                            lag_ratio=0.35),
                run_time=4.52,
            )
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(DrawBorderThenFill(tri_r), Write(name_r), run_time=3.48)
            self.play(
                LaggedStart(FadeIn(score_r[0], shift=RIGHT * 0.2),
                            FadeIn(score_r[1], shift=RIGHT * 0.2),
                            lag_ratio=0.45),
                run_time=2.0,
            )
            self.add_sound(self.sfx["swipe"], gain=-15)
            # Create and Indicate cannot share a mobject in one play()
            self.play(Create(gap), FadeIn(score_r[2], scale=1.4), run_time=1.4)
            self.play(Indicate(gap, color=ROSE, scale_factor=1.05),
                      run_time=1.47)
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(
                Circumscribe(VGroup(tri_l, name_l), color=SUCCESS, buff=0.20),
                tri_r.animate.set_opacity(0.05),
                run_time=1.0,
            )
            self.play(
                FadeOut(VGroup(rule, gl, gr, tri_l, tri_r, marks_l, marks_r,
                               name_l, name_r, score_l, score_r, gap)),
                run_time=0.74,
            )
        # beats sized to the sentences they illustrate
        # 7.65+1.74+4.52+3.48+2.0+1.4+1.47+1.0+0.74 = 24.0 s

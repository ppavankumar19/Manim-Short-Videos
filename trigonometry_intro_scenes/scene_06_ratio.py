from common import *

# Template: diagram owns the LEFT half, words own the RIGHT half, and the
# two never share space.  Every label sits outside the triangles.
TH = 46 * DEGREES
B = np.array([-1.10, -2.05, 0.0])          # the shared corner, where he stands
D1, D2 = 1.85, 3.70                        # near and far

A1 = B + LEFT * D1
C1 = A1 + UP * (D1 * np.tan(TH))
A2 = B + LEFT * D2
C2 = A2 + UP * (D2 * np.tan(TH))


class Scene06Ratio(VoiceoverScene):
    """Same angle, different size — and the ratio never budges."""

    def construct(self):
        self.set_speech_service(scene_speech_service("ratio"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(lesson_backdrop())

        head = heading("the same angle, twice", AMBER, 40).to_edge(UP, buff=0.42)

        # --- the diagram, left half ------------------------------------
        ground = Line(B + RIGHT * 0.55, A2 + LEFT * 0.55,
                      stroke_color=MUTED, stroke_width=4)

        big = Polygon(B, A2, C2, stroke_color=VIOLET, stroke_width=6,
                      fill_color=VIOLET, fill_opacity=0.14,
                      joint_type=LineJointType.BEVEL)
        small = Polygon(B, A1, C1, stroke_color=ACCENT, stroke_width=6,
                        fill_color=ACCENT, fill_opacity=0.22,
                        joint_type=LineJointType.BEVEL)

        # Built explicitly rather than with Angle(), which picks the reflex
        # side for some line orderings.  B->A2 points along 180 degrees, so
        # the arc sweeps back by exactly theta.
        ang = Arc(radius=0.62, start_angle=PI, angle=-TH, arc_center=B,
                  stroke_color=SUCCESS, stroke_width=6)
        ang_lbl = txt("same angle", 24, SUCCESS)
        ang_lbl.next_to(B, DOWN + RIGHT * 0.4, buff=0.30)

        # labels sit OUTSIDE both triangles, never on top of them
        l_small = chip(txt("closer", 26, ACCENT)
                       .move_to(C1 + np.array([1.15, 0.30, 0.0])))
        tick_small = Line(C1 + np.array([0.10, 0.06, 0.0]),
                          C1 + np.array([0.68, 0.24, 0.0]),
                          stroke_color=ACCENT, stroke_width=3)
        l_big = chip(txt("further back", 26, VIOLET))
        l_big.move_to(C2 + np.array([0.0, 0.58, 0.0]))

        blown = txt("the big one is the small one, blown up", 25, INK)
        blown.move_to(np.array([-2.95, -3.05, 0.0]))

        # --- the words, right half -------------------------------------
        ratio = VGroup(txt("want", 34, ACCENT),
                       Line(LEFT * 0.62, RIGHT * 0.62, stroke_color=INK,
                            stroke_width=3),
                       txt("walk", 34, VIOLET)).arrange(DOWN, buff=0.16)
        same = txt("the same number,\nevery time", 26, MUTED)
        same.next_to(ratio, DOWN, buff=0.34)
        block1 = VGroup(ratio, same)

        name = heading("we call it  tan", SUCCESS, 44)
        friendly = txt("sin, cos and tan are just\nnames for numbers\nthat never change",
                       24, MUTED)
        friendly.next_to(name, DOWN, buff=0.34, aligned_edge=LEFT)
        block2 = VGroup(name, friendly)

        col = VGroup(block1, block2).arrange(DOWN, buff=0.85,
                                             aligned_edge=LEFT)
        col.move_to(np.array([3.70, -0.10, 0.0]))

        with self.voiceover(text=NARRATION["ratio"]):
            self.play(FadeIn(head, shift=DOWN * 0.2), Create(ground),
                      run_time=2.10)
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(DrawBorderThenFill(small), Create(tick_small),
                      FadeIn(l_small), run_time=3.37)
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(DrawBorderThenFill(big), FadeIn(l_big), run_time=3.79)
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(Create(ang), FadeIn(ang_lbl), run_time=2.94)
            self.play(FadeIn(blown, shift=UP * 0.15),
                      Indicate(VGroup(small, big), color=INK,
                               scale_factor=1.03),
                      run_time=3.80)
            self.add_sound(self.sfx["ding"], gain=-15)
            self.play(FadeIn(block1, shift=RIGHT * 0.25), run_time=5.47)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.play(FadeIn(name, scale=0.75), run_time=3.79)
            self.play(Indicate(name, color=SUCCESS, scale_factor=1.10),
                      run_time=2.95)
            self.play(FadeIn(friendly, shift=UP * 0.15), run_time=3.78)
        # 2.1+3.37+3.79+2.94+3.8+5.47+3.79+2.95+3.78 = 31.99 s

        self.play(FadeOut(VGroup(head, ground, small, big, ang, ang_lbl,
                                 l_small, tick_small, l_big, blown, col)),
                  run_time=0.69)

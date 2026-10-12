from common import *

RP = 1.30


class Scene09Pizza(VoiceoverScene):
    """The other classic route to the same answer, in twenty seconds."""

    def construct(self):
        self.set_speech_service(scene_speech_service("pizza"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(lesson_backdrop())

        head = txt("Another way to see it", 38, AMBER).to_edge(UP, buff=0.50)

        pie = sliced_circle(8, RP).move_to(np.array([-4.0, 0.05, 0.0]))
        row8 = interlocked(8, RP).move_to(np.array([1.2, 0.05, 0.0]))
        row16 = interlocked(16, RP).move_to(np.array([1.2, 0.05, 0.0]))
        row32 = interlocked(32, RP).move_to(np.array([1.2, 0.05, 0.0]))

        rect = Rectangle(width=PI * RP, height=RP, stroke_color=SUCCESS,
                         stroke_width=6, fill_color=SKY, fill_opacity=0.25)
        rect.move_to(np.array([1.2, 0.05, 0.0]))
        w_br = BraceBetweenPoints(rect.get_corner(DR), rect.get_corner(DL),
                                  direction=DOWN, color=AMBER)
        w_lbl = mtx(r"\pi r", 36, AMBER).next_to(w_br, DOWN, buff=0.16)
        h_br = BraceBetweenPoints(rect.get_corner(UR), rect.get_corner(DR),
                                  direction=RIGHT, color=SKY)
        h_lbl = mtx("r", 36, SKY).next_to(h_br, RIGHT, buff=0.16)

        same = mtx(r"\pi r \times r \;=\; \pi r^2", 52, SUCCESS)
        same.to_edge(DOWN, buff=0.60)

        with self.voiceover(text=NARRATION["pizza"]):
            self.play(FadeIn(head, shift=DOWN * 0.2), run_time=2.85)
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(FadeIn(pie, scale=0.8), run_time=2.44)
            self.add_sound(self.sfx["whoosh"], gain=-17)
            self.play(TransformFromCopy(pie, row8), run_time=4.06)
            self.play(Transform(row8, row16), run_time=1.84)
            self.play(Transform(row8, row32), run_time=1.81)
            self.add_sound(self.sfx["pop"], gain=-16)
            self.play(FadeIn(rect), FadeOut(row8),
                      GrowFromCenter(w_br), FadeIn(w_lbl),
                      GrowFromCenter(h_br), FadeIn(h_lbl), run_time=3.25)
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(Write(same), run_time=3.25)
        # 2.85+2.44+4.06+1.84+1.81+3.25+3.25+0.54 = 20.04 s

        self.play(FadeOut(VGroup(head, pie, rect, w_br, w_lbl, h_br, h_lbl,
                                 same)), run_time=0.54)

from common import *


class Scene09Example(VoiceoverScene):
    """Solve it, then put the answer next to a human being."""

    def construct(self):
        self.set_speech_service(scene_speech_service("example"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(blueprint_grid())

        s1 = mtx(r"\tan 60^\circ \;=\; \sqrt{3}", 48, SUCCESS)
        s2 = mtx(r"\sqrt{3} \;=\; \frac{h}{15}", 48, INK)
        s3 = mtx(r"h \;=\; 15\sqrt{3}", 48, INK)
        s4 = mtx(r"h \;\approx\; 25.98\,\text{m}", 56, AMBER)
        steps = VGroup(s1, s2, s3, s4).arrange(DOWN, buff=0.60)
        steps.move_to(np.array([-2.65, 0.15, 0.0]))
        box = SurroundingRectangle(s4, color=AMBER, buff=0.24, corner_radius=0.12)

        # scale check, drawn to the real 25.98 : 1.7 ratio
        gy = -3.05
        man_h = 0.30
        tower_h = man_h * (HEIGHT_M / 1.7)          # ~4.58, true to scale
        t_foot = np.array([3.15, gy, 0.0])
        tower = realistic_tower(t_foot, t_foot + UP * tower_h, width=0.55)
        man = Man(base=np.array([4.45, gy, 0.0]), height=man_h, facing=LEFT,
                  pose=LOOKING_UP)
        t_br = BraceBetweenPoints(t_foot + UP * tower_h, t_foot, direction=LEFT,
                                  color=AMBER)
        t_lbl = mtx(r"25.98\,\text{m}", 28, AMBER).next_to(t_br, LEFT, buff=0.12)
        m_br = BraceBetweenPoints(np.array([4.45, gy + man_h, 0.0]),
                                  np.array([4.45, gy, 0.0]), direction=RIGHT,
                                  color=SUCCESS)
        m_lbl = mtx(r"1.7\,\text{m}", 24, SUCCESS).next_to(m_br, RIGHT, buff=0.10)
        ratio = mtx(r"\frac{h}{1.7} \;\approx\; 15", 34, INK)
        ratio.move_to(np.array([3.75, gy + tower_h + 0.75, 0.0]))

        with self.voiceover(text=NARRATION["example"]):
            self.play(Write(s1), run_time=4.4)
            self.play(Write(s2),
                      Indicate(s1, color=SUCCESS, scale_factor=1.12),
                      run_time=3.5)
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(Write(s3), run_time=3.1)
            self.add_sound(self.sfx["success"], gain=-13)
            self.play(
                Write(s4), Create(box),
                Flash(s4.get_center(), color=AMBER, flash_radius=1.3,
                      num_lines=16),
                run_time=7.0,
            )
            self.add_sound(self.sfx["pop"], gain=-16)
            self.play(
                GrowFromEdge(tower, DOWN), FadeIn(man),
                GrowFromCenter(t_br), FadeIn(t_lbl),
                GrowFromCenter(m_br), FadeIn(m_lbl),
                run_time=3.1,
            )
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(FadeIn(ratio, shift=DOWN * 0.2),
                      Indicate(t_br, color=AMBER, scale_factor=1.05),
                      run_time=2.9)
            self.play(
                FadeOut(VGroup(steps, box, tower, man, t_br, t_lbl, m_br,
                               m_lbl, ratio)),
                run_time=1.0,
            )
        # beats sized to the sentences they illustrate
        # 4.4+3.5+3.1+7.0+3.1+2.9+1.0 = 25.0 s

from common import *


class Scene11Example1(VoiceoverScene):
    """Put r = 3.5 into the formula and finish the sum."""

    def construct(self):
        self.set_speech_service(scene_speech_service("example1"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(lesson_backdrop())

        head = mtx(r"A \;=\; \pi r^2", 54, ACCENT).to_edge(UP, buff=0.65)

        lines = VGroup(
            mtx(r"A \;=\; \tfrac{22}{7} \times 3.5 \times 3.5", 46, INK),
            mtx(r"3.5 \times 3.5 \;=\; 12.25", 42, MUTED),
            mtx(r"A \;=\; \tfrac{22}{7} \times 12.25", 46, INK),
            mtx(r"A \;=\; 38.5\,\text{cm}^2", 58, SUCCESS),
        ).arrange(DOWN, buff=0.58)
        lines.move_to(np.array([0.0, -0.25, 0.0]))
        box = SurroundingRectangle(lines[3], color=SUCCESS, buff=0.28,
                                   corner_radius=0.14)
        cap = txt("that is the space inside", 28, MUTED)
        cap.next_to(box, DOWN, buff=0.36)

        with self.voiceover(text=NARRATION["example1"]):
            self.play(FadeIn(head, shift=DOWN * 0.2), run_time=1.3)
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(TransformFromCopy(head, lines[0]), run_time=2.15)
            self.play(FadeIn(lines[1], shift=RIGHT * 0.2), run_time=5.15)
            self.play(TransformFromCopy(lines[0], lines[2]), run_time=5.15)
            self.add_sound(self.sfx["success"], gain=-13)
            self.play(FadeIn(lines[3], shift=UP * 0.2), Create(box),
                      FadeIn(cap),
                      Flash(lines[3].get_center(), color=SUCCESS,
                            flash_radius=1.4, num_lines=16),
                      run_time=4.25)
        # 1.3+2.15+5.15+5.15+4.25+0.5 = 18.5 s

        self.play(FadeOut(VGroup(head, lines, box, cap)), run_time=0.5)

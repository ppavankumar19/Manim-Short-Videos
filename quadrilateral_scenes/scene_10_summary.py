from common import *


class Scene10Summary(VoiceoverScene):
    def construct(self):
        self.set_speech_service(scene_speech_service("summary"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(paper_backdrop())

        law = mtx(r"5\ \ell \;\Longrightarrow\; \square", 68, SUCCESS)
        law.move_to(UP * 1.05)
        rule = rule_line(4.4, MUTED).next_to(law, DOWN, buff=0.60)
        line = mtx(r"\square \;=\; \triangle \;+\; \triangle", 48, AMBER)
        line.next_to(rule, DOWN, buff=0.60)

        with self.voiceover(text=NARRATION["summary"]):
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(Write(law), run_time=3.7)
            self.play(Create(rule), run_time=1.05)
            self.play(FadeIn(line, shift=UP * 0.2), run_time=3.65)
        # 3.7+1.05+3.65 = 8.4 s

        self.wait(END_HOLD)
        self.play(FadeOut(VGroup(law, rule, line)), run_time=0.6)

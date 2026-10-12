from common import *


class Scene10Summary(VoiceoverScene):
    def construct(self):
        self.set_speech_service(scene_speech_service("summary"), create_subcaption=True)
        self.sfx = load_sfx()

        self.add(sky_ground_backdrop(-3.30))
        self.add(star_field(20, y_min=0.9).set_opacity(0.5))

        law = mtx(r"\theta \;+\; d \;\Longrightarrow\; h", 66, SUCCESS)
        law.move_to(UP * 0.95)
        rule = rule_line(4.0, MUTED).next_to(law, DOWN, buff=0.60)
        line = mtx(r"h \;=\; d\,\tan\theta", 46, AMBER).next_to(rule, DOWN, buff=0.60)

        with self.voiceover(text=NARRATION["summary"]):
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(Write(law), run_time=3.5)
            self.play(Create(rule), run_time=1.0)
            self.play(FadeIn(line, shift=UP * 0.2), run_time=3.5)
        # 3.5+1.0+3.5 = 8.0 s

        self.wait(END_HOLD)
        self.play(FadeOut(VGroup(law, rule, line)), run_time=0.6)

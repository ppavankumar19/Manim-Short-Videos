from common import *


class Scene01Title(VoiceoverScene):
    def construct(self):
        self.set_speech_service(scene_speech_service("title"), create_subcaption=True)
        self.sfx = load_sfx()

        self.add(sky_ground_backdrop(-3.30))
        stars = star_field(22, y_min=0.9).set_opacity(0.5)
        self.add(stars)

        title = txt("Heights and Distances", 46, ACCENT, "BOLD").move_to(UP * 1.35)
        law = mtx(r"h \;=\; d\,\tan\theta", 60, SUCCESS).move_to(DOWN * 0.35)
        rule = rule_line(3.6, MUTED).next_to(law, DOWN, buff=0.55)

        with self.voiceover(text=NARRATION["title"]):
            self.play(Write(title), run_time=2.2)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.play(SpinInFromNothing(law), Create(rule), run_time=1.6)
            self.play(FadeOut(VGroup(title, law, rule, stars)), run_time=1.2)
        # 2.2+1.6+1.2 = 5.0 s

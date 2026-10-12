from common import *


class Scene01Title(VoiceoverScene):
    def construct(self):
        self.set_speech_service(scene_speech_service("title"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(paper_backdrop())

        title = heading("Constructing a Quadrilateral", ACCENT)
        title.move_to(UP * 0.85)
        rule = rule_line(6.4, MUTED).next_to(title, DOWN, buff=0.42)
        sub = mtx(r"S\!\cdot\!S\!\cdot\!S \;+\; D\!\cdot\!D", 46, SUCCESS)
        sub.next_to(rule, DOWN, buff=0.46)

        comp = compass_icon(np.array([-5.35, 1.55, 0.0]), 1.05, AMBER)
        marks = mtx(r"3 \;+\; 2 \;=\; 5", 34, MUTED)
        marks.move_to(np.array([4.90, -1.55, 0.0]))

        with self.voiceover(text=NARRATION["title"]):
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(FadeIn(title, shift=DOWN * 0.25),
                      Create(comp), run_time=2.0)
            self.play(Create(rule), FadeIn(sub, shift=UP * 0.2),
                      FadeIn(marks), run_time=2.0)
            self.play(FadeOut(VGroup(title, rule, sub, comp, marks)),
                      run_time=1.0)
        # 2.0+2.0+1.0 = 5.0 s

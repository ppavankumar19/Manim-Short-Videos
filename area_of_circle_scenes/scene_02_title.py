from common import *


class Scene02Title(VoiceoverScene):
    def construct(self):
        self.set_speech_service(scene_speech_service("title"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(lesson_backdrop())

        title = heading("The Area of a Circle", ACCENT).move_to(UP * 0.85)
        rule = rule_line(6.0, MUTED).next_to(title, DOWN, buff=0.42)
        sub = mtx(r"\pi r^2 \;=\; ?", 58, AMBER).next_to(rule, DOWN, buff=0.50)
        ring = Circle(radius=2.9, stroke_color=VIOLET, stroke_width=4,
                      stroke_opacity=0.35, fill_opacity=0)

        with self.voiceover(text=NARRATION["title"]):
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(FadeIn(title, shift=DOWN * 0.25), Create(ring),
                      run_time=4.05)
            self.play(Create(rule), Write(sub), run_time=2.31)
            self.play(FadeOut(VGroup(title, rule, sub, ring)), run_time=0.58)
        # 4.05+2.31+0.58 = 6.94 s

from common import *


class Scene11Overview(VoiceoverScene):
    """Closing recap — the whole construction as five symbolic lines."""

    def construct(self):
        self.set_speech_service(scene_speech_service("overview"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(paper_backdrop())

        head = heading("Method Recap", AMBER)

        rows = [
            mtx(r"n \;=\; 4\times 2 \;-\; 3 \;=\; 5", 32, INK),
            mtx(r"\triangle \;\Longleftarrow\; \{\ell_1,\ell_2,\ell_3\}"
                r"\;\;\Rightarrow\;\; \triangle ABC", 32, INK),
            mtx(r"AB \;\to\; \odot(A,5.0)\,\cap\,\odot(B,5.2) \;=\; C",
                32, INK),
            mtx(r"\odot(B,5.4)\,\cap\,\odot(C,4.8) \;=\; D", 32, INK),
            mtx(r"\square ABCD \;\checkmark", 32, SUCCESS),
        ]
        lines = VGroup()
        for i, row in enumerate(rows, 1):
            badge = Circle(radius=0.22, stroke_color=SUCCESS, stroke_width=2,
                           fill_color=SUCCESS, fill_opacity=0.15)
            num = mtx(str(i), 22, SUCCESS).move_to(badge.get_center())
            lines.add(VGroup(VGroup(badge, num), row).arrange(RIGHT, buff=0.38))
        lines.arrange(DOWN, buff=0.46, aligned_edge=LEFT)

        frame = card(11.6, lines.height + 1.4, AMBER)
        lines.move_to(frame.get_center())
        panel = VGroup(frame, lines).move_to(DOWN * 0.40)

        with self.voiceover(text=NARRATION["overview"]):
            self.play(FadeIn(head), run_time=1.8)
            self.play(Create(frame), run_time=1.8)
            self.play(
                LaggedStart(*[FadeIn(r, shift=RIGHT * 0.25) for r in lines],
                            lag_ratio=0.32),
                run_time=11.9,
            )
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(Circumscribe(lines[-1], color=SUCCESS, buff=0.15),
                      run_time=2.0)
            self.play(FadeOut(VGroup(head, panel)), run_time=2.0)
        # 1.8+1.8+11.9+2.0+2.0 = 19.5 s

        self.wait(END_HOLD)

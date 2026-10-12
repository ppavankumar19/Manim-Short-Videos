from common import *


class Scene11Overview(VoiceoverScene):
    """Closing recap — the method as four symbolic lines."""

    def construct(self):
        self.set_speech_service(scene_speech_service("overview"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(blueprint_grid())

        head = heading("Method Recap", AMBER)

        rows = [
            mtx(r"\triangle:\quad h \perp d,\quad \angle = 90^\circ", 34, INK),
            mtx(r"\theta \;=\; \angle ABC", 34, INK),
            mtx(r"\tan\theta \;=\; \dfrac{h}{d} \;=\; f(\theta)", 34, INK),
            mtx(r"h \;=\; d\,\tan\theta", 34, SUCCESS),
        ]
        badges = VGroup()
        lines = VGroup()
        for i, row in enumerate(rows, 1):
            badge = Circle(radius=0.24, stroke_color=SUCCESS, stroke_width=2,
                           fill_color=SUCCESS, fill_opacity=0.15)
            num = mtx(str(i), 24, SUCCESS).move_to(badge.get_center())
            item = VGroup(VGroup(badge, num), row).arrange(RIGHT, buff=0.40)
            lines.add(item)
            badges.add(badge)
        lines.arrange(DOWN, buff=0.52, aligned_edge=LEFT)

        frame = card(11.2, lines.height + 1.5, AMBER)
        lines.move_to(frame.get_center())
        panel = VGroup(frame, lines).move_to(DOWN * 0.35)

        with self.voiceover(text=NARRATION["overview"]):
            self.play(FadeIn(head), run_time=2.0)
            self.play(Create(frame), run_time=2.0)
            self.play(
                LaggedStart(*[FadeIn(r, shift=RIGHT * 0.25) for r in lines],
                            lag_ratio=0.35),
                run_time=9.5,
            )
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(Circumscribe(lines[-1], color=SUCCESS, buff=0.15),
                      run_time=2.5)
            self.play(FadeOut(VGroup(head, panel)), run_time=2.0)
        # 2.0+2.0+9.5+2.5+2.0 = 18.0 s

        self.wait(END_HOLD)

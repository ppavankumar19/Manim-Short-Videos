from common import *


class Scene03Hard(VoiceoverScene):
    """Counting boxes works for a square and breaks on a circle."""

    def construct(self):
        self.set_speech_service(scene_speech_service("hard"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(lesson_backdrop())

        SIDE = 2.6
        sq_c = np.array([-3.5, 0.15, 0.0])
        ci_c = np.array([3.3, 0.15, 0.0])

        square = Square(side_length=SIDE, stroke_color=SKY, stroke_width=6,
                        fill_opacity=0).move_to(sq_c)
        grid = counting_grid(sq_c, SIDE, 4, SKY)
        count = Integer(0, font_size=44, color=SKY)
        count.next_to(square, DOWN, buff=0.45)
        easy = txt("easy!", 34, SUCCESS).next_to(count, DOWN, buff=0.25)

        circle = Circle(radius=SIDE / 2, stroke_color=AMBER, stroke_width=6,
                        fill_opacity=0).move_to(ci_c)
        grid2 = counting_grid(ci_c, SIDE, 4, AMBER)
        # the boxes the curved edge slices through
        broken = VGroup()
        for box in grid2:
            d = float(np.linalg.norm(box.get_center() - ci_c))
            corner = float(np.linalg.norm(box.get_corner(UR) - box.get_center()))
            if abs(d - SIDE / 2) < corner:
                broken.add(box)
        cross = VGroup(
            Line(UL * 0.30, DR * 0.30, stroke_color=ROSE, stroke_width=8),
            Line(UR * 0.30, DL * 0.30, stroke_color=ROSE, stroke_width=8),
        ).next_to(circle, DOWN, buff=0.45)
        nope = txt("boxes do not fit", 32, ROSE).next_to(cross, DOWN, buff=0.22)
        trick = txt("We need a smarter trick.", 40, AMBER).to_edge(DOWN, buff=0.55)

        with self.voiceover(text=NARRATION["hard"]):
            self.play(Create(square), run_time=4.07)
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(
                LaggedStart(*[FadeIn(b) for b in grid], lag_ratio=0.05),
                count.animate.set_value(16),
                run_time=6.11,
            )
            self.play(FadeIn(easy, scale=0.7), Create(circle), run_time=3.06)
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(FadeIn(grid2), run_time=3.06)
            self.add_sound(self.sfx["swipe"], gain=-16)
            self.play(
                LaggedStart(*[b.animate.set_stroke(ROSE, 3).set_fill(ROSE, 0.30)
                              for b in broken], lag_ratio=0.06),
                run_time=6.63,
            )
            self.play(FadeIn(cross, scale=1.5), FadeIn(nope), run_time=3.06)
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(FadeIn(trick, shift=UP * 0.2), run_time=2.54)
        # 4.07+6.11+3.06+3.06+6.63+3.06+2.54+0.68 = 29.21 s

        self.play(FadeOut(VGroup(square, grid, count, easy, circle, grid2,
                                 cross, nope, trick)), run_time=0.68)

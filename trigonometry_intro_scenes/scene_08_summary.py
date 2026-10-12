from common import *


class Scene08Summary(VoiceoverScene):
    """What we discussed, as points — the thing to screenshot."""

    def construct(self):
        self.set_speech_service(scene_speech_service("summary"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(lesson_backdrop())

        head = heading("what we learned today", AMBER, 44).to_edge(UP, buff=0.50)

        points = [
            "trigonometry  =  measuring triangles",
            "a triangle cannot wobble",
            "a few parts fix all the rest",
            "measure one distance, one angle",
            "the triangle gives you the rest",
        ]
        rows = VGroup()
        ticks = VGroup()
        for p in points:
            t = tick_mark(ORIGIN, 0.20, SUCCESS)
            label = txt(p, 32, INK)
            row = VGroup(t, label).arrange(RIGHT, buff=0.42)
            rows.add(row)
            ticks.add(t)
        rows.arrange(DOWN, buff=0.58, aligned_edge=LEFT)

        frame = card(10.8, rows.height + 1.3, SUCCESS)
        rows.move_to(frame.get_center())
        panel = VGroup(frame, rows).move_to(DOWN * 0.35)

        with self.voiceover(text=NARRATION["summary"]):
            # One tick per spoken point, each sized to its own sentence,
            # instead of a single long LaggedStart that drifts away from
            # the words naming each point.
            self.play(FadeIn(head, shift=DOWN * 0.2), run_time=2.68)
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(Create(frame), FadeIn(rows[0], shift=RIGHT * 0.30),
                      run_time=1.79)
            self.play(FadeIn(rows[1], shift=RIGHT * 0.30), run_time=2.68)
            self.play(FadeIn(rows[2], shift=RIGHT * 0.30), run_time=2.68)
            self.play(FadeIn(rows[3], shift=RIGHT * 0.30), run_time=2.68)
            self.play(FadeIn(rows[4], shift=RIGHT * 0.30), run_time=4.91)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.play(Circumscribe(rows[-1], color=SUCCESS, buff=0.18),
                      run_time=3.58)
        # beats sized to the sentences they illustrate
        # 2.68+1.79+2.68+2.68+2.68+4.91+3.58 = 21.0 s

        self.wait(END_HOLD)
        self.play(FadeOut(VGroup(head, panel)), run_time=0.67)

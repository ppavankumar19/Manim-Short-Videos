from common import *

OFF = np.array([-3.15, 0.15, 0.0])
A9, B9, C9, D9 = [p + OFF for p in (A, B, C, D)]


class Scene09Verify(VoiceoverScene):
    """Measure the finished figure back against all five given numbers."""

    def construct(self):
        self.set_speech_service(scene_speech_service("verify"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(paper_backdrop())

        quad = Polygon(A9, B9, C9, D9, stroke_color=INK, stroke_width=3,
                       stroke_opacity=0.40, fill_color=ACCENT,
                       fill_opacity=0.09)
        # the diagonals belong in the picture too — the panel ticks them off
        diags = VGroup(
            Line(A9, C9, stroke_color=VIOLET, stroke_width=3,
                 stroke_opacity=0.55),
            Line(B9, D9, stroke_color=VIOLET, stroke_width=3,
                 stroke_opacity=0.55),
        )
        marks = VGroup(vertex(A9, "A", DOWN + LEFT * 0.4),
                       vertex(B9, "B", DOWN + RIGHT * 0.4),
                       vertex(C9, "C", UP + RIGHT * 0.3),
                       vertex(D9, "D", LEFT + UP * 0.3))

        segs = [
            (Line(A9, B9, stroke_color=SUCCESS, stroke_width=8), r"AB \;=\; 4.5"),
            (Line(B9, C9, stroke_color=SUCCESS, stroke_width=8), r"BC \;=\; 5.2"),
            (Line(C9, D9, stroke_color=SUCCESS, stroke_width=8), r"CD \;=\; 4.8"),
            (Line(A9, C9, stroke_color=SUCCESS, stroke_width=8), r"AC \;=\; 5.0"),
            (Line(B9, D9, stroke_color=SUCCESS, stroke_width=8), r"BD \;=\; 5.4"),
        ]
        rows = VGroup(*[
            mtx(t + r"\;\; \checkmark", 34, SUCCESS) for _, t in segs
        ]).arrange(DOWN, buff=0.42, aligned_edge=LEFT)
        rows.move_to(np.array([3.75, 1.05, 0.0]))
        frame = SurroundingRectangle(rows, color=SUCCESS, buff=0.48,
                                     corner_radius=0.16)

        extra = mtx(r"AD \;\to\; 1.12", 36, AMBER)
        extra.next_to(frame, DOWN, buff=0.55)
        note = mtx(r"5 \;\Longrightarrow\; \square", 40, VIOLET)
        note.next_to(extra, DOWN, buff=0.48)

        with self.voiceover(text=NARRATION["verify"]):
            self.play(FadeIn(quad), FadeIn(diags), FadeIn(marks),
                      Create(frame), run_time=4.71)
            # one tick per spoken measurement, each as long as it is said
            row_times = [2.15, 2.15, 2.15, 1.71, 2.57]
            for i, (seg, _) in enumerate(segs):
                self.add_sound(self.sfx["click"], gain=-18)
                self.play(
                    ShowPassingFlash(seg.copy().set_color(SUCCESS),
                                     time_width=0.65),
                    FadeIn(rows[i], shift=RIGHT * 0.2),
                    run_time=row_times[i],
                )
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(FadeIn(extra, shift=UP * 0.15),
                      Create(DashedLine(A9, D9, stroke_color=AMBER,
                                        stroke_width=5, dash_length=0.12)),
                      run_time=2.84)
            self.play(Write(note), Circumscribe(frame, color=SUCCESS,
                                                buff=0.10), run_time=2.72)
        # beats sized to the sentences they illustrate
        # 4.71 + (2.15+2.15+2.15+1.71+2.57) + 2.84 + 2.72 = 21.0 s

        self.wait(END_HOLD)

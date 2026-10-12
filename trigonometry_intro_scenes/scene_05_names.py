from common import *

# Shifted right so the left-hand label has room inside the frame, and the
# whole figure sits centred rather than crowding the left edge.
A = np.array([-1.55, -1.75, 0.0])          # foot of the tree
B = np.array([4.05, -1.75, 0.0])           # where he stands
C = np.array([-1.55, 1.95, 0.0])           # top of the tree


class Scene05Names(VoiceoverScene):
    """The three sides, named in words a child already owns."""

    def construct(self):
        self.set_speech_service(scene_speech_service("names"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(lesson_backdrop())

        head = heading("just three sides", AMBER, 40).to_edge(UP, buff=0.45)

        face = Polygon(A, B, C, fill_color=ACCENT, fill_opacity=0.12,
                       stroke_width=0)
        base = Line(A, B, stroke_color=VIOLET, stroke_width=9)
        rise = Line(A, C, stroke_color=ACCENT, stroke_width=9)
        sight = Line(B, C, stroke_color=AMBER, stroke_width=8)
        corner = RightAngle(Line(A, B), Line(A, C), length=0.34, color=MUTED,
                            stroke_width=4)
        eye = Dot(B, color=SUCCESS, radius=0.10)

        # Shorter labels, each clear of the figure and of the frame edge.
        l_base = chip(txt("you WALK this", 28, VIOLET)
                      .move_to(np.array([1.25, -2.65, 0.0])))
        l_rise = chip(txt("you WANT this", 28, ACCENT)
                      .move_to(np.array([-4.30, 0.10, 0.0])))
        l_sight = chip(txt("you LOOK along this", 28, AMBER)
                       .move_to(np.array([3.30, 1.90, 0.0])))

        closing = heading("walk it  •  want it  •  look along it", SUCCESS, 34)
        closing.to_edge(DOWN, buff=0.42)

        with self.voiceover(text=NARRATION["names"]):
            self.play(FadeIn(head, shift=DOWN * 0.2), FadeIn(face),
                      FadeIn(corner), FadeIn(eye), run_time=2.85)
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(Create(base), FadeIn(l_base, shift=UP * 0.2),
                      run_time=3.58)
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(Create(rise), FadeIn(l_rise, shift=RIGHT * 0.2),
                      run_time=3.22)
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(Create(sight), FadeIn(l_sight, shift=DOWN * 0.2),
                      run_time=5.0)
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(FadeIn(closing, shift=UP * 0.2),
                      LaggedStart(Indicate(base, color=VIOLET),
                                  Indicate(rise, color=ACCENT),
                                  Indicate(sight, color=AMBER),
                                  lag_ratio=0.45),
                      run_time=7.15)
        # 3.27+4+4+4.54+5.99+0.54 = 22.34 s

        self.play(FadeOut(VGroup(head, face, base, rise, sight, corner, eye,
                                 l_base, l_rise, l_sight, closing)),
                  run_time=0.54)

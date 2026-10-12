from common import *


class Scene00Greeting(VoiceoverScene, ThreeDScene):
    """Hello, over a slowly turning triangle in space."""

    def construct(self):
        self.set_speech_service(scene_speech_service("greeting"), create_subcaption=True)
        self.sfx = load_sfx()
        stage_3d(self)

        self.set_camera_orientation(phi=68 * DEGREES, theta=-70 * DEGREES,
                                    zoom=1.0)

        # A RIGHT-angled wire triangle turning in space — the shape the
        # whole subject is about, seen as an object rather than a drawing.
        pts = [np.array([-1.70, -1.30, 0.0]),      # the square corner
               np.array([ 2.10, -1.30, 0.0]),      # along the ground
               np.array([-1.70,  1.55, 0.0])]      # standing up
        corner = np.array([-1.70, -1.30, 0.0])
        m = 0.42
        wire = VGroup(
            *[line3(pts[i], pts[(i + 1) % 3], ACCENT, 9.0) for i in range(3)],
            # the little square that says "this is a right angle"
            line3(corner + RIGHT * m, corner + RIGHT * m + UP * m, MUTED, 5.0),
            line3(corner + UP * m, corner + RIGHT * m + UP * m, MUTED, 5.0),
            *[dot3(p, AMBER, 0.09) for p in pts],
        )
        wire.move_to(ORIGIN)

        hello = heading("Hello, friends!", ACCENT, 58)
        question = heading("What is trigonometry?", AMBER, 46)
        promise = txt("by the end, you will know", 30, INK)
        for m, y in ((hello, 2.55), (question, -1.75), (promise, -2.75)):
            self.add_fixed_in_frame_mobjects(m)
            m.move_to(np.array([0.0, y, 0.0]))
            m.set_opacity(0.0)

        with self.voiceover(text=NARRATION["greeting"]):
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(hello.animate.set_opacity(1.0), run_time=2.80)
            self.add_sound(self.sfx["whoosh"], gain=-17)
            self.play(question.animate.set_opacity(1.0), run_time=1.40)
            # "it sounds like a big, scary word" — let it sit there
            self.play(Indicate(question, color=AMBER, scale_factor=1.06),
                      run_time=3.27)
            self.play(promise.animate.set_opacity(1.0), run_time=6.53)
        # beats sized to the sentences they illustrate
        # 2.8+1.4+3.27+6.53 = 14.0 s

        wire.clear_updaters()
        self.play(FadeOut(wire),
                  hello.animate.set_opacity(0.0),
                  question.animate.set_opacity(0.0),
                  promise.animate.set_opacity(0.0),
                  run_time=0.7)

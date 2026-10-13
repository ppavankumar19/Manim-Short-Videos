"""Beat 1 -- the man and the theory he wanted to be true."""

from common import *


class Scene01Kepler(VoiceoverScene):
    """Serif name plate over the period plate, held while the claim lands."""

    def construct(self):
        self.set_speech_service(scene_speech_service("kepler"))
        self.add(star_field(70, seed=3).set_opacity(0.35))

        caps = Captions(self, "kepler")

        portrait = ImageMobject(KEPLER_IMAGE)
        portrait.height = 4.05
        portrait.move_to(UP * 0.28)
        frame = Rectangle(width=portrait.width + 0.06,
                          height=portrait.height + 0.06,
                          stroke_color="#6B6355", stroke_width=2,
                          fill_opacity=0.0).move_to(portrait)

        name = plate("Kepler", 74).move_to(UP * 3.10)

        with self.voiceover(text=NARRATION["kepler"]) as tracker:
            caps.start(tracker)
            lead, steps = cue_times(tracker, "kepler", [0, 2])
            if lead > 0.05:
                self.wait(lead)

            self.add(portrait, frame)
            portrait.set_opacity(0.0)
            frame.set_stroke(opacity=0.0)
            self.play(
                portrait.animate.set_opacity(1.0),
                frame.animate.set_stroke(opacity=1.0),
                Write(name),
                run_time=steps[0], rate_func=rate_functions.ease_out_sine,
            )
            # A slow push in, so the plate is never a still frame.
            self.play(
                portrait.animate.scale(1.06),
                Indicate(name, color=INK, scale_factor=1.04),
                run_time=steps[1], rate_func=rate_functions.linear,
            )

        caps.stop()
        self.play(FadeOut(Group(portrait, frame, name)), run_time=0.5)

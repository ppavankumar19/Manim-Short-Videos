"""Beat 5 -- Tycho Brahe, and the aside about how the data was got."""

from common import *
from map_art import uraniborg


MARKS = [
    0,   # "And the way he did"       the observatory draws itself
    2,   # "heroic, by the"           the name plate arrives
    4,   # "beside the point."        a slow drift out
]


class Scene05Tycho(VoiceoverScene):
    """The observatory, drawn as it is described, under a serif name plate."""

    def construct(self):
        self.set_speech_service(scene_speech_service("tycho"))
        self.add(star_field(60, seed=17).set_opacity(0.25))

        caps = Captions(self, "tycho")

        art = uraniborg().scale(1.12).move_to(LEFT * 2.55 + UP * 0.42)
        name = plate("Tycho Brahe", 58).move_to(RIGHT * 3.85 + UP * 2.35)

        with self.voiceover(text=NARRATION["tycho"]) as tracker:
            caps.start(tracker)
            lead, steps = cue_times(tracker, "tycho", MARKS)
            if lead > 0.05:
                self.wait(lead)

            self.play(Create(art, lag_ratio=0.02),
                      run_time=steps[0], rate_func=rate_functions.linear)
            self.play(Write(name), art.animate.scale(1.05),
                      run_time=steps[1], rate_func=rate_functions.ease_out_sine)
            self.play(art.animate.scale(1.04).shift(RIGHT * 0.22),
                      run_time=steps[2], rate_func=rate_functions.linear)

        caps.stop()
        self.play(FadeOut(art), FadeOut(name), run_time=0.4)

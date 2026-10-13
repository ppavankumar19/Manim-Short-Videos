"""Beat 4 -- the data, and where it lived.

The reference clip pushes a satellite view down the Oresund until it lands on
the island of Ven.  Same move here, over a drawn strait: the map scales up
about the island, so the push reads as altitude rather than as a zoom.
"""

from common import *
from map_art import oresund

MARKS = [
    0,   # "Eventually, he"           the strait, high up
    2,   # "his hands on some"        descending
    4,   # "try to confirm"           Ven named
]


class Scene04Ven(VoiceoverScene):
    """A push down the Oresund onto Tycho's island."""

    def construct(self):
        self.set_speech_service(scene_speech_service("ven"))

        caps = Captions(self, "ven")

        art, ven = oresund(width=22.0)
        art.scale(0.85, about_point=ven)     # start high, island still small
        self.add(art)
        art.set_z_index(-5)

        label = plate("Island of Ven", 40)
        label.move_to(ven + np.array([2.45, 0.95, 0.0]))
        label.set_opacity(0.0)
        self.add(label)

        with self.voiceover(text=NARRATION["ven"]) as tracker:
            caps.start(tracker)
            lead, steps = cue_times(tracker, "ven", MARKS)
            if lead > 0.05:
                self.wait(lead)

            # The whole map grows about the island, so Ven stays put on screen
            # while everything around it opens out -- a descent, not a zoom.
            self.play(art.animate.scale(1.30, about_point=ven),
                      run_time=steps[0], rate_func=rate_functions.linear)
            self.play(art.animate.scale(1.40, about_point=ven),
                      run_time=steps[1], rate_func=rate_functions.linear)
            self.play(
                art.animate.scale(1.45, about_point=ven),
                label.animate.set_opacity(1.0).shift(RIGHT * 0.18),
                run_time=steps[2], rate_func=rate_functions.linear,
            )

        caps.stop()
        self.play(FadeOut(art), FadeOut(label), run_time=0.4)

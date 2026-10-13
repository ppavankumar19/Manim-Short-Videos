"""Beat 7 -- the wrong premise, and where it led.

The nest dissolves and the camera swings overhead until the ecliptic is flat
on: what is left is the thing Kepler actually found, the orbits themselves,
seen the way his laws describe them.
"""

from manim import ThreeDScene

from common import *

MARKS = [
    0,   # "But, even though"         the solids still there, camera rising
    2,   # "wrong premise, this"      the solids let go
    4,   # "be the first person"      overhead, orbits alone
    6,   # "planets actually"         the planets run
    8,   # "the sun, and to"          hold
    10,  # "eponymous laws."          settle
]

THETA_CAM = -96 * DEGREES
PHI = [67, 52, 30, 8, 0, 0]
ZOOM = [1.45, 0.70, 0.30, 0.235, 0.225, 0.22]


class Scene07Laws(VoiceoverScene, ThreeDScene):
    """From the model overhead to the orbits, seen flat on."""

    def construct(self):
        self.set_speech_service(scene_speech_service("laws"))
        self.set_camera_orientation(phi=PHI[0] * DEGREES, theta=THETA_CAM,
                                    zoom=ZOOM[0],
                                    focal_distance=FOCAL)

        self.add_fixed_in_frame_mobjects(star_field(150, seed=5))
        self.add_fixed_in_frame_mobjects(sun_glow())

        caps = Captions(self, "laws")
        shells, orbits, solids = full_nest()
        order = [solids[name] for name in NEST_ORDER]

        for shell in shells:
            pin_shell(self, shell)
        # This beat opens on beat 6's close-up, inside the outer balls, so the
        # ones the camera is already within never come back.
        for shell in shells[2:]:
            self.remove(shell)
        self.add(orbits, *order)

        with self.voiceover(text=NARRATION["laws"]) as tracker:
            caps.start(tracker)
            lead, steps = cue_times(tracker, "laws", MARKS)
            if lead > 0.05:
                self.wait(lead)

            def step(i, *anims, spin=1.0):
                self.move_camera(
                    phi=PHI[i] * DEGREES, theta=THETA_CAM, zoom=ZOOM[i],
                    run_time=steps[i], rate_func=rate_functions.ease_in_out_sine,
                    added_anims=[spin_orbits(orbits, steps[i] * spin), *anims],
                )

            step(0)
            # The premise goes; the measurements it was fitted to stay.
            step(1, *[s.animate.set_stroke(opacity=0.0) for s in order],
                 *[fade_shell(shell, out=True) for shell in shells[:2]])
            step(2, *[o[0].animate.set_stroke(opacity=0.55) for o in orbits])
            # Overhead now, so the orbits read as the circles they nearly are,
            # and the planets are allowed to run at their own rates.
            step(3, spin=2.6)
            step(4, spin=2.6)
            step(5, spin=1.6)

        caps.stop()
        self.play(FadeOut(orbits), run_time=0.4)

"""Beat 3 -- what the nest was supposed to buy him.

Opens on the finished model at the camera scene 02 left it, then walks the
five solids one at a time while the narration reaches for the word "natural".
"""

from manim import ThreeDScene

from common import *

MARKS = [
    0,   # "You get these six"        the six shells pulse outward in turn
    2,   # "ratios between"           hold on the whole nest
    4,   # "spheres, Kepler"          hold
    6,   # "match the ratios of"      the orbits brighten against the shells
    8,   # "six known planets."       hold
    9,   # "Since these are the"      octahedron alone
    10,  # "Platonic solids,"         icosahedron alone
    11,  # "it somehow feels"         dodecahedron alone
    12,  # "like a very natural"      tetrahedron alone
    13,  # "or universal"             cube alone
    14,  # "set of ratios."           all five back together
]

# Beat 2 signs off framed on the cube, and this beat holds that framing: the
# five solids are walked one at a time, not zoomed to one at a time.
_WIDE = framing_zoom(SOLID_R["cube"])
ZOOM = [_WIDE] * 11

PHI_CAM = 67 * DEGREES
THETA_CAM = -96 * DEGREES


class Scene03Ratios(VoiceoverScene, ThreeDScene):
    """Six spheres, six orbits, and the five solids that set their ratios."""

    def construct(self):
        self.set_speech_service(scene_speech_service("ratios"))
        self.set_camera_orientation(phi=PHI_CAM, theta=THETA_CAM, zoom=ZOOM[0],
                                    focal_distance=FOCAL)

        self.add_fixed_in_frame_mobjects(star_field(150, seed=5))
        self.add_fixed_in_frame_mobjects(sun_glow())

        caps = Captions(self, "ratios")
        shells, orbits, solids = full_nest()
        order = [solids[name] for name in NEST_ORDER]

        for shell in shells:
            pin_shell(self, shell)
        self.add(orbits, *order)

        with self.voiceover(text=NARRATION["ratios"]) as tracker:
            caps.start(tracker)
            lead, steps = cue_times(tracker, "ratios", MARKS)
            if lead > 0.05:
                self.wait(lead)

            def step(i, *anims, drift=0.05):
                """One cut, with a slow theta drift so the nest keeps turning."""
                self.move_camera(
                    phi=PHI_CAM, theta=THETA_CAM - drift * sum(steps[:i + 1]),
                    zoom=ZOOM[i], run_time=steps[i],
                    rate_func=rate_functions.linear,
                    added_anims=[spin_orbits(orbits, steps[i]), *anims],
                )

            def only(index):
                """Leave one solid lit and drop the rest back to a whisper."""
                return [
                    solid.animate.set_stroke(opacity=1.0 if k == index else BURIED)
                    for k, solid in enumerate(order)
                ]

            # 0-4 -- the whole model, counted through and then held
            step(0, LaggedStart(*[
                shell[-1].animate.set_stroke(opacity=0.55) for shell in shells
            ], lag_ratio=0.16))
            step(1, *[shell[-1].animate.set_stroke(opacity=0.16)
                      for shell in shells])
            step(2)
            # Brighten the rings only -- set_stroke(width=...) on the whole
            # orbit flattens the trail's gradient back to a flat stroke.
            step(3, *[o[0].animate.set_stroke(opacity=0.50) for o in orbits])
            step(4)

            # 5-9 -- one Platonic solid at a time
            for k in range(5):
                step(5 + k, *only(k))

            # 10 -- and back to the whole model, cube outermost: bringing all
            # five up to full strength at once only makes white noise.
            step(10, *only(len(order) - 1))

        caps.stop()
        self.play(FadeOut(VGroup(orbits, *order, *shells)), run_time=0.45)

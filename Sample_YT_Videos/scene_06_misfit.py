"""Beat 6 -- the theory meets the measurements and loses.

Back on the model.  The claim of the beat is a number, so the beat shows the
number: the camera drops back in on the inner system and lays Kepler's
predicted sphere over the orbit it was supposed to land on, leaving the gap
between the two on screen while the narration names it.
"""

from manim import ThreeDScene, DashedVMobject

from common import *

MARKS = [
    0,   # "And he couldn't get"      the model washes out to the measurements
    1,   # "the theory to fit."       and comes back
    2,   # "It was always off"        in on Venus
    3,   # "by a few percent."        prediction against measurement
]

PHI_CAM = 67 * DEGREES
THETA_CAM = -96 * DEGREES
ZOOM = [framing_zoom(SOLID_R["cube"]), 0.19, 0.75, 1.45]

# Anchored on Mercury, Kepler's octahedron puts Venus's sphere at sqrt(3)
# Mercury radii.  The measured ratio of the semi-major axes is 0.723 / 0.387.
KEPLER_VENUS = SPHERE_R[1]
TRUE_VENUS = SPHERE_R[0] * (0.723 / 0.387)


class Scene06Misfit(VoiceoverScene, ThreeDScene):
    """The predicted sphere, the measured orbit, and the daylight between."""

    def construct(self):
        self.set_speech_service(scene_speech_service("misfit"))
        self.set_camera_orientation(phi=PHI_CAM, theta=THETA_CAM, zoom=ZOOM[0],
                                    focal_distance=FOCAL)

        self.add_fixed_in_frame_mobjects(star_field(150, seed=5))
        self.add_fixed_in_frame_mobjects(sun_glow())

        caps = Captions(self, "misfit")
        shells, orbits, solids = full_nest()
        order = [solids[name] for name in NEST_ORDER]

        for shell in shells:
            pin_shell(self, shell)
        self.add(orbits, *order)

        # What the model promised, against what Tycho measured.
        predicted = DashedVMobject(
            Circle(radius=KEPLER_VENUS, stroke_color=AMBER, stroke_width=4.2,
                   fill_opacity=0.0),
            num_dashes=56, dashed_ratio=0.55,
        )
        predicted.set_shade_in_3d(True).set_z_index(Z_SOLID + 1)
        measured = Circle(radius=TRUE_VENUS, stroke_color=PLANETS[1][1],
                          stroke_width=4.2, fill_opacity=0.0)
        measured.set_shade_in_3d(True).set_z_index(Z_SOLID + 1)

        legend = VGroup(
            kicker("Kepler's sphere", 24, AMBER),
            kicker("Venus, measured", 24, PLANETS[1][1]),
        ).arrange(DOWN, buff=0.20, aligned_edge=LEFT).to_corner(UR, buff=0.55)
        self.add_fixed_in_frame_mobjects(legend)
        legend.set_opacity(0.0)

        with self.voiceover(text=NARRATION["misfit"]) as tracker:
            caps.start(tracker)
            lead, steps = cue_times(tracker, "misfit", MARKS)
            if lead > 0.05:
                self.wait(lead)

            def step(i, *anims):
                self.move_camera(
                    phi=PHI_CAM, theta=THETA_CAM - 0.05 * sum(steps[:i + 1]),
                    zoom=ZOOM[i], run_time=steps[i],
                    rate_func=rate_functions.ease_in_out_sine,
                    added_anims=[spin_orbits(orbits, steps[i]), *anims],
                )

            def solids_at(outer, inner):
                # Only the stroke is touched: these wireframes have no fill, and
                # set_opacity on the shells would drive their soft wash opaque.
                # The cube leads and the buried ones stay buried, so the nest
                # never flattens into five wireframes of equal weight.
                return [s.animate.set_stroke(opacity=outer if k == len(order) - 1
                                             else inner)
                        for k, s in enumerate(order)]

            step(0, *solids_at(0.12, 0.05))
            step(1, *solids_at(1.0, BURIED))
            # Pushing in on Venus takes the camera inside the outer balls,
            # where they stop being spheres and become a grey wash over the
            # whole frame, so they are retired on the way in.
            step(2, *solids_at(0.30, 0.05),
                 *[fade_shell(shells[k], out=True) for k in (3, 4, 5)])
            step(3, Create(predicted), Create(measured),
                 fade_shell(shells[2], out=True),
                 legend.animate.set_opacity(1.0))

        caps.stop()
        self.play(FadeOut(VGroup(orbits, *order, predicted, measured)),
                  *[fade_shell(s, out=True) for s in shells[:2]],
                  legend.animate.set_opacity(0.0), run_time=0.45)

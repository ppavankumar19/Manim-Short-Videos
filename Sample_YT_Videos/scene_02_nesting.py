"""Beat 2 -- the Mysterium Cosmographicum, built inside out.

The spine of the piece.  A sphere goes inside an octahedron, a sphere around
that, an icosahedron around that, and so on out to the cube -- and because
each solid's inradius and circumradius set the two spheres it sits between,
the camera has to pull back across a factor of fourteen to keep up.  The
on-deck solids ride a rail along the top of the frame and drop off it one at a
time as the narration calls them.
"""

from manim import ThreeDScene

from common import *

# Which caption line each step of the build starts on.  Everything downstream
# -- run times, camera moves, when a badge leaves the rail -- is cut to these,
# and the times themselves come from the TTS word boundaries.
MARKS = [
    0,   # "The idea was if you"      sun, inner orbits, Mercury's sphere
    2,   # "inscribed in an"          octahedron
    4,   # "then you fit the"         hold
    6,   # "sphere around that,"      Venus's sphere
    7,   # "and then fit the"         hold
    9,   # "icosahedron"              icosahedron
    11,  # "layer on another"         hold
    12,  # "sphere, and then"         Earth's sphere
    13,  # "a dodecahedron,"          dodecahedron
    14,  # "one more sphere,"         Mars's sphere
    15,  # "then a tetrahedron,"      tetrahedron
    16,  # "one more sphere,"         Jupiter's sphere
    17,  # "a cube, and then"         cube
    18,  # "one final sphere."        Saturn's sphere
]

# The outermost radius on screen at the end of each step -- the newest solid's
# circumradius, or the newest sphere's radius.  `framing_zoom` turns each into
# a camera zoom that holds it at a constant size, so the build never shrinks
# into a tangle however far the nest grows.  Step 0 is framed on the
# octahedron that is about to arrive, so its entrance costs no camera move,
# and step 4 eases part-way to the icosahedron rather than snapping to it.
FRAME_R = [
    SOLID_R["octahedron"],  SOLID_R["octahedron"],
    SOLID_R["octahedron"],  SOLID_R["octahedron"],
    1.95,
    SOLID_R["icosahedron"], SOLID_R["icosahedron"], SOLID_R["icosahedron"],
    SOLID_R["dodecahedron"], SOLID_R["dodecahedron"],
    SOLID_R["tetrahedron"], SOLID_R["tetrahedron"],
    SOLID_R["cube"], SOLID_R["cube"],
]
ZOOM = [framing_zoom(r) for r in FRAME_R]

PHI_CAM = 67 * DEGREES
THETA_CAM = -96 * DEGREES


class Scene02Nesting(VoiceoverScene, ThreeDScene):
    """Every sphere and solid of the nest, dropped in on its own word."""

    def construct(self):
        self.set_speech_service(scene_speech_service("nesting"))
        self.set_camera_orientation(phi=PHI_CAM, theta=THETA_CAM, zoom=ZOOM[0],
                                    focal_distance=FOCAL)

        self.add_fixed_in_frame_mobjects(star_field(150, seed=5))
        self.add_fixed_in_frame_mobjects(sun_glow())

        caps = Captions(self, "nesting")

        rail, badges = queue_rail(NEST_ORDER[1:])   # the octahedron drops first
        self.add_fixed_in_frame_mobjects(rail, badges)
        rail.set_stroke(opacity=0.0)
        badges.set_stroke(opacity=0.0)

        orbits = solar_system().set_z_index(Z_ORBIT)
        shells = [shell_sphere(r).set_z_index(Z_SHELL) for r in SPHERE_R]
        solids = {name: wire_solid(name).set_z_index(Z_SOLID)
                  for name in NEST_ORDER}

        # Pinning a shell also drops it into the scene, so take it straight
        # back out: the beat wants each ball from the moment it fades in, not
        # from the first frame.
        for shell in shells:
            pin_shell(self, shell)
            self.remove(shell)

        # Only the orbits that have been reached are on screen, so the solar
        # system grows with the nest instead of the outer planets sitting there
        # waiting for their solid.
        live = VGroup()

        with self.voiceover(text=NARRATION["nesting"]) as tracker:
            caps.start(tracker)
            lead, steps = cue_times(tracker, "nesting", MARKS)
            if lead > 0.05:
                self.wait(lead)

            def step(i, *anims, spin=True):
                """One cut of the build: its animations plus the camera easing."""
                extra = list(anims)
                if spin and len(live):
                    extra.append(spin_orbits(live, steps[i]))
                self.move_camera(zoom=ZOOM[i], run_time=steps[i],
                                 rate_func=rate_functions.ease_in_out_sine,
                                 added_anims=extra)

            def show_orbit(i):
                live.add(orbits[i])
                return Create(orbits[i])

            def show_shell(i):
                """Bring in one ball, pushing the ones it encloses back.

                Every disc in a ball shares one alpha -- the profile comes from
                how many overlap -- so scaling that alpha dims a whole ball
                without flattening it.  Without this the six balls compose into
                one bright wash instead of the reference clip's single
                dominant sphere with a faint core inside it."""
                return [fade_shell(shells[i]),
                        *[recede_shell(shells[k], i - k) for k in range(i)]]

            def turn(solid, i):
                """Idle rotation, so a hold beat is never a frozen frame."""
                return Rotate(solid, 0.16 * steps[i], axis=OUT,
                              about_point=ORIGIN, run_time=steps[i],
                              rate_func=rate_functions.linear)

            def retire(badge):
                return FadeOut(badge, scale=0.2)

            def bury(*names):
                """Drop the solids a new sphere has just closed over.

                Only the outermost solid is ever drawn at full strength, the
                way the reference clip does it -- otherwise five nested
                wireframes pile up into white noise at the centre."""
                return [solids[n].animate.set_stroke(opacity=BURIED)
                        for n in names]

            # 0 -- the sun, the inner orbits, and the sphere Kepler starts from
            step(0,
                 LaggedStart(show_orbit(0), show_orbit(1), show_orbit(2),
                             show_orbit(3), lag_ratio=0.18),
                 *show_shell(0),
                 rail.animate.set_stroke(opacity=0.7),
                 badges.animate.set_stroke(opacity=1.0),
                 spin=False)

            step(1, Create(solids["octahedron"]))
            # Hold beats turn the solid rather than flashing it: Indicate
            # leaves a shaded-in-3D wireframe stuck on its highlight colour.
            step(2, turn(solids["octahedron"], 2))
            step(3, *show_shell(1), *bury("octahedron"))
            step(4)
            step(5, retire(badges[0]), Create(solids["icosahedron"]))
            step(6, turn(solids["icosahedron"], 6))
            step(7, *show_shell(2), *bury("icosahedron"))
            step(8, retire(badges[1]), Create(solids["dodecahedron"]))
            step(9, *show_shell(3), *bury("dodecahedron"))
            step(10, retire(badges[2]), Create(solids["tetrahedron"]))
            step(11, *show_shell(4), show_orbit(4), *bury("tetrahedron"))
            step(12, retire(badges[3]), Create(solids["cube"]),
                 rail.animate.set_stroke(opacity=0.0))
            step(13, *show_shell(5), show_orbit(5))

        caps.stop()

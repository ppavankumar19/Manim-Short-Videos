"""Beat 8 -- the closing hold.

No narration: the orbits simply keep turning overhead, then fade.  The
reference clip ends on a call to action pointing off-frame; that belongs to
its own channel, so this closes on the astronomy instead.
"""

from manim import ThreeDScene

from common import *

THETA_CAM = -96 * DEGREES
HOLD = 3.2


class Scene08Outro(VoiceoverScene, ThreeDScene):
    """Overhead orbits under the closing call to action."""

    def construct(self):
        self.set_camera_orientation(phi=0.0, theta=THETA_CAM, zoom=0.22,
                                    focal_distance=FOCAL)

        self.add_fixed_in_frame_mobjects(star_field(150, seed=5))
        self.add_fixed_in_frame_mobjects(sun_glow())

        orbits = solar_system().set_z_index(Z_ORBIT)
        self.add(orbits)

        self.play(spin_orbits(orbits, HOLD), run_time=HOLD,
                  rate_func=rate_functions.linear)
        self.play(FadeOut(orbits), run_time=0.9)

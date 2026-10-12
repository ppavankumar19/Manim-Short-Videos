from common import *
from manim import ThreeDScene

# 3D layout: z is up, the ground is the xy-plane, and the whole triangle
# lives in the y = 0 slice — which is exactly why looking down the y-axis
# flattens it into the picture drawn on paper.
H3 = 3.0
D3 = H3 / np.sqrt(3.0)
FOOT3 = np.array([0.0, 0.0, 0.0])
TOP3 = np.array([0.0, 0.0, H3])
OBS3 = np.array([D3, 0.0, 0.0])


def _arc_between(centre, p_from, p_to, radius, color, n=48):
    """An angle arc drawn in the plane of two 3D rays (manim's Angle is 2D)."""
    u = (p_from - centre) / np.linalg.norm(p_from - centre)
    w = (p_to - centre) / np.linalg.norm(p_to - centre)
    n_vec = w - np.dot(w, u) * u
    n_vec = n_vec / np.linalg.norm(n_vec)
    span = float(np.arccos(np.clip(np.dot(u, w), -1.0, 1.0)))
    pts = [centre + radius * (np.cos(t) * u + np.sin(t) * n_vec)
           for t in np.linspace(0.0, span, n)]
    arc = VMobject(stroke_color=color, stroke_width=5)
    arc.set_points_as_corners(pts)
    return arc


class Scene04Space(VoiceoverScene, ThreeDScene):
    """The triangle is not on paper — it is standing on the ground."""

    def construct(self):
        self.set_speech_service(scene_speech_service("space"), create_subcaption=True)
        self.sfx = load_sfx()

        # the triangle sits between z=0 and z=H3, so the camera looks at its
        # middle rather than at the origin
        self.set_camera_orientation(phi=66 * DEGREES, theta=-54 * DEGREES,
                                    zoom=1.05,
                                    frame_center=np.array([0.7, 0.0, 1.30]))

        # --- ground -------------------------------------------------------
        ground = Rectangle(width=7.0, height=6.0, fill_color=GROUND_COLOR,
                           fill_opacity=0.85, stroke_width=0)
        ground.move_to(np.array([1.4, 0.0, 0.0]))
        grid = VGroup()
        for gx in np.arange(-2.0, 5.01, 0.8):
            grid.add(Line(np.array([gx, -3.0, 0.0]), np.array([gx, 3.0, 0.0]),
                          stroke_color=GROUND_HILITE, stroke_width=1.5,
                          stroke_opacity=0.55))
        for gy in np.arange(-3.0, 3.01, 0.8):
            grid.add(Line(np.array([-2.0, gy, 0.0]), np.array([5.0, gy, 0.0]),
                          stroke_color=GROUND_HILITE, stroke_width=1.5,
                          stroke_opacity=0.55))

        tower3 = box3(FOOT3 + np.array([0.0, 0.0, H3 / 2]), 0.62, 0.62, H3,
                      "#5A6675", TOWER_BODY, "#252D38")

        face = face3([FOOT3, OBS3, TOP3], ACCENT, 0.22, 0.0)
        l_h = line3(FOOT3, TOP3, ACCENT, 8.0)
        # lifted a hair off the ground plane so it is not lost to z-fighting
        l_d = line3(FOOT3 + OUT * 0.02, OBS3 + OUT * 0.02, VIOLET, 9.0)
        l_s = line3(OBS3, TOP3, AMBER, 7.0)
        ang3 = _arc_between(OBS3, FOOT3, TOP3, 0.52, SUCCESS)
        obs_mark = dot3(OBS3, SUCCESS, 0.10)

        cap_space = mtx(r"h,\; d,\; \theta \;\in\; \mathbb{R}^3", 40, INK)
        cap_space.to_corner(UR, buff=0.7)
        cap_flat = mtx(r"\tan\theta \;=\; \frac{h}{d}", 52, SUCCESS)
        cap_flat.to_corner(UR, buff=0.7)

        with self.voiceover(text=NARRATION["space"]):
            self.add_sound(self.sfx["whoosh"], gain=-16)
            self.play(FadeIn(ground), Create(grid), run_time=1.7)
            self.play(GrowFromEdge(tower3, IN), run_time=1.7)
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(
                Create(l_h), Create(l_d), Create(l_s),
                FadeIn(face), FadeIn(obs_mark),
                run_time=2.8,
            )
            self.play(Create(ang3), run_time=1.6)
            self.add_fixed_in_frame_mobjects(cap_space)
            self.play(FadeIn(cap_space), run_time=0.8)

            # Orbit, but stay clear of theta = 0 / 180: the triangle lives in
            # the y = 0 plane, so those two angles look straight down its edge
            # and it collapses to a line on screen.
            self.move_camera(theta=-46 * DEGREES, phi=58 * DEGREES, run_time=2.2)
            self.move_camera(theta=-146 * DEGREES, phi=74 * DEGREES, run_time=2.2)

            # settle exactly side-on: the 3D scene becomes the 2D drawing
            self.play(FadeOut(cap_space), run_time=0.4)
            self.move_camera(theta=-90 * DEGREES, phi=90 * DEGREES,
                             zoom=1.25,
                             frame_center=np.array([0.55, 0.0, 1.45]),
                             run_time=6.0)
            self.add_fixed_in_frame_mobjects(cap_flat)
            self.play(
                FadeIn(cap_flat, shift=DOWN * 0.2),
                tower3.animate.set_opacity(0.14),
                run_time=3.6,
            )
            self.play(
                FadeOut(VGroup(ground, grid, tower3, face, l_h, l_d, l_s,
                               ang3, obs_mark, cap_flat)),
                run_time=2.0,
            )
        # beats sized to the sentences they illustrate
        # 1.7+1.7+2.8+1.6+0.8+2.2+2.2+0.4+6.0+3.6+2.0 = 25.0 s

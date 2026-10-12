from common import *

# The whole beat stands in 3D: the triangle is an object in the world, not
# a drawing.  z is up, the ground is the xy-plane, and the figure lives in
# the y = 0 slice, so settling side-on turns it into the picture on paper.
H3 = 3.0                                   # tree height
D3 = 3.4                                   # how far back he walks
# The figure is built centred on x = 0 rather than being pushed back into
# frame with frame_center — that way it sits in the middle of the shot at
# every camera angle instead of drifting to one side.
FOOT = np.array([-D3 / 2, 0.0, 0.0])
TOP = np.array([-D3 / 2, 0.0, H3])
EYE = np.array([D3 / 2, 0.0, 0.0])


class Scene04Trick(VoiceoverScene, ThreeDScene):
    """Walk a distance, look up an angle — the triangle does the rest."""

    def construct(self):
        self.set_speech_service(scene_speech_service("trick"), create_subcaption=True)
        self.sfx = load_sfx()
        stage_3d(self)

        # ONE camera height for the whole beat.  phi never changes and the
        # frame centre never moves, so the figure never drifts out of shot;
        # only theta turns, which is what "seen from all round" needs.
        PHI = 74 * DEGREES
        CENTRE = np.array([0.0, 0.0, 1.30])
        self.set_camera_orientation(phi=PHI, theta=-58 * DEGREES, zoom=0.98,
                                    frame_center=CENTRE)

        # --- the world ----------------------------------------------------
        ground = Rectangle(width=9.0, height=6.5, fill_color=GROUND,
                           fill_opacity=0.9, stroke_width=0)
        ground.move_to(ORIGIN)
        grid = VGroup()
        for gx in np.arange(-4.25, 4.26, 0.85):
            grid.add(Line(np.array([gx, -3.2, 0.0]), np.array([gx, 3.2, 0.0]),
                          stroke_color=GROUND_HI, stroke_width=1.6,
                          stroke_opacity=0.5))
        for gy in np.arange(-3.2, 3.21, 0.85):
            grid.add(Line(np.array([-4.25, gy, 0.0]), np.array([4.25, gy, 0.0]),
                          stroke_color=GROUND_HI, stroke_width=1.6,
                          stroke_opacity=0.5))

        trunk_h = H3 * 0.55
        trunk = box3(FOOT + np.array([0.0, 0.0, trunk_h / 2]),
                     0.34, 0.34, trunk_h, "#A9743A", WOOD, WOOD_DARK)
        # A low-poly fir crown: flat crisp faces instead of a banded Sphere.
        # fir3's top apex sits at base + 1.12*height, so height is chosen to
        # land the tip exactly on TOP — the sight line then reaches the very
        # top of the tree instead of stopping inside the foliage.
        leaves = fir3(FOOT + np.array([0.0, 0.0, trunk_h]),
                      (H3 - trunk_h) / 1.12, 0.92, 3)

        # --- the two things he can measure --------------------------------
        walk = line3(FOOT, EYE, VIOLET, 9.0)
        rise = line3(FOOT, TOP, ACCENT, 9.0)
        sight = line3(EYE, TOP, AMBER, 8.0)
        face = face3([FOOT, EYE, TOP], ACCENT, 0.22, 0.0)
        ang = arc_between_3d(EYE, FOOT, TOP, 0.62, SUCCESS)
        me = dot3(EYE, SUCCESS, 0.11)

        cap1 = chip(txt("the ground you walk", 30, VIOLET))
        cap2 = chip(txt("the angle you look up", 30, SUCCESS))
        cap3 = chip(heading("a real triangle, standing up", SUCCESS, 36))
        for m, y in ((cap1, 3.15), (cap2, 3.15), (cap3, 3.15)):
            self.add_fixed_in_frame_mobjects(m)
            m.move_to(np.array([0.0, y, 0.0]))
            m.set_opacity(0.0)

        with self.voiceover(text=NARRATION["trick"]):
            self.add_sound(self.sfx["whoosh"], gain=-17)
            self.play(FadeIn(ground), Create(grid), run_time=3.17)
            self.play(GrowFromEdge(trunk, IN), FadeIn(leaves), run_time=3.56)
            # he walks back along the ground
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(Create(walk), FadeIn(me), run_time=4.74)
            self.play(cap1.animate.set_opacity(1.0), run_time=1.99)
            # and looks up
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(Create(sight), run_time=6.32)
            self.play(Create(ang), cap1.animate.set_opacity(0.0),
                      cap2.animate.set_opacity(1.0), run_time=2.38)
            # the triangle closes
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(Create(rise), FadeIn(face),
                      cap2.animate.set_opacity(0.0), run_time=0.79)
            self.play(cap3.animate.set_opacity(1.0), run_time=5.93)
            # seen from all round: it is an object, not a drawing
            self.move_camera(theta=-122 * DEGREES, phi=PHI, zoom=0.98,
                             frame_center=CENTRE, run_time=2.77)
            self.move_camera(theta=-90 * DEGREES, phi=PHI, zoom=0.98,
                             frame_center=CENTRE, run_time=4.36)

        # 2.93+3.6+4.95+2.7+3.38+3.82+3.38+2.25+4.5+4.5+0.9 = 36.91 s

        self.play(FadeOut(VGroup(ground, grid, trunk, walk, rise, sight,
                                 face, ang)),
                  FadeOut(leaves), FadeOut(me),
                  cap3.animate.set_opacity(0.0), run_time=0.9)

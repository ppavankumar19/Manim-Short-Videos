from common import *

# Opens looking straight down at the xy-plane, so it reads as a flat page
# until the camera pulls away and the four-bar folds out of it.
#
# The triangle is finished with entirely before the square appears: one
# idea at a time, matching the order the narration says it in.
# A right-angled triangle: 2.8 along the ground, 2.1 standing up.  Every
# triangle in this video has its square corner, because every triangle a
# student will meet in trigonometry does.
TRI = [np.array([-4.45, -1.15, 0.0]),      # the square corner
       np.array([-1.65, -1.15, 0.0]),      # along the ground
       np.array([-4.45, 0.95, 0.0])]       # standing up

QO = np.array([1.15, -1.15, 0.0])
QW, QH = 2.55, 2.10


class Scene02Rigid(VoiceoverScene, ThreeDScene):
    """Three sticks cannot move.  Four sticks will not stay still."""

    def construct(self):
        self.set_speech_service(scene_speech_service("rigid"), create_subcaption=True)
        self.sfx = load_sfx()
        stage_3d(self)

        self.set_camera_orientation(phi=0.0, theta=-90 * DEGREES, zoom=1.0)

        tri = bars3d(TRI, SUCCESS)
        quad = bars3d(quad_pts(QO, QW, QH, 0.0))

        ask = heading("why triangles?", AMBER, 46).move_to(np.array([0.0, 0.35, 0.0]))
        lbl_t = txt("3 sticks", 34, SUCCESS).move_to(np.array([-3.05, 2.45, 0.0]))
        lbl_q = txt("4 sticks", 34, AMBER).move_to(np.array([2.45, 2.45, 0.0]))
        ok = txt("cannot move", 32, SUCCESS).move_to(np.array([-3.05, -2.60, 0.0]))
        bad = txt("wobbles!", 32, ROSE).move_to(np.array([2.45, -2.60, 0.0]))
        law = heading("only a triangle cannot wobble", SUCCESS, 40)
        law.move_to(np.array([0.0, -3.35, 0.0]))
        for m in (ask, lbl_t, lbl_q, ok, bad, law):
            self.add_fixed_in_frame_mobjects(m)
            m.set_opacity(0.0)

        with self.voiceover(text=NARRATION["rigid"]):
            # 1. the question, on its own
            self.add_sound(self.sfx["ding"], gain=-15)
            self.play(ask.animate.set_opacity(1.0), run_time=4.04)

            # 2. THE TRIANGLE, alone
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(ask.animate.set_opacity(0.0),
                      Create(tri), lbl_t.animate.set_opacity(1.0),
                      run_time=4.04)

            # 3. push it — it refuses
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(Wiggle(tri, scale_value=1.02, rotation_angle=0.012),
                      ok.animate.set_opacity(1.0),
                      run_time=4.94)

            # 4. only NOW does the four-bar arrive
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(Create(quad), lbl_q.animate.set_opacity(1.0),
                      run_time=3.59)

            # 5. push it — it leans, still flat
            self.add_sound(self.sfx["whoosh"], gain=-17)
            self.play(
                Succession(
                    Transform(quad, bars3d(quad_pts(QO, QW, QH, 0.42)),
                              run_time=1.10),
                    Transform(quad, bars3d(quad_pts(QO, QW, QH, -0.34)),
                              run_time=1.10),
                    Transform(quad, bars3d(quad_pts(QO, QW, QH, 0.24)),
                              run_time=0.94),
                ),
                bad.animate.set_opacity(1.0),
                run_time=3.14,
            )

            # 6. and it does not even stay on the page
            self.move_camera(phi=70 * DEGREES, theta=-58 * DEGREES,
                             run_time=1.80)
            self.add_sound(self.sfx["swipe"], gain=-16)
            self.play(
                Succession(
                    Transform(quad, bars3d(quad_pts(QO, QW, QH, 0.24, 1.15)),
                              run_time=1.12),
                    Transform(quad, bars3d(quad_pts(QO, QW, QH, 0.24, 0.55)),
                              run_time=1.12),
                ),
                run_time=2.24,
            )

            # 7. the triangle, meanwhile, has not budged
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(Wiggle(tri, scale_value=1.03, rotation_angle=0.015),
                      run_time=4.04)
            self.play(law.animate.set_opacity(1.0), run_time=3.50)
            self.play(
                FadeOut(VGroup(tri, quad)),
                *[m.animate.set_opacity(0.0)
                  for m in (lbl_t, lbl_q, ok, bad, law)],
                run_time=3.67,
            )
        # 4.04+4.04+4.94+3.59+3.14+1.8+2.24+4.04+3.5+3.67 = 35.0 s

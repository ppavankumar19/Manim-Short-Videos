from common import *

# The whole beat lives in 3D, but it opens looking straight down at the
# xy-plane, so it *reads* as a flat page until the camera pulls away and the
# quadrilateral folds out of it.  That fold is the point of the scene.
TRI = [np.array([-4.55, -1.05, 0.0]),
       np.array([-1.75, -1.05, 0.0]),
       np.array([-3.15, 1.35, 0.0])]

L1, L2 = 2.55, 2.10          # the four bar lengths, never changed
QO = np.array([1.05, -1.05, 0.0])


def quad_pts(shear: float, fold: float = 0.0):
    """Four joints of a 4-bar linkage.

    `shear` leans it inside the plane.  `fold` then hinges the last joint
    about the p0-p2 diagonal, which keeps both bars touching that joint at
    their exact lengths while taking the figure genuinely out of the plane —
    the thing a triangle simply cannot do.
    """
    p0 = QO
    p1 = QO + RIGHT * L1
    top = np.array([np.sin(shear) * L2, np.cos(shear) * L2, 0.0])
    p2 = p1 + top
    p3 = p0 + top
    if fold:
        axis = p2 - p0
        u = axis / np.linalg.norm(axis)
        v = p3 - p0
        v_par = np.dot(v, u) * u
        v_perp = v - v_par
        w = np.cross(u, v_perp)
        p3 = p0 + v_par + v_perp * np.cos(fold) + w * np.sin(fold)
    return [p0, p1, p2, p3]


def bars(pts, color=WOOD, diag_opacity: float = 0.0):
    """A linkage as bars with bolted joints, drawn with 3D-safe primitives.

    The bracing diagonal is always built (so every pose has the same
    submobject structure and Transform can morph between them cleanly); it
    is simply invisible until the brace goes in.
    """
    g = VGroup()
    n = len(pts)
    for i in range(n):
        g.add(line3(pts[i], pts[(i + 1) % n], color, 11.0))
    if n == 4:
        brace = line3(pts[1], pts[3], AMBER, 9.0)
        brace.set_stroke(opacity=diag_opacity)
        g.add(brace)
    for p in pts:
        g.add(dot3(p, LEAD, 0.10))
    return g


class Scene02Rigid(VoiceoverScene, ThreeDScene):
    """A triangle cannot move.  A quadrilateral will not stay still."""

    def construct(self):
        self.set_speech_service(scene_speech_service("rigid"), create_subcaption=True)
        self.sfx = load_sfx()

        self.set_camera_orientation(phi=0.0, theta=-90 * DEGREES, zoom=1.0)

        tri = bars(TRI, SUCCESS)
        quad = bars(quad_pts(0.0))

        lbl_t = mtx(r"\triangle", 60, SUCCESS).move_to(np.array([-3.15, 2.55, 0.0]))
        lbl_q = mtx(r"\square", 60, AMBER).move_to(np.array([2.35, 2.55, 0.0]))
        verdict_t = mtx(r"\triangle \;:\; \checkmark", 46, SUCCESS)
        verdict_t.move_to(np.array([-3.15, -2.55, 0.0]))
        verdict_q = mtx(r"\square \;:\; \times", 46, ROSE)
        verdict_q.move_to(np.array([2.35, -2.55, 0.0]))
        for m in (lbl_t, lbl_q, verdict_t, verdict_q):
            self.add_fixed_in_frame_mobjects(m)
            m.set_opacity(0.0)

        law = mtx(r"\square \;\longrightarrow\; "
                  r"\triangle \,+\, \triangle", 48, SUCCESS)
        law.to_edge(DOWN, buff=0.55)
        self.add_fixed_in_frame_mobjects(law)
        law.set_opacity(0.0)

        with self.voiceover(text=NARRATION["rigid"]):
            # 1. the two linkages, seen flat
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(Create(tri), Create(quad),
                      lbl_t.animate.set_opacity(1.0),
                      lbl_q.animate.set_opacity(1.0),
                      run_time=4.0)

            # 2. push the triangle: it refuses
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(Wiggle(tri, scale_value=1.02, rotation_angle=0.012),
                      verdict_t.animate.set_opacity(1.0),
                      run_time=3.0)

            # 3. push the quadrilateral: it leans, still flat
            self.add_sound(self.sfx["whoosh"], gain=-17)
            self.play(
                Succession(
                    Transform(quad, bars(quad_pts(0.42)), run_time=1.6),
                    Transform(quad, bars(quad_pts(-0.34)), run_time=1.6),
                    Transform(quad, bars(quad_pts(0.24)), run_time=1.3),
                ),
                verdict_q.animate.set_opacity(1.0),
                run_time=4.5,
            )

            # 4. and it does not even stay on the page
            self.move_camera(phi=70 * DEGREES, theta=-58 * DEGREES,
                             run_time=2.5)
            self.add_sound(self.sfx["swipe"], gain=-16)
            self.play(
                Succession(
                    Transform(quad, bars(quad_pts(0.24, 1.15)), run_time=2.0),
                    Transform(quad, bars(quad_pts(0.24, 0.55)), run_time=2.0),
                ),
                run_time=4.0,
            )

            # 5. nail one diagonal across it and the floppiness dies
            self.add_sound(self.sfx["ding"], gain=-14)
            fixed = bars(quad_pts(0.24, 0.55), diag_opacity=1.0)
            self.play(Transform(quad, fixed), run_time=2.0)
            self.play(
                Wiggle(quad, scale_value=1.02, rotation_angle=0.012),
                verdict_q.animate.set_opacity(0.0),
                law.animate.set_opacity(1.0),
                run_time=4.0,
            )
            self.play(
                FadeOut(VGroup(tri, quad)),
                lbl_t.animate.set_opacity(0.0),
                lbl_q.animate.set_opacity(0.0),
                verdict_t.animate.set_opacity(0.0),
                law.animate.set_opacity(0.0),
                run_time=2.0,
            )
        # 4.0+3.0+4.5+2.5+4.0+2.0+4.0+2.0 = 26.0 s

from common import *


class Scene00Intro(VoiceoverScene):
    """Why trigonometry: four things you cannot put a tape on."""

    def construct(self):
        self.set_speech_service(scene_speech_service("intro"), create_subcaption=True)
        self.sfx = load_sfx()

        gy = -2.60
        self.add(sky_ground_backdrop(gy))
        stars = star_field(30, y_min=0.2)

        peak_c = np.array([-3.75, gy, 0.0])
        mtn = mountain(peak_c, width=4.6, height=3.05)
        mtn_q = mtx(r"h = \;?", 34, AMBER).move_to(peak_c + UP * 3.45)

        t_foot = np.array([0.45, gy, 0.0])
        t_top = t_foot + UP * 3.05
        tower = realistic_tower(t_foot, t_top, width=0.72)
        tower_q = mtx(r"h = \;?", 34, AMBER).move_to(t_top + UP * 0.85)

        # A lit strip of water so the boat is clearly at sea, not on land.
        sea = Rectangle(width=5.6, height=1.30, fill_color="#123F63",
                        fill_opacity=1, stroke_width=0)
        sea.move_to(np.array([4.5, gy - 0.65, 0.0]))
        swell = VGroup(*[
            Line(np.array([x, gy - 0.30 - 0.34 * (i % 3), 0.0]),
                 np.array([x + 0.55, gy - 0.30 - 0.34 * (i % 3), 0.0]),
                 stroke_color="#3E82B8", stroke_width=3, stroke_opacity=0.75)
            for i, x in enumerate(np.arange(2.1, 6.9, 0.85))
        ])
        # ship() hangs its hull below the given centre, so the centre sits on
        # the waterline, not under it.
        boat = ship(np.array([3.1, gy + 0.14, 0.0]), scale=1.45)
        boat_q = mtx(r"d = \;?", 32, AMBER).move_to(np.array([5.35, gy + 0.70, 0.0]))
        sea_line = Line(np.array([1.95, gy - 0.02, 0.0]),
                        np.array([FRAME_W / 2, gy - 0.02, 0.0]),
                        stroke_color="#6FA8D0", stroke_width=4)

        # A tape that tries to reach the peak and gives up.
        tape = tape_measure(np.array([-0.9, gy + 0.25, 0.0]),
                            np.array([-2.6, gy + 1.1, 0.0]))
        tape_x = VGroup(
            Line(UL * 0.19, DR * 0.19, stroke_color=ROSE, stroke_width=6),
            Line(UR * 0.19, DL * 0.19, stroke_color=ROSE, stroke_width=6),
        ).move_to(np.array([-2.1, gy + 1.35, 0.0]))

        # The closing idea, in symbols.
        tri = Polygon(np.array([-1.9, -1.5, 0.0]), np.array([1.9, -1.5, 0.0]),
                      np.array([-1.9, 1.5, 0.0]),
                      stroke_color=ACCENT, stroke_width=5,
                      fill_color=ACCENT, fill_opacity=0.10)
        tri_ang = Angle(Line(np.array([1.9, -1.5, 0.0]), np.array([-1.9, -1.5, 0.0])),
                        Line(np.array([1.9, -1.5, 0.0]), np.array([-1.9, 1.5, 0.0])),
                        radius=0.62, color=SUCCESS, stroke_width=5, other_angle=True)
        tri_th = mtx(r"\theta", 40, SUCCESS).move_to(np.array([0.72, -1.16, 0.0]))
        lbl_h = mtx(r"h", 44, ACCENT).move_to(np.array([-2.32, 0.0, 0.0]))
        lbl_d = mtx(r"d", 44, VIOLET).move_to(np.array([0.0, -1.95, 0.0]))
        claim = mtx(r"\theta \;\longrightarrow\; h,\; d", 52, AMBER)
        claim.move_to(np.array([0.0, 2.35, 0.0]))

        with self.voiceover(text=NARRATION["intro"]):
            # Each run_time below is the measured length of the sentence it
            # illustrates (taken from the beat's own .srt), so the picture
            # arrives with the words instead of trailing three seconds behind.
            self.play(LaggedStart(*[FadeIn(s, scale=0.4) for s in stars],
                                  lag_ratio=0.03), run_time=0.9)
            self.add_sound(self.sfx["whoosh"], gain=-16)
            self.play(GrowFromEdge(mtn, DOWN), FadeIn(mtn_q, shift=DOWN * 0.3),
                      run_time=2.2)
            self.add_sound(self.sfx["pop"], gain=-16)
            self.play(GrowFromEdge(tower, DOWN), FadeIn(tower_q, shift=DOWN * 0.3),
                      run_time=2.0)
            self.add_sound(self.sfx["whoosh"], gain=-18)
            self.play(
                FadeIn(sea), FadeIn(swell), Create(sea_line),
                boat.animate.shift(RIGHT * 1.35), FadeIn(boat_q),
                run_time=3.0,
            )
            self.add(boat)
            self.add_sound(self.sfx["click"], gain=-16)
            # Create and Wiggle cannot share a mobject in one play() — Create
            # rebuilds the point array Wiggle has already snapshotted.
            self.play(Create(tape), run_time=2.0)
            self.play(Wiggle(tape, scale_value=1.12),
                      FadeIn(tape_x, scale=1.6), run_time=2.2)
            self.add_sound(self.sfx["swipe"], gain=-16)
            self.play(
                FadeOut(VGroup(mtn, mtn_q, tower, tower_q, sea, swell, sea_line,
                               boat, boat_q, tape, tape_x)),
                stars.animate.set_opacity(0.25),
                Create(tri),
                run_time=3.1,
            )
            self.play(Create(tri_ang), FadeIn(tri_th, scale=0.6), run_time=1.8)
            self.play(
                LaggedStart(FadeIn(lbl_h, shift=RIGHT * 0.2),
                            FadeIn(lbl_d, shift=UP * 0.2), lag_ratio=0.45),
                run_time=3.2,
            )
            self.add_sound(self.sfx["ding"], gain=-13)
            self.play(
                Write(claim),
                Flash(tri_ang.get_center(), color=SUCCESS, flash_radius=0.9,
                      num_lines=14, line_length=0.3),
                run_time=4.0,
            )
            self.play(FadeOut(VGroup(tri, tri_ang, tri_th, lbl_h, lbl_d,
                                     claim, stars)),
                      run_time=0.6)
        # 0.9+2.2+2.0+3.0+2.0+2.2+3.1+1.8+3.2+4.0+0.6 = 25.0 s

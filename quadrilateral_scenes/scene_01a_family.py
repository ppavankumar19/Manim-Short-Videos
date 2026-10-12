from common import *

# The context beat.  Six four-sided shapes are laid out on a drafting table
# and the camera starts directly overhead, so the opening frame looks exactly
# like a page of a textbook.  Then the camera tilts and walks sideways: the
# "drawings" turn out to be solid plates with thickness, standing in a space
# the viewer can look around.  Nothing about the mathematics changes -- that
# is the point.  A square is a square from every angle.

COLS = [-4.55, 0.0, 4.55]
ROWS = [2.05, -2.05]
PLACARD_Y = -2.35          # how far in front of a shape its name stands
LIFT = OUT * 0.02          # keeps marks clear of the face they sit on

SLOT = {
    name: np.array([COLS[i % 3], ROWS[i // 3], 0.0])
    for i, name in enumerate(FAMILY_ORDER)
}


def placed(name: str) -> list:
    """The vertex list of one family member, in its slot on the table."""
    return shifted(FAMILY_PTS[name], SLOT[name])


class Scene01aFamily(VoiceoverScene, ThreeDScene):
    """Meet all six quadrilaterals, in three dimensions, before building one."""

    def construct(self):
        self.set_speech_service(scene_speech_service("family"), create_subcaption=True)
        self.sfx = load_sfx()

        self.set_camera_orientation(phi=0.0, theta=-90 * DEGREES, zoom=1.0)
        table = table_top()
        self.add(table)

        plates = {n: plate(placed(n), FAMILY_COLOR[n]) for n in FAMILY_ORDER}
        names = {
            n: placard(txt(FAMILY_NAME[n], 26, FAMILY_COLOR[n], "BOLD"),
                       SLOT[n] + np.array([0.0, PLACARD_Y, 0.0]), lift=0.22)
            for n in FAMILY_ORDER
        }
        diags = {
            n: diagonals([p + LIFT for p in plate_top(placed(n))], MUTED, 2.6)
            for n in FAMILY_ORDER
        }

        # The angle sum names four corners, so one figure on the table is
        # actually lettered A, B, C, D -- otherwise the formula is talking
        # about corners nothing on screen has named.
        abcd = corner_letters([p + LIFT for p in plate_top(placed("trapezium"))],
                              color=VIOLET, size=34, buff=0.50)

        title = heading("The Quadrilateral Family", ACCENT)
        # the count sits in the corner, clear of the table and the placards
        count = mtx(r"n = 4", 40, AMBER).to_edge(UP, buff=0.45)
        count.shift(RIGHT * 5.6)
        angle_sum = mtx(r"\angle A + \angle B + \angle C + \angle D "
                        r"= 360^\circ", 44, SUCCESS)
        angle_sum.to_edge(DOWN, buff=0.60)
        for m in (title, count, angle_sum):
            self.add_fixed_in_frame_mobjects(m)
            m.set_opacity(0.0)

        with self.voiceover(text=NARRATION["family"]):
            # 1. seen from directly above, they are just six drawings
            self.add_sound(self.sfx["whoosh"], gain=-16)
            self.play(
                title.animate.set_opacity(1.0),
                LaggedStart(*[GrowFromCenter(plates[n]) for n in FAMILY_ORDER],
                            lag_ratio=0.22),
                run_time=6.0,
            )

            # 2. the camera leaves the page and they become solids
            self.add_sound(self.sfx["swipe"], gain=-16)
            self.move_camera(phi=55 * DEGREES, theta=-90 * DEGREES, run_time=5.0)

            # 3. name every one of them
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(
                LaggedStart(*[FadeIn(names[n], shift=OUT * 0.30)
                              for n in FAMILY_ORDER], lag_ratio=0.20),
                count.animate.set_opacity(1.0),
                run_time=5.5,
            )

            # 4. walk around them: same six shapes, a different viewpoint
            self.add_sound(self.sfx["pop"], gain=-17)
            self.move_camera(
                theta=-78 * DEGREES,
                added_anims=[
                    LaggedStart(*[Indicate(plates[n], color=FAMILY_COLOR[n],
                                           scale_factor=1.08)
                                  for n in FAMILY_ORDER], lag_ratio=0.16),
                ],
                run_time=7.0,
            )

            # 5. what every one of them shares: four corners, and 360 degrees
            self.add_sound(self.sfx["ding"], gain=-14)
            # the names have done their job; clearing them leaves the frame
            # to the one fact that is true of every plate on the table
            self.play(
                LaggedStart(*[Create(diags[n]) for n in FAMILY_ORDER],
                            lag_ratio=0.14),
                FadeIn(abcd),
                FadeOut(VGroup(*names.values())),
                angle_sum.animate.set_opacity(1.0),
                count.animate.set_opacity(0.0),
                run_time=8.0,
            )

            self.move_camera(
                theta=-90 * DEGREES,
                added_anims=[
                    FadeOut(VGroup(*plates.values(), *diags.values(), abcd)),
                    title.animate.set_opacity(0.0),
                    angle_sum.animate.set_opacity(0.0),
                ],
                run_time=5.5,
            )
            self.remove(table)
        # 6.0+5.0+5.5+7.0+8.0+5.5 = 37.0 s

from common import *

# Three of the six, in the order in which conditions are given up: square,
# rectangle, parallelogram.  Each one is marked with the notation a student
# will meet in the textbook -- ticks for equal sides, a small square for a
# right angle, chevrons for parallel -- so the difference between them is
# visible on the figure rather than asserted in a caption.

COLS = [-4.60, 0.0, 4.60]
ROW_Y = 0.55
PLACARD_Y = -2.30
LIFT = OUT * 0.02
SHOWN = ["square", "rectangle", "parallelogram"]

SLOT = {n: np.array([COLS[i], ROW_Y, 0.0]) for i, n in enumerate(SHOWN)}


def placed(name: str) -> list:
    return shifted(FAMILY_PTS[name], SLOT[name])


class Scene01bTypesA(VoiceoverScene, ThreeDScene):
    """Square, rectangle, parallelogram: what survives each relaxation."""

    def construct(self):
        self.set_speech_service(scene_speech_service("typesa"), create_subcaption=True)
        self.sfx = load_sfx()

        self.set_camera_orientation(phi=54 * DEGREES, theta=-90 * DEGREES)
        table = table_top()
        self.add(table)

        plates, names, tops = {}, {}, {}
        for n in SHOWN:
            plates[n] = plate(placed(n), FAMILY_COLOR[n], opacity=0.45)
            names[n] = placard(txt(FAMILY_NAME[n], 26, MUTED, "BOLD"),
                               SLOT[n] + np.array([0.0, PLACARD_Y, 0.0]),
                               lift=0.22)
            tops[n] = [p + LIFT for p in plate_top(placed(n))]

        # a, b, c, d on the figure itself, in the shape's own colour, so the
        # condition written along the bottom of the frame can be read off the
        # picture instead of taken on trust
        letters = {n: side_letters(tops[n], color=FAMILY_COLOR[n], size=34,
                                   buff=0.52)
                   for n in SHOWN}

        title = heading("Which conditions hold?", ACCENT)
        rule = mtx(FAMILY_RULE["square"], 46, ACCENT).to_edge(DOWN, buff=0.62)
        for m in (title, rule):
            self.add_fixed_in_frame_mobjects(m)
            m.set_opacity(0.0)

        # --- the marks, one set per shape -----------------------------------
        sq = tops["square"]
        sq_marks = VGroup(
            *[ticks(sq[i], sq[(i + 1) % 4], 1, INK) for i in range(4)],
            *[corner_mark(sq[i], sq[(i - 1) % 4], sq[(i + 1) % 4], 0.26, INK)
              for i in range(4)],
        )

        rc = tops["rectangle"]
        rc_marks = VGroup(
            ticks(rc[0], rc[1], 1, INK), ticks(rc[2], rc[3], 1, INK),
            ticks(rc[1], rc[2], 2, INK), ticks(rc[3], rc[0], 2, INK),
            *[corner_mark(rc[i], rc[(i - 1) % 4], rc[(i + 1) % 4], 0.26, INK)
              for i in range(4)],
        )

        pa = tops["parallelogram"]
        pa_marks = VGroup(
            chevrons(pa[0], pa[1], 1, INK), chevrons(pa[3], pa[2], 1, INK),
            chevrons(pa[1], pa[2], 2, INK), chevrons(pa[0], pa[3], 2, INK),
        )
        # the right angle is exactly what a parallelogram has given up, so the
        # corners are drawn as the angles they actually are, not as claims
        pa_angles = VGroup(
            angle_arc(pa[0], pa[3], pa[1], 0.46, ROSE),
            angle_arc(pa[2], pa[1], pa[3], 0.46, ROSE),
            ticks(pa[0] + (pa[1] - pa[0]) * 0.16,
                  pa[0] + (pa[3] - pa[0]) * 0.16, 1, ROSE, 0.09, 0.09, 3.0),
            ticks(pa[2] + (pa[3] - pa[2]) * 0.16,
                  pa[2] + (pa[1] - pa[2]) * 0.16, 1, ROSE, 0.09, 0.09, 3.0),
        )

        with self.voiceover(text=NARRATION["typesa"]):
            self.add_sound(self.sfx["whoosh"], gain=-16)
            self.play(
                title.animate.set_opacity(1.0),
                LaggedStart(*[FadeIn(plates[n], shift=OUT * 0.4) for n in SHOWN],
                            lag_ratio=0.18),
                LaggedStart(*[FadeIn(names[n]) for n in SHOWN], lag_ratio=0.18),
                run_time=4.6,
            )

            # 1. the square: everything equal, everything square
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(
                plates["square"].animate.set_opacity(0.95),
                names["square"].animate.set_color(ACCENT),
                rule.animate.set_opacity(1.0),
                run_time=1.6,
            )
            self.play(Create(sq_marks),
                      FadeIn(letters["square"]), run_time=4.0)
            self.play(Indicate(plates["square"], color=ACCENT,
                               scale_factor=1.05), run_time=1.8)

            # 2. the rectangle: keep the corners, let the sides differ
            self.add_sound(self.sfx["click"], gain=-17)
            new_rule = mtx(FAMILY_RULE["rectangle"], 46, SUCCESS)
            new_rule.to_edge(DOWN, buff=0.62)
            self.add_fixed_in_frame_mobjects(new_rule)
            new_rule.set_opacity(0.0)
            self.play(
                plates["square"].animate.set_opacity(0.45),
                names["square"].animate.set_color(MUTED),
                VGroup(sq_marks, letters["square"]).animate.set_opacity(0.25),
                plates["rectangle"].animate.set_opacity(0.95),
                names["rectangle"].animate.set_color(SUCCESS),
                rule.animate.set_opacity(0.0),
                new_rule.animate.set_opacity(1.0),
                run_time=2.0,
            )
            self.play(Create(rc_marks),
                      FadeIn(letters["rectangle"]), run_time=4.1)
            self.play(Indicate(plates["rectangle"], color=SUCCESS,
                               scale_factor=1.05), run_time=1.8)

            # 3. the parallelogram: let the corners tilt as well
            self.add_sound(self.sfx["swipe"], gain=-16)
            last_rule = mtx(FAMILY_RULE["parallelogram"], 42, AMBER)
            last_rule.to_edge(DOWN, buff=0.62)
            self.add_fixed_in_frame_mobjects(last_rule)
            last_rule.set_opacity(0.0)
            self.play(
                plates["rectangle"].animate.set_opacity(0.45),
                names["rectangle"].animate.set_color(MUTED),
                VGroup(rc_marks, letters["rectangle"]).animate.set_opacity(0.25),
                plates["parallelogram"].animate.set_opacity(0.95),
                names["parallelogram"].animate.set_color(AMBER),
                new_rule.animate.set_opacity(0.0),
                last_rule.animate.set_opacity(1.0),
                run_time=2.0,
            )
            self.play(Create(pa_marks),
                      FadeIn(letters["parallelogram"]),
                      run_time=3.2)
            self.add_sound(self.sfx["pop"], gain=-17)
            no_right = mtx(r"\angle A = \angle C \ne 90^\circ", 40, ROSE)
            no_right.to_edge(DOWN, buff=1.55)
            self.add_fixed_in_frame_mobjects(no_right)
            no_right.set_opacity(0.0)
            self.play(Create(pa_angles), no_right.animate.set_opacity(1.0),
                      run_time=1.2)
            # a wiggle, not a colour flash: the rose angle arcs have to stay
            # readable, and leaning the shape is the honest gesture anyway
            self.play(Wiggle(plates["parallelogram"], scale_value=1.03,
                             rotation_angle=0.02), run_time=1.2)

            self.play(
                FadeOut(VGroup(*plates.values(), *names.values(),
                               sq_marks, rc_marks, pa_marks, pa_angles,
                               *letters.values())),
                no_right.animate.set_opacity(0.0),
                title.animate.set_opacity(0.0),
                last_rule.animate.set_opacity(0.0),
                run_time=2.0,
            )
            self.remove(table)
        # 4.6+1.6+4.0+1.8+2.0+4.1+1.8+2.0+3.2+1.2+1.2+2.0 = 29.5 s

from common import *

# The other branch of the family: rhombus, trapezium, kite.  Each keeps less
# than the one before it, and the marks show exactly what is left -- four
# equal sides, then one parallel pair, then only two pairs of equal
# neighbours.  By the end the viewer has seen how little a shape needs in
# order to still be a quadrilateral, which is the reason the construction
# beats need five measurements to pin one down.

COLS = [-4.60, 0.0, 4.60]
ROW_Y = 0.55
PLACARD_Y = -2.30
LIFT = OUT * 0.02
SHOWN = ["rhombus", "trapezium", "kite"]

SLOT = {n: np.array([COLS[i], ROW_Y, 0.0]) for i, n in enumerate(SHOWN)}


def placed(name: str) -> list:
    return shifted(FAMILY_PTS[name], SLOT[name])


class Scene01cTypesB(VoiceoverScene, ThreeDScene):
    """Rhombus, trapezium, kite: fewer conditions, more freedom."""

    def construct(self):
        self.set_speech_service(scene_speech_service("typesb"), create_subcaption=True)
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

        # the same lettering as the first branch, so a, b, c and d mean the
        # same thing across both halves of the family
        letters = {n: side_letters(tops[n], color=FAMILY_COLOR[n], size=34,
                                   buff=0.52)
                   for n in SHOWN}

        title = heading("Which conditions hold?", ACCENT)
        self.add_fixed_in_frame_mobjects(title)
        title.set_opacity(0.0)

        # --- rhombus: four equal sides, and diagonals that cross square ------
        rh = tops["rhombus"]
        rh_marks = VGroup(*[ticks(rh[i], rh[(i + 1) % 4], 1, INK)
                            for i in range(4)])
        rh_diag = diagonals(rh, ROSE, 3.0, dash=False)
        centre_rh = (rh[0] + rh[2]) / 2.0
        rh_perp = corner_mark(centre_rh, rh[0], rh[1], 0.22, INK)

        # --- trapezium: one parallel pair, and nothing else promised ---------
        tr = tops["trapezium"]
        tr_marks = VGroup(chevrons(tr[0], tr[1], 1, INK),
                          chevrons(tr[3], tr[2], 1, INK))
        tr_free = VGroup(
            Line(tr[1], tr[2], stroke_color=ROSE, stroke_width=6),
            Line(tr[3], tr[0], stroke_color=ROSE, stroke_width=6),
        )

        # --- kite: two pairs of equal neighbours, no parallel pair at all ----
        kt = tops["kite"]
        kt_marks = VGroup(
            ticks(kt[0], kt[1], 1, INK), ticks(kt[3], kt[0], 1, INK),
            ticks(kt[1], kt[2], 2, INK), ticks(kt[2], kt[3], 2, INK),
        )
        kt_axis = DashedLine(kt[0], kt[2], stroke_color=TEAL, stroke_width=3.5)

        def rule_at(name: str, size: int = 46) -> MathTex:
            m = mtx(FAMILY_RULE[name], size, FAMILY_COLOR[name])
            m.to_edge(DOWN, buff=0.62)
            self.add_fixed_in_frame_mobjects(m)
            m.set_opacity(0.0)
            return m

        r_rh, r_tr, r_kt = (rule_at("rhombus"), rule_at("trapezium"),
                            rule_at("kite"))

        with self.voiceover(text=NARRATION["typesb"]):
            self.add_sound(self.sfx["whoosh"], gain=-16)
            self.play(
                title.animate.set_opacity(1.0),
                LaggedStart(*[FadeIn(plates[n], shift=OUT * 0.4) for n in SHOWN],
                            lag_ratio=0.18),
                LaggedStart(*[FadeIn(names[n]) for n in SHOWN], lag_ratio=0.18),
                run_time=3.6,
            )

            # 1. the rhombus
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(
                plates["rhombus"].animate.set_opacity(0.95),
                names["rhombus"].animate.set_color(ROSE),
                r_rh.animate.set_opacity(1.0),
                run_time=1.6,
            )
            self.play(Create(rh_marks),
                      FadeIn(letters["rhombus"]), run_time=2.8)
            self.play(Create(rh_diag), FadeIn(rh_perp), run_time=2.4)

            # 2. the trapezium
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(
                plates["rhombus"].animate.set_opacity(0.45),
                names["rhombus"].animate.set_color(MUTED),
                VGroup(rh_marks, rh_diag, rh_perp,
                       letters["rhombus"]).animate.set_opacity(0.25),
                plates["trapezium"].animate.set_opacity(0.95),
                names["trapezium"].animate.set_color(VIOLET),
                r_rh.animate.set_opacity(0.0),
                r_tr.animate.set_opacity(1.0),
                run_time=1.8,
            )
            self.play(Create(tr_marks),
                      FadeIn(letters["trapezium"]), run_time=2.4)
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(ShowPassingFlash(tr_free.copy().set_color(ROSE),
                                       time_width=0.6), run_time=1.8)

            # 3. the kite
            self.add_sound(self.sfx["swipe"], gain=-16)
            self.play(
                plates["trapezium"].animate.set_opacity(0.45),
                names["trapezium"].animate.set_color(MUTED),
                VGroup(tr_marks, letters["trapezium"]).animate.set_opacity(0.25),
                plates["kite"].animate.set_opacity(0.95),
                names["kite"].animate.set_color(TEAL),
                r_tr.animate.set_opacity(0.0),
                r_kt.animate.set_opacity(1.0),
                run_time=1.8,
            )
            self.play(Create(kt_marks),
                      FadeIn(letters["kite"]), run_time=2.6)
            self.play(Create(kt_axis), run_time=1.2)
            self.play(Indicate(plates["kite"], color=TEAL, scale_factor=1.06),
                      run_time=1.4)

            self.play(
                FadeOut(VGroup(*plates.values(), *names.values(),
                               rh_marks, rh_diag, rh_perp, tr_marks,
                               kt_marks, kt_axis, *letters.values())),
                title.animate.set_opacity(0.0),
                r_kt.animate.set_opacity(0.0),
                run_time=2.0,
            )
            self.remove(table)
        # 3.6+1.6+2.8+2.4+1.8+2.4+1.8+1.8+2.6+1.2+1.4+2.0 = 25.4 s

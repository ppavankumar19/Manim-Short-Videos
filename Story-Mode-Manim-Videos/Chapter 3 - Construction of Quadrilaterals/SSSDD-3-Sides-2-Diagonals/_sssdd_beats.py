"""Scene beats for Storyboard 04 (S.S.S.D.D)."""

    # ================================================================ beats ==

    def compass_on(self, centre, target, radius, spread, color,
                   hinge_dir=None, leg_ratio=0.62, bias: float = 0.0):
        """Put a pair of compasses on the board with its needle on `centre` and
        its pencil at the start of the arc, ready to sweep.

        The sector is centred on the direction of `target` (so the arc really
        passes through the point being located); `bias` rotates the whole
        sector by that many degrees when one tail of a symmetric arc would
        stray over the figure or off the board."""
        C = np.array(centre, dtype=float)
        ang = float(np.degrees(np.arctan2(target[1] - C[1], target[0] - C[0])))
        start = ang - spread + bias
        sweep = ValueTracker(0.004)

        def tip_at():
            a = (start + sweep.get_value()) * DEGREES
            return C + radius * np.array([np.cos(a), np.sin(a), 0.0])

        arc = always_redraw(lambda: Arc(
            radius=radius, start_angle=start * DEGREES,
            angle=max(sweep.get_value(), 0.004) * DEGREES, arc_center=C,
            color=color, stroke_width=2.8))
        tool = always_redraw(lambda: compass_tool(
            C, tip_at(), hinge_dir=hinge_dir, leg_ratio=leg_ratio))
        self.add(arc, tool)
        self.arc, self.tool, self.sweep = arc, tool, sweep
        return sweep

    def put_down_tool(self, tool, run_time: float = 0.3) -> None:
        """Lay a pair of compasses down on the desk.

        The tool is an `always_redraw` mobject: its updater rebuilds it at full
        opacity on every frame, so `FadeOut` on the live object never shows and
        the compasses stayed standing on the board over the finished drawing.
        Fade a static copy instead and drop the live one."""
        snap = tool.copy()
        snap.clear_updaters()
        self.remove(tool)
        self.add(snap)
        self.play(FadeOut(snap), run_time=run_time)

    def sweep_compass(self, tracker, mark: str, spread: float,
                      put_down: bool = True, reserve: float = 0.0,
                      hold: bool = True) -> None:
        """Sweep the compasses already on the board to the end of the arc, then
        (by default) lay them down -- all inside the current window.  `reserve`
        keeps that many seconds of the window for the animation that follows
        (a note appearing, the second arc of the pair), and `hold=False` leaves
        that remainder to the caller instead of waiting it out."""
        budget = leftover(tracker, mark)
        sweep_time = max(budget - (0.35 if put_down else 0.0) - reserve, 0.4)
        self.play(self.sweep.animate.set_value(2 * spread), run_time=sweep_time)
        if put_down:
            self.put_down_tool(self.tool)
        if hold:
            self.wait(leftover(tracker, mark))

    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Construct a Quadrilateral", 33, CHALK_WHITE,
                               "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 1.85, 0]))
            sub = board_text("Three Sides and Two Diagonals", 20,
                             CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 0.95, 0]))
            self.play(FadeIn(title, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(sub, color=CHALK_YELLOW, scale_factor=1.04),
                      run_time=max(leftover(tracker, "b0"), 0.4))
            self.add_sound(self.sfx["ding"], gain=-13)

            # the defining measurements of THIS case are the two diagonals
            A, B, C, D = example_frame(origin=np.array([BOARD_CX - 1.0, -0.72, 0]),
                                       scale=0.26)
            outline = Polygon(A, B, C, D, color=CHALK_WHITE, stroke_width=2.2,
                              fill_color=CHALK_WHITE, fill_opacity=0.05)
            outline.set_stroke(opacity=0.45)
            diag = VGroup(Line(A, C, color=CHALK_YELLOW, stroke_width=3.0),
                          Line(B, D, color=CHALK_AMBER, stroke_width=3.0))
            names = diamond_names(A, B, C, D, "ABCD", 14, pull=0.05)
            tag = board_text("Analyse → Triangle → Arcs → Join", 18,
                             CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))
            self.play(FadeIn(outline), FadeIn(names), run_time=min(
                leftover(tracker, "b1"), 1.0))
            self.play(Create(diag), run_time=0.8)
            self.play(Flash(diag, color=CHALK_YELLOW, flash_radius=0.7),
                      run_time=0.6)
            self.appear(tag, tracker, "b1", 0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: three sides and two diagonals ------------------------------
    def beat1_data(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("Three Sides and Two Diagonals", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            # each caption sits directly above its own row with the same
            # ~0.2 gap, so "2 diagonals" can no longer read as part of the
            # three-side row above it
            lab_sides = board_text("3 sides", 17, CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX, 2.20, 0]))
            sides = VGroup(
                measure_card(r"AB=4.5", CHALK_CYAN),
                measure_card(r"BC=5.2", CHALK_CYAN),
                measure_card(r"CD=4.8", CHALK_CYAN),
            ).arrange(RIGHT, buff=0.30).move_to(
                np.array([BOARD_CX, 1.68, 0]))
            lab_diags = board_text("2 diagonals", 17, CHALK_AMBER, "BOLD"
                                   ).move_to(np.array([BOARD_CX, 1.13, 0]))
            diags = VGroup(
                measure_card(r"AC=5", CHALK_YELLOW),
                measure_card(r"BD=5.4", CHALK_AMBER),
            ).arrange(RIGHT, buff=0.30).move_to(
                np.array([BOARD_CX, 0.60, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(lab_sides), run_time=0.35)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.12)
                                    for c in sides], lag_ratio=0.25),
                      run_time=1.0)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.wait(leftover(tracker, "b0b"))
            self.play(FadeIn(lab_diags), run_time=0.35)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.12)
                                    for c in diags], lag_ratio=0.30),
                      run_time=0.9)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b1"))

            strip = board_text("3 Sides + 2 Diagonals", 21, CHALK_GREEN, "BOLD"
                               ).move_to(np.array([BOARD_CX, -1.75, 0]))
            box = SurroundingRectangle(strip, color=CHALK_GREEN, buff=0.16,
                                       corner_radius=0.1, stroke_width=2.6)
            self.play(FadeIn(strip, shift=UP * 0.1), Create(box), run_time=0.6)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["click"], gain=-15)

            ask = board_text("Which three should we use first?", 19,
                             CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.50, 0]))
            self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: find the triangle whose three lengths are known ------------
    def beat2_choose(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("Find a Complete Triangle", 22, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            A, B, C, D = example_frame()
            full = Polygon(A, B, C, D, color=CHALK_WHITE, stroke_width=2.0,
                           fill_opacity=0.0)
            full.set_stroke(opacity=0.28)
            names = diamond_names(A, B, C, D, "ABCD", 17)
            tri = Polygon(A, B, C, color=CHALK_CYAN, stroke_width=3.0,
                          fill_color=CHALK_CYAN, fill_opacity=0.16)
            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=4.0)
            bc = Line(B, C, color=CHALK_YELLOW, stroke_width=4.0)
            diag = Line(A, C, color=CHALK_YELLOW, stroke_width=4.0)
            diamond_line = Line(B, D, color=CHALK_AMBER, stroke_width=2.6)
            diamond_line.set_stroke(opacity=0.45)
            centroid = np.array([A, B, C, D], dtype=float).mean(axis=0)
            lab_ab = side_label(A, B, centroid, "4.5", CHALK_YELLOW, 16, 0.18)
            lab_bc = side_label(B, C, centroid, "5.2", CHALK_YELLOW, 16, 0.18)
            lab_ac = board_text("AC = 5", 16, CHALK_YELLOW, "BOLD").move_to(
                (A + C) / 2 + DOWN * 0.62)
            sss = combo_card("Side + Side + Side", "three known lengths",
                              CHALK_GREEN).move_to(
                np.array([BOARD_CX + 3.1, 0.55, 0]))
            note = board_text("One diagonal turns two sides into a triangle.",
                              18, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(full), FadeIn(names), FadeIn(diamond_line),
                      run_time=0.7)
            self.play(FadeIn(tri), run_time=0.5)
            self.play(Create(ab), FadeIn(lab_ab), run_time=0.7)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(Create(bc), FadeIn(lab_bc), run_time=0.7)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            self.play(Create(diag), FadeIn(lab_ac), run_time=0.7)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeIn(sss, shift=RIGHT * 0.12), FadeIn(note, shift=UP * 0.1),
                      Circumscribe(tri, color=CHALK_CYAN, stroke_width=2.6,
                                   time_width=0.6),
                      run_time=0.9)
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: the 3 + 2 plan ---------------------------------------------
    def beat3_plan(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()

            heading = board_text("3 Build. 2 Locate.", 23, CHALK_AMBER, "BOLD"
                                 ).move_to(np.array([BOARD_CX, 2.72, 0]))
            build_cards = VGroup(
                measure_card(r"AB=4.5", CHALK_YELLOW),
                measure_card(r"BC=5.2", CHALK_YELLOW),
                measure_card(r"AC=5", CHALK_YELLOW),
            ).arrange(DOWN, buff=0.22).move_to(
                np.array([BOARD_CX - 2.6, 0.55, 0]))
            locate_cards = VGroup(
                measure_card(r"CD=4.8", CHALK_CYAN),
                measure_card(r"BD=5.4", CHALK_AMBER),
            ).arrange(DOWN, buff=0.22).move_to(
                np.array([BOARD_CX + 2.7, 0.75, 0]))
            lab_build = board_text("BUILD", 18, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX - 2.6, 1.85, 0]))
            lab_locate = board_text("LOCATE", 18, CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX + 2.7, 1.75, 0]))
            tri = Polygon(np.array([-0.7, -1.4, 0]), np.array([0.05, 0.35, 0]),
                          np.array([0.8, -1.4, 0]), color=CHALK_CYAN,
                          stroke_width=2.6, fill_color=CHALK_CYAN,
                          fill_opacity=0.16)
            tri.move_to(np.array([BOARD_CX - 2.6, -1.45, 0]))
            tri.scale(0.65)
            d_dot = Dot(radius=0.09, color=CHALK_YELLOW).move_to(
                np.array([BOARD_CX + 2.7, -1.0, 0]))
            d_lab = board_text("D", 17, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX + 2.95, -1.0, 0]))
            flow = board_text("3 measurements → triangle → 2 measurements → D",
                              17, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.45, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(lab_build), run_time=0.35)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.12)
                                    for c in build_cards], lag_ratio=0.25),
                      run_time=1.0)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(Create(tri), run_time=0.8)
            self.wait(leftover(tracker, "b1"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(lab_locate), run_time=0.35)
            self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.12)
                                    for c in locate_cards], lag_ratio=0.30),
                      run_time=0.9)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeIn(d_dot, scale=0.5), FadeIn(d_lab),
                      Circumscribe(d_dot, color=CHALK_YELLOW, fade_out=True),
                      run_time=0.7)
            self.play(FadeIn(flow, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: draw the diagonal and the first arc ------------------------
    def beat4_diagonal(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 1 — Draw the Diagonal AC", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            A, B, C, D = example_frame()
            base = Line(A, C, color=CHALK_WHITE, stroke_width=4.5)
            names = VGroup(vertex_label("A", A, "UL"), vertex_label("C", C, "DR"))
            lab_ac = board_text("AC = 5 cm", 17, CHALK_CYAN, "BOLD").move_to(
                (A + C) / 2 + DOWN * 0.62)
            note = board_text("Every point on this arc is 4.5 cm from A.", 18,
                              CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(Create(base), FadeIn(names), FadeIn(lab_ac), run_time=0.8)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.wait(leftover(tracker, "b1"))
            self.compass_on(A, B, 4.5 * SCALE, 17, CHALK_CYAN,
                            hinge_dir=(1.0, -1.0, 0.0))
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.sweep_compass(tracker, "b3", 17, reserve=0.5, hold=False)
            self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: the second arc fixes B -------------------------------------
    def beat5_triangle(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 2 — Complete the Triangle", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            A, B, C, D = example_frame()
            base = Line(A, C, color=CHALK_WHITE, stroke_width=4.5)
            names = VGroup(vertex_label("A", A, "UL"), vertex_label("C", C, "DR"))
            lab_ac = board_text("AC = 5 cm", 17, CHALK_CYAN, "BOLD").move_to(
                (A + C) / 2 + DOWN * 0.62)
            arc_a = locating_arc(A, B, 4.5 * SCALE, 17, CHALK_CYAN)
            b_dot = Dot(radius=0.09, color=CHALK_YELLOW).move_to(B)
            # directly above B, in the wedge the two arcs open upwards: the
            # series' up-right slot put the letter on the arcs themselves
            b_name = board_text("B", 18, CHALK_WHITE, "BOLD").move_to(
                B + np.array([0.0, 0.30, 0]))
            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=4.0)
            bc = Line(B, C, color=CHALK_YELLOW, stroke_width=4.0)
            tri = Polygon(A, B, C, color=CHALK_CYAN, stroke_width=2.6,
                          fill_color=CHALK_CYAN, fill_opacity=0.16)
            centroid = np.array([A, B, C, D], dtype=float).mean(axis=0)
            lab_ab = side_label(A, B, centroid, "AB = 4.5 cm", CHALK_YELLOW, 16,
                                0.18)
            lab_bc = side_label(C, B, B + C - centroid, "BC = 5.2 cm",
                                CHALK_YELLOW, 16, 0.18)
            note = board_text("Three sides fix this triangle.", 19, CHALK_GREEN,
                              "BOLD").move_to(np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(Create(base), FadeIn(names), FadeIn(lab_ac), run_time=0.8)
            self.play(Create(arc_a), run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.compass_on(C, B, 5.2 * SCALE, 15, CHALK_GREEN,
                            hinge_dir=(1.0, 1.0, 0.0))
            self.sweep_compass(tracker, "b1", 15)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(FadeIn(b_dot, scale=0.5), FadeIn(b_name),
                      Indicate(b_dot, color=CHALK_YELLOW, scale_factor=1.9),
                      run_time=min(leftover(tracker, "b2"), 1.0))
            self.play(Create(ab), FadeIn(lab_ab), Create(bc), FadeIn(lab_bc),
                      run_time=min(leftover(tracker, "b2"), 1.2))
            self.play(FadeIn(tri), run_time=0.6)
            self.play(FadeIn(note, shift=UP * 0.1),
                      Flash(tri, color=CHALK_CYAN, flash_radius=0.7),
                      run_time=0.8)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: the side and the diagonal locate D -------------------------
    def beat6_locate_d(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 3 — Locate D", 22, CHALK_AMBER, "BOLD"
                                 ).move_to(np.array([BOARD_CX, 2.72, 0]))
            A, B, C, D = example_frame()
            tri = Polygon(A, B, C, color=CHALK_CYAN, stroke_width=2.4,
                          fill_color=CHALK_CYAN, fill_opacity=0.14)
            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=3.4)
            bc = Line(B, C, color=CHALK_YELLOW, stroke_width=3.4)
            diag = Line(A, C, color=CHALK_YELLOW, stroke_width=4.0)
            names = VGroup(vertex_label("A", A, "UL", CHALK_WHITE, 17),
                           vertex_label("B", B, "UR", CHALK_WHITE, 17),
                           vertex_label("C", C, "DR", CHALK_WHITE, 17))
            # the two distances that locate D, on cards: a label hung on the
            # B -> D radius landed on the A B side of the triangle
            rad_b = radius_line(B, D, CHALK_AMBER)
            rad_c = radius_line(C, D, CHALK_PINK)
            card_bd = measure_card(r"BD=5.4", CHALK_AMBER, 16).move_to(
                np.array([BOARD_CX + 2.75, -0.55, 0]))
            card_bd_lab = board_text("diagonal BD", 15, CHALK_AMBER, "BOLD"
                                     ).move_to(np.array([BOARD_CX + 2.75, -1.02, 0]))
            card_cd = measure_card(r"CD=4.8", CHALK_PINK, 16).move_to(
                np.array([BOARD_CX + 2.75, -1.60, 0]))
            card_cd_lab = board_text("side CD", 15, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX + 2.75, -2.07, 0]))
            d_dot = Dot(radius=0.09, color=CHALK_YELLOW).move_to(D)
            d_name = vertex_label("D", D, "DR", CHALK_WHITE).shift(
                np.array([0.14, -0.20, 0]))
            guide_c = DashedLine(C, D, color=CHALK_WHITE, stroke_width=1.8,
                                 dash_length=0.12)
            guide_a = DashedLine(A, D, color=CHALK_WHITE, stroke_width=1.8,
                                 dash_length=0.12)
            note = board_text("One diagonal and one side have located D.", 19,
                              CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.62, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(tri), FadeIn(ab), FadeIn(bc), FadeIn(diag),
                      FadeIn(names), run_time=0.8)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            # the two distances that locate D, shown before either arc
            self.play(FadeIn(rad_b), FadeIn(rad_c), FadeIn(card_bd),
                      FadeIn(card_bd_lab), FadeIn(card_cd), FadeIn(card_cd_lab),
                      run_time=0.7)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            self.compass_on(B, D, 5.4 * SCALE, 16, CHALK_AMBER,
                            hinge_dir=(1.0, 1.0, 0.0))
            self.sweep_compass(tracker, "b2", 16)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            # the tail of a symmetric arc about C would poke back over the
            # diagonal, so this sector is rotated 8 degrees further down
            self.compass_on(C, D, 4.8 * SCALE, 14, CHALK_PINK,
                            hinge_dir=(1.0, -1.0, 0.0), bias=8.0)
            self.sweep_compass(tracker, "b3", 14)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(FadeIn(d_dot, scale=0.5), FadeIn(d_name),
                      Indicate(d_dot, color=CHALK_YELLOW, scale_factor=1.9),
                      run_time=0.9)
            self.play(Create(guide_c), Create(guide_a), run_time=0.8)
            self.play(FadeIn(note, shift=UP * 0.1),
                      Flash(d_dot, color=CHALK_GREEN, flash_radius=0.6),
                      run_time=0.8)
            self.wait(leftover(tracker, "b4"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: complete the quadrilateral and verify ----------------------
    def beat7_complete(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("Required Quadrilateral ABCD", 22, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            A, B, C, D = example_frame()
            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=4.0)
            bc = Line(B, C, color=CHALK_YELLOW, stroke_width=4.0)
            diag_ac = Line(A, C, color=CHALK_YELLOW, stroke_width=3.4)
            cd = Line(C, D, color=CHALK_GREEN, stroke_width=4.0)
            bd = Line(B, D, color=CHALK_AMBER, stroke_width=3.4)
            ad = Line(A, D, color=CHALK_GREEN, stroke_width=4.0)
            quad = Polygon(A, B, C, D, color=CHALK_CYAN, stroke_width=2.2,
                           fill_color=CHALK_CYAN, fill_opacity=0.10)
            names = diamond_names(A, B, C, D, "ABCD", 17)
            checks = VGroup(
                check_row(r"AB=4.5", CHALK_GREEN, 15),
                check_row(r"BC=5.2", CHALK_GREEN, 15),
                check_row(r"CD=4.8", CHALK_GREEN, 15),
                check_row(r"AC=5", CHALK_YELLOW, 15),
                check_row(r"BD=5.4", CHALK_AMBER, 15),
            ).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX + 3.0, 0.1, 0]))
            note = board_text("AD was never given: the construction fixed it.",
                              18, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(quad), FadeIn(names), Create(ab), Create(bc),
                      Create(diag_ac), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(Create(cd), run_time=min(leftover(tracker, "b1"), 0.8))
            self.play(Create(bd), run_time=min(leftover(tracker, "b1"), 0.8))
            self.play(Create(ad), run_time=min(leftover(tracker, "b1"), 0.8))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1)
                                    for c in checks], lag_ratio=0.22),
                      run_time=min(leftover(tracker, "b2"), 1.6))
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(note, shift=UP * 0.1),
                      Circumscribe(ad, color=CHALK_GREEN, stroke_width=2.6,
                                   time_width=0.6),
                      run_time=min(leftover(tracker, "b3"), 1.0))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the reusable method ----------------------------------------
    def beat8_method(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("Analyse First", 23, CHALK_AMBER, "BOLD"
                                 ).move_to(np.array([BOARD_CX, 2.72, 0]))
            steps = VGroup(
                combo_card("1. SKETCH", "mark 3 sides + 2 diagonals", CHALK_CYAN),
                combo_card("2. FIND THE TRIANGLE", "the three known lengths",
                           CHALK_GREEN),
                combo_card("3. TWO ARCS", "side + diagonal as radii", CHALK_PINK),
                combo_card("4. JOIN", "complete and verify", CHALK_YELLOW),
            ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX - 2.3, 0.35, 0]))
            A, B, C, D = example_frame(origin=np.array([BOARD_CX + 2.3, 0.55, 0]),
                                       scale=0.28)
            mini = VGroup(
                Polygon(A, B, C, D, color=CHALK_WHITE, stroke_width=2.0,
                        fill_opacity=0.0),
                Line(A, C, color=CHALK_YELLOW, stroke_width=3.0),
                Line(B, D, color=CHALK_AMBER, stroke_width=2.4),
                Polygon(A, B, C, color=CHALK_CYAN, stroke_width=1.6,
                        fill_color=CHALK_CYAN, fill_opacity=0.18),
                locating_arc(B, D, 5.4 * 0.28, 20, CHALK_AMBER),
                locating_arc(C, D, 4.8 * 0.28, 20, CHALK_PINK),
                Dot(radius=0.07, color=CHALK_YELLOW).move_to(D),
            )
            names = diamond_names(A, B, C, D, "ABCD", 13, pull=0.05)
            note = board_text("Start with the triangle whose 3 lengths are "
                              "known.", 17, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(steps), run_time=1.2)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(mini[0]), FadeIn(names), FadeIn(mini[1]),
                      FadeIn(mini[2]), run_time=min(leftover(tracker, "b1"), 1.0))
            self.play(FadeIn(mini[3]), Create(mini[4]), Create(mini[5]),
                      FadeIn(mini[6]), run_time=min(leftover(tracker, "b1"), 1.6))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b1"))

            self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
            self.play(Circumscribe(steps[1], color=CHALK_GREEN, stroke_width=2.4,
                                   time_width=0.6),
                      run_time=min(leftover(tracker, "b2"), 1.2))
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 9: student challenge (Exercise 3.3(a)) ------------------------
    def beat9_challenge(self) -> None:
        with self.voiceover(text=NARRATION["scene9_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", 30, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, 2.62, 0]))
            tag = board_text("Exercise 3.3(a) — quadrilateral GOLD", 15,
                             CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, 2.24, 0]))
            G, O, L, D = practice_frame()
            rough = Polygon(G, O, L, D, color=CHALK_WHITE, stroke_width=2.4,
                            fill_color=CHALK_WHITE, fill_opacity=0.06)
            diag = Line(G, L, color=CHALK_YELLOW, stroke_width=3.6)
            diag2 = Line(O, D, color=CHALK_AMBER, stroke_width=3.0)
            # hand-placed: the automatic corner slots put two letters on the
            # two arcs that cross at O
            names = VGroup(
                board_text("G", 15, CHALK_WHITE, "BOLD").move_to(
                    G + np.array([-0.30, 0.02, 0])),
                board_text("O", 15, CHALK_WHITE, "BOLD").move_to(
                    O + np.array([-0.30, -0.28, 0])),
                board_text("L", 15, CHALK_WHITE, "BOLD").move_to(
                    L + np.array([0.26, -0.02, 0])),
                board_text("D", 15, CHALK_WHITE, "BOLD").move_to(
                    D + np.array([-0.02, 0.30, 0])),
            )
            cards = VGroup(
                measure_card(r"OL=7.5", CHALK_CYAN, 15),
                measure_card(r"GL=6", CHALK_YELLOW, 15),
                measure_card(r"LD=5", CHALK_CYAN, 15),
                measure_card(r"DG=5.5", CHALK_CYAN, 15),
                measure_card(r"OD=10", CHALK_AMBER, 15),
            ).arrange(DOWN, buff=0.20).move_to(
                np.array([BOARD_CX + 2.4, 0.55, 0]))
            ask = board_text("Which triangle comes first?", 18, CHALK_WHITE,
                             "BOLD").move_to(
                np.array([BOARD_CX + 0.30, -2.45, 0]))
            pause = board_text("Pause and decide.", 18, CHALK_YELLOW, "BOLD"
                               ).move_to(np.array([BOARD_CX + 2.4, -1.9, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(tag), run_time=0.4)
            self.play(FadeIn(rough), FadeIn(names), FadeIn(diag), FadeIn(diag2),
                      run_time=0.8)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.10)
                                    for c in cards], lag_ratio=0.18),
                      run_time=min(leftover(tracker, "b1"), 1.6))
            self.wait(leftover(tracker, "b1"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(ask, shift=RIGHT * 0.12), run_time=0.5)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(pause, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b3"))

            self.challenge = {"rough": rough, "names": names, "cards": cards,
                              "ask": ask, "pause": pause, "diag": diag,
                              "points": (G, O, L, D)}
            self._capture_srt(tracker)

        play_challenge_countdown(self, seconds=4, sfx=self.sfx,
                                 position=np.array([BOARD_CX + 1.35, 0.5, 0]))

        with self.voiceover(text=NARRATION["scene9_reveal"]) as tracker:
            ch = self.challenge
            G, O, L, D = ch["points"]
            names = ch["names"]

            # the question and the pause prompt have done their job: clearing
            # both leaves the bottom of the board free for the arc about L,
            # whose pencil sweeps down to y = -2.44
            self.play(FadeOut(ch["pause"]), FadeOut(ch["ask"]), run_time=0.4)
            self.wait(leftover(tracker, "b0"))
            tri = Polygon(G, L, D, color=CHALK_GREEN, stroke_width=3.0,
                          fill_color=CHALK_GREEN, fill_opacity=0.14)
            centroid = np.array([G, O, L, D], dtype=float).mean(axis=0)
            # clear of the figure, of the O -> D diagonal (which crosses G L)
            # and of both pairs of compasses: their needles sit on L and D and
            # every part of the instrument stays to the left of the figure
            lab_gl = board_text("GL = 6", 15, CHALK_GREEN, "BOLD").move_to(
                L + np.array([0.66, -0.50, 0]))
            lab_ld = side_label(L, D, centroid, "LD = 5", CHALK_GREEN, 15, 0.18)
            lab_dg = side_label(D, G, centroid, "DG = 5.5", CHALK_GREEN, 15, 0.18)
            self.play(Create(tri),
                      Circumscribe(ch["diag"], color=CHALK_YELLOW,
                                   stroke_width=2.4, time_width=0.6),
                      run_time=min(leftover(tracker, "b1"), 1.2))
            self.play(FadeIn(lab_gl), FadeIn(lab_ld), FadeIn(lab_dg),
                      run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            badge = board_text("First triangle: GLD", 18, CHALK_GREEN, "BOLD"
                               ).move_to(np.array([BOARD_CX + 2.4, -1.75, 0]))
            self.play(FadeIn(badge, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["ding"], gain=-13)

            first_tool = None
            # leg_ratio 0.52: a compass opened out for a wide arc keeps its
            # hinge near the needle-pencil line, so the instrument stays on the
            # left of the figure instead of sweeping across the L letter and
            # the G L label
            self.compass_on(L, O, 7.5 * 0.34, 14, CHALK_CYAN,
                            hinge_dir=(-1.0, -1.0, 0.0), bias=4.0,
                            leg_ratio=0.52)
            first_tool = self.tool
            # fixed sweeps, not "use the whole window": the pair of arcs, the
            # two compasses being laid down and the appearance of O all have to
            # fit inside this one narration window
            self.play(self.sweep.animate.set_value(28), run_time=2.2)
            self.compass_on(D, O, 10.0 * 0.34, 14, CHALK_PINK,
                            hinge_dir=(1.0, -1.0, 0.0), bias=4.0,
                            leg_ratio=0.52)
            self.play(self.sweep.animate.set_value(28), run_time=2.2)
            self.put_down_tool(first_tool)
            self.put_down_tool(self.tool)
            o_dot = Dot(radius=0.08, color=CHALK_YELLOW).move_to(O)
            o_name = names[1]
            quad = Polygon(G, O, L, D, color=CHALK_CYAN, stroke_width=2.4,
                           fill_color=CHALK_CYAN, fill_opacity=0.12)
            self.play(FadeIn(o_dot, scale=0.5), FadeIn(quad),
                      Indicate(o_dot, color=CHALK_YELLOW, scale_factor=2.0),
                      Circumscribe(o_name, color=CHALK_YELLOW, fade_out=True),
                      run_time=min(leftover(tracker, "b3"), 1.0))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap ------------------------------------------------------
    def beat10_recap(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("Three Sides and Two Diagonals", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            # the recap figure is nudged a little right of the left edge, so it
            # reads as centred in the left half instead of hugging the margin
            A, B, C, D = example_frame(origin=np.array([BOARD_CX - 3.35, 0.55, 0]),
                                       scale=0.30)
            diag_ac = Line(A, C, color=CHALK_YELLOW, stroke_width=3.2)
            diag_bd = Line(B, D, color=CHALK_AMBER, stroke_width=2.8)
            tri = Polygon(A, B, C, color=CHALK_YELLOW, stroke_width=3.0,
                          fill_color=CHALK_YELLOW, fill_opacity=0.16)
            quad = Polygon(A, B, C, D, color=CHALK_CYAN, stroke_width=2.2,
                           fill_color=CHALK_CYAN, fill_opacity=0.10)
            names = diamond_names(A, B, C, D, "ABCD", 15, pull=0.05)
            arc_b = locating_arc(B, D, 5.4 * 0.30, 18, CHALK_AMBER)
            arc_c = locating_arc(C, D, 4.8 * 0.30, 18, CHALK_PINK)
            d_dot = Dot(radius=0.08, color=CHALK_YELLOW).move_to(D)

            rows = VGroup(
                summary_row(1, "Two sides + one diagonal:",
                            r"\triangle ABC", CHALK_YELLOW),
                summary_row(2, "One side + one diagonal:",
                            r"D", CHALK_AMBER),
                summary_row(3, "The fifth side is fixed by the drawing:",
                            r"AD", CHALK_GREEN),
            ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX + 1.8, 1.35, 0]))
            final = board_text("3 build, 2 locate.", 18, CHALK_GREEN, "BOLD"
                               ).move_to(np.array([BOARD_CX, -1.90, 0]))
            take = board_text("Sketch, find the triangle, intersect, join.", 16,
                              CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.45, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(quad), FadeIn(names), Create(tri), Create(diag_ac),
                      Create(diag_bd), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(rows[0], shift=RIGHT * 0.12), run_time=0.5)
            self.play(Create(arc_b), Create(arc_c), FadeIn(d_dot),
                      FadeIn(rows[1], shift=RIGHT * 0.12),
                      run_time=min(leftover(tracker, "b1"), 1.6))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b1"))

            self.play(Indicate(d_dot, color=CHALK_YELLOW, scale_factor=2.0),
                      FadeIn(rows[2], shift=RIGHT * 0.12), run_time=0.8)
            self.add_sound(self.sfx["success"], gain=-11)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeIn(final, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(take),
                      Circumscribe(quad, color=CHALK_AMBER, stroke_width=3,
                                   time_width=0.5),
                      run_time=min(leftover(tracker, "b3"), 1.2))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b3"))

            summary = VGroup(quad, names, tri, diag_ac, diag_bd, arc_b, arc_c,
                             d_dot, rows, final, take)
            thanks = board_text("Thank You for Watching!", 40, CHALK_WHITE,
                                "BOLD")
            thanks2 = board_text("See you in the next lesson :)", 25, CHALK_CYAN)
            thanks_group = VGroup(thanks, thanks2).arrange(
                DOWN, buff=0.3).move_to(np.array([BOARD_CX, BOARD_CY, 0]))
            self.play(FadeOut(summary), FadeOut(heading), run_time=min(
                leftover(tracker, "b4") * 0.5, 0.8))
            self.play(FadeIn(thanks, shift=UP * 0.1), run_time=0.6)
            self.add_sound(self.sfx["success"], gain=-11)
            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(thanks2, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b5"))
            self.play(Circumscribe(thanks_group, color=CHALK_AMBER,
                                   stroke_width=3, time_width=0.5),
                      run_time=0.25)
            self.play(Indicate(thanks, color=CHALK_WHITE, scale_factor=1.01),
                      run_time=rt(tracker.get_remaining_duration()))
            self._capture_srt(tracker)

        self.wait(END_HOLD)

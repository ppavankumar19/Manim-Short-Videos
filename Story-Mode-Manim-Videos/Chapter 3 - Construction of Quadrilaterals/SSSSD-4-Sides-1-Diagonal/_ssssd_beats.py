"""Scene beats for Storyboard 03 (S.S.S.S.D)."""

    # ================================================================ beats ==

    def compass_on(self, centre, target, radius, spread, color,
                   hinge_dir=None, leg_ratio=0.62):
        """Put a pair of compasses on the board with its needle on `centre` and
        its pencil at the start of the arc, ready to sweep."""
        arc, tool, sweep = compass_arc_drawer(
            centre, target, radius, spread, color, hinge_dir=hinge_dir,
            leg_ratio=leg_ratio)
        self.add(arc, tool)
        self.arc, self.tool, self.sweep = arc, tool, sweep
        return sweep

    def sweep_compass(self, tracker, mark: str, spread: float,
                      put_down: bool = True) -> None:
        """Sweep the compasses already on the board to the end of the arc, then
        (by default) lay them down -- all inside the current narration window."""
        budget = leftover(tracker, mark)
        sweep_time = max(budget - (0.35 if put_down else 0.0), 0.4)
        self.play(self.sweep.animate.set_value(2 * spread), run_time=sweep_time)
        if put_down:
            self.play(FadeOut(self.tool), run_time=0.3)
        self.wait(leftover(tracker, mark))

    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Construct a Quadrilateral", 33, CHALK_WHITE,
                               "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 1.85, 0]))
            sub = board_text("Four Sides and One Diagonal", 21, CHALK_YELLOW,
                             "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 0.95, 0]))
            self.play(FadeIn(title, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(sub, color=CHALK_YELLOW, scale_factor=1.04),
                      run_time=max(leftover(tracker, "b0"), 0.4))
            self.add_sound(self.sfx["ding"], gain=-13)

            # small enough that its vertex letters clear the subtitle above and
            # the tag line below
            A, B, C, D = example_frame(origin=np.array([BOARD_CX - 0.75, -0.60, 0]),
                                       scale=0.30)
            outline = Polygon(A, B, C, D, color=CHALK_WHITE, stroke_width=2.2,
                              fill_color=CHALK_WHITE, fill_opacity=0.05)
            outline.set_stroke(opacity=0.45)
            diag = Line(A, C, color=CHALK_YELLOW, stroke_width=3.4)
            names = diamond_names(A, B, C, D, "ABCD", 15, pull=0.05)
            tag = board_text("Diagonal → Triangle → Arcs → Join", 18,
                             CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))
            self.play(FadeIn(outline), FadeIn(names), run_time=min(
                leftover(tracker, "b1"), 1.0))
            self.play(Create(diag), run_time=0.8)
            self.play(Flash(diag, color=CHALK_YELLOW, flash_radius=0.7),
                      run_time=0.6)
            self.play(FadeIn(tag, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b1"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: the five given measurements --------------------------------
    def beat1_data(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("Four Sides and One Diagonal", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            cards = VGroup(
                measure_card(r"AB=4", CHALK_CYAN),
                measure_card(r"BC=3.6", CHALK_CYAN),
                measure_card(r"CD=4.2", CHALK_CYAN),
                measure_card(r"AD=4.8", CHALK_CYAN),
                measure_card(r"AC=5", CHALK_YELLOW),
            ).arrange(DOWN, buff=0.24).move_to(np.array([BOARD_CX, 0.55, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.12)
                                    for c in cards[:4]], lag_ratio=0.22),
                      run_time=1.0)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            # the diagonal is its own piece of information: it arrives with its
            # own sentence
            self.wait(leftover(tracker, "b0b"))
            self.play(FadeIn(cards[4], shift=RIGHT * 0.12), run_time=0.45)
            self.play(Indicate(cards[4], color=CHALK_YELLOW, scale_factor=1.08),
                      run_time=0.9)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b1"))

            strip = board_text("4 Sides + 1 Diagonal", 21, CHALK_GREEN, "BOLD"
                               ).move_to(np.array([BOARD_CX, -1.79, 0]))
            box = SurroundingRectangle(strip, color=CHALK_GREEN, buff=0.16,
                                       corner_radius=0.1, stroke_width=2.6)
            self.play(FadeIn(strip, shift=UP * 0.1), Create(box), run_time=0.6)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["click"], gain=-15)

            ask = board_text("Where should we start?", 19, CHALK_WHITE, "BOLD"
                             ).move_to(np.array([BOARD_CX, -2.54, 0]))
            self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: the diagonal makes two triangles ---------------------------
    def beat2_split(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("One Diagonal, Two Triangles", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            A, B, C, D = example_frame(origin=np.array([BOARD_CX - 1.6, 0.55, 0]),
                                       scale=0.42)
            quad = Polygon(A, B, C, D, color=CHALK_WHITE, stroke_width=2.2,
                           fill_color=CHALK_WHITE, fill_opacity=0.05)
            diag = Line(A, C, color=CHALK_YELLOW, stroke_width=4.0)
            names = diamond_names(A, B, C, D, "ABCD", 17)
            tri_b = Polygon(A, B, C, color=CHALK_CYAN, stroke_width=2.6,
                            fill_color=CHALK_CYAN, fill_opacity=0.20)
            tri_d = Polygon(A, C, D, color=CHALK_GREEN, stroke_width=2.6,
                            fill_color=CHALK_GREEN, fill_opacity=0.20)
            eq = MathTex(r"ABCD", r"=", r"\triangle ABC", r"+",
                         r"\triangle ACD", font_size=32).move_to(
                np.array([BOARD_CX, -1.85, 0]))
            ask = board_text("Which triangle can we build first?", 19,
                             CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(Create(quad), FadeIn(names), run_time=0.8)
            self.play(Create(diag), run_time=0.7)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(tri_b), run_time=0.5)
            self.wait(leftover(tracker, "b1"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(tri_d), run_time=0.5)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(tri_b.animate.shift(UP * 0.14),
                      tri_d.animate.shift(DOWN * 0.14), run_time=0.6)
            self.play(tri_b.animate.shift(DOWN * 0.14),
                      tri_d.animate.shift(UP * 0.14), run_time=0.6)
            self.wait(leftover(tracker, "b3"))

            self.play(FadeIn(eq, shift=UP * 0.08),
                      Circumscribe(diag, color=CHALK_YELLOW, stroke_width=2.4,
                                   time_width=0.6),
                      run_time=1.0)
            self.wait(leftover(tracker, "b4"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b5"))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: the first triangle is the S.S.S one ------------------------
    def beat3_choose(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()

            heading = board_text("Use 3 of the 5 Measurements", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            A, B, C, D = example_frame(origin=np.array([BOARD_CX - 1.5, 0.30, 0]))
            full = Polygon(A, B, C, D, color=CHALK_WHITE, stroke_width=2.0,
                           fill_opacity=0.0)
            full.set_stroke(opacity=0.28)
            names = diamond_names(A, B, C, D, "ABCD", 17)
            tri = Polygon(A, B, C, color=CHALK_CYAN, stroke_width=3.0,
                          fill_color=CHALK_CYAN, fill_opacity=0.16)
            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=4.0)
            bc = Line(B, C, color=CHALK_YELLOW, stroke_width=4.0)
            diag = Line(A, C, color=CHALK_YELLOW, stroke_width=4.0)
            centroid = np.array([A, B, C, D], dtype=float).mean(axis=0)
            lab_ab = side_label(A, B, centroid, "4", CHALK_YELLOW, 16, 0.20)
            lab_bc = side_label(B, C, centroid, "3.6", CHALK_YELLOW, 16, 0.20)
            # under the middle of the diagonal: just below C the compasses' own
            # body sits, and beside C the vertex letter crowds it
            lab_ac = board_text("AC = 5", 16, CHALK_YELLOW, "BOLD").move_to(
                (A + C) / 2 + DOWN * 0.65)
            sss = combo_card("Side + Side + Side", "three known sides", CHALK_GREEN)
            sss.move_to(np.array([BOARD_CX + 3.0, 0.55, 0]))
            note = board_text("No angle is needed here.", 18, CHALK_WHITE, "BOLD"
                              ).move_to(np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(full), FadeIn(names), run_time=0.6)
            self.play(Create(ab), FadeIn(lab_ab), run_time=0.8)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(Create(bc), FadeIn(lab_bc), run_time=0.8)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            self.play(Create(diag), FadeIn(lab_ac), run_time=0.8)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(tri), FadeIn(sss, shift=RIGHT * 0.12),
                      FadeIn(note, shift=UP * 0.1), run_time=0.9)
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["ding"], gain=-13)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: draw the diagonal and the first arc ------------------------
    def beat4_diagonal(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 1 — Draw the Diagonal", 22, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            A, B, C, D = example_frame()
            base = Line(A, C, color=CHALK_WHITE, stroke_width=4.5)
            names = VGroup(vertex_label("A", A, "UL"), vertex_label("C", C, "DR"))
            # under the middle of the diagonal, clear of the compasses and of
            # the vertex letters at either end
            lab_ac = board_text("AC = 5 cm", 17, CHALK_CYAN, "BOLD").move_to(
                (A + C) / 2 + DOWN * 0.65)
            note1 = board_text("This diagonal belongs to both triangles.", 18,
                               CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))
            note2 = board_text("B is 4 cm from A, so it lies on this arc.", 18,
                               CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(Create(base), FadeIn(names), run_time=0.8)
            self.play(FadeIn(lab_ac), run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(note1, shift=UP * 0.1), run_time=0.5)
            # the note leaves inside its own window, so the next one starts on
            # the mark rather than late
            self.wait(max(leftover(tracker, "b1") - 0.35, 0.0))
            self.play(FadeOut(note1), run_time=0.3)
            self.add_sound(self.sfx["click"], gain=-15)
            self.compass_on(A, B, 4.0 * SCALE, 17, CHALK_CYAN,
                            hinge_dir=(1.0, -1.0, 0.0))
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["ding"], gain=-13)

            # the note appears as the pencil starts to draw the arc B must lie
            # on, so the sweep itself fills the window and the beat ends on its
            # mark
            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(note2, shift=UP * 0.1), run_time=0.5)
            self.sweep_compass(tracker, "b4", 17)
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
            # under the middle of the diagonal, clear of the compasses and of
            # the vertex letters at either end
            lab_ac = board_text("AC = 5 cm", 17, CHALK_CYAN, "BOLD").move_to(
                (A + C) / 2 + DOWN * 0.65)
            arc_a = locating_arc(A, B, 4.0 * SCALE, 17, CHALK_CYAN)
            b_dot = Dot(radius=0.09, color=CHALK_YELLOW).move_to(B)
            b_name = vertex_label("B", B, "UR", CHALK_WHITE)
            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=4.0)
            bc = Line(B, C, color=CHALK_YELLOW, stroke_width=4.0)
            tri = Polygon(A, B, C, color=CHALK_CYAN, stroke_width=2.6,
                          fill_color=CHALK_CYAN, fill_opacity=0.16)
            centroid = np.array([A, B, C, D], dtype=float).mean(axis=0)
            # the two side labels sit outside/inside so the compasses' legs,
            # which sweep up to the right of C, cannot run through them
            lab_ab = side_label(A, B, centroid, "AB = 4 cm", CHALK_YELLOW, 16, 0.20)
            lab_bc = side_label(C, B, B + C - centroid, "BC = 3.6 cm",
                                CHALK_YELLOW, 16, 0.20)
            note = board_text("Three sides fix this triangle.", 19, CHALK_GREEN,
                              "BOLD").move_to(np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(Create(base), FadeIn(names), FadeIn(lab_ac),
                      run_time=0.8)
            self.play(Create(arc_a), run_time=0.7)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            # the compasses move to C for the third side
            self.compass_on(C, B, 3.6 * SCALE, 16, CHALK_GREEN,
                            hinge_dir=(1.0, 1.0, 0.0))
            self.sweep_compass(tracker, "b1", 16)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(FadeIn(b_dot, scale=0.5), FadeIn(b_name),
                      Indicate(b_dot, color=CHALK_YELLOW, scale_factor=1.9),
                      run_time=0.9)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(Create(ab), FadeIn(lab_ab), Create(bc), FadeIn(lab_bc),
                      run_time=1.1)
            self.play(FadeIn(tri), run_time=0.6)
            self.play(FadeIn(note, shift=UP * 0.1),
                      Flash(tri, color=CHALK_CYAN, flash_radius=0.7),
                      run_time=0.8)
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: the remaining two sides locate D ---------------------------
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
            quad_names_all = diamond_names(A, B, C, D, "ABCD", 17)
            names = VGroup(quad_names_all[0], quad_names_all[1],
                           quad_names_all[2])
            arc_c = locating_arc(C, D, 4.2 * SCALE, 18, CHALK_PINK)
            rad_a = radius_line(A, D, CHALK_CYAN, "AD = 4.8 cm", 15)
            d_dot = Dot(radius=0.09, color=CHALK_YELLOW).move_to(D)
            d_name = vertex_label("D", D, "DR", CHALK_WHITE).shift(
                np.array([0.12, -0.12, 0]))
            guide1 = DashedLine(A, D, color=CHALK_WHITE, stroke_width=1.8,
                                dash_length=0.12)
            guide2 = DashedLine(C, D, color=CHALK_WHITE, stroke_width=1.8,
                                dash_length=0.12)
            note = board_text("D satisfies both distances.", 19, CHALK_GREEN,
                              "BOLD").move_to(np.array([BOARD_CX, -2.60, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(tri), FadeIn(ab), FadeIn(bc), FadeIn(diag),
                      FadeIn(names), run_time=0.8)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(rad_a), run_time=0.5)
            self.compass_on(A, D, 4.8 * SCALE, 18, CHALK_CYAN,
                            hinge_dir=(-1.0, -1.0, 0.0))
            self.sweep_compass(tracker, "b2", 18)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            # the second arc is drawn with the compasses as well: both arcs of
            # the pair must come from the instrument
            self.compass_on(C, D, 4.2 * SCALE, 18, CHALK_PINK,
                            hinge_dir=(1.0, -1.0, 0.0))
            self.sweep_compass(tracker, "b3", 18)
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(FadeIn(d_dot, scale=0.5), FadeIn(d_name),
                      Indicate(d_dot, color=CHALK_YELLOW, scale_factor=1.9),
                      run_time=0.9)
            self.play(Create(guide1), Create(guide2), run_time=0.8)
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
            ad = Line(A, D, color=CHALK_GREEN, stroke_width=4.0)
            dc = Line(D, C, color=CHALK_GREEN, stroke_width=4.0)
            diag = Line(A, C, color=CHALK_WHITE, stroke_width=3.0)
            quad = Polygon(A, B, C, D, color=CHALK_CYAN, stroke_width=2.2,
                           fill_color=CHALK_CYAN, fill_opacity=0.10)
            names = diamond_names(A, B, C, D, "ABCD", 17)
            checks = VGroup(
                check_row(r"AB=4", CHALK_GREEN, 15),
                check_row(r"BC=3.6", CHALK_GREEN, 15),
                check_row(r"CD=4.2", CHALK_GREEN, 15),
                check_row(r"AD=4.8", CHALK_GREEN, 15),
                check_row(r"AC=5", CHALK_YELLOW, 15),
            ).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX + 3.0, 0.1, 0]))
            title = board_text("All five measurements used.", 19, CHALK_GREEN,
                               "BOLD").move_to(np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(Create(ab), Create(bc), Create(diag), FadeIn(quad),
                      FadeIn(names), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(Create(ad), run_time=min(leftover(tracker, "b1"), 1.0))
            self.play(Create(dc), run_time=min(leftover(tracker, "b1"), 1.0))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            self.play(FadeIn(title, shift=UP * 0.1), run_time=0.5)
            self.play(Flash(quad, color=CHALK_CYAN, flash_radius=0.8),
                      run_time=min(leftover(tracker, "b2"), 0.9))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b2"))

            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1)
                                    for c in checks], lag_ratio=0.22),
                      run_time=min(leftover(tracker, "b3"), 1.6))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the reusable method ----------------------------------------
    def beat8_method(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("Diagonal First", 23, CHALK_AMBER, "BOLD"
                                 ).move_to(np.array([BOARD_CX, 2.72, 0]))
            steps = VGroup(
                combo_card("1. SKETCH", "mark 4 sides + the diagonal", CHALK_CYAN),
                combo_card("2. TRIANGLE", "diagonal + 2 sides, by SSS",
                           CHALK_GREEN),
                combo_card("3. TWO ARCS", "remaining sides as radii", CHALK_PINK),
                combo_card("4. JOIN", "complete and verify", CHALK_YELLOW),
            ).arrange(DOWN, buff=0.20, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX - 2.35, 0.35, 0]))
            A, B, C, D = example_frame(origin=np.array([BOARD_CX + 2.2, 0.55, 0]),
                                       scale=0.30)
            mini = VGroup(
                Polygon(A, B, C, D, color=CHALK_WHITE, stroke_width=2.0,
                        fill_opacity=0.0),
                Line(A, C, color=CHALK_YELLOW, stroke_width=3.0),
                Line(A, B, color=CHALK_YELLOW, stroke_width=3.0),
                Line(B, C, color=CHALK_YELLOW, stroke_width=3.0),
                Polygon(A, B, C, color=CHALK_CYAN, stroke_width=1.6,
                        fill_color=CHALK_CYAN, fill_opacity=0.18),
                locating_arc(A, D, 4.8 * 0.30, 20, CHALK_CYAN),
                locating_arc(C, D, 4.2 * 0.30, 20, CHALK_PINK),
                Dot(radius=0.07, color=CHALK_YELLOW).move_to(D),
            )
            names = diamond_names(A, B, C, D, "ABCD", 14, pull=0.05)
            note = board_text("Diagonal → Triangle → Arcs → Join → Verify", 17,
                              CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(steps), run_time=1.2)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(mini[0]), FadeIn(names), FadeIn(mini[1]),
                      FadeIn(mini[2]), FadeIn(mini[3]),
                      run_time=min(leftover(tracker, "b1"), 1.0))
            self.play(FadeIn(mini[4]), Create(mini[5]), Create(mini[6]),
                      FadeIn(mini[7]), run_time=min(leftover(tracker, "b1"), 1.6))
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

    # -- Scene 9: student challenge ------------------------------------------
    def beat9_challenge(self) -> None:
        with self.voiceover(text=NARRATION["scene9_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", 30, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, 2.62, 0]))
            tag = board_text("Practice set — made for this video.", 15,
                             CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, 2.24, 0]))
            P, Q, R, S = practice_frame()
            rough = Polygon(P, Q, R, S, color=CHALK_WHITE, stroke_width=2.4,
                            fill_color=CHALK_WHITE, fill_opacity=0.06)
            diag = Line(P, R, color=CHALK_YELLOW, stroke_width=3.6)
            names = diamond_names(P, Q, R, S, "PQRS", 16)
            cards = VGroup(
                measure_card(r"PQ=4", CHALK_CYAN, 15),
                measure_card(r"QR=3", CHALK_CYAN, 15),
                measure_card(r"RS=5", CHALK_CYAN, 15),
                measure_card(r"PS=4.5", CHALK_CYAN, 15),
                measure_card(r"PR=5.5", CHALK_YELLOW, 15),
            ).arrange(DOWN, buff=0.20).move_to(
                np.array([BOARD_CX + 2.4, 0.55, 0]))
            ask = board_text("Which triangle comes first?", 18, CHALK_WHITE,
                             "BOLD").move_to(np.array([BOARD_CX - 1.0, -2.15, 0]))
            pause = board_text("Pause and decide.", 18, CHALK_YELLOW, "BOLD"
                               ).move_to(np.array([BOARD_CX + 2.4, -1.9, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(tag), run_time=0.4)
            self.play(FadeIn(rough), FadeIn(names), run_time=0.7)
            self.play(Create(diag), run_time=0.7)
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
                              "points": (P, Q, R, S)}
            self._capture_srt(tracker)

        play_challenge_countdown(self, seconds=4, sfx=self.sfx,
                                 position=np.array([BOARD_CX + 0.65, 0.5, 0]))

        with self.voiceover(text=NARRATION["scene9_reveal"]) as tracker:
            ch = self.challenge
            P, Q, R, S = ch["points"]
            rough, names = ch["rough"], ch["names"]

            self.play(FadeOut(ch["pause"]), run_time=0.4)
            tri = Polygon(P, Q, R, color=CHALK_GREEN, stroke_width=3.0,
                          fill_color=CHALK_GREEN, fill_opacity=0.14)
            lab_pq = board_text("PQ = 4", 15, CHALK_GREEN, "BOLD").move_to(
                (P + Q) / 2 + np.array([-0.62, 0.04, 0]))
            lab_qr = board_text("QR = 3", 15, CHALK_GREEN, "BOLD").move_to(
                (Q + R) / 2 + np.array([0.62, 0.06, 0]))
            self.play(Create(tri),
                      Circumscribe(ch["diag"], color=CHALK_YELLOW,
                                   stroke_width=2.4, time_width=0.6),
                      run_time=min(leftover(tracker, "b1"), 1.2))
            self.play(FadeIn(lab_pq), FadeIn(lab_qr), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            badge = board_text("First triangle: PQR", 18, CHALK_GREEN, "BOLD"
                               ).move_to(np.array([BOARD_CX + 2.4, -1.75, 0]))
            self.play(FadeIn(badge, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["ding"], gain=-13)

            arc_p = locating_arc(P, S, 4.5 * 0.40, 20, CHALK_CYAN)
            arc_r = locating_arc(R, S, 5.0 * 0.40, 20, CHALK_PINK)
            s_dot = Dot(radius=0.08, color=CHALK_YELLOW).move_to(S)
            s_name = names[3]   # already clear of both arcs
            quad = Polygon(P, Q, R, S, color=CHALK_CYAN, stroke_width=2.4,
                           fill_color=CHALK_CYAN, fill_opacity=0.12)
            quad_cen = np.array([P, Q, R, S], dtype=float).mean(axis=0)
            self.compass_on(P, S, 4.5 * 0.40, 20, CHALK_CYAN,
                            hinge_dir=(-1.0, -0.6, 0.0))
            first_tool = self.tool
            self.sweep_compass(tracker, "b3", 20, put_down=False)
            self.compass_on(R, S, 5.0 * 0.40, 20, CHALK_PINK,
                            hinge_dir=(1.0, -0.6, 0.0))
            self.sweep_compass(tracker, "b3", 20)
            self.play(FadeOut(first_tool), run_time=0.3)
            self.play(FadeIn(s_dot, scale=0.5), FadeIn(quad),
                      Indicate(s_dot, color=CHALK_YELLOW, scale_factor=2.0),
                      Circumscribe(s_name, color=CHALK_YELLOW, fade_out=True),
                      run_time=min(leftover(tracker, "b3"), 1.0))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap ------------------------------------------------------
    def beat10_recap(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("Four Sides and One Diagonal", 23, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            # the recap figure is centred in the left half of the board, not
            # jammed into the corner
            A, B, C, D = example_frame(origin=np.array([BOARD_CX - 3.65, 0.55, 0]),
                                       scale=0.34)
            diag = Line(A, C, color=CHALK_YELLOW, stroke_width=3.2)
            tri = Polygon(A, B, C, color=CHALK_YELLOW, stroke_width=3.0,
                          fill_color=CHALK_YELLOW, fill_opacity=0.16)
            quad = Polygon(A, B, C, D, color=CHALK_CYAN, stroke_width=2.2,
                           fill_color=CHALK_CYAN, fill_opacity=0.10)
            names = diamond_names(A, B, C, D, "ABCD", 16, pull=0.06)
            arc_a = locating_arc(A, D, 4.8 * 0.34, 20, CHALK_CYAN)
            arc_c = locating_arc(C, D, 4.2 * 0.34, 20, CHALK_PINK)
            d_dot = Dot(radius=0.08, color=CHALK_YELLOW).move_to(D)

            rows = VGroup(
                summary_row(1, "Diagonal + two sides:",
                            r"\triangle ABC", CHALK_YELLOW),
                summary_row(2, "Other two sides as radii:",
                            r"AD,\ DC", CHALK_CYAN),
                summary_row(3, "Their crossing gives the vertex:",
                            r"D", CHALK_GREEN),
            ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX + 1.8, 1.35, 0]))
            final = board_text("Diagonal → Triangle → Arcs → Join", 17,
                               CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -1.90, 0]))
            take = board_text("Use the diagonal to make two triangles.", 16,
                              CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.45, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(quad), FadeIn(names), Create(tri), Create(diag),
                      run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(rows[0], shift=RIGHT * 0.12), run_time=0.5)
            self.play(Create(arc_a), Create(arc_c), FadeIn(d_dot),
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

            summary = VGroup(quad, names, tri, diag, arc_a, arc_c, d_dot, rows,
                             final, take)
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

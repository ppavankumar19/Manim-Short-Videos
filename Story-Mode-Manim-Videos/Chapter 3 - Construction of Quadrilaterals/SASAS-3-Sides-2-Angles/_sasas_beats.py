"""Scene beats for Storyboard 06 (S.A.S.A.S)."""

    # ================================================================ beats ==

    # -- the SRT export, with a short tail folded into the caption before it --
    def _capture_srt(self, tracker, words_per_line: int = 9) -> None:
        wbs = [wb for wb in tracker.data.get("word_boundaries", [])
               if wb.get("text", "").strip()]
        if not wbs:
            return
        starts = [tracker.start_t + wb["audio_offset"] / AUDIO_OFFSET_RESOLUTION
                  for wb in wbs]
        chunks = []
        for i in range(0, len(wbs), words_per_line):
            chunk = wbs[i:i + words_per_line]
            end = starts[i + words_per_line] if i + words_per_line < len(starts) \
                else tracker.end_t
            chunks.append([starts[i], end, list(chunk)])
        if len(chunks) > 1 and len(chunks[-1][2]) <= 2:
            tail = chunks.pop()
            chunks[-1][1] = tail[1]
            chunks[-1][2].extend(tail[2])
        for start, end, chunk in chunks:
            text = " ".join(wb["text"] for wb in chunk)
            self._srt_entries.append((start, end, text))

    # -- instruments ---------------------------------------------------------
    def put_down_tool(self, tool, run_time: float = 0.3) -> None:
        """Lay a pair of compasses down on the desk: fade a static copy and
        drop the live `always_redraw` object, whose updater would otherwise
        rebuild it at full opacity on every frame."""
        snap = tool.copy()
        snap.clear_updaters()
        self.remove(tool)
        self.add(snap)
        self.play(FadeOut(snap), run_time=run_time)

    def compass_on(self, centre, target, radius, spread, color,
                   hinge_dir=None, leg_ratio=0.62, bias: float = 0.0):
        v = np.array(centre, dtype=float)
        ang = float(np.degrees(np.arctan2(target[1] - v[1], target[0] - v[0])))
        start = ang - spread + bias
        sweep = ValueTracker(0.004)

        def tip_at():
            a = (start + sweep.get_value()) * DEGREES
            return v + radius * np.array([np.cos(a), np.sin(a), 0.0])

        arc = always_redraw(lambda: Arc(
            radius=radius, start_angle=start * DEGREES,
            angle=max(sweep.get_value(), 0.004) * DEGREES, arc_center=v,
            color=color, stroke_width=2.8))
        tool = always_redraw(lambda: compass_tool(
            v, tip_at(), hinge_dir=hinge_dir, leg_ratio=leg_ratio))
        self.add(arc, tool)
        self.arc, self.tool, self.sweep = arc, tool, sweep
        return sweep

    def sweep_compass(self, tracker, mark: str, spread: float,
                      put_down: bool = True, reserve: float = 0.0,
                      hold: bool = True) -> None:
        budget = leftover(tracker, mark)
        sweep_time = max(budget - (0.35 if put_down else 0.0) - reserve, 0.4)
        self.play(self.sweep.animate.set_value(2 * spread), run_time=sweep_time)
        if put_down:
            self.put_down_tool(self.tool)
        if hold:
            self.wait(leftover(tracker, mark))

    def setout_arm(self, vertex, start_deg, end_deg, length, radius, color,
                   stroke: float = 3.4):
        """An arm that swings from one direction to the other while the angle
        arc grows under it."""
        v = np.array(vertex, dtype=float)
        sweep = ValueTracker(0.0)

        def now() -> float:
            return start_deg + (end_deg - start_deg) * sweep.get_value()

        arm = always_redraw(lambda: Line(
            v, ray_point(v, now(), length), color=color, stroke_width=stroke))
        arc = always_redraw(lambda: Arc(
            radius=radius, start_angle=start_deg * DEGREES,
            angle=(end_deg - start_deg) * sweep.get_value() * DEGREES,
            arc_center=v, color=color, stroke_width=2.6))
        self.add(arc, arm)
        self.arm, self.arm_sweep, self.arm_arc = arm, sweep, arc
        return sweep

    def vertex_letters(self, points, offsets, letters="ABCD", size=17,
                       color=CHALK_WHITE):
        out = []
        for letter, p, off in zip(letters, points, offsets):
            out.append(board_text(letter, size, color, "BOLD").move_to(
                np.array(p, dtype=float) + np.array([off[0], off[1], 0.0])))
        return VGroup(*out)

    def column_card(self, mob, y, x=3.05):
        return mob.move_to(np.array([x, y, 0]))

    def column_note(self, text, y, x=3.05, size=16, color=CHALK_WHITE):
        return board_text(text, size, color, "BOLD").move_to(
            np.array([x, y, 0]))

    def ray_line(self, vertex, direction_deg, length, color=CHALK_PINK,
                 width=3.2, dashed=False):
        end = ray_point(vertex, direction_deg, length)
        if dashed:
            return DashedLine(np.array(vertex, dtype=float), end, color=color,
                              stroke_width=width, dash_length=0.14)
        return Line(np.array(vertex, dtype=float), end, color=color,
                    stroke_width=width)

    # -- Scene 0: title ------------------------------------------------------
    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Construct a Quadrilateral", 33, CHALK_WHITE,
                               "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 1.95, 0]))
            sub = board_text("Three Sides + Two Included Angles", 20,
                             CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 1.05, 0]))
            self.play(FadeIn(title, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(sub, color=CHALK_YELLOW, scale_factor=1.03),
                      run_time=max(leftover(tracker, "b0"), 0.4))
            self.add_sound(self.sfx["ding"], gain=-13)

            # the signature: the chain's first three build the triangle, the
            # last angle gives a direction and the last side the distance
            d = example_construction(
                centre=np.array([BOARD_CX + 0.35, -0.45, 0]), scale=0.42)
            A, B, C, D = d["quad"]
            outline = Polygon(A, B, C, D, color=CHALK_WHITE, stroke_width=2.2)
            outline.set_stroke(opacity=0.38)
            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=3.4)
            bc = Line(B, C, color=CHALK_YELLOW, stroke_width=3.4)
            cd = Line(C, D, color=CHALK_AMBER, stroke_width=3.0)
            ad = Line(A, D, color=CHALK_GREEN, stroke_width=3.0)
            ang_b = angle_mark(B, A, C, radius=0.46, color=CHALK_AMBER)
            ang_c = angle_mark(C, B, D, radius=0.46, color=CHALK_PINK)
            names = self.vertex_letters(
                (A, B, C, D), ((-0.24, -0.09), (0.12, -0.24), (0.26, 0.02),
                               (-0.10, 0.24)), size=14)
            tag = board_text("Chain → SAS → Ray → Distance", 18, CHALK_GREEN,
                             "BOLD").move_to(np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(outline), FadeIn(names), run_time=min(
                leftover(tracker, "b1"), 0.8))
            self.play(Create(ab), Create(bc), FadeIn(ang_b), run_time=0.8)
            self.play(Create(cd), Create(ad), FadeIn(ang_c), run_time=0.8)
            self.play(Flash(VGroup(ab, bc, cd, ad), color=CHALK_YELLOW,
                            flash_radius=0.6), run_time=0.5)
            self.appear(tag, tracker, "b1", 0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: the measurement chain --------------------------------------
    def beat1_chain(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("Three Sides + Two Included Angles", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            caption = board_text("Follow the measurement chain", 17,
                                 CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, 2.24, 0]))

            row = VGroup(
                measure_card(r"AB=5\text{ cm}", CHALK_CYAN),
                degree_card(r"\angle B = 100^\circ", CHALK_AMBER),
                measure_card(r"BC=4.5\text{ cm}", CHALK_CYAN),
                degree_card(r"\angle C = 75^\circ", CHALK_PINK),
                measure_card(r"CD=6\text{ cm}", CHALK_CYAN),
            ).arrange(RIGHT, buff=0.42).move_to(
                np.array([BOARD_CX, 0.75, 0]))
            arrows = VGroup(*[
                Arrow(row[i].get_right() + RIGHT * 0.06,
                      row[i + 1].get_left() + LEFT * 0.06, buff=0,
                      color=CHALK_WHITE, stroke_width=2.2, tip_length=0.14,
                      max_stroke_width_to_length_ratio=10)
                for i in range(4)])
            sas = VGroup(*[
                board_text(s, 16, CHALK_GREEN, "BOLD").move_to(
                    np.array([card.get_center()[0], 0.16, 0]))
                for card, s in zip(row, "SASAS")])
            boxes = VGroup(*[card[0] for card in row])
            strip = board_text("S.A.S.A.S", 22, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -1.35, 0]))
            box = SurroundingRectangle(strip, color=CHALK_GREEN, buff=0.16,
                                       corner_radius=0.1, stroke_width=2.6)
            spell = board_text("Side – Angle – Side – Angle – Side", 16,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -1.92, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(caption), FadeIn(boxes), FadeIn(arrows),
                      run_time=0.8)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(row[0][1]), FadeIn(sas[0]), run_time=0.4)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeIn(row[1][1]), FadeIn(sas[1]), run_time=0.4)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b3"))

            self.play(FadeIn(row[2][1]), FadeIn(sas[2]), run_time=0.4)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b4"))

            self.play(FadeIn(row[3][1]), FadeIn(sas[3]), run_time=0.4)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b5"))

            self.play(FadeIn(row[4][1]), FadeIn(sas[4]), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(strip, shift=UP * 0.1), Create(box),
                      FadeIn(spell), run_time=0.7)
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.wait(leftover(tracker, "b6"))
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: what "included" means --------------------------------------
    def beat2_included(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("What Does Included Mean?", 21, CHALK_AMBER,
                                 "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            included = board_text("Included = between\ntwo given sides", 16,
                                  CHALK_GREEN, "BOLD").move_to(
                np.array([3.05, -1.25, 0]))
            incl_box = SurroundingRectangle(included, color=CHALK_GREEN,
                                            buff=0.14, corner_radius=0.1,
                                            stroke_width=2.4)
            d = example_construction()
            A, B, C, D = d["quad"]
            names = self.vertex_letters(
                (A, B, C, D), ((-0.28, -0.10), (0.14, -0.30), (-0.26, 0.37),
                               (-0.10, 0.30)))
            full = Polygon(A, B, C, D, color=CHALK_WHITE, stroke_width=2.0)
            full.set_stroke(opacity=0.26)
            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=4.0)
            bc = Line(B, C, color=CHALK_YELLOW, stroke_width=4.0)
            cd = Line(C, D, color=CHALK_GREEN, stroke_width=4.0)
            ang_b = angle_mark(B, A, C, radius=0.80, color=CHALK_YELLOW,
                               label="100°")
            ang_c = angle_mark(C, B, D, radius=0.80, color=CHALK_GREEN,
                               label="75°")
            note_b = self.column_note("100° is between\nA B and B C", 1.15,
                                      color=CHALK_YELLOW)
            note_c = self.column_note("75° is between\nB C and C D", 0.10,
                                      color=CHALK_GREEN)
            chain = MathTex(r"AB \;-\; \angle B \;-\; BC \;-\; \angle C \;-\; CD",
                            font_size=30, color=CHALK_WHITE).move_to(
                np.array([BOARD_CX, -2.50, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(full), FadeIn(names), run_time=0.7)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(Create(ab), Create(bc), FadeIn(ang_b), FadeIn(note_b),
                      run_time=0.8)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            self.play(Create(cd), FadeIn(ang_c), FadeIn(note_c),
                      run_time=0.8)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeIn(included, shift=UP * 0.1), Create(incl_box),
                      run_time=min(leftover(tracker, "b3"), 0.7))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(chain, shift=UP * 0.1), run_time=0.6)
            self.wait(leftover(tracker, "b4"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: the 3 + 2 plan ---------------------------------------------
    def beat3_plan(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()

            heading = board_text("3 Build. 2 Finish.", 23, CHALK_AMBER, "BOLD"
                                 ).move_to(np.array([BOARD_CX, 2.72, 0]))
            lab_build = board_text("BUILD", 18, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX - 2.5, 2.15, 0]))
            build_cards = VGroup(
                measure_card(r"AB=5\text{ cm}", CHALK_YELLOW),
                degree_card(r"\angle B = 100^\circ", CHALK_YELLOW),
                measure_card(r"BC=4.5\text{ cm}", CHALK_YELLOW),
            ).arrange(DOWN, buff=0.20).move_to(
                np.array([BOARD_CX - 2.5, 1.05, 0]))
            tri = Polygon(np.array([-0.70, -1.40, 0]), np.array([0.05, 0.35, 0]),
                          np.array([0.80, -1.40, 0]), color=CHALK_CYAN,
                          stroke_width=2.6, fill_color=CHALK_CYAN,
                          fill_opacity=0.16)
            tri.move_to(np.array([BOARD_CX - 2.5, -1.55, 0]))
            tri.scale(0.74)
            ang_t = angle_mark(tri.get_vertices()[0], tri.get_vertices()[1],
                               tri.get_vertices()[2], radius=0.22,
                               color=CHALK_YELLOW)

            lab_finish = board_text("FINISH", 18, CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX + 2.6, 2.15, 0]))
            finish_cards = VGroup(
                degree_card(r"\angle C = 75^\circ", CHALK_PINK),
                measure_card(r"CD=6\text{ cm}", CHALK_CYAN),
            ).arrange(DOWN, buff=0.20).move_to(
                np.array([BOARD_CX + 2.6, 1.35, 0]))
            # a miniature of the last two: a ray from C, and the 6 cm arc
            mv = np.array([BOARD_CX + 2.6, -1.45, 0])
            m_arm = Line(mv + np.array([0.72, -0.30, 0]),
                         mv + np.array([-0.72, -0.30, 0]), color=CHALK_WHITE,
                         stroke_width=2.0)
            m_ray = Line(mv + np.array([0.72, -0.30, 0]),
                         mv + np.array([-0.60, 0.62, 0]), color=CHALK_PINK,
                         stroke_width=2.4)
            m_arc = Arc(radius=1.04, start_angle=170 * DEGREES,
                        angle=26 * DEGREES, arc_center=mv + np.array([0.72, -0.30, 0]),
                        color=CHALK_CYAN, stroke_width=2.4)
            m_dot = Dot(radius=0.08, color=CHALK_YELLOW).move_to(
                mv + np.array([-0.58, 0.52, 0]))
            m_d = board_text("D", 15, CHALK_WHITE, "BOLD").move_to(
                mv + np.array([-0.42, 0.72, 0]))
            flow = board_text("3 measurements → triangle, 2 → ray + distance",
                              17, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.45, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(lab_build), run_time=0.35)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.12)
                                    for c in build_cards], lag_ratio=0.25),
                      run_time=1.0)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(Create(tri), FadeIn(ang_t), run_time=0.8)
            self.wait(leftover(tracker, "b1"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(lab_finish), run_time=0.35)
            self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.12)
                                    for c in finish_cards], lag_ratio=0.28),
                      run_time=0.9)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b2"))

            self.play(Create(m_arm), Create(m_ray), Create(m_arc),
                      FadeIn(m_dot), FadeIn(m_d), run_time=1.0)
            self.play(FadeIn(flow, shift=UP * 0.1),
                      Circumscribe(m_dot, color=CHALK_YELLOW, stroke_width=2.4),
                      run_time=min(leftover(tracker, "b3"), 1.0))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: draw A B and set out 100 degrees at B ----------------------
    def beat4_build(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 2 — Start with SAS", 21, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            d = example_construction()
            A, B, C, D = d["quad"]
            names = self.vertex_letters(
                (A, B), ((-0.28, -0.10), (0.14, -0.30)))
            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=4.2)
            lab_ab = board_text("5 cm", 15, CHALK_YELLOW, "BOLD").move_to(
                (A + B) / 2 + DOWN * 0.30)
            prot = protractor(B, color=CHALK_AMBER, radius=0.95)
            tick_deg = d["bc_deg"]
            tick_dot = Dot(radius=0.07, color=CHALK_YELLOW).move_to(
                np.array(B, dtype=float) + 0.95 * unit(tick_deg))
            ang_mark = angle_mark(B, A, C, radius=0.62, color=CHALK_AMBER)
            ang_lab = board_text("100°", 15, CHALK_AMBER, "BOLD").move_to(
                np.array(B, dtype=float) + 1.32 * unit(
                    (d["ba_deg"] + tick_deg) / 2.0))
            ray_bc = self.ray_line(B, tick_deg, dist(B, C) * 1.12, CHALK_AMBER,
                                   3.2)
            card_ab = self.column_card(measure_card(r"AB=5\text{ cm}", CHALK_YELLOW), 1.55)
            card_b = self.column_card(degree_card(r"\angle B = 100^\circ",
                                                  CHALK_AMBER), 0.75)
            note = self.column_note("C must lie\nsomewhere on this ray.", -0.35)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.wait(leftover(tracker, "b0"))

            self.play(Create(ab), FadeIn(names), FadeIn(lab_ab), FadeIn(card_ab),
                      run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b1"))

            self.play(FadeIn(prot), run_time=0.6)
            self.play(FadeIn(tick_dot, scale=0.5), run_time=0.35)
            self.play(FadeIn(ang_mark), FadeIn(ang_lab), FadeIn(card_b),
                      run_time=min(leftover(tracker, "b2"), 0.6))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeOut(prot), run_time=0.4)
            self.play(Create(ray_bc), FadeIn(note, shift=UP * 0.08),
                      run_time=min(leftover(tracker, "b3"), 1.0))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["ding"], gain=-13)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: complete the triangle --------------------------------------
    def beat5_triangle(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 2 — Complete the Triangle", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            d = example_construction()
            A, B, C, D = d["quad"]
            names = self.vertex_letters(
                (A, B, C), ((-0.28, -0.10), (0.14, -0.30), (-0.26, 0.37)))
            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=4.2)
            lab_ab = board_text("5 cm", 15, CHALK_YELLOW, "BOLD").move_to(
                (A + B) / 2 + DOWN * 0.30)
            ray_bc = self.ray_line(B, d["bc_deg"], dist(B, C) * 1.12,
                                   CHALK_AMBER, 3.2)
            ang_mark = angle_mark(B, A, C, radius=0.62, color=CHALK_AMBER)
            ang_lab = board_text("100°", 15, CHALK_AMBER, "BOLD").move_to(
                np.array(B, dtype=float) + 1.32 * unit(
                    (d["ba_deg"] + d["bc_deg"]) / 2.0))
            c_dot = Dot(radius=0.10, color=CHALK_YELLOW).move_to(C)
            bc = Line(B, C, color=CHALK_YELLOW, stroke_width=4.2)
            # pushed towards the inside of the triangle: outward would run
            # into the step column
            lab_bc = side_label(B, C, B + C - A, "4.5 cm", CHALK_YELLOW, 15,
                                0.20)
            ac = DashedLine(A, C, color=CHALK_WHITE, stroke_width=2.0,
                            dash_length=0.14)
            tri = Polygon(A, B, C, color=CHALK_CYAN, stroke_width=2.6,
                          fill_color=CHALK_CYAN, fill_opacity=0.16)
            card_bc = self.column_card(measure_card(r"BC=4.5\text{ cm}", CHALK_YELLOW),
                                       1.55)
            card_b = self.column_card(degree_card(r"\angle B = 100^\circ",
                                                  CHALK_AMBER), 0.75)
            note = self.column_note("Triangle A B C is fixed\nby S.A.S.", -0.35)
            notgiven = board_text("A C was not given — the construction made it.",
                                  16, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.58, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(Create(ab), FadeIn(names), FadeIn(lab_ab), FadeIn(ang_mark),
                      FadeIn(ang_lab), FadeIn(ray_bc), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            # the compasses carry B C from the card to the ray
            self.compass_on(B, C, dist(B, C), 10, CHALK_GREEN,
                            hinge_dir=(1.0, -1.0, 0.0), leg_ratio=0.55)
            self.sweep_compass(tracker, "b1", 10)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(FadeIn(c_dot, scale=0.5),
                      Indicate(c_dot, color=CHALK_YELLOW, scale_factor=1.9),
                      run_time=min(leftover(tracker, "b2"), 0.8))
            self.play(Create(bc), FadeIn(lab_bc), FadeIn(card_bc),
                      run_time=min(leftover(tracker, "b2"), 0.8))
            self.play(FadeIn(card_b), run_time=0.3)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(Create(ac), FadeIn(tri), run_time=min(
                leftover(tracker, "b3"), 0.9))
            self.play(FadeIn(note, shift=UP * 0.08), FadeIn(notgiven),
                      Flash(tri, color=CHALK_CYAN, flash_radius=0.7),
                      run_time=0.8)
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: the second included angle gives D a direction --------------
    def beat6_second_angle(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 3 — The Angle at C", 21, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            d = example_construction()
            A, B, C, D = d["quad"]
            names = self.vertex_letters(
                (A, B, C), ((-0.28, -0.10), (0.14, -0.30), (-0.26, 0.37)))
            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=4.2)
            bc = Line(B, C, color=CHALK_YELLOW, stroke_width=4.2)
            tri = Polygon(A, B, C, color=CHALK_CYAN, stroke_width=2.4,
                          fill_color=CHALK_CYAN, fill_opacity=0.14)
            ang_b = angle_mark(B, A, C, radius=0.62, color=CHALK_AMBER,
                               label="100°")
            card_c = self.column_card(degree_card(r"\angle C = 75^\circ",
                                                  CHALK_PINK), 1.55)
            note1 = self.column_note("D could lie anywhere\non this ray.", 0.35)
            note2 = self.column_note("…but we still need\nthe distance from C.",
                                     -0.75, color=CHALK_YELLOW)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(tri), FadeIn(names), Create(ab), Create(bc),
                      FadeIn(ang_b), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            # the arm swings from C B round to 75 degrees, the arc growing
            self.setout_arm(C, d["cb_deg"], d["cd_deg"], dist(C, D) * 0.55,
                            0.60, CHALK_PINK)
            self.play(self.arm_sweep.animate.set_value(1.0), run_time=min(
                leftover(tracker, "b1"), 1.6))
            # inside the angle but clear of the A C edge, which lies in the
            # same wedge
            ang_c = board_text("75°", 15, CHALK_PINK, "BOLD").move_to(
                np.array(C, dtype=float) + 0.85 * unit(
                    d["cb_deg"] + (d["cd_deg"] - d["cb_deg"]) / 3.0))
            self.play(FadeIn(ang_c), FadeIn(card_c),
                      run_time=min(leftover(tracker, "b1"), 0.6))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            ray_cd = self.ray_line(C, d["cd_deg"], dist(C, D) * 1.02,
                                   CHALK_PINK, 3.2)
            self.play(Transform(self.arm, ray_cd),
                      FadeIn(note1, shift=UP * 0.08),
                      run_time=min(leftover(tracker, "b2"), 1.0))
            self.play(FadeOut(self.arm_arc), run_time=0.3)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["ding"], gain=-13)

            # a dot that can sit anywhere along the ray: the angle gives a
            # direction, not a distance
            walker = Dot(radius=0.09, color=CHALK_YELLOW).move_to(
                ray_point(C, d["cd_deg"], dist(C, D) * 0.28))
            self.play(FadeIn(walker), run_time=0.3)
            self.play(walker.animate.move_to(
                ray_point(C, d["cd_deg"], dist(C, D) * 1.0)),
                run_time=min(leftover(tracker, "b3"), 1.6))
            self.play(FadeOut(walker), FadeIn(note2, shift=UP * 0.08),
                      run_time=0.6)
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: the last side fixes D --------------------------------------
    def beat7_locate_d(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 4 — Locate D", 21, CHALK_AMBER, "BOLD"
                                 ).move_to(np.array([BOARD_CX, 2.72, 0]))
            d = example_construction()
            A, B, C, D = d["quad"]
            names = self.vertex_letters(
                (A, B, C), ((-0.28, -0.10), (0.14, -0.30), (-0.26, 0.37)))
            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=4.2)
            bc = Line(B, C, color=CHALK_YELLOW, stroke_width=4.2)
            tri = Polygon(A, B, C, color=CHALK_CYAN, stroke_width=2.4,
                          fill_color=CHALK_CYAN, fill_opacity=0.14)
            ray_cd = self.ray_line(C, d["cd_deg"], dist(C, D) * 1.02,
                                   CHALK_PINK, 3.2)
            # inside the angle but clear of the A C edge, which lies in the
            # same wedge
            ang_c = board_text("75°", 15, CHALK_PINK, "BOLD").move_to(
                np.array(C, dtype=float) + 0.85 * unit(
                    d["cb_deg"] + (d["cd_deg"] - d["cb_deg"]) / 3.0))
            card_cd = self.column_card(measure_card(r"CD=6\text{ cm}", CHALK_CYAN), 1.55)
            card_c = self.column_card(degree_card(r"\angle C = 75^\circ",
                                                  CHALK_PINK), 0.75)
            d_dot = Dot(radius=0.11, color=CHALK_YELLOW).move_to(D)
            d_name = board_text("D", 17, CHALK_WHITE, "BOLD").move_to(
                D + 0.34 * unit(dir_deg(C, D)))
            ad = Line(A, D, color=CHALK_GREEN, stroke_width=4.2)
            quad = Polygon(A, B, C, D, color=CHALK_CYAN, stroke_width=2.4,
                           fill_color=CHALK_CYAN, fill_opacity=0.10)
            exact = self.column_note("Angle + Side\n= exact vertex", -0.35,
                                     color=CHALK_GREEN)
            rule = board_text("Direction + Distance → D", 17, CHALK_GREEN,
                              "BOLD").move_to(np.array([BOARD_CX, -2.58, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(tri), FadeIn(names), Create(ab), Create(bc),
                      Create(ray_cd), FadeIn(ang_c), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            # the compasses carry the 6 cm from the card to the ray
            self.compass_on(C, D, dist(C, D), 9, CHALK_GREEN,
                            hinge_dir=(1.0, -1.0, 0.0), leg_ratio=0.52)
            self.sweep_compass(tracker, "b1", 9)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(FadeIn(card_cd), run_time=0.3)
            self.play(FadeIn(d_dot, scale=0.5), FadeIn(d_name),
                      Indicate(d_dot, color=CHALK_YELLOW, scale_factor=2.1),
                      run_time=min(leftover(tracker, "b2"), 1.0))
            self.play(FadeIn(card_c), FadeIn(exact, shift=UP * 0.08),
                      run_time=0.5)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(Create(ad), FadeIn(quad), FadeIn(rule, shift=UP * 0.08),
                      Circumscribe(d_dot, color=CHALK_GREEN, stroke_width=2.6),
                      run_time=min(leftover(tracker, "b3"), 1.1))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: complete, verify, generalise -------------------------------
    def beat8_complete(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("Required Quadrilateral ABCD", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            d = example_construction()
            A, B, C, D = d["quad"]
            names = self.vertex_letters(
                (A, B, C, D), ((-0.28, -0.10), (0.14, -0.30), (-0.26, 0.37),
                               (-0.10, 0.30)))
            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=4.0)
            bc = Line(B, C, color=CHALK_YELLOW, stroke_width=4.0)
            cd = Line(C, D, color=CHALK_AMBER, stroke_width=4.0)
            ad = Line(A, D, color=CHALK_GREEN, stroke_width=4.2)
            ac = DashedLine(A, C, color=CHALK_WHITE, stroke_width=1.8,
                            dash_length=0.14)
            quad = Polygon(A, B, C, D, color=CHALK_CYAN, stroke_width=2.4,
                           fill_color=CHALK_CYAN, fill_opacity=0.10)
            ang_b = angle_mark(B, A, C, radius=0.80, color=CHALK_AMBER,
                               label="100°")
            ang_c = angle_mark(C, B, D, radius=0.80, color=CHALK_PINK,
                               label=None)
            ang_c_lab = board_text("75°", 15, CHALK_PINK, "BOLD").move_to(
                np.array(C, dtype=float) + 0.85 * unit(
                    d["cb_deg"] + (d["cd_deg"] - d["cb_deg"]) / 3.0))
            checks = VGroup(
                check_row(r"AB=5\text{ cm}", CHALK_GREEN, 15),
                check_row(r"100^\circ", CHALK_AMBER, 15),
                check_row(r"BC=4.5\text{ cm}", CHALK_GREEN, 15),
                check_row(r"75^\circ", CHALK_PINK, 15),
                check_row(r"CD=6\text{ cm}", CHALK_GREEN, 15),
            ).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to(
                np.array([3.05, 0.75, 0]))
            never = board_text("A D was never given.", 16, CHALK_WHITE, "BOLD"
                               ).move_to(np.array([BOARD_CX, -2.58, 0]))
            steps = VGroup(
                combo_card("1. SKETCH", "the 3 sides + 2 angles", CHALK_CYAN),
                combo_card("2. SAS TRIANGLE", "A B, angle B, B C", CHALK_GREEN),
                combo_card("3. SECOND ANGLE", "the ray from C", CHALK_PINK),
                combo_card("4. FINAL SIDE", "6 cm on that ray, then A D",
                           CHALK_YELLOW),
            ).arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to(
                np.array([3.40, 0.55, 0]))
            flow = board_text("Sketch → SAS → Ray → Length", 17, CHALK_GREEN,
                              "BOLD").move_to(np.array([BOARD_CX, -2.58, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(quad), FadeIn(names), Create(ab), Create(bc),
                      Create(cd), Create(ad), Create(ac), run_time=0.9)
            self.play(FadeIn(ang_b), FadeIn(ang_c), FadeIn(ang_c_lab),
                      run_time=min(leftover(tracker, "b0"), 0.6))
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1)
                                    for c in checks], lag_ratio=0.20),
                      run_time=min(leftover(tracker, "b0"), 1.6))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(never, shift=UP * 0.08), run_time=0.5)
            self.wait(leftover(tracker, "b1"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeOut(checks), FadeOut(ac), FadeOut(ang_b),
                      FadeOut(ang_c), FadeOut(ang_c_lab), FadeOut(never),
                      run_time=0.5)
            self.play(FadeIn(steps), run_time=min(leftover(tracker, "b2"), 1.2))
            self.play(FadeIn(flow, shift=UP * 0.1),
                      Circumscribe(quad, color=CHALK_AMBER, stroke_width=3,
                                   time_width=0.5),
                      run_time=min(leftover(tracker, "b2"), 1.0))
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 9: student challenge (Exercise 3.5(a)) ------------------------
    def beat9_challenge(self) -> None:
        with self.voiceover(text=NARRATION["scene9_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", 30, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, 2.62, 0]))
            tag = board_text("Exercise 3.5(a) — quadrilateral P Q R S", 15,
                             CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, 2.24, 0]))
            d = practice_construction()
            P, Q, R, S = d["quad"]
            names = self.vertex_letters(
                (P, Q, R, S), ((-0.28, -0.10), (0.12, -0.30), (0.30, 0.06),
                               (-0.10, 0.30)), letters="PQRS")
            rough = Polygon(P, Q, R, S, color=CHALK_WHITE, stroke_width=2.4,
                            fill_color=CHALK_WHITE, fill_opacity=0.06)
            pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=3.4)
            qr = Line(Q, R, color=CHALK_YELLOW, stroke_width=3.4)
            cards = VGroup(
                measure_card(r"PQ=3.6\text{ cm}", CHALK_CYAN, 15),
                degree_card(r"\angle Q = 135^\circ", CHALK_AMBER, 15),
                measure_card(r"QR=4.5\text{ cm}", CHALK_CYAN, 15),
                degree_card(r"\angle R = 60^\circ", CHALK_PINK, 15),
                measure_card(r"RS=5.6\text{ cm}", CHALK_CYAN, 15),
            ).arrange(DOWN, buff=0.15).move_to(np.array([3.05, 0.55, 0]))
            ask = board_text("Which three measurements construct the first "
                             "triangle?", 16, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX + 0.75, -2.62, 0]))
            prompt = board_text("Find the first Side–Angle–Side group.", 16,
                                CHALK_YELLOW, "BOLD").move_to(
                np.array([3.05, -1.30, 0]))
            pause = board_text("Pause and decide.", 17, CHALK_YELLOW, "BOLD"
                               ).move_to(np.array([3.05, -2.10, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(tag), run_time=0.4)
            self.play(FadeIn(rough), FadeIn(names), run_time=0.7)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.10)
                                    for c in cards], lag_ratio=0.14),
                      run_time=min(leftover(tracker, "b1"), 1.8))
            self.play(Create(pq), Create(qr), run_time=min(
                leftover(tracker, "b1"), 0.8))
            self.wait(leftover(tracker, "b1"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(ask, shift=RIGHT * 0.12),
                      FadeIn(prompt, shift=RIGHT * 0.12), run_time=0.5)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(pause, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b3"))

            self.challenge = {"rough": rough, "names": names, "cards": cards,
                              "ask": ask, "pause": pause, "prompt": prompt,
                              "pq": pq, "qr": qr, "points": (P, Q, R, S),
                              "data": d}
            self._capture_srt(tracker)

        play_challenge_countdown(self, seconds=4, sfx=self.sfx,
                                 position=np.array([BOARD_CX, BOARD_CY, 0]))

        with self.voiceover(text=NARRATION["scene9_reveal"]) as tracker:
            ch = self.challenge
            P, Q, R, S = ch["points"]
            d = ch["data"]
            names = ch["names"]

            self.play(FadeOut(ch["pause"]), FadeOut(ch["ask"]),
                      FadeOut(ch["prompt"]), run_time=0.4)
            self.wait(leftover(tracker, "b0"))

            tri = Polygon(P, Q, R, color=CHALK_GREEN, stroke_width=3.0,
                          fill_color=CHALK_GREEN, fill_opacity=0.14)
            badge = board_text("First triangle: P Q R", 17, CHALK_GREEN, "BOLD"
                               ).move_to(np.array([3.05, -1.55, 0]))
            badge2 = board_text("built by S.A.S", 15, CHALK_GREEN, "BOLD"
                                ).move_to(np.array([3.05, -1.93, 0]))
            self.play(Create(tri),
                      Indicate(ch["cards"][1], color=CHALK_AMBER,
                               scale_factor=1.12),
                      Circumscribe(tri, color=CHALK_GREEN, stroke_width=2.6,
                                   time_width=0.6),
                      run_time=min(leftover(tracker, "b1"), 1.2))
            self.play(FadeIn(badge, shift=UP * 0.1), FadeIn(badge2),
                      run_time=min(leftover(tracker, "b1"), 0.6))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            ray_r = self.ray_line(R, d["cd_deg"], dist(R, S) * 1.06, CHALK_PINK,
                                  3.0)
            s_arc = Arc(radius=dist(R, S), start_angle=(d["cd_deg"] - 9) * DEGREES,
                        angle=18 * DEGREES, arc_center=np.array(R, dtype=float),
                        color=CHALK_CYAN, stroke_width=2.6)
            self.play(Create(ray_r), run_time=min(leftover(tracker, "b2"), 0.8))
            self.play(Create(s_arc), run_time=min(leftover(tracker, "b2"), 0.8))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b2"))

            s_dot = Dot(radius=0.10, color=CHALK_YELLOW).move_to(S)
            ps = Line(P, S, color=CHALK_GREEN, stroke_width=3.6)
            quad = Polygon(P, Q, R, S, color=CHALK_CYAN, stroke_width=2.4,
                           fill_color=CHALK_CYAN, fill_opacity=0.12)
            built = board_text("S.A.S builds. A.S finishes.", 16, CHALK_GREEN,
                               "BOLD").move_to(np.array([BOARD_CX, -2.62, 0]))
            self.play(FadeIn(s_dot, scale=0.5), Create(ps), FadeIn(quad),
                      FadeIn(built, shift=UP * 0.08),
                      Indicate(s_dot, color=CHALK_YELLOW, scale_factor=2.1),
                      Circumscribe(names[3], color=CHALK_YELLOW,
                                   fade_out=True),
                      run_time=min(leftover(tracker, "b3"), 1.2))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap -----------------------------------------------------
    def beat10_recap(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("Three Sides + Two Included Angles", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            d = example_construction(
                centre=np.array([BOARD_CX - 2.8, 0.35, 0]), scale=0.60)
            A, B, C, D = d["quad"]
            names = self.vertex_letters(
                (A, B, C, D), ((-0.26, -0.09), (0.12, -0.26), (0.26, 0.02),
                               (-0.10, 0.26)), size=15)
            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=3.4)
            bc = Line(B, C, color=CHALK_YELLOW, stroke_width=3.4)
            cd = Line(C, D, color=CHALK_AMBER, stroke_width=3.4)
            ad = Line(A, D, color=CHALK_GREEN, stroke_width=3.6)
            tri = Polygon(A, B, C, color=CHALK_YELLOW, stroke_width=3.0,
                          fill_color=CHALK_YELLOW, fill_opacity=0.16)
            quad = Polygon(A, B, C, D, color=CHALK_CYAN, stroke_width=2.2,
                           fill_color=CHALK_CYAN, fill_opacity=0.10)
            ang_b = angle_mark(B, A, C, radius=0.58, color=CHALK_AMBER,
                               label="100°")
            ang_c = angle_mark(C, B, D, radius=0.58, color=CHALK_PINK,
                               label=None)
            ang_c_lab = board_text("75°", 15, CHALK_PINK, "BOLD").move_to(
                np.array(C, dtype=float) + 0.92 * unit(
                    d["cb_deg"] + 0.24 * (d["cd_deg"] - d["cb_deg"])))

            rows = VGroup(
                summary_row(1, "First three measurements:",
                            r"\triangle ABC", CHALK_YELLOW),
                summary_row(2, "Next angle: a", r"direction", CHALK_PINK),
                summary_row(3, "Final side: the", r"distance", CHALK_CYAN),
            ).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX + 1.85, 1.15, 0]))
            final = board_text("S.A.S builds the first triangle.", 17,
                               CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -1.90, 0]))
            take = board_text("Angle gives direction. Side gives distance.",
                              16, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.42, 0]))
            acr = board_text("S.A.S.A.S", 18, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX - 2.8, -1.62, 0]))
            acr_box = SurroundingRectangle(acr, color=CHALK_GREEN, buff=0.14,
                                          corner_radius=0.1, stroke_width=2.4)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(quad), FadeIn(names), Create(tri), Create(ab),
                      Create(bc), FadeIn(ang_b), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(rows[0], shift=RIGHT * 0.12), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            self.play(Create(cd), FadeIn(ang_c), FadeIn(ang_c_lab),
                      FadeIn(rows[1], shift=RIGHT * 0.12),
                      run_time=min(leftover(tracker, "b2"), 0.9))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b2"))

            self.play(Create(ad), FadeIn(rows[2], shift=RIGHT * 0.12),
                      run_time=min(leftover(tracker, "b3"), 0.9))
            self.play(FadeIn(final, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(take), FadeIn(acr), Create(acr_box),
                      Circumscribe(quad, color=CHALK_AMBER, stroke_width=3,
                                   time_width=0.5),
                      run_time=min(leftover(tracker, "b3"), 1.0))
            self.add_sound(self.sfx["success"], gain=-11)
            self.wait(leftover(tracker, "b3"))

            summary = VGroup(quad, names, tri, ab, bc, cd, ad, ang_b, ang_c,
                             ang_c_lab, rows, final, take, acr, acr_box)
            thanks = board_text("Thank You for Watching!", 40, CHALK_WHITE,
                                "BOLD")
            thanks2 = board_text("See you in the next lesson :)", 25,
                                 CHALK_CYAN)
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

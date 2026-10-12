"""Scene beats for Storyboard 07 (special quadrilaterals)."""

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
        """Lay a pair of compasses down: fade a static copy and drop the live
        `always_redraw` object, whose updater would rebuild it every frame."""
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

    def shape_sketch(self, pts, color=CHALK_WHITE, fill=CHALK_WHITE,
                     width=2.4, opacity=0.10):
        return Polygon(*pts, color=color, stroke_width=width,
                       fill_color=fill, fill_opacity=opacity)

    # -- Scene 0: title ------------------------------------------------------
    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Special Quadrilaterals", 34, CHALK_WHITE,
                               "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 2.00, 0]))
            sub = board_text("Parallelogram · Rhombus · Square", 20,
                             CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 1.12, 0]))
            self.play(FadeIn(title, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(sub, color=CHALK_YELLOW, scale_factor=1.03),
                      run_time=max(leftover(tracker, "b0"), 0.4))
            self.add_sound(self.sfx["ding"], gain=-13)

            # one small figure of each kind, with its name
            p_pts = parallelogram_frame(
                centre=np.array([BOARD_CX - 3.0, -0.85, 0]), scale=0.24)["quad"]
            r_pts = rhombus_frame(
                centre=np.array([BOARD_CX, -0.85, 0]), scale=0.30)["quad"]
            s_pts = square_frame(
                centre=np.array([BOARD_CX + 3.0, -0.85, 0]), scale=0.34)["quad"]
            figs = VGroup(
                VGroup(self.shape_sketch(p_pts, CHALK_WHITE, CHALK_CYAN,
                                         opacity=0.14),
                       board_text("PARALLELOGRAM", 13, CHALK_CYAN, "BOLD"
                                  ).move_to(np.array([BOARD_CX - 3.0, -2.05, 0]))),
                VGroup(self.shape_sketch(r_pts, CHALK_WHITE, CHALK_PINK,
                                         opacity=0.14),
                       board_text("RHOMBUS", 13, CHALK_PINK, "BOLD").move_to(
                           np.array([BOARD_CX, -2.05, 0]))),
                VGroup(self.shape_sketch(s_pts, CHALK_WHITE, CHALK_GREEN,
                                         opacity=0.14),
                       board_text("SQUARE", 13, CHALK_GREEN, "BOLD").move_to(
                           np.array([BOARD_CX + 3.0, -2.05, 0]))),
            )
            tag = board_text("Property → Missing Information → Construction",
                             17, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, 0.35, 0]))

            self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.1) for f in figs],
                                  lag_ratio=0.3),
                      run_time=min(leftover(tracker, "b1"), 1.4))
            self.appear(tag, tracker, "b1", 0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: three short lists of measurements --------------------------
    def beat1_special(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("Special Shape = Extra Information", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            cols = (BOARD_CX - 3.05, BOARD_CX, BOARD_CX + 3.05)
            names = ("PARALLELOGRAM", "RHOMBUS", "SQUARE")
            givens = (("Given:", "2 sides", "+ 1 angle"),
                      ("Given:", "2 diagonals", ""),
                      ("Given:", "1 diagonal", ""))
            asks = ("Only 3 measurements?", "Only 2 measurements?",
                    "Can this be enough?")
            props = (("Opposite angles equal;", "consecutive angles",
                      "supplementary"),
                     ("Diagonals bisect", "each other at 90°", ""),
                     ("Equal perpendicular-", "bisecting diagonals", ""))

            boxes, heads, give_txt, qmarks, prop_txt = (VGroup() for _ in range(5))
            for x, name, gv, pk in zip(cols, names, givens, props):
                box = RoundedRectangle(corner_radius=0.14, width=3.05,
                                       height=2.90, stroke_color=CHALK_WHITE,
                                       stroke_width=2.0, fill_color="#16202B",
                                       fill_opacity=0.45).move_to(
                    np.array([x, 0.30, 0]))
                head = board_text(name, 15, CHALK_YELLOW, "BOLD").move_to(
                    np.array([x, 1.50, 0]))
                # empty entries would become empty Text mobjects
                give = VGroup(*[board_text(line, 14, colour, "BOLD")
                                for line, colour in zip(gv, (CHALK_WHITE,
                                                             CHALK_CYAN,
                                                             CHALK_CYAN))
                                if line]).arrange(DOWN, buff=0.10).move_to(
                    np.array([x, 0.80, 0]))
                qm = board_text("?", 30, CHALK_PINK, "BOLD").move_to(
                    np.array([x, -0.25, 0]))
                prop = VGroup(*[board_text(line, 13, CHALK_GREEN, "BOLD")
                                for line in pk if line]
                              ).arrange(DOWN, buff=0.08).move_to(
                    np.array([x, -0.35, 0]))
                boxes.add(box)
                heads.add(head)
                give_txt.add(give)
                qmarks.add(qm)
                prop_txt.add(prop)

            question = board_text(asks[0], 14, CHALK_WHITE, "BOLD").move_to(
                np.array([cols[0], -0.85, 0]))
            question2 = board_text(asks[1], 14, CHALK_WHITE, "BOLD").move_to(
                np.array([cols[1], -0.85, 0]))
            question3 = board_text(asks[2], 14, CHALK_WHITE, "BOLD").move_to(
                np.array([cols[2], -0.85, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(boxes), LaggedStart(*[
                FadeIn(h, shift=UP * 0.08) for h in heads], lag_ratio=0.2),
                run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(give_txt[0]), FadeIn(qmarks[0]), FadeIn(question),
                      run_time=0.6)
            self.wait(leftover(tracker, "b0b"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(give_txt[1]), FadeIn(qmarks[1]), FadeIn(question2),
                      run_time=0.6)
            self.wait(leftover(tracker, "b1"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(give_txt[2]), FadeIn(qmarks[2]), FadeIn(question3),
                      run_time=0.6)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["click"], gain=-15)

            # the property is the key: each question mark turns into one
            self.play(*[FadeOut(q) for q in qmarks],
                      *[FadeIn(p, shift=UP * 0.08) for p in prop_txt],
                      *[FadeOut(q) for q in (question, question2, question3)],
                      run_time=min(leftover(tracker, "b3"), 1.2))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: parallelogram, find the missing angles ---------------------
    def beat2_parallelogram(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("Use the Properties First", 21, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            d = parallelogram_frame()
            B, E, L, T = d["quad"]
            names = self.vertex_letters(
                (B, E, L, T), ((-0.10, -0.28), (0.12, -0.30), (0.30, 0.10),
                               (-0.30, 0.10)), letters="BELT")
            quad = self.shape_sketch((B, E, L, T), CHALK_WHITE, CHALK_WHITE,
                                     width=2.2, opacity=0.08)
            card_be = self.column_card(measure_card(r"BE=4.2\text{ cm}", CHALK_CYAN), 1.55)
            card_el = self.column_card(measure_card(r"EL=5\text{ cm}", CHALK_CYAN), 0.95)
            card_t = self.column_card(degree_card(r"\angle T = 45^\circ",
                                                  CHALK_YELLOW), 0.35)
            # the angle at T is between the sides T L and T B -- T E is the
            # diagonal and does not bound it
            ang_t = angle_mark(T, L, B, radius=0.46, color=CHALK_YELLOW,
                               label=None)
            ang_t_lab = board_text("45°", 15, CHALK_YELLOW, "BOLD").move_to(
                np.array(T, dtype=float) + 1.05 * unit(
                    (dir_deg(T, L) + dir_deg(T, B)) / 2.0))
            note_opp = self.column_note("Opposite angles\nare equal", -0.55,
                                       color=CHALK_YELLOW)
            ang_e = angle_mark(E, B, L, radius=0.46, color=CHALK_YELLOW,
                               label=None)
            ang_e_lab = board_text("45°", 15, CHALK_YELLOW, "BOLD").move_to(
                np.array(E, dtype=float) + 0.90 * unit(
                    (dir_deg(E, B) + dir_deg(E, L)) / 2.0))
            note_sup = self.column_note("Consecutive angles\nadd to 180°", -1.25,
                                       color=CHALK_PINK)
            calc = self.column_card(value_card(r"180^\circ - 45^\circ = "
                                               r"135^\circ", CHALK_PINK), -2.15)
            ang_l = angle_mark(L, E, T, radius=0.50, color=CHALK_PINK,
                               label="135°")
            ang_b = angle_mark(B, E, T, radius=0.50, color=CHALK_PINK,
                               label="135°")
            allfour = board_text("45°, 135°, 45°, 135° — from one given angle",
                                 17, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(quad), FadeIn(names), FadeIn(card_be),
                      FadeIn(card_el), FadeIn(card_t), run_time=0.8)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(ang_t), FadeIn(ang_t_lab), run_time=0.5)
            self.wait(leftover(tracker, "b1"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(note_opp), FadeIn(ang_e), FadeIn(ang_e_lab),
                      run_time=min(leftover(tracker, "b2"), 0.9))
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(note_sup), FadeIn(calc),
                      FadeIn(ang_l),
                      run_time=min(leftover(tracker, "b3"), 0.9))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(ang_b), run_time=0.4)
            self.wait(leftover(tracker, "b4"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(allfour, shift=UP * 0.08),
                      Circumscribe(quad, color=CHALK_AMBER, stroke_width=3,
                                   time_width=0.5),
                      run_time=min(leftover(tracker, "b5"), 1.1))
            self.wait(leftover(tracker, "b5"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: construct the parallelogram --------------------------------
    def beat3_construct_belt(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 2 — Build Triangle BEL", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            d = parallelogram_frame()
            B, E, L, T = d["quad"]
            names = self.vertex_letters(
                (B, E), ((-0.10, -0.28), (0.12, -0.30)), letters="BE")
            be = Line(B, E, color=CHALK_YELLOW, stroke_width=4.2)
            lab_be = board_text("4.2 cm", 15, CHALK_YELLOW, "BOLD").move_to(
                (B + E) / 2 + DOWN * 0.30)
            lab_e = board_text("45°", 15, CHALK_YELLOW, "BOLD").move_to(
                np.array(E, dtype=float) + 0.86 * unit(
                    (d["eb_deg"] + d["el_deg"]) / 2.0))
            ray_el = self.ray_line(E, d["el_deg"], dist(E, L),
                                   CHALK_AMBER, 3.2)
            l_dot = Dot(radius=0.10, color=CHALK_YELLOW).move_to(L)
            # radially clear of the arc that marks L
            l_name = board_text("L", 17, CHALK_WHITE, "BOLD").move_to(
                L + 0.42 * unit(d["el_deg"]))
            el = Line(E, L, color=CHALK_YELLOW, stroke_width=4.0)
            lab_el = side_label(E, L, B, "5 cm", CHALK_YELLOW, 15, 0.20)
            tri = Polygon(B, E, L, color=CHALK_CYAN, stroke_width=2.6,
                          fill_color=CHALK_CYAN, fill_opacity=0.16)
            card_be = self.column_card(measure_card(r"BE=4.2\text{ cm}", CHALK_CYAN), 1.55)
            card_el = self.column_card(measure_card(r"EL=5\text{ cm}", CHALK_CYAN), 0.95)
            note_tri = self.column_note("Triangle B E L is fixed\nby S.A.S.",
                                        -0.10)
            # outside the figure: the triangle's own diagonal runs through
            # the middle of both 135 degree corners
            lab_b = board_text("135°", 15, CHALK_PINK, "BOLD").move_to(
                np.array(B, dtype=float) + 1.30 * unit(-35.0))
            lab_l = board_text("135°", 15, CHALK_PINK, "BOLD").move_to(
                np.array(L, dtype=float) + 1.00 * unit(20.0))
            t_dot = Dot(radius=0.10, color=CHALK_YELLOW).move_to(T)
            t_name = board_text("T", 17, CHALK_WHITE, "BOLD").move_to(
                T + np.array([-0.30, 0.10, 0]))
            quad = Polygon(B, E, L, T, color=CHALK_CYAN, stroke_width=2.4,
                           fill_color=CHALK_CYAN, fill_opacity=0.10)
            done = board_text("PARALLELOGRAM COMPLETE", 16, CHALK_GREEN, "BOLD"
                              ).move_to(np.array([3.05, -1.85, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.wait(leftover(tracker, "b0"))

            self.play(Create(be), FadeIn(names), FadeIn(lab_be), FadeIn(card_be),
                      run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b1"))

            self.setout_arm(E, d["eb_deg"], d["el_deg"], dist(E, L) * 0.55,
                            0.52, CHALK_AMBER)
            self.play(self.arm_sweep.animate.set_value(1.0), run_time=min(
                leftover(tracker, "b2"), 0.9))
            self.play(Transform(self.arm, ray_el), FadeIn(lab_e),
                      run_time=min(leftover(tracker, "b2"), 0.5))
            self.play(FadeOut(self.arm_arc), run_time=0.25)
            self.compass_on(E, L, dist(E, L), 10, CHALK_GREEN,
                            hinge_dir=(1.0, -1.0, 0.0), leg_ratio=0.55)
            self.sweep_compass(tracker, "b2", 10)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(FadeIn(l_dot, scale=0.5), FadeIn(l_name), Create(el),
                      FadeIn(lab_el), FadeIn(card_el), FadeIn(tri),
                      FadeIn(note_tri),
                      run_time=min(leftover(tracker, "b3"), 1.1))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b3"))

            self.setout_arm(B, d["be_deg"], d["ebt_deg"], dist(B, T) * 0.62,
                            0.60, CHALK_PINK)
            self.play(self.arm_sweep.animate.set_value(1.0), run_time=min(
                leftover(tracker, "b4"), 0.9))
            self.play(Transform(self.arm,
                                self.ray_line(B, d["ebt_deg"],
                                              dist(B, T) * 1.05, CHALK_PINK,
                                              3.0)),
                      FadeIn(lab_b), run_time=min(leftover(tracker, "b4"), 0.5))
            self.play(FadeOut(self.arm_arc), run_time=0.25)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b4"))

            self.setout_arm(L, d["le_deg"], d["lt_deg"], dist(L, T) * 0.62,
                            0.60, CHALK_PINK)
            self.play(self.arm_sweep.animate.set_value(1.0), run_time=min(
                leftover(tracker, "b5"), 0.9))
            self.play(Transform(self.arm,
                                self.ray_line(L, d["lt_deg"],
                                              dist(L, T) * 1.05, CHALK_PINK,
                                              3.0)),
                      FadeIn(lab_l), run_time=min(leftover(tracker, "b5"), 0.5))
            self.play(FadeOut(self.arm_arc), run_time=0.25)

            self.play(FadeIn(t_dot, scale=0.5), FadeIn(t_name), FadeIn(quad),
                      FadeIn(done, shift=UP * 0.08),
                      Circumscribe(t_dot, color=CHALK_YELLOW,
                                   stroke_width=2.6),
                      run_time=min(leftover(tracker, "b5"), 1.2))
            self.wait(leftover(tracker, "b5"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)
    # -- Scene 4: the rhombus diagonal properties ----------------------------
    def beat4_rhombus_props(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()

            heading = board_text("RHOMBUS ABCD — Read the Diagonals", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            r = rhombus_frame()
            A, B, C, D = r["quad"]
            O = mid(A, C)
            names = self.vertex_letters(
                (A, B, C, D), ((-0.30, 0.02), (0.06, 0.26), (0.26, 0.02),
                               (0.06, -0.34)))
            ac = Line(A, C, color=CHALK_YELLOW, stroke_width=4.0)
            bd = Line(B, D, color=CHALK_PINK, stroke_width=4.0)
            o_dot = Dot(radius=0.09, color=CHALK_GREEN).move_to(O)
            o_name = board_text("O", 15, CHALK_GREEN, "BOLD").move_to(
                O + np.array([-0.36, -0.34, 0]))
            quad = self.shape_sketch((A, B, C, D), CHALK_WHITE, CHALK_WHITE,
                                     width=2.2, opacity=0.08)
            card_ac = self.column_card(measure_card(r"AC=4.5\text{ cm}", CHALK_YELLOW), 1.75)
            card_bd = self.column_card(measure_card(r"BD=6\text{ cm}", CHALK_PINK), 1.15)
            right = angle_mark(O, C, B, radius=0.26, color=CHALK_GREEN,
                               right_angle=True)
            right_lab = board_text("90°", 13, CHALK_GREEN, "BOLD").move_to(
                O + np.array([0.50, 0.44, 0]))
            note_perp = self.column_note("Diagonals are\nperpendicular", 0.35,
                                         color=CHALK_GREEN)
            mid_ticks = VGroup(
                Line(O + np.array([-0.06, 0.20, 0]),
                     O + np.array([0.06, 0.20, 0]), color=CHALK_WHITE,
                     stroke_width=2.4),
                Line(O + np.array([-0.06, -0.20, 0]),
                     O + np.array([0.06, -0.20, 0]), color=CHALK_WHITE,
                     stroke_width=2.4),
                Line(O + np.array([0.20, -0.06, 0]),
                     O + np.array([0.20, 0.06, 0]), color=CHALK_WHITE,
                     stroke_width=2.4),
                Line(O + np.array([-0.20, -0.06, 0]),
                     O + np.array([-0.20, 0.06, 0]), color=CHALK_WHITE,
                     stroke_width=2.4))
            note_bis = self.column_note("Diagonals bisect\neach other", -0.45,
                                        color=CHALK_WHITE)
            boxed = self.column_card(value_card(
                r"OB = OD = \tfrac{6}{2} = 3\text{ cm}", CHALK_GREEN), -1.35)
            strip = board_text("BISECT + PERPENDICULAR", 16, CHALK_GREEN, "BOLD"
                               ).move_to(np.array([BOARD_CX + 0.45, -2.50, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(quad), FadeIn(names), Create(ac), Create(bd),
                      FadeIn(o_dot), FadeIn(o_name), FadeIn(card_ac),
                      FadeIn(card_bd), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(right), FadeIn(right_lab), FadeIn(note_perp),
                      run_time=min(leftover(tracker, "b1"), 0.8))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            self.play(FadeIn(mid_ticks), FadeIn(note_bis),
                      run_time=min(leftover(tracker, "b2"), 0.8))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b2"))

            self.play(Indicate(mid_ticks, color=CHALK_WHITE,
                               scale_factor=1.15),
                      run_time=min(leftover(tracker, "b3"), 0.7))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b3"))

            self.play(FadeIn(boxed, shift=UP * 0.08),
                      FadeIn(strip, shift=UP * 0.08),
                      run_time=min(leftover(tracker, "b4"), 0.8))
            self.wait(leftover(tracker, "b4"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: construct the rhombus --------------------------------------
    def beat5_construct_rhombus(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 2 — Draw A C and Its Bisector", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            r = rhombus_frame()
            A, B, C, D = r["quad"]
            O = mid(A, C)
            names = self.vertex_letters(
                (A, C), ((-0.30, 0.02), (0.26, 0.02)), letters="AC")
            ac = Line(A, C, color=CHALK_YELLOW, stroke_width=4.2)
            # left of the perpendicular, clear of the compasses' legs
            lab_ac = board_text("4.5 cm", 15, CHALK_YELLOW, "BOLD").move_to(
                (A + C) / 2 + np.array([-0.78, -0.28, 0]))
            o_dot = Dot(radius=0.09, color=CHALK_GREEN).move_to(O)
            o_name = board_text("O", 15, CHALK_GREEN, "BOLD").move_to(
                O + np.array([-0.32, 0.30, 0]))
            card_ac = self.column_card(measure_card(r"AC=4.5\text{ cm}", CHALK_YELLOW), 1.55)
            perp_end_a, perp_end_b = perpendicular_ends(
                O, r["ac_deg"], dist(O, B) * 1.22)
            perp = DashedLine(perp_end_a, perp_end_b, color=CHALK_WHITE,
                              stroke_width=2.2, dash_length=0.16)
            note_perp = self.column_note("The perpendicular\nthrough O", 0.55)
            card_3 = self.column_card(value_card(r"\tfrac{6}{2} = 3\text{ cm}",
                                                 CHALK_GREEN), -0.35)
            b_dot = Dot(radius=0.10, color=CHALK_YELLOW).move_to(B)
            b_name = board_text("B", 17, CHALK_WHITE, "BOLD").move_to(
                B + np.array([0.34, 0.26, 0]))
            d_dot = Dot(radius=0.10, color=CHALK_YELLOW).move_to(D)
            d_name = board_text("D", 17, CHALK_WHITE, "BOLD").move_to(
                D + np.array([0.34, -0.34, 0]))
            sides = VGroup(
                Line(A, B, color=CHALK_GREEN, stroke_width=4.0),
                Line(B, C, color=CHALK_GREEN, stroke_width=4.0),
                Line(C, D, color=CHALK_GREEN, stroke_width=4.0),
                Line(D, A, color=CHALK_GREEN, stroke_width=4.0))
            quad = Polygon(A, B, C, D, color=CHALK_CYAN, stroke_width=2.4,
                           fill_color=CHALK_CYAN, fill_opacity=0.10)
            done = board_text("RHOMBUS COMPLETE", 16, CHALK_GREEN, "BOLD"
                              ).move_to(np.array([3.05, -1.45, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(Create(ac), FadeIn(names), FadeIn(lab_ac), FadeIn(o_dot),
                      FadeIn(o_name), FadeIn(card_ac), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(Create(perp), FadeIn(note_perp), run_time=min(
                leftover(tracker, "b1"), 0.8))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            # the compasses carry half of B D to both sides of O
            self.compass_on(O, B, dist(O, B), 12, CHALK_GREEN,
                            hinge_dir=(-1.0, 1.0, 0.0), leg_ratio=0.5)
            self.sweep_compass(tracker, "b2", 12, put_down=False)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(FadeIn(b_dot, scale=0.5), FadeIn(b_name),
                      FadeIn(card_3), run_time=min(
                          leftover(tracker, "b3"), 0.8))
            self.compass_on(O, D, dist(O, D), 12, CHALK_GREEN,
                            hinge_dir=(1.0, -1.0, 0.0), leg_ratio=0.5)
            self.sweep_compass(tracker, "b3", 12)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(FadeIn(d_dot, scale=0.5), FadeIn(d_name),
                      run_time=min(leftover(tracker, "b4"), 0.8))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b4"))

            self.play(Create(sides), FadeIn(quad), FadeIn(done, shift=UP * 0.08),
                      Circumscribe(quad, color=CHALK_AMBER, stroke_width=3,
                                   time_width=0.5),
                      run_time=min(leftover(tracker, "b5"), 1.2))
            self.wait(leftover(tracker, "b5"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: from rhombus to square -------------------------------------
    def beat6_square(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("From Rhombus to Square", 21, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            r = rhombus_frame()
            A, B, C, D = r["quad"]
            O = mid(A, C)
            names = self.vertex_letters(
                (A, B, C, D), ((-0.30, 0.02), (0.06, 0.26), (0.26, 0.02),
                               (0.06, -0.34)))
            rh = VGroup(
                Polygon(A, B, C, D, color=CHALK_WHITE, stroke_width=2.4,
                        fill_color=CHALK_CYAN, fill_opacity=0.10),
                Line(A, C, color=CHALK_YELLOW, stroke_width=3.6),
                Line(B, D, color=CHALK_PINK, stroke_width=3.6))
            sq = square_frame(centre=RHOMB_CENTRE, scale=RHOMB_SCALE, diag=6.0)
            J, M_, U, P_ = sq["quad"]
            sq_group = VGroup(
                Polygon(J, M_, U, P_, color=CHALK_WHITE, stroke_width=2.4,
                        fill_color=CHALK_GREEN, fill_opacity=0.10),
                Line(J, U, color=CHALK_YELLOW, stroke_width=3.6),
                Line(M_, P_, color=CHALK_PINK, stroke_width=3.6))
            ask = board_text("What if both diagonals are equal?", 17,
                             CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX + 0.85, -2.68, 0]))
            note_sq = self.column_note("Equal diagonals, bisecting\nat right "
                                       "angles: a square", 0.55, color=CHALK_GREEN)
            card_sq = self.column_card(value_card(r"4.2 \div 2 = 2.1\text{ cm}",
                                                  CHALK_GREEN), -0.45)
            # the exercise construction
            s = square_frame()
            J2, M2, U2, P2 = s["quad"]
            O2 = mid(J2, U2)
            perp_a, perp_b = perpendicular_ends(O2, s["ju_deg"],
                                                dist(O2, M2) * 1.05)
            perp = DashedLine(perp_a, perp_b, color=CHALK_WHITE,
                              stroke_width=2.2, dash_length=0.16)
            o2_dot = Dot(radius=0.09, color=CHALK_GREEN).move_to(O2)
            o2_name = board_text("O", 15, CHALK_GREEN, "BOLD").move_to(
                O2 + np.array([-0.32, 0.30, 0]))
            m_dot = Dot(radius=0.10, color=CHALK_YELLOW).move_to(M2)
            p_dot = Dot(radius=0.10, color=CHALK_YELLOW).move_to(P2)
            u_dot = Dot(radius=0.10, color=CHALK_YELLOW).move_to(U2)
            j_dot = Dot(radius=0.10, color=CHALK_YELLOW).move_to(J2)
            j_name = board_text("J", 17, CHALK_WHITE, "BOLD").move_to(
                J2 + np.array([-0.30, 0.02, 0]))
            u_name = board_text("U", 17, CHALK_WHITE, "BOLD").move_to(
                U2 + np.array([0.26, 0.02, 0]))
            m_name = board_text("M", 17, CHALK_WHITE, "BOLD").move_to(
                M2 + np.array([0.06, 0.26, 0]))
            p_name = board_text("P", 17, CHALK_WHITE, "BOLD").move_to(
                P2 + np.array([0.06, -0.34, 0]))
            ju = Line(J2, U2, color=CHALK_YELLOW, stroke_width=4.2)
            lab_ju = board_text("4.2 cm", 15, CHALK_YELLOW, "BOLD").move_to(
                (J2 + U2) / 2 + np.array([-0.62, -0.52, 0]))
            jump = VGroup(Line(J2, M2, color=CHALK_GREEN, stroke_width=4.0),
                          Line(M2, U2, color=CHALK_GREEN, stroke_width=4.0),
                          Line(U2, P2, color=CHALK_GREEN, stroke_width=4.0),
                          Line(P2, J2, color=CHALK_GREEN, stroke_width=4.0))
            jump_quad = Polygon(J2, M2, U2, P2, color=CHALK_CYAN,
                                stroke_width=2.4, fill_color=CHALK_CYAN,
                                fill_opacity=0.10)
            done = board_text("SQUARE COMPLETE", 16, CHALK_GREEN, "BOLD"
                              ).move_to(np.array([3.05, -1.45, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(rh), FadeIn(names), run_time=0.8)
            self.play(FadeIn(ask, shift=UP * 0.08), run_time=min(
                leftover(tracker, "b0"), 0.6))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(Transform(rh, sq_group), FadeOut(names),
                      run_time=min(
                leftover(tracker, "b1"), 1.4))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.wait(leftover(tracker, "b1"))

            self.play(FadeIn(note_sq), FadeIn(card_sq), run_time=min(
                leftover(tracker, "b2"), 0.7))
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["ding"], gain=-13)

            # the exercise: square J U M P from its diagonal
            self.play(FadeOut(rh), FadeOut(ask), FadeOut(note_sq),
                      FadeOut(card_sq), run_time=0.5)
            self.play(Create(ju), FadeIn(j_dot), FadeIn(u_dot), FadeIn(j_name),
                      FadeIn(u_name), FadeIn(lab_ju), FadeIn(o2_dot),
                      FadeIn(o2_name), run_time=0.9)
            self.play(Create(perp), run_time=min(
                leftover(tracker, "b3"), 0.8))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b3"))

            self.compass_on(O2, M2, dist(O2, M2), 12, CHALK_GREEN,
                            hinge_dir=(-1.0, 1.0, 0.0), leg_ratio=0.5)
            self.sweep_compass(tracker, "b4", 12, put_down=False)
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.play(FadeIn(m_dot, scale=0.5), FadeIn(m_name),
                      run_time=min(leftover(tracker, "b4"), 0.7))
            self.compass_on(O2, P2, dist(O2, P2), 12, CHALK_GREEN,
                            hinge_dir=(1.0, -1.0, 0.0), leg_ratio=0.5)
            self.sweep_compass(tracker, "b4", 12)
            self.play(FadeIn(p_dot, scale=0.5), FadeIn(p_name),
                      run_time=min(leftover(tracker, "b4"), 0.7))
            self.wait(leftover(tracker, "b4"))

            self.play(Create(jump), FadeIn(jump_quad),
                      FadeIn(done, shift=UP * 0.08),
                      Circumscribe(jump_quad, color=CHALK_AMBER,
                                   stroke_width=3, time_width=0.5),
                      run_time=min(leftover(tracker, "b5"), 1.2))
            self.wait(leftover(tracker, "b5"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: three shapes, three property strategies --------------------
    def beat7_compare(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("Which Property Unlocks the Construction?", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            cols = (BOARD_CX - 3.0, BOARD_CX, BOARD_CX + 3.0)
            names = ("PARALLELOGRAM", "RHOMBUS", "SQUARE")
            colors = (CHALK_CYAN, CHALK_PINK, CHALK_GREEN)
            keys = (("Opposite angles equal", "consecutive angles",
                     "sum to 180°"),
                    ("Diagonals bisect", "each other at 90°", ""),
                    ("Equal diagonals,", "perpendicular", "bisectors", ""))
            effects = (("→ the missing angles",),
                       ("→ every vertex from", "the diagonals"),
                       ("→ one more condition",))

            heads, figs, keys_txt, eff_txt = (VGroup() for _ in range(4))
            for i, (x, name, col) in enumerate(zip(cols, names, colors)):
                heads.add(board_text(name, 15, col, "BOLD").move_to(
                    np.array([x, 2.20, 0])))
                if i == 0:
                    pts = parallelogram_frame(centre=np.array([x, 1.00, 0]),
                                              scale=0.22)["quad"]
                elif i == 1:
                    pts = rhombus_frame(centre=np.array([x, 1.00, 0]),
                                        scale=0.26)["quad"]
                else:
                    pts = square_frame(centre=np.array([x, 1.00, 0]),
                                       scale=0.30)["quad"]
                figs.add(Polygon(*pts, color=CHALK_WHITE, stroke_width=2.2,
                                 fill_color=col, fill_opacity=0.12))
                keys_txt.add(VGroup(*[board_text(line, 13, col, "BOLD")
                                      for line in keys[i] if line]).arrange(
                    DOWN, buff=0.08).move_to(np.array([x, -0.30, 0])))
                eff_txt.add(VGroup(*[board_text(line, 13, CHALK_WHITE, "BOLD")
                                     for line in effects[i]]).arrange(
                    DOWN, buff=0.06).move_to(np.array([x, -1.10, 0])))

            question = board_text("So which property gives the missing "
                                  "information?", 17, CHALK_YELLOW, "BOLD"
                                  ).move_to(np.array([BOARD_CX, -1.95, 0]))
            flow = board_text("Given + Special Property → New Information → "
                              "Construction", 16, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(heads), run_time=0.7)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(figs[0], shift=UP * 0.08), FadeIn(keys_txt[0]),
                      FadeIn(eff_txt[0]), run_time=min(
                          leftover(tracker, "b1"), 0.9))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            self.play(FadeIn(figs[1], shift=UP * 0.08), FadeIn(keys_txt[1]),
                      FadeIn(eff_txt[1]), run_time=min(
                          leftover(tracker, "b2"), 0.9))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeIn(figs[2], shift=UP * 0.08), FadeIn(keys_txt[2]),
                      FadeIn(eff_txt[2]), run_time=min(
                          leftover(tracker, "b3"), 0.9))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b3"))

            self.play(FadeIn(question, shift=UP * 0.08), run_time=min(
                leftover(tracker, "b4"), 0.6))
            self.play(FadeIn(flow, shift=UP * 0.08), run_time=min(
                leftover(tracker, "b4"), 0.6))
            self.wait(leftover(tracker, "b4"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the method -------------------------------------------------
    def beat8_method(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("Analyse Before You Draw", 23, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            steps = VGroup(
                combo_card("1. IDENTIFY", "parallelogram? rhombus? square?",
                           CHALK_CYAN),
                combo_card("2. RECALL", "its angles, sides, diagonals",
                           CHALK_GREEN),
                combo_card("3. DERIVE", "180 - 45 = 135   or   6 / 2 = 3",
                           CHALK_PINK),
                combo_card("4. CONSTRUCT", "with ruler, compasses, protractor",
                           CHALK_YELLOW),
            ).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to(
                np.array([2.85, 0.55, 0]))
            flow = board_text("Shape → Property → Derived Measurement → "
                              "Construction", 16, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))
            # a small worked reminder on the left
            r = rhombus_frame(centre=np.array([BOARD_CX - 2.6, 0.45, 0]),
                              scale=0.32)
            A, B, C, D = r["quad"]
            O = mid(A, C)
            sketch = VGroup(
                Polygon(A, B, C, D, color=CHALK_WHITE, stroke_width=2.2,
                        fill_color=CHALK_WHITE, fill_opacity=0.06),
                Line(A, C, color=CHALK_YELLOW, stroke_width=2.8),
                Line(B, D, color=CHALK_PINK, stroke_width=2.8),
                Dot(radius=0.07, color=CHALK_GREEN).move_to(O),
                board_text("6 / 2 = 3", 14, CHALK_GREEN, "BOLD").move_to(
                    np.array([BOARD_CX - 2.6, -1.35, 0])))
            note = board_text("The property supplies\nwhat was not given", 15,
                              CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX - 2.6, -2.05, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(steps), run_time=1.1)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(sketch, shift=UP * 0.08), run_time=min(
                leftover(tracker, "b1"), 0.8))
            self.play(FadeIn(note, shift=UP * 0.08), run_time=min(
                leftover(tracker, "b1"), 0.5))
            self.wait(leftover(tracker, "b1"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(flow, shift=UP * 0.1),
                      Circumscribe(steps[1], color=CHALK_GREEN,
                                   stroke_width=2.4, time_width=0.6),
                      run_time=min(leftover(tracker, "b2"), 1.0))
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
            tag = board_text("Property first — construction second", 15,
                             CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, 2.24, 0]))

            # challenge A: a parallelogram whose angle A really is 65 degrees
            ca_c = np.array([BOARD_CX - 3.05, 0.30, 0])
            a4 = np.array([0.0, 0.0, 0.0])
            b4 = ray_point(a4, 0.0, 4.0)
            d4 = ray_point(a4, 65.0, 4.5)
            c4 = b4 + (d4 - a4)
            A1, B1, C1, D1 = to_board((a4, b4, c4, d4), ca_c, 0.34)
            qa = Polygon(A1, B1, C1, D1, color=CHALK_WHITE, stroke_width=2.2,
                         fill_color=CHALK_CYAN, fill_opacity=0.10)
            na = self.vertex_letters(
                (A1, B1, C1, D1), ((-0.24, -0.24), (0.10, -0.26), (0.24, 0.10),
                                   (-0.24, 0.10)))
            ang_a = angle_mark(A1, B1, D1, radius=0.30, color=CHALK_YELLOW,
                               label="65°")
            hand_a = board_text("A parallelogram with angle A = 65°", 15,
                                CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX - 3.05, -1.35, 0]))
            ask_a = board_text("What are the other three angles?", 15,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX - 3.05, -1.85, 0]))
            ans_a = board_text("65°, 115°, 115°", 16, CHALK_GREEN, "BOLD"
                               ).move_to(np.array([BOARD_CX - 3.05, -2.40, 0]))

            # challenge B: a rhombus with diagonals 8 and 6
            rb = rhombus_frame(centre=np.array([BOARD_CX + 2.55, 0.30, 0]),
                               scale=0.42, ac=8.0, bd=6.0)
            A2, B2, C2, D2 = rb["quad"]
            O2 = mid(A2, C2)
            qb = Polygon(A2, B2, C2, D2, color=CHALK_WHITE, stroke_width=2.2,
                         fill_color=CHALK_PINK, fill_opacity=0.10)
            diag_b = VGroup(Line(A2, C2, color=CHALK_YELLOW, stroke_width=3.0),
                            Line(B2, D2, color=CHALK_PINK, stroke_width=3.0))
            o2_dot = Dot(radius=0.08, color=CHALK_GREEN).move_to(O2)
            o2_name = board_text("O", 14, CHALK_GREEN, "BOLD").move_to(
                O2 + np.array([0.20, 0.14, 0]))
            hand_b = board_text("A rhombus: AC = 8 cm, BD = 6 cm", 15,
                                CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX + 2.55, -1.35, 0]))
            ask_b = board_text("How far is each vertex from O?", 15,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX + 2.55, -1.85, 0]))
            half_labels = VGroup(
                board_text("4 cm", 14, CHALK_YELLOW, "BOLD").move_to(
                    mid(O2, A2) + np.array([0.0, -0.30, 0])),
                board_text("4 cm", 14, CHALK_YELLOW, "BOLD").move_to(
                    mid(O2, C2) + np.array([0.0, -0.30, 0])),
                board_text("3 cm", 14, CHALK_PINK, "BOLD").move_to(
                    mid(O2, B2) + np.array([0.42, 0.0, 0])),
                board_text("3 cm", 14, CHALK_PINK, "BOLD").move_to(
                    mid(O2, D2) + np.array([0.42, 0.0, 0])))
            ans_b = board_text("OA = OC = 4 cm, OB = OD = 3 cm", 15,
                               CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX + 2.55, -2.40, 0]))
            pause = board_text("Pause and work them out.", 17, CHALK_YELLOW,
                               "BOLD").move_to(
                np.array([BOARD_CX, -2.70, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(tag), run_time=0.4)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(qa), FadeIn(na), FadeIn(ang_a), FadeIn(hand_a),
                      FadeIn(ask_a), run_time=0.8)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b1"))

            self.play(FadeIn(qb), FadeIn(diag_b), FadeIn(o2_dot),
                      FadeIn(o2_name), FadeIn(hand_b), FadeIn(ask_b),
                      run_time=0.8)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeIn(pause, shift=UP * 0.08), run_time=0.5)
            self.wait(leftover(tracker, "b3"))

            self.challenge = {"qa": qa, "na": na, "ang_a": ang_a, "hand_a": hand_a,
                              "ask_a": ask_a, "qb": qb, "diag_b": diag_b,
                              "o2_dot": o2_dot, "o2_name": o2_name,
                              "hand_b": hand_b, "ask_b": ask_b, "pause": pause,
                              "half": half_labels, "ans_a": ans_a, "ans_b": ans_b,
                              "pts_a": (A1, B1, C1, D1), "pts_b": (A2, B2, C2, D2)}
            self._capture_srt(tracker)

        play_challenge_countdown(self, seconds=4, sfx=self.sfx,
                                 position=np.array([BOARD_CX, BOARD_CY, 0]))

        with self.voiceover(text=NARRATION["scene9_reveal"]) as tracker:
            ch = self.challenge
            A1, B1, C1, D1 = ch["pts_a"]
            A2, B2, C2, D2 = ch["pts_b"]
            O2 = mid(A2, C2)

            self.play(FadeOut(ch["pause"]), FadeOut(ch["ang_a"]),
                      run_time=0.4)
            self.wait(leftover(tracker, "b0"))
            self.add_sound(self.sfx["pop"], gain=-13)

            # the parallelogram's four angles
            angs = VGroup(
                angle_mark(A1, B1, D1, radius=0.26, color=CHALK_YELLOW,
                           label="65°"),
                angle_mark(B1, A1, C1, radius=0.26, color=CHALK_GREEN,
                           label="115°"),
                angle_mark(C1, B1, D1, radius=0.26, color=CHALK_GREEN,
                           label="115°"),
                angle_mark(D1, A1, C1, radius=0.26, color=CHALK_YELLOW,
                           label="65°"))
            self.play(FadeIn(angs), run_time=min(leftover(tracker, "b1"), 1.2))
            self.play(FadeIn(ch["ans_a"], shift=UP * 0.06), run_time=min(
                leftover(tracker, "b1"), 0.5))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b1"))

            # the rhombus's half-diagonals
            right = angle_mark(O2, C2, B2, radius=0.22, color=CHALK_GREEN,
                               right_angle=True)
            sides_b = VGroup(
                Line(A2, B2, color=CHALK_GREEN, stroke_width=3.0),
                Line(B2, C2, color=CHALK_GREEN, stroke_width=3.0),
                Line(C2, D2, color=CHALK_GREEN, stroke_width=3.0),
                Line(D2, A2, color=CHALK_GREEN, stroke_width=3.0))
            self.play(FadeIn(right), FadeIn(ch["half"]), run_time=min(
                leftover(tracker, "b2"), 1.0))
            self.play(FadeIn(ch["ans_b"], shift=UP * 0.06), run_time=min(
                leftover(tracker, "b2"), 0.5))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b2"))

            self.play(Create(sides_b), run_time=min(leftover(tracker, "b3"), 1.0))
            self.play(Circumscribe(ch["qb"], color=CHALK_AMBER, stroke_width=3,
                                   time_width=0.5),
                      run_time=min(leftover(tracker, "b3"), 0.8))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap -----------------------------------------------------
    def beat10_recap(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("Know the Shape. Use Its Properties.", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            cols = (BOARD_CX - 3.0, BOARD_CX, BOARD_CX + 3.0)
            names = ("PARALLELOGRAM", "RHOMBUS", "SQUARE")
            colors = (CHALK_CYAN, CHALK_PINK, CHALK_GREEN)
            props = (("Opposite angles equal,", "consecutive angles add to 180°"),
                     ("Diagonals bisect", "at right angles"),
                     ("Equal perpendicular-", "bisecting diagonals"))
            figs, prop_txt, name_txt = (VGroup() for _ in range(3))
            for i, (x, name, col) in enumerate(zip(cols, names, colors)):
                name_txt.add(board_text(name, 14, col, "BOLD").move_to(
                    np.array([x, 2.18, 0])))
                if i == 0:
                    pts = parallelogram_frame(centre=np.array([x, 1.10, 0]),
                                              scale=0.22)["quad"]
                elif i == 1:
                    pts = rhombus_frame(centre=np.array([x, 1.10, 0]),
                                        scale=0.26)["quad"]
                else:
                    pts = square_frame(centre=np.array([x, 1.10, 0]),
                                       scale=0.30)["quad"]
                figs.add(Polygon(*pts, color=CHALK_WHITE, stroke_width=2.2,
                                 fill_color=col, fill_opacity=0.12))
                prop_txt.add(VGroup(*[board_text(line, 13, col, "BOLD")
                                      for line in props[i]]).arrange(
                    DOWN, buff=0.08).move_to(np.array([x, -0.35, 0])))
            chain = board_text("Special properties → missing measurements → "
                               "construction", 16, CHALK_GREEN, "BOLD"
                               ).move_to(np.array([BOARD_CX, -1.45, 0]))
            chain_box = SurroundingRectangle(chain, color=CHALK_GREEN, buff=0.16,
                                             corner_radius=0.1, stroke_width=2.4)
            final = board_text("Know the Shape. Use Its Properties. Construct "
                               "It.", 17, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.15, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(name_txt), FadeIn(figs), run_time=0.8)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(prop_txt[0]), run_time=min(
                leftover(tracker, "b1"), 0.6))
            self.wait(leftover(tracker, "b1"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(prop_txt[1]), FadeIn(prop_txt[2]),
                      run_time=min(leftover(tracker, "b2"), 0.7))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.play(FadeIn(chain, shift=UP * 0.08), Create(chain_box),
                      FadeIn(final, shift=UP * 0.08), run_time=min(
                          leftover(tracker, "b2"), 0.7))
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["success"], gain=-11)

            summary = VGroup(name_txt, figs, prop_txt, chain, chain_box, final)
            thanks = board_text("Thank You for Watching!", 40, CHALK_WHITE,
                                "BOLD")
            thanks2 = board_text("See you in the next lesson :)", 25,
                                 CHALK_CYAN)
            thanks_group = VGroup(thanks, thanks2).arrange(
                DOWN, buff=0.3).move_to(np.array([BOARD_CX, BOARD_CY, 0]))
            self.play(FadeOut(summary), FadeOut(heading), run_time=0.4)
            self.play(FadeIn(thanks, shift=UP * 0.1), run_time=0.5)
            self.add_sound(self.sfx["success"], gain=-11)
            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(thanks2, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b4"))
            self.play(Circumscribe(thanks_group, color=CHALK_AMBER,
                                   stroke_width=3, time_width=0.5),
                      run_time=0.25)
            self.play(Indicate(thanks, color=CHALK_WHITE, scale_factor=1.01),
                      run_time=rt(tracker.get_remaining_duration()))
            self._capture_srt(tracker)

        self.wait(END_HOLD)

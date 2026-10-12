"""Scene beats for Storyboard 05 (S.A.S.A.A)."""

    # ================================================================ beats ==

    # -- real SRT export -----------------------------------------------------
    def _capture_srt(self, tracker, words_per_line: int = 9) -> None:
        """Same ground-truth export as the rest of the series, with one change:
        a final chunk of one or two words is folded into the caption before it.
        A stand-alone last word keeps its own half-second caption, which lands
        mostly in silence at the end of the piece and reads badly."""
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
        """Lay a pair of compasses down on the desk.

        The tool is an `always_redraw` mobject: its updater rebuilds it at full
        opacity on every frame, so `FadeOut` on the live object never shows.
        Fade a static copy instead and drop the live one."""
        snap = tool.copy()
        snap.clear_updaters()
        self.remove(tool)
        self.add(snap)
        self.play(FadeOut(snap), run_time=run_time)

    def compass_on(self, centre, target, radius, spread, color,
                   hinge_dir=None, leg_ratio=0.62, bias: float = 0.0):
        """Park a pair of compasses with its needle on `centre` and its pencil
        at the start of the arc, ready to sweep.  `bias` rotates the whole
        sector when a symmetric arc would stray over the figure."""
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
                      hold: bool = True, seconds: float | None = None) -> None:
        """Sweep the compasses already on the board to the end of the arc."""
        budget = leftover(tracker, mark) if seconds is None else seconds
        span = 2 * spread if seconds is None else spread
        sweep_time = max(budget - (0.35 if put_down else 0.0) - reserve, 0.4)
        self.play(self.sweep.animate.set_value(span), run_time=sweep_time)
        if put_down:
            self.put_down_tool(self.tool)
        if hold and seconds is None:
            self.wait(leftover(tracker, mark))

    def setout_arm(self, vertex, start_deg, end_deg, length, radius, color,
                   stroke: float = 3.4):
        """An arm that swings from one direction to the other while the angle
        arc grows under it -- how an angle is set out on paper."""
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

    def vertex_letters(self, points, offsets, letters="PQRS", size=17,
                       color=CHALK_WHITE):
        """Vertex letters placed by hand, one offset each -- the automatic
        corners put a letter inside this elongated figure."""
        out = []
        for letter, p, off in zip(letters, points, offsets):
            shift = np.array([off[0], off[1], 0.0])
            out.append(board_text(letter, size, color, "BOLD").move_to(
                np.array(p, dtype=float) + shift))
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

    def bisect_inset(self, centre, scale=1.0):
        """A compact '75 degrees between 60 and 90' inset: the two standard
        angles, the bisector between them, and the arithmetic."""
        v = np.array(centre, dtype=float)
        base = Line(v, v + np.array([1.05, 0, 0]), color=CHALK_WHITE,
                    stroke_width=2.0)
        a60 = Line(v, v + np.array([np.cos(60 * DEGREES),
                                    np.sin(60 * DEGREES), 0]) * 0.92,
                   color=CHALK_CYAN, stroke_width=2.0)
        a90 = Line(v, v + np.array([0, 0.92, 0]), color=CHALK_AMBER,
                   stroke_width=2.0)
        bis = DashedLine(v, v + np.array([np.cos(75 * DEGREES),
                                          np.sin(75 * DEGREES), 0]) * 1.0,
                         color=CHALK_GREEN, stroke_width=2.2, dash_length=0.08)
        arc60 = Arc(radius=0.46, start_angle=0, angle=60 * DEGREES,
                    arc_center=v, color=CHALK_CYAN, stroke_width=1.6)
        arc90 = Arc(radius=0.58, start_angle=0, angle=90 * DEGREES,
                    arc_center=v, color=CHALK_AMBER, stroke_width=1.6)
        l60 = board_text("60°", 13, CHALK_CYAN, "BOLD").move_to(
            v + np.array([0.80, 0.14, 0]))
        l90 = board_text("90°", 13, CHALK_AMBER, "BOLD").move_to(
            v + np.array([-0.05, 1.16, 0]))
        l75 = board_text("75°", 13, CHALK_GREEN, "BOLD").move_to(
            v + np.array([1.05, 0.86, 0]))
        eq = board_text("75° = (60° + 90°)/2", 13, CHALK_GREEN, "BOLD"
                        ).move_to(v + np.array([1.02, -0.36, 0]))
        grp = VGroup(base, a60, a90, arc60, arc90, bis, l60, l90, l75, eq)
        grp.scale(scale, about_point=v)
        return grp

    # -- Scene 0: title ------------------------------------------------------
    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Construct a Quadrilateral", 33, CHALK_WHITE,
                               "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 1.85, 0]))
            sub = board_text("Two Sides and Three Angles", 20, CHALK_YELLOW,
                             "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 0.95, 0]))
            self.play(FadeIn(title, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(sub, color=CHALK_YELLOW, scale_factor=1.04),
                      run_time=max(leftover(tracker, "b0"), 0.4))
            self.add_sound(self.sfx["ding"], gain=-13)

            # the signature of this case: the S.A.S triangle and the two rays
            d = example_construction(
                centre=np.array([BOARD_CX + 0.35, -0.72, 0]), scale=0.24)
            P, Q, R, S = d["quad"]
            outline = Polygon(P, Q, R, S, color=CHALK_WHITE, stroke_width=2.2)
            outline.set_stroke(opacity=0.40)
            pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=3.4)
            qr = Line(Q, R, color=CHALK_YELLOW, stroke_width=3.4)
            ang_q = angle_mark(Q, P, R, radius=0.34, color=CHALK_AMBER,
                               label="100°")
            ray_p = self.ray_line(P, d["ps_deg"], dist(P, S) * 1.05,
                                  CHALK_CYAN, 2.6, True)
            ray_r = self.ray_line(R, d["rs_deg"], dist(R, S) * 1.05,
                                  CHALK_PINK, 2.6, True)
            names = self.vertex_letters(
                (P, Q, R, S), ((-0.22, -0.10), (0.10, -0.24), (0.24, 0.02),
                               (-0.08, 0.24)), size=14)
            tag = board_text("Sides → Triangle → Rays → Meet", 18, CHALK_GREEN,
                             "BOLD").move_to(np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(outline), FadeIn(names), run_time=min(
                leftover(tracker, "b1"), 0.8))
            self.play(Create(pq), Create(qr), FadeIn(ang_q), run_time=0.9)
            self.play(Create(ray_p), Create(ray_r), run_time=0.9)
            self.play(Flash(VGroup(ray_p, ray_r), color=CHALK_YELLOW,
                            flash_radius=0.6), run_time=0.5)
            self.appear(tag, tracker, "b1", 0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: two adjacent sides and three angles ------------------------
    def beat1_data(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("Two Sides and Three Angles", 22, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            lab_sides = board_text("2 adjacent sides", 17, CHALK_CYAN, "BOLD"
                                   ).move_to(np.array([BOARD_CX, 2.20, 0]))
            sides = VGroup(
                measure_card(r"PQ=4\text{ cm}", CHALK_CYAN),
                measure_card(r"QR=4.8\text{ cm}", CHALK_CYAN),
            ).arrange(RIGHT, buff=0.34).move_to(
                np.array([BOARD_CX, 1.68, 0]))
            lab_angles = board_text("3 angles", 17, CHALK_AMBER, "BOLD"
                                    ).move_to(np.array([BOARD_CX, 1.13, 0]))
            angles = VGroup(
                degree_card(r"\angle P = 75^\circ", CHALK_YELLOW),
                degree_card(r"\angle Q = 100^\circ", CHALK_AMBER),
                degree_card(r"\angle R = 120^\circ", CHALK_PINK),
            ).arrange(RIGHT, buff=0.30).move_to(
                np.array([BOARD_CX, 0.60, 0]))
            strip = board_text("S.A.S.A.A", 22, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -1.28, 0]))
            box = SurroundingRectangle(strip, color=CHALK_GREEN, buff=0.16,
                                       corner_radius=0.1, stroke_width=2.6)
            spell = board_text("Side – Angle – Side – Angle – Angle", 16,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -1.86, 0]))
            ask = board_text("Where do we begin?", 19, CHALK_WHITE, "BOLD"
                             ).move_to(np.array([BOARD_CX, -2.50, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(lab_sides), run_time=0.35)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.12)
                                    for c in sides], lag_ratio=0.28),
                      run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.wait(leftover(tracker, "b0b"))
            self.play(FadeIn(lab_angles), run_time=0.35)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.12)
                                    for c in angles], lag_ratio=0.22),
                      run_time=1.1)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b1"))

            self.play(FadeIn(strip, shift=UP * 0.1), Create(box),
                      FadeIn(spell), run_time=0.7)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: find the S.A.S triangle ------------------------------------
    def beat2_choose(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("Find the Side – Angle – Side Triangle", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            d = example_construction()
            P, Q, R, S = d["quad"]
            names = self.vertex_letters(
                (P, Q, R, S), ((-0.28, -0.10), (0.12, -0.30), (0.50, -0.40),
                               (-0.14, 0.34)))
            full = Polygon(P, Q, R, S, color=CHALK_WHITE, stroke_width=2.0)
            full.set_stroke(opacity=0.28)
            pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=4.0)
            qr = Line(Q, R, color=CHALK_YELLOW, stroke_width=4.0)
            ang_q = angle_mark(Q, P, R, radius=0.52, color=CHALK_YELLOW,
                               label="100°")
            tri = Polygon(P, Q, R, color=CHALK_CYAN, stroke_width=3.0,
                          fill_color=CHALK_CYAN, fill_opacity=0.16)
            ray_p = self.ray_line(P, d["ps_deg"], 4.40, CHALK_CYAN, 2.2, True)
            ray_r = self.ray_line(R, d["rs_deg"], 2.60, CHALK_PINK, 2.2, True)
            s_dot = Dot(radius=0.08, color=CHALK_YELLOW).move_to(S)

            c_pq = self.column_card(measure_card(r"PQ=4\text{ cm}", CHALK_YELLOW), 1.55)
            c_q = self.column_card(degree_card(r"\angle Q = 100^\circ", CHALK_YELLOW), 0.95)
            c_qr = self.column_card(measure_card(r"QR=4.8\text{ cm}", CHALK_YELLOW), 0.35)
            sas = board_text("Side – Angle – Side", 18, CHALK_GREEN, "BOLD"
                             ).move_to(np.array([3.05, -0.32, 0]))
            sas_short = board_text("S.A.S", 16, CHALK_GREEN, "BOLD").move_to(
                np.array([3.05, -0.72, 0]))
            later_lab = board_text("USE LATER", 15, CHALK_PINK, "BOLD"
                                   ).move_to(np.array([3.05, -1.15, 0]))
            later = VGroup(
                degree_card(r"\angle P = 75^\circ", CHALK_CYAN, 15),
                degree_card(r"\angle R = 120^\circ", CHALK_PINK, 15),
            ).arrange(DOWN, buff=0.18).move_to(np.array([3.05, -2.00, 0]))
            later_box = SurroundingRectangle(later, color=CHALK_PINK, buff=0.14,
                                             corner_radius=0.1,
                                             stroke_width=2.0)
            note = board_text("The included angle\ntells us the first "
                              "triangle.", 16, CHALK_WHITE, "BOLD").move_to(
                np.array([3.05, 2.26, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(full), FadeIn(names), FadeIn(ray_p), FadeIn(ray_r),
                      FadeIn(s_dot), run_time=0.8)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(Create(pq), FadeIn(c_pq), run_time=0.7)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            self.play(FadeIn(c_q), run_time=0.4)
            self.play(Create(qr), FadeIn(c_qr), FadeIn(ang_q),
                      run_time=min(leftover(tracker, "b2"), 0.9))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeIn(tri), FadeIn(sas), FadeIn(sas_short),
                      Circumscribe(tri, color=CHALK_CYAN, stroke_width=2.6,
                                   time_width=0.6),
                      run_time=min(leftover(tracker, "b3"), 1.0))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)

            self.play(FadeIn(later_lab), FadeIn(later), Create(later_box),
                      run_time=0.6)
            self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b4"))
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: the 3 + 2 plan ---------------------------------------------
    def beat3_plan(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()

            heading = board_text("3 Build. 2 Locate.", 23, CHALK_AMBER, "BOLD"
                                 ).move_to(np.array([BOARD_CX, 2.72, 0]))
            lab_build = board_text("BUILD", 18, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX - 2.5, 2.18, 0]))
            build_cards = VGroup(
                measure_card(r"PQ=4\text{ cm}", CHALK_YELLOW),
                degree_card(r"\angle Q = 100^\circ", CHALK_YELLOW),
                measure_card(r"QR=4.8\text{ cm}", CHALK_YELLOW),
            ).arrange(DOWN, buff=0.22).move_to(
                np.array([BOARD_CX - 2.5, 1.05, 0]))
            tri = Polygon(np.array([-0.62, -1.30, 0]), np.array([0.04, 0.30, 0]),
                          np.array([0.70, -1.30, 0]), color=CHALK_CYAN,
                          stroke_width=2.6, fill_color=CHALK_CYAN,
                          fill_opacity=0.16)
            tri.move_to(np.array([BOARD_CX - 2.5, -1.55, 0]))
            tri.scale(0.72)
            ang_t = angle_mark(tri.get_vertices()[0], tri.get_vertices()[1],
                               tri.get_vertices()[2], radius=0.22,
                               color=CHALK_YELLOW)

            lab_locate = board_text("LOCATE", 18, CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX + 2.6, 2.18, 0]))
            locate_cards = VGroup(
                degree_card(r"\angle P = 75^\circ", CHALK_CYAN),
                degree_card(r"\angle R = 120^\circ", CHALK_PINK),
            ).arrange(DOWN, buff=0.22).move_to(
                np.array([BOARD_CX + 2.6, 1.32, 0]))
            # a miniature of the two rays meeting
            mv = np.array([BOARD_CX + 2.6, -1.55, 0])
            m_base = Line(mv + np.array([-0.75, -0.42, 0]),
                          mv + np.array([0.80, -0.42, 0]), color=CHALK_WHITE,
                          stroke_width=2.0)
            m_ray_a = Line(mv + np.array([-0.75, -0.42, 0]),
                           mv + np.array([0.55, 0.62, 0]), color=CHALK_CYAN,
                           stroke_width=2.4)
            m_ray_b = Line(mv + np.array([0.80, -0.42, 0]),
                           mv + np.array([-0.30, 0.70, 0]), color=CHALK_PINK,
                           stroke_width=2.4)
            m_dot = Dot(radius=0.08, color=CHALK_YELLOW).move_to(
                mv + np.array([0.13, 0.05, 0]))
            m_s = board_text("S", 15, CHALK_WHITE, "BOLD").move_to(
                mv + np.array([0.48, 0.32, 0]))
            flow = board_text("3 measurements → triangle, 2 angles → rays", 17,
                              CHALK_GREEN, "BOLD").move_to(
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

            self.play(FadeIn(lab_locate), run_time=0.35)
            self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.12)
                                    for c in locate_cards], lag_ratio=0.28),
                      run_time=0.9)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b2"))

            self.play(Create(m_base), Create(m_ray_a), Create(m_ray_b),
                      FadeIn(m_dot), FadeIn(m_s), run_time=0.9)
            self.play(FadeIn(flow, shift=UP * 0.1),
                      Circumscribe(m_dot, color=CHALK_YELLOW, stroke_width=2.4),
                      run_time=min(leftover(tracker, "b3"), 1.0))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: draw P Q and set out 100 degrees at Q ----------------------
    def beat4_build(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 2 — Build Triangle PQR by S.A.S", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            d = example_construction()
            P, Q, R, S = d["quad"]
            names = self.vertex_letters(
                (P, Q), ((-0.28, -0.10), (0.12, -0.30)))
            pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=4.2)
            lab_pq = board_text("4 cm", 15, CHALK_YELLOW, "BOLD").move_to(
                (P + Q) / 2 + DOWN * 0.32)
            prot = protractor(Q, color=CHALK_AMBER, radius=0.95)
            tick_deg = d["qr_deg"]
            tick_dot = Dot(radius=0.07, color=CHALK_YELLOW).move_to(
                np.array(Q, dtype=float) + 0.95 * unit(tick_deg))
            ang_q = angle_mark(Q, P, R, radius=0.55, color=CHALK_AMBER)
            ang_lab = board_text("100°", 15, CHALK_AMBER, "BOLD").move_to(
                np.array(Q, dtype=float) + 1.30 * unit(
                    (d["qp_deg"] + tick_deg) / 2.0))
            ray_qr = self.ray_line(Q, tick_deg, dist(Q, R) * 1.10, CHALK_AMBER,
                                   3.2)
            note = self.column_note("R must lie\nsomewhere on this ray.", -0.75)
            card_pq = self.column_card(measure_card(r"PQ=4\text{ cm}", CHALK_YELLOW), 1.35)
            card_q = self.column_card(degree_card(r"\angle Q = 100^\circ", CHALK_AMBER), 0.55)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.wait(leftover(tracker, "b0"))

            self.play(Create(pq), FadeIn(names), FadeIn(lab_pq), FadeIn(card_pq),
                      run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b1"))

            # the protractor is laid on the base, the 100 degree graduation
            # marked, and the ray drawn through it
            self.play(FadeIn(prot), run_time=0.6)
            self.play(FadeIn(tick_dot, scale=0.5), run_time=0.35)
            self.play(FadeIn(ang_q), FadeIn(ang_lab), FadeIn(card_q),
                      run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeOut(prot), run_time=0.4)
            self.play(Create(ray_qr), FadeIn(note, shift=UP * 0.08),
                      run_time=min(leftover(tracker, "b3"), 1.0))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["ding"], gain=-13)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: measure 4.8 along the ray -- that point is R ---------------
    def beat5_triangle(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 2 — Complete the Triangle", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            d = example_construction()
            P, Q, R, S = d["quad"]
            names = self.vertex_letters(
                (P, Q, R), ((-0.28, -0.10), (0.12, -0.30), (0.50, -0.40)))
            pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=4.2)
            lab_pq = board_text("4 cm", 15, CHALK_YELLOW, "BOLD").move_to(
                (P + Q) / 2 + DOWN * 0.32)
            ray_qr = self.ray_line(Q, d["qr_deg"], dist(Q, R) * 1.10,
                                   CHALK_AMBER, 3.2)
            ang_q = angle_mark(Q, P, R, radius=0.55, color=CHALK_AMBER)
            ang_lab = board_text("100°", 15, CHALK_AMBER, "BOLD").move_to(
                np.array(Q, dtype=float) + 1.04 * unit(
                    (d["qp_deg"] + d["qr_deg"]) / 2.0))
            r_dot = Dot(radius=0.10, color=CHALK_YELLOW).move_to(R)
            qr = Line(Q, R, color=CHALK_YELLOW, stroke_width=4.2)
            lab_qr = side_label(Q, R, P, "4.8 cm", CHALK_YELLOW, 15, 0.20)
            pr = DashedLine(P, R, color=CHALK_WHITE, stroke_width=2.0,
                            dash_length=0.14)
            tri = Polygon(P, Q, R, color=CHALK_CYAN, stroke_width=2.6,
                          fill_color=CHALK_CYAN, fill_opacity=0.16)
            card_qr = self.column_card(measure_card(r"QR=4.8\text{ cm}", CHALK_YELLOW),
                                       1.35)
            card_q = self.column_card(degree_card(r"\angle Q = 100^\circ", CHALK_AMBER), 0.55)
            note = self.column_note("Triangle P Q R is fixed\nby S.A.S.", -0.75)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(Create(pq), FadeIn(names), FadeIn(lab_pq), FadeIn(ang_q),
                      FadeIn(ang_lab), FadeIn(ray_qr), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            # the compasses carry the 4.8 cm from the card to the ray
            self.compass_on(Q, R, dist(Q, R), 11, CHALK_GREEN,
                            hinge_dir=(1.0, -1.0, 0.0), leg_ratio=0.55)
            self.sweep_compass(tracker, "b1", 11)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(FadeIn(r_dot, scale=0.5),
                      Indicate(r_dot, color=CHALK_YELLOW, scale_factor=1.9),
                      run_time=min(leftover(tracker, "b2"), 0.8))
            self.play(Create(qr), FadeIn(lab_qr), FadeIn(card_qr),
                      run_time=min(leftover(tracker, "b2"), 0.9))
            self.play(FadeIn(card_q), run_time=0.3)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(Create(pr), FadeIn(tri), run_time=min(
                leftover(tracker, "b3"), 0.9))
            self.play(FadeIn(note, shift=UP * 0.08),
                      Flash(tri, color=CHALK_CYAN, flash_radius=0.7),
                      run_time=0.8)
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: the 75 degree angle at P gives one ray ---------------------
    def beat6_first_ray(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 3 — Set Out the Angle at P", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            d = example_construction()
            P, Q, R, S = d["quad"]
            names = self.vertex_letters(
                (P, Q, R), ((-0.28, -0.10), (0.12, -0.30), (0.50, -0.40)))
            pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=4.2)
            qr = Line(Q, R, color=CHALK_YELLOW, stroke_width=4.2)
            tri = Polygon(P, Q, R, color=CHALK_CYAN, stroke_width=2.4,
                          fill_color=CHALK_CYAN, fill_opacity=0.14)
            ang_q = angle_mark(Q, P, R, radius=0.55, color=CHALK_AMBER)
            ang_lab_q = board_text("100°", 15, CHALK_AMBER, "BOLD").move_to(
                np.array(Q, dtype=float) + 1.30 * unit(
                    (d["qp_deg"] + d["qr_deg"]) / 2.0))
            card_p = self.column_card(degree_card(r"\angle P = 75^\circ", CHALK_YELLOW),
                                      1.55)
            note = self.column_note("S could be somewhere\non this ray.", -0.30)
            inset = self.bisect_inset(np.array([2.35, -1.85, 0]), scale=0.92)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(tri), FadeIn(names), Create(pq), Create(qr),
                      FadeIn(ang_q), FadeIn(ang_lab_q), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            # the arm swings from P Q round to 75 degrees, the arc growing under
            # it: the angle is set out, not guessed
            self.setout_arm(P, d["pq_deg"], d["ps_deg"], dist(P, S) * 0.62,
                            0.80, CHALK_YELLOW)
            self.play(self.arm_sweep.animate.set_value(1.0), run_time=min(
                leftover(tracker, "b1"), 1.6))
            ang_p = board_text("75°", 15, CHALK_YELLOW, "BOLD").move_to(
                np.array(P, dtype=float) + 1.15 * unit(
                    d["ps_deg"] + 35.0))
            self.play(FadeIn(ang_p), FadeIn(card_p),
                      run_time=min(leftover(tracker, "b1"), 0.6))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            ray_p = self.ray_line(P, d["ps_deg"], dist(P, S) * 1.06, CHALK_CYAN,
                                  3.2)
            self.play(Transform(self.arm, ray_p), FadeIn(note, shift=UP * 0.08),
                      run_time=min(leftover(tracker, "b2"), 1.0))
            self.play(FadeOut(self.arm_arc), run_time=0.3)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["ding"], gain=-13)

            # a dot that can sit anywhere on the ray: an angle gives a
            # direction, not a distance
            walker = Dot(radius=0.09, color=CHALK_YELLOW).move_to(
                ray_point(P, d["ps_deg"], dist(P, S) * 0.30))
            self.play(FadeIn(walker), run_time=0.3)
            self.play(walker.animate.move_to(
                ray_point(P, d["ps_deg"], dist(P, S) * 1.02)),
                run_time=min(leftover(tracker, "b3"), 1.8))
            self.play(FadeOut(walker), run_time=0.3)
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(inset, shift=UP * 0.08), run_time=0.7)
            self.wait(leftover(tracker, "b4"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: the 120 degree angle at R, and the two rays meet -----------
    def beat7_second_ray(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 4 — The Angle at R Finds S", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            d = example_construction()
            P, Q, R, S = d["quad"]
            names = self.vertex_letters(
                (P, Q, R), ((-0.28, -0.10), (0.12, -0.30), (0.50, -0.40)))
            pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=4.2)
            qr = Line(Q, R, color=CHALK_YELLOW, stroke_width=4.2)
            tri = Polygon(P, Q, R, color=CHALK_CYAN, stroke_width=2.4,
                          fill_color=CHALK_CYAN, fill_opacity=0.14)
            ray_p = self.ray_line(P, d["ps_deg"], dist(P, S) * 1.06, CHALK_CYAN,
                                  3.2)
            ang_p = board_text("75°", 15, CHALK_YELLOW, "BOLD").move_to(
                np.array(P, dtype=float) + 1.15 * unit(
                    d["ps_deg"] + 35.0))
            card_r = self.column_card(degree_card(r"\angle R = 120^\circ", CHALK_PINK), 1.55)

            # the standard construction of 120 degrees: an arc about R, then the
            # same opening stepped round twice.  The two steps are 60 degrees
            # each, and the sign follows the interior of the angle: the chord of
            # a 60 degree step is exactly the compass opening, so the arcs of the
            # steps really do meet on the base arc.
            r_len = 1.05
            signed = ((d["rs_deg"] - d["rq_deg"] + 180.0) % 360.0) - 180.0
            step = 60.0 if signed > 0 else -60.0
            a1 = ray_point(R, d["rq_deg"], r_len)
            a2 = ray_point(R, d["rq_deg"] + step, r_len)
            a3 = ray_point(R, d["rq_deg"] + 2 * step, r_len)
            # the base arc sweeps from a3 round to a1 and passes through a2
            mid = a2
            dots = VGroup(*[Dot(radius=0.07, color=CHALK_PINK).move_to(p)
                            for p in (a1, a2, a3)])
            chord1 = Line(a1, a2, color=CHALK_PINK, stroke_width=2.0)
            chord2 = Line(a2, a3, color=CHALK_PINK, stroke_width=2.0)
            ray_r = self.ray_line(R, d["rs_deg"], dist(R, S) * 1.06, CHALK_PINK,
                                  3.2)
            s_dot = Dot(radius=0.11, color=CHALK_YELLOW).move_to(S)
            s_name = board_text("S", 17, CHALK_WHITE, "BOLD").move_to(
                S + np.array([-0.10, 0.30, 0]))
            note = self.column_note("The two rays cross\nat exactly one point.",
                                    -0.35)
            agree = board_text("Two directions agree at one point.", 17, CHALK_GREEN,
                               "BOLD").move_to(np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(tri), FadeIn(names), Create(pq), Create(qr),
                      Create(ray_p), FadeIn(ang_p), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            # the base arc, then the same opening stepped round twice: the
            # chord of each 60 degree step is exactly the opening, so the arcs
            # of the steps really do land on the base arc
            self.compass_on(R, mid, r_len, 60, CHALK_PINK,
                            hinge_dir=(1.0, 0.6, 0.0), leg_ratio=0.52)
            self.play(self.sweep.animate.set_value(120), run_time=min(
                leftover(tracker, "b1") * 0.42, 1.7))
            self.play(FadeIn(dots[0], scale=0.5), run_time=0.25)
            first = self.tool
            self.compass_on(a1, a2, r_len, 12, CHALK_PINK,
                            hinge_dir=(-1.0, -0.4, 0.0), leg_ratio=0.6)
            self.play(self.sweep.animate.set_value(24), run_time=0.75)
            self.play(FadeIn(dots[1], scale=0.5), FadeIn(chord1), run_time=0.3)
            self.compass_on(a2, a3, r_len, 12, CHALK_PINK,
                            hinge_dir=(1.0, 0.4, 0.0), leg_ratio=0.6)
            self.play(self.sweep.animate.set_value(24), run_time=0.75)
            self.play(FadeIn(dots[2], scale=0.5), FadeIn(chord2),
                      FadeOut(first), run_time=0.4)
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.wait(leftover(tracker, "b1"))

            # the ray through the 120 degree mark
            self.play(FadeIn(card_r), run_time=0.3)
            self.play(Create(ray_r), run_time=min(leftover(tracker, "b2"), 0.9))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeIn(s_dot, scale=0.5), FadeIn(s_name),
                      Indicate(s_dot, color=CHALK_YELLOW, scale_factor=2.1),
                      run_time=min(leftover(tracker, "b3"), 1.0))
            self.play(FadeIn(note, shift=UP * 0.08), run_time=0.5)
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeOut(VGroup(dots, chord1, chord2)),
                      FadeIn(agree, shift=UP * 0.1),
                      Circumscribe(s_dot, color=CHALK_GREEN, stroke_width=2.6),
                      run_time=min(leftover(tracker, "b4"), 1.0))
            self.wait(leftover(tracker, "b4"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: complete, verify, generalise -------------------------------
    def beat8_complete(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("Required Quadrilateral PQRS", 21,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            d = example_construction()
            P, Q, R, S = d["quad"]
            names = self.vertex_letters(
                (P, Q, R, S), ((-0.28, -0.10), (0.12, -0.30), (0.50, -0.40),
                               (-0.14, 0.34)))
            pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=4.0)
            qr = Line(Q, R, color=CHALK_YELLOW, stroke_width=4.0)
            ps = Line(P, S, color=CHALK_GREEN, stroke_width=4.2)
            rs = Line(R, S, color=CHALK_GREEN, stroke_width=4.2)
            ray_p = self.ray_line(P, d["ps_deg"], dist(P, S) * 1.06, CHALK_CYAN,
                                  2.4)
            ray_r = self.ray_line(R, d["rs_deg"], dist(R, S) * 1.06, CHALK_PINK,
                                  2.4)
            quad = Polygon(P, Q, R, S, color=CHALK_CYAN, stroke_width=2.4,
                           fill_color=CHALK_CYAN, fill_opacity=0.10)
            ang_p = angle_mark(P, Q, S, radius=0.62, color=CHALK_YELLOW,
                               label="75°")
            ang_q = angle_mark(Q, P, R, radius=0.55, color=CHALK_AMBER,
                               label="100°")
            ang_r = angle_mark(R, Q, S, radius=0.62, color=CHALK_PINK,
                               label="120°")
            checks = VGroup(
                check_row(r"PQ=4\text{ cm}", CHALK_GREEN, 15),
                check_row(r"QR=4.8\text{ cm}", CHALK_GREEN, 15),
                check_row(r"75^\circ", CHALK_YELLOW, 15),
                check_row(r"100^\circ", CHALK_AMBER, 15),
                check_row(r"120^\circ", CHALK_PINK, 15),
            ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(
                np.array([3.05, 0.80, 0]))
            steps = VGroup(
                combo_card("1. SKETCH", "2 adjacent sides + 3 angles",
                           CHALK_CYAN),
                combo_card("2. SAS TRIANGLE", "the two sides and angle Q",
                           CHALK_GREEN),
                combo_card("3. TWO ANGLE RAYS", "from P and from R",
                           CHALK_PINK),
                combo_card("4. INTERSECT", "their meeting is the 4th vertex",
                           CHALK_YELLOW),
            ).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to(
                np.array([2.62, 0.35, 0]))
            flow = board_text("Sketch → SAS → Rays → Intersection", 17,
                              CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(quad), FadeIn(names), Create(pq), Create(qr),
                      FadeIn(ray_p), FadeIn(ray_r), run_time=0.8)
            self.play(Create(ps), Create(rs), run_time=min(
                leftover(tracker, "b0"), 1.0))
            self.play(FadeIn(ang_p), FadeIn(ang_q), FadeIn(ang_r),
                      run_time=min(leftover(tracker, "b0"), 1.0))
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1)
                                    for c in checks], lag_ratio=0.20),
                      run_time=min(leftover(tracker, "b1"), 1.6))
            self.wait(leftover(tracker, "b1"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeOut(checks), FadeOut(ang_p), FadeOut(ang_q), FadeOut(ang_r),
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

    # -- Scene 9: student challenge ------------------------------------------
    def beat9_challenge(self) -> None:
        with self.voiceover(text=NARRATION["scene9_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", 30, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, 2.62, 0]))
            tag = board_text("Quadrilateral A B C D", 15, CHALK_WHITE, "BOLD"
                             ).move_to(np.array([BOARD_CX, 2.24, 0]))
            d = practice_construction()
            A, B, C, D = d["quad"]
            names = self.vertex_letters(
                (A, B, C, D), ((-0.28, -0.10), (0.12, -0.30), (0.50, -0.40),
                               (-0.34, 0.06)), letters="ABCD")
            rough = Polygon(A, B, C, D, color=CHALK_WHITE, stroke_width=2.4,
                            fill_color=CHALK_WHITE, fill_opacity=0.06)
            ab = Line(A, B, color=CHALK_YELLOW, stroke_width=3.4)
            bc = Line(B, C, color=CHALK_YELLOW, stroke_width=3.4)
            cards = VGroup(
                measure_card(r"AB=5\text{ cm}", CHALK_CYAN, 15),
                measure_card(r"BC=4\text{ cm}", CHALK_CYAN, 15),
                degree_card(r"\angle A = 70^\circ", CHALK_YELLOW, 15),
                degree_card(r"\angle B = 110^\circ", CHALK_AMBER, 15),
                degree_card(r"\angle C = 120^\circ", CHALK_PINK, 15),
            ).arrange(DOWN, buff=0.16).move_to(np.array([3.05, 0.75, 0]))
            ask = board_text("Which three measurements should you use "
                             "first?", 16, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX + 0.80, -2.62, 0]))
            prompt = board_text("What is their included angle?", 16,
                                CHALK_YELLOW, "BOLD").move_to(
                np.array([3.05, -1.35, 0]))
            pause = board_text("Pause and decide.", 17, CHALK_YELLOW, "BOLD"
                               ).move_to(np.array([3.05, -2.05, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(tag), run_time=0.4)
            self.play(FadeIn(rough), FadeIn(names), run_time=0.7)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.10)
                                    for c in cards], lag_ratio=0.16),
                      run_time=min(leftover(tracker, "b1"), 1.6))
            self.play(Create(ab), Create(bc), run_time=min(
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
                              "ask": ask, "pause": pause, "ab": ab, "bc": bc,
                              "prompt": prompt, "points": (A, B, C, D),
                              "data": d}
            self._capture_srt(tracker)

        play_challenge_countdown(self, seconds=4, sfx=self.sfx,
                                 position=np.array([BOARD_CX, BOARD_CY, 0]))

        with self.voiceover(text=NARRATION["scene9_reveal"]) as tracker:
            ch = self.challenge
            A, B, C, D = ch["points"]
            d = ch["data"]
            names = ch["names"]

            # the question and the pause prompt have done their job
            self.play(FadeOut(ch["pause"]), FadeOut(ch["ask"]),
                      FadeOut(ch["prompt"]), run_time=0.4)
            self.wait(leftover(tracker, "b0"))

            tri = Polygon(A, B, C, color=CHALK_GREEN, stroke_width=3.0,
                          fill_color=CHALK_GREEN, fill_opacity=0.14)
            badge = board_text("First triangle: A B C", 17, CHALK_GREEN,
                               "BOLD").move_to(np.array([3.05, -1.55, 0]))
            badge2 = board_text("built by S.A.S", 15, CHALK_GREEN, "BOLD"
                                ).move_to(np.array([3.05, -1.93, 0]))
            self.play(Create(tri),
                      Indicate(ch["cards"][3], color=CHALK_AMBER,
                               scale_factor=1.12),
                      Circumscribe(tri, color=CHALK_GREEN, stroke_width=2.6,
                                   time_width=0.6),
                      run_time=min(leftover(tracker, "b1"), 1.2))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            ray_a = self.ray_line(A, d["ps_deg"], dist(A, D) * 1.02, CHALK_CYAN,
                                  3.0)
            ray_c = self.ray_line(C, d["rs_deg"], dist(C, D) * 1.08, CHALK_PINK,
                                  3.0)
            d_dot = Dot(radius=0.10, color=CHALK_YELLOW).move_to(D)
            self.play(FadeIn(badge, shift=UP * 0.1), FadeIn(badge2),
                      run_time=0.5)
            self.play(Create(ray_a), Create(ray_c), run_time=min(
                leftover(tracker, "b2"), 1.4))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b2"))

            quad = Polygon(A, B, C, D, color=CHALK_CYAN, stroke_width=2.4,
                           fill_color=CHALK_CYAN, fill_opacity=0.12)
            built = board_text("S.A.S builds. Two angles locate.", 16,
                               CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))
            self.play(FadeIn(d_dot, scale=0.5), FadeIn(quad),
                      FadeIn(built, shift=UP * 0.08),
                      Indicate(d_dot, color=CHALK_YELLOW, scale_factor=2.1),
                      Circumscribe(names[3], color=CHALK_YELLOW,
                                   fade_out=True),
                      run_time=min(leftover(tracker, "b3"), 1.0))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap -----------------------------------------------------
    def beat10_recap(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("Two Sides and Three Angles", 22, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            d = example_construction(
                centre=np.array([BOARD_CX - 3.05, 0.35, 0]), scale=0.36)
            P, Q, R, S = d["quad"]
            names = self.vertex_letters(
                (P, Q, R, S), ((-0.24, -0.09), (0.10, -0.26), (0.34, -0.22),
                               (-0.14, 0.30)), size=15)
            pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=3.4)
            qr = Line(Q, R, color=CHALK_YELLOW, stroke_width=3.4)
            tri = Polygon(P, Q, R, color=CHALK_YELLOW, stroke_width=3.0,
                          fill_color=CHALK_YELLOW, fill_opacity=0.16)
            ray_p = self.ray_line(P, d["ps_deg"], dist(P, S) * 1.06, CHALK_CYAN,
                                  2.6)
            ray_r = self.ray_line(R, d["rs_deg"], dist(R, S) * 1.06, CHALK_PINK,
                                  2.6)
            quad = Polygon(P, Q, R, S, color=CHALK_CYAN, stroke_width=2.2,
                           fill_color=CHALK_CYAN, fill_opacity=0.10)
            ang_q = angle_mark(Q, P, R, radius=0.36, color=CHALK_AMBER)
            s_dot = Dot(radius=0.08, color=CHALK_YELLOW).move_to(S)

            rows = VGroup(
                summary_row(1, "Two adjacent sides + the angle:",
                            r"\triangle PQR", CHALK_YELLOW),
                summary_row(2, "The other two angles:",
                            r"rays", CHALK_CYAN),
                summary_row(3, "Their crossing:", r"S", CHALK_GREEN),
            ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX + 1.6, 1.20, 0]))
            final = board_text("Side–Angle–Side builds the triangle.", 17,
                               CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -1.90, 0]))
            take = board_text("Angle–Angle locates the fourth vertex.", 16,
                              CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.45, 0]))
            acr = board_text("S.A.S.A.A", 18, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX - 3.05, -1.90, 0]))
            acr_box = SurroundingRectangle(acr, color=CHALK_GREEN, buff=0.14,
                                          corner_radius=0.1, stroke_width=2.4)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(quad), FadeIn(names), Create(tri), Create(pq),
                      Create(qr), FadeIn(ang_q), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.wait(leftover(tracker, "b0"))

            self.play(FadeIn(rows[0], shift=RIGHT * 0.12), run_time=0.5)
            self.play(Create(ray_p), Create(ray_r),
                      FadeIn(rows[1], shift=RIGHT * 0.12),
                      run_time=min(leftover(tracker, "b1"), 1.4))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b1"))

            self.play(FadeIn(s_dot, scale=0.5),
                      FadeIn(rows[2], shift=RIGHT * 0.12),
                      Indicate(s_dot, color=CHALK_YELLOW, scale_factor=2.0),
                      run_time=min(leftover(tracker, "b2"), 1.0))
            self.add_sound(self.sfx["success"], gain=-11)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeIn(final, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(take), FadeIn(acr), Create(acr_box),
                      Circumscribe(quad, color=CHALK_AMBER, stroke_width=3,
                                   time_width=0.5),
                      run_time=min(leftover(tracker, "b3"), 1.2))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b3"))

            summary = VGroup(quad, names, tri, pq, qr, ray_p, ray_r, ang_q,
                             s_dot, rows, final, take, acr, acr_box)
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

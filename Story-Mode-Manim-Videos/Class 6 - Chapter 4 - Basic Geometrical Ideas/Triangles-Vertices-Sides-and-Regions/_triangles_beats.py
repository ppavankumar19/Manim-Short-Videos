    # ================================================================ beats ==
    # Triangles (Class 6 Maths, Chapter 4, Storymode 05).
    #
    # SYNC RULE for every reveal: wait for the narration bookmark that ends the
    # phrase describing a thing, and only then bring it on.  Playing first and
    # waiting afterwards shows the picture a whole window early, which reads as
    # broken sync.
    #
    # Layout rules, so the audits stay clean:
    #   * the heading sits on the board's own heading line (2.72) and its
    #     sub-heading at 2.16, the closing banner at -1.15 and the closing strip
    #     at -1.80 -- nothing at all below CAPTION_SAFE_Y = -2.00;
    #   * the persistent triangle A-B-C is fixed (TRI_A / TRI_B / TRI_C) so every
    #     scene draws exactly the same figure, and the three vertex letters are
    #     offset outward so no letter sits on a side;
    #   * the figure is the diagram block and stays centred on BOARD_CX, and the
    #     right-hand column (COL_L, left-aligned, capped at COL_W) carries
    #     whatever that scene is naming as its deliberate side label column;
    #   * the challenge uses the series' shared 10-second THINK clock, dead
    #     centre of the board, and the four question cards sit in the four
    #     corners so the badge never covers one.

    def closing(self, tracker, mob=None, color=CHALK_YELLOW, run_time=None):
        """Consume the tail of the narration window on the last reveal."""
        budget = rt(tracker.get_remaining_duration()) if run_time is None \
            else run_time
        if mob is None:
            self.wait(max(budget, 0.0))
        else:
            self.play(Indicate(mob, color=color, scale_factor=1.03),
                      run_time=max(budget, MIN_RT))

    def figure(self, scale=1.0, cx=None, cy=None, fill_op=0.14,
               side_color=CHALK_GREEN, letters="ABC", dot_size=MARK_SIZE):
        """The persistent triangle, drawn as three thick chalk sides with a
        tinted interior and a solid dot plus an offset letter at each corner.

        Every corner letter is placed by the one rule (`corner_label_dx`: the
        same distance out along the corner's own outward bisector), so A, B and
        C look the same in every scene and none of them can sit on a side.
        """
        pts = tri_pts(scale, TRI_CEN[0] if cx is None else cx,
                      TRI_CEN[1] if cy is None else cy)
        a, b, c = pts
        grp = VGroup()
        fill = VGroup()
        if fill_op:
            fill = tri_fill(pts, fill_op)
            grp.add(fill)
        sides = VGroup(tri_side(a, b, side_color), tri_side(b, c, side_color),
                       tri_side(c, a, side_color))
        grp.add(sides)
        verts = VGroup()
        for i, (p, letter) in enumerate(zip(pts, letters)):
            if letter:
                dx, dy = corner_label_dx(pts, i)
                verts.add(dot_point(letter, p[0], p[1], CHALK_PINK,
                                    size=dot_size, label_dx=(dx, dy)))
        grp.add(verts)
        grp.fill = fill
        grp.sides = sides
        grp.verts = verts
        grp.points = pts
        return grp

    def col_item(self, head, note, color, y, x=COL_L, width=COL_W, height=0.92,
                 head_size=15, note_size=12):
        """One row of the right-hand column: a keyword and its note inside one
        card, spaced so no two words on the board come closer than 0.22 units.

        The card is capped to `COL_W` and left-aligned on `COL_L`, so the column
        never reaches across the figure's corner letters nor off the green board.
        """
        h = board_text(head, head_size, color, "BOLD")
        n = board_text(note, note_size, CHALK_WHITE, "BOLD")
        box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                               stroke_color=color, stroke_width=1.8,
                               fill_color=PANEL_FILL, fill_opacity=0.55)
        h.move_to(box.get_center() + UP * 0.26)
        n.move_to(box.get_center() + DOWN * 0.26)
        grp = VGroup(box, h, n)
        grp.box = box
        grp.head = h
        grp.note = n
        return at_left(grp, x, y)

    def q_card(self, title, pict, color=CHALK_CYAN, width=3.00, pad=0.12,
               title_size=13, buff=0.28):
        """One 'your turn' card: a prompt above its small diagram."""
        head = board_text(title, title_size, color, "BOLD")
        content = VGroup(head, pict).arrange(DOWN, buff=buff)
        box = RoundedRectangle(corner_radius=0.10, width=width,
                               height=content.height + 2 * pad,
                               stroke_color=color, stroke_width=1.9,
                               fill_color=PANEL_FILL, fill_opacity=0.55)
        content.move_to(box.get_center())
        return VGroup(box, content)

    def answer_row(self, tag, headline, note, color, width=8.60, height=0.62,
                   pad=0.34, buff=0.36):
        """One revealed answer: its letter, the result and a short note.

        The row is laid out in FIXED COLUMNS rather than centred in its box, so
        the tag column and the text column are the same vertical line in every
        row (centring put each letter at a different x).  The box itself stays
        centred on BOARD_CX.  The same helper draws the recap list.
        """
        lab = board_text(tag, 17, color, "BOLD")
        name = board_text(headline, 17, color, "BOLD")
        txt = board_text(note, 15, CHALK_WHITE, "BOLD")
        row = VGroup(lab, name, txt).arrange(RIGHT, buff=buff)
        box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                               stroke_color=color, stroke_width=1.8,
                               fill_color=PANEL_FILL, fill_opacity=0.6)
        row.move_to(np.array([box.get_left()[0] + pad + row.width / 2.0,
                              box.get_center()[1], 0.0]))
        return VGroup(box, row)

    def mini_triangle(self, letters="PQR", color=CHALK_GREEN, arc=False,
                      points=()):
        """A small triangle for the challenge cards (centred on the origin).

        It is the SAME shape the lesson builds (A->P, B->Q, C->R), scaled to a
        card-sized thumbnail, and its corner letters use the same
        outward-bisector rule as the big figure, so no letter ever sits on a
        side and no dot ever lands inside a letter.  Pass `letters=""` for the
        card that carries the region points, so X, Y and Z have the whole
        thumbnail to themselves.
        """
        pts = [np.array([(x - TRI_CEN[0]) * 0.34, (y - TRI_CEN[1]) * 0.34, 0.0])
               for x, y in (TRI_A, TRI_B, TRI_C)]
        p, q, r = pts
        parts = [Polygon(p.copy(), q.copy(), r.copy(), stroke_color=color,
                         stroke_width=2.6, fill_color=CHALK_CYAN,
                         fill_opacity=0.16)]
        for i, (pt, letter) in enumerate(zip(pts, letters)):
            if letter:
                dx, dy = corner_label_dx(pts, i, 0.22)
                parts.append(dot_point(letter, pt[0], pt[1], CHALK_PINK,
                                       size=12, label_dx=(dx, dy), r=0.045))
        if arc:
            parts.append(corner_arc(q, p, r, 0.15, CHALK_AMBER, 2.0))
        # X inside, Y exactly on the base, Z out beyond side AB -- the same
        # three regions the lesson names, drawn on the same thumbnail shape.
        spots = {"in": ((-0.14, -0.14), (0.22, 0.0)),
                 "on": ((0.30, -0.298), (0.02, -0.21)),
                 "out": ((-0.549, 0.154), (-0.20, 0.06))}
        for name, kind in points:
            (px, py), (dx, dy) = spots[kind]
            col = {"in": CHALK_CYAN, "on": CHALK_AMBER,
                   "out": CHALK_PINK}[kind]
            parts.append(dot_point(name, px, py, col, size=10,
                                   label_dx=(dx, dy), r=0.045))
        return VGroup(*parts)

    # -- Scene 0: title ------------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = at(board_text("Triangles Uncovered", 26, CHALK_PINK,
                                  "BOLD"), BOARD_CX, 1.98)
            sub = at(board_text("Vertices · Sides · Angles · Triangular Region",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, 1.42)

            # the figure is the diagram block: centred on the board axis, with
            # the four counts left-aligned in its side label column at the right
            fig = self.figure(scale=0.72, cx=BOARD_CX, cy=-0.32, fill_op=0.16)
            c1 = at_left(chip("3 SIDES", CHALK_GREEN, size=14), COL_L, 0.88)
            c2 = at_left(chip("3 VERTICES", CHALK_PINK, size=14), COL_L, 0.16)
            c3 = at_left(chip("3 ANGLES", CHALK_AMBER, size=14), COL_L, -0.56)
            c4 = at_left(chip("interior · boundary · exterior", CHALK_CYAN,
                              size=12, width=COL_W), COL_L, -1.28)

            strip = at(board_text("Three sides, three vertices, three angles.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(title, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(fig.fill), Create(fig.sides), FadeIn(fig.verts),
                      run_time=0.85)
            self.play(FadeIn(c1, scale=0.9), FadeIn(c2, scale=0.9),
                      FadeIn(c3, scale=0.9), run_time=0.55)
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(c4, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.closing(tracker, c4)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: how many sticks close a figure -----------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("How Many Sticks Close a Figure?", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("One stick, two sticks, three sticks.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            a, b, c = tri_pts(0.86, BOARD_CX, -0.22)
            s1 = match_stick(a, b)
            s2 = match_stick(b, c)
            s3 = match_stick(c, a)
            fill = tri_fill((a, b, c), 0.16)

            k1 = at_left(chip("1 STICK · OPEN", CHALK_RED, size=14), COL_L, 1.15)
            k2 = at_left(chip("2 STICKS · OPEN", CHALK_RED, size=14), COL_L, 0.45)
            k3 = at_left(chip("3 STICKS · CLOSED", CHALK_GREEN, size=14), COL_L,
                         -0.25)

            banner = at(board_text("3 IS THE LEAST NUMBER OF SEGMENTS", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Three line segments are enough to close the "
                                  "figure.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(s1.line), FadeIn(s1.head), FadeIn(k1, scale=0.9),
                      run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(s2.line), FadeIn(s2.head), FadeIn(k2, scale=0.9),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Create(s3.line), FadeIn(s3.head), FadeIn(fill),
                      FadeIn(k3, scale=0.9), run_time=0.70)
            self.add_sound(self.sfx["success"], gain=-12)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: what is a triangle -----------------------------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("What Is a Triangle?", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Simple · closed · three line segments.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(scale=0.72, cx=BOARD_CX, cy=0.18, fill_op=0.14)

            i1 = self.col_item("SIMPLE", "the sides do not cross", CHALK_GREEN,
                               0.80)
            i2 = self.col_item("CLOSED", "the ends join up", CHALK_CYAN, -0.40)

            banner = at(board_text("3 LINE SEGMENTS = TRIANGLE", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("A simple closed figure formed by three line "
                                  "segments.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(fig.fill), Create(fig.sides), FadeIn(fig.verts),
                      run_time=0.70)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(i1, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(i2, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: the three sides --------------------------------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Three Sides", 20, CHALK_AMBER, "BOLD"),
                         BOARD_CX, ROW_Y)
            sub = at(board_text("The three line segments of the figure.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill_op=0.10)
            a, b, c = fig.points
            l_ab = at(board_text("AB", 17, CHALK_GREEN, "BOLD"),
                      *side_label_pos(fig.points, 0))
            l_bc = at(board_text("BC", 17, CHALK_GREEN, "BOLD"),
                      *side_label_pos(fig.points, 1))
            l_ca = at(board_text("CA", 17, CHALK_GREEN, "BOLD"),
                      *side_label_pos(fig.points, 2))

            k1 = at_left(chip("SIDE 1 · AB", CHALK_GREEN, size=14), COL_L,
                         COL_ROWS[0])
            k2 = at_left(chip("SIDE 2 · BC", CHALK_GREEN, size=14), COL_L,
                         COL_ROWS[1])
            k3 = at_left(chip("SIDE 3 · CA", CHALK_GREEN, size=14), COL_L,
                         COL_ROWS[2])
            note = at_left(board_text("the sides form the boundary", 12,
                                      CHALK_WHITE, "BOLD"), COL_L, COL_NOTE_Y)

            strip = at(board_text("The three sides together form the boundary.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(fig.fill), Create(fig.sides), FadeIn(fig.verts),
                      run_time=0.75)

            self.wait(leftover(tracker, "b0"))
            self.play(Indicate(fig.sides[0], color=CHALK_YELLOW, scale_factor=1.02),
                      FadeIn(l_ab, scale=0.9), FadeIn(k1, scale=0.9),
                      run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Indicate(fig.sides[1], color=CHALK_YELLOW, scale_factor=1.02),
                      FadeIn(l_bc, scale=0.9), FadeIn(k2, scale=0.9),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Indicate(fig.sides[2], color=CHALK_YELLOW, scale_factor=1.02),
                      FadeIn(l_ca, scale=0.9), FadeIn(k3, scale=0.9),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(Indicate(fig.sides, color=CHALK_GREEN, scale_factor=1.03),
                      FadeIn(note, shift=UP * 0.05),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: the three vertices -----------------------------------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Three Vertices", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The points where the sides meet.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill_op=0.10)
            k1 = at_left(chip("VERTEX A", CHALK_PINK, size=14), COL_L,
                         COL_ROWS[0])
            k2 = at_left(chip("VERTEX B", CHALK_PINK, size=14), COL_L,
                         COL_ROWS[1])
            k3 = at_left(chip("VERTEX C", CHALK_PINK, size=14), COL_L,
                         COL_ROWS[2])
            note = at_left(board_text("a corner, not a side", 12, CHALK_WHITE,
                                      "BOLD"), COL_L, COL_NOTE_Y)

            strip = at(board_text("A vertex is a corner of the triangle.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(fig.fill), Create(fig.sides), run_time=0.60)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(fig.verts[0], scale=0.85), FadeIn(k1, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(fig.verts[1], scale=0.85), FadeIn(k2, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(fig.verts[2], scale=0.85), FadeIn(k3, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(Indicate(fig.verts, color=CHALK_PINK, scale_factor=1.15),
                      FadeIn(note, shift=UP * 0.05),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: three vertices give three angles ---------------------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("Three Vertices, Three Angles", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Every vertex gives an angle.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill_op=0.10)
            a, b, c = fig.points
            arc_a = corner_arc(a, b, c, CORNER_R, CHALK_GREEN, 3.0)
            arc_b = corner_arc(b, a, c, CORNER_R, CHALK_CYAN, 3.0)
            arc_c = corner_arc(c, a, b, CORNER_R, CHALK_PINK, 3.0)

            def angle_row(pre, tex, color, y):
                p = board_text(pre, 15, color, "BOLD")
                m = chalk_math(tex, size=24, color=color)
                return at_left(VGroup(p, m).arrange(RIGHT, buff=0.26), COL_L, y)

            r1 = angle_row("at A", r"\angle BAC", CHALK_GREEN, 1.25)
            r2 = angle_row("at B", r"\angle ABC", CHALK_CYAN, 0.45)
            r3 = angle_row("at C", r"\angle ACB", CHALK_PINK, -0.35)
            note = at_left(board_text("the vertex is the middle letter", 12,
                                      CHALK_WHITE, "BOLD"), COL_L, -1.05)

            strip = at(board_text("Three vertices give three angles.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(fig.fill), Create(fig.sides), FadeIn(fig.verts),
                      run_time=0.70)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(arc_a), FadeIn(r1, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(arc_b), FadeIn(r2, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Create(arc_c), FadeIn(r3, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(Indicate(VGroup(arc_a, arc_b, arc_c), color=CHALK_YELLOW,
                               scale_factor=1.04),
                      FadeIn(note, shift=UP * 0.05),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: naming the triangle ----------------------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("Naming the Triangle", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("We use its three vertices.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill_op=0.14)
            name = at_left(chalk_math(r"\triangle ABC", size=38,
                                      color=CHALK_YELLOW), COL_L, 0.95)
            n1 = at_left(board_text("the vertices in order", 12, CHALK_WHITE,
                                    "BOLD"), COL_L, 0.20)
            n2 = at_left(board_text("BCA and CAB name it too", 12, CHALK_WHITE,
                                    "BOLD"), COL_L, -0.55)

            strip = at(board_text("Name a triangle by its three vertices, in "
                                  "order.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(fig.fill), Create(fig.sides), FadeIn(fig.verts),
                      run_time=0.75)

            self.wait(leftover(tracker, "b0"))
            self.play(Indicate(fig.verts, color=CHALK_PINK, scale_factor=1.12),
                      run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Indicate(fig.sides[0], color=CHALK_YELLOW, scale_factor=1.02),
                      run_time=0.24)
            self.play(Indicate(fig.sides[1], color=CHALK_YELLOW, scale_factor=1.02),
                      run_time=0.24)
            self.play(Indicate(fig.sides[2], color=CHALK_YELLOW, scale_factor=1.02),
                      run_time=0.24)
            self.play(FadeIn(name, scale=0.9), FadeIn(n1, shift=UP * 0.05),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(n2, shift=UP * 0.05),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: interior, boundary, exterior -------------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Interior, Boundary, Exterior", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A triangle divides the plane into three parts.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill_op=0.18)
            # P sits in the open interior, Q exactly ON the base (its letter
            # just below the base, in the air under the figure), and R outside
            # to the upper left, across side AB -- so the three points are far
            # apart and each one's region reads at a glance.  (The old cut put
            # them all in the right-hand half, where the column sits.)
            p_pt = dot_point("P", 0.30, 0.30, CHALK_CYAN, size=MARK_SIZE,
                             label_dx=(0.22, 0.16))
            q_pt = dot_point("Q", 0.60, -0.45, CHALK_AMBER, size=MARK_SIZE,
                             label_dx=(0.0, -0.31))
            r_pt = dot_point("R", -0.885, 0.727, CHALK_PINK, size=MARK_SIZE,
                             label_dx=(-0.24, 0.20))

            k1 = at_left(chip("P · INTERIOR", CHALK_CYAN, size=14), COL_L,
                         COL_ROWS[0])
            k2 = at_left(chip("Q · BOUNDARY", CHALK_AMBER, size=14), COL_L,
                         COL_ROWS[1])
            k3 = at_left(chip("R · EXTERIOR", CHALK_PINK, size=14), COL_L,
                         COL_ROWS[2])
            note = at_left(board_text("inside · on a side · outside", 12,
                                      CHALK_WHITE, "BOLD"), COL_L, COL_NOTE_Y)

            strip = at(board_text("Three parts of the plane: interior, boundary, "
                                  "exterior.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(fig.fill), Create(fig.sides), FadeIn(fig.verts),
                      run_time=0.70)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(p_pt, scale=0.85), FadeIn(k1, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(q_pt, scale=0.85), FadeIn(k2, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(r_pt, scale=0.85), FadeIn(k3, scale=0.9),
                      run_time=0.50)
            self.play(FadeIn(note, shift=UP * 0.05),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the triangular region --------------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Triangular Region", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The interior together with the boundary.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill_op=0.22)
            a, b, c = fig.points
            glow = VGroup(tri_side(a, b, CHALK_YELLOW, 7.5),
                          tri_side(b, c, CHALK_YELLOW, 7.5),
                          tri_side(c, a, CHALK_YELLOW, 7.5))

            k1 = at_left(chip("INTERIOR", CHALK_CYAN, size=14), COL_L, 1.15)
            k2 = at_left(chip("+ BOUNDARY", CHALK_GREEN, size=14), COL_L, 0.45)
            k3 = at_left(chip("= THE REGION", CHALK_YELLOW, size=14), COL_L,
                         -0.35)
            note = at_left(board_text("the region includes the sides", 12,
                                      CHALK_WHITE, "BOLD"), COL_L, -1.05)

            strip = at(board_text("The region is the interior plus the boundary.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(fig.sides), FadeIn(fig.verts), run_time=0.60)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(fig.fill), FadeIn(k1, scale=0.9), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(glow), FadeIn(k2, scale=0.9), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Indicate(VGroup(fig.fill, glow), color=CHALK_YELLOW,
                               scale_factor=1.03),
                      FadeIn(k3, scale=0.9), FadeIn(note, shift=UP * 0.05),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.65)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, k3)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 9: your turn (questions, the silent clock, then the answers) ---
    def beat_s9(self) -> None:
        with self.voiceover(text=NARRATION["s9q"]) as tracker:
            self.reset_board()

            heading = at(board_text("YOUR TURN", 26, CHALK_PINK, "BOLD"),
                         BOARD_CX, 2.78)
            sub = at(board_text("Four quick checks.", 16, CHALK_WHITE, "BOLD"),
                     BOARD_CX, 2.20)

            qa = at(self.q_card("name the sides",
                                self.mini_triangle("PQR", CHALK_GREEN),
                                CHALK_GREEN), -2.80, 0.92)
            qb = at(self.q_card("name the vertices",
                                self.mini_triangle("PQR", CHALK_CYAN),
                                CHALK_CYAN), 3.70, 0.92)
            qc = at(self.q_card("name the angle at Q",
                                self.mini_triangle("PQR", CHALK_AMBER, arc=True),
                                CHALK_AMBER), -2.80, -1.02)
            qd = at(self.q_card("X, Y, Z belong where?",
                                self.mini_triangle("", CHALK_PINK,
                                                   points=(("X", "in"),
                                                           ("Y", "on"),
                                                           ("Z", "out"))),
                                CHALK_PINK), 3.70, -1.02)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(qa, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(qb, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(qc, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(qd, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self._capture_srt(tracker)

        # The ten-second THINK pause is deliberately SILENT: the questions have
        # just been read, so the clock ticks alone, with no narration to sync
        # against.
        play_challenge_countdown(self, seconds=10, sfx=self.sfx,
                                 position=np.array([BOARD_CX, BOARD_CY, 0]))

        with self.voiceover(text=NARRATION["s9a"]) as tracker:
            self.wait(leftover(tracker, "b0"))
            self.play(FadeOut(qa), FadeOut(qb), FadeOut(qc), FadeOut(qd),
                      run_time=0.50)
            a1 = at(self.answer_row("A", "PQ · QR · RP",
                                    "the three line segments", CHALK_GREEN),
                    BOARD_CX, 1.62)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "P · Q · R", "the three corners",
                                    CHALK_CYAN), BOARD_CX, 0.82)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "angle PQR", "Q stays in the middle",
                                    CHALK_AMBER), BOARD_CX, 0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "X · Y · Z sorted",
                                    "interior · boundary · exterior",
                                    CHALK_PINK), BOARD_CX, -0.78)
            self.play(FadeIn(a4, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, a4)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap and the spoken thank-you ----------------------------
    def beat_s10(self) -> None:
        with self.voiceover(text=NARRATION["s10"]) as tracker:
            self.reset_board()

            heading = at(board_text("Build · Identify · Locate", 22, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)

            r1 = at(self.answer_row("1", "3 SIDES · 3 VERTICES · 3 ANGLES",
                                    "the parts of a triangle", CHALK_GREEN),
                    BOARD_CX, 1.48)
            r2 = at(self.answer_row("2", "THREE LINE SEGMENTS",
                                    "simple and closed", CHALK_CYAN),
                    BOARD_CX, 0.72)
            r3 = at(self.answer_row("3", "TRIANGULAR REGION",
                                    "interior together with the boundary",
                                    CHALK_YELLOW), BOARD_CX, -0.04)
            r4 = at(self.answer_row("4", "BUILD · IDENTIFY · LOCATE",
                                    "name it, then sort the points",
                                    CHALK_AMBER), BOARD_CX, -0.80)
            strip = at(board_text("Build it, identify its parts, then locate the "
                                  "points.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)
            thanks = at(board_text("Thank You for Watching!", 30, CHALK_WHITE,
                                   "BOLD"), BOARD_CX, 0.62)
            bye = at(board_text("See you in the next lesson :)", 22, CHALK_YELLOW,
                                "BOLD"), BOARD_CX, -0.32)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(r1, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(r2, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(r3, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(r4, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            # The list stays on the board through the whole closing sentence:
            # the strip is written on its own bookmark as the voice says "and
            # locate the points.", and only the bookmark in front of "Thank you
            # for watching," clears the board and brings in the card.  (The old
            # cut brought the strip on one bookmark early, with r4, and then
            # cleared everything on the next one, so the frame ran ahead of the
            # voice.)
            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeOut(heading), FadeOut(r1), FadeOut(r2), FadeOut(r3),
                      FadeOut(r4), FadeOut(strip), run_time=0.55)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.50)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            # 0.90 rather than 1.20: this piece's own audio runs the closing
            # sentence a little slower than the draft SRT assumes, and this
            # keeps every piece at 0.00 s stretch
            self.closing(tracker, thanks, run_time=0.90)
            self._capture_srt(tracker)

        self.wait(END_HOLD)

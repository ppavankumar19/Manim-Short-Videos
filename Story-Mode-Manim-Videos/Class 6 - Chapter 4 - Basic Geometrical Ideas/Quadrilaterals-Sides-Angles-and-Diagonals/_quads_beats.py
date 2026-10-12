    # ================================================================ beats ==
    # Quadrilaterals (Class 6 Maths, Chapter 4, Storymode 06).
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
    #   * the persistent quadrilateral A-B-C-D is fixed (QUAD_A .. QUAD_D) so
    #     every scene draws exactly the same figure, and the four vertex letters
    #     are offset outward so no letter sits on a side;
    #   * the figure occupies the left two thirds and the right-hand column
    #     (COL_L, left-aligned) carries whatever that scene is naming, so nothing
    #     has to be written across the boundary;
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
               side_color=CHALK_GREEN, letters="ABCD", dot_size=MARK_SIZE):
        """The persistent quadrilateral, drawn as four thick chalk sides with a
        tinted interior and a solid dot plus an offset letter at each corner.

        Every corner letter is placed by the one rule (`corner_label_dx`: the
        same distance out along the corner's own outward bisector), so A, B, C
        and D look the same in every scene and none of them can sit on a side.
        """
        pts = quad_pts(scale, QUAD_CEN[0] if cx is None else cx,
                       QUAD_CEN[1] if cy is None else cy)
        a, b, c, d = pts
        grp = VGroup()
        fill = VGroup()
        if fill_op:
            fill = quad_fill(pts, fill_op)
            grp.add(fill)
        sides = VGroup(quad_side(a, b, side_color), quad_side(b, c, side_color),
                       quad_side(c, d, side_color), quad_side(d, a, side_color))
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

        The card is capped to `COL_W` so the column never reaches across the
        figure's corner letters nor off the green board.
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

    def mini_quad(self, letters="PQRS", color=CHALK_GREEN, arc=None,
                  diags=False):
        """A small quadrilateral for the challenge cards (centred on the
        origin): four sides, a solid dot and an offset letter at each corner,
        optionally the angle mark at P or the two dashed diagonals.

        It is the SAME shape the lesson builds (A->P, B->Q, C->R, D->S),
        scaled to a card-sized thumbnail, and its letters use the same
        outward-bisector rule as the big figure, scaled with it, so no letter
        ever sits on a side and no dot ever lands inside a letter.
        """
        pts = [np.array([x * 0.34, y * 0.34, 0.0]) for x, y in QUAD_LOCAL]
        p, q, r, s = pts
        parts = [Polygon(*[pt.copy() for pt in pts],
                         stroke_color=color, stroke_width=2.6,
                         fill_color=CHALK_CYAN, fill_opacity=0.16)]
        for i, (pt, letter) in enumerate(zip(pts, letters)):
            if letter:
                dx, dy = corner_label_dx(pts, i, 0.22)
                parts.append(dot_point(letter, pt[0], pt[1], CHALK_PINK,
                                       size=12, label_dx=(dx, dy), r=0.045))
        if arc == "P":
            parts.append(corner_arc(p, q, s, 0.13, CHALK_AMBER, 2.0))
        if diags:
            parts.append(diag(p, r, CHALK_YELLOW, 2.0, dash=0.08))
            parts.append(diag(q, s, CHALK_PINK, 2.0, dash=0.08))
        return VGroup(*parts)

    # -- Scene 0: title ------------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = at(board_text("Exploring Quadrilaterals", 25, CHALK_PINK,
                                  "BOLD"), BOARD_CX, 2.06)
            sub = at(board_text("Sides · Vertices · Angles · Diagonals", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, 1.42)

            # the figure is the diagram block: centred on the board axis, with
            # the four counts in its side label column at the right
            fig = self.figure(scale=0.72, cx=BOARD_CX, cy=-0.25, fill_op=0.16)
            a, b, c, d = fig.points
            diag1 = diag(a, c)
            diag2 = diag(b, d)

            # the four counts, left-aligned in the figure's side label column
            c1 = at_left(chip("4 SIDES", CHALK_GREEN, size=14), COL_L, 0.88)
            c2 = at_left(chip("4 VERTICES", CHALK_PINK, size=14), COL_L, 0.16)
            c3 = at_left(chip("4 ANGLES", CHALK_AMBER, size=14), COL_L, -0.56)
            c4 = at_left(chip("2 DIAGONALS", CHALK_YELLOW, size=14), COL_L,
                         -1.28)

            strip = at(board_text("A simple closed polygon with four sides.",
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
            self.play(FadeIn(diag1), FadeIn(diag2), FadeIn(c4, scale=0.9),
                      run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.closing(tracker, c4)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: from a triangle to a quadrilateral -------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            # On-screen heading only -- the narration is untouched.  The old
            # "What Happens When We Add a Fourth Corner?" was 6.68 wide and ran
            # straight into the top-right "Mathematics" badge (badge x
            # [+3.79..+5.59] y [+2.82..+3.22], heading right edge +3.84, i.e.
            # the boxes actually overlapped).  This keeps the meaning on the
            # same heading line, size, colour and weight, and clears both
            # badges by more than a unit.
            heading = at(board_text("Adding a Fourth Corner", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A triangle grows one more side.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            a, b, c, d = quad_pts()
            t_ab = quad_side(a, b, CHALK_AMBER, 5.0)
            t_bc = quad_side(b, c, CHALK_AMBER, 5.0)
            t_ca = quad_side(c, a, CHALK_AMBER, 5.0)
            va = dot_point("A", a[0], a[1], CHALK_PINK, size=MARK_SIZE,
                           label_dx=corner_label_dx((a, b, c, d), 0))
            vb = dot_point("B", b[0], b[1], CHALK_PINK, size=MARK_SIZE,
                           label_dx=corner_label_dx((a, b, c, d), 1))
            vc = dot_point("C", c[0], c[1], CHALK_PINK, size=MARK_SIZE,
                           label_dx=corner_label_dx((a, b, c, d), 2))
            vd = dot_point("D", d[0], d[1], CHALK_PINK, size=MARK_SIZE,
                           label_dx=corner_label_dx((a, b, c, d), 3))
            s_cd = quad_side(c, d, CHALK_GREEN)
            s_da = quad_side(d, a, CHALK_GREEN)
            g_ab = quad_side(a, b, CHALK_GREEN)
            g_bc = quad_side(b, c, CHALK_GREEN)
            fill = quad_fill((a, b, c, d), 0.16)

            k1 = at_left(chip("3 SIDES · TRIANGLE", CHALK_AMBER, size=12),
                         COL_L, 0.85)
            k2 = at_left(chip("4 SIDES · QUADRILATERAL", CHALK_GREEN, size=12),
                         COL_L, 0.15)

            banner = at(board_text("THE THIRD SIDE OPENS IN TWO", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Adding a fourth corner gives a quadrilateral.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(t_ab), Create(t_bc), Create(t_ca), FadeIn(va),
                      FadeIn(vb), FadeIn(vc), run_time=0.75)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(k1, scale=0.9), run_time=0.40)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(vd, scale=0.85), run_time=0.45)
            self.play(Indicate(vd, color=CHALK_PINK, scale_factor=1.30),
                      run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeOut(t_ca), FadeOut(t_ab), FadeOut(t_bc),
                      Create(s_cd), Create(s_da), Create(g_ab), Create(g_bc),
                      FadeIn(fill), run_time=0.85)
            self.play(FadeIn(k2, scale=0.9),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-12)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: the definition, built segment by segment -------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("What Makes It a Quadrilateral?", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Simple · closed · four line segments.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            a, b, c, d = quad_pts()
            s_ab = quad_side(a, b)
            s_bc = quad_side(b, c)
            s_cd = quad_side(c, d)
            s_da = quad_side(d, a)
            fill = quad_fill((a, b, c, d), 0.16)
            va = dot_point("A", a[0], a[1], CHALK_PINK, size=MARK_SIZE,
                           label_dx=corner_label_dx((a, b, c, d), 0))
            vb = dot_point("B", b[0], b[1], CHALK_PINK, size=MARK_SIZE,
                           label_dx=corner_label_dx((a, b, c, d), 1))
            vc = dot_point("C", c[0], c[1], CHALK_PINK, size=MARK_SIZE,
                           label_dx=corner_label_dx((a, b, c, d), 2))
            vd = dot_point("D", d[0], d[1], CHALK_PINK, size=MARK_SIZE,
                           label_dx=corner_label_dx((a, b, c, d), 3))

            k1 = at_left(chip("SIDE 1 · AB", CHALK_GREEN, size=14), COL_L, 1.42)
            k2 = at_left(chip("SIDE 2 · BC", CHALK_GREEN, size=14), COL_L, 0.78)
            k3 = at_left(chip("SIDE 3 · CD", CHALK_GREEN, size=14), COL_L, 0.14)
            k4 = at_left(chip("SIDE 4 · DA", CHALK_GREEN, size=14), COL_L,
                         -0.50)

            banner = at(board_text("4 SEGMENTS = QUADRILATERAL", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Simple, closed, and made of four line "
                                  "segments.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(s_ab), FadeIn(va), FadeIn(vb), FadeIn(k1, scale=0.9),
                      run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(s_bc), FadeIn(k2, scale=0.9), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Create(s_cd), FadeIn(vc), FadeIn(k3, scale=0.9),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(Create(s_da), FadeIn(vd), FadeIn(fill),
                      FadeIn(k4, scale=0.9), run_time=0.70)
            self.add_sound(self.sfx["success"], gain=-12)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: the four sides and the four vertices -----------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Four Sides and the Four Vertices", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The boundary and its corners.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill_op=0.11)
            l_ab = at(board_text("AB", 17, CHALK_GREEN, "BOLD"),
                      *side_label_pos(fig.points, 0))
            l_bc = at(board_text("BC", 17, CHALK_GREEN, "BOLD"),
                      *side_label_pos(fig.points, 1))
            l_cd = at(board_text("CD", 17, CHALK_GREEN, "BOLD"),
                      *side_label_pos(fig.points, 2))
            l_da = at(board_text("DA", 17, CHALK_GREEN, "BOLD"),
                      *side_label_pos(fig.points, 3))

            k1 = at_left(chip("4 SIDES · BOUNDARY", CHALK_GREEN, size=13),
                         COL_L, 0.95)
            k2 = at_left(chip("4 VERTICES · CORNERS", CHALK_PINK, size=13),
                         COL_L, 0.15)
            note = at_left(board_text("every side joins two vertices", 12,
                                      CHALK_WHITE, "BOLD"), COL_L, -0.65)

            strip = at(board_text("The sides form the boundary, and the corners "
                                  "are the vertices.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(fig.fill), Create(fig.sides), run_time=0.70)

            self.wait(leftover(tracker, "b0"))
            self.play(Indicate(fig.sides[0], color=CHALK_YELLOW, scale_factor=1.02),
                      FadeIn(l_ab, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Indicate(fig.sides[1], color=CHALK_YELLOW, scale_factor=1.02),
                      FadeIn(l_bc, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Indicate(fig.sides[2], color=CHALK_YELLOW, scale_factor=1.02),
                      FadeIn(l_cd, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(Indicate(fig.sides[3], color=CHALK_YELLOW, scale_factor=1.02),
                      FadeIn(l_da, scale=0.9), FadeIn(k1, scale=0.9),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(fig.verts, scale=0.9), FadeIn(k2, scale=0.9),
                      run_time=0.60)
            self.add_sound(self.sfx["success"], gain=-12)

            self.wait(leftover(tracker, "b5"))
            self.play(Indicate(fig.verts, color=CHALK_PINK, scale_factor=1.12),
                      FadeIn(note, shift=UP * 0.05),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: four corners, four angles ----------------------------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("Four Corners, Four Angles", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Every corner holds an angle.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill_op=0.11)
            a, b, c, d = fig.points
            col_a, col_b, col_c, col_d = (CHALK_GREEN, CHALK_CYAN, CHALK_PINK,
                                          CHALK_AMBER)
            arc_a = corner_arc(a, b, d, CORNER_R, col_a, 3.0)
            arc_b = corner_arc(b, c, a, CORNER_R, col_b, 3.0)
            arc_c = corner_arc(c, d, b, CORNER_R, col_c, 3.0)
            arc_d = corner_arc(d, a, c, CORNER_R, col_d, 3.0)

            r1 = at(chalk_math(r"\angle A", size=26, color=col_a),
                    COL_L + COL_W / 2.0, 1.25)
            r2 = at(chalk_math(r"\angle B", size=26, color=col_b),
                    COL_L + COL_W / 2.0, 0.55)
            r3 = at(chalk_math(r"\angle C", size=26, color=col_c),
                    COL_L + COL_W / 2.0, -0.15)
            r4 = at(chalk_math(r"\angle D", size=26, color=col_d),
                    COL_L + COL_W / 2.0, -0.85)

            strip = at(board_text("Four vertices give four angles.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(fig.fill), Create(fig.sides), FadeIn(fig.verts),
                      run_time=0.70)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(arc_a), FadeIn(r1, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(arc_b), FadeIn(r2, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Create(arc_c), FadeIn(r3, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(Create(arc_d), FadeIn(r4, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(Indicate(VGroup(arc_a, arc_b, arc_c, arc_d),
                               color=CHALK_YELLOW, scale_factor=1.04),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: adjacent sides share a vertex ------------------------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("Adjacent Means Next To", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Adjacent sides share a vertex.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill_op=0.11)
            a, b, c, d = fig.points
            hl_ab = quad_side(a, b, CHALK_YELLOW, 7.0)
            hl_bc = quad_side(b, c, CHALK_CYAN, 7.0)
            hl_da = quad_side(d, a, CHALK_GREEN, 7.0)

            k1 = at_left(chip("AB and BC · meet at B", CHALK_CYAN, size=13),
                         COL_L, 0.85)
            k2 = at_left(chip("AB and DA · meet at A", CHALK_GREEN, size=13),
                         COL_L, 0.15)

            banner = at(board_text("ADJACENT SIDES SHARE A CORNER", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Neighbouring sides always share a vertex.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(fig.fill), Create(fig.sides), FadeIn(fig.verts),
                      run_time=0.70)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(hl_ab), Create(hl_bc), run_time=0.50)
            self.play(Indicate(fig.verts[1], color=CHALK_YELLOW,
                               scale_factor=1.35),
                      FadeIn(k1, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(hl_da), run_time=0.40)
            self.play(Indicate(fig.verts[0], color=CHALK_YELLOW,
                               scale_factor=1.35),
                      FadeIn(k2, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: opposite means across --------------------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("Opposite Means Across", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Opposite elements never meet.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill_op=0.11)
            a, b, c, d = fig.points
            hl_ab = quad_side(a, b, CHALK_YELLOW, 7.0)
            hl_cd = quad_side(c, d, CHALK_YELLOW, 7.0)
            hl_bc = quad_side(b, c, CHALK_CYAN, 7.0)
            hl_da = quad_side(d, a, CHALK_CYAN, 7.0)

            arc_a = corner_arc(a, b, d, CORNER_R, CHALK_GREEN, 3.0)
            arc_c = corner_arc(c, d, b, CORNER_R, CHALK_GREEN, 3.0)
            arc_b = corner_arc(b, c, a, CORNER_R, CHALK_PINK, 3.0)
            arc_d = corner_arc(d, a, c, CORNER_R, CHALK_PINK, 3.0)

            k1 = at_left(chip("AB opposite CD", CHALK_YELLOW, size=14),
                         COL_L, 1.20)
            k2 = at_left(chip("BC opposite DA", CHALK_YELLOW, size=14),
                         COL_L, 0.50)
            k3 = at_left(chip("A opposite C · B opposite D", CHALK_WHITE,
                              size=12), COL_L, -0.20)
            k4 = at_left(chip("ACROSS, NOT NEXT TO", CHALK_CYAN, size=12),
                         COL_L, -0.90)

            banner = at(board_text("NEXT TO OR ACROSS?", 18, CHALK_YELLOW,
                                   "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Opposite elements lie across the shape.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(fig.fill), Create(fig.sides), FadeIn(fig.verts),
                      run_time=0.70)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(hl_ab), Create(hl_cd), FadeIn(k1, scale=0.9),
                      run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(hl_bc), Create(hl_da), FadeIn(k2, scale=0.9),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Create(arc_a), Create(arc_c), FadeIn(k3, scale=0.9),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(Create(arc_b), Create(arc_d), FadeIn(k4, scale=0.9),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.65)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: diagonals join opposite vertices ---------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Diagonals Join Opposite Vertices", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The two segments across the inside.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill_op=0.11)
            a, b, c, d = fig.points
            # each diagonal carries its own colour, and its chip matches, so
            # AC and BD can be told apart at a glance
            diag_ac = diag(a, c, CHALK_YELLOW)
            diag_bd = diag(b, d, CHALK_PINK)

            k1 = at_left(chip("AC · a diagonal", CHALK_YELLOW, size=14,
                              width=COL_W), COL_L, 0.85)
            k2 = at_left(chip("BD · a diagonal", CHALK_PINK, size=14,
                              width=COL_W), COL_L, 0.15)

            banner = at(board_text("OPPOSITE VERTICES = DIAGONAL", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The two diagonals of ABCD are AC and BD.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(fig.fill), Create(fig.sides), FadeIn(fig.verts),
                      run_time=0.70)

            self.wait(leftover(tracker, "b0"))
            self.play(Indicate(fig.verts[0], color=CHALK_YELLOW,
                               scale_factor=1.35),
                      Indicate(fig.verts[2], color=CHALK_YELLOW,
                               scale_factor=1.35), run_time=0.55)
            self.play(Create(diag_ac), FadeIn(k1, scale=0.9), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Indicate(fig.verts[1], color=CHALK_YELLOW,
                               scale_factor=1.35),
                      Indicate(fig.verts[3], color=CHALK_YELLOW,
                               scale_factor=1.35), run_time=0.55)
            self.play(Create(diag_bd), FadeIn(k2, scale=0.9), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Indicate(VGroup(diag_ac, diag_bd), color=CHALK_YELLOW,
                               scale_factor=1.03),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the relationship map ---------------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Relationship Map", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Adjacent, opposite, or diagonal.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill_op=0.11)
            a, b, c, d = fig.points
            hl_ab = quad_side(a, b, CHALK_YELLOW, 7.0)
            hl_bc = quad_side(b, c, CHALK_YELLOW, 7.0)
            hl_cd = quad_side(c, d, CHALK_CYAN, 7.0)
            diag_ac = diag(a, c)

            k1 = self.col_item("ADJACENT", "share a corner", CHALK_YELLOW, 1.15)
            k2 = self.col_item("OPPOSITE", "across the shape", CHALK_CYAN, 0.05)
            k3 = self.col_item("DIAGONAL", "join opposite vertices", CHALK_PINK,
                               -1.05)

            strip = at(board_text("Next to is adjacent, across is opposite.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(fig.fill), Create(fig.sides), FadeIn(fig.verts),
                      run_time=0.70)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(hl_ab), Create(hl_bc),
                      Indicate(fig.verts[1], color=CHALK_YELLOW,
                               scale_factor=1.35),
                      FadeIn(k1, scale=0.9), run_time=0.65)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeOut(hl_bc), Create(hl_cd), FadeIn(k2, scale=0.9),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Create(diag_ac),
                      Indicate(VGroup(fig.verts[0], fig.verts[2]),
                               color=CHALK_YELLOW, scale_factor=1.30),
                      FadeIn(k3, scale=0.9), run_time=0.65)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
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

            qa = at(self.q_card("opposite of QR?",
                                self.mini_quad("PQRS", CHALK_GREEN),
                                CHALK_GREEN), -2.80, 0.92)
            qb = at(self.q_card("opposite of angle P?",
                                self.mini_quad("PQRS", CHALK_CYAN, arc="P"),
                                CHALK_CYAN), 3.70, 0.92)
            qc = at(self.q_card("adjacent to PQ?",
                                self.mini_quad("PQRS", CHALK_AMBER),
                                CHALK_AMBER), -2.80, -1.02)
            qd = at(self.q_card("join opposite corners",
                                self.mini_quad("PQRS", CHALK_PINK),
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
            a1 = at(self.answer_row("A", "PS is opposite QR",
                                    "across the quadrilateral", CHALK_GREEN),
                    BOARD_CX, 1.62)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "angle R", "R is opposite P",
                                    CHALK_CYAN), BOARD_CX, 0.82)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "PS and QR",
                                    "each shares a vertex with PQ",
                                    CHALK_AMBER), BOARD_CX, 0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "PR and QS",
                                    "the two diagonals of PQRS", CHALK_PINK),
                    BOARD_CX, -0.78)
            self.play(FadeIn(a4, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, a4)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap and the spoken thank-you ----------------------------
    def beat_s10(self) -> None:
        with self.voiceover(text=NARRATION["s10"]) as tracker:
            self.reset_board()

            heading = at(board_text("Build · Compare · Connect", 22, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)

            r1 = at(self.answer_row("1", "4 SIDES · 4 VERTICES · 4 ANGLES",
                                    "the parts of a quadrilateral", CHALK_GREEN),
                    BOARD_CX, 1.48)
            r2 = at(self.answer_row("2", "ADJACENT = NEXT TO",
                                    "adjacent sides share a vertex", CHALK_CYAN),
                    BOARD_CX, 0.72)
            r3 = at(self.answer_row("3", "OPPOSITE = ACROSS",
                                    "AB with CD, BC with DA", CHALK_YELLOW),
                    BOARD_CX, -0.04)
            r4 = at(self.answer_row("4", "2 DIAGONALS",
                                    "they join the opposite vertices",
                                    CHALK_AMBER), BOARD_CX, -0.80)
            strip = at(board_text("Ask: are they next to each other, or across?",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)
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
            # the strip is written on its own bookmark as the voice says "Build
            # it, compare its parts, and connect the corners.", and only the
            # bookmark in front of "Thank you for watching," clears the board
            # and brings in the card.  (The old cut cleared everything on b4,
            # one phrase early, so the frame ran ahead of the voice.)
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

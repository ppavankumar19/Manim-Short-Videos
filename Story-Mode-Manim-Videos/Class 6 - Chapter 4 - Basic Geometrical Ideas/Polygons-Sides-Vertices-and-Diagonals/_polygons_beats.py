    # ================================================================ beats ==
    # Polygons (Class 6 Maths, Chapter 4, Storymode 03).
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
    #   * the persistent quadrilateral and triangle use the fixed, audited
    #     Q_FINAL / T_FINAL coordinates (scale 0.72) so their corner letters
    #     always clear the sub-heading above and the banner below;
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

    def q_card(self, title, pict, color=CHALK_CYAN, width=3.00, pad=0.18,
               title_size=13, buff=0.24):
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
        row (centring put each number at a different x).  The box itself stays
        centred on BOARD_CX.
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

    def mini_quad(self, names=("P", "Q", "R", "S"), color=CHALK_GREEN, s=0.30,
                  diags=False, hl=None):
        """A small labelled quadrilateral PQRS for the challenge cards.

        It is the SAME clean quadrilateral the lesson builds (A->P, B->Q, C->R,
        D->S), scaled about its own centre to a card-sized thumbnail, so the
        challenge asks about the shape the learner has just met.  The letters
        keep the one marker style -- all four at the same offset -- scaled with
        the figure so they stay just outside their corners in a 3.00-wide card.
        """
        cx, cy = QUAD_CENTRE
        pts = {n: ((QUAD_PTS[k][0] - cx) * s, (QUAD_PTS[k][1] - cy) * s)
               for n, k in zip(names, "ABCD")}
        outline = Polygon(*[np.array([*pts[n], 0.0]) for n in names],
                          stroke_color=color, stroke_width=3.2,
                          fill_color=CHALK_CYAN, fill_opacity=0.10)
        offs = {"P": (-0.20, -0.24), "Q": (0.20, -0.24),
                "R": (0.20, 0.24), "S": (-0.20, 0.24)}
        verts = VGroup(*[vertex(n, pts[n], CHALK_CYAN, size=13,
                                label_dx=offs[n]) for n in names])
        parts = [outline, verts]
        if diags:
            parts.append(diag(pts[names[0]], pts[names[2]], CHALK_AMBER, 2.6))
            parts.append(diag(pts[names[1]], pts[names[3]], CHALK_PINK, 2.6))
        if hl == "PQ":
            parts.append(side_seg(pts[names[0]], pts[names[1]],
                                  CHALK_YELLOW, 5.0))
        return VGroup(*parts)

    def mini_open(self, color=CHALK_WHITE):
        """A small open chain (not a polygon) for the challenge."""
        a, b, c, d = (-1.2, 0.4), (-0.3, -0.3), (0.5, 0.3), (1.2, -0.2)
        return VGroup(side_seg(a, b, color, 3.0), side_seg(b, c, color, 3.0),
                      side_seg(c, d, color, 3.0))

    # -- Scene 0: title ------------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = at(board_text("Polygons Explained", 28, CHALK_PINK, "BOLD"),
                       BOARD_CX, 1.66)
            sub = at(board_text("Sides · Vertices · Adjacent Elements · "
                                "Diagonals", 18, CHALK_WHITE, "BOLD"),
                     BOARD_CX, 1.00)

            specs = (("SIDE", "side", "the boundary", CHALK_GREEN),
                     ("VERTEX", "vertex", "a corner point", CHALK_CYAN),
                     ("DIAGONAL", "diagonal", "joins opposite vertices",
                      CHALK_AMBER))
            # One centred row: the three captions differ in width, so the
            # columns are placed by equal air (row_centres) and the row's ink is
            # centred on the board axis.  The old columns ran -2.20..+2.20, i.e.
            # centred on 0.0, half a unit left of BOARD_CX.
            labels, figs, notes = VGroup(), VGroup(), VGroup()
            raw_figs, caps = [], []
            for label, kind, note, color in specs:
                if kind == "side":
                    fig = VGroup(side_seg((-0.8, 0.0), (0.8, 0.0), color, 4.6),
                                 Dot(radius=DOT_R, color=CHALK_CYAN,
                                     fill_opacity=1.0).move_to(
                                     np.array([-0.8, 0.0, 0.0])),
                                 Dot(radius=DOT_R, color=CHALK_CYAN,
                                     fill_opacity=1.0).move_to(
                                     np.array([0.8, 0.0, 0.0])))
                elif kind == "vertex":
                    fig = Dot(radius=0.11, color=color, fill_opacity=1.0)
                else:
                    fig = diag((-0.8, 0.0), (0.8, 0.0), color, 3.2)
                raw_figs.append(fig)
                caps.append((board_text(label, 14, color, "BOLD"),
                             board_text(note, 12, CHALK_WHITE, "BOLD")))
            xs = row_centres([max(f.width, c[0].width, c[1].width) / 2.0
                              for f, c in zip(raw_figs, caps)], 0.55)
            for x, fig, (lab, note) in zip(xs, raw_figs, caps):
                figs.add(at(fig, x, -0.18))
                labels.add(at(lab, x, 0.34))
                notes.add(at(note, x, -0.74))
            strip = at(board_text("A simple closed figure made of line "
                                  "segments.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(title, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            # the parts are drawn first, then NAMED on the line that names them
            # ("sides, vertices, and diagonals ... let us learn their names")
            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[Create(m) for m in figs], lag_ratio=0.22),
                      run_time=0.75)

            self.wait(leftover(tracker, "b1"))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.06) for m in labels],
                                  lag_ratio=0.18), run_time=0.55)
            self.play(LaggedStart(*[FadeIn(m, scale=0.85) for m in notes],
                                  lag_ratio=0.18), run_time=0.55)
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: from a closed curve to a polygon ---------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("From a Closed Curve to a Polygon", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The smooth boundary becomes straight "
                                "segments.", 17, CHALK_WHITE, "BOLD"),
                     BOARD_CX, SUB_Y)

            # the SAME clean quadrilateral, shown at 0.85 here so the oval, the
            # arrow and the polygon form one centred row: the oval's ink on the
            # left, the arrow centred in the gap between them, the polygon on
            # the right, each caption under its own figure.  Block ink+labels
            # [-3.52..+4.52] -> centre +0.50.  (It used to run -3.85..+4.80 with
            # the arrow butted against the polygon's left corner.)
            ymid = 0.50
            curve = at(Ellipse(width=1.70, height=1.30, stroke_color=CHALK_WHITE,
                               stroke_width=3.2), -2.43, ymid)
            curve_lab = at(board_text("a smooth closed curve", 14, CHALK_WHITE,
                                      "BOLD"), -2.43, -0.62)
            pts = quad_points(0.85, dx=2.57 - BOARD_CX, dy=ymid - QUAD_CENTRE[1])
            poly = quad_shape(pts, CHALK_GREEN, 3.4)
            verts = quad_verts(pts, CHALK_CYAN, MARK_SIZE)
            poly_lab = at(board_text("polygon", 15, CHALK_GREEN, "BOLD"),
                          2.57, -0.62)
            arrow = Arrow(np.array([curve.get_right()[0] + 0.45, ymid, 0.0]),
                          np.array([poly.get_left()[0] - 0.45, ymid, 0.0]),
                          buff=0.0, color=CHALK_AMBER, stroke_width=3.0,
                          tip_length=0.22)

            banner = at(board_text("POLYGON = SIMPLE + CLOSED + LINE SEGMENTS",
                                   17, CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The corners appear when the boundary "
                                  "straightens.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(curve), FadeIn(curve_lab, shift=UP * 0.05),
                      run_time=0.65)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(poly), FadeIn(verts, scale=0.8), Create(arrow),
                      FadeIn(poly_lab, scale=0.9), run_time=0.70)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: what must a polygon have -----------------------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("What Must a Polygon Have?", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Line segments, closed, and no crossing.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # the chain and the triangle are both centred on the board axis;
            # their captions are side labels, parked clear of the figure
            chain = at(open_chain(CHALK_WHITE, 4.0), BOARD_CX, 0.90)
            open_note = at(board_text("not closed", 14, CHALK_PINK, "BOLD"),
                           3.30, 0.90)
            tri = tri_shape(CHALK_GREEN, 4.0)
            tverts = tri_verts()
            closed_note = at(board_text("closed", 14, CHALK_GREEN, "BOLD"),
                             3.30, 0.30)

            banner = at(board_text("SIMPLE + CLOSED + LINE SEGMENTS", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("3 sides is the smallest number.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(chain), FadeIn(open_note, shift=UP * 0.05),
                      run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeOut(chain), FadeOut(open_note), run_time=0.40)
            self.play(Create(tri), FadeIn(tverts, scale=0.8),
                      FadeIn(closed_note, shift=UP * 0.05), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: sides and vertices of a triangle ---------------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Sides and Vertices", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Triangle ABC: three sides, three corners.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            tri = tri_shape(CHALK_GREEN, 4.0)
            verts = tri_verts()
            side_ab = side_seg(tpoint("A"), tpoint("B"), CHALK_CYAN, 5.5)
            side_bc = side_seg(tpoint("B"), tpoint("C"), CHALK_YELLOW, 5.5)
            side_ca = side_seg(tpoint("C"), tpoint("A"), CHALK_PINK, 5.5)

            sides_chip = at(chip("SIDES", CHALK_GREEN), -3.30, 1.55)
            verts_chip = at(chip("VERTICES", CHALK_CYAN), 3.30, 1.55)
            banner = at(board_text("SIDES MEET AT VERTICES", 18, CHALK_YELLOW,
                                   "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("A triangle has three sides and three "
                                  "vertices.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(tri), FadeIn(verts, scale=0.8), run_time=0.60)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(side_ab), FadeIn(sides_chip, scale=0.9),
                      run_time=0.45)
            self.play(Create(side_bc), Create(side_ca), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(LaggedStart(*[Indicate(v, color=CHALK_CYAN,
                                             scale_factor=1.2)
                                    for v in verts], lag_ratio=0.25),
                      FadeIn(verts_chip, scale=0.9), run_time=0.70)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Indicate(verts[1], color=CHALK_YELLOW, scale_factor=1.3),
                      Indicate(side_ab, color=CHALK_YELLOW, scale_factor=1.05),
                      Indicate(side_bc, color=CHALK_YELLOW, scale_factor=1.05),
                      run_time=0.65)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: building quadrilateral ABCD --------------------------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("Building Quadrilateral ABCD", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Four sides, four vertices.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            outline = quad_shape(QUAD_PTS, CHALK_GREEN, 4.0)
            verts = quad_verts(QUAD_PTS)
            side_ab = side_seg(qpoint("A"), qpoint("B"), CHALK_CYAN, 5.5)
            side_bc = side_seg(qpoint("B"), qpoint("C"), CHALK_YELLOW, 5.5)
            side_cd = side_seg(qpoint("C"), qpoint("D"), CHALK_PINK, 5.5)
            side_da = side_seg(qpoint("D"), qpoint("A"), CHALK_WHITE, 5.5)
            sides_chip = at(chip("4 SIDES", CHALK_GREEN), -3.30, 1.55)
            verts_chip = at(chip("4 VERTICES", CHALK_CYAN), 3.30, 1.55)

            strip = at(board_text("A quadrilateral is a polygon with four "
                                  "sides.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(outline), FadeIn(verts, scale=0.8), run_time=0.60)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(side_ab), FadeIn(sides_chip, scale=0.9),
                      run_time=0.40)
            self.play(Create(side_bc), run_time=0.30)
            self.play(Create(side_cd), run_time=0.30)
            self.play(Create(side_da), run_time=0.30)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(LaggedStart(*[Indicate(v, color=CHALK_CYAN,
                                             scale_factor=1.15)
                                    for v in verts], lag_ratio=0.22),
                      FadeIn(verts_chip, scale=0.9), run_time=0.70)
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: adjacent = next to -----------------------------------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("Adjacent = Next To", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Sides that share a corner.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            outline = quad_shape(QUAD_PTS, CHALK_GREEN, 4.0)
            verts = quad_verts(QUAD_PTS)
            side_ab = side_seg(qpoint("A"), qpoint("B"), CHALK_CYAN, 5.5)
            side_bc = side_seg(qpoint("B"), qpoint("C"), CHALK_YELLOW, 5.5)
            side_da = side_seg(qpoint("D"), qpoint("A"), CHALK_PINK, 5.5)

            banner = at(board_text("ADJACENT = SHARING A CORNER", 18,
                                   CHALK_AMBER, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("AB is adjacent to BC and to DA — they share "
                                  "a corner.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(outline), FadeIn(verts, scale=0.8), run_time=0.60)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(side_ab), run_time=0.45)
            self.play(Indicate(verts[0], color=CHALK_CYAN, scale_factor=1.25),
                      Indicate(verts[1], color=CHALK_CYAN, scale_factor=1.25),
                      run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(side_bc), Create(side_da), run_time=0.55)
            self.play(Indicate(verts[1], color=CHALK_YELLOW, scale_factor=1.25),
                      Indicate(verts[0], color=CHALK_YELLOW, scale_factor=1.25),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: adjacent vs opposite ---------------------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("Across, Not Next To", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The side and vertices opposite AB.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            outline = quad_shape(QUAD_PTS, CHALK_GREEN, 4.0)
            verts = quad_verts(QUAD_PTS)
            side_ab = side_seg(qpoint("A"), qpoint("B"), CHALK_CYAN, 5.5)
            side_cd = side_seg(qpoint("C"), qpoint("D"), CHALK_PINK, 5.5)

            banner = at(board_text("OPPOSITE VERTICES: A and C · B and D", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("CD is the side opposite AB — they do not "
                                  "share a corner.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(outline), FadeIn(verts, scale=0.8), run_time=0.60)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(side_ab), Create(side_cd), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Indicate(verts[0], color=CHALK_AMBER, scale_factor=1.3),
                      Indicate(verts[2], color=CHALK_AMBER, scale_factor=1.3),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Indicate(verts[1], color=CHALK_YELLOW, scale_factor=1.3),
                      Indicate(verts[3], color=CHALK_YELLOW, scale_factor=1.3),
                      run_time=0.60)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: diagonals --------------------------------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Diagonals Cut Across", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Join the opposite vertices.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            outline = quad_shape(QUAD_PTS, CHALK_GREEN, 4.0)
            verts = quad_verts(QUAD_PTS)
            # each diagonal carries its own colour (and its own chip, on the
            # matching side, so the pair is symmetric about the board axis), so
            # AC and BD can be told apart at a glance
            d_ac = diag(qpoint("A"), qpoint("C"), CHALK_AMBER, 4.0)
            d_bd = diag(qpoint("B"), qpoint("D"), CHALK_PINK, 4.0)

            diag_ac = at(chip("AC", CHALK_AMBER, width=1.20), -3.30, 1.55)
            diag_bd = at(chip("BD", CHALK_PINK, width=1.20), 3.30, 1.55)
            banner = at(board_text("DIAGONAL = JOIN OPPOSITE VERTICES", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Quadrilateral ABCD has two diagonals: AC "
                                  "and BD.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(outline), FadeIn(verts, scale=0.8), run_time=0.60)

            self.wait(leftover(tracker, "b0"))
            self.play(Indicate(verts[0], color=CHALK_AMBER, scale_factor=1.3),
                      Indicate(verts[2], color=CHALK_AMBER, scale_factor=1.3),
                      run_time=0.50)
            self.play(Create(d_ac), FadeIn(diag_ac, scale=0.9), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Indicate(verts[1], color=CHALK_PINK, scale_factor=1.3),
                      Indicate(verts[3], color=CHALK_PINK, scale_factor=1.3),
                      run_time=0.50)
            self.play(Create(d_bd), FadeIn(diag_bd, scale=0.9), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: side or diagonal -------------------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("Side or Diagonal?", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Boundary segment, or opposite-vertex "
                                "connection?", 17, CHALK_WHITE, "BOLD"),
                     BOARD_CX, SUB_Y)

            outline = quad_shape(QUAD_PTS, CHALK_GREEN, 4.0)
            verts = quad_verts(QUAD_PTS)
            side_ab = side_seg(qpoint("A"), qpoint("B"), CHALK_CYAN, 5.5)
            d_ac = diag(qpoint("A"), qpoint("C"), CHALK_AMBER, 3.4)

            banner = at(board_text("BOUNDARY = SIDE · OPPOSITE VERTICES = "
                                   "DIAGONAL", 17, CHALK_YELLOW, "BOLD"),
                        BOARD_CX, BANNER_Y)
            strip = at(board_text("AB is a side; AC is a diagonal — a diagonal "
                                  "is never on the boundary.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(outline), FadeIn(verts, scale=0.8), run_time=0.60)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(side_ab), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(d_ac), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
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
            sub = at(board_text("Four checks on quadrilateral PQRS.", 16,
                                CHALK_WHITE, "BOLD"), BOARD_CX, 2.20)

            qa = at(self.q_card("name the four sides", self.mini_quad(),
                                CHALK_GREEN), -2.75, 0.95)
            qb = at(self.q_card("adjacent to PQ?",
                                self.mini_quad(hl="PQ"), CHALK_YELLOW),
                    3.75, 0.95)
            qc = at(self.q_card("name the diagonals",
                                self.mini_quad(diags=True), CHALK_AMBER),
                    -2.75, -1.00)
            qd = at(self.q_card("is this a polygon?", self.mini_open(),
                                CHALK_CYAN), 3.75, -1.00)

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
            a1 = at(self.answer_row("A", "PQ · QR · RS · SP", "the four sides",
                                    CHALK_GREEN), BOARD_CX, 1.62)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "QR and PS",
                                    "share an endpoint with PQ", CHALK_YELLOW),
                    BOARD_CX, 0.82)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "PR and QS", "join opposite vertices",
                                    CHALK_AMBER), BOARD_CX, 0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "NO — not a polygon",
                                    "an open chain is not closed", CHALK_PINK),
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

            heading = at(board_text("Know the Parts", 22, CHALK_AMBER, "BOLD"),
                         BOARD_CX, ROW_Y)

            r1 = at(self.answer_row("1", "POLYGON",
                                    "simple + closed + line segments",
                                    CHALK_GREEN), BOARD_CX, 1.48)
            r2 = at(self.answer_row("2", "SIDES · VERTICES",
                                    "boundary segments · corner points",
                                    CHALK_CYAN), BOARD_CX, 0.72)
            r3 = at(self.answer_row("3", "ADJACENT",
                                    "sides sharing a corner", CHALK_YELLOW),
                    BOARD_CX, -0.04)
            r4 = at(self.answer_row("4", "DIAGONALS",
                                    "join opposite vertices", CHALK_AMBER),
                    BOARD_CX, -0.80)
            strip = at(board_text("Know the parts — understand the polygon.",
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
            # the strip is written on its own bookmark as the voice says "Know
            # the parts, and you understand the polygon.", and only the bookmark
            # in front of "Thank you for watching," clears the board and brings
            # in the card.  (The old cut cleared everything on b4, one phrase
            # early, so the frame ran ahead of the voice.)
            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeOut(heading), FadeOut(r1), FadeOut(r2), FadeOut(r3),
                      FadeOut(r4), FadeOut(strip), run_time=0.55)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.50)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.closing(tracker, thanks, run_time=1.1)
            self._capture_srt(tracker)

        self.wait(END_HOLD)

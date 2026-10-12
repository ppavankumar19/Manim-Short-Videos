    # ================================================================ beats ==
    # Curves & Regions (Class 6 Maths, Chapter 4, Storymode 02).
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
    #   * every curve is built centred on the origin and then pinned with `at`,
    #     so a heading, a card and a diagram all share the board centre;
    #   * one row per idea, with at least 0.22 units of clear air between the
    #     ink of neighbouring rows (checked by audit_clearance.py);
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
        """One 'your turn' card: a one-line prompt above its small diagram."""
        head = board_text(title, title_size, color, "BOLD")
        content = VGroup(head, pict).arrange(DOWN, buff=buff)
        box = RoundedRectangle(corner_radius=0.10, width=width,
                               height=content.height + 2 * pad,
                               stroke_color=color, stroke_width=1.9,
                               fill_color=PANEL_FILL, fill_opacity=0.55)
        content.move_to(box.get_center())
        return VGroup(box, content)

    def curve_card(self, title, curve, color, width=2.80, pad=0.24,
                   title_size=14, buff=0.20):
        """A titled card around a small curve (used in the 2-question scene)."""
        head = board_text(title, title_size, color, "BOLD")
        content = VGroup(head, curve).arrange(DOWN, buff=buff)
        box = RoundedRectangle(corner_radius=0.10, width=width,
                               height=content.height + 2 * pad,
                               stroke_color=color, stroke_width=1.9,
                               fill_color=PANEL_FILL, fill_opacity=0.55)
        content.move_to(box.get_center())
        return VGroup(box, content)

    def region_mini(self, color=CHALK_GREEN, w=1.40, h=0.64):
        """A small closed figure with P inside, Q on the edge, R outside.

        The letters sit *around* the drawing, so the card stays short enough to
        keep clear of the caption band below the board -- but each one is also
        a clear 0.2+ away from the curve: Q's letter sits ABOVE the top vertex
        (beside it, the arc curved under the letter and touched it) and R's
        letter is a full step to the right of the right vertex."""
        oval = Ellipse(width=w, height=h, stroke_color=color, stroke_width=2.6)
        fill = Ellipse(width=w, height=h, stroke_width=0, fill_color=CHALK_CYAN,
                       fill_opacity=0.18)
        # P -- inside the edge, its letter beside the dot, all well within
        pdot = Dot(radius=DOT_R, color=CHALK_CYAN, fill_opacity=1.0).move_to(
            np.array([-0.36, 0.0, 0.0]))
        plab = board_text("P", 13, CHALK_CYAN, "BOLD").move_to(
            np.array([-0.16, 0.0, 0.0]))
        # Q -- exactly on the edge, the letter above the top vertex
        qdot = Dot(radius=DOT_R, color=CHALK_AMBER, fill_opacity=1.0).move_to(
            np.array([0.0, h / 2.0, 0.0]))
        qlab = board_text("Q", 13, CHALK_AMBER, "BOLD").move_to(
            np.array([0.0, h / 2.0 + 0.32, 0.0]))
        # R -- outside the edge
        rdot = Dot(radius=DOT_R, color=CHALK_PINK, fill_opacity=1.0).move_to(
            np.array([w / 2.0 + 0.22, 0.0, 0.0]))
        rlab = board_text("R", 13, CHALK_PINK, "BOLD").move_to(
            np.array([w / 2.0 + 0.44, 0.0, 0.0]))
        return VGroup(fill, oval, pdot, plab, qdot, qlab, rdot, rlab)

    def answer_row(self, tag, headline, note, color, width=8.60, height=0.62,
                   pad=0.34, buff=0.36):
        """One revealed answer: its letter, the result and a short note.

        The row is laid out in FIXED COLUMNS, not centred in the box: every row
        starts at the box's left edge plus `pad`, then tag, sentence and note
        follow with one constant `buff` between them.  Centring each row put the
        letter at a different x in every row (the sentences differ in width), so
        the answers scene read "A  OPEN + SIMPLE" / "B   CLOSED ..." with the
        letters and gaps all out of line; the recap rows had the same defect.
        With the row anchored left the tag column is one vertical line and the
        sentence column starts at the same x in every row, while the box itself
        stays centred on BOARD_CX.  The widest row (D: P interior · Q boundary ·
        R exterior / inside · on · outside) is 7.08 wide against 7.92 of room.
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

    # -- Scene 0: title ------------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = at(board_text("Understanding Curves & Regions", 27,
                                  CHALK_PINK, "BOLD"), BOARD_CX, 1.66)
            sub = at(board_text("Open · Closed · Interior · Exterior · Boundary",
                                18, CHALK_WHITE, "BOLD"), BOARD_CX, 1.06)

            specs = (("OPEN", "open_wave", "the ends stay apart", CHALK_CYAN),
                     ("CLOSED", "oval", "the path joins back", CHALK_GREEN),
                     ("NOT SIMPLE", "eight", "the path crosses itself",
                      CHALK_PINK))
            # One evenly spaced row: the three figures' ink is centred on the
            # board axis and every label/caption sits clear of its own curve
            # (the old card put OPEN on the wave's crest, CLOSED on the oval's
            # top and "the path joins back" across the oval's lower arc).
            # The three rows are stacked with >= 0.20 of clear air everywhere:
            # heading 1.66 / sub 1.06 / labels 0.52 / figures -0.38 /
            # captions -1.20, each caption still a clear 0.20 under its curve
            # and 0.41 above the closing strip.
            loop_w, loop_h = 1.50, 1.05
            xs = row_centres((0.85, loop_w / 2.0, 0.55), 1.10)
            lab_y, pic_y, note_y = 0.52, -0.38, -1.20
            labels, pics, notes = VGroup(), VGroup(), VGroup()
            for x, (label, kind, note, color) in zip(xs, specs):
                labels.add(at(board_text(label, 14, color, "BOLD"), x, lab_y))
                curve = (open_wave(color, width=1.70, amp=0.40) if kind == "open_wave"
                         else oval(color, w=loop_w, h=loop_h) if kind == "oval"
                         else figure_eight(color, a=0.55))
                pics.add(at(curve, x, pic_y))
                notes.add(at(board_text(note, 12, CHALK_WHITE, "BOLD"), x, note_y))
            strip = at(board_text("A curve is drawn without lifting the pencil.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            # The pencil tip that drew the closed loop keeps travelling round
            # it for the whole hold -- through the waits and the closing
            # Indicate -- because the phase is advanced on every frame, not by
            # a fixed-length Rotate.  (A Rotate about the centre would trace a
            # circle and leave the oval, so the point is parametric.)  It is
            # chalk-yellow, not green, so the travelling tip stays visible
            # against the green loop it is drawing.
            phase = ValueTracker(0.0)
            trace = Dot(radius=0.055, color=CHALK_YELLOW, fill_opacity=1.0)
            trace.move_to(loop_point(xs[1], pic_y, loop_w, loop_h, 0.0))
            trace.add_updater(lambda m: m.move_to(
                loop_point(xs[1], pic_y, loop_w, loop_h, phase.get_value())))
            phase.add_updater(lambda m, dt: m.increment_value(dt * LOOP_SPEED))

            self.play(FadeIn(title, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.06) for m in labels],
                                  lag_ratio=0.18), run_time=0.55)
            self.play(LaggedStart(*[Create(m) for m in pics], lag_ratio=0.22),
                      run_time=0.75)
            self.add(phase)
            self.play(FadeIn(trace, scale=0.7), run_time=0.30)

            self.wait(leftover(tracker, "b1"))
            self.play(LaggedStart(*[FadeIn(m, scale=0.85) for m in notes],
                                  lag_ratio=0.18), run_time=0.55)
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: one pencil, many curves ------------------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("One Pencil, Many Curves", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A curve is drawn without lifting the pencil.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            xa = row_centres((0.95, 0.725, 0.62, 0.85), 0.75)
            pic_y, name_y = 1.10, 0.22
            wave = at(open_wave(CHALK_CYAN, width=1.90, amp=0.45), xa[0], pic_y)
            loop = at(oval(CHALK_GREEN, w=1.45, h=1.00), xa[1], pic_y)
            eight = at(figure_eight(CHALK_PINK, a=0.62), xa[2], pic_y)
            line = at(straight_line(xa[3] - 0.85, xa[3] + 0.85, pic_y, CHALK_YELLOW),
                      xa[3], pic_y)
            names = VGroup(*[
                at(board_text(n, 13, c, "BOLD"), x, name_y)
                for n, c, x in (("a wavy path", CHALK_CYAN, xa[0]),
                                ("a loop", CHALK_GREEN, xa[1]),
                                ("a crossing path", CHALK_PINK, xa[2]),
                                ("even a straight line", CHALK_YELLOW, xa[3]))])

            banner = at(board_text("YES — EVEN A STRAIGHT LINE IS A CURVE", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Any figure drawn in one continuous stroke.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(wave), Create(loop), Create(eight), run_time=1.1)
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.05) for m in names],
                                  lag_ratio=0.2), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(line), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: open or closed ---------------------------------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("Open or Closed?", 20, CHALK_AMBER, "BOLD"),
                         BOARD_CX, ROW_Y)
            sub = at(board_text("Question 1: does the path close?", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # Two columns, one evenly spaced row: the pair's ink is centred on
            # the board axis, the captions sit UNDER their figure (the old card
            # ran "the path comes back and closes" straight through the oval's
            # lower arc) and the chips sit clear below the captions.
            yc, note_y, chip_y = 1.25, 0.26, -0.45
            xs = row_centres((1.35, 1.10), 1.50)
            wave = at(open_wave(CHALK_CYAN, width=2.70, amp=0.55), xs[0], yc)
            open_note = at(board_text("the two ends stay apart", 14, CHALK_WHITE,
                                      "BOLD"), xs[0], note_y)
            open_chip = at(chip("OPEN CURVE", CHALK_CYAN), xs[0], chip_y)
            oval_mob = at(oval(CHALK_GREEN, w=2.20, h=1.10), xs[1], yc)
            close_note = at(board_text("the path comes back and closes", 14,
                                       CHALK_WHITE, "BOLD"), xs[1], note_y)
            close_chip = at(chip("CLOSED CURVE", CHALK_GREEN), xs[1], chip_y)

            banner = at(board_text("QUESTION 1: DOES THE PATH CLOSE?", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("If the ends meet, the curve is closed.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(wave), run_time=0.70)
            self.play(FadeIn(open_note, shift=UP * 0.05),
                      FadeIn(open_chip, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(oval_mob), run_time=0.70)
            self.play(FadeIn(close_note, shift=UP * 0.05),
                      FadeIn(close_chip, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: simple or self-crossing ------------------------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Simple or Self-Crossing?", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Question 2: does it cross itself?", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # Same two-column shape as the open/closed frame: both figures end
            # on a common line (y = 0.70) so the captions can sit clear below
            # them -- "never crosses itself" used to cut the oval's lower arc
            # and "it crosses itself here" the figure-eight itself.
            note_y, chip_y = 0.30, -0.45
            ox, ex = row_centres((1.10, 1.15), 1.50)
            oval_mob = at(oval(CHALK_GREEN, w=2.20, h=1.10), ox, 1.25)
            simple_note = at(board_text("never crosses itself", 14, CHALK_WHITE,
                                        "BOLD"), ox, note_y)
            simple_chip = at(chip("SIMPLE", CHALK_GREEN), ox, chip_y)

            eight = at(figure_eight(CHALK_PINK, a=1.15), ex, 1.11)
            cross = at(Dot(radius=0.055, color=CHALK_YELLOW, fill_opacity=1.0),
                       ex, 1.11)
            cross_note = at(board_text("it crosses itself here", 14, CHALK_WHITE,
                                       "BOLD"), ex, note_y)
            not_chip = at(chip("NOT SIMPLE", CHALK_PINK), ex, chip_y)

            banner = at(board_text("SIMPLE = DOES NOT CROSS ITSELF", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Simple means no crossing, not easy.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(oval_mob), run_time=0.65)
            self.play(FadeIn(simple_note, shift=UP * 0.05),
                      FadeIn(simple_chip, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(eight), run_time=0.65)
            self.play(FadeIn(cross, scale=0.8),
                      FadeIn(cross_note, shift=UP * 0.05),
                      FadeIn(not_chip, scale=0.9), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: two different questions ------------------------------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("Two Different Questions", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Open or closed?  Simple or not simple?", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # three equal cards, evenly spaced and centred on the board axis
            xs = row_centres((1.40, 1.40, 1.40), 0.30)
            ca = at(self.curve_card("OPEN + SIMPLE",
                                    open_wave(CHALK_CYAN, width=2.10, amp=0.40),
                                    CHALK_CYAN), xs[0], 0.45)
            cb = at(self.curve_card("CLOSED + SIMPLE",
                                    oval(CHALK_GREEN, w=1.50, h=1.10),
                                    CHALK_GREEN), xs[1], 0.45)
            cc = at(self.curve_card("CLOSED, NOT SIMPLE",
                                    figure_eight(CHALK_PINK, a=0.55),
                                    CHALK_PINK), xs[2], 0.45)

            banner = at(board_text("ASK BOTH QUESTIONS FOR EVERY CURVE", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Open or closed · simple or not simple.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(ca, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(cb, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(cc, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: a closed curve separates the plane -------------------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("A Closed Curve Separates the Plane", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Like the boundary wall of a park.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # the park wall is centred on the board axis; the BOUNDARY chip now
            # sits a clear 0.25 above the wall (it used to cut the oval's top)
            # and the traveller crosses the wall just under the EXTERIOR chip
            yc, w, h = 0.30, 3.20, 1.60
            wall = at(oval(CHALK_GREEN, w=w, h=h), BOARD_CX, yc)
            inside = at(interior_fill(w, h, CHALK_CYAN, 0.20), BOARD_CX, yc)
            boundary_chip = at(chip("BOUNDARY", CHALK_AMBER), BOARD_CX, 1.60)
            interior_chip = at(chip("INTERIOR", CHALK_CYAN), BOARD_CX, yc)
            exterior_chip = at(chip("EXTERIOR", CHALK_PINK), BOARD_CX + 2.80, yc)
            traveller = Dot(radius=0.06, color=CHALK_YELLOW, fill_opacity=1.0)
            traveller.move_to(np.array([BOARD_CX + 2.10, -0.35, 0.0]))

            banner = at(board_text("A CLOSED FIGURE SEPARATES THE PLANE", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Inside · On the wall · Outside.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(inside), Create(wall), run_time=0.70)
            self.play(FadeIn(boundary_chip, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(interior_chip, scale=0.9),
                      FadeIn(exterior_chip, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(traveller, scale=0.8), run_time=0.35)
            self.play(traveller.animate.move_to(
                np.array([BOARD_CX + 0.40, -0.35, 0.0])), run_time=1.1)
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: where is the point -----------------------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("Where Is the Point?", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Inside, on the edge, or outside?", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # the test oval is centred on the board axis, A sits well inside it,
            # B's letter 0.25 clear of the left vertex, C's letter 0.26 clear of
            # the right vertex, and the three result chips are one evenly
            # spaced, board-centred row
            yc, w, h = 0.75, 2.60, 1.50
            wall = at(oval(CHALK_GREEN, w=w, h=h), BOARD_CX, yc)
            inside = at(interior_fill(w, h, CHALK_CYAN, 0.18), BOARD_CX, yc)
            pa = dot_point("A", BOARD_CX, yc + 0.10, CHALK_CYAN, size=18,
                           label_dy=-0.34)
            pb = VGroup(Dot(radius=DOT_R, color=CHALK_AMBER,
                            fill_opacity=1.0).move_to(
                            np.array([BOARD_CX - w / 2.0, yc, 0.0])),
                        at(board_text("B", 18, CHALK_AMBER, "BOLD"),
                           BOARD_CX - w / 2.0 - 0.34, yc))
            pc = dot_point("C", BOARD_CX + w / 2.0 + 0.35, yc, CHALK_PINK,
                           size=18, label_dy=-0.34)

            chips = VGroup(chip("A · INTERIOR", CHALK_CYAN),
                           chip("B · BOUNDARY", CHALK_AMBER),
                           chip("C · EXTERIOR", CHALK_PINK))
            chips.arrange(RIGHT, buff=0.40).move_to(
                np.array([BOARD_CX, -0.60, 0.0]))
            chip_a, chip_b, chip_c = chips

            banner = at(board_text("INSIDE · ON THE EDGE · OUTSIDE", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Each point has exactly one place.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(inside), Create(wall), run_time=0.60)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(pa, scale=0.8), FadeIn(chip_a, scale=0.9),
                      run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(pb, scale=0.8), FadeIn(chip_b, scale=0.9),
                      run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(pc, scale=0.8), FadeIn(chip_c, scale=0.9),
                      run_time=0.45)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: what a region is -------------------------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("What Is a Region?", 20, CHALK_AMBER, "BOLD"),
                         BOARD_CX, ROW_Y)
            sub = at(board_text("The interior and the boundary together.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # the wall is paired with the right-hand REGION column, so the two
            # together are centred on the board axis (union -3.30..+4.30); the
            # BOUNDARY chip keeps 0.30 of air above the wall's top edge
            yc, w, h = 0.20, 3.00, 1.70
            wall = at(oval(CHALK_GREEN, w=w, h=h), -1.80, yc)
            inside = at(interior_fill(w, h, CHALK_CYAN, 0.20), -1.80, yc)
            interior_chip = at(chip("INTERIOR", CHALK_CYAN), -1.80, yc)
            boundary_chip = at(chip("BOUNDARY", CHALK_AMBER), -1.80, 1.60)
            region_chip = at(chip("REGION", CHALK_YELLOW, width=3.20, height=0.9),
                             2.70, 0.55)
            region_note = at(board_text("the whole closed part", 13, CHALK_WHITE,
                                        "BOLD"), 2.70, -0.32)

            banner = at(board_text("REGION = INTERIOR + BOUNDARY", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The edge is part of the region too.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(inside), Create(wall), run_time=0.60)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(interior_chip, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(boundary_chip, scale=0.9),
                      Indicate(wall, color=CHALK_AMBER, scale_factor=1.04),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(region_chip, scale=0.9),
                      FadeIn(region_note, shift=UP * 0.05), run_time=0.55)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: from a closed curve to a polygon ---------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("From a Closed Curve to a Polygon", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Make the boundary from straight line segments.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # oval + arrow + hexagon are one row, centred on the board axis,
            # with both names a clear 0.3 below their figure
            xs = row_centres((0.95, 0.70), 2.60)
            yc, lab_y = 0.85, -0.25
            oval_mob = at(oval(CHALK_GREEN, w=1.90, h=1.40), xs[0], yc)
            oval_lab = at(board_text("closed curve", 14, CHALK_WHITE, "BOLD"),
                          xs[0], lab_y)
            # a hexagon built from six straight segments
            pts = [np.array([0.70 * np.cos(a), 0.70 * np.sin(a), 0.0])
                   for a in np.linspace(np.pi / 6, 2 * np.pi + np.pi / 6, 7)]
            hexagon = Polygon(*pts, stroke_color=CHALK_CYAN, stroke_width=3.0)
            hexagon.move_to(np.array([xs[1], yc, 0.0]))
            poly_lab = at(board_text("polygon", 14, CHALK_WHITE, "BOLD"),
                          xs[1], lab_y)
            arrow = Arrow(np.array([xs[0] + 1.30, yc, 0.0]),
                          np.array([xs[1] - 1.05, yc, 0.0]), buff=0.15,
                          color=CHALK_AMBER, stroke_width=3.0,
                          tip_length=0.22)

            banner = at(board_text("A POLYGON IS A SIMPLE CLOSED FIGURE OF "
                                   "LINE SEGMENTS", 17, CHALK_YELLOW, "BOLD"),
                        BOARD_CX, BANNER_Y)
            strip = at(board_text("Triangles and quadrilaterals come next.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(oval_mob), FadeIn(oval_lab, shift=UP * 0.05),
                      run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(hexagon), FadeIn(poly_lab, shift=UP * 0.05),
                      run_time=0.60)
            self.play(Create(arrow), run_time=0.40)
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
                         BOARD_CX, ROW_Y)
            sub = at(board_text("Classify each diagram, then locate P, Q and R.",
                                16, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # the four question cards are the series' corner grid about the
            # board axis (union -4.25..+5.25, centre 0.5), raised just enough
            # that no card's box dips into the caption band; the P/Q/R card
            # keeps 0.30 between its prompt and the mini figure (Q's letter sits
            # above the mini's top vertex, so 0.20 left them touching)
            qa = at(self.q_card("open or closed?",
                                open_wave(CHALK_CYAN, width=1.70, amp=0.30),
                                CHALK_CYAN), -2.75, 1.00)
            qb = at(self.q_card("open or closed?",
                                oval(CHALK_GREEN, w=1.30, h=0.90),
                                CHALK_GREEN), 3.75, 1.00)
            qc = at(self.q_card("simple or not simple?",
                                figure_eight(CHALK_PINK, a=0.42),
                                CHALK_PINK), -2.75, -0.95)
            qd = at(self.q_card("classify P, Q and R",
                                self.region_mini(CHALK_GREEN),
                                CHALK_AMBER, pad=0.14, buff=0.30), 3.75, -0.95)

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
            a1 = at(self.answer_row("A", "OPEN + SIMPLE",
                                    "two free ends, no crossing", CHALK_CYAN),
                    BOARD_CX, 1.62)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "CLOSED + SIMPLE", "a smooth oval",
                                    CHALK_GREEN), BOARD_CX, 0.82)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "NOT SIMPLE", "it crosses itself",
                                    CHALK_PINK), BOARD_CX, 0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "P interior · Q boundary · R exterior",
                                    "inside · on · outside", CHALK_AMBER),
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

            heading = at(board_text("Draw · Classify · Locate", 22, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)

            r1 = at(self.answer_row("1", "DOES IT CLOSE?", "open or closed",
                                    CHALK_CYAN, width=8.60, height=0.62),
                    BOARD_CX, 1.45)
            r2 = at(self.answer_row("2", "DOES IT CROSS ITSELF?",
                                    "simple or not simple", CHALK_GREEN,
                                    width=8.60, height=0.62), BOARD_CX, 0.55)
            r3 = at(self.answer_row("3", "WHERE IS THE POINT?",
                                    "interior · boundary · exterior",
                                    CHALK_AMBER, width=8.60, height=0.62),
                    BOARD_CX, -0.35)
            banner = at(board_text("REGION = INTERIOR + BOUNDARY", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Draw · Classify · Locate", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)
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
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)

            # The closing paragraph is narrated in full before the board gives
            # way: the three rows and the rule line stay up through it, the
            # strip is written on its own bookmark as the voice says "Draw,
            # classify, locate.", and ONLY the bookmark in front of "Thank you
            # for watching," clears the board and brings in the card -- the old
            # cut cleared everything on b4, one phrase early, so the frame
            # jumped ahead of the voice.
            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeOut(heading), FadeOut(r1), FadeOut(r2), FadeOut(r3),
                      FadeOut(banner), FadeOut(strip), run_time=0.55)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.50)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.closing(tracker, thanks, run_time=1.2)
            self._capture_srt(tracker)

        self.wait(END_HOLD)

    # ================================================================ beats ==
    # Angles and parallel lines (Class 8, Chapter 2, "Applications of Angles
    # and Parallel Lines").
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
    #   * the figure is fixed (PAR_Y1/PAR_Y2, TRA_TOP/TRA_BOT) so every scene
    #     draws the same two parallel lines and the same transversal, and the
    #     transversal stops above the banner line so no banner is ever crossed
    #     by a chalk line;
    #   * the eight numbers sit inside their own wedges, on the bisector, clear
    #     of both lines that bound the wedge and of the arc;
    #   * the right-hand column (COL_X) carries the rule of the scene, so no
    #     text has to be written across the figure;
    #   * the challenge uses the series' shared 10-second THINK clock, dead
    #     centre of the board, with the four question cards in the corners.

    def closing(self, tracker, mob=None, color=CHALK_YELLOW, run_time=None):
        """Consume the tail of the narration window on the last reveal."""
        budget = rt(tracker.get_remaining_duration()) if run_time is None \
            else run_time
        if mob is None:
            self.wait(max(budget, 0.0))
        else:
            self.play(Indicate(mob, color=color, scale_factor=1.03),
                      run_time=max(budget, MIN_RT))

    def figure(self, fill=0.10, band_on=False, marks=True, numbers=(),
               num_color=CHALK_WHITE, num_size=15, scale=1.0,
               about=(-1.00, 0.30), hot=(), hot_color=CHALK_YELLOW,
               hot_opacity=0.38):
        """The whole figure: the two parallel lines, the transversal, the eight
        translucent wedges with their arcs, and (optionally) the eight numbers
        and a pair of wedges picked out in one rule colour."""
        grp = VGroup()
        if band_on:
            grp.add(band())
        pair = par_pair()
        tra = transversal()
        grp.add(pair.l1, pair.l2, tra)
        if marks:
            grp.add(pair.marks)
        wedges, arcs = VGroup(), VGroup()
        for n in range(1, 9):
            # Only the *chosen* pair is filled: filling all eight wedges would
            # paint a full disc around each crossing, which hides the very
            # structure this lesson is about.
            if fill > 0:
                wedges.add(angle_sector(n, color=CHALK_CYAN, opacity=fill))
            arcs.add(angle_arc(n, color=CHALK_AMBER, width=2.0))
        for n in hot:
            wedges.add(angle_sector(n, color=hot_color, opacity=hot_opacity))
            arcs.add(angle_arc(n, color=hot_color, width=3.4))
        grp.add(wedges, arcs)
        nums = VGroup()
        for n in numbers:
            x, y = angle_pos(n)
            nums.add(at(board_text(str(n), num_size, num_color, "BOLD"), x, y))
        if len(nums):
            grp.add(nums)
        if scale != 1.0:
            grp.scale(scale, about_point=pt(about))
        grp.pair, grp.tra, grp.wedges, grp.arcs, grp.nums = (pair, tra,
                                                             wedges, arcs, nums)
        return grp

    def numbers(self, ns, color=CHALK_WHITE, size=15, scale=1.0,
                about=(-1.00, 0.30)):
        """The numbers of the given angles, in place."""
        grp = VGroup()
        for n in ns:
            x, y = angle_pos(n)
            grp.add(at(board_text(str(n), size, color, "BOLD"), x, y))
        if scale != 1.0:
            grp.scale(scale, about_point=pt(about))
        return grp

    def highlight(self, ns, color, opacity=0.38, width=3.4, scale=1.0,
                 about=(-1.00, 0.30)):
        """The wedges of the given angles, over-drawn in one rule colour."""
        grp = VGroup()
        for n in ns:
            grp.add(angle_sector(n, color=color, opacity=opacity))
            grp.add(angle_arc(n, color=color, width=width))
        if scale != 1.0:
            grp.scale(scale, about_point=pt(about))
        return grp

    def col_item(self, head, note, color, y, x=COL_X, width=3.20, height=0.92,
                 head_size=15, note_size=13):
        """One row of the right-hand column: a keyword and its note inside one
        card, spaced so no two words on the board come closer than 0.22 units."""
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
        return at(grp, x, y)

    def q_card(self, title, pict, color=CHALK_CYAN, width=3.00, pad=0.12,
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

    def ask_card(self, title, lines, color=CHALK_CYAN, width=3.00, pad=0.12,
                 title_size=13, line_size=12, buff=0.32):
        """A 'your turn' card whose question is written in words."""
        head = board_text(title, title_size, color, "BOLD")
        body = VGroup(*[board_text(line, line_size, CHALK_WHITE, "BOLD")
                        for line in lines]).arrange(DOWN, buff=0.24)
        content = VGroup(head, body).arrange(DOWN, buff=buff)
        box = RoundedRectangle(corner_radius=0.10, width=width,
                               height=content.height + 2 * pad,
                               stroke_color=color, stroke_width=1.9,
                               fill_color=PANEL_FILL, fill_opacity=0.55)
        content.move_to(box.get_center())
        return VGroup(box, content)

    def answer_row(self, tag, headline, note, color, width=8.60, height=0.50):
        """One revealed answer: its letter, the result and a short note."""
        lab = board_text(tag, 16, color, "BOLD")
        name = board_text(headline, 16, color, "BOLD")
        txt = board_text(note, 14, CHALK_WHITE, "BOLD")
        row = VGroup(lab, name, txt).arrange(RIGHT, buff=0.42)
        box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                               stroke_color=color, stroke_width=1.8,
                               fill_color=PANEL_FILL, fill_opacity=0.6)
        row.move_to(box.get_center())
        return VGroup(box, row)

    def rule_row(self, tag, name, note, color, hot, y, width=8.60,
                 height=0.58, pict_scale=0.16):
        """One row of the six-rule recap: the rule's own picture on the left
        (the parallel lines with its pair lit in the rule colour), then the
        number, the name and the equation.

        The picture sits inside the row's own box and is returned inside the
        same VGroup, so the row is one object: the layout audit never reads it
        as a figure drawn behind somebody else's card."""
        pict = self.figure(fill=0.0, marks=False, hot=hot, hot_color=color,
                           scale=pict_scale, about=(-1.00, 0.30))
        tagt = board_text(tag, 15, color, "BOLD")
        nm = board_text(name, 15, color, "BOLD")
        nt = board_text(note, 13, CHALK_WHITE, "BOLD")
        text = VGroup(tagt, nm, nt).arrange(RIGHT, buff=0.30)
        box = RoundedRectangle(corner_radius=0.09, width=width, height=height,
                               stroke_color=color, stroke_width=1.7,
                               fill_color=PANEL_FILL, fill_opacity=0.55)
        box.move_to(np.array([BOARD_CX, float(y), 0.0]))
        pict.move_to(np.array([BOARD_CX - width / 2 + 0.62, float(y), 0.0]))
        text.next_to(pict, RIGHT, buff=0.30)
        text.move_to(np.array([text.get_center()[0], float(y), 0.0]))
        return VGroup(box, pict, text)

    # -- Scene 0: title ------------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = at(board_text("Angles and Parallel Lines", 25, CHALK_PINK,
                                  "BOLD"), BOARD_CX, 2.06)
            sub = at(board_text("When a transversal cuts two parallel lines", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, 1.42)

            fig = self.figure(fill=0.0, scale=0.55, about=(-1.30, 0.10))
            c1 = at(chip("8 ANGLES", CHALK_CYAN, size=15), COL_X, 0.88)
            c2 = at(chip("6 RELATIONSHIPS", CHALK_GREEN, size=15), COL_X, 0.16)
            c3 = at(chip("1 EQUATION", CHALK_YELLOW, size=15), COL_X, -0.56)
            strip = at(board_text("Two parallel lines and a transversal make "
                                  "eight angles.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(title, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(fig), run_time=0.90)
            self.play(FadeIn(c1, scale=0.9), FadeIn(strip, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(c2, scale=0.9), FadeIn(c3, scale=0.9),
                      run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.closing(tracker, c3)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: the lines and the transversal ------------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("Parallel Lines and a Transversal", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Two lines that never meet, cut by one line.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            pair = par_pair()
            tra = transversal()

            arcs = VGroup(*[angle_arc(n, width=2.0) for n in range(1, 9)])

            i1 = self.col_item("PARALLEL LINES", "they never meet", CHALK_WHITE,
                               0.85)
            i2 = self.col_item("TRANSVERSAL", "one line across", CHALK_AMBER,
                               -0.35)

            banner = at(board_text("ONE LINE CROSSES TWO PARALLEL LINES", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("A transversal cutting parallel lines makes "
                                  "eight angles.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(pair.l1), Create(pair.l2),
                      FadeIn(i1, shift=RIGHT * 0.10), run_time=0.70)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(pair.marks), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Create(tra), FadeIn(i2, shift=RIGHT * 0.10),
                      run_time=0.65)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(Create(arcs), run_time=0.70)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: the eight angles and the two regions -----------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("Eight Angles, Two Regions", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Four angles at each crossing.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fig = self.figure(fill=0.0, band_on=False)
            nums_up = self.numbers((1, 2, 3, 4))
            nums_low = self.numbers((5, 6, 7, 8))
            inter = band()

            i1 = self.col_item("INTERIOR", "angles 3, 4, 5, 6", CHALK_GREEN,
                               0.85)
            i2 = self.col_item("EXTERIOR", "angles 1, 2, 7, 8", CHALK_CYAN,
                               -0.35)

            strip = at(board_text("Angles 3, 4, 5 and 6 lie between the parallel "
                                  "lines.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(fig), run_time=0.80)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(nums_up, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(nums_low, scale=0.9), FadeIn(inter),
                      FadeIn(i1, shift=RIGHT * 0.10), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(i2, shift=RIGHT * 0.10),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: vertically opposite and the linear pair --------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Vertically Opposite and Linear Pairs", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("What happens at one crossing.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            v = RULE_COLOR["vertical"]
            fig = self.figure(fill=0.0, numbers=range(1, 9), num_size=14)
            hi1 = self.highlight((1, 4), v)
            hi2 = self.highlight((1, 2), v)
            hi3 = self.highlight((5, 8), v)

            i1 = self.col_item("VERTICALLY OPPOSITE", "angle 1 = angle 4", v,
                               0.85)
            i2 = self.col_item("LINEAR PAIR", "angle 1 + angle 2 = 180", v,
                               -0.35)

            banner = at(board_text("VERTICALLY OPPOSITE ANGLES ARE EQUAL", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Angles on a straight line add up to 180 "
                                  "degrees.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(fig), run_time=0.80)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(hi1), FadeIn(i1, shift=RIGHT * 0.10), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(hi2), FadeIn(i2, shift=RIGHT * 0.10), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(hi3), run_time=0.50)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: corresponding angles ---------------------------------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("Corresponding Angles", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The same position at each crossing.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            c = RULE_COLOR["corresponding"]
            fig = self.figure(fill=0.0, numbers=range(1, 9), num_size=14)
            hi1 = self.highlight((1, 5), c)
            hi2 = self.highlight((2, 6), c)
            hi3 = self.highlight((3, 7, 4, 8), c)

            i1 = self.col_item("1 AND 5", "both at the top left", c, 0.85)
            i2 = self.col_item("2 AND 6", "both at the top right", c, -0.35)

            banner = at(board_text("CORRESPONDING ANGLES ARE EQUAL", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Angle 3 = angle 7, and angle 4 = angle 8.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(fig), run_time=0.80)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(hi1), FadeIn(i1, shift=RIGHT * 0.10), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(hi2), FadeIn(i2, shift=RIGHT * 0.10), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(hi3), run_time=0.55)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: alternate interior angles ----------------------------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("Alternate Interior Angles", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Opposite sides, between the lines.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            c = RULE_COLOR["alt_interior"]
            fig = self.figure(fill=0.0, band_on=True, numbers=range(1, 9),
                              num_size=14)
            hi1 = self.highlight((4, 5), c)
            hi2 = self.highlight((3, 6), c)

            i1 = self.col_item("4 AND 5", "opposite sides, inside", c, 0.85)
            i2 = self.col_item("3 AND 6", "opposite sides, inside", c, -0.35)

            banner = at(board_text("ALTERNATE INTERIOR ANGLES ARE EQUAL", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Both alternate interior pairs are equal.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(fig), run_time=0.80)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(hi1), FadeIn(i1, shift=RIGHT * 0.10), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(hi2), FadeIn(i2, shift=RIGHT * 0.10), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: same-side interior angles ----------------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("Same-Side Interior Angles", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Between the lines, on one side.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            c = RULE_COLOR["same_side_interior"]
            fig = self.figure(fill=0.0, band_on=True, numbers=range(1, 9),
                              num_size=14)
            hi1 = self.highlight((3, 5), c)
            hi2 = self.highlight((4, 6), c)

            i1 = self.col_item("3 AND 5", "angle 3 + angle 5 = 180", c, 0.85)
            i2 = self.col_item("4 AND 6", "angle 4 + angle 6 = 180", c, -0.35)

            banner = at(board_text("SAME-SIDE INTERIOR ANGLES ADD TO 180", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Together they make a straight angle.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(fig), run_time=0.80)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(hi1), FadeIn(i1, shift=RIGHT * 0.10), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(hi2), FadeIn(i2, shift=RIGHT * 0.10),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: the two exterior rules -------------------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Two Exterior Rules", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Outside the parallel lines.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            ca = RULE_COLOR["alt_exterior"]
            cs = RULE_COLOR["same_side_exterior"]
            fig = self.figure(fill=0.0, numbers=range(1, 9), num_size=14)
            hi1 = self.highlight((2, 7), ca)
            hi2 = self.highlight((1, 8), ca)
            hi3 = self.highlight((1, 7), cs)
            hi4 = self.highlight((2, 8), cs)

            i1 = self.col_item("ALTERNATE EXTERIOR", "2 = 7 and 1 = 8", ca, 0.85)
            i2 = self.col_item("SAME-SIDE EXTERIOR", "1 + 7 = 180, 2 + 8 = 180",
                               cs, -0.35)

            banner = at(board_text("EXTERIOR PAIRS: EQUAL OR 180", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Outside the lines: two pairs equal, two pairs "
                                  "180.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(fig), run_time=0.80)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(hi1), FadeIn(i1, shift=RIGHT * 0.10), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(hi2), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(hi3), FadeIn(i2, shift=RIGHT * 0.10), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(hi4), FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: from the rule to a linear equation -------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("From the Rule to an Equation", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Same-side interior angles: they add to 180.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            c = RULE_COLOR["same_side_interior"]
            fig = self.figure(fill=0.0, band_on=True, hot=(3, 5),
                              hot_color=c, numbers=range(1, 9), num_size=14)

            r1 = at(chalk_math(r"(3x + 20) + (5x - 8) = 180", size=26, color=c),
                    COL_X, 1.45)
            r2 = at(chalk_math(r"8x + 12 = 180", size=26, color=CHALK_WHITE),
                    COL_X, 0.80)
            r3 = at(chalk_math(r"8x = 168", size=26, color=CHALK_WHITE),
                    COL_X, 0.15)
            r4 = at(chalk_math(r"x = 21", size=26, color=CHALK_YELLOW),
                    COL_X, -0.50)
            r5 = at(chalk_math(r"83^\circ \text{ and } 97^\circ", size=24,
                               color=c), COL_X, -1.15)

            strip = at(board_text("x = 21, so the angles are 83 and 97 degrees.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(fig), run_time=0.80)

            self.wait(leftover(tracker, "b0"))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(r1, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(r2, scale=0.9), run_time=0.40)
            self.play(FadeIn(r3, scale=0.9), run_time=0.40)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(r4, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(r5, scale=0.9), FadeIn(strip, shift=UP * 0.06),
                      run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 9: the same routine on a second pair --------------------------
    def beat_s9(self) -> None:
        with self.voiceover(text=NARRATION["s9"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Same Routine, Another Pair", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Corresponding angles: the two are equal.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            c = RULE_COLOR["corresponding"]
            fig = self.figure(fill=0.0, numbers=range(1, 9), num_size=14,
                              hot=(1, 5), hot_color=c)

            r1 = at(chalk_math(r"5x = 2x + 24", size=26, color=c), COL_X, 1.45)
            r2 = at(chalk_math(r"3x = 24", size=26, color=CHALK_WHITE), COL_X,
                    0.80)
            r3 = at(chalk_math(r"x = 8", size=26, color=CHALK_YELLOW), COL_X,
                    0.15)
            r4 = at(chalk_math(r"40^\circ \text{ and } 40^\circ", size=24,
                               color=c), COL_X, -0.50)

            banner = at(board_text("EQUAL ANGLES GIVE AN EQUATION", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("x = 8, and both angles are 40 degrees.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(fig), run_time=0.80)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(r1, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(r2, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(r3, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(r4, scale=0.9), FadeIn(strip, shift=UP * 0.06),
                      run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 10: your turn (questions, the silent clock, then the answers) --
    def beat_s9q(self) -> None:
        with self.voiceover(text=NARRATION["s9q"]) as tracker:
            self.reset_board()

            heading = at(board_text("YOUR TURN", 26, CHALK_PINK, "BOLD"),
                         BOARD_CX, 2.78)
            sub = at(board_text("Four quick checks.", 16, CHALK_WHITE, "BOLD"),
                     BOARD_CX, 2.20)

            mini = dict(scale=0.30, about=(-1.00, 0.30), fill=0.0)
            qa = at(self.q_card("same position",
                                self.figure(hot=(1, 5), hot_color=CHALK_YELLOW,
                                            **mini), CHALK_CYAN), -2.80, 0.92)
            qb = at(self.q_card("opposite sides",
                                self.figure(hot=(4, 5), hot_color=CHALK_YELLOW,
                                            **mini), CHALK_CYAN), 3.70, 0.92)
            qc = at(self.q_card("same side",
                                self.figure(hot=(3, 5), hot_color=CHALK_YELLOW,
                                            **mini), CHALK_CYAN), -2.80, -1.02)
            qd = at(self.ask_card("corresponding angles",
                                  ["2x + 10  and  3x - 30", "find x"],
                                  CHALK_PINK, line_size=13), 3.70, -1.02)

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
            a1 = at(self.answer_row("A", "corresponding",
                                    "the pair are equal", CHALK_PINK),
                    BOARD_CX, 1.62)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "alternate interior",
                                    "the pair are equal", CHALK_RED),
                    BOARD_CX, 0.82)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "same-side interior",
                                    "they add to 180 degrees",
                                    RULE_COLOR["same_side_interior"]),
                    BOARD_CX, 0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "x = 40",
                                    "2x + 10 = 3x - 30, so each angle is 90",
                                    CHALK_YELLOW), BOARD_CX, -0.78)
            self.play(FadeIn(a4, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, a4)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 10: the six rules, then the spoken thank-you ------------------
    def beat_s10(self) -> None:
        with self.voiceover(text=NARRATION["s10"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Six Relationships", 22, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)

            rows = [("1", "CORRESPONDING", "angle 1 = angle 5", (1, 5),
                     RULE_COLOR["corresponding"]),
                    ("2", "ALTERNATE INTERIOR", "angle 4 = angle 5", (4, 5),
                     RULE_COLOR["alt_interior"]),
                    ("3", "ALTERNATE EXTERIOR", "angle 2 = angle 7", (2, 7),
                     RULE_COLOR["alt_exterior"]),
                    ("4", "VERTICALLY OPPOSITE", "angle 1 = angle 4", (1, 4),
                     RULE_COLOR["vertical"]),
                    ("5", "SAME-SIDE INTERIOR", "angle 3 + angle 5 = 180",
                     (3, 5), RULE_COLOR["same_side_interior"]),
                    ("6", "SAME-SIDE EXTERIOR", "angle 1 + angle 7 = 180",
                     (1, 7), RULE_COLOR["same_side_exterior"])]
            ys = (2.05, 1.39, 0.73, 0.07, -0.59, -1.25)
            r = [self.rule_row(t, h, n, c, hot, y)
                 for (t, h, n, hot, c), y in zip(rows, ys)]

            strip = at(board_text("Geometry gives the rule, and the equation "
                                  "finds x.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)
            thanks = at(board_text("Thank You for Watching!", 30, CHALK_WHITE,
                                   "BOLD"), BOARD_CX, 0.62)
            bye = at(board_text("See you in the next lesson :)", 22, CHALK_YELLOW,
                                "BOLD"), BOARD_CX, -0.32)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(r[0], shift=UP * 0.06), run_time=0.40)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(r[1], shift=UP * 0.06), run_time=0.35)
            self.play(FadeIn(r[2], shift=UP * 0.06), run_time=0.35)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(r[3], shift=UP * 0.06), run_time=0.40)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(r[4], shift=UP * 0.06), run_time=0.35)
            self.play(FadeIn(r[5], shift=UP * 0.06), run_time=0.35)
            self.add_sound(self.sfx["success"], gain=-11)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeOut(heading), *[FadeOut(x) for x in r],
                      FadeOut(strip), run_time=0.55)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.50)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.closing(tracker, thanks, run_time=1.2)
            self._capture_srt(tracker)

        self.wait(END_HOLD)

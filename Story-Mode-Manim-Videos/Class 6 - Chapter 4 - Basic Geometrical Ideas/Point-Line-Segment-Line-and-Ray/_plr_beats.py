    # ================================================================ beats ==
    # Point, Line Segment, Line & Ray (Class 6 Maths, Chapter 4, Storymode 01).
    #
    # SYNC RULE for every reveal: wait for the narration bookmark that ends the
    # phrase describing a thing, and only then bring it on.  Playing first and
    # waiting afterwards shows the picture a whole window early, which reads as
    # broken sync.
    #
    # Layout rules, so the audits stay clean:
    #   * the heading sits on the board's own heading line (2.72) and its
    #     sub-heading at 2.24, the closing banner at -1.15 and the closing strip
    #     at -1.80 -- nothing at all below CAPTION_SAFE_Y = -2.00;
    #   * every diagram is built centred on the origin and then pinned with
    #     `place_line` / `at`, so a heading, a card and a diagram all share the
    #     board centre and two pictograms on one row line up exactly;
    #   * one row per idea, with at least 0.22 units of clear air between the
    #     ink of neighbouring rows (checked by audit_clearance.py);
    #   * the challenge uses the series' shared 10-second THINK clock, dead
    #     centre of the board, and the four question cards sit in the four
    #     corners so the badge never covers one.
    ROW_Y = 2.72
    SUB_Y = 2.10
    BANNER_Y = -1.15
    STRIP_Y = -1.80

    def closing(self, tracker, mob=None, color=CHALK_YELLOW, run_time=None):
        """Consume the tail of the narration window on the last reveal."""
        budget = rt(tracker.get_remaining_duration()) if run_time is None \
            else run_time
        if mob is None:
            self.wait(max(budget, 0.0))
        else:
            self.play(Indicate(mob, color=color, scale_factor=1.03),
                      run_time=max(budget, MIN_RT))

    def q_card(self, title, pict, color=CHALK_CYAN, width=3.00, pad=0.22,
               title_size=13, buff=0.20):
        """One 'your turn' card: a one-line prompt above its small diagram.

        The box is sized around the finished content, so the clearance between
        the ink and the card's own edge is `pad` by construction.
        """
        head = board_text(title, title_size, color, "BOLD")
        content = VGroup(head, pict).arrange(DOWN, buff=buff)
        box = RoundedRectangle(corner_radius=0.10, width=width,
                               height=content.height + 2 * pad,
                               stroke_color=color, stroke_width=1.9,
                               fill_color=PANEL_FILL, fill_opacity=0.55)
        content.move_to(box.get_center())
        return VGroup(box, content)

    def ask_card(self, title, lines, color=CHALK_CYAN, width=3.00, pad=0.22,
                 title_size=15, line_size=14, buff=0.26):
        """One 'your turn' card that asks its question in words."""
        head = board_text(title, title_size, color, "BOLD")
        body = VGroup(*[board_text(line, line_size, CHALK_WHITE, "BOLD")
                        for line in lines]).arrange(DOWN, buff=0.26)
        content = VGroup(head, body).arrange(DOWN, buff=buff)
        box = RoundedRectangle(corner_radius=0.10, width=width,
                               height=content.height + 2 * pad,
                               stroke_color=color, stroke_width=1.9,
                               fill_color=PANEL_FILL, fill_opacity=0.55)
        content.move_to(box.get_center())
        return VGroup(box, content)

    def answer_row(self, tag, headline, note, color, width=8.60, height=0.62,
                   pad=0.34, buff=0.36):
        """One revealed answer: its letter, the object's name and a short note.

        The row is laid out in FIXED COLUMNS rather than centred in its box:
        every row starts at the box's left edge plus `pad`, then tag, name and
        note follow with one constant `buff` between them.  Centring each row
        put the letter at a different x in every row (the names differ in
        width), so A, B, C and D were not on one vertical line; the box itself
        stays centred on BOARD_CX.
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

            title = at(board_text("Point, Line Segment, Line & Ray", 29,
                                  CHALK_PINK, "BOLD"), BOARD_CX, 1.62)
            sub = at(board_text("The Building Blocks of Geometry", 20,
                                CHALK_WHITE, "BOLD"), BOARD_CX, 0.96)

            specs = (("POINT", "point", "0", CHALK_CYAN),
                     ("SEGMENT", "segment", "2", CHALK_GREEN),
                     ("RAY", "ray", "1", CHALK_YELLOW),
                     ("LINE", "line", "0", CHALK_AMBER))
            # ONE centred row: the four pictograms are all 1.60 wide, so equal
            # centre spacing is also equal air, and row_centres lands the row's
            # ink on the board axis.  (The old columns ran -3.45..+3.45, i.e.
            # they were centred on 0.0, half a unit left of BOARD_CX.)
            xs = row_centres((0.80, 0.80, 0.80, 0.80), 0.70)
            labels, pics, counts = VGroup(), VGroup(), VGroup()
            for x, (name, kind, count, color) in zip(xs, specs):
                labels.add(at(board_text(name, 14, color, "BOLD"), x, 0.26))
                pics.add(place_line(pictogram(kind, width=1.60, color=color,
                                              marks=False, dot_color=color),
                                    x, -0.30))
                counts.add(at(board_text(count, 15, CHALK_WHITE, "BOLD"),
                              x, -0.86))
            strip = at(board_text("Every shape begins with these four ideas.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(title, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(sub, shift=UP * 0.08), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.06) for m in labels],
                                  lag_ratio=0.18), run_time=0.55)
            self.play(LaggedStart(*[FadeIn(m, scale=0.85) for m in pics],
                                  lag_ratio=0.18), run_time=0.60)

            self.wait(leftover(tracker, "b1"))
            self.play(LaggedStart(*[FadeIn(m, scale=0.80) for m in counts],
                                  lag_ratio=0.18), run_time=0.55)
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: geometry is all around us ----------------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("Every Shape Starts with Simple Ideas", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Geometry is all around us.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            # the everyday objects are drawn as real, shaded things (a closed
            # book, a lit screen, a petalled rangoli, a five-pointed star) and
            # the row is centred on the board axis with equal air between the
            # four -- measured, not guessed, because the four icons differ in
            # width (0.6 to 1.0)
            kinds = ("book", "screen", "rangoli", "star")
            icons = [object_icon(k, size=0.72) for k in kinds]
            icon_names = [board_text(k, 15, CHALK_CYAN, "BOLD") for k in kinds]
            xicon = row_centres([max(i.width, n.width) / 2.0
                                 for i, n in zip(icons, icon_names)], 1.30)
            icons_row, names_row = VGroup(), VGroup()
            for x, ic, nm in zip(xicon, icons, icon_names):
                icons_row.add(at(ic, x, 1.28))
                names_row.add(at(nm, x, 0.52))

            # the three reductions below are centred on the same axis, with the
            # tiny "point" column measured by its caption (its ink is one dot)
            lower = (("point", "a point", CHALK_CYAN),
                     ("segment", "a straight piece", CHALK_GREEN),
                     ("ray", "an arrowed path", CHALK_YELLOW))
            raw = [pictogram(kind, width=1.80, color=color, marks=False,
                             dot_color=color) for kind, _, color in lower]
            cap = [board_text(label, 15, CHALK_WHITE, "BOLD")
                   for _, label, _ in lower]
            xlow = row_centres([max(p.width, c.width) / 2.0
                                for p, c in zip(raw, cap)], 1.25)
            pics, labs = VGroup(), VGroup()
            for x, pict, label, (_, _, color) in zip(xlow, raw, cap, lower):
                pics.add(place_line(pict, x, -0.18))
                labs.add(at(label, x, -0.68))
            banner = at(board_text("EVERY SHAPE IS BUILT FROM SIMPLE PIECES", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            # the everyday objects arrive while the voice names them
            self.play(LaggedStart(*[FadeIn(m, scale=0.85) for m in icons_row],
                                  lag_ratio=0.30),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.80, 0.9))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.05)
                                    for m in names_row],
                                  lag_ratio=0.20), run_time=0.50)

            self.wait(leftover(tracker, "b1"))
            self.play(LaggedStart(*[FadeIn(m, scale=0.90) for m in pics],
                                  lag_ratio=0.25), run_time=0.60)
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.05) for m in labs],
                                  lag_ratio=0.25), run_time=0.55)
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            question = at(board_text("What is the simplest thing we can draw?",
                                     18, CHALK_PINK, "BOLD"),
                          BOARD_CX, STRIP_Y)
            self.play(FadeIn(question, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, question)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: a point marks a location -----------------------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("A Point Marks a Location", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Start with the simplest object of all.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # the pencil dot, sharpened smaller and smaller; it stands as the
            # left half of a two-part comparison ("the ink" against "the idea"),
            # so the comparison is centred as ONE block on the board axis (the
            # old pair ran -4.28..+3.55, centred 0.36 left of BOARD_CX)
            dx = 0.85
            shrink = VGroup()
            for i, radius in enumerate((0.145, 0.105, 0.075, 0.052)):
                x = -3.30 + i * 0.70 + dx
                shrink.add(Dot(radius=radius, color=CHALK_WHITE,
                               fill_opacity=1.0).move_to(
                                   np.array([x, 1.25, 0.0])))
            shrink_note = at(board_text("a pencil dot, sharpened and sharpened",
                                        14, CHALK_WHITE, "BOLD"), -2.25 + dx,
                             0.42)
            ideal = dot_point("A", 2.10 + dx, 1.25, CHALK_CYAN)
            ideal_note = at(board_text("a location, with no size at all", 14,
                                       CHALK_WHITE, "BOLD"), 2.10 + dx, 0.42)

            pts = VGroup(*[dot_point(name, x, -0.35, CHALK_CYAN)
                           for name, x in (("A", -2.80), ("B", 0.50),
                                           ("C", 3.80))])

            banner = at(board_text("POINT = A LOCATION", 19, CHALK_YELLOW, "BOLD"),
                        BOARD_CX, BANNER_Y)
            strip = at(board_text("Named with a capital letter: A, B, C.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(m, scale=0.7) for m in shrink],
                                  lag_ratio=0.22), run_time=0.70)
            self.play(FadeIn(shrink_note, shift=UP * 0.05), run_time=0.40)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(ideal, scale=0.85), run_time=0.45)
            self.play(FadeIn(ideal_note, shift=UP * 0.05), run_time=0.40)
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(LaggedStart(*[FadeIn(m, scale=0.8) for m in pts],
                                  lag_ratio=0.25), run_time=0.60)
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: the line segment -------------------------------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Join Two Points: the Line Segment", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Only one of the paths between them is straight.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # The segment IS this scene's picture, so it is centred on the
            # board axis with the ruler directly under it and the "definite
            # length" caption under the ruler.  (The old drawing ran -2.60..1.00
            # at centre -0.80 with its ruler at -1.35, and the caption sat out
            # at +2.35: every row of the frame leaned a different way.)
            seg_len = 3.60
            yseg = 0.75
            xa, xb = BOARD_CX - seg_len / 2.0, BOARD_CX + seg_len / 2.0
            notation = at(chalk_math(r"\overline{AB}", size=34, color=CHALK_GREEN),
                          -1.90, 1.45)
            counter = at(chip("2 ENDPOINTS", CHALK_GREEN), 2.30, 1.45)

            curves = VGroup(curve_path(xa, xb, yseg, 0.30, CHALK_WHITE, 1.8),
                            curve_path(xa, xb, yseg, -0.30, CHALK_WHITE, 1.8),
                            curve_path(xa, xb, yseg, 0.14, CHALK_WHITE, 1.5))
            seg = straight(xa, xb, yseg, CHALK_GREEN)
            pts = pair_dots(xa, xb, yseg, ("A", "B"), CHALK_CYAN)
            ruler_mob = at(ruler(seg_len - 0.20, 0.30), BOARD_CX, -0.10)
            len_note = at(board_text("a definite length", 15, CHALK_AMBER,
                                     "BOLD"), BOARD_CX, -0.58)
            banner = at(board_text("LINE SEGMENT = TWO ENDPOINTS", 19,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The shortest path between A and B.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(notation, scale=0.9), FadeIn(counter, scale=0.9),
                      run_time=0.50)

            # the curved routes are tried, then the straight one wins
            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.25),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.55, 1.0))
            self.play(FadeOut(curves), run_time=0.45)
            self.play(Create(seg), FadeIn(pts), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(ruler_mob, shift=UP * 0.06),
                      FadeIn(len_note, shift=UP * 0.06), run_time=0.50)
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: the line ---------------------------------------------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("Extend Both Ways: the Line", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Past A, past B, and on without stopping.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # A and B are the points left over from the segment, so they stay
            # centred on the board axis and the endless line is drawn
            # symmetrically through them; the endpoint counter is one centred
            # chip.  (The old pair sat at centre -0.60 and the chip was parked
            # out at -3.20, three and a half units off the axis.)
            yline = 1.20
            xa, xb = BOARD_CX - 1.30, BOARD_CX + 1.30
            seg = straight(xa, xb, yline, CHALK_GREEN)
            pts = pair_dots(xa, xb, yline, ("A", "B"), CHALK_CYAN)
            extended = both_way_line(-4.30, 5.30, yline, CHALK_AMBER)
            small_l = at(board_text("l", 22, CHALK_AMBER, "BOLD"), 4.50, 1.62)

            counter_old = at(chip("2 ENDPOINTS", CHALK_GREEN), BOARD_CX, 0.20)
            counter_new = at(chip("NO ENDPOINTS", CHALK_AMBER), BOARD_CX, 0.20)
            note = at(board_text("A and B are points on the line, not endpoints.",
                                 16, CHALK_WHITE, "BOLD"), BOARD_CX, -0.55)
            banner = at(board_text("A LINE HAS NO ENDPOINTS", 19, CHALK_YELLOW,
                                   "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("A line may also be named by a small letter.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(seg), FadeIn(pts), FadeIn(counter_old, scale=0.9),
                      run_time=0.55)

            self.wait(leftover(tracker, "b0"))
            self.play(ReplacementTransform(seg, extended),
                      ReplacementTransform(counter_old, counter_new),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.55, 1.1))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(note, shift=UP * 0.06), run_time=0.45)
            self.play(Indicate(pts, color=CHALK_WHITE, scale_factor=1.05),
                      run_time=0.60)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(small_l, scale=0.85), run_time=0.40)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: the ray ----------------------------------------------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("One Starting Point: the Ray", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The light of a torch begins at one point.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # The ray comes OUT of a real torch: a shaded barrel with grip
            # rings and a switch, a flaring head and a glowing lens, and the
            # translucent beam that widens from that lens -- the ray is drawn
            # inside it, so the picture reads "light starts at one point and
            # spreads in one direction".
            xa, xb, yray = -2.90, 0.60, 1.20
            torch = place_torch(torch_icon(), xa - 0.12, yray)
            # the beam widens to 0.90 at the far end: wide enough to read as
            # light, narrow enough that its edges clear every caption (the
            # letters under A and B sit 0.05-0.13 clear of the lower edge, and
            # the sub-heading 0.09 clear of the upper one)
            light = light_cone(xa - 0.10, 4.95, yray, half0=0.13, half1=0.90)
            beam_start = straight(xa, xb, yray, CHALK_YELLOW)
            beam = ray_line(xa, 4.80, yray, CHALK_YELLOW)
            start_dot = dot_point("A", xa, yray, CHALK_CYAN)
            through_b = dot_point("B", xb, yray, CHALK_CYAN)

            initial = at(board_text("INITIAL POINT", 15, CHALK_PINK, "BOLD"),
                         -1.30, 0.72)
            notation = at(chalk_math(r"\overrightarrow{AB}", size=34,
                                     color=CHALK_YELLOW), -1.70, 0.10)
            counter = at(chip("1 ENDPOINT", CHALK_YELLOW), 1.90, 0.10)
            banner = at(board_text("1 ENDPOINT + 1 ENDLESS DIRECTION", 19,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Sun rays, light rays and torch rays all work "
                                  "this way.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(torch, scale=0.9), FadeIn(start_dot), run_time=0.50)
            self.play(Create(beam_start), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(ReplacementTransform(beam_start, beam), FadeIn(light),
                      FadeIn(through_b), run_time=0.65)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(FadeIn(initial, shift=UP * 0.06), run_time=0.45)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(counter, scale=0.9), run_time=0.45)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(notation, scale=0.9), run_time=0.45)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, notation)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: the endpoint test ------------------------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Endpoint Test", 20, CHALK_AMBER, "BOLD"),
                         BOARD_CX, ROW_Y)
            sub = at(board_text("Count the endpoints: two, one, none.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            rows = (("SEGMENT", "segment", "2 ENDPOINTS", CHALK_GREEN, 1.45,
                     ("A", "B")),
                    ("RAY", "ray", "1 ENDPOINT", CHALK_YELLOW, 0.50, ("R",)),
                    ("LINE", "line", "0 ENDPOINTS", CHALK_AMBER, -0.45,
                     ("S", "T")))
            # ONE centred three-column row -- label | diagram | counter -- with
            # the same 0.75 of air either side of the diagram.  (The old row ran
            # -4.38..+3.24, so its centre sat 1.07 left of the board axis.)
            tags, pics, counts = VGroup(), VGroup(), VGroup()
            for label, kind, count, color, y, nm in rows:
                tags.add(at(board_text(label, 15, color, "BOLD"), -2.70, y))
                pics.add(place_line(pictogram(kind, width=3.00, color=color,
                                              names=nm,
                                              marks=(kind != "line")), 0.10, y))
                counts.add(at(chip(count, color, size=15), 3.30, y))
            banner = at(board_text("2 → SEGMENT   ·   1 → RAY   ·   0 → LINE", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Only the segment has a definite length.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(FadeIn(tags, shift=UP * 0.05), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(pics[0], scale=0.9), FadeIn(counts[0], scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(pics[1], scale=0.9), FadeIn(counts[1], scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(pics[2], scale=0.9), FadeIn(counts[2], scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: points on the same line ------------------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Points on the Same Line", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("C, A and B lie on one straight line.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # C, A and B on one line, the whole diagram centred on the board
            # axis: the line, the three points and the two opposite rays are
            # symmetric about A, and the two ray names sit under the ray tips.
            # (The old line ran -3.40..+3.40 and the points -2.20..+2.00, i.e.
            # centred on 0.0 and -0.10.)  Every letter now sits the one marker
            # offset BELOW its point, as it does in every other scene.
            yline = 1.05
            xc, xa, xb = -1.70, 0.30, 2.50
            base = straight(-2.90, 3.90, yline, CHALK_WHITE, 2.2)
            pts = VGroup(*[dot_point(name, x, yline, color)
                           for name, x, color in (("C", xc, CHALK_CYAN),
                                                  ("A", xa, CHALK_PINK),
                                                  ("B", xb, CHALK_CYAN))])
            # the two rays replace the plain line: one to B, one to C
            ray_ab = ray_line(xa, 3.90, yline, CHALK_CYAN)
            ray_ac = Arrow(np.array([xa, yline, 0.0]),
                           np.array([-2.90, yline, 0.0]), buff=0.0,
                           color=CHALK_PINK, stroke_color=CHALK_PINK,
                           stroke_width=LINE_W, tip_length=0.24,
                           max_tip_length_to_length_ratio=0.30)
            note = at(board_text("Both rays start at A.", 16, CHALK_WHITE, "BOLD"),
                      BOARD_CX, -0.20)
            notation_c = at(chalk_math(r"\overrightarrow{AC}", size=32,
                                       color=CHALK_PINK), -2.90, -0.80)
            notation_b = at(chalk_math(r"\overrightarrow{AB}", size=32,
                                       color=CHALK_CYAN), 3.90, -0.80)
            banner = at(board_text("SAME STRAIGHT LINE", 19, CHALK_YELLOW, "BOLD"),
                        BOARD_CX, BANNER_Y)
            strip = at(board_text("Two rays, one starting point, opposite "
                                  "directions.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(base), run_time=0.55)
            self.play(LaggedStart(*[FadeIn(m, scale=0.8) for m in pts],
                                  lag_ratio=0.25), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.45)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeOut(base), Create(ray_ab), FadeIn(notation_b, scale=0.9),
                      run_time=0.55)
            self.play(Create(ray_ac), FadeIn(notation_c, scale=0.9),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(note, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, note)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: why the order of the letters matters -----------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("Why the Order of Letters Matters", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The first letter names the starting point.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # the three points sit on the ray in the middle of the board, the
            # letters below them at the one marker offset (they used to be
            # labelled from above, the only scene in the video that did)
            yray = 1.45
            xo, xa, xb = -2.10, 0.80, 2.80
            beam = ray_line(xo, 4.80, yray, CHALK_YELLOW)
            pts = VGroup(*[dot_point(name, x, yray, color)
                           for name, x, color in (("O", xo, CHALK_PINK),
                                                  ("A", xa, CHALK_CYAN),
                                                  ("B", xb, CHALK_CYAN))])

            same = at(self.ask_card("ray OA = ray OB",
                                    ["same start, same direction"],
                                    CHALK_GREEN, width=4.20), -1.75, -0.05)
            differ = at(self.ask_card("ray AO is different",
                                      ["the start changes to A"],
                                      CHALK_PINK, width=4.20), 2.75, -0.05)
            banner = at(board_text("THE FIRST LETTER NAMES THE INITIAL POINT",
                                   18, CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Ray AO starts at A, so it is a different ray.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(beam), FadeIn(pts), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Indicate(pts[0], color=CHALK_PINK, scale_factor=1.15),
                      run_time=0.55)
            self.play(FadeIn(same, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Indicate(pts[1], color=CHALK_CYAN, scale_factor=1.15),
                      run_time=0.55)
            self.play(FadeIn(differ, shift=UP * 0.08), run_time=0.50)
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
            sub = at(board_text("Name each object, then answer the last question.",
                                16, CHALK_WHITE, "BOLD"), BOARD_CX, 2.22)

            qa = at(self.q_card("name this object",
                                pictogram("segment", width=1.90, color=CHALK_GREEN,
                                          names=("P", "Q")),
                                CHALK_GREEN), -2.75, 1.25)
            qb = at(self.q_card("name this object",
                                pictogram("ray", width=1.90, color=CHALK_YELLOW,
                                          names=("R",)),
                                CHALK_YELLOW), 3.75, 1.25)
            qc = at(self.q_card("name this object",
                                pictogram("line", width=1.90, color=CHALK_AMBER,
                                          names=("S", "T")),
                                CHALK_AMBER), -2.75, -1.15)
            qd = at(self.ask_card("ray OA", ["can it also be",
                                             "named ray OB?"],
                                  CHALK_CYAN, width=3.00), 3.75, -1.15)

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
            a1 = at(self.answer_row("A", "LINE SEGMENT PQ", "2 endpoints",
                                    CHALK_GREEN), BOARD_CX, 1.62)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "RAY", "1 endpoint", CHALK_YELLOW),
                    BOARD_CX, 0.82)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "LINE", "0 endpoints", CHALK_AMBER),
                    BOARD_CX, 0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "YES — ray OA = ray OB",
                                    "both start at O", CHALK_CYAN),
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

            heading = at(board_text("One Idea, Four Objects", 24, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)

            stages = (("POINT", "point", "marks a location", CHALK_CYAN, ()),
                      ("SEGMENT", "segment", "2 endpoints", CHALK_GREEN,
                       ("A", "B")),
                      ("RAY", "ray", "1 endpoint", CHALK_YELLOW, ("A",)),
                      ("LINE", "line", "0 endpoints", CHALK_AMBER, ()))
            # Four fixed columns centred as ONE block on the board axis (they
            # used to run -3.45..+3.45, i.e. centred on 0.0), every picture
            # letter at the video's one marker offset BELOW its endpoint, and
            # each of the three text rows sitting under its own column -- the
            # last row used to be one centred sentence that belonged to no
            # column in particular.
            xs = [BOARD_CX - 3.45 + i * 2.30 for i in range(4)]
            names, pics, notes, rules = VGroup(), VGroup(), VGroup(), VGroup()
            for x, (label, kind, note, color, marks) in zip(xs, stages):
                names.add(at(board_text(label, 16, color, "BOLD"), x, 1.48))
                pics.add(place_line(pictogram(kind, width=1.70, color=color,
                                              names=marks, marks=False),
                                    x, 0.88))
                notes.add(at(board_text(note, 14, CHALK_WHITE, "BOLD"), x, 0.10))
            for x, entry in zip(xs, ("POINT = LOCATION", "SEGMENT = 2",
                                     "RAY = 1", "LINE = 0")):
                rules.add(at(board_text(entry, 13, CHALK_WHITE, "BOLD"),
                             x, -0.45))
            final = at(board_text("FROM A POINT, GEOMETRY BEGINS", 20,
                                  CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Location → Connection → One Way → Both Ways",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)
            thanks = at(board_text("Thank You for Watching!", 30, CHALK_WHITE,
                                   "BOLD"), BOARD_CX, 0.62)
            bye = at(board_text("See you in the next lesson :)", 22, CHALK_YELLOW,
                                "BOLD"), BOARD_CX, -0.32)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(names[0], shift=UP * 0.06),
                      FadeIn(pics[0], scale=0.9),
                      FadeIn(notes[0], shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(names[1], shift=UP * 0.06),
                      FadeIn(pics[1], scale=0.9),
                      FadeIn(notes[1], shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(names[2], shift=UP * 0.06),
                      FadeIn(pics[2], scale=0.9),
                      FadeIn(notes[2], shift=UP * 0.06),
                      FadeIn(names[3], shift=UP * 0.06),
                      FadeIn(pics[3], scale=0.9),
                      FadeIn(notes[3], shift=UP * 0.06), run_time=0.70)
            self.play(FadeIn(rules, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(final, shift=UP * 0.06), run_time=0.45)

            # the closing card is narrated: it appears as the voice says
            # "Thank you for watching,", the goodbye line as the voice says
            # "and see you in the next lesson."
            self.wait(leftover(tracker, "b4"))
            self.play(FadeOut(heading), FadeOut(names), FadeOut(pics),
                      FadeOut(notes), FadeOut(rules), FadeOut(final),
                      FadeOut(strip), run_time=0.55)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.50)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.closing(tracker, thanks, run_time=1.1)
            self._capture_srt(tracker)

        self.wait(END_HOLD)

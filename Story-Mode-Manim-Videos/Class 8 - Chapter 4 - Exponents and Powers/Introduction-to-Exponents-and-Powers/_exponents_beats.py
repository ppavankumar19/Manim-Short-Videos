    # ================================================================ beats ==
    # Introduction to Exponents & Powers (Class 8, Chapter 4, Storymode 01).
    #
    # SYNC RULE for every reveal: wait for the narration bookmark that ends the
    # phrase describing a thing, and only then bring it on.  Playing first and
    # waiting afterwards shows the picture a whole window early, which reads as
    # broken sync.
    #
    # Layout rules, so the audits stay clean:
    #   * the heading sits on the board's own heading line (2.72), the closing
    #     strip on STRIP_Y (-1.80); nothing at all sits below CAPTION_SAFE_Y;
    #   * two-column work is centred on the board's left and right halves;
    #   * nothing is placed on a line, and no card, tile or chip is placed over
    #     another element -- checked by audit_clearance.py and
    #     audit_sync_overlap.py;
    #   * the challenge uses the series' shared 10-second THINK clock, dead
    #     centre of the board, and the three question cards sit on the LEFT
    #     while it runs so the badge never covers them.
    ROW_Y = 2.72
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

    def rule_row(self, label, detail, color=CHALK_WHITE, width=8.8,
                 height=0.66, size=18):
        """One recap row: a coloured label badge, then what it means."""
        badge = board_text(label, size, color, "BOLD")
        body = board_text(detail, size - 3, CHALK_WHITE, "BOLD")
        row = VGroup(badge, body).arrange(RIGHT, buff=0.34)
        box = RoundedRectangle(corner_radius=0.09, width=width, height=height,
                               stroke_color=color, stroke_width=1.7,
                               fill_color=PANEL_FILL, fill_opacity=0.7)
        row.move_to(box.get_center())
        return VGroup(box, row)

    def q_card(self, title, body, color=CHALK_CYAN, width=3.7, height=0.92):
        """One 'your turn' question card: the prompt over the expression."""
        head = board_text(title, 14, color, "BOLD")
        box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                               stroke_color=color, stroke_width=1.9,
                               fill_color=PANEL_FILL, fill_opacity=0.55)
        head.move_to(box.get_center() + UP * 0.24)
        body.move_to(box.get_center() + DOWN * 0.22)
        return VGroup(box, head, body)

    def answer_row(self, tag, maths, note, color, width=7.6, height=0.70):
        """One revealed answer: its letter, the expression and a short note."""
        lab = board_text(tag, 17, color, "BOLD")
        txt = board_text(note, 16, CHALK_WHITE, "BOLD")
        row = VGroup(lab, maths, txt).arrange(RIGHT, buff=0.40)
        box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                               stroke_color=color, stroke_width=1.8,
                               fill_color=PANEL_FILL, fill_opacity=0.6)
        row.move_to(box.get_center())
        return VGroup(box, row)

    # -- Scene 0: title ------------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            heading = at(board_text("Introduction to Exponents & Powers", 26,
                                    CHALK_WHITE, "BOLD"), BOARD_CX, 2.05)
            sub = at(board_text("Base  \u00b7  Exponent  \u00b7  Power", 20,
                                CHALK_AMBER, "BOLD"), BOARD_CX, 1.40)
            show = at(chalk_math(r"3^6 = 3 \times 3 \times 3 \times 3 "
                                 r"\times 3 \times 3", size=30,
                                 color=CHALK_CYAN), BOARD_CX, 0.52)
            promise = at(board_text("A short way to write repeated "
                                    "multiplication.", 16, CHALK_WHITE, "BOLD"),
                         BOARD_CX, BANNER_Y)
            strip = at(board_text("Exponent notation saves space.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(sub, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(show, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(promise, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, show, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: there must be a shorter way --------------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("There Must Be a Shorter Way", 24,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            chain = at(chain_of(6, "3", CHALK_WHITE, size=26), BOARD_CX, 1.02)
            counts = VGroup(*[
                at(count_badge(i + 1), chain.tiles[i].get_center()[0],
                   chain.tiles[i].get_center()[1] + 0.78)
                for i in range(6)])
            note = at(board_text("Six factors of three, every one written out.",
                                 17, CHALK_WHITE, "BOLD"), BOARD_CX, -0.22)
            question = at(board_text("Do we really need to write three six "
                                     "times?", 19, CHALK_PINK, "BOLD"),
                          BOARD_CX, -0.22)
            result = at(board_text("There must be a shorter way.", 20,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, -1.10)
            strip = at(board_text("Repeated multiplication is long to write.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.06)
                                    for t in chain.tiles], lag_ratio=0.16),
                      run_time=1.0)
            self.play(LaggedStart(*[FadeIn(c, scale=0.7)
                                    for c in chain.crosses], lag_ratio=0.14),
                      run_time=0.6)
            self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in counts],
                                  lag_ratio=0.14), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(note, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b2"))
            self.play(ReplacementTransform(note, question), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            # the compression: ONE three stays behind as the base, the other
            # five leave, and the count rides up into the exponent position
            base = chain.tiles[0]
            self.play(FadeOut(*chain.crosses), FadeOut(*chain.tiles[1:]),
                      FadeOut(counts),
                      base.animate.move_to(np.array([BOARD_CX - 0.24, 1.02,
                                                     0.0])),
                      run_time=0.75)
            sup = board_text("6", 30, CHALK_YELLOW, "BOLD")
            sup.move_to(base.get_corner(UR) + np.array([0.16, 0.05, 0.0]))
            self.play(FadeIn(sup, scale=0.6), FadeIn(result, shift=UP * 0.08),
                      run_time=0.6)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, sup, color=CHALK_YELLOW)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: what the exponent really counts ----------------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("What Does the Exponent Count?", 23,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            chain = at(chain_of(6, "3", CHALK_WHITE, size=24, buff=0.16),
                       BOARD_CX, 1.38)
            counts = VGroup(*[
                at(count_badge(i + 1), chain.tiles[i].get_center()[0],
                   chain.tiles[i].get_center()[1] + 0.72)
                for i in range(6)])
            brace = brace_note(chain, "6 factors", CHALK_CYAN, size=15)
            power = at(chalk_math("3^6", size=54, color=CHALK_WHITE),
                       BOARD_CX, -0.32)
            banner = at(board_text("EXPONENT = NUMBER OF TIMES THE BASE IS "
                                   "USED AS A FACTOR", 16, CHALK_YELLOW,
                                   "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The exponent counts equal factors.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.06)
                                    for t in chain.tiles], lag_ratio=0.14),
                      run_time=0.9)
            self.play(LaggedStart(*[FadeIn(c, scale=0.7)
                                    for c in chain.crosses], lag_ratio=0.12),
                      run_time=0.55)
            # the counter visits the six factors in step with the voice naming
            # them ("three times three times three ... six equal factors"), so
            # it spreads across whatever is left of that phrase's window
            visit_rt = max(tracker.time_until_bookmark("b1") - 0.10, 0.60)
            self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in counts],
                                  lag_ratio=0.16), run_time=min(visit_rt, 3.20))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(brace, shift=DOWN * 0.06), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(power, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(banner, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, power, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: base, exponent and power -----------------------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Base, Exponent and Power", 24,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            big = at(chalk_math("3^6", size=64, color=CHALK_WHITE),
                     BOARD_CX, 1.15)
            base_card = panel("BASE", ["the number that is repeated",
                                       "here it is the 3"],
                              CHALK_CYAN, width=4.1, height=1.40)
            exp_card = panel("EXPONENT", ["how many times it is used",
                                          "here it is the 6"],
                             CHALK_PINK, width=4.1, height=1.40)
            at(base_card, -2.25, -0.15)
            at(exp_card, 3.25, -0.15)
            cards = VGroup(base_card, exp_card)

            p_label = board_text("POWER", 17, CHALK_GREEN, "BOLD")
            p_body = board_text("the whole expression, read as three raised "
                                "to the power six", 15, CHALK_WHITE, "BOLD")
            p_row = VGroup(p_label, p_body).arrange(RIGHT, buff=0.30)
            p_box = RoundedRectangle(corner_radius=0.09,
                                     width=p_row.width + 0.60, height=0.56,
                                     stroke_color=CHALK_GREEN, stroke_width=1.8,
                                     fill_color=PANEL_FILL, fill_opacity=0.7)
            p_row.move_to(p_box.get_center())
            power_card = at(VGroup(p_box, p_row), BOARD_CX, -1.30)
            ring = SurroundingRectangle(base_card, color=CHALK_CYAN, buff=0.05,
                                        corner_radius=0.12, stroke_width=3.0)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(big, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(cards, shift=UP * 0.08), FadeIn(ring),
                      run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(Transform(ring, SurroundingRectangle(
                exp_card, color=CHALK_PINK, buff=0.05, corner_radius=0.12,
                stroke_width=3.0)), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(power_card, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, power_card, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: the power compressor ---------------------------------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Power Compressor", 24, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            comp = at(machine("POWER", "COMPRESSOR", CHALK_CYAN), BOARD_CX,
                      0.95)
            factors = at(chalk_math(r"4 \times 4 \times 4 \times 4 \times 4",
                                    size=26, color=CHALK_WHITE), -2.95, 0.95)
            out = at(chalk_math("4^5", size=48, color=CHALK_YELLOW), 3.55, 0.95)
            arrow_in = Arrow(factors.get_right() + RIGHT * 0.16,
                             comp.get_left() + LEFT * 0.10, buff=0,
                             stroke_width=3.0, color=CHALK_CYAN,
                             max_tip_length_to_length_ratio=0.16)
            arrow_out = Arrow(comp.get_right() + RIGHT * 0.10,
                              out.get_left() + LEFT * 0.16, buff=0,
                              stroke_width=3.0, color=CHALK_YELLOW,
                              max_tip_length_to_length_ratio=0.16)
            count_note = at(board_text("it counts five factors", 15,
                                       CHALK_YELLOW, "BOLD"), BOARD_CX, -0.16)
            expanded = at(chalk_math(r"4 \times 4 \times 4 \times 4 \times 4",
                                     size=22, color=CHALK_YELLOW), 3.55, 0.95)
            banner = at(board_text("COMPRESS  \u2194  EXPAND", 22,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, -0.82)
            strip = at(board_text("Five fours multiplied, or four to the "
                                  "power five.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(comp, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(factors, shift=RIGHT * 0.10),
                      GrowArrow(arrow_in), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(count_note, scale=0.8), GrowArrow(arrow_out),
                      FadeIn(out, shift=LEFT * 0.10), run_time=0.6)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(Transform(out, expanded), FadeOut(arrow_out),
                      FadeOut(count_note), run_time=0.7)
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(banner, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, banner)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: a very important difference --------------------------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("A Very Important Difference", 24,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            l_box = RoundedRectangle(corner_radius=0.10, width=4.3, height=1.9,
                                     stroke_color=CHALK_CYAN, stroke_width=2.0,
                                     fill_color=PANEL_FILL, fill_opacity=0.55)
            l_head = chalk_math("4^5", size=42, color=CHALK_CYAN)
            l_body = chalk_math(r"4 \times 4 \times 4 \times 4 \times 4 = 1024",
                                size=22, color=CHALK_WHITE)
            l_head.move_to(l_box.get_center() + UP * 0.52)
            l_body.move_to(l_box.get_center() + DOWN * 0.36)
            left_card = at(VGroup(l_box, l_head, l_body), -2.15, 0.42)

            r_box = RoundedRectangle(corner_radius=0.10, width=2.9, height=1.9,
                                     stroke_color=CHALK_RED, stroke_width=2.0,
                                     fill_color=PANEL_FILL, fill_opacity=0.55)
            r_head = chalk_math(r"4 \times 5", size=42, color=CHALK_RED)
            r_body = chalk_math("= 20", size=26, color=CHALK_WHITE)
            r_head.move_to(r_box.get_center() + UP * 0.52)
            r_body.move_to(r_box.get_center() + DOWN * 0.36)
            right_card = at(VGroup(r_box, r_head, r_body), 3.45, 0.42)

            neq = at(chalk_math(r"\neq", size=64, color=CHALK_PINK), 1.00, 0.42)
            banner = at(board_text("THE EXPONENT COUNTS FACTORS", 19,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Not the number to multiply by.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(left_card, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(right_card, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(neq, scale=0.7), run_time=0.45)
            self.play(FadeIn(banner, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, neq, color=CHALK_PINK)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: powers of ten ----------------------------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("Powers of Ten", 24, CHALK_AMBER, "BOLD"),
                         BOARD_CX, ROW_Y)
            r1 = at(chalk_math(r"10^1 = 10", size=30, color=CHALK_WHITE),
                    BOARD_CX, 1.62)
            r2 = at(chalk_math(r"10^2 = 10 \times 10 = 100", size=30,
                               color=CHALK_WHITE), BOARD_CX, 1.02)
            r3 = at(chalk_math(r"10^3 = 10 \times 10 \times 10 = 1000", size=30,
                               color=CHALK_WHITE), BOARD_CX, 0.42)
            more = at(chip("+ one more zero", CHALK_CYAN, size=15), 4.20, 0.42)
            r9 = at(chalk_math(r"10^9 = 1000000000", size=34,
                               color=CHALK_YELLOW), BOARD_CX, -0.42)
            note = at(board_text("nine zeros after the one", 16, CHALK_CYAN,
                                 "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Powers of ten write large place values "
                                  "compactly.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(r1, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(r2, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(r3, shift=UP * 0.08), FadeIn(more, scale=0.8),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(r9, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(note, shift=UP * 0.08), run_time=0.4)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, r9, color=CHALK_YELLOW)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: why exponents are useful for large numbers -----------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Why Exponents Are Useful", 24, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sun_grp = at(sun(0.60), -2.95, 1.45)
            sun_lab = at(board_text("the Sun", 17, CHALK_AMBER, "BOLD"),
                         -2.95, 0.36)
            l_box = RoundedRectangle(corner_radius=0.10, width=5.0, height=1.25,
                                     stroke_color=CHALK_RED, stroke_width=2.0,
                                     fill_color=PANEL_FILL, fill_opacity=0.55)
            l_num = board_text("1,40,00,00,000 m", 26, CHALK_WHITE, "BOLD")
            l_note = board_text("long to read, long to write", 15, CHALK_RED,
                                "BOLD")
            l_num.move_to(l_box.get_center() + UP * 0.22)
            l_note.move_to(l_box.get_center() + DOWN * 0.30)
            long_card = at(VGroup(l_box, l_num, l_note), 2.35, 1.45)

            down_arrow = Arrow(np.array([2.35, 0.72, 0.0]),
                               np.array([2.35, 0.20, 0.0]), buff=0,
                               stroke_width=3.0, color=CHALK_GREEN,
                               max_tip_length_to_length_ratio=0.35)
            c_math = chalk_math(r"1.4 \times 10^9", size=44, color=CHALK_GREEN)
            c_unit = board_text("metres", 20, CHALK_WHITE, "BOLD")
            c_row = VGroup(c_math, c_unit).arrange(RIGHT, buff=0.30)
            c_box = RoundedRectangle(corner_radius=0.10,
                                     width=c_row.width + 0.70, height=0.86,
                                     stroke_color=CHALK_GREEN, stroke_width=2.2,
                                     fill_color=PANEL_FILL, fill_opacity=0.6)
            c_row.move_to(c_box.get_center())
            compact = at(VGroup(c_box, c_row), BOARD_CX, -0.42)
            reading = at(board_text("10 raised to the power 9", 16, CHALK_CYAN,
                                    "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The same idea writes the distance to the Sun, "
                                  "or the age of the universe.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(sun_grp, scale=0.85), run_time=0.5)
            self.play(FadeIn(sun_lab, shift=UP * 0.06), run_time=0.35)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(long_card, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(GrowArrow(down_arrow), FadeIn(compact, shift=UP * 0.08),
                      run_time=0.65)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(reading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, compact, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: when numbers grow fast (the chessboard) --------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("When Numbers Grow Fast", 24, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            grid = at(chessboard(2, 6, sq=0.66), BOARD_CX, 1.30)
            grains = VGroup(*[
                at(board_text(g, 13, CHALK_WHITE, "BOLD"),
                   grid.squares[i].get_center()[0], 1.63)
                for i, g in enumerate(("1", "2", "4", "8", "16", "32"))])
            note = at(board_text("every square doubles the one before it", 17,
                                 CHALK_CYAN, "BOLD"), BOARD_CX, 0.28)
            banner = at(board_text("Exponents write that growth compactly.", 19,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, -0.65)
            strip = at(board_text("Doubling again and again grows enormous "
                                  "numbers.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(grid, shift=UP * 0.08), run_time=0.6)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(g, scale=0.7) for g in grains],
                                  lag_ratio=0.22), run_time=1.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(note, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            # the board shrinks away, the way the 64 squares hide the total
            centre = grid.get_center()
            self.play(*[m.animate.scale(0.60, about_point=centre)
                        for m in (grid, *grains)], run_time=0.8)
            self.play(FadeIn(banner, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 9: your turn -- three questions, then the 10-second clock -----
    def beat_s9(self) -> None:
        with self.voiceover(text=NARRATION["s9q"]) as tracker:
            self.reset_board()

            heading = at(board_text("YOUR TURN", 26, CHALK_PINK, "BOLD"),
                         BOARD_CX, 2.78)
            sub = at(board_text("Choose the rule before you calculate.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, 2.24)

            qa = at(self.q_card("Write in exponential form",
                                chalk_math(r"7 \times 7 \times 7 \times 7",
                                           size=20, color=CHALK_WHITE)),
                    -2.55, 1.45)
            qb = at(self.q_card("Expand it",
                                chalk_math("2^5", size=22, color=CHALK_WHITE)),
                    -2.55, 0.31)
            qc = at(self.q_card("Name the base and the exponent",
                                chalk_math("10^6", size=22, color=CHALK_WHITE)),
                    -2.55, -0.83)

            ans_a = at(self.answer_row("A",
                                       chalk_math("7^4", size=30,
                                                  color=CHALK_GREEN),
                                       "four factors of seven", CHALK_GREEN),
                       BOARD_CX, 1.30)
            ans_b = at(self.answer_row("B",
                                       chalk_math(r"2 \times 2 \times 2 \times "
                                                  r"2 \times 2", size=24,
                                                  color=CHALK_YELLOW),
                                       "five twos multiplied", CHALK_YELLOW),
                       BOARD_CX, 0.45)
            ans_c = at(self.answer_row("C",
                                       chalk_math("10^6", size=26,
                                                  color=CHALK_PINK),
                                       "base 10, exponent 6", CHALK_PINK),
                       BOARD_CX, -0.40)
            done = at(board_text("Write  \u2192  Expand  \u2192  Identify", 18,
                                 CHALK_YELLOW, "BOLD"), BOARD_CX, -1.30)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(sub, shift=UP * 0.08), run_time=0.4)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(q, shift=RIGHT * 0.10)
                                    for q in (qa, qb, qc)], lag_ratio=0.22),
                      run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)

            self._capture_srt(tracker)

        # The ten-second THINK pause is deliberately SILENT -- the
        # questions have just been read, so the clock ticks alone, with
        # no narration to sync against.
        play_challenge_countdown(self, seconds=10, sfx=self.sfx,
                                 position=np.array([BOARD_CX, BOARD_CY, 0]))

        with self.voiceover(text=NARRATION["s9a"]) as tracker:

            self.wait(leftover(tracker, "b0"))
            self.play(FadeOut(qa), FadeOut(qb), FadeOut(qc), run_time=0.5)
            self.play(FadeIn(ans_a, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(ans_b, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(ans_c, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(done, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, done)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap -----------------------------------------------------
    def beat_s10(self) -> None:
        with self.voiceover(text=NARRATION["s10"]) as tracker:
            self.reset_board()

            heading = at(board_text("Base  \u00b7  Exponent  \u00b7  Power", 24,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            rows = VGroup(
                self.rule_row("BASE", "the number that is repeated  "
                              "(3 in three to the power six)", CHALK_CYAN),
                self.rule_row("EXPONENT", "how many times it is used  "
                              "(6 in three to the power six)", CHALK_PINK),
                self.rule_row("POWER", "the compact expression for it all",
                              CHALK_GREEN),
            )
            at(rows[0], BOARD_CX, 1.55)
            at(rows[1], BOARD_CX, 0.70)
            at(rows[2], BOARD_CX, -0.15)
            final = at(board_text("Exponents make repeated multiplication "
                                  "short.", 20, CHALK_YELLOW, "BOLD"),
                       BOARD_CX, BANNER_Y)
            strip = at(board_text("BASE and REPEAT COUNT give the POWER "
                                  "NOTATION.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            thanks = at(board_text("Thank You for Watching!", 30, CHALK_WHITE,
                                   "BOLD"), BOARD_CX, 0.62)
            bye = at(board_text("See you in the next lesson :)", 22,
                                CHALK_YELLOW, "BOLD"), BOARD_CX, -0.32)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(rows[0], shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(rows[1], shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(rows[2], shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(final, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["success"], gain=-11)

            # the closing card is narrated: it appears as the voice says
            # "Thank you for watching,", and the goodbye line as the voice
            # says "and see you in the next lesson."
            self.wait(leftover(tracker, "b3"))
            self.play(FadeOut(heading), FadeOut(rows[0]), FadeOut(rows[1]),
                      FadeOut(rows[2]), FadeOut(final), FadeOut(strip),
                      run_time=0.5)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.5)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.closing(tracker, thanks, run_time=1.2)
            self._capture_srt(tracker)

        self.wait(END_HOLD)




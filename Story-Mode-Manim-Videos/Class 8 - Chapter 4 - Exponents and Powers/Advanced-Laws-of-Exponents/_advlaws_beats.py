    # ================================================================ beats ==
    # Advanced Laws of Exponents (Class 8, Chapter 4, Storymode 04).
    #
    # SYNC RULE for every reveal: wait for the narration bookmark that ends the
    # phrase describing a thing, and only then bring it on.  Playing first and
    # waiting afterwards shows the picture a whole window early, which reads as
    # broken sync.
    #
    # Layout rules, so the audits stay clean:
    #   * the heading sits on ROW_Y (2.72), the closing strip on STRIP_Y (-1.80);
    #     nothing at all sits below y = -2.00;
    #   * the visual identity is "the exponent knows what is inside the brackets":
    #     the outer exponent duplicates the whole group, splits horizontally over
    #     a product, splits vertically over a fraction, and the zero-exponent
    #     scene reuses storymode 03's cancellation;
    #   * nothing is placed on a line, and no card, tile or chip is placed over
    #     another element -- checked by audit_clearance.py and
    #     audit_sync_overlap.py;
    #   * the challenge uses the series' shared 10-second THINK clock, dead
    #     centre of the board, with the question cards on the LEFT while it runs.
    ROW_Y = 2.72
    BANNER_Y = -1.30
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

    def chain_positions(self, n, y, cx=None):
        """The x centres of an n-tile chain centred on the board."""
        cx = BOARD_CX if cx is None else cx
        width = n * TILE_W + (n - 1) * TILE_BUFF
        x0 = cx - width / 2.0 + TILE_W / 2.0
        return [np.array([x0 + i * (TILE_W + TILE_BUFF), y, 0.0])
                for i in range(n)]

    # -- Scene 0: title ------------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            heading = at(board_text("Advanced Laws of Exponents", 26,
                                    CHALK_WHITE, "BOLD"), BOARD_CX, 2.15)
            sub = at(board_text("Power of a Power  \u00b7  Product  \u00b7  "
                                "Fraction  \u00b7  Zero", 16, CHALK_AMBER,
                                "BOLD"), BOARD_CX, 1.50)
            laws = VGroup(
                at(chalk_math(r"(a^m)^n = a^{mn}", size=28, color=CHALK_CYAN),
                   GRID_X[0], 0.85),
                at(chalk_math(r"(ab)^m = a^m b^m", size=28,
                              color=CHALK_YELLOW), GRID_X[1], 0.85),
                at(chalk_math(r"(a/b)^m = a^m/b^m", size=28, color=CHALK_PINK),
                   GRID_X[0], -0.15),
                at(chalk_math(r"a^0 = 1", size=28, color=CHALK_GREEN),
                   GRID_X[1], -0.15),
            )
            promise = at(board_text("See the structure, then choose the law.",
                                    16, CHALK_WHITE, "BOLD"),
                         BOARD_CX, -1.05)
            strip = at(board_text("Four new laws, four different structures.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(sub, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.08) for m in laws],
                                  lag_ratio=0.25), run_time=1.1)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(promise, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, laws, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: one chapter, different structures ---------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("Same Exponents, Different Structures", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            same_base = at(law_card(chalk_math(r"a^m \times a^n", size=28,
                                               color=CHALK_WHITE),
                                    "video 3: same-base product", CHALK_WHITE,
                                    width=4.0, height=1.40),
                           GRID_X[0], 1.45)
            power = at(law_card(chalk_math(r"(a^m)^n", size=28,
                                           color=CHALK_CYAN),
                                "power of a power", CHALK_CYAN,
                                width=4.0, height=1.40),
                       GRID_X[1], 1.45)
            product = at(law_card(chalk_math(r"(ab)^m", size=28,
                                             color=CHALK_YELLOW),
                                  "power of a product", CHALK_YELLOW,
                                  width=4.0, height=1.40),
                         GRID_X[0], -0.15)
            fraction = at(law_card(chalk_math(r"(a/b)^m", size=28,
                                              color=CHALK_PINK),
                                   "power of a fraction", CHALK_PINK,
                                   width=4.0, height=1.40),
                          GRID_X[1], -0.15)
            query = at(chalk_math("?", size=40, color=CHALK_PINK),
                       BOARD_CX, 1.45)
            banner = at(board_text("First recognise the structure.", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The shape decides the rule.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(same_base, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(power, shift=UP * 0.08), FadeIn(query, scale=0.7),
                      run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(product, shift=UP * 0.08),
                      FadeIn(fraction, shift=UP * 0.08), run_time=0.6)
            self.play(FadeIn(banner, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: power of a power -- the groups duplicate -------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("Groups \u00d7 Factors in Each Group", 21,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            start = at(chalk_math(r"(2^3)^2", size=38, color=CHALK_WHITE),
                       BOARD_CX, 1.95)
            run_a, tiles_a = tile_run(3, "2", CHALK_CYAN)
            run_b, tiles_b = tile_run(3, "2", CHALK_PINK)
            at(run_a, -0.75, 1.10)
            at(run_b, 1.75, 1.10)
            lab_a = at(board_text("3 factors", 14, CHALK_CYAN, "BOLD"),
                       -2.75, 1.10)
            lab_b = at(board_text("3 factors", 14, CHALK_PINK, "BOLD"),
                       3.75, 1.10)
            maths = at(chalk_math(r"2 \times 3 = 6", size=26, color=CHALK_YELLOW),
                       BOARD_CX, 0.25)
            groups = at(chip("2 groups \u00d7 3 factors", CHALK_CYAN, size=15),
                        3.60, 0.25)
            law = at(card(chalk_math(r"(a^m)^n = a^{mn}", size=32,
                                     color=CHALK_GREEN), CHALK_GREEN),
                     BOARD_CX, -0.80)
            strip = at(board_text("POWER OF A POWER \u2014 MULTIPLY THE "
                                  "EXPONENTS.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(start, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(run_a, shift=UP * 0.08), FadeIn(lab_a),
                      run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(run_b, shift=UP * 0.08), FadeIn(lab_b),
                      run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            targets = self.chain_positions(6, 1.10)
            self.play(*[t.animate.move_to(p) for t, p in
                        zip(list(tiles_a) + list(tiles_b), targets)],
                      FadeOut(lab_a), FadeOut(lab_b), run_time=0.8)
            self.play(FadeIn(maths, shift=UP * 0.08), FadeIn(groups, scale=0.85),
                      run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(law, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, law, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: the general power-of-a-power law ---------------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Multiply the Exponents", 23, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            start = at(chalk_math(r"(a^m)^n", size=54, color=CHALK_WHITE),
                       BOARD_CX, 1.85)
            copies = at(chip("n copies of a to the power m", CHALK_CYAN,
                             size=16), BOARD_CX, 0.95)
            added = at(chalk_math(r"m + m + \cdots + m = mn", size=32,
                                  color=CHALK_YELLOW), BOARD_CX, 0.00)
            law = at(card(chalk_math(r"(a^m)^n = a^{mn}", size=32,
                                     color=CHALK_GREEN), CHALK_GREEN),
                     BOARD_CX, -1.00)
            mult = at(chip("multiply, never add", CHALK_GREEN, size=15),
                      3.85, -1.00)
            strip = at(board_text("NEVER ADD THE EXPONENTS HERE.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(start, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(copies, scale=0.85), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(added, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(law, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(mult, scale=0.85), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, law, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: power of a product -- the exponent splits horizontally -----
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Exponent Reaches Every Factor", 21,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            start = at(chalk_math(r"(2 \times 3)^4", size=38, color=CHALK_WHITE),
                       BOARD_CX, 2.00)
            copies = at(chalk_math(r"(2 \times 3)(2 \times 3)(2 \times 3)"
                                   r"(2 \times 3)", size=24, color=CHALK_WHITE),
                        BOARD_CX, 1.10)
            twos = at(chalk_math(r"2 \times 2 \times 2 \times 2 = 2^4", size=28,
                                 color=CHALK_CYAN), BOARD_CX, 0.40)
            threes = at(chalk_math(r"3 \times 3 \times 3 \times 3 = 3^4", size=28,
                                   color=CHALK_PINK), BOARD_CX, -0.30)
            law = at(card(chalk_math(r"(ab)^m = a^m b^m", size=32,
                                     color=CHALK_GREEN), CHALK_GREEN),
                     BOARD_CX, -1.30)
            dist = at(chip("distribute the power", CHALK_GREEN, size=15),
                      3.90, -1.30)
            strip = at(board_text("THE OUTER EXPONENT APPLIES TO BOTH.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(start, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(copies, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(twos, shift=UP * 0.08),
                      FadeIn(threes, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(law, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(dist, scale=0.85), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, law, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: power of a fraction -- the exponent splits vertically ------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("Power the Top and the Bottom", 21,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            start = at(chalk_math(r"(2/5)^3", size=44, color=CHALK_WHITE),
                       BOARD_CX, 1.85)
            law = at(law_card(chalk_math(r"(a/b)^m = a^m/b^m", size=24,
                                         color=CHALK_GREEN),
                              "top and bottom", CHALK_GREEN,
                              width=2.60, height=1.00), 3.85, 1.85)
            copies = at(chalk_math(r"(2/5) \times (2/5) \times (2/5)", size=30,
                                   color=CHALK_WHITE), BOARD_CX, 0.80)
            grouped = at(chalk_math(r"\frac{2 \times 2 \times 2}{5 \times 5 "
                                    r"\times 5} = \frac{2^3}{5^3}", size=28,
                                    color=CHALK_CYAN), BOARD_CX, -0.55)
            strip = at(board_text("POWER THE NUMERATOR AND THE DENOMINATOR.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(start, shift=UP * 0.08),
                      FadeIn(law, scale=0.9), run_time=0.6)
            self.play(FadeIn(copies, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(grouped, shift=UP * 0.08), run_time=0.65)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, grouped, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: why a non-zero number to the power zero is one -------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("Zero Exponent Does Not Mean Zero", 21,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            one = at(chalk_math(r"\frac{a^4}{a^4} = 1", size=34,
                                color=CHALK_GREEN), BOARD_CX, 1.70)
            quotient = at(chalk_math(r"\frac{a^4}{a^4} = a^{4-4} = a^0",
                                     size=32, color=CHALK_CYAN),
                          BOARD_CX, 0.45)
            minus = at(chalk_math(r"4 - 4 = 0", size=30, color=CHALK_YELLOW),
                       BOARD_CX, -0.45)
            law = at(law_card(chalk_math("a^0 = 1", size=30, color=CHALK_GREEN),
                              "for any non-zero a", CHALK_GREEN,
                              width=4.00, height=1.05, math_up=0.26,
                              note_down=0.32), BOARD_CX, -1.40)
            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(one, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(quotient, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(minus, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(law, scale=0.9), run_time=0.5)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, law, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: which law should I use? ------------------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Structure Chooses the Law", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            lanes = VGroup(
                at(law_card(chalk_math(r"(a^m)^n", size=28, color=CHALK_CYAN),
                            "power on power \u2192 multiply", CHALK_CYAN),
                   GRID_X[0], GRID_Y[0]),
                at(law_card(chalk_math(r"(ab)^m", size=28,
                                       color=CHALK_YELLOW),
                            "product \u2192 distribute", CHALK_YELLOW),
                   GRID_X[1], GRID_Y[0]),
                at(law_card(chalk_math(r"(a/b)^m", size=28, color=CHALK_PINK),
                            "fraction \u2192 top and bottom", CHALK_PINK),
                   GRID_X[0], GRID_Y[1]),
                at(law_card(chalk_math(r"a^0", size=28, color=CHALK_GREEN),
                            "zero exponent \u2192 one", CHALK_GREEN),
                   GRID_X[1], GRID_Y[1]),
            )
            strip = at(board_text("RECOGNISE FIRST, THEN APPLY.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(lanes[0], shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(lanes[1], shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(lanes[2], shift=UP * 0.08),
                      FadeIn(lanes[3], shift=UP * 0.08), run_time=0.6)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, lanes, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: four mistakes to avoid -------------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("Don't Mix the Rules", 22, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            arrow = board_text("\u2192", 20, CHALK_WHITE, "BOLD")
            row1 = at(card(VGroup(
                chalk_math(r"(x^2)^3 = x^{2+3} = x^5", size=24,
                           color=CHALK_RED),
                mark_no(0.85),
                arrow.copy(),
                chalk_math(r"x^6", size=26, color=CHALK_GREEN)
            ).arrange(RIGHT, buff=0.36), CHALK_RED, pad_y=0.22),
                BOARD_CX, 1.85)
            row2 = at(card(VGroup(
                chalk_math(r"(ab)^3 = a^3 b", size=24, color=CHALK_RED),
                mark_no(0.85),
                arrow.copy(),
                chalk_math(r"a^3 b^3", size=26, color=CHALK_GREEN)
            ).arrange(RIGHT, buff=0.36), CHALK_RED, pad_y=0.22),
                BOARD_CX, 1.00)
            row3 = at(card(VGroup(
                chalk_math(r"(a/b)^2 = a^2/b", size=24, color=CHALK_RED),
                mark_no(0.85),
                arrow.copy(),
                chalk_math(r"a^2/b^2", size=26, color=CHALK_GREEN)
            ).arrange(RIGHT, buff=0.36), CHALK_RED, pad_y=0.22),
                BOARD_CX, -0.05)
            row4 = at(card(VGroup(
                chalk_math(r"7^0 = 0", size=24, color=CHALK_RED),
                mark_no(0.85),
                arrow.copy(),
                chalk_math(r"1", size=26, color=CHALK_GREEN)
            ).arrange(RIGHT, buff=0.36), CHALK_RED, pad_y=0.22),
                BOARD_CX, -1.05)
            strip = at(board_text("LOOK AT THE WHOLE EXPRESSION.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(row1, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(row2, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(row3, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(row4, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 9: your turn -- four questions, then the 10-second clock ------
    def beat_s9(self) -> None:
        with self.voiceover(text=NARRATION["s9q"]) as tracker:
            self.reset_board()

            heading = at(board_text("YOUR TURN", 26, CHALK_PINK, "BOLD"),
                         BOARD_CX, ROW_Y)
            qa = at(q_card("power of a power",
                           chalk_math(r"(3^4)^2", size=20, color=CHALK_WHITE),
                           height=0.92, head_up=0.28, body_down=0.22),
                    -2.55, 1.45)
            qb = at(q_card("power of a product",
                           chalk_math(r"(5x)^3", size=20, color=CHALK_WHITE),
                           height=0.92, head_up=0.28, body_down=0.22),
                    3.55, 1.45)
            qc = at(q_card("power of a fraction",
                           chalk_math(r"(3/7)^2", size=20, color=CHALK_WHITE),
                           height=0.92, head_up=0.28, body_down=0.22),
                    -2.55, 0.20)
            qd = at(q_card("zero exponent",
                           chalk_math(r"(-6)^0", size=20, color=CHALK_WHITE),
                           height=0.92, head_up=0.28, body_down=0.22),
                    3.55, 0.20)

            ans_a = at(answer_row("A",
                                  chalk_math(r"(3^4)^2 = 3^{8}", 28,
                                             color=CHALK_CYAN),
                                  "multiply the exponents", CHALK_CYAN),
                       BOARD_CX, 1.55)
            ans_b = at(answer_row("B",
                                  chalk_math(r"(5x)^3 = 5^3 x^3", 28,
                                             color=CHALK_YELLOW),
                                  "distribute the power", CHALK_YELLOW),
                       BOARD_CX, 0.70)
            ans_c = at(answer_row("C",
                                  chalk_math(r"(3/7)^2 = 3^2/7^2 = 9/49", 28,
                                             color=CHALK_PINK),
                                  "top and bottom", CHALK_PINK),
                       BOARD_CX, -0.15)
            ans_d = at(answer_row("D",
                                  chalk_math(r"(-6)^0 = 1", 28,
                                             color=CHALK_GREEN),
                                  "zero exponent", CHALK_GREEN),
                       BOARD_CX, -1.00)
            done = at(board_text("RECOGNISE FIRST, SIMPLIFY SECOND.", 18,
                                 CHALK_YELLOW, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.5)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(q, shift=RIGHT * 0.10)
                                    for q in (qa, qb, qc, qd)],
                                  lag_ratio=0.20), run_time=1.0)
            self.add_sound(self.sfx["pop"], gain=-13)

            self._capture_srt(tracker)

        # The ten-second THINK pause is deliberately SILENT -- the
        # questions have just been read, so the clock ticks alone, with
        # no narration to sync against.
        play_challenge_countdown(self, seconds=10, sfx=self.sfx,
                                 position=np.array([BOARD_CX, BOARD_CY, 0]))

        with self.voiceover(text=NARRATION["s9a"]) as tracker:

            self.wait(leftover(tracker, "b0"))
            self.play(FadeOut(qa), FadeOut(qb), FadeOut(qc), FadeOut(qd),
                      run_time=0.5)
            self.play(FadeIn(ans_a, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(ans_b, shift=UP * 0.08),
                      FadeIn(ans_c, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(ans_d, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(done, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, done)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap -----------------------------------------------------
    def beat_s10(self) -> None:
        with self.voiceover(text=NARRATION["s10"]) as tracker:
            self.reset_board()

            heading = at(board_text("Recognise \u2192 Apply \u2192 Simplify", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            lanes = VGroup(
                at(law_card(chalk_math(r"(a^m)^n = a^{mn}", size=24,
                                       color=CHALK_CYAN),
                            "power on power \u2192 multiply", CHALK_CYAN),
                   GRID_X[0], GRID_Y[0]),
                at(law_card(chalk_math(r"(ab)^m = a^m b^m", size=24,
                                       color=CHALK_YELLOW),
                            "product \u2192 distribute", CHALK_YELLOW),
                   GRID_X[1], GRID_Y[0]),
                at(law_card(chalk_math(r"(a/b)^m = a^m/b^m", size=24,
                                       color=CHALK_PINK),
                            "fraction \u2192 top and bottom", CHALK_PINK),
                   GRID_X[0], GRID_Y[1]),
                at(law_card(chalk_math("a^0 = 1", size=24, color=CHALK_GREEN),
                            "zero exponent \u2192 one", CHALK_GREEN),
                   GRID_X[1], GRID_Y[1]),
            )
            strip = at(board_text("SEE THE STRUCTURE, THEN CHOOSE THE LAW.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            thanks = at(board_text("Thank You for Watching!", 30, CHALK_WHITE,
                                   "BOLD"), BOARD_CX, 0.62)
            bye = at(board_text("See you in the next lesson :)", 22,
                                CHALK_YELLOW, "BOLD"), BOARD_CX, -0.32)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(lanes[0], shift=UP * 0.08),
                      FadeIn(lanes[1], shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(lanes[2], shift=UP * 0.08),
                      FadeIn(lanes[3], shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["success"], gain=-11)

            # the closing card is narrated: it appears as the voice says
            # "Thank you for watching,", the goodbye line as the voice says
            # "and see you in the next lesson."
            self.wait(leftover(tracker, "b3"))
            self.play(FadeOut(heading), FadeOut(lanes), FadeOut(strip),
                      run_time=0.5)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.5)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.closing(tracker, thanks, run_time=1.2)
            self._capture_srt(tracker)

        self.wait(END_HOLD)



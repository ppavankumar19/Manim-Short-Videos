    # ================================================================ beats ==
    # Product & Quotient Laws of Exponents (Class 8, Chapter 4, Storymode 03).
    #
    # SYNC RULE for every reveal: wait for the narration bookmark that ends the
    # phrase describing a thing, and only then bring it on.  Playing first and
    # waiting afterwards shows the picture a whole window early, which reads as
    # broken sync.
    #
    # Layout rules, so the audits stay clean:
    #   * the heading sits on ROW_Y (2.72), the closing strip on STRIP_Y (-1.80);
    #     nothing at all sits below y = -2.00;
    #   * the FACTOR BLOCKS are the same mobjects throughout -- the two groups
    #     physically slide together for the product, and the matched tiles are
    #     slashed and removed for the quotient (no clear-and-redraw);
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

            heading = at(board_text("Product & Quotient Laws", 28, CHALK_WHITE,
                                    "BOLD"), BOARD_CX, 2.20)
            sub = at(board_text("Multiplying and Dividing Powers with the Same "
                                "Base", 17, CHALK_AMBER, "BOLD"),
                     BOARD_CX, 1.55)
            law1 = at(chalk_math(r"a^m \times a^n = a^{m+n}", size=38,
                                 color=CHALK_CYAN), BOARD_CX, 0.78)
            law2 = at(chalk_math(r"\frac{a^m}{a^n} = a^{m-n}", size=38,
                                 color=CHALK_YELLOW), BOARD_CX, -0.18)
            promise = at(board_text("Same base: the exponents do the "
                                    "arithmetic.", 16, CHALK_WHITE, "BOLD"),
                         BOARD_CX, -1.15)
            strip = at(board_text("Multiply  \u2192  add;   divide  \u2192  "
                                  "subtract.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(sub, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(law1, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(promise, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(law2, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, law1, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: expanding everything gets messy ----------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("There Must Be a Faster Way", 24,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            start = at(chalk_math(r"2^4 \times 2^3", size=44,
                                  color=CHALK_WHITE), BOARD_CX, 1.60)
            expand = at(chalk_math(r"2 \times 2 \times 2 \times 2 \times 2 "
                                   r"\times 2 \times 2", size=26,
                                   color=CHALK_WHITE), BOARD_CX, 0.60)
            joined = at(chalk_math("2^7", size=48, color=CHALK_YELLOW),
                        BOARD_CX, -0.40)
            banner = at(board_text("There must be a shortcut.", 20,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Expanding everything every time is slow.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(start, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(expand, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(ReplacementTransform(expand, joined), run_time=0.7)
            self.play(FadeIn(banner, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, joined, color=CHALK_YELLOW)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: why product exponents add (the factor blocks join) ---------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("Multiplication Joins Factors", 24,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            run_a, tiles_a = tile_run(4, "2", CHALK_CYAN)
            run_b, tiles_b = tile_run(3, "2", CHALK_PINK)
            cross = chalk_math(r"\times", size=30, color=CHALK_WHITE)
            row = at(VGroup(run_a, cross, run_b).arrange(RIGHT, buff=0.40),
                     BOARD_CX, 1.28)
            lab_a = at(board_text("4 factors", 15, CHALK_CYAN, "BOLD"),
                       run_a.get_center()[0], 1.86)
            lab_b = at(board_text("3 factors", 15, CHALK_PINK, "BOLD"),
                       run_b.get_center()[0], 1.86)
            plus = at(board_text("4 + 3 = 7", 19, CHALK_YELLOW, "BOLD"),
                      BOARD_CX, 1.86)
            power = at(chalk_math(r"2^{4+3} = 2^{7}", size=36,
                                  color=CHALK_GREEN), BOARD_CX, 0.28)
            law = at(card(chalk_math(r"a^m \times a^n = a^{m+n}", size=34,
                                     color=CHALK_GREEN), CHALK_GREEN),
                     BOARD_CX, -1.00)
            strip = at(board_text("KEEP THE BASE \u2014 ADD THE EXPONENTS.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(run_a, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(cross, scale=0.8), run_time=0.35)
            self.play(FadeIn(run_b, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(lab_a), FadeIn(lab_b), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            all_tiles = list(tiles_a) + list(tiles_b)
            targets = self.chain_positions(7, 1.28)
            self.play(*[t.animate.move_to(p)
                        for t, p in zip(all_tiles, targets)],
                      FadeOut(cross), FadeOut(lab_a), FadeOut(lab_b),
                      run_time=0.9)
            self.play(FadeIn(plus, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeOut(plus),
                      FadeIn(power, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(law, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, law, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: the product law with a negative exponent -------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Keep the Base, Add the Exponents", 23,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            start = at(chalk_math(r"3^2 \times 3^{-4}", size=44,
                                  color=CHALK_WHITE), BOARD_CX, 1.60)
            same = at(chip("the same base", CHALK_GREEN, size=15), 3.85, 1.60)
            add = at(chalk_math(r"2 + (-4) = -2", size=40, color=CHALK_YELLOW),
                     BOARD_CX, 0.75)
            result = at(card(chalk_math(r"3^2 \times 3^{-4} = 3^{-2}", size=38,
                                        color=CHALK_GREEN), CHALK_GREEN),
                        BOARD_CX, -0.10)
            back = at(chalk_math(r"3^{-2} = 1/3^2 = 1/9", size=30,
                                 color=CHALK_CYAN), BOARD_CX, -1.15)
            strip = at(board_text("The law holds for integer exponents.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(start, shift=UP * 0.08),
                      FadeIn(same, scale=0.8), run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(add, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(result, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(back, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, back, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: why quotient exponents subtract (the factors cancel) -------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("Division Cancels Matching Factors", 23,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            top, top_tiles = tile_run(7, "a", CHALK_WHITE)
            bot, bot_tiles = tile_run(3, "a", CHALK_WHITE)
            at(top, BOARD_CX, 1.55)
            at(bot, bot_tiles[1].get_center()[0], 0.62)
            bar = frac_bar(top.get_left()[0] - 0.10, top.get_right()[0] + 0.10,
                           1.08)
            marks = VGroup(*[cancel_mark(t)
                             for t in (top_tiles[0], top_tiles[1],
                                       top_tiles[2])],
                           *[cancel_mark(t) for t in bot_tiles])
            left_label = at(board_text("7 factors", 15, CHALK_CYAN, "BOLD"),
                            -2.95, 1.55)
            below_label = at(board_text("3 factors", 15, CHALK_PINK, "BOLD"),
                             -2.95, 0.62)
            minus = at(board_text("7 - 3 = 4", 19, CHALK_YELLOW, "BOLD"),
                       3.55, 0.20)
            law = at(card(chalk_math(r"\frac{a^m}{a^n} = a^{m-n}", size=34,
                                     color=CHALK_PINK), CHALK_PINK),
                     BOARD_CX, -0.90)
            strip = at(board_text("DIVISION CANCELS MATCHING FACTORS.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(top, shift=UP * 0.08), run_time=0.6)
            self.play(FadeIn(bar), FadeIn(bot, shift=DOWN * 0.08),
                      run_time=0.55)
            self.play(FadeIn(left_label), FadeIn(below_label), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            # the matched factors go label-first, so the slash crosses an empty
            # block rather than running through the glyph
            self.play(*[FadeOut(t.label) for t in
                        (top_tiles[0], top_tiles[1], top_tiles[2], *bot_tiles)],
                      LaggedStart(*[FadeIn(m, scale=0.7) for m in marks],
                                  lag_ratio=0.16), run_time=1.0)
            self.play(FadeOut(VGroup(*top_tiles[:3])),
                      FadeOut(VGroup(*bot_tiles)),
                      FadeOut(left_label), FadeOut(below_label),
                      run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            rest = self.chain_positions(4, 0.20)
            self.play(*[t.animate.move_to(p) for t, p in
                        zip(top_tiles[3:], rest)],
                      FadeOut(bar), FadeOut(marks), run_time=0.7)
            self.play(FadeIn(minus, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(law, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, law, color=CHALK_PINK)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: apply the quotient law -- 4^7 / 4^4 ------------------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("Top Exponent Minus Bottom Exponent", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            frac = at(chalk_math(r"\frac{4^7}{4^4}", size=48,
                                 color=CHALK_WHITE), BOARD_CX, 1.55)
            same = at(chip("the same base", CHALK_GREEN, size=15), 3.85, 1.55)
            sub_line = at(chalk_math(r"7 - 4 = 3", size=40,
                                     color=CHALK_YELLOW), BOARD_CX, 0.45)
            result = at(card(chalk_math(r"\frac{4^7}{4^4} = 4^{7-4} = 4^3",
                                        size=32, color=CHALK_PINK),
                             CHALK_PINK), BOARD_CX, -0.70)
            value = at(card(chalk_math("4^3 = 64", size=24,
                                         color=CHALK_CYAN), CHALK_CYAN),
                             4.30, -0.70)
            strip = at(board_text("Numerator exponent minus denominator "
                                  "exponent.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(frac, shift=UP * 0.08),
                      FadeIn(same, scale=0.8), run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(sub_line, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(result, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(value, scale=0.85), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, value, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: when the answer exponent is negative -----------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("A Negative Answer Is Fine", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            frac = at(chalk_math(r"\frac{5^2}{5^5}", size=48,
                                 color=CHALK_WHITE), BOARD_CX, 1.55)
            same = at(chip("the same base", CHALK_GREEN, size=15), 3.85, 1.55)
            sub_line = at(chalk_math(r"2 - 5 = -3", size=40,
                                     color=CHALK_YELLOW), BOARD_CX, 0.45)
            result = at(card(chalk_math(r"\frac{5^2}{5^5} = 5^{-3}", size=34,
                                        color=CHALK_PINK), CHALK_PINK),
                        BOARD_CX, -0.70)
            recip = at(card(chalk_math(r"= 1/5^3 = 1/125", size=22,
                                         color=CHALK_CYAN), CHALK_CYAN),
                             4.05, -0.70)
            strip = at(board_text("A negative exponent is a valid answer.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(frac, shift=UP * 0.08),
                      FadeIn(same, scale=0.8), run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(sub_line, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(result, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(recip, scale=0.85), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, recip, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: product against quotient -----------------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Same Base Is the Key", 22, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            product = at(zone_card(
                "PRODUCT",
                [chalk_math(r"a^m \times a^n", size=30, color=CHALK_WHITE),
                 chalk_math(r"= a^{m+n}", size=30, color=CHALK_WHITE)],
                CHALK_CYAN, width=4.2, height=2.80,
                note="JOIN  \u2192  ADD"), -2.35, 0.55)
            quotient = at(zone_card(
                "QUOTIENT",
                [chalk_math(r"\frac{a^m}{a^n}", size=30, color=CHALK_WHITE),
                 chalk_math(r"= a^{m-n}", size=30, color=CHALK_WHITE)],
                CHALK_PINK, width=4.2, height=2.80,
                note="CANCEL  \u2192  SUBTRACT"), 3.35, 0.55)
            key = at(board_text("SAME\nBASE", 18, CHALK_YELLOW, "BOLD"),
                     BOARD_CX, 0.55)
            strip = at(board_text("a is not zero, and the exponents are "
                                  "integers.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(product, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(quotient, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(key, scale=0.8), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, key, color=CHALK_YELLOW)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: three mistakes to avoid ------------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("Three Mistakes to Avoid", 22, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            row1 = at(card(VGroup(
                chalk_math(r"x^{-3} \times x^{-2} = x^{-6}", size=24,
                           color=CHALK_RED),
                mark_no(0.85),
                board_text("\u2192", 20, CHALK_WHITE, "BOLD"),
                chalk_math(r"x^{-5}", size=26, color=CHALK_GREEN)
            ).arrange(RIGHT, buff=0.38), CHALK_RED, pad_y=0.30),
                BOARD_CX, 1.62)
            row2 = at(card(VGroup(
                chalk_math(r"2^{3} \times 3^{4}", size=24, color=CHALK_WHITE),
                mark_no(0.85),
                chalk_math(r"2 \neq 3", size=24, color=CHALK_PINK),
                board_text("different bases", 15, CHALK_PINK, "BOLD")
            ).arrange(RIGHT, buff=0.38), CHALK_RED, pad_y=0.30),
                BOARD_CX, 0.66)
            row3 = at(card(VGroup(
                chalk_math(r"\frac{a^2}{a^5} = a^{5-2}", size=24,
                           color=CHALK_RED),
                mark_no(0.85),
                board_text("\u2192", 20, CHALK_WHITE, "BOLD"),
                chalk_math(r"a^{-3}", size=26, color=CHALK_GREEN)
            ).arrange(RIGHT, buff=0.38), CHALK_RED, pad_y=0.30),
                BOARD_CX, -0.45)
            banner = at(board_text("Read the operation carefully.", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Same base first; then add or subtract.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(row1, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(row2, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(row3, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(banner, shift=UP * 0.08), run_time=0.45)
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
            sub = at(board_text("Product  \u00b7  Quotient  \u00b7  Same base",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, 2.24)

            qa = at(q_card("Simplify",
                           chalk_math(r"2^{-3} \times 2^{-2}", size=20,
                                      color=CHALK_WHITE)), -2.55, 1.50)
            qb = at(q_card("Simplify",
                           chalk_math(r"7^{-2} \times 7^{5}", size=20,
                                      color=CHALK_WHITE)), -2.55, 0.35)
            qc = at(q_card("Simplify",
                           chalk_math(r"\frac{4^7}{4^4}", size=18,
                                      color=CHALK_WHITE),
                           height=1.10, head_up=0.32, body_down=0.28),
                    -2.55, -0.90)

            ans_a = at(answer_row("A",
                                  chalk_math(r"2^{-3+(-2)} = 2^{-5}", 28,
                                             color=CHALK_GREEN),
                                  "add the exponents", CHALK_GREEN),
                       BOARD_CX, 1.30)
            ans_b = at(answer_row("B",
                                  chalk_math(r"7^{-2+5} = 7^{3}", 28,
                                             color=CHALK_YELLOW),
                                  "add the exponents", CHALK_YELLOW),
                       BOARD_CX, 0.45)
            ans_c = at(answer_row("C",
                                  chalk_math(r"4^{7-4} = 4^{3} = 64", 28,
                                             color=CHALK_PINK),
                                  "subtract the exponents", CHALK_PINK),
                       BOARD_CX, -0.40)
            done = at(board_text("KEEP THE BASE  \u2192  ADD OR SUBTRACT", 18,
                                 CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)

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

            heading = at(board_text("Join or Cancel", 24, CHALK_AMBER, "BOLD"),
                         BOARD_CX, ROW_Y)
            product = at(card(VGroup(
                chalk_math(r"a^m \times a^n = a^{m+n}", size=34,
                           color=CHALK_CYAN),
                board_text("JOIN  \u2192  ADD", 16, CHALK_CYAN, "BOLD")
            ).arrange(DOWN, buff=0.26), CHALK_CYAN), BOARD_CX, 1.15)
            quotient = at(card(VGroup(
                chalk_math(r"\frac{a^m}{a^n} = a^{m-n}", size=34,
                           color=CHALK_PINK),
                board_text("CANCEL  \u2192  SUBTRACT", 16, CHALK_PINK, "BOLD")
            ).arrange(DOWN, buff=0.26), CHALK_PINK), BOARD_CX, -0.45)
            notzero = at(chalk_math(r"a \neq 0", size=22, color=CHALK_YELLOW),
                         4.45, -0.45)
            strip = at(board_text("Same non-zero base, integer exponents.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            thanks = at(board_text("Thank You for Watching!", 30, CHALK_WHITE,
                                   "BOLD"), BOARD_CX, 0.62)
            bye = at(board_text("See you in the next lesson :)", 22,
                                CHALK_YELLOW, "BOLD"), BOARD_CX, -0.32)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(product, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(quotient, shift=UP * 0.08),
                      FadeIn(notzero), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["success"], gain=-11)

            # the closing card is narrated: it appears as the voice says
            # "Thank you for watching,", the goodbye line as the voice says
            # "and see you in the next lesson."
            self.wait(leftover(tracker, "b3"))
            self.play(FadeOut(heading), FadeOut(product), FadeOut(quotient),
                      FadeOut(notzero), FadeOut(strip), run_time=0.5)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.5)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.closing(tracker, thanks, run_time=1.2)
            self._capture_srt(tracker)

        self.wait(END_HOLD)



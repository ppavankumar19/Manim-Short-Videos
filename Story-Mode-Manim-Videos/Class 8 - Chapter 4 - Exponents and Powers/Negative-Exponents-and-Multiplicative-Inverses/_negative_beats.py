    # ================================================================ beats ==
    # Understanding Negative Exponents: Reciprocal Rules and Multiplicative
    # Inverses (Class 8, Chapter 4, Storymode 02).
    #
    # SYNC RULE for every reveal: wait for the narration bookmark that ends the
    # phrase describing a thing, and only then bring it on.  Playing first and
    # waiting afterwards shows the picture a whole window early, which reads as
    # broken sync.
    #
    # Layout rules, so the audits stay clean:
    #   * the heading sits on ROW_Y (2.72), the closing strip on STRIP_Y (-1.80);
    #     nothing at all sits below y = -2.00;
    #   * the staircase descends with a small indent, and its "one step down"
    #     note divides by the STAIRCASE'S OWN BASE (10 in scenes 2, 3 and 10,
    #     2 in scene 4) -- safeguard G;
    #   * nothing is placed on a line, and no card, step or chip is placed over
    #     another element -- checked by audit_clearance.py and
    #     audit_sync_overlap.py;
    #   * the challenge uses the series' shared 10-second THINK clock, dead
    #     centre of the board, with the question cards on the LEFT while it runs.
    ROW_Y = 2.72
    BANNER_Y = -1.25
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

    # -- Scene 0: title ------------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            heading = at(board_text("Negative Exponents", 28, CHALK_WHITE,
                                    "BOLD"), BOARD_CX, 2.05)
            sub = at(board_text("Reciprocals and Multiplicative Inverses", 19,
                                CHALK_AMBER, "BOLD"), BOARD_CX, 1.36)
            show = at(chalk_math(r"2^{-3} = \frac{1}{2^3} = \frac{1}{8}",
                                 size=40, color=CHALK_CYAN), BOARD_CX, 0.42)
            promise = at(board_text("A negative power is not a negative "
                                    "number.", 16, CHALK_WHITE, "BOLD"),
                         BOARD_CX, BANNER_Y + 0.05)
            strip = at(board_text("The minus sign means: take the reciprocal.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(sub, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(show, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(promise, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, show, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: from huge numbers to tiny numbers --------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("From Huge Numbers to Tiny Numbers", 24,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sun_grp = at(sun(0.50), -3.60, 1.60)
            solar = at(card(VGroup(
                chalk_math(r"1.4 \times 10^9", size=26, color=CHALK_GREEN),
                board_text("metres", 16, CHALK_WHITE, "BOLD")
            ).arrange(RIGHT, buff=0.25), CHALK_GREEN), -1.35, 1.60)
            hair = at(card(board_text("0.000005 m", 26, CHALK_CYAN, "BOLD"),
                           CHALK_CYAN), 3.20, 1.60)
            big_lab = at(board_text("the Sun's width", 14, CHALK_AMBER, "BOLD"),
                         -1.35, 0.86)
            tiny_lab = at(board_text("a hair's thickness", 14, CHALK_AMBER,
                                     "BOLD"), 3.20, 0.86)
            zoom = Arrow(solar.get_right() + RIGHT * 0.22,
                         hair.get_left() + LEFT * 0.22, buff=0,
                         stroke_width=3.0, color=CHALK_WHITE,
                         max_tip_length_to_length_ratio=0.30)
            question = at(board_text("Can exponents take us below one?", 20,
                                     CHALK_PINK, "BOLD"), BOARD_CX, 0.25)
            line = number_line(-0.72)
            banner = at(board_text("We need a new kind of power.", 20,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, -1.20)
            strip = at(board_text("Positive powers grow; negative powers "
                                  "shrink.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(sun_grp, scale=0.85), run_time=0.45)
            self.play(FadeIn(solar, shift=UP * 0.08),
                      FadeIn(big_lab), run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(GrowArrow(zoom), FadeIn(hair, shift=LEFT * 0.10),
                      FadeIn(tiny_lab), run_time=0.7)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(question, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(line, shift=UP * 0.06), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, banner)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: follow the pattern down to zero ----------------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("Follow the Pattern", 24, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            stairs = staircase([r"10^{3} = 1000", r"10^{2} = 100",
                                r"10^{1} = 10", r"10^{0} = 1"],
                               x0=1.30, y0=1.50, dy=0.62, dx=-0.50, size=28)
            tens = VGroup(*[at(chip("\u00f7 10", CHALK_YELLOW, size=16),
                               x, y) for x, y in ((3.15, 1.19), (2.65, 0.57),
                                                  (2.15, -0.05))])
            way_down = down_arrow(-1.65, 1.85, -0.75)
            prompt = at(card(chalk_math(r"10^{-1} = ?", size=24,
                                        color=CHALK_PINK), CHALK_PINK),
                        3.55, -0.50)
            banner = at(board_text("Every step down divides by ten.", 19,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The pattern must continue below one.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(way_down), run_time=0.4)
            self.play(FadeIn(stairs.rows[0], shift=RIGHT * 0.10),
                      FadeIn(tens[0], scale=0.8), run_time=0.5)
            self.play(FadeIn(stairs.rows[1], shift=RIGHT * 0.10),
                      FadeIn(tens[1], scale=0.8), run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(stairs.rows[2], shift=RIGHT * 0.10),
                      FadeIn(tens[2], scale=0.8), run_time=0.5)
            self.play(FadeIn(stairs.rows[3], shift=RIGHT * 0.10), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(prompt, scale=0.8), run_time=0.45)
            self.play(FadeIn(banner, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, stairs.rows[3], color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: crossing zero -- the negative exponents appear -------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Crossing Zero", 24, CHALK_AMBER, "BOLD"),
                         BOARD_CX, ROW_Y)
            stairs = staircase([r"10^{2} = 100", r"10^{1} = 10",
                                r"10^{0} = 1", r"10^{-1} = 1/10",
                                r"10^{-2} = 1/100", r"10^{-3} = 1/1000"],
                               x0=1.55, y0=1.72, dy=0.58, dx=-0.40, size=26)
            way_down = down_arrow(-2.45, 1.98, -1.32)
            note = at(divider_box(["\u00f7 10", "each step"]), -3.55, 0.20)
            key = at(card(chalk_math(r"10^{-1} = \frac{1}{10}", size=34,
                                     color=CHALK_YELLOW), CHALK_YELLOW),
                     3.15, -0.75)
            ring = SurroundingRectangle(stairs.rows[3], color=CHALK_YELLOW,
                                        buff=0.10, corner_radius=0.10,
                                        stroke_width=3.0)
            strip = at(board_text("The minus sign moves the power under one.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(way_down), FadeIn(note), run_time=0.5)
            self.play(FadeIn(stairs.rows[0], shift=RIGHT * 0.10),
                      FadeIn(stairs.rows[1], shift=RIGHT * 0.10),
                      FadeIn(stairs.rows[2], shift=RIGHT * 0.10),
                      run_time=0.7)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(stairs.rows[3], shift=DOWN * 0.08),
                      FadeIn(ring), run_time=0.55)
            self.play(FadeIn(key, scale=0.85), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(stairs.rows[4], shift=DOWN * 0.08),
                      FadeIn(stairs.rows[5], shift=DOWN * 0.08), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, key, color=CHALK_YELLOW)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: the same idea for another base -----------------------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("Any Base Works", 24, CHALK_AMBER, "BOLD"),
                         BOARD_CX, ROW_Y)
            stairs = staircase([r"2^{3} = 8", r"2^{2} = 4", r"2^{1} = 2",
                                r"2^{0} = 1", r"2^{-1} = 1/2",
                                r"2^{-2} = 1/4"],
                               x0=1.55, y0=1.72, dy=0.58, dx=-0.40, size=26)
            way_down = down_arrow(-2.45, 1.98, -1.32)
            note = at(divider_box(["\u00f7 2", "each step"]), -3.55, 0.20)
            same = at(card(board_text("the same pattern,\nany base", 16,
                                      CHALK_CYAN, "BOLD"), CHALK_CYAN),
                      3.15, -0.75)
            strip = at(board_text("One step down divides by the base.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(way_down), run_time=0.4)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(stairs.rows[0], shift=RIGHT * 0.10),
                      FadeIn(stairs.rows[1], shift=RIGHT * 0.10),
                      run_time=0.5)
            self.play(FadeIn(stairs.rows[2], shift=RIGHT * 0.10),
                      FadeIn(stairs.rows[3], shift=RIGHT * 0.10),
                      run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(note, scale=0.85), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(stairs.rows[4], shift=DOWN * 0.08),
                      FadeIn(stairs.rows[5], shift=DOWN * 0.08),
                      run_time=0.55)
            self.play(FadeIn(same, scale=0.85), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, same, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: the general rule -------------------------------------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Negative Exponent Rule", 24,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            big = at(chalk_math("a^{-m}", size=76, color=CHALK_WHITE),
                     BOARD_CX, 1.35)
            notzero = at(chalk_math(r"a \neq 0", size=26, color=CHALK_PINK),
                         3.60, 1.35)
            rule = at(card(chalk_math(r"a^{-m} = \frac{1}{a^m}", size=54,
                                      color=CHALK_GREEN), CHALK_GREEN,
                           pad_x=0.60, pad_y=0.44), BOARD_CX, 1.20)
            back = at(card(chalk_math(r"\frac{1}{a^m} = a^{-m}", size=44,
                                      color=CHALK_CYAN), CHALK_CYAN,
                           pad_x=0.56, pad_y=0.40), BOARD_CX, -0.35)
            back_note = at(board_text("positive downstairs", 15,
                                          CHALK_WHITE, "BOLD"), 3.85, -0.35)
            banner = at(board_text("Negative exponent \u2192 reciprocal.", 19,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("a to the power minus m is the reciprocal.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(big, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(notzero, shift=LEFT * 0.08), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(ReplacementTransform(big, rule), run_time=0.7)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(back, shift=UP * 0.08),
                      FadeIn(back_note, shift=LEFT * 0.08), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, rule, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: a negative exponent is not a negative number ---------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("Not a Negative Number", 24, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            left = at(card(chalk_math(r"2^{-3} = \frac{1}{2^3} = \frac{1}{8}",
                                      size=32, color=CHALK_CYAN), CHALK_CYAN),
                      -2.35, 0.55)
            right = at(card(chalk_math(r"-2^{3} = -8", size=40,
                                       color=CHALK_RED), CHALK_RED),
                       3.45, 0.55)
            neq = at(chalk_math(r"\neq", size=60, color=CHALK_PINK), 0.85, 0.55)
            banner = at(board_text("The minus sign is part of the exponent.", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("It takes the reciprocal, not the sign.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(left, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(right, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(neq, scale=0.7), run_time=0.45)
            self.play(FadeIn(banner, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, neq, color=CHALK_PINK)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: multiplicative inverses (the reciprocal mirror) ------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Multiplicative Inverses", 24, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            axis = mirror(BOARD_CX, 1.85, 0.45)
            left = at(card(chalk_math("2^{3} = 8", size=40, color=CHALK_CYAN),
                           CHALK_CYAN), -2.45, 1.20)
            right = at(card(chalk_math(r"2^{-3} = \frac{1}{8}", size=36,
                                       color=CHALK_PINK), CHALK_PINK),
                       3.45, 1.20)
            product = at(chalk_math(r"8 \times \frac{1}{8} = 1", size=36,
                                    color=CHALK_YELLOW), BOARD_CX, 0.00)
            general = at(chalk_math(r"a^m \times a^{-m} = a^{m+(-m)} = a^{0} "
                                    r"= 1", size=28, color=CHALK_GREEN),
                         BOARD_CX, -0.85)
            strip = at(board_text("Each is the multiplicative inverse of the "
                                  "other.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(axis, shift=DOWN * 0.08), run_time=0.5)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(left, shift=UP * 0.08),
                      FadeIn(right, shift=UP * 0.08), run_time=0.65)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(product, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(general, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, general, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: finding an inverse quickly ---------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("Flip the Sign", 24, CHALK_AMBER, "BOLD"),
                         BOARD_CX, ROW_Y)
            pair1 = at(card(VGroup(
                chalk_math(r"3^{-5} \rightarrow 3^{5}", size=26,
                           color=CHALK_CYAN),
                chalk_math(r"3^{-5} \times 3^{5} = 3^{0} = 1", size=20,
                           color=CHALK_WHITE)).arrange(RIGHT, buff=0.70),
                CHALK_CYAN), BOARD_CX, 1.55)
            pair2 = at(card(VGroup(
                chalk_math(r"4^{-3} \rightarrow 4^{3}", size=26,
                           color=CHALK_YELLOW),
                chalk_math(r"4^{-3} \times 4^{3} = 4^{0} = 1", size=20,
                           color=CHALK_WHITE)).arrange(RIGHT, buff=0.70),
                CHALK_YELLOW), BOARD_CX, 0.65)
            pair3 = at(card(VGroup(
                chalk_math(r"x^{-n} \rightarrow x^{n}", size=26,
                           color=CHALK_PINK),
                chalk_math(r"x^{-n} \times x^{n} = x^{0} = 1", size=20,
                           color=CHALK_WHITE)).arrange(RIGHT, buff=0.70),
                CHALK_PINK), BOARD_CX, -0.25)
            banner = at(board_text("The inverse reverses the exponent sign.", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The inverse of a power is the same power "
                                  "flipped.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(pair1, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(pair2, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(pair3, shift=UP * 0.08), run_time=0.5)
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
            sub = at(board_text("Rewrite  \u00b7  Evaluate  \u00b7  Invert", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, 2.24)

            qa = at(q_card("Write with a positive exponent",
                           chalk_math("10^{-4}", size=22, color=CHALK_WHITE)),
                    -2.55, 1.45)
            qb = at(q_card("Find its value",
                           chalk_math("5^{-2}", size=22, color=CHALK_WHITE)),
                    -2.55, 0.31)
            qc = at(q_card("Write the multiplicative inverse",
                           chalk_math("7^{-3}", size=22, color=CHALK_WHITE)),
                    -2.55, -0.83)

            ans_a = at(answer_row("A",
                                  chalk_math(r"10^{-4} = \frac{1}{10^4}", 28,
                                             color=CHALK_GREEN),
                                  "one over ten thousand", CHALK_GREEN),
                       BOARD_CX, 1.30)
            ans_b = at(answer_row("B",
                                  chalk_math(r"5^{-2} = \frac{1}{5^2} = "
                                             r"\frac{1}{25}", 26,
                                             color=CHALK_YELLOW),
                                  "one twenty fifth", CHALK_YELLOW),
                       BOARD_CX, 0.45)
            ans_c = at(answer_row("C", chalk_math("7^{3}", 30, color=CHALK_PINK),
                                  "their product is one", CHALK_PINK),
                       BOARD_CX, -0.40)
            done = at(board_text("Rewrite  \u2192  Evaluate  \u2192  Find the "
                                 "inverse", 18, CHALK_YELLOW, "BOLD"),
                      BOARD_CX, -1.30)

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

            heading = at(board_text("Pattern, Rule, Inverse", 24, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            stairs = staircase([r"10^{1} = 10", r"10^{0} = 1",
                                r"10^{-1} = 1/10", r"10^{-2} = 1/100"],
                               x0=-2.15, y0=1.50, dy=0.62, dx=0.20, size=24)
            mirror_pair = at(chalk_math(r"a^m \leftrightarrow a^{-m}", size=30,
                                        color=CHALK_CYAN), 2.85, 1.25)
            product = at(chalk_math(r"a^m \times a^{-m} = 1", size=28,
                                    color=CHALK_YELLOW), 2.85, 0.45)
            rule = at(card(chalk_math(r"a^{-m} = \frac{1}{a^m}", size=32,
                                      color=CHALK_GREEN), CHALK_GREEN),
                      2.85, -0.45)
            notzero = at(chalk_math(r"a \neq 0", size=20, color=CHALK_PINK),
                         4.85, -0.45)
            strip = at(board_text("Negative exponent \u2192 reciprocal \u2192 "
                                  "inverse.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            thanks = at(board_text("Thank You for Watching!", 30, CHALK_WHITE,
                                   "BOLD"), BOARD_CX, 0.62)
            bye = at(board_text("See you in the next lesson :)", 22,
                                CHALK_YELLOW, "BOLD"), BOARD_CX, -0.32)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(stairs.rows[0], shift=RIGHT * 0.10),
                      FadeIn(stairs.rows[1], shift=RIGHT * 0.10),
                      run_time=0.5)
            self.play(FadeIn(stairs.rows[2], shift=RIGHT * 0.10),
                      FadeIn(stairs.rows[3], shift=RIGHT * 0.10),
                      run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(mirror_pair, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(product, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(rule, scale=0.9), FadeIn(notzero),
                      run_time=0.55)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["success"], gain=-11)

            # the closing card is narrated: it appears as the voice says
            # "Thank you for watching,", the goodbye line as the voice says
            # "and see you in the next lesson."
            self.wait(leftover(tracker, "b3"))
            self.play(FadeOut(heading), FadeOut(stairs), FadeOut(mirror_pair),
                      FadeOut(product), FadeOut(rule), FadeOut(notzero),
                      FadeOut(strip), run_time=0.5)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.5)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.closing(tracker, thanks, run_time=1.2)
            self._capture_srt(tracker)

        self.wait(END_HOLD)


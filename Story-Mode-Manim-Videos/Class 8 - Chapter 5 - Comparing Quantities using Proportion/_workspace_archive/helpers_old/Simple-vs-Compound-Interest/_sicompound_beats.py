    # ================================================================ beats ==
    # Simple Interest vs. Compound Interest: Deriving the Compound Interest
    # Formula (Class 8 Maths, Chapter 5, Storymode 02).
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
    #   * every row of cards is centred on BOARD_CX (`hrow`), and two texts never
    #     come closer than the 0.22 units the clearance audit asks for -- which
    #     is why every card holds its own lines 0.26 or more apart;
    #   * the SIMPLE-INTEREST ladder keeps its principal block LOCKED with the
    #     drawn padlock: P + I never becomes the next principal there, or the
    #     ladder would accidentally depict compound interest;
    #   * in the COMPOUND ladder the amount really does become the next
    #     principal: the P and I blocks are replaced in ONE play by the merged
    #     A1 block, which then slides down into the principal slot;
    #   * a drawn cross always lives in the same VGroup as the card it strikes
    #     through (otherwise the clearance audit reads the strokes as a line
    #     running into a card);
    #   * the challenge uses the series' shared 10-second THINK clock, dead
    #     centre of the board, and the question cards sit in the four corners so
    #     the badge never covers one.

    def closing(self, tracker, mob=None, color=CHALK_YELLOW, run_time=None):
        """Consume the tail of the narration window on the last reveal."""
        budget = rt(tracker.get_remaining_duration()) if run_time is None \
            else run_time
        if mob is None:
            self.wait(max(budget, 0.0))
        else:
            self.play(Indicate(mob, color=color, scale_factor=1.03),
                      run_time=max(budget, MIN_RT))

    def hrow(self, *mobs, y, gap=0.45, cx=BOARD_CX):
        """One row of board objects: centred on the board, equal air between."""
        row = VGroup(*mobs).arrange(RIGHT, buff=gap)
        return at(row, cx, y)

    def method_row(self, y=0.50):
        """Ramesh's and Sreenu's account cards, side by side."""
        ca, cb = row_centres((CARD_W / 2, CARD_W / 2), 0.50)
        a = at(method_card("RAMESH'S METHOD", "Simple Interest",
                           "Rs 100 gives Rs 120", CHALK_GREEN, "coins"), ca, y)
        b = at(method_card("SREENU'S METHOD", "Compound Interest",
                           "Rs 100 gives Rs 121", CHALK_PINK, "note"), cb, y)
        return a, b

    def q_card(self, title, pict, color=CHALK_CYAN, width=3.10, pad=0.12,
               title_size=13, buff=0.26):
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

    # -- Scene 0: title -- the same money, two methods, two answers ----------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = at(board_text("Same Money, Two Methods", 24, CHALK_PINK,
                                  "BOLD"), BOARD_CX, 2.06)
            sub = at(board_text("Rs 100 for 2 years at 10%: Rs 120 or Rs 121?",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, 1.40)

            a_card, b_card = self.method_row(y=0.45)
            same = at(chip("SAME PRINCIPAL · SAME RATE · SAME TIME",
                           CHALK_CYAN, 14), BOARD_CX, -0.60)
            banner = at(board_text("WHERE DID THE EXTRA Re 1 COME FROM?", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Same principal, same rate, same time: one "
                                  "rupee more.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(title, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(a_card, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(b_card, shift=LEFT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(same, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(Indicate(a_card, color=CHALK_GREEN, scale_factor=1.02),
                      Indicate(b_card, color=CHALK_PINK, scale_factor=1.02),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: simple interest -- the base is locked at the principal ------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("Ramesh's Method: Simple Interest", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The interest stays on the original principal.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # the money ladder: the principal is LOCKED, and the two interest
            # blocks are identical because the base never moves
            base, i1, i2, total = ladder(
                -2.45,
                [("Principal Rs 100", CHALK_GREEN, -0.85),
                 ("Interest Rs 10", CHALK_YELLOW),
                 ("Interest Rs 10", CHALK_YELLOW),
                 ("Amount Rs 120", CHALK_CYAN)],
                height=0.54, step=0.62, size=13, y0=-0.45)

            formula = at(chalk_math(r"SI = \frac{P \times T \times R}{100}",
                                    size=24, color=CHALK_WHITE), 2.55, 1.05)
            data = at(chip("Rs 2,500 at 12% for 3 years", CHALK_AMBER, 14),
                      2.55, 0.30)
            result = at(chip("SI = Rs 900, Amount = Rs 3,400", CHALK_GREEN, 13),
                        2.55, -0.42)

            banner = at(board_text("THE SAME INTEREST EVERY YEAR", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Simple interest always uses the original "
                                  "principal.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(base, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(i1, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(i2, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(total, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(formula, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(data, shift=UP * 0.06),
                      FadeIn(result, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: compound interest -- the amount becomes the next principal --
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("Sreenu's Method: Compound Interest", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Each new amount becomes the next principal.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            p_block = at(block_row("Principal Rs 100", CHALK_GREEN),
                         -2.45, -0.45)
            i1 = at(block_row("Interest Rs 10", CHALK_YELLOW), -2.45, 0.17)
            a1 = at(block_row("Amount Rs 110", CHALK_CYAN), -2.45, -0.14)
            i2 = at(block_row("Interest Rs 11", CHALK_AMBER, width=2.60,
                              height=0.70), -2.45, 0.17)
            a2 = at(block_row("Amount Rs 121", CHALK_CYAN), -2.45, -0.14)
            slot = np.array([-2.45, -0.45, 0.0])

            y1 = at(chip("Year 1: 10% of Rs 100 = Rs 10", CHALK_GREEN, 14),
                    2.55, 0.90)
            y2 = at(chip("Year 2: 10% of Rs 110 = Rs 11", CHALK_AMBER, 14),
                    2.55, 0.18)
            more = at(chip("The second interest is Re 1 more", CHALK_PINK, 14),
                      2.55, -0.54)
            extra = at(chip("The extra Re 1 is 10% of Rs 10", CHALK_PINK, 14),
                       2.55, -0.54)

            banner = at(board_text("THE INTEREST EARNED ALSO EARNS INTEREST", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The extra rupee is interest on the first "
                                  "year's interest.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(p_block, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(i1, shift=UP * 0.06),
                      FadeIn(y1, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            # the principal and its interest MERGE into one A1 block, which then
            # slides down into the principal slot and becomes year two's base
            self.wait(leftover(tracker, "b2"))
            self.play(FadeOut(p_block, shift=UP * 0.10),
                      FadeOut(i1, shift=DOWN * 0.10),
                      FadeIn(a1, scale=1.04), run_time=0.60)
            self.play(a1.animate.move_to(slot), run_time=0.55)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(i2, scale=0.95),
                      FadeIn(y2, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeOut(a1, shift=UP * 0.10),
                      FadeOut(i2, shift=DOWN * 0.10),
                      FadeIn(a2, scale=1.04), run_time=0.60)
            self.play(a2.animate.move_to(slot), run_time=0.55)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(more, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b6"))
            self.play(Transform(more, extra),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: one period -- the growth factor -----------------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("The One-Period Growth Factor", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Amount equals principal plus the interest on "
                                "it.", 17, CHALK_WHITE, "BOLD"),
                     BOARD_CX, SUB_Y)

            p_block = at(block_row("Principal Rs 100", CHALK_GREEN, width=2.10,
                                   height=0.58, size=13), -3.15, 0.95)
            m1 = at(chalk_math(r"A_1 = P + \frac{P \times R}{100}", size=26,
                               color=CHALK_WHITE), 1.30, 0.95)
            m2 = at(chalk_math(r"A_1 = P\left(1+\frac{R}{100}\right)", size=26,
                               color=CHALK_WHITE), 1.30, 0.95)
            gf = at(factor_card(CHALK_AMBER, 2.80, 0.90, 28), 2.55, -0.30)
            tag = at(chip("ONE-PERIOD GROWTH FACTOR", CHALK_AMBER, 14),
                     -2.05, -0.30)

            banner = at(board_text("EVERY PERIOD MULTIPLIES BY THIS FACTOR", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The bracket is the one-period growth "
                                  "factor.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(p_block, shift=RIGHT * 0.10),
                      FadeIn(m1, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(TransformMatchingTex(m1, m2), run_time=0.80)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(gf, scale=0.95), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(tag, shift=UP * 0.06),
                      Indicate(p_block, color=CHALK_GREEN, scale_factor=1.04),
                      run_time=0.65)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: year two -- the same factor multiplies again ---------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Same Factor Multiplies Again", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The year-one amount is the year-two principal.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            m_a = at(chalk_math(r"A_2 = P\left(1+\frac{R}{100}\right)", size=26,
                                color=CHALK_WHITE), BOARD_CX, 1.25)
            m_b = at(chalk_math(
                r"A_2 = P\left(1+\frac{R}{100}\right)"
                r"\left(1+\frac{R}{100}\right)", size=24, color=CHALK_WHITE),
                BOARD_CX, 1.25)
            m_c = at(chalk_math(r"A_2 = P\left(1+\frac{R}{100}\right)^2", size=26,
                                color=CHALK_WHITE), BOARD_CX, 1.25)

            gf1 = at(factor_card(CHALK_GREEN, 2.30, 0.78, 24), -1.15, 0.30)
            gf2 = at(factor_card(CHALK_PINK, 2.30, 0.78, 24), 2.15, 0.30)
            times = at(chalk_math(r"\times", size=26, color=CHALK_WHITE),
                       BOARD_CX, 0.30)
            y1 = at(chip("YEAR 1", CHALK_GREEN, 12), -1.15, -0.45)
            y2 = at(chip("YEAR 2", CHALK_PINK, 12), 2.15, -0.45)

            banner = at(board_text("TWO YEARS, TWO FACTORS, ONE POWER", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The same growth factor multiplies once "
                                  "more.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(m_a, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(gf1, scale=0.95),
                      FadeIn(y1, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(times, scale=0.95), FadeIn(gf2, scale=0.95),
                      FadeIn(y2, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(TransformMatchingTex(m_a, m_b), run_time=0.75)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(TransformMatchingTex(m_b, m_c), run_time=0.75)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: n years -- repeated multiplication becomes a power ---------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("One Factor for Every Year", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Year one, year two, up to year n.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            m_a = at(chalk_math(r"A = P\left(1+\frac{R}{100}\right)^2", size=26,
                                color=CHALK_WHITE), BOARD_CX, -0.40)
            m_b = at(chalk_math(r"A = P\left(1+\frac{R}{100}\right)^n", size=26,
                                color=CHALK_YELLOW), BOARD_CX, -0.40)

            chain = self.hrow(
                chip("YEAR 1", CHALK_GREEN, 12),
                chalk_math(r"\times", size=20, color=CHALK_WHITE),
                chip("YEAR 2", CHALK_CYAN, 12),
                chalk_math(r"\times", size=20, color=CHALK_WHITE),
                chip("YEAR 3", CHALK_PINK, 12),
                chalk_math(r"\cdots", size=20, color=CHALK_WHITE),
                chip("YEAR n", CHALK_AMBER, 12), y=0.62, gap=0.26)
            note = at(chip("n = NUMBER OF GROWTH PERIODS", CHALK_AMBER, 11),
                      -2.75, -0.40)

            banner = at(board_text("ONE FACTOR EVERY YEAR MAKES A POWER", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The exponent counts the number of growth "
                                  "periods.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(m_a, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(chain, shift=UP * 0.06), run_time=0.70)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(TransformMatchingTex(m_a, m_b), run_time=0.75)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(note, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: the formula gives the AMOUNT --------------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Formula Gives the Amount", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The amount is principal plus interest.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            m_a = at(chalk_math(r"A = P\left(1+\frac{R}{100}\right)^n", size=26,
                                color=CHALK_YELLOW), BOARD_CX, 1.30)
            m_b = at(chalk_math(
                r"CI = A - P = P\left(1+\frac{R}{100}\right)^n - P", size=26,
                color=CHALK_YELLOW), BOARD_CX, 1.30)

            amount = at(block_row("Amount Rs 121", CHALK_CYAN, width=3.20,
                                  height=0.58, size=14), BOARD_CX, 0.45)
            principal = at(block_row("Principal Rs 100", CHALK_GREEN, width=2.60,
                                     height=0.56, size=14), -1.60, -0.32)
            plus = at(chalk_math("+", size=26, color=CHALK_WHITE),
                      BOARD_CX, -0.32)
            interest = at(block_row("Interest Rs 21", CHALK_AMBER, width=2.60,
                                    height=0.56, size=14), 2.60, -0.32)

            banner = at(board_text("THE FORMULA GIVES THE AMOUNT", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The formula gives the amount, not the "
                                  "interest.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(m_a, shift=UP * 0.06),
                      FadeIn(amount, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(principal, shift=RIGHT * 0.10),
                      FadeIn(plus, scale=0.95), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(interest, shift=LEFT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(TransformMatchingTex(m_a, m_b), run_time=0.80)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: applying the formula ---------------------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Apply It: Rs 5,000 at 8% for 2 Years", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Principal Rs 5,000, rate 8%, two years.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            inputs = self.hrow(chip("P = Rs 5,000", CHALK_GREEN, 14),
                               chip("R = 8%", CHALK_AMBER, 14),
                               chip("n = 2 years", CHALK_CYAN, 14),
                               y=1.32, gap=0.40)
            m_a = at(chalk_math(r"A = 5000\left(\frac{108}{100}\right)^2",
                                size=26, color=CHALK_WHITE), BOARD_CX, 0.48)
            m_b = at(chalk_math(
                r"A = 5000\left(\frac{108}{100}\right)^2 = 5832", size=26,
                color=CHALK_WHITE), BOARD_CX, 0.48)
            amount = at(chip("AMOUNT = Rs 5,832", CHALK_GREEN, 15), -1.85, -0.42)
            ci_rule = at(chip("CI = AMOUNT - PRINCIPAL", CHALK_AMBER, 14),
                         2.05, -0.42)
            ci_num = at(chip("CI = Rs 5,832 - Rs 5,000 = Rs 832", CHALK_AMBER, 13),
                        2.05, -0.42)

            banner = at(board_text("CI IS THE AMOUNT MINUS THE PRINCIPAL", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Compound interest is the amount minus the "
                                  "principal.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(inputs, shift=UP * 0.06),
                      FadeIn(m_a, shift=UP * 0.06), run_time=0.65)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(TransformMatchingTex(m_a, m_b), run_time=0.70)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(amount, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(ci_rule, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(Transform(ci_rule, ci_num), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the two ladders side by side --------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("Simple and Compound Side by Side", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("One base stays locked, the other grows.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            head_l = at(board_text("SIMPLE INTEREST", 13, CHALK_GREEN, "BOLD"),
                        -2.40, 1.68)
            head_r = at(board_text("COMPOUND INTEREST", 13, CHALK_PINK, "BOLD"),
                        2.90, 1.68)
            sy = (-0.50, 0.05, 0.60, 1.15)

            s_base = at(block_row("Principal Rs 100", CHALK_GREEN, SMALL_W,
                                  SMALL_H, 12, lock_dx=-SMALL_W / 2 - 0.14),
                        -2.40, sy[0])
            s_i1 = at(block_row("Interest Rs 10", CHALK_YELLOW, SMALL_W,
                                SMALL_H, 12), -2.40, sy[1])
            s_i2 = at(block_row("Interest Rs 10", CHALK_YELLOW, SMALL_W,
                                SMALL_H, 12), -2.40, sy[2])
            s_amt = at(block_row("Amount Rs 120", CHALK_CYAN, SMALL_W, SMALL_H,
                                 12), -2.40, sy[3])

            c_base = at(block_row("Principal Rs 100", CHALK_GREEN, SMALL_W,
                                  SMALL_H, 12), 2.90, sy[0])
            c_new = at(block_row("Base Rs 110", CHALK_CYAN, SMALL_W, SMALL_H,
                                 12), 2.90, sy[1])
            c_i2 = at(block_row("Interest Rs 11", CHALK_AMBER, 2.06, 0.50, 12),
                      2.90, sy[2])
            c_amt = at(block_row("Amount Rs 121", CHALK_PINK, SMALL_W, SMALL_H,
                                 12), 2.90, sy[3])

            mid = at(chip("YEAR 1: BOTH ADD Rs 10", CHALK_YELLOW, 12),
                     BOARD_CX, sy[1])
            banner = at(board_text("AFTER ONE YEAR SI AND CI ARE THE SAME", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The base changes only from the second year "
                                  "on.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.05)
                                    for m in (s_base, s_i1, s_i2, s_amt)],
                                  lag_ratio=0.18),
                      FadeIn(head_l, shift=UP * 0.06), run_time=0.95)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.05)
                                    for m in (c_base, c_new, c_i2, c_amt)],
                                  lag_ratio=0.18),
                      FadeIn(head_r, shift=UP * 0.06), run_time=0.95)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(mid, scale=0.92), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(Indicate(s_i1, color=CHALK_YELLOW, scale_factor=1.06),
                      Indicate(s_i2, color=CHALK_YELLOW, scale_factor=1.06),
                      run_time=0.70)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
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

            pic_a = chalk_math(r"P = 2000,\ R = 5\%,\ T = 3", size=18,
                               color=CHALK_GREEN)
            pic_b = chalk_math(r"P = 5000,\ R = 10\%,\ n = 2", size=18,
                               color=CHALK_CYAN)
            pic_c = VGroup(
                board_text("on Rs 5,000 every year", 11, CHALK_AMBER, "BOLD"),
                board_text("on last year's amount", 11, CHALK_AMBER,
                           "BOLD")).arrange(DOWN, buff=0.24)
            pic_d = chalk_math(r"SI \;=\; CI", size=20, color=CHALK_PINK)

            qa = at(self.q_card("A · Simple interest", pic_a, CHALK_GREEN),
                    -2.75, 0.95)
            qb = at(self.q_card("B · Compound interest", pic_b, CHALK_CYAN),
                    3.75, 0.95)
            qc = at(self.q_card("C · Which method?", pic_c, CHALK_AMBER),
                    -2.75, -1.10)
            qd = at(self.q_card("D · After year one?", pic_d, CHALK_PINK),
                    3.75, -1.10)

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
            a1 = at(self.answer_row("A", "SI = Rs 300",
                                    "amount = Rs 2,300", CHALK_GREEN),
                    BOARD_CX, 1.62)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "A = Rs 6,050",
                                    "CI = Rs 1,050", CHALK_CYAN),
                    BOARD_CX, 0.82)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "Rs 5,000 each year is SI",
                                    "on the last amount is CI", CHALK_AMBER),
                    BOARD_CX, 0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "No, they match",
                                    "one period, same principal", CHALK_PINK),
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

            heading = at(board_text("Simple · Compound · Growth", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)

            r1 = at(self.answer_row("1", "SIMPLE INTEREST",
                                    "the base stays the original principal",
                                    CHALK_GREEN), BOARD_CX, 1.48)
            r2 = at(self.answer_row("2", "COMPOUND INTEREST",
                                    "the amount becomes the next base",
                                    CHALK_CYAN), BOARD_CX, 0.72)
            r3 = at(self.answer_row("3", "DERIVATION",
                                    "A1, then A2, then A = P(1+R/100)^n",
                                    CHALK_YELLOW), BOARD_CX, -0.04)
            r4 = at(self.answer_row("4", "COMPOUND INTEREST",
                                    "CI = A - P: amount minus principal",
                                    CHALK_AMBER), BOARD_CX, -0.80)
            strip = at(board_text("Simple stays on the original base; compound "
                                  "grows on the new base.", 16, CHALK_WHITE,
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
            self.play(FadeIn(r4, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            # The list stays on the board through the whole closing sentence:
            # the strip is written on its own bookmark as the voice says "Simple
            # stays on the original base; compound grows on the new base.", and
            # only the bookmark in front of "Thank you for watching," clears the
            # board and brings in the card.
            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeOut(heading), FadeOut(r1), FadeOut(r2), FadeOut(r3),
                      FadeOut(r4), FadeOut(strip), run_time=0.55)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.50)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.closing(tracker, thanks, run_time=0.90)
            self._capture_srt(tracker)

        self.wait(END_HOLD)

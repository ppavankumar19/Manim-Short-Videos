    # ================================================================ beats ==
    # Compounding Half-Yearly, Quarterly & Applications to Population Growth
    # and Depreciation (Class 8 Maths, Chapter 5, Storymode 04).
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
    #   * two texts never come closer than the 0.22 units the clearance audit
    #     asks for, which is why every card cuts its own box to its content;
    #   * the compounding clock is the same furniture in every scene, and the
    #     SAME sector object is transformed from one period to two to four, so
    #     the dial is seen to split rather than being redrawn;
    #   * a drawn cross always lives in the same VGroup as the card it strikes
    #     through (otherwise the clearance audit reads the strokes as a line
    #     running into a box);
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

    def q_card(self, title, pict, color=CHALK_CYAN, width=3.20, pad=0.12,
               title_size=13, buff=0.26):
        """One 'your turn' card: a prompt above its small worked figure."""
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

    def formula_block(self, head, tex, color, x, y, head_size=13, buff=0.32):
        """One labelled formula for the summary board: a bold head line over a
        full-height maths object.

        The 0.32 gap between the head and the formula is the room the exponent
        gets: the audit measures text boxes, so nothing may come closer than
        0.22 to the raised power (`\\frac` plus a full-size superscript, never a
        cramped `\\tfrac`).
        """
        h = board_text(head, head_size, color, "BOLD")
        grp = VGroup(h, tex).arrange(DOWN, buff=buff)
        grp.head, grp.tex = h, tex
        return at(grp, x, y)

    # -- Scene 0: title ------------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = at(board_text("Compounding Periods, Growth & Depreciation",
                                  26, CHALK_PINK, "BOLD"), BOARD_CX, 2.06)
            sub = at(board_text("Half-Yearly · Quarterly · Growth · "
                                "Depreciation", 17, CHALK_WHITE, "BOLD"),
                     BOARD_CX, 1.46)

            self.play(FadeIn(title, shift=UP * 0.08), run_time=0.55)
            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            # the card is bare by design, so each of the narrated numbers
            # spotlights the line that carries the lesson's four parts
            self.wait(leftover(tracker, "b1"))
            self.play(Indicate(sub, color=CHALK_YELLOW, scale_factor=1.03),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Indicate(title, color=CHALK_PINK, scale_factor=1.02),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(Indicate(sub, color=CHALK_YELLOW, scale_factor=1.03),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(Indicate(title, color=CHALK_PINK, scale_factor=1.02),
                      run_time=0.70)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: the conversion period, and the dial that splits -------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Conversion Period", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("How often is the interest added?", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            face = clock_face(-2.45, 0.45)
            sec1 = clock_sectors(-2.45, 0.45, 1)
            lab1 = dial_label(-2.45, 0.45, "1 YEAR")
            note = at(chip("ONE PERIOD EACH YEAR", CHALK_GREEN, size=13),
                      2.90, -0.55)
            rate1 = at(chip("RATE: R PER YEAR", CHALK_AMBER, size=14),
                       2.90, 1.15)
            per1 = at(chip("PERIODS: n", CHALK_CYAN, size=14), 2.90, 0.35)
            rate2 = at(chip("RATE: R/2 PER PERIOD", CHALK_AMBER, size=14),
                       2.90, 1.15)
            rate3 = at(chip("RATE: R/4 PER PERIOD", CHALK_AMBER, size=14),
                       2.90, 1.15)
            per3 = at(chip("PERIODS: 4n", CHALK_CYAN, size=14), 2.90, 0.35)
            sec2 = clock_sectors(-2.45, 0.45, 2)
            sec4 = clock_sectors(-2.45, 0.45, 4)
            lab2 = dial_label(-2.45, 0.45, "HALF-YEARLY")
            lab3 = dial_label(-2.45, 0.45, "QUARTERLY")

            banner = at(board_text("RATE AND PERIODS CHANGE TOGETHER", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The conversion period fixes the rate and "
                                  "the number of periods.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(face), FadeIn(sec1), FadeIn(lab1),
                      FadeIn(note, scale=0.95), run_time=0.65)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(rate1, shift=RIGHT * 0.10),
                      FadeIn(per1, shift=RIGHT * 0.10), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(ReplacementTransform(sec1, sec2),
                      ReplacementTransform(rate1, rate2),
                      ReplacementTransform(lab1, lab2), run_time=0.75)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b3"))
            self.play(ReplacementTransform(sec2, sec4),
                      ReplacementTransform(rate2, rate3),
                      ReplacementTransform(lab2, lab3),
                      ReplacementTransform(per1, per3), run_time=0.85)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: the half-yearly rule -- both things change together ---------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("Half-Yearly: Two Changes at Once", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Halve the rate, double the periods.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            changes = self.hrow(
                chip("RATE HALVES: R → R/2", CHALK_AMBER, size=13),
                chip("PERIODS DOUBLE: n → 2n", CHALK_CYAN, size=13),
                y=1.55, gap=0.55)

            face = clock_face(-2.70, 0.35, r=0.80)
            sec1 = clock_sectors(-2.70, 0.35, 1, r=0.80)
            lab1 = dial_label(-2.70, 0.35, "1 YEAR")
            sec2 = clock_sectors(-2.70, 0.35, 2, r=0.80)
            lab2 = dial_label(-2.70, 0.35, "HALF-YEARLY")

            # a display-style fraction and a full-height power: the exponent is
            # never cramped, and the formula sits on the board's centre line
            # between the dial (left) and the struck-through card (right)
            tex1 = at(chalk_math(r"A = P\left(1 + \frac{R}{100}\right)^{n}",
                                 size=26, color=CHALK_WHITE), BOARD_CX, 0.15)
            tex2 = at(chalk_math(r"A = P\left(1 + \frac{R}{200}\right)^{2n}",
                                 size=26, color=CHALK_YELLOW), BOARD_CX, 0.15)

            wrong = wrong_card("10% EVERY 6 MONTHS", CHALK_RED, width=2.60,
                               height=1.05, size=14)
            wrong.move_to(np.array([3.80, 0.35, 0.0]))
            wrong_cross = wrong.cross
            wrong_cross.set_stroke(opacity=0)

            banner = at(board_text("RATE AND PERIODS CHANGE TOGETHER", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Half-yearly means 5% each half-year, never "
                                  "10% every six months.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(changes, shift=UP * 0.06), FadeIn(face),
                      FadeIn(sec1), FadeIn(lab1), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(ReplacementTransform(sec1, sec2),
                      ReplacementTransform(lab1, lab2), run_time=0.55)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b2"))
            self.play(Indicate(changes[1], color=CHALK_CYAN, scale_factor=1.06),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(tex1, shift=UP * 0.06), run_time=0.40)
            self.play(TransformMatchingTex(tex1, tex2), run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(wrong, scale=0.92), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b5"))
            self.play(wrong_cross.animate.set_stroke(opacity=1),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: the worked half-yearly example ------------------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Half-Yearly: Rs 1,000 at 10%", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Rate 5% for each half-year, 2 periods.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            given = self.hrow(
                chip("P = Rs 1,000", CHALK_GREEN, size=13),
                chip("R = 10% p.a.", CHALK_AMBER, size=13),
                chip("TIME = 1 YEAR", CHALK_CYAN, size=13),
                y=1.45, gap=0.50)
            # the money itself, drawn: rupee coins with thickness beside the
            # principal and beside the payout, and a fanned bundle of notes
            # under each -- the working keeps its own clear column between them
            coins = coin_stack(-4.15, 1.42, 3)
            coins2 = coin_stack(3.30, 0.85, 4)
            seed = note_stack(-3.35, -0.45, 3, "Rs 1,000", 11, CHALK_YELLOW)
            paid = note_stack(4.05, -0.45, 3, "Rs 1,102.50", 11, CHALK_GREEN)

            rate = at(chip("RATE PER PERIOD = 10/2 = 5%", CHALK_AMBER, size=13),
                      -2.60, 0.78)
            periods = at(chip("PERIODS = 2", CHALK_CYAN, size=13), 0.85, 0.78)
            amount = at(chalk_math(r"A = 1000(1.05)^{2} = 1102.50", size=28,
                                   color=CHALK_GREEN), BOARD_CX, -0.45)

            banner = at(board_text("AMOUNT = Rs 1,102.50", 18, CHALK_YELLOW,
                                   "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("CI = 1102.50 - 1000 = Rs 102.50", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(given, shift=UP * 0.06),
                      FadeIn(coins, scale=0.9),
                      FadeIn(seed, scale=0.92), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(rate, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(periods, shift=LEFT * 0.10),
                      FadeIn(coins2, scale=0.9), FadeIn(paid, scale=0.92),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(amount, shift=UP * 0.06),
                      FadeIn(banner, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: quarterly -- the same rule, extended to four periods -------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("Quarterly: R/4 and 4n", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A year has four quarters.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            face = clock_face(-2.55, 0.35)
            sec4 = clock_sectors(-2.55, 0.35, 4)
            lab4 = dial_label(-2.55, 0.35, "QUARTERLY")
            extend = at(chip("SAME RULE, EXTENDED", CHALK_GREEN, size=13),
                        0.45, 0.35)
            rate = at(chip("RATE = R/4 PER QUARTER", CHALK_AMBER, size=13),
                      2.90, 1.25)
            periods = at(chip("PERIODS = 4n", CHALK_CYAN, size=14), 2.90, 0.55)
            formula = at(chalk_math(r"A = P\left(1 + \frac{R}{400}\right)^{4n}",
                                    size=26, color=CHALK_YELLOW), 2.90, -0.40)

            banner = at(board_text("THE SAME CONVERSION-PERIOD RULE", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Quarterly extends the rule from two periods "
                                  "to four.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(face), FadeIn(sec4), FadeIn(lab4),
                      FadeIn(extend, scale=0.95), run_time=0.65)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(rate, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(periods, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(formula, shift=UP * 0.06),
                      FadeIn(banner, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: population growth -- the new total is the next base --------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("Population Growth Is Compound", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The new total becomes the next base.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fact = at(chip("VILLAGE = 6,250 PEOPLE", CHALK_CYAN, size=13),
                      -2.45, 1.35)
            grow = at(chip("GROWTH = 8% EACH YEAR", CHALK_GREEN, size=13),
                      2.55, 1.35)
            town = village(-2.45, 0.30)
            bars = VGroup(
                Rectangle(width=0.30, height=0.30, stroke_width=0,
                          fill_color=CHALK_GREEN, fill_opacity=0.45),
                Rectangle(width=0.30, height=0.45, stroke_width=0,
                          fill_color=CHALK_GREEN, fill_opacity=0.55),
                Rectangle(width=0.30, height=0.62, stroke_width=0,
                          fill_color=CHALK_GREEN, fill_opacity=0.65),
            ).arrange(RIGHT, buff=0.14, aligned_edge=DOWN)
            bars.move_to(np.array([2.55, 0.10, 0.0]))
            rising = arrow_between((2.05, -0.02), (3.15, 0.70), CHALK_YELLOW)

            y1 = at(chip("YEAR 1: 6250 × 1.08 = 6750", CHALK_AMBER, size=13),
                    -2.30, -0.62)
            y2 = at(chip("YEAR 2: 6750 × 1.08 = 7290", CHALK_PINK, size=13),
                    2.85, -0.62)
            banner = at(board_text("6250 × (1.08)^2 = 7,290", 18, CHALK_YELLOW,
                                   "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Repeated increase uses the new total each "
                                  "time.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(town, scale=0.92),
                      FadeIn(fact, shift=UP * 0.06),
                      FadeIn(grow, shift=UP * 0.06), run_time=0.65)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(y1, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(LaggedStart(*[FadeIn(b, scale=0.85) for b in bars],
                                  lag_ratio=0.3),
                      GrowArrow(rising), run_time=0.65)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(y2, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: depreciation -- what remains, and the bouncing ball --------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("Depreciation: Keeping (100 - R)%", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A reduction in value due to use and age.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            keeps = at(chip("KEEPS (100 - R)% EACH TIME", CHALK_CYAN, size=13),
                       2.70, 1.38)
            # the depreciating assets, drawn and shaded: a television and a car
            tv = tv_icon(-3.55, 0.62)
            car = car_icon(-2.45, 0.56)
            bar_full = value_bar(-2.55, -0.05, frac=1.0, label="100%",
                                 color=CHALK_GREEN)
            bar_90 = value_bar(-2.55, -0.05, frac=0.90, label="90%",
                               color=CHALK_AMBER)
            # the ball loses a tenth of its height at every bounce: the drop and
            # all three heights (25 m, 22.5 m, 20.25 m) are drawn on the board
            ball = bounce_track(2.70, -0.10)

            formula = at(chalk_math(r"V = P\left(1 - \frac{R}{100}\right)^{n}",
                                    size=26, color=CHALK_YELLOW), -2.60, 1.38)
            ball_note = at(chip("25 → 22.5 → 20.25 m", CHALK_PINK,
                                size=13), 2.70, -0.66)

            banner = at(board_text("25 × 0.9 × 0.9 = 20.25 m", 18, CHALK_YELLOW,
                                   "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Depreciation keeps the remaining value "
                                  "each time.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(tv, scale=0.92), FadeIn(car, scale=0.92),
                      FadeIn(bar_full), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(keeps, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(ReplacementTransform(bar_full, bar_90), run_time=0.55)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(formula, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(ball), FadeIn(ball_note, shift=UP * 0.06),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.75)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: one structure, three uses ----------------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("One Structure, Three Uses", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Growth multiplies up, depreciation down.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            up_card = at(note_card("GROWTH", ["P(1 + r)^n"], CHALK_GREEN),
                         -2.30, 1.10)
            down_card = at(note_card("DEPRECIATION", ["P(1 - r)^n"], CHALK_PINK),
                           2.30, 1.10)
            how = at(chip("HOW OFTEN?", CHALK_CYAN, size=14), -1.20, 0.05)
            which = at(chip("UP OR DOWN?", CHALK_AMBER, size=14), 0.70, 0.05)
            up_bar, down_bar = meter(3.70, -0.25)

            banner = at(board_text("GROWTH ADDS, DEPRECIATION KEEPS", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("They differ only in the sign of the "
                                  "factor.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(up_card, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(down_card, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(up_bar, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(down_bar, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(how, shift=UP * 0.06),
                      FadeIn(which, shift=UP * 0.06),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the five-step decision map ---------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("Five Steps to Apply It", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Period, rate, factor, repeat.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            steps = self.hrow(
                chip("1 · CONVERSION PERIOD", CHALK_GREEN, size=13),
                chip("2 · RATE PER PERIOD", CHALK_AMBER, size=13),
                chip("3 · NUMBER OF PERIODS", CHALK_CYAN, size=13),
                y=1.35, gap=0.40)
            steps2 = self.hrow(
                chip("4 · PLUS FOR GROWTH", CHALK_GREEN, size=13),
                chip("5 · MINUS FOR DECREASE", CHALK_PINK, size=13),
                y=0.45, gap=0.50)
            rule = at(chip("RATE AND PERIODS CHANGE TOGETHER", CHALK_YELLOW,
                           size=13), BOARD_CX, -0.60)

            banner = at(board_text("PERIOD → RATE → FACTOR → REPEAT", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Five steps, every time.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(steps[0], shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(steps[1], shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(steps[2], shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(steps2[0], shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(steps2[1], shift=UP * 0.06),
                      FadeIn(rule, scale=0.95), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
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
            sub = at(board_text("Three questions and a quick check.", 16,
                                CHALK_WHITE, "BOLD"), BOARD_CX, 2.20)

            pic_a = VGroup(
                board_text("Rs 12,000 · 10% p.a.", 12, CHALK_GREEN, "BOLD"),
                board_text("time 1.5 years", 12, CHALK_GREEN, "BOLD"),
            ).arrange(DOWN, buff=0.24)
            pic_b = VGroup(
                board_text("12% p.a. · 2 years", 12, CHALK_CYAN, "BOLD"),
                board_text("rate? periods?", 12, CHALK_CYAN, "BOLD"),
            ).arrange(DOWN, buff=0.24)
            pic_c = VGroup(
                board_text("TV = Rs 21,000", 12, CHALK_AMBER, "BOLD"),
                board_text("5% in one year", 12, CHALK_AMBER, "BOLD"),
            ).arrange(DOWN, buff=0.24)
            pic_d = VGroup(
                board_text("8% growth → ?", 12, CHALK_PINK, "BOLD"),
                board_text("8% fall → ?", 12, CHALK_PINK, "BOLD"),
            ).arrange(DOWN, buff=0.24)

            qa = at(self.q_card("A · HALF-YEARLY", pic_a, CHALK_GREEN),
                    -2.72, 1.05)
            qb = at(self.q_card("B · QUARTERLY", pic_b, CHALK_CYAN), 3.72, 1.05)
            qc = at(self.q_card("C · DEPRECIATION", pic_c, CHALK_AMBER),
                    -2.72, -1.05)
            qd = at(self.q_card("D · QUICK CHECK", pic_d, CHALK_PINK),
                    3.72, -1.05)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(qa, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(qb, shift=LEFT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(qc, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(qd, shift=LEFT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)
            self.closing(tracker, qd)
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
            a1 = at(self.answer_row("A", "Rs 12,000 × (1.05)^3",
                                    "= Rs 13,891.50 · 5%, 3 periods",
                                    CHALK_GREEN), BOARD_CX, 1.62)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "3% per quarter, 8 quarters",
                                    "A = P(1.03)^8", CHALK_CYAN),
                    BOARD_CX, 0.82)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "Rs 21,000 × 0.95",
                                    "= Rs 19,950 · 95% remains", CHALK_AMBER),
                    BOARD_CX, 0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "growth 1.08",
                                    "depreciation 0.92 · 1 - 0.08", CHALK_PINK),
                    BOARD_CX, -0.78)
            self.play(FadeIn(a4, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, a4)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 10: the whole lesson gathered on one board --------------------
    def beat_s10(self) -> None:
        """The summary: the conversion period's three cases, the two mixed
        formulas, and the five-step map -- one board, in the order the lesson
        taught them."""
        with self.voiceover(text=NARRATION["s10"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Whole Lesson on One Board", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Period · Rate · Formula · Five Steps", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            cases = self.hrow(
                chip("ANNUAL: R · n", CHALK_GREEN, size=13),
                chip("HALF-YEARLY: R/2 · 2n", CHALK_AMBER, size=13),
                chip("QUARTERLY: R/4 · 4n", CHALK_CYAN, size=13),
                y=1.45, gap=0.45)

            growth = self.formula_block(
                "GROWTH: MONEY & POPULATION",
                chalk_math(r"A = P\left(1 + \frac{R}{100}\right)^{n}", size=26,
                           color=CHALK_GREEN), CHALK_GREEN, -2.55, 0.42)
            decay = self.formula_block(
                "DEPRECIATION: VALUE",
                chalk_math(r"V = P\left(1 - \frac{R}{100}\right)^{n}", size=26,
                           color=CHALK_PINK), CHALK_PINK, 2.55, 0.42)

            chain = at(chip("1 PERIOD → 2 RATE → 3 COUNT → 4 +/- → 5 REPEAT",
                            CHALK_YELLOW, size=13), BOARD_CX, -0.66)
            banner = at(board_text("PERIOD · RATE · FORMULA · FIVE STEPS", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("One structure: period, rate, factor, "
                                  "repeat.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(cases[0], shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(cases[1], shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(cases[2], shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(growth, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(decay, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(chain, scale=0.95),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.80)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, chain)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 11: recap and the spoken thank-you ----------------------------
    def beat_s11(self) -> None:
        with self.voiceover(text=NARRATION["s11"]) as tracker:
            self.reset_board()

            heading = at(board_text("Period · Rate · Factor · Repeat", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)

            r1 = at(self.answer_row("1", "CONVERSION PERIOD",
                                    "annually, half-yearly, quarterly",
                                    CHALK_GREEN), BOARD_CX, 1.48)
            r2 = at(self.answer_row("2", "GROWTH",
                                    "P(1 + R/100)^n: money and people",
                                    CHALK_CYAN), BOARD_CX, 0.72)
            r3 = at(self.answer_row("3", "DEPRECIATION",
                                    "P(1 - R/100)^n: the remaining value",
                                    CHALK_PINK), BOARD_CX, -0.04)
            r4 = at(self.answer_row("4", "TWO DECISIONS",
                                    "how often, and up or down",
                                    CHALK_AMBER), BOARD_CX, -0.80)
            strip = at(board_text("Period, rate, factor, repeat.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)
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
            # the strip is written on its own bookmark as the voice says
            # "Period, rate, factor, repeat.", and only the bookmark in front of
            # "Thank you for watching," clears the board and brings in the card.
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

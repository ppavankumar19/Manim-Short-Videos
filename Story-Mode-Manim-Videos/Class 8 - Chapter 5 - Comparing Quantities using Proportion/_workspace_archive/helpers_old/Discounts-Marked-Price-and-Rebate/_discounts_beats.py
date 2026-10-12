    # ================================================================ beats ==
    # Discounts, Marked Price & Rebate (Class 8 Maths, Chapter 5, Storymode 02).
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
    #   * every row of cards is centred on BOARD_CX (`hrow` / `row_centres`) and
    #     two texts never come closer than the 0.22 units the clearance audit
    #     asks for -- which is why every card spaces its own lines by 0.26;
    #   * the marked price never leaves the board: the tag stays up through the
    #     scene while the discount is cut away from the bar, and the discount
    #     AMOUNT (rupees) is always drawn apart from the discount RATE (percent);
    #   * a drawn cross always lives in the same VGroup as the statement it
    #     strikes through (otherwise the audit reads the strokes as a line
    #     running into somebody else's card);
    #   * the challenge uses the series' shared 10-second THINK clock, dead
    #     centre of the board, and the four prompt cards sit in the four corners
    #     so the badge never covers one.

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

    def answer_row(self, tag, headline, note, color, width=8.60, height=0.62,
                   pad=0.30, buff=0.34):
        """One revealed step or answer: its number, the work and the result.

        The row is laid out in FIXED COLUMNS rather than centred in its box, so
        the number column and the text columns are the same vertical line in
        every row (centring put each number at a different x).  The box itself
        stays where the caller puts it.  The same helper draws the recap list.
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
        grp = VGroup(box, row)
        grp.box, grp.row = box, row
        return grp

    def q_card(self, title, pict, color=CHALK_CYAN, width=3.00, pad=0.14,
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

    # -- Scene 0: title ------------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            heading = at(board_text("Discounts, Marked Price & Rebate", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The tag price is not always the price you pay.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            tag = at(price_tag("Rs 1600", size=24), BOARD_CX, 1.05)
            sticker = price_sticker("6% OFF", 2.45, 1.45, r=0.52)

            c1 = chip("MARKED PRICE (MP)", CHALK_GREEN, size=15)
            c2 = chip("DISCOUNT / REBATE", CHALK_AMBER, size=15)
            c3 = chip("SELLING PRICE (SP)", CHALK_CYAN, size=15)
            self.hrow(c1, c2, c3, y=-0.30, gap=0.45)

            formula = at(chalk_math(r"\text{MP} - \text{Discount} = \text{SP}",
                                    size=30, color=CHALK_YELLOW),
                         BOARD_CX, BANNER_Y)
            strip = at(board_text("The tagged price never disappears: the "
                                  "discount is a part of it.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(tag, scale=0.9), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(sticker, scale=0.85), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(c1, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(c2, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(c3, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(formula, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: the three parts, and the relation --------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Three Parts of a Price", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Marked price, discount, selling price.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            c1 = list_card("MARKED PRICE",
                           ["price written on the article",
                            "also called the list price"], CHALK_GREEN,
                           width=2.90, height=1.47)
            c2 = list_card("DISCOUNT",
                           ["the amount reduced",
                            "also called the rebate"], CHALK_AMBER,
                           width=2.90, height=1.47)
            c3 = list_card("SELLING PRICE",
                           ["what is actually paid",
                            "SP = MP - D"], CHALK_CYAN,
                           width=2.90, height=1.47)
            for card, cx in zip((c1, c2, c3),
                                row_centres((1.45, 1.45, 1.45), 0.45)):
                at(card, cx, 1.02)

            formula = at(chalk_math(r"\text{MP} - \text{Discount} = \text{SP}",
                                    size=28, color=CHALK_YELLOW), 1.60, -0.45)
            tag = at(price_tag("Rs 80", size=22), -3.20, -0.45)
            strip = at(board_text("The discount is always calculated from the "
                                  "marked price.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(c1, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(c2, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(c3, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(formula, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(tag, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: the book -- find the discount, then the SP -----------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Discount Comes First", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A book marked Rs 80 at 15% off.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            book = at(book_icon(0, 0, "Rs 80", CHALK_CYAN, scale=1.0),
                      -3.35, 1.42)
            sticker = price_sticker("15% OFF", -2.05, 1.60, r=0.48)

            r1 = at(self.answer_row("1", "DISCOUNT = 15/100 × 80", "= Rs 12",
                                    CHALK_GREEN, width=6.30), 1.75, 1.60)
            r2 = at(self.answer_row("2", "SP = 80 - 12", "= Rs 68", CHALK_CYAN,
                                    width=6.30), 1.75, 0.90)

            # the marked price bar: 100% is Rs 80, and the 15% block is cut off
            bar = split_bar(-1.0, 0.05, width=BAR_W, cut=0.15,
                            sp_text="SP = 85% of MP", sp_size=14, slide=1.10)
            arrow = bar_arrow(-1.0, -0.32, width=BAR_W)
            mp_lab = at(board_text("100% = MP = Rs 80", 14, CHALK_WHITE,
                                   "BOLD"), -1.0, -0.48)
            d_lab = board_text("DISCOUNT 15% = Rs 12", 14, CHALK_PINK, "BOLD")
            d_lab.move_to(np.array([bar.slot_x + d_lab.width / 2.0,
                                    bar.slot_y, 0.0]))
            coins = at(coin_stack(0, 0, 3, 0.9), 4.60, -0.55)

            formula = at(chalk_math(r"\text{MP} - \text{Discount} = \text{SP}",
                                    size=28, color=CHALK_YELLOW),
                         BOARD_CX, BANNER_Y)
            strip = at(board_text("The discount is always calculated on the "
                                  "marked price.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(book, scale=0.9), FadeIn(sticker, scale=0.85),
                      run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(bar, scale=0.95), FadeIn(arrow), FadeIn(mp_lab),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(r1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(r2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(bar.disc.animate.shift(bar.delta),
                      bar.cut_mark.animate.set_stroke(opacity=1),
                      FadeIn(d_lab, shift=UP * 0.06), FadeIn(coins, scale=0.9),
                      run_time=0.70)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(formula, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: the cycle -- from the two prices to the discount percent ---
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Finding the Discount Percent", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A cycle marked Rs 3600, sold for Rs 3312.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            bike = at(cycle_icon(0, 0, "Rs 3600", CHALK_AMBER, scale=0.92),
                      -3.50, 1.30)
            pair = price_pair(1.00, 1.10, 6.00, mp_text="MP = Rs 3600",
                              sp_text="SP = Rs 3312", frac=0.92)
            rs = at(board_text("Rs 288", 16, CHALK_PINK, "BOLD"), 4.45, 1.10)

            diff = at(chip("DISCOUNT = 3600 - 3312 = Rs 288", CHALK_AMBER,
                           size=14), BOARD_CX, -0.35)
            base = at(chip("THE BASE IS THE MARKED PRICE", CHALK_PINK,
                           size=14), BOARD_CX, -0.95)
            percent = at(chip("d% = 288/3600 × 100 = 8%", CHALK_YELLOW,
                              size=15), BOARD_CX, -0.35)
            strip = at(board_text("Always divide by the marked price, and never "
                                  "by the selling price.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(bike, scale=0.9), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(pair, scale=0.96), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(rs, scale=0.9), FadeIn(diff, shift=UP * 0.06),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(base, shift=UP * 0.06),
                      pair.gap.animate.shift(pair.gap_delta),
                      rs.animate.shift(pair.gap_delta), run_time=0.65)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeOut(diff), FadeIn(percent, shift=UP * 0.06),
                      run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: the fan -- given the percent, find the selling price -------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("Given the Discount, Find the SP", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A fan marked Rs 1600 with 6% off.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fan = at(fan_icon(0, 0, "Rs 1600", CHALK_CYAN, scale=0.95),
                     -3.55, 1.30)
            sticker = price_sticker("6% OFF", -2.62, 1.70, r=0.46)

            r1 = at(self.answer_row("1", "DISCOUNT = 6/100 × 1600", "= Rs 96",
                                    CHALK_GREEN, width=6.40), 1.80, 1.55)
            r2 = at(self.answer_row("2", "SP = 1600 - 96", "= Rs 1504",
                                    CHALK_CYAN, width=6.40), 1.80, 0.85)

            amt = chip("DISCOUNT AMOUNT = Rs 96", CHALK_AMBER, size=14)
            neq = chalk_math(r"\neq", size=26, color=CHALK_RED)
            rate = chip("DISCOUNT RATE = 6%", CHALK_PINK, size=14)
            self.hrow(amt, neq, rate, y=-0.45, gap=0.45)
            notes = at(note_stack(0, 0, 3, 0.9), 4.20, -0.45)

            strip = at(board_text("The amount is in rupees; the rate is a "
                                  "percentage of the marked price.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(fan, scale=0.9), FadeIn(sticker, scale=0.85),
                      run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(r1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(r2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(amt, scale=0.9), FadeIn(rate, scale=0.9),
                      FadeIn(neq, scale=0.9), FadeIn(notes, scale=0.9),
                      run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: the shortcut -- what remains is (100 - d)% ----------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Shortcut: What Remains", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("If 6% is taken off, 94% remains.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            r1 = at(self.answer_row("1", "FIND D, THEN SUBTRACT",
                                    "Rs 96, then 1600 - 96", CHALK_GREEN,
                                    width=8.60), BOARD_CX, 1.60)
            r2 = at(self.answer_row("2", "FIND WHAT REMAINS",
                                    "94/100 × 1600 = Rs 1504", CHALK_CYAN,
                                    width=8.60), BOARD_CX, 0.90)

            # the same thousand-six-hundred bar: 6% is cut away, 94% stays
            bar = split_bar(-1.0, 0.05, width=BAR_W, cut=0.06,
                            sp_text="SP = 94% of MP", sp_size=14, slide=1.60,
                            slot_side="left")
            arrow = bar_arrow(-1.0, -0.32, width=BAR_W)
            mp_lab = at(board_text("100% = MP = Rs 1600", 14, CHALK_WHITE,
                                   "BOLD"), -1.0, -0.48)
            d_lab = board_text("6% = Rs 96", 14, CHALK_PINK, "BOLD")
            d_lab.move_to(np.array([bar.slot_x + d_lab.width / 2.0,
                                    bar.slot_y, 0.0]))

            tick1 = tick(np.array([5.05, 1.60, 0.0]))
            tick2 = tick(np.array([5.05, 0.90, 0.0]))
            same = at(chip("BOTH ROUTES GIVE Rs 1504", CHALK_YELLOW, size=14),
                      3.15, -0.55)
            formula = at(chalk_math(
                r"SP = \frac{100 - d}{100} \times MP", size=24,
                color=CHALK_YELLOW), BOARD_CX, BANNER_Y)
            strip = at(board_text("Both routes land on the same selling price, "
                                  "Rs 1504.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(bar, scale=0.95), FadeIn(arrow), FadeIn(mp_lab),
                      run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(bar.disc.animate.shift(bar.delta),
                      bar.cut_mark.animate.set_stroke(opacity=1),
                      FadeIn(d_lab, shift=UP * 0.06), run_time=0.65)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(r1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(r2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(tick1, scale=0.8), FadeIn(tick2, scale=0.8),
                      FadeIn(same, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(formula, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: which formula? --------------------------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("Which Formula Do I Need?", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Look at what the question gives you.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            c1 = list_card("MP + DISCOUNT %",
                           ["find the discount", "then SP = MP - D"],
                           CHALK_GREEN, width=2.90, height=1.47)
            c2 = list_card("MP + SP",
                           ["find D = MP - SP", "then D / MP × 100"],
                           CHALK_CYAN, width=2.90, height=1.47)
            c3 = list_card("MP + DISCOUNT Rs",
                           ["SP = MP - D", "the discount is given"],
                           CHALK_AMBER, width=2.90, height=1.47)
            for card, cx in zip((c1, c2, c3),
                                row_centres((1.45, 1.45, 1.45), 0.45)):
                at(card, cx, 1.05)

            first = at(chip("FIRST FIND THE DISCOUNT", CHALK_YELLOW, size=15),
                       BOARD_CX, BAND_B)
            banner = at(board_text("THE BASE IS ALWAYS THE MARKED PRICE", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Read the question twice, and pick the route "
                                  "that fits.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(c1, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(c2, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(c3, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(first, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: the four mistakes, and the fix for each --------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Common Mistakes and Their Fixes", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Four wrong ideas, four corrections.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            cards = (
                ("d% = D / SP × 100", "the base is the marked price, not SP"),
                ("SP = MP + D", "subtract: SP = MP - D"),
                ("6% = Rs 6", "6% is the rate, Rs 96 the amount"),
                ("15% off means pay 15%", "85% is still payable"),
            )
            centres = row_centres((2.025, 2.025), 0.42)
            rows = (1.10, -0.30)
            built = []
            for i, (wrong, fix) in enumerate(cards):
                card = mistake_card(wrong, fix, CHALK_RED, width=4.05,
                                    height=1.10)
                at(card, centres[i % 2], rows[i // 2])
                built.append(card)
            m1, m2, m3, m4 = built

            checks = self.hrow(chip("BASE = MP", CHALK_GREEN, size=14),
                               chip("SUBTRACT, NEVER ADD", CHALK_YELLOW,
                                    size=14),
                               chip("RATE % vs AMOUNT Rs", CHALK_CYAN,
                                    size=14), y=-1.15, gap=0.40)
            strip = at(board_text("Check the base, the sign, and the units, "
                                  "every time.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(m1, scale=0.92), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(m2, scale=0.92), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(m3, scale=0.92), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(m4, scale=0.92), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(checks, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: does the answer make sense? --------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("Does the Answer Make Sense?", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Check the selling price against the marked "
                                "price.", 17, CHALK_WHITE, "BOLD"),
                     BOARD_CX, SUB_Y)

            c1 = list_card("A DISCOUNT SHRINKS SP",
                           ["so always check SP < MP"], CHALK_GREEN,
                           width=3.60, height=1.05, head_size=14)
            c2 = list_card("d% OFF LEAVES (100 - d)%",
                           ["6% off leaves 94% payable"], CHALK_PINK,
                           width=3.60, height=1.05, head_size=14)
            for card, cx in zip((c1, c2), row_centres((1.80, 1.80), 0.50)):
                at(card, cx, 1.20)

            pair = price_pair(0.50, 0.20, 5.60, mp_text="MP = Rs 1600 = 100%",
                              sp_text="SP = Rs 1504 = 94%", frac=0.94)
            check = at(chip("SO SP < MP: THE CHECK PASSES", CHALK_YELLOW,
                            size=15), BOARD_CX, BANNER_Y)
            good = tick(np.array([3.35, -0.35, 0.0]))
            strip = at(board_text("Check SP < MP, and check that d plus "
                                  "(100 - d) makes 100.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(c1, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(c2, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(pair, scale=0.96), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(good, scale=0.8), FadeIn(check, scale=0.9),
                      run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
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

            pic_a = VGroup(board_text("MP = Rs 450, 7% off", 12, CHALK_GREEN,
                                      "BOLD"),
                           board_text("find D, then SP", 12, CHALK_GREEN,
                                      "BOLD")).arrange(DOWN, buff=0.26)
            pic_b = VGroup(board_text("MP = Rs 1000", 12, CHALK_CYAN, "BOLD"),
                           board_text("SP = Rs 900: find D%", 12, CHALK_CYAN,
                                      "BOLD")).arrange(DOWN, buff=0.26)
            pic_c = VGroup(board_text("MP = Rs 250, 5% off", 12, CHALK_AMBER,
                                      "BOLD"),
                           board_text("find SP using 95%", 12, CHALK_AMBER,
                                      "BOLD")).arrange(DOWN, buff=0.26)
            pic_d = VGroup(board_text("is SP smaller than MP?", 12, CHALK_PINK,
                                      "BOLD"),
                           board_text("check every answer", 12, CHALK_PINK,
                                      "BOLD")).arrange(DOWN, buff=0.26)

            qa = at(self.q_card("A · SHIRT", pic_a, CHALK_GREEN), -2.85, 0.80)
            qb = at(self.q_card("B · ARTICLE", pic_b, CHALK_CYAN), 3.65, 0.80)
            qc = at(self.q_card("C · TABLE", pic_c, CHALK_AMBER), -2.85, -0.95)
            qd = at(self.q_card("D · CHECK", pic_d, CHALK_PINK), 3.65, -0.95)

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

            # the questions are read: hold the board for the rest of the window
            self.closing(tracker)
            self._capture_srt(tracker)

        # The ten-second THINK pause is deliberately SILENT: the questions have
        # just been read, so the clock ticks alone, with no narration to sync
        # against.
        play_challenge_countdown(self, seconds=10, sfx=self.sfx,
                                 position=np.array([BOARD_CX, BOARD_CY, 0]))

        with self.voiceover(text=NARRATION["s9a"]) as tracker:
            self.wait(leftover(tracker, "b0"))
            self.play(FadeOut(qa), FadeOut(qb), FadeOut(qc), FadeOut(qd),
                      run_time=0.55)
            a1 = at(self.answer_row("A", "discount Rs 31.50",
                                    "SP = 450 - 31.50 = Rs 418.50",
                                    CHALK_GREEN), BOARD_CX, 1.50)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "discount Rs 100",
                                    "d% = 100/1000 × 100 = 10%", CHALK_CYAN),
                    BOARD_CX, 0.70)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "95% remains",
                                    "SP = 95/100 × 250 = Rs 237.50",
                                    CHALK_AMBER), BOARD_CX, -0.10)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            strip = at(board_text("The base is the marked price, and SP is "
                                  "always smaller than MP.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap and the spoken thank-you ----------------------------
    def beat_s10(self) -> None:
        with self.voiceover(text=NARRATION["s10"]) as tracker:
            self.reset_board()

            heading = at(board_text("Marked Price to Selling Price", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)

            r1 = at(self.answer_row("1", "MARKED PRICE",
                                    "the price written on the article (MP)",
                                    CHALK_GREEN), BOARD_CX, 1.48)
            r2 = at(self.answer_row("2", "DISCOUNT OR REBATE",
                                    "the amount reduced: SP = MP - D",
                                    CHALK_CYAN), BOARD_CX, 0.72)
            r3 = at(self.answer_row("3", "DISCOUNT PERCENT",
                                    "D% = (MP - SP) / MP × 100",
                                    CHALK_YELLOW), BOARD_CX, -0.04)
            r4 = at(self.answer_row("4", "THE PRICE FLOW",
                                    "tag, reduce, pay, compare", CHALK_AMBER),
                    BOARD_CX, -0.80)
            strip = at(board_text("Keep the marked price visible, subtract the "
                                  "discount, check the answer.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)
            thanks = at(board_text("Thank You for Watching!", 30, CHALK_WHITE,
                                   "BOLD"), BOARD_CX, 0.62)
            bye = at(board_text("See you in the next lesson :)", 22,
                                CHALK_YELLOW, "BOLD"), BOARD_CX, -0.32)

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

            # The four lines stay on the board through the whole closing
            # sentence: the strip is written on its own bookmark as the voice
            # says it, and only the bookmark in front of "Thank you for
            # watching," clears the board and brings in the card.
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

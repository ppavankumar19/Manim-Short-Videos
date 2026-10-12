    # ================================================================ beats ==
    # Compound Ratio & Inverse Ratio: Applications in Business Profit Sharing
    # (Class 8 Maths, Chapter 5, Storymode 01).
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
    #     is why the cards space their own lines by 0.22 or more;
    #   * the two partners' cards are the same furniture in every scene, so
    #     Ramayya and Gopalam stay recognisable;
    #   * a drawn cross always lives in the same VGroup as the chip it strikes
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

    def partner_row(self, months_a="12 months", months_b="9 months",
                    money_b="Rs 3,000", y=BAND_A):
        """The two partners' cards, side by side and centred on the board."""
        ca, cb = row_centres((CARD_W / 2, CARD_W / 2), 0.50)
        a = at(partner_card(RAMAYYA[0], RAMAYYA[1], months_a, RAMAYYA[3]), ca, y)
        b = at(partner_card(GOPALAM[0], money_b, months_b, GOPALAM[3]), cb, y)
        return a, b

    def q_card(self, title, pict, color=CHALK_CYAN, width=3.00, pad=0.12,
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

    # -- Scene 0: title ------------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = at(board_text("Two Partners, One Profit", 26, CHALK_PINK,
                                  "BOLD"), BOARD_CX, 2.06)
            sub = at(board_text("Ramayya and Gopalam: money and time together.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, 1.46)

            a_card, b_card = self.partner_row()
            bag = money_bag(BOARD_CX, -0.32, 1.02)

            ask = at(board_text("SHOULD THEY SHARE IT EQUALLY?", 18,
                                CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Profit is shared in the ratio of what each "
                                  "partner contributed.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(title, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(a_card, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(b_card, shift=LEFT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(bag, scale=0.9), run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(ask, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: a ratio is ordered; the inverse swaps the terms -------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("A Ratio Is an Ordered Comparison", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Three to two is not two to three.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            c32 = ratio_card(3, 2, CHALK_GREEN)
            neq = chalk_math(r"\neq", size=30, color=CHALK_RED)
            c23 = ratio_card(2, 3, CHALK_PINK)
            row = self.hrow(c32, neq, c23, y=BAND_A, gap=0.60)

            # the inverse: one card turns over on the spot and reads b : a
            swap = at(ratio_card("a", "b", CHALK_AMBER, width=1.90, height=0.80,
                                 size=28), -0.20, BAND_B)
            flipped = at(ratio_card("b", "a", CHALK_PINK, width=1.90,
                                    height=0.80, size=28), -0.20, BAND_B)
            tag = at(chip("INVERSE", CHALK_PINK, size=14), 1.90, BAND_B)

            banner = at(board_text("THE INVERSE OF 4 : 5 IS 5 : 4", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Inverse means swap the two terms, never add "
                                  "them.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(c32, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(neq, scale=0.9), FadeIn(c23, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(swap, shift=UP * 0.08), run_time=0.40)
            self.play(Rotate(swap, PI, axis=UP), run_time=0.45)
            self.play(Transform(swap, flipped), FadeIn(tag, scale=0.9),
                      run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: the same time -- the time factor cancels --------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("Same Time for Both Partners", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The time factor cancels.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            a_card, b_card = self.partner_row(months_a="12 months",
                                              months_b="12 months")
            flow = self.hrow(
                chip("SAME TIME · 12 MONTHS EACH", CHALK_CYAN, size=13),
                chip("TIME CANCELS", CHALK_YELLOW, size=13),
                chip("CAPITAL 2000 : 3000 = 2 : 3", CHALK_GREEN, size=13),
                y=BAND_B, gap=0.40)
            banner = at(board_text("SO THE PROFIT IS DIVIDED 2 : 3", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("With the same time, the profit is divided "
                                  "2 : 3.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(a_card, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(b_card, shift=LEFT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(flow, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: the same capital -- the capital factor cancels --------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Same Capital, Different Time", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The capital factor cancels.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            ca, cb = row_centres((CARD_W / 2, CARD_W / 2), 0.50)
            a_card = at(partner_card("Ramayya", "Rs 5,000", "12 months",
                                     CHALK_GREEN), ca, BAND_A)
            b_card = at(partner_card("Gopalam", "Rs 5,000", "9 months",
                                     CHALK_PINK), cb, BAND_A)
            flow = self.hrow(
                chip("SAME CAPITAL · Rs 5,000 EACH", CHALK_CYAN, size=13),
                chip("CAPITAL CANCELS", CHALK_YELLOW, size=13),
                chip("TIME 12 : 9 = 4 : 3", CHALK_AMBER, size=13),
                y=BAND_B, gap=0.40)
            banner = at(board_text("SO THE PROFIT FOLLOWS 4 : 3", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("With the same capital, the profit follows "
                                  "the time ratio 4 : 3.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(a_card, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(b_card, shift=LEFT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(flow, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: both the money and the time differ -------------------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("Both Capital and Time Differ", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Neither ratio alone is enough.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            a_card, b_card = self.partner_row()
            cap = at(chip("CAPITAL 2000 : 3000 = 2 : 3", CHALK_GREEN, size=13),
                     -2.10, BAND_B)
            tim = at(chip("TIME 12 : 9 = 4 : 3", CHALK_AMBER, size=13),
                     1.25, BAND_B)
            comb = at(chip("COMBINE BOTH", CHALK_PINK, size=14), 3.85, BAND_B)

            banner = at(board_text("NEITHER RATIO ALONE CAN DECIDE", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("When both differ, the two ratios must be "
                                  "combined.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(a_card, shift=RIGHT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(b_card, shift=LEFT * 0.10), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(cap, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(tim, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(comb, scale=0.9),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: the compound ratio rule, and the mistake --------------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Compound Ratio Rule", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Multiply the corresponding terms.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            box = at(machine(4.60, 1.50), BOARD_CX, 0.62)
            slot1 = np.array([-2.60, 0.92, 0.0])
            slot2 = np.array([-2.60, 0.22, 0.0])
            in1 = at(ratio_card(2, 3, CHALK_GREEN, width=1.50, height=0.62,
                                size=22), -3.55, 0.92)
            in2 = at(ratio_card(4, 3, CHALK_AMBER, width=1.50, height=0.62,
                                size=22), -3.55, 0.22)
            formula = at(chalk_math(r"a:b \times c:d \rightarrow ac:bd", size=24,
                                    color=CHALK_YELLOW), BOARD_CX, 0.34)
            out = at(ratio_card("ac", "bd", CHALK_YELLOW, width=1.90,
                                height=0.70, size=24), BOARD_CX, -0.78)

            # the wrong idea: its card carries the drawn cross in the top half
            # and the formula under it, so the strike-through never runs into
            # the lettering (the audit measures that clearance)
            wrong = wrong_card("(a + c) : (b + d)", CHALK_RED, width=2.60,
                               height=1.05, size=15)
            wrong.move_to(np.array([3.85, 0.62, 0.0]))
            wrong_cross = wrong.cross
            wrong_cross.set_stroke(opacity=0)

            strip = at(board_text("A compound ratio multiplies corresponding "
                                  "terms; it never adds them.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(box, scale=0.95), FadeIn(in1, shift=RIGHT * 0.10),
                      FadeIn(in2, shift=RIGHT * 0.10), run_time=0.60)
            self.play(in1.animate.move_to(slot1), in2.animate.move_to(slot2),
                      run_time=0.55)
            self.play(FadeOut(in1), FadeOut(in2), run_time=0.35)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(formula, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(out, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(wrong, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(wrong_cross.animate.set_stroke(opacity=1),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: applying the rule, and the money x time cross-check ---------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("Applying the Compound Ratio", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Two to three, compounded with four to three.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            c1 = ratio_card(2, 3, CHALK_GREEN)
            times = chalk_math(r"\times", size=24, color=CHALK_WHITE)
            c2 = ratio_card(4, 3, CHALK_AMBER)
            arrow = arrow_between((0.0, 0.0), (0.60, 0.0), CHALK_YELLOW)
            c3 = ratio_card(8, 9, CHALK_YELLOW)
            row = self.hrow(c1, times, c2, arrow, c3, y=BAND_A, gap=0.42)

            m1 = chip("Rs 2000 × 12 = Rs 24,000", CHALK_GREEN, size=13)
            m2 = chip("Rs 3000 × 9 = Rs 27,000", CHALK_PINK, size=13)
            m3 = chip("24,000 : 27,000 = 8 : 9", CHALK_YELLOW, size=13)
            row2 = self.hrow(m1, m2, m3, y=BAND_B, gap=0.42)

            banner = at(board_text("CAPITAL AND TIME GIVE 8 : 9", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Money times time gives the same ratio, "
                                  "8 : 9.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(c1, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(times, scale=0.9), FadeIn(c2, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(GrowArrow(arrow), FadeIn(c3, scale=0.9), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(m1, shift=UP * 0.06), FadeIn(m2, shift=UP * 0.06),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(m3, shift=UP * 0.06),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, banner)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: from the ratio to rupees -----------------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("From Ratio to Rupees", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Divide the profit into equal parts.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            total = at(chip("PROFIT (EXAMPLE) = Rs 17,000", CHALK_GREEN,
                            size=14), -1.85, 1.32)
            parts = at(chip("8 + 9 = 17 EQUAL PARTS OF Rs 1,000", CHALK_AMBER,
                            size=13), 2.25, 1.32)

            blocks = profit_blocks(17, CHALK_CYAN, side=0.26, gap=0.08)
            for b in blocks[:8]:
                b.set_fill(CHALK_GREEN, 0.5).set_stroke(CHALK_GREEN)
            for b in blocks[8:]:
                b.set_fill(CHALK_PINK, 0.5).set_stroke(CHALK_PINK)
            at(blocks, BOARD_CX, 0.30)

            left_t = [np.array([-1.85 + (c - 1.5) * 0.34,
                                0.60 + (1 - r) * 0.34, 0.0])
                      for r in range(2) for c in range(4)]
            right_t = [np.array([2.25 + (c - 2.0) * 0.34,
                                 0.60 + (1 - r) * 0.34, 0.0])
                       for r in range(2) for c in range(5)][:9]

            ra = at(chip("RAMAYYA: 8 × Rs 1,000 = Rs 8,000", CHALK_GREEN,
                         size=13), -1.85, -0.62)
            go = at(chip("GOPALAM: 9 × Rs 1,000 = Rs 9,000", CHALK_PINK,
                         size=13), 2.25, -0.62)
            each = at(chip("EACH PART = Rs 1,000", CHALK_CYAN, size=13),
                      BOARD_CX, -1.32)

            strip = at(board_text("Rs 8,000 + Rs 9,000 = Rs 17,000: the whole "
                                  "profit is shared.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(total, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(parts, shift=UP * 0.06),
                      LaggedStart(*[FadeIn(b, scale=0.8) for b in blocks],
                                  lag_ratio=0.05), run_time=0.80)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(each, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(*[b.animate.move_to(t)
                        for b, t in zip(blocks[:8], left_t)],
                      FadeIn(ra, shift=UP * 0.06), run_time=0.70)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(*[b.animate.move_to(t)
                        for b, t in zip(blocks[8:], right_t)],
                      FadeIn(go, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.75)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the decision map -------------------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("Which Ratio Decides the Share?", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Time, capital, or both.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            c1 = note_card("SAME TIME", ["use the capital ratio"], CHALK_GREEN,
                           width=2.80, height=1.05)
            c2 = note_card("SAME CAPITAL", ["use the time ratio"], CHALK_CYAN,
                           width=2.80, height=1.05)
            c3 = note_card("BOTH DIFFERENT", ["use the compound ratio"],
                           CHALK_AMBER, width=2.80, height=1.05)
            row = self.hrow(c1, c2, c3, y=0.95, gap=0.45)

            rule = at(chip("PROFIT SHARE FOLLOWS CAPITAL × TIME", CHALK_YELLOW,
                           size=15), BOARD_CX, BAND_B)
            banner = at(board_text("BOTH DIFFERENT MEANS COMPOUND RATIO", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("A partner's share follows capital multiplied "
                                  "by time.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(c1, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(c2, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(c3, shift=UP * 0.06),
                      FadeIn(banner, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(rule, scale=0.9), FadeIn(strip, shift=UP * 0.06),
                      run_time=0.50)
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

            pic_a = chalk_math(r"7 : 5 \;\rightarrow\; ?", size=20,
                               color=CHALK_GREEN)
            pic_b = chalk_math(r"3 : 4 \times 2 : 3", size=20, color=CHALK_CYAN)
            pic_c = chalk_math(r"3 : 4 \times 5 : 4", size=20, color=CHALK_AMBER)
            pic_d = VGroup(board_text("P: Rs 4,000, 6 months", 12, CHALK_PINK,
                                      "BOLD"),
                           board_text("Q: Rs 3,000, 8 months", 12, CHALK_PINK,
                                      "BOLD")).arrange(DOWN, buff=0.24)

            qa = at(self.q_card("inverse of 7 : 5", pic_a, CHALK_GREEN),
                    -2.80, 0.92)
            qb = at(self.q_card("compound 3 : 4 and 2 : 3", pic_b, CHALK_CYAN),
                    3.70, 0.92)
            qc = at(self.q_card("3 : 4 with the inverse of 4 : 5", pic_c,
                                CHALK_AMBER), -2.80, -1.02)
            qd = at(self.q_card("P and Q: what ratio?", pic_d, CHALK_PINK),
                    3.70, -1.02)

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
            a1 = at(self.answer_row("A", "inverse of 7 : 5 is 5 : 7",
                                    "the inverse swaps the terms", CHALK_GREEN),
                    BOARD_CX, 1.62)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "3 : 4 and 2 : 3 give 6 : 12",
                                    "which simplifies to 1 : 2", CHALK_CYAN),
                    BOARD_CX, 0.82)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "3 : 4 with 5 : 4 give 15 : 16",
                                    "3 × 5 to 4 × 4", CHALK_AMBER),
                    BOARD_CX, 0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "Rs 24,000 : Rs 24,000",
                                    "so the ratio is 1 : 1", CHALK_PINK),
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

            heading = at(board_text("Inverse · Compound · Partnership", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)

            r1 = at(self.answer_row("1", "INVERSE RATIO",
                                    "swap the terms: a : b becomes b : a",
                                    CHALK_GREEN), BOARD_CX, 1.48)
            r2 = at(self.answer_row("2", "COMPOUND RATIO",
                                    "multiply corresponding terms: ac : bd",
                                    CHALK_CYAN), BOARD_CX, 0.72)
            r3 = at(self.answer_row("3", "PARTNERSHIP",
                                    "the share follows capital × time",
                                    CHALK_YELLOW), BOARD_CX, -0.04)
            r4 = at(self.answer_row("4", "SHARE THE PROFIT",
                                    "divide it into equal parts using the ratio",
                                    CHALK_AMBER), BOARD_CX, -0.80)
            strip = at(board_text("Money and time together decide the share.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)
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
            # the strip is written on its own bookmark as the voice says "Money
            # and time together decide the share.", and only the bookmark in
            # front of "Thank you for watching," clears the board and brings in
            # the card.
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

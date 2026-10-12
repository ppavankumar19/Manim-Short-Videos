    # ================================================================ beats ==
    # Profit, Loss & Overhead Expenses: Solving Single and Double Transaction
    # Problems (Class 8 Maths, Chapter 5, Storymode 02).
    #
    # SYNC RULE for every reveal: wait for the narration bookmark that starts
    # the phrase naming a thing, and only then bring it on.  Playing first and
    # waiting afterwards shows the picture a whole window early, which reads as
    # broken sync.
    #
    # Layout rules, so the audits stay clean:
    #   * the heading sits on the board's own heading line (2.72) and its
    #     sub-heading at 2.16, the closing strip at -1.80 -- nothing at all
    #     below CAPTION_SAFE_Y = -2.00;
    #   * every stacked pair of texts is at least 0.22 units apart, which is why
    #     the ledger rows sit 0.48 apart and every reveal is a short fade;
    #   * a drawn cross always lives in the SAME VGroup as the card it strikes
    #     through (`wrong_card`), so the audit never reads the strokes as a line
    #     running into somebody else's box;
    #   * the answer rows, the five steps and the recap list share one set of
    #     fixed columns (`answer_row`), so A/B/C/D and 1/2/3/4 sit on one
    #     vertical line;
    #   * the challenge uses the series' shared 10-second THINK clock, dead
    #     centre of the board, with the question cards in the four corners.

    def closing(self, tracker, mob=None, color=CHALK_YELLOW, run_time=None):
        """Consume the tail of the narration window on the last reveal."""
        budget = rt(tracker.get_remaining_duration()) if run_time is None \
            else run_time
        if mob is None:
            self.wait(max(budget, 0.0))
        else:
            self.play(Indicate(mob, color=color, scale_factor=1.03),
                      run_time=max(budget, MIN_RT))

    def answer_row(self, tag, headline, note, color, width=8.60, height=0.62,
                   pad=0.30):
        """One revealed row: its tag, the result and a short note.

        The cells sit in FIXED columns, not centred: the tag column and the
        name column are the same two vertical lines in every row of every list
        of this video (which is what keeps A/B/C/D and 1/2/3/4 on one line) and
        the note is flush with the row's own right edge.  Centring put each tag
        at a different x.
        """
        box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                               stroke_color=color, stroke_width=1.8,
                               fill_color=PANEL_FILL, fill_opacity=0.60)
        lab = board_text(tag, 15, color, "BOLD")
        name = board_text(headline, 14, color, "BOLD")
        txt = board_text(note, 13, CHALK_WHITE, "BOLD")
        x0 = box.get_left()[0] + pad
        cy = box.get_center()[1]
        lab.move_to(np.array([x0 + 0.19, cy, 0.0]))
        name.move_to(np.array([x0 + 0.62 + name.width / 2.0, cy, 0.0]))
        txt.move_to(np.array([box.get_right()[0] - pad - txt.width / 2.0,
                              cy, 0.0]))
        grp = VGroup(box, lab, name, txt)
        grp.box, grp.tag, grp.name, grp.note = box, lab, name, txt
        return grp

    def q_card(self, title, lines, color=CHALK_CYAN, width=3.50, pad=0.14,
               title_size=13, line_size=12, buff=0.28):
        """One 'your turn' card: a prompt over the figures it asks about."""
        head = board_text(title, title_size, color, "BOLD")
        body = VGroup(*[board_text(line, line_size, CHALK_WHITE, "BOLD")
                        for line in lines]).arrange(DOWN, buff=0.24)
        content = VGroup(head, body).arrange(DOWN, buff=buff)
        box = RoundedRectangle(corner_radius=0.10, width=width,
                               height=content.height + 2 * pad,
                               stroke_color=color, stroke_width=1.9,
                               fill_color=PANEL_FILL, fill_opacity=0.55)
        content.move_to(box.get_center())
        grp = VGroup(box, content)
        grp.box, grp.head, grp.body = box, head, body
        return grp

    # -- Scene 0: title ------------------------------------------------------
    # The purchase price is not the real cost: the refrigerator, the two
    # expense tags that dock under it, the total cost price they flow into and
    # the profit that remains -- with the tempting "Rs 2,000" struck through.
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Real Cost of a Purchase", 24,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A second-hand refrigerator.", 16,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            fridge = at(refrigerator(0.0, 0.0, 1.35, CHALK_CYAN), -3.70, 0.95)
            buy = at(chip("BOUGHT FOR Rs 5,000", CHALK_CYAN, size=14),
                     -0.60, 1.45)
            truck = at(truck_icon(0.0, 0.0, 1.15), -2.45, 0.70)
            move_tag = at(chip("TRANSPORT Rs 100", CHALK_YELLOW, size=14),
                          -0.60, 0.70)
            spanner = at(wrench_icon(0.0, 0.0, 1.15), -2.45, -0.05)
            fix_tag = at(chip("REPAIRS Rs 500", CHALK_YELLOW, size=14),
                         -0.60, -0.05)
            flow = arrow_between((-0.60, -0.36), (-0.60, -0.71), CHALK_GREEN)
            total = total_box("TOTAL COST PRICE = Rs 5,600", -0.60, -1.05,
                              CHALK_GREEN, width=3.60)
            sold = at(chip("SOLD FOR Rs 7,000", CHALK_PINK, size=14), 3.50, 1.45)
            real = at(board_text("REAL PROFIT", 15, CHALK_GREEN, "BOLD"),
                      3.50, 0.75)
            amount = at(chip("Rs 1,400", CHALK_GREEN, size=20), 3.50, 0.15)
            wrong = wrong_card("Rs 2,000", CHALK_RED, width=2.20, height=1.00,
                               size=16)
            wrong.move_to(np.array([3.50, -0.90, 0.0]))
            wrong_cross = wrong.cross
            wrong_cross.set_stroke(opacity=0)
            strip = at(board_text("Rs 5,000 + Rs 100 + Rs 500 = Rs 5,600 is "
                                  "the real cost.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(fridge, scale=0.92),
                      FadeIn(buy, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(truck, shift=RIGHT * 0.10),
                      FadeIn(move_tag, shift=RIGHT * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(spanner, shift=RIGHT * 0.10),
                      FadeIn(fix_tag, shift=RIGHT * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(GrowArrow(flow), FadeIn(total, scale=0.94), run_time=0.60)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(sold, shift=UP * 0.06), FadeIn(real, shift=UP * 0.06),
                      FadeIn(amount, scale=0.90), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(wrong, scale=0.92),
                      wrong_cross.animate.set_stroke(opacity=1),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: profit, loss, or neither -- and the two-pan balance ---------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("Profit, Loss, or Neither?", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Ask which one is bigger before subtracting.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            r1 = at(self.answer_row("1", "SP 650 > CP 500", "PROFIT Rs 150",
                                    CHALK_GREEN, width=5.20, height=0.56),
                    -1.85, 1.30)
            r2 = at(self.answer_row("2", "SP 450 < CP 500", "LOSS Rs 50",
                                    CHALK_RED, width=5.20, height=0.56),
                    -1.85, 0.60)
            r3 = at(self.answer_row("3", "SP 500 = CP 500", "NEITHER",
                                    CHALK_YELLOW, width=5.20, height=0.56),
                    -1.85, -0.10)
            f1 = chip("PROFIT = SP - CP", CHALK_GREEN, size=14)
            f2 = chip("LOSS = CP - SP", CHALK_PINK, size=14)
            formulas = VGroup(f1, f2).arrange(RIGHT, buff=0.45)
            at(formulas, -1.85, -0.95)

            stand, beam, moving = balance_rig(2.95, 0.55, 0.80)
            out_lbl = at(board_text("MONEY OUT", 11, CHALK_CYAN, "BOLD"),
                         1.96, 0.20)
            in_lbl = at(board_text("MONEY IN", 11, CHALK_PINK, "BOLD"),
                        3.94, 0.20)

            strip = at(board_text("Always compare before you subtract.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(r1, shift=UP * 0.06), FadeIn(stand, scale=0.94),
                      FadeIn(moving), FadeIn(out_lbl), FadeIn(in_lbl),
                      beam.animate.set_value(1.0), run_time=0.70)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(r2, shift=UP * 0.06), beam.animate.set_value(-1.0),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(r3, shift=UP * 0.06), beam.animate.set_value(0.0),
                      run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(f1, scale=0.92), FadeIn(f2, scale=0.92),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: the percentage is taken on the cost price -------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Percentage Is Taken on CP", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Measured against the cost price.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            example = at(chip("Rs 150 ON CP Rs 500 = 30%", CHALK_CYAN, size=13),
                         BOARD_CX, 0.95)
            base = at(chip("THE BASE IS ALWAYS CP", CHALK_YELLOW, size=13),
                      BOARD_CX, 0.15)
            pc = formula_card("PROFIT PERCENT",
                              r"\frac{\text{Profit}}{\text{CP}} \times 100",
                              CHALK_GREEN)
            at(pc, -2.70, 0.85)
            lc = formula_card("LOSS PERCENT",
                              r"\frac{\text{Loss}}{\text{CP}} \times 100",
                              CHALK_PINK)
            at(lc, 3.70, 0.85)
            wrong = wrong_card("PROFIT / SP × 100", CHALK_RED, width=2.90,
                               height=1.10, size=15)
            wrong.move_to(np.array([BOARD_CX, -0.75, 0.0]))
            wrong_cross = wrong.cross
            wrong_cross.set_stroke(opacity=0)
            strip = at(board_text("Never divide the difference by the selling "
                                  "price.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(example, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(pc, scale=0.94), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(lc, scale=0.94), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(base, scale=0.92), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(wrong, scale=0.92),
                      wrong_cross.animate.set_stroke(opacity=1),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: the refrigerator ledger -- an overhead profit ---------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Refrigerator Ledger", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Add every expense to the purchase price.", 16,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            frame = ledger_frame()
            fridge = at(refrigerator(0.0, 0.0, 0.58, CHALK_CYAN), -3.35, 1.36)
            out1 = ledger_line("Purchase price", "Rs 5,000", LED_ROW_Y[0],
                               CHALK_CYAN)
            out2 = ledger_line("Transport", "Rs 100", LED_ROW_Y[1], CHALK_YELLOW)
            out3 = ledger_line("Repairs", "Rs 500", LED_ROW_Y[2], CHALK_YELLOW)
            total = total_box("TOTAL COST PRICE = Rs 5,600")
            in1 = ledger_line("Selling price", "Rs 7,000", LED_ROW_Y[0],
                              CHALK_PINK, x_left=LED_IN_L, x_right=LED_IN_R)
            in2 = ledger_line("Profit", "Rs 1,400", LED_ROW_Y[1], CHALK_GREEN,
                              x_left=LED_IN_L, x_right=LED_IN_R)
            in3 = at(chalk_math(r"1400 \div 5600 \times 100 = 25\%", size=21,
                                color=CHALK_GREEN), LED_IN_CX, LED_ROW_Y[2])
            strip = at(board_text("The purchase price plus the overheads is the "
                                  "real cost.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(frame, scale=0.97), FadeIn(fridge, scale=0.92),
                      FadeIn(out1, shift=RIGHT * 0.06), run_time=0.65)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(out2, shift=RIGHT * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(out3, shift=RIGHT * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(total, scale=0.94), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(in1, shift=RIGHT * 0.06),
                      FadeIn(in2, shift=RIGHT * 0.06), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(in3, shift=UP * 0.06), FadeIn(strip, shift=UP * 0.06),
                      run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, total)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: the same ledger with a loss ---------------------------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("Overheads Can Bring a Loss", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A flat bought and then repaired.", 16,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            frame = ledger_frame()
            flat = at(flat_icon(0.0, 0.0, 0.72, CHALK_AMBER), -3.30, 1.35)
            out1 = ledger_line("Purchase price", "Rs 4,50,000", LED_ROW_Y[0],
                               CHALK_CYAN)
            out2 = ledger_line("Repairs, painting", "Rs 10,000", LED_ROW_Y[1],
                               CHALK_YELLOW)
            total = total_box("TOTAL COST PRICE = Rs 4,60,000")
            in1 = ledger_line("Selling price", "Rs 4,25,500", LED_ROW_Y[0],
                              CHALK_PINK, x_left=LED_IN_L, x_right=LED_IN_R)
            in2 = ledger_line("Loss", "Rs 34,500", LED_ROW_Y[1], CHALK_RED,
                              x_left=LED_IN_L, x_right=LED_IN_R)
            in3 = at(chalk_math(r"34500 \div 460000 \times 100 = 7.5\%",
                                size=21, color=CHALK_RED), LED_IN_CX,
                     LED_ROW_Y[2])
            strip = at(board_text("The overheads still belong to the cost.", 15,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(frame, scale=0.97), FadeIn(flat, scale=0.92),
                      FadeIn(out1, shift=RIGHT * 0.06), run_time=0.65)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(out2, shift=RIGHT * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(total, scale=0.94), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(in1, shift=RIGHT * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(in2, shift=RIGHT * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(in3, shift=UP * 0.06), FadeIn(strip, shift=UP * 0.06),
                      run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, total)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: the two-item trap -- +20% and -20% do NOT cancel ------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("Two Tables, Twenty Percent Each", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Do a gain and a loss cancel?", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            table1 = at(table_icon(0.0, 0.0, 0.95), -2.70, 1.15)
            table2 = at(table_icon(0.0, 0.0, 0.95), 3.88, 1.15)
            sp1 = at(chip("SOLD FOR Rs 3,000", CHALK_CYAN, size=13), -2.70, 0.55)
            sp2 = at(chip("SOLD FOR Rs 3,000", CHALK_CYAN, size=13), 3.88, 0.55)
            gain = at(chip("+20% GAIN", CHALK_GREEN, size=14), -2.70, -0.15)
            loss = at(chip("-20% LOSS", CHALK_PINK, size=14), 3.88, -0.15)
            zero = wrong_card("0%", CHALK_RED, width=1.40, height=1.00, size=20)
            zero.move_to(np.array([BOARD_CX, -0.15, 0.0]))
            zero_cross = zero.cross
            zero_cross.set_stroke(opacity=0)
            base1 = at(math_card(r"\text{CP} = \frac{3000}{1.2} = "
                                 r"\text{Rs}\,2500", CHALK_GREEN, width=3.10,
                                 height=1.00, size=20), -2.70, -1.00)
            base2 = at(math_card(r"\text{CP} = \frac{3000}{0.8} = "
                                 r"\text{Rs}\,3750", CHALK_PINK, width=3.10,
                                 height=1.00, size=20), 3.88, -1.00)
            strip = at(board_text("The two cost prices are different.", 15,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(table1, scale=0.92), FadeIn(table2, scale=0.92),
                      FadeIn(sp1, shift=UP * 0.06), FadeIn(sp2, shift=UP * 0.06),
                      run_time=0.65)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(gain, scale=0.92), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(loss, scale=0.92), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            # the tempting cancellation: the two labels head for the middle and
            # a "0%" card appears between them -- then it is stopped
            self.wait(leftover(tracker, "b3"))
            self.play(gain.animate.move_to(np.array([-1.25, -0.15, 0.0])),
                      loss.animate.move_to(np.array([2.25, -0.15, 0.0])),
                      FadeIn(zero, scale=0.92), run_time=0.65)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b4"))
            self.play(zero_cross.animate.set_stroke(opacity=1),
                      gain.animate.move_to(np.array([-2.70, -0.15, 0.0])),
                      loss.animate.move_to(np.array([3.88, -0.15, 0.0])),
                      run_time=0.70)
            self.play(FadeIn(base1, scale=0.94), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(base2, scale=0.94), FadeIn(strip, shift=UP * 0.06),
                      run_time=0.60)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: the whole transaction -- two ledgers merge into one ---------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Whole Transaction", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Add the two costs and the two selling prices.",
                                16, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            m1 = at(mini_ledger("TABLE 1", [("Cost price", "Rs 2,500"),
                                            ("Selling price", "Rs 3,000"),
                                            ("Gain", "Rs 500")], CHALK_GREEN),
                    -2.15, 0.88)
            m2 = at(mini_ledger("TABLE 2", [("Cost price", "Rs 3,750"),
                                            ("Selling price", "Rs 3,000"),
                                            ("Loss", "Rs 500")], CHALK_PINK),
                    3.15, 0.88)
            frame = ledger_frame(width=9.00, height=2.80, cy=0.10,
                                 rule_bot=-0.20)
            out1 = ledger_line("Total cost price", "Rs 6,250", 0.16, CHALK_GREEN)
            in1 = ledger_line("Total selling price", "Rs 6,000", 0.16,
                              CHALK_PINK, x_left=LED_IN_L, x_right=LED_IN_R)
            result = result_box("OVERALL: A LOSS OF Rs 250", BOARD_CX, -0.60,
                                CHALK_RED, width=5.40)
            pct = at(chalk_math(r"250 \div 6250 \times 100 = 4\%", size=21,
                                color=CHALK_RED), BOARD_CX, -1.10)
            strip = at(board_text("Plus twenty and minus twenty did not give "
                                  "zero.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            # the two item ledgers are physically drawn together and the one
            # total ledger takes their place
            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(m1, scale=0.93), FadeIn(m2, scale=0.93),
                      run_time=0.60)
            self.play(m1.animate.move_to(np.array([-1.85, 0.88, 0.0])),
                      m2.animate.move_to(np.array([2.85, 0.88, 0.0])),
                      run_time=0.55)
            self.play(FadeOut(m1), FadeOut(m2), FadeIn(frame, scale=0.97),
                      FadeIn(out1, shift=RIGHT * 0.06), run_time=0.65)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(in1, shift=RIGHT * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(result, scale=0.94), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(pct, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, result)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: the decision process ---------------------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Decision Process", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Five steps, every time.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            r1 = at(self.answer_row("1", "FIND THE PURCHASE PRICE",
                                    "what was paid for the item", CHALK_CYAN,
                                    height=0.50), BOARD_CX, 1.50)
            r2 = at(self.answer_row("2", "ADD THE OVERHEADS",
                                    "transport, repair, labour, storage",
                                    CHALK_YELLOW, height=0.50),
                    BOARD_CX, 0.88)
            r3 = at(self.answer_row("3", "FIND THE TOTAL SELLING PRICE",
                                    "what the buyer paid you", CHALK_GREEN,
                                    height=0.50), BOARD_CX, 0.26)
            r4 = at(self.answer_row("4", "COMPARE THE TWO",
                                    "SP bigger: profit, smaller: loss",
                                    CHALK_PINK, height=0.50), BOARD_CX, -0.36)
            r5 = at(self.answer_row("5", "DIVIDE BY THE COST PRICE",
                                    "then multiply by one hundred", CHALK_AMBER,
                                    height=0.50), BOARD_CX, -0.98)
            strip = at(board_text("For several items, compare the totals.", 15,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

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

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(r5, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: spoiled stock still costs ----------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("Spoiled Stock Still Costs", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Overheads count even for what is not sold.", 16,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            frame = ledger_frame()
            bananas = at(banana_bunch(0.0, 0.0, 0.62, CHALK_YELLOW), -3.35, 1.40)
            spoil = at(chip("SPOILED, NOT FREE", CHALK_RED, size=12), 3.35, 1.36)
            out1 = ledger_line("Bananas bought", "Rs 1,250", LED_ROW_Y[0],
                               CHALK_CYAN)
            out2 = ledger_line("Transport", "Rs 250", LED_ROW_Y[1], CHALK_YELLOW)
            total = total_box("TOTAL COST PRICE = Rs 1,500")
            in1 = ledger_line("Dozens sold", "Rs 1,575", LED_ROW_Y[0],
                              CHALK_PINK, x_left=LED_IN_L, x_right=LED_IN_R)
            in2 = ledger_line("Profit", "Rs 75", LED_ROW_Y[1], CHALK_GREEN,
                              x_left=LED_IN_L, x_right=LED_IN_R)
            in3 = at(chalk_math(r"75 \div 1500 \times 100 = 5\%", size=21,
                                color=CHALK_GREEN), LED_IN_CX, LED_ROW_Y[2])
            strip = at(board_text("Spoiled bananas are still part of the cost "
                                  "price.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(frame, scale=0.97), FadeIn(bananas, scale=0.92),
                      run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(out1, shift=RIGHT * 0.06),
                      FadeIn(out2, shift=RIGHT * 0.06),
                      FadeIn(total, scale=0.94), run_time=0.65)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(in1, shift=RIGHT * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(spoil, scale=0.92), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(in2, shift=RIGHT * 0.06),
                      FadeIn(in3, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, total)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 9: your turn (questions, the silent clock, then the answers) ---
    def beat_s9(self) -> None:
        with self.voiceover(text=NARRATION["s9q"]) as tracker:
            self.reset_board()

            heading = at(board_text("YOUR TURN", 26, CHALK_PINK, "BOLD"),
                         BOARD_CX, 2.78)
            sub = at(board_text("Two problems.", 16, CHALK_WHITE, "BOLD"),
                     BOARD_CX, 2.20)

            qa = at(self.q_card("A bicycle",
                                ["BOUGHT Rs 4,000",
                                 "TRANSPORT Rs 200, REPAIR Rs 300",
                                 "SOLD Rs 5,400"], CHALK_GREEN), -2.70, 0.90)
            qb = at(self.q_card("Find",
                                ["THE TOTAL COST PRICE",
                                 "THE PROFIT",
                                 "THE PROFIT PERCENT"], CHALK_YELLOW),
                    3.70, 0.90)
            qc = at(self.q_card("Two television sets",
                                ["EACH SOLD Rs 9,900",
                                 "ONE +10%, ONE -10%",
                                 "DID THEY CANCEL?"], CHALK_CYAN),
                    -2.70, -1.00)
            qd = at(self.q_card("Find",
                                ["BOTH COST PRICES",
                                 "TOTAL CP, TOTAL SP",
                                 "OVERALL PROFIT OR LOSS"], CHALK_PINK),
                    3.70, -1.00)

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
            a1 = at(self.answer_row("A", "TOTAL CP = Rs 4,500",
                                    "4,000 + 200 + 300", CHALK_GREEN),
                    BOARD_CX, 1.58)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "PROFIT = Rs 900",
                                    "5,400 - 4,500; that is 20%", CHALK_YELLOW),
                    BOARD_CX, 0.78)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "FIRST TV: CP = Rs 9,000",
                                    "9,900 / 1.1", CHALK_CYAN),
                    BOARD_CX, -0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "SECOND TV: CP = Rs 11,000",
                                    "total loss Rs 200 = 1%", CHALK_PINK),
                    BOARD_CX, -0.82)
            self.play(FadeIn(a4, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, a4)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap and the spoken thank-you ----------------------------
    def beat_s10(self) -> None:
        with self.voiceover(text=NARRATION["s10"]) as tracker:
            self.reset_board()

            heading = at(board_text("Purchase · Overheads · Percentage", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)

            r1 = at(self.answer_row("1", "ADD THE OVERHEADS",
                                    "purchase + transport + repair", CHALK_GREEN),
                    BOARD_CX, 1.48)
            r2 = at(self.answer_row("2", "COMPARE WITH THE SP",
                                    "bigger: profit, smaller: loss",
                                    CHALK_CYAN), BOARD_CX, 0.72)
            r3 = at(self.answer_row("3", "PERCENT ON THE COST PRICE",
                                    "divide by CP, not by SP", CHALK_YELLOW),
                    BOARD_CX, -0.04)
            r4 = at(self.answer_row("4", "MANY ITEMS",
                                    "compare total cost with total SP",
                                    CHALK_AMBER), BOARD_CX, -0.80)
            strip = at(board_text("The purchase price alone is never the real "
                                  "cost.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)
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
            # the strip is written on its own bookmark as the voice says "The
            # purchase price alone is never the real cost.", and only the
            # bookmark in front of "Thank you for watching," clears the board
            # and brings in the card.
            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeOut(heading), FadeOut(r1), FadeOut(r2), FadeOut(r3),
                      FadeOut(r4), FadeOut(strip), run_time=0.35)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.35)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.30)
            # 0.60 rather than 0.90: this piece's own audio runs the closing
            # sentence a little faster than the draft SRT assumes, and this
            # keeps every piece at 0.00 s stretch
            self.closing(tracker, thanks, run_time=0.60)
            self._capture_srt(tracker)

        self.wait(END_HOLD)

    # ================================================================ beats ==
    # Sales Tax, VAT & GST Calculations: Determining Original Prices and Total
    # Bills (Class 8 Maths, Chapter 5, Storymode 03).
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
    #   * ROW_A holds the diagram, ROW_B the numbers worked under it and ROW_C
    #     the rule chip above the banner, so nothing ever moves line by line;
    #   * every row of cards is centred on BOARD_CX (`hrow`, `row_centres`), and
    #     two texts never come closer than the 0.22 units the clearance audit
    #     asks for -- which is why a card's own lines are spaced by 0.26 or more
    #     and its head sits 0.30 above its body;
    #   * the BASE PRICE and the TAX-INCLUSIVE BILL are never the same object on
    #     screen: the bill bar is the base, and the translucent tax layer is
    #     visibly something ADDED to it;
    #   * a drawn cross always lives in the same VGroup as the card it strikes
    #     through (otherwise the clearance audit reads the strokes as a line
    #     running into somebody else's card);
    #   * the challenge uses the series' shared 10-second THINK clock, dead
    #     centre of the board, and the question cards sit in the four corners so
    #     the clock never covers one.

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

    def even_row(self, *mobs, y, gap=0.45, cx=BOARD_CX):
        """One row whose elements are spaced by their own ink, not by centre."""
        halves = [m.width / 2.0 for m in mobs]
        centres = row_centres(halves, gap, cx)
        for m, x in zip(mobs, centres):
            at(m, x, y)
        return VGroup(*mobs)

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

    def checked_row(self, text, color=CHALK_GREEN, size=12):
        """A chip that carries a drawn tick just OUTSIDE its box.

        The tick is kept clear of the chip's box (and so of its lettering) and
        is far too small to be read as a line running into a panel.
        """
        c = chip(text, color, size=size)
        k = tick((0.0, 0.0), color, 0.16)
        row = VGroup(k, c).arrange(RIGHT, buff=0.18)
        row.chip, row.tick = c, k
        return row

    # -- Scene 0: the tag is not the bill ------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = at(board_text("The Tag Is Not the Bill", 26, CHALK_PINK,
                                  "BOLD"), BOARD_CX, 2.06)
            sub = at(board_text("A pair of shoes, and a six percent tax.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, 1.44)

            shoes = at(shoe_pair(0.0, 0.0, 0.85, CHALK_PINK), -3.70, 0.82)
            tag = at(price_tag(2.00, 0.74, CHALK_PINK, "Rs 450", 14),
                     -1.85, 0.82)
            rate = at(chip("SALES TAX 6%", CHALK_AMBER, size=14), 0.85, 0.82)
            bill = at(receipt(1.60, 1.00, CHALK_CYAN, "BILL", "Rs 477", 12),
                      3.75, 0.82)

            q1 = name_card("BASE PRICE", "before tax", CHALK_GREEN)
            q2 = name_card("TAX AMOUNT", "the percentage added", CHALK_AMBER)
            q3 = name_card("FINAL BILL", "base plus tax", CHALK_YELLOW)
            row = self.even_row(q1, q2, q3, y=-0.45, gap=0.45)

            banner = at(board_text("BASE + TAX = THE FINAL BILL", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The price on the tag is not always the bill "
                                  "you pay.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(title, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(shoes, scale=0.9), FadeIn(tag, scale=0.9),
                      run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(rate, scale=0.9), FadeIn(bill, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(q1, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(q2, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(q3, shift=UP * 0.06),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: a tax is a percentage increase -----------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("A Tax Is a Percentage Increase", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The base price is the one hundred percent.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            bar = at(bill_bar(2.40, 0.54, CHALK_GREEN, "BASE PRICE = 100%", 13),
                     -2.80, ROW_A)
            layer = tax_layer(0.62, 0.54, CHALK_AMBER, "6%", 12)
            layer_start = np.array([-1.29, ROW_A + 0.72, 0.0])
            layer.move_to(layer_start)
            merged = at(bill_bar(3.02, 0.54, CHALK_YELLOW, "106% = THE BILL",
                                 13), -2.49, ROW_A)
            rate = at(chip("6% GIVES 106%", CHALK_AMBER, size=13), 0.85, ROW_A)
            # the bill grows as the layer joins the bar
            rec = at(receipt(1.70, 1.06, CHALK_CYAN, "BILL", "Rs 477", 12),
                     3.60, ROW_A)
            rec.scale(0.66)

            formula = at(chip("FINAL BILL = (100 + r) / 100 x BASE PRICE",
                              CHALK_YELLOW, size=13), BOARD_CX, ROW_B)
            idea = at(chip("SAME AS A PERCENTAGE INCREASE", CHALK_PINK,
                           size=13), BOARD_CX, ROW_C)
            banner = at(board_text("A TAX IS A PERCENTAGE INCREASE", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Adding r percent makes the bill one hundred "
                                  "plus r percent of the base.", 15,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(bar, scale=0.95), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(layer, scale=0.9), run_time=0.35)
            self.play(layer.animate.move_to(np.array([-1.29, ROW_A, 0.0])),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(ReplacementTransform(VGroup(bar, layer), merged),
                      FadeIn(rate, scale=0.9), run_time=0.50)
            self.play(FadeIn(rec, scale=0.80), run_time=0.30)
            self.play(rec.animate.scale(1.0 / 0.66), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(formula, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(idea, shift=UP * 0.06),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: sales tax on Rs 450 at 6% ----------------------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("Sales Tax on a Pair of Shoes", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Base Rs 450 and sales tax 6%.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            shoes = at(shoe_pair(0.0, 0.0, 0.85, CHALK_PINK), -3.72, ROW_A)
            tag = at(price_tag(2.00, 0.82, CHALK_PINK, "Rs 450", 14),
                     -1.85, ROW_A)
            tax = at(chip("TAX 6% OF 450 = Rs 27", CHALK_AMBER, size=13),
                     1.20, ROW_A)
            bill = at(chip("BILL = Rs 477", CHALK_YELLOW, size=13), 3.75, ROW_A)

            m1 = chip("6/100 x 450 = Rs 27", CHALK_AMBER, size=13)
            m2 = chip("450 + 27 = Rs 477", CHALK_GREEN, size=13)
            row = self.even_row(m1, m2, y=ROW_B, gap=0.50)

            short = at(chip("SHORTCUT: 106% OF 450 = 1.06 x 450 = Rs 477",
                            CHALK_YELLOW, size=13), BOARD_CX, ROW_C)
            banner = at(board_text("TAX Rs 27, FINAL BILL Rs 477", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The bill is the base price plus the tax.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(shoes, scale=0.9), FadeIn(tag, scale=0.9),
                      run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(tax, scale=0.9), run_time=0.40)
            self.play(FadeIn(m1, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(bill, scale=0.9), FadeIn(m2, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(short, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: reading a VAT-inclusive bill -------------------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Reading a VAT-Inclusive Bill", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("VAT is the same percentage idea.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            slip = at(med_receipt(1.95, 1.30, CHALK_CYAN, "MEDICAL",
                                  "Rs 372.18", 12), -3.40, 0.96)
            before = at(chip("PRE-VAT = Rs 354.45", CHALK_CYAN, size=13),
                        -0.75, 0.96)
            vat = at(chip("+ VAT 5% = Rs 17.72", CHALK_AMBER, size=13),
                     2.15, 0.96)

            b1 = chip("BASE + VAT = THE BILL", CHALK_YELLOW, size=13)
            b2 = chip("354.45 + 17.72 = Rs 372.18", CHALK_GREEN, size=13)
            row = self.even_row(b1, b2, y=ROW_B, gap=0.50)

            same = at(chip("VAT = THE SAME PERCENTAGE IDEA", CHALK_CYAN,
                           size=12), BOARD_CX, ROW_C)
            note = at(chip("HISTORICAL RATES, NOT TODAY'S TAX ADVICE",
                           CHALK_PINK, size=12), BOARD_CX, ROW_C)
            banner = at(board_text("BASE Rs 354.45 + VAT Rs 17.72 = Rs 372.18",
                                   16, CHALK_YELLOW, "BOLD"),
                        BOARD_CX, BANNER_Y)
            strip = at(board_text("Sales tax, VAT and GST share one arithmetic "
                                  "model.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(slip, scale=0.9), FadeIn(before, scale=0.9),
                      run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(vat, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(b1, shift=UP * 0.06), FadeIn(b2, shift=UP * 0.06),
                      FadeIn(banner, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(same, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeOut(same), FadeIn(note, scale=0.9),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: GST uses the same structure --------------------------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("GST Uses the Same Structure", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Base Rs 1,000 and GST at 5%.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            goods = at(goods_icon(0.0, 0.0, 1.0, CHALK_GREEN), -3.85, ROW_A)
            service = at(service_icon(0.0, 0.0, 1.0, CHALK_CYAN), -2.85, ROW_A)
            label = at(chip("GST: AN INDIRECT TAX ON GOODS AND SERVICES",
                            CHALK_CYAN, size=12), 1.30, ROW_A)

            rate = chip("BASE = Rs 1,000 · GST = 5%", CHALK_GREEN, size=13)
            rate.move_to(np.array([BOARD_CX, ROW_B, 0.0]))
            tax = at(chip("TAX = 5/100 x 1,000 = Rs 50", CHALK_AMBER, size=13),
                     BOARD_CX, ROW_B)
            add = at(chip("BILL = 1,000 + 50 = Rs 1,050", CHALK_GREEN,
                          size=13), BOARD_CX, ROW_C)
            short = at(chip("SHORTCUT: 105% OF 1,000 = Rs 1,050",
                            CHALK_YELLOW, size=13), BOARD_CX, ROW_B)

            banner = at(board_text("BASE + 5% GST = Rs 1,050", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("GST is indirect, but the arithmetic is "
                                  "unchanged.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(goods, scale=0.9), FadeIn(service, scale=0.9),
                      FadeIn(label, scale=0.9), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(rate, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeOut(rate), FadeIn(tax, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(add, scale=0.9), FadeIn(banner, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeOut(tax), FadeIn(short, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: working backward from a tax-inclusive bill -----------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("Finding the Price Before Tax", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The bill is 118%, not 100%.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            # the 118% bar: the base portion plus the marked 18% tax portion
            rb = rate_bar(2.60, REV_RATE, 0.58, CHALK_GREEN, CHALK_AMBER,
                          "118% = THE BILL", "18%", 13, 11)
            rb.move_to(np.array([-2.85, 0.94, 0.0]))
            base_lab = board_text("100% = BASE PRICE", 13, CHALK_WHITE, "BOLD")
            base_lab.move_to(rb.base.get_center())

            bill = chip("BILL INCL. 18% GST = Rs 2,360", CHALK_CYAN, size=13)
            bill.move_to(np.array([BOARD_CX, ROW_B, 0.0]))
            div = at(chip("2,360 x 100/118", CHALK_AMBER, size=13),
                     BOARD_CX, ROW_B)
            r1 = chip("BASE = Rs 2,000", CHALK_GREEN, size=13)
            r2 = chip("TAX = Rs 360", CHALK_AMBER, size=13)
            res = self.even_row(r1, r2, y=ROW_B, gap=0.50)

            formula = at(chip("BASE = BILL x 100 / (100 + r)", CHALK_YELLOW,
                              size=13), BOARD_CX, ROW_C)
            banner = at(board_text("BASE = Rs 2,000, TAX = Rs 360", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            warn = at(board_text("NEVER SUBTRACT THE RATE OFF THE BILL", 16,
                                 CHALK_RED, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Work backward with 100 divided by 100 plus "
                                  "r.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(bill, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(rb, scale=0.95), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeOut(bill), FadeIn(div, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            # the tax portion leaves and the bar is the 100% base again -- only
            # NOW does the reverse formula go on the board
            self.wait(leftover(tracker, "b3"))
            self.play(FadeOut(rb.tax), FadeOut(rb.tax_label),
                      FadeOut(rb.label), FadeIn(base_lab, scale=0.9),
                      FadeOut(div), run_time=0.55)
            self.play(FadeIn(res, shift=UP * 0.06), run_time=0.45)
            self.play(FadeIn(formula, scale=0.9),
                      FadeIn(banner, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeOut(banner), FadeIn(warn, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: the textbook's CGST / SGST split ---------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("CGST and SGST in the Textbook", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A worked example, not a universal rule.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            whole = at(whole_tax_block(3.60, 0.66, CHALK_AMBER,
                                       "GST = Rs 360", 13), -1.60, ROW_A)
            # the two bare halves: the CGST and SGST wording arrives one
            # bookmark at a time, so the split itself is what b2 shows
            split = tax_split(3.60, 0.66, CHALK_AMBER, None, None, 12)
            split.move_to(np.array([-1.60, ROW_A, 0.0]))
            cgst = board_text("CGST Rs 180", 12, CHALK_WHITE, "BOLD")
            cgst.move_to(split.half_l.get_center())
            sgst = board_text("SGST Rs 180", 12, CHALK_WHITE, "BOLD")
            sgst.move_to(split.half_r.get_center())
            tag = at(chip("THE TEXTBOOK HALVES IT", CHALK_CYAN, size=13),
                     3.05, ROW_A)

            h1 = chip("360 / 2 = Rs 180 EACH", CHALK_GREEN, size=13)
            h2 = chip("180 + 180 = Rs 360", CHALK_AMBER, size=13)
            row = self.even_row(h1, h2, y=ROW_B, gap=0.50)

            note = at(chip("THIS IS THE WORKED CASE, NOT EVERY BILL",
                           CHALK_PINK, size=12), BOARD_CX, ROW_C)
            banner = at(board_text("CGST Rs 180 + SGST Rs 180 = Rs 360", 17,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The equal split belongs to this worked "
                                  "example.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(whole, scale=0.95), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(tag, scale=0.9), FadeIn(h1, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            # the one tax block physically halves, and the CGST half is named
            self.wait(leftover(tracker, "b2"))
            self.play(ReplacementTransform(whole, split), run_time=0.55)
            self.play(FadeIn(cgst, scale=0.9), run_time=0.35)
            self.play(split.half_l.animate.shift(LEFT * 0.10),
                      split.half_r.animate.shift(RIGHT * 0.10),
                      cgst.animate.shift(LEFT * 0.10), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            # the SGST wording follows its own half, which has already shifted
            sgst.shift(RIGHT * 0.10)
            self.play(FadeIn(sgst, scale=0.9), FadeIn(h2, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(note, scale=0.9), FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: forward or backward -- the two-lane decision board ---------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Forward or Backward?", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("What you were given decides the lane.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            lane1 = lane_card("BASE PRICE GIVEN",
                              ["tax = r% of the base",
                               "bill = base + tax"], CHALK_GREEN,
                              width=4.20, head_size=14, line_size=12)
            lane2 = lane_card("TAX-INCLUSIVE BILL GIVEN",
                              ["base = bill x 100 / (100 + r)",
                               "the tax is bill - base"], CHALK_CYAN,
                              width=4.20, head_size=14, line_size=12)
            self.even_row(lane1, lane2, y=0.80, gap=0.45)

            ask = chip("THE LANE FOLLOWS WHAT YOU WERE GIVEN", CHALK_YELLOW,
                       size=13)
            ask.move_to(np.array([BOARD_CX, -0.48, 0.0]))
            adds = chip("TAX ADDS TO THE BASE", CHALK_GREEN, size=13)
            takes = chip("DISCOUNT TAKES OFF THE PRICE", CHALK_RED, size=13)
            keep = self.even_row(adds, takes, y=-0.48, gap=0.50)

            banner = at(board_text("TAX ADDS, DISCOUNT REMOVES", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Given the base go forward; given the bill go "
                                  "backward.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(lane1, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(lane2, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(ask, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeOut(ask), FadeIn(keep, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the classic error, and the correction ----------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Classic Tax Error", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Apply the rate to the base, never the bill.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            start = chip("BASE = Rs 1,000 · GST = 18%", CHALK_CYAN, size=13)
            start.move_to(np.array([BOARD_CX, ROW_B, 0.0]))
            tax = chip("18% OF Rs 1,000 = Rs 180", CHALK_GREEN, size=13)
            bill = chip("BILL = Rs 1,180", CHALK_YELLOW, size=13)
            known = self.even_row(tax, bill, y=ROW_B, gap=0.50)

            wrong1 = wrong_card("18% OF Rs 1,180", CHALK_RED, 2.70, 1.00, 13)
            wrong1.move_to(np.array([-2.45, 1.00, 0.0]))
            c1 = wrong1.cross
            c1.set_stroke(opacity=0)
            wrong2 = wrong_card("1180 - 18% = ?", CHALK_RED, 2.70, 1.00, 13)
            wrong2.move_to(np.array([1.75, 1.00, 0.0]))
            c2 = wrong2.cross
            c2.set_stroke(opacity=0)

            good1 = self.checked_row("18% OF Rs 1,000 = Rs 180", CHALK_GREEN)
            good2 = self.checked_row("Rs 1,180 x 100/118 = Rs 1,000",
                                     CHALK_CYAN)
            fix = self.even_row(good1, good2, y=ROW_C, gap=0.45)

            banner = at(board_text("NEVER APPLY THE RATE TO THE BILL", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The rate is charged on the base, never on "
                                  "the total.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(start, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeOut(start), FadeIn(known, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(wrong1, scale=0.9), run_time=0.40)
            self.play(c1.animate.set_stroke(opacity=1), run_time=0.40)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(wrong2, scale=0.9), run_time=0.40)
            self.play(c2.animate.set_stroke(opacity=1), run_time=0.40)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(fix, shift=UP * 0.06),
                      FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.60)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, banner)
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

            pic_a = board_text("Rs 800 + 5% tax = ?", 14, CHALK_GREEN, "BOLD")
            pic_b = board_text("Rs 1,180 incl. 18% = ?", 13, CHALK_CYAN,
                               "BOLD")
            pic_c = board_text("GST Rs 180, split equally?", 13, CHALK_AMBER,
                               "BOLD")
            pic_d = VGroup(board_text("18% of Rs 1,180:", 12, CHALK_PINK,
                                      "BOLD"),
                           board_text("right for Rs 1,000?", 12, CHALK_PINK,
                                      "BOLD")).arrange(DOWN, buff=0.24)

            qa = at(self.q_card("A: tax and bill", pic_a, CHALK_GREEN),
                    -2.80, 0.92)
            qb = at(self.q_card("B: base and tax", pic_b, CHALK_CYAN),
                    3.70, 0.92)
            qc = at(self.q_card("C: CGST and SGST", pic_c, CHALK_AMBER),
                    -2.80, -1.02)
            qd = at(self.q_card("D: spot the error", pic_d, CHALK_PINK),
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
            a1 = at(self.answer_row("A", "tax Rs 40, bill Rs 840",
                                    "5% of Rs 800 = Rs 40", CHALK_GREEN),
                    BOARD_CX, 1.62)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "base Rs 1,000, tax Rs 180",
                                    "1,180 x 100/118 = Rs 1,000", CHALK_CYAN),
                    BOARD_CX, 0.82)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "CGST Rs 90, SGST Rs 90",
                                    "180 split equally: 90 + 90", CHALK_AMBER),
                    BOARD_CX, 0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "No: 18% of Rs 1,180 is wrong",
                                    "the rate belongs on Rs 1,000",
                                    CHALK_PINK), BOARD_CX, -0.78)
            self.play(FadeIn(a4, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, a4)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap and the spoken thank-you ----------------------------
    def beat_s10(self) -> None:
        with self.voiceover(text=NARRATION["s10"]) as tracker:
            self.reset_board()

            heading = at(board_text("Base, Tax Rate, Bill", 22, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Four formulas to carry away.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            r1 = at(self.answer_row("1", "TAX",
                                    "tax = r / 100 x base price", CHALK_GREEN),
                    BOARD_CX, 1.48)
            r2 = at(self.answer_row("2", "BILL",
                                    "bill = base + tax = (100 + r)/100 x base",
                                    CHALK_CYAN), BOARD_CX, 0.72)
            r3 = at(self.answer_row("3", "REVERSE",
                                    "base = bill x 100 / (100 + r)",
                                    CHALK_YELLOW), BOARD_CX, -0.04)
            r4 = at(self.answer_row("4", "TAX OR DISCOUNT",
                                    "tax adds to the base; discount removes",
                                    CHALK_AMBER), BOARD_CX, -0.80)
            strip = at(board_text("Start at 100%, add the tax, work backward "
                                  "with 100/(100 + r).", 15, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)
            thanks = at(board_text("Thank You for Watching!", 30, CHALK_WHITE,
                                   "BOLD"), BOARD_CX, 0.62)
            bye = at(board_text("See you in the next lesson :)", 22,
                                CHALK_YELLOW, "BOLD"), BOARD_CX, -0.32)

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

            # The list stays on the board through the whole closing sentence:
            # the strip is written on its own bookmark as the voice says "Start
            # at one hundred percent, add the tax, and work backward...", and
            # only the bookmark in front of "Thank you for watching," clears the
            # board and brings in the card.
            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeOut(heading), FadeOut(sub), FadeOut(r1), FadeOut(r2),
                      FadeOut(r3), FadeOut(r4), FadeOut(strip), run_time=0.55)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.50)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.closing(tracker, thanks, run_time=0.90)
            self._capture_srt(tracker)

        self.wait(END_HOLD)

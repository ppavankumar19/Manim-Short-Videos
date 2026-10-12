    # ================================================================ beats ==
    # Percentage Increases, Decreases & Quick Estimation Rules on Bills
    # (Class 8 Maths, Chapter 5, Storymode 02).
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
    #   * the percentage control panel (CONVERT / CHANGE / ESTIMATE) stays on
    #     PANEL_Y in every teaching scene, so the two rows under it (ROW_A and
    #     ROW_B) and the rule chip on ROW_C never move;
    #   * every row of cards is centred on BOARD_CX (`hrow`), and two texts never
    #     come closer than the 0.22 units the clearance audit asks for -- which
    #     is why the cards space their own lines by 0.22 or more;
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

    # -- Scene 0: title -- 225 of 300 against 200 of 250 ----------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = at(board_text("Who Did Better?", 26, CHALK_PINK, "BOLD"),
                       BOARD_CX, 1.98)
            sub = at(board_text("225 of 300, or 200 of 250?", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, 1.42)

            # the two hundred-cell squares: A lights 75 cells, B lights 80.
            # The percentage figures sit BELOW their square, never on it: a
            # grid cell is a Rectangle -- and so a Polygon -- to the audit, and
            # a letter sitting on a cell's own outline is a TEXT-ON-SIDE defect.
            ga = at(percent_grid(75, CHALK_GREEN), -1.85, 0.62)
            gb = at(percent_grid(80, CHALK_CYAN), 2.35, 0.62)
            p75 = at(board_text("75%", 22, CHALK_GREEN, "BOLD"), -1.85, -0.12)
            p80 = at(board_text("80%", 22, CHALK_CYAN, "BOLD"), 2.35, -0.12)
            cap_a = at(board_text("Group A: 225 out of 300", 14, CHALK_WHITE,
                                  "BOLD"), -1.85, -0.60)
            cap_b = at(board_text("Group B: 200 out of 250", 14, CHALK_WHITE,
                                  "BOLD"), 2.35, -0.60)
            ask = at(chalk_math("?", size=44, color=CHALK_YELLOW),
                     BOARD_CX, 0.62)

            banner = at(board_text("ONE SCALE: OUT OF 100", 18, CHALK_YELLOW,
                                   "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("A percentage puts different totals on one "
                                  "common scale.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(title, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(ga, scale=0.95), run_time=0.40)
            self.play(LaggedStart(*[c.animate.set_fill(CHALK_GREEN, 0.62)
                                    for c in ga.lit], lag_ratio=0.02),
                      run_time=0.70)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(gb, scale=0.95), run_time=0.40)
            self.play(LaggedStart(*[c.animate.set_fill(CHALK_CYAN, 0.62)
                                    for c in gb.lit], lag_ratio=0.02),
                      run_time=0.70)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(p75, scale=0.9), FadeIn(p80, scale=0.9),
                      run_time=0.45)
            self.play(FadeIn(cap_a, shift=UP * 0.06),
                      FadeIn(cap_b, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(ask, scale=0.9), FadeIn(banner, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: convert both to one scale -----------------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("One Scale for Every Total", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Part over whole, times one hundred.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)
            panel = mode_panel("CONVERT")

            ca = chip("225 : 300 = 3 : 4", CHALK_GREEN, size=14)
            cb = chip("200 : 250 = 4 : 5", CHALK_CYAN, size=14)
            ha, hb = ca.width / 2.0, cb.width / 2.0
            xa, xb = row_centres((ha, hb), 0.55)
            ca = at(ca, xa, ROW_A)
            cb = at(cb, xb, ROW_A)

            row_b = VGroup(
                chip("= 75 OUT OF 100 = 75%", CHALK_GREEN, size=14),
                chip("= 80 OUT OF 100 = 80%", CHALK_CYAN, size=14),
            )
            ha, hb = row_b[0].width / 2.0, row_b[1].width / 2.0
            xa, xb = row_centres((ha, hb), 0.50)
            r75 = at(row_b[0], xa, ROW_B)
            r80 = at(row_b[1], xb, ROW_B)

            rule = at(chip("PERCENTAGE = PART / WHOLE x 100", CHALK_YELLOW,
                           size=14), BOARD_CX, ROW_C)
            banner = at(board_text("GROUP B DID BETTER: 80% > 75%", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Always name the whole: 300 for A and 250 "
                                  "for B.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), FadeIn(panel, scale=0.95),
                      run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(ca, shift=UP * 0.06), FadeIn(cb, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(r75, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(r80, scale=0.9), FadeIn(banner, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(rule, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: a 35% increase -- the block ATTACHES ------------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("A 35% Increase Attaches a Block", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("The increase is measured from the original.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)
            panel = mode_panel("CHANGE")

            bar = at(pct_bar(2.20, 0.50, CHALK_GREEN, "100% ORIGINAL", 14),
                     -2.20, ROW_A)
            block = pct_block(0.77, 0.50, CHALK_AMBER, "35%", 13)
            block.move_to(np.array([3.90, ROW_A, 0.0]))
            merged = at(chip("= 135% OF ORIGINAL", CHALK_YELLOW, size=14),
                        1.75, ROW_A)
            rule = at(chip("NEW VALUE = 135% OF THE ORIGINAL", CHALK_CYAN,
                           size=14), BOARD_CX, ROW_B)
            note = at(chip("THE INCREASE IS MEASURED FROM THE ORIGINAL",
                           CHALK_AMBER, size=13), BOARD_CX, ROW_C)
            banner = at(board_text("A 35% INCREASE GIVES 135% OF THE ORIGINAL",
                                   16, CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The increase is measured from the original, "
                                  "not the new value.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), FadeIn(panel, scale=0.95),
                      run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(bar, scale=0.95), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(block, scale=0.9), run_time=0.30)
            self.play(block.animate.next_to(bar, RIGHT, buff=0.0),
                      run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(merged, shift=UP * 0.06), FadeIn(rule, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(note, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: applying the increase to Rs 98,700 --------------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Applying the 35% Increase", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Add the increase to the original figure.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)
            panel = mode_panel("CHANGE")

            bag = at(money_bag(0.0, 0.0, 0.86, CHALK_AMBER, "SALES"),
                     -3.30, ROW_A)
            note = at(money_note(1.70, 0.80, CHALK_GREEN, "Rs 34,545"),
                      -1.20, ROW_A)
            up = at(chip("UP 35% THIS MONTH", CHALK_AMBER, size=14), 2.30, ROW_A)

            before = chip("SALES = Rs 98,700 (100%)", CHALK_CYAN, size=14)
            after = chip("98,700 + 34,545 = Rs 1,33,245", CHALK_GREEN, size=14)
            hb, ha = before.width / 2.0, after.width / 2.0
            xb, xa = row_centres((hb, ha), 0.50)
            before = at(before, xb, ROW_B)
            after = at(after, xa, ROW_B)

            route = at(chip("INCREASE = 35% OF 98,700 = Rs 34,545", CHALK_AMBER,
                            size=14), BOARD_CX, ROW_C)
            short = chip("SHORTCUT: 135% OF 98,700 = Rs 1,33,245",
                         CHALK_YELLOW, size=14)
            short.move_to(route.get_center())

            banner = at(board_text("NEW SALES = Rs 1,33,245", 18, CHALK_YELLOW,
                                   "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("A 35% rise gives 135% of the original "
                                  "figure.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), FadeIn(panel, scale=0.95),
                      run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(bag, scale=0.9), FadeIn(before, shift=UP * 0.06),
                      run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(up, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(note, scale=0.9), FadeIn(route, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(after, shift=UP * 0.06),
                      FadeIn(banner, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(Transform(route, short), FadeIn(strip, shift=UP * 0.06),
                      run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: a 10% decrease -- the block DETACHES and leaves -------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("A 10% Decrease on a Price Tag", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A decrease is taken away from one hundred.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)
            panel = mode_panel("CHANGE")

            tag = at(price_tag(2.30, 0.86, CHALK_PINK, "Rs 550"), -3.10, ROW_A)
            tens = at(decade_row(10, 0.26, 0.03, CHALK_CYAN, 0.52), 1.50,
                      ROW_A)
            last = tens[9]
            tag10 = board_text("10%", 13, CHALK_RED, "BOLD")
            tag10.move_to(np.array([last.get_center()[0], ROW_A - 0.44, 0.0]))

            part = chip("10% OF 550 = Rs 55", CHALK_RED, size=14)
            rest = chip("550 - 55 = Rs 495", CHALK_GREEN, size=14)
            hp, hr = part.width / 2.0, rest.width / 2.0
            xp, xr = row_centres((hp, hr), 0.50)
            part = at(part, xp, ROW_B)
            rest = at(rest, xr, ROW_B)

            inc = chip("INCREASE p% -> 100% + p%", CHALK_GREEN, size=14)
            dec = chip("DECREASE p% -> 100% - p%", CHALK_RED, size=14)
            hi, hd = inc.width / 2.0, dec.width / 2.0
            xi, xd = row_centres((hi, hd), 0.50)
            inc = at(inc, xi, ROW_C)
            dec = at(dec, xd, ROW_C)

            banner = at(board_text("10% OFF -> YOU PAY 90%", 18, CHALK_YELLOW,
                                   "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("A decrease is taken away from one hundred "
                                  "percent.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), FadeIn(panel, scale=0.95),
                      run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(tag, scale=0.9), FadeIn(tens, shift=UP * 0.06),
                      run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(last.animate.set_fill(CHALK_RED, 0.55
                                            ).set_stroke(CHALK_RED),
                      FadeIn(tag10, scale=0.9), FadeIn(part, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(last.animate.shift(RIGHT * 1.10 + DOWN * 0.55
                                         ).set_fill(CHALK_RED, 0.10
                                                    ).set_stroke(opacity=0.25),
                      tag10.animate.shift(RIGHT * 1.10 + DOWN * 0.55
                                          ).set_opacity(0.15),
                      FadeIn(rest, scale=0.9), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(inc, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(dec, scale=0.9), FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.55)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: the mental toolkit, and the doubled-halving mistake ---------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Mental Percentage Toolkit", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Ten percent first, then half, then add.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)
            panel = mode_panel("ESTIMATE")

            whole = at(pct_block(1.20, 0.54, CHALK_AMBER, "10%", 14),
                       -2.00, ROW_A)
            halves = split_block(1.20, 0.54, CHALK_AMBER)
            halves.move_to(whole.get_center())

            rules = VGroup(
                chip("10% = ONE TENTH", CHALK_GREEN, size=12),
                chip("5% = HALF OF 10%", CHALK_CYAN, size=12),
                chip("15% = 10% + 5%", CHALK_AMBER, size=12),
                chip("20% = 2 x 10%", CHALK_PINK, size=12),
            )
            halves_w = [c.width / 2.0 for c in rules]
            centres = row_centres(halves_w, 0.28)
            for c, x in zip(rules, centres):
                at(c, x, ROW_B)

            wrong = wrong_card("5% = HALF OF 20%", CHALK_RED, width=2.30,
                               height=0.85, size=13)
            wrong.move_to(np.array([2.90, ROW_A, 0.0]))
            wrong_cross = wrong.cross
            wrong_cross.set_stroke(opacity=0)

            demo = at(chip("ON 480:  10% = 48,  5% = 24,  SO 15% = 72",
                           CHALK_YELLOW, size=14), BOARD_CX, ROW_C)
            banner = at(board_text("5% IS HALF OF 10%, NOT OF 20%", 16,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Build hard percentages out of ten percent.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), FadeIn(panel, scale=0.95),
                      run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(whole, scale=0.9), FadeIn(rules[0], scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(ReplacementTransform(whole, halves), run_time=0.45)
            self.play(halves.half_l.animate.shift(LEFT * 0.07),
                      halves.half_r.animate.shift(RIGHT * 0.07),
                      FadeIn(rules[1], scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(rules[2], scale=0.9), FadeIn(rules[3], scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(wrong, scale=0.9), run_time=0.40)
            self.play(wrong_cross.animate.set_stroke(opacity=1),
                      FadeIn(banner, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(demo, scale=0.9), FadeIn(strip, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: estimating 15% on the bill ---------------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("Estimating 15% on a Bill", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Round the bill, then build fifteen percent.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)
            panel = mode_panel("ESTIMATE")

            bill = at(receipt(1.70, 1.00, CHALK_CYAN, "BILL", "Rs 477.80"),
                      -3.35, ROW_A)
            ruler = number_ruler()
            start_x = nl_x(BILL)
            dot = Dot(radius=0.10, color=CHALK_PINK)
            dot.move_to(np.array([start_x, NL_Y, 0.0]))

            ten = chip("10% OF 480 = Rs 48", CHALK_GREEN, size=13)
            five = chip("5% = HALF OF THAT = Rs 24", CHALK_CYAN, size=13)
            fifteen = chip("15% = 48 + 24 = Rs 72", CHALK_AMBER, size=13)
            t1, t2, t3 = (ten, five, fifteen)
            w1, w2, w3 = t1.width / 2.0, t2.width / 2.0, t3.width / 2.0
            c1, c2, c3 = row_centres((w1, w2, w3), 0.30)
            ten = at(t1, c1, ROW_B)
            five = at(t2, c2, ROW_B)
            fifteen = at(t3, c3, ROW_B)

            step = chip("APPROX Rs 480 - Rs 72 = Rs 408", CHALK_YELLOW, size=14)
            approx = chalk_math(r"\approx", size=30, color=CHALK_YELLOW)
            paid = chip("ABOUT Rs 410", CHALK_GREEN, size=14)
            hs, hp = step.width / 2.0, paid.width / 2.0
            xs, xp = row_centres((hs, hp), 0.90)
            step = at(step, xs, ROW_C)
            approx.move_to(np.array([(xs + hs + xp - hp) / 2.0, ROW_C, 0.0]))
            paid = at(paid, xp, ROW_C)

            banner = at(board_text("ROUND THE BILL, THEN PAY ABOUT Rs 410", 16,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("Round the bill, then build fifteen percent "
                                  "from ten percent.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), FadeIn(panel, scale=0.95),
                      run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(bill, scale=0.9), FadeIn(ruler, shift=UP * 0.06),
                      run_time=0.45)
            self.play(FadeIn(dot, scale=0.9), run_time=0.25)
            self.play(dot.animate.move_to(np.array([nl_x(ROUNDED_BILL), NL_Y,
                                                    0.0])), run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(ten, scale=0.9), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(five, scale=0.9), FadeIn(fifteen, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(step, scale=0.9), FadeIn(approx, scale=0.9),
                      run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(paid, scale=0.9), FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: the exact lane beside the estimate lane --------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Exact Lane and Estimate Lane", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("An estimate is a check, not exact arithmetic.",
                                17, CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)
            panel = mode_panel("ESTIMATE")

            exact = note_card("EXACT LANE", ["15% of 477.80 = 71.67"],
                              CHALK_CYAN, width=4.30, height=1.00,
                              head_size=14, line_size=13)
            mental = note_card("MENTAL LANE", ["15% of 480 = 72"],
                               CHALK_GREEN, width=4.30, height=1.00,
                               head_size=14, line_size=13)
            he, hm = exact.width / 2.0, mental.width / 2.0
            xe, xm = row_centres((he, hm), 0.45)
            exact = at(exact, xe, ROW_A)
            mental = at(mental, xm, ROW_A)

            l1 = chip("477.80 - 71.67 = 406.13", CHALK_CYAN, size=14)
            l2 = chip("480 - 72 = 408, ABOUT 410", CHALK_GREEN, size=14)
            h1, h2 = l1.width / 2.0, l2.width / 2.0
            x1, x2 = row_centres((h1, h2), 0.50)
            l1 = at(l1, x1, ROW_B)
            l2 = at(l2, x2, ROW_B)

            check = chip("AN ESTIMATE IS A REASONABLENESS CHECK, NOT EXACT "
                         "ARITHMETIC", CHALK_YELLOW, size=13)
            mark = tick((0.0, 0.0), CHALK_GREEN, 0.18)
            hk, hc = mark.width / 2.0, check.width / 2.0
            xk, xc = row_centres((hk, hc), 0.35)
            mark.move_to(np.array([xk, ROW_C, 0.0]))
            check = at(check, xc, ROW_C)

            banner = at(board_text("EXACT 406.13, ESTIMATE ABOUT 410", 16,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("An estimate is a reasonableness check, not "
                                  "exact arithmetic.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), FadeIn(panel, scale=0.95),
                      run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(exact, scale=0.95), FadeIn(l1, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(mental, scale=0.95), FadeIn(l2, shift=UP * 0.06),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(mark), FadeIn(check, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the four-move decision map ---------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Four-Move Decision Map", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Convert, change, estimate, check.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)
            panel = mode_panel("ALL")

            c1 = note_card("CONVERT", ["part / whole x 100"], CHALK_GREEN,
                           width=2.20, height=1.05, head_size=14,
                           line_size=12)
            c2 = note_card("INCREASE", ["100% + p%"], CHALK_AMBER,
                           width=2.20, height=1.05, head_size=14,
                           line_size=12)
            c3 = note_card("DECREASE", ["100% - p%"], CHALK_CYAN,
                           width=2.20, height=1.05, head_size=14,
                           line_size=12)
            c4 = note_card("ESTIMATE", ["round, then use 10%"], CHALK_PINK,
                           width=2.20, height=1.05, head_size=14,
                           line_size=12)
            hw = [c.width / 2.0 for c in (c1, c2, c3, c4)]
            xs = row_centres(hw, 0.28)
            c1, c2, c3, c4 = (at(c, x, 0.72) for c, x in zip((c1, c2, c3, c4),
                                                             xs))

            flow = at(chip("CONVERT -> CHANGE -> ESTIMATE -> CHECK",
                           CHALK_YELLOW, size=15), BOARD_CX, ROW_C)
            banner = at(board_text("FOUR MOVES: CONVERT, INCREASE, DECREASE, "
                                   "ESTIMATE", 16, CHALK_YELLOW, "BOLD"),
                        BOARD_CX, BANNER_Y)
            strip = at(board_text("Round first, then build the percentage from "
                                  "ten percent.", 15, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), FadeIn(panel, scale=0.95),
                      run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(c1, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(c2, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(c3, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(c4, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(flow, scale=0.9), FadeIn(banner, shift=UP * 0.06),
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

            pic_a = chalk_math(r"\frac{18}{24} \to \; ?\%", size=18,
                               color=CHALK_GREEN)
            pic_b = board_text("800 - 10% = ?", 14, CHALK_CYAN, "BOLD")
            pic_c = board_text("round 360, 20% = ?", 14, CHALK_AMBER, "BOLD")
            pic_d = board_text("900 + 35% = ?", 14, CHALK_PINK, "BOLD")

            qa = at(self.q_card("convert 18 out of 24", pic_a, CHALK_GREEN),
                    -2.80, 0.92)
            qb = at(self.q_card("Rs 800 with 10% off", pic_b, CHALK_CYAN),
                    3.70, 0.92)
            qc = at(self.q_card("estimate 20% of 357.30", pic_c, CHALK_AMBER),
                    -2.80, -1.02)
            qd = at(self.q_card("increase Rs 900 by 35%", pic_d, CHALK_PINK),
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
            a1 = at(self.answer_row("A", "18 of 24 = 75%",
                                    "18 / 24 = 3 / 4 = 75%", CHALK_GREEN),
                    BOARD_CX, 1.62)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "Rs 800 - 10% = Rs 720",
                                    "10% of 800 = Rs 80", CHALK_CYAN),
                    BOARD_CX, 0.82)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "about 20% of 360 = Rs 72",
                                    "10% = 36, so 20% = 72", CHALK_AMBER),
                    BOARD_CX, 0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "Rs 900 + 35% = Rs 1,215",
                                    "135% of 900 = Rs 1,215", CHALK_PINK),
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

            heading = at(board_text("Compare, Change, Estimate, Check", 18,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Four rules to carry away.", 17, CHALK_WHITE,
                                "BOLD"), BOARD_CX, SUB_Y)

            r1 = at(self.answer_row("1", "COMPARE",
                                    "always out of one hundred", CHALK_GREEN),
                    BOARD_CX, 1.48)
            r2 = at(self.answer_row("2", "CHANGE",
                                    "increase adds, decrease subtracts",
                                    CHALK_CYAN), BOARD_CX, 0.72)
            r3 = at(self.answer_row("3", "ESTIMATE",
                                    "round, then build from 10%", CHALK_YELLOW),
                    BOARD_CX, -0.04)
            r4 = at(self.answer_row("4", "CHECK",
                                    "an estimate is a reasonableness check",
                                    CHALK_AMBER), BOARD_CX, -0.80)
            strip = at(board_text("Compare, change, estimate, then check.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)
            thanks = at(board_text("Thank You for Watching!", 30, CHALK_WHITE,
                                   "BOLD"), BOARD_CX, 0.62)
            bye = at(board_text("See you in the next lesson :)", 22, CHALK_YELLOW,
                                "BOLD"), BOARD_CX, -0.32)

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

            # The four rules stay on the board through the whole closing
            # sentence: the strip is written on its own bookmark as the voice
            # says "Compare, change, estimate, check.", and only the bookmark in
            # front of "Thank you for watching," clears the board and brings in
            # the card.
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

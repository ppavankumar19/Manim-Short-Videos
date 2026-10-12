    # ================================================================ beats ==
    # Basic Divisibility Rules for 2, 3, 5, 6, 9 and 10.
    #
    # SYNC RULE for every reveal: wait for the narration bookmark that ends the
    # phrase describing a thing, and only then bring it on.  Playing first and
    # waiting afterwards shows the picture a whole window early (the board was
    # giving away "remainder zero" while the voice was still saying "twenty four
    # divided by four"), which reads as broken sync.
    #
    # Layout rules, so the audits stay clean:
    #   * the heading sits on ROW_Y, the closing strip on STRIP_Y (-1.95);
    #     nothing at all sits below CAPTION_SAFE_Y (-2.15);
    #   * two-column work is centred on LEFT_X and RIGHT_X;
    #   * nothing is placed on a line, and no card, chip or dot is placed over
    #     another element -- checked by audit_clearance.py and
    #     audit_sync_overlap.py.
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
    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Divisibility Rules", 33, CHALK_WHITE,
                               "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 1.62, 0]))
            sub = board_text("Quick Tests for 2, 3, 5, 6, 9 and 10", 20,
                             CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 0.86, 0]))
            chips = VGroup(*[badge_card(d, CHALK_CYAN, size=26)
                             for d in ("2", "3", "5", "6", "9", "10")]
                           ).arrange(RIGHT, buff=0.28).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.16, 0]))
            promise = board_text("Check divisibility without doing the "
                                 "division.", 17, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -1.32, 0]))
            tag = board_text("Look  ·  Add  ·  Combine", 19, CHALK_GREEN,
                             "BOLD").move_to(np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(title, shift=UP * 0.10), run_time=0.5)
            self.play(FadeIn(sub, shift=UP * 0.10), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in chips],
                                  lag_ratio=0.15), run_time=1.0)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(promise, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(tag, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, tag)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: the hook -- sharing, and why the idea is old --------------
    def beat1_chocolate(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("Hasini's Birthday", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            lot = measure_card(r"125\text{ chocolates}", CHALK_YELLOW, 22
                               ).move_to(np.array([BOARD_CX, 2.24, 0]))
            hook = board_text("Traders shared grain this way for centuries.",
                              16, CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX, 1.78, 0]))

            attempts = VGroup()
            for divisor, verdict_text, ok in (
                    ("5", "25 groups,  nothing left", True),
                    ("6", "20 groups,  5 left over", False)):
                attempts.add(VGroup(
                    badge_card(divisor, CHALK_CYAN, size=20, width=0.58,
                               height=0.44),
                    board_text(verdict_text, 15,
                               CHALK_GREEN if ok else CHALK_PINK, "BOLD"),
                    mark_yes(0.9) if ok else mark_no(0.9),
                ).arrange(RIGHT, buff=0.30))
            attempts.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX + 0.05, 0.80, 0]))

            ask = board_text("Can we tell without dividing?", 20, CHALK_GREEN,
                             "BOLD").move_to(np.array([BOARD_CX, -1.16, 0]))
            ask_box = SurroundingRectangle(ask, color=CHALK_GREEN, buff=0.20,
                                           corner_radius=0.10, stroke_width=2.4)
            strip = board_text("Every guess costs another division.", 16,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(lot, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(hook, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(attempts[0], shift=RIGHT * 0.12), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(attempts[1], shift=RIGHT * 0.12), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(ask, shift=UP * 0.08), Create(ask_box),
                      run_time=0.55)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b5"))
            self.closing(tracker, ask_box, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: what does "divisible" mean? --------------------------------
    def beat2_divisible(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("What Does \u201cDivisible\u201d Mean?", 23,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, ROW_Y, 0]))
            l_head = number_card(24, CHALK_WHITE, size=24).move_to(
                np.array([LEFT_X, 2.02, 0]))
            r_head = number_card(29, CHALK_WHITE, size=24).move_to(
                np.array([RIGHT_X, 2.02, 0]))

            # The two share-box grids are TOP-aligned, so the three-row grid of
            # 29 sets the height and the verdict rows below are clear of both.
            l_grid = chocolate_groups(6, per_group=4, cols=3).scale(0.80)
            r_grid = chocolate_groups(7, per_group=4, cols=3).scale(0.80)
            l_grid.shift(UP * (1.42 - l_grid.get_top()[1]))
            r_grid.shift(UP * (1.42 - r_grid.get_top()[1]))
            l_grid.move_to(np.array([LEFT_X, l_grid.get_center()[1], 0]))
            r_grid.move_to(np.array([RIGHT_X, r_grid.get_center()[1], 0]))
            # the one left-over chocolate sits beside the seventh share-box,
            # not under it where the verdict row runs
            lone = Dot(radius=0.06, color=CHALK_YELLOW).next_to(
                r_grid[-1], RIGHT, buff=0.18)

            l_rem = verdict(True, "Remainder 0", size=15).move_to(
                np.array([LEFT_X, -0.22, 0]))
            r_rem = verdict(False, "Remainder 1", size=15).move_to(
                np.array([RIGHT_X, -0.22, 0]))
            l_tag = board_text("DIVISIBLE", 18, CHALK_GREEN, "BOLD").move_to(
                np.array([LEFT_X, -0.78, 0]))
            r_tag = board_text("NOT DIVISIBLE", 18, CHALK_PINK, "BOLD"
                               ).move_to(np.array([RIGHT_X, -0.78, 0]))

            rule = board_text("Remainder 0  \u2192  exactly divisible", 19,
                              CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -1.40, 0]))
            rule_box = SurroundingRectangle(rule, color=CHALK_GREEN, buff=0.20,
                                            corner_radius=0.10, stroke_width=2.4)
            strip = board_text("Now let us inspect the digits.", 16,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(l_head), FadeIn(r_head), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(b) for b in l_grid], lag_ratio=0.16),
                      run_time=1.1)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(l_rem), FadeIn(l_tag), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(LaggedStart(*[FadeIn(b) for b in r_grid], lag_ratio=0.14),
                      run_time=1.2)
            self.play(FadeIn(lone, scale=0.6), run_time=0.3)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(r_rem), FadeIn(r_tag), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(rule, shift=UP * 0.08), Create(rule_box),
                      run_time=0.5)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.45)
            self.closing(tracker, rule_box, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: divisibility by 2 ------------------------------------------
    def beat3_rule2(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()

            heading = board_text("Divisibility by 2", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            tiles = VGroup()
            rings = VGroup()
            verdicts = VGroup()
            for value in ("953", "9534"):
                grp, parts = digit_tiles(value, size=29)
                tiles.add(grp)
                rings.add(tile_ring(parts[-1]))
                ok = value[-1] in "02468"
                verdicts.add(VGroup(
                    mark_yes(1.0) if ok else mark_no(1.0),
                    board_text("yes" if ok else "no", 16,
                               CHALK_GREEN if ok else CHALK_PINK, "BOLD"),
                ).arrange(RIGHT, buff=0.16))
            tiles.arrange(RIGHT, buff=1.00).move_to(
                np.array([BOARD_CX, 1.94, 0]))
            for ring, tile_row in zip(rings, tiles):
                ring.move_to(tile_row[-1].get_center())
            verdicts.arrange(RIGHT, buff=1.62).move_to(
                np.array([BOARD_CX - 0.02, 1.16, 0]))
            # the "yes" verdict belongs to the second number, the "no" to the
            # first, so they are revealed separately, under their own number
            yes_mark = verdicts[1].move_to(np.array([tiles[1].get_center()[0],
                                                     1.16, 0]))
            no_mark = verdicts[0].move_to(np.array([tiles[0].get_center()[0],
                                                    1.16, 0]))

            even_head = board_text("Even ending digits", 17, CHALK_CYAN, "BOLD"
                                   ).move_to(np.array([BOARD_CX, 0.36, 0]))
            even_tiles = VGroup(*[badge_card(d, CHALK_GREEN, size=22, width=0.54,
                                             height=0.52)
                                  for d in ("0", "2", "4", "6", "8")]
                                ).arrange(RIGHT, buff=0.22).move_to(
                np.array([BOARD_CX, -0.26, 0]))

            rule = board_text("Divisible by 2  \u2192  the ones digit is "
                              "0, 2, 4, 6 or 8", 19, CHALK_YELLOW, "BOLD"
                              ).move_to(np.array([BOARD_CX, -1.28, 0]))
            rule_box = SurroundingRectangle(rule, color=CHALK_YELLOW, buff=0.20,
                                            corner_radius=0.10, stroke_width=2.4)
            strip = board_text("For 2, ignore every digit except the last one.",
                               16, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(tiles[0]), run_time=0.35)
            self.play(Create(rings[0]), run_time=0.3)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(tiles[1]), run_time=0.35)
            self.play(Create(rings[1]), run_time=0.3)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(Indicate(rings, color=CHALK_YELLOW, scale_factor=1.06),
                      run_time=0.6)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(even_head, shift=UP * 0.08), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.10)
                                    for t in even_tiles], lag_ratio=0.16),
                      run_time=0.8)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(yes_mark, shift=DOWN * 0.08), run_time=0.4)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(no_mark, shift=DOWN * 0.08), run_time=0.4)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(rule, shift=UP * 0.08), Create(rule_box),
                      run_time=0.55)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, rule_box)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: divisibility by 5 and 10 -----------------------------------
    def beat4_rule5_10(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()

            heading = board_text("Divisibility by 5 and 10", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))

            l_tiles, l_parts = digit_tiles("5785", size=24)
            l_tiles.move_to(np.array([LEFT_X, 2.00, 0]))
            l_ring = tile_ring(l_parts[-1], CHALK_YELLOW)
            r_tiles, r_parts = digit_tiles("1250", size=24)
            r_tiles.move_to(np.array([RIGHT_X, 2.00, 0]))
            r_ring = tile_ring(r_parts[-1], CHALK_YELLOW)

            l_checks = VGroup(verdict(True, "ones digit 5  \u2192  \u00f75",
                                      size=15)).move_to(
                np.array([LEFT_X, 1.22, 0]))
            r_checks = VGroup(
                verdict(True, "ones digit 0  \u2192  \u00f75", size=15),
                verdict(True, "ones digit 0  \u2192  \u00f710", size=15),
            ).arrange(DOWN, buff=0.18).move_to(np.array([RIGHT_X, 1.13, 0]))

            rules = VGroup(
                rule_line("2", "0, 2, 4, 6, 8", CHALK_CYAN, width=2.9),
                rule_line("5", "0 or 5", CHALK_GREEN, width=2.9),
                rule_line("10", "0", CHALK_PINK, width=2.9),
            ).arrange(RIGHT, buff=0.32).move_to(
                np.array([BOARD_CX, -0.34, 0]))
            title = board_text("LAST-DIGIT RULES", 20, CHALK_YELLOW, "BOLD"
                               ).move_to(np.array([BOARD_CX, -1.32, 0]))
            title_box = SurroundingRectangle(title, color=CHALK_YELLOW,
                                             buff=0.18, corner_radius=0.10,
                                             stroke_width=2.4)
            strip = board_text("Three rules, one glance.", 16, CHALK_WHITE,
                               "BOLD").move_to(np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(l_tiles), run_time=0.35)
            self.play(Create(l_ring), run_time=0.3)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(l_checks), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(r_tiles), run_time=0.35)
            self.play(Create(r_ring), run_time=0.3)

            self.wait(leftover(tracker, "b3"))
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.10)
                                    for c in r_checks], lag_ratio=0.3),
                      run_time=0.7)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.08)
                                    for r in rules], lag_ratio=0.22),
                      run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(title, shift=UP * 0.08), Create(title_box),
                      run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, title_box)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: divisibility by 3 ------------------------------------------
    def beat5_rule3(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            self.reset_board()

            heading = board_text("Divisibility by 3", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))

            l_grp, l_parts = digit_tiles("27", size=24)
            r_grp, r_parts = digit_tiles("37", size=24)
            l_grp.move_to(np.array([LEFT_X, 2.02, 0]))
            r_grp.move_to(np.array([RIGHT_X, 2.02, 0]))
            l_ring = tile_ring(l_parts[-1])
            r_ring = tile_ring(r_parts[-1])
            same = board_text("Same last digit \u2014 different answer.", 17,
                              CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, 1.38, 0]))
            l_mark = verdict(True, "27 \u00f7 3", size=15).move_to(
                np.array([LEFT_X, 0.94, 0]))
            r_mark = verdict(False, "37 \u00f7 3", size=15).move_to(
                np.array([RIGHT_X, 0.94, 0]))

            big, big_parts = digit_tiles("36129", size=27)
            big.move_to(np.array([BOARD_CX, 0.16, 0]))
            expr = chalk_math(r"3+6+1+2+9 = 21", size=30, color=CHALK_YELLOW
                              ).move_to(np.array([BOARD_CX, -0.60, 0]))
            result = board_text("21 \u00f7 3 is exact  \u2192  36129 is "
                                "divisible by 3", 18, CHALK_GREEN, "BOLD"
                                ).move_to(np.array([BOARD_CX, -1.30, 0]))
            result_box = SurroundingRectangle(result, color=CHALK_GREEN,
                                              buff=0.18, corner_radius=0.10,
                                              stroke_width=2.4)
            strip = board_text("Digit sum divisible by 3  \u2192  number "
                               "divisible by 3.", 16, CHALK_WHITE, "BOLD"
                               ).move_to(np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(l_grp), FadeIn(r_grp), run_time=0.45)
            self.play(Create(l_ring), Create(r_ring), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(same, shift=UP * 0.08), run_time=0.4)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(l_mark), FadeIn(r_mark), run_time=0.45)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(big), run_time=0.5)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(expr, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(result, shift=UP * 0.08), Create(result_box),
                      run_time=0.55)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, result_box, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: divisibility by 9 ------------------------------------------
    def beat6_rule9(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("Divisibility by 9", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            num, parts = digit_tiles("9846", size=27)
            num.move_to(np.array([BOARD_CX, 2.00, 0]))
            expr = chalk_math(r"9+8+4+6 = 27", size=30, color=CHALK_YELLOW
                              ).move_to(np.array([BOARD_CX, 1.22, 0]))
            times = chalk_math(r"27 = 9 \times 3", size=28, color=CHALK_CYAN
                               ).move_to(np.array([BOARD_CX, 0.56, 0]))
            result = board_text("9846 is divisible by 9", 19, CHALK_GREEN,
                                "BOLD").move_to(
                np.array([BOARD_CX, -0.18, 0]))
            result_box = SurroundingRectangle(result, color=CHALK_GREEN,
                                              buff=0.18, corner_radius=0.10,
                                              stroke_width=2.4)
            rules = VGroup(
                rule_line("\u00f73", "sum divisible by 3", CHALK_CYAN,
                          width=3.6),
                rule_line("\u00f79", "sum divisible by 9", CHALK_GREEN,
                          width=3.6),
            ).arrange(RIGHT, buff=0.36).move_to(
                np.array([BOARD_CX, -1.16, 0]))
            strip = board_text("3 and 9  \u2192  ADD THE DIGITS", 18,
                               CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(num), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(expr, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(times, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(result, shift=UP * 0.08), Create(result_box),
                      run_time=0.55)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.08)
                                    for r in rules], lag_ratio=0.25),
                      run_time=0.8)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.45)
            self.closing(tracker, result_box, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: divisibility by 6 ------------------------------------------
    def beat7_rule6(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("Divisibility by 6", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            num, parts = digit_tiles("7224", size=27)
            num.move_to(np.array([BOARD_CX, 2.04, 0]))

            gate_two = gate("\u00f72 test", "last digit 4", CHALK_CYAN)
            gate_two.move_to(np.array([LEFT_X, 1.06, 0]))
            gate_three = gate("\u00f73 test", "7+2+2+4 = 15", CHALK_PINK)
            gate_three.move_to(np.array([RIGHT_X, 1.06, 0]))
            tick_two = mark_yes(0.95).move_to(gate_two.get_corner(UR)
                                              + np.array([-0.24, -0.26, 0]))
            tick_three = mark_yes(0.95).move_to(gate_three.get_corner(UR)
                                                + np.array([-0.24, -0.26, 0]))
            gate_two = VGroup(gate_two, tick_two)
            gate_three = VGroup(gate_three, tick_three)

            six = badge_card("6", CHALK_GREEN, size=30, width=0.86, height=0.86
                             ).move_to(np.array([BOARD_CX, 0.02, 0]))
            left_arrow = Arrow(gate_two.get_bottom() + DOWN * 0.04,
                               six.get_left() + LEFT * 0.06, buff=0,
                               color=CHALK_CYAN, stroke_width=2.6,
                               tip_length=0.16,
                               max_stroke_width_to_length_ratio=10)
            right_arrow = Arrow(gate_three.get_bottom() + DOWN * 0.04,
                                six.get_right() + RIGHT * 0.06, buff=0,
                                color=CHALK_PINK, stroke_width=2.6,
                                tip_length=0.16,
                                max_stroke_width_to_length_ratio=10)

            result = board_text("7224 is divisible by 6", 19, CHALK_GREEN,
                                "BOLD").move_to(np.array([BOARD_CX, -0.92, 0]))
            result_box = SurroundingRectangle(result, color=CHALK_GREEN,
                                              buff=0.18, corner_radius=0.10,
                                              stroke_width=2.4)
            strip = board_text("Divisible by 6  =  divisible by BOTH 2 and 3.",
                               16, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(num), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(gate_two), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(gate_three), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(GrowArrow(left_arrow), GrowArrow(right_arrow),
                      run_time=0.6)
            self.play(FadeIn(six, scale=0.7), run_time=0.4)
            self.play(FadeIn(result, shift=UP * 0.08), Create(result_box),
                      run_time=0.5)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.45)
            self.closing(tracker, result_box, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: real life -- 372 runners into teams of six -----------------
    def beat8_application(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("Use It: Relay Teams of Six", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            lot = measure_card(r"372\text{ runners}", CHALK_YELLOW, 22
                               ).move_to(np.array([BOARD_CX, 2.02, 0]))

            gate_two = gate("\u00f72 test", "ends in 2", CHALK_CYAN)
            gate_two.move_to(np.array([LEFT_X, 1.02, 0]))
            gate_three = gate("\u00f73 test", "3+7+2 = 12", CHALK_PINK)
            gate_three.move_to(np.array([RIGHT_X, 1.02, 0]))
            tick_two = mark_yes(0.95).move_to(gate_two.get_corner(UR)
                                              + np.array([-0.24, -0.26, 0]))
            tick_three = mark_yes(0.95).move_to(gate_three.get_corner(UR)
                                                + np.array([-0.24, -0.26, 0]))
            gate_two = VGroup(gate_two, tick_two)
            gate_three = VGroup(gate_three, tick_three)

            six = badge_card("6", CHALK_GREEN, size=30, width=0.86, height=0.86
                             ).move_to(np.array([BOARD_CX, -0.02, 0]))
            left_arrow = Arrow(gate_two.get_bottom() + DOWN * 0.04,
                               six.get_left() + LEFT * 0.06, buff=0,
                               color=CHALK_CYAN, stroke_width=2.6,
                               tip_length=0.16,
                               max_stroke_width_to_length_ratio=10)
            right_arrow = Arrow(gate_three.get_bottom() + DOWN * 0.04,
                                six.get_right() + RIGHT * 0.06, buff=0,
                                color=CHALK_PINK, stroke_width=2.6,
                                tip_length=0.16,
                                max_stroke_width_to_length_ratio=10)

            answer = board_text("62 teams  \u00b7  nobody left out",
                                21, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -0.98, 0]))
            answer_box = SurroundingRectangle(answer, color=CHALK_GREEN,
                                              buff=0.20, corner_radius=0.10,
                                              stroke_width=2.4)
            strip = board_text("6 \u00d7 62 = 372, and no long division.",
                               16, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(lot, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(gate_two), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(gate_three), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(GrowArrow(left_arrow), GrowArrow(right_arrow),
                      run_time=0.6)
            self.play(FadeIn(six, scale=0.7), run_time=0.4)
            self.play(FadeIn(answer, shift=UP * 0.08), Create(answer_box),
                      run_time=0.5)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.45)
            self.closing(tracker, answer_box, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 9: your turn -- test 12345 ------------------------------------
    def beat9_challenge(self) -> None:
        with self.voiceover(text=NARRATION["scene9"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", 26, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, 2.62, 0]))
            sub = board_text("Which of these divide 12345?", 18,
                             CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, 2.24, 0]))

            divisors = ("2", "3", "5", "6", "9", "10")
            buttons = VGroup(*[badge_card(d, CHALK_AMBER, size=26, width=0.80,
                                          height=0.64) for d in divisors]
                             ).arrange(RIGHT, buff=0.44).move_to(
                np.array([BOARD_CX, 1.66, 0]))
            marks = {d: (mark_no(1.0, CHALK_RED) if d in ("2", "6", "9", "10")
                         else mark_yes(1.0)).move_to(
                np.array([buttons[i].get_center()[0], 1.16, 0]))
                for i, d in enumerate(divisors)}

            num, parts = digit_tiles("12345", size=31)
            num.move_to(np.array([BOARD_CX, 0.46, 0]))

            why_three = board_text("1+2+3+4+5 = 15  \u2192  divisible by 3",
                                   22, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -0.46, 0]))
            why_five = board_text("ends in 5  \u2192  divisible by 5", 22,
                                  CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -1.02, 0]))
            answer = board_text("12345 is divisible by 3 and by 5.", 20,
                                CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.68, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(sub), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.08)
                                    for b in buttons], lag_ratio=0.12),
                      run_time=0.8)
            self.play(FadeIn(num), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            # the shared THINK clock, centred on the board (story_common)
            play_challenge_countdown(self, seconds=4, sfx=self.sfx,
                                     position=np.array([BOARD_CX, BOARD_CY, 0]))

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(marks["2"], scale=0.7),
                      FadeIn(marks["6"], scale=0.7), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(marks["5"], scale=0.7),
                      FadeIn(marks["10"], scale=0.7), run_time=0.5)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(marks["3"], scale=0.7),
                      FadeIn(marks["9"], scale=0.7),
                      FadeIn(why_three, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(why_five, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(answer, shift=UP * 0.08), run_time=0.5)
            self.closing(tracker, answer, color=CHALK_YELLOW)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap and thank-you ---------------------------------------
    def beat10_recap(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("Divisibility Rules", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            rows = VGroup(
                rule_line("LAST DIGIT", "2: 0,2,4,6,8   \u00b7   5: 0 or 5"
                                        "   \u00b7   10: 0", CHALK_CYAN,
                          width=8.6, size=19),
                rule_line("ADD THE DIGITS", "3: sum \u00f7 3   \u00b7   "
                                            "9: sum \u00f7 9", CHALK_GREEN,
                          width=8.6, size=19),
                rule_line("COMBINE TWO TESTS", "6: divisible by 2 AND by 3",
                          CHALK_PINK, width=8.6, size=19),
            ).arrange(DOWN, buff=0.24, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX, 1.08, 0]))

            examples = board_text("452 \u2192 2     5785 \u2192 5     "
                                  "9846 \u2192 9     7224 \u2192 6", 18,
                                  CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -0.52, 0]))
            message = board_text("LOOK.  ADD.  COMBINE.", 24, CHALK_YELLOW,
                                 "BOLD").move_to(
                np.array([BOARD_CX, -1.18, 0]))
            promise = board_text("Check divisibility without doing the "
                                 "division.", 16, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            thanks = board_text("Thank You for Watching!", 30, CHALK_WHITE,
                                "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 0.42, 0]))
            bye = board_text("See you in the next lesson :)", 22, CHALK_YELLOW,
                             "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY - 0.52, 0]))
            board_group = VGroup(heading, rows, examples, message, promise)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(rows[0], shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(rows[1], shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(rows[2], shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(examples, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(message, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(promise, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["success"], gain=-11)

            self.wait(leftover(tracker, "b4"))
            # the closing card, over the same board
            self.play(FadeOut(board_group), run_time=0.5)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.5)
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.play(Indicate(thanks, color=CHALK_YELLOW, scale_factor=1.03),
                      run_time=rt(tracker.get_remaining_duration()))
            self._capture_srt(tracker)

        self.wait(END_HOLD)

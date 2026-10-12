    # ================================================================ beats ==
    # Advanced Divisibility Rules for 4, 8 and 11.
    #
    # SYNC RULE for every reveal: wait for the narration bookmark that ends the
    # phrase describing a thing, and only then bring it on.  Playing first and
    # waiting afterwards shows the picture a whole window early, which reads as
    # broken sync.
    #
    # Layout rules, so the audits stay clean:
    #   * the heading sits on ROW_Y, the closing strip on STRIP_Y (-1.80, lifted
    #     0.15 clear of the subtitle zone after the production audit);
    #     nothing at all sits below CAPTION_SAFE_Y (-2.00);
    #   * two-column work is centred on LEFT_X and RIGHT_X;
    #   * nothing is placed on a line, and no card, chip or dot is placed over
    #     another element -- checked by audit_clearance.py and
    #     audit_sync_overlap.py.
    #
    # Scene order: a real-world cold open, the title, the six known rules, why 4
    # and 8 need two and three digits (with the textbook's 56496 and 93624), the
    # two lenses, the alternating test for 11 and a number that fails it, the
    # three-clue dashboard, a stadium-sized application, the staged challenge and
    # the recap.
    def closing(self, tracker, mob=None, color=CHALK_YELLOW, run_time=None):
        """Consume the tail of the narration window on the last reveal."""
        budget = rt(tracker.get_remaining_duration()) if run_time is None \
            else run_time
        if mob is None:
            self.wait(max(budget, 0.0))
        else:
            self.play(Indicate(mob, color=color, scale_factor=1.03),
                      run_time=max(budget, MIN_RT))

    # -- Scene 0a: cold open -- why anyone cares ------------------------------
    # The production audit's first note: the video used to open on "three more
    # divisibility tests", a promise with nothing behind it.  This scene runs
    # BEFORE the title card and grounds 4, 8 and 11 in places the class has
    # already met them: the calendar, tiling, and a bank account number.
    def beat_cold_open(self) -> None:
        with self.voiceover(text=NARRATION["hook"]) as tracker:
            self.reset_board()

            heading = board_text("Why These Tests?", 26, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))

            rows = VGroup(
                VGroup(badge_card("4", CHALK_CYAN, size=24, width=0.72,
                                  height=0.62),
                       board_text("a leap year comes every four years", 16,
                                  CHALK_WHITE, "BOLD")).arrange(RIGHT, buff=0.30),
                VGroup(badge_card("8", CHALK_GREEN, size=24, width=0.72,
                                  height=0.62),
                       board_text("a tiler checks if eight tiles fit", 16,
                                  CHALK_WHITE, "BOLD")).arrange(RIGHT, buff=0.30),
                VGroup(badge_card("11", CHALK_PINK, size=24, width=0.72,
                                  height=0.62),
                       board_text("a bank reads long account numbers", 16,
                                  CHALK_WHITE, "BOLD")).arrange(RIGHT, buff=0.30),
            ).arrange(DOWN, buff=0.42).move_to(
                np.array([BOARD_CX, 0.62, 0]))
            punch = board_text("The tests are already around you.", 18,
                               CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.16, 0]))
            strip = board_text("Look for them outside the textbook.", 16,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(rows[0], shift=RIGHT * 0.10), run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(rows[1], shift=RIGHT * 0.10), run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(rows[2], shift=RIGHT * 0.10), run_time=0.5)
            self.play(FadeIn(punch, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, punch)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 0: title ------------------------------------------------------
    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Advanced Divisibility Tests", 30, CHALK_WHITE,
                               "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 1.62, 0]))
            sub = board_text("Quick Tests for 4, 8 and 11", 20, CHALK_YELLOW,
                             "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 0.86, 0]))
            chips = VGroup(*[badge_card(d, CHALK_CYAN, size=30, width=0.96,
                                        height=0.80)
                             for d in ("4", "8", "11")]
                           ).arrange(RIGHT, buff=0.60).move_to(
                np.array([BOARD_CX, BOARD_CY - 0.24, 0]))
            promise = board_text("Test divisibility without dividing the whole "
                                 "number.", 16, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -1.20, 0]))
            tag = board_text("Zoom  ·  Zoom deeper  ·  Alternate", 19,
                             CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(title, shift=UP * 0.10), run_time=0.5)
            self.play(FadeIn(sub, shift=UP * 0.10), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in chips],
                                  lag_ratio=0.18), run_time=0.9)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(promise, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(tag, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, tag)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: the scanner gains three modes ------------------------------
    def beat1_hook(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("New Numbers, New Patterns", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            known = VGroup(*[badge_card(d, CHALK_WHITE, size=20, width=0.62,
                                        height=0.50)
                             for d in ("2", "3", "5", "6", "9", "10")]
                           ).arrange(RIGHT, buff=0.30).move_to(
                np.array([BOARD_CX, 1.98, 0]))
            known_note = board_text("the six rules you already know", 15,
                                    CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, 1.52, 0]))

            fresh = VGroup(*[badge_card(d, CHALK_CYAN, size=30, width=0.96,
                                        height=0.80)
                             for d in ("4", "8", "11")]
                           ).arrange(RIGHT, buff=0.60).move_to(
                np.array([BOARD_CX, 0.66, 0]))
            fresh_note = board_text("three new rules", 16, CHALK_CYAN, "BOLD"
                                    ).move_to(np.array([BOARD_CX, 0.06, 0]))

            question = board_text("One digit is not enough.", 19, CHALK_PINK,
                                  "BOLD").move_to(np.array([BOARD_CX, -0.60, 0]))
            answer = board_text("Four and eight look deeper.  Eleven "
                                "alternates.", 17, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -1.18, 0]))
            strip = board_text("Find the pattern. Avoid full division.", 16,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.08)
                                    for c in known], lag_ratio=0.12),
                      run_time=0.7)
            self.play(FadeIn(known_note), run_time=0.35)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in fresh],
                                  lag_ratio=0.25), run_time=0.9)
            self.play(FadeIn(fresh_note), run_time=0.35)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(question, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(answer, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["click"], gain=-15)
            self.closing(tracker, answer, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: why 4 needs only two digits --------------------------------
    def beat2_why4(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("Why 4 Needs Only Two Digits", 23,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, ROW_Y, 0]))
            num, tiles = digit_tiles("76532", size=27)
            num.move_to(np.array([BOARD_CX, 2.02, 0]))
            split = chalk_math(r"76532 = 76500 + 32", size=28, color=CHALK_YELLOW
                               ).move_to(np.array([BOARD_CX, 1.22, 0]))
            hundred = chalk_math(r"76500 = 765 \times 100"
                                 r"\qquad 100 \div 4 = 25", size=24,
                                 color=CHALK_CYAN).move_to(
                np.array([BOARD_CX, 0.54, 0]))
            note = board_text("the first part is already divisible by 4", 16,
                              CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -0.12, 0]))
            # One row rather than two: the banner lift left no room for a
            # separate "32 / 4 = 8" line above a boxed verdict, so the last
            # division and the verdict share the closing row.
            tail = VGroup(
                chalk_math(r"32 \div 4 = 8", size=26, color=CHALK_YELLOW),
                board_text("so 76532 is divisible by 4", 18, CHALK_GREEN,
                           "BOLD"),
            ).arrange(RIGHT, buff=0.42).move_to(
                np.array([BOARD_CX, -0.86, 0]))
            strip = board_text("For 4  \u2192  the last 2 digits.", 16,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))
            result_box = SurroundingRectangle(tail, color=CHALK_GREEN,
                                              buff=0.16, corner_radius=0.10,
                                              stroke_width=2.4)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(num), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(split, shift=UP * 0.08), run_time=0.5)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(hundred, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(note, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(tail, shift=UP * 0.08), Create(result_box),
                      run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, result_box, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: apply the rule -- 56496 ------------------------------------
    def beat3_apply4(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()

            heading = board_text("Last 2 Digits", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            num, tiles = digit_tiles("56496", size=29)
            num.move_to(np.array([BOARD_CX, 1.98, 0]))
            lens = digit_lens(tiles, 2)
            faded = dim_outside(tiles, 2)
            working = chalk_math(r"96 = 4 \times 24", size=28, color=CHALK_YELLOW
                                 ).move_to(np.array([BOARD_CX, 0.98, 0]))
            tick = mark_yes(1.05).move_to(
                np.array([BOARD_CX - 1.62, 0.34, 0]))
            rule_card = rule_line("DIVISIBILITY BY 4", "test the last two digits",
                                  CHALK_CYAN, width=7.0, size=18).move_to(
                np.array([BOARD_CX, -1.14, 0]))
            strip = board_text("Works for numbers greater than 100.", 16,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(num), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(lens), faded.animate.set_opacity(0.22),
                      run_time=0.6)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(working, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(tick, scale=0.6), run_time=0.3)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            result = board_text("56496 is divisible by 4", 18, CHALK_GREEN,
                                "BOLD").move_to(
                np.array([BOARD_CX, -0.34, 0]))
            result_box = SurroundingRectangle(result, color=CHALK_GREEN,
                                              buff=0.18, corner_radius=0.10,
                                              stroke_width=2.4)
            self.play(FadeIn(result, shift=UP * 0.08), Create(result_box),
                      run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(rule_card, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, rule_card, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: why 8 needs three digits -----------------------------------
    def beat4_why8(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()

            heading = board_text("Why 8 Needs Three Digits", 23, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            hundred = VGroup(
                badge_card("100", CHALK_PINK, size=22, width=1.10, height=0.56),
                mark_no(0.95),
                badge_card("1000 = 8 \u00d7 125", CHALK_GREEN, size=20,
                           width=2.60, height=0.56),
                mark_yes(0.95),
            ).arrange(RIGHT, buff=0.24).move_to(
                np.array([BOARD_CX, 2.02, 0]))

            num, tiles = digit_tiles("93624", size=27)
            num.move_to(np.array([BOARD_CX, 1.24, 0]))
            split = chalk_math(r"93624 = 93000 + 624", size=26,
                               color=CHALK_YELLOW).move_to(
                np.array([BOARD_CX, 0.50, 0]))
            note = board_text("93000 is a multiple of 1000, so it is already "
                              "divisible by 8", 15, CHALK_GREEN, "BOLD"
                              ).move_to(np.array([BOARD_CX, -0.20, 0]))
            result = board_text("624 = 8 \u00d7 78, so 93624 is divisible by 8",
                                17, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -1.02, 0]))
            result_box = SurroundingRectangle(result, color=CHALK_GREEN,
                                              buff=0.18, corner_radius=0.10,
                                              stroke_width=2.4)
            strip = board_text("For 8  \u2192  the last 3 digits.", 16,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(hundred), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(num), run_time=0.4)
            self.play(FadeIn(split, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(note, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(result, shift=UP * 0.08), Create(result_box),
                      run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, result_box, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: two lenses, two different widths ---------------------------
    def beat5_two_lenses(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            self.reset_board()

            heading = board_text("Don't Mix the Two", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            num, tiles = digit_tiles("2104", size=29)
            num.move_to(np.array([BOARD_CX, 1.90, 0]))
            lens_two = digit_lens(tiles, 2, CHALK_CYAN)
            lens_three = digit_lens(tiles, 3, CHALK_PINK)

            four_line = board_text("for 4: last two \u2192 04 = 4", 17,
                                   CHALK_CYAN, "BOLD").move_to(
                np.array([BOARD_CX, 1.02, 0]))
            eight_line = board_text("for 8: last three \u2192 104 = 8 \u00d7 13",
                                    17, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, 0.30, 0]))
            memory = board_text("4 \u2192 TWO digits          8 \u2192 THREE digits",
                                22, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -0.66, 0]))
            strip = board_text("4 looks at two digits; 8 looks at three.", 16,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(num), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(lens_two), run_time=0.4)
            self.play(FadeIn(four_line, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(ReplacementTransform(lens_two, lens_three), run_time=0.5)
            self.play(FadeIn(eight_line, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(memory, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, memory)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: divisibility by 11 -- 1221 ---------------------------------
    def beat6_rule11(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("Divisibility by 11", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            num, tiles = digit_tiles("1221", size=29)
            num.move_to(np.array([BOARD_CX - 0.55, 2.02, 0]))
            tags = place_tags(tiles, color=CHALK_CYAN, size=11, y_shift=-0.46)
            start = board_text("start from the right  \u2190", 14, CHALK_YELLOW,
                               "BOLD").move_to(np.array([3.55, 2.02, 0]))

            odd = basket("odd places", "1 + 2", 3, CHALK_CYAN, width=3.4
                         ).move_to(np.array([LEFT_X, 0.50, 0]))
            even = basket("even places", "2 + 1", 3, CHALK_PINK, width=3.4
                          ).move_to(np.array([RIGHT_X, 0.50, 0]))
            diff = chalk_math(r"3 - 3 = 0", size=30, color=CHALK_YELLOW
                              ).move_to(np.array([BOARD_CX, -0.62, 0]))
            result = board_text("1221 is divisible by 11", 18, CHALK_GREEN,
                                "BOLD").move_to(
                np.array([BOARD_CX, -1.16, 0]))
            result_box = SurroundingRectangle(result, color=CHALK_GREEN,
                                              buff=0.14, corner_radius=0.10,
                                              stroke_width=2.4)
            strip = board_text("Alternate  \u2192  Add  \u2192  Compare.", 16,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(num), run_time=0.4)

            self.wait(leftover(tracker, "b0"))
            self.play(LaggedStart(*[FadeIn(t, scale=0.7) for t in tags],
                                  lag_ratio=0.18), run_time=0.7)
            self.play(FadeIn(start), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(odd, shift=UP * 0.10), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(even, shift=UP * 0.10), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(diff, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(result, shift=UP * 0.08), Create(result_box),
                      run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, result_box, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: the same test failing -- 6535 ------------------------------
    def beat7_11_fails(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("When the Test Fails", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            num, tiles = digit_tiles("6535", size=29)
            num.move_to(np.array([BOARD_CX - 0.55, 2.02, 0]))
            tags = place_tags(tiles, color=CHALK_CYAN, size=11, y_shift=-0.46)

            odd = basket("odd places", "5 + 5", 10, CHALK_CYAN, width=3.4
                         ).move_to(np.array([LEFT_X, 0.50, 0]))
            even = basket("even places", "3 + 6", 9, CHALK_PINK, width=3.4
                          ).move_to(np.array([RIGHT_X, 0.50, 0]))
            diff = chalk_math(r"10 - 9 = 1", size=30, color=CHALK_YELLOW
                              ).move_to(np.array([BOARD_CX, -0.62, 0]))
            result = board_text("6535 is not divisible by 11", 18, CHALK_PINK,
                                "BOLD").move_to(
                np.array([BOARD_CX, -1.16, 0]))
            result_box = SurroundingRectangle(result, color=CHALK_PINK,
                                              buff=0.14, corner_radius=0.10,
                                              stroke_width=2.4)
            strip = VGroup(
                board_text("1221 \u2192 0", 17, CHALK_WHITE, "BOLD"),
                mark_yes(0.85),
                board_text("6535 \u2192 1", 17, CHALK_WHITE, "BOLD"),
                mark_no(0.85),
            ).arrange(RIGHT, buff=0.30).move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(num), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(t, scale=0.7) for t in tags],
                                  lag_ratio=0.18), run_time=0.7)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(odd), FadeIn(even), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(diff, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(result, shift=UP * 0.08), Create(result_box),
                      run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, result_box, color=CHALK_PINK)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: three rules, three clues -----------------------------------
    def beat8_dashboard(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("Three Advanced Rules, Three Clues", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, ROW_Y, 0]))
            panels = VGroup(
                zone_panel("\u00f74  LAST 2 DIGITS",
                           ["56496 \u2192 96", "96 = 4 \u00d7 24"],
                           CHALK_CYAN, size=14),
                zone_panel("\u00f78  LAST 3 DIGITS",
                           ["93624 \u2192 624", "624 = 8 \u00d7 78"],
                           CHALK_GREEN, size=14),
                zone_panel("\u00f711  ALTERNATING SUMS",
                           ["1221 \u2192 3 and 3", "3 - 3 = 0"],
                           CHALK_PINK, size=14),
            ).arrange(RIGHT, buff=0.30).move_to(
                np.array([BOARD_CX, 0.90, 0]))
            memory = board_text("4 \u2192 2 digits     8 \u2192 3 digits     "
                                "11 \u2192 2 alternating groups", 18,
                                CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -0.86, 0]))
            strip = board_text("Three clues instead of three tricks.", 16,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(panels[0], shift=UP * 0.10), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(panels[1], shift=UP * 0.10), run_time=0.55)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(panels[2], shift=UP * 0.10), run_time=0.55)
            self.play(FadeIn(memory, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, memory)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8b: the rule doing real work -- 56496 seats -------------------
    # The audit's second note: a 10-15 s real-world application before "Your
    # Turn", so the three tests are shown deciding something a viewer cares
    # about.  The textbook's own 56496 carries it.
    def beat_apply(self) -> None:
        with self.voiceover(text=NARRATION["apply"]) as tracker:
            self.reset_board()

            heading = board_text("Real Seats, Real Boxes", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, ROW_Y, 0]))
            num, tiles = digit_tiles("56496", size=28)
            num.move_to(np.array([BOARD_CX, 1.86, 0]))
            lens = digit_lens(tiles, 2, CHALK_CYAN)
            box_row = VGroup(
                board_text("boxes of four seats", 15, CHALK_WHITE, "BOLD"),
                *[badge_card("4", CHALK_CYAN, size=18, width=0.56, height=0.50)
                  for _ in range(4)],
            ).arrange(RIGHT, buff=0.24).move_to(
                np.array([BOARD_CX, 1.00, 0]))
            work = chalk_math(r"96 \div 4 = 24", size=28, color=CHALK_YELLOW
                              ).move_to(np.array([BOARD_CX, 0.28, 0]))
            result = board_text("so 56496 divides by four", 18, CHALK_GREEN,
                                "BOLD").move_to(
                np.array([BOARD_CX, -0.30, 0]))
            result_box = SurroundingRectangle(result, color=CHALK_GREEN,
                                              buff=0.15, corner_radius=0.10,
                                              stroke_width=2.4)
            call = verdict(True, "no seat is left over", size=16).move_to(
                np.array([BOARD_CX, -1.05, 0]))
            strip = board_text("The rule decides before the boxes are packed.",
                               16, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, STRIP_Y, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(num), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(box_row, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(lens), run_time=0.45)
            self.play(FadeIn(work, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(result, shift=UP * 0.08), Create(result_box),
                      run_time=0.5)
            self.add_sound(self.sfx["ding"], gain=-13)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(call, scale=0.85), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.closing(tracker, call, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # The audit called the old single-window challenge "cramped": two six-digit
    # numbers, five checks and two verdicts on the board at once.  It is now
    # staged sequentially -- the 4 and 8 work on the left, then it clears, then
    # the centred 11 check in larger type.
    def beat9_challenge(self) -> None:
        with self.voiceover(text=NARRATION["scene9"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", 26, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, 2.62, 0]))
            sub = board_text("Choose the rule before you calculate.", 17,
                             CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, 2.10, 0]))

            # --- first number: 4 and 8, worked on the left -------------------
            a_num, a_tiles = digit_tiles("726352", size=25)
            a_num.move_to(np.array([LEFT_X - 0.15, 1.58, 0]))
            a_four = VGroup(
                board_text("last two: 52 = 4 \u00d7 13", 15, CHALK_CYAN,
                           "BOLD"), mark_yes(0.85),
            ).arrange(RIGHT, buff=0.18).move_to(
                np.array([LEFT_X - 0.15, 0.94, 0]))
            a_eight = VGroup(
                board_text("last three: 352 = 8 \u00d7 44", 15, CHALK_GREEN,
                           "BOLD"), mark_yes(0.85),
            ).arrange(RIGHT, buff=0.18).move_to(
                np.array([LEFT_X - 0.15, 0.44, 0]))
            answer_a = board_text("726352 is divisible by 4 and by 8.", 17,
                                  CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -0.72, 0]))
            answer_a_box = SurroundingRectangle(answer_a, color=CHALK_GREEN,
                                                buff=0.16, corner_radius=0.10,
                                                stroke_width=2.4)
            group_a = VGroup(a_num, a_four, a_eight, answer_a, answer_a_box)

            # --- second number: 11, centred, larger type ---------------------
            b_num, b_tiles = digit_tiles("10824", size=32)
            b_num.move_to(np.array([BOARD_CX, 1.48, 0]))
            b_odd = board_text("odd places:  4 + 8 + 1 = 13", 20, CHALK_CYAN,
                               "BOLD").move_to(
                np.array([BOARD_CX - 1.95, 0.62, 0]))
            b_even = board_text("even places:  2 + 0 = 2", 20, CHALK_PINK,
                                "BOLD").move_to(
                np.array([BOARD_CX + 2.26, 0.62, 0]))
            b_diff = VGroup(
                chalk_math(r"13 - 2 = 11", size=30, color=CHALK_YELLOW),
                mark_yes(1.0),
            ).arrange(RIGHT, buff=0.26).move_to(
                np.array([BOARD_CX, -0.25, 0]))
            answer_b = board_text("10824 is divisible by 11.", 19, CHALK_PINK,
                                  "BOLD").move_to(
                np.array([BOARD_CX, -1.05, 0]))
            answer_b_box = SurroundingRectangle(answer_b, color=CHALK_PINK,
                                                buff=0.16, corner_radius=0.10,
                                                stroke_width=2.4)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(sub), run_time=0.4)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(a_num, shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            # the shared THINK clock, centred on the board (story_common)
            play_challenge_countdown(self, seconds=4, sfx=self.sfx,
                                     position=np.array([BOARD_CX, BOARD_CY, 0]))

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(a_four, shift=UP * 0.08),
                      FadeIn(a_eight, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(answer_a, shift=UP * 0.08), Create(answer_a_box),
                      run_time=0.5)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeOut(group_a), run_time=0.4)
            self.play(FadeIn(b_num, shift=UP * 0.08), run_time=0.45)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b5"))
            self.play(FadeIn(b_odd, shift=UP * 0.08),
                      FadeIn(b_even, shift=UP * 0.08), run_time=0.7)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(b_diff, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(answer_b, shift=UP * 0.08), Create(answer_b_box),
                      run_time=0.5)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, answer_b_box, color=CHALK_PINK)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap and thank-you ---------------------------------------
    def beat10_recap(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("Advanced Divisibility Rules", 24,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, ROW_Y, 0]))
            rows = VGroup(
                rule_line("4", "last 2 digits   (564 | 96)", CHALK_CYAN,
                          width=8.6, size=19),
                rule_line("8", "last 3 digits   (93 | 624)", CHALK_GREEN,
                          width=8.6, size=19),
                rule_line("11", "alternating sums   (1221: 3 - 3 = 0)",
                          CHALK_PINK, width=8.6, size=19),
            ).arrange(DOWN, buff=0.24, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX, 1.24, 0]))
            examples = VGroup(
                VGroup(board_text("96 \u00f7 4", 18, CHALK_WHITE, "BOLD"),
                       mark_yes(0.9)).arrange(RIGHT, buff=0.20),
                VGroup(board_text("624 \u00f7 8", 18, CHALK_WHITE, "BOLD"),
                       mark_yes(0.9)).arrange(RIGHT, buff=0.20),
                VGroup(board_text("1221 \u2192 0", 18, CHALK_WHITE, "BOLD"),
                       mark_yes(0.9)).arrange(RIGHT, buff=0.20),
            ).arrange(RIGHT, buff=0.62).move_to(
                np.array([BOARD_CX, -0.52, 0]))
            message = board_text("ZOOM.  ZOOM MORE.  ALTERNATE.", 23,
                                 CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, -1.12, 0]))
            promise = board_text("Test divisibility without dividing the whole "
                                 "number.", 16, CHALK_WHITE, "BOLD").move_to(
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
            self.play(FadeOut(board_group), run_time=0.5)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.5)
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.play(Indicate(thanks, color=CHALK_YELLOW, scale_factor=1.03),
                      run_time=rt(tracker.get_remaining_duration()))
            self._capture_srt(tracker)

        self.wait(END_HOLD)

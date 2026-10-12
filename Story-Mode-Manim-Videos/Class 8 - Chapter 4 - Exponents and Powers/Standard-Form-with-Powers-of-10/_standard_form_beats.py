    # ================================================================ beats ==
    # Standard Form with Powers of 10 (Class 8, Chapter 4, Storymode 05 -- the
    # closing video of the five-part sequence).
    #
    # SYNC RULE for every reveal: wait for the narration bookmark that ends the
    # phrase describing a thing, and only then bring it on.  Playing first and
    # waiting afterwards shows the picture a whole window early, which reads as
    # broken sync.
    #
    # Layout rules, so the audits stay clean:
    #   * the heading sits on ROW_Y (2.72), the closing strip on STRIP_Y (-1.80);
    #     nothing at all sits below y = -2.00;
    #   * the visual identity is the DECIMAL-POINT ELEVATOR: the numeral is laid
    #     out slot by slot and the decimal marker walks it one place at a time
    #     while a counter ticks, so the exponent is counted, not announced;
    #   * nothing is placed on a line, and no card, digit or chip is placed over
    #     another element -- checked by audit_clearance.py and
    #     audit_sync_overlap.py;
    #   * the challenge uses the series' shared 10-second THINK clock, dead
    #     centre of the board, with the question cards around it.
    ROW_Y = 2.72
    BANNER_Y = -1.30
    STRIP_Y = -1.80
    TRACK_Y = 0.95
    COUNT_Y = 1.78

    def closing(self, tracker, mob=None, color=CHALK_YELLOW, run_time=None):
        """Consume the tail of the narration window on the last reveal."""
        budget = rt(tracker.get_remaining_duration()) if run_time is None \
            else run_time
        if mob is None:
            self.wait(max(budget, 0.0))
        else:
            self.play(Indicate(mob, color=color, scale_factor=1.03),
                      run_time=max(budget, MIN_RT))

    def run_elevator(self, tracker, mark, track, marker, counter, target,
                     next_mark=None, max_rt=0.90):
        """Walk the decimal point to `target`, in step with the narration.

        Where the voice does not count aloud (scenes 3 and 5) the walk is spread
        across the whole narration window, so the marker can never reach the end
        while the sentence is still being spoken; `next_mark` is the bookmark
        that closes that window."""
        self.wait(leftover(tracker, mark))
        start = track.point_pos
        n = abs(target - start)
        step = 1 if target > start else -1
        span = max(tracker.time_until_bookmark(next_mark), 0.0) \
            if next_mark else 0.0
        step_rt = min(max(span / n, 0.22), max_rt) if span else 0.22
        for k in range(1, n + 1):
            pos = start + k * step
            new_counter = at(board_text(str(k), 20, CHALK_CYAN, "BOLD"),
                             BOARD_CX, COUNT_Y)
            self.play(marker.animate.move_to(
                np.array([track.positions[pos], TRACK_Y, 0.0])),
                Transform(counter, new_counter), run_time=step_rt)
            self.add_sound(self.sfx["click"], gain=-26)
        track.point_pos = target

    def run_elevator_marked(self, tracker, marks, track, marker, counter,
                            direction=-1, step_rt=0.30):
        """One place per narration bookmark -- used where the voice counts
        aloud, so the counter shows the number being spoken as it is said."""
        for k, mark in enumerate(marks, start=1):
            self.wait(leftover(tracker, mark))
            pos = track.point_pos + direction
            new_counter = at(board_text(str(k), 20, CHALK_CYAN, "BOLD"),
                             BOARD_CX, COUNT_Y)
            self.play(marker.animate.move_to(
                np.array([track.positions[pos], TRACK_Y, 0.0])),
                Transform(counter, new_counter), run_time=step_rt)
            self.add_sound(self.sfx["click"], gain=-26)
            track.point_pos = pos

    def elevator(self, digits, point_pos, note="the decimal point",
                 label_x=3.95):
        """A ready-made elevator: the track, its marker and its counter.

        `label_x` moves the little legend to whichever end is free -- scenes 5
        and 6 use the right-hand side for their drawing."""
        track = decimal_slots(digits, point_pos, y=TRACK_Y,
                                 pitch=0.44, size=34)
        marker = deci_marker(track.positions[point_pos], TRACK_Y)
        counter = at(board_text("0", 20, CHALK_CYAN, "BOLD"), BOARD_CX, COUNT_Y)
        label = at(board_text(note, 14, CHALK_WHITE, "BOLD"), label_x, TRACK_Y)
        return track, marker, counter, label

    # -- Scene 0: title ------------------------------------------------------
    def beat_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            heading = at(board_text("Standard Form with Powers of 10", 24,
                                    CHALK_WHITE, "BOLD"), BOARD_CX, 2.10)
            sub = at(board_text("Writing Very Large and Very Small Numbers", 17,
                                CHALK_AMBER, "BOLD"), BOARD_CX, 1.45)
            big = at(chalk_math(r"300,000,000 = 3 \times 10^8", size=32,
                                color=CHALK_CYAN), BOARD_CX, 0.65)
            small = at(chalk_math(r"0.000003 = 3 \times 10^{-6}", size=32,
                                  color=CHALK_YELLOW), BOARD_CX, -0.35)
            promise = at(board_text("Move the decimal, count the places, write "
                                    "the power.", 16, CHALK_WHITE, "BOLD"),
                         BOARD_CX, -1.25)
            strip = at(board_text("One notation for both extremes.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.5)
            self.play(FadeIn(sub, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(big, shift=UP * 0.08),
                      FadeIn(small, shift=UP * 0.08), run_time=0.6)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(promise, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, big, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: from the cosmic to the microscopic -------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("One Notation for Both Extremes", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sun_grp = at(sun(0.28), -2.60, 1.98)
            big = at(law_card(board_text("300,000,000 m", 24, CHALK_WHITE,
                                         "BOLD"),
                              "the Sun's distance", CHALK_WHITE, width=3.30,
                              height=1.10), -2.60, 0.92)
            wire = at(chip_icon(0.58), 3.40, 1.98)
            small = at(law_card(board_text("0.000003 m", 24, CHALK_WHITE,
                                           "BOLD"),
                                "the wire in a chip", CHALK_WHITE, width=3.30,
                                height=1.10), 3.40, 0.92)
            zoom = DoubleArrow(np.array([-0.85, 0.92, 0.0]),
                               np.array([1.65, 0.92, 0.0]), buff=0,
                               stroke_width=3.0, color=CHALK_WHITE,
                               max_tip_length_to_length_ratio=0.10)
            zoom_lab = at(board_text("same notation", 13, CHALK_WHITE, "BOLD"),
                          BOARD_CX, 0.42)
            question = at(board_text("Can one notation handle both?", 19,
                                     CHALK_PINK, "BOLD"), BOARD_CX, 1.98)
            ans_big = at(chalk_math(r"= 3 \times 10^8", size=30,
                                    color=CHALK_CYAN), -2.60, -0.40)
            ans_small = at(chalk_math(r"= 3 \times 10^{-6}", size=30,
                                      color=CHALK_YELLOW), 3.40, -0.40)
            strip = at(board_text("The exponent tells the scale.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(sun_grp, scale=0.8), FadeIn(big, shift=UP * 0.08),
                      run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(wire, scale=0.8), FadeIn(small, shift=UP * 0.08),
                      FadeIn(question, shift=UP * 0.08), run_time=0.6)
            self.play(GrowArrow(zoom), FadeIn(zoom_lab), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(ans_big, shift=UP * 0.08),
                      FadeIn(ans_small, shift=UP * 0.08), run_time=0.6)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, question, color=CHALK_PINK)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: powers of ten are a scale ----------------------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Exponent Tells the Scale", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            ruler = scale_marks([-3, -2, -1, 0, 1, 2, 3])
            left_tag = at(board_text("\u2190  SMALLER", 15, CHALK_PINK, "BOLD"),
                          -3.20, 1.95)
            right_tag = at(board_text("LARGER  \u2192", 15, CHALK_GREEN, "BOLD"),
                           4.20, 1.95)
            pos_note = at(chip("positive exponent: large scale", CHALK_GREEN,
                               size=16), 2.65, -0.95)
            neg_note = at(chip("negative exponent: small scale", CHALK_PINK,
                               size=16), -1.85, -0.95)
            strip = at(board_text("POWERS OF TEN ARE A SCALE.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(ruler.axis), FadeIn(ruler.ticks[3]),
                      FadeIn(VGroup(ruler.labels[6], ruler.labels[7])),
                      run_time=0.7)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(VGroup(*ruler.ticks[4:]), scale=0.85),
                      FadeIn(VGroup(*ruler.labels[8:])),
                      FadeIn(right_tag, shift=LEFT * 0.08), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(VGroup(*ruler.ticks[:3]), scale=0.85),
                      FadeIn(VGroup(*ruler.labels[:6])),
                      FadeIn(left_tag, shift=RIGHT * 0.08), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(pos_note, scale=0.9), FadeIn(neg_note, scale=0.9),
                      run_time=0.55)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: 300 000 000 -> 3 x 10^8 ------------------------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Large \u2192 Positive Exponent", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            track, marker, counter, label = self.elevator("300000000", 9)
            result = at(chalk_math(r"3 \times 10^8", size=36,
                                   color=CHALK_GREEN), BOARD_CX, -0.05)
            rule = at(chip("decimal moved LEFT 8 places \u2192 +8", CHALK_GREEN,
                           size=17), BOARD_CX, -0.95)
            strip = at(board_text("MOVE LEFT, COUNT, EXPONENT IS POSITIVE.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(track), FadeIn(marker, scale=0.8),
                      FadeIn(counter), FadeIn(label), run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.run_elevator(tracker, "b1", track, marker, counter, 1,
                              next_mark="b2")

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(result, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(rule, scale=0.9), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, result, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: 6 020 000 000 -> 6.02 x 10^9 -------------------------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("Count the Moves", 22, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            track, marker, counter, label = self.elevator("6020000000", 10)
            rings = VGroup(*[SurroundingRectangle(track.glyphs[i], buff=0.05,
                                                  color=CHALK_GREEN,
                                                  stroke_width=2.6)
                             for i in range(3)])
            result = at(chalk_math(r"6.02 \times 10^9", size=36,
                                   color=CHALK_GREEN), BOARD_CX, -0.05)
            keep = at(chip("the digits we keep: 602", CHALK_GREEN, size=16),
                      3.60, -0.95)
            strip = at(board_text("LARGE NUMBER \u2192 POSITIVE EXPONENT.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(track), FadeIn(marker, scale=0.8),
                      FadeIn(counter), FadeIn(label), run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.run_elevator_marked(tracker, [f"b{k}" for k in range(2, 11)],
                                     track, marker, counter, direction=-1)

            self.wait(leftover(tracker, "b11"))
            self.play(FadeIn(rings), run_time=0.5)
            self.play(FadeIn(keep, scale=0.9), run_time=0.45)

            self.wait(leftover(tracker, "b12"))
            self.play(FadeIn(result, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, result, color=CHALK_GREEN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: 0.000003 -> 3 x 10^-6 --------------------------------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("Small \u2192 Negative Exponent", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            track, marker, counter, label = self.elevator(
                "0000003", 1, label_x=-2.30)
            result = at(chalk_math(r"3 \times 10^{-6}", size=36,
                                   color=CHALK_YELLOW), BOARD_CX, -0.05)
            signed = at(chip("six places, and the exponent is \u22126",
                             CHALK_PINK, size=16), BOARD_CX, -0.95)
            strip = at(board_text("SMALL NUMBER \u2192 NEGATIVE EXPONENT.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            wire = at(chip_icon(0.54), 4.15, 1.55)
            wire_lab = at(board_text("a wire in a chip", 13, CHALK_CYAN, "BOLD"),
                          4.15, 0.90)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(track), FadeIn(marker, scale=0.8),
                      FadeIn(counter), FadeIn(label), run_time=0.6)
            self.play(FadeIn(wire, scale=0.85), FadeIn(wire_lab),
                      run_time=0.5)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.run_elevator(tracker, "b1", track, marker, counter, 7,
                              next_mark="b2")

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(result, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(signed, scale=0.9), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, result, color=CHALK_YELLOW)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: 0.00001275 -> 1.275 x 10^-5 --------------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("Keep the Digits \u2014 Change the Scale",
                                    21, CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            track, marker, counter, label = self.elevator(
                "000001275", 1, label_x=-2.55)
            rings = VGroup(*[SurroundingRectangle(track.glyphs[i], buff=0.05,
                                                  color=CHALK_CYAN,
                                                  stroke_width=2.6)
                             for i in range(5, 9)])
            result = at(chalk_math(r"1.275 \times 10^{-5}", size=34,
                                   color=CHALK_CYAN), BOARD_CX, -0.05)
            same = at(chip("same quantity, different representation",
                           CHALK_CYAN, size=16), BOARD_CX, -0.95)
            strip = at(board_text("KEEP THE DIGITS \u2014 CHANGE THE SCALE.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            cell = at(plant_cell(0.98, 0.74), 4.10, 1.60)
            cell_lab = at(board_text("a plant cell", 13, CHALK_GREEN, "BOLD"),
                          4.10, 0.95)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)
            self.play(FadeIn(track), FadeIn(marker, scale=0.8),
                      FadeIn(counter), FadeIn(label), run_time=0.6)
            self.play(FadeIn(cell, scale=0.85), FadeIn(cell_lab),
                      FadeIn(rings), run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.run_elevator_marked(tracker, [f"b{k}" for k in range(2, 7)],
                                     track, marker, counter, direction=1)

            self.wait(leftover(tracker, "b7"))
            self.play(FadeIn(result, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(same, scale=0.9), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, result, color=CHALK_CYAN)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: standard form back to usual form ---------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Standard Form \u2192 Usual Form", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            row1 = at(card(VGroup(
                chalk_math(r"4.67 \times 10^4 = 46700", size=28,
                           color=CHALK_CYAN),
                board_text("positive \u2192 decimal right 4", 14, CHALK_GREEN,
                           "BOLD")).arrange(RIGHT, buff=0.60),
                CHALK_CYAN, pad_y=0.24), BOARD_CX, 1.35)
            row2 = at(card(VGroup(
                chalk_math(r"3.02 \times 10^{-6} = 0.00000302", size=24,
                           color=CHALK_PINK),
                board_text("negative \u2192 decimal left 6", 14, CHALK_PINK,
                           "BOLD")).arrange(RIGHT, buff=0.60),
                CHALK_PINK, pad_y=0.24), BOARD_CX, 0.05)
            warn = at(chip("these directions are for the reverse conversion",
                           CHALK_YELLOW, size=16), BOARD_CX, -1.05)
            strip = at(board_text("POSITIVE \u2192 RIGHT;  NEGATIVE \u2192 "
                                  "LEFT.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(row1, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(row2, shift=UP * 0.08), run_time=0.6)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(warn, scale=0.9), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, warn)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the complete map -------------------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("Which Direction Am I Converting?", 22,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            rows = VGroup(
                at(card(VGroup(
                    chalk_math(r"6020000000 \rightarrow 6.02 \times 10^9",
                               size=20, color=CHALK_WHITE),
                    board_text("large: decimal left \u2192 positive", 13,
                               CHALK_GREEN, "BOLD")).arrange(RIGHT, buff=0.55),
                    CHALK_GREEN, pad_y=0.22), BOARD_CX, 1.75),
                at(card(VGroup(
                    chalk_math(r"0.00001275 \rightarrow 1.275 \times 10^{-5}",
                               size=20, color=CHALK_WHITE),
                    board_text("small: decimal right \u2192 negative", 13,
                               CHALK_PINK, "BOLD")).arrange(RIGHT, buff=0.55),
                    CHALK_PINK, pad_y=0.22), BOARD_CX, 0.85),
                at(card(VGroup(
                    chalk_math(r"4.67 \times 10^4 \rightarrow 46700", size=20,
                               color=CHALK_WHITE),
                    board_text("positive \u2192 decimal right", 13, CHALK_GREEN,
                               "BOLD")).arrange(RIGHT, buff=0.55),
                    CHALK_GREEN, pad_y=0.22), BOARD_CX, -0.05),
                at(card(VGroup(
                    chalk_math(r"3.02 \times 10^{-6} \rightarrow 0.00000302",
                               size=20, color=CHALK_WHITE),
                    board_text("negative \u2192 decimal left", 13, CHALK_PINK,
                               "BOLD")).arrange(RIGHT, buff=0.55),
                    CHALK_PINK, pad_y=0.22), BOARD_CX, -0.95),
            )
            strip = at(board_text("FIRST ASK WHICH WAY YOU ARE CONVERTING.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(rows[0], shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(rows[1], shift=UP * 0.08), run_time=0.5)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(rows[2], shift=UP * 0.08),
                      FadeIn(rows[3], shift=UP * 0.08), run_time=0.6)
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 9: your turn -- three conversions, then the 10-second clock ---
    def beat_s9(self) -> None:
        with self.voiceover(text=NARRATION["s9q"]) as tracker:
            self.reset_board()

            heading = at(board_text("YOUR TURN", 26, CHALK_PINK, "BOLD"),
                         BOARD_CX, ROW_Y)
            qa = at(q_card("small \u2192 standard form",
                           chalk_math("0.0000456", size=20, color=CHALK_WHITE)),
                    -2.55, 1.45)
            qb = at(q_card("large \u2192 standard form",
                           chalk_math("6020000000", size=18,
                                      color=CHALK_WHITE)),
                    3.55, 1.45)
            qc = at(q_card("standard \u2192 usual form",
                           chalk_math(r"5.8 \times 10^{7}", size=20,
                                      color=CHALK_WHITE)),
                    -2.55, 0.20)

            ans_a = at(answer_row("A",
                                  chalk_math(r"0.0000456 = 4.56 \times 10^{-5}",
                                             26, color=CHALK_CYAN),
                                  "right 5 places", CHALK_CYAN),
                       BOARD_CX, 1.55)
            ans_b = at(answer_row("B",
                                  chalk_math(r"6020000000 = 6.02 \times 10^9",
                                             26, color=CHALK_YELLOW),
                                  "left 9 places", CHALK_YELLOW),
                       BOARD_CX, 0.70)
            ans_c = at(answer_row("C",
                                  chalk_math(r"5.8 \times 10^{7} = 58000000", 26,
                                             color=CHALK_PINK),
                                  "right 7 places", CHALK_PINK),
                       BOARD_CX, -0.15)
            done = at(board_text("SMALL \u2192 NEGATIVE   \u00b7   LARGE \u2192 "
                                 "POSITIVE", 18, CHALK_YELLOW, "BOLD"),
                      BOARD_CX, -1.05)
            strip = at(board_text("MOVE, COUNT, CHOOSE THE SIGN, WRITE.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.5)

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
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, done)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap -----------------------------------------------------
    def beat_s10(self) -> None:
        with self.voiceover(text=NARRATION["s10"]) as tracker:
            self.reset_board()

            heading = at(board_text("Move \u2192 Count \u2192 Sign \u2192 Write",
                                    22, CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            steps = at(VGroup(
                chip("MOVE", CHALK_CYAN, size=16),
                chip("COUNT", CHALK_CYAN, size=16),
                chip("CHOOSE THE SIGN", CHALK_YELLOW, size=16),
                chip("WRITE  \u00d7 10\u207f", CHALK_YELLOW, size=16),
            ).arrange(RIGHT, buff=0.32), BOARD_CX, 1.35)
            big = at(chalk_math(r"300,000,000 = 3 \times 10^8", size=30,
                                color=CHALK_CYAN), BOARD_CX, 0.35)
            small = at(chalk_math(r"0.000003 = 3 \times 10^{-6}", size=30,
                                  color=CHALK_YELLOW), BOARD_CX, -0.45)
            strip = at(board_text("POWERS OF 10 WRITE THE VERY LARGE AND THE "
                                  "VERY SMALL.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            thanks = at(board_text("Thank You for Watching!", 30, CHALK_WHITE,
                                   "BOLD"), BOARD_CX, 0.62)
            bye = at(board_text("See you in the next lesson :)", 22,
                                CHALK_YELLOW, "BOLD"), BOARD_CX, -0.32)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.45)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(steps, shift=UP * 0.08),
                      FadeIn(big, shift=UP * 0.08), run_time=0.7)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(small, shift=UP * 0.08), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(strip, shift=UP * 0.08), run_time=0.4)
            self.add_sound(self.sfx["success"], gain=-11)

            # the closing card is narrated: it appears as the voice says
            # "Thank you for watching the chapter,", the goodbye line as the
            # voice says "and see you in the next lesson."
            self.wait(leftover(tracker, "b3"))
            self.play(FadeOut(heading), FadeOut(steps), FadeOut(big),
                      FadeOut(small), FadeOut(strip), run_time=0.5)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.5)

            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.closing(tracker, thanks, run_time=1.2)
            self._capture_srt(tracker)

        self.wait(END_HOLD)







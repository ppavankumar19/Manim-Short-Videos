    # ================================================================ beats ==
    # Angles (Class 6 Maths, Chapter 4, Storymode 04).
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
    #   * the persistent angle O-A-B is fixed (O_PT / A_PT / B_PT) so every
    #     scene draws exactly the same opening; its one arm runs along the
    #     bottom-left and the free space to the right carries the labels;
    #   * the angle marker (the light fill + its arc) is deliberately small, so
    #     the words of the interior, the arms and the exterior sit in open board
    #     rather than inside a filled shape;
    #   * the challenge uses the series' shared 10-second THINK clock, dead
    #     centre of the board, and the four question cards sit in the four
    #     corners so the badge never covers one.

    def closing(self, tracker, mob=None, color=CHALK_YELLOW, run_time=None):
        """Consume the tail of the narration window on the last reveal."""
        budget = rt(tracker.get_remaining_duration()) if run_time is None \
            else run_time
        if mob is None:
            self.wait(max(budget, 0.0))
        else:
            self.play(Indicate(mob, color=color, scale_factor=1.03),
                      run_time=max(budget, MIN_RT))

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

    def answer_row(self, tag, headline, note, color, width=8.60, height=0.62,
                   buff=0.36):
        """One revealed answer, laid out in fixed columns: the letter, then the
        result, then the note.  Every row starts at the same x, so A, B, C and D
        line up down the board and the spacing is identical on every row."""
        lab = board_text(tag, 17, color, "BOLD")
        name = board_text(headline, 17, color, "BOLD")
        txt = board_text(note, 14, CHALK_WHITE, "BOLD")
        row = VGroup(lab, name, txt).arrange(RIGHT, buff=buff)
        box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                               stroke_color=color, stroke_width=1.8,
                               fill_color=PANEL_FILL, fill_opacity=0.6)
        box.move_to(np.array([BOARD_CX, 0.0, 0.0]))
        row.move_to(box.get_center())
        left = BOARD_CX - width / 2.0 + 0.34
        row.shift(np.array([left - row.get_left()[0], 0.0, 0.0]))
        return VGroup(box, row)

    def mini_angle(self, vertex="O", arms=("C", "D"), color=CHALK_GREEN,
                   points=(), show_arms=True):
        """A small angle for the challenge cards (centred on the origin):
        two arrowed rays from one vertex, the arc mark and the letters.

        Every letter is placed in open space -- a letter inside this narrow
        wedge would sit on one of the arms, which the clearance audit rejects --
        so a region point's letter stands just outside the opening and reads as
        its label."""
        o = np.array([0.0, 0.0, 0.0])
        len1, len2 = 0.98, 0.88
        r1 = ray_from(o, 0.0, len1, color, 3.2, 0.20)
        r2 = ray_from(o, 45.0, len2, color, 3.2, 0.20)
        arc = arc_at(o, 0.0, 45.0, 0.36, CHALK_AMBER, 2.6)
        end1 = o + np.array([len1, 0.0, 0.0])
        end2 = o + np.array([len2 * np.cos(np.radians(45)),
                             len2 * np.sin(np.radians(45)), 0.0])
        parts = [r1, r2, arc,
                 dot_point(vertex, o[0], o[1], CHALK_PINK, size=13,
                           label_dx=(0.04, -0.28))]
        if show_arms:
            parts.append(dot_point(arms[0], end1[0], end1[1], CHALK_CYAN,
                                   size=13, label_dx=(0.18, -0.08)))
            parts.append(dot_point(arms[1], end2[0], end2[1], CHALK_CYAN,
                                   size=13, label_dx=(0.06, 0.26)))
        spots = {"in": ((0.35, 0.27), (0.36, 0.12)),
                 "on": ((0.74, 0.0), (0.0, -0.32)),
                 "out": ((-0.38, 0.35), (-0.10, 0.30))}
        for name, kind in points:
            (px, py), (dx, dy) = spots[kind]
            col = {"in": CHALK_CYAN, "on": CHALK_AMBER,
                   "out": CHALK_PINK}[kind]
            parts.append(dot_point(name, px, py, col, size=12,
                                   label_dx=(dx, dy)))
        return VGroup(*parts)

    def ask_card(self, title, lines, color=CHALK_CYAN, width=3.00, pad=0.14,
                 title_size=15, line_size=12, buff=0.26):
        """A 'your turn' card whose question is written in words."""
        head = board_text(title, title_size, color, "BOLD")
        body = VGroup(*[board_text(line, line_size, CHALK_WHITE, "BOLD")
                        for line in lines]).arrange(DOWN, buff=0.26)
        content = VGroup(head, body).arrange(DOWN, buff=buff)
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

            title = at(board_text("Understanding Angles", 28, CHALK_PINK,
                                  "BOLD"), BOARD_CX, 1.66)
            sub = at(board_text("Vertex · Arms · Angle Regions", 18, CHALK_WHITE,
                                "BOLD"), BOARD_CX, 1.00)

            o = np.array([-0.60, -1.05, 0.0])
            r1 = ray_from(o, 0.0, 2.40, CHALK_GREEN, 4.0)
            r2 = ray_from(o, 40.0, 1.90, CHALK_GREEN, 4.0)
            arc = arc_at(o, 0.0, 40.0, 0.62, CHALK_AMBER, 2.6)
            wedge = wedge_at(o, 0.0, 40.0, 0.62, CHALK_CYAN, 0.20)
            vert = dot_point("O", o[0], o[1], CHALK_PINK, size=18,
                             label_dx=(-0.24, -0.28))
            labs = VGroup(at(board_text("arms", 14, CHALK_GREEN, "BOLD"),
                             0.10, 0.05),
                          at(board_text("vertex", 14, CHALK_PINK, "BOLD"),
                             -1.15, -0.72))
            verts_lab = at(board_text("A", 18, CHALK_WHITE, "BOLD"),
                           o[0] + 1.90 * np.cos(np.radians(40)) + 0.10,
                           o[1] + 1.90 * np.sin(np.radians(40)) + 0.22)
            strip = at(board_text("Two rays with one common endpoint make an "
                                  "angle.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(title, shift=UP * 0.08), run_time=0.55)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(wedge), Create(r1), Create(r2), Create(arc),
                      FadeIn(vert), run_time=0.85)
            self.play(FadeIn(labs, shift=UP * 0.05), FadeIn(verts_lab),
                      run_time=0.55)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 1: what makes an angle ----------------------------------------
    def beat_s1(self) -> None:
        with self.voiceover(text=NARRATION["s1"]) as tracker:
            self.reset_board()

            heading = at(board_text("What Makes an Angle?", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("A door opening, and the hands of a clock.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            # The door and the clock are the two everyday openings; they sit
            # symmetrically about the board's own centre line (0.50).
            door = door_icon()
            shift = np.array([DOOR_X, 0.62, 0.0]) - door.get_center()
            door.shift(shift)
            hinge = door.hinge + shift
            door_lab = at(board_text("a door opening", 14, CHALK_WHITE, "BOLD"),
                          DOOR_X, -0.66)
            clock = at(clock_icon(), CLOCK_X, 0.72)
            clock_lab = at(board_text("clock hands", 14, CHALK_WHITE, "BOLD"),
                           CLOCK_X, -0.66)

            banner = at(board_text("AN ANGLE APPEARS", 19, CHALK_YELLOW, "BOLD"),
                        BOARD_CX, BANNER_Y)
            strip = at(board_text("Keep only the two directions and you have "
                                  "two rays from one point.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(door.frame), Create(door.threshold),
                      Create(door.leaf), FadeIn(door_lab, shift=UP * 0.05),
                      run_time=0.60)
            self.play(Rotate(door.leaf, angle=-0.30, about_point=hinge),
                      Create(door.swing), run_time=0.80)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(clock.face), Create(clock.hand1),
                      Create(clock.hand2), FadeIn(clock_lab, shift=UP * 0.05),
                      run_time=0.60)
            self.play(Rotate(clock.hand2, angle=0.95,
                             about_point=clock.get_center()), run_time=0.80)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeOut(door), FadeOut(door_lab), FadeOut(clock),
                      FadeOut(clock_lab), run_time=0.50)
            o = np.array([O_PT[0], O_PT[1], 0.0])
            bare_r1 = ray_from(o, ANG_B, RAY_B_LEN, CHALK_GREEN, RAY_W)
            bare_r2 = ray_from(o, ANG_A, RAY_A_LEN, CHALK_GREEN, RAY_W)
            bare_arc = arc_at(o, ANG_B, ANG_A, MARK_R, CHALK_AMBER, 2.8)
            bare_vert = dot_point("O", o[0], o[1], CHALK_PINK, size=20,
                                  label_dx=(-0.24, -0.26))
            self.play(Create(bare_r1), Create(bare_r2), Create(bare_arc),
                      FadeIn(bare_vert), run_time=0.75)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 2: two rays form an angle -------------------------------------
    def beat_s2(self) -> None:
        with self.voiceover(text=NARRATION["s2"]) as tracker:
            self.reset_board()

            heading = at(board_text("Two Rays Form an Angle", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("They start at the same point, O.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            o = np.array([O_PT[0], O_PT[1], 0.0])
            ray_b = ray_from(o, ANG_B, RAY_B_LEN, CHALK_GREEN, RAY_W)
            ray_a = ray_from(o, ANG_A, RAY_A_LEN, CHALK_GREEN, RAY_W)
            vert = dot_point("O", o[0], o[1], CHALK_PINK, size=20,
                             label_dx=(-0.24, -0.26))
            end_a = dot_point("A", A_PT[0], A_PT[1], CHALK_CYAN, size=18,
                              label_dx=(A_LABEL[0] - A_PT[0],
                                        A_LABEL[1] - A_PT[1]))
            end_b = dot_point("B", B_PT[0], B_PT[1], CHALK_CYAN, size=18,
                              label_dx=(0.24, 0.22))
            arc = arc_at(o, ANG_B, ANG_A, MARK_R, CHALK_AMBER, 2.8)
            wedge = wedge_at(o, ANG_B, ANG_A, MARK_R, CHALK_CYAN, 0.20)
            name = at(chalk_math(r"\angle AOB", size=32, color=CHALK_YELLOW),
                      3.30, 0.60)

            banner = at(board_text("2 RAYS + 1 ENDPOINT = ANGLE", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The opening between the rays is the angle.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(ray_b), FadeIn(vert), FadeIn(end_b),
                      run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Create(ray_a), FadeIn(end_a), run_time=0.60)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(wedge), Create(arc), run_time=0.50)
            self.play(FadeIn(name, scale=0.9), run_time=0.45)
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 3: vertex and arms --------------------------------------------
    def beat_s3(self) -> None:
        with self.voiceover(text=NARRATION["s3"]) as tracker:
            self.reset_board()

            heading = at(board_text("Vertex and Arms", 20, CHALK_AMBER, "BOLD"),
                         BOARD_CX, ROW_Y)
            sub = at(board_text("The common endpoint and the two rays.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            o = np.array([O_PT[0], O_PT[1], 0.0])
            ray_b = ray_from(o, ANG_B, RAY_B_LEN, CHALK_GREEN, RAY_W)
            ray_a = ray_from(o, ANG_A, RAY_A_LEN, CHALK_GREEN, RAY_W)
            arc = arc_at(o, ANG_B, ANG_A, MARK_R, CHALK_AMBER, 2.8)
            wedge = wedge_at(o, ANG_B, ANG_A, MARK_R, CHALK_CYAN, 0.20)
            vert = dot_point("O", o[0], o[1], CHALK_PINK, size=22,
                             label_dx=(-0.26, -0.28))
            end_a = dot_point("A", A_PT[0], A_PT[1], CHALK_CYAN, size=18,
                              label_dx=(A_LABEL[0] - A_PT[0],
                                        A_LABEL[1] - A_PT[1]))
            end_b = dot_point("B", B_PT[0], B_PT[1], CHALK_CYAN, size=18,
                              label_dx=(B_LABEL[0] - B_PT[0],
                                        B_LABEL[1] - B_PT[1]))

            r1 = at(board_text("VERTEX", 15, CHALK_PINK, "BOLD"), 3.30, 1.30)
            r2 = at(board_text("the common endpoint", 13, CHALK_WHITE, "BOLD"),
                    3.30, 0.86)
            r3 = at(board_text("ARM 1 · OA", 15, CHALK_CYAN, "BOLD"),
                    3.30, 0.22)
            r4 = at(board_text("ARM 2 · OB", 15, CHALK_GREEN, "BOLD"),
                    3.30, -0.50)
            r5 = at(board_text("also called sides", 13, CHALK_WHITE, "BOLD"),
                    3.30, -0.94)

            strip = at(board_text("The two rays are the arms, also called the "
                                  "sides.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(ray_b), Create(ray_a), Create(arc), FadeIn(wedge),
                      FadeIn(vert), FadeIn(end_a), FadeIn(end_b), run_time=0.70)

            self.wait(leftover(tracker, "b0"))
            self.play(Indicate(vert, color=CHALK_PINK, scale_factor=1.35),
                      FadeIn(r1, shift=UP * 0.05), FadeIn(r2, shift=UP * 0.05),
                      run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(Indicate(ray_a, color=CHALK_CYAN, scale_factor=1.02),
                      FadeIn(r3, shift=UP * 0.05), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(Indicate(ray_b, color=CHALK_GREEN, scale_factor=1.02),
                      FadeIn(r4, shift=UP * 0.05), FadeIn(r5, shift=UP * 0.05),
                      run_time=0.60)
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 4: the naming rule --------------------------------------------
    def beat_s4(self) -> None:
        with self.voiceover(text=NARRATION["s4"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Middle Letter", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("With three letters, the vertex goes in the "
                                "middle.", 17, CHALK_WHITE, "BOLD"),
                     BOARD_CX, SUB_Y)

            o = np.array([O_PT[0], O_PT[1], 0.0])
            ray_b = ray_from(o, ANG_B, RAY_B_LEN, CHALK_GREEN, RAY_W)
            ray_a = ray_from(o, ANG_A, RAY_A_LEN, CHALK_GREEN, RAY_W)
            arc = arc_at(o, ANG_B, ANG_A, MARK_R, CHALK_AMBER, 2.8)
            wedge = wedge_at(o, ANG_B, ANG_A, MARK_R, CHALK_CYAN, 0.20)
            vert = dot_point("O", o[0], o[1], CHALK_PINK, size=22,
                             label_dx=(-0.26, -0.28))
            end_a = dot_point("A", A_PT[0], A_PT[1], CHALK_CYAN, size=18,
                              label_dx=(A_LABEL[0] - A_PT[0],
                                        A_LABEL[1] - A_PT[1]))
            end_b = dot_point("B", B_PT[0], B_PT[1], CHALK_CYAN, size=18,
                              label_dx=(B_LABEL[0] - B_PT[0],
                                        B_LABEL[1] - B_PT[1]))

            row_y = (1.34, 0.62, -0.10, -0.82)
            n1 = at(chalk_math(r"\angle AOB", size=30, color=CHALK_GREEN),
                    2.95, row_y[0])
            n2 = at(chalk_math(r"\angle BOA", size=30, color=CHALK_GREEN),
                    2.95, row_y[1])
            n3 = at(chalk_math(r"\angle OAB", size=30, color=CHALK_RED),
                    2.95, row_y[2])
            n4 = at(chalk_math(r"\angle ABO", size=30, color=CHALK_RED),
                    2.95, row_y[3])
            m1 = mark_yes((4.20, row_y[0]))
            m2 = mark_yes((4.20, row_y[1]))
            m3 = mark_no((4.20, row_y[2]))
            m4 = mark_no((4.20, row_y[3]))

            strip = at(board_text("The middle letter must be the vertex O.", 16,
                                  CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(ray_b), Create(ray_a), Create(arc), FadeIn(wedge),
                      FadeIn(vert), FadeIn(end_a), FadeIn(end_b), run_time=0.70)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(n1, scale=0.9), Create(m1), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(n2, scale=0.9), Create(m2), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(n3, scale=0.9), Create(m3),
                      FadeIn(n4, scale=0.9), Create(m4), run_time=0.70)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 5: AOB = BOA, and the short name ------------------------------
    def beat_s5(self) -> None:
        with self.voiceover(text=NARRATION["s5"]) as tracker:
            self.reset_board()

            heading = at(board_text("Same Angle, Two Names", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Reading the arms in the other order.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            o = np.array([O_PT[0], O_PT[1], 0.0])
            ray_b = ray_from(o, ANG_B, RAY_B_LEN, CHALK_GREEN, RAY_W)
            ray_a = ray_from(o, ANG_A, RAY_A_LEN, CHALK_GREEN, RAY_W)
            arc = arc_at(o, ANG_B, ANG_A, MARK_R, CHALK_AMBER, 2.8)
            wedge = wedge_at(o, ANG_B, ANG_A, MARK_R, CHALK_CYAN, 0.20)
            vert = dot_point("O", o[0], o[1], CHALK_PINK, size=22,
                             label_dx=(-0.26, -0.28))
            end_a = dot_point("A", A_PT[0], A_PT[1], CHALK_CYAN, size=18,
                              label_dx=(A_LABEL[0] - A_PT[0],
                                        A_LABEL[1] - A_PT[1]))
            end_b = dot_point("B", B_PT[0], B_PT[1], CHALK_CYAN, size=18,
                              label_dx=(B_LABEL[0] - B_PT[0],
                                        B_LABEL[1] - B_PT[1]))
            hl_a = ray_from(o, ANG_A, RAY_A_LEN, CHALK_CYAN, 6.0)

            equal = at(chalk_math(r"\angle AOB = \angle BOA", size=28,
                                  color=CHALK_YELLOW), 3.20, 0.70)
            short = at(chip("angle O", CHALK_CYAN, size=16), 3.20, -0.20)
            short_note = at(board_text("only with one angle at O", 13,
                                       CHALK_WHITE, "BOLD"), 3.60, -0.95)

            strip = at(board_text("Reversing the arms does not change the "
                                  "angle.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(ray_b), Create(ray_a), Create(arc), FadeIn(wedge),
                      FadeIn(vert), FadeIn(end_a), FadeIn(end_b), run_time=0.70)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(hl_a), run_time=0.30)
            self.play(Indicate(ray_b, color=CHALK_YELLOW, scale_factor=1.02),
                      run_time=0.45)
            self.play(FadeOut(hl_a), run_time=0.25)
            self.play(FadeIn(equal, scale=0.9), run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(short, scale=0.9),
                      FadeIn(short_note, shift=UP * 0.05), run_time=0.50)
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.45)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 6: the interior -----------------------------------------------
    def beat_s6(self) -> None:
        with self.voiceover(text=NARRATION["s6"]) as tracker:
            self.reset_board()

            heading = at(board_text("The Interior", 20, CHALK_AMBER, "BOLD"),
                         BOARD_CX, ROW_Y)
            sub = at(board_text("The region between the two arms.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            o = np.array([O_PT[0], O_PT[1], 0.0])
            ray_b = ray_from(o, ANG_B, RAY_B_LEN, CHALK_GREEN, RAY_W)
            ray_a = ray_from(o, ANG_A, RAY_A_LEN, CHALK_GREEN, RAY_W)
            arc = arc_at(o, ANG_B, ANG_A, MARK_R, CHALK_AMBER, 2.8)
            wedge = wedge_at(o, ANG_B, ANG_A, MARK_R, CHALK_CYAN, 0.22)
            vert = dot_point("O", o[0], o[1], CHALK_PINK, size=22,
                             label_dx=(-0.26, -0.28))
            interior_lab = at(board_text("INTERIOR", 14, CHALK_CYAN, "BOLD"),
                              0.55, -0.45)
            x_pt = dot_point("X", -0.80, -0.30, CHALK_CYAN, size=18,
                             label_dx=(-0.06, -0.28))
            banner = at(board_text("INTERIOR = BETWEEN THE ARMS", 18,
                                   CHALK_YELLOW, "BOLD"), BOARD_CX, BANNER_Y)
            strip = at(board_text("The interior follows the arms outward.",
                                  16, CHALK_WHITE, "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(ray_b), Create(ray_a), FadeIn(vert), run_time=0.60)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(wedge), Create(arc),
                      FadeIn(interior_lab, shift=UP * 0.05), run_time=0.60)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(x_pt, scale=0.85), run_time=0.45)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(banner, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 7: boundary and exterior --------------------------------------
    def beat_s7(self) -> None:
        with self.voiceover(text=NARRATION["s7"]) as tracker:
            self.reset_board()

            heading = at(board_text("Boundary and Exterior", 20, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("On an arm, or outside the opening.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            o = np.array([O_PT[0], O_PT[1], 0.0])
            ray_b = ray_from(o, ANG_B, RAY_B_LEN, CHALK_GREEN, RAY_W)
            ray_a = ray_from(o, ANG_A, RAY_A_LEN, CHALK_GREEN, RAY_W)
            arc = arc_at(o, ANG_B, ANG_A, MARK_R, CHALK_AMBER, 2.8)
            wedge = wedge_at(o, ANG_B, ANG_A, MARK_R, CHALK_CYAN, 0.20)
            vert = dot_point("O", o[0], o[1], CHALK_PINK, size=22,
                             label_dx=(-0.26, -0.28))
            s_pt = dot_point("S", 0.60, -0.97, CHALK_AMBER, size=18,
                             label_dx=(0.0, -0.30))
            z_pt = dot_point("Z", -1.40, 0.60, CHALK_PINK, size=18,
                             label_dx=(-0.06, 0.26))
            c1 = at(chip("INTERIOR", CHALK_CYAN, size=14), 3.30, 0.62)
            c2 = at(chip("BOUNDARY", CHALK_AMBER, size=14), 3.30, -0.10)
            c3 = at(chip("EXTERIOR", CHALK_PINK, size=14), 3.30, -0.82)
            traveller = Dot(radius=0.06, color=CHALK_YELLOW, fill_opacity=1.0)
            traveller.move_to(np.array([-1.40, 0.60, 0.0]))

            strip = at(board_text("Interior, boundary and exterior — three "
                                  "parts of the plane.", 16, CHALK_WHITE,
                                  "BOLD"), BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)
            self.play(Create(ray_b), Create(ray_a), Create(arc), FadeIn(wedge),
                      FadeIn(vert), run_time=0.65)

            self.wait(leftover(tracker, "b0"))
            self.play(FadeIn(s_pt, scale=0.85), FadeIn(c1, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(z_pt, scale=0.85), FadeIn(c2, scale=0.9),
                      FadeIn(c3, scale=0.9), run_time=0.55)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(traveller, scale=0.8), run_time=0.30)
            self.play(traveller.animate.move_to(np.array([-0.80, -0.30, 0.0])),
                      run_time=1.05)
            self.add_sound(self.sfx["click"], gain=-15)
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.closing(tracker, strip)
            self._capture_srt(tracker)
        self.wait(TRANSITION_HOLD)

    # -- Scene 8: where does each point belong -------------------------------
    def beat_s8(self) -> None:
        with self.voiceover(text=NARRATION["s8"]) as tracker:
            self.reset_board()

            heading = at(board_text("Where Does Each Point Belong?", 20,
                                    CHALK_AMBER, "BOLD"), BOARD_CX, ROW_Y)
            sub = at(board_text("Angle PQR, with its vertex at Q.", 17,
                                CHALK_WHITE, "BOLD"), BOARD_CX, SUB_Y)

            o = np.array([O_PT[0], O_PT[1], 0.0])
            ray_b = ray_from(o, ANG_B, RAY_B_LEN, CHALK_GREEN, RAY_W)
            ray_a = ray_from(o, ANG_A, RAY_A_LEN, CHALK_GREEN, RAY_W)
            arc = arc_at(o, ANG_B, ANG_A, MARK_R, CHALK_AMBER, 2.8)
            wedge = wedge_at(o, ANG_B, ANG_A, MARK_R, CHALK_CYAN, 0.20)
            vert = dot_point("Q", o[0], o[1], CHALK_PINK, size=20,
                             label_dx=(-0.28, -0.26))
            end_p = dot_point("P", A_PT[0], A_PT[1], CHALK_CYAN, size=18,
                              label_dx=(A_LABEL[0] - A_PT[0],
                                        A_LABEL[1] - A_PT[1]))
            end_r = dot_point("R", B_PT[0], B_PT[1], CHALK_CYAN, size=18,
                              label_dx=(B_LABEL[0] - B_PT[0],
                                        B_LABEL[1] - B_PT[1]))
            m_pt = dot_point("M", -0.80, -0.30, CHALK_CYAN, size=18,
                             label_dx=(-0.06, -0.28))
            n_pt = dot_point("N", 0.60, -0.97, CHALK_AMBER, size=18,
                             label_dx=(0.0, -0.30))
            t_pt = dot_point("T", -1.40, 0.60, CHALK_PINK, size=18,
                             label_dx=(-0.06, 0.26))
            c1 = at(chip("M · INTERIOR", CHALK_CYAN, size=14), 3.30, 0.62)
            c2 = at(chip("N · BOUNDARY", CHALK_AMBER, size=14), 3.30, -0.10)
            c3 = at(chip("T · EXTERIOR", CHALK_PINK, size=14), 3.30, -0.82)

            strip = at(board_text("Every other point lies in one of the three "
                                  "regions.", 16, CHALK_WHITE, "BOLD"),
                       BOARD_CX, STRIP_Y)

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.50)
            self.play(FadeIn(sub, shift=UP * 0.06), run_time=0.40)

            self.wait(leftover(tracker, "b0"))
            self.play(Create(ray_b), Create(ray_a), Create(arc), FadeIn(wedge),
                      FadeIn(vert), FadeIn(end_p), FadeIn(end_r), run_time=0.70)
            self.add_sound(self.sfx["pop"], gain=-13)

            self.wait(leftover(tracker, "b1"))
            self.play(FadeIn(n_pt, scale=0.85), FadeIn(c2, scale=0.9),
                      run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            self.play(FadeIn(m_pt, scale=0.85), FadeIn(c1, scale=0.9),
                      FadeIn(t_pt, scale=0.85), FadeIn(c3, scale=0.9),
                      run_time=0.70)
            self.play(FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["ding"], gain=-13)
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

            qa = at(self.q_card("vertex? arms?",
                                self.mini_angle("O", ("C", "D"), CHALK_GREEN),
                                CHALK_GREEN), CARD_L, 0.92)
            qb = at(self.q_card("give two names",
                                self.mini_angle("Q", ("A", "B"), CHALK_CYAN),
                                CHALK_CYAN), CARD_R, 0.92)
            qc = at(self.q_card("classify M, N, T",
                                self.mini_angle("Q", ("P", "R"), CHALK_AMBER,
                                                points=(("M", "in"),
                                                        ("N", "on"),
                                                        ("T", "out")),
                                                show_arms=False),
                                CHALK_AMBER), CARD_L, -0.98)
            qd = at(self.ask_card("which name is wrong?",
                                  ["angle AOB", "angle BOA", "angle ABO"],
                                  CHALK_PINK, width=3.00), CARD_R, -0.98)

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
            a1 = at(self.answer_row("A", "vertex O · arms OC and OD",
                                    "the common endpoint and the rays",
                                    CHALK_GREEN), BOARD_CX, 1.62)
            self.play(FadeIn(a1, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b1"))
            a2 = at(self.answer_row("B", "angle AQB = angle BQA",
                                    "vertex Q in the middle", CHALK_CYAN),
                    BOARD_CX, 0.82)
            self.play(FadeIn(a2, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b2"))
            a3 = at(self.answer_row("C", "M interior · N boundary · T exterior",
                                    "between · on an arm · outside",
                                    CHALK_AMBER), BOARD_CX, 0.02)
            self.play(FadeIn(a3, shift=UP * 0.08), run_time=0.50)
            self.add_sound(self.sfx["click"], gain=-15)

            self.wait(leftover(tracker, "b3"))
            a4 = at(self.answer_row("D", "angle ABO is wrong",
                                    "the middle letter must be the vertex",
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

            heading = at(board_text("Build · Name · Locate", 22, CHALK_AMBER,
                                    "BOLD"), BOARD_CX, ROW_Y)

            r1 = at(self.answer_row("1", "TWO RAYS + ONE POINT",
                                    "this is how an angle is formed",
                                    CHALK_GREEN), BOARD_CX, 1.48)
            r2 = at(self.answer_row("2", "VERTEX · ARMS",
                                    "common endpoint · the two rays (sides)",
                                    CHALK_CYAN), BOARD_CX, 0.72)
            r3 = at(self.answer_row("3", "THE VERTEX IN THE MIDDLE",
                                    "angle AOB = angle BOA", CHALK_YELLOW),
                    BOARD_CX, -0.04)
            r4 = at(self.answer_row("4", "INTERIOR · BOUNDARY · EXTERIOR",
                                    "between · on an arm · outside",
                                    CHALK_AMBER), BOARD_CX, -0.80)
            strip = at(board_text("Build the angle, name it, then locate the "
                                  "points.", 16, CHALK_WHITE, "BOLD"),
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
            self.play(FadeIn(r4, shift=UP * 0.06),
                      FadeIn(strip, shift=UP * 0.06), run_time=0.50)
            self.add_sound(self.sfx["success"], gain=-11)

            # The closing strip now goes up with the last recap row, so the whole
            # "...interior, boundary and exterior. Build, name, locate." stretch
            # plays with the finished board in front of the learner; the board is
            # only cleared when the voice actually says "Thank you for watching,".
            self.wait(leftover(tracker, "b4"))

            # "Thank you for watching," -- only now does the recap give way to
            # the thank-you card, so no earlier sentence is cut off.
            self.wait(leftover(tracker, "b5"))
            self.play(FadeOut(heading), FadeOut(r1), FadeOut(r2), FadeOut(r3),
                      FadeOut(r4), FadeOut(strip), run_time=0.55)
            self.play(FadeIn(thanks, shift=UP * 0.10), run_time=0.50)

            self.wait(leftover(tracker, "b6"))
            self.play(FadeIn(bye, shift=UP * 0.10), run_time=0.45)
            self.closing(tracker, thanks, run_time=1.2)
            self._capture_srt(tracker)

        self.wait(END_HOLD)

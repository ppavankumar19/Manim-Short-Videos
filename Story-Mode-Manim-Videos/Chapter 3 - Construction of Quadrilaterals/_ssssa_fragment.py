# ------------------------------------------------- construction furniture ----

from manim import Arc  # noqa: E402  (imported here so the base head stays put)

SCALE = 0.52            # board units per centimetre of the textbook drawing


def circle_intersection(c1, r1, c2, r2, upper=True):
    """Where two circles meet, on the chosen side of the line c1 -> c2.

    This is the mathematics behind "intersect the two arcs": with the four
    side lengths known, the fourth vertex is exactly this point."""
    c1 = np.array(c1, dtype=float)[:2]
    c2 = np.array(c2, dtype=float)[:2]
    d_vec = c2 - c1
    d = float(np.linalg.norm(d_vec))
    if d < 1e-6 or d > r1 + r2 or d < abs(r1 - r2):
        return None
    a = (d * d + r1 * r1 - r2 * r2) / (2.0 * d)
    h = float(np.sqrt(max(r1 * r1 - a * a, 0.0)))
    base = c1 + a * d_vec / d
    perp = np.array([-d_vec[1], d_vec[0]]) / d
    first = base + h * perp
    second = base - h * perp
    pick = first if ((first[1] > second[1]) == upper) else second
    return np.array([pick[0], pick[1], 0.0])


def compass_arc(centre, radius, start_deg, span_deg, color=CHALK_CYAN,
                width=2.6) -> Arc:
    """A compass arc: every point at `radius` from `centre`."""
    return Arc(radius=radius, start_angle=start_deg * DEGREES,
               angle=span_deg * DEGREES, arc_center=np.array(centre, dtype=float),
               color=color, stroke_width=width)


def radius_line(centre, point, color=CHALK_WHITE, label=None, size=15,
                dashed=True) -> VGroup:
    """The compass radius: a line from the centre out to the arc, optionally
    labelled with the radius that is set on the compass."""
    maker = DashedLine if dashed else Line
    kwargs = {"dash_length": 0.1} if dashed else {}
    line = maker(np.array(centre, dtype=float), np.array(point, dtype=float),
                 color=color, stroke_width=1.7, **kwargs)
    if label is None:
        return VGroup(line)
    mid = (np.array(centre, dtype=float) + np.array(point, dtype=float)) / 2.0
    lab = board_text(label, size, color, "BOLD").move_to(mid + UP * 0.24)
    return VGroup(line, lab)


def measure_card(label, color=CHALK_WHITE, size=18) -> VGroup:
    """One given measurement on a small card."""
    tex = MathTex(label, font_size=size, color=color)
    box = RoundedRectangle(corner_radius=0.08, width=tex.width + 0.46,
                           height=tex.height + 0.32, stroke_color=color,
                           stroke_width=1.8, fill_color="#16202B",
                           fill_opacity=0.8)
    tex.move_to(box.get_center())
    grp = VGroup(box, tex)
    grp.tex = tex
    return grp


def check_row(label, color=CHALK_GREEN, size=17) -> VGroup:
    """A verification row: a green tick plus the measurement it confirms."""
    mark = VGroup(
        Line(ORIGIN, np.array([0.09, -0.11, 0.0])),
        Line(np.array([0.09, -0.11, 0.0]), np.array([0.28, 0.17, 0.0])),
    ).set_stroke(color=color, width=4.0)
    txt = MathTex(label, font_size=size, color=CHALK_WHITE)
    return VGroup(mark, txt).arrange(RIGHT, buff=0.22)


def protractor(centre, color=CHALK_AMBER, radius=0.95) -> VGroup:
    """A semicircular protractor with 10-degree ticks: it is laid over the
    vertex while the given angle is set out, then taken away again."""
    body = Arc(radius=radius, start_angle=0.0, angle=180 * DEGREES,
               arc_center=np.array(centre, dtype=float), color=color,
               stroke_width=1.6, stroke_opacity=0.7)
    ticks = VGroup()
    for deg in range(0, 181, 10):
        a = deg * DEGREES
        direction = np.array([np.cos(a), np.sin(a), 0.0])
        outer = np.array(centre, dtype=float) + radius * direction
        inner = np.array(centre, dtype=float) + radius * 0.90 * direction
        ticks.add(Line(inner, outer, color=color, stroke_width=1.2,
                       stroke_opacity=0.65))
    return VGroup(body, ticks)


def example_frame(origin=None, scale=SCALE):
    """Textbook Example 1, built exactly as the construction does it.

    P Q = 4.5 cm and Q R = 5.2 cm with angle R Q P = 120 degrees fix triangle
    P Q R; S is then the intersection of the 4 cm arc about P and the 5.5 cm
    arc about R."""
    if origin is None:
        origin = np.array([BOARD_CX - 0.6, -0.6, 0.0])
    P = np.array(origin, dtype=float)
    Q = P + np.array([4.5 * scale, 0.0, 0.0])
    ang = 120 * DEGREES
    R = Q + 5.2 * scale * np.array([np.cos(ang), np.sin(ang), 0.0])
    S = circle_intersection(P, 4.0 * scale, R, 5.5 * scale, upper=True)
    return P, Q, R, S


def exercise_frame(origin=None, scale=SCALE):
    """Exercise 3.1(a): A B = 5.5, B C = 3.5, C D = 4, A D = 5, angle A = 45."""
    if origin is None:
        origin = np.array([BOARD_CX - 0.4, -0.5, 0.0])
    A = np.array(origin, dtype=float)
    B = A + np.array([5.5 * scale, 0.0, 0.0])
    a = 45 * DEGREES
    D = A + 5.0 * scale * np.array([np.cos(a), np.sin(a), 0.0])
    C = circle_intersection(B, 3.5 * scale, D, 4.0 * scale, upper=True)
    return A, B, C, D


def vertex_label(letter, point, side="DL", color=CHALK_WHITE,
                 size=18) -> Text:
    """A vertex letter placed clear of its corner."""
    corner = {"DL": DL, "DR": DR, "UR": UR, "UL": UL}[side]
    return board_text(letter, size, color, "BOLD").next_to(
        np.array(point, dtype=float), corner, buff=0.10)


def quad_names(points, letters="PQRS", size=18, color=CHALK_WHITE) -> VGroup:
    """The four vertex letters, each outside its own corner."""
    sides = ("DL", "DR", "UR", "UL")
    return VGroup(*[vertex_label(letter, point, side, color, size)
                    for letter, point, side in zip(letters, points, sides)])


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "How do we construct a quadrilateral when we are given four sides and "
        "one angle?<bookmark mark='b0'/> We will build it in four clear steps, "
        "and we will see exactly why each one works.<bookmark mark='b1'/>"
    ),
    "scene1": (
        "Here is our problem.<bookmark mark='b0'/> We are given five "
        "measurements. P Q is four point five centimetres. Q R is five point "
        "two centimetres. R S is five point five centimetres. P S is four "
        "centimetres. And angle R Q P is one hundred and twenty degrees."
        "<bookmark mark='b1'/> Four sides and one angle: that is the S S S S A "
        "combination.<bookmark mark='b2'/> So where should we start?"
        "<bookmark mark='b3'/>"
    ),
    "scene2": (
        "We start with a rough sketch.<bookmark mark='b0'/> Draw the "
        "quadrilateral P Q R S, going round in order, and mark every "
        "measurement on it.<bookmark mark='b1'/> This sketch is not to scale. "
        "It is only here to show us which measurements belong together."
        "<bookmark mark='b2'/> Look closely at the angle: it sits at Q, "
        "between Q P and Q R.<bookmark mark='b3'/>"
    ),
    "scene3": (
        "Now we look for a triangle that we can build straight away."
        "<bookmark mark='b0'/> We know P Q, we know Q R, and we know the angle "
        "between them.<bookmark mark='b1'/> Two sides and the included angle: "
        "that is side, angle, side.<bookmark mark='b2'/> So triangle P Q R is "
        "the one to construct first.<bookmark mark='b3'/>"
    ),
    "scene4": (
        "Let us construct it accurately.<bookmark mark='b0'/> Draw P Q, four "
        "point five centimetres long, and label the ends P and Q."
        "<bookmark mark='b1'/> At Q, set out the angle of one hundred and "
        "twenty degrees from Q P.<bookmark mark='b2'/> R must lie somewhere "
        "along that ray. The angle fixes its direction, but not yet its "
        "distance.<bookmark mark='b3'/>"
    ),
    "scene5": (
        "So we set the compass to five point two centimetres.<bookmark "
        "mark='b0'/> With the compass point at Q, we draw an arc that cuts the "
        "ray.<bookmark mark='b1'/> Where the arc cuts the ray, that is R."
        "<bookmark mark='b2'/> Triangle P Q R is now completely fixed."
        "<bookmark mark='b3'/>"
    ),
    "scene6": (
        "Only one vertex is left: S.<bookmark mark='b0'/> We know P S is four "
        "centimetres, so S must lie on the arc of radius four about P."
        "<bookmark mark='b1'/> We also know R S is five point five "
        "centimetres, so S must lie on the arc of radius five point five about "
        "R.<bookmark mark='b2'/> Those two arcs meet at exactly one point on "
        "this side, and that point satisfies both distances.<bookmark "
        "mark='b3'/> There is S.<bookmark mark='b4'/>"
    ),
    "scene7": (
        "Now we finish the figure.<bookmark mark='b0'/> Join P to S, and join S "
        "to R.<bookmark mark='b1'/> Those two sides complete the quadrilateral "
        "P Q R S.<bookmark mark='b2'/> Let us check every measurement: P Q is "
        "four point five, Q R is five point two, R S is five point five, P S is "
        "four, and angle R Q P is one hundred and twenty degrees. All five are "
        "used.<bookmark mark='b3'/>"
    ),
    "scene8": (
        "This is the method, and it works for every problem of this kind."
        "<bookmark mark='b0'/> First sketch the figure and mark what is given. "
        "Then build the first triangle from two sides and the included angle. "
        "Then use the two remaining lengths as radii, and intersect those arcs. "
        "Finally join the last sides, and verify.<bookmark mark='b1'/> Sketch, "
        "triangle, arcs, join.<bookmark mark='b2'/>"
    ),
    "scene9_setup": (
        "Your turn.<bookmark mark='b0'/> In quadrilateral A B C D, A B is five "
        "point five centimetres, B C is three point five centimetres, C D is "
        "four centimetres, A D is five centimetres, and angle A is forty five "
        "degrees.<bookmark mark='b1'/> Which triangle should you construct "
        "first?<bookmark mark='b2'/> Pause the video and decide.<bookmark "
        "mark='b3'/>"
    ),
    "scene9_reveal": (
        "Let us check.<bookmark mark='b0'/> The angle is at A, between A B and "
        "A D, and we know both of those sides.<bookmark mark='b1'/> So triangle "
        "B A D comes first, from A B, A D and the angle of forty five degrees."
        "<bookmark mark='b2'/> Then C is found by two arcs: radius three point "
        "five about B, and radius four about D. Where they cross is C, and the "
        "quadrilateral A B C D is complete.<bookmark mark='b3'/>"
    ),
    "scene10": (
        "Let us put the method together.<bookmark mark='b0'/> Three "
        "measurements build the triangle: two sides and the included angle."
        "<bookmark mark='b1'/> Two more measurements locate the fourth vertex, "
        "as the intersection of two arcs.<bookmark mark='b2'/> Sketch, "
        "triangle, arcs, join, verify. That is the S S S S A method."
        "<bookmark mark='b3'/> Thank you for watching!<bookmark mark='b4'/> See "
        "you in the next lesson!<bookmark mark='b5'/>"
    ),
}

# @@PLUMBING@@

    def construct(self):
        self.sfx = load_sfx()
        self.set_speech_service(get_speech_service(), create_subcaption=False)
        install_synced_voiceover(self)

        self.add_background()

        self.beat0_title()
        self.beat1_data()
        self.beat2_sketch()
        self.beat3_choose()
        self.beat4_side_angle()
        self.beat5_triangle()
        self.beat6_locate_s()
        self.beat7_complete()
        self.beat8_method()
        self.beat9_challenge()
        self.beat10_recap()

        self._write_real_srt()

    # ================================================================ beats ==

    def beat0_title(self) -> None:
        with self.voiceover(text=NARRATION["title"]) as tracker:
            self.reset_board()

            title = board_text("Construct PQRS", 34, CHALK_WHITE, "BOLD"
                               ).move_to(np.array([BOARD_CX, BOARD_CY + 1.85, 0]))
            sub = board_text("Four Sides + One Angle  (S.S.S.S.A)", 22,
                             CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX, BOARD_CY + 0.95, 0]))
            self.play(FadeIn(title, shift=UP * 0.1), run_time=quick(
                tracker.time_until_bookmark("b0") * 0.5))
            self.play(FadeIn(sub, shift=UP * 0.1), run_time=quick(
                tracker.time_until_bookmark("b0") * 0.5))
            self.play(Indicate(sub, color=CHALK_YELLOW, scale_factor=1.04),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["ding"], gain=-13)

            P, Q, R, S = example_frame(origin=np.array([BOARD_CX - 0.7, -1.25, 0]),
                                       scale=0.34)
            outline = Polygon(P, Q, R, S, color=CHALK_CYAN, stroke_width=2.6,
                              fill_color=CHALK_CYAN, fill_opacity=0.10)
            names = VGroup(*[vertex_label(t, p, s, CHALK_WHITE, 15)
                             for t, p, s in zip("PQRS", (P, Q, R, S),
                                                ("DL", "DR", "UR", "UL"))])
            tag = board_text("Steps: sketch, triangle, arcs, join", 18,
                             CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.45, 0]))
            self.play(FadeIn(outline), FadeIn(names), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.5))
            self.play(FadeIn(tag, shift=UP * 0.1),
                      Flash(outline, color=CHALK_CYAN, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 1: the five given measurements --------------------------------
    def beat1_data(self) -> None:
        with self.voiceover(text=NARRATION["scene1"]) as tracker:
            self.reset_board()

            heading = board_text("Four Sides + One Angle", 24, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            cards = VGroup(
                measure_card(r"PQ=4.5", CHALK_CYAN),
                measure_card(r"QR=5.2", CHALK_CYAN),
                measure_card(r"RS=5.5", CHALK_CYAN),
                measure_card(r"PS=4", CHALK_CYAN),
                measure_card(r"\angle RQP=120^\circ", CHALK_YELLOW),
            ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX, 0.15, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=quick(
                tracker.time_until_bookmark("b0") * 0.6))
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.12)
                                    for c in cards[:4]], lag_ratio=0.25),
                      run_time=rt(tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(FadeIn(cards[4], shift=RIGHT * 0.12),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.play(Indicate(cards[4], color=CHALK_YELLOW, scale_factor=1.08),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.add_sound(self.sfx["ding"], gain=-13)

            ssssa = board_text("Side + Side + Side + Side + Angle", 20,
                               CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX + 2.9, -1.5, 0]))
            box = SurroundingRectangle(ssssa, color=CHALK_GREEN, buff=0.16,
                                       corner_radius=0.1, stroke_width=2.6)
            self.play(FadeIn(ssssa, shift=UP * 0.1), Create(box),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            ask = board_text("Where should we start?", 20, CHALK_WHITE, "BOLD"
                             ).move_to(np.array([BOARD_CX + 2.9, -2.15, 0]))
            self.play(FadeIn(ask, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 2: the rough sketch -------------------------------------------
    def beat2_sketch(self) -> None:
        with self.voiceover(text=NARRATION["scene2"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 1 — Rough Sketch", 22, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            # the rough sketch is deliberately *not* to scale: a free shape
            rough = Polygon(np.array([-1.5, -0.7, 0]), np.array([1.9, -0.9, 0]),
                            np.array([2.4, 1.3, 0]), np.array([-1.9, 1.5, 0]),
                            color=CHALK_WHITE, stroke_width=2.6,
                            fill_color=CHALK_WHITE, fill_opacity=0.05)
            rough.corners = (np.array([-1.5, -0.7, 0]), np.array([1.9, -0.9, 0]),
                             np.array([2.4, 1.3, 0]), np.array([-1.9, 1.5, 0]))
            centre = rough.get_center()
            names = quad_names(rough.corners, "PQRS", 18)
            lab_pq = side_label(rough.corners[0], rough.corners[1], centre,
                                "4.5", CHALK_CYAN, 16, 0.18)
            lab_qr = side_label(rough.corners[1], rough.corners[2], centre,
                                "5.2", CHALK_CYAN, 16, 0.18)
            lab_rs = side_label(rough.corners[2], rough.corners[3], centre,
                                "5.5", CHALK_CYAN, 16, 0.18)
            lab_ps = side_label(rough.corners[3], rough.corners[0], centre,
                                "4", CHALK_CYAN, 16, 0.18)
            q_arc = angle_mark(rough.corners[1], rough.corners[0],
                               rough.corners[2], radius=0.42,
                               color=CHALK_YELLOW, label="120°")
            note = board_text("Not to scale", 17, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.0, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=quick(
                tracker.time_until_bookmark("b0") * 0.5))
            self.play(Create(rough), FadeIn(names), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.5))
            self.play(FadeIn(note), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(FadeIn(lab_pq), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.5))
            self.play(FadeIn(lab_qr), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.5))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(lab_rs), FadeIn(lab_ps), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(Create(q_arc.arc), FadeIn(q_arc.label),
                      Indicate(names[1], color=CHALK_YELLOW, scale_factor=1.5),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 3: which three measurements come first ------------------------
    def beat3_choose(self) -> None:
        with self.voiceover(text=NARRATION["scene3"]) as tracker:
            self.reset_board()

            heading = board_text("Use 3 of the 5 Measurements First", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            P, Q, R, S = example_frame()
            full = Polygon(P, Q, R, S, color=CHALK_WHITE, stroke_width=2.2,
                           fill_opacity=0.0)
            full.set_stroke(opacity=0.30)
            names = quad_names((P, Q, R, S), "PQRS", 18)
            tri = Polygon(P, Q, R, color=CHALK_CYAN, stroke_width=3.2,
                          fill_color=CHALK_CYAN, fill_opacity=0.16)
            tri_pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=4.0)
            tri_qr = Line(Q, R, color=CHALK_YELLOW, stroke_width=4.0)
            lab_pq = board_text("PQ = 4.5", 16, CHALK_YELLOW, "BOLD").move_to(
                (P + Q) / 2 + DOWN * 0.32)
            lab_qr = board_text("QR = 5.2", 16, CHALK_YELLOW, "BOLD").move_to(
                (Q + R) / 2 + np.array([0.62, 0.06, 0]))
            q_arc = angle_mark(Q, P, R, radius=0.5, color=CHALK_PINK,
                               label="120°")
            sas = measure_card(r"\text{Side}+\text{Angle}+\text{Side}",
                               CHALK_GREEN, 17).move_to(
                np.array([BOARD_CX + 2.9, 1.4, 0]))
            sas2 = measure_card(r"\text{S.A.S}", CHALK_GREEN, 17).move_to(
                np.array([BOARD_CX + 2.9, 0.7, 0]))
            note = board_text("Three measurements fix this triangle.", 18,
                              CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX + 2.9, -1.6, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), FadeIn(full),
                      FadeIn(names), run_time=quick(
                          tracker.time_until_bookmark("b0") * 0.5))
            self.play(Create(tri_pq), FadeIn(lab_pq), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(Create(tri_qr), FadeIn(lab_qr), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.5))
            self.play(FadeIn(tri), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.5))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(Create(q_arc.arc), FadeIn(q_arc.label), run_time=rt(
                tracker.time_until_bookmark("b2") * 0.5))
            self.play(FadeIn(sas, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b2") * 0.5))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(sas2, shift=UP * 0.1), FadeIn(note),
                      Flash(tri, color=CHALK_CYAN, flash_radius=0.8),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 4: draw PQ and set out the angle ------------------------------
    def beat4_side_angle(self) -> None:
        with self.voiceover(text=NARRATION["scene4"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 2 — PQ and the 120° Angle", 22,
                                 CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            P, Q, R, S = example_frame()
            base = Line(P, Q, color=CHALK_WHITE, stroke_width=4.5)
            names = VGroup(vertex_label("P", P, "DL"), vertex_label("Q", Q, "DR"))
            lab_pq = board_text("PQ = 4.5 cm", 17, CHALK_CYAN, "BOLD").move_to(
                (P + Q) / 2 + DOWN * 0.30)
            ray = DashedLine(Q, R + 0.55 * (R - Q),
                             color=CHALK_YELLOW, stroke_width=2.0,
                             dash_length=0.14)
            prot = protractor(Q, radius=1.05)
            q_arc = angle_mark(Q, P, R, radius=0.52, color=CHALK_PINK,
                               label="120°")
            note = board_text("R must lie somewhere on this ray.", 19,
                              CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX + 2.4, -1.7, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=quick(
                tracker.time_until_bookmark("b0") * 0.5))
            self.play(Create(base), FadeIn(names), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.5))
            self.play(FadeIn(lab_pq), run_time=rt(
                tracker.time_until_bookmark("b0")))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(FadeIn(prot, scale=0.9), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.5))
            self.play(Create(ray), FadeOut(prot), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.5))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(Create(q_arc.arc), FadeIn(q_arc.label),
                      Indicate(q_arc.arc, color=CHALK_PINK, scale_factor=1.06),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(note, shift=UP * 0.1),
                      Indicate(ray, color=CHALK_YELLOW, scale_factor=1.0),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 5: the compass arc that fixes R -------------------------------
    def beat5_triangle(self) -> None:
        with self.voiceover(text=NARRATION["scene5"]) as tracker:
            self.reset_board()

            heading = board_text("Triangle PQR is Fixed", 22, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            P, Q, R, S = example_frame()
            base = Line(P, Q, color=CHALK_WHITE, stroke_width=4.5)
            ray = DashedLine(Q, R + 0.5 * (R - Q), color=CHALK_YELLOW,
                             stroke_width=1.8, dash_length=0.14)
            names = VGroup(vertex_label("P", P, "DL"), vertex_label("Q", Q, "DR"))
            lab_pq = board_text("PQ = 4.5 cm", 16, CHALK_CYAN, "BOLD").move_to(
                (P + Q) / 2 + DOWN * 0.30)
            arc = compass_arc(Q, 5.2 * SCALE, 100, 45, CHALK_GREEN)
            rad = radius_line(Q, Q + 5.2 * SCALE * np.array(
                [np.cos(108 * DEGREES), np.sin(108 * DEGREES), 0.0]),
                CHALK_GREEN, "5.2 cm")
            r_dot = Dot(radius=0.085, color=CHALK_YELLOW).move_to(R)
            r_name = vertex_label("R", R, "UR", CHALK_WHITE)
            tri = Polygon(P, Q, R, color=CHALK_CYAN, stroke_width=2.4,
                          fill_color=CHALK_CYAN, fill_opacity=0.12)
            lab_qr = board_text("QR = 5.2 cm", 16, CHALK_GREEN, "BOLD").move_to(
                (Q + R) / 2 + np.array([0.6, 0.1, 0]))
            note = board_text("Three measurements used. Two still left: "
                              "PS = 4, RS = 5.5.", 18, CHALK_WHITE, "BOLD"
                              ).move_to(np.array([BOARD_CX, -2.1, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), Create(base),
                      FadeIn(names), FadeIn(ray), FadeIn(lab_pq),
                      run_time=quick(tracker.time_until_bookmark("b0") * 0.5))
            self.play(FadeIn(rad), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.5))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(Create(arc), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(FadeIn(r_dot, scale=0.5), FadeIn(r_name),
                      Indicate(r_dot, color=CHALK_YELLOW, scale_factor=1.8),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            self.play(FadeIn(tri), FadeIn(lab_qr), FadeOut(rad), FadeOut(ray),
                      run_time=rt(tracker.time_until_bookmark("b2") * 0.5))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(note, shift=UP * 0.1),
                      Flash(tri, color=CHALK_CYAN, flash_radius=0.7),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 6: two arcs locate S ------------------------------------------
    def beat6_locate_s(self) -> None:
        with self.voiceover(text=NARRATION["scene6"]) as tracker:
            self.reset_board()

            heading = board_text("STEP 3 — Locate S", 22, CHALK_AMBER, "BOLD"
                                 ).move_to(np.array([BOARD_CX, 2.72, 0]))
            P, Q, R, S = example_frame()
            tri = Polygon(P, Q, R, color=CHALK_CYAN, stroke_width=2.4,
                          fill_color=CHALK_CYAN, fill_opacity=0.12)
            names = quad_names((P, Q, R, S), "PQRS", 17)
            tri_names = VGroup(*[names[i] for i in (0, 1, 2)])
            arc_p = compass_arc(P, 4.0 * SCALE, 25, 75, CHALK_PINK)
            arc_r = compass_arc(R, 5.5 * SCALE, 150, 80, CHALK_GREEN)
            rad_p = radius_line(P, S, CHALK_PINK, "PS = 4 cm")
            rad_r = radius_line(R, S, CHALK_GREEN, "RS = 5.5 cm")
            s_dot = Dot(radius=0.09, color=CHALK_YELLOW).move_to(S)
            s_name = vertex_label("S", S, "UL", CHALK_WHITE)
            guide1 = DashedLine(P, S, color=CHALK_WHITE, stroke_width=1.8,
                                dash_length=0.12)
            guide2 = DashedLine(R, S, color=CHALK_WHITE, stroke_width=1.8,
                                dash_length=0.12)
            note = board_text("S satisfies both distances.", 19, CHALK_GREEN,
                              "BOLD").move_to(np.array([BOARD_CX, -2.2, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), FadeIn(tri),
                      FadeIn(tri_names), run_time=quick(
                          tracker.time_until_bookmark("b0") * 0.6))
            self.play(FadeIn(rad_p), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(Create(arc_p), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(FadeIn(rad_r), Create(arc_r), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(FadeIn(s_dot, scale=0.5), FadeIn(s_name),
                      Indicate(s_dot, color=CHALK_YELLOW, scale_factor=2.0),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            self.play(Create(guide1), Create(guide2), FadeOut(rad_p),
                      FadeOut(rad_r), run_time=rt(
                          tracker.time_until_bookmark("b3") * 0.5))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(note, shift=UP * 0.1),
                      Flash(s_dot, color=CHALK_GREEN, flash_radius=0.6),
                      run_time=rt(tracker.time_until_bookmark("b4")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 7: join the last two sides and verify -------------------------
    def beat7_complete(self) -> None:
        with self.voiceover(text=NARRATION["scene7"]) as tracker:
            self.reset_board()

            heading = board_text("Required Quadrilateral PQRS", 22, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            P, Q, R, S = example_frame()
            qp = Line(P, Q, color=CHALK_WHITE, stroke_width=4.0)
            qr = Line(Q, R, color=CHALK_WHITE, stroke_width=4.0)
            ps = Line(P, S, color=CHALK_GREEN, stroke_width=4.0)
            sr = Line(S, R, color=CHALK_GREEN, stroke_width=4.0)
            quad = Polygon(P, Q, R, S, color=CHALK_CYAN, stroke_width=2.2,
                           fill_color=CHALK_CYAN, fill_opacity=0.10)
            names = quad_names((P, Q, R, S), "PQRS", 17)
            checks = VGroup(
                check_row(r"PQ=4.5", CHALK_GREEN, 15),
                check_row(r"QR=5.2", CHALK_GREEN, 15),
                check_row(r"RS=5.5", CHALK_GREEN, 15),
                check_row(r"PS=4", CHALK_GREEN, 15),
                check_row(r"\angle RQP=120^\circ", CHALK_YELLOW, 15),
            ).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX + 3.0, 0.0, 0]))
            title = board_text("All five measurements used.", 19, CHALK_GREEN,
                               "BOLD").move_to(np.array([BOARD_CX, -2.35, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), Create(qp), Create(qr),
                      FadeIn(names), run_time=quick(
                          tracker.time_until_bookmark("b0") * 0.6))
            self.play(Create(ps), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.4))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(Create(sr), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.5))
            self.play(FadeIn(quad), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.5))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(title, shift=UP * 0.1),
                      Flash(quad, color=CHALK_CYAN, flash_radius=0.8),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1)
                                    for c in checks], lag_ratio=0.3),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 8: the reusable method ----------------------------------------
    def beat8_method(self) -> None:
        with self.voiceover(text=NARRATION["scene8"]) as tracker:
            self.reset_board()

            heading = board_text("The S.S.S.S.A Method", 23, CHALK_AMBER,
                                 "BOLD").move_to(np.array([BOARD_CX, 2.72, 0]))
            steps = VGroup(
                combo_card("1. SKETCH", "mark all 5 measurements", CHALK_CYAN),
                combo_card("2. TRIANGLE", "2 sides + included angle",
                           CHALK_GREEN),
                combo_card("3. TWO ARCS", "remaining lengths as radii",
                           CHALK_PINK),
                combo_card("4. JOIN", "complete and verify", CHALK_YELLOW),
            ).arrange(DOWN, buff=0.20, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX - 2.35, 0.35, 0]))
            P, Q, R, S = example_frame(origin=np.array([BOARD_CX + 2.2, 0.55, 0]),
                                       scale=0.30)
            mini = VGroup(
                Polygon(P, Q, R, S, color=CHALK_WHITE, stroke_width=2.0,
                        fill_opacity=0.0),
                Line(P, Q, color=CHALK_YELLOW, stroke_width=3.0),
                Line(Q, R, color=CHALK_YELLOW, stroke_width=3.0),
                compass_arc(P, 4.0 * 0.30, 25, 75, CHALK_PINK, 2.0),
                compass_arc(R, 5.5 * 0.30, 150, 80, CHALK_GREEN, 2.0),
                Dot(radius=0.07, color=CHALK_YELLOW).move_to(S),
            )
            names = quad_names((P, Q, R, S), "PQRS", 14)
            note = board_text("Sketch → Triangle → Arcs → Join → Verify", 18,
                              CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.35, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=quick(
                tracker.time_until_bookmark("b0") * 0.5))
            self.play(FadeIn(steps), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.5))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(FadeIn(mini[0]), FadeIn(names), FadeIn(mini[1]),
                      FadeIn(mini[2]), run_time=rt(
                          tracker.time_until_bookmark("b1") * 0.4))
            self.play(Create(mini[3]), Create(mini[4]), FadeIn(mini[5]),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.6))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(note, shift=UP * 0.1),
                      Circumscribe(steps[0], color=CHALK_CYAN, stroke_width=2.4,
                                   time_width=0.6),
                      run_time=rt(tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 9: student challenge ------------------------------------------
    def beat9_challenge(self) -> None:
        with self.voiceover(text=NARRATION["scene9_setup"]) as tracker:
            self.reset_board()

            heading = board_text("YOUR TURN", 30, CHALK_PINK, "BOLD").move_to(
                np.array([BOARD_CX, 2.62, 0]))
            A, B, C, D = exercise_frame(origin=np.array([BOARD_CX - 2.6, -0.35, 0]),
                                       scale=0.40)
            rough = Polygon(A, B, C, D, color=CHALK_WHITE, stroke_width=2.4,
                            fill_color=CHALK_WHITE, fill_opacity=0.06)
            names = quad_names((A, B, C, D), "ABCD", 16)
            a_arc = angle_mark(A, B, D, radius=0.36, color=CHALK_YELLOW,
                               label="45°")
            cards = VGroup(
                measure_card(r"AB=5.5", CHALK_CYAN, 15),
                measure_card(r"BC=3.5", CHALK_CYAN, 15),
                measure_card(r"CD=4", CHALK_CYAN, 15),
                measure_card(r"AD=5", CHALK_CYAN, 15),
                measure_card(r"\angle A=45^\circ", CHALK_YELLOW, 15),
            ).arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX + 2.5, 0.55, 0]))
            ask = board_text("Which triangle comes first?", 18, CHALK_WHITE,
                             "BOLD").move_to(np.array([BOARD_CX - 2.4, -2.0, 0]))
            pause = board_text("Pause and decide.", 18, CHALK_YELLOW, "BOLD"
                               ).move_to(np.array([BOARD_CX + 2.5, -1.9, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), FadeIn(rough),
                      FadeIn(names), run_time=quick(
                          tracker.time_until_bookmark("b0") * 0.6))
            self.play(Create(a_arc.arc), FadeIn(a_arc.label),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.4))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(FadeIn(cards), run_time=rt(
                tracker.time_until_bookmark("b1")))
            self.add_sound(self.sfx["click"], gain=-15)

            self.play(FadeIn(ask, shift=RIGHT * 0.12), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeIn(pause, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b3")))

            self.challenge = {"rough": rough, "names": names, "cards": cards,
                              "ask": ask, "pause": pause, "a_arc": a_arc,
                              "points": (A, B, C, D)}
            self._capture_srt(tracker)

        play_challenge_countdown(self, seconds=4, sfx=self.sfx,
                                 position=np.array([BOARD_CX, 0.55, 0]))

        with self.voiceover(text=NARRATION["scene9_reveal"]) as tracker:
            ch = self.challenge
            A, B, C, D = ch["points"]
            rough, names = ch["rough"], ch["names"]

            self.play(FadeOut(ch["pause"]), run_time=rt(
                tracker.time_until_bookmark("b0") * 0.5))
            tri_bad = Polygon(B, A, D, color=CHALK_GREEN, stroke_width=3.0,
                              fill_color=CHALK_GREEN, fill_opacity=0.14)
            lab_ab = board_text("AB = 5.5", 15, CHALK_GREEN, "BOLD").move_to(
                (A + B) / 2 + DOWN * 0.28)
            lab_ad = board_text("AD = 5", 15, CHALK_GREEN, "BOLD").move_to(
                (A + D) / 2 + np.array([0.5, 0.05, 0]))
            self.play(Create(tri_bad),
                      Indicate(ch["a_arc"].arc, color=CHALK_YELLOW,
                               scale_factor=1.08),
                      run_time=rt(tracker.time_until_bookmark("b1") * 0.5))
            self.play(FadeIn(lab_ab), FadeIn(lab_ad), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.5))
            self.add_sound(self.sfx["click"], gain=-15)

            badge = board_text("First triangle: BAD", 18, CHALK_GREEN, "BOLD"
                               ).move_to(np.array([BOARD_CX + 2.5, -0.6, 0]))
            self.play(FadeIn(badge, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["ding"], gain=-13)

            arc_b = compass_arc(B, 3.5 * 0.40, 40, 80, CHALK_PINK)
            arc_d = compass_arc(D, 4.0 * 0.40, 300, 70, CHALK_CYAN)
            c_dot = Dot(radius=0.08, color=CHALK_YELLOW).move_to(C)
            c_name = vertex_label("C", C, "UR", CHALK_WHITE)
            quad = Polygon(A, B, C, D, color=CHALK_CYAN, stroke_width=2.4,
                           fill_color=CHALK_CYAN, fill_opacity=0.12)
            self.play(Create(arc_b), Create(arc_d), run_time=rt(
                tracker.time_until_bookmark("b3") * 0.5))
            self.play(FadeIn(c_dot, scale=0.5), FadeIn(c_name), FadeIn(quad),
                      Indicate(c_dot, color=CHALK_YELLOW, scale_factor=2.0),
                      run_time=rt(tracker.time_until_bookmark("b3") * 0.5))
            self.add_sound(self.sfx["success"], gain=-11)
            self._capture_srt(tracker)

        self.wait(TRANSITION_HOLD)

    # -- Scene 10: recap ------------------------------------------------------
    def beat10_recap(self) -> None:
        with self.voiceover(text=NARRATION["scene10"]) as tracker:
            self.reset_board()

            heading = board_text("S.S.S.S.A", 26, CHALK_AMBER, "BOLD").move_to(
                np.array([BOARD_CX, 2.72, 0]))
            P, Q, R, S = example_frame(origin=np.array([BOARD_CX - 1.6, 0.5, 0]),
                                       scale=0.46)
            tri = Polygon(P, Q, R, color=CHALK_YELLOW, stroke_width=3.4,
                          fill_color=CHALK_YELLOW, fill_opacity=0.16)
            quad = Polygon(P, Q, R, S, color=CHALK_CYAN, stroke_width=2.4,
                           fill_color=CHALK_CYAN, fill_opacity=0.10)
            names = quad_names((P, Q, R, S), "PQRS", 17)
            arc_p = compass_arc(P, 4.0 * 0.46, 25, 75, CHALK_PINK)
            arc_r = compass_arc(R, 5.5 * 0.46, 150, 80, CHALK_GREEN)
            s_dot = Dot(radius=0.09, color=CHALK_YELLOW).move_to(S)

            rows = VGroup(
                summary_row(1, "Two sides + included angle:",
                            r"\triangle PQR", CHALK_YELLOW),
                summary_row(2, "Remaining two sides as radii:",
                            r"PS,\ RS", CHALK_PINK),
                summary_row(3, "Intersection gives the fourth vertex:",
                            r"S", CHALK_GREEN),
            ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(
                np.array([BOARD_CX + 1.9, 1.35, 0]))
            final = board_text("3 measurements build the triangle, "
                               "2 more locate the fourth vertex.", 19,
                               CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -1.75, 0]))
            small = board_text("Sketch → Triangle → Arcs → Join → Verify", 17,
                               CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.3, 0]))

            self.play(FadeIn(heading, shift=UP * 0.08), run_time=quick(
                tracker.time_until_bookmark("b0") * 0.4))
            self.play(FadeIn(quad), FadeIn(names), Create(tri),
                      run_time=rt(tracker.time_until_bookmark("b0") * 0.6))
            self.add_sound(self.sfx["pop"], gain=-13)

            self.play(FadeIn(rows[0], shift=RIGHT * 0.12), run_time=rt(
                tracker.time_until_bookmark("b1") * 0.5))
            self.play(Create(arc_p), Create(arc_r), FadeIn(s_dot),
                      FadeIn(rows[1], shift=RIGHT * 0.12), run_time=rt(
                          tracker.time_until_bookmark("b1") * 0.5))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(Indicate(s_dot, color=CHALK_YELLOW, scale_factor=2.0),
                      FadeIn(rows[2], shift=RIGHT * 0.12), run_time=rt(
                          tracker.time_until_bookmark("b2")))
            self.add_sound(self.sfx["success"], gain=-11)

            self.play(FadeIn(final, shift=UP * 0.1),
                      FadeIn(small),
                      Circumscribe(quad, color=CHALK_AMBER, stroke_width=3,
                                   time_width=0.5),
                      run_time=rt(tracker.time_until_bookmark("b3")))
            self.add_sound(self.sfx["ding"], gain=-13)

            summary = VGroup(quad, names, tri, arc_p, arc_r, s_dot, rows,
                             final, small)
            thanks = board_text("Thank You for Watching!", 40, CHALK_WHITE,
                                "BOLD")
            thanks2 = board_text("See you in the next lesson :)", 25, CHALK_CYAN)
            thanks_group = VGroup(thanks, thanks2).arrange(
                DOWN, buff=0.3).move_to(np.array([BOARD_CX, BOARD_CY, 0]))
            self.play(FadeOut(summary), FadeOut(heading), run_time=rt(
                tracker.time_until_bookmark("b4") * 0.35))
            self.play(FadeIn(thanks, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b4") * 0.65))
            self.add_sound(self.sfx["success"], gain=-11)
            self.play(FadeIn(thanks2, shift=UP * 0.1), run_time=rt(
                tracker.time_until_bookmark("b5")))
            self.play(Circumscribe(thanks_group, color=CHALK_AMBER,
                                   stroke_width=3, time_width=0.5),
                      run_time=0.25)
            self.play(Indicate(thanks, color=CHALK_WHITE, scale_factor=1.01),
                      run_time=rt(tracker.get_remaining_duration()))
            self._capture_srt(tracker)

        self.wait(END_HOLD)


if __name__ == "__main__":
    pass

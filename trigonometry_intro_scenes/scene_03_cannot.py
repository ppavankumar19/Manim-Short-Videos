from common import *

GY = -2.35


class Scene03Cannot(VoiceoverScene):
    """Three things a measuring tape simply cannot reach."""

    def construct(self):
        self.set_speech_service(scene_speech_service("cannot"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(lesson_backdrop())

        ground = Line(np.array([-FRAME_W / 2, GY, 0.0]),
                      np.array([FRAME_W / 2, GY, 0.0]),
                      stroke_color=GROUND_HI, stroke_width=4)
        head = heading("Can you measure these?", AMBER, 40).to_edge(UP, buff=0.45)

        # 1 — a tree you cannot climb
        big_tree = tree(np.array([-4.55, GY, 0.0]), 3.0, 1.05)
        # the crown reaches GY+3.32, so the label sits well clear above it
        t_q = chip(mtx(r"h = \;?", 34, AMBER)
                   .move_to(np.array([-4.55, GY + 4.15, 0.0])))
        t_no = txt("cannot climb", 24, ROSE).move_to(np.array([-4.55, GY - 0.55, 0.0]))

        # 2 — a river you cannot swim
        water = river(np.array([0.0, GY - 0.35, 0.0]), 4.2, 1.35)
        r_q = chip(mtx(r"w = \;?", 34, AMBER)
                   .move_to(np.array([0.0, GY + 0.85, 0.0])))
        r_no = txt("cannot swim", 24, ROSE).move_to(np.array([0.0, GY - 1.45, 0.0]))

        # 3 — a ship you cannot walk to
        sea = Rectangle(width=4.6, height=1.1, fill_color="#12304A",
                        fill_opacity=1, stroke_width=0)
        sea.move_to(np.array([4.6, GY - 0.55, 0.0]))
        ship = boat(np.array([4.6, GY - 0.02, 0.0]), 1.15)
        s_q = chip(mtx(r"d = \;?", 34, AMBER)
                   .move_to(np.array([4.6, GY + 0.95, 0.0])))
        s_no = txt("cannot walk there", 24, ROSE).move_to(
            np.array([4.6, GY - 1.45, 0.0]))

        # the tape that gives up
        tape = tape_measure(np.array([-2.2, 0.55, 0.0]), np.array([0.9, 1.35, 0.0]))
        tape_x = cross_mark(np.array([1.5, 1.60, 0.0]), 0.32)
        useless = heading("a tape is no use here", ROSE, 38).move_to(DOWN * 0.15)

        with self.voiceover(text=NARRATION["cannot"]):
            self.play(FadeIn(head, shift=DOWN * 0.2), Create(ground),
                      run_time=4.36)
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(GrowFromEdge(big_tree, DOWN), FadeIn(t_q), FadeIn(t_no),
                      run_time=3.93)
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(FadeIn(water), FadeIn(r_q), FadeIn(r_no), run_time=5.23)
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(FadeIn(sea), FadeIn(ship), FadeIn(s_q), FadeIn(s_no),
                      run_time=4.81)
            self.add_sound(self.sfx["swipe"], gain=-16)
            self.play(Create(tape), run_time=1.09)
            self.play(FadeIn(tape_x, scale=1.6),
                      Wiggle(tape, scale_value=1.10), run_time=1.09)
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(FadeIn(useless, shift=UP * 0.2), run_time=3.49)
        # 3.6+3.69+4.25+4.06+1.75+2.03+4.62+0.55 = 24.55 s

        self.play(FadeOut(VGroup(head, ground, big_tree, t_q, t_no, water,
                                 r_q, r_no, sea, ship, s_q, s_no, tape,
                                 tape_x, useless)), run_time=0.55)

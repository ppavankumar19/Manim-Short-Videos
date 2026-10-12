from common import *

# Six counting squares.  A child can count them before and after, which is
# the whole proof that rearranging does not change how much there is —
# far more graspable than "I cannot measure a round thing", which a child
# can fairly answer with "I would just use a piece of string".
CELL = 0.78
START = np.array([-4.20, -0.55, 0.0])       # bottom-left of the 3x2 block
SQ_COLS = ("#4CC9FF", "#3DE0A6", "#FFC53D", "#FF8095", "#CE93FF", "#A3E635")


def _cell(origin, i, j):
    return origin + np.array([(i + 0.5) * CELL, (j + 0.5) * CELL, 0.0])


class Scene05Idea(VoiceoverScene):
    """Cut it up, move the pieces — you still have the same amount."""

    def construct(self):
        self.set_speech_service(scene_speech_service("idea"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(lesson_backdrop())

        name = heading("Archimedes had a simple idea", AMBER, 42)
        name.move_to(UP * 2.85)

        # --- six squares, first as a neat 3 x 2 rectangle ------------------
        squares = VGroup()
        for k in range(6):
            squares.add(
                Square(side_length=CELL * 0.94, fill_color=SQ_COLS[k],
                       fill_opacity=0.88, stroke_color=BG_BOTTOM,
                       stroke_width=3).move_to(_cell(START, k % 3, k // 3)))
        cap_a = txt("6 pieces", 30, MUTED).next_to(squares, DOWN, buff=0.42)

        # --- the same six, shuffled into a staircase -----------------------
        STAIR = np.array([1.35, -0.55, 0.0])
        stair_cells = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (1, 2)]
        targets = [_cell(STAIR, i, j) for i, j in stair_cells]
        cap_b = txt("still 6 pieces", 30, MUTED)
        cap_b.move_to(np.array([STAIR[0] + 1.2, START[1] - 0.42, 0.0]))

        arrow = Arrow(np.array([-1.05, 0.60, 0.0]), np.array([0.75, 0.60, 0.0]),
                      color=MUTED, stroke_width=6, buff=0.05)
        moved = txt("cut them up  •  move them about", 30, INK)
        moved.move_to(np.array([-0.15, 1.45, 0.0]))
        same = heading("nothing is lost!", SUCCESS, 44).move_to(DOWN * 2.75)

        # --- so do exactly that to a circle -------------------------------
        circ = Circle(radius=1.30, stroke_color=ACCENT, stroke_width=7,
                      fill_color=ACCENT, fill_opacity=0.18)
        circ.move_to(np.array([-3.45, -0.10, 0.0]))
        plan = heading("cut the circle up,\nbuild a shape you know", AMBER, 38)
        plan.move_to(np.array([2.35, -0.10, 0.0]))
        plan_arrow = Arrow(np.array([-1.85, -0.10, 0.0]),
                           np.array([-0.35, -0.10, 0.0]),
                           color=AMBER, stroke_width=6, buff=0.05)

        with self.voiceover(text=NARRATION["idea"]):
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(FadeIn(name, shift=DOWN * 0.2), run_time=2.08)
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(
                LaggedStart(*[GrowFromCenter(s) for s in squares],
                            lag_ratio=0.12),
                FadeIn(cap_a), run_time=3.9)
            # the pieces get shuffled into a completely different shape
            self.add_sound(self.sfx["swipe"], gain=-16)
            self.play(
                GrowArrow(arrow), FadeIn(moved),
                LaggedStart(*[sq.animate.move_to(t)
                              for sq, t in zip(squares, targets)],
                            lag_ratio=0.16),
                FadeOut(cap_a), run_time=4.02)
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(FadeIn(cap_b), FadeIn(same, scale=0.75),
                      Indicate(squares, color=SUCCESS, scale_factor=1.05),
                      run_time=1.25)
            # now do the same thing to a circle
            self.add_sound(self.sfx["pop"], gain=-16)
            self.play(
                FadeOut(VGroup(squares, cap_b, arrow, moved, same, name)),
                FadeIn(circ), GrowArrow(plan_arrow),
                FadeIn(plan, shift=RIGHT * 0.2),
                run_time=4.98)
        # 2.08+3.9+4.02+1.25+4.98 = 16.23 s

        self.play(FadeOut(VGroup(circ, plan_arrow, plan)), run_time=0.54)

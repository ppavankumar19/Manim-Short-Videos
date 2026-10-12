from common import *

O = np.array([-3.0, 0.15, 0.0])          # where the circle sits
BIG = 1.95                                # a roomier radius for this beat


class Scene06Rings(VoiceoverScene):
    """A circle is not one shape — it is a stack of rings."""

    def construct(self):
        self.set_speech_service(scene_speech_service("rings"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(lesson_backdrop())

        secret = txt("The secret:", 38, AMBER).to_edge(UP, buff=0.55)

        disc = Circle(radius=BIG, stroke_color=ACCENT, stroke_width=6,
                      fill_color=ACCENT, fill_opacity=0.15).move_to(O)

        trunk = tree_rings(np.array([3.6, 0.55, 0.0]), 1.35, 7)
        l_trunk = txt("like a tree trunk", 30, "#B98B57")
        l_trunk.next_to(trunk, DOWN, buff=0.35)

        # three named rings, drawn one at a time
        r_small = Circle(radius=BIG * 0.22, stroke_color=VIOLET,
                         stroke_width=8, fill_opacity=0).move_to(O)
        r_mid = Circle(radius=BIG * 0.55, stroke_color=ROSE,
                       stroke_width=8, fill_opacity=0).move_to(O)
        r_big = Circle(radius=BIG * 0.86, stroke_color=ORANGE,
                       stroke_width=8, fill_opacity=0).move_to(O)
        r_edge = Circle(radius=BIG, stroke_color=AMBER,
                        stroke_width=8, fill_opacity=0).move_to(O)

        # the live count: rings redrawn from the tracker every frame
        n_tr = ValueTracker(8.0)

        def build():
            n = int(round(n_tr.get_value()))
            g = VGroup()
            for i in range(n):
                t = BIG * (i + 0.5) / n
                g.add(Circle(radius=t, stroke_color=ring_colour(t, BIG),
                             stroke_width=max(1.5, RING_W * 26 / n * 0.72),
                             fill_opacity=0).move_to(O))
            return g

        live = always_redraw(build)
        # The number grows a digit at a time (8 -> 16 -> 32 -> 64).  Anchor
        # the word and hang the number off its left edge, or the two drift
        # into each other as the digits arrive.
        n_word = txt("rings", 34, MUTED).move_to(np.array([4.15, -2.35, 0.0]))
        n_num = Integer(8, font_size=52, color=AMBER)
        n_num.add_updater(
            lambda m: m.set_value(int(round(n_tr.get_value())))
                       .next_to(n_word, LEFT, buff=0.26)
                       .align_to(n_word, DOWN))
        n_lbl = VGroup(n_word)

        closing = txt("a circle IS its rings", 36, SUCCESS).to_edge(DOWN, buff=0.5)

        with self.voiceover(text=NARRATION["rings"]):
            self.play(FadeIn(secret, shift=DOWN * 0.2), run_time=1.82)
            self.play(GrowFromCenter(disc), run_time=2.72)
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(disc.animate.set_fill(opacity=0.06), run_time=2.28)
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(FadeIn(trunk, scale=0.8), FadeIn(l_trunk), run_time=3.18)
            self.play(Create(r_small), run_time=2.72)
            self.play(Create(r_mid), run_time=2.27)
            self.play(Create(r_big), run_time=2.28)
            self.play(Create(r_edge), run_time=3.18)
            # hand over to the live stack and let the count climb
            self.remove(r_small, r_mid, r_big, r_edge)
            self.add(live, n_word, n_num)
            self.add_sound(self.sfx["whoosh"], gain=-16)
            self.play(n_tr.animate.set_value(32.0), run_time=2.72,
                      rate_func=rate_functions.ease_in_out_sine)
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(n_tr.animate.set_value(64.0),
                      FadeIn(closing, shift=UP * 0.2), run_time=5,
                      rate_func=rate_functions.ease_in_out_sine)
        # 1.82+2.72+2.28+3.18+2.72+2.27+2.28+3.18+2.72+5+0.59 = 28.76 s

        live.clear_updaters()
        n_num.clear_updaters()
        self.play(FadeOut(VGroup(secret, disc, trunk, l_trunk, live, n_word, n_num,
                                 closing)), run_time=0.59)

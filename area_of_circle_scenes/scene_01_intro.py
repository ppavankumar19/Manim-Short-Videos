from common import *


class Scene01Intro(VoiceoverScene):
    """Round things you already know, and the word 'area'."""

    def construct(self):
        self.set_speech_service(scene_speech_service("intro"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(lesson_backdrop())

        head = txt("How many round things can you see?", 38, ACCENT)
        head.to_edge(UP, buff=0.55)

        wheel = bus_wheel(np.array([-4.4, 0.75, 0.0]), 0.78)
        clock = wall_clock(np.array([-1.5, 0.75, 0.0]), 0.78)
        roti = chapati(np.array([1.5, 0.75, 0.0]), 0.78)
        rupee = coin(np.array([4.4, 0.75, 0.0]), 0.66)

        l_wheel = txt("wheel", 26, MUTED).next_to(wheel, DOWN, buff=0.28)
        l_clock = txt("clock", 26, MUTED).next_to(clock, DOWN, buff=0.28)
        l_roti = txt("chapati", 26, MUTED).next_to(roti, DOWN, buff=0.28)
        l_coin = txt("coin", 26, MUTED).next_to(rupee, DOWN, buff=0.28)

        every = txt("Circles are everywhere.", 36, AMBER).move_to(DOWN * 1.15)

        ask = txt("How much paint to fill one in?", 36, INK).move_to(DOWN * 1.15)
        # the paint actually floods the chapati
        paint = Circle(radius=0.78, stroke_width=0, fill_color=SKY,
                       fill_opacity=0.85).move_to(roti.get_center())
        area_lbl = txt("that is the AREA", 40, SUCCESS).move_to(DOWN * 2.45)

        with self.voiceover(text=NARRATION["intro"]):
            self.play(FadeIn(head, shift=DOWN * 0.2), run_time=4.36)
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(GrowFromCenter(wheel), FadeIn(l_wheel), run_time=2.18)
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(GrowFromCenter(clock), FadeIn(l_clock), run_time=2.17)
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(GrowFromCenter(roti), FadeIn(l_roti), run_time=2.62)
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(GrowFromCenter(rupee), FadeIn(l_coin), run_time=1.73)
            self.play(FadeIn(every, scale=0.8), run_time=1.32)
            self.play(ReplacementTransform(every, ask), run_time=2.17)
            self.add_sound(self.sfx["whoosh"], gain=-16)
            self.play(GrowFromCenter(paint), run_time=5.66)
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(FadeIn(area_lbl, shift=UP * 0.2), run_time=2.18)
        # 4.36+2.18+2.17+2.62+1.73+1.32+2.17+5.66+2.18+0.61 = 25 s

        self.play(FadeOut(VGroup(head, wheel, clock, roti, rupee, l_wheel,
                                 l_clock, l_roti, l_coin, ask, paint,
                                 area_lbl)), run_time=0.61)

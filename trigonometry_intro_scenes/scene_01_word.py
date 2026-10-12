from common import *


class Scene01Word(VoiceoverScene):
    """The long frightening word, taken to pieces."""

    def construct(self):
        self.set_speech_service(scene_speech_service("word"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(lesson_backdrop())

        whole = heading("TRIGONOMETRY", ACCENT, 76).move_to(UP * 2.15)
        scary = txt("...long, and a bit frightening", 30, MUTED)
        scary.next_to(whole, DOWN, buff=0.40)

        # the three pieces, each landing under its own little picture
        tri = heading("TRI", AMBER, 62)
        gono = heading("GONO", ROSE, 62)
        metry = heading("METRY", SUCCESS, 62)
        pieces = VGroup(tri, gono, metry).arrange(RIGHT, buff=1.35)
        pieces.move_to(UP * 0.35)

        m_tri = txt("three", 34, AMBER).next_to(tri, DOWN, buff=0.34)
        m_gono = txt("corners", 34, ROSE).next_to(gono, DOWN, buff=0.34)
        m_metry = txt("measuring", 34, SUCCESS).next_to(metry, DOWN, buff=0.34)

        # a picture for each piece: three dots, a triangle, a ruler
        dots = VGroup(*[Dot(radius=0.13, color=AMBER) for _ in range(3)])
        dots.arrange(RIGHT, buff=0.30).next_to(m_tri, DOWN, buff=0.45)
        shape = Polygon(np.array([-0.42, -0.30, 0.0]),
                        np.array([0.42, -0.30, 0.0]),
                        np.array([0.0, 0.40, 0.0]),
                        stroke_color=ROSE, stroke_width=5,
                        fill_color=ROSE, fill_opacity=0.18)
        shape.next_to(m_gono, DOWN, buff=0.40)
        ruler = VGroup(
            Rectangle(width=1.25, height=0.34, fill_color="#E7C873",
                      fill_opacity=0.95, stroke_color="#B08A3E",
                      stroke_width=2),
            *[Line(np.array([x, 0.17, 0.0]), np.array([x, 0.02, 0.0]),
                   stroke_color="#7C5E22", stroke_width=2)
              for x in np.arange(-0.50, 0.55, 0.20)],
        )
        ruler.next_to(m_metry, DOWN, buff=0.42)

        answer = heading("measuring triangles", SUCCESS, 50)
        answer.move_to(DOWN * 2.55)

        with self.voiceover(text=NARRATION["word"]):
            self.play(Write(whole), run_time=3.45)
            self.play(FadeIn(scary, shift=UP * 0.15), run_time=2.64)
            self.add_sound(self.sfx["swipe"], gain=-16)
            # the word comes apart
            self.play(FadeOut(scary),
                      TransformFromCopy(whole, pieces), run_time=3.25)
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(FadeIn(m_tri, shift=UP * 0.2),
                      LaggedStart(*[GrowFromCenter(d) for d in dots],
                                  lag_ratio=0.25),
                      run_time=3.05)
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(FadeIn(m_gono, shift=UP * 0.2), Create(shape),
                      run_time=3.05)
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(FadeIn(m_metry, shift=UP * 0.2), FadeIn(ruler),
                      run_time=3.05)
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(Indicate(VGroup(m_tri, m_gono, m_metry), color=INK,
                               scale_factor=1.12), run_time=3.35)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.play(Write(answer), run_time=3.56)
        # 3.45+2.64+3.25+3.05+3.05+3.05+3.35+3.56+0.61 = 26.01 s

        self.play(FadeOut(VGroup(whole, pieces, m_tri, m_gono, m_metry,
                                 dots, shape, ruler, answer)), run_time=0.61)

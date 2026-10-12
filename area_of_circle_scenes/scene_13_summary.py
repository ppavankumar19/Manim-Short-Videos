from common import *

O = np.array([-4.35, 0.30, 0.0])
T = np.array([1.85, -0.95, 0.0])


class Scene13Summary(VoiceoverScene):
    """The whole idea in one picture: circle, rings, triangle, formula."""

    def construct(self):
        self.set_speech_service(scene_speech_service("summary"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(lesson_backdrop())

        head = txt("So remember...", 38, AMBER).to_edge(UP, buff=0.50)

        rings = ring_stack(1.0, O, T, N_RINGS, R_CIRC)
        tri = Polygon(T + LEFT * (TAU * R_CIRC / 2),
                      T + RIGHT * (TAU * R_CIRC / 2), T + UP * R_CIRC,
                      stroke_color=SUCCESS, stroke_width=5, fill_opacity=0)
        arrow = Arrow(np.array([-2.55, 0.10, 0.0]), np.array([-1.35, -0.55, 0.0]),
                      color=AMBER, stroke_width=5, buff=0.05)

        half = mtx(r"\tfrac{1}{2} \times 2 \pi r \times r", 44, INK)
        half.move_to(np.array([1.85, 1.75, 0.0]))
        final = mtx(r"\pi r^2", 76, SUCCESS).move_to(np.array([1.85, -2.75, 0.0]))
        box = SurroundingRectangle(final, color=SUCCESS, buff=0.30,
                                   corner_radius=0.16)
        ever = txt("every single time", 28, MUTED).next_to(box, RIGHT, buff=0.55)

        with self.voiceover(text=NARRATION["summary"]):
            self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.9)
            self.play(FadeIn(rings), run_time=2.5)
            self.add_sound(self.sfx["whoosh"], gain=-17)
            self.play(
                Transform(rings, ring_stack(0.0, O, T, N_RINGS, R_CIRC)),
                GrowArrow(arrow), run_time=5.2,
            )
            self.play(Create(tri), FadeIn(half), run_time=3)
            self.add_sound(self.sfx["ding"], gain=-13)
            self.play(Write(final), Create(box), run_time=2.1)
            self.play(FadeIn(ever), run_time=1.3)
        # 0.9+2.5+5.2+3+2.1+1.3+0.5 = 15.5 s

        self.play(FadeOut(VGroup(head, rings, tri, arrow, half, final, box,
                                 ever)), run_time=0.5)

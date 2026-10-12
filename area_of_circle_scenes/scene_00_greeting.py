from common import *


def spoke_wheel(radius: float = 3.35) -> VGroup:
    """A big faint wheel that reads as turning.

    A plain circle looks identical however far you spin it, so the wheel
    needs marks: spokes and rim ticks give the eye something to follow.
    """
    rim = Circle(radius=radius, stroke_color=ACCENT, stroke_width=5,
                 stroke_opacity=0.22, fill_opacity=0)
    inner = Circle(radius=radius * 0.62, stroke_color=VIOLET, stroke_width=3,
                   stroke_opacity=0.16, fill_opacity=0)
    spokes = VGroup(*[
        Line(radius * 0.10 * np.array([np.cos(a), np.sin(a), 0.0]),
             radius * np.array([np.cos(a), np.sin(a), 0.0]),
             stroke_color=ACCENT, stroke_width=3, stroke_opacity=0.15)
        for a in np.arange(0, TAU, TAU / 12)
    ])
    ticks = VGroup(*[
        Line(radius * 0.94 * np.array([np.cos(a), np.sin(a), 0.0]),
             radius * np.array([np.cos(a), np.sin(a), 0.0]),
             stroke_color=AMBER, stroke_width=4, stroke_opacity=0.28)
        for a in np.arange(0, TAU, TAU / 36)
    ])
    hub = Circle(radius=radius * 0.07, stroke_color=AMBER, stroke_width=3,
                 stroke_opacity=0.30, fill_opacity=0)
    return VGroup(rim, inner, spokes, ticks, hub)


class Scene00Greeting(VoiceoverScene):
    """Say hello, over one slowly turning wheel."""

    def construct(self):
        self.set_speech_service(scene_speech_service("greeting"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(lesson_backdrop())

        wheel = spoke_wheel()
        wheel.add_updater(lambda m, dt: m.rotate(0.16 * dt))
        self.add(wheel)

        hello = heading("Hello, friends!", ACCENT, 62).move_to(UP * 1.60)
        puzzle = txt("A 2000-year-old puzzle", 40, AMBER).move_to(UP * 0.20)
        promise = txt("and you will solve it yourself", 32, INK).move_to(DOWN * 0.85)
        go = mtx(r"\pi r^2 \;=\; ?", 62, SUCCESS).move_to(DOWN * 2.25)

        with self.voiceover(text=NARRATION["greeting"]):
            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(FadeIn(hello, shift=DOWN * 0.3), run_time=1.83)
            self.add_sound(self.sfx["whoosh"], gain=-17)
            self.play(FadeIn(puzzle, scale=0.75), run_time=5.5)
            self.play(FadeIn(promise, shift=UP * 0.2), run_time=2.75)
            self.add_sound(self.sfx["pop"], gain=-15)
            self.play(Write(go), run_time=1.37)
        # 1.83+5.5+2.75+1.37 = 11.45 s

        wheel.clear_updaters()
        self.play(FadeOut(VGroup(hello, puzzle, promise, go, wheel)),
                  run_time=0.5)

from common import *

# The circle sits up top; the triangle builds itself underneath.
O = np.array([0.0, 1.70, 0.0])
T = np.array([0.0, -2.15, 0.0])          # midpoint of the triangle's base
N = N_RINGS
SPREAD = 7.0                              # how many rings are mid-flight at once


def alpha_for(i: int, p: float) -> float:
    """How rolled-up ring `i` still is, given overall progress `p`.

    Ring 0 is the outermost and leaves first, so the longest line lands at
    the bottom of the stack and the triangle builds downward-up.
    """
    x = (p * (N + SPREAD) - i) / SPREAD
    return float(np.clip(1.0 - x, 0.0, 1.0))


class Scene07Unroll(VoiceoverScene):
    """Pull every ring straight; a triangle appears. The whole point."""

    def construct(self):
        self.set_speech_service(scene_speech_service("unroll"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(lesson_backdrop())

        magic = txt("Now the magic...", 38, AMBER).to_edge(UP, buff=0.45)

        radii = list(reversed(ring_radii(N, R_CIRC)))   # outermost first
        prog = ValueTracker(0.0)

        def build():
            return VGroup(*[
                unrolled_ring(t, alpha_for(i, prog.get_value()), O, T, R_CIRC)
                for i, t in enumerate(radii)
            ])

        rings = always_redraw(build)
        # a rim while it is still a disc, so it reads as one solid object
        rim = Circle(radius=R_CIRC + 0.035, stroke_color="#0A1220",
                     stroke_width=6, fill_opacity=0).move_to(O)
        self.add(rim, rings)

        # labels that ride along with the beat
        longest = mtx(r"2 \pi r", 44, AMBER)
        longest.move_to(np.array([TAU * R_CIRC / 2 + 0.75, T[1], 0.0]))
        l_long = txt("the outside ring", 26, MUTED).next_to(longest, UP, buff=0.20)
        shorter = txt("each one shorter", 28, ROSE)
        shorter.move_to(np.array([-4.55, -1.15, 0.0]))
        centre_dot = txt("centre = a dot", 26, VIOLET)
        centre_dot.move_to(np.array([-4.55, -0.30, 0.0]))

        tri = Polygon(T + LEFT * (TAU * R_CIRC / 2),
                      T + RIGHT * (TAU * R_CIRC / 2),
                      T + UP * R_CIRC,
                      stroke_color=SUCCESS, stroke_width=6, fill_opacity=0)
        shout = txt("A triangle!", 46, SUCCESS).move_to(UP * 1.55)

        with self.voiceover(text=NARRATION["unroll"]):
            self.play(FadeIn(magic, shift=DOWN * 0.2), run_time=1.28)
            self.remove(rim)
            self.add_sound(self.sfx["whoosh"], gain=-17)
            # one continuous unroll, ring by ring, across the next six beats
            self.play(prog.animate.set_value(0.10), run_time=2.98,
                      rate_func=rate_functions.linear)
            self.play(prog.animate.set_value(0.22), run_time=5.53,
                      rate_func=rate_functions.linear)
            self.add_sound(self.sfx["ding"], gain=-15)
            self.play(FadeIn(longest, shift=LEFT * 0.2), FadeIn(l_long),
                      run_time=2.55)
            self.play(prog.animate.set_value(0.45), FadeIn(shorter),
                      run_time=3.41, rate_func=rate_functions.linear)
            self.play(prog.animate.set_value(0.62), run_time=2.55,
                      rate_func=rate_functions.linear)
            self.play(prog.animate.set_value(0.88), FadeIn(centre_dot),
                      run_time=4.26, rate_func=rate_functions.linear)
            self.add_sound(self.sfx["whoosh"], gain=-16)
            self.play(prog.animate.set_value(1.0), FadeOut(magic),
                      run_time=4.68, rate_func=rate_functions.ease_out_sine)
            self.play(FadeOut(VGroup(shorter, centre_dot)), run_time=1.28)
            self.add_sound(self.sfx["success"], gain=-13)
            self.play(Create(tri), run_time=0.85)
            self.play(FadeIn(shout, scale=0.7),
                      Flash(T + UP * R_CIRC, color=SUCCESS, flash_radius=0.9,
                            num_lines=16),
                      run_time=2.55)
        # 1.28+2.98+5.53+2.55+3.41+2.55+4.26+4.68+1.28+0.85+2.55+0.53 = 32.45 s

        rings.clear_updaters()
        self.play(FadeOut(VGroup(rings, longest, l_long, tri, shout)),
                  run_time=0.53)

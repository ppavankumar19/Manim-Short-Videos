from common import *

# The man stands just behind the triangle's vertex so the ray of sight
# leaves the ground in front of his feet instead of cutting through him.
MAN_BASE = OBS + RIGHT * 0.46


class Scene02Hook(VoiceoverScene):
    """A tower, a man, and the two things he can actually measure."""

    def construct(self):
        self.set_speech_service(scene_speech_service("hook"), create_subcaption=True)
        self.sfx = load_sfx()

        self.add(sky_ground_backdrop())
        self.add(star_field(18, y_min=1.2).set_opacity(0.45))

        tower = realistic_tower()
        h_q = mtx(r"h = \;?", 40, AMBER).move_to(TOP + UP * 0.95 + RIGHT * 0.15)

        start_x = 4.6
        man = Man(base=np.array([start_x, GROUND_Y, 0.0]), height=MAN_H,
                  facing=LEFT, pose=WALK_A)

        steps = 6
        xs = np.linspace(start_x, MAN_BASE[0], steps + 1)
        walk = []
        for i in range(1, steps + 1):
            pose = WALK_B if i % 2 else WALK_A
            if i == steps:
                pose = LOOKING_UP
            target = Man(base=np.array([xs[i], GROUND_Y, 0.0]), height=MAN_H,
                         facing=LEFT, pose=pose)
            walk.append(Transform(man, target, run_time=5.0 / steps,
                                  rate_func=rate_functions.linear))

        looking = Man(base=MAN_BASE, height=MAN_H, facing=LEFT, pose=POINTING_UP)

        sight = DashedLine(OBS, TOP, stroke_color=AMBER, stroke_width=4,
                           dash_length=0.14)
        obs_dot = Dot(OBS, color=SUCCESS, radius=0.07)

        ground_brace = BraceBetweenPoints(OBS, FOOT, direction=DOWN, color=MUTED)
        d_lbl = mtx(r"d", 40, MUTED).next_to(ground_brace, DOWN, buff=0.18)

        # What a tape can reach, and what it cannot — in symbols.
        can_d = mtx(r"\checkmark \;\; d", 44, SUCCESS)
        can_t = mtx(r"\checkmark \;\; \theta", 44, SUCCESS)
        cant_h = mtx(r"\times \;\; h", 44, ROSE)
        panel = VGroup(can_d, can_t, cant_h).arrange(DOWN, buff=0.62,
                                                     aligned_edge=LEFT)
        panel.move_to(np.array([3.30, 0.55, 0.0]))
        panel_box = SurroundingRectangle(panel, color=MUTED, buff=0.55,
                                         corner_radius=0.16)

        with self.voiceover(text=NARRATION["hook"]):
            self.add_sound(self.sfx["whoosh"], gain=-15)
            self.play(GrowFromEdge(tower, DOWN), FadeIn(h_q, shift=DOWN * 0.3),
                      run_time=3.5)
            self.add(man)
            self.play(Succession(*walk), run_time=5.0)
            self.add_sound(self.sfx["pop"], gain=-16)
            self.play(
                Transform(man, looking), FadeIn(obs_dot),
                Create(sight), run_time=4.0,
            )
            self.add_sound(self.sfx["click"], gain=-17)
            self.play(GrowFromCenter(ground_brace), FadeIn(d_lbl),
                      Create(panel_box),
                      LaggedStart(FadeIn(can_d, shift=RIGHT * 0.2),
                                  FadeIn(can_t, shift=RIGHT * 0.2),
                                  lag_ratio=0.5),
                      run_time=4.0)
            self.play(
                Indicate(h_q, color=AMBER, scale_factor=1.35),
                Flash(TOP, color=AMBER, flash_radius=0.6, num_lines=12),
                FadeIn(cant_h, scale=1.4),
                run_time=2.5,
            )
            self.play(
                FadeOut(VGroup(tower, h_q, man, sight, obs_dot, ground_brace,
                               d_lbl, panel, panel_box)),
                run_time=1.0,
            )
        # 3.5+5.0+4.0+4.0+2.5+1.0 = 20.0 s

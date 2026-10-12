from common import *


def house(centre):
    """A house with the detail that makes it read as a house.

    Walls, framed windows, a door with a step, a tiled pitched roof with
    overhanging eaves, and a chimney.  The roof is a real triangle, which
    is the point: a builder sets its pitch by an angle.
    """
    c = np.asarray(centre, dtype=float)
    W, D, H = 1.70, 1.30, 1.35
    F = -D / 2 - 0.05                      # the face we look at, held proud
    RW, RD, RH = W + 0.34, D + 0.34, 0.88  # roof overhangs the walls
    RF = -RD / 2 - 0.05

    walls = box3(c + np.array([0.0, 0.0, H / 2]), W, D, H,
                 "#E4D2B4", "#D3BC98", "#A8916F")

    def plate(dx, z0, z1, w, col, y=F):
        return face3([c + np.array([dx - w, y, z0]), c + np.array([dx + w, y, z0]),
                      c + np.array([dx + w, y, z1]), c + np.array([dx - w, y, z1])],
                     col)

    # two framed windows with cross bars
    win = VGroup()
    for dx in (-0.47, 0.47):
        win.add(plate(dx, 0.62, 1.02, 0.20, "#7A5230"))          # frame
        win.add(plate(dx, 0.65, 0.99, 0.17, "#5FA8E0", F - 0.01))  # glass
        win.add(line3(c + np.array([dx, F - 0.02, 0.65]),
                      c + np.array([dx, F - 0.02, 0.99]), "#7A5230", 3.0))
        win.add(line3(c + np.array([dx - 0.17, F - 0.02, 0.82]),
                      c + np.array([dx + 0.17, F - 0.02, 0.82]), "#7A5230", 3.0))

    # CE sorts 3D mobjects by one point's depth, which here works out as
    # 0.961*|y| + 0.276*z.  The door sits low, so its z term is small and
    # at y = F it lands BEHIND the wall face.  Pushing it forward past
    # y = -0.76 makes the y term dominate and the door show.
    DF = F - 0.22
    door = VGroup(plate(0.0, 0.0, 0.62, 0.22, "#6B4423", DF),
                  plate(0.0, 0.03, 0.59, 0.19, "#8A5A2B", DF - 0.01),
                  dot3(c + np.array([0.13, DF - 0.02, 0.31]), "#FFE08A", 0.030))
    step = box3(c + np.array([0.0, F - 0.14, 0.045]), 0.62, 0.28, 0.09,
                "#B9B2A6", "#A29B8F", "#857F74")

    roof = roof3(c + np.array([0.0, 0.0, H]), RW, RD, RH, "#C25E47", "#8E3D2E")
    # tile courses along the near slope
    tiles = VGroup()
    for f in (0.25, 0.5, 0.75):
        z = H + RH * f
        x = (RW / 2) * (1 - f)
        tiles.add(line3(c + np.array([-x, RF, z]), c + np.array([x, RF, z]),
                        "#9E4636", 3.0))
    chimney = box3(c + np.array([W * 0.30, 0.10, H + RH * 0.72]),
                   0.24, 0.24, 0.58, "#9C6B54", "#8A5D48", "#6E4A39")

    return VGroup(walls, win, door, step, roof, tiles, chimney)


def rocket_ship(nose_at):
    """A rocket: flame, fins, body, nose cone."""
    b = np.asarray(nose_at, dtype=float)
    BODY_H, R = 0.86, 0.15
    flame = VGroup(
        face3([b + np.array([-R * 0.85, 0.0, 0.0]),
               b + np.array([R * 0.85, 0.0, 0.0]),
               b + np.array([0.0, 0.0, -0.48])], "#FFC53D"),
        face3([b + np.array([-R * 0.42, 0.0, 0.0]),
               b + np.array([R * 0.42, 0.0, 0.0]),
               b + np.array([0.0, 0.0, -0.27])], "#FF8095"),
    )
    fins = VGroup(*[
        face3([b + np.array([sx * R, 0.0, 0.0]),
               b + np.array([sx * R * 2.4, 0.0, -0.03]),
               b + np.array([sx * R, 0.0, 0.34])], "#D9536B")
        for sx in (-1, 1)
    ])
    body = box3(b + np.array([0.0, 0.0, BODY_H / 2]), R * 2, R * 2, BODY_H,
                "#F8FAFC", "#E2E8F0", "#94A3B8")
    nose = pyramid3(b + np.array([0.0, 0.0, BODY_H]), R * 2, R * 2, 0.46,
                    "#FF8095", "#D9536B")
    return VGroup(flame, fins, body, nose)


def satellite(centre):
    """A satellite: two solar wings, a body, and a dish underneath."""
    c = np.asarray(centre, dtype=float)
    wings = VGroup(
        panel3(c + np.array([-0.48, 0.0, 0.0]), 0.62, 0.30, "#2F6FB5"),
        panel3(c + np.array([0.48, 0.0, 0.0]), 0.62, 0.30, "#2F6FB5"),
    )
    booms = VGroup(line3(c + LEFT * 0.13, c + LEFT * 0.30, "#CBD5E1", 4.0),
                   line3(c + RIGHT * 0.13, c + RIGHT * 0.30, "#CBD5E1", 4.0))
    body = box3(c, 0.26, 0.22, 0.26, "#FFE08A", AMBER, "#B8860B")
    dish = face3([c + np.array([-0.10, 0.0, -0.13]),
                  c + np.array([0.10, 0.0, -0.13]),
                  c + np.array([0.15, 0.0, -0.31]),
                  c + np.array([-0.15, 0.0, -0.31])], "#E2E8F0")
    return VGroup(wings, booms, body, dish)


class Scene07Used(VoiceoverScene, ThreeDScene):
    """Where the triangle is actually doing a job, out in the world."""

    def construct(self):
        self.set_speech_service(scene_speech_service("used"), create_subcaption=True)
        self.sfx = load_sfx()
        stage_3d(self)

        # A single fixed camera, pulled back far enough that all three
        # vignettes stay fully in shot for the whole beat.
        self.set_camera_orientation(phi=74 * DEGREES, theta=-90 * DEGREES,
                                    zoom=0.80,
                                    frame_center=np.array([0.0, 0.0, 1.30]))

        ground = Rectangle(width=13.0, height=8.0, fill_color="#14243E",
                           fill_opacity=0.75, stroke_width=0)
        ground.set_shade_in_3d(True)
        grid = VGroup(*[
            Line(np.array([x, -4.0, 0.0]), np.array([x, 4.0, 0.0]),
                 stroke_color="#27456F", stroke_width=1.5, stroke_opacity=0.5)
            for x in np.arange(-6.5, 6.51, 1.0)
        ] + [
            Line(np.array([-6.5, y, 0.0]), np.array([6.5, y, 0.0]),
                 stroke_color="#27456F", stroke_width=1.5, stroke_opacity=0.5)
            for y in np.arange(-4.0, 4.01, 1.0)
        ])
        grid.set_shade_in_3d(True)

        # 1 — a house, and the roof pitch the builder sets
        HOME = np.array([-4.35, 0.0, 0.0])
        home = house(HOME)
        # The roof gable reaches y = -0.87, so the markers sit in front of
        # it or the depth sort hides them behind the slope.
        FY = -1.15
        EAVE_L = HOME + np.array([-1.02, FY, 1.35])
        EAVE_R = HOME + np.array([1.02, FY, 1.35])
        RIDGE = HOME + np.array([0.0, FY, 2.23])
        pitch = line3(EAVE_L, RIDGE, AMBER, 9.0)
        eave = line3(EAVE_L, EAVE_R, VIOLET, 7.0)
        # the pitch angle itself, drawn where a builder would measure it
        roof_ang = arc_between_3d(EAVE_L, EAVE_R, RIDGE, 0.58, SUCCESS)
        roof_ang.set_stroke(width=7)

        # 2 — a rocket, and the angle it climbs at
        LAUNCH = np.array([-0.85, 0.0, 0.0])
        TIP = LAUNCH + np.array([1.85, 0.0, 2.85])
        path = VMobject(stroke_color=ROSE, stroke_width=6)
        path.set_points_smoothly([
            LAUNCH + np.array([1.85 * t, 0.0, 2.85 * t ** 1.5])
            for t in np.linspace(0, 1, 40)])
        path.set_shade_in_3d(True)
        ship = rocket_ship(TIP)
        ship.rotate(0.55, axis=RIGHT, about_point=TIP)
        launch = line3(LAUNCH, LAUNCH + np.array([1.85, 0.0, 0.0]), VIOLET, 7.0)

        # 3 — satellites fixing a phone on the ground
        PAD = np.array([4.55, 0.0, 0.0])
        pad = Circle(radius=1.00, stroke_color=SUCCESS, stroke_width=5,
                     fill_color=SUCCESS, fill_opacity=0.16).move_to(PAD)
        pad.set_shade_in_3d(True)
        phone = box3(PAD + np.array([0.0, 0.0, 0.24]), 0.28, 0.14, 0.48,
                     "#F8FAFC", "#E2E8F0", "#94A3B8")
        screen = face3([PAD + np.array([-0.11, -0.078, 0.10]),
                        PAD + np.array([0.11, -0.078, 0.10]),
                        PAD + np.array([0.11, -0.078, 0.42]),
                        PAD + np.array([-0.11, -0.078, 0.42])], "#4CC9FF")
        sats = [PAD + v for v in (np.array([-1.45, 0.65, 2.60]),
                                  np.array([1.60, -0.55, 2.35]),
                                  np.array([0.10, 1.55, 2.95]))]
        sat_group = VGroup(*[satellite(p) for p in sats])
        beams = VGroup(*[line3(p, PAD + np.array([0.0, 0.0, 0.48]), AMBER,
                               5.0, 0.9) for p in sats])

        caps = []
        for words in ("builders set a roof by its angle",
                      "sailors crossed oceans with it",
                      "engineers fly rockets with it",
                      "satellites find your phone with it"):
            m = chip(heading(words, INK, 34))
            self.add_fixed_in_frame_mobjects(m)
            m.to_edge(UP, buff=0.45)
            m.set_opacity(0.0)
            caps.append(m)
        closing = chip(heading("every one is a triangle underneath", SUCCESS, 36))
        self.add_fixed_in_frame_mobjects(closing)
        closing.to_edge(UP, buff=0.45)
        closing.set_opacity(0.0)

        with self.voiceover(text=NARRATION["used"]):
            self.play(FadeIn(ground), Create(grid), run_time=2.11)
            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(GrowFromEdge(home, IN), Create(eave), Create(pitch),
                      Create(roof_ang),
                      caps[0].animate.set_opacity(1.0), run_time=3.37)
            self.add_sound(self.sfx["whoosh"], gain=-17)
            self.play(caps[0].animate.set_opacity(0.0),
                      caps[1].animate.set_opacity(1.0), run_time=4.64)
            self.add_sound(self.sfx["whoosh"], gain=-16)
            self.play(Create(launch), Create(path), FadeIn(ship),
                      caps[1].animate.set_opacity(0.0),
                      caps[2].animate.set_opacity(1.0), run_time=3.80)
            self.add_sound(self.sfx["ding"], gain=-15)
            self.play(FadeIn(pad), FadeIn(phone), FadeIn(screen),
                      LaggedStart(*[GrowFromCenter(s) for s in sat_group],
                                  lag_ratio=0.3),
                      caps[2].animate.set_opacity(0.0),
                      caps[3].animate.set_opacity(1.0), run_time=4.60)
            self.play(Create(beams), run_time=3.00)
            self.add_sound(self.sfx["success"], gain=-13)
            self.play(caps[3].animate.set_opacity(0.0),
                      closing.animate.set_opacity(1.0), run_time=3.79)
        # 2.17+4.52+4.16+4.88+4.34+2.17+3.07 = 25.31 s

        self.play(FadeOut(VGroup(ground, grid, home, eave, pitch, roof_ang, path,
                                 launch, beams, sat_group, pad, screen)),
                  FadeOut(ship), FadeOut(phone),
                  closing.animate.set_opacity(0.0), run_time=0.72)

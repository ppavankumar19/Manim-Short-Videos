from common import *

# The six shapes are not six species, they are one family with a hierarchy,
# and this beat draws that hierarchy as a tree.  It is deliberately flat --
# no camera tilt -- because an inclusion diagram has to be read, not walked
# around, and because it sets up the sentence the rest of the lesson lives
# on: going down the tree means adding conditions, and a construction is
# nothing but a list of conditions.

ICON = 0.42                       # how far each icon is scaled from full size

# Every name is set to one side of its icon, never underneath it: the arrows
# arrive from below, and a label parked in the arrival path is the fastest way
# to make a clean diagram look like a scribble.
NODES = {
    #  name            centre                     icon shape       colour   label side
    "quad": (np.array([0.0, 2.60, 0.0]), None, MUTED, RIGHT),
    "trapezium": (np.array([-3.45, 1.10, 0.0]), "trapezium", VIOLET, LEFT),
    "kite": (np.array([3.45, 1.10, 0.0]), "kite", TEAL, RIGHT),
    "parallelogram": (np.array([-3.45, -0.50, 0.0]), "parallelogram", AMBER, LEFT),
    "rectangle": (np.array([-5.75, -1.95, 0.0]), "rectangle", SUCCESS, DOWN),
    "rhombus": (np.array([-1.20, -1.95, 0.0]), "rhombus", ROSE, RIGHT),
    "square": (np.array([-3.10, -3.10, 0.0]), "square", ACCENT, DOWN),
}

# child -> parent, i.e. "every child is also a parent".  The rhombus is a
# kite as well as a parallelogram, and that second edge is drawn dashed
# because it is the one every class forgets.
EDGES = [
    ("trapezium", "quad", False),
    ("kite", "quad", False),
    ("parallelogram", "trapezium", False),
    ("rectangle", "parallelogram", False),
    ("rhombus", "parallelogram", False),
    ("rhombus", "kite", True),
    ("square", "rectangle", False),
    ("square", "rhombus", False),
]

# a plain, unequal quadrilateral for the root of the tree: nothing equal,
# nothing parallel, nothing square -- the only thing every member still is
GENERIC = [np.array(v) for v in ((-1.5375, -0.6125, 0.0), (0.7625, -0.8625, 0.0),
                                 (0.9625, 0.8375, 0.0), (-1.1875, 0.6375, 0.0))]


def icon(name: str | None, color: str) -> VGroup:
    pts = GENERIC if name is None else FAMILY_PTS[name]
    body = Polygon(*[p * ICON for p in pts], fill_color=color,
                   fill_opacity=0.35, stroke_color=color, stroke_width=3.5)
    return VGroup(body)


class Scene01dTree(VoiceoverScene):
    """One family, in order of how much each member promises."""

    def construct(self):
        self.set_speech_service(scene_speech_service("tree"), create_subcaption=True)
        self.sfx = load_sfx()
        self.add(paper_backdrop())

        marks, labels = {}, {}
        for key, (pos, shape, color, side) in NODES.items():
            g = icon(shape, color).move_to(pos)
            marks[key] = g
            name = "Quadrilateral" if shape is None else FAMILY_NAME[shape]
            labels[key] = txt(name, 22, color, "BOLD").next_to(g, side, buff=0.18)

        links = VGroup()
        for child, parent, dashed in EDGES:
            start = marks[child].get_center()
            end = marks[parent].get_center()
            span = max(float(np.linalg.norm(end - start)), 1e-6)
            u = (end - start) / span
            # trim proportionally, so a short link between two neighbouring
            # levels still has an arrow left after both ends are cleared
            a = start + u * min(0.72, 0.30 * span)
            b = end - u * min(0.78, 0.32 * span)
            if dashed:
                links.add(DashedLine(a, b, stroke_color=MUTED, stroke_width=2.2,
                                     stroke_opacity=0.55))
            else:
                links.add(Arrow(a, b, buff=0, stroke_width=3,
                                max_tip_length_to_length_ratio=0.12,
                                color=MUTED))

        title = heading("One family, not six shapes", ACCENT)
        legend = mtx(r"X \longrightarrow Y \;\equiv\; X \subset Y", 30, MUTED)
        legend.move_to(np.array([4.55, -0.75, 0.0]))
        chain = mtx(r"\text{square} \subset \text{rhombus} \subset "
                    r"\text{parallelogram} \subset \text{trapezium}", 22, SUCCESS)
        chain.move_to(np.array([3.40, -2.60, 0.0]))
        conds = mtx(r"\downarrow \;\; +\,\text{conditions}", 30, AMBER)
        conds.move_to(np.array([4.55, -3.55, 0.0]))

        with self.voiceover(text=NARRATION["tree"]):
            self.add_sound(self.sfx["whoosh"], gain=-16)
            self.play(FadeIn(title, shift=DOWN * 0.2),
                      GrowFromCenter(marks["quad"]),
                      FadeIn(labels["quad"]), run_time=3.8)

            self.add_sound(self.sfx["click"], gain=-17)
            self.play(
                LaggedStart(*[GrowArrow(links[i]) for i in (0, 1)],
                            lag_ratio=0.30),
                LaggedStart(*[FadeIn(VGroup(marks[k], labels[k]),
                                     shift=DOWN * 0.2)
                              for k in ("trapezium", "kite")], lag_ratio=0.30),
                run_time=5.2,
            )

            self.add_sound(self.sfx["pop"], gain=-17)
            self.play(
                GrowArrow(links[2]),
                FadeIn(VGroup(marks["parallelogram"], labels["parallelogram"]),
                       shift=DOWN * 0.2),
                FadeIn(legend),
                run_time=3.8,
            )

            self.play(
                LaggedStart(*[GrowArrow(links[i]) for i in (3, 4)],
                            lag_ratio=0.30),
                LaggedStart(*[FadeIn(VGroup(marks[k], labels[k]),
                                     shift=DOWN * 0.2)
                              for k in ("rectangle", "rhombus")], lag_ratio=0.30),
                run_time=4.6,
            )
            self.play(Create(links[5]), run_time=1.6)

            self.add_sound(self.sfx["ding"], gain=-14)
            self.play(
                LaggedStart(*[GrowArrow(links[i]) for i in (6, 7)],
                            lag_ratio=0.25),
                FadeIn(VGroup(marks["square"], labels["square"]),
                       shift=DOWN * 0.2),
                run_time=4.2,
            )
            self.play(Write(chain), FadeIn(conds, shift=DOWN * 0.2),
                      run_time=4.0)
            self.play(
                Indicate(VGroup(marks["square"], marks["rhombus"],
                                marks["parallelogram"], marks["trapezium"]),
                         color=SUCCESS, scale_factor=1.06),
                run_time=2.4,
            )

            self.play(
                FadeOut(VGroup(title, legend, chain, conds, links,
                               *marks.values(), *labels.values())),
                run_time=1.8,
            )
        # 3.8+5.2+3.8+4.6+1.6+4.2+4.0+2.4+1.8 = 31.4 s

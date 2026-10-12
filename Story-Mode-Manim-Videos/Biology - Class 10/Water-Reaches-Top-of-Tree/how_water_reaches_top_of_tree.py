"""
How Water Reaches the Top of a Tree: Xylem, Root Pressure & Transpiration Pull
Story-mode chalkboard lesson (Class 10 Biology, Chapter 3: Circulation).

LLM KEY / FUNCTION NAME: how_water_reaches_top_of_tree

Follow ONE water drop from the soil to the atmosphere:
soil -> root hair -> (osmosis) root cells -> xylem -> (root pressure: a small,
variable push) -> leaf mesophyll -> (transpiration) stomata -> atmosphere, and
the transpiration pull on the continuous water column -- the main force.

Production rules (the series' rules): everything inside the green board,
medium type (TEXT_SCALE 0.72), boxes that hug their text, fixed-size picture
cards with the caption in its own strip, visible arrows and plus signs,
nothing on the teacher / students / badges, and every picture appears when the
voice reaches its bookmark.

Corrections / decisions on the draft storyboard:
  * water is shown as a CONTINUOUS column in the xylem (linked molecules that
    move together), never as droplets jumping up independently;
  * evaporation happens from mesophyll cell surfaces into air spaces and out
    through the stoma -- never inside the xylem tube;
  * root pressure is drawn as a SMALL arrow, transpiration pull as a LARGE one;
  * the phrase "continuous molecular attraction" is the headline; the word
    cohesion is not used;
  * the five-pause challenge uses the series' ten-second THINK clock;
  * phloem is not shown (this video is about water in xylem only).

Scenes: title, then
  1 the 180 m problem    2 root hairs       3 root hair -> xylem (osmosis)
  4 root pressure        5 why it is not enough
  6 the leaf loses water 7 transpiration pull   8 the column does not break
  9 your turn           10 one drop's journey, summary and thanks
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_BIO = next(p for p in _HERE.parents if (p / "bio_kit.py").exists())
if str(_BIO) not in sys.path:
    sys.path.insert(0, str(_BIO))

from bio_kit import *  # noqa: F401,F403,E402
from bio_art import *  # noqa: F401,F403,E402
from bio_widgets import *  # noqa: F401,F403,E402

WATER_C = "#4FC3F7"
GREEN_C = "#81C784"
SOIL_C = "#BCAAA4"

NARRATION = {
    "title": (
        "How does water reach the top of a tree? <bookmark mark='b0'/> "
        "Xylem, root pressure and transpiration pull."
    ),
    "s1": (
        "Look at this eucalyptus tree, and a person standing beside it. "
        "<bookmark mark='b0'/> Now let us climb. Twenty metres, "
        "<bookmark mark='b1'/> sixty metres, <bookmark mark='b2'/> one "
        "hundred metres, <bookmark mark='b3'/> and finally, about one hundred "
        "and eighty metres. <bookmark mark='b4'/> Far below, in the soil near "
        "a root, is one tiny drop of water. <bookmark mark='b5'/> So how can "
        "this drop get all the way up there?"
    ),
    "s2": (
        "The first gate is the root hair. <bookmark mark='b0'/> A root has "
        "many fine, microscopic projections, and each one is a root hair. "
        "<bookmark mark='b1'/> Water sits in thin films between the soil "
        "particles. <bookmark mark='b2'/> Our drop moves towards a root hair "
        "and crosses into it. This is where water enters the plant. "
        "<bookmark mark='b3'/> Each root hair is tiny, but together they make "
        "a huge absorbing region. <bookmark mark='b4'/> So how does water "
        "move in? <bookmark mark='b5'/> The answer is osmosis."
    ),
    "s3": (
        "Now follow the drop inside the root. <bookmark mark='b0'/> The soil "
        "water is more dilute, and the cell sap of the root hair is more "
        "concentrated. <bookmark mark='b1'/> So water moves into the root "
        "hair by osmosis. <bookmark mark='b2'/> The same drop then passes from "
        "cell to cell, through the neighbouring root cells. "
        "<bookmark mark='b3'/> Finally, it enters a large vertical tube: the "
        "xylem vessel. <bookmark mark='b4'/> Many root hairs feed many xylem "
        "pathways. <bookmark mark='b5'/> So the path is: soil, root hair, "
        "root cells, xylem."
    ),
    "s4": (
        "Many root hairs keep adding water, and it collects in the xylem. "
        "<bookmark mark='b0'/> Pressure builds up there, and it can push the "
        "water upward. This is called root pressure. <bookmark mark='b1'/> You "
        "can see it in a simple activity. Cut a stem, and fix a glass tube to "
        "it. The water level rises from M one to M two. <bookmark "
        "mark='b2'/> But notice the arrow. It is only a small push, "
        "<bookmark mark='b3'/> and it is not the main force."
    ),
    "s5": (
        "Now picture the whole tree. The xylem runs unbroken from the roots "
        "to the crown. <bookmark mark='b0'/> Root pressure pushes from the "
        "bottom, but next to the height of the tree, it is small. "
        "<bookmark mark='b1'/> In fact, root pressure is seldom high, and "
        "sometimes it may be nil. <bookmark mark='b2'/> Then what lifts the "
        "water to the top? <bookmark mark='b3'/> To find out, go up to a leaf."
    ),
    "s6": (
        "Inside a leaf, the xylem ends near the mesophyll cells. "
        "<bookmark mark='b0'/> Water reaches the mesophyll region. "
        "<bookmark mark='b1'/> From the moist surfaces of these cells, water "
        "evaporates into the air spaces as vapour. <bookmark mark='b2'/> The "
        "vapour moves out through the stomata into the atmosphere. This loss "
        "of water by evaporation from the leaf is called transpiration. "
        "<bookmark mark='b3'/> Molecule after molecule leaves in this way. A "
        "little water also evaporates through the lenticels of the stem. "
        "<bookmark mark='b4'/> So what happens to the water below?"
    ),
    "s7": (
        "Think of the xylem as a tall, narrow tube, completely filled with a "
        "continuous column of water. <bookmark mark='b0'/> At the top, one "
        "water molecule evaporates from the leaf. <bookmark mark='b1'/> The "
        "molecule below moves up to take its place, then the next, then the "
        "next. <bookmark mark='b2'/> The movement passes down the whole "
        "column, and the column moves as one connected stream. <bookmark "
        "mark='b3'/> This pulling effect is the transpiration pull. "
        "<bookmark mark='b4'/> At the bottom, root pressure is a small push. "
        "At the top, transpiration is the main pull. <bookmark mark='b5'/> So "
        "the main pull comes from above, and the push from below is minor and "
        "variable."
    ),
    "s8": (
        "Why does the water column not break? <bookmark mark='b0'/> Because "
        "water molecules attract one another. <bookmark mark='b1'/> So when "
        "the top molecule is pulled, its neighbours follow. The column "
        "stretches a little, but it stays connected. <bookmark mark='b2'/> It "
        "is like drinking through a straw: pull at the top, and the whole "
        "column of water rises. <bookmark mark='b3'/> In the same way, one "
        "continuous pathway <bookmark mark='b4'/> runs from the root, through "
        "the stem, to the leaf."
    ),
    "s9q": (
        "Your turn. Build the water pathway. <bookmark mark='b0'/> A: where "
        "does water enter the plant? <bookmark mark='b1'/> B: which process "
        "helps water enter and move towards the xylem? <bookmark "
        "mark='b2'/> C: which tissue carries water upward? <bookmark "
        "mark='b3'/> D: in a tall tree, which is the main pull, root pressure "
        "or transpiration? <bookmark mark='b4'/> E: put these in order: "
        "xylem, soil, leaf, root hair, atmosphere. Take your time, and pause "
        "the video if you need to."
    ),
    "s9a": (
        "Let us check. <bookmark mark='b0'/> A: the root hair. "
        "<bookmark mark='b1'/> B: osmosis. <bookmark mark='b2'/> C: the "
        "xylem. <bookmark mark='b3'/> D: transpiration pull. <bookmark "
        "mark='b4'/> E: soil, root hair, xylem, leaf, atmosphere. "
        "<bookmark mark='b5'/> Roots push a little, but leaves pull the most."
    ),
    "s10": (
        "Follow one last drop. <bookmark mark='b0'/> It enters a root hair, "
        "<bookmark mark='b1'/> and moves from cell to cell by osmosis. "
        "<bookmark mark='b2'/> It enters the xylem, <bookmark mark='b3'/> "
        "where a small, variable push from root pressure helps from below. "
        "<bookmark mark='b4'/> At the leaf, water evaporates. This is "
        "transpiration, <bookmark mark='b5'/> and it pulls the whole water "
        "column upward. This is the transpiration pull, the main pull. "
        "<bookmark mark='b6'/> Finally, the water vapour leaves into the "
        "atmosphere. <bookmark mark='b7'/> This continuous moving column is "
        "the transpiration stream. <bookmark mark='b8'/> So: roots absorb, "
        "<bookmark mark='b9'/> xylem connects, <bookmark mark='b10'/> leaves "
        "transpire, <bookmark mark='b11'/> and the transpiration pull lifts "
        "the water. <bookmark mark='b12'/> Thank you for watching, "
        "<bookmark mark='b13'/> and see you in the next lesson."
    ),
}


# ------------------------------------------------------------- helpers ------
def chain(labels, colors, size=22, gap=0.10, arrow_len=0.34):
    """Chips joined by arrows:  A -> B -> C."""
    parts = []
    for k, (lb, col) in enumerate(zip(labels, colors)):
        parts.append(chip(lb, col, size))
        if k < len(labels) - 1:
            parts.append(arrow([0, 0, 0], [arrow_len, 0, 0], CHALK_WHITE, 6,
                               0.16))
    row = VGroup(*parts).arrange(RIGHT, buff=gap)
    return row


def trunk_path(tree, x0, ground_y, extra_top=0.0):
    """Points along the centre of the eucalyptus trunk, in board coordinates."""
    s = tree.H / 3.2
    pts = []
    for t in np.linspace(0, 1, 24):
        pts.append([x0 + 0.10 * s * np.sin(t * 3.4), ground_y + t * tree.H, 0])
    pts.append([x0 + 0.10 * s * np.sin(3.4), ground_y + tree.H + extra_top, 0])
    return pts


def glow_path(pts, color=XYL_C, w=5):
    base = VMobject()
    base.set_points_as_corners([np.array(p, dtype=float) for p in pts])
    base.set_stroke(color, w * 2.6, opacity=0.25)
    core = VMobject()
    core.set_points_as_corners([np.array(p, dtype=float) for p in pts])
    core.set_stroke(color, w, opacity=1.0)
    return VGroup(base, core)


def linked(col):
    """Make the links of a water column follow its molecules."""
    links = VGroup(*[Line(a.get_center(), b.get_center(),
                          stroke_color="#E1F5FE", stroke_width=3.2,
                          stroke_opacity=0.9)
                     for a, b in zip(col.mols[:-1], col.mols[1:])])

    def upd(g):
        for ln, a, b in zip(g, col.mols[:-1], col.mols[1:]):
            ln.put_start_and_end_on(a.get_center(), b.get_center())
    links.add_updater(upd)
    return links


class HowWaterReachesTopOfTreeStory(BioScene):
    NARRATION = NARRATION
    TEXT_SCALE = 0.72
    TIGHT_BOXES = True
    STRICT_BOXES = True
    AVOID_ART = True
    BEATS = ("title", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9",
             "s10")

    # ------------------------------------------------------------ title ------
    def beat_title(self):
        with self.narrate("title") as tr:
            main = P(T("How Water Reaches", 56, CHALK_AMBER, max_w=8.6), CX, 0.95)
            main2 = P(T("the Top of a Tree", 56, CHALK_AMBER, max_w=8.6), CX,
                      0.20)
            rule = Line([CX - 3.0, -0.38, 0], [CX + 3.0, -0.38, 0],
                        stroke_color=CHALK_GREEN, stroke_width=4)
            sub = P(T("Xylem, Root Pressure & Transpiration Pull", 30,
                      CHALK_WHITE, max_w=8.6), CX, -0.86)
            self.show(VGroup(main, main2), rt=0.7)
            self.cue(tr, "b0", rule, sub, sfx="ding", rt=0.7)
            self.finish(tr)

    # ------------------------------------------------------------ scene 1 ----
    def beat_s1(self):
        with self.narrate("s1") as tr:
            self.heading("The 180-Metre Problem")
            gy = -2.02
            tree_x = -0.80
            tr_ = eucalyptus(3.9)
            tr_.move_to([tree_x, gy, 0], aligned_edge=DOWN)
            tr_.shift(RIGHT * (tree_x - tr_.trunk.get_center()[0]))
            soil = soil_with_roots(3.0, 0.62)
            soil.move_to([tree_x, gy - 0.31, 0])
            from human_figure import Man
            man = Man(base=[0, 0, 0], height=0.22, facing=RIGHT, shirt="#4F8EF7")
            man.move_to([tree_x + 0.72, gy + 0.13, 0])
            man_l = P(T("a person (not to scale)", 18, CHALK_WHITE),
                      tree_x + 2.0, gy + 0.30)
            top_y = gy + 3.9
            rx = -2.60
            ruler = Line([rx, gy, 0], [rx, top_y, 0], stroke_color=CHALK_WHITE,
                         stroke_width=3)
            marks = []
            for m, col in ((20, CHALK_CYAN), (60, CHALK_GREEN),
                           (100, CHALK_AMBER), (180, CHALK_YELLOW)):
                y = gy + 3.9 * m / 180.0
                tick = Line([rx - 0.14, y, 0], [rx + 0.14, y, 0],
                            stroke_color=col, stroke_width=5)
                lab = chip(f"{m} m", col, 24)
                lab.move_to([rx - 0.95, y, 0])
                lead = DashedLine([rx + 0.14, y, 0],
                                  [tree_x - 0.05, y, 0], stroke_color=col,
                                  stroke_width=2, stroke_opacity=0.6,
                                  dash_length=0.08)
                marks.append(VGroup(tick, lab, lead))
            self.add(soil, tr_)
            c0 = P(fm(r"0\,\mathrm{m}", CHALK_WHITE, 60, w=2.6), 3.05, 1.15)
            drop = small_drop(0.12).move_to([tree_x + 0.55, gy - 0.34, 0])
            q = tcard("", ["HOW CAN THIS DROP", "REACH A LEAF 180 m", "ABOVE THE GROUND?"],
                      CHALK_PINK, w=3.2, body_size=30, pad=0.18, gap=0.10)
            P(q, 3.10, -0.35)
            self.cue(tr, "b0", FadeIn(man), FadeIn(man_l), FadeIn(ruler),
                     FadeIn(c0), sfx="pop")
            for k, (mk, val) in enumerate(zip(marks, (20, 60, 100, 180))):
                nc = P(fm(rf"{val}\,\mathrm{{m}}", CHALK_WHITE if val < 180
                          else CHALK_YELLOW, 60, w=2.6), 3.05, 1.15)
                self.cue(tr, f"b{k + 1}", FadeIn(mk), ReplacementTransform(c0, nc),
                         sfx="click" if k < 3 else "ding")
                c0 = nc
            self.cue(tr, "b5", FadeIn(drop, scale=1.6), FadeIn(q), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 2 ----
    def beat_s2(self):
        with self.narrate("s2") as tr:
            self.heading("The First Gate: Root Hairs")
            view = root_hair_view(5.0, 2.9)
            P(view, -1.55, 0.50)
            vc = view.get_center()
            hair = view.hairs[2]
            off = view.get_center()
            htip = hair.tip + off
            hroot = hair.root + off
            ring = Circle(radius=0.30, stroke_color=CHALK_YELLOW, stroke_width=4,
                          fill_opacity=0).move_to(htip + LEFT * 0.40)
            c_hair = chip("ROOT HAIR", CHALK_YELLOW, 28)
            P(c_hair, 3.55, 1.55)
            lead = arrow(c_hair.get_left() + LEFT * 0.03, htip + RIGHT * 0.12 + UP * 0.12,
                         CHALK_YELLOW, 4, 0.16)
            c_in = tcard("", ["WATER ENTERS", "THE PLANT HERE"], CHALK_GREEN,
                         w=2.8, body_size=26, pad=0.14, gap=0.06)
            P(c_in, 3.55, 0.65)
            c_big = tcard("", ["SMALL STRUCTURES,", "HUGE ABSORBING", "REGION"],
                          CHALK_CYAN, w=2.8, body_size=24, pad=0.14, gap=0.06)
            P(c_big, 3.55, -0.50)
            c_q = chip("HOW DOES WATER MOVE IN?", CHALK_PINK, 26)
            c_os = chip("OSMOSIS", CHALK_YELLOW, 40)
            VGroup(c_q, c_os).arrange(DOWN, buff=0.18)
            P(VGroup(c_q, c_os), CX - 0.2, -1.95)
            ndrop = min(view.drops, key=lambda d: np.linalg.norm(
                d.get_center() - (htip + RIGHT * 0.9 + UP * 0.1)))
            jd = small_drop(0.11).move_to(ndrop.get_center())
            self.cue(tr, "b0", FadeIn(view), sfx="pop")
            self.cue(tr, "b1", FadeIn(ring), FadeIn(c_hair), FadeIn(lead),
                     sfx="click")
            self.cue(tr, "b2", *[Indicate(d, color=CHALK_YELLOW,
                                          scale_factor=1.6) for d in view.drops],
                     FadeIn(jd), sfx="click")
            self.cue(tr, "b3", jd.animate.move_to(htip), FadeIn(c_in),
                     sfx="whoosh", rt=0.9)
            self.go(jd.animate.move_to(hroot + RIGHT * 0.35), rt=0.9)
            self.cue(tr, "b4", FadeIn(c_big), sfx="click")
            self.cue(tr, "b5", FadeIn(c_q), FadeIn(c_os), sfx="ding")
            self.finish(tr)

    # ------------------------------------------------------------ scene 3 ----
    def beat_s3(self):
        with self.narrate("s3") as tr:
            self.heading("From Root Hair to Xylem")
            ry = 0.60
            B = 1.20                       # every block is B x B
            xs = [-3.55 + 1.52 * k for k in range(6)]

            # 1 soil
            soil = RoundedRectangle(corner_radius=0.10, width=B, height=B)
            paint(soil, ["#5D4037", "#3E2723"], op=1, lw=2.2, sheen=0.0,
                  line="#2B1B14")
            sgr = soil_grains(B - 0.2, B - 0.2, n=5, seed=6, r=(0.07, 0.11))
            sd = VGroup(*[small_drop(0.06).move_to(np.array(p)) for p in
                          ([-0.28, 0.30, 0], [0.30, -0.28, 0], [0.1, 0.38, 0])])
            b_soil = VGroup(soil, sgr, sd).move_to([xs[0], ry, 0])
            # 2 root hair
            hbox = RoundedRectangle(corner_radius=0.10, width=B, height=B)
            hbox.set_fill("#16202B", 0.5).set_stroke("#8D6E63", 1.6)
            hcell = RoundedRectangle(corner_radius=0.24, width=0.52, height=B - 0.18)
            paint(hcell, ["#FFF3E0", "#FFE0B2"], lw=2.4, sheen=0.3,
                  line="#8D6E63")
            hdots = VGroup(*[Dot(radius=0.04, color="#CE93D8").move_to(
                np.array([dx, dy, 0])) for dx, dy in
                ((-0.10, 0.35), (0.08, 0.2), (-0.06, 0.05), (0.10, -0.1),
                 (-0.08, -0.25), (0.05, -0.38), (0.0, 0.46))])
            b_hair = VGroup(hbox, hcell, hdots).move_to([xs[1], ry, 0])
            # 3-5 root cells
            b_cells = [root_cell(B - 0.08, B - 0.08).move_to([xs[k], ry, 0])
                       for k in (2, 3, 4)]
            # 6 xylem
            xtube = xylem_tube(B + 0.1, 0.46)
            xbox = RoundedRectangle(corner_radius=0.10, width=B, height=B)
            xbox.set_fill("#16202B", 0.5).set_stroke("#1565C0", 1.6)
            b_xyl = VGroup(xbox, xtube).move_to([xs[5], ry, 0])
            blocks = VGroup(b_soil, b_hair, *b_cells, b_xyl)

            # the same arrow between every pair of neighbours
            conn = [arrow([x + B / 2 + 0.06, ry, 0], [x + B / 2 + 0.06 + 0.26, ry, 0],
                          WATER_C, 6, 0.16) for x in xs[:-1]]

            lab_y = ry + B / 2 + 0.26
            names = [("SOIL", SOIL_C, xs[0]), ("ROOT HAIR", CHALK_YELLOW, xs[1]),
                     ("ROOT CELLS", CHALK_GREEN, xs[3]), ("XYLEM", XYL_C, xs[5])]
            labs = VGroup(*[T(n, 20, c).move_to([x, lab_y, 0])
                            for n, c, x in names])
            osm = P(tag_label("OSMOSIS", CHALK_YELLOW, 22),
                    (xs[0] + xs[1]) / 2, lab_y + 0.52)
            dil = P(chip("DILUTE", CHALK_CYAN, 20), xs[0], ry - B / 2 - 0.34)
            con = P(chip("CONCENTRATED", "#CE93D8", 20), xs[1] + 0.35,
                    ry - B / 2 - 0.34)
            xl = P(tag_label("XYLEM VESSEL", XYL_C, 20), xs[5] - 0.1,
                   ry - B / 2 - 0.34)
            jd = small_drop(0.10).move_to([xs[0], ry, 0])
            ch = chain(["SOIL", "ROOT HAIR", "ROOT CELLS", "XYLEM"],
                       [SOIL_C, CHALK_YELLOW, CHALK_GREEN, XYL_C], 20)
            P(ch, CX - 0.1, -2.05)
            many = tag_label("MANY ROOT HAIRS FEED MANY XYLEM PATHWAYS", CHALK_CYAN,
                             18)
            P(many, CX - 0.1, -1.38)
            self.cue(tr, "b0", FadeIn(blocks), FadeIn(labs), sfx="pop")
            self.cue(tr, "b1", FadeIn(dil), FadeIn(con), sfx="click")
            self.cue(tr, "b2", FadeIn(jd), FadeIn(osm), FadeIn(conn[0]),
                     sfx="whoosh")
            self.go(jd.animate.move_to([xs[1], ry, 0]), rt=0.8)
            self.cue(tr, "b3", FadeIn(conn[1]), jd.animate.move_to([xs[2], ry, 0]),
                     sfx="click", rt=0.8)
            self.go(FadeIn(conn[2]), jd.animate.move_to([xs[3], ry, 0]), rt=0.8)
            self.go(FadeIn(conn[3]), jd.animate.move_to([xs[4], ry, 0]), rt=0.8)
            self.cue(tr, "b4", FadeIn(conn[4]), jd.animate.move_to([xs[5], ry, 0]),
                     FadeIn(xl), sfx="ding", rt=0.9)
            self.cue(tr, "b5", FadeIn(many), FadeIn(ch), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 4 ----
    def beat_s4(self):
        with self.narrate("s4") as tr:
            self.heading("Root Pressure: a Push from Below")
            lx, ly = -1.75, 0.50
            boxL = panel(4.2, 3.1, CHALK_CYAN)
            P(boxL, lx, ly)
            rv = root_side_view(2.45)
            rv.move_to([lx - 0.65, ly + 0.16, 0])
            tube = rv.tube
            col = water_column(1.0, 6)
            col.move_to([tube.get_center()[0], tube.get_bottom()[1] + 0.05 + 0.5, 0])
            off = rv.get_center()
            drops = VGroup(*[small_drop(0.075).move_to(pt + off + d * 0.12)
                             for pt, d in rv.hair_tips[2::3]])
            capL = T("ROOT AND ITS XYLEM", 22, CHALK_CYAN)
            capL.move_to([lx, ly - 1.33, 0])
            cardL = VGroup(boxL, rv, col, drops, capL)
            ax = lx + 1.45
            push = arrow([ax, ly - 0.65, 0], [ax, ly + 0.40, 0], PUSH_C, 8, 0.26)
            rp = lines(["ROOT", "PRESSURE"], 20, PUSH_C, buff=0.05)
            rp.move_to([ax, ly + 0.95, 0])

            rx, ry = 2.70, 0.50
            boxR = panel(3.4, 3.1, CHALK_AMBER)
            P(boxR, rx, ry)
            app = pot_apparatus()
            fit(app, 2.2, 2.45)
            app.move_to([rx - 0.25, ry + 0.16, 0])
            capR = T("ACTIVITY: M1 TO M2", 22, CHALK_AMBER)
            capR.move_to([rx, ry - 1.33, 0])
            cardR = VGroup(boxR, app, capR)
            lvl1 = app.lvl1
            lvl2 = lvl1.copy()
            lvl2.stretch_to_fit_height(lvl1.height * 1.0 +
                                       (app.m2y - app.m1y) * (lvl1.height /
                                                              (app.m1y - app.y0)))
            lvl2.align_to(lvl1, DOWN)
            strip = P(chip("A PUSH, NOT THE MAIN FORCE", CHALK_YELLOW, 26),
                      CX + 0.1, -1.72)
            self.cue(tr, "b0", FadeIn(cardL), sfx="pop")
            self.cue(tr, "b1", FadeIn(push), FadeIn(rp),
                     col.animate.shift(UP * 0.30),
                     *[d.animate.shift(0.18 * (-1 if d.get_center()[0] > rv.get_center()[0]
                                               else 1) * RIGHT) for d in drops],
                     sfx="click", rt=1.0)
            self.cue(tr, "b2", FadeIn(cardR), sfx="click")
            self.go(Transform(lvl1, lvl2), rt=1.3)
            self.cue(tr, "b3", push.animate.scale(0.6).set_opacity(0.85),
                     FadeIn(strip), sfx="click")
            self.finish(tr)

    # ------------------------------------------------------------ scene 5 ----
    def beat_s5(self):
        with self.narrate("s5") as tr:
            self.heading("Why Root Pressure Is Not Enough")
            gy = -2.12
            tx = -1.45
            tree = eucalyptus(4.05)
            tree.move_to([tx, gy, 0], aligned_edge=DOWN)
            tree.shift(RIGHT * (tx - tree.trunk.get_center()[0]))
            soil = soil_with_roots(2.6, 0.62)
            soil.move_to([tx, gy - 0.31, 0])
            path = glow_path(trunk_path(tree, tx, gy, 0.0), XYL_C, 4)
            hl = VGroup(DoubleArrow([tx - 1.35, gy, 0], [tx - 1.35, gy + 3.9, 0],
                                    buff=0, stroke_width=3, color=CHALK_WHITE,
                                    tip_length=0.16),
                        T("180 m", 22, CHALK_WHITE).move_to([tx - 1.95, gy + 1.95, 0]))
            sm = arrow([tx + 0.60, gy + 0.05, 0], [tx + 0.60, gy + 0.75, 0],
                       PUSH_C, 8, 0.24)
            sm_l = P(tag_label("ROOT PRESSURE: SMALL", PUSH_C, 20), tx + 2.30,
                     gy + 0.45)
            w1 = tcard("", ["ROOT PRESSURE", "IS SELDOM HIGH"], CHALK_AMBER,
                       w=3.1, body_size=26, pad=0.14, gap=0.06)
            w2 = tcard("", ["SOMETIMES IT", "MAY BE NIL"], CHALK_AMBER, w=3.1,
                       body_size=26, pad=0.14, gap=0.06)
            VGroup(w1, w2).arrange(DOWN, buff=0.22)
            P(VGroup(w1, w2), 3.35, 1.0)
            q = tcard("", ["THEN WHAT LIFTS", "WATER TO THE TOP?"], CHALK_PINK,
                      w=3.1, body_size=28, pad=0.16, gap=0.06)
            P(q, 3.35, -0.55)
            self.add(soil)
            self.cue(tr, "b0", FadeIn(tree), FadeIn(path), FadeIn(hl), sfx="pop")
            self.cue(tr, "b1", FadeIn(sm), FadeIn(sm_l), sfx="click")
            self.cue(tr, "b2", FadeIn(w1), sfx="click")
            self.cue(tr, "b2", FadeIn(w2), sfx=None)
            self.cue(tr, "b3", FadeIn(q), sfx="ding")
            self.finish(tr)

    # ------------------------------------------------------------ scene 6 ----
    def beat_s6(self):
        with self.narrate("s6") as tr:
            self.heading("The Leaf Loses Water")
            leaf_ = leaf_section(5.2, 2.7)
            P(leaf_, 0.45, 0.80)
            o = leaf_.get_center()
            xyl = o + leaf_.xyl
            stoma = o + leaf_.stoma
            airs = [o + p for p in leaf_.air]
            cells = leaf_.cells

            def callout(txt, col, lab_pos, target):
                lab = tag_label(txt, col, 20)
                lab.move_to(lab_pos)
                side_right = target[0] > lab_pos[0]
                start = lab.get_right() if side_right else lab.get_left()
                ln = Line(start, target, stroke_color=col, stroke_width=2.4)
                dt = Dot(target, radius=0.05, color=col)
                return VGroup(lab, ln, dt)
            c_x = callout("XYLEM", XYL_C, [-3.60, xyl[1] - 0.30, 0],
                          xyl + LEFT * 0.17)
            c_m = callout("MESOPHYLL", GREEN_C, [-3.38, xyl[1] + 0.50, 0],
                          cells[0].get_center() + LEFT * 0.12 + UP * 0.12)
            c_a = callout("AIR SPACE", CHALK_CYAN, [4.30, airs[1][1] + 0.38, 0],
                          airs[1] + RIGHT * 0.10)
            c_s = callout("STOMA", CHALK_AMBER, [4.30, stoma[1] + 0.02, 0],
                          stoma + RIGHT * 0.20)
            films = VGroup(*[c[0].copy().set_fill(opacity=0).set_stroke(
                XYL_C, 2.6, opacity=0.95) for c in (cells[0], cells[6])])
            xring = Circle(radius=0.23, stroke_color=XYL_C, stroke_width=4,
                           fill_opacity=0).move_to(xyl)
            vs = VGroup(*[vapour_dot().move_to(p) for p in airs[:3]])
            outs = VGroup(*[vapour_dot().move_to(stoma + np.array([dx, -0.32 - 0.20 * k,
                                                                   0]))
                            for k, dx in enumerate((-0.08, 0.10, -0.03))])
            zone = RoundedRectangle(corner_radius=0.12, width=5.2, height=0.78)
            zone.set_fill("#B3E5FC", 0.10).set_stroke("#81D4FA", 1.8, opacity=0.6)
            zone.move_to([o[0], o[1] - 1.35 - 0.39, 0])
            atm = T("ATMOSPHERE", 18, CHALK_CYAN)
            atm.move_to([zone.get_right()[0] - 0.74, zone.get_center()[1], 0])
            tp = tag_label("TRANSPIRATION", CHALK_YELLOW, 20)
            tp.move_to([stoma[0] - 1.50, zone.get_center()[1], 0])
            lent = P(tag_label("LENTICELS OF THE STEM LOSE A LITTLE WATER TOO",
                               CHALK_AMBER, 18), CX - 0.1, -1.86)
            qn = P(chip("WHAT HAPPENS TO THE WATER BELOW?", CHALK_PINK, 24),
                   CX - 0.1, -2.42)
            more = VGroup(*[vapour_dot().move_to(stoma + np.array([dx, -0.34 - dy,
                                                                  0]))
                            for dx, dy in ((0.22, 0.0), (-0.24, 0.04),
                                           (0.06, 0.30))])
            self.add(zone, atm)
            self.cue(tr, "b0", FadeIn(leaf_), FadeIn(c_m), FadeIn(c_x), sfx="pop")
            self.cue(tr, "b1", FadeIn(films), FadeIn(xring), sfx="click")
            self.cue(tr, "b2", FadeIn(vs), FadeIn(c_a), sfx="click")
            self.cue(tr, "b3", FadeIn(outs), FadeIn(c_s), FadeIn(tp), sfx="ding")
            self.cue(tr, "b4", FadeIn(more), FadeIn(lent), FadeIn(qn),
                     sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 7 ----
    def beat_s7(self):
        with self.narrate("s7") as tr:
            self.heading("Transpiration Pull")
            tx = -2.3
            tube = xylem_tube(3.0, 0.50)
            tube.move_to([tx, 0.10, 0])
            col = water_column(2.7, 13)
            col.move_to(tube.get_center())
            links = linked(col)
            dy = col.mols[1].get_center()[1] - col.mols[0].get_center()[1]
            l_top = P(tag_label("LEAF END", GREEN_C, 20), tx, 1.95)
            l_bot = P(tag_label("ROOT END", CHALK_AMBER, 20), tx, -1.70)
            vap = vapour_dot().move_to(col.mols[-1].get_center())
            evap = tag_label("EVAPORATION", CHALK_CYAN, 20)
            evap.move_to([tx + 2.0, 1.95, 0])
            pull = arrow([tx + 1.0, -0.20, 0], [tx + 1.0, 1.62, 0], PULL_C, 14,
                         0.42)
            pull_l = tag_label("TRANSPIRATION PULL", PULL_C, 22)
            pull_l.move_to([tx + 2.75, 0.75, 0])
            push = arrow([tx + 1.0, -1.35, 0], [tx + 1.0, -0.95, 0], PUSH_C, 6,
                         0.2)
            push_l = tag_label("ROOT PRESSURE", PUSH_C, 20)
            push_l.move_to([tx + 2.55, -1.20, 0])
            mp = tcard("", ["MAIN PULL", "FROM ABOVE"], PULL_C, w=2.7,
                       body_size=26, pad=0.14, gap=0.06)
            mn = tcard("", ["MINOR, VARIABLE", "PUSH FROM BELOW"], PUSH_C, w=2.7,
                       body_size=22, pad=0.14, gap=0.06)
            VGroup(mp, mn).arrange(DOWN, buff=0.28)
            P(VGroup(mp, mn), 3.85, 0.30)
            self.cue(tr, "b0", FadeIn(tube), FadeIn(col), FadeIn(links),
                     FadeIn(l_top), FadeIn(l_bot), sfx="pop")
            top = col.mols[-1]
            first_link = links[-1]
            self.cue(tr, "b1", FadeIn(vap), FadeIn(evap), sfx="click")
            links.remove(first_link)
            others = col.mols[:-1]
            self.go(vap.animate.shift(UP * 0.28 + RIGHT * 0.45).set_opacity(0.0),
                    top.animate.shift(UP * 0.28 + RIGHT * 0.45).set_opacity(0.0),
                    FadeOut(first_link), rt=0.7)
            self.cue(tr, "b2", LaggedStart(*[m.animate.shift(UP * dy)
                                             for m in others[::-1]],
                                           lag_ratio=0.12), sfx="whoosh", rt=2.0)
            self.cue(tr, "b3", *[Indicate(m, color=CHALK_YELLOW, scale_factor=1.35)
                                 for m in others[::2]], sfx="click", rt=0.8)
            self.cue(tr, "b4", FadeIn(pull), FadeIn(pull_l), sfx="ding")
            self.cue(tr, "b5", FadeIn(push), FadeIn(push_l), FadeIn(mp),
                     FadeIn(mn), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 8 ----
    def beat_s8(self):
        with self.narrate("s8") as tr:
            self.heading("Why the Water Column Does Not Break")
            tube = xylem_tube(2.1, 0.50)
            col = water_column(1.85, 9)
            col.move_to(tube.get_center())
            links = linked(col)
            pic = VGroup(tube, col, links)
            cardL = pic_card(pic, "CONTINUOUS COLUMN", CHALK_CYAN, w=3.5, h=3.0,
                             pic_w=2.5, pic_h=2.2, cap_size=24)
            P(cardL, -1.95, 0.55)
            sg = straw_glass(2.1)
            cardR = pic_card(sg, "LIKE A STRAW", CHALK_AMBER, w=3.5, h=3.0,
                             pic_w=2.5, pic_h=2.2, cap_size=24)
            P(cardR, 2.2, 0.55)
            attract = P(chip("WATER MOLECULES ATTRACT ONE ANOTHER", CHALK_YELLOW,
                             24), CX + 0.1, -1.32)
            ch = chain(["ROOT", "STEM", "LEAF"], [CHALK_AMBER, GREEN_C,
                                                   CHALK_GREEN], 24)
            P(ch, CX + 0.1, -2.12)
            up = arrow(cardR.box.get_center() + np.array([0.95, -0.2, 0]),
                       cardR.box.get_center() + np.array([0.95, 0.55, 0]),
                       PULL_C, 7, 0.22)
            top3 = col.mols[-3:]
            self.cue(tr, "b0", FadeIn(cardL), sfx="pop")
            self.cue(tr, "b1", FadeIn(attract), sfx="ding")
            self.cue(tr, "b2", LaggedStart(*[m.animate.shift(UP * 0.07)
                                             for m in col.mols[::-1]],
                                           lag_ratio=0.1), sfx="click", rt=1.2)
            self.cue(tr, "b3", FadeIn(cardR), FadeIn(up), sfx="click")
            self.cue(tr, "b4", FadeIn(ch), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 9 ----
    def beat_s9(self):
        with self.narrate("s9q") as tr:
            self.heading("YOUR TURN", "Build the water pathway.", CHALK_PINK)
            specs = [("A", "Where does water enter the plant?", "?", CHALK_YELLOW),
                     ("B", "What moves water towards the xylem?", "?",
                      CHALK_CYAN),
                     ("C", "Which tissue carries water up?", "?", XYL_C),
                     ("D", "Main pull: root pressure or ...?", "?", PULL_C),
                     ("E", "Order: xylem, soil, leaf, root hair, air", "?",
                      CHALK_GREEN)]
            rows = [qa_row(l, q, a, c, w=8.3, h=0.60, size=26)
                    for l, q, a, c in specs]
            ys = (1.30, 0.55, -0.20, -0.95, -1.70)
            for r_, y in zip(rows, ys):
                P(r_, CX + 0.05, y)
            for k, r_ in enumerate(rows):
                self.cue(tr, f"b{k}", FadeIn(r_), sfx="pop" if k == 0 else "click")
            self.finish(tr)
            self._rows = rows
        self.think_clock()
        with self.narrate("s9a", reset=False) as tr:
            answers = ["ROOT HAIR", "OSMOSIS", "XYLEM", "TRANSPIRATION PULL"]
            rows = self._rows
            for k in range(4):
                new = T(answers[k], 26, specs[k][3], max_w=3.0)
                new.move_to(rows[k].slot.get_center())
                new.align_to(rows[k].slot, RIGHT)
                self.cue(tr, f"b{k}", ReplacementTransform(rows[k].slot, new),
                         sfx="click", rt=0.5)
            chE = chain(["SOIL", "ROOT HAIR", "XYLEM", "LEAF", "ATMOSPHERE"],
                        [SOIL_C, CHALK_YELLOW, XYL_C, GREEN_C, CHALK_WHITE], 20)
            fit(chE, 7.8)
            P(chE, CX + 0.05, -1.70)
            self.cue(tr, "b4", FadeOut(rows[4]), FadeIn(chE), sfx="click",
                     rt=0.6)
            strip = P(chip("ROOTS PUSH A LITTLE, LEAVES PULL THE MOST",
                           CHALK_YELLOW, 24), CX + 0.1, -2.38)
            self.cue(tr, "b5", FadeIn(strip), sfx="success")
            self.finish(tr)

    # ----------------------------------------------------------- scene 10 ----
    def beat_s10(self):
        with self.narrate("s10") as tr:
            head = self.heading("One Drop's Complete Journey")
            gy = -2.05
            tx = -1.55
            tree = eucalyptus(3.9)
            tree.move_to([tx, gy, 0], aligned_edge=DOWN)
            tree.shift(RIGHT * (tx - tree.trunk.get_center()[0]))
            soil = soil_with_roots(2.6, 0.62)
            soil.move_to([tx, gy - 0.31, 0])
            pts = trunk_path(tree, tx, gy, 0.3)
            full = glow_path(pts, XYL_C, 4)
            self.add(soil, tree)
            drop = small_drop(0.12).move_to([tx + 0.45, gy - 0.18, 0])
            idx = lambda f: pts[int(f * (len(pts) - 1))]

            def chp(txt, col):
                c_ = chip(txt, col, 20, w=3.1, h=0.46)
                c_._tight = True
                return c_
            rows = [chp("ROOT HAIR", CHALK_YELLOW),
                    chp("OSMOSIS", CHALK_CYAN),
                    chp("XYLEM", XYL_C),
                    chp("ROOT PRESSURE: small push", PUSH_C),
                    chp("TRANSPIRATION", CHALK_GREEN),
                    chp("TRANSPIRATION PULL: main", PULL_C),
                    chp("VAPOUR TO ATMOSPHERE", VAP_C),
                    chp("TRANSPIRATION STREAM", CHALK_YELLOW)]
            for k, r_ in enumerate(rows):
                P(r_, 3.05, 1.80 - k * 0.60)
            sm = arrow([tx + 0.55, gy + 0.05, 0], [tx + 0.55, gy + 0.5, 0], PUSH_C,
                       6, 0.18)
            vp = [vapour_dot().move_to(np.array(pts[-1]) + np.array(
                [0.5 + 0.2 * k, 0.2 + 0.15 * k, 0])) for k in range(3)]
            vps = VGroup(*vp)
            big = arrow([tx + 0.75, gy + 1.5, 0], [tx + 0.75, gy + 3.2, 0],
                        PULL_C, 10, 0.34)
            msgs = [("ROOTS ABSORB", CHALK_YELLOW), ("XYLEM CONNECTS", XYL_C),
                    ("LEAVES TRANSPIRE", CHALK_GREEN),
                    ("TRANSPIRATION PULL LIFTS THE WATER", PULL_C)]
            cards = []
            for k, (m, c) in enumerate(msgs):
                words = m.split(" ")
                if len(words) > 2:
                    lines_ = [" ".join(words[:2]), " ".join(words[2:])]
                else:
                    lines_ = [m]
                cards.append(tcard("", lines_, c, w=3.4, body_size=28, pad=0.14,
                                   gap=0.06))
            for k, c in enumerate(cards):
                P(c, 3.3, 1.55 - k * 1.05)
            thanks = P(T("Thank You for Watching!", 52, CHALK_WHITE, max_w=9.4),
                       CX, 0.55)
            bye = P(T("See you in the next lesson :)", 38, CHALK_YELLOW,
                      max_w=9.0), CX, -0.65)
            self.cue(tr, "b0", FadeIn(drop, scale=1.6), sfx="pop")
            self.cue(tr, "b1", rows[0].animate.set_opacity(1.0) if False else
                     FadeIn(rows[0]), drop.animate.move_to([tx + 0.12, gy - 0.05,
                                                            0]), sfx="click")
            self.cue(tr, "b2", FadeIn(rows[1]), sfx="click")
            self.cue(tr, "b3", FadeIn(rows[2]), drop.animate.move_to(idx(0.12)),
                     Create(full), sfx="click")
            self.cue(tr, "b4", FadeIn(rows[3]), FadeIn(sm), sfx="click")
            self.cue(tr, "b5", FadeIn(rows[4]), drop.animate.move_to(idx(1.0)),
                     sfx="whoosh", rt=1.2)
            self.cue(tr, "b6", FadeIn(rows[5]), FadeIn(big),
                     Indicate(full, color=PULL_C, scale_factor=1.0), sfx="ding")
            self.cue(tr, "b7", FadeIn(rows[6]), FadeIn(vps), sfx="click")
            self.cue(tr, "b8", FadeIn(rows[7]), sfx="ding", snap="chips")
            self.cue(tr, "b9", *[FadeOut(r_) for r_ in rows], FadeIn(cards[0]),
                     sfx="pop")
            self.cue(tr, "b10", FadeIn(cards[1]), sfx="click")
            self.cue(tr, "b11", FadeIn(cards[2]), FadeIn(cards[3]), sfx="success")
            self.hold(tr, "b12")
            keep = [m for m in self.mobjects if m not in self.fixtures]
            self.go(*[FadeOut(m) for m in keep], rt=0.6)
            self.cue(tr, "b12", FadeIn(thanks, shift=UP * 0.1), sfx=None)
            self.cue(tr, "b13", FadeIn(bye, shift=UP * 0.1), sfx=None)
            self.finish(tr)
        if not self.still:
            self.wait(END_HOLD)

"""
Photosynthesis Explained: Inputs, Process & Outputs in One Visual Flow
Story-mode chalkboard lesson (Class 10 Biology, Chapter 1: Nutrition,
Storymode 01).

LLM KEY / FUNCTION NAME: photosynthesis_inputs_outputs_visual_flow

Production rules (the series' rules, carried over from the Class 8 videos):
  - every object sits inside the green board; medium type (TEXT_SCALE 0.85);
    every box hugs its text; boxes keep a small gap; nothing sits on the
    teacher, the students or the corner badges (AVOID_ART);
  - each picture appears exactly when the voice reaches its bookmark;
  - realistic shaded diagrams (bio_art): lit leaves with veins, a root cut-away,
    a glowing Sun, shaded atoms, a plant cell with chloroplasts and grana,
    a skeletal glucose ring.

Corrections made to the draft storyboard:
  * the textbook equation is kept exactly, and the NET equation
    6CO2 + 6H2O -> C6H12O6 + 6O2 is added after it, so students see that water
    on both sides means six molecules are used overall;
  * the student challenge uses the series' ten-second THINK clock instead of
    five four-second pauses (too short to answer);
  * the zoom (leaf -> cell -> chloroplast) is a three-stage ladder shown on one
    board, so the persistent-diagram idea survives at 16:9;
  * chlorophyll is drawn INSIDE the leaf / chloroplast and never flies in like
    water or carbon dioxide.

Scenes:
  1. Plants do not eat a plate of food -- where does it come from?
  2. Four requirements: water (soil), carbon dioxide (air), light (Sun),
     chlorophyll (green parts).
  3. Materials vs energy vs pigment.
  4. Leaf -> cell -> chloroplast: the site.
  5. Glucose, made by a series of reactions.
  6. Oxygen returns to the air; IN and OUT.
  7. The equation, read as a story, then in symbols.
  8. Glucose -> starch and cellulose.
  9. Your turn: complete the map (THINK clock, answers).
 10. The whole story, the bridge to Video 2, and the thank-you.
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

NARRATION = {
    "title": (
        "Photosynthesis. <bookmark mark='b0'/> Inputs, process and outputs, "
        "in one visual flow."
    ),
    "s1": (
        "A person eats a plate of food. That is how an animal gets its food: "
        "from outside. <bookmark mark='b0'/> Now try the same with a plant. "
        "Nobody puts a plate of food in front of it. <bookmark mark='b1'/> And "
        "yet the plant keeps growing. New leaves open, and fruits form. "
        "<bookmark mark='b2'/> So where does a plant's food come from? "
        "<bookmark mark='b3'/> The answer begins in one green leaf. The leaf "
        "can help make it."
    ),
    "s2": (
        "What does photosynthesis need? Four things. <bookmark mark='b0'/> "
        "Water comes from the soil, and the roots carry it up to the leaf. "
        "<bookmark mark='b1'/> Carbon dioxide comes from the air around the "
        "leaf. <bookmark mark='b2'/> Light energy comes from the Sun. "
        "<bookmark mark='b3'/> And chlorophyll, the green pigment, is already "
        "inside the green parts of the plant. <bookmark mark='b4'/> Water, "
        "carbon dioxide, light and chlorophyll: these are the four "
        "requirements."
    ),
    "s3": (
        "But the four do not play the same role. <bookmark mark='b0'/> "
        "Carbon dioxide and water are the chemical materials. They are the "
        "matter that gets used. <bookmark mark='b1'/> Light is the energy "
        "source. It supplies energy, but it does not become part of the food. "
        "<bookmark mark='b2'/> Chlorophyll is the light-capturing pigment. It "
        "helps to catch the light, and it is not used up like water. "
        "<bookmark mark='b3'/> Materials, energy and pigment work together in "
        "photosynthesis. <bookmark mark='b4'/> So needed for the process does "
        "not mean consumed in the same way."
    ),
    "s4": (
        "Where does all this happen? Zoom into a leaf. <bookmark mark='b0'/> "
        "Inside it are cells, and each green cell holds many small green "
        "bodies. <bookmark mark='b1'/> One of them is a chloroplast. "
        "<bookmark mark='b2'/> The chloroplast is the site of photosynthesis. "
        "<bookmark mark='b3'/> Carbon dioxide, water and light all meet "
        "here. <bookmark mark='b4'/> We will open the chloroplast in the next "
        "video."
    ),
    "s5": (
        "Now, what does the chloroplast make? <bookmark mark='b0'/> Carbon "
        "dioxide enters from the air. <bookmark mark='b1'/> Water arrives "
        "from the soil. <bookmark mark='b2'/> Light energy switches the "
        "chloroplast on. <bookmark mark='b3'/> Inside, it is not one step. A "
        "series of reactions takes place, with several intermediate "
        "compounds. <bookmark mark='b4'/> The main product is glucose, a "
        "carbohydrate. <bookmark mark='b5'/> The light energy is now stored in "
        "it as chemical energy."
    ),
    "s6": (
        "Photosynthesis also gives out a gas. <bookmark mark='b0'/> Oxygen "
        "forms inside the chloroplast. <bookmark mark='b1'/> It leaves the "
        "cell, <bookmark mark='b2'/> and then the leaf, <bookmark mark='b3'/> "
        "and goes out into the air. <bookmark mark='b4'/> So, in: carbon "
        "dioxide and water, with light. Out: glucose and oxygen. "
        "<bookmark mark='b5'/> The purpose is food. Oxygen is an important "
        "product that is released along the way."
    ),
    "s7": (
        "Now let us read the equation as a story. <bookmark mark='b0'/> In "
        "words: carbon dioxide plus water, with light and chlorophyll, gives "
        "glucose, water and oxygen. <bookmark mark='b1'/> Carbon dioxide is "
        "C O two. <bookmark mark='b2'/> Water is H two O, and glucose is C six "
        "H twelve O six. <bookmark mark='b3'/> Now the numbers. The textbook "
        "equation is: six C O two plus twelve H two O, in light and "
        "chlorophyll, gives C six H twelve O six, plus six H two O, plus six "
        "O two. <bookmark mark='b4'/> Notice that water appears on both sides, "
        "twelve going in and six coming out. <bookmark mark='b5'/> So overall, "
        "six water molecules are used, and the net equation is six C O two "
        "plus six H two O gives C six H twelve O six plus six O two."
    ),
    "s8": (
        "Glucose is only the beginning of plant material. <bookmark "
        "mark='b0'/> Many glucose units can join into larger carbohydrates. "
        "<bookmark mark='b1'/> Glucose can be used to form starch, which the "
        "plant stores, <bookmark mark='b2'/> and cellulose, which builds the "
        "cell wall. <bookmark mark='b3'/> Each arrow says can be used to form, "
        "because each takes more steps. <bookmark mark='b4'/> So "
        "photosynthesis provides the starting food material."
    ),
    "s9q": (
        "Your turn. Complete the photosynthesis map. <bookmark mark='b0'/> A: "
        "which gas enters the leaf from the air? <bookmark mark='b1'/> B: what "
        "is carried up from the roots? <bookmark mark='b2'/> C: which is the "
        "energy source? <bookmark mark='b3'/> D: which food is made inside the "
        "plant? <bookmark mark='b4'/> E: which gas is released into the air? "
        "And two quick checks: which supplies energy, carbon dioxide or "
        "sunlight? And where does photosynthesis happen? Take your time, and "
        "pause the video if you need to."
    ),
    "s9a": (
        "Let us check. <bookmark mark='b0'/> A: carbon dioxide. "
        "<bookmark mark='b1'/> B: water. <bookmark mark='b2'/> C: light "
        "energy from the Sun. <bookmark mark='b3'/> D: glucose. "
        "<bookmark mark='b4'/> E: oxygen. <bookmark mark='b5'/> Sunlight "
        "supplies the energy, not carbon dioxide, and photosynthesis happens "
        "in the chloroplast."
    ),
    "s10": (
        "Here is the whole story. <bookmark mark='b0'/> Water rises from the "
        "soil. <bookmark mark='b1'/> Carbon dioxide enters the leaf. "
        "<bookmark mark='b2'/> Sunlight strikes the leaf. <bookmark "
        "mark='b3'/> Chlorophyll in the chloroplast captures the light. "
        "<bookmark mark='b4'/> Photosynthesis happens inside. <bookmark "
        "mark='b5'/> Glucose stays in the plant, and oxygen goes out into the "
        "air. <bookmark mark='b6'/> Simple materials plus light energy become "
        "energy-rich food. Input, transform, output. <bookmark mark='b7'/> But "
        "how does one chloroplast capture light and build food? Next time: "
        "grana, stroma and the pigments. <bookmark mark='b8'/> Thank you for "
        "watching, <bookmark mark='b9'/> and see you in the next lesson."
    ),
}

WATER_C = "#4FC3F7"
CO2_C = "#CFD8DC"
LIGHT_C = "#FFD54F"
CHLORO_C = "#81C784"
GLU_C = "#FFB74D"
O2_C = "#EF9A9A"


# ------------------------------------------------------------ helpers -------
def fm(tex, color=CHALK_WHITE, size=40, w=None, h=None, pad=0.30):
    """A boxed chemical formula."""
    m = M(tex, size, color)
    box = panel(w or m.width + 2 * pad, h or m.height + 0.30, color,
                radius=0.14, stroke=2.4)
    m.move_to(box)
    g = VGroup(box, m)
    g.box = box
    return g


def icard(icon, head, sub, color, w=3.0, h=1.5, icon_w=1.0, head_size=26,
          sub_size=22):
    """Icon on the left, name + one line on the right, in a tight card."""
    ic = fit(icon, icon_w, h - 0.3)
    txt = VGroup(T(head, head_size, color)).arrange(DOWN, aligned_edge=LEFT)
    if sub:
        txt.add(T(sub, sub_size, CHALK_WHITE))
        txt.arrange(DOWN, buff=0.08, aligned_edge=LEFT)
    fit(txt, w - ic.width - 0.65, h - 0.3)
    row = VGroup(ic, txt).arrange(RIGHT, buff=0.25)
    box = panel(row.width + 0.5, max(row.height + 0.3, 0.7), color)
    row.move_to(box)
    g = VGroup(box, row)
    g.box = box
    return g


def stack_card(icon, head, lines_, color, w=3.1, h=2.7, icon_h=1.1,
               head_size=28, line_size=22):
    """Picture on top, bold head, short lines under it."""
    ic = fit(icon, w - 0.5, icon_h)
    parts = [ic, T(head, head_size, color, max_w=w - 0.3)]
    parts += [T(s, line_size, CHALK_WHITE, max_w=w - 0.3) for s in lines_]
    col = VGroup(*parts).arrange(DOWN, buff=0.12)
    box = panel(max(w, 0.1), max(h, col.height + 0.30), color)
    col.move_to(box)
    g = VGroup(box, col)
    g.box = box
    g._tight = True          # fixed size: neighbours stay the same height
    return g


def pic_card(pic, caption, color, w=4.2, h=2.7, pic_w=3.5, pic_h=1.75,
             cap_size=22):
    """A fixed-size card: the picture sits in the upper part and the caption
    in its own strip underneath, so text can never touch the drawing."""
    box = panel(w, h, color)
    pic = fit(pic, pic_w, pic_h)
    cap = T(caption, cap_size, color, max_w=w - 0.4)
    strip_h = cap.height + 0.12
    top_room = h - strip_h - 0.45
    pic.move_to(box.get_top() + DOWN * (0.20 + top_room / 2))
    cap.move_to(box.get_bottom() + UP * (0.17 + cap.height / 2))
    g = VGroup(box, pic, cap)
    g.box = box
    g._tight = True
    return g


def big_plant(ground_y, h=2.5, soil_w=3.2, cx=None):
    pl = plant(h, soil_w=soil_w)
    pl.move_to([CX if cx is None else cx, ground_y, 0])
    # .move_to centres the whole group; re-seat so the ground line is exact
    pl.shift(UP * (ground_y - pl.soil.get_top()[1]))
    return pl


def crown_of(pl):
    return pl.leaves[-1].get_center()


class PhotosynthesisInputsOutputsVisualFlowStory(BioScene):
    NARRATION = NARRATION
    TEXT_SCALE = 0.72
    TIGHT_BOXES = True
    STRICT_BOXES = True
    AVOID_ART = True
    BEATS = ("title", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10")

    # ------------------------------------------------------------ title ------
    def beat_title(self):
        with self.narrate("title") as tr:
            main = P(T("Photosynthesis", 64, CHALK_AMBER, max_w=8.4), CX, 0.55)
            rule = Line([CX - 3.0, -0.12, 0], [CX + 3.0, -0.12, 0],
                        stroke_color=CHALK_GREEN, stroke_width=4)
            sub = P(T("Inputs, Process & Outputs in One Visual Flow", 32,
                      CHALK_WHITE, max_w=8.6), CX, -0.62)
            self.show(main, rt=0.7)
            self.cue(tr, "b0", rule, sub, sfx="ding", rt=0.7)
            self.finish(tr)

    # ------------------------------------------------------------ scene 1 ----
    def beat_s1(self):
        with self.narrate("s1") as tr:
            self.heading("Where Does a Plant's Food Come From?")
            man = person_eating(1.9)
            table = Rectangle(width=1.35, height=0.10)
            paint(table, "#8D6E63", lw=2.2, sheen=0.2, line="#3E2723")
            legs = VGroup(*[Rectangle(width=0.08, height=0.70).set_fill(
                "#6D4C41", 1).set_stroke("#3E2723", 1.6) for _ in range(2)])
            legs[0].next_to(table, DOWN, buff=0, aligned_edge=LEFT).shift(
                RIGHT * 0.12)
            legs[1].next_to(table, DOWN, buff=0, aligned_edge=RIGHT).shift(
                LEFT * 0.12)
            pl1 = plate(0.9).next_to(table, UP, buff=-0.03)
            man.next_to(table, LEFT, buff=0.15, aligned_edge=DOWN)
            scene_l = VGroup(man, table, legs, pl1)
            scene_l.scale(1.0)
            cardL = pic_card(scene_l, "Animals: food comes from outside",
                             CHALK_AMBER, pic_w=3.6, pic_h=1.95)
            pt = plant(0.85, soil_w=1.9)
            cardR = pic_card(pt, "Plants: nobody serves a plate", CHALK_GREEN,
                             pic_w=3.6, pic_h=1.95)
            P(cardL, CX - 2.35, 0.62)
            P(cardR, CX + 2.35, 0.62)
            pl2 = plate(0.8).move_to(cardR.box.get_center() +
                                     np.array([1.35, -0.25, 0]))
            q = T("?", 52, CHALK_RED).move_to(pl2.get_center() + UP * 0.34)
            apple = Circle(radius=0.15)
            paint(apple, ["#EF5350", "#B71C1C"], lw=2.0, sheen=0.5,
                  line="#5D0A0A")
            apple.move_to(pt.leaves[-1].get_center() + np.array([0.55, 0.02, 0]))
            newleaf = leaf(0.55, 0.26, 0.12).rotate(60 * DEGREES)
            newleaf.move_to(pt.leaves[-1].get_center() +
                            np.array([-0.55, 0.12, 0]))
            ask = P(T("WHERE DOES THE FOOD COME FROM?", 34, CHALK_YELLOW,
                      max_w=7.8), CX + 0.1, -1.38)
            strip = P(T("THE LEAF CAN HELP MAKE IT.", 30, CHALK_GREEN,
                        max_w=7.8), CX + 0.1, -2.05)
            self.cue(tr, "b0", cardL, sfx="pop")
            self.cue(tr, "b1", cardR, FadeIn(pl2), FadeIn(q), sfx="click")
            self.cue(tr, "b2", FadeOut(pl2), FadeOut(q), FadeIn(apple,
                                                              scale=0.4),
                     FadeIn(newleaf, scale=0.4), sfx="whoosh")
            self.cue(tr, "b3", ask, sfx="ding")
            self.cue(tr, "b3", strip, sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 2 ----
    def beat_s2(self):
        with self.narrate("s2") as tr:
            self.heading("What Does Photosynthesis Need?")
            pl = big_plant(-1.45, h=2.35, soil_w=2.5, cx=CX)
            cr = crown_of(pl)
            water_arrow = arrow([CX - 0.05, -2.25, 0], [CX - 0.05, -0.55, 0],
                                WATER_C, 7)
            drops = VGroup(*[droplet(0.36).move_to([CX + dx, y, 0])
                             for dx, y in ((-0.60, -2.05), (0.55, -1.85),
                                           (-0.40, -1.65))])
            c_w = icard(droplet(0.5), "WATER", "from the soil", WATER_C, w=2.6)
            P(c_w, 3.05, -1.85)
            mols = VGroup(*[co2(1.0).move_to(p) for p in
                            [[CX + 1.20, 1.70, 0], [CX + 1.40, 1.05, 0],
                             [CX + 1.25, 0.40, 0]]])
            co_arrows = VGroup(*[arrow(m.get_center() + LEFT * 0.55,
                                       cr + RIGHT * 0.70 + UP * (0.40 - 0.25 * k),
                                       CO2_C, 4, 0.16)
                                 for k, m in enumerate(mols)])
            c_c = icard(co2(0.8), "CARBON DIOXIDE", "from the air", CO2_C,
                        w=2.9, head_size=22, sub_size=20, icon_w=0.8)
            P(c_c, 3.90, 1.55)
            sn = P(sun(0.45), -3.25, 1.35)
            rays = VGroup(*[wavy(sn.get_center() + np.array([0.55, -0.25 - k * 0.32,
                                                              0]),
                                 cr + np.array([-0.45, 0.05 - k * 0.12, 0]),
                                 amp=0.05, waves=5, color=LIGHT_C, w=3.5)
                            for k in range(3)])
            c_l = icard(sun(0.2, halo=False), "LIGHT ENERGY", "from the Sun",
                        LIGHT_C, w=3.3, head_size=24, icon_w=0.6)
            P(c_l, -2.65, -0.15)
            gl = glow(1.0, CHLORO_C, layers=6, peak=0.6).move_to(cr)
            c_h = icard(leaf(0.9, 0.42, 0.1), "CHLOROPHYLL",
                        "in the green parts", CHLORO_C, w=2.9,
                        head_size=22, sub_size=20, icon_w=0.7)
            P(c_h, 3.90, 0.50)
            self.add(pl)
            self.cue(tr, "b0", drops, water_arrow, c_w, sfx="pop")
            self.cue(tr, "b1", mols, co_arrows, c_c, sfx="click")
            self.cue(tr, "b2", sn, rays, c_l, sfx="ding")
            self.cue(tr, "b3", FadeIn(gl), c_h, sfx="click")
            self.cue(tr, "b4", *[Indicate(c, color=c.box.get_color(), scale_factor=1.06)
                                 for c in (c_w, c_c, c_l, c_h)], sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 3 ----
    def beat_s3(self):
        with self.narrate("s3") as tr:
            self.heading("Not All Four Play the Same Role")
            both = VGroup(co2(1.3), h2o(1.3)).arrange(RIGHT, buff=0.6)
            m_card = stack_card(both, "MATERIALS", ["carbon dioxide + water",
                                                    "the matter that is used"],
                                CHALK_CYAN, w=2.75, h=2.6, icon_h=0.95,
                                line_size=21)
            e_card = stack_card(sun(0.34), "ENERGY SOURCE",
                                ["light supplies", "energy only"], LIGHT_C,
                                w=2.75, h=2.6, icon_h=0.95)
            p_card = stack_card(VGroup(glow(0.7, CHLORO_C, 5, 0.5),
                                       leaf(1.1, 0.5, 0.1)),
                                "PIGMENT", ["chlorophyll catches",
                                            "light; not used up"],
                                CHLORO_C, w=2.75, h=2.6, icon_h=0.95)
            xs = (CX - 3.35, CX, CX + 3.35)
            for c, x in zip((m_card, e_card, p_card), xs):
                P(c, x, 0.70)
            plus1 = P(T("+", 48, CHALK_YELLOW), CX - 1.675, 0.70)
            plus2 = P(T("+", 48, CHALK_YELLOW), CX + 1.675, 0.70)
            ar = arrow([CX, -0.68, 0], [CX, -1.10, 0], CHALK_YELLOW, 8, 0.24)
            ph = P(chip("PHOTOSYNTHESIS", CHALK_YELLOW, 34), CX, -1.50)
            warn = P(chip("NEEDED DOES NOT MEAN CONSUMED THE SAME WAY",
                          CHALK_PINK, 26, w=7.9), CX + 0.1, -2.25)
            self.cue(tr, "b0", m_card, sfx="pop")
            self.cue(tr, "b1", e_card, plus1, sfx="click")
            self.cue(tr, "b2", p_card, plus2, sfx="click")
            self.cue(tr, "b3", ar, ph, sfx="ding")
            self.cue(tr, "b4", warn, sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 4 ----
    def beat_s4(self):
        with self.narrate("s4") as tr:
            self.heading("Where Does It Happen?")
            lf = leaf(2.5, 1.1, 0.10, veins=7)
            ring = Circle(radius=0.34, stroke_color=CHALK_YELLOW,
                          stroke_width=4, fill_opacity=0)
            ring.move_to(lf.get_center() + np.array([0.2, 0.08, 0]))
            c1 = pic_card(VGroup(lf, ring), "LEAF", CHALK_GREEN, w=2.75,
                          h=2.7, pic_w=2.4, pic_h=1.5, cap_size=26)
            c2 = pic_card(plant_cell(2.5, 1.75), "PLANT CELL", CHALK_GREEN,
                          w=2.75, h=2.7, pic_w=2.4, pic_h=1.55, cap_size=26)
            c3 = pic_card(chloroplast(2.4, 4), "CHLOROPLAST", CHALK_YELLOW,
                          w=2.75, h=2.7, pic_w=2.4, pic_h=1.45, cap_size=26)
            xs = (CX - 3.3, CX, CX + 3.3)
            for c, x in zip((c1, c2, c3), xs):
                P(c, x, 0.62)
            a1 = arrow([CX - 1.88, 0.62, 0], [CX - 1.42, 0.62, 0], CHALK_WHITE,
                       8, 0.26)
            a2 = arrow([CX + 1.42, 0.62, 0], [CX + 1.88, 0.62, 0], CHALK_WHITE,
                       8, 0.26)
            site = P(chip("SITE OF PHOTOSYNTHESIS", CHALK_YELLOW, 32), CX + 0.1,
                     -1.40)
            ins = VGroup(fm(r"\mathrm{CO_2}", CO2_C, 34, w=1.5),
                         fm(r"\mathrm{H_2O}", WATER_C, 34, w=1.5),
                         tag_label("LIGHT", LIGHT_C, 26))
            hrow(*ins, y=-2.20, gap=0.55, cx=CX + 0.1)
            self.cue(tr, "b0", c1, sfx="pop")
            self.cue(tr, "b1", a1, c2, sfx="click")
            self.cue(tr, "b2", a2, c3, sfx="click")
            self.cue(tr, "b3", site, *list(ins), sfx="ding")
            self.cue(tr, "b4", Indicate(c3.box, color=CHALK_YELLOW,
                                        scale_factor=1.03), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 5 ----
    def beat_s5(self):
        with self.narrate("s5") as tr:
            self.heading("Making Glucose Inside the Chloroplast")
            chl = chloroplast(2.9, 4)
            P(chl, CX - 0.45, 0.50)
            co_m = VGroup(*[co2(0.9) for _ in range(3)]).arrange(DOWN, buff=0.16)
            P(co_m, -3.30, 1.38)
            co_l = P(fm(r"\mathrm{CO_2}", CO2_C, 28, w=1.2), -3.30, 0.34)
            a_co = arrow([-2.35, 1.20, 0], [CX - 2.3, 0.85, 0], CO2_C, 5, 0.18)
            w_m = VGroup(*[droplet(0.42) for _ in range(3)]).arrange(RIGHT,
                                                                     buff=0.12)
            P(w_m, -3.10, -0.30)
            w_l = P(fm(r"\mathrm{H_2O}", WATER_C, 28, w=1.2), -3.00, -0.84)
            a_w = arrow([-2.15, -0.25, 0], [CX - 2.2, 0.15, 0], WATER_C, 5,
                        0.18)
            ray = wavy([CX - 0.45, 2.20, 0], [CX - 0.45, 1.05, 0], amp=0.06,
                       waves=5, color=LIGHT_C, w=4)
            ray2 = wavy([CX - 1.15, 2.20, 0], [CX - 1.1, 1.0, 0], amp=0.06,
                        waves=5, color=LIGHT_C, w=4)
            rl = P(tag_label("LIGHT ENERGY", LIGHT_C, 20), CX + 0.70, 1.88)
            chamber = Ellipse(width=3.45, height=1.95, stroke_color=CHALK_YELLOW,
                              stroke_width=2.4, fill_opacity=0)
            chamber.move_to(chl)
            ser = P(chip("SERIES OF REACTIONS", CHALK_YELLOW, 26), CX - 0.45,
                    -0.92)
            steps = VGroup(*[Dot(radius=0.07, color=CHALK_YELLOW)
                             for _ in range(5)]).arrange(RIGHT, buff=0.22)
            P(steps, CX - 0.45, -1.38)
            gl_ring = glucose_ring(0.55)
            gcard = VGroup(panel(2.7, 2.95, GLU_C), VGroup(
                gl_ring, T("GLUCOSE", 24, GLU_C),
                M(r"\mathrm{C_6H_{12}O_6}", 28, CHALK_WHITE)).arrange(
                DOWN, buff=0.14))
            gcard[1].move_to(gcard[0])
            gcard.box = gcard[0]
            P(gcard, 3.98, 0.50)
            a_out = arrow([CX + 1.35, 0.50, 0], [gcard.get_left()[0] - 0.05,
                                                 0.55, 0], GLU_C, 6, 0.2)
            strip = P(T("Light energy is stored as chemical energy in food.",
                        24, CHALK_WHITE, max_w=7.9), CX + 0.1, -2.30)
            self.add(chl)
            self.cue(tr, "b0", co_m, co_l, a_co, sfx="pop")
            self.cue(tr, "b1", w_m, w_l, a_w, sfx="click")
            self.cue(tr, "b2", ray, ray2, rl, sfx="ding")
            self.cue(tr, "b3", FadeIn(chamber), ser, steps, sfx="click")
            self.cue(tr, "b4", a_out, gcard, sfx="success")
            self.cue(tr, "b5", strip, sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 6 ----
    def beat_s6(self):
        with self.narrate("s6") as tr:
            self.heading("Oxygen Goes Back to the Air")
            chl = chloroplast(1.9, 3)
            cell = plant_cell(2.6, 1.75, chloros=5)
            lf = leaf(2.2, 1.05, 0.10, veins=6)
            icons = [chl, cell, lf]
            xs = [-3.05, -0.55, 1.85]
            labs = ["CHLOROPLAST", "CELL", "LEAF"]
            stage = VGroup()
            for ic, x, lb in zip(icons, xs, labs):
                ic.move_to([x, 0.90, 0])
                t = T(lb, 22, CHALK_GREEN)
                t.move_to([x, -0.28, 0])
                stage.add(VGroup(ic, t))
            air_box = panel(2.1, 1.9, CHALK_CYAN, opacity=0.35)
            air_box.move_to([4.15, 0.98, 0])
            air = P(T("AIR", 26, CHALK_CYAN), 4.15, -0.28)
            airs = VGroup(*[o2(0.7).move_to(p) for p in
                            [[3.7, 1.35, 0], [4.55, 1.15, 0], [3.85, 0.65, 0],
                             [4.55, 0.45, 0]]])
            o_start = o2(1.0).move_to([-3.05, 0.90, 0])
            tag_o = P(fm(r"\mathrm{O_2}", O2_C, 28, w=1.1), -3.05, 2.05)
            ins = P(icard(VGroup(co2(0.6), h2o(0.6)).arrange(RIGHT, buff=0.2),
                          "IN", "carbon dioxide, water, light",
                          CHALK_CYAN, w=4.0, h=0.95, icon_w=1.2),
                    CX - 1.75, -1.35)
            outc = P(icard(VGroup(glucose_hex(0.22), o2(0.6)).arrange(RIGHT,
                                                                     buff=0.2),
                           "OUT", "glucose + oxygen", CHALK_AMBER, w=3.4,
                           h=0.95, icon_w=1.2), CX + 2.30, -1.35)
            strip = P(T("The purpose is food. Oxygen is released along the way.",
                        24, CHALK_WHITE, max_w=7.9), CX + 0.1, -2.25)
            self.add(stage, air_box, air)
            self.cue(tr, "b0", o_start, tag_o, sfx="pop")
            self.cue(tr, "b1", o_start.animate.move_to([-0.55, 0.90, 0]),
                     sfx="whoosh", rt=0.9)
            self.cue(tr, "b2", o_start.animate.move_to([1.85, 0.90, 0]),
                     sfx="whoosh", rt=0.9)
            self.cue(tr, "b3", o_start.animate.move_to([4.15, 0.90, 0]),
                     FadeIn(airs), sfx="whoosh", rt=0.9)
            self.cue(tr, "b4", ins, outc, sfx="ding")
            self.cue(tr, "b5", strip, sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 7 ----
    def beat_s7(self):
        with self.narrate("s7") as tr:
            self.heading("Read the Equation as a Story")
            arrow_tex = lambda: M(r"\xrightarrow[\text{Chlorophyll}]{\text{Light}}",
                                  46, CHALK_YELLOW)

            def row(pieces, y, size):
                items = []
                for k, p in enumerate(pieces):
                    if p == "ARROW":
                        items.append(arrow_tex())
                    elif isinstance(p, tuple):
                        items.append(M(p[0], size, p[1]))
                    else:
                        items.append(M(p, size, CHALK_WHITE))
                g = VGroup(*items).arrange(RIGHT, buff=0.2)
                fit(g, 9.3)
                return P(g, CX, y)
            word = row([(r"\text{Carbon dioxide}", CO2_C), "+",
                        (r"\text{Water}", WATER_C), "ARROW",
                        (r"\text{Glucose}", GLU_C), "+",
                        (r"\text{Water}", WATER_C), "+",
                        (r"\text{Oxygen}", O2_C)], 1.35, 36)
            plain = row([(r"\mathrm{CO_2}", CO2_C), "+",
                         (r"\mathrm{H_2O}", WATER_C), "ARROW",
                         (r"\mathrm{C_6H_{12}O_6}", GLU_C), "+",
                         (r"\mathrm{H_2O}", WATER_C), "+",
                         (r"\mathrm{O_2}", O2_C)], 1.35, 44)
            full = row([(r"6\,\mathrm{CO_2}", CO2_C), "+",
                        (r"12\,\mathrm{H_2O}", WATER_C), "ARROW",
                        (r"\mathrm{C_6H_{12}O_6}", GLU_C), "+",
                        (r"6\,\mathrm{H_2O}", WATER_C), "+",
                        (r"6\,\mathrm{O_2}", O2_C)], 1.35, 44)
            br_l = Brace(VGroup(full[0], full[1], full[2]), DOWN, color=CHALK_CYAN,
                         buff=0.12)
            br_r = Brace(VGroup(full[4], full[5], full[6], full[7], full[8]),
                         DOWN, color=CHALK_AMBER, buff=0.12)
            lab_l = P(tag_label("REACTING MATERIALS", CHALK_CYAN, 22),
                      br_l.get_bottom()[0], br_l.get_bottom()[1] - 0.35)
            lab_r = P(tag_label("PRODUCTS", CHALK_AMBER, 22),
                      br_r.get_bottom()[0], br_r.get_bottom()[1] - 0.35)
            lab_m = P(tag_label("ENERGY + PIGMENT", CHALK_YELLOW, 22),
                      full[3].get_center()[0], 2.05)
            b1 = SurroundingRectangle(full[2], color=CHALK_YELLOW, buff=0.10,
                                      stroke_width=3)
            b2 = SurroundingRectangle(full[6], color=CHALK_YELLOW, buff=0.10,
                                      stroke_width=3)
            both_t = P(T("water on both sides", 24, CHALK_YELLOW),
                       (full[2].get_center()[0] + full[6].get_center()[0]) / 2,
                       -0.62)
            net_h = T("NET (overall):", 24, CHALK_GREEN)
            net = M(r"6\,\mathrm{CO_2}+6\,\mathrm{H_2O}\rightarrow "
                    r"\mathrm{C_6H_{12}O_6}+6\,\mathrm{O_2}", 40, CHALK_GREEN)
            netg = VGroup(net_h, net).arrange(DOWN, buff=0.15)
            fit(netg, 9.3)
            nbox = panel(netg.width + 0.6, netg.height + 0.34, CHALK_GREEN)
            netc = VGroup(nbox, netg)
            netg.move_to(nbox)
            netc.box = nbox
            P(netc, CX, -1.70)
            self.cue(tr, "b0", word, sfx="pop")
            self.cue(tr, "b1", Indicate(word, color=CHALK_YELLOW,
                                        scale_factor=1.03), sfx=None)
            self.cue(tr, "b2", ReplacementTransform(word, plain), sfx="ding",
                     rt=1.0)
            self.cue(tr, "b3", ReplacementTransform(plain, full), sfx="ding",
                     rt=1.0, snap="full")
            self.cue(tr, "b3", br_l, br_r, lab_l, lab_m, lab_r, sfx=None)
            self.cue(tr, "b4", Create(b1), Create(b2), FadeIn(both_t),
                     sfx="click")
            self.cue(tr, "b5", netc, sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 8 ----
    def beat_s8(self):
        with self.narrate("s8") as tr:
            self.heading("Glucose Builds More Plant Material")
            g1 = P(glucose_ring(0.58), -2.75, 0.95)
            gl = P(fm(r"\mathrm{C_6H_{12}O_6}", GLU_C, 28, w=2.1), -2.75, -0.38)
            chain = VGroup(*[glucose_hex(0.30) for _ in range(6)]).arrange(
                RIGHT, buff=-0.02)
            P(chain, CX + 2.15, 0.95)
            ch_l = P(T("CARBOHYDRATES", 26, CHALK_AMBER), CX + 2.15, 0.22)
            ar0 = arrow([-1.65, 0.95, 0], [CX + 0.35, 0.95, 0], GLU_C, 6)
            st = icard(starch_granule(0.34), "STARCH", "stored by the plant",
                       CHALK_AMBER, w=3.7, h=1.2, icon_w=0.9)
            ce = icard(cellulose_wall(0.9, 0.45), "CELLULOSE", "builds the cell wall",
                       CHALK_GREEN, w=3.7, h=1.2, icon_w=1.0)
            P(st, -1.15, -1.40)
            P(ce, 2.95, -1.40)
            a_st = arrow([CX + 0.9, 0.00, 0], [st.get_top()[0] + 0.3, st.get_top()[1] +
                                                0.05, 0], GLU_C, 5, 0.18)
            a_ce = arrow([CX + 3.0, 0.00, 0], [ce.get_top()[0] - 0.2, ce.get_top()[1] +
                                                0.05, 0], GLU_C, 5, 0.18)
            can = VGroup(T("can be used to form", 22, CHALK_YELLOW))
            can_l = P(T("can be used to form", 22, CHALK_YELLOW), CX + 0.85, -0.58)
            strip = P(T("Photosynthesis provides the starting food material.",
                        24, CHALK_WHITE, max_w=9.4), CX + 0.1, -2.30)
            self.cue(tr, "b0", g1, gl, sfx="pop")
            self.cue(tr, "b1", ar0, chain, ch_l, sfx="click")
            self.cue(tr, "b2", a_st, st, sfx="click")
            self.cue(tr, "b2", a_ce, ce, sfx=None)
            self.cue(tr, "b3", can_l, sfx="ding")
            self.cue(tr, "b4", strip, sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 9 ----
    def beat_s9(self):
        with self.narrate("s9q") as tr:
            self.heading("YOUR TURN", "Complete the photosynthesis map.",
                         CHALK_PINK)
            pl = big_plant(-0.40, h=1.65, soil_w=2.6)
            cr = crown_of(pl)
            self.add(pl)

            def qchip(letter, color, x, y):
                g = chip(f"{letter}   ?", color, 28)
                return P(g, x, y)
            qa = qchip("A", CHALK_CYAN, 3.65, 1.40)
            qb = qchip("B", WATER_C, 3.40, -0.85)
            qc = qchip("C", LIGHT_C, -2.60, 1.40)
            qd = qchip("D", GLU_C, -2.55, 0.15)
            qe = qchip("E", O2_C, 3.65, 0.35)
            arrows = [
                arrow([3.0, 1.40, 0], cr + RIGHT * 0.35, CHALK_CYAN, 5, 0.18),
                arrow([2.75, -0.85, 0], [CX + 0.30, -1.00, 0], WATER_C, 5, 0.18),
                arrow([-1.75, 1.40, 0], cr + LEFT * 0.35, LIGHT_C, 5, 0.18),
                arrow([-1.60, 0.15, 0], [CX - 0.15, 0.30, 0], GLU_C, 5, 0.18),
                arrow(cr + RIGHT * 0.9 + DOWN * 0.1, [3.05, 0.35, 0], O2_C, 5,
                      0.18),
            ]
            self.cue(tr, "b0", qa, arrows[0], sfx="pop")
            self.cue(tr, "b1", qb, arrows[1])
            self.cue(tr, "b2", qc, arrows[2])
            self.cue(tr, "b3", qd, arrows[3])
            self.cue(tr, "b4", qe, arrows[4])
            q1 = P(chip("ENERGY: CO2 OR SUNLIGHT ?", CHALK_PINK, 18), CX + 0.1,
                   -1.84)
            q2 = P(chip("SITE OF PHOTOSYNTHESIS ?", CHALK_PINK, 18), CX + 0.1,
                   -2.40)
            self.show(q1, q2)
            self.finish(tr)
        self.think_clock()
        with self.narrate("s9a", reset=False) as tr:
            def ans(letter, txt, tex, color, ref):
                body = M(tex, 30, color) if tex else T(txt, 28, color)
                row = VGroup(T(letter, 28, color), body).arrange(RIGHT,
                                                                buff=0.25)
                box = panel(row.width + 0.5, row.height + 0.3, color)
                row.move_to(box)
                g = VGroup(box, row)
                g.box = box
                g.move_to(ref.get_center())
                return g
            aa = ans("A", "", r"\mathrm{CO_2}", CHALK_CYAN, qa)
            ab = ans("B", "", r"\mathrm{H_2O}", WATER_C, qb)
            ac = ans("C", "LIGHT", None, LIGHT_C, qc)
            ad = ans("D", "GLUCOSE", None, GLU_C, qd)
            ae = ans("E", "", r"\mathrm{O_2}", O2_C, qe)
            self.cue(tr, "b0", FadeOut(qa), FadeIn(aa), sfx="click", rt=0.5)
            self.cue(tr, "b1", FadeOut(qb), FadeIn(ab))
            self.cue(tr, "b2", FadeOut(qc), FadeIn(ac))
            self.cue(tr, "b3", FadeOut(qd), FadeIn(ad))
            self.cue(tr, "b4", FadeOut(qe), FadeIn(ae))
            r1 = P(chip("SUNLIGHT: the energy", CHALK_GREEN, 18), CX + 0.1, -1.84)
            r2 = P(chip("THE CHLOROPLAST", CHALK_GREEN, 18), CX + 0.1, -2.40)
            self.cue(tr, "b5", FadeOut(q1), FadeOut(q2), FadeIn(r1),
                     FadeIn(r2), sfx="success", rt=0.5)
            self.finish(tr)

    # ----------------------------------------------------------- scene 10 ----
    def beat_s10(self):
        with self.narrate("s10") as tr:
            head = self.heading("The Complete Photosynthesis Story")
            pl = big_plant(-0.70, h=1.95, soil_w=2.6)
            cr = crown_of(pl)
            self.add(pl)
            w_arrow = arrow([CX - 0.05, -1.55, 0], [CX - 0.05, -0.20, 0],
                            WATER_C, 7)
            w_lab = P(fm(r"\mathrm{H_2O}", WATER_C, 26, w=1.1), CX + 2.55, -1.20)
            c_m = VGroup(*[co2(0.8).move_to(p) for p in
                           [[CX + 2.45, 1.70, 0], [CX + 2.45, 1.10, 0]]])
            c_a = arrow([CX + 1.80, 1.40, 0], cr + RIGHT * 0.65,
                        CO2_C, 5, 0.18)
            c_lab = P(fm(r"\mathrm{CO_2}", CO2_C, 26, w=1.0), CX + 3.75, 1.40)
            sn = P(sun(0.36), -3.30, 1.78)
            rays = VGroup(*[wavy(sn.get_center() + np.array([0.50, -0.05 - k *
                                                             0.20, 0]),
                                 cr + np.array([-0.45, 0.05 - k * 0.12, 0]),
                                 amp=0.05, waves=5, color=LIGHT_C, w=3.5)
                            for k in range(3)])
            l_lab = P(tag_label("LIGHT ENERGY", LIGHT_C, 20), -3.15, 0.88)
            spacer = Rectangle(width=1.7, height=0.34, stroke_width=0, fill_opacity=0)
            inset = VGroup(panel(2.3, 1.65, CHLORO_C),
                           VGroup(chloroplast(1.7, 3), spacer).arrange(DOWN, buff=0.04))
            inset[1].move_to(inset[0])
            inset.box = inset[0]
            P(inset, -2.55, -0.92)
            zl = P(tag_label("CHLOROPHYLL", CHLORO_C, 20), -2.55, 0.26)
            ins_arrow = arrow(inset.get_right() + LEFT * 0.05 + UP * 0.45,
                              cr + LEFT * 0.55 + DOWN * 0.45, CHLORO_C, 4, 0.14)
            tr_lab = P(T("PHOTOSYNTHESIS", 20, CHALK_YELLOW), -2.55, spacer.get_center()[1])
            glu = P(glucose_hex(0.28), CX + 1.00, -0.20)
            glu_l = P(fm(r"\mathrm{C_6H_{12}O_6}", GLU_C, 22, w=1.8), CX + 2.15,
                      -0.52)
            o_mol = VGroup(*[o2(0.8).move_to(p) for p in
                             [[CX + 3.45, 0.55, 0], [CX + 3.45, 0.00, 0]]])
            o_a = arrow(cr + RIGHT * 1.0 + DOWN * 0.55, [CX + 2.85, 0.45, 0],
                        O2_C, 5, 0.18)
            o_lab = P(fm(r"\mathrm{O_2}", O2_C, 26, w=1.0), CX + 3.45, -0.55)
            eq = P(M(r"6\,\mathrm{CO_2}+12\,\mathrm{H_2O}\xrightarrow"
                     r"[\text{Chlorophyll}]{\text{Light}}\mathrm{C_6H_{12}O_6}"
                     r"+6\,\mathrm{H_2O}+6\,\mathrm{O_2}", 36, CHALK_WHITE,
                     max_w=8.0), CX + 0.1, -2.26)
            msg = P(chip("SIMPLE MATERIALS + LIGHT  ->  ENERGY-RICH FOOD",
                         CHALK_YELLOW, 24, w=7.4), CX + 0.9, 2.30)
            self.cue(tr, "b0", w_arrow, w_lab, sfx="pop")
            self.cue(tr, "b1", c_m, c_a, c_lab, sfx="click")
            self.cue(tr, "b2", sn, rays, l_lab, sfx="ding")
            self.cue(tr, "b3", inset, ins_arrow, zl, sfx="click")
            self.cue(tr, "b4", tr_lab, sfx="ding")
            self.cue(tr, "b5", glu, glu_l, o_a, o_mol, o_lab, sfx="success",
                     snap="outputs")
            self.cue(tr, "b6", eq, FadeOut(head), FadeIn(msg), sfx="success",
                     snap="eq")
            nxt = P(chip("NEXT: CHLOROPLAST - GRANA, STROMA & PIGMENTS",
                         CHALK_CYAN, 24, w=7.4), CX + 0.9, 2.30)
            thanks = P(T("Thank You for Watching!", 52, CHALK_WHITE,
                         max_w=9.4), CX, 0.55)
            bye = P(T("See you in the next lesson :)", 38, CHALK_YELLOW,
                      max_w=9.0), CX, -0.65)
            self.cue(tr, "b7", ReplacementTransform(msg, nxt), sfx="ding")
            self.hold(tr, "b8")
            keep = [m for m in self.mobjects if m not in self.fixtures]
            self.go(*[FadeOut(m) for m in keep], rt=0.6)
            self.cue(tr, "b8", FadeIn(thanks, shift=UP * 0.1), sfx=None)
            self.cue(tr, "b9", FadeIn(bye, shift=UP * 0.1), sfx=None)
            self.finish(tr)
        if not self.still:
            self.wait(END_HOLD)

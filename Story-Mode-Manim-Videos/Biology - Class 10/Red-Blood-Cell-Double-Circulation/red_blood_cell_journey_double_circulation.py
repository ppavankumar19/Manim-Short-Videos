"""
A Red Blood Cell's Journey: Understanding Double Circulation Through the
Heart, Lungs & Body
Story-mode chalkboard lesson (Class 10 Biology, Chapter 3: Circulation).

LLM KEY / FUNCTION NAME: red_blood_cell_journey_double_circulation

ONE red blood cell is followed through the whole circuit:
body -> vena cava -> right atrium -> (tricuspid valve) -> right ventricle ->
pulmonary artery -> lungs (becomes oxygenated) -> pulmonary veins -> left
atrium -> (mitral valve) -> left ventricle -> aorta -> body (becomes
deoxygenated again) -> back to the right atrium.  Two passes through the heart
in one complete circulation = DOUBLE CIRCULATION.

Production rules (the series' rules, all kept): everything inside the green
board; larger type (TEXT_SCALE 0.92); boxes that hug their text; nothing on the
teacher / students / badges; arrows and signs visible; every picture appears
when the voice reaches its bookmark; the same cell is never replaced.

Backdrop: assets/background.png (one big empty chalkboard, no students or
teacher) -- the whole board is used: a 3.4-wide panel on the right, a label
column on the left, the map / heart / insets scaled up in between, and type
about 28% larger than before.

Decisions on the draft storyboard:
  * ONE fixed circulation map (heart centre, lungs top, body bottom) is reused
    by every scene, so the viewer never loses their place; the right side of
    the heart stays on the viewer's LEFT and carries a permanent
    "RIGHT SIDE" tag, the left side a "LEFT SIDE" tag.
  * colour code: blue = deoxygenated, red = oxygenated; the cell keeps its
    glowing ring and only changes colour at the lungs and at the tissues;
  * artery/vein are defined by direction (away from / towards the heart); the
    pulmonary artery and pulmonary veins are shown as the two exceptions;
  * the heart-visit counter counts each pass through the heart: 1 on entering
    the right atrium, 2 on entering the left atrium (two passes = double);
  * valves visibly block a backward move once;
  * the challenge uses the series' ten-second THINK clock.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_BIO = next(p for p in _HERE.parents if (p / "bio_kit.py").exists())
if str(_BIO) not in sys.path:
    sys.path.insert(0, str(_BIO))

# This video uses the plain full-width board (assets/background.png, no
# students / teacher); it must be chosen before bio_kit is first imported.
os.environ["BIO_BOARD"] = "plain"

from bio_kit import *  # noqa: F401,F403,E402
from bio_art import *  # noqa: F401,F403,E402
from bio_widgets import *  # noqa: F401,F403,E402
from bio_heart_art import *  # noqa: F401,F403,E402
from bio_real_art import real_heart, alveolus_view  # noqa: E402
import bio_thorax_art as TX  # noqa: E402
from bio_thorax_art import Thorax, upper_body_real, flow, ATTR_BODY  # noqa: E402

assert BOARD_NAME == "plain", "bio_kit was imported before BIO_BOARD was set"

NARRATION = {
    "title": (
        "A red blood cell's journey. <bookmark mark='b0'/> Understanding "
        "double circulation through the heart, lungs and body."
    ),
    "s1": (
        "Look inside a large vein. Millions of red blood cells are flowing "
        "back towards the heart. <bookmark mark='b0'/> Now freeze them, and "
        "follow just one. <bookmark mark='b1'/> This cell is low on oxygen, "
        "its destination is unknown, and it has visited the heart zero "
        "times. <bookmark mark='b2'/> Can you trace its complete journey? "
        "And how many times will it pass through the heart?"
    ),
    "s2": (
        "The journey starts in the body. <bookmark mark='b0'/> Our cell "
        "leaves the body tissues and enters the veins. <bookmark "
        "mark='b1'/> Blood from the upper body returns through the superior "
        "vena cava, <bookmark mark='b2'/> and blood from the lower body "
        "returns through the inferior vena cava. <bookmark mark='b3'/> Both "
        "routes meet at the right atrium. <bookmark mark='b4'/> This is the "
        "cell's first visit to the heart. <bookmark mark='b5'/> So: body, "
        "vena cava, right atrium."
    ),
    "s3": (
        "Now we are inside the heart. The cell waits in the right atrium. "
        "<bookmark mark='b0'/> Between the right atrium and the right "
        "ventricle is the tricuspid valve. <bookmark mark='b1'/> The valve "
        "opens, and the cell moves into the right ventricle. <bookmark "
        "mark='b2'/> Then the valve closes behind it. If the blood tries to "
        "flow backward, the valve blocks it. This is one-way flow. "
        "<bookmark mark='b3'/> Now the cell is in the right ventricle. "
        "<bookmark mark='b4'/> Where will this ventricle send the blood?"
    ),
    "s4": (
        "The right ventricle contracts, and the cell shoots into the "
        "pulmonary artery. <bookmark mark='b0'/> You might think an artery "
        "always carries oxygenated blood. <bookmark mark='b1'/> But not "
        "always: the pulmonary artery carries deoxygenated blood to the "
        "lungs. <bookmark mark='b2'/> The route right ventricle, pulmonary "
        "artery, lungs is called pulmonary circulation. <bookmark "
        "mark='b3'/> The cell now approaches the lungs."
    ),
    "s5": (
        "Inside the lungs, the cell enters a narrow capillary. <bookmark "
        "mark='b0'/> Capillaries are microscopic vessels that connect "
        "arteries to veins. <bookmark mark='b1'/> Before the lungs, the cell "
        "is deoxygenated. <bookmark mark='b2'/> In the lungs, it picks up "
        "oxygen, and its status changes to oxygenated. <bookmark mark='b3'/> "
        "Now it leaves through the pulmonary vein. The pulmonary vein "
        "carries oxygenated blood, which is another exception. <bookmark "
        "mark='b4'/> Remember: an artery leads away from the heart, and a "
        "vein leads towards it."
    ),
    "s6": (
        "The cell has returned to the heart, this time to the left atrium. "
        "<bookmark mark='b0'/> The pulmonary loop is complete: right "
        "ventricle, lungs, left atrium. This is the cell's second visit to "
        "the heart. <bookmark mark='b1'/> Between the left atrium and the "
        "left ventricle is the bicuspid, or mitral, valve. <bookmark "
        "mark='b2'/> It opens, and the cell moves into the left ventricle. "
        "<bookmark mark='b3'/> Next stop: the whole body."
    ),
    "s7": (
        "The left ventricle contracts strongly and pushes the cell into the "
        "aorta. <bookmark mark='b0'/> The aorta carries oxygenated blood to "
        "the body: the brain, arms, liver, kidneys and lower body. "
        "<bookmark mark='b1'/> The cell travels along the aorta towards the "
        "body. <bookmark mark='b2'/> This route, left ventricle, aorta, body, "
        "is called systemic circulation."
    ),
    "s8": (
        "Now the cell reaches a capillary bed in the body tissues. "
        "<bookmark mark='b0'/> It arrives oxygenated, and gives oxygen to "
        "the cells around it. <bookmark mark='b1'/> As it leaves, it is "
        "deoxygenated again. <bookmark mark='b2'/> The capillaries join up to "
        "form veins, because capillaries connect arteries to veins. "
        "<bookmark mark='b3'/> The cell returns through the vena cava to the "
        "right atrium, <bookmark mark='b4'/> exactly where it started. One "
        "complete journey."
    ),
    "s9": (
        "Now let us see why this is called double circulation. <bookmark "
        "mark='b0'/> The first loop: heart, lungs, heart. This is pulmonary "
        "circulation. <bookmark mark='b1'/> The second loop: heart, body, "
        "heart. This is systemic circulation. <bookmark mark='b2'/> In one "
        "complete circulation, the blood passes through the heart twice. "
        "<bookmark mark='b3'/> Two passes through the heart: that is double "
        "circulation. <bookmark mark='b4'/> Pulmonary loop plus systemic "
        "loop equals double circulation."
    ),
    "s10q": (
        "Your turn. Be the red blood cell. You are now in the right atrium. "
        "<bookmark mark='b0'/> A: where do you go next? <bookmark "
        "mark='b1'/> B: which vessel takes you to the lungs? <bookmark "
        "mark='b2'/> C: after the lungs, which chamber do you reach first? "
        "<bookmark mark='b3'/> D: from the left ventricle, which major "
        "vessel carries you to the body? <bookmark mark='b4'/> E: why is it "
        "called double circulation? Take your time, and pause the video if "
        "you need to."
    ),
    "s10a": (
        "Let us check. <bookmark mark='b0'/> A: the right ventricle. "
        "<bookmark mark='b1'/> B: the pulmonary artery. <bookmark "
        "mark='b2'/> C: the left atrium. <bookmark mark='b3'/> D: the aorta. "
        "<bookmark mark='b4'/> E: because the blood passes through the heart "
        "twice in one complete circulation."
    ),
    "s11": (
        "Here is the whole journey in one go. <bookmark mark='b0'/> From the "
        "body, through the vena cava, into the right atrium and the right "
        "ventricle. <bookmark mark='b1'/> Then the pulmonary artery and the "
        "lungs. <bookmark mark='b2'/> Then the pulmonary veins, the left "
        "atrium and the left ventricle. <bookmark mark='b3'/> Then the aorta, "
        "and back to the body. <bookmark mark='b4'/> Remember: right to the "
        "lungs, left to the body. <bookmark mark='b5'/> A pulmonary loop plus "
        "a systemic loop is double circulation. <bookmark mark='b6'/> Thank "
        "you for watching, <bookmark mark='b7'/> and see you in the next "
        "lesson."
    ),
}

PX = 4.69                      # centre of the right-hand panel
PW = 3.50                      # width of EVERY box in that panel
LX = -5.40                     # centre of the left label column
PAN_TOP = 2.45                 # top edge of every right-hand stack
TAG_Y = -2.66                  # y of the RIGHT SIDE / LEFT SIDE tags
S_MAP = 1.08                   # the old map layout, scaled up by this much
HEART_H = 4.70                 # height of the anatomical heart (scenes 3, 6)
HC = np.array([-0.90, -0.35, 0.0])         # centre of the heart in those scenes
ATTR_HEART = "Heart: ZooFari, CC BY-SA 3.0"


# ------------------------------------------------------------- helpers ------
def mlines(txt, col, size):
    """Text (one or several lines, split at newlines) with every line centred."""
    parts = txt.split("\n")
    return lines(parts, size, col, buff=0.03) if len(parts) > 1 else \
        T(txt, size, col)


def tag_box(txt, col, size):
    t = mlines(txt, col, size)
    box = RoundedRectangle(corner_radius=0.12, width=t.width + 0.34,
                           height=t.height + 0.20, stroke_color=col,
                           stroke_width=2.2, fill_color=PANEL_FILL,
                           fill_opacity=0.85)
    t.move_to(box)
    g = VGroup(box, t)
    g.box = box
    return g


def callout(txt, col, lab_pos, target, size=19):
    lab = tag_box(txt, col, size)
    lab.move_to(lab_pos)
    side_right = target[0] > lab_pos[0]
    start = lab.get_right() if side_right else lab.get_left()
    ln = Line(start, target, stroke_color=col, stroke_width=2.4)
    dt = Dot(target, radius=0.05, color=col)
    return VGroup(lab, ln, dt)


def side_label(lines_, col, pos, target, size=17, facing="right"):
    """A narrow label parked in the empty margin; only its thin leader line
    crosses the drawing (never the box).  facing="right": the leader leaves
    from the box's right edge (box to the left of the target); "left": the
    other way round."""
    body = lines(lines_, size, col, buff=0.02)
    box = panel(body.width + 0.28, body.height + 0.20, col, radius=0.10,
                stroke=2.0)
    body.move_to(box)
    g = VGroup(box, body)
    g.box = box
    g._tight = True
    g.move_to([pos[0], pos[1], 0])
    tgt = np.array([target[0], target[1], 0.0])
    start = box.get_right() if facing == "right" else box.get_left()
    ln = Line(start, tgt, stroke_color=col, stroke_width=2.4)
    dt = Dot(tgt, radius=0.05, color=col)
    return VGroup(g, ln, dt)


def tag(txt):
    c = chip(txt, CHALK_WHITE, 20, w=1.90, h=0.44)
    c._tight = True
    return c


def chain_v(labels, colors, size=21, w=3.3, gap=0.04, h=0.50):
    """Vertical chain: chip, down-arrow, chip ..."""
    parts = []
    for k, (lb, col) in enumerate(zip(labels, colors)):
        c = chip(lb, col, size, w=w, h=h)
        c._tight = True
        parts.append(c)
        if k < len(labels) - 1:
            parts.append(arrow([0, 0, 0], [0, -0.20, 0], CHALK_WHITE, 5, 0.13))
    return VGroup(*parts).arrange(DOWN, buff=gap)


def pchip(txt, col, size, h=None, w=PW):
    """A panel chip, always PW wide; newlines make centred extra lines."""
    lab = mlines(txt, col, size)
    fit(lab, w - 0.3)
    box = panel(w, h or lab.height + 0.34, col, radius=0.14, stroke=2.4)
    lab.move_to(box.get_center())
    c = VGroup(box, lab)
    c.box, c.label = box, lab
    c._tight = True
    return c


def pcard(head, body, col, size=22, head_size=26, w=PW, pad=0.15, gap=0.06):
    """A panel card, always PW wide (never shrunk to its text)."""
    c = tcard(head, body, col, w=w, head_size=head_size, body_size=size,
              pad=pad, gap=gap)
    c._tight = True
    return c


def counter(n):
    c = pchip(f"HEART VISITS: {n}", CHALK_YELLOW, 24, h=0.56, w=PW)
    return P(c, PX, 1.9)


def status(label, col):
    c = pchip(label, col, 24, h=0.52, w=PW)
    return P(c, PX, 1.3)


def gate(pos, opened, size=0.38, color=CHALK_YELLOW):
    """A valve 'gate' drawn over the anatomical heart: two leaflets that meet
    (closed) or swing apart (open)."""
    x, y = float(pos[0]), float(pos[1])
    if opened:
        a = Line([x - size, y + 0.02, 0], [x - size * 0.45, y - size * 0.55, 0])
        b = Line([x + size, y + 0.02, 0], [x + size * 0.45, y - size * 0.55, 0])
    else:
        a = Line([x - size, y + 0.02, 0], [x - 0.02, y - size * 0.18, 0])
        b = Line([x + size, y + 0.02, 0], [x + 0.02, y - size * 0.18, 0])
    g = VGroup(*[ln.set_stroke(OUTLINE, 12) for ln in (a.copy(), b.copy())],
               *[ln.set_stroke(color, 7) for ln in (a, b)])
    return g


def credit(txt):
    t = T(txt, 14, CHALK_WHITE)
    t.set_opacity(0.8)
    return P(t, PX, -2.22)


def F(x, y):
    """Old map layout (centre (-0.10,-0.20)) -> this layout, S_MAP larger."""
    return np.array([(x + 0.10) * S_MAP + MAP_C[0],
                     (y + 0.20) * S_MAP + MAP_C[1], 0.0])


MAP_C = (-0.45, -0.35)         # where the map's centre sits on the board
TH = Thorax(cx=MAP_C[0], cy=MAP_C[1], height=3.7 * S_MAP)
BAND_Y = float(F(0, -2.35)[1])
BUST_C = np.array([-3.70, 1.22, 0.0])


def stack(items, top=PAN_TOP, gap=0.18, x=None, max_h=5.0):
    """Lay panel items out top-down with a real gap, centred on the panel."""
    g = VGroup(*items).arrange(DOWN, buff=gap)
    if g.height > max_h:
        g.scale(max_h / g.height)
    g.move_to([PX if x is None else x, top - g.height / 2, 0])
    return g


def M_(pts):
    """plate-frame points -> board points"""
    return [TH.b(p) for p in pts]


SVC_OUT = [np.array([-2.85, 1.00, 0.0]), F(-1.95, 1.38), F(-1.25, 1.32),
           F(-0.85, 1.10), TH.b((-1.0, 2.2))]
IVC_OUT = [F(-2.05, -2.10), F(-1.45, -2.00), F(-0.95, -1.75),
           TH.b((-1.0, -2.55))]
AORTA_OUT = [TH.b((0.45, 3.35)), F(0.30, 1.90), F(1.00, 2.12), F(2.00, 2.08),
             F(2.30, 1.55), F(2.30, -1.20), F(2.30, -2.10)]
BAND_L, BAND_R = float(F(-2.70, 0)[0]), float(F(2.55, 0)[0])


class RedBloodCellJourneyDoubleCirculationStory(BioScene):
    NARRATION = NARRATION
    TEXT_SCALE = 0.92
    TIGHT_BOXES = True
    STRICT_BOXES = True
    AVOID_ART = True
    CLOCK_AT = (5.70, 2.55)     # small THINK clock, top right, board not dimmed
    BEATS = ("title", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9",
             "s10", "s11")

    # --------------------------------------------------- the fixed map -------
    def put_map(self, tags=True):
        plate = TH.plate()
        tubes = VGroup()
        for pts, col in ((SVC_OUT, TX.DEOX), (IVC_OUT, TX.DEOX),
                         (AORTA_OUT, TX.OXY)):
            tubes.add(flow(pts, col, 10, 0.85))
            tubes.add(TX.chevrons(pts, "#FFFFFF", 3, 0.08))
        inner = VGroup()
        for pts, col in ((TX.SVC_IN, TX.DEOX), (TX.IVC_IN, TX.DEOX),
                         (TX.RA_RV, TX.DEOX), (TX.RV_TRUNK, TX.DEOX),
                         (TX.PA_PATH, TX.DEOX), (TX.PV_PATH, TX.OXY),
                         (TX.LA_LV, TX.OXY), (TX.LV_AORTA, TX.OXY)):
            inner.add(flow(M_(pts), col, 6, 0.55, outline=False))
        bust = upper_body_real(1.85).move_to(BUST_C)
        band = body_band(BAND_R - BAND_L, 0.50).move_to(
            [(BAND_L + BAND_R) / 2, BAND_Y, 0])
        up_l = T("UPPER BODY", 18, CHALK_WHITE).move_to(
            BUST_C + DOWN * (0.925 + 0.20))
        bd_l = T("BODY TISSUES", 20, CHALK_WHITE).move_to(
            [float(F(-1.0, 0)[0]) + 0.1, BAND_Y, 0])
        parts = [plate, inner, tubes, bust, band, up_l, bd_l]
        if tags:
            parts.append(tag("RIGHT SIDE").move_to([LX, TAG_Y, 0]))
            parts.append(tag("LEFT SIDE").move_to([5.35, TAG_Y - 0.08, 0]))
        m = Group(*parts)
        self.add(m)
        m.plate = plate
        return m

    def rbc_at(self, p, oxy=False, r=0.14):
        c = rbc(r, oxy)
        c.move_to(np.array([p[0], p[1], 0.0]))
        return c

    def travel(self, cell, pts, rt=2.0):
        pts = [np.array([q[0], q[1], 0.0]) for q in pts]
        return MoveAlongPath(cell, TX.path_vm(pts), run_time=rt,
                             rate_func=linear)

    # ------------------------------------------------------------ title ------
    def beat_title(self):
        with self.narrate("title") as tr:
            main = P(T("A Red Blood Cell's Journey", 60, CHALK_AMBER, max_w=11.4),
                     CX, 1.15)
            cell = rbc(0.30, False).move_to([CX, 0.20, 0])
            rule = Line([CX - 3.6, -0.55, 0], [CX + 3.6, -0.55, 0],
                        stroke_color=CHALK_GREEN, stroke_width=4)
            sub = P(T("Understanding Double Circulation", 38, CHALK_WHITE,
                      max_w=11.0), CX, -1.12)
            sub2 = P(T("Through the Heart, Lungs & Body", 34, CHALK_WHITE,
                       max_w=11.0), CX, -1.76)
            self.show(VGroup(main, cell), rt=0.7)
            self.cue(tr, "b0", rule, sub, sub2, sfx="ding", rt=0.7)
            self.finish(tr)

    # ------------------------------------------------------------ scene 1 ----
    def beat_s1(self):
        with self.narrate("s1") as tr:
            self.heading("Follow One Red Blood Cell")
            vx, vy = -1.75, 0.50
            vein = RoundedRectangle(corner_radius=0.55, width=8.6, height=3.0)
            paint(vein, ["#2B3E70", "#1B2748"], op=0.95, lw=4.0, sheen=0.2,
                  line="#8FB0F0")
            vein.move_to([vx, vy, 0])
            hl = Line([vx - 3.9, vy + 1.25, 0], [vx + 3.9, vy + 1.25, 0],
                      stroke_color="#FFFFFF", stroke_width=3, stroke_opacity=0.18)
            rng = np.random.RandomState(12)
            others = VGroup()
            pts = []
            for _ in range(160):
                x = rng.uniform(vx - 3.85, vx + 3.85)
                y = rng.uniform(vy - 0.95, vy + 0.95)
                if all((x - a) ** 2 + (y - b) ** 2 > 0.22 for a, b in pts) \
                        and abs(x - (vx + 0.2)) + abs(y - vy) > 0.85:
                    pts.append((x, y))
            for (x, y) in pts[:34]:
                c = plain_rbc(0.14, False)
                c.rotate(rng.uniform(-0.5, 0.5))
                c.move_to([x, y, 0])
                others.add(c)
            star = rbc(0.18, False).move_to([vx + 0.2, vy, 0])
            arrows = VGroup(*[arrow([vx - 3.8 + 1.4 * k, -1.35, 0],
                                    [vx - 3.1 + 1.4 * k, -1.35, 0], DEOX_L, 5, 0.18)
                              for k in range(6)])
            t0 = P(T("MILLIONS OF CELLS ARE MOVING...", 30, CHALK_WHITE,
                     max_w=8.4), vx, -2.15)
            t1 = P(T("FOLLOW JUST ONE.", 40, CHALK_YELLOW), vx, -2.15)
            panel_ = pcard("YOUR CELL", ["Oxygen status: LOW", "Destination: ?",
                                         "Heart visits: 0"], CHALK_CYAN,
                           size=22, head_size=28, pad=0.16, gap=0.08)
            P(panel_, PX, 0.95)
            q = pcard("", ["CAN YOU TRACE ITS", "COMPLETE JOURNEY?"], CHALK_PINK,
                      size=22, pad=0.14, gap=0.07)
            P(q, PX, -1.15)
            self.cue(tr, "b0", FadeIn(vein), FadeIn(hl), FadeIn(others),
                     FadeIn(arrows), FadeIn(t0), sfx="pop")
            self.cue(tr, "b1", others.animate.set_opacity(0.25),
                     FadeIn(star, scale=1.4), ReplacementTransform(t0, t1),
                     sfx="ding")
            self.cue(tr, "b2", FadeIn(panel_), FadeIn(q), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 2 ----
    def beat_s2(self):
        with self.narrate("s2") as tr:
            self.heading("Returning from the Body")
            m = self.put_map()
            cell = self.rbc_at(F(-2.3, 0) * [1, 0, 0] + np.array([0, BAND_Y, 0]),
                               False)
            others = VGroup(*[plain_rbc(0.11, False).move_to(SVC_OUT[0]),
                              plain_rbc(0.11, False).move_to(SVC_OUT[1])])
            st = status("OXYGEN: LOW", DEOX_L)
            ct = counter(0)
            chain_ = chain_v(["BODY", "VENA CAVA", "RIGHT ATRIUM"],
                             [CHALK_WHITE, DEOX_L, CHALK_CYAN], 22, PW)
            panel_ = stack([ct, st, chain_], top=PAN_TOP, gap=0.22)
            lab_svc = side_label(["SUPERIOR", "VENA CAVA"], DEOX_L, (LX, -0.33),
                                 TH.b((-1.05, 1.0)))
            lab_ra = side_label(["RIGHT", "ATRIUM"], CHALK_CYAN, (LX, -1.13),
                                TH.b(TX.PTS["RA"]) + LEFT * 0.05)
            lab_ivc = side_label(["INFERIOR", "VENA CAVA"], DEOX_L, (LX, -1.93),
                                 TH.b((-1.05, -1.40)))
            self.add(ct, st)
            self.add(cell)
            self.cue(tr, "b0", FadeIn(cell), FadeIn(chain_), sfx="pop")
            self.cue(tr, "b1", self.travel(cell, [cell.get_center(), IVC_OUT[0]],
                                           0.8), sfx="whoosh")
            self.cue(tr, "b2", FadeIn(lab_svc), FadeIn(others),
                     self.travel(others[0], SVC_OUT + M_(TX.SVC_IN), 2.4),
                     sfx="click")
            self.cue(tr, "b3", FadeIn(lab_ivc),
                     self.travel(cell, IVC_OUT + M_(TX.IVC_IN), 2.6),
                     sfx="click")
            self.cue(tr, "b4", FadeIn(lab_ra),
                     ReplacementTransform(ct, counter(1).move_to(ct)), sfx="ding")
            self.cue(tr, "b5", Indicate(chain_, color=CHALK_YELLOW,
                                        scale_factor=1.04), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ heart ------
    def put_heart(self):
        heart = real_heart(HEART_H)
        heart.move_to(HC)
        self.add(heart)
        return heart

    def side_tags(self):
        r_ = tag("RIGHT SIDE").move_to([LX, TAG_Y, 0])
        l_ = tag("LEFT SIDE").move_to([5.35, TAG_Y - 0.08, 0])
        return r_, l_

    # ------------------------------------------------------------ scene 3 ----
    def beat_s3(self):
        with self.narrate("s3") as tr:
            self.heading("Right Atrium to Right Ventricle")
            heart = self.put_heart()
            ra, rv, tri = heart.at("RA"), heart.at("RV"), heart.at("TRI")
            cell = rbc(0.18, False).move_to(ra)
            side_r, side_l = self.side_tags()
            c_ra = side_label(["RIGHT", "ATRIUM"], CHALK_CYAN, (LX, ra[1]),
                              ra + LEFT * 0.40)
            c_rv = side_label(["RIGHT", "VENTRICLE"], CHALK_CYAN, (LX, rv[1]),
                              rv + LEFT * 0.35)
            c_tri = callout("TRICUSPID\nVALVE", CHALK_YELLOW,
                            [1.95, tri[1] - 0.60, 0], tri + RIGHT * 0.12, 19)
            st = pchip("OXYGEN: LOW", DEOX_L, 24, h=0.58)
            ow = pchip("ONE-WAY FLOW", CHALK_GREEN, 26, h=0.62)
            q = pcard("", ["WHERE DOES THIS", "VENTRICLE SEND", "THE BLOOD?"],
                      CHALK_PINK, size=24, pad=0.14, gap=0.06)
            stack([st, ow, q], top=PAN_TOP, gap=0.24)
            ring = Circle(radius=0.72, stroke_color=CHALK_YELLOW, stroke_width=4,
                          fill_opacity=0).move_to(rv)
            g_closed = gate(tri, False)
            g_open = gate(tri, True)
            cr = credit(ATTR_HEART)
            self.cue(tr, "b0", FadeIn(cell), FadeIn(side_r), FadeIn(side_l),
                     FadeIn(c_ra), FadeIn(c_tri), FadeIn(st), FadeIn(g_closed),
                     FadeIn(cr), sfx="pop")
            self.cue(tr, "b1", FadeIn(c_rv), Transform(g_closed, g_open),
                     cell.animate.move_to(rv), sfx="whoosh", rt=1.3)
            self.cue(tr, "b2", Transform(g_closed, gate(tri, False)),
                     FadeIn(ow), sfx="click", rt=0.6)
            self.go(cell.animate.shift(UP * 0.30), rt=0.25)
            self.go(cell.animate.shift(DOWN * 0.30), rt=0.25)
            self.cue(tr, "b3", Create(ring), sfx="ding")
            self.cue(tr, "b4", FadeIn(q), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 4 ----
    def beat_s4(self):
        with self.narrate("s4") as tr:
            self.heading("The First Loop: Heart to Lungs")
            m = self.put_map()
            cell = self.rbc_at(TH.b(TX.PTS["RV"]), False)
            st = status("OXYGEN: LOW", DEOX_L)
            ct = counter(1)
            card = pcard("", ["ARTERY = ALWAYS", "OXYGENATED?"], CHALK_PINK,
                         size=24, pad=0.16, gap=0.07)
            nope = pchip("NOT ALWAYS", CHALK_RED, 28, h=0.60)
            pa_note = pcard("", ["PULMONARY ARTERY:", "DEOXYGENATED",
                                 "BLOOD TO LUNGS"], DEOX_L, size=21,
                            pad=0.16, gap=0.06)
            chain_ = chain_v(["RIGHT VENTRICLE", "PULMONARY ARTERY", "LUNGS"],
                             [CHALK_CYAN, DEOX_L, CHALK_PINK], 21, PW, h=0.46)
            pc = pchip("PULMONARY\nCIRCULATION", CHALK_YELLOW, 22, w=PW)
            top = [ct, st]
            stack(top + [card], top=PAN_TOP, gap=0.16)
            stack(top + [card, nope], top=PAN_TOP, gap=0.16)
            stack(top + [pa_note], top=PAN_TOP, gap=0.16)
            stack(top + [chain_, pc], top=PAN_TOP, gap=0.16)
            lab_pa = side_label(["PULMONARY", "ARTERY"], DEOX_L, (LX, -0.33),
                                TH.b((0.80, 1.05)))
            lab_lu = side_label(["LUNGS"], CHALK_PINK, (LX, -1.13),
                                TH.b(TX.PTS["LUNG_L"]))
            self.add(ct, st, cell)
            self.cue(tr, "b0", self.travel(cell, M_(TX.RV_TRUNK) + M_(TX.PA_PATH),
                                           2.6), FadeIn(lab_pa), sfx="whoosh")
            self.cue(tr, "b1", FadeIn(card), sfx="click")
            self.cue(tr, "b1", FadeIn(nope), sfx=None)
            self.cue(tr, "b2", FadeOut(card), FadeOut(nope), FadeIn(pa_note),
                     FadeIn(lab_lu), sfx="ding")
            self.cue(tr, "b3", FadeOut(pa_note), FadeIn(chain_), FadeIn(pc),
                     sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 5 ----
    def beat_s5(self):
        with self.narrate("s5") as tr:
            self.heading("At the Lungs: Oxygen Is Picked Up")
            cy = 0.12
            # left card: the real alveoli
            cx_l = -4.55
            boxL = panel(3.70, 4.05, CHALK_PINK, opacity=0.35)
            P(boxL, cx_l, cy)
            alv = alveolus_view(3.30)
            alv.move_to([cx_l, cy + 0.12, 0])
            capL = lines(["ALVEOLI AND", "THEIR CAPILLARIES"], 17, CHALK_PINK,
                         buff=0.03)
            capL.move_to([cx_l, cy - 1.68, 0])
            cardL = VGroup(boxL, alv, capL)
            # right card: one capillary, the cell and the oxygen
            cx_r = -0.05
            kk = 1.45
            boxR = panel(5.20, 4.05, CHALK_PINK, opacity=0.35)
            P(boxR, cx_r, cy)
            ins = lung_inset(3.30, 2.50)
            ins.scale(kk)
            ins.move_to([cx_r, cy + 0.10, 0])
            pts = [np.array([p[0] * kk + cx_r, p[1] * kk + cy + 0.10, 0.0])
                   for p in ins.cap_pts]
            pts_t = [(p[0], p[1]) for p in pts]
            cell = rbc(0.19, False).move_to(pts[0])

            def under(txt, col, x, target):
                lab = pchip(txt, col, 18, w=2.0)
                lab.move_to([x, cy - 2.02 - 0.38, 0])
                ln = Line(lab.get_top(), np.array([target[0], target[1], 0.0]),
                          stroke_color=col, stroke_width=2.4)
                return VGroup(lab, ln, Dot(np.array([target[0], target[1], 0.0]),
                                           radius=0.05, color=col))
            c_cap = under("CAPILLARY", CHALK_YELLOW, cx_r - 1.35,
                          pts[1] + DOWN * 0.05)
            c_pv = under("PULMONARY\nVEIN", OXY_L, cx_r + 1.35, pts[-2])
            st0 = pchip("BEFORE LUNGS:\nDEOXYGENATED", DEOX_L, 22, w=PW)
            st1 = pchip("NOW:\nOXYGENATED", OXY_L, 24, w=PW)
            exc = pcard("EXCEPTION", ["PULMONARY VEIN", "CARRIES", "OXYGENATED BLOOD"],
                        OXY_L, size=20, head_size=24, pad=0.14, gap=0.05)
            rule = pcard("", ["ARTERY: AWAY", "FROM THE HEART", "VEIN: TOWARDS",
                              "THE HEART"], CHALK_YELLOW, size=20,
                         pad=0.14, gap=0.04)
            stk = stack([st0, exc, rule], top=PAN_TOP, gap=0.16)
            st1.move_to(st0)
            o2s = VGroup(*[o2(0.95).move_to([cx_r + dx, cy + 0.10 + dy, 0])
                           for dx, dy in ((-0.65, 0.40), (0.55, 0.35), (0.0, -0.40))])
            self.cue(tr, "b0", FadeIn(cardL), FadeIn(boxR), FadeIn(ins),
                     FadeIn(cell), sfx="pop")
            self.cue(tr, "b1", FadeIn(c_cap), sfx="click")
            self.cue(tr, "b2", FadeIn(st0), sfx="click")
            self.cue(tr, "b3", FadeIn(o2s), self.travel(cell, pts_t[:5], 2.2),
                     sfx="ding")
            new = rbc(0.19, True).move_to(cell.get_center())
            self.go(ReplacementTransform(cell, new), ReplacementTransform(st0, st1),
                    FadeOut(o2s), rt=0.8)
            cell = new
            self.cue(tr, "b3", self.travel(cell, pts_t[4:], 1.4), FadeIn(c_pv),
                     FadeIn(exc), sfx="click")
            self.cue(tr, "b4", FadeIn(rule), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 6 ----
    def beat_s6(self):
        with self.narrate("s6") as tr:
            self.heading("Left Atrium to Left Ventricle")
            heart = self.put_heart()
            la, lv, mit = heart.at("LA"), heart.at("LV"), heart.at("MIT")
            cell = rbc(0.18, True).move_to(la)
            side_r, side_l = self.side_tags()
            st = pchip("OXYGENATED", OXY_L, 24, h=0.52)
            c_la = side_label(["LEFT", "ATRIUM"], CHALK_CYAN, (1.85, la[1] + 0.55),
                              la + UP * 0.12 + RIGHT * 0.05, facing="left")
            c_mit = side_label(["MITRAL VALVE", "(BICUSPID)"], CHALK_YELLOW,
                               (1.85, mit[1] - 0.35), mit + RIGHT * 0.10,
                               facing="left")
            c_lv = side_label(["LEFT", "VENTRICLE"], CHALK_CYAN,
                              (1.85, lv[1] - 1.05), lv + RIGHT * 0.30,
                              facing="left")
            done = pcard("", ["PULMONARY LOOP", "COMPLETE"], CHALK_GREEN,
                         size=24, pad=0.14, gap=0.06)
            visit = pchip("HEART VISITS: 2", CHALK_YELLOW, 24, h=0.56)
            nxt = pcard("", ["NEXT STOP:", "THE WHOLE BODY"], CHALK_PINK,
                        size=24, pad=0.14, gap=0.06)
            stack([st, visit, done, nxt], top=PAN_TOP, gap=0.20)
            g_closed = gate(mit, False, 0.34)
            g_open = gate(mit, True, 0.34)
            cr = credit(ATTR_HEART)
            self.cue(tr, "b0", FadeIn(cell), FadeIn(side_r), FadeIn(side_l),
                     FadeIn(st), FadeIn(c_la), FadeIn(cr), sfx="pop")
            self.cue(tr, "b1", FadeIn(done), FadeIn(visit), sfx="ding")
            self.cue(tr, "b2", FadeIn(c_mit), FadeIn(c_lv), FadeIn(g_closed),
                     sfx="click")
            self.cue(tr, "b3", Transform(g_closed, g_open),
                     cell.animate.move_to(lv), FadeIn(nxt), sfx="whoosh", rt=1.3)
            self.finish(tr)

    # ------------------------------------------------------------ scene 7 ----
    def beat_s7(self):
        with self.narrate("s7") as tr:
            self.heading("The Second Loop: Heart to Body")
            m = self.put_map()
            cell = self.rbc_at(TH.b(TX.PTS["LV"]), True)
            st = status("OXYGENATED", OXY_L)
            ct = counter(2)
            organs = VGroup(*[chip(t, CHALK_PINK, 19, w=2.3, h=0.40)
                              for t in ("BRAIN", "ARMS", "LIVER", "KIDNEYS",
                                        "LOWER BODY")]).arrange(DOWN, buff=0.11)
            for o_ in organs:
                o_._tight = True
            chain_ = chain_v(["LEFT VENTRICLE", "AORTA", "BODY"],
                             [CHALK_CYAN, OXY_L, CHALK_PINK], 21, PW, h=0.46)
            sc = pchip("SYSTEMIC CIRCULATION", CHALK_YELLOW, 20, h=0.50)
            lab_ao = callout("AORTA", OXY_L, [3.60, -2.28, 0],
                             np.array([float(F(2.30, 0)[0]) + 0.03, -2.28, 0.0]),
                             18)
            lab_lv = side_label(["LEFT", "VENTRICLE"], CHALK_CYAN, (LX, -0.90),
                                TH.b(TX.PTS["LV"]))
            stack([ct, st, organs], top=PAN_TOP, gap=0.18)
            grp_ = VGroup(chain_, sc).arrange(DOWN, buff=0.14)
            grp_.move_to(organs.get_center())
            grp_.align_to(organs, UP)
            self.add(ct, st, cell)
            self.cue(tr, "b0", self.travel(cell, M_(TX.LA_LV)[-1:] +
                                           M_(TX.LV_AORTA)[:3], 1.6),
                     FadeIn(lab_lv), sfx="whoosh")
            self.cue(tr, "b1", FadeIn(organs), FadeIn(lab_ao), sfx="click")
            self.cue(tr, "b2", FadeOut(organs), self.travel(
                cell, M_(TX.LV_AORTA)[2:] + AORTA_OUT[1:], 3.0),
                FadeIn(chain_), FadeIn(sc), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 8 ----
    def beat_s8(self):
        with self.narrate("s8") as tr:
            self.heading("From the Body Back to the Heart")
            ix, iy = -1.75, 0.14
            kk = 1.50
            box = panel(7.7, 3.95, "#F4A877", opacity=0.30)
            P(box, ix, iy)
            ins = tissue_inset(4.6, 2.7)
            ins.scale(kk)
            ins.move_to([ix, iy + 0.05, 0])
            pts = [np.array([p[0] * kk + ix, p[1] * kk + iy + 0.05, 0.0])
                   for p in ins.cap_pts]
            pts_t = [(p[0], p[1]) for p in pts]
            cell = rbc(0.19, True).move_to(pts[0])
            st0 = pchip("ARRIVES:\nOXYGENATED", OXY_L, 22, w=PW)
            st1 = pchip("LEAVES:\nDEOXYGENATED", DEOX_L, 22, w=PW)
            o2s = VGroup(*[o2(0.8).move_to(pts[3] + np.array([dx, dy, 0]))
                           for dx, dy in ((-0.85, 0.65), (0.0, 0.75), (0.85, 0.65))])
            ch = chain(["BODY", "VEINS", "VENA CAVA", "RIGHT ATRIUM"],
                       [CHALK_WHITE, DEOX_L, DEOX_L, CHALK_CYAN], 21)
            fit(ch, 9.8)
            P(ch, ix, -2.45)
            cap_c = pcard("", ["CAPILLARIES JOIN", "TO FORM VEINS"], CHALK_CYAN,
                          size=22, pad=0.14, gap=0.06)
            done = pcard("", ["SAME CELL,", "SAME PLACE:", "ONE COMPLETE",
                              "JOURNEY"], CHALK_YELLOW, size=22,
                         pad=0.14, gap=0.05)
            stack([st0, cap_c, done], top=PAN_TOP, gap=0.22)
            st1.move_to(st0)
            self.add(box)
            self.cue(tr, "b0", FadeIn(ins), FadeIn(cell), FadeIn(st0), sfx="pop")
            self.cue(tr, "b0", self.travel(cell, pts_t[:4], 1.6), FadeIn(o2s),
                     sfx="click")
            self.go(*[o.animate.shift(UP * 0.30) for o in o2s], rt=0.8)
            new = rbc(0.19, False).move_to(cell.get_center())
            self.cue(tr, "b1", ReplacementTransform(cell, new),
                     ReplacementTransform(st0, st1), FadeOut(o2s), sfx="ding",
                     rt=0.8)
            cell = new
            self.cue(tr, "b2", self.travel(cell, pts_t[3:], 1.6), FadeIn(cap_c),
                     sfx="click")
            self.cue(tr, "b3", FadeIn(ch), sfx="click")
            self.cue(tr, "b4", FadeIn(done), sfx="success")
            self.finish(tr)

    # ------------------------------------------------------------ scene 9 ----
    def beat_s9(self):
        with self.narrate("s9") as tr:
            self.heading("Why It Is Called Double Circulation")
            m = self.put_map()
            loop1 = M_(TX.RV_TRUNK) + M_(TX.PA_PATH) + M_(TX.PV_PATH) + \
                M_(TX.LA_LV)[:1]
            xr, xl = float(F(1.0, 0)[0]), float(F(-1.0, 0)[0])
            loop2 = M_(TX.LV_AORTA) + AORTA_OUT[1:] + \
                [np.array([xr, BAND_Y, 0.0]), np.array([xl, BAND_Y, 0.0])] + \
                IVC_OUT[::-1][::-1] + M_(TX.IVC_IN)
            g1 = TX.path_vm(loop1).set_stroke(CHALK_CYAN, 13, opacity=0.65)
            g2 = TX.path_vm(loop2).set_stroke(CHALK_YELLOW, 13, opacity=0.55)
            l1 = pchip("PULMONARY CIRCULATION", CHALK_CYAN, 19, h=0.50)
            l2 = pchip("SYSTEMIC CIRCULATION", CHALK_YELLOW, 19, h=0.50)
            ct1 = counter(0)
            c1, c2 = counter(1), counter(2)
            two = pcard("", ["TWO PASSES", "THROUGH THE HEART"], CHALK_PINK,
                        size=23, pad=0.14, gap=0.06)
            dbl = pchip("DOUBLE\nCIRCULATION", CHALK_GREEN, 24)
            formula = pcard("", ["PULMONARY + SYSTEMIC", "= DOUBLE CIRCULATION"],
                            CHALK_GREEN, size=19, pad=0.14, gap=0.06)
            stack([ct1, l1, l2, two, formula], top=PAN_TOP, gap=0.16)
            dbl.move_to(two)
            for it in (l1, l2, two, formula):
                it.set_opacity(0)
            dbl.set_opacity(0)
            self.add(ct1)
            self.cue(tr, "b0", Create(g1), l1.animate.set_opacity(1),
                     ReplacementTransform(ct1, c1.move_to(ct1)), sfx="pop", rt=1.5)
            self.cue(tr, "b1", Create(g2), l2.animate.set_opacity(1),
                     ReplacementTransform(c1, c2.move_to(ct1)), sfx="click", rt=1.5)
            self.cue(tr, "b2", two.animate.set_opacity(1), sfx="click")
            self.cue(tr, "b3", two.animate.set_opacity(0),
                     dbl.animate.set_opacity(1), sfx="ding")
            self.cue(tr, "b4", formula.animate.set_opacity(1), sfx="success")
            self.finish(tr)

    # ----------------------------------------------------------- scene 10 ----
    def beat_s10(self):
        with self.narrate("s10q") as tr:
            self.heading("YOUR TURN", "Be the red blood cell: you are in the RIGHT ATRIUM.",
                         CHALK_PINK)
            specs = [("A", "Where do you go next?", "?", CHALK_CYAN),
                     ("B", "Which vessel leads to the lungs?", "?", DEOX_L),
                     ("C", "After the lungs, which chamber first?", "?", OXY_L),
                     ("D", "Which vessel carries you to the body?", "?", OXY),
                     ("E", "Why 'double' circulation?", "?", CHALK_GREEN)]
            rows = [qa_row(l, q, a, c, w=11.8, h=0.76, size=26)
                    for l, q, a, c in specs]
            ys = (1.28, 0.36, -0.56, -1.48, -2.40)
            for r_, y in zip(rows, ys):
                P(r_, CX, y)
            for k, r_ in enumerate(rows):
                self.cue(tr, f"b{k}", FadeIn(r_), sfx="pop" if k == 0 else "click")
            self.finish(tr)
            self._rows = rows
            self._specs = specs
        self.think_clock()
        with self.narrate("s10a", reset=False) as tr:
            answers = ["RIGHT VENTRICLE", "PULMONARY ARTERY", "LEFT ATRIUM", "AORTA",
                       "TWICE THROUGH HEART"]
            rows = self._rows
            for k in range(5):
                new = T(answers[k], 26, self._specs[k][3], max_w=4.2)
                new.move_to(rows[k].slot.get_center())
                new.align_to(rows[k].slot, RIGHT)
                self.cue(tr, f"b{k}", ReplacementTransform(rows[k].slot, new),
                         sfx="click" if k < 4 else "success", rt=0.5)
            self.finish(tr)

    # ----------------------------------------------------------- scene 11 ----
    def beat_s11(self):
        with self.narrate("s11") as tr:
            head = self.heading("The Whole Journey in One Go")
            D, O = DEOX_L, OXY_L

            def cp(txt, col):
                c_ = chip(txt, col, 21, h=0.50)
                c_._tight = True
                return c_
            names = [("BODY", CHALK_WHITE), ("VENA CAVA", D), ("RIGHT ATRIUM", D),
                     ("RIGHT VENTRICLE", D), ("PULMONARY ARTERY", D),
                     ("LUNGS", CHALK_PINK), ("PULMONARY VEINS", O),
                     ("LEFT ATRIUM", O), ("LEFT VENTRICLE", O), ("AORTA", O),
                     ("BODY", CHALK_WHITE)]
            chips = [cp(t, c) for t, c in names]

            def row(idx, y):
                parts = []
                for n_, k in enumerate(idx):
                    parts.append(chips[k])
                    if n_ < len(idx) - 1:
                        parts.append(arrow([0, 0, 0], [0.34, 0, 0], CHALK_WHITE,
                                           5, 0.16))
                r_ = VGroup(*parts).arrange(RIGHT, buff=0.12)
                fit(r_, 11.9)
                return P(r_, CX, y)
            r1 = row([0, 1, 2, 3], 1.62)
            r2 = row([4, 5, 6, 7], 0.67)
            r3 = row([8, 9, 10], -0.28)

            def elbow(ca, cb):
                """last chip of one row -> first chip of the next row"""
                xa, xb = ca.get_center()[0], cb.get_center()[0]
                ya, yb = ca.get_bottom()[1] - 0.02, cb.get_top()[1] + 0.02
                ym = (ya + yb) / 2
                kw = dict(stroke_color=CHALK_WHITE, stroke_width=5)
                return VGroup(Line([xa, ya, 0], [xa, ym, 0], **kw),
                              Line([xa, ym, 0], [xb, ym, 0], **kw),
                              arrow([xb, ym, 0], [xb, yb, 0], CHALK_WHITE, 5,
                                    0.16))
            ar1 = elbow(chips[3], chips[4])
            ar2 = elbow(chips[7], chips[8])
            mem = tcard("", ["RIGHT  >  LUNGS", "LEFT  >  BODY"], CHALK_YELLOW,
                        w=5.2, body_size=32, pad=0.16, gap=0.08)
            P(mem, CX, -1.50)
            frm = chip("PULMONARY + SYSTEMIC = DOUBLE CIRCULATION", CHALK_GREEN,
                       24)
            frm._tight = True
            P(frm, CX, -2.65)
            thanks = P(T("Thank You for Watching!", 60, CHALK_WHITE, max_w=11.8),
                       CX, 0.60)
            bye = P(T("See you in the next lesson :)", 44, CHALK_YELLOW,
                      max_w=11.0), CX, -0.75)
            self.cue(tr, "b0", FadeIn(r1), sfx="pop")
            self.cue(tr, "b1", FadeIn(ar1), FadeIn(r2), sfx="click")
            self.cue(tr, "b2", FadeIn(ar2), FadeIn(r3), sfx="click")
            self.cue(tr, "b3", Indicate(r3, color=CHALK_YELLOW,
                                        scale_factor=1.03), sfx=None)
            self.cue(tr, "b4", FadeIn(mem), sfx="ding")
            self.cue(tr, "b5", FadeIn(frm), sfx="success", snap="grid")
            self.hold(tr, "b6")
            keep = [m_ for m_ in self.mobjects if m_ not in self.fixtures]
            self.go(*[FadeOut(m_) for m_ in keep], rt=0.6)
            self.cue(tr, "b6", FadeIn(thanks, shift=UP * 0.1), sfx=None)
            self.cue(tr, "b7", FadeIn(bye, shift=UP * 0.1), sfx=None)
            self.finish(tr)
        if not self.still:
            self.wait(END_HOLD)

"""Board furniture and narration for Storyboard 04 -- Compounding Half-Yearly,
Quarterly & Applications to Population Growth and Depreciation, Class 8
Mathematics, Chapter 5 (Comparing Quantities using Proportion).

This file is *spliced*, never imported: assemble_periods.py grafts it into the
proven head of the Chapter 3 quadrilaterals set, so the theme names (CHALK_*,
FONT, BOARD_*), `board_text`, `chalk_math`, `appear` and the pacing helpers
(`rt`, `quick`, `leftover`) are already defined above it.

The furniture is this video's compounding kit:

  * `clock_face`    -- the one-year dial (rim + twelve chalk ticks),
  * `clock_sectors` -- the dial's fill, in 1 / 2 / 4 equal pie sectors, so the
                       same object visibly splits as the conversion period
                       shortens,
  * `rate_card`     -- the rate the dial carries (R -> R/2 -> R/4),
  * `coin_stack` / `rupee_note` -- the money, drawn as filled discs and notes,
  * `house` / `village` / `person_icon` -- the population that grows,
  * `tv_icon` / `value_bar` -- the value that depreciates,
  * `bounce_track`  -- the textbook's ball losing height at every bounce,
  * `meter`         -- growth up against depreciation down,
  * `wrong_card` / `tick` -- the drawn cross and tick (Segoe Print has neither).

Everything is drawn as filled, shaded geometry -- pie sectors with chalk rims,
coins with thickness, houses with roofs and doors, a television with a stand --
never as a bare outline.
"""
from __future__ import annotations

import numpy as np

# ------------------------------------------------------------ board layout --
# (this section is spliced into a head whose own imports omit Arc, Ellipse and
#  Sector; Dot, Circle, Line, DashedLine, Rectangle, Polygon, RoundedRectangle,
#  Square, Arrow, VGroup, UP, DOWN, LEFT, RIGHT, DEGREES, TAU, PI and np are
#  already imported by the head)
from manim import Arc, Ellipse, Sector  # noqa: E402,F401

# Board layout shared by every scene of this video.
ROW_Y = 2.72             # every scene heading sits on this line
SUB_Y = 2.16             # the one-line sub-heading under it
BANNER_Y = -1.15         # the closing banner, above the strip
# The burned-in caption grows up from the bottom of the frame: a one-line cue
# starts at y = -3.38 and a wrapped two-line cue reaches y = -2.93 (measured on
# the series' own burned 360p cuts), so every closing strip sits at -1.80 and
# nothing at all sits below CAPTION_SAFE_Y = -2.00 -- audited by the
# IN-CAPTION-BAND check.
STRIP_Y = -1.80
CAPTION_SAFE_Y = -2.00

# The two content bands.  Cards are 0.94 tall, so their TEXT boxes stay at least
# 0.25 units apart vertically at these centres -- the audits measure text.
BAND_A = 0.70            # the upper band (the working, the formula cards)
BAND_B = -0.50           # the lower band (the result of the upper band)

PANEL_FILL = "#16202B"
CARD_W = 3.30            # the standard card width
CARD_H = 0.94            # the standard card height
CHIP_H = 0.50
MARK_SIZE = 18           # ONE letter size for every labelled figure
CLOCK_R = 0.85           # the compounding dial's radius
CLOCK_FILL = "#0E1A14"
PLOT_COLORS = (CHALK_GREEN, CHALK_CYAN, CHALK_AMBER, CHALK_PINK)

# The figures this video works with.  The textbook's own numbers: Rs 1,000 at
# 10% p.a. compounded half-yearly, a village of 6,250 growing 8% a year, a ball
# dropped from 25 m losing 10% at each bounce, and the challenge amounts.
PRINCIPAL = 1000
RATE_PA = 10
AMOUNT_HALF = 1102.50
CI_HALF = 102.50
VILLAGE0 = 6250
GROWTH_PC = 8
VILLAGE2 = 7290
BALL_H0 = 25
BALL_H2 = 20.25
TV_PRICE = 21000
CHALLENGE_A = "Rs 13,891.50"


# ---------------------------------------------------------------- furniture --
def write_text_long(path, text: str) -> None:
    """Write a text file, through the extended-length path when needed.

    This topic's media paths -- `...\\media\\videos\\
    compounding_periods_half_yearly_quarterly_depreciation\\360p30\\<Class>.real.srt`
    -- run past the 260-character MAX_PATH limit, which is why the chapter
    pipeline renders into the short `D:\\m3` media dir and copies the result back
    here.  The copy-back and this ground-truth SRT write therefore fall back to
    the ``\\\\?\\`` extended form when the plain path is too long for the OS.
    """
    try:
        Path(path).write_text(text, encoding="utf-8")
    except OSError:
        with open("\\\\?\\" + str(Path(path).resolve()), "w",
                  encoding="utf-8") as fh:
            fh.write(text)


def at(mob, x, y):
    """Pin a mobject to a board coordinate."""
    return mob.move_to(np.array([float(x), float(y), 0.0]))


def row_centres(half_widths, gap, cx=BOARD_CX):
    """x centres for a row of elements whose ink is `gap` apart.

    The row's combined ink is centred on `cx` (the green board's centre line) and
    the elements of a row are not equally wide, so equal centre spacing is NOT
    equal spacing on the board: this returns the centres that leave exactly `gap`
    units of clear air between neighbours.
    """
    total = 2.0 * sum(half_widths) + gap * (len(half_widths) - 1)
    x = cx - total / 2.0
    centres = []
    for half in half_widths:
        centres.append(x + half)
        x += 2.0 * half + gap
    return tuple(centres)


def panel(width, height, color=CHALK_WHITE, opacity=0.6, radius=0.10,
          stroke=1.9):
    """A rounded panel: the box every card and chip is drawn on."""
    return RoundedRectangle(corner_radius=radius, width=width, height=height,
                            stroke_color=color, stroke_width=stroke,
                            fill_color=PANEL_FILL, fill_opacity=opacity)


def chip(text, color=CHALK_CYAN, size=14, width=None, height=CHIP_H,
         fill=PANEL_FILL):
    """A small labelled chip.  Its box is cut to its own label, so the lettering
    can never spill outside the panel (the audit measures that overflow)."""
    lab = board_text(text, size, color, "BOLD")
    box = RoundedRectangle(corner_radius=0.09,
                           width=width or (lab.width + 0.40), height=height,
                           stroke_color=color, stroke_width=1.7,
                           fill_color=fill, fill_opacity=0.7)
    lab.move_to(box.get_center())
    grp = VGroup(box, lab)
    grp.box, grp.label = box, lab
    return grp


def note_card(head, lines, color=CHALK_CYAN, width=None, head_size=15,
              line_size=13, gap=0.28, buff=0.24, pad=0.44):
    """A card with a bold head line and one or two body lines under it.

    Head and body are held `gap` apart and the box is cut to the finished
    content, so the pair passes both the clearance audit (which flags any two
    texts closer than 0.22) and the overflow check (a fixed box height once let
    a two-line body hang out of its card).
    """
    h = board_text(head, head_size, color, "BOLD")
    body = VGroup(*[board_text(line, line_size, CHALK_WHITE, "BOLD")
                    for line in lines]).arrange(DOWN, buff=buff)
    content = VGroup(h, body).arrange(DOWN, buff=gap)
    box = panel(width or (content.width + pad), content.height + pad, color)
    content.move_to(box.get_center())
    grp = VGroup(box, content)
    grp.box, grp.head, grp.body = box, h, body
    return grp


def coin_stack(cx, cy, n=3, scale=1.0, color=CHALK_YELLOW):
    """A stack of rupee coins: filled discs WITH THICKNESS, drawn bottom-up.

    Each coin is a dark milled edge under a bright face, so the stack reads as
    real metal on the board rather than as a flat outline.
    """
    discs = VGroup()
    for i in range(n):
        y = cy + 0.072 * i * scale
        edge = Ellipse(width=0.44 * scale, height=0.16 * scale, stroke_width=0,
                       fill_color="#8A6A18", fill_opacity=0.85)
        edge.move_to(np.array([cx, y - 0.030 * scale, 0.0]))
        face = Ellipse(width=0.44 * scale, height=0.16 * scale,
                       stroke_color=color, stroke_width=1.5,
                       fill_color=color, fill_opacity=0.45)
        face.move_to(np.array([cx, y, 0.0]))
        discs.add(edge, face)
    return discs


def note_stack(cx, cy, n=3, text="Rs 1000", size=12, color=CHALK_YELLOW):
    """A bundle of drawn rupee notes: filled rectangles fanned out, top labelled.

    The rectangles are cut to the label plus 0.22 of chalk margin on every side
    (a `Rectangle` is a `Polygon` to the audit, which samples its perimeter
    against lettering).
    """
    lab = board_text(text, size, color, "BOLD")
    w = lab.width + 0.44
    h = max(lab.height + 0.24, 0.40)
    grp = VGroup()
    for i in range(n):
        b = Rectangle(width=w, height=h, stroke_color=color, stroke_width=1.5,
                      fill_color=color, fill_opacity=0.18)
        b.move_to(np.array([cx - 0.045 * (n - 1 - i),
                            cy - 0.050 * (n - 1 - i), 0.0]))
        grp.add(b)
    lab.move_to(grp[-1].get_center())
    grp.add(lab)
    grp.label = lab
    return grp


def clock_face(cx, cy, r=CLOCK_R, color=CHALK_CYAN):
    """The one-year dial: a filled face with a chalk rim and twelve ticks.

    The ticks stay in the outer tenth of the dial, clear of the words chalked
    at its centre (a tick crossing the middle of the dial ran through the
    period label).
    """
    rim = Circle(radius=r, stroke_color=color, stroke_width=2.6,
                 fill_color=CLOCK_FILL, fill_opacity=0.55)
    rim.move_to(np.array([cx, cy, 0.0]))
    ticks = VGroup()
    for k in range(12):
        a = (90 - 30 * k) * DEGREES
        d = np.array([np.cos(a), np.sin(a), 0.0])
        p = np.array([cx, cy, 0.0])
        ticks.add(Line(p + d * r * 0.90, p + d * r * 0.99,
                       stroke_color=color, stroke_width=1.3))
    return VGroup(rim, ticks)


def clock_sectors(cx, cy, n, r=CLOCK_R, colors=PLOT_COLORS):
    """The dial's fill, cut into `n` equal pie sectors.

    n = 1 is the whole year, n = 2 is two half-years and n = 4 is four
    quarters.  Each piece is a *filled* sector with its own chalk rim, so the
    same object is seen to split rather than being redrawn.
    """
    c = np.array([cx, cy, 0.0])
    grp = VGroup()
    for k in range(n):
        col = colors[k % len(colors)]
        grp.add(Sector(radius=r * 0.93,
                       start_angle=90 * DEGREES - k * TAU / n,
                       angle=TAU / n, arc_center=c,
                       stroke_color=col, stroke_width=1.8,
                       fill_color=col, fill_opacity=0.26))
    return grp


def dial_label(cx, cy, text, color=CHALK_WHITE, size=13):
    """The words chalked inside the dial (1 YEAR, HALF-YEARLY, QUARTERLY).

    Kept short and small: the widest label must stay inside the ring of ticks.
    """
    return board_text(text, size, color, "BOLD").move_to(
        np.array([cx, cy, 0.0]))


def rate_card(sym, color=CHALK_AMBER, size=24, width=1.46, height=0.62):
    """The rate the dial carries -- a maths object in its own chalk box."""
    tex = chalk_math(sym, size=size, color=color)
    box = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                           stroke_color=color, stroke_width=2.0,
                           fill_color=PANEL_FILL, fill_opacity=0.65)
    tex.move_to(box.get_center())
    grp = VGroup(box, tex)
    grp.box, grp.tex = box, tex
    return grp


def person_icon(cx, cy, color=CHALK_CYAN, scale=1.0):
    """A small filled figure: a round head over a pair of shoulders."""
    head = Circle(radius=0.10 * scale, stroke_width=0,
                  fill_color=color, fill_opacity=0.9)
    head.move_to(np.array([cx, cy + 0.15 * scale, 0.0]))
    body = Ellipse(width=0.38 * scale, height=0.26 * scale, stroke_width=0,
                   fill_color=color, fill_opacity=0.5)
    body.move_to(np.array([cx, cy - 0.10 * scale, 0.0]))
    return VGroup(body, head)


def house(cx, cy, s=1.0, color=CHALK_AMBER):
    """A drawn house: a filled wall, a pitched roof and a doorway."""
    body = Rectangle(width=0.46 * s, height=0.34 * s, stroke_color=color,
                     stroke_width=1.5, fill_color=color, fill_opacity=0.40)
    body.move_to(np.array([cx, cy - 0.07 * s, 0.0]))
    roof = Polygon(np.array([cx - 0.30 * s, cy + 0.10 * s, 0.0]),
                   np.array([cx + 0.30 * s, cy + 0.10 * s, 0.0]),
                   np.array([cx, cy + 0.34 * s, 0.0]),
                   stroke_color=CHALK_PINK, stroke_width=1.5,
                   fill_color=CHALK_PINK, fill_opacity=0.42)
    door = Rectangle(width=0.12 * s, height=0.17 * s, stroke_width=0,
                     fill_color=PANEL_FILL, fill_opacity=0.9)
    door.move_to(np.array([cx, cy - 0.16 * s, 0.0]))
    return VGroup(body, roof, door)


def village(cx, cy, color=CHALK_AMBER, s=1.15):
    """A drawn village: three houses and their people -- the population that
    grows.  Walls, pitched roofs, doorways and round heads over shoulders are
    all filled shapes, so nothing here reads as a bare outline."""
    grp = VGroup()
    for k, dx in enumerate((-0.62, 0.0, 0.62)):
        size = s if k == 1 else s * 0.84
        grp.add(house(cx + dx, cy + (0.06 if k == 1 else 0.0), size, color))
    for dx in (-0.46, 0.02, 0.50, 0.80):
        grp.add(person_icon(cx + dx, cy - 0.46 * s, CHALK_CYAN, 0.95))
    return grp


def car_icon(cx, cy, s=1.0, color=CHALK_PINK):
    """A drawn car: a filled body, a cabin and two solid wheels."""
    body = RoundedRectangle(corner_radius=0.06, width=0.86 * s,
                            height=0.24 * s, stroke_color=color,
                            stroke_width=1.8, fill_color=color,
                            fill_opacity=0.34)
    body.move_to(np.array([cx, cy, 0.0]))
    cabin = RoundedRectangle(corner_radius=0.05, width=0.44 * s,
                             height=0.20 * s, stroke_color=color,
                             stroke_width=1.6, fill_color=color,
                             fill_opacity=0.26)
    cabin.move_to(np.array([cx - 0.04 * s, cy + 0.20 * s, 0.0]))
    wheels = VGroup()
    for dx in (-0.26 * s, 0.26 * s):
        wheels.add(Circle(radius=0.085 * s, stroke_width=0,
                          fill_color="#1B2733", fill_opacity=1.0).move_to(
            np.array([cx + dx, cy - 0.14 * s, 0.0])))
    return VGroup(body, cabin, wheels)


def tv_icon(cx, cy, s=1.0, color=CHALK_CYAN):
    """A drawn television: a filled screen on a narrow stand."""
    screen = RoundedRectangle(corner_radius=0.05, width=0.74 * s,
                              height=0.54 * s, stroke_color=color,
                              stroke_width=2.0, fill_color=color,
                              fill_opacity=0.28)
    screen.move_to(np.array([cx, cy + 0.10 * s, 0.0]))
    neck = Rectangle(width=0.16 * s, height=0.10 * s, stroke_width=0,
                     fill_color=color, fill_opacity=0.55)
    neck.move_to(np.array([cx, cy - 0.22 * s, 0.0]))
    foot = Rectangle(width=0.50 * s, height=0.06 * s, stroke_width=0,
                     fill_color=color, fill_opacity=0.45)
    foot.move_to(np.array([cx, cy - 0.30 * s, 0.0]))
    return VGroup(screen, neck, foot)


def value_bar(cx, cy, w=1.60, h=0.66, frac=1.0, color=CHALK_GREEN,
              label="100%"):
    """A value drawn as a filled bar: what is left after each depreciation.

    The bar and its label are ONE board object, so the label is never read as
    chalk sitting inside somebody else's filled box.
    """
    frame = Rectangle(width=w, height=h, stroke_color=CHALK_WHITE,
                      stroke_width=1.6, fill_color=PANEL_FILL,
                      fill_opacity=0.5)
    frame.move_to(np.array([cx, cy, 0.0]))
    fw = max(w * frac, 0.03)
    fill = Rectangle(width=fw, height=h - 0.08, stroke_width=0,
                     fill_color=color, fill_opacity=0.45)
    fill.move_to(np.array([cx - w / 2.0 + fw / 2.0, cy, 0.0]))
    lab = board_text(label, 13, color, "BOLD").move_to(np.array([cx, cy, 0.0]))
    grp = VGroup(frame, fill, lab)
    grp.frame, grp.fill, grp.label = frame, fill, lab
    return grp


def bounce_arc(p1, p2, peak, color=CHALK_WHITE, width=2.0):
    """One bounce: the arc a ball traces between two touches of the ground."""
    a = abs(p2[0] - p1[0]) / 2.0
    s = max(peak, 1e-3)
    radius = (a * a + s * s) / (2.0 * s)
    mx = (p1[0] + p2[0]) / 2.0
    cy = p1[1] - (radius - s)
    start = np.degrees(np.arctan2(p1[1] - cy, p1[0] - mx))
    ang = np.degrees(2.0 * np.arcsin(min(a / radius, 1.0)))
    return Arc(radius=radius, start_angle=start * DEGREES,
               angle=ang * DEGREES, arc_center=np.array([mx, cy, 0.0]),
               color=color, stroke_width=width)


def ball_icon(cx, cy, r=0.14, color=CHALK_PINK):
    """The ball itself: a filled disc with a highlight."""
    body = Circle(radius=r, stroke_width=0, fill_color=color,
                  fill_opacity=0.85).move_to(np.array([cx, cy, 0.0]))
    gloss = Circle(radius=r * 0.34, stroke_width=0, fill_color=CHALK_WHITE,
                   fill_opacity=0.45).move_to(
        np.array([cx - r * 0.30, cy + r * 0.30, 0.0]))
    return VGroup(body, gloss)


def bounce_track(cx, cy, h0=0.85, drop=0.9, width=1.90, color=CHALK_WHITE,
                 marker=CHALK_AMBER):
    """The textbook's bouncing ball, with all THREE HEIGHTS DRAWN.

    `cy` is the ground line, `h0` the release height (25 m).  The ball falls
    and each bounce rises to `drop` of the previous height: 22.5 m, then
    20.25 m.  The drop is a dashed vertical and every one of the three heights
    carries its own dashed level marker, so the decreasing heights are measured
    on the board instead of merely being asserted in words.  The marker lines
    are short, so they can never run into a label or the ball.
    """
    x0 = cx - width / 2.0                     # where the ball is released
    h1, h2 = h0 * drop, h0 * drop * drop
    w1, w2 = width * 0.52, width * 0.48
    p1 = (x0 + w1, cy)
    p2 = (p1[0] + w2, cy)

    ground = Line(np.array([x0 - 0.16, cy, 0.0]),
                  np.array([p2[0] + 0.16, cy, 0.0]),
                  stroke_color=color, stroke_width=1.8)
    fall = DashedLine(np.array([x0, cy, 0.0]), np.array([x0, cy + h0, 0.0]),
                      color=color, stroke_width=1.4, dash_length=0.07)
    grp = VGroup(ground, fall)
    for xa, xb, h in ((x0 + 0.20, x0 + 0.80, h0),
                      (p1[0] - 0.30, p1[0] + 0.30, h1),
                      (p2[0] - 0.34, p2[0] + 0.10, h2)):
        grp.add(DashedLine(np.array([xa, cy + h, 0.0]),
                           np.array([xb, cy + h, 0.0]),
                           color=marker, stroke_width=1.3, dash_length=0.07))
    grp.add(bounce_arc((x0, cy), p1, h1, color))
    grp.add(bounce_arc(p1, p2, h2, color))
    grp.add(ball_icon(x0, cy + h0))
    grp.ground, grp.heights = ground, (h0, h1, h2)
    return grp


def meter(cx, cy, up=1.0, down=1.0, w=0.32):
    """Growth against depreciation: one bar up, one bar down, one baseline."""
    base = Line(np.array([cx - 0.60, cy, 0.0]), np.array([cx + 0.60, cy, 0.0]),
                stroke_color=CHALK_WHITE, stroke_width=2.0)
    upbar = Rectangle(width=w, height=0.46 * up, stroke_width=0,
                      fill_color=CHALK_GREEN, fill_opacity=0.5)
    upbar.move_to(np.array([cx - 0.32, cy + 0.23 * up, 0.0]))
    dnbar = Rectangle(width=w, height=0.46 * down, stroke_width=0,
                      fill_color=CHALK_PINK, fill_opacity=0.5)
    dnbar.move_to(np.array([cx + 0.32, cy - 0.23 * down, 0.0]))
    up_lab = board_text("+", 16, CHALK_GREEN, "BOLD").move_to(
        np.array([cx - 0.32, cy + 0.46 * up + 0.16, 0.0]))
    dn_lab = board_text("-", 16, CHALK_PINK, "BOLD").move_to(
        np.array([cx + 0.32, cy - 0.46 * down - 0.16, 0.0]))
    up_grp = VGroup(base, upbar, up_lab)
    dn_grp = VGroup(dnbar, dn_lab)
    up_grp.label, dn_grp.label = up_lab, dn_lab
    return up_grp, dn_grp


def wrong_card(text, color=CHALK_RED, width=2.60, height=1.05, size=15):
    """A card holding a WRONG statement, with a drawn cross over it.

    The cross occupies the card's top half and the statement its bottom half, so
    the strike-through is unmistakable yet never comes within the 0.04 units the
    audit allows between a stroke and the lettering.  The whole card is ONE
    board object, so the strokes are never read as a line running into a box.
    """
    box = panel(width, height, color, opacity=0.7)
    cross = VGroup(
        Line(np.array([-width / 2 + 0.55, 0.14, 0.0]),
             np.array([-width / 2 + 1.05, 0.50, 0.0]),
             stroke_color=color, stroke_width=4.2),
        Line(np.array([-width / 2 + 0.55, 0.50, 0.0]),
             np.array([-width / 2 + 1.05, 0.14, 0.0]),
             stroke_color=color, stroke_width=4.2),
    )
    cross.move_to(box.get_center() + UP * (height / 2 - 0.24))
    cross.shift(RIGHT * 0.10)
    lab = board_text(text, size, color, "BOLD")
    lab.move_to(box.get_center() + DOWN * (height / 2 - 0.22))
    grp = VGroup(box, cross, lab)
    grp.box, grp.cross, grp.label = box, cross, lab
    return grp


def tick(p, color=CHALK_GREEN, s=0.16):
    """A drawn tick (Segoe Print has no tick glyph)."""
    a = np.array([p[0] - s * 0.60, p[1] + s * 0.05, 0.0])
    b = np.array([p[0] - s * 0.05, p[1] - s * 0.55, 0.0])
    c = np.array([p[0] + s * 0.65, p[1] + s * 0.75, 0.0])
    return VGroup(Line(a, b, stroke_color=color, stroke_width=3.4),
                  Line(b, c, stroke_color=color, stroke_width=3.4))


def arrow_between(p1, p2, color=CHALK_YELLOW, width=3.0, tip=0.20):
    """A short arrow from one board point to another."""
    return Arrow(np.array([p1[0], p1[1], 0.0]), np.array([p2[0], p2[1], 0.0]),
                 buff=0.0, stroke_color=color, stroke_width=width,
                 tip_length=tip, max_tip_length_to_length_ratio=0.35)


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "One thousand rupees at ten percent per annum. <bookmark mark='b0'/> "
        "Compounded every year, that money becomes one thousand one hundred "
        "rupees after one year. <bookmark mark='b1'/> But the same ten percent "
        "compounded half-yearly gives one thousand fifty rupees after six "
        "months, <bookmark mark='b2'/> and one thousand one hundred two rupees "
        "and fifty paise after a year. <bookmark mark='b3'/> Same money, same "
        "rate, more interest. <bookmark mark='b4'/> Why does the timing change "
        "the answer?"
    ),
    "s1": (
        "First, the conversion period. <bookmark mark='b0'/> The conversion "
        "period is the time interval after which the interest is added to the "
        "principal. <bookmark mark='b1'/> If interest is added once a year, the "
        "period is one full year: one turn of the clock. <bookmark mark='b2'/> "
        "If it is added every six months, that same year is cut into two equal "
        "periods. <bookmark mark='b3'/> And if it is added every three months, "
        "the year becomes four quarter periods. <bookmark mark='b4'/> So the "
        "conversion period fixes two things together, the rate for each period "
        "and how many periods there are."
    ),
    "s2": (
        "Now the half-yearly rule. <bookmark mark='b0'/> When the conversion "
        "period halves, two things change at the same time. <bookmark "
        "mark='b1'/> The rate for each period halves as well: R becomes R "
        "divided by two. <bookmark mark='b2'/> And the number of periods "
        "doubles: n becomes two n. <bookmark mark='b3'/> So the amount is P "
        "times one plus R over two hundred, all raised to two n. <bookmark "
        "mark='b4'/> Ten percent per annum compounded half-yearly means five "
        "percent for each half-year, <bookmark mark='b5'/> never ten percent "
        "every six months, and never change the exponent alone."
    ),
    "s3": (
        "Let us work it out. <bookmark mark='b0'/> Principal one thousand "
        "rupees, rate ten percent per annum, time one year, compounded "
        "half-yearly. <bookmark mark='b1'/> The rate for each half-year is ten "
        "divided by two, that is five percent. <bookmark mark='b2'/> And one "
        "year holds two half-yearly periods. <bookmark mark='b3'/> So the "
        "amount is one thousand times one point zero five squared, which is one "
        "thousand one hundred two rupees and fifty paise. <bookmark mark='b4'/> "
        "The compound interest is one thousand one hundred two point five minus "
        "one thousand, that is one hundred two rupees and fifty paise."
    ),
    "s4": (
        "A year has four quarters. <bookmark mark='b0'/> So when interest is "
        "compounded quarterly, the rate for one period becomes R divided by "
        "four, <bookmark mark='b1'/> and the number of periods becomes four n. "
        "<bookmark mark='b2'/> The amount is P times one plus R over four "
        "hundred, all raised to four n. <bookmark mark='b3'/> This is the same "
        "conversion-period rule, extended from two periods to four. <bookmark "
        "mark='b4'/> The rate and the number of periods always change together."
    ),
    "s5": (
        "The same structure answers questions about population. <bookmark "
        "mark='b0'/> A village has six thousand two hundred and fifty people, "
        "and the population grows by eight percent every year. <bookmark "
        "mark='b1'/> After one year the population is six thousand two hundred "
        "and fifty times one point zero eight, <bookmark mark='b2'/> and that "
        "new total becomes the base for the next year. <bookmark mark='b3'/> So "
        "after two years the population is six thousand two hundred and fifty "
        "times one point zero eight squared, which is seven thousand two "
        "hundred and ninety. <bookmark mark='b4'/> A repeated percentage "
        "increase is exactly the same structure as compound interest."
    ),
    "s6": (
        "Now depreciation, the mirror image. <bookmark mark='b0'/> Depreciation "
        "is a reduction in the value of an article due to use and age. "
        "<bookmark mark='b1'/> A quantity that loses R percent in each period "
        "keeps one hundred minus R percent. <bookmark mark='b2'/> Ten percent "
        "off leaves ninety percent, and the next reduction is taken from the "
        "new value. <bookmark mark='b3'/> So after two periods the value is P "
        "times zero point nine squared, and in general V is P times one minus R "
        "over one hundred, all raised to n. <bookmark mark='b4'/> A ball "
        "dropped from twenty five metres loses ten percent of its height at "
        "each bounce, so after two bounces it rises to twenty five times zero "
        "point nine squared, that is twenty point two five metres."
    ),
    "s7": (
        "One structure, three uses. <bookmark mark='b0'/> Money at compound "
        "interest and population growth both use P times one plus r, all raised "
        "to n. <bookmark mark='b1'/> Depreciation uses P times one minus r, "
        "raised to n. <bookmark mark='b2'/> A growth multiplier is greater than "
        "one, <bookmark mark='b3'/> and a depreciation multiplier is less than "
        "one. <bookmark mark='b4'/> So keep two decisions separate: how often "
        "the update happens, and whether the quantity rises or falls."
    ),
    "s8": (
        "Here is the decision map. <bookmark mark='b0'/> Step one: identify the "
        "conversion period. <bookmark mark='b1'/> Step two: find the rate for "
        "one period. <bookmark mark='b2'/> Step three: count the number of "
        "periods. <bookmark mark='b3'/> Step four: choose plus for growth, or "
        "minus for decrease. <bookmark mark='b4'/> Step five: apply that factor "
        "again and again. <bookmark mark='b5'/> Period, rate, factor, repeat: "
        "that is the whole method."
    ),
    "s9q": (
        "Your turn. Three questions. <bookmark mark='b0'/> First: twelve "
        "thousand rupees at ten percent per annum for one and a half years, "
        "compounded half-yearly. Find the amount. <bookmark mark='b1'/> Second: "
        "twelve percent per annum for two years, compounded quarterly. What is "
        "the rate for each period, and how many periods are there? <bookmark "
        "mark='b2'/> Third: a television costing twenty one thousand rupees "
        "depreciates by five percent in one year. What is it worth now? "
        "<bookmark mark='b3'/> And a quick check: for eight percent growth, "
        "which factor do you use, and for eight percent depreciation, which "
        "factor?"
    ),
    "s9a": (
        "Let us check. <bookmark mark='b0'/> For A, the rate is five percent per "
        "half-year and one and a half years is three periods, so the amount is "
        "twelve thousand times one point zero five cubed, that is thirteen "
        "thousand eight hundred ninety one rupees and fifty paise. <bookmark "
        "mark='b1'/> For B, twelve divided by four is three percent per "
        "quarter, and two years is eight quarters, so the amount is P times one "
        "point zero three raised to eight. <bookmark mark='b2'/> For C, five "
        "percent depreciation leaves ninety five percent, so twenty one "
        "thousand times zero point nine five is nineteen thousand nine hundred "
        "and fifty rupees. <bookmark mark='b3'/> And the quick check: for eight "
        "percent growth use one point zero eight, and for eight percent "
        "depreciation use zero point nine two, because one minus zero point "
        "zero eight is zero point nine two."
    ),
    "s10": (
        "Let us gather the whole lesson in one place. <bookmark mark='b0'/> The "
        "conversion period has three cases: annually, the rate is R and there "
        "are n periods; <bookmark mark='b1'/> half-yearly, the rate is R over "
        "two and the periods double to two n; <bookmark mark='b2'/> quarterly, "
        "the rate is R over four and the periods become four n. <bookmark "
        "mark='b3'/> Growth uses A equals P times one plus R over one hundred, "
        "all raised to n: that is compound interest and population. <bookmark "
        "mark='b4'/> Depreciation uses V equals P times one minus R over one "
        "hundred, all raised to n: the value keeps what is left. <bookmark "
        "mark='b5'/> And the five steps: identify the conversion period, find "
        "the rate for one period, count the number of periods, choose plus for "
        "growth or minus for decrease, and apply that factor again and again."
    ),
    "s11": (
        "One last look. <bookmark mark='b0'/> The compounding clock: annually, "
        "half-yearly, quarterly, with the rate and the number of periods "
        "changing together. <bookmark mark='b1'/> Growth uses P times one plus "
        "R over one hundred, all raised to n, <bookmark mark='b2'/> and "
        "depreciation uses P times one minus R over one hundred, raised to n. "
        "<bookmark mark='b3'/> Keep the two decisions separate: how often, and "
        "up or down. <bookmark mark='b4'/> Period, rate, factor, repeat. "
        "<bookmark mark='b5'/> Thank you for watching, <bookmark mark='b6'/> "
        "and see you in the next lesson."
    ),
}

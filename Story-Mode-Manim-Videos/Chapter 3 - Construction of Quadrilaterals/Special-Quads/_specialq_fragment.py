"""Geometry frames and narration for Storyboard 07 (special quadrilaterals).

Three constructions, each driven by the property of its shape rather than by a
full set of five measurements:

  * the parallelogram B E L T -- two adjacent sides and one angle, with the
    other three angles derived from "opposite angles are equal" and
    "consecutive angles are supplementary";
  * the rhombus A B C D -- its two diagonals, which bisect each other at right
    angles, so each vertex is half a diagonal from the crossing point;
  * the square J U M P -- the rhombus rule with the extra condition that the
    diagonals are equal.

Every vertex is generated from the given numbers with vectors, never placed by
hand.
"""


# ------------------------------------------------- construction furniture ----
PARA_SCALE = 0.72       # board units per centimetre
RHOMB_SCALE = 0.68
SQUARE_SCALE = 0.80
PARA_CENTRE = np.array([BOARD_CX - 1.65, 0.20, 0.0])
RHOMB_CENTRE = np.array([BOARD_CX - 1.50, 0.05, 0.0])
SQUARE_CENTRE = np.array([BOARD_CX - 1.50, 0.05, 0.0])


def unit(deg):
    """The unit vector at `deg` degrees."""
    a = deg * DEGREES
    return np.array([np.cos(a), np.sin(a), 0.0])


def ray_point(vertex, deg, length):
    """The point `length` away from `vertex` in the direction `deg`."""
    return np.array(vertex, dtype=float) + length * unit(deg)


def dir_deg(p, q) -> float:
    """The direction from `p` to `q`, in degrees."""
    d = np.array(q, dtype=float) - np.array(p, dtype=float)
    return float(np.degrees(np.arctan2(d[1], d[0])))


def dist(p, q) -> float:
    """How far apart two points are, in board units."""
    return float(np.linalg.norm(np.array(p, dtype=float)
                                - np.array(q, dtype=float)))


def mid(p, q):
    """The midpoint of two points."""
    return (np.array(p, dtype=float) + np.array(q, dtype=float)) / 2.0


def to_board(points, centre, scale):
    """Map centimetre coordinates onto the board: the figure's bounding box
    centre goes to `centre`, and one centimetre becomes `scale` board units."""
    pts = [np.array(p, dtype=float) for p in points]
    lo = np.min(np.array([p[:2] for p in pts]), axis=0)
    hi = np.max(np.array([p[:2] for p in pts]), axis=0)
    c = (lo + hi) / 2.0
    return [np.array([centre[0] + (p[0] - c[0]) * scale,
                      centre[1] + (p[1] - c[1]) * scale, 0.0]) for p in pts]


def perpendicular_ends(p, direction_deg, length):
    """The two ends of the segment of `length` through `p`, perpendicular to
    `direction_deg` -- the line the other diagonal lies on."""
    return (ray_point(p, direction_deg + 90.0, length),
            ray_point(p, direction_deg - 90.0, length))


# ------------------------------------------------------------- the figures --
def parallelogram_frame(centre=None, scale=PARA_SCALE,
                        be=4.2, el=5.0, angle_t=45.0):
    """Parallelogram B E L T.

    B E = 4.2 cm and E L = 5 cm with the angle at T = 45 degrees.  Because the
    opposite angles of a parallelogram are equal, the angle at E is also 45, so
    triangle B E L is fixed by S.A.S; T is then B + (L - E), which is where the
    two 135 degree rays from B and from L meet."""
    b = np.array([0.0, 0.0, 0.0])
    e = ray_point(b, 0.0, be)
    l = ray_point(e, 180.0 - angle_t, el)          # angle at E = angle at T
    t = b + (l - e)
    B, E, L, T = to_board((b, e, l, t),
                          PARA_CENTRE if centre is None else centre, scale)
    return {
        "quad": (B, E, L, T),
        "model": (b, e, l, t),
        "be_deg": dir_deg(B, E), "el_deg": dir_deg(E, L),
        "eb_deg": dir_deg(E, B), "ebt_deg": dir_deg(B, T),
        "le_deg": dir_deg(L, E), "lt_deg": dir_deg(L, T),
    }


def rhombus_frame(centre=None, scale=RHOMB_SCALE, ac=4.5, bd=6.0):
    """Rhombus A B C D from its two diagonals.

    A C and B D bisect each other at right angles, so with O at their crossing
    A and C are half of A C either side of O, and B and D are half of B D."""
    a = np.array([-ac / 2.0, 0.0, 0.0])
    c = np.array([ac / 2.0, 0.0, 0.0])
    b = np.array([0.0, bd / 2.0, 0.0])
    d = np.array([0.0, -bd / 2.0, 0.0])
    A, B, C, D = to_board((a, b, c, d),
                          RHOMB_CENTRE if centre is None else centre, scale)
    return {
        "quad": (A, B, C, D),
        "model": (a, b, c, d),
        "ac_deg": dir_deg(A, C), "bd_deg": dir_deg(B, D),
        "half_ac": ac / 2.0, "half_bd": bd / 2.0,
        "diag": (ac, bd),
    }


def square_frame(centre=None, scale=SQUARE_SCALE, diag=4.2):
    """Square J U M P from one diagonal.

    In a square the diagonals are equal and bisect each other at right angles,
    so the other diagonal is the same length, and every vertex is half a
    diagonal from the crossing point O."""
    half = diag / 2.0
    j = np.array([-half, 0.0, 0.0])
    u = np.array([half, 0.0, 0.0])
    m = np.array([0.0, half, 0.0])
    p = np.array([0.0, -half, 0.0])
    J, M, U, P = to_board((j, m, u, p),
                          SQUARE_CENTRE if centre is None else centre, scale)
    return {
        "quad": (J, M, U, P),
        "model": (j, m, u, p),
        "ju_deg": dir_deg(J, U), "mp_deg": dir_deg(M, P),
        "half": half, "diag": diag,
    }


def labelled_shapes(centre=None, scale=0.30):
    """Small versions of all three shapes, for the comparison and the recap:
    returns (parallelogram, rhombus, square) point sets, each centred on its
    own centre argument."""
    return (parallelogram_frame(centre, scale)["quad"],
            rhombus_frame(centre, scale)["quad"],
            square_frame(centre, scale)["quad"])


def side_label(p1, p2, centroid, text, color=CHALK_CYAN, size=17,
               offset=0.22):
    """A length label placed clear of its own side, pushed along the true
    outward normal (the earlier version pushed along centroid -> midpoint, which
    is not perpendicular, so a label could sit on its own side)."""
    lab = board_text(text, size, color, "BOLD")
    p1 = np.array(p1, dtype=float)
    p2 = np.array(p2, dtype=float)
    m = (p1 + p2) / 2.0
    d = p2 - p1
    n = np.array([-d[1], d[0], 0.0])
    n = n / (np.linalg.norm(n[:2]) or 1.0)
    if np.dot(n, m - np.array(centroid, dtype=float)) < 0:
        n = -n
    half = (abs(n[0]) * lab.width + abs(n[1]) * lab.height) / 2.0
    return lab.move_to(m + n * (half + offset))


def degree_card(label, color=CHALK_AMBER, size=17) -> VGroup:
    """A card for an angle: LaTeX for the angle symbol, since Segoe Print has
    no glyph for it."""
    tex = MathTex(label, font_size=size, color=color)
    box = RoundedRectangle(corner_radius=0.08, width=tex.width + 0.46,
                           height=tex.height + 0.32, stroke_color=color,
                           stroke_width=1.8, fill_color="#16202B",
                           fill_opacity=0.8)
    tex.move_to(box.get_center())
    grp = VGroup(box, tex)
    grp.tex = tex
    return grp


def value_card(label, color=CHALK_GREEN, size=16) -> VGroup:
    """A card for a derived value, e.g. 180 - 45 = 135."""
    tex = MathTex(label, font_size=size, color=color)
    box = RoundedRectangle(corner_radius=0.08, width=tex.width + 0.44,
                           height=tex.height + 0.28, stroke_color=color,
                           stroke_width=1.8, fill_color="#16202B",
                           fill_opacity=0.8)
    tex.move_to(box.get_center())
    grp = VGroup(box, tex)
    grp.tex = tex
    return grp


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "Three special quadrilaterals, and three surprisingly short lists of "
        "measurements.<bookmark mark='b0'/> Each of them carries a property "
        "that supplies whatever is missing.<bookmark mark='b1'/>"
    ),
    "scene1": (
        "Look at what each shape is given.<bookmark mark='b0'/> A "
        "parallelogram: two sides and one angle. Only three "
        "measurements.<bookmark mark='b0b'/> A rhombus: two diagonals. Only "
        "two.<bookmark mark='b1'/> A square: a single diagonal. Can that "
        "really be enough?<bookmark mark='b2'/> It can, because the name of "
        "the shape is information too: its properties give us the measurements "
        "that were never listed.<bookmark mark='b3'/>"
    ),
    "scene2": (
        "Start with the parallelogram B E L T.<bookmark mark='b0'/> We are "
        "given B E, four point two centimetres, E L, five centimetres, and the "
        "angle at T, forty five degrees.<bookmark mark='b1'/> In a "
        "parallelogram opposite angles are equal, so the angle at E is also "
        "forty five degrees.<bookmark mark='b2'/> And consecutive angles are "
        "supplementary: one hundred and eighty minus forty five is one hundred "
        "and thirty five.<bookmark mark='b3'/> So the angle at L is one "
        "hundred and thirty five degrees, and so is the angle at "
        "B.<bookmark mark='b4'/> Four angles, from one given "
        "angle.<bookmark mark='b5'/>"
    ),
    "scene3": (
        "Now the construction is straightforward.<bookmark mark='b0'/> Draw B "
        "E, four point two centimetres.<bookmark mark='b1'/> At E set out "
        "forty five degrees and mark E L, five centimetres: that is triangle B "
        "E L by side, angle, side.<bookmark mark='b2'/> At B, set out one "
        "hundred and thirty five degrees and draw the ray.<bookmark "
        "mark='b3'/> At L, set out one hundred and thirty five degrees as "
        "well, and draw the second ray.<bookmark mark='b4'/> The two rays meet "
        "at T, and the parallelogram is complete.<bookmark mark='b5'/>"
    ),
    "scene4": (
        "Now the rhombus.<bookmark mark='b0'/> A rhombus is given by its two "
        "diagonals: A C is four point five centimetres and B D is six. Only two "
        "measurements, but a rhombus has two properties we can use.<bookmark "
        "mark='b1'/> Its diagonals are perpendicular: they cross at right "
        "angles, at O.<bookmark mark='b2'/> And they bisect each other, so O "
        "is the midpoint of both.<bookmark mark='b3'/> Which means O B and O D "
        "are each half of six: three centimetres.<bookmark mark='b4'/>"
    ),
    "scene5": (
        "So this is how we construct it.<bookmark mark='b0'/> Draw A C, four "
        "point five centimetres, and mark its midpoint O.<bookmark "
        "mark='b1'/> Through O draw the perpendicular to A C: that is the line "
        "the other diagonal lies on.<bookmark mark='b2'/> Set the compasses to "
        "three centimetres, put the needle at O, and mark the perpendicular on "
        "both sides.<bookmark mark='b3'/> Those marks are B and D, because each "
        "is three centimetres from O, exactly half of B D.<bookmark "
        "mark='b4'/> Join A to B, B to C, C to D and D to A: the rhombus is "
        "complete, and we never needed its side lengths.<bookmark mark='b5'/>"
    ),
    "scene6": (
        "Here is a question worth asking: what if the two diagonals of the "
        "rhombus were equal?<bookmark mark='b0'/> Watch the shorter diagonal "
        "grow until both are the same length.<bookmark mark='b1'/> The rhombus "
        "becomes a square, because equal diagonals that bisect each other at "
        "right angles always give a square.<bookmark mark='b2'/> So we can "
        "construct square J U M P with diagonal four point two centimetres the "
        "same way: draw J U, find its midpoint, and draw the perpendicular "
        "through it.<bookmark mark='b3'/> The other diagonal is equal, so it is "
        "also four point two centimetres, and O M and O P are two point one "
        "centimetres each.<bookmark mark='b4'/> Mark M and P, join the four "
        "vertices, and the square is complete.<bookmark mark='b5'/>"
    ),
    "scene7": (
        "Three shapes, three strategies.<bookmark mark='b0'/> For the "
        "parallelogram, opposite angles are equal and consecutive angles add to "
        "one hundred and eighty degrees: that gives the missing "
        "angles.<bookmark mark='b1'/> For the rhombus, the diagonals bisect "
        "each other at right angles: that gives every vertex from the "
        "diagonals.<bookmark mark='b2'/> For the square the diagonals are equal "
        "as well: the same construction, with one extra condition.<bookmark "
        "mark='b3'/> So which property gives the missing information?<bookmark "
        "mark='b4'/>"
    ),
    "scene8": (
        "That is the method for every special quadrilateral.<bookmark "
        "mark='b0'/> Identify the shape. Recall its properties. Derive the "
        "measurements that are missing. Then construct.<bookmark mark='b1'/> "
        "Analyse before you draw: the property tells you what to do with the "
        "ruler, the compasses and the protractor.<bookmark mark='b2'/>"
    ),
    "scene9_setup": (
        "Your turn, two quick ones.<bookmark mark='b0'/> A parallelogram has "
        "angle A equal to sixty five degrees. What are the other three "
        "angles?<bookmark mark='b1'/> And a rhombus has diagonals A C of eight "
        "centimetres and B D of six. How far is each vertex from the point "
        "where the diagonals cross?<bookmark mark='b2'/> Pause the video and "
        "work them out.<bookmark mark='b3'/>"
    ),
    "scene9_reveal": (
        "Let us check.<bookmark mark='b0'/> In the parallelogram the angle "
        "opposite A is C, so C is sixty five degrees; and the angles next to A "
        "are supplementary, so B and D are one hundred and eighty minus sixty "
        "five: one hundred and fifteen degrees each.<bookmark mark='b1'/> In "
        "the rhombus, O is the midpoint of both diagonals, so O A and O C are "
        "four centimetres, and O B and O D are three.<bookmark mark='b2'/> Draw "
        "the perpendicular diagonals, mark those distances, and join the ends: "
        "that is the rhombus.<bookmark mark='b3'/>"
    ),
    "scene10": (
        "One idea holds all three together.<bookmark mark='b0'/> A special "
        "shape comes with extra information: use its properties to find the "
        "missing measurements, and then construct.<bookmark mark='b1'/> Know "
        "the shape. Use its properties. Construct it.<bookmark mark='b2'/> "
        "Thank you for watching!<bookmark mark='b3'/> See you in the next "
        "lesson!<bookmark mark='b4'/>"
    ),
}

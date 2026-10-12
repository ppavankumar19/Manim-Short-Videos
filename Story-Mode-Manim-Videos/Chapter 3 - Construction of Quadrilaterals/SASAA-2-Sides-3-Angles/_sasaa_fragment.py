"""Geometry frames and narration for Storyboard 05 (S.A.S.A.A).

The two figures are built the way the construction builds them: first the
S.A.S triangle from the two adjacent sides and the angle between them, then the
fourth vertex as the crossing of the two rays set out by the remaining angles.
"""


# ------------------------------------------------- construction furniture ----
SCALE = 0.55            # board units per centimetre of the textbook drawing
PRACTICE_SCALE = 0.46
# The figure is long and narrow (S P = 7.4 cm against P Q = 4 cm), so it is
# placed a little left of centre on the board with the step column on the right.
EXAMPLE_CENTRE = np.array([BOARD_CX - 1.8, 0.05, 0.0])
PRACTICE_CENTRE = np.array([BOARD_CX - 1.9, -0.15, 0.0])


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


def ray_intersection(p1, d1, p2, d2):
    """Where the ray from `p1` at `d1` degrees meets the ray from `p2` at `d2`.

    Returns (point, t, s) with `t` and `s` the distances along each ray, so the
    caller can insist that the crossing lies *in front of* both rays -- the
    construction has no meaning otherwise."""
    p1 = np.array(p1, dtype=float)
    p2 = np.array(p2, dtype=float)
    u, v = unit(d1)[:2], unit(d2)[:2]
    a = np.array([[u[0], -v[0]], [u[1], -v[1]]])
    t, s = np.linalg.solve(a, (p2 - p1)[:2])
    return p1 + t * unit(d1), float(t), float(s)


def crossing(p1, arm1, angle1, p2, arm2, angle2):
    """`p1` and `p2` are joined by a known arm; the two remaining angles are
    set out from those arms.  The fourth vertex is the crossing that lies in
    front of both rays (the other three sign combinations point away)."""
    for s1 in (-1.0, 1.0):
        for s2 in (-1.0, 1.0):
            point, t, s = ray_intersection(p1, arm1 + s1 * angle1,
                                           p2, arm2 + s2 * angle2)
            if t > 1e-6 and s > 1e-6:
                return point, arm1 + s1 * angle1, arm2 + s2 * angle2
    raise ValueError("the two rays do not meet in front of both vertices")


def to_board(points, centre, scale):
    """Map centimetre coordinates onto the board: the figure's bounding box
    centre goes to `centre`, and one centimetre becomes `scale` board units."""
    pts = [np.array(p, dtype=float) for p in points]
    lo = np.min(np.array([p[:2] for p in pts]), axis=0)
    hi = np.max(np.array([p[:2] for p in pts]), axis=0)
    mid = (lo + hi) / 2.0
    return [np.array([centre[0] + (p[0] - mid[0]) * scale,
                      centre[1] + (p[1] - mid[1]) * scale, 0.0]) for p in pts]


def _build(p, q, side_qr, angle_q, angle_p, angle_r, centre, scale):
    """Shared construction: the S.A.S triangle first, then the crossing.

    Returns the four board points as `quad` (first, second, third = the S.A.S
    triangle, fourth = the crossing), the model-centimetre points, and every
    direction the animation needs."""
    r = ray_point(q, dir_deg(q, p) - angle_q, side_qr)
    s, ps_deg, rs_deg = crossing(p, dir_deg(p, q), angle_p,
                                 r, dir_deg(r, q), angle_r)
    a, b, c, d = to_board((p, q, r, s), centre, scale)
    return {
        "quad": (a, b, c, d),
        "model": (p, q, r, s),
        "pq_deg": dir_deg(a, b), "qr_deg": dir_deg(b, c),
        "qp_deg": dir_deg(b, a), "rq_deg": dir_deg(c, b),
        "ps_deg": dir_deg(a, d), "rs_deg": dir_deg(c, d),
        "sp_deg": dir_deg(d, a), "sr_deg": dir_deg(d, c),
        "pr_deg": dir_deg(a, c),
    }


def example_construction(centre=None, scale=SCALE):
    """Textbook Example 6, built the way the construction builds it.

    P Q = 4 cm and Q R = 4.8 cm with the angle at Q = 100 degrees fix triangle
    P Q R by S.A.S; the angles at P (75 degrees from P Q) and at R (120 degrees
    from R Q) then give two rays that cross at S.  P S and R S are not given --
    they are what the construction produces."""
    c = EXAMPLE_CENTRE if centre is None else centre
    return _build(np.array([0.0, 0.0, 0.0]), np.array([4.0, 0.0, 0.0]),
                  4.8, 100.0, 75.0, 120.0, c, scale)


def example_frame(centre=None, scale=SCALE):
    """The four vertices of Example 6 as (P, Q, R, S)."""
    return example_construction(centre, scale)["quad"]


def practice_construction(centre=None, scale=PRACTICE_SCALE):
    """Exercise data for the student challenge: A B = 5 cm, B C = 4 cm, the
    angle at B = 110 degrees, and the angles at A = 70 and at C = 120."""
    c = PRACTICE_CENTRE if centre is None else centre
    return _build(np.array([0.0, 0.0, 0.0]), np.array([5.0, 0.0, 0.0]),
                  4.0, 110.0, 70.0, 120.0, c, scale)


def practice_frame(centre=None, scale=PRACTICE_SCALE):
    """The four vertices of the practice quadrilateral as (A, B, C, D)."""
    return practice_construction(centre, scale)["quad"]


def side_label(p1, p2, centroid, text, color=CHALK_CYAN, size=17,
               offset=0.22):
    """A length label placed clear of its own side.

    Overrides the version earlier in this file, which pushed the label along
    the centroid -> midpoint direction: that direction is not perpendicular to
    the side, so the label was moved by less than the half-extent it actually
    needs and a steep side ran straight through its own label.  Here the push
    is along the true outward normal."""
    lab = board_text(text, size, color, "BOLD")
    p1 = np.array(p1, dtype=float)
    p2 = np.array(p2, dtype=float)
    mid = (p1 + p2) / 2.0
    d = p2 - p1
    n = np.array([-d[1], d[0], 0.0])
    n = n / (np.linalg.norm(n[:2]) or 1.0)
    if np.dot(n, mid - np.array(centroid, dtype=float)) < 0:
        n = -n
    half = (abs(n[0]) * lab.width + abs(n[1]) * lab.height) / 2.0
    return lab.move_to(mid + n * (half + offset))


def degree_card(label, color=CHALK_AMBER, size=17) -> VGroup:
    """A measurement card for an angle: the same look as `measure_card`, and
    LaTeX for the angle symbol -- Segoe Print has no glyph for the angle sign,
    so the card's content is typeset rather than chalk-written."""
    tex = MathTex(label, font_size=size, color=color)
    box = RoundedRectangle(corner_radius=0.08, width=tex.width + 0.46,
                           height=tex.height + 0.32, stroke_color=color,
                           stroke_width=1.8, fill_color="#16202B",
                           fill_opacity=0.8)
    tex.move_to(box.get_center())
    grp = VGroup(box, tex)
    grp.tex = tex
    return grp


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "How do we construct a quadrilateral from two adjacent sides and three "
        "angles?<bookmark mark='b0'/> Two lengths and three angles: the plan "
        "has to sort them before anything is drawn.<bookmark mark='b1'/>"
    ),
    "scene1": (
        "Here is our problem.<bookmark mark='b0'/> Two adjacent sides: P Q is "
        "four centimetres, and Q R is four point eight.<bookmark mark='b0b'/> "
        "Three angles: angle P is seventy five degrees, angle Q is one "
        "hundred, and angle R is one hundred and twenty.<bookmark mark='b1'/> "
        "Two sides and three angles.<bookmark mark='b2'/> So where do we "
        "begin?<bookmark mark='b3'/>"
    ),
    "scene2": (
        "A diagonal was not given this time.<bookmark mark='b0'/> So look for "
        "the triangle we can already build: P Q is four, Q R is four point "
        "eight, and they meet at Q.<bookmark mark='b1'/> The angle between "
        "them, angle Q, is one hundred degrees.<bookmark mark='b2'/> Side, "
        "angle, side: triangle P Q R is fixed.<bookmark mark='b3'/> The other "
        "two angles come later.<bookmark mark='b4'/>"
    ),
    "scene3": (
        "Here is the whole plan.<bookmark mark='b0'/> Three measurements build "
        "the first triangle: the side P Q, the angle Q, and the side Q "
        "R.<bookmark mark='b1'/> The other two, the angle at P and the angle "
        "at R, locate the fourth vertex.<bookmark mark='b2'/> Three build, and "
        "two locate.<bookmark mark='b3'/>"
    ),
    "scene4": (
        "Now we construct it accurately.<bookmark mark='b0'/> Draw the side P "
        "Q, four centimetres long, and label the ends P and Q.<bookmark "
        "mark='b1'/> At Q, set out an angle of one hundred degrees from Q "
        "P.<bookmark mark='b2'/> The new ray is the direction of Q R, so R "
        "must lie somewhere on it.<bookmark mark='b3'/>"
    ),
    "scene5": (
        "Set the compasses to four point eight centimetres, the length of Q "
        "R.<bookmark mark='b0'/> With the needle at Q, mark that distance "
        "along the ray.<bookmark mark='b1'/> That point is R.<bookmark "
        "mark='b2'/> Join P to R, and triangle P Q R is fixed by side, angle, "
        "side.<bookmark mark='b3'/>"
    ),
    "scene6": (
        "Only the fourth vertex is left.<bookmark mark='b0'/> At P, set out an "
        "angle of seventy five degrees from P Q, on the inside of the "
        "figure.<bookmark mark='b1'/> Every point on this ray makes seventy "
        "five degrees with P Q, so S lies somewhere on it.<bookmark "
        "mark='b2'/> An angle gives a direction, not a distance.<bookmark "
        "mark='b3'/> Seventy five degrees is half way between sixty and "
        "ninety.<bookmark mark='b4'/>"
    ),
    "scene7": (
        "Now the angle at R.<bookmark mark='b0'/> With the compasses, mark one "
        "hundred and twenty degrees from R Q<bookmark mark='b1'/> and draw the "
        "second ray.<bookmark mark='b2'/> This ray is another set of possible "
        "places for S, and the two rays cross at exactly one "
        "point.<bookmark mark='b3'/> That point is S: two directions agree "
        "there.<bookmark mark='b4'/>"
    ),
    "scene8": (
        "We finish the figure: join P to S and R to S.<bookmark mark='b0'/> "
        "Let us check every measurement: P Q is four, Q R is four point eight, "
        "angle P is seventy five degrees, angle Q is one hundred, and angle R "
        "is one hundred and twenty.<bookmark mark='b1'/> Here is the method: "
        "sketch the figure, build the side angle side triangle, draw the two "
        "remaining angle rays, and their crossing gives the last "
        "vertex.<bookmark mark='b2'/>"
    ),
    "scene9_setup": (
        "Your turn.<bookmark mark='b0'/> Construct quadrilateral A B C D: A B "
        "is five centimetres, B C is four centimetres, angle A is seventy "
        "degrees, angle B is one hundred and ten degrees, and angle C is one "
        "hundred and twenty degrees.<bookmark mark='b1'/> Which three "
        "measurements should you use first?<bookmark mark='b2'/> Pause the "
        "video and decide.<bookmark mark='b3'/>"
    ),
    "scene9_reveal": (
        "Let us check.<bookmark mark='b0'/> A B and B C are the two adjacent "
        "sides, and they meet at B.<bookmark mark='b1'/> So the triangle is A "
        "B C, built by side, angle, side.<bookmark mark='b2'/> Then the angles "
        "at A and C give two rays, and where they cross is D.<bookmark "
        "mark='b3'/>"
    ),
    "scene10": (
        "Let us put it together.<bookmark mark='b0'/> Two adjacent sides and "
        "the angle between them build the first triangle.<bookmark mark='b1'/> "
        "The other two angles give two rays, and their crossing is the fourth "
        "vertex.<bookmark mark='b2'/> Side angle side builds; angle angle "
        "locates.<bookmark mark='b3'/> Thank you for watching!<bookmark "
        "mark='b4'/> See you in the next lesson!<bookmark mark='b5'/>"
    ),
}

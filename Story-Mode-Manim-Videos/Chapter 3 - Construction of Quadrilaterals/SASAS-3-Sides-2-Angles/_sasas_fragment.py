"""Geometry frames and narration for Storyboard 06 (S.A.S.A.S).

The chain S-A-S-A-S is built in order: the first three measurements give
triangle A B C by S.A.S (the angle at B turns the side A B into the direction of
B C), the second angle turns C B into the direction of C D, and the last side
marks D at that distance along the ray.
"""


# ------------------------------------------------- construction furniture ----
SCALE = 0.82            # board units per centimetre of the textbook drawing
PRACTICE_SCALE = 0.70
# Both figures are wider than they are tall, so they sit a little left of centre
# with the measurement/step column on the right.
EXAMPLE_CENTRE = np.array([BOARD_CX - 1.3, 0.0, 0.0])
PRACTICE_CENTRE = np.array([BOARD_CX - 1.4, -0.1, 0.0])


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


def _convex(a, b, c, d) -> bool:
    """True when the four points, in that order, form a convex quadrilateral:
    every turn round the boundary goes the same way."""
    pts = [np.array(p, dtype=float) for p in (a, b, c, d)]
    signs = []
    for i in range(4):
        u = pts[(i + 1) % 4] - pts[i]
        v = pts[(i + 2) % 4] - pts[(i + 1) % 4]
        signs.append(float(np.sign(u[0] * v[1] - u[1] * v[0])))
    return all(s > 0 for s in signs) or all(s < 0 for s in signs)


def to_board(points, centre, scale):
    """Map centimetre coordinates onto the board: the figure's bounding box
    centre goes to `centre`, and one centimetre becomes `scale` board units."""
    pts = [np.array(p, dtype=float) for p in points]
    lo = np.min(np.array([p[:2] for p in pts]), axis=0)
    hi = np.max(np.array([p[:2] for p in pts]), axis=0)
    mid = (lo + hi) / 2.0
    return [np.array([centre[0] + (p[0] - mid[0]) * scale,
                      centre[1] + (p[1] - mid[1]) * scale, 0.0]) for p in pts]


def quadrilateral_from_chain(a, b, side_ab, angle_b, side_bc, angle_c, side_cd,
                             centre, scale):
    """Build the quadrilateral from the five measurements in chain order.

    `a` and `b` are the two ends of the side drawn first.  The angle at `b`
    turns the direction b -> a into the direction b -> c, and `c` sits one side
    length along it, so the first three measurements build triangle a b c by
    S.A.S.  The angle at `c` then turns c -> b into the direction of c -> d (the
    turn is taken on the side that keeps the quadrilateral convex), and the last
    side length marks `d` at that distance along the ray -- a direction and a
    distance, which is exactly how the textbook locates the fourth vertex."""
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    c = ray_point(b, dir_deg(b, a) - angle_b, side_bc)
    d = None
    for sign in (-1.0, 1.0):
        trial = ray_point(c, dir_deg(c, b) + sign * angle_c, side_cd)
        if _convex(a, b, c, trial):
            d = trial
            break
    if d is None:                       # pragma: no cover - data dependant
        raise ValueError("no convex quadrilateral for these measurements")
    A, B, C, D = to_board((a, b, c, d), centre, scale)
    return {
        "quad": (A, B, C, D),
        "model": (a, b, c, d),
        "ab_deg": dir_deg(A, B), "bc_deg": dir_deg(B, C),
        "ba_deg": dir_deg(B, A), "cb_deg": dir_deg(C, B),
        "cd_deg": dir_deg(C, D), "dc_deg": dir_deg(D, C),
        "ac_deg": dir_deg(A, C), "ad_deg": dir_deg(A, D),
        "da_deg": dir_deg(D, A),
    }


def example_construction(centre=None, scale=SCALE):
    """Textbook Example 8, in chain order: A B = 5 cm, angle B = 100 degrees,
    B C = 4.5 cm, angle C = 75 degrees, C D = 6 cm."""
    c = EXAMPLE_CENTRE if centre is None else centre
    return quadrilateral_from_chain(np.array([-5.0, 0.0, 0.0]),
                                    np.array([0.0, 0.0, 0.0]),
                                    5.0, 100.0, 4.5, 75.0, 6.0, c, scale)


def example_frame(centre=None, scale=SCALE):
    """The four vertices of Example 8 as (A, B, C, D)."""
    return example_construction(centre, scale)["quad"]


def practice_construction(centre=None, scale=PRACTICE_SCALE):
    """Exercise 3.5(a), in chain order: P Q = 3.6 cm, angle Q = 135 degrees,
    Q R = 4.5 cm, angle R = 60 degrees, R S = 5.6 cm."""
    c = PRACTICE_CENTRE if centre is None else centre
    return quadrilateral_from_chain(np.array([-3.6, 0.0, 0.0]),
                                    np.array([0.0, 0.0, 0.0]),
                                    3.6, 135.0, 4.5, 60.0, 5.6, c, scale)


def practice_frame(centre=None, scale=PRACTICE_SCALE):
    """The four vertices of the practice quadrilateral as (P, Q, R, S)."""
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
        "How do we construct a quadrilateral from three sides and two included "
        "angles?<bookmark mark='b0'/> Read the five measurements as a chain: "
        "side, angle, side, angle, side.<bookmark mark='b1'/>"
    ),
    "scene1": (
        "Here is our problem: five measurements, in the order they "
        "connect.<bookmark mark='b0'/> A B is five centimetres, a "
        "side.<bookmark mark='b1'/> Angle B is one hundred degrees: an angle "
        "between two sides.<bookmark mark='b2'/> B C is four point five "
        "centimetres.<bookmark mark='b3'/> Angle C is seventy five "
        "degrees.<bookmark mark='b4'/> And C D is six centimetres.<bookmark "
        "mark='b5'/> Side, angle, side, angle, side.<bookmark mark='b6'/>"
    ),
    "scene2": (
        "Now, what does included mean?<bookmark mark='b0'/> Angle B is the "
        "angle between the two sides that meet at B: A B and B C.<bookmark "
        "mark='b1'/> Angle C is the angle between B C and C D.<bookmark "
        "mark='b2'/> Each angle sits between the sides next to it.<bookmark "
        "mark='b3'/> That is the chain: side, angle, side, angle, "
        "side.<bookmark mark='b4'/>"
    ),
    "scene3": (
        "Here is the whole plan.<bookmark mark='b0'/> The first three "
        "measurements build the triangle: the side A B, the angle B, and the "
        "side B C.<bookmark mark='b1'/> The last two finish the figure: the "
        "angle at C gives a direction, and the side C D gives the "
        "distance.<bookmark mark='b2'/> Three build, and two finish.<bookmark "
        "mark='b3'/>"
    ),
    "scene4": (
        "Now we construct it accurately.<bookmark mark='b0'/> Draw A B, five "
        "centimetres long, and label the ends A and B.<bookmark mark='b1'/> At "
        "B, set out an angle of one hundred degrees from B A.<bookmark "
        "mark='b2'/> The new ray is the direction of B C, so C must lie "
        "somewhere on it.<bookmark mark='b3'/>"
    ),
    "scene5": (
        "Set the compasses to four point five centimetres, the length of B "
        "C.<bookmark mark='b0'/> With the needle at B, mark that distance "
        "along the ray: that point is C.<bookmark mark='b1'/> Join B to C, and "
        "join C to A to close the triangle.<bookmark mark='b2'/> Triangle A B "
        "C is fixed by side, angle, side; the side A C was not given, so the "
        "construction made it.<bookmark mark='b3'/>"
    ),
    "scene6": (
        "The first three measurements are used.<bookmark mark='b0'/> At C, the "
        "angle between C B and C D is seventy five degrees.<bookmark "
        "mark='b1'/> Set that angle out from C B and draw the ray: every point "
        "on it is in the right direction from C.<bookmark mark='b2'/> But the "
        "angle alone does not say how far, so D could be anywhere along this "
        "ray.<bookmark mark='b3'/>"
    ),
    "scene7": (
        "The last measurement is the side C D, six centimetres.<bookmark "
        "mark='b0'/> Set the compasses to six centimetres and put the needle "
        "at C.<bookmark mark='b1'/> Every point on this arc is six centimetres "
        "from C, so where it cuts the ray is D.<bookmark mark='b2'/> Join A to "
        "D, and the quadrilateral A B C D is complete: one direction, and one "
        "distance.<bookmark mark='b3'/>"
    ),
    "scene8": (
        "Let us check every measurement: A B is five, angle B is one hundred "
        "degrees, B C is four point five, angle C is seventy five degrees, and "
        "C D is six.<bookmark mark='b0'/> All five are used, and A D was never "
        "given.<bookmark mark='b1'/> Here is the method: sketch the figure, "
        "build the side angle side triangle, draw the ray from the next angle, "
        "mark the last side on that ray, and join the last side.<bookmark "
        "mark='b2'/>"
    ),
    "scene9_setup": (
        "Your turn.<bookmark mark='b0'/> Construct P Q R S with P Q three "
        "point six centimetres, Q R four point five centimetres, R S five "
        "point six centimetres, angle Q one hundred and thirty five degrees, "
        "and angle R sixty degrees.<bookmark mark='b1'/> Which three "
        "measurements construct the first triangle?<bookmark mark='b2'/> Pause "
        "the video and decide.<bookmark mark='b3'/>"
    ),
    "scene9_reveal": (
        "Let us check.<bookmark mark='b0'/> P Q, angle Q and Q R are the side, "
        "angle, side group, so the first triangle is P Q R.<bookmark "
        "mark='b1'/> Then the sixty degrees at R gives the direction, and R S "
        "gives the distance along it.<bookmark mark='b2'/> That point is S; "
        "join P to S and the quadrilateral is complete.<bookmark mark='b3'/>"
    ),
    "scene10": (
        "The chain is the whole method.<bookmark mark='b0'/> The first three "
        "measurements build the first triangle.<bookmark mark='b1'/> The next "
        "angle gives a direction.<bookmark mark='b2'/> The last side gives the "
        "distance, and direction and distance together locate the fourth "
        "vertex.<bookmark mark='b3'/> Thank you for watching!<bookmark "
        "mark='b4'/> See you in the next lesson!<bookmark mark='b5'/>"
    ),
}

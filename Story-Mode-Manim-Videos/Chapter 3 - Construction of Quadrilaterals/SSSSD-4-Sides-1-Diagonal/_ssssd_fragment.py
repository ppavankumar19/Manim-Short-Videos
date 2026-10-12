"""Geometry frames and narration for Storyboard 03 (S.S.S.S.D)."""


# ------------------------------------------------- construction furniture ----
SCALE = 0.56            # board units per centimetre of the textbook drawing
AC_Y = 0.30             # the diagonal AC is drawn level, at this height


def triangle_apex(A, C, rA, rC, up=True):
    """The third vertex of a triangle whose other two vertices are A and C:
    the point at distance `rA` from A and `rC` from C, on the chosen side of
    the line A -> C.  This is exactly "intersect the two arcs"."""
    return circle_intersection(A, rA, C, rC, upper=up)


def example_frame(origin=None, scale=SCALE, base_y=None):
    """Textbook Example 3, built the way the construction builds it.

    A C = 5 cm is the diagonal, and it is the shared side of the two triangles:
    B is the point with A B = 4 cm and B C = 3.6 cm above the diagonal, and D
    is the point with A D = 4.8 cm and C D = 4.2 cm below it -- the textbook
    places the fourth vertex on the other side of the diagonal."""
    if origin is None:
        y = AC_Y if base_y is None else base_y
        origin = np.array([BOARD_CX - 1.4, y, 0.0])
    A = np.array(origin, dtype=float)
    C = A + np.array([5.0 * scale, 0.0, 0.0])
    B = triangle_apex(A, C, 4.0 * scale, 3.6 * scale, up=True)
    D = triangle_apex(A, C, 4.8 * scale, 4.2 * scale, up=False)
    return A, B, C, D


def practice_frame(origin=None, scale=0.40, base_y=None):
    """The practice set used for the challenge: P R = 5.5 is the diagonal,
    P Q = 4 and Q R = 3 above it, P S = 4.5 and R S = 5 below it."""
    if origin is None:
        y = AC_Y if base_y is None else base_y
        origin = np.array([BOARD_CX - 3.0, y, 0.0])
    P = np.array(origin, dtype=float)
    R = P + np.array([5.5 * scale, 0.0, 0.0])
    Q = triangle_apex(P, R, 4.0 * scale, 3.0 * scale, up=True)
    S = triangle_apex(P, R, 4.5 * scale, 5.0 * scale, up=False)
    return P, Q, R, S


def diamond_names(left, top, right, bottom, letters="ABCD", size=17,
                  color=CHALK_WHITE, pull=0.0) -> VGroup:
    """Vertex letters for this video's quadrilateral.

    The diagonal is drawn level, so the figure has one vertex on the left, one
    at the top, one on the right and one at the bottom, and each letter goes to
    the corner that is actually free.  The series' default quad-sides put the
    top vertex's letter down-right and the bottom vertex's letter up-left, which
    here would land them on the figure's own sides; and the bottom vertex is
    where the two locating arcs cross, so its letter is pushed out to the
    down-right, clear of both arcs (measured clearance 0.10-0.38)."""
    def place(letter, point, side, extra=None):
        lab = vertex_label(letter, point, side, color, size)
        if extra is not None:
            lab.shift(extra)
        if pull:
            # the small recap figures need the letter nearer its corner: the
            # fixed 0.10 offset is a large fraction of a 2-unit figure
            d = np.array(point, dtype=float) - lab.get_center()
            n = float(np.linalg.norm(d[:2]))
            if n > 1e-6:
                lab.shift(d / n * min(pull, max(n - 0.02, 0.0)))
        return lab

    return VGroup(place(letters[0], left, "UL"),
                  place(letters[1], top, "UR"),
                  place(letters[2], right, "UR"),
                  place(letters[3], bottom, "DR",
                        np.array([0.14, -0.20, 0.0])))


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "How do we construct a quadrilateral when we are given four sides and "
        "one diagonal?<bookmark mark='b0'/> The diagonal is the key: it joins "
        "two opposite corners, and it turns one quadrilateral into two "
        "triangles.<bookmark mark='b1'/>"
    ),
    "scene1": (
        "Here is our problem.<bookmark mark='b0'/> Four sides and one diagonal. "
        "A B is four centimetres. B C is three point six centimetres. C D is "
        "four point two centimetres. A D is four point eight centimetres."
        "<bookmark mark='b0b'/> And the diagonal A C is five centimetres."
        "<bookmark mark='b1'/> Four sides and one diagonal: that is the "
        "measurement set.<bookmark mark='b2'/> So where should we start?"
        "<bookmark mark='b3'/>"
    ),
    "scene2": (
        "Look at what the diagonal does.<bookmark mark='b0'/> It joins two "
        "opposite corners, A and C, and it divides the quadrilateral into two "
        "triangles:<bookmark mark='b1'/> triangle A B C on one side,"
        "<bookmark mark='b2'/> and triangle A C D on the other."
        "<bookmark mark='b3'/> One quadrilateral, two triangles."
        "<bookmark mark='b4'/> Which triangle can we build first?"
        "<bookmark mark='b5'/>"
    ),
    "scene3": (
        "So we look for a triangle whose three sides are all known."
        "<bookmark mark='b0'/> In triangle A B C we know A B is four, and B C "
        "is three point six.<bookmark mark='b1'/> We also know the diagonal A C "
        "is five. Three sides and no angle:<bookmark mark='b2'/> that is all we "
        "need. Triangle A B C is the one to construct first.<bookmark "
        "mark='b3'/>"
    ),
    "scene4": (
        "Let us construct it accurately.<bookmark mark='b0'/> Draw the diagonal "
        "A C, five centimetres long, and label the ends A and C.<bookmark "
        "mark='b1'/> This diagonal belongs to both triangles, so it stays on the "
        "board.<bookmark mark='b2'/> Set the compasses to four centimetres and "
        "put the needle at A.<bookmark mark='b3'/> Draw an arc above the "
        "diagonal: every point on it is four centimetres from A, so B lies "
        "somewhere on it.<bookmark mark='b4'/>"
    ),
    "scene5": (
        "Now set the compasses to three point six centimetres and put the "
        "needle at C.<bookmark mark='b0'/> Draw the second arc, above the "
        "diagonal as well.<bookmark mark='b1'/> Where the two arcs cross, that "
        "point is B, because it is four centimetres from A and three point six "
        "centimetres from C.<bookmark mark='b2'/> Join A to B and B to C: "
        "triangle A B C is now fixed by its three sides.<bookmark mark='b3'/>"
    ),
    "scene6": (
        "Only the fourth vertex is left.<bookmark mark='b0'/> D is four point "
        "eight centimetres from A, four point two centimetres from C, and it "
        "lies on the other side of the diagonal.<bookmark mark='b1'/> Set the "
        "compasses to four point eight and draw an arc about A, below the "
        "diagonal.<bookmark mark='b2'/> Then set them to four point two and "
        "draw an arc about C.<bookmark mark='b3'/> Where those two arcs cross "
        "is D, because it satisfies both distances.<bookmark mark='b4'/>"
    ),
    "scene7": (
        "Now we finish the figure.<bookmark mark='b0'/> Join A to D, and join D "
        "to C.<bookmark mark='b1'/> The quadrilateral A B C D is complete. Let "
        "us check every measurement:<bookmark mark='b2'/> A B is four, B C is "
        "three point six, C D is four point two, A D is four point eight, and "
        "the diagonal A C is five. All five are used.<bookmark mark='b3'/>"
    ),
    "scene8": (
        "This is the method, and it works for every problem of this kind."
        "<bookmark mark='b0'/> First sketch the figure and mark what is given. "
        "Then build the first triangle from the diagonal and the two sides that "
        "meet it. Then use the two remaining sides as radii, and intersect "
        "those arcs. Finally join the last sides, and verify.<bookmark "
        "mark='b1'/> Diagonal, triangle, arcs, join.<bookmark mark='b2'/>"
    ),
    "scene9_setup": (
        "Your turn.<bookmark mark='b0'/> In quadrilateral P Q R S, P Q is four "
        "centimetres, Q R is three centimetres, R S is five centimetres, P S is "
        "four point five centimetres, and the diagonal P R is five point five "
        "centimetres.<bookmark mark='b1'/> Which triangle should you construct "
        "first?<bookmark mark='b2'/> Pause the video and decide.<bookmark "
        "mark='b3'/>"
    ),
    "scene9_reveal": (
        "Let us check.<bookmark mark='b0'/> The diagonal is P R, so the two "
        "triangles are P Q R and P R S.<bookmark mark='b1'/> In triangle P Q R "
        "we know P Q is four, Q R is three, and P R is five point five: three "
        "sides, so triangle P Q R comes first.<bookmark mark='b2'/> Then S is "
        "found by two arcs: radius four point five about P, and radius five "
        "about R. Where they cross is S, and the quadrilateral P Q R S is "
        "complete.<bookmark mark='b3'/>"
    ),
    "scene10": (
        "Let us put the method together.<bookmark mark='b0'/> Three "
        "measurements build the first triangle: the diagonal and the two sides "
        "that meet it.<bookmark mark='b1'/> The other two sides locate the "
        "fourth vertex, as the intersection of two arcs.<bookmark mark='b2'/> "
        "Diagonal, triangle, arcs, join, verify.<bookmark mark='b3'/> Thank you "
        "for watching!<bookmark mark='b4'/> See you in the next "
        "lesson!<bookmark mark='b5'/>"
    ),
}

"""Geometry frames and narration for Storyboard 04 (S.S.S.D.D)."""


# ------------------------------------------------- construction furniture ----
SCALE = 0.56            # board units per centimetre of the textbook drawing
AC_Y = -0.40            # the diagonal AC is drawn level, at this height
                        # (this quadrilateral is tall: the apex B reaches 4.5 cm
                        # above AC, so the base sits lower than in storyboard 03)


def example_frame(origin=None, scale=SCALE, base_y=None):
    """Textbook Example 5, built the way the construction builds it.

    A C = 5 cm is a diagonal and the shared side of the two triangles.  B is
    the point with A B = 4.5 and B C = 5.2 above it (so triangle A B C is fixed
    by its three sides), and D is the point with B D = 5.4 and C D = 4.8 on the
    other side of A C -- the textbook's instruction.  A D is never given."""
    if origin is None:
        y = AC_Y if base_y is None else base_y
        origin = np.array([BOARD_CX - 1.6, y, 0.0])
    A = np.array(origin, dtype=float)
    C = A + np.array([5.0 * scale, 0.0, 0.0])
    B = circle_intersection(A, 4.5 * scale, C, 5.2 * scale, upper=True)
    D = circle_intersection(B, 5.4 * scale, C, 4.8 * scale, upper=False)
    return A, B, C, D


def side_label(p1, p2, centroid, text, color=CHALK_CYAN, size=17,
               offset=0.22):
    """A length label placed clear of its own side.

    Overrides the version earlier in this file, which pushed the label along
    the centroid -> midpoint direction: that direction is not perpendicular to
    the side, so the label was moved by less than the half-extent it actually
    needs and a tall side (this quadrilateral's A B is 66 degrees) ran straight
    through its own label.  Here the push is along the true outward normal."""
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


def practice_frame(origin=None, scale=0.34, base_y=-0.25):
    """Exercise 3.3(a): quadrilateral G O L D.

    O L = 7.5, L D = 5 and D G = 5.5 with the diagonal G L = 6 build triangle
    G L D by S.S.S; the diagonal O D = 10 and the side O L = 7.5 then locate O
    on the far side of G L.  G O is not given.  O hangs well below the
    diagonal, so this figure is drawn a little smaller than the example: at
    0.34 the two locating arcs still finish inside the board.  It sits a little
    right of the board's left edge (BOARD_CX - 2.3) so that it reads as centred
    in the left half instead of hugging the margin."""
    if origin is None:
        y = base_y if base_y is None else base_y
        origin = np.array([BOARD_CX - 2.3, y, 0.0])
    G = np.array(origin, dtype=float)
    L = G + np.array([6.0 * scale, 0.0, 0.0])
    D = circle_intersection(G, 5.5 * scale, L, 5.0 * scale, upper=True)
    O = circle_intersection(L, 7.5 * scale, D, 10.0 * scale, upper=False)
    return G, O, L, D


# ---------------------------------------------------------------- narration --
NARRATION = {
    "title": (
        "How do we construct a quadrilateral when we are given three sides and "
        "two diagonals?<bookmark mark='b0'/> There is no angle and no fourth "
        "side, so first we must sort the measurements and find a triangle we "
        "can build.<bookmark mark='b1'/>"
    ),
    "scene1": (
        "Here is our problem.<bookmark mark='b0'/> Three sides: A B is four "
        "point five centimetres, B C is five point two, and C D is four point "
        "eight.<bookmark mark='b0b'/> And two diagonals: A C is five "
        "centimetres, and B D is five point four.<bookmark mark='b1'/> Three "
        "sides and two diagonals: that is the measurement set.<bookmark "
        "mark='b2'/> So which three should we use first?<bookmark mark='b3'/>"
    ),
    "scene2": (
        "A diagonal joins opposite corners, so it belongs to a triangle."
        "<bookmark mark='b0'/> "
        "Look at the triangle A B C: we know A B is four point five, B C is "
        "five point two, and the diagonal A C is five.<bookmark mark='b1'/> "
        "Three known lengths, all in one triangle.<bookmark mark='b2'/> So "
        "triangle A B C can be built first, by side, side, side."
        "<bookmark mark='b3'/>"
    ),
    "scene3": (
        "That is the whole plan.<bookmark mark='b0'/> Three measurements build "
        "the first triangle: two sides and the diagonal between them."
        "<bookmark mark='b1'/> The other two measurements, the side C D and the "
        "diagonal B D, locate the fourth vertex.<bookmark mark='b2'/> Three "
        "build, and two locate.<bookmark mark='b3'/>"
    ),
    "scene4": (
        "Let us construct it accurately.<bookmark mark='b0'/> Draw the diagonal "
        "A C, five centimetres long, and label the ends A and C.<bookmark "
        "mark='b1'/> Set the compasses to four point five centimetres, the "
        "length of A B,<bookmark mark='b2'/> and put the needle at A. Every "
        "point on this arc is four point five centimetres from A, so B lies "
        "somewhere on it.<bookmark mark='b3'/>"
    ),
    "scene5": (
        "Now set the compasses to five point two centimetres and put the needle "
        "at C.<bookmark mark='b0'/> Draw the second arc, and where the two arcs "
        "cross, that point is B.<bookmark mark='b1'/> Join A to B and B to C: "
        "triangle A B C is fixed by its three sides.<bookmark mark='b2'/>"
    ),
    "scene6": (
        "Only the fourth vertex is left.<bookmark mark='b0'/> D lies on the "
        "other side of the diagonal A C, and it must be five point four "
        "centimetres from B and four point eight centimetres from C."
        "<bookmark mark='b1'/> So set the compasses to five point four, the "
        "diagonal B D, and draw an arc about B.<bookmark mark='b2'/> Then set "
        "them to four point eight, the side C D, and draw an arc about C."
        "<bookmark mark='b3'/> Where those two arcs cross is D: one diagonal "
        "and one side have located it.<bookmark mark='b4'/>"
    ),
    "scene7": (
        "Now we finish the figure.<bookmark mark='b0'/> Join C to D, join the "
        "diagonal B to D, and join A to D to close the quadrilateral."
        "<bookmark mark='b1'/> Let us check every measurement: A B is four "
        "point five, B C is five point two, C D is four point eight, the "
        "diagonal A C is five, and the diagonal B D is five point four. All "
        "five are used.<bookmark mark='b2'/> And A D was never given: the "
        "construction decided it.<bookmark mark='b3'/>"
    ),
    "scene8": (
        "This is the method, and it works for every problem of this kind."
        "<bookmark mark='b0'/> First sketch the figure and mark what is given. "
        "Then find the triangle whose three lengths are all known, and build "
        "that one. Then use the remaining side and diagonal as radii, and "
        "intersect those arcs. Finally join the last sides, and verify."
        "<bookmark mark='b1'/> Could we have started with triangle A B D "
        "instead? No: A D is not given, so that triangle has only two known "
        "sides.<bookmark mark='b2'/>"
    ),
    "scene9_setup": (
        "Your turn.<bookmark mark='b0'/> In quadrilateral G O L D, G L is six "
        "centimetres, L D is five centimetres, D G is five point five "
        "centimetres, O L is seven point five centimetres, and the diagonal "
        "O D is ten centimetres.<bookmark mark='b1'/> Which triangle should you "
        "construct first?<bookmark mark='b2'/> Pause the video and decide."
        "<bookmark mark='b3'/>"
    ),
    "scene9_reveal": (
        "Let us check.<bookmark mark='b0'/> The diagonal is G L, so the two "
        "triangles are G O L and G L D.<bookmark mark='b1'/> In triangle G L D "
        "we know G L is six, L D is five, and D G is five point five: three "
        "known lengths, so triangle G L D comes first.<bookmark mark='b2'/> "
        "Then O is found by two arcs: radius seven point five about L, and "
        "radius ten about D. Where they cross is O, and the quadrilateral "
        "G O L D is complete.<bookmark mark='b3'/>"
    ),
    "scene10": (
        "Let us put the method together.<bookmark mark='b0'/> Two sides and one "
        "diagonal build the first triangle.<bookmark mark='b1'/> One side and "
        "one diagonal locate the fourth vertex, as the intersection of two "
        "arcs.<bookmark mark='b2'/> Triangle first, then the missing vertex."
        "<bookmark mark='b3'/> Thank you for watching!<bookmark mark='b4'/> See "
        "you in the next lesson!<bookmark mark='b5'/>"
    ),
}

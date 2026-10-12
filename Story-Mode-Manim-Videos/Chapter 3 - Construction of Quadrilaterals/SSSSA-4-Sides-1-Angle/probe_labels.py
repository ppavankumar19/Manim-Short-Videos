"""Pick the S vertex-letter placement that no construction line crosses, and
fix the scene-10 recap layout for the corrected (wider) figure."""
import numpy as np
from manim import *

import construct_quadrilateral_4sides_1angle as M

X0, X1, Y1, Y0 = -4.45, 5.29, 3.32, -3.05
CX = 0.5
SIDES = {"DL": np.array([-1.0, -1.0, 0.0]), "DR": np.array([1.0, -1.0, 0.0]),
         "UR": np.array([1.0, 1.0, 0.0]), "UL": np.array([-1.0, 1.0, 0.0])}


def bb(m):
    return (float(m.get_corner(DL)[0]), float(m.get_corner(UR)[0]),
            float(m.get_corner(DL)[1]), float(m.get_corner(UR)[1]))


def hits(a, b):
    ax0, ax1, ay0, ay1 = bb(a)
    bx0, bx1, by0, by1 = bb(b)
    return (min(ax1, bx1) - max(ax0, bx0) > 0.01
            and min(ay1, by1) - max(ay0, by0) > 0.01)


print("=== S label placement ===")
for tag, (P, Q, R, S) in (
        ("scene6", M.example_frame()),
        ("scene10", M.example_frame(origin=np.array([CX - 4.1, -1.3, 0]),
                                    scale=0.34))):
    sc = 0.52 if tag == "scene6" else 0.34
    arc_p = M.locating_arc(P, S, 4.0 * sc, 30, M.CHALK_PINK)
    arc_r = M.locating_arc(R, S, 5.5 * sc, 40 if tag == "scene6" else 25,
                           M.CHALK_GREEN)
    guide1 = DashedLine(P, S)
    guide2 = DashedLine(R, S)
    edge = Polygon(P, Q, R, S)
    others = {"arc_p": arc_p, "arc_r": arc_r, "guidePS": guide1,
              "guideRS": guide2, "edges": edge}
    print(f"-- {tag}: S at {np.round(S, 2)}")
    for side in SIDES:
        lab = M.vertex_label("S", S, side, M.CHALK_WHITE, 17)
        bad = [nm for nm, m in others.items() if hits(lab, m)]
        x0, x1, y0, y1 = bb(lab)
        off = "OFF-BOARD" if (x0 < X0 or x1 > X1 or y0 < Y0 or y1 > Y1) else ""
        print(f"   {side}: bbox x[{x0:+.2f}..{x1:+.2f}] y[{y0:+.2f}..{y1:+.2f}]"
              f"  clashes={bad or 'none'} {off}")

print("=== scene 10 recap: figure left, rows right ===")
rows = VGroup(
    M.summary_row(1, "Two sides + included angle:", r"\triangle PQR",
                  M.CHALK_YELLOW),
    M.summary_row(2, "Remaining two sides as radii:", r"PS,\ RS", M.CHALK_PINK),
    M.summary_row(3, "Intersection gives the fourth vertex:", r"S",
                  M.CHALK_GREEN),
).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(np.array([CX + 1.9, 1.35, 0]))
final = M.board_text("3 measurements build the triangle, 2 more locate the "
                     "fourth vertex.", 19, M.CHALK_GREEN, "BOLD").move_to(
    np.array([CX, -1.75, 0]))
small = M.board_text("Sketch → Triangle → Arcs → Join → Verify", 17,
                     M.CHALK_WHITE, "BOLD").move_to(np.array([CX, -2.3, 0]))
head = M.board_text("S.S.S.S.A", 26, M.CHALK_AMBER, "BOLD").move_to(
    np.array([CX, 2.72, 0]))
print("  rows   ", np.round(bb(rows), 2))
print("  final  ", np.round(bb(final), 2))
for ox, oy, sc, side in ((-4.1, -1.3, 0.34, "UR"), (-4.1, -1.2, 0.36, "UR"),
                         (-4.0, -1.35, 0.34, "DL")):
    P, Q, R, S = M.example_frame(origin=np.array([CX + ox, oy, 0]), scale=sc)
    quad = Polygon(P, Q, R, S)
    names = VGroup(M.vertex_label("P", P, "DL", M.CHALK_WHITE, 16),
                   M.vertex_label("Q", Q, "DR", M.CHALK_WHITE, 16),
                   M.vertex_label("R", R, "UR", M.CHALK_WHITE, 16),
                   M.vertex_label("S", S, side, M.CHALK_WHITE, 16))
    arc_p = M.locating_arc(P, S, 4.0 * sc, 30, M.CHALK_PINK)
    arc_r = M.locating_arc(R, S, 5.5 * sc, 25, M.CHALK_GREEN)
    body = VGroup(quad, names, arc_p, arc_r)
    print(f"-- ox={ox} oy={oy} scale={sc} side={side}: P{P.round(2)} "
          f"Q{Q.round(2)} R{R.round(2)} S{S.round(2)}")
    print("   figure ", np.round(bb(body), 2),
          "clash rows:", hits(body, rows), "clash final:", hits(body, final),
          "clash small:", hits(body, small), "clash head:", hits(body, head))
    print("   arcs through S:", round(float(np.linalg.norm(
        np.array(arc_p.point_from_proportion(0.5)) - np.array(S))), 3),
        round(float(np.linalg.norm(
            np.array(arc_r.point_from_proportion(0.5)) - np.array(S))), 3))

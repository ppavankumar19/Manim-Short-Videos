"""Check the corrected layouts: everything inside the *visible* board edges
(x -4.45..5.29, y -3.05..3.32) and no two elements overlapping."""
import numpy as np
from manim import *

import construct_quadrilateral_4sides_1angle as M

# the board as it actually appears in the chalkboard background image
X0, X1, Y1, Y0 = -4.45, 5.29, 3.32, -3.05
CX = 0.5


def bb(m):
    return (float(m.get_corner(DL)[0]), float(m.get_corner(UR)[0]),
            float(m.get_corner(DL)[1]), float(m.get_corner(UR)[1]))


def show(name, *mobs):
    xs0 = min(bb(m)[0] for m in mobs)
    xs1 = max(bb(m)[1] for m in mobs)
    ys0 = min(bb(m)[2] for m in mobs)
    ys1 = max(bb(m)[3] for m in mobs)
    bad = ""
    if xs0 < X0 + 0.06 or xs1 > X1 - 0.06:
        bad += "  <<OFF-X"
    if ys0 < Y0 + 0.06 or ys1 > Y1 - 0.06:
        bad += "  <<OFF-Y"
    print(f"{name:34s} x[{xs0:+.2f}..{xs1:+.2f}] y[{ys0:+.2f}..{ys1:+.2f}]{bad}")


def clash(a, b, name):
    ax0, ax1, ay0, ay1 = bb(a)
    bx0, bx1, by0, by1 = bb(b)
    ox = min(ax1, bx1) - max(ax0, bx0)
    oy = min(ay1, by1) - max(ay0, by0)
    if ox > 0.02 and oy > 0.02:
        print(f"  !! OVERLAP {name}: {ox:.2f} x {oy:.2f}")
    else:
        print(f"  ok  {name}: gap x={-ox:.2f} y={-oy:.2f}")


print("==== SCENE 1 ====")
cards = VGroup(
    M.measure_card(r"PQ=4.5", M.CHALK_CYAN),
    M.measure_card(r"QR=5.2", M.CHALK_CYAN),
    M.measure_card(r"RS=5.5", M.CHALK_CYAN),
    M.measure_card(r"PS=4", M.CHALK_CYAN),
    M.measure_card(r"\angle RQP=120^\circ", M.CHALK_YELLOW),
).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(np.array([CX, 0.32, 0]))
strip = M.board_text("Side + Side + Side + Side + Angle", 18, M.CHALK_GREEN,
                     "BOLD").move_to(np.array([CX + 2.1, -1.75, 0]))
box = SurroundingRectangle(strip, color=M.CHALK_GREEN, buff=0.16,
                           corner_radius=0.1, stroke_width=2.6)
ask = M.board_text("Where should we start?", 18, M.CHALK_WHITE, "BOLD").move_to(
    np.array([CX + 2.1, -2.5, 0]))
head = M.board_text("Four Sides + One Angle", 24, M.CHALK_AMBER, "BOLD").move_to(
    np.array([CX, 2.72, 0]))
show("heading", head)
show("cards", cards)
show("strip + box", strip, box)
show("ask", ask)
clash(cards, box, "cards/box")
clash(box, ask, "box/ask")
clash(head, cards, "heading/cards")

print("==== SCENE 3 ====")
P, Q, R, S = M.example_frame()
tri = Polygon(P, Q, R)
fullq = Polygon(P, Q, R, S)
note = M.board_text("Three measurements fix this triangle.", 17, M.CHALK_WHITE,
                    "BOLD").move_to(np.array([CX + 1.75, -1.6, 0]))
sas = M.measure_card(r"\text{Side}+\text{Angle}+\text{Side}", M.CHALK_GREEN,
                     17).move_to(np.array([CX + 2.9, 1.4, 0]))
sas2 = M.measure_card(r"\text{S.A.S}", M.CHALK_GREEN, 17).move_to(
    np.array([CX + 2.9, 0.7, 0]))
lab_pq = M.board_text("PQ = 4.5", 16, M.CHALK_YELLOW, "BOLD").move_to(
    (P + Q) / 2 + DOWN * 0.32)
lab_qr = M.board_text("QR = 5.2", 16, M.CHALK_YELLOW, "BOLD").move_to(
    (Q + R) / 2 + np.array([0.62, 0.06, 0]))
for nm, m in (("figure", fullq), ("note", note), ("sas", sas), ("sas2", sas2),
              ("lab_pq", lab_pq), ("lab_qr", lab_qr)):
    show(nm, m)
clash(fullq, note, "figure/note")
clash(note, lab_pq, "note/lab_pq")
clash(sas, sas2, "sas/sas2")
clash(fullq, sas, "figure/sas")
clash(fullq, sas2, "figure/sas2")

print("==== SCENE 4 / 5 ray (must stay below the heading) ====")
for label, ext in (("scene4", 0.25), ("scene5", 0.22)):
    ray = DashedLine(Q, R + ext * (R - Q))
    hd = M.board_text("STEP 2", 22, M.CHALK_AMBER, "BOLD").move_to(
        np.array([CX, 2.72, 0]))
    show(f"{label} ray", ray)
    clash(ray, hd, f"{label} ray/heading")

print("==== SCENE 6 arcs (must pass through S) ====")
P, Q, R, S = M.example_frame()
ap = M.locating_arc(P, S, 4.0 * M.SCALE, 30, M.CHALK_PINK)
ar = M.locating_arc(R, S, 5.5 * M.SCALE, 40, M.CHALK_GREEN)
for nm, arc, ctr, rad in (("arc_p", ap, P, 4.0 * M.SCALE),
                          ("arc_r", ar, R, 5.5 * M.SCALE)):
    d = float(np.linalg.norm(np.array(arc.point_from_proportion(0.5)) - np.array(S)))
    show(nm, arc)
    print(f"     {nm}: midpoint distance to S = {d:.3f} (radius {rad:.2f})"
          f"  {'PASSES THROUGH S' if d < 0.02 else 'MISSES S'}")
guide1 = DashedLine(P, S, color=M.CHALK_WHITE, stroke_width=1.8,
                    dash_length=0.12)
guide2 = DashedLine(R, S, color=M.CHALK_WHITE, stroke_width=1.8,
                    dash_length=0.12)
show("figure + guides", Polygon(P, Q, R, S), guide1, guide2)

print("==== SCENE 9 reveal badge ====")
A, B, C, D = M.exercise_frame(origin=np.array([CX - 2.6, -0.35, 0]), scale=0.40)
cards9 = VGroup(
    M.measure_card(r"AB=5.5", M.CHALK_CYAN, 15),
    M.measure_card(r"BC=3.5", M.CHALK_CYAN, 15),
    M.measure_card(r"CD=4", M.CHALK_CYAN, 15),
    M.measure_card(r"AD=5", M.CHALK_CYAN, 15),
    M.measure_card(r"\angle A=45^\circ", M.CHALK_YELLOW, 15),
).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
print("     cards9 arranged bbox:", np.round(bb(cards9), 2),
      "-> scene places them at x=3.0")
badge = M.board_text("First triangle: BAD", 18, M.CHALK_GREEN, "BOLD").move_to(
    np.array([CX + 2.5, -1.35, 0]))
show("badge", badge)
show("figure", Polygon(A, B, C, D))
print("     cards9 shifted to x=3.0 -> y range",
      np.round(bb(cards9)[2:], 2))
clash(badge, cards9, "badge/cards(y-only)")

print("==== SCENE 10 ====")
P, Q, R, S = M.example_frame(origin=np.array([CX - 2.1, -1.15, 0]), scale=0.36)
quad = Polygon(P, Q, R, S)
tri = Polygon(P, Q, R)
names = M.quad_names((P, Q, R, S), "PQRS", 17)
ap = M.locating_arc(P, S, 4.0 * 0.36, 30, M.CHALK_PINK)
ar = M.locating_arc(R, S, 5.5 * 0.36, 40, M.CHALK_GREEN)
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
hd = M.board_text("S.S.S.S.A", 26, M.CHALK_AMBER, "BOLD").move_to(
    np.array([CX, 2.72, 0]))
print("     P", np.round(P, 2), "Q", np.round(Q, 2), "R", np.round(R, 2),
      "S", np.round(S, 2))
for nm, m in (("heading", hd), ("rows", rows), ("names", names), ("quad", quad),
              ("arc_p", ap), ("arc_r", ar), ("final", final), ("small", small)):
    show(nm, m)
clash(hd, rows, "heading/rows")
clash(rows, quad, "rows/quad")
clash(rows, names, "rows/names")
clash(rows, ar, "rows/arc_r")
clash(rows, ap, "rows/arc_p")
clash(quad, final, "quad/final")
clash(names, final, "names/final")
clash(ar, final, "arc_r/final")
clash(ap, final, "arc_p/final")
for nm, arc in (("arc_p", ap), ("arc_r", ar)):
    d = float(np.linalg.norm(np.array(arc.point_from_proportion(0.5)) - np.array(S)))
    print(f"     {nm} midpoint distance to S = {d:.3f}"
          f"  {'PASSES THROUGH S' if d < 0.02 else 'MISSES S'}")

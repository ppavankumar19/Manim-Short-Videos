"""Layout check for the corrected Example-1 geometry (interior angle at Q is
120 degrees, so Q R leaves Q at 60 degrees above the base).

Board as it actually appears in the chalkboard image: x -4.45..5.29,
y -3.05..3.32.  Reports every crowded element's extent plus pairwise clashes.
"""
import numpy as np
from manim import *

import construct_quadrilateral_4sides_1angle as M

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
    print(f"  {name:26s} x[{xs0:+.2f}..{xs1:+.2f}] y[{ys0:+.2f}..{ys1:+.2f}]{bad}")


def clash(a, b, name):
    ax0, ax1, ay0, ay1 = bb(a)
    bx0, bx1, by0, by1 = bb(b)
    ox = min(ax1, bx1) - max(ax0, bx0)
    oy = min(ay1, by1) - max(ay0, by0)
    if ox > 0.02 and oy > 0.02:
        print(f"  !! OVERLAP {name}: {ox:.2f} x {oy:.2f}")
    else:
        print(f"  ok  {name}: gap x={-ox:.2f} y={-oy:.2f}")


def angle_at(v, a, b):
    u1 = np.array(a, float) - np.array(v, float)
    u2 = np.array(b, float) - np.array(v, float)
    return float(np.degrees(np.arccos(np.clip(
        np.dot(u1, u2) / (np.linalg.norm(u1) * np.linalg.norm(u2)), -1, 1))))


print("=== GEOMETRY (default frame, scale 0.52) ===")
P, Q, R, S = M.example_frame()
print("  P", np.round(P, 2), "Q", np.round(Q, 2), "R", np.round(R, 2),
      "S", np.round(S, 2))
print(f"  PQ={np.linalg.norm(Q - P) / M.SCALE:.2f}  "
      f"QR={np.linalg.norm(R - Q) / M.SCALE:.2f}  "
      f"RS={np.linalg.norm(S - R) / M.SCALE:.2f}  "
      f"PS={np.linalg.norm(S - P) / M.SCALE:.2f}  "
      f"angleQ={angle_at(Q, P, R):.1f}  angleP={angle_at(P, Q, S):.1f}  "
      f"angleR={angle_at(R, Q, S):.1f}  angleS={angle_at(S, P, R):.1f}")

print("=== SCENE 3: which three measurements first ===")
tri = Polygon(P, Q, R)
fullq = Polygon(P, Q, R, S)
names = M.quad_names((P, Q, R, S), "PQRS", 18)
lab_pq = M.board_text("PQ = 4.5", 16, M.CHALK_YELLOW, "BOLD").move_to(
    (P + Q) / 2 + DOWN * 0.32)
lab_qr = M.board_text("QR = 5.2", 16, M.CHALK_YELLOW, "BOLD").move_to(
    (Q + R) / 2 + np.array([0.62, 0.06, 0]))
q_arc = M.angle_mark(Q, P, R, radius=0.5, color=M.CHALK_PINK, label="120°")
sas = M.measure_card(r"\text{Side}+\text{Angle}+\text{Side}", M.CHALK_GREEN,
                     17).move_to(np.array([CX + 2.9, 1.4, 0]))
sas2 = M.measure_card(r"\text{S.A.S}", M.CHALK_GREEN, 17).move_to(
    np.array([CX + 2.9, 0.7, 0]))
note = M.board_text("Three measurements fix this triangle.", 17, M.CHALK_WHITE,
                    "BOLD").move_to(np.array([CX + 1.75, -1.75, 0]))
show("figure", fullq)
show("names", names)
show("lab_pq", lab_pq)
show("lab_qr", lab_qr)
show("120 label", q_arc)
show("sas cards", sas, sas2)
show("note", note)
clash(fullq, sas, "figure/sas")
clash(fullq, note, "figure/note")
clash(lab_pq, note, "lab_pq/note")
clash(lab_qr, sas2, "lab_qr/sas2")
clash(names[1], lab_pq, "nameQ/lab_pq")
clash(q_arc, lab_qr, "120arc/lab_qr")

print("=== SCENE 4: draw PQ and the 120 ray ===")
base = Line(P, Q)
ray = DashedLine(Q, R + 0.25 * (R - Q))
prot = M.protractor(Q, radius=1.05)
note4 = M.board_text("R must lie somewhere on this ray.", 19, M.CHALK_GREEN,
                     "BOLD").move_to(np.array([CX + 2.2, -1.7, 0]))
head4 = M.board_text("STEP 2 - PQ and the 120 Angle", 22, M.CHALK_AMBER,
                     "BOLD").move_to(np.array([CX, 2.72, 0]))
show("base+ray", base, ray)
show("protractor", prot)
show("note", note4)
show("names", M.VGroup(M.vertex_label("P", P, "DL"), M.vertex_label("Q", Q, "DR")))
clash(ray, head4, "ray/heading")
clash(prot, note4, "protractor/note")
clash(ray, sas, "ray/sas(not in scene)")

print("=== SCENE 5: the arc that fixes R ===")
arc5 = M.locating_arc(Q, R, 5.2 * M.SCALE, 22, M.CHALK_GREEN)
rad5 = M.radius_line(Q, Q + 5.2 * M.SCALE * np.array(
    [np.cos(45 * DEGREES), np.sin(45 * DEGREES), 0.0]), M.CHALK_GREEN,
    "5.2 cm")
lab_qr5 = M.board_text("QR = 5.2 cm", 16, M.CHALK_GREEN, "BOLD").move_to(
    (Q + R) / 2 + np.array([0.6, 0.1, 0]))
r_name = M.vertex_label("R", R, "UR")
note5 = M.board_text("Three measurements used. Two still left: PS = 4, "
                     "RS = 5.5.", 18, M.CHALK_WHITE, "BOLD").move_to(
    np.array([CX, -2.1, 0]))
for nm, m in (("arc", arc5), ("rad", rad5), ("lab_qr", lab_qr5), ("R name",
              r_name), ("note", note5)):
    show(nm, m)
d, _ = 0.0, 0
print(f"  arc midpoint check: distance to R = "
      f"{float(np.linalg.norm(np.array(arc5.point_from_proportion(0.5)) - np.array(R))):.3f}")
clash(arc5, note5, "arc5/note")
clash(rad5, arc5, "rad/arc (overlap expected)")

print("=== SCENE 6: two arcs locate S ===")
arc_p = M.locating_arc(P, S, 4.0 * M.SCALE, 30, M.CHALK_PINK)
arc_r = M.locating_arc(R, S, 5.5 * M.SCALE, 40, M.CHALK_GREEN)
rad_p = M.radius_line(P, S, M.CHALK_PINK, "PS = 4 cm")
rad_r = M.radius_line(R, S, M.CHALK_GREEN, "RS = 5.5 cm")
s_name = M.vertex_label("S", S, "UL").shift(np.array([-0.12, 0.12, 0]))
note6 = M.board_text("S satisfies both distances.", 19, M.CHALK_GREEN,
                     "BOLD").move_to(np.array([CX, -2.2, 0]))
for nm, m in (("arc_p", arc_p), ("arc_r", arc_r), ("rad_p", rad_p),
              ("rad_r", rad_r), ("S name", s_name), ("note", note6)):
    show(nm, m)
for nm, a in (("arc_p", arc_p), ("arc_r", arc_r)):
    d = float(np.linalg.norm(np.array(a.point_from_proportion(0.5)) - np.array(S)))
    print(f"  {nm} through S: {d:.3f}  {'OK' if d < 0.02 else 'MISSES'}")
clash(s_name, arc_p, "Sname/arc_p")
clash(s_name, arc_r, "Sname/arc_r")

print("=== SCENE 7: complete and verify ===")
quad7 = Polygon(P, Q, R, S)
checks = VGroup(
    M.check_row(r"PQ=4.5", M.CHALK_GREEN, 15),
    M.check_row(r"QR=5.2", M.CHALK_GREEN, 15),
    M.check_row(r"RS=5.5", M.CHALK_GREEN, 15),
    M.check_row(r"PS=4", M.CHALK_GREEN, 15),
    M.check_row(r"\angle RQP=120^\circ", M.CHALK_YELLOW, 15),
).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to(
    np.array([CX + 3.0, 0.0, 0]))
title7 = M.board_text("All five measurements used.", 19, M.CHALK_GREEN,
                      "BOLD").move_to(np.array([CX, -2.35, 0]))
show("quad", quad7)
show("checks", checks)
show("title", title7)
clash(quad7, checks, "quad/checks")
clash(M.quad_names((P, Q, R, S), "PQRS", 17), checks, "names/checks")
clash(checks, title7, "checks/title")

print("=== SCENE 8: the reusable method + mini construction ===")
P8, Q8, R8, S8 = M.example_frame(origin=np.array([CX + 2.2, 0.55, 0]),
                                 scale=0.30)
mini = VGroup(
    Polygon(P8, Q8, R8, S8),
    M.locating_arc(P8, S8, 4.0 * 0.30, 30, M.CHALK_PINK),
    M.locating_arc(R8, S8, 5.5 * 0.30, 35, M.CHALK_GREEN),
)
cards8 = VGroup(
    M.combo_card("1. SKETCH", "mark all 5 measurements", M.CHALK_CYAN),
    M.combo_card("2. TRIANGLE", "2 sides + included angle", M.CHALK_GREEN),
    M.combo_card("3. TWO ARCS", "remaining lengths as radii", M.CHALK_PINK),
    M.combo_card("4. JOIN", "complete and verify", M.CHALK_YELLOW),
).arrange(DOWN, buff=0.20, aligned_edge=LEFT).move_to(
    np.array([CX - 2.35, 0.35, 0]))
names8 = M.quad_names((P8, Q8, R8, S8), "PQRS", 14)
names8[3].shift(np.array([-0.10, 0.10, 0]))
note8 = M.board_text("Sketch → Triangle → Arcs → Join → Verify", 18,
                     M.CHALK_WHITE, "BOLD").move_to(np.array([CX, -2.35, 0]))
head8 = M.board_text("The S.S.S.S.A Method", 23, M.CHALK_AMBER, "BOLD").move_to(
    np.array([CX, 2.72, 0]))
for nm, m in (("cards", cards8), ("mini", mini), ("names", names8),
              ("note", note8), ("heading", head8)):
    show(nm, m)
clash(cards8, mini, "cards/mini")
clash(cards8, names8, "cards/names")
clash(mini, head8, "mini/heading")
clash(names8, head8, "names/heading")
clash(mini, note8, "mini/note")
for nm, a, tgt, rad in (("arc_p", mini[1], S8, 4.0 * 0.30),
                        ("arc_r", mini[2], S8, 5.5 * 0.30)):
    d = float(np.linalg.norm(np.array(a.point_from_proportion(0.5)) - np.array(tgt)))
    print(f"  {nm} through S: {d:.3f}  {'OK' if d < 0.02 else 'MISSES'}")

print("=== SCENE 10: recap mini ===")
for oy, sc, spread in ((-1.3, 0.34, 25),):
    P10, Q10, R10, S10 = M.example_frame(
        origin=np.array([CX - 4.1, oy, 0]), scale=sc)
    q10 = Polygon(P10, Q10, R10, S10)
    n10 = M.quad_names((P10, Q10, R10, S10), "PQRS", 17)
    n10[3].shift(np.array([-0.12, 0.12, 0]))
    ap = M.locating_arc(P10, S10, 4.0 * sc, 30, M.CHALK_PINK)
    ar = M.locating_arc(R10, S10, 5.5 * sc, spread, M.CHALK_GREEN)
    print(f"  -- origin_y={oy} scale={sc} spread={spread}")
    show("quad", q10)
    show("names", n10)
    show("arc_p", ap)
    show("arc_r", ar)
    clash(q10, ar, "quad/arc_r")
    clash(n10, ar, "names/arc_r")
    clash(ap, ar, "arc_p/arc_r")

print("=== SCENE 10 fixed furniture ===")
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
head10 = M.board_text("S.S.S.S.A", 26, M.CHALK_AMBER, "BOLD").move_to(
    np.array([CX, 2.72, 0]))
for nm, m in (("rows", rows), ("final", final), ("small", small),
              ("heading", head10)):
    show(nm, m)

print("=== TITLE scene figure ===")
Pt, Qt, Rt, St = M.example_frame(origin=np.array([CX - 0.7, -1.25, 0]),
                                 scale=0.34)
show("title figure", Polygon(Pt, Qt, Rt, St))
show("title names", M.VGroup(*[M.vertex_label(t, p, s, M.CHALK_WHITE, 15)
                               for t, p, s in zip("PQRS", (Pt, Qt, Rt, St),
                                                  ("DL", "DR", "UR", "UL"))]))
show("title tag", M.board_text("Steps: sketch, triangle, arcs, join", 18,
                               M.CHALK_GREEN, "BOLD").move_to(
    np.array([CX, -2.45, 0])))

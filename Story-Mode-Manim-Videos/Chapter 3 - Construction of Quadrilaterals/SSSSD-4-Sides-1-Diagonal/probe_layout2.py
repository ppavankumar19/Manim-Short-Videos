import numpy as np
from manim import *
import construct_quadrilateral_4sides_1diagonal as M

def bb(m):
    return (float(m.get_corner(DL)[0]), float(m.get_corner(UR)[0]),
            float(m.get_corner(DL)[1]), float(m.get_corner(UR)[1]))

def show(name, *mobs):
    xs0 = min(bb(m)[0] for m in mobs); xs1 = max(bb(m)[1] for m in mobs)
    ys0 = min(bb(m)[2] for m in mobs); ys1 = max(bb(m)[3] for m in mobs)
    bad = ""
    if xs0 < -4.39 or xs1 > 5.23: bad += "  <<OFF-X"
    if ys0 < -2.99 or ys1 > 3.26: bad += "  <<OFF-Y"
    print(f"  {name:24s} x[{xs0:+.2f}..{xs1:+.2f}] y[{ys0:+.2f}..{ys1:+.2f}]{bad}")

def clash(a, b, nm):
    ax0, ax1, ay0, ay1 = bb(a); bx0, bx1, by0, by1 = bb(b)
    ox = min(ax1, bx1) - max(ax0, bx0); oy = min(ay1, by1) - max(ay0, by0)
    print(f"  {'!! OVERLAP' if (ox > 0.02 and oy > 0.02) else 'ok  '} {nm}: {ox:+.2f} x {oy:+.2f}")

def clear_of(label, curve):
    x0, x1, y0, y1 = bb(label); best = 9.9
    for part in [m for m in curve.get_family() if len(getattr(m, "points", ()))]:
        for t in np.linspace(0, 1, 150):
            p = part.point_from_proportion(t)
            dx = max(x0 - p[0], 0.0, p[0] - x1); dy = max(y0 - p[1], 0.0, p[1] - y1)
            best = min(best, float(np.hypot(dx, dy)))
    return best

sc = M.SCALE
print("=== SCENE 4: compass about A ===")
A, B, C, D = M.example_frame()
lab_ac = M.board_text("AC = 5 cm", 17, M.CHALK_CYAN, "BOLD").move_to(C + np.array([-0.58, -0.32, 0]))
note = M.board_text("B is 4 cm from A, so it lies on this arc.", 18, M.CHALK_GREEN, "BOLD").move_to(np.array([M.BOARD_CX, -2.55, 0]))
arc, tool, sweep = M.compass_arc_drawer(A, B, 4.0 * sc, 24, M.CHALK_CYAN, hinge_dir=(1.0, -1.0, 0.0))
show("lab_ac", lab_ac); show("note", note); show("compass", arc, tool)
for lbl, nm in ((lab_ac, "lab_ac"), (note, "note")):
    g = clear_of(lbl, tool)
    print(f"  compass vs {nm}: gap {g:.3f} {'OK' if g > 0.05 else '!! TOUCHES'}")

print("=== SCENE 5: compass about C + AB/BC labels ===")
cen = np.array([A, B, C, D], dtype=float).mean(axis=0)
lab_ab = M.side_label(A, B, cen, "AB = 4 cm", M.CHALK_YELLOW, 16, 0.20)
lab_bc = M.side_label(C, B, B + C - cen, "BC = 3.6 cm", M.CHALK_YELLOW, 16, 0.20)
arc2, tool2, sw2 = M.compass_arc_drawer(C, B, 3.6 * sc, 22, M.CHALK_GREEN, hinge_dir=(1.0, 1.0, 0.0))
for nm, m in (("lab_ab", lab_ab), ("lab_bc", lab_bc), ("lab_ac", lab_ac)):
    show(nm, m)
show("compass", arc2, tool2)
for lbl, nm in ((lab_ab, "lab_ab"), (lab_bc, "lab_bc"), (lab_ac, "lab_ac")):
    g = clear_of(lbl, tool2)
    print(f"  compass vs {nm}: gap {g:.3f} {'OK' if g > 0.05 else '!! TOUCHES'}")

print("=== SCENE 6: compass about A (below) + the AD label ===")
rad_a = M.radius_line(A, D, M.CHALK_CYAN, "AD = 4.8 cm", 15)
arc3, tool3, sw3 = M.compass_arc_drawer(A, D, 4.8 * sc, 22, M.CHALK_CYAN, hinge_dir=(-1.0, -1.0, 0.0))
show("AD label", rad_a[1]); show("compass", arc3, tool3)
for lbl, nm in ((rad_a[1], "AD label"),):
    g = clear_of(lbl, tool3)
    print(f"  compass vs {nm}: gap {g:.3f} {'OK' if g > 0.05 else '!! TOUCHES'}")
clash(rad_a[1], arc3, "ADlabel/arc")

print("=== SCENE 9: clock park ===")
P, Q, R, S = M.practice_frame()
fig = Polygon(P, Q, R, S)
names = M.quad_names((P, Q, R, S), "PQRS", 16)
cards = VGroup(M.measure_card(r"PQ=4", M.CHALK_CYAN, 15), M.measure_card(r"QR=3", M.CHALK_CYAN, 15),
               M.measure_card(r"RS=5", M.CHALK_CYAN, 15), M.measure_card(r"PS=4.5", M.CHALK_CYAN, 15),
               M.measure_card(r"PR=5.5", M.CHALK_YELLOW, 15)).arrange(DOWN, buff=0.20).move_to(np.array([M.BOARD_CX + 2.4, 0.55, 0]))
clock = Circle(radius=0.9).move_to(np.array([M.BOARD_CX + 0.65, 0.5, 0]))
ask = M.board_text("Which triangle comes first?", 18, M.CHALK_WHITE, "BOLD").move_to(np.array([M.BOARD_CX - 1.0, -2.15, 0]))
for nm, m in (("clock", clock), ("figure", fig), ("names", names), ("cards", cards), ("ask", ask)):
    show(nm, m)
clash(clock, fig, "clock/figure"); clash(clock, names, "clock/names")
clash(clock, cards, "clock/cards"); clash(clock, ask, "clock/ask")

print("=== SCENE 10: figure + lines ===")
A10, B10, C10, D10 = M.example_frame(origin=np.array([M.BOARD_CX - 4.2, -1.15, 0]), scale=0.34)
n10 = M.quad_names((A10, B10, C10, D10), "ABCD", 16)
final = M.board_text("Diagonal ? Triangle ? Arcs ? Join", 17, M.CHALK_GREEN, "BOLD").move_to(np.array([M.BOARD_CX, -1.90, 0]))
take = M.board_text("Use the diagonal to make two triangles.", 16, M.CHALK_WHITE, "BOLD").move_to(np.array([M.BOARD_CX, -2.45, 0]))
for nm, m in (("figure", Polygon(A10, B10, C10, D10)), ("names", n10), ("final", final), ("take", take)):
    show(nm, m)
clash(n10, final, "names/final"); clash(n10, take, "names/take"); clash(final, take, "final/take")

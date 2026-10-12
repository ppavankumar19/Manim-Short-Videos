"""Geometry + layout proof for storyboard 03 (S.S.S.S.D).

Checks, before a render is spent:
  * the constructed quadrilateral really satisfies the five given measurements,
  * every crowded element sits inside the board and clear of its neighbours,
  * the compasses stay on the board and clear of the figure's labels.
"""
import numpy as np
from manim import *

import construct_quadrilateral_4sides_1diagonal as M

X0, X1, Y1, Y0 = -4.45, 5.29, 3.32, -3.05
CX = M.BOARD_CX


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
    tag = "!! OVERLAP" if (ox > 0.02 and oy > 0.02) else "ok  "
    print(f"  {tag} {name}: {ox:+.2f} x {oy:+.2f}")


def dist(a, b):
    return float(np.linalg.norm(np.array(a, float) - np.array(b, float)))


DEG = 180.0 / np.pi


def angle_at(v, a, b):
    """The interior angle at v between the segments v->a and v->b."""
    u1 = np.array(a, float) - np.array(v, float)
    u2 = np.array(b, float) - np.array(v, float)
    return float(np.degrees(np.arccos(np.clip(
        np.dot(u1, u2) / (np.linalg.norm(u1) * np.linalg.norm(u2)), -1, 1))))


def clear_of(label, curve):
    """Smallest real distance between a label box and a curve (0 = touching)."""
    x0, x1, y0, y1 = bb(label)
    best = 9.9
    parts = [m for m in curve.get_family() if len(getattr(m, "points", ()))]
    for part in parts:
        for t in np.linspace(0, 1, 150):
            p = part.point_from_proportion(t)
            dx = max(x0 - p[0], 0.0, p[0] - x1)
            dy = max(y0 - p[1], 0.0, p[1] - y1)
            best = min(best, float(np.hypot(dx, dy)))
    return best


print("=== EXAMPLE 3 GEOMETRY (scale 0.56) ===")
A, B, C, D = M.example_frame()
sc = M.SCALE
print(f"  AB={dist(A, B) / sc:.2f}  BC={dist(B, C) / sc:.2f}  "
      f"CD={dist(C, D) / sc:.2f}  AD={dist(A, D) / sc:.2f}  "
      f"AC={dist(A, C) / sc:.2f}")
print(f"  B {'above' if B[1] > A[1] else 'BELOW'} AC, "
      f"D {'below' if D[1] < A[1] else 'ABOVE'} AC")
print(f"  angles: A={angle_at(A, B, D):.1f}  B={angle_at(B, A, C):.1f}  "
      f"C={angle_at(C, B, D):.1f}  D={angle_at(D, A, C):.1f}")
show("figure", Polygon(A, B, C, D))
show("names", M.quad_names((A, B, C, D), "ABCD", 17))

print("=== PRACTICE SET GEOMETRY (scale 0.40) ===")
P, Q, R, S = M.practice_frame()
print(f"  PQ={dist(P, Q) / 0.40:.2f}  QR={dist(Q, R) / 0.40:.2f}  "
      f"RS={dist(R, S) / 0.40:.2f}  PS={dist(P, S) / 0.40:.2f}  "
      f"PR={dist(P, R) / 0.40:.2f}")
print(f"  Q {'above' if Q[1] > P[1] else 'BELOW'} PR, "
      f"S {'below' if S[1] < P[1] else 'ABOVE'} PR")
show("figure", Polygon(P, Q, R, S))

print("=== SCENE 1: centred measurement cards ===")
cards = VGroup(
    M.measure_card(r"AB=4", M.CHALK_CYAN), M.measure_card(r"BC=3.6", M.CHALK_CYAN),
    M.measure_card(r"CD=4.2", M.CHALK_CYAN), M.measure_card(r"AD=4.8", M.CHALK_CYAN),
    M.measure_card(r"AC=5", M.CHALK_YELLOW),
).arrange(DOWN, buff=0.24).move_to(np.array([CX, 0.55, 0]))
strip = M.board_text("4 Sides + 1 Diagonal", 21, M.CHALK_GREEN, "BOLD").move_to(
    np.array([CX, -1.79, 0]))
box = SurroundingRectangle(strip, color=M.CHALK_GREEN, buff=0.16,
                           corner_radius=0.1, stroke_width=2.6)
ask = M.board_text("Where should we start?", 19, M.CHALK_WHITE, "BOLD").move_to(
    np.array([CX, -2.54, 0]))
head = M.board_text("Four Sides and One Diagonal", 24, M.CHALK_AMBER,
                    "BOLD").move_to(np.array([CX, 2.72, 0]))
for nm, m in (("heading", head), ("cards", cards), ("box", box), ("ask", ask)):
    show(nm, m)
clash(head, cards, "heading/cards")
clash(cards, box, "cards/box")
clash(box, ask, "box/ask")

print("=== SCENE 2: split + equation + question ===")
A2, B2, C2, D2 = M.example_frame(origin=np.array([CX - 1.6, 0.55, 0]), scale=0.42)
quad2 = Polygon(A2, B2, C2, D2)
names2 = M.quad_names((A2, B2, C2, D2), "ABCD", 17)
eq = MathTex(r"ABCD", r"=", r"\triangle ABC", r"+", r"\triangle ACD",
             font_size=32).move_to(np.array([CX, -1.85, 0]))
ask2 = M.board_text("Which triangle can we build first?", 19, M.CHALK_WHITE,
                    "BOLD").move_to(np.array([CX, -2.55, 0]))
for nm, m in (("figure", quad2), ("names", names2), ("equation", eq),
              ("question", ask2)):
    show(nm, m)
clash(names2, eq, "names/equation")
clash(eq, ask2, "equation/question")
clash(quad2, eq, "figure/equation")

print("=== SCENE 3: S.S.S callout ===")
A3, B3, C3, D3 = M.example_frame(origin=np.array([CX - 1.5, 0.30, 0]))
cen3 = np.array([A3, B3, C3, D3], dtype=float).mean(axis=0)
lab_ab = M.side_label(A3, B3, cen3, "4", M.CHALK_YELLOW, 16, 0.20)
lab_bc = M.side_label(B3, C3, cen3, "3.6", M.CHALK_YELLOW, 16, 0.20)
lab_ac = M.board_text("AC = 5", 16, M.CHALK_YELLOW, "BOLD").move_to(
    (A3 + C3) / 2 + DOWN * 0.30)
sss = M.combo_card("Side + Side + Side", "three known sides", M.CHALK_GREEN)
sss.move_to(np.array([CX + 3.1, 0.55, 0]))
note3 = M.board_text("No angle is needed here.", 18, M.CHALK_WHITE, "BOLD"
                     ).move_to(np.array([CX, -2.55, 0]))
names3 = M.quad_names((A3, B3, C3, D3), "ABCD", 17)
for nm, m in (("figure", Polygon(A3, B3, C3, D3)), ("names", names3),
              ("lab_ab", lab_ab), ("lab_bc", lab_bc), ("lab_ac", lab_ac),
              ("sss card", sss), ("note", note3)):
    show(nm, m)
clash(sss, names3, "sss/names")
clash(sss, lab_bc, "sss/lab_bc")
clash(lab_ac, note3, "lab_ac/note")
clash(names3, note3, "names/note")

print("=== SCENE 4/5/6: compasses on the construction ===")
for tag, origin in (("scene4/5", None),):
    A4, B4, C4, D4 = M.example_frame(origin=origin)
    base = Line(A4, C4)
    lab_ac4 = M.board_text("AC = 5 cm", 17, M.CHALK_CYAN, "BOLD").move_to(
        (A4 + C4) / 2 + DOWN * 0.32)
    note4 = M.board_text("B is 4 cm from A, so it lies on this arc.", 18,
                         M.CHALK_GREEN, "BOLD").move_to(np.array([CX, -2.55, 0]))
    show("base+labels", base, lab_ac4)
    show("note", note4)
    clash(lab_ac4, note4, "lab_ac/note")
    for hinge, r, tgt, nm in (((1.0, -1.0, 0.0), 4.0 * sc, B4, "A-arc"),
                              ((1.0, 1.0, 0.0), 3.6 * sc, B4, "C-arc"),
                              ((-1.0, -1.0, 0.0), 4.8 * sc, D4, "A-D-arc")):
        ctr = A4 if nm.startswith("A") else C4
        arc, tool, sweep = M.compass_arc_drawer(
            ctr, tgt, r, 22, M.CHALK_CYAN, hinge_dir=hinge)
        show(f"compass {nm}", arc, tool)
        for lbl, lname in ((lab_ac4, "lab_ac"), (note4, "note")):
            g = clear_of(lbl, tool)
            if g < 0.05:
                print(f"  !! compass {nm} touches {lname} (gap {g:.3f})")

print("=== SCENE 7: figure + tick rows ===")
A7, B7, C7, D7 = M.example_frame()
quad7 = Polygon(A7, B7, C7, D7)
names7 = M.quad_names((A7, B7, C7, D7), "ABCD", 17)
checks = VGroup(
    M.check_row(r"AB=4", M.CHALK_GREEN, 15), M.check_row(r"BC=3.6", M.CHALK_GREEN, 15),
    M.check_row(r"CD=4.2", M.CHALK_GREEN, 15), M.check_row(r"AD=4.8", M.CHALK_GREEN, 15),
    M.check_row(r"AC=5", M.CHALK_YELLOW, 15),
).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to(
    np.array([CX + 3.0, 0.1, 0]))
title7 = M.board_text("All five measurements used.", 19, M.CHALK_GREEN,
                      "BOLD").move_to(np.array([CX, -2.55, 0]))
for nm, m in (("figure", quad7), ("names", names7), ("checks", checks),
              ("title", title7)):
    show(nm, m)
clash(names7, checks, "names/checks")
clash(checks, title7, "checks/title")
clash(names7, title7, "names/title")

print("=== SCENE 8: method cards + mini ===")
steps = VGroup(
    M.combo_card("1. SKETCH", "mark 4 sides + the diagonal", M.CHALK_CYAN),
    M.combo_card("2. TRIANGLE", "diagonal + 2 sides, by SSS", M.CHALK_GREEN),
    M.combo_card("3. TWO ARCS", "remaining sides as radii", M.CHALK_PINK),
    M.combo_card("4. JOIN", "complete and verify", M.CHALK_YELLOW),
).arrange(DOWN, buff=0.20, aligned_edge=LEFT).move_to(
    np.array([CX - 2.35, 0.35, 0]))
A8, B8, C8, D8 = M.example_frame(origin=np.array([CX + 2.2, 0.55, 0]), scale=0.30)
mini = VGroup(
    Polygon(A8, B8, C8, D8), Line(A8, C8), Line(A8, B8), Line(B8, C8),
    M.locating_arc(A8, D8, 4.8 * 0.30, 26, M.CHALK_CYAN),
    M.locating_arc(C8, D8, 4.2 * 0.30, 26, M.CHALK_PINK),
)
names8 = M.quad_names((A8, B8, C8, D8), "ABCD", 14)
note8 = M.board_text("Diagonal → Triangle → Arcs → Join → Verify", 17,
                     M.CHALK_WHITE, "BOLD").move_to(np.array([CX, -2.55, 0]))
head8 = M.board_text("Diagonal First", 23, M.CHALK_AMBER, "BOLD").move_to(
    np.array([CX, 2.72, 0]))
for nm, m in (("cards", steps), ("mini", mini), ("names", names8),
              ("note", note8), ("heading", head8)):
    show(nm, m)
clash(steps, mini, "cards/mini")
clash(steps, names8, "cards/names")
clash(mini, head8, "mini/heading")
clash(names8, head8, "names/heading")
clash(mini, note8, "mini/note")

print("=== SCENE 9: practice + cards + clock + badge ===")
P9, Q9, R9, S9 = M.practice_frame()
fig9 = Polygon(P9, Q9, R9, S9)
names9 = M.quad_names((P9, Q9, R9, S9), "PQRS", 16)
cards9 = VGroup(
    M.measure_card(r"PQ=4", M.CHALK_CYAN, 15), M.measure_card(r"QR=3", M.CHALK_CYAN, 15),
    M.measure_card(r"RS=5", M.CHALK_CYAN, 15), M.measure_card(r"PS=4.5", M.CHALK_CYAN, 15),
    M.measure_card(r"PR=5.5", M.CHALK_YELLOW, 15),
).arrange(DOWN, buff=0.20).move_to(np.array([CX + 2.4, 0.55, 0]))
ask9 = M.board_text("Which triangle comes first?", 18, M.CHALK_WHITE, "BOLD"
                    ).move_to(np.array([CX - 1.0, -2.15, 0]))
pause9 = M.board_text("Pause and decide.", 18, M.CHALK_YELLOW, "BOLD").move_to(
    np.array([CX + 2.4, -1.9, 0]))
tag9 = M.board_text("Practice set — made for this video.", 15, M.CHALK_WHITE,
                    "BOLD").move_to(np.array([CX, 2.24, 0]))
head9 = M.board_text("YOUR TURN", 30, M.CHALK_PINK, "BOLD").move_to(
    np.array([CX, 2.62, 0]))
clock = VGroup(Circle(radius=0.9).move_to(np.array([CX - 4.0, 0.9, 0])))
for nm, m in (("figure", fig9), ("names", names9), ("cards", cards9),
              ("ask", ask9), ("pause", pause9), ("tag", tag9),
              ("heading", head9), ("clock", clock)):
    show(nm, m)
clash(fig9, cards9, "figure/cards")
clash(names9, cards9, "names/cards")
clash(cards9, pause9, "cards/pause")
clash(fig9, ask9, "figure/ask")
clash(clock, fig9, "clock/figure")
clash(clock, names9, "clock/names")
cat_p, cat_r = M.locating_arc(P9, S9, 4.5 * 0.40, 24, M.CHALK_CYAN), \
    M.locating_arc(R9, S9, 5.0 * 0.40, 24, M.CHALK_PINK)
show("reveal arcs", cat_p, cat_r)
badge9 = M.board_text("First triangle: PQR", 18, M.CHALK_GREEN, "BOLD").move_to(
    np.array([CX + 2.4, -1.75, 0]))
show("badge", badge9)
clash(badge9, cards9, "badge/cards")
clash(badge9, cat_p, "badge/arc_p")
clash(cards9, M.quad_names((P9, Q9, R9, S9), "PQRS", 17), "cards/names")

print("=== SCENE 10: recap ===")
A10, B10, C10, D10 = M.example_frame(origin=np.array([CX - 4.1, -1.15, 0]),
                                     scale=0.34)
fig10 = Polygon(A10, B10, C10, D10)
rows = VGroup(
    M.summary_row(1, "Diagonal + two sides:", r"\triangle ABC", M.CHALK_YELLOW),
    M.summary_row(2, "Other two sides as radii:", r"AD,\ DC", M.CHALK_CYAN),
    M.summary_row(3, "Their crossing gives the vertex:", r"D", M.CHALK_GREEN),
).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(
    np.array([CX + 1.8, 1.35, 0]))
final10 = M.board_text("Diagonal → Triangle → Arcs → Join", 19, M.CHALK_GREEN,
                       "BOLD").move_to(np.array([CX, -1.90, 0]))
take10 = M.board_text("Use the diagonal to make two triangles.", 17,
                      M.CHALK_WHITE, "BOLD").move_to(np.array([CX, -2.45, 0]))
names10 = M.quad_names((A10, B10, C10, D10), "ABCD", 16)
for nm, m in (("figure", fig10), ("names", names10), ("rows", rows),
              ("final", final10), ("take", take10)):
    show(nm, m)
clash(names10, rows, "names/rows")
clash(fig10, final10, "figure/final")
clash(rows, final10, "rows/final")
clash(final10, take10, "final/take")

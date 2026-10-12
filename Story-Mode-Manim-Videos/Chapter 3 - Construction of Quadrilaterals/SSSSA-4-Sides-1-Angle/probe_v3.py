import numpy as np
from manim import *
import construct_quadrilateral_4sides_1angle as M

def bb(m):
    return (float(m.get_corner(DL)[0]), float(m.get_corner(UR)[0]),
            float(m.get_corner(DL)[1]), float(m.get_corner(UR)[1]))

def show(name, m):
    x0, x1, y0, y1 = bb(m)
    flag = "  <<OFF-BOARD" if (x0 < -4.39 or x1 > 5.23 or y0 < -2.99 or y1 > 3.26) else ""
    print(f"  {name:16s} x[{x0:+.2f}..{x1:+.2f}] y[{y0:+.2f}..{y1:+.2f}]{flag}")

def clash(a, b, nm):
    ax0, ax1, ay0, ay1 = bb(a); bx0, bx1, by0, by1 = bb(b)
    ox = min(ax1, bx1) - max(ax0, bx0); oy = min(ay1, by1) - max(ay0, by0)
    print(f"  {'!! OVERLAP' if (ox > 0.02 and oy > 0.02) else 'ok  '} {nm}: {ox:+.2f} x {oy:+.2f}")

P, Q, R, S = M.example_frame()
print("=== SCENE 3 (final) ===")
cen = np.array([P, Q, R, S], dtype=float).mean(axis=0)
lab_qr = M.side_label(Q, R, cen, "QR = 5.2", M.CHALK_YELLOW, 16, 0.20)
sas = M.measure_card(r"\text{Side}+\text{Angle}+\text{Side}", M.CHALK_GREEN, 16).move_to(np.array([3.6, -0.55, 0]))
sas2 = M.measure_card(r"\text{S.A.S}", M.CHALK_GREEN, 16).move_to(np.array([3.6, -1.15, 0]))
note = M.board_text("Three measurements fix this triangle.", 17, M.CHALK_WHITE, "BOLD").move_to(np.array([0.5, -2.3, 0]))
for nm, m in (("lab_qr", lab_qr), ("sas", sas), ("sas2", sas2), ("note", note), ("figure", M.Polygon(P, Q, R, S))):
    show(nm, m)
clash(sas, lab_qr, "sas/lab_qr"); clash(sas2, lab_qr, "sas2/lab_qr"); clash(sas, note, "sas/note")
clash(sas2, note, "sas2/note"); clash(lab_qr, M.Polygon(P, Q, R, S), "lab_qr/figure")

print("=== SCENE 1 (final) ===")
cards = VGroup(
    M.measure_card(r"PQ=4.5", M.CHALK_CYAN), M.measure_card(r"QR=5.2", M.CHALK_CYAN),
    M.measure_card(r"RS=5.5", M.CHALK_CYAN), M.measure_card(r"PS=4", M.CHALK_CYAN),
    M.measure_card(r"\angle RQP=120^\circ", M.CHALK_YELLOW),
).arrange(DOWN, buff=0.24).move_to(np.array([0.5, 0.55, 0]))
strip = M.board_text("4 Sides + 1 Angle", 21, M.CHALK_GREEN, "BOLD").move_to(np.array([0.5, -1.79, 0]))
box = SurroundingRectangle(strip, color=M.CHALK_GREEN, buff=0.16, corner_radius=0.1, stroke_width=2.6)
ask = M.board_text("Where should we start?", 19, M.CHALK_WHITE, "BOLD").move_to(np.array([0.5, -2.54, 0]))
head = M.board_text("Four Sides and One Angle", 24, M.CHALK_AMBER, "BOLD").move_to(np.array([0.5, 2.72, 0]))
for nm, m in (("heading", head), ("cards", cards), ("box", box), ("ask", ask)):
    show(nm, m)
clash(head, cards, "heading/cards"); clash(cards, box, "cards/box"); clash(box, ask, "box/ask")

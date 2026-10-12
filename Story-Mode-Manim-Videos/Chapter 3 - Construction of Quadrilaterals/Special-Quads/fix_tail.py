"""Fix the tail beats and append them to _specialq_beats.py.

The challenge's parallelogram must actually have a 65 degree angle (the BELT
frame is 45/135), the angle mark there was passed a stray expression, and the
scene-4 strip needs to clear the D letter.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
TAIL = HERE / "_specialq_beats_tail.py"
BEATS = HERE / "_specialq_beats.py"

t = TAIL.read_text(encoding="utf-8")
n0 = len(t)

# --- scene 4: the strip clear of the D letter ------------------------------
old = """            strip = board_text("BISECT + PERPENDICULAR", 16, CHALK_GREEN, "BOLD"
                               ).move_to(np.array([BOARD_CX, -2.55, 0]))"""
new = """            strip = board_text("BISECT + PERPENDICULAR", 16, CHALK_GREEN, "BOLD"
                               ).move_to(np.array([BOARD_CX + 0.45, -2.50, 0]))"""
assert old in t
t = t.replace(old, new, 1)

# --- challenge A: a real 65 degree parallelogram, lettered A B C D ---------
old = """            # challenge A: a parallelogram with angle A = 65
            pa = parallelogram_frame(centre=np.array([BOARD_CX - 3.05, 0.30, 0]),
                                     scale=0.34)
            A1, E1, L1, T1 = pa["quad"]
            qa = Polygon(A1, E1, L1, T1, color=CHALK_WHITE, stroke_width=2.2,
                         fill_color=CHALK_CYAN, fill_opacity=0.10)
            na = self.vertex_letters(
                (A1, E1, L1, T1), ((-0.10, -0.26), (0.10, -0.28), (0.26, 0.08),
                                   (-0.26, 0.08)), letters="BELT")
            ang_a = angle_mark(T1, E1, B if False else A1, radius=0.30,
                               color=CHALK_YELLOW, label="45°")
            hand_a = board_text("A parallelogram: ∠A = 65°".replace("∠", ""),
                                15, CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX - 3.05, -1.35, 0]))"""
new = """            # challenge A: a parallelogram whose angle A really is 65 degrees
            ca_c = np.array([BOARD_CX - 3.05, 0.30, 0])
            a4 = np.array([0.0, 0.0, 0.0])
            b4 = ray_point(a4, 0.0, 4.0)
            d4 = ray_point(a4, 65.0, 4.5)
            c4 = b4 + (d4 - a4)
            A1, B1, C1, D1 = to_board((a4, b4, c4, d4), ca_c, 0.34)
            qa = Polygon(A1, B1, C1, D1, color=CHALK_WHITE, stroke_width=2.2,
                         fill_color=CHALK_CYAN, fill_opacity=0.10)
            na = self.vertex_letters(
                (A1, B1, C1, D1), ((-0.24, -0.24), (0.10, -0.26), (0.24, 0.10),
                                   (-0.24, 0.10)))
            ang_a = angle_mark(A1, B1, D1, radius=0.30, color=CHALK_YELLOW,
                               label="65°")
            hand_a = board_text("A parallelogram with angle A = 65°", 15,
                                CHALK_YELLOW, "BOLD").move_to(
                np.array([BOARD_CX - 3.05, -1.35, 0]))"""
assert old in t
t = t.replace(old, new, 1)

# --- the pause sits below everything --------------------------------------
old = """            pause = board_text("Pause and work them out.", 17, CHALK_YELLOW,
                               "BOLD").move_to(
                np.array([BOARD_CX, -2.62, 0]))"""
new = """            pause = board_text("Pause and work them out.", 17, CHALK_YELLOW,
                               "BOLD").move_to(
                np.array([BOARD_CX, -2.70, 0]))"""
assert old in t
t = t.replace(old, new, 1)

old = """                              "pts_a": (A1, E1, L1, T1), "pts_b": (A2, B2, C2, D2)}"""
new = """                              "pts_a": (A1, B1, C1, D1), "pts_b": (A2, B2, C2, D2)}"""
assert old in t
t = t.replace(old, new, 1)

# --- the reveal's four angle marks ----------------------------------------
old = """            ch = self.challenge
            A1, E1, L1, T1 = ch["pts_a"]
            A2, B2, C2, D2 = ch["pts_b"]
            O2 = mid(A2, C2)"""
new = """            ch = self.challenge
            A1, B1, C1, D1 = ch["pts_a"]
            A2, B2, C2, D2 = ch["pts_b"]
            O2 = mid(A2, C2)"""
assert old in t
t = t.replace(old, new, 1)

old = """            angs = VGroup(
                angle_mark(A1, E1, T1, radius=0.28, color=CHALK_YELLOW,
                           label="65°"),
                angle_mark(E1, A1, L1, radius=0.28, color=CHALK_GREEN,
                           label="115°"),
                angle_mark(L1, E1, T1, radius=0.28, color=CHALK_GREEN,
                           label="115°"),
                angle_mark(T1, L1, A1, radius=0.28, color=CHALK_YELLOW,
                           label="65°"))"""
new = """            angs = VGroup(
                angle_mark(A1, B1, D1, radius=0.26, color=CHALK_YELLOW,
                           label="65°"),
                angle_mark(B1, A1, C1, radius=0.26, color=CHALK_GREEN,
                           label="115°"),
                angle_mark(C1, B1, D1, radius=0.26, color=CHALK_GREEN,
                           label="115°"),
                angle_mark(D1, A1, C1, radius=0.26, color=CHALK_YELLOW,
                           label="65°"))"""
assert old in t
t = t.replace(old, new, 1)

TAIL.write_text(t, encoding="utf-8")
print(f"tail patched: {n0} -> {len(t)} chars")

base = BEATS.read_text(encoding="utf-8").rstrip("\n")
BEATS.write_text(base + "\n" + t.lstrip("\n"), encoding="utf-8")
TAIL.unlink()
print(f"appended; beats now {len(BEATS.read_text(encoding='utf-8').splitlines())} lines")

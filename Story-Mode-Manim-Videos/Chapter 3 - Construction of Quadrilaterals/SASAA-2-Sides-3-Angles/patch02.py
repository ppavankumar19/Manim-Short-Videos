"""Second patch of _sasaa_beats.py: the remaining audit hits."""
from pathlib import Path

B = Path(__file__).resolve().parent / "_sasaa_beats.py"
F = Path(__file__).resolve().parent / "_sasaa_fragment.py"

s = B.read_text(encoding="utf-8")
n0 = len(s)

# --- R's letter further out of the 120-degree construction -------------------
s = s.replace("(0.40, -0.28)", "(0.50, -0.40)")

# --- the 4 cm label goes below P Q, clear of the P R diagonal ---------------
s = s.replace("""            lab_pq = board_text("4 cm", 15, CHALK_YELLOW, "BOLD").move_to(
                P + np.array([0.55, 0.26, 0]))""",
              """            lab_pq = board_text("4 cm", 15, CHALK_YELLOW, "BOLD").move_to(
                (P + Q) / 2 + DOWN * 0.32)""")

# --- the 75 degree label sits outside the angle, clear of P R --------------
s = s.replace("""            ang_p = board_text("75°", 15, CHALK_YELLOW, "BOLD").move_to(
                np.array(P, dtype=float) + 1.30 * unit(
                    (d["pq_deg"] + d["ps_deg"]) / 2.0))""",
              """            ang_p = board_text("75°", 15, CHALK_YELLOW, "BOLD").move_to(
                np.array(P, dtype=float) + 1.15 * unit(
                    d["ps_deg"] + 35.0))""")

# --- the challenge line clear of the B letter ------------------------------
s = s.replace("""                np.array([BOARD_CX + 0.75, -2.50, 0]))""",
              """                np.array([BOARD_CX + 0.60, -2.50, 0]))""")

# --- scene 2's note on two lines, clear of the "use later" panel -----------
s = s.replace("""            note = board_text("The included angle tells us the first triangle.",
                              17, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))""",
              """            note = board_text("The included angle\\ntells us the first "
                              "triangle.", 16, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.52, 0]))""")

# --- the inset's labels off the bisector and the rays ---------------------
s = s.replace("""        l60 = board_text("60°", 13, CHALK_CYAN, "BOLD").move_to(
            v + np.array([0.78, 0.20, 0]))
        l90 = board_text("90°", 13, CHALK_AMBER, "BOLD").move_to(
            v + np.array([0.10, 0.78, 0]))
        l75 = board_text("75°", 13, CHALK_GREEN, "BOLD").move_to(
            v + np.array([1.09, 0.78, 0]))
        eq = board_text("75° = (60° + 90°)/2", 13, CHALK_GREEN, "BOLD"
                        ).move_to(v + np.array([0.98, -0.34, 0]))""",
              """        l60 = board_text("60°", 13, CHALK_CYAN, "BOLD").move_to(
            v + np.array([0.80, 0.14, 0]))
        l90 = board_text("90°", 13, CHALK_AMBER, "BOLD").move_to(
            v + np.array([-0.05, 0.98, 0]))
        l75 = board_text("75°", 13, CHALK_GREEN, "BOLD").move_to(
            v + np.array([1.05, 0.86, 0]))
        eq = board_text("75° = (60° + 90°)/2", 13, CHALK_GREEN, "BOLD"
                        ).move_to(v + np.array([1.02, -0.36, 0]))""")

B.write_text(s, encoding="utf-8")
print(f"beats: {n0} -> {len(s)} chars")

f = F.read_text(encoding="utf-8")
f2 = f.replace("PRACTICE_CENTRE = np.array([BOARD_CX - 1.9, -0.30, 0.0])",
               "PRACTICE_CENTRE = np.array([BOARD_CX - 1.9, -0.15, 0.0])")
F.write_text(f2, encoding="utf-8")
print(f"fragment centre changed: {f != f2}")

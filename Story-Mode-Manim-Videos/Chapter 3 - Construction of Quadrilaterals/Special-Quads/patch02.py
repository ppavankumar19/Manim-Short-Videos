"""Patch 02: the comparison columns, the duplicated 65 degree mark, and the
recap's closing order (which was costing 1.1 s of overrun)."""
from pathlib import Path

P = Path(__file__).resolve().parent / "_specialq_beats.py"
s = P.read_text(encoding="utf-8")
n0 = len(s)
reps = []

# ---------------------------------------------------------------- scene 7 ---
reps.append((
    """            keys = (("Opposite angles equal", "Consecutive angles add to 180°"),
                    ("Diagonals bisect each other", "at right angles"),
                    ("Equal diagonals,",
                     "perpendicular bisectors of each other"))
            effects = ("→ the missing angles",
                       "→ every vertex from the diagonals",
                       "→ the rhombus construction, one condition more")
            given = (("2 sides + 1 angle",), ("2 diagonals",), ("1 diagonal",))

            heads, figs, keys_txt, eff_txt, giv_txt = (VGroup() for _ in range(5))
            for i, (x, name, col) in enumerate(zip(cols, names, colors)):
                heads.add(board_text(name, 15, col, "BOLD").move_to(
                    np.array([x, 2.24, 0])))
                giv_txt.add(board_text(given[i][0], 13, CHALK_WHITE, "BOLD"
                                       ).move_to(np.array([x, 1.90, 0])))
                if i == 0:
                    pts = parallelogram_frame(centre=np.array([x, 1.05, 0]),
                                              scale=0.22)["quad"]
                elif i == 1:
                    pts = rhombus_frame(centre=np.array([x, 1.05, 0]),
                                        scale=0.26)["quad"]
                else:
                    pts = square_frame(centre=np.array([x, 1.05, 0]),
                                       scale=0.30)["quad"]
                figs.add(Polygon(*pts, color=CHALK_WHITE, stroke_width=2.2,
                                 fill_color=col, fill_opacity=0.12))
                keys_txt.add(VGroup(*[board_text(line, 13, col, "BOLD")
                                      for line in keys[i]]).arrange(
                    DOWN, buff=0.08).move_to(np.array([x, -0.32, 0])))
                eff_txt.add(board_text(effects[i], 13, CHALK_WHITE, "BOLD"
                                       ).move_to(np.array([x, -0.95, 0])))""",
    """            keys = (("Opposite angles equal", "consecutive angles",
                     "sum to 180°"),
                    ("Diagonals bisect", "each other at 90°", ""),
                    ("Equal diagonals,", "perpendicular", "bisectors", ""))
            effects = (("→ the missing angles",),
                       ("→ every vertex from", "the diagonals"),
                       ("→ one more condition",))

            heads, figs, keys_txt, eff_txt = (VGroup() for _ in range(4))
            for i, (x, name, col) in enumerate(zip(cols, names, colors)):
                heads.add(board_text(name, 15, col, "BOLD").move_to(
                    np.array([x, 2.20, 0])))
                if i == 0:
                    pts = parallelogram_frame(centre=np.array([x, 1.00, 0]),
                                              scale=0.22)["quad"]
                elif i == 1:
                    pts = rhombus_frame(centre=np.array([x, 1.00, 0]),
                                        scale=0.26)["quad"]
                else:
                    pts = square_frame(centre=np.array([x, 1.00, 0]),
                                       scale=0.30)["quad"]
                figs.add(Polygon(*pts, color=CHALK_WHITE, stroke_width=2.2,
                                 fill_color=col, fill_opacity=0.12))
                keys_txt.add(VGroup(*[board_text(line, 13, col, "BOLD")
                                      for line in keys[i] if line]).arrange(
                    DOWN, buff=0.08).move_to(np.array([x, -0.30, 0])))
                eff_txt.add(VGroup(*[board_text(line, 13, CHALK_WHITE, "BOLD")
                                     for line in effects[i]]).arrange(
                    DOWN, buff=0.06).move_to(np.array([x, -1.10, 0])))"""))
reps.append((
    """            self.play(FadeIn(heads), FadeIn(giv_txt), run_time=0.7)""",
    """            self.play(FadeIn(heads), run_time=0.7)"""))

# ---------------------------------------------------------------- scene 9 ---
reps.append((
    """            self.play(FadeOut(ch["pause"]), run_time=0.4)
            self.wait(leftover(tracker, "b0"))
            self.add_sound(self.sfx["pop"], gain=-13)""",
    """            self.play(FadeOut(ch["pause"]), FadeOut(ch["ang_a"]),
                      run_time=0.4)
            self.wait(leftover(tracker, "b0"))
            self.add_sound(self.sfx["pop"], gain=-13)"""))

# --------------------------------------------------------------- scene 10 ---
reps.append((
    """            self.play(FadeIn(prop_txt[1]), FadeIn(prop_txt[2]),
                      run_time=min(leftover(tracker, "b2"), 0.9))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeIn(chain, shift=UP * 0.08), Create(chain_box),
                      FadeIn(final, shift=UP * 0.08), run_time=min(
                          leftover(tracker, "b3"), 0.8))
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["success"], gain=-11)""",
    """            self.play(FadeIn(prop_txt[1]), FadeIn(prop_txt[2]),
                      run_time=min(leftover(tracker, "b2"), 0.7))
            self.add_sound(self.sfx["ding"], gain=-13)
            self.play(FadeIn(chain, shift=UP * 0.08), Create(chain_box),
                      FadeIn(final, shift=UP * 0.08), run_time=min(
                          leftover(tracker, "b2"), 0.7))
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["success"], gain=-11)"""))
reps.append((
    """            self.play(FadeOut(summary), FadeOut(heading), run_time=min(
                leftover(tracker, "b4") * 0.5, 0.8))
            self.play(FadeIn(thanks, shift=UP * 0.1), run_time=0.6)
            self.add_sound(self.sfx["success"], gain=-11)
            self.wait(leftover(tracker, "b4"))
            self.play(FadeIn(thanks2, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b4"))""",
    """            self.play(FadeOut(summary), FadeOut(heading), run_time=0.4)
            self.play(FadeIn(thanks, shift=UP * 0.1), run_time=0.5)
            self.add_sound(self.sfx["success"], gain=-11)
            self.wait(leftover(tracker, "b3"))
            self.play(FadeIn(thanks2, shift=UP * 0.1), run_time=0.5)
            self.wait(leftover(tracker, "b4"))"""))

for old, new in reps:
    assert old in s, f"not found: {old[:70]!r}"
    s = s.replace(old, new, 1)

P.write_text(s, encoding="utf-8")
print(f"beats: {n0} -> {len(s)} chars, {len(reps)} replacements")

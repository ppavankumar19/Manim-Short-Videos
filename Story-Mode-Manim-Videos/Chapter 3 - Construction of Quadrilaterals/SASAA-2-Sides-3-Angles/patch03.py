"""Third patch: give scene 7's construction its own narration windows.

The 120 degree construction (base arc, two chord steps, the ray) was crammed
into the single window that ended at the old `b1`, so every sweep ran at the
0.4 s floor and the whole instrument flashed past.  The narration now marks the
construction, the ray and the crossing separately, and the beat paces them.
"""
from pathlib import Path

B = Path(__file__).resolve().parent / "_sasaa_beats.py"
s = B.read_text(encoding="utf-8")
n0 = len(s)

# scene 4: only the letters that exist yet
s = s.replace("""                (P, Q, R), ((-0.28, -0.10), (0.12, -0.30), (0.50, -0.40)))
            pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=4.2)""",
              """                (P, Q), ((-0.28, -0.10), (0.12, -0.30)))
            pq = Line(P, Q, color=CHALK_YELLOW, stroke_width=4.2)""")

# scene 7: construction -> ray -> crossing -> agreement, one window each
old = """            # one long sweep of the base arc, then the two chord steps
            self.compass_on(R, mid, r_len, 60, CHALK_PINK,
                            hinge_dir=(1.0, 0.6, 0.0), leg_ratio=0.52)
            self.sweep_compass(tracker, "b1", 60, put_down=False, reserve=3.6)
            self.play(FadeIn(dots[0], scale=0.5), run_time=0.3)
            first = self.tool
            self.compass_on(a1, a2, r_len, 12, CHALK_PINK,
                            hinge_dir=(-1.0, -0.4, 0.0), leg_ratio=0.6)
            self.sweep_compass(tracker, "b1", 12, reserve=2.5)
            self.play(FadeIn(dots[1], scale=0.5), FadeIn(chord1), run_time=0.35)
            self.compass_on(a2, a3, r_len, 12, CHALK_PINK,
                            hinge_dir=(1.0, 0.4, 0.0), leg_ratio=0.6)
            self.sweep_compass(tracker, "b1", 12, reserve=1.4)
            self.play(FadeIn(dots[2], scale=0.5), FadeIn(chord2),
                      FadeOut(first), run_time=0.4)
            self.add_sound(self.sfx["whoosh"], gain=-14)

            self.play(Create(ray_r), run_time=min(leftover(tracker, "b1"), 1.0))
            self.play(FadeIn(card_r), run_time=0.3)
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b1"))

            self.play(FadeIn(s_dot, scale=0.5), FadeIn(s_name),
                      Indicate(s_dot, color=CHALK_YELLOW, scale_factor=2.1),
                      run_time=min(leftover(tracker, "b2"), 1.0))
            self.play(FadeIn(note, shift=UP * 0.08), run_time=0.5)
            self.wait(leftover(tracker, "b2"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeOut(VGroup(dots, chord1, chord2)),
                      FadeIn(agree, shift=UP * 0.1),
                      Circumscribe(s_dot, color=CHALK_GREEN, stroke_width=2.6),
                      run_time=min(leftover(tracker, "b3"), 1.0))
            self.wait(leftover(tracker, "b3"))"""
new = """            # the base arc, then the same opening stepped round twice: the
            # chord of each 60 degree step is exactly the opening, so the arcs
            # of the steps really do land on the base arc
            self.compass_on(R, mid, r_len, 60, CHALK_PINK,
                            hinge_dir=(1.0, 0.6, 0.0), leg_ratio=0.52)
            self.play(self.sweep.animate.set_value(120), run_time=min(
                leftover(tracker, "b1") * 0.42, 1.7))
            self.play(FadeIn(dots[0], scale=0.5), run_time=0.25)
            first = self.tool
            self.compass_on(a1, a2, r_len, 12, CHALK_PINK,
                            hinge_dir=(-1.0, -0.4, 0.0), leg_ratio=0.6)
            self.play(self.sweep.animate.set_value(24), run_time=0.75)
            self.play(FadeIn(dots[1], scale=0.5), FadeIn(chord1), run_time=0.3)
            self.compass_on(a2, a3, r_len, 12, CHALK_PINK,
                            hinge_dir=(1.0, 0.4, 0.0), leg_ratio=0.6)
            self.play(self.sweep.animate.set_value(24), run_time=0.75)
            self.play(FadeIn(dots[2], scale=0.5), FadeIn(chord2),
                      FadeOut(first), run_time=0.4)
            self.add_sound(self.sfx["whoosh"], gain=-14)
            self.wait(leftover(tracker, "b1"))

            # the ray through the 120 degree mark
            self.play(FadeIn(card_r), run_time=0.3)
            self.play(Create(ray_r), run_time=min(leftover(tracker, "b2"), 0.9))
            self.add_sound(self.sfx["click"], gain=-15)
            self.wait(leftover(tracker, "b2"))

            self.play(FadeIn(s_dot, scale=0.5), FadeIn(s_name),
                      Indicate(s_dot, color=CHALK_YELLOW, scale_factor=2.1),
                      run_time=min(leftover(tracker, "b3"), 1.0))
            self.play(FadeIn(note, shift=UP * 0.08), run_time=0.5)
            self.wait(leftover(tracker, "b3"))
            self.add_sound(self.sfx["ding"], gain=-13)

            self.play(FadeOut(VGroup(dots, chord1, chord2)),
                      FadeIn(agree, shift=UP * 0.1),
                      Circumscribe(s_dot, color=CHALK_GREEN, stroke_width=2.6),
                      run_time=min(leftover(tracker, "b4"), 1.0))
            self.wait(leftover(tracker, "b4"))"""
assert old in s
s = s.replace(old, new)

B.write_text(s, encoding="utf-8")
print(f"beats: {n0} -> {len(s)} chars")

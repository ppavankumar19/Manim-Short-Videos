"""Patch 05: match the on-screen wording to the storyboard document.

The build already covered the storyboard's content; these are the places where
my on-screen strings differed from the ones the document specifies:

  scene 2   add the boxed "S.A.S" beside "Side - Angle - Side"
  scene 4   heading -> "STEP 2 - Build Triangle PQR by S.A.S"
  scene 5   note    -> "Triangle P Q R is fixed by S.A.S"
  scene 6   note    -> "S could be somewhere on this ray"
  scene 7   line    -> "Two directions agree at one point."
  scene 9   question -> "Which three measurements should you use first?"
            add "What is their included angle?", "built by S.A.S" and
            "S.A.S builds. Two angles locate."
  scene 10  the two closing sentences from the document's final frame, plus a
            boxed "S.A.S.A.A"
"""
from pathlib import Path

P = Path(__file__).resolve().parent / "_sasaa_beats.py"
s = P.read_text(encoding="utf-8")
n0 = len(s)

reps = []

# --- scene 2: the acronym beside the words ---------------------------------
reps.append((
    """            sas = board_text("Side – Angle – Side", 18, CHALK_GREEN, "BOLD"
                             ).move_to(np.array([3.05, -0.40, 0]))""",
    """            sas = board_text("Side – Angle – Side", 18, CHALK_GREEN, "BOLD"
                             ).move_to(np.array([3.05, -0.32, 0]))
            sas_short = board_text("S.A.S", 16, CHALK_GREEN, "BOLD").move_to(
                np.array([3.05, -0.72, 0]))"""))
reps.append((
    """            self.play(FadeIn(tri), FadeIn(sas),
                      Circumscribe(tri, color=CHALK_CYAN, stroke_width=2.6,
                                   time_width=0.6),
                      run_time=min(leftover(tracker, "b3"), 1.0))""",
    """            self.play(FadeIn(tri), FadeIn(sas), FadeIn(sas_short),
                      Circumscribe(tri, color=CHALK_CYAN, stroke_width=2.6,
                                   time_width=0.6),
                      run_time=min(leftover(tracker, "b3"), 1.0))"""))

# --- scene 4: heading names the method -------------------------------------
reps.append(('board_text("STEP 2 — Build Triangle PQR", 21,',
             'board_text("STEP 2 — Build Triangle PQR by S.A.S", 21,'))

# --- scene 5 / 6: the notes in the document's words ------------------------
reps.append(('self.column_note("Triangle P Q R is fixed\\nby side, angle, "\n'
             '                                    "side.", -0.75)',
             'self.column_note("Triangle P Q R is fixed\\nby S.A.S.", -0.75)'))
reps.append(('self.column_note("S lies somewhere on\\nthis ray: 75° from "\n'
             '                                    "P Q.", -0.30)',
             'self.column_note("S could be somewhere\\non this ray.", -0.30)'))

# --- scene 7: the document's sentence --------------------------------------
reps.append(('agree = board_text("Two directions agree at S.", 17, CHALK_GREEN,',
             'agree = board_text("Two directions agree at one point.", 17, '
             'CHALK_GREEN,'))

# --- scene 9: question, prompt, badges -------------------------------------
reps.append(("""            ask = board_text("Which three measurements come first?", 17,
                             CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX + 0.60, -2.50, 0]))""",
             """            ask = board_text("Which three measurements should you use "
                             "first?", 16, CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX + 0.80, -2.62, 0]))
            prompt = board_text("What is their included angle?", 16,
                                CHALK_YELLOW, "BOLD").move_to(
                np.array([3.05, -1.35, 0]))"""))
reps.append(("""            self.play(FadeIn(ask, shift=RIGHT * 0.12), run_time=0.5)
            self.wait(leftover(tracker, "b2"))""",
             """            self.play(FadeIn(ask, shift=RIGHT * 0.12),
                      FadeIn(prompt, shift=RIGHT * 0.12), run_time=0.5)
            self.wait(leftover(tracker, "b2"))"""))
reps.append(("""            self.challenge = {"rough": rough, "names": names, "cards": cards,
                              "ask": ask, "pause": pause, "ab": ab, "bc": bc,
                              "points": (A, B, C, D), "data": d}""",
             """            self.challenge = {"rough": rough, "names": names, "cards": cards,
                              "ask": ask, "pause": pause, "ab": ab, "bc": bc,
                              "prompt": prompt, "points": (A, B, C, D),
                              "data": d}"""))
reps.append(("""            self.play(FadeOut(ch["pause"]), FadeOut(ch["ask"]), run_time=0.4)""",
             """            self.play(FadeOut(ch["pause"]), FadeOut(ch["ask"]),
                      FadeOut(ch["prompt"]), run_time=0.4)"""))
reps.append(("""            badge = board_text("First triangle: A B C", 17, CHALK_GREEN, "BOLD"
                               ).move_to(np.array([3.05, -1.55, 0]))""",
             """            badge = board_text("First triangle: A B C", 17, CHALK_GREEN,
                               "BOLD").move_to(np.array([3.05, -1.55, 0]))
            badge2 = board_text("built by S.A.S", 15, CHALK_GREEN, "BOLD"
                                ).move_to(np.array([3.05, -1.93, 0]))"""))
reps.append(("""            self.play(FadeIn(badge, shift=UP * 0.1), run_time=0.5)""",
             """            self.play(FadeIn(badge, shift=UP * 0.1), FadeIn(badge2),
                      run_time=0.5)"""))
reps.append(("""            quad = Polygon(A, B, C, D, color=CHALK_CYAN, stroke_width=2.4,
                           fill_color=CHALK_CYAN, fill_opacity=0.12)
            self.play(FadeIn(d_dot, scale=0.5), FadeIn(quad),""",
             """            quad = Polygon(A, B, C, D, color=CHALK_CYAN, stroke_width=2.4,
                           fill_color=CHALK_CYAN, fill_opacity=0.12)
            built = board_text("S.A.S builds. Two angles locate.", 16,
                               CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -2.55, 0]))
            self.play(FadeIn(d_dot, scale=0.5), FadeIn(quad),
                      FadeIn(built, shift=UP * 0.08),"""))

# --- scene 10: the closing sentences and the acronym ------------------------
reps.append(("""            final = board_text("Side–Angle–Side builds; Angle–Angle locates.",
                               17, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -1.90, 0]))
            take = board_text("S.A.S.A.A — 2 sides and 3 angles.", 16,
                              CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.45, 0]))""",
             """            final = board_text("Side–Angle–Side builds the triangle.", 17,
                               CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX, -1.90, 0]))
            take = board_text("Angle–Angle locates the fourth vertex.", 16,
                              CHALK_WHITE, "BOLD").move_to(
                np.array([BOARD_CX, -2.45, 0]))
            acr = board_text("S.A.S.A.A", 18, CHALK_GREEN, "BOLD").move_to(
                np.array([BOARD_CX - 3.05, -1.90, 0]))
            acr_box = SurroundingRectangle(acr, color=CHALK_GREEN, buff=0.14,
                                          corner_radius=0.1, stroke_width=2.4)"""))
reps.append(("""            self.play(FadeIn(take),
                      Circumscribe(quad, color=CHALK_AMBER, stroke_width=3,
                                   time_width=0.5),
                      run_time=min(leftover(tracker, "b3"), 1.2))""",
             """            self.play(FadeIn(take), FadeIn(acr), Create(acr_box),
                      Circumscribe(quad, color=CHALK_AMBER, stroke_width=3,
                                   time_width=0.5),
                      run_time=min(leftover(tracker, "b3"), 1.2))"""))
reps.append(("""            summary = VGroup(quad, names, tri, pq, qr, ray_p, ray_r, ang_q,
                             s_dot, rows, final, take)""",
             """            summary = VGroup(quad, names, tri, pq, qr, ray_p, ray_r, ang_q,
                             s_dot, rows, final, take, acr, acr_box)"""))

for old, new in reps:
    assert old in s, f"not found: {old[:60]!r}"
    s = s.replace(old, new, 1)

P.write_text(s, encoding="utf-8")
print(f"beats: {n0} -> {len(s)} chars, {len(reps)} replacements")

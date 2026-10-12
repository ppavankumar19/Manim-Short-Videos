"""ACT I - Why tokenisation exists (Scenes 01-05).

    Scene 01  The AI That Cannot Read          text enters a model that wants numbers
    Scene 02  Computers Need a Dictionary       tokens map to integer IDs
    Scene 03  The Word Dictionary Problem       whole-word vocabularies break
    Scene 04  The Character-Level Alternative   coverage bought with length
    Scene 05  The Subword Breakthrough          reusable pieces

Provenance is labelled on screen throughout: `book` chips mark values printed
in Chapter 2, `illus` chips mark examples invented to explain.  Scene 03 is
the one place where the teaching example (the play family) is NOT the book's
example (the apology family), so it shows both and says which is which.

Render:
    python -m manim render --resolution 640,360 --fps 30 \
        --media_dir D:\\m3 act1_scenes.py Chapter2Act1
"""
from __future__ import annotations

import numpy as np

from manim import (
    DOWN, DR, LEFT, ORIGIN, RIGHT, UP, UL, UR,
    AddTextLetterByLetter, AnimationGroup, Circumscribe, Create, Flash,
    FadeIn, FadeOut, GrowArrow, Indicate, LaggedStart, Line, Polygon,
    Rectangle, ReplacementTransform, RoundedRectangle, Succession, Text,
    TransformFromCopy, VGroup, Wiggle, Write, there_and_back,
)

from components import (
    brace_meter, callout, id_array, id_chip, raw_text_track, token_block,
    token_row, unknown_token, vocabulary_table,
)
from data_traces import (
    BOOK, CHAPTER, HOOK_PROMPT, PLAY_FAMILY, TOY_LOOKUP, WORD_VS_SUBWORD,
)
from theme import (
    AMBER, GREEN, INK, MUTED, NEON_BLUE, NEON_CYAN, NEON_MAGENTA,
    NEON_VIOLET, PANEL, PANEL_EDGE, ROSE, SAFE_B, SAFE_L, SAFE_R, SAFE_T,
    TITLE_Y, WHITE, LLMScene, fit, mono, panel, pg, rt, source_chip,
    title_bar, token_color,
)
from three_d import (
    apply_depth, grid_floor, input_grid_floor, token_tunnel, vault_wall,
)

# ============================================================== narration ===
NARRATION = {
    # -- Scene 01 --------------------------------------------------------
    "s01a": (
        "Here is a question for a language model. What is the capital of "
        "India? You type it, you send it, and an answer comes back. It looks "
        "as though the model is reading your words directly."
        "<bookmark mark='send'/>"
    ),
    "s01b": (
        "It is not. Before the model sees anything at all, that sentence is "
        "taken apart and turned into something else entirely. Watch what the "
        "model actually receives.<bookmark mark='reveal'/> A list of integers."
        "<bookmark mark='ints'/>"
    ),
    "s01c": (
        "One number for every piece of the text. No letters, no words, no "
        "punctuation, just positions in a table.<bookmark mark='table'/>"
    ),
    "s01d": (
        "So how does text become numbers? That is what this episode is about."
        "<bookmark mark='question'/>"
    ),
    # -- Scene 02 --------------------------------------------------------
    "s02a": (
        "Start from the simplest idea. A tokenizer needs a dictionary. On the "
        "left, readable text. On the right, a list of integers. The "
        "dictionary is the bridge between the two worlds."
        "<bookmark mark='bridge'/>"
    ),
    "s02b": (
        "Take a short greeting: Hello, with an exclamation mark. The tokenizer "
        "does not keep it whole. It cuts it into two pieces. Hello, and the "
        "exclamation mark on its own. Each piece is called a token."
        "<bookmark mark='tokens'/>"
    ),
    "s02c": (
        "Every token then looks itself up in the dictionary. Hello is entry "
        "forty two.<bookmark mark='first'/> The exclamation mark is entry "
        "ninety one.<bookmark mark='second'/> Those two integers are what the "
        "model receives.<bookmark mark='array'/> I invented these particular "
        "numbers to keep the picture clean, but the mechanism is exactly what "
        "every real tokenizer does.<bookmark mark='caveat'/>"
    ),
    # -- Scene 03 --------------------------------------------------------
    "s03a": (
        "For a long time, the dictionary held whole words. Every word the "
        "system knew got its own drawer in the cabinet. Play. Player. "
        "Playing. Played. Four drawers, four entries, for one idea."
        "<bookmark mark='drawers'/>"
    ),
    "s03b": (
        "That works beautifully until somebody uses a word that was never in "
        "the training data. Playfulness. There is no drawer for it. The "
        "searchlight sweeps the cabinet and finds nothing."
        "<bookmark mark='search'/> So the word is thrown away, and replaced "
        "by a single marker: unknown token.<bookmark mark='unknown'/> The "
        "word is gone. The model cannot tell you what it was."
    ),
    "s03c": (
        "The book makes exactly this point with a different family: apology, "
        "apologize, apologetic, apologist.<bookmark mark='book'/> Four whole "
        "words, all built on one stem, and the vocabulary pays for every one "
        "of them separately. That is a lot of storage for very little "
        "difference.<bookmark mark='cost'/>"
    ),
    "s03d": (
        "But look closely at those drawers, and a pattern appears. The same "
        "letters keep coming back. Play. Play. Play.<bookmark mark='pattern'/> "
        "If those letters could be shared, one entry would do the work of "
        "many.<bookmark mark='share'/>"
    ),
    # -- Scene 04 --------------------------------------------------------
    "s04a": (
        "So here is one escape route. Forget words entirely. Treat every "
        "single character as a token. Playful shatters into seven separate "
        "pieces.<bookmark mark='shatter'/> P. L. A. Y. F. U. L."
        "<bookmark mark='letters'/>"
    ),
    "s04b": (
        "Now nothing is ever unknown again, because every word in every "
        "language is built from characters the system already has."
        "<bookmark mark='coverage'/> But look at the price. The word play, "
        "which used to be one token, is now four.<bookmark mark='price'/>"
    ),
    "s04c": (
        "And that price is paid in the model's context. Subword tokens average "
        "about three characters each, so a context of one thousand and twenty "
        "four tokens holds roughly three times as much text as characters "
        "would.<bookmark mark='context'/>"
    ),
    "s04d": (
        "Character tokenization is not wrong. It is a different trade: "
        "complete coverage, bought with much longer sequences for the model "
        "to work through.<bookmark mark='trade'/>"
    ),
    # -- Scene 05 --------------------------------------------------------
    "s05a": (
        "So the machine takes the middle path. Keep whole words when they are "
        "common. Break the rare ones into reusable pieces. Play, player, "
        "playing. All three share the same opening.<bookmark mark='share'/>"
    ),
    "s05b": (
        "That shared opening collapses into a single block: play."
        "<bookmark mark='collapse'/> Now the endings can be stored "
        "separately. Er. And ing.<bookmark mark='pieces'/> Three words, built "
        "from three pieces."
    ),
    "s05c": (
        "And a word the vocabulary has never seen? Playful. It needs no new "
        "entry at all. Play is already there.<bookmark mark='have'/> Ful is "
        "already there. The word is simply assembled.<bookmark mark='assembled'/>"
    ),
    "s05d": (
        "That is what the book calls subword tokenization.<bookmark "
        "mark='named'/> It is why the pieces for apology, apologize, "
        "apologetic and apologist can be shared, instead of stored whole. "
        "Whole words when useful.<bookmark mark='whole'/> Smaller pieces when "
        "needed.<bookmark mark='smaller'/>"
    ),
}


class Chapter2Act1(LLMScene):

    narration = NARRATION
    """Scenes 01-05: the problem, the dictionary, and the subword idea."""

    module_stem = "act1_scenes"

    def construct(self) -> None:
        self.setup_episode()
        self.add_backdrop()

        self.s01_the_ai_that_cannot_read()
        self.s02_computers_need_a_dictionary()
        self.s03_the_word_dictionary_problem()
        self.s04_the_character_alternative()
        self.s05_the_subword_breakthrough()

        self.write_real_srt()

    # =================================================================
    # Scene 01 - The AI That Cannot Read
    # =================================================================
    def s01_the_ai_that_cannot_read(self) -> None:
        # -- 1a: the prompt is typed and sent -----------------------------
        with self.beat("s01a") as tracker:
            title = self.scene_title("01  -  The AI That Cannot Read")
            self.play(FadeIn(title), run_time=0.5)

            term = panel(7.6, 1.05, color=NEON_CYAN)
            term.move_to(np.array([0.0, 1.38, 0.0]))
            caret = mono(">", 26, GREEN).move_to(
                np.array([term.get_left()[0] + 0.34, 1.38, 0.0]))
            typed = mono(HOOK_PROMPT["text"], 25, INK)
            typed.next_to(caret, RIGHT, buff=0.20)
            typed.set_x(term.get_center()[0] + 0.18)
            terminal = VGroup(term, caret, typed)

            self.play(FadeIn(term), FadeIn(caret), run_time=0.5)
            self.play(AddTextLetterByLetter(typed),
                      run_time=rt(tracker.time_until_bookmark("send") * 0.85))
            self.keep.add(terminal)

            # The machine: a wide container whose *interior* is where the
            # numeric input will appear.  Its label lives inside it, so the
            # status panel above can never collide with it.
            machine = RoundedRectangle(
                corner_radius=0.20, width=9.2, height=1.55,
                fill_color="#061A31", fill_opacity=0.94,
                stroke_color=NEON_BLUE, stroke_width=2.4)
            machine.move_to(np.array([0.0, -1.00, 0.0]))
            label = pg("LANGUAGE MODEL", 18, NEON_BLUE, "BOLD")
            label.move_to(np.array([0.0, -0.44, 0.0]))
            gate = Line(
                np.array([machine.get_left()[0], machine.get_top()[1], 0.0]),
                np.array([machine.get_left()[0], machine.get_bottom()[1], 0.0]),
                stroke_color=NEON_CYAN, stroke_width=3.0)
            self.play(FadeIn(VGroup(machine, label, gate)), run_time=0.6)

            flight = typed.copy()
            self.add(flight)
            self.play(
                flight.animate.move_to(machine.get_center()).set_opacity(0.0),
                run_time=rt(tracker.get_remaining_duration() * 0.45),
            )
            self.remove(flight)
            self.play(machine.animate.shift(LEFT * 0.18),
                      rate_func=there_and_back, run_time=0.5)
            self.hold(VGroup(machine, label, gate))
            self.dissolve(tracker)

        # -- 1b: the model refuses text -----------------------------------
        with self.beat("s01b") as tracker:
            warn = VGroup(
                panel(5.6, 0.66, color=ROSE),
                mono("EXPECTED: NUMERIC INPUT", 24, ROSE, "BOLD"),
            )
            warn[1].move_to(warn[0].get_center())
            warn.move_to(np.array([0.0, 0.52, 0.0]))
            self.play(FadeIn(warn, scale=0.9),
                      run_time=rt(tracker.time_until_bookmark("reveal")))
            self.play(Flash(warn[0], color=ROSE, flash_radius=1.2),
                      run_time=0.4)
            self.keep.add(warn)

            # what the model actually wants: numbered positions, appearing
            # *inside* the machine, below its label
            slots = VGroup(*[
                VGroup(
                    panel(0.80, 0.58, color=NEON_CYAN, fill_opacity=0.10),
                    mono(f"{i}", 19, MUTED),
                ).move_to(np.array([-4.00 + i * 0.89, -1.32, 0.0]))
                for i in range(10)
            ])
            for s in slots:
                s[1].move_to(s[0].get_center())
                s.set_z_index(1)
            self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.12) for s in slots],
                                  lag_ratio=0.10),
                      run_time=rt(tracker.get_remaining_duration() * 0.85))
            self.keep.add(slots)
            self.dissolve(tracker)

        # -- 1c: through the boundary, into the model's real input ---------
        self.release_stage(0.6)
        with self.beat("s01c") as tracker:
            # A shallow look-down with the grid pulled well inside the panel:
            # at phi=40 the corner cells project outwards, so the field has to
            # be smaller and shallower than it looks in world coordinates.
            self.view_3d(phi=38, theta=-70, zoom=0.84, animate=False)
            # No floor grid here: its far edge projected just past the rim,
            # and the numbered positions already carry the depth cue.  Two
            # rows of six fill the panel without any cell leaving it.
            grid = input_grid_floor(rows=2, cols=6, pitch_x=1.34, pitch_z=1.02,
                                    y=-0.78)
            budget = tracker.time_until_bookmark("table")
            self.play(FadeIn(grid), run_time=rt(budget * 0.80))
            self.keep.add(grid)

            # the prompt is chrome, not world geometry: keep it legible, and
            # clear of the title rule at TITLE_Y - 0.30
            prompt_box = panel(6.2, 0.85, color=NEON_CYAN, fill_opacity=0.18)
            prompt_box.move_to(np.array([0.0, 1.58, 0.0]))
            ghost = mono(HOOK_PROMPT["text"], 24, INK).move_to(
                prompt_box.get_center())
            ghost_panel = self.hud(VGroup(prompt_box, ghost))
            self.play(FadeIn(ghost_panel), run_time=0.5)
            self.hold(ghost_panel)

        # the grid has made its point; clear it so the question has the panel
        self.dissolve(tracker)
        self.view_2d(animate=True, run_time=0.8)

        with self.beat("s01d") as tracker:
            q = pg("How does text become numbers?", 30, AMBER, "BOLD")
            self.hud(q)
            q.move_to(np.array([0.0, -0.10, 0.0]))
            self.play(Write(q),
                      run_time=rt(tracker.time_until_bookmark("question") * 0.8))
            chip = self.hud(source_chip("illus"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(q, chip)

        self.release_stage(0.4)
        self.clear_stage(run_time=0.4)

    # =================================================================
    # Scene 02 - Computers Need a Dictionary
    # =================================================================
    def s02_computers_need_a_dictionary(self) -> None:
        with self.beat("s02a") as tracker:
            title = self.scene_title("02  -  Computers Need a Dictionary")
            self.play(FadeIn(title), run_time=0.5)

            left = VGroup(
                pg("readable text", 17, MUTED).move_to(
                    np.array([-4.3, 1.55, 0.0])),
                mono(TOY_LOOKUP["word"], 32, INK).move_to(
                    np.array([-4.3, 0.95, 0.0])),
            )
            right = VGroup(
                pg("integers", 17, MUTED).move_to(np.array([4.3, 1.55, 0.0])),
                mono("[ ? , ? ]", 30, NEON_CYAN).move_to(
                    np.array([4.3, 0.95, 0.0])),
            )
            bridge = panel(3.5, 1.2, color=AMBER)
            bridge.move_to(np.array([0.0, 0.95, 0.0]))
            bl = pg("dictionary", 20, AMBER, "BOLD").move_to(bridge.get_center())
            self.play(FadeIn(left), FadeIn(right), run_time=0.8)
            self.play(FadeIn(VGroup(bridge, bl), scale=0.9),
                      run_time=rt(tracker.get_remaining_duration() - 0.3))
            self.keep.add(left, right, VGroup(bridge, bl))

        self.dissolve(tracker)

        with self.beat("s02b") as tracker:
            word = mono(TOY_LOOKUP["word"], 34, INK)
            word.move_to(np.array([0.0, 1.5, 0.0]))
            self.play(FadeIn(word, shift=DOWN * 0.12), run_time=0.7)

            pieces = token_row([t for t, _ in TOY_LOOKUP["pieces"]], size=30)
            pieces.move_to(np.array([0.0, 0.35, 0.0]))
            cut = Line(
                np.array([0.0, 1.05, 0.0]), np.array([0.0, 1.85, 0.0]),
                stroke_color=ROSE, stroke_width=2.4, stroke_opacity=0.9)
            self.play(Create(cut),
                      run_time=rt(tracker.time_until_bookmark("tokens") * 0.5))
            self.play(
                AnimationGroup(
                    FadeOut(word), FadeOut(cut),
                    LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in pieces],
                                lag_ratio=0.25),
                ),
                run_time=rt(tracker.get_remaining_duration() - 0.3),
            )
            self.keep.add(pieces)

        self.dissolve(tracker)

        with self.beat("s02c") as tracker:
            table = vocabulary_table(
                [(t, i) for t, i in TOY_LOOKUP["pieces"]], width=7.0, size=24)
            table.move_to(np.array([0.0, 0.55, 0.0]))
            self.play(FadeIn(table), run_time=0.8)
            self.keep.add(table)

            def rowbox(i, color):
                return RoundedRectangle(
                    corner_radius=0.08,
                    width=table.rows[i].width + 0.5,
                    height=table.rows[i].height + 0.16,
                    stroke_color=color, stroke_width=2.2, fill_opacity=0.0,
                ).move_to(table.rows[i].get_center())

            box1 = rowbox(0, GREEN)
            self.play(Create(box1),
                      run_time=rt(tracker.time_until_bookmark("first") * 0.6))
            box2 = rowbox(1, GREEN)
            self.play(Create(box2),
                      run_time=rt(tracker.time_until_bookmark("second")
                                  - tracker.time_until_bookmark("first")))

            arr = id_array([i for _, i in TOY_LOOKUP["pieces"]], size=26)
            arr.move_to(np.array([0.0, -1.02, 0.0]))
            self.play(TransformFromCopy(table.rows, arr),
                      run_time=rt(tracker.get_remaining_duration() * 0.6))
            cav = callout("these IDs are invented for the example - the "
                          "mechanism is not", color=AMBER, size=15)
            cav.move_to(np.array([0.0, -1.55, 0.0]))
            self.play(FadeIn(cav), run_time=0.5)
            chip = self.hud(source_chip("illus"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(box1, box2, arr, cav, chip)

        self.clear_stage(run_time=0.4)

    # =================================================================
    # Scene 03 - The Word Dictionary Problem
    # =================================================================
    def s03_the_word_dictionary_problem(self) -> None:
        with self.beat("s03a") as tracker:
            title = self.scene_title("03  -  The Word Dictionary Problem")
            self.play(FadeIn(title), run_time=0.5)

            drawers = VGroup()
            for i, w in enumerate(["play", "player", "playing", "played"]):
                box = RoundedRectangle(
                    corner_radius=0.08, width=2.0, height=0.72,
                    fill_color=PANEL, fill_opacity=0.85,
                    stroke_color=NEON_BLUE, stroke_width=1.8)
                lab = mono(w, 24, INK).move_to(box.get_center())
                handle = Line(
                    np.array([-0.30, box.get_center()[1] - 0.36, 0.0]),
                    np.array([0.30, box.get_center()[1] - 0.36, 0.0]),
                    stroke_color=NEON_BLUE, stroke_width=2.0)
                drawers.add(VGroup(box, lab, handle))
            drawers.arrange(RIGHT, buff=0.28).move_to(
                np.array([0.0, 0.95, 0.0]))
            self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.2) for d in drawers],
                                  lag_ratio=0.22),
                      run_time=rt(tracker.time_until_bookmark("drawers") * 0.8))
            for d in drawers:
                self.play(Indicate(d[1], color=AMBER, scale_factor=1.12),
                          run_time=0.22)
            self.keep.add(drawers)

        self.dissolve(tracker)

        with self.beat("s03b") as tracker:
            ask = mono("playfulness", 34, AMBER)
            ask.move_to(np.array([0.0, 1.35, 0.0]))
            self.play(FadeIn(ask, shift=DOWN * 0.12), run_time=0.7)

            search = Rectangle(
                width=0.9, height=1.0, stroke_color=NEON_CYAN, stroke_width=1.6,
                fill_color=NEON_CYAN, fill_opacity=0.10)
            search.move_to(np.array([-4.4, 0.95, 0.0]))
            self.play(FadeIn(search), run_time=0.4)
            self.play(
                search.animate.move_to(np.array([4.4, 0.95, 0.0])),
                run_time=rt(tracker.time_until_bookmark("search") - 0.4),
            )
            miss = pg("no match", 20, ROSE, "BOLD").next_to(
                np.array([4.4, 0.95, 0.0]), UP, buff=0.58)
            self.play(FadeIn(miss), run_time=0.3)
            self.remove(search)
            self.play(FadeOut(miss), run_time=0.3)
            search.move_to(np.array([-4.4, 0.95, 0.0]))

            unk = unknown_token("[UNK]", size=28)
            unk.move_to(np.array([0.0, -0.45, 0.0]))
            self.play(
                FadeOut(search),
                TransformFromCopy(ask, unk),
                run_time=rt(tracker.time_until_bookmark("unknown") - 0.3),
            )
            lost = callout("the word itself is unrecoverable", color=ROSE,
                           size=16).move_to(np.array([0.0, -1.30, 0.0]))
            self.play(FadeIn(lost), run_time=0.6)
            chip = self.hud(source_chip("illus"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(VGroup(unk, lost, chip))

        self.clear_stage(run_time=0.4)

        # the book-grounded pass (audit fix F3)
        with self.beat("s03c") as tracker:
            fam = VGroup(*[mono(w, 26, INK) for w in WORD_VS_SUBWORD["word_family"]])
            fam.arrange(RIGHT, buff=0.5).move_to(np.array([0.0, 0.95, 0.0]))
            self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.14) for f in fam],
                                  lag_ratio=0.2),
                      run_time=rt(tracker.time_until_bookmark("book") * 0.8))
            stem = mono(WORD_VS_SUBWORD["stem"], 26, GREEN)
            stem.next_to(fam, DOWN, buff=0.55)
            braces = VGroup(*[
                Line(np.array([f.get_center()[0], 0.72, 0.0]),
                     np.array([f.get_center()[0], 0.48, 0.0]),
                     stroke_color=GREEN, stroke_width=1.6, stroke_opacity=0.8)
                for f in fam
            ])
            rule = Line(
                np.array([fam.get_left()[0], 0.48, 0.0]),
                np.array([fam.get_right()[0], 0.48, 0.0]),
                stroke_color=GREEN, stroke_width=1.6)
            self.play(Create(braces), Create(rule), FadeIn(stem), run_time=0.8)
            cost = callout("four whole entries for one stem - expensive",
                           color=ROSE, size=16).move_to(
                np.array([0.0, -1.35, 0.0]))
            self.play(FadeIn(cost),
                      run_time=rt(tracker.time_until_bookmark("cost") * 0.7))
            chip = self.hud(source_chip("book"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(VGroup(fam, braces, rule, stem, cost, chip))

        self.dissolve(tracker)

        with self.beat("s03d") as tracker:
            reuse = token_row(["play", "play", "play"], size=30,
                              start_index=0)
            reuse.move_to(np.array([0.0, 0.60, 0.0]))
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.16) for b in reuse],
                                  lag_ratio=0.3),
                      run_time=rt(tracker.time_until_bookmark("pattern") * 0.7))
            box = RoundedRectangle(
                corner_radius=0.10, width=reuse.width + 0.5,
                height=reuse.height + 0.4,
                stroke_color=AMBER, stroke_width=2.4, fill_opacity=0.0)
            box.move_to(reuse.get_center())
            self.play(Create(box), run_time=0.5)
            payoff = pg("one shared piece", 24, AMBER, "BOLD").move_to(
                np.array([0.0, -0.75, 0.0]))
            self.play(Write(payoff),
                      run_time=rt(tracker.time_until_bookmark("share") * 0.8))
            self.keep.add(VGroup(reuse, box, payoff))

        self.clear_stage(run_time=0.4)

    # =================================================================
    # Scene 04 - The Character-Level Alternative
    # =================================================================
    def s04_the_character_alternative(self) -> None:
        with self.beat("s04a") as tracker:
            title = self.scene_title("04  -  The Character-Level Alternative")
            self.play(FadeIn(title), run_time=0.5)

            word = mono("playful", 40, INK).move_to(np.array([0.0, 1.25, 0.0]))
            chars = list("playful")
            cards = VGroup(*[
                token_block(c, i, size=30) for i, c in enumerate(chars)
            ])
            cards.arrange(RIGHT, buff=0.16).move_to(
                np.array([0.0, 0.10, 0.0]))

            self.play(FadeIn(word), run_time=0.6)
            self.play(
                AnimationGroup(
                    FadeOut(word),
                    LaggedStart(*[TransformFromCopy(word, c) for c in cards],
                                lag_ratio=0.12),
                ),
                run_time=rt(tracker.time_until_bookmark("shatter") * 0.7),
            )
            self.play(LaggedStart(*[
                Indicate(c, color=WHITE, scale_factor=1.10) for c in cards
            ], lag_ratio=0.18),
                      run_time=rt(tracker.get_remaining_duration() * 0.7))
            self.keep.add(cards)

        self.dissolve(tracker)

        with self.beat("s04b") as tracker:
            good = callout("nothing is ever unknown again", color=GREEN, size=18)
            good.move_to(np.array([0.0, 1.62, 0.0]))
            self.play(FadeIn(good),
                      run_time=rt(tracker.time_until_bookmark("coverage") * 0.7))

            one = token_block("play", 0, size=28).move_to(
                np.array([-3.2, 0.30, 0.0]))
            cost_panel = panel(4.4, 1.45, color=ROSE).move_to(
                np.array([2.7, 0.35, 0.0]))
            cost_txt = VGroup(
                pg("the same word", 17, MUTED),
                pg("as 4 tokens", 22, ROSE, "BOLD"),
            ).arrange(DOWN, buff=0.14).move_to(cost_panel.get_center())
            four = token_row(list("play"), size=26, start_index=1)
            four.arrange(RIGHT, buff=0.10).move_to(
                np.array([2.7, -0.72, 0.0])).scale(0.78)

            self.play(FadeIn(one), run_time=0.5)
            bar1 = brace_meter(one, "1 token", direction=DOWN, color=GREEN)
            self.play(FadeIn(bar1), run_time=0.4)
            self.play(FadeIn(VGroup(cost_panel, cost_txt)), FadeIn(four),
                      run_time=rt(tracker.time_until_bookmark("price") * 0.7))
            bar2 = brace_meter(four, "4 tokens", direction=DOWN, color=ROSE)
            self.play(FadeIn(bar2), run_time=0.5)
            self.keep.add(VGroup(good, one, bar1, cost_panel, cost_txt,
                                 four, bar2))

        self.dissolve(tracker)

        with self.beat("s04c") as tracker:
            meter = panel(7.4, 1.5, color=NEON_VIOLET).move_to(
                np.array([0.0, 0.75, 0.0]))
            head = pg("model context", 18, MUTED).next_to(meter, UP, buff=0.12)
            seq = VGroup(*[
                Rectangle(width=0.30, height=0.72, fill_color=GREEN,
                          fill_opacity=0.75, stroke_width=0)
                for _ in range(22)
            ]).arrange(RIGHT, buff=0.045).move_to(meter.get_center())
            self.play(FadeIn(VGroup(meter, head, seq)), run_time=0.7)
            note = pg("3 characters per token on average", 20, AMBER, "BOLD")
            note.move_to(np.array([0.0, -0.45, 0.0]))
            self.play(Write(note),
                      run_time=rt(tracker.time_until_bookmark("context") * 0.7))
            out = callout("so roughly 3x more text fits in the same context",
                          color=GREEN, size=18).move_to(
                np.array([0.0, -1.35, 0.0]))
            self.play(FadeIn(out),
                      run_time=rt(tracker.get_remaining_duration() * 0.7))
            chip = self.hud(source_chip("book"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(VGroup(meter, head, seq, note, out, chip))

        self.dissolve(tracker)

        with self.beat("s04d") as tracker:
            trade = VGroup(
                callout("complete coverage", color=GREEN, size=22),
                pg("bought with", 18, MUTED),
                callout("much longer sequences", color=ROSE, size=22),
            ).arrange(DOWN, buff=0.34).move_to(np.array([0.0, 0.55, 0.0]))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.14) for t in trade],
                                  lag_ratio=0.35),
                      run_time=rt(tracker.time_until_bookmark("trade") * 0.8))
            self.keep.add(trade)

        self.clear_stage(run_time=0.4)

    # =================================================================
    # Scene 05 - The Subword Breakthrough
    # =================================================================
    def s05_the_subword_breakthrough(self) -> None:
        with self.beat("s05a") as tracker:
            title = self.scene_title("05  -  The Subword Breakthrough")
            self.play(FadeIn(title), run_time=0.5)

            rows = VGroup()
            for word, _ in PLAY_FAMILY["words"]:
                rows.add(mono(word, 30, INK))
            rows.arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to(
                np.array([-1.6, 0.75, 0.0]))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows],
                                  lag_ratio=0.25),
                      run_time=rt(tracker.time_until_bookmark("share") * 0.7))
            # the shared opening glows in all three at once
            self.play(LaggedStart(*[
                Indicate(r, color=AMBER, scale_factor=1.06) for r in rows
            ], lag_ratio=0.1),
                      run_time=rt(tracker.get_remaining_duration() * 0.7))
            self.keep.add(rows)

        self.dissolve(tracker)

        with self.beat("s05b") as tracker:
            stem = token_block("play", 0, size=32)
            stem.move_to(np.array([-3.4, 0.90, 0.0]))
            self.play(FadeIn(stem, shift=DOWN * 0.18),
                      run_time=rt(tracker.time_until_bookmark("collapse") * 0.6))

            suf_er = token_block("er", 1, size=30)
            suf_ing = token_block("ing", 2, size=30)
            suffixes = VGroup(suf_er, suf_ing).arrange(RIGHT, buff=0.45)
            suffixes.move_to(np.array([1.6, 0.90, 0.0]))
            self.play(LaggedStart(FadeIn(suf_er, shift=DOWN * 0.18),
                                  FadeIn(suf_ing, shift=DOWN * 0.18),
                                  lag_ratio=0.4),
                      run_time=rt(tracker.time_until_bookmark("pieces") * 0.7))

            # assemble the three words from the shared pieces
            built = VGroup()
            for word, parts in PLAY_FAMILY["words"]:
                b = token_row(parts, size=20, start_index=0)
                built.add(VGroup(b, pg(word, 16, MUTED).next_to(
                    b, RIGHT, buff=0.26)))
            built.arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to(
                np.array([0.0, -0.50, 0.0]))
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.12) for b in built],
                                  lag_ratio=0.3),
                      run_time=rt(tracker.get_remaining_duration() * 0.85))
            self.keep.add(VGroup(stem, suffixes, built))

        self.clear_stage(run_time=0.4)

        with self.beat("s05c") as tracker:
            unseen = mono(PLAY_FAMILY["unseen"][0], 36, AMBER).move_to(
                np.array([0.0, 1.35, 0.0]))
            self.play(FadeIn(unseen, shift=DOWN * 0.14), run_time=0.7)
            have = VGroup(
                token_block("play", 0, size=32),
                token_block("ful", 4, size=32),
            ).arrange(RIGHT, buff=0.45).move_to(np.array([0.0, 0.15, 0.0]))
            self.play(FadeIn(have[0], shift=UP * 0.16),
                      run_time=rt(tracker.time_until_bookmark("have") * 0.6))
            self.play(FadeIn(have[1], shift=UP * 0.16), run_time=0.5)
            self.play(
                Circumscribe(have, color=GREEN, buff=0.18),
                run_time=rt(tracker.time_until_bookmark("assembled") * 0.7),
            )
            done = pg("assembled, not stored", 22, GREEN, "BOLD").move_to(
                np.array([0.0, -0.95, 0.0]))
            self.play(Write(done),
                      run_time=rt(tracker.get_remaining_duration() * 0.7))
            chip = self.hud(source_chip("illus"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(VGroup(unseen, have, done, chip))

        self.dissolve(tracker)

        with self.beat("s05d") as tracker:
            back = VGroup(*[mono(w, 24, INK)
                            for w in WORD_VS_SUBWORD["word_family"]])
            back.arrange(RIGHT, buff=0.44).move_to(np.array([0.0, 1.15, 0.0]))
            self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.12) for f in back],
                                  lag_ratio=0.18),
                      run_time=rt(tracker.time_until_bookmark("named") * 0.6))
            pieces = token_row(
                [WORD_VS_SUBWORD["stem"]] + WORD_VS_SUBWORD["suffixes"],
                size=24, start_index=0)
            pieces.arrange(RIGHT, buff=0.16).move_to(
                np.array([0.0, 0.15, 0.0]))
            self.play(FadeIn(pieces, shift=UP * 0.14), run_time=0.8)

            line1 = pg("Whole words when useful.", 28, GREEN, "BOLD")
            line1.move_to(np.array([0.0, -0.85, 0.0]))
            line2 = pg("Smaller pieces when needed.", 28, AMBER, "BOLD")
            line2.move_to(np.array([0.0, -1.45, 0.0]))
            self.play(Write(line1),
                      run_time=rt(tracker.time_until_bookmark("smaller") * 0.7))
            self.play(Write(line2),
                      run_time=rt(tracker.get_remaining_duration() * 0.7))
            chip = self.hud(source_chip("book"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(VGroup(back, pieces, line1, line2, chip))

        self.clear_stage(run_time=0.5)

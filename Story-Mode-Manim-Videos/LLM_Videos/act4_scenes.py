"""ACT IV - Why the differences matter (Scenes 13-15).

    Scene 13  The Token Budget           granularity decides how much text fits
    Scene 14  The Tokenizer Laboratory   pause-and-predict recall
    Scene 15  Into the Embedding Matrix  recap and the bridge to embeddings

Audit addition G6 lands here: the book states (p.57) that a pretrained model
is tied to the tokenizer it was trained with, which is the real reason this
whole episode matters.  Scene 15 closes on it.

Render:
    python -m manim render --resolution 640,360 --fps 30 \
        --media_dir D:\\m3 act4_scenes.py Chapter2Act4
"""
from __future__ import annotations

import numpy as np

from manim import (
    DOWN, LEFT, ORIGIN, RIGHT, UP,
    Circumscribe, Create, FadeIn, FadeOut, GrowArrow, GrowFromEdge, Indicate, LaggedStart,
    Line, Rectangle, RoundedRectangle, Text, TransformFromCopy, VGroup, Write,
)

from components import (
    book_sample_line, callout, context_slot_meter, embedding_matrix, id_array,
    token_block, token_row,
)
from data_traces import CONTEXT_DEMO, PHI3, TOKENIZER_LOCK
from theme import (
    AMBER, GREEN, INK, MUTED, NEON_BLUE, NEON_CYAN, NEON_MAGENTA,
    NEON_VIOLET, PANEL, PANEL_EDGE, ROSE, SAFE_B, SAFE_L, SAFE_R, SAFE_T, SAFE_W,
    WHITE, LLMScene, fit, mono, panel, pg, rt, source_chip, title_bar,
)
from three_d import (
    apply_depth, embedding_slab, grid_floor, vector_beam,
)

# ============================================================== narration ===
NARRATION = {
    # -- Scene 13 --------------------------------------------------------
    "s13a": (
        "Why does any of this matter in practice? Because a language model "
        "has a fixed number of positions it can look at.<bookmark "
        "mark='fixed'/> That limit is counted in tokens, not in words, and "
        "not in characters."
    ),
    "s13b": (
        "Picture a context of twelve positions.<bookmark mark='twelve'/> A "
        "finely split version of a sentence fills eleven of them."
        "<bookmark mark='fine'/> Only one position is left."
    ),
    "s13c": (
        "The same sentence, tokenized with larger pieces, needs six."
        "<bookmark mark='coarse'/> Same text, twice the room to spare. These "
        "particular counts are made up to make the point, but the effect is "
        "real.<bookmark mark='illus'/>"
    ),
    "s13d": (
        "So the tokenizer decides how much text fits, and how much work the "
        "model does to read it.<bookmark mark='matters'/> One caution though. "
        "A lower token count does not by itself make a model better. "
        "Architecture, training, and the context limit all matter just as "
        "much.<bookmark mark='caution'/>"
    ),
    # -- Scene 14 --------------------------------------------------------
    "s14a": (
        "Before we finish, a question.<bookmark mark='q'/> We ran the same "
        "string through four trained tokenizers, and they did not agree. "
        "Which statement does that support?<bookmark mark='pause'/>"
    ),
    "s14b": (
        "One: every tokenizer produces the same sequence. Two: every "
        "character becomes exactly one token. Three: different trained "
        "tokenizers can segment the same input differently, and can preserve "
        "or lose parts of it.<bookmark mark='reveal'/>"
    ),
    "s14c": (
        "The answer is three.<bookmark mark='answer'/> BERT lowercased the "
        "word before splitting it. GPT-2 recovered the emoji from raw bytes, "
        "and BERT could not. And GPT-4 used two pieces where FLAN-T5 used "
        "five. Same input, different outcomes, every time."
    ),
    # -- Scene 15 --------------------------------------------------------
    "s15a": (
        "So let us put the journey back together. Raw text is segmented into "
        "tokens.<bookmark mark='one'/> Each token is looked up in the "
        "vocabulary and becomes an integer ID.<bookmark mark='two'/> And that "
        "sequence of IDs is what the model receives.<bookmark mark='three'/>"
    ),
    "s15b": (
        "Those IDs now move inside the model, where a second table is "
        "waiting.<bookmark mark='inside'/> Each ID selects one row of that "
        "table, and the row is a learned vector. That vector is what the "
        "model actually computes with.<bookmark mark='vector'/>"
    ),
    "s15c": (
        "Keep the distinction clear. An ID is a discrete label. It has no "
        "size and no direction. The meaning lives in the vector it selects, "
        "not in the number itself.<bookmark mark='distinct'/>"
    ),
    "s15d": (
        "And one consequence that is easy to miss. A pretrained language "
        "model is tied to the tokenizer it was trained with. It cannot simply "
        "swap in a different one without being trained again."
        "<bookmark mark='lock'/> Which leaves our next question: how can a "
        "list of numbers represent meaning?<bookmark mark='next'/>"
    ),
}


class Chapter2Act4(LLMScene):
    """Scenes 13-15: the practical stake, the check, and the bridge."""

    narration = NARRATION

    module_stem = "act4_scenes"

    def construct(self) -> None:
        self.setup_episode()
        self.add_backdrop()

        self.s13_the_token_budget()
        self.s14_the_tokenizer_laboratory()
        self.s15_into_the_embedding_matrix()

        self.write_real_srt()

    # =================================================================
    # Scene 13 - The Token Budget
    # =================================================================
    def s13_the_token_budget(self) -> None:
        with self.beat("s13a") as tracker:
            self.scene_title("13  -  The Token Budget")
            self.play(FadeIn(self.chrome), run_time=0.5)

            frame = panel(6.4, 1.15, color=NEON_CYAN).move_to(
                np.array([0.0, 0.65, 0.0]))
            lbl = pg("context limit", 20, NEON_CYAN, "BOLD").move_to(
                np.array([0.0, 0.65, 0.0]))
            self.play(FadeIn(VGroup(frame, lbl)),
                      run_time=rt(tracker.time_until_bookmark("fixed") * 0.7))
            note = pg("counted in tokens, not words", 18, MUTED).move_to(
                np.array([0.0, -0.55, 0.0]))
            self.play(FadeIn(note),
                      run_time=rt(tracker.get_remaining_duration() * 0.7))
            self.keep.add(frame, lbl, note)

        self.dissolve(tracker)

        with self.beat("s13b") as tracker:
            meter = context_slot_meter(CONTEXT_DEMO["capacity"],
                                       CONTEXT_DEMO["fine_grained_used"],
                                       slot=0.52, used_color=ROSE)
            meter.move_to(np.array([0.0, 0.55, 0.0]))
            head = pg("finely split - 11 of 12 used", 19, ROSE, "BOLD")
            head.move_to(np.array([0.0, 1.55, 0.0]))
            self.play(FadeIn(head),
                      run_time=rt(tracker.time_until_bookmark("fine") * 0.6))
            self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in meter.cells],
                                  lag_ratio=0.06),
                      run_time=rt(tracker.get_remaining_duration() * 0.8))
            self.keep.add(VGroup(meter, head))

        self.dissolve(tracker)

        with self.beat("s13c") as tracker:
            head = pg("larger pieces - 6 of 12 used", 19, GREEN, "BOLD")
            head.move_to(np.array([0.0, 1.55, 0.0]))
            meter = context_slot_meter(CONTEXT_DEMO["capacity"],
                                       CONTEXT_DEMO["coarse_used"],
                                       slot=0.52, used_color=GREEN)
            meter.move_to(np.array([0.0, 0.55, 0.0]))
            self.play(FadeIn(head),
                      run_time=rt(tracker.time_until_bookmark("coarse") * 0.5))
            self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in meter.cells],
                                  lag_ratio=0.06),
                      run_time=rt(tracker.time_until_bookmark("illus") * 0.5))
            chip = callout("slot counts invented for this example",
                           color=AMBER, size=15).move_to(
                np.array([0.0, -1.35, 0.0]))
            self.play(FadeIn(chip),
                      run_time=rt(tracker.get_remaining_duration() * 0.6))
            chip2 = self.hud(source_chip("illus"))
            self.play(FadeIn(chip2), run_time=0.3)
            self.keep.add(VGroup(meter, head, chip, chip2))

        self.dissolve(tracker)

        with self.beat("s13d") as tracker:
            two = VGroup(
                callout("token granularity sets how much text fits", color=GREEN,
                        size=20),
                pg("and how much work the model does", 18, MUTED),
            ).arrange(DOWN, buff=0.16)
            caution = VGroup(
                callout("but a lower token count is not automatically better",
                        color=ROSE, size=20),
                pg("architecture, training and context limit matter too",
                   18, MUTED),
            ).arrange(DOWN, buff=0.16)
            VGroup(two, caution).arrange(DOWN, buff=0.50).move_to(
                np.array([0.0, 0.45, 0.0]))
            self.play(FadeIn(two),
                      run_time=rt(tracker.time_until_bookmark("caution") * 0.6))
            self.play(FadeIn(caution),
                      run_time=rt(tracker.get_remaining_duration() * 0.6))
            self.keep.add(two, caution)

        self.clear_stage(run_time=0.5)

    # =================================================================
    # Scene 14 - The Tokenizer Laboratory
    # =================================================================
    def s14_the_tokenizer_laboratory(self) -> None:
        statements = [
            "Every tokenizer produces the same sequence.",
            "Every character becomes exactly one token.",
            "Different trained tokenizers can segment and "
            "preserve the input differently.",
        ]

        with self.beat("s14a") as tracker:
            self.scene_title("14  -  The Tokenizer Laboratory")
            self.play(FadeIn(self.chrome), run_time=0.5)

            sample = book_sample_line(size=14)
            fit(sample, SAFE_W - 0.6)
            sample.move_to(np.array([0.0, 1.85, 0.0]))
            self.play(FadeIn(sample),
                      run_time=rt(tracker.time_until_bookmark("pause") * 0.6))
            self.hold(sample)

        # the narration itself carries the thinking gap; hold the frame for it
        with self.beat("s14b") as tracker:
            options = VGroup()
            for i, text in enumerate(statements, 1):
                body = pg(text, 21, INK)
                body.move_to(np.array([0.35, 1.15 - (i - 1) * 0.70, 0.0]))
                badge = pg(f"{i}", 22, NEON_CYAN, "BOLD").move_to(
                    np.array([SAFE_L + 0.55, 1.15 - (i - 1) * 0.70, 0.0]))
                options.add(VGroup(badge, body))
            options.scale(0.90)
            options.set_x(0.0)
            self.play(LaggedStart(*[FadeIn(o, shift=UP * 0.12) for o in options],
                                  lag_ratio=0.30),
                      run_time=rt(tracker.time_until_bookmark("reveal") * 0.8))
            self.keep.add(options)

        self.dissolve(tracker)

        with self.beat("s14c") as tracker:
            answer = 3
            options = VGroup()
            for i, text in enumerate(statements, 1):
                on = i == answer
                body = pg(text, 21, GREEN if on else MUTED,
                          "BOLD" if on else "NORMAL")
                body.move_to(np.array([0.35, 1.15 - (i - 1) * 0.70, 0.0]))
                badge = pg(f"{i}", 22, GREEN if on else MUTED, "BOLD")
                badge.move_to(np.array([SAFE_L + 0.55,
                                        1.15 - (i - 1) * 0.70, 0.0]))
                options.add(VGroup(badge, body))
            # Segoe Print is a wide handwriting face, so the option column is
            # scaled to the panel before it is shown
            options.scale(0.90)
            options.set_x(0.0)
            self.play(FadeIn(options),
                      run_time=rt(tracker.time_until_bookmark("answer") * 0.6))
            box = RoundedRectangle(
                corner_radius=0.10, width=SAFE_W - 0.3,
                height=options[2].height + 0.20,
                stroke_color=GREEN, stroke_width=2.4, fill_opacity=0.0)
            box.move_to(options[2].get_center())
            self.play(Create(box), run_time=0.6)

            # three brief replays of what the comparison actually showed
            replays = VGroup(
                VGroup(pg("BERT lowercased the word", 15, NEON_CYAN),
                       token_row(["capital", "##ization"], size=17)).arrange(
                    DOWN, buff=0.08),
                VGroup(pg("GPT-2 recovered the emoji from bytes", 15, GREEN),
                       mono("8582 236 113", 17, GREEN)).arrange(
                    DOWN, buff=0.08),
                VGroup(pg("GPT-4 used 2 pieces, FLAN-T5 used 5", 15, AMBER),
                       token_row(["CAPITAL", "IZATION"], size=17)).arrange(
                    DOWN, buff=0.08),
            ).arrange(RIGHT, buff=0.50)
            fit(replays, SAFE_W - 0.4)
            replays.move_to(np.array([0.0, -1.12, 0.0]))
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.10) for r in replays],
                                  lag_ratio=0.35),
                      run_time=rt(tracker.get_remaining_duration() * 0.8))
            chip = self.hud(source_chip("book"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(options, box, replays, chip)

        self.clear_stage(run_time=0.5)

    # =================================================================
    # Scene 15 - Into the Embedding Matrix
    # =================================================================
    def s15_into_the_embedding_matrix(self) -> None:
        with self.beat("s15a") as tracker:
            self.scene_title("15  -  Into the Embedding Matrix")
            self.play(FadeIn(self.chrome), run_time=0.5)

            steps = VGroup(
                VGroup(pg("1", 20, NEON_CYAN, "BOLD"),
                       pg("raw text is segmented into tokens", 20, INK)).arrange(
                    RIGHT, buff=0.30),
                VGroup(pg("2", 20, NEON_CYAN, "BOLD"),
                       pg("each token becomes an integer ID", 20, INK)).arrange(
                    RIGHT, buff=0.30),
                VGroup(pg("3", 20, NEON_CYAN, "BOLD"),
                       pg("the model receives that sequence", 20, INK)).arrange(
                    RIGHT, buff=0.30),
            ).arrange(DOWN, buff=0.42, aligned_edge=LEFT)
            fit(steps, SAFE_W - 0.7)
            steps.move_to(np.array([-1.4, 0.45, 0.0]))
            self.play(FadeIn(steps[0]),
                      run_time=rt(tracker.time_until_bookmark("two") * 0.5))
            self.play(FadeIn(steps[1]), run_time=0.6)
            self.play(FadeIn(steps[2]),
                      run_time=rt(tracker.get_remaining_duration() * 0.6))
            self.keep.add(steps)

        self.dissolve(tracker)

        with self.beat("s15b") as tracker:
            self.view_3d(phi=62, theta=-62, zoom=1.0, animate=False)
            slab = embedding_slab(rows=7, cols=8)
            slab.move_to(np.array([-1.9, 0.35, 0.0]))
            self.play(FadeIn(slab), run_time=0.9)
            self.hold(slab)

            beams = VGroup(vector_beam(seed=2, spread=2.6, z=0.15),
                           vector_beam(seed=5, spread=2.6, z=-0.55))
            beams.move_to(np.array([2.9, -0.45, 0.0]))
            self.play(GrowFromEdge(beams, edge=DOWN),
                      run_time=rt(tracker.time_until_bookmark("vector") * 0.7))

            labels = VGroup(
                pg("learned vectors, not IDs", 17, NEON_VIOLET, "BOLD"),
                mono("one row per token ID", 15, MUTED),
            ).arrange(DOWN, buff=0.08).move_to(np.array([2.9, 1.55, 0.0]))
            self.hud(labels)
            self.play(FadeIn(labels), run_time=0.5)
            self.keep.add(beams, labels)

        self.dissolve(tracker)
        self.release_stage(0.5)
        self.view_2d(animate=True, run_time=0.8)

        with self.beat("s15c") as tracker:
            ids = id_array([p for _, p in PHI3["pieces"]], size=26)
            ids.move_to(np.array([-3.1, 0.45, 0.0]))
            vs = embedding_matrix(rows=4, cols=5, cell=0.32,
                                  highlight=(1,), label="row selected")
            vs.move_to(np.array([1.9, 0.45, 0.0]))
            self.play(FadeIn(ids), run_time=0.5)
            self.play(FadeIn(vs),
                      run_time=rt(tracker.time_until_bookmark("distinct") * 0.6))
            note = callout("the integer is a label - the vector carries meaning",
                           color=AMBER, size=16).move_to(
                np.array([0.0, -1.35, 0.0]))
            self.play(FadeIn(note),
                      run_time=rt(tracker.get_remaining_duration() * 0.6))
            chip = self.hud(source_chip("book"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(ids, vs, note, chip)

        self.dissolve(tracker)

        with self.beat("s15d") as tracker:
            lock = callout(TOKENIZER_LOCK, color=NEON_MAGENTA, size=18)
            fit(lock, SAFE_W - 0.8)
            lock.move_to(np.array([0.0, 0.85, 0.0]))
            self.play(FadeIn(lock, shift=UP * 0.12),
                      run_time=rt(tracker.time_until_bookmark("lock") * 0.7))
            nxt = pg("How can a list of numbers represent meaning?",
                     26, AMBER, "BOLD")
            fit(nxt, SAFE_W - 0.8)
            nxt.move_to(np.array([0.0, -0.65, 0.0]))
            self.play(Write(nxt),
                      run_time=rt(tracker.time_until_bookmark("next") * 0.7))
            self.play(Indicate(nxt, color=WHITE, scale_factor=1.04),
                      run_time=rt(tracker.get_remaining_duration() * 0.6))
            chip = self.hud(source_chip("book"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(lock, nxt, chip)

        self.clear_stage(run_time=0.6)

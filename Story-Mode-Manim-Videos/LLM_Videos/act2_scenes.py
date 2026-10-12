"""ACT II - Inside the tokenizer (Scenes 06-08).

    Scene 06  Inside a Tokenizer           method, parameters, training data
    Scene 07  The Vocabulary Lookup        apologizing -> apolog + izing, with real IDs
    Scene 08  The Journey Back             IDs -> text, the bidirectional interface

Audit additions carried here:
  * G2 - the book publishes a vocabulary size for every tokenizer it
    discusses, so Scene 06 shows the real bar chart instead of talking about
    "capacity" in the abstract.
  * G5 - Scene 06 also shows the actual special-token inventories, which the
    storyboard mentioned only by name.
  * G8 - Phi-3 reuses the Llama 2 tokenizer and adds chat tokens (p.53).

Render:
    python -m manim render --resolution 640,360 --fps 30 \
        --media_dir D:\\m3 act2_scenes.py Chapter2Act2
"""
from __future__ import annotations

import numpy as np

from manim import (
    DOWN, LEFT, ORIGIN, RIGHT, UP,
    Circumscribe, Create, FadeIn, FadeOut, GrowArrow, Indicate, LaggedStart,
    Line, Rectangle, ReplacementTransform, RoundedRectangle, Text,
    TransformFromCopy, VGroup, Write,
)

from components import (
    callout, id_array, id_chip, token_block, token_row, vocab_bar_chart,
    vocabulary_table,
)
from data_traces import PHI3, PHI3_DECODE, SECTION_HOW, TOKENIZERS, VOCAB_SIZES
from theme import (
    AMBER, GREEN, INK, MUTED, NEON_BLUE, NEON_CYAN, NEON_MAGENTA,
    NEON_VIOLET, PANEL, PANEL_EDGE, ROSE, SAFE_B, SAFE_L, SAFE_R, SAFE_T,
    WHITE, LLMScene, fit, mono, panel, pg, rt, source_chip, space_marker,
    title_bar, token_color,
)
from three_d import (
    apply_depth, control_console, glow, grid_floor, vault_wall,
)

# ============================================================== narration ===
NARRATION = {
    # -- Scene 06 --------------------------------------------------------
    "s06a": (
        "Three decisions shape every tokenizer.<bookmark mark='three'/> "
        "First, the method: the algorithm that learns where to cut. Byte pair "
        "encoding for the GPT family. WordPiece for BERT. They aim at the "
        "same goal and reach it in different ways.<bookmark mark='method'/>"
    ),
    "s06b": (
        "Second, the parameters, and the most visible one is vocabulary size. "
        "These are the real numbers from the book.<bookmark mark='chart'/> "
        "BERT uncased holds thirty thousand five hundred and twenty two "
        "entries. GPT-2 holds fifty thousand two hundred and fifty seven. "
        "GPT-4 holds a little over one hundred thousand.<bookmark mark='gpt4'/>"
    ),
    "s06c": (
        "Third, the data the tokenizer is trained on. Same method, same size, "
        "but trained on code instead of prose, and you get a different "
        "vocabulary.<bookmark mark='data'/> So a method name alone can never "
        "tell you how a word will be split.<bookmark mark='conclude'/>"
    ),
    "s06d": (
        "Every tokenizer also reserves special tokens. Unknown, padding, "
        "beginning and end of text, separator, mask.<bookmark mark='specials'/> "
        "These are not words. They are instructions to the model."
        "<bookmark mark='instr'/>"
    ),
    # -- Scene 07 --------------------------------------------------------
    "s07a": (
        "Now the real thing. The book runs this next example on the Phi-3 "
        "tokenizer, which reuses the Llama 2 vocabulary and adds chat "
        "tokens.<bookmark mark='phi'/> Here is our word: apologizing."
        "<bookmark mark='word'/>"
    ),
    "s07b": (
        "The tokenizer does not keep it whole, and it does not fall back to "
        "letters. It returns two pieces: apolog, and izing."
        "<bookmark mark='split'/> Neither piece is a word on its own."
    ),
    "s07c": (
        "Each piece is an entry in the vocabulary, and each entry has an "
        "integer. Apolog is twenty seven thousand seven hundred and forty "
        "six.<bookmark mark='id1'/> Izing is five thousand two hundred and "
        "eighty one.<bookmark mark='id2'/> Those are the numbers the model "
        "receives.<bookmark mark='array'/>"
    ),
    "s07d": (
        "And there is a detail you cannot see in ordinary text. Izing carries "
        "a hidden character at its start, meaning: I am joined to what came "
        "before.<bookmark mark='hidden'/> A token without that marker is read "
        "as starting a new word. Whitespace is part of the encoding, not part "
        "of the string.<bookmark mark='whitespace'/>"
    ),
    # -- Scene 08 --------------------------------------------------------
    "s08a": (
        "The same machinery runs in reverse. The model's output is not text "
        "either. It is more integers.<bookmark mark='reverse'/>"
    ),
    "s08b": (
        "Three thousand three hundred and twenty three.<bookmark "
        "mark='id1'/> Six hundred and twenty two.<bookmark mark='id2'/> Look "
        "them up and you get Sub, and ject. Decoded together, they read "
        "Subject.<bookmark mark='joined'/>"
    ),
    "s08c": (
        "So the tokenizer stands on both sides of the model. Text to IDs on "
        "the way in.<bookmark mark='in'/> IDs back to text on the way out."
        "<bookmark mark='out'/> That is why the same component appears twice "
        "in the pipeline."
    ),
}


class Chapter2Act2(LLMScene):
    """Scenes 06-08: what determines a tokenizer, and the round trip."""

    narration = NARRATION

    module_stem = "act2_scenes"

    def construct(self) -> None:
        self.setup_episode()
        self.add_backdrop()

        self.s06_inside_a_tokenizer()
        self.s07_the_vocabulary_lookup()
        self.s08_the_journey_back()

        self.write_real_srt()

    # =================================================================
    # Scene 06 - Inside a Tokenizer
    # =================================================================
    def s06_inside_a_tokenizer(self) -> None:
        with self.beat("s06a") as tracker:
            self.scene_title("06  -  Inside a Tokenizer")
            self.play(FadeIn(self.chrome), run_time=0.5)

            self.view_3d(phi=64, theta=-58, zoom=1.0, animate=False)
            rig = control_console([
                ("Method", "BPE / WordPiece"),
                ("Parameters", "vocab size, specials"),
                ("Training data", "prose / code / domain"),
            ])
            rig.scale(0.85).move_to(np.array([0.0, 0.45, 0.0]))
            self.hold(rig)
            self.play(FadeIn(rig, shift=UP * 0.2), run_time=0.9)

            # legible HUD labels: the dial captions are in 3D and small
            labels = VGroup()
            for i, (name, val) in enumerate([
                ("Method", "BPE / WordPiece"),
                ("Parameters", "vocab size, specials"),
                ("Training data", "prose / code / domain"),
            ]):
                lbl = VGroup(
                    pg(name, 18, [NEON_CYAN, NEON_VIOLET, AMBER][i], "BOLD"),
                    pg(val, 14, MUTED),
                ).arrange(DOWN, buff=0.06)
                lbl.move_to(np.array([-3.6 + i * 3.6, -1.42, 0.0]))
                labels.add(lbl)
            self.hud(labels)
            self.keep.add(labels)
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.12) for x in labels],
                                  lag_ratio=0.25),
                      run_time=rt(tracker.time_until_bookmark("method") * 0.4))
            # the three controls light up as the narration names them
            self.play(LaggedStart(*[Indicate(d, color=WHITE, scale_factor=1.18)
                                    for d in rig.dials], lag_ratio=0.4),
                      run_time=rt(tracker.time_until_bookmark("method") * 0.45))

        self.dissolve(tracker)
        # The 3D rig is a one-beat shot: give the camera back to the panel and
        # drop the console, or every later beat in this scene draws tilted.
        self.release_stage(0.5)
        self.view_2d(animate=True, run_time=0.8)

        with self.beat("s06b") as tracker:
            chart = vocab_bar_chart(VOCAB_SIZES, width=8.6, height=2.8)
            chart.move_to(np.array([0.0, 0.30, 0.0]))
            self.play(FadeIn(chart), run_time=0.8)
            self.keep.add(chart)

            hl = VGroup()
            for name in ("BERT uncased", "GPT-2", "GPT-4"):
                for row in chart.rows:
                    if row[0].text == name:
                        hl.add(Rectangle(
                            width=chart.width - 0.04,
                            height=row.height,
                            stroke_color=AMBER, stroke_width=1.6,
                            fill_opacity=0.0).move_to(row.get_center()))
            self.play(LaggedStart(*[Create(b) for b in hl], lag_ratio=0.3),
                      run_time=rt(tracker.time_until_bookmark("gpt4") * 0.7))
            note = callout("real vocabulary sizes, as published in the book",
                           color=GREEN, size=15).move_to(
                np.array([0.0, -1.55, 0.0]))
            self.play(FadeIn(note), run_time=0.5)
            chip = self.hud(source_chip("book"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(hl, note, chip)

        self.dissolve(tracker)

        with self.beat("s06c") as tracker:
            left = panel(4.6, 1.35, color=NEON_CYAN)
            left.move_to(np.array([-2.7, 0.55, 0.0]))
            lt = VGroup(
                pg("trained on prose", 19, INK, "BOLD"),
                mono("play  token  word", 20, MUTED),
            ).arrange(DOWN, buff=0.16).move_to(left.get_center())
            right = panel(4.6, 1.35, color=AMBER)
            right.move_to(np.array([2.7, 0.55, 0.0]))
            rt_ = VGroup(
                pg("trained on code", 19, INK, "BOLD"),
                mono("    elif  def  return", 20, MUTED),
            ).arrange(DOWN, buff=0.16).move_to(right.get_center())

            self.play(FadeIn(VGroup(left, lt)), FadeIn(VGroup(right, rt_)),
                      run_time=rt(tracker.time_until_bookmark("data") * 0.6))
            same = pg("same method, same size", 20, MUTED).move_to(
                np.array([0.0, -0.55, 0.0]))
            concl = callout("a method name cannot predict the split",
                            color=ROSE, size=18).move_to(
                np.array([0.0, -1.35, 0.0]))
            self.play(FadeIn(same), run_time=0.4)
            self.play(FadeIn(concl),
                      run_time=rt(tracker.time_until_bookmark("conclude") * 0.7))
            self.keep.add(VGroup(left, lt), VGroup(right, rt_), same, concl)

        self.dissolve(tracker)

        with self.beat("s06d") as tracker:
            specials = [
                ("[UNK]", "unknown", ROSE),
                ("[PAD]", "padding", NEON_BLUE),
                ("<s>", "begin", NEON_CYAN),
                ("</s>", "end", NEON_CYAN),
                ("[SEP]", "separator", NEON_VIOLET),
                ("[MASK]", "mask", NEON_MAGENTA),
                ("<|endoftext|>", "GPT end", AMBER),
                ("<|assistant|>", "chat role", GREEN),
            ]
            tiles = VGroup()
            for marker, meaning, color in specials:
                box = panel(2.42, 0.58, color=color, fill_opacity=0.16)
                name = mono(marker, 16, color, "BOLD")
                mean = pg(meaning, 11, MUTED)
                VGroup(name, mean).arrange(RIGHT, buff=0.18).move_to(
                    box.get_center())
                tiles.add(VGroup(box, name, mean))
            # Build the rows from explicit indices: VGroup *slicing* returns
            # family members (every glyph), not the top-level children.
            rows = VGroup(
                VGroup(*[tiles[i] for i in range(4)]).arrange(RIGHT, buff=0.16),
                VGroup(*[tiles[i] for i in range(4, 8)]).arrange(RIGHT, buff=0.16),
            ).arrange(DOWN, buff=0.18).move_to(np.array([0.0, 0.55, 0.0]))

            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.10) for t in tiles],
                                  lag_ratio=0.12),
                      run_time=rt(tracker.time_until_bookmark("specials") * 0.8))
            note = callout("not words - instructions the model understands",
                           color=GREEN, size=18).move_to(
                np.array([0.0, -1.35, 0.0]))
            self.play(FadeIn(note),
                      run_time=rt(tracker.get_remaining_duration() * 0.7))
            chip = self.hud(source_chip("book"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(rows, note, chip)

        self.clear_stage(run_time=0.5)
        self.view_2d()

    # =================================================================
    # Scene 07 - The Vocabulary Lookup
    # =================================================================
    def s07_the_vocabulary_lookup(self) -> None:
        with self.beat("s07a") as tracker:
            self.scene_title("07  -  The Vocabulary Lookup")
            self.play(FadeIn(self.chrome), run_time=0.5)

            word = mono(PHI3["word"], 40, INK).move_to(
                np.array([0.0, 0.85, 0.0]))
            self.play(FadeIn(word, shift=DOWN * 0.14),
                      run_time=rt(tracker.time_until_bookmark("word") * 0.7))
            meta = callout(
                f"{PHI3['name']}  -  {PHI3['method']}, vocabulary "
                f"{PHI3['vocab']:,}  (book p.{PHI3['page']})",
                color=NEON_CYAN, size=14).move_to(
                np.array([0.0, -1.30, 0.0]))
            self.play(FadeIn(meta), run_time=0.5)
            chip = self.hud(source_chip("book"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(VGroup(word, meta, chip))

        self.dissolve(tracker)

        with self.beat("s07b") as tracker:
            word = mono(PHI3["word"], 36, INK).move_to(
                np.array([0.0, 1.35, 0.0]))
            self.play(FadeIn(word), run_time=0.5)
            cut = Line(np.array([0.0, 0.98, 0.0]),
                       np.array([0.0, 1.72, 0.0]),
                       stroke_color=ROSE, stroke_width=2.6)
            pieces = token_row([p for p, _ in PHI3["pieces"]], size=32)
            pieces.move_to(np.array([0.0, 0.25, 0.0]))
            self.play(Create(cut), run_time=0.4)
            self.play(
                FadeOut(word), FadeOut(cut),
                LaggedStart(*[FadeIn(b, shift=DOWN * 0.16) for b in pieces],
                            lag_ratio=0.3),
                run_time=rt(tracker.time_until_bookmark("split") * 0.8),
            )
            self.keep.add(pieces)
            note = pg("neither piece is a word on its own", 20, MUTED)
            note.move_to(np.array([0.0, -0.90, 0.0]))
            self.play(FadeIn(note),
                      run_time=rt(tracker.get_remaining_duration() * 0.7))
            self.keep.add(note)

        self.clear_stage(run_time=0.5)

        # the vault: a real searchable vocabulary, in 3D
        with self.beat("s07c") as tracker:
            self.view_3d(phi=62, theta=-62, zoom=1.0, animate=False)
            entries = [(p, i) for p, i in PHI3["pieces"]] + [
                ("token", 3301), ("garden", 7229), ("Subject", 3323),
                ("##ization", 7712), ("to", 304),
            ]
            wall = vault_wall(entries, rows_visible=3)
            wall.scale(0.85).move_to(np.array([0.0, 1.10, 0.0]))
            self.play(FadeIn(wall), run_time=0.9)
            self.hold(wall)
            drawer = wall[0]
            self.add(glow(drawer, color=NEON_CYAN, layers=2, base_opacity=0.30))
            self.play(drawer.animate.shift(np.array([0.0, 0.0, 0.55])),
                      run_time=rt(tracker.time_until_bookmark("id1") * 0.6))
            apply_depth(drawer, base=-5.5)

            chips = id_array([i for _, i in PHI3["pieces"]], size=30)
            chips.move_to(np.array([0.0, -1.45, 0.0]))
            self.hud(chips)
            self.play(FadeIn(chips),
                      run_time=rt(tracker.time_until_bookmark("array") * 0.7))
            chip = self.hud(source_chip("book"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(chips, chip)

        self.dissolve(tracker)
        self.release_stage(0.5)

        with self.beat("s07d") as tracker:
            pair = token_row([p for p, _ in PHI3["pieces"]], size=30)
            pair.move_to(np.array([0.0, 1.30, 0.0]))
            self.play(FadeIn(pair), run_time=0.6)
            # U+2423 renders as nothing in every installed font, so the
            # continuation marker is a *drawn* box, never a character.
            marker = space_marker(0.42, AMBER)
            marker.next_to(pair[1], LEFT, buff=0.10)
            self.play(FadeIn(marker), run_time=0.4)
            self.play(Circumscribe(pair[1], color=AMBER, buff=0.12),
                      run_time=rt(tracker.time_until_bookmark("whitespace") * 0.7))
            note = callout("whitespace is encoded, not written",
                           color=AMBER, size=18).move_to(
                np.array([0.0, -1.45, 0.0]))
            self.play(FadeIn(note),
                      run_time=rt(tracker.get_remaining_duration() * 0.6))
            chip = self.hud(source_chip("book"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(VGroup(pair, marker, note, chip))

        self.clear_stage(run_time=0.5)
        self.view_2d()

    # =================================================================
    # Scene 08 - The Journey Back
    # =================================================================
    def s08_the_journey_back(self) -> None:
        with self.beat("s08a") as tracker:
            self.scene_title("08  -  The Journey Back")
            self.play(FadeIn(self.chrome), run_time=0.5)

            ids = id_array([p for _, p in PHI3_DECODE["pieces"]], size=34)
            ids.move_to(np.array([0.0, 0.75, 0.0]))
            self.play(FadeIn(ids, shift=DOWN * 0.14),
                      run_time=rt(tracker.time_until_bookmark("reverse") * 0.7))
            note = pg("the model's output is integers, not text", 20, MUTED)
            note.move_to(np.array([0.0, -0.85, 0.0]))
            self.play(FadeIn(note),
                      run_time=rt(tracker.get_remaining_duration() * 0.7))
            self.keep.add(VGroup(ids, note))

        self.dissolve(tracker)

        with self.beat("s08b") as tracker:
            ids = id_array([p for _, p in PHI3_DECODE["pieces"]], size=34)
            ids.move_to(np.array([0.0, 1.30, 0.0]))
            self.play(FadeIn(ids), run_time=0.5)

            pieces = VGroup(*[
                VGroup(mono(tok, 30, INK),
                       id_chip(ident, size=18)).arrange(DOWN, buff=0.14)
                for tok, ident in PHI3_DECODE["pieces"]
            ]).arrange(RIGHT, buff=0.70).move_to(
                np.array([0.0, 0.05, 0.0]))
            self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.14) for p in pieces],
                                  lag_ratio=0.35),
                      run_time=rt(tracker.time_until_bookmark("joined") * 0.7))

            joined = mono(PHI3_DECODE["joined"], 38, GREEN, "BOLD")
            joined.move_to(np.array([0.0, -1.15, 0.0]))
            self.play(TransformFromCopy(pieces, joined),
                      run_time=rt(tracker.time_until_bookmark("joined") * 0.5))
            self.play(Circumscribe(joined, color=GREEN, buff=0.16), run_time=0.6)
            chip = self.hud(source_chip("book"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(VGroup(ids, pieces, joined, chip))

        self.dissolve(tracker)

        with self.beat("s08c") as tracker:
            box = panel(9.6, 2.35, color=PANEL_EDGE).move_to(
                np.array([0.0, 0.15, 0.0]))
            enc = VGroup(
                pg("text", 20, INK, "BOLD"),
                pg("tokenizer", 17, NEON_CYAN, "BOLD"),
                mono("IDs", 20, NEON_CYAN),
            ).arrange(RIGHT, buff=0.85)
            enc.move_to(np.array([0.0, 0.88, 0.0]))
            model = panel(2.4, 1.0, color=NEON_BLUE).move_to(
                np.array([0.0, 0.00, 0.0]))
            mlbl = pg("MODEL", 18, NEON_BLUE, "BOLD").move_to(model.get_center())
            dec = VGroup(
                mono("IDs", 20, NEON_VIOLET),
                pg("tokenizer", 17, NEON_VIOLET, "BOLD"),
                pg("text", 20, INK, "BOLD"),
            ).arrange(RIGHT, buff=0.85).move_to(np.array([0.0, -0.88, 0.0]))
            self.play(FadeIn(VGroup(box, enc)), run_time=0.7)
            self.play(FadeIn(VGroup(model, mlbl)),
                      run_time=rt(tracker.time_until_bookmark("in") * 0.6))
            self.play(FadeIn(dec),
                      run_time=rt(tracker.time_until_bookmark("out") * 0.6))
            self.play(Indicate(VGroup(enc, dec), color=GREEN, scale_factor=1.03),
                      run_time=rt(tracker.get_remaining_duration() * 0.7))
            self.keep.add(VGroup(box, enc, model, mlbl, dec))

        self.clear_stage(run_time=0.5)

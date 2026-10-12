"""ACT III - The tokenizer experiment (Scenes 09-12).

    Scene 09  One Prompt, Four Tokenizers     the laboratory bench
    Scene 10  The Capitalization Challenge    same word, four different splits
    Scene 11  The Emoji That Disappeared      [UNK] versus byte fallback
    Scene 12  Why Spaces Matter to Code       indentation, keywords, digits

This is the technical centrepiece, so the book's recorded values are used
verbatim and every illustrative element is labelled.  Three audit additions
live here:

  * F1 - GPT-2 is labelled "BPE (byte fallback)", not "byte-level BPE", which
    the book explicitly says these tokenizers are not.
  * F5 - the book prints token IDs for the musical note only, so the Chinese
    character is shown as byte-derived pieces *with no IDs invented*.
  * G1 - BERT's *cased* variant (eight pieces for the same word) is included;
    it is the sharpest contrast in the whole comparison.
  * G3 - BERT uncased discards newlines, which the storyboard omitted.
  * G4 - StarCoder2's one-token-per-digit behaviour, for the code scene.

Render:
    python -m manim render --resolution 640,360 --fps 30 \
        --media_dir D:\\m3 act3_scenes.py Chapter2Act3
"""
from __future__ import annotations

import numpy as np

from manim import (
    DOWN, LEFT, ORIGIN, RIGHT, UP,
    Arrow, Circumscribe, Create, FadeIn, FadeOut, GrowArrow, Indicate, LaggedStart,
    Line, Rectangle, ReplacementTransform, RoundedRectangle, Text,
    TransformFromCopy, VGroup, Write,
)

from components import (
    book_sample_line, brace_meter, byte_sequence, callout, id_array, id_chip,
    music_note, token_block, token_row, unknown_token, vocab_bar_chart,
)
from data_traces import (
    BOOK_SAMPLE, CODE_SAMPLE, COMPARISON_KEYS, GPT2_EMOJI, TOKENIZERS,
)
from theme import (
    AMBER, GREEN, INK, MUTED, NEON_BLUE, NEON_CYAN, NEON_MAGENTA,
    NEON_VIOLET, PANEL, PANEL_EDGE, ROSE, SAFE_B, SAFE_L, SAFE_R, SAFE_T, SAFE_W, cjk,
    WHITE, LLMScene, fit, mono, panel, pg, rt, source_chip, title_bar,
    token_color,
)
from three_d import apply_depth, grid_floor, input_grid_floor, lab_bench

# ============================================================== narration ===
NARRATION = {
    # -- Scene 09 --------------------------------------------------------
    "s09a": (
        "Time for the experiment.<bookmark mark='start'/> The book takes one "
        "single string and runs it through one trained tokenizer after "
        "another, so the only thing changing is the tokenizer itself."
        "<bookmark mark='one'/>"
    ),
    "s09b": (
        "Here are four of them.<bookmark mark='four'/> BERT uncased, which "
        "uses WordPiece. GPT-2, which uses byte pair encoding. FLAN-T5, which "
        "uses SentencePiece. And GPT-4, also byte pair encoding, with a much "
        "larger vocabulary.<bookmark mark='named'/>"
    ),
    "s09c": (
        "Notice the distinction. WordPiece and byte pair encoding are "
        "algorithms. SentencePiece is a framework that can implement more "
        "than one of them. And FLAN-T5 and GPT-4 are models that own a "
        "particular trained tokenizer.<bookmark mark='distinct'/> Keep those "
        "separate, and the rest of this comparison makes sense."
    ),
    "s09d": (
        "The book compares eight trained tokenizers in total. We are showing "
        "four, because four is enough to see the disagreements."
        "<bookmark mark='subset'/> And they do disagree."
        "<bookmark mark='disagree'/>"
    ),
    # -- Scene 10 --------------------------------------------------------
    "s10a": (
        "Look at one word from the test string: capitalization, written in "
        "capitals.<bookmark mark='word'/>"
    ),
    "s10b": (
        "BERT uncased lowercases its input first. So the capitals are gone "
        "before anything else happens.<bookmark mark='lower'/> It then splits "
        "the word into capital, and hash-hash ization. Two pieces."
        "<bookmark mark='two'/> Those double hashes mark a continuation: this "
        "token is joined to the one before it."
    ),
    "s10c": (
        "But BERT also ships in a cased version, and it does not lowercase. "
        "The very same word becomes eight pieces.<bookmark mark='eight'/> "
        "Eight. That is four times the cost, for one word."
    ),
    "s10d": (
        "GPT-2 keeps the capitals and uses four pieces.<bookmark mark='gpt2'/> "
        "FLAN-T5 uses five.<bookmark mark='t5'/> GPT-4 uses two: CAPITAL, and "
        "IZATION.<bookmark mark='gpt4'/> Same input, same word, four different "
        "answers."
    ),
    "s10e": (
        "And there is a cost that never shows up in a token count. BERT "
        "uncased throws the newline characters away completely."
        "<bookmark mark='newline'/> Which means a chat log, where every turn "
        "starts on a new line, loses that structure before the model ever "
        "sees it.<bookmark mark='blind'/>"
    ),
    # -- Scene 11 --------------------------------------------------------
    "s11a": (
        "Now the part of the test string that breaks the older tokenizers. A "
        "musical note, and the Chinese character for bird.<bookmark "
        "mark='chars'/>"
    ),
    "s11b": (
        "BERT replaces both with unknown.<bookmark mark='bert'/> FLAN-T5 does "
        "the same thing, using its own marker.<bookmark mark='t5'/> And here "
        "is why that matters: the marker records that something was there. It "
        "does not record what.<bookmark mark='gone'/> Look the marker up, and "
        "the character is simply gone."
    ),
    "s11c": (
        "GPT-2 takes a different route. It falls back to the raw bytes that "
        "make up the character.<bookmark mark='bytes'/> The musical note is "
        "three bytes, and they become three tokens.<bookmark mark='three'/> "
        "Printed on their own they look like replacement characters, because "
        "a single byte is not a readable character."
    ),
    "s11d": (
        "Their identifiers are 8582, 236 and 113.<bookmark mark='ids'/> Decode "
        "them together, as a group, and the note comes back intact."
        "<bookmark mark='back'/> The book prints no identifiers for the "
        "Chinese character, so neither do we.<bookmark mark='noids'/>"
    ),
    "s11e": (
        "That is the trade. Byte fallback keeps coverage, so nothing is ever "
        "simply lost.<bookmark mark='trade'/> But a single character can cost "
        "several tokens, and every one of them takes a position in the "
        "context.<bookmark mark='cost'/>"
    ),
    # -- Scene 12 --------------------------------------------------------
    "s12a": (
        "One more kind of input decides the outcome: whitespace. Here is the "
        "book's own code example.<bookmark mark='code'/> Those dots mark four "
        "spaces of indentation. They are not code — they are showing you what "
        "is invisible."
    ),
    "s12b": (
        "Send those four spaces through a character-level tokenizer and you "
        "get four separate tokens.<bookmark mark='four'/> The model then has "
        "to work out that they belong together, and how deep the indentation "
        "is."
    ),
    "s12c": (
        "GPT-4 does something better here. It holds a single token for four "
        "consecutive spaces. In fact it has a dedicated token for every run "
        "of whitespace up to eighty three.<bookmark mark='spaces'/> And the "
        "Python keyword elif gets a token of its own.<bookmark mark='elif'/>"
    ),
    "s12d": (
        "StarCoder2 is a code specialist, and pushes further. It gives every "
        "digit its own token, so six hundred becomes three tokens: six, zero, "
        "zero.<bookmark mark='digits'/> The reasoning is that numbers and "
        "mathematics are represented more clearly that way."
    ),
    "s12e": (
        "One caution. This is not parsing. A tokenizer that handles "
        "indentation and keywords well makes the model's job easier."
        "<bookmark mark='easier'/> It does not make the code it generates "
        "correct.<bookmark mark='correct'/>"
    ),
}


def _split_row(label: str, pieces, *, y: float, color: str, note: str = "",
               size: int = 21, start_index: int = 0) -> VGroup:
    """One tokenizer's answer: name on the left, its pieces along the row."""
    name = pg(label, 17, color, "BOLD").move_to(
        np.array([SAFE_L + 1.15, y, 0.0]))
    blocks = token_row(list(pieces), size=size, start_index=start_index)
    left_edge = SAFE_L + 2.30
    avail = (SAFE_R - 2.70) - left_edge
    # BERT cased needs eight pieces; at full size they run off the frame.
    if blocks.width > avail:
        blocks.scale(avail / blocks.width)
    blocks.move_to(np.array([0.0, y, 0.0]))
    blocks.align_to(np.array([left_edge, y, 0.0]), LEFT)
    sub = pg(note, 12, MUTED).move_to(np.array([SAFE_R - 1.35, y, 0.0]))
    g = VGroup(name, blocks, sub)
    g.name, g.blocks, g.sub = name, blocks, sub
    return g


class Chapter2Act3(LLMScene):
    """Scenes 09-12: the same string through four trained tokenizers."""

    narration = NARRATION

    module_stem = "act3_scenes"

    def construct(self) -> None:
        self.setup_episode()
        self.add_backdrop()

        self.s09_one_prompt_four_tokenizers()
        self.s10_the_capitalization_challenge()
        self.s11_the_emoji_that_disappeared()
        self.s12_why_spaces_matter_to_code()

        self.write_real_srt()

    # =================================================================
    # Scene 09 - One Prompt, Four Tokenizers
    # =================================================================
    def s09_one_prompt_four_tokenizers(self) -> None:
        by_key = {t["key"]: t for t in TOKENIZERS}
        chosen = [by_key[k] for k in COMPARISON_KEYS]
        colors = [NEON_CYAN, NEON_BLUE, "#A6D854", "#E78AC3"]

        with self.beat("s09a") as tracker:
            self.scene_title("09  -  One Prompt, Four Tokenizers")
            self.play(FadeIn(self.chrome), run_time=0.5)

            sample = book_sample_line(size=15)
            fit(sample, SAFE_W - 0.6)
            sample.move_to(np.array([0.0, 1.95, 0.0]))
            self.play(FadeIn(sample, shift=DOWN * 0.12),
                      run_time=rt(tracker.time_until_bookmark("one") * 0.7))
            self.hold(sample)

        self.dissolve(tracker)
        self.release_stage(0.4)

        with self.beat("s09b") as tracker:
            self.view_3d(phi=68, theta=-64, zoom=1.0, animate=False)
            bench = lab_bench([(t["label"], t["method"], t["year"], c)
                               for t, c in zip(chosen, colors)], spacing=2.85)
            # the projected rig is wider and lower than its world coordinates
            # suggest, so it is scaled and lifted to sit inside the rim
            bench.scale(0.68).move_to(np.array([0.0, 0.62, 0.0]))
            self.play(FadeIn(bench[0]), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.30)
                                    for m in bench.machines], lag_ratio=0.28),
                      run_time=rt(tracker.time_until_bookmark("named") * 0.5))
            self.hold(bench)

            labels = VGroup()
            for i, (t, c) in enumerate(zip(chosen, colors)):
                lbl = VGroup(
                    pg(t["label"], 16, c, "BOLD"),
                    pg(f"{t['method']}  {t['year']}", 12, MUTED),
                ).arrange(DOWN, buff=0.05)
                lbl.move_to(np.array([-4.30 + i * 2.87, -1.35, 0.0]))
                labels.add(lbl)
            self.hud(labels)
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.10) for x in labels],
                                  lag_ratio=0.2),
                      run_time=rt(tracker.time_until_bookmark("named") * 0.55))
            self.keep.add(labels)

        self.dissolve(tracker)
        self.release_stage(0.5)
        self.view_2d(animate=True, run_time=0.8)

        with self.beat("s09c") as tracker:
            algo = panel(3.35, 1.5, color=NEON_CYAN).move_to(
                np.array([-3.55, 0.45, 0.0]))
            al = VGroup(
                pg("ALGORITHMS", 16, NEON_CYAN, "BOLD"),
                mono("BPE", 24, INK), mono("WordPiece", 24, INK),
            ).arrange(DOWN, buff=0.10).move_to(algo.get_center())
            frame = panel(3.35, 1.5, color=AMBER).move_to(
                np.array([0.0, 0.45, 0.0]))
            fl = VGroup(
                pg("FRAMEWORK", 16, AMBER, "BOLD"),
                mono("SentencePiece", 22, INK),
                pg("can implement either", 13, MUTED),
            ).arrange(DOWN, buff=0.10).move_to(frame.get_center())
            models = panel(3.35, 1.5, color=NEON_VIOLET).move_to(
                np.array([3.55, 0.45, 0.0]))
            ml = VGroup(
                pg("MODELS", 16, NEON_VIOLET, "BOLD"),
                mono("FLAN-T5", 20, INK), mono("GPT-4", 20, INK),
            ).arrange(DOWN, buff=0.10).move_to(models.get_center())

            self.play(FadeIn(VGroup(algo, al)), run_time=0.6)
            self.play(FadeIn(VGroup(frame, fl)),
                      run_time=rt(tracker.time_until_bookmark("distinct") * 0.6))
            self.play(FadeIn(VGroup(models, ml)), run_time=0.6)
            self.keep.add(VGroup(algo, al), VGroup(frame, fl), VGroup(models, ml))

        self.dissolve(tracker)

        with self.beat("s09d") as tracker:
            note = callout("the book compares eight tokenizers - these are four",
                           color=NEON_CYAN, size=18).move_to(
                np.array([0.0, 1.30, 0.0]))
            self.play(FadeIn(note),
                      run_time=rt(tracker.time_until_bookmark("subset") * 0.6))
            sample = mono("CAPITALIZATION", 40, INK, "BOLD").move_to(
                np.array([0.0, 0.05, 0.0]))
            self.play(FadeIn(sample, scale=1.1),
                      run_time=rt(tracker.time_until_bookmark("disagree") * 0.6))
            self.play(Indicate(sample, color=ROSE, scale_factor=1.06),
                      run_time=rt(tracker.get_remaining_duration() * 0.6))
            chip = self.hud(source_chip("book"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(note, sample, chip)

        self.clear_stage(run_time=0.5)

    # =================================================================
    # Scene 10 - The Capitalization Challenge
    # =================================================================
    def s10_the_capitalization_challenge(self) -> None:
        by_key = {t["key"]: t for t in TOKENIZERS}

        with self.beat("s10a") as tracker:
            self.scene_title("10  -  The Capitalization Challenge")
            self.play(FadeIn(self.chrome), run_time=0.5)
            word = mono("CAPITALIZATION", 44, INK, "BOLD").move_to(
                np.array([0.0, 0.55, 0.0]))
            self.play(FadeIn(word, scale=1.06),
                      run_time=rt(tracker.time_until_bookmark("word") * 0.7))
            chip = self.hud(source_chip("book"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(VGroup(word, chip))

        self.dissolve(tracker)

        # BERT uncased: lowercases before it splits
        with self.beat("s10b") as tracker:
            upper = mono("CAPITALIZATION", 30, MUTED).move_to(
                np.array([0.0, 1.70, 0.0]))
            lower = mono("capitalization", 30, INK).move_to(
                np.array([0.0, 1.70, 0.0]))
            self.play(FadeIn(upper), run_time=0.4)
            self.play(ReplacementTransform(upper, lower),
                      run_time=rt(tracker.time_until_bookmark("two") * 0.25))
            row = _split_row(by_key["bert_uncased"]["label"],
                             by_key["bert_uncased"]["caps"],
                             y=0.55, color=NEON_CYAN,
                             note="lowercases the input first")
            self.play(FadeIn(row.name), run_time=0.3)
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.12)
                                    for b in row.blocks], lag_ratio=0.3),
                      run_time=rt(tracker.time_until_bookmark("two") * 0.5))
            self.play(FadeIn(row.sub), run_time=0.4)
            hashnote = callout("## marks a continuation of the previous token",
                               color=AMBER, size=16).move_to(
                np.array([0.0, -1.20, 0.0]))
            self.play(FadeIn(hashnote),
                      run_time=rt(tracker.get_remaining_duration() * 0.6))
            self.keep.add(VGroup(lower, row, hashnote))

        self.dissolve(tracker)

        # BERT cased: the same word, eight pieces  (audit addition G1)
        with self.beat("s10c") as tracker:
            row = _split_row(by_key["bert_cased"]["label"],
                             by_key["bert_cased"]["caps"],
                             y=0.55, color=NEON_MAGENTA,
                             note="keeps capitals - 8 pieces")
            self.play(FadeIn(row.name), run_time=0.3)
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.10)
                                    for b in row.blocks], lag_ratio=0.12),
                      run_time=rt(tracker.time_until_bookmark("eight") * 0.7))
            self.play(FadeIn(row.sub), run_time=0.4)
            cost = callout("one word, four times the cost", color=ROSE,
                           size=17).move_to(np.array([0.0, -1.20, 0.0]))
            self.play(FadeIn(cost),
                      run_time=rt(tracker.get_remaining_duration() * 0.6))
            chip = self.hud(source_chip("book"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(VGroup(row, cost, chip))

        self.clear_stage(run_time=0.5)

        # all four side by side
        with self.beat("s10d") as tracker:
            rows = VGroup(
                _split_row(by_key["bert_uncased"]["label"],
                           by_key["bert_uncased"]["caps"], y=1.35,
                           color=NEON_CYAN, note="2 pieces", size=19),
                _split_row(by_key["gpt2"]["label"], by_key["gpt2"]["caps"],
                           y=0.55, color=NEON_BLUE, note="4 pieces", size=19),
                _split_row(by_key["flan_t5"]["label"], by_key["flan_t5"]["caps"],
                           y=-0.25, color="#A6D854", note="5 pieces", size=19),
                _split_row(by_key["gpt4"]["label"], by_key["gpt4"]["caps"],
                           y=-1.05, color="#E78AC3", note="2 pieces", size=19),
            )
            self.play(FadeIn(rows[0]), run_time=0.4)
            self.play(FadeIn(rows[1]),
                      run_time=rt(tracker.time_until_bookmark("t5") * 0.5))
            self.play(FadeIn(rows[2]), run_time=0.5)
            self.play(FadeIn(rows[3]),
                      run_time=rt(tracker.time_until_bookmark("gpt4") * 0.6))
            self.play(LaggedStart(*[
                Circumscribe(r.blocks, color=WHITE, buff=0.06)
                for r in rows
            ], lag_ratio=0.25),
                      run_time=rt(tracker.get_remaining_duration() * 0.7))
            chip = self.hud(source_chip("book"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(rows, chip)

        self.dissolve(tracker)

        # the newline cost (audit addition G3)
        with self.beat("s10e") as tracker:
            log = mono("user: hello\nassistant: hi\nuser: help", 24, INK)
            log.move_to(np.array([0.0, 0.75, 0.0]))
            flat = mono("user: hello assistant: hi user: help", 24, ROSE)
            flat.move_to(np.array([0.0, 0.75, 0.0]))
            self.play(FadeIn(log), run_time=0.6)
            self.play(ReplacementTransform(log, flat),
                      run_time=rt(tracker.time_until_bookmark("blind") * 0.6))
            warn = callout("newlines dropped - the line structure is gone",
                           color=ROSE, size=18).move_to(
                np.array([0.0, -0.85, 0.0]))
            self.play(FadeIn(warn),
                      run_time=rt(tracker.get_remaining_duration() * 0.6))
            chip = self.hud(source_chip("book"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(VGroup(flat, warn, chip))

        self.clear_stage(run_time=0.5)

    # =================================================================
    # Scene 11 - The Emoji That Disappeared
    # =================================================================
    def s11_the_emoji_that_disappeared(self) -> None:
        with self.beat("s11a") as tracker:
            self.scene_title("11  -  The Emoji That Disappeared")
            self.play(FadeIn(self.chrome), run_time=0.5)
            big = VGroup(
                music_note(height=1.55, color=INK),
                cjk(GPT2_EMOJI["other_char"], 58),
            ).arrange(RIGHT, buff=0.85)
            big.move_to(np.array([0.0, 0.45, 0.0]))
            self.play(FadeIn(big, scale=1.15),
                      run_time=rt(tracker.time_until_bookmark("chars") * 0.7))
            chip = self.hud(source_chip("book"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(VGroup(big, chip))

        self.dissolve(tracker)

        with self.beat("s11b") as tracker:
            rows = VGroup()
            for label, marker, color in [("BERT uncased", "[UNK]", NEON_CYAN),
                                         ("FLAN-T5", "<unk>", "#A6D854")]:
                unk = VGroup(unknown_token(marker, size=24),
                             unknown_token(marker, size=24)).arrange(
                    RIGHT, buff=0.16)
                row = VGroup(pg(label, 17, color, "BOLD"), unk).arrange(
                    RIGHT, buff=0.60)
                rows.add(row)
            rows.arrange(DOWN, buff=0.42).move_to(np.array([0.0, 0.55, 0.0]))
            self.play(FadeIn(rows[0]),
                      run_time=rt(tracker.time_until_bookmark("t5") * 0.5))
            self.play(FadeIn(rows[1]), run_time=0.5)
            gone = callout("the marker records that something was there, "
                           "not what", color=ROSE, size=17).move_to(
                np.array([0.0, -1.15, 0.0]))
            self.play(FadeIn(gone),
                      run_time=rt(tracker.time_until_bookmark("gone") * 0.6))
            chip = self.hud(source_chip("book"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(rows, gone, chip)

        self.dissolve(tracker)

        with self.beat("s11c") as tracker:
            note = music_note(height=1.25, color=INK).move_to(
                np.array([0.0, 1.45, 0.0]))
            self.play(FadeIn(note), run_time=0.5)
            bytes_ = byte_sequence(GPT2_EMOJI["char"], size=22)
            bytes_.move_to(np.array([0.0, 0.55, 0.0]))
            self.play(FadeIn(bytes_, shift=UP * 0.14),
                      run_time=rt(tracker.time_until_bookmark("three") * 0.7))
            lbl = pg("three bytes of UTF-8", 17, MUTED).next_to(
                bytes_, DOWN, buff=0.24)
            self.play(FadeIn(lbl), run_time=0.4)
            self.keep.add(VGroup(note, bytes_, lbl))

        self.dissolve(tracker)

        with self.beat("s11d") as tracker:
            bytes_ = byte_sequence(GPT2_EMOJI["char"], size=22)
            bytes_.move_to(np.array([0.0, 0.75, 0.0]))
            self.play(FadeIn(bytes_), run_time=0.5)
            ids = id_array(GPT2_EMOJI["ids"], size=26)
            ids.move_to(np.array([0.0, -0.35, 0.0]))
            self.play(FadeIn(ids, shift=UP * 0.12),
                      run_time=rt(tracker.time_until_bookmark("ids") * 0.6))
            back = music_note(height=1.05, color=GREEN)
            back.move_to(np.array([-2.3, -1.18, 0.0]))
            # Arrow (not Line): GrowArrow needs a tip.  Keep the *mobject* --
            # an animation wrapper cannot be added to a VGroup.
            arrow = Arrow(np.array([0.4, -1.18, 0.0]),
                          np.array([-1.0, -1.18, 0.0]),
                          buff=0.0, color=GREEN, stroke_width=3.0,
                          max_tip_length_to_length_ratio=0.22)
            self.play(GrowArrow(arrow), FadeIn(back),
                      run_time=rt(tracker.time_until_bookmark("back") * 0.6))
            noids = callout("the book prints no IDs for the second character",
                            color=AMBER, size=15).move_to(
                np.array([2.30, -1.18, 0.0]))
            self.play(FadeIn(noids),
                      run_time=rt(tracker.time_until_bookmark("noids") * 0.5))
            chip = self.hud(source_chip("book"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(VGroup(bytes_, ids, back, arrow, noids, chip))

        self.dissolve(tracker)

        with self.beat("s11e") as tracker:
            trade = VGroup(
                callout("coverage preserved", color=GREEN, size=21),
                pg("but one character can cost several tokens", 20, MUTED),
                callout("and every token takes a context position",
                        color=ROSE, size=21),
            ).arrange(DOWN, buff=0.30).move_to(np.array([0.0, 0.45, 0.0]))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.12) for t in trade],
                                  lag_ratio=0.35),
                      run_time=rt(tracker.get_remaining_duration() * 0.8))
            self.keep.add(trade)

        self.clear_stage(run_time=0.5)

    # =================================================================
    # Scene 12 - Why Spaces Matter to Code
    # =================================================================
    def s12_why_spaces_matter_to_code(self) -> None:
        with self.beat("s12a") as tracker:
            self.scene_title("12  -  Why Spaces Matter to Code")
            self.play(FadeIn(self.chrome), run_time=0.5)

            code = VGroup(*[
                mono(line, 26, INK) for line in CODE_SAMPLE["lines"]
            ]).arrange(DOWN, buff=0.30, aligned_edge=LEFT)
            code.move_to(np.array([-0.4, 0.45, 0.0]))
            # highlight the four dots that stand for the indentation
            marks = VGroup()
            for line in code[1:]:
                marks.add(Rectangle(
                    width=1.15, height=0.44, stroke_color=AMBER,
                    stroke_width=1.6, fill_color=AMBER, fill_opacity=0.14,
                ).move_to(np.array([line.get_left()[0] + 0.52,
                                    line.get_center()[1], 0.0])))
            self.play(FadeIn(code), run_time=0.8)
            self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=0.4),
                      run_time=rt(tracker.time_until_bookmark("code") * 0.7))
            note = pg(CODE_SAMPLE["note"], 16, AMBER).move_to(
                np.array([0.0, -1.45, 0.0]))
            self.play(FadeIn(note), run_time=0.6)
            chip = self.hud(source_chip("book"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(VGroup(code, marks, note, chip))

        self.dissolve(tracker)

        with self.beat("s12b") as tracker:
            four = token_row(list("    "), size=30, start_index=0)
            four.move_to(np.array([0.0, 0.75, 0.0]))
            self.play(FadeIn(four, shift=UP * 0.12),
                      run_time=rt(tracker.time_until_bookmark("four") * 0.6))
            bar = brace_meter(four, "4 tokens", direction=DOWN, color=ROSE)
            self.play(FadeIn(bar), run_time=0.5)
            cost = callout("the model must reconstruct the indentation level",
                           color=ROSE, size=18).move_to(
                np.array([0.0, -1.15, 0.0]))
            self.play(FadeIn(cost),
                      run_time=rt(tracker.get_remaining_duration() * 0.6))
            self.keep.add(VGroup(four, bar, cost))

        self.dissolve(tracker)

        with self.beat("s12c") as tracker:
            # Four literal spaces render as nothing in Pango, so the token
            # carries the visible space marker the rest of the episode uses.
            one = token_block("\u2423\u2423\u2423\u2423", 3, size=30)
            one.move_to(np.array([0.0, 0.95, 0.0]))
            self.play(FadeIn(one, shift=UP * 0.12),
                      run_time=rt(tracker.time_until_bookmark("spaces") * 0.6))
            bar = brace_meter(one, "1 token", direction=DOWN, color=GREEN)
            self.play(FadeIn(bar), run_time=0.5)
            elif_ = VGroup(
                pg("and a keyword gets a token of its own", 17, MUTED),
                token_row(["elif"], size=30, start_index=5),
            ).arrange(RIGHT, buff=0.40).move_to(np.array([0.0, -0.85, 0.0]))
            self.play(FadeIn(elif_),
                      run_time=rt(tracker.get_remaining_duration() * 0.6))
            chip = self.hud(source_chip("book"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(VGroup(one, bar, elif_, chip))

        self.dissolve(tracker)

        with self.beat("s12d") as tracker:
            digits = token_row(list("600"), size=32, start_index=0)
            digits.move_to(np.array([0.0, 0.65, 0.0]))
            self.play(FadeIn(digits, shift=UP * 0.12),
                      run_time=rt(tracker.time_until_bookmark("digits") * 0.6))
            lbl = VGroup(
                pg("StarCoder2 - trained on code", 18, AMBER, "BOLD"),
                pg("one token per digit", 16, MUTED),
            ).arrange(DOWN, buff=0.12).move_to(np.array([0.0, -0.65, 0.0]))
            self.play(FadeIn(lbl),
                      run_time=rt(tracker.get_remaining_duration() * 0.6))
            chip = self.hud(source_chip("book"))
            self.play(FadeIn(chip), run_time=0.3)
            self.keep.add(VGroup(digits, lbl, chip))

        self.dissolve(tracker)

        with self.beat("s12e") as tracker:
            ok = VGroup(
                callout("better handled indentation and keywords", color=GREEN,
                        size=19),
                pg("make the model's job easier", 18, MUTED),
            ).arrange(DOWN, buff=0.18)
            no = VGroup(
                callout("they do not make generated code correct", color=ROSE,
                        size=19),
                pg("that is not parsing", 18, MUTED),
            ).arrange(DOWN, buff=0.18)
            VGroup(ok, no).arrange(DOWN, buff=0.45).move_to(
                np.array([0.0, 0.45, 0.0]))
            self.play(FadeIn(ok),
                      run_time=rt(tracker.time_until_bookmark("correct") * 0.6))
            self.play(FadeIn(no),
                      run_time=rt(tracker.get_remaining_duration() * 0.6))
            self.keep.add(ok, no)

        self.clear_stage(run_time=0.5)

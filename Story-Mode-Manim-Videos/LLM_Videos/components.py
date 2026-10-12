"""The episode's reusable mobject families.

The storyboard asks for nine named components; they are all here, plus a few
small helpers the scenes share.  Every scene builds its picture out of these,
so a token block looks identical in Scene 02 and Scene 15.

Colour convention (see ``theme``): a token's colour comes from its *index*
using the book's own six-colour cycle, so the same token keeps the same
colour everywhere it appears.
"""
from __future__ import annotations

import numpy as np

from manim import (
    DEGREES, DOWN, LEFT, ORIGIN, RIGHT, UP,
    Arrow, Brace, Circle, Create, DashedLine, DecimalNumber, Dot, Ellipse,
    FadeIn, Integer, LaggedStart, Line, Polygon, Rectangle, RoundedRectangle,
    SurroundingRectangle, Text, VGroup,
)

from theme import (
    AMBER, GREEN, INK, MONO, MUTED, NEON_BLUE, NEON_CYAN, NEON_MAGENTA,
    NEON_VIOLET, PANEL, PANEL_EDGE, ROSE, WHITE, cjk, mono, panel, pg,
    token_color,
)

# ============================================================== 1. TokenBlock


def token_block(text: str, index: int = 0, *, size: int = 24,
                color: str | None = None, fill_opacity: float = 0.20,
                pad_x: float = 0.30, pad_y: float = 0.26,
                show_marks: bool = True) -> VGroup:
    """One token: a coloured box carrying its exact token string.

    ``show_marks`` renders a leading whitespace/boundary marker, which is how
    the book distinguishes ``izing`` (continues the previous token) from
    ``to`` (starts a new word).  Encoding it is the whole point of Scene 07's
    caveat, so it is on by default.
    """
    color = color or token_color(index)
    display = text
    if show_marks and text.startswith(" "):
        display = "\u2423" + text[1:]          # open box = visible space
    label = mono(display, size, INK)
    box = RoundedRectangle(
        corner_radius=0.09,
        width=label.width + pad_x * 2,
        height=label.height + pad_y,
        fill_color=color, fill_opacity=fill_opacity,
        stroke_color=color, stroke_width=2.0,
    )
    label.move_to(box.get_center())
    g = VGroup(box, label)
    g.box, g.label, g.token_text, g.index = box, label, text, index
    return g


def token_row(pieces, *, size: int = 24, buff: float = 0.12,
              start_index: int = 0) -> VGroup:
    """A horizontal run of token blocks, coloured by position."""
    blocks = VGroup(*[
        token_block(p, start_index + i, size=size)
        for i, p in enumerate(pieces)
    ])
    blocks.arrange(RIGHT, buff=buff)
    return blocks


# ============================================================== 2. IdChip


def id_chip(value, *, index: int = 0, size: int = 22,
            color: str | None = None, width: float | None = None) -> VGroup:
    """A token ID: a discrete vocabulary identifier, never a magnitude."""
    color = color or NEON_CYAN
    label = mono(str(value), size, color, "BOLD")
    box = RoundedRectangle(
        corner_radius=0.28,
        width=width or (label.width + 0.40),
        height=label.height + 0.24,
        fill_color=color, fill_opacity=0.14,
        stroke_color=color, stroke_width=1.8,
    )
    label.move_to(box.get_center())
    g = VGroup(box, label)
    g.value, g.label = value, label
    return g


def id_array(values, *, size: int = 22, buff: float = 0.14) -> VGroup:
    """``[27746, 5281]`` as a run of chips inside brackets."""
    chips = VGroup(*[id_chip(v, index=i, size=size) for i, v in enumerate(values)])
    chips.arrange(RIGHT, buff=buff)
    left = mono("[", size + 8, MUTED).next_to(chips, LEFT, buff=0.10)
    right = mono("]", size + 8, MUTED).next_to(chips, RIGHT, buff=0.10)
    g = VGroup(left, chips, right)
    g.chips = chips
    return g


# ============================================================== 3. RawTextTrack


def raw_text_track(text: str, *, size: int = 24, color: str = INK,
                   track_color: str = NEON_CYAN, monospace: bool = False) -> VGroup:
    """The original input string sitting on a measured character track.

    The ruler underneath shows *positions*, not tokens: the lesson is that
    the model never sees these characters at all.
    """
    make = mono if monospace else pg
    label = make(text, size, color)
    rule = Line(LEFT, RIGHT, stroke_color=track_color, stroke_width=1.5).set_width(
        max(label.width + 0.5, 1.0))
    rule.next_to(label, DOWN, buff=0.14)
    ticks = VGroup()
    n = max(len(text), 1)
    for i in range(n + 1):
        x = rule.get_start()[0] + (rule.width * i / n)
        ticks.add(Line(
            np.array([x, rule.get_center()[1] - 0.07, 0.0]),
            np.array([x, rule.get_center()[1] + 0.07, 0.0]),
            stroke_color=track_color, stroke_width=1.0, stroke_opacity=0.45,
        ))
    g = VGroup(label, rule, ticks)
    g.label, g.rule = label, rule
    return g


# ============================================================== 4. VocabularyTable


def vocabulary_table(entries, *, size: int = 22, width: float = 7.4,
                     row_buff: float = 0.20, title: str = "Vocabulary") -> VGroup:
    """Token string -> ID, with the matched rows highlightable.

    ``entries`` is a list of ``(token_string, id_or_None)``.  Passing ``None``
    for an id draws an empty cell, which is how Scene 03 shows an entry the
    vocabulary simply does not have.
    """
    head = pg(title, 20, NEON_CYAN, "BOLD")
    rows = VGroup()
    for tok, ident in entries:
        left = mono(tok, size, INK)
        left.move_to(np.array([-width / 2 + 1.1, 0.0, 0.0]))
        right = (mono(str(ident), size, NEON_CYAN) if ident is not None
                 else mono("\u2014", size, MUTED))
        right.move_to(np.array([width / 2 - 1.1, 0.0, 0.0]))
        rows.add(VGroup(left, right))
    rows.arrange(DOWN, buff=row_buff)

    body = VGroup(head, rows).arrange(DOWN, buff=0.34)
    frame = panel(width + 0.6, body.height + 0.46, color=PANEL_EDGE)
    frame.move_to(body.get_center())
    g = VGroup(frame, body)
    g.rows, g.body = rows, body
    return g


def highlight_row(table: VGroup, index: int, *, color: str = GREEN) -> SurroundingRectangle:
    """A box around one table row, revealed after the match is explained."""
    row = table.rows[index]
    return SurroundingRectangle(
        row, color=color, buff=0.10, corner_radius=0.06, stroke_width=2.0,
    )


# ============================================================== 5. TokenizerMachine


def tokenizer_machine(label: str, method: str, year: str = "",
                      *, width: float = 3.1, height: float = 1.15,
                      color: str = NEON_CYAN, panel_open: bool = False) -> VGroup:
    """One named, trained tokenizer -- a machine, not a method.

    ``method`` is the algorithm or framework; ``label`` is the model whose
    trained tokenizer this is.  Keeping the two visually distinct is what
    stops "BPE" being mistaken for a model.
    """
    body = RoundedRectangle(
        corner_radius=0.14, width=width, height=height,
        fill_color=PANEL, fill_opacity=0.92,
        stroke_color=color, stroke_width=2.2,
    )
    name = pg(label, 20, INK, "BOLD")
    sub = pg(f"{method}{'  ' + year if year else ''}", 14, MUTED)
    stack = VGroup(name, sub).arrange(DOWN, buff=0.10).move_to(body.get_center())
    g = VGroup(body, stack)
    g.name, g.sub = name, sub
    if not panel_open:
        # a frosted window that can be lifted to reveal the segmentation
        glass = Rectangle(
            width=width - 0.34, height=height * 0.46,
            fill_color=NEON_BLUE, fill_opacity=0.16,
            stroke_color=NEON_BLUE, stroke_width=1.0, stroke_opacity=0.5,
        ).move_to(body.get_center())
        g.add(glass)
        g.glass = glass
    return g


# ============================================================== 6. UnknownTokenIndicator


def unknown_token(marker: str = "[UNK]", *, index: int = 0,
                  size: int = 22) -> VGroup:
    """An unknown-token marker: information that cannot be recovered.

    The marker string is rendered exactly as the book prints it -- ``[UNK]``
    for BERT, ``<unk>`` for FLAN-T5.  Flattening those two into one label
    would erase a real difference between the tokenizers.
    """
    label = mono(marker, size, ROSE, "BOLD")
    box = RoundedRectangle(
        corner_radius=0.09,
        width=label.width + 0.34, height=label.height + 0.26,
        fill_color=ROSE, fill_opacity=0.22,
        stroke_color=ROSE, stroke_width=2.0,
    )
    label.move_to(box.get_center())
    g = VGroup(box, label)
    g.marker = marker
    return g


# ============================================================== 7. ByteSequenceView


def byte_sequence(text: str, *, size: int = 18, color: str = AMBER) -> VGroup:
    """UTF-8 bytes of a character, as hex chips.

    Byte-derived pieces cannot be drawn as printable glyphs (the book prints
    them as a replacement character for exactly this reason), so each byte is
    shown as its own hex value and the *joined decode* is what produces the
    visible character.
    """
    raw = text.encode("utf-8")
    chips = VGroup()
    for b in raw:
        lab = mono(f"{b:02X}", size, color)
        box = RoundedRectangle(
            corner_radius=0.08, width=lab.width + 0.26, height=lab.height + 0.20,
            fill_color=color, fill_opacity=0.16,
            stroke_color=color, stroke_width=1.6,
        )
        lab.move_to(box.get_center())
        chips.add(VGroup(box, lab))
    chips.arrange(RIGHT, buff=0.10)
    g = VGroup(chips)
    g.chips = chips
    return g


# ============================================================== 8. ContextSlotMeter


def context_slot_meter(capacity: int, used: int, *, slot: float = 0.46,
                       color: str = NEON_CYAN, used_color: str = GREEN,
                       per_row: int | None = None) -> VGroup:
    """A fixed context container with `used` of `capacity` positions filled.

    Makes the trade-off physical: a finer segmentation fills the container
    sooner, so less text fits.
    """
    per_row = per_row or capacity
    cells = VGroup()
    for i in range(capacity):
        c = Rectangle(
            width=slot, height=slot,
            fill_color=used_color if i < used else PANEL,
            fill_opacity=0.78 if i < used else 0.30,
            stroke_color=used_color if i < used else PANEL_EDGE,
            stroke_width=1.4,
        )
        cells.add(c)
    rows = VGroup()
    for i in range(0, capacity, per_row):
        row = VGroup(*cells[i:i + per_row]).arrange(RIGHT, buff=0.08)
        rows.add(row)
    rows.arrange(DOWN, buff=0.08)
    frame = RoundedRectangle(
        corner_radius=0.10, width=rows.width + 0.26, height=rows.height + 0.26,
        stroke_color=color, stroke_width=1.8, fill_opacity=0.0,
    ).move_to(rows.get_center())
    g = VGroup(frame, rows)
    g.cells, g.used, g.capacity = cells, used, capacity
    return g


# ============================================================== 9. EmbeddingMatrix


def embedding_matrix(rows: int = 6, cols: int = 6, *, cell: float = 0.34,
                     highlight: tuple[int, ...] = (), color: str = NEON_VIOLET,
                     label: str = "Embedding lookup table") -> VGroup:
    """A slab of learned vectors; highlighted rows are the looked-up ones.

    Deliberately a *table of vectors*, not a table of IDs -- the ID only
    selects a row, it carries no magnitude of its own.
    """
    cells = VGroup()
    for r in range(rows):
        row = VGroup()
        for c in range(cols):
            on = r in highlight
            row.add(Rectangle(
                width=cell, height=cell,
                fill_color=color if on else PANEL,
                fill_opacity=0.60 if on else 0.34,
                stroke_color=color if on else PANEL_EDGE,
                stroke_width=1.2 if on else 0.8,
            ))
        row.arrange(RIGHT, buff=0.04)
        cells.add(row)
    cells.arrange(DOWN, buff=0.04)
    frame = RoundedRectangle(
        corner_radius=0.08, width=cells.width + 0.22, height=cells.height + 0.22,
        stroke_color=color, stroke_width=1.8, fill_opacity=0.0,
    ).move_to(cells.get_center())
    title = pg(label, 18, MUTED).next_to(frame, UP, buff=0.16)
    g = VGroup(frame, cells, title)
    g.cells, g.title = cells, title
    return g


# ================================================================= extras ===


def music_note(*, height: float = 1.0, color: str = INK,
               fill_opacity: float = 1.0) -> VGroup:
    """A musical note, drawn as vectors.

    Not a font glyph on purpose.  U+1F3B5 is outside the Basic Multilingual
    Plane, and a render test across every font installed on this machine
    (Consolas, Segoe UI, Segoe UI Emoji, Microsoft YaHei, SimSun, Arial,
    Malgun Gothic) showed Manim's ``Text`` drawing *nothing* for it in all
    seven.  Drawing the shape guarantees it appears, and it scales and tints
    like every other mobject.
    """
    h = height
    head = Ellipse(
        width=h * 0.46, height=h * 0.33,
        fill_color=color, fill_opacity=fill_opacity,
        stroke_color=color, stroke_width=h * 0.05,
    ).rotate(-22 * DEGREES)
    stem = Line(
        np.array([h * 0.19, h * 0.00, 0.0]),
        np.array([h * 0.19, h * 0.92, 0.0]),
        stroke_color=color, stroke_width=h * 0.065,
    )
    flag = Polygon(
        np.array([h * 0.19, h * 0.92, 0.0]),
        np.array([h * 0.55, h * 0.71, 0.0]),
        np.array([h * 0.47, h * 0.88, 0.0]),
        np.array([h * 0.19, h * 0.80, 0.0]),
        fill_color=color, fill_opacity=fill_opacity, stroke_width=0,
    )
    g = VGroup(head, stem, flag)
    g.move_to(ORIGIN)
    return g


def book_sample_line(*, size: int = 16, color: str = NEON_CYAN) -> VGroup:
    """The book's comparison string as a drawable assembly.

    The emoji cannot be a character (see :func:`music_note`), so the line is
    composed from parts rather than one ``Text``.
    """
    parts = VGroup(
        pg("English and CAPITALIZATION", size, INK),
        music_note(height=size / 44.0, color=color),
        cjk("\u9E1F", size=size + 4),
        pg("show_tokens  False  None  elif  ==  >=  else", size, INK),
        pg("two tabs  \"\t\"  12.0*50=600", size, INK),
    ).arrange(RIGHT, buff=0.26)
    frame = RoundedRectangle(
        corner_radius=0.08, width=parts.width + 0.40,
        height=parts.height + 0.26,
        fill_color=color, fill_opacity=0.10,
        stroke_color=color, stroke_width=1.2,
    )
    parts.move_to(frame.get_center())
    return VGroup(frame, parts)


def vocab_bar_chart(data, *, width: float = 8.4, height: float = 2.6,
                    max_value: float | None = None,
                    highlight: tuple[str, ...] = ()) -> VGroup:
    """Real, book-recorded vocabulary sizes as horizontal bars.

    Scene 06 currently speaks about "vocabulary capacity" in the abstract;
    the book publishes an actual number for every tokenizer it discusses, so
    the scene shows those instead.
    """
    max_value = max_value or max(v for _, v, _ in data)
    label_w, value_w = 2.5, 1.3
    bar_zone = width - label_w - value_w
    bars = VGroup()
    for name, value, year in data:
        on = name in highlight
        bar = Rectangle(
            width=max(bar_zone * value / max_value, 0.02), height=height / len(data) * 0.62,
            fill_color=NEON_CYAN if not on else AMBER,
            fill_opacity=0.72 if on else 0.42,
            stroke_width=0,
        )
        name_lbl = pg(f"{name}", 16, INK if on else MUTED)
        name_lbl.move_to(np.array([-width / 2 + label_w / 2, 0.0, 0.0]))
        val_lbl = mono(f"{value:,}", 15, AMBER if on else NEON_CYAN)
        val_lbl.move_to(np.array([width / 2 - value_w / 2, 0.0, 0.0]))
        row = VGroup(name_lbl, bar, val_lbl)
        bar.move_to(np.array([-width / 2 + label_w + bar.width / 2, 0.0, 0.0]))
        row.year = year
        bars.add(row)
    bars.arrange(DOWN, buff=0.10)
    g = VGroup(bars)
    g.rows = bars
    return g


def labelled_arrow(start, end, *, color: str = NEON_CYAN, label: str = "",
                   size: int = 18, buff: float = 0.14) -> VGroup:
    """An arrow with an optional caption, so the caption never overlaps it."""
    arrow = Arrow(start, end, buff=0.0, color=color, stroke_width=3.0,
                  max_tip_length_to_length_ratio=0.10)
    if not label:
        return VGroup(arrow)
    txt = pg(label, size, color)
    txt.next_to(arrow, UP, buff=buff)
    return VGroup(arrow, txt)


def callout(text: str, *, color: str = AMBER, size: int = 18,
            width: float | None = None) -> VGroup:
    """A short explanatory caption in a soft capsule."""
    label = pg(text, size, color)
    if width and label.width > width:
        label.scale(width / label.width)
    box = RoundedRectangle(
        corner_radius=0.10, width=label.width + 0.40, height=label.height + 0.24,
        fill_color=color, fill_opacity=0.10,
        stroke_color=color, stroke_width=1.2,
    )
    label.move_to(box.get_center())
    return VGroup(box, label)


def brace_meter(mob, label: str, *, direction=DOWN, color: str = NEON_CYAN,
                size: int = 18) -> VGroup:
    """A brace under/over `mob` carrying a count -- the token counter."""
    b = Brace(mob, direction=direction, color=color, buff=0.10)
    txt = mono(label, size, color, "BOLD").next_to(b, direction, buff=0.08)
    return VGroup(b, txt)

"""Every value that appears on screen, in one place, with its provenance.

Rule for this episode (from the master prompt): a number is either
``book`` -- printed in *Hands-On Large Language Models*, Chapter 2 -- or
``illus`` -- created for explanation and labelled as such on screen.  Nothing
is invented and then presented as recorded.

Page numbers are book pages.  The PDF's internal numbering is offset by +2
(PDF page 40 == book page 38).

Verified against ``CHAPTER2_BOOK_TEXT_EXTRACT.txt``, which is a verbatim
extraction of the chapter's tokenization half.
"""
from __future__ import annotations

# --------------------------------------------------------------- anchors ---
BOOK = "Hands-On Large Language Models (Alammar & Grootendorst, O'Reilly 2024)"
CHAPTER = "Chapter 2 - Tokens and Embeddings"
SECTION_INPUTS = "How Tokenizers Prepare the Inputs to the Language Model"
SECTION_HOW = "How Does the Tokenizer Break Down Text?"
SECTION_GRANULARITY = "Word Versus Subword Versus Character Versus Byte Tokens"
SECTION_COMPARE = "Comparing Trained LLM Tokenizers"
SECTION_PROPS = "Tokenizer Properties"
PAGES = {
    "inputs": "38-42",
    "how": "43",
    "granularity": "44-45",
    "compare": "46-54",
    "props": "55-56",
    "embeddings_start": "57",
}

# The three determiners of a tokenizer's behaviour (p.43, restated p.55).
THREE_FACTORS = [
    ("Method", "BPE / WordPiece - the algorithm"),
    ("Parameters", "Vocabulary size, special tokens"),
    ("Training data", "Language, code, domain"),
]

# ------------------------------------------------- the recurring sample ----
# The book's own comparison string (p.46).  Stored once, in full, so we never
# compare a short substring against segmentations recorded for the long
# string -- tokenisation depends on surrounding text and whitespace.
BOOK_SAMPLE = (
    "English and CAPITALIZATION\n"
    "\n"
    "\U0001F3B5\u9E1F\n"
    "show_tokens False None elif == >= else: two tabs:\"\t\" Three tabs: \"    \"\n"
    "\n"
    "12.0*50=600\n"
)

# ----------------------------------------------------- Phi-3, the example --
# p.40-41: input_ids tensor [[ 1, 14350, 385, 4876, 27746, 5281, ... ]] with
# the decoded token list beneath it.  Index 4/5 line up with apolog / izing.
PHI3 = {
    "name": "Phi-3 (Llama 2 tokenizer + chat tokens)",
    "provenance": "book",
    "page": "40-41, 53",
    "vocab": 32000,
    "method": "BPE",
    "prompt": ("Write an email apologizing to Sarah for the tragic gardening "
               "mishap. Explain how it happened.<|assistant|>"),
    "word": "apologizing",
    "pieces": [("apolog", 27746), ("izing", 5281)],
    "special_begin": ("<s>", 1),
}

# p.42: the first two generated tokens.
PHI3_DECODE = {
    "provenance": "book",
    "page": "42",
    "pieces": [("Sub", 3323), ("ject", 622)],
    "joined": "Subject",
    "colon": (":", 29901),
}

# --------------------------------------------- the tokenizer comparison -----
# Every entry below is recorded in the book.  `provenance` is 'book' for all
# of them; the *display* is simplified (boundary markers omitted for
# readability) and that simplification is stated on screen.
TOKENIZERS = [
    {
        "key": "bert_uncased",
        "label": "BERT base (uncased)",
        "method": "WordPiece",
        "year": "2018",
        "vocab": 30522,
        "specials": ["[UNK]", "[SEP]", "[PAD]", "[CLS]", "[MASK]"],
        "caps": ["capital", "##ization"],
        "caps_note": "lowercases the input first",
        "emoji": "[UNK]",
        "emoji_marker": "[UNK]",
        "newlines": "dropped - the model is blind to newline structure",
        "four_spaces": ["", " ", " ", " "],
        "elif_token": ["el", "##if"],
        "provenance": "book",
        "page": "47-48",
    },
    {
        "key": "bert_cased",
        "label": "BERT base (cased)",
        "method": "WordPiece",
        "year": "2018",
        "vocab": 28996,
        "specials": ["[UNK]", "[SEP]", "[PAD]", "[CLS]", "[MASK]"],
        "caps": ["CA", "##PI", "##TA", "##L", "##I", "##Z", "##AT", "##ION"],
        "caps_note": "keeps capitals - eight pieces for one word",
        "emoji": "[UNK]",
        "emoji_marker": "[UNK]",
        "newlines": "dropped",
        "four_spaces": ["", " ", " ", " "],
        "elif_token": ["el", "##if"],
        "provenance": "book",
        "page": "48",
    },
    {
        "key": "gpt2",
        "label": "GPT-2",
        # The book calls this "Byte pair encoding (BPE)" and notes that
        # GPT-2/RoBERTa keep bytes in the vocabulary as a *fallback*, while
        # explicitly saying that does not make them tokenization-free
        # byte-level tokenizers.  So: BPE with byte fallback.
        "method": "BPE (byte fallback)",
        "year": "2019",
        "vocab": 50257,
        "specials": ["<|endoftext|>"],
        "caps": ["CAP", "ITAL", "IZ", "ATION"],
        "caps_note": "capitalisation preserved, four pieces",
        "emoji": "byte-derived pieces",
        "emoji_marker": None,
        "newlines": "represented in the tokenizer",
        "four_spaces": None,          # three tokens (220) + one inside the quote
        "elif_token": ["el", "if"],
        "provenance": "book",
        "page": "49",
    },
    {
        "key": "flan_t5",
        "label": "FLAN-T5",
        "method": "SentencePiece",
        "year": "2022",
        "vocab": 32100,
        "specials": ["<unk>", "<pad>", "</s>"],
        "caps": ["CA", "PI", "TAL", "IZ", "ATION"],
        "caps_note": "five pieces; boundary markers not shown",
        "emoji": "<unk>",
        "emoji_marker": "<unk>",
        "newlines": "no newline or whitespace tokens at all",
        "four_spaces": None,
        "elif_token": ["e", "l", "if"],
        "provenance": "book",
        "page": "50",
    },
    {
        "key": "gpt4",
        "label": "GPT-4",
        "method": "BPE",
        "year": "2023",
        "vocab": 100000,              # "a little over 100,000"
        "vocab_label": "a little over 100,000",
        "specials": ["<|endoftext|>", "<|fim_prefix|>", "<|fim_middle|>", "<|fim_suffix|>"],
        "caps": ["CAPITAL", "IZATION"],
        "caps_note": "two pieces - fewer than its ancestor",
        "emoji": "byte-derived pieces",
        "emoji_marker": None,
        "newlines": "represented in the tokenizer",
        "four_spaces": ["    "],       # a single token for four spaces
        "elif_token": ["elif"],        # the keyword owns a token
        "provenance": "book",
        "page": "50-51",
    },
]

# The subset shown side by side in the episode.  The book compares eight
# trained tokenizers; showing four is a deliberate simplification and the
# scene says so on screen.
COMPARISON_KEYS = ["bert_uncased", "gpt2", "flan_t5", "gpt4"]

# Book-recorded vocabulary sizes for the bar chart (pp.47-54).
VOCAB_SIZES = [
    ("BERT cased", 28996, "2018"),
    ("BERT uncased", 30522, "2018"),
    ("Phi-3", 32000, "2024"),
    ("FLAN-T5", 32100, "2022"),
    ("StarCoder2", 49152, "2024"),
    ("Galactica", 50000, "2023"),
    ("GPT-2", 50257, "2019"),
    ("GPT-4", 100000, "2023"),
]

# --------------------------------------------- byte fallback / emoji ------
GPT2_EMOJI = {
    "provenance": "book",
    "page": "49",
    "char": "\U0001F3B5",             # musical note
    "ids": [8582, 236, 113],
    "note": "tokenizer.decode([8582, 236, 113]) prints the note back",
    # The book says the Chinese character is also represented by several
    # tokens, but prints NO ids for it -- so the episode shows none.
    "other_char": "\u9E1F",
    "other_ids": None,
}

# --------------------------------------------------------- code scene -----
# p.56: the book's own code example.  The four dots are the book's rendering
# of the four indentation spaces.
CODE_SAMPLE = {
    "provenance": "book",
    "page": "56",
    "lines": ["def add_numbers(a, b):", '...."""Add the two numbers `a` and `b`."""', "....return a + b"],
    "indent": 4,
    "indent_marker": "\u00b7",
    "note": "the four dots reveal four spaces; they are not literal code characters",
}

# ------------------------------------------------------- misc anchors -----
WORD_VS_SUBWORD = {
    "provenance": "book",
    "page": "44",
    # The book's own word-level example, and the subword rescue of it.
    "word_family": ["apology", "apologize", "apologetic", "apologist"],
    "stem": "apolog",
    "suffixes": ["-y", "-ize", "-etic", "-ist"],
    "char_example": "play",
    "chars": ["p", "l", "a", "y"],
    "chars_per_token": "subword tokens often average three characters per token",
    "context": "with a context length of 1,024, roughly three times as much text fits",
}

# The play/player/playing family used to *teach* reuse.  This is NOT the
# book's example -- the book's is the apology family above -- so it is
# labelled illustrative on screen and paired with the book-grounded pass.
PLAY_FAMILY = {
    "provenance": "illus",
    "words": [("play", ["play"]),
              ("player", ["play", "er"]),
              ("playing", ["play", "ing"])],
    "unseen": ("playful", ["play", "ful"]),
}

# Scene 01's prompt.  Original, invented for the hook.
HOOK_PROMPT = {
    "provenance": "illus",
    "text": "What is the capital of India?",
}

# Scene 02's toy vocabulary lookup.  Deliberately far away from every real id
# in the book so it can never be mistaken for a recorded output.
TOY_LOOKUP = {
    "provenance": "illus",
    "word": "Hello!",
    "pieces": [("Hello", 42), ("!", 91)],
}

# Scene 13's context budget.  Invented to make the trade-off visible.
CONTEXT_DEMO = {
    "provenance": "illus",
    "capacity": 12,
    "fine_grained_used": 11,
    "coarse_used": 6,
}

# --------------------------------------------- the episode's own text -----
EPISODE_TITLE = "The Secret Language of LLMs"
EPISODE_SUBTITLE = "Tokenisation: how text becomes numbers"

# Scene 15's closing bridge, from the book (p.57).
TOKENIZER_LOCK = ("A pretrained language model is linked to its tokenizer "
                  "and cannot use a different one without training.")

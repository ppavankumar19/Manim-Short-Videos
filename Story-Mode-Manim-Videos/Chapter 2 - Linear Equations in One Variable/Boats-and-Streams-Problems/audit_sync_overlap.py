"""Sync & overlap audit harness for two_digit_puzzles_story.py.

Replays the scene headlessly:
  - fakes self.voiceover() with REAL per-beat audio durations and per-bookmark
    word timings recovered from the rendered TwoDigitPuzzlesStory.real.srt,
  - fakes self.play() by running manim's own _setup_scene/begin/interpolate/
    clean_up_from_scene bookkeeping (so the scene's visible mobject set at
    each step is exactly what a real render would show), then
  - at every play boundary, checks every pair of visible mobjects for
    bounding-box overlaps (partial overlaps and text-in-text containment
    are flagged; intentional frame-around-text containment is whitelisted),
  - and per narration piece, reports how much the animation run-time
    overshoots the audio (sync stretch).

Run from the topic folder:
    .venv/Scripts/python.exe audit_sync_overlap.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
_ROOT = next(p for p in _HERE.parents
        if (p / "speech_service.py").exists())
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from manim import config  # noqa: E402
config.renderer = "cairo"
config.disable_caching = True

from manim import (  # noqa: E402
    Arrow, Circle, DoubleArrow, Ellipse, Line, MathTex, Polygon, Rectangle, VGroup,
    RoundedRectangle, Sector, SurroundingRectangle, Text, Dot,
)
from manim.animation.animation import prepare_animation  # noqa: E402

from upstream_downstream_story import (  # noqa: E402
    BOARD_LEFT, BOARD_RIGHT, BOARD_BOTTOM, BOARD_TOP, BOARD_CX, NARRATION,
    UpstreamDownstreamStory,
)

# ---------------------------------------------------------------- SRT data ---
SRT = (_HERE / "media" / "videos" / "upstream_downstream_story" / "360p30"
       / "UpstreamDownstreamStory.real.srt")

PIECE_ORDER = [
    "title", "scene1", "scene2", "scene3", "scene4", "scene5", "scene6",
    "scene7", "scene8", "scene9_setup", "scene9_reveal", "scene10",
]
PIECE_ANCHORS = {
    "title": "today we solve a puzzle",
    "scene1": "look at this river",
    "scene2": "let the boat's own speed",
    "scene3": "now the boat turns around",
    "scene4": "now let's bring in the times",
    "scene5": "here is the key idea",
    "scene6": "now we solve it",
    "scene7": "let's check that answer",
    "scene8": "here is the method",
    "scene9_setup": "your turn a boat covers",
    "scene9_reveal": "downstream the effective speed",
    "scene10": "let's summarise",
}


def norm_word(w: str) -> str:
    return re.sub(r"[^a-z0-9']", "", w.lower())


def parse_srt() -> list[tuple[str, float]]:
    """Return a flat (word, start_time) stream from the rendered SRT."""
    entries: list[tuple[float, float, str]] = []
    lines = SRT.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        m = re.match(r"(\d\d):(\d\d):(\d\d),(\d\d\d) --> "
                     r"(\d\d):(\d\d):(\d\d),(\d\d\d)", line)
        if m:
            def secs(g: int) -> float:
                return (int(m.group(g)) * 3600 + int(m.group(g + 1)) * 60
                        + int(m.group(g + 2)) + int(m.group(g + 3)) / 1000)
            start, end = secs(1), secs(5)
            text = ""
            j = i + 1
            while j < len(lines) and lines[j].strip() and " --> " not in lines[j]:
                text += " " + lines[j].strip()
                j += 1
            entries.append((start, end, text.strip()))
            i = j
        else:
            i += 1
    stream: list[tuple[str, float]] = []
    for start, end, text in entries:
        words = text.split()
        dur = max(end - start, 0.001)
        for k, w in enumerate(words):
            stream.append((w, start + dur * k / len(words)))
    return stream


def piece_bounds(stream) -> dict[str, dict]:
    words = [w for w, _ in stream]
    times = [t for _, t in stream]
    norm = [norm_word(w) for w in words]
    starts: dict[str, int] = {}
    for piece in PIECE_ORDER:
        anchor = PIECE_ANCHORS[piece].split()
        for idx in range(len(norm) - len(anchor) + 1):
            if norm[idx:idx + len(anchor)] == anchor:
                starts[piece] = idx
                break
        else:
            raise RuntimeError(f"anchor not found for {piece}")
    order = sorted(PIECE_ORDER, key=lambda p: starts[p])
    bounds = {}
    for k, piece in enumerate(order):
        s = starts[piece]
        e = starts[order[k + 1]] if k + 1 < len(order) else len(words)
        piece_words = words[s:e]
        piece_times = times[s:e]
        dur = (piece_times[-1] - piece_times[0]) if piece_times else 0.0
        bounds[piece] = {"words": piece_words, "times": piece_times,
                         "start": piece_times[0], "dur": dur}
    return bounds


def bookmark_times(text: str, wb: dict) -> dict[str, float]:
    """Replicate the Gemini/manim-voiceover word mapping: bookmark char
    offset in the bookmark-stripped text -> first word at/after it."""
    cleaned = re.sub(r"<bookmark mark='[^']+'/>", "", text)
    tokens = list(re.finditer(r"\S+", cleaned))
    if not tokens:
        return {}
    marks: dict[str, float] = {}
    removed = 0
    for m in re.finditer(r"<bookmark mark='([^']+)'/>", text):
        cleaned_pos = m.start() - removed
        removed += len(m.group(0))
        # find the first word at/after the bookmark's char offset
        word_idx = 0
        for tok in tokens:
            if tok.start() >= cleaned_pos:
                break
            word_idx += 1
        if word_idx < len(wb["times"]):
            marks[m.group(1)] = wb["times"][word_idx] - wb["times"][0]
        else:
            marks[m.group(1)] = wb["dur"]
    return marks


# ------------------------------------------------------------- harness -------
FRAME_TYPES = (Rectangle, RoundedRectangle, SurroundingRectangle, Circle, Line,
               Arrow, DoubleArrow, Polygon, Sector, Ellipse, Dot)


def is_texty(mobj) -> bool:
    for m in mobj.get_family():
        if isinstance(m, Text):
            return True
        if hasattr(m, "tex_string"):
            return True
    return False


AREA_FRAMES = (Rectangle, RoundedRectangle, SurroundingRectangle, Circle,
               Ellipse, Polygon, Sector)
LINE_FRAMES = (Line, Arrow, DoubleArrow, Dot)


def frame_kind(mobj):
    """'area' / 'line' if mobject is a pure frame (no text), else None.
    Composite icons (boxes + dials + planks) count as 'area' containers."""
    fam = mobj.get_family()
    if any(isinstance(m, Text) or hasattr(m, "tex_string") for m in fam):
        return None
    if any(isinstance(m, AREA_FRAMES) for m in fam):
        return "area"
    if any(isinstance(m, LINE_FRAMES) for m in fam):
        return "line"
    return None


def is_think_badge(mobj) -> bool:
    return any(isinstance(m, Text) and m.text.startswith("THINK")
               for m in mobj.get_family())


def content_leaves(mobj) -> list:
    """Flatten a mobject into the parts that are actually seen: text units
    (Text objects and MathTex parts) and individual frames (boxes, arrows...).
    Container groups are never compared as a whole -- a VGroup holding three
    arrows has a bbox spanning the whole row, which produced false hits."""
    if isinstance(mobj, (Text,)) or (hasattr(mobj, "tex_string")
                                     and not isinstance(mobj, VGroup)):
        return [mobj]
    leaves, seen = [], set()
    for x in mobj.get_family():
        if x is mobj:
            continue
        leaf = isinstance(x, Text) or hasattr(x, "tex_string")
        if not leaf:
            leaf = frame_kind(x) is not None and not isinstance(x, (MathTex, Text))
        if leaf and is_decor(x):
            continue          # drop-shadow copies are decoration, not content
        if leaf and id(x) not in seen:
            leaves.append(x)
            for d in x.get_family():   # don't re-add a leaf's own parts
                seen.add(id(d))
    return leaves or [mobj]


def is_decor(mobj) -> bool:
    """True for the dimmed black copies made by drop_shadow()."""
    try:
        return (mobj.get_stroke_width() == 0
                and mobj.get_fill_opacity() < 0.5)
    except Exception:
        return False


def describe(mobj) -> str:
    fam = mobj.get_family()
    txt = next((getattr(m, "tex_string", "") or getattr(m, "text", "")
                for m in fam
                if isinstance(m, Text) or hasattr(m, "tex_string")), "")
    if txt:
        txt = txt[:26].replace("\n", " ")
    c = mobj.get_center()
    return f"{type(mobj).__name__}({txt!r}) @({c[0]:.2f},{c[1]:.2f})"


class Harness:
    def __init__(self, scene: UpstreamDownstreamStory):
        self.scene = scene
        self.clock = 0.0
        self.piece = "GAP"
        self.step = 0
        self.reports: list[str] = []
        self.sync: list[dict] = []
        stream = parse_srt()
        self.bounds = piece_bounds(stream)
        # bookmark times per piece (absolute scene time computed on entry)
        self.piece_mark_times: dict[str, float] = {}
        for piece in PIECE_ORDER:
            self.piece_mark_times[piece] = bookmark_times(NARRATION[piece],
                                                          self.bounds[piece])

    # -- fake voiceover -----------------------------------------------------
    def _enter_piece(self, text: str) -> None:
        for piece in PIECE_ORDER:
            if NARRATION[piece] == text:
                self.piece = piece
                break
        else:
            self.piece = "UNKNOWN"
        self.piece_start = self.clock
        self.piece_play_time = 0.0
        self.piece_dur = self.bounds[self.piece]["dur"] if self.piece in self.bounds else 0.0
        self.piece_marks_abs = {
            mark: self.piece_start + rel
            for mark, rel in self.piece_mark_times.get(self.piece, {}).items()
        }
        # inventory of text still on the board when this beat starts
        scene = self.scene
        skip = {id(getattr(scene, n, None)) for n in
                ("bg", "student", "teacher", "badge", "badge_l")}
        leftovers = [describe(m) for m in scene.mobjects
                     if id(m) not in skip and is_texty(m)]
        print(f"[{self.piece:14s}] start board: {len(leftovers)} text mobjects"
              + ((" -> " + "; ".join(leftovers[:6])) if leftovers else ""))

    def _exit_piece(self) -> None:
        stretch = self.piece_play_time - self.piece_dur
        self.sync.append({
            "piece": self.piece,
            "audio": round(self.piece_dur, 2),
            "anim": round(self.piece_play_time, 2),
            "stretch": round(max(0.0, stretch), 2),
        })
        self.piece = "GAP"

    def tracker(self):
        h = self

        class FakeTracker:
            data = {"word_boundaries": []}

            def time_until_bookmark(tself, mark: str) -> float:
                t_abs = h.piece_marks_abs.get(mark, h.piece_start)
                return max(0.0, t_abs - h.clock)

            def get_remaining_duration(tself) -> float:
                return max(0.0, (h.piece_start + h.piece_dur) - h.clock)

        return FakeTracker()

    def voiceover_cm(self, text: str):
        h = self

        class CM:
            def __enter__(cm_self):
                h._enter_piece(text)
                return h.tracker()

            def __exit__(cm_self, *exc):
                h._exit_piece()

        return CM()

    # -- fake play / wait ---------------------------------------------------
    def play(self, *args, run_time: float = 1.0, **kwargs):
        animations = [prepare_animation(a) for a in args]
        self.scene.add_mobjects_from_animations(animations)
        for a in animations:
            a._setup_scene(self.scene)
            a.begin()
        for a in animations:
            a.interpolate(1)
            a.clean_up_from_scene(self.scene)
        self.clock += float(run_time)
        if self.piece != "GAP":
            self.piece_play_time += float(run_time)
        self.step += 1
        self.check_overlaps()

    def wait(self, duration: float = 1.0, **kwargs):
        self.clock += max(0.0, float(duration))

    # -- overlap checks -----------------------------------------------------
    def check_overlaps(self):
        scene = self.scene
        skip = {id(getattr(scene, n, None)) for n in
                ("bg", "student", "teacher", "badge", "badge_l")}
        mobs = []
        for m in scene.mobjects:
            if id(m) in skip or is_think_badge(m):
                continue          # the challenge clock intentionally covers the board
            mobs.extend(content_leaves(m))
        for i in range(len(mobs)):
            for j in range(i + 1, len(mobs)):
                a, b = mobs[i], mobs[j]
                if is_think_badge(a) or is_think_badge(b):
                    continue  # the challenge clock intentionally covers the board
                ax0, ay0, ax1, ay1 = self.bbox(a)
                bx0, by0, bx1, by1 = self.bbox(b)
                ix = min(ax1, bx1) - max(ax0, bx0)
                iy = min(ay1, by1) - max(ay0, by0)
                if ix <= 0 or iy <= 0:
                    continue
                inter = ix * iy
                area_a = max((ax1 - ax0) * (ay1 - ay0), 1e-6)
                area_b = max((bx1 - bx0) * (by1 - by0), 1e-6)
                small = min(area_a, area_b)
                ratio = inter / small
                if ratio < 0.02:
                    continue
                a_text, b_text = is_texty(a), is_texty(b)
                ka, kb = frame_kind(a), frame_kind(b)
                flag = None
                if a_text and b_text:
                    contained = ratio >= 0.9
                    if contained:
                        flag = "TEXT-IN-TEXT"
                    else:
                        flag = f"PARTIAL {ratio:.0%}"
                elif (a_text and kb == "line") or (b_text and ka == "line"):
                    # a label sitting on top of an arrow is a real collision
                    if ratio >= 0.06:
                        flag = f"TEXT-ON-ARROW {ratio:.0%}"
                # text inside/near area frames (boxes, highlights) is by design
                if flag:
                    self.reports.append(
                        f"[{self.piece:12s} step {self.step:2d}] {flag:12s} "
                        f"{describe(a)}  <->  {describe(b)}")
        # board bounds
        for m in mobs:
            x0, y0, x1, y1 = self.bbox(m)
            # the countdown dim veil is a full-frame rectangle by design
            if isinstance(m, Rectangle) and (x1 - x0) > config.frame_width * 0.95:
                continue
            if x0 < BOARD_LEFT + 0.12 or x1 > BOARD_RIGHT - 0.12 or y1 > BOARD_TOP - 0.05:
                self.reports.append(
                    f"[{self.piece:12s} step {self.step:2d}] OUT-OF-BOARD "
                    f"{describe(m)}")
            if y0 < BOARD_BOTTOM + 0.55 and not is_texty(m):
                pass
            # the two corner badges live on the top strip: nothing else may
            # reach into them (a long heading once overlapped the badge)
            if (y1 > BOARD_TOP - 0.85
                    and (x1 > BOARD_RIGHT - 1.15 or x0 < BOARD_LEFT + 1.15)):
                self.reports.append(
                    f"[{self.piece:12s} step {self.step:2d}] NEAR-BADGE "
                    f"{describe(m)}")
        # centre alignment: the board's centrepiece (equations, machine rows)
        # must sit on BOARD_CX. Wide left-aligned lists are reported for review.
        for m in scene.mobjects:
            if id(m) in skip:
                continue
            x0, y0, x1, y1 = self.bbox(m)
            width = x1 - x0
            if width < 1.6:
                continue
            if isinstance(m, Rectangle) and width > config.frame_width * 0.95:
                continue
            cx = (x0 + x1) / 2
            off = abs(cx - BOARD_CX)
            if off > 0.35:
                self.reports.append(
                    f"[{self.piece:12s} step {self.step:2d}] OFF-CENTRE  "
                    f"dx={cx - BOARD_CX:+.2f} span=[{x0:+.2f}..{x1:+.2f}] "
                    f"{describe(m)}")

    @staticmethod
    def bbox(mobj):
        ul = mobj.get_corner([-1, 1, 0])
        dr = mobj.get_corner([1, -1, 0])
        return ul[0], dr[1], dr[0], ul[1]


def main() -> None:
    scene = UpstreamDownstreamStory()
    h = Harness(scene)

    # monkeypatch
    scene.voiceover = lambda text=None, **kw: h.voiceover_cm(text)
    scene.play = h.play
    scene.wait = h.wait
    scene.add_sound = lambda *a, **k: None
    scene.set_speech_service = lambda *a, **k: None
    scene._capture_srt = lambda *a, **k: None
    scene._write_real_srt = lambda: None

    scene.construct()

    print("\n===== SYNC (animation time vs audio duration per beat) =====")
    total_anim = total_audio = total_stretch = 0.0
    for row in h.sync:
        flag = "  <<< STRETCH" if row["stretch"] > 0.35 else ""
        print(f"{row['piece']:14s} audio={row['audio']:6.2f}s "
              f"anim={row['anim']:6.2f}s stretch={row['stretch']:5.2f}s{flag}")
        total_audio += row["audio"]
        total_anim += row["anim"]
        total_stretch += row["stretch"]
    print(f"{'TOTAL':14s} audio={total_audio:6.2f}s anim={total_anim:6.2f}s "
          f"stretch={total_stretch:5.2f}s   (video time incl. gaps ~ {h.clock:.1f}s)")

    print("\n===== OVERLAPS =====")
    seen = set()
    for r in h.reports:
        if r not in seen:
            print(r)
            seen.add(r)
    if not h.reports:
        print("(none)")


if __name__ == "__main__":
    main()

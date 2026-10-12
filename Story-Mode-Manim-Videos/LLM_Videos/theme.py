"""Chapter 2 - Episode 1: "The Secret Language of LLMs".

Theme, type scale, safe area, and the base scene class.

The visual language is *not* the chalkboard used by the Story-Mode maths
series: this episode sits on the neon tech backdrop that already ships in
``LLM_Videos/assets/background.png`` (a glass panel with a cyan -> violet
rim, over a reflective floor).  Every colour below is sampled from that
artwork so drawn content reads as part of the panel rather than on top of it.

Two things make this episode different from the maths videos:

* Base class is ``ThreeDScene`` *and* ``VoiceoverScene``.  ``ThreeDScene``
  gives us a perspective camera for the 3D shots; ``VoiceoverScene`` gives
  us per-beat narration.  The MRO was smoke-tested before any scene was
  written.
* Narration timings are real per-word offsets, not the character-count
  estimate the Gemini TTS path produces -- see ``audio.py``.

3D note (important): in Manim CE, ``ThreeDCamera.get_mobjects_to_display``
sorts mobjects whose ``shade_in_3d`` is set (i.e. ``Surface``/``Sphere``/
``Polyhedron``) to the *back*, and every ordinary mobject to the front.  So
3D geometry here is built from plain ``Polygon``/``Rectangle``/``Line``/
``Text`` placed at real ``z`` coordinates: they are still perspective
projected by the camera, but they keep their ``z_index`` ordering against
the backdrop.  Avoid ``Surface``/``Sphere`` in this episode.
"""
from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path

import numpy as np

from manim import (
    DOWN, LEFT, ORIGIN, RIGHT, UP, DEGREES,
    Group, ImageMobject, Line, Rectangle, RoundedRectangle, Text, VGroup,
    FadeIn, FadeOut, config, logger,
)
from manim_voiceover import VoiceoverScene
from manim_voiceover.tracker import AUDIO_OFFSET_RESOLUTION

from manim import ThreeDScene

from audio import VOICEOVER_DIR, HybridZephyrSpeechService

# ------------------------------------------------------------------ paths ---
HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
BACKGROUND = ASSETS / "background.png"

# ----------------------------------------------------------------- theme ---
# Sampled from assets/background.png.
BG_DEEP = "#04101F"          # outside the glass panel
PANEL = "#0A2140"            # panel glass
PANEL_EDGE = "#1B4B7A"
INK = "#EAF4FF"              # primary prose
MUTED = "#8FB3D9"            # secondary prose / axis labels
NEON_CYAN = "#22D3EE"        # primary accent / raw text
NEON_BLUE = "#3B82F6"
NEON_VIOLET = "#8B5CF6"      # learned parameters (embeddings)
NEON_MAGENTA = "#E879F9"
AMBER = "#FBBF24"            # byte / fallback / warnings
ROSE = "#FB7185"             # unknown token / information loss
GREEN = "#34D399"            # success / verified
WHITE = "#FFFFFF"

# The book's own six-colour token cycle (Chapter 2, page 46, `colors_list`).
# Using the book's palette for token blocks keeps the video visually
# consistent with the printed tokenizer comparisons.
TOKEN_COLORS = [
    "#66C2A5",  # 102;194;165
    "#FC8D62",  # 252;141;98
    "#8DA0CB",  # 141;160;203
    "#E78AC3",  # 231;138;195
    "#A6D854",  # 166;216;84
    "#FFD92F",  # 255;217,47
]


def token_color(i: int) -> str:
    """The book's colour cycle, so token i is always the same colour."""
    return TOKEN_COLORS[i % len(TOKEN_COLORS)]


# ---------------------------------------------------------------- type -----
# The series font.  Every one of the 25 existing Story-Mode videos uses
# Segoe Print, so this episode does too -- including token strings and code,
# for a single consistent voice across the channel.  (It is wider than
# Consolas was, which is why several rows needed re-fitting.)
FONT = "Segoe Print"
MONO = "Segoe Print"


def pg(s: str, size: int = 26, color: str = INK, weight: str = "NORMAL") -> Text:
    """Prose."""
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def mono(s: str, size: int = 26, color: str = INK, weight: str = "NORMAL") -> Text:
    """Token strings, token IDs and code.

    Same face as the prose, matching the rest of the series.  Whitespace is
    never expressed with a character -- see :func:`space_marker`.
    """
    return Text(s, font=MONO, font_size=size, color=color, weight=weight)


#: CJK: neither Segoe Print nor Calibri carries Han characters on this
#: machine, and Microsoft YaHei does.
CJK_FONT = "Microsoft YaHei"


def cjk(s: str, size: int = 26, color: str = INK, weight: str = "NORMAL") -> Text:
    """Han / kana text, which the prose and mono faces do not cover."""
    return Text(s, font=CJK_FONT, font_size=size, color=color, weight=weight)


def space_marker(height: float, color: str, *, width_ratio: float = 0.34) -> Rectangle:
    """A drawn marker standing in for a space inside a token.

    U+2423 OPEN BOX was the obvious character, but measured across Segoe
    Print, Calibri and Consolas it has an advance width of 0.04 units at
    font_size 26 -- i.e. it is not really there, and it renders as nothing.
    Drawing the mark guarantees it appears in every font.
    """
    return Rectangle(
        width=height * width_ratio, height=height * 0.62,
        stroke_color=color, stroke_width=1.2,
        fill_color=color, fill_opacity=0.22,
    )


# ----------------------------------------------------------- safe area -----
# Measured from the backdrop, not eyeballed.  `_measure_panel.py` profiles
# the artwork and finds the neon rim's core at x = -6.04 / +6.03 and
# y = +3.25 / -2.14 (image pixels -> Manim frame).  Everything drawn must sit
# inside that rounded rectangle; the reflective floor below it is reserved
# for the burned-in subtitles and carries no content.
#
# 0.45 of margin is kept off the rim so nothing touches the glow or the
# curved corners.
SAFE_L, SAFE_R = -5.58, 5.58
SAFE_B, SAFE_T = -1.82, 2.90
TITLE_Y = 2.48
CONTENT_CY = 0.45
SAFE_W = SAFE_R - SAFE_L
SAFE_H = SAFE_T - SAFE_B

# The source-fidelity chips required by the master prompt: every original
# example must be visibly marked as invented, and every book value as
# recorded.  A viewer should never have to guess which is which.
# ---- layout audit tuning (see LLMScene._audit) ----
AUDIT_LAYOUT = os.environ.get("LLM_LAYOUT_AUDIT", "") in ("1", "2")
OUT_TOL = 0.06        # frame units of slack before 'outside' is reported
OVERLAP_FRAC = 0.12   # share of the smaller box before 'overlap' is reported
AUDIT_VERBOSE = os.environ.get("LLM_LAYOUT_AUDIT") == "2"   # include box coordinates


def _box_contains(outer, inner) -> bool:
    """Does `inner` sit entirely within `outer`?"""
    return (outer[0] <= inner[0] and outer[1] <= inner[1]
            and outer[2] >= inner[2] and outer[3] >= inner[3])


def _is_highlight_box(rect, rect_box, other_leaves) -> bool:
    """A hollow rectangle wrapping one item of a list is a highlight.

    Scene 14's answer box and the chart-row highlights are markers, not
    collisions: they contain at least one text leaf of the other group while
    the group itself stays outside.
    """
    from manim import Rectangle, RoundedRectangle
    if not isinstance(rect, (Rectangle, RoundedRectangle)):
        return False
    try:
        if rect.get_fill_opacity() > 0.05:
            return False
    except Exception:  # noqa: BLE001
        return False
    return any(b is not None and _box_contains(rect_box, b)
               for b in other_leaves)
OVERLAP_IGNORE_GLYPHS = True   # two glyphs of the same phrase are not a clash

CHIP_BOOK = ("BOOK-RECORDED", NEON_CYAN)
CHIP_ILLUS = ("ILLUSTRATIVE", AMBER)


# ------------------------------------------------------------- helpers -----
def panel(width: float, height: float, *, color: str = PANEL_EDGE,
          fill: str = PANEL, fill_opacity: float = 0.72,
          stroke_width: float = 1.6, radius: float = 0.16) -> RoundedRectangle:
    """A glass card sized for the backdrop panel."""
    return RoundedRectangle(
        corner_radius=radius, width=width, height=height,
        fill_color=fill, fill_opacity=fill_opacity,
        stroke_color=color, stroke_width=stroke_width,
    )


def source_chip(kind: str, *, scale: float = 1.0) -> VGroup:
    """Bottom-right 'BOOK-RECORDED' / 'ILLUSTRATIVE' provenance chip."""
    label, color = CHIP_BOOK if kind == "book" else CHIP_ILLUS
    txt = pg(label, 13, color, "BOLD")
    frame = RoundedRectangle(
        corner_radius=0.06, width=txt.width + 0.26, height=txt.height + 0.16,
        stroke_color=color, stroke_width=1.1,
        fill_color=color, fill_opacity=0.10,
    )
    txt.move_to(frame.get_center())
    g = VGroup(frame, txt)
    if scale != 1.0:
        g.scale(scale)
    return g.move_to(np.array([SAFE_R - g.width / 2, SAFE_B + 0.16, 0.0]))


def title_bar(text: str, *, color: str = NEON_CYAN) -> VGroup:
    """Scene title inside the panel's top edge, with a hairline rule."""
    label = pg(text, 25, color, "BOLD").move_to(np.array([0.0, TITLE_Y, 0.0]))
    rule = Line(
        np.array([SAFE_L + 0.10, TITLE_Y - 0.30, 0.0]),
        np.array([SAFE_R - 0.10, TITLE_Y - 0.30, 0.0]),
        stroke_color=color, stroke_width=1.0, stroke_opacity=0.35,
    )
    return VGroup(label, rule)


def caption_hint(text: str, y: float | None = None) -> Text:
    """A one-line takeaway pinned above the subtitle strip."""
    label = pg(text, 22, AMBER, "BOLD")
    return label.move_to(np.array([0.0, SAFE_B + 0.62 if y is None else y, 0.0]))


def fit(mob, max_width: float = SAFE_W - 0.4):
    """Shrink in place until it fits the safe width.  Measure, never guess."""
    if mob.width > max_width:
        mob.scale(max_width / mob.width)
    return mob


def rt(seconds: float, floor: float = 0.05) -> float:
    """A run_time that can never be zero or negative."""
    return max(float(seconds), floor)


# ------------------------------------------------------- base scene --------
class LLMScene(ThreeDScene, VoiceoverScene):
    """Base for every act of this episode.

    Provides the backdrop, the narration service, and the ground-truth SRT
    capture that the house pipeline (``pipeline_360.py``) verifies and burns.
    """

    #: set by each act so the SRT lands in the right media folder
    module_stem: str = "chapter2_ep1"
    #: ``{beat_key: narration_text}`` -- set by each act class
    narration: dict = {}

    def construct(self) -> None:  # pragma: no cover - overridden
        raise NotImplementedError

    @contextmanager
    def beat(self, key: str):
        """Run one narrated beat and always record its captions.

        Using ``self.voiceover`` directly and remembering to call
        ``capture_srt`` per beat is a trap: the first Act I render shipped
        with captions for only 9 of its 19 beats, because the beats that did
        not happen to end with a provenance chip were never captured.  Going
        through this wrapper makes the caption unconditional.
        """
        with self.voiceover(text=self.narration[key]) as tracker:
            yield tracker
        self.capture_srt(tracker)

    # -- setup ----------------------------------------------------------
    def setup_episode(self) -> None:
        """Narration service + per-run state.

        The voice cache is pinned to this folder's ``media/voiceovers`` (not
        ``config.media_dir``), so switching the movie output between D:\\m3
        and a local media dir never re-synthesises 20 minutes of audio.
        """
        self.voice = HybridZephyrSpeechService(cache_dir=VOICEOVER_DIR)
        self.set_speech_service(self.voice, create_subcaption=False)
        self._srt_entries: list[tuple[float, float, str]] = []
        self.backdrop: Group | None = None
        self._audit_issues: list[str] = []
        self._audit_n = 0
        self.keep = VGroup()      # per-beat content; cleared on each cut
        self.stage = VGroup()     # scene-long props; cleared at scene end
        self.chrome = VGroup()    # scene title etc; cleared at scene end

    def scene_title(self, text: str, *, color: str = NEON_CYAN):
        """The scene's title bar: pinned to the frame and kept all scene.

        Kept out of ``self.keep`` on purpose.  ``VGroup[:1]`` slices the
        *family* (every glyph), not the top-level members, so using a slice
        to say "keep the title" would have faded exactly one letter of it.
        """
        bar = self.hud(title_bar(text, color=color))
        self.chrome.add(bar)
        return bar

    def add_backdrop(self, *, dim: float = 0.0) -> ImageMobject:
        """The supplied neon panel, full frame, behind everything.

        *Fixed in frame* on purpose.  A normal mobject gets projected by
        ThreeDCamera, so the entire backdrop swings away with the camera
        during a 3D shot (verified: the panel tilted into a plane).  Fixed
        mobjects skip that projection, and because neither they nor ordinary
        geometry is ``shade_in_3d``, the camera still orders everything by
        ``z_index`` -- which is what keeps this at the back.
        """
        bg = ImageMobject(str(BACKGROUND))
        bg.stretch_to_fit_width(config.frame_width)
        bg.stretch_to_fit_height(config.frame_height)
        bg.move_to(ORIGIN)
        bg.set_z_index(-100)
        self.add(bg)
        self.hud(bg)
        layers = Group(bg)
        if dim:
            veil = Rectangle(
                width=config.frame_width, height=config.frame_height,
                fill_color=BG_DEEP, fill_opacity=dim, stroke_width=0,
            ).move_to(ORIGIN)
            veil.set_z_index(-90)
            self.add(veil)
            self.hud(veil)
            layers.add(veil)
        # protected from every stage clear, for the whole episode.
        # Group, not VGroup: VGroup only accepts VMobjects, and the backdrop
        # is an ImageMobject.
        self.backdrop = Group(bg)
        return bg

    def hud(self, *mobjects):
        """Pin mobjects to the screen so they survive a camera move.

        Titles, provenance chips and footer lines are chrome: they belong to
        the frame, not to the 3D world.  This only marks them as fixed -- it
        does not add them -- so a later ``FadeIn`` still animates them in.
        """
        add = getattr(self.camera, "add_fixed_in_frame_mobjects", None)
        if add is not None and mobjects:
            add(*mobjects)
        return mobjects[0] if len(mobjects) == 1 else VGroup(*mobjects)

    def unhud(self, *mobjects) -> None:
        remove = getattr(self.camera, "remove_fixed_in_frame_mobjects", None)
        if remove is not None and mobjects:
            remove(*mobjects)

    # -- real (word-boundary-accurate) SRT export ------------------------
    def capture_srt(self, tracker, words_per_line: int = 9) -> None:
        """Append this beat's real word timings as SRT cues."""
        wbs = [wb for wb in tracker.data.get("word_boundaries", [])
               if wb.get("text", "").strip()]
        if not wbs:
            return
        starts = [tracker.start_t + wb["audio_offset"] / AUDIO_OFFSET_RESOLUTION
                  for wb in wbs]
        for i in range(0, len(wbs), words_per_line):
            chunk = wbs[i:i + words_per_line]
            chunk_starts = starts[i:i + words_per_line]
            end = (starts[i + words_per_line]
                   if i + words_per_line < len(starts) else tracker.end_t)
            text = " ".join(wb["text"] for wb in chunk)
            self._srt_entries.append((chunk_starts[0], end, text))
        # A sentence-final single word straddles the following pause: with
        # audio-measured timings its cue lands mostly in silence, which both
        # fails the sync verifier and reads badly.  Fold it into the line
        # before it (words and timing are preserved; only the grouping moves).
        while (len(self._srt_entries) >= 2
               and len(self._srt_entries[-1][2].split()) == 1):
            prev = self._srt_entries[-2]
            last = self._srt_entries[-1]
            self._srt_entries[-2] = (prev[0], last[1],
                                     f"{prev[2]} {last[2]}")
            self._srt_entries.pop()

    def write_real_srt(self) -> Path:
        """Write the real SRT next to where Manim puts this render's movie.

        The house pipeline reads ``<media>/videos/<stem>/<quality>/<Class>.real.srt``
        so the file is written there, with a convenience copy one level up.
        """
        quality = f"{config.pixel_height}p{int(round(config.frame_rate))}"
        out_dir = Path(config.media_dir) / "videos" / self.module_stem / quality
        out_dir.mkdir(parents=True, exist_ok=True)
        srt_path = out_dir / f"{self.__class__.__name__}.real.srt"

        def fmt(t: float) -> str:
            # Round to whole milliseconds FIRST: rounding the fractional part
            # on its own can yield ms == 1000, which writes a four-digit
            # millisecond field -- invalid SRT that strict parsers drop.
            total = int(round(max(float(t), 0.0) * 1000))
            h = total // 3_600_000
            m = (total // 60_000) % 60
            s = (total // 1000) % 60
            ms = total % 1000
            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

        lines: list[str] = []
        for idx, (start, end, text) in enumerate(self._srt_entries, 1):
            lines.append(str(idx))
            lines.append(f"{fmt(start)} --> {fmt(max(end, start + 0.3))}")
            lines.append(text)
            lines.append("")
        srt_path.write_text("\n".join(lines), encoding="utf-8")
        sibling = out_dir.parent / f"{self.__class__.__name__}.real.srt"
        sibling.write_text("\n".join(lines), encoding="utf-8")
        logger.info(f"[real SRT] {srt_path}  ({len(self._srt_entries)} cues)")
        return srt_path

    # -- small conveniences ---------------------------------------------
    def show(self, *mobjects, run_time: float = 0.6, **kwargs):
        """Fade in, then remember so the next beat can clear the stage."""
        self.play(*[FadeIn(m, **kwargs) for m in mobjects], run_time=run_time)
        self.keep.add(*mobjects)

    # -- stage management ------------------------------------------------
    def _protected_ids(self, *groups) -> set[int]:
        ids: set[int] = set()
        for g in groups:
            ids |= {id(m) for m in g.get_family()}
        if self.backdrop is not None:
            ids |= {id(m) for m in self.backdrop.get_family()}
        return ids

    def _unprotected(self, *protected) -> Group:
        """Everything on stage that is not explicitly protected.

        Clearing used to be bookkeeping: each beat had to remember to
        register what it created.  Miss once and the object is orphaned --
        on stage but tracked by nothing, so no later fade ever removes it.
        That is how Act I's "LANGUAGE MODEL" machine leaked into Scene 02.
        Inverting it -- clear everything except what was explicitly
        protected -- makes the failure mode impossible instead of silent.
        """
        keep_ids = self._protected_ids(*protected)
        return Group(*[m for m in self.mobjects if id(m) not in keep_ids])

    def _clear_members(self, members: Group, run_time: float | None) -> None:
        if not len(members):
            return
        if run_time and run_time > 0.2:
            self.play(FadeOut(members), run_time=run_time)
        self.remove(*list(members))

    def hold(self, *mobjects):
        """Register a scene-long prop: survives ``dissolve``, dies at scene end."""
        self.stage.add(*mobjects)
        return mobjects[0] if len(mobjects) == 1 else VGroup(*mobjects)

    def release_stage(self, run_time: float = 0.6) -> None:
        """Drop the scene-long props early (e.g. before a camera change)."""
        self._clear_members(self._group_members(self.stage), run_time)
        self.stage = VGroup()

    def _group_members(self, group) -> Group:
        """The family members of `group` that are actually on stage."""
        live = {id(m) for m in self.mobjects}
        return Group(*[m for m in group.get_family() if id(m) in live])

    def clear_stage(self, run_time: float = 0.5, keep=()):
        """Close a scene: everything goes except the backdrop.

        Unlike ``dissolve`` this deliberately does *not* protect the chrome --
        the title belongs to this scene and must not survive into the next
        one.  (It did, once: Scene 02's title was drawn straight over Scene
        01's, because clear_stage protected chrome and nothing removed it.)
        """
        keep = VGroup(*keep)
        doomed = self._unprotected(keep)
        self.keep, self.stage, self.chrome = keep, VGroup(), VGroup()
        self._clear_members(doomed, run_time)

    def dissolve(self, tracker, *, persist=(), frac: float = 1.0):
        """Clear the stage *inside* the beat, using the narration's own tail.

        Ending a beat with a silent fixed-length fade leaves dead air between
        every beat (about ten seconds over an act).  Fading over whatever
        narration is left costs nothing and reads as a natural cut.

        Anything not in ``persist``, ``self.stage`` or ``self.chrome`` is
        removed, so an unregistered object cannot survive the cut.
        """
        persist = VGroup(*persist)
        doomed = self._unprotected(self.chrome, self.stage, persist)
        self.keep = persist
        self._clear_members(doomed, tracker.get_remaining_duration() * frac)

    # -- layout audit ----------------------------------------------------
    # Set LLM_LAYOUT_AUDIT=1 and render with --dry_run to get an objective
    # report of everything that escapes the panel or collides with something
    # else, without writing a single frame.  Eyeballing extracted frames
    # found the two collisions in Act I; this finds all of them.
    def play(self, *args, **kwargs):
        result = super().play(*args, **kwargs)
        if AUDIT_LAYOUT:
            self._audit()
        return result

    def tear_down(self):  # noqa: D102 - Manim hook
        if AUDIT_LAYOUT:
            self.report_layout()
        super_tear_down = getattr(super(), "tear_down", None)
        if super_tear_down is not None:
            super_tear_down()

    def _label(self, mob) -> str:
        names = [s.text for s in mob.get_family()
                 if isinstance(s, Text) and getattr(s, "text", "")]
        return repr(" | ".join(names)[:52]) if names else ""

    def _visible(self, mob) -> bool:
        best = 0.0
        for s in mob.get_family():
            if s.submobjects:
                continue
            try:
                best = max(best, s.get_fill_opacity(), s.get_stroke_opacity())
            except Exception:  # noqa: BLE001 - some mobjects have neither
                best = max(best, 1.0)
        return best > 0.03

    def _leaf_box(self, mob):
        """On-screen bounding box of one leaf mobject, camera included."""
        pts = mob.get_all_points()
        if pts is None or len(pts) == 0:
            return None
        pts = np.asarray(pts)
        if len(pts) > 240:
            pts = pts[:: max(1, len(pts) // 240)]
        try:
            sub = self.camera.points_to_subpixel_coords(mob, pts)
        except Exception:  # noqa: BLE001
            return None
        if sub is None or len(sub) == 0:
            return None
        sx = config.frame_width / config.pixel_width
        sy = config.frame_height / config.pixel_height
        fc = self.camera.frame_center
        xs = (sub[:, 0] - config.pixel_width / 2) * sx + fc[0]
        ys = (config.pixel_height / 2 - sub[:, 1]) * sy + fc[1]
        return (float(xs.min()), float(ys.min()), float(xs.max()), float(ys.max()))

    def _screen_box(self, mob):
        """Union of the leaf boxes of `mob`: what is actually on screen.

        Not the box of the group itself.  ``fixed_in_frame`` is recorded per
        mobject, and a wrapper VGroup built at a call site -- ``VGroup(a, b)``
        handed straight to ``play`` -- is *not* in that set even though its
        children are.  Asking such a wrapper for its own projection therefore
        projected it as 3D geometry and reported the scene title at the wrong
        height, which read as a title/label clash in every 3D shot.  The
        renderer draws family members, so their union is the truth.
        """
        boxes = [b for b in (self._leaf_box(s) for s in mob.get_family()
                             if not s.submobjects) if b is not None]
        if not boxes:
            return None
        return (min(b[0] for b in boxes), min(b[1] for b in boxes),
                max(b[2] for b in boxes), max(b[3] for b in boxes))

    def _audit(self) -> None:
        self._audit_n += 1
        groups = []
        # Camera animations add the camera's own ValueTrackers to the scene;
        # those are machinery, not content, and their coordinates are
        # meaningless in frame space.
        from manim import ValueTracker
        for m in list(self.mobjects):
            if isinstance(m, ValueTracker):
                continue
            if self.backdrop is not None and (
                    m is self.backdrop or m in self.backdrop.get_family()):
                continue
            if not self._visible(m):
                continue
            groups.append(m)

        tag = f"{self.__class__.__name__}#{self._audit_n}"

        # 1) top-level objects that escape the panel
        for m in groups:
            box = self._screen_box(m)
            if box is None:
                continue
            x0, y0, x1, y1 = box
            over = []
            if x0 < SAFE_L - OUT_TOL:
                over.append(f"left {x0:+.2f} < {SAFE_L:+.2f}")
            if x1 > SAFE_R + OUT_TOL:
                over.append(f"right {x1:+.2f} > {SAFE_R:+.2f}")
            if y0 < SAFE_B - OUT_TOL:
                over.append(f"below {y0:+.2f} < {SAFE_B:+.2f}")
            if y1 > SAFE_T + OUT_TOL:
                over.append(f"above {y1:+.2f} > {SAFE_T:+.2f}")
            if over:
                self._audit_issues.append(
                    f"[{tag}] OUTSIDE {type(m).__name__} {self._label(m)} "
                    f"-> " + "; ".join(over))

        # 2) collisions, comparing whole on-screen objects but exempting
        # containment.  Leaf-level comparison was tried and is far too noisy:
        # Segoe Print is a handwriting face, so the bounding boxes of
        # neighbouring glyphs inside one word already overlap.  Comparing
        # groups, and skipping any pair where a *part* of one sits inside the
        # other, keeps the signal (a label inside its panel, a highlight box
        # drawn around one item of a list) and drops the noise.
        leaf_boxes: dict[int, list] = {}
        for m in groups:
            leaf_boxes[id(m)] = [
                b for b in (self._screen_box(s) for s in m.get_family()
                            if not s.submobjects) if b is not None
            ]

        boxes = [(m, self._screen_box(m)) for m in groups]
        boxes = [(m, b) for m, b in boxes if b is not None]

        for i in range(len(boxes)):
            mi, (ax0, ay0, ax1, ay1) = boxes[i]
            for j in range(i + 1, len(boxes)):
                mj, (bx0, by0, bx1, by1) = boxes[j]
                iw = min(ax1, bx1) - max(ax0, bx0)
                ih = min(ay1, by1) - max(ay0, by0)
                if iw <= 0 or ih <= 0:
                    continue
                area_a = (ax1 - ax0) * (ay1 - ay0)
                area_b = (bx1 - bx0) * (by1 - by0)
                small = min(area_a, area_b)
                if small <= 1e-6:
                    continue
                frac = (iw * ih) / small
                if frac < OVERLAP_FRAC:
                    continue
                if _box_contains((ax0, ay0, ax1, ay1), (bx0, by0, bx1, by1)):
                    continue
                if _box_contains((bx0, by0, bx1, by1), (ax0, ay0, ax1, ay1)):
                    continue
                if leaf_boxes[id(mi)] and all(_box_contains((bx0, by0, bx1, by1), b)
                                      for b in leaf_boxes[id(mi)]):
                    continue
                if leaf_boxes[id(mj)] and all(_box_contains((ax0, ay0, ax1, ay1), b)
                                      for b in leaf_boxes[id(mj)]):
                    continue
                # Parts of one 3D rig overlap each other by construction: a
                # machine standing on a long bench shares the bench's
                # projected bounding box, and adjacent boxes' boxes touch.
                # ``rig`` tags mark those mobjects as one composition.
                if (getattr(mi, "rig", None) is not None
                        and getattr(mi, "rig", None) == getattr(mj, "rig", None)):
                    continue
                # A tiny label next to a much larger surface (a nameplate
                # under a rig, a caption on a panel) is layout, not a crash.
                if min(area_a, area_b) * 8 < max(area_a, area_b):
                    continue
                # A hollow box drawn around one item of a list (Scene 14's
                # answer highlight, the chart-row highlights) is a marker,
                # not a collision: it contains at least one text leaf of the
                # other group while the group itself stays outside.
                if _is_highlight_box(mi, (bx0, by0, bx1, by1),
                                     leaf_boxes[id(mj)]):
                    continue
                if _is_highlight_box(mj, (ax0, ay0, ax1, ay1),
                                     leaf_boxes[id(mi)]):
                    continue
                extra = ""
                if AUDIT_VERBOSE:
                    extra = (f"   A=[{ax0:+.2f},{ay0:+.2f},{ax1:+.2f},{ay1:+.2f}]"
                             f" B=[{bx0:+.2f},{by0:+.2f},{bx1:+.2f},{by1:+.2f}]")
                self._audit_issues.append(
                    f"[{tag}] OVERLAP {frac:.0%}  "
                    f"{self._label(mi) or type(mi).__name__} "
                    f"<> {self._label(mj) or type(mj).__name__}{extra}")

    def report_layout(self) -> None:
        out = HERE / "media" / "layout_audit"
        out.mkdir(parents=True, exist_ok=True)
        path = out / f"{self.__class__.__name__}.txt"
        seen: list[str] = []
        for line in self._audit_issues:
            if line not in seen:
                seen.append(line)
        path.write_text("\n".join(seen) + "\n", encoding="utf-8")
        outside = [x for x in seen if "OUTSIDE" in x]
        overlap = [x for x in seen if "OVERLAP" in x]
        logger.info(f"[layout] {self.__class__.__name__}: "
                    f"{len(outside)} outside, {len(overlap)} overlaps "
                    f"-> {path}")

    def view_2d(self, *, animate: bool = False, run_time: float = 1.0):
        """Return to the straight-on composition (the default framing).

        Most of the episode is 2D on the panel; the 3D shots are deliberate
        departures and always come back here.  ``zoom`` is reset explicitly,
        otherwise a 3D shot's zoom persists into the next scene.
        """
        if animate:
            self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0,
                             run_time=run_time)
        else:
            self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)
        return self

    def view_3d(self, *, phi: float = 62, theta: float = -55,
                zoom: float = 1.0, animate: bool = True,
                run_time: float = 1.4, **kwargs):
        """Move into a perspective view for a 3D shot."""
        target = dict(phi=phi * DEGREES, theta=theta * DEGREES, zoom=zoom, **kwargs)
        if animate:
            self.move_camera(run_time=run_time, **target)
        else:
            self.set_camera_orientation(**target)
        return self

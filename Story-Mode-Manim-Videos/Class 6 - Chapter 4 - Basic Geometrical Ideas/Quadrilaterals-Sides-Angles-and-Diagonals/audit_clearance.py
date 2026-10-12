"""Measure how close two pieces of chalk text come, per scene.

audit_sync_overlap.py reports hard *overlaps*.  This companion reports the
*tight* spots just short of one: every pair of text mobjects whose bounding
boxes are separated by less than `min_gap` (tight) or which touch/overlap
(negative gap).  The scene is replayed exactly as the audit replays it, so
each pair is measured at its true pose, `always_redraw` instruments included.

    python audit_clearance.py <topic-folder> <module.py> <Class> [min_gap]

It imports that topic's own audit_sync_overlap.py (which holds the harness,
the SRT bounds and the narration table) and subclass it, so nothing here has
to know the topic.
"""
from __future__ import annotations

import importlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Ticks, crosses and ballot boxes: present in the LaTeX fonts, absent from
# Segoe Print, so they must never be handed to board_text().
GLYPH_HINT = re.compile("[\u2713\u2714\u2717\u2718\u2610\u2611\u2612]")


def main() -> None:
    topic = sys.argv[1]
    module = Path(sys.argv[2]).stem
    cls_name = sys.argv[3]
    min_gap = float(sys.argv[4]) if len(sys.argv) > 4 else 0.22

    topic_dir = (HERE / topic).resolve()
    sys.path.insert(0, str(topic_dir))
    sys.path.insert(0, str(HERE.parent.parent))          # repo root
    sys.path.insert(0, str(HERE.parent.parent.parent))   # repo parent

    audit = importlib.import_module("audit_sync_overlap")
    mod = importlib.import_module(module)
    scene_cls = getattr(mod, cls_name)

    tight: list[str] = []
    online: list[str] = []
    foreign: list[str] = []
    seen: set[str] = set()
    seen_line: set[str] = set()
    seen_box: set[str] = set()

    def is_card_box(leaf, require_fill: bool = False) -> bool:
        """A rectangular panel (card, boxed strip) -- not the figure's own
        polygon, not a full-frame veil and not a thin bar such as a compass
        handle.

        `require_fill` keeps only panels that are actually filled: chalk can
        disappear *behind* those, whereas a highlight ring around a digit is
        unfilled and holds its own glyph by design."""
        fam = leaf.get_family()
        rects = [m for m in fam
                 if isinstance(m, (audit.Rectangle, audit.RoundedRectangle,
                                   audit.SurroundingRectangle))]
        if not rects:
            return False
        x0, y0 = leaf.get_left()[0], leaf.get_bottom()[1]
        x1, y1 = leaf.get_right()[0], leaf.get_top()[1]
        w, h = x1 - x0, y1 - y0
        if min(w, h) < 0.16 or x1 - x0 > 8.0 or y1 - y0 > 5.0:
            return False
        if w * h < 0.40:
            return False
        if require_fill:
            try:
                if max(m.get_fill_opacity() for m in rects) < 0.25:
                    return False
            except Exception:
                return False
        return True

    class ClearanceHarness(audit.Harness):
        def check_overlaps(self) -> None:
            scene = self.scene
            skip = {id(getattr(scene, n, None)) for n in
                    ("bg", "student", "teacher", "badge", "badge_l")}
            texts, curves = [], []
            roots: dict[int, list] = {}
            for m in scene.mobjects:
                if id(m) in skip or audit.is_think_badge(m):
                    continue
                if isinstance(m, audit.ValueTracker):
                    continue
                rid = id(m)
                for leaf in audit.content_leaves(m):
                    roots.setdefault(rid, []).append(leaf)
                    if audit.is_texty(leaf):
                        texts.append((rid, leaf))
                    elif audit.frame_kind(leaf) == "line":
                        curves.append((rid, leaf))
            boxes = [(rid, leaf) for rid, leaves in roots.items()
                     for leaf in leaves if is_card_box(leaf)]
            filled = [(rid, leaf) for rid, leaves in roots.items()
                      for leaf in leaves if is_card_box(leaf, require_fill=True)]
            for i in range(len(texts)):
                for j in range(i + 1, len(texts)):
                    a, b = texts[i][1], texts[j][1]
                    ax0, ay0, ax1, ay1 = self.bbox(a)
                    bx0, by0, bx1, by1 = self.bbox(b)
                    gx = max(ax0 - bx1, bx0 - ax1)
                    gy = max(ay0 - by1, by0 - ay1)
                    gap = max(gx, gy)
                    if gap >= min_gap:
                        continue
                    kind = "OVERLAP" if gap <= 0 else f"tight {gap:.2f}"
                    if kind.startswith("tight") and min(gx, gy) >= min_gap:
                        continue      # diagonal neighbours: boxes overlap only
                    key = f"{self.piece}|{kind}|{audit.describe(a)}|" \
                          f"{audit.describe(b)}"
                    if key in seen:
                        continue
                    seen.add(key)
                    tight.append(
                        f"[{self.piece:14s} step {self.step:3d}] {kind:12s} "
                        f"{audit.describe(a)}   <->   {audit.describe(b)}")
            # text a chalk line actually runs through: the bbox test above
            # cannot see this (a straight line's box is degenerate), so sample
            # the real geometry -- the same measure audit_sync_overlap uses.
            for t in (leaf for _, leaf in texts):
                tx0, ty0, tx1, ty1 = self.bbox(t)
                for c in (leaf for _, leaf in curves):
                    cx0, cy0, cx1, cy1 = self.bbox(c)
                    if (max(tx0 - cx1, cx0 - tx1) > 0.06
                            or max(ty0 - cy1, cy0 - ty1) > 0.06):
                        continue
                    clear = self.true_clearance(t, c)
                    if clear > 0.03:
                        continue
                    key = f"{self.piece}|{audit.describe(t)}|" \
                          f"{audit.describe(c)}|{clear:.2f}"
                    if key in seen_line:
                        continue
                    seen_line.add(key)
                    online.append(
                        f"[{self.piece:14s} step {self.step:3d}] "
                        f"ON-LINE gap {clear:.2f}  {audit.describe(t)}"
                        f"   <->   {audit.describe(c)}")
            # a figure drawn behind a card: chalk inside somebody else's box.
            # Two leaves from the same top-level mobject belong together (a
            # card's own text sits in the card's own box), so only foreign
            # combinations are reported.
            def report_box(msg: str) -> None:
                if msg in seen_box:
                    return
                seen_box.add(msg)
                foreign.append(f"[{self.piece:14s} step {self.step:3d}] {msg}")

            # Segoe Print has no tick, cross or ballot-box glyph: a literal one
            # in a Text renders as an empty box.  The series draws its ticks
            # with strokes (mark_yes / check_row), so any of these in visible
            # text is a defect.
            for _rid, t in texts:
                raw = (getattr(t, "text", "") or getattr(t, "tex_string", ""))
                if GLYPH_HINT.search(raw):
                    report_box(f"GLYPH-AS-TEXT  {raw[:40]!r}  (no such glyph in "
                               f"the board font)")

            # a chalk dot inside a label is always a mistake: the share-dots
            # and vertex dots belong beside their figure, never over wording
            dots = [(rid, l) for rid, leaves in roots.items() for l in leaves
                    if isinstance(l, audit.Dot)]
            for rid_c, c in dots:
                ccx, ccy = c.get_center()[0], c.get_center()[1]
                for rid_t, t in texts:
                    if rid_t == rid_c:
                        continue
                    x0, y0, x1, y1 = self.bbox(t)
                    if x0 < ccx < x1 and y0 < ccy < y1:
                        report_box(f"DOT-ON-TEXT  {audit.describe(c)} inside  "
                                   f"{audit.describe(t)}")

            texts_by_root: dict[int, list] = {}
            for rid, t in texts:
                texts_by_root.setdefault(rid, []).append(t)

            def inside(mob, box) -> bool:
                x0, y0, x1, y1 = self.bbox(mob)
                bx0, by0, bx1, by1 = self.bbox(box)
                cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
                return (bx0 + 0.02 < cx < bx1 - 0.02
                        and by0 + 0.02 < cy < by1 - 0.02)

            for r1, t in texts:
                tx0, ty0, tx1, ty1 = self.bbox(t)
                ta = max((tx1 - tx0) * (ty1 - ty0), 1e-6)
                length = len((getattr(t, "text", "")
                              or getattr(t, "tex_string", "")).strip())
                if length > 4:
                    continue          # panels hold prose; figures hold labels
                for r2, b in filled:
                    if r1 == r2:
                        continue
                    bx0, by0, bx1, by1 = self.bbox(b)
                    # a frame that merely wraps the text (a card's own box,
                    # even when the scene adds box and text separately) is not
                    # a foreign box; one much larger than the text is.
                    if (bx1 - bx0) * (by1 - by0) < 8.0 * ta:
                        continue
                    # and a panel's own lines all sit inside it, so a label is
                    # only foreign if its group has members outside this box
                    if not any(not inside(o, b)
                               for o in texts_by_root.get(r1, []) if o is not t):
                        continue
                    if inside(t, b):
                        report_box(f"TEXT-IN-BOX  {audit.describe(t)}"
                                   f"   inside   {audit.describe(b)}")
            for r1, c in curves:
                if isinstance(c, audit.Dot):
                    continue
                cx0, cy0, cx1, cy1 = self.bbox(c)
                if max(cx1 - cx0, cy1 - cy0) < 0.45:
                    continue      # a tick or a chip's own stroke, not a figure
                parts = [m for m in c.get_family()
                         if len(getattr(m, "points", ()))]
                for r2, b in boxes:
                    if r1 == r2:
                        continue
                    bx0, by0, bx1, by1 = self.bbox(b)
                    hit = False
                    for part in parts:
                        for s in range(0, 21):
                            p = part.point_from_proportion(s / 20.0)
                            if (bx0 + 0.04 < p[0] < bx1 - 0.04
                                    and by0 + 0.04 < p[1] < by1 - 0.04):
                                hit = True
                                break
                        if hit:
                            break
                    if hit:
                        report_box(f"LINE-IN-BOX  {audit.describe(c)}"
                                   f"   runs into   {audit.describe(b)}")

    scene = scene_cls()
    h = ClearanceHarness(scene)
    scene.voiceover = lambda text=None, **kw: h.voiceover_cm(text)
    scene.play = h.play
    scene.wait = h.wait
    scene.add_sound = lambda *a, **k: None
    scene.set_speech_service = lambda *a, **k: None
    scene._capture_srt = lambda *a, **k: None
    scene._write_real_srt = lambda: None

    scene.construct()

    print(f"\n===== TIGHT / OVERLAPPING TEXT PAIRS (gap < {min_gap}) =====")
    if not tight:
        print("(none)")
    for line in tight:
        print(line)
    print(f"\n{len(tight)} pair(s) closer than {min_gap} units")

    print("\n===== TEXT A CHALK LINE RUNS THROUGH =====")
    if not online:
        print("(none)")
    for line in online:
        print(line)
    print(f"\n{len(online)} text/line collision(s)")

    print("\n===== CHALK INSIDE SOMEBODY ELSE'S CARD =====")
    if not foreign:
        print("(none)")
    for line in foreign:
        print(line)
    print(f"\n{len(foreign)} foreign-box collision(s)")


if __name__ == "__main__":
    main()

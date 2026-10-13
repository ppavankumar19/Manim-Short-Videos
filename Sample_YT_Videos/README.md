# Kepler short — landscape re-creation

A Manim CE rebuild of the reference clip
`When being beautifully wrong leads to discovery.mp4`, turned from portrait
720×1280 @ 30 fps into **1920×1080 @ 60 fps**.

Narration is re-voiced through the project's own `speech_service.py`
(`en-IN-PrabhatNeural` via edge-tts), not lifted from the reference mp3.

## Render

```
..\.venv\Scripts\python.exe render_all.py            # all beats, then join
..\.venv\Scripts\python.exe render_all.py --only 02  # one beat
..\.venv\Scripts\python.exe render_all.py --join     # re-join what is on disk
```

Output: `kepler_short.mp4` in this folder. Beats land under
`media/videos/<module>/1080p60/`, narration is cached in `media/voiceovers/`
so a re-render is offline and fast.

## Layout

| File | What it holds |
| --- | --- |
| `common.py` | Theme, narration, the karaoke `Captions` system, platonic-solid geometry, orbits, sun, stars |
| `map_art.py` | The two shots the reference fills with photography: the Oresund, and Uraniborg |
| `scene_01_kepler.py` … `scene_08_outro.py` | One beat each |
| `render_all.py` | Render + concat driver |

## How the sync works

The captions are the reference clip's: two short lines on screen, the spoken
one amber. Rather than guessing times, `common.Captions` reads the **edge-tts
word boundaries** of our own narration, so each line lights up when it is
actually spoken. `common.cue_times` reuses the same times to cut the animation
— every scene declares which caption line each step starts on (`MARKS`), and
the run times fall out of that. Change the wording or the voice rate and the
choreography re-syncs itself.

## Why the nest stays legible

Three rules, all taken off the reference clip frame by frame. Drop any one of
them and five nested wireframes turn into white noise.

* **Constant framing.** `framing_zoom` sets the camera so the *newest* thing —
  the solid just drawn, or the sphere just closed — is always the same size on
  screen. The nest spans a factor of fourteen, so a fixed camera would either
  crop the octahedron or lose the cube.
* **Only the outermost solid is lit.** As each sphere closes over a solid, that
  solid drops to `BURIED` (12%) and survives as a faint web at the centre.
* **Each ball recedes as a bigger one encloses it.** Every disc in a ball
  shares one alpha — the sphere profile comes from how many overlap — so
  scaling that alpha by `SHELL_RECEDE` dims a whole ball without flattening it.

The balls themselves are flat discs kept square to the camera. A sphere's
silhouette from any viewpoint is a circle about the line of sight, and every
shell is centred on the origin the camera is aimed at, so this projects
identically to a real sphere at a fraction of the cost. The discs are spaced at
`sqrt(1 - (j/n)^2)` so the number covering radius `b` follows the real optical
depth through a sphere — evenly spaced discs give a bright core with a clear
edge, which is not what a sphere looks like.

The camera runs at `focal_distance=220`, near-orthographic like the reference.
Manim's default of 20 is shorter than the cube's own circumradius and bends it
into a frustum.

## Geometry

`SPHERE_R` is Kepler's *Mysterium Cosmographicum* at its true proportions.
Each solid's inradius is the sphere below it and its circumradius the sphere
above, so the six radii are derived, not placed:

```
1.000  Mercury
1.732  Venus      (octahedron,  R/r = sqrt 3)
2.180  Earth      (icosahedron, R/r = 1.2584)
2.743  Mars       (dodecahedron)
8.229  Jupiter    (tetrahedron, R/r = 3)
14.252 Saturn     (cube,        R/r = sqrt 3)
```

That factor of fourteen is why the camera in beat 2 pulls back as hard as it
does.

## Where this departs from the reference

* **It runs longer than 60 s.** The reference narrator does about 3.4 words a
  second, which PrabhatNeural can only match by gabbling, so `BEAT_RATE` sits
  near the voice's natural pace instead. Raise it there to trade clarity for
  length — the animation follows, since every run time is derived from the
  resulting word boundaries.
* **No end card.** The reference closes on "Full video on YouTube" and an arrow
  pointing off-frame; that belongs to its own channel, so this holds on the
  orbits and fades.
* **The Oresund and Uraniborg are drawn, not photographed.** The reference
  cuts to satellite imagery and to a period engraving. Neither asset is in
  this repo, so `map_art.py` builds a stylised strait and a line-art
  observatory that occupy the same place in the edit.
* **Beat 6 shows the mismatch.** Where the reference holds a wide shot under
  "it was always off by a few percent", this version drops back in on Venus
  and lays Kepler's predicted sphere (amber, dashed) over the measured orbit,
  so the gap the line names is on screen.
* **The opening plate uses `images.jfif`**, the landscape illustration
  supplied with the reference, rather than the portrait painting the reference
  crops — it fits the landscape frame without pillarboxing.

# Manim resources: biology (downloaded, kept OUTSIDE the project folders)

Freely licensed anatomy drawings fetched from Wikimedia Commons for the
Class 10 Biology story-mode videos.  They are *data*: Manim only parses them
(`SVGMobject`); nothing in them is executed.  Before use they were checked for
`<script>`, `onload/onclick` handlers, remote `xlink:href` links and embedded
bitmaps (none found).

| file (in `_downloads/`)        | what it is                          | author            | licence        |
|--------------------------------|-------------------------------------|-------------------|----------------|
| `heart_diagram_en.svg`         | anatomical heart cut-away           | ZooFari           | CC BY-SA 3.0   |
| `alveolus_diagram.svg`         | alveoli with capillary network      | LadyofHats        | public domain  |
| `respiratory_system.svg`       | whole respiratory system (unused)   | LadyofHats, Jmarchn | public domain |
| `circulatory_system.svg`       | whole circulatory system (unused)   | LadyofHats, M. Ruiz Villarreal | public domain |
| `human_heart_clean.svg`        | schematic heart (unused)            | Wnauta            | CC BY-SA 3.0   |
| `capillary.svg`                | 3D capillary section (unused)       | Kelvinsong        | CC BY-SA 3.0   |
| `red_blood_cells.svg`          | black RBC blobs (unused, poor)      | Jessica Polka     | CC BY-SA 4.0   |

Exact source URLs: `_downloads/sources.json`.

CC BY-SA files must be credited when used (the videos show a small credit
line) and adaptations (our recolouring / label removal) stay under the same
licence.

How the project uses them: `Biology - Class 10/bio_real_art.py`
 * `real_heart(height)` removes the baked-in labels and leader lines, recolours
   the black cavities (blue right side, red left side) and exposes anatomy
   anchors (`RA RV LA LV TRI MIT ...`) via `.at(name)`;
 * `alveolus_view(width)` removes the grey plate and leader lines.

# Brief: turn one photo of the red bin shelving into bin-unit files

Under the 5-row pull-out drawer wall (see `HANDOFF.md`) is red open-bin shelving. It is made of one red **unit** per drawer column: a unit sits directly under its drawer column, is 2 bins wide, and has stacked rows of bins (bigger bins near the top, smaller lower down — count what you see, never assume). Each bin has a printed label strip on its front lip, for example:

    46¢ EACH | 9/16 Wrench | 3/8-16 x 3/4 | HEX BOLTS | Coarse | 25.99 Box/100 | barcode | 00051

Each photo you get shows two whole units side by side (plus slivers of the neighbours at the edges — ignore those). The left whole unit is the lower column number.

Project root: `/home/litsush/hhh/project/hankins-screw-aisle` (run commands from there). Python: `.venv/bin/python`. Helper CLI: `.venv/bin/python tools/kit.py` (run with no args for help; `rectify`, `grid`, `zoom`, `overlay`, `check`). Import helpers with `import sys; sys.path.insert(0, "tools"); from kit import rects, bands`.
Photos: `originals/bottom/IMG_xxxx.jpg` (3024×4032).
Scratch: `/tmp/claude-1000/-home-litsush-hhh/15dece7a-f509-4f04-a030-82a7b9de1dab/scratchpad/work/bins/<photo>/`. Only final outputs go in the project.

## Outputs, per unit (column NN, two digits)

1. `images/bins/cNN.jpg`: the unit face, straightened with `kit.py rectify` to **500×1500** (W×H). Quad = the unit's outer face: top-left/top-right just under the aluminium diamond-plate shelf edge, at the outer edges of the unit's red side posts; bottom corners at the bottom of the unit (where it meets the floor/kick plate). Top-left, top-right, bottom-right, bottom-left order.
2. `bins/cNNbins.json`:
```
{ "id": "cNNbins", "kind": "bins", "column": NN, "row": 6, "half": null,
  "title": "Bins under column NN",
  "description": "<one plain sentence: what's in these bins>",
  "front_image": null, "tray_image": "images/bins/cNN.jpg", "tray_image_px": [500, 1500],
  "photo": "IMG_xxxx.jpg",
  "compartments": [ {item_index, x0, y0, x1, y1}, ... ],   # fractions of the 500x1500 image; one per bin, covering the bin opening + its label
  "items": [ ... ] }
```
   Items, in reading order (top row first, left bin then right bin):
   - `sku`: the number printed under the barcode, as a string exactly as printed (e.g. "00051")
   - `slot_letter`: null
   - `name`: clear product name from the label, e.g. "3/8-16 x 3/4 hex bolt, coarse thread, 9/16 wrench"
   - `label_short`: the size line, e.g. "3/8-16 x 3/4"
   - `price_cents`: the EACH price (46¢ → 46, 1.85 → 185); null only if unreadable (add a note)
   - `box_price_cents` / `box_qty`: the box price and count (25.99 Box/100 → 2599, 100); null if absent
   - `upc`: "" and `upc_source`: null (these labels print no UPC digits)
   - `location`: "Bin <sku>" (e.g. "Bin 00051"); if two bins share a number make it unique by adding "(left)"/"(right)"
   - optional `note`: empty bin, missing/blank label, contents don't match label, unreadable value.
   - A bin with no label at all still gets an item (`sku` "", name "Unlabelled bin", prices null, a note, location "Unlabelled bin, row R left/right").

## Reading

Zoom on the full-resolution original (`kit.py zoom`, ~700 px wide crops upscaled to 1600) row by row. Prices: read cents carefully (superscript cents like 26⁹⁹ = 26.99). Labels lower down are smaller and more angled — zoom harder.

## Check (required)

1. `.venv/bin/python tools/kit.py check bins/cNNbins.json` → OK.
2. `kit.py overlay bins/cNNbins.json <scratch>/ov_cNN.jpg` and LOOK: every rectangle on one bin, sizes in sensible order.

Touch only `images/bins/cNN.jpg` and `bins/cNNbins.json` for your columns. Don't run build scripts.

## Report back (short)

Columns done, bin count per unit, notes added, and any value you're unsure of.

# Brief: turn one wall column's photos into drawer files

You are adding one column of a hardware store's screw-aisle drawer wall (5 rows high, 30 columns wide, Midwest Fastener pull-out drawers) to a dataset. Columns 1–10 are done; you do the column you are assigned.

Project root: `/home/litsush/hhh/project/hankins-screw-aisle` (run commands from there).
Python: `.venv/bin/python` (has OpenCV, Pillow, numpy). Helper CLI: `.venv/bin/python tools/kit.py` (run with no args for help; read `tools/kit.py` once).
Photos: `originals/batch2/IMG_xxxx.jpg`, 3024×4032 portrait (one is landscape/sideways; rotate it yourself in python if needed, save the rotated copy into your scratch folder, never overwrite originals).
Scratch: put grids, zooms and other working images under `/tmp/claude-1000/-home-litsush-hhh/15dece7a-f509-4f04-a030-82a7b9de1dab/scratchpad/work/c<NN>/`. Only final outputs go in the project.

Read `HANDOFF.md` for background and look at 2–3 finished examples (e.g. `drawers/c07r3-left.json`, `drawers/c09r3.json`, `drawers/c01r1.json`) and their images before starting.

## Your inputs

- One **fronts photo**: all 5 drawer fronts of the column, row 1 at the top.
- One **tray photo per drawer** (usually 5, sometimes 6–7 when a row slot holds two separate half-width boxes). Each shows the open lid with its printed label card(s), and the tray of compartments. The label code (e.g. "Bolts 15", "Household 11", "Specialty 27") is printed on both the drawer front and the lid; use it to match each tray photo to its row.

## Your outputs

1. `images/fronts/cNNrR.jpg` for each row R (NN = two-digit column). 720×150, made with `kit.py rectify` from the fronts photo. Pick the four corners of the whole drawer face (the blue face with the label, both labels if the slot has two). One front image per row slot, even when the slot holds two half drawers.
2. `images/trays/<id>.jpg`: the tray, straightened top-down, **1200 px wide**, height chosen to match the tray's real proportions (estimate from the compartment geometry; typical full trays are about 1200×800, shallow ones 1200×540, half-width boxes are narrower/taller, so pick h so compartments look square-ish where they really are square). Quad corners = inner corners of the tray's cardboard insert (top-left = back-left, bottom-right = front-right). Exclude the lid.
3. `drawers/<id>.json`, one per drawer, exactly the schema of the existing files:
   - `id`: `cNNrR`, or `cNNrR-left` / `cNNrR-right` when the slot holds two separate boxes (each with its own tray photo). If one tray photo has two label cards stacked on the lid (e.g. "Bolts 15" and "Bolts 35") and one tray holds both products, that is ONE drawer with `half: null` and a title like `"Bolts 15 and Bolts 35"`.
   - `column`, `row`, `half` (null/"L"/"R"), `title` (the label code(s)), `description` (one plain sentence: what's in it, size range, base SKU), `front_image`, `tray_image`, `tray_image_px` [w,h], `compartments`, `items`.
   - items, in label order (back row first, left to right; then the next card if there are two):
     `sku` (string, as printed before the dash on the label, usually 5 digits), `slot_letter` (the letter after the dash: A–R skipping I and O), `name` (clear full product name, e.g. "1/4-28 x 1-1/2 grade 5 hex cap screw, zinc"), `price_cents` (int; null only if truly unreadable, with a note), `upc` (12 digits), `upc_source`, `location` ("<label code>, slot <letter>", e.g. "Bolts 15, slot C"), `label_short` (short text shown on the compartment, e.g. "1/4-28 x 1-1/2" or "3/8 ID"), optional `note`.
   - `compartments`: `{item_index, x0, y0, x1, y1}` fractions of the tray image (y=0 is the back of the drawer, y=1 the front). `kit.bands()` turns pixel rows into these. Layouts vary a lot (tall, wide, odd slots) — map what you see, never assume a grid. Match compartments to items by the label card layout: the card is a map of the tray (same rows/columns, same proportions), so use it.

## Reading labels (most of the work)

Each label cell shows: size/description, price (e.g. `79¢`, `$1.45`), a barcode, and under it `SKU - LETTER` plus the UPC digits (`7 38287 SSSSS C`). Zoom in on the full-resolution original (`kit.py zoom`, crops of ~600–900 px wide upscaled to 1600) until digits are crisp. Work cell by cell; don't guess from one blurry overview.

- **UPC**: usually `738287` + SKU + check digit. Read the printed check digit and verify it with `kit.upc_check`. If what you read disagrees with the math, re-zoom. If the digits are genuinely unreadable, compute it and set `upc_source: "calculated_from_sku"`; otherwise `"read_from_label"`. Some product lines use another prefix (e.g. `719199`) — use what is printed.
- **SKUs** usually run consecutively within a card (e.g. 60421, 60422, …); use that pattern to cross-check, but trust the print.
- **Prices** have no checksum: read each one carefully at high zoom.
- Add a `note` for anything off: empty compartment, compartment not on the label, lid card not matching the tray contents, unreadable value.

## Check your work (required)

1. `.venv/bin/python tools/kit.py check drawers/cNN*.json` must print OK for every file.
2. For every drawer, run `kit.py overlay drawers/<id>.json <scratch>/ov_<id>.jpg` and LOOK at it: each rectangle must sit on one real compartment and the label must match what's physically in it (sizes increasing the way the card says, etc.). Fix and repeat until right.
3. Look at each front image you made: straight, cropped to the drawer face, label readable.

Do not edit any file outside `images/fronts/cNN*`, `images/trays/cNN*`, `drawers/cNN*`. Do not run `build_wall.py` (the coordinator does).

## Report back (short)

- Which photo went to which drawer id.
- Drawer count, item count, how many UPCs were calculated rather than read.
- Every note you added, and anything you're unsure about (especially prices you could not read cleanly).

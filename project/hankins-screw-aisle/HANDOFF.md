# Hankins screw aisle: drawer wall data

This folder is a handoff from a Claude chat session to Claude Code. It holds everything collected so far about one section of a hardware store's screw aisle: a wall of pull-out drawers (Midwest Fastener displays), 5 rows high and 30 columns wide. Each drawer holds a tray of small compartments, and each compartment holds one product.

**Status (2026-11-10):** all 30 columns are done: 157 drawers, 2,630 items. The two 3D scans of the aisle are stitched together, with the drawer photos placed on them. See "Update 2026-11-10" at the bottom.

**Where this is going:**
1. A web page of the wall at `hankins.chopsticklabs.com` (Cloudflare Pages). The working page is in `web/`.
2. Later, a 3D game written in Rust where you walk the store and open these drawers. `data.json` and `images/` are meant to feed it.

The owner, Blake, is not very technical. Explain choices in plain language, and ask before big decisions.

## Folder layout

| Path | What it is |
|---|---|
| `data.json` | The dataset. Start here. |
| `images/fronts/` | Straightened photo of each drawer front, 720×150. |
| `images/trays/` | Straightened top-down photo of each open tray, 1200 wide. |
| `web/` | The current clickable wall page: `index.html` plus `img/`. Static, no build step. Upload `web/` as-is to Cloudflare Pages. |
| `originals/` | Every raw phone photo (sent as a separate zip). `_map.json` says which drawer each one shows. |
| `tools/` | The Python scripts that produced all of this (see below). |

## data.json

```
drawers[]:
  id            "c07r3-left"  (column 7, row 3, left half)
  column, row   wall position; row 1 is the top, column 1 the far left
  half          null, "L" or "R". Some drawer slots hold two separate boxes side by side
                (e.g. Nuts 19 and Nuts 19.5). Each half is its own drawer entry.
  title, description
  front_image, tray_image, tray_image_px [w, h]
  compartments[]  {item_index, x0, y0, x1, y1}
                  Rectangles as fractions (0–1) of the tray image.
                  y = 0 is the back of the drawer, y = 1 the front.
  items[]
    sku           5-digit Midwest number, e.g. "62161" (weld nuts use 6 digits, "931374")
    slot_letter   letter printed on the lid label (A–R, skipping I and O)
    name, price_cents, location, label_short
    upc           12 digits
    upc_source    "read_from_label" or "calculated_from_sku"
    note          only present when something is off (empty slot, lid and tray disagree, etc.)
```

Compartment layouts differ from drawer to drawer: anywhere from 6 to 32 compartments, with tall, wide and odd-shaped slots. Never assume a fixed grid.

## How accurate is it

- **UPCs:** 922 were read from the labels and pass the UPC check-digit test. 28 were too small to read and were calculated from the SKU (marked `calculated_from_sku`). Most UPCs are `738287` + SKU + check digit; the Nuts 19.5 weld nuts use prefix `719199`.
- **Prices** were read by eye with no checksum, so spot-check a few.
- **20 items carry a `note`:** empty compartments, missing dividers, lids that don't match what's in the tray. Search for `"note"` to list them.

## How new columns were added (the workflow)

Blake sends one photo of a column's 5 drawer fronts, then one photo per open drawer showing the lid label and the whole tray. For each batch:

1. **Straighten** (`tools/crop*.py`): hand-picked corner points plus an OpenCV perspective warp. Fronts become 720×150 and trays 1200 wide.
2. **Map compartments:** draw a 100 px grid over each straightened tray, read off the divider positions by eye, and enter them as rows of x-boundaries (the `seq()` helper in `build.py`).
3. **Read the labels:** type in size, price, SKU, slot letter and UPC check digit. `build.py` asserts each check digit, so a misread fails the build.
4. **Build** (`tools/build.py` + `tools/template.html`): produces `wall.html` and `data.json`.

`build.py` grew by patching, so it's messy. A cleaner rewrite would keep one data file per drawer and generate everything from it. That's a good first job if work continues here, and automatic compartment detection would speed up the remaining 20 columns.

## Photo tips that worked best

Shoot straight down over the open drawer with the whole tray and the whole lid label in frame, in even light. Shoot fronts square-on, one photo per column, sent in left-to-right order.

## Update 2026-11-10: new pipeline, columns 11–30, 3D scan

- **One file per drawer:** `drawers/<id>.json` is now the source of truth, and `data.json` is generated from it. Run `.venv/bin/python tools/build_wall.py` to rebuild `data.json` and `web/`. The old `build.py`, `crop*.py` and `patch*.py` are kept only for history.
- **Tools:** `tools/kit.py` has `rectify`, `grid`, `zoom`, `overlay` and `check`; `check` validates UPC check digits and compartment coverage. `tools/COLUMN_BRIEF.md` is the step-by-step brief used to process each column.
- **Columns 11–30:** the photos are in `originals/batch2/`, and `_map.json` maps them to columns. New images are named `images/fronts/cNNrR.jpg` and `images/trays/<id>.jpg`. 15 UPCs were calculated rather than read. `REVIEW_columns_11-30.md` lists the 68 flagged items.
- **3D scan:** `King.ply` (left) and `King2.ply` (right) are Gaussian splats in `/home/litsush/hhh/plys`.
  - `tools/wallframe.py` fits the wall plane.
  - `tools/ortho.py` renders straight-on images.
  - `tools/stitch.py` scales and aligns King2 to King (SIFT match on the orthophotos, scale 1.071), cuts the overlap and writes `scan/aisle_left_merged.ply`.
  - Drawer positions are in `scan/wall_layout.json`. Column edges were read by eye from `scan/mosaic.jpg`; see `POSTS` in `stitch.py`.
  - `tools/export_splat.py` writes the 23 MB web version, `scan/aisle.splat`.
  - `web/3d.html` shows it with the drawer photos on the wall; tap a drawer to open it in a pop-up over the 3D view. Both pages share the pop-up code in `tools/drawer.js` and `tools/drawer.css`; the build copies them into `web/` along with `drawers.json`.
- **Known issues:**
  - `c03r1` (columns 1–10 data) has two overlapping compartments.
  - Column 1's left edge falls just outside the scan.
  - Scan units are the scan's own units, not metres.

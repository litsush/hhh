# Right-hand wall: changes to the briefs

The right-hand wall of the screw aisle is a second wall: 24 drawer columns (5 rows) with the same red bin shelving underneath. Follow `tools/COLUMN_BRIEF.md` (drawers) or `tools/BIN_BRIEF.md` (bins) exactly, with these changes:

- **Photos** are in `originals/right/` (drawers) and `originals/right_bottom/` (bins), not `originals/batch2` / `originals/bottom`. `originals/right/_map.json` lists the fronts photo and tray photos for each right-wall column.
- **Every id, file name and image name gets an `R` prefix**: `Rc05r3`, `Rc05r3-left`, `Rc05bins`. So `drawers/Rc05r3.json`, `images/fronts/Rc05r3.jpg`, `images/trays/Rc05r3.jpg`, `bins/Rc05bins.json`, `images/bins/Rc05.jpg`.
- **Add `"wall": "right"`** to every JSON file (right after `"id"`). `column` stays the plain number (5), and `row` is the same as before.
- Titles: drawers keep the label code as the title (e.g. "Metric 23", "Stainless 104"); bins use "Bins under right-wall column NN".
- Column numbers count left to right as you face the right-hand wall, in the same order as the photos.
- Bins: photo k in `originals/right_bottom/` (sorted by name) shows units 2k−1 (left whole unit) and 2k (right whole unit). If the photo clearly shows something different, such as one unit or three, report that instead of guessing.
- Your scratch folder is `/tmp/claude-1000/-home-litsush-hhh/15dece7a-f509-4f04-a030-82a7b9de1dab/scratchpad/work/R<NN>/` (or `Rbins<k>/`).
- `kit.py check` understands `wall: right`. Touch only your own `R`-prefixed files.

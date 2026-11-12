"""Helpers for turning drawer photos into drawers/*.json entries.

Run with the project venv:  .venv/bin/python tools/kit.py <command> ...

Commands
  rectify SRC OUT W H "x,y x,y x,y x,y"
        Perspective-warp the quad (top-left, top-right, bottom-right, bottom-left,
        in SRC pixel coords) to a flat W x H image. Fronts: 720 150. Trays: 1200 <h>.
  grid IMG OUT [--step 100] [--crop x0,y0,x1,y1] [--width 1400]
        Draw a labelled pixel grid over IMG (or a crop of it) to read coordinates.
  zoom SRC OUT x0 y0 x1 y1 [--width 1600]
        Crop a region at full resolution and scale it, for reading small label text.
  overlay DRAWER.json OUT
        Draw the drawer's compartments over its tray image, labelled with slot
        letter and label_short, to check the mapping by eye.
  check DRAWER.json [...]
        Validate drawer files (UPC check digits, compartment coverage, fields).

Python helpers:  import sys; sys.path.insert(0, "tools"); from kit import upc_check, make_upc, bands, rects
  upc_check(first11) -> int
  make_upc(sku, prefix="738287") -> 12-digit string
  bands(rows, w, h) -> compartments list; rows = [(y0, y1, [x0, x1, x2, ...]), ...]
        in tray pixels, numbered left-to-right, back row first.
  rects([(item_index, x0, y0, x1, y1), ...], w, h) -> compartments for irregular layouts.
"""
import json, os, sys

LETTERS = "ABCDEFGHJKLMNPQRSTUVWXYZ"  # labels skip I and O


def upc_check(s):
    d = [int(c) for c in s]
    return (10 - (3 * sum(d[0::2]) + sum(d[1::2])) % 10) % 10


def make_upc(sku, prefix="738287"):
    s = prefix + str(sku)
    assert len(s) == 11, s
    return s + str(upc_check(s))


def bands(rows, w, h, start=0):
    out, i = [], start
    for y0, y1, xs in rows:
        for a, b in zip(xs, xs[1:]):
            out.append(dict(item_index=i, x0=round(a / w, 4), y0=round(y0 / h, 4),
                            x1=round(b / w, 4), y1=round(y1 / h, 4)))
            i += 1
    return out


def rects(boxes, w, h):
    """boxes = [(item_index, x0, y0, x1, y1), ...] in tray pixels -> compartments."""
    return [dict(item_index=i, x0=round(a / w, 4), y0=round(b / h, 4), x1=round(c / w, 4), y1=round(d / h, 4))
            for i, a, b, c, d in boxes]


def _cv():
    import cv2, numpy as np
    return cv2, np


def rectify(src, out, w, h, quad):
    cv2, np = _cv()
    im = cv2.imread(src)
    q = [tuple(map(float, p.split(","))) for p in quad.split()]
    assert len(q) == 4, "need 4 points"
    M = cv2.getPerspectiveTransform(np.float32(q), np.float32([[0, 0], [w, 0], [w, h], [0, h]]))
    r = cv2.warpPerspective(im, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    cv2.imwrite(out, r, [cv2.IMWRITE_JPEG_QUALITY, 82])


def grid(img, out, step=100, crop=None, width=1400):
    cv2, np = _cv()
    im = cv2.imread(img)
    ox = oy = 0
    if crop:
        x0, y0, x1, y1 = crop
        im = im[y0:y1, x0:x1].copy(); ox, oy = x0, y0
    s = width / im.shape[1]
    im = cv2.resize(im, (width, int(im.shape[0] * s)), interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC)
    H, W = im.shape[:2]
    first_x = (-(ox) % step); first_y = (-(oy) % step)
    for gx in range(first_x, int(W / s) + 1, step):
        X = int(gx * s); cv2.line(im, (X, 0), (X, H), (0, 255, 255), 1)
        cv2.putText(im, str(gx + ox), (X + 2, 14), 0, .45, (0, 0, 255), 2)
    for gy in range(first_y, int(H / s) + 1, step):
        Y = int(gy * s); cv2.line(im, (0, Y), (W, Y), (0, 255, 255), 1)
        cv2.putText(im, str(gy + oy), (2, Y + 14), 0, .45, (0, 0, 255), 2)
    cv2.imwrite(out, im, [cv2.IMWRITE_JPEG_QUALITY, 85])


def zoom(src, out, x0, y0, x1, y1, width=1600):
    cv2, np = _cv()
    im = cv2.imread(src)[y0:y1, x0:x1]
    s = width / im.shape[1]
    im = cv2.resize(im, (width, int(im.shape[0] * s)), interpolation=cv2.INTER_CUBIC if s > 1 else cv2.INTER_AREA)
    cv2.imwrite(out, im, [cv2.IMWRITE_JPEG_QUALITY, 90])


def overlay(path, out):
    cv2, np = _cv()
    d = json.load(open(path))
    root = os.path.dirname(os.path.dirname(os.path.abspath(path)))
    im = cv2.imread(os.path.join(root, d["tray_image"]))
    H, W = im.shape[:2]
    for c in d["compartments"]:
        it = d["items"][c["item_index"]]
        p0 = (int(c["x0"] * W), int(c["y0"] * H)); p1 = (int(c["x1"] * W), int(c["y1"] * H))
        cv2.rectangle(im, p0, p1, (0, 0, 255), 2)
        t = f'{it.get("slot_letter","?")} {it.get("label_short","")}'
        cv2.putText(im, t, (p0[0] + 4, p0[1] + 20), 0, .55, (0, 0, 0), 4)
        cv2.putText(im, t, (p0[0] + 4, p0[1] + 20), 0, .55, (255, 255, 255), 1)
    cv2.imwrite(out, im, [cv2.IMWRITE_JPEG_QUALITY, 85])


REQ_D = ["id", "column", "row", "half", "title", "description", "front_image", "tray_image",
         "tray_image_px", "compartments", "items"]
REQ_I = ["sku", "slot_letter", "name", "price_cents", "upc", "upc_source", "location", "label_short"]


def check(path):
    errs = []
    d = json.load(open(path))
    root = os.path.dirname(os.path.dirname(os.path.abspath(path)))
    for k in REQ_D:
        if k not in d: errs.append(f"missing drawer field {k}")
    if errs: return errs
    pre = {"left": "", "right": "R"}.get(d.get("wall", "left"), "?")
    if d.get("kind") == "bins":
        exp = pre + f'c{d["column"]:02d}bins'
    else:
        exp = pre + f'c{d["column"]:02d}r{d["row"]}' + {None: "", "L": "-left", "R": "-right"}[d["half"]]
    if d["id"] != exp: errs.append(f'id {d["id"]} should be {exp}')
    if os.path.basename(path) != d["id"] + ".json": errs.append("file name must be <id>.json")
    for k in ("front_image", "tray_image"):
        if d[k] and not os.path.exists(os.path.join(root, d[k])): errs.append(f"{k} not found: {d[k]}")
    if d["tray_image"] and os.path.exists(os.path.join(root, d["tray_image"])):
        from PIL import Image
        sz = list(Image.open(os.path.join(root, d["tray_image"])).size)
        if sz != list(d["tray_image_px"]): errs.append(f"tray_image_px {d['tray_image_px']} != actual {sz}")
    n = len(d["items"])
    seen = {}
    for j, it in enumerate(d["items"]):
        for k in REQ_I:
            if k not in it: errs.append(f"item {j} missing {k}")
        u = str(it.get("upc", ""))
        if u:
            if len(u) != 12 or not u.isdigit(): errs.append(f"item {j} upc not 12 digits: {u}")
            elif upc_check(u[:11]) != int(u[11]): errs.append(f"item {j} upc check digit wrong: {u} (expected {upc_check(u[:11])})")
            elif str(it.get("sku")) not in u: errs.append(f"item {j} sku {it.get('sku')} not inside upc {u}")
        if it.get("upc_source") not in ("read_from_label", "calculated_from_sku", None):
            errs.append(f"item {j} bad upc_source")
        if not isinstance(it.get("price_cents"), (int, type(None))): errs.append(f"item {j} price_cents must be int or null")
        if d.get("kind") == "bins":
            for k in ("box_price_cents", "box_qty"):
                if not isinstance(it.get(k), (int, type(None))): errs.append(f"item {j} {k} must be int or null")
        L = it.get("location")
        if L in seen: errs.append(f"location {L!r} used twice (items {seen[L]} and {j})")
        seen[L] = j
        sl = it.get("slot_letter")
        if sl is not None and (len(str(sl)) != 1 or str(sl) not in LETTERS):
            errs.append(f"item {j} slot_letter {sl!r} is not a single label letter (A-Z without I/O)")
    idx = [c["item_index"] for c in d["compartments"]]
    for c in d["compartments"]:
        if not (0 <= c["x0"] < c["x1"] <= 1 and 0 <= c["y0"] < c["y1"] <= 1):
            errs.append(f"compartment {c} out of range")
        if not 0 <= c["item_index"] < n: errs.append(f"compartment points at missing item {c['item_index']}")
    for j in range(n):
        if j not in idx and "note" not in d["items"][j]:
            errs.append(f"item {j} ({d['items'][j].get('slot_letter')}) has no compartment and no note")
    # overlaps (beyond small tolerance)
    cs = d["compartments"]
    for a in range(len(cs)):
        for b in range(a + 1, len(cs)):
            A, B = cs[a], cs[b]
            ox = min(A["x1"], B["x1"]) - max(A["x0"], B["x0"]); oy = min(A["y1"], B["y1"]) - max(A["y0"], B["y0"])
            if ox > .01 and oy > .01: errs.append(f"compartments for items {A['item_index']} and {B['item_index']} overlap")
    return errs


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit()
    cmd = a[0]
    def opt(name, default):
        if name in a: i = a.index(name); v = a[i + 1]; del a[i:i + 2]; return v
        return default
    if cmd == "rectify":
        rectify(a[1], a[2], int(a[3]), int(a[4]), a[5])
    elif cmd == "grid":
        step = int(opt("--step", 100)); width = int(opt("--width", 1400)); crop = opt("--crop", None)
        grid(a[1], a[2], step, tuple(map(int, crop.split(","))) if crop else None, width)
    elif cmd == "zoom":
        width = int(opt("--width", 1600)); zoom(a[1], a[2], *map(int, a[3:7]), width=width)
    elif cmd == "overlay":
        overlay(a[1], a[2])
    elif cmd == "check":
        bad = 0
        for p in a[1:]:
            e = check(p)
            print(("OK   " if not e else "FAIL ") + p)
            for x in e: print("     - " + x)
            bad += bool(e)
        sys.exit(1 if bad else 0)
    else:
        print(__doc__)

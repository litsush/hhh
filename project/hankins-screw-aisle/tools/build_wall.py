"""Build data.json and the web page from drawers/*.json.

    .venv/bin/python tools/build_wall.py

Reads every drawers/<id>.json, writes data.json (the full dataset) and web/
(index.html plus img/fronts and img/trays copied from images/). Upload web/
as-is to Cloudflare Pages.
"""
import glob, json, os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WALLS = [dict(key="left", name="Left side of the aisle", cols=30), dict(key="right", name="Right side of the aisle", cols=24)]


def main():
    os.chdir(ROOT)
    drawers = [json.load(open(p)) for p in glob.glob("drawers/*.json")]
    bins = [json.load(open(p)) for p in glob.glob("bins/*.json")]
    for d in drawers + bins: d.setdefault("wall", "left")
    order = {None: 0, "L": 1, "R": 2}; wo = {w["key"]: i for i, w in enumerate(WALLS)}
    drawers.sort(key=lambda d: (wo[d["wall"]], d["column"], d["row"], order[d["half"]]))
    bins.sort(key=lambda d: (wo[d["wall"]], d["column"]))
    full = {w["key"]: sorted({d["column"] for d in drawers if d["wall"] == w["key"]}) for w in WALLS}
    data = {
        "source": "Screw aisle pull-out drawer sections (Midwest Fastener displays): left wall 5 rows x 30 columns, right wall 5 rows x 24 columns",
        "coordinates": "Compartment rectangles are fractions (0-1) of the straightened tray image; x left to right, "
                       "y back of drawer (top) to front (bottom). Rows are numbered top (1) to bottom (5) of the wall, "
                       "columns left (1) to right as you face that wall. wall is \"left\" or \"right\" (the side of the aisle); "
                       "right-wall ids start with R.",
        "walls": WALLS,
        "drawer_count": len(drawers),
        "item_count": sum(len(d["items"]) for d in drawers),
        "drawers": drawers,
        "bin_unit_count": len(bins),
        "bin_count": sum(len(b["items"]) for b in bins),
        "bin_units": bins,
    }
    json.dump(data, open("data.json", "w"), indent=1, ensure_ascii=False)

    # web page
    os.makedirs("web/img", exist_ok=True)
    used = set()
    for d in drawers + bins:
        for k in ("front_image", "tray_image"):
            if d.get(k): used.add(d[k])
    for p in used:
        dst = os.path.join("web/img", os.path.relpath(p, "images"))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(p):
            shutil.copy2(p, dst)
    slim = []
    for d in drawers + bins:
        slim.append(dict(kind=d.get("kind", "drawer"), wl=d["wall"],
            id=d["id"], c=d["column"], r=d["row"], h=d["half"], t=d["title"], s=d["description"],
            f=d["front_image"].replace("images/", "img/", 1) if d["front_image"] else None,
            i=d["tray_image"].replace("images/", "img/", 1) if d["tray_image"] else None,
            px=d["tray_image_px"],
            cells=[[c["item_index"], c["x0"], c["y0"], c["x1"], c["y1"]] for c in d["compartments"]],
            items=[dict(n=it["name"], p=it["price_cents"], k=it["sku"] + ("-" + it["slot_letter"] if it.get("slot_letter") else ""),
                        u=it["upc"], w=it["location"], l=it["label_short"], **({"x": it["note"]} if it.get("note") else {}),
                        **({"bp": it.get("box_price_cents"), "bq": it.get("box_qty")} if it.get("box_qty") else {}))
                   for it in d["items"]],
        ))
    tpl = open("tools/wall_template.html").read()
    html = (tpl.replace("__DATA__", json.dumps([x for x in slim if x["kind"] == "drawer"], ensure_ascii=False, separators=(",", ":")))
               .replace("__BINS__", json.dumps([x for x in slim if x["kind"] == "bins"], ensure_ascii=False, separators=(",", ":")))
               .replace("__BINPRODUCTS__", f'{data["bin_count"]:,}').replace("__WALLS__", json.dumps(WALLS))
               .replace("__ITEMS__", f'{data["item_count"]:,}').replace("__DRAWERS__", str(len(drawers))))
    open("web/index.html", "w").write(html)
    json.dump(slim, open("web/drawers.json", "w"), ensure_ascii=False, separators=(",", ":"))
    for f in ("drawer.css", "drawer.js"):
        shutil.copy2(os.path.join("tools", f), os.path.join("web", f))
    # 3D viewer (only if the stitched scans exist: stitch.py + place_all.py + export_splat.py)
    # scan/*.splat are not in git (web/*.splat are); copy them only when a fresher export exists locally
    SPLATS = ["aisle.splat", "right.splat", "back.splat"]
    if os.path.exists("scan/wall_layout.json") and any(os.path.exists(f"scan/{f}") or os.path.exists(f"web/{f}") for f in SPLATS):
        Lw = json.load(open("scan/wall_layout.json"))
        if os.path.exists("scan/wall_layout_right.json"):
            Lr = json.load(open("scan/wall_layout_right.json"))
            Lw["slots"] = Lw["slots"] + Lr["slots"]; Lw["bin_slots"] = Lw.get("bin_slots", []) + Lr["bin_slots"]
        byslot = {}
        for d in drawers: byslot.setdefault((d["wall"], d["column"], d["row"]), []).append(d)
        slots = []
        for s in Lw["slots"]:
            ds = byslot.get((s.get("wall", "left"), s["column"], s["row"]), [])
            slots.append(dict(w=s.get("wall", "left"), c=s["column"], r=s["row"], q=s["corners_world"],
                              f=ds[0]["front_image"].replace("images/", "img/", 1) if ds else None,
                              d=[dict(id=d["id"], t=d["title"], n=len(d["items"])) for d in ds]))
        bslots = []
        byb = {(b["wall"], b["column"]): b for b in bins}
        for b in Lw.get("bin_slots", []):
            u = byb.get((b.get("wall", "left"), b["column"]))
            bslots.append(dict(w=b.get("wall", "left"), c=b["column"], q=b["corners_world"], f=u["tray_image"].replace("images/", "img/", 1) if u else None,
                               d=[dict(id=u["id"], t=u["title"], n=len(u["items"]))] if u else []))
        json.dump(dict(normal=Lw["wall_normal_world"], up=Lw["wall_up_world"], right=Lw["wall_right_world"], slots=slots, bins=bslots,
                       scans=[f for f in SPLATS if os.path.exists(f"scan/{f}") or os.path.exists(f"web/{f}")]),
                  open("web/wall3d.json", "w"), separators=(",", ":"))
        for f in SPLATS:
            if os.path.exists(f"scan/{f}") and (not os.path.exists(f"web/{f}") or os.path.getmtime(f"web/{f}") < os.path.getmtime(f"scan/{f}")):
                shutil.copy2(f"scan/{f}", f"web/{f}")
        shutil.copy2("tools/viewer_template.html", "web/3d.html")
    print(f"{len(bins)} bin units, {data['bin_count']} bins")
    print(f"{len(drawers)} drawers, {data['item_count']} items, columns done: {full}")


if __name__ == "__main__":
    main()

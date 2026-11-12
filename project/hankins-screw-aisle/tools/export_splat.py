"""Write compact .splat files (32 bytes/splat, no view-dependent colour) for the web viewer, one per part
of the store, each capped in size so it stays under Cloudflare's 25 MiB per-file limit.

    .venv/bin/python tools/export_splat.py

  scan/aisle_left_merged.ply -> scan/aisle.splat   left wall of the screw aisle   (stitch.py)
  scan/right_merged.ply      -> scan/right.splat   right wall + both endcaps      (place_all.py)
  scan/back_merged.ply       -> scan/back.splat    animal endcap + hinges aisle   (place_all.py)

Splats floating just in front of a drawer or bin photo are dropped (the photo replaces them). Everything
is cropped to a box around the aisle in King's wall frame (x along the aisle, y up, z toward the right wall).
"""
import sys, json, os
import numpy as np
sys.path.insert(0, 'tools'); import splat

F = json.load(open('scan/frames.json'))['King']; R = np.array(F['R']); c = np.array(F['c'])
W = lambda pts: (np.asarray(pts) - c) @ R.T


def quads(layout_file):
    L = json.load(open(layout_file))
    return (W([p for s in L['slots'] for p in s['corners_world']]), W([p for b in L.get('bin_slots', []) for p in b['corners_world']]))


def infront(w, q, toward):
    """splats within 0.004..0.12 units in front of the quad region q (toward = +1 means larger z is in front)."""
    lo, hi = q.min(0), q.max(0)
    face = hi[2] if toward > 0 else lo[2]
    dz = (w[:, 2] - face) * toward
    return (w[:, 0] > lo[0]) & (w[:, 0] < hi[0]) & (w[:, 1] > lo[1] - 0.01) & (w[:, 1] < hi[1] + 0.01) & (dz > 0.004) & (dz < 0.15)


def export(src, dst, box, max_splats, walls=()):
    p, a = splat.load(src); w = W(a[:, :3])
    keep = np.all((w > box[0]) & (w < box[1]), 1)
    for q, toward in walls:
        r = infront(w, q, toward); print(f'  {dst}: removed {int((keep & r).sum())} splats in front of photos'); keep &= ~r
    al = splat.alpha(p, a); keep &= al > 0.05
    a, al = a[keep], al[keep]
    si = p.index('scale_0'); sc = np.exp(a[:, si:si + 3])
    o = np.argsort(-(sc.prod(1) * al))[:max_splats]; a, al, sc = a[o], al[o], sc[o]
    col = (np.c_[splat.rgb(p, a), al] * 255).clip(0, 255).astype(np.uint8)
    ri = p.index('rot_0'); qq = a[:, ri:ri + 4]; qq = qq / np.linalg.norm(qq, axis=1, keepdims=True)
    buf = np.zeros(len(a), dtype=[('p', '<f4', 3), ('s', '<f4', 3), ('c', 'u1', 4), ('r', 'u1', 4)])
    buf['p'] = a[:, :3]; buf['s'] = sc; buf['c'] = col; buf['r'] = (qq * 128 + 128).clip(0, 255).astype(np.uint8)
    buf.tofile(dst); print(f'{dst}: {len(a)} splats, {buf.nbytes / 2**20:.1f} MiB (of {keep.sum()} in the crop)')


if __name__ == '__main__':
    dl, bl = quads('scan/wall_layout.json')
    dr, br = quads('scan/wall_layout_right.json')
    zr = dr[:, 2].mean()                      # right-wall drawer faces, ~2 units across the aisle
    x0 = min(dl[:, 0].min(), dr[:, 0].min()) - 0.5; x1 = max(dl[:, 0].max(), dr[:, 0].max()) + 0.6
    y0 = bl[:, 1].min() - 0.3; y1 = dl[:, 1].max() + 1.2
    # left wall: from behind its face to just short of the right wall
    export('scan/aisle_left_merged.ply', 'scan/aisle.splat',
           (np.array([x0, y0, dl[:, 2].min() - 0.35]), np.array([x1, y1, zr - 0.5])), 480000, [(dl, 1), (bl, 1)])
    # right wall: from the aisle middle to the back of its cabinets (the endcaps stick out a bit further)
    export('scan/right_merged.ply', 'scan/right.splat',
           (np.array([x0 - 1.0, y0, 0.6]), np.array([x1 + 1.2, y1, zr + 0.75])), 440000, [(dr, -1), (br, -1)])
    # hinges aisle behind the right wall, plus the animal endcap
    export('scan/back_merged.ply', 'scan/back.splat',
           (np.array([x0 - 1.5, y0, zr + 0.2]), np.array([x1 + 1.5, y1, zr + 3.0])), 260000)

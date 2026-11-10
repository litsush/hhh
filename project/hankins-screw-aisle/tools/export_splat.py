"""Write a compact .splat (32 bytes/splat, no view-dependent colour) of the merged scan, cropped to the
aisle around the drawer wall, capped in size so it fits Cloudflare Pages' 25 MiB file limit.
    .venv/bin/python tools/export_splat.py [max_splats]"""
import sys, json, numpy as np
sys.path.insert(0, 'tools'); import splat
MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 520000
p, a = splat.load('scan/aisle_left_merged.ply')
F = json.load(open('scan/frames.json'))['King']; R = np.array(F['R']); c = np.array(F['c'])
L = json.load(open('scan/wall_layout.json'))
q = np.array([pt for s in L['slots'] for pt in s['corners_world']]); wq = (q - c) @ R.T
w = (a[:, :3] - c) @ R.T
lo = wq.min(0) - [0.4, 1.2, 0.35]; hi = wq.max(0) + [0.4, 1.2, 1.2]
keep = np.all((w > lo) & (w < hi), 1)
# drop splats floating just in front of the drawer fronts: the drawer photos (drawn at +0.01) replace them
blo = wq.min(0); bhi = wq.max(0)
infront = (w[:, 0] > blo[0]) & (w[:, 0] < bhi[0]) & (w[:, 1] > blo[1] - 0.01) & (w[:, 1] < bhi[1] + 0.01) & (w[:, 2] > bhi[2] + 0.004) & (w[:, 2] < bhi[2] + 0.12)
print('removed in front of drawers:', int((keep & infront).sum()))
keep &= ~infront
al = splat.alpha(p, a); keep &= al > 0.05
a = a[keep]; al = al[keep]
si = p.index('scale_0'); sc = np.exp(a[:, si:si + 3])
imp = sc.prod(1) * al
o = np.argsort(-imp)[:MAX]; a, al, sc = a[o], al[o], sc[o]
col = (np.c_[splat.rgb(p, a), al] * 255).clip(0, 255).astype(np.uint8)
ri = p.index('rot_0'); qq = a[:, ri:ri + 4]; qq = qq / np.linalg.norm(qq, axis=1, keepdims=True)
rot = (qq * 128 + 128).clip(0, 255).astype(np.uint8)
buf = np.zeros(len(a), dtype=[('p', '<f4', 3), ('s', '<f4', 3), ('c', 'u1', 4), ('r', 'u1', 4)])
buf['p'] = a[:, :3]; buf['s'] = sc; buf['c'] = col; buf['r'] = rot
buf.tofile('scan/aisle.splat'); print(len(a), 'splats,', round(buf.nbytes / 2**20, 1), 'MiB; kept of cropped', keep.sum())

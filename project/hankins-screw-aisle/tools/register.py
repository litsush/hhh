"""Find how the Gaussian-splat scans fit together (pairwise 3D similarity transforms).

    .venv/bin/python tools/register.py render      # orthographic views of every scan from 24 directions
    .venv/bin/python tools/register.py match A B   # match scan A against scan B, print/save the transform

Method: each scan is rendered as straight-on (orthographic) pictures looking horizontally from 24
directions around its "up" axis, remembering which splat landed on each pixel. Two scans that saw the
same surface from the same side produce near-identical pictures up to zoom/shift, so SIFT features
are matched between every view of A and every view of B. Matched pixels are lifted back to the 3D
splat positions, and a scale+rotation+shift (similarity) is fitted with RANSAC.
Outputs go to scan/reg/ (views_<scan>.npz, pair_<A>__<B>.json).
"""
import sys, os, json, glob
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(__file__)); import splat

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
PLY = '/home/litsush/hhh/plys'
OUT = 'scan/reg'; os.makedirs(OUT, exist_ok=True)
MPP = float(os.environ.get("MPP", 0.003))
NYAW = 24


def key(name): return name.replace(' ', '_')


def core(name):
    p, a = splat.load(f'{PLY}/{name}.ply'); x = a[:, :3]; al = splat.alpha(p, a)
    m = np.median(x, 0); d = np.linalg.norm(x - m, axis=1)
    k = (d < np.percentile(d, 92)) & (al > .35)
    return x[k], splat.rgb(p, a)[k], m


def up_axis(x):
    """Gravity guess: -y with the dominant wall normal removed (walls are vertical)."""
    r = np.random.default_rng(0); sub = x[r.choice(len(x), min(40000, len(x)), replace=False)]
    best = (0, None)
    for _ in range(800):
        q = sub[r.choice(len(sub), 3, replace=False)]; n = np.cross(q[1] - q[0], q[2] - q[0]); L = np.linalg.norm(n)
        if L < 1e-9: continue
        n /= L
        if abs(n[1]) > .3: continue
        c = (np.abs((sub - q[0]) @ n) < .03).sum()
        if c > best[0]: best = (c, n)
    n = best[1]; u = np.array([0., -1, 0]); u -= u.dot(n) * n; return u / np.linalg.norm(u), n


def render_views(name):
    x, c, m = core(name); u, n = up_axis(x)
    t = np.cross(u, n); t /= np.linalg.norm(t)
    imgs, idxs, meta = [], [], []
    for k in range(NYAW):
        th = 2 * np.pi * k / NYAW; d = np.cos(th) * n + np.sin(th) * t  # viewer sits at +d, looks along -d
        fwd = -d; right = np.cross(fwd, u)
        pr, pu, dep = (x - m) @ right, (x - m) @ u, (x - m) @ fwd
        lo = np.percentile(pr, .5), np.percentile(pu, .5); hi = np.percentile(pr, 99.5), np.percentile(pu, 99.5)
        W, H = int((hi[0] - lo[0]) / MPP) + 1, int((hi[1] - lo[1]) / MPP) + 1
        px = ((pr - lo[0]) / MPP).astype(int); py = ((hi[1] - pu) / MPP).astype(int)
        ok = (px >= 0) & (px < W) & (py >= 0) & (py < H); ii = np.nonzero(ok)[0]
        o = ii[np.argsort(-dep[ii])]  # far first, near overwrites
        img = np.full((H, W, 3), 255, np.uint8); idx = np.full((H, W), -1, np.int64)
        img[py[o], px[o]] = (c[o] * 255).astype(np.uint8); idx[py[o], px[o]] = o
        hole = (idx < 0).astype(np.uint8); img = cv2.inpaint(img, hole, 2, cv2.INPAINT_TELEA)
        imgs.append(img); idxs.append(idx); meta.append(dict(th=th))
    np.savez_compressed(f'{OUT}/views_{key(name)}.npz', x=x.astype(np.float32), u=u, n=n, m=m,
                        **{f'img{k}': imgs[k] for k in range(NYAW)}, **{f'idx{k}': idxs[k] for k in range(NYAW)})
    for k in range(0, NYAW, 6): cv2.imwrite(f'{OUT}/view_{key(name)}_{k:02d}.jpg', imgs[k][..., ::-1])
    print(name, 'views', [i.shape[:2] for i in imgs[:1]])


def feats(name):
    z = np.load(f'{OUT}/views_{key(name)}.npz'); sift = cv2.SIFT_create(0, contrastThreshold=0.02)
    F = []
    for k in range(NYAW):
        g = cv2.cvtColor(z[f'img{k}'], cv2.COLOR_RGB2GRAY)
        kp, des = sift.detectAndCompute(g, None)
        F.append((np.float32([p.pt for p in kp]), des, z[f'idx{k}']))
    return z['x'], F


def lift(pts, idx, x):
    out = []; H, W = idx.shape
    for (px, py) in pts:
        i, j = int(round(py)), int(round(px))
        win = idx[max(0, i - 2):i + 3, max(0, j - 2):j + 3].ravel(); win = win[win >= 0]
        out.append(np.median(x[win], 0) if len(win) else [np.nan] * 3)
    return np.array(out)


def umeyama(A, B):
    """s, R, t with B ≈ s R A + t."""
    ma, mb = A.mean(0), B.mean(0); a, b = A - ma, B - mb
    U, S, Vt = np.linalg.svd(b.T @ a / len(A)); D = np.eye(3); D[2, 2] = np.sign(np.linalg.det(U @ Vt))
    R = U @ D @ Vt; s = (S * np.diag(D)).sum() / (a ** 2).sum() * len(A)
    return s, R, mb - s * R @ ma


def ransac_sim3(A, B, tol=0.04, it=4000, seed=0):
    r = np.random.default_rng(seed); best = (0, None)
    for _ in range(it):
        k = r.choice(len(A), 3, replace=False)
        if np.linalg.matrix_rank(A[k] - A[k[0]], tol=1e-3) < 2: continue
        s, R, t = umeyama(A[k], B[k])
        if not (.5 < s < 2): continue
        e = np.linalg.norm(s * (A @ R.T) + t - B, axis=1); inl = e < tol
        if inl.sum() > best[0]: best = (inl.sum(), inl)
    if best[1] is None: return None
    inl = best[1]
    for _ in range(3):
        s, R, t = umeyama(A[inl], B[inl]); e = np.linalg.norm(s * (A @ R.T) + t - B, axis=1); inl = e < tol
    return s, R, t, inl, e


def guided(pa, da, pb, db, M, rad=10):
    """Re-match using the rough 2D transform: only consider B features near where A's should land."""
    from scipy.spatial import cKDTree
    pred = pa @ M[:, :2].T + M[:, 2]; tree = cKDTree(pb)
    s1, s2 = [], []
    for k, cand in enumerate(tree.query_ball_point(pred, rad)):
        if not cand: continue
        d = np.linalg.norm(db[cand] - da[k], axis=1); o = np.argsort(d)
        if d[o[0]] > 300: continue
        if len(o) > 1 and d[o[0]] > .9 * d[o[1]]: continue
        s1.append(pa[k]); s2.append(pb[cand[o[0]]])
    return np.float32(s1), np.float32(s2)


def match(a, b):
    xa, Fa = feats(a); xb, Fb = feats(b)
    bf = cv2.BFMatcher(cv2.NORM_L2)
    PA, PB, src = [], [], []
    for i, (pa, da, ia) in enumerate(Fa):
        if da is None or len(da) < 50: continue
        for j, (pb, db, ib) in enumerate(Fb):
            if db is None or len(db) < 50: continue
            mm = bf.knnMatch(da, db, k=2); g = [m for m, n2 in (q for q in mm if len(q) == 2) if m.distance < .8 * n2.distance]
            if len(g) < 12: continue
            s1 = pa[[m.queryIdx for m in g]]; s2 = pb[[m.trainIdx for m in g]]
            M, inl = cv2.estimateAffinePartial2D(s1, s2, ransacReprojThreshold=6, maxIters=5000)
            if M is None or inl.sum() < 8: continue
            sc = np.hypot(M[0, 0], M[1, 0]); rot = np.degrees(np.arctan2(M[1, 0], M[0, 0]))
            if not (.6 < sc < 1.6) or abs(rot) > 12: continue
            s1, s2 = guided(pa, da, pb, db, M)
            if len(s1) < 20: continue
            M, inl = cv2.estimateAffinePartial2D(s1, s2, ransacReprojThreshold=4, maxIters=5000)
            if M is None: continue
            inl = inl.ravel() > 0
            if inl.sum() < 40: continue
            print(f'  view {i}-{j}: {inl.sum()} 2D inliers, zoom {np.hypot(M[0,0],M[1,0]):.3f}', flush=True)
            A3 = lift(s1[inl], ia, xa); B3 = lift(s2[inl], ib, xb); ok = ~np.isnan(A3).any(1) & ~np.isnan(B3).any(1)
            PA.append(A3[ok]); PB.append(B3[ok]); src += [(i, j)] * int(ok.sum())
    if not PA: print(a, b, 'no matches'); return None
    A3, B3 = np.vstack(PA), np.vstack(PB)
    res = ransac_sim3(A3, B3)
    if res is None: print(a, b, 'ransac failed'); return None
    s, R, t, inl, e = res
    views = {}
    for (i, j), k in zip(src, inl):
        if k: views[f'{i}-{j}'] = views.get(f'{i}-{j}', 0) + 1
    out = dict(a=a, b=b, s=float(s), R=R.tolist(), t=t.tolist(), inliers=int(inl.sum()), candidates=len(A3),
               rms=float(np.sqrt((e[inl] ** 2).mean())), views=dict(sorted(views.items(), key=lambda kv: -kv[1])[:6]))
    json.dump(out, open(f'{OUT}/pair_{key(a)}__{key(b)}.json', 'w'), indent=1)
    print(f'{a} -> {b}: inliers {out["inliers"]}/{out["candidates"]} scale {s:.4f} rms {out["rms"]:.4f} views {out["views"]}')
    return out


if __name__ == '__main__':
    if sys.argv[1] == 'render':
        for nm in sys.argv[2:]: render_views(nm)
    elif sys.argv[1] == 'match':
        match(sys.argv[2], sys.argv[3])

"""Put the right-hand wall scans and the back (animal endcap + hinges aisle) scans into the world,
which is King.ply's coordinate system (the left wall, see stitch.py). Also lays out the right wall's
drawer and bin photos in 3D.

    .venv/bin/python tools/place_all.py

Inputs: /home/litsush/hhh/plys/*.ply, scan/reg/pair_*.json (tools/register.py), scan/place.json
(numbers measured by hand, see below), scan/frames.json + scan/ortho_meta.json (King's wall frame).
Outputs: scan/right_merged.ply, scan/back_merged.ply (world coords, gitignored), scan/wall_layout_right.json.

How the pieces were tied together (2026-11-11):
- Group B = Screw right 1 + Screw right 2 + Endcap, joined by register.py (SIFT on rendered views).
  The long Screw right 1 scan drifted: its wall bows by ~0.3 units and tilts ~2.7 degrees along its
  length. B is "flattened" with a quadratic depth curve and a linear height ramp (place.json B.curve_quad,
  band_top_px), with zero correction at T_ref (the far, column-24 end).
- B -> world: Screw right 1 also saw ~4 columns of the LEFT wall across the aisle, near the left wall's
  column 1. That strip was matched to King's orthophoto (SIFT, 124 inliers), giving along-aisle position,
  height and scale (to_king.A/o/s); the across-aisle distance comes from the depth of the same strip
  (to_king.zoff). The two walls are assumed exactly parallel and facing.
- Group C = AnimalEndcap + Hinges1 + Hinges2 (register.py). AnimalEndcap saw the last 3 right-wall
  columns from the side; their posts and drawer-band top were matched by eye to the right-wall
  orthophoto (C.match), which places C at the column-24 end, behind the right wall.
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__)); import splat

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
PLY = '/home/litsush/hhh/plys'
P = json.load(open('scan/place.json')); B = P['B']; C = P['C']; K2 = P['to_king']
F = json.load(open('scan/frames.json'))['King']; R1 = np.array(F['R']); c1 = np.array(F['c'])
key = lambda s: s.replace(' ', '_')


def pair(a, b):
    p = json.load(open(f'scan/reg/pair_{key(a)}__{key(b)}.json')); M = np.eye(4)
    M[:3, :3] = p['s'] * np.array(p['R']); M[:3, 3] = p['t']; return M


def quat_mul(q, r):
    w0, x0, y0, z0 = q.T; w1, x1, y1, z1 = r.T
    return np.stack([w0*w1-x0*x1-y0*y1-z0*z1, w0*x1+x0*w1+y0*z1-z0*y1, w0*y1-x0*z1+y0*w1+z0*x1, w0*z1+x0*y1-y0*x1+z0*w1], 1)


def rot_to_quat(R):
    w = np.sqrt(max(0, 1 + R[0, 0] + R[1, 1] + R[2, 2])) / 2
    x = np.copysign(np.sqrt(max(0, 1 + R[0, 0] - R[1, 1] - R[2, 2])) / 2, R[2, 1] - R[1, 2])
    y = np.copysign(np.sqrt(max(0, 1 - R[0, 0] + R[1, 1] - R[2, 2])) / 2, R[0, 2] - R[2, 0])
    z = np.copysign(np.sqrt(max(0, 1 - R[0, 0] - R[1, 1] + R[2, 2])) / 2, R[1, 0] - R[0, 1])
    return np.array([w, x, y, z])


def apply_linear(props, a, L, tvec):
    """p -> L p + t for a whole splat array; L = scale * rotation."""
    U, S, Vt = np.linalg.svd(L); Rm = U @ Vt; s = S.mean()
    a = a.copy(); a[:, :3] = a[:, :3] @ L.T + tvec
    si = props.index('scale_0'); a[:, si:si + 3] += np.log(s)
    ri = props.index('rot_0'); q = a[:, ri:ri + 4]; q = q / np.linalg.norm(q, axis=1, keepdims=True)
    a[:, ri:ri + 4] = quat_mul(np.repeat(rot_to_quat(Rm)[None], len(q), 0), q)
    return a


# ---- group B (right wall) -------------------------------------------------------------------------
Bm, Bt, Bu, Bn = (np.array(B[k]) for k in 'mtun'); BF = np.stack([Bt, Bu, Bn])   # rows: T, U, N axes
lo0, lo1 = B['ortho_lo']; H = B['ortho_H']; mpp = B['mpp']
px_T = lambda px: lo0 + px * mpp
px_U = lambda py: lo1 + (H - 1 - py) * mpp


def lin(pts, x):
    (x0, y0), (x1, y1) = pts; return y0 + (y1 - y0) * (np.asarray(x) - x0) / (x1 - x0)


def curve(T): return np.polyval(B['curve_quad'], np.clip(T, *B['curve_range']))
def utop_raw(T):  # band-top height (raw B coords) along the wall
    T = np.clip(T, *B['curve_range']); px = (T - lo0) / mpp
    return px_U(lin(B['band_top_px'], px))


Tref = B['T_ref']


def flatten(w):
    """raw B wall coords (T,U,N) -> flattened (bow and tilt removed, unchanged at T_ref)."""
    w = w.copy(); w[:, 2] -= curve(w[:, 0]) - curve(Tref); w[:, 1] -= utop_raw(w[:, 0]) - utop_raw(Tref); return w


A = np.array(K2['A']); o = np.array(K2['o']); sB = K2['sB']; s = K2['s']
# flattened B wall coords -> King wall coords (linear part) and then -> world
Kl = np.array([[-sB * A[0, 0], sB * A[0, 1], 0], [-sB * A[1, 0], sB * A[1, 1], 0], [0, 0, -s]])
Kt = np.array([o[0], o[1], K2['zoff']])


def bflat_to_world(w):
    return (w @ Kl.T + Kt) @ R1 + c1


L_B = R1.T @ Kl  # world = L_B @ wflat + R1.T @ Kt + c1


def build_B():
    Ms = {'Screw right 1': np.eye(4), 'Screw right 2': pair('Screw right 2', 'Screw right 1')}
    Ms['Endcap'] = Ms['Screw right 2'] @ pair('Endcap', 'Screw right 2')
    out = []
    for nm, M in Ms.items():
        p, a = splat.load(f'{PLY}/{nm}.ply')
        a = apply_linear(p, a, M[:3, :3], M[:3, 3])
        w = (a[:, :3] - Bm) @ BF.T
        lo, hi = B['cuts'][nm]; k = (w[:, 0] >= lo) & (w[:, 0] < hi)
        d = w[:, 2] - curve(w[:, 0]); k &= (d < B['blob_d']) & (d > -1.5)   # drop the far wall seen across the aisle
        a, w = a[k], w[k]
        wf = flatten(w)
        a[:, :3] = bflat_to_world(wf)
        # rotate/scale splat shapes with the linear part (positions already done)
        U_, S_, Vt_ = np.linalg.svd(L_B); Rm = U_ @ Vt_
        si = p.index('scale_0'); a[:, si:si + 3] += np.log(S_.mean())
        ri = p.index('rot_0'); q = a[:, ri:ri + 4]; q = q / np.linalg.norm(q, axis=1, keepdims=True)
        a[:, ri:ri + 4] = quat_mul(np.repeat(rot_to_quat(Rm)[None], len(q), 0), q)
        print(f'B {nm}: kept {k.sum()} of {len(k)}'); out.append(a)
    return p, np.vstack(out)


# ---- group C (animal endcap + hinges aisle, behind the right wall) ------------------------------------
Cm, Ct, Cu, Cn = (np.array(C[k]) for k in 'mtun'); CF = np.stack([Ct, Cu, Cn])
cl0, cl1 = C['seg_lo']; CH = C['seg_H']


def c_to_braw():
    """2D similarity in the wall plane from the two matched points, depth from the drawer-face planes."""
    (pc1, pb1), (pc2, pb2) = C['match']
    c1_ = np.array([cl0 + pc1[0] * mpp, cl1 + (CH - 1 - pc1[1]) * mpp]); c2_ = np.array([cl0 + pc2[0] * mpp, cl1 + (CH - 1 - pc2[1]) * mpp])
    b1 = np.array([px_T(pb1[0]), px_U(pb1[1])]); b2 = np.array([px_T(pb2[0]), px_U(pb2[1])])
    dc, db = c2_ - c1_, b2 - b1
    sc = np.linalg.norm(db) / np.linalg.norm(dc); th = np.arctan2(db[1], db[0]) - np.arctan2(dc[1], dc[0])
    R2 = sc * np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]]); t2 = b1 - R2 @ c1_
    Tj = b2[0]; nB = curve(Tj) + B['face_d']
    M = np.eye(3) * sc; M[:2, :2] = R2
    tv = np.array([t2[0], t2[1], nB - sc * C['face_n']])
    return M, tv, Tj, sc


def build_C():
    Ms = {'AnimalEndcap': np.eye(4), 'Hinges1': pair('Hinges1', 'AnimalEndcap')}
    Ms['Hinges2'] = Ms['Hinges1'] @ pair('Hinges2', 'Hinges1')
    M3, tv, Tj, sc = c_to_braw()
    # world = L_B @ flat(braw) ...; flatten at the junction is a constant offset
    off = np.array([0, -(utop_raw(Tj) - utop_raw(Tref)), -(curve(Tj) - curve(Tref))])
    Lc = L_B @ M3 @ CF  # C scan coords -> world (linear)
    tc = L_B @ (M3 @ (-CF @ Cm) + tv + off) + R1.T @ Kt + c1
    out = []
    for nm, M in Ms.items():
        p, a = splat.load(f'{PLY}/{nm}.ply')
        a = apply_linear(p, a, M[:3, :3], M[:3, 3])
        w = (a[:, :3] - Cm) @ CF.T
        lo, hi = C['cuts'][nm]; k = (w[:, 0] >= lo) & (w[:, 0] < hi)
        a = apply_linear(p, a[k], Lc, tc)
        # drop what C saw of the screw-aisle side (Screw right 1 already has it): points in front of the
        # back face of the screw-side cabinets, along the drawer run
        wf = ((a[:, :3] - c1) @ R1.T - Kt) @ np.linalg.inv(Kl).T
        dup = (wf[:, 0] < Tj + 0.03) & (wf[:, 2] > B['face_d'] - 0.3)
        a = a[~dup]
        print(f'C {nm}: kept {len(a)} of {len(k)} (dropped {dup.sum()} duplicates of the right wall)'); out.append(a)
    print(f'C scale to B {sc:.4f}')
    return p, np.vstack(out)


# ---- right wall drawer/bin layout ----------------------------------------------------------------
def layout():
    drawers = {}
    import glob
    for f in glob.glob('drawers/R*.json'):
        d = json.load(open(f)); drawers.setdefault((d['column'], d['row']), []).append(d)
    top = utop_raw(Tref); bot = top - (lin(B['band_bottom_px'], 320) - lin(B['band_top_px'], 320)) * mpp
    face = B['face_d'] + curve(Tref); binf = B['bins_d'] + curve(Tref)
    T = lambda k: px_T(B['post0_px'] + (k - 1) * B['post_step_px'])
    W = lambda t_, u_, n_: bflat_to_world(np.array([[t_, u_, n_]]))[0].round(4).tolist()
    slots, bins = [], []
    for col in range(1, 25):
        tl, tr = T(col), T(col + 1)
        for row in range(1, 6):
            y0 = top + (bot - top) * (row - 1) / 5; y1 = top + (bot - top) * row / 5
            ds = sorted(drawers.get((col, row), []), key=lambda d: {None: 0, 'L': 1, 'R': 2}[d['half']])
            slots.append(dict(wall='right', column=col, row=row, drawer_ids=[d['id'] for d in ds],
                              front_image=ds[0]['front_image'] if ds else None,
                              corners_world=[W(tl, y0, face), W(tr, y0, face), W(tr, y1, face), W(tl, y1, face)]))
        bt = bot - 8 * mpp; bb = bt - 300 * mpp
        bins.append(dict(wall='right', column=col, bin_id=f'Rc{col:02d}bins',
                         corners_world=[W(tl, bt, binf), W(tr, bt, binf), W(tr, bb, binf), W(tl, bb, binf)]))
    n = (R1.T @ -Kl[:, 2]); n /= np.linalg.norm(n)
    json.dump(dict(note='Right-wall drawer-front and bin quads in world (King) coords; corner order top-left, top-right, '
                        'bottom-right, bottom-left as seen facing the right wall.',
                   wall_normal_world=(-R1[2]).round(5).tolist(), slots=slots, bin_slots=bins),
              open('scan/wall_layout_right.json', 'w'), indent=1)
    return slots


if __name__ == '__main__':
    layout()
    p, aB = build_B(); splat.save('scan/right_merged.ply', p, aB)
    p, aC = build_C(); splat.save('scan/back_merged.ply', p, aC)
    print('right', len(aB), 'back', len(aC))

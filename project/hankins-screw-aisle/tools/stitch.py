"""Merge the two Gaussian-splat scans (King.ply = left part of the aisle, King2.ply = right part)
into one splat in King's coordinate system, and place every drawer of the wall in 3D.

    .venv/bin/python tools/stitch.py

Inputs:  /home/litsush/hhh/plys/King.ply, King2.ply, scan/frames.json (wall planes, from wallframe.py
         + manual mirror fix), scan/ortho_meta.json + scan/align2d.json (orthophoto match, from ortho.py).
Outputs: scan/aisle_left_merged.ply   merged splat
         scan/wall_layout.json        3D corners of every drawer front (merged/King coordinates)
         scan/wall_preview.jpg        straight-on picture of the merged wall with drawer photos pasted on
How the drawer grid was found: column edges (posts) and the band top/bottom were read by eye from the
stitched orthophoto (3 mm per pixel, King ortho pixel coords) — see POSTS / TOP / BOTTOM below.
"""
import json, os, glob, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__)); import splat

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
F = json.load(open('scan/frames.json')); OM = json.load(open('scan/ortho_meta.json'))
M = np.array(json.load(open('scan/align2d.json'))['M'])

# Post x positions (left edge of each column) in King-ortho pixels; col 1 left edge is outside the scan.
POSTS = [-48, 50, 152, 250, 347, 446, 548, 645, 745, 845, 943, 1044, 1145, 1243, 1342, 1443, 1541, 1640,
         1739, 1842, 1938, 2039, 2138, 2236, 2337, 2436, 2528, 2631, 2734, 2835, 2936]
TOP = ((0, 283), (3000, 279))      # (ortho x, ortho y) top edge of row 1, linearly interpolated
BOTTOM = ((0, 384), (3000, 370))   # bottom edge of row 5
CUT_PX = 2190                      # use King left of this ortho x, King2 right of it


def lerp(p, x):
    (x0, y0), (x1, y1) = p
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def px_to_wall(px, py, name='King'):
    o = OM[name]; H = o['size'][1]
    return np.array([o['lo'][0] + px * o['mpp'], o['lo'][1] + (H - 1 - py) * o['mpp']])


def wall_to_px(w, name):
    o = OM[name]; H = o['size'][1]
    return np.c_[(w[:, 0] - o['lo'][0]) / o['mpp'], (H - 1) - (w[:, 1] - o['lo'][1]) / o['mpp']]


def frame(name):
    return np.array(F[name]['R']), np.array(F[name]['c'])


def king2_to_king_affine():
    """Return (A, b) with p_King = A @ p_King2 + b, A = s * rotation."""
    R1, c1 = frame('King'); R2, c2 = frame('King2')
    s = float(np.hypot(M[0, 0], M[1, 0]))
    def f(w2):  # King2 wall coords -> King wall coords
        p2 = wall_to_px(w2[None, :2], 'King2')[0]
        p1 = M[:, :2] @ p2 + M[:, 2]
        o = OM['King']; H = o['size'][1]
        return np.array([o['lo'][0] + p1[0] * o['mpp'], o['lo'][1] + (H - 1 - p1[1]) * o['mpp'], s * w2[2]])
    w0 = np.zeros(3); f0 = f(w0)
    L = np.stack([f(np.eye(3)[i]) - f0 for i in range(3)], 1)       # wall2 -> wall1 linear part
    A = R1.T @ L @ R2                                                # world2 -> world1
    b = R1.T @ (f0 - L @ (R2 @ c2)) + c1
    return A, b, s


def quat_mul(q, r):
    w0, x0, y0, z0 = q.T; w1, x1, y1, z1 = r.T
    return np.stack([w0*w1-x0*x1-y0*y1-z0*z1, w0*x1+x0*w1+y0*z1-z0*y1, w0*y1-x0*z1+y0*w1+z0*x1, w0*z1+x0*y1-y0*x1+z0*w1], 1)


def rot_to_quat(R):
    w = np.sqrt(max(0, 1 + R[0, 0] + R[1, 1] + R[2, 2])) / 2
    x = np.copysign(np.sqrt(max(0, 1 + R[0, 0] - R[1, 1] - R[2, 2])) / 2, R[2, 1] - R[1, 2])
    y = np.copysign(np.sqrt(max(0, 1 - R[0, 0] + R[1, 1] - R[2, 2])) / 2, R[0, 2] - R[2, 0])
    z = np.copysign(np.sqrt(max(0, 1 - R[0, 0] - R[1, 1] + R[2, 2])) / 2, R[1, 0] - R[0, 1])
    return np.array([w, x, y, z])


def merge():
    A, b, s = king2_to_king_affine()
    U, S, Vt = np.linalg.svd(A); Rot = U @ Vt
    p1, a1 = splat.load('/home/litsush/hhh/plys/King.ply')
    p2, a2 = splat.load('/home/litsush/hhh/plys/King2.ply')
    assert p1 == p2
    R1, c1 = frame('King')
    cut_wx = px_to_wall(CUT_PX, 0)[0]
    a2 = a2.copy()
    a2[:, :3] = a2[:, :3] @ A.T + b
    for k in ('nx', 'ny', 'nz'):
        pass  # normals are unused by splat renderers
    si = p2.index('scale_0'); a2[:, si:si + 3] += np.log(s)
    ri = p2.index('rot_0'); q = a2[:, ri:ri + 4]; q = q / np.linalg.norm(q, axis=1, keepdims=True)
    a2[:, ri:ri + 4] = quat_mul(np.repeat(rot_to_quat(Rot)[None], len(q), 0), q)
    # view-dependent colour (f_rest) is left unrotated; the rotation is small, so the error is minor
    w1 = (a1[:, :3] - c1) @ R1.T; w2 = (a2[:, :3] - c1) @ R1.T
    keep1 = w1[:, 0] < cut_wx; keep2 = w2[:, 0] >= cut_wx
    out = np.vstack([a1[keep1], a2[keep2]])
    splat.save('scan/aisle_left_merged.ply', p1, out)
    print(f'merged: {keep1.sum()} from King + {keep2.sum()} from King2 = {len(out)} splats; King2 scale {s:.4f}')
    return R1, c1


def wall_depth():
    """Median wall-normal offset of the drawer fronts in King's frame."""
    p, a = splat.load('/home/litsush/hhh/plys/King.ply'); R1, c1 = frame('King')
    w = (a[:, :3] - c1) @ R1.T
    y0 = px_to_wall(0, TOP[0][1])[1]; y1 = px_to_wall(0, BOTTOM[0][1])[1]
    x0 = px_to_wall(POSTS[1], 0)[0]; x1 = px_to_wall(POSTS[20], 0)[0]
    k = (w[:, 0] > x0) & (w[:, 0] < x1) & (w[:, 1] < y0) & (w[:, 1] > y1) & (splat.alpha(p, a) > .5) & (np.abs(w[:, 2]) < .3)
    return float(np.median(w[k, 2]))


def layout(R1, c1, z):
    drawers = {}
    for f in glob.glob('drawers/*.json'):
        d = json.load(open(f)); drawers.setdefault((d['column'], d['row']), []).append(d)
    out = []
    for col in range(1, 31):
        xl, xr = POSTS[col - 1], POSTS[col]
        for row in range(1, 6):
            def corner(x, r):
                t, btm = lerp(TOP, x), lerp(BOTTOM, x)
                y = t + (btm - t) * r / 5
                w = np.r_[px_to_wall(x, y), z]
                return (R1.T @ w + c1).round(4).tolist(), (x, y)
            q = [corner(xl, row - 1), corner(xr, row - 1), corner(xr, row), corner(xl, row)]
            ds = sorted(drawers.get((col, row), []), key=lambda d: {None: 0, 'L': 1, 'R': 2}[d['half']])
            out.append(dict(column=col, row=row, drawer_ids=[d['id'] for d in ds],
                            front_image=ds[0]['front_image'] if ds else None,
                            corners_world=[c[0] for c in q], corners_ortho_px=[c[1] for c in q]))
    n = R1[2]
    json.dump(dict(note='Drawer-front quads in the merged splat coordinates (same as King.ply). Corner order: '
                        'top-left, top-right, bottom-right, bottom-left as seen facing the wall. '
                        'Scale is the scan\'s own units (not metres).',
                   wall_normal_world=n.round(5).tolist(), wall_up_world=R1[1].round(5).tolist(),
                   wall_right_world=R1[0].round(5).tolist(), slots=out), open('scan/wall_layout.json', 'w'), indent=1)
    return out


def preview(slots):
    import cv2
    from PIL import Image
    base = cv2.imread('scan/mosaic.jpg')
    for s in slots:
        if not s['front_image']: continue
        img = cv2.imread(s['front_image']); h, w = img.shape[:2]
        dst = np.float32(s['corners_ortho_px']); src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
        Hm = cv2.getPerspectiveTransform(src, dst)
        warped = cv2.warpPerspective(img, Hm, (base.shape[1], base.shape[0]))
        mask = cv2.warpPerspective(np.full((h, w), 255, np.uint8), Hm, (base.shape[1], base.shape[0])) > 0
        base[mask] = warped[mask]
    cv2.imwrite('scan/wall_preview.jpg', base, [cv2.IMWRITE_JPEG_QUALITY, 88])


def mosaic():
    import cv2
    a = cv2.imread('scan/ortho_King.png'); b = cv2.imread('scan/ortho_King2.png')
    W = int(max(a.shape[1], M[0, 2] + b.shape[1] * np.hypot(M[0, 0], M[1, 0])) + 10)
    canvas = np.full((a.shape[0], W, 3), 255, np.uint8); canvas[:, :a.shape[1]] = a
    wb = cv2.warpAffine(b, M, (W, a.shape[0]), borderValue=(255, 255, 255))
    m = wb.sum(2) < 760; m[:, :CUT_PX] = False; canvas[m] = wb[m]
    cv2.imwrite('scan/mosaic.jpg', canvas, [cv2.IMWRITE_JPEG_QUALITY, 90])


if __name__ == '__main__':
    mosaic()
    R1, c1 = merge()
    z = wall_depth(); print('drawer-front depth offset', round(z, 4))
    slots = layout(R1, c1, z); preview(slots)
    print('slots with photos:', sum(1 for s in slots if s['front_image']), 'of', len(slots))

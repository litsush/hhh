"""Fit the shelf-facade plane of a splat and render a straight-on orthophoto of it."""
import sys, json, numpy as np
sys.path.insert(0, __file__.rsplit('/',1)[0]); import splat
def ransac_plane(x, it=400, tol=0.03, seed=0):
    r=np.random.default_rng(seed); best=(0,None)
    for _ in range(it):
        p=x[r.choice(len(x),3,replace=False)]; n=np.cross(p[1]-p[0],p[2]-p[0]); L=np.linalg.norm(n)
        if L<1e-9: continue
        n/=L; c=(np.abs((x-p[0])@n)<tol).sum()
        if c>best[0]: best=(c,(n,p[0]))
    n,p0=best[1]; inl=np.abs((x-p0)@n)<tol
    c=x[inl].mean(0); u,s,vt=np.linalg.svd(x[inl]-c,full_matrices=False); n=vt[2]
    return n,c,inl
def frame(name, up_hint):
    p,a=splat.load(f'/home/litsush/hhh/plys/{name}.ply'); x=a[:,:3]
    m=np.median(x,0); d=np.linalg.norm(x-m,axis=1); core=(d<np.percentile(d,90))&(splat.alpha(p,a)>.5)
    sub=x[core][::5]
    n,c,inl=ransac_plane(sub)
    # orient: up = hint projected into plane, x = up × n
    up=np.array(up_hint,float); up-=up.dot(n)*n; up/=np.linalg.norm(up); ex=np.cross(up,n); ex/=np.linalg.norm(ex)
    # make normal face the camera side (side with more points in front)
    side=np.sign(np.median((sub-c)@n)); 
    R=np.stack([ex,up,n])  # rows: wall x, wall y, wall normal
    return dict(name=name,R=R.tolist(),c=c.tolist(),inlier_frac=float(inl.mean()),side=float(side))
if __name__=='__main__':
    out={}
    for nm in ['King','King2']:
        out[nm]=frame(nm,[0,-1,0]); print(nm,out[nm]['inlier_frac'],np.round(out[nm]['R'],3).tolist())
    json.dump(out,open('scan/frames.json','w'),indent=1)

import sys,json,numpy as np
sys.path.insert(0,'tools');import splat
from PIL import Image
F=json.load(open('scan/frames.json'))
def wall_coords(name):
    p,a=splat.load(f'/home/litsush/hhh/plys/{name}.ply'); f=F[name]; R=np.array(f['R']); c=np.array(f['c'])
    w=(a[:,:3]-c)@R.T; return p,a,w
def ortho(name,mpp=0.003,band=(-0.25,0.4),out=None):
    p,a,w=wall_coords(name); col=splat.rgb(p,a); al=splat.alpha(p,a)
    z=w[:,2]*F[name]['side']  # >0 = toward camera
    k=(al>.3)&(z>band[0])&(z<band[1])
    lo=np.percentile(w[k,:2],1,axis=0); hi=np.percentile(w[k,:2],99,axis=0)
    W,H=((hi-lo)/mpp).astype(int)+1
    px=((w[k,0]-lo[0])/mpp).astype(int); py=(H-1-((w[k,1]-lo[1])/mpp)).astype(int)
    ok=(px>=0)&(px<W)&(py>=0)&(py<H); px,py,zz,cc=px[ok],py[ok],z[k][ok],col[k][ok]
    o=np.argsort(zz); img=np.full((H,W,3),255,np.uint8); img[py[o],px[o]]=(cc[o]*255).astype(np.uint8)
    # fill small holes
    import cv2; m=(img.sum(2)==765).astype(np.uint8); img=cv2.inpaint(img,m,2,cv2.INPAINT_TELEA)
    Image.fromarray(img).save(out or f'scan/ortho_{name}.png')
    return dict(lo=lo.tolist(),mpp=mpp,size=[int(W),int(H)])
if __name__=='__main__':
    meta={n:ortho(n) for n in ['King','King2']}; json.dump(meta,open('scan/ortho_meta.json','w'),indent=1); print(meta)

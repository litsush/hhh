"""Gaussian-splat PLY helpers: load/save, and render quick point previews."""
import numpy as np, sys
def load(p):
    with open(p,'rb') as f:
        h=b''
        while not h.endswith(b'end_header\n'): h+=f.readline()
        props=[l.split()[-1].decode() for l in h.split(b'\n') if l.startswith(b'property')]
        n=int([l for l in h.split(b'\n') if l.startswith(b'element vertex')][0].split()[-1])
        a=np.fromfile(f,dtype=np.float32,count=n*len(props)).reshape(n,len(props))
    return props,a
def save(p,props,a):
    with open(p,'wb') as f:
        f.write(('ply\nformat binary_little_endian 1.0\nelement vertex %d\n'%len(a)+''.join('property float %s\n'%x for x in props)+'end_header\n').encode())
        a.astype(np.float32).tofile(f)
def rgb(props,a):
    i=props.index('f_dc_0'); return np.clip(0.5+0.28209479*a[:,i:i+3],0,1)
def alpha(props,a): return 1/(1+np.exp(-a[:,props.index('opacity')]))
def render(x,c,out,res=1400,axes=(0,1),depth=2,flip_y=True,lo=None,hi=None):
    """Orthographic point render: x Nx3 in some frame, c Nx3 colors. Nearest (smallest depth) wins."""
    from PIL import Image
    u,v,d=x[:,axes[0]],x[:,axes[1]],x[:,depth]
    lo=lo if lo is not None else np.percentile(np.c_[u,v],0.5,axis=0); hi=hi if hi is not None else np.percentile(np.c_[u,v],99.5,axis=0)
    s=res/max(hi-lo); W,H=int((hi[0]-lo[0])*s)+1,int((hi[1]-lo[1])*s)+1
    px=((u-lo[0])*s).astype(int); py=((v-lo[1])*s).astype(int)
    if flip_y: py=H-1-py
    k=(px>=0)&(px<W)&(py>=0)&(py<H); px,py,d,cc=px[k],py[k],d[k],c[k]
    o=np.argsort(-d); img=np.full((H,W,3),255,np.uint8)
    img[py[o],px[o]]=(cc[o]*255).astype(np.uint8)
    Image.fromarray(img).save(out); return lo,hi,s

s=open('build.py').read()
a=s.index('S=[');b=s.index('def chk');s=s[:a]+s[b:]
a=s.index('def half');b=s.index("b=lambda f")
new='''S1=['1/4','3/8','1/2','3/4','1','1-1/4','1-1/2']
S2=['3/16','1/4','3/8','1/2','3/4','1','1-1/4']
ST=['3/8','1/2','3/4','1','1-1/4','1-1/2','2']
def fm(c): return f'${c/100:.2f}' if c>=100 else f'{c}¢'
def half(mach,base,head,th,zs,bs,z,b,zc,bc):
    out=[]
    for r,(mat,sz,pr,cd,off,row) in enumerate([('Zinc',zs,z,zc,1,'Back'),('Brass',bs,b,bc,11,'Front')]):
        assert len(pr)==8 and len(cd)==8
        for c in range(8):
            sku=base+off+c; u=f'738287{sku}'; assert chk(u)==int(cd[c]),(u,cd[c],chk(u))
            nut=c==7
            nm=f'{th} {mat.lower()} hex nuts' if nut else f'{th} x {sz[c]} {mat.lower()} {head} head'
            out.append(dict(name=nm,short='Nuts' if nut else sz[c],price=fm(pr[c]),sku=f'{sku}-{LET[r*8+c]}',upc=f'7 38287 {sku} {cd[c]}',where=f'{mach}, {row.lower()} row, column {c+1}'))
    return out
def dw(m1,b1,m2,b2,th,zs,bs,p,c): 
    return half(f'Machine {m1}',b1,'round',th,zs,bs,*p[:2],*c[:2])+half(f'Machine {m2}',b2,'flat',th,zs,bs,*p[2:],*c[2:])
T=[
 dw(1,62160,21,62140,'4-40',S1,S2,[[25,26,28,29,31,32,33,23],[32,32,35,40,44,46,50,29],[25,26,28,29,31,32,33,23],[34,35,40,44,47,52,55,29]],['74185296','63074185','96307418','85296307']),
 dw(2,62000,22,61980,'6-32',ST,ST,[[24,26,27,29,31,33,34,23],[32,35,41,45,47,53,63,32],[24,25,26,29,30,31,34,23],[35,41,50,54,58,63,75,32]],['63074185','52963074','29630741','18529630']),
 dw(3,61760,23,61740,'8-32',ST,ST,[[25,28,29,29,32,35,45,23],[44,50,56,62,64,75,85,40],[25,28,29,30,32,35,42,23],[50,56,62,67,75,79,105,40]],['07418529','96307418','29630741','18529630']),
 dw(4,61480,24,61460,'10-24',ST,ST,[[25,28,29,32,32,33,42,23],[47,55,64,69,79,85,95,43],[25,27,29,32,33,36,42,23],[56,63,75,79,89,99,119,43]],['74185296','63074185','96307418','85296307']),
 dw(5,61440,25,61420,'10-32',ST,ST,[[26,28,28,32,32,33,44,23],[47,57,64,75,79,89,95,43],[25,28,28,31,33,36,42,23],[56,63,75,79,89,99,119,43]],['18529630','07418529','30741852','29630741']),
]
G=[([0,212,425,638,800],[[0,146,295,443,590,738,892,1047,1200],[0,135,287,433,585,735,885,1037,1197],[0,122,275,425,578,733,888,1037,1200],[0,112,268,415,570,722,880,1042,1200]]),
 ([0,215,428,645,800],[[0,165,312,462,610,758,905,1055,1200],[0,165,315,465,612,762,908,1058,1200],[0,158,310,462,612,760,908,1055,1200],[0,158,308,460,605,758,905,1055,1200]]),
 ([0,187,382,585,800],[[45,190,332,470,605,740,880,1018,1162],[22,172,318,460,600,742,882,1020,1172],[0,160,305,448,597,740,882,1020,1180],[0,135,295,440,590,740,885,1035,1200]]),
 ([0,183,382,585,800],[[38,185,320,458,598,733,872,1010,1155],[25,175,322,462,603,742,878,1015,1170],[8,165,312,455,600,738,878,1022,1182],[0,152,302,448,598,742,888,1035,1200]]),
 ([0,183,380,582,800],[[30,177,315,452,592,728,865,1005,1150],[25,175,315,455,598,730,870,1008,1165],[5,160,303,447,592,735,880,1018,1172],[0,155,302,448,595,738,885,1030,1195]])]
SUB=['4-40 coarse slotted screws: round head (62160), flat head (62140)','6-32 coarse slotted screws: round head (62000), flat head (61980)','8-32 coarse slotted screws: round head (61760), flat head (61740)','10-24 coarse slotted screws: round head (61480), flat head (61460)','10-32 fine slotted screws: round head (61440), flat head (61420)']
M=[(1,21),(2,22),(3,23),(4,24),(5,25)]
dr=[dict(title=f'Machine {a} and Machine {b}',sub=SUB[i],items=T[i],img='tray' if i==0 else f'tray{i+1}',ys=G[i][0],rows=G[i][1]) for i,(a,b) in enumerate(M)]
data=dict(drawers=dr)
'''
s=s[:a]+new+s[b:]
s=s.replace("img['tray']=b('img/tray.jpg')","img['tray']=b('img/tray.jpg')\nfor n in range(2,6): img[f'tray{n}']=b(f'img/tray{n}.jpg')")
open('build.py','w').write(s)
t=open('template.html').read()
for o,n in [("t.style.backgroundImage='url('+IMG.tray+')';D.rows.forEach","t.style.backgroundImage='url('+IMG[d.img]+')';d.rows.forEach"),
 ("top=D.ys[r]/800,h=(D.ys[r+1]-D.ys[r])/800","top=d.ys[r]/800,h=(d.ys[r+1]-d.ys[r])/800"),
 ("pick(it,n,l,top,w,h)}","pick(it,n,l,top,w,h,d.img)}") if 0 else ("n.onclick=()=>pick(it,n,l,top,w,h)","n.onclick=()=>pick(it,n,l,top,w,h,d.img)"),
 ("function pick(it,n,l,top,w,h){","function pick(it,n,l,top,w,h,im){"),
 ("background-image:url(${IMG.tray})","background-image:url(${IMG[im]})"),
 ("marks the drawer with its inside photographed. The other four in column 1 use real fronts and open empty. Scroll sideways for the remaining 29 columns.","marks a drawer with its inside photographed. All five in column 1 are done. Scroll sideways for the other 29 columns."),
 ("Prototype: 5 drawers high, 30 wide.","5 drawers high, 30 wide.")]:
    assert o in t,o; t=t.replace(o,n)
open('template.html','w').write(t)

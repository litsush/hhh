s=open('build.py').read()
new='''for x,(ys,rows) in zip(dr,G):
    x['cells']=[[r*8+c,row[c],ys[r],row[c+1],ys[r+1]] for r,row in enumerate(rows) for c in range(8)]; x['h']=800; del x['ys'],x['rows']
def stove(mach,base,head,th,ls,cents,cd):
    out=[]
    for i,(l,c,k) in enumerate(zip(ls,cents,cd)):
        sku=base+1+i;u=f'738287{sku}';assert chk(u)==int(k),(u,k,chk(u))
        L='ABCDEFGH'[i]; out.append(dict(name=f'{th} x {l} {head} head stove bolt',short=l,price=fm(c),sku=f'{sku}-{L}',upc=f'7 38287 {sku} {k}',where=f'Machine {mach}, slot {L}'))
    return out
def long_(mach,base,head,cents,cd):
    S=[('10-24','4'),('10-24','5'),('10-24','6'),('1/4-20','4'),('1/4-20','5'),('1/4-20','6')]; out=[]
    for i,((th,l),c,k) in enumerate(zip(S,cents,cd)):
        sku=base+1+i;u=f'738287{sku}';assert chk(u)==int(k),(u,k,chk(u));L='ABCDEF'[i]
        out.append(dict(name=f'{th} x {l} {head} head stove bolt',short=f'{th.split("-")[0]} x {l}',price=fm(c),sku=f'{sku}-{L}',upc=f'7 38287 {sku} {k}',where=f'Machine {mach}, slot {L}'))
    return out
A=['1/2','3/4','1','1-1/4','1-1/2','2','2-1/2','3'];B=['3/4','1','1-1/4','1-1/2','2','2-1/2','3']
I6=stove(11,60740,'round','1/4-20',A,[40,45,48,51,58,64,69,79],'30741852')+stove(17,60720,'flat','1/4-20',A,[41,45,48,52,58,65,75,79],'52963074')
I7=stove(12,60340,'round','5/16-18',B,[75,89,95,95,109,109,119],'5296307')+stove(18,60320,'flat','5/16-18',B,[75,89,89,95,109,109,119],'7418529')
I8=stove(13,60160,'round','3/8-16',B,[95,99,109,109,119,129,135],'9630741')+stove(19,60140,'flat','3/8-16',B,[95,105,115,115,125,129,135],'1852963')
I9=long_(14,60120,'round',[75,85,95,109,109,119],'307418')+long_(20,60100,'flat',[75,89,95,99,109,129],'529630')
I10=[]
sz=['3/4','1','1-1/2','2','3/4','1','2']
for r,(rw,head,zc,br,nm,nc,cd,off) in enumerate([('back','round',[46,52,60,66],[85,115,149],'zinc',28,'18529630',1),('front','flat',[46,52,60,66],[95,115,165],'brass',47,'07418529',11)]):
    pr=zc+br+[nc]
    for c in range(8):
        sku=61200+off+c;u=f'738287{sku}';assert chk(u)==int(cd[c]),(u,cd[c],chk(u));nut=c==7;mat='zinc' if c<4 else 'brass'
        I10.append(dict(name=f'12-24 {nm} hex nuts' if nut else f'12-24 x {sz[c]} {mat} {head} head',short='Nuts' if nut else sz[c],price=fm(pr[c]),sku=f'{sku}-{LET[r*8+c]}',upc=f'7 38287 {sku} {cd[c]}',where=f'Machine 34, {rw} row, column {c+1}'))
I10[8]['note']='On the label, but this drawer has no compartment for it.'
def rc(rows):
    out=[]
    return out
C6=[[0,0,0,205,205],[1,205,0,403,205],[2,403,0,700,205],[3,700,0,950,205],[4,950,0,1200,205],[8,0,205,212,425],[9,212,215,412,425],[6,412,215,805,415],[7,805,205,1200,415],[5,0,425,412,630],[10,412,415,703,620],[11,703,415,950,620],[12,950,410,1200,620],[13,0,630,415,800],[14,415,620,805,800],[15,805,615,1200,800]]
def seq(bands):
    i=0;out=[]
    for y0,y1,xs in bands:
        for a,b in zip(xs,xs[1:]): out.append([i,a,y0,b,y1]);i+=1
    return out
C7=seq([(0,205,[0,305,605,900,1200]),(205,410,[0,405,800,1200]),(410,605,[0,305,603,895,1200]),(605,800,[0,397,797,1200])])
C8=seq([(0,190,[0,320,610,900,1200]),(190,395,[0,425,810,1200]),(395,595,[0,325,630,925,1200]),(595,800,[0,430,840,1200])])
ry=[0,100,195,290,392,492,595,695,800]
C9=[[0,0,0,225,395],[3,225,0,460,395],[1,460,ry[0],1200,ry[1]],[2,460,ry[1],1200,ry[2]],[4,460,ry[2],1200,ry[3]],[5,460,ry[3],1200,ry[4]],[6,0,400,225,800],[9,225,400,460,800],[7,460,ry[4],1200,ry[5]],[8,460,ry[5],1200,ry[6]],[10,460,ry[6],1200,ry[7]],[11,460,ry[7],1200,ry[8]]]
top=[5,160,305,455,603,748,893,1042,1200];bot=[135,297,450,608,752,905,1058,1200]
C10=[[i,top[i],0,top[i+1],265] for i in range(8)]+[[8,0,270,135,520]]+[[9+i,bot[i],270,bot[i+1],520] for i in range(7)]
NEW=[('Machines 11 and 17','1/4-20 slotted stove bolts: round head (60740), flat head (60720)',I6,C6,800),('Machines 12 and 18','5/16-18 slotted stove bolts: round head (60340), flat head (60320)',I7,C7,800),('Machines 13 and 19','3/8-16 slotted stove bolts: round head (60160), flat head (60140)',I8,C8,800),('Machines 14 and 20','Longer slotted stove bolts, 10-24 and 1/4-20: round head (60120), flat head (60100)',I9,C9,800),('Machine 34','12-24 coarse slotted machine screws, flat and round head (61200)',I10,C10,520)]
for n,(t,sb,it,ce,h) in enumerate(NEW):
    assert sorted(c[0] for c in ce)==list(range(len(it))),t
    dr.append(dict(title=t,sub=sb,items=it,img=f'tray{n+6}',cells=ce,h=h))
data=dict(drawers=dr)
'''
assert 'data=dict(drawers=dr)\n' in s
s=s.replace('data=dict(drawers=dr)\n',new,1)
s=s.replace("img={f'd{i}':b(f'img/d{i}.jpg') for i in range(1,6)}","img={f'd{i}':b(f'img/d{i}.jpg') for i in range(1,11)}").replace("for n in range(2,6): img","for n in range(2,11): img")
s=s.replace("print(len(h),[len(x) for x in T])","print(len(h),[len(x['items']) for x in dr])")
open('build.py','w').write(s)
t=open('template.html').read()
a=t.index("d.rows.forEach");b=t.index("$('detail').innerHTML='<p class=\"hint\">Tap a compartment")
t=t[:a]+"""d.cells.forEach(([i,x0,y0,x1,y1])=>{const it=d.items[i],l=x0/1200,w=(x1-x0)/1200,top=y0/d.h,h=(y1-y0)/d.h,n=document.createElement('button');n.className='cell';n.style.cssText=`left:${l*100}%;top:${top*100}%;width:${w*100}%;height:${h*100}%`;
   n.setAttribute('aria-label',it.name+', '+it.price);n.innerHTML='<span>'+it.short+'</span>';n.onclick=()=>pick(it,n,l,top,w,h,d);t.appendChild(n)});
  """+t[b:]
R=[("t.style.backgroundImage='url('+IMG[d.img]+')';","t.style.backgroundImage='url('+IMG[d.img]+')';t.style.aspectRatio='1200/'+d.h;"),
("t.className='tray';t.style.backgroundImage='';","t.className='tray';t.style.backgroundImage='';t.style.aspectRatio='';"),
("Tap a compartment. Rows run back to front: round zinc, round brass, flat zinc, flat brass.","Tap a compartment."),
("function pick(it,n,l,top,w,h,im){","function pick(it,n,l,top,w,h,d){const im=d.img;"),
("aspect-ratio:${w*1200}/${h*800}","aspect-ratio:${w*1200}/${h*d.h}"),
("<dt>UPC</dt><dd>${it.upc}</dd></dl>","<dt>UPC</dt><dd>${it.upc}</dd></dl>${it.note?'<p class=\"nt\">'+it.note+'</p>':''}"),
("for(let c=2;c<=30;c++)","for(let c=3;c<=30;c++)"),
("All five in column 1 are done. Scroll sideways for the other 29 columns.","Columns 1 and 2 are done. Scroll sideways for the other 28."),
(".hint{",".nt{margin:6px 0 0;font-size:13px;color:#a3341f}.hint{")]
for o,n in R:
    assert o in t,o;t=t.replace(o,n)
open('template.html','w').write(t)

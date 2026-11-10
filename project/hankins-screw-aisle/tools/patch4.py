s=open('build.py').read()
new='''def grid(m,base,rows):
    o=[]
    for i,(nm,sh,c,k) in enumerate(rows):
        o.append(it(m,base+((1+i) if i<8 else (11+i-8)),LET[i],nm,sh,c,k))
    return o
def thr(m,base,th,suffix,ls,cents,cd,start):
    return [(f'{th} x {l} {suffix}',l,c,k) for l,c,k in zip(ls,cents,cd)]
R62=[('8-32',x) for x in ['1/2','3/4','1','1-1/4','1-1/2','1-3/4','2']]+[('10-24',x) for x in ['1/2','3/4','1']]+[('1/4-20',x) for x in ['1/2','3/4','1','1-1/2']]
I16=grid(62,63240,[(f'{t} x {l} zinc combo truss head',two(t,l),c,k) for (t,l),c,k in zip(R62,[22,23,27,30,34,39,41,23,27,31,32,39,45,54],'52963074418529')])
L63=['3/8','1/2','5/8','3/4','1','1-1/4','1-1/2','2']
SH='zinc slot indented hex head'
I17=grid(63,65540,thr(0,0,'6-32',SH,L63,[32,33,34,36,41,43,51,56],'41852963',0)+thr(0,0,'8-32',SH,L63,[33,34,36,40,43,53,56,62],'30741852',0))
I17+=grid(64,65560,thr(0,0,'10-24','coarse '+SH,L63,[40,42,43,44,49,55,69,85],'29630741',0)+thr(0,0,'10-32','fine '+SH,L63,[41,43,44,47,52,58,69,85],'18529630',0))
R65=[('6-32','1/2','oval'),('6-32','1/2','round'),('6-32','3/4','round'),('8-32','1/2','round'),('8-32','3/4','round'),('8-32','1','round'),('8-32','1-1/2','round'),('10-24','3/4','round'),('10-24','1','round'),('10-24','1-1/2','round'),('1/4-20','1','round'),('1/4-20','1-1/2','round')]
I18=grid(65,70940,[(f'{t} x {l} one-way security {h} head',two(t,l),c,k) for (t,l,h),c,k in zip(R65,[56,37,43,45,48,57,66,55,66,75,79,95],'418529633074')])
L68=['3/8','1/2','3/4','1','1-1/4','1-1/2','2','2-1/2']
BK='black phillips pan head'
I19=grid(68,33140,thr(0,0,'6-32',BK,L68,[24,26,28,28,30,32,33,37],'74185296',0)+thr(0,0,'8-32',BK,L68,[29,30,31,33,34,35,43,46],'63074185',0))
I19+=grid(69,33160,thr(0,0,'10-24','coarse '+BK,L68,[32,34,35,36,37,38,47,54],'52963074',0)+thr(0,0,'10-32','fine '+BK,L68,[32,34,35,36,37,38,47,54],'41852963',0))
L70=['1/2','3/4','1','1-1/4','1-1/2','2','2-1/2','3']
I20=grid(70,33180,[(f'1/4-20 x {l} {BK}',l,c,k) for l,c,k in zip(L70,[38,41,45,46,49,50,62,65],'30741852')])
C16=seq([(0,240,[0,158,303,447,590,795,975,1165]),(240,510,[5,160,318,478,625,805,990,1200])])
C17=seq([(0,190,[35,190,338,482,625,768,905,1050,1195]),(190,390,[30,190,345,495,632,778,925,1068,1200]),(390,595,[30,192,348,500,642,790,935,1092,1200]),(595,800,[30,200,350,505,655,808,960,1108,1200])])
C18=seq([(0,245,[0,200,395,598,780,975,1170]),(245,540,[0,215,420,612,805,1000,1200])])
C19=seq([(0,205,[5,168,318,465,608,755,900,1040,1185]),(205,410,[15,172,325,472,612,762,905,1045,1190]),(410,605,[15,175,330,480,622,770,912,1058,1200]),(605,800,[20,182,335,488,635,780,922,1065,1200])])
C20=seq([(0,255,[0,205,405,660,910,1170]),(255,520,[0,410,810,1200])])
NEW4=[('Machine 62','Combination truss head machine screws, 8-32 to 1/4-20 (63240)',I16,C16,520),('Machines 63 and 64','Slot indented hex head machine screws: 6-32 and 8-32 (65540), 10-24 and 10-32 (65560)',I17,C17,800),('Machine 65','One-way security machine screws, oval and round head, 6-32 to 1/4-20 (70940)',I18,C18,540),('Machines 68 and 69','Black oxide phillips pan head: 6-32 and 8-32 (33140), 10-24 and 10-32 (33160)',I19,C19,800),('Machine 70','Black oxide phillips pan head machine screws, 1/4-20 (33180)',I20,C20,520)]
for n,(t,sb,i_,ce,h) in enumerate(NEW4):
    assert sorted(c[0] for c in ce)==list(range(len(i_))),(t,len(ce),len(i_))
    dr.append(dict(title=t,sub=sb,items=i_,img=f'tray{n+16}',cells=ce,h=h))
data=dict(drawers=dr)
'''
k='data=dict(drawers=dr)\n';assert s.count(k)==1
s=s.replace(k,new).replace("for i in range(1,16)}","for i in range(1,21)}").replace("for n in range(2,16): img","for n in range(2,21): img")
open('build.py','w').write(s)
t=open('template.html').read()
for o,n in [("for(let c=4;c<=30;c++)","for(let c=5;c<=30;c++)"),("Columns 1 to 3 are done. Scroll sideways for the other 27.","Columns 1 to 4 are done. Scroll sideways for the other 26.")]:
    assert o in t;t=t.replace(o,n)
open('template.html','w').write(t)

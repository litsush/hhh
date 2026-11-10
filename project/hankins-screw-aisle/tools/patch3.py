s=open('build.py').read()
new='''
def it(m,sku,L,nm,sh,c,k):
    u=f'738287{sku}';assert chk(u)==int(k),(u,k,chk(u))
    return dict(name=nm,short=sh,price=fm(c),sku=f'{sku}-{L}',upc=f'7 38287 {sku} {k}',where=f'Machine {m}, slot {L}')
def two(th,l): return f'{th}<br>x {l}'
def N(th): return f'{th}<br>Nuts'
# Machine 8
S8=[('6-32',None),('8-32',None),('10-24',None),('1/4-20',None),('6-32','3/8'),('6-32','1/2'),('6-32','1'),('8-32','3/8'),('8-32','1/2'),('8-32','3/4'),('8-32','1'),('10-24','1/2'),('10-24','3/4'),('10-24','1'),('1/4-20','3/4'),('1/4-20','1')]
P8=[33,38,46,62,42,43,46,42,43,46,56,52,64,79,105,119]
I11=[]
for i,((th,l),c,k) in enumerate(zip(S8,P8,'4185296330741852'[:0] or '4185296337418 '[:0] or '4185296341852963'[:0] or '41852963'+'30741852')):
    off=(1+i) if i<8 else (11+i-8)
    I11.append(it(8,61580+off,LET[i],f'{th} brass hex nuts' if l is None else f'{th} x {l} brass oval head',N(th) if l is None else two(th,l),c,k))
# Machine 40
R40=[('1/2',99,'3'),('3/4',109,'0'),('1',129,'7'),('1-1/2',149,'4'),('2',179,'1'),('2-1/2',219,'8'),('3',269,'5')]
for i,(l,c,k) in enumerate(R40): I11.append(it(40,61041+i,'ABCDEFG'[i],f'1/4-20 x {l} brass round head',l,c,k))
I11.append(it(40,61048,'H','1/4-20 brass hex nuts','Nuts',64,'2'))
F40=[('3/4',115,'2'),('1',129,'9'),('1-1/2',155,'6'),('2',195,'3'),('2-1/2',239,'0'),('3',279,'7')]
for i,(l,c,k) in enumerate(F40): I11.append(it(40,61051+i,'JKLMNP'[i],f'1/4-20 x {l} brass flat head',l,c,k))
C11=[[i,a,0,b,200] for i,(a,b) in enumerate(zip([0,165,312,460,603,750,897,1037],[165,312,460,603,750,897,1037,1190]))]
C11+=[[8+i,a,200,b,405] for i,(a,b) in enumerate(zip([0,160,310,458,605,752,897,1037],[160,310,458,605,752,897,1037,1190]))]
xr=[0,152,302,447,600,742];xf=[0,150,300,443,597,742]
C11+=[[16+i,xr[i],405,xr[i+1],603] for i in range(5)]+[[21,742,405,895,695],[22,895,400,1037,695],[23,1037,390,1190,695]]
C11+=[[24+i,xf[i],603,xf[i+1],800] for i in range(5)]+[[29,742,695,1190,800]]
# Machine 7
S7=[('6-32','3/4','Round',49,'9'),('8-32','1/2','Round',51,'6'),('8-32','3/4','Round',55,'3'),('10-24','1/2','Round',60,'0'),('10-24','3/4','Round',75,'7'),('10-24','1','Round',79,'4'),('1/4-20','3/4','Round',79,'1'),('1/4-20','1','Round',85,'8'),('1/4-20','1-1/2','Round',105,'8'),('6-32','1/2','Oval',46,'5'),('8-32','3/4','Oval',63,'2'),('10-24','1','Oval',69,'9'),('6-32',None,'',44,'6'),('8-32',None,'',49,'3'),('10-24',None,'',55,'0'),('1/4-20',None,'',66,'7')]
I12=[]
for i,(th,l,h,c,k) in enumerate(S7):
    off=(1+i) if i<8 else (11+i-8)
    I12.append(it(7,61600+off,LET[i],f'{th} aluminum hex nuts' if l is None else f'{th} x {l} aluminum {h.lower()} head',N(th) if l is None else two(th,l),c,k))
x1=[0,145,300,447,597,740,887,1030,1180];x2=[0,130,290,440,600,750,905,1055,1200]
C12=[[i,x1[i],0,x1[i+1],250] for i in range(8)]+[[8+i,x2[i],250,x2[i+1],540] for i in range(8)]
PL=['3/4','1','1-1/4','1-1/2','2','2-1/2','3']
def phil(m,base,th,head,cents,cd):
    o=[it(m,base+1+i,'ABCDEFG'[i],f'{th} x {PL[i]} zinc phillips {head} head',PL[i],cents[i],cd[i]) for i in range(7)]
    o.append(it(m,base+8,'H',f'{th} zinc hex nuts','Nuts',cents[7],cd[7]));return o
I13=phil(49,77540,'5/16-18','pan',[46,53,56,67,79,109,119,30],'96307418')+phil(58,77360,'5/16-18','flat',[41,49,53,63,75,95,109,29],'30741852')
I14=phil(50,77560,'3/8-16','pan',[85,105,119,135,159,175,195,44],'74185296')+phil(59,77380,'3/8-16','flat',[58,75,85,95,109,129,139,35],'18529630')
C13=seq([(0,110,[0,312,610,905,1195]),(110,370,[0,318,612,908,1200]),(370,503,[5,328,628,935,1200]),(503,800,[0,332,645,950,1200])])
C14=seq([(0,115,[10,320,615,908,1195]),(115,375,[5,335,625,915,1200]),(375,505,[10,328,628,930,1200]),(505,800,[0,318,640,945,1200])])
S60=[('10-24','4',59,'6'),('10-24','5',79,'3'),('10-24','6',119,'0'),('1/4-20','4',75,'7'),('1/4-20','5',105,'4'),('1/4-20','6',129,'1')]
I15=[it(60,77401+i,'ABCDEF'[i],f'{th} x {l} zinc phillips flat head',f'{th.split("-")[0]} x {l}',c,k) for i,(th,l,c,k) in enumerate(S60)]
I15[0]['note']=I15[3]['note']='Covered by a card marked EMPTY in this drawer.'
y=[0,130,265,400,560]
C15=[[0,0,0,235,560],[3,235,0,455,560],[1,455,y[0],1200,y[1]],[2,455,y[1],1200,y[2]],[4,455,y[2],1200,y[3]],[5,455,y[3],1200,y[4]]]
NEW3=[('Machines 8 and 40','Solid brass slotted: oval head 6-32 to 1/4-20 (61580), flat and round 1/4-20 (61040)',I11,C11,800),('Machine 7','Aluminum slotted machine screws, round and oval head, 6-32 to 1/4-20 (61600)',I12,C12,540),('Machines 49 and 58','5/16-18 phillips machine screws: pan head (77540), flat head (77360)',I13,C13,800),('Machines 50 and 59','3/8-16 phillips machine screws: pan head (77560), flat head (77380)',I14,C14,800),('Machine 60','Longer phillips flat head machine screws, 10-24 and 1/4-20 (77400)',I15,C15,560)]
for n,(t,sb,i_,ce,h) in enumerate(NEW3):
    assert sorted(c[0] for c in ce)==list(range(len(i_))),t
    dr.append(dict(title=t,sub=sb,items=i_,img=f'tray{n+11}',cells=ce,h=h))
data=dict(drawers=dr)
open('data.json','w').write(json.dumps(data,ensure_ascii=False,indent=1))
'''
k='data=dict(drawers=dr)\n'
assert s.count(k)==1
s=s.replace(k,new.lstrip('\n'))
s=s.replace("for i in range(1,11)}","for i in range(1,16)}").replace("for n in range(2,11): img","for n in range(2,16): img")
open('build.py','w').write(s)
t=open('template.html').read()
for o,n in [("for(let c=3;c<=30;c++)","for(let c=4;c<=30;c++)"),("Columns 1 and 2 are done. Scroll sideways for the other 28.","Columns 1 to 3 are done. Scroll sideways for the other 27.")]:
    assert o in t;t=t.replace(o,n)
open('template.html','w').write(t)

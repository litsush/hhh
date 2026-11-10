s=open('build.py').read()
new='''def ex(wh,rows):
    o=[]
    for sku,L,nm,sh,c,k in rows:
        x=it(0,sku,L,nm,sh,c,k);x['where']=f'{wh}, slot {L}';o.append(x)
    return o
GS='slotted fillister head gun screw'
I21=ex('Machine 72',[(32921,'A','8-40 x 1/4 '+GS,two('8-40','1/4'),175,'6'),(32922,'B','8-40 x 3/8 '+GS,two('8-40','3/8'),175,'3'),(32923,'C','8-40 x 1/2 '+GS,two('8-40','1/2'),175,'0'),(32924,'D','8-40 x 3/4 '+GS,two('8-40','3/4'),175,'7'),(32925,'E','8-40 x 1 '+GS,two('8-40','1'),185,'4'),(32926,'F','8-36 x 1 '+GS,two('8-36','1'),185,'1'),(32927,'G','10-32 x 1 '+GS,two('10-32','1'),179,'8'),(32928,'H','10-24 x 1 '+GS,two('10-24','1'),179,'5'),(32929,'J','12-28 x 1 '+GS,two('12-28','1'),179,'2'),(32931,'K','12-24 x 1 '+GS,two('12-24','1'),179,'5'),(32932,'L','Plastic tweezers','Tweezers',149,'2')])
C21=[[i,x,0,y,258] for i,(x,y) in enumerate([(0,207),(207,412),(412,612),(612,815),(815,1030)])]+[[5+i,x,258,y,540] for i,(x,y) in enumerate([(0,218),(218,430),(430,635),(635,840),(840,1040)])]+[[10,1040,0,1200,540]]
WO='slotted Weaver oval head gun screw';PS='plug screw'
I22=ex('Machine 73',[(32941,'A','6-48 x 5/32 '+WO,two('6-48','5/32'),169,'4'),(32942,'B','6-48 x 3/16 '+WO,two('6-48','3/16'),175,'1'),(32943,'C','6-48 x 1/4 '+WO,two('6-48','1/4'),179,'8'),(32944,'D','6-48 x 1/2 '+WO,two('6-48','1/2'),179,'5'),(32945,'E','8-40 x 1/4 '+WO,two('8-40','1/4'),189,'2'),(32946,'F','8-40 x 1/2 '+WO,two('8-40','1/2'),195,'9'),(32947,'G','#10 x 1-1/4 oval butt plate screw','Butt plate',145,'6'),(32948,'H','6-48 x 1/8 '+PS,two('6-48','1/8'),139,'3'),(32949,'J','6-40 x 1/8 '+PS,two('6-40','1/8'),139,'0'),(32951,'K','8-40 x 1/8 '+PS,two('8-40','1/8'),145,'3'),(32952,'L','10-32 x 1/8 '+PS,two('10-32','1/8'),145,'0'),(32953,'M','Metal tweezers','Metal',329,'7'),(32954,'N','Plastic tweezers','Plastic',149,'4')])
C22=[[i,x,0,y,260] for i,(x,y) in enumerate([(0,150),(150,305),(305,465),(465,612),(612,765),(765,925)])]+[[6+i,x,260,y,540] for i,(x,y) in enumerate([(0,310),(310,472),(472,628),(628,778),(778,950)])]+[[11,950,0,1095,540],[12,1095,0,1200,540]]
F74=[(32961,'A','6-48','3/8','T-10','fillister',165),(32962,'B','6-48','9/16','T-10','fillister',169),(32963,'C','6-40','3/8','T-10','fillister',179),(32964,'D','6-40','1/2','T-10','fillister',185),(32965,'E','8-40','1/4','T-10','fillister',189),(32966,'F','8-40','1/4','T-15','fillister',189),(32967,'G','8-40','3/8','T-15','fillister',189),(32968,'H','8-40','1/2','T-10','fillister',199),(32969,'J','8-40','1/2','T-15','fillister',199),(32971,'K','6-48','1/4','T-10','fillister',209),(32972,'L','6-48','1/4','T-10','Weaver',199),(32973,'M','6-48','3/8','T-10','Weaver',199),(32974,'N','6-40','1/4','T-10','Weaver',199),(32975,'P','6-40','3/8','T-10','Weaver',209),(32976,'Q','8-40','1/4','T-15','Weaver',209),(32977,'R','8-40','3/8','T-15','Weaver',209),(32978,'S','8-40','1/2','T-10','Weaver',209),(32979,'T','8-40','1/2','T-15','Weaver',209)]
cd=lambda n:str(chk(f'738287{n}'))
I23=ex('Machine 74',[(n,L,f'{t} x {l} {d} star drive {h} head gun screw',f'{t} x {l}<br>{d}',c,cd(n)) for n,L,t,l,d,h,c in F74]+[(32958,'U','T-10 short arm wrench','T-10 wrench',165,cd(32958)),(32959,'V','T-15 short arm wrench','T-15 wrench',179,cd(32959))])
for x in I23: x['upc_calculated']=True
C23=seq([(0,140,[0,208,415,615,810,1005,1200]),(140,285,[0,212,420,625,822,1025,1200]),(285,435,[0,210,428,632,835,1040,1200]),(435,600,[0,640,1200])])
def nt(t,k_): return f'{t}<br>{k_}'
I24=ex('Nuts 3',[(60901,'A','1/4-28 castle nut',nt('1/4-28','Castle'),145,'1'),(60902,'B','5/16-24 castle nut',nt('5/16-24','Castle'),155,'8'),(60903,'C','3/8-24 castle nut',nt('3/8-24','Castle'),165,'5'),(60904,'D','7/16-20 castle nut',nt('7/16-20','Castle'),185,'2'),(60905,'E','1/2-20 castle nut',nt('1/2-20','Castle'),219,'9'),(60906,'F','1/4-28 hex nut',nt('1/4-28','Hex'),32,'6'),(60907,'G','5/16-24 hex nut',nt('5/16-24','Hex'),37,'3'),(60908,'H','3/8-24 hex nut',nt('3/8-24','Hex'),51,'0'),(60911,'J','7/16-20 hex nut',nt('7/16-20','Hex'),64,'0'),(60912,'K','1/2-20 hex nut',nt('1/2-20','Hex'),75,'7'),(60913,'L','9/16-18 hex nut',nt('9/16-18','Hex'),85,'4'),(60914,'M','5/8-18 hex nut',nt('5/8-18','Hex'),109,'1'),(60915,'N','3/4-16 hex nut',nt('3/4-16','Hex'),145,'8')])
C24=seq([(0,240,[0,152,318,478,610,895,1040,1185]),(240,540,[0,203,365,785,925,1075,1200])])
R4=[(68541,'A','9/16-18','Castle fine',359,'1'),(68542,'B','5/8-18','Castle fine',399,'8'),(68543,'C','3/4-16','Castle fine',539,'5'),(68544,'D','7/8-14','Castle fine',759,'2'),(68545,'E','1/4-20','Slotted coarse',99,'9'),(68546,'F','5/16-18','Slotted coarse',115,'6'),(68547,'G','3/8-16','Slotted coarse',115,'3'),(68548,'H','7/16-14','Slotted coarse',125,'0'),(68551,'J','1/2-13','Slotted coarse',135,'0'),(68552,'K','9/16-12','Slotted coarse',209,'7'),(68553,'L','5/8-11','Slotted coarse',219,'4'),(68554,'M','3/4-10','Slotted coarse',279,'1'),(68555,'N','7/8-9','Slotted coarse',429,'8'),(68556,'P','1-8','Slotted coarse',579,'5')]
I25=ex('Nuts 4',[(n,L,f'{t} {k_.split()[0].lower()} nut, {k_.split()[1]} thread',nt(t,k_.split()[0]),c,k) for n,L,t,k_,c,k in R4])
I25[11]['note']=I25[12]['note']='The divider between 3/4-10 and 7/8-9 looks flattened or missing, so this slot is approximate.'
C25=seq([(0,250,[0,165,365,580,760,905,1055,1190]),(250,520,[0,165,320,475,622,790,960,1200])])
NEW5=[('Machine 72','Slotted fillister head gun screws, 8-32 to 12-24, with tweezers (32920)',I21,C21,540),('Machine 73','Slotted Weaver oval head gun screws and plug screws, with tweezers (32940)',I22,C22,540),('Machine 74','Star drive fillister and Weaver oval head gun screws, with wrenches (32960)',I23,C23,600),('Nuts 3','Castle and hex nuts, fine thread, 1/4-28 to 3/4-16 (60900)',I24,C24,540),('Nuts 4','Castle and slotted hex nuts, coarse and fine, 1/4-20 to 1-8 (68540)',I25,C25,520)]
for n,(t,sb,i_,ce,h) in enumerate(NEW5):
    assert sorted(c[0] for c in ce)==list(range(len(i_))),(t,len(ce),len(i_))
    dr.append(dict(title=t,sub=sb,items=i_,img=f'tray{n+21}',cells=ce,h=h))
data=dict(drawers=dr)
'''
k='data=dict(drawers=dr)\n';assert s.count(k)==1
s=s.replace(k,new).replace("for i in range(1,21)}","for i in range(1,26)}").replace("for n in range(2,21): img","for n in range(2,26): img")
open('build.py','w').write(s)
t=open('template.html').read()
for o,n in [("for(let c=5;c<=30;c++)","for(let c=6;c<=30;c++)"),("Columns 1 to 4 are done. Scroll sideways for the other 26.","Columns 1 to 5 are done. Scroll sideways for the other 25.")]:
    assert o in t;t=t.replace(o,n)
open('template.html','w').write(t)

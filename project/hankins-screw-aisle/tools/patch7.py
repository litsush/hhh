s=open('build.py').read()
new='''for i_,x in enumerate(dr): x['front']=f'd{i_+1}'
I31=nuts('Nuts 16','nylon insert locking wing nut',[(71781,'A','8-32','coarse',199,'5'),(71782,'B','10-24','coarse',239,'2'),(71783,'C','10-32','fine',239,'9'),(71784,'D','1/4-20','coarse',259,'6'),(71785,'E','5/16-18','coarse',319,'3'),(71786,'F','3/8-16','coarse',389,'0')])
I32=nuts('Nuts 17','coupling nut',[(64501,'A','10-24','coarse',95,'9'),(64502,'B','1/4-20','coarse',109,'6'),(64503,'C','5/16-18','coarse',159,'3'),(64504,'D','3/8-16','coarse',199,'0')])
I32+=ex('Nuts 17',[(64505,'E','3/8-16 to 1/4-20 reducing coupling nut','3/8 to 1/4',209,'7'),(64506,'F','3/8-16 to 1/2-13 reducing coupling nut','3/8 to 1/2',239,'4')])
I32+=nuts('Nuts 17','coupling nut',[(64507,'G','1/2-13','coarse',259,'1'),(64508,'H','5/8-11','coarse',389,'8'),(64511,'J','3/4-10','coarse',619,'8')])
T19=[(60881,'A','6-32 x 1/4','pronged','5/32',58,'6'),(60882,'B','8-32 x 1/4','pronged','7/32',64,'3'),(60883,'C','10-24 x 9/32','pronged','15/64',68,'0'),(60884,'D','10-24 x 7/16','pronged','15/64',69,'7'),(60885,'E','1/4-20 x 5/16','pronged','5/16',75,'4'),(60886,'F','1/4-20 x 7/16','pronged','5/16',75,'1'),(60887,'G','1/4-20 x 9/16','pronged','5/16',79,'8'),(60888,'H','5/16-18 x 3/8','pronged','25/64',79,'5'),(60891,'J','6-32 x 1/4','brad hole','5/32',85,'5'),(60892,'K','8-32 x 1/4','brad hole','7/32',95,'2'),(60893,'L','10-24 x 5/16','brad hole','15/64',99,'9'),(60894,'M','10-32 x 5/16','brad hole','15/64',115,'6'),(60895,'N','1/4-20 x 5/16','brad hole','5/16',115,'3'),(60896,'P','5/16-18 x 5/8','brad hole','25/64',125,'0'),(60897,'Q','3/8-16 x 7/16','brad hole','15/32',135,'7'),(60898,'R','1/4-20 x 1/4','brad hole rectangle base','5/16',135,'4')]
I33=ex('Nuts 19',[(n,L,f'{z} {k_} T-nut, for {h} hole',z.replace(' x ','<br>x '),c,kk) for n,L,z,k_,h,c,kk in T19])
I33[3]['note']='This compartment was empty in the photo.'
W=[('A','8-32 x 1/4','',52,'31361','6'),('B','10-24 x 5/16','',52,'31362','3'),('C','1/4-20 x 5/16','',58,'31363','0'),('D','1/4-20 x 7/16','',63,'31364','7'),('E','1/4-20 x 9/16','',69,'31365','4'),('F','5/16-18 x 3/8','',89,'31366','1'),('G','5/16-18 x 5/8','',99,'31367','8'),('H','3/8-16 x 7/16','',125,'31368','5'),('J','1/2-13 x 3/8','',269,'31371','5'),('K','1/4-20 x 7/16',' projection',99,'31372','2'),('L','5/16-18 x 3/8',' projection',125,'31373','9'),('M','3/8-16 x 7/16',' projection',145,'31374','6')]
I34=[]
for L,z,p,c,n,k_ in W:
    u='719199'+n;assert chk(u)==int(k_),(u,k_,chk(u))
    I34.append(dict(name=f'{z} round{p} weld nut',short=z.replace(' x ','<br>x '),price=fm(c),sku=f'9{n}-{L}',upc=f'7 19199 {n} {k_}',where=f'Nuts 19.5, slot {L}'))
SP=[(61621,'A','4-40','flat, machine screw',47,'7'),(61622,'B','6-32','flat, machine screw',51,'4'),(61623,'C','8-32','flat, machine screw',53,'1'),(61624,'D','10-24','flat, machine screw',60,'8'),(61625,'E','1/4-20','flat, machine screw',62,'5'),(61626,'F','8-32','U type, machine screw',79,'2'),(61627,'G','10-24','U type, machine screw',89,'9'),(61628,'H','1/4-20','U type, machine screw',89,'6'),(61631,'J','8-32','J type, machine screw',79,'6'),(61632,'K','10-24','J type, machine screw',99,'3'),(61633,'L','10-24','angle type, machine screw',139,'0'),(61634,'M','No. 4','flat, sheet metal screw',46,'7'),(61635,'N','No. 6','flat, sheet metal screw',48,'4'),(61636,'P','No. 8','flat, sheet metal screw',59,'1'),(61637,'Q','No. 10','flat, sheet metal screw',64,'8'),(61638,'R','No. 14','flat, sheet metal screw',89,'5')]
I35=ex('Nuts 20',[(n,L,f'{z} speed nut, {k_}',f'{z}<br>{k_.split(",")[0].split()[0]}',c,kk) for n,L,z,k_,c,kk in SP])
P21=[(61137,'A','3/8 washer push nut, black','3/8 black',125,'3'),(61138,'B','1/2 washer push nut, black','1/2 black',169,'0'),(61139,'C','5/8 washer push nut, black','5/8 black',289,'7'),(61145,'E','3/16 washer cap push nut','3/16 cap',63,'8'),(61146,'F','1/4 washer cap push nut','1/4 cap',66,'5'),(61147,'G','5/16 washer cap push nut','5/16 cap',67,'2'),(61148,'H','3/8 washer cap push nut','3/8 cap',69,'9'),(61151,'J','7/16 washer cap push nut','7/16 cap',89,'9'),(61152,'K','1/2 washer cap push nut','1/2 cap',105,'6'),(65975,'','5/8 washer cap push nut','5/8 cap',169,'7'),(65976,'','3/4 washer cap push nut','3/4 cap',259,'4'),(61153,'L','3/32 rectangular push nut','3/32 rect',44,'3'),(61154,'M','1/8 rectangular push nut','1/8 rect',46,'0'),(61155,'N','3/16 rectangular push nut','3/16 rect',50,'7'),(61156,'P','3/16 open acorn push nut','3/16 acorn',99,'4'),(61157,'Q','Item 61157 (lid says not available)','N/A',109,'1')]
J=ex('Nuts 21',P21)
for x,r in zip(J,P21):
    if r[1]=='': x['sku']=str(r[0]); x['where']=f'Nuts 21, front row (SKU {r[0]})'
J[0]['note']=J[2]['note']='The lid lists a black washer push nut here, but the photo shows small acorn nuts.'
J[15]['note']='The lid says NOT AVAILABLE, PUT IN EMPTY BOX, though this compartment holds nuts in the photo.'
I35+=J
PR=[(65961,'A','No. 8 red screw protector','No. 8',37,'0'),(65962,'B','No. 10 black screw protector','No. 10',41,'7'),(65963,'C','1/4 white screw protector','1/4',44,'4'),(65964,'D','5/16 green screw protector','5/16',45,'1'),(65965,'E','3/8 yellow screw protector','3/8',51,'8'),(65966,'F','1/2 gray screw protector','1/2',55,'5'),(65967,'G','3/16 black push nut','3/16',115,'2'),(65968,'H','1/4 white push nut','1/4',125,'9'),(65971,'J','5/16 red push nut','5/16',159,'9'),(65972,'K','3/8 white push nut','3/8',169,'6'),(65973,'L','7/16 black push nut','7/16',179,'3'),(65974,'M','1/2 white push nut','1/2',259,'0')]
I36=ex('Nuts 22',PR)
I36[1]['note']='This drawer has an open gap here, with no box for this item.'
I36+=nuts('Nuts 24','push nut bolt retainer',[(76301,'A','No. 6','',29,'0'),(76302,'B','No. 8','',31,'7'),(76303,'C','No. 10','',33,'4'),(76304,'D','1/4','',34,'1'),(76305,'E','5/16','',37,'8'),(76306,'F','3/8','',42,'5'),(76307,'G','7/16','',46,'2'),(76308,'H','1/2','',51,'9')])
C31=seq([(0,248,[0,400,795,1200]),(248,540,[0,400,815,1200])])
C32=seq([(0,250,[0,152,360,620,888,1000,1190]),(250,540,[0,402,820,1200])])
C33=seq([(0,250,[0,135,300,450,600,750,900,1050,1200]),(250,540,[0,115,262,435,598,750,905,1065,1200])])
C34=seq([(0,250,[0,160,320,475,625,815,1005,1200]),(250,540,[0,265,570,770,970,1200])])
C35=seq([(0,195,[20,180,330,478,622,765,905,1048,1195]),(195,400,[25,185,335,485,628,772,912,1055,1200]),(400,600,[20,180,332,480,625,772,920,1065,1200]),(600,800,[5,165,315,510,660,805,945,1100,1200])])
C36=seq([(0,205,[30,205,290,435,605,800,995,1195]),(205,410,[20,225,420,615,900,1195]),(410,612,[30,245,398,600,900,1195]),(612,800,[20,325,765,1200])])
NEW7=[('Nuts 16','Nylon insert locking wing nuts, 8-32 to 3/8-16 (71780)',I31,C31,540,'d31',None),('Nuts 17','Coupling nuts, coarse thread, 10-24 to 3/4-10 (64500)',I32,C32,540,'d32',None),('Nuts 19','T-nuts, long prong and brad hole, 6-32 to 3/8-16 (60880)',I33,C33,540,'d33','L'),('Nuts 19.5','Round and round projection weld nuts, 8-32 to 1/2-13 (931360)',I34,C34,540,'d33','R'),('Nuts 20 and 21','Speed nuts (61620) and push nuts for rods and axles (61140)',I35,C35,800,'d34',None),('Nuts 22 and 24','Push nuts and screw protectors (65960) and push nut bolt retainers (76300)',I36,C36,800,'d35',None)]
for n,(t,sb,i_,ce,h,fr,sp) in enumerate(NEW7):
    assert sorted(c[0] for c in ce)==list(range(len(i_))),(t,len(ce),len(i_))
    x=dict(title=t,sub=sb,items=i_,img=f'tray{n+31}',cells=ce,h=h,front=fr)
    if sp: x['split']=sp
    dr.append(x)
data=dict(drawers=dr)
'''
k='data=dict(drawers=dr)\n';assert s.count(k)==2 or s.count(k)==1
i=s.rindex(k);s=s[:i]+new+s[i+len(k):]
s=s.replace("for i in range(1,31)}","for i in range(1,36)}").replace("for n in range(2,31): img","for n in range(2,37): img")
open('build.py','w').write(s)
t=open('template.html').read()
a=t.index("D.drawers.forEach((d,i)=>{");b=t.index("for(let c=7;c<=30;c++)")
t=t[:a]+"""let pair;D.drawers.forEach((d,i)=>{const b=document.createElement('button');b.className='tile'+(d.items?' has':'')+(d.split?' half '+d.split:'');b.setAttribute('aria-label','Open drawer: '+d.title);
 b.innerHTML='<img alt="" src="'+IMG[d.front]+'">';b.onclick=()=>open(d,i,b);
 if(d.split==='L'){pair=document.createElement('div');pair.className='pair';grid.appendChild(pair)}
 (d.split?pair:grid).appendChild(b)});
"""+t[b:]
R=[("for(let c=7;c<=30;c++)","for(let c=8;c<=30;c++)"),("$('front').src=IMG['d'+(i+1)];","$('front').src=IMG[d.front];"),("Columns 1 to 6 are done. Scroll sideways for the other 24.","Columns 1 to 7 are done. Scroll sideways for the other 23."),
(".empty{",".pair{display:flex;gap:2px;aspect-ratio:720/150}.tile.half{width:calc(50% - 1px);height:100%;aspect-ratio:auto}.tile.half img{width:calc(200% + 2px);max-width:none}.tile.half.R img{margin-left:calc(-100% - 2px)}.empty{")]
for o,n in R:
    assert o in t,o;t=t.replace(o,n)
open('template.html','w').write(t)

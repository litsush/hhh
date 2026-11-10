s=open('build.py').read()
new='''def tw(z): return z.replace(' x ','<br>x ')
W25=[(64541,'A','6-32 x 1/2','',135,'5'),(64542,'B','6-32 x 1','',149,'2'),(64543,'C','8-32 x 1/2',' wide head',199,'9'),(64544,'D','8-32 x 1/2','',155,'6'),(64545,'E','10-32 x 1/2','',199,'3'),(64546,'F','10-32 x 1','',209,'0'),(64547,'G','10-32 x 1-1/2','',239,'7'),(64548,'H','1/4-20 x 5/8','',189,'4'),(64551,'J','1/4-20 x 3/4','',219,'4'),(64552,'K','1/4-20 x 1','',239,'1'),(64553,'L','5/16-18 x 3/4','',329,'8'),(64554,'M','3/8-16 x 1','',439,'5')]
I37=ex('Nuts 25',[(n,L,f'{z}{w_} rubber expansion well nut',tw(z)+(' wide' if w_ else ''),c,k) for n,L,z,w_,c,k in W25])
I37[3]['note']='This compartment was empty in the photo.'
I37+=ex('Nuts 26',[(70721,'A','6-32 short jack nut, 21/64 drill bit','6-32 short',135,'2'),(70722,'B','6-32 long jack nut, 21/64 drill bit','6-32 long',135,'9'),(70723,'C','10-24 short jack nut, 25/64 drill bit','10-24 short',159,'6'),(70724,'D','10-24 long jack nut, 25/64 drill bit','10-24 long',169,'3'),(70725,'E','1/4-20 short jack nut, 7/16 drill bit','1/4-20 short',185,'0'),(70726,'F','1/4-20 long jack nut, 7/16 drill bit','1/4-20 long',199,'7'),(70727,'G','6mm x 1.00 pitch jack nut, 7/16 drill bit','6mm',279,'4'),(70728,'H','4 inch friction wrench','Wrench',429,'1')])
C37=seq([(0,195,[30,180,328,472,615,800,985,1180]),(195,388,[35,235,428,615,900,1195])])+[[12,15,388,472,490],[13,15,490,472,595],[14,15,595,472,695],[15,15,695,472,800],[16,472,388,908,520],[17,472,520,908,660],[18,472,660,908,800],[19,908,388,1200,800]]
I38=nuts('Nuts 30','grade 5 hex nut',[(69121,'A','1/4-28','fine',32,'4'),(69122,'B','5/16-24','fine',37,'1'),(69123,'C','3/8-24','fine',46,'8'),(69124,'D','7/16-20','fine',66,'5'),(69125,'E','1/2-20','fine',75,'2'),(69126,'F','9/16-18','fine',125,'9'),(69127,'G','5/8-18','fine',135,'6'),(69128,'H','3/4-16','fine',175,'3'),(69131,'J','7/8-14','fine',279,'3'),(69132,'K','1-14','fine',439,'0')])
C38=seq([(0,262,[0,160,305,498,690,965,1200]),(262,540,[0,210,505,905,1200])])
I39=nuts('Nuts 31','USS grade 8 hex nut',[(63041,'A','1/4-20','coarse',41,'1'),(63042,'B','5/16-18','coarse',53,'8'),(63043,'C','3/8-16','coarse',66,'5'),(63044,'D','7/16-14','coarse',85,'2'),(63045,'E','1/2-13','coarse',109,'9'),(63046,'F','9/16-12','coarse',145,'6'),(63047,'G','5/8-11','coarse',175,'3'),(63048,'H','3/4-10','coarse',219,'0'),(63051,'J','7/8-9','coarse',329,'0'),(63052,'K','1-8','coarse',479,'7')])
C39=seq([(0,250,[0,165,318,510,700,985,1200]),(250,540,[0,200,510,820,1200])])
I40=nuts('Nuts 33','grade 8 nylon insert lock nut',[(76261,'A','1/4-20','coarse',115,'7'),(76262,'B','5/16-18','coarse',135,'4'),(76263,'C','3/8-16','coarse',155,'1'),(76264,'D','7/16-14','coarse',199,'8'),(76268,'H','1/4-28','fine',135,'6'),(76271,'J','5/16-24','fine',155,'6'),(76272,'K','3/8-24','fine',175,'3'),(76273,'L','7/16-20','fine',239,'0'),(76265,'E','1/2-13','coarse',219,'5'),(76266,'F','5/8-11','coarse',269,'2'),(76267,'G','3/4-10','coarse',359,'9'),(76274,'M','1/2-20','fine',219,'7'),(76275,'N','5/8-18','fine',279,'4'),(76276,'P','3/4-16','fine',379,'1')])
C40=seq([(0,255,[0,155,305,455,600,742,885,1020,1195]),(255,540,[0,190,395,600,800,1000,1200])])
I41=nuts('Nuts 35','solid brass wing nut',[(71761,'A','10-24','coarse',135,'7'),(71762,'B','10-32','fine',149,'4'),(71763,'C','1/4-20','coarse',159,'1'),(71764,'D','5/16-18','coarse',209,'8'),(71765,'E','3/8-16','coarse',279,'5'),(71766,'F','1/2-13','coarse',539,'2')])
I41[4]['note']='This compartment also holds a small loose box with a handwritten label and darker wing nuts.'
C41=seq([(0,250,[5,325,625,910,1200]),(250,540,[0,632,1200])])
R36=[(61061,'A','4-40','cap nut, brass',85,'1'),(61062,'B','6-32','cap nut, brass',89,'8'),(61063,'C','8-32','cap nut, brass',95,'5'),(61064,'D','10-24','cap nut, brass',105,'2'),(61065,'E','1/4-20','cap nut, brass',125,'9'),(61066,'F','5/16-18','cap nut, brass',159,'6'),(61067,'G','3/8-16','cap nut, brass',209,'3'),(61068,'H','10-32','cap nut, brass',115,'0'),(61071,'J','6-32','knurled nut, brass',115,'0'),(61072,'K','8-32','knurled nut, brass',125,'7'),(61073,'L','10-32','knurled nut, brass',135,'4'),(61074,'M','6-32','cap nut, nickel plated brass',89,'1'),(61075,'N','8-32','cap nut, nickel plated brass',95,'8'),(61076,'P','10-24','cap nut, nickel plated brass',115,'5'),(61077,'Q','1/4-20','cap nut, nickel plated brass',135,'2'),(61078,'R','10-32','cap nut, nickel plated brass',115,'9')]
I42=ex('Nuts 36',[(n,L,f'{z} {k_}',z,c,kk) for n,L,z,k_,c,kk in R36])
I42[14]['note']='This compartment was empty in the photo.'
C42=seq([(0,250,[0,155,305,460,605,750,895,1040,1180]),(250,540,[0,135,295,440,600,750,900,1045,1200])])
I43=nuts('Nuts 37','black oxide hex nut',[(34161,'A','6-32','',28,'4'),(34162,'B','8-32','',30,'1'),(34163,'C','10-24','',31,'8'),(34164,'D','10-32','',31,'5'),(34165,'E','1/4-20','',32,'2'),(34166,'F','5/16-18','',32,'9')])
I43+=nuts('Nuts 37','black oxide lock nut',[(34167,'G','6-32','',41,'6'),(34168,'H','8-32','',43,'3'),(34171,'J','10-24','',44,'3'),(34172,'K','10-32','',44,'0'),(34173,'L','1/4-20','',57,'7'),(34174,'M','5/16-18','',57,'4')])
C43=seq([(0,248,[5,205,400,600,785,980,1180]),(248,540,[0,205,410,605,805,1005,1200])])
NEW8=[('Nuts 25 and 26','Rubber expansion well nuts (64540) and jack nuts with friction wrench (70720)',I37,C37,800,'d36',None),('Nuts 30','Grade 5 hex nuts, fine thread, 1/4-28 to 1-14 (69120)',I38,C38,540,'d37',None),('Nuts 31','USS grade 8 hex nuts, coarse thread, 1/4-20 to 1-8 (63040)',I39,C39,540,'d38',None),('Nuts 33','Grade 8 nylon insert lock nuts, 1/4-20 to 3/4-16 (76260)',I40,C40,540,'d39','L'),('Nuts 35','Solid brass wing nuts, 10-24 to 1/2-13 (71760)',I41,C41,540,'d39','R'),('Nuts 36','Solid brass cap and knurled nuts, plus nickel plated cap nuts (61060)',I42,C42,540,'d40','L'),('Nuts 37','Black oxide hex and lock nuts, 6-32 to 5/16-18 (34160)',I43,C43,540,'d40','R')]
for n,(t,sb,i_,ce,h,fr,sp) in enumerate(NEW8):
    assert sorted(c[0] for c in ce)==list(range(len(i_))),(t,len(ce),len(i_))
    x=dict(title=t,sub=sb,items=i_,img=f'tray{n+37}',cells=ce,h=h,front=fr)
    if sp: x['split']=sp
    dr.append(x)
data=dict(drawers=dr)
'''
k='data=dict(drawers=dr)\n';i=s.rindex(k);s=s[:i]+new+s[i+len(k):]
s=s.replace("for i in range(1,36)}","for i in range(1,41)}").replace("for n in range(2,37): img","for n in range(2,44): img")
open('build.py','w').write(s)
t=open('template.html').read()
for o,n in [("for(let c=8;c<=30;c++)","for(let c=9;c<=30;c++)"),("Columns 1 to 7 are done. Scroll sideways for the other 23.","Columns 1 to 8 are done. Scroll sideways for the other 22.")]:
    assert o in t;t=t.replace(o,n)
open('template.html','w').write(t)

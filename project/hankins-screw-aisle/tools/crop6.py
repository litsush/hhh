import cv2,numpy as np
U='/mnt/user-data/uploads/'
def warp(im,q,w,h):
    M=cv2.getPerspectiveTransform(np.float32(q),np.float32([[0,0],[w,0],[w,h],[0,h]]))
    return cv2.warpPerspective(im,M,(w,h),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
f=cv2.imread(U+'34c0d104-image.jpg')
F=[[(10,325),(1510,330),(1512,625),(0,620)],[(20,655),(1495,645),(1500,935),(15,935)],[(30,975),(1480,965),(1500,1240),(10,1240)],[(55,1260),(1460,1245),(1470,1525),(45,1525)],[(75,1530),(1425,1510),(1455,1760),(55,1760)]]
s=[]
for i,q in enumerate(F):
    w=warp(f,q,720,150);cv2.imwrite(f'img/d{i+16}.jpg',w,[cv2.IMWRITE_JPEG_QUALITY,78]);s.append(w)
cv2.imwrite('f4.jpg',np.vstack(s))
T={16:('d29641cc',[(175,1088),(1432,1068),(1530,1610),(-20,1610)],520),
   17:('7160ce6f',[(300,1042),(1195,1030),(1510,2016),(62,2016)],800),
   18:('11d37469',[(185,1062),(1440,1030),(1520,1615),(15,1640)],540),
   19:('b49826e7',[(318,1048),(1198,1025),(1520,2016),(72,2016)],800),
   20:('a9583914',[(122,1000),(1300,945),(1525,1540),(-15,1590)],520)}
for n,(a,q,h) in T.items():
    t=warp(cv2.imread(U+a+'-image.jpg'),q,1200,h);cv2.imwrite(f'img/tray{n}.jpg',t,[cv2.IMWRITE_JPEG_QUALITY,74])
    g=t.copy()
    for x in range(0,1200,100):
        cv2.line(g,(x,0),(x,h),(0,255,255),1);cv2.putText(g,str(x),(x+2,16),0,.5,(0,255,0),2)
    for y in range(0,h,100):
        cv2.line(g,(0,y),(1200,y),(0,255,255),1);cv2.putText(g,str(y),(2,y+16),0,.5,(0,255,0),2)
    cv2.imwrite(f'g{n}.jpg',g,[cv2.IMWRITE_JPEG_QUALITY,80])

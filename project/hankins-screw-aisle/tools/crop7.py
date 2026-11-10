import cv2,numpy as np
U='/mnt/user-data/uploads/'
def warp(im,q,w,h):
    M=cv2.getPerspectiveTransform(np.float32(q),np.float32([[0,0],[w,0],[w,h],[0,h]]))
    return cv2.warpPerspective(im,M,(w,h),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
f=cv2.imread(U+'8e918d56-image.jpg')
F=[[(25,335),(1512,320),(1512,610),(15,610)],[(55,665),(1505,645),(1510,925),(45,925)],[(90,970),(1480,950),(1495,1215),(75,1215)],[(115,1260),(1465,1240),(1480,1495),(100,1495)],[(140,1530),(1450,1500),(1480,1745),(125,1745)]]
s=[]
for i,q in enumerate(F):
    w=warp(f,q,720,150);cv2.imwrite(f'img/d{i+21}.jpg',w,[cv2.IMWRITE_JPEG_QUALITY,78]);s.append(w)
cv2.imwrite('f5.jpg',np.vstack(s))
T={21:('26639132',[(160,1045),(1400,1015),(1510,1645),(-20,1680)],540),
   22:('1c381a03',[(115,1140),(1370,1105),(1520,1745),(-25,1770)],540),
   23:('dfd3b5ad',[(125,1160),(1375,1130),(1510,1830),(-20,1850)],600),
   24:('af04237e',[(130,1075),(1370,1035),(1500,1680),(-20,1710)],540),
   25:('ab8dbd1c',[(170,1060),(1360,1020),(1510,1640),(-5,1680)],520)}
for n,(a,q,h) in T.items():
    t=warp(cv2.imread(U+a+'-image.jpg'),q,1200,h);cv2.imwrite(f'img/tray{n}.jpg',t,[cv2.IMWRITE_JPEG_QUALITY,74])
    g=t.copy()
    for x in range(0,1200,100):
        cv2.line(g,(x,0),(x,h),(0,255,255),1);cv2.putText(g,str(x),(x+2,16),0,.5,(0,255,0),2)
    for y in range(0,h,100):
        cv2.line(g,(0,y),(1200,y),(0,255,255),1);cv2.putText(g,str(y),(2,y+16),0,.5,(0,255,0),2)
    cv2.imwrite(f'g{n}.jpg',g,[cv2.IMWRITE_JPEG_QUALITY,80])
z=cv2.imread(U+'dfd3b5ad-image.jpg')[640:1040,0:1512];cv2.imwrite('z74.jpg',cv2.resize(z,None,fx=1.3,fy=1.3,interpolation=cv2.INTER_CUBIC))

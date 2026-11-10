import cv2,numpy as np
U='/mnt/user-data/uploads/'
def warp(im,q,w,h):
    M=cv2.getPerspectiveTransform(np.float32(q),np.float32([[0,0],[w,0],[w,h],[0,h]]))
    return cv2.warpPerspective(im,M,(w,h),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
f=cv2.imread(U+'6ed38ca1-image.jpg')
F=[[(38,358),(1422,348),(1425,535),(42,535)],[(58,668),(1420,662),(1418,850),(60,865)],[(85,955),(1398,945),(1398,1105),(92,1112)],[(95,1225),(1382,1202),(1388,1352),(100,1375)],[(112,1482),(1370,1472),(1372,1610),(118,1618)]]
s=[]
for i,q in enumerate(F):
    w=warp(f,q,720,150);cv2.imwrite(f'img/d{i+36}.jpg',w,[cv2.IMWRITE_JPEG_QUALITY,78]);s.append(w)
cv2.imwrite('f8.jpg',np.vstack(s))
T={37:('838ad8f0',[(312,990),(1200,985),(1490,1975),(105,1985)],800),
   38:('58e869c3',[(140,975),(1405,960),(1510,1610),(0,1640)],540),
   39:('ccbd62f8',[(125,1010),(1385,970),(1510,1640),(0,1680)],540),
   40:('99dcf38a',[(160,1105),(1425,1125),(1505,1830),(0,1720)],540),
   41:('fefed914',[(105,1015),(1385,990),(1512,1700),(30,1735)],540),
   42:('79df6f93',[(105,1155),(1395,1160),(1500,1880),(0,1815)],540),
   43:('07195964',[(85,1095),(1390,1020),(1480,1690),(0,1825)],540)}
for n,(a,q,h) in T.items():
    t=warp(cv2.imread(U+a+'-image.jpg'),q,1200,h);cv2.imwrite(f'img/tray{n}.jpg',t,[cv2.IMWRITE_JPEG_QUALITY,74])
    g=t.copy()
    for x in range(0,1200,100):
        cv2.line(g,(x,0),(x,h),(0,255,255),1);cv2.putText(g,str(x),(x+2,16),0,.5,(0,255,0),2)
    for y in range(0,h,100):
        cv2.line(g,(0,y),(1200,y),(0,255,255),1);cv2.putText(g,str(y),(2,y+16),0,.5,(0,255,0),2)
    cv2.imwrite(f'g{n}.jpg',g,[cv2.IMWRITE_JPEG_QUALITY,80])

import cv2,numpy as np
U='/mnt/user-data/uploads/'
def warp(im,q,w,h):
    M=cv2.getPerspectiveTransform(np.float32(q),np.float32([[0,0],[w,0],[w,h],[0,h]]))
    return cv2.warpPerspective(im,M,(w,h),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
f=cv2.imread(U+'abf75f0e-image.jpg')
F=[[(15,365),(1505,370),(1505,600),(10,592)],[(22,692),(1488,692),(1480,905),(28,905)],[(42,1002),(1480,992),(1478,1175),(48,1175)],[(62,1290),(1465,1298),(1470,1468),(60,1468)],[(78,1570),(1452,1568),(1456,1738),(70,1738)]]
s=[]
for i,q in enumerate(F):
    w=warp(f,q,720,150);cv2.imwrite(f'img/d{i+31}.jpg',w,[cv2.IMWRITE_JPEG_QUALITY,78]);s.append(w)
cv2.imwrite('f7.jpg',np.vstack(s))
T={31:('5672784d',[(125,1120),(1345,1095),(1505,1730),(0,1790)],540),
   32:('39abea29',[(125,1110),(1375,1090),(1510,1770),(0,1815)],540),
   33:('d67ef883',[(135,1078),(1395,1085),(1505,1765),(0,1700)],540),
   34:('8f2fde3c',[(105,1150),(1350,1130),(1512,1770),(0,1850)],540),
   35:('8c1a895d',[(305,1015),(1205,1005),(1510,2016),(75,2016)],800),
   36:('26e688c2',[(305,1010),(1205,1005),(1510,2016),(105,2016)],800)}
for n,(a,q,h) in T.items():
    t=warp(cv2.imread(U+a+'-image.jpg'),q,1200,h);cv2.imwrite(f'img/tray{n}.jpg',t,[cv2.IMWRITE_JPEG_QUALITY,74])
    g=t.copy()
    for x in range(0,1200,100):
        cv2.line(g,(x,0),(x,h),(0,255,255),1);cv2.putText(g,str(x),(x+2,16),0,.5,(0,255,0),2)
    for y in range(0,h,100):
        cv2.line(g,(0,y),(1200,y),(0,255,255),1);cv2.putText(g,str(y),(2,y+16),0,.5,(0,255,0),2)
    cv2.imwrite(f'g{n}.jpg',g,[cv2.IMWRITE_JPEG_QUALITY,80])

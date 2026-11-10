import cv2,numpy as np
U='/mnt/user-data/uploads/'
def warp(im,q,w,h):
    M=cv2.getPerspectiveTransform(np.float32(q),np.float32([[0,0],[w,0],[w,h],[0,h]]))
    return cv2.warpPerspective(im,M,(w,h),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
f=cv2.imread(U+'9193fc01-image.jpg')
F=[[(5,405),(1495,400),(1495,665),(5,660)],[(15,755),(1505,765),(1505,955),(20,950)],[(10,1090),(1505,1100),(1505,1285),(10,1280)],[(55,1370),(1445,1372),(1445,1522),(55,1522)],[(85,1625),(1415,1625),(1415,1765),(85,1765)]]
s=[]
for i,q in enumerate(F):
    w=warp(f,q,720,150);cv2.imwrite(f'img/d{i+46}.jpg',w,[cv2.IMWRITE_JPEG_QUALITY,78]);s.append(w)
cv2.imwrite('f10.jpg',np.vstack(s))
T={49:('6dd5b8d0',[(95,1010),(1490,1000),(1512,1660),(0,1670)],540),
   50:('2b10f6b3',[(305,995),(1170,990),(1395,2016),(115,2016)],800),
   51:('5d180bbe',[(330,1030),(1200,1030),(1420,2000),(190,2000)],800),
   52:('3ed83339',[(300,1005),(1225,1005),(1380,2016),(150,2016)],800),
   53:('4ce9521f',[(335,995),(1210,995),(1390,2016),(180,2016)],800)}
for n,(a,q,h) in T.items():
    t=warp(cv2.imread(U+a+'-image.jpg'),q,1200,h);cv2.imwrite(f'img/tray{n}.jpg',t,[cv2.IMWRITE_JPEG_QUALITY,74])
    g=t.copy()
    for x in range(0,1200,100):
        cv2.line(g,(x,0),(x,h),(0,255,255),1);cv2.putText(g,str(x),(x+2,16),0,.5,(0,255,0),2)
    for y in range(0,h,100):
        cv2.line(g,(0,y),(1200,y),(0,255,255),1);cv2.putText(g,str(y),(2,y+16),0,.5,(0,255,0),2)
    cv2.imwrite(f'g{n}.jpg',g,[cv2.IMWRITE_JPEG_QUALITY,80])

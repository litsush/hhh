import cv2,numpy as np
U='/mnt/user-data/uploads/'
def warp(im,q,w,h):
    M=cv2.getPerspectiveTransform(np.float32(q),np.float32([[0,0],[w,0],[w,h],[0,h]]))
    return cv2.warpPerspective(im,M,(w,h),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
f=cv2.imread(U+'5e8cea67-image.jpg')
F=[[(0,195),(1512,190),(1512,510),(0,505)],[(8,535),(1508,525),(1510,835),(10,830)],[(35,855),(1495,845),(1500,1135),(38,1130)],[(68,1155),(1482,1148),(1488,1435),(65,1425)],[(98,1450),(1458,1430),(1485,1712),(72,1712)]]
s=[]
for i,q in enumerate(F):
    w=warp(f,q,720,150);cv2.imwrite(f'img/d{i+6}.jpg',w,[cv2.IMWRITE_JPEG_QUALITY,78]);s.append(w)
cv2.imwrite('f2.jpg',np.vstack(s))
T={6:('0cfdf6ad',[(285,1040),(1140,1015),(1430,2016),(100,2016)],800),
   7:('0a03b609',[(315,1040),(1160,1030),(1443,2016),(94,2016)],800),
   8:('367e7743',[(300,1030),(1175,1010),(1505,2016),(66,2016)],800),
   9:('1f6e1d66',[(300,1020),(1170,1010),(1505,2016),(40,2016)],800),
   10:('ab57ee8f',[(120,1085),(1320,1040),(1510,1660),(0,1735)],520)}
for n,(a,q,h) in T.items():
    t=warp(cv2.imread(U+a+'-image.jpg'),q,1200,h);cv2.imwrite(f'img/tray{n}.jpg',t,[cv2.IMWRITE_JPEG_QUALITY,74])
    g=t.copy()
    for x in range(0,1200,100):
        cv2.line(g,(x,0),(x,h),(0,255,255),1);cv2.putText(g,str(x),(x+2,16),0,.5,(0,255,0),2)
    for y in range(0,h,100):
        cv2.line(g,(0,y),(1200,y),(0,255,255),1);cv2.putText(g,str(y),(2,y+16),0,.5,(0,255,0),2)
    cv2.imwrite(f'g{n}.jpg',g,[cv2.IMWRITE_JPEG_QUALITY,80])

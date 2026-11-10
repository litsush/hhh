import cv2,numpy as np
U='/mnt/user-data/uploads/'
def warp(im,q,w,h):
    M=cv2.getPerspectiveTransform(np.float32(q),np.float32([[0,0],[w,0],[w,h],[0,h]]))
    return cv2.warpPerspective(im,M,(w,h),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
f=cv2.imread(U+'de1fc09a-image.jpg')
F=[[(30,365),(1490,365),(1490,595),(30,590)],[(50,685),(1480,685),(1480,890),(50,890)],[(75,975),(1470,975),(1470,1150),(75,1150)],[(90,1265),(1465,1270),(1465,1440),(90,1440)],[(120,1525),(1425,1525),(1425,1672),(120,1672)]]
s=[]
for i,q in enumerate(F):
    w=warp(f,q,720,150);cv2.imwrite(f'img/d{i+41}.jpg',w,[cv2.IMWRITE_JPEG_QUALITY,78]);s.append(w)
cv2.imwrite('f9.jpg',np.vstack(s))
T={44:('60ed849a',[(115,1075),(1395,1040),(1510,1720),(0,1760)],540),
   45:('bf8e7fcb',[(85,1095),(1400,1070),(1512,1760),(-10,1810)],540),
   46:('c0b040ef',[(298,1025),(1190,1005),(1512,2016),(100,2016)],800),
   47:('62025f4c',[(340,1025),(1205,1015),(1490,2016),(140,2016)],800),
   48:('fb92b18b',[(295,1010),(1205,995),(1490,2016),(140,2016)],800)}
for n,(a,q,h) in T.items():
    t=warp(cv2.imread(U+a+'-image.jpg'),q,1200,h);cv2.imwrite(f'img/tray{n}.jpg',t,[cv2.IMWRITE_JPEG_QUALITY,74])
    g=t.copy()
    for x in range(0,1200,100):
        cv2.line(g,(x,0),(x,h),(0,255,255),1);cv2.putText(g,str(x),(x+2,16),0,.5,(0,255,0),2)
    for y in range(0,h,100):
        cv2.line(g,(0,y),(1200,y),(0,255,255),1);cv2.putText(g,str(y),(2,y+16),0,.5,(0,255,0),2)
    cv2.imwrite(f'g{n}.jpg',g,[cv2.IMWRITE_JPEG_QUALITY,80])

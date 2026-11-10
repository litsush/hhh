import cv2,numpy as np
U='/mnt/user-data/uploads/'
def warp(im,q,w,h):
    M=cv2.getPerspectiveTransform(np.float32(q),np.float32([[0,0],[w,0],[w,h],[0,h]]))
    return cv2.warpPerspective(im,M,(w,h),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
f=cv2.imread(U+'d29979ab-image.jpg')
F=[[(0,225),(1512,205),(1512,520),(0,525)],[(3,570),(1505,545),(1512,850),(0,850)],[(3,895),(1498,875),(1512,1165),(0,1165)],[(30,1195),(1475,1175),(1490,1470),(22,1460)],[(45,1488),(1470,1470),(1498,1745),(20,1745)]]
s=[]
for i,q in enumerate(F):
    w=warp(f,q,720,150);cv2.imwrite(f'img/d{i+11}.jpg',w,[cv2.IMWRITE_JPEG_QUALITY,78]);s.append(w)
cv2.imwrite('f3.jpg',np.vstack(s))
T={11:('cfcacf68',[(270,1035),(1125,1012),(1405,2016),(12,2016)],800),
   12:('bc136dbe',[(130,1195),(1360,1170),(1530,1755),(-20,1780)],540),
   13:('db7c7f53',[(370,1040),(1225,1020),(1490,2016),(90,2016)],800),
   14:('bde0e7c5',[(335,1030),(1210,1015),(1475,2016),(45,2016)],800),
   15:('a68c41ed',[(150,1075),(1370,1035),(1530,1725),(10,1765)],560)}
for n,(a,q,h) in T.items():
    t=warp(cv2.imread(U+a+'-image.jpg'),q,1200,h);cv2.imwrite(f'img/tray{n}.jpg',t,[cv2.IMWRITE_JPEG_QUALITY,74])
    g=t.copy()
    for x in range(0,1200,100):
        cv2.line(g,(x,0),(x,h),(0,255,255),1);cv2.putText(g,str(x),(x+2,16),0,.5,(0,255,0),2)
    for y in range(0,h,100):
        cv2.line(g,(0,y),(1200,y),(0,255,255),1);cv2.putText(g,str(y),(2,y+16),0,.5,(0,255,0),2)
    cv2.imwrite(f'g{n}.jpg',g,[cv2.IMWRITE_JPEG_QUALITY,80])

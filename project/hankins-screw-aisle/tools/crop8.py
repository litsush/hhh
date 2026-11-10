import cv2,numpy as np
U='/mnt/user-data/uploads/'
def warp(im,q,w,h):
    M=cv2.getPerspectiveTransform(np.float32(q),np.float32([[0,0],[w,0],[w,h],[0,h]]))
    return cv2.warpPerspective(im,M,(w,h),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
f=cv2.imread(U+'8c27525b-image.jpg')
F=[[(12,252),(1512,262),(1512,505),(5,485)],[(30,588),(1505,605),(1510,822),(25,808)],[(50,895),(1485,905),(1490,1095),(45,1088)],[(55,1198),(1455,1215),(1472,1408),(50,1392)],[(90,1465),(1440,1480),(1445,1640),(80,1632)]]
s=[]
for i,q in enumerate(F):
    w=warp(f,q,720,150);cv2.imwrite(f'img/d{i+26}.jpg',w,[cv2.IMWRITE_JPEG_QUALITY,78]);s.append(w)
cv2.imwrite('f6.jpg',np.vstack(s))
T={26:('4cf6fad4',[(135,1140),(1475,1120),(1570,1790),(-70,1830)],540),
   27:('be3efa2b',[(145,1130),(1345,1115),(1530,1790),(-30,1815)],540),
   28:('4c8a270a',[(310,975),(1150,965),(1455,1960),(95,1975)],800),
   29:('1e91ed25',[(140,1080),(1375,1075),(1510,1665),(-5,1680)],540),
   30:('1e0828cc',[(335,1005),(1215,1000),(1510,2016),(110,2016)],800)}
for n,(a,q,h) in T.items():
    t=warp(cv2.imread(U+a+'-image.jpg'),q,1200,h);cv2.imwrite(f'img/tray{n}.jpg',t,[cv2.IMWRITE_JPEG_QUALITY,74])
    g=t.copy()
    for x in range(0,1200,100):
        cv2.line(g,(x,0),(x,h),(0,255,255),1);cv2.putText(g,str(x),(x+2,16),0,.5,(0,255,0),2)
    for y in range(0,h,100):
        cv2.line(g,(0,y),(1200,y),(0,255,255),1);cv2.putText(g,str(y),(2,y+16),0,.5,(0,255,0),2)
    cv2.imwrite(f'g{n}.jpg',g,[cv2.IMWRITE_JPEG_QUALITY,80])

import cv2,numpy as np
U='/mnt/user-data/uploads/'
Q={2:('a6bc5ce2',[(245,1080),(1150,1062),(1455,2016),(-72,2016)]),
   3:('5735d399',[(232,1040),(1175,1030),(1432,2016),(-50,2016)]),
   4:('b375e796',[(268,1025),(1215,1018),(1478,2016),(20,2016)]),
   5:('e4e0827d',[(278,1030),(1205,1015),(1460,2016),(85,2016)])}
def warp(im,q,w,h):
    M=cv2.getPerspectiveTransform(np.float32(q),np.float32([[0,0],[w,0],[w,h],[0,h]]))
    return cv2.warpPerspective(im,M,(w,h),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
sheet=[]
for n,(f,q) in Q.items():
    t=warp(cv2.imread(U+f+'-image.jpg'),q,1200,800);cv2.imwrite(f'img/tray{n}.jpg',t,[cv2.IMWRITE_JPEG_QUALITY,74])
    g=t.copy()
    for x in range(0,1200,100):
        cv2.line(g,(x,0),(x,800),(0,255,255),1);cv2.putText(g,str(x),(x+2,16),0,.5,(0,255,0),2)
    for y in range(0,800,100):
        cv2.line(g,(0,y),(1200,y),(0,255,255),1);cv2.putText(g,str(y),(2,y+16),0,.5,(0,255,0),2)
    cv2.imwrite(f'g{n}.jpg',g,[cv2.IMWRITE_JPEG_QUALITY,80])
im=cv2.imread(U+'a6bc5ce2-image.jpg');c=im[120:470,930:1190];cv2.imwrite('z.jpg',cv2.resize(c,None,fx=2.4,fy=2.4,interpolation=cv2.INTER_CUBIC))

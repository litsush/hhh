import cv2,numpy as np
U='/mnt/user-data/uploads/'
f=cv2.imread(U+'52af7330-image.jpg'); o=cv2.imread(U+'30cfd307-image.jpg')
def warp(im,q,w,h):
    M=cv2.getPerspectiveTransform(np.float32(q),np.float32([[0,0],[w,0],[w,h],[0,h]]))
    return cv2.warpPerspective(im,M,(w,h),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
Q=[[(42,730),(1470,745),(1455,1035),(42,985)],
   [(85,1008),(1412,1035),(1400,1285),(88,1235)],
   [(110,1265),(1378,1290),(1365,1520),(112,1470)],
   [(130,1500),(1345,1525),(1335,1740),(135,1690)],
   [(140,1735),(1325,1765),(1315,1960),(145,1915)]]
for i,q in enumerate(Q):
    cv2.imwrite(f'img/d{i+1}.jpg',warp(f,q,720,150),[cv2.IMWRITE_JPEG_QUALITY,78])
# tray: use outer corners, bottom row extended to photo bottom
tray=warp(o,[(272,1058),(1150,1045),(1395,2016),(30,2016)],1200,800)
cv2.imwrite('img/tray.jpg',tray,[cv2.IMWRITE_JPEG_QUALITY,74])
s=np.vstack([cv2.imread(f'img/d{i}.jpg') for i in range(1,6)]);cv2.imwrite('fronts_check.jpg',s)

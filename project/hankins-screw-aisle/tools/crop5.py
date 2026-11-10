import cv2,numpy as np
im=cv2.imread('/mnt/user-data/uploads/aa185895-image.jpg')
q=[(135,305),(1350,318),(1530,1620),(-20,1620)];w,h=1200,800
M=cv2.getPerspectiveTransform(np.float32(q),np.float32([[0,0],[w,0],[w,h],[0,h]]))
t=cv2.warpPerspective(im,M,(w,h),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
cv2.imwrite('img/tray6.jpg',t,[cv2.IMWRITE_JPEG_QUALITY,74])
g=t.copy()
for x in range(0,1200,100):
    cv2.line(g,(x,0),(x,h),(0,255,255),1);cv2.putText(g,str(x),(x+2,16),0,.5,(0,255,0),2)
for y in range(0,h,100):
    cv2.line(g,(0,y),(1200,y),(0,255,255),1);cv2.putText(g,str(y),(2,y+16),0,.5,(0,255,0),2)
cv2.imwrite('g6.jpg',g,[cv2.IMWRITE_JPEG_QUALITY,80])

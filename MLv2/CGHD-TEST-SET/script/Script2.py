import cv2 
import numpy as np
import os
import matplotlib.pyplot as plt

ldir=os.listdir('../')

print('Dir list:',ldir)
print('Writing to storage:')
#reading image
for imgn in ldir:
    if imgn=='script':
        break
    imadd='../'+imgn
    image = cv2.imread(imadd)  
    image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    er=cv2.getStructuringElement(cv2.MORPH_RECT , (6,8))
    dil=cv2.getStructuringElement(cv2.MORPH_RECT , (6,9))
    bg=image
    for i in range(10):
        bg=cv2.morphologyEx(bg, cv2.MORPH_DILATE, dil)
        bg=cv2.morphologyEx(bg, cv2.MORPH_ERODE, er)

    out_gray=cv2.divide(image, bg, scale=255)
    out_binary=cv2.threshold(out_gray, 0, 255, cv2.THRESH_OTSU )[1] 

    cv2.imwrite(imgn,out_binary)
    print(imgn, end=' ')
#    opening = cv2.morphologyEx(out_binary, cv2.MORPH_OPEN,dil)

#    cv2.imwrite('open/'+imgn+'_o.png',opening)

 #   edges = cv2.Canny(opening, 50, 150)

 #   cv2.imwrite('edges/'+imgn+'_e.png',edges)
#    lines = cv2.HoughLinesP(edges,1,np.pi/180,40,minLineLength=10,maxLineGap=30)
#    result=edges
#    for x1,y1,x2,y2 in lines[0]:
#        i+=1
#        cv2.line(result,(x1,y1),(x2,y2),(255,0,0),1)

#    cv2.imwrite('res/'+imgn+'_r.png',result)

cv2.waitKey(0)

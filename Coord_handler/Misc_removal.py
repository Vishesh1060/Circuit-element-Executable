import Image_handler as Ih
import cv2
import os
from modelcsv import csvparse

imdir='../MLv2/CGHD-TEST-SET'
listimg=os.listdir(imdir)
img2=[]

x=0
for imgname in listimg:
    print('reading:',imdir+'/'+imgname)
    img = cv2.imread(imdir+'/'+imgname)
    bg=Ih.image_resize(img,width=879)
#    cv2.imshow('original',img)
    er=cv2.getStructuringElement(cv2.MORPH_RECT , (6,8))
    dil=cv2.getStructuringElement(cv2.MORPH_RECT , (6,9))
    for i in range(10):
        bg=cv2.morphologyEx(bg, cv2.MORPH_DILATE, dil)
        bg=cv2.morphologyEx(bg, cv2.MORPH_ERODE, er)
#    out_gray=cv2.divide(img, bg, scale=255)
    out_binary=cv2.threshold(bg, 0, 255, cv2.THRESH_OTSU )[1]
    cv2.imshow('bg'+str(x),out_binary)
#    img2.append(Ih.image_remove_background(img, imgData=0))
    x=x+1
    if(x>=1):
        break
'''    
for i in range(0,x):
    cv2.imshow('NoBG'+str(i),img2[i])
'''    
cv2.waitKey(0)
cv2.destroyAllWindows()
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 09:35:40 2023

@author: vishesh
"""

import cv2  
import numpy as np
import csv
import os
import json
import Image_handler as Ih
from modelcsv import csvparse

#from jsformat import jsout

(imgData,i,j)=({},-1,-1)
jsout_dir='../out_json/'
imdir="../MLv2/imgs/sv_ (28).jpg"
imgData=csvparse('../Mlv2/out_imgs/sv_ (28).csv')
img = cv2.imread(imdir)
img,(rw,ry)=Ih.new_image_resize(img,width=800)


def imdiv(imgData):
    elis=imgData['element_id']
    xaxs=[]
    flag=0
    for x in range(len(elis)):  
        if elis[x].startswith('G'):
            xval=int(rw*imgData['rectangle_bottom_right'][x][0])
            print('xval=',xval,end=' ')
            if xaxs==[]:
                flag=1
            else:
                for y in xaxs:
                    if abs(y-xval)>=30 or xaxs==[]:
                        flag=1
                        print(y,xval,abs(y-xval),"y,xval,abs")
            if flag==1:            
                xaxs.append(xval)
                flag=0
    xaxs.sort()
    print(xaxs)
    return xaxs
            
c=imdiv(imgData)

for cv in c:
    c2=(cv,imgData['img_height'][0])
    c1=(cv,0)
    cv2.line(img,c1,c2,(int(155-i*10),100+i*10,50*i), 2)
    cv2.putText(img,imgData['element_id'][i],c2, cv2.FONT_HERSHEY_DUPLEX, 0.8,(162,252, 252), 1)

img=Ih.image_label_all(img, imgData)
cv2.imshow('ab',img)
cv2.waitKey(0)
cv2.destroyAllWindows()


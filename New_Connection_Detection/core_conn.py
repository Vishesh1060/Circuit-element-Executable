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
imdir="../MLv2/imgs/sv_ (41).jpg"
imgData=csvparse('../Mlv2/out_imgs/sv_ (41).csv')
img = cv2.imread(imdir)
img,(rw,ry)=Ih.new_image_resize(img,width=800)
original=img.copy()

for idx,elemid in enumerate(imgData['element_id']):
    print(idx,'Removing',elemid,imgData['element_name'][idx])
    if idx>=1:
        img=Ih.image_remove_element(img, imgData, elemid,mflag=1)
    else:
        img=Ih.image_remove_element(img, imgData, elemid,mflag=0)


def ValidateDivRange(xaxs):
    divcoords,flag=[],1
    for val in xaxs:
#        xaxs.remove(val)
        if val in divcoords:
            flag=0
        for ranval in divcoords:
            if ranval >=(val-30) and ranval <= (val+30):
                flag=0
        if flag==1:
            divcoords.append(val)
        flag=1
    return divcoords

def imagediv(imgData):
    elis=imgData['element_id']
    xaxs=[]
    flag=0
    for x in range(len(elis)):  
        if elis[x].startswith('G'):
            xval=int(rw*imgData['rectangle_bottom_right'][x][0])
#            print('xval=',xval,end=' ')
            if xaxs==[]:
                flag=1
            else:
                for y in xaxs:
                    if abs(y-xval)>=30 or xaxs==[]:
                        flag=1
#                        print(y,xval,abs(y-xval),"y,xval,abs")
            if flag==1:            
                xaxs.append(xval)
                flag=0
    xaxs.sort()
    divcoords=ValidateDivRange(xaxs.copy())
    print("--",xaxs)
    print("-+",divcoords)
    return xaxs,divcoords

def linedtn(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bounding_boxes = []
    lineset1=[]
    kernel=np.ones((2,4),np.uint8)
    structure=np.ones((1,13),np.uint8)
    hlines=cv2.dilate(img,kernel,iterations=1)
    hlines=cv2.erode(hlines,structure,iterations=5)
    
    for cnt in contours:
        # Get the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(cnt)
        # Append the coordinates to the list
        linetopleft=(x, y)
        linebottomright=(x + w, y + h)
        lineset1.append((linetopleft,linebottomright))
        bounding_boxes.append(((x, y), (x + w, y + h)))
        # Draw the rectangle on the image for visualization
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return img
    
            
c,cdash=imagediv(imgData)

img2=img.copy()

i=0
for cv in cdash:
    i+=5
    c2=(cv,imgData['img_height'][0])
    c1=(cv,0)
    cv2.line(img2,c1,c2,(int(155-i*2),50+i*7,50*i), 2)
i=0
for cv in c:
    i+=5
    c2=(cv,imgData['img_height'][0])
    c1=(cv,0)
    cv2.line(img,c1,c2,(int(155-i*2),50+i*7,50*i), 2)
#    cv2.putText(img,imgData['element_id'][i],c2, cv2.FONT_HERSHEY_DUPLEX, 0.8,(162,252, 252), 1)

cropped=[]
height,width,_=img2.shape
cdash.append(width)
for indx,val in enumerate(cdash):
    if indx==0:
        crpd=img2[0:height,0:val]
        print((0,val))
    else:
        crpd=img2[0:height,cdash[indx-1]:val]
        print((cdash[indx-1],val),end='')
    
    cropped.append(crpd)
    
i=0
for crpimgs in cropped:    
    i+=1
    cv2.imshow('crps'+str(i),crpimgs)
    det1=linedtn(crpimgs)
    cv2.imshow('crpsline'+str(i),det1)
    
#img=Ih.image_label_all(img, imgData)
cv2.imshow('ab',img)
cv2.imshow('ab2',img2)
cv2.imshow('orig',original)
cv2.waitKey(0)
cv2.destroyAllWindows()


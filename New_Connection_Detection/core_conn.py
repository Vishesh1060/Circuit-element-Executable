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
import Core_Conn_Support as Ccs
from modelcsv import csvparse

#from jsformat import jsout



(imgData,i,j)=({},-1,-1)
jsout_dir='../out_json/'
imdir="../MLv2/imgs/"
csvpath="../Mlv2/out_imgs/"

Limgs=os.listdir(imdir)
Limgs=Limgs[15:]

trialdivide,i,Limgdata=[],0,[]
for imgadd in Limgs:
    print(csvpath+imgadd[:-4]+'.csv')
    try:
        Limgdata.append(csvparse(csvpath+imgadd[:-4]+'.csv'))
    except FileNotFoundError as f:
        print(f)
        continue
    if i==100:
        break
    else:
        i+=1        
    img = cv2.imread(imdir+imgadd)
#    img,(rw,ry)=Ih.new_image_resize(img,width=800)
    original=img.copy()
    trialdivide.append(Ccs.imgblurdivide(img))

for i in range(len(trialdivide)):
    im_gray = cv2.cvtColor(trialdivide[i], cv2.COLOR_BGR2GRAY)
    (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    trialdivide[i]=Ccs.imgremove_all(im_bw,Limgdata[i])
    trialdivide[i]=Ih.image_label_all(trialdivide[i],Limgdata[i])
    cv2.imwrite(str(i)+Limgs[i],im_bw)
#img=imgremove_all(img, imgData)

#hmiss,frd=imghitmisslinefilter(img)

#blurd=imgblurdivide(original)

img2=None
#img.copy()
c,cdash=None,None
#imagediv(imgData)

cropped=[]
#height,width,_=img2.shape
#cdash.append(width)


'''
print("Image Split X-Coordinates:")
for indx,val in enumerate(cdash):
    if indx==0:
        crpd=img2[0:height,0:val]
        print((0,val),end='')
    else:
        crpd=img2[0:height,cdash[indx-1]:val]
        print((cdash[indx-1],val),end='')
    
    cropped.append(crpd)
 '''   
i=0
for crpimgs in cropped:    
    i+=1
#    cv2.imshow('crps'+str(i),crpimgs)
#    det1=linedtn(crpimgs)
 #   cv2.imshow('crpsline'+str(i),det1)
    
#img=Ih.image_label_all(img, imgData)
#cv2.imshow('img',img)
#cv2.imshow('img2',img2)
#cv2.imshow('orig',original)
cv2.waitKey(0)
cv2.destroyAllWindows()


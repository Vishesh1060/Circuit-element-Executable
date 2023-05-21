import cv2  
import numpy as np
import csv
import os
import json
import Image_handler as Ih
from jsformat import jsout
from modelcsv import csvparse


imgData=csvparse('../Mlv2/out_imgs/sv_ (73).csv')

crdntes=imgData['rectangle_top_left'].copy()
crd=sorted(crdntes)
print(crd)



def image_assign_gateid(imgData,crd):
    Gates=[]
    Types={}
    for i in range(len(imgData['element_name'])):
        if imgData['element_id'][i][0]=='G':
            Gates.append(imgData['element_id'][i])
            Types.update({imgData['element_id'][i]:{"type":imgData['element_name'][i],"in":2,"out":1}})
        else:
            pass
    return (Gates,Types)


def findmincrop(img,imgData):
    global crdntes
    mincrd=crdntes[0][0]
    indexmin=0
    for i in range(len(crdntes)):
        if(crdntes[i][0]<mincrd):
            mincrd=crdntes[i][0]
            indexmin=i   
    crdntes.pop(indexmin)        
    return indexmin 

origid=imgData['element_id']
newid=image_assign_gateid(imgData,crd)
         
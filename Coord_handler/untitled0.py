# -*- coding: utf-8 -*-
"""
Created on Fri May  5 17:39:24 2023

@author: vishe
"""

import Image_handler as Ih
import cv2
import numpy as np
import os
from modelcsv import csvparse


ldir=os.listdir()
ltemp=[]


imdir='C:/Users/vishe.IDEAPADFLEX/Desktop/MiniProject/research paper/Vishesh/images/Dataset image steps/2sv_ (73).jpg'
csvpath="C:/Users/vishe.IDEAPADFLEX/Desktop/MiniProject_final/Circuit-element-Executable/MLv2/out_imgs/sv_ (73).csv"
imgData=csvparse(csvpath)
print(imgData)

img=cv2.imread(imdir)
img=Ih.image_resize(img,width=890)

img2=Ih.image_label_all(img, imgData)

print('\n\n-----\t-----\n\n',imgData)
cv2.imwrite('out.png',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

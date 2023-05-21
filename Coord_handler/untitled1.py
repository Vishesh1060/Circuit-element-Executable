# -*- coding: utf-8 -*-
"""
Created on Fri May  5 19:23:57 2023

@author: vishe
"""
import Image_handler as Ih
import cv2
import numpy as np
import os


def image_mdnfilter(img):
    img_filtered = cv2.medianBlur(img,5)
    return img_filtered

def image_sharpen(img,magnitude=10,threshold=0):

    # Apply a Gaussian blur with a kernel and a sigma of 1.0
    img_blurred = cv2.GaussianBlur(img, (7,17), 200.0)
    kernel = np.array ( [ [-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    img_sharpened2 = cv2.filter2D (img, -1, kernel)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    
    cv2.imshow('shar',img_blurred)
    morph = cv2.morphologyEx(img_sharpened2, cv2.MORPH_CLOSE, kernel)   
    
#    morph = cv2.morphologyEx(img_erode, cv2.MORPH_CLOSE, kernel)
    
    # Display the original and sharpened images
    return morph

img = cv2.imread("C:/Users/vishe.IDEAPADFLEX/Desktop/MiniProject_final/MLv2/in_imgs/sv_ (113).jpg")
img=Ih.image_resize(img,width=900)
img=Ih.image_remove_background(img, imgData=None)

img=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

img_filtered=image_mdnfilter(img)
morph=image_sharpen(img_filtered)

(lower,upper) = (np.array([95,95,100]),np.array([255,255,255]))
thresh = cv2.inRange(img, lower, upper)
    
cv2.imshow('thresh',thresh)


cv2.imshow("Filtered", img_filtered)
cv2.imshow("Original", img)
cv2.imshow("morph", morph)

#cv2.imwrite('Mini circuit _20b.jpg',thresh)

# Wait for a key press to exit
cv2.waitKey(0)

# Destroy all windows
cv2.destroyAllWindows()
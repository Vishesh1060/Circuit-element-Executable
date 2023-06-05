# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 22:25:58 2023

@author: vishe
"""

import cv2,os
import Image_handler as Ih
import numpy as np
from modelcsv import csvparse
import Core_Conn_Support as ccs

csvpath="../MLv2/out_imgs/sv_ (41).csv"
imdir="../MLv2/imgs/"
Limgs=os.listdir(imdir)

imgData=csvparse(csvpath)
img = cv2.imread(imdir+Limgs[28])
img,(rw,ry) = Ih.new_image_resize(img,width=890)
print(imdir+Limgs[28])


def hllineprinter(img,lines):
    for line in lines:
        # Get the parameters of the line
        rho, theta = line[0]
        # Convert to Cartesian coordinates
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        # Get two points on the line
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        # Draw the line on the image
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    return img

def hlplineprinter(img,lines):
    for line in lines:
        # Get the endpoints of the line
        x1, y1, x2, y2 = line[0]
        # Draw the line on the image
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    return img

def hlplinedetector(img):
    mLL=70
    while(True):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply Canny edge detection
        edges = cv2.Canny(gray, 50, 150)
        # Apply Probabilistic Hough Line Transform with a lower threshold value
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=mLL)
        if lines == None:
            mLL-=20
        else: 
            break
    return lines
    
def hllinedetector(img):
    edges = cv2.Canny(img, 50, 150)
    lines = cv2.HoughLines(edges, 1, np.pi/30, 50)
    return lines

i=0
def contourlinedetector(img):
    global i
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
    blur = cv2.GaussianBlur(gray, (11, 11), 0)

    # Apply Otsu's thresholding to binarize the image
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Apply morphological opening to remove small objects or noise
    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    
    edges = cv2.Canny(opening, 149, 150)
    i+=1
    cv2.imshow('edge'+str(i),edges)
    cv2.waitKey(1)
    # Find the contours of the edges
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # Create an empty list to store the bounding boxes
    boxes = []
    # Loop through the contours
    try:
        for cnt,hry in zip(contours, hierarchy[0]):
            # Approximate the contour with a polygon
            epsilon = 0.01 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, False)
            # Check if the polygon has four vertices and is convex
            if len(approx) >= 4 or cv2.isContourConvex(approx):
               if hry[2]==-1:
                    print(hry)
                    x, y, w, h = cv2.boundingRect(cnt)
                    boxes.append(((x, y), (x + w, y + h)))
    except TypeError as te:
        print(te)
    return boxes

def contourlineprinter(img,boxes):
    for box in boxes:
        # Get the top left and bottom right coordinates of the box
        top_left, bottom_right = box
        # Draw a green rectangle on the image
        cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
    return img

'''
i=0
for elem in imgData['element_id']:
    img=Ih.image_remove_element(img, imgData,elem,i)
    i+=1
'''



img=ccs.imgblurdivide(img)

for elem in imgData['element_id']:
    if elem.startswith('G') or elem.startswith('M'):
        img=ccs.replace_with_white(img, imgData, elem)
        

#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

divcoords,croplist=ccs.imagediv(imgData)

imdiv=[]
imdiv2=[]
imdiv3=[]

for val in croplist:
    _,height,_=img.shape
    print(val)
    imdiv.append(img[0:height,val[0]:val[1]])
'''
for indx,im in enumerate(imdiv):
    lines=hllinedetector(im.copy())
    imdiv[indx]=hllineprinter(im.copy(), lines)

for indx,im in enumerate(imdiv):
    lines2=hlplinedetector(im.copy())
    imdiv2.append(hlplineprinter(im.copy(), lines2))
'''
for indx,im in enumerate(imdiv):
    boxes=contourlinedetector(im.copy())
    imdiv3.append(contourlineprinter(im.copy(), boxes))


# for indx,im in enumerate(imdiv):
#     cv2.imshow('im'+str(indx),im)

for indx,im in enumerate(imdiv3):
    cv2.imshow('imdiv3'+str(indx),im)
img=Ih.image_label_all(img, imgData)
cv2.imshow('image',img)


cv2.waitKey(0)
cv2.destroyAllWindows()

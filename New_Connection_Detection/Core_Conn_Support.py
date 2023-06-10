# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 20:11:44 2023

@author: vishe
"""
import cv2  
import numpy as np
import csv
import os
import time
import json
import Image_handler as Ih
from modelcsv import csvparse

#from Image_handler import resize,r,rw,ry as resize,r,rw,ry
i=0

def ihimgremove_all(img,imgData):
    for idx,elemid in enumerate(imgData['element_id']):
        print(idx,'Removing',elemid,imgData['element_name'][idx])
        if idx>=1:
            ## remove this condition
            img=Ih.image_remove_element(img, imgData, elemid)
        else:
            img=Ih.image_remove_element(img, imgData, elemid,mflag=1)
    return img

def imgremove_all(img,imgData):
    for idx,elemid in enumerate(imgData['element_id']):
        print(idx,'Removing',elemid,imgData['element_name'][idx])
        if idx>=1:
            ## remove this condition
            img=New_image_remove_element(img, imgData, elemid)
        else:
            img=New_image_remove_element(img, imgData, elemid)
    return img

def replace_with_white(img,imgData,element_id):
    (resize,rw,ry,lower,upper)=Ih.globalserve()
    index=0
    #global imgData
    for indx,elem in enumerate(imgData['element_id']):
        if(elem==element_id):
            index=indx
            break
    if(not resize):
        (x,y)=imgData['rectangle_top_left'][index]
        top_left=(int(x)+10,int(y)+1)
        top_left = imgData['rectangle_top_left'][index]
        
        (x,y) = imgData['rectangle_bottom_right'][index]
        #bottom_right=(int(x)-15,int(y)-15)
        bottom_right=(int(x),int(y))
        bottom_right = imgData['rectangle_bottom_right'][index]
    else:
        (x,y)=imgData['rectangle_top_left'][index]
        (x,y)=(rw*x,ry*y)
        top_left=(int(x),int(y))        
        (x,y) = imgData['rectangle_bottom_right'][index]
        (x,y)=(rw*x,ry*y)
        bottom_right=(int(x),int(y))

    # Get the coordinates of the top left and bottom right corners
    x1, y1 = top_left
    x2, y2 = bottom_right
    # Get the shape of the image
    height, width, channels = img.shape
    # Check if the coordinates are valid
    if x1 < 0 or x1 > width or x2 < 0 or x2 > width or y1 < 0 or y1 > height or y2 < 0 or y2 > height:
        print("Invalid coordinates")
        return img
    # Create a white image with the same shape as the original image
    white = np.ones_like(img) * 255
    # Copy the white image to the rectangular area in the original image
    img[y1:y2, x1:x2] = white[y1:y2, x1:x2]
    # Return the modified image
    return img

def New_image_remove_element(im3,imgData,element_id,mflag=0):
    index=0
    #global imgData
    (resize,rw,ry,lower,upper)=Ih.globalserve()

    for indx,elem in enumerate(imgData['element_id']):
        if(elem==element_id):
            index=indx
            break
    if(not resize):
        (x,y)=imgData['rectangle_top_left'][index]
        top_left=(int(x)+5,int(y)+1)
        top_left = imgData['rectangle_top_left'][index]
        
        (x,y) = imgData['rectangle_bottom_right'][index]
        bottom_right=(int(x)-10,int(y)-10) 
        bottom_right = imgData['rectangle_bottom_right'][index]
    else:
        (x,y)=imgData['rectangle_top_left'][index]
        (x,y)=(rw*x,ry*y)
        top_left=(int(x),int(y))        
        (x,y) = imgData['rectangle_bottom_right'][index]
        (x,y)=(rw*x,ry*y)
        bottom_right=(int(x),int(y))  
            
#    gray = cv2.cvtColor(im3, cv2.COLOR_BGR2GRAY)
    cropped = im3[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

    try:
        (h,w)=cropped.shape
    except Exception as e:
        print(e,end='')
        (h,w,_)=cropped.shape
    
    _, mask = cv2.threshold(cropped, 140, 255, cv2.THRESH_BINARY)
    mask=np.zeros((h,w),dtype=np.uint8)
#    cv2.imshow('mask2',mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
#    cv2.imshow('mask', mask)   

    offset_contours = []
    for cnt in contours:
        offset_cnt = cnt + top_left # add top left coordinates to each contour point    
        offset_contours.append(offset_cnt)
        
    global i
    cv2.imwrite('mask/mask1'+str(i)+'.png',mask)
    i+=1
#    im3dash=cv2.cvtColor(im3, cv2.COLOR_RGB2GRAY)
    try:    
        thresh_rgb = cv2.cvtColor(im3, cv2.COLOR_GRAY2RGB)
    except Exception as e:
        print(e,end='')
        thresh_rgb=im3.copy

    cv2.drawContours(thresh_rgb, offset_contours, -1, (255,255,255), 10)
    cv2.fillPoly(thresh_rgb, offset_contours, (255, 255, 255))
    cropped = thresh_rgb[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    
    return thresh_rgb

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
    (resize,rw,ry,lower,upper)=Ih.globalserve()
    if resize==False:
        rw,ry=1,1
    width=int(rw*imgData['img_width'][0])
    
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
    
    croplist=[]
    for indx,val in enumerate(divcoords):
        xval=int(val)
        if indx==0:
            croplist.append((0,xval))
        else:
    #        print(cropped[indx-1])
            croplist.append((croplist[indx-1][1],xval))
    croplist.append((croplist[indx][1],width))
#    print("--",xaxs)
#    print("-+",divcoords)
    return divcoords,croplist


#converts box coordinates from split images to combined, requires a parent list of all boxes lists for the split images
def imagedivcombine(Lboxes,croplist,imgData):
    (resize,rw,ry,lower,upper)=Ih.globalserve()
    linedata={
        'clistgrp':[],
        'cboxes':[]
        }
    
    if resize==False:
        rw,ry=1,1
    width=int(rw*imgData['img_width'][0])
    for indx,clist in enumerate(croplist):
        for val in Lboxes[indx]:
            tl,tlx=val[0],val[0][0]
            br,brx=val[1],val[1][0]
#            print("clist",clist[indx],coord,"--")
            tl=(tlx+clist[0],tl[1])
            br=(brx+clist[0],br[1])
            coord=(tl,br)
            linedata['clistgrp'].append(indx)
            linedata['cboxes'].append(coord)
#    print(linedata)
    return linedata
        
    

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

def templabeldivision(c,cdash):
    global img,img2
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

def imgblurdivide(image):
    global imgData
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)    
    blur = cv2.GaussianBlur(gray, (17, 17),sigmaX=33, sigmaY=33)
    divide = cv2.divide(gray, blur, scale=255)
    divide= cv2.cvtColor(divide, cv2.COLOR_GRAY2BGR)
    cv2.imshow('Divide', divide)
    return divide
    
def imghitmisslinefilter(image):
    img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    kernel_h = np.array([[-1, -1, -1,-1],
                     [1, 1, 1,1],
                     [-1, -1, -1,-1]], np.uint8)
    kernel_v = np.array([[-1, 1, -1],
                         [-1, 1, -1],
                         [-1, 1, -1],
                         [-1, 1, -1]], np.uint8)
    img = cv2.GaussianBlur(img, (5,5), 2)
    
    structure=np.ones((2,8),np.uint8)
    img=cv2.erode(img,structure,iterations=1)
    hitmiss_h = cv2.morphologyEx(img, cv2.MORPH_HITMISS, kernel_h)
    img=cv2.dilate(img,structure,iterations=1)
    
    structure=np.ones((8,2),np.uint8)
    img=cv2.erode(img,structure,iterations=1)
    hitmiss_v = cv2.morphologyEx(img, cv2.MORPH_HITMISS, kernel_v)
    img=cv2.dilate(img,structure,iterations=1)
    
    hitmiss = cv2.bitwise_or(hitmiss_h, hitmiss_v)
    
    
    
    kernel_n = np.ones((5, 5), np.uint8)

    # Apply opening and closing to remove noise
    opening = cv2.morphologyEx(hitmiss, cv2.MORPH_OPEN, kernel_n)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel_n)
    
    return hitmiss,closing

i=0
def hlplinedetector(img):
    global i
    mLL=0
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
    blur = cv2.GaussianBlur(gray, (11, 11), 0)

    # Apply Otsu's thresholding to binarize the image
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Apply morphological opening to remove small objects or noise
    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    
    edges = cv2.Canny(opening, 149, 150)
#    cv2.imshow('edge'+str(i),edges)
    i+=1
    cv2.waitKey(1)
    # Apply Probabilistic Hough Line Transform with a lower threshold value
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=mLL)
    return lines
    
def hllinedetector(img):
    edges = cv2.Canny(img, 50, 150)
    lines = cv2.HoughLines(edges, 1, np.pi/30, 50)
    return lines

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
    try:
        for line in lines:
            # Get the endpoints of the line
            x1, y1, x2, y2 = line[0]
            # Draw the line on the image
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    except TypeError as te:
        print(te)
    return img

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
                    x, y, w, h = cv2.boundingRect(cnt)
                    boxes.append(((x, y), (x + w, y + h)))
    except TypeError as te:
        print(te)
    return boxes

def contourlineprinter(img,boxes,linelabel=False):
    linlist,i=[],0
    for box in boxes:
        i+=1
        # Get the top left and bottom right coordinates of the box
        top_left, bottom_right = box
        # Draw a green rectangle on the image
        cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
        if linelabel==True:
            cv2.putText(img,'l'+str(i),top_left, cv2.FONT_HERSHEY_DUPLEX, 0.8,(162,52, 252), 1)
            linlist.append('l'+str(i))
    if linelabel==True:
        return img,linlist
    else:
        return img

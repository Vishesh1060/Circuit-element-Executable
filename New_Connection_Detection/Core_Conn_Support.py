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
    global rw
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
#    print("--",xaxs)
#    print("-+",divcoords)
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
#    cv2.imshow('Divide', divide)
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
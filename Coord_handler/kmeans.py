import cv2  
import numpy as np
import os
import csv

for L in file:
    i+=1
    if i==0:
        for key in L:
            if key not in imgData:
                imgData[key]=[]
    else:
        j=-1        
        kl=list(imgData.keys())
        for value in L:
            j+=1
            if value.isnumeric():
                imgData[kl[j]].append(int(value))
            elif kl[j]=="rectangle_top_left" or kl[j]=="rectangle_bottom_right":
                strval=value.strip("()").split(',')
                inttupval=(int(strval[0]),int(strval[1]))
                imgData[kl[j]].append(inttupval)
            else:
                imgData[kl[j]].append(value)

def image_resize(image, width = None, height = None):
    inter = cv2.INTER_AREA
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    resized = cv2.resize(image, dim, interpolation = inter)
    return resized

files=os.listdir('..\MLv2\imgs')
filelist=[]

for x in files:
    if(x.endswith('.jpg')):
        filelist.append(x)

im3=cv2.imread('../MLv2/imgs/'+x)
im3=image_resize(im3,width=1000)
pixels = np.float32(im3.reshape(-1, 3))
n_colors = 5

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .9)
flags = cv2.KMEANS_RANDOM_CENTERS
_, labels, apalette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
_, acounts = np.unique(labels, return_counts=True)
dominant = apalette[np.argmax(acounts)]
foreground = apalette[np.argmin(acounts)]
#[120,120,120] 200 200 250
avalues=[]
for i in range(len(dominant)):
    dominant[i]-=22
    avalues.append(int(round(dominant[i])))
(r,g,b)=avalues
lower = np.array([r,g,b])
upper = np.array([255,255,255])

thresh = cv2.inRange(im3, lower, upper)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

gray = cv2.cvtColor(im3, cv2.COLOR_BGR2GRAY)
cropped = gray[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
_, mask = cv2.threshold(cropped, 127, 255, cv2.THRESH_BINARY)




cv2.imshow('original', im3)   
cv2.imshow('thresh', thresh)
cv2.imshow('morph', thresh)
cv2.waitKey()
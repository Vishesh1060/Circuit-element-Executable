import cv2  
import numpy as np
import os
import csv

(imgData,i,j,file)=({},-1,-1,csv.reader(open('../Mlv2/out_imgs/sv_ (73).csv','r')))

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

def image_dominant_color(im3,n_colors=5):
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
    bvalues=[]
    for i in range(len(dominant)):
        if (n_colors>2):
            dominant[i]-=22
        avalues.append(int(round(dominant[i])))
    (r,g,b)=avalues
    
    for i in range(len(foreground)):
        bvalues.append(int(round(foreground[i])))
    
    if (n_colors>2):
        (r2,g2,b2)=(255,255,255)
    else:
        (r2,g2,b2)=bvalues
    lower = np.array([r,g,b])
    upper = np.array([r2,g2,b2])
    return (lower,upper)


def image_remove_element(im3,element_id):
    index=0
    global imgData
    for indx,elem in imgData['element_id']:
        if(elem==element_id):
            index=indx
    
    top_left = imgData['rectangle_top_left'][index]
    bottom_right = imgData['rectangle_bottom_right'][index]
            
    (lower,upper)=image_dominant_color(im3)
    thresh = cv2.inRange(im3, lower, upper)
    #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))
    #morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    gray = cv2.cvtColor(im3, cv2.COLOR_BGR2GRAY)
    cropped = gray[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    
    _, mask = cv2.threshold(cropped, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.imshow('mask', mask)   
    
    offset_contours = []
    for cnt in contours:
        offset_cnt = cnt + top_left # add top left coordinates to each contour point    
        offset_contours.append(offset_cnt)
    
    thresh_rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)
    
    cv2.drawContours(thresh_rgb, offset_contours, -1, (255,255,255), 20)
    #cv2.fillPoly(thresh_rgb, offset_contours, (255, 255, 255))
    cropped = thresh_rgb[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    
    return thresh_rgb

files=os.listdir('..\MLv2\imgs')
filelist=[]

for x in files:
    if(x.endswith('.jpg')):
        filelist.append(x)

im3=cv2.imread('../Mlv2/imgs/sv_ (73).jpg')
im3=image_resize(im3,width=1000)

#cv2.imshow('original', im3)   
#cv2.imshow('thresh', thresh)
#cv2.imshow('cropped', cropped)
#cv2.imshow('final',thresh_rgb)
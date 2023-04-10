import cv2  
import numpy as np
import functools

def image_label_all(image,imgData):
    for i in range(len(imgData['rectangle_top_left'])):
        cv2.rectangle(image,imgData['rectangle_top_left'][i],imgData['rectangle_bottom_right'][i], (int(255-i*10),0+i*10,10*i), 2)
        cv2.putText(image,imgData['element_id'][i],imgData['rectangle_top_left'][i], cv2.FONT_HERSHEY_DUPLEX, 0.8,(162,252, 252), 1)
    return image

#Aspect ratio conserving resize function 
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

#Calculates the percentage overlap between two rectangles.
##Function checking for all elements in one image
def image_percent_overlap(imgData):
    Overlap={(1,2):''}
    for i in range(len(imgData['rectangle_top_left'])):
        for j in range(len(imgData['rectangle_top_left'])):
            if(i==j):
                pass
            else:
                percentval=percent_overlap(imgData['rectangle_top_left'][i],imgData['rectangle_bottom_right'][i],imgData['rectangle_top_left'][j],imgData['rectangle_bottom_right'][j])
                if percentval!=0.0:
                    Overlap.update({(imgData['element_id'][i],imgData['element_id'][j]):percentval})
                    

#Returns a tuple containing two values: (Most Dominant color, Least Dominant color)
## Can be summarised as, returns (background color, foreground color) 
### Very compute heavy, using memoization to reduce memory cost
(lower,upper)=(None,None)        
def image_dominant_color(image,n_colors=5,mflag=0):
    global lower
    global upper
    im3=image
    if mflag:
        if lower is not None and upper is not None:
            return (lower,upper)
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

"""
RecTL1: Top-left and bottom-right corners of the first rectangle (x1,y1,x2,y2)
rect2 (tuple): Top-left and bottom-right corners of the second rectangle (x1,y1,x2,y2)
"""   
 
def percent_overlap(RecTL1,RecBR1,RecTL2,RecBR2):
    rect1=(RecTL1+RecBR1)
    rect2=(RecTL2+RecBR2)
    x_overlap = max(0, min(rect1[2], rect2[2]) - max(rect1[0], rect2[0]))
    y_overlap = max(0, min(rect1[3], rect2[3]) - max(rect1[1], rect2[1]))
    intersection_area = x_overlap * y_overlap
    rect1_area = (rect1[2] - rect1[0]) * (rect1[3] - rect1[1])
    rect2_area = (rect2[2] - rect2[0]) * (rect2[3] - rect2[1])
    total_area = rect1_area + rect2_area - intersection_area
    if total_area == 0:
        return 0.0
    else:
        return float(intersection_area) / float(total_area) * 100

# Removes element by given id, returns the image 
# Input parameters: image,imagedata,element id (given by the form G0 or M1 etc), and
# Memoization flag, set to 1 if repeating multiple times (such as in a loop) to reduce compute cost   
def image_remove_element(im3,imgData,element_id,mflag=0):
    index=0
    #global imgData
    for indx,elem in enumerate(imgData['element_id']):
        if(elem==element_id):
            index=indx
            break
    
    top_left = imgData['rectangle_top_left'][index]
    bottom_right = imgData['rectangle_bottom_right'][index]
            
    (lower,upper)=image_dominant_color(im3,mflag=mflag)
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
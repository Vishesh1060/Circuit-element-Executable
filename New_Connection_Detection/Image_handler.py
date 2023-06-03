import cv2  
import numpy as np
import functools

resize,rw,ry=False,1,1
(lower,upper)=(None,None) 

#for cross module compatibility and extension
def globalserve():
    global resize,rw,ry
    global lower,upper
    return (resize,rw,ry,lower,upper)
    
def image_label_all(image,imgData):
    global resize,rw,ry
    if(not resize):
        for i in range(len(imgData['rectangle_top_left'])):
            cv2.rectangle(image,imgData['rectangle_top_left'][i],imgData['rectangle_bottom_right'][i], (int(155-i*10),100+i*10,10*i), 2)
            cv2.putText(image,imgData['element_id'][i],imgData['rectangle_top_left'][i], cv2.FONT_HERSHEY_DUPLEX, 0.8,(162,252, 252), 1)
    else:
        for i in range(len(imgData['rectangle_top_left'])):
            (x,y)=imgData['rectangle_top_left'][i]
            (x,y)=(rw*x,ry*y)
            c1=(int(x),int(y))
            (x,y)=imgData['rectangle_bottom_right'][i]
            (x,y)=(rw*x,ry*y)
            c2=(int(x),int(y))
            cv2.rectangle(image,c1,c2, (int(155-i*10),100+i*10,50*i), 2)
            cv2.putText(image,imgData['element_id'][i],c1, cv2.FONT_HERSHEY_DUPLEX, 0.8,(162,252, 252), 1)
    return image

#Aspect ratio conserving resize function 
##Use the new version for image aware resizing with no errors
def image_resize(image, width = None, height = None):
    global resize,r
    resize=False
    inter = cv2.INTER_AREA
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r2 = height / float(h)
        dim = (int(w * r2), height)
    else:
        r2 = width / float(w)
        dim = (width, int(h * r2))
    r=r2
    resized = cv2.resize(image, dim, interpolation = inter)
    return resized

def new_image_resize(image, width = None, height = None):
    global resize,rw,ry
    resize=True
    inter = cv2.INTER_AREA
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        ry1 = height / float(h)
        dim = (int(w * ry1), height)

        rw = dim[0] / float(w)
        ry = ry1
    else:
        rw1 = width / float(w)
        dim = (width, int(h * rw1))
        
        ry = dim[1] / float(h)
        rw = rw1

    resized = cv2.resize(image, dim, interpolation = inter)
    return resized,(rw,ry)


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
def overlap(rect1, rect2):
    # unpack the coordinates of the rectangles
    x1, y1, x2, y2 = rect1 # top left and bottom right of the first rectangle
    x3, y3, x4, y4 = rect2 # top left and bottom right of the second rectangle

    # calculate the area of the rectangles
    area1 = (x2 - x1) * (y2 - y1)
    area2 = (x4 - x3) * (y4 - y3)

    # calculate the intersection of the rectangles
    x5 = max(x1, x3) # left edge of the intersection
    y5 = max(y1, y3) # top edge of the intersection
    x6 = min(x2, x4) # right edge of the intersection
    y6 = min(y2, y4) # bottom edge of the intersection

    # check if the rectangles overlap
    if x5 < x6 and y5 < y6:
        # calculate the area of the intersection
        area3 = (x6 - x5) * (y6 - y5)

        # calculate the percent overlap
        percent = (area3 / (area1 + area2 - area3)) * 100

        # return the percent overlap
        return percent
    else:
        # return zero if there is no overlap
        return 0

def image_remove_background(im3,imgData,mflag=0):
#   Does not really need a parsed imgData file, set imgData to 0 if running in such a situation
    (lower,upper)=image_dominant_color(im3,mflag=mflag)   
#    lower=np.array([105,106,110])
    print(lower,upper)
    thresh = cv2.inRange(im3, lower, upper)
    return thresh


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
            
    (lower,upper)=image_dominant_color(im3,mflag=mflag)   
#    lower=np.array([110,113,118])
    thresh = cv2.inRange(im3, lower, upper)
    #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))
    #morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    gray = cv2.cvtColor(im3, cv2.COLOR_BGR2GRAY)
    cropped = gray[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    
    _, mask = cv2.threshold(cropped, 140, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
#    cv2.imshow('mask', mask)   
    offset_contours = []
    for cnt in contours:
        offset_cnt = cnt + top_left # add top left coordinates to each contour point    
        offset_contours.append(offset_cnt)
    
    thresh_rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)
    
    cv2.drawContours(thresh_rgb, offset_contours, -1, (255,255,255), 10)
    #cv2.fillPoly(thresh_rgb, offset_contours, (255, 255, 255))
    cropped = thresh_rgb[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    
    return thresh_rgb

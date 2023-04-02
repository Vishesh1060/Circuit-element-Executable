import cv2  
import numpy as np
import csv
import os

(imgData,i,j,file)=({},-1,-1,csv.reader(open('../Mlv2/out_imgs/sv_ (73).csv','r')))

jsout={
    "Jinja": {
        "template": ""
    },
    "generic_present": False,
    "entity_name": "entity",
    "LRGates": {
        "G1": ["i1","i2"],
        "G2": ["i3","i4"],
        "G3": ["G1","G2"]
    },
    "Gates": ["G1","G2","G3"],
    "types": {
        "G1": {
            "type": "AND",
            "in": 2,
            "out": 1
        },
        "G2": {
            "type": "AND",
            "in": 2,
            "out": 1
        },
        "G3": {
            "type": "OR",
            "in": 2,
            "out": 1
        }
    },
    "Terminals": {
        "in": 4,
        "out": 1
    },
    "Link": {}
}


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

#CSV parser
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
                
#key values are ['img_height', 'img_width', 'img_channels', 'element_name', 'confidence', 'rectangle_top_left', 'rectangle_bottom_right']
##includes Code for converting string in csv to int

#Gate Labeler
def image_assign_gateid(imgData):
    Gates=[]
    Types={}
    for i in range(len(imgData['element_name'])):
        if imgData['element_id'][i][0]=='G':
            Gates.append(imgData['element_id'][i])
            Types.update({imgData['element_id'][i]:{"type":imgData['element_name'][i],"in":-1,"out":-1}})
        else:
            pass
    return (Gates,Types)


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



blank_image = np.zeros((imgData['img_height'][0],imgData['img_width'][0],imgData['img_channels'][0]), dtype=np.uint8)
im2=cv2.imread('../Mlv2/out_imgs/sv_ (73).png')
im3=cv2.imread('../MLv2/imgs/sv_ (73).jpg')

#resizing for visibility
blank_image = image_resize(blank_image, width=1000)
im2 = image_resize(im2, width=1000)
im3 = image_resize(im3, width=1000)
(Gates,Types)=image_assign_gateid(imgData)
image_percent_overlap(imgData)


for i in range(len(imgData['rectangle_top_left'])):
    cv2.rectangle(blank_image,imgData['rectangle_top_left'][i],imgData['rectangle_bottom_right'][i], (int(255-i*10),0+i*10,10*i), 2)
    cv2.putText(blank_image,imgData['element_id'][i],imgData['rectangle_top_left'][i], cv2.FONT_HERSHEY_DUPLEX, 0.8,(162,252, 252), 1)

#cv2.imshow('window',blank_image)
#cv2.imshow('window2',im2)


(w, h) = (imgData['img_width'][0],imgData['img_height'][0])


# Define the bounding box coordinates (top left and bottom right)
(x1, y1) = imgData['rectangle_top_left'][1] # Top left
(x2, y2) = imgData['rectangle_bottom_right'][1] # Bottom right


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
cv2.imshow('thresh', thresh)
cv2.imshow('morph', thresh)


# Show the result
#cv2.imshow("Result", im2)
cv2.waitKey()


#json_object = json.dumps(dictionary, indent=4)
#with open("sample.json", "w") as outfile:
#   outfile.write(json_object)
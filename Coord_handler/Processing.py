import cv2  
import numpy as np
import csv
import os
import json
import Image_handler as Ih
from jsformat import jsout
from modelcsv import csvparse



(imgData,i,j)=({},-1,-1)
jsout_dir='../out_json/'
imdir="../MLv2/imgs/sv_ (73).jpg"
imgData=csvparse('../Mlv2/out_imgs/sv_ (73).csv')
img = cv2.imread(imdir)
                
#key values are ['img_height', 'img_width', 'img_channels', 'element_name', 'confidence', 'rectangle_top_left', 'rectangle_bottom_right']
##includes Code for converting string in csv to int

img = cv2.imread(imdir)
img2 = cv2.imread(imdir)

img=Ih.image_resize(img,width=879)
img2=Ih.image_resize(img,width=879)
height,width,_=img2.shape
mcnt=0
cv2.imshow("original",img)

for elem in imgData['element_id']:
    if mcnt==0:
        img=Ih.image_remove_element(img, imgData,elem)
        mcnt=1      
    else:
        img=Ih.image_remove_element(img, imgData,elem,mcnt)

cv2.imshow('removedelements.png',img)
#print(crdntes)
#print(sorted(crdntes))

#cv2.imshow('img2',img)           


#imgData['rectangle_top_left'][indexmin][0]
cropped= img[0:height,0:int(width/3)]

kernel=np.ones((2,4),np.uint8)
structure=np.ones((1,13),np.uint8)

hlines=cv2.dilate(cropped,kernel,iterations=1)


hlines=cv2.erode(hlines,structure,iterations=5)

kernel=np.ones((8,1),np.uint8)
vlines=cv2.erode(cropped,kernel,iterations=1)
vlines=cv2.dilate(vlines,kernel,iterations=1)

cv2.imshow('hlines1',hlines)
#cv2.imshow('vlines',vlines)

#cv2.imshow('original',img2)
gray = cv2.cvtColor(hlines, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

#(lower,upper)=Ih.image_dominant_color(img)
#nobgimg = cv2.inRange(img, lower, upper)
#thresh=cv2.bitwise_not(nobgimg)
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
bounding_boxes = []
lineset1=[]

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

for i in range(len(lineset1)):
    tl1,br1=lineset1[i]
    for j in range(len(lineset1)):
        if i==j:
            continue
        else:
            tl2,br2=lineset1[j]
            percen=Ih.overlap((tl1+br1),(tl2+br2))
            #print("i",i,"j",j,"--",percen,"%")
            if(percen!=0.0):
                pass

# Show the image with bounding boxes
#cv2.imshow("Bounding Boxes",img)
#(x,y)=lineset1[4][0]
#(x2,y2)=lineset1[4][1]
#cv2.rectangle(img2, (x, y), (x2,y2), (0, 255, 0), 2)
#cv2.imshow('thresh',binary)

img2=Ih.image_label_all(img2, imgData)


#indexmin=findmincrop(img2, imgData)
#imgData['rectangle_top_left'][indexmin][0]
####<------------------------------------------------>
cropped= img[0:height,int(width/3):int((2*width)/3)]

structure=np.ones((1,13),np.uint8)
hlines=cv2.erode(cropped,structure,iterations=3)
hlines=cv2.dilate(hlines,kernel,iterations=1)

kernel=np.ones((6,1),np.uint8)
vlines=cv2.erode(cropped,kernel,iterations=1)
#cv2.imshow('vlines2',vlines)

vlines=cv2.dilate(vlines,kernel,iterations=1)

#cv2.imshow('hlines2',hlines)
cv2.imshow('vlines',vlines)

#cv2.imshow('original',img2)

gray = cv2.cvtColor(vlines, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

#(lower,upper)=Ih.image_dominant_color(img)
#nobgimg = cv2.inRange(img, lower, upper)
#thresh=cv2.bitwise_not(nobgimg)
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
bounding_boxes = []


for cnt in contours:
    # Get the bounding rectangle of the contour
    x, y, w, h = cv2.boundingRect(cnt)
    # Append the coordinates to the list
    linetopleft=(x, y)
    linebottomright=(x + w, y + h)
    lineset1.append([linetopleft,linebottomright])
    bounding_boxes.append(((x, y), (x + w, y + h)))
    # Draw the rectangle on the image for visualization
    cv2.rectangle(cropped, (x, y), (x + w, y + h), (0, 255, 0), 2)

for i in range(len(lineset1)):
    tl1,br1=lineset1[i]
    for j in range(len(lineset1)):
        if i==j:
            continue
        else:
            tl2,br2=lineset1[j]
            percen=Ih.overlap((tl1+br1),(tl2+br2))
            #print("i",i,"j",j,"--",percen,"%")
            if(percen!=0.0):
                pass
   
####
cropped= img[0:height,int(2*width/3):int(width)]

kernel=np.ones((1,2),np.uint8)
structure=np.ones((1,13),np.uint8)

hlines=cv2.dilate(cropped,kernel,iterations=2)
hlines=cv2.erode(hlines,structure,iterations=3)


kernel=np.ones((8,1),np.uint8)
vlines=cv2.erode(cropped,kernel,iterations=1)
vlines=cv2.dilate(vlines,kernel,iterations=1)

cv2.imshow('hlines3',hlines)
#cv2.imshow('vlines',vlines)

#cv2.imshow('original',img2)

gray = cv2.cvtColor(hlines, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

#(lower,upper)=Ih.image_dominant_color(img)
#nobgimg = cv2.inRange(img, lower, upper)
#thresh=cv2.bitwise_not(nobgimg)
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
bounding_boxes = []


for cnt in contours:
    # Get the bounding rectangle of the contour
    x, y, w, h = cv2.boundingRect(cnt)
    # Append the coordinates to the list
    linetopleft=(x, y)
    linebottomright=(x + w, y + h)
    lineset1.append([linetopleft,linebottomright])
    bounding_boxes.append(((x, y), (x + w, y + h)))
    print("--",(x, y), (x + w, y + h))
    # Draw the rectangle on the image for visualization
    cv2.rectangle(cropped, (x, y), (x + w, y + h), (0, 255, 0), 2)

for i in range(len(lineset1)):
    tl1,br1=lineset1[i]
    for j in range(len(lineset1)):
        if i==j:
            continue
        else:
            tl2,br2=lineset1[j]
            percen=Ih.overlap((tl1+br1),(tl2+br2))
            #print("i",i,"j",j,"--",percen,"%")
            if(percen!=0.0):
                pass    
# Show the image with bounding boxes
print(bounding_boxes)
img3=cv2.imread(imdir)
(i,j)=(0,-1)
img3=Ih.image_resize(img3,width=879)
for val in lineset1:
    j+=1
    if j==4:
        i+=1
    elif j==6:
        i+=1
    linetopleft=val[0]
    linebottomright=val[1]
        
    linetopleft=(linetopleft[0]+i*width//3,linetopleft[1])
    linebottomright=(linebottomright[0]+i*width//3,linebottomright[1])
    print("=>",linetopleft,linebottomright)
    # Draw the rectangle on the image for visualization
    cv2.rectangle(img3, linetopleft, linebottomright, (0, 255, 0), 2)
    
img3=Ih.image_label_all(img3,imgData)
cv2.imwrite('labelledonoriginalimage.png',img3)

img=Ih.image_label_all(img, imgData)
cv2.imshow("linesdetected.png",img)

'''
(x,y)=lineset1[4][0]
(x2,y2)=lineset1[4][1]
cv2.rectangle(img2, (x, y), (x2,y2), (0, 255, 0), 2)
#cv2.imshow("check",img2)

'''


cv2.waitKey(0)
cv2.destroyAllWindows()



'''
kernel=np.ones((1,8),np.uint8)
hlines=cv2.erode(thresh,kernel,iterations=3)
kernel=np.ones((8,1),np.uint8)
vlines=cv2.erode(thresh,kernel,iterations=3)
'''

# cv2.imshow('vlines',vlines)
# cv2.imshow('hlines',hlines)
#lines=vlines+hlines

#cv2.imshow('lines',lines)

cv2.waitKey()

'''
(Gates,Types)=image_assign_gateid(imgData)
jsout["Types"].update(Types)
jsout["Gates"].extend(Gates)
json_object = json.dumps(jsout, indent=4)
with open(str(jsout_dir+"data.json"), "w") as outfile:
   outfile.write(json_object)
 '''
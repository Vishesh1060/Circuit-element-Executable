# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 16:31:04 2023

@author: vishe
"""
import cv2,os
import Image_handler as Ih
import numpy as np
from modelcsv import csvparse

csvpath="../MLv2/out_imgs/sv_ (16).csv"
imdir="../MLv2/imgs/"
Limgs=os.listdir(imdir)

imgData=csvparse(csvpath)
img = cv2.imread(imdir+Limgs[13])
img,(rw,ry) = Ih.new_image_resize(img,width=890)
cv2.imshow('imgremel',img)
print(imdir+Limgs[13])


i=0
for elem in imgData['element_id']:
    img=Ih.image_remove_element(img, imgData,elem,i)
    i+=1
    


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray, 50, 150)
# Apply HoughLines to detect lines and their parameters
lines = cv2.HoughLines(edges, 1, np.pi/180, 100)

# Define a function to find the intersection point of two lines
def line_intersection(line1, line2):
    # Extract the line parameters
    rho1, theta1 = line1[0]
    rho2, theta2 = line2[0]
    # Calculate the sine and cosine of the angles
    cos1 = np.cos(theta1)
    sin1 = np.sin(theta1)
    cos2 = np.cos(theta2)
    sin2 = np.sin(theta2)
    # Calculate the determinant
    det = cos1 * sin2 - cos2 * sin1
    # Check if the lines are parallel
    if det == 0:
        return None
    # Calculate the intersection point
    x = (sin2 * rho1 - sin1 * rho2) / det
    y = (-cos2 * rho1 + cos1 * rho2) / det
    return (int(x), int(y))

# Define a dictionary to store the connections of each gate
connections = {}
for i in range(1,17):
    connections['gate'+str(i)]=[]

# Loop through all the lines


for i in range(len(lines)):
    # Get the first line
    line1 = lines[i]
    # Get the name of the gate corresponding to this line (you may need to change this according to your data)
    gate1 = 'gate' + str(i+1)
    # Initialize an empty list for this gate's connections
    connections[gate1] = []
    # Get the line parameters
    rho1, theta1 = line1[0]
    # Calculate two points on the line for drawing
    a1 = np.cos(theta1)
    b1 = np.sin(theta1)
    x01 = a1 * rho1
    y01 = b1 * rho1
    x11 = int(x01 + 1000 * (-b1))
    y11 = int(y01 + 1000 * (a1))
    x21 = int(x01 - 1000 * (-b1))
    y21 = int(y01 - 1000 * (a1))
    # Draw the line on the image (optional)
    cv2.line(img, (x11, y11), (x21, y21), (0, 255, 0), 2)
    
    # Loop through all the other lines

    for j in range(i+1, len(lines)):
        # Get the second line
        line2 = lines[j]
        # Get the name of the gate corresponding to this line (you may need to change this according to your data)
        gate2 = 'gate' + str(j+1)
        # Find the intersection point of the two lines
        point = line_intersection(line1, line2)
        # Check if there is an intersection point
        if point is not None:
            # Draw a circle at the intersection point for visualization (optional)
            cv2.circle(img, point, 5, (0, 0, 255), -1)
            # Add the second gate to the first gate's connections list
            connections[gate1].append(gate2)
            # Add the first gate to the second gate's connections list
            connections[gate2].append(gate1)

# Print the connections dictionary
print(connections)

# Show the image with lines and intersection points (optional)
img=Ih.image_label_all(img, imgData)
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

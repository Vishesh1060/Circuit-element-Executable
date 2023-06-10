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

#14,41,15,38
csvpath="../MLv2/out_imgs/sv_ (38).csv"
imdir="../MLv2/imgs/sv_ (38).jpg"
#Limgs=os.listdir(imdir)

imgData=csvparse(csvpath)
img = cv2.imread(imdir)
img,(rw,ry) = Ih.new_image_resize(img,width=890)
print(imdir)

 # Return True if the boxes are intersecting or very close, False otherwise
 # Takes a tuple of top left and bottom right coordinates
 # is gate
def nConnrcgn(e1TlBr,e2TlBr,isGate=False,isline=False,xthreshold=5):
   # unpack the tuples
  (resize,rw,ry,lower,upper)=Ih.globalserve()
  
  (a1,b1),(a2,b2) = e1TlBr # line top left and bottom right coordinates
  (x1,y1),(x2,y2) = e2TlBr # gate (or line) top left and bottom right coordinates
  if resize==True and isGate==True:    
      x1,x2=x1*rw,x2*rw
      y1,y2=y1*ry,y2*ry
  
  flag,conntype=False,None
  # check if the line ends are touching or very near the gate coordinates
  if a2==x1 or abs(a2-x1)<=xthreshold:
      if (b1>=y1 and b1<=y2) or (b2>=y1 and b2<=y2):     
          flag=True
          if isGate==True:
              conntype='Gate_input'
  if a1==x2 or abs(a1-x2)<=xthreshold:
      if b2>=y1 and b2<=y2 or (b1>=y1 and b1<=y2):
          flag=True
          if isGate==True:
              conntype='Gate_output'

  if isGate==True:
      percent_overlap = Ih.percent_overlap((a1,b1), (a2,b2), (x1,y1), (x2,y2))
      
      if int(percent_overlap)>1:
          if flag==False:
#              print('percent_overlap is',int(percent_overlap))
#              print('\nEligible for overlap match\n')
              flag,conntype=True,'Gate_input_Overlap'
      return (flag,conntype)
  return (flag,None)

#checks if the area of a line is too small, discards it if so:
def linevaliditycheck(linedata):
    i,r,arealist=1,0,[]
    cboxes=linedata['cboxes'].copy()
    for TlBr in cboxes:
        (resize,rw,ry,lower,upper)=Ih.globalserve()
        (a1,b1),(a2,b2) = TlBr # line top left and bottom right coordinates
        line_area = ((b2 - b1) * (a2 - a1))
        arealist.append(line_area)
        if line_area<=150:
#            print('l'+str(i),' LArea=',line_area,end=' removed ')
            _=linedata['cboxes'].pop(i-r-1),linedata['clistgrp'].pop(i-r-1)
            r+=1
        i+=1
    
            
    

def Connrcgn(GateTlbr,LineTlbr, threshold=10):
  box1,box2=GateTlbr,LineTlbr
  # Unpack the coordinates
  (x1, y1),(x2, y2) = box1
  (x3, y3),(x4, y4) = box2
  # Calculate the width and height of each box
  w1 = x2 - x1
  h1 = y2 - y1
  w2 = x4 - x3
  h2 = y4 - y3
  # Calculate the center of each box
  cx1 = x1 + w1 / 2
  cy1 = y1 + h1 / 2
  cx2 = x3 + w2 / 2
  cy2 = y3 + h2 / 2
  # Calculate the distance between the centers
  dx,dy = abs(cx1 - cx2),abs(cy1 - cy2)
  condition= dx < (w1 + w2) / 2 + threshold and dy < (h1 + h2) / 2 + threshold
  
  
  # Check if the distance is smaller than the sum of half-widths and half-heights plus the threshold
  return condition


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


for indx,im in enumerate(imdiv):
    boxes=contourlinedetector(im.copy())
    imdiv3.append(contourlineprinter(im.copy(), boxes))
    
imdiv3.append(contourlineprinter(im.copy(), boxes))    
for indx,im in enumerate(imdiv3):
    cv2.imshow('imdiv3'+str(indx),im)

'''
# for indx,im in enumerate(imdiv):
#     cv2.imshow('im'+str(indx),im)

Lboxes=[]
for indx,im in enumerate(imdiv):
    boxes=ccs.contourlinedetector(im.copy())
    Lboxes.append(boxes)

linedata=ccs.imagedivcombine(Lboxes,croplist,imgData)
linevaliditycheck(linedata)

imgout,linlist=ccs.contourlineprinter(img.copy(),linedata['cboxes'],linelabel=True)
imgout=Ih.image_label_all(imgout, imgData)

Ijson={
    "Jinja": {
        "template": ""
    },
    "generic_present": False,
    "entity_name": "entity",
    "LRGates": {},
    "Gates": [],
    "Types": {},
    "Terminals": {
        "in": None,
        "out": None
    },
    "Link": {}
}

for indx,elem in enumerate(imgData['element_id']):
    if elem.startswith('G'):
        Ijson["Gates"].append(elem)
        Ijson["Types"].update({
            elem:{
                "type":imgData["element_name"][indx],
                "in":None,
                "out":1
                }
            })
print(Ijson)       

indivconn={
    'elemid':None,
    'inputs':[],
    'outputs':[]
    }        
groupconn=[]        

for indx0,elem in enumerate(imgData['element_id']):
    if elem.startswith('G'): 
        indivconn={
            'elemid':elem,
            'inputs':[],
            'outputs':[]
            }   
        for indx1,lin in enumerate(linedata['cboxes']):
            gatecrds=(imgData['rectangle_top_left'][indx0],imgData['rectangle_bottom_right'][indx0])
            flag,conntype=nConnrcgn(lin,gatecrds,True)
            if flag:
                if conntype=='Gate_output':
                    indivconn['outputs'].append(linlist[indx1])
                else:
                    indivconn['inputs'].append(linlist[indx1])
                print(linlist[indx1],"is connected to Gate ID: ",elem,'as',conntype)
#                print(linlist[indx1],"is NOT connected to Gate ID: ",elem)
        groupconn.append(indivconn)


def isnotoutputfromgate(lineref,groupconn):
    for val in groupconn:
        if lineref in val['outputs']:
            return False
    return True

grouplineconn=[]
for indx0,lin0 in enumerate(linedata['cboxes']):
    indivlineconn={
        'lineid':linlist[indx0],
        'isinput':False,
        'isoutput':False,
        'conn':[]
        }
    if linedata['clistgrp'][indx0]==min(linedata['clistgrp']):
        indivlineconn['isinput']=True
    if linedata['clistgrp'][indx0]==max(linedata['clistgrp']):
        indivlineconn['isoutput']=True
    for indx1,lin1 in enumerate(linedata['cboxes']):
        if lin0==lin1:
            continue
        flag,_=nConnrcgn(lin0,lin1,isline=True)
        if flag and isnotoutputfromgate(linlist[indx0],groupconn) and indivlineconn['isinput']==False and indivlineconn['isoutput']==False:
            indivlineconn['conn'].append(linlist[indx1])
            print(linlist[indx0],"is connected to line ID: ",linlist[indx1])
    grouplineconn.append(indivlineconn)
        
print('\n\n',grouplineconn)
print('\n\n',groupconn)

img=Ih.image_label_all(img, imgData)

cv2.imshow('image',img)

cv2.imshow('imageout',imgout)



cv2.waitKey(0)
cv2.destroyAllWindows()

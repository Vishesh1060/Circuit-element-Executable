import cv2
import numpy as np
import Image_handler as Ih


img = cv2.imread("sv_ (60).jpg")
img2 = cv2.imread("sv_ (60).jpg")
img=Ih.image_resize(img,width=750)
img2=Ih.image_resize(img2,width=750)

(lower,upper)=Ih.image_dominant_color(img)
thresh = cv2.inRange(img, lower, upper)
thresh=cv2.bitwise_not(thresh)







'''
thresh2 = cv2.inRange(img2, lower, upper)
kernel=np.ones((1,10),np.uint8)
structure=np.ones((1,14),np.uint8)
hlines=cv2.erode(thresh,kernel,iterations=3)
cv2.imshow('erode',hlines)
hlines=cv2.dilate(hlines,structure,iterations=5)
print(thresh.shape)
print(lower,upper)
#cv2.imshow('window1',thresh2)
#cv2.imshow('window3',thresh)
cv2.imshow('dilate',hlines)

#########################################
blank_image = np.zeros((imgData['img_height'][0],imgData['img_width'][0],imgData['img_channels'][0]), dtype=np.uint8)
im2=cv2.imread(imdir)
im3=cv2.imread(imdir)

blank_image = Ih.image_resize(blank_image, width=1000)
blank_image = Ih.image_label_all(blank_image,imgData)
im3 = Ih.image_resize(im3, width=1000)
im2 = Ih.image_resize(im2, width=1000)


Ih.image_percent_overlap(imgData)

(lower,upper)=Ih.image_dominant_color(im3)

#im3=Ih.image_remove_element(im3,imgData,'G0')


im3 = Ih.image_label_all(im3,imgData)

cv2.imshow('window',blank_image)
cv2.imshow('window2',im2)
cv2.imshow('window3',im3)
cv2.waitKey()


'''
cv2.waitKey()
#print(img.shape)

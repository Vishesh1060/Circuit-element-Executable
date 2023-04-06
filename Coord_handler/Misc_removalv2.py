import cv2
import numpy as np
import skimage
from skimage.filters import threshold_otsu
from skimage.morphology import closing, square
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops

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

# Read the image and convert it to grayscale
img = cv2.imread('../MLv2/imgs/sv_ (73).jpg')

img=image_resize(img,width=1000)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# Apply Otsu's thresholding to binarize the image
thresh = threshold_otsu(gray)
binary = gray > thresh

# Apply morphological closing to fill small holes and gaps
closed = closing(binary, square(3))

# Remove the border pixels to avoid false positives
cleared = clear_border(closed)

# Label the connected components and get their properties
label_img = label(cleared)
regions = regionprops(label_img)

# Loop over the regions and filter out the ones that are likely to be text
text_regions = []
for region in regions:
    # Get the bounding box coordinates, area and eccentricity of the region
    minr, minc, maxr, maxc = region.bbox
    area = region.area
    eccentricity = region.eccentricity

    # Compute the aspect ratio and solidity of the region
    height = maxr - minr + 1
    width = maxc - minc + 1
    aspect_ratio = width / height
    solidity = area / (height * width)

    # Apply some heuristic criteria to identify text regions
    if (aspect_ratio > 0.2 and aspect_ratio < 5 and 
        solidity > 0.3 and solidity < 0.9 and 
        area > 100 and area < 10000 and 
        eccentricity > 0.1 and eccentricity < 0.95):
        # Append the region to the text regions list
        text_regions.append(region)

# Create a mask image with zeros
mask = np.zeros_like(gray)

# Loop over the text regions and draw white rectangles on the mask image
for region in text_regions:
    # Get the bounding box coordinates of the region
    minr, minc, maxr, maxc = region.bbox

    # Draw a white rectangle on the mask image
    cv2.rectangle(mask, (minc, minr), (maxc, maxr), (255, 255, 255), -1)

# Invert the mask image to get black rectangles on white background
mask = 255 - mask

# Apply bitwise and operation between the original image and the mask image
result = cv2.bitwise_and(img, img, mask=mask)

# Save the result image
cv2.imshow("result.jpg", result)
cv2.waitKey()
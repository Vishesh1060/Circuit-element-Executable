import cv2
import pytesseract

image = cv2.imread('../MLv2/imgs/sv_ (73).jpg')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 5)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
clean = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

config = r'--psm 6' # Assume a block of text of uniform font size and style
text_regions = pytesseract.image_to_data(clean, output_type=pytesseract.Output.DICT, config=config)
for i in range(len(text_regions['level'])):
    x = text_regions['left'][i]
    y = text_regions['top'][i]
    w = text_regions['width'][i]
    h = text_regions['height'][i]
    
    clean[y:y+h, x:x+w] = 0

result = cv2.bitwise_and(image, image, mask=clean)

cv2.imshow('result', result)

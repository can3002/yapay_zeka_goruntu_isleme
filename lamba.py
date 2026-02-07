import cv2
import numpy as np

img = cv2.imread("lamba.jpeg")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#kırmızı için değerler
red_lower = np.array([0, 100, 100])
red_upper = np.array([10, 255, 255])
#satı için değerler
yellow_lower = np.array([20, 100, 100])
yellow_upper = np.array([35, 255, 255])
# yeşil için değerler
green_lower = np.array([40, 50, 50])
greeN_upper = np.array([80, 255, 255])

mask1 = cv2.inRange(hsv,red_lower,red_upper)
mask2 = cv2.inRange(hsv,yellow_lower,yellow_upper)
mask3 = cv2.inRange(hsv,green_lower,greeN_upper)

#kırmızı gürültü azaltma
kernel1 = np.ones((2,2),np.uint8)
mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, kernel1)
#sarı gürültü azaltma
kernel2 = np.ones((2,2),np.uint8)
mask2 = cv2.morphologyEx(mask2, cv2.MORPH_OPEN, kernel2)
#yeşil gürültü azaltma
kernel3 = np.ones((2,2),np.uint8)
mask3 = cv2.morphologyEx(mask3, cv2.MORPH_OPEN, kernel3)

contours1, _ = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours2, _ = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours3, _ = cv2.findContours(mask3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if contours1 :
    #kırmızı kontür
    largest_contour1 = max(contours1, key=cv2.contourArea)
    (x,y), radius = cv2.minEnclosingCircle(largest_contour1)
    center = (int(x), int(y))
    radius = int(radius)
    cv2.circle(img, center, radius, (0,255,0), 3)
if contours2:
    #sari kontür
    lc = max(contours2, key=cv2.contourArea)
    (x1,y1), r = cv2.minEnclosingCircle(lc)
    c = (int(x1), int(y1))
    r = int(r)
    cv2.circle(img,c,r,(255,0,0),3)
if contours3:    
     #yeşil kontür
    lc1 = max(contours3, key=cv2.contourArea)
    (x2,y2), r1 = cv2.minEnclosingCircle(lc1)
    c1 = (int(x2),int(y2))
    r1 = int(r1)
    cv2.circle(img,c1,r1,(0,0,255), 3)

cv2.imshow("Top algılama", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
import cv2 as cv
import sys
 
img = cv.imread("/app/images/starry_night.jpg") # correct path for Docker container
 
if img is None:
    sys.exit("Could not read the image.")
 
cv.imshow("Display window", img)
k = cv.waitKey(0)
 
if k == ord("s"):
    cv.imwrite("starry_night.png", img)
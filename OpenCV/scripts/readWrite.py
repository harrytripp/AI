import cv2 as cv
import sys
import os

# Ensure output directory exists
os.makedirs("/app/imageOutput", exist_ok=True)

img = cv.imread("/app/images/starry_night.jpg")
if img is None:
    sys.exit("Could not read the image.")

cv.imwrite("/app/imageOutput/starry_night.png", img)
print("Image successfully saved to /app/imageOutput/starry_night.png")
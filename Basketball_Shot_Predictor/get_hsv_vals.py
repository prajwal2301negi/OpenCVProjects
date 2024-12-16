import math
import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
import numpy as np

# Initialize the Video
cap = cv2.VideoCapture('Videos/vid (6).mp4')


# Create the color Finder object
myColorFinder = ColorFinder(True) # False -> No debug Mode
hsvVals = 'red'


while True:

    # Two things->

    # 1.Grab the image
    success, img = cap.read()
    # img = cv2.imread("Ball.png")
    img = img[0:900, :]


    # Find the Color Ball
    imgColor, mask = myColorFinder.update(img, hsvVals) 


    cv2.imshow("ImageColor", imgColor)
    cv2.waitKey(100)



#     {'hmin': 0, 'smin': 0, 'vmin': 0, 'hmax': 179, 'smax': 255, 'vmax': 255}
#     {'hmin': 0, 'smin': 0, 'vmin': 0, 'hmax': 179, 'smax': 255, 'vmax': 255}
#     {'hmin': 0, 'smin': 0, 'vmin': 0, 'hmax': 179, 'smax': 255, 'vmax': 255}
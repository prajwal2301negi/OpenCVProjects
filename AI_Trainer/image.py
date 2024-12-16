# We will detect angle using 3 points, and then count the number of curls using this.
# We will mark the body parts as numbers and calculate the angle between the numbers. Eg -> angle between 11, 12, 13.
# Based on the angle, we will find the number of curls.

import cv2
import numpy as np
import time

import Pose_Detection_Module as pm

# We will use text Image for angles and then videos for curls
cap = cv2.VideoCapture("Videos/1.mp4")

detector = pm.poseDetector()

while True:

    # Video
    # success, img = cap.read()
    # img = cv2.resize(img, (1280, 720))



    # Image
    img = cv2.imread("Images/2.jpg")
    img = detector.findPose(img, False)

    lmList = detector.findPosition(img, False)

    if len(lmList) != 0:
        # see pose_detection_image for points reference
        # Right Arm
        detector.findAngle(img, 12, 14, 16)

        # Left Arm
        detector.findAngle(img, 11, 13, 15)


    cv2.imshow("Image", img)
    cv2.waitKey(1)
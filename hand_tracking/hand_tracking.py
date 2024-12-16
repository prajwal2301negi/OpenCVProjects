import cv2
import time

cap = cv2.VideoCapture(0)
cap.set(3, 1080)
cap.set(4, 720)

pTime = 0
cTime = 0

# Hand Tracking Module from cv-zone -->
# from cvzone.HandTrackingModule import HandDetector
# detector = HandDetector(detectionCon=0.8)

import HandTrackingModule as htm
detector = htm.handDetector(maxHands=1)

while True:
    success, img = cap.read()

    # Find Hand
    img = detector.findHands(img)

    # Find Landmark
    lmList, bbox = detector.findPosition(img) # lmList and bounding_box_info


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)



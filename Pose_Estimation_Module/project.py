import cv2
import mediapipe as mp
import time

import PoseEstimationModule as pm


cap = cv2.VideoCapture('PoseVideos/4.mp4')
pTime = 0

detector = pm.poseDetector(mode=False, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5)


    # Check if the video file is opened successfully
if not cap.isOpened():
    print("Error: Cannot open video file.")
    exit()

while True:
    success, img = cap.read()
    if not success:
        print("Video ended or failed to read.")
        break

    img = detector.findPose(img)

    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED) 

    cTime = time.time()
    fps = 1 / (cTime - pTime)  
    pTime = cTime   
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
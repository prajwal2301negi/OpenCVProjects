import cv2
import numpy as np
import HandTrackingModule as htm
import time

# Parameters
wCam, hCam = 640, 480
frameR = 100 # frame reduction
wScr, hScr = 1920, 1080  # Screen width and height
pTime = 0

smoothening = 7 # for smoothening the motion
plocX, plocY = 0, 0
clocX, clocY = 0, 0


# Steps->
# 1. Find hand landmarks
# 2. Get the tip of the index and middle fingers
# 3. Check which fingers are up
# 4. Only IndexFinger: Moving Mode
# 5. COnvert coordinates
# 6. Smoothen values
# 7. Move the mouse
# 8. Both index and middle fingers are up: Clicking Mode
# 9. FInd distance between fingers
# 10. Click mouse if distance apart
# 11. Frame rate
# 12. Display


# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(3, wCam)  # Set camera width
cap.set(4, hCam)  # Set camera height

# Initialize hand detector
detector = htm.handDetector(maxHands=1)

while True:
    # 1. Capture frame and detect hands
    success, img = cap.read()
    if not success:
        print("Failed to capture frame from camera.")
        break

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)


    # 2. Get the tip of index and middle fingers
    x1, y1, x2, y2 = None, None, None, None

    if len(lmList) > 8:
        x1, y1 = lmList[8][1:]  # Index finger tip
        # 8th landmark coordinates (should be [524, 220])
    if len(lmList) > 12:
        x2, y2 = lmList[12][1:]  # Middle finger tip
        # 12th landmark coordinates (should be [466, 174])
    # ([], [])
    # ([], [])
    # ([], []) 
    # ([[0, 388, 424], [1, 456, 378], [2, 497, 312], [3, 528, 255], [4, 568, 211], [5, 432, 205], [6, 448, 133], [7, 470, 96], [8, 494, 67], [9, 389, 197], [10, 374, 115], [11, 377, 61], [12, 389, 20], [13, 352, 208], [14, 337, 131], [15, 350, 83], [16, 375, 47], [17, 321, 232], [18, 302, 169], [19, 316, 130], [20, 345, 101]], (302, 20, 568, 424))  


    # 3. Check which fingers are up
    fingers = detector.fingersUp() if lmList else []

    if len(fingers) >= 3:
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2) # setting detection to a particular frame


        # 4. Only Index Finger : Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:
            if x1 is not None and y1 is not None:


                # 5. Convert coordinates from camera to screen
                x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))
              

                # 6. Smoothen values 
                clocX = plocX + (x3 - plocX) /smoothening
                clocY = plocY + (y3 - plocY) /smoothening
                

                # 7. Move the mouse
                x1, y1 = int(x1), int(y1)  # Ensure they are integers
                if 0 <= x1 < wCam and 0 <= y1 < hCam:  # Bounds check
                    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                else:
                    print(f"Coordinates out of bounds: x1={x1}, y1={y1}")
                plocX, plocY = clocX, clocY    
        else:
            print(f"Finger states: {fingers}")
    


        # 8. Both Index and Middle Finger are up: Clicking Mode
        if fingers[1] == 1 and fingers[2] == 0:


            # 9. Find distance between the fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)  #landmark 8 and landmark 12


            # 10. Click mouse if distance is short
            if length<70:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
    else:
        print("hand not detected.")


    # 11. Frame rate calculation
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)


    # 12. Display the frame
    cv2.imshow("Hand Tracking", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()

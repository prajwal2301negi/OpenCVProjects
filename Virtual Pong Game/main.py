import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Importing all images
imgBackground = cv2.imread("Resources/Background.png")
imgGameOver = cv2.imread("Resources/gameOver.jpg")
imgBall = cv2.imread("Resources/Ball.jpg", cv2.IMREAD_UNCHANGED)
imgBat1 = cv2.imread("Resources/bat1.png", cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread("Resources/bat2.png", cv2.IMREAD_UNCHANGED)

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Variables
ballPos = [100, 100] # default ball posititon

# ball speed
speedX = 15
speedY = 15

# flag 
gameOver = False

# score
score = [0, 0]


while True:
    _, img = cap.read()
    img = cv2.flip(img, 1) # 0 -> horizontal, 1-> vertical.
    imgRaw = img.copy()  # creating copy of our image



    # Find the hand and its landmarks
    hands, img = detector.findHands(img, flipType=False)  # don't flip the image(left hand will be left now and vice versa)



    # Resize the background image to match the frame size
    imgBackground = cv2.resize(imgBackground, (img.shape[1], img.shape[0]))



    # If the background image has an alpha channel, convert it to 3 channels
    if imgBackground.shape[2] == 4:
        imgBackground = cv2.cvtColor(imgBackground, cv2.COLOR_BGRA2BGR)



    # Overlaying the background image
    img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0) # 0.2 and 0.8, negative of each other will be given.



    # Check for hands
    if hands: # Based on left and right, we will put our hands left and right.
        for hand in hands:
            x, y, w, h = hand['bbox'] # extracting coordinates
            h1, w1, _ = imgBat1.shape
            y1 = y - h1 // 2 # for taking finger in the middle of bat
            y1 = np.clip(y1, 20, 415) # clipping below value se that bat not move down. CLipping y1 and min, max values. Added margin to y1



            if hand['type'] == "Left": # if hand in left side, put bat in left side
                img = cvzone.overlayPNG(img, imgBat1, (59, y1))
                if 59 < ballPos[0] < 59 + w1 and y1 < ballPos[1] < y1 + h1:  # if ball is between batarea, ball has hit the bat
                    # Reversing direction ox x, as ball hit by bat cnd chaging other parameters.
                    speedX = -speedX
                    ballPos[0] += 30
                    score[0] += 1


            if hand['type'] == "Right":
                img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
                if 1195 - 50 < ballPos[0] < 1195 and y1 < ballPos[1] < y1 + h1:
                    speedX = -speedX
                    ballPos[0] -= 30  # observe left hand parameter 
                    score[1] += 1




    # Game Over 
    if ballPos[0] < 40 or ballPos[0] > 1200:   # when ball goes outside 
        gameOver = True




    if gameOver:
        img = imgGameOver
        # Displaying score if game over
        cv2.putText(img, str(score[1] + score[0]).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX, 2.5, (200, 0, 200), 5)

    else:
        # If game is not over, move the ball

        # Move the Ball 
        # bounce from the wall
        if ballPos[1] >= 500 or ballPos[1] <= 10:
            speedY = -speedY # changing the direction

        # telling ball chage ball position
        ballPos[0] += speedX
        ballPos[1] += speedY
        



        # Ensure the ball image has an alpha channel (if not, add one)
        if imgBall.shape[2] == 3:  # If the image has only 3 channels (RGB)
            imgBall = cv2.cvtColor(imgBall, cv2.COLOR_RGB2BGRA)  # Convert to RGBA




        # Now you can safely overlay the ball image
        # Drawing ball
        img = cvzone.overlayPNG(img, imgBall, ballPos)



        # Displaying Score
        cv2.putText(img, str(score[0]), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
        cv2.putText(img, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)



    imgHeight, imgWidth, _ = img.shape
    rawHeight, rawWidth, _ = imgRaw.shape
        # Ensure we're within bounds before overlaying
    if imgHeight >= 700 and imgWidth >= 233: 
        # Resize imgRaw and overlay it on img
        img[580:700, 20:233] = cv2.resize(imgRaw, (213, 120))  # imgRaw is copy of image (see above)
    else:
        print("Image dimensions are smaller than expected. Skipping overlay.")



    cv2.imshow("Image", img)
    key = cv2.waitKey(1)


    if key == ord('r'):
        # Resetting the game
        ballPos = [100, 100]
        speedX = 15
        speedY = 15
        gameOver = False
        score = [0, 0]
        imgGameOver = cv2.imread("Resources/gameOver.png")
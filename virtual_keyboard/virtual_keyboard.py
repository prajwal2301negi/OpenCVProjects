import cv2
import time

from time import sleep

# for simulating keyboard
from pynput.keyboard import Controller


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

# Alphabets in keyboard
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]


# Text to be displayed after pressing key
finalText = ""

keyboard = Controller()

# Drawing Keys
def drawALL(img, buttonList):
        for button in buttonList: 
            x, y = button.pos
            w, h = button.size # width and height
            cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
            cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

        return img    


# Displaying QWERTY Keyboard -->
class Button():
    def __init__(self, pos, text, size = [85, 85]):
        self.pos = pos
        self.size = size
        self.text = text
        # It will not run single time as image changes every time, but buttons run single time only.


# Buttons
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i+ 50], key))

# myButton1 = Button([100, 100], "Q")
# myButton2 = Button([100, 100], "W")
# myButton3 = Button([100, 100], "E")
# myButton4 = Button([100, 100], "R")
# myButton5 = Button([100, 100], "T")
# myButton6 = Button([100, 100], "Y")

while True:
    success, img = cap.read()

    # Find Hand
    img = detector.findHands(img)

    # Find Landmark
    lmList, bbox = detector.findPosition(img) # lmList and bounding_box_info

    # Displaying Single Button -->
    # cv2.rectangle(img, (100, 100), (200, 200), (255, 0, 255), cv2.FILLED)
    # cv2.putText(img, "Q ", (115, 180), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    # Displaying Buttons QWERTY ->
    # img = myButton1.draw(img)
    # img = myButton2.draw(img)
    # img = myButton3.draw(img)
    # img = myButton4.draw(img)
    # img = myButton5.draw(img)
    # img = myButton6.draw(img)

    # Displaying Buttons
    img = drawALL(img, buttonList)

    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size
            # print("X",x)
            # print("Y",y)
            # X 950
            # Y 250

            # print(lmList)-> lmList has [id, x, y] structure.
            # [[0, 711, 546], [1, 677, 555], [2, 626, 532], [3, 585, 498], [4, 555, 464], [5, 688, 466], [6, 599, 442], [7, 571, 462], [8, 565, 472], [9, 700, 440], [10, 603, 431], [11, 589, 458], [12, 598, 471], [13, 701, 422], [14, 608, 416], [15, 603, 445], [16, 619, 458], [17, 694, 407], [18, 620, 401], [19, 614, 427], [20, 627, 442]]
            

            # lmList[8][0] # Index finger tip
            if x < lmList[8][1] < x + w and y < lmList[8][2] < y + h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                # will be detecting click as the shortest distance between index and middle finger
                l, _, _ = detector.findDistance(8, 12, img, draw = False) # l is the length ie distance


                # print(l) --> (distance between middle and index finger)
                # 42.80186911806539
                # 42.720018726587654
                # 175.8237754116319
                # 185.951606607740
                # 189.4650363523571
                # 191.9713520294109

                if l<45:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                    finalText += button.text  

                    # to delay typing to prevent overtyping
                    sleep(0.15)  


    # when clicked
    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 427), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)   
             
    # Frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)



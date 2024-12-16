import cv2
from cvzone.HandTrackingModule import HandDetector

import time

class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value


    def draw(self, img):    
    
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width,self.pos[1]+self.height), (225, 225, 225), cv2.FILLED)

        # Adding border around it
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width,self.pos[1]+self.height), (50, 50, 50), 3)

        # 9
        cv2.putText(img, self.value, (self.pos[0] + 40, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)
     

    def checkClick(self, x, y):
        #x1<x<x1+width 
        if self.pos[0]<x<self.pos[0] + self.width and \
        self.pos[1]<y<self.pos[1] + self.height:
            cv2.rectangle(img, self.pos, (self.pos[0]+self.width,self.pos[1]+self.height), (255, 255, 255), cv2.FILLED)

            # Adding border around it
            cv2.rectangle(img, self.pos, (self.pos[0]+self.width,self.pos[1]+self.height), (50, 50, 50), 3)

            # '9'
            cv2.putText(img, self.value, (self.pos[0] + 25, self.pos[1] + 80), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 5)

            return True
        
        else:
            return False
     
# Webcam
cap = cv2.VideoCapture(0)

cap.set(3, 1280) # changing WIDTH id->3
cap.set(4, 720) #changing HEIGHT id->4

# Initialization
detector = HandDetector(detectionCon = 0.8, maxHands = 1)

# Creating Buttons
buttonListValues = [['7', '8', '9', '*'],
                    ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'],
                    ['0', '/', '.', '=']]


# button1 = Button((700, 150), 100, 100, '5' )
buttonList = []
# for x in range(4):
#     xpos = x*100 + 800
#     ypos = 100+ 150
#     buttonList.append(Button((xpos, ypos), 100, 100, '5'))    # 5, 5, 5, 5
for x in range(4):
    for y in range(4):
        xpos = x * 100 + 800
        ypos = y * 100 + 150
        buttonList.append(Button((xpos, ypos), 100, 100, buttonListValues[y][x]))   


# Variables
myEquation = ''

DelayCounter = 0

# Loop
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1) # if use 0, then flip vertically. As use 1 --> flip horizontally.


    # Hand Detection
    # Using mediapipe in backend to detect hand and will return a list and an image with drawing.
    hands, img = detector.findHands(img, flipType=False)

    # Draw all buttons
    cv2.rectangle(img, (800, 50), (800 + 400, 70 + 100), (225, 225, 225), cv2.FILLED)

    # Adding border around it
    cv2.rectangle(img, (800, 50), (800 + 400, 70 + 100), (50, 50, 50), 3)


    # Draw all buttons
    for button in buttonList:
        button.draw(img)


    # Processing
    if hands:
        lmList = hands[0]['lmList']
        # Pass only the first two elements (x, y) to findDistance
        length, _, _ = detector.findDistance(lmList[8][:2], lmList[12][:2])  # Only x and y

        x, y = lmList[8][:2] # main finger x and y

        if length<50:
            for i, button in enumerate(buttonList):
                if button.checkClick(x, y) and DelayCounter == 0:
                    myValue = buttonListValues[int(i%4)][int(i/4)]
                    if myValue == "=":
                        myEquation = str(eval(myEquation))
                    else:    
                        myEquation += myValue
                    # time.sleep(0.2)    not best way to do it ---> avoiding duplicates
                    DelayCounter = 1 # starting counter


    # To avoid Duplicate
    if DelayCounter !=0:
        DelayCounter += 1
        if DelayCounter > 10:
            DelayCounter = 0


    # Display the Equation/Result   
    cv2.putText(img, myEquation, (810, 120), cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)

    cv2.imshow("img", img)
    key = cv2.waitKey(1)

    if key == ord('c'):
        myEquation = ''

import os
import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread("Background.png")


# Importing all the mode images to a list
folderPathModes = "Modes"
listImgModesPath = os.listdir(folderPathModes)
listImgModes = []
for imgModePath in listImgModesPath:
    listImgModes.append(cv2.imread(os.path.join(folderPathModes, imgModePath)))



# Importing all the icons to a list -> Icons to be placed at bottom
folderPathIcons = "Icons"
listImgIconsPath = os.listdir(folderPathIcons)
listImgIcons = []
for imgIconsPath in listImgIconsPath:
    listImgIcons.append(cv2.imread(os.path.join(folderPathIcons, imgIconsPath)))    




# for changing selection mode
modeType = 0  

# if selection == 0, then option 1 (mapping of options)
selection = -1

# we draw counter so that up to that time if we hold up the finger and process if we want to select virtually that option
counter=0

# speed for the ellipse
selectionSpeed = 7

detector = HandDetector(detectionCon=0.8, maxHands=1)

# Positions for mapping of options with fingers, center of the options(images)
modePositions = [(1136, 196), (1000, 384), (1136, 581)]

# counterPause -> once we select, there should be a pause, when pause is complete we should be able to select next, otherwise we will be keep selecting one option and too late for user to change option. Work when sitching between options.
counterPause = 0

# Each time we are selecting, goes here. Eg-> which sugar quantity we are selecting, which coffee we are selecting.
selectionList = [-1, -1, -1]  # will append selections here


while True:
    success, img = cap.read()

    # Find the hand and its landmarks
    hands, img = detector.findHands(img)

    # overlay our image with background
    imgBackground[139:139 + 480, 50:50 + 640] = img
    imgBackground[0:720, 847: 1280] = listImgModes[modeType]

    if hands and counterPause == 0 and modeType < 3:  # for not selecting confirm page, we are defining modeType

        # Hand 1
        hand1 = hands[0]
        fingers1 = detector.fingersUp(hand1)
        # print(fingers1)
        if fingers1 == [0, 1, 0, 0, 0]:
            if selection != 1: 
                counter = 1 
            selection = 1
        elif fingers1 == [0, 1, 1, 0, 0]:
            if selection != 2:
                counter = 1 # counter should reset to 1 and start back again, if we came to this finger after previous finger
            selection = 2
        elif fingers1 == [0, 1, 1, 1, 0]:
            if selection != 3:
                counter = 1
            selection = 3
        else:
            selection = -1
            counter = 0

        if counter > 0:
            counter += 1
            # print(counter)
            cv2.ellipse(imgBackground, modePositions[selection - 1], (103, 103), 0, 0, counter * selectionSpeed, (0, 255, 0), 20) 
            # modePosition[] is the location of center of options.
            # (103, 103) -> size of the radius in x and y direction.
            # 0, 0 -> starting angle of the ellipse
            # counter * selectionSpeed -> ending angle of the ellipse
            # (0, 255, 0) -> color of the ellipse
            # 20 -> thickness of the ellipse


            if counter * selectionSpeed > 360:
                selectionList[modeType] = selection

                # increasing modeType -> it goes to next selection
                modeType += 1
                counter = 0
                selection = -1
                counterPause = 1


    # To pause after each selection is made
    if counterPause > 0:
        counterPause += 1
        if counterPause > 60:  # wait for 60 iterations
            counterPause = 0


    # Add selection icon at the bottom
    if selectionList[0] != -1:
        imgBackground[636:636 + 65, 133:133 + 65] = listImgIcons[selectionList[0] - 1]
    if selectionList[1] != -1:
        imgBackground[636:636 + 65, 340:340 + 65] = listImgIcons[2+selectionList[1]]
    if selectionList[2] != -1:
        imgBackground[636:636 + 65, 542:542 + 65] = listImgIcons[5+selectionList[2]]


    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()    

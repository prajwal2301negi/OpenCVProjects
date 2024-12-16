import cv2
import time

import numpy as np
import handTrackingModule as htm


import math

# pychaw library helps us to change volume of our computer


#################
wCam, hCam = 640, 480
###################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.8)

# pychaw
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Other features-->
# volume.GetMute()
# volume.GetMasterVolumeLevel()

# print(volume.GetVolumeRange())  # -65 to 0,
# 0 will be max and -65 will be m in
# volume.SetMasterVolumeLevel(# volume form -65 to 0, None)

volRange = volume.GetVolumeRange()

# setting names of volume
minVol = volRange[0]
maxVol = volRange[1] 

# Initial Values
volBar = 400
vol = 0
volPer = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img) # This will give us the hands
    lmlist = detector.findPosition(img, draw=False)  # landmark list
    if len(lmlist) != 0:
    #   print(lmlist[4], lmlist[8])

      x1, y1 = lmlist[4][1], lmlist[4][2]  # 1st element as x and second element as y

      x2, y2 = lmlist[8][1], lmlist[8][2]  # 1st element as x and second element as y

       # Getting middle point of line
      cx, cy = (x1+x2)//2, (y1+y2)//2

      # THUMB
      cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
      
      # INDEX FINGER
      cv2.circle(img, (x2,y2), 15, (255,0,255), cv2.FILLED)

      # LINE b/w thumb and finger
      cv2.line(img, (x1,y1),(x2,y2),(255,0,255),3)

      cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED)

      # Distance formula 
      length = math.hypot(x2-x1, y2-y1)


      # hand Range -> 50 to 200
      # volume range -> -65 to 0

      vol = np.interp(length, [50, 200], [minVol, maxVol])  # minVOl and maxVol are the range we want to convert
    #   print(vol) -> will show volume by dist between index finger and thumb
      volBar = np.interp(length, [50, 200], [400, 150])
      volPer = np.interp(length, [50, 200], [0, 100])  


      volume.SetMasterVolumeLevel(vol, None)


      if length<50:
            cv2.circle(img, (cx,cy), 15, (0, 255, 0), cv2.FILLED)
         
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)          


    # adding Frame Rate
    cTime = time.time()
    fps = 1/(cTime-pTime) # currentTime - previousTime

    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 250, 0), 2 )


    cv2.imshow("img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()    
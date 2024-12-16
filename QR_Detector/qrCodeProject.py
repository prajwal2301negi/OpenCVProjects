import cv2
import numpy as np
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

with open('myDataFile.txt') as f:
    myDataList = f.read().splitlines()
# print(myDataList) --> ['10000001'] barcode reading


while True:    
    success, img = cap.read()
    for barcode in decode(img):
        myData = barcode.data.decode('utf-8')
        # print(myData) # 10000003 -> barcode shown

        if myData in myDataList:
            # print('Authorized')
            myOutput = 'Authorized'
            myColor = (0,255,0)
        else:
            # print('Not Authorized')
            myOutput = 'Not - Authorized'
            myColor = (0, 0, 255)

        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        # bounding box of rectangle
        cv2.polylines(img, [pts], True, myColor, 5)
        # Display Text info on barcode
        pts2 = barcode.rect
        cv2.putText(img, myOutput, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, myColor, 2)

    cv2.imshow('result', img)
    cv2.waitKey(1)    

import cv2
import numpy as np
# for detection of bar code and qr code and their position as well, and it will also decode the message for us well. 
from pyzbar.pyzbar import decode

img = cv2.imread('img.jpg')
code = decode(img)
# print(code)
# [Decoded(data=b'RAJEEV KUMAR ,CT-GD,IRLA-35200039,B-95,NAME DEP-RUBEE DEVI,WIFE', type='QRCODE', rect=Rect(left=528, top=62, width=149, height=149), polygon=[Point(x=528, y=210), Point(x=676, y=211), Point(x=677, y=63), Point(x=530, y=62)], quality=1, orientation='UP')]

for barcode in decode(img):
    # print(barcode.data) -->
    #b'RAJEEV KUMAR ,CT-GD,IRLA-35200039,B-95,NAME DEP-RUBEE DEVI,WIFE'
    myData = barcode.data.decode('utf-8') # decoding data
    # print(myData) -->
    # RAJEEV KUMAR ,CT-GD,IRLA-35200039,B-95,NAME DEP-RUBEE DEVI,WIFE


import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set width
cap.set(4, 720)   # Set height
detector = HandDetector(detectionCon=0.8)

colorR = (255, 0, 255)  # Initial color for the rectangle

cx, cy, w, h = 100, 100, 200, 200


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flip image horizontally, horizontal flip = 1, vertical flip = 0

    hands, img = detector.findHands(img)  # Use findHands to get all deteced hands
    if hands:

        # l, _, _ = detector.findDistance(8, 12, img)
        # # Two fingers dist

        # if l<30:

        lmList = hands[0]["lmList"]  # Get landmarks of the first detected hand
        cursor = lmList[8]  # Access the landmark for the index finger

        if cx-w//2 < cursor[0] < cx+w//2 and cy-h/2 < cursor[1] < cy+h//2:
                colorR = (0, 255, 0)  # Change color to green when finger is within the rectangle
                cx, cy = cursor[0], cursor[1]

        else:
            colorR = (255, 0, 255)  

        cv2.rectangle(img, (cx-w//2, cy-h//2), (cx+w//2,cy+h//2), colorR, cv2.FILLED)
            

    if not success:
            print("Failed to capture image")
            break

    cv2.imshow("image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()  
cv2.destroyAllWindows()  

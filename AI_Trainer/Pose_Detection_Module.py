import cv2
import mediapipe as mp
import time
import math

class poseDetector():

    def __init__(self, mode = False, upBody = False, smooth = True, detectionCon = 0.5, trackCon = 0.5):

        self.mode = mode # whenever we create new objects, it has its own variables.
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # Initialize MediaPipe Pose and drawing utilities
        self.mpPose = mp.solutions.pose
        self.mpDraw = mp.solutions.drawing_utils
        # self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth, self.detectionCon, self.trackCon)
        self.pose = self.mpPose.Pose(
            static_image_mode=self.mode,
            # upper_body_only=self.upBody,
            smooth_landmarks=self.smooth,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )


    def findPose(self, img, draw = True):
        # Convert the image to RGB as MediaPipe expects RGB input
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        # Draw pose landmarks on the original BGR image
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks( img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img  



    def findPosition(self, img, draw = True):   
        self.lmList = []

        if self.results.pose_landmarks:  
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        return self.lmList  

    def findAngle(self, img, p1, p2, p3, draw = True):
        # Calculate the angle between three points

        # Get the landmarks
        x1, y1 = self.lmList[p1][1:] # [3, 485, 281], it will take 3 in p1 and rest and in 1:(ignore 1 and take rest of it).
        x2, y2 = self.lmList[p2][1:] 
        x3, y3 = self.lmList[p3][1:]

        # Calculate the angle
        angle = math.degrees(math.atan2(y3-y2, x3-x2) - math.atan2(y1-y2, x1-x2))

        # print(angle)
        # 86.00908690157023
        # 86.00908690157023
        # 86.00908690157023

        if angle < 0:
            angle += 360

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (255, 0, 0), 2)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 0), 2)
            cv2.circle(img, (x3, y3), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (255, 0, 0), 2)
            cv2.putText(img, str(int(angle)), (x2-50, y2+50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)
            
        return angle    


def main():

    cap = cv2.VideoCapture('PoseVideos/4.mp4')
    pTime = 0
    # detector = poseDetector()
    detector = poseDetector(mode=False, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5)


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

        # if len(lmList) != 0:
        #     cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)

        cTime = time.time()
        fps = 1 / (cTime - pTime)  
        pTime = cTime      

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
import cv2
import mediapipe as mp
import time


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
        lmList = []

        if self.results.pose_landmarks:  
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        return lmList            


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
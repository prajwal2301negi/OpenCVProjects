import cv2
import numpy as np
import time

import Pose_Detection_Module as pm

# We will use text Image for angles and then videos for curls
cap = cv2.VideoCapture("Videos/1.mp4")

# # Create a VideoWriter object to save the output video
# fourcc = cv2.VideoWriter_fourcc(*'MP4V')  
# out = cv2.VideoWriter('output_video.mp4', fourcc, 60.0, (1280, 720))  # 60fps, 1280x720 resolution

detector = pm.poseDetector()

# Parameters
dir = 0  # 0 for up, 1 for down
count = 0

while True:
    # Video
    success, img = cap.read()
    if not success:
        break
    img = cv2.resize(img, (1280, 720))

    # Image
    # img = cv2.imread("Images/2.jpg")
    img = detector.findPose(img, False)

    lmList = detector.findPosition(img, False)

    if len(lmList) != 0:

        # see pose_detection_image for points reference
        # Right Arm
        angle = detector.findAngle(img, 12, 14, 16)

        # Left Arm
        # angle = detector.findAngle(img, 11, 13, 15)


        # # Write the frame to the video file
        # out.write(img)

        if angle is not None:  # Ensure angle is valid
            # Map angle to percentage
            per = np.interp(angle, (145, 25), (0, 100))

            # Check for dumbbell curls
            if per == 100:
                if dir == 0:
                    count += 0.5
                    dir = 1
            if per == 0:
                if dir == 1:
                    count += 0.5
                    dir = 0   

            # Display the count
            cv2.putText(img, str(int(count)), (50, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL, 5, (255, 0, 0), 5)        

        else:
        
            print("Angle not detected or is invalid!")

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

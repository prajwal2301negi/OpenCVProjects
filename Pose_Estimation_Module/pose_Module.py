import cv2
import mediapipe as mp

# Initialize MediaPipe Pose and drawing utilities
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# Open the video file
cap = cv2.VideoCapture('PoseVideos/4.mp4')

# Check if the video file is opened successfully
if not cap.isOpened():
    print("Error: Cannot open video file.")
    exit()

while True:
    success, img = cap.read()
    if not success:
        print("Video ended or failed to read.")
        break

    # Convert the image to RGB as MediaPipe expects RGB input
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)

    # Draw pose landmarks on the original BGR image
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Display the image with landmarks
    cv2.imshow("Pose Detection", img)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release the video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

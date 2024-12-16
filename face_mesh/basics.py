import cv2
import mediapipe as mp
import time

# Initialize Mediapipe Face Mesh and Drawing utilities
mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=2)

# Choose video source: 0 for webcam, or provide a video file path
video_source = 0  # Change to "Videos/1.mp4" for a video file
cap = cv2.VideoCapture(video_source)

if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()

pTime = 0  # Previous time for FPS calculation

while True:
    success, img = cap.read()
    if not success:
        print("Error: Could not read frame from video source.")
        break

    # Convert the image to RGB (required by Mediapipe)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)

    # Process and draw landmarks if faces are detected
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_TESSELATION, drawSpec, drawSpec)
            for id, lm in enumerate(faceLms.landmark):
                ih, iw, _ = img.shape
                x, y = int(lm.x * iw), int(lm.y * ih)
                # landmark coordinates
                print(f"ID: {id}, X: {x}, Y: {y}")


    cTime = time.time()
    fps = 1 / (cTime - pTime) if cTime != pTime else 0
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Face Mesh", img)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

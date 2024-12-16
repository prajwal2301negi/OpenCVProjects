import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import google.generativeai as genai
from PIL import Image # for sending image
import streamlit as st

st.set_page_config(layout="wide")
st.image('MathGestures.png')
 
col1, col2 = st.columns([3,2])
with col1:
    run = st.checkbox('Run', value=True)
    FRAME_WINDOW = st.image([])
 
with col2:
    st.title("Answer")
    output_text_area = st.subheader("")
 

 
genai.configure(api_key="ENTER_YOUR_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')
 

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
 

# Initialize the HandDetector class with the given parameters
detector = HandDetector(staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.7, minTrackCon=0.5)
 
 
def getHandInfo(img):
    # Find hands in the current frame
    # The 'draw' parameter draws landmarks and hand outlines on the image if set to True
    # The 'flipType' parameter flips the image, making it easier for some detections
    hands, img = detector.findHands(img, draw=False, flipType=True)
 
    # Check if any hands are detected
    if hands:
        # Information for the first hand detected
        hand = hands[0]  # Get the first hand detected
        lmList = hand["lmList"]  # List of 21 landmarks for the first hand
        # Count the number of fingers up for the first hand
        fingers = detector.fingersUp(hand)
        # print(fingers)
        return fingers, lmList
    else:
        return None
 


def draw(info,prev_pos,canvas): 
    # get all the info of fingers
    fingers, lmList = info
    current_pos= None
    if fingers == [0, 1, 0, 0, 0]: # index finger 
        current_pos = lmList[8][0:2] # will give 0 and 1
        if prev_pos is None: prev_pos = current_pos # draw drop in this case
        # draw line between previous pt and new pt
        cv2.line(canvas,current_pos,prev_pos,(255,0,255),10)
    elif fingers == [1, 1, 1, 1, 1]: # to reset canvas -> all fingers up
        canvas = np.zeros_like(img)
 
    return current_pos, canvas 
 


def sendToAI(model,canvas,fingers):
    if fingers == [1,1,1,1,0]: # send to ai model when this finger configuration is done
        pil_image = Image.fromarray(canvas) # converting to PIL format
        response = model.generate_content(["Solve this math problem", pil_image]) # sending the image
        return response.text
 

 
prev_pos= None
canvas=None # as we will dra above canvas
image_combined = None
output_text= ""
# Continuously get frames from the webcam


while True:
    # Capture each frame from the webcam
    # 'success' will be True if the frame is successfully captured, 'img' will contain the frame
    success, img = cap.read()
    img = cv2.flip(img, 1) # flipping it horizontally
 
    if canvas is None:
        canvas = np.zeros_like(img) # black canvas
 
 
    info = getHandInfo(img)
    if info:
        fingers, lmList = info
        prev_pos,canvas = draw(info, prev_pos,canvas)
        output_text = sendToAI(model,canvas,fingers)
 
    image_combined= cv2.addWeighted(img, 0.7, canvas, 0.3, 0) # merging canvas and our image, image-> 0.7 and canvas -> 0.3

    FRAME_WINDOW.image(image_combined,channels="BGR")
 
    if output_text:
        output_text_area.text(output_text)
 
    # Display the image in a window
    cv2.imshow("Canvas", canvas)
    cv2.imshow("image_combined", image_combined)
 
 
    # Keep the window open and update it for each frame; wait for 1 millisecond between frames
    cv2.waitKey(1)
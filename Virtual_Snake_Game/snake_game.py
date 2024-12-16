import math
import random
import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector



# Terms ->
# 1. List of Points
# 2. List of Distances
# 3. Current Length
# 4. Total Length

# Methodology ->
# When we move our finger, it creates a new pt and then the distance between that pt and new pt is calculated. and we draw that line. 
# In this way, we add length ot the snake. the added length might be bigger than the length of snake and increase the length of the snake.
# We calculate few distance and based ont that, remove few of the lengths at the back.
# If total length formaed after new point is 190 and allowed maximum length is 175, then the points at the back will be remove. After reduction, length can be 167 also. But length cannot be more than 175.
# If the head collides with the length, game over. Compute the distance between head and each point, if any low below a threshold, collision detected.



cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)


detector = HandDetector(detectionCon=0.8, maxHands=1)



class SnakeGameClass:
    def __init__(self, pathFood):
        self.points = []  # all points of the snake
        self.lengths = []  # distance between each point
        self.currentLength = 0  # total length of the snake
        self.allowedLength = 150  # total allowed Length
        self.previousHead = 0, 0  # previous head point

        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood, _ = self.imgFood.shape  # dimension of food, to check if the snake has hit this dimension.
        self.foodPoint = 0, 0 # initial Point of food.
        self.randomFoodLocation() # randomly generating food location

        self.score = 0
        self.gameOver = False



    def randomFoodLocation(self):
        self.foodPoint = random.randint(100, 1000), random.randint(100, 600) # Random location of x and y for food(new locations of food)




    def update(self, imgMain, currentHead):
        # 1. If we are getting current head, we will put them in points[].
        # 2. Check dist between current head and previous head and put in length[].
        # 3. update current length to total length of the chain.
        if self.gameOver:
            cvzone.putTextRect(imgMain, "Game Over", [300, 400],scale=7, thickness=5, offset=20)
            cvzone.putTextRect(imgMain, f'Your Score: {self.score}', [300, 550], scale=7, thickness=5, offset=20)
        else:
            px, py = self.previousHead  # point 1
            cx, cy = currentHead  # current Head
            self.points.append([cx, cy]) # appending current head pts
            distance = math.hypot(cx - px, cy - py)  # point 2 (using distance formula)
            self.lengths.append(distance) # appending distance
            self.currentLength += distance # adding dist to current length of the snake. eg-> pLength = 50, added = 100, newLength = 150
            self.previousHead = cx, cy # updating previous heads ie current head




            # Length Reduction  (Step 2 of methodology)
            if self.currentLength > self.allowedLength:
                for i, length in enumerate(self.lengths):
                    self.currentLength -= length # will go through all the length and remove the lengths, Keep reducing until get the desired length.

                    self.lengths.pop(i) # removing from lengthlist
                    self.points.pop(i)  # removing from pointsList
                    if self.currentLength < self.allowedLength:
                        break




            # Check if snake ate the Food
            # when snake eat the food, random location of foode will generate again and length of snake increases.
            rx, ry = self.foodPoint # random x and y
            if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and \
                    ry - self.hFood // 2 < cy < ry + self.hFood // 2:
                self.randomFoodLocation()
                self.allowedLength += 50
                self.score += 1
                print(self.score)



            # Draw Snake
            if self.points: # if we have some points, then run it.
                for i, point in enumerate(self.points):
                    if i != 0: # if more than 0 [i-1] and [i] are the two points
                        cv2.line(imgMain, self.points[i - 1], self.points[i], (0, 0, 255), 20)
                        # drawing circle in snake [-1]-> last point
                cv2.circle(imgMain, self.points[-1], 20, (0, 255, 0), cv2.FILLED)




            # Draw Food
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood, (rx - self.wFood // 2, ry - self.hFood // 2)) #imgMain is the background Image and imgFood is the front Image
            cvzone.putTextRect(imgMain, f'Score: {self.score}', [50, 80], scale=3, thickness=3, offset=10)




            # Check for Collision (Point 3 Methodology)
            # we will use point polygon test -> to check if one point lies over the other point. # Polygon function will give the distance between all pts to the head except last and the next to head point.
            # Polgon test will give the minimum distance as the output.
            pts = np.array(self.points[:-2], np.int32) # take all pts except last two.
            pts = pts.reshape((-1, 1, 2)) # so that compatible with function
            cv2.polylines(imgMain, [pts], False, (0, 255, 0), 3) # Draw polygon paths to see snake goes to right path.
            minDist = cv2.pointPolygonTest(pts, (cx, cy), True) # to check if Donut has hit. pts -> all the pts of Donut. cx, cy -> head pts(current head pts to check if these pts hitting any of these pts, then it will give the output of distance, it can also give 0 or -1 output based on hitting the obstacle).
            # Right now if nearly 0 is the distance between Donut and snake, it is considered to be hit.




            if -1 <= minDist <= 1: # Increase the dist to make game difficult 
                print("Hit")
                self.gameOver = True # showing different screen when game over
                self.points = []  # all points of the snake
                self.lengths = []  # distance between each point
                self.currentLength = 0  # total length of the snake
                self.allowedLength = 150  # total allowed Length
                self.previousHead = 0, 0  # previous head point
                self.randomFoodLocation()

        return imgMain
    



game = SnakeGameClass("Donut.png")



while True:
    success, img = cap.read()
    img = cv2.flip(img, 1) # flipping
    hands, img = detector.findHands(img, flipType=False)


    if hands:
        lmList = hands[0]['lmList'] # first hand
        pointIndex = lmList[8][0:2] # index finger. (0,1) as we are not dealing in 3D.
        img = game.update(img, pointIndex) # updated image



    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    
    if key == ord('r'):
        game.gameOver = False
import cv2
import time
import os
import handTrackingModule as htm

# Video settings
cap = cv2.VideoCapture(0)
wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0

# Hand detector function
detector = htm.handDetector()

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    handedness = detector.findHandedness()
    lmList = detector.findPosition(img)

    if len(lmList) != 0:
        fingers = []

        # Check if fingers are open or not
        # Thumb 1 right hand, 0 left hand
        if handedness == 1:
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        else:
            if lmList[tipIds[0]][1] < lmList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)            

        # Other fingers
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
                
        # print(fingers)
        totalFingers = fingers.count(1)
        cv2.putText(img, f'Count: {int(totalFingers)}', (10, 60), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)
        
    # Fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key > -1:
        break

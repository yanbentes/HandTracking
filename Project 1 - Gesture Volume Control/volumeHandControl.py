import cv2
import time
import numpy as np
import handTrackingModule as htm
import math
import subprocess

cap = cv2.VideoCapture(0)
wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)

# Volume PipeWire/PulseAudio

while True:
    success, img = cap.read()

    # Hand detection
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:
        # print(lmList[4], lmList[8])
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2) // 2, (y1+y2) // 2
        
        cv2.circle(img, (x1,y1), 12, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 12, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 2)
        cv2.circle(img, (cx,cy), 8, (255,0,255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)

        if length < 50:
            cv2.circle(img, (cx,cy), 8, (0,255,0), cv2.FILLED)

        # Hand range 50 -> 300
        # Volume range
        
    # Fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)


    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key > -1:
        break

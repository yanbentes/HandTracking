import cv2
import time
import os
import handTrackingModule as htm
from playsound import playsound

def playSound(num):
    match num:
        case 0:
            return None
        case 1:
            playsound('sounds/mixkit-arcade-game-complete-or-approved-mission-205.wav')
        case 2:
            return playsound('sounds/mixkit-casino-bling-achievement-2067.wav')
        case 3:
            return playsound('sounds/mixkit-game-flute-bonus-2313.wav')
        case 4:
            return playsound('sounds/mixkit-flute-alert-2307.wav')
        case 5:
            return playsound('sounds/mixkit-ominous-drums-227.wav')
        case _:
            return None
        
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
        cv2.putText(img, f'{int(totalFingers)}', (10, 60), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)
        # playSound(totalFingers)

    # Fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key > -1:
        break

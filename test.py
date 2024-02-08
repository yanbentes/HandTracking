import cv2
import mediapipe as mp
import time
import handTrackingModule as htm

pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
        
    if len(lmList) != 0:
        print(lmList[4])
        
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 60), cv2.FONT_HERSHEY_PLAIN, 3,
                (0, 0, 255), 3)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key > -1:
        break

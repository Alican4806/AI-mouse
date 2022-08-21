import mediapipe as mp
import time


import numpy as np
import cv2 as cv
import autopy
import HandTrackingModule as htm
wCam , hCam = 640 , 480
frame = 100
get = cv.VideoCapture(0)
get.set(3,wCam)
get.set(4,hCam)
pTime = 0
detector = htm.handDetector(maxHands=1)

wScr,hScr = autopy.screen.size()
print(wScr,hScr)
while True:
    
    # 1 Find hand lanmarks
    success, cap = get.read()
    cap = cv.flip(cap,1) # The camera is reversed.
    img = detector.findHands(cap)
    landmark = detector.findPositon(img)
    
    
    if len(landmark) != 0:
        # print(detector.fingersUp)
        fingers = detector.fingersUp()
        
        # MOVING MODE 
        x1,y1 = landmark[8][1],landmark[8][2] # Information is received about the location of the index finger.
        xMiddle,yMiddle = landmark[12][1:]
        
        # The range of the screen and the frame are adjusted
        xp =np.interp(x1,[frame,wCam-frame],[0,wScr])
        yp = np.interp(y1,[frame,hCam-2*frame],[0,hScr])
        
        cv.rectangle(img,((frame),(frame)),((wCam-frame),(hCam-2*frame)),(250,50,100),2) # The bounded of the mouse is defined by rectangle.
        if fingers[1]==True and fingers[2]==False and fingers[3]==False and fingers[4]==False and fingers[0]==False:# Only index finger is up
            cv.circle(img,(x1,y1),10,(255,0,0),cv.FILLED)
            autopy.mouse.move(xp,yp) # Working move mode
            
        # CLICK MODE (when Index and middle finger are up)
        
        elif fingers[1]==True and fingers[2]==True and fingers[3]==False and fingers[4]==False and fingers[0]==False:
            Index = cv.circle(img,(x1,y1),10,(255,0,0),cv.FILLED)
            Middle = cv.circle(img,(xMiddle,yMiddle),10,(255,0,0),cv.FILLED)
            cv.line(img,(x1,y1),(xMiddle,yMiddle),(255,255,0),2)
            print(np.disp(Index,Middle))
            autopy.mouse.click()
        # if fingers[] == True:
        #     autopy.mouse.move(fingers[4][1],fingers[4][2])
        # if detector.fingersUp[1] == True:
        #     x1 , y1 = detector.fingersUp[1][1:]
        #     autopy.mouse.move(x1,y1)
    
    # 2 Find index and middle  finger position
    # 3 Index finger is up to move
    # 4 Index finger and middle finger are up for click mode
    # 5 
        
    
    # Fps
    cTime = time.time()
    fps = 1/(cTime-pTime)
    
    pTime = cTime
    cv.putText(cap,f'FPS:{(int(fps))}',(60,60),cv.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)
    
    
    if success == True:
        
        cv.imshow('image',img)
        
        if  cv.waitKey(5)& 0xFF == ord('a'):
            break
cv.destroyAllWindows()

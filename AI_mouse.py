from turtle import left
import mediapipe as mp
import time


import numpy as np
import cv2 as cv
import autopy
import HandTrackingModule as htm
#######################
wCam , hCam = 640 , 480
frame = 100
#######################
get = cv.VideoCapture(0)
get.set(3,wCam)
get.set(4,hCam)
pTime = 0
detector = htm.handDetector(maxHands=1)
cLocX,cLocY = 0, 0 # Current locations
pLocX , pLocY = 0, 0 # Previous locations
smooth =5 # smoothing cofficient
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
        xp =np.interp(x1,[frame,wCam-frame],[0,wScr]) # The ranges which are screen dimensions and frame dimensions, are equated each other.
        yp = np.interp(y1,[frame,hCam-2*frame],[0,hScr])
        
        cv.rectangle(img,((frame),(frame)),((wCam-frame),(hCam-2*frame)),(250,50,100),2) # The bounded of the mouse is defined by rectangle.
        if fingers[1]==True and fingers[2]==False and fingers[3]==False and fingers[4]==False and fingers[0]==False:# Only index finger is up
            # It will be more smooth
            cLocX = pLocX + (xp - pLocX)/ smooth
            cLocY = pLocY + (yp - pLocY)/ smooth
            pLocX = cLocX
            pLocY = cLocY
            cv.circle(img,(x1,y1),10,(255,0,0),cv.FILLED)
            autopy.mouse.move(cLocX,cLocY) # Working move mode
            cv.putText(img,'Moving mode is active',(int(wCam/3),hCam-30),cv.FONT_HERSHEY_PLAIN,1.6,(2,255,255),2)
        # CLICK MODE (when Index and middle finger are up)
        
        elif fingers[1]==True and fingers[2]==True and fingers[3]==False and fingers[4]==False and fingers[0]==False:
            
            distance = detector.fingerDistance(8,12,img,True) # 8 and 12 are points which are on the hand
            print(distance)
            if distance <35: # If the distance is less than 35 pixel, it will be working click mode
                cv.putText(img,'Clicking mode is active',(int(wCam/3),hCam-30),cv.FONT_HERSHEY_PLAIN,1.6,(255,255,255),2)
                autopy.mouse.click()
        elif fingers[1]==True and fingers[2]==True and fingers[3]==True and fingers[4]==False and fingers[0]==False:
            
            distance1 = detector.fingerDistance(8,12,img,True,5,2,(255,0,255),(0,0,255)) # 8 and 12 are points which are on the hand
            print(f'this is {distance1}')
            distance2 = detector.fingerDistance(12,16,img,True,5,2,(255,0,255),(0,0,255))
            print(f'this is {distance2}')
            if distance1 <30 and distance2 <30:
                cv.putText(img,'Right clicking is active',(int(wCam/3),hCam-30),cv.FONT_HERSHEY_PLAIN,1.6,(255,0,255),2)
                autopy.mouse.click(autopy.mouse.Button.RIGHT)
        elif fingers[1]==True and fingers[2]==True and fingers[3]==True and fingers[4]==True and fingers[0]==False:
            distance1 = detector.fingerDistance(8,12,img,True,5,2,(255,0,255),(0,0,255)) # 8 and 12 are points which are on the hand
            print(f'this is {distance1}')
            distance2 = detector.fingerDistance(12,16,img,True,5,2,(255,0,255),(0,0,255))
            print(f'this is {distance2}')
            distance3 = detector.fingerDistance(16,20,img,True,5,2,(255,0,255),(0,0,255))
            print(f'this is {distance3}')
            if distance1 <30 and distance2 <30 and distance3 < 43:
                cv.putText(img,'Roll clicking is active',(int(wCam/3),hCam-30),cv.FONT_HERSHEY_PLAIN,1.6,(255,0,0),2)
                autopy.mouse.click(autopy.mouse.Button.MIDDLE)
        elif fingers[1]==False and fingers[2]==False and fingers[3]==False and fingers[4]==False and fingers[0]==True:
        #     finger = not fingers[1]
            finger = True
            cv.putText(img,'back button is active',(int(wCam/3),hCam-30),cv.FONT_HERSHEY_PLAIN,1.6,(120,1200,0),2)
            autopy.key.toggle(autopy.key.Code.LEFT_ARROW,finger,[autopy.key.Modifier.ALT],1)
            # finger = fingers[1]
                # autopy.key.toggle(autopy.key.Code.LEFT,)
                # cv.circle(img,)
            # autopy.key.toggle(autopy.key.Code.UP_ARROW, False, [autopy.key.Modifier.CONTROL], 0)
            
            
        elif fingers[1]==False and fingers[2]==False and fingers[3]==False and fingers[4]==True and fingers[0]==False:
            finger = True
            cv.putText(img,'forward button is active',(int(wCam/3),hCam-30),cv.FONT_HERSHEY_PLAIN,1.6,(120,1200,0),2)
            autopy.key.toggle(autopy.key.Code.RIGHT_ARROW,finger,[autopy.key.Modifier.ALT],1)
            
        autopy.key.toggle(autopy.key.Code.LEFT_ARROW,False,[autopy.key.Modifier.ALT],0)
        autopy.key.toggle(autopy.key.Code.RIGHT_ARROW,False,[autopy.key.Modifier.ALT],0)
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

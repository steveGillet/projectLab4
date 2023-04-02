import cv2
import numpy as np
import time
#from adafruit_servokit import ServoKit
print(cv2.__version__)
timeMark=time.time()
dtFIL=0
 
def nothing(x):
    pass
 
cv2.namedWindow('TrackBars')
cv2.moveWindow('TrackBars',1320,0)
cv2.createTrackbar('hueLower', 'TrackBars',100,179,nothing)
cv2.createTrackbar('hueUpper', 'TrackBars',116,179,nothing)
cv2.createTrackbar('satLow', 'TrackBars',160,255,nothing)
cv2.createTrackbar('satHigh', 'TrackBars',255,255,nothing)
cv2.createTrackbar('valLow', 'TrackBars',150,255,nothing)
cv2.createTrackbar('valHigh', 'TrackBars',255,255,nothing)
#kit=ServoKit(channels=16)
 
# tilt=90
# pan=90
# dTilt=10
# dPan=1
 
# kit.servo[0].angle=pan
# kit.servo[1].angle=tilt
# kit.servo[2].angle=pan
# kit.servo[3].angle=tilt
 
width=720
height=480
flip=2
font=cv2.FONT_HERSHEY_SIMPLEX
camSet1='nvarguscamerasrc sensor-id=0 ee-mode=1 ee-strength=0 tnr-mode=2 tnr-strength=1 wbmode=3 ! video/x-raw(memory:NVMM), width=3264, height=2464, framerate=21/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.3 brightness=-.2 saturation=1.2 ! appsink drop=True'
camSet2='nvarguscamerasrc sensor-id=1 ee-mode=1 ee-strength=0 tnr-mode=2 tnr-strength=1 wbmode=3 ! video/x-raw(memory:NVMM), width=3264, height=2464, framerate=21/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.3 brightness=-.2 saturation=1.2 ! appsink drop=True'
 
#camSet='nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=3264, height=2464, framerate=21/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
#camSet ='v4l2src device=/dev/video1 ! video/x-raw,width='+str(width)+',height='+str(height)+',framerate=20/1 ! videoconvert ! appsink'
cam1=cv2.VideoCapture(camSet1)
cam2=cv2.VideoCapture(camSet2)
while True:
    _, frame1 = cam1.read()
    _, frame2 = cam2.read()
 
    hsv1=cv2.cvtColor(frame1,cv2.COLOR_BGR2HSV)
    hsv2=cv2.cvtColor(frame2,cv2.COLOR_BGR2HSV)
 
    hueLow=cv2.getTrackbarPos('hueLower', 'TrackBars')
    hueUp=cv2.getTrackbarPos('hueUpper', 'TrackBars')
 
    Ls=cv2.getTrackbarPos('satLow', 'TrackBars')
    Us=cv2.getTrackbarPos('satHigh', 'TrackBars')
 
    Lv=cv2.getTrackbarPos('valLow', 'TrackBars')
    Uv=cv2.getTrackbarPos('valHigh', 'TrackBars')
 
    l_b=np.array([hueLow,Ls,Lv])
    u_b=np.array([hueUp,Us,Uv])
 
    FGmask1=cv2.inRange(hsv1,l_b,u_b)
    FGmask2=cv2.inRange(hsv2,l_b,u_b)
 
    cv2.imshow('FGmask1',FGmask1)
    cv2.moveWindow('FGmask1',0,0)
 
    contours1,_ = cv2.findContours(FGmask1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours1=sorted(contours1,key=lambda x:cv2.contourArea(x),reverse=True)
    for cnt in contours1:
        area=cv2.contourArea(cnt)
        (x,y,w,h)=cv2.boundingRect(cnt)
        if area>=100:
            cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,255),3)
            break
    
    contours2,_ = cv2.findContours(FGmask2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours2=sorted(contours2,key=lambda x:cv2.contourArea(x),reverse=True)
    for cnt in contours2:
        area=cv2.contourArea(cnt)
        (x,y,w,h)=cv2.boundingRect(cnt)
        if area>=100:
            cv2.rectangle(frame2,(x,y),(x+w,y+h),(0,255,255),3)
            break
 
    frame3=np.hstack((frame1,frame2))
    dt=time.time()-timeMark
    timeMark=time.time()
    dtFIL=.9*dtFIL + .1*dt
    fps=1/dtFIL
    cv2.rectangle(frame3,(0,0),(150,40),(0,0,255),-1)
    cv2.putText(frame3,'fps: '+str(round(fps,1)),(0,30),font,1,(0,255,255),2)
 
    #cv2.imshow('myCam1',frame1)
    #cv2.imshow('myCam2',frame2)
    cv2.imshow('comboCam',frame3)
    cv2.moveWindow('comboCam',0,450)
    # kit.servo[0].angle=pan
    # kit.servo[2].angle=pan
    # pan=pan+dPan
    # if pan>=179 or pan<=1:
    #     dPan=dPan*(-1)
    #     tilt=tilt+dTilt
    #     kit.servo[1].angle=tilt
    #     kit.servo[3].angle=tilt
    #     if tilt>=169 or tilt<=11:
    #         dTilt=dTilt*(-1)
    if cv2.waitKey(1)==ord('q'):
        break
cam1.release()
cam2.release()
cv2.destroyAllWindows()